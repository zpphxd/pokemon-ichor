-- The Frozen Hour check, run by tools/ichor/tests/ichor_frozen.sh (read it first).

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local log, expect, wait, shot, settle = L.log, L.expect, L.wait, L.shot, L.settle

local PX, PY = 6, 45                 -- in Route 1's south grass
local WOOLOO_A, WOOLOO_B = 5, 6      -- the two wandering Wooloo (one palette)
local YOUTH = 3                      -- the youth, rewritten as caught mid-stride
local YX, YY = 8, 44

-- --- Palettes and objects ---------------------------------------------------------------
local function bgPal(slot) return S.gPlttBufferUnfaded + slot * 32 end
local function objPal(slot) return S.gPlttBufferUnfaded + 0x200 + slot * 32 end
local function colors(addr)
  local t = {}
  for i = 0, 15 do t[i] = emu:read16(addr + i * 2) end
  return t
end
local function rgb(c) return c & 31, (c >> 5) & 31, (c >> 10) & 31 end
local function isGray(addr)
  for i = 0, 15 do
    local r, g, b = rgb(emu:read16(addr + i * 2))
    if r ~= g or g ~= b then return false end
  end
  return true
end
local function same(a, b)
  for i = 0, 15 do if a[i] ~= b[i] then return false end end
  return true
end
local function grayBgCount()
  local n = 0
  for s = 0, 12 do if isGray(bgPal(s)) then n = n + 1 end end
  return n
end
local function obj(localId)
  for i = 0, S.OBJECT_EVENTS_COUNT - 1 do
    local o = S.gObjectEvents + i * S.OBJECT_EVENT_SIZE
    if emu:read8(o) & 1 == 1 and emu:read8(o + S.OFF_OBJ_LOCAL_ID) == localId then return o end
  end
end
local function frozen(o) return emu:read8(o + 1) & 1 == 1 end
local function sprite(o) return S.gSprites + emu:read8(o + S.OFF_OBJ_SPRITE_ID) * S.SPRITE_SIZE end
local function palSlot(o) return emu:read16(sprite(o) + S.OFF_SPRITE_OAM_ATTR2) >> 12 end
local function at(o)
  local c = o + S.OFF_OBJ_CURRENT_COORDS
  return emu:read16(c), emu:read16(c + 2)
end
local function setVar(v, n) L.setVar(v, n) end
local function run(header, opts) L.runHeader(header, opts) end
local function toRoute1(header)
  setVar(S.VAR_0x8008, PX); setVar(S.VAR_0x8009, PY)
  run(header, { limit = 4000 })
  L.waitUntil(function() return L.mapId() == S.MAP_ROUTE1 and L.idle() end, 3000, "Route 1")
  wait(40)
end

