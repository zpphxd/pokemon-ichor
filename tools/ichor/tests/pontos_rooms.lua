-- The Black Sea's rooms check, run by tools/ichor/tests/pontos_rooms.sh (read it first).
--
-- Quickstarts, gives a Pidgeot, a Liepard and a Rotom that knows only Thunder
-- Shock, then warps into each of the seven rooms by its door mat and plays it
-- with key presses (engine_lib.lua and slice_lib.lua walk the live map):
--   - every person and every readable thing, talked to or read;
--   - Phineus's dove and Argos's Heat Rock, taken once (a second talk gives nothing);
--   - Ixos's trade (Pidgeot for Unfezant) and Byssa's (Liepard for Persian),
--     with the traded Pokemon swapping places in the room;
--   - the healer heals; the Agora's stall opens; the Pithos opens and shuts;
--   - the Rotom through all five works, one form each, then back out of the
--     last one to its plain form;
--   - out by the mat: the town and the warp id each room's warp 0 names.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local log, expect, wait, shot, tap = L.log, L.expect, L.wait, L.shot, L.tap
for k, v in pairs(dofile(L.OUT .. "pontos_scripts.lua")) do
  if k == "SCRIPTS" then
    for name, addr in pairs(v) do S.SCRIPTS[name] = addr end
  else
    S[k] = v
  end
end

local function species(slot)
  L.setVar(S.VAR_0x8005, slot)
  L.runHeader("PontosTest_SpeciesHeader")
  return L.getVar(S.VAR_0x8000)
end
local function warpId() return emu:read8(L.sb1() + S.OFF_SB1_LOCATION + S.OFF_LOCATION_WARP_ID) end
-- A party Pokemon's nickname, A-Z only.
local function nickname(slot)
  local s = ""
  for i = 0, 11 do
    local b = emu:read8(L.partyMon(slot) + S.OFF_MON_NICKNAME + i)
    if b == 0xFF then break end
    if b >= 0xBB and b <= 0xD4 then s = s .. string.char(65 + b - 0xBB) else s = s .. "?" end
  end
  return s
end

local function enter(header, map, name, mat)
  L.setBeat(name, false)
  L.runHeader(header)
  L.waitUntil(function() return L.mapId() == map and L.idle() end, 4000, "the warp into " .. name)
  wait(20)
  local x, y = L.pos()
  expect(x == mat[1] and y == mat[2], string.format("%s: arrived on the door mat at (%d,%d)", name, x, y))
  shot("room")
end

local function leave(town, wid, name)
  L.useWarp(town)
  expect(L.mapId() == town and warpId() == wid,
         string.format("%s: the mat leads to map %d warp %d (got map %d warp %d)", name, town, wid, L.mapId(), warpId()))
end

local function talkTo(script, opts) return L.talk(L.npc(script), opts) end
local function read(script) return L.talk(L.sign(script)) end

-- The PC's party panel, when a trade asks for a Pokemon: up to YOUR PARTY, open
-- it, `downs` slots down, choose it and SELECT.
local function pickForTrade(downs)
  return function()
    wait(90); shot("trade_choose")
    tap(K.UP); wait(20); tap(K.UP); wait(20)
    tap(K.A); wait(60)
    for _ = 1, downs do tap(K.DOWN); wait(16) end
    shot("trade_party")
    tap(K.A); wait(40)
    tap(K.A); wait(40)
    L.waitUntil(function() return not L.on("CB2_PokeStorage") end, 1200, "the storage screen to close")
  end
end

-- The party menu the workshop's works open: `downs` slots down to the Rotom,
-- choose it, then A through the change and the move it learns.
local function pickRotom(downs, label)
  return function()
    wait(60)
    for _ = 1, downs do tap(K.DOWN); wait(12) end
    shot(label .. "_party")
    tap(K.A)
    local t0, n = L.now(), 0
    while L.on("CB2_UpdatePartyMenu") do
      wait(30)
      if n < 3 then n = n + 1; shot(string.format("%s_change_%d", label, n)) end
      tap(K.A)
      if L.now() - t0 > 3000 then L.fail("the party menu never closed (" .. label .. ")") end
    end
  end
end

