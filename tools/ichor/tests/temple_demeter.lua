-- Eleusa's story, beats 19-22, run by tools/ichor/tests/temple_demeter.sh (read it first).
--
-- Plays with key presses on tools/ichor/tests/engine_lib.lua (slice_lib's walker: a
-- breadth-first search over the live map, one step at a time). People, signs and
-- triggers are found by the script they run, so a moved NPC never breaks the walk.
-- Setup runs one test-only script from temple_demeter_setup.s (the party, the badges,
-- the Torch, then the warp to Eleusa's west edge); everything after it is key presses,
-- with mGBA save states to play Chloe three ways from one moment.
--
-- Prints "DEMETER ok ..." per check and "DEMETER shot ..." per screenshot, and ends
-- with "DEMETER done"; any failure prints "DEMETER FAIL: ..." first.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
for k, v in pairs(dofile(L.OUT .. "demeter_symbols.lua")) do S[k] = v end

local V = "EleusaVillage_EventScript_"
local T = "EleusaVillage_TempleOfDemeter_EventScript_"
local expect = L.expect

local function flash() return emu:read8(L.sb1() + S.OFF_SB1_FLASH) end
local function favor(god) return emu:read8(L.ichor() + S.OFF_ICHOR_FAVOR + god) end
local function tile(x, y) return (L.grid().tile(x, y)) end

-- The hall's grain pits are black (floor.void) until boarded over: walks keep off them.
local function noPits(x, y) return tile(x, y) == S.MT_VOID end
local function opts(t) t = t or {}; t.avoid = noPits; return t end

local function talk(target, what, o)
  local boxes = L.talk(target, o)
  expect((boxes or 0) >= 1, string.format("%s: %d message box(es)", what, boxes or 0))
  return boxes
end

local function saveState(name)
  emu:saveStateFile(L.OUT .. name .. ".ss", 31)
  L.log("ok saved the state '" .. name .. "'")
end
local function loadState(name)
  emu:loadStateFile(L.OUT .. name .. ".ss", 31)
  L.wait(30)
  L.waitUntil(L.idle, 600, "control after loading '" .. name .. "'")
  L.log("ok back to the state '" .. name .. "'")
end

local function lastBattle() return L.battles[#L.battles] end

-- --- Setup: just in from Route 5 ------------------------------------------------------------

local function setup()
  L.setBeat("setup", false)
  L.quickstart()
  L.runHeader("DemeterTest_SetupHeader")
  local x, y = L.pos()
  expect(L.mapId() == S.MAP_ELEUSA and x == 0 and y == 25,
         string.format("on Eleusa's west edge, where Route 5 comes in (%d,%d)", x, y))
  expect(L.partyLevel(0) == 100, "a level-100 lead")
  expect(L.getFlag(S.FLAG_GOT_HECATES_TORCH), "Hecate's Torch in hand")
  expect(L.getFlag(S.FLAG_BADGE02_GET) and not L.getFlag(S.FLAG_BADGE03_GET), "the Herald Laurel, not yet the Harvest Laurel")
  expect(L.mapMusic() == S.MUS_ELEUSA, "Eleusa plays MUS_ICHOR_ELEUSA")
  L.shot("west_edge")
  saveState("arrival")
end

-- --- Beat 19: Krokis's gate -----------------------------------------------------------------

local function gate()
  L.setBeat("gate", false)
  expect(not L.getFlag(S.FLAG_SAFFRON_THREAD), "no saffron thread yet")
  local walked = L.go(12, 25, { trigger = true })
  expect(not walked, "Krokis's gate takes over on the road in")
  local boxes = L.settle({ every = true })
  expect(boxes >= 5, string.format("the saffron thread, three times: %d boxes", boxes))
  expect(L.getFlag(S.FLAG_SAFFRON_THREAD), "FLAG_ICHOR_SAFFRON_THREAD set")
  local x, y = L.pos()
  expect(x == 8 and y == 26, string.format("the player stepped up beside Krokis (%d,%d)", x, y))
  expect(L.getFlag(S.FLAG_ARRIVED_ELEUSA) and L.getFlag(S.FLAG_VISITED_ELEUSA),
         "beat 20: FLAG_ICHOR_ARRIVED_ELEUSA and the fly flag FLAG_ICHOR_VISITED_ELEUSA")
  L.shot("after_the_thread")
  -- once only: back out across the trigger and in again
  expect(L.go(3, 25, { trigger = true }), "back across the gate: nothing plays")
  expect(L.go(12, 25, { trigger = true }), "and in again: the thread doesn't replay")
  talk(L.npc(V .. "Krokis"), "Krokis afterwards (the damp)")
end

-- --- Beat 20: Kleon in the square ------------------------------------------------------------

local function square()
  L.setBeat("square", false)
  expect(not L.getFlag(S.FLAG_HIDE_KLEON_ELEUSA), "Kleon waits in the square")
  talk(L.npc(V .. "Kleon"), "Kleon before the trial", { shots = { [1] = "kleon_square" } })
  expect(L.npc(V .. "Kleon").present, "Kleon is there to talk to")
  expect(L.getFlag(S.FLAG_HIDE_PROCESSION), "no procession before the Laurel")
end

-- --- Beat 21: the Lesser Mysteries ------------------------------------------------------------

local function rite()
  L.setBeat("rite", false)
  L.useWarp(S.MAP_TEMPLE_DEMETER)
  expect(L.mapId() == S.MAP_TEMPLE_DEMETER, "into the Telesterion")
  expect(L.mapMusic() == S.MUS_TEMPLE_DEMETER, "the hall plays MUS_ICHOR_TEMPLE_DEMETER")
  expect(flash() == 3, string.format("the hall is dark: flash %d, the Torch's radius", flash()))
  L.shot("hall_entry")
  talk(L.npc(T .. "Doso"), "Doso's welcome", opts({ every = true }))
  expect(L.getFlag(S.FLAG_MET_DOSO), "Doso's welcome heard")
  -- out of turn: Spring won't take while Autumn is cold
  talk(L.sign(T .. "BrazierSpring"), "Spring, out of turn", opts())
  expect(not L.getFlag(S.FLAG_BRAZIER_SPRING), "Spring stays cold out of turn")
  -- the trail, each acolyte a checkpoint: Autumn (Kallidike), Winter (Eumolpos), Spring (Melissa)
  for _, s in ipairs({ { "Autumn", "Kallidike", "KALLIDIKE" }, { "Winter", "Eumolpos", "EUMOLPOS" },
                       { "Spring", "Melissa", "MELISSA" } }) do
    talk(L.npc(T .. s[2]), s[2], opts())
    expect(L.defeated(S["TRAINER_" .. s[3]]), s[2] .. " beaten")
    talk(L.sign(T .. "Brazier" .. s[1]), s[1] .. " lit", opts({ shots = { [3] = "lit_" .. s[1] } }))
    expect(L.getFlag(S["FLAG_BRAZIER_" .. string.upper(s[1])]), s[1] .. "'s flag set")
    expect(flash() == 0, s[1] .. "'s quarter is bright")
  end
  -- the aisle is dark again
  L.go(13, 15, opts())
  expect(flash() == 3, string.format("the aisle is dark again (flash %d)", flash()))
  -- a misstep into a grain pit: the tiers by Spring, and Doso's chalk hint
  L.go(15, 20, opts())
  L.tap(K.RIGHT, 8)
  L.settle()
  local px, py = L.pos()
  expect(px == 23 and py == 4 and L.getFlag(S.FLAG_PIT_FALL),
         string.format("a pit drops you on the tiers by Spring (%d,%d)", px, py))
  talk(L.npc(T .. "Doso"), "Doso's chalk hint", opts())
  expect(L.getVar(S.VAR_DOSO_CHALK) == 1, "Doso gave the chalk hint after the fall")
  -- the master: along Hecate's chalk to Summer, and Chloe in the doorway
  talk(L.sign(T .. "BrazierSummer"), "Summer lit", opts({ every = true }))
  expect(L.getFlag(S.FLAG_BRAZIER_SUMMER) and L.getFlag(S.FLAG_MYSTERIES_DONE), "Summer lit: the Lesser Mysteries done")
  expect(not L.getFlag(S.FLAG_HIDE_CHLOE), "Chloe is revealed")
  -- back across the hall to her (the pits are still open)
  L.go(13, 16, opts())
  expect(L.npc(T .. "Chloe").present, "Chloe stands in the Anaktoron's doorway")
  L.shot("before_chloe")
  saveState("before_chloe")
end

-- The Laurel and what comes with it, after a won battle.
local function laurelChecks(how, trainer, other)
  expect(L.defeated(trainer) and not L.defeated(other), how .. ": the right Chloe beaten")
  local rec = lastBattle()
  expect(rec.outcome == S.B_OUTCOME_WON, how .. ": won")
  expect(rec.song == L.songHeader(S.MUS_BATTLE_HIEROPHANT),
         how .. ": the Hierophant's battle music (the rival theme, as Kerykos's), got " .. L.songName(rec.song))
  expect(L.getFlag(S.FLAG_BADGE03_GET), how .. ": FLAG_BADGE03_GET, the Harvest Laurel")
  expect(L.getFlag(S.FLAG_GOT_TM_GIGA_DRAIN) and L.itemCount(S.ITEM_TM19) == 1, how .. ": TM19 Giga Drain")
  expect(L.getFlag(S.FLAG_CHLOE_RITE) and L.itemCount(S.ITEM_BARLEY_CAKE) >= 1, how .. ": Demeter's rite, a Barley Cake")
  expect(favor(S.ICHOR_GOD_DEMETER) >= S.ICHOR_FAVOR_LAUREL,
         string.format("%s: Demeter Favor %d (+15 for the Laurel)", how, favor(S.ICHOR_GOD_DEMETER)))
  for _, n in ipairs({ "KALLIDIKE", "EUMOLPOS", "MELISSA" }) do
    expect(L.defeated(S["TRAINER_" .. n]), how .. ": " .. n .. " counts as beaten")
  end
  expect(tile(17, 18) == S.MT_FLOOR and L.getVar(S.VAR_PITS_BOARDED) == 1, how .. ": the pits are boarded over")
end

local function chloe()
  L.setBeat("chloe", false)
  -- 1. Lost: the lead at 1 HP uses Leer; Chloe knocks it out and the player whites out.
  emu:write16(L.partyMon(0) + S.OFF_MON_HP, 1)
  L.battleMode = "lose"
  L.talk(L.npc(T .. "Chloe"), opts({ every = true }))
  L.battleMode = nil
  expect(lastBattle().outcome == S.B_OUTCOME_LOST, "lost to Chloe")
  expect(not L.getFlag(S.FLAG_BADGE03_GET), "no Laurel after a loss")
  expect(L.mapId() ~= S.MAP_TEMPLE_DEMETER, "whited out of the hall, to the last place of healing")
  L.shot("after_the_loss")
  loadState("before_chloe")
  -- 2. By night: Persenyx's team.
  L.runHeader("DemeterTest_NightHeader")
  talk(L.npc(T .. "Chloe"), "Chloe by night", opts({ every = true }))
  laurelChecks("by night", S.TRAINER_CHLOE_NIGHT, S.TRAINER_CHLOE_DAY)
  loadState("before_chloe")
  -- 3. By day: Korantha's. The run carries on from here.
  L.runHeader("DemeterTest_DayHeader")
  talk(L.npc(T .. "Chloe"), "Chloe by day", opts({ every = true }))
  laurelChecks("by day", S.TRAINER_CHLOE_DAY, S.TRAINER_CHLOE_NIGHT)
  L.shot("the_laurel")
  local before = #L.battles
  talk(L.npc(T .. "Chloe"), "Chloe after the Laurel", opts())
  expect(#L.battles == before, "no second battle with Chloe")
  talk(L.npc(T .. "Doso"), "Doso after the Laurel", opts())
end

-- --- Beat 22: the procession, and re-entering after the Laurel --------------------------------

local function procession()
  L.setBeat("procession", false)
  L.useWarp(S.MAP_ELEUSA, true)
  local boxes = L.settle({ every = true })
  expect(boxes >= 2, string.format("the procession arrives: %d boxes", boxes))
  expect(L.getFlag(S.FLAG_PROCESSION_ARRIVED), "FLAG_ICHOR_PROCESSION_ARRIVED")
  local x, y = L.pos()
  expect(x == 25 and y == 12, string.format("on the Telesterion's steps (%d,%d)", x, y))
  expect(L.npc(V .. "Alethea").present and L.npc(V .. "Kerykos").present, "Alethea and Kerykos are here")
  L.shot("procession")
  -- back in after the Laurel: the braziers burn, the pits are boarded, Chloe stays
  L.useWarp(S.MAP_TEMPLE_DEMETER)
  expect(tile(2, 21) == S.MT_BRAZIER_TOP_LIT and tile(24, 21) == S.MT_BRAZIER_TOP_LIT, "re-entry: the braziers burn")
  expect(tile(17, 18) == S.MT_FLOOR, "re-entry: the pits are boarded over")
  expect(not L.getFlag(S.FLAG_HIDE_CHLOE), "re-entry: Chloe in her doorway")
  local before = #L.battles
  talk(L.npc(T .. "Chloe"), "Chloe on re-entry", opts())
  expect(#L.battles == before and L.npc(T .. "Chloe").present, "re-entry: Chloe talks, no battle")
  L.shot("hall_after_the_laurel")
  L.useWarp(S.MAP_ELEUSA)
  expect(L.mapId() == S.MAP_ELEUSA, "out again: the procession's arrival doesn't replay")
  -- the square, the night before
  talk(L.npc(V .. "Kleon"), "Kleon after the trial", { shots = { [1] = "kleon_after_trial" } })
  talk(L.npc(V .. "Alethea"), "Alethea")
  talk(L.npc(V .. "Eudemos"), "Eudemos")
  talk(L.npc(V .. "Initiate2"), "an initiate")
end

local function mysteries()
  L.setBeat("mysteries", false)
  talk(L.npc(V .. "Kerykos"), "Kerykos, NO", { answers = { "no" } })
  expect(not L.getFlag(S.FLAG_MYSTERIES_BEGUN) and L.mapId() == S.MAP_ELEUSA, "NO: the doors stay open")
  -- the battle's intro, photographed as Kleon (from behind: his back pic) slides in beside the player
  local intro = false
  local function introShots()
    if not intro and L.inBattle() then
      intro = true
      for i, n in ipairs({ 40, 60, 60, 80 }) do L.wait(n); L.shot("multi_intro_" .. i) end
    end
    return false
  end
  talk(L.npc(V .. "Kerykos"), "Kerykos, YES: the night of the Mysteries",
       { answers = { "yes" }, every = true, limit = 40000, stop = introShots })
  expect(L.getFlag(S.FLAG_MYSTERIES_BEGUN), "FLAG_ICHOR_MYSTERIES_BEGUN")
  local rec = lastBattle()
  expect(rec and rec.trainer and rec.outcome == S.B_OUTCOME_WON, "the grunts beaten")
  local types = emu:read32(S.gBattleTypeFlags)
  expect(types & S.BATTLE_TYPE_MULTI ~= 0 and types & S.BATTLE_TYPE_INGAME_PARTNER ~= 0,
         "a multi battle with an in-game partner (Kleon)")
  expect(rec.song == L.songHeader(S.MUS_TITAN), "the Titans' battle music, got " .. L.songName(rec.song))
  expect(not L.getFlag(S.FLAG_NO_WHITEOUT), "FLAG_ICHOR_NO_WHITEOUT cleared after the battle")
  expect(L.getFlag(S.FLAG_MYSTERIES_NIGHT) and L.getFlag(S.FLAG_TELESTERION_MULTI) and L.getFlag(S.FLAG_SANCTUM_OPEN),
         "FLAG_ICHOR_MYSTERIES_NIGHT, _TELESTERION_MULTI and _SANCTUM_OPEN set")
  expect(L.mapId() == S.MAP_SANCTUM_B1F, "down the stair under the Anaktoron, into the sanctum (B1F)")
  L.shot("sanctum_b1f")
end

-- After the night: up through the Ploutonion, and the wrecked hall with Kleon at the door.
local function after()
  L.setBeat("after", false)
  L.useWarp(S.MAP_ELEUSA)
  expect(L.mapId() == S.MAP_ELEUSA, "back up through the Ploutonion's open gate")
  expect(L.getFlag(S.FLAG_HIDE_KLEON_ELEUSA) and L.getFlag(S.FLAG_HIDE_PROCESSION),
         "the square is empty: everyone is in the Telesterion")
  L.useWarp(S.MAP_TEMPLE_DEMETER)
  expect(tile(2, 22) == S.MT_OVERTURNED_L and tile(24, 22) == S.MT_OVERTURNED_L,
         "the front braziers lie overturned")
  expect(L.getFlag(S.FLAG_HIDE_CHLOE), "Chloe is below")
  expect(not L.getFlag(S.FLAG_HIDE_KLEON_TELESTERION), "Kleon is in the hall")
  -- (he stands where ON_TRANSITION put him, not on his template: walk up the aisle until he's on screen)
  L.go(13, 18, opts())
  local kleon = L.npc(T .. "Kleon")
  expect(kleon.present and kleon.x == 14 and kleon.y == 14, string.format("Kleon keeps the door (%d,%d)", kleon.x, kleon.y))
  talk(kleon, "Kleon at the door", opts())
  talk(L.sign(T .. "BrazierAutumn"), "the overturned brazier", opts())
  L.shot("wrecked_hall")
  L.useWarp(S.MAP_SANCTUM_B1F)
  expect(L.mapId() == S.MAP_SANCTUM_B1F, "the Anaktoron's stair leads down to B1F")
end

L.start(function()
  setup()
  gate()
  square()
  rite()
  chloe()
  procession()
  mysteries()
  after()
  L.log("ok the story is done")
end)
