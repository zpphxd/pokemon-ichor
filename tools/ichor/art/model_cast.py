"""Export image-model-led named cast sources, not hand-authored native art.

python3 tools/ichor/art/model_cast.py --out DIR --review DIR
python3 tools/ichor/art/model_cast.py --write

The selected RGBA source crops are authoritative. Alpha is thresholded at
128, margins trimmed, and pixels reduced with nearest-neighbor sampling.
Walkers keep the engine's existing shared palettes byte-for-byte; portraits
use at most fifteen GBA colors. Kleon and Alethea quantize fronts/backs
together. Tiny accent hues may receive extra palette weight, never broad
red garments. Legacy polygon/ASCII writers must not overwrite these paths.
"""
import argparse
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).parent / "base/named_cast"
PEOPLE = Path("graphics/object_events/pics/people/ichor")
FRONT = Path("graphics/trainers/front_pics")
BACK = Path("graphics/trainers/back_pics")
WALKERS = (
    "aiakides", "alethea", "apollo", "cami", "demeter", "endeis",
    "kedalion", "kerykos", "kleon", "kleon_seasick", "kleon_tablet",
    "mom", "pheidon", "professor_daphne", "pronomos", "sam",
    "hierophant_ione", "titan_grunt",
)
PORTRAITS = (
    "alethea", "cami", "hierophant_ione", "hierophant_kerykos",
    "kleon", "professor_daphne", "sam", "titan_grunt",
)
INTRO = Path("graphics/birch_speech/birch.png")
OWNED = ({PEOPLE / f"{n}.png" for n in WALKERS}
         | {FRONT / f"{n}.png" for n in PORTRAITS}
         | {BACK / f"{n}.png" for n in ("kleon", "alethea")} | {INTRO})
ROBES = {"professor_daphne", "hierophant_ione", "mom", "endeis",
         "apollo", "cami", "demeter"}
