-- Kythera's and Melos's trainers against design/phase4/SCRIPT.md Part 3 (see
-- act3_trainers.sh). The expected teams are read from the script itself, so a
-- change on either side shows up here.
--
-- 1. gTrainers, for every trainer in Part 3's Kythera section: class, name, AI,
--    items, and each Pokémon's species, level, held item, ability, IVs and moves.
-- 2. Battles, with two level-100 Metagross: Eudoros (an ordinary trainer) and
--    Galatea (Hierophant 7) started from a test script, and the bad guests,
--    Ochros and Psephos, from Axylos's house's own scene. Each opponent's party
--    in gParties is checked against the script when the battle starts, and each
--    trainer is marked beaten after the win.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, emu = L.S, L.emu
for k, v in pairs(dofile(L.OUT .. "trainer_symbols.lua")) do S[k] = v end

-- --- The script's teams -------------------------------------------------------------------------

local function scriptTrainers()
  local f = io.open("design/phase4/SCRIPT.md")
  if not f then L.fail("can't open design/phase4/SCRIPT.md") end
  local inPart, block, mon = false, nil, nil
  local trainers, order = {}, {}
  for line in f:lines() do
    if line:match("^# Part 3%. Trainers") then
      inPart = true
    elseif inPart and line:match("^## Knossa's trainers") then
      break
    elseif inPart then
      local const = line:match("^=== (TRAINER_ICHOR_[%w_]+) ===$")
      if const then
        block, mon = { const = const, mons = {} }, nil
        trainers[const] = block
        order[#order + 1] = const
      elseif block and line == "```" then
        block, mon = nil, nil
      elseif block and line == "" then
        mon = nil
      elseif block and line:match("^%- ") then
        mon.moves[#mon.moves + 1] = line:sub(3)
      elseif block then
        local k, v = line:match("^([%a ]+): (.*)$")
        if k and mon then
          mon[k] = v
        elseif k then
          block[k] = v
        else
          local species, item = line:match("^(%S+) @ (.+)$")
          mon = { species = species or line, item = item, moves = {} }
          block.mons[#block.mons + 1] = mon
        end
      end
    end
  end
  f:close()
  return trainers, order
end

-- "Mystic Water" -> S.ITEM_MYSTIC_WATER
local function const(prefix, words)
  local name = prefix .. (words:upper():gsub("[ %-]", "_"))
  local v = S[name]
  if v == nil then L.fail("no constant " .. name .. " in act3_trainers_consts.c") end
  return v
end

-- "24 HP / 24 Atk / ..." packed as TRAINER_PARTY_IVS does
local IV_SHIFT = { HP = 0, Atk = 5, Def = 10, Spe = 15, SpA = 20, SpD = 25 }
local function packIvs(s)
  local v = 0
  for n, stat in s:gmatch("(%d+) (%a+)") do v = v | (tonumber(n) << IV_SHIFT[stat]) end
  return v
end

local function readSized(addr, size)
  if size == 1 then return emu:read8(addr) elseif size == 2 then return emu:read16(addr) end
  return emu:read32(addr)
end

-- A-Z in the game's charset
local function gameName(addr)
  local t = {}
  for i = 0, 11 do
    local b = emu:read8(addr + i)
    if b == 0xFF then break end
    t[#t + 1] = (b >= 0xBB and b <= 0xD4) and string.char(65 + b - 0xBB) or "?"
  end
  return table.concat(t)
end

-- --- 1. gTrainers ---------------------------------------------------------------------------------

-- whether gSpeciesInfo gives this species this ability in any slot
local function canHave(species, ability)
  local base = S.gSpeciesInfo + species * S.SPECIES_INFO_SIZE + S.OFF_SPECIES_ABILITIES
  for k = 0, S.NUM_ABILITY_SLOTS - 1 do
    if readSized(base + k * S.SPECIES_ABILITY_SIZE, S.SPECIES_ABILITY_SIZE) == ability then return true end
  end
  return false
end

local function checkTable(trainers, order)
  -- Kythera's trainers are two blocks: 320-347, and 490-498 (the route standard's second
  -- wave, taken from the top of act3's range so Knossa's 348 on stay free)
  local blocks = (S.TRAINER_ICHOR_MYRSINE + 1 - S.TRAINER_ICHOR_EUDOROS)
                 + (S.TRAINER_ICHOR_DEXITHEA + 1 - S.TRAINER_ICHOR_LYKON)
  L.expect(#order == blocks,
           string.format("SCRIPT's Kythera section has %d trainers, ids %d-%d and %d-%d", #order,
                         S.TRAINER_ICHOR_EUDOROS, S.TRAINER_ICHOR_MYRSINE, S.TRAINER_ICHOR_LYKON,
                         S.TRAINER_ICHOR_DEXITHEA))
  local wrong, mons = {}, 0
  local function want(cond, what) if not cond then wrong[#wrong + 1] = what end end
  for i, c in ipairs(order) do
    local w = trainers[c]
    local id = S[c]
    if id == nil then L.fail("no constant " .. c .. " in act3_trainers_consts.c") end
    local where = c:sub(15)
    local first = S.TRAINER_ICHOR_MYRSINE + 1 - S.TRAINER_ICHOR_EUDOROS
    local expectId = i <= first and S.TRAINER_ICHOR_EUDOROS + i - 1 or S.TRAINER_ICHOR_LYKON + i - first - 1
    want(id == expectId, string.format("%s is id %d, out of SCRIPT's order", where, id))
    local t = S.gTrainers + (S.DIFFICULTY_NORMAL * S.TRAINERS_COUNT + id) * S.TRAINER_SIZE
    want(emu:read8(t + S.OFF_TRAINER_CLASS) == const("TRAINER_CLASS_", w.Class), where .. ": class " .. w.Class)
    want(gameName(t + S.OFF_TRAINER_NAME) == w.Name, where .. ": name " .. w.Name)
    local ai = 0
    for raw in w.AI:gmatch("[^/]+") do
      local flag = raw:match("^%s*(.-)%s*$")
      ai = ai | (flag == "Basic Trainer" and S.AI_BASIC_TRAINER or flag == "Check Bad Move" and S.AI_CHECK_BAD_MOVE
                 or L.fail(where .. ": unknown AI " .. flag))
    end
    want(emu:read32(t + S.OFF_TRAINER_AI_FLAGS) == ai, where .. ": AI " .. w.AI)
    local items = {}
    for item in (w.Items or ""):gmatch("[^/]+") do items[#items + 1] = const("ITEM_", item:match("^%s*(.-)%s*$")) end
    for k = 1, S.MAX_TRAINER_ITEMS do
      want(readSized(t + S.OFF_TRAINER_ITEMS + (k - 1) * S.TRAINER_ITEM_SIZE, S.TRAINER_ITEM_SIZE)
           == (items[k] or S.ITEM_NONE), string.format("%s: item %d", where, k))
    end
    local party = emu:read32(t + S.OFF_TRAINER_PARTY)
    for m, mon in ipairs(w.mons) do
      local p = party + (m - 1) * S.TRAINER_MON_SIZE
      local what = string.format("%s's %s", where, mon.species)
      want(readSized(p + S.OFF_TMON_SPECIES, S.TMON_SPECIES_SIZE) == const("SPECIES_", mon.species), what)
      want(emu:read8(p + S.OFF_TMON_LEVEL) == tonumber(mon.Level), what .. ": level " .. mon.Level)
      want(readSized(p + S.OFF_TMON_ITEM, S.TMON_ITEM_SIZE) == (mon.item and const("ITEM_", mon.item) or S.ITEM_NONE),
           what .. ": holds " .. (mon.item or "nothing"))
      -- An ability the stand-in species can't have is left out (the game stops
      -- on an illegal-ability screen): trainers.party lists them.
      local ability = mon.Ability and const("ABILITY_", mon.Ability) or S.ABILITY_NONE
      local species = const("SPECIES_", mon.species)
      if ability ~= S.ABILITY_NONE and not canHave(species, ability) then
        L.note(string.format("%s: SCRIPT's %s waits for the dex (the stand-in can't have it)", what, mon.Ability))
        ability = S.ABILITY_NONE
      end
      want(readSized(p + S.OFF_TMON_ABILITY, S.TMON_ABILITY_SIZE) == ability,
           what .. ": ability " .. (ability ~= S.ABILITY_NONE and mon.Ability or "(default)"))
      want(emu:read32(p + S.OFF_TMON_IV) == packIvs(mon.IVs), what .. ": IVs " .. mon.IVs)
      for k = 1, 4 do
        local move = readSized(p + S.OFF_TMON_MOVES + (k - 1) * S.TMON_MOVE_SIZE, S.TMON_MOVE_SIZE)
        want(move == (mon.moves[k] and const("MOVE_", mon.moves[k]) or 0),
             string.format("%s: move %d %s", what, k, mon.moves[k] or "(level-up default)"))
      end
      mons = mons + 1
    end
  end
  for _, what in ipairs(wrong) do L.check(false, "gTrainers differs from SCRIPT: " .. what) end
  L.check(#wrong == 0, string.format("gTrainers matches SCRIPT for all %d trainers and %d Pokémon "
                                     .. "(class, name, AI, items; species, level, held item, ability, IVs, moves)",
                                     #order, mons))
end

-- --- 2. Battles -----------------------------------------------------------------------------------

-- species and held item of a party Pokémon (substruct 0, decrypted)
local function decode(mon)
  local personality, otId = emu:read32(mon), emu:read32(mon + 4)
  local key = personality ~ otId
  local slot0 = emu:read8(S.sSubstructOffsets + personality % 24)
  local w = emu:read32(mon + S.OFF_BOXMON_SECURE + slot0 * S.SUBSTRUCT_SIZE) ~ key
  return w & 0x7FF, (w >> 16) & 0x3FF
end

local function checkParty(slot, want, where)
  local n = 0
  for i = 0, S.PARTY_SIZE - 1 do
    local mon = S.gParties + (slot * S.PARTY_SIZE + i) * S.POKEMON_SIZE
    local species, item = decode(mon)
    if species ~= 0 then
      n = n + 1
      local w = want.mons[n]
      if not w then L.fail(string.format("%s has more than SCRIPT's %d Pokémon", where, #want.mons)) end
      local level = emu:read8(mon + S.OFF_MON_LEVEL)
      L.check(species == const("SPECIES_", w.species) and level == tonumber(w.Level)
              and item == (w.item and const("ITEM_", w.item) or S.ITEM_NONE),
              string.format("%s's Pokémon %d is %s at level %s%s (species %d, level %d)", where, n, w.species,
                            w.Level, w.item and (" holding " .. w.item) or "", species, level))
    end
  end
  L.check(n == #want.mons, string.format("%s brings %d Pokémon, as SCRIPT says", where, #want.mons))
end

-- Play a battle out, checking the opponents' parties as it starts.
local function battle(sides, name)
  local fought
  L.settle({ limit = 40000, hooks = { BattleMainCB2 = function()
    local two = emu:read32(S.gBattleTypeFlags) & S.BATTLE_TYPE_TWO_OPPONENTS ~= 0
    L.check(two == (#sides == 2), string.format("%s: %s", name, #sides == 2 and "two trainers at once" or "one trainer"))
    for _, side in ipairs(sides) do checkParty(side[1], side[2], side[3]) end
    L.shot(name)
    fought = L.battle()
  end } })
  if not fought then L.fail(name .. ": no battle started") end
  L.check(fought.outcome == S.B_OUTCOME_WON, name .. ": won")
end

L.start(function()
  local trainers, order = scriptTrainers()
  L.quickstart()
  checkTable(trainers, order)

  L.runHeader("Act3Trainers_GiveHeader")
  L.check(L.partyLevel(0) == 100 and L.partyLevel(1) == 100, "the test party: two level-100 Metagross")

  L.runHeader("Act3Trainers_EudorosHeader", { noSettle = true })
  battle({ { S.B_TRAINER_OPPONENT_A, trainers.TRAINER_ICHOR_EUDOROS, "Eudoros" } }, "eudoros")
  L.check(L.defeated(S.TRAINER_ICHOR_EUDOROS), "Eudoros is marked beaten")

  L.runHeader("Act3Trainers_GalateaHeader", { noSettle = true })
  battle({ { S.B_TRAINER_OPPONENT_A, trainers.TRAINER_ICHOR_GALATEA_1, "Galatea" } }, "galatea")
  L.check(L.defeated(S.TRAINER_ICHOR_GALATEA_1), "Galatea is marked beaten")

  -- The bad guests: the house's first-entry scene, YES to the challenge, and
  -- one battle against both Titanborn at once.
  L.runHeader("Act3Trainers_GuestsHeader", { noSettle = true })
  L.waitUntil(function() return L.mapId() == S.MAP_AXYLOS_HOUSE end, 600, "Axylos's house")
  battle({ { S.B_TRAINER_OPPONENT_A, trainers.TRAINER_ICHOR_OCHROS, "Ochros" },
           { S.B_TRAINER_OPPONENT_B, trainers.TRAINER_ICHOR_PSEPHOS, "Psephos" } }, "bad_guests")
  L.check(L.defeated(S.TRAINER_ICHOR_OCHROS) and L.defeated(S.TRAINER_ICHOR_PSEPHOS),
          "Ochros and Psephos are both marked beaten")
  L.check(L.getFlag(S.FLAG_ICHOR_BAD_GUESTS_GONE), "the guests leave the house (FLAG_ICHOR_BAD_GUESTS_GONE)")
  L.shot("after_guests")
end)
