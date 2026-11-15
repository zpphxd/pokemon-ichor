-- The post-game's opening on Kalliste, run by tools/ichor/tests/pg_opening.sh (read it first).
--
-- 1. With FLAG_ICHOR_POSTGAME clear, nothing of the post-game shows in Elaia or Akti:
--    its people's FLAG_TEMP hide flags are set, Nausikles still stands at the gangplank,
--    the quay's triggers are off, and the slice's own people are where they were.
-- 2. With it set: Kleon at Elaia's well (LABORS scene 0), the heralds, the Euploia
--    given on Akti's quay (ODYSSEY scene 1) and the gangplank, Lampon's fire from the
--    great hearth to the quay, Diktys's boat (Route 1's root and Demeas's rope),
--    Glaukias in the Fisher's house, and Phaedon's heal in the Asclepeion.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local log, expect, wait, shot = L.log, L.expect, L.wait, L.shot

-- The post-game's scripts are EventScript_Ichor*: engine_build.sh lists them at the
-- top level, and L.npc looks people up by script in S.SCRIPTS.
for name, addr in pairs(S) do
  if type(name) == "string" and name:match("^EventScript_Ichor") then S.SCRIPTS[name] = addr end
end

local function warp(header, x, y, map)
  L.setVar(S.VAR_0x8008, x); L.setVar(S.VAR_0x8009, y)
  L.runHeader(header, { limit = 4000 })
  L.waitUntil(function() return L.mapId() == map and L.idle() end, 3000, header)
  wait(40)
end

local function at(localId, x, y, what)
  local ox, oy = L.objectAt(localId)
  expect(ox == x and oy == y, string.format("%s stands at (%d,%d) (found %s)", what, x, y,
                                            ox and string.format("(%d,%d)", ox, oy) or "nobody"))
end

local function gone(localId, what)
  expect(L.objectAt(localId) == nil, what .. " isn't there")
end

local function talk(script, opts)
  L.talk(L.npc(script), opts)
end

