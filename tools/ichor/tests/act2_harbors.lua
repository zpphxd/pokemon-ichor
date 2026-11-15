-- The Gulf crossing check, run by tools/ichor/tests/act2_harbors.sh (read it first).
--
-- Setup touches no ROM data: after Quickstart a test-only event script in spare
-- EWRAM gives a team and the road west's flags so far, and warps onto Kirrha's north
-- road, where Route 9 comes in. Then everything is played with key presses: beat 37A
-- in Kirrha, the crossing (37B), the landing at Aigion (37C), and the ferry back.

local L = dofile("tools/ichor/tests/slice_lib.lua")
L.init{ tag = "HARBORS", out = "build/test_harbors/", symbols = "build/test_harbors/symbols.lua" }
local S, K = L.S, L.K
local emu = L.emu
local log, expect, wait, waitUntil, shot = L.log, L.expect, L.wait, L.waitUntil, L.shot

local function bankFlag(f)
  local o = f - S.ICHOR_FLAGS_START
  local base = emu:read32(S.gSaveBlock3Ptr) + S.OFF_SB3_ICHOR + S.OFF_ICHOR_FLAGS
  return (emu:read8(base + (o >> 3)) >> (o & 7)) & 1 == 1
end
-- slice_lib's walker hides people by their hide flags; the crossing's are in the bank.
local getFlag1 = L.getFlag
function L.getFlag(f)
  if f >= S.ICHOR_FLAGS_START and f <= S.ICHOR_FLAGS_END then return bankFlag(f) end
  return getFlag1(f)
end
local flag = L.getFlag

