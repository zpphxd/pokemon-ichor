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
local function collect(x, y, flag, item, what, opts)
  local before = L.itemCount(S[item])
  if getFlag(S[flag]) then L.fail(what .. ": " .. flag .. " already set before collecting") end
  talk(x, y, opts)
  local after = L.itemCount(S[item])
  L.check(after > before, string.format("%s: %s in the bag (%d -> %d)", what, item, before, after))
  L.check(getFlag(S[flag]), what .. ": " .. flag .. " set (so it can't be taken twice)")
  -- and asking again gives nothing more
  talk(x, y, { from = opts and opts.from, answers = opts and opts.answers })
  local again = L.itemCount(S[item])
  L.check(again == after, string.format("%s: a second try gives nothing (%d -> %d)", what, after, again))
end

-- A trainer: talk to them (walking there may get the player spotted first, and
-- the battle is played out on the way), then talk again for the after-battle line
-- and make sure it isn't a second battle.
local function trainer(name, x, y, song, opts)
  local id = S["TRAINER_" .. name]
  -- (they may already have spotted the player on the way to something else)
  if not L.defeated(id) then talk(x, y, opts) end
  expect(L.defeated(id), name .. " is beaten")
  local rec
  for _, b in ipairs(L.battles) do if b.who == name then rec = b end end
  battleCheck(rec, name, song, name)
  local n1 = #L.battles
  talk(x, y, { shotBefore = string.lower(name) .. "_after" })
  L.check(#L.battles == n1, name .. " does not battle again")
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

local BEATS = {}
local function beat(name, fn) BEATS[#BEATS + 1] = { name = name, fn = fn } end
local HALIA_RING = { 10, 14, 18, 20 }

-- Beat 1: the player's house -----------------------------------------------------------------------

beat("01_bedroom", function()
  mapIs(S.MAP_HOUSE_2F, "woke on 2F")
  local x, y = pos()
  expect(x == 5 and y == 5, string.format("by the kline (at %d,%d)", x, y))
  local name = {}
  for i = 0, 6 do name[#name + 1] = emu:read8(L.sb2() + S.OFF_SB2_NAME + i) end
  local want = IANTHE and { 0xC3, 0xBB, 0xC8, 0xCE, 0xC2, 0xBF, 0xFF } or { 0xCE, 0xC2, 0xBF, 0xC9, 0xFF }
  local same = true
  for i, b in ipairs(want) do if name[i] ~= b then same = false end end
  expect(same and emu:read8(L.sb2() + S.OFF_SB2_GENDER) == (IANTHE and 1 or 0),
         IANTHE and "the player is Ianthe, named IANTHE" or "the player is Theo, named THEO")
  musicIs(S.MUS_ELAIA, "Elaia's theme in the bedroom")
  shot("bedroom")
  -- the stair gate, the room's objects, then the water clock
  expect(not go(8, 2, { trigger = true }), "the stair gate stops the player")
  wait(30); shot("mom_calls_upstairs"); settle()
  x, y = pos()
  expect(y == 3, "stepped back from the stairs")
  talk(6, 5, { shotBefore = "knucklebones" })
  talk(1, 2, { shotBefore = "scrolls" })
  talk(4, 1, { shotBefore = "water_clock", shots = { [1] = "klepsydra_text" } })
  expect(getFlag(S.FLAG_SET_WATER_CLOCK), "the water clock is set")
  go(8, 2)
  L.enter(K.UP, S.MAP_HOUSE_1F, "the stairs down", true)
end)

beat("01_mom", function()
  shot("mom_comes_over")
  settle({ shots = { [3] = "mom_klotheia", [7] = "talaria", [13] = "mom_oracle" } })
  flagsSet({ "FLAG_TALKED_TO_MOM", "FLAG_SYS_B_DASH", "FLAG_RECEIVED_RUNNING_SHOES" }, "Mom gave the Talaria")
  shot("downstairs")
  talk(1, 3, { shotBefore = "hearth" })
  go(5, 8)
  L.enter(K.DOWN, S.MAP_ELAIA, "the front door")
  mapIs(S.MAP_ELAIA, "out of the front door into Elaia")
  musicIs(S.MUS_ELAIA, "Elaia's theme in the village")
  shot("front_door")
end)

beat("01_kydippe", function()
  go(17, 7)
  L.enter(K.UP, S.MAP_KYDIPPE, "Kydippe's door")
  collect(2, 2, "FLAG_GOT_KYDIPPE_ORAN", "ITEM_ORAN_BERRY", "Kydippe's Oran Berries",
          { shotBefore = "kydippe", shots = { [2] = "kydippe_delivered_you" } })
  talk(2, 2, { shotBefore = "kydippe_after" })
  go(4, 7)
  L.enter(K.DOWN, S.MAP_ELAIA, "Kydippe's door out")
end)

-- Beat 2: the gates, then Halia --------------------------------------------------------------------

beat("02_gates", function()
  expect(not go(5, 30, { trigger = true, avoid = HALIA_RING }), "the note on the Akademia door")
  wait(40); shot("akademia_note"); settle()
  expect(not getFlag(S.FLAG_THREAD_READ), "the thread is still unread")
  expect(not go(11, 2, { trigger = true, avoid = HALIA_RING }), "the old shepherd stops the player")
  wait(30); shot("shepherd_gate"); settle()
  local _, y = pos()
  expect(y == 3, "turned back from the road")
end)

beat("02_halia", function()
  expect(not go(14, 18, { trigger = true }), "Halia calls the player into line")
  wait(30); shot("halia_calls")
  settle({ answers = { "no" }, shots = { [3] = "korinna_reading", [8] = "philon_reading", [12] = "your_hand",
                                         [14] = "hm", [15] = "turn_around", [16] = "again",
                                         [17] = "your_own_business", [18] = "liar" } })
  expect(getFlag(S.FLAG_THREAD_READ), "the thread is read")
  shot("after_the_reading")
end)

-- Beat 3: the Akademia -----------------------------------------------------------------------------

beat("03_akademia", function()
  go(5, 30)
  L.enter(K.UP, S.MAP_AKADEMIA, "the Akademia door", true)
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
  go(10, 12)
  L.enter(K.DOWN, S.MAP_ELAIA, "the Akademia's door out")
end)

-- Beat 4: Kleon's battle, Alethea, and the village after ------------------------------------------------

beat("04_kleon", function()
  expect(not getFlag(S.FLAG_HIDE_KLEON_ELAIA), "Kleon waits in the square")
  shot("kleon_waits")
  expect(not go(14, 19, { trigger = true }), "Kleon calls the player at the steps")
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
  -- the village's things to find
  collect(24, 11, "FLAG_ITEM_ELAIA_POTION", "ITEM_POTION", "the Potion by the olive press")
  collect(23, 14, "FLAG_GOT_ELAIA_RELIC_COPPER", "ITEM_RELIC_COPPER", "the Relic Copper in the well",
          { shotBefore = "well" })
  collect(5, 3, "FLAG_HIDDEN_ELAIA_HONEY", "ITEM_HONEY", "the Honey at Mom's beehives")
  -- the villagers after the battle
  talk(14, 15, { shotBefore = "halia_after" })
  talk(14, 5, { shotBefore = "village_sign" })
  talk(26, 12, { shotBefore = "olive_farmer" })
  -- home: Mom's after-battle line and her offer of a meal
  go(5, 9)
  L.enter(K.UP, S.MAP_HOUSE_1F, "the front door")
  expect(L.idle(), "no scene replays at home")
  talk(3, 3, { shotBefore = "mom_after", answers = { "yes" } })
  go(5, 8)
  L.enter(K.DOWN, S.MAP_ELAIA, "the front door")
end)

-- Beat 5: Route 1 and Kronion Hill -------------------------------------------------------------------

beat("05_route1", function()
  go(11, 1)
  shot("north_gate_open")
  L.enter(K.UP, S.MAP_ROUTE1, "Route 1")
  musicIs(S.MUS_ROUTE1, "the Route 1 theme")
  shot("route1_south")
  collect(16, 56, "FLAG_GOT_MOOMOO_MILK", "ITEM_MOOMOO_MILK", "the carter's Moomoo Milk", { shotBefore = "carter" })
  talk(5, 55, { shotBefore = "wall_youth" })
  trainer("TITYROS", 7, 48, S.MUS_BATTLE_TRAINER)
  collect(3, 42, "FLAG_ITEM_ROUTE1_POKE_BALL", "ITEM_POKE_BALL", "the Poke Ball past Tityros")
end)

beat("05_grove", function()
  trainer("PHYLLIS", 25, 37, S.MUS_BATTLE_TRAINER)
  collect(27, 35, "FLAG_ITEM_ROUTE1_MIRACLE_SEED", "ITEM_MIRACLE_SEED", "the Miracle Seed in the grove")
  collect(4, 29, "FLAG_HIDDEN_ROUTE1_ANTIDOTE", "ITEM_ANTIDOTE", "the hidden Antidote")
  collect(7, 24, "FLAG_GOT_ROUTE1_SITRUS", "ITEM_SITRUS_BERRY", "the olive farmer's Sitrus Berry",
          { shotBefore = "olive_farmer" })
  collect(6, 24, "FLAG_HIDDEN_ROUTE1_ORAN", "ITEM_ORAN_BERRY", "the Oran Berry under the big olive")
  trainer("KOMATAS", 18, 25, S.MUS_BATTLE_TRAINER)
end)

beat("05_fork", function()
  collect(15, 20, "FLAG_ITEM_ROUTE1_POTION", "ITEM_POTION", "the Potion at the fork herm")
  talk(14, 20, { shotBefore = "herm_fork" })
  trainer("AGIS", 15, 16, S.MUS_BATTLE_TRAINER)
  collect(15, 14, "FLAG_HIDDEN_ROUTE1_REPEL", "ITEM_REPEL", "the Repel in the wall")
end)

beat("05_flock", function()
  expect(not getFlag(S.FLAG_HIDE_FLOCK), "the flock is on the road")
  talk(10, 15, { shotBefore = "amaryllis_before" })
  talk(11, 14, { shotBefore = "flock_wooloo" })
  trainer("POLYEIDOS", 27, 18, S.MUS_BATTLE_TRAINER)
end)

beat("05_kronion_hill", function()
  go(29, 19)
  L.enter(K.RIGHT, S.MAP_KRONION, "Kronion Hill")
  shot("hill_foot")
  musicIs(S.MUS_ROUTE1, "Kronion Hill keeps the route's theme")
  expect(not go(5, 11, { trigger = true }), "the summit scene starts at the top of the stair")
end)

beat("05_summit", function()
  local _, fought = settle({ every = true, answers = { "no" } })
  expect(#fought == 2, "two grunt battles in the summit scene")
  battleCheck(fought[1], "PETROS", S.MUS_TITAN, "Petros")
  battleCheck(fought[2], "AMATHOS", S.MUS_TITAN, "Amathos")
  flagsSet({ "FLAG_RUINS_CLEARED", "FLAG_FOUND_TABLET", "FLAG_DEXNAV_GET", "FLAG_HIDE_ALETHEA_RUINS",
             "FLAG_HIDE_RUINS_GRUNTS", "FLAG_HIDE_TITAN_TABLET", "FLAG_HIDE_FLOCK" }, "the summit's flags")
  shot("summit_after")
  collect(12, 8, "FLAG_ITEM_KRONION_ESCAPE_ROPE", "ITEM_ESCAPE_ROPE", "the grunts' Escape Rope")
  collect(15, 8, "FLAG_HIDDEN_KRONION_HARD_STONE", "ITEM_HARD_STONE", "the Hard Stone in the rubble")
  collect(11, 5, "FLAG_HIDDEN_KRONION_STARDUST", "ITEM_STARDUST", "the Stardust behind the altar")
  talk(4, 11, { shotBefore = "stele" })
  talk(11, 7, { shotBefore = "pit_after" })
end)

beat("05_road_open", function()
  go(0, 17)
  L.enter(K.LEFT, S.MAP_ROUTE1, "back to Route 1")
  shot("flock_gone")
  talk(10, 15, { shotBefore = "amaryllis_after" })
  go(11, 0)
end)

-- Beat 6: Akti --------------------------------------------------------------------------------------

beat("06_akti_arrival", function()
  L.enter(K.UP, S.MAP_AKTI, "Akti", true)
  shot("arrival")
  settle({ every = true })
  flagsSet({ "FLAG_ARRIVED_AKTI", "FLAG_VISITED_AKTI" }, "arrived in Akti")
  musicIs(S.MUS_AKTI, "Akti's theme")
  shot("after_arrival")
  talk(9, 25, { shotBefore = "diktys_after" })
  talk(14, 24, { shotBefore = "town_sign" })
  collect(7, 24, "FLAG_HIDDEN_AKTI_SUPER_POTION", "ITEM_SUPER_POTION", "the Super Potion behind Diktys's nets")
  talk(6, 23, { shotBefore = "pilgrim" })
end)

beat("06_asclepeion", function()
  go(3, 23)
  L.enter(K.UP, S.MAP_ASCLEPEION, "the Asclepeion")
  musicIs(S.MUS_ASCLEPEION, "the Asclepeion's theme")
  shot("asclepeion")
  log(string.format("note party HP before the heal: %d/%d", L.partyHp(0)))
  talk(7, 2, { from = { { 7, 4 } }, shotBefore = "healer", shots = { [1] = "healer_welcome", [3] = "healer_rest" } })
  local hp, maxHp = L.partyHp(0)
  expect(hp == maxHp and hp > 1, string.format("the healer restored the party (%d/%d)", hp, maxHp))
  local hmap, hx, hy = L.lastHeal()
  expect(hmap == S.MAP_AKTI, string.format("the respawn point is Akti (map %d at %d,%d)", hmap, hx, hy))
  talk(13, 9, { shotBefore = "bandaged_fisher" })
  talk(3, 3, { shotBefore = "old_man" })
  talk(2, 2, { shotBefore = "statue" })
  talk(14, 3, { shotBefore = "pithos_woman" })
  go(10, 5)
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
  go(7, 10)
  L.enter(K.DOWN, S.MAP_AKTI, "out of the Asclepeion")
end)

beat("06_agora", function()
  go(7, 17)
  L.enter(K.UP, S.MAP_AGORA, "the Agora")
  shot("agora")
  log(string.format("note the Agora plays %s (map music id %d)", L.song(), L.mapMusic()))
  -- The shop's BUY/SELL/QUIT menu and its item list are not script prompts, so
  -- this one is played by hand.
  talk(3, 2, { from = { { 3, 4 } }, shotBefore = "demeas", noSettle = true })
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
  talk(9, 3, { shotBefore = "customer_man" })
  go(6, 8)
  L.enter(K.DOWN, S.MAP_AKTI, "out of the Agora")
end)

beat("06_fishers_house", function()
  go(3, 15)
  L.enter(K.UP, S.MAP_FISHERS, "the Fisher's house")
  shot("fishers_house")
  collect(3, 2, "FLAG_GOT_OLD_ROD", "ITEM_OLD_ROD", "Glaukos's Old Rod",
          { shotBefore = "glaukos", answers = { "no" }, every = true })
  talk(6, 6, { shotBefore = "grandson" })
  go(4, 7)
  L.enter(K.DOWN, S.MAP_AKTI, "out of the Fisher's house")
end)

beat("06_harbor_before", function()
  -- The quay's west end (and the Potion among its crates) is reached only past
  -- the tile Kleon stands on until the ending; it is collected in 08_after.
  L.check(L.canReachNextTo(2, 10), "the Potion among the quay crates (2,10) can be reached before the ending")
  talk(5, 10, { shotBefore = "kleon_before", shots = { [2] = "kleon_soup" } })
  talk(7, 9, { shotBefore = "nausikles_before" })
  talk(8, 9, { shotBefore = "rower" })
  collect(16, 11, "FLAG_ITEM_AKTI_PARALYZE_HEAL", "ITEM_PARALYZE_HEAL", "the Paralyze Heal by the fish stall")
  talk(19, 10, { shotBefore = "fishwife" })
  talk(14, 5, { shotBefore = "pier_kid" })
  talk(15, 5, { from = { { 15, 6, "up" } }, shotBefore = "islet_fisher" })
  collect(25, 6, "FLAG_GOT_MYSTIC_WATER", "ITEM_MYSTIC_WATER", "Hydna's Mystic Water", { shotBefore = "hydna" })
  collect(23, 9, "FLAG_HIDDEN_AKTI_HEART_SCALE", "ITEM_HEART_SCALE", "the Heart Scale on the beach")
  collect(24, 7, "FLAG_HIDDEN_AKTI_PEARL", "ITEM_PEARL", "the Pearl on the tide rocks")
  talk(26, 4, { from = { { 26, 5, "up" } }, shotBefore = "grotto_rubble" })
  talk(17, 17, { shotBefore = "temple_old_woman" })
end)

-- Akti's two newest homes (MAP_DESIGN.md §2): Kapra the loose goat and Aigon's
-- Soothe Bell; Doris's grotto lore (her trade waits for the laurel, in 08_after)
beat("06_homes", function()
  talk(2, 15, { from = { { 3, 15, "left" } }, shotBefore = "kapra" })
  flagsSet({ "FLAG_AKTI_GOAT_HOME" }, "Kapra went home")
  go(18, 26)
  L.enter(K.UP, S.MAP_GOATHERDS, "the goatherd's farmhouse")
  shot("goatherds_house")
  collect(2, 3, "FLAG_GOT_SOOTHE_BELL", "ITEM_SOOTHE_BELL", "Aigon's Soothe Bell",
          { from = { { 2, 4, "up" } }, shotBefore = "aigon" })
  go(3, 6)
  L.enter(K.DOWN, S.MAP_AKTI, "out of the goatherd's farmhouse")
  go(26, 15)
  L.enter(K.UP, S.MAP_DIVERS, "the divers' house")
  shot("divers_house")
  talk(2, 3, { from = { { 2, 4, "up" } }, shotBefore = "doris" })
  talk(6, 2, { from = { { 6, 3, "up" } }, shotBefore = "water_clock" })
  go(3, 6)
  L.enter(K.DOWN, S.MAP_AKTI, "out of the divers' house")
end)

-- Beat 7: the Temple of Hestia ----------------------------------------------------------------------

beat("07_temple", function()
  go(19, 17)
  L.enter(K.UP, S.MAP_TEMPLE, "the Temple of Hestia")
  musicIs(S.MUS_TEMPLE, "the Temple's theme")
  shot("temple_entry")
  expect(L.getVar(S.VAR_HEARTH_TRIAL) == 0, "no flame on arrival")
  talk(9, 22, { shotBefore = "euboulos" })
  talk(6, 21, { shotBefore = "hymn", every = true })
  -- up the west side of the hall, out of Lampon's sight (he faces down column 8)
  talk(7, 14, { from = { { 7, 15 } }, shotBefore = "hands_off", avoid = { 8, 16, 8, 22 } })
  expect(L.getVar(S.VAR_HEARTH_TRIAL) == 0, "no flame before Lampon is beaten")
  trainer("LAMPON", 8, 15, S.MUS_BATTLE_TRAINER)
end)

beat("07_hearth_trial", function()
  local function light(x, y, want, what, opts)
    opts = opts or {}
    opts.shotBefore = what
    talk(x, y, opts)
    expect(L.getVar(S.VAR_HEARTH_TRIAL) == want, string.format("%s (trial %d)", what, L.getVar(S.VAR_HEARTH_TRIAL)))
    shot(what .. "_done")
  end
  light(7, 14, 1, "take_flame", { from = { { 7, 15 } } })
  light(13, 4, 2, "door_brazier")
  light(3, 4, 3, "table_brazier")
  light(3, 16, 4, "loom_brazier")
  light(13, 16, 5, "bed_brazier")
  talk(7, 14, { from = { { 7, 15, "up" }, { 9, 15, "up" } }, shotBefore = "return_flame", every = true })
  flagsSet({ "FLAG_TRIAL_DONE", "FLAG_GOT_CHARCOAL" }, "the trial is done and the Charcoal found")
  expect(L.getVar(S.VAR_HEARTH_TRIAL) == 6 and L.itemCount(S.ITEM_CHARCOAL) == 1, "trial var 6, one Charcoal")
  trainer("PYRRHA", 3, 12, S.MUS_BATTLE_TRAINER)
  trainer("AITHRA", 12, 17, S.MUS_BATTLE_TRAINER)
end)

beat("07_ione", function()
  local n0 = #L.battles
  talk(8, 3, { from = { { 8, 5, "up" } }, shotBefore = "ione", every = true })
  local rec
  for i = n0 + 1, #L.battles do if L.battles[i].who == "IONE" then rec = L.battles[i] end end
  battleCheck(rec, "IONE", S.MUS_BATTLE_RIVAL, "Ione")
  flagsSet({ "FLAG_BADGE01_GET", "FLAG_GOT_TM_FACADE" }, "the Hearth Laurel and TM42")
  expect(L.itemCount(S.ITEM_TM42) == 1, "TM42 Facade in the bag")
  local n1 = #L.battles
  talk(8, 3, { from = { { 8, 5, "up" } }, shotBefore = "ione_after" })
  expect(#L.battles == n1, "Ione does not battle again")
  talk(15, 3, { shotBefore = "kanthos" })
  talk(9, 22, { shotBefore = "euboulos_after" })
end)

-- Beat 8: the harbor ---------------------------------------------------------------------------------

beat("08_harbor_part1", function()
  go(8, 23)
  L.enter(K.DOWN, S.MAP_AKTI, "out of the Temple", true)
  shot("doorstep")
  settle({ every = true })
  flagsClear({ "FLAG_HIDE_ALETHEA_AKTI" }, "after part 1, Alethea's hide flag is clear (else leaving and re-entering Akti replays part 1)")
end)

beat("08_harbor_part2", function()
  expect(not go(10, 10, { trigger = true }), "the quay starts the ending")
  settle({ every = true, answers = { "no" } })
  flagsSet({ "FLAG_SLICE_COMPLETE", "FLAG_HIDE_KLEON_AKTI", "FLAG_HIDE_ALETHEA_AKTI" }, "the slice is complete")
  shot("the_end")
end)

beat("08_after", function()
  talk(7, 9, { shotBefore = "nausikles_after" })
  collect(2, 10, "FLAG_ITEM_AKTI_POTION", "ITEM_POTION", "the Potion among the quay crates")
  -- with the laurel, Doris trades her shell bell for the beach's Heart Scale
  go(26, 15)
  L.enter(K.UP, S.MAP_DIVERS, "the divers' house after the laurel")
  collect(2, 3, "FLAG_GOT_SHELL_BELL", "ITEM_SHELL_BELL", "Doris's shell bell, for the Heart Scale",
          { from = { { 2, 4, "up" } }, answers = { "yes" }, shotBefore = "doris_trade" })
  go(3, 6)
  L.enter(K.DOWN, S.MAP_AKTI, "out of the divers' house")
  -- re-entering Akti after the end replays nothing
  go(3, 23)
  L.enter(K.UP, S.MAP_ASCLEPEION, "the Asclepeion again")
  go(7, 10)
  L.enter(K.DOWN, S.MAP_AKTI, "Akti again")
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
  log(string.format("ok the slice played through in %d frames, %d battles", now(), #L.battles))
  if L.bugs > 0 then L.fail(string.format("played to the end, but %d check(s) failed (the BUG lines)", L.bugs)) end
  log("PASS")
end)
