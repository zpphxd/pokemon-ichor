-- The Hearth Trial check, run by tools/ichor/tests/temple_trial.sh (read it first).
--
-- Plays the Temple of Hestia as a player would, with key presses, and checks the
-- game's state after each beat: VAR_ICHOR_HEARTH_TRIAL, the trial flags, trainer
-- flags, and the brazier and cord metatiles in the live map.
--
-- Setup touches no ROM data. After Quickstart, it writes a tiny event script into
-- spare EWRAM (above everything the linker places there) and points the current
-- map header's script table at it as an ON_FRAME script. The game runs it on the
-- next frame: give a level-100 Prinplup that knows only Surf (and the eighth
-- badge, so it obeys), then warp into the temple. The same trick warps back in for the re-entry check. Options are set to
-- fast text, Set battle style and no battle animations.
--
-- Prints "TEMPLE ok ..." per check, "TEMPLE shot ..." per screenshot, and ends with
-- "TEMPLE done"; any failure prints "TEMPLE FAIL: ..." first.

local S = dofile("build/temple_trial/symbols.lua")
local OUT = "build/temple_trial/"
local K = { A = C.GBA_KEY.A, B = C.GBA_KEY.B, START = C.GBA_KEY.START, SELECT = C.GBA_KEY.SELECT,
            UP = C.GBA_KEY.UP, DOWN = C.GBA_KEY.DOWN, LEFT = C.GBA_KEY.LEFT, RIGHT = C.GBA_KEY.RIGHT }
local SCRATCH = 0x0203F000  -- spare EWRAM: the linker's EWRAM data ends near 0x02037400

-- The test reads as straight-line code in a coroutine. mGBA only lets its own
-- functions run on the main Lua thread, so the coroutine asks the frame callback
-- to make each call (yield "call") and to advance a frame (yield "frame").
local emu = setmetatable({}, { __index = function(_, name)
  return function(_, ...) return coroutine.yield("call", name, ...) end
end })
local function log(s) coroutine.yield("log", "TEMPLE " .. s) end
local function fail(s) error("TEMPLE FAIL: " .. s, 0) end
local function frame() coroutine.yield("frame") end
local function wait(n) for _ = 1, n do frame() end end
local function now() return emu:currentFrame() end

-- --- Game state ------------------------------------------------------------------------

local function sb1() return emu:read32(S.gSaveBlock1Ptr) end
local function sb2() return emu:read32(S.gSaveBlock2Ptr) end
local function getVar(v) return emu:read16(sb1() + S.OFF_SB1_VARS + (v - S.VARS_START) * 2) end
local function getFlag(f) return (emu:read8(sb1() + S.OFF_SB1_FLAGS + (f >> 3)) >> (f & 7)) & 1 == 1 end
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
      tap(K.A)
      wait(6)
    end
    if now() - t0 > (limit or 20000) then fail("stuck: the player never got control back") end
  end
end

-- Press A on whatever the player faces and play the script out.
local function use()
  tap(K.A); wait(10); settle()
end

-- One step. Returns false if the game took control (a trainer saw the player, or
-- a trigger fired) before the step was over.
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
  -- Trainer sight and triggers run on the frame after a step ends, so the player
  -- only counts as free once it has stayed free for a few frames.
  t0 = now()
  local calm = 0
  while calm < 4 do
    if idle() then calm = calm + 1 else calm = 0 end
    if now() - t0 > 60 then return false end
    frame()
  end
  return true
end

-- Walk a list of waypoints, each in a straight line from the last.
-- Returns false if the walk was interrupted, with the player wherever it stopped.
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
local function walkTo(points)
  if not walk(points) then
    local x, y = pos()
    fail(string.format("walk interrupted at (%d,%d)", x, y))
  end
end

-- Turn toward a blocked tile (a brazier, the hearth, a person) without moving.
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

-- A trainer battle that starts from the current script. Screenshots the action menu.
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

-- --- The temple ---------------------------------------------------------------------------

-- Each brazier: its bowl (x, y) and its cold legs metatile (lit = cold + 1). A lit
-- brazier also warms the floor under its legs (BrazierLight_Below); a cold one
-- leaves plain floor there. Positions are the room in tools/ichor/maps/temple.py.
local BRAZIERS = {
  door = { 13, 3, 0x242 }, table = { 3, 3, 0x244 }, loom = { 3, 16, 0x246 }, bed = { 13, 16, 0x248 },
  dais_l = { 7, 7, 0x24A }, dais_r = { 9, 7, 0x24A },
}
local CORD = { 8, 7 }
local FLOOR, LIGHT_BELOW = 0x201, 0x281
local function isLit(name)
  local b = BRAZIERS[name]
  return metatile(b[1], b[2]) == 0x241 and metatile(b[1], b[2] + 1) == b[3] + 1
     and metatile(b[1], b[2] + 2) == LIGHT_BELOW
