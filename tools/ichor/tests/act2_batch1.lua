-- Batch 1's joins, run by tools/ichor/tests/act2_batch1.sh (read it first).
--
-- Each agent's own test plays its beats on its own maps, mostly arriving by script
-- warp. This one walks the joins between them instead: from Route 6 north across
-- every seam to Thyrsa, in and out of every door on the way, through the theater
-- to the skene, and back south across every seam to Route 6, all by key presses.
--
-- Setup touches no ROM data: after Quickstart, a test-only script in spare EWRAM
-- gives a level-100 Prinplup, the story flags of beats 26-34 (so no first-time
-- scene stands in the way), every batch 1 trainer beaten and a long Repel, then
-- warps to Route 6 above the vines.
--
-- Prints "B1 ok ..." per check and "B1 shot ..." per screenshot, and ends with
-- "B1 done"; a failure prints "B1 FAIL: ..." first.

local OUT = os.getenv("B1_OUT") or "build/test_act2_batch1/"
local L = dofile("tools/ichor/tests/slice_lib.lua")
L.init{ tag = "B1", out = OUT, symbols = OUT .. "symbols.lua" }
local S, K = L.S, L.K
local wait, now, expect, shot, tap = L.wait, L.now, L.expect, L.shot, L.tap
local emu = L.emu

local function warpTo(map, x, y, extra)
  local s = { S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 } }
  for _, b in ipairs(extra or {}) do s[#s + 1] = b end
  for _, b in ipairs({ S.SCR_OP_WARP, map >> 8, map & 0xFF, 0xFF, { x, 2 }, { y, 2 },
                       S.SCR_OP_WAITSTATE, S.SCR_OP_END }) do s[#s + 1] = b end
  L.runRamScript(s)
  L.waitUntil(function() return L.mapId() == map and L.idle() end, 3000, "arrival on map " .. map)
  wait(30)
end

-- In through the door that leads to `room`, check the room, and back out to `home`.
local function visit(room, home, name, inner)
  L.useWarp(room)
  expect(L.mapId() == room, name .. ": its door leads in")
  shot(name)
  if inner then inner() end
  L.useWarp(home)
  expect(L.mapId() == home, name .. ": its way out leads back")
end

-- Off the map's edge into the next map, and check where the player came out.
local function cross(dir, map, name)
  L.leaveEdge(dir, map)
  expect(L.mapId() == map, name)
  shot(name:gsub("[^%w]+", "_"))
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

  local setup = {
    S.SCR_OP_CALLNATIVE, { S.ScrCmd_createmon | 1, 4 }, 0, S.PARTY_SIZE,
    { S.SPECIES_TEST, 2 }, { 100, 2 }, { (1 << 17) | (1 << 18) | (1 << 19) | (1 << 20), 4 },
    { S.MOVE_TEST, 2 }, { S.MOVE_NONE, 2 }, { S.MOVE_NONE, 2 }, { S.MOVE_NONE, 2 },
    S.SCR_OP_SETFLAG, { S.FLAG_SYS_POKEMON_GET, 2 },
    S.SCR_OP_SETFLAG, { S.FLAG_BADGE08_GET, 2 },
    S.SCR_OP_SETFLAG, { S.FLAG_SICKLE, 2 },
    S.SCR_OP_SETFLAG, { S.FLAG_GIRDLE, 2 },
    S.SCR_OP_SETFLAG, { S.FLAG_MASK_LAUREL, 2 },
    S.SCR_OP_SETVAR, { S.VAR_PLAY, 2 }, { S.PLAY_LAUREL_GIVEN, 2 },
    S.SCR_OP_SETVAR, { S.VAR_DIONYSIA, 2 }, { S.DIONYSIA_EMPTY, 2 },
    S.SCR_OP_SETVAR, { S.VAR_REPEL_STEP_COUNT, 2 }, { 999, 2 },
  }
  for i = 0, S.STORY_FLAG_COUNT - 1 do
    setup[#setup + 1] = S.SCR_OP_SETFLAG
    setup[#setup + 1] = { S["STORY_FLAGS_" .. i], 2 }
  end
  for t = S.TRAINER_FIRST, S.TRAINER_LAST do
    setup[#setup + 1] = S.SCR_OP_SETFLAG
    setup[#setup + 1] = { S.TRAINER_FLAGS_START + t, 2 }
  end

  -- North: Route 6, Antiope's cave, Eleutherai and its three houses.
  L.setBeat("north", false)
  warpTo(S.MAP_ROUTE6, 45, 18, setup)
  shot("route6_start")
  visit(S.MAP_CAVE, S.MAP_ROUTE6, "antiopes_cave")
  cross("up", S.MAP_ELEUTHERAI, "route6 to eleutherai")
  visit(S.MAP_WATCH_HOUSE, S.MAP_ELEUTHERAI, "eleutherai_watch_house")
  visit(S.MAP_OINOE_HOUSE, S.MAP_ELEUTHERAI, "eleutherai_oinoe_house")
  visit(S.MAP_LYSIDIKE_HOUSE, S.MAP_ELEUTHERAI, "eleutherai_lysidike_house")
  cross("up", S.MAP_KITHAIRON, "eleutherai to kithairon")
  cross("up", S.MAP_ROUTE7, "kithairon to route7")
  cross("up", S.MAP_THYRSA, "route7 to thyrsa")

  -- Thyrsa: every door, the theater and its skene.
  L.setBeat("thyrsa", false)
  local rooms = {
    { S.MAP_ASCLEPEION, "thyrsa_asclepeion" }, { S.MAP_AGORA, "thyrsa_agora" },
    { S.MAP_TAVERN, "thyrsa_tavern" }, { S.MAP_TEMPLE, "thyrsa_temple" },
    { S.MAP_MASK_WORKSHOP, "thyrsa_mask_workshop" }, { S.MAP_ACTOR_HOUSE, "thyrsa_actor_house" },
    { S.MAP_EUDORA_HOUSE, "thyrsa_eudora_house" }, { S.MAP_MANTO_HOUSE, "thyrsa_manto_house" },
    { S.MAP_PINDAROS_HOUSE, "thyrsa_pindaros_house" }, { S.MAP_SOWN_HOUSE, "thyrsa_sown_house" },
    { S.MAP_VINTNER_HOUSE, "thyrsa_vintner_house" },
  }
  for _, r in ipairs(rooms) do visit(r[1], S.MAP_THYRSA, r[2]) end
  visit(S.MAP_THEATER, S.MAP_THYRSA, "thyrsa_theater", function()
    visit(S.MAP_SKENE, S.MAP_THEATER, "theater_skene")
  end)

  -- South again, across every seam the other way.
  L.setBeat("south", false)
  cross("down", S.MAP_ROUTE7, "thyrsa to route7")
  cross("down", S.MAP_KITHAIRON, "route7 to kithairon")
  cross("down", S.MAP_ELEUTHERAI, "kithairon to eleutherai")
  cross("down", S.MAP_ROUTE6, "eleutherai to route6")

end

L.start(main)
