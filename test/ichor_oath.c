#include "global.h"
#include "battle.h"
#include "battle_scripts.h"
#include "battle_util.h"
#include "battle_script_commands.h"
#include "chooseboxmon.h"
#include "event_data.h"
#include "ichor_oath.h"
#include "ichor_save.h"
#include "pokemon.h"
#include "pokemon_storage_system.h"
#include "item.h"
#include "safari_zone.h"
#include "string_util.h"
#include "test/battle.h"
#include "constants/battle.h"
#include "constants/items.h"
#include "constants/region_map_sections.h"

static void ResetOath(void)
{
    Ichor_InitSave();
    ResetPokemonStorageSystem();
    FlagClear(FLAG_ICHOR_GOT_STARTER);
}

TEST("Ichor: the Oath is an independent once-only pre-partner choice")
{
    ResetOath();
    EXPECT(!Ichor_IsOathActive());
    EXPECT(!Ichor_ChooseOath(2));
    EXPECT_EQ(gIchorSave.oath.state, ICHOR_OATH_UNDECIDED);
    EXPECT(Ichor_ChooseOath(TRUE));
    EXPECT(Ichor_IsOathActive());
    EXPECT(!Ichor_ChooseOath(FALSE));
    EXPECT(Ichor_IsOathActive());
    ResetOath();
    EXPECT(Ichor_ChooseOath(FALSE));
    EXPECT_EQ(gIchorSave.oath.state, ICHOR_OATH_DECLINED);
    EXPECT(!Ichor_ChooseOath(TRUE));
    ResetOath();
    FlagSet(FLAG_ICHOR_GOT_STARTER);
    EXPECT(!Ichor_ChooseOath(TRUE));
    EXPECT(!Ichor_IsOathActive());
}

TEST("Ichor: an Oath shares one chance across a named area's maps")
{
    ResetOath();
    EXPECT(Ichor_ChooseOath(TRUE));
    EXPECT(Ichor_ClaimOathEncounter(MAPSEC_KALLISTE_ROUTE_1));
    EXPECT(!Ichor_ClaimOathEncounter(MAPSEC_KALLISTE_ROUTE_1));
    EXPECT(Ichor_ClaimOathEncounter(MAPSEC_HECATES_HOLLOW));
    EXPECT_EQ(Ichor_CountOathEncounters(), 2);
    EXPECT(!Ichor_HasOathEncounter(MAPSEC_ELAIA_VILLAGE));
    Ichor_OnSaveLoaded();
    EXPECT(!Ichor_ClaimOathEncounter(MAPSEC_KALLISTE_ROUTE_1));
    EXPECT_EQ(Ichor_CountOathEncounters(), 2);
}

TEST("Ichor: Oath encounter bits are bounded and cannot alias adjacent areas")
{
    u32 section;
    ResetOath();
    EXPECT(Ichor_ChooseOath(TRUE));
    EXPECT(!Ichor_ClaimOathEncounter(MAPSEC_NONE));
    EXPECT(!Ichor_ClaimOathEncounter(MAPSEC_COUNT));
    EXPECT(!Ichor_ClaimOathEncounter(0xFFFFFFFF));
    EXPECT(!Ichor_ClaimOathEncounter(MAPSEC_DYNAMIC));
    EXPECT(!Ichor_ClaimOathEncounter(MAPSEC_SECRET_BASE));
    EXPECT_EQ(Ichor_CountOathEncounters(), 0);
    for (section = 0; section < MAPSEC_NONE; section++)
    {
        if (section == MAPSEC_DYNAMIC || section == MAPSEC_SECRET_BASE)
            continue;
        EXPECT(!Ichor_HasOathEncounter(section));
        EXPECT(Ichor_ClaimOathEncounter(section));
        EXPECT(Ichor_HasOathEncounter(section));
        EXPECT(!Ichor_ClaimOathEncounter(section));
    }
    EXPECT_EQ(Ichor_CountOathEncounters(), MAPSEC_NONE - 2);
}

