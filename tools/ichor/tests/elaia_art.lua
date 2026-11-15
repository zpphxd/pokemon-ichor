-- An engine-rendered gallery, not a substitute for the real opening playthrough.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, emu = L.S, L.emu
local BEFORE = os.getenv("ELAIA_ART_BASELINE") == "1"
local names = {
  "NEBREL", "KLADOE", "DAPHNYAD", "KYNDER", "DIKYON", "PYLAKYON",
  "HIPLING", "THALAMARE", "SEISMARE", "ERIPIP", "GALEKIT", "SMOLIV",
}

local function sprite(id)
  return S.gSprites + id * S.SPRITE_SIZE
end

L.start(function()
  L.quickstart()
  for _, name in ipairs(names) do
    for shiny = 0, 1 do
      L.setVar(S.VAR_0x8000, S[name])
      L.setVar(S.VAR_0x8001, shiny)
      L.runHeader("ElaiaArt_ShowHeader")
      local front = L.getVar(S.VAR_0x8005)
      local back = L.getVar(S.VAR_0x8006)
      L.expect(front < S.SPRITE_LIMIT and back < S.SPRITE_LIMIT and front ~= back,
               name .. " loads distinct front/back sprite IDs")
      if front >= S.SPRITE_LIMIT or back >= S.SPRITE_LIMIT or front == back then
        L.fail(name .. " sprite allocation failed")
      end
      L.expect(emu:read16(sprite(front) + 4) >> 12 == 14
               and emu:read16(sprite(back) + 4) >> 12 == 15,
               name .. " uses the requested independent palette slots")
      local images = emu:read32(sprite(front) + S.OFF_SPRITE_IMAGES)
      local first = emu:read32(images)
      local second = emu:read32(images + S.FRAME_IMAGE_SIZE)
      if not (BEFORE and name == "SMOLIV") then
        L.expect(L.snapshot(first, S.PIC_BYTES) ~= L.snapshot(second, S.PIC_BYTES),
                 name .. " decompresses two distinct native front frames")
      end
      L.wait(8)
      local tag = name:lower() .. (shiny == 1 and "_shiny" or "_normal")
      L.shot(tag .. "_front0_back")
      -- The preserved baseline's Smoliv has only one supported front frame.
      if not (BEFORE and name == "SMOLIV") then
        L.setVar(S.VAR_0x8002, S.SPRITE_SIZE)
        L.runHeader("ElaiaArt_FrameHeader")
        L.wait(8)
        L.expect(emu:read8(sprite(front) + S.OFF_SPRITE_ANIM_NUM) == 1,
                 name .. " switches to front frame 1 through StartSpriteAnim")
        L.shot(tag .. "_front1_back")
      end
      L.runHeader("ElaiaArt_FreeHeader")
    end
  end
end)
