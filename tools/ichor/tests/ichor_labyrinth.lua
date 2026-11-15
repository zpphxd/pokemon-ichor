-- The Labyrinth's engine check, run by tools/ichor/tests/ichor_labyrinth.sh (read it first).

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local log, expect, wait, shot, tap, settle = L.log, L.expect, L.wait, L.shot, L.tap, L.settle

local FLOOR, TWIN = 1, 2
local H, V, NE, NW, SE, SW, CAPN, CAPS, CAPW, CAPE = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
local AX, AY, BX, BY = 15, 49, 19, 49          -- the two bronze rings
local ASTERION = 3                             -- the youth's template, rewritten
local SHEPHERD = 4                             -- Tityros, at (12,49) facing west
local MX, MY = 13, 43                          -- where he stands

-- --- Helpers -------------------------------------------------------------------------------
local function metatile(x, y)
  local width = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_WIDTH)
  local map = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_MAP)
  return emu:read16(map + 2 * ((x + S.MAP_OFFSET) + (y + S.MAP_OFFSET) * width)) & 0x3FF
end
local function gridAddr(x, y)
  local width = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_WIDTH)
  local map = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_MAP)
  return map + 2 * ((x + S.MAP_OFFSET) + (y + S.MAP_OFFSET) * width)
end
local function collision(x, y) return (emu:read16(gridAddr(x, y)) >> 10) & 3 end
local function twin(shape) return TWIN + shape end
local function thread() return L.ichor() + S.OFF_ICHOR_THREAD end
local function anchorCount() return emu:read8(thread() + S.OFF_THR_ANCHOR_COUNT) end
local function current() return emu:read8(thread() + S.OFF_THR_CURRENT) end
local function liveLen() return emu:read8(thread() + S.OFF_THR_LIVE_LEN) end
local function anchorSteps(i) return emu:read16(thread() + S.OFF_THR_ANCHORS + i * S.ANCHOR_SIZE + S.OFF_ANCHOR_STEPS) end
local function menuUp()
  return L.taskRunning("Task_HandleScrollingMultichoiceInput") or L.taskRunning("Task_HandleMultichoiceInput")
end
local function warpTo(x, y)
  L.setVar(S.VAR_0x8008, x); L.setVar(S.VAR_0x8009, y)
  L.runHeader("LabTest_WarpHeader", { limit = 4000 })
  L.waitUntil(function() local px, py = L.pos() return px == x and py == y and L.idle() end, 3000, "the warp")
  wait(30)
end
local function setDark(on)
  local a = S.gMapHeader + S.OFF_MAPHEADER_FLAGS_BYTE
  local b = emu:read8(a)
  if on then b = b | (1 << S.MAPHEADER_CAVE_BIT) else b = b & ~(1 << S.MAPHEADER_CAVE_BIT) end
  emu:write8(a, b)
  emu:write8(L.sb1() + S.OFF_SB1_FLASH_LEVEL, on and 7 or 0)
end
-- Open the Thread's menu and pick entry `index`; `pick` then chooses in the RETURN TO list.
local function threadMenu(index, name, pick)
  L.runHeader("LabTest_ThreadMenuHeader", { noSettle = true })
  L.waitUntil(menuUp, 600, "the Thread's menu")
  wait(20); shot(name)
  for _ = 1, index do tap(K.DOWN); wait(8) end
  tap(K.A)
  if pick then
    L.waitUntil(function() return not menuUp() end, 120, "the menu to close")
    L.waitUntil(menuUp, 600, "the RETURN TO list")
    wait(20); shot(name .. "_list")
    for _ = 1, pick do tap(K.DOWN); wait(8) end
    tap(K.A)
  end
  settle({ limit = 4000 })
  wait(10)
end
local function asterion()
  for i = 0, S.OBJECT_EVENTS_COUNT - 1 do
    local o = S.gObjectEvents + i * S.OBJECT_EVENT_SIZE
    if emu:read8(o) & 1 == 1 and emu:read8(o + S.OFF_OBJ_LOCAL_ID) == ASTERION then return o end
  end
