-- Aegina Town check, run by tools/ichor/tests/aegina_town.sh (read it first).
--
-- Env: AEGINA_OUT is the screenshot folder; AEGINA_SYMBOLS the table the .sh wrote.
-- Quickstarts a new game, then loads Aigina directly (see ichor_lib.lua):
--   1. The voyage night: arriving through warp 0 (the deck's scripted warp) plays
--      beat 10B on the quay: Kleon pats the stones, Alethea and Kleon talk and
--      walk off, Nausikles sends everyone to the inn. The sky is forced to night.
--   2. Screen-sized views of the town along the player's route, at night.
--   3. Every person, sign and hidden item, the shut gate, and the three doors.
--   4. After the crossing: no arrival, the gate open with its keeper aside, the
--      road north walkable to the seam, and Nausikles running the ferry.
-- Passes when every expectation holds; "AEGINA FAIL" lines name the ones that don't.

local L = dofile("tools/ichor/tests/ichor_lib.lua")
local S = dofile(os.getenv("AEGINA_SYMBOLS") or "build/test_aegina/symbols.lua")
local K = L.K
local OUT = os.getenv("AEGINA_OUT") or "build/test_aegina/"

local function split(map) return map >> 8, map & 0xFF end
local G, N = split(S.MAP_AEGINA)
local DIR = { south = 1, north = 2, west = 3, east = 4 }

-- local ids, in map.json's order
local NAUSIKLES, KLEON, ALETHEA, GATEKEEPER = 1, 2, 3, 4

local function location()
  local a = L.sb1() + S.OFF_SB1_LOCATION
  return emu:read8(a) * 256 + emu:read8(a + 1)
end

local function s16(v) if v >= 0x8000 then return v - 0x10000 end return v end

local function player_obj()
  return S.gObjectEvents + emu:read8(S.gPlayerAvatar + S.OFF_AVATAR_OBJECT_EVENT_ID) * S.OBJECT_EVENT_SIZE
end

local function player_xy()
  local c = player_obj() + S.OFF_OBJ_CURRENT_COORDS
  return s16(emu:read16(c)) - S.MAP_OFFSET, s16(emu:read16(c + 2)) - S.MAP_OFFSET
end

-- The object with this local id on the current map, if it's on screen.
local function object_xy(id)
  for i = 0, S.OBJECT_EVENTS_COUNT - 1 do
    local o = S.gObjectEvents + i * S.OBJECT_EVENT_SIZE
    if emu:read8(o) & 1 == 1 and emu:read8(o + S.OFF_OBJ_LOCAL_ID) == id then
      local c = o + S.OFF_OBJ_CURRENT_COORDS
      return s16(emu:read16(c)) - S.MAP_OFFSET, s16(emu:read16(c + 2)) - S.MAP_OFFSET
    end
  end
  return nil
end

local function metatile(x, y)
  local width = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_WIDTH)
  local map = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_MAP)
  return emu:read16(map + 2 * ((x + S.MAP_OFFSET) + (y + S.MAP_OFFSET) * width)) & 0x3FF
end

-- Face a direction without moving (written straight into the player's object
-- event: facingDirection is the low nibble at 0x18, movementDirection the high).
local function face(dir)
  return { check = function()
    emu:write8(player_obj() + 0x18, dir | (dir << 4))
    return true, "faced " .. dir
  end }
end

local function at(x, y, what)
  return { check = function()
    local px, py = player_xy()
    return px == x and py == y, string.format("%s: the player is at (%d,%d); want (%d,%d)", what, px, py, x, y)
  end }
end

local function on_map(map, what)
  return { check = function()
    return location() == map, string.format("%s: on map 0x%04X; want 0x%04X", what, location(), map)
  end }
end

-- Warping while a script runs corrupts the heap, so every warp first checks the
-- field is idle (no script, no message box): a talk that leaves a box open fails
-- here instead of crashing the game.
local CONTEXT_SHUTDOWN = 2
local function idle(what)
  return { check = function()
    local busy = emu:read8(S.sGlobalScriptContextStatus) ~= CONTEXT_SHUTDOWN
                 or emu:read8(S.sLockFieldControls) ~= 0
    return not busy, "the field is idle before " .. what
  end }
end

local function go(x, y, warp)
  return { idle(string.format("warping to (%d,%d)", x, y)),
           { warp = { G, N, warp or -1, x, y }, wait = 200 } }
end

local function view(name, x, y)
  return L.seq(go(x, y), { { shot = "view_" .. name .. ".png", wait = 2 } })
end

-- Read something in front of the player: warp, face it, press A to talk and then
-- once for each of its n boxes.
local function read(name, x, y, dir, n, gap)
  return L.seq(go(x, y), { face(dir), { wait = 4 } }, L.talk(name, n + 1, gap or 40),
               { { wait = 30 }, { shot = name .. "_end.png" } })
end

local function door(name, x, y, map)
  return L.seq(go(x, y + 1), {
    { hold = K.UP, frames = 40, wait = 160 },
    { shot = "door_" .. name .. ".png" },
    on_map(map, "the " .. name .. " door"),
  })
end

