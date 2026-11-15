-- The Oikoumene's batch-1 trainer classes, run by tools/ichor/tests/oikoumene_trainer_pics.sh
-- (read it first). One battle per new class: the class table's label, the intro
-- line, the front pic's palette, and a screenshot of the intro.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, emu = L.S, L.emu
local expect, wait, shot = L.expect, L.wait, L.shot
for k, v in pairs(dofile(L.OUT .. "oik_symbols.lua")) do S[k] = v end
local CASES = dofile(L.OUT .. "expect.lua")

-- --- The emulator's copy of the ROM ------------------------------------------------------------
-- mGBA runs its own functions only on the main Lua thread, so the test queues its
-- ROM writes and this frame callback (added before L.start's, so it runs first)
-- applies them through the cart0 memory domain, which patches the loaded ROM.
local pending = {}
callbacks:add("frame", function()
  if #pending == 0 then return end
  local rom = _G.emu.memory.cart0
  for _, w in ipairs(pending) do rom:write8(w[1] - 0x08000000, w[2]) end
  pending = {}
end)
local function romWrite(addr, bytes)
  for i, b in ipairs(bytes) do pending[#pending + 1] = { addr + i - 1, b } end
  wait(1)
  for i, b in ipairs(bytes) do
    if emu:read8(addr + i - 1) ~= b then L.fail(string.format("ROM write at 0x%08X didn't take", addr + i - 1)) end
  end
end

-- --- The game's charset (charmap.txt), enough for names and battle lines ------------------------
local DEC = { [0x00] = " ", [0x39] = " ", [0x77] = " ", [0xAB] = "!", [0xAC] = "?", [0xAD] = ".", [0xAE] = "-",
              [0xB8] = ",", [0xFA] = " ", [0xFB] = " ", [0xFE] = " " }  -- 0x39 NBSP, 0x77 spacer
for b = 65, 90 do DEC[0xBB + b - 65] = string.char(b) end
for b = 97, 122 do DEC[0xD5 + b - 97] = string.char(b) end
for b = 48, 57 do DEC[0xA1 + b - 48] = string.char(b) end
local ENC = {}
for b, c in pairs(DEC) do if c ~= " " or b == 0x00 then ENC[c] = b end end

local function readText(addr, max)
  local t, i = {}, 0
  while i < max do
    local b = emu:read8(addr + i)
    if b == 0xFF then break end
    if b == 0xFC then i = i + 1 else t[#t + 1] = DEC[b] or string.format("{%02X}", b) end
    i = i + 1
  end
  return (table.concat(t):gsub("%s+", " "))
end
local function encodeName(s, len)
  local out = {}
  for c in s:gmatch(".") do out[#out + 1] = ENC[c] or L.fail("can't encode " .. c) end
  while #out <= len do out[#out + 1] = 0xFF end
  return out
end

-- An OBJ palette slot holding exactly colors 1-15 of the pic's palette, or nil.
local function palSlot(pal)
  for slot = 0, 15 do
    local base, same = S.gPlttBufferUnfaded + 0x200 + slot * 32, true
    for j = 1, 15 do
      if emu:read16(base + j * 2) ~= pal[j] then same = false break end
    end
    if same then return slot end
  end
end

L.start(function()
  L.quickstart()
  L.runHeader("OikTr_GiveHeader")
  expect(L.partyLevel(0) == 70, "the player has a Pokémon to battle with")
  -- gTrainers is [DIFFICULTY_COUNT][TRAINERS_COUNT]; the game reads the normal row
  local trainer = S.gTrainers + (S.DIFFICULTY_NORMAL * S.TRAINERS_COUNT + S.TEST_TRAINER) * S.TRAINER_SIZE
  expect(readText(trainer + S.OFF_TRAINER_NAME, S.TRAINER_NAME_LENGTH + 1) == "TITYROS",
         "the stand-in's ROM entry is where the test looks (TITYROS)")
  local state = emu:saveStateBuffer(31)
  L.beat = "intro"

  local seen = {}
  for i, c in ipairs(CASES) do
    if i > 1 then
      emu:loadStateBuffer(state, 31)
      wait(2)
    end
    local cls, pic = S[c.class], S[c.pic]
    if not cls or not pic then L.fail("no constant for " .. c.class .. " or " .. c.pic) end
    expect(cls < S.TRAINER_CLASS_COUNT and pic < S.TRAINER_PIC_COUNT, c.class .. " and " .. c.pic .. " are in range")
    expect(not seen[cls], c.class .. " is its own class")
    seen[cls] = true

    -- 1. the label, straight from gTrainerClasses
    local label = readText(S.gTrainerClasses + cls * S.TRAINER_CLASS_SIZE, 13)
    expect(label == c.label, string.format("%s is labelled %s (read %q)", c.class, c.label, label))

    -- 2. the stand-in trainer becomes this class, with this pic and name
    romWrite(trainer + S.OFF_TRAINER_CLASS, { cls })
    romWrite(trainer + S.OFF_TRAINER_PIC, { pic })
    romWrite(trainer + S.OFF_TRAINER_NAME, encodeName(c.name, S.TRAINER_NAME_LENGTH))

    -- 3. the battle, to its intro line
    L.runHeader("OikTr_BattleHeader", { noSettle = true })
    L.waitUntil(L.inBattle, 1500, "the battle against the " .. c.label)
    L.waitUntil(function() return readText(S.gDisplayedStringBattle, 120):find("challenged", 1, true) end,
                1500, "the " .. c.label .. "'s intro line")
    wait(60)
    local line = readText(S.gDisplayedStringBattle, 120)
    expect(line:find(c.label .. " " .. c.name, 1, true) ~= nil,
           string.format("the intro names the %s: %q", c.label, line))

    -- 4. the front pic is the one drawn for it
    local slot = palSlot(c.pal)
    expect(slot ~= nil, string.format("%s's palette is loaded (%s)", c.file, slot and ("OBJ slot " .. slot) or "none"))
    shot(c.file .. "_" .. c.label:lower():gsub(" ", "_"))
  end
end)
