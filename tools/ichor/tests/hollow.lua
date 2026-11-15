-- Hecate's Hollow, run by tools/ichor/tests/hollow.sh (read it first).
--
-- Plays with key presses on tools/ichor/tests/engine_lib.lua (slice_lib's walker:
-- a breadth-first search over the live map, one step at a time). People, signs,
-- items, webs and braziers are found by the script they run or the flag they set,
-- so a moved one never breaks the walk; a missing one fails with its name.
--
-- The walk: in at the east mouth; the old woman; the dark road and its three barks;
-- the forks' side ways (fork 1's loop, fork 2's dead end and Phaino); the Hekataion
-- (beat 18: the offering, the Torch, the spring); the webs, Hekabe and her supper,
-- the braziers, the web chamber (Raknit, once the Arachne amphora is set), hall 2,
-- Kallias, Battos; the shortcut back east and its ledge; a wild Pokemon from the
-- Hollow's table; the hounds at night; and out of the west mouth.
--
-- Prints "HOLLOW ok ..." per check and "HOLLOW shot ..." per screenshot, and ends
-- with "HOLLOW done"; any failure prints "HOLLOW FAIL: ..." first.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
for k, v in pairs(dofile(L.OUT .. "hollow_symbols.lua")) do
  if k == "SCRIPTS" then
    for n, a in pairs(v) do S.SCRIPTS[n] = a end
  else
    S[k] = v
  end
end

local P = "HecatesHollow_EventScript_"
local function expect(cond, what) L.expect(cond, what) end
local function flash() return emu:read8(L.sb1() + S.OFF_SB1_FLASH) end
-- A lit place's flash level: 1, not 0, until the engine restarts the flash effect after
-- full light (ICHOR_STUB_DARKNESS in the map's scripts.pory).
local LIT = 1
local function region() return L.getVar(S.VAR_TEMP_2_E) end

-- A map id from include/constants/map_groups.h, or nil when it isn't registered.
local function mapConst(name)
  local f = io.open("include/constants/map_groups.h", "r")
  if not f then return nil end
  for line in f:lines() do
    local num, group = line:match("^%s+" .. name .. "%s*= %((%d+) | %((%d+) << 8%)%),")
    if num then f:close(); return tonumber(group) * 256 + tonumber(num) end
  end
  f:close()
  return nil
end

-- Warp to (x, y) on `map` from an ON_FRAME script in spare EWRAM.
local function warpTo(map, x, y)
  L.setVar(S.VAR_TEMP_0, 0)
  L.runRamScript({ S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 },
                   S.SCR_OP_WARP, map >> 8, map & 0xFF, 0xFF, { x, 2 }, { y, 2 }, S.SCR_OP_WAITSTATE, S.SCR_OP_END })
  L.waitUntil(function() return L.mapId() == map and L.idle() end, 3000, "the warp to map " .. map)
  L.wait(40)
end

-- A level-100 lead in party slot 0 (as eleusa.lua does it).
local function giveLead()
  local mon = L.partyMon(0)
  for o = 0, S.POKEMON_SIZE - 1 do emu:write8(mon + o, 0) end
  for k, b in ipairs({ 0xCE, 0xBF, 0xCD, 0xCE, 0xFF }) do emu:write8(mon + 7 + k, b) end -- "TEST"
  emu:write8(mon + 18, 2)
  emu:write8(mon + 19, 0x02)
  emu:write8(mon + 20, 0xFF)
  emu:write16(mon + S.OFF_BOXMON_SECURE, S.SPECIES_LEAD & 0x7FF)
  emu:write16(mon + S.OFF_BOXMON_SECURE + 12, S.MOVE_LEAD)   -- substruct 1 (attacks): move 1
  emu:write8(mon + S.OFF_BOXMON_SECURE + 20, 15)             -- and its PP
  local sum = 0
  for o = 0, 47, 2 do sum = sum + emu:read16(mon + S.OFF_BOXMON_SECURE + o) end
  emu:write16(mon + S.OFF_BOXMON_CHECKSUM, sum & 0xFFFF)
  emu:write8(mon + S.OFF_MON_LEVEL, 5)
  emu:write8(S.gPartiesCount, 1)
  -- the eighth badge only so the level-100 test Pokémon obeys (as emporion.lua does);
  -- nothing in the Hollow reads it
  L.setFlag(S.FLAG_BADGE08, true)
  L.assistLevel100()
  local hp, maxhp = L.partyHp(0)
  expect(L.partyLevel(0) == S.MAX_LEVEL and hp > 0, string.format("a level-100 lead (HP %d/%d)", hp, maxhp))