end
local function asterionAt()
  local o = asterion()
  if not o then return nil end
  local c = o + S.OFF_OBJ_CURRENT_COORDS
  return emu:read16(c) - S.MAP_OFFSET, emu:read16(c + 2) - S.MAP_OFFSET
end
local function asterionFacing() return emu:read8(asterion() + S.OFF_OBJ_FACING) & 0xF end
-- Route 1 with Asterion at (MX, MY) facing `movement`, dark unless `lit`; the
-- player at (px, py). `options` are ICHOR_CHARGER_* bits; `script` replaces his
-- object script (for ICHOR_CHARGER_HIT_SCRIPT).
local function stage(px, py, movement, lit, options, script)
  warpTo(px, py)
  local t = L.sb1() + S.OFF_SB1_TEMPLATES
  for i = 0, 63 do
    local tpl = t + i * S.TEMPLATE_SIZE
    if emu:read8(tpl + S.OFF_TPL_LOCAL_ID) == ASTERION then
      emu:write16(tpl + S.OFF_TPL_X, MX)
      emu:write16(tpl + S.OFF_TPL_Y, MY)
      emu:write8(tpl + S.OFF_TPL_MOVEMENT, movement)
      emu:write16(tpl + S.OFF_TPL_TRAINER_TYPE, 0)
      emu:write16(tpl + S.OFF_TPL_TRAINER_TYPE + 2, 0)
      if script then emu:write32(tpl + S.OFF_TPL_SCRIPT, script) end
      break
    end
  end
  L.setVar(S.VAR_0x8008, ASTERION)
  L.runHeader("LabTest_RespawnHeader")
  L.setVar(S.VAR_0x800A, options or 0)
  L.runHeader("LabTest_AsterionHeader")
  setDark(not lit)
  wait(20)
end
local function steps(keys) for _, k in ipairs(keys) do L.step(k) end end

