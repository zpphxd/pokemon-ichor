-- Visual check of the Aethos Pokédex: the regional list and a few entries.
--
--   build/tools/ichor-mgba-headless --script tools/ichor/tests/aethos_pokedex.lua \
--       --frames 6000 --until "POKEDEX done" pokeemerald.gba
--
-- Quickstarts a new game, gives the Pokédex and marks every Aethos species
-- seen and caught, then opens the Pokédex from the start menu. Screenshots go
-- to build/aethos_dex/ (which must exist).
--
-- Pokes memory through gSaveBlock1Ptr. Offsets are from include/global.h for
-- this build (SaveBlock1.flags 0x1270, dexSeen 0x3598, dexCaught 0x362C; recheck
-- them if SaveBlock1 changes), FLAG_SYS_POKEDEX_GET = 2145, and the Aethos
-- national numbers run from AETHOS_FIRST_NAT (1026) for 152 species.

local OUT = os.getenv("POKEDEX_OUT") or "build/aethos_dex/"
local K = C.GBA_KEY
local FLAGS, SEEN, CAUGHT = 0x1270, 0x3598, 0x362C
local FLAG_SYS_POKEDEX_GET = 2145
local FIRST_NAT, COUNT = tonumber(os.getenv("AETHOS_FIRST_NAT") or "1026"), 152

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

local SB1 = sym("gSaveBlock1Ptr")

local function setBit(base, n)
  local byte = base + (n >> 3)
  emu:write8(byte, emu:read8(byte) | (1 << (n & 7)))
end

local function giveDex()
  local sb = emu:read32(SB1)
  setBit(sb + FLAGS, FLAG_SYS_POKEDEX_GET)
  for i = 0, COUNT - 1 do
    local n = FIRST_NAT + i - 1
    setBit(sb + SEEN, n)
    setBit(sb + CAUGHT, n)
  end
end

local schedule = {
  [500]  = { press = K.START },
  [1020] = { press = K.SELECT },          -- Quickstart
  [2500] = { give = true },
  [2560] = { press = K.START },           -- start menu: Pokédex is first
  [2640] = { shot = "dex_0_menu.png" },
  [2660] = { press = K.A },
  [2900] = { shot = "dex_1_list.png" },
  [2920] = { press = K.A },               -- #001 Nebrel
  [3150] = { shot = "dex_2_nebrel.png" },
  [3170] = { press = K.B },
  [3300] = { press = K.LEFT },            -- page up the list from the top wraps nowhere; go down instead
  [3320] = { press = K.RIGHT },
  [3340] = { press = K.RIGHT },
  [3360] = { press = K.RIGHT },
  [3380] = { press = K.RIGHT },
  [3400] = { press = K.RIGHT },
  [3420] = { press = K.RIGHT },
  [3440] = { press = K.RIGHT },
  [3460] = { press = K.RIGHT },
  [3480] = { press = K.RIGHT },
  [3500] = { press = K.RIGHT },
  [3520] = { press = K.RIGHT },
  [3540] = { press = K.RIGHT },
  [3560] = { press = K.RIGHT },
  [3580] = { press = K.RIGHT },
  [3600] = { press = K.RIGHT },
  [3620] = { press = K.RIGHT },
  [3700] = { shot = "dex_3_list_end.png" },
  [3720] = { press = K.A },
  [3950] = { shot = "dex_4_entry.png" },
  [3960] = { done = true },
}

local held, releaseAt = nil, 0
callbacks:add("frame", function()
  local f = emu:currentFrame()
  if held and f >= releaseAt then emu:clearKey(held); held = nil end
  local step = schedule[f]
  if not step then return end
  if step.press then emu:addKey(step.press); held = step.press; releaseAt = f + 6 end
  if step.give then if SB1 then giveDex() else console:log("POKEDEX FAIL: no gSaveBlock1Ptr") end end
  if step.shot then emu:screenshot(OUT .. step.shot); console:log("POKEDEX shot " .. step.shot) end
  if step.done then console:log("POKEDEX done") end
end)
