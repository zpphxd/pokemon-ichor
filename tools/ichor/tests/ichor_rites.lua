-- Rites check, run by tools/ichor/tests/ichor_rites.sh (read it first).
-- Altars run as a map's bg event would run them (ichor_rites_setup.s), on Route 1.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local log, expect, wait, shot, tap, settle = L.log, L.expect, L.wait, L.shot, L.tap, L.settle

local PX, PY = 11, 47

local function favor(god) return emu:read8(L.ichor() + S.OFF_ICHOR_FAVOR + god) end
local function setFavor(god, v) emu:write8(L.ichor() + S.OFF_ICHOR_FAVOR + god, v) end
local function blessing()
  local b = L.ichor()
  return emu:read8(b + S.OFF_ICHOR_BLESSING_GOD), emu:read16(b + S.OFF_ICHOR_BLESSING_STEPS), emu:read8(b + S.OFF_ICHOR_BLESSING_FLAGS)
end
local function give(item, n)
  L.setVar(S.VAR_0x8004, item); L.setVar(S.VAR_0x8005, n or 1)
  L.runHeader("RitesTest_GiveHeader")
end

local function menuUp()
  return L.taskRunning("Task_HandleScrollingMultichoiceInput") or L.taskRunning("Task_HandleMultichoiceInput")
end

-- Run an altar and pick its menu entry `index` (0 PRAY, 1 MAKE AN OFFERING / OFFER A
-- BATTLE, 2 FAVOR, ...). opts.offer picks the offering list's entry; opts.answers go to settle.
local function altar(header, index, name, opts)
  opts = opts or {}
  L.runHeader(header, { noSettle = true })
  L.waitUntil(menuUp, 600, "the altar's menu")
  wait(20); shot(name .. "_menu")
  for _ = 1, index do tap(K.DOWN); wait(8) end
  tap(K.A)
  if opts.offer then
    L.waitUntil(function() return not menuUp() end, 120, "the altar menu to close")
    L.waitUntil(menuUp, 600, "the offering list")
    wait(20); shot(name .. "_offerings")
    for _ = 1, opts.offer do tap(K.DOWN); wait(8) end
    tap(K.A)
  end
  settle({ answers = opts.answers, shots = { [1] = name .. "_1", [2] = name .. "_2", [3] = name .. "_3" },
           hooks = opts.hooks })
end


