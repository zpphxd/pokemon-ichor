-- The Troad's rooms check, run by tools/ichor/tests/troad_rooms.sh (read it first).
--
-- Every room of Sestos and Ilion, entered through its door mat: the mat is warp 0
-- and names its town's warp with the room's number; every household is talked
-- to; every gift is taken once and a second talk gives nothing more; both trades
-- are made; Hero's windy stair is climbed (a draught puts the flame out, the next
-- climb lights the lamp); Odysseus gives the Xenion and is battled, then found at
-- the temple. People, signs and triggers are found by the script they run, never
-- by coordinates, so re-dressing a room never breaks this.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local extra = dofile(L.OUT .. "troad_symbols.lua")
for k, v in pairs(extra.SCRIPTS) do S.SCRIPTS[k] = v end
for k, v in pairs(extra) do if k ~= "SCRIPTS" then S[k] = v end end
local log, expect, wait, shot, tap, settle = L.log, L.expect, L.wait, L.shot, L.tap, L.settle

local function s16(v) if v >= 0x8000 then return v - 0x10000 end return v end
local function npc(script) return L.npc(script) end
local function sign(script) return L.sign(script) end
local function talk(target, opts) return L.talk(target, opts) end

-- --- Rooms ------------------------------------------------------------------------------

-- Warp in through the door mat, and check the mat: warp 0, the room's only
-- exit, naming its town's warp with the room's number (BUILD.md §5).
local function enter(name, map, town, warpId)
  L.runHeader("TroadTest_" .. name .. "Header", { limit = 4000 })
  L.waitUntil(function() return L.mapId() == map and L.idle() end, 4000, name)
  wait(30)
  local ev = emu:read32(S.gMapHeader + S.OFF_MAPHEADER_EVENTS)
  local w = emu:read32(ev + S.OFF_EVENTS_WARPS)
  local wx, wy = s16(emu:read16(w)), s16(emu:read16(w + 2))
  local dest = emu:read8(w + S.OFF_WARP_MAP_GROUP) * 256 + emu:read8(w + S.OFF_WARP_MAP_NUM)
  local id = emu:read8(w + S.OFF_WARP_ID)
  local x, y = L.pos()
  expect(x == wx and y == wy, string.format("%s: arrived on the door mat, warp 0 at (%d,%d)", name, wx, wy))
  expect(emu:read8(ev + S.OFF_EVENTS_WARP_COUNT) == 1 and dest == town and id == warpId,
         string.format("%s: warp 0 is its only exit and leads to its town's warp %d (got %d)", name, warpId, id))
  shot(name)
end

-- Talk to someone and check a gift: `count` of `item` after the first talk, and
-- the same after a second.
local function gift(who, item, count, flag, what)
  local before = L.itemCount(item)
  talk(npc(who))
  expect(L.itemCount(item) == before + count and L.getFlag(flag),
         string.format("%s: %d given, and its flag set (%d -> %d)", what, count, before, L.itemCount(item)))
  talk(npc(who))
  expect(L.itemCount(item) == before + count, what .. ": a second talk gives nothing more")
end

-- --- The party --------------------------------------------------------------------------

local function mon(slot) return S.gParties + slot * S.POKEMON_SIZE end
local function swap(a, b)
  for o = 0, S.POKEMON_SIZE - 4, 4 do
    local va, vb = emu:read32(mon(a) + o), emu:read32(mon(b) + o)
    emu:write32(mon(a) + o, vb); emu:write32(mon(b) + o, va)
  end
end
-- A party Pokémon's nickname, decoded from the game's charset (letters only),
-- in capitals.
local function nickname(slot)
  local s = ""
  for i = 0, 9 do
    local b = emu:read8(mon(slot) + S.OFF_MON_NICKNAME + i)
    if b == 0xFF then break end
    if b >= 0xBB and b <= 0xD4 then s = s .. string.char(65 + b - 0xBB)
    elseif b >= 0xD5 and b <= 0xEE then s = s .. string.char(65 + b - 0xD5)
    else s = s .. "?" end
  end
  return s