L.start(function()
  L.quickstart()
  L.runHeader("PgTest_SetupHeader", { limit = 4000 })

  -- 1. Before the post-game ----------------------------------------------------------------
  L.setBeat("before", false)
  expect(not L.getFlag(S.FLAG_ICHOR_POSTGAME), "the post-game flag starts clear")

  warp("PgTest_ElaiaHeader", 24, 16, S.MAP_ELAIA)
  shot("elaia_before")
  expect(L.getFlag(S.FLAG_TEMP_18) and L.getFlag(S.FLAG_TEMP_19), "Elaia: Kleon's and the herald's hide flags are set")
  gone(S.LOCALID_ELAIA_PG_KLEON, "Elaia: Kleon at the well")

  warp("PgTest_AktiHeader", 12, 12, S.MAP_AKTI)
  shot("akti_before")
  expect(L.getFlag(S.FLAG_TEMP_18) and L.getFlag(S.FLAG_TEMP_19) and L.getFlag(S.FLAG_TEMP_1A),
         "Akti: the herald's, Alethea's and Lampon's hide flags are set")
  gone(S.LOCALID_AKTI_PG_ALETHEA, "Akti: Alethea on the deck")
  gone(S.LOCALID_AKTI_PG_LAMPON, "Akti: Lampon on the quay")
  at(S.LOCALID_AKTI_NAUSIKLES, 7, 9, "Akti: Nausikles, at the gangplank as in the slice,")
  expect(L.getVar(S.VAR_TEMP_5) == 0 and L.getVar(S.VAR_TEMP_6) == 0, "Akti: the post-game's quay triggers are off")
  expect(not L.getFlag(S.FLAG_TEMP_1B), "Akti: Diktys keeps his place on the beach")

  warp("PgTest_AsclepeionHeader", 7, 6, S.MAP_AKTI_ASCLEPEION)
  shot("asclepeion_before")
  at(S.LOCALID_AKTI_HEALER, 7, 2, "the Asclepeion: the healer, at her counter,")
  gone(S.LOCALID_AKTI_PG_PHAEDON, "the Asclepeion: Phaedon")
  gone(S.LOCALID_AKTI_PG_ELPIS, "the Asclepeion: Elpis")

  warp("PgTest_FishersHeader", 4, 6, S.MAP_AKTI_FISHERS)
  at(S.LOCALID_AKTI_GLAUKOS, 3, 2, "the Fisher's house: Glaukos")
  at(S.LOCALID_FISHERS_HOUSE_GLAUKIAS, 6, 6, "the Fisher's house: his grandson")

  warp("PgTest_TempleHeader", 8, 18, S.MAP_AKTI_TEMPLE)
  at(S.LOCALID_TEMPLE_LAMPON, 8, 15, "the temple: Lampon at the great hearth")

  -- 2. The post-game ------------------------------------------------------------------------
  L.setFlag(S.FLAG_ICHOR_POSTGAME, true)

  -- Kleon at the well, once
  L.setBeat("kleon", false)
  warp("PgTest_ElaiaHeader", 24, 16, S.MAP_ELAIA)
  at(S.LOCALID_ELAIA_PG_KLEON, 24, 18, "Elaia: Kleon on the well's edge")
  shot("elaia_kleon_at_well")
  talk("EventScript_IchorPg_KleonWell", { shots = { [1] = "kleon_second", [5] = "kleon_twelve", [7] = "kleon_olympia" } })
  expect(L.getFlag(S.FLAG_ICHOR_PG_KLEON_AT_WELL), "Kleon's scene sets its flag")
  gone(S.LOCALID_ELAIA_PG_KLEON, "Kleon, gone toward Olympia,")
  talk("ElaiaVillage_EventScript_Gylippos", { shots = { [1] = "gylippos_olympia" } })

  L.setBeat("heralds", false)
  talk("EventScript_IchorHerald_Elaia", { shots = { [1] = "herald_elaia_truce", [2] = "herald_elaia_road" } })
  expect(L.getVar(S.VAR_0x8004) == S.ICHOR_HERALD_ELAIA, "Elaia's herald speaks for Elaia")
  warp("PgTest_ElaiaHeader", 24, 16, S.MAP_ELAIA)
  gone(S.LOCALID_ELAIA_PG_KLEON, "Kleon, after a reload,")

  -- The Euploia: scene 1 on Akti's quay
  L.setBeat("euploia", false)
  warp("PgTest_AktiHeader", 12, 12, S.MAP_AKTI)
  gone(S.LOCALID_AKTI_NAUSIKLES, "Akti: the slice's Nausikles at the gangplank")
  at(S.LOCALID_AKTI_PG_NAUSIKLES, 5, 9, "Akti: Nausikles on his bollard")
  at(S.LOCALID_AKTI_PG_ALETHEA, 6, 8, "Akti: Alethea on the Euploia's deck")
  expect(L.getVar(S.VAR_TEMP_5) == 1, "Akti: scene 1 waits on the quay")
  shot("akti_quay_postgame")
  local fired = not L.goTrigger(L.triggers("EventScript_IchorPg_AktiShipRow9", "EventScript_IchorPg_AktiShipRow10",
                                           "EventScript_IchorPg_AktiShipRow11"))
  expect(fired, "crossing x = 10 starts scene 1")
  L.settle({ shots = { [1] = "nausikles_archon", [4] = "alethea_reachable", [9] = "euploia_given", [10] = "alethea_coming" } })
  expect(L.getFlag(S.FLAG_ICHOR_GOT_EUPLOIA), "scene 1 gives the Euploia")
  gone(S.LOCALID_AKTI_PG_ALETHEA, "Alethea, gone aboard,")
  local px, py = L.pos()
  expect(px == 6 and py == 9, string.format("the player stands between them at (6,9) (%d,%d)", px, py))
  expect(L.getVar(S.VAR_TEMP_5) == 2, "the gangplank boards now")
  talk("EventScript_IchorPg_Nausikles", { shots = { [1] = "nausikles_after" } })
  fired = not L.goTrigger(L.triggers("EventScript_IchorPg_AktiGangplank"))
  expect(fired, "the gangplank's foot asks to board")
  L.settle({ answers = { "no" }, shots = { [1] = "board_prompt" } })
  expect(L.mapId() == S.MAP_AKTI, "answering NO stays on the quay")
  talk("EventScript_IchorHerald_Akti", { shots = { [2] = "herald_akti_road" } })
  expect(L.getVar(S.VAR_0x8004) == S.ICHOR_HERALD_AKTI, "Akti's herald speaks for Akti")

  -- Lampon: Hestia's fire from the great hearth to the quay
  L.setBeat("lampon", false)
  warp("PgTest_TempleHeader", 8, 18, S.MAP_AKTI_TEMPLE)
  talk("AktiTown_TempleOfHestia_EventScript_Lampon", { shots = { [1] = "lampon_asks" } })
  expect(L.getFlag(S.FLAG_ICHOR_PG_LAMPON_ASKED), "Lampon asks for the fire")
  L.talk(L.sign("AktiTown_TempleOfHestia_EventScript_GreatHearth"), { answers = { "yes" }, shots = { [2] = "torch_lit" } })
  expect(L.getFlag(S.FLAG_ICHOR_PG_HEARTH_FIRE), "the Torch takes Hestia's fire at the great hearth")
  L.useWarp(S.MAP_AKTI)
  expect(L.getVar(S.VAR_TEMP_6) == 1 and L.getFlag(S.FLAG_ICHOR_PG_HEARTH_FIRE),
         "the fire comes out of the temple, and Lampon waits at the gangplank")
  expect(not L.getFlag(S.FLAG_TEMP_1A), "Akti: Lampon waits at the gangplank (his hide flag is clear)")
  shot("fire_out_of_temple")
  fired = not L.goTrigger(L.triggers("EventScript_IchorPgCrew_LamponQuayRow9", "EventScript_IchorPgCrew_LamponQuayRow10",
                                     "EventScript_IchorPgCrew_LamponQuayRow11"))
  expect(fired, "the quay takes the fire")
  L.settle({ shots = { [1] = "lampon_quay", [6] = "lampon_hearth_catches" } })
  expect(L.getFlag(S.FLAG_ICHOR_CREW_LAMPON) and not L.getFlag(S.FLAG_ICHOR_PG_HEARTH_FIRE),
         "Lampon takes the fire for the ship's hearth and joins the crew")
  gone(S.LOCALID_AKTI_PG_LAMPON, "Lampon, gone aboard,")
  warp("PgTest_TempleHeader", 8, 18, S.MAP_AKTI_TEMPLE)
  gone(S.LOCALID_TEMPLE_LAMPON, "the temple: Lampon, aboard now,")

  -- Diktys: a root from Route 1, rope from the Agora
  L.setBeat("diktys", false)
  warp("PgTest_AktiHeader", 11, 24, S.MAP_AKTI)
  talk("AktiTown_EventScript_Diktys", { shots = { [1] = "diktys_asks" } })
  expect(L.getFlag(S.FLAG_ICHOR_PG_DIKTYS_ASKED), "Diktys asks for a root and rope")
  warp("PgTest_Route1Header", 9, 26, S.MAP_ROUTE1)
  talk("KallisteRoute1_EventScript_OliveFarmer", { shots = { [1] = "farmer_root" } })
  expect(L.itemCount(S.ITEM_BIG_ROOT) == 1 and L.getFlag(S.FLAG_ICHOR_PG_GOT_BIG_ROOT), "the olive farmer gives a Big Root")
  warp("PgTest_AgoraHeader", 6, 6, S.MAP_AKTI_AGORA)
  talk("AktiTown_Agora_EventScript_Demeas", { shots = { [1] = "demeas_rope" } })
  expect(L.getFlag(S.FLAG_ICHOR_PG_GOT_ROPE), "Demeas puts the rope on Diktys's tab")
  warp("PgTest_AktiHeader", 11, 24, S.MAP_AKTI)
  talk("AktiTown_EventScript_Diktys", { shots = { [3] = "diktys_mended" } })
  expect(L.getFlag(S.FLAG_ICHOR_CREW_DIKTYS) and L.itemCount(S.ITEM_BIG_ROOT) == 0,
         "the boat is mended with the root, and Diktys joins the crew")
  gone(S.LOCALID_AKTI_DIKTYS, "Diktys, gone for his tools,")

  -- Glaukias: say yes
  L.setBeat("glaukias", false)
  warp("PgTest_FishersHeader", 4, 6, S.MAP_AKTI_FISHERS)
  gone(S.LOCALID_AKTI_GLAUKOS, "the Fisher's house: Glaukos (the sea kept him)")
  shot("fishers_house_postgame")
  talk("AktiTown_FishersHouse_EventScript_Grandson", { answers = { "yes" }, shots = { [1] = "glaukias_rod", [5] = "glaukias_begs" } })
  expect(L.itemCount(S.ITEM_OLD_ROD) == 1, "Glaukias hands over his grandfather's Old Rod")
  expect(L.getFlag(S.FLAG_ICHOR_CREW_GLAUKIAS), "Glaukias joins the crew")
  gone(S.LOCALID_FISHERS_HOUSE_GLAUKIAS, "Glaukias, off to the ship,")

  -- Phaedon's heal, and Elpis
  L.setBeat("phaedon", false)
  warp("PgTest_AsclepeionHeader", 7, 6, S.MAP_AKTI_ASCLEPEION)
  at(S.LOCALID_AKTI_PG_PHAEDON, 7, 2, "the Asclepeion: Phaedon at the counter")
  at(S.LOCALID_AKTI_HEALER, 11, 3, "the Asclepeion: the healer, by the Pithos,")
  at(S.LOCALID_AKTI_PG_ELPIS, 0, 9, "the Asclepeion: Elpis by the cot")
  shot("asclepeion_postgame")
  emu:write16(L.partyMon(0) + S.OFF_MON_HP, 1)
  local hp, maxHp = L.partyHp(0)
  expect(hp == 1, "the party is hurt (" .. hp .. "/" .. maxHp .. ")")
  talk("EventScript_IchorPg_Phaedon", { shots = { [1] = "phaedon_easy_now", [2] = "phaedon_there" } })
  hp, maxHp = L.partyHp(0)
  expect(hp == maxHp, string.format("Phaedon heals the party (%d/%d)", hp, maxHp))
  talk("EventScript_IchorPg_Elpis", { shots = { [1] = "elpis", [3] = "elpis_starry" } })
  shot("done")
end)
