-- Collection flags are fixture inputs; every restoration is through the real shelf.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local SHELF = "ElaiaVillage_Akademia_EventScript_Scrolls"
local f = assert(io.open("graphics/ichor/amphorae.4bpp", "rb"))
local pictures = f:read("a")
f:close()

local function pictureWindow()
  local encoded = emu:read8(S.sAmphoraWindowIdPlusOne)
  return encoded == 0 and S.WINDOW_NONE or encoded - 1
end

local function parts(amphora, count)
  for piece = 0, S.SHERD_COUNT - 1 do
    L.setFlag(S.FLAG_SHERDS + amphora * S.SHERD_COUNT + piece, piece < count)
  end
end

local function countRestored()
  local count = 0
  for amphora = 0, S.AMPHORA_COUNT - 1 do
    if L.getFlag(S.FLAG_AMPHORAE + amphora) then count = count + 1 end
  end
  return count
end

local function readShelf(amphora, answers, requirePicture)
  local seen = false
  L.talk(L.sign(SHELF), {
    answers = answers or { amphora, "yes" }, every = true,
    stop = function()
      local id = pictureWindow()
      if id ~= S.WINDOW_NONE and not seen then
        seen = true
        local window = S.gWindows + id * S.WINDOW_SIZE
        L.expect(emu:read8(window + S.OFF_WINDOW_WIDTH) == 8 and emu:read8(window + S.OFF_WINDOW_HEIGHT) == 8,
                 "amphora " .. amphora .. " uses the required 64x64 picture window")
        local tiles = emu:read32(window + S.OFF_WINDOW_TILES)
        for i = 0, 2047 do
          if emu:read8(tiles + i) ~= pictures:byte(amphora * 2048 + i + 1) then
            L.fail("amphora " .. amphora .. " displays the wrong painting at byte " .. i)
          end
        end
        L.expect(true, "amphora " .. amphora .. " displays all 2048 bytes of its own painting")
        L.wait(2)
        L.shot("painting_" .. amphora)
      end
      return false
    end,
  })
  L.expect(seen == requirePicture, "amphora " .. amphora .. " picture visibility matches restoration")
  L.expect(pictureWindow() == S.WINDOW_NONE, "the painting window is released after reading")
end

local function saveAndContinue()
  L.runHeader("AmphoraeTest_SaveHeader")
  emu:reset()
  L.continueSave()
end

local function fillPocket()
  local pocket = L.sb1() + S.OFF_SB1_BAG
  local key = emu:read32(L.sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
  local saved = {}
  for i = 0, S.BAG_ITEMS_COUNT - 1 do
    local slot = pocket + i * S.ITEM_SLOT_SIZE
    saved[i] = { emu:read16(slot), emu:read16(slot + 2) ~ key }
    emu:write16(slot, S.ITEM_HONEY)
    emu:write16(slot + 2, S.MAX_BAG_ITEM_CAPACITY ~ key)
  end
  return function()
    pocket = L.sb1() + S.OFF_SB1_BAG
    key = emu:read32(L.sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
    for i = 0, S.BAG_ITEMS_COUNT - 1 do
      emu:write16(pocket + i * S.ITEM_SLOT_SIZE, saved[i][1])
      emu:write16(pocket + i * S.ITEM_SLOT_SIZE + 2, saved[i][2] ~ key)
    end
  end
end

L.start(function()
  L.expect(#pictures == S.AMPHORA_COUNT * 2048, "the asset contains twelve distinct 64x64 4bpp panels")
  L.quickstart()
  L.runHeader("AmphoraeTest_SetupHeader")
  L.expect(L.mapId() == S.MAP_AKADEMIA and L.getFlag(S.FLAG_DAPHNE_HIDDEN) and not L.objectAt(S.LOCALID_DAPHNE),
           "the real shelf stays available while Daphne is away after the Mysteries")
  L.talk(L.sign(SHELF), { every = true })
  L.expect(countRestored() == 0 and not L.getFlag(S.FLAG_PATCH), "the empty shelf explains collecting without granting anything")
  parts(0, 3)
  readShelf(0, { 0 }, false)
  L.expect(countRestored() == 0, "three pieces cannot restore an amphora")
  parts(0, 4)
  readShelf(0, { 0, "no" }, false)
  L.expect(countRestored() == 0, "declining restoration keeps all four pieces pending")
  local cancelled = false
  L.talk(L.sign(SHELF), { stop = function()
    if L.taskRunning("Task_HandleScrollingMultichoiceInput") then
      cancelled = true
      L.wait(20)
      L.shot("shelf_cancel")
      L.tap(K.B)
      L.wait(20)
      return true
    end
    return false
  end })
  L.settle()
  L.expect(cancelled and countRestored() == 0, "B cancels the real shelf menu without claiming restoration")

  for amphora = 0, S.AMPHORA_COUNT - 2 do
    parts(amphora, 4)
    readShelf(amphora, nil, true)
    L.expect(countRestored() == amphora + 1 and L.getFlag(S.FLAG_AMPHORAE + amphora),
             "the real menu restores amphora " .. amphora .. " exactly once")
    for piece = 0, S.SHERD_COUNT - 1 do
      L.expect(L.getFlag(S.FLAG_SHERDS + amphora * S.SHERD_COUNT + piece), "restoration retains its collected sherd record")
    end
  end
  L.expect(emu:read8(L.ichor() + S.OFF_ICHOR_FAVOR + S.GOD_HEPHAESTUS) == 5
           and emu:read8(L.ichor() + S.OFF_ICHOR_FAVOR + S.GOD_APHRODITE) == 5,
           "the real Hephaestus and Paris restorations each grant five Favor")
  parts(11, 4)
  L.expect(not L.getFlag(S.FLAG_PATCH) and L.itemCount(S.ITEM_PATCH) == 0,
           "collecting all forty-eight sherds does not grant the twelve-restoration reward")
  local restore = fillPocket()
  readShelf(11, nil, true)
  L.expect(countRestored() == 12 and not L.getFlag(S.FLAG_PATCH) and L.itemCount(S.ITEM_PATCH) == 0,
           "a full Bag keeps the last-page Ability Patch pending without undoing restoration")
  saveAndContinue()
  L.expect(countRestored() == 12 and not L.getFlag(S.FLAG_PATCH), "all twelve restorations and the pending reward survive CONTINUE")
  restore()
  readShelf(0, { 0 }, true)
  L.expect(L.getFlag(S.FLAG_PATCH) and L.itemCount(S.ITEM_PATCH) == 1, "making room claims exactly one Ability Patch")
  saveAndContinue()
  readShelf(10, { 10 }, true)
  L.expect(countRestored() == 12 and L.itemCount(S.ITEM_PATCH) == 1, "saved restorations remain readable without repeating the collection gift")
  L.expect(emu:read8(L.ichor() + S.OFF_ICHOR_FAVOR + S.GOD_HEPHAESTUS) == 5
           and emu:read8(L.ichor() + S.OFF_ICHOR_FAVOR + S.GOD_APHRODITE) == 5,
           "rereading restored myths cannot repeat their Favor")
  L.shot("shelf_after_reading")
end)