TEST("Ichor: absent and released Oaths do not consume ordinary encounter chances")
{
    ResetOath();
    EXPECT(Ichor_ClaimOathEncounter(MAPSEC_KALLISTE_ROUTE_1));
    EXPECT(Ichor_ClaimOathEncounter(MAPSEC_KALLISTE_ROUTE_1));
    EXPECT_EQ(Ichor_CountOathEncounters(), 0);
    EXPECT(!Ichor_ReleaseOath());
    EXPECT(!Ichor_FailOath());
    EXPECT(Ichor_ChooseOath(TRUE));
    EXPECT(Ichor_ClaimOathEncounter(MAPSEC_KALLISTE_ROUTE_1));
    EXPECT(Ichor_ReleaseOath());
    EXPECT_EQ(gIchorSave.oath.state, ICHOR_OATH_RELEASED);
    EXPECT(!Ichor_ReleaseOath());
    EXPECT(!Ichor_FailOath());
    EXPECT(!Ichor_ChooseOath(TRUE));
    EXPECT(Ichor_ClaimOathEncounter(MAPSEC_KALLISTE_ROUTE_1));
    EXPECT(Ichor_HasOathEncounter(MAPSEC_KALLISTE_ROUTE_1));
    EXPECT(Ichor_ClaimOathEncounter(MAPSEC_HECATES_HOLLOW));
    EXPECT_EQ(Ichor_CountOathEncounters(), 1);
}

TEST("Ichor: a failed Oath retains its receipts and cannot be sworn again")
{
    ResetOath();
    EXPECT(Ichor_ChooseOath(TRUE));
    EXPECT(Ichor_ClaimOathEncounter(MAPSEC_AKTI_TOWN));
    gIchorSave.oath.fallenCount = 3;
    EXPECT(Ichor_FailOath());
    EXPECT_EQ(gIchorSave.oath.state, ICHOR_OATH_FAILED);
    EXPECT(!Ichor_IsOathActive());
    EXPECT(!Ichor_FailOath());
    EXPECT(!Ichor_ChooseOath(TRUE));
    EXPECT_EQ(Ichor_CountOathEncounters(), 1);
    EXPECT_EQ(gIchorSave.oath.fallenCount, 3);
}

TEST("Ichor: version 4 migrates Oath bytes without changing existing progress")
{
    u32 i;
    gIchorSave.version = 4;
    gIchorSave.momWins = 27;
    gIchorSave.favor[1] = 83;
    gIchorSave.vars[0] = 2;
    gIchorSave.flags[0] = 0xA5;
    gIchorSave.flags2[0] = 0x5A;
    gIchorSave.thread.anchorCount = 4;
    memset(&gIchorSave.oath, 0xFF, sizeof(gIchorSave.oath));
    Ichor_OnSaveLoaded();
    EXPECT_EQ(gIchorSave.version, ICHOR_SAVE_VERSION);
    EXPECT_EQ(gIchorSave.oath.state, ICHOR_OATH_UNDECIDED);
    EXPECT_EQ(gIchorSave.oath.fallenCount, 0);
    for (i = 0; i < sizeof(gIchorSave.oath.encounters); i++)
        EXPECT_EQ(gIchorSave.oath.encounters[i], 0);
    EXPECT_EQ(gIchorSave.momWins, 27);
    EXPECT_EQ(gIchorSave.favor[1], 83);
    EXPECT_EQ(gIchorSave.vars[0], 2);
    EXPECT_EQ(gIchorSave.flags[0], 0xA5);
    EXPECT_EQ(gIchorSave.flags2[0], 0x5A);
    EXPECT_EQ(gIchorSave.thread.anchorCount, 4);
}

static void CreateOathMon(struct Pokemon *mon)
{
    CreateRandomMon(mon, SPECIES_NEBREL, 5);
}

