-- The voyage's transitions check, run by tools/ichor/tests/voyage_transitions.sh
-- (read it first).
--
-- Plays, as a player, every map change around Aigina's inn on the voyage night,
-- and records each one frame by frame:
--   1. out of the inn by its door mat onto Aigina's street, and back in;
--   2. Endeis, "Ready for bed?", the night by the fire, and the warp to the deck;
--   3. beat 10C on deck and the Euploia making Emporion's quay.
-- While recording, every frame's screenshot lands in OUT/<leg>/NNNN.png and its
-- state (map, player tile and facing, how much of the palette is lit) in
-- OUT/<leg>/frames.csv. Between two frames where the screen is not black, the
-- test fails on a change of map (a warp seen un-faded) or any person moving more
-- than one tile (a pop); and on arrival on each map, it checks the tile and the
-- facing the player is shown on when the screen first lights up.
--
-- Prints "VOYAGE ok ..." per check and ends with "VOYAGE done"; any failure prints
-- "VOYAGE FAIL: ..." first.

local S = dofile(os.getenv("VOYAGE_SYMBOLS") or "build/test_voyage_transitions/symbols.lua")
local OUT = os.getenv("VOYAGE_OUT") or "build/test_voyage_transitions/"
local SCRATCH = 0x0203F000  -- spare EWRAM past the linker's last EWRAM symbol
local K = { A = C.GBA_KEY.A, B = C.GBA_KEY.B, START = C.GBA_KEY.START, SELECT = C.GBA_KEY.SELECT,
            UP = C.GBA_KEY.UP, DOWN = C.GBA_KEY.DOWN, LEFT = C.GBA_KEY.LEFT, RIGHT = C.GBA_KEY.RIGHT }
local FACING = { [1] = "south", [2] = "north", [3] = "west", [4] = "east" }

local emu = setmetatable({}, { __index = function(_, name)
  return function(_, ...) return coroutine.yield("call", name, ...) end
end })
local function log(s) coroutine.yield("log", "VOYAGE " .. s) end
local function fail(s) error("VOYAGE FAIL: " .. s, 0) end
local function rawFrame() coroutine.yield("frame") end
local function now() return emu:currentFrame() end

-- --- Game state ------------------------------------------------------------------

local function sb1() return emu:read32(S.gSaveBlock1Ptr) end
local function sb2() return emu:read32(S.gSaveBlock2Ptr) end
local function getFlag(f) return (emu:read8(sb1() + S.OFF_SB1_FLAGS + (f >> 3)) >> (f & 7)) & 1 == 1 end
local function mapId()
  local loc = sb1() + S.OFF_SB1_LOCATION
  return emu:read8(loc) * 256 + emu:read8(loc + 1)
end
local function s16(v) if v >= 0x8000 then return v - 0x10000 end return v end
local function playerObject()
  return S.gObjectEvents + emu:read8(S.gPlayerAvatar + S.OFF_AVATAR_OBJECT_EVENT_ID) * S.OBJECT_EVENT_SIZE
end
local function pos()
  local c = playerObject() + S.OFF_OBJ_CURRENT_COORDS
  return s16(emu:read16(c)) - S.MAP_OFFSET, s16(emu:read16(c + 2)) - S.MAP_OFFSET
end
local function facing() return emu:read8(playerObject() + 0x18) & 0xF end
local function callback2() return emu:read32(S.gMain + S.OFF_MAIN_CALLBACK2) end
local function inOverworld() return callback2() == (S.CB2_Overworld | 1) end
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
-- How many of the 512 palette colors in palette RAM are not black: 0 is a black
-- screen, a lit map has hundreds.
local function litColors()
  local n = 0
  for i = 0, 511 do
    if emu:read16(0x05000000 + 2 * i) & 0x7FFF ~= 0 then n = n + 1 end
  end
  return n
end
local LIT = 24
-- Every live person's tile, the player's under the key "player".
local function people()
  local t = {}
  local player = emu:read8(S.gPlayerAvatar + S.OFF_AVATAR_OBJECT_EVENT_ID)
  for i = 0, S.NUM_OBJECT_EVENTS - 1 do
    local o = S.gObjectEvents + i * S.OBJECT_EVENT_SIZE
    if emu:read8(o) & 1 == 1 then
      local c = o + S.OFF_OBJ_CURRENT_COORDS
      local key = (i == player) and "player" or ("id" .. emu:read8(o + S.OFF_OBJ_LOCAL_ID))
      t[key] = { s16(emu:read16(c)) - S.MAP_OFFSET, s16(emu:read16(c + 2)) - S.MAP_OFFSET }
    end
  end
  return t
end

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

-- --- The frame recorder -------------------------------------------------------------

