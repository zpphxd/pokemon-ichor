-- Excavation check, run by tools/ichor/tests/ichor_dig.sh (read it first).

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local log, expect, wait, shot, settle = L.log, L.expect, L.wait, L.shot, L.settle

local X, Y = 14, 22                   -- Route 1, below the fork herm
local DAILY, FIXED = S.FLAG_DAILY_ICHOR_DIG_START, S.FLAG_ICHOR_DIG_FIXED_START

local function digFind() return emu:read16(S.sDig + S.OFF_DIG_FIND) end
local function digQty() return emu:read8(S.sDig + S.OFF_DIG_QUANTITY) end
local function setSeed(v) emu:write32(L.sb1() + S.OFF_SB1_DAILY_SEED, v) end
local function give(item, n)
  L.setVar(S.VAR_0x8004, item); L.setVar(S.VAR_0x8005, n or 1)
  L.runHeader("DigTest_GiveHeader")
end
local function take(item, n)
  L.setVar(S.VAR_0x8004, item); L.setVar(S.VAR_0x8005, n or 1)
  L.runHeader("DigTest_TakeHeader")
end
local function dig(header, index, arg, name)
  L.setVar(S.VAR_0x8004, index); L.setVar(S.VAR_0x8005, arg)
  if name then
    L.runHeader(header, { noSettle = true })
    wait(24); shot(name .. "_pose")
    L.waitUntil(function() return L.boxUp() end, 600, "the dig's message")
    wait(40); shot(name)
  end
  if not name then L.runHeader(header) else settle() end
end
local function spot(index, arg, name) dig("DigTest_SpotHeader", index, arg, name) end
local function fixed(index, find, name) dig("DigTest_FixedHeader", index, find, name) end

local function describe(find)
  if find < S.ITEMS_COUNT then return string.format("item %d", find) end
  return string.format("find 0x%04X", find)
end