TEST("Ichor: swearing reserves an empty Urn without overwriting stored Pokemon")
{
    struct Pokemon mon;
    u8 oldName[BOX_NAME_LENGTH + 1];
    ResetOath();
    StringCopy(oldName, GetBoxNamePtr(TOTAL_BOXES_COUNT - 1));
    CreateOathMon(&mon);
    SetBoxMonAt(TOTAL_BOXES_COUNT - 1, 0, &mon.box);
    EXPECT(!Ichor_ChooseOath(TRUE));
    EXPECT(!Ichor_IsUrnBox(TOTAL_BOXES_COUNT - 1));
    EXPECT_EQ(GetBoxMonDataAt(TOTAL_BOXES_COUNT - 1, 0, MON_DATA_SPECIES), SPECIES_NEBREL);
    EXPECT_EQ(StringCompare(oldName, GetBoxNamePtr(TOTAL_BOXES_COUNT - 1)), 0);
    EXPECT(Ichor_ChooseOath(FALSE));
    ResetOath();
    EXPECT(Ichor_ChooseOath(TRUE));
    EXPECT_EQ(StringCompare(GetBoxNamePtr(TOTAL_BOXES_COUNT - 1), COMPOUND_STRING("URN")), 0);
    EXPECT(Ichor_IsUrnBox(TOTAL_BOXES_COUNT - 1));
    EXPECT(!Ichor_IsUrnBox(TOTAL_BOXES_COUNT - 2));
    EXPECT(!Ichor_IsUrnBox(TOTAL_BOXES_COUNT));
}

TEST("Ichor: only actual non-Egg fainting under the Oath records a fall")
{
    struct Pokemon mon;
    u32 zero = 0, egg = TRUE;
    ResetOath();
    CreateOathMon(&mon);
    EXPECT(!Ichor_RecordOathFallen(&mon));
    EXPECT(Ichor_ChooseOath(TRUE));
    EXPECT(!Ichor_RecordOathFallen(&mon));
    SetMonData(&mon, MON_DATA_IS_EGG, &egg);
    SetMonData(&mon, MON_DATA_HP, &zero);
    EXPECT(!Ichor_RecordOathFallen(&mon));
    SetMonData(&mon, MON_DATA_IS_EGG, &zero);
    EXPECT(Ichor_RecordOathFallen(&mon));
    EXPECT(Ichor_IsOathFallen(&mon.box));
    EXPECT_EQ(gIchorSave.oath.fallenCount, 1);
    EXPECT(!Ichor_RecordOathFallen(&mon));
    EXPECT_EQ(gIchorSave.oath.fallenCount, 1);
    ZeroMonData(&mon);
    EXPECT(!Ichor_RecordOathFallen(&mon));
}

TEST("Ichor: legacy Pokemon's formerly unused bit is ignored outside an Oath")
{
    struct Pokemon mon;
    ResetOath();
    CreateOathMon(&mon);
    mon.box.oathFallen = TRUE;
    EXPECT(!Ichor_IsOathFallen(&mon.box));
    FlagSet(FLAG_ICHOR_GOT_STARTER);
    EXPECT(!Ichor_ChooseOath(TRUE));
    EXPECT(!Ichor_IsOathFallen(&mon.box));
}

TEST("Ichor: the Urn retains the entire fallen Pokemon before clearing its source")
{
    struct Pokemon mon;
    struct BoxPokemon snapshot;
    const u8 nickname[POKEMON_NAME_LENGTH + 1] = _("CLOUD");
    u32 zero = 0, location = MAPSEC_KALLISTE_ROUTE_1;
    ResetOath();
    EXPECT(Ichor_ChooseOath(TRUE));
    CreateOathMon(&mon);
    EXPECT_EQ(Ichor_StoreOathFallen(&mon), ICHOR_URN_NOT_FALLEN);
    SetMonData(&mon, MON_DATA_NICKNAME, nickname);
    SetMonData(&mon, MON_DATA_MET_LOCATION, &location);
    SetMonData(&mon, MON_DATA_HP, &zero);
    EXPECT(Ichor_RecordOathFallen(&mon));
    snapshot = mon.box;
    EXPECT_EQ(Ichor_StoreOathFallen(&mon), ICHOR_URN_STORED);
    EXPECT_EQ(memcmp(GetBoxedMonPtr(TOTAL_BOXES_COUNT - 1, 0), &snapshot, sizeof(snapshot)), 0);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_SPECIES), SPECIES_NONE);
    EXPECT_EQ(gIchorSave.oath.fallenCount, 1);
    EXPECT_EQ(Ichor_StoreOathFallen(&mon), ICHOR_URN_NOT_FALLEN);
}

