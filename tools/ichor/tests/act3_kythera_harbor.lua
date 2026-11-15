-- Act III's opening voyage, III-1A to III-1C2 (see act3_kythera_harbor.sh).
--
-- Played with key presses on the real maps; the one assist is the start state
-- (Act II's end, from act3_kythera_harbor_setup.s) and two level-100 Metagross.
-- The walker routes by the live map grid, so moving a person or a trigger in the
-- builders never breaks the run; a missing one fails with its script's name.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S = L.S
for k, v in pairs(dofile(L.OUT .. "act3_scripts.lua")) do S.SCRIPTS[k] = v end

local P = { deck = "TriremeEuploia_DeckSouth_EventScript_", melos = "Melos_EventScript_",
            sk = "KytheraSkandeia_EventScript_" }

local function act3() return L.getVar(S.VAR_ICHOR_ACT3) end
local function flagCheck(flag, what) L.check(L.getFlag(S[flag]), what .. " (" .. flag .. ")") end

L.start(function()
  L.quickstart()

  -- III-1A. The boarding: Daphne's goodbye, Alethea's letter, Nausikles's YES
  L.setBeat("01_boarding", false)
  L.runHeader("Act3Harbor_StartHeader", { noSettle = true })
  L.waitUntil(function() return L.mapId() == S.MAP_DECK end, 900, "the southern deck")
  L.wait(40)
  L.shot("deck_moored")
  L.settle({ every = true, limit = 30000 })
  L.expect(L.mapId() == S.MAP_DECK, "back on deck for the night crossing")
  flagCheck("FLAG_ICHOR_DAPHNE_SAILED_ASTYRA", "Daphne sailed home")
  L.expect(act3() == 1, "VAR_ICHOR_ACT3 is 1 once aboard")
  L.shot("deck_night")

  -- III-1B. Route 22 by night: the lookout's fleet, Eudoros, then sleep
  L.setBeat("02_night", false)
  if not L.goTrigger(L.triggers(P.deck .. "TitanFleet")) then
    L.settle({ every = true })
  end
  flagCheck("FLAG_ICHOR_SAW_TITAN_FLEET", "the lookout showed the dark fleet")
  L.talk(L.npc(P.deck .. "Eudoros"), { shotBefore = "eudoros" })
  L.check(L.defeated(S.TRAINER_ICHOR_EUDOROS), "SAILOR Eudoros beaten")
  L.talk(L.npc(P.deck .. "OldSailor"), { shotBefore = "old_sailor" })
  L.talk(L.npc(P.deck .. "Nausikles"), { every = true, limit = 30000 })
  L.expect(L.mapId() == S.MAP_MELOS, "morning: Melos's jetty")
  flagCheck("FLAG_ICHOR_REACHED_MELOS", "landed at Melos")
  flagCheck("FLAG_ICHOR_VISITED_MELOS", "Nausikles's arrival lines played")
  L.shot("melos_jetty")

  -- III-1B2. Melos: Kentrios on the stair, the statue's rite, Theion, the seam
  L.setBeat("03_melos", false)
  if not L.goTrigger(L.triggers(P.melos .. "KentriosWarning")) then
    L.settle({ every = true })
  end
  flagCheck("FLAG_ICHOR_MET_KENTRIOS", "Kentrios warned of the turning statue")
  L.shot("melos_terrace")
  L.talk(L.npc(P.melos .. "Statue"), { every = true })
  flagCheck("FLAG_ICHOR_MELOS_RITE", "the statue's offering")
  L.shot("melos_statue_after_rite")
  L.talk(L.sign(P.melos .. "Seam"), { every = true, limit = 30000 })
  L.check(L.defeated(S.TRAINER_ICHOR_THEION), "TITANBORN Theion beaten on the way to the slope")
  flagCheck("FLAG_ICHOR_MELOS_OBSIDIAN_LUMP", "the lump of black glass from the seam")
  L.shot("melos_slope")

  -- III-1B3 and III-1C: sail on; Cape Malea; Skandeia's quay and the requisition
  L.setBeat("04_malea_and_skandeia", false)
  L.talk(L.npc(P.melos .. "Nausikles"), { every = true, limit = 40000 })
  L.expect(L.mapId() == S.MAP_SKANDEIA, "Skandeia's quay")
  flagCheck("FLAG_ICHOR_CROSSED_ROUTE22", "Malea rounded")
  L.expect(act3() == 2, "VAR_ICHOR_ACT3 is 2 on landing at Skandeia")
  flagCheck("FLAG_ICHOR_VISITED_SKANDEIA", "Skandeia is a fly target")
  L.check(L.defeated(S.TRAINER_ICHOR_MOLYBDOS), "TITANBORN Molybdos beaten")
  flagCheck("FLAG_ICHOR_EUPLOIA_KEPT", "the Euploia isn't requisitioned")
  L.check(L.objectAt(S.LOCALID_SKANDEIA_MOLYBDOS) == nil, "Molybdos stamps off down the quay")
  L.shot("skandeia_quay")

  -- The Kronist preaches to anyone walking down the quay
  L.setBeat("05_kronist", false)
  if not L.goTrigger(L.triggers(P.sk .. "KronistPreaches")) then
    L.settle({ every = true })
  end
  flagCheck("FLAG_ICHOR_HEARD_KRONIST", "the Kronist's sermon")

  -- III-1C2. Alethea on the main street, then the bad guests at Axylos's table
  L.setBeat("06_alethea", false)
  if not L.goTrigger(L.triggers(P.sk .. "AletheaRejoins")) then
    L.settle({ every = true, limit = 30000 })
  end
  flagCheck("FLAG_ICHOR_ALETHEA_REJOINED", "Alethea rejoined")
  local ax, ay = L.objectAt(S.LOCALID_SKANDEIA_ALETHEA_DOOR)
  L.check(ax == 11 and ay == 16, string.format("Alethea waits at Axylos's door (%s,%s)", ax, ay))
  L.shot("alethea_at_the_door")
  L.useWarp(S.MAP_AXYLOS_HOUSE, true)
  L.settle({ every = true, limit = 40000 })
  L.check(L.defeated(S.TRAINER_ICHOR_OCHROS) and L.defeated(S.TRAINER_ICHOR_PSEPHOS), "the bad guests beaten")
  flagCheck("FLAG_ICHOR_BAD_GUESTS_GONE", "the bad guests are gone")
  L.shot("axylos_table")
  L.useWarp(S.MAP_SKANDEIA)
  L.settle()
  L.check(L.objectAt(S.LOCALID_SKANDEIA_ALETHEA_DOOR) == nil, "Alethea has gone ahead (hidden at the door)")
  L.shot("street_after")

  -- The Asclepeion makes Skandeia the respawn point
  L.setBeat("07_asclepeion", false)
  L.useWarp(S.MAP_SKANDEIA_ASCLEPEION)
  L.settle()
  local hm, hx, hy = L.lastHeal()
  L.check(hm == S.MAP_SKANDEIA and hx == 22 and hy == 16,
          string.format("the respawn is Skandeia's Asclepeion door (map %d, %d,%d)", hm, hx, hy))
  L.useWarp(S.MAP_SKANDEIA)
  L.settle()

  -- III-1I. With the Horn (VAR_ICHOR_ACT3 = 4, set here), Nausikles sails for Amnisos
  L.setBeat("08_amnisos", false)
  L.setVar(S.VAR_ICHOR_ACT3, 4)
  L.talk(L.npc(P.sk .. "Nausikles"), { every = true, limit = 30000 })
  flagCheck("FLAG_ICHOR_SAILED_FOR_KNOSSA", "sailed for Knossa")
  L.expect(L.mapId() == S.MAP_DECK, "on deck for the run along Knossa's coast")
  L.shot("deck_to_amnisos")
  L.log("ok the voyage played through")
end)
