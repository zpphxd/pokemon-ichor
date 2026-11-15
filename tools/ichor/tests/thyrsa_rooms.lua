-- Thyrsa's and Eleutherai's interiors (Act II batch 1, the rooms agent):
--
--   tools/ichor/tests/thyrsa_rooms.sh [rom]
--
-- A quickstart save, then a screenshot tour of all thirteen rooms with their
-- people in place, and the rooms' services played: the Asclepeion's heal (the
-- party's balls land on the healing basin, and the healer bows), Opsimos's soup in
-- the watch-house, Pindaros's welcome and rest menu, the Agora's wine counter, and
-- thirty steps on Staphylos's treading floor. Screenshots land in
-- build/test_thyrsa_rooms/; read them.
local L = dofile("tools/ichor/tests/ichor_lib.lua")
local K = L.K
local OUT = os.getenv("ROOMS_OUT") or "build/test_thyrsa_rooms/"

-- Map numbers come from the generated header, so the Hoenn cut can renumber them.
local MAPS = {}
do
  local f = assert(io.open("include/constants/map_groups.h", "r"))
  for line in f:lines() do
    local name, num, grp = line:match("^%s+(MAP_[%w_]+)%s*=%s*%((%d+)%s*|%s*%((%d+)%s*<<%s*8%)%)")
    if name then MAPS[name] = { tonumber(grp), tonumber(num) } end
  end
  f:close()
end

local function at(map, x, y, wait)
  local m = assert(MAPS[map], map)
  return { warp = { m[1], m[2], -1, x, y }, wait = wait or 90 }
end

local function shots(prefix, key, n, gap)
  local out = {}
  for k = 1, n do
    table.insert(out, { shot = string.format("%s_%02d.png", prefix, k) })
    table.insert(out, { press = key, wait = gap or 40 })
  end
  return out
end

local function face(key) return { hold = key, frames = 3, wait = 20 } end

-- Each room: where to stand for the tour shot (just inside the door), and a
-- second spot that frames the far side.
local TOUR = {
  { "Eleutherai_WatchHouse",    "MAP_ELEUTHERAI_WATCH_HOUSE",    7, 6, 13, 4 },
  { "Eleutherai_OinoeHouse",    "MAP_ELEUTHERAI_OINOE_HOUSE",    4, 5 },
  { "Eleutherai_LysidikeHouse", "MAP_ELEUTHERAI_LYSIDIKE_HOUSE", 5, 6 },
  { "ThyrsaCity_Asclepeion",    "MAP_THYRSA_CITY_ASCLEPEION",    7, 9, 7, 4 },
  { "ThyrsaCity_Agora",         "MAP_THYRSA_CITY_AGORA",         6, 8 },
  { "ThyrsaCity_Tavern",        "MAP_THYRSA_CITY_TAVERN",        5, 8, 7, 5 },
  { "ThyrsaCity_PindarosHouse", "MAP_THYRSA_CITY_PINDAROS_HOUSE", 2, 7, 8, 5 },
  { "ThyrsaCity_MantoHouse",    "MAP_THYRSA_CITY_MANTO_HOUSE",   4, 6 },
  { "ThyrsaCity_VintnerHouse",  "MAP_THYRSA_CITY_VINTNER_HOUSE", 6, 8 },
  { "ThyrsaCity_ActorHouse",    "MAP_THYRSA_CITY_ACTOR_HOUSE",   3, 8, 3, 5 },
  { "ThyrsaCity_EudoraHouse",   "MAP_THYRSA_CITY_EUDORA_HOUSE",  5, 9, 6, 3 },
  { "ThyrsaCity_MaskWorkshop",  "MAP_THYRSA_CITY_MASK_WORKSHOP", 6, 5, 12, 4 },
  { "ThyrsaCity_SownHouse",     "MAP_THYRSA_CITY_SOWN_HOUSE",    4, 6 },
}

local tour = {}
for _, r in ipairs(TOUR) do
  table.insert(tour, at(r[2], r[3], r[4]))
  table.insert(tour, { shot = r[1] .. ".png" })
  if r[5] then
    table.insert(tour, at(r[2], r[5], r[6]))
    table.insert(tour, { shot = r[1] .. "_far.png" })
  end
end

local steps = L.seq(
  L.quickstart(),
  { { instant_text = true }, { give_mon = 7, wait = 2 } },
  tour,
  -- The Asclepeion: talk across the counter from (7,4) and heal.
  { at("MAP_THYRSA_CITY_ASCLEPEION", 7, 4, 100), face(K.UP) },
  shots("heal", K.A, 4, 30),
  { { wait = 120 }, { shot = "heal_balls.png", wait = 190 }, { shot = "heal_done.png" } },
  shots("heal_end", K.B, 4, 30),
  { { check = function()
        local g, n = L.last_heal()
        local m = MAPS["MAP_THYRSA_CITY"]
        return g == m[1] and n == m[2], string.format("respawn set to Thyrsa (%d.%d)", g, n)
      end } },
  -- Opsimos's soup.
  { at("MAP_ELEUTHERAI_WATCH_HOUSE", 12, 4), face(K.UP) },
  shots("opsimos", K.A, 4, 120),
  -- Pindaros: welcome, heal, his first-visit lines, the rest menu.
  { at("MAP_THYRSA_CITY_PINDAROS_HOUSE", 8, 5), face(K.UP) },
  shots("pindaros", K.A, 9, 90),
  shots("pindaros_close", K.B, 3, 40),
  -- The wine counter: talk across it from (4,4).
  { at("MAP_THYRSA_CITY_AGORA", 4, 4), face(K.UP) },
  shots("wine", K.A, 3, 60),
  shots("wine_close", K.B, 4, 40),
  -- Treading: YES to Staphylos from (4,5), then thirty steps on the floor.
  { at("MAP_THYRSA_CITY_VINTNER_HOUSE", 4, 5), face(K.DOWN) },
  shots("tread_ask", K.A, 3, 40),
  { { shot = "tread_yes.png" },
    { hold = K.UP, frames = 16, wait = 24 },
    { hold = K.RIGHT, frames = 16, wait = 24 },
    { shot = "tread_on.png" } }
)
-- 30 steps on the floor's row 4, between x 5 and 8 (the first step was onto (5,4))
local treads = {}
local dir, x = K.RIGHT, 5
for _ = 1, 29 do
  if x == 8 then dir = K.LEFT elseif x == 5 then dir = K.RIGHT end
  x = x + (dir == K.RIGHT and 1 or -1)
  table.insert(treads, { hold = dir, frames = 16, wait = 26 })
end
steps = L.seq(steps, treads, { { shot = "tread_done_1.png" } }, shots("tread_done", K.A, 6, 40),
  { { log = "tour and services played" } })

L.run("ROOMS", OUT, steps)
