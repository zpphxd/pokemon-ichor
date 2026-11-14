-- Pokemon Ichor UI check: captures the pottery dialogue box and menu frames.
-- Run by tools/ichor/ui_check.sh in build/tools/ichor-mgba-headless.
-- Reuses the smoke test's proven title flow (Quickstart, then the truck), then
-- opens the start menu, picks SAVE to get a dialogue box and a YES/NO box,
-- cancels, opens OPTION and previews frame types 2-5 (then sets type 1 back),
-- then reads a box in the
-- truck three times: as a plain message, with a speaker name box, and as a
-- sign. The last two are forced by writing gSpeakerName and gMsgIsSignPost;
-- ui_check.sh passes their addresses from pokeemerald.map. This only drives
-- the art check; the smoke test never touches memory.

local OUT = os.getenv("UI_CHECK_OUT") or "build/ui_check/"
local K = C.GBA_KEY
local SPEAKER = tonumber(os.getenv("UI_SPEAKER_NAME") or "")      -- &gSpeakerName
local SPEAKERS = tonumber(os.getenv("UI_SPEAKER_TABLE") or "")    -- gSpeakerNamesTable
local SIGNPOST = tonumber(os.getenv("UI_MSG_IS_SIGNPOST") or "")  -- &gMsgIsSignPost
local SP_NAME_MOM = 1

local function setSpeaker()
  if SPEAKER and SPEAKERS then emu:write32(SPEAKER, emu:read32(SPEAKERS + 4 * SP_NAME_MOM)) end
end
local function setSignpost()
  if SIGNPOST then emu:write8(SIGNPOST, 1) end
end

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
  [3320] = { press = K.DOWN },
  [3340] = { press = K.DOWN },
  [3360] = { press = K.DOWN },
  [3380] = { press = K.DOWN },
  [3400] = { press = K.DOWN },               -- FRAME
  [3420] = { press = K.RIGHT },              -- preview TYPE2..5 in the options window
  [3460] = { shot = "ui_frame_2.png" },
  [3480] = { press = K.RIGHT },
  [3520] = { shot = "ui_frame_3.png" },
  [3540] = { press = K.RIGHT },
  [3580] = { shot = "ui_frame_4.png" },
  [3600] = { press = K.RIGHT },
  [3640] = { shot = "ui_frame_5.png" },
  [3660] = { press = K.LEFT },
  [3680] = { press = K.LEFT },
  [3700] = { press = K.LEFT },
  [3720] = { press = K.LEFT },               -- back to TYPE1 before leaving
  [3760] = { press = K.B },                  -- leave options
  [3900] = { shot = "ui_after_options.png" },
  [3920] = { press = K.B },                  -- close the start menu
  [4020] = { press = K.DOWN },               -- face the box below the player
  [4040] = { press = K.DOWN },
  [4060] = { press = K.DOWN },
  [4080] = { press = K.A },                  -- read it: a plain field message
  [4160] = { shot = "ui_dialogue_printing.png" },
  [4300] = { shot = "ui_dialogue.png" },
  [4320] = { press = K.A },                  -- second page (a page takes ~200 frames)
  [4580] = { press = K.A },                  -- close
  [4660] = { poke = setSpeaker },            -- next message gets a "MOM" name box
  [4680] = { press = K.A },
  [4900] = { shot = "ui_name_box.png" },
  [4920] = { press = K.A },
  [5160] = { press = K.A },                  -- close; the name box clears itself
  [5240] = { press = K.A },                  -- and once more, framed as a sign
  [5241] = { poke = setSignpost, until_ = 5300 },
  [5460] = { shot = "ui_sign.png" },
  [5480] = { done = true },
}

local held, releaseAt = nil, 0
local poking, pokeUntil = nil, 0

callbacks:add("frame", function()
  local f = emu:currentFrame()
  if held and f >= releaseAt then emu:clearKey(held); held = nil end
  if poking then
    if f <= pokeUntil then poking() else poking = nil end
  end
  local step = schedule[f]
  if not step then return end
  if step.press then emu:addKey(step.press); held = step.press; releaseAt = f + 6 end
  if step.poke then step.poke(); if step.until_ then poking, pokeUntil = step.poke, step.until_ end end
  if step.shot then emu:screenshot(OUT .. step.shot); console:log("UI shot " .. step.shot .. " at frame " .. f) end
  if step.done then console:log("UI done at frame " .. f) end -- the runner stops on this line
end)
