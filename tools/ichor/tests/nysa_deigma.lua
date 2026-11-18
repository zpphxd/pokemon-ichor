-- The Nursery of Nysa (Route 7) and the Great Deigma (Emporion), played from a
-- Quickstart with the setup blob's party (tools/ichor/tests/nysa_deigma.sh).
--   1. Makris takes two Onotis; they roam the glade outside as overworld
--      Pokémon; under Hera's blessing every egg check finds an Egg (50% doubled),
--      without it some don't; Aristaios hands the Egg over; Makris returns one
--      for her fee.
--   2. In through the stoa's east door: three stalls sell, the curio stall's
--      stock holds for the day and changes on the next, Phormion buys coins.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
for k, v in pairs(dofile(L.OUT .. "extra_symbols.lua")) do
  if k == "SCRIPTS" then for n, a in pairs(v) do S.SCRIPTS[n] = a end else S[k] = v end
end

local N = "Route7_NurseryOfNysa_EventScript_"
local R7 = "Route7_KroniaGrounds_EventScript_"
local D = "EmporionCity_GreatDeigma_EventScript_"

local function partyCount()
  local n = 0
  for i = 0, 5 do if L.partySpecies(i) ~= 0 then n = n + 1 end end
  return n
end
local function daycareMon(i) return L.sb1() + S.OFF_SB1_DAYCARE + i * S.DAYCARE_MON_SIZE end
local function daycareHas(i) return (emu:read8(daycareMon(i) + S.OFF_BOXMON_FLAGS) >> 1) & 1 == 1 end
local function bless(god, steps)
  local b = L.ichor()
  emu:write8(b + S.OFF_ICHOR_BLESSING_GOD, god)
  emu:write16(b + S.OFF_ICHOR_BLESSING_STEPS, steps)
end

-- The PC-style chooser chooseboxmon opens: party button, then the slot.
local function chooseParty(slot, shot)
  L.waitUntil(function() return L.on("CB2_PokeStorage") end, 900, "the storage screen to choose a Pokémon")
  L.wait(90); if shot then L.shot(shot) end
  L.tap(K.UP); L.wait(20); L.tap(K.UP); L.wait(20)
  L.tap(K.A); L.wait(60)
  for _ = 1, slot do L.tap(K.DOWN); L.wait(20) end
  L.tap(K.A); L.wait(40)
  L.tap(K.A); L.wait(40)
  L.waitUntil(function() return not L.on("CB2_PokeStorage") end, 1200, "the storage screen to close")
end

-- Play a seller's lines into the shop, buy one of the first thing listed, leave.
local function buyFirst(script, item, shot)
  local before, money = L.itemCount(item), L.money()
  L.talk(L.npc(script), { noSettle = true })
  local t0 = L.now()
  while not L.taskRunning("Task_ShopMenu") do
    L.tap(K.A); L.wait(20)
    if L.now() - t0 > 1500 then L.fail(script .. ": the shop never opened") end
  end
  L.wait(20); L.tap(K.A)                                      -- BUY
  L.waitUntil(function() return L.taskRunning("Task_BuyMenu") end, 600, "the item list")
  L.wait(40); L.shot(shot)
  L.tap(K.A)                                                  -- the first item
  t0 = L.now()
  while L.itemCount(item) == before do
    if L.taskRunning("Task_HandleYesNoInput") then L.wait(10); L.tap(K.A); L.wait(20)
    else L.tap(K.A); L.wait(20) end
    if L.now() - t0 > 1500 then L.fail(script .. ": the purchase never went through") end
  end
  t0 = L.now()
  L.wait(30)
  while not L.taskRunning("Task_BuyMenu") do
    L.tap(K.A); L.wait(30)
    if L.now() - t0 > 900 then L.fail(script .. ": never back at the item list") end
  end
  L.wait(20); L.tap(K.B)
  L.waitUntil(function() return L.taskRunning("Task_ShopMenu") end, 600, "the shop menu again")
  L.wait(20); L.tap(K.B)                                      -- QUIT
  L.settle()
  L.expect(L.itemCount(item) == before + 1 and L.money() < money,
           string.format("%s sells one (%d -> %d, money %d -> %d)", script, before, L.itemCount(item), money, L.money()))
