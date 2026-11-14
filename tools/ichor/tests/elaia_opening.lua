-- The opening check, run by tools/ichor/tests/elaia_opening.sh (read it first).
--
-- Plays a NEW GAME as a player would, with key presses, from Daphne's speech to
-- the road north out of Elaia, and checks the game's state after each beat:
-- the map, the player's tile, the story flags, the map music, the party.
--
-- Env: ELAIA_STARTER 0 Snivy, 1 Cyndaquil, 2 Piplup; ELAIA_OUTCOME win (Kleon's
-- starter is put on 1 HP), lose (the player's is), or any (played straight);
-- ELAIA_OUT the screenshot folder; ELAIA_SYMBOLS the table elaia_symbols.sh wrote.
--
-- Walking uses a breadth-first search over the live map grid (collision bits and
-- the people standing on it), one step at a time, so the route follows the map
-- as it is built rather than coordinates written down here.
--
-- Prints "ELAIA ok ..." per check, "ELAIA shot ..." per screenshot, and ends with
-- "ELAIA done"; any failure prints "ELAIA FAIL: ..." first.

local S = dofile(os.getenv("ELAIA_SYMBOLS") or "build/elaia_opening/symbols.lua")
local OUT = os.getenv("ELAIA_OUT") or "build/elaia_opening/"
local STARTER = tonumber(os.getenv("ELAIA_STARTER") or "0")
local OUTCOME = os.getenv("ELAIA_OUTCOME") or "any"
local K = { A = C.GBA_KEY.A, B = C.GBA_KEY.B, START = C.GBA_KEY.START, SELECT = C.GBA_KEY.SELECT,
            UP = C.GBA_KEY.UP, DOWN = C.GBA_KEY.DOWN, LEFT = C.GBA_KEY.LEFT, RIGHT = C.GBA_KEY.RIGHT }

-- The test reads as straight-line code in a coroutine. mGBA only lets its own
-- functions run on the main Lua thread, so the coroutine asks the frame callback
-- to make each call (yield "call") and to advance a frame (yield "frame").
local emu = setmetatable({}, { __index = function(_, name)
  return function(_, ...) return coroutine.yield("call", name, ...) end
end })
local function log(s) coroutine.yield("log", "ELAIA " .. s) end
local function fail(s) error("ELAIA FAIL: " .. s, 0) end
local function frame() coroutine.yield("frame") end
local function wait(n) for _ = 1, n do frame() end end
local function now() return emu:currentFrame() end

-- --- Game state ------------------------------------------------------------------------

local function sb1() return emu:read32(S.gSaveBlock1Ptr) end
local function sb2() return emu:read32(S.gSaveBlock2Ptr) end
local function getVar(v) return emu:read16(sb1() + S.OFF_SB1_VARS + (v - S.VARS_START) * 2) end
local function getFlag(f) return (emu:read8(sb1() + S.OFF_SB1_FLAGS + (f >> 3)) >> (f & 7)) & 1 == 1 end
local function mapId()
  local loc = sb1() + S.OFF_SB1_LOCATION
  return emu:read8(loc) * 256 + emu:read8(loc + 1)
end
local function mapMusic() return emu:read16(S.sCurrentMapMusic) end
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
local function on(cb) return callback2() == (S[cb] | 1) end
local CONTEXT_SHUTDOWN = 2
local function idle()
  return inOverworld()
     and emu:read8(S.sLockFieldControls) == 0
     and emu:read8(S.sGlobalScriptContextStatus) == CONTEXT_SHUTDOWN
     and emu:read8(S.gPlayerAvatar + S.OFF_AVATAR_TILE_TRANSITION) == 0
end
local function taskRunning(name)
  for i = 0, S.NUM_TASKS - 1 do
    local t = S.gTasks + i * S.TASK_SIZE
    if emu:read8(t + S.OFF_TASK_ACTIVE) ~= 0 and emu:read32(t + S.OFF_TASK_FUNC) == (S[name] | 1) then
      return true
    end
  end
  return false
end
local function partyMon(slot) return S.gParties + slot * S.POKEMON_SIZE end
local function partyHp(slot)
  local m = partyMon(slot)
  return emu:read16(m + S.OFF_MON_HP), emu:read16(m + S.OFF_MON_MAXHP)
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
local shots = 0
local function shot(name)
  shots = shots + 1
  local file = string.format("%02d_%s.png", shots, name)
  emu:screenshot(OUT .. file)
  log("shot " .. file)
end

local function waitUntil(cond, limit, what)
  local t0 = now()
  while not cond() do
    if now() - t0 > limit then fail("timed out waiting for " .. what) end
    frame()
  end
end

-- A naming screen (the player's name, or a nickname): keep the offered name.
local function acceptName(what)
  wait(40)
  shot(what)
  tap(K.START); wait(20); tap(K.A)
  waitUntil(function() return not on("CB2_NamingScreen") end, 600, "the naming screen to close")
end

-- Play out whatever the game is doing until the player is free again for 20
-- frames. A on a YES/NO answers YES. While a message box is up, each box gets
-- time to print in full before A, so `at` can map message-box counts to
-- screenshot names, taken just before that box is dismissed.
local function boxUp() return emu:read8(S.sFieldMessageBoxMode) ~= 0 end
local function settle(at, limit)
  local t0, calm, boxes = now(), 0, 0
  at = at or {}
  while calm < 20 do
    if idle() then
      calm = calm + 1
      frame()
    else
      calm = 0
      if on("CB2_NamingScreen") then
        acceptName("naming")
      elseif on("CB2_WallClock") then
        -- CONFIRM, then "Is this the correct time?" offers NO first
        wait(30); tap(K.A); wait(40); tap(K.UP); wait(10); tap(K.A)
        waitUntil(function() return not on("CB2_WallClock") end, 600, "the water clock to close")
      elseif boxUp() then
        wait(34)                                 -- fast text: a full box prints in this
        if boxUp() then
          boxes = boxes + 1
          if at[boxes] then shot(at[boxes]) end
          tap(K.A)
        end
        wait(4)
      else
        tap(K.A)                                 -- a cutscene, a fanfare, a menu
        wait(6)
      end
    end
    if now() - t0 > (limit or 20000) then
      shot("stuck")
      fail(string.format("stuck: the player never got control back (callback2 %08x, lock %d, script %d)",
                         callback2(), emu:read8(S.sLockFieldControls), emu:read8(S.sGlobalScriptContextStatus)))
    end
  end
end

-- One step. Returns false if the game took control (a trigger fired) before the
-- step was over.
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
  if x == x0 and y == y0 then
    if not idle() then return false end
    fail(string.format("blocked at (%d,%d)", x0, y0))
  end
  t0 = now()
  local calm = 0
  while calm < 4 do
    if idle() then calm = calm + 1 else calm = 0 end
    if now() - t0 > 60 then return false end
    frame()
  end
  return true
end

-- --- Walking by the live map ----------------------------------------------------------------

local LEDGES = { [0x087] = true, [0x08D] = true, [0x08E] = true, [0x0D5] = true, [0x0D6] = true }
local function blockedMap()
  local width = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_WIDTH)
  local map = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_MAP)
  local people = {}
  local me = emu:read8(S.gPlayerAvatar + S.OFF_AVATAR_OBJECT_EVENT_ID)
  for i = 0, S.OBJECT_EVENTS_COUNT - 1 do
    local o = S.gObjectEvents + i * S.OBJECT_EVENT_SIZE
    if i ~= me and emu:read8(o) & 1 == 1 then
      local c = o + S.OFF_OBJ_CURRENT_COORDS
      people[(emu:read16(c) - S.MAP_OFFSET) .. "," .. (emu:read16(c + 2) - S.MAP_OFFSET)] = true
    end
  end
  return function(x, y)
    if x < 0 or y < 0 or x >= width - (2 * S.MAP_OFFSET + 1) then return true end
    local block = emu:read16(map + 2 * ((x + S.MAP_OFFSET) + (y + S.MAP_OFFSET) * width))
    return block & S.MAPGRID_COLLISION_MASK ~= 0 or LEDGES[block & 0x3FF] or people[x .. "," .. y]
  end
