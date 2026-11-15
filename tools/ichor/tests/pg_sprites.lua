-- The post-game's first sprites, run by tools/ichor/tests/pg_sprites.sh (read it first).
--
--   1. Akti's harbor quay, the map's own people cleared away.
--   2. The Euploia, sail full in the west basin and slack in the east water,
--      rows in place to each heading in turn. Each ship spawns from its own
--      graphics id, plays its heading's walk frames (south 3,0,4; north
--      5,1,6; west and east 7,2,8, east flipped) and loads the Euploia
--      palette, and each heading is screenshotted.
--   3. The eleven walkers, in two groups on the quay, the same way: graphics
--      ids, walk frames per heading, the cast or the Olympia palette.
--   4. The six trainer pics are registered: TRAINER_PIC_ICHOR_* sit below
--      TRAINER_PIC_COUNT and each gTrainerPicInfo entry points into the ROM.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, emu = L.S, L.emu
local expect, shot, log = L.expect, L.shot, L.log
for k, v in pairs(dofile(L.OUT .. "pg_symbols.lua")) do S[k] = v end

local OBJ_SHIPS = { { id = 0x50, gfx = "GFX_EUPLOIA", name = "Euploia (full)" },
                    { id = 0x51, gfx = "GFX_EUPLOIA_SLACK", name = "Euploia (slack)" } }
local CREW = { { 0x60, "NOLAN", "CAST" }, { 0x61, "PHEMIOS", "CAST" }, { 0x62, "LYNKEUS", "CAST" },
               { 0x63, "TRUCE_HERALD", "CAST" }, { 0x64, "ACHILLES", "OLYMPIA" }, { 0x65, "ODYSSEUS", "OLYMPIA" } }
local OLYMPIA = { { 0x66, "HIPPOLYTA", "OLYMPIA" }, { 0x67, "ATALANTA", "OLYMPIA" }, { 0x68, "ARIADNE", "OLYMPIA" },
                  { 0x69, "OLYMPIAS", "OLYMPIA" }, { 0x6A, "PAIONIOS", "OLYMPIA" } }
local HEADINGS = {
  { dir = "Down", frames = { 0, 3, 4 } },
  { dir = "Up", frames = { 1, 5, 6 } },
  { dir = "Left", frames = { 2, 7, 8 } },
  { dir = "Right", frames = { 2, 7, 8 } },
}

-- One color from each palette, as BGR555, to tell which palette a sprite shows:
-- the Euploia's wood, Olympias's purple, the cast's slate.
local function bgr(r, g, b) return (b >> 3) << 10 | (g >> 3) << 5 | (r >> 3) end
local PAL_PROBE = {
  EUPLOIA = { index = 5, color = bgr(176, 120, 72) },
  OLYMPIA = { index = 15, color = bgr(152, 80, 152) },
  CAST = { index = 14, color = bgr(72, 64, 96) },
}

local function objectAt(i) return S.gObjectEvents + i * S.OBJECT_EVENT_SIZE end
local function object(localId)
  for i = 0, S.OBJECT_EVENTS_COUNT - 1 do
    local o = objectAt(i)
    if emu:read8(o) & 1 == 1 and emu:read8(o + S.OFF_OBJ_LOCAL_ID) == localId then return o end
  end
end
local function sprite(o) return S.gSprites + emu:read8(o + S.OFF_OBJ_SPRITE_ID) * S.SPRITE_SIZE end
-- The sheet frame the sprite shows: anims[animNum][animCmdIndex].imageValue
local function shown(o)
  local s = sprite(o)
  local num, cmd = emu:read8(s + S.OFF_SPRITE_ANIM_NUM), emu:read8(s + S.OFF_SPRITE_ANIM_CMD)
  local seq = emu:read32(emu:read32(s + S.OFF_SPRITE_ANIMS) + num * 4)
  return emu:read16(seq + cmd * 4)
end
-- oam.attr2's palette number, and that palette's color `index`
local function palColor(o, index)
  local pn = (emu:read16(sprite(o) + 4) >> 12) & 0xF
  return emu:read16(S.gPlttBufferUnfaded + (256 + pn * 16 + index) * 2)
end

-- Remove every active object but the player whose local id passes `match`
-- (nil: all of them), through PgSpr_Remove.
local function clear(match)
  for i = 0, S.OBJECT_EVENTS_COUNT - 1 do
    local o = objectAt(i)
    local active, player = emu:read8(o) & 1 == 1, emu:read8(o + 2) & 1 == 1
    if active and not player and (not match or match(emu:read8(o + S.OFF_OBJ_LOCAL_ID))) then
      L.setVar(S.VAR_0x8004, o & 0xFFFF)
      L.setVar(S.VAR_0x8005, o >> 16)
      L.runHeader("PgSpr_RemoveHeader")
    end
  end
end
local function between(lo, hi) return function(id) return id >= lo and id <= hi end end