FOLK = {"aiakides", "endeis", "kedalion", "mom", "pheidon", "pronomos"}
THEOXENIA = {"sam", "apollo", "cami", "demeter"}
FRONT_PHASES = {"professor_daphne": (.4, -.4)}
LEG_BOXES = {
    "aiakides": ((4, 26, 12, 32), (6, 26, 13, 32)),
    "alethea": ((4, 27, 12, 32), (6, 27, 14, 32)),
    "kerykos": ((4, 27, 11, 32), (6, 28, 12, 32)),
    "kleon": ((4, 26, 11, 32), (6, 26, 13, 32)),
    "kedalion": ((3, 26, 11, 32), (4, 26, 11, 32)),
    "pheidon": ((4, 26, 13, 32), (4, 26, 12, 32)),
    "sam": ((4, 27, 12, 32), (6, 28, 14, 32)),
}
# These are selection masks and measured joints in model-authored RGBA crops,
# not colored geometry. Bones register to the retained joints while keeping
# source-relative widths; hands/orbs use rigid uniform scaling and rotation.
# Source pixels only, nearest-neighbor, no mirrored costumes or seam painting.
ARM_PIECES = {
    "kleon": (
        (
            ([(16, 363), (75, 338), (104, 305), (154, 320), (175, 340),
              (170, 380), (116, 402), (48, 423), (12, 412)],
             ((151, 343), (28, 391))),
            ([(34, 267), (91, 260), (87, 310), (65, 365), (78, 397),
              (47, 418), (10, 412), (0, 386), (14, 330)],
             ((28, 391), (60, 270))),
            ([(35, 217), (53, 181), (95, 161), (125, 173), (136, 196),
              (139, 221), (124, 249), (91, 262), (64, 281), (34, 266)],
             ((60, 270), (99, 202))),
        ),
        (
            ([(42, 199), (92, 210), (148, 222), (166, 246), (168, 276),
              (143, 291), (104, 278), (62, 250), (22, 227)],
             ((145, 260), (30, 204))),
            ([(35, 98), (85, 100), (85, 160), (66, 192), (92, 214),
              (61, 246), (27, 227), (0, 211), (0, 181), (13, 142)],
             ((30, 204), (90, 100))),
            ([(44, 108), (60, 74), (80, 40), (100, 12), (140, 0),
              (166, 12), (168, 47), (158, 75), (130, 92), (96, 110),
              (75, 128)], ((90, 100), (136, 35))),
        ),
        (
            ([(385, 535), (430, 505), (495, 518), (575, 535),
              (620, 550), (620, 655), (535, 672), (440, 665), (390, 615)],
             ((470, 589), (610, 614))),
            ([(580, 548), (740, 545), (880, 501), (1005, 463),
              (1035, 540), (920, 580), (745, 653), (590, 664)],
             ((610, 614), (990, 520))),
            ([(970, 360), (1199, 360), (1199, 650), (970, 650)],
             ((990, 520), (1085, 503))),
        ),
    ),
    "alethea": (
        (
            ([(13, 495), (75, 466), (124, 440), (190, 408),
              (223, 440), (245, 480), (236, 502), (159, 543),
              (75, 579), (15, 583)], ((223, 455), (32, 540))),
            ([(55, 334), (112, 334), (106, 410), (74, 479),
              (69, 543), (55, 583), (14, 583), (0, 543), (0, 489),
              (27, 421)], ((32, 540), (85, 345))),
            ([(55, 244), (76, 213), (116, 188), (155, 180),
              (187, 200), (204, 229), (203, 270), (179, 305),
              (128, 337), (104, 358), (50, 349)],
             ((85, 345), (145, 238))),
        ),
        (
            ([(16, 153), (49, 144), (73, 158), (93, 171),
              (92, 199), (72, 210), (48, 196), (18, 175)],
             ((87, 188), (24, 160))),
            ([(23, 74), (66, 89), (58, 128), (45, 148),
              (58, 165), (36, 187), (8, 173), (0, 150), (5, 112)],
             ((24, 160), (55, 83))),
            ([(30, 0), (100, 0), (105, 48), (77, 70), (55, 94),
              (30, 86), (25, 60)], ((55, 83), (68, 32))),
        ),
        (
            ([(132, 326), (168, 307), (234, 316), (306, 340),
              (321, 415), (237, 426), (156, 424), (135, 398)],
             ((174, 370), (302, 373))),
            ([(280, 341), (394, 331), (508, 292), (537, 354),
              (430, 401), (306, 421)], ((302, 373), (500, 340))),
            ([(487, 190), (682, 190), (682, 420), (487, 420)],
             ((500, 340), (591, 296))),
        ),
    ),
}
REST_ARM_MASKS = {
    "kleon": [(0, 335), (68, 335), (83, 386), (67, 475), (0, 475)],
    "alethea": [(23, 270), (69, 282), (66, 308), (47, 324),
                (40, 360), (35, 392), (0, 392), (0, 357), (10, 318)],
}


def is_owned(path):
    path = Path(path).resolve()
    return path.is_relative_to(ROOT) and path.relative_to(ROOT) in OWNED


def source(name, kind):
    return Image.open(BASE / f"{name}-{kind}.png").convert("RGBA")


def opaque(image):
    image = image.copy()
    image.putalpha(image.getchannel("A").point(lambda x: 255 if x >= 128 else 0))
    return image


