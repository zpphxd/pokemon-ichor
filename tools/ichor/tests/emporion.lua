-- Emporion's check, run by tools/ichor/tests/emporion.sh (read it first).
--
-- Plays the city and the harbor district as a player would, with key presses,
-- and checks the game's state after each event. Setup touches no ROM data: after
-- Quickstart it writes a tiny event script into spare EWRAM and points the current
-- map header's script table at it as an ON_FRAME script (aegina_homes.lua's trick).
--
-- Prints "EMPORION ok ..." per check, "EMPORION shot ..." per screenshot, and ends
-- with "EMPORION done"; any failure prints "EMPORION FAIL: ..." first.

local S = dofile("build/emporion_test/symbols.lua")
S.HandleInputChooseAction = dofile("build/emporion_test/battle_symbols.lua").HandleInputChooseAction
local OUT = "build/emporion_test/"
local K = { A = C.GBA_KEY.A, B = C.GBA_KEY.B, START = C.GBA_KEY.START, SELECT = C.GBA_KEY.SELECT,
            UP = C.GBA_KEY.UP, DOWN = C.GBA_KEY.DOWN, LEFT = C.GBA_KEY.LEFT, RIGHT = C.GBA_KEY.RIGHT }
local SCRATCH = 0x0203F000  -- spare EWRAM: the linker's EWRAM data ends near 0x02037400

local emu = setmetatable({}, { __index = function(_, name)
  return function(_, ...) return coroutine.yield("call", name, ...) end
end })
local function log(s) coroutine.yield("log", "EMPORION " .. s) end
local function fail(s) error("EMPORION FAIL: " .. s, 0) end
local function frame() coroutine.yield("frame") end
local function wait(n) for _ = 1, n do frame() end end
local function now() return emu:currentFrame() end

-- --- Game state ------------------------------------------------------------------------

local function sb1() return emu:read32(S.gSaveBlock1Ptr) end
local function sb2() return emu:read32(S.gSaveBlock2Ptr) end
local function ichor() return emu:read32(S.gSaveBlock3Ptr) + S.OFF_SB3_ICHOR end
-- Any flag, wherever it is saved: SaveBlock1 or IchorSave's bank.
local function getFlag(f)
  if f >= S.ICHOR_FLAGS_START and f <= S.ICHOR_FLAGS_END then
    local o = f - S.ICHOR_FLAGS_START
    return (emu:read8(ichor() + S.OFF_ICHOR_FLAGS + (o >> 3)) >> (o & 7)) & 1 == 1
  end
  if f >= S.ICHOR_DAILY_FLAGS_START and f <= S.ICHOR_DAILY_FLAGS_END then
    local o = f - S.ICHOR_DAILY_FLAGS_START
    return (emu:read8(ichor() + S.OFF_ICHOR_DAILY_FLAGS + (o >> 3)) >> (o & 7)) & 1 == 1
  end
  return (emu:read8(sb1() + S.OFF_SB1_FLAGS + (f >> 3)) >> (f & 7)) & 1 == 1
end

local function writeFlag(f, value)
  local offset, base
  if f >= S.ICHOR_FLAGS_START and f <= S.ICHOR_FLAGS_END then
    offset, base = f - S.ICHOR_FLAGS_START, ichor() + S.OFF_ICHOR_FLAGS
  elseif f >= S.ICHOR_DAILY_FLAGS_START and f <= S.ICHOR_DAILY_FLAGS_END then
    offset, base = f - S.ICHOR_DAILY_FLAGS_START, ichor() + S.OFF_ICHOR_DAILY_FLAGS
  else
    offset, base = f, sb1() + S.OFF_SB1_FLAGS
  end
  local address = base + (offset >> 3)
  local mask = 1 << (offset & 7)
  local byte = emu:read8(address)
  emu:write8(address, value and (byte | mask) or (byte & ~mask))
end

