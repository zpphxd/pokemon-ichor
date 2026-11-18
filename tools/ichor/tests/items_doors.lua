-- Item icons, the ground jar and door animations: run by items_doors.sh (read it
-- first). Steps run on tools/ichor/tests/ichor_lib.lua's runner; ids and offsets
-- come from the symbols table the shell script builds from the game's headers.
--
--   1. Doors. Walk into and out of every animated door on the slice's maps, with
--      a screenshot every 3 frames (an exit starts on the room's mat): Elaia's two Petalburg doors (a Hoenn door
--      must not animate on an Ichor map), Akti's Asclepeion and Agora. Then the
--      aethos doors no map uses yet (farmhouse, palaestra, theater), written into
--      Akti's map grid over the Asclepeion's door cell, whose warp they borrow.
--   2. The ground jars, where Route 1, Kronion Hill and Akti place them.
--   3. The bag: every pocket filled with the slice's items, one screenshot per
--      item; the Items pocket twice, as it holds 30.
--   4. The Agora's buy list, one screenshot per stock line.
-- ITEMS_MODE=doors stops after part 1, so an older ROM can be compared.

local L = dofile("tools/ichor/tests/ichor_lib.lua")
local S = dofile(os.getenv("ITEMS_SYMBOLS") or "build/test_items_doors/symbols.lua")
local OUT = os.getenv("ITEMS_OUT") or "build/test_items_doors/"
local MODE = os.getenv("ITEMS_MODE") or "all"
local K = L.K

-- this ROM's symbols, not the ones in pokeemerald.map
L.SB1, L.SB2, L.MAIN, L.CB2_LOADMAP = S.gSaveBlock1Ptr, S.gSaveBlock2Ptr, S.gMain, S.CB2_LoadMap

local function group(map) return map >> 8 end
local function num(map) return map & 0xFF end
local function sb1() return emu:read32(S.gSaveBlock1Ptr) end
local function sb2() return emu:read32(S.gSaveBlock2Ptr) end

local function setflag(f, on)
  local a = sb1() + S.OFF_SB1_FLAGS + (f >> 3)
  local b = emu:read8(a)
  if on == false then b = b & ~(1 << (f & 7)) else b = b | (1 << (f & 7)) end
  emu:write8(a, b)
end

local function warp(map, x, y, wait)
  return { warp = { group(map), num(map), -1, x, y }, wait = wait or 120 }
end

-- A quiet slice: BAG first in the start menu, no cutscene or trainer in the way.
local function quiet()
  return { check = function()
    setflag(S.FLAG_SYS_POKEDEX_GET, false)
    setflag(S.FLAG_DEXNAV_GET, false)
    setflag(S.FLAG_SYS_POKEMON_GET, false)
    setflag(S.FLAG_SYS_POKENAV_GET, false)
    for _, f in ipairs({ S.FLAG_ARRIVED_AKTI, S.FLAG_RUINS_CLEARED, S.FLAG_HIDE_RUINS_GRUNTS,
                         S.FLAG_HIDE_ALETHEA_RUINS }) do setflag(f, true) end
    for t = S.TRAINER_ICHOR_FIRST, S.TRAINER_ICHOR_LAST do setflag(S.TRAINER_FLAGS_START + t, true) end
    local a = sb2() + S.OFF_SB2_OPTIONS        -- instant text
    emu:write16(a, (emu:read16(a) & ~7) | 3)
    return true, "quiet slice: flags and instant text set"
  end }
end

-- A walk into a door: hold the direction (a turn, then the step), then a
-- screenshot every 3 frames through the door's animation and the fade.
local function walk_shots(prefix, key, n)
  local out = { { hold = key, frames = 14, wait = 1 } }
  for k = 0, n - 1 do
    table.insert(out, { shot = string.format("%s_%02d.png", prefix, k), wait = 3 })
  end
  return out
end

-- Write metatile `mt` into the live map grid at (x, y), keeping its collision and
-- elevation bits. The screen catches up when the field is redrawn.
local function set_metatile(x, y, mt)
  return { check = function()
    local w = emu:read32(S.gBackupMapLayout + S.OFF_LAYOUT_WIDTH)
    local map = emu:read32(S.gBackupMapLayout + S.OFF_LAYOUT_MAP)
    local a = map + 2 * ((x + S.MAP_OFFSET) + w * (y + S.MAP_OFFSET))
    emu:write16(a, (emu:read16(a) & 0xFC00) | mt)
    return true, string.format("metatile %03X written at (%d,%d)", mt, x, y)
  end }
end

-- Open and close the bag: on the way back the field is redrawn from the grid.
local function redraw()
  return {
    { press = K.START, wait = 40 }, { press = K.A, wait = 150 },
    { press = K.B, wait = 150 }, { press = K.B, wait = 40 },
  }
end

local AKTI, ASCLEPEION, AGORA = S.MAP_AKTI, S.MAP_ASCLEPEION, S.MAP_AGORA

local doors = L.seq(
  L.quickstart(),
  { quiet() },

  -- Elaia: the player's house and the Akademia are Petalburg's doors
  { warp(S.MAP_ELAIA, 5, 9) }, walk_shots("door_elaia_house", K.UP, 30),
  { warp(S.MAP_ELAIA, 7, 17) }, walk_shots("door_elaia_akademia", K.UP, 30),

  -- Akti: the Asclepeion (in, then out over its mat) and the Agora
  { warp(AKTI, 3, 23) }, walk_shots("door_asclepeion_in", K.UP, 30),
  { warp(ASCLEPEION, 7, 10) }, walk_shots("door_asclepeion_out", K.DOWN, 60),
  { warp(AKTI, 7, 17) }, walk_shots("door_agora_in", K.UP, 30),
  { warp(AGORA, 6, 8) }, walk_shots("door_agora_out", K.DOWN, 60),

  -- aethos doors not on a map yet, over the Asclepeion's door cell
  { warp(AKTI, 3, 23), set_metatile(3, 22, 0x021) }, redraw(), walk_shots("door_farmhouse_in", K.UP, 30),
  { warp(AKTI, 3, 23), set_metatile(3, 22, 0x1CD) }, redraw(), walk_shots("door_palaestra_in", K.UP, 30),
  { warp(AKTI, 3, 23), set_metatile(3, 22, 0x1DB) }, redraw(), walk_shots("door_theater_in", K.UP, 30)
)

-- The ground jars: stand two tiles south of each one the maps place.
local jars = {}
for _, j in ipairs({
  { "route1_poke_ball", S.MAP_ROUTE1, 3, 42 }, { "route1_miracle_seed", S.MAP_ROUTE1, 27, 35 },
  { "route1_potion", S.MAP_ROUTE1, 15, 20 }, { "kronion_escape_rope", S.MAP_KRONION, 12, 8 },
  { "akti_potion", AKTI, 2, 10 }, { "akti_paralyze_heal", AKTI, 16, 10 },
}) do
  table.insert(jars, warp(j[2], j[3], j[4] + 2, 150))
  table.insert(jars, { shot = "jar_" .. j[1] .. ".png", wait = 2 })
end

-- The bag. Pockets are filled straight into SaveBlock1; quantities are stored
-- XORed with SaveBlock2's encryption key, as the bag code does.
local function fill(offset, count, items)
  local base = sb1() + S.OFF_SB1_BAG + offset
  local key = emu:read32(sb2() + S.OFF_SB2_KEY) & 0xFFFF
  for i = 0, count - 1 do
    local id = items[i + 1] or 0
    emu:write16(base + i * S.SLOT_SIZE, id)
    emu:write16(base + i * S.SLOT_SIZE + 2, ((id ~= 0) and 3 or 0) ~ key)
  end
end

local ITEMS_A = { S.ITEM_POTION, S.ITEM_SUPER_POTION, S.ITEM_HYPER_POTION, S.ITEM_MAX_POTION,
  S.ITEM_FULL_RESTORE, S.ITEM_ANTIDOTE, S.ITEM_PARALYZE_HEAL, S.ITEM_BURN_HEAL, S.ITEM_ICE_HEAL,
  S.ITEM_AWAKENING, S.ITEM_FULL_HEAL, S.ITEM_REVIVE, S.ITEM_MAX_REVIVE, S.ITEM_ETHER, S.ITEM_MAX_ETHER,
  S.ITEM_ELIXIR, S.ITEM_MAX_ELIXIR, S.ITEM_REPEL, S.ITEM_SUPER_REPEL, S.ITEM_MAX_REPEL, S.ITEM_HONEY,
  S.ITEM_MOOMOO_MILK, S.ITEM_FRESH_WATER, S.ITEM_ENERGY_POWDER, S.ITEM_HEAL_POWDER, S.ITEM_ENERGY_ROOT,
  S.ITEM_REVIVAL_HERB, S.ITEM_MIRACLE_SEED, S.ITEM_HARD_STONE, S.ITEM_CHARCOAL }
local ITEMS_B = { S.ITEM_MYSTIC_WATER, S.ITEM_STARDUST, S.ITEM_STAR_PIECE, S.ITEM_PEARL, S.ITEM_BIG_PEARL,
  S.ITEM_HEART_SCALE, S.ITEM_RELIC_COPPER, S.ITEM_RELIC_SILVER, S.ITEM_RELIC_GOLD, S.ITEM_COMET_SHARD,
  S.ITEM_SOFT_SAND, S.ITEM_SHOAL_SALT }
local TMS = { S.ITEM_TM_FACADE, S.ITEM_TM_FOCUS_PUNCH, S.ITEM_TM_WATER_PULSE, S.ITEM_TM_SUNNY_DAY,
  S.ITEM_TM_THUNDERBOLT, S.ITEM_TM_GIGA_DRAIN, S.ITEM_TM_ICE_BEAM, S.ITEM_TM_PSYCHIC, S.ITEM_TM_SHADOW_BALL,
  S.ITEM_TM_DRAGON_CLAW, S.ITEM_TM_SLUDGE_BOMB, S.ITEM_TM_EARTHQUAKE, S.ITEM_TM_ROCK_TOMB,
  S.ITEM_TM_AERIAL_ACE, S.ITEM_TM_STEEL_WING, S.ITEM_TM_THIEF, S.ITEM_HM_CUT }

-- Every Poke Ball, over the two passes: the pocket holds 16.
local BALLS_A = { S.ITEM_POKE_BALL, S.ITEM_GREAT_BALL, S.ITEM_ULTRA_BALL, S.ITEM_MASTER_BALL, S.ITEM_PREMIER_BALL, S.ITEM_HEAL_BALL, S.ITEM_NET_BALL, S.ITEM_NEST_BALL, S.ITEM_DIVE_BALL, S.ITEM_DUSK_BALL, S.ITEM_TIMER_BALL, S.ITEM_QUICK_BALL, S.ITEM_REPEAT_BALL, S.ITEM_LUXURY_BALL, S.ITEM_LEVEL_BALL, S.ITEM_LURE_BALL }
local BALLS_B = { S.ITEM_MOON_BALL, S.ITEM_FRIEND_BALL, S.ITEM_LOVE_BALL, S.ITEM_FAST_BALL, S.ITEM_HEAVY_BALL, S.ITEM_DREAM_BALL, S.ITEM_SAFARI_BALL, S.ITEM_SPORT_BALL, S.ITEM_PARK_BALL, S.ITEM_BEAST_BALL, S.ITEM_CHERISH_BALL, S.ITEM_STRANGE_BALL }

local function fill_bag(items, balls)
  return { check = function()
    fill(S.OFF_BAG_ITEMS, S.BAG_ITEMS_COUNT, items)
    fill(S.OFF_BAG_KEY, S.BAG_KEYITEMS_COUNT, { S.ITEM_ESCAPE_ROPE, S.ITEM_OLD_ROD })
    fill(S.OFF_BAG_BALLS, S.BAG_POKEBALLS_COUNT, balls)
    fill(S.OFF_BAG_TMHM, S.BAG_TMHM_COUNT, TMS)
    fill(S.OFF_BAG_BERRIES, S.BAG_BERRIES_COUNT, { S.ITEM_ORAN_BERRY, S.ITEM_SITRUS_BERRY })
    return true, string.format("bag filled (%d in Items)", #items)
  end }
end

-- One screenshot per line of the open pocket, then on to the next pocket.
local function page(prefix, n)
  local out = {}
  for k = 1, n do
    table.insert(out, { shot = string.format("%s_%02d.png", prefix, k), wait = 2 })
    table.insert(out, { press = K.DOWN, wait = 14 })
  end
  for _ = 1, n do table.insert(out, { press = K.UP, wait = 8 }) end
  return out
end

local bag = L.seq(
  { warp(AKTI, 12, 20), fill_bag(ITEMS_A, BALLS_A),
    { press = K.START, wait = 40 }, { press = K.A, wait = 160 } },
  page("bag_items_a", #ITEMS_A),
  { { press = K.RIGHT, wait = 40 } }, page("bag_balls", #BALLS_A),
  { { press = K.RIGHT, wait = 40 } }, page("bag_tms", #TMS),
  { { press = K.RIGHT, wait = 40 } }, page("bag_berries", 2),
  { { press = K.RIGHT, wait = 40 } }, page("bag_key", 2),
  { { press = K.B, wait = 150 }, { press = K.B, wait = 40 },
    fill_bag(ITEMS_B, BALLS_B), { press = K.START, wait = 40 }, { press = K.A, wait = 160 },
    { press = K.RIGHT, wait = 40 } },          -- Key Items wraps round to Items
  page("bag_items_b", #ITEMS_B),
  { { press = K.RIGHT, wait = 40 } }, page("bag_balls_b", #BALLS_B),
  { { press = K.B, wait = 150 }, { press = K.B, wait = 40 } }
)

-- The Agora: Demeas across the counter, from (3,4); the stock before the laurel.
local shop = L.seq(
  { warp(AGORA, 3, 4, 120), { hold = K.UP, frames = 4, wait = 30 } },
  L.talk("shop_demeas", 2, 30),
  { { press = K.A, wait = 150 } },             -- BUY
  page("shop_buy", 5),
  { { press = K.B, wait = 120 }, { press = K.B, wait = 60 }, { press = K.A, wait = 30 } }
)

local steps = doors
if MODE ~= "doors" then steps = L.seq(doors, jars, bag, shop) end
L.run("ITEMS", OUT, steps)
