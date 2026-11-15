-- Walk test for the player's overworld sprites (Theo and Ianthe).
--
--   build/tools/ichor-mgba-headless --script tools/ichor/tests/player_ow_walk.lua \
--       --frames 4200 --until "WALK done" pokeemerald.gba
--
-- Env: WALK_GENDER=0 for Theo (default) or 1 for Ianthe; WALK_OUT is the
-- screenshot folder (default build/walk_test/, which must exist).
--
-- Quickstarts a new game (the smoke test's timing), forces the player's gender
-- (Quickstart picks one at random) and gives the running shoes, then in the
-- bedroom walks 2 tiles up, down, left and right, and runs the same way while
-- holding B. It screenshots every 2 frames while moving, so every walk and run
-- frame and both facings of the side view are caught mid-step.
-- tools/ichor/art/sprites_player_ow_review.py crops these into review sheets.
--
-- Pokes memory: gSaveBlock2Ptr->playerGender, and FLAG_SYS_B_DASH in
-- gSaveBlock1Ptr->flags. Pointer addresses come from pokeemerald.map; the
-- offsets are from include/global.h (SaveBlock2.playerGender at 0x08,
-- SaveBlock1.flags at 0x1270) and FLAG_SYS_B_DASH = SYSTEM_FLAGS + 0x60 (SYSTEM_FLAGS is 0x500 + MAX_TRAINERS_COUNT_EMERALD,
-- read from include/constants/opponents.h).

local OUT = os.getenv("WALK_OUT") or "build/walk_test/"
local GENDER = tonumber(os.getenv("WALK_GENDER") or "0")
local K = C.GBA_KEY

local GENDER_OFFSET = 0x08
local FLAGS_OFFSET = 0x1270
local FLAG_SYS_B_DASH = (function()
  local f = io.open("include/constants/opponents.h", "r")
  local count
  if f then
    for line in f:lines() do
      count = count or tonumber(line:match("^#define MAX_TRAINERS_COUNT_EMERALD%s+(%d+)"))
    end
    f:close()
  end
  return 0x500 + (count or 864) + 0x60
end)()

local function sym(name)
  local f = io.open("pokeemerald.map", "r")
  if not f then return nil end
  local addr
  for line in f:lines() do
    addr = line:match("^%s+0x(%x+)%s+" .. name .. "%s*$")
    if addr then break end
  end
  f:close()
  return addr and tonumber(addr, 16)
end

local SB1 = sym("gSaveBlock1Ptr")
local SB2 = sym("gSaveBlock2Ptr")
if not (SB1 and SB2) then console:log("WALK FAIL: no save block pointers in pokeemerald.map") end

local function forceGender()
  if SB2 then emu:write8(emu:read32(SB2) + GENDER_OFFSET, GENDER) end
end

local function giveRunningShoes()
  if SB1 then
    local byte = emu:read32(SB1) + FLAGS_OFFSET + (FLAG_SYS_B_DASH >> 3)
    emu:write8(byte, emu:read8(byte) | (1 << (FLAG_SYS_B_DASH & 7)))
  end
end

-- Moves after the map has loaded: keys held for `len` frames, then a pause.
local START = 2500
local moves = {
  { name = "walk_up",    keys = { K.UP },          len = 44 },
  { name = "walk_down",  keys = { K.DOWN },        len = 44 },
  { name = "walk_left",  keys = { K.LEFT },        len = 44 },
  { name = "walk_right", keys = { K.RIGHT },       len = 44 },
  { name = "run_left",   keys = { K.B, K.LEFT },   len = 28 },
  { name = "run_right",  keys = { K.B, K.RIGHT },  len = 28 },
  { name = "run_up",     keys = { K.B, K.UP },     len = 28 },
  { name = "run_down",   keys = { K.B, K.DOWN },   len = 28 },
}
local PAUSE = 24

-- frame -> list of actions
local schedule = {}
local function at(f, action)
  schedule[f] = schedule[f] or {}
  table.insert(schedule[f], action)
end

at(500, { press = K.START })   -- skip the intro
at(1020, { press = K.SELECT }) -- Quickstart
at(START - 10, { shot = "00_stand.png" })

local f = START
for i, m in ipairs(moves) do
  at(f, { hold = m.keys })
  for t = 0, m.len + 8, 2 do
    at(f + t, { shot = string.format("%02d_%s_%03d.png", i, m.name, t) })
  end
  at(f + m.len, { release = m.keys })
  f = f + m.len + PAUSE
end
at(f, { done = true })

local pressed, releaseAt = nil, 0

callbacks:add("frame", function()
  local fr = emu:currentFrame()
  if pressed and fr >= releaseAt then emu:clearKey(pressed); pressed = nil end
  if fr > 1020 and fr < START then forceGender() end
  if fr >= START - 100 and fr < START then giveRunningShoes() end
  local steps = schedule[fr]
  if not steps then return end
  for _, s in ipairs(steps) do
    if s.press then emu:addKey(s.press); pressed = s.press; releaseAt = fr + 6 end
    if s.hold then for _, k in ipairs(s.hold) do emu:addKey(k) end end
    if s.release then for _, k in ipairs(s.release) do emu:clearKey(k) end end
    if s.shot then emu:screenshot(OUT .. s.shot) end
    if s.done then
      local g = SB2 and emu:read8(emu:read32(SB2) + GENDER_OFFSET)
      console:log("WALK gender " .. tostring(g) .. " (wanted " .. GENDER .. ")")
      console:log("WALK done at frame " .. fr) -- the runner stops on this line
    end
  end
end)
