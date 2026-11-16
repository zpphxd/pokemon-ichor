-- The slice playthrough, run by tools/ichor/tests/slice_playthrough.sh (read it first).
--
-- One continuous run from a fresh cartridge through the slice and into Phase 2, with key
-- presses only: the title, the OPTION menu, NEW GAME, Daphne's speech and the
-- naming screen, then every beat of design/phase1/SCRIPT.md in order. Walking
-- uses slice_lib.lua's breadth-first search over the live map grid. Every
-- trainer is fought, every gift and item in the slice is collected, and the game
-- is saved in the Asclepeion, reset and continued from the save.
--
-- Unless SLICE_NATURAL=1, right after the starter screen the starter's experience is set
-- to level 100's (and the game recalculates its stats). That is battle strength
-- only: its moves, met level and species are untouched, it never levels or
-- evolves, and every battle is still fought with button presses (the first
-- move for trainers, RUN for wild Pokémon, or the first move once a trapping one
-- won't let it flee). Nothing else is written to memory
-- except reading state; options are set in the OPTION menu by hand. Natural
-- mode rejects emulator memory writes, RAM scripts, assists and state resumes.
-- The button-only natural pilot is a progression probe, not a balance verdict.
--
-- Env: SLICE_OUT (default build/slice/), SLICE_SYMBOLS (default <out>symbols.lua),
-- SLICE_STARTER 0 Nebrel / 1 Kynder / 2 Hipling (default 0),
-- SLICE_GENDER theo / ianthe (default theo), SLICE_FROM <beat> (resume from that
-- beat's save state), SLICE_WORKAROUNDS=1 (release a stuck waitmovement, logged
-- as a BUG, so the rest of the slice can still be checked),
-- SLICE_DIFFICULTY mortal / hero / spartan (default hero),
-- SLICE_STOP_AFTER <beat> (explicitly partial coverage, never a full-run PASS).
--
-- Prints "SLICE ok ..." per check, "SLICE BEAT ..." per beat (with a save state
-- in <out>states/), "SLICE shot ..." per screenshot and "SLICE TEXT ..." per
-- message. A check that doesn't block play logs "SLICE BUG ..." and the run
-- carries on; a blocking one stops it. Ends with "SLICE PASS" only if nothing
-- failed, then "SLICE done"; any failure prints "SLICE FAIL: ..." first.

local OUT = os.getenv("SLICE_OUT") or "build/slice/"
local NATURAL = os.getenv("SLICE_NATURAL") == "1"
local L = dofile("tools/ichor/tests/slice_lib.lua")
L.init{ tag = "SLICE", out = OUT, symbols = os.getenv("SLICE_SYMBOLS") or (OUT .. "symbols.lua"), readOnly = NATURAL }
L.statesDir = OUT .. "states/"
local S, K = L.S, L.K
local emu = L.emu
local log, expect, note, wait, now, tap, shot = L.log, L.expect, L.note, L.wait, L.now, L.tap, L.shot
local getFlag, mapId, pos, settle, talk, go = L.getFlag, L.mapId, L.pos, L.settle, L.talk, L.go

local STARTER = tonumber(os.getenv("SLICE_STARTER") or "0")
local IANTHE = (os.getenv("SLICE_GENDER") or "theo") == "ianthe"
local SPECIES = { [0] = "Nebrel", [1] = "Kynder", [2] = "Hipling" }
local DIFFICULTY = os.getenv("SLICE_DIFFICULTY") or "hero"
local DIFFICULTIES = { mortal = 0, hero = 1, spartan = 2 }
local STEP_GLASS_LIMITS = { mortal = 150, hero = 120, spartan = 100 }
local KLEON_TAKES = { [0] = 1, [1] = 2, [2] = 0 }   -- SCRIPT.md beat 3
local KLEON_TRAINER = { [0] = "KLEON_KYNDER", [1] = "KLEON_HIPLING", [2] = "KLEON_NEBREL" }
if NATURAL then L.pilot = dofile("tools/ichor/tests/slice_pilot.lua")(L, STARTER) end

-- --- Checks shared by every beat -----------------------------------------------------------

local function mapIs(map, what)
  expect(mapId() == map, what or ("on map " .. map))
end
-- The song really playing (the BGM player's header), not just the map's choice.
local function musicIs(song, what)
  local t0 = now()
  while not L.playing(song) do
    if now() - t0 > 240 then
      L.check(false, string.format("%s: playing %s, want %s", what, L.song(), L.songName(L.songHeader(song))))
      return
    end
    L.frame()
  end
  log(string.format("ok %s plays (%s)", what, L.song()))
end
local function flagsSet(list, what)
  local missing = {}
  for _, f in ipairs(list) do
    if not getFlag(S[f]) then missing[#missing + 1] = f end
  end
  L.check(#missing == 0, what .. (#missing > 0 and (": not set: " .. table.concat(missing, ", ")) or ""))
end
local function flagsClear(list, what)
  local set = {}
  for _, f in ipairs(list) do
    if getFlag(S[f]) then set[#set + 1] = f end
  end
  L.check(#set == 0, what .. (#set > 0 and (": set: " .. table.concat(set, ", ")) or ""))
end
local function battleCheck(rec, who, song, what)
  expect(rec and rec.trainer and rec.outcome == S.B_OUTCOME_WON, "won " .. what)
  if who then expect(rec.who == who, what .. " was " .. who .. " (got " .. tostring(rec.who) .. ")") end
  if song then
    local want = L.songHeader(song)
    L.check(rec.song == want, string.format("%s battle music is %s (want %s)", what, L.songName(rec.song),
                                            L.songName(want)))
  end
end

-- An item ball, a hidden item or a gift: it lands in the bag, and its flag is
-- set so it can't be had twice.
-- `where` is a function returning the target (L.npc, L.ball, L.sign, L.hidden),
-- looked up on the live map each time, so the test follows the map as built.
local function collect(where, flag, item, what, opts)
  local before = L.itemCount(S[item])
  if getFlag(S[flag]) then L.fail(what .. ": " .. flag .. " already set before collecting") end
  local target = where()
  talk(target, opts)
  local after = L.itemCount(S[item])
  L.check(after > before, string.format("%s: %s in the bag (%d -> %d)", what, item, before, after))
  L.check(getFlag(S[flag]), what .. ": " .. flag .. " set (so it can't be taken twice)")
  -- and asking again gives nothing more (an item ball is gone: try its tile)
  talk(target, { answers = opts and opts.answers })
  local again = L.itemCount(S[item])
  L.check(again == after, string.format("%s: a second try gives nothing (%d -> %d)", what, after, again))
end
local function npc(script, nth) return function() return L.npc(script, nth) end end
local function ball(flag) return function() return L.ball(S[flag]) end end
local function hidden(flag) return function() return L.hidden(S[flag]) end end
local function sign(script) return function() return L.sign(script) end end

-- Trainer battles so far. A wild one can start on the step back to a trainer who
-- stands by tall grass, so "doesn't battle again" counts only trainer battles.
local function trainerBattles()
  local n = 0
  for _, b in ipairs(L.battles) do if b.trainer then n = n + 1 end end
  return n
end

-- A trainer: talk to them (walking there may get the player spotted first, and
-- the battle is played out on the way), then talk again for the after-battle line
-- and make sure it isn't a second battle.
local function trainer(name, script, song, opts)
  if L.pilot then L.pilot.recover() end
  local id = S["TRAINER_" .. name]
  -- (they may already have spotted the player on the way to something else)
  if not L.defeated(id) then talk(L.npc(script), opts) end
  expect(L.defeated(id), name .. " is beaten")
  local rec
  for _, b in ipairs(L.battles) do if b.who == name then rec = b end end
  battleCheck(rec, name, song, name)
  local n1 = trainerBattles()
  talk(L.npc(script), { shotBefore = string.lower(name) .. "_after" })
  L.check(trainerBattles() == n1, name .. " does not battle again")
end

-- Visit a list of things in the order the map makes shortest: always the nearest
-- one the player can reach. Returns the ones that can't be reached yet.
-- Each item: { target = function() ... end, run = function() ... end, name = "..." }
local function visitAll(list, avoid)
  local left = {}
  for _, it in ipairs(list) do left[#left + 1] = it end
  local deferred = {}
  while #left > 0 do
    if L.pilot then L.pilot.recover() end
    local i = L.nearest(left, avoid)
    if not i then break end
    local it = table.remove(left, i)
    log("note visiting " .. it.name)
    -- someone who only appears up close (a flock, a wanderer) can close the way
    -- on arrival: put it back for later rather than fail
    local ok, err = pcall(it.run)
    if not ok then
      if tostring(err):find("no path from", 1, true) then
        log("note the way to " .. it.name .. " closed on arrival")
        deferred[#deferred + 1] = it
      else
        error(err, 0)
      end
    end
  end
  for _, it in ipairs(deferred) do left[#left + 1] = it end
  for _, it in ipairs(left) do log("note can't reach " .. it.name .. " yet") end
  return left
end
local function visit(name, where, run) return { name = name, target = where, run = run } end
local function visitTrainer(name, script)
  return visit(name, npc(script), function() trainer(name, script, S.MUS_BATTLE_TRAINER) end)
end
local function visitItem(name, where, flag, item, opts)
  return visit(name, where, function() collect(where, flag, item, name, opts) end)
end
local function visitTalk(name, where, opts)
  return visit(name, where, function() talk(where(), opts or { shotBefore = name }) end)
end

-- --- Boot, options, new game -------------------------------------------------------------------

local function boot()
  L.setBeat("00_title", false)
  L.waitUntil(function() return now() >= 500 end, 600, "frame 500")
  tap(K.START)
  L.waitUntil(function() return now() >= 1000 end, 600, "frame 1000")
  shot("title")
  tap(K.A)
  L.waitUntil(function() return L.on("CB2_MainMenu") end, 600, "the main menu")
  wait(60)
  shot("main_menu_fresh")

  -- OPTION, by hand: fast text, battle scene off, the Set battle style.
  tap(K.DOWN); wait(10); tap(K.A)
  L.waitUntil(function() return L.taskRunning("Task_OptionMenuProcessInput") end, 600, "the OPTION menu")
  wait(20)
  shot("options_before")
  local function opt() return emu:read16(L.sb2() + S.OFF_SB2_OPTIONS) end
  tap(K.RIGHT); wait(6)                  -- TEXT SPEED: MID -> FAST
  tap(K.DOWN); wait(6); tap(K.RIGHT); wait(6)   -- BATTLE SCENE: ON -> OFF
  tap(K.DOWN); wait(6); tap(K.RIGHT); wait(6)   -- BATTLE STYLE: SHIFT -> SET
  wait(10)
  shot("options_after")
  tap(K.B)
  L.waitUntil(function() return L.on("CB2_MainMenu") end, 600, "the main menu after OPTION")
  wait(40)
  local o = opt()
  expect(o & 7 == 2, string.format("text speed is FAST (options %04x)", o))
  expect((o >> 10) & 1 == 1 and (o >> 9) & 1 == 1, string.format("battle scene OFF, style SET (options %04x)", o))
  -- back up to NEW GAME (the menu comes back with OPTION highlighted, once it has faded in)
  for _ = 1, 5 do
    wait(60); tap(K.UP); wait(20); tap(K.A); wait(60)
    if not L.taskRunning("Task_OptionMenuProcessInput") then break end
    tap(K.B)
    L.waitUntil(function() return L.on("CB2_MainMenu") end, 600, "the main menu again")
  end

  -- Daphne's speech: A through it, the gender menu, the naming screen.
  L.setBeat("00_daphne_speech", false)
  local t0, presses, genderShot = now(), 0, false
  while not (L.inOverworld() and L.idle()) do
    if L.on("CB2_NamingScreen") then
      L.acceptName("speech_naming")
    elseif L.taskRunning("Task_NewGameBirchSpeech_ChooseGender") and not genderShot then
      wait(20); shot("speech_gender"); genderShot = true
      if IANTHE then tap(K.DOWN); wait(10) end
      tap(K.A); wait(30)
    else
      presses = presses + 1
      if presses % 3 == 0 then shot(string.format("speech_%02d", presses)) end
      tap(K.A); wait(30)
    end
    if now() - t0 > 30000 then L.fail("Daphne's speech never ended") end
  end
  wait(30)
end

-- --- The beats, in play order ---------------------------------------------------------------------
-- Each beat starts with a save state (<out>states/<name>.ss). SLICE_FROM=<name>
-- loads that state and plays on from there: handy while fixing one beat, but the
-- director's run always starts from the title.
--
-- Nothing below names a coordinate but the Herald's Run's route (beat 15), the
-- builder's solving route through the one-way turnstiles. People, signs, items,
-- triggers and warps are found on the live map by the script they run or the
-- flag they set (slice_lib's L.npc, L.sign, L.ball, L.hidden, L.triggers,
-- L.useWarp, L.leaveEdge), so moving them on a map never breaks the run; taking
-- one away fails with its name.

local BEATS = {}
local function beat(name, fn) BEATS[#BEATS + 1] = { name = name, fn = fn } end
local E, R1, KH, AK = "ElaiaVillage_EventScript_", "KallisteRoute1_EventScript_",
                      "KallisteRoute1_KronionHill_EventScript_", "AktiTown_EventScript_"

-- Beat 1: the player's house -----------------------------------------------------------------------

beat("01_bedroom", function()
  mapIs(S.MAP_HOUSE_2F, "woke on 2F")
  log(string.format("note woke at (%d,%d)", pos()))
  local name = {}
  for i = 0, 6 do name[#name + 1] = emu:read8(L.sb2() + S.OFF_SB2_NAME + i) end
  local want = IANTHE and { 0xC3, 0xBB, 0xC8, 0xCE, 0xC2, 0xBF, 0xFF } or { 0xCE, 0xC2, 0xBF, 0xC9, 0xFF }
  local same = true
  for i, b in ipairs(want) do if name[i] ~= b then same = false end end
  expect(same and emu:read8(L.sb2() + S.OFF_SB2_GENDER) == (IANTHE and 1 or 0),
         IANTHE and "the player is Ianthe, named IANTHE" or "the player is Theo, named THEO")
  musicIs(S.MUS_ELAIA, "Elaia's theme in the bedroom")
  shot("bedroom")
  -- the stair gate, the room's things, then the water clock
  local gate = L.triggers("ElaiaVillage_PlayersHouse_2F_EventScript_StairGate")
  expect(not L.goTrigger(gate), "the stair gate stops the player")
  wait(30); shot("mom_calls_upstairs"); settle()
  expect(not L.onTile(gate), "stepped back from the stairs")
  talk(L.sign("ElaiaVillage_PlayersHouse_2F_EventScript_Knucklebones"), { shotBefore = "knucklebones" })
  talk(L.sign("ElaiaVillage_PlayersHouse_2F_EventScript_Scrolls"), { shotBefore = "scrolls" })
  talk(L.sign("ElaiaVillage_PlayersHouse_2F_EventScript_WaterClock"),
       { shotBefore = "water_clock", shots = { [1] = "klepsydra_text" },
         answers = { ({ mortal = "up", hero = "yes", spartan = "down" })[DIFFICULTY] } })
  expect(getFlag(S.FLAG_SET_WATER_CLOCK), "the water clock is set")
  expect(getFlag(S.FLAG_DIFFICULTY_CHOSEN) and L.getVar(S.VAR_DIFFICULTY) == DIFFICULTIES[DIFFICULTY],
         "the actual water-clock menu saved " .. DIFFICULTY)
  expect(not getFlag(S.FLAG_OATH_CHOICE_PENDING), "the separate Oath choice is resolved")
  local ichor = emu:read32(S.gSaveBlock3Ptr) + S.OFF_SB3_ICHOR
  expect(emu:read8(ichor + S.OFF_ICHOR_OATH_STATE) == S.OATH_DECLINED,
         "the ordinary playthrough did not swear the Oath")
  L.useWarp(S.MAP_HOUSE_1F, true)
end)

beat("01_mom", function()
  shot("mom_comes_over")
  settle({ shots = { [3] = "mom_klotheia", [7] = "talaria", [13] = "mom_oracle" } })
  flagsSet({ "FLAG_TALKED_TO_MOM", "FLAG_SYS_B_DASH", "FLAG_RECEIVED_RUNNING_SHOES" }, "Mom gave the Talaria")
  shot("downstairs")
  talk(L.sign("ElaiaVillage_PlayersHouse_1F_EventScript_Hearth"), { shotBefore = "hearth" })
  L.useWarp(S.MAP_ELAIA)
  mapIs(S.MAP_ELAIA, "out of the front door into Elaia")
  musicIs(S.MUS_ELAIA, "Elaia's theme in the village")
  shot("front_door")
end)

beat("01_kydippe", function()
  L.useWarp(S.MAP_KYDIPPE)
  collect(npc("ElaiaVillage_NeighborsHouse_EventScript_Kydippe"), "FLAG_GOT_KYDIPPE_ORAN", "ITEM_ORAN_BERRY",
          "Kydippe's Oran Berries", { shotBefore = "kydippe", shots = { [2] = "kydippe_delivered_you" } })
  talk(L.npc("ElaiaVillage_NeighborsHouse_EventScript_Kydippe"), { shotBefore = "kydippe_after" })
  L.useWarp(S.MAP_ELAIA)
end)

-- Beat 2: the gates, then Halia --------------------------------------------------------------------

beat("02_gates", function()
  local ring = L.triggers(E .. "HaliaCalls")
  local note = L.triggers(E .. "AkademiaNote")
  expect(not L.goTrigger(note, { avoid = ring }), "the note on the Akademia door")
  wait(40); shot("akademia_note"); settle()
  expect(not getFlag(S.FLAG_THREAD_READ), "the thread is still unread")
  expect(mapId() == S.MAP_ELAIA and not L.onTile(note), "stepped back from the door")
  local gate = L.triggers(E .. "ShepherdGate")
  expect(not L.goTrigger(gate, { avoid = ring }), "the old shepherd stops the player")
  wait(30); shot("shepherd_gate"); settle()
  expect(not L.onTile(gate), "turned back from the road")
end)

beat("02_halia", function()
  expect(not L.goTrigger(L.triggers(E .. "HaliaCalls")), "Halia calls the player into line")
  wait(30); shot("halia_calls")
  settle({ answers = { "no" }, shots = { [3] = "korinna_reading", [8] = "philon_reading", [12] = "your_hand",
                                         [14] = "hm", [15] = "turn_around", [16] = "again",
                                         [17] = "your_own_business", [18] = "liar" } })
  expect(getFlag(S.FLAG_THREAD_READ), "the thread is read")
  shot("after_the_reading")
end)

-- Beat 3: the Akademia -----------------------------------------------------------------------------

beat("03_akademia", function()
  L.useWarp(S.MAP_AKADEMIA, true)
  musicIs(S.MUS_AKADEMIA, "the Akademia's lyre theme")
  shot("akademia_alethea")
  settle({ every = true, answers = { "down", "no" }, hooks = {
    CB2_StarterChoose = function()
      wait(90); shot("starter_screen")
      if STARTER == 0 then tap(K.LEFT) elseif STARTER == 2 then tap(K.RIGHT) end
      wait(30); tap(K.A); wait(60); shot("starter_confirm"); tap(K.A)
      L.waitUntil(L.inOverworld, 1200, "the Akademia after the starter screen")
    end } })
  expect(L.getVar(S.VAR_STARTER_MON) == STARTER, "VAR_STARTER_MON is " .. SPECIES[STARTER])
  flagsSet({ "FLAG_GOT_STARTER", "FLAG_SYS_POKEMON_GET", "FLAG_SYS_POKEDEX_GET", "FLAG_KLEON_TOOK_STARTER" },
           "a partner, the Pokedex, and Kleon took his")
  local hide = { [0] = "FLAG_HIDE_KRATER_NEBREL", [1] = "FLAG_HIDE_KRATER_KYNDER", [2] = "FLAG_HIDE_KRATER_HIPLING" }
  local third = 3 - STARTER - KLEON_TAKES[STARTER]
  flagsSet({ hide[STARTER], hide[KLEON_TAKES[STARTER]] }, "both taken kraters are hidden")
  flagsClear({ hide[third] }, "the last krater stays: " .. SPECIES[third])
  expect(L.partyLevel(0) == 5, "the starter arrives at level 5")

  if NATURAL then
    log(string.format("ok NATURAL: starter species %d remains level 5 (exp %d); memory writes prohibited",
                      L.partySpecies(0), L.partyExperience(0)))
  else
    local species, growth, exp = L.assistLevel100()
    log(string.format("ok ASSIST: starter (species %d, growth %d) set to level 100 (exp %d)", species, growth, exp))
  end
  shot("last_krater")
  L.useWarp(S.MAP_ELAIA)
end)

-- Beat 4: Kleon's battle, Alethea, and the village after ------------------------------------------------

beat("04_kleon", function()
  expect(not getFlag(S.FLAG_HIDE_KLEON_ELAIA), "Kleon waits in the square")
  shot("kleon_waits")
  expect(not L.goTrigger(L.triggers(E .. "KleonTrigger")), "Kleon calls the player at the steps")
  wait(40); shot("kleon_there_you_are")
  local _, fought = settle({ answers = { "no" }, shots = { [4] = "kleon_oracle", [6] = "kleon_battle_me" } })
  expect(#fought == 1, "one battle with Kleon")
  local won = fought[1] and fought[1].outcome == S.B_OUTCOME_WON
  if NATURAL and not won then
    expect(fought[1] and fought[1].trainer and fought[1].outcome == S.B_OUTCOME_LOST,
           "Kleon's supported opening loss returns to the story")
    flagsClear({ "FLAG_WON_KLEON_1" }, "losing does not record a victory")
    L.check(fought[1].song == L.songHeader(S.MUS_BATTLE_RIVAL), "Kleon's loss uses the rival battle music")
  else
    battleCheck(fought[1], KLEON_TRAINER[STARTER], S.MUS_BATTLE_RIVAL, "Kleon")
    flagsSet({ "FLAG_WON_KLEON_1" }, "the actual rival win is recorded")
  end
  flagsSet({ "FLAG_KLEON_BATTLE_1_DONE", "FLAG_GOT_POKEBALLS", "FLAG_HIDE_KLEON_ELAIA",
             "FLAG_HIDE_ALETHEA_ELAIA" }, "beat 4's flags")
  flagsClear({ "FLAG_NO_WHITEOUT" }, "the no-whiteout flag is cleared")
  local hp, maxHp = L.partyHp(0)
  expect(hp == maxHp and hp > 0, "Alethea healed the actual opening battle damage")
  expect(L.itemCount(S.ITEM_POKE_BALL) == 5, "Alethea's five Poke Balls")
  mapIs(S.MAP_ELAIA, "still in Elaia")
  musicIs(S.MUS_ELAIA, "Elaia's theme again")
  shot("square_after")
end)

beat("04_elaia_after", function()
  visitAll({
    visitItem("the Potion by the olive press", ball("FLAG_ITEM_ELAIA_POTION"), "FLAG_ITEM_ELAIA_POTION", "ITEM_POTION"),
    visitItem("the Relic Copper in the well", sign(E .. "Well"), "FLAG_GOT_ELAIA_RELIC_COPPER", "ITEM_RELIC_COPPER",
              { shotBefore = "well" }),
    visitItem("the Honey at Mom's beehives", hidden("FLAG_HIDDEN_ELAIA_HONEY"), "FLAG_HIDDEN_ELAIA_HONEY", "ITEM_HONEY"),
    visitItem("the X Speed past the race start", hidden("FLAG_HIDDEN_ELAIA_X_SPEED"), "FLAG_HIDDEN_ELAIA_X_SPEED",
              "ITEM_X_SPEED"),
    visitTalk("halia_after", npc(E .. "Halia")),
    visitTalk("village_sign", sign(E .. "VillageSign")),
    visitTalk("olive_farmer", npc(E .. "OliveFarmer")),
  })
  -- Glykera's bakery: the comb from Mom's hives buys two honey cakes
  local BK = "ElaiaVillage_BakersHouse_EventScript_"
  L.useWarp(S.MAP_BAKERS_HOUSE)
  expect(L.idle(), "no scene plays in Glykera's house")
  local honey, cakes = L.itemCount(S.ITEM_HONEY), L.itemCount(S.ITEM_OLD_GATEAU)
  talk(L.npc(BK .. "Glykera"), { shotBefore = "glykera" })
  expect(getFlag(S.FLAG_GOT_GLYKERA_CAKES), "Glykera trades the comb for honey cakes (FLAG_ICHOR_GOT_GLYKERA_CAKES)")
  L.check(L.itemCount(S.ITEM_HONEY) == honey - 1, "Glykera takes the Honey")
  L.check(L.itemCount(S.ITEM_OLD_GATEAU) == cakes + 2,
          string.format("two honey cakes in the bag (ITEM_OLD_GATEAU %d -> %d)", cakes, L.itemCount(S.ITEM_OLD_GATEAU)))
  talk(L.npc(BK .. "Glykera"), { shotBefore = "glykera_after" })
  L.check(L.itemCount(S.ITEM_OLD_GATEAU) == cakes + 2, "asking Glykera again gives no more cakes")
  visitAll({
    -- Kimon offers his Halcyling for a Galekit, which the slice's run doesn't catch: say no
    visitTalk("kimon", npc(BK .. "Kimon"), { shotBefore = "kimon", answers = { "no" } }),
    visitTalk("bakery_oven", sign(BK .. "Oven")),
    visitTalk("honey_shelf", sign(BK .. "HoneyShelf")),
    visitTalk("pithos", sign(BK .. "Pithos")),
    visitTalk("model_trireme", sign(BK .. "ModelTrireme")),
    visitTalk("bakery_window", sign(BK .. "Window")),
  })
  L.useWarp(S.MAP_ELAIA)
  -- home: Mom's after-battle line and her offer of a meal
  L.useWarp(S.MAP_HOUSE_1F)
  expect(L.idle(), "no scene replays at home")
  talk(L.npc("ElaiaVillage_PlayersHouse_1F_EventScript_Mom"), { shotBefore = "mom_after", answers = { "yes" } })
  L.useWarp(S.MAP_ELAIA)
end)

-- Beat 5: Route 1 and Kronion Hill -------------------------------------------------------------------
-- Everything on the route is visited nearest-first; what the flock walls off
-- waits for the second pass, after the hill.

local route1Later
beat("05_route1", function()
  shot("north_gate")
  L.leaveEdge("up", S.MAP_ROUTE1)
  musicIs(S.MUS_ROUTE1, "the Route 1 theme")
  shot("route1_south")
  expect(not getFlag(S.FLAG_HIDE_FLOCK), "the flock is on the road")
  route1Later = visitAll({
    visitItem("the carter's Moomoo Milk", npc(R1 .. "Carter"), "FLAG_GOT_MOOMOO_MILK", "ITEM_MOOMOO_MILK",
              { shotBefore = "carter" }),
    visitTalk("wall_youth", npc(R1 .. "WallYouth")),
    visitTalk("herm_south", sign(R1 .. "HermSouth")),
    visitTrainer("TITYROS", R1 .. "Tityros"),
    visitTrainer("THESTYLIS", R1 .. "Thestylis"),
    visitItem("the Route 1 Poke Ball", ball("FLAG_ITEM_ROUTE1_POKE_BALL"), "FLAG_ITEM_ROUTE1_POKE_BALL", "ITEM_POKE_BALL"),
    visitTrainer("PHYLLIS", R1 .. "Phyllis"),
    visitItem("the Miracle Seed", ball("FLAG_ITEM_ROUTE1_MIRACLE_SEED"), "FLAG_ITEM_ROUTE1_MIRACLE_SEED", "ITEM_MIRACLE_SEED"),
    visitItem("the hidden Antidote", hidden("FLAG_HIDDEN_ROUTE1_ANTIDOTE"), "FLAG_HIDDEN_ROUTE1_ANTIDOTE", "ITEM_ANTIDOTE"),
    visitItem("the hidden Repel", hidden("FLAG_HIDDEN_ROUTE1_REPEL"), "FLAG_HIDDEN_ROUTE1_REPEL", "ITEM_REPEL"),
    visitItem("the olive farmer's Sitrus Berry", npc(R1 .. "OliveFarmer"), "FLAG_GOT_ROUTE1_SITRUS", "ITEM_SITRUS_BERRY",
              { shotBefore = "olive_farmer" }),
    visitItem("the Oran Berry under the big olive", hidden("FLAG_HIDDEN_ROUTE1_ORAN"), "FLAG_HIDDEN_ROUTE1_ORAN",
              "ITEM_ORAN_BERRY"),
    visitTrainer("KOMATAS", R1 .. "Komatas"),
    visitItem("the Route 1 Potion", ball("FLAG_ITEM_ROUTE1_POTION"), "FLAG_ITEM_ROUTE1_POTION", "ITEM_POTION"),
    visitTalk("herm_fork", sign(R1 .. "HermFork")),
    visitTrainer("AGIS", R1 .. "Agis"),
    visitTrainer("POLYEIDOS", R1 .. "Polyeidos"),
    visitTalk("amaryllis_before", npc(R1 .. "Amaryllis")),
    visitTalk("flock_goat", npc(R1 .. "FlockGoat")),
    visitTalk("herm_north", sign(R1 .. "HermNorth")),
  })
  -- the flock is still there, so the road north is shut
  for _, it in ipairs(route1Later) do
    if it.name == "flock_goat" or it.name == "amaryllis_before" then
      L.check(false, "the flock (or Amaryllis) can be reached before the hill: " .. it.name)
    end
  end
  log(string.format("note %d thing(s) on Route 1 wait for the flock to move", #route1Later))
end)

beat("05_kronion_hill", function()
  if not route1Later then route1Later = {} end
  L.leaveEdge("right", S.MAP_KRONION)
  shot("hill_foot")
  musicIs(S.MUS_ROUTE1, "Kronion Hill keeps the route's theme")
  expect(not L.goTrigger(L.triggers(KH .. "SummitScene")), "the summit scene starts at the top of the stair")
end)

beat("05_summit", function()
  local _, fought = settle({ every = true, answers = { "no" } })
  expect(#fought == 2, "two grunt battles in the summit scene")
  battleCheck(fought[1], "PETROS", S.MUS_TITAN, "Petros")
  battleCheck(fought[2], "AMATHOS", S.MUS_TITAN, "Amathos")
  flagsSet({ "FLAG_RUINS_CLEARED", "FLAG_FOUND_TABLET", "FLAG_DEXNAV_GET", "FLAG_HIDE_ALETHEA_RUINS",
             "FLAG_HIDE_RUINS_GRUNTS", "FLAG_HIDE_TITAN_TABLET", "FLAG_HIDE_FLOCK" }, "the summit's flags")
  shot("summit_after")
  visitAll({
    visitItem("the grunts' Escape Rope", ball("FLAG_ITEM_KRONION_ESCAPE_ROPE"), "FLAG_ITEM_KRONION_ESCAPE_ROPE",
              "ITEM_ESCAPE_ROPE"),
    visitItem("the Hard Stone", hidden("FLAG_HIDDEN_KRONION_HARD_STONE"), "FLAG_HIDDEN_KRONION_HARD_STONE", "ITEM_HARD_STONE"),
    visitItem("the Stardust", hidden("FLAG_HIDDEN_KRONION_STARDUST"), "FLAG_HIDDEN_KRONION_STARDUST", "ITEM_STARDUST"),
    visitTalk("stele", sign(KH .. "Stele")),
    visitTalk("altar", sign(KH .. "Altar")),
    visitTalk("pit_after", sign(KH .. "Pit"), { shotBefore = "pit_after", every = true }),
    -- the high pastures, down the goat path past the herm
    visitTalk("herm_fork_kronion", sign(KH .. "HermFork")),
    visitTrainer("MENALKAS", KH .. "Menalkas"),
    visitTalk("fold_kid", npc(KH .. "FoldKid")),
    visitTrainer("THYRSIS", KH .. "Thyrsis"),
    visitTalk("pan_shrine", sign(KH .. "PanShrine")),
    visitItem("the Burn Heal on the olive terraces", ball("FLAG_ITEM_KRONION_BURN_HEAL"), "FLAG_ITEM_KRONION_BURN_HEAL",
              "ITEM_BURN_HEAL"),
    visitTrainer("LYKIDAS", KH .. "Lykidas"),
    visitItem("the Everstone on the lookout shelf", ball("FLAG_ITEM_KRONION_EVERSTONE"), "FLAG_ITEM_KRONION_EVERSTONE",
              "ITEM_EVERSTONE"),
    visitItem("the Pretty Feather on the point", hidden("FLAG_HIDDEN_KRONION_FEATHER"), "FLAG_HIDDEN_KRONION_FEATHER",
              "ITEM_PRETTY_FEATHER"),
  })
end)

beat("05_road_open", function()
  if not route1Later then L.fail("resume at 05_route1 or earlier: the second Route 1 pass needs the first") end
  L.leaveEdge("left", S.MAP_ROUTE1)
  shot("flock_gone")
  -- the second pass: whatever the flock walled off, then Amaryllis's after-line
  for i = #route1Later, 1, -1 do
    local n = route1Later[i].name
    if n == "flock_goat" or n == "amaryllis_before" then table.remove(route1Later, i) end
  end
  local left = visitAll(route1Later)
  L.check(#left == 0, string.format("everything on Route 1 can be reached after the hill (%d left)", #left))
  talk(L.npc(R1 .. "Amaryllis"), { shotBefore = "amaryllis_after" })
end)

-- Beat 6: Akti --------------------------------------------------------------------------------------

beat("06_akti_arrival", function()
  L.leaveEdge("up", S.MAP_AKTI, true)
  shot("arrival")
  settle({ every = true })
  flagsSet({ "FLAG_ARRIVED_AKTI", "FLAG_VISITED_AKTI" }, "arrived in Akti")
  musicIs(S.MUS_AKTI, "Akti's theme")
  shot("after_arrival")
  talk(L.npc(AK .. "Diktys"), { shotBefore = "diktys_after" })
  talk(L.sign(AK .. "TownSign"), { shotBefore = "town_sign" })
  collect(hidden("FLAG_HIDDEN_AKTI_SUPER_POTION"), "FLAG_HIDDEN_AKTI_SUPER_POTION", "ITEM_SUPER_POTION",
          "the Super Potion behind Diktys's nets")
  talk(L.npc(AK .. "Pilgrim"), { shotBefore = "pilgrim" })
end)

beat("06_asclepeion", function()
  L.useWarp(S.MAP_ASCLEPEION)
  musicIs(S.MUS_ASCLEPEION, "the Asclepeion's theme")
  shot("asclepeion")
  log(string.format("note party HP before the heal: %d/%d", L.partyHp(0)))
  talk(L.npc("AktiTown_Asclepeion_EventScript_Healer"),
       { shotBefore = "healer", shots = { [1] = "healer_welcome", [3] = "healer_rest" } })
  local hp, maxHp = L.partyHp(0)
  expect(hp == maxHp and hp > 1, string.format("the healer restored the party (%d/%d)", hp, maxHp))
  local hmap, hx, hy = L.lastHeal()
  expect(hmap == S.MAP_AKTI, string.format("the respawn point is Akti (map %d at %d,%d)", hmap, hx, hy))
  visitAll({
    visitTalk("bandaged_fisher", npc("AktiTown_Asclepeion_EventScript_BandagedFisher")),
    visitTalk("old_man", npc("AktiTown_Asclepeion_EventScript_OldMan")),
    visitTalk("statue", sign("AktiTown_Asclepeion_EventScript_Statue")),
    visitTalk("pithos_woman", npc("AktiTown_Asclepeion_EventScript_PithosWoman")),
  })
end)

beat("06_save", function()
  -- START, then down to SAVE (MENU_ACTION_SAVE is 5 in src/start_menu.c's enum)
  tap(K.START); wait(30)
  L.waitUntil(function() return emu:read8(S.sNumStartMenuActions) > 0 end, 120, "the start menu")
  shot("start_menu")
  local n = emu:read8(S.sNumStartMenuActions)
  local target
  for i = 0, n - 1 do if emu:read8(S.sCurrentStartMenuActions + i) == 5 then target = i end end
  expect(target ~= nil, "SAVE is on the start menu")
  local cur = emu:read8(S.sStartMenuCursorPos)
  for _ = 1, (target - cur) % n do tap(K.DOWN); wait(4) end
  wait(10); shot("start_menu_save")
  tap(K.A)
  settle({ shots = { [1] = "save_prompt" } })
  local map, px, py = mapId(), pos()
  local level, hp = L.partyLevel(0), L.partyHp(0)
  log(string.format("ok saved on map %d at (%d,%d)", map, px, py))

  emu:reset()
  -- the boot's own timing: START skips the intro, A leaves the title screen
  wait(500); tap(K.START); wait(500); tap(K.A)
  L.waitUntil(function() return L.on("CB2_MainMenu") end, 900, "the main menu with a save")
  wait(80)
  shot("main_menu_continue")
  tap(K.A)
  L.waitUntil(L.idle, 3000, "the field after CONTINUE")
  wait(30)
  shot("continued")
  local x, y = pos()
  expect(mapId() == map and x == px and y == py, string.format("CONTINUE puts the player back on map %d (%d,%d)", map, x, y))
  expect(L.partyLevel(0) == level and L.partyHp(0) == hp, "the party is as it was saved")
  flagsSet({ "FLAG_ARRIVED_AKTI", "FLAG_RUINS_CLEARED", "FLAG_KLEON_BATTLE_1_DONE" }, "story flags survive the reload")
  musicIs(S.MUS_ASCLEPEION, "the Asclepeion's theme after the reload")
  L.useWarp(S.MAP_AKTI)
end)

beat("06_agora", function()
  L.useWarp(S.MAP_AGORA)
  shot("agora")
  musicIs(S.MUS_AGORA, "the Agora's theme")
  -- The shop's BUY/SELL/QUIT menu and its item list are not script prompts, so
  -- this one is played by hand.
  talk(L.npc("AktiTown_Agora_EventScript_Demeas"), { shotBefore = "demeas", noSettle = true })
  wait(40); shot("demeas_welcome")
  local t0 = now()
  while not L.taskRunning("Task_ShopMenu") do
    tap(K.A); wait(30)
    if now() - t0 > 900 then L.fail("Demeas's shop menu never opened") end
  end
  wait(20); shot("agora_menu"); tap(K.A)                              -- BUY
  L.waitUntil(function() return L.taskRunning("Task_BuyMenu") end, 600, "the Agora's item list")
  wait(40); shot("agora_shop")
  if L.pilot then L.pilot.buyBalls() end
  tap(K.B)
  L.waitUntil(function() return L.taskRunning("Task_ShopMenu") end, 600, "the shop menu again")
  wait(20); shot("agora_menu_again"); tap(K.B)                        -- QUIT
  wait(40); shot("demeas_bye")
  settle()
  visitAll({
    visitTalk("customer_man", npc("AktiTown_Agora_EventScript_CustomerMan")),
    visitTalk("customer_girl", npc("AktiTown_Agora_EventScript_CustomerGirl")),
  })
  L.useWarp(S.MAP_AKTI)
end)

beat("06_fishers_house", function()
  L.useWarp(S.MAP_FISHERS)
  shot("fishers_house")
  collect(npc("AktiTown_FishersHouse_EventScript_Glaukos"), "FLAG_GOT_OLD_ROD", "ITEM_OLD_ROD", "Glaukos's Old Rod",
          { shotBefore = "glaukos", answers = { "no" }, every = true })
  talk(L.npc("AktiTown_FishersHouse_EventScript_Grandson"), { shotBefore = "grandson" })
  L.useWarp(S.MAP_AKTI)
end)

beat("06_harbor_before", function()
  -- The quay's west end (and the Potion among its crates) is reached only past
  -- the tile Kleon stands on until the ending; it is collected in 08_after.
  L.finding(L.distanceTo(L.ball(S.FLAG_ITEM_AKTI_POTION)) ~= nil,
            "the Potion among the quay crates can be reached before the ending (QA.md m1)")
  visitAll({
    visitTalk("kleon_before", npc(AK .. "Kleon"), { shotBefore = "kleon_before", shots = { [2] = "kleon_soup" } }),
    visitTalk("nausikles_before", npc(AK .. "Nausikles")),
    visitTalk("rower", npc(AK .. "Rower")),
    visitItem("the Paralyze Heal by the fish stall", ball("FLAG_ITEM_AKTI_PARALYZE_HEAL"), "FLAG_ITEM_AKTI_PARALYZE_HEAL",
              "ITEM_PARALYZE_HEAL"),
    visitTalk("fishwife", npc(AK .. "Fishwife")),
    visitTalk("pier_kid", npc(AK .. "Kid")),
    visitTalk("islet_fisher", npc(AK .. "IsletFisher")),
    visitItem("Hydna's Mystic Water", npc(AK .. "Hydna"), "FLAG_GOT_MYSTIC_WATER", "ITEM_MYSTIC_WATER",
              { shotBefore = "hydna" }),
    visitItem("the Heart Scale on the beach", hidden("FLAG_HIDDEN_AKTI_HEART_SCALE"), "FLAG_HIDDEN_AKTI_HEART_SCALE",
              "ITEM_HEART_SCALE"),
    visitItem("the Pearl on the tide rocks", hidden("FLAG_HIDDEN_AKTI_PEARL"), "FLAG_HIDDEN_AKTI_PEARL", "ITEM_PEARL"),
    visitTalk("grotto_rubble", sign(AK .. "GrottoRubble")),
    visitTalk("goat", npc(AK .. "Goat")),
    visitTalk("quay_sign", sign(AK .. "QuaySign")),
    visitTalk("temple_old_woman", npc(AK .. "OldWoman")),
  })
end)

-- Akti's two newest homes (MAP_DESIGN.md §2): Kapra the loose goat and Aigon's
-- Soothe Bell; Doris's grotto lore (her trade waits for the laurel, in 08_after)
beat("06_homes", function()
  talk(L.npc(AK .. "LooseGoat"), { shotBefore = "kapra" })
  flagsSet({ "FLAG_AKTI_GOAT_HOME" }, "Kapra went home")
  L.useWarp(S.MAP_GOATHERDS)
  shot("goatherds_house")
  collect(npc("AktiTown_GoatherdsHouse_EventScript_Aigon"), "FLAG_GOT_SOOTHE_BELL", "ITEM_SOOTHE_BELL",
          "Aigon's Soothe Bell", { shotBefore = "aigon" })
  talk(L.sign("AktiTown_GoatherdsHouse_EventScript_Hearth"), { shotBefore = "goatherds_hearth" })
  L.useWarp(S.MAP_AKTI)
  L.useWarp(S.MAP_DIVERS)
  shot("divers_house")
  talk(L.npc("AktiTown_DiversHouse_EventScript_Doris"), { shotBefore = "doris" })
  talk(L.sign("AktiTown_DiversHouse_EventScript_WaterClock"), { shotBefore = "water_clock" })
  L.useWarp(S.MAP_AKTI)
end)

-- Beat 7: the Temple of Hestia ----------------------------------------------------------------------

local T = "AktiTown_TempleOfHestia_EventScript_"
beat("07_temple", function()
  if L.pilot then L.pilot.trainKallisteTeam() end
  L.useWarp(S.MAP_TEMPLE)
  musicIs(S.MUS_TEMPLE, "the Temple's theme")
  shot("temple_entry")
  expect(L.getVar(S.VAR_HEARTH_TRIAL) == 0, "no flame on arrival")
  talk(L.npc(T .. "Euboulos"), { shotBefore = "euboulos" })
  talk(L.sign(T .. "Stele"), { shotBefore = "hymn", every = true })
  -- to the hearth out of Lampon's sight: he won't let go of it yet
  talk(L.sign(T .. "GreatHearth"), { shotBefore = "hands_off", avoid = L.sight(T .. "Lampon") })
  expect(L.getVar(S.VAR_HEARTH_TRIAL) == 0, "no flame before Lampon is beaten")
  trainer("LAMPON", T .. "Lampon", S.MUS_BATTLE_TRAINER)
end)

beat("07_hearth_trial", function()
  local function light(script, want, what)
    talk(L.sign(script), { shotBefore = what })
    expect(L.getVar(S.VAR_HEARTH_TRIAL) == want, string.format("%s (trial %d)", what, L.getVar(S.VAR_HEARTH_TRIAL)))
    shot(what .. "_done")
  end
  -- the order of the hymn: Door, Table, Loom, Bed
  light(T .. "GreatHearth", 1, "take_flame")
  light(T .. "BrazierDoor", 2, "door_brazier")
  light(T .. "BrazierTable", 3, "table_brazier")
  light(T .. "BrazierLoom", 4, "loom_brazier")
  light(T .. "BrazierBed", 5, "bed_brazier")
  talk(L.sign(T .. "GreatHearth"), { shotBefore = "return_flame", every = true })
  flagsSet({ "FLAG_TRIAL_DONE", "FLAG_GOT_CHARCOAL" }, "the trial is done and the Charcoal found")
  expect(L.getVar(S.VAR_HEARTH_TRIAL) == 6 and L.itemCount(S.ITEM_CHARCOAL) == 1, "trial var 6, one Charcoal")
  trainer("PYRRHA", T .. "Pyrrha", S.MUS_BATTLE_TRAINER)
  trainer("AITHRA", T .. "Aithra", S.MUS_BATTLE_TRAINER)
end)

beat("07_ione", function()
  if L.pilot then L.pilot.prepareBoss() end
  local n0 = #L.battles
  talk(L.npc(T .. "Ione"), { shotBefore = "ione", every = true })
  local rec
  for i = n0 + 1, #L.battles do if L.battles[i].who == "IONE" then rec = L.battles[i] end end
  battleCheck(rec, "IONE", S.MUS_BATTLE_RIVAL, "Ione")
  flagsSet({ "FLAG_BADGE01_GET", "FLAG_GOT_TM_FACADE" }, "the Hearth Laurel and TM42")
  expect(L.itemCount(S.ITEM_TM42) == 1, "TM42 Facade in the bag")
  local n1 = #L.battles
  talk(L.npc(T .. "Ione"), { shotBefore = "ione_after" })
  expect(#L.battles == n1, "Ione does not battle again")
  talk(L.npc(T .. "Kanthos"), { shotBefore = "kanthos" })
  talk(L.npc(T .. "Euboulos"), { shotBefore = "euboulos_after" })
end)

-- Beat 8: the harbor ---------------------------------------------------------------------------------

beat("08_harbor_part1", function()
  L.useWarp(S.MAP_AKTI, true)
  shot("doorstep")
  settle({ every = true })
  flagsClear({ "FLAG_HIDE_ALETHEA_AKTI" },
             "after part 1, Alethea's hide flag is clear (else leaving and re-entering Akti replays part 1)")
end)

beat("08_harbor_part2", function()
  local quay = L.triggers(AK .. "HarborPart2Row9", AK .. "HarborPart2Row10", AK .. "HarborPart2Row11")
  expect(not L.goTrigger(quay), "the quay starts the ending")
  settle({ every = true, answers = { "no" } })
  flagsSet({ "FLAG_SLICE_COMPLETE", "FLAG_HIDE_KLEON_AKTI" }, "the slice is complete")
  -- Phase 2: no farewell card; Alethea stays on the quay with Halia's message
  flagsClear({ "FLAG_HIDE_ALETHEA_AKTI" }, "Alethea waits on the quay after the slice")
  shot("the_end")
end)

beat("08_after", function()
  expect(L.itemCount(S.ITEM_CHARCOAL) == 1, "the actual Hearth Trial coal is in the Bag for the mainland")
  talk(L.npc(AK .. "Nausikles"), { shotBefore = "nausikles_after" })
  collect(ball("FLAG_ITEM_AKTI_POTION"), "FLAG_ITEM_AKTI_POTION", "ITEM_POTION", "the Potion among the quay crates")
  -- with the laurel, Doris trades her shell bell for the beach's Heart Scale
  L.useWarp(S.MAP_DIVERS)
  collect(npc("AktiTown_DiversHouse_EventScript_Doris"), "FLAG_GOT_SHELL_BELL", "ITEM_SHELL_BELL",
          "Doris's shell bell, for the Heart Scale", { answers = { "yes" }, shotBefore = "doris_trade" })
  L.useWarp(S.MAP_AKTI)
  -- re-entering Akti after the end replays nothing
  L.useWarp(S.MAP_ASCLEPEION)
  L.useWarp(S.MAP_AKTI)
  wait(60)
  expect(L.idle(), "Akti after the end is quiet")
  shot("akti_after_the_end")
end)

-- === Phase 2, Act I on the mainland (design/phase2/SCRIPT.md) ===================================

-- Beat 9A: back down Route 1 to Elaia, where Halia looks at your hand once more.
beat("09a_halia", function()
  talk(L.npc(AK .. "Alethea"), { shotBefore = "alethea_pointer" })
  L.leaveEdge("down", S.MAP_ROUTE1)
  L.leaveEdge("down", S.MAP_ELAIA)
  musicIs(S.MUS_ELAIA, "Elaia's theme")
  local ring = L.triggers("ElaiaVillage_EventScript_HaliaSecondLook")
  expect(not L.goTrigger(ring), "the square starts Halia's second look")
  settle({ every = true })
  flagsSet({ "FLAG_HALIA_SECOND_LOOK", "FLAG_HIDE_MOM_HOME" }, "Halia has looked again; Mom has gone to the harbor")
  flagsClear({ "FLAG_HIDE_MOM_AKTI", "FLAG_HIDE_KLEON_AKTI_DOOR" }, "Mom and Kleon wait in Akti")
  shot("halia_after")
  talk(L.npc("ElaiaVillage_EventScript_Halia"), { shotBefore = "halia_go_on" })
end)

-- Beat 9B: up to Akti; the wind turns, Kleon has his laurel, Mom brings honey.
beat("09b_winds", function()
  L.leaveEdge("up", S.MAP_ROUTE1)
  L.leaveEdge("up", S.MAP_AKTI, true)
  settle({ every = true })
  shot("wind_from_the_south")
  local honey = L.itemCount(S.ITEM_HONEY)
  local quay = L.triggers(AK .. "WindsQuayRow9", AK .. "WindsQuayRow10", AK .. "WindsQuayRow11")
  expect(not L.goTrigger(quay), "the quay starts the winds-turned scene")
  settle({ every = true })
  flagsSet({ "FLAG_WINDS_TURNED", "FLAG_MOM_HARBOR", "FLAG_HIDE_ALETHEA_AKTI", "FLAG_HIDE_KLEON_AKTI_DOOR" },
           "the wind has turned, Mom has been, and the others are aboard")
  L.check(L.itemCount(S.ITEM_HONEY) == honey + 2, string.format("Mom's two Honey (%d -> %d)", honey,
                                                                L.itemCount(S.ITEM_HONEY)))
  talk(L.npc(AK .. "Mom"), { shotBefore = "mom_on_the_quay" })
  -- re-entering Akti now replays nothing
  L.useWarp(S.MAP_AGORA)
  L.useWarp(S.MAP_AKTI)
  wait(60)
  expect(L.idle(), "Akti after the wind is quiet")
end)

beat("09b_board", function()
  talk(L.npc(AK .. "Nausikles"), { shotBefore = "all_aboard", answers = { "yes" } })
  L.waitUntil(function() return mapId() == S.MAP_DECK end, 600, "the Euploia's deck")
  flagsSet({ "FLAG_BOARDED_EUPLOIA", "FLAG_HIDE_MOM_AKTI" }, "aboard, and Mom has gone home")
  flagsClear({ "FLAG_HIDE_MOM_HOME" }, "Mom is home again")
  -- "Cast off!" plays on arrival
  settle({ every = true })
  musicIs(S.MUS_TRIREME, "the crossing's theme")
  shot("aboard")
end)

-- Beat 10: the crossing. The deck's people, trainers and items, and the hold, first;
-- then Nausikles's steering oar starts the calm, the snatchers and the night leg.
local TD, TH = "TriremeDeck_EventScript_", "TriremeHold_EventScript_"
beat("10_deck", function()
  trainer("ALETHEA_DECK", TD .. "Alethea", S.MUS_BATTLE_TRAINER, { answers = { "yes" } })
  flagsSet({ "FLAG_BATTLED_ALETHEA_DECK" }, "Alethea's practice battle")
  talk(L.npc(TD .. "Kleon"), { shotBefore = "kleon_at_the_rail" })
  talk(L.npc(TD .. "Lookout"), { shotBefore = "lookout" })
  trainer("LYKON", TD .. "Lykon", S.MUS_BATTLE_TRAINER)
  trainer("PHORMION", TD .. "Phormion", S.MUS_BATTLE_TRAINER)
  collect(ball("FLAG_ITEM_DECK_SUPER_POTION"), "FLAG_ITEM_DECK_SUPER_POTION", "ITEM_SUPER_POTION",
          "the Super Potion among the bow cargo")
  collect(hidden("FLAG_HIDDEN_DECK_HEART_SCALE"), "FLAG_HIDDEN_DECK_HEART_SCALE", "ITEM_HEART_SCALE",
          "the Heart Scale in the rope coil")
  talk(L.sign(TD .. "Klepsydra"), { shotBefore = "klepsydra" })
  L.useWarp(S.MAP_HOLD)
  shot("the_hold")
  for _, who in ipairs({ "LakonianRower", "Rower1", "Rower2", "Rower3" }) do
    talk(L.npc(TH .. who), { shotBefore = string.lower(who) })
  end
  collect(ball("FLAG_ITEM_HOLD_POTION"), "FLAG_ITEM_HOLD_POTION", "ITEM_POTION", "the Potion under the bottom bench")
  L.useWarp(S.MAP_DECK)
end)

beat("10_calm", function()
  -- the steering oar: the calm, the split reed, Kleon's stroke, then a free moment
  talk(L.npc(TD .. "Nausikles"), { shotBefore = "steering_oar", answers = { "yes" }, every = true })
  shot("the_calm")
  talk(L.sign(TD .. "Klepsydra"), { shotBefore = "klepsydra_upward" })
  -- the lookout's shout: crossing x = 8 walks the player to the bow
  local bow = L.triggers(TD .. "ToBowRow4", TD .. "ToBowRow5", TD .. "ToBowRow6", TD .. "ToBowRow7",
                         TD .. "ToBowRow8", TD .. "ToBowRow9")
  expect(not L.goTrigger(bow), "the bow line starts the nest scene")
  -- the snatchers (fought: no running), the hatching, the chick (take it, no
  -- nickname), the night leg, and on to Aigina's quay
  settle({ every = true, answers = { "yes", "no" } })
  L.waitUntil(function() return mapId() == S.MAP_AEGINA end, 3000, "Aigina's quay")
  settle({ every = true })
  flagsSet({ "FLAG_SAVED_HALCYON_NEST", "FLAG_GOT_HALCYLING" }, "the nest is saved and the chick taken")
  flagsClear({ "FLAG_NO_WHITEOUT", "FLAG_NO_RUNNING" }, "the snatcher battles' flags are cleared")
  flagsSet({ "FLAG_ARRIVED_AEGINA", "FLAG_VISITED_AEGINA", "FLAG_HIDE_AEGINA_CAST" }, "the arrival on Aigina")
  shot("aigina_by_night")
end)

-- Beat 10B: a night ashore on Aigina.
local AG = "AeginaTown_EventScript_"
beat("10b_aigina", function()
  visitAll({
    visitTalk("gatekeeper", npc(AG .. "Gatekeeper")),
    visitTalk("fisherwoman", npc(AG .. "Fisherwoman")),
    visitTalk("kid", npc(AG .. "Kid")),
    visitTalk("kolona", sign(AG .. "Kolona")),
    visitTalk("town_sign", sign(AG .. "TownSign")),
    visitItem("the Big Pearl at the end of the mole", hidden("FLAG_HIDDEN_AEGINA_BIG_PEARL"),
              "FLAG_HIDDEN_AEGINA_BIG_PEARL", "ITEM_BIG_PEARL"),
    visitItem("the Stardust at Kolona's foot", hidden("FLAG_HIDDEN_AEGINA_STARDUST"),
              "FLAG_HIDDEN_AEGINA_STARDUST", "ITEM_STARDUST"),
  })
  L.useWarp(S.MAP_AEGINA_MINT)
  talk(L.npc("AeginaTown_Mint_EventScript_Pheidon"), { shotBefore = "pheidon", answers = { "no" } })
  L.useWarp(S.MAP_AEGINA)
  L.useWarp(S.MAP_AEGINA_AIAKIDES)
  talk(L.npc("AeginaTown_AiakidesHouse_EventScript_Aiakides"), { shotBefore = "aiakides" })
  L.useWarp(S.MAP_AEGINA)
  L.useWarp(S.MAP_AEGINA_INN)
  -- bed: the night by the hearth, Kleon's question (the second answer), then the
  -- deck at dawn, where beat 10C plays
  talk(L.npc("AeginaTown_Inn_EventScript_Endeis"), { shotBefore = "endeis", answers = { "yes", "down" }, every = true,
                                                      stop = function() return mapId() == S.MAP_DECK and L.inOverworld() end })
  L.waitUntil(function() return mapId() == S.MAP_DECK end, 3000, "the deck at dawn")
  flagsSet({ "FLAG_AEGINA_NIGHT" }, "the night at the inn")
end)

-- Beat 10C: the last leg. The Euploia makes Emporion's quay, where beat 11 plays
-- on arrival; the next beat starts there.
beat("10c_last_leg", function()
  settle({ every = true, stop = function() return mapId() == S.MAP_HARBOR and L.inOverworld() end })
  mapIs(S.MAP_HARBOR, "the Euploia makes Emporion's quay")
  flagsSet({ "FLAG_CROSSING_DONE", "FLAG_VISITED_EMPORION" }, "the crossing is done, and Emporion is on the map")
  flagsClear({ "FLAG_ARRIVED_EMPORION" }, "beat 11 is still to play")
end)

-- === Phase 2, batch 2: Emporion and the Temple of Hermes (beats 11-16) ============================

local EH, EC = "EmporionHarbor_EventScript_", "EmporionCity_EventScript_"
local HM = "EmporionCity_TempleOfHermes_EventScript_"
local KLEON_2 = { [0] = "KLEON_2_KYNDER", [1] = "KLEON_2_HIPLING", [2] = "KLEON_2_NEBREL" }

-- A shop: the BUY list looked at, then out. The shop menus aren't script
-- prompts, so this is played by hand, as Demeas's is.
local function shop(target, name)
  talk(target, { shotBefore = name, noSettle = true })
  local t0 = now()
  while not L.taskRunning("Task_ShopMenu") do
    tap(K.A); wait(20)
    if now() - t0 > 900 then L.fail(name .. ": the shop menu never opened") end
  end
  wait(20); tap(K.A)                                                  -- BUY
  L.waitUntil(function() return L.taskRunning("Task_BuyMenu") end, 600, name .. "'s item list")
  wait(40); shot(name .. "_wares")
  if L.pilot and name == "general_stall" then L.pilot.buyMedicine() end
  tap(K.B)
  L.waitUntil(function() return L.taskRunning("Task_ShopMenu") end, 600, name .. "'s menu again")
  wait(20); tap(K.B)                                                  -- QUIT
  settle()
end
local function visitShop(name, where) return visit(name, where, function() shop(where(), name) end) end

-- The city's scene treads, kept off until the beat that means to step on them:
-- the temple stair's bottom tread (beat 14) and the Isthmus Gate (beat 16).
local function holdCity()
  local hold = L.triggers(EC .. "KleonStepsX21", EC .. "KleonStepsX22", EC .. "KleonStepsX23",
                          EC .. "KleonStepsX24", EC .. "KleonStepsX25")
  if not getFlag(S.FLAG_KLEON_BATTLE_2_DONE) then
    for k in pairs(L.triggers(EC .. "IsthmusGateX7", EC .. "IsthmusGateX8", EC .. "IsthmusGateX9")) do hold[k] = true end
  end
  L.keepOff[S.MAP_CITY] = hold
end
local function gateTread() return L.triggers(EC .. "IsthmusGateX7", EC .. "IsthmusGateX8", EC .. "IsthmusGateX9") end

-- Beat 11: the herald on the quay.
beat("11_quay", function()
  musicIs(S.MUS_EMPORION, "Emporion's theme on the quay")
  shot("emporion_quay")
  -- Kleon's sprint; Kerykos and the herm, where MAKE AN OFFERING is sent back to
  -- PRAY; the oil, the Trowel, the planter's dig, and Alethea off to the Deigma
  settle({ every = true, answers = { "down", "yes" } })
  flagsSet({ "FLAG_ARRIVED_EMPORION", "FLAG_RITES_TUTORIAL", "FLAG_GOT_TROWEL", "FLAG_DUG_EMPORION_QUAY",
             "FLAG_HIDE_KLEON_QUAY", "FLAG_HIDE_KERYKOS_QUAY", "FLAG_HIDE_ALETHEA_QUAY" },
           "beat 11: arrived, the rites tutorial and oil, the Trowel, the dig")
  L.check(not (L.npc(EH .. "Kleon").present or L.npc(EH .. "Kerykos").present or L.npc(EH .. "Alethea").present),
          "Kleon, Kerykos and Alethea have left the quay")
  shot("quay_after")
end)

-- The harbor district: its people, signs and items, and the hiring hall.
beat("11_harbor", function()
  visitAll({
    visitTalk("quay_herm", sign(EH .. "QuayHerm")),                     -- an altar now: PRAY
    visitTalk("planter_dug", sign(EH .. "Planter")),
    visitTalk("city_sign", sign(EH .. "CitySign")),
    visitItem("the Heart Scale on the quay steps", hidden("FLAG_HIDDEN_EMPORION_HEART_SCALE"),
              "FLAG_HIDDEN_EMPORION_HEART_SCALE", "ITEM_HEART_SCALE"),
    visit("nausikles_stay", npc(EH .. "Nausikles"), function()
      talk(L.npc(EH .. "Nausikles"), { shotBefore = "nausikles", answers = { "down" } })   -- STAY
      mapIs(S.MAP_HARBOR, "STAY keeps the player on the quay")
    end),
    visitTalk("customs_man", npc(EH .. "CustomsMan")),
    visit("glykera", npc(EH .. "Glykera"), function()
      talk(L.npc(EH .. "Glykera"), { shotBefore = "glykera" })           -- YES: oil for the fan
      flagsSet({ "FLAG_DAEDALUS_PAGE_1" }, "Glykera trades Daedalus's page I for an Olive Oil")
      talk(L.npc(EH .. "Glykera"), { shotBefore = "glykera_after" })
    end),
    visitTalk("wine_seller", npc(EH .. "WineSeller")),
    visitTalk("harbor_road_sign", sign(EH .. "HarborRoadSign")),
    visitTalk("stevedore", npc(EH .. "Stevedore")),
    visitTalk("dockhand", npc(EH .. "Dockhand")),
    visitTalk("hiring_board", sign(EH .. "HiringBoard")),
    visitTalk("sailor", npc(EH .. "Sailor")),
    visitTalk("mother", npc(EH .. "Mother")),
    visitTalk("son", npc(EH .. "Son")),
    visitItem("the Super Potion on the ship sheds' slipway", ball("FLAG_ITEM_EMPORION_SUPER_POTION"),
              "FLAG_ITEM_EMPORION_SUPER_POTION", "ITEM_SUPER_POTION"),
    visitTalk("dig_sheds", sign(EH .. "DigShipsheds")),
    visitItem("the Bronze Obol in the harbor wall", hidden("FLAG_HIDDEN_EMPORION_BRONZE_OBOL"),
              "FLAG_HIDDEN_EMPORION_BRONZE_OBOL", "ITEM_RELIC_COPPER"),
    visit("halitherses", npc(EH .. "Halitherses"), function()
      talk(L.npc(EH .. "Halitherses"), { shotBefore = "halitherses" })
      flagsSet({ "FLAG_MET_HALITHERSES" }, "Halitherses introduces himself")
      talk(L.npc(EH .. "Halitherses"), { shotBefore = "halitherses_omen" })   -- today's omen
    end),
    visitTalk("poseidon_altar", sign(EH .. "PoseidonAltar")),
    visitTalk("victors_wreath", sign(EH .. "VictorsWreath")),
    visitTalk("stevedore_2", npc(EH .. "Stevedore2")),
  })
  -- the Titans' hiring hall, in the warehouse by the ship sheds
  local HH = "EmporionCity_HiringHall_EventScript_"
  L.useWarp(S.MAP_HIRING_HALL)
  shot("hiring_hall")
  local n0 = #L.battles
  collect(npc(HH .. "CrewBoss"), "FLAG_HIRING_HALL", "ITEM_ROCKY_HELMET", "the crew boss's Rocky Helmet",
          { shotBefore = "crew_boss" })
  expect(#L.battles == n0 + 1, "one battle with the crew boss, and no second")
  battleCheck(L.battles[n0 + 1], "CREW_BOSS", S.MUS_TITAN, "the crew boss")
  visitAll({
    visitTalk("hall_dockhand", npc(HH .. "Dockhand")),
    visitTalk("ledger", sign(HH .. "Ledger")),
    visitTalk("sickle_crate", sign(HH .. "SickleCrate")),
    visitTalk("crates", sign(HH .. "Crates")),
    visitTalk("helmets", sign(HH .. "Helmets")),
    visitTalk("hoist", sign(HH .. "Hoist")),
    visitTalk("shed_doors", sign(HH .. "ShedDoors")),
  })
  L.useWarp(S.MAP_HARBOR)
end)

-- Up the harbor road into the city: the Agora and its people, the snatcher,
-- Number Nine, the signs and items. The temple stair and the Isthmus Gate wait.
beat("11_city", function()
  L.leaveEdge("up", S.MAP_CITY)
  musicIs(S.MUS_EMPORION, "Emporion's theme in the city")
  shot("harbor_road")
  holdCity()
  local relics = L.itemCount(S.ITEM_RELIC_COPPER)
  visitAll({
    visitTalk("fork_sign", sign(EC .. "ForkSign")),
    visitTalk("nemea_sign", sign(EC .. "NemeaGateSign")),
    visitTalk("nemea_hoplite", npc(EC .. "NemeaHoplite")),
    visitTalk("asclepeion_sign", sign(EC .. "AsclepeionSign")),
    visitTalk("deigma_sign", sign(EC .. "DeigmaSign")),
    visitTalk("metic", npc(EC .. "Metic")),
    visitItem("the Repel behind the Deigma", ball("FLAG_ITEM_EMPORION_REPEL"), "FLAG_ITEM_EMPORION_REPEL", "ITEM_REPEL"),
    visit("great_herm", sign(EC .. "GreatHerm"), function()
      talk(L.sign(EC .. "GreatHerm"), { shotBefore = "great_herm" })      -- YES: anoint it
      flagsSet({ "FLAG_HERM_EMPORION" }, "the crossroads herm is anointed")
    end),
    visitShop("general_stall", npc(EC .. "GeneralStallkeeper")),
    visitShop("kydon", npc(EC .. "Kydon")),
    visitShop("offerings_stall", npc(EC .. "OfferingsStallkeeper")),
    visit("pasion", npc(EC .. "Pasion"), function()
      local money = L.money()
      talk(L.npc(EC .. "Pasion"), { shotBefore = "pasion" })              -- YES: sell him the obol
      L.check(L.money() == money + 600, string.format("Pasion pays 600 for a Bronze Obol (money %d -> %d)",
                                                      money, L.money()))
    end),
    visitTalk("elder", npc(EC .. "Elder")),
    visitItem("the Honey under Kydon's awning", hidden("FLAG_HIDDEN_EMPORION_HONEY"), "FLAG_HIDDEN_EMPORION_HONEY",
              "ITEM_HONEY"),
    -- one jar in four holds a Pithound (run from, if one does)
    visitTalk("stoa_jar", sign(EC .. "Pithos")),
    visitItem("the X Speed at the end of the stoa", ball("FLAG_ITEM_EMPORION_X_SPEED"), "FLAG_ITEM_EMPORION_X_SPEED",
              "ITEM_X_SPEED"),
    visitTalk("spice_seller", npc(EC .. "SpiceSeller")),
    visitShop("scroll_stall", npc(EC .. "ScrollStallkeeper")),
    visitTalk("man_with_a_lamp", npc(EC .. "ManWithALamp")),
    visitTalk("shopper", npc(EC .. "Shopper")),
    visitTalk("kid", npc(EC .. "Kid")),
    visitTalk("agora_sign", sign(EC .. "AgoraSign")),
    visit("sykeas_and_the_snatcher", npc(EC .. "Sykeas"), function()
      talk(L.npc(EC .. "Sykeas"), { shotBefore = "sykeas_before" })
      -- the snatcher on his awning: a static battle, gone whatever happens
      local n0 = #L.battles
      talk(L.npc(EC .. "Harpeck"), { shotBefore = "harpeck" })
      expect(#L.battles == n0 + 1 and not L.battles[n0 + 1].trainer, "a wild battle with Sykeas's snatcher")
      flagsSet({ "FLAG_HIDE_SYKEAS_HARPECK" }, "the snatcher is gone after its battle")
      L.check(not L.npc(EC .. "Harpeck").present, "the snatcher is off the awning")
      collect(npc(EC .. "Sykeas"), "FLAG_GOT_SYKEAS_FIGS", "ITEM_FIGY_BERRY", "Sykeas's figs",
              { shotBefore = "sykeas_after" })
      L.check(L.itemCount(S.ITEM_PRETTY_FEATHER) >= 1, "and the feather the snatcher dropped")
    end),
    visitTalk("fishmonger", npc(EC .. "Fishmonger")),
    visit("number_nine", npc(EC .. "NumberNine"), function()
      talk(L.npc(EC .. "NumberNine"), { shotBefore = "number_nine" })     -- YES: untie it
      flagsSet({ "FLAG_NUMBER_NINE_UNTIED" }, "Number Nine walks off his plinth")
      L.check(not L.npc(EC .. "NumberNine").present, "Number Nine has gone")
      talk(L.sign(EC .. "EmptyPlinth"), { shotBefore = "empty_plinth" })
    end),
    visitTalk("tavern_sign", sign(EC .. "TavernSign")),
    visitTalk("pilgrim", npc(EC .. "Pilgrim")),
    visitTalk("runner", npc(EC .. "Runner")),
    visitTalk("temple_sign", sign(EC .. "TempleSign")),
    visitTalk("peirene", sign(EC .. "Peirene")),
    visitTalk("cistern", sign(EC .. "Cistern")),
    visitTalk("cistern_sign", sign(EC .. "CisternSign")),
    visitTalk("hephaisteion_sign", sign(EC .. "HephaisteionSign")),
    visitTalk("dig_garden", sign(EC .. "DigHephaisteion")),
    visitTalk("isthmus_gate_sign", sign(EC .. "IsthmusGateSign")),
    visitItem("the Stardust at the top of Acrocorinth's stair", hidden("FLAG_HIDDEN_EMPORION_STARDUST"),
              "FLAG_HIDDEN_EMPORION_STARDUST", "ITEM_STARDUST"),
  })
  L.check(L.itemCount(S.ITEM_RELIC_COPPER) == relics - 1, "the obol went to Pasion")
end)

-- The city's rooms, before the temple: the Asclepeion, the Deigma (beat 12), the
-- Dolphin, the households, the runners, the potter and the Hephaisteion (beat 13).
local function room(map, fn)
  holdCity()
  L.useWarp(map)
  fn()
  L.useWarp(S.MAP_CITY)
end

beat("11_asclepeion", function()
  local A = "EmporionCity_Asclepeion_EventScript_"
  room(S.MAP_E_ASCLEPEION, function()
    shot("asclepeion")
    talk(L.npc(A .. "Healer"), { shotBefore = "healer" })
    local hp, maxHp = L.partyHp(0)
    expect(hp == maxHp and hp > 1, string.format("Emporion's healer restored the party (%d/%d)", hp, maxHp))
    local hmap = L.lastHeal()
    expect(hmap == S.MAP_CITY, string.format("the respawn point is Emporion (map %d)", hmap))
    -- (the Pithos's menu would open the box: the slice's run leaves it shut)
    visitAll({
      visitTalk("panacoil", npc(A .. "Panacoil")),
      visitTalk("asclepeion_sailor", npc(A .. "Sailor")),
      visitTalk("old_woman", npc(A .. "OldWoman")),
      visitTalk("young_healer", npc(A .. "YoungHealer")),
      visitTalk("asclepius", sign(A .. "Statue")),
      visitTalk("bell_pull", sign(A .. "BellPull")),
      visitTalk("anchors", sign(A .. "Anchors")),
      visitTalk("votives", sign(A .. "Votives")),
    })
  end)
end)

-- Beat 12: the Deigma, forty lamps. It plays on the first visit after beat 11.
beat("12_deigma", function()
  local D = "EmporionCity_Deigma_EventScript_"
  holdCity()
  expect(not getFlag(S.FLAG_DEIGMA_CLUE), "no clue before the Deigma")
  L.useWarp(S.MAP_DEIGMA, true)
  shot("deigma_alethea")
  settle({ every = true })
  flagsSet({ "FLAG_DEIGMA_CLUE" }, "beat 12: Alethea learns of the forty lamps and sees the hook (FLAG_ICHOR_DEIGMA_CLUE)")
  L.check(not L.npc(D .. "Alethea").present, "Alethea has left the Deigma")
  visitAll({
    visitTalk("lampis", npc(D .. "Lampis")),
    -- Thaletas wants an Onotis for his Narkeray; the run has none: NO
    visitTalk("thaletas", npc(D .. "Thaletas"), { shotBefore = "thaletas", answers = { "no" } }),
    visitTalk("wool_merchant", npc(D .. "WoolMerchant")),
    visitTalk("grain_trader", npc(D .. "GrainMerchant")),
    visitTalk("notice", sign(D .. "Notice")),
    visitTalk("scribes_desk", sign(D .. "ScribesDesk")),
    visitTalk("register", sign(D .. "Register")),
    visitTalk("tunny", sign(D .. "Tunny")),
    visitTalk("lamps", sign(D .. "Lamps")),
    visitTalk("wool", sign(D .. "Wool")),
    visitTalk("oil", sign(D .. "Oil")),
    visitTalk("grain", sign(D .. "Grain")),
    visitTalk("helmet", sign(D .. "Helmet")),
    visitTalk("scales", sign(D .. "Scales")),
  })
  flagsClear({ "FLAG_TRADED_NARKERAY" }, "no trade without an Onotis")
  L.finding(L.distanceTo(L.npc(D .. "Narkeray")) ~= nil,
            "Thaletas's Narkeray can be looked at (Thaletas stands in the only way to the quay edge beside it)")
  L.useWarp(S.MAP_CITY)
  -- back in, beat 12 doesn't play again
  L.useWarp(S.MAP_DEIGMA)
  expect(L.idle() and not L.npc(D .. "Alethea").present, "beat 12 plays once")
  L.useWarp(S.MAP_CITY)
end)

-- The Dolphin: knucklebones with the champion and both regulars, until each is beaten once.
beat("11_tavern", function()
  local TV = "EmporionCity_Tavern_EventScript_"
  local function knucklebones(who, flag, item, quantity)
    local before, tries = item and L.itemCount(S[item]), 0
    while not getFlag(S[flag]) do
      tries = tries + 1
      if tries > 25 then L.check(false, who .. ": never won at knucklebones in 25 games") return end
      talk(L.npc(TV .. who), { shotBefore = tries == 1 and string.lower(who) or nil,
                             menuChoice = 4, limit = 40000 })
    end
    log(string.format("ok beat %s at knucklebones in %d game(s) (%s)", who, tries, flag))
    if item then
      L.check(L.itemCount(S[item]) == before + quantity, string.format("%s's prize: %s (%d -> %d)", who, item, before,
                                                          L.itemCount(S[item])))
    end
  end
  room(S.MAP_TAVERN, function()
    shot("tavern")
    knucklebones("Myrtale", "FLAG_KNUCKLEBONES_EMPORION")          -- TM Fling (a flag until the TM exists)
    knucklebones("Strepsiades", "FLAG_KNUCKLEBONES_STREPSIADES", "ITEM_OLIVE_OIL", 2)
    knucklebones("Stratyllis", "FLAG_KNUCKLEBONES_STRATYLLIS", "ITEM_WINE", 1)
    visitAll({
      visitTalk("bones_table", sign(TV .. "BonesTable")),
      visitTalk("tavern_mosaic", sign(TV .. "Mosaic")),
      visitTalk("rack", sign(TV .. "Rack")),
      visitTalk("krater", sign(TV .. "Krater")),
      visitTalk("nets", sign(TV .. "Nets")),
    })
  end)
end)

beat("11_households", function()
  local PX, WD = "EmporionCity_PhiloxenosHouse_EventScript_", "EmporionCity_WidowsHouse_EventScript_"
  room(S.MAP_PHILOXENOS, function()
    shot("philoxenos_house")
    -- he feeds you first (a heal), then offers the guest bed (YES)
    talk(L.npc(PX .. "Philoxenos"), { shotBefore = "philoxenos" })
    flagsClear({ "FLAG_PHILOXENOS_LAUREL_2" }, "no laurel story before the Herald Laurel")
    visitAll({
      visitTalk("cook", npc(PX .. "Cook")),
      visitTalk("philoxenos_mosaic", sign(PX .. "Mosaic")),
      visitTalk("philoxenos_hearth", sign(PX .. "Hearth")),
      visitTalk("guest_bed", sign(PX .. "GuestBed")),
      visitTalk("washbasin", sign(PX .. "Washbasin")),
    })
  end)
  room(S.MAP_WIDOW, function()
    shot("widows_house")
    collect(npc(WD .. "Penelopeia"), "FLAG_GOT_WIDOWS_GIFT", "ITEM_SEA_INCENSE", "Penelopeia's Sea Incense",
            { shotBefore = "penelopeia" })
    L.finding(L.distanceTo(L.sign(WD .. "Loom")) ~= nil,
              "Penelopeia's loom can be looked at (she stands in the only way to the place in front of it)")
    visitAll({
      visitTalk("widow_window", sign(WD .. "Window")),
      visitTalk("oar", sign(WD .. "Oar")),
      visitTalk("shrine", sign(WD .. "Shrine")),
    })
  end)
end)

beat("11_workshops", function()
  local RH, PW = "EmporionCity_RunnersHouse_EventScript_", "EmporionCity_PottersWorkshop_EventScript_"
  room(S.MAP_RUNNERS, function()
    shot("runners_house")
    collect(npc(RH .. "Dromokleia"), "FLAG_GOT_QUICK_CLAW", "ITEM_QUICK_CLAW", "Dromokleia's Quick Claw",
            { shotBefore = "dromokleia" })
    flagsClear({ "FLAG_WROTE_TO_MOM" }, "no letter home before the end of Act I")
    visitAll({
      visitTalk("stretcher", npc(RH .. "Runner")),
      visitTalk("young_runner", npc(RH .. "YoungRunner")),
      visitTalk("road_map", sign(RH .. "RoadMap")),
      visitTalk("ribbon", sign(RH .. "Ribbon")),
      visitTalk("water_jar", sign(RH .. "WaterJar")),
      visitTalk("runners_klepsydra", sign(RH .. "Klepsydra")),
      visitTalk("sandals", sign(RH .. "Sandals")),
    })
  end)
  room(S.MAP_POTTER, function()
    shot("potters_workshop")
    -- Euphronios paints a Harpeck, then a Chelonet, then a Stachyss: the run carries none
    talk(L.npc(PW .. "Euphronios"), { shotBefore = "euphronios" })
    flagsClear({ "FLAG_EUPHRONIOS_1" }, "no painting without a Harpeck in the party")
    note("Euphronios's paintings wait for a Harpeck, a Chelonet and a Stachyss, which the run doesn't catch")
    visitAll({
      visitTalk("potter_apprentice", npc(PW .. "Apprentice")),
      visitTalk("kiln", sign(PW .. "Kiln")),
      visitTalk("wheel", sign(PW .. "Wheel")),
      visitTalk("signature", sign(PW .. "Signature")),
      visitTalk("shelves", sign(PW .. "Shelves")),
      visitTalk("paint_table", sign(PW .. "PaintTable")),
      visitTalk("slip_pots", sign(PW .. "SlipPots")),
      visitTalk("clay_bin", sign(PW .. "ClayBin")),
    })
  end)
end)

-- Beat 13: the cold forge. The slice's Charcoal, from Hestia's own hearth, relights it.
beat("13_forge", function()
  local HP = "EmporionCity_Hephaisteion_EventScript_"
  room(S.MAP_HEPHAISTEION, function()
    shot("cold_forge")
    expect(L.itemCount(S.ITEM_CHARCOAL) == 1, "the Charcoal from the Hearth Trial is in the bag")
    talk(L.npc(HP .. "Kedalion"), { shotBefore = "kedalion", every = true })   -- YES: spare a sliver
    flagsSet({ "FLAG_FORGE_RELIT", "FLAG_GOT_BRONZE_HAMMER" }, "beat 13: the forge is relit, and the Bronze Hammer")
    L.check(L.itemCount(S.ITEM_CHARCOAL) == 1, "the Charcoal isn't used up")
    shot("forge_lit")
    talk(L.npc(HP .. "Kedalion"), { shotBefore = "kedalion_after" })
    visitAll({
      visitTalk("smith_apprentice", npc(HP .. "Apprentice")),
      visitTalk("forge", sign(HP .. "Forge")),
      visitTalk("bellows", sign(HP .. "Bellows")),
      visitTalk("tongs_rack", sign(HP .. "TongsRack")),
      visitTalk("trough", sign(HP .. "Trough")),
      visitTalk("workbench", sign(HP .. "Workbench")),
      visitTalk("smith_votives", sign(HP .. "Votives")),
    })
  end)
end)

-- Beat 14: Kleon on the temple steps, then the Isthmus Gate before the Laurel.
beat("14_temple_steps", function()
  holdCity()
  expect(not getFlag(S.FLAG_KLEON_WON_HERALD), "Kleon hasn't won the Herald Laurel yet")
  -- Beat 14 waits on the stair's bottom tread: is that the only way up to the door?
  local door
  for _, w in ipairs(L.mapEvents().warps) do if w.map == S.MAP_HERMES then door = w end end
  L.finding(L.distanceTo({ tiles = { { x = door.x, y = door.y } } }) == nil,
            "the temple door can't be reached without the stair's bottom tread (else beat 14 is skipped, "
            .. "and beat 16 plays to a hidden Kleon)")
  local tread = L.triggers(EC .. "KleonStepsX21", EC .. "KleonStepsX22", EC .. "KleonStepsX23",
                           EC .. "KleonStepsX24", EC .. "KleonStepsX25")
  expect(not L.goTrigger(tread), "the temple stair's bottom tread starts beat 14")
  wait(30); shot("kleon_on_the_steps")
  settle({ every = true })
  flagsSet({ "FLAG_KLEON_WON_HERALD", "FLAG_HIDE_KLEON_TEMPLE_STEPS" }, "beat 14: Kleon won the Herald Laurel first")
  flagsClear({ "FLAG_HIDE_KLEON_ISTHMUS_GATE" }, "Kleon waits at the Isthmus Gate")
  L.check(not L.npc(EC .. "KleonSteps").present, "Kleon has run off from the steps")
  -- the Isthmus Gate before the Herald Laurel: the hoplites turn the player back
  local gate = gateTread()
  expect(not L.goTrigger(gate), "the Isthmus Gate's hoplites stop the player")
  wait(30); shot("gate_shut")
  settle()
  expect(mapId() == S.MAP_CITY and not L.onTile(gate), "turned back from the Isthmus Gate without a laurel")
  flagsClear({ "FLAG_KLEON_BATTLE_2_DONE" }, "no battle with Kleon before the Laurel")
end)

-- Beat 15: the Temple of Hermes and the Herald's Run.
-- The turnstiles turn one way only, so walks in the temple keep off them; the
-- Run itself is walked by the builder's solving route (temple_hermes.lua), the
-- one place this run names coordinates.
local function holdTemple()
  local step, hold = S.SCRIPTS[HM .. "Step"], {}
  for _, c in ipairs(L.mapEvents().coords) do
    if c.script ~= step then hold[c.x .. "," .. c.y] = true end
  end
  L.keepOff[S.MAP_HERMES] = hold
end
-- Walk the waypoints, each in a straight line from the last (x first). A turnstile
-- passed the right way carries the player a tile on; a trainer's sight or the
-- glass speaking at a mark takes control, and the walk plays that out and goes on.
local function runTo(points)
  for _, p in ipairs(points) do
    for _ = 1, 100 do
      local x, y = pos()
      if x == p[1] and y == p[2] then break end
      local key
      if x < p[1] then key = K.RIGHT elseif x > p[1] then key = K.LEFT
      elseif y < p[2] then key = K.DOWN else key = K.UP end
      local r = L.step(key)
      if r == "blocked" then shot("run_blocked"); L.fail(string.format("the Run's route is blocked at (%d,%d)", x, y)) end
      if r == "taken" then settle() end
    end
    local x, y = pos()
    if x ~= p[1] or y ~= p[2] then L.fail(string.format("the Run never reached (%d,%d) (at %d,%d)", p[1], p[2], x, y)) end
  end
end
local function glass() return L.getVar(S.VAR_TEMP_2) end
local function delivered() return L.getVar(S.VAR_TEMP_1) end
local function running() return L.getVar(S.VAR_TEMP_3) == 1 end
-- Something by the route, spoken to where the route puts the player (no steps off the glass).
local function here(target, opts)
  expect(L.distanceTo(target) == 0, "at " .. target.what .. " without a step off the route")
  talk(target, opts)
end
local function herm(name, flag)
  local oil = L.getVar(S.VAR_TEMP_5)
  here(L.sign(HM .. "Herm" .. name), { shotBefore = "oil_" .. string.lower(name) })   -- YES: oil his face
  L.check(getFlag(S[flag]) and L.getVar(S.VAR_TEMP_5) == oil - 1, name .. " is oiled, and turns to point the way")
end
local function deliver(name, n)
  here(L.sign(HM .. "Herm" .. name), { shotBefore = "deliver_" .. string.lower(name), every = n == 3 })
  L.check(delivered() == n or (n == 3 and getFlag(S.FLAG_HERALDS_RUN_DONE)),
          string.format("%s takes scroll %d (glass %d)", name, n, glass()))
end
-- An acolyte who stopped the player on the route: the after-battle line, said where they stand.
local function acolyte(name, script)
  local id = S["TRAINER_" .. name]
  expect(L.defeated(id), name .. " is beaten")
  local rec
  for _, b in ipairs(L.battles) do if b.who == name then rec = b end end
  battleCheck(rec, name, S.MUS_BATTLE_TRAINER, name)
  local n1 = trainerBattles()
  here(L.npc(script), { shotBefore = string.lower(name) .. "_after" })
  L.check(trainerBattles() == n1, name .. " does not battle again")
end

beat("15_temple", function()
  holdCity()
  L.useWarp(S.MAP_HERMES)
  holdTemple()
  musicIs(S.MUS_TEMPLE_HERMES, "the Temple of Hermes's theme")
  shot("temple_of_hermes")
  flagsClear({ "FLAG_HERALDS_RUN_DONE", "FLAG_BADGE02_GET" }, "no run yet")
  talk(L.npc(HM .. "Angelos"), { shotBefore = "angelos" })
  talk(L.sign(HM .. "StepGlass"), { shotBefore = "step_glass" })
  -- three flasks from the jar; J1, by the door, oiled before the glass runs; and the jar again
  for _ = 1, 3 do talk(L.sign(HM .. "OilJar"), { shotBefore = "oil_jar" }) end
  expect(L.getVar(S.VAR_TEMP_5) == 3, "three flasks of oil")
  talk(L.sign(HM .. "HermJ1"), { shotBefore = "oil_j1" })
  L.check(getFlag(S.FLAG_HERMES_HERM_J1), "J1 is oiled")
  talk(L.sign(HM .. "OilJar"), { shotBefore = "oil_jar_again" })
  expect(L.getVar(S.VAR_TEMP_5) == 3, "the flasks are full again")
  -- Kerykos's rite, YES: the scrolls, and the glass begins
  talk(L.npc(HM .. "Kerykos"), { shotBefore = "kerykos_rite", every = true })
  flagsSet({ "FLAG_HERALDS_RUN_TOLD" }, "Kerykos told the rite")
  local limit = STEP_GLASS_LIMITS[DIFFICULTY]
  expect(running() and glass() == limit and delivered() == 0, string.format("the Run is on: %d steps in the glass", limit))
  L.check(not L.npc(HM .. "Kerykos").present, "Kerykos took the short way")
  musicIs(S.MUS_TEMPLE_HERMES, "the Herald's Run plays from its first bar")
end)

beat("15_herald_run", function()
  holdTemple()
  expect(running(), "the Run is on")
  -- Leg 1, the lower gallery: east along the porch, through T1, Podarge, the Threshold herm
  runTo({ { 14, 21 }, { 16, 21 } })
  acolyte("PODARGE", HM .. "Podarge")
  runTo({ { 16, 20 }, { 18, 20 } })
  deliver("H1", 1)
  -- Leg 2: back west through T1b, J2, the turnstile stair, J3, T3, the gap and Euchidas, T4, the Road herm
  runTo({ { 18, 18 }, { 17, 18 }, { 15, 18 }, { 2, 18 } })
  herm("J2", "FLAG_HERMES_HERM_J2")
  runTo({ { 2, 16 }, { 2, 14 } })
  herm("J3", "FLAG_HERMES_HERM_J3")
  runTo({ { 2, 13 }, { 3, 13 }, { 5, 13 }, { 10, 13 }, { 10, 14 }, { 10, 15 } })
  acolyte("EUCHIDAS", HM .. "Euchidas")
  runTo({ { 10, 16 }, { 15, 16 }, { 15, 15 }, { 17, 15 }, { 18, 15 } })
  deliver("H2", 2)
  -- Leg 3: the east stair, J4, T5, the Market herm
  runTo({ { 18, 13 }, { 18, 10 } })
  herm("J4", "FLAG_HERMES_HERM_J4")
  runTo({ { 18, 8 }, { 7, 8 }, { 5, 8 }, { 2, 8 } })
  local left = glass()
  expect(running() and left > 0, string.format("made the Market herm with sand to spare (%d of %d steps left)",
                                           left, STEP_GLASS_LIMITS[DIFFICULTY]))
  deliver("H3", 3)
  flagsSet({ "FLAG_HERALDS_RUN_DONE" }, "the Run is done (FLAG_ICHOR_HERALDS_RUN_DONE)")
  flagsClear({ "FLAG_HERALDS_RUN_FAILED" }, "the glass never ran dry")
  expect(not running(), "the glass stopped")
  shot("run_done")
end)

beat("15_kerykos", function()
  holdTemple()
  -- back east through T5 (turned round now), and in through T6b to Philonides, who faces the wall
  runTo({ { 5, 8 }, { 7, 8 }, { 18, 8 }, { 18, 11 }, { 17, 11 }, { 15, 11 }, { 4, 11 } })
  expect(not L.defeated(S.TRAINER_PHILONIDES), "Philonides never saw the player")
  trainer("PHILONIDES", HM .. "Philonides", S.MUS_BATTLE_TRAINER)
  -- out through T6, up through the open gate to the dais
  runTo({ { 15, 11 }, { 15, 10 }, { 17, 10 }, { 18, 10 }, { 18, 8 }, { 10, 8 }, { 10, 5 } })
  shot("the_dais")
  if L.pilot then L.pilot.recover() end
  local honey, n0 = L.itemCount(S.ITEM_HONEY), #L.battles
  talk(L.npc(HM .. "Kerykos"), { shotBefore = "kerykos_dais", every = true })
  expect(#L.battles == n0 + 1, "one battle with Kerykos")
  battleCheck(L.battles[n0 + 1], "KERYKOS", S.MUS_BATTLE_RIVAL, "Kerykos")
  flagsSet({ "FLAG_BADGE02_GET", "FLAG_GOT_TM_AERIAL_ACE", "FLAG_HERMES_OFFERING" },
           "the Herald Laurel, TM40 and Kerykos's honey")
  expect(L.itemCount(S.ITEM_TM40) == 1, "TM40 Aerial Ace in the bag")
  L.check(L.itemCount(S.ITEM_HONEY) == honey + 1, "a Honey from Kerykos's pockets")
  for _, n in ipairs({ "PODARGE", "EUCHIDAS", "PHILONIDES", "KERYKOS" }) do
    L.check(L.defeated(S["TRAINER_" .. n]), n .. " counts as beaten")
  end
  -- again: his list, and the short way down (YES)
  local n1 = #L.battles
  talk(L.npc(HM .. "Kerykos"), { shotBefore = "kerykos_after" })
  L.check(#L.battles == n1, "Kerykos does not battle again")
  mapIs(S.MAP_HERMES, "the short way down stays in the temple")
  shot("short_way_down")
  talk(L.npc(HM .. "Angelos"), { shotBefore = "angelos_after" })
  L.useWarp(S.MAP_CITY)
  musicIs(S.MUS_EMPORION, "Emporion's theme again")
end)

-- With the Herald Laurel: Philoxenos trades the story for Wine.
beat("15_laurel_story", function()
  local PX = "EmporionCity_PhiloxenosHouse_EventScript_"
  room(S.MAP_PHILOXENOS, function()
    collect(npc(PX .. "Philoxenos"), "FLAG_PHILOXENOS_LAUREL_2", "ITEM_WINE",
            "Philoxenos's Wine for the Herald Laurel's story", { shotBefore = "philoxenos_laurel" })
  end)
end)

-- Beat 16: the Isthmus Gate and Kleon's second battle.
beat("16_isthmus_gate", function()
  holdCity()
  flagsClear({ "FLAG_HIDE_KLEON_ISTHMUS_GATE" }, "Kleon waits in the Isthmus Gate")
  local gate = gateTread()
  expect(not L.goTrigger(gate), "the Isthmus Gate starts beat 16")
  wait(30); shot("kleon_at_the_gate")
  local _, fought = settle({ every = true })
  expect(#fought == 1, "one battle with Kleon")
  local rival = fought[1]
  expect(rival.trainer and rival.trainerId == S["TRAINER_" .. KLEON_2[STARTER]],
         "the actual Isthmus Gate opponent is Kleon's starter-specific second team")
  local won = rival.outcome == S.B_OUTCOME_WON
  if won then
    battleCheck(rival, KLEON_2[STARTER], S.MUS_BATTLE_RIVAL, "Kleon at the Isthmus Gate")
  else
    expect(rival.outcome == S.B_OUTCOME_LOST, "Kleon's supported second loss returns to the story")
    L.check(rival.song == L.songHeader(S.MUS_BATTLE_RIVAL), "Kleon's second loss uses the rival battle music")
    for slot = 0, emu:read8(S.gPartiesCount + S.B_TRAINER_PLAYER) - 1 do
      local hp, maxHp = L.partyHp(slot)
      expect(hp == maxHp and hp > 0, "the native loss branch heals partner " .. slot)
    end
  end
  expect(getFlag(S.FLAG_WON_KLEON_2) == won, "Kleon's second victory flag matches the actual outcome")
  flagsSet({ "FLAG_KLEON_BATTLE_2_DONE", "FLAG_HIDE_KLEON_ISTHMUS_GATE" },
           "beat 16: Kleon's second battle is complete")
  flagsClear({ "FLAG_NO_WHITEOUT" }, "the no-whiteout flag is cleared")
  L.check(not L.npc(EC .. "KleonGate").present, "Kleon has run through the gate")
  -- the hoplites step aside: the gate plays nothing now
  expect(L.goTrigger(gate), "the Isthmus Gate lets the herald through")
  expect(L.idle(), "the open Isthmus Gate preserves field control")
  shot("through_the_gate")
end)

local function healedParty(what)
  for slot = 0, emu:read8(S.gPartiesCount + S.B_TRAINER_PLAYER) - 1 do
    local hp, maxHp = L.partyHp(slot)
    expect(hp == maxHp and hp > 0, what .. " healed partner " .. slot)
  end
end

beat("17_rockslide", function()
  room(S.MAP_E_ASCLEPEION, function()
    talk(L.npc("EmporionCity_Asclepeion_EventScript_Healer"))
    healedParty("Emporion's actual clinic")
  end)
  L.leaveEdge("up", S.MAP_ROUTE4)
  mapIs(S.MAP_ROUTE4, "through the opened Isthmus Gate onto Route 4")
  local R = "Route4_Isthmus_EventScript_"
  trainer("EXEKIAS", R .. "Exekias", S.MUS_BATTLE_TRAINER)
  trainer("MYRRHINE", R .. "Myrrhine", S.MUS_BATTLE_TRAINER)
  if not L.defeated(S.TRAINER_LAAS) then talk(L.npc(R .. "Laas")) end
  expect(L.defeated(S.TRAINER_LAAS), "the herm's Titanborn guard is beaten")
  flagsSet({ "FLAG_HIDE_GRUNT_LAAS" }, "Laas leaves the actual herm")
  trainer("ISTHMUS_MENALKAS", R .. "Menalkas", S.MUS_BATTLE_TRAINER)
  trainer("PHEIDIPPOS", R .. "Pheidippos", S.MUS_BATTLE_TRAINER)
  if not getFlag(S.FLAG_SAW_ROCKSLIDE) then
    expect(not L.goTrigger(L.triggers(R .. "RockslideScene")), "the rockslide starts beat 17")
    settle({ every = true })
  end
  flagsSet({ "FLAG_SAW_ROCKSLIDE" }, "the procession's obstruction is introduced")
  trainer("KAPELOS", R .. "Kapelos", S.MUS_BATTLE_TRAINER)
  talk(L.npc(R .. "Healer"))
  healedParty("The procession's actual healer")
  local cakes = L.itemCount(S.ITEM_BARLEY_CAKE)
  for i, x in ipairs({ 52, 53, 54 }) do
    talk(x, 9, { every = true, shotBefore = "rockslide_heap_" .. i })
    flagsSet({ "FLAG_HIDE_ROCKSLIDE_" .. i }, "the Hammer clears heap " .. i)
  end
  flagsSet({ "FLAG_ROCKSLIDE_CLEARED", "FLAG_GOT_PROCESSION_BARLEY", "FLAG_ITEM_ROCK_TOMB" },
           "the actual slide rewards and open road")
  expect(L.itemCount(S.ITEM_BARLEY_CAKE) == cakes + 2, "Eudemos gives two actual Barley Cakes")
  expect(L.itemCount(S.ITEM_TM39) >= 1, "the last heap reveals the Rock Tomb scroll")
  L.useWarp(S.MAP_HOLLOW)
  mapIs(S.MAP_HOLLOW, "the cleared road reaches Hecate's Hollow")
end)

beat("18_hollow", function()
  local H = "HecatesHollow_EventScript_"
  musicIs(S.MUS_HOLLOW, "Hecate's Hollow")
  talk(L.npc(H .. "OldWoman"), { every = true })
  flagsSet({ "FLAG_MET_CRONE" }, "the old woman's warning")
  for _, name in ipairs({ "BarkLeft", "BarkRight", "BarkAhead" }) do
    expect(not L.goTrigger(L.triggers(H .. name)), "the dog guides the player: " .. name)
    settle({ every = true })
    if name == "BarkRight" then trainer("PHAINO", H .. "Phaino", S.MUS_BATTLE_TRAINER) end
  end
  talk(L.sign(H .. "Hekataion"), { answers = { "yes" }, every = true })
  flagsSet({ "FLAG_GOT_TORCH" }, "the actual crossroads offering grants Hecate's Torch")
  expect(L.itemCount(S.ITEM_HECATES_TORCH) == 1, "one real Torch, not just its story flag")
  talk(L.sign(H .. "Spring"))
  healedParty("Hecate's actual spring")
  talk(L.npc(H .. "Web", 1))
  flagsSet({ "FLAG_WEB_WEST" }, "the owned Torch opens the western web")
  L.go(5, 15)
  trainer("HEKABE", H .. "Hekabe", S.MUS_BATTLE_TRAINER)
  flagsSet({ "FLAG_HEKABE_SUPPER" }, "Hekabe's actual supper reward")
  talk(L.sign(H .. "Brazier1"))
  L.go(4, 21)
  talk(L.sign(H .. "Brazier2"))
  flagsSet({ "FLAG_HOLLOW_BRAZIER_1", "FLAG_HOLLOW_BRAZIER_2" }, "both western passages are lit")
  trainer("KALLIAS", H .. "Kallias", S.MUS_BATTLE_TRAINER)
  trainer("BATTOS", H .. "Battos", S.MUS_BATTLE_TRAINER)
  L.useWarp(S.MAP_ROUTE5)
  mapIs(S.MAP_ROUTE5, "out of the actual Hollow onto the Skironian cliffs")
  shot("beyond_the_hollow")
end)

beat("19_cliffs", function()
  local R = "Route5_SkironianCliffs_EventScript_"
  for _, t in ipairs({ { "KYNEGEIROS", "Kynegeiros" }, { "MELANTHIOS", "Melanthios" },
                      { "ARISTAIOS", "Aristaios" }, { "DAPHNIS", "Daphnis" }, { "MYRTO", "Myrto" },
                      { "MOPSOS", "Mopsos" }, { "KERDON", "Kerdon" } }) do
    trainer(t[1], R .. t[2], S.MUS_BATTLE_TRAINER)
  end
  talk(L.npc(R .. "Aigialeus"), { every = true })
  flagsSet({ "FLAG_GOT_GOOD_ROD" }, "Aigialeus gives his actual rod")
  expect(L.itemCount(S.ITEM_GOOD_ROD) == 1, "the Good Rod is owned")
  L.useWarp(S.MAP_REST_HOUSE)
  talk(L.npc("Route5_RestHouse_EventScript_Xenokles"), { answers = { "no" } })
  healedParty("Xenokles's actual hospitality")
  flagsSet({ "FLAG_MET_XENOKLES" }, "the inn's welcome is saved")
  L.useWarp(S.MAP_ROUTE5)
  L.leaveEdge("right", S.MAP_ELEUSA)
  mapIs(S.MAP_ELEUSA, "the connected cliff road reaches Eleusa")
end)

beat("20_eleusa_arrival", function()
  local V = "EleusaVillage_EventScript_"
  L.go(12, 25)
  flagsSet({ "FLAG_SAFFRON_THREAD", "FLAG_ARRIVED_ELEUSA", "FLAG_VISITED_ELEUSA" },
           "Krokis's actual thread scene and Eleusa's arrival")
  musicIs(S.MUS_ELEUSA, "Eleusa's village theme")
  talk(L.npc(V .. "Krokis"))
  talk(L.npc(V .. "Kleon"), { every = true })
  expect(L.idle(), "the continuous arrival restores field control")
  shot("eleusa_before_the_mysteries")
end)

L.start(function()
  local from = os.getenv("SLICE_FROM")
  local stop = os.getenv("SLICE_STOP_AFTER")
  if from == "" then from = nil end
  if stop == "" then stop = nil end
  expect(SPECIES[STARTER] and DIFFICULTIES[DIFFICULTY], "valid starter and difficulty")
  expect(not NATURAL or (not from and not L.workarounds), "unassisted runs cannot resume fixtures or use workarounds")
  if NATURAL then
    local function refuses(fn, reason)
      local ok, err = pcall(fn)
      expect(not ok and tostring(err):find(reason, 1, true), "natural guard rejects " .. reason)
    end
    for _, width in ipairs({ 8, 16, 32 }) do
      local value = emu["read" .. width](emu, S.gParties)
      refuses(function() emu["write" .. width](emu, S.gParties, value) end, "emulator write" .. width)
    end
    refuses(function() emu:loadStateFile("unused.ss", 31) end, "emulator loadStateFile")
    refuses(function() L.runRamScript({}) end, "a RAM script")
    refuses(L.assistLevel100, "the level-100 assist")
  end
  local first, last = 1, #BEATS
  local function beatIndex(name)
    for i, b in ipairs(BEATS) do if b.name == name then return i end end
    L.fail("unknown beat " .. name)
  end
  if from then first = beatIndex(from) end
  if stop then last = beatIndex(stop) end
  expect(first <= last, "requested beat range is in play order")
  log(string.format("note %s pilot, %s difficulty, starter %s, %s%s",
                    NATURAL and "NATURAL button-only team pilot" or "ASSISTED level-100",
                    DIFFICULTY, SPECIES[STARTER], IANTHE and "Ianthe" or "Theo",
                    from and (", resuming at " .. from) or ""))
  if from then
    wait(2)
    expect(emu:loadStateFile(L.statesDir .. from .. ".ss", 31), "loaded the state for " .. from)
    wait(2)
  else
    boot()
  end
  for i = first, last do
    L.setBeat(BEATS[i].name, not (from and i == first))
    if L.pilot and L.idle() then L.pilot.recover() end
    BEATS[i].fn()
    log("REACHED " .. BEATS[i].name)
  end
  if stop then
    log("note PARTIAL coverage ends at " .. stop .. "; not a full playthrough or balance approval")
  elseif from then
    log("note a resumed run checks only the beats it played")
  else
    -- every trainer in the slice and Phase 2 so far
    for _, n in ipairs({ "TITYROS", "THESTYLIS", "PHYLLIS", "KOMATAS", "AGIS", "POLYEIDOS", "PETROS", "AMATHOS",
                         "MENALKAS", "THYRSIS", "LYKIDAS", "LAMPON", "PYRRHA", "AITHRA", "IONE", KLEON_TRAINER[STARTER],
                         "ALETHEA_DECK", "PHORMION", "LYKON",
                         "CREW_BOSS", "PODARGE", "EUCHIDAS", "PHILONIDES", "KERYKOS", KLEON_2[STARTER],
                         "EXEKIAS", "MYRRHINE", "LAAS", "ISTHMUS_MENALKAS", "PHEIDIPPOS", "KAPELOS",
                         "PHAINO", "HEKABE", "KALLIAS", "BATTOS", "KYNEGEIROS", "MELANTHIOS", "ARISTAIOS",
                         "DAPHNIS", "MYRTO", "MOPSOS", "KERDON" }) do
      local openingLoss = NATURAL and n == KLEON_TRAINER[STARTER] and getFlag(S.FLAG_KLEON_BATTLE_1_DONE)
      local gateLoss = false
      if n == KLEON_2[STARTER] and getFlag(S.FLAG_KLEON_BATTLE_2_DONE) then
        for _, b in ipairs(L.battles) do
          if b.trainer and b.trainerId == S["TRAINER_" .. n] and b.outcome == S.B_OUTCOME_LOST then
            gateLoss = true
          end
        end
      end
      if not L.defeated(S["TRAINER_" .. n]) and not openingLoss and not gateLoss then L.fail(n .. " was never beaten") end
    end
    log("ok every required trainer so far is beaten (authored rival losses permit progression)")
  end
  log(string.format("ok requested coverage played through in %d frames, %d battles, %d design finding(s)",
                    now(), #L.battles, L.findings))
  if L.bugs > 0 then L.fail(string.format("played to the end, but %d check(s) failed (the BUG lines)", L.bugs)) end
  log(stop and ("PARTIAL PASS " .. stop) or "PASS")
end)
