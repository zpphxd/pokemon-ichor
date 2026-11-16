local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local glyphs = {}
for line in io.lines("charmap.txt") do
  local c, hex = line:match("^'(.-)'%s*=%s*(%x+)")
  if c == "\\'" then c = "'" end
  if c and #c == 1 then glyphs[c] = tonumber(hex, 16) end
end
local function contains(text)
  local encoded, actual = {}, {}
  for i = 1, #text do encoded[i] = string.char(assert(glyphs[text:sub(i, i)])) end
  for i = 0, 1023 do
    local b = emu:read8(S.gStringVar4 + i)
    if b == 255 then break end
    actual[#actual + 1] = string.char(b)
  end
  return table.concat(actual):find(table.concat(encoded), 1, true) ~= nil
end
local function menu()
  return L.taskRunning("Task_HandleScrollingMultichoiceInput")
end
local function waitMenu()
  L.waitUntil(menu, 1500, "the journal menu")
  L.wait(15)
end
local function choose(index)
  waitMenu()
  local current = L.getVar(S.VAR_0x8000)
  local category = L.getVar(S.VAR_CATEGORY)
  if category == 0 then
    current = ({ [100] = 0, [101] = 1, [40] = 2, [41] = 3 })[current] or 0
  elseif category == 1 then
    current = current < 12 and current or 0
  else
    current = current >= 16 and current < 28 and current - 16 or 0
  end
  local key = index < current and K.UP or K.DOWN
  for _ = 1, math.abs(index - current) do L.tap(key) end
  L.tap(K.A)
  L.waitUntil(function() return not menu() end, 120, "the journal selection")
end
local function read(index, text, name)
  choose(index)
  L.waitUntil(function() return L.boxUp() and contains(text) end, 600, name .. " text")
  L.wait(35)
  L.shot(name)
  L.expect(contains(text), name .. " shows saved progress")
  L.settle{ stop = menu, every = true }
  waitMenu()
end
local function back()
  waitMenu()
  L.tap(K.B)
  L.waitUntil(function() return not menu() end, 120, "B to close the menu")
  L.wait(10)
end
local function open(callbackName)
  callbackName = callbackName or "StartMenuDeedsCallback"
  L.tap(K.START)
  L.waitUntil(function() return L.taskRunning("Task_ShowStartMenu") end, 300, "the start menu")
  L.wait(25)
  local count, target = emu:read8(S.sNumStartMenuActions), nil
  L.expect(count <= 9, "the start menu fits its nine-entry buffer")
  for i = 0, count - 1 do
    local action = emu:read8(S.sCurrentStartMenuActions + i)
    local callback = emu:read32(S.sStartMenuItems + action * S.MENU_ACTION_SIZE + S.OFF_MENU_ACTION_FUNC)
    if callback == (S[callbackName] | 1) then target = i end
  end
  L.expect(target ~= nil, callbackName .. " is in the actual start menu")
  for _ = 1, 9 do
    if emu:read8(S.sStartMenuCursorPos) == target then break end
    L.tap(K.DOWN)
  end
  L.shot("start_menu_deeds")
  L.tap(K.A)
  if callbackName ~= "StartMenuDeedsCallback" then
    L.waitUntil(function() return L.on("CB2_TrainerCard") end, 1500, "the trainer card")
    L.wait(45)
    L.shot("trainer_card_preserved")
    L.expect(L.on("CB2_TrainerCard"), "the player's trainer card remains accessible")
    L.tap(K.B)
    L.waitUntil(function() return L.taskRunning("Task_ShowStartMenu") end, 1800, "the start menu after the card")
    L.wait(25)
    L.tap(K.B)
    L.settle()
    return
  end
  waitMenu()
  L.expect(L.scriptRunning() and L.getVar(S.VAR_CATEGORY) == 0, "the real DEEDS callback opens the journal without a fade")
end

L.start(function()
  L.quickstart()
  L.runHeader("DeedsTest_SetupHeader")
  L.setFlag(S.FLAG_POKEDEX)
  L.setFlag(S.FLAG_POKENAV)
  if S.FLAG_DEXNAV ~= 0 then L.setFlag(S.FLAG_DEXNAV) end
  for i = 0, 6 do L.setFlag(S.FLAG_ICHOR_HERMS_START + i) end
  open()
  choose(1)
  L.waitUntil(function() return contains("No amphorae recorded") end, 600, "the empty amphora page")
  L.settle{ stop = menu, every = true }
  waitMenu()
  L.expect(L.getVar(S.VAR_CATEGORY) == 0, "the empty amphora page returns to the journal contents")
  back()
  L.settle()
  for i = 0, S.AMPHORA_COUNT - 1 do
    for piece = 0, 3 do L.setFlag(S.FLAG_SHERDS + i * 4 + piece) end
    L.setFlag(S.FLAG_AMPHORAE + i, i ~= 0)
  end
  L.setFlag(S.FLAG_RAKNIT)
  local flagsBefore = L.snapshot(L.ichor() + S.OFF_ICHOR_FLAGS, 448)
  open()
  choose(0)
  read(10, "Open.", "pending_moms_parcel")
  L.expect(not L.getFlag(S.FLAG_HONEY), "reading Mom's pending gift cannot claim it")
  read(11, "Pages found: 0 of 7", "scrolling_story_pages")
  back()
  waitMenu()
  choose(1)
  read(0, "Ready for Daphne", "four_sherds_not_restored")
  L.expect(not L.getFlag(S.FLAG_AMPHORAE), "four sherds stay unrestored after journal reading")
  read(1, "Restored.", "persephone_open_lead")
  read(2, "Lead done.", "raknit_claimed_lead")
  read(11, "Ariadne", "twelfth_amphora_scroll")
  back()
  waitMenu()
  read(2, "7 of 23", "herm_count")
  read(3, "Day ", "festival_calendar")
  back()
  L.settle()
  L.expect(L.snapshot(L.ichor() + S.OFF_ICHOR_FLAGS, 448) == flagsBefore, "journal navigation changes no saved quest receipts")
  local x, y = L.pos()
  L.step(K.DOWN)
  local nx, ny = L.pos()
  L.expect(x ~= nx or y ~= ny, "B releases field controls after closing the journal")
  open("StartMenuPlayerNameCallback")

  L.setFlag(S.FLAG_STYLUS)
  open()
  choose(0)
  read(10, "Athena's hint:", "stylus_pending_gift")
  back()
  waitMenu()
  choose(1)
  read(0, "Athena's hint:", "stylus_sherd_hint")
  read(1, "Athena's hint:", "stylus_encounter_hint")
  back()
  waitMenu()
  back()
  L.settle()
  L.runHeader("DeedsTest_SaveHeader")
  emu:reset()
  L.continueSave()
  open()
  choose(1)
  read(2, "Lead done.", "saved_claimed_lead")
  L.expect(L.getFlag(S.FLAG_STYLUS) and not L.getFlag(S.FLAG_HONEY), "saved hints and unclaimed gifts survive CONTINUE")
  back()
  waitMenu()
  back()
  L.settle()
end)
