-- Real loaders/palettes and full image-table copies; test-only forced frames.
-- Sam/Cami's two unrouted dialogue portraits are deliberately not ROM claims.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, emu = L.S, L.emu
local folk = {AIAKIDES=true, ENDEIS=true, KEDALION=true, MOM=true, PHEIDON=true, PRONOMOS=true}
local gods = {SAM=true, APOLLO=true, CAMI=true, DEMETER=true}
local names = {"AIAKIDES", "ALETHEA", "APOLLO", "CAMI", "DEMETER", "ENDEIS",
               "KEDALION", "KERYKOS", "KLEON", "KLEON_SEASICK", "KLEON_TABLET",
               "MOM", "PHEIDON", "PROFESSOR_DAPHNE", "PRONOMOS", "SAM",
               "HIEROPHANT_IONE", "TITAN_GRUNT"}
local portraits = {"ALETHEA", "HIEROPHANT_IONE", "HIEROPHANT_KERYKOS",
                   "KLEON", "PROFESSOR_DAPHNE", "TITAN_GRUNT"}

local function dump(path, address, size)
    local file = assert(io.open(L.OUT .. path, "wb"))
    local bytes = {}
    for i = 0, size - 1 do bytes[#bytes + 1] = string.char(emu:read8(address + i)) end
    file:write(table.concat(bytes))
    file:close()
end

local function render(name, kind, count)
    local tag = name:lower() .. (kind == 0 and "_walk" or kind == 1 and "_front" or "_back")
    L.setVar(S.VAR_0x8000, S[(kind == 0 and "GFX_" or "PIC_") .. name])
    L.setVar(S.VAR_0x8001, kind)
    L.runHeader("NamedCast_OpenHeader")
    local id = L.getVar(S.VAR_0x8005)
    L.expect(id < S.SPRITE_LIMIT, tag .. " real graphics ID allocated")
    if id >= S.SPRITE_LIMIT then L.fail(tag .. " allocation failed") end
    local sprite = S.gSprites + id * S.SPRITE_SIZE
    local paletteSource
    if kind == 0 then
        local family = folk[name] and "Folk" or gods[name] and "Theoxenia" or "Cast"
        paletteSource = assert(S["gObjectEventPal_Ichor" .. family])
        L.expect(L.getVar(S.VAR_0x800A) == S["PAL_" .. family:upper()],
                 tag .. " actual shared palette tag")
    else
        local info = emu:read32(S.gTrainerPicInfo + S["PIC_" .. name] * S.TRAINER_INFO_SIZE
                              + (kind == 1 and S.OFF_TRAINER_FRONT or S.OFF_TRAINER_BACK))
        paletteSource = emu:read32(info + (kind == 1 and S.OFF_FRONT_PALETTE or S.OFF_BACK_PALETTE))
    end
    local images = emu:read32(sprite + S.OFF_SPRITE_IMAGES)
    for frame = 0, count - 1 do
        for mirror = 0, (kind == 0 and (frame == 2 or frame == 7 or frame == 8)) and 1 or 0 do
            L.setVar(S.VAR_0x8002, frame)
            L.setVar(S.VAR_0x8003, mirror)
            L.runHeader("NamedCast_FrameHeader")
            L.wait(3)
            local label = tag .. "_frame" .. frame .. (mirror == 1 and "_east" or "")
            local size = kind == 0 and 256 or 2048
            local relative = emu:read8(images + S.OFF_FRAME_IMAGE_RELATIVE) ~= 0
            local image = images + (relative and 0 or frame * S.FRAME_IMAGE_SIZE)
            local source = emu:read32(image + S.OFF_FRAME_IMAGE_DATA) + (relative and frame * size or 0)
            local attr2 = emu:read16(sprite + 4)
            local vram = 0x06010000 + (attr2 & 0x3FF) * 32
            local palette = S.gPlttBufferUnfaded + (256 + (attr2 >> 12) * 16) * 2
            local hardwarePalette = 0x05000200 + (attr2 >> 12) * 32
            L.expect(L.getVar(S.VAR_0x8007) == size, label .. " native image size")
            L.expect(L.snapshot(vram, size) == L.snapshot(source, size), label .. " full OBJ VRAM copy")
            L.expect(L.snapshot(palette, 32) == L.snapshot(paletteSource, 32)
                     and L.snapshot(hardwarePalette, 32) == L.snapshot(paletteSource, 32),
                     label .. " all sixteen actual ROM palette words")
            L.expect((emu:read16(sprite + 2) & 0x1000 ~= 0) == (mirror == 1), label .. " hardware mirror")
            L.shot(label)
            if mirror == 0 then
                dump(label .. ".4bpp", vram, size)
                dump(label .. ".gbapal", palette, 32)
            end
        end
    end
    L.runHeader("NamedCast_FreeHeader")
end

L.start(function()
    L.quickstart()
    L.log("NOTE TEST_ONLY: real named graphics IDs and palettes, forced source frames/east mirrors")
    for _, name in ipairs(names) do
        render(name, 0, (name == "SAM" or name == "APOLLO") and 12 or name == "CAMI" and 11 or 9)
    end
    for _, name in ipairs(portraits) do render(name, 1, 1) end
    for _, name in ipairs({"KLEON", "ALETHEA"}) do render(name, 2, 4) end
end)