end

local function talk(target, what, opts)
  local boxes = L.talk(target, opts)
  expect((boxes or 0) >= 1, string.format("%s: %d message box(es)", what, boxes or 0))
  return boxes
end

local function quiet(on) L.setVar(S.VAR_REPEL_STEP_COUNT, on and 250 or 0) end

-- The local hour, by moving SaveBlock2's local time offset (struct Time: days s16,
-- hours s8): gLocalTime = the RTC minus the offset.
local function setHour(want)
  local now = emu:read8(S.gLocalTime + 2)
  local off = L.sb2() + S.OFF_SB2_LOCAL_TIME_OFFSET
  local h = (emu:read8(off + 2) + (now - want)) % 24
  if h >= 12 then h = h - 24 end
  emu:write8(off + 2, h & 0xFF)
end

-- --- The east mouth -------------------------------------------------------------------------

local function eastMouth()
  L.setBeat("east_mouth", false)
  warpTo(S.MAP_HOLLOW, 46, 34)
  expect(L.mapMusic() == S.MUS_HOLLOW, "the Hollow plays MUS_ICHOR_HOLLOW")
  expect(flash() == LIT and region() == 1, string.format("daylight at the east mouth (flash %d, region %d)", flash(), region()))
  L.shot("east_mouth_daylight")
  talk(L.npc(P .. "OldWoman"), "the old woman", { every = true })
  expect(L.getFlag(S.FLAG_MET_CRONE), "the old woman's warning heard")
  talk(L.npc(P .. "OldWoman"), "the old woman again")
  talk(L.sign(P .. "SignEast"), "the east mouth's stone", { shots = { [1] = "sign_east" } })
end

-- --- The dark road --------------------------------------------------------------------------

local function bark(script, what)
  local set = L.triggers(P .. script)
  local fired = not L.goTrigger(set)
  if fired then
    local boxes = L.settle({ shots = { [1] = "bark_" .. what } })
    expect(boxes >= 1, "the dog barks at " .. what)
  else
    L.fail("no bark at " .. what)
  end
end

local function darkRoad()
  L.setBeat("dark_road", false)
  quiet(true)
  L.go(36, 36)
  expect(flash() == 7, string.format("past the daylight it's dark: flash %d (no Torch: 7)", flash()))
  L.shot("dark_no_torch")
  -- fork 1: the bark says left; the right is a loop with the Escape Rope on it
  bark("BarkLeft", "fork1")
  L.talk(L.hidden(S.FLAG_HIDDEN_ESCAPE_ROPE))
  expect(L.getFlag(S.FLAG_HIDDEN_ESCAPE_ROPE), "fork 1's loop: the hidden Escape Rope")
  L.shot("fork1_loop")
  -- fork 2: right is the way on; the dead end left has the Bronze Obol and Phaino
  bark("BarkRight", "fork2")
  L.talk(L.ball(S.FLAG_ITEM_OBOL))
  expect(L.getFlag(S.FLAG_ITEM_OBOL), "fork 2's dead end: the Bronze Obol")
  if not L.defeated(S.TRAINER_PHAINO) then
    talk(L.npc(P .. "Phaino"), "Phaino", { shots = { [1] = "phaino" } })
  end
  expect(L.defeated(S.TRAINER_PHAINO), "Phaino beaten")
  talk(L.npc(P .. "Phaino"), "Phaino after")
  -- fork 3: straight ahead; the left loop hides Stardust
  bark("BarkAhead", "fork3")
  L.talk(L.hidden(S.FLAG_HIDDEN_STARDUST))
  expect(L.getFlag(S.FLAG_HIDDEN_STARDUST), "fork 3's loop: the hidden Stardust")
