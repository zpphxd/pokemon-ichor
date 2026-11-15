-- Herm waystones check, run by tools/ichor/tests/ichor_herms.sh (read it first).

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local log, expect, wait, shot, tap, settle = L.log, L.expect, L.wait, L.shot, L.tap, L.settle

local LAND_X, LAND_Y = 14, 21   -- south of Route 1's fork herm (src/data/ichor_herms.h)
local function hermFlag(h) return S.FLAG_ICHOR_HERMS_START + h end
local function hermes() return emu:read8(L.ichor() + S.OFF_ICHOR_FAVOR + S.ICHOR_GOD_HERMES) end
local function give(item, n)
  L.setVar(S.VAR_0x8004, item); L.setVar(S.VAR_0x8005, n or 1)
  L.runHeader("HermTest_GiveHeader")
end
local function herm(name, answers)
  L.runHeader("HermTest_HermHeader", { answers = answers })
  shot(name)
end

L.start(function()
  L.quickstart()
  L.setVar(S.VAR_0x8008, LAND_X); L.setVar(S.VAR_0x8009, LAND_Y + 1)
  L.runHeader("HermTest_SetupHeader", { limit = 4000 })
  L.waitUntil(function() return L.mapId() == S.MAP_ROUTE1 and L.idle() end, 3000, "Route 1")
  wait(40)

  herm("no_oil")
  expect(not L.getFlag(hermFlag(S.HERM_KALLISTE_ROUTE_1)), "without olive oil the herm stays dry")

  give(S.ITEM_OLIVE_OIL, 2)
  herm("anointed", { "yes" })
  expect(L.getFlag(hermFlag(S.HERM_KALLISTE_ROUTE_1)) and L.itemCount(S.ITEM_OLIVE_OIL) == 1 and hermes() == 1,
         string.format("anointing takes one oil (%d left) and gives Hermes +1 (%d)", L.itemCount(S.ITEM_OLIVE_OIL), hermes()))
  herm("again")
  expect(L.itemCount(S.ITEM_OLIVE_OIL) == 1 and hermes() == 1, "an anointed herm takes no more oil")

  -- Daedalus's Wings, from Akti back to the herm
  give(S.ITEM_DAEDALUS_WINGS, 1)
  L.runHeader("HermTest_AktiHeader", { limit = 4000 })
  L.waitUntil(function() return L.mapId() == S.MAP_AKTI and L.idle() end, 3000, "Akti")
  wait(60)
  tap(K.SELECT)
  L.waitUntil(function() return L.taskRunning("Task_HandleScrollingMultichoiceInput") end, 300, "the Relic Ring")
  wait(20); tap(K.A)                                     -- FLY
  L.waitUntil(function() return L.on("CB2_FlyMap") end, 600, "the fly map")
  wait(90)
  shot("fly_map_with_herm")
  local dots = 0
  for i = 0, S.MAX_SPRITES - 1 do
    local sp = S.gSprites + i * S.SPRITE_SIZE
    if emu:read32(sp + S.OFF_SPRITE_CALLBACK) & ~1 == S.SpriteCB_FlyDestIcon  -- Thumb bit off
       and emu:read16(sp + S.OFF_SPRITE_DATA0) == S.MAPSEC_KALLISTE_ROUTE_1 then dots = dots + 1 end
  end
  expect(dots == 1, string.format("the fly map lights the anointed herm's route (%d dot)", dots))
  local fly = emu:read32(S.sFlyMap)
  local rm = fly + S.OFF_FLYMAP_REGIONMAP
  emu:write16(rm + S.OFF_RM_MAPSEC, S.MAPSEC_KALLISTE_ROUTE_1)      -- the cursor on Route 1
  emu:write8(rm + S.OFF_RM_MAPSECTYPE, S.MAPSECTYPE_CITY_CANFLY)
  tap(K.A)
  L.waitUntil(function() return L.mapId() == S.MAP_ROUTE1 and L.idle() end, 4000, "the flight to Route 1")
  wait(30)
  shot("landed")
  local x, y = L.pos()
  expect(x == LAND_X and y == LAND_Y, string.format("the Wings land south of the herm (%d,%d)", x, y))

  -- The last herm: Hermes +10, and the herald's-staff stamp's flag
  for h = 0, S.HERM_COUNT - 1 do L.setFlag(hermFlag(h), h ~= S.HERM_KALLISTE_ROUTE_1) end
  herm("last", { "yes" })
  expect(L.getFlag(S.FLAG_ICHOR_ALL_HERMS_REWARD) and hermes() == 12,
         string.format("the last herm: Hermes +10 more (%d) and the all-herms flag", hermes()))
end)
