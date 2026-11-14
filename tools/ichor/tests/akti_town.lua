-- Akti Town check: arrival, the Asclepeion, the Pithos, the Agora and the Old Rod.
--
--   mkdir -p build/akti_test && build/tools/ichor-mgba-headless \
--       --script tools/ichor/tests/akti_town.lua --frames 12000 --until "AKTI done" pokeemerald.gba
--
-- Env: AKTI_OUT is the screenshot folder (default build/akti_test/, which must exist).
-- Quickstarts a new game, then loads each map directly (see ichor_lib.lua):
--   1. Akti's south road: one step onto the gate plays the arrival (beat 6).
--   2. Screen-sized views of the town along the slice's route.
--   3. The Asclepeion: heal with the Ichor healer, check the respawn point is Akti.
--   4. The Pithos: open the jar, look into Pokémon storage, close it.
--   5. The Agora: talk to Demeas and open the shop.
--   6. The Fisher's house: Glaukos gives the Old Rod.
-- Passes when every expectation holds; "AKTI FAIL" lines name the ones that don't.

local L = dofile("tools/ichor/tests/ichor_lib.lua")
local K = L.K
local OUT = os.getenv("AKTI_OUT") or "build/akti_test/"

local AKTI, INDOOR = 0, 75            -- map groups (include/constants/map_groups.h)
local MAP_AKTI = 59
local MAP_ASCLEPEION, MAP_AGORA, MAP_FISHERS = 4, 5, 6
local MAP_DIVERS, MAP_GOATHERDS = 8, 9
local FLAG_BADGE01_GET = L.system_flag(0x7)
local FLAG_ICHOR_AKTI_GOAT_HOME = 0x4C
local FLAG_ICHOR_GOT_SOOTHE_BELL = 0x4E
local FLAG_ICHOR_GOT_SHELL_BELL = 0x4F
local FLAG_ICHOR_ARRIVED_AKTI = 0x2E
local FLAG_ICHOR_VISITED_AKTI = 0x2F
local FLAG_ICHOR_GOT_OLD_ROD = 0x38

local function view(name, x, y)
  return {
    { warp = { AKTI, MAP_AKTI, -1, x, y }, wait = 240 },   -- past the map-name popup
    { shot = "town_" .. name .. ".png", wait = 2 },
  }
end

