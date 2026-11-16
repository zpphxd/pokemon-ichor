-- Forced picture-loader/table evidence, not natural battle/controller coverage.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, emu = L.S, L.emu

local function binary_snapshot(data)
    local result = {}
    for offset = 1, #data, 4 do
        result[#result + 1] = string.format("%08x", string.unpack("<I4", data, offset))
    end
    return table.concat(result)
end

local function source_tiles(folder, front)
    local path = "build/assets/graphics/trainers/" .. (front and "front_pics/" or "back_pics/")
                 .. folder .. ".png.4bpp"
    local file = assert(io.open(path, "rb"), "Missing built native source: " .. path)
    local data = file:read("a")
    file:close()
    assert(#data == S.PIC_BYTES * (front and 1 or 4), "Wrong built source size: " .. path)
    return data
end

local function verify(sprite, frame, expected, palette, tag)
    local images = emu:read32(sprite + S.OFF_SPRITE_IMAGES)
    local image = images + frame * S.FRAME_IMAGE_SIZE
    local source = emu:read32(image)
    local attr2 = emu:read16(sprite + 4)
    local vram = 0x06010000 + (attr2 & 0x3FF) * 32
    L.expect(emu:read16(image + 4) == S.PIC_BYTES, tag .. " native64 frame size")
    local data = binary_snapshot(expected:sub(frame * S.PIC_BYTES + 1, (frame + 1) * S.PIC_BYTES))
    L.expect(L.snapshot(source, S.PIC_BYTES) == data, tag .. " source pixels from real loader")
    L.expect(L.snapshot(vram, S.PIC_BYTES) == data, tag .. " full rendered OBJ VRAM")
    L.expect(L.snapshot(S.gPlttBufferUnfaded + (256 + (attr2 >> 12) * 16) * 2, 32)
             == L.snapshot(palette, 32), tag .. " all16 bound trainer palette words")
end

L.start(function()
    L.quickstart()
    L.log("NOTE TEST_ONLY: real front/back loaders and actual back animation tables")
    for _, who in ipairs({
        {name = "theo", folder = "brendan", pic = S.PIC_THEO,
         palette = S.gTrainerPalette_Brendan, back = S.gTrainerBackPic_Brendan},
        {name = "ianthe", folder = "may", pic = S.PIC_IANTHE,
         palette = S.gTrainerPalette_May, back = S.gTrainerBackPic_May},
    }) do
        for _, front in ipairs({true, false}) do
            local expected = source_tiles(who.folder, front)
            for anim = 0, front and 0 or 2 do
                L.setVar(S.VAR_0x8000, who.pic)
                L.setVar(S.VAR_0x8001, front and 1 or 0)
                L.setVar(S.VAR_0x8002, anim)
                L.runHeader("PlayerBattle_CreateHeader")
                local id = L.getVar(S.VAR_0x8005)
                L.expect(id < S.SPRITE_LIMIT, who.name .. " real picture allocated")
                if id >= S.SPRITE_LIMIT then L.fail("player picture allocation") end
                local sprite = S.gSprites + id * S.SPRITE_SIZE
                if front then
                    L.wait(3)
                    verify(sprite, 0, expected, who.palette, who.name .. "_front")
                    L.shot(who.name .. "_front")
                else
                    L.expect(L.snapshot(who.back, #expected) == binary_snapshot(expected),
                             who.name .. " all4 compiled back frames match canonical source")
                    local anims = emu:read32(sprite + S.OFF_SPRITE_ANIMS)
                    local seq = emu:read32(anims + anim * 4)
                    local order = anim == 0 and {3} or anim == 1 and {0, 1, 2, 0, 3}
                                  or {3, 0, 2, 2, 3}
                    local durations = anim == 0 and {0} or anim == 1 and {24, 9, 24, 9, 50}
                                      or {9, 9, 24, 24, 50}
                    for phase, value in ipairs(order) do
                        L.expect(emu:read16(seq + (phase - 1) * 4) == value,
                                 who.name .. " actual animation" .. anim .. " source order" .. phase)
                        L.expect(emu:read16(seq + (phase - 1) * 4 + 2) & 0x3F == durations[phase],
                                 who.name .. " actual animation" .. anim .. " duration" .. phase)
                    end
                    L.runHeader("PlayerBattle_StartHeader", {noSettle = true})
                    for phase, value in ipairs(order) do
                        if anim ~= 0 then
                            L.waitUntil(function()
                                return emu:read8(sprite + S.OFF_SPRITE_ANIM_CMD) == phase - 1
                            end, 100, "player back phase" .. phase)
                        end
                        L.wait(2)
                        local tag = who.name .. "_back_anim" .. anim .. "_phase" .. phase
                        verify(sprite, value, expected, who.palette, tag)
                        L.shot(tag)
                    end
                    L.wait(durations[#durations] + 3)
                    L.runHeader("PlayerBattle_InspectHeader")
                    L.expect(L.getVar(S.VAR_0x800A) == 1,
                             who.name .. " animation" .. anim .. " reaches real finite end")
                end
                L.runHeader("PlayerBattle_FreeHeader")
            end
        end
    end
end)
