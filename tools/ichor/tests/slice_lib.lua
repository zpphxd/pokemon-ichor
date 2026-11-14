-- Shared helpers for the slice playthrough and its side checks (load with dofile).
--
--   local L = dofile("tools/ichor/tests/slice_lib.lua")
--   L.init{ tag = "SLICE", out = "build/slice/", symbols = "build/slice/symbols.lua" }
--   L.start(function() ... end)
--
-- A test reads as straight-line code in a coroutine. mGBA only lets its own
-- functions run on the main Lua thread, so the coroutine asks the frame callback
-- to make each call (yield "call") and to advance a frame (yield "frame").
--
-- Everything here plays with key presses only. Walking is a breadth-first search
-- over the live map grid (collision bits, metatile behaviors, ledges, the people
-- standing on it, warps and story triggers), one step at a time, so a route
-- follows the map as it is built. A step that the grid says is open but the game
-- refuses is remembered for that map and logged as a NOTE, and the walk replans.
--
-- Log lines: "<TAG> ok ...", "<TAG> shot ...", "<TAG> NOTE ...", "<TAG> TEXT ..."
-- (every field message as raw game-charset hex, for slice_text_report.py),
-- "<TAG> BATTLE ...", and "<TAG> FAIL: ..." on a failure. The run ends with
-- "<TAG> done".

local L = {}
local S, OUT, TAG
L.K = { A = C.GBA_KEY.A, B = C.GBA_KEY.B, START = C.GBA_KEY.START, SELECT = C.GBA_KEY.SELECT,
        UP = C.GBA_KEY.UP, DOWN = C.GBA_KEY.DOWN, LEFT = C.GBA_KEY.LEFT, RIGHT = C.GBA_KEY.RIGHT }
local K = L.K

local emu = setmetatable({}, { __index = function(_, name)
  return function(_, ...) return coroutine.yield("call", name, ...) end
end })
L.emu = emu

function L.init(opts)
  TAG = opts.tag
  OUT = opts.out
  S = dofile(opts.symbols)
  L.S = S
  L.OUT = OUT
end

-- --- Logging and checks --------------------------------------------------------------

-- Frames since the script started, counted here: emu:currentFrame() starts
-- again from zero after emu:reset().
local frames = 0
function L.log(s) coroutine.yield("log", TAG .. " " .. s) end
function L.fail(s) error(TAG .. " FAIL: " .. s, 0) end
function L.frame() coroutine.yield("frame"); frames = frames + 1 end
function L.wait(n) for _ = 1, n do L.frame() end end
function L.now() return frames end
local log, fail, frame, wait, now = L.log, L.fail, L.frame, L.wait, L.now

function L.expect(cond, what)
  if not cond then fail(what) end
  log("ok " .. what)
end
-- A finding that does not stop the run: QA reads these from the log.
function L.note(s) log("NOTE " .. s) end
-- A failed check that doesn't block play: logged as BUG and counted, the run
-- carries on to the end, and the run fails there. expect() is for the checks
-- the rest of the run depends on.
L.bugs = 0
function L.check(cond, what)
  if cond then log("ok " .. what) return true end
  L.bugs = L.bugs + 1
  log("BUG " .. what)
  return false
end

function L.waitUntil(cond, limit, what)
  local t0 = now()
  while not cond() do
    if now() - t0 > limit then fail("timed out waiting for " .. what) end
    frame()
  end
end
local waitUntil = L.waitUntil

-- --- Game state ------------------------------------------------------------------------

function L.sb1() return emu:read32(S.gSaveBlock1Ptr) end
function L.sb2() return emu:read32(S.gSaveBlock2Ptr) end
function L.getVar(v) return emu:read16(L.sb1() + S.OFF_SB1_VARS + (v - S.VARS_START) * 2) end
function L.getFlag(f) return (emu:read8(L.sb1() + S.OFF_SB1_FLAGS + (f >> 3)) >> (f & 7)) & 1 == 1 end
function L.defeated(t) return L.getFlag(S.TRAINER_FLAGS_START + t) end
function L.mapId()
  local loc = L.sb1() + S.OFF_SB1_LOCATION
  return emu:read8(loc) * 256 + emu:read8(loc + 1)
end
function L.mapMusic() return emu:read16(S.sCurrentMapMusic) end
function L.money()
  return emu:read32(L.sb1() + S.OFF_SB1_MONEY) ~ emu:read32(L.sb2() + S.OFF_SB2_ENCRYPTION_KEY)
