-- Pokemon Ichor UI check: captures the pottery dialogue box and menu frames.
-- Run by tools/ichor/ui_check.sh in build/tools/ichor-mgba-headless.
--
-- 1. Quickstart (the player's bedroom), then the start menu: SAVE gives a
--    dialogue box and a YES/NO box, OPTION previews frame types 2-5 and sets
--    type 1 back.
-- 2. The Akti Asclepeion, loaded directly (see tests/ichor_lib.lua): talk to
--    the old man for a plain field message, talk again with a speaker name
--    forced for the name box, then read the Asclepius statue for the sign
--    frame. The bedroom has nothing to read, so the check goes where the
--    slice's own people are. Where to stand is read from the map's JSON, so
--    the check follows the map if its events move.
--
-- The name box is forced by writing gSpeakerName (ui_check.sh passes its
-- address from pokeemerald.map). This only drives the art check; the smoke
-- test never touches memory.

local L = dofile("tools/ichor/tests/ichor_lib.lua")
local K = L.K
local OUT = os.getenv("UI_CHECK_OUT") or "build/ui_check/"
local SPEAKER = tonumber(os.getenv("UI_SPEAKER_NAME") or "")      -- &gSpeakerName
local SPEAKERS = tonumber(os.getenv("UI_SPEAKER_TABLE") or "")    -- gSpeakerNamesTable
local SP_NAME_MOM = 1

local MAP_NAME = "AktiTown_Asclepeion"
local MAP_CONST = "MAP_AKTI_TOWN_ASCLEPEION"
local NPC_SCRIPT = "AktiTown_Asclepeion_EventScript_OldMan"
local SIGN_SCRIPT = "AktiTown_Asclepeion_EventScript_Statue"

local function read(path)
  local f = io.open(path, "r")
  if not f then return nil end
  local s = f:read("a")
  f:close()
  return s
end

-- Map group and number from include/constants/map_groups.h: (num | (group << 8)).
local function map_id(name)
  local s = read("include/constants/map_groups.h") or ""
  local num, group = s:match(name .. "%s*=%s*%((%d+)%s*|%s*%((%d+)%s*<<%s*8%)%)")
  return tonumber(group), tonumber(num)
end

-- The x and y of the event in a map.json whose script is `script`.
local function event_pos(map, script)
  local s = read("data/maps/" .. map .. "/map.json") or ""
  local at = s:find('"' .. script .. '"', 1, true)
  if not at then return nil end
  local open = 1
  for i = at, 1, -1 do
    if s:sub(i, i) == "{" then open = i; break end
  end
  local block = s:sub(open, at)
  return tonumber(block:match('"x"%s*:%s*(%-?%d+)')), tonumber(block:match('"y"%s*:%s*(%-?%d+)'))
end

local group, num = map_id(MAP_CONST)
local nx, ny = event_pos(MAP_NAME, NPC_SCRIPT)
local sx, sy = event_pos(MAP_NAME, SIGN_SCRIPT)
if not (group and nx and sx) then
  console:log("UI FAIL: could not find " .. MAP_CONST .. ", the old man or the statue")
end

local function poke(fn, why)
  return { check = function() fn(); return true, why end }
end

local function set_speaker()
  if SPEAKER and SPEAKERS then emu:write32(SPEAKER, emu:read32(SPEAKERS + 4 * SP_NAME_MOM)) end
end

-- Stand south of (x, y) and face it.
local function face(x, y)
  return {
    { warp = { group or 0, num or 0, -1, x, y + 1 }, wait = 120 },
    { press = K.UP, wait = 30 },
  }
end

local steps = L.seq(
  L.quickstart(),
  { { wait = 100 },
    -- The start menu (bedroom): BAG, <player>, SAVE, OPTION, EXIT.
    { press = K.START, wait = 100 }, { shot = "ui_start_menu.png", wait = 20 },
    { press = K.DOWN, wait = 20 }, { press = K.DOWN, wait = 20 },   -- SAVE
    { press = K.A, wait = 40 }, { shot = "ui_save_printing.png", wait = 150 },
    { shot = "ui_yes_no.png", wait = 20 },                          -- "Would you like to save..." + YES/NO
    { press = K.B, wait = 110 }, { shot = "ui_menu_after_no.png", wait = 20 },
    { press = K.DOWN, wait = 20 },                                  -- OPTION
    { press = K.A, wait = 180 }, { shot = "ui_options.png", wait = 20 },
    { press = K.DOWN, wait = 20 }, { press = K.DOWN, wait = 20 }, { press = K.DOWN, wait = 20 },
    { press = K.DOWN, wait = 20 }, { press = K.DOWN, wait = 20 },   -- FRAME
    { press = K.RIGHT, wait = 40 }, { shot = "ui_frame_2.png", wait = 20 },
    { press = K.RIGHT, wait = 40 }, { shot = "ui_frame_3.png", wait = 20 },
    { press = K.RIGHT, wait = 40 }, { shot = "ui_frame_4.png", wait = 20 },
    { press = K.RIGHT, wait = 40 }, { shot = "ui_frame_5.png", wait = 20 },
    { press = K.LEFT, wait = 20 }, { press = K.LEFT, wait = 20 },
    { press = K.LEFT, wait = 20 }, { press = K.LEFT, wait = 40 },   -- back to TYPE1
    { press = K.B, wait = 140 }, { shot = "ui_after_options.png", wait = 20 },
    { press = K.B, wait = 60 } },                                   -- close the start menu

  -- A plain field message: the old man's two pages, at the player's text speed.
  face(nx or 0, ny or 0),
  { { press = K.A, wait = 60 }, { shot = "ui_dialogue_printing.png", wait = 280 },
    { shot = "ui_dialogue.png", wait = 20 },
    { press = K.A, wait = 300 }, { press = K.A, wait = 80 } },

  -- The same, with a speaker name: the name box. Instant text from here on.
  { { instant_text = true }, poke(set_speaker, "speaker set to MOM"),
    { press = K.A, wait = 40 }, { shot = "ui_name_box.png", wait = 20 },
    { press = K.A, wait = 40 }, { press = K.A, wait = 80 } },

  -- The statue: a sign.
  face(sx or 0, sy or 0),
  { { press = K.A, wait = 40 }, { shot = "ui_sign.png", wait = 20 },
    { press = K.A, wait = 60 } }
)

L.run("UI", OUT, steps)
