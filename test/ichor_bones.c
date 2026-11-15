// Ichor: knucklebones (design/SYSTEMS.md §9, design/ENGINE_API.md §7): the
// named throws, each opponent's play, Mom's record and her bee, and Silenos.
#include "global.h"
#include "event_data.h"
#include "ichor_bones.h"
#include "ichor_save.h"
#include "random.h"
#include "string_util.h"
#include "test/test.h"
#include "constants/characters.h"
#include "constants/ichor.h"

void Ichor_BonesStart(void);
void Ichor_BonesPlayerThrow(void);
void Ichor_BonesToggle(void);
void Ichor_BonesRethrow(void);
u16 Ichor_BonesOpponentThrow(void);
u16 Ichor_BonesScore(void);
u16 Ichor_BonesCallLoaded(void);
u16 Ichor_BonesMatchOver(void);

// faces as indices: 0 is a 1, 1 a 3, 2 a 4, 3 a 6
#define ONE 0
#define THREE 1
#define FOUR 2
#define SIX 3

TEST("Ichor: Aphrodite beats everything, the Dog loses to everything, else the higher sum")
{
    static const u8 aphrodite[] = {ONE, THREE, FOUR, SIX};
    static const u8 sixes[] = {SIX, SIX, SIX, SIX};
    static const u8 dog[] = {ONE, ONE, ONE, ONE};
    static const u8 low[] = {ONE, ONE, ONE, THREE};
    static const u8 seventeen[] = {THREE, FOUR, FOUR, SIX};
    static const u8 seventeen2[] = {SIX, FOUR, THREE, FOUR};
    EXPECT_EQ(Ichor_BonesTestCompare(aphrodite, sixes), ICHOR_BONES_YOURS);
    EXPECT_EQ(Ichor_BonesTestCompare(sixes, aphrodite), ICHOR_BONES_THEIRS);
    EXPECT_EQ(Ichor_BonesTestCompare(aphrodite, aphrodite), ICHOR_BONES_TIE);
    EXPECT_EQ(Ichor_BonesTestCompare(low, dog), ICHOR_BONES_YOURS);
    EXPECT_EQ(Ichor_BonesTestCompare(dog, low), ICHOR_BONES_THEIRS);
    EXPECT_EQ(Ichor_BonesTestCompare(sixes, seventeen), ICHOR_BONES_YOURS);
    EXPECT_EQ(Ichor_BonesTestCompare(seventeen, seventeen2), ICHOR_BONES_TIE);
}

TEST("Ichor: each opponent rethrows as their personality plays")
{
    static const u8 ones[] = {ONE, SIX, THREE, ONE};
    static const u8 threeSides[] = {ONE, THREE, THREE, SIX};
    static const u8 twoSides[] = {THREE, THREE, FOUR, FOUR};
    static const u8 aphrodite[] = {SIX, ONE, FOUR, THREE};
    static const u8 mixed[] = {ONE, THREE, FOUR, SIX};
    static const u8 fours[] = {FOUR, THREE, FOUR, SIX};
    static const u8 lowMom[] = {THREE, THREE, FOUR, ONE};

    EXPECT_EQ(Ichor_BonesTestMarks(ICHOR_BONES_CAUTIOUS, ones), (1 << 0) | (1 << 3));
    // Bold holds three different sides: it rethrows one of the pair for the fourth
    EXPECT(Ichor_BonesTestMarks(ICHOR_BONES_BOLD, threeSides) == (1 << 1)
        || Ichor_BonesTestMarks(ICHOR_BONES_BOLD, threeSides) == (1 << 2));
    EXPECT_EQ(Ichor_BonesTestMarks(ICHOR_BONES_BOLD, twoSides), 0);
    // nobody breaks up an Aphrodite
    EXPECT_EQ(Ichor_BonesTestMarks(ICHOR_BONES_CAUTIOUS, aphrodite), 0);
    EXPECT_EQ(Ichor_BonesTestMarks(ICHOR_BONES_MOM, mixed), 0);
    // Silenos, and Mom once she plays fair, rethrow anything under a fresh bone's worth
    FlagSet(FLAG_ICHOR_MOM_CONFESSED);
    EXPECT_EQ(Ichor_BonesTestMarks(ICHOR_BONES_SILENOS, fours), (1 << 1));
    EXPECT_EQ(Ichor_BonesTestMarks(ICHOR_BONES_MOM, fours), (1 << 1));
    // with the bee, Mom keeps her 3s once her total reaches 16
    FlagClear(FLAG_ICHOR_MOM_CONFESSED);
    EXPECT_EQ(Ichor_BonesTestMarks(ICHOR_BONES_MOM, fours), 0);
    EXPECT_EQ(Ichor_BonesTestMarks(ICHOR_BONES_MOM, lowMom), (1 << 0) | (1 << 1) | (1 << 3));
}