local steps = L.seq(
  L.quickstart(),
  { { instant_text = true } },

  -- 1. beat 10B: off the gangplank onto the quay, warp 0, at night
  { { warp = { G, N, 0, 12, 12 }, wait = 150 },
    { shot = "01_arrival.png" },
    at(12, 12, "the arrival tile") },
  L.talk("02_arrival", 6, 50),
  { { wait = 40 }, { shot = "03_walk_off.png", wait = 140 },
    { shot = "04_after.png" },
    { expect_flag = S.FLAG_ARRIVED, why = "the arrival did not set FLAG_ICHOR_ARRIVED_AEGINA" },
    { expect_flag = S.FLAG_VISITED, why = "Aigina was not marked visited" },
    { expect_flag = S.FLAG_HIDE_CAST, why = "Kleon and Alethea were not hidden after walking off" },
    { check = function()
        local t = emu:read8(S.gTimeOfDay)
        return t == S.TIME_NIGHT, string.format("time of day is %d on the voyage night; want night (%d)", t, S.TIME_NIGHT)
      end },
    { check = function()
        return object_xy(KLEON) == nil and object_xy(ALETHEA) == nil, "Kleon and Alethea are gone from the quay"
      end } },

  -- 2. the town at night, a screen at a time along the player's route
  view("quay", 12, 12), view("waterfront_west", 7, 12), view("kolona", 4, 8),
  view("headland", 3, 4), view("west_mole", 8, 4), view("east_mole", 17, 4),
  view("inn", 15, 17), view("square", 21, 18), view("lane", 24, 9),
  view("ant_hills", 22, 10), view("gate", 24, 5), view("aiakides", 27, 9),
  view("east_street", 26, 12), view("orchard", 5, 16), view("beach", 10, 19),
  view("south", 18, 19),
  { { check = function()
        return emu:read8(S.gTimeOfDay) == S.TIME_NIGHT, "the night holds after a warp within town"
      end } },

  -- 3. the people, the signs, the hidden items and the doors on the voyage night
  read("10_nausikles_night", 12, 12, DIR.north, 1),
  read("11_gatekeeper_night", 24, 5, DIR.north, 2),
  go(25, 4),
  { { hold = K.UP, frames = 40, wait = 60 }, at(25, 4, "the shut gate"),
    { shot = "12_gate_shut.png" },
    { check = function()
        return metatile(24, 3) == 0x2C0 and metatile(25, 3) == 0x2C1, "the gate's leaves are shut"
      end } },
  read("13_fisherwoman", 18, 3, DIR.west, 2),
  read("14_kid", 21, 10, DIR.north, 2),
  read("15_ergant", 22, 10, DIR.north, 1),
  read("16_kolona", 3, 8, DIR.north, 4),
  read("17_town_sign", 10, 13, DIR.north, 1),
  read("18_inn_sign", 16, 17, DIR.north, 1),
  read("19_mint_sign", 22, 17, DIR.north, 1),
  read("20_aiakides_sign", 26, 9, DIR.north, 1),
  read("21_gate_sign", 26, 4, DIR.north, 1),
  -- (the item fanfare holds the box: give it time before each press)
  read("22_stardust", 4, 8, DIR.north, 2, 200),
  { { expect_flag = S.FLAG_STARDUST, why = "the Stardust at Kolona's foot was not found" } },
  read("23_big_pearl", 16, 4, DIR.north, 2, 200),
  { { expect_flag = S.FLAG_BIG_PEARL, why = "the Big Pearl at the end of the mole was not found" } },
  door("inn", 15, 16, S.MAP_INN),
  door("mint", 21, 16, S.MAP_MINT),
  door("aiakides", 27, 8, S.MAP_AIAKIDES),

  -- 4. after the crossing: a later visit by ferry
  { { flag = S.FLAG_CROSSING_DONE },
    { flag = S.FLAG_NIGHT } },
  go(12, 12, 0),
  { { shot = "30_later_visit.png" },
    at(12, 12, "the ferry's landing"),
    { check = function()
        return metatile(24, 3) ~= 0x2C0 and metatile(25, 3) ~= 0x2C1, "the gate stands open"
      end },
    { check = function()
        return object_xy(KLEON) == nil and object_xy(ALETHEA) == nil, "the voyage cast stay hidden"
      end },
    { check = function()
        local x, y = object_xy(NAUSIKLES)
        return x == 12 and y == 11, "Nausikles waits at the gangplank's foot"
      end } },
  read("31_ferry", 12, 12, DIR.north, 1),
  { { shot = "32_ferry_choice.png" }, { press = K.B, wait = 40 }, { shot = "33_ferry_stay.png" },
    { press = K.A, wait = 40 } },
  read("34_gatekeeper_later", 23, 5, DIR.north, 1),
  go(24, 5),
  { { check = function()
        local x, y = object_xy(GATEKEEPER)
        return x == 23 and y == 4, string.format("the gatekeeper is at (%s,%s); want (23,4), beside the gate", tostring(x), tostring(y))
      end },
    { shot = "35_gate_open.png" }, { hold = K.UP, frames = 140, wait = 170 },
    at(24, 0, "the road through the gate, at the seam"), { shot = "36_through_the_gate.png" } }
)

L.run("AEGINA", OUT, steps)
