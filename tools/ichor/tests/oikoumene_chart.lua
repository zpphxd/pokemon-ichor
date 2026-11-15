-- The Oikoumene chart check, run by tools/ichor/tests/oikoumene_chart.sh (read it first).

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local log, expect, wait, shot, tap = L.log, L.expect, L.wait, L.shot, L.tap
for k, v in pairs(dofile(L.OUT .. "chart_symbols.lua")) do S[k] = v end

local LAND_X, LAND_Y = 3, 23      -- batch 1's placeholder heal tile in every town
local AKTI_X, AKTI_Y = 3, 23      -- HEAL_LOCATION_AKTI_TOWN

local function bgr(r, g, b) return (r >> 3) | ((g >> 3) << 5) | ((b >> 3) << 10) end
local function bgColor(i) return emu:read16(S.gPlttBufferUnfaded + i * 2) & 0x7FFF end
local OIK_OCEAN = bgr(88, 32, 64)       -- the Oikoumene chart's colour 4 (ui_oikoumene_map.py)
local AETHOS_INK = bgr(32, 24, 24)      -- the Aethos chart's colour 4 (ui_world_map.py)
local TROAD_FACE = bgr(224, 208, 168)   -- popup palettes, colour 4 (ui_oikoumene_popups.py)
local PAPYRUS_FACE = bgr(232, 216, 160)

local function mapsec() return emu:read8(S.gMapHeader + S.OFF_MAPHEADER_MAPSEC) end
local function chart() return L.getVar(S.VAR_ICHOR_OIK_CHART) end
local function rm() return emu:read32(S.sFlyMap) + S.OFF_FLYMAP_REGIONMAP end
local function cursorSec() return emu:read16(rm() + S.OFF_RM_MAPSEC) end
local function cursorType() return emu:read8(rm() + S.OFF_RM_MAPSECTYPE) end
local function cursorAt() return emu:read16(rm() + S.OFF_RM_CURSOR_X) - 1, emu:read16(rm() + S.OFF_RM_CURSOR_Y) - 2 end

-- fly-target sprites for a section: all of them, and the lit (flyable) ones
local function targets(sec)
  local all, lit = 0, 0
  for i = 0, S.MAX_SPRITES - 1 do
    local sp = S.gSprites + i * S.SPRITE_SIZE
    if emu:read32(sp + S.OFF_SPRITE_TEMPLATE) == S.sFlyDestIconSpriteTemplate
       and emu:read16(sp + S.OFF_SPRITE_DATA0) == sec then
      all = all + 1
      if emu:read32(sp + S.OFF_SPRITE_CALLBACK) & ~1 == S.SpriteCB_FlyDestIcon then lit = lit + 1 end
    end
  end
  return all, lit
end

local function give(item, n)
  L.setVar(S.VAR_0x8004, item); L.setVar(S.VAR_0x8005, n or 1)
  L.runHeader("ChartTest_GiveHeader")
end
local function goTo(header, map, what)
  L.runHeader(header, { limit = 4000 })
  L.waitUntil(function() return L.mapId() == map and L.idle() end, 3000, what)
  wait(90)                                  -- the map-name popup has loaded its stone by now
end
local function openFlyMap()
  tap(K.SELECT)
  L.waitUntil(function() return L.taskRunning("Task_HandleScrollingMultichoiceInput") end, 300, "the Relic Ring")
  wait(20); tap(K.A)                        -- FLY
  L.waitUntil(function() return L.on("CB2_FlyMap") end, 600, "the fly map")
  wait(90)
end
local function closeFlyMap(map)
  tap(K.B)
  L.waitUntil(function() return L.mapId() == map and L.inOverworld() and L.idle() end, 2000, "back in the field")
  wait(30)
end
local function moveCursor(key, n)
  for _ = 1, n do tap(key); wait(14) end
  wait(10)
end
local function flyHere(map, what)
  tap(K.A)
  L.waitUntil(function() return L.mapId() == map and L.idle() end, 4000, what)
  wait(30)
end

