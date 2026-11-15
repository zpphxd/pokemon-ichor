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
-- A design-level finding (a judgment call, tracked in QA.md): logged, never fails the run.
L.findings = 0
function L.finding(cond, what)
  if cond then log("ok " .. what) return true end
  L.findings = L.findings + 1
  log("FINDING " .. what)
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
-- IchorSave, in SaveBlock3, holds the Ichor bank of flags and vars
-- (GetFlagPointer and GetVarPointer in src/event_data.c send their ids there).
local function ichor() return emu:read32(S.gSaveBlock3Ptr) + S.OFF_SB3_ICHOR end
function L.getVar(v)
  if v >= S.ICHOR_VARS_START and v <= S.ICHOR_VARS_END then
    return emu:read16(ichor() + S.OFF_ICHOR_VARS + (v - S.ICHOR_VARS_START) * 2)
  end
  return emu:read16(L.sb1() + S.OFF_SB1_VARS + (v - S.VARS_START) * 2)
end
function L.getFlag(f)
  local base, o = L.sb1() + S.OFF_SB1_FLAGS, f
  if f >= S.ICHOR_FLAGS_START and f <= S.ICHOR_FLAGS_END then
    base, o = ichor() + S.OFF_ICHOR_FLAGS, f - S.ICHOR_FLAGS_START
  elseif f >= S.ICHOR_DAILY_FLAGS_START and f <= S.ICHOR_DAILY_FLAGS_END then
    base, o = ichor() + S.OFF_ICHOR_DAILY_FLAGS, f - S.ICHOR_DAILY_FLAGS_START
  end
  return (emu:read8(base + (o >> 3)) >> (o & 7)) & 1 == 1
