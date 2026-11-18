// Ichor: the rites (design/SYSTEMS.md §3).
//
// Walk up to an altar and press A: PRAY (free; the god's minor blessing, and
// +1 Favor the first time each day), MAKE AN OFFERING (the major blessing and
// Favor by the god's taste), FAVOR (your rank), or LEAVE. Favor runs 0-100 per
// god and never drops. One blessing at a time, counted in steps like a Repel.
// Gifts come at Favor 30 (a lesson: a move taught to a Pokémon), 60 (a tool or
// relic upgrade) and 100 (the god's sacred animal).
//
// data/scripts/ichor_rites.pory holds the altar scripts; the specials and the
// blessing hooks the engine calls are here.
#include "global.h"
#include "ichor_star_chart.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_player_avatar.h"
#include "ichor_frozen.h"
#include "ichor_relics.h"
#include "ichor_rites.h"
#include "ichor_calendar.h"
#include "ichor_save.h"
#include "battle.h"
#include "item.h"
#include "list_menu.h"
#include "malloc.h"
#include "pokemon.h"
#include "random.h"
#include "rtc.h"
#include "script.h"
#include "script_menu.h"
#include "script_pokemon_util.h"
#include "string_util.h"
#include "strings.h"
#include "wild_encounter.h"
#include "constants/abilities.h"
#include "constants/hold_effects.h"
#include "constants/items.h"
#include "constants/moves.h"
#include "constants/pokemon.h"
#include "constants/rtc.h"

extern const u8 EventScript_IchorBlessingFaded[];

// --- The gods ------------------------------------------------------------------

// Offering classes, used in the taste tables beside real items.
#define OFFER_FEATHER   0xFFF1  // the seven feathers (Artemis's "first of the hunt")
#define OFFER_SEA_GIFT  0xFFF2  // Pearl, Big Pearl, Shoal Salt, Shoal Shell, Heart Scale
#define OFFER_BERRY     0xFFF3  // first fruits: any berry but the pomegranate (Pomeg)

struct IchorGod
{
    const u8 *name;
    const u8 *altar;      // what the altar looks like
    const u8 *sign;       // the god's answer to a prayer
    const u8 *blessing;   // the blessing's name
    const u8 *does;       // what it does, in a line the player can use
    const u8 *fade;       // when it ends
    u16 loved[2];
    u16 liked[3];
    u16 giftMove;         // gift I, a lesson
    u16 giftFlag;         // gift II, as a flag, or 0
    u16 giftItem;         // gift II, as an item, or ITEM_NONE
    const u8 *giftText;   // gift II
    const u8 *animal;     // gift III
};

