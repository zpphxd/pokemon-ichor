-- Shared helpers for the Act III engine checks (load with dofile), on top of
-- tools/ichor/tests/engine_lib.lua: a test spot in the Akti Agora, with the
-- map's first three objects rebuilt as whatever a check needs (a statue, a
-- mirror, a bull), and a plain floor under them. Nothing in the ROM changes:
-- the objects come from rewriting SaveBlock1's copy of the map's templates and
-- respawning them, and the floor from writing the live map grid.
--
--   local L = dofile("tools/ichor/tests/act3_lib.lua")
--   L.start(function() L.quickstart(); L.toSpot(6, 6); L.place{ {...}, ... } end)

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, emu = L.S, L.emu
L.consts = S

-- --- The map grid ---------------------------------------------------------------------------

local function gridAddr(x, y)
  local width = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_WIDTH)
  local map = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_MAP)
  return map + 2 * ((x + S.MAP_OFFSET) + (y + S.MAP_OFFSET) * width)
end
function L.block(x, y) return emu:read16(gridAddr(x, y)) end
function L.setBlock(x, y, b) emu:write16(gridAddr(x, y), b) end
function L.metatile(x, y) return L.block(x, y) & S.MAPGRID_METATILE_ID_MASK end

-- Floor (the map's commonest passable block) on every tile in `open`, and a
-- wall (the same block, impassable) on every tile in `walls`: {{x, y}, ...}.
-- Returns the floor block.
function L.arena(open, walls)
  local layout = emu:read32(S.gMapHeader + S.OFF_MAPHEADER_MAPLAYOUT)
  local w, h = emu:read32(layout), emu:read32(layout + 4) -- MapLayout's width and height
  local count, floor, best = {}, nil, 0
  for y = 0, h - 1 do
    for x = 0, w - 1 do
      local b = L.block(x, y)
      if b & S.MAPGRID_COLLISION_MASK == 0 then
        count[b] = (count[b] or 0) + 1
        if count[b] > best then floor, best = b, count[b] end
      end
    end
  end
  for _, t in ipairs(open) do L.setBlock(t[1], t[2], floor) end
  for _, t in ipairs(walls or {}) do L.setBlock(t[1], t[2], floor | S.MAPGRID_COLLISION_MASK) end
  L.runHeader("Act3Test_RedrawHeader")
  return floor
end
-- A row of floor from (x0, y) to (x1, y).
function L.row(x0, x1, y)
  local t = {}
  for x = x0, x1 do t[#t + 1] = { x, y } end
  return t
end

-- --- The spot and its objects -------------------------------------------------------------

-- Warp into the Agora at (x, y) and wait for the field.
function L.toSpot(x, y)
  L.setVar(S.VAR_0x8000 + 8, x)
  L.setVar(S.VAR_0x8000 + 9, y)
  L.runHeader("Act3Test_WarpHeader")
  local px, py = L.pos()
  L.expect(L.mapId() == S.MAP_AGORA and px == x and py == y,
           string.format("the test spot: the Agora at (%d,%d)", px, py))
  L.loadBlob() -- a warp doesn't touch EWRAM, but be sure
end

local function template(i)
  return L.sb1() + S.OFF_SB1_TEMPLATES + i * S.OBJECT_TEMPLATE_SIZE
end

-- Rebuild the map's first #objs objects: each { x, y, movement[, script] }.
-- Returns their local ids, in order.
function L.place(objs)
  local events = emu:read32(S.gMapHeader + S.OFF_MAPHEADER_EVENTS)
  local count = emu:read8(events + S.OFF_EVENTS_OBJECT_COUNT)
  if count < #objs or #objs > 3 or #objs < 1 then L.fail(string.format("the spot has %d objects, the check needs %d", count, #objs)) end
  local ids = {}
  for i, o in ipairs(objs) do
    local t = template(i - 1)
    ids[i] = emu:read8(t + S.OFF_TEMPLATE_LOCAL_ID)
    emu:write16(t + S.OFF_TEMPLATE_X, o[1])
    emu:write16(t + S.OFF_TEMPLATE_Y, o[2])
    emu:write8(t + S.OFF_TEMPLATE_MOVEMENT_TYPE, o[3])
    emu:write8(t + S.OFF_TEMPLATE_MOVEMENT_RANGE, 0)
    emu:write16(t + S.OFF_TEMPLATE_TRAINER_TYPE, 0)
    emu:write32(t + S.OFF_TEMPLATE_SCRIPT, o[4] or 0)
    emu:write16(t + S.OFF_TEMPLATE_FLAG, 0)
  end
  for i = 1, 3 do L.setVar(S.VAR_0x8000 + i - 1, ids[i] or ids[1]) end
  L.runHeader("Act3Test_RespawnHeader")
  -- every other object gone, and its template off the map so it can't come back
  for i = #objs, count - 1 do
    local t = template(i)
    emu:write16(t + S.OFF_TEMPLATE_Y, 0x7F)
    L.setVar(S.VAR_0x8000, emu:read8(t + S.OFF_TEMPLATE_LOCAL_ID))
    L.runHeader("Act3Test_RemoveHeader")
  end
  for i, o in ipairs(objs) do
    local x, y = L.objectAt(ids[i])
    L.expect(x == o[1] and y == o[2], string.format("object %d stands at (%d,%d)", ids[i], o[1], o[2]))
  end
  return ids
end

-- The live object with this local id: its event struct's address.
function L.object(localId)
  for i = 0, S.OBJECT_EVENTS_COUNT - 1 do
    local o = S.gObjectEvents + i * S.OBJECT_EVENT_SIZE
    if emu:read8(o) & 1 == 1 and emu:read8(o + S.OFF_OBJ_LOCAL_ID) == localId then return o end
  end
end
-- facingDirection is the low nibble of byte 0x18 (as L.facing reads the player's)
function L.objectFacing(localId) return emu:read8(L.object(localId) + 0x18) & 0xF end

L.DIRS = { [1] = "south", [2] = "north", [3] = "west", [4] = "east" }

return L