TEST("Ichor: a full Urn preserves its contents and leaves the fallen source intact")
{
    struct Pokemon mon, living;
    struct BoxPokemon snapshot;
    u32 i, box, zero = 0;
    ResetOath();
    EXPECT(Ichor_ChooseOath(TRUE));
    for (i = 0; i < IN_BOX_COUNT; i++)
    {
        CreateOathMon(&mon);
        SetMonData(&mon, MON_DATA_HP, &zero);
        EXPECT(Ichor_RecordOathFallen(&mon));
        EXPECT_EQ(Ichor_StoreOathFallen(&mon), ICHOR_URN_STORED);
    }
    CreateOathMon(&living);
    for (box = 0; box < TOTAL_BOXES_COUNT - 1; box++)
        for (i = 0; i < IN_BOX_COUNT; i++)
            SetBoxMonAt(box, i, &living.box);
    CreateOathMon(&mon);
    SetMonData(&mon, MON_DATA_HP, &zero);
    EXPECT(Ichor_RecordOathFallen(&mon));
    snapshot = mon.box;
    EXPECT_EQ(Ichor_StoreOathFallen(&mon), ICHOR_URN_FULL);
    EXPECT_EQ(memcmp(&mon.box, &snapshot, sizeof(snapshot)), 0);
    EXPECT_EQ(CountMonsInBox(TOTAL_BOXES_COUNT - 1), IN_BOX_COUNT);
    EXPECT_EQ(gIchorSave.oath.fallenCount, IN_BOX_COUNT + 1);
    for (i = 0; i < IN_BOX_COUNT; i++)
        EXPECT(Ichor_IsOathFallen(GetBoxedMonPtr(TOTAL_BOXES_COUNT - 1, i)));
}

TEST("Ichor: a growing Urn reserves only empty jars and preserves living Pokemon")
{
    struct Pokemon mon, living;
    u32 i, zero = 0;
    ResetOath();
    EXPECT(Ichor_ChooseOath(TRUE));
    CreateOathMon(&living);
    SetBoxMonAt(TOTAL_BOXES_COUNT - 2, 0, &living.box);
    for (i = 0; i < IN_BOX_COUNT + 1; i++)
    {
        CreateOathMon(&mon);
        SetMonData(&mon, MON_DATA_HP, &zero);
        EXPECT(Ichor_RecordOathFallen(&mon));
        EXPECT_EQ(Ichor_StoreOathFallen(&mon), ICHOR_URN_STORED);
    }
    EXPECT_EQ(CountMonsInBox(TOTAL_BOXES_COUNT - 1), IN_BOX_COUNT);
    EXPECT_EQ(CountMonsInBox(TOTAL_BOXES_COUNT - 3), 1);
    EXPECT(Ichor_IsUrnBox(TOTAL_BOXES_COUNT - 3));
    EXPECT(!Ichor_IsUrnBox(TOTAL_BOXES_COUNT - 2));
    EXPECT_EQ(StringCompare(GetBoxNamePtr(TOTAL_BOXES_COUNT - 3), COMPOUND_STRING("URN 2")), 0);
    EXPECT_EQ(memcmp(GetBoxedMonPtr(TOTAL_BOXES_COUNT - 2, 0), &living.box, sizeof(living.box)), 0);
    EXPECT(Ichor_ReleaseOath());
    EXPECT(Ichor_IsUrnBox(TOTAL_BOXES_COUNT - 3));
}

