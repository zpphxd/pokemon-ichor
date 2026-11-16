-- Eleusa Village and the Temple of Demeter, run by tools/ichor/tests/eleusa.sh (read it first).
--
-- Plays with key presses on tools/ichor/tests/engine_lib.lua (slice_lib's walker:
-- a breadth-first search over the live map, one step at a time). People, signs,
-- items and doors are found by the script they run or the flag they set, so a
-- moved NPC never breaks the walk; a missing one fails with its name.
--
-- Prints "ELEUSA ok ..." per check and "ELEUSA shot ..." per screenshot, and ends
-- with "ELEUSA done"; any failure prints "ELEUSA FAIL: ..." first.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
for k, v in pairs(dofile(L.OUT .. "eleusa_symbols.lua")) do
  if k == "SCRIPTS" then
    for n, a in pairs(v) do S.SCRIPTS[n] = a end
  else
    S[k] = v
  end
end

local V = "EleusaVillage_EventScript_"
local T = "EleusaVillage_TempleOfDemeter_EventScript_"
local VOID = 0x20D                       -- the temple's pits (temple_demeter: floor.void)

local function expect(cond, what) L.expect(cond, what) end

-- Warp to (x, y) on `map` from an ON_FRAME script in spare EWRAM.
local function warpTo(map, x, y)
  L.setVar(S.VAR_TEMP_0, 0)            -- the frame script runs while VAR_TEMP_0 is 0
  L.runRamScript({ S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 },
                   S.SCR_OP_WARP, map >> 8, map & 0xFF, 0xFF, { x, 2 }, { y, 2 }, S.SCR_OP_WAITSTATE, S.SCR_OP_END })
  L.waitUntil(function() return L.mapId() == map and L.idle() end, 3000, "the warp to map " .. map)
  L.wait(30)
end

-- Use the engine's own creation/move commands, as the Emporion walk does.
local function giveLead(level)
  level = level or 100
  local creationLevel = level == S.MAX_LEVEL and 5 or level
  for i = 0, S.PARTY_SIZE - 1 do
    for o = 0, S.POKEMON_SIZE - 1 do emu:write8(L.partyMon(i) + o, 0) end
  end
  emu:write8(S.gPartiesCount, 0)
  L.setVar(S.VAR_TEMP_0, 0)
  L.runRamScript({ S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 },
                   S.SCR_OP_CALLNATIVE, { S.ScrCmd_createmon | 1, 4 }, 0, S.PARTY_SIZE,
                   { S.SPECIES_LEAD, 2 }, { creationLevel, 2 }, { 0, 4 },
                   S.SCR_OP_SETMONMOVE, 0, 0, { S.MOVE_FLAMETHROWER, 2 }, S.SCR_OP_END })
  L.settle()
  if level == S.MAX_LEVEL then
    -- Obedience uses met level, so create at 5 and reuse the existing strength assist.
    L.setVar(S.VAR_TEMP_0, 0)
    L.assistLevel100()
    L.settle()
  end
  local hp, maxhp = L.partyHp(0)
  expect(L.partyLevel(0) == level and hp > 0, string.format("a level-%d lead (HP %d/%d)", level, hp, maxhp))
  -- Hecate's Torch (the braziers are the engine's, and want it), and the story's
  -- trainers counted beaten: this walk checks the places; temple_demeter.sh plays the story.
  L.setFlag(S.FLAG_GOT_HECATES_TORCH, true)
  for _, t in ipairs({ "TRAINER_EUBOULEUS", "TRAINER_KALLIDIKE", "TRAINER_EUMOLPOS", "TRAINER_MELISSA" }) do
    L.setFlag(S.TRAINER_FLAGS_START + S[t], true)
  end
end

local function paletteTagLoaded(tag)
  for i = 0, 15 do
    if emu:read16(S.sSpritePaletteTags + 2 * i) == tag then return true end
  end
  return false
end

