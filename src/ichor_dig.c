// Ichor: excavation (design/SYSTEMS.md §5, design/ENGINE_API.md §8).
//
// A daily dig spot rolls its find from its act's loot table, seeded by the
// day's seed and the spot, so reloading a save digs up the same thing. It can
// be dug once a day (FLAG_DAILY_ICHOR_DIG_START + spot). A fixed find gives
// what the map names, once (FLAG_ICHOR_DIG_FIXED_START + index). Sherds,
// ostraka, prophecy tablets and Daedalus's pages are flags, not items.
// data/scripts/ichor_dig.pory runs a dig; these specials keep the books.

#include "global.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_effect.h"
#include "field_player_avatar.h"
#include "item.h"
#include "money.h"
#include "random.h"
#include "sound.h"
#include "string_util.h"
#include "ichor_dig.h"
#include "ichor_relics.h"
#include "constants/field_effects.h"
#include "constants/flags.h"
#include "constants/ichor.h"
#include "constants/items.h"
#include "constants/songs.h"

#define DIG_SALT          0x0D16D16
#define DAILY_SPOT_COUNT  96   // FLAG_DAILY_ICHOR_DIG_START's range
#define FIXED_FIND_COUNT  64   // FLAG_ICHOR_DIG_FIXED_START's range
#define PROPHECY_COUNT    8
#define PAGE_COUNT        7
#define ROLL_TRIES        16
#define NONE_LEFT         0xFF

enum
{
    FIND_SHERD,
    FIND_OBOL,
    FIND_OWL,
    FIND_STATER,
    FIND_OSTRAKON,
    FIND_SHARD,
    FIND_STARDUST,
    FIND_HARD_STONE,
    FIND_HEART_SCALE,
    FIND_FOSSIL,
    FIND_PEARL,
    FIND_EVO_STONE,
    FIND_RARE_BONE,
    FIND_PP_UP,
    FIND_COMET_SHARD,
    FIND_BOTTLE_CAP,
    FIND_ICHOR_STONE,
};

struct DigLoot
{
    u8 find;
    u8 weight; // percent; each table sums to 100
};

// SYSTEMS §5's loot tables
static const struct DigLoot sLootActI[] =
{
    {FIND_SHERD, 22}, {FIND_OBOL, 18}, {FIND_OSTRAKON, 10}, {FIND_SHARD, 10},
    {FIND_STARDUST, 12}, {FIND_HARD_STONE, 10}, {FIND_HEART_SCALE, 8},
    {FIND_FOSSIL, 6}, {FIND_PEARL, 4},
};

static const struct DigLoot sLootActII[] =
{
    {FIND_SHERD, 20}, {FIND_OBOL, 12}, {FIND_OWL, 8}, {FIND_OSTRAKON, 10},
    {FIND_SHARD, 8}, {FIND_STARDUST, 6}, {FIND_HARD_STONE, 6},
    {FIND_HEART_SCALE, 8}, {FIND_FOSSIL, 8}, {FIND_EVO_STONE, 8},
    {FIND_RARE_BONE, 6},
};

static const struct DigLoot sLootActIII[] =
{
    {FIND_SHERD, 16}, {FIND_OWL, 10}, {FIND_STATER, 4}, {FIND_OSTRAKON, 8},
    {FIND_SHARD, 10}, {FIND_STARDUST, 8}, {FIND_HEART_SCALE, 6},
    {FIND_FOSSIL, 10}, {FIND_EVO_STONE, 10}, {FIND_RARE_BONE, 6},
    {FIND_PP_UP, 6}, {FIND_COMET_SHARD, 3}, {FIND_BOTTLE_CAP, 2},
    {FIND_ICHOR_STONE, 1},
};

static const struct DigLoot *const sLootTables[] =
{
    [ICHOR_DIG_ACT_I] = sLootActI,
    [ICHOR_DIG_ACT_II] = sLootActII,
    [ICHOR_DIG_ACT_III] = sLootActIII,
};

static const u8 sLootCounts[] =
{
    [ICHOR_DIG_ACT_I] = ARRAY_COUNT(sLootActI),
    [ICHOR_DIG_ACT_II] = ARRAY_COUNT(sLootActII),
    [ICHOR_DIG_ACT_III] = ARRAY_COUNT(sLootActIII),
};

static const u16 sShards[] = {ITEM_RED_SHARD, ITEM_BLUE_SHARD, ITEM_YELLOW_SHARD, ITEM_GREEN_SHARD};