local function itemCount(item)
  local key = emu:read32(sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
  local count = 0
  for i = 0, S.BAG_SLOTS - 1 do
    local slot = sb1() + S.OFF_SB1_BAG + i * S.ITEM_SLOT_SIZE
    if emu:read16(slot) == item then
      count = count + (emu:read16(slot + S.OFF_ITEM_SLOT_QUANTITY) ~ key)
    end
  end
  return count
end

local function money()
  return emu:read32(sb1() + S.OFF_SB1_MONEY) ~ emu:read32(sb2() + S.OFF_SB2_ENCRYPTION_KEY)
end
local function setMoney(amount)
  emu:write32(sb1() + S.OFF_SB1_MONEY, amount ~ emu:read32(sb2() + S.OFF_SB2_ENCRYPTION_KEY))
end
local function addCoinFixture(item)
  local encryptionKey = emu:read32(sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
  for i = 0, S.BAG_ITEMS_COUNT - 1 do
    local slot = sb1() + S.OFF_SB1_BAG + i * S.ITEM_SLOT_SIZE
    if emu:read16(slot) == 0 then
      emu:write16(slot, item)
      emu:write16(slot + S.OFF_ITEM_SLOT_QUANTITY, 1 ~ encryptionKey)
      return
    end
  end
  fail("no empty item slot for the coin fixture")
end

local function mapId()
  local loc = sb1() + S.OFF_SB1_LOCATION
  return emu:read8(loc) * 256 + emu:read8(loc + 1)
end

local function saveBag()
  local slots = {}
  local encryptionKey = emu:read32(sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
  for i = 0, S.BAG_SLOTS - 1 do
    local slot = sb1() + S.OFF_SB1_BAG + i * S.ITEM_SLOT_SIZE
    slots[i] = { emu:read16(slot), emu:read16(slot + S.OFF_ITEM_SLOT_QUANTITY) ~ encryptionKey }
  end
  return slots, function()
    local currentKey = emu:read32(sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
    for i = 0, S.BAG_SLOTS - 1 do
      local slot = sb1() + S.OFF_SB1_BAG + i * S.ITEM_SLOT_SIZE
      emu:write16(slot, slots[i][1])
      emu:write16(slot + S.OFF_ITEM_SLOT_QUANTITY, slots[i][2] ~ currentKey)
    end
  end
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
local function inBattle() return on("BattleMainCB2") end
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
local function multichoice() return taskRunning("Task_HandleScrollingMultichoiceInput") end
-- Whether the current map has a live object with this local id.
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

-- A battle that has started (or is starting) is played with A: FIGHT and the
-- first move. The test Pokémon is strong enough that Kleon's battle ends.
local function playBattle(name)
  waitUntil(inBattle, 1500, "the battle to start (" .. name .. ")")
  wait(400)
  shot(name)
  local t0, n = now(), 0
  while not inOverworld() do
    tap(K.A); wait(6)
    if now() - t0 > 300 * (n + 1) and n < 3 then
      n = n + 1
      shot(string.format("%s_%d.png", name:gsub("%.png$", ""), n))
    end
    if now() - t0 > 30000 then shot(name .. "_stuck.png"); fail("battle never ended: " .. name) end
  end
  log(string.format("battle %s outcome %d", name, emu:read8(S.gBattleOutcome)))
  return emu:read8(S.gBattleOutcome)
end

-- Press through a script: screenshot every message box as prefix_NN.png before
-- pressing A, and A through fades and fanfares, until `stop()` holds (default:
-- the player is free again for 20 frames). A on a YES/NO prompt answers YES; a
-- battle that starts is played to its end.
local function playThrough(prefix, stop, limit)
  local t0, calm, boxes = now(), 0, 0
  while true do
    if stop and stop() then return boxes end
    if inBattle() then playBattle(prefix .. "_battle.png") end
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

-- One step; returns false if something (a wandering person) is in the way.
local function tryStep(key)
  local x0, y0 = pos()
  emu:addKey(key)
  local t0 = now()
  repeat
    frame()
    local x, y = pos()
    if x ~= x0 or y ~= y0 or boxUp() then break end
  until now() - t0 > 40
  emu:clearKey(key)
  waitUntil(function() return idle() or boxUp() end, 300, "the step or field message")
  if boxUp() then playThrough("walking_message") end
  local x, y = pos()
  return x ~= x0 or y ~= y0
end
local function step(key)
  if not tryStep(key) then
    local x, y = pos()
    shot("blocked.png"); fail(string.format("blocked at (%d,%d) on map %d", x, y, mapId()))
  end
end

-- Walk to each point in turn by the shortest open path on the builders' walk
-- grids (emporion_grids.py), stepping round anyone who wanders into the way.
local G = dofile("build/emporion_test/grids.lua")
local function gridFor()
  if mapId() == S.MAP_CITY then return G.MAP_CITY elseif mapId() == S.MAP_HARBOR then return G.MAP_HARBOR end
  fail("no walk grid for map " .. mapId())
end
local function isOpen(g, x, y)
  return y >= 0 and y < #g and x >= 0 and x < #g[1] and g[y + 1]:sub(x + 1, x + 1) == "."
end
local function key(x, y) return y * 1000 + x end
local function path(tx, ty, avoid)
  local g = gridFor()
  local sx, sy = pos()
  local prev, q, head = { [key(sx, sy)] = false }, { { sx, sy } }, 1
  for k in pairs(avoid or {}) do prev[k] = prev[k] == nil and { 0, 0, 0 } or prev[k] end
  while head <= #q do
    local x, y = q[head][1], q[head][2]
    head = head + 1
    if x == tx and y == ty then
      local steps, k = {}, key(x, y)
      while prev[k] do
        table.insert(steps, 1, prev[k][3])
        k = key(prev[k][1], prev[k][2])
      end
      return steps
    end
    for _, d in ipairs({ { 1, 0, K.RIGHT }, { -1, 0, K.LEFT }, { 0, 1, K.DOWN }, { 0, -1, K.UP } }) do
      local nx, ny = x + d[1], y + d[2]
      if prev[key(nx, ny)] == nil and isOpen(g, nx, ny) then
        prev[key(nx, ny)] = { x, y, d[3] }
        q[#q + 1] = { nx, ny }
      end
    end
  end
  if avoid and next(avoid) then return nil end    -- try again without the detour
  fail(string.format("no path from (%d,%d) to (%d,%d) on map %d", sx, sy, tx, ty, mapId()))
end
-- A cell someone wandered into is avoided on the next try; the next try after
-- that forgets it again, since wanderers move on.
local STEP = { [K.RIGHT] = { 1, 0 }, [K.LEFT] = { -1, 0 }, [K.DOWN] = { 0, 1 }, [K.UP] = { 0, -1 } }
local function goTo(tx, ty)
  local avoid = {}
  for try = 1, 10 do
    local x, y = pos()
    if x == tx and y == ty then return end
    local blocked, destinationBlocked = false, false
    local steps = path(tx, ty, try % 3 ~= 0 and avoid or {}) or path(tx, ty, {})
    for _, k in ipairs(steps) do
      if not tryStep(k) then
        blocked = true
        local bx, by = pos()
        local d = STEP[k]
        destinationBlocked = bx + d[1] == tx and by + d[2] == ty
        if not destinationBlocked then avoid[key(bx + d[1], by + d[2])] = true end
        break
      end
    end
    if not blocked then return end
    if destinationBlocked then
      -- Give a walker room to leave the destination instead of pinning it there.
      for _, k in ipairs({ K.DOWN, K.RIGHT, K.LEFT, K.UP }) do
        local bx, by = pos()
        local d = STEP[k]
        if isOpen(gridFor(), bx + d[1], by + d[2])
           and not (bx + d[1] == tx and by + d[2] == ty)
           and tryStep(k) then break end
      end
    end
    wait(30)
  end
  local x, y = pos()
  shot("blocked.png"); fail(string.format("could not reach (%d,%d) from (%d,%d)", tx, ty, x, y))
end
local function walkTo(points)
  for _, p in ipairs(points) do goTo(p[1], p[2]) end
end
-- Turn toward a blocked tile (a person, a sign) without moving.
local FACING = { [K.DOWN] = 1, [K.UP] = 2, [K.LEFT] = 3, [K.RIGHT] = 4 }
-- Toward something solid a long press turns (the bump); toward open ground (a
-- hidden item on the quay steps) a short press turns without stepping.
local DELTA = { [K.DOWN] = { 0, 1 }, [K.UP] = { 0, -1 }, [K.LEFT] = { -1, 0 }, [K.RIGHT] = { 1, 0 } }
local function face(key)
  local x0, y0 = pos()
  local facing0 = emu:read8(playerObject() + 0x18) & 0xF
  if facing0 ~= FACING[key] then
    local tx, ty = x0 + DELTA[key][1], y0 + DELTA[key][2]
    if isOpen(gridFor(), tx, ty) then
      emu:addKey(key); frame(); emu:clearKey(key)
    else
      tap(key, 16)
    end
  end
  wait(12)
  local x, y = pos()
  if x ~= x0 or y ~= y0 then fail(string.format("face() moved the player from (%d,%d)", x0, y0)) end
  local facing = emu:read8(playerObject() + 0x18) & 0xF
  if facing ~= FACING[key] then fail(string.format("face() did not turn (facing %d, wanted %d)", facing, FACING[key])) end
end

-- Walk the route, face, press A and press through what follows.
-- Press A until a script starts (a bump against a wall can swallow the first);
-- false if none does. (sFieldMessageBoxMode drops back to hidden as soon as a
-- box has printed, so a started script is the sure sign, not a box.)
local function interact()
  for _ = 1, 3 do
    tap(K.A)
    local t0 = now()
    while now() - t0 < 40 do
      if not idle() or boxUp() then return true end
      frame()
    end
  end
  return false
end
local function talk(route, key, prefix)
  walkTo(route)
  face(key)
  shot(prefix .. "_00.png")
  if not interact() then fail("nothing happened at " .. prefix) end
  wait(20)
  shot(prefix .. "_first.png")
  return playThrough(prefix)
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
local function runRamScript(script, noEnd)
  local tableAddr, frameTable, code = SCRATCH, SCRATCH + 0x20, SCRATCH + 0x40
  local flat = { S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 } }
  for _, b in ipairs(script) do flat[#flat + 1] = b end
  if not noEnd then flat[#flat + 1] = S.SCR_OP_END end
  poke(code, flat)
  poke(frameTable, { { S.VAR_TEMP_0, 2 }, { 0, 2 }, { code, 4 }, { 0, 2 } })
  poke(tableAddr, { S.MAP_SCRIPT_ON_FRAME_TABLE, { frameTable, 4 }, 0 })
  emu:write16(sb1() + S.OFF_SB1_VARS + (S.VAR_TEMP_0 - S.VARS_START) * 2, 0)
  emu:write32(S.gMapHeader + S.OFF_MAPHEADER_MAPSCRIPTS, tableAddr)
end
local function add(script, t) for _, b in ipairs(t) do script[#script + 1] = b end end
local function setFlag(script, f) add(script, { S.SCR_OP_SETFLAG, { f, 2 } }) end
local function giveMon(script, species, level)
  add(script, { S.SCR_OP_CALLNATIVE, { S.ScrCmd_createmon | 1, 4 }, 0, S.PARTY_SIZE,
                { species, 2 }, { level, 2 }, { 0, 4 } })
end
-- warp to (x, y) on `map` (no warp id), then wait for it
local function warpTo(script, map, x, y)
  add(script, { S.SCR_OP_WARP, map >> 8, map & 0xFF, 0xFF, { x, 2 }, { y, 2 }, S.SCR_OP_WAITSTATE })
  runRamScript(script)
  waitUntil(function() return mapId() == map and idle() end, 4000, "the warp to map " .. map)
  wait(30)
end

-- Walk into a door from the tile in front of it (`key` toward it) and check it
-- leads to `dest`; then come back to (bx, by) on `home`. The interiors are other
-- agents' maps: only the arrival is checked here.
local function door(front, key, dest, name, home, back)
  walkTo({ front })
  emu:addKey(key)
  waitUntil(function() return mapId() == dest end, 200, "the door to " .. name)
  emu:clearKey(key)
  waitUntil(idle, 4000, "the arrival in " .. name)
  wait(20)
  shot("door_" .. name .. ".png")
  expect(mapId() == dest, "the door at (" .. front[1] .. "," .. front[2] .. ") leads to " .. name)
  warpTo({}, home, back[1], back[2])
end

-- --- The checks -----------------------------------------------------------------------------

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

-- Beat 10C's end and beat 11 on the quay.
local function arrival()
  local setup = {}
  setFlag(setup, S.FLAG_SYS_POKEMON_GET)
  -- the eighth badge only so the level-100 test Pokémon obeys (battle_util.c);
  -- nothing in Emporion reads it
  setFlag(setup, S.FLAG_BADGE08_GET)
  -- beat 12 plays in the Deigma on first entry; emporion_rooms.sh plays it, so
  -- this walk of the city marks it done and only checks the door
  setFlag(setup, S.FLAG_DEIGMA_CLUE)
  giveMon(setup, S.SPECIES_TEST, 100)
  -- its first move, the one A picks, is Surf: every battle here ends in a turn or two
  add(setup, { S.SCR_OP_SETMONMOVE, 0, 0, { S.MOVE_SURF, 2 } })
  add(setup, { S.SCR_OP_SETVAR, { S.VAR_STARTER_MON, 2 }, { 0, 2 } })
  add(setup, { S.SCR_OP_GOTO, { S.Ichor_EventScript_EuploiaMakesEmporion, 4 } })
  runRamScript(setup, true)
  waitUntil(function() return mapId() == S.MAP_HARBOR end, 3000, "the Euploia to make Emporion")
  expect(getFlag(S.FLAG_CROSSING_DONE), "the crossing is done")
  waitUntil(function() return inOverworld() end, 3000, "the harbor")
  wait(20)
  local x, y = pos()
  expect(x == 30 and y == 16, string.format("the Euploia's warp lands on her berth, (30,16) (at %d,%d)", x, y))
  expect(objectPresent(S.LOCALID_HARBOR_KLEON) and objectPresent(S.LOCALID_HARBOR_ALETHEA)
         and objectPresent(S.LOCALID_HARBOR_KERYKOS), "Kleon, Alethea and Kerykos are on the quay")
  shot("b11_00_arrival.png")
  -- up to the altar menu; MAKE AN OFFERING first, which Kerykos sends back
  playThrough("b11_a", multichoice)
  wait(20); shot("b11_altar_menu.png")
  tap(K.DOWN); wait(6); tap(K.A); wait(10)
  playThrough("b11_b", multichoice)
  wait(20); shot("b11_altar_menu_again.png")
  tap(K.A); wait(10)
  playThrough("b11_c")
  expect(getFlag(S.FLAG_ARRIVED), "beat 11 sets FLAG_ICHOR_ARRIVED_EMPORION")
  expect(getFlag(S.FLAG_VISITED), "Emporion is a fly target (FLAG_ICHOR_VISITED_EMPORION)")
  expect(getFlag(S.FLAG_RITES_TUTORIAL), "Kerykos's rites tutorial and oil (FLAG_ICHOR_RITES_TUTORIAL)")
  expect(getFlag(S.FLAG_GOT_TROWEL), "Alethea's Trowel (FLAG_ICHOR_GOT_TROWEL)")
  expect(itemCount(S.ITEM_TROWEL) == 1 and itemCount(S.ITEM_OLIVE_OIL) == 3,
         "the actual Trowel and three Olive Oil are in the Bag")
  expect(getFlag(S.FLAG_DUG_QUAY), "the planter's sherd is dug (FLAG_ICHOR_DUG_EMPORION_QUAY)")
  expect(getFlag(S.FLAG_QUAY_FIXED) and getFlag(S.FLAG_ARACHNE_SHERD),
         "the fixed dig records an actual Arachne sherd in engine state")
  expect(emu:read8(ichor() + S.OFF_ICHOR_FAVOR + S.GOD_HERMES) == 1,
         "the tutorial prayer earns one Hermes Favor")
  expect(not objectPresent(S.LOCALID_HARBOR_KLEON) and not objectPresent(S.LOCALID_HARBOR_ALETHEA)
         and not objectPresent(S.LOCALID_HARBOR_KERYKOS), "the cast has left the quay")
  local px, py = pos()
  expect(px == 31 and py == 14, string.format("the player ends at the planter, (31,14) (at %d,%d)", px, py))
  shot("b11_99_free.png")
end

local function harbor()
  -- the quay herm (an altar now), the planter, the city's sign
  walkTo({ { 30, 14 } }); face(K.UP); interact()
  playThrough("h_herm", multichoice); tap(K.A); wait(10); playThrough("h_herm_pray")
  talk({ { 31, 14 } }, K.UP, "h_planter")
  expect(not getFlag(S.FLAG_ARACHNE_SHERD + 1), "revisiting the planter does not grant a second sherd")
  talk({ { 29, 14 } }, K.UP, "h_city_sign")
  -- the landing steps' Heart Scale; Nausikles's ferry: STAY
  talk({ { 29, 15 }, { 25, 15 } }, K.DOWN, "h_heart_scale")
  expect(getFlag(S.FLAG_HIDDEN_HEART_SCALE), "the Heart Scale on the quay steps")
  walkTo({ { 28, 14 } }); face(K.DOWN); interact()
  playThrough("h_nausikles", multichoice)
  wait(10); shot("h_ferry_menu.png")
  tap(K.DOWN); wait(6); tap(K.A); wait(10)
  playThrough("h_nausikles_stay")
  expect(mapId() == S.MAP_HARBOR, "STAY keeps the player on the quay")
  -- the customs man
  talk({ { 24, 15 } }, K.UP, "h_customs")
  -- the forum: Glykera and Daedalus's page I, the wine-seller
  talk({ { 33, 15 }, { 33, 8 }, { 29, 8 } }, K.LEFT, "h_glykera")
  expect(getFlag(S.FLAG_PAGE_1), "Glykera trades Daedalus's page I for an Olive Oil")
  expect(itemCount(S.ITEM_OLIVE_OIL) == 2 and getFlag(S.FLAG_ENGINE_PAGE_1),
         "Glykera consumes one real Olive Oil and records page I in engine state")
  talk({ { 29, 6 }, { 21, 6 }, { 21, 8 } }, K.LEFT, "h_wine")
  -- the road's sign; the yard: the dockhand, the hiring board, the hiring hall
  talk({ { 21, 4 } }, K.LEFT, "h_road_sign")
  talk({ { 21, 10 }, { 10, 10 } }, K.LEFT, "h_dockhand")
  talk({ { 6, 10 }, { 6, 9 } }, K.UP, "h_hiring_board")
  door({ 4, 9 }, K.UP, S.MAP_HIRING_HALL, "hiring_hall", S.MAP_HARBOR, { 4, 9 })
  -- the ship sheds: the sailor, the mother and son, the Super Potion, the dig
  talk({ { 15, 10 }, { 18, 10 }, { 18, 14 }, { 16, 14 } }, K.LEFT, "h_sailor")
  talk({ { 16, 15 }, { 6, 15 }, { 6, 14 } }, K.LEFT, "h_mother")
  talk({ { 6, 15 }, { 2, 15 } }, K.UP, "h_super_potion")
  expect(getFlag(S.FLAG_ITEM_SUPER_POTION), "the Super Potion on the ship sheds' slipway")
  talk({ { 11, 15 } }, K.UP, "h_dig_sheds")
  expect(getFlag(S.FLAG_DAILY_SHIPSHEDS), "the ship sheds record today's real dig")
  talk({ { 11, 15 } }, K.UP, "h_dig_sheds_again")
  -- the mole: the Bronze Obol in the wall, Halitherses twice
  talk({ { 16, 15 }, { 33, 15 }, { 33, 11 }, { 43, 11 }, { 43, 18 } }, K.RIGHT, "h_obol")
  expect(getFlag(S.FLAG_HIDDEN_OBOL), "the Bronze Obol in the harbor wall")
  talk({ { 43, 22 } }, K.DOWN, "h_halitherses_1")
  expect(getFlag(S.FLAG_MET_HALITHERSES), "Halitherses introduces himself")
  local oldKind = emu:read8(ichor() + S.OFF_ICHOR_OMEN_KIND)
  local oldEntry = emu:read16(ichor() + S.OFF_ICHOR_OMEN_ENTRY)
  emu:write8(ichor() + S.OFF_ICHOR_OMEN_KIND, S.OMEN_GOOD_SIGN)
  emu:write16(ichor() + S.OFF_ICHOR_OMEN_ENTRY, 3)
  tap(K.A); wait(10); playThrough("h_halitherses_2")
  expect(getFlag(S.FLAG_AUGURY_READ), "Halitherses records the actual daily omen")
  expect(emu:read8(ichor() + S.OFF_ICHOR_OMEN_KIND) == S.OMEN_GOOD_SIGN
         and emu:read16(ichor() + S.OFF_ICHOR_OMEN_ENTRY) == 3,
         "reading the lucky-three omen does not reroll the sky")
  tap(K.A); wait(10); playThrough("h_halitherses_3")
  warpTo({}, S.MAP_HARBOR, 43, 22)
  face(K.DOWN); interact(); playThrough("h_halitherses_reentry")
  expect(getFlag(S.FLAG_AUGURY_READ), "the daily augury limit survives leaving and reentering the harbor")
  local blessing = {}
  for i = 0, S.BLESSING_SIZE - 1 do blessing[i] = emu:read8(ichor() + S.OFF_ICHOR_BLESSING + i) end
  emu:write16(ichor() + S.OFF_ICHOR_OMEN_ENTRY, 0)
  writeFlag(S.FLAG_AUGURY_READ, false)
  interact()
  playThrough("h_halitherses_blessing_no", function() return taskRunning("Task_HandleYesNoInput") end)
  wait(20); tap(K.B); playThrough("h_halitherses_blessing_declined")
  for i = 0, S.BLESSING_SIZE - 1 do
    expect(emu:read8(ichor() + S.OFF_ICHOR_BLESSING + i) == blessing[i], "declining augury preserves blessing byte " .. i)
  end
  writeFlag(S.FLAG_AUGURY_READ, false)
  interact(); playThrough("h_halitherses_blessing_yes")
  expect(getFlag(S.FLAG_AUGURY_READ) and emu:read8(ichor() + S.OFF_ICHOR_BLESSING) == S.GOD_HERMES
         and emu:read16(ichor() + S.OFF_ICHOR_BLESSING + S.OFF_BLESSING_STEPS) == 100,
         "accepting the good sign grants Hermes's real hundred-step blessing")
  emu:write16(ichor() + S.OFF_ICHOR_BLESSING + S.OFF_BLESSING_STEPS, 37)
  interact(); playThrough("h_halitherses_blessing_again")
  expect(emu:read16(ichor() + S.OFF_ICHOR_BLESSING + S.OFF_BLESSING_STEPS) == 37,
         "repeated augury cannot refresh the day's blessing")
  writeFlag(S.FLAG_AUGURY_READ, false)
  emu:write8(ichor() + S.OFF_ICHOR_OMEN_KIND, S.OMEN_VISITOR)
  emu:write16(ichor() + S.OFF_ICHOR_OMEN_ENTRY, S.OMEN_KORANTHA)
  interact(); playThrough("h_halitherses_korantha")
  expect(getFlag(S.FLAG_AUGURY_READ)
         and emu:read8(ichor() + S.OFF_ICHOR_OMEN_KIND) == S.OMEN_VISITOR
         and emu:read16(ichor() + S.OFF_ICHOR_OMEN_ENTRY) == S.OMEN_KORANTHA,
         "Halitherses reports the saved Korantha visitor without rerolling it")
  writeFlag(S.FLAG_AUGURY_READ, false)
  emu:write16(ichor() + S.OFF_ICHOR_OMEN_ENTRY, S.OMEN_PITHOUND)
  interact(); playThrough("h_halitherses_pithound")
  expect(getFlag(S.FLAG_AUGURY_READ)
         and emu:read8(ichor() + S.OFF_ICHOR_OMEN_KIND) == S.OMEN_VISITOR
         and emu:read16(ichor() + S.OFF_ICHOR_OMEN_ENTRY) == S.OMEN_PITHOUND,
         "Halitherses reports the saved marked-jar visitor and its location")
  writeFlag(S.FLAG_AUGURY_READ, false)
  emu:write16(ichor() + S.OFF_ICHOR_OMEN_ENTRY, S.OMEN_NEMECUB)
  interact(); playThrough("h_halitherses_nemecub")
  expect(getFlag(S.FLAG_AUGURY_READ)
         and emu:read8(ichor() + S.OFF_ICHOR_OMEN_KIND) == S.OMEN_VISITOR
         and emu:read16(ichor() + S.OFF_ICHOR_OMEN_ENTRY) == S.OMEN_NEMECUB,
         "Halitherses reports the saved golden cub and the Isthmus hill spur")
  for i = 0, S.BLESSING_SIZE - 1 do emu:write8(ichor() + S.OFF_ICHOR_BLESSING + i, blessing[i]) end
  emu:write8(ichor() + S.OFF_ICHOR_OMEN_KIND, oldKind)
  emu:write16(ichor() + S.OFF_ICHOR_OMEN_ENTRY, oldEntry)
  -- Poseidon's sanctuary and the stevedore at the quay's east end
  talk({ { 43, 11 }, { 36, 14 } }, K.UP, "h_poseidon_altar")
  talk({ { 37, 14 } }, K.UP, "h_victors_wreath")
  talk({ { 36, 14 } }, K.DOWN, "h_stevedore")
end

-- The deck's ferry to Emporion (the deck's own map is the trireme agent's): run
-- Ichor_EventScript_FerryDeck with the Emporion destination, answer YES.
local function ferry()
  local s = {}
  setFlag(s, S.FLAG_FERRY_TO_EMPORION)
  warpTo(s, S.MAP_DECK, 2, 2)
  runRamScript({ S.SCR_OP_GOTO, { S.Ichor_EventScript_FerryDeck, 4 } }, true)
  playThrough("ferry_deck", function() return mapId() == S.MAP_HARBOR end)
  waitUntil(idle, 4000, "the harbor after the ferry")
  local x, y = pos()
  expect(mapId() == S.MAP_HARBOR and x == 30 and y == 16, "the deck's ferry sails to Emporion's berth (30,16)")
  expect(not objectPresent(S.LOCALID_HARBOR_KERYKOS), "beat 11 does not replay")
end

local function intoCity()
  walkTo({ { 30, 15 }, { 33, 15 }, { 33, 10 }, { 23, 10 }, { 23, 0 } })
  step(K.UP)
  local x, y = pos()
  expect(mapId() == S.MAP_CITY and x == 23 and y == 45, "the harbor road leads up into the city (23,45)")
  shot("c_00_harbor_road.png")
end

local function markedPithos()
  local oldKind = emu:read8(ichor() + S.OFF_ICHOR_OMEN_KIND)
  local oldEntry = emu:read16(ichor() + S.OFF_ICHOR_OMEN_ENTRY)
  local oldConsumed = getFlag(S.FLAG_OMEN_PITHOUND)
  local function setOmen(kind, entry)
    emu:write8(ichor() + S.OFF_ICHOR_OMEN_KIND, kind)
    emu:write16(ichor() + S.OFF_ICHOR_OMEN_ENTRY, entry)
  end
  local function reload()
    warpTo({}, S.MAP_HARBOR, 23, 1)
    warpTo({}, S.MAP_CITY, 10, 23)
    face(K.DOWN)
  end
  local function empty(prefix)
    interact()
    playThrough(prefix, function() return inBattle() or idle() end)
    expect(not inBattle(), prefix .. " cannot start a visitor battle")
  end
  local function encounter(prefix)
    interact()
    playThrough(prefix, inBattle)
    local t0 = now()
    while emu:read32(S.gBattlerControllerFuncs) ~= (S.HandleInputChooseAction | 1) do
      tap(K.A); wait(4)
      if now() - t0 > 1500 then fail("no marked-jar battle action menu") end
    end
    expect(emu:read16(S.gBattleMons + S.BATTLE_MON_SIZE + S.OFF_BATTLE_MON_SPECIES) == S.SPECIES_PITHOUND
           and emu:read8(S.gBattleMons + S.BATTLE_MON_SIZE + S.OFF_BATTLE_MON_LEVEL) == 16,
           prefix .. " starts the actual level-16 Pithound")
  end

  setOmen(S.OMEN_GOOD_SIGN, oldEntry)
  writeFlag(S.FLAG_OMEN_PITHOUND, false)
  reload()
  empty("c_marked_jar_legacy_off_day")
  setOmen(S.OMEN_VISITOR, S.OMEN_PITHOUND)
  expect(emu:saveStateFile(OUT .. "before_pithound.ss", 31), "saved the unused marked-jar state")
  for i = 0, S.PARTY_SIZE * S.POKEMON_SIZE - 1 do emu:write8(S.gParties + i, 0) end
  emu:write8(S.gPartiesCount, 0)
  local weak = {}
  giveMon(weak, S.SPECIES_TEST, 5)
  add(weak, { S.SCR_OP_SETMONMOVE, 0, 0, { S.MOVE_SURF, 2 } })
  runRamScript(weak)
  wait(60); waitUntil(idle, 1200, "the weak visitor fixture")
  encounter("c_marked_jar_loss")
  expect(playBattle("c_marked_jar_loss_battle.png") == S.B_OUTCOME_LOST
         and not getFlag(S.FLAG_OMEN_PITHOUND), "losing leaves the marked-jar visitor available")
  playThrough("c_marked_jar_whiteout")
  expect(emu:loadStateFile(OUT .. "before_pithound.ss", 31), "restored the unused marked-jar state")
  wait(20)
  encounter("c_marked_jar_run")
  tap(K.DOWN); tap(K.RIGHT); tap(K.A)
  playThrough("c_marked_jar_ran")
  expect(emu:read8(S.gBattleOutcome) == S.B_OUTCOME_RAN and not getFlag(S.FLAG_OMEN_PITHOUND),
         "running leaves the marked-jar visitor available")
  reload()
  encounter("c_marked_jar_defeat")
  tap(K.UP); tap(K.LEFT)
  expect(playBattle("c_marked_jar_defeat_battle.png") == S.B_OUTCOME_WON,
         "the marked-jar visitor can actually be defeated")
  playThrough("c_marked_jar_defeated")
  expect(getFlag(S.FLAG_OMEN_PITHOUND), "defeat consumes only today's marked-jar visit")
  empty("c_marked_jar_repeat")
  reload()
  empty("c_marked_jar_reentry")
  writeFlag(S.FLAG_OMEN_PITHOUND, false)
  setOmen(S.OMEN_VISITOR, S.OMEN_KORANTHA)
  empty("c_marked_jar_expired")
  expect(not getFlag(S.FLAG_OMEN_PITHOUND), "an expired jar does not consume a later visitor")
  setOmen(S.OMEN_VISITOR, S.OMEN_PITHOUND)
  reload()
  local balls = {}
  local key = emu:read32(sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
  for i = 0, S.BAG_POKEBALLS_COUNT - 1 do
    local slot = sb1() + S.OFF_SB1_POKEBALLS + i * S.ITEM_SLOT_SIZE
    local item = emu:read16(slot)
    if item ~= 0 then
      add(balls, { S.SCR_OP_REMOVEITEM, { item, 2 }, { emu:read16(slot + S.OFF_ITEM_SLOT_QUANTITY) ~ key, 2 } })
    end
  end
  add(balls, { S.SCR_OP_ADDITEM, { S.ITEM_MASTER_BALL, 2 }, { 1, 2 } })
  runRamScript(balls)
  wait(60); waitUntil(idle, 1200, "the marked-jar capture fixture")
  expect(itemCount(S.ITEM_MASTER_BALL) == 1, "the marked-jar capture has one real Master Ball")
  encounter("c_marked_jar_capture")
  tap(K.UP); tap(K.RIGHT); tap(K.A)
  waitUntil(function() return taskRunning("Task_BagMenu_HandleInput") end, 1200, "the marked-jar battle Bag")
  wait(30)
  for i = 1, S.POCKETS_COUNT do
    if emu:read8(S.gBagPosition + S.OFF_BAG_POSITION_POCKET) == S.POCKET_POKE_BALLS then break end
    tap(K.RIGHT); wait(50)
  end
  expect(emu:read8(S.gBagPosition + S.OFF_BAG_POSITION_POCKET) == S.POCKET_POKE_BALLS,
         "the marked-jar battle Bag selects the Poke Ball pocket")
  tap(K.UP); tap(K.UP); tap(K.A); wait(20); tap(K.A)
  local t0 = now()
  while not idle() do
    if on("CB2_NamingScreen") then
      wait(40); shot("c_marked_jar_caught.png")
      tap(K.START); wait(20); tap(K.A); wait(40)
    else
      tap(K.A); wait(4)
    end
    if now() - t0 > 12000 then fail("the marked-jar capture never returned to the field") end
  end
  expect(emu:read8(S.gBattleOutcome) == S.B_OUTCOME_CAUGHT
         and emu:read8(S.gPartiesCount) == 2 and itemCount(S.ITEM_MASTER_BALL) == 0
         and getFlag(S.FLAG_OMEN_PITHOUND),
         "an actual marked-jar capture adds Pithound, consumes the ball and saves the visit")
  reload()
  empty("c_marked_jar_caught_reentry")
  setOmen(oldKind, oldEntry)
  writeFlag(S.FLAG_OMEN_PITHOUND, oldConsumed)
  walkTo({ { 12, 23 } })
end

local function city()
  -- the fork sign and the Nemea gate
  talk({ { 23, 42 }, { 21, 42 } }, K.LEFT, "c_fork_sign")
  talk({ { 21, 41 }, { 3, 41 } }, K.UP, "c_nemea_sign")
  talk({ { 2, 41 } }, K.LEFT, "c_nemea_hoplite")
  -- the harbor quarter: the Asclepeion, the Deigma, the metic, the Repel
  walkTo({ { 21, 41 }, { 21, 39 } })
  talk({ { 15, 39 }, { 15, 37 } }, K.UP, "c_asclepeion_sign")
  door({ 16, 37 }, K.UP, S.MAP_ASCLEPEION, "asclepeion", S.MAP_CITY, { 16, 37 })
  talk({ { 16, 39 }, { 31, 39 }, { 31, 37 } }, K.UP, "c_deigma_sign")
  door({ 32, 37 }, K.UP, S.MAP_DEIGMA, "deigma", S.MAP_CITY, { 32, 37 })
  talk({ { 28, 37 } }, K.LEFT, "c_metic")
  talk({ { 39, 37 }, { 39, 33 } }, K.LEFT, "c_repel")
  expect(getFlag(S.FLAG_ITEM_REPEL), "the Repel behind the Deigma")
  -- the Agora: the herm, the stalls, the stoa
  walkTo({ { 27, 31 } })
  local bag, restoreBag = saveBag()
  local favorBefore = emu:read8(ichor() + S.OFF_ICHOR_FAVOR + S.GOD_HERMES)
  for i, slot in pairs(bag) do
    if slot[1] == S.ITEM_OLIVE_OIL then emu:write16(sb1() + S.OFF_SB1_BAG + i * S.ITEM_SLOT_SIZE, 0) end
  end
  talk({ { 27, 31 } }, K.LEFT, "c_herm_no_oil")
  expect(not getFlag(S.FLAG_ENGINE_HERM) and not getFlag(S.FLAG_HERM),
         "tutorial completion cannot anoint the herm without actual Oil")
  restoreBag()
  local oilBefore = itemCount(S.ITEM_OLIVE_OIL)
  interact()
  playThrough("c_herm_decline", function() return taskRunning("Task_HandleYesNoInput") end)
  wait(20); tap(K.B); playThrough("c_herm_declined")
  expect(not getFlag(S.FLAG_ENGINE_HERM) and itemCount(S.ITEM_OLIVE_OIL) == oilBefore,
         "declining the herm keeps its Oil and dry state")
  talk({ { 27, 31 } }, K.LEFT, "c_herm")
  expect(getFlag(S.FLAG_ENGINE_HERM) and getFlag(S.FLAG_HERM) and itemCount(S.ITEM_OLIVE_OIL) == oilBefore - 1,
         "the crossroads herm registers its real anchor and consumes one Oil")
  expect(emu:read8(ichor() + S.OFF_ICHOR_FAVOR + S.GOD_HERMES) == favorBefore + 1,
         "the crossroads herm grants Hermes one Favor")
  talk({ { 27, 31 } }, K.LEFT, "c_herm_again")
  expect(itemCount(S.ITEM_OLIVE_OIL) == oilBefore - 1
         and emu:read8(ichor() + S.OFF_ICHOR_FAVOR + S.GOD_HERMES) == favorBefore + 1,
         "revisiting the herm neither consumes Oil nor repeats Favor")
  writeFlag(S.FLAG_ENGINE_HERM, false)
  warpTo({}, S.MAP_CITY, 27, 31)
  expect(getFlag(S.FLAG_ENGINE_HERM) and itemCount(S.ITEM_OLIVE_OIL) == oilBefore - 1
         and emu:read8(ichor() + S.OFF_ICHOR_FAVOR + S.GOD_HERMES) == favorBefore + 1,
         "legacy city anointing registers the anchor on reentry without another charge or reward")
  walkTo({ { 27, 30 }, { 20, 30 }, { 20, 26 } }); face(K.LEFT); interact()
  playThrough("c_general", function() return taskRunning("Task_ShopMenu") end)
  wait(20); shot("c_general_mart.png")
  tap(K.B); wait(20); playThrough("c_general_bye")
  walkTo({ { 20, 27 }, { 18, 27 }, { 18, 30 } }); face(K.UP); interact()
  playThrough("c_kydon", function() return taskRunning("Task_ShopMenu") end)
  wait(20); shot("c_kydon_mart.png")
  tap(K.B); wait(20); playThrough("c_kydon_bye")
  walkTo({ { 15, 30 } }); face(K.UP); interact()
  playThrough("c_offerings", function() return taskRunning("Task_ShopMenu") end)
  for i, item in ipairs({ S.ITEM_OLIVE_OIL, S.ITEM_BARLEY_CAKE, S.ITEM_WINE, S.ITEM_FRANKINCENSE, 0 }) do
    expect(emu:read16(S.EmporionCity_Mart_Offerings + (i - 1) * 2) == item,
           "the offering stall stocks its specified item " .. i)
  end
  tap(K.A)
  waitUntil(function() return taskRunning("Task_BuyMenu") end, 900, "the offering stall's item list")
  wait(20); shot("c_offerings_stock.png")
  for i, item in ipairs({ S.ITEM_OLIVE_OIL, S.ITEM_BARLEY_CAKE, S.ITEM_WINE, S.ITEM_FRANKINCENSE }) do
    local beforeItem, beforeMoney = itemCount(item), money()
    if i > 1 then tap(K.DOWN); wait(12) end
    tap(K.A)
    playThrough("c_offerings_quantity_" .. i, function() return taskRunning("Task_BuyHowManyDialogueHandleInput") end)
    tap(K.A)
    playThrough("c_offerings_confirm_" .. i, function() return taskRunning("Task_CallYesOrNoCallback") end)
    tap(K.A)
    playThrough("c_offerings_bought_" .. i, function() return taskRunning("Task_BuyMenu") end)
    expect(itemCount(item) == beforeItem + 1 and money() == beforeMoney - ({ 200, 150, 300, 500 })[i],
           "the offering stall sells real offering " .. i .. " at its specified price")
  end
  tap(K.B)
  waitUntil(function() return taskRunning("Task_ShopMenu") end, 900, "the offering stall's menu again")
  wait(20); tap(K.B); playThrough("c_offerings_bye")
  walkTo({ { 12, 30 } }); face(K.UP)
  local function pasion(row, answer, prefix)
    interact()
    playThrough(prefix, function() return taskRunning("Task_HandleMultichoiceInput") end)
    wait(20)
    if row == nil then tap(K.B) else
      for _ = 1, row do tap(K.DOWN); wait(8) end
      tap(K.A)
    end
    if answer then
      playThrough(prefix .. "_quote", function() return taskRunning("Task_HandleYesNoInput") end)
      wait(20); shot(prefix .. "_price.png"); tap(answer)
    end
    playThrough(prefix .. "_done")
  end
  local originalMoney = money()
  addCoinFixture(S.ITEM_RELIC_SILVER)
  pasion(nil, nil, "c_pasion_cancel")
  pasion(1, K.B, "c_pasion_decline")
  expect(itemCount(S.ITEM_RELIC_SILVER) == 1 and money() == originalMoney,
         "Pasion's menu cancellation and declined quote keep coin and money")
  for row, coin in ipairs({ S.ITEM_RELIC_COPPER, S.ITEM_RELIC_SILVER, S.ITEM_RELIC_GOLD }) do
    if coin ~= S.ITEM_RELIC_SILVER then addCoinFixture(coin) end
    local beforeCoin, beforeMoney = itemCount(coin), money()
    pasion(row - 1, K.A, "c_pasion_sale_" .. row)
    expect(itemCount(coin) == beforeCoin - 1 and money() == beforeMoney + ({ 600, 2400, 6000 })[row],
           "Pasion buys coin " .. row .. " at the market price plus twenty percent")
  end
  pasion(1, nil, "c_pasion_no_coin")
  expect(itemCount(S.ITEM_RELIC_SILVER) == 0, "Pasion cannot sell a missing coin")
  addCoinFixture(S.ITEM_RELIC_SILVER)
  setMoney(S.MAX_MONEY)
  pasion(1, nil, "c_pasion_money_cap")
  expect(itemCount(S.ITEM_RELIC_SILVER) == 1 and money() == S.MAX_MONEY,
         "Pasion refuses a capped payment without taking the coin")
  setMoney(originalMoney)
  pasion(1, K.A, "c_pasion_cap_retry")
  expect(itemCount(S.ITEM_RELIC_SILVER) == 0 and money() == originalMoney + 2400,
         "Pasion pays the retained coin after there is room for its full value")
  talk({ { 14, 30 }, { 14, 31 } }, K.LEFT, "c_elder")
  talk({ { 14, 30 }, { 16, 30 }, { 16, 27 } }, K.DOWN, "c_honey")
  expect(getFlag(S.FLAG_HIDDEN_HONEY), "the Honey under Kydon's awning")
  -- the jars: try until one holds a Pithound (one in four), then fight it
  walkTo({ { 12, 23 } }); face(K.DOWN)
  local originalRng = {}
  for i = 0, S.RNG_STATE_SIZE - 1 do originalRng[i] = emu:read8(S.gRngValue + i) end
  -- SeedRng(0xC0FFEE)'s warmed state: earlier conversations must not make this flaky.
  emu:write32(S.gRngValue + S.OFF_RNG_A, 0xC6B1859D)
  emu:write32(S.gRngValue + S.OFF_RNG_B, 0x18DF44C1)
  emu:write32(S.gRngValue + S.OFF_RNG_C, 0x5E0062DC)
  emu:write32(S.gRngValue + S.OFF_RNG_COUNTER, 0x11)
  local found = false
  for i = 1, 16 do
    interact()
    local t0 = now()
    while not idle() and not inBattle() do
      -- A every half second: the jar's line, or the growl and into the battle
      wait(30)
      if i == 1 and now() - t0 < 40 then shot("c_pithos_empty.png") end
      if not inBattle() and not idle() then tap(K.A) end
      if now() - t0 > 3000 then shot("c_pithos_stuck.png"); fail("stuck at the jars") end
    end
    if inBattle() then
      playBattle("c_pithound_battle.png"); found = true
      waitUntil(idle, 3000, "the field after the Pithound")
      break
    end
    wait(10)
  end
  for i = 0, S.RNG_STATE_SIZE - 1 do emu:write8(S.gRngValue + i, originalRng[i]) end
  expect(found, "a jar by the stoa holds a Pithound")
  markedPithos()
  talk({ { 11, 22 } }, K.LEFT, "c_x_speed")
  expect(getFlag(S.FLAG_ITEM_X_SPEED), "the X Speed at the end of the stoa")
  walkTo({ { 13, 22 } }); face(K.UP); interact(); playThrough("c_spice_seller")
  walkTo({ { 15, 22 } }); face(K.UP); interact()
  playThrough("c_scrolls", function() return taskRunning("Task_ShopMenu") end)
  wait(20); shot("c_scrolls_mart.png")
  tap(K.B); wait(20); playThrough("c_scrolls_bye")
  talk({ { 20, 22 }, { 20, 24 }, { 25, 24 } }, K.LEFT, "c_shopper")
  talk({ { 27, 24 } }, K.UP, "c_agora_sign")
  -- Sykeas and his snatcher
  talk({ { 30, 24 }, { 30, 27 } }, K.UP, "c_sykeas_before")
  talk({ { 30, 24 }, { 29, 24 } }, K.DOWN, "c_harpeck")
  expect(getFlag(S.FLAG_HIDE_HARPECK) and not objectPresent(S.LOCALID_HARPECK), "the snatcher is gone after its battle")
  talk({ { 30, 24 }, { 31, 24 }, { 31, 27 }, { 30, 27 } }, K.UP, "c_sykeas_after")
  expect(getFlag(S.FLAG_GOT_FIGS), "Sykeas gives his figs and the Pretty Feather")
  talk({ { 34, 27 }, { 34, 26 } }, K.LEFT, "c_fishmonger")
  -- Number Nine
  talk({ { 34, 24 } }, K.UP, "c_number_nine")
  expect(getFlag(S.FLAG_NUMBER_NINE) and not objectPresent(S.LOCALID_NUMBER_NINE), "Number Nine walks off his plinth")
  talk({ { 34, 24 } }, K.UP, "c_empty_plinth")
  -- the households and the tavern
  door({ 39, 22 }, K.UP, S.MAP_PHILOXENOS, "philoxenos", S.MAP_CITY, { 39, 22 })
end

-- (door() is for doors; a plain walk for the rest.)
local function city2()
  door({ 45, 28 }, K.UP, S.MAP_WIDOW, "widows_house", S.MAP_CITY, { 45, 28 })
  talk({ { 45, 23 }, { 29, 23 }, { 29, 22 } }, K.UP, "c_tavern_sign")
  door({ 30, 22 }, K.UP, S.MAP_TAVERN, "tavern", S.MAP_CITY, { 30, 22 })
  -- the acrocorinth stair's Stardust
  walkTo({ { 35, 22 }, { 35, 13 }, { 41, 13 }, { 41, 10 }, { 44, 10 }, { 44, 6 } })
  face(K.UP); interact(); playThrough("c_stardust")
  expect(getFlag(S.FLAG_HIDDEN_STARDUST), "the Stardust at the top of Acrocorinth's stair")
  shot("c_acrocorinth.png")
  -- beat 14 on the temple stair
  walkTo({ { 44, 10 }, { 41, 10 }, { 41, 13 }, { 36, 13 }, { 36, 17 }, { 23, 17 } })
  expect(not getFlag(S.FLAG_KLEON_WON_HERALD), "Kleon hasn't won the Herald Laurel yet")
  emu:addKey(K.UP); wait(12); emu:clearKey(K.UP)   -- onto the bottom tread: the trigger
  local shots = 0
  playThrough("b14", function()
    -- Kleon on his way down the steps and off west, between the boxes
    if not boxUp() and objectPresent(S.LOCALID_KLEON_STEPS) and shots < 6 and now() % 20 == 0 then
      shots = shots + 1
      shot(string.format("b14_kleon_%d.png", shots))
    end
    return idle() and getFlag(S.FLAG_KLEON_WON_HERALD)
  end)
  expect(getFlag(S.FLAG_KLEON_WON_HERALD), "beat 14 sets FLAG_ICHOR_KLEON_WON_HERALD")
  expect(not objectPresent(S.LOCALID_KLEON_STEPS), "Kleon has run off from the steps")
  -- the temple terrace
  talk({ { 23, 12 }, { 22, 12 } }, K.UP, "c_temple_sign")
  door({ 23, 12 }, K.UP, S.MAP_TEMPLE, "temple_of_hermes", S.MAP_CITY, { 23, 12 })
  talk({ { 31, 12 }, { 31, 11 } }, K.UP, "c_peirene")
  talk({ { 31, 13 }, { 31, 15 } }, K.UP, "c_cistern")
  talk({ { 30, 15 }, { 30, 13 }, { 18, 13 } }, K.RIGHT, "c_pilgrim")
  -- the runners' house, the Hephaisteion, the potters' lane
  door({ 12, 10 }, K.UP, S.MAP_RUNNERS, "runners_house", S.MAP_CITY, { 12, 10 })
  talk({ { 12, 13 }, { 2, 13 }, { 2, 12 } }, K.UP, "c_hephaisteion_sign")
  door({ 3, 12 }, K.UP, S.MAP_HEPHAISTEION, "hephaisteion", S.MAP_CITY, { 3, 12 })
  walkTo({ { 1, 12 }, { 1, 9 } })
  local bag, restoreBag = saveBag()
  for i, slot in pairs(bag) do
    if slot[1] == S.ITEM_TROWEL then
      emu:write16(sb1() + S.OFF_SB1_BAG + i * S.ITEM_SLOT_SIZE, 0)
    end
  end
  talk({ { 1, 9 } }, K.LEFT, "c_dig_garden_no_trowel")
  expect(not getFlag(S.FLAG_DAILY_HEPHAISTEION), "the garden stays undug without the actual Trowel")
  restoreBag()

  local originalSeed = emu:read32(sb1() + S.OFF_SB1_DAILY_SEED)
  emu:write32(sb1() + S.OFF_SB1_DAILY_SEED, 0x5EED)
  local encryptionKey = emu:read32(sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
  for i = 0, S.BAG_ITEMS_COUNT - 1 do
    local slot = sb1() + S.OFF_SB1_BAG + i * S.ITEM_SLOT_SIZE
    emu:write16(slot, S.ITEM_POTION)
    emu:write16(slot + S.OFF_ITEM_SLOT_QUANTITY, S.MAX_BAG_ITEM_CAPACITY ~ encryptionKey)
  end
  -- A full Bag's find goes to the Pithos (src/item.c), so fill that too.
  local pithos, pithosSaved = sb1() + S.OFF_SB1_PC_ITEMS, {}
  for i = 0, S.PC_ITEMS_COUNT - 1 do
    pithosSaved[i] = emu:read32(pithos + i * S.ITEM_SLOT_SIZE)
    emu:write16(pithos + i * S.ITEM_SLOT_SIZE, S.ITEM_POTION)
    emu:write16(pithos + i * S.ITEM_SLOT_SIZE + S.OFF_ITEM_SLOT_QUANTITY, 999)
  end
  talk({ { 1, 9 } }, K.LEFT, "c_dig_garden_full_bag")
  local gardenFind = emu:read16(S.sDig + S.OFF_DIG_FIND)
  local gardenQuantity = emu:read8(S.sDig + S.OFF_DIG_QUANTITY)
  expect(gardenFind < S.ITEMS_COUNT, "the garden's full-Bag fixture rolls an actual item")
  expect(not getFlag(S.FLAG_DAILY_HEPHAISTEION), "a full Bag and Pithos leave the garden's find buried for retry")
  pithos = sb1() + S.OFF_SB1_PC_ITEMS
  for i = 0, S.PC_ITEMS_COUNT - 1 do emu:write32(pithos + i * S.ITEM_SLOT_SIZE, pithosSaved[i]) end
  restoreBag()
  local gardenCount = itemCount(gardenFind)
  talk({ { 1, 9 } }, K.LEFT, "c_dig_garden")
  expect(getFlag(S.FLAG_DAILY_HEPHAISTEION), "the Hephaisteion garden records its own daily dig")
  expect(emu:read16(S.sDig + S.OFF_DIG_FIND) == gardenFind and itemCount(gardenFind) == gardenCount + gardenQuantity,
         "making room receives the same garden find in its exact quantity")
  emu:write32(sb1() + S.OFF_SB1_DAILY_SEED, originalSeed)
  local gardenBag = {}
  for i = 0, S.BAG_SLOTS * S.ITEM_SLOT_SIZE - 1 do gardenBag[i] = emu:read8(sb1() + S.OFF_SB1_BAG + i) end
  talk({ { 1, 9 } }, K.LEFT, "c_dig_garden_again")
  local unchanged = true
  for i = 0, S.BAG_SLOTS * S.ITEM_SLOT_SIZE - 1 do
    if emu:read8(sb1() + S.OFF_SB1_BAG + i) ~= gardenBag[i] then unchanged = false; break end
  end
  expect(unchanged, "the same day's repeat garden dig leaves the entire Bag unchanged")
  walkTo({ { 1, 13 }, { 8, 13 }, { 8, 20 }, { 3, 20 } })
  door({ 3, 20 }, K.UP, S.MAP_POTTER, "potters_workshop", S.MAP_CITY, { 3, 20 })
  -- the Isthmus Gate before the Herald Laurel: the hoplites turn the player back
  talk({ { 8, 20 }, { 8, 6 }, { 6, 6 }, { 6, 5 } }, K.LEFT, "c_gate_sign")
  talk({ { 6, 4 } }, K.UP, "c_gate_hoplite")
end

local function gateBeforeLaurel()
  walkTo({ { 8, 5 } })
  emu:addKey(K.UP); wait(12); emu:clearKey(K.UP)
  playThrough("c_gate_shut")
  local x, y = pos()
  expect(x == 8 and y == 5, string.format("the hoplites step the player back from the gate (at %d,%d)", x, y))
  expect(not getFlag(S.FLAG_KLEON_BATTLE_2_DONE), "no battle without the Herald Laurel")
end

local function gateAfterLaurel()
  local s = {}
  setFlag(s, S.FLAG_BADGE02_GET)
  warpTo(s, S.MAP_CITY, 8, 6)
  expect(objectPresent(S.LOCALID_KLEON_GATE), "Kleon waits in the Isthmus Gate")
  shot("b16_00_gate.png")
  walkTo({ { 9, 6 }, { 9, 5 } })
  emu:addKey(K.UP); wait(12); emu:clearKey(K.UP)
  playThrough("b16")
  expect(getFlag(S.FLAG_KLEON_BATTLE_2_DONE), "beat 16 sets FLAG_ICHOR_KLEON_BATTLE_2_DONE")
  expect(getFlag(S.FLAG_WON_KLEON_2), "the test party beats Kleon (FLAG_ICHOR_WON_KLEON_2)")
  expect(not objectPresent(S.LOCALID_KLEON_GATE), "Kleon has run through the gate")
  walkTo({ { 8, 4 }, { 8, 0 } })
  local x, y = pos()
  expect(x == 8 and y == 0, "the Isthmus road is open to the north seam")
  shot("b16_99_through.png")
end

local function backToTheQuay()
  warpTo({}, S.MAP_CITY, 23, 39)
  walkTo({ { 23, 45 } })
  step(K.DOWN)
  waitUntil(idle, 600, "the harbor"); wait(30)
  local x, y = pos()
  expect(mapId() == S.MAP_HARBOR and x == 23 and y == 0,
         string.format("the harbor road leads back down to the quay (map %d at %d,%d)", mapId(), x, y))
  shot("h_99_back_on_the_quay.png")
end

local function recoverLegacyTrowel()
  for i = 0, S.BAG_SLOTS - 1 do
    local slot = sb1() + S.OFF_SB1_BAG + i * S.ITEM_SLOT_SIZE
    if emu:read16(slot) == S.ITEM_TROWEL then
      emu:write16(slot, 0)
      emu:write16(slot + S.OFF_ITEM_SLOT_QUANTITY, 0)
    end
  end
  expect(getFlag(S.FLAG_GOT_TROWEL) and itemCount(S.ITEM_TROWEL) == 0,
         "simulate the old arrival's Trowel flag without an actual item")
  warpTo({}, S.MAP_CITY, 23, 39)
  warpTo({}, S.MAP_HARBOR, 30, 16)
  expect(objectPresent(S.LOCALID_HARBOR_ALETHEA), "Alethea returns for an unfulfilled Trowel gift")
  talk({ { 30, 16 } }, K.LEFT, "legacy_trowel")
  expect(itemCount(S.ITEM_TROWEL) == 1 and not objectPresent(S.LOCALID_HARBOR_ALETHEA),
         "Alethea grants the missing Trowel and leaves")
  warpTo({}, S.MAP_CITY, 23, 39)
  warpTo({}, S.MAP_HARBOR, 30, 16)
  expect(itemCount(S.ITEM_TROWEL) == 1 and not objectPresent(S.LOCALID_HARBOR_ALETHEA),
         "the recovered Trowel is not given twice")
end

local function eleusaWeather()
  local oldKind = emu:read8(ichor() + S.OFF_ICHOR_OMEN_KIND)
  local oldEntry = emu:read16(ichor() + S.OFF_ICHOR_OMEN_ENTRY)
  emu:write8(ichor() + S.OFF_ICHOR_OMEN_KIND, S.OMEN_WEATHER)
  emu:write16(ichor() + S.OFF_ICHOR_OMEN_ENTRY, S.OMEN_WEATHER_ELEUSA_SUN)
  warpTo({}, S.MAP_ELEUSA, 25, 12)
  expect(emu:read8(sb1() + S.OFF_SB1_WEATHER) == S.WEATHER_DROUGHT,
         "Eleusa's actual transition applies today's sun omen")
  wait(60); shot("eleusa_omen_sun.png")
  emu:write8(ichor() + S.OFF_ICHOR_OMEN_KIND, S.OMEN_GOOD_SIGN)
  emu:write16(ichor() + S.OFF_ICHOR_OMEN_ENTRY, 3)
  warpTo({}, S.MAP_ELEUSA, 25, 12)
  expect(emu:read8(sb1() + S.OFF_SB1_WEATHER) == S.WEATHER_NONE,
         "Eleusa restores normal weather when the sun omen no longer applies")
  wait(60); shot("eleusa_omen_clear.png")
  emu:write8(ichor() + S.OFF_ICHOR_OMEN_KIND, oldKind)
  emu:write16(ichor() + S.OFF_ICHOR_OMEN_ENTRY, oldEntry)
end

local co = coroutine.create(function()
  boot()
  arrival()
  harbor()
  ferry()
  intoCity()
  city()
  city2()
  gateBeforeLaurel()
  gateAfterLaurel()
  backToTheQuay()
  recoverLegacyTrowel()
  eleusaWeather()
end)

local realEmu = _G.emu
callbacks:add("frame", function()
  if not co then return end
  local result = table.pack(coroutine.resume(co))
  while true do
    if not result[1] then
      local err = tostring(result[2])
      console:log(err:find("^EMPORION FAIL") and err or ("EMPORION FAIL: " .. err))
      console:log("EMPORION done")
      co = nil
      return
    end
    if coroutine.status(co) == "dead" then
      console:log("EMPORION done")
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
