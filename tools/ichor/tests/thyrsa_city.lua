-- Thyrsa City check, run by tools/ichor/tests/thyrsa_city.sh (read it first).
--
-- Setup touches no ROM data: after Quickstart a test-only event script in spare
-- EWRAM gives a team and Act II's flags, marks the city's three trainers beaten
-- (they are ordinary trainers; this run is about the city's scenes), and warps onto
-- the road below the Elektran Gate. Then everything is played with key presses.

local L = dofile("tools/ichor/tests/slice_lib.lua")
L.init{ tag = "THYRSA", out = "build/test_thyrsa/", symbols = "build/test_thyrsa/symbols.lua" }
local S, K = L.S, L.K
local emu = L.emu
local log, expect, wait, waitUntil, shot = L.log, L.expect, L.wait, L.waitUntil, L.shot

local function bankFlag(f)
  local o = f - S.ICHOR_FLAGS_START
  local base = emu:read32(S.gSaveBlock3Ptr) + S.OFF_SB3_ICHOR + S.OFF_ICHOR_FLAGS
  return (emu:read8(base + (o >> 3)) >> (o & 7)) & 1 == 1
end
-- slice_lib's walker hides people by their hide flags; Thyrsa's are in the Ichor bank.
local getFlag1 = L.getFlag
function L.getFlag(f)
  if f >= S.ICHOR_FLAGS_START and f <= S.ICHOR_FLAGS_END then return bankFlag(f) end
  return getFlag1(f)
end

-- An ON_FRAME script that sets flags and warps into Thyrsa at (x, y).
local function warpIn(x, y, flags, extra)
  local s = { S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 } }
  for _, b in ipairs(extra or {}) do s[#s + 1] = b end
  for _, f in ipairs(flags or {}) do
    s[#s + 1] = S.SCR_OP_SETFLAG
    s[#s + 1] = { f, 2 }
  end
  local map = S.MAP_THYRSA_CITY
  for _, b in ipairs({ S.SCR_OP_WARP, map >> 8, map & 0xFF, S.WARP_ID_NONE & 0xFF, { x, 2 }, { y, 2 },
                       S.SCR_OP_WAITSTATE, S.SCR_OP_END }) do
    s[#s + 1] = b
  end
  L.runRamScript(s)
  waitUntil(function() return L.mapId() == S.MAP_THYRSA_CITY and L.idle() end, 4000, "Thyrsa City")
  wait(30)
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

  L.setBeat("arrival", false)
  local team = { S.SCR_OP_CALLNATIVE, { S.ScrCmd_createmon | 1, 4 }, 0, S.PARTY_SIZE,
                 { S.SPECIES_TEST, 2 }, { 60, 2 }, { (1 << 17) | (1 << 18) | (1 << 19) | (1 << 20), 4 },
                 { S.MOVE_TEST, 2 }, { S.MOVE_NONE, 2 }, { S.MOVE_NONE, 2 }, { S.MOVE_NONE, 2 } }
  warpIn(27, 44, { S.FLAG_SYS_POKEMON_GET, S.FLAG_BADGE08_GET, S.FLAG_ACT2_BEGUN,
                   S.TRAINER_FLAGS_START + S.TRAINER_OINOPION, S.TRAINER_FLAGS_START + S.TRAINER_LENAIA,
                   S.TRAINER_FLAGS_START + S.TRAINER_HEGELOCHOS }, team)
  expect(not bankFlag(S.FLAG_ARRIVED), "not yet arrived on the road")
  shot("road_to_the_gate")
  L.go(27, 41)
  shot("the_elektran_gate")

  -- Beat 30: through the gate, the gatekeeper's welcome.
  local fired = not L.goTrigger(L.triggers("ThyrsaCity_EventScript_ArrivalX26", "ThyrsaCity_EventScript_ArrivalX27",
                                           "ThyrsaCity_EventScript_ArrivalX28", "ThyrsaCity_EventScript_ArrivalX29"))
  expect(fired, "the gatekeeper's welcome starts inside the gate")
  L.settle({ shots = { [1] = "gatekeeper_seven_gates", [6] = "gatekeeper_masks" } })
  expect(bankFlag(S.FLAG_ARRIVED) and bankFlag(S.FLAG_VISITED), "arrived in Thyrsa (both flags)")
  shot("after_the_welcome")

  -- The tour, district by district.
  L.setBeat("tour", false)
  L.go(25, 32); shot("lower_town")
  L.talk(L.npc("ThyrsaCity_EventScript_Beggar"), { shots = { [1] = "beggar" } })
  expect(bankFlag(S.FLAG_DECOY), "the beggar's spring: a Pecha Berry")
  L.go(21, 32); shot("asclepeion")
  L.go(27, 24); shot("the_square")
  L.talk(L.npc("ThyrsaCity_EventScript_Herald"), { shots = { [1] = "herald" } })
  L.go(27, 15); shot("the_kadmeia_stair")
  L.go(27, 10); shot("temple_of_dionysus")
  L.go(15, 8); shot("semele")
  L.talk(L.npc("ThyrsaCity_EventScript_Alethea"), { shots = { [1] = "alethea_semele" } })
  L.talk(L.sign("ThyrsaCity_EventScript_SemeleCrack"), { shots = { [1] = "semele_crack" } })
  L.talk(L.npc("ThyrsaCity_EventScript_Manto"), { shots = { [1] = "manto_footsteps", [7] = "manto_listens",
                                                             [11] = "manto_omen" } })
  expect(bankFlag(S.FLAG_MET_MANTO), "met Manto on the wall")
  L.go(39, 11); shot("manto_house")
  L.go(38, 17); shot("theater_terrace")
  local stopped = not L.goTrigger(L.triggers("ThyrsaCity_EventScript_TheaterKeeperStop"))
  expect(stopped, "the theater keeper turns a player without a laurel away")
  L.settle({ shots = { [1] = "theater_keeper" } })
  L.go(40, 24); shot("polos_and_euthykles")
  L.go(40, 31); shot("the_lanes")
  L.go(44, 31); shot("proitid_gate")
  L.talk(L.npc("ThyrsaCity_EventScript_ProitidGuard"), { shots = { [1] = "proitid_guard" } })
  L.go(39, 36); shot("eudora")
  L.go(19, 24); shot("vineyards")
  L.go(12, 24); shot("neistan_lane")
  L.talk(L.npc("ThyrsaCity_EventScript_NeistanGuard"), { shots = { [1] = "neistan_festival" } })
  L.go(14, 36); shot("old_trellises")

  -- After the Dionysia, with the Girdle: the drum, and Alethea going west.
  L.setBeat("west_gate", false)
  warpIn(14, 24, { S.FLAG_DIONYSIA_DONE, S.FLAG_GIRDLE, S.FLAG_BADGE04_GET })
  shot("the_fallen_drum")
  L.talk(L.npc("ThyrsaCity_EventScript_NeistanGuard", 2), { shots = { [1] = "guards_drum" } })
  L.talk(L.npc("ThyrsaCity_EventScript_NeistanDrum"),
         { answers = { "yes" }, shots = { [2] = "drum_pushed", [6] = "alethea_west", [14] = "alethea_cursed" } })
  expect(bankFlag(S.FLAG_DRUM_MOVED), "the drum is out of the gate")
  expect(bankFlag(S.FLAG_ALETHEA_WENT_WEST), "Alethea went west")
  shot("gate_open")
  L.go(5, 24); shot("the_road_west")

  -- Manto's omen after the Dionysia: the visitor in the old vines.
  L.setBeat("omen", false)
  L.go(27, 14)
  L.talk(L.npc("ThyrsaCity_EventScript_Manto"), { shots = { [2] = "omen_visitor" } })
  expect(bankFlag(S.FLAG_OMEN_TOLD), "Manto told the rare visitor")
  L.go(14, 36); shot("thyrsivy_in_the_vines")
  log("ok the city plays through")
end

L.start(main)
