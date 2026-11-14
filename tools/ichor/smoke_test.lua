-- Pokemon Ichor smoke test.
-- Run by tools/ichor/smoke_test.sh in build/tools/ichor-mgba-headless.
--
-- Boots the ROM twice and saves screenshots to build/smoke/:
--   1. NEW GAME from the main menu: Daphne's speech (her portrait, Smoliv, the
--      THEO/IANTHE menu, the naming screen), then waking on 2F in Elaia.
--   2. After a reset, Quickstart (SELECT on the title screen) straight to 2F,
--      and the start menu.
-- Both runs check that the player wakes on 2F with Elaia's theme playing.
-- It reads game state through build/smoke/symbols.lua (tools/ichor/tests/
-- elaia_symbols.sh), so it waits on the game rather than on fixed frame counts.
-- Prints "SMOKE ok ..." per check and ends with "SMOKE done"; a failure prints
-- "SMOKE FAIL: ..." first.

local S = dofile("build/smoke/symbols.lua")
local OUT = "build/smoke/"
local K = { A = C.GBA_KEY.A, B = C.GBA_KEY.B, START = C.GBA_KEY.START, SELECT = C.GBA_KEY.SELECT }

-- Straight-line test code in a coroutine; the frame callback makes mGBA calls for it.
local emu = setmetatable({}, { __index = function(_, name)
  return function(_, ...) return coroutine.yield("call", name, ...) end
end })
local function log(s) coroutine.yield("log", "SMOKE " .. s) end
local function fail(s) error("SMOKE FAIL: " .. s, 0) end
local function frame() coroutine.yield("frame") end
local function wait(n) for _ = 1, n do frame() end end

local function callback2() return emu:read32(S.gMain + S.OFF_MAIN_CALLBACK2) end
local function on(cb) return callback2() == (S[cb] | 1) end
local function idle()
  return on("CB2_Overworld") and emu:read8(S.sLockFieldControls) == 0
     and emu:read8(S.sGlobalScriptContextStatus) == 2
end
local function mapId()
  local loc = emu:read32(S.gSaveBlock1Ptr) + S.OFF_SB1_LOCATION
  return emu:read8(loc) * 256 + emu:read8(loc + 1)
end
local function taskRunning(name)
  if not S[name] then return false end -- the linker dropped it: nothing can run it
  for i = 0, S.NUM_TASKS - 1 do
    local t = S.gTasks + i * S.TASK_SIZE
    if emu:read8(t + S.OFF_TASK_ACTIVE) ~= 0 and emu:read32(t + S.OFF_TASK_FUNC) == (S[name] | 1) then
      return true
    end
  end
  return false
end
local function tap(key, hold) emu:addKey(key); wait(hold or 4); emu:clearKey(key); wait(4) end
local function shot(name) emu:screenshot(OUT .. name); log("shot " .. name) end
local function waitFor(cond, limit, what)
  for _ = 1, limit do
    if cond() then return end
    frame()
  end
  fail("timed out waiting for " .. what)
end
local function expect(cond, what)
  if not cond then fail(what) end
  log("ok " .. what)
end

-- The live 2F grid matches its layout file cell for cell: nothing (like Hoenn's
-- truck intro, which wrote its door into cells (4,1)-(4,3)) has stamped over it.
local function bedroomIntact()
  local f = io.open("data/layouts/ElaiaVillage_PlayersHouse_2F/map.bin", "rb")
  if not f then fail("can't read the 2F layout") end
  local data = f:read("a")
  f:close()
  local width = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_WIDTH)
  local map = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_MAP)
  local w = width - (2 * S.MAP_OFFSET + 1)  -- MAP_OFFSET_W
  for i = 0, #data // 2 - 1 do
    local want = string.unpack("<I2", data, 2 * i + 1) & 0x3FF
    local x, y = i % w, i // w
    local got = emu:read16(map + 2 * ((x + S.MAP_OFFSET) + (y + S.MAP_OFFSET) * width)) & 0x3FF
    if got ~= want then return false, x, y end
  end
  return true
end

local function wokeAtHome(how)
  -- the truck intro shook the camera from its own task for ~10 seconds
  local shook = false
  for _ = 1, 3000 do
    if taskRunning("Task_HandleTruckSequence") then shook = true end
    if idle() then break end
    frame()
  end
  expect(idle(), how .. ": the player has control")
  expect(not shook, how .. ": no truck intro (no camera shake)")
  expect(mapId() == S.MAP_HOUSE_2F, how .. ": woke on 2F")
  expect(emu:read16(S.sCurrentMapMusic) == S.MUS_ELAIA, how .. ": Elaia's theme from the first frame")
  wait(30)
  local ok, x, y = bedroomIntact()
  expect(ok, how .. ": the bedroom is as built" .. (ok and "" or string.format(" (cell %d,%d differs)", x, y)))
end

local function main()
  -- 1. NEW GAME and Daphne's speech
  wait(500); tap(K.START)                                  -- skip the intro
  wait(500); shot("01_title.png")
  tap(K.A)
  waitFor(function() return on("CB2_MainMenu") end, 600, "the main menu")
  wait(90); tap(K.A)                                       -- NEW GAME
  wait(520)                                                -- Daphne fades in and greets you
  local presses, shots = 0, { [3] = "02_daphne.png", [9] = "03_smoliv.png", [15] = "04_myth.png" }
  local gender = false
  for _ = 1, 60 do
    if idle() then break end
    if on("CB2_NamingScreen") then
      wait(40); shot("06_naming.png"); tap(K.START); wait(20); tap(K.A); wait(60)
    elseif not gender and taskRunning("Task_NewGameBirchSpeech_ChooseGender") then
      gender = true
      wait(20); shot("05_theo_or_ianthe.png"); tap(K.A); wait(40)
    else
      presses = presses + 1
      if shots[presses] then shot(shots[presses]) end
      tap(K.A); wait(150)                                  -- let each box print in full
    end
  end
  wokeAtHome("new game")
  shot("07_new_game.png")

  -- 2. Quickstart, after a reset
  emu:reset()
  wait(500); tap(K.START)
  wait(500); tap(K.SELECT)                                 -- Quickstart from the title
  wokeAtHome("Quickstart")
  shot("08_quickstart.png")
  tap(K.START); wait(60); shot("09_start_menu.png"); tap(K.B)
end

local co = coroutine.create(main)
local realEmu = _G.emu
callbacks:add("frame", function()
  if not co then return end
  local result = table.pack(coroutine.resume(co))
  while true do
    if not result[1] then
      local err = tostring(result[2])
      console:log(err:find("^SMOKE FAIL") and err or ("SMOKE FAIL: " .. err))
      console:log("SMOKE done")
      co = nil
      return
    end
    if coroutine.status(co) == "dead" then
      console:log("SMOKE done") -- the runner stops on this line
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
