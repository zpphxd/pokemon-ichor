local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, emu = L.S, L.emu
local sites = {
  { header = "Kronion", map = S.MAP_KRONION, index = 6, script = "KallisteRoute1_KronionHill_EventScript_DigShrine" },
  { header = "Terraces", map = S.MAP_TERRACES, index = 7, script = "KallisteRoute1_EventScript_DigTerraces" },
  { header = "Akti", map = S.MAP_AKTI, index = 8, script = "AktiTown_EventScript_DigBeach" },
}

local function visit(site)
  L.runHeader("KallisteDigs_" .. site.header .. "Header")
  L.expect(L.mapId() == site.map, "the actual " .. site.header .. " map")
end

local function sherds()
  local count = 0
  for i = 0, S.ICHOR_SHERDS_PER_AMPHORA - 1 do
    if L.getFlag(S.FLAG_KRONOS_SHERDS + i) then count = count + 1 end
  end
  return count
end

local function dig(site)
  L.talk(L.sign(site.script), { every = true })
end

local function withFind(site, kind, item, action)
  local savedSeed = emu:read32(L.sb1() + S.OFF_SB1_DAILY_SEED)
  for seed = 0, 4095 do
    emu:write32(L.sb1() + S.OFF_SB1_DAILY_SEED, seed)
    L.setVar(S.VAR_0x8004, site.index)
    L.setVar(S.VAR_0x8005, S.KRONOS_DIG_TABLE)
    L.runHeader("KallisteDigs_ProbeHeader")
    if L.getVar(S.VAR_TEMP_E) ~= S.ICHOR_DIG_READY then
      L.fail("the real dig probe is not ready at " .. site.header)
    end
    if L.getVar(S.VAR_RESULT) == kind and (not item or L.getVar(S.VAR_0x8006) == item) then
      action()
      emu:write32(L.sb1() + S.OFF_SB1_DAILY_SEED, savedSeed)
      return
    end
  end
  L.fail("no seed produced the requested real find at " .. site.header)
end

local function saveAndContinue()
  L.runHeader("KallisteDigs_SaveHeader")
  emu:reset()
  L.continueSave()
end

local function nextDay()
  local day, map = L.getVar(S.VAR_DAYS), L.mapId()
  L.runHeader("KallisteDigs_AdvanceHeader")
  L.waitUntil(function() return L.getVar(S.VAR_DAYS) > day end, 9000, "the actual field clock's next day")
  L.expect(L.mapId() == map and emu:read8(S.gLocalTime + S.OFF_TIME_HOURS) == 0,
           "midnight renews the digs without leaving the map")
end

local function fillItemPocket()
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
  L.quickstart()
  L.runHeader("KallisteDigs_SetupHeader")
  L.setVar(S.VAR_RESULT, 0x1234)
  L.expect(L.getVar(S.VAR_RESULT) == 0x1234 and emu:read16(S.gSpecialVar_Result) == 0x1234,
           "the variable helper addresses the real native result")
  L.expect(L.itemCount(S.ITEM_TROWEL) == 0, "the return starts without the Trowel")
  for _, site in ipairs(sites) do
    visit(site)
    dig(site)
    L.expect(not L.getFlag(S.FLAG_DIG_START + site.index) and sherds() == 0,
             site.header .. " hints at excavation without consuming its find")
  end
  L.runHeader("KallisteDigs_TrowelHeader")
  L.expect(L.itemCount(S.ITEM_TROWEL) == 1, "the actual Trowel is in the Bag")
  for n, site in ipairs(sites) do
    visit(site)
    withFind(site, S.ICHOR_FIND_KIND_SHERD, nil, function() dig(site) end)
    L.expect(L.getFlag(S.FLAG_DIG_START + site.index) and sherds() == n,
             site.header .. " gives one Kronos sherd and records its own daily index")
    for j = n + 1, #sites do
      L.expect(not L.getFlag(S.FLAG_DIG_START + sites[j].index), "later dig " .. sites[j].header .. " stays available")
    end
    dig(site)
    L.expect(sherds() == n, site.header .. " cannot give another same-day sherd")
  end
  saveAndContinue()
  L.expect(sherds() == 3, "the three collected sherds survive saving and CONTINUE")
  for _, site in ipairs(sites) do
    visit(site)
    dig(site)
    L.expect(L.getFlag(S.FLAG_DIG_START + site.index) and sherds() == 3,
             site.header .. " remains consumed after saving and revisiting")
  end
  nextDay()
  for _, site in ipairs(sites) do
    L.expect(not L.getFlag(S.FLAG_DIG_START + site.index), site.header .. " renews at midnight")
  end
  visit(sites[1])
  withFind(sites[1], S.ICHOR_FIND_KIND_SHERD, nil, function() dig(sites[1]) end)
  L.expect(sherds() == 4, "a later day's real dig completes the four-piece collection")
  L.expect(not L.getFlag(S.FLAG_KRONOS_AMPHORA), "four sherds do not falsely count as a restored amphora")
  for a = 1, S.ICHOR_AMPHORA_COUNT - 1 do
    for i = 0, S.ICHOR_SHERDS_PER_AMPHORA - 1 do
      L.expect(not L.getFlag(S.FLAG_KRONOS_SHERDS + a * S.ICHOR_SHERDS_PER_AMPHORA + i),
               "Kalliste cannot give amphora " .. a .. " sherd " .. i)
    end
  end

  visit(sites[2])
  withFind(sites[2], S.ICHOR_FIND_KIND_ITEM, S.ITEM_STARDUST, function()
    local restore = fillItemPocket()
    dig(sites[2])
    L.expect(not L.getFlag(S.FLAG_DIG_START + sites[2].index), "a full Bag leaves the terrace find in the ground")
    saveAndContinue()
    L.expect(not L.getFlag(S.FLAG_DIG_START + sites[2].index) and sherds() == 4,
             "the refused find and all four sherds survive CONTINUE")
    restore()
    local before = L.itemCount(S.ITEM_STARDUST)
    dig(sites[2])
    L.expect(L.getFlag(S.FLAG_DIG_START + sites[2].index) and L.itemCount(S.ITEM_STARDUST) == before + 1,
             "making room retrieves the same Stardust find, once")
    dig(sites[2])
    L.expect(L.itemCount(S.ITEM_STARDUST) == before + 1 and sherds() == 4, "the retried dig cannot duplicate any reward")
  end)
  visit(sites[3])
  withFind(sites[3], S.ICHOR_FIND_KIND_ITEM, nil, function() dig(sites[3]) end)
  L.expect(L.getFlag(S.FLAG_DIG_START + sites[3].index) and sherds() == 4,
           "a whole sherd collection leaves the beach's other loot usable")
end)