L.start(function()
  L.quickstart()
  L.runHeader("PontosTest_SetupHeader")
  expect(species(0) == S.SPECIES_PIDGEOT and species(1) == S.SPECIES_LIEPARD and species(2) == S.SPECIES_ROTOM,
         "the party is a Pidgeot, a Liepard and a Rotom")

  -- Phineus's house: the dove, once; the cage empties.
  enter("PontosTest_PhineusHeader", S.MAP_PHINEUS, "phineus", { 4, 7 })
  talkTo("Salmydessos_PhineussHouse_EventScript_Phineus", { every = true })
  expect(L.getFlag(S.FLAG_GOT_PHINEUS_DOVE), "Phineus gives the dove (FLAG_ICHOR_GOT_PHINEUS_DOVE)")
  shot("cage_empty")
  talkTo("Salmydessos_PhineussHouse_EventScript_Phineus")
  expect(L.getFlag(S.FLAG_GOT_PHINEUS_DOVE), "a second talk: his stool, and no second dove")
  for _, s in ipairs({ "DoveCage", "Shutters", "ClawMarks", "Table", "Jars", "Stool" }) do
    read("Salmydessos_PhineussHouse_EventScript_" .. s)
  end
  leave(S.MAP_SALMYDESSOS, 0, "phineus")

  -- The bird-catcher's: the trade, then the Pidgeot in the Unfezant's place.
  enter("PontosTest_BirdCatcherHeader", S.MAP_BIRDCATCHER, "birdcatcher", { 3, 6 })
  talkTo("Salmydessos_BirdCatchersHouse_EventScript_Unfezant")
  talkTo("Salmydessos_BirdCatchersHouse_EventScript_Ixos", { hooks = { CB2_PokeStorage = pickForTrade(0) } })
  expect(L.getFlag(S.FLAG_TRADED_UNFEZANT), "Ixos's trade sets FLAG_ICHOR_TRADED_UNFEZANT")
  expect(species(0) == S.SPECIES_UNFEZANT and nickname(0) == "PHASIANOS",
         "the Pidgeot's slot now holds PHASIANOS the Unfezant (" .. nickname(0) .. ")")
  shot("after_trade")
  talkTo("Salmydessos_BirdCatchersHouse_EventScript_Pidgeot")
  talkTo("Salmydessos_BirdCatchersHouse_EventScript_Ixos")
  for _, s in ipairs({ "Cages", "LimeSticks", "DecoyOwl" }) do
    read("Salmydessos_BirdCatchersHouse_EventScript_" .. s)
  end
  leave(S.MAP_SALMYDESSOS, 1, "birdcatcher")

  -- The Asclepeion: the healer heals across the counter; the Pithos opens and shuts.
  enter("PontosTest_AsclepeionHeader", S.MAP_ASCLEPEION, "asclepeion", { 6, 9 })
  local hp = L.partyHp(0)
  emu:write16(L.partyMon(0) + S.OFF_MON_HP, 1)
  talkTo("Aia_Asclepeion_EventScript_Healer", { every = true })
  local hp2, max = L.partyHp(0)
  expect(hp2 == max and hp2 >= hp, string.format("the healer heals the party (%d/%d)", hp2, max))
  talkTo("Aia_Asclepeion_EventScript_Watcher")
  talkTo("Aia_Asclepeion_EventScript_OldMan")
  read("Aia_Asclepeion_EventScript_Serpent")
  L.talk(L.sign("Aia_Asclepeion_EventScript_Pithos"), { noSettle = true })
  local function menuUp()
    return L.taskRunning("Task_HandleScrollingMultichoiceInput") or L.taskRunning("Task_HandleMultichoiceInput")
  end
  local t0 = L.now()
  while not menuUp() do
    if L.boxUp() then wait(34); if not menuUp() then tap(K.A) end end
    wait(4)
    if L.now() - t0 > 1500 then L.fail("the Pithos never offered its menu") end
  end
  wait(20); shot("pithos_menu")
  expect(true, "the Pithos opens its menu: Pokemon, your things, close the lid")
  tap(K.B)
  L.settle()
  leave(S.MAP_AIA, 0, "asclepeion")

  -- The Agora: the stall opens; the people and the fleece.
  enter("PontosTest_AgoraHeader", S.MAP_AGORA, "agora", { 5, 8 })
  talkTo("Aia_Agora_EventScript_Korax", { noSettle = true })
  L.waitUntil(function() return L.taskRunning("Task_ShopMenu") end, 600, "the stall's menu")
  wait(20); shot("stall")
  expect(true, "Korax's stall opens")
  tap(K.B)
  L.settle()
  talkTo("Aia_Agora_EventScript_FleeceMan")
  talkTo("Aia_Agora_EventScript_Sailor")
  for _, s in ipairs({ "Fleece", "Pheasants", "Linen" }) do read("Aia_Agora_EventScript_" .. s) end
  leave(S.MAP_AIA, 1, "agora")

  -- Phrixos's sons: the story and the Heat Rock, once.
  enter("PontosTest_PhrixosHeader", S.MAP_PHRIXOS, "phrixos", { 4, 7 })
  talkTo("Aia_PhrixosSonsHouse_EventScript_Argos", { every = true })
  expect(L.getFlag(S.FLAG_GOT_HEAT_ROCK) and L.itemCount(S.ITEM_HEAT_ROCK) == 1,
         "Argos gives a Heat Rock (FLAG_ICHOR_GOT_HEAT_ROCK)")
  talkTo("Aia_PhrixosSonsHouse_EventScript_Argos")
  expect(L.itemCount(S.ITEM_HEAT_ROCK) == 1, "a second talk: the wreck's story, and no second Heat Rock")
  talkTo("Aia_PhrixosSonsHouse_EventScript_Phrontis")
  talkTo("Aia_PhrixosSonsHouse_EventScript_Melas")
  for _, s in ipairs({ "RamPanel", "Altar", "Hearth" }) do read("Aia_PhrixosSonsHouse_EventScript_" .. s) end
  leave(S.MAP_AIA, 2, "phrixos")

  -- The linen-weaver's: the trade (the Liepard is the second Pokemon), then the
  -- Liepard in the Persian's place.
  enter("PontosTest_LinenHeader", S.MAP_LINEN, "linen", { 5, 7 })
  talkTo("Aia_LinenWeaversHouse_EventScript_Persian")
  talkTo("Aia_LinenWeaversHouse_EventScript_Byssa", { hooks = { CB2_PokeStorage = pickForTrade(1) } })
  expect(L.getFlag(S.FLAG_TRADED_PERSIAN), "Byssa's trade sets FLAG_ICHOR_TRADED_PERSIAN")
  expect(species(1) == S.SPECIES_PERSIAN and nickname(1) == "TIGRIS",
         "the Liepard's slot now holds TIGRIS the Persian (" .. nickname(1) .. ")")
  shot("after_trade")
  talkTo("Aia_LinenWeaversHouse_EventScript_Liepard")
  talkTo("Aia_LinenWeaversHouse_EventScript_Byssa")
  for _, s in ipairs({ "Loom", "LinenLine", "Flax", "Bolts", "Tub" }) do read("Aia_LinenWeaversHouse_EventScript_" .. s) end
  leave(S.MAP_AIA, 3, "linen")

  -- The workshop: Tekton, the loose Rotom, then the five works in turn.
  enter("PontosTest_WorkshopHeader", S.MAP_WORKSHOP, "workshop", { 6, 8 })
  talkTo("Aia_PalaceWorkshop_EventScript_Tekton")
  talkTo("Aia_PalaceWorkshop_EventScript_Rotom")
  for _, s in ipairs({ "GoldenMaid", "Tripod", "Workbench" }) do read("Aia_PalaceWorkshop_EventScript_" .. s) end
  local works = {
    { "FireJar", S.SPECIES_ROTOM_HEAT, "fire_jar" },
    { "WashBasin", S.SPECIES_ROTOM_WASH, "wash_basin" },
    { "ColdKrater", S.SPECIES_ROTOM_FROST, "cold_krater" },
    { "Fan", S.SPECIES_ROTOM_FAN, "fan" },
    { "Sledge", S.SPECIES_ROTOM_MOW, "sledge" },
  }
  for _, w in ipairs(works) do
    L.talk(L.sign("Aia_PalaceWorkshop_EventScript_" .. w[1]),
           { hooks = { CB2_UpdatePartyMenu = pickRotom(2, w[3]) } })
    local got = species(2)
    expect(got == w[2], string.format("the %s turns the Rotom into form %d (got %d)", w[3], w[2], got))
  end
  L.talk(L.sign("Aia_PalaceWorkshop_EventScript_Sledge"), { hooks = { CB2_UpdatePartyMenu = pickRotom(2, "out") } })
  expect(species(2) == S.SPECIES_ROTOM, "the same work again lets the Rotom back out, plain")
  leave(S.MAP_AIA, 4, "workshop")
end)
