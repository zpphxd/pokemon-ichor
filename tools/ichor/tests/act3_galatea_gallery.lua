-- Galatea's Gallery, run by tools/ichor/tests/act3_galatea_gallery.sh (read it first).
--
-- Each room's route comes from act3_galatea_routes.lua, which
-- tools/ichor/maps/kythera_temple.py writes with its model's predictions: who
-- touches the player and when, and where every statue ends. The game is played
-- with key presses and must agree.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local R = dofile("tools/ichor/tests/act3_galatea_routes.lua")
for k, v in pairs(dofile(L.OUT .. "temple_scripts.lua")) do S.SCRIPTS[k] = v end
local expect = L.expect
local KEY = { N = K.UP, S = K.DOWN, W = K.LEFT, E = K.RIGHT }
local MOVE = { N = { 0, -1 }, S = { 0, 1 }, W = { -1, 0 }, E = { 1, 0 } }
local DIRNAME = { [1] = "south", [2] = "north", [3] = "west", [4] = "east" }

local function objectFacing(localId)
  for i = 0, S.OBJECT_EVENTS_COUNT - 1 do
    local o = S.gObjectEvents + i * S.OBJECT_EVENT_SIZE
    if emu:read8(o) & 1 == 1 and emu:read8(o + S.OFF_OBJ_LOCAL_ID) == localId then
      return emu:read8(o + 0x18) & 0xF
    end
  end
end

local function warpTo(x, y)
  L.setVar(S.VAR_0x8008, x)
  L.setVar(S.VAR_0x8009, y)
  L.runHeader("Gallery_WarpHeader")
  local px, py = L.pos()
  expect(L.mapId() == S.MAP_TEMPLE and px == x and py == y,
         string.format("into the temple at (%d,%d)", px, py))
end

-- Turn toward a neighbouring tile without stepping (a short press against an object).
local function faceToward(tx, ty)
  local x, y = L.pos()
  local key = (tx > x and K.RIGHT) or (tx < x and K.LEFT) or (ty > y and K.DOWN) or K.UP
  L.face(key)
end

-- Walk a route from the player's tile. A step the game takes over (a room's
-- trigger, a trainer, a touch) is played out. Returns the 0-based index of the
-- step after which the player was sent elsewhere (a touch), or nil.
local function play(name, route, opts)
  opts = opts or {}
  for i, a in ipairs(route.steps) do
    if a:sub(1, 1) == "t" then
      local id = S[a:sub(2)]
      local mx, my = L.objectAt(id)
      faceToward(mx, my)
      L.tap(K.A)
      L.wait(10)
      L.settle({ answers = { "yes" } })
    else
      local x, y = L.pos()
      local r = L.step(KEY[a])
      if r == "blocked" then L.shot(name .. "_blocked"); L.fail(string.format("%s: step %d (%s) from (%d,%d) is blocked", name, i - 1, a, x, y)) end
      if opts.shotAt and opts.shotAt[i - 1] then L.shot(opts.shotAt[i - 1]) end
      if r == "taken" then L.settle({ answers = opts.answers }) end
      local nx, ny = L.pos()
      if nx ~= x + MOVE[a][1] or ny ~= y + MOVE[a][2] then
        return i - 1
      end
    end
  end
end

-- Every statue of the route's room that is on screen must stand where the model says.
local function checkStatues(name, route, which)
  for id, at in pairs(route[which or "statues"]) do
    local x, y = L.objectAt(S[id])
    if x then
      expect(x == at[1] and y == at[2],
             string.format("%s: %s at (%d,%d), the model says (%d,%d)", name, id, x, y, at[1], at[2]))
    else
      L.note(string.format("%s: %s is off screen", name, id))
    end
  end
end

