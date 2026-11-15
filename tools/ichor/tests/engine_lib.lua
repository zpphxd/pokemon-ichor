-- Shared helpers for the Ichor engine-system checks (load with dofile), on top
-- of tools/ichor/tests/slice_lib.lua. Read tools/ichor/tests/engine_build.sh first.
--
--   local L = dofile("tools/ichor/tests/engine_lib.lua")   -- slice_lib, extended
--   L.start(function() L.quickstart() ... L.runHeader("SaveTest_BanksHeader") ... end)
--
-- The tag and output folder come from ENGINE_TAG and ENGINE_OUT (engine_run sets
-- both). The symbols are slice_symbols.sh's table merged with engine_symbols.lua.
-- Test-only event scripts come from the setup blob: L.runHeader points the map
-- header's script table at one of its ON_FRAME headers, which runs on the next
-- overworld frame while VAR_TEMP_F is 0 and sets it to 1.

local OUT = os.getenv("ENGINE_OUT") or "build/test_engine/"
local TAG = os.getenv("ENGINE_TAG") or "ENGINE"
local BLOB_ADDR = tonumber(os.getenv("ENGINE_BLOB_ADDR") or "0x0203F000")

local L = dofile("tools/ichor/tests/slice_lib.lua")
L.init{ tag = TAG, out = OUT, symbols = OUT .. "symbols.lua" }
local S, K, emu = L.S, L.K, L.emu
for k, v in pairs(dofile(OUT .. "engine_symbols.lua")) do S[k] = v end
L.OUT, L.TAG = OUT, TAG

-- --- The setup blob ---------------------------------------------------------------------------

local blob, headers = {}, {}
do
  local f = io.open(OUT .. "setup.bin", "rb")
  if f then
    local data = f:read("a")
    f:close()
    for i = 1, #data do blob[i] = data:byte(i) end
    for line in io.lines(OUT .. "setup.syms") do
      local name, hex = line:match("^(%S+) (%x+)$")
      if name then headers[name] = tonumber(hex, 16) end
    end
  end
end
L.headers = headers

function L.loadBlob()
  for i, b in ipairs(blob) do emu:write8(BLOB_ADDR + i - 1, b) end
end

function L.setVar(v, value)
  if v >= S.SPECIAL_VARS_START then
    emu:write16(S["gSpecialVar_0x" .. string.format("%04X", v)], value)
  elseif v >= S.ICHOR_VARS_START and v <= S.ICHOR_VARS_END then
    emu:write16(L.ichor() + S.OFF_ICHOR_VARS + (v - S.ICHOR_VARS_START) * 2, value)
  else
    emu:write16(L.sb1() + S.OFF_SB1_VARS + (v - S.VARS_START) * 2, value)
  end
end

-- Run one of the blob's ON_FRAME headers and wait for the player to be free again,
-- pressing A through any message (A on YES/NO answers YES) unless opts.noSettle.
function L.runHeader(name, opts)
  opts = opts or {}
  local addr = headers[name]
  if not addr then L.fail("no header " .. name .. " in the setup blob") end
  L.setVar(S.VAR_TEMP_F, 0)
  emu:write32(S.gMapHeader + S.OFF_MAPHEADER_MAPSCRIPTS, addr)
  L.waitUntil(function() return L.getVar(S.VAR_TEMP_F) ~= 0 end, opts.start or 600, name .. " to start")
  if opts.noSettle then return end
  L.settle({ limit = opts.limit, answers = opts.answers })
end

-- --- IchorSave ---------------------------------------------------------------------------------

function L.ichor() return emu:read32(S.gSaveBlock3Ptr) + S.OFF_SB3_ICHOR end

-- Any flag or var, wherever it is saved: SaveBlock1 or the Ichor banks.
local getFlag1, getVar1 = L.getFlag, L.getVar
function L.getFlag(f)
  if f >= S.ICHOR_FLAGS_START and f <= S.ICHOR_FLAGS_END then
    local o = f - S.ICHOR_FLAGS_START
    return (emu:read8(L.ichor() + S.OFF_ICHOR_FLAGS + (o >> 3)) >> (o & 7)) & 1 == 1
  elseif f >= S.ICHOR_DAILY_FLAGS_START and f <= S.ICHOR_DAILY_FLAGS_END then
    local o = f - S.ICHOR_DAILY_FLAGS_START
    return (emu:read8(L.ichor() + S.OFF_ICHOR_DAILY_FLAGS + (o >> 3)) >> (o & 7)) & 1 == 1
  end
  return getFlag1(f)
end
function L.getVar(v)
  if v >= S.SPECIAL_VARS_START then
    return emu:read16(S["gSpecialVar_0x" .. string.format("%04X", v)])
  elseif v >= S.ICHOR_VARS_START and v <= S.ICHOR_VARS_END then
    return emu:read16(L.ichor() + S.OFF_ICHOR_VARS + (v - S.ICHOR_VARS_START) * 2)
  end
  return getVar1(v)
end
function L.setFlag(f, on)
  local base, o
  if f >= S.ICHOR_FLAGS_START and f <= S.ICHOR_FLAGS_END then
    base, o = L.ichor() + S.OFF_ICHOR_FLAGS, f - S.ICHOR_FLAGS_START
  elseif f >= S.ICHOR_DAILY_FLAGS_START and f <= S.ICHOR_DAILY_FLAGS_END then
    base, o = L.ichor() + S.OFF_ICHOR_DAILY_FLAGS, f - S.ICHOR_DAILY_FLAGS_START
  else
    base, o = L.sb1() + S.OFF_SB1_FLAGS, f
  end
  local a = base + (o >> 3)
  local b = emu:read8(a)
  if on == false then b = b & ~(1 << (o & 7)) else b = b | (1 << (o & 7)) end
  emu:write8(a, b)
end

-- `n` bytes from `addr`, as a string, to compare two snapshots.
function L.snapshot(addr, n)
  local t = {}
  for i = 0, n - 1, 4 do t[#t + 1] = string.format("%08x", emu:read32(addr + i)) end
  return table.concat(t)
end

-- --- Starting -----------------------------------------------------------------------------------

-- A new game with the expansion's Quickstart, on the smoke test's timing, then
-- fast text and no battle animations, and the blob copied in.
function L.quickstart()
  L.waitUntil(function() return L.now() >= 500 end, 600, "frame 500")
  L.tap(K.START)
  L.waitUntil(function() return L.now() >= 1020 end, 600, "frame 1020")
  L.tap(K.SELECT)
  L.waitUntil(L.idle, 4000, "the new game")
  L.wait(30)
  local opt = L.sb2() + S.OFF_SB2_OPTIONS
  emu:write16(opt, (emu:read16(opt) & ~0x7) | 2 | (1 << 9) | (1 << 10))
  L.loadBlob()
end

-- After emu:reset(): the title, then CONTINUE on the main menu.
function L.continueSave()
  L.wait(500); L.tap(K.START); L.wait(500); L.tap(K.A)
  L.waitUntil(function() return L.on("CB2_MainMenu") end, 900, "the main menu with a save")
  L.wait(80)
  L.tap(K.A)
  L.waitUntil(L.idle, 3000, "the field after CONTINUE")
  L.wait(30)
  L.loadBlob()
end

return L