L.start(function()
  L.quickstart()
  L.setVar(S.VAR_0x8008, X); L.setVar(S.VAR_0x8009, Y)
  L.runHeader("DigTest_SetupHeader", { limit = 4000 })
  L.waitUntil(function() return L.mapId() == S.MAP_ROUTE1 and L.idle() end, 3000, "Route 1")
  wait(40)
  for i = 0, 47 do L.setFlag(S.FLAG_ICHOR_SHERDS_START + i, false) end
  for i = 0, 31 do L.setFlag(S.FLAG_ICHOR_OSTRAKA_START + i, false) end

  -- No Trowel: the earth is only turned
  spot(0, S.ICHOR_DIG_ACT_I | S.DIG_SHERDS_KRONOS, "no_trowel")
  expect(not L.getFlag(DAILY + 0), "without the Trowel, a dig spot stays undug")

  -- A daily spot: its find, then dug out for the day
  give(S.ITEM_ALETHEAS_TROWEL)
  setSeed(0x1234ABCD)
  spot(0, S.ICHOR_DIG_ACT_I | S.DIG_SHERDS_KRONOS, "daily")
  local find0, qty0 = digFind(), digQty()
  local function took(find, qty, n0)  -- an item, a Kronos sherd or the first ostrakon
    if find < S.ITEMS_COUNT then return L.itemCount(find) == n0 + qty end
    return L.getFlag(S.FLAG_ICHOR_SHERDS_START + S.ICHOR_AMPHORA_KRONOS * 4) or L.getFlag(S.FLAG_ICHOR_OSTRAKA_START)
  end
  local n0 = find0 < S.ITEMS_COUNT and L.itemCount(find0) - qty0 or 0
  expect(L.getFlag(DAILY + 0) and took(find0, qty0, n0),
         string.format("a daily spot digs up its find (%s x%d) and is dug out for the day", describe(find0), qty0))
  local after = find0 < S.ITEMS_COUNT and L.itemCount(find0) or -1
  spot(0, S.ICHOR_DIG_ACT_I | S.DIG_SHERDS_KRONOS)
  expect(L.getFlag(DAILY + 0) and (find0 >= S.ITEMS_COUNT or L.itemCount(find0) == after),
         "the same spot gives nothing more today")

  -- A reload gives the same find: undo the dig and dig again
  L.setFlag(DAILY + 0, false)
  if find0 < S.ITEMS_COUNT then take(find0, qty0) end
  for i = 0, 47 do L.setFlag(S.FLAG_ICHOR_SHERDS_START + i, false) end
  for i = 0, 31 do L.setFlag(S.FLAG_ICHOR_OSTRAKA_START + i, false) end
  spot(0, S.ICHOR_DIG_ACT_I | S.DIG_SHERDS_KRONOS)
  expect(digFind() == find0, string.format("digging again on the same day finds the same thing (%s, %s)",
         describe(find0), describe(digFind())))

  -- A few more spots: every find is an Act I item, a Kronos sherd or an ostrakon
  local ok, seen = true, {}
  for s = 1, 6 do
    spot(s, S.ICHOR_DIG_ACT_I | S.DIG_SHERDS_KRONOS)
    local f = digFind()
    seen[#seen + 1] = describe(f)
    if not L.getFlag(DAILY + s) then ok = false end
    if f >= S.ITEMS_COUNT and f ~= S.FIND_SHERD_ARACHNE - S.ICHOR_AMPHORA_ARACHNE + S.ICHOR_AMPHORA_KRONOS
       and f ~= S.ICHOR_FIND_OSTRAKON then ok = false end
  end
  expect(ok, "six more spots each dig once, with Act I's finds: " .. table.concat(seen, ", "))

  -- Fixed finds: an item once, then bare
  local bones = L.itemCount(S.ITEM_RARE_BONE)
  fixed(0, S.ITEM_RARE_BONE, "fixed_item")
  expect(L.getFlag(FIXED + 0) and L.itemCount(S.ITEM_RARE_BONE) == bones + 1, "a fixed find gives its item")
  fixed(0, S.ITEM_RARE_BONE, "fixed_bare")
  expect(L.itemCount(S.ITEM_RARE_BONE) == bones + 1, "... and is bare afterwards")

  -- Sherds, a prophecy tablet, a page and an ostrakon
  local arachne = S.FLAG_ICHOR_SHERDS_START + S.ICHOR_AMPHORA_ARACHNE * 4
  fixed(1, S.FIND_SHERD_ARACHNE, "sherd")
  fixed(2, S.FIND_SHERD_ARACHNE)
  expect(L.getFlag(arachne) and L.getFlag(arachne + 1) and not L.getFlag(arachne + 2),
         "two fixed sherds give the Arachne amphora's first two pieces")
  fixed(3, S.FIND_PROPHECY_3, "tablet")
  expect(L.getFlag(S.FLAG_ICHOR_PROPHECY_START + 2), "prophecy tablet 3 sets FLAG_ICHOR_PROPHECY_START + 2")
  fixed(4, S.FIND_PAGE_4, "page")
  expect(L.getFlag(S.FLAG_ICHOR_PAGES_START + 3), "Daedalus's page IV sets FLAG_ICHOR_PAGES_START + 3")
  local ostraka = 0
  for i = 0, 29 do if L.getFlag(S.FLAG_ICHOR_OSTRAKA_START + i) then ostraka = ostraka + 1 end end
  fixed(5, S.ICHOR_FIND_OSTRAKON, "ostrakon")
  expect(L.getFlag(S.FLAG_ICHOR_OSTRAKA_START + ostraka), string.format("the next ostrakon (%d) is found", ostraka + 1))

  -- A call: the map's script goes on, and VAR_RESULT says whether it dug
  L.setVar(S.VAR_0x8004, 6); L.setVar(S.VAR_0x8005, S.ITEM_PEARL)
  L.runHeader("DigTest_CallHeader")
  expect(L.getVar(S.VAR_0x8009) == 1 and L.getFlag(FIXED + 6), "a called dig returns TRUE and the script goes on")
  L.setVar(S.VAR_0x8004, 6); L.setVar(S.VAR_0x8005, S.ITEM_PEARL)
  L.runHeader("DigTest_CallHeader")
  expect(L.getVar(S.VAR_0x8009) == 0, "a called dig of a bare spot returns FALSE")

  -- A dig-spot object shows until its dig: give a Route 1 object the find's flag
  local victim
  for i, o in ipairs(L.mapEvents().objects) do
    if L.objectAt(o.localId) then victim = { slot = i - 1, localId = o.localId }; break end
  end
  if victim then
    local t = L.sb1() + S.OFF_SB1_OBJ_TEMPLATES + victim.slot * S.OBJECT_TEMPLATE_SIZE
    emu:write16(t + S.OFF_TEMPLATE_FLAG, FIXED + 9)
    fixed(9, S.ITEM_PEARL)
    expect(L.objectAt(victim.localId) == nil and L.getFlag(FIXED + 9),
           string.format("digging removes the object hidden by the find's flag (local id %d)", victim.localId))
  else
    expect(false, "Route 1 has an object to stand in for a dig-spot object")
  end

  -- Hades's blessing doubles an item find
  local b = L.ichor() + S.OFF_ICHOR_BLESSING
  emu:write8(b, S.ICHOR_GOD_HADES); emu:write16(b + 2, 500)
  local doubled
  for s = 10, 40 do
    spot(s, S.ICHOR_DIG_ACT_I)
    if digFind() < S.ITEMS_COUNT then doubled = digQty(); break end
  end
  expect(doubled == 2, string.format("under Hades's blessing an item comes up twice (x%s)", tostring(doubled)))
  emu:write8(b, 0); emu:write16(b + 2, 0)

end)
