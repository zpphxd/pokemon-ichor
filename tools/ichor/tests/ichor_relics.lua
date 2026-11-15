-- Relics check, run by tools/ichor/tests/ichor_relics.sh (read it first).
--
-- The arena is Route 1's open patch around (11,47). Obstacles are spawned by
-- rewriting one of Route 1's object templates in RAM; water, waterfalls and deep
-- water are written into the live map grid; a dive connection and the dark-map
-- bit are written into the RAM map header. Nothing in the ROM is patched.
--
--   1. No Pokémon offers a field move, though one knows Cut and Surf.
--   2. Each relic flag is set as its item enters the bag (the Talaria's is FLAG_SYS_B_DASH).
--   3. Every obstacle refuses without its relic, asks with it, and clears: the thicket,
--      rubble, the column drum (then a push), cobweb, thornweb and great boulder
--      (refused without the upgrade first), and the labrys seal. AUTO acts without
--      asking; a map that forbids relics refuses.
--   4. Darkness: the light radius from no torch, the Torch, its upgrade, Hecate's
--      blessing, and dousing.
--   5. The Relic Ring: SELECT, a registered item run from it, the Helm, the cursor
--      memory, the torch doused and relit, and the Wings' fly map, cancelled.
--   6. Water: the Conch (Surf), the Horn (Waterfall) and the Pearl (Dive), each
--      refused without it.
--   7. Aeolus's Bag clears fog.
--   8. The bag's Key Items pocket and the option row, photographed.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local log, expect, wait, shot, tap, settle = L.log, L.expect, L.wait, L.shot, L.tap, L.settle

local PX, PY = 11, 47           -- where the player stands, facing north
local OX, OY = 11, 46           -- where obstacles stand
local TEMPLATE = 3              -- Route 1's object template we rewrite (the shepherd)
local tplLocalId

local function relicFlag(item) return S.FLAG_ICHOR_RELICS_START + (item - S.ICHOR_RELIC_FIRST) end

local function give(item)
  L.setVar(S.VAR_0x8004, item)
  L.runHeader("RelicTest_GiveHeader")
end

local function warpHome()
  L.setVar(S.VAR_0x8008, PX); L.setVar(S.VAR_0x8009, PY)
  L.runHeader("RelicTest_WarpHeader", { limit = 4000 })
  L.waitUntil(function() local x, y = L.pos() return x == PX and y == PY and L.idle() end, 3000, "the warp home")
  wait(40)
  L.face(K.UP)
end

-- Rewrite template TEMPLATE as an obstacle at (OX, OY) and spawn it.
local function spawn(gfx, script)
  local t = L.sb1() + S.OFF_SB1_TEMPLATES + TEMPLATE * S.TEMPLATE_SIZE
  tplLocalId = emu:read8(t + S.OFF_TPL_LOCAL_ID)
  -- the template is packed: graphicsId sits at an odd offset, so write it a byte at a time
  emu:write8(t + S.OFF_TPL_GFX, gfx & 0xFF)
  emu:write8(t + S.OFF_TPL_GFX + 1, gfx >> 8)
  emu:write16(t + S.OFF_TPL_X, OX)
  emu:write16(t + S.OFF_TPL_Y, OY)
  emu:write8(t + S.OFF_TPL_ELEVATION, 3)
  emu:write8(t + S.OFF_TPL_MOVEMENT, S.MOVEMENT_TYPE_FACE_DOWN)
  emu:write16(t + S.OFF_TPL_TRAINER_TYPE, 0)        -- not a trainer
  emu:write16(t + S.OFF_TPL_TRAINER_TYPE + 2, 0)
  emu:write32(t + S.OFF_TPL_SCRIPT, script)
  emu:write16(t + S.OFF_TPL_FLAG, 0)
  L.setVar(S.VAR_0x8008, tplLocalId)
  L.runHeader("RelicTest_SpawnHeader")
  wait(10)
  local x, y = L.objectAt(tplLocalId)
  expect(x == OX and y == OY, string.format("an obstacle stands at (%d,%d)", OX, OY))
end
local function present() return L.objectAt(tplLocalId) ~= nil end

-- Page through any boxes until a YES/NO; answer it (YES unless opts.no) and
-- photograph the pose. Returns whether a YES/NO was asked.
local function answer(prefix, opts)
  opts = opts or {}
  local asked = false
  local t0 = L.now()
  local pages = 0
  while L.now() - t0 < 900 do
    if L.taskRunning("Task_HandleYesNoInput") then asked = true break end
    if L.idle() and L.now() - t0 > 60 then break end
    if L.boxUp() then
      wait(40)
      if L.taskRunning("Task_HandleYesNoInput") then asked = true break end
      pages = pages + 1
      shot(string.format("%s_text%d", prefix, pages)); tap(K.A)
    end
    L.frame()
  end
  if asked then
    wait(10); shot(prefix .. "_ask")
    if opts.no then tap(K.DOWN) end
    tap(K.A)
    if os.getenv("POSEBURST") then
      for k = 1, 12 do wait(8); shot(string.format("%s_burst%02d", prefix, k)) end
    else
      wait(opts.poseAt or 50); shot(prefix .. "_pose")
    end
  end
  settle()
  return asked
end

-- Talk to what's in front, then answer.
local function interact(prefix, opts)
  L.face(K.UP)
  tap(K.A)
  return answer(prefix, opts)
end

-- Load the obstacle's script address from the engine symbols.
local function sym(name)
  local a = S[name]
  if not a then L.fail("no symbol " .. name) end
  return a
end

-- --- The map grid -----------------------------------------------------------------

local function setMetatile(x, y, id, elevation, collision)
  local w = emu:read32(S.gBackupMapLayout + S.OFF_LAYOUT_WIDTH)
  local map = emu:read32(S.gBackupMapLayout + S.OFF_LAYOUT_MAP)
  local a = map + 2 * ((x + S.MAP_OFFSET) + w * (y + S.MAP_OFFSET))
  emu:write16(a, (elevation << 12) | ((collision or 0) << 10) | id)
end
local OCEAN, WATERFALL, DEEP = 44, 76, 334   -- aethos primary metatiles (MB_OCEAN_WATER, MB_WATERFALL, MB_DEEP_WATER)

local function redraw()
  -- Opening and closing the start menu redraws the field from the grid.
  tap(K.START); wait(30); tap(K.B); wait(40)
end

local function surfing() return emu:read8(S.gPlayerAvatar + S.OFF_AVATAR_FLAGS) & S.PLAYER_AVATAR_FLAG_SURFING ~= 0 end
local function flashLevel() return emu:read8(L.sb1() + S.OFF_SB1_FLASH_LEVEL) end
local function setCave(on)
  local a = S.gMapHeader + S.OFF_MAPHEADER_FLAGS_BYTE
  local b = emu:read8(a)
  if on then b = b | (1 << S.MAPHEADER_CAVE_BIT) else b = b & ~(1 << S.MAPHEADER_CAVE_BIT) end
  emu:write8(a, b)
end
local function flashIs(want, what)
  L.runHeader("RelicTest_FlashHeader")
  expect(flashLevel() == want, string.format("%s: light level %d (want %d)", what, flashLevel(), want))
end

-- START, BAG: open the bag and leave it. Coming back re-creates the field, with
-- the darkness of the current light level.
local function startMenuTo(action)
  tap(K.START); wait(30)
  local n = emu:read8(S.sNumStartMenuActions)
  local index
  for i = 0, n - 1 do if emu:read8(S.sCurrentStartMenuActions + i) == action then index = i end end
  if not index then L.fail("no start menu action " .. action) end
  local cur = emu:read8(S.sStartMenuCursorPos)
  for _ = 1, (index - cur) % n do tap(K.DOWN); wait(4) end
  tap(K.A)
end
local MENU_ACTION_BAG, MENU_ACTION_OPTION = 2, 6
local function bagAndBack(shots)
  startMenuTo(MENU_ACTION_BAG)
  L.waitUntil(function() return L.on("CB2_Bag") end, 600, "the bag")
  wait(60)
  for p = 1, shots or 0 do
    shot(string.format("bag_pocket_%d", p))
    tap(K.RIGHT); wait(40)
  end
  tap(K.B)
  L.waitUntil(function() return L.taskRunning("Task_ShowStartMenu") or L.inOverworld() end, 600, "the field again")
  wait(30)
  if not L.idle() then tap(K.B); wait(30) end
  L.waitUntil(L.idle, 600, "the field after the bag")
end

-- Open the Relic Ring with SELECT and return when its menu is up.
local function openRing(name)
  tap(K.SELECT)
  L.waitUntil(function() return L.taskRunning("Task_HandleScrollingMultichoiceInput") or L.taskRunning("Task_HandleMultichoiceInput") end,
              240, "the Relic Ring")
  wait(20)
  shot(name)
end

L.start(function()
  L.quickstart()
  L.setVar(S.VAR_0x8008, PX); L.setVar(S.VAR_0x8009, PY)
  L.runHeader("RelicTest_SetupHeader", { limit = 4000 })
  L.waitUntil(function() return L.mapId() == S.MAP_ROUTE1 and L.idle() end, 3000, "Route 1")
  wait(60)
  L.face(K.UP)
  shot("arena")

  -- 1. No field moves from Pokémon
  L.runHeader("RelicTest_FieldMovesHeader")
  expect(L.getVar(S.VAR_0x8000) == 3, string.format("Cut and Surf are locked for Pokémon, though one knows both (%d of 3 checks)", L.getVar(S.VAR_0x8000)))

  -- 2. Relic flags follow the bag
  give(S.ITEM_TALARIA)
  expect(L.getFlag(S.FLAG_SYS_B_DASH), "the Talaria in the bag sets FLAG_SYS_B_DASH, its relic flag")

  -- 4a. Darkness without the Torch
  setCave(true)
  flashIs(S.ICHOR_FLASH_NO_TORCH, "a dark map without the Torch")
  setCave(false)
  L.runHeader("RelicTest_FlashHeader")

  -- 3. Obstacles
  local obstacles = {
    { name = "thicket", gfx = S.GFX_CUTTABLE_TREE, script = "EventScript_CutTree", relic = S.ITEM_DEMETERS_SICKLE },
    { name = "rubble", gfx = S.GFX_BREAKABLE_ROCK, script = "EventScript_RockSmash", relic = S.ITEM_BRONZE_HAMMER },
    { name = "cobweb", gfx = S.GFX_BREAKABLE_ROCK, script = "EventScript_IchorCobweb", relic = S.ITEM_HECATES_TORCH },
    { name = "thornweb", gfx = S.GFX_BREAKABLE_ROCK, script = "EventScript_IchorThornweb", relic = S.ITEM_HECATES_TORCH,
      upgrade = S.FLAG_ICHOR_THREE_FLAMED_TORCH },
    { name = "great_boulder", gfx = S.GFX_PUSHABLE_BOULDER, script = "EventScript_IchorGreatBoulder", relic = S.ITEM_BRONZE_HAMMER,
      upgrade = S.FLAG_ICHOR_HEPHAESTUS_HAMMER },
    { name = "labrys_seal", gfx = S.GFX_BREAKABLE_ROCK, script = "EventScript_IchorLabrysSeal", relic = S.ITEM_LABRYS },
  }
  for _, o in ipairs(obstacles) do
    spawn(o.gfx, sym(o.script))
    if not L.getFlag(relicFlag(o.relic)) then
      local asked = interact(o.name .. "_without")
      expect(not asked and present(), o.name .. ": without the relic it stays, and nothing asks")
      give(o.relic)
      expect(L.getFlag(relicFlag(o.relic)), o.name .. ": the relic's flag is set as it enters the bag")
    end
    if o.upgrade then
      local asked = interact(o.name .. "_weak")
      expect(not asked and present(), o.name .. ": without the upgrade it stays")
      L.setFlag(o.upgrade, true)
    end
    local asked = interact(o.name)
    expect(asked and not present(), o.name .. ": asks, then clears")
  end

  for _, o in ipairs(obstacles) do if o.upgrade then L.setFlag(o.upgrade, false) end end

  -- NO answers keep it
  spawn(S.GFX_CUTTABLE_TREE, sym("EventScript_CutTree"))
  interact("thicket_no", { no = true })
  expect(present(), "answering NO leaves the thicket")

  -- AUTO acts without asking
  local opt = L.ichor() + S.OFF_ICHOR_OPTIONS
  emu:write8(opt, emu:read8(opt) | S.ICHOR_OPTION_RELIC_AUTO)
  local asked = interact("thicket_auto")
  expect(not asked and not present(), "AUTO cuts the thicket without a question")
  emu:write8(opt, emu:read8(opt) & ~S.ICHOR_OPTION_RELIC_AUTO)

  -- A trial that forbids outside tools; a map change lifts it
  spawn(S.GFX_BREAKABLE_ROCK, sym("EventScript_RockSmash"))
  L.setFlag(S.FLAG_ICHOR_NO_RELICS, true)
  interact("forbidden")
  expect(present(), "FLAG_ICHOR_NO_RELICS keeps the rubble")
  warpHome()
  expect(not L.getFlag(S.FLAG_ICHOR_NO_RELICS), "a map change clears FLAG_ICHOR_NO_RELICS")

  -- The column drum: brace, then push
  spawn(S.GFX_PUSHABLE_BOULDER, sym("EventScript_StrengthBoulder"))
  interact("drum_without")
  give(S.ITEM_GIRDLE_OF_HERAKLES)
  interact("drum")
  expect(L.getFlag(S.FLAG_SYS_USE_STRENGTH), "the Girdle braces: FLAG_SYS_USE_STRENGTH")
  L.step(K.UP)
  wait(40)
  local dx, dy = L.objectAt(tplLocalId)
  expect(dx == OX and dy == OY - 1, string.format("the player pushes the drum north (now at %s,%s)", tostring(dx), tostring(dy)))
  shot("drum_pushed")
  warpHome()

  -- 4b. Darkness with the Torch
  setCave(true)
  flashIs(S.ICHOR_FLASH_TORCH, "the Torch")
  L.setFlag(S.FLAG_ICHOR_THREE_FLAMED_TORCH, true)
  flashIs(S.ICHOR_FLASH_TORCH_STRONG, "the Three-Flamed Torch")
  emu:write8(L.ichor() + S.OFF_ICHOR_BLESSING_GOD, S.ICHOR_GOD_HECATE)
  emu:write16(L.ichor() + S.OFF_ICHOR_BLESSING_STEPS, 100)
  flashIs(S.ICHOR_FLASH_TORCH_BOTH, "the Three-Flamed Torch and Hecate's blessing")
  emu:write8(L.ichor() + S.OFF_ICHOR_BLESSING_GOD, 0)
  emu:write16(L.ichor() + S.OFF_ICHOR_BLESSING_STEPS, 0)
  L.setFlag(S.FLAG_ICHOR_THREE_FLAMED_TORCH, false)
  flashIs(S.ICHOR_FLASH_TORCH, "back to the plain Torch")
  shot("dark_torch")

  -- 5. The Relic Ring. Owning the Wings opens it; the Hammer is registered.
  give(S.ITEM_DAEDALUS_WINGS)
  emu:write16(L.sb1() + S.OFF_SB1_REGISTERED_ITEM, S.ITEM_BRONZE_HAMMER)
  bagAndBack()                          -- the field comes back dark, lit by the Torch
  shot("dark_field")
  openRing("ring_douse")
  -- entries: BRONZE HAMMER, FLY, DOUSE TORCH, ...; douse the torch
  tap(K.DOWN); wait(8); tap(K.DOWN); wait(10)
  tap(K.A)
  settle()
  L.waitUntil(function() return flashLevel() == S.ICHOR_FLASH_DOUSED and L.idle() end, 400, "the torch to go out")
  expect(L.getFlag(S.FLAG_ICHOR_TORCH_DOUSED), "the Ring douses the torch: the map goes dark")
  shot("doused")
  openRing("ring_light")
  tap(K.A)                              -- the cursor stays on the torch: LIGHT TORCH
  settle()
  L.waitUntil(function() return flashLevel() == S.ICHOR_FLASH_TORCH and L.idle() end, 400, "the torch to light")
  expect(not L.getFlag(S.FLAG_ICHOR_TORCH_DOUSED), "... and lights it again, on the same entry")
  setCave(false)
  L.runHeader("RelicTest_FlashHeader")
  bagAndBack()

  -- The registered Hammer, run from the Ring, breaks rubble in front
  spawn(S.GFX_BREAKABLE_ROCK, sym("EventScript_RockSmash"))
  openRing("ring_registered")
  tap(K.UP); wait(8); tap(K.UP); wait(10)       -- from the torch up to BRONZE HAMMER
  shot("ring_registered_cursor")
  tap(K.A)
  local askedR = answer("ring_registered")
  expect(askedR and not present(), "the Ring runs the registered Bronze Hammer on the rubble in front")

  -- The Helm, and the Ring remembering it
  give(S.ITEM_HELM_OF_DARKNESS)
  openRing("ring_helm")
  tap(K.DOWN); tap(K.DOWN); wait(8); tap(K.DOWN); wait(10)   -- BRONZE HAMMER, FLY, DOUSE TORCH, WEAR HELM
  tap(K.A)
  settle()
  expect(L.getFlag(S.FLAG_ICHOR_HELM_ON), "the Ring puts the Helm of Darkness on")
  local want = S.ITEM_HELM_OF_DARKNESS - S.ICHOR_RELIC_FIRST + 1
  expect(emu:read8(L.ichor() + S.OFF_ICHOR_RING_CURSOR) == want, "the Ring remembers the Helm as its last entry")
  openRing("ring_cursor_on_helm")
  tap(K.A)                              -- the cursor starts on REMOVE HELM
  settle()
  expect(not L.getFlag(S.FLAG_ICHOR_HELM_ON), "... so SELECT, A takes it off again")

  -- The Wings: the fly map, cancelled, back to the field
  openRing("ring_fly")
  tap(K.UP); wait(8); tap(K.UP); wait(10)       -- from the Helm up to FLY
  shot("ring_fly_cursor")
  tap(K.A)
  L.waitUntil(function() return L.on("CB2_FlyMap") end, 600, "the fly map")
  wait(60)
  shot("fly_map")
  tap(K.B)
  L.waitUntil(function() return L.idle() end, 900, "the field after cancelling the fly map")
  local fx, fy = L.pos()
  expect(L.inOverworld() and L.mapId() == S.MAP_ROUTE1 and fx == PX and fy == PY,
         string.format("cancelling the Wings' fly map goes back to the field, where the player stood (%d,%d)", fx, fy))
  wait(30)
  warpHome()

  -- 6. Water. Ocean in front, a two-tile waterfall, then deep water.
  setMetatile(OX, OY, OCEAN, 1)
  setMetatile(OX, OY - 1, WATERFALL, 1)
  setMetatile(OX, OY - 2, WATERFALL, 1)
  setMetatile(OX, OY - 3, DEEP, 1)
  redraw()
  L.face(K.UP)
  shot("water_grid")
  tap(K.A); wait(60)
  expect(not surfing() and L.idle(), "without the Conch the water does nothing")
  give(S.ITEM_POSEIDONS_CONCH)
  local asked = interact("surf", { poseAt = 30 })
  expect(asked and surfing(), "Poseidon's Conch: the player rides the water")
  wait(30)
  local x, y = L.pos()
  expect(x == OX and y == OY, string.format("... onto the water at (%d,%d)", x, y))
  shot("surfing")
  interact("waterfall_without")
  x, y = L.pos()
  expect(y == OY, "without the Horn the waterfall can't be climbed")
  give(S.ITEM_HORN_OF_ACHELOUS)
  interact("waterfall", { poseAt = 40 })
  L.waitUntil(function() local _, yy = L.pos() return yy == OY - 3 and L.idle() end, 900, "the climb")
  expect(surfing(), "the Horn of Achelous climbs the waterfall, still riding")
  shot("waterfall_top")
  -- Dive: a dive connection back to Route 1, written into the RAM header
  local conns = emu:read32(S.gMapHeader + S.OFF_MAPHEADER_CONNECTIONS)
  local n = conns ~= 0 and emu:read32(conns) or 0
  local old = n > 0 and emu:read32(conns + 4) or 0
  local scratch = 0x0203FC00
  for i = 0, n * S.CONNECTION_SIZE - 1 do emu:write8(scratch + 16 + i, emu:read8(old + i)) end
  local c = scratch + 16 + n * S.CONNECTION_SIZE
  emu:write8(c + S.OFF_CONN_DIRECTION, S.CONNECTION_DIVE)
  emu:write32(c + S.OFF_CONN_OFFSET, 0)
  emu:write8(c + S.OFF_CONN_GROUP, S.MAP_ROUTE1 >> 8)
  emu:write8(c + S.OFF_CONN_NUM, S.MAP_ROUTE1 & 0xFF)
  emu:write32(scratch, n + 1)
  emu:write32(scratch + 4, scratch + 16)
  emu:write32(S.gMapHeader + S.OFF_MAPHEADER_CONNECTIONS, scratch)
  tap(K.A); wait(60)
  expect(L.idle() and surfing(), "without the Nereid Pearl deep water does nothing")
  give(S.ITEM_NEREID_PEARL)
  tap(K.A)
  local dived = answer("dive", { poseAt = 40 })
  L.waitUntil(L.idle, 3000, "the field after the dive")
  expect(dived, "the Nereid Pearl asks before diving")
  expect(L.mapId() == S.MAP_ROUTE1, "the Nereid Pearl dives through the map's dive connection")
  warpHome()

  -- 7. Aeolus's Bag
  give(S.ITEM_AEOLUS_BAG)
  L.runHeader("RelicTest_FogHeader")
  wait(180)
  shot("fog")
  emu:write16(L.sb1() + S.OFF_SB1_REGISTERED_ITEM, S.ITEM_AEOLUS_BAG)
  openRing("ring_bag")
  for _ = 1, 4 do tap(K.UP); wait(8) end  -- to the top: the registered bag
  tap(K.A)
  settle()
  wait(120)
  expect(emu:read8(S.gWeather + S.OFF_WEATHER_CURR) == S.WEATHER_NONE, "Aeolus's Bag blows the fog away")
  shot("fog_gone")

  -- 8. The bag's Key Items, and the option row
  give(S.ITEM_ARIADNES_THREAD)
  bagAndBack(6)
  startMenuTo(MENU_ACTION_OPTION)
  L.waitUntil(function() return L.taskRunning("Task_OptionMenuProcessInput") end, 600, "the option menu")
  wait(30)
  for _ = 1, 6 do tap(K.DOWN); wait(4) end
  shot("options_relic_prompts")
  tap(K.RIGHT); wait(10)
  shot("options_auto")
  tap(K.B)
  L.waitUntil(function() return not L.taskRunning("Task_OptionMenuProcessInput") end, 600, "the option menu to close")
  expect(emu:read8(L.ichor() + S.OFF_ICHOR_OPTIONS) & S.ICHOR_OPTION_RELIC_AUTO ~= 0, "the option row saves AUTO")
end)
