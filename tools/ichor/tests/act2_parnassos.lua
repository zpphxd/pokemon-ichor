-- Lebadeia and Route 9 check, run by tools/ichor/tests/act2_parnassos.sh (read it first).
--
-- Setup touches no ROM data: after Quickstart a test-only event script in spare
-- EWRAM gives a level-100 team, the Girdle (its relic flag), Act II's flags and a
-- long Repel, and warps onto the road at Lebadeia's east gate. Then everything is
-- played with key presses, finding people, signs and triggers by their scripts.
--
-- Prints "PARN ok ..." per check and "PARN shot ..." per screenshot, and ends with
-- "PARN done"; a failure prints "PARN FAIL: ..." first.

local L = dofile("tools/ichor/tests/slice_lib.lua")
L.init{ tag = "PARN", out = "build/test_parnassos/", symbols = "build/test_parnassos/symbols.lua" }
local S, K = L.S, L.K
local emu = L.emu
local log, expect, wait, waitUntil, shot = L.log, L.expect, L.wait, L.waitUntil, L.shot

local LB, R9 = "Lebadeia_EventScript_", "Route9_Schiste_EventScript_"

-- The Ichor bank (and its daily bank right after it) lives in IchorSave.
local function bankFlag(f)
  local o = f - S.ICHOR_FLAGS_START
  local base = emu:read32(S.gSaveBlock3Ptr) + S.OFF_SB3_ICHOR + S.OFF_ICHOR_FLAGS
  return (emu:read8(base + (o >> 3)) >> (o & 7)) & 1 == 1
end
local getFlag1 = L.getFlag
function L.getFlag(f)
  if f >= S.ICHOR_FLAGS_START and f <= S.ICHOR_FLAGS_END then return bankFlag(f) end
  return getFlag1(f)
end

local function metatile(x, y)
  local width = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_WIDTH)
  local map = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_MAP)
  return emu:read16(map + 2 * ((x + S.MAP_OFFSET) + (y + S.MAP_OFFSET) * width)) & 0x3FF
end

