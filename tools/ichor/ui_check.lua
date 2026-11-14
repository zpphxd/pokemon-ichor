-- Pokemon Ichor UI check: captures the pottery dialogue box and menu frames.
-- Run by tools/ichor/ui_check.sh in build/tools/ichor-mgba-headless.
-- Reuses the smoke test's proven title flow (Quickstart, then the truck), then
-- opens the start menu, picks SAVE to get a dialogue box and a YES/NO box,
-- cancels, and opens OPTION to show the frame setting.

local OUT = os.getenv("UI_CHECK_OUT") or "build/ui_check/"
local K = C.GBA_KEY

-- frame -> action. Presses last 6 frames. Start menu (truck): BAG, <player>,
-- SAVE, OPTION, EXIT.
local schedule = {
  [500]  = { press = K.START },              -- skip the intro (smoke test timing)
  [1020] = { press = K.SELECT },             -- Quickstart: new game from title
  [2600] = { press = K.START },              -- open the start menu
  [2700] = { shot = "ui_start_menu.png" },
  [2720] = { press = K.DOWN },
  [2740] = { press = K.DOWN },               -- cursor on SAVE
  [2760] = { press = K.A },
  [2800] = { shot = "ui_save_printing.png" },
  [2950] = { shot = "ui_yes_no.png" },       -- "Would you like to save..." + YES/NO
  [2970] = { press = K.B },                  -- NO: back to the start menu, on SAVE
  [3080] = { shot = "ui_menu_after_no.png" },
  [3100] = { press = K.DOWN },               -- OPTION
  [3120] = { press = K.A },
  [3300] = { shot = "ui_options.png" },
  [3320] = { press = K.B },                  -- leave options
  [3500] = { shot = "ui_after_options.png" },
  [3520] = { press = K.B },                  -- close the start menu
  [3620] = { press = K.DOWN },               -- face the box below the player
  [3640] = { press = K.DOWN },
  [3660] = { press = K.DOWN },
  [3680] = { press = K.A },                  -- read it: a plain field message
  [3760] = { shot = "ui_dialogue_printing.png" },
  [3900] = { shot = "ui_dialogue.png" },
  [3920] = { done = true },
}

local held, releaseAt = nil, 0

callbacks:add("frame", function()
  local f = emu:currentFrame()
  if held and f >= releaseAt then emu:clearKey(held); held = nil end
  local step = schedule[f]
  if not step then return end
  if step.press then emu:addKey(step.press); held = step.press; releaseAt = f + 6 end
  if step.shot then emu:screenshot(OUT .. step.shot); console:log("UI shot " .. step.shot .. " at frame " .. f) end
  if step.done then console:log("UI done at frame " .. f) end -- the runner stops on this line
end)