end

-- The box screen of an in-game trade: up past the jar's name to YOUR PARTY,
-- open it, the first Pokémon, SELECT (aegina_homes.lua's path).
local function pickFirst()
  wait(90); shot("trade_choose")
  tap(K.UP); wait(20); tap(K.UP); wait(20)
  tap(K.A); wait(60)
  tap(K.A); wait(40)
  tap(K.A); wait(40)
  L.waitUntil(function() return not L.on("CB2_PokeStorage") end, 1200, "the box screen to close")
end

-- Odysseus's battle, made short: every frame his Pokémon are put at 1 HP (his
-- Full Restores included), and the Mewtwo leads with its first move.
local function ctrl(name) return emu:read32(S.gBattlerControllerFuncs) == (S[name] | 1) end
local shotBattle = false
local function battleStep()
  local enemy = S.gParties + S.B_TRAINER_OPPONENT_A * S.PARTY_SIZE * S.POKEMON_SIZE
  for i = 0, S.PARTY_SIZE - 1 do
    if emu:read16(enemy + i * S.POKEMON_SIZE + S.OFF_MON_HP) > 1 then
      emu:write16(enemy + i * S.POKEMON_SIZE + S.OFF_MON_HP, 1)
    end
  end
  local bm = S.gBattleMons + S.BATTLE_MON_SIZE + S.OFF_BATTLE_MON_HP
  if emu:read16(bm) > 1 then emu:write16(bm, 1) end
  if ctrl("HandleInputChooseAction") then
    if not shotBattle then shot("odysseus_battle"); shotBattle = true end
    tap(K.UP); tap(K.LEFT); tap(K.A)
  elseif ctrl("HandleInputChooseMove") then
    tap(K.UP); tap(K.LEFT); tap(K.A)
  else
    tap(K.A)
  end
  wait(4)
end

-- --- The checks -------------------------------------------------------------------------