-- An ON_FRAME script that sets flags and warps to (x, y) on `map`.
local function warpIn(map, x, y, flags, extra, scene)
  local s = { S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 } }
  for _, b in ipairs(extra or {}) do s[#s + 1] = b end
  for _, f in ipairs(flags or {}) do
    s[#s + 1] = S.SCR_OP_SETFLAG
    s[#s + 1] = { f, 2 }
  end
  for _, b in ipairs({ S.SCR_OP_WARP, map >> 8, map & 0xFF, S.WARP_ID_NONE & 0xFF, { x, 2 }, { y, 2 },
                       S.SCR_OP_WAITSTATE, S.SCR_OP_END }) do
    s[#s + 1] = b
  end
  L.runRamScript(s)
  waitUntil(function() return L.mapId() == map and (scene or L.idle()) end, 4000, "arrival on map " .. map)
  wait(30)
end

-- Push the drum in front of the player one tile (the player stays put).
local function push(key)
  local x0, y0 = L.pos()
  emu:addKey(key); wait(24); emu:clearKey(key); wait(40)
  local x, y = L.pos()
  if x ~= x0 or y ~= y0 then L.fail(string.format("pushing moved the player from (%d,%d)", x0, y0)) end
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

  -- Beat 35B: Lebadeia's east gate. The arrival pan plays on the first frame.
  L.setBeat("35b_lebadeia", false)
  local team = { S.SCR_OP_CALLNATIVE, { S.ScrCmd_createmon | 1, 4 }, 0, S.PARTY_SIZE,
                 { S.SPECIES_TEST, 2 }, { 100, 2 }, { (1 << 17) | (1 << 18) | (1 << 19) | (1 << 20), 4 },
                 { S.MOVE_TEST, 2 }, { S.MOVE_NONE, 2 }, { S.MOVE_NONE, 2 }, { S.MOVE_NONE, 2 },
                 S.SCR_OP_SETVAR, { S.VAR_REPEL_STEP_COUNT, 2 }, { 999, 2 } }
  warpIn(S.MAP_LEBADEIA, 31, 12, { S.FLAG_SYS_POKEMON_GET, S.FLAG_BADGE08_GET, S.FLAG_ACT2_BEGUN, S.FLAG_GIRDLE },
         team, true)
  wait(60)
  shot("lebadeia_arrival_pan")
  L.settle({ shots = { [1] = "alethea_there_you_are" } })
  expect(bankFlag(S.FLAG_VISITED_LEBADEIA), "Lebadeia is visited (its fly flag)")
  expect(metatile(6, 2) == S.METATILE_GRILLE, "the bronze grille is shut")
  shot("lebadeia_east_gate")
  L.go(24, 13); shot("lebadeia_hall_and_river")
  L.go(13, 13); shot("lebadeia_bridge")
  L.talk(L.npc(LB .. "CakeSeller"), { shots = { [1] = "cake_seller" } })
  L.talk(L.ball(S.FLAG_ITEM_LEB_REVIVE), { shots = { [1] = "lebadeia_revive" } })
  expect(bankFlag(S.FLAG_ITEM_LEB_REVIVE), "the Revive on the river bank")
  L.go(4, 9); shot("lebadeia_grove")

  -- Alethea between the two springs.
  local fired = not L.goTrigger(L.triggers(LB .. "SpringsTalk"))
  expect(fired, "the springs talk starts on the pilgrims' steps")
  L.settle({ shots = { [1] = "alethea_notes", [6] = "alethea_lethe", [12] = "alethea_wrong", [16] = "alethea_pilgrims" } })
  expect(bankFlag(S.FLAG_SPRINGS_TALK), "Alethea explained the springs")
  shot("the_precinct")
  L.talk(L.npc(LB .. "Farmer"), { shots = { [2] = "pilgrim_farmer" } })
  L.talk(L.npc(LB .. "Sailor"), { shots = { [1] = "pilgrim_sailor" } })
  L.talk(L.npc(LB .. "OldWoman"), { shots = { [1] = "pilgrim_old_woman" } })
  L.talk(L.npc(LB .. "OldMan"), { shots = { [2] = "old_man_lethe" } })
  L.talk(L.npc(LB .. "Priest"), { shots = { [3] = "priest_chair" } })
  L.talk(L.sign(LB .. "Grille"), { shots = { [2] = "grille_locked" } })
  L.talk(L.hidden(S.FLAG_HIDDEN_ITEM_OBOL), { shots = { [1] = "bronze_obol" } })

  -- Saon: YES, the two drinks, the honey, the grille.
  local honey = L.itemCount(S.ITEM_HONEY)
  L.talk(L.npc(LB .. "Saon"), { answers = { "yes" }, shots = { [3] = "saon_cloth", [6] = "saon_go_down",
                                                                [8] = "drink_lethe", [9] = "drink_mnemosyne" } })
  expect(bankFlag(S.FLAG_GRILLE_OPEN), "Saon opened the grille")
  expect(metatile(6, 2) == S.METATILE_GRILLE_OPEN, "the grille stands open")
  expect(L.itemCount(S.ITEM_HONEY) == honey + 1, "Saon gave the honey for the snakes")
  L.go(6, 3); shot("on_the_chair")
  L.talk(L.sign(LB .. "Mnemosyne"))
  L.go(9, 19); shot("lebadeia_footbridge")
  L.talk(L.npc(LB .. "Child"), { shots = { [2] = "child_goose" } })
  L.go(18, 20); shot("lebadeia_mason")
  L.go(5, 19); shot("lebadeia_herkyna")
  L.go(1, 12); shot("lebadeia_west_road")
  L.leaveEdge("left", S.MAP_ROUTE9)

  -- Beat 36: the Split Road.
  L.setBeat("36_route9", false)
  shot("route9_east")
  expect(bankFlag(S.FLAG_HIDE_ALETHEA_LEBADEIA), "Alethea walked on from Lebadeia")
  L.go(45, 21); shot("route9_koretas")
  expect(L.defeated(S.TRAINER_KORETAS), "Koretas fought by the east sign")
  L.go(45, 19); shot("route9_goats_slope")
  L.go(41, 20); shot("route9_band_a1")
  L.go(38, 20); shot("route9_band_a2")
  L.go(37, 17); shot("route9_cleft")
  expect(L.defeated(S.TRAINER_ONOMARCHOS), "Onomarchos fought in the cleft")

  -- 36A: where three roads meet.
  fired = not L.goTrigger(L.triggers(R9 .. "Crossroads"))
  expect(fired, "the crossroads scene starts on the paving's edge")
  L.settle({ shots = { [1] = "delphoi_from_the_crossroads", [3] = "crossroads_kirrha", [6] = "crossroads_indulge" } })
  expect(bankFlag(S.FLAG_SCHISTE_ARRIVED), "arrived at the Split Road's crossroads")
  shot("the_crossroads")
  L.talk(L.sign(R9 .. "GreatHerm"), { shots = { [1] = "great_herm" } })
  L.talk(L.sign(R9 .. "SignCrossroads"), { shots = { [2] = "split_road_sign" } })
  L.talk(L.npc(R9 .. "OldMan"), { shots = { [1] = "old_man_stone" } })
  L.talk(L.sign(R9 .. "Shrine"), { shots = { [1] = "shrine_scratched" } })
  L.talk(L.npc(R9 .. "Psephos"), { shots = { [1] = "psephos" } })
  expect(L.defeated(S.TRAINER_PSEPHOS), "Psephos fought at the shrine")
  wait(60)
  expect(bankFlag(S.FLAG_HIDE_PSEPHOS) and not L.npc(R9 .. "Psephos").present, "Psephos walked off")
  L.talk(L.sign(R9 .. "Shrine"), { answers = { "yes" }, shots = { [1] = "shrine_cleanse" } })
  expect(bankFlag(S.FLAG_ALTAR_ROUTE9), "Apollo's shrine is cleansed")
  L.talk(L.sign(R9 .. "LaurelTree"), { shots = { [1] = "laurel_sprig" } })
  expect(bankFlag(S.FLAG_DAILY_LAUREL) and L.itemCount(S.ITEM_LAUREL_SPRIG) >= 1, "a Laurel Sprig from the shrine's laurel")

  -- 36B: up the north-west fork to the lookout.
  L.setBeat("36b_lookout", false)
  L.go(27, 13); shot("fork_start")
  L.go(20, 12); shot("fork_switchback")
  L.go(19, 8); shot("fork_corner")
  L.go(21, 8); shot("broken_bridge")
  L.go(14, 8); shot("fork_band")
  fired = not L.goTrigger(L.triggers(R9 .. "Lookout"))
  expect(fired, "the lookout scene starts at the shelf")
  L.settle({ shots = { [1] = "navel_of_the_world", [3] = "no_smoke", [5] = "holding_breath" } })
  expect(bankFlag(S.FLAG_LOOKOUT_SEEN), "Alethea saw Delphoi from the lookout")
  shot("the_lookout")
  L.talk(L.sign(R9 .. "Falls"), { shots = { [1] = "kastalian_falls" } })
  L.talk(L.sign(R9 .. "Cairn"), { shots = { [2] = "cairn_soon" } })
  L.talk(L.npc(R9 .. "Xenodike"), { shots = { [1] = "xenodike_bench" } })
  L.talk(L.ball(S.FLAG_ITEM_MAX_REVIVE), { shots = { [1] = "max_revive" } })
  expect(bankFlag(S.FLAG_ITEM_MAX_REVIVE), "the Max Revive at the lookout's tip")
  -- Pylades's fig (Kirrha's inn gives it): Xenodike comes down.
  warpIn(S.MAP_ROUTE9, 6, 8, { S.FLAG_PYLADES_FIG })
  L.talk(L.npc(R9 .. "Xenodike"), { shots = { [1] = "xenodike_fig", [4] = "xenodike_didnt_need" } })
  expect(bankFlag(S.FLAG_XENODIKE_CAME_DOWN) and bankFlag(S.FLAG_HIDE_XENODIKE), "Xenodike came down")

  -- 36C: the treasury ruin's drums, with the Girdle.
  L.setBeat("36c_treasury", false)
  L.go(21, 23); shot("cutting_top")
  L.go(18, 23)
  L.talk(L.npc("EventScript_StrengthBoulder", 1), { answers = { "yes" }, shots = { [1] = "drum_prompt" } })
  L.face(K.LEFT)
  push(K.LEFT)
  shot("drum_1_on_the_lip")
  local r = L.step(K.LEFT)
  L.settle({ shots = { [1] = "drum_1_rolls" } })
  expect(metatile(15, 23) == S.METATILE_DRUM_GULLY_B, "drum 1 lies in the gully")
  L.go(18, 21); L.face(K.RIGHT)
  push(K.RIGHT)
  shot("drum_2_in_the_alcove")
  L.go(19, 19); L.face(K.LEFT)
  push(K.LEFT)
  r = L.step(K.LEFT)
  L.settle({ shots = { [1] = "drum_3_rolls" } })
  expect(bankFlag(S.FLAG_HIDE_DRUMS), "the treasury's path is open")
  expect(metatile(16, 19) == S.METATILE_DRUM_GULLY, "drum 3 lies in the gully")
  L.go(18, 17); shot("treasury_floor")
  L.talk(L.ball(S.FLAG_ITEM_TM), { shots = { [1] = "tm_in_the_treasury" } })
  L.talk(L.ball(S.FLAG_ITEM_HARD_STONE))
  L.talk(L.sign(R9 .. "TreasuryView"), { shots = { [2] = "view_of_arkadia" } })
  expect(bankFlag(S.FLAG_ITEM_TM) and bankFlag(S.FLAG_ITEM_HARD_STONE), "the treasury's finds")

  -- Down the south-west road: band B2, the terraces, Lykoreus, toward Kirrha.
  L.setBeat("36_southwest", false)
  L.go(22, 30); shot("band_b2")
  expect(L.defeated(S.TRAINER_PHOKOS), "Phokos fought in the cutting")
  expect(L.defeated(S.TRAINER_DAULIS), "Daulis fought beside band B2")
  L.go(18, 33); shot("terrace_path")
  expect(L.defeated(S.TRAINER_LYKOREUS), "Lykoreus fought on the olive terrace")
  L.go(1, 30); shot("west_stair")
  L.talk(L.ball(S.FLAG_ITEM_SUPER_POTION), { shots = { [1] = "terrace_end_potion" } })
  L.go(9, 34)
  L.go(9, 37); shot("band_b3")
  expect(bankFlag(S.FLAG_HIDE_ALETHEA_ROUTE9), "Alethea went on ahead to Kirrha")
  L.go(9, 42); shot("road_to_kirrha")

  -- The omen's visitor: once an augur has told it, an Enigmaw on the stone.
  L.setBeat("omen", false)
  warpIn(S.MAP_ROUTE9, 28, 17, { S.FLAG_OMEN_TOLD })
  expect(L.npc(R9 .. "Enigmaw").present, "the Enigmaw sits on the boundary stone")
  expect(metatile(32, 15) == S.METATILE_ALTAR, "the shrine stays clean")
  shot("enigmaw_on_the_stone")
  log("ok Lebadeia and the Split Road play through")
end

L.start(main)