local function talk(target, what, opts)
  local boxes = L.talk(target, opts)
  expect((boxes or 0) >= 1, string.format("%s: %d message box(es)", what, boxes or 0))
  return boxes
end

local function flash() return emu:read8(L.sb1() + S.OFF_SB1_FLASH) end

local function bagCounts()
  local counts = {}
  local encryptionKey = emu:read32(L.sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
  for i = 0, S.BAG_SLOTS - 1 do
    local slot = L.sb1() + S.OFF_SB1_BAG + i * S.ITEM_SLOT_SIZE
    local item = emu:read16(slot)
    counts[item] = (counts[item] or 0) + (emu:read16(slot + S.OFF_ITEM_SLOT_QUANTITY) ~ encryptionKey)
  end
  return counts
end

local function collectibleFlags()
  local flags = {}
  for i = 0, 3 do flags[S.FLAG_PERSEPHONE_SHERDS + i] = L.getFlag(S.FLAG_PERSEPHONE_SHERDS + i) end
  for i = 0, 29 do flags[S.FLAG_OSTRAKA + i] = L.getFlag(S.FLAG_OSTRAKA + i) end
  return flags
end

local function dig(name, flag)
  local before, flagsBefore = bagCounts(), collectibleFlags()
  talk(L.sign(V .. name), name, { every = true })
  local find = emu:read16(S.sDig + S.OFF_DIG_FIND)
  local quantity = emu:read8(S.sDig + S.OFF_DIG_QUANTITY)
  expect(L.getFlag(flag), name .. " records its own daily excavation")
  if find < S.ITEMS_COUNT then
    expect(quantity >= 1 and L.itemCount(find) == (before[find] or 0) + quantity, name .. " grants its actual item and quantity")
  else
    local foundFlag = emu:read16(S.sDig + S.OFF_DIG_FIND_FLAG)
    expect(flagsBefore[foundFlag] == false and L.getFlag(foundFlag),
           name .. " grants a new Persephone sherd or ostrakon, not another area's sherd")
  end
  local after, flagsAfter = bagCounts(), collectibleFlags()
  talk(L.sign(V .. name), name .. "_again")
  local unchanged = true
  local repeated = bagCounts()
  for item, quantityAfter in pairs(after) do
    if repeated[item] ~= quantityAfter then unchanged = false end
  end
  for item, quantityAfter in pairs(repeated) do
    if after[item] ~= quantityAfter then unchanged = false end
  end
  for f, set in pairs(flagsAfter) do if L.getFlag(f) ~= set then unchanged = false end end
  expect(unchanged, name .. " gives nothing extra on the same day")
  return find
end

-- --- The village ---------------------------------------------------------------------------

local function village()
  L.setBeat("village", false)
  warpTo(S.MAP_ELEUSA, 1, 25)
  -- a repel for the walk round the village: the wheat's wild Pokemon are
  -- wheat()'s to meet, and one jumping out on the way to a person can leave
  -- the talk that follows pressing A into nothing
  L.setVar(S.VAR_REPEL_STEP_COUNT, 2000)
  expect(L.mapMusic() == S.MUS_ELEUSA, "Eleusa plays MUS_ICHOR_ELEUSA")
  L.shot("west_gate")
  -- everyone in the village
  for _, who in ipairs({ "Krokis", "WaterCarrier", "Kid", "Kopros", "Dysaules", "Eubouleus", "Hoplite" }) do
    talk(L.npc(V .. who), who, { shots = { [1] = "talk_" .. who } })
  end
  -- every sign and thing to read
  for _, s in ipairs({ "VillageSign", "SanctuarySign", "TempleSign", "PloutonionSign", "NorthRoadSign",
                       "RharianSign", "WellBench", "Beehives", "DigSpotWest", "DigSpotEast" }) do
    talk(L.sign(V .. s), s, { shots = { [1] = "read_" .. s } })
  end
  expect(not L.getFlag(S.FLAG_DIG_WEST) and not L.getFlag(S.FLAG_DIG_EAST),
         "both fields stay undug without the actual Trowel")
  local favorBefore = emu:read8(L.ichor() + S.OFF_ICHOR_FAVOR + S.GOD_DEMETER)
  L.talk(L.sign(V .. "FieldShrine"), { answers = { 4 }, every = true })
  expect(emu:read8(L.ichor() + S.OFF_ICHOR_FAVOR + S.GOD_DEMETER) == favorBefore,
         "leaving Demeter's field-shrine menu grants no Favor")
  L.talk(L.sign(V .. "FieldShrine"), { answers = { 0 }, every = true })
  expect(emu:read8(L.ichor() + S.OFF_ICHOR_FAVOR + S.GOD_DEMETER) == favorBefore + 1
         and emu:read8(L.ichor() + S.OFF_ICHOR_BLESSING) == S.GOD_DEMETER,
         "the field shrine's actual prayer grants Demeter Favor and her blessing")
  L.talk(L.sign(V .. "FieldShrine"), { answers = { 0 } })
  expect(emu:read8(L.ichor() + S.OFF_ICHOR_FAVOR + S.GOD_DEMETER) == favorBefore + 1,
         "a repeated field-shrine prayer does not farm daily Favor")
  L.setVar(S.VAR_TEMP_0, 0)
  L.runRamScript({ S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 },
                   S.SCR_OP_ADDITEM, { S.ITEM_TROWEL, 2 }, { 1, 2 }, S.SCR_OP_END })
  L.settle()
  expect(L.itemCount(S.ITEM_TROWEL) == 1, "the field-dig fixture receives one real Trowel")
  dig("DigSpotWest", S.FLAG_DIG_WEST)
  expect(not L.getFlag(S.FLAG_DIG_EAST), "digging the west field leaves the east field available")
  local savedSeed = emu:read32(L.sb1() + S.OFF_SB1_DAILY_SEED)
  -- Both first rolls are sherds, with or without Demeter's blessing.
  emu:write32(L.sb1() + S.OFF_SB1_DAILY_SEED, 0x3C)
  expect(dig("DigSpotEast", S.FLAG_DIG_EAST) == S.FIND_PERSEPHONE_SHERD
         and L.getFlag(S.FLAG_PERSEPHONE_SHERDS),
         "the east field's real sherd belongs to Persephone's amphora")
  emu:write32(L.sb1() + S.OFF_SB1_DAILY_SEED, savedSeed)
  -- the items, visible and hidden
  for _, f in ipairs({ "FLAG_ITEM_SUPER_POTION", "FLAG_ITEM_AWAKENING" }) do
    L.talk(L.ball(S[f]))
    expect(L.getFlag(S[f]), f .. " taken")
  end
  for _, f in ipairs({ "FLAG_HIDDEN_HONEY", "FLAG_HIDDEN_POMEG", "FLAG_HIDDEN_OBOL" }) do
    L.talk(L.hidden(S[f]))
    expect(L.getFlag(S[f]), f .. " found")
  end