end
local function isCold(name)
  local b = BRAZIERS[name]
  return metatile(b[1], b[2]) == 0x240 and metatile(b[1], b[2] + 1) == b[3]
     and metatile(b[1], b[2] + 2) == FLOOR
end
local function expectRoom(lit, what)
  for _, name in ipairs({ "door", "table", "loom", "bed", "dais_l", "dais_r" }) do
    if lit[name] then
      if not isLit(name) then fail(what .. ": " .. name .. " should be lit") end
    elseif not isCold(name) then
      fail(what .. ": " .. name .. " should be cold")
    end
  end
  local cord = metatile(CORD[1], CORD[2])
  if lit.cord_gone then
    if cord ~= 0x204 then fail(what .. ": the cord should be gone") end
  elseif cord ~= 0x207 then
    fail(what .. ": the cord should be up")
  end
  log("ok room " .. what)
end
local function trial() return getVar(S.VAR_HEARTH_TRIAL) end

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
                  -- A level-100 mon obeys only with the eighth badge. The first badge
                  -- (the Hearth Laurel) stays unset: Ione gives it.
                  S.SCR_OP_SETFLAG, { S.FLAG_BADGE08_GET, 2 } }
  for _, b in ipairs(warpScript(S.MAP_TEMPLE)) do setup[#setup + 1] = b end
  setup[#setup + 1] = S.SCR_OP_END
  runRamScript(setup)
  enterTemple()

  local x, y = pos()
  expect(x == 8 and y == 23, "arrived on the door mat")
  expect(trial() == 0, "no flame on arrival")
  expectRoom({}, "on arrival")
  shot("01_entry.png")

  -- Euboulos, then the hymn.
  walkTo({ { 8, 22 } }); face(K.RIGHT); tap(K.A); wait(90)
  shot("02_euboulos.png"); settle()
  walkTo({ { 8, 21 }, { 7, 21 } }); face(K.LEFT); tap(K.A); wait(90)
  shot("03_stele_hymn.png"); settle()

  -- Up beside the runner, out of Lampon's sight: he won't let go of the hearth yet.
  walkTo({ { 7, 15 } }); face(K.UP); tap(K.A); wait(90)
  shot("04_hearth_hands_off.png"); settle()
  expect(trial() == 0, "no flame before Lampon is beaten")

  face(K.RIGHT); tap(K.A); wait(90)
  shot("05_lampon_intro.png")
  battle("06_lampon_battle.png", S.TRAINER_LAMPON)

  -- Take a flame, then lose it at the door.
  face(K.UP); tap(K.A); wait(90); tap(K.A); wait(90)  -- the hearth, then the question
  shot("07_take_flame.png"); settle()
  expect(trial() == 1, "carrying a flame")
  expect(not walk({ { 7, 23 } }), "the door mat stops a torch-bearer")
  wait(40); shot("08_torch_sputters.png"); settle()
  expect(trial() == 0, "the torch went out at the door")

  -- Take it again; Door first, then a wrong brazier (the Bed) puts everything out.
  walkTo({ { 7, 15 } }); face(K.UP); use()
  expect(trial() == 1, "carrying a flame again")
  walkTo({ { 7, 16 }, { 11, 16 }, { 11, 9 }, { 13, 9 }, { 13, 5 } }); face(K.UP); use()
  expect(trial() == 2, "the Door brazier is first")
  expectRoom({ door = true }, "after the Door")
  shot("09_door_lit.png")
  -- the plaque, "Light it?", YES, then the braziers die
  walkTo({ { 13, 15 } }); face(K.DOWN); tap(K.A); wait(90); tap(K.A); wait(90); tap(K.A); wait(220)
  shot("10_wrong_brazier.png"); settle()
  expect(trial() == 0, "a wrong brazier ends the run")
  expectRoom({}, "after the wrong brazier")

  -- The right order: Door, Pyrrha on the way, Table, Loom, Aithra, Bed.
  walkTo({ { 13, 13 }, { 10, 13 } }); face(K.LEFT); use()
  expect(trial() == 1, "a third flame")
  walkTo({ { 10, 9 }, { 13, 9 }, { 13, 5 } }); face(K.UP); use()
  expect(trial() == 2, "the Door again")
  walkTo({ { 13, 9 }, { 5, 9 }, { 5, 11 } })
  expect(not walk({ { 5, 12 } }), "Pyrrha sees the player")
  battle("11_pyrrha_battle.png", S.TRAINER_PYRRHA)
  expect(trial() == 2 and isLit("door"), "the flame survives a battle")
  walkTo({ { 5, 9 }, { 4, 9 }, { 4, 8 }, { 3, 8 }, { 3, 5 } }); face(K.UP); use()
  expect(trial() == 3, "the Table is second")
  shot("12_table_lit.png")
  walkTo({ { 3, 15 } }); face(K.DOWN); use()
  expect(trial() == 4, "the Loom is third")
  shot("13_loom_lit.png")
  walkTo({ { 3, 13 }, { 5, 13 }, { 5, 17 }, { 9, 17 } })
  expect(not walk({ { 10, 17 } }), "Aithra sees the player")
  battle("14_aithra_battle.png", S.TRAINER_AITHRA)
  walkTo({ { 10, 16 }, { 12, 16 } }); face(K.RIGHT); use()
  expect(trial() == 5, "the Bed is fourth")
  expectRoom({ door = true, table = true, loom = true, bed = true }, "with all four lit")
  shot("15_bed_lit.png")

  -- Euboulos knows the last flame is still owed.
  walkTo({ { 10, 16 }, { 10, 19 }, { 9, 19 }, { 9, 21 } }); face(K.DOWN); tap(K.A); wait(90)
  shot("16_euboulos_owed.png"); settle()

  -- The last flame goes home.
  walkTo({ { 9, 15 } }); face(K.UP); tap(K.A); wait(90)
  shot("17_return_flame.png")
  tap(K.A); wait(16)       -- YES: the flare, under a white flash
  shot("18_flare.png")
  wait(160)
  shot("19_hearth_roars.png")
  tap(K.A); wait(260)      -- the camera climbs to the dais
  shot("20_dais_open.png")
  tap(K.A); wait(260)      -- and comes back
  shot("21_ashes.png")
  tap(K.A)
  waitUntil(function() return getFlag(S.FLAG_GOT_CHARCOAL) end, 600, "the Charcoal")
  wait(60)
  shot("22_charcoal.png"); settle()
  expect(getFlag(S.FLAG_TRIAL_DONE) and trial() == 6, "the trial is done")
  expect(getFlag(S.FLAG_GOT_CHARCOAL), "got the Charcoal")
  expectRoom({ door = true, table = true, loom = true, bed = true, dais_l = true, dais_r = true, cord_gone = true },
             "after the trial")

  -- Up through the burnt cord to Ione.
  walkTo({ { 10, 15 }, { 10, 9 }, { 8, 9 } })
  shot("23_way_open.png")
  walkTo({ { 8, 5 } }); face(K.UP); tap(K.A); wait(90)
  shot("24_ione_intro.png")
end

-- Ione's rewards need screenshots mid-scene, so her battle is played by hand here.
local function ioneAndAfter()
  local t0 = now()
  while not inBattle() do
    tap(K.A); wait(9)
    if now() - t0 > 6000 then fail("no battle with Ione") end
  end
  wait(480)
  shot("25_ione_battle.png")
  while not inOverworld() do tap(K.A); wait(6) end
  expect(emu:read8(S.gBattleOutcome) == S.B_OUTCOME_WON, "beat Ione")
  t0 = now()
  while not getFlag(S.FLAG_BADGE01_GET) do
    tap(K.A); wait(12)
    if now() - t0 > 3000 then fail("no Hearth Laurel") end
  end
  wait(70); shot("26_hearth_laurel.png")
  while not getFlag(S.FLAG_GOT_TM_FACADE) do
    tap(K.A); wait(12)
    if now() - t0 > 6000 then fail("no TM42") end
  end
  wait(70); shot("27_tm42_facade.png")
  settle()
  expect(defeated(S.TRAINER_IONE), "Ione's trainer flag")

  tap(K.A); wait(90); shot("28_ione_after.png"); settle()

  -- Kanthos, tied by the side door.
  walkTo({ { 8, 9 }, { 13, 9 }, { 13, 5 }, { 14, 5 }, { 14, 3 } }); face(K.RIGHT); tap(K.A); wait(90)
  shot("29_kanthos.png"); settle()

  -- Out through the door mat to Akti, then back in: the room stays solved.
  walkTo({ { 14, 5 }, { 13, 5 }, { 13, 9 }, { 10, 9 }, { 10, 17 }, { 8, 17 }, { 8, 23 } })
  emu:addKey(K.DOWN)
  waitUntil(function() return mapId() == S.MAP_AKTI end, 400, "Akti")
  emu:clearKey(K.DOWN)
  waitUntil(idle, 2000, "Akti to load")
  wait(20); shot("30_akti_outside.png")
  local back = warpScript(S.MAP_TEMPLE)
  back[#back + 1] = S.SCR_OP_END
  runRamScript(back)
  enterTemple()
  expectRoom({ door = true, table = true, loom = true, bed = true, dais_l = true, dais_r = true, cord_gone = true },
             "on re-entry")
  walkTo({ { 8, 19 } }); wait(10)
  shot("31_reentry.png")
end

local co = coroutine.create(function()
  main()
  ioneAndAfter()
end)

local realEmu = _G.emu
callbacks:add("frame", function()
  if not co then return end
  local result = table.pack(coroutine.resume(co))
  while true do
    if not result[1] then
      local err = tostring(result[2])
      console:log(err:find("^TEMPLE FAIL") and err or ("TEMPLE FAIL: " .. err))
      console:log("TEMPLE done")
      co = nil
      return
    end
    if coroutine.status(co) == "dead" then
      console:log("TEMPLE done")
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