local steps = L.seq(
  L.quickstart(),
  { { instant_text = true },
    { give_mon = 7, wait = 2 } },             -- a hurt Squirtle, so there is something to heal

  -- 1. beat 6: Diktys meets the player at the gate
  { { warp = { AKTI, MAP_AKTI, -1, 12, 26 }, wait = 100 },
    { shot = "01_south_road.png" },
    { hold = K.DOWN, frames = 10, wait = 130 } },
  L.talk("02_arrival", 6, 30),
  { { wait = 110 },
    { shot = "03_after_arrival.png" },
    { expect_flag = FLAG_ICHOR_ARRIVED_AKTI, why = "the arrival scene did not set FLAG_ICHOR_ARRIVED_AKTI" },
    { expect_flag = FLAG_ICHOR_VISITED_AKTI, why = "Akti's ON_TRANSITION did not set FLAG_ICHOR_VISITED_AKTI" },
    -- SCRIPT.md beat 6: only the Asclepeion's first heal makes Akti the respawn point
    { check = function()
        local g, n = L.last_heal()
        return not (g == AKTI and n == MAP_AKTI),
               "the arrival scene made Akti the respawn point; only the Asclepeion should"
      end } },

  -- 2. the town, a screen at a time
  view("plaza", 12, 20), view("temple", 19, 19), view("harbor_street", 12, 14),
  view("quay", 8, 10), view("pier", 14, 6), view("beach", 23, 8),
  view("asclepeion_garden", 4, 24), view("mole", 5, 5), view("lower_town", 21, 24),

  -- the relic gates (SYSTEMS.md §1, D10), locked side only: the rubble in the
  -- grotto on the tide rocks, and the islet shrine, which the old fisher at the
  -- end of the pier explains
  view("grotto_from_beach", 25, 8),
  view("grotto", 26, 5),
  { { hold = K.UP, frames = 4, wait = 20 } },
  L.talk("40_grotto_rubble", 4, 30),
  view("islet_from_pier", 15, 6),
  { { hold = K.UP, frames = 4, wait = 20 } },
  L.talk("41_islet_fisher", 5, 30),

  -- 3. the Asclepeion: talk across the counter at (7,4)
  { { warp = { INDOOR, MAP_ASCLEPEION, -1, 7, 4 }, wait = 100 },
    { shot = "10_asclepeion.png" },
    { hold = K.UP, frames = 4, wait = 30 } },
  -- A opens "Welcome", then the spring, then "Shall we tend yours?", then picks YES
  L.talk("11_healer", 4, 30),
  { { wait = 10 }, { shot = "12_healer_rest.png", wait = 300 } },   -- the spring's heal jingle
  L.talk("13_healer_done", 2, 40),            -- "Whole and well", "Go in health."
  { { check = function()
        local hp = L.party_hp()
        return hp == 20, string.format("party HP after healing is %d; want 20", hp)
      end },
    { check = function()
        local g, n, x, y = L.last_heal()
        return g == AKTI and n == MAP_AKTI and x == 3 and y == 23,
               string.format("respawn point is map %d.%d (%d,%d); want Akti (3,23)", g, n, x, y)
      end } },

  -- 4. the Pithos, from (12,3) facing the jar
  { { warp = { INDOOR, MAP_ASCLEPEION, -1, 12, 3 }, wait = 100 },
    { hold = K.UP, frames = 4, wait = 30 } },
  L.talk("14_pithos", 3, 30),                 -- (facing it), the jar, lifting the lid
  { { wait = 10 }, { shot = "15_pithos_menu.png" },
    { press = K.A, wait = 30 } },              -- "Pokémon"
  L.talk("16_pithos_storage", 2, 30),          -- "opened", "rest safely"
  { { wait = 120 }, { shot = "17_pokemon_storage.png" },
    { press = K.B, wait = 150 }, { shot = "18_pithos_menu_again.png" },
    { press = K.B, wait = 30 }, { shot = "19_pithos_closed.png" },
    { press = K.A, wait = 30 } },

  -- 5. the Agora: Demeas across his counter, from (3,4)
  { { warp = { INDOOR, MAP_AGORA, -1, 3, 4 }, wait = 100 },
    { shot = "20_agora.png" },
    { hold = K.UP, frames = 4, wait = 30 } },
  L.talk("21_demeas", 2, 30),                 -- (facing him), "Welcome to the Agora!"
  { { wait = 10 }, { shot = "22_dont_haggle.png" },
    { press = K.A, wait = 150 },               -- BUY
    { shot = "23_agora_shop.png" },
    { press = K.B, wait = 120 }, { shot = "24_agora_after_shop.png" },
    { press = K.B, wait = 60 }, { shot = "25_demeas_bye.png" },
    { press = K.A, wait = 30 } },

  -- 6. the Fisher's house: Glaukos at the window, from (3,3)
  { { warp = { INDOOR, MAP_FISHERS, -1, 3, 3 }, wait = 100 },
    { shot = "30_fishers_house.png" },
    { hold = K.UP, frames = 4, wait = 30 } },
  L.talk("31_glaukos", 2, 30),                -- (facing him) "Do you fish?", then YES
  { { wait = 10 }, { shot = "32_glaukos_liar.png" }, { press = K.A, wait = 160 },
    { shot = "33_old_rod.png" }, { press = K.A, wait = 40 } },
  L.talk("34_glaukos_after", 2, 40),
  { { expect_flag = FLAG_ICHOR_GOT_OLD_ROD, why = "Glaukos did not set FLAG_ICHOR_GOT_OLD_ROD" },
    { shot = "35_end.png" } },

  -- 7. the goatherd's farmhouse: Aigon asks after Kapra, the loose goat; she is
  --    eating the Fisher's washing; sent home, she earns his Soothe Bell
  { { warp = { INDOOR, MAP_GOATHERDS, -1, 2, 4 }, wait = 100 },
    { shot = "50_goatherds_house.png" },
    { hold = K.UP, frames = 4, wait = 30 } },
  L.talk("51_aigon_quest", 4, 30),
  { { warp = { AKTI, MAP_AKTI, -1, 3, 15 }, wait = 240 },
    { shot = "52_kapra.png" },
    { hold = K.LEFT, frames = 4, wait = 30 } },
  L.talk("53_kapra", 4, 30),
  { { wait = 90 }, { shot = "53_kapra_gone.png" },
    { expect_flag = FLAG_ICHOR_AKTI_GOAT_HOME, why = "Kapra did not go home" } },
  { { warp = { INDOOR, MAP_GOATHERDS, -1, 2, 4 }, wait = 100 },
    { hold = K.UP, frames = 4, wait = 30 } },
  L.talk("54_aigon_bell", 4, 30),
  { { wait = 10 }, { shot = "55_soothe_bell.png" }, { press = K.A, wait = 160 },
    { shot = "55_soothe_bell_pocket.png" }, { press = K.A, wait = 40 },
    { expect_flag = FLAG_ICHOR_GOT_SOOTHE_BELL, why = "Aigon did not give the Soothe Bell" } },

  -- 8. the divers' house: Doris's grotto lore before the laurel; after it, her
  --    shell bell for the Heart Scale off the beach
  { { warp = { INDOOR, MAP_DIVERS, -1, 2, 4 }, wait = 100 },
    { shot = "60_divers_house.png" },
    { hold = K.UP, frames = 4, wait = 30 } },
  L.talk("61_doris_lore", 6, 30),
  { { warp = { AKTI, MAP_AKTI, -1, 22, 9 }, wait = 240 },   -- the Heart Scale is hidden at (23,9)
    { hold = K.RIGHT, frames = 4, wait = 30 } },
  L.talk("62_heart_scale", 1, 160),
  { { press = K.A, wait = 40 }, { press = K.A, wait = 40 },
    { flag = FLAG_BADGE01_GET },
    { warp = { INDOOR, MAP_DIVERS, -1, 2, 4 }, wait = 100 },
    { hold = K.UP, frames = 4, wait = 30 } },
  L.talk("63_doris_trade", 5, 30),             -- three lines, then YES to the trade
  { { wait = 10 }, { shot = "64_shell_bell.png" }, { press = K.A, wait = 160 },
    { shot = "64_shell_bell_pocket.png" }, { press = K.A, wait = 40 } },
  L.talk("65_doris_after", 2, 30),
  { { expect_flag = FLAG_ICHOR_GOT_SHELL_BELL, why = "Doris did not trade her shell bell" },
    { flag = FLAG_BADGE01_GET, set = false },
    { shot = "66_end.png" } }
)

L.run("AKTI", OUT, steps)