end

-- --- The Hekataion (beat 18) -------------------------------------------------------------------

local function hekataion()
  L.setBeat("hekataion", false)
  L.go(25, 12)
  expect(region() == 2 and flash() == 4, string.format("the Hekataion is lit faintly from above (flash %d)", flash()))
  L.shot("hekataion_faint")
  -- a web on the road west, before the Torch: fire would clear it
  talk(L.npc(P .. "Web", 1), "the west web without the Torch", { shots = { [1] = "web_no_torch" } })
  expect(not L.getFlag(S.FLAG_WEB_WEST), "the web stays without the Torch")
  -- the offering: once refused, then made
  talk(L.sign(P .. "Hekataion"), "the Hekataion, refused", { answers = { "no" }, every = true })
  expect(not L.getFlag(S.FLAG_GOT_TORCH), "no Torch for a refusal")
  talk(L.sign(P .. "Hekataion"), "beat 18", { every = true })
  expect(L.getFlag(S.FLAG_GOT_TORCH) and L.itemCount(S.ITEM_TORCH) == 1, "Hecate's Torch in the bag")
  expect(flash() == LIT, string.format("the Hekataion's torches burn (flash %d)", flash()))
  local mid = L.grid().tile(25, 5)
  expect(mid == S.MT_TORCH_S_GONE, string.format("the middle face's torch is gone (metatile 0x%03X)", mid or 0))
  L.shot("hekataion_lit")
  -- the midpoint rest and Hecate's altar
  local mon = L.partyMon(0)
  emu:write16(mon + S.OFF_MON_HP, 1)
  talk(L.sign(P .. "Spring"), "the spring")
  local hp = L.partyHp(0)
  expect(hp > 1, string.format("the spring heals (HP %d)", hp))
  talk(L.sign(P .. "Hekataion"), "Hecate's altar", { shots = { [1] = "altar" } })
  L.talk(L.hidden(S.FLAG_HIDDEN_HONEY))
  expect(L.getFlag(S.FLAG_HIDDEN_HONEY), "Hecate's supper niche: the hidden Honey")
end

-- --- The road west -----------------------------------------------------------------------------

local function burn(nth, flag, what)
  talk(L.npc(P .. "Web", nth), what, { shots = { [1] = "burn_" .. what } })
  L.wait(10)
  expect(L.getFlag(flag), what .. " burnt")
end