// The Aethos fossils wait for the dex; Kanto's and Hoenn's stand in.
static const u16 sFossils[] = {ITEM_HELIX_FOSSIL, ITEM_DOME_FOSSIL, ITEM_OLD_AMBER, ITEM_ROOT_FOSSIL, ITEM_CLAW_FOSSIL};

static const u16 sEvoStones[] =
{
    ITEM_FIRE_STONE, ITEM_WATER_STONE, ITEM_THUNDER_STONE, ITEM_LEAF_STONE, ITEM_MOON_STONE,
    ITEM_SUN_STONE, ITEM_SHINY_STONE, ITEM_DUSK_STONE, ITEM_DAWN_STONE, ITEM_ICE_STONE,
};

// Ichor Stones are Mega Stones (PITCH §2). The dig's 1% gives one of these;
// Balance may retune the list.
static const u16 sIchorStones[] =
{
    ITEM_HOUNDOOMINITE, ITEM_AERODACTYLITE, ITEM_TYRANITARITE, ITEM_GARDEVOIRITE, ITEM_LUCARIONITE,
    ITEM_AGGRONITE, ITEM_STEELIXITE, ITEM_PINSIRITE, ITEM_HERACRONITE, ITEM_SCIZORITE,
};

// What each amphora's painting shows, as a sherd's message names it
static const u8 *const sAmphoraMyths[ICHOR_AMPHORA_COUNT] =
{
    [ICHOR_AMPHORA_KRONOS]     = COMPOUND_STRING("Kronos and the stone"),
    [ICHOR_AMPHORA_PERSEPHONE] = COMPOUND_STRING("Persephone's seeds"),
    [ICHOR_AMPHORA_ARACHNE]    = COMPOUND_STRING("Arachne at the loom"),
    [ICHOR_AMPHORA_HERMES]     = COMPOUND_STRING("Hermes and the cattle"),
    [ICHOR_AMPHORA_HEPHAESTUS] = COMPOUND_STRING("Hephaestus going home"),
    [ICHOR_AMPHORA_ICARUS]     = COMPOUND_STRING("Icarus falling"),
    [ICHOR_AMPHORA_PANDORA]    = COMPOUND_STRING("Pandora's jar"),
    [ICHOR_AMPHORA_ORPHEUS]    = COMPOUND_STRING("Orpheus singing"),
    [ICHOR_AMPHORA_ATALANTA]   = COMPOUND_STRING("Atalanta's race"),
    [ICHOR_AMPHORA_PHAETHON]   = COMPOUND_STRING("Phaethon's chariot"),
    [ICHOR_AMPHORA_PARIS]      = COMPOUND_STRING("Paris and the apple"),
    [ICHOR_AMPHORA_THESEUS]    = COMPOUND_STRING("Theseus and the bull"),
};

// The 30 ostraka, dug up in this order (SYSTEMS §5). Nine name Aristeides,
// for Lysimachos's line; the last is the player's.
static const u8 *const sOstraka[ICHOR_OSTRAKA_COUNT] =
{
    COMPOUND_STRING("ARISTEIDES.\nSick of hearing him called the Just."),
    COMPOUND_STRING("THEMISTOKLES.\nTalks about boats at dinner."),
    COMPOUND_STRING("HYPERION.\nBurned my fence."),
    COMPOUND_STRING("THE GOAT.\nYou know which goat."),
    COMPOUND_STRING("ARISTEIDES.\nToo fair by half."),
    COMPOUND_STRING("KLEISTHENES.\nInvented this. Serves him right."),
    COMPOUND_STRING("ARISTEIDES.\nSettled my quarrel. I lost."),
    COMPOUND_STRING("MY NEIGHBOR.\nThe one with the flute."),
    COMPOUND_STRING("ARISTEIDES.\nNever once wrong. Suspicious."),
    COMPOUND_STRING("ARCHIPPOS.\nRicher than me."),
    COMPOUND_STRING("ARISTEIDES.\nMy wife likes him."),
    COMPOUND_STRING("THE FERRYMAN.\nRaised the fare again."),
    COMPOUND_STRING("ARISTEIDES.\nSame as last year."),
    COMPOUND_STRING("STRATON.\nSold me a lame mule."),
    COMPOUND_STRING("MEGAKLES.\nHis dog howls all night."),
    COMPOUND_STRING("ARISTEIDES.\nHe wrote this for me. Nice man."),
    COMPOUND_STRING("XANTHIPPOS.\nTook my seat at the theater."),
    COMPOUND_STRING("THE ARCHON'S COOK.\nToo much salt."),
    COMPOUND_STRING("ARISTEIDES.\nJust because."),
    COMPOUND_STRING("HIPPARCHOS.\nLaughs like a donkey."),
    COMPOUND_STRING("MY BROTHER-IN-LAW.\nAgain."),
    COMPOUND_STRING("LEAGROS.\nSwims in the drinking cistern."),
    COMPOUND_STRING("ARISTEIDES.\nEveryone else is doing it."),
    COMPOUND_STRING("THE OLIVE INSPECTOR.\nHe knows what he did."),
    COMPOUND_STRING("LYSIMACHOS.\nFor raising him that way."),
    COMPOUND_STRING("NIKIAS.\nTakes an hour to say yes."),
    COMPOUND_STRING("THE TAX MAN.\nOn principle."),
    COMPOUND_STRING("PERIKLES.\nThat helmet. Every day."),
    COMPOUND_STRING("THE MOON.\nKeeps me up."),
    COMPOUND_STRING("{PLAYER}.\nNever met them. Just a feeling."),
};

