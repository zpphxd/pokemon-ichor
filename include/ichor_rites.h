#ifndef GUARD_ICHOR_RITES_H
#define GUARD_ICHOR_RITES_H

// Ichor: the rites (design/SYSTEMS.md §3). Altars, Favor 0-100 per god, one
// blessing at a time counted in steps, and gifts at Favor 30, 60 and 100.
// design/ENGINE_API.md §3 lists what map scripts call.

#include "constants/ichor.h"

struct WildPokemon;

// IchorSave.blessing.flags
#define ICHOR_BLESSING_MAJOR   (1 << 0)  // from an offering; a prayer gives the minor one
#define ICHOR_BLESSING_FRENZY  (1 << 1)  // Dionysus's Frenzy
#define ICHOR_BLESSING_REVEL   (1 << 2)  // given through Dionysus's Revel

#define ICHOR_FAVOR_MAX        100
#define ICHOR_RANK_KNOWN       10
#define ICHOR_RANK_FAVORED     30   // gift I
#define ICHOR_RANK_BELOVED     60   // gift II
#define ICHOR_RANK_CHOSEN      100  // gift III
#define ICHOR_BLESSING_MAX_STEPS 4095

u8 Ichor_GetFavor(u32 god);
void Ichor_AddFavorTo(u32 god, u32 amount);
bool32 Ichor_HasBlessing(void);
void Ichor_SetBlessingTo(u32 god, u32 steps, u32 flags);
bool32 Ichor_IsFrenzy(void);
const u8 *Ichor_GetGodName(u32 god);
void Ichor_BufferBlessingPanel(u8 *dst);

// The step tick (field_control_avatar.c)
bool8 Ichor_OnStep(void);

// Blessing hooks, one call each in vanilla code
u32 Ichor_ModifyEncounterRate(u32 rate);                    // wild_encounter.c
u32 Ichor_ModifyLandSlot(u32 index);                        // wild_encounter.c
u32 Ichor_ModifyWildSlot(const struct WildPokemon *wildPokemon, u32 index, u32 (*choose)(void));
bool32 Ichor_IsWildLevelAllowed(u32 level);                 // wild_encounter.c
u32 Ichor_ModifyWildLevel(u32 level);                       // wild_encounter.c
u32 Ichor_ModifyWildGender(u32 gender, u32 species);        // wild_encounter.c
bool32 Ichor_BoostsWildHeldItems(void);                     // pokemon.c
void Ichor_ModifyExp(s32 *expAmount);                       // battle_script_commands.c
u32 Ichor_ModifyPrizeMoney(u32 money);                      // battle_script_commands.c
bool32 Ichor_AlwaysEscapes(u32 battler);                    // battle_util.c
u32 Ichor_ModifyBuyPrice(u32 price);                        // shop.c
u32 Ichor_ModifySellPrice(u32 itemId, u32 price);           // item.c
bool32 Ichor_FishBitesAtOnce(void);                         // fishing.c
bool32 Ichor_FavorsRareFishingSlots(void);                  // wild_encounter.c
u32 Ichor_ExtraShinyRolls(void);                            // pokemon.c
u32 Ichor_ExtraEggCycles(void);                             // daycare.c
u32 Ichor_ModifyEggChance(u32 chance);                      // daycare.c
s32 Ichor_ModifyFriendshipDelta(struct Pokemon *mon, s32 delta); // pokemon.c
u32 Ichor_ExtraBerryYield(void);                            // berry.c
u32 Ichor_DexNavSneakBonus(void);                           // dexnav.c
u32 Ichor_DexNavHiddenRate(u32 rate);                       // dexnav.c

#endif // GUARD_ICHOR_RITES_H
