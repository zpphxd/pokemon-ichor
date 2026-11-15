-- Side checks for the slice, run by tools/ichor/tests/slice_sidechecks.sh (read it first).
--
-- Each check loads a save state that slice_playthrough.lua left at the start of
-- a beat (build/slice/states/<beat>.ss), plays one thing with key presses and
-- checks the result: whiting out at each stage, losing a story battle and coming
-- back, leaving and re-entering a map mid-story, taking a gift twice, and a tour
-- of every start-menu screen for the look review. A check that fails logs
-- "CHECK FAIL <name>: ..." and the next one runs; BUG lines are findings.
--
-- Env: CHECKS_OUT (default build/slice_checks/), CHECKS_STATES (default
-- build/slice/states/), CHECKS_ONLY (a comma-separated list of check names).

local OUT = os.getenv("CHECKS_OUT") or "build/slice_checks/"
local STATES = os.getenv("CHECKS_STATES") or "build/slice/states/"
local L = dofile("tools/ichor/tests/slice_lib.lua")
L.init{ tag = "CHECK", out = OUT, symbols = os.getenv("CHECKS_SYMBOLS") or "build/slice/symbols.lua" }
local S, K = L.S, L.K
local emu = L.emu
local log, wait, tap, shot, settle, talk, go = L.log, L.wait, L.tap, L.shot, L.settle, L.talk, L.go
L.workarounds = true   -- a known softlock is logged as a BUG here, and the check carries on

local function load(state)
  wait(2)
  if not emu:loadStateFile(STATES .. state .. ".ss", 31) then L.fail("no save state " .. STATES .. state .. ".ss") end
  wait(10)
  if not L.idle() then settle() end
end

local HOME = { map = "MAP_HOUSE_1F", song = "MUS_ELAIA" }
local AKTI = { map = "MAP_ASCLEPEION", song = "MUS_ASCLEPEION" }
local E, R1, KH, AK, T = "ElaiaVillage_EventScript_", "KallisteRoute1_EventScript_",
                         "KallisteRoute1_KronionHill_EventScript_", "AktiTown_EventScript_",
                         "AktiTown_TempleOfHestia_EventScript_"

-- White out where the player stands and see where they wake.
local function whiteoutAt(state, want, label)
  load(state)
  local from, fx, fy = L.mapId(), L.pos()
  L.whiteOut()
  L.waitUntil(function() return L.mapId() ~= from and L.inOverworld() end, 4000, "the whiteout's warp")
  wait(60)
  shot("woke_" .. label)
  settle({ every = true })
  local m, x, y = L.mapId(), L.pos()
  local hp, maxHp = L.partyHp(0)
  log(string.format("note whiteout from map %d (%d,%d) woke on map %d at (%d,%d), HP %d/%d, playing %s",
                    from, fx, fy, m, x, y, hp, maxHp, L.song()))
  L.check(m == S[want.map], string.format("whiting out (%s) wakes on map %d (got %d)", label, S[want.map], m))
  L.check(hp == maxHp and hp > 0, string.format("... with the party healed (%d/%d)", hp, maxHp))
  L.check(L.playing(S[want.song]), string.format("... to the room's music (playing %s)", L.song()))
  L.check(L.idle(), "... and the player can move")
  shot("after_" .. label)
end

