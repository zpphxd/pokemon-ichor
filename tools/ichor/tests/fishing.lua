-- Cast the Old Rod at one shore cell until something bites: run by fishing.sh
-- (read it first), once per spot.
--
-- Quickstarts, gives a test Pokémon, puts the Old Rod in the key pocket and
-- registers it on SELECT, then warps to FISH_SPOT's cell, turns to face the
-- water and casts. Each frame it reads the fishing task's step (src/fishing.c):
-- at "Oh! A bite!" (FISHING_WAIT_FOR_A) it presses A to reel in; after "Not
-- even a nibble" it clears the box and casts again. It passes when the hooked
-- Pokémon's battle starts (gIsFishingEncounter), and fails if the rod is refused
-- (no fishing task after SELECT: "There's a time and place...") or nothing bites
-- in MAX_CASTS casts.

local L = dofile("tools/ichor/tests/ichor_lib.lua")
local S = dofile(os.getenv("FISH_SYMBOLS"))
local OUT = os.getenv("FISH_OUT")
local SPOT = os.getenv("FISH_SPOT")
local K = L.K
local TAG = "FISH " .. SPOT

-- spot: map, the shore cell, the key that faces the water
local SPOTS = {
  route8 = { S.MAP_ROUTE8_KOPAIS_ROAD, 21, 13, K.DOWN },     -- the screenshot's sand path, facing south
  kirrha = { S.MAP_KIRRHA, 5, 22, K.DOWN },
  neraida = { S.MAP_KYTHERA_NERAIDA_FALLS, 19, 14, K.UP },
  route12 = { S.MAP_ROUTE12_CYPRESS_ROAD, 29, 29, K.LEFT },
}
local spot = assert(SPOTS[SPOT], "unknown FISH_SPOT " .. tostring(SPOT))
local MAX_CASTS = 40
-- src/fishing.c's steps
local WAIT_FOR_A, MON_ON_HOOK, START_ENCOUNTER, NOT_EVEN_NIBBLE, GOT_AWAY = 8, 11, 12, 13, 14

local function sb1() return emu:read32(S.gSaveBlock1Ptr) end
local function sb2() return emu:read32(S.gSaveBlock2Ptr) end

local function fishing_step()
  for t = 0, 15 do
    local a = S.gTasks + t * S.TASK_SIZE
    if emu:read8(a + 4) ~= 0 and (emu:read32(a) | 1) == (S.Task_Fishing | 1) then
      return emu:read16(a + S.OFF_TASK_DATA)
    end
  end
  return nil
end

local function give_rod()
  local base = sb1() + S.OFF_SB1_BAG + S.OFF_BAG_KEY
  local key = emu:read32(sb2() + S.OFF_SB2_KEY) & 0xFFFF
  emu:write16(base, S.ITEM_OLD_ROD)
  emu:write16(base + 2, 1 ~ key)
  emu:write16(sb1() + S.OFF_SB1_REGISTERED, S.ITEM_OLD_ROD)
end

local setup = L.seq(L.quickstart(), {
  { instant_text = true, give_mon = 0x19 },
  { check = function() give_rod(); return true, "Old Rod in the bag, on SELECT" end },
  { warp = { spot[1] >> 8, spot[1] & 0xFF, -1, spot[2], spot[3] }, wait = 180 },
  { hold = spot[4], frames = 3, wait = 30 },
  { shot = SPOT .. "_0_shore.png" },
})

local last_step, landed
local phase, casts, waitUntil, idle, hooked, cast_seen, released = "setup", 0, 0, 0, false, false, {}
local function finish() console:log(TAG .. " finished"); phase = "done" end
L.run(TAG .. " setup", OUT, setup)
local function tick()
  local f = emu:currentFrame()
  for k, at in pairs(released) do
    if f >= at then emu:clearKey(k); released[k] = nil end
  end
  local function press(key) emu:addKey(key); released[key] = f + 4 end
  if phase == "setup" then
    if f > 2800 then phase = "cast" end
    return
  end
  if f < waitUntil or phase == "done" then return end
  local step = fishing_step()
  if step ~= last_step then
    console:log(string.format("%s step %s at %d (cast %d)", TAG, tostring(step), f, casts))
    last_step = step
  end
  if phase == "cast" then
    if casts >= MAX_CASTS then
      console:log(TAG .. " FAIL: nothing bit in " .. casts .. " casts")
      finish(); return
    end
    casts = casts + 1
    press(K.SELECT)
    phase, idle, waitUntil = "fishing", 0, f + 20
  elseif phase == "fishing" then
    if emu:read8(S.gIsFishingEncounter) ~= 0 then
      console:log(string.format("%s ok: battle after %d cast(s)", TAG, casts))
      phase, waitUntil = "battle", f + 420
    elseif step == nil then
      idle = idle + 1
      if idle > 90 then
        if not cast_seen then  -- SELECT never started the rod: "There's a time and place..."
          emu:screenshot(OUT .. SPOT .. "_x_refused.png")
          console:log(TAG .. " FAIL: the rod was refused (no fishing task after SELECT)")
          finish(); return
        end
        phase = "cast"
      end
    else
      cast_seen = true
      idle = 0
      if step == WAIT_FOR_A then
        if not hooked then emu:screenshot(OUT .. SPOT .. "_1_bite.png") end
        hooked = true
        press(K.A); waitUntil = f + 6
      elseif step == NOT_EVEN_NIBBLE or step == GOT_AWAY or step > GOT_AWAY then
        press(K.A); waitUntil = f + 10
      elseif step == MON_ON_HOOK or step == START_ENCOUNTER then
        -- "A Pokémon's on the hook!": the box waits for a press before the battle
        if not landed then emu:screenshot(OUT .. SPOT .. "_2_hooked.png") end
        landed = true
        press(K.A); waitUntil = f + 20
      end
    end
  elseif phase == "battle" then
    emu:screenshot(OUT .. SPOT .. "_3_battle.png")
    console:log(TAG .. " PASS")
    finish()
  end
end
callbacks:add("frame", function()
  local ok, err = pcall(tick)
  if not ok then console:log(TAG .. " FAIL: lua error " .. tostring(err)); finish() end
end)
