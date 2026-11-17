-- Ordinary move animations must fade the whole battle background or none of it.
-- The painted backgrounds draw their sky or back wall in BG palettes 2-3 and
-- their ground in palette 4, so a fade that skipped palette 4 darkened only
-- the top of the screen. Each turn both sides use the same move: Tackle (no
-- background fade), Brick Break (contact, darkens), Mega Drain (special,
-- tints green) and Scary Face (status, fades to black), over three painted
-- backgrounds.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu

local MOVES = {
  { S.MOVE_TACKLE, "tackle", false },
  { S.MOVE_BRICK_BREAK, "brick_break", true },
  { S.MOVE_MEGA_DRAIN, "mega_drain", true },
  { S.MOVE_SCARY_FACE, "scary_face", true },
}
local BG_PALETTES = { 2, 3, 4 } -- what LoadBattleEnvironmentGfx loads

local function actionMenu()
  return emu:read32(S.gBattlerControllerFuncs) == (S.HandleInputChooseAction | 1)
end

local function faded(p)
  return L.snapshot(S.gPlttBufferFaded + p * 32, 32) ~= L.snapshot(S.gPlttBufferUnfaded + p * 32, 32)
end

-- A metatile in the current layout with this behavior, written under the player
-- (live grid only) so the next wild battle picks that environment.
local function standOn(behavior)
  local layout = emu:read32(S.gMapHeader + S.OFF_MAPHEADER_MAPLAYOUT)
  for mid = 0, S.NUM_METATILES_TOTAL - 1 do
    local ts, idx = emu:read32(layout + S.OFF_LAYOUT_PRIMARY), mid
    if mid >= S.NUM_METATILES_IN_PRIMARY then
      ts, idx = emu:read32(layout + S.OFF_LAYOUT_SECONDARY), mid - S.NUM_METATILES_IN_PRIMARY
    end
    if emu:read16(emu:read32(ts + S.OFF_TILESET_ATTRIBUTES) + 2 * idx) & S.METATILE_ATTR_BEHAVIOR_MASK == behavior then
      local width = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_WIDTH)
      local map = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_MAP)
      local x, y = L.pos()
      local a = map + 2 * ((x + S.MAP_OFFSET) + (y + S.MAP_OFFSET) * width)
      emu:write16(a, (emu:read16(a) & ~S.MAPGRID_METATILE_ID_MASK) | mid)
      return
    end
  end
  L.fail("no metatile with behavior " .. behavior)
end

local function flee()
  L.waitUntil(function()
    if L.inOverworld() then return true end
    if actionMenu() then L.tap(K.DOWN); L.tap(K.RIGHT); L.tap(K.A) else L.tap(K.A) end
    L.wait(4)
    return false
  end, 3000, "fleeing the battle")
  L.settle()
end

-- One turn: both sides use `move`. Every animation frame, the three background
-- palettes must be all faded or all unfaded.
local function turn(env, slot, move)
  local opponent = S.gBattleMons + S.BATTLE_MON_SIZE
  for i = 0, 3 do
    emu:write16(opponent + S.OFF_BATTLE_MON_MOVES + i * S.MOVE_ENTRY_SIZE, move[1])
  end
  L.tap(K.UP); L.tap(K.LEFT); L.tap(K.A)
  L.waitUntil(function() return emu:read32(S.gBattlerControllerFuncs) == (S.HandleInputChooseMove | 1) end,
              300, "the move menu")
  L.wait(10)
  emu:write8(S.gMoveSelectionCursor, slot)
  L.wait(2)
  L.tap(K.A)
  local seen, faded3, split, best, shot = {}, {}, nil, {}, {}
  L.waitUntil(function()
    if emu:read8(S.gAnimScriptActive) ~= 0 and emu:read16(S.gAnimMoveIndex) == move[1] then
      local side = emu:read8(S.gBattleAnimAttacker) & 1
      seen[side] = true
      local state, depth = {}, 0
      for _, p in ipairs(BG_PALETTES) do
        state[#state + 1] = faded(p) and "F" or "-"
        for c = 1, 15 do
          local a = emu:read16(S.gPlttBufferFaded + (p * 16 + c) * 2)
          local b = emu:read16(S.gPlttBufferUnfaded + (p * 16 + c) * 2)
          for sh = 0, 10, 5 do depth = depth + math.abs(((a >> sh) & 31) - ((b >> sh) & 31)) end
        end
      end
      state = table.concat(state)
      if state == "FFF" then faded3[side] = true end
      if state ~= "---" and state ~= "FFF" and not split then split = state end
      -- one screenshot per side, at its deepest background fade
      if depth > 0 and (not best[side] or depth > best[side]) then
        best[side] = depth
        if shot[side] then os.remove(L.OUT .. "shots/" .. shot[side]) end
        shot[side] = L.shot(string.format("%s_side%d_%s", move[2], side, state))
      end
      L.wait(1)
      return false
    end
    if actionMenu() then return true end
    if L.now() % 8 == 0 then L.tap(K.A) else L.wait(1) end
    return false
  end, 3000, move[2] .. "'s turn")
  L.expect(seen[0] and seen[1], string.format("%s: both sides animate %s", env, move[2]))
  L.check(split == nil, string.format("%s: %s fades BG palettes 2-4 together (saw %s)",
                                      env, move[2], tostring(split)))
  if move[3] then
    L.check(faded3[0] and faded3[1], string.format("%s: %s fades the whole background", env, move[2]))
  else
    L.check(not best[0] and not best[1], string.format("%s: %s leaves the background alone", env, move[2]))
  end
end

L.start(function()
  L.quickstart()
  local opt = L.sb2() + S.OFF_SB2_OPTIONS
  emu:write16(opt, emu:read16(opt) & ~(1 << 10)) -- battle animations on
  L.runHeader("Anim_SetupHeader")
  for _, env in ipairs({ { "plain" }, { "grass", S.MB_TALL_GRASS, S.BATTLE_ENVIRONMENT_GRASS },
                         { "sand", S.MB_SAND, S.BATTLE_ENVIRONMENT_SAND } }) do
    L.setBeat(env[1], false)
    if env[2] then standOn(env[2]) end
    L.runHeader("Anim_BattleHeader", { noSettle = true })
    L.waitUntil(function()
      if actionMenu() then return true end
      L.tap(K.A); L.wait(4)
      return false
    end, 3000, "the wild battle's action menu")
    if env[3] then
      L.expect(emu:read8(S.gBattleEnvironment) == env[3], env[1] .. ": the painted background is in use")
    end
    L.wait(30)
    L.shot("menu")
    for slot, move in ipairs(MOVES) do turn(env[1], slot - 1, move) end
    flee()
  end
  if L.bugs > 0 then L.fail(string.format("%d check(s) failed (the BUG lines)", L.bugs)) end
end)
