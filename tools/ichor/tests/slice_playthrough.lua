-- The slice playthrough, run by tools/ichor/tests/slice_playthrough.sh (read it first).
--
-- One continuous run from a fresh cartridge to "Thank you for playing", with key
-- presses only: the title, the OPTION menu, NEW GAME, Daphne's speech and the
-- naming screen, then every beat of design/phase1/SCRIPT.md in order. Walking
-- uses slice_lib.lua's breadth-first search over the live map grid. Every
-- trainer is fought, every gift and item in the slice is collected, and the game
-- is saved in the Asclepeion, reset and continued from the save.
--
-- THE ONE ASSIST: right after the starter screen, the starter's experience is set
-- to level 100's (and the game recalculates its stats). That is battle strength
-- only: its moves, met level and species are untouched, it never levels or
-- evolves, and every battle is still fought with button presses (the first
-- move for trainers, RUN for wild Pokémon). Nothing else is written to memory
-- except reading state; options are set in the OPTION menu by hand.
--
-- Env: SLICE_OUT (default build/slice/), SLICE_SYMBOLS (default <out>symbols.lua),
-- SLICE_STARTER 0 Snivy / 1 Cyndaquil / 2 Piplup (default 0),
-- SLICE_GENDER theo / ianthe (default theo), SLICE_FROM <beat> (resume from that
-- beat's save state), SLICE_WORKAROUNDS=1 (release a stuck waitmovement, logged
-- as a BUG, so the rest of the slice can still be checked).
--
-- Prints "SLICE ok ..." per check, "SLICE BEAT ..." per beat (with a save state
-- in <out>states/), "SLICE shot ..." per screenshot and "SLICE TEXT ..." per
-- message. A check that doesn't block play logs "SLICE BUG ..." and the run
-- carries on; a blocking one stops it. Ends with "SLICE PASS" only if nothing
-- failed, then "SLICE done"; any failure prints "SLICE FAIL: ..." first.

local OUT = os.getenv("SLICE_OUT") or "build/slice/"
local L = dofile("tools/ichor/tests/slice_lib.lua")
L.init{ tag = "SLICE", out = OUT, symbols = os.getenv("SLICE_SYMBOLS") or (OUT .. "symbols.lua") }
L.statesDir = OUT .. "states/"
local S, K = L.S, L.K
local emu = L.emu
local log, expect, note, wait, now, tap, shot = L.log, L.expect, L.note, L.wait, L.now, L.tap, L.shot
local getFlag, mapId, pos, settle, talk, go = L.getFlag, L.mapId, L.pos, L.settle, L.talk, L.go

local STARTER = tonumber(os.getenv("SLICE_STARTER") or "0")
local IANTHE = (os.getenv("SLICE_GENDER") or "theo") == "ianthe"
local SPECIES = { [0] = "Snivy", [1] = "Cyndaquil", [2] = "Piplup" }
local KLEON_TAKES = { [0] = 1, [1] = 2, [2] = 0 }   -- SCRIPT.md beat 3
local KLEON_TRAINER = { [0] = "KLEON_CYNDAQUIL", [1] = "KLEON_PIPLUP", [2] = "KLEON_SNIVY" }

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

