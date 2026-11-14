#!/usr/bin/env python3
"""Assemble the slice's look-review gallery from a playthrough's screenshots.

  tools/ichor/tests/slice_gallery.py [--out design/phase1/img/gallery] [--all build/slice/review]

Reads build/slice/run.log and build/slice_checks/run.log (the "shot <file> map <id>
<field|scene|battle>" lines) and their shots/ folders, picks a representative
frame per beat, per map, per battle and per menu, and writes 2x contact sheets,
one per section, captioned with the beat and the moment:

  <out>/01_opening.png ... <out>/13_maps.png

Frames are picked by name (the playthrough names every moment it shoots), so
the sheets stay comparable from one art pass to the next. --all also writes
every screenshot of the run, in order, as numbered sheets for a full QA read.
"""
import argparse
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
SCALE = 2
COLS = 3
PER_SHEET = 12
CAPTION = 22
PAD = 12
HEADER = 40
BG = (24, 20, 20)
INK = (232, 216, 176)

# (sheet name, title, [(regex on "<beat>_<name>", how many to keep)])
SECTIONS = [
    ("01_opening", "Title, options, Daphne's speech", [
        (r"00_title_title$", 1), (r"00_title_main_menu_fresh$", 1), (r"00_title_options_after$", 1),
        (r"00_daphne_speech_speech_\d+$", 7), (r"00_daphne_speech_speech_gender$", 1),
        (r"00_daphne_speech_speech_naming$", 1), (r"01_bedroom_bedroom$", 1)]),
    ("02_elaia_morning", "Beat 1: festival morning", [
        (r"01_bedroom_mom_calls_upstairs$", 1), (r"01_bedroom_knucklebones$", 1), (r"01_bedroom_klepsydra_text$", 1),
        (r"01_bedroom_naming$", 1), (r"01_mom_mom_comes_over$", 1), (r"01_mom_mom_klotheia$", 1), (r"01_mom_talaria$", 1),
        (r"01_mom_mom_oracle$", 1), (r"01_mom_front_door$", 1), (r"01_kydippe_kydippe$", 1),
        (r"01_kydippe_kydippe_delivered_you$", 1), (r"02_gates_akademia_note$", 1), (r"02_gates_shepherd_gate$", 1)]),
    ("03_halia", "Beat 2: Halia reads the threads", [
        (r"02_halia_halia_calls$", 1), (r"02_halia_korinna_reading$", 1), (r"02_halia_philon_reading$", 1),
        (r"02_halia_your_hand$", 1), (r"02_halia_hm$", 1), (r"02_halia_turn_around$", 1), (r"02_halia_prompt_no$", 1), (r"02_halia_liar$", 1),
        (r"02_halia_your_own_business$", 1), (r"02_halia_after_the_reading$", 1)]),
    ("04_akademia", "Beat 3: the Akademia and the starters", [
        (r"03_akademia_akademia_alethea$", 1), (r"03_akademia_text_0[2-6]$", 3), (r"03_akademia_menu_down$", 1),
        (r"03_akademia_starter_screen$", 1), (r"03_akademia_starter_confirm$", 1), (r"03_akademia_text_(1\d|2\d)$", 5),
        (r"03_akademia_last_krater$", 1)]),
    ("05_kleon", "Beat 4: Kleon in the square, and the village after", [
        (r"04_kleon_kleon_waits$", 1), (r"04_kleon_kleon_there_you_are$", 1), (r"04_kleon_kleon_oracle$", 1),
        (r"04_kleon_prompt_no$", 1), (r"04_kleon_battle$", 1), (r"04_kleon_square_after$", 1),
        (r"04_elaia_after_well$", 1), (r"04_elaia_after_halia_after$", 1), (r"04_elaia_after_village_sign$", 1),
        (r"04_elaia_after_olive_farmer$", 1), (r"04_elaia_after_mom_after$", 1)]),
    ("06_route1", "Beat 5: Route 1", [
        (r"05_route1_north_gate_open$", 1), (r"05_route1_route1_south$", 1), (r"05_route1_carter$", 1),
        (r"05_route1_wall_youth$", 1), (r"05_route1_battle$", 1), (r"05_route1_tityros_after$", 1),
        (r"05_grove_battle$", 2), (r"05_grove_olive_farmer$", 1), (r"05_fork_herm_fork$", 1), (r"05_fork_battle$", 1),
        (r"05_flock_amaryllis_before$", 1), (r"05_flock_flock_wooloo$", 1), (r"05_flock_battle$", 1),
        (r"05_route1_wild_battle$", 1)]),
    ("07_kronion_hill", "Beat 5: Kronion Hill", [
        (r"05_kronion_hill_hill_foot$", 1), (r"05_summit_text_\d+$", 6), (r"05_summit_battle$", 2),
        (r"05_summit_prompt_no$", 1), (r"05_summit_summit_after$", 1), (r"05_summit_stele$", 1),
        (r"05_summit_pit_after$", 1), (r"05_road_open_flock_gone$", 1), (r"05_road_open_amaryllis_after$", 1)]),
    ("08_akti", "Beat 6: Akti, the Asclepeion, the Agora", [
        (r"06_akti_arrival_arrival$", 1), (r"06_akti_arrival_text_0[1-6]$", 3), (r"06_akti_arrival_after_arrival$", 1),
        (r"06_akti_arrival_pilgrim$", 1), (r"06_asclepeion_asclepeion$", 1), (r"06_asclepeion_healer_welcome$", 1),
        (r"06_asclepeion_healer_rest$", 1), (r"06_asclepeion_old_man$", 1), (r"06_asclepeion_pithos_woman$", 1),
        (r"06_save_start_menu$", 1), (r"06_save_save_prompt$", 1), (r"06_save_main_menu_continue$", 1),
        (r"06_agora_agora$", 1), (r"06_agora_agora_menu$", 1), (r"06_agora_agora_shop$", 1),
        (r"06_fishers_house_fishers_house$", 1), (r"06_fishers_house_glaukos$", 1), (r"06_fishers_house_text_0[2-4]$", 2),
        (r"06_harbor_before_kleon_before$", 1), (r"06_harbor_before_kleon_soup$", 1),
        (r"06_harbor_before_nausikles_before$", 1), (r"06_harbor_before_fishwife$", 1), (r"06_harbor_before_hydna$", 1),
        (r"06_harbor_before_temple_old_woman$", 1)]),
    ("09_temple", "Beat 7: the Temple of Hestia", [
        (r"07_temple_temple_entry$", 1), (r"07_temple_euboulos$", 1), (r"07_temple_text_0[1-8]$", 4),
        (r"07_temple_hands_off$", 1), (r"07_temple_battle$", 1), (r"07_hearth_trial_take_flame_done$", 1),
        (r"07_hearth_trial_door_brazier_done$", 1), (r"07_hearth_trial_table_brazier_done$", 1),
        (r"07_hearth_trial_loom_brazier_done$", 1), (r"07_hearth_trial_bed_brazier_done$", 1),
        (r"07_hearth_trial_return_flame$", 1), (r"07_hearth_trial_text_0[1-6]$", 4), (r"07_hearth_trial_battle$", 2),
        (r"07_ione_ione$", 1), (r"07_ione_text_\d+$", 6), (r"07_ione_battle$", 1), (r"07_ione_ione_after$", 1),
        (r"07_ione_kanthos$", 1)]),
    ("10_ending", "Beat 8: the harbor, when the winds turn", [
        (r"08_harbor_part1_doorstep$", 1), (r"08_harbor_part1_text_\d+$", 4), (r"08_harbor_part2_text_\d+$", 8),
        (r"08_harbor_part2_prompt_no$", 1), (r"08_harbor_part2_the_end$", 1), (r"08_after_nausikles_after$", 1),
        (r"08_after_akti_after_the_end$", 1)]),
    ("11_battles", "Every battle in the slice (the first action menu)", [
        (r"_battle$", 20), (r"_wild_battle$", 1)]),
    ("12_menus", "The start menu and its screens (after the slice)", [
        (r"menus_start_menu_pokedex$", 1), (r"menus_pokedex$", 1), (r"menus_pokedex_entry$", 1), (r"menus_party$", 1),
        (r"menus_party_actions$", 1), (r"menus_summary_\d$", 5), (r"menus_bag_pocket_\d$", 5), (r"menus_augury$", 1),
        (r"menus_trainer_card$", 1), (r"menus_trainer_card_back$", 1), (r"menus_option$", 1)]),
]

