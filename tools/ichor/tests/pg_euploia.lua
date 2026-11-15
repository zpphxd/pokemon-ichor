-- The Euploia refitted, run by tools/ichor/tests/pg_euploia.sh (read it first).

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local log, expect, wait, shot, tap = L.log, L.expect, L.wait, L.shot, L.tap

for k, v in pairs(dofile(L.OUT .. "euploia_scripts.lua")) do S.SCRIPTS[k] = v end
for _, k in ipairs({ "EventScript_IchorAltar_Poseidon", "EventScript_IchorLeaveShip" }) do
  if not S[k] then L.fail("the ROM has no " .. k) end
  S.SCRIPTS[k] = S[k]
end

local CREW = { "LAMPON", "DIKTYS", "KYDON", "PHEMIOS", "LYNKEUS", "IASO", "GLAUKIAS", "NOLAN", "OARSMEN" }
local HAUL = { "PEARL", "BIG_PEARL", "HEART_SCALE", "SHOAL_SALT", "SHOAL_SHELL", "STAR_PIECE", "WATER_STONE" }

local function setCrew(on) for _, c in ipairs(CREW) do L.setFlag(S["FLAG_ICHOR_CREW_" .. c], on) end end
local function blessingGod() return emu:read8(L.ichor() + S.OFF_ICHOR_BLESSING_GOD) end
local function favor(god) return emu:read8(L.ichor() + S.OFF_ICHOR_FAVOR + god) end
local function hauled()
  local n = 0
  for _, it in ipairs(HAUL) do n = n + L.itemCount(S["ITEM_" .. it]) end
  return n
end
local function hurt() for slot = 0, 1 do emu:write16(L.partyMon(slot) + S.OFF_MON_HP, 1) end end
local function full()
  for slot = 0, 1 do
    local h, m = L.partyHp(slot)
    if h ~= m then return false end
  end
  return true
end
local function metatile(x, y) return (L.grid().tile(x, y)) end

-- Aboard: the person's hide flag is clear. (People off screen aren't spawned, so
-- this reads the template's flag, which ON_TRANSITION set or left clear.)
local function aboard(script)
  local addr = S.SCRIPTS[script]
  for _, o in ipairs(L.mapEvents().objects) do
    if o.script == addr then return o.flag == 0 or not L.getFlag(o.flag) end
  end
  L.fail("no one on this map runs " .. script)
end
local function talk(script, opts) return L.talk(L.npc(script), opts) end
local function read(script, opts) return L.talk(L.sign(script), opts) end

-- Talk to or read something, pressing A through its text, and report whether a
-- menu (a multichoice or the shop) came up; B closes it, and the rest plays out.
local function menuDuring(target, name)
  L.talk(target, { noSettle = true })
  local seen
  for _ = 1, 120 do
    if L.taskRunning("Task_ShopMenu") then seen = "shop" break end
    if L.taskRunning("Task_HandleMultichoiceInput") or L.taskRunning("Task_HandleScrollingMultichoiceInput") then
      seen = "menu" break
    end
    if L.idle() then break end
    tap(K.A); wait(20)
  end
  if seen then
    wait(20); shot(name); tap(K.B); wait(20)
  end
  L.settle()
  return seen
end

local function arrive(map, what)
  L.waitUntil(function() return L.mapId() == map and L.idle() end, 3000, what)
  wait(30)
end
local function toDeck() L.runHeader("EuploiaTest_DeckHeader", { limit = 4000 }); arrive(S.MAP_DECK, "the deck") end
local function toBelow() L.runHeader("EuploiaTest_BelowHeader", { limit = 4000 }); arrive(S.MAP_BELOW, "below deck") end

local DECK_CREW = { "Lynkeus", "Glaukias", "Nolan", "Oarsman1", "Oarsman2", "Oarsman3" }
local BELOW_CREW = { "Lampon", "Kydon", "Phemios", "Iaso", "Diktys" }