static const struct IchorGod sGods[ICHOR_GOD_COUNT] =
{
    [ICHOR_GOD_HESTIA] = {
        .name = COMPOUND_STRING("Hestia"),
        .altar = COMPOUND_STRING("A hearth of Hestia.\nThe embers are still warm."),
        .sign = COMPOUND_STRING("The embers brighten, as if someone\nhad breathed on them."),
        .blessing = COMPOUND_STRING("Hearthfire"),
        .does = COMPOUND_STRING("Her warmth stays with you. Use it\nfrom the SELECT ring to rest anywhere."),
        .fade = COMPOUND_STRING("Hestia's warmth fades from you."),
        .loved = {ITEM_OLIVE_OIL}, .liked = {ITEM_BARLEY_CAKE, ITEM_HONEY},
        .giftMove = MOVE_WISH,
        .giftFlag = FLAG_ICHOR_EVER_EMBER,
        .giftText = COMPOUND_STRING("Her fire will never go out in you.\pHearthfire no longer fades, and\nany home's hearth will warm you."),
        .animal = COMPOUND_STRING("Kanthos's foal, the hearth donkey"),
    },
    [ICHOR_GOD_HERMES] = {
        .name = COMPOUND_STRING("Hermes"),
        .altar = COMPOUND_STRING("A herm of Hermes, its stone face\nworn smooth by passing hands."),
        .sign = COMPOUND_STRING("Somewhere close, a sandal strap\ncreaks. No one is there."),
        .blessing = COMPOUND_STRING("Swift Trade"),
        .does = COMPOUND_STRING("Hermes smiles on your bargains.\nPrices fall, and prizes rise."),
        .fade = COMPOUND_STRING("Hermes has gone on his way."),
        .loved = {ITEM_HONEY}, .liked = {ITEM_FRANKINCENSE, ITEM_OLIVE_OIL},
        .giftMove = MOVE_U_TURN,
        .giftFlag = FLAG_ICHOR_WINGED_TALARIA,
        .giftText = COMPOUND_STRING("Your Talaria sprout real wings!\pRunning, you can leap\na one-tile gap."),
        .animal = COMPOUND_STRING("a lyre-tortoise"),
    },
    [ICHOR_GOD_DEMETER] = {
        .name = COMPOUND_STRING("Demeter"),
        .altar = COMPOUND_STRING("A grain shrine of Demeter, hung\nwith dry ears of barley."),
        .sign = COMPOUND_STRING("The barley ears whisper,\nthough there's no wind."),
        .blessing = COMPOUND_STRING("Harvest"),
        .does = COMPOUND_STRING("Her plenty follows you. Wild Pokémon\ncarry more, and trees give more."),
        .fade = COMPOUND_STRING("Demeter's plenty passes."),
        .loved = {ITEM_BARLEY_CAKE}, .liked = {OFFER_BERRY},
        .giftMove = MOVE_LEECH_SEED,
        .giftFlag = FLAG_ICHOR_HARVEST_BASKET,
        .giftText = COMPOUND_STRING("She gives you a harvest basket.\pEvery berry tree you pick\nwill give one more."),
        .animal = COMPOUND_STRING("her chariot-serpent"),
    },
    [ICHOR_GOD_DIONYSUS] = {
        .name = COMPOUND_STRING("Dionysus"),
        .altar = COMPOUND_STRING("An ivy shrine of Dionysus,\nsticky with old wine."),
        .sign = COMPOUND_STRING("Somewhere a flute plays\nthree notes, and stops."),
        .blessing = COMPOUND_STRING("Revel"),
        .does = COMPOUND_STRING("The god of the vine passes you\nanother god's favor, and laughs."),
        .fade = COMPOUND_STRING("The revel winds down."),
        .loved = {ITEM_WINE}, .liked = {ITEM_FIGY_BERRY, ITEM_GREPA_BERRY},
        .giftMove = MOVE_SWAGGER,
        .giftFlag = FLAG_ICHOR_THYRSUS,
        .giftText = COMPOUND_STRING("He gives you a thyrsus, a fennel\nstaff crowned with a pine cone.\pHis Revels will turn to Frenzy\nfar more often."),
        .animal = COMPOUND_STRING("a panther"),
    },
    [ICHOR_GOD_ARTEMIS] = {
        .name = COMPOUND_STRING("Artemis"),
        .altar = COMPOUND_STRING("A forest shrine of Artemis.\nA bow is cut into the stone."),
        .sign = COMPOUND_STRING("A deer's track appears beside\nyours, then is gone."),
        .blessing = COMPOUND_STRING("Moonlit Hunt"),
        .does = COMPOUND_STRING("You move like her hunters. Fewer\nPokémon find you; rarer ones, by night."),
        .fade = COMPOUND_STRING("Artemis's moon sets on you."),
        .loved = {OFFER_FEATHER}, .liked = {ITEM_BARLEY_CAKE},
        .giftMove = MOVE_NIGHT_SLASH,
        .giftFlag = FLAG_ICHOR_HUNTERS_MOON,
        .giftText = COMPOUND_STRING("The Hunter's Moon shines in your\nAugur's Eye.\pIt can now tell a place's\nrarest Pokémon."),
        .animal = COMPOUND_STRING("the golden-horned deer"),
    },
    [ICHOR_GOD_HEPHAESTUS] = {
        .name = COMPOUND_STRING("Hephaestus"),
        .altar = COMPOUND_STRING("A forge altar of Hephaestus,\nblack with soot."),
        .sign = COMPOUND_STRING("Far off, a hammer rings once."),
        .blessing = COMPOUND_STRING("Forge-sight"),
        .does = COMPOUND_STRING("Your eyes catch every glint.\nHidden things show themselves."),
        .fade = COMPOUND_STRING("The forge-glow leaves your eyes."),
        .loved = {ITEM_BRONZE_VOTIVE}, .liked = {ITEM_WINE},
        .giftMove = MOVE_FLASH_CANNON,
        .giftFlag = FLAG_ICHOR_HEPHAESTUS_HAMMER,
        .giftText = COMPOUND_STRING("He reforges your Bronze Hammer!\pHephaestus's Hammer can split\nthe great boulders."),
        .animal = COMPOUND_STRING("the golden automaton"),
    },
    [ICHOR_GOD_APHRODITE] = {
        .name = COMPOUND_STRING("Aphrodite"),
        .altar = COMPOUND_STRING("A myrtle shrine of Aphrodite\nbeside a spring."),
        .sign = COMPOUND_STRING("The spring ripples, and a white\ndove lands on the rim."),
        .blessing = COMPOUND_STRING("Charm"),
        .does = COMPOUND_STRING("Her charm is on you. Your Pokémon\nwarm to you twice as fast."),
        .fade = COMPOUND_STRING("Aphrodite's charm fades."),
        .loved = {ITEM_FRANKINCENSE}, .liked = {ITEM_PRETTY_FEATHER, OFFER_SEA_GIFT},
        .giftMove = MOVE_DRAINING_KISS,
        .giftItem = ITEM_MYRTLE_WREATH,
        .giftText = COMPOUND_STRING("She crowns you with myrtle.\pA Pokémon that holds it\nnever grows cold to you."),
        .animal = COMPOUND_STRING("a swan"),
    },
    [ICHOR_GOD_APOLLO] = {
        .name = COMPOUND_STRING("Apollo"),
        .altar = COMPOUND_STRING("An altar of Apollo,\ncrowned with laurel."),
        .sign = COMPOUND_STRING("A laurel leaf turns in\nthe windless air."),
        .blessing = COMPOUND_STRING("Daylight"),
        .does = COMPOUND_STRING("His light is on you. Your Pokémon\nlearn more from every battle."),
        .fade = COMPOUND_STRING("Apollo's light fades from you."),
        .loved = {ITEM_LAUREL_SPRIG}, .liked = {ITEM_FRANKINCENSE, ITEM_HONEY},
        .giftMove = MOVE_SOLAR_BEAM,
        .giftItem = ITEM_POKE_FLUTE,
        .giftText = COMPOUND_STRING("He gives you a lyre.\pIts song wakes anything\nthat sleeps in your way."),
        .animal = COMPOUND_STRING("a raven"),
    },
    [ICHOR_GOD_ARES] = {
        .name = COMPOUND_STRING("Ares"),
        .altar = COMPOUND_STRING("A trophy of Ares: a bronze helmet\nand shield on a post."),
        .sign = COMPOUND_STRING("The shield rings, though\nnothing struck it."),
        .blessing = COMPOUND_STRING("War-lust"),
        .does = COMPOUND_STRING("Ares wants a fight. Weak Pokémon\nflee you, and strong ones come."),
        .fade = COMPOUND_STRING("Ares loses interest in you."),
        .giftMove = MOVE_BULK_UP,
        .giftItem = ITEM_VS_SEEKER,
        .giftText = COMPOUND_STRING("He gives you a war horn.\pBlow it, and the Trainers you\nhave beaten will want more."),
        .animal = COMPOUND_STRING("his war-dogs"),
    },
    [ICHOR_GOD_POSEIDON] = {
        .name = COMPOUND_STRING("Poseidon"),
        .altar = COMPOUND_STRING("A sea shrine of Poseidon,\ncrusted with salt."),
        .sign = COMPOUND_STRING("A wave breaks somewhere\nout of sight."),
        .blessing = COMPOUND_STRING("Calm Seas"),
        .does = COMPOUND_STRING("He calms the water for you. Every\ncast bites at once."),
        .fade = COMPOUND_STRING("The sea goes about its business."),
        .loved = {OFFER_SEA_GIFT}, .liked = {ITEM_WINE, ITEM_BARLEY_CAKE},
        .giftMove = MOVE_SCALD,
        .giftFlag = FLAG_ICHOR_TRITON_CONCH,
        .giftText = COMPOUND_STRING("Your conch becomes Triton's Conch!\pIts call will calm\nthe whirlpools."),
        .animal = COMPOUND_STRING("a hippocampus"),
    },
    [ICHOR_GOD_ATHENA] = {
        .name = COMPOUND_STRING("Athena"),
        .altar = COMPOUND_STRING("An owl stele of Athena."),
        .sign = COMPOUND_STRING("An owl calls once."),
        .blessing = COMPOUND_STRING("Owl's Eye"),
        .does = COMPOUND_STRING("Her owl watches for you. Hidden\nPokémon show, and you can always flee."),
        .fade = COMPOUND_STRING("Athena's owl flies off."),
        .loved = {ITEM_OLIVE_OIL}, .liked = {ITEM_FRANKINCENSE, ITEM_HONEY},
        .giftMove = MOVE_CALM_MIND,
        .giftFlag = FLAG_ICHOR_ATHENAS_STYLUS,
        .giftText = COMPOUND_STRING("She gives you a bronze stylus.\pYour Scroll of Deeds will hint\nat every task still open."),
        .animal = COMPOUND_STRING("an owl"),
    },
    [ICHOR_GOD_HERA] = {
        .name = COMPOUND_STRING("Hera"),
        .altar = COMPOUND_STRING("A wellhead sacred to Hera, its\nrim carved with peacock eyes."),
        .sign = COMPOUND_STRING("A peacock feather drifts\ndown into the well."),
        .blessing = COMPOUND_STRING("Queen's Care"),
        .does = COMPOUND_STRING("She watches over the young.\nEggs come and hatch twice as fast."),
        .fade = COMPOUND_STRING("Hera turns her gaze elsewhere."),
        .loved = {ITEM_POMEG_BERRY}, .liked = {ITEM_PRETTY_FEATHER, ITEM_HONEY},
        .giftMove = MOVE_PROTECT,
        .giftFlag = FLAG_ICHOR_EYES_OF_ARGUS,
        .giftText = COMPOUND_STRING("She gives you the Eyes of Argus.\pYour Augur's Eye never closes,\nand it sees shining Pokémon."),
        .animal = COMPOUND_STRING("the white cow of Argos"),
    },
    [ICHOR_GOD_ZEUS] = {
        .name = COMPOUND_STRING("Zeus"),
        .altar = COMPOUND_STRING("An oak shrine of Zeus. Acorns\nlie on the altar stone."),
        .sign = COMPOUND_STRING("Thunder mutters far away\nunder a clear sky."),
        .blessing = COMPOUND_STRING("Thunderhead"),
        .does = COMPOUND_STRING("His storm is on you. Shining and\nstorm-born Pokémon come out."),
        .fade = COMPOUND_STRING("The storm passes over."),
        .loved = {ITEM_WINE}, .liked = {ITEM_FRANKINCENSE, ITEM_HONEY},
        .giftMove = MOVE_THUNDERBOLT,
        .giftItem = ITEM_SHINY_CHARM,
        .giftText = COMPOUND_STRING("He gives you an acorn from the\noak of Dodona.\pShining Pokémon will\nfind you more often."),
        .animal = COMPOUND_STRING("the oak-dove of Dodona"),
    },
    [ICHOR_GOD_HECATE] = {
        .name = COMPOUND_STRING("Hecate"),
        .altar = COMPOUND_STRING("A crossroads shrine of Hecate,\nthree faces on one pillar."),
        .sign = COMPOUND_STRING("A dog barks three times,\nfrom three directions."),
        .blessing = COMPOUND_STRING("Crossroads"),
        .does = COMPOUND_STRING("She lights your way. Your torch\nburns brighter, and the night stirs."),
        .fade = COMPOUND_STRING("Hecate's torches go out."),
        .loved = {ITEM_BARLEY_CAKE}, .liked = {ITEM_HONEY, OFFER_SEA_GIFT},
        .giftMove = MOVE_HEX,
        .giftFlag = FLAG_ICHOR_THREE_FLAMED_TORCH,
        .giftText = COMPOUND_STRING("Your torch splits into three flames!\pThe Three-Flamed Torch lights\nfarther and burns thornwebs."),
        .animal = COMPOUND_STRING("her polecat"),
    },
    [ICHOR_GOD_HADES] = {
        .name = COMPOUND_STRING("Hades"),
        .altar = COMPOUND_STRING("A black altar of Hades,\ncold to the touch."),
        .sign = COMPOUND_STRING("The air goes still and cold."),
        .blessing = COMPOUND_STRING("Wealth Below"),
        .does = COMPOUND_STRING("He shares what lies beneath.\nThe earth gives double."),
        .fade = COMPOUND_STRING("Hades takes back his gifts."),
        .loved = {ITEM_RELIC_COPPER}, .liked = {ITEM_POMEG_BERRY},
        .giftMove = MOVE_SHADOW_BALL,
        .giftFlag = FLAG_ICHOR_HELM_OF_HADES,
        .giftText = COMPOUND_STRING("Your helm becomes the Helm of\nHades. It hides you even by day."),
        .animal = COMPOUND_STRING("the black horse"),
    },
};

