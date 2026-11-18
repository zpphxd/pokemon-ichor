-- Eleusa's six interiors, run by tools/ichor/tests/eleusa_rooms.sh (read it first).
--
-- Plays each room's events as a player would, with key presses, as
-- emporion_rooms.lua does Emporion's, but on engine_lib.lua's walker (eleusa.lua's):
-- every room is entered by walking through its door in the village, and left by
-- its mat, and the walk checks it comes out on that door's tile. People, signs
-- and hidden items are found by the script they run or the flag they set, so a
-- moved NPC never breaks the walk; a missing one fails with its name.
--
-- Prints "ELEUSA_ROOMS ok ..." per check and "ELEUSA_ROOMS shot ..." per
-- screenshot, and ends with "ELEUSA_ROOMS done"; any failure prints
-- "ELEUSA_ROOMS FAIL: ..." first.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
for k, v in pairs(dofile(L.OUT .. "eleusa_rooms_symbols.lua")) do S[k] = v end

local A = "EleusaVillage_Asclepeion_EventScript_"
local G = "EleusaVillage_Agora_EventScript_"
local KE = "EleusaVillage_HouseOfKeleos_EventScript_"
local F = "EleusaVillage_Farmhouse_EventScript_"
local R = "EleusaVillage_GranaryHouse_EventScript_"
local P = "EleusaVillage_PoetsHouse_EventScript_"

local function expect(cond, what) L.expect(cond, what) end

-- Each room: its village door (the first cell of a barn door) and the mat it
-- arrives on (the room's warp 0).
local ROOMS = {
  asclepeion = { map = "MAP_E_ASCLEPEION", door = { 10, 23 }, mat = { 9, 9 } },
  agora      = { map = "MAP_E_AGORA",      door = { 17, 23 }, mat = { 4, 7 } },
  keleos     = { map = "MAP_E_KELEOS",     door = { 38, 23 }, mat = { 7, 9 } },
  granary    = { map = "MAP_E_GRANARY",    door = { 15, 17 }, mat = { 4, 8 } },
  poets      = { map = "MAP_E_POETS",      door = { 24, 30 }, mat = { 4, 7 } },
  farmhouse  = { map = "MAP_E_FARMHOUSE",  door = { 31, 30 }, mat = { 4, 7 } },
}

-- --- Setup ---------------------------------------------------------------------------------

-- Run a byte script once, as the current map's ON_FRAME script.
local function ramScript(body)
  L.setVar(S.VAR_TEMP_0, 0)
  local s = { S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 } }
  for _, b in ipairs(body) do s[#s + 1] = b end
  s[#s + 1] = S.SCR_OP_END
  L.runRamScript(s)
end
local function createMon(body, species, level)
  for _, b in ipairs({ S.SCR_OP_CALLNATIVE, { S.ScrCmd_createmon | 1, 4 }, 0, S.PARTY_SIZE,
                       { species, 2 }, { level, 2 }, { 0, 4 } }) do body[#body + 1] = b end
end

local function setup()
  L.setFlag(S.FLAG_SYS_POKEMON_GET_E, true)
  -- Eubouleus watches the threshing floor, on the way to Euphorion's door: his battle is
  -- temple_demeter.sh's, so this walk counts him beaten
  L.setFlag(S.TRAINER_FLAGS_START + S.TRAINER_EUBOULEUS, true)
  local body = {}
  createMon(body, S.SPECIES_LEAD_E, 20)
  createMon(body, S.SPECIES_MELIBEE, 20)
  -- then to the road below the Asclepeion's door
  for _, b in ipairs({ S.SCR_OP_WARP, S.MAP_ELEUSA >> 8, S.MAP_ELEUSA & 0xFF, 0xFF, { 10, 2 }, { 24, 2 },
                       S.SCR_OP_WAITSTATE }) do body[#body + 1] = b end
  ramScript(body)
  L.waitUntil(function() return L.mapId() == S.MAP_ELEUSA and L.idle() end, 3000, "the warp to Eleusa")
  L.wait(30)
  local x, y = L.pos()
  expect(x == 10 and y == 24, string.format("in Eleusa, below the Asclepeion's door (%d,%d)", x, y))
  L.shot("village_start")
end

-- --- Helpers -------------------------------------------------------------------------------

local function hurt(slot) emu:write16(L.partyMon(slot) + S.OFF_MON_HP_E, 1) end
local function nickname(slot)
  local s = ""
  for i = 0, 9 do
    local b = emu:read8(L.partyMon(slot) + S.OFF_MON_NICKNAME + i)
    if b == 0xFF then break end
    if b >= 0xBB and b <= 0xD4 then s = s .. string.char(65 + b - 0xBB) else s = s .. "?" end
  end
  return s
end

local function talk(target, what, opts)
  opts = opts or {}
  opts.shots = opts.shots or { [1] = what }
  local boxes = L.talk(target, opts)
  expect((boxes or 0) >= 1, string.format("%s: %d message box(es)", what, boxes or 0))
  return boxes
end

-- Walk in through the room's door from the village.
local function enter(name)
  local r = ROOMS[name]
  L.setVar(S.VAR_REPEL_STEP_COUNT, 250)       -- keep the wheat quiet on the way
  L.useWarp(S[r.map])
  local x, y = L.pos()
  expect(L.mapId() == S[r.map] and x == r.mat[1] and y == r.mat[2],
         string.format("%s: in through its door, onto the mat at (%d,%d)", name, x, y))
  L.shot(name .. "_room")
end

-- Walk out over the mat: the player comes out of the room's own door.
local function leave(name)
  local r = ROOMS[name]
  L.useWarp(S.MAP_ELEUSA)
  local x, y = L.pos()
  expect(L.mapId() == S.MAP_ELEUSA and x == r.door[1] and (y == r.door[2] or y == r.door[2] + 1),
         string.format("%s: out by its door (%d,%d) at (%d,%d)", name, r.door[1], r.door[2], x, y))
end

local function readAll(prefix, room, names)
  for _, n in ipairs(names) do
    talk(L.sign(prefix .. n), room .. ": " .. n, { shots = { [1] = room .. "_read_" .. n } })
  end
end

-- --- The rooms -----------------------------------------------------------------------------

local function asclepeion()
  enter("asclepeion")
  local m, hx, hy = L.lastHeal()
  expect(m == S.MAP_ELEUSA and hx == 10 and hy == 24,
         string.format("the Asclepeion sets the respawn: map %d (%d,%d), HEAL_LOCATION_ELEUSA_VILLAGE", m, hx, hy))
  hurt(0)
  talk(L.npc(A .. "Healer"), "asclepeion_healer", { every = true })
  local hp, maxHp = L.partyHp(0)
  expect(hp == maxHp, string.format("the healer heals across the counter (%d/%d)", hp, maxHp))
  talk(L.npc(A .. "Panacoil"), "asclepeion_panacoil")
  talk(L.npc(A .. "Pilgrim"), "asclepeion_pilgrim")
  talk(L.npc(A .. "Farmer"), "asclepeion_farmer")
  readAll(A, "asclepeion", { "Statue", "Garden", "Herbs", "Sheaves" })
  -- The Pithos: its two lines, its menu (shown, then closed with B), the lid.
  L.talk(L.sign(A .. "Pithos"), { noSettle = true })
  L.waitUntil(L.boxUp, 300, "the Pithos's text")
  L.wait(34); L.shot("asclepeion_pithos")
  local n = 0
  repeat
    L.tap(K.B); L.wait(40); n = n + 1
    if n == 2 then L.shot("asclepeion_pithos_menu") end
  until L.idle() or n > 12
  expect(L.idle() and not L.on("CB2_PokeStorage"), "the Pithos's menu opens and closes")
  leave("asclepeion")
end

local function agora()
  enter("agora")
  -- The shop's BUY/SELL/QUIT menu and its item list aren't script prompts, so
  -- this is played by hand, as the slice's Agora is.
  L.talk(L.npc(G .. "Stallkeeper"), { noSettle = true, shotBefore = "agora_stallkeeper" })
  local t0 = L.now()
  while not L.taskRunning("Task_ShopMenu") do
    L.tap(K.A); L.wait(20)
    if L.now() - t0 > 900 then L.fail("the stall's shop menu never opened") end
  end
  L.wait(20); L.shot("agora_menu"); L.tap(K.A)                         -- BUY
  L.waitUntil(function() return L.taskRunning("Task_BuyMenu") end, 600, "the stall's item list")
  L.wait(40); L.shot("agora_wares")
  expect(true, "the stall's shop opens on its item list")
  L.tap(K.B)
  L.waitUntil(function() return L.taskRunning("Task_ShopMenu") end, 600, "the shop menu again")
  L.wait(20); L.tap(K.B)                                               -- QUIT
  L.settle({ shots = { [1] = "agora_bye" } })
  expect(L.idle(), "and closes")
  talk(L.npc(G .. "Customer"), "agora_customer")
  readAll(G, "agora", { "HoneyJars", "Scale", "Sacks" })
  leave("agora")
end

local function granary()
  enter("granary")
  local coins = L.itemCount(S.ITEM_AMULET_COIN)
  talk(L.npc(R .. "Sitokles"), "granary_sitokles_lore", { every = true })
  expect(not L.getFlag(S.FLAG_GOT_AMULET_COIN), "before the theft, Sitokles only talks")
  L.setFlag(S.FLAG_FRAGMENT_STOLEN, true)
  talk(L.npc(R .. "Sitokles"), "granary_sitokles_coin", { every = true })
  expect(L.getFlag(S.FLAG_GOT_AMULET_COIN) and L.itemCount(S.ITEM_AMULET_COIN) == coins + 1,
         "after the theft, Sitokles gives the Amulet Coin (FLAG_ICHOR_GOT_AMULET_COIN)")
  talk(L.npc(R .. "Sitokles"), "granary_sitokles_after")
  expect(L.itemCount(S.ITEM_AMULET_COIN) == coins + 1, "and only once")
  local revives = L.itemCount(S.ITEM_REVIVE)
  L.talk(L.hidden(S.FLAG_HIDDEN_REVIVE), { shots = { [1] = "granary_revive" } })
  expect(L.getFlag(S.FLAG_HIDDEN_REVIVE) and L.itemCount(S.ITEM_REVIVE) == revives + 1,
         "the Revive under the bed (FLAG_ICHOR_HIDDEN_ELEUSA_GRANARY_REVIVE)")
  readAll(R, "granary", { "Painting", "SeedCorn", "TallyBoard", "GrainPit" })
  leave("granary")
end

local function poets()
  enter("poets")
  expect(L.npc(P .. "Pithound").present and not L.npc(P .. "Melibee").present,
         "the Pithound is on the stage with Euphorion before the trade")
  talk(L.npc(P .. "Pithound"), "poets_pithound")
  -- Euphorion's lines, YES to the trade, then the storage screen to choose.
  L.talk(L.npc(P .. "Euphorion"), { every = true, stop = function() return L.on("CB2_PokeStorage") end })
  L.waitUntil(function() return L.on("CB2_PokeStorage") end, 600, "the storage screen to choose a Melibee")
  L.wait(90); L.shot("poets_choose_mon")
  L.tap(K.UP); L.wait(20); L.tap(K.UP); L.wait(20)
  L.tap(K.A); L.wait(60)
  L.tap(K.DOWN); L.wait(20)                    -- the Melibee is the second Pokemon
  L.tap(K.A); L.wait(40); L.shot("poets_select")
  L.tap(K.A); L.wait(40)
  L.waitUntil(function() return not L.on("CB2_PokeStorage") end, 1200, "the storage screen to close")
  L.waitUntil(function() return not L.inOverworld() end, 600, "the trade scene")
  local t0, step = L.now(), 0
  while not L.inOverworld() do
    L.tap(K.A); L.wait(9)
    -- a shot every 54 frames: both Pokemon's pics, from the farewell to CRITIC's arrival
    step = step + 1
    if step % 6 == 0 then L.shot(string.format("poets_trade_%02d", step // 6)) end
    if L.now() - t0 > 12000 then L.fail("the trade scene never ended") end
  end
  L.settle({ every = true })
  expect(L.getFlag(S.FLAG_TRADED_PITHOUND), "the trade sets FLAG_ICHOR_TRADED_PITHOUND")
  expect(nickname(1) == "CRITIC", "the Melibee's slot now holds CRITIC (" .. nickname(1) .. ")")
  expect(not L.npc(P .. "Pithound").present and L.npc(P .. "Melibee").present,
         "the Melibee is on the stage after the trade")
  L.shot("poets_melibee")
  talk(L.npc(P .. "Melibee"), "poets_melibee_talk")
  talk(L.npc(P .. "Euphorion"), "poets_after_trade")
  -- After Act I: the new ending.
  L.setFlag(S.FLAG_ACT1_COMPLETE, true)
  talk(L.npc(P .. "Euphorion"), "poets_new_ending", { every = true })
  L.setFlag(S.FLAG_ACT1_COMPLETE, false)
  readAll(P, "poets", { "Desk", "Stage", "Chorus" })
  leave("poets")
end

local function farmhouse()
  enter("farmhouse")
  talk(L.npc(F .. "Theano"), "farmhouse_theano", { every = true })
  expect(L.getFlag(S.FLAG_GOT_TM_BULLET_SEED) and L.itemCount(S.ITEM_TM09) == 1,
         "Theano gives TM09 Bullet Seed (FLAG_ICHOR_GOT_TM_BULLET_SEED)")
  talk(L.npc(F .. "Theano"), "farmhouse_theano_after")
  expect(L.itemCount(S.ITEM_TM09) == 1, "and only once")
  talk(L.npc(F .. "Galekit"), "farmhouse_galekit")
  readAll(F, "farmhouse", { "Stool", "SeedJars", "Hearth" })
  leave("farmhouse")
end

local function keleos()
  enter("keleos")
  hurt(0)
  talk(L.npc(KE .. "Metaneira"), "keleos_metaneira", { every = true, answers = { "no" } })
  local hp, maxHp = L.partyHp(0)
  expect(hp == maxHp, string.format("Metaneira's table heals the party (%d/%d)", hp, maxHp))
  expect(L.getFlag(S.FLAG_MET_METANEIRA) and not L.getFlag(S.FLAG_GOT_KYKEON),
         "her welcome is told (FLAG_ICHOR_MET_METANEIRA); no drink before the Harvest Laurel")
  -- After the Harvest Laurel, once: the goddess's drink. Then the rest by the hearth.
  L.setFlag(S.FLAG_BADGE03_GET_E, true)
  local water, cakes = L.itemCount(S.ITEM_FRESH_WATER), L.itemCount(S.ITEM_BARLEY_CAKE)
  hurt(0)
  talk(L.npc(KE .. "Metaneira"), "keleos_kykeon", { every = true, answers = { "yes" } })
  expect(L.getFlag(S.FLAG_GOT_KYKEON) and L.itemCount(S.ITEM_FRESH_WATER) == water + 2
         and L.itemCount(S.ITEM_BARLEY_CAKE) == cakes + 2,
         "after the Harvest Laurel: 2 Fresh Water and 2 Barley Cakes (FLAG_ICHOR_GOT_KYKEON)")
  hp, maxHp = L.partyHp(0)
  expect(hp == maxHp, "and a night by the hearth")
  talk(L.npc(KE .. "Metaneira"), "keleos_again", { answers = { "no" } })
  expect(L.itemCount(S.ITEM_BARLEY_CAKE) == cakes + 2, "the drink is given once")
  talk(L.npc(KE .. "Girl"), "keleos_girl")
  readAll(KE, "keleos", { "Hearth", "Cradle", "Loom", "WaterJars", "Altar" })
  leave("keleos")
end

L.start(function()
  L.quickstart()
  setup()
  asclepeion()
  agora()
  granary()
  poets()
  farmhouse()
  keleos()
  L.shot("village_end")
  L.log("ok the walk through Eleusa's six rooms is done")
end)
