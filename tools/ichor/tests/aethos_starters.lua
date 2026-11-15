-- Visual check of the Aethos starters: screenshots of the starter choice
-- showing Nebrel, Kynder and Hipling, then the first battle with Nebrel.
--
--   build/tools/ichor-mgba-headless --script tools/ichor/tests/aethos_starters.lua \
--       --frames 6000 --until "STARTERS done" pokeemerald.gba
--
-- Quickstarts a new game (the smoke test's timing), then runs the ChooseStarter
-- special by pointing gMain.callback2 at it, as the script command would.
-- Screenshots go to build/aethos_dex/ (which must exist).

local OUT = os.getenv("STARTERS_OUT") or "build/aethos_dex/"
local K = C.GBA_KEY

local function sym(name)
  local f = io.open("pokeemerald.map", "r")
  if not f then return nil end
  local addr
  for line in f:lines() do
    addr = line:match("^%s+0x(%x+)%s+" .. name .. "%s*$")
    if addr then break end
  end
  f:close()
  return addr and tonumber(addr, 16)
end

local MAIN, CHOOSE = sym("gMain"), sym("ChooseStarter")

local schedule = {
  [500]  = { press = K.START },
  [1020] = { press = K.SELECT },                 -- Quickstart
  [2500] = { choose = true },                    -- special ChooseStarter
  [2800] = { shot = "starter_0_intro.png" },
  [2820] = { press = K.A },                      -- look at the Grass starter
  [2950] = { shot = "starter_1_nebrel.png" },
  [2960] = { press = K.B },
  [3020] = { press = K.RIGHT },
  [3040] = { press = K.A },
  [3170] = { shot = "starter_2_kynder.png" },
  [3180] = { press = K.B },
  [3240] = { press = K.RIGHT },
  [3260] = { press = K.A },
  [3390] = { shot = "starter_3_hipling.png" },
  [3400] = { press = K.B },
  [3460] = { press = K.LEFT },
  [3480] = { press = K.LEFT },
  [3500] = { press = K.A },                      -- Nebrel
  [3640] = { press = K.A },                      -- yes
  [4300] = { shot = "battle_1.png" },
  [4400] = { press = K.A },
  [4600] = { shot = "battle_2.png" },
  [4700] = { press = K.A },
  [4900] = { shot = "battle_3.png" },
  [4920] = { press = K.A },
  [5000] = { shot = "battle_4_moves.png" },
  [5010] = { done = true },
}

local held, releaseAt = nil, 0
callbacks:add("frame", function()
  local f = emu:currentFrame()
  if held and f >= releaseAt then emu:clearKey(held); held = nil end
  local step = schedule[f]
  if not step then return end
  if step.press then emu:addKey(step.press); held = step.press; releaseAt = f + 6 end
  if step.choose then
    if MAIN and CHOOSE then emu:write32(MAIN + 4, CHOOSE | 1) else console:log("STARTERS FAIL: no gMain/ChooseStarter") end
  end
  if step.shot then emu:screenshot(OUT .. step.shot); console:log("STARTERS shot " .. step.shot) end
  if step.done then console:log("STARTERS done") end
end)