// Gods Dionysus's Revel can pass on: all but himself, Zeus and Hades.
static const u8 sRevelGods[] = {
    ICHOR_GOD_HESTIA, ICHOR_GOD_HERMES, ICHOR_GOD_DEMETER, ICHOR_GOD_ARTEMIS, ICHOR_GOD_HEPHAESTUS,
    ICHOR_GOD_APHRODITE, ICHOR_GOD_APOLLO, ICHOR_GOD_ARES, ICHOR_GOD_POSEIDON, ICHOR_GOD_ATHENA,
    ICHOR_GOD_HERA, ICHOR_GOD_HECATE,
};

// Everything the offering list offers (besides any berry).
static const u16 sOfferings[] = {
    ITEM_OLIVE_OIL, ITEM_BARLEY_CAKE, ITEM_WINE, ITEM_FRANKINCENSE, ITEM_LAUREL_SPRIG, ITEM_BRONZE_VOTIVE,
    ITEM_HONEY, ITEM_RELIC_COPPER,
    ITEM_HEALTH_FEATHER, ITEM_MUSCLE_FEATHER, ITEM_RESIST_FEATHER, ITEM_GENIUS_FEATHER, ITEM_CLEVER_FEATHER,
    ITEM_SWIFT_FEATHER, ITEM_PRETTY_FEATHER,
    ITEM_PEARL, ITEM_BIG_PEARL, ITEM_SHOAL_SALT, ITEM_SHOAL_SHELL, ITEM_HEART_SCALE,
};

static bool32 IsValidGod(u32 god)
{
    return god > ICHOR_GOD_NONE && god < ICHOR_GOD_COUNT;
}

const u8 *Ichor_GetGodName(u32 god)
{
    return IsValidGod(god) ? sGods[god].name : gText_EmptyString2;
}

// --- Favor -----------------------------------------------------------------------

u8 Ichor_GetFavor(u32 god)
{
    return IsValidGod(god) ? gIchorSave.favor[god] : 0;
}

void Ichor_AddFavorTo(u32 god, u32 amount)
{
    u32 favor;
    if (!IsValidGod(god))
        return;
    favor = gIchorSave.favor[god] + amount;
    gIchorSave.favor[god] = min(favor, ICHOR_FAVOR_MAX);
    if (gIchorSave.favor[god] >= 30)
    {
        if (god == ICHOR_GOD_ARTEMIS)
            Ichor_PlaceStar(ICHOR_STAR_ORION);
        else if (god == ICHOR_GOD_HERA)
            Ichor_PlaceStar(ICHOR_STAR_CANCER);
    }
}

