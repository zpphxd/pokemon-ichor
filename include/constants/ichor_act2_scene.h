#ifndef GUARD_CONSTANTS_ICHOR_ACT2_SCENE_H
#define GUARD_CONSTANTS_ICHOR_ACT2_SCENE_H

// Ichor: the Dionysia's constants (design/phase3/SCRIPT.md, beats 32-34), and
// the picture window's (beats 32-55), for the C (src/ichor_act2_scene.c) and
// the scripts (data/event_scripts.s includes this file). Only #defines here.

// VAR_ICHOR_DIONYSIA, the play's stage
#define DIONYSIA_NONE          0  // before the play
#define DIONYSIA_PLAY          1  // the tragedy: the opening scene in the theater
#define DIONYSIA_BACKSTAGE     2  // Silenos called the awake ones backstage: Thespis's scene
#define DIONYSIA_ENTRANCE_1    3  // the entrances: none made yet (all six blocks entranced)
#define DIONYSIA_ENTRANCE_2    4  // the comic entrance made (the low pair laughs)
#define DIONYSIA_ENTRANCE_3    5  // the tragic entrance made (the middle pair laughs)
#define DIONYSIA_WAKING        6  // the satyrs: the trance breaks, the actor fights
#define DIONYSIA_OVER          7  // FLAG_ICHOR_DIONYSIA_DONE: Kleon waits in the empty theater
#define DIONYSIA_EMPTY         8  // Kleon's third battle is over: the theater stands empty

// VAR_ICHOR_DIONYSIA_MASK, the mask worn backstage (kept across the entrances' warps)
#define DIONYSIA_MASK_NONE     0
#define DIONYSIA_MASK_COMIC    1
#define DIONYSIA_MASK_TRAGIC   2
#define DIONYSIA_MASK_SATYR    3

// The three pairs of blocks of seats (gSpecialVar_0x8004 for the trance specials)
#define THEATER_PAIR_LOW       0  // blocks 1 and 6: their ends come down to the parodoi
#define THEATER_PAIR_MID       1  // blocks 2 and 5
#define THEATER_PAIR_TOP       2  // blocks 3 and 4: the back of the cavea
#define THEATER_PAIR_COUNT     3

// Where the entrances come out on the stage: each stage door's lower cell
// (tools/ichor/maps/theater.py), and the skene's door cells behind them.
#define THEATER_DOOR_IVY_X     14
#define THEATER_DOOR_CROWN_X   19
#define THEATER_DOOR_GOAT_X    25
#define THEATER_DOOR_Y         5
#define SKENE_DOOR_IVY_X       4
#define SKENE_DOOR_CROWN_X     9
#define SKENE_DOOR_GOAT_X      15
#define SKENE_DOOR_Y           2

// Ichor_ShowPicture's pictures (gSpecialVar_0x8004): a 64x64 image in a picture box
#define ICHOR_PICTURE_PROGRAM          0  // the Dionysia's program, with the hook (beat 32)
#define ICHOR_PICTURE_DECREE           1  // the ostracism's decree (Astyra, beat 53)
#define ICHOR_PICTURE_FORGED_ORDER     2  // the forged order at the Propylaia (the Akropolis, beat 55)
#define ICHOR_PICTURE_PRACTICE_TABLETS 3  // the practice tablets at the hearing (the Stoa, beat 52)
#define ICHOR_PICTURE_COUNT            4

#endif // GUARD_CONSTANTS_ICHOR_ACT2_SCENE_H
