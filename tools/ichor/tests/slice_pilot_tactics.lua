-- Isolated battle-input model; no emulator memory is accessed or changed.
local createPilot = dofile("tools/ichor/tests/slice_pilot.lua")
local function battle(moves, held, ability, difficulty, ownAbility)
  local S = {
    gBattleMons = 100, BATTLE_MON_SIZE = 100, gBattlerPartyIndexes = 400,
    gPartiesCount = 500, B_TRAINER_PLAYER = 0, gMoveSelectionCursor = 1,
    gDisplayedStringBattle = 1000, gTypesInfo = 2000, TYPE_INFO_SIZE = 16,
    OFF_TYPE_NAME = 0, NUMBER_OF_MON_TYPES = 7, TYPE_ID_SIZE = 1,
    gTypeEffectivenessTable = 5000, TYPE_EFFECT_SIZE = 2, TYPE_EFFECT_ONE = 4096,
    gCategoryIconSpriteId = 5, gSprites = 3000, PILOT_SPRITE_SIZE = 64,
    OFF_PILOT_SPRITE_ANIM = 0, MAX_MON_MOVES = 4, MOVE_ID_SIZE = 2,
    OFF_BATTLE_MON_MOVES = 0, OFF_BATTLE_MON_PP = 8, OFF_BATTLE_MON_TYPES = 12,
    OFF_BATTLE_MON_ATTACK = 16, OFF_BATTLE_MON_DEFENSE = 18,
    OFF_BATTLE_MON_SP_ATTACK = 20, OFF_BATTLE_MON_SP_DEFENSE = 22,
    OFF_BATTLE_MON_STAGES = 24, OFF_BATTLE_MON_ABILITY = 32,
    OFF_BATTLE_MON_ITEM = 34, OFF_BATTLE_MON_STATUS = 36,
    OFF_BATTLE_MON_HP = 40, OFF_BATTLE_MON_MAXHP = 42,
    VAR_DIFFICULTY = 123, DIFFICULTY_HARD = 2,
    STAT_ATK = 1, STAT_DEF = 2, STAT_SPATK = 4, STAT_SPDEF = 5,
    DAMAGE_CATEGORY_PHYSICAL = 1, DAMAGE_CATEGORY_SPECIAL = 2, ABILITY_FUR_COAT = 9,
    ABILITY_FLASH_FIRE = 10,
    ABILITY_WATER_ABSORB = 11, ABILITY_STORM_DRAIN = 12, ABILITY_DRY_SKIN = 13,
    ABILITY_SAP_SIPPER = 14, ABILITY_LEVITATE = 15, ABILITY_EARTH_EATER = 16,
    ABILITY_VOLT_ABSORB = 17, ABILITY_LIGHTNING_ROD = 18, ABILITY_MOTOR_DRIVE = 19,
    ABILITY_MOLD_BREAKER = 21, ABILITY_TERAVOLT = 22, ABILITY_TURBOBLAZE = 23,
    MOVE_YAWN = 20, MOVE_DOUBLE_KICK = 10, ITEM_POKE_BALL = 103,
    ITEM_SUPER_POTION = 104, ITEM_POTION = 105, ITEM_MOOMOO_MILK = 106,
    TYPE_GRASS = 2, TYPE_FIRE = 3, TYPE_WATER = 4,
    TYPE_GROUND = 5, TYPE_ELECTRIC = 6,
    ITEM_MIRACLE_SEED = 100, ITEM_CHARCOAL = 101, ITEM_MYSTIC_WATER = 102,
    CHAR_A = 65, CHAR_0 = 48, CHAR_SPACE = 32, CHAR_COLON = 58, EOS = 255,
    MOVE_DESCRIPTION_BUTTON = 5, L_BUTTON = 5,
  }
  local K = {UP = 1, DOWN = 2, LEFT = 3, RIGHT = 4, L = 5, A = 6}
  local m8, m16, m32 = {[1] = 0, [5] = 0, [400] = 0, [401] = 0, [500] = 1}, {}, {[236] = 0, [600] = 123}
  local function text(address, value)
    for i = 1, #value do m8[address + i - 1] = value:byte(i) end
    m8[address + #value] = 255
  end
  local names = {"NORMAL", "GRASS", "FIRE", "WATER", "GROUND", "ELECTRIC"}
  for i, name in ipairs(names) do text(2000 + i * 16, name) end
  for side = 0, 1 do
    local base = 100 + side * 100
    for i = 0, 7 do m8[base + 24 + i] = 6 end
    for i = 0, 2 do m8[base + 12 + i] = i == 0 and (side == 0 and 3 or 1) or 0 end
    for _, offset in ipairs({16, 18, 20, 22}) do m16[base + offset] = 100 end
  end
  m16[132], m16[134], m16[232] = ownAbility or 0, held or 0, ability or 0
  m16[140], m16[142] = 10, 40
  for i = 0, 3 do
    m16[100 + i * 2] = moves[i + 1] and moves[i + 1].id or 0
    m8[108 + i] = moves[i + 1] and 10 or 0
  end
  for own = 1, 6 do
    m16[5000 + (own * 7 + 1) * 2] = 4096
  end
  local description, choices = false, {}
  local function display()
    local move = assert(moves[m8[1] + 1])
    text(1000, description and ("PWR: " .. move.power) or ("TYPE/" .. names[move.kind]))
    m8[3000] = move.category
  end
  display()
  local function read(memory, address)
    return assert(memory[address], "unexpected modeled memory read " .. address)
  end
  local pilot = createPilot({
    S = S, K = K,
    emu = {
      read8 = function(_, address) return read(m8, address) end,
      read16 = function(_, address) return read(m16, address) end,
      read32 = function(_, address) return read(m32, address) end,
    },
    tap = function(key)
      local cursor = m8[1]
      if key == K.L then description = not description
      elseif key == K.UP and cursor >= 2 then m8[1] = cursor - 2
      elseif key == K.DOWN and moves[cursor + 3] then m8[1] = cursor + 2
      elseif key == K.LEFT and cursor % 2 == 1 then m8[1] = cursor - 1
      elseif key == K.RIGHT and cursor % 2 == 0 and moves[cursor + 2] then m8[1] = cursor + 1
      elseif key == K.A then choices[#choices + 1] = m8[1] end
      display()
    end,
    wait = function() end, log = function() end, shot = function() end,
    expect = function(condition, message) assert(condition, message) end,
    fail = function(message) error(message, 0) end,
    isTrainerBattle = function() return true end,
    itemCount = function(item)
      assert(item == S.ITEM_POKE_BALL, "Spartan must not inspect medicines for battle use")
      return 0
    end,
    getVar = function(variable)
      assert(variable == S.VAR_DIFFICULTY)
      return difficulty or 1
    end,
    partyMon = function() return 600 end,
  }, 1)
  pilot.beginBattle()
  return pilot, choices, m8, m32
end

local function move(id, power, kind, category)
  return {id = id, power = power, kind = kind or 1, category = category or 1}
end
local pilot, choices = battle({move(10, 30), move(11, 40)})
pilot.chooseMove()
assert(choices[1] == 0, "Double Kick must account for both hits")
pilot, choices = battle({move(11, 40, 3, 2), move(12, 65, 1, 2)})
pilot.chooseMove()
assert(choices[1] == 1, "without Charcoal, the stronger neutral move wins")
pilot, choices = battle({move(11, 40, 3, 2), move(12, 65, 1, 2)}, 101)
pilot.chooseMove()
assert(choices[1] == 0, "the actually held Charcoal boosts Fire damage")
pilot, choices = battle({move(11, 80), move(12, 60, 1, 2)}, 0, 9)
pilot.chooseMove()
assert(choices[1] == 1, "Fur Coat favors the available special attack")
for _, immunity in ipairs({{10, 3}, {11, 4}, {12, 4}, {13, 4}, {14, 2},
                          {15, 5}, {16, 5}, {17, 6}, {18, 6}, {19, 6}}) do
  pilot, choices = battle({move(11, 100, immunity[2]), move(12, 40)}, 0, immunity[1])
  pilot.chooseMove()
  assert(choices[1] == 1, "an ability-immune attack must not beat available neutral damage")
  for breaker = 21, 23 do
    pilot, choices = battle({move(11, 100, immunity[2]), move(12, 40)}, 0, immunity[1], 1, breaker)
    pilot.chooseMove()
    assert(choices[1] == 0, "an ability-breaking attacker must bypass the immunity")
  end
end
pilot, choices = battle({move(11, 80), move(12, 60, 1, 2)}, 0, 9, 1, 21)
pilot.chooseMove()
assert(choices[1] == 0, "Mold Breaker must bypass Fur Coat")
local party, status
pilot, choices, party, status = battle({move(20, 0, 1, 3), move(11, 40)})
pilot.chooseMove(); pilot.chooseMove()
assert(choices[1] == 0 and choices[2] == 1, "Yawn must not stall repeated turns")
party[401] = 1
pilot.chooseMove()
assert(choices[3] == 0, "a different opponent can receive Yawn")
party[401], status[236] = 2, 1
pilot.chooseMove()
assert(choices[4] == 1, "an already statused opponent must not receive Yawn")
pilot = battle({move(11, 40)}, 0, 0, 2)
assert(not pilot.chooseAction(true), "Spartan must never request battle medicine")
console:log("PILOT TACTICS PASS: multi-hit, held booster, ability immunities/bypass, Fur Coat, bounded Yawn and Spartan item ban")
console:log("PILOT TACTICS done")
