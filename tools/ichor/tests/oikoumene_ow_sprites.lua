-- Oikoumene overworld sprites check, run by tools/ichor/tests/oikoumene_ow_sprites.sh (read it first).
--
--   1. A lead Pokémon, then Akti by the Agora, with Akti's own people cleared,
--      so the player and the follower stand alone.
--   2. For each land (the Troad, Egypt, the Black Sea): every walker spawns
--      from its graphics id in two rows round the player, then
--      * the land's walkers share one OBJ palette slot, it holds exactly
--        ichor_<land>.pal, and it is neither the player's slot nor the
--        follower's, whose colours are untouched;
--      * all walk a square, two tiles each way (left, down, right, up),
--        showing the walk frames of each direction (7/8, 3/4, 7/8 mirrored,
--        5/6), and end where they began;
--      * screenshots standing and mid-step each way; then they're removed.
--   3. Four of each land at once: three palettes in three different slots,
--      none of them the player's or the follower's.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, emu = L.S, L.emu
local expect, shot, log = L.expect, L.shot, L.log
for k, v in pairs(dofile(L.OUT .. "oikow_symbols.lua")) do S[k] = v end

local FIRST_ID = 0x40
local PX, PY = 9, 21                       -- the player's tile on Akti
local SPOTS = {}                           -- two rows of six, two tiles apart
for _, y in ipairs({ 18, 23 }) do
  for _, x in ipairs({ 4, 6, 8, 10, 12, 14 }) do SPOTS[#SPOTS + 1] = { x, y } end
end

local LANDS = {
  { tag = "troad", file = "ichor_troad.pal", first = S.GFX_FIRST, names = {
      "hero_lampkeeper", "priam", "cassandra", "hektor", "odysseus", "trojan_m", "trojan_f",
      "trojan_hoplite", "charioteer", "shepherd_ida" } },
  { tag = "kemet", file = "ichor_kemet.pal", first = S.GFX_FIRST_KEMET, names = {
      "proteus", "helen", "egyptian_m", "egyptian_f", "sun_priest", "scribe", "embalmer",
      "nile_boatman", "phoenician" } },
  { tag = "pontos", file = "ichor_pontos.pal", first = S.GFX_FIRST_PONTOS, names = {
      "aietes", "medea", "phineus", "colchian_m", "colchian_f", "argonaut", "sorceress",
      "chalybes_smith" } },
}

-- A JASC palette as the 16 BGR555 words the game loads.
local function palWords(file)
  local words, n = {}, 0
  for line in io.lines("graphics/object_events/palettes/" .. file) do
    local r, g, b = line:match("^(%d+) (%d+) (%d+)%s*$")
    if r then
      n = n + 1
      words[n] = (tonumber(r) >> 3) | ((tonumber(g) >> 3) << 5) | ((tonumber(b) >> 3) << 10)
    end
  end
  return words
end
-- The 16 colours of OBJ palette slot n, as loaded (before weather and time tint).
local function slotWords(n)
  local t = {}
  for i = 0, 15 do t[i + 1] = emu:read16(S.gPlttBufferUnfaded + 2 * (256 + n * 16 + i)) end
  return t
end
local function sameColours(a, b)        -- colour 0 is transparent and not compared
  for i = 2, 16 do if a[i] ~= b[i] then return false end end
  return true
end

local function object(localId)
  for i = 0, S.OBJECT_EVENTS_COUNT - 1 do
    local o = S.gObjectEvents + i * S.OBJECT_EVENT_SIZE
    if emu:read8(o) & 1 == 1 and emu:read8(o + S.OFF_OBJ_LOCAL_ID) == localId then return o end
  end
end
local function sprite(o) return S.gSprites + emu:read8(o + S.OFF_OBJ_SPRITE_ID) * S.SPRITE_SIZE end
local function palSlot(o) return (emu:read16(sprite(o) + 4) >> 12) & 0xF end   -- oam attr2
local function hflip(o) return (emu:read16(sprite(o) + 2) >> 12) & 1 end       -- oam attr1
-- The sheet frame the sprite shows: anims[animNum][animCmdIndex].imageValue
local function shown(o)
  local s = sprite(o)
  local num, cmd = emu:read8(s + S.OFF_SPRITE_ANIM_NUM), emu:read8(s + S.OFF_SPRITE_ANIM_CMD)
  local seq = emu:read32(emu:read32(s + S.OFF_SPRITE_ANIMS) + num * 4)
  return emu:read16(seq + cmd * 4)
end
local function coords(o)
  local c = o + S.OFF_OBJ_CURRENT_COORDS
  return emu:read16(c) - S.MAP_OFFSET, emu:read16(c + 2) - S.MAP_OFFSET
end

local function spawn(gfx, id, x, y)
  L.setVar(S.VAR_0x8004, gfx)
  L.setVar(S.VAR_0x8006, id)
  L.setVar(S.VAR_0x8007, x)
  L.setVar(S.VAR_0x8008, y)
  L.runHeader("OikOw_SpawnHeader")
end
local function remove(id)
  L.setVar(S.VAR_0x8006, id)
  L.runHeader("OikOw_RemoveHeader")
end

-- Walk every walker present two tiles one way; returns, per walker, the set
-- of frames shown and whether any was mirrored.
local function step(header, walkers, tag, dir)
  L.setVar(S.VAR_0x8000, 0)
  L.runHeader(header, { noSettle = true })
  local seen = {}
  for i = 1, #walkers do seen[i] = { frames = {}, flipped = false } end
  local took
  for f = 1, 240 do
    for i, w in ipairs(walkers) do
      local o = object(w.id)
      if o then
        seen[i].frames[shown(o)] = true
        if hflip(o) == 1 then seen[i].flipped = true end
      end
    end
    if f == 6 then shot(tag .. "_walk_" .. dir) end
    if L.getVar(S.VAR_0x8000) == 1 then took = f; break end
    L.frame()
  end
  L.settle()
  expect(took ~= nil, string.format("%s: every walker finishes walking %s", tag, dir))
  return seen
end

local WALKS = {
  { header = "OikOw_WalkLeftHeader", dir = "left", frames = { 7, 8 }, flipped = false },
  { header = "OikOw_WalkDownHeader", dir = "down", frames = { 3, 4 }, flipped = false },
  { header = "OikOw_WalkRightHeader", dir = "right", frames = { 7, 8 }, flipped = true },
  { header = "OikOw_WalkUpHeader", dir = "up", frames = { 5, 6 }, flipped = false },
}

L.start(function()
  expect(S.GFX_LAST - S.GFX_FIRST + 1 == 27, "the batch's 27 graphics ids run contiguously")
  L.quickstart()

  -- 1. A follower, Akti, and an empty square
  L.runHeader("OikOw_PartyHeader")
  L.setVar(S.VAR_0x8007, PX)
  L.setVar(S.VAR_0x8008, PY)
  L.runHeader("OikOw_AktiHeader", { limit = 4000 })
  L.waitUntil(function() local x, y = L.pos() return x == PX and y == PY and L.idle() end, 3000, "the warp to Akti")
  expect(L.mapId() == S.MAP_AKTI, "the player is on Akti")
  L.wait(200)                                  -- past the map-name popup
  L.runHeader("OikOw_ClearHeader")
  L.wait(10)

  local player = L.playerObject()
  local follower = object(S.OBJ_EVENT_ID_FOLLOWER)
  expect(follower ~= nil, "a follower walks with the player")
  local playerSlot = palSlot(player)
  local followerSlot = follower and palSlot(follower)
  local playerColours = slotWords(playerSlot)
  local followerColours = follower and slotWords(followerSlot)
  log(string.format("ok player in OBJ palette %d, follower in %s", playerSlot, tostring(followerSlot)))
  shot("akti_cleared")

  -- 2. Each land
  local slots = {}
  for _, land in ipairs(LANDS) do
    L.setBeat(land.tag)
    local walkers = {}
    for i, name in ipairs(land.names) do
      local gfx, spot = land.first + i - 1, SPOTS[i]
      walkers[i] = { name = name, gfx = gfx, id = FIRST_ID + i - 1, x = spot[1], y = spot[2] }
      spawn(gfx, walkers[i].id, spot[1], spot[2])
    end
    L.wait(20)
    local want = palWords(land.file)
    local slot
    for _, w in ipairs(walkers) do
      local o = object(w.id)
      expect(o ~= nil and emu:read16(o + S.OFF_OBJ_GRAPHICS_ID) == w.gfx,
             string.format("%s spawns from OBJ_EVENT_GFX_ICHOR_%s (%d)", w.name, w.name:upper(), w.gfx))
      if o then
        slot = slot or palSlot(o)
        expect(palSlot(o) == slot, string.format("%s shares the %s palette slot (%d, not %d)",
                                                 w.name, land.tag, palSlot(o), slot))
        expect(shown(o) == 0, string.format("%s stands facing down (frame %d)", w.name, shown(o)))
      end
    end
    slots[land.tag] = slot
    expect(slot ~= playerSlot and slot ~= followerSlot,
           string.format("%s palette in slot %d, clear of the player (%d) and the follower (%s)",
                         land.tag, slot, playerSlot, tostring(followerSlot)))
    expect(sameColours(slotWords(slot), want), string.format("slot %d holds exactly %s", slot, land.file))
    expect(sameColours(slotWords(playerSlot), playerColours), land.tag .. ": the player's colours are untouched")
    if follower then
      expect(sameColours(slotWords(followerSlot), followerColours), land.tag .. ": the follower's colours are untouched")
    end
    shot(land.tag .. "_stand")

    for _, walk in ipairs(WALKS) do
      local seen = step(walk.header, walkers, land.tag, walk.dir)
      for i, w in ipairs(walkers) do
        local ok = seen[i].frames[walk.frames[1]] and seen[i].frames[walk.frames[2]]
        expect(ok and seen[i].flipped == walk.flipped,
               string.format("%s walking %s shows frames %d and %d%s", w.name, walk.dir,
                             walk.frames[1], walk.frames[2], walk.flipped and ", mirrored" or ""))
      end
    end
    L.runHeader("OikOw_FaceDownHeader")
    for _, w in ipairs(walkers) do
      local o = object(w.id)
      local x, y = coords(o)
      expect(x == w.x and y == w.y, string.format("%s walks the square back to (%d,%d): at (%d,%d)",
                                                  w.name, w.x, w.y, x, y))
    end
    shot(land.tag .. "_after")
    log(string.format("ok %s: %d walkers in OBJ palette %d", land.tag, #walkers, slot))
    for _, w in ipairs(walkers) do remove(w.id) end
    L.wait(10)
  end

  -- 3. All three lands at once
  L.setBeat("mixed")
  local mixed, n = {}, 0
  for _, land in ipairs(LANDS) do
    for i = 1, 4 do
      n = n + 1
      mixed[n] = { land = land, id = FIRST_ID + n - 1 }
      spawn(land.first + i - 1, mixed[n].id, SPOTS[n][1], SPOTS[n][2])
    end
  end
  L.wait(20)
  local used = {}
  for li, land in ipairs(LANDS) do
    local o = object(mixed[(li - 1) * 4 + 1].id)
    local slot = palSlot(o)
    expect(not used[slot], string.format("%s has a slot of its own (%d)", land.tag, slot))
    used[slot] = true
    expect(slot ~= playerSlot and slot ~= followerSlot, land.tag .. " stays clear of the player and the follower")
    expect(sameColours(slotWords(slot), palWords(land.file)), string.format("slot %d holds %s", slot, land.file))
  end
  expect(sameColours(slotWords(playerSlot), playerColours), "mixed: the player's colours are untouched")
  shot("mixed_stand")
  step("OikOw_WalkDownHeader", {}, "mixed", "down")
end)
