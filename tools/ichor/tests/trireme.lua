-- The Euploia check, run by tools/ichor/tests/trireme.sh (read it first).
--
-- Setup touches no ROM data: after Quickstart the test copies trireme_setup.s's
-- assembled blob into spare EWRAM and points the current map header's script
-- table at one of its ON_FRAME headers. The first gives a starter and beat 9B's
-- flags and takes the gangplank's warp (the deck's warp 0); the second sets the
-- night at Aigina's inn and boards again for beat 10C.
--
-- Then, as a player: casting off; a tour of the deck; Kleon, Alethea (no to her
-- practice battle: her trainer id is a stub), the lookout; the Super Potion;
-- down the hatch to the hold, the Lakonian rower and the Potion, and back up;
-- the klepsydra and the hidden Heart Scale; Nausikles and the set piece to the
-- free moment in the calm; the klepsydra running backward; the walk to the bow,
-- the nest, two snatcher battles, the hatching, the chick (taken, not
-- nicknamed), the night leg and the warp to Aigina; then beat 10C and the ferry.
--
-- Prints "TRIREME ok ..." per check and "TRIREME shot ..." per screenshot, and
-- ends with "TRIREME done"; any failure prints "TRIREME FAIL: ..." first.

local S = dofile("build/test_trireme/symbols.lua")
local OUT = os.getenv("TRIREME_OUT") or "build/test_trireme/"
local BLOB_ADDR = tonumber(os.getenv("TRIREME_BLOB_ADDR") or "0x0203F000")
local K = { A = C.GBA_KEY.A, B = C.GBA_KEY.B, START = C.GBA_KEY.START, SELECT = C.GBA_KEY.SELECT,
            UP = C.GBA_KEY.UP, DOWN = C.GBA_KEY.DOWN, LEFT = C.GBA_KEY.LEFT, RIGHT = C.GBA_KEY.RIGHT }

-- The test reads as straight-line code in a coroutine; the frame callback makes
-- each emulator call for it (yield "call") and advances frames (yield "frame").
local emu = setmetatable({}, { __index = function(_, name)
  return function(_, ...) return coroutine.yield("call", name, ...) end
end })
local function log(s) coroutine.yield("log", "TRIREME " .. s) end
local function fail(s) error("TRIREME FAIL: " .. s, 0) end
local function frame() coroutine.yield("frame") end
local function wait(n) for _ = 1, n do frame() end end
local function now() return emu:currentFrame() end

-- --- Game state ------------------------------------------------------------------

local function sb1() return emu:read32(S.gSaveBlock1Ptr) end
local function sb2() return emu:read32(S.gSaveBlock2Ptr) end
local function getFlag(f) return (emu:read8(sb1() + S.OFF_SB1_FLAGS + (f >> 3)) >> (f & 7)) & 1 == 1 end
local function defeated(t) return getFlag(S.TRAINER_FLAGS_START + t) end
local function tempVar1() return emu:read16(sb1() + S.OFF_SB1_VARS + 2 * S.VAR_TEMP_1_INDEX) end
local function partyCount() return emu:read8(S.gPartiesCount) end
local function mapId()
  local loc = sb1() + S.OFF_SB1_LOCATION
  return emu:read8(loc) * 256 + emu:read8(loc + 1)
end
local function playerObject()
  return S.gObjectEvents + emu:read8(S.gPlayerAvatar + S.OFF_AVATAR_OBJECT_EVENT_ID) * S.OBJECT_EVENT_SIZE
end
local function pos()
  local c = playerObject() + S.OFF_OBJ_CURRENT_COORDS
  return emu:read16(c) - S.MAP_OFFSET, emu:read16(c + 2) - S.MAP_OFFSET
end
local function callback2() return emu:read32(S.gMain + S.OFF_MAIN_CALLBACK2) end
local function inOverworld() return callback2() == (S.CB2_Overworld | 1) end
local function inBattle() return callback2() == (S.BattleMainCB2 | 1) end
local CONTEXT_SHUTDOWN = 2
local function idle()
  return inOverworld()
     and emu:read8(S.sLockFieldControls) == 0
     and emu:read8(S.sGlobalScriptContextStatus) == CONTEXT_SHUTDOWN
     and emu:read8(S.gPlayerAvatar + S.OFF_AVATAR_TILE_TRANSITION) == 0