// special Ichor_AddFavor: VAR_0x8004 god, VAR_0x8005 amount. Favor never drops.
void Ichor_AddFavor(void)
{
    Ichor_AddFavorTo(gSpecialVar_0x8004, gSpecialVar_0x8005);
}

// specialvar Ichor_GetFavorOf: VAR_0x8004 god.
u16 Ichor_GetFavorOf(void)
{
    return Ichor_GetFavor(gSpecialVar_0x8004);
}

// --- Blessings ---------------------------------------------------------------------

bool32 Ichor_HasBlessing(void)
{
    return IsValidGod(gIchorSave.blessing.god) && gIchorSave.blessing.steps != 0;
}

bool32 Ichor_IsFrenzy(void)
{
    return Ichor_HasBlessing() && (gIchorSave.blessing.flags & ICHOR_BLESSING_FRENZY);
}

void Ichor_SetBlessingTo(u32 god, u32 steps, u32 flags)
{
    gIchorSave.blessing.god = god;
    gIchorSave.blessing.steps = min(steps, ICHOR_BLESSING_MAX_STEPS);
    gIchorSave.blessing.flags = flags;
}

// specialvar Ichor_GetBlessingGod: the god whose blessing is on you, or 0.
u16 Ichor_GetBlessingGod(void)
{
    return Ichor_HasBlessing() ? gIchorSave.blessing.god : ICHOR_GOD_NONE;
}

// special Ichor_GrantBlessing: VAR_0x8004 god, VAR_0x8005 steps (a minor blessing).
void Ichor_GrantBlessing(void)
{
    if (IsValidGod(gSpecialVar_0x8004))
        Ichor_SetBlessingTo(gSpecialVar_0x8004, gSpecialVar_0x8005, 0);
}

static u32 ScaleByRank(u32 god, u32 steps)
{
    if (Ichor_GetFavor(god) >= ICHOR_RANK_BELOVED)
        steps = steps * 3 / 2;
    return steps;
}

// Bless the player with `god`'s blessing. Dionysus passes on another god's, at
// 1.5x the length; one time in eight a major Revel is a Frenzy instead, one time
// in three once he has given the thyrsus (his gift II).
static void Bless(u32 god, u32 steps, bool32 major)
{
    u32 flags = major ? ICHOR_BLESSING_MAJOR : 0;

    steps = ScaleByRank(god, steps);
    if (god == ICHOR_GOD_DIONYSUS)
    {
        if (major && (Random() % (FlagGet(FLAG_ICHOR_THYRSUS) ? 3 : 8)) == 0)
        {
            Ichor_SetBlessingTo(ICHOR_GOD_DIONYSUS, steps, flags | ICHOR_BLESSING_FRENZY);
            return;
        }
        god = sRevelGods[Random() % ARRAY_COUNT(sRevelGods)];
        steps = steps * 3 / 2;
        flags |= ICHOR_BLESSING_REVEL;
    }
    Ichor_SetBlessingTo(god, steps, flags);
}

// The step tick: one step off the blessing; when it runs out, the god's line.
static bool32 BlessingStep(void)
{
    u32 god = gIchorSave.blessing.god;

    if (!Ichor_HasBlessing())
        return FALSE;
    if (god == ICHOR_GOD_HESTIA && FlagGet(FLAG_ICHOR_EVER_EMBER))
        return FALSE;
    if (--gIchorSave.blessing.steps != 0)
        return FALSE;
    gIchorSave.blessing.god = ICHOR_GOD_NONE;
    gIchorSave.blessing.flags = 0;
    StringCopy(gStringVar4, sGods[god].fade);
    ScriptContext_SetupScript(EventScript_IchorBlessingFaded);
    return TRUE;
}

// field_control_avatar.c, every step: the blessing counts down, and so does a
// carried flame (src/ichor_relics.c). TRUE when a script started.
bool8 Ichor_OnStep(void)
{
    bool32 talked = BlessingStep();
    return Ichor_CarriedFlameStep(!talked) || talked;
}

// --- Offerings ----------------------------------------------------------------------

enum { TASTE_ACCEPT, TASTE_LIKE, TASTE_LOVE, TASTE_REFUSE };

static bool32 IsFeather(u32 item)
{
    return (item >= ITEM_HEALTH_FEATHER && item <= ITEM_SWIFT_FEATHER) || item == ITEM_PRETTY_FEATHER;
}

static bool32 IsSeaGift(u32 item)
{
    return item == ITEM_PEARL || item == ITEM_BIG_PEARL || item == ITEM_SHOAL_SALT
        || item == ITEM_SHOAL_SHELL || item == ITEM_HEART_SCALE;
}

static bool32 IsBerry(u32 item)
{
    return item >= FIRST_BERRY_INDEX && item <= LAST_BERRY_INDEX;
}

bool32 Ichor_TakeFirstFruits(void)
{
    u32 item, count = 0, remaining = 3;

    for (item = FIRST_BERRY_INDEX; item <= LAST_BERRY_INDEX && count < 3; item++)
        count += CountTotalItemQuantityInBag(item);
    if (count < 3)
        return FALSE;

    for (item = FIRST_BERRY_INDEX; item <= LAST_BERRY_INDEX && remaining; item++)
    {
        u32 take = min(remaining, CountTotalItemQuantityInBag(item));
        if (take)
        {
            RemoveBagItem(item, take);
            remaining -= take;
        }
    }
    return TRUE;
}

static bool32 MatchesTaste(u16 taste, u32 item)
{
    switch (taste)
    {
    case ITEM_NONE:      return FALSE;
    case OFFER_FEATHER:  return IsFeather(item);
    case OFFER_SEA_GIFT: return IsSeaGift(item);
    case OFFER_BERRY:    return IsBerry(item) && item != ITEM_POMEG_BERRY;
    default:             return taste == item;
    }
}

static bool32 IsOffering(u32 item)
{
    u32 i;
    if (IsBerry(item))
        return TRUE;
    for (i = 0; i < ARRAY_COUNT(sOfferings); i++)
    {
        if (sOfferings[i] == item)
            return TRUE;
    }
    return FALSE;
}

