-- Pokemon Ichor smoke test.
-- Run by tools/ichor/smoke_test.sh in build/tools/ichor-mgba-headless.
-- Boots the ROM, walks the title flow with the expansion's Quickstart (SELECT on
-- the title screen) and saves screenshots to build/smoke/.

local OUT = "build/smoke/"
local K = C.GBA_KEY

-- frame -> action. Presses last 6 frames. Frame timing is stable for a given ROM
-- (re-probe if the intro or the opening scene changes); RNG is not, because it
-- follows the real-time clock, so Quickstart's player gender varies between runs.
local schedule = {
  [500]  = { press = K.START },              -- skip the intro; title is up by ~900
  [1000] = { shot = "01_title.png" },
  [1020] = { press = K.SELECT },             -- Quickstart: new game from title
  [2500] = { shot = "02_new_game.png" },     -- at home in Elaia Village
  [2600] = { press = K.START },              -- open the start menu
  [2700] = { shot = "03_start_menu.png" },
  [2720] = { press = K.B },
  [2800] = { done = true },
}

local held, releaseAt = nil, 0

callbacks:add("frame", function()
  local f = emu:currentFrame()
  if held and f >= releaseAt then emu:clearKey(held); held = nil end
  local step = schedule[f]
  if not step then return end
  if step.press then emu:addKey(step.press); held = step.press; releaseAt = f + 6 end
  if step.shot then emu:screenshot(OUT .. step.shot); console:log("SMOKE shot " .. step.shot .. " at frame " .. f) end
  if step.done then console:log("SMOKE done at frame " .. f) end -- the runner stops on this line
end)