def trim(image):
    image = opaque(image)
    alpha = np.array(image.getchannel("A"))
    occupied = np.flatnonzero(np.any(alpha, axis=1))
    bands = np.split(occupied, np.flatnonzero(np.diff(occupied) > max(8, image.height // 25)) + 1)
    if len(bands) > 1:
        # Model sheets sometimes place the preceding cell's toes below a divider.
        band = max(bands, key=lambda b: np.count_nonzero(alpha[b[0]:b[-1] + 1]))
        keep = np.zeros_like(alpha)
        keep[band[0]:band[-1] + 1] = alpha[band[0]:band[-1] + 1]
        removed = np.count_nonzero(alpha) - np.count_nonzero(keep)
        if removed > np.count_nonzero(alpha) * .1:
            raise ValueError("Ambiguous cell boundary: substantial art outside the main figure band")
        print(f"Trimmed {removed} opaque neighboring-cell fragment pixels before native reduction")
        image.putalpha(Image.fromarray(keep))
    box = image.getchannel("A").getbbox()
    if box is None:
        raise ValueError("Empty image-model source cell")
    return image.crop(box)


def cells(image, columns, rows):
    return [trim(image.crop((round(x * image.width / columns),
                             round(y * image.height / rows),
                             round((x + 1) * image.width / columns),
                             round((y + 1) * image.height / rows))))
            for y in range(rows) for x in range(columns)]


def fit(image, size=(64, 64), margin=2, phase=(0, 0)):
    image = trim(image)
    scale = min((size[0] - 2 * margin) / image.width,
                (size[1] - 2 * margin) / image.height)
    target = (max(1, round(image.width * scale)),
              max(1, round(image.height * scale)))
    if phase != (0, 0):
        # A sampling phase preserves small source eyes without repainting them.
        pad = round(2 / scale)
        padded = Image.new("RGBA", (image.width + pad * 2, image.height + pad * 2))
        padded.alpha_composite(image, (pad, pad))
        dx, dy = (p / scale for p in phase)
        image = padded.resize(target, Image.Resampling.NEAREST,
                              box=(pad + dx, pad + dy,
                                   pad + image.width + dx, pad + image.height + dy))
    else:
        image = image.resize(target, Image.Resampling.NEAREST)
    canvas = Image.new("RGBA", size)
    canvas.alpha_composite(image, ((size[0] - image.width) // 2,
                                   size[1] - margin - image.height))
    return canvas


def palette(images):
    arrays = [np.array(im) for im in images]
    pixels = np.concatenate([a[a[:, :, 3] != 0, :3] for a in arrays])
    weighted = [pixels]
    p = pixels.astype("int32")
    # Separate tiny saturated accents from broad ochre/hair, plus orb lights.
    for channel in range(3):
        others = [i for i in range(3) if i != channel]
        selected = pixels[(p[:, channel] >= 128)
                          & (p[:, channel] > p[:, others[0]] * 2)
                          & (p[:, channel] > p[:, others[1]] * 2)
                          & (np.abs(p[:, others[0]] - p[:, others[1]]) < p[:, channel] * .2)]
        if 0 < len(selected) <= len(pixels) * .03:
            weighted.extend([selected] * 12)
    lights = pixels[(pixels.min(axis=1) >= 168)
                    & (np.ptp(pixels, axis=1) < 48)]
    if 0 < len(lights) <= len(pixels) * .03:
        weighted.extend([lights] * 12)
    strip = Image.fromarray(np.concatenate(weighted).reshape(1, -1, 3))
    quantized = strip.quantize(colors=15, method=Image.Quantize.MEDIANCUT, kmeans=5)
    colors = np.array(quantized.getpalette()[:45]).reshape(-1, 3)
    colors = np.unique(np.clip(np.round(colors / 8) * 8, 0, 248).astype("uint8"), axis=0)
    return [(112, 192, 160)] + [tuple(map(int, c)) for c in colors]


def indexed(image, colors):
    a = np.array(image)
    rgb = np.array(colors[1:], dtype="int32")
    delta = a[:, :, None, :3].astype("int32") - rgb[None, None, :, :]
    indices = np.argmin(np.sum(delta * delta, axis=3), axis=2) + 1
    indices[a[:, :, 3] == 0] = 0
    result = Image.fromarray(indices.astype("uint8"))
    flat = [c for color in colors for c in color]
    result.putpalette(flat + [0] * (768 - len(flat)))
    result.info["transparency"] = 0
    return result


def shared_palette(name):
    family = "folk" if name in FOLK else "theoxenia" if name in THEOXENIA else "cast"
    path = ROOT / f"graphics/object_events/palettes/ichor_{family}.pal"
    lines = path.read_text().splitlines()
    if lines[:3] != ["JASC-PAL", "0100", "16"]:
        raise ValueError(f"Unexpected shared palette format: {path}")
    return [tuple(map(int, line.split())) for line in lines[3:19]]


def opposite_contact(image, box):
    image = image.copy()
    image.paste(ImageOps.mirror(image.crop(box)), box[:2])
    return image


def walker(name):
    special = name in {"kleon_seasick", "kleon_tablet"}
    frames = cells(source(name, "walk"), 3, 3 if special or name == "kleon" else 2)
    scale = min(16 / max(f.width for f in frames),
                30 / max(f.height for f in frames))
    fitted = []
    for i, frame in enumerate(frames):
        frame = frame.resize((max(1, round(frame.width * scale)),
                              max(1, round(frame.height * scale))),
                             Image.Resampling.NEAREST)
        canvas = Image.new("RGBA", (16, 32))
        floor = 30 if i < 3 or special else 31
        canvas.alpha_composite(frame, ((16 - frame.width) // 2, floor + 1 - frame.height))
        fitted.append(canvas)
    if special:
        fitted = [fitted[i] for i in (0, 1, 2, 3, 6, 4, 7, 5, 8)]
    else:
        if name == "kleon":
            down, up, left = fitted[3], fitted[5], fitted[7]
        else:
            down, up, left = fitted[3:]
        if name == "cami":
            # The model's rear stride put the sole wheat ear on the wrong side.
            up = ImageOps.mirror(up)
        y = 27 if name in ROBES else 24
        # Front/rear lower-leg assembly leaves asymmetric upper costumes intact.
        down_box, up_box = LEG_BOXES.get(name, ((3, y, 13, 32), (3, y, 13, 32)))
        down_b, up_b = opposite_contact(down, down_box), opposite_contact(up, up_box)
        # Do not mirror profile boots: their toes must continue pointing left.
        profile = fit(source(name, "profile-b"), (16, 32), margin=0)
        left_b = left.copy()
        left_b.paste(profile.crop((0, y, 16, 32)), (0, y))
        fitted = fitted[:3] + [down, down_b, up, up_b, left, left_b]
    if name in {"sam", "apollo"}:
        fitted.extend(fit(f, (16, 32), margin=1) for f in cells(source(name, "strum"), 3, 1))
    if name == "cami":
        seated = cells(source(name, "seated"), 2, 1)
        for frame, height in zip(seated, (25, 28)):
            part = fit(frame, (16, height), margin=0)
            canvas = Image.new("RGBA", (16, 32))
            canvas.alpha_composite(part, (0, 31 - height))
            fitted.append(canvas)
    colors = shared_palette(name)
    sheet = Image.new("P", (16 * len(fitted), 32))
    sheet.putpalette(indexed(fitted[0], colors).getpalette())
    sheet.info["transparency"] = 0
    for i, frame in enumerate(fitted):
        sheet.paste(indexed(frame, colors), (16 * i, 0))
    return sheet


def back_sources(name):
    original = source(name, "back")
    frames = cells(original, 2, 2)
    if name == "kleon":
        frames[2] = trim(source("kleon", "release"))
        # A fingertip from the neighboring release cell crosses the divider.
        frames[3] = trim(original.crop((original.width // 2 + 70,
                                       original.height // 2,
                                       original.width, original.height)))
    else:
        frames[0], frames[2] = cells(source("alethea", "hold-release"), 2, 1)
    return frames


def selection(image, vertices):
    mask = Image.new("L", image.size)
    ImageDraw.Draw(mask).polygon(vertices, fill=255)
    return mask


def place_piece(image, vertices, joints, targets, width_scale=None):
    image = image.copy()
    image.putalpha(ImageChops.multiply(image.getchannel("A"), selection(image, vertices)))
    start, end = (np.array(p, dtype=float) for p in joints)
    target_start, target_end = (np.array(p, dtype=float) for p in targets)
    sx, sy = end - start
    tx, ty = target_end - target_start
    denominator = sx * sx + sy * sy
    a, b = (tx * sx + ty * sy) / denominator, (ty * sx - tx * sy) / denominator
    matrix = np.array(((a, -b), (b, a)))
    if width_scale is not None:
        source_axis = (end - start) / np.linalg.norm(end - start)
        target_axis = (target_end - target_start) / np.linalg.norm(target_end - target_start)
        source_perp = np.array((-source_axis[1], source_axis[0]))
        target_perp = np.array((-target_axis[1], target_axis[0]))
        matrix = (np.outer(target_end - target_start, source_axis)
                  / np.linalg.norm(end - start)
                  + width_scale * np.outer(target_perp, source_perp))
    inverse = np.linalg.inv(matrix)
    offset = inverse @ (matrix @ start - target_start)
    data = (*inverse[0], offset[0], *inverse[1], offset[1])
    return image.transform((64, 64), Image.Transform.AFFINE, data,
                           resample=Image.Resampling.NEAREST)


def backs(name):
    frames = back_sources(name)
    rest = frames[3]
    scale = 56 / rest.height
    position = (9, 8) if name == "kleon" else (16, 8)
    size = (round(rest.width * scale), 56)
    base = rest.copy()
    base.putalpha(ImageChops.subtract(base.getchannel("A"), selection(base, REST_ARM_MASKS[name])))
    body = Image.new("RGBA", (64, 64))
    body.alpha_composite(base.resize(size, Image.Resampling.NEAREST), position)
    root = (17, 47) if name == "kleon" else (24, 49)
    targets = (
        (root, (7, 56), (8, 46), (8, 38)),
        (root, (7, 36), (9, 26), (9, 18)),
        ((23, 47) if name == "kleon" else root, (38, 43), (50, 38), (56, 38)),
    )
    result = []
    widths = (26 / 214, 26 / 214, 26 / 485) if name == "kleon" else (30 / 400, 30 / 210, 30 / 420)
    for frame, pieces, points, width in zip(frames, ARM_PIECES[name], targets, widths):
        canvas = body.copy()
        for i, (vertices, joints) in enumerate(pieces):
            canvas.alpha_composite(place_piece(frame, vertices, joints, points[i:i + 2],
                                                width_scale=width if i < 2 else None))
        result.append(canvas)
    canvas = Image.new("RGBA", (64, 64))
    canvas.alpha_composite(rest.resize(size, Image.Resampling.NEAREST), position)
    result.append(canvas)
    return result


@lru_cache(maxsize=1)
def build():
    outputs = {PEOPLE / f"{name}.png": walker(name) for name in WALKERS}
    for name in PORTRAITS:
        front = fit(source(name, "front"), phase=FRONT_PHASES.get(name, (0, 0)))
        sequence = [front] + (backs(name) if name in {"kleon", "alethea"} else [])
        colors = palette(sequence)
        outputs[FRONT / f"{name}.png"] = indexed(front, colors)
        if len(sequence) > 1:
            sheet = Image.new("P", (64, 256))
            sheet.putpalette(indexed(front, colors).getpalette())
            sheet.info["transparency"] = 0
            for i, frame in enumerate(sequence[1:]):
                sheet.paste(indexed(frame, colors), (0, i * 64))
            outputs[BACK / f"{name}.png"] = sheet
    outputs[INTRO] = outputs[FRONT / "professor_daphne.png"].copy()
    if set(outputs) != OWNED:
        raise ValueError("Named-cast output scope changed")
    return outputs


def review(outputs, directory):
    directory.mkdir(parents=True, exist_ok=True)
    for path, image in outputs.items():
        fw, fh = (16, 32) if path.parent == PEOPLE else (64, 64)
        count = image.width // fw * (image.height // fh)
        board = Image.new("RGB", (max(660, count * (fw * 4 + 8)), fh * 5 + 48),
                          (232, 228, 216))
        draw = ImageDraw.Draw(board)
        draw.text((8, 8), f"{path}: IMAGE-MODEL-LED NATIVE CANDIDATE, pending artistic review", fill="black")
        for i in range(count):
            x, y = (i * fw, 0) if fh == image.height else (0, i * fh)
            frame = image.crop((x, y, x + fw, y + fh)).convert("RGBA")
            draw.text((i * (fw * 4 + 8) + 4, 28), str(i), fill="black")
            board.paste(frame, (i * (fw * 4 + 8), 44), frame)
            large = frame.resize((fw * 4, fh * 4), Image.Resampling.NEAREST)
            board.paste(large, (i * (fw * 4 + 8), 48 + fh), large)
        kind = "walk" if path.parent == PEOPLE else "back" if path.parent == BACK else "front"
        board.save(directory / f"{path.stem}-{kind}.png")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--review", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if not (args.out or args.review or args.write):
        parser.error("Choose --out, --review, or --write")
    outputs = build()
    for directory in ([ROOT] if args.write else []) + ([args.out] if args.out else []):
        for path, image in outputs.items():
            destination = directory / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            image.save(destination, bits=4, transparency=0)
    if args.review:
        review(outputs, args.review)
    print(f"Exported {len(outputs)} named-cast surfaces; artistic approval remains separate")


if __name__ == "__main__":
    main()
