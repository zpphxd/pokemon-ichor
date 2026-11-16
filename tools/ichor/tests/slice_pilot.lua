-- Button-only decisions for natural runs; the shared adapter remains read-only.
return function(L, starter)
  local S, K, emu = L.S, L.K, L.emu
  local P, powers, types, categories = {}, {}, {}, {}
  local partyBefore, ballsBefore, throws, switchTarget, switched
  local starterPersonality, attemptedYawn, evolvingSlot

  local function gameString(address)
    local bytes = {}
    for i = 0, 511 do
      local b = emu:read8(address + i)
      if b == S.EOS then return table.concat(bytes) end
      bytes[#bytes + 1] = string.char(b)
    end
    L.fail("native menu string did not terminate")
  end

  local function moveType()
    local text = gameString(S.gDisplayedStringBattle)
    for kind = 1, S.NUMBER_OF_MON_TYPES - 1 do
      local name = gameString(S.gTypesInfo + kind * S.TYPE_INFO_SIZE + S.OFF_TYPE_NAME)
      if #name > 0 and text:sub(-#name) == name then return kind end
    end
    L.fail("native move-type display did not name a known type")
  end

  local function stageFactor(battler, stat)
    local stage = emu:read8(S.gBattleMons + battler * S.BATTLE_MON_SIZE + S.OFF_BATTLE_MON_STAGES + stat)
    L.expect(stage <= 12, "native battle stat stage is valid")
    return stage >= 6 and (stage - 4) / 2 or 2 / (8 - stage)
  end

  local function attackScore(power, kind, category, move)
    if power == 0 then return 0 end
    local ability = emu:read16(S.gBattleMons + S.BATTLE_MON_SIZE + S.OFF_BATTLE_MON_ABILITY)
    local ownAbility = emu:read16(S.gBattleMons + S.OFF_BATTLE_MON_ABILITY)
    if ownAbility == S.ABILITY_MOLD_BREAKER or ownAbility == S.ABILITY_TERAVOLT or ownAbility == S.ABILITY_TURBOBLAZE then
      ability = 0
    end
    if (kind == S.TYPE_FIRE and ability == S.ABILITY_FLASH_FIRE)
       or (kind == S.TYPE_WATER and (ability == S.ABILITY_WATER_ABSORB or ability == S.ABILITY_STORM_DRAIN or ability == S.ABILITY_DRY_SKIN))
       or (kind == S.TYPE_GRASS and ability == S.ABILITY_SAP_SIPPER)
       or (kind == S.TYPE_GROUND and (ability == S.ABILITY_LEVITATE or ability == S.ABILITY_EARTH_EATER))
       or (kind == S.TYPE_ELECTRIC and (ability == S.ABILITY_VOLT_ABSORB or ability == S.ABILITY_LIGHTNING_ROD or ability == S.ABILITY_MOTOR_DRIVE)) then
      return 0
    end
    local score, seen = power, {}
    if move == S.MOVE_DOUBLE_KICK then score = score * 2 end
    local item = emu:read16(S.gBattleMons + S.OFF_BATTLE_MON_ITEM)
    if (item == S.ITEM_MIRACLE_SEED and kind == S.TYPE_GRASS)
       or (item == S.ITEM_CHARCOAL and kind == S.TYPE_FIRE)
       or (item == S.ITEM_HARD_STONE and kind == S.TYPE_ROCK)
       or (item == S.ITEM_MYSTIC_WATER and kind == S.TYPE_WATER) then score = score * 1.2 end
    for i = 0, 2 do
      local own = emu:read8(S.gBattleMons + S.OFF_BATTLE_MON_TYPES + i * S.TYPE_ID_SIZE)
      if own == kind then score = score * 1.5; break end
    end
    for i = 0, 2 do
      local foe = emu:read8(S.gBattleMons + S.BATTLE_MON_SIZE + S.OFF_BATTLE_MON_TYPES + i * S.TYPE_ID_SIZE)
      if foe ~= 0 and not seen[foe] then
        local address = S.gTypeEffectivenessTable + (kind * S.NUMBER_OF_MON_TYPES + foe) * S.TYPE_EFFECT_SIZE
        score = score * emu:read16(address) / S.TYPE_EFFECT_ONE
        seen[foe] = true
      end
    end
    local physical = category == S.DAMAGE_CATEGORY_PHYSICAL
    local atkOffset = physical and S.OFF_BATTLE_MON_ATTACK or S.OFF_BATTLE_MON_SP_ATTACK
    local defOffset = physical and S.OFF_BATTLE_MON_DEFENSE or S.OFF_BATTLE_MON_SP_DEFENSE
    local attack = emu:read16(S.gBattleMons + atkOffset) * stageFactor(0, physical and S.STAT_ATK or S.STAT_SPATK)
    local defense = emu:read16(S.gBattleMons + S.BATTLE_MON_SIZE + defOffset)
                  * stageFactor(1, physical and S.STAT_DEF or S.STAT_SPDEF)
    if physical and ability == S.ABILITY_FUR_COAT then
      defense = defense * 2
    end
    local status = emu:read32(S.gBattleMons + S.OFF_BATTLE_MON_STATUS)
    if physical then
      if ownAbility == S.ABILITY_GUTS and status ~= 0 then
        attack = attack * 1.5
      elseif status & S.STATUS1_BURN ~= 0 and (move ~= S.MOVE_FACADE or S.BURN_WEAKENS_FACADE ~= 0) then
        attack = attack / 2
      end
    end
    if emu:read16(S.gBattleMons + S.OFF_BATTLE_MON_HP) * 3 <= emu:read16(S.gBattleMons + S.OFF_BATTLE_MON_MAXHP)
       and ((ownAbility == S.ABILITY_BLAZE and kind == S.TYPE_FIRE)
         or (ownAbility == S.ABILITY_OVERGROW and kind == S.TYPE_GRASS)
         or (ownAbility == S.ABILITY_TORRENT and kind == S.TYPE_WATER)) then
      score = score * 1.5
    end
    L.expect(attack > 0 and defense > 0, "native battle stats are positive")
    score = score * attack / defense
    return score
  end

  function P.moveCursor(slot)
    for _ = 1, 4 do
      local current = emu:read8(S.gMoveSelectionCursor)
      if current == slot then return end
      if current // 2 ~= slot // 2 and (slot < 2 or current % 2 == slot % 2) then
        L.tap(slot < 2 and K.UP or K.DOWN)
      else
        L.tap(slot % 2 == 0 and K.LEFT or K.RIGHT)
      end
    end
    L.fail("natural pilot could not select move slot " .. slot)
  end

  local function descriptionPower()
    local text = {}
    for i = 0, 511 do
      local b = emu:read8(S.gDisplayedStringBattle + i)
      if b == S.EOS then break end
      if b >= S.CHAR_A and b < S.CHAR_A + 26 then
        text[#text + 1] = string.char(65 + b - S.CHAR_A)
      elseif b >= S.CHAR_0 and b < S.CHAR_0 + 10 then
        text[#text + 1] = string.char(48 + b - S.CHAR_0)
      elseif b == S.CHAR_COLON then text[#text + 1] = ":"
      elseif b == S.CHAR_SPACE then text[#text + 1] = " "
      else text[#text + 1] = "#" end
    end
    text = table.concat(text)
    L.expect(text:find("PWR: ", 1, true), "the actual move-description screen supplies power")
    return tonumber(text:match("PWR: (%d+)")) or 0
  end

  function P.chooseMove()
    L.expect(S.MOVE_DESCRIPTION_BUTTON == S.L_BUTTON, "the native move-description button is L")
    local selected, best, yawn = nil, -1, nil
    for slot = 0, S.MAX_MON_MOVES - 1 do
      local move = emu:read16(S.gBattleMons + S.OFF_BATTLE_MON_MOVES + slot * S.MOVE_ID_SIZE)
      local pp = emu:read8(S.gBattleMons + S.OFF_BATTLE_MON_PP + slot)
      if move ~= 0 and pp > 0 then
        if powers[move] == nil then
          P.moveCursor(slot)
          types[move] = moveType()
          L.tap(K.L); L.wait(4)
          powers[move] = descriptionPower()
          local icon = emu:read8(S.gCategoryIconSpriteId)
          L.expect(icon < 64, "the native description has a category icon")
          categories[move] = emu:read8(S.gSprites + icon * S.PILOT_SPRITE_SIZE + S.OFF_PILOT_SPRITE_ANIM)
          L.log(string.format("PILOT inspected move=%d native_power=%d category=%d", move, powers[move], categories[move]))
          L.shot("natural_move_description_" .. move)
          L.tap(K.L); L.wait(4)
        end
        local score = attackScore(powers[move], types[move], categories[move], move)
        local foe = emu:read16(S.gBattlerPartyIndexes + S.BATTLER_PARTY_INDEX_SIZE)
        if move == S.MOVE_YAWN and L.isTrainerBattle() and not attemptedYawn[foe]
           and emu:read32(S.gBattleMons + S.BATTLE_MON_SIZE + S.OFF_BATTLE_MON_STATUS) == 0 then
          yawn = slot
        end
        if score >= best then selected, best = slot, score end
      end
    end
    L.expect(selected ~= nil, "the natural pilot found a move with real PP")
    if yawn then
      -- Yawn needs a setup turn; prefer a conservative two-hit finish.
      local level = emu:read8(S.gBattleMons + S.OFF_BATTLE_MON_LEVEL)
      local damage = best > 0 and math.floor(((2 * level // 5 + 2) * best / 50 + 2) * 0.85) or 0
      if damage * 2 < emu:read16(S.gBattleMons + S.BATTLE_MON_SIZE + S.OFF_BATTLE_MON_HP) then
        selected, best = yawn, 1000000
      end
    end
    P.moveCursor(selected)
    local foe = emu:read16(S.gBattlerPartyIndexes + S.BATTLER_PARTY_INDEX_SIZE)
    L.log(string.format("PILOT attack slot=%d move=%d score=%.2f foe_party=%d foe_hp=%d", selected,
                        emu:read16(S.gBattleMons + S.OFF_BATTLE_MON_MOVES + selected * S.MOVE_ID_SIZE), best,
                        foe, emu:read16(S.gBattleMons + S.BATTLE_MON_SIZE + S.OFF_BATTLE_MON_HP)))
    if emu:read16(S.gBattleMons + S.OFF_BATTLE_MON_MOVES + selected * S.MOVE_ID_SIZE) == S.MOVE_YAWN then
      attemptedYawn[foe] = true
    end
    L.tap(K.A)
  end

  function P.observeEvolution()
    local task = L.taskAddress("Task_EvolutionScene")
    if task then evolvingSlot = emu:read16(task + S.OFF_EVOLUTION_PARTY_ID) end
  end

  function P.learnMove()
    L.wait(20)
    local incoming = emu:read16(S.gMoveToLearn)
    if incoming == S.MOVE_HOWL then
      L.log("PILOT declining Howl; this pilot does not use Attack setup")
      L.shot("natural_declined_setup_move")
      L.tap(K.B)
      L.waitUntil(function() return not L.taskRunning("Task_HandleReplaceMoveInput") end, 900, "declining the unused setup move")
      return
    end
    local mon = evolvingSlot
    if mon == nil then mon = emu:read8(emu:read32(S.gBattleStruct) + S.OFF_EXP_GETTER_MON) end
    L.expect(mon < emu:read8(S.gPartiesCount + S.B_TRAINER_PLAYER), "the actual learner is in the party")
    local selected, lowest = 0, math.huge
    local moves = {}
    for slot = 0, S.MAX_MON_MOVES - 1 do moves[slot] = L.partyMove(mon, slot) end
    for slot = 0, S.MAX_MON_MOVES - 1 do
      local move = moves[slot]
      local priority = powers[move] or 1000
      if move == S.MOVE_YAWN then priority = 2000 end
      if priority > 0 then
        local duplicate = false
        for other = 0, S.MAX_MON_MOVES - 1 do
          if other ~= slot and types[move] and types[move] == types[moves[other]]
             and categories[move] == categories[moves[other]]
             and (powers[moves[other]] or 0) >= priority then duplicate = true end
        end
        if not duplicate then priority = priority + 100 end
      end
      if priority < lowest then selected, lowest = slot, priority end
    end
    for _ = 1, selected do L.tap(K.DOWN) end
    L.log(string.format("PILOT learning party=%d move=%d replaces=%d in slot=%d",
                        mon, incoming, moves[selected], selected))
    L.shot("natural_move_learning")
    L.tap(K.A)
    L.waitUntil(function() return not L.taskRunning("Task_HandleReplaceMoveInput") end, 900, "the native move choice")
  end

  local function partySlot(slot)
    for _ = 1, 16 do
      local switching = emu:read8(S.gPartyMenu + S.OFF_PARTY_MENU_ACTION) == S.PARTY_ACTION_SWITCH
      local offset = switching and S.OFF_PARTY_MENU_SECOND_SLOT or S.OFF_PARTY_MENU_SLOT
      local current = emu:read8(S.gPartyMenu + offset)
      if current == slot then return end
      if slot == 0 then L.tap(K.LEFT)
      elseif current == 0 then L.tap(K.RIGHT)
      else L.tap(current > slot and K.UP or K.DOWN) end
    end
    L.fail("could not select native party slot " .. slot)
  end

  function P.chooseReplacement()
    L.wait(30)
    local count = emu:read8(S.gPartiesCount + S.B_TRAINER_PLAYER)
    for slot = 0, count - 1 do
      if L.partyHp(slot) > 0 and slot ~= emu:read16(S.gBattlerPartyIndexes)
         and (switchTarget == nil or slot == switchTarget) then
        partySlot(slot)
        L.shot("natural_living_replacement")
        L.tap(K.A); L.wait(20); L.tap(K.A)
        L.waitUntil(L.inBattle, 1200, "a living caught partner entering the battle")
        L.wait(30)
        switchTarget = nil
        return
      end
    end
    L.fail("native replacement menu has no living partner")
  end

  local function openBag()
    L.tap(K.START)
    L.waitUntil(function() return L.taskRunning("Task_ShowStartMenu") end, 300, "the start menu")
    L.wait(25)
    local count, target = emu:read8(S.sNumStartMenuActions), nil
    for i = 0, count - 1 do
      if emu:read8(S.sCurrentStartMenuActions + i) == 2 then target = i end
    end
    L.expect(target ~= nil, "the natural pilot can open the actual Bag")
    for _ = 1, (target - emu:read8(S.sStartMenuCursorPos)) % count do L.tap(K.DOWN) end
    L.tap(K.A)
    L.waitUntil(function() return L.taskRunning("Task_BagMenu_HandleInput") end, 1200, "the Bag")
    L.wait(30)
  end

  local function selectItem(item, pocket, offset, capacity, medicineSlot, give)
    for _ = 1, S.POCKETS_COUNT do
      if emu:read8(S.gBagPosition + S.OFF_BAG_POCKET) == pocket then break end
      L.tap(K.RIGHT); L.wait(50)
    end
    L.expect(emu:read8(S.gBagPosition + S.OFF_BAG_POCKET) == pocket, "the actual healing pocket is open")
    local index
    for i = 0, capacity - 1 do
      if emu:read16(L.sb1() + S.OFF_SB1_BAG + offset + i * S.ITEM_SLOT_SIZE) == item then index = i; break end
    end
    L.expect(index ~= nil, "the healing item is in the actual pocket")
    for _ = 1, capacity + 1 do
      local current = emu:read16(S.gBagPosition + S.OFF_BAG_CURSOR + pocket * 2)
                    + emu:read16(S.gBagPosition + S.OFF_BAG_SCROLL + pocket * 2)
      if current == index then break end
      L.tap(current > index and K.UP or K.DOWN)
    end
    L.tap(K.A)
    L.waitUntil(function()
      return L.taskRunning("Task_ItemContext_SingleRow") or L.taskRunning("Task_ItemContext_MultipleRows")
    end, 300, "the actual item action menu")
    L.wait(20)
    L.expect(emu:read16(S.gSpecialVar_ItemId) == item, "the selected item matches the request")
    if medicineSlot ~= nil and pocket == S.POCKET_BERRIES then L.tap(K.DOWN) end
    if give then L.tap(K.RIGHT) end
    L.shot("natural_item_use_menu")
    L.tap(K.A)
    if medicineSlot ~= nil then
      L.waitUntil(function() return L.taskRunning("Task_HandleChooseMonInput") end, 1200, "the medicine's party picker")
      L.wait(30)
      partySlot(medicineSlot)
    end
  end

  local function closeMenus()
    for _ = 1, 40 do
      if L.idle() then return end
      L.tap(K.B); L.wait(15)
    end
    L.fail("the native menus did not return field control")
  end

  function P.beginBattle()
    evolvingSlot = nil
    if starterPersonality == nil then starterPersonality = emu:read32(L.partyMon(0)) end
    attemptedYawn = {}
    partyBefore = emu:read8(S.gPartiesCount + S.B_TRAINER_PLAYER)
    ballsBefore, throws = L.itemCount(S.ITEM_POKE_BALL), 0
    switchTarget, switched = nil, false
  end

  local function buyItems(item, quantity, down, expectedCost)
    L.expect(L.taskRunning("Task_BuyMenu"), "purchases start in the actual item list")
    local before, money = L.itemCount(item), L.money()
    if expectedCost then L.expect(money >= expectedCost, "the natural pilot can afford the requested supplies") end
    local task = L.taskAddress("Task_BuyMenu")
    for _ = 1, down do L.tap(K.DOWN) end
    L.tap(K.A)
    L.waitUntil(function()
      if L.taskRunning("Task_BuyHowManyDialogueHandleInput") then return true end
      L.tap(K.A); L.wait(8)
      return false
    end, 900, "the native shop quantity picker")
    L.expect(emu:read16(task + S.OFF_BUY_ITEM_ID) == item, "the real shop selected the requested item")
    for _ = 2, quantity do L.tap(K.UP) end
    L.expect(emu:read16(task + S.OFF_BUY_ITEM_COUNT) == quantity, "the real quantity picker selected the requested count")
    L.shot("natural_buy_supplies")
    L.tap(K.A)
    L.waitUntil(function() return not L.taskRunning("Task_BuyHowManyDialogueHandleInput") end, 300, "the native price quote")
    local price = gameString(S.gStringVar3)
    L.expect(#price > 0 and #price <= 6, "the native quote has a valid money width")
    local cost = 0
    for i = 1, #price do
      local digit = price:byte(i) - S.CHAR_0
      L.expect(digit >= 0 and digit <= 9, "the native quote contains only decimal digits")
      cost = cost * 10 + digit
    end
    L.expect(cost > 0 and cost <= money, "the actual quoted purchase is affordable")
    if expectedCost then L.expect(cost == expectedCost, "the native quote matches the expected ordinary-ball price") end
    L.waitUntil(function()
      if L.itemCount(item) == before + quantity and L.money() == money - cost then return true end
      L.expect(not L.taskRunning("Task_BuyMenu"), "the shop returned without the requested supplies and quoted payment")
      L.tap(K.A); L.wait(8)
      return false
    end, 1200, "the purchased supplies and exact quoted payment")
    L.waitUntil(function()
      if L.taskRunning("Task_BuyMenu") then return true end
      L.tap(K.A); L.wait(8)
      return false
    end, 900, "the item list after the purchase")
    L.log(string.format("PILOT bought item=%d count=%d->%d money=%d->%d quoted_cost=%d",
                        item, before, L.itemCount(item), money, L.money(), cost))
    L.shot("natural_paid_for_supplies")
  end

  function P.buyBalls()
    buyItems(S.ITEM_POKE_BALL, 5, 0, 1000)
  end

  function P.buyMedicine()
    buyItems(S.ITEM_SUPER_POTION, 5, 2)
  end

  function P.chooseAction(trainer)
    if trainer and L.getVar(S.VAR_DIFFICULTY) ~= S.DIFFICULTY_HARD then
      local hp = emu:read16(S.gBattleMons + S.OFF_BATTLE_MON_HP)
      local maxHp = emu:read16(S.gBattleMons + S.OFF_BATTLE_MON_MAXHP)
      if hp > 0 and hp * 2 <= maxHp then
        for _, item in ipairs({S.ITEM_SUPER_POTION, S.ITEM_POTION, S.ITEM_MOOMOO_MILK}) do
          local before = L.itemCount(item)
          if before > 0 then
            local slot = emu:read16(S.gBattlerPartyIndexes)
            L.tap(K.UP); L.tap(K.RIGHT); L.tap(K.A)
            L.waitUntil(function() return L.taskRunning("Task_BagMenu_HandleInput") end, 1200, "the native battle medicine Bag")
            L.wait(30)
            selectItem(item, S.POCKET_ITEMS, S.OFF_BAG_ITEMS, S.BAG_ITEMS_COUNT, slot)
            L.tap(K.A)
            L.waitUntil(function()
              if L.inBattle() and emu:read16(S.gBattleMons + S.OFF_BATTLE_MON_HP) > hp then return true end
              L.tap(K.A); L.wait(8)
              return false
            end, 1800, "native battle medicine recovery")
            L.expect(L.itemCount(item) == before - 1, "battle healing consumes exactly one owned medicine")
            L.log("PILOT native battle healing item=" .. item)
            return true
          end
        end
      end
    end
    if P.training and not trainer and not switched then
      switched = true
      local strongest = 0
      for slot = 1, emu:read8(S.gPartiesCount + S.B_TRAINER_PLAYER) - 1 do
        if L.partyHp(slot) > 0 and L.partyLevel(slot) > L.partyLevel(strongest) then strongest = slot end
      end
      if strongest ~= emu:read16(S.gBattlerPartyIndexes) then
        switchTarget = strongest
        L.log("PILOT native switch training to party slot " .. strongest)
        L.tap(K.DOWN); L.tap(K.LEFT); L.tap(K.A)
        L.waitUntil(function() return L.taskRunning("Task_HandleChooseMonInput") end, 1200, "the native battle switch menu")
        return true
      end
    end
    local count = emu:read8(S.gPartiesCount + S.B_TRAINER_PLAYER)
    if trainer or throws >= 3 or L.itemCount(S.ITEM_POKE_BALL) == 0 or count >= 4
       or (L.mapId() ~= S.MAP_ROUTE1 and L.mapId() ~= S.MAP_KRONION) then return false end
    local species = emu:read16(S.gBattleMons + S.BATTLE_MON_SIZE + S.OFF_BATTLE_MON_SPECIES)
    if count >= 3 and (not P.training or (species ~= S.SPECIES_EOPEEP and species ~= S.SPECIES_PEBBLITH)) then return false end
    for slot = 0, count - 1 do
      if L.partySpecies(slot) == species then return false end
    end
    L.tap(K.UP); L.tap(K.RIGHT); L.tap(K.A)
    L.waitUntil(function() return L.taskRunning("Task_BagMenu_HandleInput") end, 1200, "the actual battle Bag")
    L.wait(30)
    selectItem(S.ITEM_POKE_BALL, S.POCKET_POKE_BALLS, S.OFF_BAG_BALLS, S.BAG_POKEBALLS_COUNT)
    L.waitUntil(L.inBattle, 1200, "the real capture throw")
    L.wait(30)
    throws = throws + 1
    return true
  end

  function P.afterBattle(rec)
    if throws > 0 then
      L.expect(L.itemCount(S.ITEM_POKE_BALL) == ballsBefore - throws, "native throws consumed exactly the owned balls")
    end
    if rec.outcome == S.B_OUTCOME_CAUGHT then
      L.expect(emu:read8(S.gPartiesCount + S.B_TRAINER_PLAYER) == partyBefore + 1, "a real capture added one partner")
      L.log("PILOT caught partner; party=" .. (partyBefore + 1))
    end
  end

  local function returnToPosition(x, y)
    if L.grid().people[x .. "," .. y] then
      L.log("PILOT return tile is now occupied by an NPC; continuing from the map entrance")
    else
      L.go(x, y)
    end
  end

  local function restAtHome()
    local map, x, y = L.mapId(), L.pos()
    if map == S.MAP_KRONION then L.leaveEdge("left", S.MAP_ROUTE1) end
    L.leaveEdge("down", S.MAP_ELAIA)
    L.useWarp(S.MAP_HOUSE_1F)
    L.talk(L.npc("ElaiaVillage_PlayersHouse_1F_EventScript_Mom"), { answers = {"yes"} })
    for slot = 0, emu:read8(S.gPartiesCount + S.B_TRAINER_PLAYER) - 1 do
      local hp, maxHp = L.partyHp(slot)
      L.expect(hp == maxHp and hp > 0, "Mom's actual meal restored partner " .. slot)
    end
    L.useWarp(S.MAP_ELAIA)
    L.leaveEdge("up", S.MAP_ROUTE1)
    if map == S.MAP_KRONION then L.leaveEdge("right", S.MAP_KRONION) end
    returnToPosition(x, y)
    L.log("PILOT returned from Mom's actual heal")
  end

  local function restAtAsclepeion()
    local map, x, y = L.mapId(), L.pos()
    local mainland = map == S.MAP_CITY or map == S.MAP_E_ASCLEPEION
    local town = mainland and S.MAP_CITY or S.MAP_AKTI
    local clinic = mainland and S.MAP_E_ASCLEPEION or S.MAP_ASCLEPEION
    local healer = mainland and "EmporionCity_Asclepeion_EventScript_Healer"
                           or "AktiTown_Asclepeion_EventScript_Healer"
    if map == S.MAP_TEMPLE then L.useWarp(town) end
    if L.mapId() == town then L.useWarp(clinic) end
    L.talk(L.npc(healer))
    for slot = 0, emu:read8(S.gPartiesCount + S.B_TRAINER_PLAYER) - 1 do
      local hp, maxHp = L.partyHp(slot)
      L.expect(hp == maxHp and hp > 0, "the native Asclepeion restored partner " .. slot)
    end
    if map ~= clinic then L.useWarp(town) end
    if map == S.MAP_TEMPLE then L.useWarp(S.MAP_TEMPLE) end
    returnToPosition(x, y)
    L.log("PILOT returned from the actual Asclepeion")
  end

  function P.recover()
    if not L.idle() or emu:read8(S.gPartiesCount + S.B_TRAINER_PLAYER) == 0 then return end
    local hp, maxHp = L.partyHp(0)
    local homeReachable = L.mapId() == S.MAP_ROUTE1 or L.mapId() == S.MAP_KRONION
    local mainlandClinic = L.mapId() == S.MAP_CITY or L.mapId() == S.MAP_E_ASCLEPEION
    local clinicReachable = mainlandClinic or L.mapId() == S.MAP_AKTI or L.mapId() == S.MAP_TEMPLE or L.mapId() == S.MAP_ASCLEPEION
    if clinicReachable and not mainlandClinic and L.getFlag(S.FLAG_BADGE01_GET) and not L.getFlag(S.FLAG_SLICE_COMPLETE) then return end
    if clinicReachable then
      for slot = 0, emu:read8(S.gPartiesCount + S.B_TRAINER_PLAYER) - 1 do
        local current, maximum = L.partyHp(slot)
        local pp = 0
        for move = 0, S.MAX_MON_MOVES - 1 do pp = pp + L.partyPp(slot, move) end
        if current < maximum or pp < 6 then restAtAsclepeion(); return end
      end
    end
    if hp == 0 and homeReachable then restAtHome(); return end
    if hp == 0 and clinicReachable then restAtAsclepeion(); return end
    if hp == 0 or hp * 4 > maxHp * 3 then return end
    local choices = {
      {S.ITEM_ORAN_BERRY, S.POCKET_BERRIES, S.OFF_BAG_BERRIES, S.BAG_BERRIES_COUNT},
      {S.ITEM_POTION, S.POCKET_ITEMS, S.OFF_BAG_ITEMS, S.BAG_ITEMS_COUNT},
      {S.ITEM_MOOMOO_MILK, S.POCKET_ITEMS, S.OFF_BAG_ITEMS, S.BAG_ITEMS_COUNT},
      {S.ITEM_SUPER_POTION, S.POCKET_ITEMS, S.OFF_BAG_ITEMS, S.BAG_ITEMS_COUNT},
    }
    for _, choice in ipairs(choices) do
      local item, pocket, offset, capacity = table.unpack(choice)
      local before = L.itemCount(item)
      if before > 0 then
        local map, x, y = L.mapId(), L.pos()
        openBag()
        selectItem(item, pocket, offset, capacity, 0)
        L.tap(K.A)
        L.waitUntil(function()
          if L.itemCount(item) == before - 1 and L.partyHp(0) > hp then return true end
          L.tap(K.A); L.wait(8)
          return false
        end, 1800, "real medicine consumption and HP recovery")
        closeMenus()
        local ax, ay = L.pos()
        L.expect(L.mapId() == map and ax == x and ay == y, "healing preserves the actual field position")
        L.expect(L.itemCount(item) == before - 1, "healing consumes exactly one owned item")
        L.log(string.format("PILOT healed item=%d count=%d->%d hp=%d->%d/%d",
                            item, before, L.itemCount(item), hp, L.partyHp(0), maxHp))
        L.shot("natural_field_heal")
        return
      end
    end
    if homeReachable then restAtHome() end
    if clinicReachable then restAtAsclepeion() end
  end

  local function openParty()
    L.tap(K.START)
    L.waitUntil(function() return L.taskRunning("Task_ShowStartMenu") end, 300, "the start menu")
    L.wait(25)
    local count, target = emu:read8(S.sNumStartMenuActions), nil
    for i = 0, count - 1 do
      if emu:read8(S.sCurrentStartMenuActions + i) == 1 then target = i end
    end
    L.expect(target ~= nil, "the native party action is available")
    for _ = 1, (target - emu:read8(S.sStartMenuCursorPos)) % count do L.tap(K.DOWN) end
    L.tap(K.A)
    L.waitUntil(function() return L.taskRunning("Task_HandleChooseMonInput") end, 1200, "the field party menu")
    L.wait(30)
  end

  local function leadWith(slot)
    if slot == 0 then return end
    local original, wanted = emu:read32(L.partyMon(0)), emu:read32(L.partyMon(slot))
    openParty()
    partySlot(slot); L.tap(K.A)
    L.waitUntil(function() return L.taskRunning("Task_HandleSelectionMenuInput") end, 300, "the field partner actions")
    -- Ichor has no field moves; SWITCH follows SUMMARY.
    L.wait(20); L.tap(K.DOWN); L.tap(K.A); L.wait(20)
    L.expect(emu:read8(S.gPartyMenu + S.OFF_PARTY_MENU_ACTION) == S.PARTY_ACTION_SWITCH, "native SWITCH is selected")
    partySlot(0); L.tap(K.A)
    L.waitUntil(function() return emu:read32(L.partyMon(0)) == wanted end, 900, "the actual party swap")
    L.waitUntil(function() return L.taskRunning("Task_HandleChooseMonInput") end, 900, "the native swap animation")
    closeMenus()
    L.expect(emu:read32(L.partyMon(slot)) == original, "the native swap preserves both partner identities")
  end

  local function giveHeldItem(slot, item, berry)
    if L.partyHeldItem(slot) ~= 0 then
      L.log("PILOT preserving party slot " .. slot .. "'s existing held item")
      return
    end
    local before = L.itemCount(item)
    L.expect(before > 0, "the collected boss-preparation item is owned")
    openBag()
    selectItem(item, berry and S.POCKET_BERRIES or S.POCKET_ITEMS,
               berry and S.OFF_BAG_BERRIES or S.OFF_BAG_ITEMS,
               berry and S.BAG_BERRIES_COUNT or S.BAG_ITEMS_COUNT, slot, true)
    L.tap(K.A)
    L.waitUntil(function()
      if L.partyHeldItem(slot) == item then return true end
      L.tap(K.A); L.wait(8)
      return false
    end, 1200, "the real held-item transfer")
    closeMenus()
    L.expect(L.itemCount(item) == before - 1, "GIVE removes exactly one owned item from the Bag")
    L.log("PILOT party slot " .. slot .. " now holds the real boss-preparation item " .. item)
    L.shot("natural_held_booster")
  end

  function P.prepareBoss()
    P.recover()
    local count = emu:read8(S.gPartiesCount + S.B_TRAINER_PLAYER)
    for slot = 0, count - 1 do
      if emu:read32(L.partyMon(slot)) == starterPersonality then leadWith(slot); break end
    end
    local hard = L.getVar(S.VAR_DIFFICULTY) == S.DIFFICULTY_HARD
    local item = hard and S.ITEM_SITRUS_BERRY or ({[0] = S.ITEM_MIRACLE_SEED, S.ITEM_CHARCOAL, S.ITEM_MYSTIC_WATER})[starter]
    L.expect(item ~= nil, "the selected starter has a native held-item plan")
    giveHeldItem(0, item, hard)
    for slot = 1, count - 1 do
      if L.partySpecies(slot) == S.SPECIES_PEBBLITH then
        giveHeldItem(slot, S.ITEM_HARD_STONE, false)
      elseif L.partyHasType(slot, S.TYPE_GRASS) and L.itemCount(S.ITEM_MIRACLE_SEED) > 0 then
        giveHeldItem(slot, S.ITEM_MIRACLE_SEED, false)
      end
    end
  end

  function P.trainKallisteTeam()
    L.expect(L.mapId() == S.MAP_AKTI and L.idle(), "the training walk starts in Akti")
    local targetLevel = L.getVar(S.VAR_DIFFICULTY) == S.DIFFICULTY_HARD and 14 or 10
    L.log("PILOT Kalliste training target=" .. targetLevel)
    local x, y = L.pos()
    restAtAsclepeion()
    L.leaveEdge("down", S.MAP_ROUTE1)
    L.leaveEdge("right", S.MAP_KRONION)
    local g, patch = L.grid(), nil
    for py = 0, g.h - 1 do
      for px = 0, g.w - 2 do
        local _, blocked, behavior = g.tile(px, py)
        local _, blocked2, behavior2 = g.tile(px + 1, py)
        if not patch and not blocked and not blocked2 and behavior == S.MB_TALL_GRASS
           and behavior2 == S.MB_TALL_GRASS and not g.people[px .. "," .. py]
           and not g.people[(px + 1) .. "," .. py] and not g.coords[px .. "," .. py]
           and not g.coords[(px + 1) .. "," .. py] and L.canReachNextTo(px, py) then
          patch = {px, py}
        end
      end
    end
    L.expect(patch ~= nil, "a real reachable grass patch is available")
    L.go(patch[1], patch[2])
    local steps = 0
    P.training = true
    while true do
      local weakest, needsRest, hasCounter = 0, false, false
      for slot = 0, emu:read8(S.gPartiesCount + S.B_TRAINER_PLAYER) - 1 do
        if L.partySpecies(slot) == S.SPECIES_EOPEEP or L.partySpecies(slot) == S.SPECIES_PEBBLITH then hasCounter = true end
        if L.partyLevel(slot) < L.partyLevel(weakest) then weakest = slot end
        local hp, maxHp = L.partyHp(slot)
        local pp = 0
        for move = 0, S.MAX_MON_MOVES - 1 do pp = pp + L.partyPp(slot, move) end
        if hp * 4 <= maxHp * 3 or pp < 6 then needsRest = true end
      end
      if L.partyLevel(weakest) >= targetLevel and hasCounter then break end
      L.expect(hasCounter or L.itemCount(S.ITEM_POKE_BALL) > 0, "owned balls remain for a Normal-type counter")
      L.expect(steps < 6000, "Kalliste training stays within its walking budget")
      if needsRest then restAtHome() end
      leadWith(weakest)
      L.go(patch[1] + steps % 2, patch[2])
      steps = steps + 1
    end
    P.training = false
    local lead
    for slot = 0, emu:read8(S.gPartiesCount + S.B_TRAINER_PLAYER) - 1 do
      if emu:read32(L.partyMon(slot)) == starterPersonality then lead = slot end
    end
    L.expect(lead ~= nil, "the original starter remains in the trained party")
    leadWith(lead)
    L.leaveEdge("left", S.MAP_ROUTE1)
    L.leaveEdge("up", S.MAP_AKTI)
    restAtAsclepeion()
    returnToPosition(x, y)
    L.log("PILOT completed real Kalliste team training; grass steps=" .. steps)
    L.shot("natural_trained_team")
  end

  return P
end
