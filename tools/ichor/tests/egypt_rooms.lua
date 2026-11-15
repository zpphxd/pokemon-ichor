-- Egypt's rooms check, run by tools/ichor/tests/egypt_rooms.sh (read it first).
--
-- Plays Naukratis's and Memphis's twelve rooms with key presses, from a
-- Quickstart. People and signs are found by the script they run, so a moved
-- person never breaks the check; a missing one fails with its name.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
for k, v in pairs(dofile(L.OUT .. "egypt_scripts.lua")) do S.SCRIPTS[k] = v end
local log, fail, wait, tap, shot = L.log, L.fail, L.wait, L.tap, L.shot
local expect = L.expect

-- --- Playing a script out ---------------------------------------------------------------

-- Press through whatever a talk starts until the player is free again. YES/NO
-- prompts and multichoice menus take their answers from opts.answers in order:
-- "yes"/"no" for a prompt, a number (how many steps down) for a menu. The
-- shop's menus are closed with B; the storage screen goes to opts.storage.
local function drive(opts)
  opts = opts or {}
  local answers, n = opts.answers or {}, 0
  local function nextAnswer(default)
    n = n + 1
    local a = answers[n]
    if a == nil then return default end
    return a
  end
  local t0, calm, boxes = L.now(), 0, 0
  while calm < 20 do
    if L.idle() then
      calm = calm + 1
      L.frame()
    else
      calm = 0
      if L.on("CB2_PokeStorage") then
        if not opts.storage then fail("a storage screen nobody expected") end
        opts.storage()
      elseif L.inBattle() then
        L.battle()
      elseif L.taskRunning("Task_BuyMenu") then
        tap(K.B); wait(20)
      elseif L.taskRunning("Task_ShopMenu") then
        wait(20); shot((opts.prefix or "shop") .. "_shop"); tap(K.B); wait(30)
      elseif L.taskRunning("Task_HandleYesNoInput") then
        wait(10)
        local a = nextAnswer("yes")
        if a == "no" then tap(K.DOWN) end
        tap(K.A)
        L.waitUntil(function() return not L.taskRunning("Task_HandleYesNoInput") end, 120, "the YES/NO to close")
      elseif L.taskRunning("Task_HandleMultichoiceInput") or L.taskRunning("Task_HandleScrollingMultichoiceInput") then
        wait(16)
        local a = nextAnswer(0)
        if type(a) ~= "number" then fail("a menu where a " .. tostring(a) .. " answer was expected") end
        if opts.prefix then shot(opts.prefix .. "_menu") end
        for _ = 1, a do tap(K.DOWN); wait(6) end
        tap(K.A)
        L.waitUntil(function() return not (L.taskRunning("Task_HandleMultichoiceInput")
                                           or L.taskRunning("Task_HandleScrollingMultichoiceInput")) end,
                    120, "the menu to close")
      elseif L.boxUp() or (L.inOverworld() and L.newText()) then
        wait(34)
        if not L.taskRunning("Task_HandleYesNoInput") then
          boxes = boxes + 1
          L.logText()
          if opts.prefix and boxes <= (opts.shots or 1) then shot(string.format("%s_%02d", opts.prefix, boxes)) end
          tap(K.A)
        end
        wait(4)
      else
        tap(K.A)
        wait(6)
      end
    end
    if L.now() - t0 > (opts.limit or 20000) then shot("stuck"); fail("stuck: " .. L.where()) end
  end
  return boxes
end

-- Walk to a person or sign (by script), face it, press A and drive the result.
local function talkTo(script, opts, nth)
  local target = S.SCRIPTS[script] and L.mapEvents() and nil
  local ok, t = pcall(L.npc, script, nth)
  if not ok then t = L.sign(script) end
  L.talk(t, { noSettle = true, shotBefore = opts and opts.shotBefore })
  return drive(opts)
end

