-- The Herald's Run check, run by tools/ichor/tests/temple_hermes.sh (read it first).
--
-- Plays the Temple of Hermes as a player would, with key presses, and checks the game's
-- state after each beat: the run's temp vars (VAR_TEMP_1 scrolls delivered, VAR_TEMP_2 the
-- glass, VAR_TEMP_3 the run is on, VAR_TEMP_5 flasks of oil), the bank flags, trainer
-- flags, the bag, the music, Kerykos's object, and the herms, turnstiles, gate, torches,
-- table and step-glass in the live map.
--
-- Setup touches no ROM data. After Quickstart it writes a tiny event script into spare
-- EWRAM and points the current map header's script table at it as an ON_FRAME script
-- (temple_trial.lua's trick): give a level-100 Prinplup that knows only Surf (and the
-- first and eighth badges, so it obeys), then warp into the temple. The same trick warps
-- back in for the re-entry check. Two shortcuts, both logged: the glass is set to 32 and
-- then 2 to reach its marks without walking a hundred steps; every other step is walked.
-- Options are set to fast text, Set battle style and no battle animations.
--
-- Prints "HERMES ok ..." per check, "HERMES shot ..." per screenshot, and ends with
-- "HERMES done"; any failure prints "HERMES FAIL: ..." first.

local S = dofile("build/temple_hermes/symbols.lua")
local OUT = "build/temple_hermes/"
local K = { A = C.GBA_KEY.A, B = C.GBA_KEY.B, START = C.GBA_KEY.START, SELECT = C.GBA_KEY.SELECT,
            UP = C.GBA_KEY.UP, DOWN = C.GBA_KEY.DOWN, LEFT = C.GBA_KEY.LEFT, RIGHT = C.GBA_KEY.RIGHT }
local SCRATCH = 0x0203F000  -- spare EWRAM: the linker's EWRAM data ends near 0x02037400
local KERYKOS = 1           -- his local id: the first person in map.json

-- The test reads as straight-line code in a coroutine. mGBA only lets its own
-- functions run on the main Lua thread, so the coroutine asks the frame callback
-- to make each call (yield "call") and to advance a frame (yield "frame").
local emu = setmetatable({}, { __index = function(_, name)
  return function(_, ...) return coroutine.yield("call", name, ...) end
end })
local function log(s) coroutine.yield("log", "HERMES " .. s) end
local function fail(s) error("HERMES FAIL: " .. s, 0) end
local function frame() coroutine.yield("frame") end
local function wait(n) for _ = 1, n do frame() end end
local function now() return emu:currentFrame() end

-- --- Game state ------------------------------------------------------------------------

local function sb1() return emu:read32(S.gSaveBlock1Ptr) end
local function sb2() return emu:read32(S.gSaveBlock2Ptr) end
local function varAddr(v) return sb1() + S.OFF_SB1_VARS + (v - S.VARS_START) * 2 end
local function getVar(v) return emu:read16(varAddr(v)) end
local function setVar(v, value) emu:write16(varAddr(v), value) end
local function getFlag(f)
  if f >= S.ICHOR_FLAGS_START and f <= S.ICHOR_FLAGS_END then
    local o = f - S.ICHOR_FLAGS_START
    local bank = emu:read32(S.gSaveBlock3Ptr) + S.OFF_SB3_ICHOR + S.OFF_ICHOR_FLAGS
    return (emu:read8(bank + (o >> 3)) >> (o & 7)) & 1 == 1
  end
  return (emu:read8(sb1() + S.OFF_SB1_FLAGS + (f >> 3)) >> (f & 7)) & 1 == 1
end
local function defeated(t) return getFlag(S.TRAINER_FLAGS_START + t) end
local function mapId()
  local loc = sb1() + S.OFF_SB1_LOCATION
  return emu:read8(loc) * 256 + emu:read8(loc + 1)
end
local function metatile(x, y)
  local width = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_WIDTH)
  local map = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_MAP)
  return emu:read16(map + 2 * ((x + S.MAP_OFFSET) + (y + S.MAP_OFFSET) * width)) & 0x3FF