end

local function doors()
  L.setBeat("doors", false)
  L.setVar(S.VAR_REPEL_STEP_COUNT, 250)
  for _, m in ipairs({ "MAP_E_ASCLEPEION", "MAP_E_AGORA", "MAP_E_KELEOS", "MAP_E_GRANARY",
                       "MAP_E_POETS", "MAP_E_FARMHOUSE" }) do
    L.useWarp(S[m])
    expect(L.mapId() == S[m], "through the door into " .. m)
    L.useWarp(S.MAP_ELEUSA)
    expect(L.mapId() == S.MAP_ELEUSA, "and back out of " .. m)
  end
  L.shot("back_from_the_doors")
  -- the Ploutonion's bronze gate is shut until the sanctum opens
  local gate = { tiles = { { x = 31, y = 8 } }, what = "the Ploutonion's gate" }
  L.talk(L.sign(V .. "PloutonionSign"))
  L.go(31, 9)
  L.tap(K.UP, 8); L.wait(40)
  expect(L.mapId() == S.MAP_ELEUSA, "the Ploutonion is shut before the sanctum opens")
  L.shot("ploutonion_shut")
  L.setFlag(S.FLAG_SANCTUM_OPEN, true)
  -- in play the Mysteries bring the player down the Anaktoron's stair first, so
  -- B1F's arrival scene has played before anyone uses the Ploutonion's gate
  L.setFlag(S.FLAG_SANCTUM_ARRIVED, true)
  local x, y = L.pos()
  warpTo(S.MAP_ELEUSA, x, y)
  L.useWarp(S.MAP_E_SANCTUM_B1F)
  expect(L.mapId() == S.MAP_E_SANCTUM_B1F, "and open once FLAG_ICHOR_SANCTUM_OPEN is set")
  L.useWarp(S.MAP_ELEUSA)
  L.setFlag(S.FLAG_SANCTUM_OPEN, false)
  L.setFlag(S.FLAG_SANCTUM_ARRIVED, false)
  local _ = gate
