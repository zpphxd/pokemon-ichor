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

-- A level-100 lead, written into party slot 0 (personality and OT id 0, so the
-- box data's substructs sit in order unencrypted), then raised by slice_lib's assist.
local function giveLead()
  local mon = L.partyMon(0)
  for o = 0, S.POKEMON_SIZE - 1 do emu:write8(mon + o, 0) end
  for k, b in ipairs({ 0xCE, 0xBF, 0xCD, 0xCE, 0xFF }) do emu:write8(mon + 7 + k, b) end -- "TEST"
  emu:write8(mon + 18, 2)
  emu:write8(mon + 19, 0x02)
  emu:write8(mon + 20, 0xFF)
  emu:write16(mon + S.OFF_BOXMON_SECURE, S.SPECIES_LEAD & 0x7FF)
  local sum = 0
  for o = 0, 47, 2 do sum = sum + emu:read16(mon + S.OFF_BOXMON_SECURE + o) end
  emu:write16(mon + S.OFF_BOXMON_CHECKSUM, sum & 0xFFFF)
  emu:write8(mon + S.OFF_MON_LEVEL, 5)
  emu:write8(S.gPartiesCount, 1)
  L.assistLevel100()
  local hp, maxhp = L.partyHp(0)
  expect(L.partyLevel(0) == S.MAX_LEVEL and hp > 0, string.format("a level-100 lead (HP %d/%d)", hp, maxhp))
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

-- --- The village ---------------------------------------------------------------------------

local function village()
  L.setBeat("village", false)
  -- a repel for the walk round the village: the wheat's wild Pokemon are wheat()'s check
  L.setVar(S.VAR_REPEL_STEP_COUNT, 999)
  warpTo(S.MAP_ELEUSA, 1, 25)
  expect(L.mapMusic() == S.MUS_ELEUSA, "Eleusa plays MUS_ICHOR_ELEUSA")
  L.shot("west_gate")
  -- everyone in the village
  for _, who in ipairs({ "Krokis", "WaterCarrier", "Kid", "Kopros", "Dysaules", "Eubouleus", "Hoplite" }) do
    talk(L.npc(V .. who), who, { shots = { [1] = "talk_" .. who } })
  end
  -- every sign and thing to read
  for _, s in ipairs({ "VillageSign", "SanctuarySign", "TempleSign", "PloutonionSign", "NorthRoadSign",
                       "RharianSign", "WellBench", "Beehives", "FieldShrine", "DigSpot" }) do
    talk(L.sign(V .. s), s, { shots = { [1] = "read_" .. s } })
  end
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
  local x, y = L.pos()
  warpTo(S.MAP_ELEUSA, x, y)
  L.useWarp(S.MAP_E_SANCTUM_B1F)
  expect(L.mapId() == S.MAP_E_SANCTUM_B1F, "and open once FLAG_ICHOR_SANCTUM_OPEN is set")
  L.useWarp(S.MAP_ELEUSA)
  L.setFlag(S.FLAG_SANCTUM_OPEN, false)
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

L.start(function()
  L.quickstart()
  giveLead()
  village()
  doors()
  wheat()
  temple()
  L.log("ok the walk is done")
end)
