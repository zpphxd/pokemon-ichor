local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local MOM = "ElaiaVillage_PlayersHouse_1F_EventScript_Mom"
local RUNNERS = "EmporionCity_RunnersHouse_EventScript_"

local function talkMom()
  L.talk(L.npc(MOM), { answers = { "no" }, every = true })
end

local function saveAndContinue()
  L.runHeader("HomeTest_SaveHeader")
  emu:reset()
  L.continueSave()
end

local function fillHoneyPocket()
  local pocket = L.sb1() + S.OFF_SB1_BAG
  local key = emu:read32(L.sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
  local saved = {}
  for i = 0, S.BAG_ITEMS_COUNT - 1 do
    local slot = pocket + i * S.ITEM_SLOT_SIZE
    saved[i] = { emu:read16(slot), emu:read16(slot + 2) ~ key }
    emu:write16(slot, S.ITEM_HONEY)
    emu:write16(slot + 2, (S.MAX_BAG_ITEM_CAPACITY - (i == 0 and 1 or 0)) ~ key)
  end
  return function()
    pocket = L.sb1() + S.OFF_SB1_BAG
    key = emu:read32(L.sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
    for i = 0, S.BAG_ITEMS_COUNT - 1 do
      emu:write16(pocket + i * S.ITEM_SLOT_SIZE, saved[i][1])
      emu:write16(pocket + i * S.ITEM_SLOT_SIZE + 2, saved[i][2] ~ key)
    end
  end
end

L.start(function()
  L.quickstart()
  L.runHeader("HomeTest_SetupHeader")
  L.expect(L.mapId() == S.MAP_HOME, "the actual player's home")
  talkMom()
  L.expect(not L.getFlag(S.FLAG_ICHOR_GOT_MOMS_HONEY) and L.itemCount(S.ITEM_HONEY) == 0,
           "the opening does not grant the return gift")
  L.setFlag(S.FLAG_ICHOR_CROSSING_DONE, true)
  talkMom()
  L.expect(L.itemCount(S.ITEM_HONEY) == 0, "a pre-ending return keeps the Honey pending")
  L.setFlag(S.FLAG_ICHOR_ACT1_COMPLETE, true)
  talkMom()
  L.expect(not L.getFlag(S.FLAG_ICHOR_GOT_MOMS_HONEY) and L.itemCount(S.ITEM_HONEY) == 0,
           "the ending alone does not replace a letter home")

  L.runHeader("HomeTest_RunnersHeader")
  L.expect(L.mapId() == S.MAP_RUNNERS, "the actual runners' house")
  L.setFlag(S.FLAG_ICHOR_ACT1_COMPLETE, false)
  L.talk(L.npc(RUNNERS .. "Dromokleia"), { every = true })
  L.expect(L.itemCount(S.ITEM_QUICK_CLAW) == 1 and not L.getFlag(S.FLAG_ICHOR_WROTE_TO_MOM),
           "the first visit keeps Quick Claw and does not send an early letter")
  L.setFlag(S.FLAG_ICHOR_ACT1_COMPLETE, true)
  for _, runner in ipairs({ "Dromokleia", "Runner", "YoungRunner" }) do
    L.setFlag(S.FLAG_ICHOR_WROTE_TO_MOM, false)
    L.talk(L.npc(RUNNERS .. runner), { every = true })
    L.expect(L.getFlag(S.FLAG_ICHOR_WROTE_TO_MOM), runner .. " carries the post-ending letter")
  end
  L.talk(L.npc(RUNNERS .. "Dromokleia"), { every = true })
  L.expect(L.itemCount(S.ITEM_QUICK_CLAW) == 1, "the letter does not repeat Quick Claw")

  L.runHeader("HomeTest_EleusaHeader")
  L.setFlag(S.FLAG_ICHOR_WROTE_TO_MOM, false)
  L.talk(L.npc("EleusaVillage_EventScript_NorthHerald"), { every = true })
  L.expect(L.getFlag(S.FLAG_ICHOR_WROTE_TO_MOM), "Eleusa's herald carries the same letter")

  L.runHeader("HomeTest_ReturnHeader")
  local restore = fillHoneyPocket()
  local before = L.itemCount(S.ITEM_HONEY)
  talkMom()
  L.expect(L.itemCount(S.ITEM_HONEY) == before and not L.getFlag(S.FLAG_ICHOR_GOT_MOMS_HONEY),
           "one free space cannot partly pay the three-Honey gift")
  restore()
  saveAndContinue()
  L.expect(L.getFlag(S.FLAG_ICHOR_WROTE_TO_MOM) and not L.getFlag(S.FLAG_ICHOR_GOT_MOMS_HONEY),
           "the sent letter and pending gift survive save and CONTINUE")
  before = L.itemCount(S.ITEM_HONEY)
  talkMom()
  L.expect(L.getFlag(S.FLAG_ICHOR_GOT_MOMS_HONEY) and L.itemCount(S.ITEM_HONEY) == before + 3,
           "the pending gift retries as exactly three Honey")
  talkMom()
  L.expect(L.itemCount(S.ITEM_HONEY) == before + 3, "talking again cannot repeat the gift")
  saveAndContinue()
  L.expect(L.getFlag(S.FLAG_ICHOR_GOT_MOMS_HONEY) and L.itemCount(S.ITEM_HONEY) == before + 3,
           "the claimed gift and Honey survive save and CONTINUE")
  talkMom()
  L.expect(L.itemCount(S.ITEM_HONEY) == before + 3, "CONTINUE cannot reopen the claimed gift")
  L.talk(L.sign("ElaiaVillage_PlayersHouse_1F_EventScript_HoneyShelf"), { every = true })
  L.expect(L.itemCount(S.ITEM_HONEY) == before + 3, "the reserved story jar is not a second gift")
end)