static u32 GetTaste(u32 god, u32 item)
{
    u32 i;
    if (god == ICHOR_GOD_DEMETER && item == ITEM_POMEG_BERRY)
        return TASTE_REFUSE;  // she looks at the pomegranate for a long time
    for (i = 0; i < ARRAY_COUNT(sGods[god].loved); i++)
    {
        if (MatchesTaste(sGods[god].loved[i], item))
            return TASTE_LOVE;
    }
    for (i = 0; i < ARRAY_COUNT(sGods[god].liked); i++)
    {
        if (MatchesTaste(sGods[god].liked[i], item))
            return TASTE_LIKE;
    }
    return TASTE_ACCEPT;
}

static const u8 sFavorByTaste[] = { [TASTE_ACCEPT] = 1, [TASTE_LIKE] = 3, [TASTE_LOVE] = 5, [TASTE_REFUSE] = 0 };
static const u16 sStepsByTaste[] = { [TASTE_ACCEPT] = 150, [TASTE_LIKE] = 300, [TASTE_LOVE] = 500, [TASTE_REFUSE] = 0 };
#define PRAYER_STEPS        100
#define PRAYER_STEPS_KNOWN  150

static void PushEntry(const u8 *text, u16 id)
{
    struct ListMenuItem item;
    u8 *name = Alloc(32); // freed by the menu
    StringExpandPlaceholders(name, text);
    item.name = name;
    item.id = id;
    MultichoiceDynamic_PushElement(item);
}

// special Ichor_BuildOfferingMenu: one entry per offering in the bag, its id
// the item. VAR_RESULT is how many.
void Ichor_BuildOfferingMenu(void)
{
    u32 item, count = 0;
    u8 *label = Alloc(32);

    for (item = ITEM_NONE + 1; item < ITEMS_COUNT; item++)
    {
        u16 n;
        u8 *end;
        if (!IsOffering(item) || !CheckBagHasItem(item, 1))
            continue;
        n = CountTotalItemQuantityInBag(item);
        end = CopyItemName(item, label);
        end = StringCopy(end, COMPOUND_STRING(" x"));
        ConvertIntToDecimalStringN(end, min(n, 999), STR_CONV_MODE_LEFT_ALIGN, 3);
        PushEntry(label, item);
        count++;
    }
    Free(label);
    gSpecialVar_Result = count;
}

// --- The altar's specials --------------------------------------------------------------
// The altar script keeps its god in VAR_0x800A and whether it's the god's temple
// altar (offerings count double) in VAR_0x800B.

#define ALTAR_GOD    gSpecialVar_0x800A
#define ALTAR_TEMPLE gSpecialVar_0x800B

// special Ichor_BufferAltar: the altar's look into gStringVar4, the god's name
// into STR_VAR_1.
void Ichor_BufferAltar(void)
{
    StringCopy(gStringVar1, Ichor_GetGodName(ALTAR_GOD));
    StringExpandPlaceholders(gStringVar4, sGods[ALTAR_GOD].altar);
}

enum { ALTAR_PRAY, ALTAR_OFFER, ALTAR_FAVOR, ALTAR_LESSON, ALTAR_REST, ALTAR_BATTLE, ALTAR_LEAVE };

// special Ichor_BuildAltarMenu: PRAY, MAKE AN OFFERING (OFFER A BATTLE at Ares's
// trophy), FAVOR, LESSON once the god has taught one, REST at a hearth with
// Ever-Ember, LEAVE.
void Ichor_BuildAltarMenu(void)
{
    PushEntry(COMPOUND_STRING("PRAY"), ALTAR_PRAY);
    if (ALTAR_GOD == ICHOR_GOD_ARES)
        PushEntry(COMPOUND_STRING("OFFER A BATTLE"), ALTAR_BATTLE);
    else
        PushEntry(COMPOUND_STRING("MAKE AN OFFERING"), ALTAR_OFFER);
    PushEntry(COMPOUND_STRING("FAVOR"), ALTAR_FAVOR);
    if (FlagGet(FLAG_ICHOR_GIFT(ALTAR_GOD, ICHOR_GIFT_I)))
        PushEntry(COMPOUND_STRING("LESSON"), ALTAR_LESSON);
    if (ALTAR_GOD == ICHOR_GOD_HESTIA && FlagGet(FLAG_ICHOR_EVER_EMBER))
        PushEntry(COMPOUND_STRING("REST"), ALTAR_REST);
    PushEntry(COMPOUND_STRING("LEAVE"), ALTAR_LEAVE);
}

// specialvar Ichor_CheckBlessingConflict: TRUE if another god's blessing is on
// the player; its god's name goes in STR_VAR_2.
bool8 Ichor_CheckBlessingConflict(void)
{
    if (!Ichor_HasBlessing() || gIchorSave.blessing.god == ALTAR_GOD)
        return FALSE;
    StringCopy(gStringVar2, Ichor_GetGodName(gIchorSave.blessing.god));
    return TRUE;
}

// Puts "<God>'s blessing, <Name>, is on you." and what it does after `head`.
static void AppendBlessingLine(u8 *dst)
{
    u32 god = gIchorSave.blessing.god;
    if (gIchorSave.blessing.flags & ICHOR_BLESSING_FRENZY)
    {
        StringAppend(dst, COMPOUND_STRING("\pThe wine goes to your head.\nFrenzy! The wilds run hot."));
        return;
    }
    if (gIchorSave.blessing.flags & ICHOR_BLESSING_REVEL)
    {
        StringAppend(dst, COMPOUND_STRING("\pDionysus laughs and passes you\n"));
        StringAppend(dst, sGods[god].name);
        StringAppend(dst, COMPOUND_STRING("'s cup instead."));
    }
    StringAppend(dst, COMPOUND_STRING("\p"));
    StringAppend(dst, sGods[god].blessing);
    StringAppend(dst, COMPOUND_STRING(" is on you.\p"));
    StringAppend(dst, sGods[god].does);
}

// special Ichor_Pray: the minor blessing; +1 Favor the first time today.
void Ichor_Pray(void)
{
    u32 god = ALTAR_GOD;
    u32 steps = Ichor_GetFavor(god) >= ICHOR_RANK_KNOWN ? PRAYER_STEPS_KNOWN : PRAYER_STEPS;
    u8 *dst = gStringVar4;

    if (!FlagGet(FLAG_DAILY_ICHOR_PRAYED_START + god))
    {
        FlagSet(FLAG_DAILY_ICHOR_PRAYED_START + god);
        Ichor_AddFavorTo(god, 1);
    }
    Bless(god, steps, FALSE);
    dst = StringCopy(dst, COMPOUND_STRING("You pray to "));
    dst = StringCopy(dst, sGods[god].name);
    dst = StringCopy(dst, COMPOUND_STRING(".\p"));
    StringCopy(dst, sGods[god].sign);
    AppendBlessingLine(gStringVar4);
}

