-- The Mystery sanctum (beat 23), run by tools/ichor/tests/sanctum.sh (read it first).
--
-- Plays with key presses on tools/ichor/tests/engine_lib.lua (slice_lib's walker: a
-- breadth-first search over the live map, one step at a time). People, signs, items,
-- triggers and warps are found by the script they run or the flag they set, so a moved
-- person never breaks the walk; a missing one fails with its name. The setup (the blob's
-- SanctumTest_SetupHeader) supplies progression; the full-Bag case temporarily fills
-- the key-item pocket and restores it before retrying. The missing-relic case
-- also clears and restores its ownership flag. Progression flags
-- is set by the game. The grain pits and the theft's line are kept off except where a
-- step means to tread on them.
--
-- Prints "SANCTUM ok ..." per check and "SANCTUM shot ..." per screenshot, and ends with
-- "SANCTUM done"; any failure prints "SANCTUM FAIL: ..." first.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
for k, v in pairs(dofile(L.OUT .. "sanctum_symbols.lua")) do S[k] = v end
S.SCRIPTS.EventScript_CutTree = S.EventScript_CutTree

local B1 = "EleusaSanctum_B1F_EventScript_"
local B2 = "EleusaSanctum_B2F_EventScript_"
local B3 = "EleusaSanctum_B3F_EventScript_"

local function expect(cond, what) L.expect(cond, what) end

