-- Route 5, the Skironian cliffs, run by tools/ichor/tests/route5.sh (read it first).
--
-- Plays the road with key presses on tools/ichor/tests/engine_lib.lua (slice_lib's
-- walker: a breadth-first search over the live map, one step at a time). People,
-- signs, items and doors are found by the script they run or the flag they set,
-- so a moved NPC never breaks the walk; a missing one fails with its name.
--
-- From a Quickstart it comes out of Hecate's Hollow's west mouth and walks the
-- road to Eleusa's gate: a wild Pokémon from the clearing's band (checked against
-- the route's table), every trainer, every item and hidden item, the set pieces,
-- Aphrodite's altar, the rubble (the Hammer), the Good Rod, the inn (rest, the
-- trade, the room's things), the great herm (anointed), then over the seam into
-- Eleusa and back.
--
-- Prints "ROUTE5 ok ..." per check and "ROUTE5 shot ..." per screenshot, and ends
-- with "ROUTE5 done"; any failure prints "ROUTE5 FAIL: ..." first.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
for k, v in pairs(dofile(L.OUT .. "route5_symbols.lua")) do
  if k == "SCRIPTS" then
    for n, a in pairs(v) do S.SCRIPTS[n] = a end
  else
    S[k] = v
  end
end

local R = "Route5_SkironianCliffs_EventScript_"
local I = "Route5_RestHouse_EventScript_"

local function expect(cond, what) L.expect(cond, what) end

local function talk(target, what, opts)
  local boxes = L.talk(target, opts)
  expect((boxes or 0) >= 1, string.format("%s: %d message box(es)", what, boxes or 0))
  return boxes
end

local function nickname(slot)
  local s = ""
  for i = 0, 9 do
    local c = emu:read8(L.partyMon(slot) + S.OFF_BOXMON_NICKNAME + i)
    if c == 0xFF then break end
    if c >= 0xBB and c <= 0xD4 then s = s .. string.char(65 + c - 0xBB) else s = s .. "?" end
  end
  return s
end

-- Between beats: a fresh repel, and the party healed (Surf has 15 PP; the road
-- has more battles than that).
local function quiet()
  L.setVar(S.VAR_REPEL_STEP_COUNT, 250)
  if L.mapId() == S.MAP_ROUTE5 then L.runHeader("Route5Test_HealHeader") end
end

-- The wild table, by time of day: every species a land encounter here may be.
local WILD = {}
for _, n in ipairs({ "LOPHOPS", "KERAZAP", "CHELONET", "GALEKIT", "ONOTIS", "EPOPOI", "ELALEAF", "ERGANT",
                     "PEBBLITH", "HARPECK", "NEMECUB", "GELASABLE", "SPALUNK" }) do
  WILD[S["SPECIES_" .. n]] = n
end

-- Walk back and forth in the clearing's band until a wild Pokémon comes out.
local function wildInTheBand()
  L.setBeat("wild", false)
  L.go(16, 6)
  local _, _, b = L.grid().tile(16, 6)
  expect(b == S.MB_TALL_GRASS, "standing in the clearing's band")
  L.setVar(S.VAR_REPEL_STEP_COUNT, 0)
  local met
  for i = 1, 300 do
    local key = (i % 2 == 0) and K.UP or K.DOWN
    local r = L.step(key)
    if r == "taken" or L.inBattle() then
      L.waitUntil(L.inBattle, 1200, "the wild battle")
      L.wait(120)
      local species = emu:read16(S.gBattleMons + S.BATTLE_MON_SIZE + S.OFF_BATTLE_MON_SPECIES)
      local level = emu:read8(S.gBattleMons + S.BATTLE_MON_SIZE + S.OFF_BATTLE_MON_LEVEL)
      met = WILD[species] or ("species " .. species)
      L.shot("wild_in_the_band")
      expect(WILD[species] ~= nil and level >= 17 and level <= 21,
             string.format("a wild %s, level %d, from Route 5's table", met, level))
      L.settle()
      break
    end
  end
  expect(met ~= nil, "a wild Pokemon met in the band")
  quiet()
end

local function trainer(t, script, what, talkTo)
  if not L.defeated(t) then
    if talkTo then
      L.talk(L.npc(R .. script))
    else
      -- walk into the sight line: the trainer stops the player and the battle plays
      L.goTrigger(L.sight(R .. script))
      L.settle()
    end
  end
  expect(L.defeated(t), what .. " beaten")
  talk(L.npc(R .. script), what .. "'s after-battle line")
end

-- --- Out of the mouth, along the cliff road -----------------------------------------------

local function cliffRoad()
  L.setBeat("cliff road", false)
  local x, y = L.pos()
  expect(L.mapId() == S.MAP_ROUTE5 and x == 9 and y == 9,
         string.format("out of the Hollow's mouth onto the cliff road (%d,%d)", x, y))
  local mus = L.mapMusic()
  expect(mus == S.MUS_ROAD or mus == S.MUS_ROAD_NIGHT,
         string.format("Route 5 plays the road's tune (%s)", mus == S.MUS_ROAD and "MUS_ICHOR_ROAD" or
                       mus == S.MUS_ROAD_NIGHT and "its night form" or tostring(mus)))
  L.shot("out_of_the_mouth")
  talk(L.sign(R .. "MouthSign"), "the mouth's sign", { shots = { [1] = "read_MouthSign" } })
  wildInTheBand()
  L.talk(L.ball(S.FLAG_ITEM_SUPER_POTION))
  expect(L.getFlag(S.FLAG_ITEM_SUPER_POTION), "the clearing's Super Potion taken")
  -- Kynegeiros watches the one-cell ledge past the seat
  trainer(S.TRAINER_KYNEGEIROS, "Kynegeiros", "Kynegeiros")
  L.shot("past_the_ledge")
  talk(L.sign(R .. "Seat"), "the rock seat", { every = true })
  L.talk(L.ball(S.FLAG_ITEM_GREAT_BALL))
  expect(L.getFlag(S.FLAG_ITEM_GREAT_BALL), "the Great Ball beside the seat taken")
  trainer(S.TRAINER_MELANTHIOS, "Melanthios", "Melanthios", true)
  talk(L.npc(R .. "Goat"), "the goatherd's kid")
  -- the knoll's column drum: no Girdle yet, so it stays put
  talk(L.npc("EventScript_StrengthBoulder"), "the column drum on the knoll's path")
  expect(not L.getFlag(S.FLAG_ITEM_PP_UP), "the watchtower's PP Up waits for the Girdle")
  talk(L.npc(R .. "PitchGatherer"), "the pitch-gatherer")
  -- the pine hollow's thicket: no Sickle yet
  talk(L.npc("EventScript_CutTree"), "the thicket over the pine hollow")
  expect(not L.getFlag(S.FLAG_THICKET_CUT), "the thicket stays until Demeter's Sickle")
end

local function meadow()
  L.setBeat("meadow", false)
  quiet()
  talk(L.sign(R .. "MeadowSign"), "the meadow's sign", { shots = { [1] = "read_MeadowSign" } })
  trainer(S.TRAINER_ARISTAIOS, "Aristaios", "Aristaios", true)
  talk(L.sign(R .. "Hives"), "the hives")
  L.talk(L.hidden(S.FLAG_HIDDEN_HONEY))
  expect(L.getFlag(S.FLAG_HIDDEN_HONEY), "the Honey under a hive found")
  L.talk(L.ball(S.FLAG_ITEM_SUPER_REPEL))
  expect(L.getFlag(S.FLAG_ITEM_SUPER_REPEL), "the Super Repel at the meadow's end taken")
  talk(L.sign(R .. "DigSpot"), "the meadow's dig spot")
  L.shot("the_meadow")
end

-- --- Down the cutting, back along the terrace ----------------------------------------------

local function terrace()
  L.setBeat("terrace", false)
  quiet()
  -- east of the cutting first: the shepherd's long grass and the Ether past him
  trainer(S.TRAINER_DAPHNIS, "Daphnis", "Daphnis", true)
  L.talk(L.ball(S.FLAG_ITEM_ETHER))
  expect(L.getFlag(S.FLAG_ITEM_ETHER), "the Ether at the terrace's east end taken")
  trainer(S.TRAINER_MYRTO, "Myrto", "Myrto", true)
  talk(L.sign(R .. "Niches"), "Aphrodite's niches", { shots = { [1] = "read_Niches" } })
  talk(L.sign("EventScript_IchorAltar_Aphrodite"), "Aphrodite's altar (prayer)", { shots = { [1] = "altar" } })
  L.talk(L.hidden(S.FLAG_HIDDEN_PRETTY_FEATHER))
  expect(L.getFlag(S.FLAG_HIDDEN_PRETTY_FEATHER), "the Pretty Feather in a niche found")
  -- the rubble closing the lookout breaks to the Bronze Hammer
  L.talk(L.npc("EventScript_RockSmash"), { answers = { "yes" } })
  expect(L.getFlag(S.FLAG_RUBBLE_BROKEN), "the Hammer broke the lookout's rubble")
  L.talk(L.ball(S.FLAG_ITEM_REVIVE))
  expect(L.getFlag(S.FLAG_ITEM_REVIVE), "the Revive at the lookout taken")
  L.shot("the_lookout")
end

-- --- Down the cleft stair to the shore ----------------------------------------------------

local function shore()
  L.setBeat("shore", false)
  quiet()
  trainer(S.TRAINER_MOPSOS, "Mopsos", "Mopsos")
  L.shot("past_the_stair")
  trainer(S.TRAINER_KERDON, "Kerdon", "Kerdon", true)
  L.talk(L.hidden(S.FLAG_HIDDEN_HEART_SCALE))
  expect(L.getFlag(S.FLAG_HIDDEN_HEART_SCALE), "the Heart Scale at the point's tip found")
  talk(L.npc(R .. "Aigialeus"), "Aigialeus", { every = true })
  expect(L.getFlag(S.FLAG_GOT_GOOD_ROD) and L.itemCount(S.ITEM_GOOD_ROD) == 1, "Aigialeus gave the Good Rod")
  talk(L.npc(R .. "Aigialeus"), "Aigialeus after the gift")
  talk(L.npc(R .. "Boat"), "Aigialeus's boat")
  talk(L.npc(R .. "PilgrimA"), "the first initiate")
  talk(L.npc(R .. "PilgrimB"), "the second initiate")
end

-- --- The Inn of the Plain --------------------------------------------------------------

local function inn()
  L.setBeat("inn", false)
  quiet()
  talk(L.sign(R .. "InnSign"), "the inn's sign")
  L.runHeader("Route5Test_OnotisHeader")              -- an Onotis to trade, in party slot 1
  L.useWarp(S.MAP_REST_HOUSE)
  expect(L.mapId() == S.MAP_REST_HOUSE, "through the inn's door")
  L.shot("inn_room")
  expect(L.npc(I .. "Galanthis").present and not L.npc(I .. "Onotis").present,
         "Galanthis sits by the sandals before the trade")
  -- rest: hurt the lead, and Xenokles heals it
  emu:write16(L.partyMon(0) + S.OFF_MON_HP, 1)
  L.talk(L.npc(I .. "Xenokles"), { noSettle = true })
  L.settle({ stop = function() return L.taskRunning("Task_HandleYesNoInput") end, every = true })
  local hp, maxhp = L.partyHp(0)
  expect(hp == maxhp, string.format("Xenokles's rest heals the party (%d/%d)", hp, maxhp))
  expect(L.getFlag(S.FLAG_MET_XENOKLES), "Xenokles's welcome heard")
  -- the trade: YES, then the Onotis (party slot 1) from the storage screen
  L.wait(10); L.shot("trade_prompt"); L.tap(K.A)
  L.waitUntil(function() return L.on("CB2_PokeStorage") end, 900, "the storage screen")
  L.wait(90); L.shot("trade_choose_mon")
  L.tap(K.UP); L.wait(20); L.tap(K.UP); L.wait(20)
  L.tap(K.A); L.wait(60)
  L.tap(K.DOWN); L.wait(20)
  L.tap(K.A); L.wait(40)
  L.tap(K.A); L.wait(40)
  L.waitUntil(function() return not L.on("CB2_PokeStorage") end, 1200, "the storage screen to close")
  L.waitUntil(function() return not L.inOverworld() end, 600, "the trade scene")
  local t0 = L.now()
  while not L.inOverworld() do
    L.tap(K.A); L.wait(9)
    if L.now() - t0 > 12000 then L.fail("the trade scene never ended") end
  end
  L.settle({ every = true })
  expect(L.getFlag(S.FLAG_TRADED_GELASABLE), "the trade sets FLAG_ICHOR_TRADED_GELASABLE")
  expect(nickname(1) == "GALANTHIS", "the Onotis's slot now holds GALANTHIS (" .. nickname(1) .. ")")
  expect(not L.npc(I .. "Galanthis").present and L.npc(I .. "Onotis").present,
         "the Onotis stands in the stall after the trade")
  L.shot("after_the_trade")
  talk(L.npc(I .. "Xenokles"), "Xenokles after the trade")
  talk(L.npc(I .. "StableBoy"), "the stable boy")
  talk(L.npc(I .. "Onotis"), "the Onotis in its stall")
  for _, s in ipairs({ "RoadMap", "Sandals", "Hearth", "Washbasin", "StableDoors" }) do
    talk(L.sign(I .. s), "the inn's " .. s)
  end
  L.useWarp(S.MAP_ROUTE5)
  expect(L.mapId() == S.MAP_ROUTE5, "back out of the inn's door")
end

-- --- The herm, the yard, and on to Eleusa ------------------------------------------------

local function eastEnd()
  L.setBeat("east end", false)
  quiet()
  local oil = L.itemCount(S.ITEM_OLIVE_OIL)
  talk(L.sign("EventScript_IchorGreatHerm"), "the great herm", { answers = { "yes" }, shots = { [2] = "herm" } })
  expect(L.getFlag(S.FLAG_HERM_ROUTE5) and L.itemCount(S.ITEM_OLIVE_OIL) == oil - 1,
         "the great herm anointed (HERM_AETHOS_ROUTE_5)")
  L.talk(L.hidden(S.FLAG_HIDDEN_ORAN_BERRY))
  expect(L.getFlag(S.FLAG_HIDDEN_ORAN_BERRY), "the Oran Berry in the inn's yard found")
  talk(L.sign(R .. "EastSign"), "the east sign", { shots = { [1] = "read_EastSign" } })
  L.shot("the_east_end")
  L.leaveEdge("right", S.MAP_ELEUSA)
  L.settle()
  expect(L.mapId() == S.MAP_ELEUSA, "over the seam into Eleusa")
  local x, y = L.pos()
  expect(x == 0 and y >= 24 and y <= 27, string.format("on Eleusa's west road (%d,%d)", x, y))
  L.go(6, 25)
  L.shot("eleusa_gate")
  L.go(1, 25)
  L.leaveEdge("left", S.MAP_ROUTE5)
  L.settle()
  x, y = L.pos()
  expect(L.mapId() == S.MAP_ROUTE5 and x == 67 and y >= 21 and y <= 24,
         string.format("and back over the seam onto Route 5 (%d,%d)", x, y))
  L.shot("back_on_route5")
end

L.start(function()
  L.quickstart()
  -- the setup gives a level-100 Swampert, with its moves, to win the trainers'
  -- battles with its first one (the Onotis for the inn's trade comes at the inn)
  L.runHeader("Route5Test_SetupHeader", { limit = 4000 })
  expect(L.partyLevel(0) == S.MAX_LEVEL, "a level-100 lead")
  -- Wild battles are fought, not run from: the route's Spalunk (Diglett until the
  -- dex lands) has Arena Trap, and slice_lib's battle player fights a wild one
  -- only while FLAG_ICHOR_NO_RUNNING is set.
  L.setFlag(S.FLAG_NO_RUNNING, true)
  L.waitUntil(function() return L.mapId() == S.MAP_ROUTE5 and L.idle() end, 3000, "the warp to Route 5")
  L.wait(30)
  quiet()
  cliffRoad()
  meadow()
  terrace()
  shore()
  inn()
  eastEnd()
  L.log("ok the walk is done")
end)
