-- Old-save compatibility for the big Bag, run by tools/ichor/tests/bag_save_compat.sh.
--
--   BAG_MODE  make    (old ROM) a new game, items in every pocket and the PC, a real save
--             dump    (old ROM) CONTINUE a save and print what it holds, without writing it
--             resave  (new ROM) CONTINUE an old save, print it, save in game, reset,
--                     CONTINUE again and print it again
--   SAVE_IN   the .sav (a copy; dump loads it read-only)
--   LAYOUT    old or new: where the Bag and the moved SaveBlock1 blocks are
--
-- Each print is a block of DUMP lines (pockets, the PC, and digests of the blocks
-- the migration moves) that the shell script compares between runs.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, emu = L.S, L.emu

-- The layout before the big Bag (src/item.c, the V6_ offsets).
local OLD = {
  bag = 0x560, pockets = { 30, 30, 16, 64, 46 }, pc = 0x498, pcCount = 50,
  dex = 13804, tail = 15120,
}
local DEX_SIZE, TAIL_SIZE = 312, 568

local function layout()
  if os.getenv("LAYOUT") == "old" then return OLD end
  return {
    bag = S.OFF_SB1_BAG,
    pockets = { S.BAG_ITEMS_COUNT, S.BAG_KEYITEMS_COUNT, S.BAG_POKEBALLS_COUNT, S.BAG_TMHM_COUNT, S.BAG_BERRIES_COUNT },
    pc = S.OFF_SB1_PC_ITEMS, pcCount = S.PC_ITEMS_COUNT,
    dex = S.OFF_SB1_DEX_SEEN, tail = S.OFF_SB1_RECORD_MIX,
  }
end

local function digest(addr, n)
  local h = 0
  for i = 0, n - 1, 4 do h = (h * 31 + emu:read32(addr + i)) & 0xFFFFFFFF end
  return string.format("%08x", h)
end

local function dump(tag)
  local lay, sb1 = layout(), L.sb1()
  local key = emu:read32(L.sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
  local names = { "items", "key", "balls", "tms", "berries" }
  local base, total = sb1 + lay.bag, 0
  for p, n in ipairs(lay.pockets) do
    local list = {}
    for i = 0, n - 1 do
      local slot = base + i * S.ITEM_SLOT_SIZE
      local id = emu:read16(slot)
      if id ~= 0 then list[#list + 1] = id .. "x" .. (emu:read16(slot + 2) ~ key); total = total + 1 end
    end
    L.log(string.format("DUMP %s %s %s", tag, names[p], table.concat(list, ",")))
    base = base + n * S.ITEM_SLOT_SIZE
  end
  local list = {}
  for i = 0, lay.pcCount - 1 do
    local slot = sb1 + lay.pc + i * S.ITEM_SLOT_SIZE
    local id = emu:read16(slot)
    if id ~= 0 then list[#list + 1] = id .. "x" .. emu:read16(slot + 2) end
  end
  L.log(string.format("DUMP %s pc %s", tag, table.concat(list, ",")))
  L.log(string.format("DUMP %s dex %s", tag, digest(sb1 + lay.dex, DEX_SIZE)))
  L.log(string.format("DUMP %s tail %s", tag, digest(sb1 + lay.tail, TAIL_SIZE)))
  L.log(string.format("DUMP %s flags %s", tag, digest(sb1 + S.OFF_SB1_FLAGS, 384)))
  L.log(string.format("DUMP %s money %d", tag, emu:read32(sb1 + S.OFF_SB1_MONEY) ~ emu:read32(L.sb2() + S.OFF_SB2_ENCRYPTION_KEY)))
  L.note(string.format("%s: %d bag stacks, %d PC stacks", tag, total, #list))
end

L.start(function()
  local mode, path = os.getenv("BAG_MODE"), os.getenv("SAVE_IN")
  if mode == "make" then
    L.expect(emu:loadSaveFile(path, false), "loaded the blank save " .. path)
    emu:reset()
    L.quickstart()
    -- An Ether in the old PC's second slot (a new game puts a Potion in the first).
    local slot = L.sb1() + OLD.pc + S.ITEM_SLOT_SIZE
    emu:write16(slot, S.ITEM_ETHER); emu:write16(slot + 2, 4)
    L.runHeader("BagOverflow_OldItemsHeader")
    L.wait(300)
    emu:reset()
    L.continueSave()
    dump("before")
  elseif mode == "dump" then
    L.expect(emu:loadSaveFile(path, true), "loaded " .. path .. " read-only")
    emu:reset()
    L.continueSave()
    dump("before")
  else
    L.expect(emu:loadSaveFile(path, false), "loaded " .. path)
    emu:reset()
    L.continueSave()
    L.expect(emu:read32(L.sb1() + S.OFF_SB1_BAG_LAYOUT) == S.ICHOR_BAG_LAYOUT_MAGIC, "the old save loads into the big Bag's layout")
    dump("migrated")
    L.runHeader("BagOverflow_SaveHeader")
    L.wait(300)
    emu:reset()
    L.continueSave()
    dump("resaved")
  end
end)
