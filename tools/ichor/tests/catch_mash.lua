-- The catch mash (src/ichor_catch.c, design/ENGINE_API.md §12) in real battles.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local M = S.gIchorCatchMash
local function isOpen() return emu:read8(M + S.OFF_MASH_OPEN) ~= 0 end
local function presses() return emu:read8(M + S.OFF_MASH_PRESSES) end
local function baseOdds() return emu:read16(M + S.OFF_MASH_BASE) end
local function finalOdds() return emu:read16(M + S.OFF_MASH_FINAL) end
local function atAction() return emu:read32(S.gBattlerControllerFuncs) == (S.HandleInputChooseAction | 1) end

local function begin()
  L.runHeader("Mash_BattleHeader", { noSettle = true })
  L.waitUntil(function()
    if atAction() then return true end
    L.tap(K.A); L.wait(4)
    return false
  end, 2000, "the wild battle's action menu")
end

-- Bag, ball pocket, then the ball `down` rows below the top; Use.
local function throw(down)
  L.tap(K.UP); L.tap(K.RIGHT); L.tap(K.A)
  L.waitUntil(function() return L.taskRunning("Task_BagMenu_HandleInput") end, 1200, "the battle Bag")
  L.wait(30)
  for _ = 1, S.POCKETS_COUNT do
    if emu:read8(S.gBagPosition + S.OFF_BAG_POSITION_POCKET) == S.POCKET_POKE_BALLS then break end
    L.tap(K.RIGHT); L.wait(50)
  end
  L.tap(K.UP); L.tap(K.UP)
  for _ = 1, down do L.tap(K.DOWN) end
  L.tap(K.A); L.wait(20); L.tap(K.A)
end

-- After a throw: back at the action menu (it broke free) or caught.
local function outcome()
  L.waitUntil(function()
    if atAction() or L.inOverworld() then return true end
    if L.on("CB2_NamingScreen") then L.acceptName("caught") else L.tap(K.A); L.wait(4) end
    return false
  end, 6000, "the throw to resolve")
  return atAction() and "free" or "caught"
end

local function waitForWindow(what)
  L.waitUntil(isOpen, 600, what)
end

L.start(function()
  L.expect(M ~= nil, "the catch-mash state symbol is available")
  L.quickstart()
  L.runHeader("Mash_SetupHeader")
  begin()
  L.shot("wild_nebrel")

  -- 1. A mashed throw.
  local caught = false
  throw(0)
  waitForWindow("the silent window on a Poké Ball throw")
  L.expect(presses() == 0, "the window opens with no presses counted")
  L.wait(4)
  L.shot("silent_window")
  local most, took = 0, false
  for i = 1, S.MASH_CAP + 4 do
    if not isOpen() then break end
    L.tap(K.A)
    if isOpen() then most = math.max(most, presses()) end
    if i == 5 then L.shot("mashing_half") end
    if most == S.MASH_CAP and not took then L.shot("mashing_full"); took = true end
  end
  L.expect(most == S.MASH_CAP, "mashing fills the row to the cap (" .. most .. "/" .. S.MASH_CAP .. ")")
  L.waitUntil(function() return not isOpen() end, S.MASH_FRAMES + 30, "the window to close")
  local base, final = baseOdds(), finalOdds()
  local want = math.min(S.MASH_CEILING, base * (100 + S.MASH_MAX_BONUS) // 100)
  L.expect(base == 45, "Nebrel at level 3 has a modified catch rate of 45 (" .. base .. ")")
  L.expect(final == want, string.format("the capped mash raises the rate x1.3: %d -> %d (want %d)", base, final, want))
  L.expect(presses() == 0, "the throw spends its presses")
  L.wait(40)
  L.shot("throw_after_mash")
  caught = outcome() == "caught"
  L.log("first throw " .. (caught and "caught" or "broke free"))

  -- 2. An untouched throw: the window still opens, the rate stays vanilla.
  if caught then begin() end
  throw(0)
  waitForWindow("the silent window on a second throw")
  L.waitUntil(function() return not isOpen() end, S.MASH_FRAMES + 30, "the untouched window to time out")
  L.expect(baseOdds() == 45 and finalOdds() == 45, "no presses keeps the vanilla rate (" .. finalOdds() .. ")")
  if outcome() == "caught" then begin() end

  -- 3. A Master Ball: no window, a sure catch.
  local balls = L.itemCount(S.ITEM_MASTER_BALL)
  throw(1)
  local opened = false
  L.waitUntil(function()
    if isOpen() then opened = true end
    if L.inOverworld() then return true end
    if L.on("CB2_NamingScreen") then L.acceptName("master_ball_catch") else L.tap(K.A); L.wait(4) end
    return false
  end, 6000, "the Master Ball catch")
  L.expect(not opened, "a Master Ball throw opens no window")
  L.expect(L.itemCount(S.ITEM_MASTER_BALL) == balls - 1 and emu:read8(S.gBattleOutcome) == S.B_OUTCOME_CAUGHT,
           "the Master Ball still catches outright")
end)
