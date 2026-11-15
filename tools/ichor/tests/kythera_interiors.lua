-- Kythera's and Melos's interiors: an in-game tour (tools/ichor/maps/kythera_homes.py).
--
--   tools/ichor/tests/kythera_interiors.sh [rom]
--
-- Env: KYTHERA_OUT is the screenshot folder (default build/test_kythera/, which
-- must exist). Quickstarts a new game with a test Pokémon at 1 HP, then loads
-- every interior in turn and screenshots it, and plays one person's lines in
-- most of them: the bad guests' scene in Axylos's house (refused), Euodia's
-- Soothe Bell, a heal at each Asclepeion, Teukros's stall, Phereklos's
-- knucklebones, Peristera's Egg, Lysis's trade (refused), Myles's bread and
-- Metronome, Kentrios, and the boathouse's stair up to Myrtis's soup and
-- Kalchedon's Damp Rock. The map groups are gMapGroup_IndoorKythera and
-- gMapGroup_IndoorMelos; the .sh reads their numbers from map_groups.json.
--
-- The runner loads maps directly, so every conversation is closed before the
-- next warp: B advances a box, and answers NO. A is pressed only an exact number
-- of times, where a YES is wanted.
-- Passes when every heal check holds; the screenshots are the review.

local L = dofile("tools/ichor/tests/ichor_lib.lua")
local K = L.K
local OUT = os.getenv("KYTHERA_OUT") or "build/test_kythera/"

local KY = tonumber(os.getenv("KYTHERA_GROUP_KY") or "") or 4
local ME = tonumber(os.getenv("KYTHERA_GROUP_ME") or "") or 5
local AXYLOS, DIVERS, PERFUMER, NIKARETE, SHIPWRIGHT, SK_ASCLEPEION, SK_AGORA = 0, 1, 2, 3, 4, 5, 6
local DOVECOTE, POTTER, PA_ASCLEPEION, PA_AGORA, PYGMALION, MIRROR, ORCHARD = 7, 8, 9, 10, 11, 12, 13
local MILL = 14
local FARM, KNAPPER, BOATHOUSE = 0, 1, 2
local SPECIES_WOOLOO = 831

-- Load a map at (x, y), wait, and screenshot it.
local function visit(group, num, x, y, name, wait)
  return {
    { warp = { group, num, -1, x, y }, wait = wait or 150 },
    { shot = name .. ".png", wait = 10 },
  }
end

