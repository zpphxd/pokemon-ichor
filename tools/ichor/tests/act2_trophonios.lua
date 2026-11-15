-- Trophonios's cave check, run by tools/ichor/tests/act2_trophonios.sh (read it first).
--
-- Plays the optional descent (SCRIPT.md Part 5, beats 35B-35C) with key presses on
-- slice_lib's walker: in through the grille (opened directly, as Saon does), the dark
-- upper chamber and the throne, down the ladder into the dark, brazier 1, Herkyna's
-- goose, the first chalk hand by torchlight and doused, the hidden Bronze Obol, the
-- ford, the marble rubble (the Bronze Hammer) to the Max Repel, Philomelos at the
-- stair's foot; then B2F: the spring, forks A-C, the web den (the Torch), the snake
-- fed with honey, Melampos by the black pool, the great boulder (Hephaestus's Hammer)
-- and the dig behind it, brazier 2, the TM's ledge, and the hole: the reading on the
-- throne of Mnemosyne (beat 35C). Then back down with everything still as left, and
-- the hole as the way out to Lebadeia.
--
-- Prints "TROPH ok ..." per check and "TROPH shot ..." per screenshot, and ends with
-- "TROPH done"; any failure prints "TROPH FAIL: ..." first.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local log, expect, wait, shot, settle = L.log, L.expect, L.wait, L.shot, L.settle
for k, v in pairs(dofile(L.OUT .. "troph_scripts.lua")) do S.SCRIPTS[k] = v end
local B1, B2 = "TrophoniosCave_B1F_EventScript_", "TrophoniosCave_B2F_EventScript_"

-- Fixed points (tools/ichor/maps/trophonios.py)
local GRILLE, THRONE, B1F_STAIR, B1F_BRAZIER = { 9, 3 }, { 12, 5 }, { 27, 21 }, { 14, 13 }
local B2F_STAIR, CLEFT, B2F_BRAZIER = { 3, 2 }, { 20, 11 }, { 10, 14 }

local function mt(x, y) return (L.grid().tile(x, y)) end
local function flash() return emu:read8(L.sb1() + S.OFF_SB1_FLASH_LEVEL) end
local function at(p) local x, y = L.pos() return x == p[1] and y == p[2] end
local function arrive(map, what)
  L.waitUntil(function() return L.mapId() == map and L.idle() end, 4000, what)
  wait(30)
end
-- Step onto a stair (MB_LADDER) from the tile beside it.
local function stair(p, from, key, map)
  L.go(from[1], from[2])
  L.face(key)
  emu:addKey(key); wait(20); emu:clearKey(key)
  arrive(map, "the stair to map " .. map)
end

L.start(function()
  L.quickstart()
  L.runHeader("TrophTest_SetupHeader", { noSettle = true })
  arrive(S.MAP_B1F, "the cave's B1F")

  -- B1F: the upper chamber, inside the grille.
  L.setBeat("b1f_upper")
  expect(at(GRILLE), "arrived on the grille's steps")
  expect(flash() == S.ICHOR_FLASH_TORCH, string.format("inside the grille it's dark: the torch's circle (flash %d)", flash()))
  shot("upper_chamber")
  L.talk(L.sign(B1 .. "Throne"), { shots = { [1] = "throne" } })
  L.talk(L.sign(B1 .. "Tablets"))
  L.talk(L.hidden(S.FLAG_HIDDEN_HONEY))
  expect(L.getFlag(S.FLAG_HIDDEN_HONEY) and L.itemCount(S.ITEM_HONEY) == 2, "the hidden honey by the throne")

  -- Down the ladder into the dark.
  L.setBeat("b1f_descent")
  L.go(9, 8); shot("ladder_top")
  L.go(9, 11); shot("on_the_ladder")
  expect(not L.goTrigger(L.triggers(B1 .. "LadderFoot")), "the ladder's foot: the dark, and water running")
  settle({ shots = { [1] = "ladder_foot" } })
  expect(flash() == S.ICHOR_FLASH_TORCH, string.format("below the ladder it's the torch's circle (flash %d)", flash()))
  L.talk(L.ball(S.FLAG_ESCAPE_ROPE))
  expect(L.getFlag(S.FLAG_ESCAPE_ROPE), "the Escape Rope at the ladder's foot")

  -- Brazier 1 by the stream lights the stream chamber for good.
  L.talk(L.sign(B1 .. "Brazier"), { shots = { [1] = "brazier_ask" }, answers = { "yes" } })
  expect(L.getFlag(S.FLAG_BRAZIER_B1F), "brazier 1 is lit (its flag)")
  expect(mt(B1F_BRAZIER[1], B1F_BRAZIER[2]) == S.MT_BRAZIER_LIT_TOP
         and mt(B1F_BRAZIER[1], B1F_BRAZIER[2] + 1) == S.MT_BRAZIER_LIT, "brazier 1 burns (its metatiles)")
  expect(flash() == 0, "the stream chamber is lit")
  shot("stream_chamber_lit")

  -- Herkyna's goose, standing in the stream.
  L.talk(L.npc(B1 .. "Goose"), { shots = { [1] = "goose" }, answers = { "yes" } })
  expect(L.getFlag(S.FLAG_GOOSE), "the goose went home up the stream")
  expect(not L.npc(B1 .. "Goose").present, "the goose is gone from the stream")

  -- The first chalk hand: by torchlight, then doused.
  L.talk(L.sign(B1 .. "Handprint"), { shots = { [1] = "handprint_lit" } })
  L.runHeader("TrophTest_DouseHeader")
  expect(L.getFlag(S.FLAG_TORCH_DOUSED) and flash() == S.ICHOR_FLASH_DOUSED, "the torch is doused: black")
  shot("doused")
  L.talk(L.sign(B1 .. "Handprint"), { shots = { [1] = "handprint_doused" } })
  L.runHeader("TrophTest_RelightHeader")
  expect(not L.getFlag(S.FLAG_TORCH_DOUSED), "the torch is lit again")

  -- The Bronze Obol in the stream; across the ford.
  L.talk(L.ball(S.FLAG_DAMP_ROCK))
  expect(L.getFlag(S.FLAG_DAMP_ROCK), "the Damp Rock in the wet corner by the stream's outlet")
  L.talk(L.hidden(S.FLAG_HIDDEN_OBOL))
  expect(L.getFlag(S.FLAG_HIDDEN_OBOL) and L.itemCount(S.ITEM_RELIC_COPPER) == 1, "the Bronze Obol in the stream")
  L.go(19, 16); shot("the_ford")
  L.go(19, 17); shot("south_bank")

  -- West: the marble rubble (the Bronze Hammer) and the Max Repel behind it.
  L.talk(L.npc("EventScript_RockSmash"), { shots = { [1] = "rubble" }, answers = { "yes" } })
  expect(not L.npc("EventScript_RockSmash").present, "the Bronze Hammer broke the marble rubble")
  L.talk(L.ball(S.FLAG_MAX_REPEL))
  expect(L.getFlag(S.FLAG_MAX_REPEL), "the Max Repel past the rubble")
  expect(flash() == S.ICHOR_FLASH_TORCH, "the rubble's passage is dark again")
  shot("max_repel_nook")

  -- East: Philomelos at the stair's foot, then down.
  L.setBeat("b1f_philomelos")
  L.go(22, 19); shot("philomelos_approach")
  L.go(22, 21)
  settle({ shots = { [1] = "philomelos" } })
  expect(L.defeated(S.TRAINER_PHILOMELOS), "Philomelos battled at the stair's foot")
  shot("b1f_stair")
  stair(B1F_STAIR, { 26, 21 }, K.RIGHT, S.MAP_B2F)

  -- B2F: the spring.
  L.setBeat("b2f")
  expect(at(B2F_STAIR), "down the stair onto B2F")
  shot("b2f_arrival")
  emu:write16(L.partyMon(0) + S.OFF_MON_HP, 1)
  L.talk(L.sign(B2 .. "Spring"), { shots = { [2] = "spring" } })
  local hp, maxhp = L.partyHp(0)
  expect(hp == maxhp, "the spring heals the party (the midpoint rest)")

  -- Fork A: its wrong branch loops back; the Ether hidden in the loop.
  L.talk(L.sign(B2 .. "HandprintA"))
  L.talk(L.hidden(S.FLAG_HIDDEN_ETHER))
  expect(L.getFlag(S.FLAG_HIDDEN_ETHER), "the Ether hidden in fork A's loop")
  L.go(7, 6); L.go(7, 4); shot("fork_a_loop_back")

  -- Fork B: the dead end's Max Ether; the web den behind its curtain.
  L.talk(L.ball(S.FLAG_MAX_ETHER))
  expect(L.defeated(S.TRAINER_MNESARETE), "Mnesarete battled where the passage narrows past fork A")
  expect(L.getFlag(S.FLAG_MAX_ETHER), "fork B's dead end pays: the Max Ether")
  L.talk(L.sign(B2 .. "HandprintB"))
  L.talk(L.npc("EventScript_IchorCobweb"), { shots = { [1] = "cobweb" }, answers = { "yes" } })
  expect(not L.npc("EventScript_IchorCobweb").present, "the Torch burned the cobweb curtain")
  L.talk(L.ball(S.FLAG_SPELL_TAG))
  expect(L.getFlag(S.FLAG_SPELL_TAG), "the Spell Tag in the web den")
  shot("web_den")

  -- Fork C: the dead end's Hyper Potion; the snake fed with honey.
  L.talk(L.ball(S.FLAG_HYPER_POTION))
  expect(L.getFlag(S.FLAG_HYPER_POTION), "fork C's dead end pays: the Hyper Potion")
  L.talk(L.sign(B2 .. "HandprintC"))
  expect(mt(CLEFT[1], CLEFT[2]) == S.MT_CLEFT_COILS, "something coils in the cleft")
  local honey = L.itemCount(S.ITEM_HONEY)
  L.talk(L.npc(B2 .. "Snake"), { shots = { [1] = "snake", [3] = "snake_honey" }, answers = { "yes" } })
  expect(L.getFlag(S.FLAG_SNAKE_FED), "the snake took the honey")
  expect(L.itemCount(S.ITEM_HONEY) == honey - 1, "one Honey left in the cleft")
  expect(mt(CLEFT[1], CLEFT[2]) == S.MT_CLEFT_EMPTY, "the cleft is empty")
  shot("cleft_open")

  -- The black pool: Melampos (optional), the great boulder, the Dusk Stone.
  L.setBeat("b2f_pool")
  L.go(21, 11); shot("black_pool")
  L.talk(L.sign(B2 .. "BlackPool"))
  L.talk(L.npc(B2 .. "Melampos"), { shots = { [1] = "melampos" } })
  expect(L.defeated(S.TRAINER_MELAMPOS), "Melampos battled by the black pool")
  L.talk(L.hidden(S.FLAG_HIDDEN_DUSK_STONE))
  expect(L.getFlag(S.FLAG_HIDDEN_DUSK_STONE), "the Dusk Stone on the black pool's far rim")
  L.talk(L.npc("EventScript_IchorGreatBoulder"), { shots = { [1] = "boulder_without" } })
  expect(L.npc("EventScript_IchorGreatBoulder").present, "without Hephaestus's Hammer the great boulder stays")
  L.runHeader("TrophTest_HephaestusHeader")
  L.talk(L.npc("EventScript_IchorGreatBoulder"), { shots = { [1] = "boulder_split" }, answers = { "yes" } })
  expect(L.getFlag(S.FLAG_BOULDER_GONE), "Hephaestus's Hammer split the great boulder (its hide flag)")
  L.talk(L.sign(B2 .. "DigSpot"), { shots = { [1] = "dig_spot" } })

  -- The oracle's chamber: brazier 2, the TM's ledge, the hole.
  L.setBeat("b2f_oracle")
  L.go(12, 17); shot("oracle_threshold")
  L.talk(L.sign(B2 .. "Brazier"), { answers = { "yes" } })
  expect(L.getFlag(S.FLAG_BRAZIER_B2F) and mt(B2F_BRAZIER[1], B2F_BRAZIER[2] + 1) == S.MT_BRAZIER_LIT,
         "brazier 2 burns in the oracle's chamber")
  expect(flash() == 0, "the oracle's chamber is lit")
  L.talk(L.ball(S.FLAG_TM))
  expect(L.getFlag(S.FLAG_TM), "the TM on the ledge")
  L.go(7, 15); shot("the_hole")

  -- Beat 35C: the hole, black, then the throne of Mnemosyne.
  L.setBeat("35c_reading")
  L.talk(L.sign(B2 .. "Hole"), { answers = { "yes" }, every = true })
  expect(L.mapId() == S.MAP_B1F and at(THRONE), "up through the hole onto the throne of Mnemosyne")
  expect(L.getFlag(S.FLAG_READING), "the reading has played")
  expect(not L.npc(B1 .. "Saon").present and not L.npc(B1 .. "Alethea").present,
         "the priests and Alethea have gone back up")
  expect(L.playing(S.MUS_HOLLOW), "the cave's music is back after the silence")
  shot("after_the_reading")

  -- Back down: everything as it was left; the hole is now the way out.
  L.setBeat("way_out")
  L.runHeader("TrophTest_RepelHeader")
  L.go(9, 13)
  expect(flash() == 0 and mt(B1F_BRAZIER[1], B1F_BRAZIER[2]) == S.MT_BRAZIER_LIT_TOP,
         "brazier 1 still burns and lights the stream")
  stair(B1F_STAIR, { 26, 21 }, K.RIGHT, S.MAP_B2F)
  L.go(19, 11)
  expect(mt(CLEFT[1], CLEFT[2]) == S.MT_CLEFT_EMPTY and not L.npc(B2 .. "Snake").present, "the snake stays gone")
  L.go(7, 15)
  expect(flash() == 0 and mt(B2F_BRAZIER[1], B2F_BRAZIER[2]) == S.MT_BRAZIER_LIT_TOP, "brazier 2 still burns")
  L.talk(L.sign(B2 .. "Hole"), { answers = { "yes" }, shots = { [2] = "feet_first" } })
  arrive(S.MAP_LEBADEIA, "Lebadeia, out through the hole")
  expect(L.mapId() == S.MAP_LEBADEIA, "the hole is the way out: Lebadeia, at the grille")
  shot("lebadeia")
end)
