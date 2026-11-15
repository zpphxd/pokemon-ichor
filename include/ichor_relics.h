#ifndef GUARD_ICHOR_RELICS_H
#define GUARD_ICHOR_RELICS_H

// Ichor: relics, the key items that replace HMs (design/SYSTEMS.md §1, §2).
// See design/ENGINE_API.md §2 for what map scripts call.

#include "main.h"
#include "constants/ichor.h"

// Ownership and use
u16 Ichor_GetRelicFlag(u16 itemId);
bool32 Ichor_HasRelic(u16 itemId);
bool32 Ichor_CanUseRelicHere(u16 itemId);
bool32 Ichor_IsBlessed(u32 god);

// Engine hooks, one call each in vanilla code
void Ichor_OnItemAdded(u16 itemId);             // item.c, AddBagItem
void Ichor_OnMapTransition(void);
void Ichor_OnFieldFrame(void);
bool32 Ichor_IsCarryingFlame(void);
void Ichor_SetCarriedFlame(u32 kind, u32 steps);
u16 Ichor_GetFlameKind(void);
u16 Ichor_GetFlameSteps(void);
bool32 Ichor_CarriedFlameStep(bool32 canTalk);  // ichor_rites.c, Ichor_OnStep
void Ichor_BufferFlamePanel(u8 *dst);           // start_menu.c               // event_data.c, ClearTempFieldEventData
u8 Ichor_GetTorchFlashLevel(void);              // overworld.c, SetDefaultFlashLevel
bool32 Ichor_IsRelicShowArg(u32 arg);           // field_effect.c, FldEff_FieldMoveShowMonInit
void Ichor_StartRelicShow(u16 itemId);
u16 Ichor_GetFlyEffectArg(void);                // field_effect.c, Task_UseFly
struct ObjectEvent;
bool32 Ichor_CanLeapGap(struct ObjectEvent *objectEvent, s16 x, s16 y, u32 direction); // field_player_avatar.c
MainCallback Ichor_GetFlyMapCancelCallback(void); // region_map.c, CB_ExitFlyMap
bool32 Ichor_TryOpenRelicRing(void);            // item_menu.c, UseRegisteredKeyItemOnField

// Bag field-use functions (src/data/items.h)
void ItemUseOutOfBattle_IchorTalaria(u8 taskId);
void ItemUseOutOfBattle_IchorContextual(u8 taskId);
void ItemUseOutOfBattle_IchorTorch(u8 taskId);
void ItemUseOutOfBattle_IchorWings(u8 taskId);
void ItemUseOutOfBattle_IchorThread(u8 taskId);
void ItemUseOutOfBattle_IchorHelm(u8 taskId);
void ItemUseOutOfBattle_IchorAeolusBag(u8 taskId);

// item_use.c helpers the relics use from the bag
void ItemUse_IchorRunFieldScript(u8 taskId, const u8 *script);
void ItemUse_IchorMessage(u8 taskId, const u8 *str);
void ItemUse_IchorOpenScreenFromBag(u8 taskId, MainCallback callback);
bool32 ItemUse_IchorIsFromField(u8 taskId);

struct MapLayout;
void Ichor_UpdateGlow(const struct MapLayout *layout, bool32 skipFaded); // fieldmap.c, after a tileset's palettes load

#endif // GUARD_ICHOR_RELICS_H
