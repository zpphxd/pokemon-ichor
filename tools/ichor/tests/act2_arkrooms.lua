-- The interiors of Styx Falls and Arkadia, run by tools/ichor/tests/act2_arkrooms.sh (read
-- it first).
--
-- Setup touches no ROM data: after Quickstart a test-only event script in spare EWRAM
-- gives a team (a Gelasable first, for Hippothoos's trade) and warps into each room. Then
-- everything is played with key presses. The outdoor maps (Styx Falls, Arkadia) belong
-- to other agents, so the test arrives in each room by warp and never walks out.

local L = dofile("tools/ichor/tests/slice_lib.lua")
L.init{ tag = "ARKROOMS", out = "build/test_arkrooms/", symbols = "build/test_arkrooms/symbols.lua" }
local S, K = L.S, L.K
local emu = L.emu
local log, expect, wait, waitUntil, shot = L.log, L.expect, L.wait, L.waitUntil, L.shot

local function bankFlag(f)
  local o = f - S.ICHOR_FLAGS_START
  local base = emu:read32(S.gSaveBlock3Ptr) + S.OFF_SB3_ICHOR + S.OFF_ICHOR_FLAGS
  return (emu:read8(base + (o >> 3)) >> (o & 7)) & 1 == 1
end
-- slice_lib's walker hides people by their hide flags; the rooms' are in the Ichor bank.
local getFlag1 = L.getFlag
function L.getFlag(f)
  if f >= S.ICHOR_FLAGS_START and f <= S.ICHOR_FLAGS_END then return bankFlag(f) end
  return getFlag1(f)
end

local function partyCount() return emu:read8(S.gPartiesCount) end

-- An ON_FRAME script that sets and clears flags, sets vars, runs `extra`, and warps into
-- `map` at (x, y). With opts.scene, the room's own arrival script is played out.
local function into(map, x, y, opts)
  opts = opts or {}
  local s = { S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 } }
  for _, b in ipairs(opts.extra or {}) do s[#s + 1] = b end
  for _, f in ipairs(opts.flags or {}) do
    s[#s + 1] = S.SCR_OP_SETFLAG
    s[#s + 1] = { f, 2 }
  end
  for _, f in ipairs(opts.clear or {}) do
    s[#s + 1] = S.SCR_OP_CLEARFLAG
    s[#s + 1] = { f, 2 }
  end
  for _, kv in ipairs(opts.vars or {}) do
    s[#s + 1] = S.SCR_OP_SETVAR
    s[#s + 1] = { kv[1], 2 }
    s[#s + 1] = { kv[2], 2 }
  end
  for _, b in ipairs({ S.SCR_OP_WARP, map >> 8, map & 0xFF, S.WARP_ID_NONE & 0xFF, { x, 2 }, { y, 2 },
                       S.SCR_OP_WAITSTATE, S.SCR_OP_END }) do
    s[#s + 1] = b
  end
  -- the ON_FRAME header runs while VAR_TEMP_0 is 0: zero it (an earlier one-off left it 1)
  emu:write16(L.sb1() + S.OFF_SB1_VARS + (S.VAR_TEMP_0 - S.VARS_START) * 2, 0)
  L.runRamScript(s)
  -- wait for the warp to start (the map may be the one we're on), then to land
  waitUntil(function() return not L.inOverworld() end, 600, string.format("the warp to map %d", map))
  waitUntil(function() return L.mapId() == map and L.inOverworld() end, 4000, string.format("map %d", map))
  if opts.scene then
    wait(40)
    L.settle(opts.scene)
  else
    waitUntil(L.idle, 4000, string.format("map %d to settle", map))
  end
  wait(20)
end

-- Is species in the party? (the game's own checkspecies, run as a one-off script; its
-- ON_FRAME header runs while VAR_TEMP_0 is 0, so zero it first)
local function hasSpecies(species)
  emu:write16(L.sb1() + S.OFF_SB1_VARS + (S.VAR_TEMP_0 - S.VARS_START) * 2, 0)
  L.runRamScript({ S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 },
                   S.SCR_OP_CALLNATIVE, { S.Scrcmd_checkspecies | 1, 4 }, { species, 2 }, S.SCR_OP_END })
  wait(10)
  return emu:read16(S.gSpecialVar_Result) == 1
end

-- Talk across a counter: stand at (x, y), face up, press A, play it out.
local function acrossCounter(x, y, opts)
  L.go(x, y)
  L.face(K.UP)
  L.tap(K.A)
  wait(10)
  return L.settle(opts)
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

  -- A Gelasable first (slot 0, so the trade's party menu opens on it), then a strong
  -- test Pokémon.
  local moves = (1 << 17) | (1 << 18) | (1 << 19) | (1 << 20)
  local team = { S.SCR_OP_CALLNATIVE, { S.ScrCmd_createmon | 1, 4 }, 0, S.PARTY_SIZE,
                 { S.SPECIES_GELASABLE, 2 }, { 30, 2 }, { 0, 4 },
                 S.SCR_OP_CALLNATIVE, { S.ScrCmd_createmon | 1, 4 }, 0, S.PARTY_SIZE,
                 { S.SPECIES_TEST, 2 }, { 60, 2 }, { moves, 4 },
                 { S.MOVE_TEST, 2 }, { S.MOVE_NONE, 2 }, { S.MOVE_NONE, 2 }, { S.MOVE_NONE, 2 } }

  -- ==================================================================== Styx Falls
  L.setBeat("inn", false)
  -- FLAG_SAW_STYX: beat 39 (the Oath Stone) has played, so Alethea has walked to the inn.
  into(S.MAP_INN, 8, 8, { flags = { S.FLAG_SYS_POKEMON_GET, S.FLAG_ACT2_BEGUN, S.FLAG_SAW_STYX }, extra = team })
  expect(partyCount() == 2, "the test team: a Gelasable and a test Pokémon")
  shot("StyxFalls_Inn")
  expect(L.objectOn(4, 7), "Alethea waits at the long table on the first visit")
  expect(bankFlag(S.FLAG_HIDE_ALETHEA_STYX), "and she's set to be gone once you leave")
  L.talk(L.npc("StyxFalls_Inn_EventScript_Alethea"), { shots = { [1] = "inn_alethea" } })
  L.talk(L.npc("StyxFalls_Inn_EventScript_Aroanios"), { answers = { "yes" },
                                                       shots = { [1] = "inn_aroanios", [6] = "inn_beds" } })
  expect(bankFlag(S.FLAG_VISITED_STYX), "rested at the inn: Styx Falls visited")
  L.talk(L.npc("StyxFalls_Inn_EventScript_Gryllos"), { shots = { [2] = "inn_gryllos" } })
  L.talk(L.npc("StyxFalls_Inn_EventScript_Eubouleus"), { answers = { "yes" },
                                                        shots = { [1] = "inn_eubouleus", [7] = "inn_gryllos_given" } })
  expect(bankFlag(S.FLAG_GOT_GRYLLOS), "Eubouleus gave Gryllos")
  expect(partyCount() == 3 and hasSpecies(S.SPECIES_KAPLET), "Gryllos the Kaplet is in the party")
  expect(not L.objectOn(15, 6), "the basket is empty")
  L.talk(L.sign("StyxFalls_Inn_EventScript_Hoof"), { shots = { [1] = "inn_hoof" } })
  L.talk(L.sign("StyxFalls_Inn_EventScript_Window"), { shots = { [1] = "inn_window" } })
  shot("StyxFalls_Inn_after")
  into(S.MAP_INN, 8, 8)
  expect(not L.objectOn(4, 7), "back in the inn, Alethea has gone on (to the Cave of Maia)")
  shot("StyxFalls_Inn_again")

  L.setBeat("oath_house", false)
  into(S.MAP_OATH_HOUSE, 4, 8)
  shot("StyxFalls_OathHouse")
  L.talk(L.npc("StyxFalls_OathHouse_EventScript_Horkia"), { shots = { [1] = "horkia", [8] = "horkia_tag" } })
  expect(bankFlag(S.FLAG_GOT_CLEANSE_TAG) and L.itemCount(S.ITEM_CLEANSE_TAG) == 1, "Horkia's Cleanse Tag")
  L.talk(L.sign("StyxFalls_OathHouse_EventScript_Lamp"), { shots = { [1] = "horkia_lamp" } })
  L.talk(L.sign("StyxFalls_OathHouse_EventScript_Cups"), { shots = { [1] = "horkia_cups" } })
  into(S.MAP_OATH_HOUSE, 4, 8, { flags = { S.FLAG_BADGE05_GET } })
  L.talk(L.npc("StyxFalls_OathHouse_EventScript_Horkia"), { shots = { [2] = "horkia_kallisto_cup" } })
  into(S.MAP_OATH_HOUSE, 4, 8, { clear = { S.FLAG_BADGE05_GET } })

  L.setBeat("stone_house", false)
  into(S.MAP_STONE_HOUSE, 4, 6)
  shot("StyxFalls_StoneHouse")
  L.talk(L.npc("StyxFalls_StoneHouse_EventScript_Kepheus"), { shots = { [1] = "kepheus", [5] = "kepheus_tm" } })
  expect(bankFlag(S.FLAG_GOT_TM_BULLDOZE), "Kepheus's TM Bulldoze (its item waits for Balance)")
  L.talk(L.sign("StyxFalls_StoneHouse_EventScript_Model"), { shots = { [1] = "kepheus_model" } })
  L.talk(L.hidden(S.FLAG_HIDDEN_EVERSTONE), { shots = { [1] = "kepheus_everstone" } })
  expect(L.itemCount(S.ITEM_EVERSTONE) == 1, "the Everstone in the lean-to's rubble")
  shot("StyxFalls_StoneHouse_leanto")

  -- ==================================================================== Arkadia
  L.setBeat("asclepeion", false)
  into(S.MAP_ASCLEPEION, 7, 9)
  shot("Arkadia_Asclepeion")
  local m, hx, hy = L.lastHeal()
  expect(m == S.MAP_ARKADIA, string.format("the Asclepeion sets the respawn to Arkadia (%d,%d)", hx, hy))
  acrossCounter(7, 4, { answers = { "yes" }, shots = { [1] = "heal_ask", [2] = "heal_balls", [3] = "heal_done" } })
  local hp, maxhp = L.partyHp(1)
  expect(hp == maxhp and hp > 0, "the healer healed the party")
  L.talk(L.npc("Arkadia_Asclepeion_EventScript_Panacoil"), { shots = { [1] = "panacoil" } })
  L.talk(L.npc("Arkadia_Asclepeion_EventScript_Huntress"), { shots = { [1] = "huntress_bite" } })
  L.talk(L.npc("Arkadia_Asclepeion_EventScript_Charcoaler"), { shots = { [1] = "charcoaler_chest" } })
  L.talk(L.sign("Arkadia_Asclepeion_EventScript_Channel"), { shots = { [1] = "asclepeion_channel" } })
  L.go(7, 5)
  shot("asclepeion_over_the_channel")

  L.setBeat("agora", false)
  into(S.MAP_AGORA, 6, 8)
  shot("Arkadia_Agora")
  -- Across the counter: her greeting, then the stall's menu (BUY / SELL / SEE YA);
  -- B leaves it, and she says her piece about the arrows.
  L.go(2, 5)
  L.face(K.UP)
  L.tap(K.A)
  wait(60)
  shot("agora_stallkeeper")
  wait(60)
  shot("agora_menu")
  L.tap(K.B)
  wait(40)
  L.settle({ shots = { [1] = "agora_arrows" } })
  L.talk(L.sign("Arkadia_Agora_EventScript_Cypress"), { shots = { [1] = "agora_cypress" } })
  L.go(6, 3)
  shot("agora_under_the_boughs")

  L.setBeat("nyktimos", false)
  into(S.MAP_NYKTIMOS, 7, 7)
  shot("Arkadia_NyktimosHall")
  L.talk(L.npc("Arkadia_NyktimosHall_EventScript_Nyktimos"), { answers = { "yes" },
                                                              shots = { [1] = "nyktimos", [3] = "nyktimos_lykaon" } })
  L.talk(L.npc("Arkadia_NyktimosHall_EventScript_Mother"), { shots = { [1] = "nyktimos_mother" } })
  L.talk(L.sign("Arkadia_NyktimosHall_EventScript_EmptyPlace"), { shots = { [1] = "nyktimos_empty_place" } })
  into(S.MAP_NYKTIMOS, 7, 7, { flags = { S.FLAG_BADGE05_GET } })
  L.talk(L.npc("Arkadia_NyktimosHall_EventScript_Nyktimos"), { answers = { "no" },
                                                              shots = { [2] = "nyktimos_black_glasses" } })
  expect(bankFlag(S.FLAG_GOT_BLACK_GLASSES) and L.itemCount(S.ITEM_BLACK_GLASSES) == 1,
         "Nyktimos's Black Glasses after the Moon Laurel")

  L.setBeat("klymene", false)
  into(S.MAP_KLYMENE, 1, 7, { clear = { S.FLAG_BADGE05_GET } })
  shot("Arkadia_KlymeneHouse")
  L.talk(L.npc("Arkadia_KlymeneHouse_EventScript_Klymene"), { answers = { "no" },
                                                             shots = { [1] = "klymene_atalanta", [6] = "klymene_race" } })
  expect(not bankFlag(S.FLAG_RACE), "saying no starts no race")
  -- The race's finish, both ways: home over the count, then inside it.
  into(S.MAP_KLYMENE, 1, 7, { flags = { S.FLAG_RACE, S.FLAG_RACE_TURNED },
                              vars = { { S.VAR_FRIENDSHIP_STEP_COUNTER, 61 } },
                              scene = { answers = { "no" }, shots = { [1] = "race_lost" } } })
  expect(not bankFlag(S.FLAG_RACE) and not bankFlag(S.FLAG_GOT_CHOICE_SCARF), "61 steps loses to Parthenopaios")
  into(S.MAP_KLYMENE, 1, 7, { flags = { S.FLAG_RACE }, clear = { S.FLAG_RACE_TURNED },
                              vars = { { S.VAR_FRIENDSHIP_STEP_COUNTER, 20 } },
                              scene = { answers = { "no" }, shots = { [1] = "race_no_stair" } } })
  expect(not bankFlag(S.FLAG_GOT_CHOICE_SCARF), "coming home without touching the stair wins nothing")
  into(S.MAP_KLYMENE, 1, 7, { flags = { S.FLAG_RACE, S.FLAG_RACE_TURNED },
                              vars = { { S.VAR_FRIENDSHIP_STEP_COUNTER, 39 } },
                              scene = { shots = { [1] = "race_won", [3] = "race_scarf" } } })
  expect(bankFlag(S.FLAG_GOT_CHOICE_SCARF) and L.itemCount(S.ITEM_CHOICE_SCARF) == 1,
         "39 steps beats him: Klymene's Choice Scarf")
  L.talk(L.npc("Arkadia_KlymeneHouse_EventScript_Klymene"), { shots = { [1] = "klymene_after" } })
  L.talk(L.sign("Arkadia_KlymeneHouse_EventScript_Apples"), { shots = { [1] = "klymene_apples" } })

  L.setBeat("charcoal_hut", false)
  into(S.MAP_CHARCOAL_HUT, 4, 6)
  shot("Arkadia_CharcoalHut")
  expect(L.objectOn(2, 6), "Arkas sits by the door before the trade")
  -- The trade's chooser is the Pithos's screen (OW_CHOOSE_FROM_PC_AND_PARTY): the cursor
  -- starts in the jar; five DOWNs reach the buttons, A on YOUR PARTY opens the party,
  -- and A picks the Gelasable in slot 0 (and SELECT in its menu).
  local chooser = 0
  local function choose()
    chooser = chooser + 1
    if chooser == 1 then
      wait(60)
      shot("trade_pithos")
      for _ = 1, 5 do L.tap(K.DOWN); wait(12) end
      L.tap(K.A); wait(60)
      shot("trade_party")
    end
    L.tap(K.A); wait(40)
    if chooser > 12 then L.fail("the trade's chooser never closed") end
  end
  L.talk(L.npc("Arkadia_CharcoalHut_EventScript_Hippothoos"),
         { answers = { "yes" }, limit = 30000, hooks = { CB2_PokeStorage = choose },
           shots = { [1] = "hippothoos_rats", [5] = "hippothoos_arkas" } })
  expect(bankFlag(S.FLAG_TRADED_ARKOBY), "traded the Gelasable for Arkas")
  expect(hasSpecies(S.SPECIES_ARKOBY) and not hasSpecies(S.SPECIES_GELASABLE), "Arkas the Arkoby is in the party")
  expect(not L.objectOn(2, 6), "the little bear has gone from the door")
  L.talk(L.npc("Arkadia_CharcoalHut_EventScript_Hippothoos"), { shots = { [2] = "hippothoos_shadow" } })
  L.talk(L.sign("Arkadia_CharcoalHut_EventScript_Drawing"), { shots = { [1] = "hippothoos_drawing" } })

  L.setBeat("goatherd", false)
  into(S.MAP_GOATHERD, 2, 7)
  shot("Arkadia_GoatherdHouse")
  expect(not L.objectOn(10, 3) and not L.objectOn(12, 3) and not L.objectOn(9, 8),
         "no lost kid is home yet")
  L.talk(L.npc("Arkadia_GoatherdHouse_EventScript_Krotos"), { shots = { [1] = "krotos_panic" } })
  expect(not bankFlag(S.FLAG_GOT_LUCKY_EGG), "no egg before the kids are home")
  into(S.MAP_GOATHERD, 2, 7, { flags = { S.FLAG_KID_1, S.FLAG_KID_2, S.FLAG_KID_3 } })
  expect(L.objectOn(10, 3) and L.objectOn(12, 3) and L.objectOn(9, 8),
         "the three kids are home in the pen")
  shot("Arkadia_GoatherdHouse_kids_home")
  L.talk(L.npc("Arkadia_GoatherdHouse_EventScript_Krotos"), { shots = { [1] = "krotos_all_three" } })
  expect(bankFlag(S.FLAG_GOT_LUCKY_EGG) and L.itemCount(S.ITEM_LUCKY_EGG) == 1, "Krotos's Lucky Egg")
  L.talk(L.sign("Arkadia_GoatherdHouse_EventScript_PanMask"), { shots = { [1] = "krotos_pan" } })
  log("ok the nine rooms play through")
end

L.start(main)
