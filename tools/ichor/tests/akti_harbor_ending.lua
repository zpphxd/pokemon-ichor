-- Akti harbor ending check: SCRIPT.md beat 8, "when the winds turn".
--
--   mkdir -p build/akti_ending && build/tools/ichor-mgba-headless \
--       --script tools/ichor/tests/akti_harbor_ending.lua --frames 12000 --until "ENDING done" pokeemerald.gba
--
-- Env: ENDING_OUT is the screenshot folder (default build/akti_ending/, which must exist).
-- Quickstarts a new game and sets what the temple agent's trial and Ione's battle
-- leave behind (FLAG_BADGE01_GET, FLAG_ICHOR_HEARTH_TRIAL_DONE), plus what an earlier
-- visit to Akti leaves (FLAG_ICHOR_ARRIVED_AKTI, FLAG_ICHOR_HIDE_ALETHEA_AKTI). Then:
--   1. Arrives through the temple's door (Akti warp 3): part 1 plays on the doorstep.
--   2. Loads the quay just east of the trireme's end and steps west across the
--      trigger line: part 2 plays, Kleon's deal is taken, the slice ends.
-- Passes when FLAG_ICHOR_SLICE_COMPLETE and the hide flags are set at the end.

local L = dofile("tools/ichor/tests/ichor_lib.lua")
local K = L.K
local OUT = os.getenv("ENDING_OUT") or "build/akti_ending/"

local AKTI, MAP_AKTI = 0, 59
local FLAG_BADGE01_GET = L.system_flag(0x7)
local FLAG_ICHOR_ARRIVED_AKTI = 0x2E
local FLAG_ICHOR_HEARTH_TRIAL_DONE = 0x30
local FLAG_ICHOR_SLICE_COMPLETE = 0x33
local FLAG_ICHOR_HIDE_KLEON_AKTI = 0x43
local FLAG_ICHOR_HIDE_ALETHEA_AKTI = 0x44

local steps = L.seq(
  L.quickstart(),
  { { instant_text = true },
    { flag = FLAG_BADGE01_GET },
    { flag = FLAG_ICHOR_HEARTH_TRIAL_DONE },
    { flag = FLAG_ICHOR_ARRIVED_AKTI },
    { flag = FLAG_ICHOR_HIDE_ALETHEA_AKTI, wait = 2 },

    -- 1. out of the temple door at (19,16); the player walks down onto the step
    { warp = { AKTI, MAP_AKTI, 3, 19, 16 }, wait = 60 },
    { shot = "01_leaving_temple.png", wait = 60 },
    { shot = "02_alethea_runs_in.png", wait = 120 } },
  L.talk("03_alethea", 7, 30),                -- six boxes, then the last A closes them
  { { wait = 40 }, { shot = "04_alethea_heads_for_quay.png", wait = 120 },
    { shot = "05_part1_done.png" },
    { expect_flag = FLAG_ICHOR_HIDE_ALETHEA_AKTI, set = false, why = "part 1 did not show Alethea" },

    -- 2. the quay: from (11,10), one step west onto the line x = 10
    { warp = { AKTI, MAP_AKTI, -1, 11, 10 }, wait = 220 },
    { shot = "06_quay.png" },
    { hold = K.LEFT, frames = 10, wait = 90 } },
  L.talk("07_captain", 8, 30),                -- Alethea, Nausikles, Alethea, Nausikles x5
  L.talk("08_kleon", 5, 30),                  -- Kleon x5, the last with YES/NO
  { { shot = "09_deal_yes.png" }, { press = K.A, wait = 30 },      -- YES
    { shot = "10_shipmate.png" }, { press = K.A, wait = 50 },      -- Kleon walks off
    { shot = "10_kleon_leaving_a.png", wait = 70 },
    { shot = "10_kleon_leaving_b.png", wait = 80 },
    { shot = "11_facing_the_sea.png", wait = 80 } },
  L.talk("12_ribbon", 2, 40),
  { { wait = 60 }, { shot = "13_thank_you.png" }, { press = K.A, wait = 120 },
    { shot = "14_back_to_the_harbor.png" },
    { expect_flag = FLAG_ICHOR_SLICE_COMPLETE, why = "FLAG_ICHOR_SLICE_COMPLETE was not set" },
    { expect_flag = FLAG_ICHOR_HIDE_KLEON_AKTI, why = "Kleon was not hidden after the ending" },
    { expect_flag = FLAG_ICHOR_HIDE_ALETHEA_AKTI, why = "Alethea was not hidden after the ending" },

    -- the harbor after the slice: Nausikles's last line
    { warp = { AKTI, MAP_AKTI, -1, 7, 10 }, wait = 220 },
    { hold = K.UP, frames = 4, wait = 30 } },
  L.talk("15_nausikles_after", 2, 40)
)

L.run("ENDING", OUT, steps)
