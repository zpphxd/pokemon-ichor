#ifndef GUARD_ICHOR_ARKADIA_H
#define GUARD_ICHOR_ARKADIA_H

// Ichor: Arkadia's scenes that need the engine (design/phase3/SCRIPT.md, beats
// 42-43). Every function here is a special (data/specials.inc).

void Ichor_ObjectFadeIn(void);       // local id gSpecialVar_0x8004 fades in over 16 frames
void Ichor_ObjectFadeOut(void);      // ... and out (then removeobject it)
void Ichor_ShowKleonTablet(void);    // Iapetos's wax tablet, in a picture box
void Ichor_HideKleonTablet(void);

#endif // GUARD_ICHOR_ARKADIA_H