L.start(function()
  L.quickstart()
  L.setVar(S.VAR_0x8008, 14); L.setVar(S.VAR_0x8009, 20)
  L.runHeader("ChartTest_SetupHeader", { limit = 4000 })
  L.waitUntil(function() return L.mapId() == S.MAP_SESTOS and L.idle() end, 3000, "Sestos")
  wait(90)

  -- On Oikoumene ground
  expect(mapsec() == S.MAPSEC_SESTOS, string.format("Sestos is its own section (%d)", mapsec()))
  expect(bgColor(224 + 4) == TROAD_FACE,
         string.format("the map-name popup is Ilion's limestone (colour %04x)", bgColor(224 + 4)))
  expect(chart() == (1 << 2), string.format("Sestos marks the chart: visited, and the last port (%04x)", chart()))
  shot("sestos_popup")
  give(S.ITEM_DAEDALUS_WINGS, 1)

  -- The Fly map, before you've arrived: the Oikoumene's chart, AETHOS hidden
  openFlyMap()
  expect(bgColor(112 + 4) == OIK_OCEAN,
         string.format("the Fly map loads the Oikoumene chart (colour %04x)", bgColor(112 + 4)))
  local x, y = cursorAt()
  expect(cursorSec() == S.MAPSEC_SESTOS and x == 13 and y == 6 and cursorType() == S.MAPSECTYPE_CITY_CANFLY,
         string.format("the cursor starts on Sestos, (13,6), a town you can fly to (sec %d at %d,%d type %d)",
                       cursorSec(), x, y, cursorType()))
  shot("fly_map_oikoumene_before_crossing")
  local all = targets(S.MAPSEC_AETHOS)
  expect(all == 0, string.format("no AETHOS target before you've arrived (%d)", all))
  moveCursor(K.LEFT, 1)
  expect(cursorSec() == S.MAPSEC_HELLESPONT, string.format("west of Sestos is the Hellespont (%d)", cursorSec()))
  moveCursor(K.LEFT, 1)
  expect(cursorSec() == S.MAPSEC_NONE, string.format("the Aethos inlay is unnamed before you've arrived (%d)", cursorSec()))
  closeFlyMap(S.MAP_SESTOS)

  -- The Aethos chart, before: THE OIKOUMENE hidden in the fog
  goTo("ChartTest_AktiHeader", S.MAP_AKTI, "Akti")
  expect(chart() == (1 << 2), string.format("Aethos leaves the chart's state alone (%04x)", chart()))
  openFlyMap()
  expect(bgColor(112 + 4) == AETHOS_INK, string.format("in Aethos the Fly map is Aethos's (colour %04x)", bgColor(112 + 4)))
  all = targets(S.MAPSEC_THE_OIKOUMENE)
  expect(all == 0, string.format("no THE OIKOUMENE target before you've arrived (%d)", all))
  moveCursor(K.RIGHT, 4); moveCursor(K.UP, 2)
  x, y = cursorAt()
  expect(x == 27 and y == 5 and cursorSec() == S.MAPSEC_NONE,
         string.format("the fog at (27,5) is unnamed before you've arrived (sec %d at %d,%d)", cursorSec(), x, y))
  closeFlyMap(S.MAP_AKTI)

  -- Arrived. THE OIKOUMENE shows, and lands at the last port: Sestos
  L.setFlag(S.FLAG_ICHOR_OIKOUMENE_ARRIVED, true)
  openFlyMap()
  local lit
  all, lit = targets(S.MAPSEC_THE_OIKOUMENE)
  expect(all == 1 and lit == 1, string.format("THE OIKOUMENE is a lit target once you've arrived (%d, %d lit)", all, lit))
  moveCursor(K.RIGHT, 4); moveCursor(K.UP, 2)
  expect(cursorSec() == S.MAPSEC_THE_OIKOUMENE and cursorType() == S.MAPSECTYPE_CITY_CANFLY,
         string.format("the cursor names THE OIKOUMENE in the fog (sec %d type %d)", cursorSec(), cursorType()))
  shot("fly_map_aethos_the_oikoumene")
  flyHere(S.MAP_SESTOS, "the crossing to Sestos")
  x, y = L.pos()
  expect(x == LAND_X and y == LAND_Y, string.format("THE OIKOUMENE lands at Sestos's heal tile (%d,%d)", x, y))

  -- AETHOS at the centre of the Oikoumene chart lands at Akti
  openFlyMap()
  all, lit = targets(S.MAPSEC_AETHOS)
  expect(all == 1 and lit == 1, string.format("AETHOS is a lit target once you've arrived (%d, %d lit)", all, lit))
  moveCursor(K.LEFT, 2)
  expect(cursorSec() == S.MAPSEC_AETHOS and cursorType() == S.MAPSECTYPE_CITY_CANFLY,
         string.format("the cursor names AETHOS on the inlay (sec %d type %d)", cursorSec(), cursorType()))
  shot("fly_map_oikoumene_aethos")
  flyHere(S.MAP_AKTI, "the crossing to Akti")
  x, y = L.pos()
  expect(x == AKTI_X and y == AKTI_Y, string.format("AETHOS lands outside Akti's Asclepeion (%d,%d)", x, y))

  -- Naukratis becomes the last port; the crossing follows it
  goTo("ChartTest_NaukratisHeader", S.MAP_NAUKRATIS, "Naukratis")
  expect(bgColor(224 + 4) == PAPYRUS_FACE,
         string.format("Egypt's map-name popup is papyrus (colour %04x)", bgColor(224 + 4)))
  expect(chart() == ((1 << 2) | (1 << 4) | 1),
         string.format("Naukratis marks the chart: visited, and port 1 (%04x)", chart()))
  shot("naukratis_popup")
  goTo("ChartTest_AktiHeader", S.MAP_AKTI, "Akti again")
  openFlyMap()
  moveCursor(K.RIGHT, 4); moveCursor(K.UP, 2)
  flyHere(S.MAP_NAUKRATIS, "the crossing to Naukratis")
  x, y = L.pos()
  expect(x == LAND_X and y == LAND_Y, string.format("THE OIKOUMENE now lands at Naukratis (%d,%d)", x, y))

  -- Battle music on Oikoumene ground: Ichor's themes, never FRLG's Kanto ones
  L.runHeader("ChartTest_WildHeader", { noSettle = true })
  local rec = L.battle()
  expect(rec.song == L.songHeader(S.MUS_ICHOR_BATTLE_WILD) and rec.song ~= L.songHeader(S.MUS_RG_VS_WILD),
         "a wild battle in the Oikoumene plays Ichor's wild theme: " .. L.songName(rec.song))
  L.waitUntil(L.idle, 2000, "the field after the wild battle")
  L.runHeader("ChartTest_TrainerHeader", { noSettle = true })
  rec = L.battle()
  expect(rec.song == L.songHeader(S.MUS_ICHOR_BATTLE_TRAINER) and rec.song ~= L.songHeader(S.MUS_RG_VS_TRAINER),
         "a trainer battle in the Oikoumene plays the Oikoumene theme's stand-in: " .. L.songName(rec.song))
end)
