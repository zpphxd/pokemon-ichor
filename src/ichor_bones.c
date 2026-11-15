// Ichor: knucklebones (design/SYSTEMS.md §9, design/ENGINE_API.md §7).
//
// Four bones, each landing 1, 3, 4 or 6. Throw all four, rethrow any of them
// once, and the higher sum wins; Aphrodite (all four sides different) beats
// everything and the Dog (four 1s) loses to everything. A tie is thrown again.
// A match is best of five. data/scripts/ichor_bones.pory runs the match; these
// specials hold its state and play the opponent.

#include "global.h"
#include "event_data.h"
#include "item.h"
#include "list_menu.h"
#include "malloc.h"
#include "random.h"
#include "script_menu.h"
#include "string_util.h"
#include "ichor_bones.h"
#include "ichor_save.h"
#include "constants/flags.h"
#include "constants/ichor.h"
#include "constants/items.h"

#define BONES          4
#define FACES          4
#define WINS_NEEDED    3   // best of five
#define NO_FACE        0xFF

static const u8 sFaceValue[FACES] = {1, 3, 4, 6};

// Percent per face (1, 3, 4, 6)
static const u8 sFairOdds[FACES]    = {10, 40, 40, 10};
static const u8 sMomOdds[FACES]     = {5, 30, 30, 35};   // the bee hums the throws
static const u8 sSilenosOdds[FACES] = {8, 31, 31, 30};   // loaded: a 6 three times in ten

static EWRAM_DATA struct
{
    u8 you[BONES];          // face indices
    u8 them[BONES];
    u8 marked;              // bones you've marked to rethrow, a bit each
    u8 rethrows;            // left this throw
    u8 bonusRethrows;       // left this match (the Aphrodite Bone)
    u8 opponent;            // ICHOR_BONES_*
    u8 yourWins;
    u8 theirWins;
    u8 sixesRunning;        // Silenos's throws in a row with two or more 6s
    bool8 calledLoaded;
    bool8 recorded;         // the match is on Mom's record
} sBones = {0};

static bool32 MomCheats(void)
{
    return sBones.opponent == ICHOR_BONES_MOM && !FlagGet(FLAG_ICHOR_MOM_CONFESSED);
}

static const u8 *OddsFor(bool32 opponent)
{
    if (!opponent)
        return sFairOdds;
    if (MomCheats())
        return sMomOdds;
    if (sBones.opponent == ICHOR_BONES_SILENOS)
        return sSilenosOdds;
    return sFairOdds;
}

static u8 RollFace(const u8 *odds)
{
    u32 i, roll = Random() % 100;
    for (i = 0; i < FACES - 1; i++)
    {
        if (roll < odds[i])
            return i;
        roll -= odds[i];
    }
    return FACES - 1;
}

static u32 Sum(const u8 *bones)
{
    u32 i, sum = 0;
    for (i = 0; i < BONES; i++)
        sum += sFaceValue[bones[i]];
    return sum;
}

static bool32 IsAphrodite(const u8 *bones)
{
    u32 i, seen = 0;
    for (i = 0; i < BONES; i++)
        seen |= 1 << bones[i];
    return seen == (1 << FACES) - 1;
}

static bool32 IsDog(const u8 *bones)
{
    u32 i;
    for (i = 0; i < BONES; i++)
    {
        if (bones[i] != 0)
            return FALSE;
    }
    return TRUE;
}

static u32 CountFace(const u8 *bones, u32 face)
{
    u32 i, n = 0;
    for (i = 0; i < BONES; i++)
        n += (bones[i] == face);
    return n;
}

// "3  4  4  6  (17)", "1  3  4  6: Aphrodite!" or "1  1  1  1: the Dog!"
static void BufferBones(u8 *dst, const u8 *bones)
{
    u32 i;
    u8 *end = dst;
    for (i = 0; i < BONES; i++)
    {
        end = ConvertIntToDecimalStringN(end, sFaceValue[bones[i]], STR_CONV_MODE_LEFT_ALIGN, 1);
        if (i < BONES - 1)
            end = StringCopy(end, COMPOUND_STRING("  "));
    }
    if (IsAphrodite(bones))
    {
        StringCopy(end, COMPOUND_STRING(": Aphrodite!"));
    }
    else if (IsDog(bones))
    {
        StringCopy(end, COMPOUND_STRING(": the Dog!"));
    }
    else
    {
        end = StringCopy(end, COMPOUND_STRING("  ("));
        end = ConvertIntToDecimalStringN(end, Sum(bones), STR_CONV_MODE_LEFT_ALIGN, 2);
        StringCopy(end, COMPOUND_STRING(")"));
    }
}

static void Throw(u8 *bones, u32 mask, const u8 *odds)
{
    u32 i;
    for (i = 0; i < BONES; i++)
    {
        if (mask & (1 << i))
            bones[i] = RollFace(odds);
    }
}

