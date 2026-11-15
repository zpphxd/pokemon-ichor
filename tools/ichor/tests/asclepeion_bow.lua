-- Asclepeion bow check: both heal scripts end with the healer's bow and give
-- the player back control.
--
--   mkdir -p build/bow_test && build/tools/ichor-mgba-headless \
--       --script tools/ichor/tests/asclepeion_bow.lua --frames 9000 --until "BOW done" pokeemerald.gba
--
-- Env: BOW_OUT is the screenshot folder (default build/bow_test/, which must exist).
-- Movement_PkmnCenterNurse_Bow plays ANIM_NURSE_BOW (frame 9), which only
-- sAnimTable_Nurse has. A healer on another table never finishes the movement
-- and waitmovement holds the player forever. Two runs through it:
--   1. Talk to the healer and heal: she bows, "Go in health.", then the player
--      walks away from the counter.
--   2. White out (gMain.callback2 = CB2_WhiteOut, the call a lost battle ends
--      in) with Akti as the last heal point: the respawn heal in the Asclepeion
--      ends with the same bow, then the player walks away.
-- Text is advanced with B where possible: once the script releases the player,
-- B does nothing, while A would start another conversation over the counter.

local L = dofile("tools/ichor/tests/ichor_lib.lua")
local K = L.K
local OUT = os.getenv("BOW_OUT") or "build/bow_test/"

local AKTI, MAP_AKTI = L.map("MAP_AKTI_TOWN")
local INDOOR, MAP_ASCLEPEION = L.map("MAP_AKTI_TOWN_ASCLEPEION")
local HEALER_LOCALID = 1                 -- LOCALID_AKTI_HEALER, the map's first object
local ANIM_NURSE_BOW = 20                -- ANIM_STD_COUNT + 0

local OBJ_EVENTS, OBJ_SIZE = L.sym("gObjectEvents"), 0x24
local SPRITES, SPRITE_SIZE = L.sym("gSprites"), 0x44
local CB2_WHITEOUT = L.sym("CB2_WhiteOut")
local healing = os.getenv("HEAL_SYMBOLS") and dofile("tools/ichor/tests/asclepeion_healing.lua")

local function obj_where(pred)
  for i = 0, 15 do
    local a = OBJ_EVENTS + i * OBJ_SIZE
    if emu:read8(a) & 1 == 1 and pred(a) then return a end
  end
end

local function player_xy()
  local a = obj_where(function(o) return emu:read8(o + 2) & 1 == 1 end)
  if not a then return nil end
  return emu:read16(a + 0x10) - 7, emu:read16(a + 0x12) - 7
end

local function healer()
  return obj_where(function(o)
    return emu:read8(o + 8) == HEALER_LOCALID and emu:read8(o + 9) == MAP_ASCLEPEION
       and emu:read8(o + 10) == INDOOR
  end)
end

-- Watch the healer's sprite every frame: count the frames she spends in the
-- bow's held pose (ANIM_NURSE_BOW, command 1: FRAME(9, 32)).
local bowFrames, lastAnim = 0, nil
callbacks:add("frame", function()
  local h = healer()
  if not h then return end
  local s = SPRITES + emu:read8(h + 0x23) * SPRITE_SIZE
  local anim, cmd = emu:read8(s + 0x2A), emu:read8(s + 0x2B)
  if anim == ANIM_NURSE_BOW and cmd == 1 then bowFrames = bowFrames + 1 end
  if anim ~= lastAnim then
    console:log(string.format("BOW healer anim %d at frame %d", anim, emu:currentFrame()))
    lastAnim = anim
  end
end)

local function expect_bow(phase)
  return { check = function()
    local n = bowFrames
    bowFrames = 0
    -- FRAME(9, 32): a stuck animation runs long, a missing one never starts
    local healed = not healing or healing.validate(phase)
    return n == 32 and healed,
           string.format("%s: healer held the bow frame for %d frames; want 32", phase, n)
  end }
end

local function expect_walked_away(phase)
  return {
    { hold = K.DOWN, frames = 24, wait = 40 },
    { check = function()
        local x, y = player_xy()
        return x == 7 and y == 5,
               string.format("%s: player at (%s,%s) after holding DOWN; want (7,5)", phase, x, y)
      end },
  }
end

local function presses(key, n, gap, prefix)
  local out = {}
  for k = 1, n do
    table.insert(out, { shot = string.format("%s_%02d.png", prefix, k) })
    table.insert(out, { press = key, wait = gap })
  end
  return out
end

local steps = L.seq(
  L.quickstart(),
  healing and { { check = healing.prepare_player } } or {},
  { { instant_text = true },
    { give_mon = 7, wait = 2 } },

  -- 1. talk to the healer across the counter from (7,4)
  { { warp = { INDOOR, MAP_ASCLEPEION, -1, 7, 4 }, wait = 100 },
    { hold = K.UP, frames = 4, wait = 30 } },
  -- talk, "Welcome", "We tend tired Pokémon", YES
  presses(K.A, 4, 30, "10_talk"),
  { { wait = 310 } },                          -- the spring's heal jingle
  -- "Whole and well" (the bow follows), then "Go in health."
  { { shot = "11_restored.png" }, { press = K.B, wait = 12 },
    { shot = "12_bow_a.png", wait = 14 }, { shot = "13_bow_b.png", wait = 40 },
    { shot = "14_go_in_health.png" } },
  presses(K.B, 3, 30, "15_close"),
  { expect_bow("talk") },
  expect_walked_away("talk"),
  { { shot = "16_walked_away.png" } },

  -- 2. white out with Akti as the last heal point
  { { check = function()
        local g, n, x, y = L.last_heal()
        return g == AKTI and n == MAP_AKTI,
               string.format("last heal point is map %d.%d before the whiteout; want Akti", g, n)
      end },
    { check = function()
        emu:write32(L.MAIN, 0)                  -- callback1: no overworld while it counts down
        emu:write8(L.MAIN + 0x438, 0)           -- gMain.state
        emu:write32(L.MAIN + 4, CB2_WHITEOUT | 1)
        return true, "whiteout started"
      end, wait = 300 },
    { wait = 60 } },
  -- "...hurried to the Asclepeion", "Let's tend your Pokémon first.", the
  -- jingle, then three pages of advice
  presses(K.B, 1, 330, "20_rushed"),
  presses(K.B, 1, 330, "21_first"),
  presses(K.B, 3, 40, "22_advice"),
  { { shot = "23_bow.png", wait = 60 } },
  presses(K.B, 2, 30, "24_after"),
  { expect_bow("whiteout") },
  expect_walked_away("whiteout"),
  { { shot = "25_walked_away.png" } }
)

L.run("BOW", OUT, steps)
