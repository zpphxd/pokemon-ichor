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
--      Then a trip into the Asclepeion and out (QA M2): part 2 must still be waiting.
--   2. Loads the quay just east of the trireme's end and steps west across the
--      trigger line: part 2 plays, Kleon's deal is taken, the slice ends.
-- Passes when FLAG_ICHOR_SLICE_COMPLETE and Kleon's hide flag are set at the end, and Alethea
-- stays on the quay (Phase 2's pointer to Halia).

local L = dofile("tools/ichor/tests/ichor_lib.lua")
local K = L.K
local OUT = os.getenv("ENDING_OUT") or "build/akti_ending/"

local AKTI, MAP_AKTI = L.map("MAP_AKTI_TOWN")
local INDOOR, MAP_ASCLEPEION = L.map("MAP_AKTI_TOWN_ASCLEPEION")
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

    -- QA M2: a trip indoors between the parts must not lose part 2 or replay part 1.
    -- By now Alethea has walked off and been put back at the quay, and her hide
    -- flag must still be clear.
    { wait = 240 },
    { expect_flag = FLAG_ICHOR_HIDE_ALETHEA_AKTI, set = false,
      why = "after part 1 Alethea's hide flag is set, so a trip indoors replays part 1 (QA M2)" },
    { warp = { INDOOR, MAP_ASCLEPEION, -1, 7, 9 }, wait = 120 },
    { shot = "05b_indoors_mid_ending.png" },
    { warp = { AKTI, MAP_AKTI, 1, 3, 22 }, wait = 220 },
    { shot = "05c_back_out.png" },
    { expect_flag = FLAG_ICHOR_HIDE_ALETHEA_AKTI, set = false,
      why = "a trip indoors set Alethea's hide flag again (QA M2)" },

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
  -- Phase 2: no farewell card. Alethea turns round with Halia's message (beat 9A's pointer).
  { { wait = 30 }, { shot = "13_halia_sent_a_gull.png" } },
  L.talk("13_pointer", 2, 40),
  { { wait = 60 }, { shot = "14_after_the_end.png" },
    { expect_flag = FLAG_ICHOR_SLICE_COMPLETE, why = "FLAG_ICHOR_SLICE_COMPLETE was not set" },
    { expect_flag = FLAG_ICHOR_HIDE_KLEON_AKTI, why = "Kleon was not hidden after the ending" },
    { expect_flag = FLAG_ICHOR_HIDE_ALETHEA_AKTI, set = false,
      why = "Alethea should wait on the quay after the ending (Phase 2's pointer to Halia)" },

    -- the harbor after the slice: Nausikles's last line (from beside him; Alethea is on (7,10))
    { warp = { AKTI, MAP_AKTI, -1, 6, 9 }, wait = 220 },
    { hold = K.RIGHT, frames = 4, wait = 30 } },
  L.talk("15_nausikles_after", 2, 40)
)

L.run("ENDING", OUT, steps)
