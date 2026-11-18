-- The climax, played through (design/phase4/SCRIPT.md III-9 to III-12): down into
-- the Loom on the night of the Omphalos, the cut and the gray, the Frozen Hour's
-- tour (the Cutter, the Measurer and Medon, the decree, Phaedon reading the true
-- prophecy, Mom's cloak, the Spinner), Kleon breaking his thread, the climb, the
-- multi battle, the crumble, the Lord of Time, the Moment and the twelve chimes,
-- Elpis's line, and the League's L-1 opening in Astyra. The Wings are stood in
-- for by test headers that land at each map's door.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
for k, v in pairs(dofile(L.OUT .. "climax_scripts.lua")) do S.SCRIPTS[k] = v end
local function flag(f, text) L.expect(L.getFlag(f), text) end
local function act3() return L.getVar(S.VAR_ICHOR_ACT3) end

-- How far the field is from color: the share of BG palette colors that are gray.
local function grayShare()
  local gray, n = 0, 0
  for i = 6 * 16 + 1, 13 * 16 - 1 do
    local c = emu:read16(S.gPlttBufferFaded + i * 2)
    local r, g, b = c & 31, (c >> 5) & 31, (c >> 10) & 31
    if c ~= 0 then
      n = n + 1
      if math.abs(r - g) <= 1 and math.abs(g - b) <= 1 then gray = gray + 1 end
    end
  end
  return n > 0 and gray / n or 0
end

local function fly(header, map, what)
  L.runHeader(header)
  L.settle()
  L.expect(L.mapId() == map, what)
end

L.start(function()
  L.quickstart()
  L.runHeader("Climax_SetupHeader")
  L.expect(L.mapId() == S.MAP_OMPHALOS_STAIR, "the climax starts where Delphoi's chapter ends")
  L.shot("omphalos_stair")

  -- III-9. Down the Omphalos stair into the Loom: the scene plays on arrival.
  L.setVar(S.VAR_TEMP_0, 1)   -- the music box's ticks (coord events) are sound only
  L.go(9, 38)
  for _ = 1, 3 do   -- the bottom step is an arrow mat: press on down into the dark
    if L.mapId() ~= S.MAP_OMPHALOS_STAIR then break end
    L.tap(K.DOWN, 8)
    L.wait(20)
  end
  L.settle({ limit = 60000, shots = { [1] = "loom_reveal", [8] = "loom_fates", [30] = "loom_harpe" } })
  L.expect(L.mapId() == S.MAP_LOOM, "the Omphalos stair comes down into the Loom")
  flag(S.FLAG_HONEY, "the Fates are given Melitta's Honey")
  L.expect(L.itemCount(S.ITEM_HONEY) == 0, "the jar is used up at the Loom")
  flag(S.FLAG_CUT, "the chains are cut")
  flag(S.FLAG_FROZEN, "the Frozen Hour begins at the Loom")
  L.expect(act3() == 15, "VAR_ICHOR_ACT3 is 15 after the cut")
  L.expect(grayShare() > 0.9, string.format("the Loom is gray (%.2f of its colors)", grayShare()))
  L.shot("loom_after")

  -- III-10A. The Stair's first step won't take your weight yet.
  L.go(2, 12)
  if L.step(K.UP) == "taken" then L.settle() end
  L.expect(L.mapId() == S.MAP_LOOM, "with no Fate roused the Stair turns you back")

  -- III-10C. Kaldera's forge: the Cutter.
  fly("Climax_ToForgeHeader", S.MAP_FORGE, "the Wings reach Kaldera's forge")
  L.shot("forge_frozen")
  L.talk(L.npc("Kaldera_TelchinesForge_EventScript_Cutter"))
  flag(S.FLAG_CUTTER, "the Cutter is roused")

  -- III-10D. The Pool of Mnemosyne: the Measurer, and Medon's memory.
  fly("Climax_ToArkadiaHeader", S.MAP_ARKADIA, "the Wings reach Arkadia")
  L.talk(L.npc("Arkadia_EventScript_Measurer"), { shots = { [2] = "medon_sepia" } })
  flag(S.FLAG_MEASURER, "the Measurer is roused")
  flag(S.FLAG_MEDON, "the pool shows Medon chaining the Fates")

  -- III-10E. Astyra: the unfinished decree, and Elpis's room.
  fly("Climax_ToStoaHeader", S.MAP_STOA, "the Wings reach the Stoa")
  L.talk(L.sign("Astyra_Stoa_EventScript_UnfinishedDecree"), { answers = { "yes" } })
  flag(S.FLAG_DECREE, "the unfinished decree is taken")
  fly("Climax_ToPhaedonsHouseHeader", S.MAP_PHAEDONS_HOUSE, "the Wings reach Phaedon's house")
  L.shot("bedside")
  L.talk(L.npc("Astyra_PhaedonsHouse_EventScript_Bedside"), { answers = { "yes" } })
  flag(S.FLAG_READ, "Phaedon reads Elpis's true prophecy")

  -- III-10F. Elaia: Mom's cloak, and the Spinner under the old olive.
  fly("Climax_ToHomeHeader", S.MAP_HOME, "the Wings reach home")
  L.talk(L.sign("ElaiaVillage_PlayersHouse_1F_EventScript_Loom"), { answers = { "yes" } })
  flag(S.FLAG_CLOAK, "Melitta's cloak goes on")
  fly("Climax_ToElaiaHeader", S.MAP_ELAIA, "the Wings reach Elaia")
  L.talk(L.npc("ElaiaVillage_EventScript_Spinner"))
  flag(S.FLAG_SPINNER, "the Spinner is roused: all twelve hours")

  -- III-10G. Delphoi's frozen court: Kleon breaks his thread as you pass him.
  fly("Climax_ToDelphoiHeader", S.MAP_DELPHOI, "the Wings reach Delphoi")
  L.shot("delphoi_frozen")
  L.goTrigger(L.triggers("Climax_EventScript_DelphoiKleonWakes"))
  L.settle({ shots = { [1] = "kleon_wakes" } })
  flag(S.FLAG_KLEON_WOKE, "Kleon breaks his own thread")
  L.expect(act3() == 16, "VAR_ICHOR_ACT3 is 16 when Kleon wakes")
  -- III-10B. The split Omphalos: the Stair of Hours climbs out of it.
  L.talk(L.sign("Delphoi_EventScript_Omphalos"))
  L.expect(L.mapId() == S.MAP_STAIR, "the Stair of Hours takes your weight now")
  L.shot("stair_foot")

  -- III-11A-B. The climb and the twelfth landing: the multi battle (Kleon beside you).
  L.goTrigger(L.triggers("StairOfHours_EventScript_KleonLine"))
  L.settle()
  L.shot("stair_climb")
  L.goTrigger(L.triggers("StairOfHours_EventScript_TwelfthLanding"))
  L.settle({ answers = { "no" }, limit = 120000, shots = { [1] = "twelfth_landing" } })
  flag(S.FLAG_BATTLE_WON, "the multi battle on the twelfth landing is won")
  flag(S.FLAG_CRUMBLED, "the stair falls away behind Kleon and Hyperion")
  L.expect(act3() == 17, "VAR_ICHOR_ACT3 is 17 after the multi battle")
  L.shot("crumble")

  -- III-11D-E. The Lord of Time, then the Moment: press A as it crosses the line.
  L.goTrigger(L.triggers("StairOfHours_EventScript_Shadow"))
  L.settle({ answers = { "yes" }, limit = 60000, stop = function()
    local x = L.objectAt(S.LOCALID_MOMENT)
    return x ~= nil and x < 19
  end })
  L.expect(L.getFlag(S.FLAG_LORD_FAINTED) or L.getFlag(S.FLAG_CAUGHT_LORD), "the Lord of Time is beaten")
  L.shot("the_moment")
  for _ = 1, 400 do
    local x = L.objectAt(S.LOCALID_MOMENT)
    if x == 13 then break end
    L.wait(1)
  end
  L.wait(2)
  L.tap(K.A)
  L.settle({ limit = 80000, shots = { [3] = "chimes" } })
  flag(S.FLAG_MOMENT, "the Moment is seized by the forelock")
  L.expect(not L.getFlag(S.FLAG_FROZEN), "the twelfth chime ends the Frozen Hour")

  -- III-12. Elpis's line, and the act's end.
  flag(S.FLAG_ELPIS_LINE, "Elpis wakes and says her thread isn't finished")
  flag(S.FLAG_OPHIUCHUS, "Ophiuchus takes its place in the Star Chart")
  flag(S.FLAG_ACT3_COMPLETE, "FLAG_ICHOR_ACT3_COMPLETE is set")
  L.expect(act3() == 19, "VAR_ICHOR_ACT3 is 19 after Elpis's line")
  flag(S.FLAG_RHEA, "Rhea holds out her wrists at dawn (III-12A)")
  L.expect(L.mapId() == S.MAP_ASTYRA, "the morning after begins in Astyra")
  L.expect(not L.getFlag(S.FLAG_HIDE_DECREE_CROWD), "the League's herald is in the street (L-1)")
  L.shot("astyra_morning")
  L.talk(L.npc("Astyra_EventScript_Kerykos"))
  flag(S.FLAG_LEAGUE_DECREE, "L-1: the Archon's decree is read")

  L.runHeader("Climax_SaveHeader")
  emu:reset()
  L.continueSave()
  L.expect(L.getFlag(S.FLAG_ACT3_COMPLETE) and act3() == 19, "the finished act survives save/reset/CONTINUE")
end)
