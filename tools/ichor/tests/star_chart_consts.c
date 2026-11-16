#include "engine_consts.h"
#include "ichor_star_chart.h"
#include "item_menu.h"
#include "window.h"
#include "sprite.h"
#include "constants/ichor.h"
#include "constants/items.h"

K(ITEM_CHART, ITEM_STAR_CHART)
K(FLAG_STARS, FLAG_ICHOR_CONSTELLATIONS_START)
K(FLAG_CONCH, FLAG_ICHOR_GOT_POSEIDONS_CONCH)
K(FLAG_BADGE4, FLAG_BADGE04_GET)
K(FLAG_BADGE5, FLAG_BADGE05_GET)
K(FLAG_BADGE7, FLAG_BADGE07_GET)
K(FLAG_BADGE8, FLAG_BADGE08_GET)
K(FLAG_PAGES, FLAG_ICHOR_PAGES_START)
K(STAR_COUNT, ICHOR_STAR_COUNT)
K(KEY_POCKET, POCKET_KEY_ITEMS)
K(OFF_BAG_POCKET, offsetof(struct BagPosition, pocket))
K(OFF_BAG_CURSOR, offsetof(struct BagPosition, cursorPosition))
K(OFF_BAG_SCROLL, offsetof(struct BagPosition, scrollPosition))
K(OFF_CHART_SELECTED, 3 * 1024 * sizeof(u16))
K(WINDOW_SIZE, sizeof(struct Window))
K(OFF_WINDOW_WIDTH, offsetof(struct Window, window.width))
K(OFF_WINDOW_HEIGHT, offsetof(struct Window, window.height))
K(OFF_WINDOW_TILES, offsetof(struct Window, tileData))
K(OFF_BAG_SPRITES, offsetof(struct BagMenu, spriteIds))
K(ICON_SLOT, ITEMMENUSPRITE_ITEM)
K(ICON_ALT_SLOT, ITEMMENUSPRITE_ITEM_ALT)
K(SPRITE_NONE, SPRITE_NONE)
K(SPRITE_SIZE, sizeof(struct Sprite))
K(OFF_SPRITE_OAM, offsetof(struct Sprite, oam))
K(OBJ_VRAM_ADDR, OBJ_VRAM0)
