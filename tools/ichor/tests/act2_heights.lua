-- The Arkadian climb check, run by tools/ichor/tests/act2_heights.sh (read it first).
--
-- Plays beats 38-40 as a player would, with key presses on slice_lib's walker
-- (paths come from the live map, people and signs are found by the script they
-- run), and checks the story's state after each: the drums' flags and the tiles
-- they leave behind, the scenes' flags and who has gone, the great herms, the
-- gifts, the trainers beaten and the shrine cleansed.
--
-- Prints "HEIGHTS ok ..." per check, "HEIGHTS shot ..." per screenshot, and ends
-- with "HEIGHTS done"; any failure prints "HEIGHTS FAIL: ..." first.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K = L.S, L.K
local log, expect, wait, shot, settle, tap = L.log, L.expect, L.wait, L.shot, L.settle, L.tap
for k, v in pairs(dofile(L.OUT .. "heights_scripts.lua")) do S.SCRIPTS[k] = v end
local R11, SF, R12, MAIA = "Route11_KrathisGorge_EventScript_", "StyxFalls_EventScript_",
                           "Route12_CypressRoad_EventScript_", "Route12_CaveOfMaia_EventScript_"

local function tile(x, y) return L.grid().tile(x, y) end
local function mt(x, y) return (tile(x, y)) end
local function solid(x, y) local _, s = tile(x, y) return s end
local function at(x, y) local px, py = L.pos() return px == x and py == y end

-- The nth Strength drum on this map (template order), where it is now.
local function drum(n) return L.npc("EventScript_StrengthBoulder", n) end

-- Push a drum: stand at `from`, face it, brace with the Girdle if this map hasn't
-- seen it yet, and walk into it. The button's scene plays out.
local function push(from, key, name)
  L.go(from[1], from[2])
  L.face(key)
  if not L.getFlag(S.FLAG_STRENGTH) then
    tap(K.A); wait(10)
    settle({ answers = { "yes" }, shots = { [1] = name .. "_brace" } })
    expect(L.getFlag(S.FLAG_STRENGTH), name .. ": the Girdle braces")
  end
  L.step(key)
  wait(30)
  settle({ shots = { [1] = name, [3] = name .. "_3" } })
end

-- A person found afresh each time the walker asks where they are: a trainer who
-- spots the player walks over, and the talk goes to where they stand now.
local function live(script)
  return setmetatable({ what = script }, { __index = function(_, k) return L.npc(script)[k] end })
end

