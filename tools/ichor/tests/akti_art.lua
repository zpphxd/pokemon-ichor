-- Real engine loaders on an EWRAM-only fixture, not a battle-playthrough claim.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, emu = L.S, L.emu

local function sprite(id)
  return S.gSprites + id * S.SPRITE_SIZE
end

local function expect_copied_frame(id, frame, description)
  local images = emu:read32(sprite(id) + S.OFF_SPRITE_IMAGES)
  local source = emu:read32(images + frame * S.FRAME_IMAGE_SIZE)
  local tile = emu:read16(sprite(id) + 4) & 0x3FF
  L.expect(L.snapshot(S.OBJ_VRAM_START + tile * 32, S.PIC_BYTES)
           == L.snapshot(source, S.PIC_BYTES), description .. " complete OBJ VRAM frame")
end

local pokemon = {"NEMECUB", "NEMELEON"}
local supported = {
  NEMECUB = true, NEMELEON = true,
  EOPEEP = true, ALEKROW = true, HOPLEKTOR = true,
  HARPECK = true, HARPELLE = true, EPOPOI = true,
  LOPHOPS = true, BASILOPS = true, GELASABLE = true,
  KERAZAP = true, KERASTORM = true,
}
local selected = os.getenv("AKTI_ART_POKEMON")
if selected then
  pokemon = {}
  for raw in (selected .. ","):gmatch("(.-),") do
    local name = raw:match("^%s*(.-)%s*$"):upper()
    assert(name ~= "", "Akti gallery species selection contains an empty name")
    assert(supported[name], "unsupported Akti gallery species " .. name)
    table.insert(pokemon, name)
  end
end

L.start(function()
  L.quickstart()
  for _, name in ipairs(pokemon) do
    local normalPalette
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
      local palette = L.snapshot(S.gPlttBufferUnfaded + (256 + 14 * 16) * 2, 32)
      L.expect(palette == L.snapshot(S.gPlttBufferUnfaded + (256 + 15 * 16) * 2, 32),
               name .. " front/back load the same16 palette colors")
      if shiny == 0 then
        normalPalette = palette
      else
        L.expect(palette ~= normalPalette, name .. " shiny palette differs from normal")
      end
      local images = emu:read32(sprite(front) + S.OFF_SPRITE_IMAGES)
      L.expect(L.snapshot(emu:read32(images), S.PIC_BYTES)
               ~= L.snapshot(emu:read32(images + S.FRAME_IMAGE_SIZE), S.PIC_BYTES),
               name .. " decompresses distinct front frames")
      L.wait(8)
      local tag = name:lower() .. (shiny == 1 and "_shiny" or "_normal")
      expect_copied_frame(front, 0, tag .. " front0")
      expect_copied_frame(back, 0, tag .. " back")
      L.shot(tag .. "_front0_back")
      L.setVar(S.VAR_0x8002, S.SPRITE_SIZE)
      L.runHeader("AktiArt_FrameHeader")
      L.wait(8)
      L.expect(emu:read8(sprite(front) + S.OFF_SPRITE_ANIM_NUM) == 1,
               name .. " starts front frame1 through the engine")
      expect_copied_frame(front, 1, tag .. " front1")
      expect_copied_frame(back, 0, tag .. " retained back")
      L.shot(tag .. "_front1_back")
      L.runHeader("AktiArt_FreeMonHeader")
    end
  end
  for _, name in ipairs({
    "SHEPHERD", "HARVESTER", "GOATHERD", "HOPLITE", "AUGUR", "ACOLYTE_M", "ACOLYTE_F",
    "POTTER", "INITIATE_F", "RUNNER",
  }) do
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