L.start(function()
  L.quickstart()
  L.runHeader("EuploiaTest_SetupHeader", { limit = 4000 })
  arrive(S.MAP_DECK, "the deck")
  L.beat = "deck"

  -- --- The deck before the ship is given, then with no crew ---------------------------------
  L.setFlag(S.FLAG_ICHOR_GOT_EUPLOIA, false)
  toDeck()
  expect(not aboard("EuploiaDeck_EventScript_Nausikles") and not aboard("EuploiaDeck_EventScript_Alethea"),
         "before Nausikles gives you the ship, he and Alethea aren't on her deck")
  local b = read("EuploiaDeck_EventScript_Chart")
  expect(b >= 1, "the chart table is bare without Alethea")
  L.setFlag(S.FLAG_ICHOR_GOT_EUPLOIA, true)
  toDeck()
  expect(aboard("EuploiaDeck_EventScript_Nausikles") and aboard("EuploiaDeck_EventScript_Alethea"),
         "with the ship given, Nausikles and Alethea are aboard")
  local away = {}
  for _, who in ipairs(DECK_CREW) do
    if aboard("EuploiaDeck_EventScript_" .. who) then away[#away + 1] = who end
  end
  expect(#away == 0, "no other crew on deck before they sign on (" .. table.concat(away, ", ") .. ")")
  shot("deck_no_crew")

  b = talk("EuploiaDeck_EventScript_Nausikles")
  expect(b >= 1, string.format("Nausikles at the helm calls EventScript_IchorHelm (%d boxes)", b))
  b = talk("EuploiaDeck_EventScript_Alethea")
  expect(b >= 2, string.format("Alethea talks about the chart and its blank west (%d boxes)", b))
  b = read("EuploiaDeck_EventScript_Chart")
  expect(b >= 2, string.format("the chart: Aethos inked in, the west blank (%d boxes)", b))
  b = read("EuploiaDeck_EventScript_Benches")
  expect(b >= 1, "the oarsmen's benches stand empty without them")
  read("EventScript_IchorAltar_Poseidon")
  expect(favor(S.ICHOR_GOD_POSEIDON) == 1 and blessingGod() == S.ICHOR_GOD_POSEIDON,
         string.format("praying at Poseidon's altar: his blessing and +1 Favor (%d)", favor(S.ICHOR_GOD_POSEIDON)))
  b = read("EventScript_IchorLeaveShip")
  expect(b >= 1 and L.mapId() == S.MAP_DECK, "the gangplank runs EventScript_IchorLeaveShip (the stub)")

  -- --- Down the hatch -----------------------------------------------------------------------
  L.go(6, 7)
  L.enter(K.LEFT, S.MAP_BELOW, "the hatch")
  wait(20)
  local x, y = L.pos()
  expect(L.mapId() == S.MAP_BELOW and x == 8 and y == 3, string.format("the hatch leads down to the ladder's foot (%d,%d)", x, y))
  L.beat = "below"

  -- --- Below deck with no crew --------------------------------------------------------------
  away = {}
  for _, who in ipairs(BELOW_CREW) do
    if aboard("EuploiaBelow_EventScript_" .. who) then away[#away + 1] = who end
  end
  expect(#away == 0, "no crew below before they sign on (" .. table.concat(away, ", ") .. ")")
  local cold = metatile(9, 3)
  read("EuploiaBelow_EventScript_Hearth")
  expect(blessingGod() == S.ICHOR_GOD_POSEIDON and not L.getFlag(S.FLAG_DAILY_ICHOR_SHIP_HEARTHFIRE),
         "without Lampon the hearth is cold: no Hearthfire")
  expect(not menuDuring(L.sign("EuploiaBelow_EventScript_Pithos"), "pithos_sealed"),
         "without Kydon the Pithos stays sealed")
  expect(not menuDuring(L.sign("EuploiaBelow_EventScript_Counter"), "stall_shut"),
         "without Kydon the stall sells nothing")
  local before = hauled()
  read("EuploiaBelow_EventScript_Nets")
  expect(hauled() == before and not L.getFlag(S.FLAG_DAILY_ICHOR_SHIP_NETS), "without Diktys the nets stay in their heap")
  b = read("EuploiaBelow_EventScript_IasoChest")
  expect(b >= 1, "Iaso's chest waits for a healer")

  hurt()
  L.setFlag(S.FLAG_ICHOR_SHIP_IASO_TENDED, true)
  read("EuploiaBelow_EventScript_Bunk", { shots = { "bunk_menu" } })
  expect(full() and not L.getFlag(S.FLAG_ICHOR_SHIP_IASO_TENDED),
         "resting in the bunk heals the party and clears Iaso's flag")
  local milk = L.itemCount(S.ITEM_MOOMOO_MILK)
  read("EuploiaBelow_EventScript_SeaChest")
  read("EuploiaBelow_EventScript_SeaChest")
  expect(L.itemCount(S.ITEM_MOOMOO_MILK) == milk + 3 and L.getFlag(S.FLAG_ICHOR_SHIP_SEA_CHEST),
         "Mom's sea chest: three Moomoo Milk, once")
  L.go(5, 5)
  shot("below_no_crew")

  -- --- Everyone aboard ----------------------------------------------------------------------
  setCrew(true)
  toBelow()
  away = {}
  for _, who in ipairs(BELOW_CREW) do
    if not aboard("EuploiaBelow_EventScript_" .. who) then away[#away + 1] = who end
  end
  expect(#away == 0, "with the crew signed on, all five are below (" .. table.concat(away, ", ") .. " missing)")
  expect(metatile(9, 3) ~= cold, string.format("with Lampon aboard the hearth is lit (0x%03X, cold 0x%03X)", metatile(9, 3), cold))
  L.go(12, 5)
  shot("below_crew")

  talk("EuploiaBelow_EventScript_Lampon")
  expect(blessingGod() == S.ICHOR_GOD_HESTIA and L.getFlag(S.FLAG_DAILY_ICHOR_SHIP_HEARTHFIRE),
         "Lampon's hearth gives Hestia's Hearthfire, and marks the day")
  b = talk("EuploiaBelow_EventScript_Lampon")
  expect(b >= 1 and blessingGod() == S.ICHOR_GOD_HESTIA, "once a day: the fire's banked")
  local hestia = favor(S.ICHOR_GOD_HESTIA)
  read("EuploiaBelow_EventScript_Hearth")
  expect(favor(S.ICHOR_GOD_HESTIA) == hestia + 1, string.format("the day's warmth taken, the hearth is Hestia's altar (Favor %d)",
         favor(S.ICHOR_GOD_HESTIA)))

  expect(menuDuring(L.npc("EuploiaBelow_EventScript_Kydon"), "stall") == "shop", "Kydon's stall opens across the counter")
  expect(menuDuring(L.sign("EuploiaBelow_EventScript_Pithos"), "pithos") == "menu", "Kydon's Pithos opens")

  before = hauled()
  talk("EuploiaBelow_EventScript_Diktys")
  expect(hauled() == before + 1 and L.getFlag(S.FLAG_DAILY_ICHOR_SHIP_NETS), "Diktys's haul: one sea gift, and the day marked")
  talk("EuploiaBelow_EventScript_Diktys")
  read("EuploiaBelow_EventScript_Nets")
  expect(hauled() == before + 1, "one haul a day")

  hurt()
  talk("EuploiaBelow_EventScript_Iaso")
  expect(full() and L.getFlag(S.FLAG_ICHOR_SHIP_IASO_TENDED), "Iaso tends the party")
  hurt()
  talk("EuploiaBelow_EventScript_Iaso")
  expect(not full(), "once per rest: Iaso waits for you to sleep")
  read("EuploiaBelow_EventScript_Bunk")
  expect(full() and not L.getFlag(S.FLAG_ICHOR_SHIP_IASO_TENDED), "the bunk heals and frees Iaso again")
  hurt()
  talk("EuploiaBelow_EventScript_Iaso")
  expect(full(), "after a rest Iaso tends them again")

  talk("EuploiaBelow_EventScript_Phemios", { shots = { "phemios", "phemios_2", "phemios_3" } })
  wait(60)
  expect(L.playing(S.MUS_ICHOR_ELAIA), "Phemios plays the song you pick (" .. L.song() .. ")")

  b = read("EuploiaBelow_EventScript_TrophyShelf")
  expect(b >= 1, "the trophy shelf, its seven places empty")
  local SPOTS = { { 4, 1 }, { 5, 1 }, { 6, 1 }, { 7, 1 }, { 4, 2 }, { 5, 2 }, { 6, 2 } }
  local empty = {}
  for i, p in ipairs(SPOTS) do empty[i] = metatile(p[1], p[2]) end
  L.runHeader("EuploiaTest_ShelfHeader")
  wait(10)
  local unchanged = 0
  for i, p in ipairs(SPOTS) do if metatile(p[1], p[2]) == empty[i] then unchanged = unchanged + 1 end end
  expect(unchanged == 0, string.format("the keepsake scripts put all seven keepsakes on their spots (%d unchanged)", unchanged))
  L.go(5, 3)
  shot("shelf_full")

  -- --- Up the ladder, everyone on deck ------------------------------------------------------
  L.go(8, 4)
  L.enter(K.UP, S.MAP_DECK, "the ladder")
  wait(20)
  x, y = L.pos()
  expect(L.mapId() == S.MAP_DECK and x == 5 and y == 7, string.format("the ladder comes up at the hatch (%d,%d)", x, y))
  expect(L.playing(S.MUS_ICHOR_TRIREME), "on deck the ship's own music plays again (" .. L.song() .. ")")
  L.beat = "deck_crew"
  away = {}
  for _, who in ipairs(DECK_CREW) do
    if not aboard("EuploiaDeck_EventScript_" .. who) then away[#away + 1] = who end
  end
  expect(#away == 0, "with the crew signed on, they're all on deck (" .. table.concat(away, ", ") .. " missing)")
  for _, who in ipairs({ "Oarsman1", "Lynkeus", "Glaukias", "Nolan" }) do
    b = talk("EuploiaDeck_EventScript_" .. who)
    expect(b >= 1, string.format("%s talks (%d boxes)", who, b))
  end
  shot("deck_crew_bow")
  b = talk("EuploiaDeck_EventScript_Alethea")
  expect(b >= 3, string.format("Alethea has a word about the dramatist (%d boxes)", b))
  L.go(10, 5)
  shot("deck_crew")
end)
