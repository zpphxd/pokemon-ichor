-- Route 8, the Kopais shore, run by tools/ichor/tests/act2_route8.sh (read it first).
--
-- Setup touches no ROM data: after Quickstart a test-only event script in spare
-- EWRAM gives a level-100 Prinplup that knows only Surf (and the eighth badge, so
-- it obeys), Act II's flag, the Girdle of Herakles, an Olive Oil and a Fresh Water,
-- a long Repel, and warps onto the road at the east edge (the Neistan Gate's side).
-- Then the road is played west with key presses, finding people, signs and items
-- by the scripts and flags they use (slice_lib.lua).
--
-- Prints "ROUTE8 ok ..." per check and "ROUTE8 shot ..." per screenshot, and ends
-- with "ROUTE8 done"; a failure prints "ROUTE8 FAIL: ..." first.

local L = dofile("tools/ichor/tests/slice_lib.lua")
L.init{ tag = "ROUTE8", out = "build/test_route8/", symbols = "build/test_route8/symbols.lua" }
local S, K = L.S, L.K
local emu = L.emu
local log, expect, wait, waitUntil, shot = L.log, L.expect, L.wait, L.waitUntil, L.shot
local R8 = "Route8_Kopais_EventScript_"

local function bankFlag(f)
  local o = f - S.ICHOR_FLAGS_START
  local base = emu:read32(S.gSaveBlock3Ptr) + S.OFF_SB3_ICHOR + S.OFF_ICHOR_FLAGS
  return (emu:read8(base + (o >> 3)) >> (o & 7)) & 1 == 1
end
-- slice_lib's walker hides people by their hide flags; Route 8's are in the Ichor bank.
local getFlag1 = L.getFlag
function L.getFlag(f)
  if f >= S.ICHOR_FLAGS_START and f <= S.ICHOR_FLAGS_END then return bankFlag(f) end
  return getFlag1(f)
end

local function warpIn(x, y, flags, extra)
  local s = { S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 } }
  for _, b in ipairs(extra or {}) do s[#s + 1] = b end
  for _, f in ipairs(flags or {}) do
    s[#s + 1] = S.SCR_OP_SETFLAG
    s[#s + 1] = { f, 2 }
  end
  local map = S.MAP_ROUTE8
  for _, b in ipairs({ S.SCR_OP_WARP, map >> 8, map & 0xFF, S.WARP_ID_NONE & 0xFF, { x, 2 }, { y, 2 },
                       S.SCR_OP_WAITSTATE, S.SCR_OP_END }) do
    s[#s + 1] = b
  end
  L.runRamScript(s)
  waitUntil(function() return L.mapId() == S.MAP_ROUTE8 and L.idle() end, 4000, "Route 8")
  wait(30)
end

local function read(note, name)
  L.talk(L.npc(R8 .. note), { shots = { [1] = name } })
end

local function main()
  -- Boot, skip the intro, Quickstart (the smoke test's timing).
  waitUntil(function() return L.now() >= 500 end, 600, "frame 500")
  L.tap(K.START)
  waitUntil(function() return L.now() >= 1020 end, 600, "frame 1020")
  L.tap(K.SELECT)
  waitUntil(L.idle, 4000, "the new game")
  wait(30)
  -- Fast text, Set battle style, no battle animations.
  local opt = L.sb2() + S.OFF_SB2_OPTIONS
  emu:write16(opt, (emu:read16(opt) & ~0x7) | 2 | (1 << 9) | (1 << 10))

  L.setBeat("35A_east", false)
  local setup = { S.SCR_OP_CALLNATIVE, { S.ScrCmd_createmon | 1, 4 }, 0, S.PARTY_SIZE,
                  { S.SPECIES_TEST, 2 }, { 100, 2 }, { (1 << 17) | (1 << 18) | (1 << 19) | (1 << 20), 4 },
                  { S.MOVE_TEST, 2 }, { S.MOVE_NONE, 2 }, { S.MOVE_NONE, 2 }, { S.MOVE_NONE, 2 },
                  S.SCR_OP_ADDITEM, { S.ITEM_OLIVE_OIL, 2 }, { 1, 2 },
                  S.SCR_OP_ADDITEM, { S.ITEM_FRESH_WATER, 2 }, { 1, 2 },
                  S.SCR_OP_SETVAR, { S.VAR_REPEL_STEP_COUNT, 2 }, { 999, 2 } }
  warpIn(62, 14, { S.FLAG_SYS_POKEMON_GET, S.FLAG_BADGE08_GET, S.FLAG_ACT2_BEGUN, S.FLAG_GIRDLE }, setup)
  expect(L.mapId() == S.MAP_ROUTE8, "on Route 8 at the east edge")
  local mus = L.mapMusic()
  expect(mus == S.MUS_ROAD or mus == S.MUS_ROAD_NIGHT,
         string.format("Route 8 plays the road's music (song %d)", mus))
  shot("east_edge")

  -- The east end: the sign, Alethea's first note and hole, Gorgidas at the reeds.
  L.talk(L.sign(R8 .. "SignEast"), { shots = { [1] = "sign_east" } })
  read("Note1", "note_1")
  L.talk(L.sign(R8 .. "DigEast"))
  L.go(50, 14); shot("gorgidas_reeds")
  expect(L.defeated(S.TRAINER_GORGIDAS), "Gorgidas spotted the player on the road")

  -- Band 1, then the eel-smoker's fire and the reeds behind it.
  L.go(47, 13); shot("band_1")
  L.go(44, 13); shot("eel_smokers_fire")
  L.talk(L.npc(R8 .. "EelSmoker"), { shots = { [1] = "eel_smoker" } })
  local hs = L.itemCount(S.ITEM_HEART_SCALE)
  L.talk(L.hidden(S.FLAG_HIDDEN_HEART_SCALE))
  expect(L.itemCount(S.ITEM_HEART_SCALE) == hs + 1, "the Heart Scale in the reeds behind the fire")

  -- The dike: the sign, Ismenias on his step, the jetty, note 2 and its hole, the Pearl.
  L.setBeat("35A_dike", false)
  L.talk(L.sign(R8 .. "SignDike"))
  L.go(37, 14); shot("dike_east")
  L.go(33, 14); shot("dike_middle")
  expect(L.defeated(S.TRAINER_ISMENIAS), "Ismenias saw the player cross the dike")
  L.talk(L.ball(S.FLAG_ITEM_SUPER_REPEL), { shotBefore = "the_jetty" })
  expect(L.itemCount(S.ITEM_SUPER_REPEL) >= 1, "the Super Repel at the jetty's end")
  read("Note2", "note_2")
  L.talk(L.sign(R8 .. "DigDike"))
  local pearl = L.itemCount(S.ITEM_PEARL)
  L.talk(L.hidden(S.FLAG_HIDDEN_PEARL))
  expect(L.itemCount(S.ITEM_PEARL) == pearl + 1, "the Pearl at the very end of the dike")

  -- Band 2, the herm at the spur fork, the decoy traveler, Timoxena's reeds.
  L.setBeat("35A_herm", false)
  L.go(28, 15); shot("band_2")
  expect(L.defeated(S.TRAINER_PELOPIDAS), "Pelopidas saw the player cross band 2")
  L.go(24, 15); shot("the_great_herm")
  L.talk(L.sign(R8 .. "GreatHerm"), { shots = { [1] = "herm_sign" } })
  expect(L.getFlag(S.FLAG_HERM), "the great herm anointed (Olive Oil)")
  L.talk(L.npc(R8 .. "Traveler"), { shots = { [1] = "traveler" } })
  expect(L.itemCount(S.ITEM_BARLEY_CAKE) == 1, "the traveler's Barley Cake, for the Fresh Water")
  expect(L.getFlag(S.FLAG_DECOY), "the decoy's flag")
  expect(not L.npc(R8 .. "Traveler").present, "the traveler has gone on")
  L.talk(L.npc(R8 .. "Timoxena"), { shotBefore = "timoxena" })
  expect(L.defeated(S.TRAINER_TIMOXENA), "Timoxena fought in the reeds")
  L.talk(L.ball(S.FLAG_ITEM_ULTRA_BALL))
  expect(L.itemCount(S.ITEM_ULTRA_BALL) >= 1, "the Ultra Ball deep in the reeds")

  -- Onchestos, note 3, the spur, the Sphinx's ledge.
  L.setBeat("35A_spur", false)
  L.talk(L.npc(R8 .. "Megareus"), { shotBefore = "megareus" })
  expect(L.defeated(S.TRAINER_MEGAREUS), "Megareus raced at Onchestos")
  L.talk(L.sign(R8 .. "SignOnchestos"), { shots = { [1] = "onchestos" } })
  L.talk(L.sign(R8 .. "DigOnchestos"))
  read("Note3", "note_3")
  L.go(24, 20); shot("goat_path")
  L.go(24, 23); shot("sphinx_ledge")
  L.talk(L.sign(R8 .. "SignSphinx"))
  local sphinx = L.npc(R8 .. "Enigmaw")
  if not sphinx.present then
    -- the emulator's clock says night, when the Enigmaw is away: bring it out for the
    -- run (the ON_TRANSITION's own day check is the same flag)
    L.note("night on the clock: the Enigmaw is hidden; spawning it to test its battle")
    L.runRamScript({ S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 },
                     S.SCR_OP_CLEARFLAG, { S.FLAG_TEMP_ENIGMAW, 2 },
                     S.SCR_OP_ADDOBJECT, { S.LOCALID_ENIGMAW, 2 }, S.SCR_OP_END })
    wait(30)
    sphinx = L.npc(R8 .. "Enigmaw")
  end
  expect(sphinx.present, "the Enigmaw on the Sphinx's ledge")
  -- slice_lib runs from wild battles; fight this one, as a player catching or beating it would
  local isTrainer = L.isTrainerBattle
  L.isTrainerBattle = function() return true end
  -- come down the goat path onto the slab from the north, so the follower trails
  -- behind on the path and not on the Enigmaw's tile
  L.go(24, 21); L.go(24, 23); L.face(K.DOWN)
  L.tap(K.A); wait(10)
  L.settle({ shots = { [1] = "enigmaw" } })
  L.isTrainerBattle = isTrainer
  expect(L.getFlag(S.FLAG_ENIGMAW), "the Enigmaw beaten (the test's Surf knocks it out)")
  expect(not L.npc(R8 .. "Enigmaw").present, "the ledge is empty")
  L.talk(L.ball(S.FLAG_ITEM_HYPER_POTION))
  expect(L.itemCount(S.ITEM_HYPER_POTION) >= 1, "the Hyper Potion on the Sphinx's ledge")
  L.talk(L.sign(R8 .. "DigSphinx"))

  -- The Treasury of Minyas: the drum in the dromos, the Girdle, three pushes.
  L.setBeat("35A_treasury", false)
  L.talk(L.sign(R8 .. "SignTomb"))
  L.go(18, 23); L.face(K.UP); shot("the_drum")
  L.talk(L.npc("EventScript_StrengthBoulder"))
  -- each push slides the drum a tile while the player stays put; then step after it
  for _ = 1, 10 do
    local px, py = L.pos()
    if px == 18 and py == 20 then break end
    L.step(K.UP); wait(24)
  end
  local x, y = L.pos()
  expect(x == 18 and y == 20, string.format("pushed the drum into the tomb (player at %d,%d)", x, y))
  shot("inside_the_treasury")
  L.talk(L.ball(S.FLAG_ITEM_TM))
  expect(L.itemCount(S.ITEM_TM_STANDIN) >= 1, "the TM in the tomb (Rock Tomb stands in for Ancient Power)")
  L.talk(L.sign(R8 .. "DigTreasury"))
  local nugget = L.itemCount(S.ITEM_NUGGET)
  L.talk(L.hidden(S.FLAG_HIDDEN_NUGGET))
  expect(L.itemCount(S.ITEM_NUGGET) == nugget + 1, "the Nugget in the Treasury's wall")

  -- The way down: east along the gully over the three ledges, to the fire.
  L.setBeat("35A_way_down", false)
  L.go(29, 22); shot("gully_top")
  L.go(39, 23); shot("gully_bottom")
  local mush = L.itemCount(S.ITEM_BIG_MUSHROOM)
  L.talk(L.hidden(S.FLAG_HIDDEN_BIG_MUSHROOM))
  expect(L.itemCount(S.ITEM_BIG_MUSHROOM) == mush + 1, "the Big Mushroom under the last ledge")
  L.go(40, 15); shot("gully_out")

  -- Back west: the narrows and Perses, band 3, the reed-boat shore, the west sign.
  L.setBeat("35A_west", false)
  L.go(16, 15); shot("the_narrows")
  L.go(14, 12)
  expect(L.defeated(S.TRAINER_PERSES), "Perses saw the player through the narrows")
  L.go(10, 12); shot("band_3")
  L.talk(L.npc(R8 .. "ReedBoatBoy"), { shots = { [1] = "reed_boat_boy" } })
  read("Note4", "note_4")
  L.talk(L.npc(R8 .. "Euphrosyne"), { shotBefore = "euphrosyne" })
  expect(L.defeated(S.TRAINER_EUPHROSYNE), "Euphrosyne fought on the shore")
  L.talk(L.ball(S.FLAG_ITEM_FULL_HEAL))
  expect(L.itemCount(S.ITEM_FULL_HEAL) >= 1, "the Full Heal on the shore")
  expect(not L.getFlag(S.FLAG_READ_NOTES), "the fifth note not read yet")
  read("Note5", "note_5")
  expect(L.getFlag(S.FLAG_READ_NOTES), "FLAG_ICHOR_READ_ALETHEA_NOTES set by the fifth note")
  L.talk(L.sign(R8 .. "SignWest"), { shots = { [1] = "sign_west" } })
  shot("west_end")

  -- Out west to Lebadeia (the connection is Route 8's; Lebadeia's own side and its
  -- art are the parnassos agent's).
  L.go(0, 12)
  for _ = 1, 3 do
    if L.mapId() == S.MAP_LEBADEIA then break end
    L.tap(K.LEFT, 24); wait(40)
  end
  if L.mapId() == S.MAP_LEBADEIA then
    log("ok left west into Lebadeia")
    shot("lebadeia_arrival")
  else
    L.note("Lebadeia's placeholder layout blocks its east edge: the seam is checked at integration")
  end
end

L.start(main)