end

local function wheat()
  L.setBeat("wheat", false)
  -- the north-west field's heart: a repel keeps the walk in quiet
  L.setVar(S.VAR_REPEL_STEP_COUNT, 250)
  L.go(13, 10)
  local mid, _, b = L.grid().tile(13, 10)
  expect(b == S.MB_TALL_GRASS, string.format("standing in the wheat (metatile 0x%03X)", mid or 0))
  -- a step to the east into wheat, photographed as the stalks part
  emu:addKey(K.RIGHT)
  for n = 1, 6 do
    L.wait(n == 1 and 4 or 5)
    if n == 2 then emu:clearKey(K.RIGHT) end
    L.shot(string.format("wheat_rustle_%d", n))
  end
  expect(paletteTagLoaded(S.FLDEFF_PAL_TAG_WHEAT), "the rustle draws from the wheat's own palette")
  L.wait(30)
  -- without the repel, a wild Pokemon of Eleusa's fields comes out of the wheat
  L.setVar(S.VAR_REPEL_STEP_COUNT, 0)
  local table_ = {}
  for _, n in ipairs({ "STACHYSS", "MELIBEE", "KAPLET", "SPALUNK", "ELALEAF", "LOPHOPS", "EPOPOI",
                       "GELASABLE", "GALEKIT", "KERAZAP", "ONOTIS", "RHOARIL" }) do
    table_[S["SPECIES_" .. n]] = n
  end
  local met
  for i = 1, 300 do
    local key = (i % 2 == 0) and K.LEFT or K.RIGHT
    local r = L.step(key)
    if r == "taken" or L.inBattle() then
      L.waitUntil(L.inBattle, 1200, "the wild battle")
      L.wait(120)
      local species = emu:read16(S.gBattleMons + S.BATTLE_MON_SIZE + S.OFF_BATTLE_MON_SPECIES)
      local level = emu:read8(S.gBattleMons + S.BATTLE_MON_SIZE + S.OFF_BATTLE_MON_LEVEL)
      met = table_[species] or ("species " .. species)
      L.shot("wild_in_the_wheat")
      expect(table_[species] ~= nil and level >= 19 and level <= 22,
             string.format("a wild %s, level %d, from Eleusa's table", met, level))
      L.settle()
      break
    end
  end
  expect(met ~= nil, "a wild Pokemon met in the wheat")
  L.setVar(S.VAR_REPEL_STEP_COUNT, 250)
end

-- --- The Telesterion -------------------------------------------------------------------------

local function noPits(x, y)
  local mid = L.grid().tile(x, y)
  return mid == VOID
end
local function opts(t) t = t or {}; t.avoid = noPits; return t end

