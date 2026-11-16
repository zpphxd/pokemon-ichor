-- IchorSave check, run by tools/ichor/tests/ichor_save.sh (read it first).
--
--   1. A new game: IchorSave is the current version, Mom's record is 0-212, everything else is zero.
--   2. Scripts write and read the flag bank, the daily bank and the var bank
--      (ichor_save_setup.s): each lands in IchorSave at its own bit, and no
--      SaveBlock1 flag or var changes.
--   3. A new day clears the daily bank and nothing else.
--   4. Save, reset, CONTINUE: the banks come back as saved.
--   5. An old save (IchorSave all zero, as a save from before it existed) loads
--      as the current version with the new-game defaults.
--   6. A version-3 save, from before the second flag bank, loads with that bank
--      zeroed (it holds what used to sit past IchorSave's end) and nothing else lost.
--   7. A hidden item with a bank flag (asm/macros/map.inc) is found once, and is
--      still found after a save and CONTINUE. The map's events are copied to RAM
--      with the hidden item added, since no map has one yet.
--   8. Oath state survives a real save, while version-4 reserved bytes migrate
--      to an undecided Oath without erasing any existing progress.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, emu = L.S, L.emu
local log, expect, wait, shot = L.log, L.expect, L.wait, L.shot

local function ichor8(off) return emu:read8(L.ichor() + off) end
local function ichor16(off) return emu:read16(L.ichor() + off) end
local function allZero(off, n)
  for i = 0, n - 1, 4 do
    if emu:read32(L.ichor() + off + i) ~= 0 then return false end
  end
  return true
end
local function sb1Flags() return L.snapshot(L.sb1() + S.OFF_SB1_FLAGS, S.NUM_FLAG_BYTES - S.NUM_FLAG_BYTES % 4) end

local function expectDefaults(when)
  expect(ichor8(S.OFF_ICHOR_VERSION) == S.ICHOR_SAVE_VERSION,
         string.format("%s: IchorSave version %d", when, ichor8(S.OFF_ICHOR_VERSION)))
  expect(ichor16(S.OFF_ICHOR_MOM_LOSSES) == 212 and ichor16(S.OFF_ICHOR_MOM_WINS) == 0,
         string.format("%s: Mom's record is %d-%d", when, ichor16(S.OFF_ICHOR_MOM_WINS), ichor16(S.OFF_ICHOR_MOM_LOSSES)))
  expect(allZero(S.OFF_ICHOR_FAVOR, 16) and allZero(S.OFF_ICHOR_VARS, S.OFF_ICHOR_RESERVED - S.OFF_ICHOR_VARS)
         and allZero(S.OFF_ICHOR_FLAGS2, S.ICHOR_SAVE_SIZE - S.OFF_ICHOR_FLAGS2),
         when .. ": Favor, both banks and the thread start empty")
  expect(ichor8(S.OFF_ICHOR_OPTIONS) == 0, when .. ": relic prompts default to ASK")
end

-- --- A hidden item planted in RAM -------------------------------------------------------
local HIDDEN_FLAG = nil            -- set once S is ready: a second-bank flag
local EVENTS_COPY, BG_COPY = 0x0203FC00, 0x0203FC40   -- spare EWRAM, past the setup blob
local function plantHiddenItem()
  local x, y = L.pos()
  local key, tx, ty
  for _, d in ipairs({ { L.K.UP, 0, -1 }, { L.K.DOWN, 0, 1 }, { L.K.LEFT, -1, 0 }, { L.K.RIGHT, 1, 0 } }) do
    if not L.objectOn(x + d[2], y + d[3]) then key, tx, ty = d[1], x + d[2], y + d[3] break end
  end
  local events = emu:read32(S.gMapHeader + S.OFF_MAPHEADER_EVENTS)
  for i = 0, S.MAP_EVENTS_SIZE - 1 do emu:write8(EVENTS_COPY + i, emu:read8(events + i)) end
  emu:write8(EVENTS_COPY + S.OFF_EVENTS_BG_COUNT, 1)
  emu:write32(EVENTS_COPY + S.OFF_EVENTS_BGS, BG_COPY)
  for i = 0, S.BG_EVENT_SIZE - 1 do emu:write8(BG_COPY + i, 0) end
  emu:write16(BG_COPY + S.OFF_BG_X, tx)
  emu:write16(BG_COPY + S.OFF_BG_Y, ty)
  emu:write8(BG_COPY + S.OFF_BG_KIND, S.BG_EVENT_HIDDEN_ITEM)
  local id = HIDDEN_FLAG - S.ICHOR_FLAGS_START + S.ICHOR_HIDDEN_ITEM_BANK_ID
  emu:write32(BG_COPY + S.OFF_BG_UNION, S.ITEM_POTION | (id << 11) | (1 << 24))
  emu:write32(S.gMapHeader + S.OFF_MAPHEADER_EVENTS, EVENTS_COPY)
  L.face(key)
end
-- Press A on it; TRUE if a message box came up
local function searchHiddenItem()
  L.tap(L.K.A)
  local box = false
  for _ = 1, 60 do wait(1) if L.boxUp() then box = true end end
  L.settle()
  return box
end

L.start(function()
  HIDDEN_FLAG = S.FLAG_ICHOR_GENERAL2_START + 5
  expect(S.SB3_SIZE <= 1624 and S.ICHOR_SAVE_SIZE == 1472 and S.OFF_SB3_ICHOR == 0,
         string.format("SaveBlock3 is %d of 1,624 bytes; IchorSave is %d bytes at its start", S.SB3_SIZE, S.ICHOR_SAVE_SIZE))

  -- 1. A new game
  L.quickstart()
  shot("new_game")
  expectDefaults("new game")

  -- Start the clock (Quickstart leaves the water clock unset): its first run
  -- counts as a new day, so it comes before any daily flag is set.
  L.runHeader("SaveTest_ClockHeader")

  -- 2. The banks
  local before = sb1Flags()
  L.setVar(S.VAR_TEMP_F, 0)
  local varsBefore = L.snapshot(L.sb1() + S.OFF_SB1_VARS, 0x200)
  L.runHeader("SaveTest_BanksHeader")
  local got = L.getVar(S.VAR_0x8000)
  expect(got == 127, string.format("the scripts read back every bank write (checks passed: %d of 127)", got))
  local function bankByte(o) return ichor8(S.OFF_ICHOR_FLAGS + o) end
  local function dailyByte(o) return ichor8(S.OFF_ICHOR_DAILY_FLAGS + o) end
  local g = S.FLAG_ICHOR_GENERAL_START - S.ICHOR_FLAGS_START
  local h = S.FLAG_ICHOR_HERMS_START + 3 - S.ICHOR_FLAGS_START
  expect(bankByte(g >> 3) & (1 << (g & 7)) ~= 0, "FLAG_ICHOR_GENERAL_START is its own bit in IchorSave.flags")
  expect(bankByte(255) == 0x80, "the bank's last flag is the top bit of the last byte")
  expect(bankByte(h >> 3) == 1 << (h & 7), "a herm flag sits in the herm range")
  local p = S.FLAG_DAILY_ICHOR_PRAYED_START + 2 - S.ICHOR_DAILY_FLAGS_START
  expect(dailyByte(p >> 3) & (1 << (p & 7)) ~= 0 and dailyByte(31) == 0x80, "daily flags land in IchorSave.dailyFlags")
  expect(ichor16(S.OFF_ICHOR_VARS) == 1234 and ichor16(S.OFF_ICHOR_VARS + 62) == 0xBEEF,
         "bank vars land in IchorSave.vars")
  L.runHeader("SaveTest_Bank2Header")
  local first, last = S.FLAG_ICHOR_GENERAL2_START - S.ICHOR_FLAGS2_START, S.ICHOR_FLAGS2_END - S.ICHOR_FLAGS2_START
  expect(L.getVar(S.VAR_0x8001) == 3 and ichor8(S.OFF_ICHOR_FLAGS2 + (first >> 3)) & (1 << (first & 7)) ~= 0
         and ichor8(S.OFF_ICHOR_FLAGS2 + (last >> 3)) == 0x80,
         "the second bank: scripts set and read its first and last flags, in IchorSave.flags2")
  expect(sb1Flags() == before, "no SaveBlock1 flag changed")
  -- VAR_TEMP_F is the only SaveBlock1 var the script writes
  L.setVar(S.VAR_TEMP_F, 0)
  expect(L.snapshot(L.sb1() + S.OFF_SB1_VARS, 0x200) == varsBefore, "no other SaveBlock1 var changed")
  L.setVar(S.VAR_TEMP_F, 1)

  -- 3. A new day: the same day changes nothing, then move the RTC offset back a
  -- day and run the time-based events again
  L.runHeader("SaveTest_NewDayHeader")
  expect(L.getFlag(S.FLAG_DAILY_ICHOR_PRAYED_START + 2), "the same day keeps the daily bank")
  local day0 = L.getVar(S.VAR_DAYS)
  local off = L.sb2() + S.OFF_SB2_LOCAL_TIME_OFFSET
  emu:write16(off, (emu:read16(off) - 1) & 0xFFFF)
  L.runHeader("SaveTest_NewDayHeader")
  expect(L.getVar(S.VAR_DAYS) == day0 + 1, string.format("the day turned (VAR_DAYS %d -> %d)", day0, L.getVar(S.VAR_DAYS)))
  expect(allZero(S.OFF_ICHOR_DAILY_FLAGS, 32), "a new day clears the daily bank")
  expect(L.getFlag(S.FLAG_ICHOR_GENERAL_START) and L.getFlag(S.ICHOR_FLAGS_END) and L.getVar(S.ICHOR_VARS_START) == 1234,
         "... and leaves the saved bank and vars alone")

  -- 7a. A hidden item with a bank flag: found once
  plantHiddenItem()
  local potions = L.itemCount(S.ITEM_POTION)
  local found = searchHiddenItem()
  expect(found and L.getFlag(HIDDEN_FLAG) and L.itemCount(S.ITEM_POTION) == potions + 1,
         "a hidden item with a second-bank flag is found, and its flag is set in IchorSave")
  shot("hidden_item")
  expect(not searchHiddenItem() and L.itemCount(S.ITEM_POTION) == potions + 1, "... and not found twice")

  -- 4. Save, reset, CONTINUE
  L.setFlag(S.FLAG_DAILY_ICHOR_GENERAL_START + 5, true)   -- a daily flag, saved mid-day
  emu:write16(L.ichor() + S.OFF_ICHOR_MOM_WINS, 3)
  local oath = L.ichor() + S.OFF_ICHOR_OATH
  local chanceByte = S.OFF_OATH_ENCOUNTERS + (S.MAPSEC_KALLISTE_ROUTE_1 >> 3)
  local chanceMask = 1 << (S.MAPSEC_KALLISTE_ROUTE_1 & 7)
  emu:write8(oath + S.OFF_OATH_STATE, S.ICHOR_OATH_ACTIVE)
  emu:write16(oath + S.OFF_OATH_FALLEN_COUNT, 7)
  emu:write8(oath + chanceByte, chanceMask)
  local saved = L.snapshot(L.ichor(), S.ICHOR_SAVE_SIZE)
  L.runHeader("SaveTest_SaveHeader")
  shot("saved")
  emu:reset()
  L.continueSave()
  shot("continued")
  expect(L.snapshot(L.ichor(), S.ICHOR_SAVE_SIZE) == saved,
         string.format("all %d bytes of IchorSave come back from the save", S.ICHOR_SAVE_SIZE))
  expect(ichor8(S.OFF_ICHOR_OATH + S.OFF_OATH_STATE) == S.ICHOR_OATH_ACTIVE
         and ichor16(S.OFF_ICHOR_OATH + S.OFF_OATH_FALLEN_COUNT) == 7
         and ichor8(S.OFF_ICHOR_OATH + chanceByte) == chanceMask,
         "the Oath state, fallen count and named-area receipt survive CONTINUE")
  expect(L.getFlag(S.ICHOR_FLAGS2_END), "the second bank's flags come back too")
  plantHiddenItem()
  expect(L.getFlag(HIDDEN_FLAG) and not searchHiddenItem() and L.itemCount(S.ITEM_POTION) == potions + 1,
         "7b. after a save and CONTINUE, the hidden item is still taken")
  expect(L.getFlag(S.FLAG_ICHOR_HERMS_START + 3) and L.getFlag(S.FLAG_DAILY_ICHOR_GENERAL_START + 5)
         and L.getVar(S.ICHOR_VARS_END) == 0xBEEF and ichor16(S.OFF_ICHOR_MOM_WINS) == 3,
         "flags, daily flags, vars and Mom's record read back through the engine")

  -- 8. A version-4 save may hold arbitrary bytes in the new Oath allocation.
  local prefix = L.snapshot(L.ichor() + 4, S.OFF_ICHOR_OATH - 4)
  local secondBank = L.snapshot(L.ichor() + S.OFF_ICHOR_FLAGS2,
                                S.ICHOR_SAVE_SIZE - S.OFF_ICHOR_FLAGS2)
  emu:write8(L.ichor() + S.OFF_ICHOR_VERSION, 4)
  for i = 0, S.ICHOR_OATH_SIZE - 1 do
    emu:write8(L.ichor() + S.OFF_ICHOR_OATH + i, 0xFF)
  end
  L.runHeader("SaveTest_SaveHeader")
  emu:reset()
  L.continueSave()
  expect(ichor8(S.OFF_ICHOR_VERSION) == S.ICHOR_SAVE_VERSION
         and allZero(S.OFF_ICHOR_OATH, S.ICHOR_OATH_SIZE),
         "version 4 clears stale reserved bytes instead of swearing an Oath")
  expect(L.snapshot(L.ichor() + 4, S.OFF_ICHOR_OATH - 4) == prefix
         and L.snapshot(L.ichor() + S.OFF_ICHOR_FLAGS2,
                        S.ICHOR_SAVE_SIZE - S.OFF_ICHOR_FLAGS2) == secondBank,
         "version-4 migration preserves both banks, vars, Favor and the Thread")
  shot("version4_continued")

  -- 6. A version-3 save: junk where the second bank now sits (the old dexNavChain)
  emu:write8(L.ichor() + S.OFF_ICHOR_VERSION, 3)
  emu:write8(L.ichor() + S.OFF_ICHOR_FLAGS2, 0x5A)
  L.runHeader("SaveTest_SaveHeader")
  emu:reset()
  L.continueSave()
  expect(ichor8(S.OFF_ICHOR_VERSION) == S.ICHOR_SAVE_VERSION and allZero(S.OFF_ICHOR_FLAGS2, S.ICHOR_SAVE_SIZE - S.OFF_ICHOR_FLAGS2)
         and ichor16(S.OFF_ICHOR_MOM_WINS) == 3 and L.getFlag(S.FLAG_ICHOR_HERMS_START + 3),
         "a version-3 save loads with the second bank zeroed and everything else kept")

  -- 5. An old save: zero IchorSave, save, reset, CONTINUE
  for i = 0, S.ICHOR_SAVE_SIZE - 1, 4 do emu:write32(L.ichor() + i, 0) end
  L.runHeader("SaveTest_SaveHeader")
  emu:reset()
  L.continueSave()
  shot("old_save_continued")
  expectDefaults("a save from before IchorSave")
  log(string.format("ok SaveBlock3 is %d bytes; IchorSave has %d reserved bytes",
                    S.SB3_SIZE, S.OFF_ICHOR_FLAGS2 - S.OFF_ICHOR_RESERVED))
end)