L.start(function()
  L.quickstart()
  L.setVar(S.VAR_0x8008, AX); L.setVar(S.VAR_0x8009, AY)
  L.runHeader("LabTest_SetupHeader", { limit = 4000 })
  L.waitUntil(function() return L.mapId() == S.MAP_ROUTE1 and L.idle() end, 3000, "Route 1")
  wait(40)

  -- === Ariadne's Thread ===============================================================
  L.runHeader("LabTest_ThreadMapHeader")
  wait(10)
  expect(anchorCount() == 1 and current() == 0, "standing on a bronze ring, the first segment starts tied")

  steps({ K.RIGHT, K.RIGHT, K.RIGHT, K.RIGHT })
  expect(metatile(AX, AY) == twin(CAPE) and metatile(16, 49) == twin(H) and metatile(18, 49) == twin(H)
         and metatile(BX, BY) == twin(CAPW) and liveLen() == 4,
         string.format("four steps east lay four tiles of thread (%d %d %d %d %d)",
           metatile(15, 49), metatile(16, 49), metatile(17, 49), metatile(18, 49), metatile(19, 49)))
  L.step(K.UP)
  expect(metatile(BX, BY) == twin(NW) and metatile(19, 48) == twin(CAPS), "a turn north draws a corner")
  shot("laid")
  L.step(K.DOWN)
  expect(metatile(19, 48) == FLOOR and metatile(BX, BY) == twin(CAPW) and liveLen() == 4,
         "stepping back winds the thread up")

  threadMenu(0, "menu_on_ring")  -- TIE OFF
  expect(anchorCount() == 2 and anchorSteps(0) == 4 and current() == 1 and liveLen() == 0,
         string.format("TIE OFF commits 4 steps and makes this ring current (anchors %d, steps %d, current %d)",
           anchorCount(), anchorSteps(0), current()))
  expect(metatile(BX, BY) == twin(CAPW), "the tied thread stays drawn")

  steps({ K.UP, K.LEFT })
  expect(metatile(19, 48) == twin(SW) and metatile(18, 48) == twin(CAPE), "new thread from the ring")
  threadMenu(1, "menu_off_ring")  -- RETURN TO, WIND IN, LEAVE: WIND IN
  expect(liveLen() == 0 and metatile(19, 48) == FLOOR and metatile(18, 48) == FLOOR and metatile(BX, BY) == twin(CAPW),
         "WIND IN takes the new thread up and leaves the tied thread")

  -- The spool runs low: 108 steps already laid (back and forth east of the ring)
  L.step(K.DOWN); L.step(K.RIGHT)
  local px, py = L.pos()
  expect(px == BX and py == BY, string.format("back on the ring (%d,%d)", px, py))
  for i = 0, 26 do emu:write8(thread() + S.OFF_THR_LIVE + i, 0xBB) end  -- E, W, E, W ...
  emu:write8(thread() + S.OFF_THR_LIVE_LEN, 108)
  L.step(K.UP)
  emu:addKey(K.LEFT)
  local warned = false
  for _ = 1, 60 do wait(1) if L.boxUp() then warned = true end end
  emu:clearKey(K.LEFT)
  shot("spool_low")
  settle()
  expect(warned and liveLen() == 110, string.format("at 10 left: \"The spool is nearly empty.\" (%d laid)", liveLen()))
  threadMenu(1, "wind_spool")
  expect(liveLen() == 0, "wound in again")

  -- A map load: the thread is saved and drawn again, even where the Turning dropped a wall
  warpTo(AX, AY)
  emu:write16(gridAddr(17, 49), 739 | (1 << 10))
  L.runHeader("LabTest_ThreadMapHeader")
  wait(10)
  expect(metatile(AX, AY) == twin(CAPE) and metatile(16, 49) == twin(H) and metatile(BX, BY) == twin(CAPW),
         "after a map load the tied thread is drawn again")
  expect(metatile(17, 49) == twin(H) and collision(17, 49) == 0, "a wall dropped on the thread is drawn open again")
  shot("redrawn")

  -- RETURN TO… the second ring
  threadMenu(1, "return", 1)
  px, py = L.pos()
  expect(px == BX and py == BY, string.format("RETURN TO… follows the thread to the second ring (%d,%d)", px, py))

  -- === The Helm of Darkness against a trainer (the shepherd at (12,49), sight 3) ========
  warpTo(9, 48)
  setDark(true)
  L.setFlag(S.FLAG_ICHOR_HELM_ON, true)
  wait(4)
  local sp = S.gSprites + emu:read8(L.playerObject() + S.OFF_OBJ_SPRITE_ID) * S.SPRITE_SIZE
  expect((emu:read16(sp) >> 10) & 3 == 1, "with the Helm on, the player is translucent")
  local r = L.step(K.DOWN)
  wait(60)
  expect(r == "moved" and L.idle(), "helmed in the dark, three tiles in front of a trainer: unseen")
  shot("helm_dark")
  setDark(false)
  L.step(K.UP); L.step(K.DOWN)
  wait(60)
  expect(L.idle(), "helmed in light, at three tiles: unseen (the Helm leaves 2)")
  r = L.step(K.RIGHT)
  L.waitUntil(function() return L.inBattle() or not L.idle() end, 120, "the trainer at two tiles")
  expect(r == "taken" or not L.idle(), "helmed in light, at two tiles: seen")
  settle({ limit = 20000 })  -- the shepherd's battle
  L.setFlag(S.FLAG_ICHOR_HELM_ON, false)

  -- === A Titan sentry (the shepherd again, unbeaten, sight 5) and the disguise ===========
  warpTo(9, 47)                                  -- out of his line first
  L.setFlag(S.TRAINER_FLAGS_START + S.TRAINER_ICHOR_TITYROS, false)
  L.setFlag(S.FLAG_SYS_B_DASH, true)
  local t = L.sb1() + S.OFF_SB1_TEMPLATES
  for i = 0, 63 do
    local tpl = t + i * S.TEMPLATE_SIZE
    if emu:read8(tpl + S.OFF_TPL_LOCAL_ID) == SHEPHERD then
      emu:write16(tpl + S.OFF_TPL_TRAINER_TYPE, S.TRAINER_TYPE_ICHOR_SENTRY)
      emu:write16(tpl + S.OFF_TPL_TRAINER_TYPE + 2, 5)
      break
    end
  end
  L.setVar(S.VAR_0x8008, SHEPHERD)
  L.runHeader("LabTest_RespawnHeader")
  L.setFlag(S.FLAG_ICHOR_DISGUISE_ON, true)
  r = L.step(K.DOWN)                             -- (9,48): the lane beside his, 3 out
  wait(60)
  expect(r == "moved" and L.idle(), "disguised and walking, in a sentry's side lane: taken for a recruit")
  steps({ K.DOWN, K.RIGHT, K.RIGHT })            -- (11,49): right in front of him
  emu:addKey(K.RIGHT)
  local bumped = false
  for _ = 1, 60 do wait(1) if L.boxUp() then bumped = true end end
  emu:clearKey(K.RIGHT)
  shot("recruit")
  settle()
  expect(bumped, "walking into him: \"Watch it, recruit.\"")
  steps({ K.UP, K.LEFT })                        -- (10,48): the side lane, 2 out, walking
  wait(30)
  expect(L.idle(), "still a recruit, walking")
  emu:addKey(K.B)
  r = L.step(K.LEFT)                             -- running into (9,48), 3 out
  emu:clearKey(K.B)
  L.waitUntil(function() return L.inBattle() or not L.idle() end, 120, "the sentry")
  expect(not L.idle(), "running within 3 tiles of a sentry's band gives the disguise away")
  settle({ limit = 20000 })
  L.setFlag(S.FLAG_ICHOR_DISGUISE_ON, false)

  -- === Asterion ==========================================================================
  -- He sees, charges, misses the dodging player and breaks the cracked wall at (13,50)
  stage(15, 47, S.MOVEMENT_TYPE_FACE_DOWN)
  steps({ K.LEFT, K.LEFT })
  L.step(K.UP)                                   -- (13,46): three tiles in front of him, in the dark
  L.step(K.RIGHT)                                -- out of his line, inside the warning
  shot("alert")
  local lowest = MY
  for _ = 1, 120 do
    wait(1)
    local _, y = asterionAt()
    if y and y > lowest then lowest = y end
    if lowest == 47 then shot("charge") end
  end
  settle()
  expect(metatile(13, 50) == FLOOR and L.getFlag(S.FLAG_TEMP_1) and lowest == 50,
         string.format("the charge broke the cracked wall and carried him into the gap (down to y=%d)", lowest))
  shot("breakthrough")
  wait(400)
  local ax, ay = asterionAt()
  expect(ax == MX and ay == MY, string.format("stunned, then he walks back up his line (%d,%d)", ax or -1, ay or -1))

  -- He knocks down a player who stays in the line: back to the current ring
  stage(15, 47, S.MOVEMENT_TYPE_FACE_DOWN)
  steps({ K.LEFT, K.LEFT, K.UP })
  L.waitUntil(function() return not L.idle() end, 200, "the charge to land")
  shot("knockdown")
  settle({ limit = 4000 })
  L.waitUntil(L.idle, 3000, "the field after the knockdown")
  px, py = L.pos()
  expect(px == AX and py == AY, string.format("knocked down, the player wakes at the current ring (%d,%d)", px, py))

  -- He hears a step close by, turns to listen, and goes back to his post
  stage(15, 45, S.MOVEMENT_TYPE_FACE_LEFT)
  L.step(K.UP)                                   -- (15,44): 3 away
  wait(20)
  expect(asterionFacing() == S.DIR_WEST, "three tiles away, he hears nothing")
  L.step(K.LEFT)                                 -- (14,44): 2 away, off his line
  wait(12)
  expect(asterionFacing() == S.DIR_SOUTH, "two tiles away, he turns toward the step")
  wait(90)
  expect(asterionFacing() == S.DIR_WEST and L.idle(), "seeing no one, he turns back to his watch")

  -- The Helm of Darkness: in his line in the dark, unseen
  stage(15, 47, S.MOVEMENT_TYPE_FACE_DOWN)
  L.setFlag(S.FLAG_ICHOR_HELM_ON, true)
  steps({ K.LEFT, K.LEFT, K.UP })
  wait(150)
  px, py = L.pos()
  ax, ay = asterionAt()
  expect(px == 13 and py == 46 and ax == MX and ay == MY and L.idle(), "helmed in the dark, three tiles in front of him: unseen")
  L.setFlag(S.FLAG_ICHOR_HELM_ON, false)

  -- The bronze bell: he rests for three of your steps, then wakes and sees you
  stage(14, 46, S.MOVEMENT_TYPE_FACE_DOWN)
  L.runHeader("LabTest_RestHeader")
  L.step(K.LEFT)                                 -- step 1, into his line
  wait(90)
  expect(L.idle() and select(1, L.pos()) == 13, "resting, he doesn't see the player in his line")
  L.step(K.RIGHT); L.step(K.LEFT)                -- steps 2 and 3: he wakes
  L.waitUntil(function() return not L.idle() end, 300, "Asterion to wake and charge")
  settle({ limit = 4000 })
  L.waitUntil(L.idle, 3000, "the field after the knockdown")
  px, py = L.pos()
  expect(px == AX and py == AY, string.format("awake after three steps, he charges (%d,%d)", px, py))

  -- === Labor 4's boar: Asterion's AI with options =======================================
  -- Deaf: a step two tiles off his line, and he doesn't turn
  stage(15, 45, S.MOVEMENT_TYPE_FACE_LEFT, true, S.ICHOR_CHARGER_DEAF)
  L.step(K.UP); L.step(K.LEFT)                   -- (14,44): 2 away
  wait(40)
  expect(asterionFacing() == S.DIR_WEST, "a deaf charger doesn't turn toward a step")

  -- A drift stops the charge and holds him; with NO_RETURN he stays where he stuck
  stage(15, 47, S.MOVEMENT_TYPE_FACE_DOWN, false, S.ICHOR_CHARGER_NO_RETURN)  -- dark: he sees 3, so the dodge is in time
  L.runHeader("LabTest_DriftHeader")
  steps({ K.LEFT, K.LEFT })
  L.step(K.UP)                                   -- (13,46): in his line
  L.step(K.RIGHT)                                -- out of it
  wait(150)
  local bx, by = asterionAt()
  expect(by == 48 and L.getFlag(S.FLAG_TEMP_2), string.format("the charge ploughs into the drift at (13,48) and sets its flag (%d,%d)", bx or -1, by or -1))
  wait(260)
  bx, by = asterionAt()
  expect(by == 48, "five seconds on, he's still stuck in the snow")
  wait(300)
  bx, by = asterionAt()
  expect(by == 48 and L.idle(), "free again, he doesn't walk back up his line")

  -- A hit runs his own script instead of the knockdown
  stage(15, 47, S.MOVEMENT_TYPE_FACE_DOWN, false, S.ICHOR_CHARGER_HIT_SCRIPT, L.headers["LabTest_BoarHitScript"])
  L.setVar(S.VAR_TEMP_4, 0); L.setVar(S.VAR_TEMP_5, 0)
  steps({ K.LEFT, K.LEFT, K.UP })                -- (13,46), and stay
  L.waitUntil(function() return L.getVar(S.VAR_TEMP_5) ~= 0 end, 400, "the boar's hit script")
  settle()
  px, py = L.pos()
  expect(L.getVar(S.VAR_TEMP_4) == ASTERION and L.getVar(S.VAR_TEMP_5) == S.ICHOR_CHARGE_HIT and px == 13 and py == 46,
         "a hit runs the charger's own script (VAR_0x8004 its id, VAR_0x8005 ICHOR_CHARGE_HIT), with no knockdown warp")

  -- === A dial ===========================================================================
  L.runHeader("LabTest_DialHeader")
  expect(L.getVar(S.VAR_TEMP_3) == 0xFF, "without the Labrys, the dial won't turn")
  L.setVar(S.VAR_0x8004, S.ITEM_LABRYS); L.setVar(S.VAR_0x8005, 1)
  L.runHeader("LabTest_GiveHeader")
  L.runHeader("LabTest_DialHeader", { answers = { "yes" } })
  expect(L.getVar(S.VAR_TEMP_3) == 1 and L.getVar(S.VAR_TEMP_2) == 8, "the Labrys turns it to B (bit 3 set)")
  L.runHeader("LabTest_DialHeader", { answers = { "yes" } })
  expect(L.getVar(S.VAR_TEMP_3) == 0 and L.getVar(S.VAR_TEMP_2) == 0, "and back to A")
end)