local function fillKeyItemPocket()
  local pocket = L.sb1() + S.OFF_SB1_BAG + S.OFF_BAG_KEY_ITEMS
  local saved = {}
  local key = emu:read32(L.sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
  for i = 0, S.BAG_KEYITEMS_COUNT - 1 do
    saved[i] = { emu:read16(pocket + i * S.ITEM_SLOT_SIZE),
                 emu:read16(pocket + i * S.ITEM_SLOT_SIZE + 2) ~ key }
    emu:write16(pocket + i * S.ITEM_SLOT_SIZE, S.ITEM_HECATES_TORCH)
    emu:write16(pocket + i * S.ITEM_SLOT_SIZE + 2, 1 ~ key)
  end
  return function()
    -- Map transitions can relocate the save blocks and change the encryption key.
    local livePocket = L.sb1() + S.OFF_SB1_BAG + S.OFF_BAG_KEY_ITEMS
    local liveKey = emu:read32(L.sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
    for i = 0, S.BAG_KEYITEMS_COUNT - 1 do
      emu:write16(livePocket + i * S.ITEM_SLOT_SIZE, saved[i][1])
      emu:write16(livePocket + i * S.ITEM_SLOT_SIZE + 2, saved[i][2] ~ liveKey)
    end
  end
end

-- Battles at Eleusa's levels can cost the lead. slice_lib's L.battle presses A through
-- everything but the action and move menus, which can't choose who comes out next; this
-- one does what a player does, and otherwise plays like it: trainers (and wild Pokemon
-- that won't let the player go) are fought with the first move, other wild ones run from.
-- settle() calls L.battle, so replacing it covers every battle in a scene.
local function controller(name) return emu:read32(S.gBattlerControllerFuncs) == (S[name] | 1) end
function L.battle()
  L.waitUntil(L.inBattle, 1200, "the battle to start")
  local trainer = L.isTrainerBattle()
  local rec = { trainer = trainer, song = 0, start = L.now() }
  local t0, turns, picks = L.now(), 0, 0
  while not L.inOverworld() do
    if L.on("CB2_UpdatePartyMenu") then
      -- the lead fainted: send out the next one that can still fight. The cursor
      -- starts on the lead (the big left panel); RIGHT goes to the second slot, DOWN on
      -- down the column, after B has closed a "no energy left" message.
      L.wait(30)
      picks = picks + 1
      if picks == 1 then L.tap(K.RIGHT) else L.tap(K.B); L.wait(12); L.tap(K.DOWN) end
      L.wait(8); L.tap(K.A); L.wait(24); L.tap(K.A); L.wait(40)
    elseif L.on("CB2_EvolutionSceneUpdate") then
      L.tap(K.A); L.wait(6)
    elseif L.inBattle() and controller("HandleInputChooseAction") then
      if rec.song == 0 then
        rec.song = L.playingHeader()
        rec.shot = L.shot(trainer and "battle" or "wild_battle")
      end
      turns = turns + 1
      if trainer or turns > 3 then
        L.tap(K.UP); L.tap(K.LEFT); L.tap(K.A)        -- FIGHT
      else
        L.tap(K.DOWN); L.tap(K.RIGHT); L.tap(K.A)     -- RUN
      end
      L.wait(4)
    elseif L.inBattle() and controller("HandleInputChooseMove") then
      L.tap(K.UP); L.tap(K.LEFT); L.tap(K.A)          -- the first move
      L.wait(4)
    else
      L.tap(K.A); L.wait(4)
    end
    if L.now() - t0 > 40000 then L.shot("stuck_battle"); L.fail("a battle never ended") end
  end
  rec.outcome = emu:read8(S.gBattleOutcome)
  rec.turns = turns
  L.battles[#L.battles + 1] = rec
  L.log(string.format("BATTLE %s outcome %d song %s turns %d frames %d", trainer and "trainer" or "wild",
                      rec.outcome, L.songName(rec.song), turns, L.now() - rec.start))
  return rec
end
local function flash() return emu:read8(L.sb1() + S.OFF_SB1_FLASH) end
local function tile(x, y) return (L.grid().tile(x, y)) end
local function favor(god) return emu:read8(L.ichor() + S.OFF_ICHOR_FAVOR + god) end
local function lastBattle() return L.battles[#L.battles] end

local function talk(target, what, opts)
  local boxes = L.talk(target, opts)
  expect((boxes or 0) >= 1, string.format("%s: %d message box(es)", what, boxes or 0))
  return boxes
end

-- Hurt the lead, so a heal can be seen.
local function hurt()
  emu:write16(L.partyMon(0) + S.OFF_MON_HP, 1)
  local hp = L.partyHp(0)
  expect(hp == 1, "the lead is down to 1 HP")
end
local function healed(what)
  local hp, maxhp = L.partyHp(0)
  expect(hp == maxhp and hp > 1, string.format("%s heals the party (HP %d/%d)", what, hp, maxhp))
end

-- A hidden item, picked up facing it from `stand`, reached by way of `via` so the
-- follower (who trails a step behind) doesn't end up standing on the item's tile.
local function pickHidden(flag, via, stand, key, what)
  L.go(via[1], via[2])
  L.go(stand[1], stand[2])
  L.face(key)
  L.tap(K.A)
  L.settle()
  expect(L.getFlag(flag), what)
end

local function fight(target, trainer, what)
  if not L.defeated(trainer) then
    L.talk(target)
    L.settle()
  end
  expect(L.defeated(trainer), what .. " beaten")
  local rec = lastBattle()
  expect(rec and rec.trainer and rec.outcome == S.B_OUTCOME_WON, what .. ": a trainer battle, won")
  return rec
end

-- --- B1F: the granaries (23A) -----------------------------------------------------------------

local function granaries()
  L.setBeat("b1f", false)
  L.runHeader("SanctumTest_SetupHeader", { noSettle = true })
  L.waitUntil(function() return L.mapId() == S.MAP_B1F and L.inOverworld() end, 3000, "the warp to B1F")
  L.wait(20)
  -- 23A plays on arrival
  L.settle({ every = true })
  expect(L.mapId() == S.MAP_B1F, "at the foot of the Anaktoron's stair, on B1F")
  expect(L.getFlag(S.FLAG_ARRIVED), "beat 23A played (FLAG_ICHOR_SANCTUM_ARRIVED)")
  expect(L.mapMusic() == S.MUS_SANCTUM, "the sanctum plays MUS_ICHOR_TEMPLE_DEMETER")
  expect(flash() == 3, string.format("the granaries are dark: flash level %d (the Torch's 3)", flash()))
  local x, y = L.pos()
  expect(x == 5 and y == 3, string.format("the player stands on the stair (%d,%d)", x, y))
  L.shot("b1f_after_23a")
  local chloe = L.npc(B1 .. "Chloe")
  expect(chloe.present, "Chloe holds the stair")
  -- Chloe heals
  hurt()
  talk(chloe, "Chloe: Hold still")
  healed("Chloe")
  -- Alethea and her grunt are gone once the stair hall is out of sight
  local alethea = L.npc(B1 .. "Alethea")
  expect(alethea.present, "Alethea is fighting the lamp grunt behind the column")
  L.shot("b1f_alethea_fight")
  -- the first brazier: teach
  talk(L.sign(B1 .. "Brazier0"), "the stair hall's brazier", { shots = { [1] = "b1f_brazier_lit" } })
  expect(L.getFlag(S.FLAG_BRAZIER_0), "the stair hall's brazier lit (FLAG_ICHOR_BRAZIERS_START + 0x18)")
  expect(tile(9, 5) == S.MT_BRAZIER_LIT_00, string.format("its bowl burns (metatile 0x%03X)", tile(9, 5) or 0))
  expect(flash() == 0, "its stretch is lit: flash level 0")
  L.shot("b1f_stair_hall_lit")
  L.go(5, 10)
  expect(flash() == 3, string.format("out in the gallery the dark comes back (flash %d)", flash()))
  expect(L.objectAt(alethea.localId) == nil, "Alethea and the grunt are gone from the screen")
  -- Bolos's side pit: the optional grunt, the Hyper Potion behind him
  local rec = fight(L.npc(B1 .. "Bolos"), S.TRAINER_BOLOS, "Bolos")
  expect(rec.song == L.songHeader(S.MUS_BATTLE_TITAN), "Bolos fights to the Titanborn's music")
  L.talk(L.ball(S.FLAG_ITEM_HYPER_POTION))
  expect(L.getFlag(S.FLAG_ITEM_HYPER_POTION) and L.itemCount(S.ITEM_HYPER_POTION) >= 1, "the Hyper Potion taken")
  -- the second and third braziers, the dig behind the great jar, the sealed granary's seed
  talk(L.sign(B1 .. "Brazier1"), "bay C's brazier")
  expect(L.getFlag(S.FLAG_BRAZIER_1) and flash() == 0, "bay C's brazier lights the upper gallery")
  expect(L.itemCount(S.ITEM_TROWEL) == 1, "the sanctum fixture carries the real Trowel")
  expect(not L.getFlag(S.FLAG_DIG_SHERD), "the fixed granary find starts unclaimed")
  talk(L.sign(B1 .. "DigSpot"), "the dig behind the great jar", { every = true })
  expect(L.getFlag(S.FLAG_DIG_SHERD) and L.getFlag(S.FLAG_PERSEPHONE_SHERDS),
         "the granary's real find is a Persephone sherd")
  talk(L.sign(B1 .. "DigSpot"), "the granary dig again")
  local sherds = 0
  for i = 0, 3 do if L.getFlag(S.FLAG_PERSEPHONE_SHERDS + i) then sherds = sherds + 1 end end
  expect(sherds == 1, "the fixed granary dig cannot give a second sherd")
  talk(L.sign(B1 .. "Brazier2"), "the Ploutonion landing's brazier")
  expect(L.getFlag(S.FLAG_BRAZIER_2), "the Ploutonion landing's brazier lit")
  L.shot("b1f_landing_lit")
  L.talk(L.hidden(S.FLAG_HIDDEN_SEED))
  expect(L.getFlag(S.FLAG_HIDDEN_SEED), "the hidden Miracle Seed found in the sealed granary")
  -- Krokalos watches the narrow way down: the walk to the steps meets him
  L.go(29, 22)
  L.settle()
  expect(L.defeated(S.TRAINER_KROKALOS), "Krokalos stops the player at the narrow way down")
  talk(L.sign(B1 .. "Brazier3"), "the apse's brazier")
  expect(L.getFlag(S.FLAG_BRAZIER_3), "the apse's brazier lit")
  L.shot("b1f_apse_lit")
  L.useWarp(S.MAP_B2F)
  expect(L.mapId() == S.MAP_B2F, "down the steps to the Hall of the Kore")
end

-- --- B2F: the Hall of the Kore (23B) ---------------------------------------------------------

local function hall()
  L.setBeat("b2f", false)
  local pits = L.triggers(B2 .. "Pit")
  L.keepOff[S.MAP_B2F] = pits
  expect(flash() == 3, "the hall is dark")
  -- the hall's head: Hyperion's voice from the far stair
  local voice = L.triggers(B2 .. "Voice")
  expect(not L.goTrigger(voice), "the voice line fires at the hall's head")
  L.settle({ every = true })
  expect(L.getFlag(S.FLAG_VOICE), "Hyperion's voice heard (FLAG_ICHOR_SANCTUM_VOICE)")
  talk(L.sign(B2 .. "Fresco1"), "the first fresco", { shots = { [1] = "b2f_fresco1" } })
  -- a step off the chalk: down a grain pit, back to the court
  L.go(11, 31)
  L.face(K.UP)
  emu:addKey(K.UP); L.wait(12); emu:clearKey(K.UP)
  L.settle()
  local x, y = L.pos()
  expect(L.mapId() == S.MAP_B2F and x == 12 and y == 34, string.format("a grain pit drops the player in the court (%d,%d)", x, y))
  -- along the chalk to the near bridge, the Super Potion, the second fresco
  L.go(11, 23)
  L.shot("b2f_across_the_pits")
  L.talk(L.ball(S.FLAG_ITEM_SUPER_POTION_B2F))
  expect(L.getFlag(S.FLAG_ITEM_SUPER_POTION_B2F), "the Super Potion by the second fresco")
  talk(L.sign(B2 .. "Fresco2"), "the second fresco")
  -- the spring: the midpoint rest, and the Ether in its overflow
  hurt()
  talk(L.sign(B2 .. "Spring"), "the iron-tasting spring", { shots = { [1] = "b2f_spring" } })
  healed("The spring")
  pickHidden(S.FLAG_HIDDEN_ETHER, { 5, 20 }, { 4, 20 }, K.UP, "the Ether in the basin's overflow")
  talk(L.sign(B2 .. "Fresco3"), "the third fresco")
  -- Konis holds the doorway to the far stair: she sees the player step out of it
  L.go(13, 7)
  L.go(13, 5)
  L.settle()
  local kx, ky = L.objectAt(L.npc(B2 .. "Konis").localId)
  expect(not (kx == 13 and ky == 6), "Konis doesn't stand in the doorway after her battle")
  expect(L.defeated(S.TRAINER_KONIS), "Konis beaten at her doorway")
  talk(L.sign(B2 .. "Fresco4"), "the fourth fresco", { shots = { [1] = "b2f_fresco4" } })
  -- Gaios in the fresco alcove, and the TM Dig the Titans left
  fight(L.npc(B2 .. "Gaios"), S.TRAINER_GAIOS, "Gaios")
  L.talk(L.ball(S.FLAG_ITEM_TM_DIG))
  expect(L.getFlag(S.FLAG_ITEM_TM_DIG) and L.itemCount(S.ITEM_TM28) >= 1, "TM28 Dig taken from the alcove")
  L.useWarp(S.MAP_B3F)
  expect(L.mapId() == S.MAP_B3F, "down the far stair to the deepest granary")
end

-- --- B3F: Hyperion (23C) ---------------------------------------------------------------------

local function vault()
  L.setBeat("b3f", false)
  local line = L.triggers(B3 .. "Theft")
  L.keepOff[S.MAP_B3F] = line
  L.shot("b3f_arrival")
  -- the sickle can be looked at before the scene
  talk(L.sign(B3 .. "Sickle"), "the bronze sickle in the dust")
  local restorePocket = fillKeyItemPocket()
  L.keepOff[S.MAP_B3F] = nil
  local before = #L.battles
  expect(not L.goTrigger(line), "the line, five steps from the chest, starts the theft")
  L.settle({ every = true })
  expect(#L.battles == before + 1, "one battle in the scene")
  local rec = lastBattle()
  expect(rec.trainer and rec.outcome == S.B_OUTCOME_WON, "Hyperion beaten")
  expect(rec.song == L.songHeader(S.MUS_BATTLE_ADMIN),
         "Hyperion fights to MUS_ICHOR_BATTLE_ADMIN (" .. L.songName(rec.song) .. ")")
  expect(L.defeated(S.TRAINER_HYPERION), "TRAINER_ICHOR_HYPERION_1's flag set")
  expect(L.getFlag(S.FLAG_FRAGMENT_STOLEN), "the shard is gone up the tunnel (FLAG_ICHOR_FRAGMENT_STOLEN)")
  expect(L.getFlag(S.FLAG_HIDE_HYPERION), "Hyperion gone, the tunnel caved in")
  expect(L.mapId() == S.MAP_B3F and not L.getFlag(S.FLAG_GOT_SICKLE),
         "a full key-item pocket cannot skip the sickle reward or start departure")
  local beforeFavor = favor(S.ICHOR_GOD_DEMETER)
  restorePocket()
  talk(L.sign(B3 .. "Sickle"), "the sickle can be collected after making room", { every = true })
  expect(favor(S.ICHOR_GOD_DEMETER) == beforeFavor + 10,
         "the successful retry grants Demeter's myth-quest Favor once")
  expect(L.getFlag(S.FLAG_GOT_SICKLE) and L.itemCount(S.ITEM_DEMETERS_SICKLE) == 1, "Demeter's Sickle received")
  expect(favor(S.ICHOR_GOD_DEMETER) >= 10, string.format("Demeter's Favor +10 (%d)", favor(S.ICHOR_GOD_DEMETER)))
  local x, y = L.pos()
  expect(L.mapId() == S.MAP_ELEUSA and x == 25 and y == 12,
         string.format("faded out to the Telesterion's steps, outside (%d,%d)", x, y))
  L.shot("telesterion_steps")
  expect(L.getFlag(S.FLAG_KLEON_LEFT), "Kleon leaves for Thyrsa after the sickle")
  expect(not L.getFlag(S.FLAG_ACT1_COMPLETE) and not L.getFlag(S.FLAG_BADGE04_GET),
         "departure grants neither Act I completion nor a fourth Laurel")
end

-- --- Back down, and the climb back ----------------------------------------------------------

local function climb()
  L.setBeat("climb", false)
  L.runHeader("SanctumTest_BackDownHeader", { noSettle = true })
  L.waitUntil(function() return L.mapId() == S.MAP_B3F and L.idle() end, 3000, "the warp back to B3F")
  L.wait(20)
  expect(tile(15, 10) == S.MT_BOULDER or tile(15, 10) == S.MT_ROCK_PILE, "the tunnel is caved in")
  expect(tile(14, 12) == S.MT_DIG_CRYPT, "the cave-in bared the old foundations: a dig")
  expect(not L.getFlag(S.FLAG_DIG_PAGE_II) and not L.getFlag(S.FLAG_PAGE_II),
         "Daedalus's exposed page starts unclaimed")
  -- the line no longer plays anything
  local line = L.triggers(B3 .. "Theft")
  expect(L.goTrigger(line), "the line is quiet after the theft")
  talk(L.sign(B3 .. "Tunnel"), "the caved-in tunnel", { shots = { [1] = "b3f_tunnel" } })
  talk(L.sign(B3 .. "DigSpot"), "Daedalus's page in the exposed foundations", { every = true })
  expect(L.getFlag(S.FLAG_DIG_PAGE_II) and L.getFlag(S.FLAG_PAGE_II),
         "actual excavation grants Daedalus's second page")
  local bagBefore = L.snapshot(L.sb1() + S.OFF_SB1_BAG, S.BAG_SIZE)
  local pagesBefore = {}
  for i = 0, 6 do pagesBefore[i] = L.getFlag(S.FLAG_PAGE_II - 1 + i) end
  talk(L.sign(B3 .. "DigSpot"), "the foundations after collecting the page")
  local unchanged = L.snapshot(L.sb1() + S.OFF_SB1_BAG, S.BAG_SIZE) == bagBefore
  for i, owned in pairs(pagesBefore) do
    if L.getFlag(S.FLAG_PAGE_II - 1 + i) ~= owned then unchanged = false end
  end
  expect(unchanged and L.getFlag(S.FLAG_DIG_PAGE_II), "the fixed page cannot be excavated twice")
  L.talk(L.ball(S.FLAG_ITEM_SOFT_SAND))
  expect(L.getFlag(S.FLAG_ITEM_SOFT_SAND) and L.itemCount(S.ITEM_SOFT_SAND) >= 1, "the Soft Sand at the tunnel's mouth")
  pickHidden(S.FLAG_HIDDEN_OBOL, { 3, 11 }, { 2, 11 }, K.UP, "the Bronze Obol in the oldest granary's dust")
  -- the next battle's music is the ordinary one again: a wild battle in the vault
  L.setVar(S.VAR_REPEL_STEP_COUNT, 0)
  local before = #L.battles
  L.go(8, 7)
  for i = 1, 400 do
    if #L.battles > before then break end
    local r = L.step((i % 2 == 0) and K.LEFT or K.RIGHT)
    if r == "taken" or L.inBattle() then L.settle() end
  end
  L.setVar(S.VAR_REPEL_STEP_COUNT, 999)
  expect(#L.battles > before and not lastBattle().trainer, "a wild Pokemon in the deepest granary")
  expect(lastBattle().song == L.songHeader(S.MUS_BATTLE_WILD_E),
         "the next battle plays the ordinary wild music (" .. L.songName(lastBattle().song) .. ")")
  -- up the three floors
  L.useWarp(S.MAP_B2F)
  expect(L.mapId() == S.MAP_B2F, "up to the Hall of the Kore")
  expect(L.npc(B2 .. "Konis").present == false, "the grunts are gone after the theft")
  L.keepOff[S.MAP_B2F] = L.triggers(B2 .. "Pit")
  L.useWarp(S.MAP_B1F)
  expect(L.mapId() == S.MAP_B1F, "up to the granaries")
  L.go(5, 4)
  expect(L.objectAt(L.npc(B1 .. "Chloe").localId) == nil, "Chloe has left the stair")
end

local function closingPresentation(branch, choice, answer)
  local file = assert(io.open("graphics/ichor/tablet_back.4bpp", "rb"))
  local picture = file:read("a")
  file:close()
  local seenPicture, hiddenPicture, seenCard = false, false, false
  local savedPalette, savedFadedPalette = {}, {}
  local opts = { every = true, menuChoice = choice, answers = { answer } }
  opts.stop = function()
    local encoded = emu:read8(S.sScenePictureWindow)
    if encoded ~= 0 and not seenPicture then
      seenPicture = true
      local window = S.gWindows + (encoded - 1) * S.WINDOW_SIZE
      expect(emu:read8(window + S.OFF_WINDOW_WIDTH) == 8
             and emu:read8(window + S.OFF_WINDOW_HEIGHT) == 8,
             branch .. ": the tablet has its own 64x64 picture window")
      local tiles = emu:read32(window + S.OFF_WINDOW_TILES)
      expect(#picture == 2048, "the tablet asset is exactly one 64x64 4bpp panel")
      for i = 0, 2047 do
        if emu:read8(tiles + i) ~= picture:byte(i + 1) then
          L.fail(branch .. ": the tablet picture differs at byte " .. i)
        end
      end
      expect(true, branch .. ": all tablet pixels match the actual compiled art")
      expect(emu:read32(S.gSpeakerName) == S.EleusaVillage_TempleOfDemeter_Text_NameDaphne,
             branch .. ": Daphne is still named while explaining the tablet")
      L.wait(34)
      L.shot(branch .. "_tablet")
    elseif encoded == 0 and seenPicture and not hiddenPicture then
      hiddenPicture = true
      for i = 0, 15 do
        if emu:read16(S.gPlttBufferUnfaded + 13 * 32 + i * 2) ~= savedPalette[i]
           or emu:read16(S.gPlttBufferFaded + 13 * 32 + i * 2) ~= savedFadedPalette[i] then
          L.fail(branch .. ": picture palette color " .. i .. " was not restored")
        end
      end
      expect(true, branch .. ": the original unfaded and displayed picture palettes are restored")
      expect(emu:read32(S.gSpeakerName) == S.EleusaVillage_TempleOfDemeter_Text_NameDaphne,
             branch .. ": Daphne remains named after the picture closes")
    elseif encoded == 0 and not seenPicture then
      for i = 0, 15 do
        savedPalette[i] = emu:read16(S.gPlttBufferUnfaded + 13 * 32 + i * 2)
        savedFadedPalette[i] = emu:read16(S.gPlttBufferFaded + 13 * 32 + i * 2)
      end
    end
    local card = emu:read8(S.sActOneCardWindow)
    if card ~= 0 and not seenCard then
      seenCard = true
      expect(hiddenPicture, branch .. ": the tablet is released before the title")
      local window = S.gWindows + (card - 1) * S.WINDOW_SIZE
      expect(emu:read8(window + S.OFF_WINDOW_WIDTH) == 28
             and emu:read8(window + S.OFF_WINDOW_HEIGHT) == 12,
             branch .. ": Act I uses a dedicated centered title window")
      L.wait(75)
      expect(emu:read8(S.sActOneCardWindow) == card,
             branch .. ": the title waits for acknowledgment instead of auto-closing")
      L.shot(branch .. "_title")
      L.tap(choice == 0 and K.B or K.A)
    end
    return false
  end
  return opts, function()
    expect(seenPicture and hiddenPicture and seenCard,
           branch .. ": the live scene shows and closes both presentation windows")
    expect(emu:read8(S.sScenePictureWindow) == 0 and emu:read8(S.sActOneCardWindow) == 0,
           branch .. ": neither scene window survives the return outside")
  end
end

local function revelation()
  local daphne = "EleusaVillage_TempleOfDemeter_EventScript_Daphne"
  L.setBeat("revelation_full_bag", false)
  expect(emu:saveStateFile(L.OUT .. "before_revelation.ss", 31), "saved the revelation entry")
  local restorePocket = fillKeyItemPocket()
  L.useWarp(S.MAP_TELESTERION, true)
  L.settle({ every = true })
  expect(not L.getFlag(S.FLAG_REVELATION) and not L.getFlag(S.FLAG_ACT1_COMPLETE)
         and L.itemCount(S.ITEM_STAR_CHART) == 0,
         "a full key-item pocket leaves the scene and reward available")
  expect(L.npc(daphne).present, "Daphne stays to retry when the Bag is full")
  expect(emu:read8(S.sScenePictureWindow) == 0 and emu:read8(S.sActOneCardWindow) == 0,
         "the full-Bag refusal does not allocate scene windows")
  restorePocket()
  local opts, checkPresentation = closingPresentation("why", 0, "no")
  L.talk(L.npc(daphne), opts)
  checkPresentation()
  expect(L.mapId() == S.MAP_ELEUSA and L.getFlag(S.FLAG_ACT1_COMPLETE),
         "making room and speaking to Daphne completes Act I")
  expect(L.getFlag(S.FLAG_REVELATION) and L.getFlag(S.FLAG_GOT_STAR_CHART)
         and L.itemCount(S.ITEM_STAR_CHART) == 1,
         "WHY? and declining home grant one real Star Chart")
  expect(not L.getFlag(S.FLAG_BADGE04_GET), "Act I completion does not grant Laurel 4")

  expect(emu:loadStateFile(L.OUT .. "before_revelation.ss", 31), "restored the other dialogue branch")
  L.setBeat("revelation_other_branch", false)
  opts, checkPresentation = closingPresentation("how", 1, "yes")
  L.useWarp(S.MAP_TELESTERION, opts)
  L.settle(opts)
  checkPresentation()
  expect(L.mapId() == S.MAP_ELEUSA and L.getFlag(S.FLAG_REVELATION)
         and L.getFlag(S.FLAG_ACT1_COMPLETE) and L.itemCount(S.ITEM_STAR_CHART) == 1,
         "HOW DO YOU KNOW? and offering to go home reach the same completion")

  L.setBeat("north_road", false)
  L.keepOff[S.MAP_ELEUSA] = L.triggers("EleusaVillage_EventScript_NorthRoadBarrier")
  L.go(45, 10)
  local ax, ay = L.objectAt(S.LOCALID_VILLAGE_ALETHEA)
  expect(ax == 44 and ay == 11, "Alethea waits by the vines after the revelation")
  L.talk(L.npc("EleusaVillage_EventScript_Alethea"), { every = true })
  local restorePocket = fillKeyItemPocket()
  L.setFlag(S.FLAG_GOT_SICKLE, false)
  L.talk(L.npc("EventScript_CutTree", 2), { every = true })
  expect(not L.getFlag(S.FLAG_NORTH_VINES_CUT) and L.npc("EventScript_CutTree", 2).present,
         "without Sickle ownership the vines remain closed")
  restorePocket()
  L.setFlag(S.FLAG_GOT_SICKLE, true)
  L.talk(L.npc("EventScript_CutTree", 2), { every = true, answers = { "no" } })
  expect(not L.getFlag(S.FLAG_NORTH_VINES_CUT), "declining to cut leaves the north-road gate closed")
  L.talk(L.npc("EventScript_CutTree", 2), { every = true, answers = { "yes" } })
  expect(L.getFlag(S.FLAG_NORTH_VINES_CUT) and not L.npc("EventScript_CutTree", 2).present,
         "the actual Sickle clears and saves the middle-west vine gate")
  L.go(45, 8)
  L.settle()
  expect(L.getFlag(S.FLAG_LEFT_WITH_ALETHEA) and not L.objectAt(S.LOCALID_VILLAGE_ALETHEA),
         "passing the cleared vines hides Alethea and saves her departure")
  for _, x in ipairs({ 45, 46 }) do
    L.go(x, 7)
    L.step(K.UP)
    L.settle({ every = true })
    local px, py = L.pos()
    expect(L.mapId() == S.MAP_ELEUSA and px == x and py == 7,
           "the herald turns back the north-road column " .. x)
  end
  L.useWarp(S.MAP_TELESTERION)
  L.settle()
  expect(not L.npc(daphne).present and not L.objectAt(S.LOCALID_REVELATION_ALETHEA),
         "the revelation actors are gone on reentry")
  expect(tile(2, 21) == S.MT_HALL_BRAZIER_LIT_00, "the autumn brazier is restored after Act I")
  expect(L.itemCount(S.ITEM_STAR_CHART) == 1, "reentry does not duplicate the Star Chart")
  L.runHeader("SanctumTest_SaveHeader")
  emu:reset()
  L.continueSave()
  expect(L.getFlag(S.FLAG_KLEON_LEFT) and L.getFlag(S.FLAG_REVELATION)
         and L.getFlag(S.FLAG_GOT_STAR_CHART) and L.getFlag(S.FLAG_ACT1_COMPLETE)
         and not L.getFlag(S.FLAG_BADGE04_GET) and L.itemCount(S.ITEM_STAR_CHART) == 1,
         "saving and CONTINUE preserve the real ending flags and Chart, without Laurel 4")
  expect(L.getFlag(S.FLAG_DIG_SHERD) and L.getFlag(S.FLAG_PERSEPHONE_SHERDS)
         and L.itemCount(S.ITEM_TROWEL) == 1,
         "saving and CONTINUE preserve the fixed Persephone sherd and real Trowel")
  expect(L.getFlag(S.FLAG_DIG_PAGE_II) and L.getFlag(S.FLAG_PAGE_II),
         "saving and CONTINUE preserve Daedalus's excavated second page")
  expect(not L.npc(daphne).present and not L.objectAt(S.LOCALID_REVELATION_ALETHEA),
         "saving and CONTINUE do not replay the revelation")
  L.useWarp(S.MAP_ELEUSA)
  L.settle()
  L.go(45, 10)
  expect(L.getFlag(S.FLAG_LEFT_WITH_ALETHEA) and not L.objectAt(S.LOCALID_VILLAGE_ALETHEA)
         and L.getFlag(S.FLAG_NORTH_VINES_CUT) and not L.npc("EventScript_CutTree", 2).present,
         "saving and CONTINUE preserve the cleared vines and Alethea's departure")
end

L.start(function()
  L.quickstart()
  granaries()
  hall()
  vault()
  climb()
  revelation()
  L.log("ok the sanctum is done")
end)