// special Ichor_MakeOffering: VAR_0x8006 is the item. Takes it (unless refused),
// gives Favor by the god's taste (double at the god's temple; Hestia takes +1 of
// every offering to anyone), and the major blessing. VAR_RESULT is the taste.
void Ichor_MakeOffering(void)
{
    u32 god = ALTAR_GOD, item = gSpecialVar_0x8006;
    u32 taste = GetTaste(god, item);
    u32 favor = sFavorByTaste[taste];
    u8 *dst = gStringVar4;

    gSpecialVar_Result = taste;
    if (taste == TASTE_REFUSE)
    {
        StringCopy(gStringVar4, COMPOUND_STRING("Demeter looks at the fruit for a\nlong time. She does not take it."));
        return;
    }
    RemoveBagItem(item, 1);
    if (ALTAR_TEMPLE)
        favor *= 2;
    Ichor_AddFavorTo(god, favor);
    if (god != ICHOR_GOD_HESTIA)
        Ichor_AddFavorTo(ICHOR_GOD_HESTIA, 1); // she took the first share of every feast
    Bless(god, sStepsByTaste[taste], TRUE);

    dst = StringCopy(dst, COMPOUND_STRING("You offer the "));
    dst = CopyItemName(item, dst);
    dst = StringCopy(dst, COMPOUND_STRING("\nto "));
    dst = StringCopy(dst, sGods[god].name);
    dst = StringCopy(dst, COMPOUND_STRING(".\p"));
    if (taste == TASTE_LOVE)
        dst = StringCopy(dst, COMPOUND_STRING("The god is delighted!\n"));
    else if (taste == TASTE_LIKE)
        dst = StringCopy(dst, COMPOUND_STRING("It is gladly taken.\n"));
    else
        dst = StringCopy(dst, COMPOUND_STRING("It is accepted.\n"));
    StringCopy(dst, sGods[god].sign);
    AppendBlessingLine(gStringVar4);
}

static const u8 *GetRankName(u32 favor)
{
    if (favor >= ICHOR_RANK_CHOSEN)
        return COMPOUND_STRING("Chosen");
    if (favor >= ICHOR_RANK_BELOVED)
        return COMPOUND_STRING("Beloved");
    if (favor >= ICHOR_RANK_FAVORED)
        return COMPOUND_STRING("Favored");
    return COMPOUND_STRING("Known");
}

// special Ichor_BufferFavor: the FAVOR entry's text.
void Ichor_BufferFavor(void)
{
    u32 god = ALTAR_GOD, favor = Ichor_GetFavor(god), next;
    u8 *dst = gStringVar4;

    if (favor < ICHOR_RANK_KNOWN)
    {
        dst = StringCopy(dst, sGods[god].name);
        StringCopy(dst, COMPOUND_STRING(" doesn't know your\nname yet."));
        return;
    }
    dst = StringCopy(dst, sGods[god].name);
    dst = StringCopy(dst, COMPOUND_STRING(" knows your name.\pYou are "));
    dst = StringCopy(dst, GetRankName(favor));
    dst = StringCopy(dst, COMPOUND_STRING(" of "));
    dst = StringCopy(dst, sGods[god].name);
    dst = StringCopy(dst, COMPOUND_STRING("."));
    next = favor < ICHOR_RANK_FAVORED ? ICHOR_RANK_FAVORED : favor < ICHOR_RANK_BELOVED ? ICHOR_RANK_BELOVED
         : favor < ICHOR_RANK_CHOSEN ? ICHOR_RANK_CHOSEN : 0;
    if (next != 0)
    {
        dst = StringCopy(dst, COMPOUND_STRING("\n"));
        dst = ConvertIntToDecimalStringN(dst, next - favor, STR_CONV_MODE_LEFT_ALIGN, 3);
        StringCopy(dst, COMPOUND_STRING(" more to the next gift."));
    }
}

// --- Gifts -------------------------------------------------------------------------

// specialvar Ichor_NextGiftDue: the first gift due at this altar's god
// (ICHOR_GIFT_I, _II or _III), or 0xFF. Buffers its text: for gift I the move
// goes in STR_VAR_2 and VAR_0x8005 (for ChooseMonForMoveTutor); for gift II an
// item goes in VAR_0x8006.
u16 Ichor_NextGiftDue(void)
{
    u32 god = ALTAR_GOD, favor = Ichor_GetFavor(god);
    u8 *dst = gStringVar4;

    StringCopy(gStringVar1, sGods[god].name);
    if (favor >= ICHOR_RANK_FAVORED && !FlagGet(FLAG_ICHOR_GIFT(god, ICHOR_GIFT_I)))
    {
        gSpecialVar_0x8005 = sGods[god].giftMove;
        StringCopy(gStringVar2, GetMoveName(sGods[god].giftMove));
        return ICHOR_GIFT_I;
    }
    if (favor >= ICHOR_RANK_BELOVED && !FlagGet(FLAG_ICHOR_GIFT(god, ICHOR_GIFT_II)))
    {
        gSpecialVar_0x8006 = sGods[god].giftItem;
        StringCopy(dst, sGods[god].giftText);
        return ICHOR_GIFT_II;
    }
    if (favor >= ICHOR_RANK_CHOSEN && !FlagGet(FLAG_ICHOR_GIFT(god, ICHOR_GIFT_III)))
    {
        dst = StringCopy(dst, COMPOUND_STRING("Something stirs at the edge of\nsight: "));
        dst = StringCopy(dst, sGods[god].animal);
        StringCopy(dst, COMPOUND_STRING(".\pIt watches you a long moment,\nthen goes. You'll meet again."));
        return ICHOR_GIFT_III;
    }
    return 0xFF;
}

// special Ichor_TakeGift: VAR_0x8005 is the gift (ICHOR_GIFT_*) just given;
// marks it, and sets gift II's upgrade flag.
void Ichor_TakeGift(void)
{
    u32 god = ALTAR_GOD;
    FlagSet(FLAG_ICHOR_GIFT(god, gSpecialVar_0x8005));
    if (gSpecialVar_0x8005 == ICHOR_GIFT_II && sGods[god].giftFlag != 0)
        FlagSet(sGods[god].giftFlag);
}

// special Ichor_BufferLesson: the LESSON entry: gift I's move again, like a TM.
void Ichor_BufferLesson(void)
{
    gSpecialVar_0x8005 = sGods[ALTAR_GOD].giftMove;
    StringCopy(gStringVar1, sGods[ALTAR_GOD].name);
    StringCopy(gStringVar2, GetMoveName(sGods[ALTAR_GOD].giftMove));
}