// --- The opponent's play ------------------------------------------------------------

// Which bones the opponent rethrows, by personality. Nobody breaks up an Aphrodite.
static u32 OpponentMarks(const u8 *bones)
{
    u32 i, mask = 0, distinct = 0, face;

    if (IsAphrodite(bones))
        return 0;
    for (face = 0; face < FACES; face++)
        distinct += CountFace(bones, face) != 0;

    switch (sBones.opponent)
    {
    case ICHOR_BONES_BOLD:
        if (distinct == FACES - 1)
        {
            // three different sides: keep one of each, rethrow the spare for the fourth
            for (i = 0; i < BONES; i++)
            {
                if (CountFace(bones, bones[i]) == 2)
                    return 1 << i;
            }
        }
        // fall through: otherwise it plays safe
    case ICHOR_BONES_CAUTIOUS:
    default:
        for (i = 0; i < BONES; i++)
        {
            if (bones[i] == 0)
                mask |= 1 << i;
        }
        return mask;
    case ICHOR_BONES_SILENOS:
    case ICHOR_BONES_MOM:
        // Sensible play: rethrow the 1s and 3s. With the bee, Mom keeps her 3s
        // once her total reaches 16. With her two rethrows that wins her all but
        // about 1 match in 18, SYSTEMS §9's 5.5% (test/ichor_bones.c).
        for (i = 0; i < BONES; i++)
        {
            if (bones[i] == 0 || (bones[i] == 1 && !(MomCheats() && Sum(bones) >= 16)))
                mask |= 1 << i;
        }
        return mask;
    }
}

// --- Specials -------------------------------------------------------------------------

// special Ichor_BonesStart: a new match against ICHOR_BONES_* VAR_0x8004.
void Ichor_BonesStart(void)
{
    memset(&sBones, 0, sizeof(sBones));
    sBones.opponent = gSpecialVar_0x8004 < ICHOR_BONES_COUNT ? gSpecialVar_0x8004 : ICHOR_BONES_CAUTIOUS;
    sBones.bonusRethrows = CheckBagHasItem(ITEM_APHRODITE_BONE, 1) ? 1 : 0;
}

// special Ichor_BonesPlayerThrow: you throw all four. Your bones in STR_VAR_1.
void Ichor_BonesPlayerThrow(void)
{
    Throw(sBones.you, (1 << BONES) - 1, OddsFor(FALSE));
    sBones.marked = 0;
    sBones.rethrows = 1;
    BufferBones(gStringVar1, sBones.you);
}

static void PushChoice(const u8 *text, u16 id)
{
    struct ListMenuItem item;
    u8 *name = Alloc(24);  // freed by the menu
    StringCopy(name, text);
    item.name = name;
    item.id = id;
    MultichoiceDynamic_PushElement(item);
}

static u32 RethrowsLeft(void)
{
    return sBones.rethrows + sBones.bonusRethrows;
}

// special Ichor_BonesBuildMenu: one line per bone (KEEP or ROLL, A to switch),
// ROLL THEM once a bone is marked and a rethrow is left, STAND, and LOADED!
// against Silenos after two throws in a row with two 6s each.
void Ichor_BonesBuildMenu(void)
{
    u32 i;
    u8 line[16], *end;

    for (i = 0; i < BONES && RethrowsLeft() != 0; i++)
    {
        end = ConvertIntToDecimalStringN(line, sFaceValue[sBones.you[i]], STR_CONV_MODE_LEFT_ALIGN, 1);
        StringCopy(end, (sBones.marked & (1 << i)) ? COMPOUND_STRING("  ROLL") : COMPOUND_STRING("  KEEP"));
        PushChoice(line, i);
    }
    if (sBones.marked != 0 && RethrowsLeft() != 0)
        PushChoice(COMPOUND_STRING("ROLL THEM"), ICHOR_BONES_MENU_ROLL);
    PushChoice(COMPOUND_STRING("STAND"), ICHOR_BONES_MENU_STAND);
    if (sBones.opponent == ICHOR_BONES_SILENOS && sBones.sixesRunning >= 2)
        PushChoice(COMPOUND_STRING("LOADED!"), ICHOR_BONES_MENU_LOADED);
}

// special Ichor_BonesToggle: bone VAR_0x8004 switches between KEEP and ROLL.
void Ichor_BonesToggle(void)
{
    if (gSpecialVar_0x8004 < BONES)
        sBones.marked ^= 1 << gSpecialVar_0x8004;
}