end

local function expect(cond, what)
  if not cond then fail(what) end
  log("ok " .. what)
end

-- --- Input -----------------------------------------------------------------------

local function tap(key, hold)
  emu:addKey(key); wait(hold or 3); emu:clearKey(key); wait(3)
end
local function shot(name)
  emu:screenshot(OUT .. name)
  log("shot " .. name)
end
local function waitUntil(cond, limit, what)
  local t0 = now()
  while not cond() do
    if now() - t0 > limit then fail("timed out waiting for " .. what) end
    frame()
  end
end

-- Wild battles: mash A (Fight, the first move) until back in the overworld.
local battles = 0
local function fightWild(name)
  battles = battles + 1
  wait(420)
  shot(name .. ".png")
  local t0 = now()
  while not inOverworld() do
    tap(K.A); wait(6)
    if now() - t0 > 20000 then fail("battle never ended: " .. name) end
  end
  local outcome = emu:read8(S.gBattleOutcome)
  log(string.format("%s ended, outcome %d", name, outcome))
end

-- Press `key` every 12 frames until the player is free for 20 frames, fighting
-- any wild battle that starts and taking a screenshot every `every` frames.
-- `pick(key)` may change the key as the scene goes (YES with A, NO with B).
local function play(prefix, limit, every, pick)
  local t0, calm, n, nextShot = now(), 0, 0, now() + 20
  local key = K.A
  while calm < 20 do
    if inBattle() then
      fightWild(string.format("%s_battle_%d", prefix, battles + 1))
      calm = 0
    elseif idle() then
      calm = calm + 1
      frame()
    else
      calm = 0
      if every and now() >= nextShot then
        n = n + 1
        shot(string.format("%s_%02d.png", prefix, n))
        nextShot = now() + every
      end
      if pick then key = pick() end
      tap(key)
      wait(6)
    end
    if now() - t0 > (limit or 20000) then fail("stuck in " .. prefix) end
  end
end

-- One step. Returns "moved", "blocked", or "taken" (a script took control).
local function step(key)
  local x0, y0 = pos()
  emu:addKey(key)
  local t0 = now()
  repeat
    frame()
    local x, y = pos()
    if x ~= x0 or y ~= y0 then break end
  until now() - t0 > 40
  emu:clearKey(key)
  local x, y = pos()
  if x == x0 and y == y0 then return "blocked" end
  t0 = now()
  local calm = 0
  while calm < 4 do
    if idle() then calm = calm + 1 else calm = 0 end
    if now() - t0 > 60 then return "taken" end
    frame()
  end
  return "moved"
end
local function walkTo(points)
  for _, p in ipairs(points) do
    while true do
      local x, y = pos()
      if x == p[1] and y == p[2] then break end
      local key
      if x < p[1] then key = K.RIGHT elseif x > p[1] then key = K.LEFT
      elseif y < p[2] then key = K.DOWN else key = K.UP end
      local r = step(key)
      if r ~= "moved" then return r, x, y end
    end
  end
  return "moved"
end
local function walk(points, what)
  local r, x, y = walkTo(points)
  if r ~= "moved" then fail(string.format("%s: %s at (%s,%s)", what, r, tostring(x), tostring(y))) end
end
-- Turn to face a direction without moving (the cell ahead is solid or a person).
local function face(key) tap(key, 2); wait(10) end
local function talk(prefix, every) tap(K.A); wait(4); play(prefix, 6000, every or 40) end

-- --- The injected scripts ----------------------------------------------------------

local blob = {}
do
  local f = assert(io.open("build/test_trireme/setup.bin", "rb"))
  local data = f:read("a")
  f:close()
  for i = 1, #data do blob[i] = data:byte(i) end
  local syms = {}
  for line in io.lines("build/test_trireme/setup.syms") do
    local name, hex = line:match("^(%S+) (%x+)$")
    if name then syms[name] = tonumber(hex, 16) end
  end
  S.blob = syms
end
local function loadBlob()
  for i, b in ipairs(blob) do emu:write8(BLOB_ADDR + i - 1, b) end
end
local function run(header)
  emu:write32(S.gMapHeader + S.OFF_MAPHEADER_MAPSCRIPTS, S.blob[header])
end

