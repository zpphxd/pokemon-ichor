"""Export the image-generated Route 4 portraits; never draw character geometry.

Usage: python3 tools/ichor/art/export_route4_characters.py --output DIR

The immutable model output is segmented by its existing alpha channel, sampled
without smoothing, and indexed for GBA use. Exports stay in DIR/native until
explicitly imported into graphics/trainers/front_pics/.
"""

import argparse
from collections import deque
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "design/art/characters/route4/generated.png"
SOURCE_SHA256 = "040ca3381cfb940e52d0c3f5e4a7615980cd2ebe877fbacfc3acc84f5d6d0794"
PORTRAITS = (
    ("potter", "EXEKIAS / POTTER", "hiker"),
    ("initiate_f", "MYRRHINE / INITIATE", "psychic_f"),
    ("runner", "PHEIDIPPOS / RUNNER", "running_triathlete_m"),
)


def split_figures(source):
    """Keep connected source pixels; do not infer or redraw anatomy."""
    width, height = source.size
    alpha = source.getchannel("A")
    remaining = bytearray(alpha.point(lambda value: int(value >= 128)).tobytes())
    components = []
    for start in range(len(remaining)):
        if not remaining[start]:
            continue
        remaining[start] = 0
        pending = deque([start])
        pixels = []
        while pending:
            position = pending.popleft()
            pixels.append(position)
            x, y = position % width, position // width
            neighbors = []
            if x:
                neighbors.append(position - 1)
            if x + 1 < width:
                neighbors.append(position + 1)
            if y:
                neighbors.append(position - width)
            if y + 1 < height:
                neighbors.append(position + width)
            for neighbor in neighbors:
                if remaining[neighbor]:
                    remaining[neighbor] = 0
                    pending.append(neighbor)
        components.append(pixels)

    figures = sorted(components, key=len, reverse=True)[:3]
    if len(figures) != 3 or min(map(len, figures)) < 1000:
        raise ValueError("Expected three separate full-body source figures")
    extras = sorted(components, key=len, reverse=True)[3:]
    if extras:
        raise ValueError(
            f"Review disconnected source details before export: "
            f"{[len(component) for component in extras]}"
        )
    extracted = []
    for pixels in figures:
        mask = Image.new("L", source.size)
        data = bytearray(width * height)
        for position in pixels:
            data[position] = 255
        mask.frombytes(bytes(data))
        bounds = mask.getbbox()
        figure = source.copy()
        figure.putalpha(mask)
        extracted.append((bounds, figure.crop(bounds)))
    return sorted(extracted, key=lambda figure: figure[0][0])


def encode(figure):
    figure = figure.copy()
    figure.thumbnail((60, 60), Image.Resampling.NEAREST)
    sampled = Image.new("RGBA", (64, 64))
    sampled.paste(figure, ((64 - figure.width) // 2, (64 - figure.height) // 2))
    pixels = list(sampled.getdata())
    opaque = [rgba[:3] for rgba in pixels if rgba[3]]
    red = [
        rgb for rgb in opaque
        if rgb[0] > 150 and rgb[1] < rgb[0] * 0.55 and rgb[2] < rgb[0] * 0.65
    ]
    green = [
        rgb for rgb in opaque
        if rgb[1] > 80 and rgb[0] < rgb[1] * 0.85 and rgb[2] < rgb[1] * 0.8
    ]
    weighted = opaque.copy()
    # Protect tiny identity accents without starving broad skin/clothing ramps.
    for accents in (red, green):
        if len(accents) <= len(opaque) * 0.03:
            weighted.extend(accents * 12)
    swatches = Image.new("RGB", (len(weighted), 1))
    swatches.putdata(weighted)
    quantized = swatches.quantize(colors=15, method=Image.Quantize.MEDIANCUT)
    palette = [value & 0xF8 for value in quantized.getpalette()[:45]]
    indexed = Image.new("P", (64, 64))
    indexed.putpalette(([0, 0, 0] + palette + [0] * 768)[:768])
    colors = iter(quantized.getdata())
    indexed.putdata([next(colors) + 1 if rgba[3] else 0 for rgba in pixels])
    indexed.info["transparency"] = 0
    return indexed


def transparent(image):
    image = image.copy()
    image.info["transparency"] = 0
    return image.convert("RGBA")


def export(output):
    actual_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if actual_hash != SOURCE_SHA256:
        raise ValueError(f"Generated source changed: {actual_hash}")
    source = Image.open(SOURCE).convert("RGBA")
    figures = split_figures(source)
    native = output / "native"
    native.mkdir(parents=True, exist_ok=True)
    board = Image.new("RGB", (760, 3 * 350), "#e8e3d7")
    draw = ImageDraw.Draw(board)
    records = []
    for row, ((name, title, old), (bounds, figure)) in enumerate(zip(PORTRAITS, figures)):
        image = encode(figure)
        target = native / f"{name}.png"
        image.save(target, bits=4, transparency=0)
        y = row * 350
        draw.text((16, y + 12), title, fill="#211e24")
        for x, label in ((16, "EXISTING PLACEHOLDER"), (300, "NEW 64x64 CANDIDATE")):
            draw.text((x, y + 34), label, fill="#211e24")
        original = Image.open(ROOT / f"graphics/trainers/front_pics/{old}.png")
        before = transparent(original)
        after = transparent(image)
        board.paste(before, (16, y + 58), before)
        board.paste(after, (300, y + 58), after)
        for x, picture in ((16, before), (300, after)):
            enlarged = picture.resize((192, 192), Image.Resampling.NEAREST)
            board.paste(enlarged, (x, y + 140), enlarged)
        reference = figure.copy()
        reference.thumbnail((160, 260), Image.Resampling.LANCZOS)
        board.paste(reference, (580, y + 60), reference)
        records.append({
            "name": name,
            "source_bounds": bounds,
            "native_bounds": after.getbbox(),
            "opaque_colors": len(set(image.getdata()) - {0}),
            "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        })
    board.save(output / "comparison.png")
    manifest = {
        "source_sha256": actual_hash,
        "source_size": source.size,
        "process": (
            "Existing alpha>=128 connected components, left-to-right; "
            "nearest-neighbor fit within 60x60 centered on 64x64; "
            "median-cut 15 colors; red/green accent weight 12 only when "
            "the accent occupies at most 3% of opaque pixels; "
            "RGB truncated to BGR555 precision; index 0 transparent; no dithering. "
            "No programmatic anatomy drawing."
        ),
        "portraits": records,
        "authoring": "Image-model-led, resampled/quantized; not hand-authored pixel art",
    }
    (output / "verification.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    export(parser.parse_args().output)
