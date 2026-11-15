-- The Kithairon crossing check, run by tools/ichor/tests/kithairon.sh (read it first).
--
-- Setup touches no ROM data: after Quickstart, a test-only script in spare EWRAM
-- gives a level-100 Prinplup that knows only Surf (and the eighth badge, so it
-- obeys), Demeter's Sickle (the relic stub's flag) and a long Repel, then warps
-- to Route 6 below the vines. From there it plays north with key presses, finding
-- people, signs and triggers by the scripts they run (slice_lib.lua).
--
-- Prints "KITH ok ..." per check and "KITH shot ..." per screenshot, and ends
-- with "KITH done"; a failure prints "KITH FAIL: ..." first.

local OUT = os.getenv("KITH_OUT") or "build/test_kithairon/"
local L = dofile("tools/ichor/tests/slice_lib.lua")
L.init{ tag = "KITH", out = OUT, symbols = OUT .. "symbols.lua" }
local S, K = L.S, L.K
local log, wait, now, expect, shot, tap = L.log, L.wait, L.now, L.expect, L.shot, L.tap
local emu = L.emu

local R6, EL, MK, R7 = "Route6_EleutheraiRoad_EventScript_", "Eleutherai_EventScript_",
  "MtKithairon_EventScript_", "Route7_KroniaGrounds_EventScript_"

-- The crossing's hide flags live in the Ichor bank (IchorSave), which slice_lib's
-- walker can't read on its own: teach it, so people hidden by them (the cut
-- thicket, the herald) stop counting as obstacles.
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