// special Ichor_GetLovedOffering: the god's first loved real item in VAR_0x8006
// (for the Hierophant's free offering), or ITEM_NONE.
void Ichor_GetLovedOffering(void)
{
    u16 item = sGods[ALTAR_GOD].loved[0];
    if (item == OFFER_SEA_GIFT)
        item = ITEM_PEARL;
    else if (item == OFFER_FEATHER)
        item = ITEM_PRETTY_FEATHER;
    else if (item == OFFER_BERRY)
        item = ITEM_ORAN_BERRY;
    gSpecialVar_0x8006 = item;
}

// specialvar Ichor_CheckGiftTaken: VAR_0x8005 = ICHOR_GIFT_*; STR_VAR_1 = the god.
bool8 Ichor_CheckGiftTaken(void)
{
    StringCopy(gStringVar1, sGods[ALTAR_GOD].name);
    return FlagGet(FLAG_ICHOR_GIFT(ALTAR_GOD, gSpecialVar_0x8005));
}

// specialvar Ichor_CheckAltarCleansed / special Ichor_CleanseAltar: VAR_0x8005
// is a desecrated altar's index. Cleansing gives its god +3 Favor.
bool8 Ichor_CheckAltarCleansed(void)
{
    return FlagGet(FLAG_ICHOR_ALTARS_START + gSpecialVar_0x8005);
}

void Ichor_CleanseAltar(void)
{
    FlagSet(FLAG_ICHOR_ALTARS_START + gSpecialVar_0x8005);
    Ichor_AddFavorTo(ALTAR_GOD, ICHOR_FAVOR_CLEANSE);
    StringCopy(gStringVar1, sGods[ALTAR_GOD].name);
}

// special Ichor_AresVictory: a won bout is Ares's loved offering.
void Ichor_AresVictory(void)
{
    Ichor_AddFavorTo(ICHOR_GOD_ARES, sFavorByTaste[TASTE_LOVE]);
    Bless(ICHOR_GOD_ARES, sStepsByTaste[TASTE_LOVE], TRUE);
    StringCopy(gStringVar4, COMPOUND_STRING("Ares is satisfied.\n"));
    StringAppend(gStringVar4, sGods[ICHOR_GOD_ARES].sign);
    AppendBlessingLine(gStringVar4);
}

// --- Hestia's Hearthfire ------------------------------------------------------------

// special Ichor_UseHearthfire: heal the party (a prayer's minor Hearthfire
// heals HP only) and end the blessing.
void Ichor_UseHearthfire(void)
{
    u32 i;
    if (gIchorSave.blessing.flags & ICHOR_BLESSING_MAJOR)
    {
        HealPlayerParty();
    }
    else
    {
        for (i = 0; i < PARTY_SIZE; i++)
        {
            u16 maxHP = GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_MAX_HP);
            if (GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_SPECIES) != SPECIES_NONE
             && !GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_IS_EGG)
             && GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_HP) != 0)
                SetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_HP, &maxHP);
        }
    }
    gIchorSave.blessing.god = ICHOR_GOD_NONE;
    gIchorSave.blessing.steps = 0;
    gIchorSave.blessing.flags = 0;
}

// specialvar Ichor_HasHearthfire: Hestia's blessing is on the player.
bool8 Ichor_HasHearthfire(void)
{
    return Ichor_IsBlessed(ICHOR_GOD_HESTIA);
}

// special Ichor_BufferBlessingPanel: "Apollo (412)" for the start menu's info
// panel, into gStringVar4. Ever-Ember's Hearthfire shows no count.
void Ichor_BufferBlessingPanel(u8 *dst)
{
    dst = StringCopy(dst, sGods[gIchorSave.blessing.god].name);
    if (gIchorSave.blessing.flags & ICHOR_BLESSING_FRENZY)
        dst = StringCopy(dst, COMPOUND_STRING("'s Frenzy"));
    if (gIchorSave.blessing.god == ICHOR_GOD_HESTIA && FlagGet(FLAG_ICHOR_EVER_EMBER))
        return;
    dst = StringCopy(dst, COMPOUND_STRING(" ("));
    dst = ConvertIntToDecimalStringN(dst, gIchorSave.blessing.steps, STR_CONV_MODE_LEFT_ALIGN, 4);
    StringCopy(dst, COMPOUND_STRING(")"));
}

// --- The blessings' effects, one hook each in vanilla code ------------------------------

static bool32 IsNight(void)
{
    return GetTimeOfDay() == TIME_NIGHT;
}

// Artemis: a quarter fewer encounters. Dionysus's Frenzy: twice as many.
// Poseidon: half as many while surfing.
u32 Ichor_ModifyEncounterRate(u32 rate)
{
    if (Ichor_IsFrozenHour())  // nothing moves in the Frozen Hour, wild Pokémon included
        return 0;
    if (Ichor_IsFrenzy())
        return rate * 2;
    if (Ichor_IsBlessed(ICHOR_GOD_ARTEMIS))
        return rate * 3 / 4;
    if (Ichor_IsBlessed(ICHOR_GOD_POSEIDON) && TestPlayerAvatarFlags(PLAYER_AVATAR_FLAG_SURFING))
        return rate / 2;
    return rate;
}

// Artemis at night: a land route's three rarest slots (9-11, 6 in 100) come
// three times as often: 12 more in 100, weighted as they are (4:1:1).
u32 Ichor_ModifyLandSlot(u32 index)
{
    u32 r;
    if (!Ichor_IsBlessed(ICHOR_GOD_ARTEMIS) || !IsNight() || index >= 9)
        return index;
    r = Random() % 100;
    if (r < 8)
        return 9;
    if (r < 10)
        return 10;
    if (r < 12)
        return 11;
    return index;
}

static bool32 IsBoostedSpecies(u32 species)
{
    bool32 zeus = Ichor_IsBlessed(ICHOR_GOD_ZEUS);
    bool32 hecate = Ichor_IsBlessed(ICHOR_GOD_HECATE) && IsNight();
    if (!zeus && !hecate)
        return FALSE;
    if (zeus && (gSpeciesInfo[species].types[0] == TYPE_ELECTRIC || gSpeciesInfo[species].types[1] == TYPE_ELECTRIC
              || gSpeciesInfo[species].types[0] == TYPE_FLYING || gSpeciesInfo[species].types[1] == TYPE_FLYING))
        return TRUE;
    if (hecate && (gSpeciesInfo[species].types[0] == TYPE_GHOST || gSpeciesInfo[species].types[1] == TYPE_GHOST
                || gSpeciesInfo[species].types[0] == TYPE_DARK || gSpeciesInfo[species].types[1] == TYPE_DARK
                || gSpeciesInfo[species].types[0] == TYPE_PSYCHIC || gSpeciesInfo[species].types[1] == TYPE_PSYCHIC))
        return TRUE;
    return FALSE;
}