local CHECKS = {}
local function check(name, fn) CHECKS[#CHECKS + 1] = { name = name, fn = fn } end

-- 1. Elaia's well: the Relic Copper once, and nobody vanishes -------------------------------------
check("well_twice", function()
  load("04_elaia_after")
  local kid = L.npc(E .. "Kid")
  L.check(kid.present, "the kid with the Wooloo is in the village")
  talk(kid, { shotBefore = "kid" })                       -- VAR_LAST_TALKED is now the kid
  local n0 = L.itemCount(S.ITEM_RELIC_COPPER)
  talk(L.sign(E .. "Well"), { shotBefore = "well_first", every = true })
  local n1 = L.itemCount(S.ITEM_RELIC_COPPER)
  L.check(n1 == n0 + 1, string.format("the well gives one Relic Copper (%d -> %d)", n0, n1))
  shot("after_the_well")
  L.check(L.npc(E .. "Kid").present, "reading the well leaves the kid where he was")
  talk(L.sign(E .. "Well"), { shotBefore = "well_again", every = true })
  local n2 = L.itemCount(S.ITEM_RELIC_COPPER)
  L.check(n2 == n1, string.format("a second look in the well gives nothing more (%d -> %d)", n1, n2))
end)

-- 2. Whiting out at each stage -------------------------------------------------------------------
check("whiteout_elaia", function() whiteoutAt("05_route1", HOME, "elaia_after_kleon") end)
check("whiteout_route1", function() whiteoutAt("05_kronion_hill", HOME, "route1") end)
check("whiteout_kronion", function() whiteoutAt("05_road_open", HOME, "kronion_hill") end)
check("whiteout_akti_before_heal", function()
  -- SCRIPT.md beat 6 sets the respawn at the Asclepeion's first heal, not on arrival
  whiteoutAt("06_asclepeion", HOME, "akti_before_first_heal")
end)
check("whiteout_akti", function() whiteoutAt("06_agora", AKTI, "akti") end)
check("whiteout_temple", function() whiteoutAt("07_hearth_trial", AKTI, "temple") end)
check("whiteout_after_the_end", function() whiteoutAt("08_after", AKTI, "after_the_end") end)

-- 3. The torch goes out on a whiteout: the room is reset on the way back in -----------------------
check("trial_flame_whiteout", function()
  load("07_hearth_trial")
  talk(L.sign(T .. "GreatHearth"), { shotBefore = "take_flame" })
  L.check(L.getVar(S.VAR_HEARTH_TRIAL) == 1, "carrying a flame")
  L.whiteOut()
  L.waitUntil(function() return L.mapId() == S.MAP_ASCLEPEION and L.inOverworld() end, 4000, "the Asclepeion")
  wait(60); settle()
  L.useWarp(S.MAP_AKTI)
  L.useWarp(S.MAP_TEMPLE)
  shot("temple_again")
  L.check(L.getVar(S.VAR_HEARTH_TRIAL) == 0, string.format("the flame is gone on the way back in (trial %d)",
                                                            L.getVar(S.VAR_HEARTH_TRIAL)))
end)

-- 4. Re-entering maps after their scenes ------------------------------------------------------------
check("reentry_akademia", function()
  load("04_elaia_after")
  L.useWarp(S.MAP_AKADEMIA)
  wait(30)
  L.check(L.idle(), "no scene replays in the Akademia")
  shot("akademia_again")
  talk(L.npc("ElaiaVillage_Akademia_EventScript_Daphne"), { shotBefore = "daphne_after_kleon", every = true })
  talk(L.sign("ElaiaVillage_Akademia_EventScript_WallMap"), { shotBefore = "wall_map", every = true })
  L.useWarp(S.MAP_ELAIA)
  wait(30)
  L.check(L.idle() and not L.npc(E .. "Kleon").present, "Kleon is gone from the square and nothing replays")
  shot("square_again")
end)

check("reentry_kronion", function()
  load("05_road_open")
  L.leaveEdge("left", S.MAP_ROUTE1)
  L.leaveEdge("right", S.MAP_KRONION)
  L.check(L.goTrigger(L.triggers(KH .. "SummitScene")), "the summit scene does not replay")
  shot("summit_again")
  talk(L.sign(KH .. "Stele"), { shotBefore = "stele_again" })
  talk(L.sign(KH .. "Pit"), { shotBefore = "dark_stair_again", every = true })
end)

check("reentry_akti_arrival", function()
  load("06_asclepeion")
  L.leaveEdge("down", S.MAP_ROUTE1)
  L.leaveEdge("up", S.MAP_AKTI)
  wait(40)
  L.check(L.idle(), "Diktys's welcome does not replay")
  shot("akti_again")
end)

check("ending_after_leaving_akti", function()
  -- Part 1 has played (Alethea ran to the quay). Step into the Asclepeion and out,
  -- then go to the quay: part 2 should start; the doorstep should not replay part 1.
  load("08_harbor_part2")
  L.useWarp(S.MAP_ASCLEPEION)
  L.useWarp(S.MAP_AKTI)
  wait(30)
  shot("quay_from_asclepeion")
  local quay = L.triggers(AK .. "HarborPart2Row9", AK .. "HarborPart2Row10", AK .. "HarborPart2Row11")
  local started = not L.goTrigger(quay)
  shot("at_the_quay")
  L.check(started, "after a trip indoors, the quay still starts the ending (part 2)")
  if started then
    settle({ answers = { "no" } })
  else
    -- see whether part 1 replays on the temple doorstep
    local replay = not L.goTrigger(L.triggers(AK .. "HarborPart1"))
    shot("doorstep_again")
    L.check(not replay, "part 1 does not replay on the temple doorstep")
    settle({ every = true })
    if not L.goTrigger(quay) then settle({ answers = { "no" } }) end
  end
  L.check(L.getFlag(S.FLAG_SLICE_COMPLETE), "the slice can still be finished")
end)

-- 5. Losing a story battle and coming back -------------------------------------------------------------
check("lose_to_ione", function()
  load("07_ione")
  emu:write16(L.partyMon(0) + S.OFF_MON_HP, 1)   -- test setup: one hit ends it
  L.battleMode = "lose"
  talk(L.npc(T .. "Ione"), { shotBefore = "ione" })
  L.battleMode = nil
  local last = L.battles[#L.battles]
  L.check(last and last.outcome == S.B_OUTCOME_LOST, "lost to Ione")
  L.waitUntil(function() return L.idle() end, 3000, "control after the loss")
  shot("after_losing_to_ione")
  log(string.format("note after losing to Ione: map %d at (%d,%d)", L.mapId(), L.pos()))
  L.check(L.mapId() == S.MAP_ASCLEPEION, "losing to Ione wakes the player in the Asclepeion")
  L.useWarp(S.MAP_AKTI)
  L.useWarp(S.MAP_TEMPLE)
  L.check(L.getFlag(S.FLAG_TRIAL_DONE) and L.getVar(S.VAR_HEARTH_TRIAL) == 6, "the trial stays done")
  talk(L.npc(T .. "Ione"), { shotBefore = "ione_rematch" })
  L.check(L.getFlag(S.FLAG_BADGE01_GET), "the rematch wins the Hearth Laurel")
end)

check("lose_to_petros", function()
  load("05_kronion_hill")
  L.leaveEdge("right", S.MAP_KRONION)
  emu:write16(L.partyMon(0) + S.OFF_MON_HP, 1)   -- test setup: one hit ends it
  L.battleMode = "lose"
  local summit = L.triggers(KH .. "SummitScene")
  L.check(not L.goTrigger(summit), "the summit scene starts")
  settle({ answers = { "no" } })
  L.battleMode = nil
  local last = L.battles[#L.battles]
  L.check(last and last.outcome == S.B_OUTCOME_LOST, "lost to Petros")
  shot("after_losing_to_petros")
  L.check(L.mapId() == S.MAP_HOUSE_1F, "losing to Petros wakes the player at home")
  L.check(not L.getFlag(S.FLAG_RUINS_CLEARED), "the hill is not cleared yet")
  -- back up the road to the hill: the scene plays again and can be won
  L.useWarp(S.MAP_ELAIA)
  L.leaveEdge("up", S.MAP_ROUTE1)
  L.leaveEdge("right", S.MAP_KRONION)
  L.check(not L.goTrigger(L.triggers(KH .. "SummitScene")), "the summit scene starts again")
  settle({ answers = { "yes" }, every = true })
  L.check(L.getFlag(S.FLAG_RUINS_CLEARED) and L.getFlag(S.FLAG_DEXNAV_GET), "the scene finishes on the second try")
  shot("summit_second_try")
end)

-- 6. Every start-menu screen, for the look review ---------------------------------------------------------
local ACTION = { POKEDEX = 0, POKEMON = 1, BAG = 2, PLAYER = 4, SAVE = 5, OPTION = 6, EXIT = 7, DEXNAV = 14 }
local function openMenu(action, label)
  L.waitUntil(L.idle, 600, "the field")
  wait(10)
  tap(K.START); wait(30)
  local n = emu:read8(S.sNumStartMenuActions)
  local target
  for i = 0, n - 1 do if emu:read8(S.sCurrentStartMenuActions + i) == action then target = i end end
  if not target then L.check(false, "the start menu has " .. label); tap(K.B); return false end
  local cur = emu:read8(S.sStartMenuCursorPos)
  for _ = 1, (target - cur) % n do tap(K.DOWN); wait(4) end
  wait(10)
  shot("start_menu_" .. label)
  tap(K.A); wait(120)
  return true
end
local function closeAll()
  for _ = 1, 12 do
    if L.idle() then return end
    tap(K.B); wait(40)
  end
  settle()
end

check("menus", function()
  load("08_after")
  if openMenu(ACTION.POKEDEX, "pokedex") then
    -- the codex, an entry, and its AREA page (the region map)
    shot("pokedex"); tap(K.A); wait(150); shot("pokedex_entry")
    -- AREA is highlighted: the entry takes input once its cry has played
    for _ = 1, 4 do tap(K.A, 6); wait(90) end
    wait(60); shot("pokedex_area")
    closeAll()
  end
  if openMenu(ACTION.POKEMON, "party") then
    shot("party"); tap(K.A); wait(30); shot("party_actions")
    tap(K.A); wait(120)                    -- SUMMARY (the first action)
    for p = 1, 5 do shot(string.format("summary_%d", p)); tap(K.RIGHT); wait(40) end
    closeAll()
  end
  if openMenu(ACTION.BAG, "bag") then
    for p = 1, 5 do shot(string.format("bag_pocket_%d", p)); tap(K.RIGHT); wait(40) end
    closeAll()
  end
  if openMenu(ACTION.DEXNAV, "augury") then shot("augury"); wait(60); shot("augury_2"); closeAll() end
  if openMenu(ACTION.PLAYER, "trainer_card") then
    shot("trainer_card"); tap(K.A); wait(60); shot("trainer_card_back"); closeAll()
  end
  if openMenu(ACTION.OPTION, "option") then shot("option"); closeAll() end
  L.check(L.idle(), "every menu closes back to the field")
end)

L.start(function()
  local only = {}
  for n in (os.getenv("CHECKS_ONLY") or ""):gmatch("[^,]+") do only[n] = true end
  local failed = 0
  for _, c in ipairs(CHECKS) do
    if next(only) == nil or only[c.name] then
      L.setBeat(c.name, false)
      local bugs0 = L.bugs
      local ok, err = pcall(c.fn)
      if not ok then
        failed = failed + 1
        log("FAIL " .. c.name .. ": " .. tostring(err):gsub("^CHECK FAIL: ", ""))
      elseif L.bugs > bugs0 then
        log(string.format("RESULT %s: %d finding(s)", c.name, L.bugs - bugs0))
      else
        log("RESULT " .. c.name .. ": clean")
      end
      L.battleMode = nil
    end
  end
  log(string.format("SUMMARY %d check(s) could not finish, %d finding(s)", failed, L.bugs))
end)
