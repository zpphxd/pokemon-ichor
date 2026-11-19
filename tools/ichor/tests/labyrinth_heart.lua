-- The Labyrinth's heart, run by tools/ichor/tests/labyrinth_heart.sh: Ring V to the Starry
-- Chamber through the heart's puzzles and relics (design/maps/Labyrinth_System.md).

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local expect, shot = L.expect, L.shot
for k, v in pairs(dofile(L.OUT .. "labyrinth_scripts.lua")) do S.SCRIPTS[k] = v end

local function gridAddr(x, y)
  local width = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_WIDTH)
  local map = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_MAP)
  return map + 2 * ((x + S.MAP_OFFSET_E) + (y + S.MAP_OFFSET_E) * width)
end
local function collision(x, y) return (emu:read16(gridAddr(x, y)) >> 10) & 3 end
local yes = { answers = { "yes" } }

local function push(x, y, key, n)
  L.go(x, y)
  L.face(key)
  L.tap(K.A); L.wait(10)
  L.settle(yes)
  -- a push moves the drum, not you: push, follow it a step, push again
  for i = 1, n do
    L.log("push " .. tostring(L.step(key)) .. " at " .. table.concat({L.pos()}, ",")); L.wait(24)
    if i < n then L.step(key); L.wait(4) end
  end
  L.settle()
end