local function roadWest()
  L.setBeat("road_west", false)
  burn(1, S.FLAG_WEB_WEST, "web_west")
  local mid = L.grid().tile(13, 10)
  expect(mid == S.MT_WEB_TORN_0, string.format("the west web is torn (metatile 0x%03X)", mid or 0))
  -- through the neck into Hekabe's hall: she sees the player at the waist
  L.go(12, 14)
  -- the Torch's 3.5 tiles (flash 3); the prayer at her altar just now adds Hecate's
  -- blessing, one level more (flash 2, 4 tiles: ENGINE_API.md §3)
  expect(flash() == 2, string.format("with the Torch and Hecate's blessing, 4 tiles of light (flash %d)", flash()))
  L.shot("dark_with_torch")
  L.go(5, 15)
  expect(L.defeated(S.TRAINER_HEKABE), "Hekabe beaten at the waist")
  expect(L.getFlag(S.FLAG_HEKABE_SUPPER) and L.itemCount(S.ITEM_CAKE) >= 1, "Hekabe's supper: a Barley Cake")
  talk(L.npc(P .. "Hekabe"), "Hekabe after")
  talk(L.sign(P .. "Brazier1"), "brazier 1", { shots = { [2] = "brazier1_lit" } })
  expect(L.getFlag(S.FLAG_BRAZIER_1) and flash() == LIT, string.format("brazier 1 burns, its hall lit (flash %d)", flash()))
  L.shot("hall1_lit")
  -- the web chamber: Silk Scarf; Raknit once the Arachne amphora is done
  burn(4, S.FLAG_WEB_CHAMBER, "web_chamber")   -- its lower cell, faced from the hall
  L.talk(L.ball(S.FLAG_ITEM_SILK_SCARF))
  expect(L.getFlag(S.FLAG_ITEM_SILK_SCARF), "the web chamber's Silk Scarf")
  talk(L.sign(P .. "WebPictures"), "the webs' pictures")
  expect(not L.npc(P .. "Raknit").present, "no Raknit before the Arachne amphora")
  L.setFlag(S.FLAG_ARACHNE_AMPHORA, true)
  local x, y = L.pos()
  warpTo(S.MAP_HOLLOW, x, y)
  expect(L.npc(P .. "Raknit").present, "Raknit hangs in the web chamber after the amphora")
  L.shot("raknit")
  L.setFlag(S.FLAG_NO_RUNNING, true)     -- so the walker fights the static instead of running
  talk(L.npc(P .. "Raknit"), "Raknit")
  L.setFlag(S.FLAG_NO_RUNNING, false)
  expect(L.getFlag(S.FLAG_RAKNIT), "Raknit caught or beaten")
  L.setFlag(S.FLAG_ARACHNE_AMPHORA, false)
  -- hall 2: the second brazier, the Ether, Kallias in the dark, Battos at the mouth
  L.go(4, 21)
  talk(L.sign(P .. "Brazier2"), "brazier 2")
  expect(L.getFlag(S.FLAG_BRAZIER_2) and flash() == LIT, "brazier 2 burns")
  L.shot("hall2_lit")
  L.talk(L.ball(S.FLAG_ITEM_ETHER))
  expect(L.getFlag(S.FLAG_ITEM_ETHER), "the Ether by the second brazier")
  L.talk(L.ball(S.FLAG_ITEM_REVIVE))
  expect(L.getFlag(S.FLAG_ITEM_REVIVE), "the Revive in Kallias's passage")
  if not L.defeated(S.TRAINER_KALLIAS) then talk(L.npc(P .. "Kallias"), "Kallias") end
  expect(L.defeated(S.TRAINER_KALLIAS), "Kallias beaten")
  talk(L.npc(P .. "Kallias"), "Kallias after", { shots = { [1] = "kallias_after" } })
  talk(L.npc(P .. "Battos"), "Battos", { shots = { [1] = "battos" } })
  expect(L.defeated(S.TRAINER_BATTOS), "Battos beaten")
  talk(L.sign(P .. "SignWest"), "the west mouth's stone")
  L.go(2, 27)
  expect(flash() == LIT and region() == 5, "daylight at the west mouth")
  L.shot("west_mouth")
end

-- --- The shortcut back east, a wild Pokemon, the night ------------------------------------------

local function shortcut()
  L.setBeat("shortcut", false)
  L.go(39, 7)
  burn(5, S.FLAG_WEB_SHORTCUT, "web_shortcut")
  L.go(40, 16)
  L.tap(K.DOWN, 8)
  L.wait(40)
  local x, y = L.pos()
  expect(y == 18, string.format("down the ledge (at %d,%d)", x, y))
  -- A wild battle can break into a walk; try each pick-up again once if so.
  L.talk(L.ball(S.FLAG_ITEM_DUSK_BALL))
  if not L.getFlag(S.FLAG_ITEM_DUSK_BALL) then L.talk(L.ball(S.FLAG_ITEM_DUSK_BALL)) end
  expect(L.getFlag(S.FLAG_ITEM_DUSK_BALL), "the Dusk Ball at the ledge's foot")
  L.talk(L.hidden(S.FLAG_HIDDEN_HARD_STONE))
  if not L.getFlag(S.FLAG_HIDDEN_HARD_STONE) then L.talk(L.hidden(S.FLAG_HIDDEN_HARD_STONE)) end
  expect(L.getFlag(S.FLAG_HIDDEN_HARD_STONE), "the shortcut's hidden Hard Stone")
  L.go(43, 34)
  expect(region() == 1 and flash() == LIT, "back out in the east mouth's daylight")
  L.shot("shortcut_done")
  talk(L.npc(P .. "OldWoman"), "the old woman, after the Torch", { shots = { [1] = "old_woman_after" } })