MAP_NAMES = {}


def map_names():
    for d in (ROOT / "data/maps").iterdir():
        f = d / "map.json"
        if f.exists():
            j = json.loads(f.read_text())
            MAP_NAMES[j.get("id")] = d.name
    groups = json.loads((ROOT / "data/maps/map_groups.json").read_text())
    ids = {}
    for g, group in enumerate(groups["group_order"]):
        for n, name in enumerate(groups[group]):
            ids[(g << 8) | n] = name
    return ids


def read_shots(log, folder):
    shots = []
    pat = re.compile(r" shot (\S+\.png)(?: map (\d+) (\w+))?")
    if not log.exists():
        return shots
    for line in log.read_text(errors="replace").splitlines():
        m = pat.search(line)
        if m and (folder / m.group(1)).exists():
            stem = m.group(1)[5:-4]   # drop "NNNN_" and ".png"
            shots.append({"file": folder / m.group(1), "stem": stem,
                          "map": int(m.group(2)) if m.group(2) else None, "kind": m.group(3)})
    return shots


def font(size):
    for path in ("/System/Library/Fonts/Menlo.ttc", "/System/Library/Fonts/Supplemental/Courier New.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def sheet(frames, title, out, scale=SCALE, cols=COLS):
    w, h = 240 * scale, 160 * scale
    rows = (len(frames) + cols - 1) // cols
    img = Image.new("RGB", (PAD + cols * (w + PAD), HEADER + rows * (h + CAPTION + PAD) + PAD), BG)
    d = ImageDraw.Draw(img)
    d.text((PAD, 10), title, fill=INK, font=font(20))
    small = font(13)
    for i, (path, caption) in enumerate(frames):
        x = PAD + (i % cols) * (w + PAD)
        y = HEADER + (i // cols) * (h + CAPTION + PAD)
        img.paste(Image.open(path).convert("RGB").resize((w, h), Image.NEAREST), (x, y))
        d.text((x, y + h + 4), caption[:64], fill=INK, font=small)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, optimize=True)
    print(f"wrote {out.relative_to(ROOT)} ({len(frames)} frames)")


def pick(shots, regex, n):
    found = [s for s in shots if re.search(regex, s["stem"])]
    if len(found) <= n:
        return found
    step = (len(found) - 1) / (n - 1) if n > 1 else 0
    return [found[round(i * step)] for i in range(n)]


def write_sections(name, title, frames, out_dir):
    per, scale, cols = (30, 1, 6) if name == "all" else (PER_SHEET, SCALE, COLS)
    # split evenly, at most `per` + 3 frames a sheet, so no sheet holds a lone frame
    sheets = max(1, -(-len(frames) // (per + 3)))
    per = -(-len(frames) // sheets)
    for k in range(0, len(frames), per):
        part = frames[k:k + per]
        suffix = "" if len(frames) <= per else f"_{k // per + 1:02d}"
        sheet(part, title + ("" if not suffix else f" ({k // per + 1})"), out_dir / f"{name}{suffix}.png",
              scale, cols)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="design/phase1/img/gallery")
    ap.add_argument("--run", default="build/slice")
    ap.add_argument("--checks", default="build/slice_checks")
    ap.add_argument("--all", help="also write every screenshot, in order, as numbered sheets here")
    a = ap.parse_args()
    out_dir = ROOT / a.out
    for old in out_dir.glob("*.png"):
        old.unlink()
    ids = map_names()
    run = read_shots(ROOT / a.run / "run.log", ROOT / a.run / "shots")
    checks = read_shots(ROOT / a.checks / "run.log", ROOT / a.checks / "shots")
    shots = run + checks
    if not run:
        raise SystemExit("no screenshots: run tools/ichor/tests/slice_playthrough.sh first")
    for name, title, wanted in SECTIONS:
        frames, used = [], set()
        for regex, n in wanted:
            for s in pick([s for s in shots if s["file"] not in used], regex, n):
                used.add(s["file"])
                frames.append((s["file"], s["stem"].replace("_", " ")))
        if frames:
            write_sections(name, title, frames, out_dir)
        else:
            print(f"skip {name}: no frames")
    # one plain field frame per map, the first the run took there
    seen, frames = set(), []
    for s in run:
        if s["kind"] == "field" and s["map"] is not None and s["map"] not in seen:
            seen.add(s["map"])
            frames.append((s["file"], f"{ids.get(s['map'], s['map'])}  ({s['stem'].replace('_', ' ')})"))
    if frames:
        write_sections("13_maps", "Every map the slice visits, as the player first sees it", frames, out_dir)
    if a.all:
        for old in (ROOT / a.all).glob("all*.png"):
            old.unlink()
        write_sections("all", "Every screenshot of the run, in order",
                       [(s["file"], s["file"].name[:-4]) for s in shots], ROOT / a.all)


if __name__ == "__main__":
    main()