static const u8 *const sRomanNumerals[] =
{
    COMPOUND_STRING("I"), COMPOUND_STRING("II"), COMPOUND_STRING("III"), COMPOUND_STRING("IV"),
    COMPOUND_STRING("V"), COMPOUND_STRING("VI"), COMPOUND_STRING("VII"),
};

// The dig under way, between Ichor_DigStart and Ichor_DigFinish
static EWRAM_DATA struct
{
    u16 flag;      // the spot's or the fixed find's flag, set once the find is taken
    u16 find;      // an item, or an ICHOR_FIND_* code
    u16 findFlag;  // the sherd, ostrakon, tablet or page flag the find sets, or 0
    u8 quantity;
} sDig = {0};

static u32 NextSherd(u32 amphora)
{
    u32 i;

    if (amphora >= ICHOR_AMPHORA_COUNT)
        return NONE_LEFT;
    for (i = 0; i < ICHOR_SHERDS_PER_AMPHORA; i++)
    {
        if (!FlagGet(FLAG_ICHOR_SHERDS_START + amphora * ICHOR_SHERDS_PER_AMPHORA + i))
            return i;
    }
    return NONE_LEFT;
}

static u32 NextOstrakon(void)
{
    u32 i;

    for (i = 0; i < ICHOR_OSTRAKA_COUNT; i++)
    {
        if (!FlagGet(FLAG_ICHOR_OSTRAKA_START + i))
            return i;
    }
    return NONE_LEFT;
}

static u32 RollLoot(rng_value_t *rng, u32 table)
{
    const struct DigLoot *loot = sLootTables[table];
    u32 i, roll = LocalRandom(rng) % 100;

    for (i = 0; i < sLootCounts[table]; i++)
    {
        if (roll < loot[i].weight)
            return loot[i].find;
        roll -= loot[i].weight;
    }
    return loot[0].find;
}

static u32 LootWeight(u32 table, u32 find)
{
    u32 i;

    for (i = 0; i < sLootCounts[table]; i++)
    {
        if (sLootTables[table][i].find == find)
            return sLootTables[table][i].weight;
    }
    return 100;
}

#define PICK(list) (list[LocalRandom(rng) % ARRAY_COUNT(list)])

static u16 LootToFind(u32 find, u32 amphora, rng_value_t *rng)
{
    switch (find)
    {
    case FIND_SHERD:       return ICHOR_FIND_SHERD(amphora);
    case FIND_OSTRAKON:    return ICHOR_FIND_OSTRAKON;
    case FIND_OBOL:        return ITEM_RELIC_COPPER;
    case FIND_OWL:         return ITEM_RELIC_SILVER;
    case FIND_STATER:      return ITEM_RELIC_GOLD;
    case FIND_SHARD:       return PICK(sShards);
    case FIND_STARDUST:    return (LocalRandom(rng) % 4) == 0 ? ITEM_STAR_PIECE : ITEM_STARDUST;
    case FIND_HARD_STONE:  return ITEM_HARD_STONE;
    case FIND_HEART_SCALE: return ITEM_HEART_SCALE;
    case FIND_FOSSIL:      return PICK(sFossils);
    case FIND_PEARL:       return ITEM_PEARL;
    case FIND_EVO_STONE:   return PICK(sEvoStones);
    case FIND_RARE_BONE:   return ITEM_RARE_BONE;
    case FIND_PP_UP:       return ITEM_PP_UP;
    case FIND_COMET_SHARD: return ITEM_COMET_SHARD;
    case FIND_BOTTLE_CAP:  return ITEM_BOTTLE_CAP;
    case FIND_ICHOR_STONE: return PICK(sIchorStones);
    }
    return ITEM_STARDUST;
}

#undef PICK

