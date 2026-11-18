-- Lakonia's fifteen rooms, run by tools/ichor/tests/lakonia_rooms.sh (read it first).
--
-- Each room is entered by a warp to the tile just inside its mat (the outdoor
-- maps are built separately), shot, and played: people are found by the script
-- they run and signs by theirs, so a moved NPC never breaks the walk.
--
-- Prints "LAKONIA_ROOMS ok ..." per check and ends with "LAKONIA_ROOMS done";
-- any failure prints "LAKONIA_ROOMS FAIL: ..." first.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
S.SCRIPTS = S.SCRIPTS or {}
for k, v in pairs(dofile(L.OUT .. "lakonia_rooms_symbols.lua")) do S.SCRIPTS[k] = v end

local function expect(cond, what) L.expect(cond, what) end

-- the tile just inside each room's mat
local ROOMS = {
  { "g_asclepeion", "MAP_G_ASCLEPEION", 7, 5 }, { "g_dyeworks", "MAP_G_DYEWORKS", 5, 6 },
  { "g_lysandros", "MAP_G_LYSANDROS", 4, 6 }, { "g_timaia", "MAP_G_TIMAIA", 4, 5 },
  { "g_kranai", "MAP_G_KRANAI", 3, 5 }, { "l_asclepeion", "MAP_L_ASCLEPEION", 3, 5 },
  { "l_agora", "MAP_L_AGORA", 3, 5 }, { "l_lampito", "MAP_L_LAMPITO", 6, 7 },
  { "l_gylippos", "MAP_L_GYLIPPOS", 3, 5 }, { "l_syssition", "MAP_L_SYSSITION", 6, 5 },
  { "l_agoge", "MAP_L_AGOGE", 7, 8 }, { "l_palaestra", "MAP_L_PALAESTRA", 5, 7 },
  { "l_orthia", "MAP_L_ORTHIA", 7, 9 }, { "l_chilon", "MAP_L_CHILON", 3, 5 },
  { "l_lichas", "MAP_L_LICHAS", 4, 6 },
}
local AT = {}
for _, r in ipairs(ROOMS) do AT[r[1]] = r end

