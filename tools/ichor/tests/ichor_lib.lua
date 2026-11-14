-- Shared helpers for Ichor's headless Lua checks (load with dofile).
--
-- A check is a list of steps run one after another, each followed by a wait in
-- frames:
--   { warp = {group, num, warpId, x, y} } load a map with the player at (x, y);
--                                         warpId >= 0 arrives through that warp
--                                         (a door plays its exit walk)
--   { flag = FLAG, set = true|false }     write an event flag
--   { instant_text = true }               set the text speed to instant
--   { give_mon = SPECIES }                a level-5 Pokémon at 1 HP in party slot 1
--   { press = KEY } / { hold = KEY, frames = N }
--   { shot = "name.png" }                 screenshot into OUT
--   { expect_flag = FLAG, set = bool, why = "..." }
--   { check = function() return ok, msg end }
--   { log = "text" }
--   wait = N on any step (default 1)
-- The run ends with "<TAG> done" (pass) or "<TAG> FAIL ..." lines before it.
--
-- The warp writes gSaveBlock1Ptr->pos and ->location and sets gMain.callback2 to
-- CB2_LoadMap: the same map load a door warp does, without the fade. Offsets are
-- from include/global.h (SaveBlock1: pos 0x00, location 0x04, lastHealLocation
-- 0x1C, flags 0x1270) and symbols from pokeemerald.map.

local M = {}
M.K = C.GBA_KEY

function M.sym(name)
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

M.SB1 = M.sym("gSaveBlock1Ptr")
M.MAIN = M.sym("gMain")
M.CB2_LOADMAP = M.sym("CB2_LoadMap")

local SB1_POS, SB1_LOCATION, SB1_LAST_HEAL, SB1_FLAGS = 0x00, 0x04, 0x1C, 0x1270

function M.sb1() return emu:read32(M.SB1) end

function M.flag(id)
  local b = emu:read8(M.sb1() + SB1_FLAGS + (id >> 3))
  return (b >> (id & 7)) & 1 == 1
end

function M.setflag(id, on)
  local a = M.sb1() + SB1_FLAGS + (id >> 3)
  local b = emu:read8(a)
  if on == false then b = b & ~(1 << (id & 7)) else b = b | (1 << (id & 7)) end
  emu:write8(a, b)
end

local function write_warp(base, group, num, warpId, x, y)
  emu:write8(base, group)
  emu:write8(base + 1, num)
  emu:write8(base + 2, warpId & 0xFF)
  emu:write16(base + 4, x & 0xFFFF)
  emu:write16(base + 6, y & 0xFFFF)
end

function M.warp(group, num, warpId, x, y)
  local sb = M.sb1()
  emu:write16(sb + SB1_POS, x)
  emu:write16(sb + SB1_POS + 2, y)
  write_warp(sb + SB1_LOCATION, group, num, warpId, x, y)
  emu:write32(M.MAIN + 4, M.CB2_LOADMAP | 1)
end

-- System flags (badges and the like) sit after the trainer flags, whose count
-- Ichor raises as it adds trainers: SYSTEM_FLAGS = 0x500 + MAX_TRAINERS_COUNT.
-- Read the count from include/constants/opponents.h rather than hardcoding it.
function M.system_flag(offset)
  local f = io.open("include/constants/opponents.h", "r")
  local count
  if f then
    for line in f:lines() do
      count = count or tonumber(line:match("^#define MAX_TRAINERS_COUNT_EMERALD%s+(%d+)"))
    end
    f:close()
  end
  return 0x500 + (count or 864) + offset
end

-- Instant text (SaveBlock2 0x14: optionsTextSpeed is the low 3 bits), so every
-- screenshot taken after a short wait shows a whole box.
M.SB2 = M.sym("gSaveBlock2Ptr")
function M.instant_text()
  local a = emu:read32(M.SB2) + 0x14
  emu:write16(a, (emu:read16(a) & ~7) | 3)
end

