-- The world's small systems, run by tools/ichor/tests/ichor_world.sh (read it first).

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local log, expect, wait, shot, tap, settle = L.log, L.expect, L.wait, L.shot, L.tap, L.settle

local function clock(h, m)
  L.setVar(S.VAR_0x8004, h); L.setVar(S.VAR_0x8005, m)
  L.runHeader("WorldTest_ClockHeader")
end
local function hours() return emu:read8(S.gLocalTime + S.OFF_TIME_HOURS) end
local function minutes() return emu:read8(S.gLocalTime + S.OFF_TIME_MINUTES) end
local function menuUp()
  return L.taskRunning("Task_HandleScrollingMultichoiceInput") or L.taskRunning("Task_HandleMultichoiceInput")
end

L.start(function()
  L.quickstart()
  L.setVar(S.VAR_0x8008, 14); L.setVar(S.VAR_0x8009, 22)
  L.runHeader("WorldTest_SetupHeader", { limit = 4000 })
  L.waitUntil(function() return L.mapId() == S.MAP_ROUTE1 and L.idle() end, 3000, "Route 1")
  wait(40)

  -- The rest at 08:00: NOON, DUSK, NIGHT and NOT NOW. The second is DUSK.
  clock(8, 0)
  wait(10)
  expect(hours() == 8, string.format("the clock is set to 08:%02d (%d)", minutes(), hours()))
  L.runHeader("WorldTest_RestHeader", { noSettle = true })
  L.waitUntil(menuUp, 600, "the rest menu")
  wait(20); shot("rest_menu_morning")
  tap(K.DOWN); wait(8); tap(K.A)
  settle()
  wait(30)
  expect(L.getVar(S.VAR_0x8009) == 1 and hours() == 19 and minutes() <= 1,
         string.format("resting until dusk moves the clock to 19:00 (%02d:%02d, answer %d)", hours(), minutes(), L.getVar(S.VAR_0x8009)))
  shot("after_rest_dusk")

  -- NOT NOW leaves the clock alone
  L.runHeader("WorldTest_RestHeader", { noSettle = true })
  L.waitUntil(menuUp, 600, "the rest menu")
  wait(20); shot("rest_menu_dusk")
  tap(K.DOWN); wait(8); tap(K.A)   -- NIGHT, NOT NOW: the second
  settle()
  expect(L.getVar(S.VAR_0x8009) == 0 and hours() == 19, "NOT NOW leaves the clock at dusk")

  -- After 20:30 no hour is left: no menu, and FALSE
  clock(20, 45)
  L.runHeader("WorldTest_RestHeader")
  expect(L.getVar(S.VAR_0x8009) == 0 and hours() == 20, "after 20:30 the rest offers nothing and the clock stays")

  -- Knucklebones: mark a bone, roll it, then stand on every throw after
  local function playBones(opponent, name)
    L.setVar(S.VAR_0x8004, opponent)
    L.runHeader("WorldTest_BonesHeader", { noSettle = true })
    local menus, first = 0, true
    L.waitUntil(function()
      if menuUp() then
        menus = menus + 1
        wait(12)
        if first then
          shot(name .. "_menu")
          tap(K.A); wait(12)                         -- the first bone: KEEP -> ROLL
          L.waitUntil(menuUp, 120, "the menu again")
          wait(12); shot(name .. "_marked")
          for _ = 1, 4 do tap(K.DOWN); wait(6) end   -- ROLL THEM
          tap(K.A)
          first = false

        else
          tap(K.B)                                   -- STAND
        end
        wait(10)
      elseif not L.idle() then
        tap(K.A); wait(6)                            -- through the messages
      end
      return L.idle() and L.getVar(S.VAR_0x8009) ~= 0xFF
    end, 20000, "the match to end")
    return L.getVar(S.VAR_0x8009), menus
  end
  local result, menus = playBones(S.ICHOR_BONES_CAUTIOUS, "bones")
  expect((result == 0 or result == 1) and menus >= 3,
         string.format("a match against a cautious regular plays to its end (%s after %d menus)", result == 1 and "won" or "lost", menus))

  local function record() return emu:read16(L.ichor() + S.OFF_ICHOR_MOM_WINS), emu:read16(L.ichor() + S.OFF_ICHOR_MOM_LOSSES) end
  local w0, l0 = record()
  result = playBones(S.ICHOR_BONES_MOM, "mom")
  local w1, l1 = record()
  expect(l0 == 212 and w1 + l1 == w0 + l0 + 1 and (result == 1) == (w1 == w0 + 1),
         string.format("a match against Mom goes on her record (%d-%d -> %d-%d)", w0, l0, w1, l1))

  -- Theoxenia's tells: a god in disguise (Route 1's youth, rewritten) casts no
  -- shadow, and the follower bows once it comes within 3 tiles
  local GOD, OTHER, GX, GY = 3, 4, 13, 43
  local function shadows(localId)
    local n = 0
    for i = 0, S.MAX_SPRITES - 1 do
      local sp = S.gSprites + i * S.SPRITE_SIZE
      if emu:read32(sp + S.OFF_SPRITE_CALLBACK) & ~1 == S.UpdateShadowFieldEffect & ~1
         and emu:read16(sp + S.OFF_SPRITE_DATA0) == localId then n = n + 1 end
    end
    return n
  end
  L.setVar(S.VAR_0x8008, GX); L.setVar(S.VAR_0x8009, GY + 5)
  L.runHeader("WorldTest_WarpHeader", { limit = 4000 })
  L.waitUntil(function() return L.idle() end, 3000, "the warp")
  wait(30)
  local t = L.sb1() + S.OFF_SB1_TEMPLATES
  for i = 0, 63 do
    local tpl = t + i * S.TEMPLATE_SIZE
    if emu:read8(tpl + S.OFF_TPL_LOCAL_ID) == GOD then
      emu:write16(tpl + S.OFF_TPL_X, GX)
      emu:write16(tpl + S.OFF_TPL_Y, GY)
      emu:write8(tpl + S.OFF_TPL_MOVEMENT, S.MOVEMENT_TYPE_FACE_DOWN)
      emu:write16(tpl + S.OFF_TPL_TRAINER_TYPE, S.TRAINER_TYPE_ICHOR_GOD)
      break
    end
  end
  L.setVar(S.VAR_0x8008, GOD)
  L.runHeader("WorldTest_RespawnHeader")
  wait(30)
  local hasFollower = L.objectAt(0xFE) ~= nil
  expect(L.objectAt(GOD) ~= nil and shadows(GOD) == 0 and shadows(OTHER) + shadows(0xFE) >= 1,
         string.format("a god in disguise casts no shadow (%d), though others do (%d)", shadows(GOD), shadows(OTHER) + shadows(0xFE)))
  expect(hasFollower and emu:read8(S.sBowedAt) == 0, "the follower is out, 4 or more tiles from the god, and hasn't bowed")
  L.step(K.UP); L.step(K.UP); L.step(K.UP)
  wait(40)
  shot("follower_bows")
  local fx, fy = L.objectAt(0xFE)
  expect(emu:read8(S.sBowedAt) == GOD, string.format("within 3 tiles the follower bows to the god (follower at %s,%s)", tostring(fx), tostring(fy)))

  -- The party's highest level (the setup's Piplup is level 20)
  L.runHeader("WorldTest_LevelHeader")
  expect(L.getVar(S.VAR_0x8009) == 20, string.format("Ichor_GetHighestPartyLevel reads the party (%d)", L.getVar(S.VAR_0x8009)))

  -- DAY/NIGHT TINT: noon's colors and 22:00's differ on Route 1; OFF in the
  -- options menu draws noon's at night while the clock still says night; it
  -- survives a save and CONTINUE; ON brings the night back.
  local SLOT, COLOR = 2, 5
  local function faded() return emu:read16(S.gPlttBufferFaded + (SLOT * 16 + COLOR) * 2) end
  local function retint() emu:write16(S.gTimeUpdateCounter, 0); wait(40) end
  local function tintOff() return emu:read8(L.ichor() + S.OFF_ICHOR_OPTIONS_W) & S.ICHOR_OPTION_TINT_OFF ~= 0 end
  local function startMenuTo(action)
    tap(K.START); wait(30)
    local n, index = emu:read8(S.sNumStartMenuActions)
    for i = 0, n - 1 do if emu:read8(S.sCurrentStartMenuActions + i) == action then index = i end end
    if not index then L.fail("no start menu action " .. action) end
    for _ = 1, (index - emu:read8(S.sStartMenuCursorPos)) % n do tap(K.DOWN); wait(4) end
    tap(K.A)
  end
  local function toggleTint(name)
    startMenuTo(6)                                  -- OPTION
    L.waitUntil(function() return L.taskRunning("Task_OptionMenuProcessInput") end, 600, "the option menu")
    wait(30)
    for _ = 1, 7 do tap(K.DOWN); wait(4) end        -- DAY/NIGHT TINT
    shot(name .. "_before")
    tap(K.RIGHT); wait(10)
    shot(name)
    tap(K.B)
    L.waitUntil(function() return not L.taskRunning("Task_OptionMenuProcessInput") end, 600, "the option menu to close")
    wait(90); tap(K.B)                              -- back on the start menu: close it
    L.waitUntil(L.idle, 1200, "the field")
    retint()
  end
  clock(12, 0); retint()
  local noon = faded()
  clock(22, 0); retint()
  local night = faded()
  expect(noon ~= night and not tintOff(), string.format("with the tint ON, 22:00 is tinted (%04X) apart from noon (%04X)", night, noon))
  toggleTint("options_tint_off")
  expect(tintOff() and faded() == noon and emu:read8(S.gTimeOfDay) == S.TIME_NIGHT,
         string.format("OFF draws noon's colors at 22:00 (%04X), and the clock still says night (%d)", faded(), emu:read8(S.gTimeOfDay)))
  shot("night_tint_off")
  L.runHeader("WorldTest_SaveHeader", { answers = { "yes", "yes" } })
  emu:reset()
  L.continueSave()
  retint()
  expect(tintOff() and faded() == noon, string.format("OFF survives a save and CONTINUE (%04X)", faded()))
  toggleTint("options_tint_on")
  expect(not tintOff() and faded() == night, string.format("ON brings the night's colors back (%04X)", faded()))
  shot("night_tint_on")
end)