-- A trainer: talk to them (walking there may get the player spotted first, and
-- the battle is played out on the way), then talk again for the after-battle line
-- and make sure it isn't a second battle.
local function trainer(name, script, song, opts)
  local id = S["TRAINER_" .. name]
  -- (they may already have spotted the player on the way to something else)
  if not L.defeated(id) then talk(L.npc(script), opts) end
  expect(L.defeated(id), name .. " is beaten")
  local rec
  for _, b in ipairs(L.battles) do if b.who == name then rec = b end end
  battleCheck(rec, name, song, name)
  local n1 = #L.battles
  talk(L.npc(script), { shotBefore = string.lower(name) .. "_after" })
  L.check(#L.battles == n1, name .. " does not battle again")
end

-- Visit a list of things in the order the map makes shortest: always the nearest
-- one the player can reach. Returns the ones that can't be reached yet.
-- Each item: { target = function() ... end, run = function() ... end, name = "..." }
local function visitAll(list, avoid)
  local left = {}
  for _, it in ipairs(list) do left[#left + 1] = it end
  local deferred = {}
  while #left > 0 do
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
-- Nothing below names a coordinate. People, signs, items, triggers and warps are
-- found on the live map by the script they run or the flag they set (slice_lib's
-- L.npc, L.sign, L.ball, L.hidden, L.triggers, L.useWarp, L.leaveEdge), so moving
-- them on a map never breaks the run; taking one away fails with its name.

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
       { shotBefore = "water_clock", shots = { [1] = "klepsydra_text" } })
  expect(getFlag(S.FLAG_SET_WATER_CLOCK), "the water clock is set")
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
  local hide = { [0] = "FLAG_HIDE_KRATER_SNIVY", [1] = "FLAG_HIDE_KRATER_CYNDAQUIL", [2] = "FLAG_HIDE_KRATER_PIPLUP" }
  local third = 3 - STARTER - KLEON_TAKES[STARTER]
  flagsSet({ hide[STARTER], hide[KLEON_TAKES[STARTER]] }, "both taken kraters are hidden")
  flagsClear({ hide[third] }, "the last krater stays: " .. SPECIES[third])
  expect(L.partyLevel(0) == 5, "the starter arrives at level 5")

  -- THE ASSIST (see the header): the starter goes to level 100.
  local species, growth, exp = L.assistLevel100()
  log(string.format("ok ASSIST: starter (species %d, growth %d) set to level 100 (exp %d)", species, growth, exp))
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
  battleCheck(fought[1], KLEON_TRAINER[STARTER], S.MUS_BATTLE_RIVAL, "Kleon")
  flagsSet({ "FLAG_KLEON_BATTLE_1_DONE", "FLAG_WON_KLEON_1", "FLAG_GOT_POKEBALLS", "FLAG_HIDE_KLEON_ELAIA",
             "FLAG_HIDE_ALETHEA_ELAIA" }, "beat 4's flags")
  flagsClear({ "FLAG_NO_WHITEOUT" }, "the no-whiteout flag is cleared")
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
    -- Kimon offers his Finizen for a Wooloo, which the slice's run doesn't catch: say no
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
    visitTalk("flock_wooloo", npc(R1 .. "FlockWooloo")),
    visitTalk("herm_north", sign(R1 .. "HermNorth")),
  })
  -- the flock is still there, so the road north is shut
  for _, it in ipairs(route1Later) do
    if it.name == "flock_wooloo" or it.name == "amaryllis_before" then
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
  })
end)

beat("05_road_open", function()
  if not route1Later then L.fail("resume at 05_route1 or earlier: the second Route 1 pass needs the first") end
  L.leaveEdge("left", S.MAP_ROUTE1)
  shot("flock_gone")
  -- the second pass: whatever the flock walled off, then Amaryllis's after-line
  for i = #route1Later, 1, -1 do
    local n = route1Later[i].name
    if n == "flock_wooloo" or n == "amaryllis_before" then table.remove(route1Later, i) end
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
  flagsSet({ "FLAG_SLICE_COMPLETE", "FLAG_HIDE_KLEON_AKTI", "FLAG_HIDE_ALETHEA_AKTI" }, "the slice is complete")
  shot("the_end")
end)

beat("08_after", function()
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

L.start(function()
  local from = os.getenv("SLICE_FROM")
  log(string.format("note starter %s, %s%s", SPECIES[STARTER], IANTHE and "Ianthe" or "Theo",
                    from and (", resuming at " .. from) or ""))
  local first = 1
  if from then
    for i, b in ipairs(BEATS) do if b.name == from then first = i end end
    wait(2)
    expect(emu:loadStateFile(L.statesDir .. from .. ".ss", 31), "loaded the state for " .. from)
    wait(2)
  else
    boot()
  end
  for i = first, #BEATS do
    L.setBeat(BEATS[i].name, not (from and i == first))
    BEATS[i].fn()
  end
  if from then
    log("note a resumed run checks only the beats it played")
  else
    -- every trainer in the slice
    for _, n in ipairs({ "TITYROS", "PHYLLIS", "KOMATAS", "AGIS", "POLYEIDOS", "PETROS", "AMATHOS", "LAMPON",
                         "PYRRHA", "AITHRA", "IONE", KLEON_TRAINER[STARTER] }) do
      if not L.defeated(S["TRAINER_" .. n]) then L.fail(n .. " was never beaten") end
    end
    log("ok every trainer in the slice is beaten")
  end
  log(string.format("ok the slice played through in %d frames, %d battles, %d design finding(s)", now(),
                    #L.battles, L.findings))
  if L.bugs > 0 then L.fail(string.format("played to the end, but %d check(s) failed (the BUG lines)", L.bugs)) end
  log("PASS")
end)