end
-- How many of an item the bag holds, across all pockets.
function L.itemCount(item)
  local bag, key = L.sb1() + S.OFF_SB1_BAG, emu:read32(L.sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
  local n = 0
  for i = 0, S.BAG_SLOTS - 1 do
    local slot = bag + i * S.ITEM_SLOT_SIZE
    if emu:read16(slot) == item then n = n + (emu:read16(slot + S.OFF_ITEM_SLOT_QUANTITY) ~ key) end
  end
  return n
end
function L.lastHeal()
  local a = L.sb1() + S.OFF_SB1_LAST_HEAL
  local function s16(v) if v >= 0x8000 then return v - 0x10000 end return v end
  return emu:read8(a) * 256 + emu:read8(a + 1), s16(emu:read16(a + 4)), s16(emu:read16(a + 6))
end

function L.playerObject()
  return S.gObjectEvents + emu:read8(S.gPlayerAvatar + S.OFF_AVATAR_OBJECT_EVENT_ID) * S.OBJECT_EVENT_SIZE
end
function L.pos()
  local c = L.playerObject() + S.OFF_OBJ_CURRENT_COORDS
  return emu:read16(c) - S.MAP_OFFSET, emu:read16(c + 2) - S.MAP_OFFSET
end
-- facingDirection is the low nibble of byte 0x18 (DIR_SOUTH 1, NORTH 2, WEST 3, EAST 4)
function L.facing() return emu:read8(L.playerObject() + 0x18) & 0xF end
-- The object event with this local id, if it is on the map.
function L.objectAt(localId)
  for i = 0, S.OBJECT_EVENTS_COUNT - 1 do
    local o = S.gObjectEvents + i * S.OBJECT_EVENT_SIZE
    if emu:read8(o) & 1 == 1 and emu:read8(o + S.OFF_OBJ_LOCAL_ID) == localId then
      local c = o + S.OFF_OBJ_CURRENT_COORDS
      return emu:read16(c) - S.MAP_OFFSET, emu:read16(c + 2) - S.MAP_OFFSET
    end
  end
end

-- Whether a person or object (not the player or the follower) stands on (x, y).
function L.objectOn(x, y)
  local me = emu:read8(S.gPlayerAvatar + S.OFF_AVATAR_OBJECT_EVENT_ID)
  for i = 0, S.OBJECT_EVENTS_COUNT - 1 do
    local o = S.gObjectEvents + i * S.OBJECT_EVENT_SIZE
    if i ~= me and emu:read8(o) & 1 == 1 and emu:read8(o + S.OFF_OBJ_LOCAL_ID) ~= S.OBJ_EVENT_ID_FOLLOWER then
      local c = o + S.OFF_OBJ_CURRENT_COORDS
      if emu:read16(c) - S.MAP_OFFSET == x and emu:read16(c + 2) - S.MAP_OFFSET == y then return true end
    end
  end
  return false
end

function L.callback2() return emu:read32(S.gMain + S.OFF_MAIN_CALLBACK2) end
function L.on(cb) return S[cb] and L.callback2() == (S[cb] | 1) end
function L.inOverworld() return L.on("CB2_Overworld") end
function L.inBattle() return L.on("BattleMainCB2") end
local CONTEXT_SHUTDOWN = 2
function L.scriptRunning() return emu:read8(S.sGlobalScriptContextStatus) ~= CONTEXT_SHUTDOWN end
function L.idle()
  return L.inOverworld()
     and emu:read8(S.sLockFieldControls) == 0
     and emu:read8(S.sGlobalScriptContextStatus) == CONTEXT_SHUTDOWN
     and emu:read8(S.gPlayerAvatar + S.OFF_AVATAR_TILE_TRANSITION) == 0
end
function L.taskRunning(name)
  if not S[name] then return false end
  for i = 0, S.NUM_TASKS - 1 do
    local t = S.gTasks + i * S.TASK_SIZE
    if emu:read8(t + S.OFF_TASK_ACTIVE) ~= 0 and emu:read32(t + S.OFF_TASK_FUNC) == (S[name] | 1) then
      return true
    end
  end
  return false
end
function L.boxUp() return emu:read8(S.sFieldMessageBoxMode) ~= 0 end
-- What the game is doing, for a failure message: the main callback, the field
-- lock, and the global script's mode, native wait function and script pointer
-- (look the addresses up in pokeemerald.map).
function L.where()
  local ctx = S.sGlobalScriptContext
  return string.format("callback2 %08x, lock %d, script status %d mode %d native %08x at %08x, map %d at %d,%d",
                       L.callback2(), emu:read8(S.sLockFieldControls), emu:read8(S.sGlobalScriptContextStatus),
                       emu:read8(ctx + 1), emu:read32(ctx + 4), emu:read32(ctx + 8), L.mapId(), L.pos())
end

function L.partyMon(slot) return S.gParties + slot * S.POKEMON_SIZE end
function L.partyHp(slot)
  local m = L.partyMon(slot or 0)
  return emu:read16(m + S.OFF_MON_HP), emu:read16(m + S.OFF_MON_MAXHP)
end
function L.partyLevel(slot) return emu:read8(L.partyMon(slot or 0) + S.OFF_MON_LEVEL) end

-- The song the BGM player is playing, as its header address. Several song ids
-- share a header (Ichor re-pointed Hoenn's slots at its own songs), so songs are
-- compared by header, and named by the header's symbol (S.SONG_NAMES).
function L.songHeader(id) return emu:read32(S.gSongTable + id * S.SONG_SIZE + S.OFF_SONG_HEADER) end
function L.playingHeader() return emu:read32(S.gMPlayInfo_BGM + S.OFF_MPLAY_SONGHEADER) end
function L.playing(id) return L.playingHeader() == L.songHeader(id) end
function L.songName(header) return S.SONG_NAMES[header or L.playingHeader()] or "?" end
-- for logs: the playing song's name
function L.song() return L.songName() end

-- --- Screenshots -------------------------------------------------------------------------

local shots = 0
L.beat = "boot"
-- Screenshots are numbered in run order and carry the beat name, so the gallery
-- script can pick a frame per beat: NNNN_<beat>_<name>.png
function L.shot(name)
  shots = shots + 1
  local file = string.format("%04d_%s_%s.png", shots, L.beat, name)
  emu:screenshot(OUT .. "shots/" .. file)
  -- the map and whether it's the plain field (for the gallery's one-frame-per-map sheet)
  local field = L.inOverworld() and not L.boxUp() and emu:read8(S.sLockFieldControls) == 0
  log(string.format("shot %s map %d %s", file, L.mapId(), field and "field" or (L.inBattle() and "battle" or "scene")))
  return file
end
function L.setBeat(name, state)
  L.beat = name
  log("BEAT " .. name)
  if state ~= false and L.statesDir then
    emu:saveStateFile(L.statesDir .. name .. ".ss", 31)
  end
end

-- --- Input -------------------------------------------------------------------------------

function L.tap(key, hold)
  emu:addKey(key); wait(hold or 3); emu:clearKey(key); wait(3)
end
local tap = L.tap

local DIR_OF_KEY = { [K.DOWN] = 1, [K.UP] = 2, [K.LEFT] = 3, [K.RIGHT] = 4 }
-- Turn toward a blocked tile without moving.
function L.face(key)
  if L.facing() == DIR_OF_KEY[key] then return end
  local x0, y0 = L.pos()
  tap(key, 2); wait(8)
  local x, y = L.pos()
  if x ~= x0 or y ~= y0 then fail(string.format("turning moved the player from (%d,%d)", x0, y0)) end
end

-- --- Field messages -------------------------------------------------------------------------

-- The message on screen, as hex in the game's charset (gStringVar4 up to EOS).
local lastText, lastSig
-- A cheap test for a new message: the first 24 bytes of gStringVar4.
local function textSig()
  local t = {}
  for i = 0, 5 do t[#t + 1] = emu:read32(S.gStringVar4 + 4 * i) end
  return table.concat(t, ",")
end
function L.newText()
  local sig = textSig()
  if sig ~= lastSig then lastSig = sig return true end
  return false
end
function L.logText()
  lastSig = textSig()
  local hex, a = {}, S.gStringVar4
  for i = 0, 1023 do
    local b = emu:read8(a + i)
    if b == 0xFF then break end
    hex[#hex + 1] = string.format("%02X", b)
  end
  local s = table.concat(hex)
  if s ~= lastText and #s > 0 then
    lastText = s
    local x, y = L.pos()
    log(string.format("TEXT %d %d,%d %s", L.mapId(), x, y, s))
  end
end

-- --- Battles ---------------------------------------------------------------------------------

function L.isTrainerBattle() return emu:read32(S.gBattleTypeFlags) & S.BATTLE_TYPE_TRAINER ~= 0 end
local function controller(name) return emu:read32(S.gBattlerControllerFuncs) == (S[name] | 1) end

local TRAINERS = { "KLEON_SNIVY", "KLEON_CYNDAQUIL", "KLEON_PIPLUP", "TITYROS", "PHYLLIS", "KOMATAS", "AGIS",
                   "POLYEIDOS", "PETROS", "AMATHOS", "LAMPON", "PYRRHA", "AITHRA", "IONE" }
local function defeatedSet()
  local t = {}
  for _, n in ipairs(TRAINERS) do t[n] = L.defeated(S["TRAINER_" .. n]) end
  return t
end

L.battles = {}
-- Play out a battle that has started (or is starting): trainers are fought with
-- the first move, wild Pokémon are run from. Returns a record of it.
function L.battle()
  local before = defeatedSet()
  waitUntil(L.inBattle, 1200, "the battle to start")
  local trainer = L.isTrainerBattle()
  local rec = { trainer = trainer, song = 0, start = now() }
  local t0, shotTaken, turns = now(), false, 0
  while not L.inOverworld() do
    if L.on("CB2_EvolutionSceneUpdate") then
      tap(K.A); wait(6)
    elseif L.inBattle() and controller("HandleInputChooseAction") then
      if not shotTaken then
        rec.song = L.playingHeader()
        rec.shot = L.shot(trainer and "battle" or "wild_battle")
        shotTaken = true
      end
      turns = turns + 1
      if trainer then
        tap(K.UP); tap(K.LEFT); tap(K.A)     -- FIGHT
      else
        tap(K.DOWN); tap(K.RIGHT); tap(K.A)  -- RUN
      end
      wait(4)
    elseif L.inBattle() and controller("HandleInputChooseMove") then
      if L.battleMode == "lose" then
        tap(K.UP); tap(K.RIGHT); tap(K.A)    -- the second move (a status move: Leer, Growl)
      else
        tap(K.UP); tap(K.LEFT); tap(K.A)     -- the first move
      end
      wait(4)
    else
      tap(K.A); wait(4)
    end
    if now() - t0 > 30000 then L.shot("stuck_battle"); fail("a battle never ended") end
  end
  rec.outcome = emu:read8(S.gBattleOutcome)
  rec.turns = turns
  local after = defeatedSet()
  for _, n in ipairs(TRAINERS) do
    if after[n] and not before[n] then rec.who = n end
  end
  L.battles[#L.battles + 1] = rec
  log(string.format("BATTLE %s %s outcome %d song %s turns %d frames %d", trainer and "trainer" or "wild",
                    rec.who or "-", rec.outcome, L.songName(rec.song), turns, now() - rec.start))
  return rec
end

-- --- Playing a scene out ------------------------------------------------------------------------

-- A naming screen (the player's name, or a nickname): keep the offered name.
function L.acceptName(what)
  wait(40)
  L.shot(what or "naming")
  tap(K.START); wait(20); tap(K.A)
  waitUntil(function() return not L.on("CB2_NamingScreen") end, 600, "the naming screen to close")
end

-- Play out whatever the game is doing until the player is free again for 20
-- frames. Options:
--   shots   = { [n] = "name" }  screenshot the nth message box before it is dismissed
--   answers = { "yes", "no", "down", ... } for successive YES/NO prompts and
--             multichoice menus (default: YES / the first choice)
--   every   = true              screenshot every message box (beat_text_NN)
--   limit   = frames before giving up
-- Returns the number of message boxes and the battles fought.
-- A script that waits on the same thing for this long, while A is pressed, is a
-- softlock. By default that fails the run. With SLICE_WORKAROUNDS=1 a stuck
-- waitmovement is released (logged as a BUG) so the rest of the slice can still
-- be checked; the run still fails at the end.
L.workarounds = os.getenv("SLICE_WORKAROUNDS") == "1"
local SOFTLOCK_FRAMES = 2400
local function softlockCheck(state)
  local ctx = S.sGlobalScriptContext
  local mode, native, ptr = emu:read8(ctx + 1), emu:read32(ctx + 4), emu:read32(ctx + 8)
  local sig = mode == 2 and string.format("%08x@%08x", native, ptr) or nil
  if sig ~= state.sig then state.sig, state.since = sig, now() return end
  if not sig or now() - state.since < SOFTLOCK_FRAMES then return end
  local what = string.format("softlock: the script at %08x waits on %08x for %d frames (%s)", ptr, native,
                             now() - state.since, L.where())
  L.shot("softlock")
  if L.workarounds and native == (S.WaitForMovementFinish | 1) then
    L.bugs = L.bugs + 1
    log("BUG " .. what .. "; WORKAROUND: released the waitmovement")
    emu:write8(ctx + 1, 1)   -- SCRIPT_MODE_BYTECODE: carry on after the wait
    state.sig = nil
  else
    fail(what)
  end
end

function L.settle(opts)
  opts = opts or {}
  local lock = {}
  local t0, calm, boxes, answered = now(), 0, 0, 0
  local fought = {}
  local at = opts.shots or {}
  local function nextAnswer()
    answered = answered + 1
    return (opts.answers or {})[answered] or "yes"
  end
  while calm < 20 do
    if L.idle() then
      calm = calm + 1
      frame()
    else
      calm = 0
      local hooked
      for name, fn in pairs(opts.hooks or {}) do
        if not hooked and L.on(name) then fn(); hooked = true end
      end
      if hooked then
        -- a caller's handler took this screen
      elseif L.on("CB2_NamingScreen") then
        L.acceptName("naming")
      elseif L.on("CB2_WallClock") then
        -- CONFIRM, then "Is this the correct time?" offers NO first
        wait(30); tap(K.A); wait(40); tap(K.UP); wait(10); tap(K.A)
        waitUntil(function() return not L.on("CB2_WallClock") end, 600, "the water clock to close")
      elseif L.inBattle() then
        fought[#fought + 1] = L.battle()
      elseif L.on("CB2_EvolutionSceneUpdate") then
        tap(K.A); wait(6)
      elseif L.taskRunning("Task_HandleYesNoInput") then
        wait(10)
        local a = nextAnswer()
        L.shot(string.format("prompt_%s", a))
        if a == "no" then tap(K.DOWN) end
        tap(K.A)
        -- the menu task lingers a frame or two: don't answer it twice
        L.waitUntil(function() return not L.taskRunning("Task_HandleYesNoInput") end, 120, "the YES/NO to close")
      elseif L.taskRunning("Task_HandleMultichoiceInput") or L.taskRunning("Task_HandleScrollingMultichoiceInput") then
        wait(10)
        local a = nextAnswer()
        L.shot(string.format("menu_%s", a))
        if a == "down" or a == "no" then tap(K.DOWN) end
        tap(K.A)
        L.waitUntil(function() return not (L.taskRunning("Task_HandleMultichoiceInput")
                                           or L.taskRunning("Task_HandleScrollingMultichoiceInput")) end,
                    120, "the menu to close")
      elseif L.boxUp() or (L.inOverworld() and L.newText()) then
        -- (a reply right after a YES/NO prints with the box mode already cleared,
        -- so a new message in gStringVar4 counts as a box too)
        wait(34)                                 -- fast text: a full box prints in this
        if not L.taskRunning("Task_HandleYesNoInput") then
          boxes = boxes + 1
          L.logText()
          if at[boxes] then L.shot(at[boxes])
          elseif opts.every then L.shot(string.format("text_%02d", boxes)) end
          tap(K.A)
        end
        wait(4)
      else
        tap(K.A)                                 -- a cutscene, a fanfare, a menu
        wait(6)
      end
    end
    softlockCheck(lock)
    if now() - t0 > (opts.limit or 20000) then
      L.shot("stuck")
      fail("stuck: the player never got control back (" .. L.where() .. ")")
    end
  end
  return boxes, fought
end

-- --- Walking by the live map ----------------------------------------------------------------

local learned = {}           -- [mapId] = { ["x,y,key"] = true } steps the game refused
local behaviorCache = {}
local function behaviorOf(mid)
  local layout = emu:read32(S.gMapHeader + S.OFF_MAPHEADER_MAPLAYOUT)
  local cache = behaviorCache[layout]
  if not cache then cache = {}; behaviorCache[layout] = cache end
  local b = cache[mid]
  if b == nil then
    local ts, idx
    if mid < S.NUM_METATILES_IN_PRIMARY then
      ts, idx = emu:read32(layout + S.OFF_LAYOUT_PRIMARY), mid
    else
      ts, idx = emu:read32(layout + S.OFF_LAYOUT_SECONDARY), mid - S.NUM_METATILES_IN_PRIMARY
    end
    b = emu:read16(emu:read32(ts + S.OFF_TILESET_ATTRIBUTES) + 2 * idx) & S.METATILE_ATTR_BEHAVIOR_MASK
    cache[mid] = b
  end
  return b
end
local WATER
local function isWater(b)
  if not WATER then
    WATER = {}
    for _, n in ipairs({ "MB_POND_WATER", "MB_INTERIOR_DEEP_WATER", "MB_DEEP_WATER", "MB_WATERFALL",
                         "MB_SOOTOPOLIS_DEEP_WATER", "MB_OCEAN_WATER", "MB_NO_SURFACING" }) do
      WATER[S[n]] = true
    end
  end
  return WATER[b]
end

local DIRS = { { 0, -1, K.UP, "MB_JUMP_NORTH" }, { 0, 1, K.DOWN, "MB_JUMP_SOUTH" },
               { -1, 0, K.LEFT, "MB_JUMP_WEST" }, { 1, 0, K.RIGHT, "MB_JUMP_EAST" } }
L.DIRS = DIRS

-- The live grid: tile(x, y) -> metatile id, collision, behavior; who stands where;
-- the current map's warps and coord triggers.
local function grid()
  local width = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_WIDTH)
  local height = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_HEIGHT)
  local map = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_MAP)
  local g = { w = width - (2 * S.MAP_OFFSET + 1), h = height - 2 * S.MAP_OFFSET, people = {}, warps = {}, coords = {} }
  local me = emu:read8(S.gPlayerAvatar + S.OFF_AVATAR_OBJECT_EVENT_ID)
  for i = 0, S.OBJECT_EVENTS_COUNT - 1 do
    local o = S.gObjectEvents + i * S.OBJECT_EVENT_SIZE
    if i ~= me and emu:read8(o) & 1 == 1 and emu:read8(o + S.OFF_OBJ_LOCAL_ID) ~= S.OBJ_EVENT_ID_FOLLOWER then
      local c = o + S.OFF_OBJ_CURRENT_COORDS
      g.people[(emu:read16(c) - S.MAP_OFFSET) .. "," .. (emu:read16(c + 2) - S.MAP_OFFSET)] = true
    end
  end
  local events = emu:read32(S.gMapHeader + S.OFF_MAPHEADER_EVENTS)
  local nw, warps = emu:read8(events + S.OFF_EVENTS_WARP_COUNT), emu:read32(events + S.OFF_EVENTS_WARPS)
  for i = 0, nw - 1 do
    local w = warps + i * S.WARP_EVENT_SIZE
    g.warps[emu:read16(w) .. "," .. emu:read16(w + 2)] = true
  end
  local nc, coords = emu:read8(events + S.OFF_EVENTS_COORD_COUNT), emu:read32(events + S.OFF_EVENTS_COORDS)
  for i = 0, nc - 1 do
    local c = coords + i * S.COORD_EVENT_SIZE
    g.coords[emu:read16(c) .. "," .. emu:read16(c + 2)] = true
  end
  function g.tile(x, y)
    if x < 0 or y < 0 or x >= g.w or y >= g.h then return nil end
    local block = emu:read16(map + 2 * ((x + S.MAP_OFFSET) + (y + S.MAP_OFFSET) * width))
    local mid = block & S.MAPGRID_METATILE_ID_MASK
    return mid, block & S.MAPGRID_COLLISION_MASK ~= 0, behaviorOf(mid), block >> 12
  end
  return g
end
L.grid = grid

-- The first key on a shortest path from the player to any goal tile, or nil.
-- goal(x, y) says whether a tile is a goal. Warps and story triggers are only
-- crossed when nothing else gets there (strict = false on the second pass).
-- Elevation follows the game's rule (IsElevationMismatchAt): a step onto a tile
-- whose elevation is neither 0, 15 nor the player's own is refused.
local function firstStep(goal, avoid, strict)
  local g = grid()
  local known = learned[L.mapId()] or {}
  local sx, sy = L.pos()
  local se = emu:read8(L.playerObject() + 0x0B) & 0xF   -- currentElevation
  local function key(x, y, e) return x .. "," .. y .. "," .. e end
  local function enterable(x, y, e)
    local mid, solid, b, te = g.tile(x, y)
    if mid == nil or solid or isWater(b) or g.people[x .. "," .. y] then return nil end
    if avoid and x >= avoid[1] and y >= avoid[2] and x <= avoid[3] and y <= avoid[4] then return nil end
    if strict and not goal(x, y) and (g.warps[x .. "," .. y] or g.coords[x .. "," .. y]) then return nil end
    for _, d in ipairs(DIRS) do if b == S[d[4]] then return nil end end   -- a ledge is only jumped
    if e ~= 0 and te ~= 0 and te ~= 15 and te ~= e then return nil end
    return te
  end
  local seen, queue, head = { [key(sx, sy, se)] = "start" }, { { sx, sy, se } }, 1
  while head <= #queue do
    local x, y, e = queue[head][1], queue[head][2], queue[head][3]
    head = head + 1
    if goal(x, y) and not (x == sx and y == sy) then
      while true do
        local from = seen[key(x, y, e)]
        if from[1] == sx and from[2] == sy and from[4] == se then return from[3] end
        x, y, e = from[1], from[2], from[4]
      end
    end
    local _, _, _, here = g.tile(x, y)
    for _, d in ipairs(DIRS) do
      local nx, ny = x + d[1], y + d[2]
      if not known[x .. "," .. y .. "," .. d[3]] then
        local _, _, b = g.tile(nx, ny)
        if b == S[d[4]] then                     -- a ledge facing this way: jump it
          nx, ny = nx + d[1], ny + d[2]
        end
        local te = enterable(nx, ny, e)
        if te then
          local ne = (te == 15 or here == 15) and e or te
          local k = key(nx, ny, ne)
          if not seen[k] then
            seen[k] = { x, y, d[3], e }
            queue[#queue + 1] = { nx, ny, ne }
          end
        end
      end
    end
  end
  return nil
end

-- Whether the player could walk next to (tx, ty) from where they stand now.
function L.canReachNextTo(tx, ty)
  local goal = function(x, y) return math.abs(x - tx) + math.abs(y - ty) == 1 end
  local x, y = L.pos()
  return goal(x, y) or firstStep(goal, nil, false) ~= nil
end

-- One step. Returns "moved", "blocked" or "taken" (the game took control: a
-- trainer saw the player, a trigger fired, a wild Pokémon jumped out).
function L.step(key)
  local x0, y0 = L.pos()
  emu:addKey(key)
  local t0 = now()
  repeat
    frame()
    local x, y = L.pos()
    if x ~= x0 or y ~= y0 then break end
  until now() - t0 > 40
  emu:clearKey(key)
  local x, y = L.pos()
  if x == x0 and y == y0 then
    if not L.idle() then return "taken" end
    return "blocked"
  end
  -- Trainer sight and triggers run on the frame after a step ends, so the player
  -- only counts as free once it has stayed free for a few frames.
  t0 = now()
  local calm = 0
  while calm < 4 do
    if L.idle() then calm = calm + 1 else calm = 0 end
    if now() - t0 > 60 then return "taken" end
    frame()
  end
  return "moved"
end

-- Walk until goal(x, y) holds for the player's tile. Returns true on arrival, or
-- false when the game took control on the way (the caller decides what that was).
local function walk(goal, what, avoid)
  for _ = 1, 400 do
    local x, y = L.pos()
    if goal(x, y) then return true end
    local k = firstStep(goal, avoid, true) or firstStep(goal, avoid, false)
    if not k then fail(string.format("no path from (%d,%d) to %s on map %d", x, y, what, L.mapId())) end
    local r = L.step(k)
    if r == "taken" then return false end
    if r == "blocked" then
      local m = L.mapId()
      learned[m] = learned[m] or {}
      learned[m][x .. "," .. y .. "," .. k] = true
      local dx, dy = 0, 0
      for _, d in ipairs(DIRS) do if d[3] == k then dx, dy = d[1], d[2] end end
      local mid, _, b = grid().tile(x + dx, y + dy)
      L.note(string.format("blocked step on map %d from (%d,%d) to (%d,%d): metatile 0x%03X, behavior 0x%02X, no collision bit",
                           m, x, y, x + dx, y + dy, mid or 0, b or 0))
    end
  end
  fail("never arrived at " .. what)
end

-- Walk to (tx, ty). Wild battles and trainers who spot the player on the way
-- are played out and the walk carries on. With opts.trigger, the walk instead
-- stops (returning false) when a script takes over, for the caller to play out.
function L.go(tx, ty, opts)
  opts = opts or {}
  local what = string.format("(%d,%d)", tx, ty)
  for _ = 1, 60 do
    if walk(function(x, y) return x == tx and y == ty end, what, opts.avoid) then return true end
    wait(2)
    if opts.trigger and L.scriptRunning() then return false end
    L.settle()
  end
  fail("kept being interrupted on the way to " .. what)
end

-- Walk next to (tx, ty) (or onto one of opts.from's tiles), face it, press A
-- and play the result out with settle(opts).
function L.talk(tx, ty, opts)
  opts = opts or {}
  local goal
  if opts.from then
    goal = function(x, y)
      for _, f in ipairs(opts.from) do if x == f[1] and y == f[2] then return true end end
      return false
    end
  else
    goal = function(x, y) return math.abs(x - tx) + math.abs(y - ty) == 1 end
  end
  for _ = 1, 60 do
    if walk(goal, string.format("next to (%d,%d)", tx, ty), opts.avoid) then break end
    wait(2)
    L.settle()
  end
  local x, y = L.pos()
  local key = (tx > x and K.RIGHT) or (tx < x and K.LEFT) or (ty > y and K.DOWN) or K.UP
  -- a `from` tile may name the way to face: { x, y, "up" } (across a counter, along a hearth)
  for _, f in ipairs(opts.from or {}) do
    if f[1] == x and f[2] == y and f[3] then key = K[string.upper(f[3])] end
  end
  L.face(key)
  if opts.shotBefore then L.shot(opts.shotBefore) end
  tap(K.A); wait(10)
  if opts.noSettle then return end
  return L.settle(opts)
end

-- Walk into a warp (a door, the stairs, an exit mat) or off a map edge, and wait
-- for the next map. With `scene`, a scene starts on arrival: don't wait for control.
function L.enter(key, map, what, scene)
  emu:addKey(key)
  waitUntil(function() return L.mapId() == map end, 600, what)
  emu:clearKey(key)
  if scene then
    waitUntil(L.inOverworld, 600, "the field after " .. what)
    wait(60)
  else
    waitUntil(L.idle, 900, "control after " .. what)
    wait(20)
  end
end

-- --- Test-only scripts in spare EWRAM ---------------------------------------------------------

-- The linker's EWRAM data ends near 0x02037500; this is well past it.
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
-- Run `script` (a byte list) once, as the current map's ON_FRAME script.
function L.runRamScript(script)
  local tableAddr, frameTable, code = SCRATCH, SCRATCH + 0x20, SCRATCH + 0x40
  poke(code, script)
  poke(frameTable, { { S.VAR_TEMP_0, 2 }, { 0, 2 }, { code, 4 }, { 0, 2 } })
  poke(tableAddr, { S.MAP_SCRIPT_ON_FRAME_TABLE, { frameTable, 4 }, 0 })
  emu:write32(S.gMapHeader + S.OFF_MAPHEADER_MAPSCRIPTS, tableAddr)
end

-- Faint the party and white out where the player stands.
function L.whiteOut()
  for slot = 0, S.PARTY_SIZE - 1 do emu:write16(L.partyMon(slot) + S.OFF_MON_HP, 0) end
  L.runRamScript({ S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 },
                   S.SCR_OP_CALLNATIVE, { S.SetCB2WhiteOut | 1, 4 }, S.SCR_OP_WAITSTATE, S.SCR_OP_END })
end

-- --- The battle-strength assist ----------------------------------------------------------------

-- Raise party slot 0 to level 100 by giving it level 100's experience, then let
-- the game recalculate its stats (SetHiddenNature with the nature it already has
-- runs CalculateMonStats). Its met level, moves and species are untouched, so it
-- still obeys (the expansion's obedience goes by met level) and never evolves or
-- learns a move: at level 100 it gains no experience.
function L.assistLevel100()
  local mon = L.partyMon(0)
  local personality, otId = emu:read32(mon), emu:read32(mon + 4)
  local key = personality ~ otId
  local species
  -- substruct 0 (growth) holds species and experience; its slot depends on personality % 24
  local slot0 = emu:read8(S.sSubstructOffsets + 0 * 24 + personality % 24)
  local secure = mon + S.OFF_BOXMON_SECURE
  local base = secure + slot0 * S.SUBSTRUCT_SIZE
  species = (emu:read32(base) ~ key) & 0x7FF
  local growth = emu:read8(S.gSpeciesInfo + species * S.SPECIES_INFO_SIZE + S.OFF_SPECIES_GROWTH_RATE)
  local exp100 = emu:read32(S.gExperienceTables + (growth * (S.MAX_LEVEL + 1) + S.MAX_LEVEL) * 4)
  local w = emu:read32(base + 4) ~ key
  w = (w & ~0x1FFFFF) | (exp100 & 0x1FFFFF)
  emu:write32(base + 4, w ~ key)
  local sum = 0
  for i = 0, S.SECURE_WORDS - 1 do
    local v = emu:read32(secure + 4 * i) ~ key
    sum = sum + (v & 0xFFFF) + (v >> 16)
  end
  emu:write16(mon + S.OFF_BOXMON_CHECKSUM, sum & 0xFFFF)
  -- The hidden nature the mon has now (byte 18: language:3, hiddenNatureModifier:5).
  local nature = (personality % S.NUM_NATURES) ~ (emu:read8(mon + 18) >> 3)
  emu:write16(S.gSpecialVar_0x8004, 0)
  emu:write16(S.gSpecialVar_Result, nature)
  L.runRamScript({ S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 },
                   S.SCR_OP_CALLNATIVE, { S.SetHiddenNature | 1, 4 }, S.SCR_OP_END })
  waitUntil(function() return L.partyLevel(0) == S.MAX_LEVEL end, 120, "the level-100 assist")
  return species, growth, exp100
end

-- --- Running a test ---------------------------------------------------------------------------

function L.start(main)
  local co = coroutine.create(main)
  local realEmu = _G.emu
  callbacks:add("frame", function()
    if not co then return end
    local result = table.pack(coroutine.resume(co))
    while true do
      if not result[1] then
        local err = tostring(result[2])
        console:log(err:find("^" .. TAG .. " FAIL") and err or (TAG .. " FAIL: " .. err))
        console:log(TAG .. " done")
        co = nil
        return
      end
      if coroutine.status(co) == "dead" then
        console:log(TAG .. " done")
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
end

return L
