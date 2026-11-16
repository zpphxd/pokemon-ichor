#ifndef GUARD_ICHOR_OATH_H
#define GUARD_ICHOR_OATH_H

enum
{
    ICHOR_OATH_UNDECIDED,
    ICHOR_OATH_DECLINED,
    ICHOR_OATH_ACTIVE,
    ICHOR_OATH_RELEASED,
    ICHOR_OATH_FAILED,
};

bool32 Ichor_IsOathActive(void);
bool32 Ichor_ChooseOath(bool32 swear);
bool32 Ichor_ReleaseOath(void);
bool32 Ichor_FailOath(void);
bool32 Ichor_HasOathEncounter(u32 mapSection);
bool32 Ichor_ClaimOathEncounter(u32 mapSection);
u32 Ichor_CountOathEncounters(void);

#endif
