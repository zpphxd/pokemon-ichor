-- Ichor's themed balls, thrown in a real wild battle: for each ball, the ball
-- pocket emptied, five of that ball given, a battle on Route 1's grass, and the
-- ball chosen from the battle Bag. Screenshots every few frames from the throw
-- to the last wobble (shots/NNNN_<ball>_tNNN.png), with the battle scene on.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu

local BALLS = {
  { "poseidon", "Ball_GiveDiveHeader", S.ITEM_DIVE_BALL },
  { "daedalus", "Ball_GiveMasterHeader", S.ITEM_MASTER_BALL },
  { "theseus", "Ball_GiveGreatHeader", S.ITEM_GREAT_BALL },
  { "nyx", "Ball_GiveDuskHeader", S.ITEM_DUSK_BALL },
  { "poke", "Ball_GivePokeHeader", S.ITEM_POKE_BALL },
}

local function emptyBallPocket()
  local base = L.sb1() + S.OFF_SB1_BAG + S.OFF_BAG_BALLS
  for i = 0, S.BAG_POKEBALLS_COUNT * S.ITEM_SLOT_SIZE - 1, 2 do emu:write16(base + i, 0) end
end

local function throw(name, header, item)
  L.beat = name
  emptyBallPocket()
  L.runHeader(header)
  L.expect(L.itemCount(item) == 5, name .. ": five balls in the Bag")
  L.runHeader("Ball_BattleHeader", { noSettle = true })
  L.waitUntil(function()
    if emu:read32(S.gBattlerControllerFuncs) == (S.HandleInputChooseAction | 1) then return true end
    L.tap(K.A); L.wait(4)
    return false
  end, 3000, name .. ": the wild battle's action menu")
  L.wait(20)
  L.tap(K.UP); L.tap(K.RIGHT); L.tap(K.A)
  L.waitUntil(function() return L.taskRunning("Task_BagMenu_HandleInput") end, 1200, name .. ": the battle Bag")
  L.wait(30)
  for _ = 1, S.POCKETS_COUNT do
    if emu:read8(S.gBagPosition + S.OFF_BAG_POSITION_POCKET) == S.POCKET_POKE_BALLS then break end
    L.tap(K.RIGHT); L.wait(50)
  end
  L.shot("bag")
  L.tap(K.UP); L.tap(K.UP); L.tap(K.A); L.wait(20); L.tap(K.A)
  for t = 0, 420, 4 do
    L.shot(string.format("t%03d", t))
    L.wait(4)
  end
  L.expect(L.itemCount(item) == 4, name .. ": one ball thrown")
  L.battle()
  L.settle()
end

L.start(function()
  L.quickstart()
  -- the battle scene on, so the throw animates (quickstart turns it off)
  local opt = L.sb2() + S.OFF_SB2_OPTIONS
  emu:write16(opt, emu:read16(opt) & ~(1 << 10))
  L.runHeader("Ball_SetupHeader")
  for _, b in ipairs(BALLS) do throw(b[1], b[2], b[3]) end
end)