L.start(function()
  L.quickstart()
  L.setVar(S.VAR_0x8008, PX); L.setVar(S.VAR_0x8009, PY)
  L.runHeader("RitesTest_SetupHeader", { limit = 4000 })
  L.waitUntil(function() return L.mapId() == S.MAP_ROUTE1 and L.idle() end, 3000, "Route 1")
  wait(40)

  -- Pray: the minor blessing, +1 Favor the first time today only
  altar("RitesTest_ApolloHeader", 0, "pray")
  local god, steps, flags = blessing()
  expect(favor(S.ICHOR_GOD_APOLLO) == 1 and god == S.ICHOR_GOD_APOLLO and steps == 100 and flags & S.ICHOR_BLESSING_MAJOR == 0,
         string.format("praying to Apollo: Favor %d, his minor blessing for %d steps", favor(S.ICHOR_GOD_APOLLO), steps))
  altar("RitesTest_ApolloHeader", 0, "pray_again")
  expect(favor(S.ICHOR_GOD_APOLLO) == 1, "a second prayer the same day gives no more Favor")

  -- The start menu's blessing panel
  tap(K.START); wait(40); shot("blessing_panel"); tap(K.B); wait(30)

  -- An offering he loves: +5 Favor, Hestia's +1, the major blessing
  give(S.ITEM_LAUREL_SPRIG, 5)
  altar("RitesTest_ApolloHeader", 1, "offer", { offer = 0 })
  god, steps, flags = blessing()
  expect(favor(S.ICHOR_GOD_APOLLO) == 6 and favor(S.ICHOR_GOD_HESTIA) == 1,
         string.format("a Laurel Sprig: Apollo %d Favor, Hestia %d", favor(S.ICHOR_GOD_APOLLO), favor(S.ICHOR_GOD_HESTIA)))
  expect(god == S.ICHOR_GOD_APOLLO and steps == 500 and flags & S.ICHOR_BLESSING_MAJOR ~= 0, "... and his major blessing, 500 steps")
  -- at his temple, offerings count double
  altar("RitesTest_ApolloTempleHeader", 1, "temple", { offer = 0 })
  expect(favor(S.ICHOR_GOD_APOLLO) == 16, string.format("the temple altar doubles it (Favor %d)", favor(S.ICHOR_GOD_APOLLO)))

  -- FAVOR
  altar("RitesTest_ApolloHeader", 2, "favor")

  -- Gift I at 30: a lesson, taught through the party menu
  setFavor(S.ICHOR_GOD_APOLLO, 29)
  altar("RitesTest_ApolloHeader", 1, "gift_i", { offer = 0 })  -- settle picks the first Pokémon
  expect(L.getFlag(S.FLAG_GIFT_APOLLO_I), "Favor 30: Apollo's lesson, Solar Beam, is taught")
  -- the altar now offers the LESSON again
  L.runHeader("RitesTest_ApolloHeader", { noSettle = true })
  L.waitUntil(menuUp, 600, "the altar's menu")
  wait(20); shot("lesson_entry"); tap(K.B); settle()

  -- Gift II at 60: the Lyre of Apollo
  setFavor(S.ICHOR_GOD_APOLLO, 59)
  altar("RitesTest_ApolloHeader", 1, "gift_ii", { offer = 0 })
  expect(L.getFlag(S.FLAG_GIFT_APOLLO_II) and L.itemCount(S.ITEM_POKE_FLUTE) == 1, "Favor 60: the Lyre of Apollo")
  -- Gift III at 100
  setFavor(S.ICHOR_GOD_APOLLO, 99)
  altar("RitesTest_ApolloHeader", 1, "gift_iii", { offer = 0 })
  expect(L.getFlag(S.FLAG_GIFT_APOLLO_III), "Favor 100: Apollo's sacred animal")

  -- Another god's blessing: the altar asks first
  altar("RitesTest_AthenaHeader", 0, "conflict_no", { answers = { "no" } })
  god = blessing()
  expect(god == S.ICHOR_GOD_APOLLO, "answering NO keeps Apollo's blessing")
  altar("RitesTest_AthenaHeader", 0, "conflict_yes", { answers = { "yes" } })
  god = blessing()
  expect(god == S.ICHOR_GOD_ATHENA, "answering YES takes Athena's")

  -- The blessing walks down to its fading line
  emu:write16(L.ichor() + S.OFF_ICHOR_BLESSING_STEPS, 2)
  L.step(K.LEFT); L.step(K.RIGHT)
  settle({ shots = { [1] = "faded" } })
  god = blessing()
  expect(god == 0, "two steps on, Athena's blessing fades")

  -- Hestia's Hearthfire, from the Relic Ring
  altar("RitesTest_HearthHeader", 0, "hearth_pray")
  emu:write16(L.partyMon(0) + S.OFF_MON_HP, 1)
  tap(K.SELECT)
  L.waitUntil(menuUp, 300, "the Relic Ring with HEARTHFIRE")
  wait(20); shot("ring_hearthfire")
  tap(K.A)
  settle()
  local hp, max = L.partyHp(0)
  god = blessing()
  expect(hp == max and hp > 1 and god == 0, string.format("Hearthfire heals the party (%d/%d) and is spent", hp, max))

  -- Demeter turns the pomegranate away
  give(S.ITEM_POMEG_BERRY, 1)
  local laurels = L.itemCount(S.ITEM_LAUREL_SPRIG)
  altar("RitesTest_DemeterHeader", 1, "pomegranate", { offer = laurels > 0 and 1 or 0 })
  expect(L.itemCount(S.ITEM_POMEG_BERRY) == 1 and favor(S.ICHOR_GOD_DEMETER) == 0, "Demeter does not take the pomegranate")

  -- A desecrated altar, cleansed, though a battle just left VAR_RESULT TRUE
  local before = favor(S.ICHOR_GOD_APOLLO)
  L.setFlag(S.FLAG_ICHOR_ALTARS_START, false)
  L.setVar(S.VAR_RESULT, 1)
  L.runHeader("RitesTest_DesecratedHeader", { answers = { "yes" } })
  expect(L.getFlag(S.FLAG_ICHOR_ALTARS_START) and favor(S.ICHOR_GOD_APOLLO) == math.min(before + 3, 100),
         "cleansing a desecrated altar marks it and gives its god +3 Favor")
end)