local function temple()
  L.setBeat("temple", false)
  L.useWarp(S.MAP_TEMPLE_DEMETER)
  expect(L.mapId() == S.MAP_TEMPLE_DEMETER, "into the Telesterion")
  expect(L.mapMusic() == S.MUS_TEMPLE_DEMETER, "the Telesterion plays MUS_ICHOR_TEMPLE_DEMETER")
  expect(flash() == 3, string.format("the hall is dark: flash level %d (the Torch's 3)", flash()))
  L.shot("telesterion_entry")
  talk(L.npc(T .. "Doso"), "Doso's welcome", opts({ every = true }))
  expect(L.getFlag(S.FLAG_MET_DOSO), "Doso's welcome heard once")
  talk(L.npc(T .. "Doso"), "Doso's name", opts())
  -- out of turn: Spring won't take while Autumn is cold
  talk(L.sign(T .. "BrazierSpring"), "Spring, out of turn", opts({ shots = { [1] = "spring_out_of_turn" } }))
  expect(not L.getFlag(S.FLAG_BRAZIER_SPRING), "Spring stays cold out of turn")
  -- the trail: Autumn (Kallidike teaches), Winter (Eumolpos), Spring (Melissa), Summer
  for _, s in ipairs({ { "Autumn", "Kallidike" }, { "Winter", "Eumolpos" }, { "Spring", "Melissa" } }) do
    talk(L.npc(T .. s[2]), s[2], opts({ shots = { [1] = "talk_" .. s[2] } }))
    talk(L.sign(T .. "Brazier" .. s[1]), s[1] .. " lit", opts({ shots = { [3] = "lit_" .. s[1] } }))
    expect(L.getFlag(S["FLAG_BRAZIER_" .. string.upper(s[1])]), s[1] .. "'s flag set")
    expect(flash() == 0, s[1] .. "'s quarter is bright")
    L.shot("quarter_" .. s[1])
  end
  -- leaving a lit quarter for the aisle brings the dark back
  L.go(13, 15, opts())
  expect(flash() == 3, string.format("the aisle is dark again (flash %d)", flash()))
  -- a misstep into a grain pit drops the player onto the tiers by the Spring brazier
  L.go(15, 20, opts())
  L.tap(K.RIGHT, 8)
  L.settle()
  local px, py = L.pos()
  expect(L.mapId() == S.MAP_TEMPLE_DEMETER and px == 23 and py == 4,
         string.format("a pit drops you on the tiers by Spring (at %d,%d)", px, py))
  -- the master: along Hecate's chalk to Summer
  talk(L.sign(T .. "BrazierSummer"), "Summer lit", opts({ every = true }))
  expect(L.getFlag(S.FLAG_BRAZIER_SUMMER) and L.getFlag(S.FLAG_MYSTERIES_DONE),
         "Summer lit: the Lesser Mysteries done")
  L.shot("summer_lit")
  local chloe = L.npc(T .. "Chloe")
  expect(chloe.present, "Chloe stands in the Anaktoron's doorway")
  -- (her battle and the Laurel are temple_demeter.sh's)
  L.go(13, 24, opts())
  L.shot("hall_lit")
  L.useWarp(S.MAP_ELEUSA)
  expect(L.mapId() == S.MAP_ELEUSA, "back up the stair to the village")
end

local function omenVisitor()
  L.setBeat("visitor", false)
  local kind = emu:read8(L.ichor() + S.OFF_ICHOR_OMEN_KIND)
  local entry = emu:read16(L.ichor() + S.OFF_ICHOR_OMEN_ENTRY)
  local noRunning = L.getFlag(S.FLAG_NO_RUNNING)
  local function reloadVillage()
    warpTo(S.MAP_TEMPLE_DEMETER, 13, 24)
    warpTo(S.MAP_ELEUSA, 16, 34)
  end
  local function setOmen(k, e)
    emu:write8(L.ichor() + S.OFF_ICHOR_OMEN_KIND, k)
    emu:write16(L.ichor() + S.OFF_ICHOR_OMEN_ENTRY, e)
  end
  -- An older save has no new hide flag. That must not reveal an off-day visitor.
  setOmen(S.OMEN_GOOD_SIGN, S.OMEN_LUCKY_THREE)
  L.setFlag(S.FLAG_OMEN_KORANTHA, false)
  reloadVillage()
  expect(not L.npc(V .. "OmenKorantha").present, "no off-day visitor, even with an unset legacy hide flag")
  setOmen(S.OMEN_VISITOR, S.OMEN_KORANTHA)
  L.setFlag(S.FLAG_OMEN_KORANTHA, false)
  reloadVillage()
  expect(L.npc(V .. "OmenKorantha").present, "the matching omen reveals Korantha in the wheat")
  L.shot("korantha_in_the_wheat")
  local visitor = L.npc(V .. "OmenKorantha").tiles[1]
  L.go(visitor.x - 1, visitor.y)
  expect(emu:saveStateFile(L.OUT .. "before_visitor.ss", 31), "saved the uncaught visitor's entry state")
  giveLead(5)
  L.setFlag(S.FLAG_NO_RUNNING, true)
  L.talk(L.npc(V .. "OmenKorantha"))
  expect(L.battles[#L.battles].outcome == S.B_OUTCOME_LOST
         and not L.getFlag(S.FLAG_OMEN_KORANTHA) and not L.getFlag(S.FLAG_CTRL_OBJ_DELETE),
         "a loss does not consume the visitor or leave the field-delete control flag set")
  expect(emu:loadStateFile(L.OUT .. "before_visitor.ss", 31), "restored the uncaught visitor's entry state")
  L.wait(20)
  L.setFlag(S.FLAG_NO_RUNNING, false)
  L.talk(L.npc(V .. "OmenKorantha"), { stop = L.inBattle, every = true })
  L.wait(120)
  expect(emu:read16(S.gBattleMons + S.BATTLE_MON_SIZE + S.OFF_BATTLE_MON_SPECIES) == S.SPECIES_KORANTHA
         and emu:read8(S.gBattleMons + S.BATTLE_MON_SIZE + S.OFF_BATTLE_MON_LEVEL) == 22,
         "the visitor starts a real level-22 Korantha encounter")
  local ran = L.battle()
  L.settle()
  expect(ran.outcome == S.B_OUTCOME_RAN and not L.getFlag(S.FLAG_OMEN_KORANTHA),
         "running does not consume today's rare visitor")
  reloadVillage()
  expect(L.npc(V .. "OmenKorantha").present, "the uncaught visitor survives map reentry")
  L.setFlag(S.FLAG_NO_RUNNING, true)
  L.talk(L.npc(V .. "OmenKorantha"), { stop = L.inBattle })
  L.wait(120)
  expect(emu:read16(S.gBattleMons + S.OFF_BATTLE_MON_MOVES) == S.MOVE_FLAMETHROWER
         and emu:read8(S.gBattleMons + S.OFF_BATTLE_MON_PP) > 0,
         "the defeat fixture has a usable first-slot attack")
  L.battle()
  L.settle()
  expect(L.battles[#L.battles].outcome == S.B_OUTCOME_WON and L.getFlag(S.FLAG_OMEN_KORANTHA)
         and not L.npc(V .. "OmenKorantha").present,
         "defeating the visitor removes it and saves today's hide state")
  reloadVillage()
  expect(not L.npc(V .. "OmenKorantha").present, "the defeated visitor cannot respawn on same-day reentry")
  L.setFlag(S.FLAG_OMEN_KORANTHA, false)
  reloadVillage()
  expect(L.npc(V .. "OmenKorantha").present, "a later matching omen can send a new visitor")
  local battlesBeforeExpiry = #L.battles
  setOmen(S.OMEN_GOOD_SIGN, S.OMEN_LUCKY_THREE)
  L.talk(L.npc(V .. "OmenKorantha"))
  expect(#L.battles == battlesBeforeExpiry and not L.npc(V .. "OmenKorantha").present,
         "a day change while standing in the wheat cannot start an expired visitor encounter")
  setOmen(S.OMEN_VISITOR, S.OMEN_KORANTHA)
  L.setFlag(S.FLAG_OMEN_KORANTHA, false)
  reloadVillage()
  local script = { S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 } }
  local encryptionKey = emu:read32(L.sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
  for i = 0, S.BAG_POKEBALLS_COUNT - 1 do
    local slot = L.sb1() + S.OFF_SB1_POKEBALLS + i * S.ITEM_SLOT_SIZE
    local item = emu:read16(slot)
    if item ~= 0 then
      script[#script + 1] = S.SCR_OP_REMOVEITEM
      script[#script + 1] = { item, 2 }
      script[#script + 1] = { emu:read16(slot + S.OFF_ITEM_SLOT_QUANTITY) ~ encryptionKey, 2 }
    end
  end
  script[#script + 1] = S.SCR_OP_ADDITEM
  script[#script + 1] = { S.ITEM_MASTER_BALL, 2 }
  script[#script + 1] = { 1, 2 }
  script[#script + 1] = S.SCR_OP_END
  L.setVar(S.VAR_TEMP_0, 0)
  L.runRamScript(script)
  L.settle()
  expect(L.itemCount(S.ITEM_MASTER_BALL) == 1, "the capture fixture grants one real Master Ball")
  L.talk(L.npc(V .. "OmenKorantha"), { stop = L.inBattle })
  L.waitUntil(function()
    if emu:read32(S.gBattlerControllerFuncs) == (S.HandleInputChooseAction | 1) then return true end
    L.tap(K.A); L.wait(4)
    return false
  end, 1200, "the visitor's battle action menu")
  L.tap(K.UP); L.tap(K.RIGHT); L.tap(K.A) -- BAG
  L.waitUntil(function() return L.taskRunning("Task_BagMenu_HandleInput") end, 1200, "the battle Bag")
  L.wait(30)
  for i = 1, S.POCKETS_COUNT do
    if emu:read8(S.gBagPosition + S.OFF_BAG_POSITION_POCKET) == S.POCKET_POKE_BALLS then break end
    L.tap(K.RIGHT); L.wait(50)
  end
  expect(emu:read8(S.gBagPosition + S.OFF_BAG_POSITION_POCKET) == S.POCKET_POKE_BALLS,
         "the battle Bag opens the Poke Ball pocket")
  L.tap(K.UP); L.tap(K.UP); L.tap(K.A); L.wait(20); L.tap(K.A)
  L.waitUntil(function()
    if L.inOverworld() then return true end
    if L.on("CB2_NamingScreen") then L.acceptName("caught_korantha") else L.tap(K.A); L.wait(4) end
    return false
  end, 12000, "the Master Ball capture and return to the wheat")
  L.settle()
  expect(emu:read8(S.gBattleOutcome) == S.B_OUTCOME_CAUGHT
         and emu:read8(S.gPartiesCount) == 2 and L.itemCount(S.ITEM_MASTER_BALL) == 0
         and L.getFlag(S.FLAG_OMEN_KORANTHA) and not L.npc(V .. "OmenKorantha").present,
         "an actual capture consumes the ball, adds the visitor to the party and removes its object")
  reloadVillage()
  expect(not L.npc(V .. "OmenKorantha").present, "the captured visitor stays gone on same-day reentry")
  setOmen(kind, entry)
  L.setFlag(S.FLAG_NO_RUNNING, noRunning)
  reloadVillage()
end

L.start(function()
  L.quickstart()
  giveLead()
  village()
  doors()
  wheat()
  temple()
  omenVisitor()
  L.log("ok the walk is done")
end)
