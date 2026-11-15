-- Headless check that the Aethos dex is really in the ROM.
--
--   tools/ichor/aethos_dex_check.sh        (writes the expectations, then runs this)
--
-- Reads the game's own tables, nothing test-only:
--   * gSpeciesInfo: every Aethos species' name, base stats, types, national dex
--     number and front pic pointer, against design/dex via the expectations file
--     that tools/dex/rom/gen.py --expect writes (AETHOS_EXPECT).
--   * the regional dex order (sHoennToNationalOrder) and the starter table
--     (sStarterMon), found by their contents in ROM since they're static.
-- Field offsets inside SpeciesInfo are calibrated from Bulbasaur and Ivysaur,
-- so the check survives upstream struct changes.
-- Prints "AETHOS PASS" or "AETHOS FAIL ...", then "AETHOS done".

local E = dofile(os.getenv("AETHOS_EXPECT") or "build/aethos_dex/expect.lua")
local ROM_START, ROM_SIZE = 0x08000000, 0x02000000

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

-- Gen 3 charmap: A-Z = 0xBB.., a-z = 0xD5..
local function encode(s)
  local out = {}
  for c in s:gmatch(".") do
    local b = c:byte()
    if b >= 65 and b <= 90 then out[#out + 1] = string.char(0xBB + b - 65)
    elseif b >= 97 and b <= 122 then out[#out + 1] = string.char(0xD5 + b - 97)
    else out[#out + 1] = "?" end
  end
  return table.concat(out)
end

local function readstr(addr, n) return emu:readRange(addr, n) end

-- find a byte string in ROM; returns its address or nil
local function romFind(needle)
  local chunk, step = 0x100000, 0x100000 - #needle
  local a = ROM_START
  while a < ROM_START + ROM_SIZE do
    local s = emu:readRange(a, chunk)
    local i = s:find(needle, 1, true)
    if i then return a + i - 1 end
    a = a + step
  end
  return nil
end

local function u16s(list)
  local t = {}
  for _, v in ipairs(list) do t[#t + 1] = string.char(v & 0xFF, (v >> 8) & 0xFF) end
  return table.concat(t)
end

local function u32s(list)
  local t = {}
  for _, v in ipairs(list) do t[#t + 1] = string.char(v & 0xFF, (v >> 8) & 0xFF, 0, 0) end
  return table.concat(t)
end

local fails = {}
local function fail(msg) fails[#fails + 1] = msg; console:log("AETHOS FAIL " .. msg) end

local function run()
  local base = sym("gSpeciesInfo")
  if not base then fail("no gSpeciesInfo in pokeemerald.map"); return end

  -- calibrate stride and the name, national dex and front pic offsets
  local scan = readstr(base, 0x400)
  local p1 = scan:find(encode("Bulbasaur"), 1, true)
  local p2 = p1 and scan:find(encode("Ivysaur"), p1, true)
  if not (p1 and p2) then fail("can't find Bulbasaur/Ivysaur in gSpeciesInfo"); return end
  local stride = p2 - p1
  local nameOff = (p1 - 1) - stride
  local function entry(id) return base + id * stride end
  local natOff
  for k = nameOff + 13, nameOff + 24 do
    if emu:read16(entry(1) + k) == 1 and emu:read16(entry(2) + k) == 2 and emu:read16(entry(25) + k) == 25 then
      natOff = k; break
    end
  end
  local bulbaFront = sym("gMonFrontPic_Bulbasaur")
  local frontOff
  for k = 0, stride - 4, 4 do
    if emu:read32(entry(1) + k) == bulbaFront then frontOff = k; break end
  end
  if not natOff or not frontOff then fail("can't calibrate natDexNum/frontPic offsets"); return end
  console:log(string.format("AETHOS stride %d, name +%d, natDex +%d, frontPic +%d", stride, nameOff, natOff, frontOff))

  -- every species
  local checked = 0
  for _, s in ipairs(E.species) do
    local a = entry(s.id)
    local name = readstr(a + nameOff, #s.name)
    if name ~= encode(s.name) or emu:read8(a + nameOff + #s.name) ~= 0xFF then
      fail(s.name .. ": name in ROM doesn't match")
    end
    for i = 1, 6 do
      if emu:read8(a + i - 1) ~= s.stats[i] then fail(s.name .. ": base stat " .. i .. " is " .. emu:read8(a + i - 1)) end
    end
    if emu:read8(a + 6) ~= s.types[1] or emu:read8(a + 7) ~= s.types[2] then fail(s.name .. ": types") end
    if emu:read16(a + natOff) ~= s.nat then fail(s.name .. ": national dex " .. emu:read16(a + natOff)) end
    local want = sym(s.front)
    if not want or emu:read32(a + frontOff) ~= want then fail(s.name .. ": front pic isn't " .. s.front) end
    checked = checked + 1
  end
  console:log("AETHOS checked " .. checked .. " species in gSpeciesInfo")

  -- the regional dex is Aethos's, #1..N in dex order
  local order = {}
  for i = 0, E.count - 1 do order[#order + 1] = E.firstNat + i end
  -- (enum NationalDexOrder isn't packed, so the table holds 32-bit entries)
  if not romFind(u32s(order)) then fail("the Aethos regional dex order isn't in ROM") end

  -- the three starters, in Grass, Fire, Water order
  if not romFind(u16s(E.starters)) then fail("the starter table isn't Nebrel, Kynder, Hipling") end
end

local ran = false
callbacks:add("frame", function()
  if ran then return end
  ran = true
  run()
  if #fails == 0 then console:log("AETHOS PASS") end
  console:log("AETHOS done")
end)
