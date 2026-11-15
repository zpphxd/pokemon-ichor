// Constants for tools/ichor/tests/oikoumene_music.lua (see engine_consts.h).
#include "engine_consts.h"
#include "gba/m4a_internal.h"
#include "constants/songs.h"

// The Oikoumene's batch-1 songs, in id order (design/oikoumene/MUSIC_cues.md)
K(MUS_ICHOR_WIDER_WORLD, MUS_ICHOR_WIDER_WORLD)
K(MUS_ICHOR_PLAIN_OF_TROY, MUS_ICHOR_PLAIN_OF_TROY)
K(MUS_ICHOR_BLACK_LAND, MUS_ICHOR_BLACK_LAND)
K(MUS_ICHOR_NECROPOLIS, MUS_ICHOR_NECROPOLIS)
K(MUS_ICHOR_BLACK_SEA, MUS_ICHOR_BLACK_SEA)
K(MUS_ICHOR_BATTLE_OIKOUMENE, MUS_ICHOR_BATTLE_OIKOUMENE)
K(MUS_ICHOR_BATTLE_PERIODOS, MUS_ICHOR_BATTLE_PERIODOS)
K(MUS_ICHOR_PERIODOS_TROAD, MUS_ICHOR_PERIODOS_TROAD)
K(MUS_ICHOR_PERIODOS_EGYPT, MUS_ICHOR_PERIODOS_EGYPT)
K(MUS_ICHOR_PERIODOS_PONTOS, MUS_ICHOR_PERIODOS_PONTOS)
K(START_MUS, START_MUS)
K(END_MUS, END_MUS)
// m4a's player and song header
K(OFF_MPLAY_STATUS, offsetof(struct MusicPlayerInfo, status))
K(OFF_MPLAY_CLOCK, offsetof(struct MusicPlayerInfo, clock))
K(OFF_MPLAY_TEMPOD, offsetof(struct MusicPlayerInfo, tempoD))
K(OFF_SONGHDR_TRACKS, offsetof(struct SongHeader, trackCount))
K(OFF_SONGHDR_TONE, offsetof(struct SongHeader, tone))
K(MUSICPLAYER_STATUS_TRACK, MUSICPLAYER_STATUS_TRACK)
K(MUSICPLAYER_STATUS_PAUSE, MUSICPLAYER_STATUS_PAUSE)
K(OFF_MAIN_VBLANK1, offsetof(struct Main, vblankCounter1))