end
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
    -- The console cuts a line near 1 KB, so a long speech (a herald's) goes out
    -- a few pages at a time: each TEXT line ends on a page break (\p).
    local chunk = {}
    local function flush()
      if #chunk > 0 then log(string.format("TEXT %d %d,%d %s", L.mapId(), x, y, table.concat(chunk))) end
      chunk = {}
    end
    local page = {}
    for i, b in ipairs(hex) do
      page[#page + 1] = b
      if b == "FB" or i == #hex then
        if #chunk + #page > 400 then flush() end
        for _, c in ipairs(page) do chunk[#chunk + 1] = c end
        page = {}
      end
    end
    flush()
  end
end

-- --- Battles ---------------------------------------------------------------------------------

function L.isTrainerBattle() return emu:read32(S.gBattleTypeFlags) & S.BATTLE_TYPE_TRAINER ~= 0 end
local function controller(name) return emu:read32(S.gBattlerControllerFuncs) == (S[name] | 1) end

local TRAINERS = { "KLEON_NEBREL", "KLEON_KYNDER", "KLEON_HIPLING", "TITYROS", "THESTYLIS", "PHYLLIS", "KOMATAS",
                   "AGIS", "POLYEIDOS", "PETROS", "AMATHOS", "MENALKAS", "THYRSIS", "LYKIDAS", "LAMPON", "PYRRHA",
                   "AITHRA", "IONE",
                   -- Phase 2
                   "ALETHEA_DECK", "PHORMION", "LYKON",
                   "CREW_BOSS", "PODARGE", "EUCHIDAS", "PHILONIDES", "KERYKOS",
                   "KLEON_2_KYNDER", "KLEON_2_HIPLING", "KLEON_2_NEBREL" }
local function defeatedSet()
  local t = {}
  for _, n in ipairs(TRAINERS) do t[n] = L.defeated(S["TRAINER_" .. n]) end
  return t
end

L.battles = {}
-- Play out a battle that has started (or is starting): trainers are fought with
-- the first move, wild Pokémon are run from (unless running is barred, when they
-- are fought too). Returns a record of it.
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
      -- a wild battle that can't be run from (FLAG_ICHOR_NO_RUNNING, Phase 2's
      -- deck snatchers) is fought like a trainer's, and so is one that won't let
      -- the player go (Arena Trap, Shadow Tag): after three tries, fight
      if trainer or turns > 3 or (S.FLAG_NO_RUNNING and L.getFlag(S.FLAG_NO_RUNNING)) then
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
--   stop    = function() -> bool  return as soon as it holds (a warp landing
--             on a map whose scene the next beat plays)
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
    if opts.stop and opts.stop() then return boxes, fought end
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
        wait(30); L.shot("wall_clock"); tap(K.A); wait(40); L.shot("wall_clock_confirm")
        tap(K.UP); wait(10); tap(K.A)
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
local function isArrow(b)
  return b == S.MB_SOUTH_ARROW_WARP or b == S.MB_NORTH_ARROW_WARP or b == S.MB_EAST_ARROW_WARP
      or b == S.MB_WEST_ARROW_WARP
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
  -- People off screen aren't spawned, so the map's own templates stand in for
  -- them: everyone whose hide flag is clear and who isn't on screen right now.
  local live = {}
  for i = 0, S.OBJECT_EVENTS_COUNT - 1 do
    local o = S.gObjectEvents + i * S.OBJECT_EVENT_SIZE
    if emu:read8(o) & 1 == 1 then live[emu:read8(o + S.OFF_OBJ_LOCAL_ID)] = true end
  end
  for _, t in ipairs(L.mapEvents().objects) do
    if not live[t.localId] and (t.flag == 0 or not L.getFlag(t.flag)) then g.people[t.x .. "," .. t.y] = true end
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
  -- The backup layout also holds MAP_OFFSET cells of each connected map around
  -- the edges: tile(x, y, true) reads them.
  function g.tile(x, y, margin)
    local m = margin and S.MAP_OFFSET or 0
    if x < -m or y < -m or x >= g.w + m or y >= g.h + m then return nil end
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
-- `avoid` is a rectangle { x0, y0, x1, y1 }, a set { ["x,y"] = true } or a
-- function (x, y) -> bool. Returns the key and the path's length.
local function avoided(avoid, x, y)
  if not avoid then return false end
  if type(avoid) == "function" then return avoid(x, y) end
  if avoid[1] then return x >= avoid[1] and y >= avoid[2] and x <= avoid[3] and y <= avoid[4] end
  return avoid[x .. "," .. y] == true
end
L.avoided = avoided
-- Tiles every walk on a map keeps off unless one is the goal: L.keepOff[mapId] =
-- { ["x,y"] = true }. A beat sets it for triggers it means to step on later (a
-- scene's tread, a gate) or that would spoil a walk (a one-way turnstile).
L.keepOff = {}
local function firstStep(goal, avoid, strict, throughPeople)
  local g = grid()
  local hold = L.keepOff[L.mapId()]
  local known = learned[L.mapId()] or {}
  local sx, sy = L.pos()
  local se = emu:read8(L.playerObject() + 0x0B) & 0xF   -- currentElevation
  local function key(x, y, e) return x .. "," .. y .. "," .. e end
  local function enterable(x, y, e)
    local mid, solid, b, te = g.tile(x, y)
    if mid == nil or solid or isWater(b) or (g.people[x .. "," .. y] and not throughPeople) then return nil end
    if avoided(avoid, x, y) then return nil end
    if hold and hold[x .. "," .. y] and not goal(x, y) then return nil end
    -- never cross a warp on the way to something else: a floor warp (the
    -- Euploia's hatch) takes the player off the map on the first step. A door
    -- mat (an arrow warp) only fires while its arrow is held, so walks cross
    -- those (the Hephaisteion's workbench is past its mat).
    if not goal(x, y) and g.warps[x .. "," .. y] and not isArrow(b) then return nil end
    if strict and not goal(x, y) and g.coords[x .. "," .. y] then return nil end
    for _, d in ipairs(DIRS) do if b == S[d[4]] then return nil end end   -- a ledge is only jumped
    if e ~= 0 and te ~= 0 and te ~= 15 and te ~= e then return nil end
    return te
  end
  local seen, queue, head = { [key(sx, sy, se)] = "start" }, { { sx, sy, se } }, 1
  while head <= #queue do
    local x, y, e = queue[head][1], queue[head][2], queue[head][3]
    head = head + 1
    if goal(x, y) and not (x == sx and y == sy) then
      local length = 0
      while true do
        local from = seen[key(x, y, e)]
        length = length + 1
        if from[1] == sx and from[2] == sy and from[4] == se then return from[3], length end
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

-- --- The current map's events, read from the ROM's event tables ----------------------
-- Tests name what they want by the script it runs (S.SCRIPTS, from the ELF) or
-- the flag it sets, and find where it is on the map as built. A moved NPC or
-- item never breaks a test; a missing one fails with its name.

local function s16(v) if v >= 0x8000 then return v - 0x10000 end return v end
local eventsCache = {}
function L.mapEvents()
  local ev = emu:read32(S.gMapHeader + S.OFF_MAPHEADER_EVENTS)
  if eventsCache[ev] then return eventsCache[ev] end
  local out = { objects = {}, warps = {}, coords = {}, bgs = {} }
  local n, base = emu:read8(ev + S.OFF_EVENTS_OBJECT_COUNT), emu:read32(ev + S.OFF_EVENTS_OBJECTS)
  for i = 0, n - 1 do
    local t = base + i * S.OBJECT_TEMPLATE_SIZE
    out.objects[#out.objects + 1] = {
      localId = emu:read8(t + S.OFF_TEMPLATE_LOCAL_ID), x = s16(emu:read16(t + S.OFF_TEMPLATE_X)),
      y = s16(emu:read16(t + S.OFF_TEMPLATE_Y)), range = emu:read16(t + S.OFF_TEMPLATE_RANGE),
      script = emu:read32(t + S.OFF_TEMPLATE_SCRIPT), flag = emu:read16(t + S.OFF_TEMPLATE_FLAG) }
  end
  n, base = emu:read8(ev + S.OFF_EVENTS_WARP_COUNT), emu:read32(ev + S.OFF_EVENTS_WARPS)
  for i = 0, n - 1 do
    local w = base + i * S.WARP_EVENT_SIZE
    out.warps[#out.warps + 1] = { x = s16(emu:read16(w)), y = s16(emu:read16(w + 2)),
      map = emu:read8(w + S.OFF_WARP_MAP_GROUP) * 256 + emu:read8(w + S.OFF_WARP_MAP_NUM) }
  end
  n, base = emu:read8(ev + S.OFF_EVENTS_COORD_COUNT), emu:read32(ev + S.OFF_EVENTS_COORDS)
  for i = 0, n - 1 do
    local c = base + i * S.COORD_EVENT_SIZE
    out.coords[#out.coords + 1] = { x = s16(emu:read16(c)), y = s16(emu:read16(c + 2)),
                                    script = emu:read32(c + S.OFF_COORD_SCRIPT) }
  end
  n, base = emu:read8(ev + S.OFF_EVENTS_BG_COUNT), emu:read32(ev + S.OFF_EVENTS_BGS)
  for i = 0, n - 1 do
    local b = base + i * S.BG_EVENT_SIZE
    out.bgs[#out.bgs + 1] = { x = emu:read16(b), y = emu:read16(b + 2), kind = emu:read8(b + S.OFF_BG_KIND),
                              union = emu:read32(b + S.OFF_BG_UNION) }
  end
  eventsCache[ev] = out
  return out
end

local function scriptAddr(name)
  local a = S.SCRIPTS[name]
  if not a then fail("the ROM has no script named " .. name) end
  return a
end

-- A person or object, by the script it runs (the nth one, for a flock): where it
-- stands now (or its template's place, if it isn't on the map), its local id and
-- its sight range.
function L.npc(script, nth)
  local addr, found = scriptAddr(script), 0
  for _, o in ipairs(L.mapEvents().objects) do
    if o.script == addr then
      found = found + 1
      if found == (nth or 1) then
        local x, y = L.objectAt(o.localId)
        return { x = x or o.x, y = y or o.y, localId = o.localId, range = o.range, present = x ~= nil,
                 tiles = { { x = x or o.x, y = y or o.y } }, what = script }
      end
    end
  end
  fail(string.format("map %d has no one running %s (the map changed?)", L.mapId(), script))
end
-- An item ball, by the flag that hides it once taken.
function L.ball(flag)
  for _, o in ipairs(L.mapEvents().objects) do
    if o.flag == flag and o.script == scriptAddr("Common_EventScript_FindItem") then
      return { x = o.x, y = o.y, localId = o.localId, tiles = { { x = o.x, y = o.y } }, what = "item ball" }
    end
  end
  fail(string.format("map %d has no item ball with flag %d", L.mapId(), flag))
end
-- A sign or other background event, by script: every tile it covers, each with
-- the way the player must face it (BG_EVENT_PLAYER_FACING_*: 1 north, 2 south,
-- 3 east, 4 west, else any).
function L.sign(script)
  local addr, tiles = scriptAddr(script), {}
  for _, b in ipairs(L.mapEvents().bgs) do
    if b.kind ~= S.BG_EVENT_HIDDEN_ITEM and b.union == addr then
      tiles[#tiles + 1] = { x = b.x, y = b.y, facing = ({ "up", "down", "right", "left" })[b.kind] }
    end
  end
  if #tiles == 0 then fail(string.format("map %d has no sign running %s", L.mapId(), script)) end
  return { tiles = tiles, x = tiles[1].x, y = tiles[1].y, what = script }
end
-- A hidden item's flag from its packed id (asm/macros/map.inc): a vanilla
-- flag's offset from FLAG_HIDDEN_ITEMS_START, or 0x1000 on for Ichor's banks.
function L.hiddenItemFlag(id)
  if id >= 0x1000 then return 0x2000 + (id - 0x1000) end
  return id + S.FLAG_HIDDEN_ITEMS_START
end

-- A hidden item, by its flag.
function L.hidden(flag)
  for _, b in ipairs(L.mapEvents().bgs) do
    if b.kind == S.BG_EVENT_HIDDEN_ITEM and L.hiddenItemFlag((b.union >> 11) & 0x1FFF) == flag then
      return { tiles = { { x = b.x, y = b.y } }, x = b.x, y = b.y, what = "hidden item" }
    end
  end
  fail(string.format("map %d has no hidden item with flag %d", L.mapId(), flag))
end
-- The tiles of the story triggers that run any of these scripts, as a set.
function L.triggers(...)
  local want, set, n = {}, {}, 0
  for _, name in ipairs({ ... }) do want[scriptAddr(name)] = true end
  for _, c in ipairs(L.mapEvents().coords) do
    if want[c.script] then set[c.x .. "," .. c.y] = true; n = n + 1 end
  end
  if n == 0 then fail(string.format("map %d has no trigger running %s", L.mapId(), table.concat({ ... }, ", "))) end
  return set
end
function L.onTile(set) local x, y = L.pos() return set[x .. "," .. y] == true end
-- The tiles a trainer watches: from where they stand, the way they face, out to
-- their sight range.
function L.sight(script)
  local t = L.npc(script)
  local set = {}
  if not t.present then return set end
  local facing
  for i = 0, S.OBJECT_EVENTS_COUNT - 1 do
    local o = S.gObjectEvents + i * S.OBJECT_EVENT_SIZE
    if emu:read8(o) & 1 == 1 and emu:read8(o + S.OFF_OBJ_LOCAL_ID) == t.localId then facing = emu:read8(o + 0x18) & 0xF end
  end
  local d = ({ { 0, 1 }, { 0, -1 }, { -1, 0 }, { 1, 0 } })[facing or 1]
  for k = 1, t.range do set[(t.x + d[1] * k) .. "," .. (t.y + d[2] * k)] = true end
  return set
end

-- Where to stand to talk to a target, and which way to face: next to any of its
-- tiles (or on the side a sign insists on), or across a counter.
local FACE_KEY = { up = K.UP, down = K.DOWN, left = K.LEFT, right = K.RIGHT }
local function standSpots(target)
  local spots, g = {}, grid()
  local function add(x, y, face) spots[x .. "," .. y] = face end
  for _, t in ipairs(target.tiles) do
    for _, d in ipairs({ { 0, 1, "up" }, { 0, -1, "down" }, { 1, 0, "left" }, { -1, 0, "right" } }) do
      -- (d is where the player stands relative to the tile; d[3] the way they face)
      if not t.facing or t.facing == d[3] then
        add(t.x + d[1], t.y + d[2], d[3])
        local _, _, b = g.tile(t.x + d[1], t.y + d[2])
        if b == S.MB_COUNTER then add(t.x + 2 * d[1], t.y + 2 * d[2], d[3]) end
      end
    end
  end
  for _, t in ipairs(target.tiles) do spots[t.x .. "," .. t.y] = nil end
  return spots
end
L.standSpots = standSpots

-- How many steps the player is from talking to a target, or nil if they can't
-- get there.
function L.distanceTo(target, avoid)
  local spots = standSpots(target)
  local x, y = L.pos()
  if spots[x .. "," .. y] then return 0 end
  local _, d = firstStep(function(a, b) return spots[a .. "," .. b] ~= nil end, avoid, false)
  return d
end

-- Whether the player could walk next to (tx, ty) from where they stand now.
function L.canReachNextTo(tx, ty)
  return L.distanceTo({ tiles = { { x = tx, y = ty } } }) ~= nil
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
  local waits = 0
  for _ = 1, 400 do
    local x, y = L.pos()
    if goal(x, y) then return true end
    local k = firstStep(goal, avoid, true) or firstStep(goal, avoid, false)
    -- someone wandering (Emporion's runner, in his lane) may stand in the only
    -- way for a moment: wait for them to move on
    while not k and waits < 20 and firstStep(goal, avoid, false, true) do
      waits = waits + 1
      wait(30)
      k = firstStep(goal, avoid, true) or firstStep(goal, avoid, false)
    end
    if not k then fail(string.format("no path from (%d,%d) to %s on map %d", x, y, what, L.mapId())) end
    local r = L.step(k)
    if r == "taken" then return false end
    local dx, dy = 0, 0
    for _, d in ipairs(DIRS) do if d[3] == k then dx, dy = d[1], d[2] end end
    -- (a wanderer who stepped into the way is no reason to remember the step)
    if r == "blocked" and not L.objectOn(x + dx, y + dy) then
      local m = L.mapId()
      learned[m] = learned[m] or {}
      learned[m][x .. "," .. y .. "," .. k] = true
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
-- `target` is what L.npc, L.ball, L.sign or L.hidden return (or x, y).
function L.talk(target, ty, opts)
  if type(target) == "number" then target = { tiles = { { x = target, y = ty } }, what = target .. "," .. ty }
  else opts = ty end
  opts = opts or {}
  local what = target.what or "a target"
  for _ = 1, 60 do
    local spots = standSpots(target)
    if walk(function(x, y) return spots[x .. "," .. y] ~= nil end, "a place to talk to " .. what, opts.avoid) then
      break
    end
    wait(2)
    L.settle()
  end
  local x, y = L.pos()
  local face = standSpots(target)[x .. "," .. y]
  if not face then fail("lost the place to talk to " .. what) end
  L.face(FACE_KEY[face])
  if opts.shotBefore then L.shot(opts.shotBefore) end
  tap(K.A); wait(10)
  if opts.noSettle then return end
  return L.settle(opts)
end

-- Walk onto one of a set of story-trigger tiles (L.triggers). Returns false when
-- a script takes over (the trigger fired), true if the player stood on it and
-- nothing happened.
function L.goTrigger(set, opts)
  opts = opts or {}
  for _ = 1, 60 do
    if walk(function(x, y) return set[x .. "," .. y] == true end, "a trigger", opts.avoid) then
      wait(4)
      local t0 = now()
      while now() - t0 < 30 do
        if not L.idle() then return false end
        frame()
      end
      return true
    end
    wait(2)
    if L.scriptRunning() then return false end
    L.settle()
  end
  fail("kept being interrupted on the way to a trigger")
end

-- Take the warp that leads to `map`: a door from the tile below it, or an exit
-- mat by standing on it and pressing its arrow. With `scene`, a scene starts on
-- arrival: don't wait for control.
function L.useWarp(map, scene)
  local g = grid()
  local spots = {}
  for _, w in ipairs(L.mapEvents().warps) do
    if w.map == map then
      local _, _, b = g.tile(w.x, w.y)
      if b == S.MB_SOUTH_ARROW_WARP then spots[w.x .. "," .. w.y] = K.DOWN
      elseif b == S.MB_NORTH_ARROW_WARP then spots[w.x .. "," .. w.y] = K.UP
      elseif b == S.MB_EAST_ARROW_WARP then spots[w.x .. "," .. w.y] = K.RIGHT
      elseif b == S.MB_WEST_ARROW_WARP then spots[w.x .. "," .. w.y] = K.LEFT
      else spots[w.x .. "," .. (w.y + 1)] = K.UP end                       -- a door or a stair
    end
  end
  if next(spots) == nil then fail(string.format("map %d has no warp to map %d", L.mapId(), map)) end
  for _ = 1, 60 do
    if walk(function(x, y) return spots[x .. "," .. y] ~= nil end, "the warp to map " .. map) then break end
    wait(2)
    L.settle()
  end
  local x, y = L.pos()
  L.enter(spots[x .. "," .. y], map, "the warp to map " .. map, scene)
end

-- Walk off the map's edge ("up", "down", "left", "right") into the connected
-- map: to an open edge tile whose neighbour across the seam is open too.
function L.leaveEdge(dir, map, scene)
  local d = ({ up = { 0, -1, K.UP }, down = { 0, 1, K.DOWN }, left = { -1, 0, K.LEFT }, right = { 1, 0, K.RIGHT } })[dir]
  local g = grid()
  local edge = {}
  local function try(x, y)
    local mid, solid, b = g.tile(x + d[1], y + d[2], true)
    if mid ~= nil and not solid and not isWater(b) then edge[x .. "," .. y] = true end
  end
  if dir == "up" or dir == "down" then
    for x = 0, g.w - 1 do try(x, dir == "up" and 0 or g.h - 1) end
  else
    for y = 0, g.h - 1 do try(dir == "left" and 0 or g.w - 1, y) end
  end
  for _ = 1, 60 do
    if walk(function(x, y) return edge[x .. "," .. y] == true end, "the " .. dir .. " edge") then break end
    wait(2)
    L.settle()
  end
  L.enter(d[3], map, "the " .. dir .. " edge to map " .. map, scene)
end

-- Of a list of targets ({ target = function() return L.npc(...) end, ... }), the
-- index of the nearest one the player can walk to, or nil.
function L.nearest(list, avoid)
  local best, bestD
  for i, item in ipairs(list) do
    local d = L.distanceTo(item.target(), avoid)
    if d and (not bestD or d < bestD) then best, bestD = i, d end
  end
  return best, bestD
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
