#ifndef GUARD_ICHOR_OATH_H
#define GUARD_ICHOR_OATH_H

struct Pokemon;
struct BoxPokemon;

enum
{
    ICHOR_OATH_UNDECIDED,
    ICHOR_OATH_DECLINED,
    ICHOR_OATH_ACTIVE,
    ICHOR_OATH_RELEASED,
    ICHOR_OATH_FAILED,
};

enum
{
    ICHOR_URN_NOT_FALLEN,
    ICHOR_URN_STORED,
    ICHOR_URN_FULL,
};

enum
{
    ICHOR_OATH_RECOVERY_NONE,
    ICHOR_OATH_RECOVERED,
    ICHOR_OATH_EXHAUSTED,
    ICHOR_OATH_RECOVERY_BLOCKED,
};

bool32 Ichor_IsOathActive(void);
bool32 Ichor_IsOathBattle(u32 battleType);
bool32 Ichor_ChooseOath(bool32 swear);
bool32 Ichor_ReleaseOath(void);
bool32 Ichor_FailOath(void);
bool32 Ichor_HasOathEncounter(u32 mapSection);
bool32 Ichor_ClaimOathEncounter(u32 mapSection);
u32 Ichor_CountOathEncounters(void);
void Ichor_BeginOathBattle(u32 battleType, u32 mapSection);
bool32 Ichor_CanCatchOathBattle(void);
bool32 Ichor_IsUrnBox(u32 box);
bool32 Ichor_IsOathFallen(const struct BoxPokemon *mon);
bool32 Ichor_RecordOathFallen(struct Pokemon *mon);
u32 Ichor_StoreOathFallen(struct Pokemon *mon);
u32 Ichor_StoreOathPartyFallen(void);
bool32 Ichor_EndOathBattle(u32 battleType, u32 battleOutcome);
void Ichor_RetryOathUrn(void);
u32 Ichor_PrepareOathRecovery(void);
void Ichor_ShowOathEndScreen(bool32 capacityBlocked);
bool32 Ichor_ShowOathAftermathNotice(void);

#endif
