-- Arkadia, the Cypress Wood and the Pool, run by tools/ichor/tests/act2_arkadia.sh (read
-- it first).
--
-- Setup touches no ROM data: after Quickstart a test-only event script in spare EWRAM
-- gives a level-60 test Pokémon, sets Act II begun (and prophecy tablet #5 found, so
-- Alethea reads it in beat 43), and arrives on Arkadia's north edge as if from Route 12.
-- Everything after that is key presses: people, signs and triggers are found by the
-- scripts they run (slice_lib.lua).
--
-- Prints "ARKADIA ok ..." per check and "ARKADIA shot ..." per screenshot, and ends with
-- "ARKADIA done"; a failure prints "ARKADIA FAIL: ..." first.

local L = dofile("tools/ichor/tests/slice_lib.lua")
L.init{ tag = "ARKADIA", out = "build/test_arkadia/", symbols = "build/test_arkadia/symbols.lua" }
local S, K = L.S, L.K
local emu = L.emu
local log, expect, wait, waitUntil, shot = L.log, L.expect, L.wait, L.waitUntil, L.shot

local A, W, P = "Arkadia_EventScript_", "Arkadia_CypressWood_EventScript_", "PoolOfMnemosyne_EventScript_"

local function bankFlag(f)
  local o = f - S.ICHOR_FLAGS_START
  local base = emu:read32(S.gSaveBlock3Ptr) + S.OFF_SB3_ICHOR + S.OFF_ICHOR_FLAGS
  return (emu:read8(base + (o >> 3)) >> (o & 7)) & 1 == 1
end
-- slice_lib's walker hides people by their hide flags; Arkadia's are in the Ichor bank.
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

-- The message on screen, decoded (enough of the charset to match lines by).
local CHARS = { [0x00] = " ", [0xAB] = "!", [0xAC] = "?", [0xAD] = ".", [0xAE] = "-", [0xB0] = "...",
                [0xB1] = '"', [0xB2] = '"', [0xB3] = "'", [0xB4] = "'", [0xB8] = ",", [0xBA] = "/",
                [0xF0] = ":", [0xFE] = " ", [0xFA] = " ", [0xFB] = " " }
