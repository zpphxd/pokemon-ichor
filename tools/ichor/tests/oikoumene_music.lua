-- The Oikoumene's batch-1 music, run by tools/ichor/tests/oikoumene_music.sh (read it first).
--
-- For each new song: its gSongTable slot holds a real header in ROM, named for the
-- song, on the `ichor` voicegroup, with 1 to 10 tracks. Then a map script plays it
-- with playbgm (oikoumene_music_setup.s) and the run checks that the BGM player has
-- it, that its clock advances at the song's tempo, that the game keeps running in
-- the overworld, and that it is still playing past the end of its first loop (the
-- loop's jump back works and the song never stops).

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, emu = L.S, L.emu
local expect, wait = L.expect, L.wait
local M = dofile(L.OUT .. "music_symbols.lua")
local LEN = dofile(L.OUT .. "song_lengths.lua")

local SONGS = { "MUS_ICHOR_WIDER_WORLD", "MUS_ICHOR_PLAIN_OF_TROY", "MUS_ICHOR_BLACK_LAND", "MUS_ICHOR_NECROPOLIS",
  "MUS_ICHOR_BLACK_SEA", "MUS_ICHOR_BATTLE_OIKOUMENE", "MUS_ICHOR_BATTLE_PERIODOS", "MUS_ICHOR_PERIODOS_TROAD",
  "MUS_ICHOR_PERIODOS_EGYPT", "MUS_ICHOR_PERIODOS_PONTOS" }

local function status() return emu:read32(S.gMPlayInfo_BGM + S.OFF_MPLAY_STATUS) end
local function clock() return emu:read32(S.gMPlayInfo_BGM + S.OFF_MPLAY_CLOCK) end
local function vblank() return emu:read32(S.gMain + S.OFF_MAIN_VBLANK1) end
local function sounding()
  local st = status()
  return st & S.MUSICPLAYER_STATUS_TRACK ~= 0 and st & S.MUSICPLAYER_STATUS_PAUSE == 0
end

L.start(function()
  L.quickstart()
  expect(S.END_MUS == S.MUS_ICHOR_PERIODOS_PONTOS, string.format("END_MUS (%d) is the last Oikoumene song", S.END_MUS))

  for _, name in ipairs(SONGS) do
    local id, len = S[name], LEN[name]
    local hdr = L.songHeader(id)
    expect(hdr >= 0x08000000 and hdr < 0x0A000000, string.format("%s (%d) has a header in ROM (0x%08x)", name, id, hdr))
    expect(L.songName(hdr) == name:lower(), string.format("%s's slot plays %s", name, L.songName(hdr)))
    local tracks = emu:read8(hdr + S.OFF_SONGHDR_TRACKS)
    expect(tracks >= 1 and tracks <= 10, string.format("%s has %d tracks", name, tracks))
    expect(emu:read32(hdr + S.OFF_SONGHDR_TONE) == M.voicegroup_ichor, name .. " is on the ichor voicegroup")

    -- (cpp has already turned the song's name into its id when the macro names the header)
    L.runHeader("MusicTest_" .. id .. "Header", { noSettle = true })
    wait(30)
    expect(L.playing(id) and sounding(), name .. " is playing on the BGM player")

    -- three seconds: the clock runs at the song's tempo (m4a: tempo / 150 ticks a frame)
    local c0, v0 = clock(), vblank()
    wait(180)
    local ticks, want = clock() - c0, 180 * len.tempo / 150
    expect(math.abs(ticks - want) <= 2, string.format("%s advances %d ticks in 180 frames (tempo %d wants %.0f)",
                                                       name, ticks, len.tempo, want))
    expect(vblank() - v0 >= 179 and L.inOverworld(), name .. ": the game runs on in the overworld")

    -- past the end of the first loop: still this song, still sounding
    local left = math.ceil((len.ticks - clock()) * 150 / len.tempo) + 120
    if left > 0 then wait(left) end
    expect(clock() > len.ticks and L.playing(id) and sounding(),
           string.format("%s loops: still playing at tick %d, past its end at %d", name, clock(), len.ticks))
  end
end)