L.start(function()
  L.quickstart()
  toRoute1("FrozenTest_SetupHeader")

  -- The world before: a colorful BG slot, the flock's palette, the route's music
  local baseline, colorful, best = {}, 0, -1
  for s = 0, 12 do
    baseline[s] = colors(bgPal(s))
    local n = 0
    for i = 0, 15 do local r, g, b = rgb(baseline[s][i]) if r ~= g or g ~= b then n = n + 1 end end
    if n > best then colorful, best = s, n end
  end
  local wa, wb = obj(WOOLOO_A), obj(WOOLOO_B)
  expect(wa and wb, "both Wooloo are on screen")
  local woolSlot = palSlot(wa)
  local woolColors = colors(objPal(woolSlot))
  local routeMusic = L.mapMusic()
  shot("before")

  -- E4: a person caught mid-stride, facing west
  local t = L.sb1() + S.OFF_SB1_TEMPLATES
  for i = 0, 63 do
    local tpl = t + i * S.TEMPLATE_SIZE
    if emu:read8(tpl + S.OFF_TPL_LOCAL_ID) == YOUTH then
      emu:write8(tpl + S.OFF_TPL_MOVEMENT, S.MOVEMENT_TYPE_ICHOR_FROZEN_STEP_LEFT)
      emu:write16(tpl + S.OFF_TPL_X, YX)
      emu:write16(tpl + S.OFF_TPL_Y, YY)
      break
    end
  end
  setVar(S.VAR_0x8008, YOUTH)
  run("FrozenTest_RespawnHeader")
  wait(20)
  local youth = obj(YOUTH)
  local sp = youth and sprite(youth)
  local cmd0 = sp and emu:read8(sp + S.OFF_SPRITE_ANIM_CMD)
  wait(60)
  expect(sp and emu:read8(sp + S.OFF_SPRITE_ANIM_NUM) == S.ANIM_STD_GO_WEST and emu:read8(sp + S.OFF_SPRITE_ANIM_CMD) == cmd0,
         "MOVEMENT_TYPE_ICHOR_FROZEN_STEP_LEFT holds the walk west's stride")
  shot("mid_stride")

  -- E1: load the map with the hour's flag set
  toRoute1("FrozenTest_EnterHeader")
  wa, wb = obj(WOOLOO_A), obj(WOOLOO_B)
  local player = L.playerObject()
  expect(grayBgCount() == 13, string.format("every tileset palette is gray (%d of 13)", grayBgCount()))
  expect(isGray(objPal(palSlot(wa))) and not isGray(objPal(palSlot(player))),
         "the flock's palette is gray and the player's isn't")
  expect(frozen(wa) and frozen(wb), "the flock is frozen")
  expect(L.mapMusic() == S.MUS_ICHOR_ELPIS_LULLABY_BOX, "only the music box plays")
  local ax, ay = at(wa)
  local bx, by = at(wb)
  wait(300)
  local ax2, ay2 = at(wa)
  local bx2, by2 = at(wb)
  expect(ax == ax2 and ay == ay2 and bx == bx2 and by == by2, "five seconds on, the flock hasn't moved")
  shot("frozen")

  -- No wild Pokémon in the tall grass
  local steps, taken = 0, 0
  for _ = 1, 8 do
    for _, key in ipairs({ K.UP, K.UP, K.UP, K.DOWN, K.DOWN, K.DOWN }) do
      local r = L.step(key)
      if r == "moved" then steps = steps + 1 elseif r == "taken" then taken = taken + 1 end
      if L.inBattle() then taken = taken + 100 end
    end
  end
  expect(taken == 0 and steps >= 40, string.format("%d steps in tall grass, no battle", steps))

  -- A trainer doesn't see you
  for _, key in ipairs({ K.RIGHT, K.RIGHT, K.DOWN, K.DOWN, K.DOWN, K.DOWN, K.RIGHT }) do L.step(key) end
  local x, y = L.pos()
  wait(90)
  expect(x == 9 and y == 49 and L.idle() and not L.inBattle(), string.format("in the shepherd's sight at (%d,%d), he stays frozen", x, y))
  shot("unseen")

  -- releaseall doesn't thaw anyone
  run("FrozenTest_LockReleaseHeader")
  wait(30)
  expect(frozen(obj(WOOLOO_A)) and frozen(obj(WOOLOO_B)), "a script's releaseall leaves the flock frozen")

  -- E3: one Wooloo unfrozen; the color runs back in
  setVar(S.VAR_0x8004, WOOLOO_A)
  run("FrozenTest_UnfreezeHeader", { noSettle = true })
  wait(8)
  local mid = colors(objPal(woolSlot))
  local partly = not isGray(objPal(woolSlot)) and not same(mid, woolColors)
  wait(30)
  expect(partly, "eight frames in, the Wooloo's color is part way back")
  expect(same(colors(objPal(woolSlot)), woolColors), "then all the way")
  expect(not frozen(obj(WOOLOO_A)) and frozen(obj(WOOLOO_B)), "the unfrozen Wooloo is free and the other still held")
  shot("unfrozen")

  -- E5: a memory in sepia
  run("FrozenTest_SepiaBeginHeader")
  wait(4)
  local sepia = false
  for i = 1, 15 do
    local r, g, b = rgb(emu:read16(bgPal(colorful) + i * 2))
    if r > b then sepia = true end
  end
  expect(sepia and not isGray(bgPal(colorful)), "sepia: warm, not gray")
  shot("sepia")
  run("FrozenTest_SepiaEndHeader")
  wait(4)
  expect(isGray(bgPal(colorful)), "and back to gray")

  -- E6: the twelve steps of color
  for step = 1, 12 do
    setVar(S.VAR_0x8004, step)
    run("FrozenTest_ColorStepHeader")
    wait(4)
    if step == 6 then
      local now = colors(bgPal(colorful))
      expect(not isGray(bgPal(colorful)) and not same(now, baseline[colorful]), "halfway up the Stair, half the color")
      shot("half_color")
    end
  end
  wait(30)
  local restored = 0
  for s = 0, 12 do if same(colors(bgPal(s)), baseline[s]) then restored = restored + 1 end end
  expect(not L.getFlag(S.FLAG_ICHOR_FROZEN_HOUR) and restored == 13,
         string.format("step 12 ends the hour, every palette as it was (%d of 13)", restored))
  wait(240)
  expect(not frozen(obj(WOOLOO_B)) and L.mapMusic() == routeMusic, "the flock moves again and the route's music returns")
  shot("color_back")

  -- E2: the gray spreads from a point
  setVar(S.VAR_0x8004, 6); setVar(S.VAR_0x8005, 40)
  run("FrozenTest_BeginHeader", { noSettle = true })
  wait(24)
  local partway = grayBgCount()
  shot("spreading")
  L.waitUntil(L.idle, 900, "the gray to finish spreading")
  wait(10)
  expect(partway > 0 and partway < 13, string.format("part way through, %d of 13 palettes are gray", partway))
  expect(L.getFlag(S.FLAG_ICHOR_FROZEN_HOUR) and grayBgCount() == 13 and frozen(obj(WOOLOO_B)),
         "then all of them, the flag is set and the flock is frozen")
  wait(120)
  expect(L.mapMusic() == S.MUS_ICHOR_ELPIS_LULLABY_BOX, "and the music box plays")
  shot("spread_done")
end)