-- The storage screen the day care and the trade open: from the jar up to YOUR
-- PARTY, open it, go down to party slot `slot`, then SELECT.
local function pickPartySlot(slot, prefix)
  return function()
    wait(90); shot(prefix .. "_storage")
    tap(K.UP); wait(20); tap(K.UP); wait(20)
    tap(K.A); wait(60)
    for _ = 1, slot do tap(K.DOWN); wait(20) end
    shot(prefix .. "_pick")
    tap(K.A); wait(40)
    tap(K.A); wait(40)
    L.waitUntil(function() return not L.on("CB2_PokeStorage") end, 1200, "the storage screen to close")
  end
end

-- --- Reading the room ----------------------------------------------------------------------

-- The current map's warps, with their warp ids.
local function warps()
  local ev = emu:read32(S.gMapHeader + S.OFF_MAPHEADER_EVENTS_E)
  local out = {}
  local n, base = emu:read8(ev + S.OFF_EVENTS_WARP_COUNT_E), emu:read32(ev + S.OFF_EVENTS_WARPS_E)
  for i = 0, n - 1 do
    local w = base + i * S.WARP_EVENT_SIZE_E
    out[#out + 1] = { x = emu:read16(w), y = emu:read16(w + 2), id = emu:read8(w + S.OFF_WARP_ID),
                      map = emu:read8(w + S.OFF_WARP_MAP_GROUP_E) * 256 + emu:read8(w + S.OFF_WARP_MAP_NUM_E) }
  end
  return out
end

local function party()
  L.runHeader("EgyptTest_PartyHeader", { noSettle = true })
  wait(4)
  return { L.getVar(S.VAR_0x8000), L.getVar(S.VAR_0x8001), L.getVar(S.VAR_0x8002), L.getVar(S.VAR_0x8003),
           size = L.getVar(S.VAR_0x8005) }
end
local function hasSpecies(sp)
  local p = party()
  for i = 1, 4 do if p[i] == sp then return i - 1 end end
  return nil
end
local function nickname(slot)
  local s = ""
  for i = 0, 9 do
    local b = emu:read8(L.partyMon(slot) + S.OFF_MON_NICKNAME_E + i)
    if b == 0xFF then break end
    if b >= 0xBB and b <= 0xD4 then s = s .. string.char(65 + b - 0xBB) else s = s .. "?" end
  end
  return s
end