local function ramScript(body)
  L.setVar(S.VAR_TEMP_0, 0)
  local s = { S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 } }
  for _, b in ipairs(body) do s[#s + 1] = b end
  s[#s + 1] = S.SCR_OP_END
  L.runRamScript(s)
end

local function enter(name)
  local r = AT[name]
  local map = S[r[2]]
  ramScript({ S.SCR_OP_WARP, map >> 8, map & 0xFF, 0xFF, { r[3], 2 }, { r[4], 2 }, S.SCR_OP_WAITSTATE })
  L.waitUntil(function() return L.mapId() == map and L.idle() end, 3000, "the warp to " .. name)
  L.wait(30)
  local x, y = L.pos()
  expect(x == r[3] and y == r[4], string.format("%s: loads, the player inside its door at (%d,%d)", name, x, y))
  L.shot(name)
end

local function addItems(list)
  local code = { S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 } }
  for _, it in ipairs(list) do
    code[#code + 1] = S.SCR_OP_ADDITEM
    code[#code + 1] = { it[1], 2 }
    code[#code + 1] = { it[2], 2 }
  end
  code[#code + 1] = S.SCR_OP_END
  L.setVar(S.VAR_TEMP_0, 0)
  L.runRamScript(code)
  L.waitUntil(function() return L.getVar(S.VAR_TEMP_0) == 1 end, 300, "the items to be given")
  L.wait(10)
end

local function createMon(species, level)
  ramScript({ S.SCR_OP_CALLNATIVE, { S.ScrCmd_createmon | 1, 4 }, 0, S.PARTY_SIZE,
              { species, 2 }, { level, 2 }, { 0, 4 } })
  L.waitUntil(function() return L.getVar(S.VAR_TEMP_0) == 1 end, 300, "the mon to be made")
  L.wait(10)
end

local function hurt(slot) emu:write16(L.partyMon(slot) + S.OFF_MON_HP_L, 1) end

local function talk(target, what, opts)
  opts = opts or {}
  opts.shots = opts.shots or { [1] = what }
  local boxes = L.talk(target, opts)
  expect((boxes or 0) >= 1, string.format("%s: %d message box(es)", what, boxes or 0))
  return boxes
end

local function read(script, what) talk(L.sign(script), what) end

-- --- Gytheion ------------------------------------------------------------------------------

local function gytheion()
  local P = "Gytheion_Asclepeion_EventScript_"
  enter("g_asclepeion")
  hurt(0)
  talk(L.npc(P .. "Healer"), "g_asclepeion_healer", { every = true })
  local hp, maxHp = L.partyHp(0)
  expect(hp == maxHp, string.format("Gytheion's healer heals across the ticket counter (%d/%d)", hp, maxHp))
  local m = L.lastHeal()
  expect(m == S.MAP_GYTHEION_O, "the Asclepeion makes Gytheion the respawn")
  talk(L.npc(P .. "Fisherman"), "g_asclepeion_fisherman")
  read(P .. "FlatSea", "g_asclepeion_flat")

  P = "Gytheion_Dyeworks_EventScript_"
  enter("g_dyeworks")
  addItems({ { S.ITEM_SHOAL_SHELL, 2 } })
  talk(L.npc(P .. "Porphyris"), "g_dyeworks_two")
  expect(not L.getFlag(S.FLAG_KINGS_ROCK), "two shells aren't three")
  addItems({ { S.ITEM_SHOAL_SHELL, 2 } })
  talk(L.npc(P .. "Porphyris"), "g_dyeworks_kingsrock")
  expect(L.getFlag(S.FLAG_KINGS_ROCK) and L.itemCount(S.ITEM_KINGS_ROCK) == 1
         and L.itemCount(S.ITEM_SHOAL_SHELL) == 1, "three shells for a King's Rock (one shell left over)")
  read(P .. "Vat", "g_dyeworks_vat")

  P = "Gytheion_LysandrosHouse_EventScript_"
  enter("g_lysandros")
  talk(L.npc(P .. "Lysandros"), "g_lysandros", { answers = { "no" } })
  read(P .. "GulfMap", "g_lysandros_map")

  P = "Gytheion_TimaiaHouse_EventScript_"
  enter("g_timaia")
  talk(L.npc(P .. "Timaia"), "g_timaia_cake", { answers = { "yes" } })
  expect(L.getFlag(S.FLAG_CARRYING_CAKE), "Timaia's fig cake is carried (FLAG_ICHOR_CARRYING_FIG_CAKE)")
  L.setFlag(S.FLAG_DELIVERED_CAKE, true)
  talk(L.npc(P .. "Timaia"), "g_timaia_leftovers")
  expect(L.getFlag(S.FLAG_LEFTOVERS) and L.itemCount(S.ITEM_LEFTOVERS) == 1, "once Teleklos has eaten it: Leftovers")

  P = "Gytheion_KranaiShrine_EventScript_"
  enter("g_kranai")
  talk(L.npc(P .. "Klymene"), "g_kranai_before")
  expect(not L.getFlag(S.FLAG_SHINY_STONE), "no Shiny Stone before the climax")
  L.setVar(S.VAR_ACT3, 19)
  talk(L.npc(P .. "Klymene"), "g_kranai_after")
  expect(L.getFlag(S.FLAG_SHINY_STONE) and L.itemCount(S.ITEM_SHINY_STONE) == 1, "after the climax: the Shiny Stone")
  L.setVar(S.VAR_ACT3, 7)
  read(P .. "Sandals", "g_kranai_sandals")
end

-- --- Lakonia -------------------------------------------------------------------------------

local function lakonia()
  local P = "Lakonia_Asclepeion_EventScript_"
  enter("l_asclepeion")
  hurt(0)
  talk(L.npc(P .. "Healer"), "l_asclepeion_healer", { every = true })
  local hp, maxHp = L.partyHp(0)
  expect(hp == maxHp, "Lakonia's healer: \"Wounds?\" ... \"Done.\"")
  expect(L.getVar(S.VAR_TEMP_1) == 1, "and remembers the visit")
  hurt(0)
  talk(L.npc(P .. "Healer"), "l_asclepeion_again", { every = true })
  hp, maxHp = L.partyHp(0)
  expect(hp == maxHp, "a second time: \"Again?\" ... \"Fight better.\"")
  local m = L.lastHeal()
  expect(m == S.MAP_LAKONIA_O, "the Asclepeion makes Lakonia the respawn")

  P = "Lakonia_Agora_EventScript_"
  enter("l_agora")
  read(P .. "Scales", "l_agora_scales")
  read(P .. "Bars", "l_agora_bars")

  P = "LakoniaLampito_EventScript_"
  enter("l_lampito")
  local g = L.grid()
  expect(g.tile(4, 2) ~= S.METATILE_HEARTH_LIT, "Lampito's hearth is cold")
  read(P .. "Stelai", "l_lampito_stelai")
  L.setFlag(S.FLAG_RHEA_UNMASKED, true)
  enter("l_agora")      -- a warp to the map you're on doesn't fade back in; go round
  enter("l_lampito")
  g = L.grid()
  expect(g.tile(4, 2) == S.METATILE_HEARTH_LIT, "after the helmet comes off, the hearth is lit")
  L.shot("l_lampito_lit")
  L.setFlag(S.FLAG_RHEA_UNMASKED, false)

  P = "Lakonia_GylipposHouse_EventScript_"
  enter("l_gylippos")
  talk(L.npc(P .. "Gylippos"), "l_gylippos")
  expect(L.getFlag(S.FLAG_STRAP), "Gylippos hands over the strap (FLAG_ICHOR_GOT_SCYTALE_STRAP)")

  P = "Lakonia_Syssition_EventScript_"
  enter("l_syssition")
  talk(L.npc(P .. "Dexippos"), "l_syssition_broth", { answers = { "yes" } })
  expect(L.getFlag(S.FLAG_TM_BULK_UP) and L.itemCount(S.ITEM_TM_BULK_UP) == 1, "the black broth: TM Bulk Up")
  talk(L.npc(P .. "Dexippos"), "l_syssition_again", { answers = { "yes" } })
  expect(L.itemCount(S.ITEM_TM_BULK_UP) == 1, "only once")

  P = "Lakonia_Agoge_EventScript_"
  enter("l_agoge")
  talk(L.npc(P .. "Archidamos"), "l_agoge_before")
  expect(not L.getFlag(S.FLAG_FOCUS_SASH), "no Focus Sash before the ring")
  L.setFlag(S.FLAG_KLEON_DONE, true)
  talk(L.npc(P .. "Archidamos"), "l_agoge_after")
  expect(L.getFlag(S.FLAG_FOCUS_SASH) and L.itemCount(S.ITEM_FOCUS_SASH) == 1, "after Kleon's ring: the Focus Sash")
  L.setFlag(S.FLAG_KLEON_DONE, false)
  read(P .. "Names", "l_agoge_names")

  P = "Lakonia_Palaestra_EventScript_"
  enter("l_palaestra")
  talk(L.npc(P .. "Hipposthenes"), "l_palaestra_before")
  expect(not L.getFlag(S.FLAG_CHOICE_BAND), "no Choice Band without a Geogrip")
  createMon(S.SPECIES_GEOGRIP, 40)
  talk(L.npc(P .. "Hipposthenes"), "l_palaestra_geogrip")
  expect(L.getFlag(S.FLAG_CHOICE_BAND) and L.itemCount(S.ITEM_CHOICE_BAND) == 1, "a Geogrip: the Choice Band")

  P = "LakoniaOrthia_EventScript_"
  enter("l_orthia")
  talk(L.npc(P .. "Kleta"), "l_orthia_start", { answers = { "yes" } })
  expect(L.getVar(S.VAR_TEMP_1) == 1, "Kleta starts the cheese game")
  -- the watched tiles: row 4 x 3..10 (the west watcher), row 6 x 4..11 (the east)
  local function watched(x, y)
    return (y == 4 and x >= 3 and x <= 10) or (y == 6 and x >= 4 and x <= 11)
  end
  for _, c in ipairs({ "CheeseWest", "CheeseMiddle", "CheeseEast" }) do
    talk(L.sign(P .. c), "l_orthia_" .. c, { avoid = watched })
  end
  expect(L.getVar(S.VAR_TEMP_2) == 3 and L.grid().tile(7, 3) ~= nil, "three cheeses, taken from behind the altar")
  talk(L.npc(P .. "Kleta"), "l_orthia_won", { avoid = watched })
  expect(L.getFlag(S.FLAG_SCOPE_LENS) and L.itemCount(S.ITEM_SCOPE_LENS) == 1, "unseen: the Scope Lens")
  -- seen: a fresh game, then a step into the west watcher's line walks you back
  enter("l_agora")
  enter("l_orthia")
  L.setVar(S.VAR_TEMP_1, 1)
  L.goTrigger({ ["7,4"] = true })
  L.settle()
  L.wait(30)
  L.shot("l_orthia_seen")
  local x, y = L.pos()
  expect(L.mapId() == S.MAP_L_ORTHIA and x == 7 and y == 9, string.format("seen: walked back to the steps (%d,%d)", x, y))

  P = "Lakonia_ChilonHouse_EventScript_"
  enter("l_chilon")
  talk(L.npc(P .. "Chilon"), "l_chilon_wrong")
  expect(not L.getFlag(S.FLAG_WISE_GLASSES), "too many words: no Wise Glasses")
  read(P .. "Shard", "l_chilon_shard")

  P = "Lakonia_LichasHouse_EventScript_"
  enter("l_lichas")
  hurt(0)
  talk(L.npc(P .. "Lichas"), "l_lichas", { every = true, answers = { "no" } })
  hp, maxHp = L.partyHp(0)
  expect(hp == maxHp and L.getFlag(S.FLAG_XENIA), "Lichas's table heals (FLAG_ICHOR_XENIA_LAKONIA)")
  read(P .. "Tripod", "l_lichas_tripod")
end

L.start(function()
  L.quickstart()
  L.setFlag(S.FLAG_SYS_POKEMON_GET_L, true)
  L.setVar(S.VAR_ACT3, 7)
  createMon(S.SPECIES_LEAD_L, 30)
  local leadHp = L.partyHp(0)
  expect((leadHp or 0) > 0, "a lead in the party")
  gytheion()
  lakonia()
  L.log("ok the walk through Lakonia's fifteen rooms is done")
end)
