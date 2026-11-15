-- Route 4, the Isthmus road, run by tools/ichor/tests/route4.sh (read it first).
--
-- Plays with key presses on tools/ichor/tests/engine_lib.lua (slice_lib's walker:
-- a breadth-first search over the live map, one step at a time). People, signs,
-- items and triggers are found by the script they run or the flag they set, so a
-- moved NPC never breaks the walk; a missing one fails with its name.
--
-- Prints "ROUTE4 ok ..." per check and "ROUTE4 shot ..." per screenshot, and ends
-- with "ROUTE4 done"; any failure prints "ROUTE4 FAIL: ..." first.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
for k, v in pairs(dofile(L.OUT .. "route4_symbols.lua")) do
  if k == "SCRIPTS" then
    for n, a in pairs(v) do S.SCRIPTS[n] = a end
  else
    S[k] = v
  end
end

local P = "Route4_Isthmus_EventScript_"
local REPEL = 4000

local function expect(cond, what) L.expect(cond, what) end

-- Warp to (x, y) on `map` from an ON_FRAME script in spare EWRAM.
local function warpTo(map, x, y)
  L.setVar(S.VAR_TEMP_0, 0)
  L.runRamScript({ S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 },
                   S.SCR_OP_WARP, map >> 8, map & 0xFF, 0xFF, { x, 2 }, { y, 2 }, S.SCR_OP_WAITSTATE, S.SCR_OP_END })
  L.waitUntil(function() return L.mapId() == map and L.idle() end, 3000, "the warp to map " .. map)
  L.wait(30)
end

-- Put items in the bag with additem, from an ON_FRAME script.
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

local function giveLead(level)
  level = level or S.MAX_LEVEL
  for i = 0, S.PARTY_SIZE - 1 do
    for o = 0, S.POKEMON_SIZE - 1 do emu:write8(L.partyMon(i) + o, 0) end
  end
  emu:write8(S.gPartiesCount, 0)
  L.setVar(S.VAR_TEMP_0, 0)
  L.runRamScript({ S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 },
                   S.SCR_OP_CALLNATIVE, { S.ScrCmd_createmon | 1, 4 }, 0, S.PARTY_SIZE,
                   { S.SPECIES_LEAD, 2 }, { level == S.MAX_LEVEL and 5 or level, 2 }, { 0, 4 },
                   S.SCR_OP_SETMONMOVE, 0, 0, { S.MOVE_LEAD, 2 }, S.SCR_OP_END })
  L.settle()
  if level == S.MAX_LEVEL then
    L.setVar(S.VAR_TEMP_0, 0)
    L.assistLevel100()
    L.settle()
  end
  local hp, maxhp = L.partyHp(0)
  expect(L.partyLevel(0) == level and hp > 0, string.format("a level-%d lead (HP %d/%d)", level, hp, maxhp))
end

local function repel() L.setVar(S.VAR_REPEL_STEP_COUNT, REPEL) end

local function read(target, what, opts)
  local boxes = L.talk(target, opts)
  expect((boxes or 0) >= 1, string.format("%s: %d message box(es)", what, boxes or 0))
  return boxes
end

local function arachneSherds()
  local count = 0
  for i = 0, 3 do
    if L.getFlag(S.FLAG_ARACHNE_SHERDS + i) then count = count + 1 end
  end
  return count
end

local function arachneDig(script, flag, seed)
  local before = arachneSherds()
  local savedSeed = emu:read32(L.sb1() + S.OFF_SB1_DAILY_SEED)
  if seed then emu:write32(L.sb1() + S.OFF_SB1_DAILY_SEED, seed) end
  read(L.sign(P .. script), script, { every = true })
  emu:write32(L.sb1() + S.OFF_SB1_DAILY_SEED, savedSeed)
  expect(L.getFlag(flag), script .. " records its own dig")
  expect(arachneSherds() == before + 1, script .. " gives one actual Arachne sherd")
  read(L.sign(P .. script), script .. " again")
  expect(arachneSherds() == before + 1, script .. " cannot give the sherd twice")