end

local function nursery()
  L.runHeader("NysaTest_SetupHeader")
  L.expect(L.mapId() == S.MAP_ROUTE7, "the setup starts on Route 7 at the nursery")
  L.expect(not L.npc(R7 .. "YardMon0").present and not L.npc(R7 .. "YardMon1").present,
           "the glade is empty before anything is left")
  L.shot("01_route7_nursery")
  L.useWarp(S.MAP_NURSERY)
  L.expect(L.mapId() == S.MAP_NURSERY, "the farmhouse door leads into the Nursery of Nysa")
  L.shot("02_nursery_inside")
  -- Makris: YES to raising one, the first Onotis (slot 1); YES to one more, the other
  L.talk(L.npc(N .. "Makris"), { noSettle = true, shotBefore = "03_makris" })
  L.settle({ stop = function() return L.on("CB2_PokeStorage") end })
  chooseParty(1, "04_choose_first")
  L.settle({ stop = function() return L.on("CB2_PokeStorage") end })
  chooseParty(1, "05_choose_second")
  L.settle({ every = true })
  L.expect(daycareHas(0) and daycareHas(1), "Makris holds two Pokémon")
  L.expect(partyCount() == 2, string.format("two are left in the party (%d)", partyCount()))
  -- out to the glade: both roam it, as themselves
  L.useWarp(S.MAP_ROUTE7)
  local g0, g1 = L.getVar(S.VAR_OBJ_GFX_ID_0), L.getVar(S.VAR_OBJ_GFX_ID_1)
  L.expect(g0 & 0x7FF == S.SPECIES_ONOTIS and g0 & S.OBJ_EVENT_MON ~= 0 and g1 & 0x7FF == S.SPECIES_ONOTIS,
           string.format("the yard's sprites are the two Onotis (%04X, %04X)", g0, g1))
  L.expect(g0 & S.OBJ_EVENT_MON_FEMALE == 0 and g1 & S.OBJ_EVENT_MON_FEMALE ~= 0,
           "the female keeps her female form")
  L.expect(L.npc(R7 .. "YardMon0").present and L.npc(R7 .. "YardMon1").present, "both roam the glade")
  L.go(37, 5); L.face(K.DOWN); L.wait(30)
  L.shot("06_glade_roamers")
  L.talk(L.npc(R7 .. "YardMon0"), { shots = { [1] = "07_yard_mon" } })
  L.go(37, 5)
  -- egg checks: steps of the second parent at 0xFE, so the next step is a check
  local function trial()
    emu:write32(daycareMon(1) + S.OFF_DAYCARE_MON_STEPS, 0xFE)
    L.setFlag(S.FLAG_PENDING_DAYCARE_EGG, false)
    local x = L.pos()
    L.step(x == 37 and K.LEFT or K.RIGHT)
    L.wait(4)
    return L.getFlag(S.FLAG_PENDING_DAYCARE_EGG)
  end
  bless(S.ICHOR_GOD_HERA, 900)
  local hera = 0
  for _ = 1, 8 do if trial() then hera = hera + 1 end end
  L.expect(hera == 8, string.format("under Hera's blessing every check finds an Egg (%d of 8)", hera))
  bless(0, 0)
  local plain = 0
  for _ = 1, 16 do if trial() then plain = plain + 1 end end
  L.expect(plain < 16, string.format("without it, some checks don't (%d of 16; the chance is 50%%)", plain))
  bless(S.ICHOR_GOD_HERA, 900)
  if not trial() then L.fail("no Egg waiting for Aristaios") end
  -- Aristaios: YES, and the Egg joins the party
  L.talk(L.npc(R7 .. "Aristaios"), { shots = { [1] = "08_aristaios", [2] = "09_egg" } })
  L.expect(partyCount() == 3 and not L.getFlag(S.FLAG_PENDING_DAYCARE_EGG),
           string.format("Aristaios gives the Egg (party %d)", partyCount()))
  -- Makris gives one back for her fee: YES to one back, the first on her list, YES to pay, NO to the other
  L.useWarp(S.MAP_NURSERY)
  local money = L.money()
  L.talk(L.npc(N .. "Makris"), { answers = { "yes", "yes", "no" }, every = true })
  L.expect(partyCount() == 4 and L.money() < money and not (daycareHas(0) and daycareHas(1)),
           string.format("Makris returns one for ¥%d", money - L.money()))
  L.shot("10_took_back")
