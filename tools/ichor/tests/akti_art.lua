-- Real engine loaders on an EWRAM-only fixture, not a battle-playthrough claim.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, emu = L.S, L.emu

local function sprite(id)
  return S.gSprites + id * S.SPRITE_SIZE
end

L.start(function()
  L.quickstart()
  for _, name in ipairs({"NEMECUB", "NEMELEON"}) do
    for shiny = 0, 1 do
      L.setVar(S.VAR_0x8000, S[name])
      L.setVar(S.VAR_0x8001, shiny)
      L.runHeader("AktiArt_MonHeader")
      local front, back = L.getVar(S.VAR_0x8005), L.getVar(S.VAR_0x8006)
      L.expect(front < S.SPRITE_LIMIT and back < S.SPRITE_LIMIT and front ~= back,
               name .. " loads separate front/back sprites")
      if front >= S.SPRITE_LIMIT or back >= S.SPRITE_LIMIT then L.fail("sprite allocation failed") end
      L.expect(emu:read16(sprite(front) + 4) >> 12 == 14
               and emu:read16(sprite(back) + 4) >> 12 == 15,
               name .. " loads independent palette slots")
      local images = emu:read32(sprite(front) + S.OFF_SPRITE_IMAGES)
      L.expect(L.snapshot(emu:read32(images), S.PIC_BYTES)
               ~= L.snapshot(emu:read32(images + S.FRAME_IMAGE_SIZE), S.PIC_BYTES),
               name .. " decompresses distinct front frames")
      L.wait(8)
      local tag = name:lower() .. (shiny == 1 and "_shiny" or "_normal")
      L.shot(tag .. "_front0_back")
      L.setVar(S.VAR_0x8002, S.SPRITE_SIZE)
      L.runHeader("AktiArt_FrameHeader")
      L.wait(8)
      L.expect(emu:read8(sprite(front) + S.OFF_SPRITE_ANIM_NUM) == 1,
               name .. " starts front frame1 through the engine")
      L.shot(tag .. "_front1_back")
      L.runHeader("AktiArt_FreeMonHeader")
    end
  end
  for _, name in ipairs({"SHEPHERD", "HARVESTER", "GOATHERD", "HOPLITE", "AUGUR", "ACOLYTE_M", "ACOLYTE_F"}) do
    L.setVar(S.VAR_0x8000, S[name])
    L.runHeader("AktiArt_TrainerHeader")
    local id = L.getVar(S.VAR_0x8005)
    L.expect(id < S.SPRITE_LIMIT, name .. " loads its trainer front sprite")
    if id >= S.SPRITE_LIMIT then L.fail("trainer allocation failed") end
    L.expect(emu:read16(sprite(id) + 4) >> 12 == 14, name .. " uses the requested portrait palette slot")
    local info = emu:read32(S.gTrainerPicInfo + S[name] * S.TRAINER_INFO_SIZE + S.OFF_TRAINER_FRONT)
    local source = emu:read32(info + S.OFF_TRAINER_PALETTE)
    L.expect(L.snapshot(source, 32) == L.snapshot(S.gPlttBufferUnfaded + (256 + 14 * 16) * 2, 32),
             name .. " loads all16 colors from its actual ROM portrait palette")
    L.wait(8)
    L.shot(name:lower() .. "_portrait")
    L.runHeader("AktiArt_FreeTrainerHeader")
  end
end)