end

local function wild()
  L.setBeat("wild", false)
  L.go(30, 36)
  quiet(false)
  local table_ = {}
  for _, n in ipairs({ "PEBBLITH", "SPALUNK", "GALEKIT", "GELASABLE", "ERGANT", "CHELONET" }) do
    table_[S["SPECIES_" .. n]] = n
  end
  local met
  for i = 1, 400 do
    local r = L.step((i % 2 == 0) and K.LEFT or K.RIGHT)
    if r == "taken" or L.inBattle() then
      L.waitUntil(L.inBattle, 1200, "the wild battle")
      L.wait(120)
      local species = emu:read16(S.gBattleMons + S.BATTLE_MON_SIZE + S.OFF_BATTLE_MON_SPECIES)
      local level = emu:read8(S.gBattleMons + S.BATTLE_MON_SIZE + S.OFF_BATTLE_MON_LEVEL)
      met = table_[species] or ("species " .. species)
      L.shot("wild_in_the_dark")
      expect(table_[species] ~= nil and level >= 17 and level <= 20,
             string.format("a wild %s, level %d, from the Hollow's table", met, level))
      L.settle()
      break
    end
  end
  expect(met ~= nil, "a wild Pokemon met on the cave floor")
  quiet(true)
end

local function night()
  L.setBeat("night", false)
  setHour(22)
  warpTo(S.MAP_HOLLOW, 24, 14)
  expect(L.npc(P .. "Hound").present, "at night a black hound sits at the pillar")
  L.go(24, 11)
  L.settle({ shots = { [1] = "hounds_fade" } })
  local w = L.objectAt(L.npc(P .. "HoundFading", 1).localId)
  local e = L.objectAt(L.npc(P .. "HoundFading", 2).localId)
  expect(w == nil and e == nil, "two of the hounds fade into the rock")
  L.shot("hound_stays")
  L.setFlag(S.FLAG_NO_RUNNING, true)
  talk(L.npc(P .. "Hound"), "Hecate's hound")
  L.setFlag(S.FLAG_NO_RUNNING, false)
  expect(L.getFlag(S.FLAG_HOUND), "the hound caught or beaten")
  setHour(12)
end

local function westMouth()
  L.setBeat("west_mouth", false)
  warpTo(S.MAP_HOLLOW, 2, 27)
  -- onto the mouth's arrow cell, then press on into the daylight
  L.go(0, 27)
  L.shot("west_mouth_edge")
  local route5 = mapConst("MAP_ROUTE5_SKIRONIAN_CLIFFS")
  emu:addKey(K.LEFT)
  L.waitUntil(function()
    local x = L.pos()
    return L.mapId() ~= S.MAP_HOLLOW or x ~= 0
  end, 600, "the west mouth's warp")
  emu:clearKey(K.LEFT)
  L.waitUntil(L.idle, 900, "control after the west mouth")
  L.wait(30)
  if route5 then
    expect(L.mapId() == route5, "out of the west mouth onto Route 5")
  else
    local x, y = L.pos()
    expect(L.mapId() == S.MAP_HOLLOW and x == 47 and y == 34,
           string.format("out of the west mouth (Route 5 isn't on this branch: the placeholder warp lands at %d,%d)", x, y))
  end
  L.shot("out_west")
end

L.start(function()
  L.quickstart()
  giveLead()
  setHour(12)        -- by day, whatever the host's clock says; night() comes later
  eastMouth()
  darkRoad()
  hekataion()
  roadWest()
  shortcut()
  wild()
  night()
  westMouth()
  L.log("ok the walk is done")
end)
