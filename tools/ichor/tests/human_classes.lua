-- TEST-ONLY gallery: real graphics IDs, movement commands and trainer loader.
-- Not normal story footage; no ROM palette, map or trainer data is patched.
-- Background layers are hidden and actors staged apart to expose whole sprites.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, emu = L.S, L.emu
local walkers = { "acolyte_f", "acolyte_m", "augur", "diver", "elder_f", "elder_m",
  "fisher", "goatherd", "harvester", "healer", "hoplite", "kid_f", "kid_m", "man",
  "merchant", "pilgrim", "priestess", "sailor", "shepherd", "woman", "youth_f", "youth_m" }
local fronts = { "acolyte_f", "acolyte_m", "augur", "goatherd", "harvester",
  "hoplite", "shepherd", "merchant", "pilgrim", "ichor_sailor" }

local function native(kind, name, ext)
  local file = assert(io.open(L.OUT .. "native/" .. kind .. "_" .. name .. ext, "rb"))
  local data = file:read("*a")
  file:close()
  return data
end
local function matches(address, bytes)
  for i = 1, #bytes do
    if emu:read8(address + i - 1) ~= bytes:byte(i) then return false end
  end
  return true
end
local function object()
  for i = 0, S.OBJECT_EVENTS_COUNT - 1 do
    local o = S.gObjectEvents + i * S.OBJECT_EVENT_SIZE
    if emu:read8(o) & 1 == 1 and emu:read8(o + S.OFF_OBJ_LOCAL_ID) == 0x50 then return o end
  end
end
local function shown(sprite)
  local number = emu:read8(sprite + S.OFF_SPRITE_ANIM_NUM)
  local command = emu:read8(sprite + S.OFF_SPRITE_ANIM_CMD)
  local sequence = emu:read32(emu:read32(sprite + S.OFF_SPRITE_ANIMS) + number * 4)
  return emu:read16(sequence + command * 4)
end
local function check(sprite, raw, palette, name)
  local attr = emu:read16(sprite + 4)
  L.expect(matches(0x06010000 + (attr & 0x3FF) * 32, raw), name .. " complete native OBJ VRAM bytes")
  L.expect(matches(0x05000200 + (attr >> 12) * 32, palette), name .. " all16 hardware palette words")
end

L.start(function()
  L.quickstart()
  L.runHeader("Humans_StageHeader")
  local total = 0
  for _, name in ipairs(walkers) do
    local gfx = assert(S["GFX_" .. name:upper()])
    L.setVar(S.VAR_0x8004, gfx)
    L.runHeader("Humans_SpawnHeader")
    local o = object()
    L.expect(o ~= nil and emu:read16(o + S.OFF_OBJ_GRAPHICS_ID) == gfx, name .. " real graphics ID spawned")
    local sprite = S.gSprites + emu:read8(o + S.OFF_OBJ_SPRITE_ID) * S.SPRITE_SIZE
    local raw, palette = native("walkers", name, ".4bpp"), native("walkers", name, ".gbapal")
    local seen = {}
    local function frame(fr, direction)
      local bytes = raw:sub(fr * 256 + 1, (fr + 1) * 256)
      local images = emu:read32(sprite + S.OFF_SPRITE_IMAGES)
      local relative = emu:read8(images + 6) == 1
      L.expect(emu:read16(images + 4) == 256 and relative == (name ~= "healer"),
               name .. " relative/explicit nurse image table contract")
      local address = relative and (emu:read32(images) + fr * 256) or emu:read32(images + fr * 8)
      L.expect(#bytes == 256 and matches(address, bytes),
               name .. " frame " .. fr .. " engine image table matches native source")
      check(sprite, bytes, palette, name .. " " .. direction .. " " .. fr)
      L.expect(((emu:read16(sprite + 2) & 0x1000) ~= 0) == (direction == "Right"),
               name .. " " .. direction .. " horizontal mirror contract")
      L.shot("TEST_ONLY_" .. name .. "_" .. direction .. "_" .. fr)
      seen[fr] = true
    end
    for _, direction in ipairs({ "Down", "Up", "Left", "Right" }) do
      local expected = ({Down={0,3,4}, Up={1,5,6}, Left={2,7,8}, Right={2,7,8}})[direction]
      local captured = {}
      L.runHeader("Humans_" .. direction .. "Header", {noSettle=true})
      for _ = 1, 900 do
        local fr = shown(sprite)
        for _, wanted in ipairs(expected) do
          if fr == wanted and not captured[fr] then
            L.wait(2)
            if shown(sprite) == fr then frame(fr, direction); captured[fr] = true end
          end
        end
        if L.getVar(S.VAR_0x8000) == 1 then break end
        L.frame()
      end
      L.expect(L.getVar(S.VAR_0x8000) == 1, name .. " " .. direction .. " movement finishes")
      L.settle()
      for _, wanted in ipairs(expected) do L.expect(captured[wanted], name .. " " .. direction .. " state " .. wanted) end
    end
    if name == "healer" then
      L.runHeader("Humans_BowHeader", {noSettle=true})
      L.waitUntil(function() return shown(sprite) == 9 end, 120, "real nurse bow frame")
      L.wait(2)
      frame(9, "Bow")
      L.settle()
    end
    local count = name == "healer" and 10 or 9
    for i = 0, count - 1 do L.expect(seen[i], name .. " native frame " .. i .. " observed"); total = total + 1 end
    L.runHeader("Humans_RemoveHeader")
    L.expect(object() == nil, name .. " gallery object removed")
  end
  L.expect(total == 199, "all199 field frames displayed by real movement tables")
  for _, name in ipairs(fronts) do
    L.setVar(S.VAR_0x8004, assert(S["PIC_" .. name:upper()]))
    L.runHeader("Humans_FrontHeader")
    local id = L.getVar(S.VAR_0x8005)
    L.expect(id < S.SPRITE_LIMIT, name .. " real trainer front loader succeeds")
    local sprite = S.gSprites + id * S.SPRITE_SIZE
    L.wait(8)
    check(sprite, native("portraits", name, ".4bpp"), native("portraits", name, ".gbapal"), name .. " front")
    L.expect((emu:read16(sprite) & 0xC000) == 0 and (emu:read16(sprite + 2) & 0xC000) == 0xC000,
             name .. " complete square64 OAM on unobscured gallery stage")
    L.shot("TEST_ONLY_front_" .. name)
    L.runHeader("Humans_FreeFrontHeader")
    L.expect(L.getVar(S.VAR_0x8006) == 0, name .. " trainer image allocation released")
  end
end)