// A whole match as the script plays it, the player rethrowing 1s and 3s.
static u32 PlayMatch(u32 opponent)
{
    u32 winner;
    gSpecialVar_0x8004 = opponent;
    Ichor_BonesStart();
    do
    {
        Ichor_BonesPlayerThrow();
        // rethrow the 1s and 3s: the face index is in the buffered text, so
        // read it back through the toggles' effect on a fresh throw
        for (gSpecialVar_0x8004 = 0; gSpecialVar_0x8004 < 4; gSpecialVar_0x8004++)
        {
            u8 face = gStringVar1[gSpecialVar_0x8004 * 3] - CHAR_0;
            if (face == 1 || face == 3)
                Ichor_BonesToggle();
        }
        Ichor_BonesRethrow();
        Ichor_BonesOpponentThrow();
        Ichor_BonesScore();
        winner = Ichor_BonesMatchOver();
    } while (winner == 0);
    return winner;
}

TEST("Ichor: Mom with her bee wins almost every match; fair, about half")
{
    u32 i, wins = 0, w0 = gIchorSave.momWins, l0 = gIchorSave.momLosses;
    SeedRng(0x5EED);
    FlagClear(FLAG_ICHOR_MOM_CONFESSED);
    for (i = 0; i < 1000; i++)
        wins += PlayMatch(ICHOR_BONES_MOM) == ICHOR_BONES_YOURS;
    EXPECT_GT(wins, 25);    // SYSTEMS §9: about 5.5%
    EXPECT_LT(wins, 95);
    EXPECT_EQ(gIchorSave.momWins, w0 + wins);  // every match goes on her record
    EXPECT_EQ(gIchorSave.momLosses, l0 + 1000 - wins);

    FlagSet(FLAG_ICHOR_MOM_CONFESSED);
    wins = 0;
    for (i = 0; i < 1000; i++)
        wins += PlayMatch(ICHOR_BONES_MOM) == ICHOR_BONES_YOURS;
    EXPECT_GT(wins, 380);   // about half
    EXPECT_LT(wins, 620);
    FlagClear(FLAG_ICHOR_MOM_CONFESSED);
    gIchorSave.momWins = w0;
    gIchorSave.momLosses = l0;
}

TEST("Ichor: calling Silenos's bones loaded wins only after two throws of two 6s running")
{
    u32 throws;
    SeedRng(0xB0E5);
    gSpecialVar_0x8004 = ICHOR_BONES_SILENOS;
    Ichor_BonesStart();
    EXPECT_EQ(Ichor_BonesCallLoaded(), FALSE);
    for (throws = 0; throws < 500; throws++)
    {
        u32 sixes = 0, i;
        Ichor_BonesOpponentThrow();
        for (i = 0; i < 4; i++)
            sixes += gStringVar2[i * 3] == CHAR_6;
        if (sixes < 2)
        {
            EXPECT_EQ(Ichor_BonesCallLoaded(), FALSE);
            continue;
        }
        Ichor_BonesOpponentThrow();
        sixes = 0;
        for (i = 0; i < 4; i++)
            sixes += gStringVar2[i * 3] == CHAR_6;
        if (sixes >= 2)
            break;
    }
    EXPECT_LT(throws, 500);
    EXPECT_EQ(Ichor_BonesCallLoaded(), TRUE);
    EXPECT_EQ(Ichor_BonesMatchOver(), ICHOR_BONES_YOURS);
}