// Zeus (Electric and Flying) and Hecate at night (Ghost, Dark, Psychic): those
// types come about twice as often. A miss draws once more, keeping only a hit.
u32 Ichor_ModifyWildSlot(const struct WildPokemon *wildPokemon, u32 index, u32 (*choose)(void))
{
    u32 other;
    index = Ichor_FestivalWildSlot(wildPokemon, index, choose); // the Anthesteria (src/ichor_calendar.c)
    if (!(Ichor_IsBlessed(ICHOR_GOD_ZEUS) || Ichor_IsBlessed(ICHOR_GOD_HECATE)) || IsBoostedSpecies(wildPokemon[index].species))
        return index;
    other = choose();
    return IsBoostedSpecies(wildPokemon[other].species) ? other : index;
}

// Ares: wild Pokémon five or more levels below your lead don't come.
bool32 Ichor_IsWildLevelAllowed(u32 level)
{
    u32 lead;
    if (!Ichor_IsBlessed(ICHOR_GOD_ARES))
        return TRUE;
    lead = GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_LEVEL);
    return level + 5 > lead;
}

// Ares: wild levels +2. The Frenzy: +3.
u32 Ichor_ModifyWildLevel(u32 level)
{
    if (Ichor_IsFrenzy())
        level += 3;
    else if (Ichor_IsBlessed(ICHOR_GOD_ARES))
        level += 2;
    return min(level, MAX_LEVEL);
}

// Aphrodite: two wild Pokémon in three are the opposite gender of your lead.
u32 Ichor_ModifyWildGender(u32 gender, u32 species)
{
    u32 lead;
    if (gender != MON_GENDER_RANDOM || !Ichor_IsBlessed(ICHOR_GOD_APHRODITE) || (Random() % 3) == 0)
        return gender;
    lead = GetMonGender(&gParties[B_TRAINER_PLAYER][0]);
    if (lead == MON_MALE)
        return MON_FEMALE;
    if (lead == MON_FEMALE)
        return MON_MALE;
    return gender;
}

// Demeter: wild Pokémon carry held items twice as often (as Compound Eyes does).
bool32 Ichor_BoostsWildHeldItems(void)
{
    return Ichor_IsBlessed(ICHOR_GOD_DEMETER);
}

// Apollo +20%, Ares +10%, the Frenzy +50%.
void Ichor_ModifyExp(s32 *expAmount)
{
    if (Ichor_IsFrenzy())
        *expAmount = *expAmount * 150 / 100;
    else if (Ichor_IsBlessed(ICHOR_GOD_APOLLO))
        *expAmount = *expAmount * 120 / 100;
    else if (Ichor_IsBlessed(ICHOR_GOD_ARES))
        *expAmount = *expAmount * 110 / 100;
}

// Hermes: trainer prize money +20%.
u32 Ichor_ModifyPrizeMoney(u32 money)
{
    return Ichor_IsBlessed(ICHOR_GOD_HERMES) ? money * 120 / 100 : money;
}

// Athena: escape from wild battles always succeeds.
bool32 Ichor_AlwaysEscapes(u32 battler)
{
    return Ichor_IsBlessed(ICHOR_GOD_ATHENA) && GetBattlerSide(battler) == B_SIDE_PLAYER
        && !(gBattleTypeFlags & BATTLE_TYPE_TRAINER);
}

// Hermes: Agora prices -20%.
u32 Ichor_ModifyBuyPrice(u32 price)
{
    return Ichor_IsBlessed(ICHOR_GOD_HERMES) ? price * 80 / 100 : price;
}

// Hermes: selling +20%. Hades: the coins (obol, owl, stater) +50%.
u32 Ichor_ModifySellPrice(u32 itemId, u32 price)
{
    if (Ichor_IsBlessed(ICHOR_GOD_HADES) && (itemId == ITEM_RELIC_COPPER || itemId == ITEM_RELIC_SILVER || itemId == ITEM_RELIC_GOLD))
        return price * 150 / 100;
    if (Ichor_IsBlessed(ICHOR_GOD_HERMES))
        return price * 120 / 100;
    return price;
}

// Poseidon: every cast gets a bite at once, and the rods' rare slots come twice as often.
bool32 Ichor_FishBitesAtOnce(void)
{
    return Ichor_IsBlessed(ICHOR_GOD_POSEIDON);
}

bool32 Ichor_FavorsRareFishingSlots(void)
{
    return Ichor_IsBlessed(ICHOR_GOD_POSEIDON);
}

// Zeus: one more shiny roll, as a Lure gives.
u32 Ichor_ExtraShinyRolls(void)
{
    return Ichor_IsBlessed(ICHOR_GOD_ZEUS) ? 1 : 0;
}

// Hera: eggs hatch twice as fast, and the day care finds them twice as often.
u32 Ichor_ExtraEggCycles(void)
{
    return Ichor_IsBlessed(ICHOR_GOD_HERA) ? 1 : 0;
}

u32 Ichor_ModifyEggChance(u32 chance)
{
    return Ichor_IsBlessed(ICHOR_GOD_HERA) ? min(chance * 2, 100) : chance;
}

// Aphrodite: friendship gains x2. The Myrtle Wreath: its holder's never drops.
s32 Ichor_ModifyFriendshipDelta(struct Pokemon *mon, s32 delta)
{
    if (delta > 0 && Ichor_IsBlessed(ICHOR_GOD_APHRODITE))
        return delta * 2;
    if (delta < 0 && GetMonData(mon, MON_DATA_HELD_ITEM) == ITEM_MYRTLE_WREATH)
        return 0;
    return delta;
}

// Demeter's blessing, or her Harvest Basket: berry trees give one more.
u32 Ichor_ExtraBerryYield(void)
{
    return (Ichor_IsBlessed(ICHOR_GOD_DEMETER) || FlagGet(FLAG_ICHOR_HARVEST_BASKET)) ? 1 : 0;
}

// Artemis: the Augur's Eye lets you creep 2 tiles closer.
u32 Ichor_DexNavSneakBonus(void)
{
    return Ichor_IsBlessed(ICHOR_GOD_ARTEMIS) ? 2 : 0;
}

// Athena: the Augur's Eye finds hidden Pokémon twice as often.
u32 Ichor_DexNavHiddenRate(u32 rate)
{
    return Ichor_IsBlessed(ICHOR_GOD_ATHENA) ? min(rate * 2, 100) : rate;
}