local rec          -- the leg being recorded: { dir, n, csv, prev, arrivals, problems }
local function frame()
  rawFrame()
  if not rec then return end
  rec.n = rec.n + 1
  local m, lit = mapId(), litColors()
  local x, y = pos()
  local f = facing()
  local ppl = people()
  emu:screenshot(string.format("%s%04d.png", rec.dir, rec.n))
  rec.csv:write(string.format("%d,%d,%d,%d,%s,%d,%s\n", rec.n, m, x, y, FACING[f] or f, lit,
                              boxUp() and "box" or ""))
  local p = rec.prev
  -- steps the player takes on deck in view (beat 10C should take none)
  if p and p.map == m and m == S.MAP_DECK and lit >= LIT and p.lit >= LIT and p.ppl.player
     and (p.ppl.player[1] ~= x or p.ppl.player[2] ~= y) then
    rec.moves = rec.moves + 1
  end
  if lit >= LIT then
    if p and p.lit >= LIT then
      if p.map ~= m then
        rec.problems[#rec.problems + 1] = string.format("frame %d: the map changes with the screen lit", rec.n)
      else
        for k, v in pairs(ppl) do
          local q = p.ppl[k]
          if q and math.abs(q[1] - v[1]) + math.abs(q[2] - v[2]) > 1 then
            rec.problems[#rec.problems + 1] = string.format("frame %d: %s pops from (%d,%d) to (%d,%d)",
                                                            rec.n, k, q[1], q[2], v[1], v[2])
          end
        end
      end
    end
    -- the first lit frame on each map: where and how the player is shown
    if not p or p.lit < LIT or p.map ~= m then
      rec.arrivals[#rec.arrivals + 1] = { map = m, x = x, y = y, facing = f, n = rec.n }
    end
  end
  rec.prev = { map = m, lit = lit, ppl = ppl }
end
local function wait(n) for _ = 1, n do frame() end end

local function record(leg)
  local dir = OUT .. leg .. "/"
  os.execute("mkdir -p '" .. dir .. "' && rm -f '" .. dir .. "'*.png")
  rec = { dir = dir, n = 0, csv = assert(io.open(dir .. "frames.csv", "w")), arrivals = {}, problems = {}, moves = 0 }
  rec.csv:write("frame,map,x,y,facing,lit,box\n")
  log("recording " .. leg)
end
local function stop()
  local r = rec
  rec = nil
  r.csv:close()
  return r
end
-- Fails on any pop or un-faded warp in the leg just recorded.
local function clean(r, what)
  for _, p in ipairs(r.problems) do log("jump " .. p) end
  expect(#r.problems == 0, what .. ": no warp seen un-faded and nobody pops a tile")
end
local function arrival(r, map)
  for _, a in ipairs(r.arrivals) do if a.map == map then return a end end
  fail("never saw the screen lit on map " .. map)
end

-- --- Input -------------------------------------------------------------------------

local function tap(key, hold)
  emu:addKey(key); wait(hold or 3); emu:clearKey(key); wait(3)
end
local function waitUntil(cond, limit, what)
  local t0 = now()
  while not cond() do
    if now() - t0 > limit then fail("timed out waiting for " .. what) end
    frame()
  end
end
-- A through every box, fade and movement until stopWhen() holds (default: free
-- for 20 frames). A on a YES/NO prompt answers YES.
local function playThrough(stopWhen, limit)
  local t0, calm = now(), 0
  while true do
    if stopWhen and stopWhen() then return end
    if not stopWhen and idle() then
      calm = calm + 1
      if calm >= 20 then return end
      frame()
    else
      calm = 0
      if boxUp() then
        wait(34)
        if stopWhen and stopWhen() then return end
        if boxUp() then tap(K.A) end
        wait(4)
      else
        if not idle() then tap(K.A) end
        wait(6)
      end
    end
    if now() - t0 > (limit or 20000) then fail("stuck playing through a scene") end
  end
end
-- Hold `key` until `cond()` holds (a warp starting), stepping past a follower.
local function holdUntil(key, cond, what)
  emu:addKey(key)
  local t0 = now()
  while not cond() do
    if now() - t0 > 300 then emu:clearKey(key); fail("never warped through " .. what) end
    frame()
  end
  emu:clearKey(key)
end
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

-- --- Setup scripts in EWRAM (aegina_homes.lua's trick) ---------------------------------

local function bytes(t)
  local out = {}
  for _, v in ipairs(t) do
    if type(v) == "table" then
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

  -- The voyage night: off the Euploia at Aigina, sent to the inn. Into the inn
  -- by its door mat (warp 0).
  local setup = { S.SCR_OP_SETFLAG, { S.FLAG_SYS_POKEMON_GET, 2 },
                  S.SCR_OP_SETFLAG, { S.FLAG_ARRIVED_AEGINA, 2 },
                  S.SCR_OP_SETFLAG, { S.FLAG_VISITED_AEGINA, 2 },
                  S.SCR_OP_SETVAR, { S.VAR_REPEL_STEP_COUNT, 2 }, { 999, 2 },
                  S.SCR_OP_CALLNATIVE, { S.ScrCmd_createmon | 1, 4 }, 0, S.PARTY_SIZE,
                  { S.SPECIES_KARKIPOOL, 2 }, { 14, 2 }, { 0, 4 },
                  S.SCR_OP_WARP, S.MAP_INN >> 8, S.MAP_INN & 0xFF, 0, { 0xFFFF, 2 }, { 0xFFFF, 2 },
                  S.SCR_OP_WAITSTATE }
  runRamScript(setup)
  waitUntil(function() return mapId() == S.MAP_INN and idle() end, 4000, "the inn")
  wait(30)
  local x, y = pos()
  expect(x == 11 and y == 11, string.format("in the inn on its door mat (at %d,%d)", x, y))

  -- 1. Out by the mat, and back in by the door
  -- round the follower, then down onto the mat's east half
  walkTo({ { 11, 9 }, { 12, 9 }, { 12, 10 } })
  record("1_inn_to_street")
  holdUntil(K.DOWN, function() return mapId() == S.MAP_AEGINA end, "the inn's mat")
  waitUntil(function() return mapId() == S.MAP_AEGINA and idle() end, 600, "Aigina's street")
  wait(20)
  local r = stop()
  clean(r, "the inn's mat to the street")
  local a = arrival(r, S.MAP_AEGINA)
  x, y = pos()
  expect(x == 15 and y == 17, string.format("out of the inn's door onto the street below it, (15,17) (at %d,%d)", x, y))
  expect(a.x == 15 and (a.y == 16 or a.y == 17) and a.facing == 1,
         string.format("the street lights up with the player in the inn's doorway facing south (%d,%d %s)",
                       a.x, a.y, FACING[a.facing] or a.facing))

  record("2_street_to_inn")
  holdUntil(K.UP, function() return mapId() == S.MAP_INN end, "the inn's door")
  waitUntil(function() return mapId() == S.MAP_INN and idle() end, 600, "the inn again")
  wait(20)
  r = stop()
  clean(r, "the street's door to the inn")
  a = arrival(r, S.MAP_INN)
  expect(a.x == 11 and a.y == 11 and a.facing == 2,
         string.format("the inn lights up with the player on its mat facing north (%d,%d %s)",
                       a.x, a.y, FACING[a.facing] or a.facing))

  -- 2. Endeis and the night, to the deck
  walkTo({ { 11, 7 }, { 7, 7 }, { 5, 7 } })
  tap(K.UP, 16); wait(10)
  tap(K.A); wait(10)
  playThrough(function() return taskRunning("Task_HandleScrollingMultichoiceInput") end)
  wait(20)
  tap(K.A); wait(10)
  -- the rest of the night, until Kleon has gone up to the loft
  playThrough(function() return not objectPresent(S.LOCALID_INN_KLEON) end)
  record("3_night_to_deck")
  playThrough(function() return mapId() == S.MAP_DECK and litColors() >= LIT end)
  wait(60)
  r = stop()
  clean(r, "the night's end to the deck")
  expect(getFlag(S.FLAG_AEGINA_NIGHT), "the night sets FLAG_ICHOR_AEGINA_NIGHT")
  a = arrival(r, S.MAP_DECK)
  expect(a.x == 8 and a.y == 4 and a.facing == 2,
         string.format("the deck lights up with the player at the starboard rail (8,4) facing the coast, north (%d,%d %s)",
                       a.x, a.y, FACING[a.facing] or a.facing))
  expect(r.moves == 0, string.format("nobody walks the player across the deck after the fade-in (%d steps)", r.moves))

  -- 3. Beat 10C, to Emporion's quay
  record("4_last_leg_to_emporion")
  playThrough(function() return mapId() == S.MAP_EMPORION_HARBOR and litColors() >= LIT end)
  wait(90)
  r = stop()
  clean(r, "the last leg to Emporion")
  expect(getFlag(S.FLAG_CROSSING_DONE), "the last leg sets FLAG_ICHOR_CROSSING_DONE")
  a = arrival(r, S.MAP_EMPORION_HARBOR)
  expect(a.x == 30 and a.y == 16 and a.facing == 2,
         string.format("Emporion lights up with the player on the Euploia's berth (30,16) facing the quay, north (%d,%d %s)",
                       a.x, a.y, FACING[a.facing] or a.facing))
  -- nobody walks the player anywhere on deck in 10C: they are already at the rail
  expect(r.moves == 0, string.format("the player stays at the rail through beat 10C (%d steps)", r.moves))
end

local co = coroutine.create(main)
local realEmu = _G.emu
callbacks:add("frame", function()
  if not co then return end
  local result = table.pack(coroutine.resume(co))
  while true do
    if not result[1] then
      local err = tostring(result[2])
      console:log(err:find("^VOYAGE FAIL") and err or ("VOYAGE FAIL: " .. err))
      console:log("VOYAGE done")
      co = nil
      return
    end
    if coroutine.status(co) == "dead" then
      console:log("VOYAGE done")
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
