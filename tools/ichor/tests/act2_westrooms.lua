-- The road west's nine interiors, run by tools/ichor/tests/act2_westrooms.sh (read it first).
--
-- Setup touches no ROM data: after Quickstart, a test-only script in spare EWRAM gives
-- a Halcyling (party slot 1) and a Lophops (slot 2) and warps into each room. Story
-- flags other maps set (Goose home, Xenodike down) are set the same way, by script.
-- Every person, sign and hidden item is found by the script it runs (slice_lib.lua).
--
-- Prints "WEST ok ..." per check and "WEST shot ..." per screenshot, and ends with
-- "WEST done"; a failure prints "WEST FAIL: ..." first.

local OUT = os.getenv("WEST_OUT") or "build/test_westrooms/"
local L = dofile("tools/ichor/tests/slice_lib.lua")
L.init{ tag = "WEST", out = OUT, symbols = OUT .. "symbols.lua" }
local S, K = L.S, L.K
local wait, now, expect, shot, tap = L.wait, L.now, L.expect, L.shot, L.tap
local emu = L.emu

local HALL, HK, MASON = "Lebadeia_PilgrimsHall_EventScript_", "Lebadeia_HerkynaHouse_EventScript_",
  "Lebadeia_MasonsHouse_EventScript_"
local INN, STALL, MUL, SWP = "Kirrha_Inn_EventScript_", "Kirrha_Agora_EventScript_",
  "Kirrha_MuleteersHouse_EventScript_", "Kirrha_SweepersHouse_EventScript_"
local ACH, GOAT = "Aigion_AchaeansHouse_EventScript_", "Aigion_GoatherdsHouse_EventScript_"