local function setOf(t)
  local s = {}
  for _, v in ipairs(t) do s[v] = true end
  return s
end
local function listOf(set)
  local t = {}
  for k in pairs(set) do t[#t + 1] = k end
  table.sort(t)
  return table.concat(t, ",")
end

-- Spawn a group to one heading, check each member, and sample the frames it shows.
local function runGroup(header, members, heading, tag)
  L.runHeader(header)
  L.wait(8)
  local seen = {}
  for _, m in ipairs(members) do
    local o = object(m.id)
    expect(o ~= nil and emu:read16(o + S.OFF_OBJ_GRAPHICS_ID) == S[m.gfx],
           string.format("%s spawns from %s (%s)", m.name, m.gfx, heading.dir))
    seen[m.id] = {}
  end
  for f = 1, 96 do
    for _, m in ipairs(members) do
      local o = object(m.id)
      if o then seen[m.id][shown(o)] = true end
    end
    if f == 40 then shot(tag .. "_" .. heading.dir:lower()) end
    L.frame()
  end
  local want = setOf(heading.frames)
  for _, m in ipairs(members) do
    local o = object(m.id)
    local got = listOf(seen[m.id])
    expect(got == listOf(want), string.format("%s walking %s shows frames %s: got %s", m.name,
                                              heading.dir:lower(), listOf(want), got))
    local probe = PAL_PROBE[m.pal]
    local c = o and palColor(o, probe.index)
    expect(c == probe.color, string.format("%s shows the %s palette (color %d = %04x, got %s)", m.name, m.pal,
                                           probe.index, probe.color, c and string.format("%04x", c) or "none"))
  end
end

-- Noon, so the screenshots show the sprites' own colors, not the evening tint.
-- Local time is the RTC minus SaveBlock2's offset (RtcCalcLocalTime), so the
-- RTC's hour is the local hour plus the offset's, and noon needs an offset of
-- that hour less 12.
local function noon()
  local hour = emu:read8(S.gLocalTime + 2)
  local off = L.sb2() + S.OFF_SB2_LOCAL_TIME_OFFSET + 2
  local h = emu:read8(off)
  if h >= 128 then h = h - 256 end
  local rtc = (hour + h) % 24
  emu:write8(off, (rtc - 12) & 0xFF)
end

L.start(function()
  L.quickstart()
  noon()
  L.runHeader("PgSpr_SetupHeader")
  L.wait(30)
  clear(nil)
  L.wait(10)
  shot("quay_cleared")

  -- 2. The ship, both sails, every heading
  local ships = {}
  for _, s in ipairs(OBJ_SHIPS) do ships[#ships + 1] = { id = s.id, gfx = s.gfx, name = s.name, pal = "EUPLOIA" } end
  for _, h in ipairs(HEADINGS) do
    clear(between(0x50, 0x51))
    runGroup("PgSpr_Ships" .. h.dir .. "Header", ships, h, "ships")
  end
  clear(between(0x50, 0x51))
  log("ok the Euploia rows in all four headings, sail full and slack")

  -- 3. The walkers
  local groups = {
    { prefix = "PgSpr_Crew", list = CREW, tag = "crew", lo = 0x60, hi = 0x65 },
    { prefix = "PgSpr_Olympia", list = OLYMPIA, tag = "olympia", lo = 0x66, hi = 0x6A },
  }
  for _, g in ipairs(groups) do
    local members = {}
    for _, w in ipairs(g.list) do
      members[#members + 1] = { id = w[1], gfx = "GFX_" .. w[2], name = w[2]:lower(), pal = w[3] }
    end
    for _, h in ipairs(HEADINGS) do
      clear(between(g.lo, g.hi))
      runGroup(g.prefix .. h.dir .. "Header", members, h, g.tag)
    end
    clear(between(g.lo, g.hi))
  end
  log("ok all eleven walkers walk in all four headings")

  -- 4. The trainer pics are in the table
  expect(S.TRAINER_PIC_ICHOR_ACHILLES < S.TRAINER_PIC_COUNT and S.TRAINER_PIC_ICHOR_OLYMPIAS < S.TRAINER_PIC_COUNT,
         "TRAINER_PIC_ICHOR_* sit inside TRAINER_PIC_COUNT")
  for pic = S.TRAINER_PIC_ICHOR_ACHILLES, S.TRAINER_PIC_ICHOR_OLYMPIAS do
    local front = emu:read32(S.gTrainerPicInfo + pic * S.TRAINER_PIC_INFO_SIZE)
    local data = front ~= 0 and emu:read32(front + S.OFF_FRONT_IMAGE) or 0
    local pal = front ~= 0 and emu:read32(front + S.OFF_FRONT_PALETTE) or 0
    expect(data >> 24 == 0x08 and pal >> 24 == 0x08,
           string.format("trainer pic %d has its front pic (%08x) and palette (%08x) in the ROM", pic, data, pal))
  end
  log("ok the six trainer pics are registered")
end)
