// Ichor: Emerald's intro scenes are gone (src/intro.c draws Ichor's own boot
// sequence from graphics/intro/). Only the bike-ride art the credits still use
// (src/intro_credits_graphics.c) is kept here.
const u16 gIntroPlayer_Pal[] = INCGFX_U16("graphics/intro/scene_2/player.pal", ".gbapal");
const u16 gIntroFlygon_Pal[] = INCGFX_U16("graphics/intro/scene_2/flygon.png", ".gbapal");

const u32 gIntroFlygon_Gfx[] = INCGFX_U32("graphics/intro/scene_2/flygon.png", ".4bpp.smol");
const u32 gIntroBrendan_Gfx[] = INCGFX_U32("graphics/intro/scene_2/brendan.png", ".4bpp.smol");
const u32 gIntroMay_Gfx[] = INCGFX_U32("graphics/intro/scene_2/may.png", ".4bpp.smol");