-- Talk to a trainer (walking up to them if they don't see the player first).
local function battle(script, trainer, name)
  L.talk(live(script), { shots = { [1] = name } })
  expect(L.defeated(trainer), "beat " .. name)
end

L.start(function()
  L.quickstart()
  L.runHeader("HeightsTest_SetupHeader", { noSettle = true })
  L.waitUntil(function() return L.mapId() == S.MAP_ROUTE11 and L.idle() end, 4000, "Route 11")
  wait(30)

  -- --- Beat 38: the drums -------------------------------------------------------------
  L.setBeat("r11_drums")
  expect(at(19, 3), "arrived at the top of Route 11")
  shot("r11_top")
  L.talk(L.sign(R11 .. "SignNorth"), { shots = { [1] = "r11_sign_north" } })
  expect(L.goTrigger(L.triggers(R11 .. "DrumsScene")) == false, "the muleteer stops the player above the drums")
  settle({ shots = { [1] = "r11_road_shut", [3] = "r11_alethea_belt" } })
  expect(L.getFlag(S.FLAG_DRUMS_SEEN), "the road is shut: FLAG_ICHOR_ROUTE11_DRUMS_SEEN")
  L.talk(L.sign(R11 .. "SignDrums"), { shots = { [1] = "r11_sign_closed" } })
  L.talk(L.npc(R11 .. "Mule"), { shots = { [1] = "r11_mule" } })
  L.talk(L.hidden(S.FLAG_HIDDEN_REVIVE))
  expect(L.getFlag(S.FLAG_HIDDEN_REVIVE) and L.itemCount(S.ITEM_REVIVE) >= 1, "the Revive in the tumbled stone")

  -- Drum 1 rolls east over the edge; the lip shuts behind it.
  push({ 19, 15 }, K.RIGHT, "r11_drum1")
  expect(L.getFlag(S.FLAG_DRUM_1) and not drum(1).present, "drum 1 went over the edge")
  expect(mt(21, 15) == S.MT_LIP and solid(21, 15), "the lip is shut once drum 1 has gone over")
  -- Drum 2 drops south into the gap and becomes road; the road is open.
  push({ 20, 15 }, K.DOWN, "r11_drum2")
  expect(L.getFlag(S.FLAG_DRUM_2) and not drum(2).present, "drum 2 dropped into the gap")
  expect(mt(20, 17) == S.MT_DRUM_WEDGED, "the gap shows the wedged drum")
  expect(L.getFlag(S.FLAG_DRUMS_DONE), "the road is open: FLAG_ICHOR_HIDE_ROUTE11_DRUMS")
  expect(L.itemCount(S.ITEM_HARD_STONE) == 1, "the muleteer's Hard Stone")
  expect(L.getFlag(S.FLAG_MULETEER_GONE) and L.getFlag(S.FLAG_ALETHEA_R11)
         and not L.npc(R11 .. "Muleteer").present and not L.npc(R11 .. "Alethea").present,
         "the muleteer and Alethea went on up the gorge")
  shot("r11_road_open")
  -- Over the wedged drum, and drum 3 rolls west until the cliff stops it.
  for _ = 1, 3 do L.step(K.DOWN) end
  expect(at(20, 18), "walked over the wedged drum")
  push({ 20, 18 }, K.LEFT, "r11_drum3")
  expect(L.getFlag(S.FLAG_DRUM_3) and not drum(3).present, "drum 3 rolled away")
  expect(mt(16, 18) == S.MT_DRUM_REST and solid(16, 18), "drum 3 rests against the cliff")
  shot("r11_drums_done")

  -- The fourth drum, across the shepherd's cave above.
  push({ 7, 11 }, K.LEFT, "r11_cave_drum")
  expect(L.getFlag(S.FLAG_CAVE_DRUM) and mt(2, 11) == S.MT_DRUM_REST, "the cave drum rolled aside")
  shot("r11_cave_open")

  -- --- The gorge ------------------------------------------------------------------------
  L.setBeat("r11_gorge")
  battle(R11 .. "Apheidas", S.TRAINER_APHEIDAS, "r11_apheidas")
  battle(R11 .. "Auge", S.TRAINER_AUGE, "r11_auge")
  battle(R11 .. "Dryops", S.TRAINER_DRYOPS, "r11_dryops")
  L.talk(L.npc(R11 .. "Traveler"), { answers = { "yes" }, shots = { [1] = "r11_traveler" } })
  expect(L.getFlag(S.FLAG_DECOY) and L.itemCount(S.ITEM_FRESH_WATER) == 0 and L.itemCount(S.ITEM_SITRUS) == 1,
         "the thirsty traveler: Fresh Water for a Sitrus Berry")
  L.talk(L.sign(R11 .. "GreatHerm"), { answers = { "yes" }, shots = { [1] = "r11_herm", [2] = "r11_herm_oil" } })
  expect(L.getFlag(S.FLAG_HERM_11) and L.itemCount(S.ITEM_OLIVE_OIL) == 1, "anointed Route 11's great herm")
  L.talk(L.npc(R11 .. "Pelasgos"), { shots = { [1] = "r11_pelasgos", [3] = "r11_pelasgos_acorns" } })
  L.talk(L.sign(R11 .. "Spring"))
  L.talk(L.sign(R11 .. "BrokenBridge"), { shots = { [1] = "r11_bridge" } })
  battle(R11 .. "Azan", S.TRAINER_AZAN, "r11_azan")
  L.talk(L.sign(R11 .. "SignSouth"), { shots = { [1] = "r11_sign_south" } })
  L.leaveEdge("down", S.MAP_STYX)
  expect(L.mapId() == S.MAP_STYX, "down the gorge into Styx Falls")

  -- --- Beat 39: Styx Falls ----------------------------------------------------------------
  L.setBeat("styx")
  shot("styx_arrival")
  expect(L.getFlag(S.FLAG_VISITED_STYX), "FLAG_ICHOR_VISITED_STYX_FALLS")
  expect(L.goTrigger(L.triggers(SF .. "StyxScene")) == false, "the cleft's foot starts the scene")
  settle({ shots = { [1] = "styx_never_a_sound", [5] = "styx_for_the_record", [8] = "styx_the_inn" } })
  expect(L.getFlag(S.FLAG_SAW_STYX) and not L.npc(SF .. "Alethea").present,
         "Alethea showed the Styx and went to the inn: FLAG_ICHOR_SAW_STYX")
  L.talk(L.sign(SF .. "OathStone"), { answers = { "yes" }, shots = { [1] = "styx_oath", [2] = "styx_oath_sworn" } })
  L.talk(L.sign(SF .. "Pool"), { shots = { [1] = "styx_pool" } })
  L.talk(L.hidden(S.FLAG_HIDDEN_OBOL))
  expect(L.itemCount(S.ITEM_OBOL) >= 1, "the obol on the pool's lip")
  L.talk(L.npc(SF .. "Muleteer"), { shots = { [1] = "styx_muleteer" } })
  expect(L.npc(SF .. "Muleteer").present, "the muleteer is down at the pool, filling hoof-cups")
  L.talk(L.npc(SF .. "OldMan"), { shots = { [3] = "styx_old_man" } })
  L.talk(L.ball(S.FLAG_BALL_SPELL_TAG))
  expect(L.itemCount(S.ITEM_SPELL_TAG) == 1, "the Spell Tag among the hoof-cups")
  L.talk(L.sign(SF .. "SignSouth"), { shots = { [1] = "styx_sign_south" } })
  L.leaveEdge("right", S.MAP_ROUTE12)
  expect(L.mapId() == S.MAP_ROUTE12, "east out of Styx Falls onto Route 12")

  -- --- Route 12 and beat 40 ------------------------------------------------------------------
  L.setBeat("r12")
  shot("r12_arrival")
  L.talk(L.sign(R12 .. "SignWest"), { shots = { [1] = "r12_sign_west" } })
  battle(R12 .. "Phegeus", S.TRAINER_PHEGEUS, "r12_phegeus")
  L.talk(L.sign(R12 .. "GreatHerm"), { answers = { "yes" }, shots = { [2] = "r12_herm" } })
  expect(L.getFlag(S.FLAG_HERM_12) and L.itemCount(S.ITEM_OLIVE_OIL) == 0, "anointed Route 12's great herm")

  L.setBeat("maia")
  L.useWarp(S.MAP_MAIA)
  expect(L.mapId() == S.MAP_MAIA, "into the Cave of Maia")
  shot("maia_arrival")
  expect(L.goTrigger(L.triggers(MAIA .. "AletheaScene")) == false, "walking in starts the lyre's story")
  settle({ shots = { [1] = "maia_born_here", [3] = "maia_first_lyre", [6] = "maia_priestess_trade", [9] = "maia_kleon" } })
  expect(L.getFlag(S.FLAG_ALETHEA_MAIA) and not L.npc(MAIA .. "Alethea").present,
         "Alethea went on to Arkadia: FLAG_ICHOR_HIDE_ALETHEA_MAIA")
  L.talk(L.npc(MAIA .. "Priestess"), { shots = { [1] = "maia_singer", [5] = "maia_throat_spray" } })
  expect(L.getFlag(S.FLAG_MAIA_SINGER) and L.itemCount(S.ITEM_THROAT_SPRAY) == 1,
         "the priestess played the tune for the Chelyra: the Throat Spray")
  L.talk(L.npc(MAIA .. "Priestess"), { shots = { [2] = "maia_rest" } })
  battle(MAIA .. "Euandros", S.TRAINER_EUANDROS, "maia_euandros")
  L.talk(L.sign(MAIA .. "Cradle"), { shots = { [1] = "maia_cradle" } })
  L.talk(L.sign(MAIA .. "Lyre"))
  L.talk(L.sign(MAIA .. "HermFace"))
  L.talk(L.hidden(S.FLAG_HIDDEN_PP_UP))
  expect(L.itemCount(S.ITEM_PP_UP) >= 1, "the PP Up in the cradle niche")
  L.talk(L.ball(S.FLAG_BALL_LEPPA))
  L.talk(L.ball(S.FLAG_BALL_MAX_REPEL))
  expect(L.itemCount(S.ITEM_LEPPA) == 1 and L.itemCount(S.ITEM_MAX_REPEL) == 1, "the pilgrims' leavings at the cave's ends")
  L.sign("EventScript_IchorAltar_Hermes")    -- fails the run if the cave has no altar of Hermes
  L.go(15, 8)
  shot("maia_altar")
  L.useWarp(S.MAP_ROUTE12)
  expect(L.mapId() == S.MAP_ROUTE12, "back out onto the Cypress Road")

  -- The hawk spur: the drum drops into the gap and makes a step; the nest's page.
  L.setBeat("r12_hawk")
  battle(R12 .. "Laodike", S.TRAINER_LAODIKE, "r12_laodike")
  L.talk(L.hidden(S.FLAG_HIDDEN_FEATHER))
  push({ 34, 8 }, K.UP, "r12_hawk_drum")
  expect(L.getFlag(S.FLAG_HAWK_DRUM) and mt(34, 6) == S.MT_HAWK_STEP, "the hawk drum wedged in its gap: a step")
  L.talk(L.sign(R12 .. "HawkNest"), { shots = { [2] = "r12_page_iv", [4] = "r12_page_tray" } })
  expect(L.getFlag(S.FLAG_PAGE_4), "Daedalus's page IV, from the hawk's nest")
  expect(L.defeated(S.TRAINER_HEKAERGE), "Hekaerge stopped the player on the spur")
  shot("r12_spur_top")

  -- Basanos and the shrine of Artemis.
  L.setBeat("r12_shrine")
  battle(R12 .. "Aipytos", S.TRAINER_AIPYTOS, "r12_aipytos")
  battle(R12 .. "Telphousa", S.TRAINER_TELPHOUSA, "r12_telphousa")
  expect(mt(46, 22) == S.MT_SHRINE_BAD_TOP, "the shrine's moon is scratched")
  L.talk(L.sign(R12 .. "Shrine"), { shots = { [1] = "r12_shrine_scratched" } })
  battle(R12 .. "Basanos", S.TRAINER_BASANOS, "r12_basanos")
  L.talk(L.sign(R12 .. "Shrine"), { answers = { "yes" }, shots = { [1] = "r12_shrine_pray", [2] = "r12_shrine_cleansed" } })
  expect(L.getFlag(S.FLAG_ALTAR_12), "the shrine of Artemis cleansed (altar 10)")
  expect(mt(46, 22) == S.MT_SHRINE_TOP, "the moon is mended at once")
  shot("r12_shrine_mended")
  L.talk(L.sign(R12 .. "SignSouth"), { shots = { [1] = "r12_sign_south" } })
  L.go(29, 35)
  shot("r12_gate")
  -- Arkadia's north road (22-25, the arkadia agent's map) meets this road (28-31)
  -- across the seam. On a branch where MAP_ARKADIA is still the placeholder the
  -- cells across are not road: say so and stop at the gate.
  local open = 0
  for x = 28, 31 do
    local mid, blocked, b, e = L.grid().tile(x, 36, true)
    if mid and not blocked and e == 3 then open = open + 1 end
  end
  if open > 0 then
    L.leaveEdge("down", S.MAP_ARKADIA)
    expect(L.mapId() == S.MAP_ARKADIA, "down the Cypress Road into Arkadia")
    shot("arkadia_arrival")
  else
    L.note("MAP_ARKADIA here is the placeholder: its north road isn't across the seam, so the walk stops at the gate")
  end

  -- --- Back at the drums: they stay where they went ----------------------------------------------
  L.setBeat("r11_again")
  L.runHeader("HeightsTest_ReturnHeader", { noSettle = true })
  L.waitUntil(function() return L.mapId() == S.MAP_ROUTE11 and L.idle() end, 4000, "Route 11 again")
  wait(30)
  expect(mt(20, 17) == S.MT_DRUM_WEDGED and mt(16, 18) == S.MT_DRUM_REST and mt(21, 15) == S.MT_LIP
         and solid(21, 15), "re-entered: the drums stay moved")
  expect(not drum(1).present and not drum(2).present and not drum(3).present, "re-entered: no drums back on the road")
  L.go(20, 16)
  expect(at(20, 16), "walked back up over the wedged drum")
  expect(not L.npc(R11 .. "Muleteer").present and not L.npc(R11 .. "Alethea").present, "re-entered: the muleteer and Alethea are gone")
  shot("r11_again")
  L.talk(L.sign(R11 .. "SignDrums"), { shots = { [1] = "r11_sign_scratched" } })
  log("ok " .. L.bugs .. " bugs")
end)
