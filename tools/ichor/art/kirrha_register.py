#!/usr/bin/env python3
"""Register gTileset_Kirrha, gTileset_Aigion and gTileset_GulfFerry in
src/data/tilesets/{headers,graphics,metatiles}.h (appended entries; idempotent).

Usage: /usr/bin/python3 tools/ichor/art/kirrha_register.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SETS = [
    ("kirrha", "Kirrha", "Kirrha, Delphoi's harbor (the harbors agent): the quay, the fish market, "
     "Parnassos's crags and the Phaidriades, the pilgrims' gate, the houses"),
    ("aigion", "Aigion", "Aigion across the gulf (the harbors agent): the quay, the grove of "
     "Zeus, Helike's drowned roofs, the ochre houses"),
    ("gulf_ferry", "GulfFerry", "Panopeus's ferry, Route 10 (the harbors agent): the deck, the "
     "patched sail, the goats' pen"),
]


def main():
    hdr = ROOT / "src/data/tilesets/headers.h"
    gfx = ROOT / "src/data/tilesets/graphics.h"
    met = ROOT / "src/data/tilesets/metatiles.h"
    H, G, M = hdr.read_text(), gfx.read_text(), met.read_text()
    for d, sym, blurb in SETS:
        if f"gTileset_{sym} =" not in H:
            H = H.rstrip("\n") + f"""

// Ichor (Act II): {blurb}. A Porytiles-managed secondary for the aethos primary,
// built by tools/ichor/art/kirrha_build.py. It uses only its own tiles and palettes 6-12.
const struct Tileset gTileset_{sym} =
{{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_{sym},
    .palettes = gTilesetPalettes_PorytilesManaged_{sym},
    .metatiles = gMetatiles_PorytilesManaged_{sym},
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_{sym},
    .callback = NULL,
}};
"""
        if f"gTilesetTiles_PorytilesManaged_{sym}[]" not in G:
            pals = ",\n".join(f'    INCBIN_U16("data/tilesets/secondary/{d}/porytiles_bin/palettes/{i:02d}.gbapal")'
                              for i in range(16))
            G = G.rstrip("\n") + f"""

// Ichor: {d}
const u32 gTilesetTiles_PorytilesManaged_{sym}[] = INCBIN_U32("data/tilesets/secondary/{d}/porytiles_bin/tiles.4bpp.lz");

const u16 gTilesetPalettes_PorytilesManaged_{sym}[][16] =
{{
{pals}
}};
"""
        if f"gMetatiles_PorytilesManaged_{sym}[]" not in M:
            M = M.rstrip("\n") + f"""

// Ichor: {d}
const u16 gMetatiles_PorytilesManaged_{sym}[] = INCBIN_U16("data/tilesets/secondary/{d}/porytiles_bin/metatiles.bin");
const u16 gMetatileAttributes_PorytilesManaged_{sym}[] = INCBIN_U16("data/tilesets/secondary/{d}/porytiles_bin/metatile_attributes.bin");
"""
    hdr.write_text(H)
    gfx.write_text(G)
    met.write_text(M)
    print("registered", ", ".join(s for _, s, _ in SETS))


if __name__ == "__main__":
    main()