TEST("Ichor: releasing the Oath keeps its Urn and already fallen records")
{
    struct Pokemon mon;
    u32 zero = 0;
    ResetOath();
    EXPECT(Ichor_ChooseOath(TRUE));
    CreateOathMon(&mon);
    SetMonData(&mon, MON_DATA_HP, &zero);
    EXPECT(Ichor_RecordOathFallen(&mon));
    EXPECT(Ichor_ReleaseOath());
    EXPECT(Ichor_IsUrnBox(TOTAL_BOXES_COUNT - 1));
    EXPECT_EQ(Ichor_StoreOathFallen(&mon), ICHOR_URN_STORED);
    CreateOathMon(&mon);
    SetMonData(&mon, MON_DATA_HP, &zero);
    EXPECT(!Ichor_RecordOathFallen(&mon));
    EXPECT_EQ(gIchorSave.oath.fallenCount, 1);
}

TEST("Ichor: version 5 preserves Oath progress while initializing only its Urn mask")
{
    ResetOath();
    EXPECT(Ichor_ChooseOath(TRUE));
    EXPECT(Ichor_ClaimOathEncounter(MAPSEC_KALLISTE_ROUTE_1));
    gIchorSave.oath.fallenCount = 7;
    gIchorSave.version = 5;
    gIchorSave.oath.urnBoxes = 0xFFFF;
    Ichor_OnSaveLoaded();
    EXPECT_EQ(gIchorSave.version, ICHOR_SAVE_VERSION);
    EXPECT(Ichor_IsOathActive());
    EXPECT_EQ(gIchorSave.oath.fallenCount, 7);
    EXPECT_EQ(Ichor_CountOathEncounters(), 1);
    EXPECT_EQ(gIchorSave.oath.urnBoxes, 1 << (TOTAL_BOXES_COUNT - 1));
    EXPECT(Ichor_IsUrnBox(TOTAL_BOXES_COUNT - 1));
    EXPECT(!Ichor_IsUrnBox(TOTAL_BOXES_COUNT - 2));
}

TEST("Ichor: the first wild battle claims one area chance for all its ball attempts")
{
    ResetOath();
    EXPECT(Ichor_ChooseOath(TRUE));
    Ichor_BeginOathBattle(BATTLE_TYPE_IS_MASTER, MAPSEC_KALLISTE_ROUTE_1);
    EXPECT(Ichor_CanCatchOathBattle());
    EXPECT(Ichor_CanCatchOathBattle());
    EXPECT_EQ(Ichor_CountOathEncounters(), 1);
    Ichor_BeginOathBattle(BATTLE_TYPE_IS_MASTER, MAPSEC_KALLISTE_ROUTE_1);
    EXPECT(!Ichor_CanCatchOathBattle());
    EXPECT_EQ(Ichor_CountOathEncounters(), 1);
    Ichor_BeginOathBattle(BATTLE_TYPE_DOUBLE | BATTLE_TYPE_IS_MASTER, MAPSEC_ELEUSA_VILLAGE);
    EXPECT(Ichor_CanCatchOathBattle());
    EXPECT_EQ(Ichor_CountOathEncounters(), 2);
}

TEST("Ichor: trainers, tutorials, ghosts and simulated battles never spend area chances")
{
    const u32 excluded[] = {
        BATTLE_TYPE_TRAINER, BATTLE_TYPE_LINK, BATTLE_TYPE_LINK_IN_BATTLE,
        BATTLE_TYPE_TOWER_LINK_MULTI, BATTLE_TYPE_RECORDED, BATTLE_TYPE_RECORDED_LINK,
        BATTLE_TYPE_BATTLE_TOWER, BATTLE_TYPE_DOME, BATTLE_TYPE_PALACE,
        BATTLE_TYPE_ARENA, BATTLE_TYPE_FACTORY, BATTLE_TYPE_PIKE,
        BATTLE_TYPE_PYRAMID, BATTLE_TYPE_TRAINER_HILL, BATTLE_TYPE_SECRET_BASE,
        BATTLE_TYPE_CATCH_TUTORIAL, BATTLE_TYPE_POKEDUDE, BATTLE_TYPE_GHOST,
    };
    u32 i;
    ResetOath();
    EXPECT(Ichor_ChooseOath(TRUE));
    for (i = 0; i < ARRAY_COUNT(excluded); i++)
    {
        Ichor_BeginOathBattle(excluded[i] | BATTLE_TYPE_IS_MASTER, MAPSEC_KALLISTE_ROUTE_1);
        EXPECT(Ichor_CanCatchOathBattle());
        EXPECT_EQ(Ichor_CountOathEncounters(), 0);
    }
}

