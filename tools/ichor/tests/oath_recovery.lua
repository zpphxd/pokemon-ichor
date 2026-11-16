local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local function oath() return L.ichor() + S.OFF_OATH end
local function boxed(box, slot)
  return emu:read32(S.gPokemonStoragePtr) + S.OFF_STORAGE_BOXES
    + box * S.BOX_BYTES + slot * S.BOX_MON_BYTES
end
local function read(addr, length)
  local bytes = {}
  for i = 0, length - 1 do bytes[i + 1] = emu:read8(addr + i) end
  return bytes
end
local function write(addr, bytes)
  for i, byte in ipairs(bytes) do emu:write8(addr + i - 1, byte) end
end
local function fight(header, ending)
  local falls = emu:read16(oath() + S.OFF_OATH_FALLEN_COUNT)
  L.runHeader(header, { noSettle = true })
  L.waitUntil(function()
    if emu:read16(oath() + S.OFF_OATH_FALLEN_COUNT) > falls then return true end
    L.tap(K.A); L.wait(4)
    return false
  end, 12000, "a real final partner fall")
  local fallen = read(S.gParties, S.PARTY_MON_BYTES)
  L.waitUntil(function()
    if ending then
      if L.on("CB2_OathEndScreen") then return true end
    elseif emu:read8(S.sOathAftermathNotice) & 0x80 ~= 0 then
      return true
    end
    L.tap(K.A); L.wait(4)
    return false
  end, 4000, ending and "the run-ending screen" or "the recovery notice")
  L.wait(120)
  return fallen
end
local function returnToTitle()
  L.tap(K.A)
  L.waitUntil(function() return L.on("CB2_InitTitleScreen") end, 300, "return to the native title")
  L.expect(not L.inOverworld(), "acknowledging the ending returns to the native title, never an unusable field party")
end