L.start(function()
  L.quickstart()
  L.runHeader("Gallery_GiveHeader")
  L.assistLevel100()

  -- 1. The pronaos: turning back toward S1 gets you touched --------------------------
  warpTo(5, 34)
  L.shot("pronaos_door")
  local r = R.pronaos_back
  local touchedAt = play("pronaos_back", r, { shotAt = { [r.at - 1] = "pronaos_s1_behind" } })
  L.shot("pronaos_touched_back_at_door")
  expect(touchedAt == r.at, string.format("S1 touches the player at step %s (the model: %d)", tostring(touchedAt), r.at))
  local px, py = L.pos()
  expect(px == 5 and py == 34, string.format("the touch sends the player back to the pronaos's door (%d,%d)", px, py))
  local sx, sy = L.objectAt(S.LOCALID_GALLERY_S1)
  expect(sx == 2 and sy == 29, string.format("S1 is back on its plinth (%s,%s)", tostring(sx), tostring(sy)))

  -- Charis: her welcome, then the walk-through (the safety valve), and S1 put back
  local charis = L.npc("KytheraTempleOfAphrodite_EventScript_Charis")
  L.talk(charis, { shots = { [1] = "pronaos_charis_welcome" } })
  L.talk(L.npc("KytheraTempleOfAphrodite_EventScript_Charis"), { answers = { "yes" }, shots = { [2] = "pronaos_charis_shows" } })
  sx, sy = L.objectAt(S.LOCALID_GALLERY_S1)
  expect(sx == 2 and sy == 29, string.format("after Charis's walk-through S1 is back on its plinth (%s,%s)", tostring(sx), tostring(sy)))
  local cx, cy = L.objectAt(S.LOCALID_GALLERY_CHARIS)
  expect(cx == 6 and cy == 32, string.format("Charis is back by the altar (%s,%s)", tostring(cx), tostring(cy)))
  warpTo(5, 34)

  -- 2. The pronaos the right way: up the west side facing M0, through the door -------
  r = R.pronaos
  touchedAt = play("pronaos", r, { shotAt = { [9] = "pronaos_facing_m0" } })
  expect(touchedAt == nil, "the pronaos walked facing the mirror: never touched")
  px, py = L.pos()
  expect(px == 5 and py == 22, string.format("through the door into the gallery (%d,%d)", px, py))
  L.shot("gallery_door")

  -- 3. The gallery: the west aisle facing W1, the north aisle facing W2, Rhodanthe --
  r = R.gallery
  touchedAt = play("gallery", r, { shotAt = { [9] = "gallery_west_aisle", [16] = "gallery_north_aisle" } })
  expect(touchedAt == nil, "the gallery's west way round: never touched")
  expect(L.getFlag(S.TRAINER_FLAGS_START + S.TRAINER_RHODANTHE), "Rhodanthe is beaten at the north door")
  checkStatues("gallery", r)
  L.shot("gallery_north_door")

  -- 4. The rose court: up the east lane, P2 turned, the north walk, the dais ---------
  local x0, y0 = L.pos()
  local stepIn = L.step(K.UP)
  if stepIn == "taken" then L.settle() end
  px, py = L.pos()
  expect(px == 16 and py == 12, string.format("into the rose court (%d,%d)", px, py))
  L.shot("court_door")
  r = R.court
  -- stop before the dais: the last step plays the scene, checked below
  local walk = { steps = {} }
  for i = 1, #r.steps - 1 do walk.steps[i] = r.steps[i] end
  touchedAt = play("court", walk)
  expect(touchedAt == nil, "the court's east lane and north walk: never touched")
  expect(objectFacing(S.LOCALID_GALLERY_P2) == S.DIR_SOUTH,
         string.format("P2 turned to face down the east lane (it faces %s)", DIRNAME[objectFacing(S.LOCALID_GALLERY_P2)] or "?"))
  expect(L.getFlag(S.FLAG_P2_BIT0) and not L.getFlag(S.FLAG_P2_BIT1), "P2's quarter-turn is kept in its flags")
  L.shot("court_before_dais")
  checkStatues("court", r, "before_last")

  -- the step onto the inlay: Galatea steps down; her speech, the battle, the Laurel
  local stepped = L.step(K.UP)
  local boxes, fought = L.settle({ answers = { "yes" }, every = true })
  L.shot("court_after_laurel")
  expect(L.getFlag(S.FLAG_GALLERY_DONE), "FLAG_ICHOR_GALLERY_DONE: the player reached the dais")
  expect(#fought >= 1 and fought[1].outcome == 1, "Galatea's battle is won")
  expect(L.getFlag(S.TRAINER_FLAGS_START + S.TRAINER_GALATEA), "Galatea is beaten")
  expect(L.getFlag(S.FLAG_BADGE07_GET), "the Foam Laurel: FLAG_BADGE07_GET")
  expect(L.getVar(S.VAR_ICHOR_ACT3) == 3, string.format("VAR_ICHOR_ACT3 is 3 at the Laurel (%d)", L.getVar(S.VAR_ICHOR_ACT3)))
  expect(L.getFlag(S.FLAG_CYGNUS), "Cygnus appears in the Star Chart")
  expect(L.getFlag(S.FLAG_GOT_TM), "FLAG_ICHOR_GOT_TM_DAZZLING_GLEAM")
  expect(L.getFlag(S.FLAG_FALLS_HINT), "Galatea sends the player to the falls")
  expect(L.getFlag(S.TRAINER_FLAGS_START + S.TRAINER_ANTHOUSA), "Anthousa counts as beaten after the Laurel")

  -- 5. After the Laurel: enter again; P2 still turned; the statues don't move --------
  warpTo(16, 12)
  L.wait(30)
  expect(objectFacing(S.LOCALID_GALLERY_P2) == S.DIR_SOUTH, "P2 is still turned after the temple is entered again")
  local before = { L.objectAt(S.LOCALID_GALLERY_S7) }
  for _ = 1, 3 do L.step(K.LEFT); L.step(K.RIGHT) end
  local after = { L.objectAt(S.LOCALID_GALLERY_S7) }
  expect(before[1] == after[1] and before[2] == after[2], "after the Laurel the court's statues stand still")
  L.shot("court_after_laurel_still")
end)