end

local DIRS = { { 0, -1, K.UP }, { 0, 1, K.DOWN }, { -1, 0, K.LEFT }, { 1, 0, K.RIGHT } }
-- The first key on a shortest path from the player to (tx, ty), or nil.
local function firstStep(tx, ty, avoid)
  local blocked = blockedMap()
  local sx, sy = pos()
  local key = function(x, y) return x .. "," .. y end
  local seen, queue, head = { [key(sx, sy)] = "start" }, { { sx, sy } }, 1
  while head <= #queue do
    local x, y = queue[head][1], queue[head][2]
    head = head + 1
    if x == tx and y == ty then
      while true do
        local from = seen[key(x, y)]
        if from[1] == sx and from[2] == sy then return from[3] end
        x, y = from[1], from[2]
      end
    end
    for _, d in ipairs(DIRS) do
      local nx, ny = x + d[1], y + d[2]
      local k = key(nx, ny)
      local avoided = avoid and nx >= avoid[1] and ny >= avoid[2] and nx <= avoid[3] and ny <= avoid[4]
      if not seen[k] and not avoided and ((nx == tx and ny == ty) or not blocked(nx, ny)) then
        seen[k] = { x, y, d[3] }
        queue[#queue + 1] = { nx, ny }
      end
    end
  end
  return nil
end

-- Walk to (tx, ty), keeping out of the `avoid` rectangle {x0, y0, x1, y1} if
-- given. Returns false if a script took over on the way.
local function go(tx, ty, avoid)
  for _ = 1, 200 do
    local x, y = pos()
    if x == tx and y == ty then return true end
    local k = firstStep(tx, ty, avoid)
    if not k then fail(string.format("no path from (%d,%d) to (%d,%d)", x, y, tx, ty)) end
    if not step(k) then return false end
  end
  fail("never arrived")
end
local function goTo(tx, ty, avoid)
  if not go(tx, ty, avoid) then
    local x, y = pos()
    fail(string.format("walk to (%d,%d) interrupted at (%d,%d)", tx, ty, x, y))
  end
end

-- Walk into a warp (a door, the stairs, an exit mat) and wait for the next map.
-- With `scene`, a scene starts on arrival, so don't wait for control.
local function enter(key, map, what, scene)
  emu:addKey(key)
  waitUntil(function() return mapId() == map end, 400, what)
  emu:clearKey(key)
  if scene then
    waitUntil(inOverworld, 600, "the field after " .. what)
    wait(60)
  else
    waitUntil(idle, 600, "control after " .. what)
    wait(20)
  end
end

-- Turn toward a blocked tile without moving.
local function face(key) tap(key, 16); wait(10) end

-- --- The battle -------------------------------------------------------------------------

local function kleonBattle(at)
  local t0, boxes = now(), 0
  while not inBattle() do
    if boxUp() then
      wait(34)
      boxes = boxes + 1
      if at[boxes] then shot(at[boxes]) end
    end
    tap(K.A); wait(9)
    if now() - t0 > 6000 then fail("no battle with Kleon") end
  end
  wait(420)  -- the intro plays itself; the action menu then waits for input
  shot("kleon_battle")
  -- Decide it: whoever is put on 1 HP goes down to the first hit.
  if OUTCOME == "win" then
    emu:write16(S.gBattleMons + 1 * S.BATTLE_MON_SIZE + S.OFF_BATTLE_MON_HP, 1)
  elseif OUTCOME == "lose" then
    emu:write16(S.gBattleMons + 0 * S.BATTLE_MON_SIZE + S.OFF_BATTLE_MON_HP, 1)
  end
  t0 = now()
  local midShot = false
  while not inOverworld() do
    tap(K.A); wait(6)
    if not midShot and now() - t0 > 700 then shot("kleon_battle_late"); midShot = true end
    if now() - t0 > 20000 then fail("the battle never ended") end
  end
  return emu:read8(S.gBattleOutcome)
end

-- --- A script of our own --------------------------------------------------------------------

-- Spare EWRAM: the linker's EWRAM data ends near 0x02037500.
local SCRATCH = 0x0203F000
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
-- Run `script` (a byte list) as the current map's ON_FRAME script, once.
local function runRamScript(script)
  local tableAddr, frameTable, code = SCRATCH, SCRATCH + 0x20, SCRATCH + 0x40
  poke(code, script)
  poke(frameTable, { { S.VAR_TEMP_0, 2 }, { 0, 2 }, { code, 4 }, { 0, 2 } })
  poke(tableAddr, { S.MAP_SCRIPT_ON_FRAME_TABLE, { frameTable, 4 }, 0 })
  emu:write32(S.gMapHeader + S.OFF_MAPHEADER_MAPSCRIPTS, tableAddr)
end

-- --- The opening ----------------------------------------------------------------------------

local SPECIES = { [0] = "Snivy", [1] = "Cyndaquil", [2] = "Piplup" }
-- Kleon takes the starter that beats yours (SCRIPT.md beat 3).
local KLEON_TAKES = { [0] = 1, [1] = 2, [2] = 0 }

local function main()
  log(string.format("note starter %s, outcome %s", SPECIES[STARTER], OUTCOME))
  -- Boot, skip the intro, then NEW GAME from the main menu (a fresh save has no CONTINUE).
  waitUntil(function() return now() >= 500 end, 600, "frame 500")
  tap(K.START)
  waitUntil(function() return now() >= 1000 end, 600, "frame 1000")
  tap(K.A)
  waitUntil(function() return on("CB2_MainMenu") end, 600, "the main menu")
  wait(60)
  shot("main_menu")
  tap(K.A)

  -- Daphne's speech: A through it, Theo at the gender menu, keep the offered name.
  local t0, presses, genderShot = now(), 0, false
  while not (inOverworld() and idle()) do
    if on("CB2_NamingScreen") then
      acceptName("speech_naming")
    elseif taskRunning("Task_NewGameBirchSpeech_ChooseGender") and not genderShot then
      wait(20); shot("speech_gender"); genderShot = true
      tap(K.A); wait(30)
    else
      presses = presses + 1
      if presses == 3 or presses == 5 or presses == 8 or presses == 17 or presses == 22 then
        shot("speech")
      end
      tap(K.A); wait(36)
    end
    if now() - t0 > 30000 then fail("Daphne's speech never ended") end
  end
  wait(30)
  -- Fast text from here on, so the scenes don't take all day.
  local opt = sb2() + S.OFF_SB2_OPTIONS
  emu:write16(opt, (emu:read16(opt) & ~0x7) | 2)

  -- Beat 1A: the player's room.
  expect(mapId() == S.MAP_HOUSE_2F, "woke on 2F")
  expectAt(5, 5, "by the kline")
  local name = {}
  for i = 0, 3 do name[#name + 1] = emu:read8(sb2() + S.OFF_SB2_NAME + i) end
  -- THEO in the game's charset, then the terminator
  expect(emu:read8(sb2() + S.OFF_SB2_GENDER) == 0 and name[1] == 0xCE and name[2] == 0xC2 and name[3] == 0xBF
         and name[4] == 0xC9 and emu:read8(sb2() + S.OFF_SB2_NAME + 4) == 0xFF, "the player is Theo, named THEO")
  waitUntil(function() return mapMusic() == S.MUS_ELAIA end, 120, "Elaia's music in the bedroom")
  log("ok Elaia's music plays in the bedroom")
  shot("bedroom")
  goTo(8, 3)
  expect(not step(K.UP), "the stair gate stops the player")
  wait(40); shot("mom_calls_upstairs"); settle()
  expectAt(8, 3, "stepped back from the stairs")
  goTo(4, 2); face(K.UP); tap(K.A); wait(60)
  shot("water_clock")
  waitUntil(function() tap(K.A); wait(20); return on("CB2_WallClock") end, 2000, "the water clock")
  wait(60); shot("water_clock_ui")
  settle()
  expect(getFlag(S.FLAG_SET_WATER_CLOCK), "the water clock is set")
  goTo(8, 2)
  enter(K.UP, S.MAP_HOUSE_1F, "the stairs down", true)

  -- Beat 1B: Mom, the Talaria and the pilgrim's story.
  shot("mom_comes_over")
  settle({ [3] = "mom_klotheia", [7] = "talaria", [13] = "mom_oracle" })
  expect(getFlag(S.FLAG_TALKED_TO_MOM), "Mom has spoken")
  expect(getFlag(S.FLAG_SYS_B_DASH), "the Talaria (running) are on")
  shot("downstairs")
  goTo(5, 8)
  enter(K.DOWN, S.MAP_ELAIA, "the front door")
  expectAt(5, 9, "out of the front door")
  expect(mapMusic() == S.MUS_ELAIA, "Elaia's theme in the village")
  shot("front_door")

  -- Kydippe next door, and her Oran Berries.
  goTo(17, 7)
  enter(K.UP, S.MAP_KYDIPPE, "Kydippe's door")
  goTo(2, 3); face(K.UP); tap(K.A); wait(60)
  shot("kydippe")
  settle({ [2] = "kydippe_delivered_you" })
  expect(getFlag(S.FLAG_GOT_KYDIPPE_ORAN), "Kydippe's Oran Berries")
  goTo(4, 7)
  enter(K.DOWN, S.MAP_ELAIA, "Kydippe's door out")
  expectAt(17, 7, "out of Kydippe's house")

  -- The Akademia's door is shut until the thread is read (round Halia's line).
  local HALIA_RING = { 10, 14, 18, 20 }
  expect(not go(5, 30, HALIA_RING), "the note on the Akademia door")
  wait(40); shot("akademia_note"); settle()
  local nx, ny = pos()
  expect(not (nx == 5 and ny == 30) and mapId() == S.MAP_ELAIA, "stepped back from the door")
  expect(not getFlag(S.FLAG_THREAD_READ), "the thread is still unread")

  -- The north gate turns the player back without a partner.
  goTo(11, 3, HALIA_RING)
  expect(not step(K.UP), "the old shepherd stops the player")
  wait(30); shot("shepherd_gate"); settle()
  expectAt(11, 3, "turned back from the road")

  -- Beat 2: Halia reads the threads.
  expect(not go(14, 18), "Halia calls the player into line")
  wait(30); shot("halia_calls")
  settle({ [3] = "korinna_reading", [8] = "philon_reading", [12] = "your_hand_silence", [14] = "turn_around",
           [16] = "your_own_business" })
  expect(getFlag(S.FLAG_THREAD_READ), "the thread is read")
  expectAt(14, 16, "at the head of the line")
  shot("after_the_reading")

  -- Beat 3: the Akademia.
  goTo(5, 30)
  enter(K.UP, S.MAP_AKADEMIA, "the Akademia door", true)
  expect(mapMusic() == S.MUS_AKADEMIA, "the Akademia's lyre theme")
  shot("akademia_alethea")
  -- Alethea, Daphne's question, then the starter screen.
  t0, presses = now(), 0
  while not on("CB2_StarterChoose") do
    if boxUp() then
      wait(34)
      presses = presses + 1
      if presses == 6 then shot("daphne_question") end
    end
    tap(K.A); wait(12)
    if now() - t0 > 8000 then fail("no starter screen") end
  end
  wait(90); shot("starter_screen")
  if STARTER == 0 then tap(K.LEFT) elseif STARTER == 2 then tap(K.RIGHT) end
  wait(30); tap(K.A); wait(60); shot("starter_confirm"); tap(K.A)
  waitUntil(inOverworld, 1200, "the Akademia after the starter screen")
  settle({ [1] = "daphne_on_the_starter", [7] = "pokedex", [10] = "kleon_arrives", [14] = "kleon_chooses",
           [19] = "he_did_not_ask" })
  expect(getVar(S.VAR_STARTER_MON) == STARTER, "VAR_STARTER_MON is " .. SPECIES[STARTER])
  expect(getFlag(S.FLAG_GOT_STARTER) and getFlag(S.FLAG_SYS_POKEMON_GET), "got a partner")
  expect(getFlag(S.FLAG_SYS_POKEDEX_GET), "got the Pokedex")
  expect(getFlag(S.FLAG_KLEON_TOOK_STARTER), "Kleon took his")
  local hide = { [0] = S.FLAG_HIDE_KRATER_SNIVY, [1] = S.FLAG_HIDE_KRATER_CYNDAQUIL, [2] = S.FLAG_HIDE_KRATER_PIPLUP }
  local third = 3 - STARTER - KLEON_TAKES[STARTER]
  expect(getFlag(hide[STARTER]) and getFlag(hide[KLEON_TAKES[STARTER]]) and not getFlag(hide[third]),
         "the last krater stays: " .. SPECIES[third])
  shot("last_krater")
  goTo(10, 12)
  enter(K.DOWN, S.MAP_ELAIA, "the Akademia's door out")
  expectAt(5, 30, "out of the Akademia")

  -- Beat 4: Kleon in the square.
  expect(not getFlag(S.FLAG_HIDE_KLEON_ELAIA), "Kleon waits in the square")
  shot("kleon_waits")
  expect(not go(14, 19), "Kleon calls the player at the steps")
  wait(40); shot("kleon_there_you_are")
  local outcome = kleonBattle({ [4] = "kleon_oracle", [6] = "kleon_battle_me" })
  if OUTCOME == "win" then expect(outcome == S.B_OUTCOME_WON, "beat Kleon")
  elseif OUTCOME == "lose" then expect(outcome == S.B_OUTCOME_LOST, "lost to Kleon")
  else log("note battle outcome " .. outcome) end
  waitUntil(inOverworld, 600, "the square after the battle")
  expect(mapId() == S.MAP_ELAIA, "still in Elaia after the battle, win or lose")
  wait(30); shot("after_the_battle")
  settle({ [4] = "gylippos", [8] = "alethea_arrives", [9] = "alethea_heals", [14] = "kronion_hill" })
  expect(getFlag(S.FLAG_KLEON_BATTLE_1_DONE), "the first battle is done")
  expect(getFlag(S.FLAG_WON_KLEON_1) == (outcome == S.B_OUTCOME_WON), "the win flag matches the outcome")
  expect(getFlag(S.FLAG_GOT_POKEBALLS), "Alethea's Poke Balls")
  expect(not getFlag(S.FLAG_NO_WHITEOUT), "the no-whiteout flag is cleared")
  local hp, maxHp = partyHp(0)
  expect(hp == maxHp and hp > 0, string.format("Alethea healed the partner (%d/%d)", hp, maxHp))
  expect(getFlag(S.FLAG_HIDE_KLEON_ELAIA) and getFlag(S.FLAG_HIDE_ALETHEA_ELAIA), "Kleon and Alethea have gone north")
  expect(mapMusic() == S.MUS_ELAIA, "Elaia's theme again")
  shot("square_after")

  -- The road north is open.
  goTo(11, 1)
  shot("north_gate_open")
  enter(K.UP, S.MAP_ROUTE1, "Route 1")
  shot("route1")

  -- Whiting out sends the player home, where Mom feeds everyone.
  for slot = 0, S.PARTY_SIZE - 1 do emu:write16(partyMon(slot) + S.OFF_MON_HP, 0) end
  runRamScript({ S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 },
                 S.SCR_OP_CALLNATIVE, { S.SetCB2WhiteOut | 1, 4 }, S.SCR_OP_WAITSTATE, S.SCR_OP_END })
  waitUntil(function() return mapId() == S.MAP_HOUSE_1F and inOverworld() end, 3000, "home after whiting out")
  wait(90); shot("whiteout_home")
  settle({ [1] = "whiteout_mom" })
  expectAt(3, 4, "woke by the hearth")
  hp, maxHp = partyHp(0)
  expect(hp == maxHp and hp > 0, string.format("Mom healed the party (%d/%d)", hp, maxHp))
  expect(mapMusic() == S.MUS_ELAIA, "Elaia's theme at home")
end

local co = coroutine.create(main)

local realEmu = _G.emu
callbacks:add("frame", function()
  if not co then return end
  local result = table.pack(coroutine.resume(co))
  while true do
    if not result[1] then
      local err = tostring(result[2])
      console:log(err:find("^ELAIA FAIL") and err or ("ELAIA FAIL: " .. err))
      console:log("ELAIA done")
      co = nil
      return
    end
    if coroutine.status(co) == "dead" then
      console:log("ELAIA done")
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