local function warpTo(map, x, y, extra)
  local s = { S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 } }
  for _, b in ipairs(extra or {}) do s[#s + 1] = b end
  for _, b in ipairs({ S.SCR_OP_WARP, map >> 8, map & 0xFF, 0xFF, { x, 2 }, { y, 2 },
                       S.SCR_OP_WAITSTATE, S.SCR_OP_END }) do s[#s + 1] = b end
  L.runRamScript(s)
  L.waitUntil(function() return L.mapId() == map and L.idle() end, 3000, "arrival on map " .. map)
  wait(30)
end

local function setFlagOp(flag) return { S.SCR_OP_SETFLAG, { flag, 2 } } end

-- A party member's species, and its friendship written directly: substruct 0 holds
-- both (species in its first halfword, friendship in byte 9), XOR-encrypted with
-- personality ^ otId, its slot chosen by personality % 24 (as assistLevel100 does).
local function substruct0(slot)
  local mon = L.partyMon(slot)
  local personality, otId = emu:read32(mon), emu:read32(mon + 4)
  local key = personality ~ otId
  local s0 = emu:read8(S.sSubstructOffsets + personality % 24)
  return mon + S.OFF_BOXMON_SECURE, mon + S.OFF_BOXMON_SECURE + s0 * S.SUBSTRUCT_SIZE, key
end
local function partySpecies(slot)
  local _, base, key = substruct0(slot)
  return (emu:read32(base) ~ key) & 0x7FF
end
local function setFriendship(slot, value)
  local secure, base, key = substruct0(slot)
  local w = emu:read32(base + 8) ~ key
  w = (w & ~0xFF00) | ((value & 0xFF) << 8)
  emu:write32(base + 8, w ~ key)
  local sum = 0
  for i = 0, S.SECURE_WORDS - 1 do
    local v = emu:read32(secure + 4 * i) ~ key
    sum = sum + (v & 0xFFFF) + (v >> 16)
  end
  emu:write16(L.partyMon(slot) + S.OFF_BOXMON_CHECKSUM, sum & 0xFFFF)
end

local function hurt()
  for slot = 0, 1 do emu:write16(L.partyMon(slot) + S.OFF_MON_HP, 1) end
end
local function healed() return L.partyHp(0) > 1 and L.partyHp(1) > 1 end

-- Walk to the far tile and screenshot: the room's second view.
local function far(name, x, y) L.go(x, y); shot(name .. "_far") end

-- Kimon's trade's way through the storage screen (elaia_opening.lua): YES to the
-- offer, up to YOUR PARTY, the second Pokémon, SELECT.
local function tradeSecondMon(what)
  local t0 = now()
  while not L.on("CB2_PokeStorage") do
    if L.boxUp() then wait(34) end
    tap(K.A); wait(9)
    if now() - t0 > 3000 then shot("stuck"); L.fail("no storage screen for " .. what) end
  end
  wait(90); shot("trade_choose_mon")
  tap(K.UP); wait(20); tap(K.UP); wait(20)
  tap(K.A); wait(60); tap(K.DOWN); wait(20); shot("trade_choose_lophops")
  tap(K.A); wait(40)
  tap(K.A); wait(40)
  L.waitUntil(function() return not L.on("CB2_PokeStorage") end, 1200, "the storage screen to close")
  L.settle({ shots = { [1] = "trade_done" } })
end

local function main()
  L.setBeat("00_boot", false)
  L.waitUntil(function() return now() >= 500 end, 600, "frame 500")
  tap(K.START)
  L.waitUntil(function() return now() >= 1020 end, 600, "frame 1020")
  tap(K.SELECT)
  L.waitUntil(L.idle, 4000, "the new game")
  wait(30)
  local opt = L.sb2() + S.OFF_SB2_OPTIONS
  emu:write16(opt, (emu:read16(opt) & ~0x7) | 2 | (1 << 9) | (1 << 10))

  -- ---- Lebadeia: the pilgrims' hall ---------------------------------------------------
  L.setBeat("35_hall", false)
  warpTo(S.MAP_HALL, 7, 7, {
    S.SCR_OP_CALLNATIVE, { S.ScrCmd_createmon | 1, 4 }, 0, S.PARTY_SIZE,
    { S.SPECIES_HALCYLING, 2 }, { 30, 2 }, { 0, 4 },
    S.SCR_OP_CALLNATIVE, { S.ScrCmd_createmon | 1, 4 }, 0, S.PARTY_SIZE,
    { S.SPECIES_LOPHOPS, 2 }, { 30, 2 }, { 0, 4 },
    S.SCR_OP_SETFLAG, { S.FLAG_SYS_POKEMON_GET, 2 },
  })
  expect(partySpecies(0) == S.SPECIES_HALCYLING and partySpecies(1) == S.SPECIES_LOPHOPS,
         "a Halcyling and a Lophops in the party")
  shot("hall")
  hurt()
  L.talk(L.npc(HALL .. "Keeper"), { shots = { [1] = "hall_keeper_cold", [2] = "hall_keeper_warm" } })
  expect(healed(), "the hall-keeper heals the party at the fire")
  local hm = L.lastHeal()
  expect(hm == S.MAP_LEBADEIA, "entering the hall sets the respawn to Lebadeia")
  L.talk(L.npc(HALL .. "BenchPilgrim"))
  L.talk(L.npc(HALL .. "WeaverPilgrim"))
  L.talk(L.sign(HALL .. "VotiveWall"), { shotBefore = "hall_votive_wall", every = true })
  far("hall", 11, 4)
  L.talk(L.sign(HALL .. "HoneyCakes"))
  -- A whiteout wakes the player in front of the hall-keeper, and she heals them.
  L.whiteOut()
  L.waitUntil(function() return L.mapId() == S.MAP_HALL end, 3000, "the respawn in the pilgrims' hall")
  wait(60); shot("hall_respawn")
  L.settle()
  local x, y = L.pos()
  expect(x == 7 and y == 7, string.format("the whiteout respawn is at (7,7) before the keeper, got (%d,%d)", x, y))
  expect(healed(), "the hall-keeper heals the party after the whiteout")

  -- ---- Lebadeia: Herkyna's house ------------------------------------------------------
  L.setBeat("35_herkyna", false)
  warpTo(S.MAP_HERKYNA, 6, 9)
  shot("herkyna")
  expect(not L.npc(HK .. "Goose").present, "the goose pen is empty while Goose is lost")
  L.talk(L.npc(HK .. "Herkyna"))
  L.talk(L.npc(HK .. "Grandmother"))
  far("herkyna", 2, 3)
  L.talk(L.sign(HK .. "Race"))
  local water = L.itemCount(S.ITEM_MYSTIC_WATER_W)
  warpTo(S.MAP_HERKYNA, 6, 9, setFlagOp(S.FLAG_GOOSE))
  expect(L.npc(HK .. "Goose").present, "Goose is home in the pen once found")
  shot("herkyna_goose_home")
  L.talk(L.npc(HK .. "Herkyna"), { shots = { [1] = "herkyna_goose_thanks" } })
  expect(L.itemCount(S.ITEM_MYSTIC_WATER_W) == water + 1, "Herkyna gives the Mystic Water")
  L.talk(L.npc(HK .. "Herkyna"))
  expect(L.itemCount(S.ITEM_MYSTIC_WATER_W) == water + 1, "only once")
  L.talk(L.npc(HK .. "Goose"))

  -- ---- Lebadeia: the mason's house ----------------------------------------------------
  L.setBeat("35_mason", false)
  warpTo(S.MAP_MASON, 4, 6)
  shot("mason")
  L.talk(L.npc(MASON .. "Agamedes"), { shots = { [5] = "mason_agamedes" } })
  L.talk(L.sign(MASON .. "RoughStone"))
  local stars = L.itemCount(S.ITEM_STAR_PIECE)
  L.talk(L.sign(MASON .. "LooseStone"), { shotBefore = "mason_loose_stone" })
  expect(L.itemCount(S.ITEM_STAR_PIECE) == stars + 1, "the loose stone hides a Star Piece")
  L.talk(L.sign(MASON .. "LooseStone"))
  expect(L.itemCount(S.ITEM_STAR_PIECE) == stars + 1, "only once")
  local dust = L.itemCount(S.ITEM_STARDUST_W)
  L.talk(L.hidden(S.FLAG_MASON_STARDUST))
  expect(L.itemCount(S.ITEM_STARDUST_W) == dust + 1, "Stardust hidden in the dust drift")
  far("mason", 10, 4)

  -- ---- Kirrha: the pilgrims' inn ------------------------------------------------------
  L.setBeat("37_inn", false)
  warpTo(S.MAP_INN, 6, 10)
  shot("inn")
  expect(not L.npc(INN .. "Xenodike").present, "Xenodike isn't at the inn while she's at the lookout")
  hurt()
  L.talk(L.npc(INN .. "Strophios"), { shots = { [1] = "inn_strophios" } })
  expect(healed(), "Strophios heals the party")
  expect(L.lastHeal() == S.MAP_KIRRHA, "entering the inn sets the respawn to Kirrha")
  L.talk(L.npc(INN .. "Pylades"), { shots = { [5] = "inn_pylades_fig" } })
  L.talk(L.npc(INN .. "WellPilgrim"))
  L.talk(L.sign(INN .. "Sign"), { shotBefore = "inn_sign" })
  local coins = L.itemCount(S.ITEM_RELIC_COPPER_W)
  L.talk(L.hidden(S.FLAG_INN_COIN))
  expect(L.itemCount(S.ITEM_RELIC_COPPER_W) == coins + 1, "a pilgrim's coin down the well")
  far("inn", 12, 8)
  local sashes = L.itemCount(S.ITEM_FOCUS_SASH)
  warpTo(S.MAP_INN, 6, 10, setFlagOp(S.FLAG_XENODIKE))
  expect(L.npc(INN .. "Xenodike").present, "Xenodike is at the inn once she came down")
  shot("inn_xenodike")
  L.talk(L.npc(INN .. "Pylades"), { shots = { [2] = "inn_xenodike_yes" } })
  expect(L.itemCount(S.ITEM_FOCUS_SASH) == sashes + 1, "Pylades gives the Focus Sash")
  L.talk(L.npc(INN .. "Xenodike"))
  L.whiteOut()
  L.waitUntil(function() return L.mapId() == S.MAP_INN end, 3000, "the respawn in the inn")
  wait(60); shot("inn_respawn")
  L.settle()
  x, y = L.pos()
  expect(x == 6 and y == 4, string.format("the whiteout respawn is at (6,4) before Strophios, got (%d,%d)", x, y))
  expect(healed(), "Strophios heals the party after the whiteout")

  -- ---- Kirrha: the Agora stall --------------------------------------------------------
  L.setBeat("37_stall", false)
  warpTo(S.MAP_STALL, 5, 6)
  shot("stall")
  L.talk(L.npc(STALL .. "Stallkeeper"), { noSettle = true })
  for _ = 1, 2 do wait(40); tap(K.A) end
  wait(60); shot("stall_menu")
  tap(K.A); wait(60); shot("stall_buy")
  for _ = 1, 4 do tap(K.B); wait(40) end
  L.settle()
  L.talk(L.sign(STALL .. "VotiveTable"))
  far("stall", 9, 3)

  -- ---- Kirrha: the muleteer's house ---------------------------------------------------
  L.setBeat("37_muleteer", false)
  warpTo(S.MAP_MULETEER, 7, 8)
  shot("muleteer")
  expect(L.npc(MUL .. "Melisseer").present, "the Melisseer hums by the window before the trade")
  L.talk(L.npc(MUL .. "Melisseer"))
  L.talk(L.npc(MUL .. "Muleteer"), { noSettle = true })
  tradeSecondMon("the muleteer's trade")
  expect(partySpecies(1) == S.SPECIES_MELISSEER, "the muleteer traded his Melisseer for the Lophops")
  expect(not L.npc(MUL .. "Melisseer").present, "the Melisseer is gone from his house")
  L.talk(L.npc(MUL .. "Muleteer"), { shots = { [1] = "muleteer_kassotis" } })
  L.talk(L.sign(MUL .. "Mule"), { shotBefore = "muleteer_mule" })
  far("muleteer", 1, 5)

  -- ---- Kirrha: the old sweeper's house ------------------------------------------------
  L.setBeat("37_sweeper", false)
  warpTo(S.MAP_SWEEPER, 4, 6)
  shot("sweeper")
  local sprigs = L.itemCount(S.ITEM_LAUREL_SPRIG)
  L.talk(L.npc(SWP .. "Thyia"), { shots = { [1] = "sweeper_thyia" } })
  expect(L.itemCount(S.ITEM_LAUREL_SPRIG) == sprigs + 1, "Thyia gives a Laurel Sprig")
  L.talk(L.npc(SWP .. "Thyia"))
  expect(L.itemCount(S.ITEM_LAUREL_SPRIG) == sprigs + 1, "one a day")
  L.talk(L.sign(SWP .. "Laurel"))
  far("sweeper", 7, 3)

  -- ---- Aigion: the old Achaean's house ------------------------------------------------
  L.setBeat("37_achaean", false)
  warpTo(S.MAP_ACHAEAN, 4, 5)
  shot("achaean")
  local feathers = L.itemCount(S.ITEM_PRETTY_FEATHER)
  L.talk(L.npc(ACH .. "Tisamenos"), { shots = { [5] = "achaean_bird" } })
  expect(L.itemCount(S.ITEM_PRETTY_FEATHER) == feathers + 2, "Tisamenos gives two Pretty Feathers for the Halcyling")
  L.talk(L.sign(ACH .. "Frieze"), { shotBefore = "achaean_frieze" })
  far("achaean", 11, 3)

  -- ---- Aigion: the goatherd's house ---------------------------------------------------
  L.setBeat("37_goatherd", false)
  warpTo(S.MAP_GOATHERD, 8, 7)
  shot("goatherd")
  local bells = L.itemCount(S.ITEM_SOOTHE_BELL_W)
  L.talk(L.npc(GOAT .. "Helike"))
  expect(L.itemCount(S.ITEM_SOOTHE_BELL_W) == bells, "no bell while the lead Pokemon isn't sure of you")
  setFriendship(0, 220)
  L.talk(L.npc(GOAT .. "Helike"), { shots = { [4] = "goatherd_bell" } })
  expect(L.itemCount(S.ITEM_SOOTHE_BELL_W) == bells + 1, "Helike gives the Soothe Bell to a friendly lead")
  L.talk(L.npc(GOAT .. "Kid"))
  far("goatherd", 4, 6)

  L.log("tour and services played")
end

L.start(main)