L.start(function()
  L.quickstart()
  L.runHeader("Oath_SetupHeader")
  emu:write8(oath() + S.OFF_OATH_STATE, S.ICHOR_OATH_ACTIVE)
  emu:write16(oath() + S.OFF_OATH_URN_BOXES, 1 << (S.TOTAL_BOXES_COUNT - 1))
  L.runHeader("Oath_UrnHeader")
  local healthy = read(S.gParties, S.BOX_MON_BYTES)
  write(boxed(0, 0), healthy)
  local fallen = fight("Oath_DefeatHeader", false)
  L.shot("living_storage_partner_recovered")
  L.expect(emu:read8(S.gPartiesCount) == 1 and L.partyHp(0) > 0
           and emu:read8(oath() + S.OFF_OATH_STATE) == S.ICHOR_OATH_ACTIVE,
           "a real scripted no-whiteout loss recovers a usable stored partner instead of resuming with no survivor")
  L.expect(L.snapshot(boxed(0, 0), S.BOX_MON_BYTES) == string.rep("00000000", S.BOX_MON_BYTES / 4),
           "recovery removes the living source from storage rather than duplicating it")
  for i = S.BOX_MON_BYTES + 1, #fallen do fallen[i] = nil end
  local urnRecord = L.snapshot(boxed(S.TOTAL_BOXES_COUNT - 1, 0), S.BOX_MON_BYTES)
  local matches = true
  for i, byte in ipairs(fallen) do
    if emu:read8(boxed(S.TOTAL_BOXES_COUNT - 1, 0) + i - 1) ~= byte then matches = false end
  end
  L.expect(matches, "the actual fallen partner reaches the Urn byte-for-byte before ordinary whiteout healing")
  L.tap(K.A); L.wait(120); L.shot("recovery_memorial_notice")
  L.tap(K.A); L.settle()
  L.runHeader("Oath_SaveHeader")
  emu:reset(); L.continueSave()
  L.expect(L.partyHp(0) > 0 and emu:read8(S.gPartiesCount) == 1
           and L.snapshot(boxed(S.TOTAL_BOXES_COUNT - 1, 0), S.BOX_MON_BYTES) == urnRecord,
           "the recovered party and unchanged memorial survive real save/reset/CONTINUE")

  local savedFalls = emu:read16(oath() + S.OFF_OATH_FALLEN_COUNT)
  local fallenParty = fight("Oath_DefeatHeader", true)
  L.shot("oath_exhaustion")
  L.expect(emu:read8(oath() + S.OFF_OATH_STATE) == S.ICHOR_OATH_FAILED and L.partyHp(0) == 0,
           "losing the final living partner ends the Oath without reviving or deleting them")
  returnToTitle()
  emu:reset(); L.continueSave()
  L.expect(emu:read8(oath() + S.OFF_OATH_STATE) == S.ICHOR_OATH_ACTIVE
           and emu:read16(oath() + S.OFF_OATH_FALLEN_COUNT) == savedFalls and L.partyHp(0) > 0
           and L.snapshot(boxed(S.TOTAL_BOXES_COUNT - 1, 0), S.BOX_MON_BYTES) == urnRecord,
           "ending the run leaves the last manual save unchanged and playable through CONTINUE")

  local healthyParty = read(S.gParties, S.PARTY_MON_BYTES)
  for slot = 1, 2 do
    local mon = S.gParties + slot * S.PARTY_MON_BYTES
    write(mon, healthyParty)
    emu:write16(mon + S.OFF_MON_HP, 1)
    emu:write32(mon + S.OFF_MON_STATUS, S.STATUS1_POISON)
  end
  write(S.gParties, fallenParty)
  emu:write8(S.gPartiesCount, 3)
  local pendingFieldRecord = L.snapshot(S.gParties, S.BOX_MON_BYTES)
  L.setVar(S.VAR_TEMP_E, 0)
  L.runHeader("Oath_FieldCleanupHeader", { noSettle = true })
  L.waitUntil(function() return emu:read32(S.gParties + S.PARTY_MON_BYTES + S.OFF_MON_STATUS) == 0 end,
              600, "the first modern poison-survival message")
  L.wait(90); L.shot("field_poison_before_compaction")
  L.expect(emu:read8(S.gPartiesCount) == 3 and L.partyHp(1) == 1
           and emu:read32(S.gParties + 2 * S.PARTY_MON_BYTES + S.OFF_MON_STATUS) == S.STATUS1_POISON,
           "field cleanup does not compact the party while later poison messages still need their original indices")
  L.waitUntil(function()
    if emu:read8(S.sOathAftermathNotice) & 0x80 ~= 0 then return true end
    L.tap(K.A); L.wait(4)
    return false
  end, 1500, "the survivor-safe field burial notice")
  L.wait(120); L.shot("field_poison_urn_notice")
  L.expect(emu:read8(S.gPartiesCount) == 2 and L.partyHp(0) == 1 and L.partyHp(1) == 1
           and emu:read32(S.gParties + S.OFF_MON_STATUS) == 0
           and emu:read32(S.gParties + S.PARTY_MON_BYTES + S.OFF_MON_STATUS) == 0,
           "both modern poison survivors keep one HP and finish their messages before burial compacts the party")
  L.expect(emu:read16(oath() + S.OFF_OATH_FALLEN_COUNT) == savedFalls
           and L.getVar(S.VAR_TEMP_E) == 0 and not L.idle(),
           "modern poison adds no fall and the original script remains paused until the Urn notice is acknowledged")
  L.tap(K.A); L.settle()
  L.expect(L.getVar(S.VAR_TEMP_E) == 77
           and L.snapshot(boxed(S.TOTAL_BOXES_COUNT - 1, 0), S.BOX_MON_BYTES) == urnRecord
           and L.snapshot(boxed(S.TOTAL_BOXES_COUNT - 1, 1), S.BOX_MON_BYTES) == pendingFieldRecord,
           "field burial resumes the original script without changing the existing memorial")
  emu:reset(); L.continueSave()

  write(boxed(0, 0), healthy)
  write(S.gParties, fallenParty)
  L.runHeader("Oath_FieldCleanupHeader", { noSettle = true })
  L.waitUntil(function()
    if emu:read8(S.sOathAftermathNotice) & 0x80 ~= 0 then return true end
    L.tap(K.A); L.wait(4)
    return false
  end, 4000, "the native all-party field-loss recovery")
  L.wait(120); L.shot("field_loss_storage_recovery")
  L.expect(emu:read8(S.gPartiesCount) == 1 and L.partyHp(0) > 0
           and emu:read8(oath() + S.OFF_OATH_STATE) == S.ICHOR_OATH_ACTIVE,
           "the native all-party field-loss script reaches the same living-storage recovery instead of reviving the fallen")
  L.tap(K.A); L.wait(120); L.tap(K.A); L.settle()
  emu:reset(); L.continueSave()

  L.runHeader("Oath_WeakPartyHeader")
  for slot = 1, 5 do write(S.gParties + slot * S.PARTY_MON_BYTES, fallenParty) end
  emu:write8(S.gPartiesCount, 6)
  for box = 0, S.TOTAL_BOXES_COUNT - 2 do write(boxed(box, 0), healthy) end
  for slot = 0, S.IN_BOX_COUNT - 1 do write(boxed(S.TOTAL_BOXES_COUNT - 1, slot), fallen) end
  local fullStorage = L.snapshot(boxed(0, 0), S.TOTAL_BOXES_COUNT * S.BOX_BYTES)
  fight("Oath_LoseHeader", true)
  L.shot("recovery_capacity_refusal")
  L.expect(emu:read8(oath() + S.OFF_OATH_STATE) == S.ICHOR_OATH_ACTIVE,
           "blocked capacity does not falsely declare exhaustion while living stored partners exist")
  L.expect(emu:read8(S.gPartiesCount) == 6 and L.snapshot(boxed(0, 0), S.TOTAL_BOXES_COUNT * S.BOX_BYTES) == fullStorage,
           "the full-party full-Urn exception preserves every stored record and all six fallen partners")
  returnToTitle()
  emu:reset(); L.continueSave()
  L.expect(L.partyHp(0) > 0 and emu:read8(S.gPartiesCount) == 1
           and emu:read16(oath() + S.OFF_OATH_FALLEN_COUNT) == savedFalls,
           "the capacity exception also leaves the last manual save unchanged")

  emu:write8(oath() + S.OFF_OATH_STATE, S.ICHOR_OATH_FAILED)
  L.runHeader("Oath_SaveHeader")
  emu:reset()
  L.wait(500); L.tap(K.START); L.wait(500); L.tap(K.A)
  L.waitUntil(function() return L.on("CB2_MainMenu") end, 900, "the main menu with a failed fixture save")
  L.wait(80); L.tap(K.A)
  L.waitUntil(function() return L.on("CB2_OathEndScreen") end, 3000, "the failed-save load guard")
  L.wait(120); L.shot("failed_save_load_guard")
  L.expect(not L.inOverworld() and emu:read8(oath() + S.OFF_OATH_STATE) == S.ICHOR_OATH_FAILED,
           "a saved FAILED state cannot bypass its terminal screen by using CONTINUE")
  returnToTitle()
end)
