-- Theoxenia sprites check, run by tools/ichor/tests/theoxenia_sprites.sh (read it first).
--
--   1. Sam, Apollo, Cami and Demeter spawn from their graphics IDs
--      (theoxenia_sprites_setup.s). Cami, facing up, sits on her bench (frame
--      9); the other three stand facing down (frame 0).
--   2. nurse_joy_bow on Sam plays ANIM_ICHOR_STRUM: frames 9, 10 and 11 in
--      the order sAnimTable_IchorLyre gives, then his resting frame, and
--      waitmovement lets the script go on. A strum that never ended would
--      hold the player forever, as the healer's bow once did.
--   3. The same on Apollo's gold lyre.
--   4. nurse_joy_bow on Cami plays ANIM_ICHOR_RISE: seated, rising (10), then
--      standing facing down, and the script goes on.
--   5. face_up seats her again.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, emu = L.S, L.emu
local expect, shot, log = L.expect, L.shot, L.log
for k, v in pairs(dofile(L.OUT .. "theox_symbols.lua")) do S[k] = v end

local SAM, APOLLO, CAMI, DEMETER = 0x50, 0x51, 0x52, 0x53
local STRUM = { 9, 10, 9, 10, 11, 10, 9, 10, 9, 11, 0 }
local RISE = { 9, 10, 0 }

local function object(localId)
  for i = 0, S.OBJECT_EVENTS_COUNT - 1 do
    local o = S.gObjectEvents + i * S.OBJECT_EVENT_SIZE
    if emu:read8(o) & 1 == 1 and emu:read8(o + S.OFF_OBJ_LOCAL_ID) == localId then return o end
  end
end
local function sprite(o) return S.gSprites + emu:read8(o + S.OFF_OBJ_SPRITE_ID) * S.SPRITE_SIZE end
-- The sheet frame the sprite shows: anims[animNum][animCmdIndex].imageValue
local function shown(o)
  local s = sprite(o)
  local num, cmd = emu:read8(s + S.OFF_SPRITE_ANIM_NUM), emu:read8(s + S.OFF_SPRITE_ANIM_CMD)
  local seq = emu:read32(emu:read32(s + S.OFF_SPRITE_ANIMS) + num * 4)
  return emu:read16(seq + cmd * 4), num
end
-- facingDirection is the low nibble of byte 0x18
local function facing(o) return emu:read8(o + 0x18) & 0xF end

local function same(a, b)
  if #a ~= #b then return false end
  for i = 1, #a do if a[i] ~= b[i] then return false end end
  return true
end

-- Run a header that plays nurse_joy_bow on `o`; record the frames it shows
-- from its first special frame until the script sets `doneVar`.
local function play(header, o, anim, doneVar, shotAt, tag)
  L.runHeader(header, { noSettle = true })
  local order, last, started, took = {}, nil, false, nil
  local shotDue
  for f = 1, 600 do
    local fr, num = shown(o)
    if num == anim and fr == 9 then started = true end
    if started and fr ~= last then
      order[#order + 1] = fr
      last = fr
      -- the screen catches up with a new frame on the next VBlank or two
      if fr == shotAt and not shotDue then shotDue = f + 2 end
    end
    if f == shotDue then shot(tag .. "_mid") end
    if L.getVar(doneVar) == 1 then took = f; break end
    L.frame()
  end
  L.settle()
  return order, took
end

local function list(t) return table.concat(t, ",") end

L.start(function()
  L.quickstart()

  -- 1. Spawn the four
  L.runHeader("Theox_SpawnHeader")
  local o = { sam = object(SAM), apollo = object(APOLLO), cami = object(CAMI), demeter = object(DEMETER) }
  for name, id in pairs({ sam = S.GFX_SAM, apollo = S.GFX_APOLLO, cami = S.GFX_CAMI, demeter = S.GFX_DEMETER }) do
    expect(o[name] ~= nil and emu:read16(o[name] + S.OFF_OBJ_GRAPHICS_ID) == id,
           string.format("%s spawns with OBJ_EVENT_GFX_ICHOR_%s (%d)", name, name:upper(), id))
  end
  L.wait(20)
  shot("spawned")
  expect(shown(o.cami) == 9 and facing(o.cami) == S.DIR_NORTH,
         string.format("Cami facing up sits on her bench: frame %d, facing %d", shown(o.cami), facing(o.cami)))
  for _, name in ipairs({ "sam", "apollo", "demeter" }) do
    expect(shown(o[name]) == 0, string.format("%s stands facing down: frame %d", name, shown(o[name])))
  end

  -- 2. Sam strums
  L.setVar(S.VAR_0x8000, 0)
  local order, took = play("Theox_StrumHeader", o.sam, S.ANIM_ICHOR_STRUM, S.VAR_0x8000, 11, "sam_strum")
  expect(took ~= nil, "Sam's strum ends and waitmovement lets the script go on")
  expect(same(order, STRUM), "Sam's strum plays frames " .. list(STRUM) .. ": got " .. list(order))
  expect(facing(o.sam) == S.DIR_SOUTH and shown(o.sam) == 0, "Sam ends standing facing down, lyre lowered")
  log(string.format("ok Sam's strum took %s frames", tostring(took)))

  -- 3. Apollo strums
  L.setVar(S.VAR_0x8000, 0)
  order, took = play("Theox_ApolloHeader", o.apollo, S.ANIM_ICHOR_STRUM, S.VAR_0x8000, 11, "apollo_strum")
  expect(took ~= nil, "Apollo's strum ends and the script goes on")
  expect(same(order, STRUM), "Apollo's strum plays frames " .. list(STRUM) .. ": got " .. list(order))

  -- 4. Cami rises
  L.setVar(S.VAR_0x8001, 0)
  order, took = play("Theox_RiseHeader", o.cami, S.ANIM_ICHOR_RISE, S.VAR_0x8001, 10, "cami_rise")
  expect(took ~= nil, "Cami's rise ends and waitmovement lets the script go on")
  expect(same(order, RISE), "Cami rises through frames " .. list(RISE) .. ": got " .. list(order))
  expect(facing(o.cami) == S.DIR_SOUTH and shown(o.cami) == 0, "Cami ends standing, facing down")
  shot("cami_stood")

  -- 5. face_up sits her down again
  L.runHeader("Theox_SitHeader")
  L.wait(10)
  expect(shown(o.cami) == 9 and facing(o.cami) == S.DIR_NORTH, "face_up seats Cami again")
  shot("cami_seated_again")
end)