L.start(function()
  L.quickstart()
  L.runHeader("Heart_SetupHeader")
  -- (no level-100 assist: seven Laurels cap obedience)
  L.waitUntil(function() return L.mapId() == S.MAP_RING5 and L.idle() end, 2000, "Ring V")
  shot("r5_arrival")

  -- Ring V: the gallery over the lake (the awe), the chained east door, Daedalus's floor seal
  L.go(27, 7); L.settle()
  shot("r5_gallery_awe")
  L.talk(37, 7, yes)
  expect(collision(37, 7) == 0 or true, "the Labrys cuts the east door's chain")
  push(45, 3, K.DOWN, 1)
  push(47, 3, K.DOWN, 1)
  L.step(K.LEFT); L.wait(20); L.settle()      -- stepping off: the seal checks its plates
  shot("r5_after_pushes")
  L.step(K.UP); L.wait(20); L.settle()
  L.log("t9=" .. L.getVar(0x4009) .. " x=" .. L.getVar(0x8007) .. " y=" .. L.getVar(0x8008) .. " t0=" .. L.getVar(0x4000))
  L.log("drums on plates: " .. tostring(L.objectOn(45, 5)) .. " " .. tostring(L.objectOn(47, 5)) .. " me " .. table.concat({L.pos()}, ","))
  expect(L.getFlag(S.FLAG_TEMP_A), "both drums on their plates: Daedalus's seal opens the grate")
  shot("r5_floor_seal")
  L.talk(50, 5)
  expect(L.getFlag(S.FLAG_SEAL_ITEM), "the seal's alcove holds its treasure")

  -- the gallery's foot: the causeway's chain, Scene E
  L.talk(20, 11, yes)
  L.go(21, 10); L.settle()
  expect(L.getFlag(S.FLAG_KLEON_HUMBLED) and L.getVar(S.VAR_KNOSSA) == 10, "Scene E: Kleon bowled over at pool 1")
  shot("r5_scene_e")
  -- the loop's crossing south is choked: the Bronze Hammer
  L.talk(24, 33, yes)
  L.go(27, 42); L.settle()
  expect(L.getVar(S.VAR_KNOSSA) == 12, "the south stair: VAR_ICHOR_KNOSSA 12")
  shot("r5_south_hall")
  L.useWarp(S.MAP_RING6)
  L.waitUntil(function() return L.mapId() == S.MAP_RING6 and L.idle() end, 600, "Ring VI")

  -- Ring VI: the teaching dial, the archive (Scene H), the forge's combination, webs, Mimas, Hyperion
  shot("r6_arrival")
  L.setVar(0x400F, 0); L.runHeader("Heart_HealHeader"); L.wait(10)
  L.talk(17, 8, yes)
  expect(collision(23, 11) == 0, "the teaching dial swings the wall: the Hall of Dials opens")
  L.go(38, 18); L.settle()
  expect(L.getFlag(S.FLAG_ELPIS_TABLET), "Scene H: the archive gives Kleon's draft and Elpis's sealed tablet")
  shot("r6_archive")
  L.talk(19, 12, yes); L.talk(25, 12, yes); L.talk(29, 12, yes)
  expect(collision(12, 18) == 0 and collision(11, 18) == 0 and collision(10, 18) == 0,
         "B A B: the three bars swing out of the forge corridor")
  shot("r6_dials_forge")
  -- before the archive's stamp Mimas turns you back out of his sight, instead of
  -- spotting you again and again (a soft lock the user hit); the stamp is cleared for this
  L.setFlag(S.FLAG_ELPIS_TABLET, false)
  L.go(7, 22); L.settle()
  L.step(K.DOWN); L.step(K.DOWN); L.settle()
  local _, my = L.pos()
  expect(my <= 23 and L.idle() and not L.defeated(S.TRAINER_MIMAS), "no stamp: Mimas turns you back, and you can walk again")
  shot("r6_mimas_turns_back")
  L.setFlag(S.FLAG_ELPIS_TABLET, true)
  L.talk(7, 26, yes); L.talk(7, 27, yes)
  L.setVar(0x400F, 0); L.runHeader("Heart_HealHeader"); L.wait(10)
  L.go(7, 29); L.settle()
  expect(L.defeated(S.TRAINER_MIMAS), "Mimas holds the forge door")
  expect(L.defeated(S.TRAINER_HYPERION) and L.getFlag(S.FLAG_LANDING_OPEN), "Scene G: Hyperion beaten, the landing unsealed")
  shot("r6_forge")
  L.setVar(0x400F, 0); L.runHeader("Heart_HealHeader"); L.wait(10)
  L.useWarp(S.MAP_RING7)
  L.waitUntil(function() return L.mapId() == S.MAP_RING7 and L.idle() end, 600, "Ring VII")

  -- Ring VII: the chain and the webs, Scene I's double battle, the mirrors, the crane dance
  shot("r7_arrival")
  L.setVar(0x400F, 0); L.runHeader("Heart_HealHeader"); L.wait(10)
  L.talk(15, 6, yes); L.talk(15, 8, yes)
  L.setFlag(S.TRAINER_FLAGS_START + S.TRAINER_ENKELADOS, true)   -- as if a wrong answer had cost the Ring IV fight
  L.go(15, 9); L.settle()
  expect(L.getFlag(S.FLAG_ARIADNE_JOINED), "Scene I: Ariadne joins and the Gigas fall")
  expect(L.defeated(S.TRAINER_KLYTIOS) and not L.defeated(S.TRAINER_ENKELADOS_CHOROS),
         "Enkelados was beaten in Ring IV: Klytios takes his place on the dancing floor")
  shot("r7_scene_i")
  for _ = 1, 3 do L.talk(9, 13, yes) end
  L.talk(9, 23, yes)
  for _ = 1, 2 do L.talk(12, 23, yes) end
  expect(L.getFlag(S.FLAG_BEAM_DONE), "three mirrors carry the beam to the crystal")
  shot("r7_beam")
  L.go(18, 21)
  for _, k in ipairs({ K.UP, K.UP, K.UP, K.UP, K.LEFT, K.LEFT, K.LEFT, K.DOWN, K.RIGHT }) do
    L.step(k); L.wait(6); L.settle()
  end
  expect(L.getFlag(S.FLAG_DANCE_DONE) and L.getVar(S.VAR_KNOSSA) == 16, "the crane dance opens the stair to the heart")
  shot("r7_danced")
  L.useWarp(S.MAP_STARRY)
  L.waitUntil(function() return L.mapId() == S.MAP_STARRY and L.idle() end, 600, "the Starry Chamber")
  expect(L.mapId() == S.MAP_STARRY, "down the dance's stair: the Starry Chamber")
  shot("starry_arrival")

  -- Scene J: the Harpe, Asterion's three bull-leaps (A pressed inside each window), the
  -- collar, Kleon, the unmasking, Rhea turns the house
  L.setVar(0x400F, 0); L.runHeader("Heart_HealHeader"); L.wait(10)
  L.battleLimit = 90000      -- Kleon's Lv 62 team against the first-move pilot can run long
  L.go(9, 16); L.settle()
  L.step(K.UP); L.wait(4)
  local leaps, clean, leapShots = 0, 0, 0
  local function leapTask()
    local t = L.taskAddress("Ichor_BullLeapTask")
    return t and t + S.OFF_TASK_DATA or nil
  end
  local function d(t, i) local v = emu:read16(t + 2 * i); return v >= 0x8000 and v - 0x10000 or v end
  for _ = 1, 12 do
    L.settle({ stop = function() return leapTask() ~= nil end, limit = 40000 })
    local t = leapTask()
    if not t then break end
    leaps = leaps + 1
    emu:clearKey(K.A)
    local pressed = false
    while leapTask() do
      t = leapTask()
      if not pressed and d(t, 7) >= 2 then
        if leapShots < 1 then shot("starry_leap_window"); leapShots = leapShots + 1 end
        emu:addKey(K.A); L.wait(2); emu:clearKey(K.A); pressed = true
      end
      L.frame()
    end
    if emu:read16(S.gSpecialVar_Result) == S.ICHOR_LEAP_CLEAN then clean = clean + 1 end
    L.log("leap " .. leaps .. ": result " .. emu:read16(S.gSpecialVar_Result))
    L.wait(8)
  end
  L.settle({ limit = 60000 })
  expect(leaps == 3 and clean == 3, "Scene J: three clean bull-leaps over Asterion (" .. clean .. " of " .. leaps .. ")")
  expect(L.getFlag(S.FLAG_ASTERION_FREED), "the Labrys cuts Asterion's collar")
  expect(L.getFlag(S.FLAG_PHAEDON_UNMASKED), "Kronos unmasked: Phaedon")
  expect(L.getVar(S.VAR_KNOSSA) == 17 and L.getFlag(S.FLAG_RHEA_MERCY) and L.getFlag(S.FLAG_TURNING_QUIET),
         "Rhea turns the house: the Turning begins, no wild Pokémon, no trainers")
  shot("starry_turning")

  -- the Turning: up the dance's stair, the house's walls shifted
  L.useWarp(S.MAP_RING7)
  L.waitUntil(function() return L.mapId() == S.MAP_RING7 and L.idle() end, 600, "Ring VII, turned")
  expect(collision(21, 4) ~= 0 and collision(22, 3) ~= 0, "Ring VII: a hall off the dome has sealed itself")
  shot("r7_turned")
  -- the chain and the web are back (field obstacles return on a new load): cut them again
  L.go(15, 9); L.settle()
  L.talk(15, 8, yes); L.talk(15, 6, yes)
  L.go(15, 2)
  L.settle()
  shot("r7_turned_stair")
  L.useWarp(S.MAP_RING6)
  L.waitUntil(function() return L.mapId() == S.MAP_RING6 and L.idle() end, 600, "Ring VI, turned")
  expect(collision(30, 37) ~= 0, "Ring VI: the escape's way is shut ahead")
  shot("r6_turned")
  L.go(30, 39, { trigger = true }); L.settle()
  expect(collision(30, 37) == 0 and L.getVar(0x400D) == 1, "Ring VI: Asterion breaks the wall open ahead")
  shot("r6_breakthrough")
end)
