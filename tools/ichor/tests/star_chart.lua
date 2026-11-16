-- Ownership/collection are fixture inputs; screens are opened through the real Bag.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local function readAsset(name)
  local file = assert(io.open(L.OUT .. name, "rb"))
  local bytes = file:read("a")
  file:close()
  return bytes
end
local iconPixels, iconPalette = readAsset("icon.4bpp"), readAsset("icon.gbapal")
local function checkBagIcon()
  local bag = emu:read32(S.gBagMenu)
  local found
  for _, slot in ipairs({ S.ICON_SLOT, S.ICON_ALT_SLOT }) do
    local id = emu:read8(bag + S.OFF_BAG_SPRITES + slot)
    if id ~= S.SPRITE_NONE then
      L.expect(found == nil, "only the selected item's icon owns a Bag sprite")
      found = id
    end
  end
  L.expect(found ~= nil, "the selected Star Chart has a live icon sprite")
  local attr2 = emu:read16(S.gSprites + found * S.SPRITE_SIZE + S.OFF_SPRITE_OAM + 4)
  local tiles = S.OBJ_VRAM_ADDR + (attr2 & 0x3FF) * 32
  L.expect(#iconPixels == 288 and #iconPalette == 32, "the chart icon is 24x24 4bpp with sixteen colors")
  for row = 0, 2 do
    for i = 0, 95 do
      if emu:read8(tiles + row * 128 + i) ~= iconPixels:byte(row * 96 + i + 1) then
        L.fail("the actual Bag sprite does not display the original chart icon")
      end
    end
  end
  for i = 0, 15 do
    local expected = iconPalette:byte(i * 2 + 1) | iconPalette:byte(i * 2 + 2) << 8
    local offset = (256 + (attr2 >> 12) * 16 + i) * 2
    if emu:read16(S.gPlttBufferFaded + offset) ~= expected then
      L.fail("the actual Bag sprite has the wrong chart color " .. i)
    end
  end
  L.expect(true, "all live icon pixels and colors match the original Star Chart art")
end
local function stars()
  local n = 0
  for i = 0, S.STAR_COUNT - 1 do if L.getFlag(S.FLAG_STARS + i) then n = n + 1 end end
  return n
end
local function selected()
  return emu:read8(emu:read32(S.sStarChart) + S.OFF_CHART_SELECTED)
end
local function panel(star)
  local window = S.gWindows + S.WINDOW_SIZE
  local tiles = emu:read32(window + S.OFF_WINDOW_TILES)
  local pixels, ink = {}, 0
  for dy = 0, 19 do
    for dx = 0, 29 do
      local x, y = 8 + star % 6 * 38 + dx, 6 + star // 6 * 28 + dy
      local byte = emu:read8(tiles + (y // 8 * 30 + x // 8) * 32 + y % 8 * 4 + x % 8 // 2)
      local color = byte >> (x % 2 * 4) & 15
      pixels[#pixels + 1] = string.char(color)
      if color ~= 0 then ink = ink + 1 end
    end
  end
  return table.concat(pixels), ink
end
local function useFromBag()
  emu:write8(S.gBagPosition + S.OFF_BAG_POCKET, S.KEY_POCKET)
  emu:write16(S.gBagPosition + S.OFF_BAG_CURSOR + 2 * S.KEY_POCKET, 0)
  emu:write16(S.gBagPosition + S.OFF_BAG_SCROLL + 2 * S.KEY_POCKET, 0)
  L.tap(K.START)
  L.waitUntil(function() return L.taskRunning("Task_ShowStartMenu") end, 300, "the start menu")
  L.wait(25)
  local n, target = emu:read8(S.sNumStartMenuActions), nil
  for i = 0, n - 1 do
    if emu:read8(S.sCurrentStartMenuActions + i) == 2 then target = i end
  end
  L.expect(target ~= nil, "the Bag is accessible from the start menu")
  for _ = 1, (target - emu:read8(S.sStartMenuCursorPos)) % n do L.tap(K.DOWN) end
  L.tap(K.A)
  L.waitUntil(function() return L.on("CB2_Bag") and L.taskRunning("Task_BagMenu_HandleInput") end, 1200, "the key-item Bag")
  L.wait(30)
  checkBagIcon()
  L.shot("chart_in_key_items")
  L.tap(K.A)
  L.waitUntil(function() return L.taskRunning("Task_ItemContext_SingleRow") or L.taskRunning("Task_ItemContext_MultipleRows") end, 300, "the chart's USE menu")
  L.wait(20)
  L.tap(K.A)
  L.waitUntil(function() return L.on("CB2_StarChart") end, 1200, "the real Star Chart")
  L.wait(40)
  L.expect(emu:read32(S.sStarChart) ~= 0, "the chart owns its screen resources")
  local window = S.gWindows + S.WINDOW_SIZE
  L.expect(emu:read8(window + S.OFF_WINDOW_WIDTH) == 30 and emu:read8(window + S.OFF_WINDOW_HEIGHT) == 16,
           "constellation lines occupy their dedicated 240x128 layer")
end
local function close()
  L.tap(K.B)
  L.waitUntil(function() return L.on("CB2_Bag") and L.taskRunning("Task_BagMenu_HandleInput") end, 1500, "the same Bag pocket")
  L.expect(emu:read32(S.sStarChart) == 0, "closing the chart releases all screen resources")
  L.wait(30)
  checkBagIcon()
  L.shot("back_in_bag")
  L.tap(K.B)
  L.waitUntil(function() return L.inOverworld() or L.taskRunning("Task_ShowStartMenu") end, 1200, "the field")
  L.wait(30)
  if L.taskRunning("Task_ShowStartMenu") then L.tap(K.B) end
  L.settle()
end
local function hold(time)
  L.setVar(S.VAR_0x8004, time)
  L.runHeader("ChartTest_HoldHeader")
end
local function skySeat()
  return L.sign("KallisteRoute1_KronionHill_EventScript_SkySeat")
end
local function openSky()
  L.talk(skySeat(), { answers = {"yes"}, stop = function() return L.on("CB2_StarChart") end })
  L.waitUntil(function() return L.on("CB2_StarChart") end, 900, "the live night sky")
  L.wait(40)
  L.expect(emu:read32(S.sStarChart) ~= 0, "the seat opens the actual shared sky screen")
  L.expect(emu:read16(S.gPlttBufferFaded + 13 * 32 + 2) == (2 | 3 << 5 | 8 << 10),
           "the live sky uses midnight blue instead of the Bag's parchment")
end
local function closeSky(music)
  L.tap(K.B)
  L.waitUntil(L.inOverworld, 1200, "the field after stargazing")
  L.settle()
  local x, y = L.pos()
  L.expect(L.idle() and emu:read32(S.sStarChart) == 0,
           "leaving the sky frees the screen and resumes the seat's real script")
  L.expect(L.mapId() == S.MAP_HILL and x == 15 and y == 9,
           "stargazing returns to the same reachable steps, not the Bag")
  L.expect(L.playingHeader() == music, "the hill's music survives stargazing")
end
L.start(function()
  L.quickstart()
  L.runHeader("ChartTest_SetupHeader")
  for _, flag in ipairs({S.FLAG_CONCH, S.FLAG_BADGE4, S.FLAG_BADGE5, S.FLAG_BADGE7, S.FLAG_BADGE8}) do L.setFlag(flag, false) end
  for i = 0, 6 do L.setFlag(S.FLAG_PAGES + i, false) end
  for i = 0, 15 do emu:write8(L.ichor() + S.OFF_ICHOR_FAVOR + i, 0) end
  for i = 0, 31 do L.setFlag(S.FLAG_STARS + i, false) end
  L.expect(L.itemCount(S.ITEM_CHART) == 1, "the fixture owns one real Star Chart")
  useFromBag()
  L.expect(stars() == 0, "an empty chart cannot invent placed myths")
  L.shot("empty_parchment")
  L.tap(K.LEFT); L.wait(10)
  L.expect(selected() == 23 and not L.getFlag(S.FLAG_STARS + 23), "the last patch stays unplaced and navigation wraps")
  local _, emptyInk = panel(23)
  L.expect(emptyInk == 0, "the Unwoven's patch contains no star pixels before its myth is placed")
  L.shot("unwoven_empty_patch")
  close()
  for i = 0, S.STAR_COUNT - 1 do L.setFlag(S.FLAG_STARS + i) end
  useFromBag()
  L.expect(stars() == 24, "all twenty-four saved placements are displayed")
  local seen = {}
  for i = 0, S.STAR_COUNT - 1 do
    local pixels, ink = panel(i)
    L.expect(ink > 30 and not seen[pixels], "constellation " .. i .. " has its own visible star-and-line pattern")
    seen[pixels] = true
  end
  local color = emu:read16(S.gPlttBufferFaded + (14 * 16 + 2) * 2)
  L.wait(12)
  L.expect(emu:read16(S.gPlttBufferFaded + (14 * 16 + 2) * 2) ~= color, "placed stars twinkle through their palette cycle")
  for i = 0, S.STAR_COUNT - 1 do
    L.expect(selected() == i, "the selected constellation is " .. i)
    L.shot("constellation_" .. i)
    L.tap(K.RIGHT); L.wait(10)
  end
  L.expect(selected() == 0, "right navigation wraps through all twenty-four patches")
  L.tap(K.DOWN); L.wait(10)
  L.expect(selected() == 6, "down moves one row of six patches")
  L.tap(K.UP); L.wait(10)
  L.expect(selected() == 0, "up returns to the previous row")
  close()
  L.runHeader("ChartTest_SaveHeader")
  emu:reset()
  L.continueSave()
  useFromBag()
  L.expect(stars() == 24 and L.itemCount(S.ITEM_CHART) == 1, "placements and the unconsumed chart survive save/reset/CONTINUE")
  L.shot("saved_complete_chart")
  close()
  L.setBeat("stargazing", false)
  for i = 0, S.STAR_COUNT - 1 do L.setFlag(S.FLAG_STARS + i, false) end
  L.runHeader("ChartTest_HillHeader")
  L.expect(L.mapId() == S.MAP_HILL, "the fixture reaches Kronion's actual summit")
  local seat = skySeat()
  L.expect(seat.x == 15 and seat.y == 8, "the seat is the existing eastern shrine steps")
  hold(S.TIME_DAY)
  L.talk(seat, { every = true })
  L.expect(L.idle() and emu:read32(S.sStarChart) == 0,
           "daytime explains the night gate without opening a sky screen")
  L.runHeader("ChartTest_RemoveHeader")
  hold(S.TIME_NIGHT)
  L.talk(seat, { every = true })
  L.expect(L.itemCount(S.ITEM_CHART) == 0 and L.idle() and emu:read32(S.sStarChart) == 0,
           "a night visitor without the real Chart receives a hint, not a sky screen")
  L.runHeader("ChartTest_TrySkyHeader")
  L.expect(L.getVar(S.VAR_TEMP_E) == 0 and emu:read32(S.sStarChart) == 0,
           "the native sky entry also requires actual Chart ownership")
  L.runHeader("ChartTest_GiveHeader")
  L.talk(seat, { answers = {"no"} })
  L.expect(L.idle() and emu:read32(S.sStarChart) == 0, "declining the seat leaves controls and resources untouched")
  L.talk(seat, { stop = function() return L.taskRunning("Task_HandleYesNoInput") end })
  emu:write8(L.ichor() + S.OFF_ICHOR_HELD_TIME, S.TIME_DAY + 1)
  emu:write16(S.gTimeUpdateCounter, 0)
  L.wait(60)
  L.expect(emu:read8(S.gTimeOfDay) == S.TIME_DAY, "the sky prompt can remain open until daylight")
  L.tap(K.A)
  L.settle({ every = true })
  L.expect(L.idle() and emu:read32(S.sStarChart) == 0,
           "daylight during the prompt reports a failed opening and restores field control")
  local visibleColors = 0
  for i = 0, 13 * 16 - 1 do
    if emu:read16(S.gPlttBufferFaded + i * 2) ~= 0 then visibleColors = visibleColors + 1 end
  end
  L.expect(visibleColors > 16, "a refused opening fades back from black to the real field")
  L.shot("daylight_retry")
  hold(S.TIME_NIGHT)
  local music = L.playingHeader()
  openSky()
  L.expect(stars() == 0, "the live sky cannot place unfinished myths")
  local _, ink = panel(23)
  L.expect(ink == 0, "the Unwoven's live patch stays empty")
  L.shot("empty_night_sky")
  closeSky(music)
  L.shot("back_on_steps")
  L.setFlag(S.FLAG_STARS + 0)
  L.setFlag(S.FLAG_STARS + 8)
  openSky()
  L.expect(stars() == 2, "the live sky displays the same two saved myths as the Chart")
  local _, first = panel(0)
  local _, second = panel(8)
  local _, unplaced = panel(23)
  L.expect(first > 30 and second > 30 and unplaced == 0,
           "only the placed dolphin and sisters have actual star-and-line pixels")
  local color = emu:read16(S.gPlttBufferFaded + (14 * 16 + 2) * 2)
  L.wait(12)
  L.expect(emu:read16(S.gPlttBufferFaded + (14 * 16 + 2) * 2) ~= color,
           "the outdoor stars really twinkle")
  L.tap(K.LEFT); L.wait(10)
  L.expect(selected() == 23, "live-sky navigation also reaches the empty final patch")
  L.shot("placed_night_sky")
  closeSky(music)
  openSky()
  L.expect(selected() == 0 and stars() == 2, "reopening the seat resets selection without adding myths")
  closeSky(music)
  L.runHeader("ChartTest_SaveHeader")
  emu:reset()
  L.continueSave()
  L.expect(L.mapId() == S.MAP_HILL and stars() == 2 and L.itemCount(S.ITEM_CHART) == 1,
           "stargazing's saved placements, location and unconsumed Chart survive CONTINUE")
  hold(S.TIME_NIGHT)
  openSky()
  closeSky(L.songHeader(S.MUS_ROUTE1))
  L.runHeader("ChartTest_IndoorHeader")
  L.expect(L.mapId() == S.MAP_AKADEMIA, "the guard fixture really is indoors")
  L.runHeader("ChartTest_TrySkyHeader")
  L.expect(L.getVar(S.VAR_TEMP_E) == 0 and L.idle() and emu:read32(S.sStarChart) == 0,
           "the native sky entry also rejects indoor callers without allocating")
  L.runHeader("ChartTest_HillHeader")
  hold(S.TIME_DAY)
  L.runHeader("ChartTest_TrySkyHeader")
  L.expect(L.getVar(S.VAR_TEMP_E) == 0 and L.idle() and emu:read32(S.sStarChart) == 0,
           "the native sky entry also rejects daytime callers without allocating")
  useFromBag()
  L.expect(stars() == 2 and emu:read16(S.gPlttBufferFaded + 13 * 32 + 2) == (29 | 25 << 5 | 18 << 10),
           "outdoor use does not turn the portable parchment into the live sky")
  close()
end)