local function warpTo(map, x, y, extra)
  local s = { S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 } }
  for _, b in ipairs(extra or {}) do s[#s + 1] = b end
  for _, b in ipairs({ S.SCR_OP_WARP, map >> 8, map & 0xFF, 0xFF, { x, 2 }, { y, 2 },
                       S.SCR_OP_WAITSTATE, S.SCR_OP_END }) do s[#s + 1] = b end
  L.runRamScript(s)
  L.waitUntil(function() return L.mapId() == map and L.idle() end, 3000, "arrival on map " .. map)
  wait(30)
end

-- A scene that a trigger or a talk has just started: let it run a little,
-- screenshot it mid-way, then play it out.
local function scene(name, frames)
  wait(frames or 90)
  shot(name)
  L.settle()
end

local function main()
  L.setBeat("00_boot", false)
  L.waitUntil(function() return now() >= 500 end, 600, "frame 500")
  tap(K.START)
  L.waitUntil(function() return now() >= 1020 end, 600, "frame 1020")
  tap(K.SELECT)
  L.waitUntil(L.idle, 4000, "the new game")
  wait(30)
  -- Fast text, Set battle style, no battle animations.
  local opt = L.sb2() + S.OFF_SB2_OPTIONS
  emu:write16(opt, (emu:read16(opt) & ~0x7) | 2 | (1 << 9) | (1 << 10))

  -- Beat 26: Route 6, below the vines.
  L.setBeat("26_route6", false)
  warpTo(S.MAP_ROUTE6, 46, 24, {
    S.SCR_OP_CALLNATIVE, { S.ScrCmd_createmon | 1, 4 }, 0, S.PARTY_SIZE,
    { S.SPECIES_TEST, 2 }, { 100, 2 }, { (1 << 17) | (1 << 18) | (1 << 19) | (1 << 20), 4 },
    { S.MOVE_TEST, 2 }, { S.MOVE_NONE, 2 }, { S.MOVE_NONE, 2 }, { S.MOVE_NONE, 2 },
    S.SCR_OP_SETFLAG, { S.FLAG_SYS_POKEMON_GET, 2 },
    S.SCR_OP_SETFLAG, { S.FLAG_BADGE08_GET, 2 },
    S.SCR_OP_SETFLAG, { S.FLAG_SICKLE, 2 },
    S.SCR_OP_SETVAR, { S.VAR_REPEL_STEP_COUNT, 2 }, { 999, 2 },
  })
  shot("route6_south")
  -- The young vines are a thorn thicket in the road's gap (Demeter's Sickle).
  expect(L.objectOn(46, 21), "the young vines grow across the road's gap")
  L.talk(L.npc(R6 .. "Alethea"))
  L.talk(46, 21, { shotBefore = "vines" })
  expect(not L.objectOn(46, 21) and L.getFlag(S.FLAG_HIDE_VINES), "the Sickle cut the thicket, for good")
  shot("vines_cut")
  expect(not L.goTrigger(L.triggers(R6 .. "HeraldScene")), "the herald's scene starts two rows below his barrier")
  scene("herald_scene", 120)
  expect(metatile(45, 18) == S.METATILE_ROAD and metatile(46, 18) == S.METATILE_ROAD, "the barrier is lifted")
  expect(not L.npc(R6 .. "Herald").present and not L.npc(R6 .. "Alethea").present,
         "the herald and Alethea have gone")
  shot("route6_open")
  -- Up the road: Ikarios, the first band, the stair, Pythodoros, the fork.
  L.go(36, 16); shot("route6_vine_terrace")
  expect(L.defeated(S.TRAINER_IKARIOS), "Ikarios fought on the vine terrace")
  L.go(29, 16); shot("route6_band_1")
  L.go(14, 12); shot("route6_stair")
  L.go(18, 9); shot("route6_gap")
  expect(L.defeated(S.TRAINER_PYTHODOROS), "Pythodoros fought at the gap")
  L.go(33, 9); shot("route6_fork")
  L.talk(L.sign(R6 .. "GreatHerm"))
  L.go(46, 9); shot("route6_spur")
  L.go(52, 8); shot("route6_cave_mouth")
  L.go(33, 5); shot("route6_band_3")
  L.go(33, 1); shot("route6_cutting")
  expect(L.defeated(S.TRAINER_ASTYLOS), "Astylos fought in the cutting")
  L.leaveEdge("up", S.MAP_ELEUTHERAI)

  -- Beat 27: Eleutherai, the plinth.
  L.setBeat("27_eleutherai", false)
  shot("eleutherai_arrival")
  L.talk(L.sign(EL .. "Plinth"))
  L.talk(L.npc(EL .. "Alethea"), { shotBefore = "plinth_scene" })
  expect(not L.npc(EL .. "Alethea").present, "Alethea went on north")
  L.go(23, 16); shot("eleutherai_fort_stair")
  L.go(23, 10); shot("eleutherai_fort_court")
  L.go(14, 18); shot("eleutherai_spring")
  L.go(22, 24); shot("eleutherai_pens")
  L.go(10, 1); shot("eleutherai_north")
  L.leaveEdge("up", S.MAP_KITHAIRON)

  -- Beat 28: Mt. Kithairon.
  L.setBeat("28_kithairon", false)
  shot("kithairon_south")
  L.go(8, 50); shot("kithairon_switchback")
  expect(L.defeated(S.TRAINER_LYKIDAS), "Lykidas fought on the first bend")
  L.go(7, 45); shot("kithairon_band_1")
  L.go(15, 41); shot("kithairon_first_cliff")
  expect(not L.goTrigger(L.triggers(MK .. "DancingFloor")), "the maenads' dance starts at the glade's edge")
  scene("dancing_floor", 150)
  shot("dancing_floor_after")
  L.go(24, 29); shot("kithairon_second_cliff")
  expect(L.defeated(S.TRAINER_EUIA), "Euia fought at the glade's only way north")
  L.go(31, 26); shot("kithairon_spring_path")
  L.go(35, 24); shot("aktaions_spring")
  L.go(27, 24); shot("pentheus_fir")
  L.talk(L.npc(MK .. "Phorbas"), { shotBefore = "phorbas" })
  shot("the_fold")
  L.go(35, 8); shot("ivy_shrine")
  L.go(21, 1); shot("kithairon_north_lip")
  L.leaveEdge("up", S.MAP_ROUTE7)

  -- Beat 29: Route 7, the Kronia grounds.
  L.setBeat("29_kronia", false)
  shot("route7_south")
  L.go(20, 30); shot("route7_defile")
  expect(L.defeated(S.TRAINER_KOMOS), "Komos fought in the defile")
  L.go(14, 24); shot("route7_switchbacks")
  L.go(9, 22); shot("route7_meadow")
  expect(L.defeated(S.TRAINER_HAGNON), "Hagnon fought at the last switchback")
  expect(not L.goTrigger(L.triggers(R7 .. "GreeterScene")), "the greeter steps into the road")
  scene("kronia_greeting", 90)
  shot("kronia_camp")
  expect(not L.goTrigger(L.triggers(R7 .. "KleonScene")), "Kleon calls from the tables")
  scene("kleon_at_the_tables", 200)
  expect(not L.npc(R7 .. "Kleon").present, "Kleon jogged off to the gate")
  L.talk(L.npc(R7 .. "Reader"), { shotBefore = "the_reader" })
  expect(not L.npc(R7 .. "Reader").present, "the reader went for someone who reads better")
  L.talk(L.npc(R7 .. "StageKronist"))
  L.go(27, 9); shot("kronia_stage")
  L.go(33, 16); shot("kronia_river")
  L.go(21, 2); shot("route7_north_gate")

  -- Antiope's cave.
  L.setBeat("cave", false)
  warpTo(S.MAP_CAVE, 7, 10)
  shot("antiopes_cave")
  L.talk(L.sign("Route6_AntiopesCave_EventScript_Carving"))
  shot("antiopes_carving")
end

L.start(main)
