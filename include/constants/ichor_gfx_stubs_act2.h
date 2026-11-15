#ifndef GUARD_CONSTANTS_ICHOR_GFX_STUBS_ACT2_H
#define GUARD_CONSTANTS_ICHOR_GFX_STUBS_ACT2_H

// ICHOR_STUB_TRAINER_ART (world-act2): Act II batch 1's new walkers and objects, named now so
// map scripts and map.json files can use their final names before the art exists. Each one
// points at an existing Ichor walker of the nearest look.
//
// When you add a real OBJ_EVENT_GFX_ICHOR_<NAME> to event_objects.h's enum, DELETE its line
// here in the same commit. A leftover line silently redirects the real sprite to the stand-in.
// design/phase3/BUILD.md lists who uses which.

// Batch 2, the road west (SCRIPT.md Part 10). The sprites2 agent makes these real.

// Batch 3, Arkadia (SCRIPT.md Part 10). The sprites3 agent makes these real.
#define OBJ_EVENT_GFX_ICHOR_HUNTRESS        OBJ_EVENT_GFX_ICHOR_YOUTH_F
#define OBJ_EVENT_GFX_ICHOR_CHARCOALER      OBJ_EVENT_GFX_ICHOR_MAN
#define OBJ_EVENT_GFX_ICHOR_KALLISTO        OBJ_EVENT_GFX_ICHOR_PRIESTESS
#define OBJ_EVENT_GFX_ICHOR_KLEON_STUMP     OBJ_EVENT_GFX_ICHOR_KLEON_SEATED
#define OBJ_EVENT_GFX_ICHOR_KLEON_BALLS     OBJ_EVENT_GFX_ICHOR_TABLET
#define OBJ_EVENT_GFX_ICHOR_TEMPLE_HOUND    OBJ_EVENT_GFX_ICHOR_TABLET
#define OBJ_EVENT_GFX_ICHOR_GOLDEN_HIND     OBJ_EVENT_GFX_ICHOR_TABLET
#define OBJ_EVENT_GFX_ICHOR_PHYLONOE        OBJ_EVENT_GFX_ICHOR_KID_F
#define OBJ_EVENT_GFX_ICHOR_MULETEER        OBJ_EVENT_GFX_ICHOR_MAN
#define OBJ_EVENT_GFX_ICHOR_LAMPLIGHTER     OBJ_EVENT_GFX_ICHOR_MAN

#endif // GUARD_CONSTANTS_ICHOR_GFX_STUBS_ACT2_H
