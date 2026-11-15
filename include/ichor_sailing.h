#ifndef GUARD_ICHOR_SAILING_H
#define GUARD_ICHOR_SAILING_H

// Ichor postgame: the sailing layer. The ship at sea, wind, the helm's voyages,
// going below deck and back, the at-sea lock and the Great Bear
// (src/ichor_sailing.c, design/postgame/ENGINE.md).

#include "constants/ichor_sailing.h"

// The ship avatar (field_player_avatar.c, field_effect_helpers.c)
bool32 Ichor_IsSailing(void);
bool32 Ichor_IsShipGraphics(u16 graphicsId);
u16 Ichor_GetShipGraphicsId(u32 direction);
void Ichor_SailStep(u32 direction);
void Ichor_SailTurn(u32 direction);
u32 Ichor_SailPushDirection(u32 direction);
u32 Ichor_TakeArrivalFacing(void);

// Wind
u32 Ichor_GetWindDirection(void);
u32 Ichor_GetWindStrength(void);
u32 Ichor_GetSailing(u32 direction);
void Ichor_RollDailyWind(void);
u32 Ichor_ModifySailingEncounterRate(u32 encounterRate);
bool32 Ichor_HasWindPanel(void);
u8 *Ichor_BufferWindPanel(u8 *dst);
#define ICHOR_WIND_PANEL_WIDTH 17   // tiles: "Wind: south-east, strong" is 129 px

// The at-sea lock on the Wings (FLAG_ICHOR_AT_SEA)
bool32 Ichor_IsSeaLocked(void);
extern const u8 gText_IchorNoHermAtSea[];

// The Relic Ring's DECK entry
bool32 Ichor_CanGoBelowDeck(void);

// The Great Bear, once a field frame (overworld.c)
bool8 Ichor_IsStarsOut(void);
void Ichor_SailingFrame(void);
void Ichor_SpriteCB_GreatBear(struct Sprite *sprite);

#endif // GUARD_ICHOR_SAILING_H
