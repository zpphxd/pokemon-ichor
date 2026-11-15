-- Emporion's interiors check, run by tools/ichor/tests/emporion_rooms.sh (read it first).
--
-- Plays each of the nine rooms' events as a player would, with key presses, and
-- checks the game's state after each: the Asclepeion's healer, beat 12 in the
-- Deigma and Thaletas's trade, beat 13 at the Hephaisteion's forge, knucklebones
-- at the Dolphin, Philoxenos's table and a laurel story, Penelopeia's gift, the
-- runners' Quick Claw and letter home, Euphronios's three paintings, and the crew
-- boss's battle and the empty hiring hall after Act I.
--
-- Setup touches no ROM data. After Quickstart it writes small event scripts into
-- spare EWRAM and points the current map header's script table at them as an
-- ON_FRAME script (aegina_homes.lua's trick): give the party, items and flags,
-- then warp into each room through its door (warp 0).
--
-- Prints "EMPORION ok ..." per check, "EMPORION shot ..." per screenshot, and
-- ends with "EMPORION done"; any failure prints "EMPORION FAIL: ..." first.

local S = dofile("build/emporion_rooms/symbols.lua")
local OUT = "build/emporion_rooms/"
local K = { A = C.GBA_KEY.A, B = C.GBA_KEY.B, START = C.GBA_KEY.START, SELECT = C.GBA_KEY.SELECT,
            UP = C.GBA_KEY.UP, DOWN = C.GBA_KEY.DOWN, LEFT = C.GBA_KEY.LEFT, RIGHT = C.GBA_KEY.RIGHT }
local SCRATCH = 0x0203F000  -- spare EWRAM: the linker's EWRAM data ends near 0x02037800

-- The test reads as straight-line code in a coroutine; mGBA calls go through the
-- frame callback (yield "call"), as in aegina_homes.lua.
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
local function getFlag(f)
  if f >= S.ICHOR_FLAGS_START and f <= S.ICHOR_FLAGS_END then
    local o = f - S.ICHOR_FLAGS_START
    local base = emu:read32(S.gSaveBlock3Ptr) + S.OFF_SB3_ICHOR + S.OFF_ICHOR_FLAGS
    return (emu:read8(base + (o >> 3)) >> (o & 7)) & 1 == 1
  end
  return (emu:read8(sb1() + S.OFF_SB1_FLAGS + (f >> 3)) >> (f & 7)) & 1 == 1
end
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
    local task = S.gTasks + i * S.TASK_SIZE
    if emu:read8(task + S.OFF_TASK_ACTIVE) ~= 0
       and emu:read32(task + S.OFF_TASK_FUNC) == (S[name] | 1) then return true end
  end
  return false
end
local function itemCount(item)
  local bag = sb1() + S.OFF_SB1_BAG
  local encryptionKey = emu:read32(sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
  local n = 0
  for i = 0, S.BAG_SLOTS - 1 do
    local slot = bag + i * S.ITEM_SLOT_SIZE
    if emu:read16(slot) == item then
      n = n + (emu:read16(slot + S.OFF_ITEM_SLOT_QUANTITY) ~ encryptionKey)
    end
  end
  return n
end
local function partyMon(slot) return S.gParties + slot * S.POKEMON_SIZE end
local function partyHp(slot)
  local m = partyMon(slot)
  return emu:read16(m + S.OFF_MON_HP), emu:read16(m + S.OFF_MON_MAXHP)
end
local function hurt(slot) emu:write16(partyMon(slot) + S.OFF_MON_HP, 1) end
local function nickname(slot)
  local s = ""
  for i = 0, 9 do
    local b = emu:read8(partyMon(slot) + S.OFF_MON_NICKNAME + i)
    if b == 0xFF then break end
    if b >= 0xBB and b <= 0xD4 then s = s .. string.char(65 + b - 0xBB) else s = s .. "?" end
  end
  return s
end
local function objectPresent(localId)
  for i = 0, S.NUM_OBJECT_EVENTS - 1 do
    local o = S.gObjectEvents + i * S.OBJECT_EVENT_SIZE
    if emu:read8(o) & 1 == 1 and emu:read8(o + S.OFF_OBJ_LOCAL_ID) == localId then return true end
  end
  return false
end
-- The metatile id drawn at a map cell (the live map, after any setmetatile).
local function metatileAt(x, y)
  local w = emu:read32(S.gBackupMapLayout + S.OFF_MAPGRID_WIDTH)
  local map = emu:read32(S.gBackupMapLayout + S.OFF_MAPGRID_MAP)
  return emu:read16(map + ((y + S.MAP_OFFSET) * w + (x + S.MAP_OFFSET)) * 2) & 0x3FF
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

-- Press through a script, screenshotting every message box as prefix_NN.png, A on
-- every box and through fades, fanfares and battles, until stop() holds (default:
-- the player is free again for 20 frames). A on a YES/NO prompt answers YES.
local function playThrough(prefix, stop, limit, shots, opts)
  opts = opts or {}
  local t0, calm, boxes = now(), 0, 0
  while true do
    if stop and stop() then return boxes end
    if not stop and idle() then
      calm = calm + 1
      if calm >= 20 then return boxes end
      frame()
    else
      calm = 0
      if opts.menuChoice and taskRunning("Task_HandleScrollingMultichoiceInput") then
        wait(20)
        opts.menus = (opts.menus or 0) + 1
        if opts.menus == 1 then shot(prefix .. "_bones_menu.png") end
        for _ = 1, opts.menuChoice do tap(K.DOWN) end
        tap(K.A)
        waitUntil(function() return not taskRunning("Task_HandleScrollingMultichoiceInput") end,
                  120, "the bones menu to close")
      elseif opts.decline and taskRunning("Task_HandleYesNoInput") then
        wait(10); tap(K.B)
        waitUntil(function() return not taskRunning("Task_HandleYesNoInput") end,
                  120, "the declined match prompt to close")
      elseif boxUp() then
        wait(34)
        if stop and stop() then return boxes end
        if boxUp() and not (opts.menuChoice and taskRunning("Task_HandleScrollingMultichoiceInput"))
                   and not (opts.decline and taskRunning("Task_HandleYesNoInput")) then
          boxes = boxes + 1
          if shots ~= false and boxes <= 40 then shot(string.format("%s_%02d.png", prefix, boxes)) end
          tap(K.A)
        end
        wait(4)
      else
        if not idle() then tap(K.A) end
        wait(6)
      end
    end
    if now() - t0 > (limit or 20000) then shot(prefix .. "_stuck.png"); fail("stuck in " .. prefix) end
  end
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
-- Walk along each leg in turn: vertical first, then horizontal, to each point.
local function walkTo(points)
  for _, p in ipairs(points) do
    while true do
      local x, y = pos()
      if x == p[1] and y == p[2] then break end
      local key
      if y < p[2] then key = K.DOWN elseif y > p[2] then key = K.UP
      elseif x < p[1] then key = K.RIGHT else key = K.LEFT end
      step(key)
    end
  end
end
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
local function talk(key, prefix, stop, opts)
  face(key)
  tap(K.A); wait(10)
  return playThrough(prefix, stop, nil, nil, opts)
end

-- --- Setup scripts in EWRAM ---------------------------------------------------------------

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
-- Each script runs when VAR_TEMP_0 holds `ticket` and moves it on, so several can
-- run on one map; a warp clears the temp vars, and the ticket starts again at 0.
local ticket = 0
local function runRamScript(script)
  local tableAddr, frameTable, code = SCRATCH, SCRATCH + 0x20, SCRATCH + 0x40
  local flat = { S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { ticket + 1, 2 } }
  for _, b in ipairs(script) do flat[#flat + 1] = b end
  flat[#flat + 1] = S.SCR_OP_END
  poke(code, flat)
  poke(frameTable, { { S.VAR_TEMP_0, 2 }, { ticket, 2 }, { code, 4 }, { 0, 2 } })
  poke(tableAddr, { S.MAP_SCRIPT_ON_FRAME_TABLE, { frameTable, 4 }, 0 })
  emu:write32(S.gMapHeader + S.OFF_MAPHEADER_MAPSCRIPTS, tableAddr)
  ticket = ticket + 1
end
local function add(script, t) for _, b in ipairs(t) do script[#script + 1] = b end end
local function giveMon(script, species, level)
  add(script, { S.SCR_OP_CALLNATIVE, { S.ScrCmd_createmon | 1, 4 }, 0, S.PARTY_SIZE,
                { species, 2 }, { level, 2 }, { 0, 4 } })
end
local function setFlag(script, f) add(script, { S.SCR_OP_SETFLAG, { f, 2 } }) end
local function clearFlag(script, f) add(script, { S.SCR_OP_CLEARFLAG, { f, 2 } }) end
local function addItem(script, item, n) add(script, { S.SCR_OP_ADDITEM, { item, 2 }, { n, 2 } }) end
-- Run a setup script on the current map, without warping.
local function setup(script)
  runRamScript(script)
  wait(30)
end
-- warp map, 0 (the door), then wait for the room; `scene` if a scene plays on entry.
local function warpInto(script, map, scene)
  add(script, { S.SCR_OP_WARP, map >> 8, map & 0xFF, 0, { 0xFFFF, 2 }, { 0xFFFF, 2 }, S.SCR_OP_WAITSTATE })
  runRamScript(script)
  ticket = 0
  if scene then
    waitUntil(function() return mapId() == map and inOverworld() end, 4000, "the warp")
    wait(20)
  else
    waitUntil(function() return mapId() == map and idle() end, 4000, "the warp")
    wait(30)
  end
end

-- --- The rooms ---------------------------------------------------------------------------

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
  -- The party: a Swampert to win the crew boss's battle, then the Onotis to trade
  -- and the three Pokémon Euphronios paints.
  local s = {}
  setFlag(s, S.FLAG_SYS_POKEMON_GET)
  setFlag(s, S.FLAG_ARRIVED_EMPORION)
  giveMon(s, S.SPECIES_SWAMPERT, 100)
  giveMon(s, S.SPECIES_ONOTIS, 15)
  giveMon(s, S.SPECIES_HARPECK, 15)
  giveMon(s, S.SPECIES_CHELONET, 15)
  giveMon(s, S.SPECIES_STACHYSS, 15)
  setup(s)
end

local function asclepeion()
  warpInto({}, S.MAP_ASCLEPEION)
  local x, y = pos()
  expect(x == 8 and y == 8, "arrived on the Asclepeion's threshold")
  shot("asclepeion_01_room.png")
  walkTo({ { 8, 4 } })
  hurt(0)
  talk(K.UP, "asclepeion_02_healer")
  local hp, maxHp = partyHp(0)
  expect(hp == maxHp, string.format("the healer heals across the counter (%d/%d)", hp, maxHp))
  walkTo({ { 6, 4 } })
  talk(K.UP, "asclepeion_03_panacoil")
  -- The Pithos: its two lines, its menu (shown, then closed with B), the lid.
  walkTo({ { 1, 4 }, { 1, 3 } })
  face(K.UP)
  tap(K.A); wait(10)
  waitUntil(boxUp, 300, "the Pithos's text")
  wait(34); shot("asclepeion_04_pithos.png")
  -- B advances the text and cancels the menu without choosing anything.
  local n = 0
  repeat
    tap(K.B); wait(40); n = n + 1
    if n == 2 then shot("asclepeion_05_pithos_menu.png") end
  until idle() or n > 12
  expect(idle() and not on("CB2_PokeStorage"), "the Pithos's menu opens and closes")
end

local function deigma()
  warpInto({}, S.MAP_DEIGMA, true)
  expect(objectPresent(S.LOCALID_ALETHEA), "Alethea waits in the Deigma after beat 11")
  shot("deigma_01_arrive.png")
  playThrough("deigma_02_forty_lamps")
  expect(getFlag(S.FLAG_DEIGMA_CLUE), "beat 12 sets FLAG_ICHOR_DEIGMA_CLUE")
  expect(not objectPresent(S.LOCALID_ALETHEA), "Alethea has left the Deigma")
  local x, y = pos()
  expect(x == 2 and y == 8, string.format("the player followed her to the notice board (%d,%d)", x, y))
  shot("deigma_03_after.png")
  -- Re-entry: the beat doesn't play again.
  warpInto({}, S.MAP_DEIGMA)
  expect(not objectPresent(S.LOCALID_ALETHEA), "beat 12 plays once")
  -- Thaletas's trade: the Onotis (party slot 1) for Socrates.
  walkTo({ { 2, 5 }, { 13, 5 } })
  expect(objectPresent(S.LOCALID_NARKERAY) and not objectPresent(S.LOCALID_ONOTIS),
         "the Narkeray swims by the quay before the trade")
  shot("deigma_04_thaletas.png")
  face(K.RIGHT)
  tap(K.A); wait(10)
  playThrough("deigma_05_thaletas", function() return on("CB2_PokeStorage") end)
  wait(90); shot("deigma_06_choose_mon.png")
  tap(K.UP); wait(20); tap(K.UP); wait(20)
  tap(K.A); wait(60)
  tap(K.DOWN); wait(20)                       -- the Onotis is the second Pokémon
  tap(K.A); wait(40); shot("deigma_07_select.png")
  tap(K.A); wait(40)
  waitUntil(function() return not on("CB2_PokeStorage") end, 1200, "the storage screen to close")
  waitUntil(function() return not inOverworld() end, 600, "the trade scene")
  local t0 = now()
  while not inOverworld() do
    tap(K.A); wait(9)
    if now() - t0 > 12000 then fail("the trade scene never ended") end
  end
  playThrough("deigma_08_after_trade")
  expect(getFlag(S.FLAG_TRADED_NARKERAY), "the trade sets FLAG_ICHOR_TRADED_NARKERAY")
  expect(nickname(1) == "SOCRATES", "the Onotis's slot now holds SOCRATES (" .. nickname(1) .. ")")
  expect(not objectPresent(S.LOCALID_NARKERAY) and objectPresent(S.LOCALID_ONOTIS),
         "the Onotis stands by Thaletas after the trade")
  shot("deigma_09_onotis.png")
end

local function hephaisteion()
  local s = {}
  addItem(s, S.ITEM_CHARCOAL, 1)
  warpInto(s, S.MAP_HEPHAISTEION)
  shot("hephaisteion_01_cold.png")
  local cold = metatileAt(4, 2)
  walkTo({ { 4, 5 } })
  talk(K.UP, "hephaisteion_02_kedalion")
  expect(getFlag(S.FLAG_FORGE_RELIT), "the forge is relit (FLAG_ICHOR_FORGE_RELIT)")
  expect(getFlag(S.FLAG_GOT_BRONZE_HAMMER), "Kedalion gives the Bronze Hammer (FLAG_ICHOR_GOT_BRONZE_HAMMER)")
  local lit = metatileAt(4, 2)
  expect(lit ~= cold, string.format("the forge's metatile swaps to lit (%03X -> %03X)", cold, lit))
  shot("hephaisteion_03_lit.png")
  warpInto({}, S.MAP_HEPHAISTEION)
  expect(metatileAt(4, 2) == lit, "the forge stays lit on re-entry")
  walkTo({ { 4, 5 } })
  talk(K.UP, "hephaisteion_04_after")
  shot("hephaisteion_05_room_lit.png")
end

local function tavern()
  warpInto({}, S.MAP_TAVERN)
  shot("tavern_01_room.png")
  walkTo({ { 6, 6 }, { 2, 6 } })
  local juice = itemCount(S.ITEM_BERRY_JUICE)
  local function opponent(key, name, flag, item, quantity)
    local before = item and itemCount(item)
    expect(not getFlag(flag), name .. "'s first-win flag starts clear")
    talk(key, name .. "_decline", nil, { decline = true })
    expect(not getFlag(flag) and (not item or itemCount(item) == before),
           "declining " .. name .. "'s match grants no prize")
    if item == S.ITEM_TM_FLING then
      local bag, saved = sb1() + S.OFF_SB1_BAG + S.OFF_BAG_TMS, {}
      local encryptionKey = emu:read32(sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
      for i = 0, S.BAG_TMHM_COUNT * S.ITEM_SLOT_SIZE - 1 do saved[i] = emu:read8(bag + i) end
      for i = 0, S.BAG_TMHM_COUNT - 1 do
        local slot = bag + i * S.ITEM_SLOT_SIZE
        emu:write16(slot, S.ITEM_TM17)
        emu:write16(slot + S.OFF_ITEM_SLOT_QUANTITY, S.MAX_BAG_ITEM_CAPACITY ~ encryptionKey)
      end
      local attempts = 0
      while not getFlag(S.FLAG_MYRTALE_PRIZE_PENDING) do
        attempts = attempts + 1
        if attempts > 25 then fail("never won Myrtale's full-Bag match in 25 games") end
        local opts = { menuChoice = 4 }
        talk(key, "Myrtale_full_bag_" .. attempts, nil, opts)
        expect((opts.menus or 0) >= 3, "Myrtale's full-Bag test plays real best-of-five matches")
      end
      expect(not getFlag(flag) and itemCount(item) == 0,
             "Myrtale saves the owed scroll but does not award a missing prize")
      for i = 0, S.BAG_TMHM_COUNT * S.ITEM_SLOT_SIZE - 1 do emu:write8(bag + i, saved[i]) end
      expect(itemCount(item) == before, "the TM pocket is restored before collecting the owed prize")
    end
    if item == S.ITEM_OLIVE_OIL then
      local bag, saved = sb1() + S.OFF_SB1_BAG, {}
      local encryptionKey = emu:read32(sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
      for i = 0, S.BAG_ITEMS_COUNT * S.ITEM_SLOT_SIZE - 1 do saved[i] = emu:read8(bag + i) end
      -- Leave exactly one space for a two-Oil prize: it must not be partly paid.
      for i = 0, S.BAG_ITEMS_COUNT - 1 do
        local slot = bag + i * S.ITEM_SLOT_SIZE
        emu:write16(slot, item)
        emu:write16(slot + S.OFF_ITEM_SLOT_QUANTITY, (S.MAX_BAG_ITEM_CAPACITY - (i == 0 and 1 or 0)) ~ encryptionKey)
      end
      local fullCount = itemCount(item)
      local function fullBagMessage()
        local text = S.EmporionCity_Tavern_EventScript_Strepsiades_Text_2
        for i = 0, 1023 do
          local b = emu:read8(text + i)
          if emu:read8(S.gStringVar4 + i) ~= b then return false end
          if b == 0xFF then return true end
        end
        return false
      end
      local attempts = 0
      repeat
        attempts = attempts + 1
        if attempts > 25 then fail("never reached Strepsiades's full-Bag prize in 25 games") end
        talk(key, "Strepsiades_full_bag_" .. attempts, nil, { menuChoice = 4 })
      until fullBagMessage()
      expect(not getFlag(flag) and itemCount(item) == fullCount,
             "a won match with one Oil space grants no partial prize or reward flag")
      for i = 0, S.BAG_ITEMS_COUNT * S.ITEM_SLOT_SIZE - 1 do emu:write8(bag + i, saved[i]) end
      expect(itemCount(item) == before, "the player's Bag is restored before retrying the prize")
    end
    local tries = 0
    while not getFlag(flag) do
      tries = tries + 1
      if tries > 25 then fail("never beat " .. name .. " in 25 games") end
      local opts = { menuChoice = 4 }
      local owed = getFlag(S.FLAG_MYRTALE_PRIZE_PENDING) and item == S.ITEM_TM_FLING
      talk(key, string.format("%s_%02d", name, tries), nil, opts)
      expect((opts.menus or 0) >= 3 or (owed and (opts.menus or 0) == 0),
             name .. (owed and " gives the owed prize without another match" or " plays a real best-of-five match"))
    end
    expect(true, string.format("beat %s in %d game(s)", name, tries))
    if item then
      expect(itemCount(item) == before + quantity, name .. " grants the actual prize")
      talk(key, name .. "_repeat", nil, { menuChoice = 4 })
      expect(itemCount(item) == before + quantity, name .. " grants no duplicate prize")
    end
  end
  opponent(K.LEFT, "Myrtale", S.FLAG_KNUCKLEBONES_EMPORION, S.ITEM_TM_FLING, 1)
  expect(not getFlag(S.FLAG_MYRTALE_PRIZE_PENDING), "collecting Myrtale's scroll clears the owed-prize flag")
  -- The previous build recorded a win without giving a TM. Restore that save state.
  local bag = sb1() + S.OFF_SB1_BAG + S.OFF_BAG_TMS
  local key = emu:read32(sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
  for i = 0, S.BAG_TMHM_COUNT - 1 do
    local slot = bag + i * S.ITEM_SLOT_SIZE
    if emu:read16(slot) == S.ITEM_TM_FLING then
      emu:write16(slot, 0)
      emu:write16(slot + S.OFF_ITEM_SLOT_QUANTITY, key)
    end
  end
  local legacyOpts = { menuChoice = 4 }
  talk(K.LEFT, "Myrtale_legacy_prize", nil, legacyOpts)
  expect(itemCount(S.ITEM_TM_FLING) == 1 and (legacyOpts.menus or 0) == 0,
         "a legacy champion win recovers the real scroll without another match")
  opponent(K.UP, "Strepsiades", S.FLAG_KNUCKLEBONES_STREPSIADES, S.ITEM_OLIVE_OIL, 2)
  walkTo({ { 6, 6 }, { 10, 6 }, { 10, 4 } })
  opponent(K.UP, "Stratyllis", S.FLAG_KNUCKLEBONES_STRATYLLIS, S.ITEM_WINE, 1)
  expect(itemCount(S.ITEM_BERRY_JUICE) == juice, "the tavern grants no substitute Berry Juice")
end

local function philoxenos()
  local s = {}
  setFlag(s, S.FLAG_BADGE02_GET)
  warpInto(s, S.MAP_PHILOXENOS)
  shot("philoxenos_01_room.png")
  walkTo({ { 6, 8 } })
  hurt(0)
  talk(K.LEFT, "philoxenos_02_xenia")
  local hp, maxHp = partyHp(0)
  expect(hp == maxHp, string.format("Philoxenos's table heals the party (%d/%d)", hp, maxHp))
  expect(getFlag(S.FLAG_PHILOXENOS_LAUREL_2), "the Herald Laurel's story is paid for (FLAG_ICHOR_PHILOXENOS_LAUREL_2)")
  talk(K.LEFT, "philoxenos_03_again")
end

local function widow()
  warpInto({}, S.MAP_WIDOW)
  shot("widow_01_room.png")
  -- Penelopeia stands at (3,3), beside her loom, so (1,3) stays free for reading it
  walkTo({ { 3, 4 } })
  talk(K.UP, "widow_02_penelopeia")
  expect(getFlag(S.FLAG_GOT_WIDOWS_GIFT), "Penelopeia gives the Sea Incense (FLAG_ICHOR_GOT_WIDOWS_GIFT)")
  talk(K.UP, "widow_03_after")
  walkTo({ { 2, 4 }, { 2, 3 }, { 1, 3 } })
  talk(K.UP, "widow_04_loom")
end

local function potter()
  warpInto({}, S.MAP_POTTER)
  shot("potter_01_room.png")
  walkTo({ { 5, 5 }, { 3, 5 } })
  for i = 1, 3 do talk(K.UP, string.format("potter_02_euphronios_%d", i)) end
  expect(getFlag(S.FLAG_EUPHRONIOS_1) and getFlag(S.FLAG_EUPHRONIOS_2) and getFlag(S.FLAG_EUPHRONIOS_3),
         "Euphronios paints a Harpeck, a Chelonet and a Stachyss (FLAG_ICHOR_EUPHRONIOS_1-3)")
  talk(K.UP, "potter_03_after")
end

local function hiringHall()
  warpInto({}, S.MAP_HIRING_HALL)
  local full = metatileAt(14, 2)
  expect(objectPresent(S.LOCALID_CREW_BOSS), "the crew boss is at his pay table")
  shot("hall_01_room.png")
  walkTo({ { 8, 6 }, { 9, 6 }, { 9, 5 } })
  face(K.UP)
  tap(K.A); wait(10)
  playThrough("hall_02_crew_boss", nil, 30000)
  expect(getFlag(S.TRAINER_FLAGS_START + S.TRAINER_CREW_BOSS), "the crew boss is beaten")
  expect(getFlag(S.FLAG_HIRING_HALL), "he gives his Rocky Helmet (FLAG_ICHOR_HIRING_HALL)")
  -- After Act I: the hall is empty, the ledger left open.
  local s = {}
  setFlag(s, S.FLAG_ACT1_COMPLETE)
  warpInto(s, S.MAP_HIRING_HALL)
  expect(not objectPresent(S.LOCALID_CREW_BOSS), "after Act I the crew boss is gone")
  expect(metatileAt(14, 2) ~= full, "after Act I the crates are cleared away")
  shot("hall_03_empty.png")
  walkTo({ { 8, 5 } })
  talk(K.UP, "hall_04_ledger")
end

local function runners()
  -- FLAG_ICHOR_ACT1_COMPLETE is still set from the hall: first the Quick Claw is
  -- skipped for the letter, so clear it, take the claw, then set it again.
  local s = {}
  clearFlag(s, S.FLAG_ACT1_COMPLETE)
  warpInto(s, S.MAP_RUNNERS)
  shot("runners_01_room.png")
  walkTo({ { 5, 4 }, { 4, 4 } })
  talk(K.UP, "runners_02_dromokleia")
  expect(getFlag(S.FLAG_GOT_QUICK_CLAW), "Dromokleia gives a Quick Claw (FLAG_ICHOR_GOT_QUICK_CLAW)")
  local s2 = {}
  setFlag(s2, S.FLAG_ACT1_COMPLETE)
  setup(s2)
  talk(K.UP, "runners_03_letter")
  expect(getFlag(S.FLAG_WROTE_TO_MOM), "after Act I the runners take a letter home (FLAG_ICHOR_WROTE_TO_MOM)")
end

local co = coroutine.create(function()
  boot()
  asclepeion()
  deigma()
  hephaisteion()
  tavern()
  philoxenos()
  widow()
  potter()
  hiringHall()
  runners()
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
    else
      local fn = realEmu[result[3]]
      result = table.pack(coroutine.resume(co, fn(realEmu, table.unpack(result, 4, result.n))))
    end
  end
end)