end

local function deigma()
  L.runHeader("NysaTest_CityHeader")
  L.expect(L.mapId() == S.MAP_CITY, "in Emporion before the stoa")
  L.shot("11_stoa_doors")
  L.go(36, 37); L.step(K.UP)
  L.waitUntil(function() return L.mapId() == S.MAP_DEIGMA and L.idle() end, 900, "the Great Deigma")
  L.expect(L.mapId() == S.MAP_DEIGMA, "the stoa's east door opens on the Great Deigma")
  L.wait(30); L.shot("12_deigma_inside")
  local r0 = L.getVar(S.VAR_ICHOR_DEIGMA_RARE)
  L.expect(L.getFlag(S.FLAG_DAILY_ICHOR_DEIGMA_RARE) and r0 <= 5,
           string.format("the curio stall draws today's stock on entry (%d)", r0))
  buyFirst(D .. "Hiram", S.ITEM_NET_BALL, "13_hiram_wares")
  buyFirst(D .. "Petraios", S.ITEM_FIRE_STONE, "14_petraios_wares")
  buyFirst(D .. "Melia", S.ITEM_ORAN_BERRY, "15_melia_wares")
  buyFirst(D .. "Amasis", S.ITEM_FRANKINCENSE, "16_amasis_wares")
  L.talk(L.npc(D .. "Kallias"), { noSettle = true })
  local t0 = L.now()
  while not L.taskRunning("Task_BuyMenu") do
    L.tap(K.A); L.wait(20)
    if L.now() - t0 > 1500 then L.fail("the curio stall never opened") end
    if L.taskRunning("Task_ShopMenu") then L.wait(20); L.tap(K.A); L.wait(20) end
  end
  L.wait(40); L.shot("17_kallias_today")
  L.tap(K.B); L.waitUntil(function() return L.taskRunning("Task_ShopMenu") end, 600, "the shop menu")
  L.wait(20); L.tap(K.B); L.settle()
  -- the same day: the same stock; the next day: another
  L.useWarp(S.MAP_CITY)
  L.go(36, 37); L.step(K.UP)
  L.waitUntil(function() return L.mapId() == S.MAP_DEIGMA and L.idle() end, 900, "the Great Deigma again")
  L.expect(L.getVar(S.VAR_ICHOR_DEIGMA_RARE) == r0, "the curio stock holds for the rest of the day")
  local day = L.getVar(S.VAR_DAYS)
  L.runHeader("NysaTest_NextDayHeader")
  L.waitUntil(function() return L.getVar(S.VAR_DAYS) > day end, 9000, "the next day")
  L.wait(60)
  L.expect(not L.getFlag(S.FLAG_DAILY_ICHOR_DEIGMA_RARE), "the new day clears the draw")
  L.useWarp(S.MAP_CITY)
  L.go(36, 37); L.step(K.UP)
  L.waitUntil(function() return L.mapId() == S.MAP_DEIGMA and L.idle() end, 900, "the Great Deigma, next day")
  local r1 = L.getVar(S.VAR_ICHOR_DEIGMA_RARE)
  L.expect(r1 ~= r0 and r1 <= 5, string.format("the next day the curio stall has new stock (%d -> %d)", r0, r1))
  -- Phormion: an Obol, YES; the Stater, YES; then nothing more
  local money = L.money()
  local ob, st = L.itemCount(S.ITEM_RELIC_COPPER), L.itemCount(S.ITEM_RELIC_GOLD)
  L.talk(L.npc(D .. "Phormion"), { answers = { 0, "yes", 2, "yes", 3 }, every = true })
  L.expect(L.itemCount(S.ITEM_RELIC_COPPER) == ob - 1 and L.itemCount(S.ITEM_RELIC_GOLD) == st - 1,
           "Phormion buys an Obol and the Stater")
  L.expect(L.money() - money == 625 + 6250,
           string.format("at a quarter over the market's price (¥%d)", L.money() - money))
  L.shot("18_phormion")
end

L.start(function()
  L.quickstart()
  nursery()
  deigma()
end)