TEST("Ichor: ordinary and released runs retain their native capture permissions")
{
    ResetOath();
    Ichor_BeginOathBattle(0, MAPSEC_NONE);
    EXPECT(Ichor_CanCatchOathBattle());
    EXPECT_EQ(Ichor_CountOathEncounters(), 0);
    EXPECT(Ichor_ChooseOath(TRUE));
    Ichor_BeginOathBattle(0, MAPSEC_KALLISTE_ROUTE_1);
    Ichor_BeginOathBattle(0, MAPSEC_KALLISTE_ROUTE_1);
    EXPECT(!Ichor_CanCatchOathBattle());
    Ichor_BeginOathBattle(0, MAPSEC_NONE);
    EXPECT(!Ichor_CanCatchOathBattle());
    EXPECT_EQ(Ichor_CountOathEncounters(), 1);
    EXPECT(Ichor_ReleaseOath());
    EXPECT(Ichor_CanCatchOathBattle());
    Ichor_BeginOathBattle(0, MAPSEC_KALLISTE_ROUTE_1);
    EXPECT(Ichor_CanCatchOathBattle());
    EXPECT_EQ(Ichor_CountOathEncounters(), 1);
}

TEST("Ichor: native quick and Safari throws refuse repeat areas without consuming balls")
{
    u32 balls;
    ResetOath();
    EXPECT(Ichor_ChooseOath(TRUE));
    Ichor_BeginOathBattle(0, MAPSEC_KALLISTE_ROUTE_1);
    Ichor_BeginOathBattle(0, MAPSEC_KALLISTE_ROUTE_1);
    gCurrentTurnActionNumber = 0;
    gBattlerByTurnOrder[0] = B_BATTLER_0;
    gBallToDisplay = ITEM_MASTER_BALL;
    EXPECT(AddBagItem(ITEM_MASTER_BALL, 2));
    balls = CountTotalItemQuantityInBag(ITEM_MASTER_BALL);
    HandleAction_ThrowBall();
    EXPECT_EQ(CountTotalItemQuantityInBag(ITEM_MASTER_BALL), balls);
    EXPECT_EQ(gBattlescriptCurrInstr, BattleScript_IchorOathNoCatch);
    gNumSafariBalls = 17;
    HandleAction_SafariZoneBallThrow();
    EXPECT_EQ(gNumSafariBalls, 17);
    EXPECT_EQ(gBattlescriptCurrInstr, BattleScript_IchorOathNoCatch);
}

TEST("Ichor: fallen partners cannot regain HP through healing, stats, items or boxing")
{
    struct Pokemon mon, restored;
    struct BoxPokemon boxed;
    u32 value = 0;
    ResetOath();
    EXPECT(Ichor_ChooseOath(TRUE));
    CreateOathMon(&mon);
    SetMonData(&mon, MON_DATA_HP, &value);
    EXPECT(Ichor_RecordOathFallen(&mon));
    value = 50;
    SetMonData(&mon, MON_DATA_HP, &value);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_HP), 0);
    value = 0;
    SetMonData(&mon, MON_DATA_HP_LOST, &value);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_HP), 0);
    CalculateMonStats(&mon);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_HP), 0);
    HealPokemon(&mon);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_HP), 0);
    EXPECT(PokemonUseItemEffects(&mon, ITEM_REVIVE, 0, 0, FALSE));
    EXPECT(PokemonUseItemEffects(&mon, ITEM_MAX_REVIVE, 0, 0, FALSE));
    EXPECT(PokemonUseItemEffects(&mon, ITEM_REVIVAL_HERB, 0, 0, FALSE));
    boxed = mon.box;
    HealBoxPokemon(&boxed);
    BoxMonToMon(&boxed, &restored);
    EXPECT_EQ(GetMonData(&restored, MON_DATA_HP), 0);
    EXPECT(Ichor_IsOathFallen(&restored.box));
    EXPECT(Ichor_ReleaseOath());
    HealPokemon(&restored);
    EXPECT_EQ(GetMonData(&restored, MON_DATA_HP), 0);
    EXPECT(PokemonUseItemEffects(&restored, ITEM_REVIVE, 0, 0, FALSE));
    EXPECT_EQ(gIchorSave.oath.fallenCount, 1);
}