// special Ichor_BonesRethrow: the marked bones are thrown again, using this
// throw's rethrow, or else the Aphrodite Bone's. Your bones in STR_VAR_1.
void Ichor_BonesRethrow(void)
{
    if (sBones.marked == 0 || RethrowsLeft() == 0)
        return;
    Throw(sBones.you, sBones.marked, OddsFor(FALSE));
    if (sBones.rethrows != 0)
        sBones.rethrows--;
    else
        sBones.bonusRethrows--;
    sBones.marked = 0;
    BufferBones(gStringVar1, sBones.you);
}

// specialvar Ichor_BonesOpponentThrow: the opponent throws and rethrows as they
// play. Their bones in STR_VAR_2; TRUE if they rethrew any.
u16 Ichor_BonesOpponentThrow(void)
{
    u32 tries, mask, rethrew = FALSE;

    Throw(sBones.them, (1 << BONES) - 1, OddsFor(TRUE));
    for (tries = MomCheats() ? 2 : 1; tries != 0; tries--)
    {
        mask = OpponentMarks(sBones.them);
        if (mask == 0)
            break;
        Throw(sBones.them, mask, OddsFor(TRUE));
        rethrew = TRUE;
    }
    if (sBones.opponent == ICHOR_BONES_SILENOS)
        sBones.sixesRunning = CountFace(sBones.them, FACES - 1) >= 2 ? sBones.sixesRunning + 1 : 0;
    BufferBones(gStringVar2, sBones.them);
    return rethrew;
}

static u32 Compare(const u8 *you, const u8 *them)
{
    if (IsAphrodite(you) != IsAphrodite(them))
        return IsAphrodite(you) ? ICHOR_BONES_YOURS : ICHOR_BONES_THEIRS;
    if (IsDog(you) != IsDog(them))
        return IsDog(them) ? ICHOR_BONES_YOURS : ICHOR_BONES_THEIRS;
    if (Sum(you) != Sum(them))
        return Sum(you) > Sum(them) ? ICHOR_BONES_YOURS : ICHOR_BONES_THEIRS;
    return ICHOR_BONES_TIE;
}

// specialvar Ichor_BonesScore: who took the throw (ICHOR_BONES_TIE, _YOURS or
// _THEIRS). The match score, yours first, in STR_VAR_1 ("2-1").
u16 Ichor_BonesScore(void)
{
    u32 result = Compare(sBones.you, sBones.them);
    u8 *end;

    if (result == ICHOR_BONES_YOURS)
        sBones.yourWins++;
    else if (result == ICHOR_BONES_THEIRS)
        sBones.theirWins++;
    end = ConvertIntToDecimalStringN(gStringVar1, sBones.yourWins, STR_CONV_MODE_LEFT_ALIGN, 1);
    end = StringCopy(end, COMPOUND_STRING("-"));
    ConvertIntToDecimalStringN(end, sBones.theirWins, STR_CONV_MODE_LEFT_ALIGN, 1);
    return result;
}

// specialvar Ichor_BonesCallLoaded: you call Silenos's bones loaded. TRUE if
// he has thrown two 6s or more twice running: the match is yours.
u16 Ichor_BonesCallLoaded(void)
{
    if (sBones.opponent != ICHOR_BONES_SILENOS || sBones.sixesRunning < 2)
        return FALSE;
    sBones.calledLoaded = TRUE;
    sBones.yourWins = WINS_NEEDED;
    return TRUE;
}

// specialvar Ichor_BonesMatchOver: 0 while the match goes on, else
// ICHOR_BONES_YOURS or _THEIRS. A match against Mom goes on her record, once.
u16 Ichor_BonesMatchOver(void)
{
    u32 winner;

    if (sBones.yourWins >= WINS_NEEDED)
        winner = ICHOR_BONES_YOURS;
    else if (sBones.theirWins >= WINS_NEEDED)
        winner = ICHOR_BONES_THEIRS;
    else
        return 0;
    if (sBones.opponent == ICHOR_BONES_MOM && !sBones.recorded)
    {
        sBones.recorded = TRUE;
        if (winner == ICHOR_BONES_YOURS && gIchorSave.momWins < 9999)
            gIchorSave.momWins++;
        else if (winner == ICHOR_BONES_THEIRS && gIchorSave.momLosses < 9999)
            gIchorSave.momLosses++;
    }
    return winner;
}

// specialvar Ichor_GetMomRecord: your wins against Mom, with her wins (your
// losses) in VAR_0x8004. For the 2F text: "Record against Mom: ..."
u16 Ichor_GetMomRecord(void)
{
    gSpecialVar_0x8004 = gIchorSave.momLosses;
    return gIchorSave.momWins;
}

// --- For the C tests ------------------------------------------------------------------

u32 Ichor_BonesTestCompare(const u8 *you, const u8 *them)
{
    return Compare(you, them);
}

u32 Ichor_BonesTestMarks(u32 opponent, const u8 *bones)
{
    sBones.opponent = opponent;
    return OpponentMarks(bones);
}