-- An ON_FRAME script that sets flags and warps to (map, x, y).
local function warpIn(map, x, y, flags, extra)
  local s = { S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 } }
  for _, b in ipairs(extra or {}) do s[#s + 1] = b end
  for _, f in ipairs(flags or {}) do
    s[#s + 1] = S.SCR_OP_SETFLAG
    s[#s + 1] = { f, 2 }
  end
  for _, b in ipairs({ S.SCR_OP_WARP, map >> 8, map & 0xFF, S.WARP_ID_NONE & 0xFF, { x, 2 }, { y, 2 },
                       S.SCR_OP_WAITSTATE, S.SCR_OP_END }) do
    s[#s + 1] = b
  end
  L.runRamScript(s)
  waitUntil(function() return L.mapId() == map and L.idle() end, 4000, "the warp")
  wait(30)
end

local function onMap(map, what)
  waitUntil(function() return L.mapId() == map and L.idle() end, 4000, what)
  wait(20)
end

local function main()
  -- Boot, skip the intro, Quickstart (the smoke test's timing).
  waitUntil(function() return L.now() >= 500 end, 600, "frame 500")
  L.tap(K.START)
  waitUntil(function() return L.now() >= 1020 end, 600, "frame 1020")
  L.tap(K.SELECT)
  waitUntil(L.idle, 4000, "the new game")
  wait(30)
  -- Fast text, Set battle style, no battle animations.
  local opt = L.sb2() + S.OFF_SB2_OPTIONS
  emu:write16(opt, (emu:read16(opt) & ~0x7) | 2 | (1 << 9) | (1 << 10))

  -- ---------------------------------------------------------------- beat 37A
  L.setBeat("kirrha", false)
  local team = { S.SCR_OP_CALLNATIVE, { S.ScrCmd_createmon | 1, 4 }, 0, S.PARTY_SIZE,
                 { S.SPECIES_TEST, 2 }, { 100, 2 }, { (1 << 17) | (1 << 18) | (1 << 19) | (1 << 20), 4 },
                 { S.MOVE_TEST, 2 }, { S.MOVE_NONE, 2 }, { S.MOVE_NONE, 2 }, { S.MOVE_NONE, 2 } }
  warpIn(S.MAP_KIRRHA, 27, 0, { S.FLAG_SYS_POKEMON_GET, S.FLAG_BADGE04_GET, S.FLAG_ACT2_BEGUN,
                                S.FLAG_GIRDLE,
                                -- the two ferry trainers stand beaten: this run is about the
                                -- crossing's scenes, and a battle's length is the battle engine's
                                -- business (their talk scripts still run, after-battle lines and all)
                                S.TRAINER_FLAGS_START + S.TRAINER_KEPHISIOS,
                                S.TRAINER_FLAGS_START + S.TRAINER_LAMPRIAS }, team)
  expect(flag(S.FLAG_VISITED_KIRRHA), "Kirrha is a fly target from the first step")
  expect(not flag(S.FLAG_ARRIVED_KIRRHA), "not yet arrived")
  shot("kirrha_north_road")

  local fired = not L.goTrigger(L.triggers("Kirrha_EventScript_Arrival"))
  expect(fired, "Alethea's lines start on the road above the harbor")
  L.settle({ shots = { [1] = "alethea_all_these_people", [3] = "alethea_patched_sail" } })
  expect(flag(S.FLAG_ARRIVED_KIRRHA), "arrived in Kirrha")
  expect(L.npc("Kirrha_EventScript_Alethea").present, "Alethea has gone down to the quay")
  shot("after_the_arrival")

  -- The pilgrims' gate: the guards, and Alethea up the road beside you.
  L.setBeat("gate", false)
  L.go(5, 11); shot("the_sacred_road")
  L.talk(L.npc("Kirrha_EventScript_TempleGuard"), { shots = { [1] = "guards_shut", [3] = "alethea_when",
                                                              [8] = "alethea_soon_what" } })
  expect(flag(S.FLAG_GATE_SEEN), "the guards said soon")
  L.talk(L.npc("Kirrha_EventScript_TempleGuard", 2), { shots = { [1] = "guards_again" } })
  L.talk(L.sign("Kirrha_EventScript_GateSign"), { shots = { [1] = "gate_sign" } })
  L.talk(L.hidden(S.FLAG_HIDDEN_OBOL), { shots = { [1] = "obol_at_the_gate" } })
  expect(flag(S.FLAG_HIDDEN_OBOL), "the pilgrim's obol at the gate's foot")

  -- The shore path under Apollo's plain: a dead end that pays.
  L.setBeat("plain", false)
  L.talk(L.ball(S.FLAG_ITEM_HYPER_POTION), { shots = { [1] = "shore_path_potion" } })
  expect(flag(S.FLAG_ITEM_HYPER_POTION), "the Hyper Potion where the shore path stops")
  L.talk(L.npc("Kirrha_EventScript_FenceWatcher"), { shots = { [1] = "fence_watcher" } })
  L.talk(L.sign("Kirrha_EventScript_FenceSign"), { shots = { [1] = "fence_sign" } })
  L.talk(L.sign("Kirrha_EventScript_DigFence"))
  L.talk(L.npc("Kirrha_EventScript_Beggar"), { answers = { "yes" }, shots = { [2] = "beggar_lucky_stone" } })
  expect(flag(S.FLAG_DECOY_KIRRHA), "paid the beggar: a decoy")

  -- The quay.
  L.setBeat("quay", false)
  L.go(17, 17); shot("the_street")
  L.talk(L.hidden(S.FLAG_HIDDEN_KIRRHA_PEARL), { shots = { [1] = "pearl_in_the_drain" } })
  expect(flag(S.FLAG_HIDDEN_KIRRHA_PEARL), "the Pearl in the fish market's drain")
  L.talk(L.npc("Kirrha_EventScript_Fishwife"), { shots = { [1] = "fishwife" } })
  L.talk(L.npc("Kirrha_EventScript_Kronist"), { answers = { "yes" },
                                               shots = { [1] = "kronist_bread", [3] = "kronist_noon",
                                                         [5] = "alethea_kinder" } })
  expect(flag(S.FLAG_KRONIST_READ), "the Kronist tried a reading")
  expect(flag(S.FLAG_KRONIST_ALETHEA), "Alethea had her say about kindness")
  L.talk(L.npc("Kirrha_EventScript_Pilgrim1"), { shots = { [1] = "pilgrim_kythera" } })
  L.talk(L.npc("Kirrha_EventScript_Pilgrim2"))
  L.talk(L.npc("Kirrha_EventScript_Pilgrim3"))
  L.talk(L.npc("Kirrha_EventScript_Alethea"), { shots = { [1] = "alethea_on_the_quay" } })
  L.talk(L.hidden(S.FLAG_HIDDEN_KIRRHA_SCALE), { shots = { [1] = "scale_at_the_quay_end" } })
  expect(flag(S.FLAG_HIDDEN_KIRRHA_SCALE), "the Heart Scale at the quay's end")
  L.talk(L.sign("Kirrha_EventScript_FerrySign"), { shots = { [1] = "ferry_sign" } })
  L.talk(L.ball(S.FLAG_ITEM_NET_BALL), { shots = { [1] = "beach_net_ball" } })
  expect(flag(S.FLAG_ITEM_NET_BALL), "the Net Ball at the beach's end")
  L.talk(L.sign("Kirrha_EventScript_TownSign"), { shots = { [1] = "town_sign" } })

  -- ---------------------------------------------------------------- beat 37B
  L.setBeat("crossing", false)
  L.talk(L.npc("Kirrha_EventScript_Panopeus"), { answers = { "yes" }, shots = { [1] = "panopeus_aigion" } })
  onMap(S.MAP_GULF_FERRY_DECK, "the ferry's deck")
  expect(flag(S.FLAG_BOARDED), "aboard the Gulf ferry")
  expect(flag(S.FLAG_HIDE_ALETHEA_KIRRHA), "Alethea left Kirrha's quay with you")
  expect(flag(S.FLAG_NO_RELICS), "no relics on a ferry under way")
  expect(L.playing(S.MUS_ICHOR_TRIREME), "the crossing plays the trireme's song")
  shot("on_deck")
  L.talk(L.npc("GulfFerry_Deck_EventScript_Alethea"), { shots = { [1] = "alethea_kallisto", [5] = "alethea_looked_at",
                                                                  [6] = "alethea_kind_to_him" } })
  expect(flag(S.FLAG_FERRY_ALETHEA), "Alethea at the stern")
  L.talk(L.npc("GulfFerry_Deck_EventScript_Goat"), { shots = { [2] = "goat_cloak" } })
  L.talk(L.sign("GulfFerry_Deck_EventScript_Rail"), { shots = { [1] = "rail_wine_dark" } })
  L.talk(L.hidden(S.FLAG_HIDDEN_FERRY_SCALE), { shots = { [1] = "goat_sat_on_it" } })
  expect(flag(S.FLAG_HIDDEN_FERRY_SCALE), "the Heart Scale in the goat pen")
  expect(L.npc("GulfFerry_Deck_EventScript_Kephisios").present, "Kephisios fishes at the rail")
  L.talk(L.npc("GulfFerry_Deck_EventScript_Kephisios"), { shots = { [1] = "kephisios_after" } })
  expect(L.npc("GulfFerry_Deck_EventScript_Lamprias").present, "Lamprias sits at the bow")
  L.talk(L.npc("GulfFerry_Deck_EventScript_Lamprias"), { shots = { [1] = "lamprias_after" } })
  expect(not L.inBattle(), "the beaten trainers only talk")
  L.talk(L.ball(S.FLAG_ITEM_FERRY_POTION), { shots = { [1] = "amphorae_potion" } })
  expect(flag(S.FLAG_ITEM_FERRY_POTION), "the Super Potion among the amphorae")

  -- ---------------------------------------------------------------- beat 37C
  L.setBeat("aigion", false)
  L.talk(L.npc("GulfFerry_Deck_EventScript_Panopeus"), { answers = { "yes" },
                                                         shots = { [1] = "panopeus_blow_on_it" } })
  onMap(S.MAP_AIGION, "Aigion's quay")
  L.settle({ shots = { [1] = "alethea_achaea", [4] = "alethea_come_on" } })
  expect(flag(S.FLAG_GULF_CROSSED) and flag(S.FLAG_VISITED_AIGION), "crossed the gulf; Aigion's a fly target")
  expect(flag(S.FLAG_AIGION_ARRIVAL), "Alethea's landing lines played")
  expect(not flag(S.FLAG_HIDE_ALETHEA_AIGION), "Alethea waits at the south road")
  expect(L.npc("Aigion_EventScript_Panopeus").present, "Panopeus is on Aigion's quay")
  shot("aigion_quay")
  L.talk(L.npc("Aigion_EventScript_Fisher"), { shots = { [2] = "fisher_helike" } })
  L.talk(L.hidden(S.FLAG_HIDDEN_AIGION_PEARL), { shots = { [1] = "pearl_over_helike" } })
  expect(flag(S.FLAG_HIDDEN_AIGION_PEARL), "the Pearl where the drowned roofs show")
  L.talk(L.sign("Aigion_EventScript_QuaySign"), { shots = { [1] = "aigion_sign" } })
  L.talk(L.ball(S.FLAG_ITEM_AIGION_REPEL), { shots = { [1] = "quay_end_super_repel" } })
  expect(flag(S.FLAG_ITEM_AIGION_REPEL), "the Super Repel at the quay's east end")
  L.talk(L.npc("Aigion_EventScript_Child"), { shots = { [1] = "child_lakonian" } })
  L.go(13, 11); shot("the_grove")
  L.talk(L.npc("Aigion_EventScript_GroveKeeper"), { shots = { [1] = "grove_keeper", [4] = "grove_heal" } })
  L.talk(L.hidden(S.FLAG_HIDDEN_AIGION_HONEY), { shots = { [1] = "honey_in_the_plane" } })
  expect(flag(S.FLAG_HIDDEN_AIGION_HONEY), "the Honey in the hollow plane")
  L.talk(L.sign("Aigion_EventScript_Altar"), { answers = { "yes" }, shots = { [1] = "altar_of_zeus", [2] = "altar_rite" } })
  L.talk(L.npc("Aigion_EventScript_AletheaRoad"), { shots = { [1] = "alethea_south_road" } })
  L.talk(L.sign("Aigion_EventScript_SouthSign"), { shots = { [1] = "south_sign" } })

  -- ------------------------------------------------------------ and back again
  L.setBeat("ferry_back", false)
  L.talk(L.npc("Aigion_EventScript_Panopeus"), { answers = { "yes" } })
  onMap(S.MAP_GULF_FERRY_DECK, "the deck, going back")
  expect(flag(S.FLAG_FERRY_TO_KIRRHA), "this run lands at Kirrha")
  expect(not L.npc("GulfFerry_Deck_EventScript_Alethea").present, "Alethea's gone on ahead: not aboard")
  shot("deck_going_back")
  L.talk(L.npc("GulfFerry_Deck_EventScript_Panopeus"), { answers = { "yes" } })
  onMap(S.MAP_KIRRHA, "Kirrha's quay")
  expect(not flag(S.FLAG_FERRY_TO_KIRRHA), "the return run is over")
  expect(not L.npc("Kirrha_EventScript_Alethea").present, "no Alethea on Kirrha's quay any more")
  shot("back_in_kirrha")
  log("ok the crossing plays through, both ways")
end

L.start(main)