TEST("Ichor: ordinary fainted partners can still heal and use revival items")
{
    struct Pokemon mon;
    u32 zero = 0;
    ResetOath();
    CreateOathMon(&mon);
    mon.box.oathFallen = TRUE;
    SetMonData(&mon, MON_DATA_HP, &zero);
    EXPECT(!PokemonUseItemEffects(&mon, ITEM_REVIVE, 0, 0, FALSE));
    EXPECT(GetMonData(&mon, MON_DATA_HP) > 0);
    SetMonData(&mon, MON_DATA_HP, &zero);
    HealPokemon(&mon);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_HP), GetMonData(&mon, MON_DATA_MAX_HP));
}

TEST("Ichor: Revival Blessing's target search skips fallen partners")
{
    u32 zero = 0;
    struct Pokemon *party = gParties[B_TRAINER_PLAYER];
    ResetOath();
    ZeroPlayerPartyMons();
    gBattleTypeFlags = 0;
    EXPECT(Ichor_ChooseOath(TRUE));
    CreateOathMon(&party[0]);
    SetMonData(&party[0], MON_DATA_HP, &zero);
    EXPECT_EQ(GetFirstFaintedPartyIndex(B_BATTLER_0), 0);
    EXPECT(Ichor_RecordOathFallen(&party[0]));
    EXPECT_EQ(GetFirstFaintedPartyIndex(B_BATTLER_0), PARTY_SIZE);
    CreateOathMon(&party[1]);
    SetMonData(&party[1], MON_DATA_HP, &zero);
    EXPECT_EQ(GetFirstFaintedPartyIndex(B_BATTLER_0), 1);
}

TEST("Ichor: normal capture storage skips every reserved Urn jar")
{
    struct Pokemon mon;
    struct BoxPokemon snapshot;
    u32 box, slot;
    ResetOath();
    EXPECT(Ichor_ChooseOath(TRUE));
    gIchorSave.oath.urnBoxes |= 1 << (TOTAL_BOXES_COUNT - 3);
    CreateOathMon(&mon);
    snapshot = mon.box;
    for (box = 0; box < TOTAL_BOXES_COUNT; box++)
        if (!Ichor_IsUrnBox(box))
            for (slot = 0; slot < IN_BOX_COUNT; slot++)
                SetBoxMonAt(box, slot, &mon.box);
    EXPECT(IsPokemonStorageFull());
    EXPECT(!CheckFreePokemonStorageSpace());
    EXPECT_EQ(CopyMonToPC(&mon), MON_CANT_GIVE);
    EXPECT_EQ(memcmp(&mon.box, &snapshot, sizeof(snapshot)), 0);
    EXPECT_EQ(CountMonsInBox(TOTAL_BOXES_COUNT - 1), 0);
    EXPECT_EQ(CountMonsInBox(TOTAL_BOXES_COUNT - 3), 0);
    ZeroBoxMonAt(0, 0);
    EXPECT(!IsPokemonStorageFull());
    EXPECT(CheckFreePokemonStorageSpace());
    EXPECT_EQ(CopyMonToPC(&mon), MON_GIVEN_TO_PC);
    EXPECT_EQ(GetBoxMonDataAt(0, 0, MON_DATA_SPECIES), SPECIES_NEBREL);
    EXPECT_EQ(CountMonsInBox(TOTAL_BOXES_COUNT - 1), 0);
    EXPECT(Ichor_ReleaseOath());
    EXPECT(IsPokemonStorageFull());
}

