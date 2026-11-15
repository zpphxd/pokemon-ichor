-- Aegina's homes check, run by tools/ichor/tests/aegina_homes.sh (read it first).
--
-- Plays the three rooms as a player would, with key presses, and checks the game's
-- state after each event: the night at the inn (beat 10B), Pheidon's trade at the
-- mint and Aiakides's Black Belt.
--
-- Setup touches no ROM data. After Quickstart, it writes a tiny event script into
-- spare EWRAM and points the current map header's script table at it as an
-- ON_FRAME script (temple_trial.lua's trick): give a Karkipool, set the voyage
-- night's arrival flag and warp into the inn through its door mat. The same trick
-- warps into the other rooms and later gives the Ergant.
--
-- Prints "AEGINA ok ..." per check, "AEGINA shot ..." per screenshot, and ends with
-- "AEGINA done"; any failure prints "AEGINA FAIL: ..." first.

local S = dofile("build/aegina_homes/symbols.lua")
local OUT = "build/aegina_homes/"
local K = { A = C.GBA_KEY.A, B = C.GBA_KEY.B, START = C.GBA_KEY.START, SELECT = C.GBA_KEY.SELECT,
            UP = C.GBA_KEY.UP, DOWN = C.GBA_KEY.DOWN, LEFT = C.GBA_KEY.LEFT, RIGHT = C.GBA_KEY.RIGHT }
local SCRATCH = 0x0203F000  -- spare EWRAM: the linker's EWRAM data ends near 0x02037400

-- The test reads as straight-line code in a coroutine. mGBA only lets its own
-- functions run on the main Lua thread, so the coroutine asks the frame callback
-- to make each call (yield "call") and to advance a frame (yield "frame").
local emu = setmetatable({}, { __index = function(_, name)
  return function(_, ...) return coroutine.yield("call", name, ...) end
end })
local function log(s) coroutine.yield("log", "AEGINA " .. s) end
local function fail(s) error("AEGINA FAIL: " .. s, 0) end
local function frame() coroutine.yield("frame") end
local function wait(n) for _ = 1, n do frame() end end
local function now() return emu:currentFrame() end

-- --- Game state ------------------------------------------------------------------------

local function sb1() return emu:read32(S.gSaveBlock1Ptr) end
local function sb2() return emu:read32(S.gSaveBlock2Ptr) end
local function getFlag(f) return (emu:read8(sb1() + S.OFF_SB1_FLAGS + (f >> 3)) >> (f & 7)) & 1 == 1 end
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
local function on(cb) return callback2() == (S[cb] | 1) end
local function inOverworld() return on("CB2_Overworld") end
local CONTEXT_SHUTDOWN = 2
local function idle()
  return inOverworld()
     and emu:read8(S.sLockFieldControls) == 0
     and emu:read8(S.sGlobalScriptContextStatus) == CONTEXT_SHUTDOWN
     and emu:read8(S.gPlayerAvatar + S.OFF_AVATAR_TILE_TRANSITION) == 0
end
local function boxUp() return emu:read8(S.sFieldMessageBoxMode) ~= 0 end
local function taskRunning(name)
  for i = 0, S.NUM_TASKS - 1 do
    local t = S.gTasks + i * S.TASK_SIZE
    if emu:read8(t + S.OFF_TASK_ACTIVE) ~= 0 and emu:read32(t + S.OFF_TASK_FUNC) == (S[name] | 1) then
      return true
    end
  end
  return false
end
local function hoursOverride() return emu:read16(S.sHoursOverride) end
local function partyMon(slot) return S.gParties + slot * S.POKEMON_SIZE end
local function partyHp(slot)
  local m = partyMon(slot)
  return emu:read16(m + S.OFF_MON_HP), emu:read16(m + S.OFF_MON_MAXHP)
end
local function hurt(slot) emu:write16(partyMon(slot) + S.OFF_MON_HP, 1) end
-- A party Pokémon's nickname, decoded from the game's charset (A-Z only).
local function nickname(slot)
  local s = ""
  for i = 0, 9 do
    local b = emu:read8(partyMon(slot) + S.OFF_MON_NICKNAME + i)
    if b == 0xFF then break end
    if b >= 0xBB and b <= 0xD4 then s = s .. string.char(65 + b - 0xBB) else s = s .. "?" end
  end
  return s
end
-- Whether the current map has a live object with this local id (its map.json index + 1).
local function objectPresent(localId)
  for i = 0, S.NUM_OBJECT_EVENTS - 1 do
    local o = S.gObjectEvents + i * S.OBJECT_EVENT_SIZE
    if emu:read8(o) & 1 == 1 and emu:read8(o + S.OFF_OBJ_LOCAL_ID) == localId then return true end
  end
  return false
end

local function expect(cond, what)
  if not cond then fail(what) end
  log("ok " .. what)
end

-- --- Input -------------------------------------------------------------------------------

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
    if now() - t0 > limit then shot("stuck.png"); fail("timed out waiting for " .. what) end
    frame()
  end
end

-- Press through a script: screenshot every message box as prefix_NN.png before
-- pressing A, and A through fades and fanfares, until `stop()` holds (default:
-- the player is free again for 20 frames). A on a YES/NO prompt answers YES.
local function playThrough(prefix, stop, limit)
  local t0, calm, boxes = now(), 0, 0
  while true do
    if stop and stop() then return boxes end
    if not stop and idle() then
      calm = calm + 1
      if calm >= 20 then return boxes end
      frame()
    else
      calm = 0
      if boxUp() then
        wait(34)                                 -- fast text: a full box prints in this
        if stop and stop() then return boxes end
        if boxUp() then
          boxes = boxes + 1
          shot(string.format("%s_%02d.png", prefix, boxes))
          tap(K.A)
        end
        wait(4)
      else
        if not idle() then tap(K.A) end          -- a fade, a fanfare, a movement
        wait(6)
      end
    end
    if now() - t0 > (limit or 20000) then shot(prefix .. "_stuck.png"); fail("stuck in " .. prefix) end
  end
end

-- One step; fails if blocked.
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
  if x == x0 and y == y0 then fail(string.format("blocked at (%d,%d)", x0, y0)) end
  waitUntil(idle, 120, "the step to end")
end
local function walkTo(points)
  for _, p in ipairs(points) do
    while true do
      local x, y = pos()
      if x == p[1] and y == p[2] then break end
      local key
      if x < p[1] then key = K.RIGHT elseif x > p[1] then key = K.LEFT
      elseif y < p[2] then key = K.DOWN else key = K.UP end
      step(key)
    end
  end
end
-- Turn toward a blocked tile (a person) without moving.
local FACING = { [K.DOWN] = 1, [K.UP] = 2, [K.LEFT] = 3, [K.RIGHT] = 4 }
local function face(key)
  local x0, y0 = pos()
  tap(key, 16)
  wait(10)
  local x, y = pos()
  if x ~= x0 or y ~= y0 then fail("face() moved the player") end
  local facing = emu:read8(playerObject() + 0x18) & 0xF
  if facing ~= FACING[key] then fail(string.format("face() did not turn (facing %d, wanted %d)", facing, FACING[key])) end
end

-- --- Setup scripts in EWRAM ---------------------------------------------------------------

local function bytes(t)
  local out = {}
  for _, v in ipairs(t) do
    if type(v) == "table" then -- { value, size }
      for i = 0, v[2] - 1 do out[#out + 1] = (v[1] >> (8 * i)) & 0xFF end
    else
      out[#out + 1] = v
    end
  end
  return out
end
local function poke(addr, t)
  for i, b in ipairs(bytes(t)) do emu:write8(addr + i - 1, b) end
end
-- Run `script` (a list of byte groups) as the current map's ON_FRAME script.
local function runRamScript(script)
  local tableAddr, frameTable, code = SCRATCH, SCRATCH + 0x20, SCRATCH + 0x40
  local flat = { S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 } }
  for _, b in ipairs(script) do flat[#flat + 1] = b end
  flat[#flat + 1] = S.SCR_OP_END
  poke(code, flat)
  poke(frameTable, { { S.VAR_TEMP_0, 2 }, { 0, 2 }, { code, 4 }, { 0, 2 } })
  poke(tableAddr, { S.MAP_SCRIPT_ON_FRAME_TABLE, { frameTable, 4 }, 0 })
  emu:write32(S.gMapHeader + S.OFF_MAPHEADER_MAPSCRIPTS, tableAddr)
end
local function giveMon(script, species, level)
  for _, b in ipairs({ S.SCR_OP_CALLNATIVE, { S.ScrCmd_createmon | 1, 4 }, 0, S.PARTY_SIZE,
                       { species, 2 }, { level, 2 }, { 0, 4 } }) do
    script[#script + 1] = b
  end
end
-- warp map, 0 (the door mat), then wait for the warp as the expansion requires
local function warpInto(script, map)
  for _, b in ipairs({ S.SCR_OP_WARP, map >> 8, map & 0xFF, 0, { 0xFFFF, 2 }, { 0xFFFF, 2 }, S.SCR_OP_WAITSTATE }) do
    script[#script + 1] = b
  end
  runRamScript(script)
  waitUntil(function() return mapId() == map and idle() end, 4000, "the warp")
  wait(30)
end

-- --- The checks -----------------------------------------------------------------------------

local KLEON, ALETHEA = S.LOCALID_KLEON, S.LOCALID_ALETHEA
local CHELONET, KARKIPOOL = S.LOCALID_CHELONET, S.LOCALID_KARKIPOOL

local function boot()
  waitUntil(function() return now() >= 500 end, 600, "frame 500")
  tap(K.START)
  waitUntil(function() return now() >= 1020 end, 600, "frame 1020")
  tap(K.SELECT)
  waitUntil(idle, 4000, "the new game")
  wait(30)
  -- Fast text, Set battle style, no battle animations.
  local opt = sb2() + S.OFF_SB2_OPTIONS
  emu:write16(opt, (emu:read16(opt) & ~0x7) | 2 | (1 << 9) | (1 << 10))
end

local function inn()
  local setup = { S.SCR_OP_SETFLAG, { S.FLAG_SYS_POKEMON_GET, 2 },
                  S.SCR_OP_SETFLAG, { S.FLAG_ARRIVED_AEGINA, 2 } }
  giveMon(setup, S.SPECIES_KARKIPOOL, 14)
  warpInto(setup, S.MAP_INN)
  local x, y = pos()
  expect(x == 11 and y == 11, "arrived on the inn's door mat")
  expect(hoursOverride() == 22, "the voyage night's tint is re-applied on entry (hour 22)")
  shot("inn_01_courtyard.png")

  walkTo({ { 11, 7 }, { 7, 7 } })
  shot("inn_02_common_room.png")
  walkTo({ { 5, 7 } })
  -- objects spawn only on screen: Kleon and Alethea are in view from here
  expect(objectPresent(KLEON) and objectPresent(ALETHEA), "Kleon and Alethea are by the fire on the voyage night")
  face(K.UP)
  hurt(0)
  tap(K.A)
  wait(10)
  -- Endeis, "Ready for bed?" (YES), the night, up to Kleon's question
  playThrough("inn_03_night", function() return taskRunning("Task_HandleScrollingMultichoiceInput") end)
  wait(20)
  shot("inn_04_question.png")
  tap(K.DOWN); wait(10)
  shot("inn_05_own_business.png")
  tap(K.A); wait(10)
  local x2, y2 = pos()
  expect(x2 == 2 and y2 == 5, "the player sits by the fire for the night")
  -- the second answer, the rest of the night, Kleon up the ladder, goodnight
  -- while no box is up and Kleon is still in the room, he's on his way to the loft
  local shots, last = 0, 0
  local function atDeck()
    if not boxUp() and objectPresent(KLEON) and shots < 8 and now() - last >= 24 then
      shots, last = shots + 1, now()
      shot(string.format("inn_07_kleon_to_loft_%d.png", shots))
    end
    return mapId() == S.MAP_DECK
  end
  playThrough("inn_06_night", atDeck)
  waitUntil(idle, 4000, "the deck")
  wait(30)
  shot("inn_08_deck.png")
  expect(getFlag(S.FLAG_AEGINA_NIGHT), "the night sets FLAG_ICHOR_AEGINA_NIGHT")
  -- the inn clears the night; on deck, beat 10C forces a morning (hour 10)
  local h = hoursOverride()
  expect(h == 0 or h == 10, string.format("the forced night tint is cleared (hour override %d)", h))
  local hp, maxHp = partyHp(0)
  expect(hp == maxHp, string.format("the night heals the party (%d/%d)", hp, maxHp))

  -- A later visit: the night's cast is gone, and Endeis heals.
  warpInto({}, S.MAP_INN)
  expect(hoursOverride() == 0, "no night tint on a later visit")
  walkTo({ { 11, 7 }, { 7, 7 }, { 5, 7 } })
  expect(not objectPresent(KLEON) and not objectPresent(ALETHEA), "Kleon and Alethea are gone after the night")
  face(K.UP)
  hurt(0)
  tap(K.A); wait(10)
  playThrough("inn_09_later_visit")
  hp, maxHp = partyHp(0)
  expect(hp == maxHp, string.format("Endeis heals on a later visit (%d/%d)", hp, maxHp))
  shot("inn_10_later_room.png")
end

local function mint()
  warpInto({}, S.MAP_MINT)
  expect(objectPresent(CHELONET) and not objectPresent(KARKIPOOL), "the Chelonet sits on the anvil before the trade")
  shot("mint_01_room.png")
  walkTo({ { 4, 6 }, { 2, 6 } })
  face(K.UP)
  tap(K.A); wait(10)
  playThrough("mint_02_pheidon", function() return on("CB2_PokeStorage") end)
  wait(90); shot("mint_03_choose_mon.png")
  -- The cursor starts in the jar; up past its name to YOUR PARTY, open the
  -- party, then the Karkipool (the first Pokemon) and SELECT.
  tap(K.UP); wait(20); tap(K.UP); wait(20)
  tap(K.A); wait(60); shot("mint_04_party.png")
  tap(K.A); wait(40); shot("mint_05_select.png")
  tap(K.A); wait(40)
  waitUntil(function() return not on("CB2_PokeStorage") end, 1200, "the storage screen to close")
  waitUntil(function() return not inOverworld() end, 600, "the trade scene")
  local t0, trade = now(), 0
  while not inOverworld() do
    if now() - t0 >= 400 * trade and trade < 5 then
      trade = trade + 1
      shot(string.format("mint_06_trade_%d.png", trade))
    end
    tap(K.A); wait(9)
    if now() - t0 > 12000 then fail("the trade scene never ended") end
  end
  playThrough("mint_07_after")
  expect(getFlag(S.FLAG_TRADED_CHELONET), "the trade sets FLAG_ICHOR_TRADED_CHELONET")
  expect(nickname(0) == "STATER", "the Karkipool's slot now holds STATER (" .. nickname(0) .. ")")
  expect(not objectPresent(CHELONET) and objectPresent(KARKIPOOL), "the Karkipool guards the strongbox after the trade")
  shot("mint_08_guard.png")
  tap(K.A); wait(10)
  playThrough("mint_09_pheidon_after")
  -- Re-entry keeps the guard.
  warpInto({}, S.MAP_MINT)
  expect(not objectPresent(CHELONET) and objectPresent(KARKIPOOL), "the Karkipool is still on guard on re-entry")
end

local function house()
  warpInto({}, S.MAP_HOUSE)
  shot("house_01_room.png")
  walkTo({ { 4, 6 }, { 2, 6 } })
  face(K.UP)
  tap(K.A); wait(10)
  playThrough("house_02_story")
  expect(not getFlag(S.FLAG_GOT_BLACK_BELT), "no Black Belt without an Ergant")
  local give = {}
  giveMon(give, S.SPECIES_ERGANT, 14)
  runRamScript(give)
  wait(30)
  tap(K.A); wait(10)
  playThrough("house_03_black_belt")
  expect(getFlag(S.FLAG_GOT_BLACK_BELT), "Aiakides gives the Black Belt for a look at an Ergant")
  tap(K.A); wait(10)
  playThrough("house_04_after")
end

local co = coroutine.create(function()
  boot()
  inn()
  mint()
  house()
end)

local realEmu = _G.emu
callbacks:add("frame", function()
  if not co then return end
  local result = table.pack(coroutine.resume(co))
  while true do
    if not result[1] then
      local err = tostring(result[2])
      console:log(err:find("^AEGINA FAIL") and err or ("AEGINA FAIL: " .. err))
      console:log("AEGINA done")
      co = nil
      return
    end
    if coroutine.status(co) == "dead" then
      console:log("AEGINA done")
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
