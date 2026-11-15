-- The sailing layer check, run by tools/ichor/tests/pg_sailing.sh (read it first).
--
-- Route 33 and the Euploia's deck are on other branches, so the ship sails Akti's
-- harbor (Ichor_PutShipAtSea), her deck is the test room MAP_PG_TEST_DECK, and
-- the Great Bear's check marks Akti an ocean route in RAM for a moment.

local L = dofile("tools/ichor/tests/pg_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local log, expect, wait, shot, tap = L.log, L.expect, L.wait, L.shot, L.tap

local SEA_X, SEA_Y = 22, 5      -- Akti's harbor: open water x 16-25 on row 5, y 0-7 on column 22
local QUAY_X, QUAY_Y = 7, 10    -- VOYAGE_AKTI's quay (src/data/ichor_voyages.h)
local GRASS_X, GRASS_Y = 10, 10 -- Route 1's tall grass by the lake

local function query()
  L.runHeader("PgSail_QueryHeader")
  return { port = L.getVar(S.VAR_0x8000), stars = L.getVar(S.VAR_0x8001), rate = L.getVar(S.VAR_0x8002),
           mooredAkti = L.getVar(S.VAR_0x8003), dir = L.getVar(S.VAR_0x8004),
           strength = L.getVar(S.VAR_0x8005), grudge = L.getVar(S.VAR_0x8006) }
end

local function setWind(dir, strength)
  L.setVar(S.VAR_0x8004, dir); L.setVar(S.VAR_0x8005, strength)
  L.runHeader("PgSail_WindHeader")
end

local function toSea(x, y, facing)
  L.setVar(S.VAR_0x8004, S.MAP_AKTI_TOWN); L.setVar(S.VAR_0x8005, x)
  L.setVar(S.VAR_0x8006, y); L.setVar(S.VAR_0x8007, facing)
  L.runHeader("PgSail_ToSeaHeader", { limit = 3000 })
  L.waitUntil(function() return L.mapId() == S.MAP_AKTI_TOWN and L.idle() end, 3000, "the ship at sea")
  wait(20)
end

local function inShip()
  local g = L.graphicsId()
  return L.surfing() and L.getFlag(S.FLAG_ICHOR_ON_SHIP) and (g == S.ICHOR_SHIP_GFX or g == S.ICHOR_SHIP_GFX_SLACK)
end

local function blobHidden()
  local id = emu:read8(L.playerObject() + S.OFF_OBJ_FIELD_EFFECT_SPRITE)
  local flags = emu:read16(L.sprite(id) + S.OFF_SPRITE_FLAGS)
  return flags & S.SPRITE_FLAG_INVISIBLE ~= 0
end

-- The follower, if any, is hidden (FOLLOWER_INVISIBLE_FLAGS includes surfing).
local function followerStowed()
  for i = 0, S.OBJECT_EVENTS_COUNT - 1 do
    local o = S.gObjectEvents + i * S.OBJECT_EVENT_SIZE
    if emu:read8(o) & 1 == 1 and emu:read8(o + S.OFF_OBJ_LOCAL_ID) == S.OBJ_EVENT_ID_FOLLOWER then
      return emu:read8(o + 1) & 0x20 ~= 0     -- invisible
    end
  end
  return true
end

local DIR_OF = { [K.LEFT] = 3, [K.RIGHT] = 4, [K.UP] = 2, [K.DOWN] = 1 }

-- Turn to face `key` without moving (a short tap from rest only turns).
local function face(key)
  if L.facing() ~= DIR_OF[key] then tap(key, 1); wait(10) end
  L.waitUntil(L.idle, 120, "the turn")
end

-- Hold `key` from rest until the ship has started her `tiles`-th tile. Returns the
-- frames that took after the first step began ((tiles - 1) whole steps), the
-- first step's movement action and the graphics during it.
local function sail(key, tiles)
  local x0, y0 = L.pos()
  local function moved() local x, y = L.pos(); return math.abs(x - x0) + math.abs(y - y0) end
  emu:addKey(key)
  local t0, action, gfx
  for _ = 1, 600 do
    L.frame()
    local m = moved()
    if m >= 1 and not t0 then t0 = L.now(); action = L.movementAction(); gfx = L.graphicsId() end
    if m >= tiles then break end
  end
  emu:clearKey(key)
  local frames = L.now() - (t0 or L.now())
  for _ = 1, 300 do
    if L.idle() then break end
    L.frame()
  end
  if not L.idle() then
    shot("stuck_sailing")
    L.fail("the ship never stopped: " .. L.where() .. string.format(" avatar flags %02x tile %d",
           emu:read8(S.gPlayerAvatar), emu:read8(S.gPlayerAvatar + 3)))
  end
  wait(4)
  return frames, action, gfx
end

-- Open the Relic Ring on the entry whose cursor value is `cursor`, and take it.
local function ring(cursor)
  emu:write8(L.ichor() + S.OFF_ICHOR_RING_CURSOR, cursor)
  tap(K.SELECT)
  L.pickMenu(0, "the Relic Ring")
end

-- Walk Route 1's grass until `n` wild battles have been run from; count the
-- shades among them (the opponent's species as the battle's first menu opens).
local function hunt(n, stopAtShade)
  local fought, shades, steps = 0, 0, 0
  local key = K.RIGHT
  while fought < n do
    local r = L.step(key)
    key = (key == K.RIGHT) and K.LEFT or K.RIGHT
    steps = steps + 1
    if steps > 4000 then L.fail("no wild battles in Route 1's grass") end
    if r == "taken" then
      local t0 = L.now()
      while not (L.inBattle() and emu:read32(S.gBattlerControllerFuncs) == (S.HandleInputChooseAction | 1)) do
        if L.now() - t0 > 2000 then
          shot("stuck_hunt")
          L.fail("no wild battle's menu after a step on Route 1: " .. L.where())
        end
        if L.idle() and L.now() - t0 > 120 then break end   -- not a battle after all
        if L.inBattle() then tap(K.A) else L.frame() end      -- through "You encountered a wild..."
      end
      if not L.inBattle() then goto continue end
      local species = emu:read16(S.gBattleMons + S.BATTLEMON_SIZE + S.OFF_BATTLEMON_SPECIES)
      if species == S.SPECIES_OBOLORN then shades = shades + 1 end
      L.battle()
      L.waitUntil(L.idle, 1200, "the field after the battle")
      wait(10)
      fought = fought + 1
      if stopAtShade and shades > 0 then break end
    end
    ::continue::
  end
  return fought, shades
end

L.start(function()
  -- 1. The post-game, ready on Akti's quay
  L.pgStart(QUAY_X, QUAY_Y)
  L.day()
  wait(30)
  expect(L.mapId() == S.MAP_AKTI_TOWN and L.timeOfDay() == S.TIME_DAY, "the post-game is ready on Akti's quay, by day")
  do
    local zero = true
    for i = 0, S.ICHOR_EPICS_SIZE - 1 do
      if i ~= S.OFF_EPICS_WIND and emu:read8(L.epics() + i) ~= 0 then zero = false end
    end
    expect(S.OFF_ICHOR_EPICS == 0x450 and S.ICHOR_EPICS_SIZE == 64 and S.OFF_ICHOR_RESERVED == 0x490 and zero,
           "IchorEpics: 64 bytes at 0x450, zero in a new game (but the day's wind); reserved now at 0x490")
  end
  local q = query()
  expect(q.port == S.VOYAGE_AKTI and q.mooredAkti == 1,
         "a ship nobody has sailed waits at Akti (Ichor_GetShipPort, Ichor_IsMooredAt)")

  -- 2. Board at Akti's gangplank: Akti has no sea map, so onto the deck, moored
  L.runHeader("PgSail_BoardHeader", { answers = { "yes" }, limit = 4000 })
  L.waitUntil(function() return L.mapId() == S.ICHOR_SHIP_DECK_MAP and L.idle() end, 3000, "the deck")
  wait(20)
  shot("deck_moored_at_akti")
  local x, y = L.pos()
  expect(x == S.ICHOR_SHIP_DECK_X and y == S.ICHOR_SHIP_DECK_Y and L.facing() == S.DIR_NORTH,
         string.format("boarding puts you on the deck at (%d,%d), facing the bow", x, y))
  expect(not L.getFlag(S.FLAG_ICHOR_ON_SHIP) and L.epic8("SHIP_PORT") == S.VOYAGE_AKTI,
         "moored at Akti (IchorEpics.shipPort), not under way")

  -- The helm, moored at a port with no sea: THE WIND?, then SET A COURSE with nowhere to go
  setWind(S.ICHOR_WIND_W, S.ICHOR_WIND_FRESH)
  L.runHeader("PgSail_HelmHeader", { noSettle = true })
  L.waitUntil(function() return L.taskRunning("Task_HandleScrollingMultichoiceInput") end, 600, "the helm's menu")
  wait(10)
  shot("helm_menu_moored")
  L.pickMenu(1, "THE WIND?")                         -- SET A COURSE, THE WIND?, STAY
  wait(40)
  shot("helm_the_wind")
  expect(L.textContains(S.gStringVar4, "fresh wind") and L.textContains(S.gStringVar4, "west"),
         "THE WIND?: Nausikles names the day's wind")
  L.settle()
  L.runHeader("PgSail_HelmHeader", { noSettle = true })
  L.pickMenu(0, "SET A COURSE")
  wait(40)
  expect(L.textContains(S.gStringVar4, "Nowhere else to go"), "SET A COURSE moored at Akti: no other port is open yet")
  L.settle()

  -- 3. The deck's gangplank, back to the quay
  L.runHeader("PgSail_LeaveHeader", { answers = { "yes" }, limit = 4000 })
  L.waitUntil(function() return L.mapId() == S.MAP_AKTI_TOWN and L.idle() end, 3000, "Akti")
  x, y = L.pos()
  expect(x == QUAY_X and y == QUAY_Y and L.epic8("SHIP_PORT") == S.VOYAGE_AKTI,
         string.format("the gangplank leads back to Akti's quay (%d,%d)", x, y))

  -- 4. The ship at sea, in Akti's harbor
  setWind(S.ICHOR_WIND_E, S.ICHOR_WIND_FRESH)      -- from the east: heading west runs before it
  toSea(SEA_X, SEA_Y, S.DIR_WEST)
  x, y = L.pos()
  expect(x == SEA_X and y == SEA_Y and L.facing() == S.DIR_WEST and inShip(),
         string.format("Ichor_PutShipAtSea: in the ship at (%d,%d), facing west", x, y))
  expect(L.graphicsId() == S.ICHOR_SHIP_GFX, "running before the wind the sail is full (ICHOR_SHIP_GFX)")
  expect(blobHidden() and followerStowed(), "no surf blob under the ship, and the follower is stowed")
  expect(L.epic8("SHIP_PORT") == S.VOYAGE_NONE and query().port == S.VOYAGE_NONE, "at sea she's moored nowhere")
  shot("ship_at_sea_downwind")

  -- Speed and sail by heading (frames for three whole steps)
  local f, act, gfx = sail(K.LEFT, 4)
  log(string.format("downwind: %d frames for 3 tiles, action %d", f, act))
  expect(act == S.MOVEMENT_ACTION_RIDE_WATER_CURRENT_LEFT and gfx == S.ICHOR_SHIP_GFX and f <= 20,
         string.format("downwind: one step faster than rowing (%d frames for 3 tiles), sail full", f))
  f, act, gfx = sail(K.RIGHT, 4)
  log(string.format("upwind: %d frames for 3 tiles, action %d", f, act))
  expect(act == S.MOVEMENT_ACTION_WALK_FAST_RIGHT and gfx == S.ICHOR_SHIP_GFX_SLACK and f >= 22,
         string.format("upwind: the surf speed (%d frames for 3 tiles), sail slack", f))
  shot("ship_upwind_slack")
  f, act, gfx = sail(K.UP, 3)
  expect(act == S.MOVEMENT_ACTION_WALK_FAST_UP and gfx == S.ICHOR_SHIP_GFX,
         "crosswind: the surf speed, sail full")
  sail(K.DOWN, 3)
  setWind(S.ICHOR_WIND_E, S.ICHOR_WIND_CALM)
  f, act, gfx = sail(K.LEFT, 2)
  expect(act == S.MOVEMENT_ACTION_WALK_FAST_LEFT and gfx == S.ICHOR_SHIP_GFX_SLACK, "a calm: rowing, sail slack")
  setWind(S.ICHOR_WIND_E, S.ICHOR_WIND_FRESH)
  L.setFlag(S.FLAG_ICHOR_SHIP_SAIL, true)
  f, act = sail(K.LEFT, 4)
  log(string.format("downwind with the new sail: %d frames for 3 tiles", f))
  expect(act == S.MOVEMENT_ACTION_WALK_FASTER_LEFT and f <= 14,
         string.format("the new sail: one step faster again downwind (%d frames for 3 tiles)", f))
  L.setFlag(S.FLAG_ICHOR_SHIP_SAIL, false)
  sail(K.RIGHT, 6)
  x, y = L.pos()
  expect(x == SEA_X and y == SEA_Y, string.format("back at (%d,%d)", x, y))

  -- A strong wind behind her: the first step from rest carries her a tile further
  face(K.LEFT)
  tap(K.LEFT, 2)
  L.waitUntil(L.idle, 300, "the step"); wait(10)
  x = L.pos()
  expect(x == SEA_X - 1, string.format("a fresh wind: one tap, one tile (x %d)", x))
  setWind(S.ICHOR_WIND_E, S.ICHOR_WIND_STRONG)
  tap(K.LEFT, 2)
  L.waitUntil(L.idle, 300, "the step"); wait(10)
  x = L.pos()
  expect(x == SEA_X - 3, string.format("a strong wind behind: one tap, two tiles (x %d)", x))
  setWind(S.ICHOR_WIND_E, S.ICHOR_WIND_FRESH)
  sail(K.RIGHT, 3)

  -- The encounter rate, by heading
  face(K.LEFT); local down = query().rate
  face(K.RIGHT); local up = query().rate
  face(K.UP); local cross = query().rate
  expect(down == 50 and up == 150 and cross == 100,
         string.format("encounters at sea: x%d%% downwind, x%d%% upwind, x%d%% crosswind", down, up, cross))

  -- Poseidon's grudge: the wind turns against any heading
  face(K.LEFT)
  L.runHeader("PgSail_GrudgeHeader")
  expect(L.graphicsId() == S.ICHOR_SHIP_GFX_SLACK and query().grudge == 1 and query().rate == 150,
         "Poseidon's grudge: heading west into an east wind is upwind now, sail slack")
  f, act = sail(K.LEFT, 2)
  expect(act == S.MOVEMENT_ACTION_WALK_FAST_LEFT, "... and she rows")
  L.runHeader("PgSail_LiftGrudgeHeader")
  expect(L.graphicsId() == S.ICHOR_SHIP_GFX and query().grudge == 0, "a special lifts the grudge")
  sail(K.RIGHT, 2)

  -- The ship goes ashore only at a landing
  sail(K.RIGHT, 3)
  x, y = L.pos()
  local r = L.step(K.RIGHT)
  expect(r == "blocked" and inShip(), string.format("from (%d,%d) the ship won't run up the beach", x, y))
  sail(K.LEFT, 3)

  -- The start menu's wind line
  tap(K.START)
  L.waitUntil(function() return L.taskRunning("Task_ShowStartMenu") or not L.idle() end, 120, "the start menu")
  wait(30)
  shot("start_menu_wind")
  do
    local id = emu:read8(S.sIchorBlessingWindowId)
    local w = S.gWindows + id * S.WINDOW_SIZE
    local width, height = emu:read8(w + S.OFF_WINDOW_WIDTH), emu:read8(w + S.OFF_WINDOW_HEIGHT)
    tap(K.B); L.waitUntil(L.idle, 300, "the start menu to close"); wait(10)
    q = query()
    expect(id ~= 0 and width == S.ICHOR_WIND_PANEL_WIDTH and height == 2 and L.textAt(S.gStringVar1, "east, fresh"),
           "the start menu's info panel shows the wind at sea (\"Wind: east, fresh\")")
  end

  -- 5. DECK and TAKE HER OUT
  face(K.UP)
  local sx, sy, sf = L.pos(); sf = L.facing()
  ring(S.RING_DECK_CURSOR)
  L.waitUntil(function() return L.mapId() == S.ICHOR_SHIP_DECK_MAP and L.idle() end, 3000, "the deck from the sea")
  wait(20)
  shot("below_deck_from_sea")
  expect(L.epic8("SEA_MAP_GROUP") * 256 + L.epic8("SEA_MAP_NUM") == S.MAP_AKTI_TOWN
         and L.epic8("SEA_X") == sx and L.epic8("SEA_Y") == sy and L.epic8("SEA_FACING") == sf
         and L.getFlag(S.FLAG_ICHOR_ON_SHIP),
         "DECK: the sea, the tile and the heading are saved, and she's still under way")
  L.runHeader("PgSail_HelmHeader", { noSettle = true })
  L.waitUntil(function() return L.taskRunning("Task_HandleScrollingMultichoiceInput") end, 600, "the helm's menu")
  wait(10)
  shot("helm_menu_at_sea")
  L.pickMenu(0, "TAKE HER OUT")
  L.settle({ limit = 4000 })
  L.waitUntil(function() return L.mapId() == S.MAP_AKTI_TOWN and L.idle() end, 3000, "back at sea")
  wait(20)
  x, y = L.pos()
  expect(x == sx and y == sy and L.facing() == sf and inShip(),
         string.format("TAKE HER OUT: back on the same tile (%d,%d) and heading, in the ship", x, y))
  shot("take_her_out")

  -- 6. SET A COURSE from below deck: the crossing to Akti's quay
  ring(S.RING_DECK_CURSOR)
  L.waitUntil(function() return L.mapId() == S.ICHOR_SHIP_DECK_MAP and L.idle() end, 3000, "the deck")
  L.runHeader("PgSail_HelmHeader", { noSettle = true })
  L.pickMenu(1, "SET A COURSE")                     -- TAKE HER OUT, SET A COURSE, ...
  L.waitUntil(function() return L.taskRunning("Task_HandleScrollingMultichoiceInput") end, 600, "the ports")
  wait(10)
  shot("set_a_course_ports")
  L.pickMenu(0, "AKTI")
  wait(40)
  shot("crossing_line")
  expect(L.textContains(S.gStringVar4, "Home to Akti"), "the crossing: Nausikles's line for Akti")
  L.settle({ limit = 4000 })
  L.waitUntil(function() return L.mapId() == S.MAP_AKTI_TOWN and L.idle() end, 3000, "Akti after the crossing")
  x, y = L.pos()
  expect(x == QUAY_X and y == QUAY_Y and not L.getFlag(S.FLAG_ICHOR_ON_SHIP) and L.epic8("SHIP_PORT") == S.VOYAGE_AKTI,
         string.format("SET A COURSE lands you on Akti's quay (%d,%d), moored there", x, y))
  shot("crossing_landed")

  -- 7. A landing on a sea map (EventScript_IchorLand)
  toSea(SEA_X, SEA_Y, S.DIR_WEST)
  L.runHeader("PgSail_LandHeader", { answers = { "yes" }, limit = 4000 })
  L.waitUntil(function() return L.mapId() == S.MAP_AKTI_TOWN and L.idle() end, 3000, "ashore")
  x, y = L.pos()
  expect(x == QUAY_X and y == QUAY_Y and not L.surfing() and not L.getFlag(S.FLAG_ICHOR_ON_SHIP)
         and L.epic8("SHIP_PORT") == S.VOYAGE_AKTI,
         "\"Go ashore at Akti?\": the quay, ship mode off, moored at Akti")

  -- 8. The Wings refuse at sea
  toSea(SEA_X, SEA_Y, S.DIR_WEST)
  L.setFlag(S.FLAG_ICHOR_AT_SEA, true)
  ring(S.ITEM_DAEDALUS_WINGS - S.ICHOR_RELIC_FIRST + 1)  -- FLY
  wait(40)
  shot("wings_at_sea")
  expect(L.textContains(S.gStringVar4, "No herm out here") and not L.on("CB2_FlyMap"),
         "past Maleia the Wings refuse: \"No herm out here. The sea has no roads.\"")
  L.settle()
  L.setFlag(S.FLAG_ICHOR_AT_SEA, false)

  -- 9. The Great Bear at night, on a sea map, in the ship
  L.night()
  wait(10)
  expect(L.findSprite("Ichor_SpriteCB_GreatBear") == nil, "no stars over a town's harbor")
  emu:write8(S.gMapHeader + S.OFF_MAPHEADER_MAPTYPE, S.MAP_TYPE_OCEAN_ROUTE)
  wait(10)
  local bear = L.findSprite("Ichor_SpriteCB_GreatBear")
  local by = bear and emu:read16(L.sprite(bear) + S.OFF_SPRITE_Y)
  expect(L.timeOfDay() == S.TIME_NIGHT and bear ~= nil and L.spriteVisible(bear) and by < 40 and query().stars == 1,
         "at night on a sea map the Great Bear hangs at the top of the screen (Ichor_IsStarsOut)")
  shot("great_bear_night")
  sail(K.LEFT, 2)
  bear = L.findSprite("Ichor_SpriteCB_GreatBear")
  expect(bear ~= nil and emu:read16(L.sprite(bear) + S.OFF_SPRITE_Y) == by, "... fixed to north as she sails")
  L.day()
  wait(10)
  expect(L.findSprite("Ichor_SpriteCB_GreatBear") == nil and query().stars == 0, "by day the stars are gone")
  emu:write8(S.gMapHeader + S.OFF_MAPHEADER_MAPTYPE, S.MAP_TYPE_TOWN)

  -- 10. The daily wind
  local function expectedWind(seed, keep)
    local roll = ((seed >> 11) ~ (seed >> 23)) % 100
    local s = roll < 20 and 0 or (roll < 75 and 1 or 2)
    if keep & S.ICHOR_WIND_GRUDGE_BIT ~= 0 then s = 2 end
    return keep | ((seed >> 3) & 7) | (s << S.ICHOR_WIND_STRENGTH_SHIFT)
  end
  L.setEpic8("WIND", 0)
  L.newDay()
  local seed = emu:read32(L.sb1() + S.OFF_SB1_DAILY_SEED)
  local wind = L.epic8("WIND")
  expect(wind == expectedWind(seed, 0),
         string.format("a new day rolls the wind from the daily seed (0x%02x)", wind))
  L.setEpic8("WIND", S.ICHOR_WIND_GRUDGE_BIT)
  L.newDay()
  seed = emu:read32(L.sb1() + S.OFF_SB1_DAILY_SEED)
  wind = L.epic8("WIND")
  expect(wind == expectedWind(seed, S.ICHOR_WIND_GRUDGE_BIT) and (wind >> S.ICHOR_WIND_STRENGTH_SHIFT) & 3 == 2,
         "the grudge holds through the night, and every day it blows strong")
  L.setVar(S.VAR_0x8004, S.ICHOR_WIND_N); L.setVar(S.VAR_0x8005, S.ICHOR_WIND_BECALMED)
  L.runHeader("PgSail_WindHeader")
  L.runHeader("PgSail_LiftGrudgeHeader")
  L.newDay()
  q = query()
  expect(L.epic8("WIND") & S.ICHOR_WIND_BECALMED_BIT ~= 0 and q.strength == S.ICHOR_WIND_CALM,
         "an event calm (ICHOR_WIND_BECALMED) outlasts the daily reset")
  setWind(S.ICHOR_WIND_E, S.ICHOR_WIND_FRESH)
  expect(L.epic8("WIND") & S.ICHOR_WIND_BECALMED_BIT == 0, "... until Ichor_SetWind gives a real wind")

  -- 11. Save at sea and reload: the epics and the ship come back
  L.setEpic16("CREW", 0x0155); L.setEpic16("LABORS_DONE", 0x0ABC); L.setEpic16("KLEOS", 0x0FFF)
  local before = L.epicsBytes()
  L.saveAndReload()
  wait(20)
  shot("reloaded_at_sea")
  expect(L.epicsBytes() == before, "save and reload keep all 64 bytes of IchorEpics")
  expect(inShip() and blobHidden(), "and you wake at sea in the ship, with no surf blob")
  L.setEpic16("CREW", 0); L.setEpic16("LABORS_DONE", 0); L.setEpic16("KLEOS", 0)

  -- 12. Shades on the roads: Route 1 by night
  L.setFlag(S.FLAG_ICHOR_ON_SHIP, false)
  L.warp(S.MAP_KALLISTE_ROUTE1, GRASS_X, GRASS_Y)
  L.encounters(true)
  L.day()
  local fought, shades = hunt(8, false)
  expect(fought == 8 and shades == 0, string.format("by day no shades on Route 1 (%d of %d)", shades, fought))
  L.night()
  fought, shades = hunt(48, true)
  expect(shades == 1, string.format("by night a gray Obolorn walks Route 1 (the first after %d battles)", fought))
  shot("shade_on_route1")
  L.setPostgame(false)
  fought, shades = hunt(12, false)
  expect(shades == 0, string.format("before the post-game, none (%d of %d)", shades, fought))
  L.setPostgame(true)
  L.encounters(false)
end)
