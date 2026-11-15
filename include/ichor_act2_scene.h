#ifndef GUARD_ICHOR_ACT2_SCENE_H
#define GUARD_ICHOR_ACT2_SCENE_H

// Ichor: Act II's scenes that need the engine (design/phase3/SCRIPT.md, beats
// 32-34): the Dionysia in Thyrsa's theater, and its picture window, which
// Astyra's beats 52-55 reuse. Every function here is a special
// (data/specials.inc); the scripts are data/maps/ThyrsaTheater*/scripts.pory
// and data/scripts/ichor_act2.pory. The stages and pairs are in
// constants/ichor_act2_scene.h.

#include "constants/ichor_act2_scene.h"

void Ichor_TheaterDusk(void);            // hold the theater at dusk, whatever the clock says
void Ichor_TheaterFillSeats(void);       // seat the Dionysia's audience (ON_LOAD)
void Ichor_TheaterTranceResume(void);    // restart the pulse for the play's stage (ON_RESUME)
void Ichor_TheaterTranceStart(void);     // the pulse begins on every pair and grows
void Ichor_TheaterTranceRelease(void);   // pair gSpecialVar_0x8004 laughs: its pulse drains away
void Ichor_TheaterTranceWake(void);      // the laugh runs round the cavea: every pair drains, top first (waits)
void Ichor_TheaterGaze(void);            // the masks' eyes pass along the tiers, block by block (waits)
void Ichor_ShowPicture(void);            // picture gSpecialVar_0x8004 (ICHOR_PICTURE_*), in a picture box
void Ichor_HidePicture(void);
void Ichor_ShowProgram(void);            // Alethea's program: Ichor_ShowPicture's ICHOR_PICTURE_PROGRAM
void Ichor_HideProgram(void);

#endif // GUARD_ICHOR_ACT2_SCENE_H