end
local function playerObject()
  return S.gObjectEvents + emu:read8(S.gPlayerAvatar + S.OFF_AVATAR_OBJECT_EVENT_ID) * S.OBJECT_EVENT_SIZE
end
local function pos()
  local c = playerObject() + S.OFF_OBJ_CURRENT_COORDS
  return emu:read16(c) - S.MAP_OFFSET, emu:read16(c + 2) - S.MAP_OFFSET
end
local function objectAt(localId)
  for i = 0, S.OBJECT_EVENTS_COUNT - 1 do
    local o = S.gObjectEvents + i * S.OBJECT_EVENT_SIZE
    if emu:read8(o) & 1 == 1 and emu:read8(o + S.OFF_OBJ_LOCAL_ID) == localId then
      local c = o + S.OFF_OBJ_CURRENT_COORDS
      return emu:read16(c) - S.MAP_OFFSET, emu:read16(c + 2) - S.MAP_OFFSET
    end
  end
end
-- Where the map will spawn a person: its template in the save (setobjectxyperm writes it).
-- People far off screen aren't spawned, so this is how to check one there.
local function templateAt(localId)
  for i = 0, S.OBJ_TEMPLATES_COUNT - 1 do
    local t = sb1() + S.OFF_SB1_OBJ_TEMPLATES + i * S.OBJ_TEMPLATE_SIZE
    if emu:read8(t + S.OFF_TEMPLATE_LOCAL_ID) == localId then
      return emu:read16(t + S.OFF_TEMPLATE_X), emu:read16(t + S.OFF_TEMPLATE_Y)
    end
  end