-- --- The test ---------------------------------------------------------------------

local function main()
  waitUntil(function() return now() >= 500 end, 600, "frame 500")
  tap(K.START)
  waitUntil(function() return now() >= 1020 end, 600, "frame 1020")
  tap(K.SELECT)
  waitUntil(idle, 4000, "the new game")
  wait(30)
  local opt = sb2() + S.OFF_SB2_OPTIONS
  emu:write16(opt, (emu:read16(opt) & ~0x7) | 2 | (1 << 9) | (1 << 10))

  -- Up the gangway: the deck's warp 0, with beat 9B's flags
  loadBlob()
  run("TriremeTest_SetupHeader")
  waitUntil(function() return mapId() == S.MAP_DECK end, 3000, "the deck")
  wait(40)
  shot("01_boarding.png")
  local x, y = pos()
  expect(x == 13 and y == 4, string.format("the gangplank puts the player at (13,4) (at %d,%d)", x, y))
  play("02_cast_off", 4000, 30)
  shot("03_under_sail.png")

  -- Kleon at the starboard rail, from (8,4)
  walk({ { 8, 4 } }, "to Kleon")
  face(K.LEFT)
  talk("04_kleon")
  -- Alethea by the mast, from (10,8); no to the practice battle (stub trainer)
  walk({ { 9, 4 }, { 9, 8 }, { 10, 8 } }, "to Alethea")
  face(K.UP)
  tap(K.A); wait(4)
  -- yes to her practice battle (A); the battle is fought as it comes
  play("05_alethea", 12000, 40)
  expect(getFlag(S.FLAG_BATTLED_ALETHEA) and defeated(S.TRAINER_ALETHEA),
         "Alethea's practice battle is fought and FLAG_ICHOR_BATTLED_ALETHEA_DECK set")
  -- Lykon by the bow cargo, facing away: talked to from (8,8)
  walk({ { 9, 8 }, { 8, 8 } }, "to Lykon")
  face(K.LEFT)
  talk("05_lykon")
  expect(defeated(S.TRAINER_LYKON), "Lykon is beaten when talked to")
  -- The Super Potion among the bow cargo, from (4,6)
  walk({ { 8, 6 }, { 4, 6 } }, "to the bow cargo")
  face(K.UP)
  talk("06_super_potion")
  expect(getFlag(S.FLAG_ITEM_SUPER_POTION), "the Super Potion is found among the bow cargo")
  -- the lookout at the bow
  walk({ { 3, 6 } }, "to the lookout")
  face(K.LEFT)
  talk("07_lookout")
  shot("08_bow.png")

  -- Down the hatch to the hold
  walk({ { 3, 6 }, { 13, 6 }, { 13, 7 } }, "to the hatch")
  local r = step(K.RIGHT)
  waitUntil(function() return mapId() == S.MAP_HOLD and idle() end, 600, "the hold")
  wait(20)
  x, y = pos()
  expect(x == 11 and y == 5, string.format("the hatch comes down the ladder at (11,5) (at %d,%d)", x, y))
  shot("10_hold.png")
  walk({ { 12, 5 }, { 13, 5 } }, "to the Lakonian rower")
  face(K.UP)
  talk("11_lakonian_rower")
  walk({ { 13, 6 }, { 9, 6 }, { 9, 5 }, { 7, 5 }, { 7, 6 }, { 3, 6 } }, "to the bottom bench")
  face(K.DOWN)
  talk("12_hold_potion")
  expect(getFlag(S.FLAG_ITEM_HOLD_POTION), "the Potion is found under the bottom bench")
  shot("13_hold_bow_end.png")
  walk({ { 7, 6 }, { 7, 5 }, { 10, 5 } }, "back to the ladder")
  step(K.RIGHT)
  waitUntil(function() return mapId() == S.MAP_DECK and idle() end, 600, "the deck again")
  wait(20)
  x, y = pos()
  expect(x == 14 and y == 7, string.format("the ladder comes up through the hatch at (14,7) (at %d,%d)", x, y))
  shot("14_up_the_hatch.png")

  -- Aft past Phormion: his sight spans the deck at x = 16
  r = walkTo({ { 14, 6 }, { 18, 6 } })
  expect(r == "taken", "Phormion stops the player crossing the deck at x = 16")
  play("15_phormion", 12000, 40)
  expect(defeated(S.TRAINER_PHORMION), "Phormion is beaten")
  -- The klepsydra, from (19,5); the Heart Scale in the coil, from (18,8)
  walk({ { 18, 6 }, { 18, 5 }, { 19, 5 } }, "to the klepsydra")
  face(K.UP)
  talk("16_klepsydra")
  walk({ { 18, 5 }, { 18, 8 } }, "to the coil")
  face(K.DOWN)
  talk("17_heart_scale")
  expect(getFlag(S.FLAG_HIDDEN_HEART_SCALE), "the Heart Scale is hidden in the stern's rope coil")

  -- Nausikles at the helm, from (18,7): the set piece, to the free moment
  walk({ { 18, 7 } }, "to Nausikles")
  face(K.RIGHT)
  tap(K.A); wait(4)
  play("20_calm", 20000, 60)
  expect(tempVar1() == 2, "the calm leaves the player free, waiting for the bow")
  shot("21_calm_free.png")
  -- the klepsydra runs backward, from (19,5)
  walk({ { 19, 5 } }, "to the klepsydra in the calm")
  face(K.UP)
  tap(K.A); wait(30)
  shot("22_klepsydra_upward.png")
  play("22_klepsydra_upward", 3000)
  -- the hatch is blocked: Kleon is on it, keeping the stroke
  walk({ { 18, 5 }, { 15, 5 }, { 14, 6 } }, "past the hatch")
  shot("23_kleon_on_hatch.png")
  expect(step(K.DOWN) == "blocked", "Kleon on the hatch keeps the player out of the hold in the calm")
  -- to the bow: the trigger line at x = 8
  r = walkTo({ { 9, 6 }, { 8, 6 } })
  expect(r == "taken", "crossing x = 8 in the calm walks the player to the bow")

  -- The nest: battles, the hatching, the chick (yes), no nickname, the night
  play("30_nest", 60000, 45, function()
    if getFlag(S.FLAG_GOT_HALCYLING) then return K.B end
    return K.A
  end)
  -- play() returns when the player is free: on Aigina's quay
  waitUntil(function() return mapId() == S.MAP_AEGINA and idle() end, 3000, "Aigina's quay")
  shot("40_aigina_quay.png")
  expect(battles == 5, string.format("three trainer battles and two snatchers (%d)", battles))
  expect(getFlag(S.FLAG_SAVED_NEST), "the nest is saved")
  expect(getFlag(S.FLAG_GOT_HALCYLING) and partyCount() == 2, "the Halcyling joins the party")
  expect(not getFlag(S.FLAG_NO_WHITEOUT) and not getFlag(S.FLAG_NO_RUNNING),
         "the snatcher battles' flags are cleared")

  -- Beat 10C: the morning after the inn
  loadBlob()
  run("TriremeTest_LastLegHeader")
  waitUntil(function() return mapId() == S.MAP_DECK end, 3000, "the deck in the morning")
  wait(30)
  shot("50_last_leg_arrive.png")
  play("51_last_leg", 8000, 40)
  expect(getFlag(S.FLAG_CROSSING_DONE), "the last leg sets FLAG_ICHOR_CROSSING_DONE")
  -- the Euploia makes Emporion: beat 11 on the quay is emporion.sh's
  waitUntil(function() return mapId() == S.MAP_EMPORION_HARBOR end, 3000, "Emporion's quay")
  shot("52_emporion_quay.png")
end

local co = coroutine.create(main)
local realEmu = _G.emu
callbacks:add("frame", function()
  if not co then return end
  local result = table.pack(coroutine.resume(co))
  while true do
    if not result[1] then
      local err = tostring(result[2])
      console:log(err:find("^TRIREME FAIL") and err or ("TRIREME FAIL: " .. err))
      console:log("TRIREME done")
      co = nil
      return
    end
    if coroutine.status(co) == "dead" then
      console:log("TRIREME done")
      co = nil
      return
    end
    local kind = result[2]
    if kind == "frame" then return end
    if kind == "log" then
      console:log(result[3])
      result = table.pack(coroutine.resume(co))
    else -- "call"
      local fn = realEmu[result[3]]
      result = table.pack(coroutine.resume(co, fn(realEmu, table.unpack(result, 4, result.n))))
    end
  end
end)