local function textNow()
  local out = {}
  for i = 0, 1023 do
    local b = emu:read8(S.gStringVar4 + i)
    if b == 0xFF then break end
    local c = CHARS[b]
    if not c then
      if b >= 0xBB and b <= 0xD4 then c = string.char(65 + b - 0xBB)
      elseif b >= 0xD5 and b <= 0xEE then c = string.char(97 + b - 0xD5)
      elseif b >= 0xA1 and b <= 0xAA then c = string.char(48 + b - 0xA1)
      else c = "" end
    end
    out[#out + 1] = c
  end
  return table.concat(out)
end
-- Screenshots by line rather than by box number: settle() looks up shots[box] once per
-- box, and this answers with the first unused cue whose words are on screen.
local function cues(list)
  return setmetatable({}, { __index = function(tbl, box)
    local t = textNow()
    for _, c in ipairs(list) do
      if not c.done and t:find(c[1], 1, true) then c.done = true; rawset(tbl, box, c[2]); return c[2] end
    end
  end })
end

-- An ON_FRAME script that sets flags, runs `extra`, and warps to `map` at (x, y).
local function into(map, x, y, opts)
  opts = opts or {}
  local s = { S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 } }
  for _, b in ipairs(opts.extra or {}) do s[#s + 1] = b end
  for _, f in ipairs(opts.flags or {}) do
    s[#s + 1] = S.SCR_OP_SETFLAG
    s[#s + 1] = { f, 2 }
  end
  for _, b in ipairs({ S.SCR_OP_WARP, map >> 8, map & 0xFF, S.WARP_ID_NONE & 0xFF, { x, 2 }, { y, 2 },
                       S.SCR_OP_WAITSTATE, S.SCR_OP_END }) do
    s[#s + 1] = b
  end
  emu:write16(L.sb1() + S.OFF_SB1_VARS + (S.VAR_TEMP_0 - S.VARS_START) * 2, 0)
  L.runRamScript(s)
  waitUntil(function() return not L.inOverworld() end, 600, string.format("the warp to map %d", map))
  waitUntil(function() return L.mapId() == map and L.inOverworld() end, 4000, string.format("map %d", map))
end

local function main()
  waitUntil(function() return L.now() >= 500 end, 600, "frame 500")
  L.tap(K.START)
  waitUntil(function() return L.now() >= 1020 end, 600, "frame 1020")
  L.tap(K.SELECT)
  waitUntil(L.idle, 4000, "the new game")
  wait(30)
  -- Fast text, Set battle style, no battle animations.
  local opt = L.sb2() + S.OFF_SB2_OPTIONS
  emu:write16(opt, (emu:read16(opt) & ~0x7) | 2 | (1 << 9) | (1 << 10))

  -- ============================================================ beat 41: Arkadia, at dusk
  L.setBeat("41_dusk", false)
  local moves = (1 << 17) | (1 << 18) | (1 << 19) | (1 << 20)
  -- (the eighth badge only so the level-60 test Pokémon obeys: obedience goes by met level)
  into(S.MAP_ARKADIA, 23, 0, {
    flags = { S.FLAG_SYS_POKEMON_GET, S.FLAG_ACT2_BEGUN, S.FLAG_TABLET_5, S.FLAG_BADGE08_GET },
    extra = { S.SCR_OP_CALLNATIVE, { S.ScrCmd_createmon | 1, 4 }, 0, S.PARTY_SIZE,
              { S.SPECIES_TEST, 2 }, { 60, 2 }, { moves, 4 },
              { S.MOVE_TEST, 2 }, { S.MOVE_NONE, 2 }, { S.MOVE_NONE, 2 }, { S.MOVE_NONE, 2 },
              S.SCR_OP_SETVAR, { S.VAR_REPEL_STEP_COUNT, 2 }, { 999, 2 } } })
  expect(metatile(20, 8) == S.METATILE_LAMP_UNLIT_L, "the gate's lamp-trees are dark when you arrive")
  L.settle({ shots = cues{ { "Dusk.", "dusk_card" }, { "Lamps up", "dusk_lamps_up" },
                           { "Six to nothing", "dusk_huntresses" }, { "That was Kleon", "dusk_alethea" },
                           { "Looking for the Lakonian", "dusk_lamplighter" },
                           { "Let's go anyway", "dusk_lets_go" } } })
  shot("dusk_after")
  expect(bankFlag(S.FLAG_ARRIVED) and bankFlag(S.FLAG_VISITED), "Arkadia arrived and a fly target")
  expect(metatile(20, 8) == S.METATILE_LAMP_LIT_L and metatile(27, 8) == S.METATILE_LAMP_LIT_R,
         "the lamplighter lit the gate's lamp-trees")
  expect(metatile(20, 15) == S.METATILE_LAMP_LIT_L, "and the town's are lit")
  expect(L.objectOn(11, 16), "Alethea waits by the Cypress Wood's gate")
  expect(L.objectOn(21, 19) and L.objectOn(22, 19), "the huntresses went on into the square")

  -- ============================================================ the town
  L.setBeat("41_town", false)
  L.go(23, 9); shot("arkadia_gate")
  L.talk(L.sign(A .. "SignForestGate"))
  L.talk(L.hidden(S.FLAG_HIDDEN_REVIVE))
  expect(L.getFlag(S.FLAG_HIDDEN_REVIVE), "the Revive in the hollow cypress by the forest gate")
  L.talk(L.npc("Arkadia_GoatherdHouse_EventScript_LostKid1"), { shots = { [1] = "kid_behind_rock" } })
  expect(bankFlag(S.FLAG_KID_1), "the kid behind the Asclepeion's rock trotted home")
  L.go(15, 12); shot("arkadia_asclepeion")
  -- the third kid plays in front of Pan's grotto, so the grotto waits until it's gone home
  L.talk(L.npc("Arkadia_GoatherdHouse_EventScript_LostKid3"), { shots = { [1] = "kid_at_grotto" } })
  L.talk(L.sign(A .. "PansGrotto"), { shots = { [1] = "pans_grotto" } })
  L.talk(L.npc(A .. "Iamos"), { shots = cues{ { "Watch.", "iamos" }, { "Tomorrow's tomorrow", "iamos_omen" } } })
  L.talk(L.npc(A .. "Kronist"), { shots = cues{ { "wish with a beard", "kronist_hunter" } } })
  L.go(24, 17); shot("arkadia_square")
  L.talk(L.npc(A .. "Huntress1"))
  L.talk(L.npc(A .. "Alethea"), { shots = { [1] = "alethea_at_gate" } })
  L.go(24, 26); shot("arkadia_main_path")
  L.talk(L.npc(A .. "LostGirl"), { answers = { "yes" }, shots = cues{ { "West! By the Wood", "lost_girl_thanks" } } })
  expect(L.getFlag(S.FLAG_DECOY) and L.itemCount(S.ITEM_TINY_MUSHROOM) == 2,
         "the lost girl was told west, and gave two Tiny Mushrooms")
  L.go(20, 34); shot("arkadia_temple_stair")
  L.talk(L.npc("Arkadia_GoatherdHouse_EventScript_LostKid2"), { shots = { [1] = "kid_on_stair" } })
  L.talk(L.npc(A .. "TempleClosed"), { shots = { [1] = "temple_closed" } })
  L.talk(L.sign(A .. "Waterfall"), { shots = { [1] = "waterfall" } })
  L.go(37, 30); shot("arkadia_krotos")
  L.go(40, 24); shot("arkadia_east_road")
  L.talk(L.npc(A .. "Cordon"), { shots = { [1] = "cordon" } })
  L.go(13, 38); shot("arkadia_south_road")
  L.talk(L.npc(A .. "Hoplite"))
  L.go(8, 36); shot("arkadia_west_road")
  L.talk(L.npc(A .. "WestGuard"))

  -- ============================================================ beat 42: the Wood
  L.setBeat("42_wood", false)
  L.useWarp(S.MAP_WOOD)
  waitUntil(function() return L.mapId() == S.MAP_WOOD and L.idle() end, 3000, "the Cypress Wood")
  wait(30)
  shot("wood_gate")
  L.talk(L.sign(W .. "SignGate"))
  L.go(31, 23); shot("wood_band_1")
  L.go(21, 22); shot("wood_corridor")
  L.talk(L.npc(W .. "Euadne"))
  expect(L.defeated(S.TRAINER_EUADNE), "Euadne fought at the narrow")
  local newMoon = L.triggers(W .. "NewMoon")
  expect(not L.goTrigger(newMoon), "the new moon starts at the clearing's mouth")
  L.settle({ shots = cues{ { "Whatever you're going to say", "kleon_dont" },
                           { "And she won anyway", "kleon_six_to_nothing" },
                           { "It was very hard to watch", "iapetos_fades_in" },
                           { "The Titans call me Iapetos", "iapetos_named" },
                           { "Kleon of Lakonia shall slay", "the_tablet" },
                           { "That's forged", "alethea_forged" },
                           { "one that's mine", "kleon_turns" },
                           { "May your thread never be cut", "kleon_takes_tablet" },
                           { "Don't follow me", "kleon_leaves" },
                           { "He didn't believe me", "alethea_alone" },
                           { "You didn't catch her", "the_hound" },
                           { "Grrrff", "skylaps" },
                           { "Three forgeries, one hand", "alethea_list" },
                           { "Show mercy at the new moon", "tablet_mercy" },
                           { "I'm taking it to Astyra", "alethea_astyra" },
                           { "Not-forgetting", "alethea_pool" } } })
  shot("wood_after")
  expect(bankFlag(S.FLAG_KLEON_JOINED), "Kleon went to the Titans (beat 42)")
  expect(bankFlag(S.FLAG_SKYLAPS), "Alethea has Skylaps (beat 43)")
  expect(bankFlag(S.FLAG_TABLET_5_READ), "Alethea read Kallisto's tablet in beat 43")
  expect(not L.objectOn(15, 13), "Kleon is gone from the stump")
  L.talk(L.sign(W .. "Stump"), { shots = { [1] = "the_stump" } })

  -- ============================================================ on to the Pool
  L.setBeat("43_pool", false)
  L.talk(L.hidden(S.FLAG_HIDDEN_CHARCOAL))
  expect(L.getFlag(S.FLAG_HIDDEN_CHARCOAL), "the Charcoal in the kiln's ash")
  shot("wood_kiln")
  L.go(9, 14); shot("wood_band_2")
  L.talk(L.npc(W .. "Lysippe"))
  expect(L.defeated(S.TRAINER_LYSIPPE), "Lysippe fought after band 2")
  L.go(4, 14); shot("wood_west")
  L.talk(L.npc(W .. "Melanippe"))
  expect(L.defeated(S.TRAINER_MELANIPPE), "Melanippe fought on the tomb spur")
  L.talk(L.sign(W .. "SignTomb"))
  L.go(6, 22); shot("wood_tomb")
  L.leaveEdge("left", S.MAP_POOL)
  wait(30)
  shot("pool_arrival")
  L.talk(L.npc(P .. "Mnaseas"), { shots = { [1] = "mnaseas" } })
  expect(bankFlag(S.FLAG_MNASEAS_TOLD), "Mnaseas told the Pool's story")
  L.talk(L.npc(P .. "Mnaseas"), { shots = { [1] = "mnaseas_again" } })
  L.talk(L.sign(P .. "Pool"), { shots = { [1] = "the_pool" } })
  L.go(11, 13); shot("pool_south")

  -- ============================================================ back to Arkadia
  L.setBeat("44_back", false)
  L.leaveEdge("right", S.MAP_WOOD)
  shot("wood_from_pool")
  L.useWarp(S.MAP_ARKADIA)
  waitUntil(function() return L.mapId() == S.MAP_ARKADIA and L.idle() end, 3000, "Arkadia again")
  wait(30)
  shot("arkadia_after")
  expect(not L.objectOn(11, 16), "Alethea has gone on to Astyra")
  L.go(20, 34)
  expect(not L.objectOn(20, 31), "the temple's gate is open")
  shot("temple_open")
  log("done")
end

L.start(main)