// A daily spot's find: VAR_0x8005's table, rerolling sherds the spot can't give
// (no amphora, or its amphora is whole) and ostraka once all 30 are found.
// Demeter's blessing rolls twice and keeps the rarer; Hades's doubles an item.
static void RollDailyFind(u32 spot, u32 tableArg)
{
    u32 table = tableArg & 0xF, amphora = ((tableArg >> 4) & 0xF) - 1; // -1 wraps: no amphora
    u32 tries, find = FIND_STARDUST;
    rng_value_t rng;

    if (table < ICHOR_DIG_ACT_I || table > ICHOR_DIG_ACT_III)
        table = ICHOR_DIG_ACT_I;
    rng = LocalRandomSeed(gSaveBlock1Ptr->dailySeed ^ ((spot + 1) * 0x9E3779B1) ^ DIG_SALT);
    for (tries = 0; tries < ROLL_TRIES; tries++)
    {
        find = RollLoot(&rng, table);
        if (Ichor_IsBlessed(ICHOR_GOD_DEMETER))
        {
            u32 other = RollLoot(&rng, table);
            if (LootWeight(table, other) < LootWeight(table, find))
                find = other;
        }
        if (find == FIND_SHERD && NextSherd(amphora) == NONE_LEFT)
            continue;
        if (find == FIND_OSTRAKON && NextOstrakon() == NONE_LEFT)
            continue;
        break;
    }
    if (tries == ROLL_TRIES)
        find = FIND_STARDUST;
    sDig.find = LootToFind(find, amphora, &rng);
    sDig.quantity = (sDig.find < ITEMS_COUNT && Ichor_IsBlessed(ICHOR_GOD_HADES)) ? 2 : 1;
}

// A fixed find that can't be given (its amphora is whole, or a bad code) gives
// Stardust instead, so the spot still pays.
static u16 CheckFixedFind(u16 find)
{
    if (find >= 0xF000)
    {
        u32 n = find & 0xFF;
        switch (find & 0xFF00)
        {
        case ICHOR_FIND_SHERD(0):
            if (NextSherd(n) != NONE_LEFT)
                return find;
            break;
        case ICHOR_FIND_PROPHECY(0):
            if (n >= 1 && n <= PROPHECY_COUNT)
                return find;
            break;
        case ICHOR_FIND_PAGE(0):
            if (n >= 1 && n <= PAGE_COUNT)
                return find;
            break;
        case ICHOR_FIND_OSTRAKON:
            if (NextOstrakon() != NONE_LEFT)
                return find;
            break;
        }
        return ITEM_STARDUST;
    }
    if (find == ITEM_NONE || find >= ITEMS_COUNT)
        return ITEM_STARDUST;
    return find;
}

// specialvar Ichor_DigStart: VAR_0x8004 the spot or find index, VAR_0x8005 the
// table or the find, VAR_0x8006 ICHOR_DIG_MODE_*. Answers ICHOR_DIG_*.
u16 Ichor_DigStart(void)
{
    u32 index = gSpecialVar_0x8004;

    sDig.findFlag = 0;
    sDig.quantity = 1;
    if (!CheckBagHasItem(ITEM_ALETHEAS_TROWEL, 1))
        return ICHOR_DIG_NO_TROWEL;
    if (gSpecialVar_0x8006 == ICHOR_DIG_MODE_FIXED)
    {
        if (index >= FIXED_FIND_COUNT)
            return ICHOR_DIG_BARE;
        sDig.flag = FLAG_ICHOR_DIG_FIXED_START + index;
        if (FlagGet(sDig.flag))
            return ICHOR_DIG_BARE;
        sDig.find = CheckFixedFind(gSpecialVar_0x8005);
    }
    else
    {
        if (index >= DAILY_SPOT_COUNT)
            return ICHOR_DIG_DUG_TODAY;
        sDig.flag = FLAG_DAILY_ICHOR_DIG_START + index;
        if (FlagGet(sDig.flag))
            return ICHOR_DIG_DUG_TODAY;
        RollDailyFind(index, gSpecialVar_0x8005);
    }
    return ICHOR_DIG_READY;
}

// special Ichor_DigPuff: dust on the tile the player digs, and the scrape.
void Ichor_DigPuff(void)
{
    struct ObjectEvent *player = &gObjectEvents[gPlayerAvatar.objectEventId];
    s16 x = player->currentCoords.x, y = player->currentCoords.y;

    MoveCoords(player->facingDirection, &x, &y);
    gFieldEffectArguments[0] = x;
    gFieldEffectArguments[1] = y;
    gFieldEffectArguments[2] = player->currentElevation;
    gFieldEffectArguments[3] = gSprites[player->spriteId].oam.priority;
    FieldEffectStart(FLDEFF_DUST);
    PlaySE(SE_M_DIG);
}