-- Put one Pokémon in the player's party. Quickstart starts with none, and the
-- Pokémon Center heal animation never ends on an empty party (it places balls
-- until its count reaches zero, and it starts at zero). With personality and OT id
-- 0 the box data's XOR key is 0 and its substructs sit in order, so species goes
-- in the first u16 of substruct 0 and the checksum is the sum of the 16-bit
-- halves (include/pokemon.h: BoxPokemon is 80 bytes, secure data at 0x20).
function M.give_test_mon(species, level)
  local party = emu:read32(M.sym("gPlayerPartyPtr"))
  local count = emu:read32(M.sym("gPlayerPartyCountPtr"))
  for o = 0, 99 do emu:write8(party + o, 0) end
  for k, b in ipairs({ 0xCE, 0xBF, 0xCD, 0xCE, 0xFF }) do emu:write8(party + 7 + k, b) end -- "TEST"
  emu:write8(party + 18, 2)                    -- language: English
  emu:write8(party + 19, 0x02)                 -- hasSpecies
  emu:write8(party + 20, 0xFF)                 -- empty OT name
  emu:write16(party + 32, species & 0x7FF)     -- substruct 0: species
  emu:write16(party + 32 + 10, 1)              -- substruct 0: Poké Ball
  local sum = 0
  for o = 0, 47, 2 do sum = sum + emu:read16(party + 32 + o) end
  emu:write16(party + 28, sum & 0xFFFF)        -- checksum
  emu:write8(party + 84, level or 5)
  emu:write16(party + 86, 1)                   -- hp, so a heal has work to do
  emu:write16(party + 88, 20)                  -- max hp
  emu:write8(count, 1)
end

function M.party_hp()
  return emu:read16(emu:read32(M.sym("gPlayerPartyPtr")) + 86)
end

-- lastHealLocation as {group, num, x, y}
function M.last_heal()
  local a = M.sb1() + SB1_LAST_HEAL
  local function s16(v) if v >= 0x8000 then return v - 0x10000 end return v end
  return emu:read8(a), emu:read8(a + 1), s16(emu:read16(a + 4)), s16(emu:read16(a + 6))
end

-- Run `steps`; `tag` prefixes every log line; `out` is the screenshot folder.
function M.run(tag, out, steps)
  local i, waitUntil, released = 1, 0, {}
  local failures = 0
  if not (M.SB1 and M.MAIN and M.CB2_LOADMAP) then
    console:log(tag .. " FAIL: symbols missing from pokeemerald.map")
  end
  local function fail(msg)
    failures = failures + 1
    console:log(tag .. " FAIL: " .. msg)
  end
  callbacks:add("frame", function()
    local f = emu:currentFrame()
    for k, at in pairs(released) do
      if f >= at then emu:clearKey(k); released[k] = nil end
    end
    if f < waitUntil or i > #steps then return end
    local s = steps[i]
    i = i + 1
    local wait = s.wait or 1
    if s.instant_text then M.instant_text() end
    if s.give_mon then M.give_test_mon(s.give_mon, 5) end
    if s.warp then M.warp(table.unpack(s.warp)) end
    if s.flag then M.setflag(s.flag, s.set ~= false) end
    if s.press then emu:addKey(s.press); released[s.press] = f + 6 end
    if s.hold then emu:addKey(s.hold); released[s.hold] = f + (s.frames or 16) end
    if s.shot then emu:screenshot(out .. s.shot); console:log(tag .. " shot " .. s.shot .. " at " .. f) end
    if s.log then console:log(tag .. " " .. s.log) end
    if s.expect_flag then
      local want = s.set ~= false
      if M.flag(s.expect_flag) ~= want then fail(s.why or ("flag " .. s.expect_flag)) end
    end
    if s.check then
      local ok, msg = s.check()
      if not ok then fail(msg) else console:log(tag .. " ok: " .. msg) end
    end
    waitUntil = f + wait
    if i > #steps then
      if failures == 0 then console:log(tag .. " PASS") end
      console:log(tag .. " done at frame " .. f)
    end
  end)
end

-- Steps that press A `n` times, `gap` frames apart, with a screenshot before
-- each press named prefix_NN.png.
function M.talk(prefix, n, gap)
  local out = {}
  for k = 1, n do
    table.insert(out, { shot = string.format("%s_%02d.png", prefix, k) })
    table.insert(out, { press = M.K.A, wait = gap or 90 })
  end
  return out
end

-- A new game from the title with the expansion's Quickstart, on the smoke test's
-- timing: START skips the intro at frame 500, SELECT at 1020, the house by 2500.
function M.quickstart()
  return {
    { log = "booting", wait = 499 },
    { press = M.K.START, wait = 520 },
    { press = M.K.SELECT, wait = 1480 },
  }
end

-- Concatenate step lists.
function M.seq(...)
  local out = {}
  for _, list in ipairs({ ... }) do
    for _, s in ipairs(list) do table.insert(out, s) end
  end
  return out
end

return M