local function sestos()
  enter("SestosAsclepeion", S.MAP_SESTOS_ASCLEPEION, S.MAP_SESTOS, 0)
  emu:write16(mon(0) + S.OFF_MON_HP, 1)
  talk(npc("Sestos_Asclepeion_EventScript_Healer"))
  local hp, max = L.partyHp(0)
  expect(hp == max, string.format("Sestos Asclepeion: the healer heals the party (%d/%d)", hp, max))
  talk(npc("Sestos_Asclepeion_EventScript_OldWoman"))
  talk(npc("Sestos_Asclepeion_EventScript_Sailor"))
  talk(sign("Sestos_Asclepeion_EventScript_Window"))

  enter("SestosAgora", S.MAP_SESTOS_AGORA, S.MAP_SESTOS, 1)
  talk(npc("Sestos_Agora_EventScript_Chandler"), { noSettle = true })
  local t0 = L.now()
  while not L.taskRunning("Task_ShopMenu") do
    tap(K.A); wait(30)
    if L.now() - t0 > 900 then L.fail("the chandler's shop never opened") end
  end
  wait(20); tap(K.A)
  L.waitUntil(function() return L.taskRunning("Task_BuyMenu") end, 600, "the chandler's list")
  wait(40); shot("sestos_agora_stock")
  tap(K.B)
  L.waitUntil(function() return L.taskRunning("Task_ShopMenu") end, 600, "the shop menu again")
  wait(20); tap(K.B); wait(40)
  settle()
  expect(true, "Sestos Agora: the chandler's late-game stock opens")
  talk(npc("Sestos_Agora_EventScript_Sailor"))

  -- Hero's tower. After dusk, Hero has carried the flame herself; by day it's yours.
  enter("SestosHerosTower", S.MAP_SESTOS_HEROS_TOWER, S.MAP_SESTOS, 2)
  emu:write8(S.sHoursOverride, 21)
  talk(sign("Sestos_HerosTower_EventScript_Hearth"))
  expect(L.getVar(S.VAR_TEMP_3) == 0, "Hero's tower: after dusk the hearth gives no flame")
  talk(npc("Sestos_HerosTower_EventScript_Hero"), { every = true })
  emu:write8(S.sHoursOverride, 12)
  talk(npc("Sestos_HerosTower_EventScript_Hero"))
  talk(sign("Sestos_HerosTower_EventScript_Hearth"))
  expect(L.getVar(S.VAR_TEMP_3) == 1, "Hero's tower: by day the hearth gives a flame")
  shot("heros_tower_flame")
  -- the lower landing's draught, on purpose
  local draught = L.triggers("Sestos_HerosTower_EventScript_Draught")
  local dx, dy
  for k in pairs(draught) do
    local x, y = k:match("(%d+),(%d+)")
    x, y = tonumber(x), tonumber(y)
    if not dy or y > dy then dx, dy = x, y end
  end
  L.go(dx, dy + 1)
  L.step(K.UP)
  settle()
  expect(L.getVar(S.VAR_TEMP_3) == 0, string.format("Hero's tower: the draught at (%d,%d) puts the flame out", dx, dy))
  talk(sign("Sestos_HerosTower_EventScript_Hearth"))
  expect(L.getVar(S.VAR_TEMP_3) == 1, "Hero's tower: a second flame")
  local fire = L.itemCount(S.ITEM_FIRE_STONE)
  talk(sign("Sestos_HerosTower_EventScript_Lamp"), { avoid = draught })
  expect(L.getFlag(S.FLAG_HERO_FIRE_STONE) and L.itemCount(S.ITEM_FIRE_STONE) == fire + 1,
         "Hero's tower: the flame climbs the windy stair, the lamp is lit, and Hero gives a Fire Stone")
  shot("heros_tower_lit")
  talk(npc("Sestos_HerosTower_EventScript_Hero"))
  talk(sign("Sestos_HerosTower_EventScript_Lamp"))
  expect(L.itemCount(S.ITEM_FIRE_STONE) == fire + 1, "Hero's tower: no second Fire Stone")

  -- The ferry house: Kymon's Cramorant for the Pelipper in the first slot.
  enter("SestosFerryHouse", S.MAP_SESTOS_FERRY_HOUSE, S.MAP_SESTOS, 3)
  expect(L.objectAt(S.LOCALID_SESTOS_CRAMORANT) and not L.objectAt(S.LOCALID_SESTOS_PELIPPER),
         "the ferry house: Aithyia by the fire before the trade")
  talk(npc("Sestos_FerryHouse_EventScript_Cramorant"))
  talk(npc("Sestos_FerryHouse_EventScript_Kymon"), { hooks = { CB2_PokeStorage = pickFirst } })
  expect(L.getFlag(S.FLAG_TRADED_KYMON_CRAMORANT) and nickname(0) == "AITHYIA",
         "the ferry house: Kymon's trade, Pelipper for AITHYIA (" .. nickname(0) .. ")")
  talk(npc("Sestos_FerryHouse_EventScript_Kymon"))
  talk(sign("Sestos_FerryHouse_EventScript_Wreath"))
  enter("SestosFerryHouse", S.MAP_SESTOS_FERRY_HOUSE, S.MAP_SESTOS, 3)
  expect(not L.objectAt(S.LOCALID_SESTOS_CRAMORANT) and L.objectAt(S.LOCALID_SESTOS_PELIPPER),
         "the ferry house: the Pelipper by the fire after it")
  talk(npc("Sestos_FerryHouse_EventScript_Pelipper"))

  enter("SestosNetLoft", S.MAP_SESTOS_NET_LOFT, S.MAP_SESTOS, 4)
  gift("Sestos_NetLoft_EventScript_Fisher", S.ITEM_SUPER_ROD, 1, S.FLAG_SESTOS_FISHER_GIFT,
       "the net-loft: the first port's Super Rod")
  expect(L.getFlag(S.FLAG_SUPER_ROD_GIVEN), "the net-loft: the shared Super Rod flag is set")
  talk(sign("Sestos_NetLoft_EventScript_Rack"))
end