end

-- Top the lead's HP back up between battles.
local function heal()
  local mon = L.partyMon(0)
  emu:write16(mon + S.OFF_MON_HP_E, emu:read16(mon + S.OFF_MON_MAXHP_E))
end

-- A trainer: walk up and talk (or be seen on the way); the battle is played out.
local function fight(script, trainer, name)
  if not L.defeated(trainer) then
    L.talk(L.npc(P .. script))
  end
  expect(L.defeated(trainer), name .. " beaten")
  heal()
end

local function item(flag, name)
  L.talk(L.ball(flag))
  expect(L.getFlag(flag), name .. " picked up")
end

local function hidden(flag, name)
  L.talk(L.hidden(flag))
  expect(L.getFlag(flag), name .. " found")
end

local function tile(x, y) local mid = L.grid().tile(x, y) return mid end

-- --- Setup and the seam ------------------------------------------------------------------------

local function setup()
  L.setBeat("setup", false)
  L.quickstart()
  giveLead()
  -- after beat 16: the Herald Laurel, Kleon gone up the road, the Hammer from the forge
  L.setFlag(S.FLAG_BADGE02_GET, true)
  L.setFlag(S.FLAG_KLEON_BATTLE_2_DONE, true)
  L.setFlag(S.FLAG_HIDE_KLEON_GATE, true)
  -- the test lead is someone else's level-100 Pokemon: Emerald's last badge makes it obey
  L.setFlag(S.FLAG_BADGE08_GET, true)
  addItems({ { S.ITEM_BRONZE_HAMMER, 1 }, { S.ITEM_OLIVE_OIL, 2 } })
  expect(L.getFlag(S.FLAG_GOT_BRONZE_HAMMER), "the Bronze Hammer is in the bag (its relic flag set)")
  repel()
  warpTo(S.MAP_EMPORION, 8, 8)
  L.shot("emporion_gate")
  L.leaveEdge("up", S.MAP_ROUTE4)
  local x, y = L.pos()
  expect(L.mapId() == S.MAP_ROUTE4 and x >= 7 and x <= 9, string.format("through the Isthmus Gate onto Route 4 at (%d,%d)", x, y))
  -- (across a seam the city's song fades out first)
  L.waitUntil(function() return L.mapMusic() ~= 0 and L.mapMusic() ~= S.MUS_EMPORION end, 900, "Route 4's song")
  local music = L.mapMusic()
  expect(music == S.MUS_ROAD or music == S.MUS_ROAD_NIGHT,
         string.format("Route 4 plays MUS_ICHOR_ROAD or its night form (song %d)", music))
  L.shot("route4_south_end")
end

-- --- The potters' quarter and the woods clearing ----------------------------------------------

local function potters()
  L.setBeat("potters", false)
  read(L.sign(P .. "SouthSign"), "the south sign", { shots = { [1] = "sign_south" } })
  -- the Hammer's first lesson: the clearing's rubble (EventScript_RockSmash)
  L.go(8, 19)
  local rubble = L.npc("EventScript_RockSmash")
  expect(rubble.present, "marble rubble chokes the woods clearing")
  L.talk(rubble, { shotBefore = "clearing_rubble" })
  expect(not L.npc("EventScript_RockSmash").present, "the rubble breaks under the Hammer")
  repel()
  item(S.FLAG_ITEM_GREAT_BALL, "the clearing's Great Ball")
  L.shot("clearing")
  L.go(8, 19)
  -- Exekias watches the road from the kiln yard: the walk north meets him
  L.go(8, 16)
  expect(L.defeated(S.TRAINER_EXEKIAS), "Exekias stops the walk north (mandatory)")
  heal()
  read(L.npc(P .. "KilnWorker"), "the kiln worker", { shots = { [1] = "kiln_worker" } })
  item(S.FLAG_ITEM_POTION, "the Potion by the kilns")
  hidden(S.FLAG_HIDDEN_ETHER, "the Ether in the kiln's ash")
  read(L.sign(P .. "DigKilns"), "the kiln dig without the Trowel")
  expect(not L.getFlag(S.FLAG_DIG_KILNS) and arachneSherds() == 0, "a missing Trowel leaves the kiln find untouched")
  addItems({ { S.ITEM_TROWEL, 1 } })
  expect(L.itemCount(S.ITEM_TROWEL) == 1, "the route fixture receives a real Trowel")
  -- Both initial rolls select sherds, with or without Demeter's reroll.
  arachneDig("DigKilns", S.FLAG_DIG_KILNS, 0x2F)
  expect(not L.getFlag(S.FLAG_DIG_SPUR), "the kiln dig leaves the spur's daily find available")
  read(L.npc(P .. "Exekias"), "Exekias after")
end

-- --- The tombs, the spur and the herm ----------------------------------------------------------

local function tombs()
  L.setBeat("tombs", false)
  read(L.sign(P .. "TombsSign"), "the tombs sign", { shots = { [1] = "sign_tombs" } })
  read(L.npc(P .. "Mourner"), "the mourner", { shots = { [1] = "mourner" } })
  read(L.sign(P .. "KalliasPanel"), "the Kallias plot")
  -- Hecate's glade off the corner: her shrine and the Spell Tag
  read(L.sign(P .. "HecateShrine"), "Hecate's crossroads shrine", { shots = { [1] = "hecate_shrine" } })
  item(S.FLAG_ITEM_SPELL_TAG, "the glade's Spell Tag")
  -- band 1, then Myrrhine across the road
  L.go(20, 14)
  local _, _, b = L.grid().tile(20, 14)
  expect(b == S.MB_TALL_GRASS, "the forced band: tall grass across the road among the tombs")
  L.shot("band_1")
  L.go(27, 14)
  expect(L.defeated(S.TRAINER_MYRRHINE), "Myrrhine stops the road past the band (mandatory)")
  heal()
  read(L.sign(P .. "ForkSign"), "the fork sign", { shots = { [1] = "sign_fork" } })
end

local function herm()
  L.setBeat("herm", false)
  -- Laas stands on the herm's step: the herm can't be reached past him
  expect(L.npc(P .. "Laas").present, "a Titanborn guards the herm")
  fight("Laas", S.TRAINER_LAAS, "Laas")
  L.settle()
  expect(L.getFlag(S.FLAG_HIDE_GRUNT_LAAS) and not L.npc(P .. "Laas").present, "Laas runs off after the battle")
  L.talk(L.sign(P .. "GreatHerm"), { every = true, shots = { [1] = "herm_desecrated" } })
  expect(L.getFlag(S.FLAG_ALTAR_ROUTE4), "a prayer cleanses the herm (desecrated altar 0)")
  L.talk(L.sign(P .. "GreatHerm"), { every = true })
  expect(L.getFlag(S.FLAG_HERM_ROUTE4), "the great herm anointed (HERM_AETHOS_ROUTE_4)")
  L.shot("herm_anointed")
end

local function spur()
  L.setBeat("spur", false)
  fight("Menalkas", S.TRAINER_MENALKAS, "Menalkas (optional)")
  read(L.npc(P .. "Menalkas"), "Menalkas after")
  read(L.npc(P .. "Goat"), "a goat")
  item(S.FLAG_ITEM_SUPER_POTION, "the spur's Super Potion")
  arachneDig("DigSpur", S.FLAG_DIG_SPUR, 0x1D)
  -- the orchard is shut by its thicket until Demeter's Sickle
  local thicket = L.npc("EventScript_CutTree")
  read(thicket, "the thicket without the Sickle", { shots = { [1] = "thicket_shut" } })
  expect(L.npc("EventScript_CutTree").present, "the thicket stays without the Sickle")
  L.shot("orchard_shut")
end

-- --- The pass: band 2, the cutting, beat 17 -----------------------------------------------------

local function pass()
  L.setBeat("pass", false)
  repel()
  L.go(35, 11)
  local _, _, b = L.grid().tile(35, 11)
  expect(b == S.MB_TALL_GRASS, "the second forced band, on the rise")
  L.go(44, 10)
  expect(L.defeated(S.TRAINER_PHEIDIPPOS), "Pheidippos stops the cutting (mandatory)")
  heal()
  L.shot("cutting")
  -- the heaps say what they need before the scene (none reachable yet: the trigger first)
  local fired = not L.goTrigger(L.triggers(P .. "RockslideScene"))
  expect(fired, "beat 17's first scene starts 4 tiles short of the slide")
  L.settle({ every = true })
  expect(L.getFlag(S.FLAG_SAW_ROCKSLIDE), "the slide's scene plays once (FLAG_ICHOR_SAW_ROCKSLIDE)")
  L.shot("slide_scene_after")
end

local function camp()
  L.setBeat("camp", false)
  for _, who in ipairs({ "Alethea", "Eudemos", "InitiateWait", "InitiateDonkey", "InitiateSecret", "Donkey" }) do
    read(L.npc(P .. who), who, { shots = { [1] = "camp_" .. who } })
  end
  read(L.npc(P .. "Healer"), "the procession's healer", { shots = { [1] = "healer" } })
  fight("Kapelos", S.TRAINER_KAPELOS, "Kapelos (optional)")
  read(L.npc(P .. "Kapelos"), "Kapelos after")
  hidden(S.FLAG_HIDDEN_STARDUST, "the Stardust by the cookfire")
  L.shot("camp")
end

-- --- The lower terrace: the lips, the plots, the wild grass ------------------------------------

local function lower()
  L.setBeat("lower", false)
  repel()
  -- down the terrace lips from the camp (one way, toward the city)
  L.go(50, 18)
  expect(L.mapId() == S.MAP_ROUTE4, "down the lips to the lower terrace")
  L.shot("lower_terrace")
  hidden(S.FLAG_HIDDEN_HARD_STONE, "the Hard Stone in the scree")
  hidden(S.FLAG_HIDDEN_ORAN, "the Oran Berry by the milestone")
  item(S.FLAG_ITEM_REPEL, "the Repel in the walled plot")
  read(L.npc("EventScript_StrengthBoulder"), "the drum without the Girdle", { shots = { [1] = "drum_shut" } })
  expect(not L.getFlag(S.FLAG_ITEM_REVIVE), "the family tomb stays shut without the Girdle")
  expect(not L.getFlag(S.FLAG_DIG_TOMB), "the Girdle-gated tomb find is still unclaimed")
  -- a wild Pokemon from Route 4's table in the east meadow
  local names = {}
  for _, n in ipairs({ "EPOPOI", "LOPHOPS", "ONOTIS", "KERAZAP", "GALEKIT", "CHELONET", "ERGANT", "ELALEAF",
                       "SPALUNK", "HARPECK", "NEMECUB", "PEBBLITH", "OBOLORN" }) do
    names[S["SPECIES_" .. n]] = n
  end
  L.go(50, 21)
  L.setVar(S.VAR_REPEL_STEP_COUNT, 0)
  local met
  for i = 1, 400 do
    local r = L.step((i % 2 == 0) and K.LEFT or K.RIGHT)
    if r == "taken" or L.inBattle() then
      L.waitUntil(L.inBattle, 1200, "the wild battle")
      L.wait(120)
      local species = emu:read16(S.gBattleMons + S.BATTLE_MON_SIZE + S.OFF_BATTLE_MON_SPECIES)
      local level = emu:read8(S.gBattleMons + S.BATTLE_MON_SIZE + S.OFF_BATTLE_MON_LEVEL)
      met = names[species] or ("species " .. species)
      L.shot("wild_on_route4")
      expect(names[species] ~= nil and level >= 16 and level <= 19,
             string.format("a wild %s, level %d, from Route 4's table", met, level))
      L.settle()
      break
    end
  end
  expect(met ~= nil, "a wild Pokemon met in Route 4's grass")
  repel()
end

-- --- The rockslide, the procession's thanks, the Hollow ----------------------------------------

local function slide()
  L.setBeat("slide", false)
  repel()
  for i, h in ipairs({ { 52, 9 }, { 53, 9 }, { 54, 9 } }) do
    expect(tile(h[1], h[2]) == S.MT_RUBBLE_SMALL, string.format("heap %d lies on the road at (%d,%d)", i, h[1], h[2]))
    L.talk(h[1], h[2], { every = i == 3, shotBefore = "heap_" .. i })
    expect(L.getFlag(S["FLAG_HIDE_ROCKSLIDE_" .. i]), string.format("heap %d broken with the Hammer", i))
    if i < 3 then
      expect(tile(h[1], h[2]) == S.MT_RUBBLE_SMALL_CLEARED, string.format("heap %d's cell is open road", i))
    end
  end
  expect(L.getFlag(S.FLAG_ROCKSLIDE_CLEARED), "the road is clear (FLAG_ICHOR_ROCKSLIDE_CLEARED)")
  expect(L.getFlag(S.FLAG_GOT_PROCESSION_BARLEY) and L.itemCount(S.ITEM_BARLEY_CAKE) == 2,
         string.format("Eudemos's Barley Cakes (%d in the bag)", L.itemCount(S.ITEM_BARLEY_CAKE)))
  expect(L.getFlag(S.FLAG_ITEM_TM_ROCK_TOMB) and L.itemCount(S.ITEM_TM39) >= 1, "TM39 Rock Tomb from under the last heap")
  expect(tile(52, 8) ~= S.MT_RUBBLE_TOP_LEFT and tile(52, 10) ~= S.MT_RUBBLE_TOP_LEFT, "the slide's big heaps are gone too")
  L.shot("road_clear")
  read(L.npc(P .. "Eudemos"), "Eudemos after")
  -- the Hollow's mouth
  read(L.sign(P .. "HollowSign"), "the Hollow's name stone", { shots = { [1] = "sign_hollow" } })
  L.go(57, 8)
  L.shot("hollow_mouth")
  local dest = L.mapEvents().warps[1].map
  L.setVar(S.VAR_TEMP_5, 77)
  emu:addKey(K.UP)
  L.waitUntil(function() return L.mapId() ~= S.MAP_ROUTE4 or L.getVar(S.VAR_TEMP_5) ~= 77 end, 600, "the Hollow's mouth")
  emu:clearKey(K.UP)
  L.waitUntil(L.idle, 900, "control after the mouth")
  L.wait(20)
  if dest == S.MAP_ROUTE4 then
    L.note("MAP_HECATES_HOLLOW isn't registered: the mouth warps back onto itself (ICHOR_STUB_HOLLOW)")
    local x, y = L.pos()
    expect(L.mapId() == S.MAP_ROUTE4 and x == 57, string.format("through the mouth and back out (at %d,%d)", x, y))
  else
    expect(L.mapId() == dest, "into Hecate's Hollow")
    L.useWarp(S.MAP_ROUTE4)
  end
  -- the procession has moved on: the camp is struck
  expect(L.getFlag(S.FLAG_HIDE_PROCESSION) and not L.npc(P .. "Alethea").present, "the procession has moved on")
  L.shot("camp_struck")
end

-- --- Act II's relics open the orchard and the family tomb --------------------------------------

local function relics()
  L.setBeat("relics", false)
  repel()
  addItems({ { S.ITEM_DEMETERS_SICKLE, 1 }, { S.ITEM_GIRDLE_OF_HERAKLES, 1 } })
  L.talk(L.npc("EventScript_CutTree"))
  expect(not L.npc("EventScript_CutTree").present, "the Sickle cuts the orchard's thicket")
  item(S.FLAG_ITEM_SUN_STONE, "the orchard's Sun Stone")
  L.shot("orchard")
  -- the family tomb: brace with the Girdle, push the drum in, take the Revive
  L.talk(L.npc("EventScript_StrengthBoulder"))
  L.go(42, 24)
  for _ = 1, 4 do L.tap(K.UP, 12); L.wait(30); L.settle() end
  local x, y = L.pos()
  expect(y <= 22, string.format("the drum pushed in and the tomb entered (at %d,%d)", x, y))
  item(S.FLAG_ITEM_REVIVE, "the tomb's Revive")
  arachneDig("DigTomb", S.FLAG_DIG_TOMB)
  L.shot("tomb_open")
end

local function omenVisitor()
  L.setBeat("visitor", false)
  local kind = emu:read8(L.ichor() + S.OFF_ICHOR_OMEN_KIND)
  local entry = emu:read16(L.ichor() + S.OFF_ICHOR_OMEN_ENTRY)
  local noRunning = L.getFlag(S.FLAG_NO_RUNNING)
  local script = P .. "OmenNemecub"
  local function setOmen(k, e)
    emu:write8(L.ichor() + S.OFF_ICHOR_OMEN_KIND, k)
    emu:write16(L.ichor() + S.OFF_ICHOR_OMEN_ENTRY, e)
  end
  local function reload()
    warpTo(S.MAP_EMPORION, 8, 8)
    warpTo(S.MAP_ROUTE4, 26, 3)
  end
  setOmen(S.OMEN_GOOD_SIGN, S.OMEN_LUCKY_THREE)
  L.setFlag(S.FLAG_OMEN_NEMECUB, false)
  reload()
  expect(not L.npc(script).present, "no off-day golden cub, even with an unset legacy hide flag")
  setOmen(S.OMEN_VISITOR, S.OMEN_NEMECUB)
  L.setFlag(S.FLAG_OMEN_NEMECUB, false)
  reload()
  expect(L.npc(script).present, "the matching omen places the golden cub on the hill spur")
  L.shot("nemecub_on_the_spur")
  local visitor = L.npc(script).tiles[1]
  L.go(visitor.x - 1, visitor.y)
  expect(emu:saveStateFile(L.OUT .. "before_visitor.ss", 31), "saved the uncaught golden-cub state")
  giveLead(1)
  L.setFlag(S.FLAG_NO_RUNNING, true)
  L.talk(L.npc(script))
  expect(L.battles[#L.battles].outcome == S.B_OUTCOME_LOST
         and not L.getFlag(S.FLAG_OMEN_NEMECUB) and not L.getFlag(S.FLAG_CTRL_OBJ_DELETE),
         "losing does not consume the golden cub or leave object-delete control set")
  expect(emu:loadStateFile(L.OUT .. "before_visitor.ss", 31), "restored the uncaught golden-cub state")
  L.wait(20)
  L.setFlag(S.FLAG_NO_RUNNING, false)
  L.talk(L.npc(script), { stop = L.inBattle, every = true })
  L.wait(120)
  expect(emu:read16(S.gBattleMons + S.BATTLE_MON_SIZE + S.OFF_BATTLE_MON_SPECIES) == S.SPECIES_NEMECUB
         and emu:read8(S.gBattleMons + S.BATTLE_MON_SIZE + S.OFF_BATTLE_MON_LEVEL) == 18,
         "the golden cub starts a real level-18 Nemecub encounter")
  local ran = L.battle()
  L.settle()
  expect(ran.outcome == S.B_OUTCOME_RAN and not L.getFlag(S.FLAG_OMEN_NEMECUB),
         "running keeps today's golden cub available")
  reload()
  expect(L.npc(script).present, "the uncaught golden cub survives reentry")
  L.setFlag(S.FLAG_NO_RUNNING, true)
  L.talk(L.npc(script))
  expect(L.battles[#L.battles].outcome == S.B_OUTCOME_WON
         and L.getFlag(S.FLAG_OMEN_NEMECUB) and not L.npc(script).present,
         "defeating the golden cub saves its hide state and removes the object")
  reload()
  expect(not L.npc(script).present, "same-day reentry cannot respawn the defeated cub")
  L.setFlag(S.FLAG_OMEN_NEMECUB, false)
  reload()
  local battles = #L.battles
  setOmen(S.OMEN_GOOD_SIGN, S.OMEN_LUCKY_THREE)
  L.talk(L.npc(script))
  expect(#L.battles == battles and not L.npc(script).present,
         "an on-map day change prevents an expired golden-cub battle")
  setOmen(S.OMEN_VISITOR, S.OMEN_NEMECUB)
  L.setFlag(S.FLAG_OMEN_NEMECUB, false)
  reload()
  local code = { S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 } }
  local key = emu:read32(L.sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
  for i = 0, S.BAG_POKEBALLS_COUNT - 1 do
    local slot = L.sb1() + S.OFF_SB1_POKEBALLS + i * S.ITEM_SLOT_SIZE
    local item = emu:read16(slot)
    if item ~= 0 then
      code[#code + 1] = S.SCR_OP_REMOVEITEM
      code[#code + 1] = { item, 2 }
      code[#code + 1] = { emu:read16(slot + S.OFF_ITEM_SLOT_QUANTITY) ~ key, 2 }
    end
  end
  code[#code + 1] = S.SCR_OP_ADDITEM
  code[#code + 1] = { S.ITEM_MASTER_BALL, 2 }
  code[#code + 1] = { 1, 2 }
  code[#code + 1] = S.SCR_OP_END
  L.setVar(S.VAR_TEMP_0, 0)
  L.runRamScript(code)
  L.settle()
  expect(L.itemCount(S.ITEM_MASTER_BALL) == 1, "the golden-cub capture has one real Master Ball")
  L.talk(L.npc(script), { stop = L.inBattle })
  L.waitUntil(function()
    if emu:read32(S.gBattlerControllerFuncs) == (S.HandleInputChooseAction | 1) then return true end
    L.tap(K.A); L.wait(4)
    return false
  end, 1200, "the golden-cub battle action menu")
  L.tap(K.UP); L.tap(K.RIGHT); L.tap(K.A)
  L.waitUntil(function() return L.taskRunning("Task_BagMenu_HandleInput") end, 1200, "the golden-cub battle Bag")
  L.wait(30)
  for i = 1, S.POCKETS_COUNT do
    if emu:read8(S.gBagPosition + S.OFF_BAG_POSITION_POCKET) == S.POCKET_POKE_BALLS then break end
    L.tap(K.RIGHT); L.wait(50)
  end
  expect(emu:read8(S.gBagPosition + S.OFF_BAG_POSITION_POCKET) == S.POCKET_POKE_BALLS,
         "the golden-cub battle Bag opens the Poke Ball pocket")
  L.tap(K.UP); L.tap(K.UP); L.tap(K.A); L.wait(20); L.tap(K.A)
  L.waitUntil(function()
    if L.inOverworld() then return true end
    if L.on("CB2_NamingScreen") then L.acceptName("caught_nemecub") else L.tap(K.A); L.wait(4) end
    return false
  end, 12000, "the golden-cub capture and return to the spur")
  L.settle()
  expect(emu:read8(S.gBattleOutcome) == S.B_OUTCOME_CAUGHT
         and emu:read8(S.gPartiesCount) == 2 and L.itemCount(S.ITEM_MASTER_BALL) == 0
         and L.getFlag(S.FLAG_OMEN_NEMECUB) and not L.npc(script).present,
         "an actual capture adds Nemecub, consumes the ball and removes the visitor")
  reload()
  expect(not L.npc(script).present, "same-day reentry cannot respawn the captured cub")
  setOmen(kind, entry)
  L.setFlag(S.FLAG_NO_RUNNING, noRunning)
  reload()
end

L.start(function()
  setup()
  potters()
  tombs()
  herm()
  spur()
  pass()
  camp()
  lower()
  slide()
  relics()
  omenVisitor()
  L.log("ok the walk is done")
end)