TEST("Ichor: fallen partners cannot use ordinary PC deposit or selection APIs")
{
    struct Pokemon mon;
    u32 zero = 0;
    ResetOath();
    EXPECT(Ichor_ChooseOath(TRUE));
    CreateOathMon(&mon);
    SetMonMoveSlot(&mon, MOVE_TACKLE, 0);
    SetMonData(&mon, MON_DATA_HP, &zero);
    EXPECT(Ichor_RecordOathFallen(&mon));
    EXPECT_EQ(CopyMonToPC(&mon), MON_CANT_GIVE);
    EXPECT(!CanBoxMonBeSelected(&mon.box));
    EXPECT(IsBoxMonExcluded(&mon.box));
    EXPECT_EQ(GetMonData(&mon, MON_DATA_SPECIES), SPECIES_NEBREL);
    EXPECT_EQ(Ichor_StoreOathFallen(&mon), ICHOR_URN_STORED);
    EXPECT_EQ(CountStorageNonEggMons(), 0);
    EXPECT(!AnyStorageMonWithMove(MOVE_TACKLE));
}

TEST("Ichor: unsworn saves keep the final jar available for ordinary storage")
{
    struct Pokemon mon;
    u32 box, slot;
    ResetOath();
    CreateOathMon(&mon);
    for (box = 0; box < TOTAL_BOXES_COUNT - 1; box++)
        for (slot = 0; slot < IN_BOX_COUNT; slot++)
            SetBoxMonAt(box, slot, &mon.box);
    EXPECT(!IsPokemonStorageFull());
    EXPECT(CheckFreePokemonStorageSpace());
    EXPECT_EQ(CopyMonToPC(&mon), MON_GIVEN_TO_PC);
    EXPECT_EQ(CountMonsInBox(TOTAL_BOXES_COUNT - 1), 1);
}

SINGLE_BATTLE_TEST("Ichor: recorded-link simulation fainting never marks a real partner")
{
    GIVEN {
        ResetOath();
        EXPECT(Ichor_ChooseOath(TRUE));
        PLAYER(SPECIES_WOBBUFFET) { HP(1); }
        PLAYER(SPECIES_WYNAUT);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(opponent, MOVE_SCRATCH); SEND_OUT(player, 1); }
    } THEN {
        EXPECT_EQ(gIchorSave.oath.fallenCount, 0);
        EXPECT(!Ichor_IsOathFallen(&gParties[B_TRAINER_PLAYER][0].box));
        Ichor_InitSave();
    }

}

TEST("Ichor: real trainer and wild fainting count but simulations and tutorials do not")
{
    const u32 excluded[] = {
        BATTLE_TYPE_LINK, BATTLE_TYPE_LINK_IN_BATTLE, BATTLE_TYPE_TOWER_LINK_MULTI,
        BATTLE_TYPE_RECORDED, BATTLE_TYPE_RECORDED_LINK, BATTLE_TYPE_FRONTIER,
        BATTLE_TYPE_TRAINER_HILL, BATTLE_TYPE_SECRET_BASE,
        BATTLE_TYPE_CATCH_TUTORIAL, BATTLE_TYPE_POKEDUDE,
    };
    u32 i;
    ResetOath();
    EXPECT(!Ichor_IsOathBattle(BATTLE_TYPE_TRAINER));
    EXPECT(Ichor_ChooseOath(TRUE));
    EXPECT(Ichor_IsOathBattle(BATTLE_TYPE_IS_MASTER));
    EXPECT(Ichor_IsOathBattle(BATTLE_TYPE_TRAINER));
    EXPECT(Ichor_IsOathBattle(BATTLE_TYPE_GHOST));
    for (i = 0; i < ARRAY_COUNT(excluded); i++)
        EXPECT(!Ichor_IsOathBattle(excluded[i]));
}