local function ilion()
  enter("IlionAsclepeion", S.MAP_ILION_ASCLEPEION, S.MAP_ILION, 0)
  emu:write16(mon(0) + S.OFF_MON_HP, 1)
  talk(npc("Ilion_Asclepeion_EventScript_Healer"))
  local hp, max = L.partyHp(0)
  expect(hp == max, string.format("Ilion Asclepeion: the healer heals the party (%d/%d)", hp, max))
  talk(npc("Ilion_Asclepeion_EventScript_Charioteer"))
  talk(npc("Ilion_Asclepeion_EventScript_Pilgrim"))

  enter("IlionAgora", S.MAP_ILION_AGORA, S.MAP_ILION, 1)
  talk(npc("Ilion_Agora_EventScript_Thymbra"), { noSettle = true })
  local t0 = L.now()
  while not L.taskRunning("Task_ShopMenu") do
    tap(K.A); wait(30)
    if L.now() - t0 > 900 then L.fail("Thymbra's shop never opened") end
  end
  wait(20); tap(K.A)
  L.waitUntil(function() return L.taskRunning("Task_BuyMenu") end, 600, "Thymbra's list")
  wait(40); shot("ilion_agora_stock")
  tap(K.B)
  L.waitUntil(function() return L.taskRunning("Task_ShopMenu") end, 600, "the shop menu again")
  wait(20); tap(K.B); wait(40)
  settle()
  expect(true, "Ilion Agora: Thymbra's late-game stock opens")
  talk(npc("Ilion_Agora_EventScript_HorseTrader"))
  talk(npc("Ilion_Agora_EventScript_ClothBuyer"))
  talk(sign("Ilion_Agora_EventScript_Bridles"))

  enter("IlionPriamsPalace", S.MAP_ILION_PRIAMS_PALACE, S.MAP_ILION, 2)
  gift("Ilion_PriamsPalace_EventScript_Priam", S.ITEM_SOOTHE_BELL_E, 1, S.FLAG_PRIAM_SOOTHE_BELL,
       "Priam's palace: the Soothe Bell, after the Gate Emblem")
  talk(npc("Ilion_PriamsPalace_EventScript_GuardWest"))
  talk(npc("Ilion_PriamsPalace_EventScript_GuardEast"))
  talk(npc("Ilion_PriamsPalace_EventScript_Steward"))
  talk(sign("Ilion_PriamsPalace_EventScript_Hearth"))

  enter("IlionCassandrasRoom", S.MAP_ILION_CASSANDRAS_ROOM, S.MAP_ILION, 3)
  gift("Ilion_CassandrasRoom_EventScript_Cassandra", S.ITEM_BOTTLE_CAP, 3, S.FLAG_CASSANDRA_LAURELS,
       "Cassandra's room: three wrong predictions, three Pythian Laurels")
  talk(sign("Ilion_CassandrasRoom_EventScript_Painting"))

  -- The guest-room: the Xenion, then the battle, with the Mewtwo leading.
  enter("IlionGuestRoom", S.MAP_ILION_GUEST_ROOM, S.MAP_ILION, 4)
  swap(0, 1)
  local xen = L.itemCount(S.ITEM_XENION)
  talk(npc("Ilion_GuestRoom_EventScript_Odysseus"), { hooks = { BattleMainCB2 = battleStep }, limit = 60000 })
  expect(L.getFlag(S.FLAG_ODYSSEUS_XENION) and L.itemCount(S.ITEM_XENION) == xen + 1,
         "the guest-room: Odysseus gives the Xenion")
  expect(L.defeated(S.TRAINER_ODYSSEUS), "the guest-room: Odysseus is battled and beaten")
  talk(npc("Ilion_GuestRoom_EventScript_Odysseus"))
  expect(L.itemCount(S.ITEM_XENION) == xen + 1 and L.inOverworld(), "the guest-room: no second Xenion, no second battle")
  talk(npc("Ilion_GuestRoom_EventScript_Host"))
  talk(sign("Ilion_GuestRoom_EventScript_WoodenHorse"))
  enter("IlionGuestRoom", S.MAP_ILION_GUEST_ROOM, S.MAP_ILION, 4)
  expect(not L.objectAt(S.LOCALID_ILION_ODYSSEUS), "the guest-room: Odysseus has gone up to the temple")

  -- The stable: a Mudsdale, moved to the first slot, for Aithon.
  enter("IlionHorseStable", S.MAP_ILION_HORSE_STABLE, S.MAP_ILION, 5)
  L.runHeader("TroadTest_GiveMudsdaleHeader")
  swap(0, 2)
  expect(L.objectAt(S.LOCALID_ILION_RAPIDASH) and not L.objectAt(S.LOCALID_ILION_MUDSDALE),
         "the stable: Aithon in the first stall before the trade")
  talk(npc("Ilion_HorseStable_EventScript_Rapidash"))
  talk(npc("Ilion_HorseStable_EventScript_Ponyta"))
  talk(npc("Ilion_HorseStable_EventScript_Idaios"), { hooks = { CB2_PokeStorage = pickFirst } })
  expect(L.getFlag(S.FLAG_TRADED_IDAIOS_RAPIDASH) and nickname(0) == "AITHON",
         "the stable: Idaios's trade, Mudsdale for AITHON (" .. nickname(0) .. ")")
  talk(npc("Ilion_HorseStable_EventScript_Idaios"))
  enter("IlionHorseStable", S.MAP_ILION_HORSE_STABLE, S.MAP_ILION, 5)
  expect(not L.objectAt(S.LOCALID_ILION_RAPIDASH) and L.objectAt(S.LOCALID_ILION_MUDSDALE),
         "the stable: your Mudsdale in the third stall after it")
  talk(npc("Ilion_HorseStable_EventScript_Mudsdale"))
  talk(sign("Ilion_HorseStable_EventScript_Trough"))

  enter("IlionMasonsHouse", S.MAP_ILION_MASONS_HOUSE, S.MAP_ILION, 6)
  talk(npc("Ilion_MasonsHouse_EventScript_Kallia"))
  gift("Ilion_MasonsHouse_EventScript_Laodokos", S.ITEM_HARD_STONE_E, 1, S.FLAG_MASON_CHISEL_RETURNED,
       "the mason's house: the chisel back, Hard Stone")
  talk(sign("Ilion_MasonsHouse_EventScript_ToolRack"))

  enter("IlionWeaversHouse", S.MAP_ILION_WEAVERS_HOUSE, S.MAP_ILION, 7)
  gift("Ilion_WeaversHouse_EventScript_Theano", S.ITEM_SILK_SCARF, 1, S.FLAG_WEAVER_SILK_SCARF,
       "the weaver's: three berries for dye, a Silk Scarf")
  expect(L.itemCount(S.ITEM_CHERI_BERRY) == 0 and L.itemCount(S.ITEM_ORAN_BERRY_E) == 0
         and L.itemCount(S.ITEM_ASPEAR_BERRY) == 0, "the weaver's: the berries went into the pots")
  talk(npc("Ilion_WeaversHouse_EventScript_Leavanny"))
  talk(sign("Ilion_WeaversHouse_EventScript_DyePots"))

  enter("IlionTempleOfAthena", S.MAP_ILION_TEMPLE_OF_ATHENA, S.MAP_ILION, 8)
  expect(L.objectAt(S.LOCALID_ILION_TEMPLE_ODYSSEUS), "the temple: Odysseus before the Palladion, after his battle")
  talk(npc("Ilion_TempleOfAthena_EventScript_Odysseus"))
  talk(npc("Ilion_TempleOfAthena_EventScript_Keeper"))
  talk(npc("Ilion_TempleOfAthena_EventScript_Worshipper"))
  talk(sign("Ilion_TempleOfAthena_EventScript_Palladion"))
end

L.start(function()
  L.quickstart()
  L.runHeader("TroadTest_SetupHeader", { limit = 4000 })
  expect(nickname(0) == "PELIPPER", "setup: a Pelipper leads the party (" .. nickname(0) .. ")")
  sestos()
  ilion()
end)