-- Turn toward a neighbour (a short press doesn't step into an occupied tile).
local function face(key) return { { press = key, wait = 24 } } end

-- Press B n times with a screenshot before each: reads a conversation to its
-- end, answering NO to any question.
local function read(prefix, n, gap)
  local out = {}
  for k = 1, n do
    table.insert(out, { shot = string.format("%s_%02d.png", prefix, k) })
    table.insert(out, { press = K.B, wait = gap or 30 })
  end
  return out
end

-- Close whatever is still open before the next warp.
local function flush()
  local out = {}
  for _ = 1, 12 do table.insert(out, { press = K.B, wait = 25 }) end
  table.insert(out, { wait = 30 })
  return out
end

local function healed(why)
  return { { check = function()
    local hp = L.party_hp()
    if hp < 20 then return false, why .. " (HP " .. hp .. ")" end
    return true, why
  end } }
end

local function hurt() return { { give_mon = SPECIES_WOOLOO, wait = 2 } } end

local steps = L.seq(
  L.quickstart(),
  { { instant_text = true } },

  -- Skandeia. Axylos's house: arriving through the door plays the bad guests'
  -- scene; read to the challenge, refuse it, and hear Alethea out.
  { { warp = { KY, AXYLOS, 0, 6, 8 }, wait = 150 } },
  read("sk_axylos_scene", 14, 45), flush(),
  { { shot = "sk_axylos_after.png" } },

  visit(KY, DIVERS, 7, 5, "sk_divers"),
  face(K.UP), L.talk("sk_bathykleia", 5, 30), read("sk_bathykleia_no", 3), flush(),

  -- the perfumer's: the roses on entry, then Euodia and her Soothe Bell
  visit(KY, PERFUMER, 3, 4, "sk_perfumer_roses", 120),
  { { press = K.B, wait = 40 } },
  face(K.UP), { { press = K.A, wait = 30 } }, read("sk_euodia", 9), flush(),

  visit(KY, NIKARETE, 4, 7, "sk_nikarete"),
  face(K.LEFT), { { press = K.A, wait = 30 } }, read("sk_nikarete_talk", 3), flush(),

  visit(KY, SHIPWRIGHT, 7, 5, "sk_shipwright"),
  face(K.LEFT), L.talk("sk_phereklos", 5, 30),   -- three boxes, then YES to a game
  { { wait = 30 } }, read("sk_phereklos_game", 6, 35), flush(),

  hurt(),
  visit(KY, SK_ASCLEPEION, 5, 4, "sk_asclepeion"),
  face(K.UP), L.talk("sk_healer", 5, 40),        -- her line, the welcome's three boxes, YES
  { { wait = 300 }, { shot = "sk_healer_done.png" } }, flush(),
  healed("Skandeia's healer restored the party"),

  visit(KY, SK_AGORA, 7, 4, "sk_agora"),
  face(K.UP), { { press = K.A, wait = 60 }, { shot = "sk_teukros_mart.png" },
    { press = K.B, wait = 60 }, { shot = "sk_teukros_bye.png" } }, flush(),

  -- Paphia
  visit(KY, DOVECOTE, 5, 4, "pa_dovecote"),
  face(K.UP), L.talk("pa_peristera", 6, 30),     -- four boxes, the question, YES
  { { wait = 150 }, { shot = "pa_peristera_egg.png" } }, flush(),

  visit(KY, POTTER, 4, 5, "pa_potter"),
  face(K.UP), L.talk("pa_lysis", 6, 30),         -- five boxes, then the question
  read("pa_lysis_no", 2), flush(),

  hurt(),
  visit(KY, PA_ASCLEPEION, 3, 4, "pa_asclepeion"),
  face(K.UP), L.talk("pa_healer", 5, 40),
  { { wait = 300 }, { shot = "pa_healer_done.png" } }, flush(),
  healed("Paphia's healer restored the party"),
  visit(KY, PA_AGORA, 6, 4, "pa_agora"),
  visit(KY, PYGMALION, 4, 3, "pa_pygmalion"),
  face(K.RIGHT), { { press = K.A, wait = 30 } }, read("pa_pygmalion_talk", 3), flush(),
  visit(KY, MIRROR, 5, 4, "pa_mirror"),
  face(K.RIGHT), { { press = K.A, wait = 30 } }, read("pa_leukippe", 3), flush(),
  visit(KY, ORCHARD, 4, 8, "pa_orchard"),
  face(K.RIGHT), { { press = K.A, wait = 30 } }, read("pa_eumelos", 3), flush(),

  -- the falls: Myles's bread (a heal) and his Metronome
  hurt(),
  visit(KY, MILL, 4, 4, "falls_mill"),
  face(K.UP), L.talk("falls_myles", 3, 40), { { wait = 220 } },
  read("falls_myles_gift", 4), flush(),
  healed("Myles's bread restored the party"),

  -- Melos
  visit(ME, FARM, 5, 4, "me_farmhouse"),
  face(K.UP), { { press = K.A, wait = 30 } }, read("me_kentrios", 2), flush(),
  visit(ME, KNAPPER, 3, 4, "me_knapper"),
  face(K.RIGHT), { { press = K.A, wait = 30 } }, read("me_melanippos", 2), flush(),
  -- the boathouse: up its stair to the room over the boat, then along to Myrtis
  hurt(),
  visit(ME, BOATHOUSE, 9, 3, "me_boathouse"),
  { { hold = K.UP, frames = 24, wait = 180 }, { shot = "me_loft_arrival.png" },
    { check = function()
        local loc = L.sb1() + 0x04
        local ok = emu:read8(loc) == ME and emu:read8(loc + 1) == 3
        return ok, "the boathouse's stair leads up to the loft"
      end } },
  visit(ME, 3, 6, 2, "me_loft"),
  face(K.DOWN),
  L.talk("me_myrtis", 2, 40), { { wait = 220 } }, read("me_myrtis_after", 5), flush(),
  healed("Myrtis's soup restored the party")
)

L.run("KYTHERA", OUT, steps)
