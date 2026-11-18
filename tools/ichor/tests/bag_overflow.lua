-- The never-full Bag, run by tools/ichor/tests/bag_overflow.sh (read it first).
--
--   1. A new game has the big Bag at SaveBlock1's end, marked with its layout magic.
--   2. With the Items pocket full, an item ball (finditem), a gift (giveitem), a
--      hidden item and a shop purchase each land in the Pithos's stored things,
--      and each says so ("...went to your Pithos").
--   3. With room in the Bag, the same gift goes to the Bag with the usual line.
--   4. Only with the Pithos full as well is a gift refused, and nothing is lost.
--   5. Everything survives a save and CONTINUE.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local expect, wait, tap = L.expect, L.wait, L.tap

-- --- Messages ---------------------------------------------------------------------------------

-- Plain ASCII letters and spaces in the game's charset (charmap.txt).
local function enc(s)
  local out = {}
  for c in s:gmatch(".") do
    local b = c:byte()
    if c == " " then out[#out + 1] = "00"
    elseif b >= 65 and b <= 90 then out[#out + 1] = string.format("%02X", 0xBB + b - 65)
    elseif b >= 97 and b <= 122 then out[#out + 1] = string.format("%02X", 0xD5 + b - 97) end
  end
  return table.concat(out)
end
local function var4()
  local hex = {}
  for i = 0, 511 do
    local b = emu:read8(S.gStringVar4 + i)
    if b == 0xFF then break end
    hex[#hex + 1] = string.format("%02X", b)
  end
  return table.concat(hex)
end
local seen = {}
local logText = L.logText
function L.logText() seen[#seen + 1] = var4(); logText() end
local function said(words)
  local want = enc(words)
  for _, t in ipairs(seen) do if t:find(want, 1, true) then return true end end
  return var4():find(want, 1, true) ~= nil
end

-- --- The Bag and the Pithos ---------------------------------------------------------------------

local function key() return emu:read32(L.sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF end
local function pocket(off) return L.sb1() + S.OFF_SB1_BAG + off end
local function count(base, n, item, encrypted)
  local total, k = 0, encrypted and key() or 0
  for i = 0, n - 1 do
    local slot = base + i * S.ITEM_SLOT_SIZE
    if emu:read16(slot) == item then total = total + (emu:read16(slot + 2) ~ k) end
  end
  return total
end
local function bagCount(item)
  local n = 0
  for _, p in ipairs({ { S.OFF_BAG_ITEMS, S.BAG_ITEMS_COUNT }, { S.OFF_BAG_KEY_ITEMS, S.BAG_KEYITEMS_COUNT },
                       { S.OFF_BAG_BALLS, S.BAG_POKEBALLS_COUNT }, { S.OFF_BAG_TMHM, S.BAG_TMHM_COUNT },
                       { S.OFF_BAG_BERRIES, S.BAG_BERRIES_COUNT } }) do
    n = n + count(pocket(p[1]), p[2], item, true)
  end
  return n
end
local function pithosCount(item) return count(L.sb1() + S.OFF_SB1_PC_ITEMS, S.PC_ITEMS_COUNT, item, false) end
local function fill(base, n, item, encrypted)
  local saved, k = {}, encrypted and key() or 0
  for i = 0, n - 1 do
    local slot = base + i * S.ITEM_SLOT_SIZE
    saved[i] = { emu:read16(slot), emu:read16(slot + 2) }
    emu:write16(slot, item)
    emu:write16(slot + 2, S.MAX_BAG_ITEM_CAPACITY ~ k)
  end
  return function()
    for i = 0, n - 1 do
      emu:write16(base + i * S.ITEM_SLOT_SIZE, saved[i][1])
      emu:write16(base + i * S.ITEM_SLOT_SIZE + 2, saved[i][2])
    end
  end
end
local function money() return emu:read32(L.sb1() + S.OFF_SB1_MONEY) ~ emu:read32(L.sb2() + S.OFF_SB2_ENCRYPTION_KEY) end

local function run(header, what)
  seen = {}
  L.runHeader(header)
  L.shot(what)
end

L.start(function()
  L.quickstart()
  L.log(string.format("pockets: items %d, key items %d, balls %d, TMs %d, berries %d; Pithos %d",
    S.BAG_ITEMS_COUNT, S.BAG_KEYITEMS_COUNT, S.BAG_POKEBALLS_COUNT, S.BAG_TMHM_COUNT, S.BAG_BERRIES_COUNT, S.PC_ITEMS_COUNT))
  expect(emu:read32(L.sb1() + S.OFF_SB1_BAG_LAYOUT) == S.ICHOR_BAG_LAYOUT_MAGIC, "a new game marks the big Bag's layout")
  expect(S.BAG_ITEMS_COUNT > 30 and S.BAG_KEYITEMS_COUNT > 30 and S.BAG_POKEBALLS_COUNT > 16
         and S.BAG_BERRIES_COUNT > 46 and S.PC_ITEMS_COUNT > 50, "every pocket and the Pithos are bigger than before")

  -- 2. A full Items pocket.
  fill(pocket(S.OFF_BAG_ITEMS), S.BAG_ITEMS_COUNT, S.ITEM_HONEY, true)
  expect(bagCount(S.ITEM_HONEY) == S.BAG_ITEMS_COUNT * S.MAX_BAG_ITEM_CAPACITY, "the Items pocket is full of Honey")

  local before = pithosCount(S.ITEM_POTION)
  run("BagOverflow_FindHeader", "item_ball")
  expect(pithosCount(S.ITEM_POTION) == before + 1 and bagCount(S.ITEM_POTION) == 0,
         "an item ball's Potion goes to the Pithos when the Bag is full")
  expect(said("went to your Pithos") and not said("Too bad"), "the item ball says the Potion went to the Pithos")

  run("BagOverflow_GiftHeader", "gift")
  expect(L.getVar(S.VAR_0x8000) == 1 and pithosCount(S.ITEM_SUPER_POTION) == 1 and bagCount(S.ITEM_SUPER_POTION) == 0,
         "a gift's Super Potion goes to the Pithos when the Bag is full")
  expect(said("went to your Pithos") and said("Super Potion"), "the gift says the Super Potion went to the Pithos")

  run("BagOverflow_HiddenHeader", "hidden_item")
  expect(pithosCount(S.ITEM_ETHER) == 1 and L.getFlag(1), "a hidden Ether goes to the Pithos, and the spot is used up")
  expect(said("went to your Pithos"), "the hidden item says the Ether went to the Pithos")

  -- The shop: BUY, the first item, one of it, YES.
  local cash, antidotes = money(), pithosCount(S.ITEM_ANTIDOTE)
  seen = {}
  L.runHeader("BagOverflow_MartHeader", { noSettle = true })
  local t0 = L.now()
  while not L.taskRunning("Task_ShopMenu") do
    tap(K.A); wait(20)
    if L.now() - t0 > 900 then L.fail("the shop menu never opened") end
  end
  wait(20); tap(K.A)
  L.waitUntil(function() return L.taskRunning("Task_BuyMenu") end, 600, "the shop's item list")
  wait(40); tap(K.A)
  L.waitUntil(function() return L.taskRunning("Task_BuyHowManyDialogueHandleInput") end, 600, "how many")
  wait(10); tap(K.A)
  wait(150); L.shot("shop_confirm"); tap(K.A)   -- the shop's own YES/NO, YES first
  L.waitUntil(function() return var4():find(enc("went to your Pithos"), 1, true) ~= nil end, 600, "the shop's Pithos line")
  wait(60); L.shot("shop_pithos")
  expect(not said("no more room"), "the shop never says there's no room")
  local t1 = L.now()
  while not L.taskRunning("Task_BuyMenu") do
    tap(K.A); wait(30)
    if L.now() - t1 > 900 then L.fail("the item list never came back") end
  end
  expect(pithosCount(S.ITEM_ANTIDOTE) == antidotes + 1 and bagCount(S.ITEM_ANTIDOTE) == 0 and money() < cash,
         "buying with a full Bag puts the Antidote in the Pithos and takes the money")
  wait(20); tap(K.B)
  L.waitUntil(function() return L.taskRunning("Task_ShopMenu") end, 600, "the shop menu again")
  wait(20); tap(K.B)
  L.settle()

  -- 3. Room in the Bag: the usual pocket line.
  local restoreSlot = function()
    local slot = pocket(S.OFF_BAG_ITEMS) + (S.BAG_ITEMS_COUNT - 1) * S.ITEM_SLOT_SIZE
    emu:write16(slot, 0); emu:write16(slot + 2, 0 ~ key())
  end
  restoreSlot()
  local pithosSuper = pithosCount(S.ITEM_SUPER_POTION)
  run("BagOverflow_GiftHeader", "gift_to_bag")
  expect(bagCount(S.ITEM_SUPER_POTION) == 1 and pithosCount(S.ITEM_SUPER_POTION) == pithosSuper,
         "with a free slot, the gift goes to the Bag")
  expect(not said("Pithos") and said("pocket"), "and it says it went into the pocket")

  -- 4. Bag and Pithos both full: refused, nothing lost.
  fill(pocket(S.OFF_BAG_ITEMS), S.BAG_ITEMS_COUNT, S.ITEM_HONEY, true)
  local pithos = {}
  for i = 0, S.PC_ITEMS_COUNT - 1 do
    local slot = L.sb1() + S.OFF_SB1_PC_ITEMS + i * S.ITEM_SLOT_SIZE
    pithos[i] = { emu:read16(slot), emu:read16(slot + 2) }
  end
  local restorePithos = fill(L.sb1() + S.OFF_SB1_PC_ITEMS, S.PC_ITEMS_COUNT, S.ITEM_HONEY, false)
  run("BagOverflow_GiftHeader", "both_full")
  expect(L.getVar(S.VAR_0x8000) == 0 and bagCount(S.ITEM_SUPER_POTION) == 0 and pithosCount(S.ITEM_SUPER_POTION) == 0,
         "with the Bag and the Pithos both full, giveitem reports failure and adds nothing")
  restorePithos()

  -- 5. Save and CONTINUE.
  restoreSlot()
  L.runHeader("BagOverflow_SaveHeader")
  wait(300)
  emu:reset()
  L.continueSave()
  expect(emu:read32(L.sb1() + S.OFF_SB1_BAG_LAYOUT) == S.ICHOR_BAG_LAYOUT_MAGIC, "the layout magic survives a save")
  expect(pithosCount(S.ITEM_POTION) == before + 1 and pithosCount(S.ITEM_SUPER_POTION) == 1
         and pithosCount(S.ITEM_ETHER) == 1 and pithosCount(S.ITEM_ANTIDOTE) == antidotes + 1,
         "the Pithos keeps every overflowed item after CONTINUE")
  expect(bagCount(S.ITEM_HONEY) == (S.BAG_ITEMS_COUNT - 1) * S.MAX_BAG_ITEM_CAPACITY,
         "the big Items pocket keeps all its slots after CONTINUE")
end)
