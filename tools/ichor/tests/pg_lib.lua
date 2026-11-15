-- Shared helpers for the post-game's headless checks (load with dofile), on top
-- of tools/ichor/tests/engine_lib.lua (read engine_build.sh first).
--
--   local L = dofile("tools/ichor/tests/pg_lib.lua")   -- engine_lib, extended
--   L.start(function()
--     L.pgStart()                       -- new game, post-game ready, at Akti's quay
--     L.warp(S.MAP_KALLISTE_ROUTE1, 10, 10)
--     L.setHour(22)                     -- night
--     ...
--   end)
--
-- A post-game check is built like the engine checks: pg_<area>.sh calls
-- engine_prepare and engine_run; pg_<area>_consts.c includes engine_consts.h and
-- adds its own k_NAME constants; pg_<area>_setup.s #includes pg_setup.inc (the
-- shared headers below rely on it) and adds its own. Its consts must define the
-- IchorEpics offsets (OFF_ICHOR_EPICS and OFF_EPICS_*), as pg_sailing_consts.c
-- does, for L.epic8 and friends.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu

-- --- Starting --------------------------------------------------------------------------------

-- A new game, then the post-game ready (pg_setup.inc's PgLib_SetupHeader):
-- FLAG_ICHOR_POSTGAME, a Lv 70 party of six (Lapras leads), every relic in the
-- bag, FLAG_ICHOR_GOT_EUPLOIA, the clock started, the slice's scenes done, a
-- Repel that keeps the low-level tables away; then Akti at (x, y), by default
-- the quay just south of the gangplank.
function L.pgStart(x, y)
  L.quickstart()
  L.setVar(S.VAR_0x8008, x or 7); L.setVar(S.VAR_0x8009, y or 10)
  L.runHeader("PgLib_SetupHeader", { limit = 6000 })
  L.waitUntil(function() return L.idle() end, 3000, "the post-game setup")
  L.wait(30)
end

function L.setPostgame(on) L.setFlag(S.FLAG_ICHOR_POSTGAME, on ~= false) end

-- Wild encounters on or off (off is a long Repel, which a Lv 70 lead turns
-- into no encounters at all on low-level tables).
function L.encounters(on) L.setVar(S.VAR_REPEL_STEP_COUNT, on and 0 or 999) end

-- --- Anywhere, at any hour ---------------------------------------------------------------------

-- Load `map` (a MAP_* value: (group << 8) | num) with the player at (x, y),
-- as a door warp's map load does, without the fade. A water tile puts the player
-- in the surf state, and in the ship while FLAG_ICHOR_ON_SHIP is set.
function L.warp(map, x, y)
  local sb = L.sb1()
  emu:write16(sb + S.OFF_SB1_POS, x)
  emu:write16(sb + S.OFF_SB1_POS + 2, y)
  local loc = sb + S.OFF_SB1_LOCATION
  emu:write8(loc, map >> 8); emu:write8(loc + 1, map & 0xFF); emu:write8(loc + 2, 0xFF)
  emu:write16(loc + 4, x); emu:write16(loc + 6, y)
  emu:write32(S.gMain + S.OFF_MAIN_CALLBACK2, S.CB2_LoadMap | 1)
  L.waitUntil(function() return L.mapId() == map and L.idle() end, 3000, string.format("map %d", map))
  L.wait(20)
end

-- The game's clock as (days, hours, minutes, seconds) structs: local time is the
-- RTC minus the saved offset (src/rtc.c).
local function readTime(a)
  local function s8(v) if v >= 0x80 then return v - 0x100 end return v end
  local d = emu:read16(a); if d >= 0x8000 then d = d - 0x10000 end
  return d, s8(emu:read8(a + 2)), s8(emu:read8(a + 3)), s8(emu:read8(a + 4))
end

-- Set the local hour (0-23), keeping the day, so no daily reset runs. The
-- overworld picks up the new time of day on its next frame.
function L.setHour(hour)
  local off = L.sb2() + S.OFF_SB2_LOCAL_TIME_OFFSET
  local ld, lh, lm, ls = readTime(S.gLocalTime)
  local od, oh, om, os = readTime(off)
  local rtc = (ld + od) * 86400 + (lh + oh) * 3600 + (lm + om) * 60 + (ls + os)
  local n = rtc - (ld * 86400 + hour * 3600)
  local nd = n // 86400; n = n - nd * 86400
  local nh = n // 3600; n = n - nh * 3600
  local nm = n // 60
  emu:write16(off, nd & 0xFFFF); emu:write8(off + 2, nh); emu:write8(off + 3, nm); emu:write8(off + 4, n - nm * 60)
  emu:write16(S.gTimeUpdateCounter, 0)
  L.wait(4)
end
function L.night() L.setHour(22) end
function L.day() L.setHour(12) end
function L.timeOfDay() return emu:read8(S.gTimeOfDay) end

-- A new day: the clock goes a day on and the time-based events run (the daily
-- flags clear, the daily seed turns, the wind changes).
function L.newDay()
  local off = L.sb2() + S.OFF_SB2_LOCAL_TIME_OFFSET
  emu:write16(off, (emu:read16(off) - 1) & 0xFFFF)
  L.runHeader("PgLib_DayHeader")
end

-- Save, reset, CONTINUE.
function L.saveAndReload()
  L.runHeader("PgLib_SaveHeader")
  emu:reset()
  L.continueSave()
end

-- --- IchorSave.epics ---------------------------------------------------------------------------

function L.epics() return L.ichor() + S.OFF_ICHOR_EPICS end
-- A field by its offset name: L.epic8("WIND"), L.setEpic8("SHIP_PORT", 1).
function L.epic8(name) return emu:read8(L.epics() + S["OFF_EPICS_" .. name]) end
function L.setEpic8(name, v) emu:write8(L.epics() + S["OFF_EPICS_" .. name], v) end
function L.epic16(name) return emu:read16(L.epics() + S["OFF_EPICS_" .. name]) end
function L.setEpic16(name, v) emu:write16(L.epics() + S["OFF_EPICS_" .. name], v) end
function L.epicsBytes() return L.snapshot(L.epics(), S.ICHOR_EPICS_SIZE) end

-- --- Steps, keys and the player -----------------------------------------------------------------

-- One step (L.step: "moved", "blocked" or "taken"); a tap; a key held for n frames.
L.press = L.tap
function L.hold(key, frames) emu:addKey(key); L.wait(frames); emu:clearKey(key); L.wait(2) end

function L.graphicsId() return emu:read16(L.playerObject() + S.OFF_OBJ_GRAPHICS_ID) end
function L.movementAction() return emu:read8(L.playerObject() + S.OFF_OBJ_MOVEMENT_ACTION) end
function L.surfing() return emu:read8(S.gPlayerAvatar + S.OFF_AVATAR_FLAGS) & S.PLAYER_AVATAR_FLAG_SURFING ~= 0 end
function L.sprite(id) return S.gSprites + id * S.SPRITE_SIZE end
function L.spriteVisible(id)
  local sp = L.sprite(id)
  return emu:read16(sp + S.OFF_SPRITE_FLAGS) & S.SPRITE_FLAG_IN_USE ~= 0
     and emu:read16(sp + S.OFF_SPRITE_FLAGS) & S.SPRITE_FLAG_INVISIBLE == 0
end
-- The sprite id of an in-use sprite running `callback` (a symbol), or nil.
function L.findSprite(callback)
  for i = 0, S.MAX_SPRITES - 1 do
    local sp = L.sprite(i)
    if emu:read16(sp + S.OFF_SPRITE_FLAGS) & S.SPRITE_FLAG_IN_USE ~= 0
       and emu:read32(sp + S.OFF_SPRITE_CALLBACK) & ~1 == S[callback] then return i end
  end
end

-- Open a scrolling menu entry: wait for the menu, press DOWN `n` times, then A.
function L.pickMenu(n, what)
  L.waitUntil(function() return L.taskRunning("Task_HandleScrollingMultichoiceInput") end, 600, what or "a menu")
  L.wait(10)
  for _ = 1, n do L.tap(K.DOWN); L.wait(2) end
  L.tap(K.A)
  L.waitUntil(function() return not L.taskRunning("Task_HandleScrollingMultichoiceInput") end, 120, "the menu to close")
end

-- --- Text in the game's charset ----------------------------------------------------------------

local CHARS = { [" "] = 0x00, ["."] = 0xAD, ["-"] = 0xAE, [","] = 0xB8, [":"] = 0xF0, ["!"] = 0xAB, ["?"] = 0xAC }
-- `s` (letters, digits, space and . - , : ! ?) as game-charset bytes, without EOS.
function L.encode(s)
  local out = {}
  for c in s:gmatch(".") do
    local b = c:byte()
    if b >= 65 and b <= 90 then out[#out + 1] = 0xBB + b - 65
    elseif b >= 97 and b <= 122 then out[#out + 1] = 0xD5 + b - 97
    elseif b >= 48 and b <= 57 then out[#out + 1] = 0xA1 + b - 48
    else out[#out + 1] = assert(CHARS[c], "pg_lib.encode: no charset byte for " .. c) end
  end
  return out
end
-- Whether the string at `addr` starts with `s`.
function L.textAt(addr, s)
  for i, b in ipairs(L.encode(s)) do
    if emu:read8(addr + i - 1) ~= b then return false end
  end
  return true
end
-- Whether `s` appears anywhere in the first 1,000 bytes at `addr` (up to EOS).
function L.textContains(addr, s)
  local want = L.encode(s)
  local hay = {}
  for i = 0, 999 do
    local b = emu:read8(addr + i)
    if b == 0xFF then break end
    hay[#hay + 1] = b
  end
  for i = 1, #hay - #want + 1 do
    local ok = true
    for j = 1, #want do if hay[i + j - 1] ~= want[j] then ok = false break end end
    if ok then return true end
  end
  return false
end

return L