end
local function itemCount(item)
  local bag, key = sb1() + S.OFF_SB1_BAG, emu:read32(sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
  local n = 0
  for i = 0, S.BAG_SLOTS - 1 do
    local slot = bag + i * S.ITEM_SLOT_SIZE
    if emu:read16(slot) == item then n = n + (emu:read16(slot + S.OFF_ITEM_SLOT_QUANTITY) ~ key) end
  end
  return n
end
local function songHeader(id) return emu:read32(S.gSongTable + id * S.SONG_SIZE + S.OFF_SONG_HEADER) end
local function playing(id) return emu:read32(S.gMPlayInfo_BGM + S.OFF_MPLAY_SONGHEADER) == songHeader(id) end
local function mapMusic() return emu:read16(S.sCurrentMapMusic) end
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
local function expectAt(x, y, what)
  local px, py = pos()
  expect(px == x and py == y, string.format("%s (at %d,%d)", what, px, py))
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
    if now() - t0 > limit then fail("timed out waiting for " .. what) end
    frame()
  end
end

-- Press A every 12 frames until the player is free again for 20 frames. A on a
-- YES/NO prompt answers YES, which is what every prompt here wants.
local function settle(limit)
  local t0, calm = now(), 0
  while calm < 20 do
    if idle() then
      calm = calm + 1
      frame()
    else
      calm = 0
      if inBattle() then fail("a battle started while settling") end
      tap(K.A)
      wait(6)
    end
    if now() - t0 > (limit or 20000) then fail("stuck: the player never got control back") end
  end
end

-- One step. Returns false if the game took control (a trainer saw the player, a turnstile
-- refused, the glass spoke) before the step was over. A turnstile passed the right way
-- carries the player a second tile and still counts as one step here.
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
  t0 = now()
  local calm = 0
  while calm < 4 do
    if idle() then calm = calm + 1 else calm = 0 end
    if now() - t0 > 90 then return false end
    frame()
  end
  return true
end

-- Walk a list of waypoints, each in a straight line from the last. Returns false if
-- the walk was interrupted, with the player wherever it stopped.
local function walk(points)
  for _, p in ipairs(points) do
    while true do
      local x, y = pos()
      if x == p[1] and y == p[2] then break end
      local key
      if x < p[1] then key = K.RIGHT elseif x > p[1] then key = K.LEFT
      elseif y < p[2] then key = K.DOWN else key = K.UP end
      if not step(key) then return false end
    end
  end
  return true
end
-- Walk, reading out any message on the way (the glass's marks); a battle is a failure.
local function go(points)
  while not walk(points) do
    wait(30)
    if inBattle() then fail("an unexpected battle") end
    settle()
  end
end

-- Turn toward a blocked tile (a herm, a person, a jar) without moving.
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
-- Speak to what the player faces and play the script out.
local function use(key)
  face(key); tap(K.A); wait(10); settle()
end

-- A trainer battle that the current script is starting. Screenshots the action menu.
local function battle(name, trainer)
  local t0 = now()
  while not inBattle() do
    tap(K.A); wait(9)
    if now() - t0 > 4000 then fail("no battle for " .. name) end
  end
  wait(480)  -- the intro plays itself; the action menu then waits for input
  shot(name)
  t0 = now()
  while not inOverworld() do
    tap(K.A); wait(6)
    if now() - t0 > 20000 then fail("battle never ended: " .. name) end
  end
  expect(emu:read8(S.gBattleOutcome) == S.B_OUTCOME_WON, "won " .. name)
  settle()
  expect(defeated(trainer), "trainer flag set after " .. name)
end

-- --- The temple ------------------------------------------------------------------------------
-- Positions are the room in tools/ichor/maps/temple_hermes.py.

local HEADS = { J1 = { 13, 19 }, J2 = { 1, 18 }, J3 = { 1, 14 }, J4 = { 19, 9 },
                H1 = { 19, 19 }, H2 = { 19, 15 }, H3 = { 1, 8 } }
local SHAFTS = { H1 = { 19, 20 }, H2 = { 19, 16 }, H3 = { 1, 9 } }
local TORCHES = { { 5, 4 }, { 15, 4 } }
local GATE, T5, GLASS, TABLE = { 10, 6 }, { 6, 8 }, { 7, 19 }, { 8, 19 }
local function head(name) return metatile(HEADS[name][1], HEADS[name][2]) end
local function headIs(name, mt, what) expect(head(name) == mt, name .. "'s head " .. what) end
local function delivered() return getVar(S.VAR_DELIVERED) end
local function glass() return getVar(S.VAR_GLASS) end
local function running() return getVar(S.VAR_RUNNING) == 1 end

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
-- Run `script` (a byte list) as the current map's ON_FRAME script.
local function runRamScript(script)
  local tableAddr, frameTable, code = SCRATCH, SCRATCH + 0x20, SCRATCH + 0x40
  poke(code, script)
  poke(frameTable, { { S.VAR_TEMP_0, 2 }, { 0, 2 }, { code, 4 }, { 0, 2 } })
  poke(tableAddr, { S.MAP_SCRIPT_ON_FRAME_TABLE, { frameTable, 4 }, 0 })
  emu:write32(S.gMapHeader + S.OFF_MAPHEADER_MAPSCRIPTS, tableAddr)
end
-- warp map, 0 (the door mat), then wait for the warp as the expansion requires
local function warpScript(map)
  return { S.SCR_OP_WARP, map >> 8, map & 0xFF, 0, { 0xFFFF, 2 }, { 0xFFFF, 2 }, S.SCR_OP_WAITSTATE }
end
local function enterTemple()
  waitUntil(function() return mapId() == S.MAP_TEMPLE and idle() end, 4000, "the temple")
  wait(30)
end

-- Speak to Kerykos by the oil jar and say YES: the scrolls, and the glass begins.
local function startRun(label)
  go({ { 8, 21 } }); face(K.UP); tap(K.A); wait(60)
  shot(label)
  settle()
  expect(running() and glass() == 120 and delivered() == 0, "the run is on: 120 steps in the glass")
  expect(objectAt(KERYKOS) == nil, "Kerykos took the short way")
  expect(metatile(TABLE[1], TABLE[2]) == S.MT_TABLE_EMPTY, "the scrolls are off the table")
end

-- Oil a junction herm the player faces (YES), and check its head turned.
local function oil(key, name, flag, want, label)
  face(key); tap(K.A); wait(40)
  if label then shot(label) end
  settle()
  expect(getFlag(flag), name .. " is oiled")
  headIs(name, want, "turned to point the way")
end

local function deliver(key, name, n, label)
  face(key); tap(K.A); wait(60)
  shot(label)
  settle()
  expect(delivered() == n, string.format("%s took scroll %d", name, n))
end

local function main()
  -- Boot, skip the intro, Quickstart (the smoke test's timing).
  waitUntil(function() return now() >= 500 end, 600, "frame 500")
  tap(K.START)
  waitUntil(function() return now() >= 1020 end, 600, "frame 1020")
  tap(K.SELECT)
  waitUntil(idle, 4000, "the new game")
  wait(30)

  -- Fast text, Set battle style, no battle animations.
  local opt = sb2() + S.OFF_SB2_OPTIONS
  emu:write16(opt, (emu:read16(opt) & ~0x7) | 2 | (1 << 9) | (1 << 10))

  local setup = { S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 },
                  S.SCR_OP_CALLNATIVE, { S.ScrCmd_createmon | 1, 4 }, 0, S.PARTY_SIZE,
                  { S.SPECIES_TEST, 2 }, { 100, 2 }, { (1 << 17) | (1 << 18) | (1 << 19) | (1 << 20), 4 },
                  { S.MOVE_TEST, 2 }, { S.MOVE_NONE, 2 }, { S.MOVE_NONE, 2 }, { S.MOVE_NONE, 2 },
                  S.SCR_OP_SETFLAG, { S.FLAG_SYS_POKEMON_GET, 2 },
                  S.SCR_OP_SETFLAG, { S.FLAG_BADGE01_GET, 2 },
                  -- A level-100 mon obeys only with the eighth badge. The second (the
                  -- Herald Laurel) stays unset: Kerykos gives it.
                  S.SCR_OP_SETFLAG, { S.FLAG_BADGE08_GET, 2 } }
  for _, b in ipairs(warpScript(S.MAP_TEMPLE)) do setup[#setup + 1] = b end
  setup[#setup + 1] = S.SCR_OP_END
  runRamScript(setup)
  enterTemple()

  -- The door, before anything.
  expectAt(10, 23, "arrived on the door mat")
  expect(not running() and not getFlag(S.FLAG_RUN_DONE), "no run yet")
  expect(metatile(GATE[1], GATE[2]) == S.MT_GATE_SHUT, "the dais gate is shut")
  expect(metatile(GLASS[1], GLASS[2]) == S.MT_GLASS, "the step-glass is on its stand")
  expect(metatile(TABLE[1], TABLE[2]) == S.MT_TABLE_FULL, "the scrolls are on Kerykos's table")
  headIs("J1", S.MT_HEAD_S, "faces straight out, unoiled")
  expect(objectAt(KERYKOS) == 8, "Kerykos waits by the oil jar")
  expect(mapMusic() == S.MUS_TEMPLE_HERMES, "the temple plays the Herald's Run")
  shot("01_entry.png")

  -- Angelos, inside the door.
  go({ { 10, 22 }, { 11, 22 } }); face(K.RIGHT); tap(K.A); wait(60)
  shot("02_angelos.png"); settle()

  -- The step-glass, then the oil jar three times.
  go({ { 11, 21 }, { 7, 21 } }); face(K.UP); tap(K.A); wait(40)
  shot("03_step_glass.png"); settle()
  go({ { 9, 21 } })
  for i = 1, 3 do
    face(K.UP); tap(K.A); wait(40)
    if i == 1 then shot("04_oil_jar.png") end
    settle()
  end
  expect(getVar(S.VAR_OIL) == 3, "three flasks of oil")

  -- Kerykos's rite, YES: the first run.
  startRun("05_kerykos_rite.png")
  expect(getFlag(S.FLAG_RUN_TOLD), "Kerykos told the rite")

  -- The turnstile out of the loop room turns east only: west into it, it refuses.
  go({ { 7, 21 }, { 6, 21 }, { 6, 22 } })
  expect(glass() == 117, "three steps off the glass")
  expect(not step(K.LEFT), "the turnstile west of the door stops the player")
  wait(30); shot("06_turnstile_refuses.png"); settle()
  expectAt(6, 22, "stepped back off the turnstile")
  expect(glass() == 115, "onto the turnstile and back: two more steps")

  -- J1, by the door: oiled, it points east, to the first herald-herm.
  go({ { 6, 21 }, { 13, 21 } })
  oil(K.UP, "J1", S.FLAG_HERM_J1, S.MT_HEAD_OILED_E, "07_oil_j1.png")
  expect(getVar(S.VAR_OIL) == 2, "the herm took a flask")
  shot("08_j1_points_east.png")

  -- The glass's marks, then dry. The glass is set to 32 (logged) rather than walked down.
  setVar(S.VAR_GLASS, 32)
  log("set the glass to 32 steps")
  go({ { 12, 21 } })
  expect(glass() == 31, "a step off the glass")
  expect(not step(K.LEFT), "the glass speaks at 30")
  wait(30); shot("09_glass_low.png"); settle()
  setVar(S.VAR_GLASS, 2)
  log("set the glass to 2 steps")
  go({ { 10, 21 } })
  expect(not step(K.LEFT), "the last grain falls")
  wait(40)
  expect(mapMusic() == 0, "the music stops dead")
  shot("10_last_grain.png")
  tap(K.A); wait(40); tap(K.A); wait(40)
  shot("11_kerykos_late.png")
  local t0 = now()
  while not (idle() and select(2, pos()) == 22) do
    if now() - t0 > 3000 then fail("never back at the door") end
    if not idle() then tap(K.A) end
    wait(10)
  end
  wait(30)
  expectAt(10, 22, "back at the door")
  expect(not running() and delivered() == 0, "the scrolls are Kerykos's again")
  expect(getFlag(S.FLAG_RUN_FAILED), "the failed run is remembered")
  expect(getFlag(S.FLAG_HERM_J1), "J1 stays oiled")
  headIs("J1", S.MT_HEAD_OILED_E, "still points east")
  expect(objectAt(KERYKOS) == 8, "Kerykos is back by the oil jar")
  expect(metatile(TABLE[1], TABLE[2]) == S.MT_TABLE_FULL, "the scrolls are back on the table")
  expect(playing(S.MUS_TEMPLE_HERMES), "the Herald's Run plays again")
  shot("12_back_at_the_door.png")

  -- Angelos has a hint now.
  go({ { 11, 22 } }); face(K.RIGHT); tap(K.A); wait(60)
  shot("13_angelos_hint.png"); settle()

  -- Fill up again (the flasks were left behind), then the second run.
  go({ { 11, 21 }, { 9, 21 } })
  for _ = 1, 3 do use(K.UP) end
  expect(getVar(S.VAR_OIL) == 3, "three flasks again")
  startRun("14_second_run.png")

  -- Leg 1, the lower gallery: the porch's track east, T1, Podarge, H1.
  go({ { 14, 21 } })
  step(K.RIGHT)   -- through T1 and into Podarge's sight
  battle("15_podarge_battle.png", S.TRAINER_PODARGE)
  expectAt(16, 21, "carried through T1")
  go({ { 16, 20 }, { 18, 20 } })
  expect(glass() == 109, "the first leg, eleven steps")
  deliver(K.RIGHT, "H1", 1, "16_h1_doorway.png")
  expect(metatile(SHAFTS.H1[1], SHAFTS.H1[2]) == S.MT_SHAFT_SCROLL, "H1 holds its scroll")
  expect(metatile(TORCHES[1][1], TORCHES[1][2]) == S.MT_TORCH_LIT, "the first relay torch is lit")
  headIs("J1", S.MT_HEAD_OILED_W, "turned to point west, to H2")

  -- Leg 2: back west through T1b, J2 and the turnstile stair.
  go({ { 18, 18 }, { 17, 18 } })
  expect(step(K.LEFT), "through T1b, west")
  expectAt(15, 18, "carried through T1b")
  go({ { 2, 18 } })
  oil(K.LEFT, "J2", S.FLAG_HERM_J2, S.MT_HEAD_OILED_N, "17_oil_j2.png")
  expect(step(K.UP), "up the turnstile stair")
  expectAt(2, 16, "carried up to the middle gallery")
  go({ { 2, 14 } })
  oil(K.LEFT, "J3", S.FLAG_HERM_J3, S.MT_HEAD_OILED_N, "18_oil_j3.png")
  go({ { 2, 13 }, { 3, 13 } })
  expect(step(K.RIGHT), "through T3, east")
  go({ { 10, 13 }, { 10, 14 } })
  shot("19_the_gap.png")
  step(K.DOWN)    -- through the gap and into Euchidas's sight
  battle("20_euchidas_battle.png", S.TRAINER_EUCHIDAS)
  go({ { 10, 16 }, { 15, 16 }, { 15, 15 } })
  expect(step(K.RIGHT), "through T4, east")
  go({ { 18, 15 } })
  deliver(K.RIGHT, "H2", 2, "21_h2_sandal.png")
  expect(metatile(TORCHES[2][1], TORCHES[2][2]) == S.MT_TORCH_LIT, "the second relay torch is lit")
  headIs("J2", S.MT_HEAD_OILED_N, "still points up, to H3")

  -- Leg 3: the east stair, J4, T5, H3.
  go({ { 18, 13 }, { 18, 10 } })
  oil(K.RIGHT, "J4", S.FLAG_HERM_J4, S.MT_HEAD_OILED_N, "22_oil_j4.png")
  expect(getVar(S.VAR_OIL) == 0, "every flask used")
  go({ { 18, 8 }, { 7, 8 } })
  expect(metatile(T5[1], T5[2]) == S.MT_TURN_W, "T5 turns west")
  expect(step(K.LEFT), "through T5, west")
  go({ { 2, 8 } })
  local left = glass()
  log(string.format("the glass at H3: %d of 120 steps left", left))
  expect(left > 0 and running(), "made H3 with sand to spare")
  deliver(K.LEFT, "H3", 3, "23_h3_purse.png")
  wait(20); shot("24_third_scroll.png"); settle()
  expect(getFlag(S.FLAG_RUN_DONE) and not running(), "the run is done and the glass stopped")
  expect(metatile(GATE[1], GATE[2]) == S.MT_GATE_OPEN, "the dais gate is open")
  expect(metatile(T5[1], T5[2]) == S.MT_TURN_E, "T5 turned round")
  for _, j in ipairs({ "J1", "J2", "J3", "J4" }) do headIs(j, S.MT_HEAD_OILED_N, "faces the dais") end
  for _, h in ipairs({ "H1", "H2", "H3" }) do headIs(h, S.MT_HEAD_N, "faces the dais") end
  local kx, ky = objectAt(KERYKOS)
  expect(kx == 10 and ky == 3, "Kerykos is already on his dais")
end

local function afterTheRun()
  -- Back east through the turned T5.
  go({ { 5, 8 } })
  expect(step(K.RIGHT), "through T5, east now")
  expectAt(7, 8, "carried through T5")

  -- Philonides, optional, facing the wall: in through T6b, which now turns west.
  go({ { 18, 8 }, { 18, 11 }, { 17, 11 } })
  expect(step(K.LEFT), "through T6b, west now")
  expectAt(15, 11, "carried through T6b")
  expect(not defeated(S.TRAINER_PHILONIDES), "Philonides never saw the player")
  go({ { 4, 11 } }); face(K.UP); tap(K.A); wait(60)
  shot("25_philonides_intro.png")
  battle("26_philonides_battle.png", S.TRAINER_PHILONIDES)
  go({ { 15, 11 }, { 15, 10 } })
  expect(step(K.RIGHT), "out through T6, east now")
  expectAt(17, 10, "carried through T6")

  -- Up the steps, through the open gate, across the lectern from Kerykos.
  go({ { 18, 10 }, { 18, 8 }, { 10, 8 }, { 10, 5 } })
  shot("27_dais.png")
  local function hermesFavor()
    return emu:read8(emu:read32(S.gSaveBlock3Ptr) + S.OFF_SB3_ICHOR + S.OFF_ICHOR_FAVOR + S.ICHOR_GOD_HERMES)
  end
  local favorBeforeLaurel = hermesFavor()
  face(K.UP); tap(K.A); wait(60)
  shot("28_kerykos_on_the_dais.png")
  local t0 = now()
  while not inBattle() do
    tap(K.A); wait(9)
    if now() - t0 > 6000 then fail("no battle with Kerykos") end
  end
  wait(480)
  expect(playing(S.MUS_BATTLE_HIEROPHANT), "the Hierophant battle music (the rival theme, stubbed)")
  shot("29_kerykos_battle.png")
  while not inOverworld() do tap(K.A); wait(6) end
  expect(emu:read8(S.gBattleOutcome) == S.B_OUTCOME_WON, "beat Kerykos")
  t0 = now()
  while not getFlag(S.FLAG_BADGE02_GET) do
    tap(K.A); wait(12)
    if now() - t0 > 3000 then fail("no Herald Laurel") end
  end
  wait(70); shot("30_herald_laurel.png")
  while not getFlag(S.FLAG_GOT_TM_AERIAL_ACE) do
    tap(K.A); wait(12)
    if now() - t0 > 6000 then fail("no TM40") end
  end
  wait(70); shot("31_tm40_aerial_ace.png")
  while not getFlag(S.FLAG_HERMES_OFFERING) do
    tap(K.A); wait(12)
    if now() - t0 > 9000 then fail("no Honey") end
  end
  wait(40); shot("32_honey.png")
  settle()
  expect(defeated(S.TRAINER_KERYKOS), "Kerykos's trainer flag")
  expect(itemCount(S.ITEM_TM40) == 1, "TM40 Aerial Ace in the bag")
  expect(itemCount(S.ITEM_HONEY) == 1, "a Honey in the bag")
  expect(hermesFavor() == math.min(favorBeforeLaurel + S.ICHOR_FAVOR_LAUREL, 100),
         "the Herald Laurel grants Hermes exactly 15 Favor")
  expect(defeated(S.TRAINER_PODARGE) and defeated(S.TRAINER_EUCHIDAS) and defeated(S.TRAINER_PHILONIDES),
         "every acolyte counts as beaten")
  expect(metatile(GLASS[1], GLASS[2]) == S.MT_GLASS_GONE, "the step-glass is put away")

  -- Again: his list, and the short way down.
  face(K.UP); tap(K.A); wait(60)
  shot("33_kerykos_after.png")
  settle()
  wait(30)
  expectAt(10, 22, "the short way down, to the door")
  shot("34_short_way_down.png")
  expect(hermesFavor() == math.min(favorBeforeLaurel + S.ICHOR_FAVOR_LAUREL, 100),
         "talking again does not repeat the Laurel Favor")

  -- Re-entry: the room stays solved.
  local back = warpScript(S.MAP_TEMPLE)
  back[#back + 1] = S.SCR_OP_END
  setVar(S.VAR_TEMP_0, 0)
  runRamScript(back)
  waitUntil(function() return select(2, pos()) == 23 end, 4000, "the re-entry")
  enterTemple()
  expect(metatile(GATE[1], GATE[2]) == S.MT_GATE_OPEN, "on re-entry the gate is open")
  expect(metatile(T5[1], T5[2]) == S.MT_TURN_E, "on re-entry T5 still turns east")
  expect(metatile(GLASS[1], GLASS[2]) == S.MT_GLASS_GONE, "on re-entry the glass is still put away")
  headIs("J1", S.MT_HEAD_OILED_N, "on re-entry still faces the dais")
  local kx, ky = templateAt(KERYKOS)
  expect(kx == 10 and ky == 3, "on re-entry Kerykos's place is his dais")
  go({ { 10, 22 }, { 10, 19 } }); wait(10)
  shot("35_reentry.png")
  go({ { 11, 19 }, { 11, 22 } }); face(K.RIGHT); tap(K.A); wait(60)
  shot("36_angelos_after.png"); settle()
end

local co = coroutine.create(function()
  main()
  afterTheRun()
end)

local realEmu = _G.emu
callbacks:add("frame", function()
  if not co then return end
  local result = table.pack(coroutine.resume(co))
  while true do
    if not result[1] then
      local err = tostring(result[2])
      console:log(err:find("^HERMES FAIL") and err or ("HERMES FAIL: " .. err))
      console:log("HERMES done")
      co = nil
      return
    end
    if coroutine.status(co) == "dead" then
      console:log("HERMES done")
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