-- Into a room by its door mat; check the mat leads back to the town's door.
local function enter(header, map, town, door, name)
  L.runHeader(header, { noSettle = true })
  L.waitUntil(function() return L.mapId() == map and L.idle() end, 4000, "the warp into " .. name)
  wait(30)
  L.setBeat(name, false)
  local ws = warps()
  expect(#ws == 2, string.format("%s: two door-mat warps (%d)", name, #ws))
  for _, w in ipairs(ws) do
    expect(w.map == town and w.id == door,
           string.format("%s: the mat at (%d,%d) leads to the town's warp %d (got map %d warp %d)",
                         name, w.x, w.y, door, w.map, w.id))
  end
  local x, y = L.pos()
  expect(ws[1].x == x and ws[1].y == y, string.format("%s: arrived on the door mat (%d,%d)", name, x, y))
  shot("room")
end

local N, M = S.MAP_NAUKRATIS, S.MAP_MEMPHIS

-- --- The rooms -------------------------------------------------------------------------------

local function naukratisAsclepeion()
  enter("EgyptTest_NAsclepeionHeader", S.MAP_N_ASCLEPEION, N, 0, "naukratis_asclepeion")
  emu:write16(L.partyMon(3) + S.OFF_MON_HP, 1)
  talkTo("Naukratis_Asclepeion_EventScript_Healer", { prefix = "healer", shots = 2 })
  local hp, maxHp = L.partyHp(3)
  expect(hp == maxHp, string.format("the Naukratis healer heals (%d/%d)", hp, maxHp))
  talkTo("Naukratis_Asclepeion_EventScript_Sailor", { prefix = "sailor" })
  talkTo("Naukratis_Asclepeion_EventScript_CatWoman", { prefix = "cat_woman" })
  talkTo("Naukratis_Asclepeion_EventScript_Espurr", { prefix = "espurr" })
  talkTo("Naukratis_Asclepeion_EventScript_Pithos", { prefix = "pithos", answers = { 2 } })
  talkTo("Naukratis_Asclepeion_EventScript_EarStele", { prefix = "ear_stele" })
  talkTo("Naukratis_Asclepeion_EventScript_Window", { prefix = "window" })
end

local function naukratisAgora()
  enter("EgyptTest_NAgoraHeader", S.MAP_N_AGORA, N, 1, "naukratis_agora")
  talkTo("Naukratis_Agora_EventScript_Stallkeeper", { prefix = "charaxos", shots = 2 })
  talkTo("Naukratis_Agora_EventScript_Trader", { prefix = "trader" })
  talkTo("Naukratis_Agora_EventScript_Porter", { prefix = "porter" })
  talkTo("Naukratis_Agora_EventScript_Amphorae", { prefix = "amphorae" })
end

local function fieldStation()
  enter("EgyptTest_NFieldStationHeader", S.MAP_N_FIELD_STATION, N, 2, "naukratis_field_station")
  local before = party().size
  -- the welcome, then "A fossil", YES to the Helix Fossil, NO to a nickname
  talkTo("Naukratis_FieldStation_EventScript_Daphne", { prefix = "daphne", shots = 8, answers = { 0, "yes", "no" } })
  expect(L.getFlag(S.FLAG_MET_DAPHNE_NAUKRATIS), "Daphne's welcome sets FLAG_ICHOR_MET_DAPHNE_NAUKRATIS")
  expect(L.itemCount(S.ITEM_HELIX_FOSSIL) == 0, "Daphne takes the Helix Fossil")
  local p = party()
  expect(p.size == before + 1 and hasSpecies(S.SPECIES_OMANYTE) ~= nil,
         string.format("the Helix Fossil wakes as an Omanyte (party %d -> %d)", before, p.size))
  -- again: no fossils left; then the Pokédex
  talkTo("Naukratis_FieldStation_EventScript_Daphne", { prefix = "daphne_none", answers = { 0 } })
  talkTo("Naukratis_FieldStation_EventScript_Daphne", { prefix = "daphne_dex", shots = 2, answers = { 1 } })
  talkTo("Naukratis_FieldStation_EventScript_Trough", { prefix = "trough" })
  talkTo("Naukratis_FieldStation_EventScript_Notes", { prefix = "notes" })
  talkTo("Naukratis_FieldStation_EventScript_Crates", { prefix = "crates" })
end

local function eggOvens()
  enter("EgyptTest_NEggOvensHeader", S.MAP_N_EGG_OVENS, N, 3, "naukratis_egg_ovens")
  talkTo("Naukratis_EggOvens_EventScript_Neferu", { prefix = "neferu" })
  -- Tiy: YES, the first Pidgey (slot 0); YES to another, the second (now slot 0)
  local picks = 0
  talkTo("Naukratis_EggOvens_EventScript_Tiy", { prefix = "tiy", shots = 3, answers = { "yes", "yes" },
    storage = function() picks = picks + 1; pickPartySlot(0, "tiy_" .. picks)() end })
  L.runHeader("EgyptTest_DaycareHeader", { noSettle = true })
  wait(4)
  expect(picks == 2 and L.getVar(S.VAR_0x8000) == S.DAYCARE_TWO_MONS,
         string.format("the egg-ovens hold two Pokémon (state %d, %d picks)", L.getVar(S.VAR_0x8000), picks))
  local p = party()
  expect(p[1] == S.SPECIES_SMEARGLE and p[2] == S.SPECIES_MACHAMP,
         "both Pidgey left the party; the Smeargle leads it now")
  talkTo("Naukratis_EggOvens_EventScript_Neferu", { prefix = "neferu_two", shots = 2 })
  talkTo("Naukratis_EggOvens_EventScript_Tiy", { prefix = "tiy_two", answers = { "no" } })
  L.runHeader("EgyptTest_DaycareHeader", { noSettle = true })
  wait(4)
  expect(L.getVar(S.VAR_0x8000) == S.DAYCARE_TWO_MONS, "saying NO to Tiy leaves both in the ovens")
  talkTo("Naukratis_EggOvens_EventScript_Oven", { prefix = "oven" })
end

local function incenseShop()
  enter("EgyptTest_NIncenseShopHeader", S.MAP_N_INCENSE_SHOP, N, 4, "naukratis_incense_shop")
  talkTo("Naukratis_IncenseShop_EventScript_Merchant", { prefix = "yadail", shots = 4 })
  talkTo("Naukratis_IncenseShop_EventScript_Customer", { prefix = "widow" })
  talkTo("Naukratis_IncenseShop_EventScript_Frankincense", { prefix = "frankincense" })
  talkTo("Naukratis_IncenseShop_EventScript_Myrrh", { prefix = "myrrh" })
end

local function pottersHouse()
  enter("EgyptTest_NPottersHouseHeader", S.MAP_N_POTTERS_HOUSE, N, 5, "naukratis_potters_house")
  expect(L.objectAt(S.LOCALID_POTTER_KECLEON) ~= nil and L.objectAt(S.LOCALID_POTTER_SMEARGLE) == nil,
         "the Kecleon sits among the pots before the trade; no Smeargle")
  talkTo("Naukratis_PottersHouse_EventScript_Kecleon", { prefix = "kecleon" })
  local slot = hasSpecies(S.SPECIES_SMEARGLE)
  expect(slot ~= nil, "a Smeargle in the party to trade")
  talkTo("Naukratis_PottersHouse_EventScript_Lykos", { prefix = "lykos", shots = 5, answers = { "yes" },
    storage = pickPartySlot(slot, "lykos"), limit = 30000 })
  expect(L.getFlag(S.FLAG_TRADED_KECLEON), "the trade sets FLAG_ICHOR_TRADED_KECLEON")
  expect(nickname(slot) == "POIKILOS", "the Smeargle's slot now holds POIKILOS (" .. nickname(slot) .. ")")
  expect(party()[slot + 1] == S.SPECIES_KECLEON, "POIKILOS is a Kecleon")
  expect(L.objectAt(S.LOCALID_POTTER_KECLEON) == nil and L.objectAt(S.LOCALID_POTTER_SMEARGLE) ~= nil,
         "after the trade the Smeargle sits where the Kecleon did")
  shot("after_trade")
  talkTo("Naukratis_PottersHouse_EventScript_Lykos", { prefix = "lykos_after" })
  talkTo("Naukratis_PottersHouse_EventScript_Smeargle", { prefix = "smeargle" })
  talkTo("Naukratis_PottersHouse_EventScript_Shelf", { prefix = "shelf" })
  talkTo("Naukratis_PottersHouse_EventScript_Kiln", { prefix = "kiln" })
  -- re-entry keeps it that way
  enter("EgyptTest_NPottersHouseHeader", S.MAP_N_POTTERS_HOUSE, N, 5, "naukratis_potters_house_again")
  expect(L.objectAt(S.LOCALID_POTTER_KECLEON) == nil and L.objectAt(S.LOCALID_POTTER_SMEARGLE) ~= nil,
         "on re-entry the Smeargle is still painting and the Kecleon is gone")
end

local function netLoft()
  enter("EgyptTest_NNetLoftHeader", S.MAP_N_NET_LOFT, N, 6, "naukratis_net_loft")
  local rods = L.itemCount(S.ITEM_SUPER_ROD)
  talkTo("Naukratis_NetLoft_EventScript_Ipy", { prefix = "ipy", shots = 3 })
  expect(L.getFlag(S.FLAG_NAUKRATIS_FISHER_GIFT) and L.getFlag(S.FLAG_SUPER_ROD_GIVEN)
         and L.itemCount(S.ITEM_SUPER_ROD) == rods + 1, "Ipy gives the Super Rod (the first port's net-loft)")
  talkTo("Naukratis_NetLoft_EventScript_Ipy", { prefix = "ipy_after" })
  expect(L.itemCount(S.ITEM_SUPER_ROD) == rods + 1 and L.itemCount(S.ITEM_BIG_PEARL) == 0,
         "Ipy's gift comes once")
  talkTo("Naukratis_NetLoft_EventScript_Merit", { prefix = "merit", shots = 4, answers = { "yes" } })
  expect(L.getFlag(S.FLAG_GOT_LINEN), "Merit sends a bolt of linen upriver (FLAG_ICHOR_GOT_LINEN)")
  talkTo("Naukratis_NetLoft_EventScript_Merit", { prefix = "merit_after" })
  talkTo("Naukratis_NetLoft_EventScript_Loom", { prefix = "loom" })
  talkTo("Naukratis_NetLoft_EventScript_Skiff", { prefix = "skiff" })
end

local function embalmerBefore()
  enter("EgyptTest_MEmbalmersHouseHeader", S.MAP_M_EMBALMERS_HOUSE, M, 4, "memphis_embalmers_house")
  talkTo("Memphis_EmbalmersHouse_EventScript_Khay", { prefix = "khay_before", shots = 3 })
  expect(not L.getFlag(S.FLAG_GOT_REAPER_CLOTH) and L.itemCount(S.ITEM_REAPER_CLOTH) == 0,
         "no Reaper Cloth without Merit's linen")
end

local function embalmer()
  enter("EgyptTest_MEmbalmersHouseHeader", S.MAP_M_EMBALMERS_HOUSE, M, 4, "memphis_embalmers_house_linen")
  talkTo("Memphis_EmbalmersHouse_EventScript_Khay", { prefix = "khay", shots = 4 })
  expect(L.getFlag(S.FLAG_GOT_REAPER_CLOTH) and L.itemCount(S.ITEM_REAPER_CLOTH) == 1,
         "Khay gives a Reaper Cloth for the linen")
  talkTo("Memphis_EmbalmersHouse_EventScript_Khay", { prefix = "khay_after" })
  expect(L.itemCount(S.ITEM_REAPER_CLOTH) == 1, "the Reaper Cloth comes once")
  talkTo("Memphis_EmbalmersHouse_EventScript_Bundle", { prefix = "bundle" })
  talkTo("Memphis_EmbalmersHouse_EventScript_Canopic", { prefix = "canopic" })
  talkTo("Memphis_EmbalmersHouse_EventScript_Anubis", { prefix = "anubis" })
  talkTo("Memphis_EmbalmersHouse_EventScript_Linen", { prefix = "linen" })
end

local function memphisAsclepeion()
  enter("EgyptTest_MAsclepeionHeader", S.MAP_M_ASCLEPEION, M, 0, "memphis_asclepeion")
  emu:write16(L.partyMon(1) + S.OFF_MON_HP, 1)
  talkTo("Memphis_Asclepeion_EventScript_Healer", { prefix = "healer", shots = 2 })
  local hp, maxHp = L.partyHp(1)
  expect(hp == maxHp, string.format("the Memphis healer heals (%d/%d)", hp, maxHp))
  talkTo("Memphis_Asclepeion_EventScript_Lector", { prefix = "lector" })
  talkTo("Memphis_Asclepeion_EventScript_Scribe", { prefix = "scribe" })
  talkTo("Memphis_Asclepeion_EventScript_Boy", { prefix = "boy" })
  talkTo("Memphis_Asclepeion_EventScript_Pithos", { prefix = "pithos", answers = { 2 } })
  talkTo("Memphis_Asclepeion_EventScript_Imhotep", { prefix = "imhotep" })
  talkTo("Memphis_Asclepeion_EventScript_EarStele", { prefix = "ear_stele" })
end

local function memphisAgora()
  enter("EgyptTest_MAgoraHeader", S.MAP_M_AGORA, M, 1, "memphis_agora")
  talkTo("Memphis_Agora_EventScript_Stallkeeper", { prefix = "senbi", shots = 2 })
  talkTo("Memphis_Agora_EventScript_LinenSeller", { prefix = "linen_seller" })
  talkTo("Memphis_Agora_EventScript_Girl", { prefix = "girl" })
  talkTo("Memphis_Agora_EventScript_Amulets", { prefix = "amulets" })
end

local function apisStable()
  enter("EgyptTest_MApisStableHeader", S.MAP_M_APIS_STABLE, M, 2, "memphis_apis_stable")
  talkTo("Memphis_ApisStable_EventScript_Keeper", { prefix = "pakhom", shots = 5 })
  talkTo("Memphis_ApisStable_EventScript_Herdsman", { prefix = "herdsman" })
  talkTo("Memphis_ApisStable_EventScript_Hesat", { prefix = "hesat" })
  talkTo("Memphis_ApisStable_EventScript_Window", { prefix = "window" })
  for _, b in ipairs({ "Bull1", "Bull4", "Bull5", "Bull6" }) do
    talkTo("Memphis_ApisStable_EventScript_" .. b, { prefix = b:lower(), shots = 2, answers = { "no" } })
  end
  -- a wrong guess: Pakhom says why, and nothing is given
  talkTo("Memphis_ApisStable_EventScript_Bull2", { prefix = "bull2_wrong", shots = 4, answers = { "yes" } })
  expect(not L.getFlag(S.FLAG_FOUND_APIS), "naming a false bull gives nothing")
  -- the true Apis: YES, then NO to a nickname
  talkTo("Memphis_ApisStable_EventScript_Bull3", { prefix = "apis", shots = 8, answers = { "yes", "no" } })
  expect(L.getFlag(S.FLAG_FOUND_APIS), "naming the true Apis sets FLAG_ICHOR_FOUND_APIS")
  expect(hasSpecies(S.SPECIES_TAUROS_PALDEA_COMBAT) ~= nil, "the Apis joins the party: a black Tauros")
  expect(L.objectAt(S.LOCALID_APIS_BULL_3) == nil, "the Apis's stall is empty")
  shot("after_apis")
  talkTo("Memphis_ApisStable_EventScript_Keeper", { prefix = "pakhom_after" })
  talkTo("Memphis_ApisStable_EventScript_Window", { prefix = "window_after" })
end

local function scribesHouse()
  enter("EgyptTest_MScribesHouseHeader", S.MAP_M_SCRIBES_HOUSE, M, 3, "memphis_scribes_house")
  -- a wrong answer to the first riddle ends the try
  talkTo("Memphis_ScribesHouse_EventScript_Scribe", { prefix = "amenemope_wrong", shots = 4, answers = { "yes", 0 } })
  expect(not L.getFlag(S.FLAG_GOT_TWISTED_SPOON), "a wrong answer gives nothing")
  -- owl (second), water (first), mouth (third)
  talkTo("Memphis_ScribesHouse_EventScript_Scribe", { prefix = "amenemope", shots = 10, answers = { "yes", 1, 0, 2 } })
  expect(L.getFlag(S.FLAG_GOT_TWISTED_SPOON) and L.itemCount(S.ITEM_TWISTED_SPOON) == 1,
         "the three riddles answered: a Twisted Spoon")
  talkTo("Memphis_ScribesHouse_EventScript_Scribe", { prefix = "amenemope_after" })
  expect(L.itemCount(S.ITEM_TWISTED_SPOON) == 1, "the Twisted Spoon comes once")
  talkTo("Memphis_ScribesHouse_EventScript_Apprentice", { prefix = "apprentice" })
  talkTo("Memphis_ScribesHouse_EventScript_Glyphs", { prefix = "glyphs" })
  talkTo("Memphis_ScribesHouse_EventScript_Ibis", { prefix = "ibis" })
  talkTo("Memphis_ScribesHouse_EventScript_Niches", { prefix = "niches" })
end

L.start(function()
  L.quickstart()
  L.runHeader("EgyptTest_SetupHeader", { noSettle = true })
  L.waitUntil(function() return L.mapId() == S.MAP_N_ASCLEPEION and L.idle() end, 4000, "the first room")
  wait(30)
  naukratisAsclepeion()
  naukratisAgora()
  fieldStation()
  eggOvens()
  incenseShop()
  pottersHouse()
  embalmerBefore()
  netLoft()
  memphisAsclepeion()
  memphisAgora()
  apisStable()
  scribesHouse()
  embalmer()
  log("ok every room played")
end)