// specialvar Ichor_DigFindKind: what the dig turned up, as ICHOR_FIND_KIND_*.
// An item comes back in VAR_0x8006 (the item) and VAR_0x8007 (how many) for
// giveitem. Anything else is buffered for the message: a sherd's myth in
// STR_VAR_1 and its count in STR_VAR_2, an ostrakon's words in STR_VAR_1, a
// tablet's or page's number in STR_VAR_1.
u16 Ichor_DigFindKind(void)
{
    u32 n = sDig.find & 0xFF;

    if (sDig.find < 0xF000)
    {
        gSpecialVar_0x8006 = sDig.find;
        gSpecialVar_0x8007 = sDig.quantity;
        return ICHOR_FIND_KIND_ITEM;
    }
    switch (sDig.find & 0xFF00)
    {
    case ICHOR_FIND_SHERD(0):
    {
        u32 sherd = NextSherd(n);
        sDig.findFlag = FLAG_ICHOR_SHERDS_START + n * ICHOR_SHERDS_PER_AMPHORA + sherd;
        StringCopy(gStringVar1, sAmphoraMyths[n]);
        ConvertIntToDecimalStringN(gStringVar2, sherd + 1, STR_CONV_MODE_LEFT_ALIGN, 1);
        return ICHOR_FIND_KIND_SHERD;
    }
    case ICHOR_FIND_PROPHECY(0):
        sDig.findFlag = FLAG_ICHOR_PROPHECY_START + n - 1;
        ConvertIntToDecimalStringN(gStringVar1, n, STR_CONV_MODE_LEFT_ALIGN, 1);
        return ICHOR_FIND_KIND_PROPHECY;
    case ICHOR_FIND_PAGE(0):
        sDig.findFlag = FLAG_ICHOR_PAGES_START + n - 1;
        StringCopy(gStringVar1, sRomanNumerals[n - 1]);
        return ICHOR_FIND_KIND_PAGE;
    default: // ICHOR_FIND_OSTRAKON
        n = NextOstrakon();
        sDig.findFlag = FLAG_ICHOR_OSTRAKA_START + n;
        StringExpandPlaceholders(gStringVar1, sOstraka[n]);
        return ICHOR_FIND_KIND_OSTRAKON;
    }
}

// special Ichor_DigFinish: the find is taken. Sets the spot's flag and the
// find's own, and removes any object on this map hidden by the spot's flag
// (a dig-spot object shows until it's dug).
void Ichor_DigFinish(void)
{
    u32 i;

    if (sDig.findFlag != 0)
        FlagSet(sDig.findFlag);
    FlagSet(sDig.flag);
    if (gMapHeader.events == NULL) // the C tests have no map
        return;
    for (i = 0; i < gMapHeader.events->objectEventCount && i < OBJECT_EVENT_TEMPLATES_COUNT; i++)
    {
        const struct ObjectEventTemplate *template = &gSaveBlock1Ptr->objectEventTemplates[i];
        if (template->flagId == sDig.flag)
            RemoveObjectEventByLocalIdAndMap(template->localId,
                                             gSaveBlock1Ptr->location.mapNum,
                                             gSaveBlock1Ptr->location.mapGroup);
    }
}

// specialvar Ichor_SellToMoneychanger: a moneychanger (Pasion in Emporion,
// Astyra's) buys one VAR_0x8004 (a coin, or anything that sells) for the
// market's price plus VAR_0x8005 percent; blessings count as at a market.
// TRUE if sold, with the money paid in STR_VAR_1. FALSE if you have none, or
// it can't be sold.
u16 Ichor_SellToMoneychanger(void)
{
    u32 item = gSpecialVar_0x8004, paid;

    if (item == ITEM_NONE || item >= ITEMS_COUNT || !CheckBagHasItem(item, 1))
        return FALSE;
    paid = GetItemSellPrice(item) * (100 + gSpecialVar_0x8005) / 100;
    if (paid == 0)
        return FALSE;
    RemoveBagItem(item, 1);
    AddMoney(&gSaveBlock1Ptr->money, paid);
    ConvertIntToDecimalStringN(gStringVar1, paid, STR_CONV_MODE_LEFT_ALIGN, 6);
    return TRUE;
}

// The daily roll alone, for the C tests: the item or ICHOR_FIND_* code.
u16 Ichor_DigRollForTest(u32 spot, u32 tableArg)
{
    RollDailyFind(spot, tableArg);
    return sDig.find;
}
