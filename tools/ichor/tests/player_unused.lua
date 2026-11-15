-- Only the real graphics IDs, image/animation tables and live palettes.
-- These unused states are forced fixtures, never claims of gameplay eligibility.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, emu = L.S, L.emu

local function frame(sprite)
    local anim = emu:read8(sprite + S.OFF_SPRITE_ANIM_NUM)
    local cmd = emu:read8(sprite + S.OFF_SPRITE_ANIM_CMD)
    local seq = emu:read32(emu:read32(sprite + S.OFF_SPRITE_ANIMS) + anim * 4)
    return emu:read16(seq + cmd * 4)
end

local function verify(sprite, value, size, female, mirrored, tag)
    local images = emu:read32(sprite + S.OFF_SPRITE_IMAGES)
    local image = images + value * S.FRAME_IMAGE_SIZE
    local data = emu:read32(image + S.OFF_FRAME_IMAGE_DATA)
    L.expect(emu:read16(image + S.OFF_FRAME_IMAGE_SIZE) == size, tag .. " frame size")
    local attr2 = emu:read16(sprite + 4)
    local vram = 0x06010000 + (attr2 & 0x3FF) * 32
    L.expect(L.snapshot(vram, size) == L.snapshot(data, size),
             tag .. " exact complete OBJ VRAM transfer")
    local palette = female and S.gObjectEventPal_May or S.gObjectEventPal_Brendan
    L.expect(L.snapshot(S.gPlttBufferUnfaded + (256 + (attr2 >> 12) * 16) * 2, 32)
             == L.snapshot(palette, 32), tag .. " all sixteen live palette words")
    L.expect((emu:read16(sprite + 2) & 0x1000 ~= 0) == mirrored,
             tag .. " correct east-facing hardware mirror")
end

L.start(function()
    L.quickstart()
    L.log("NOTE TEST_ONLY: unused watering/decorating state fixtures; no controller changes")
    for _, gender in ipairs({"THEO", "IANTHE"}) do
        for _, state in ipairs({"WATER", "DECOR"}) do
            local limit = state == "WATER" and 7 or 0
            for anim = 0, limit do
                local tag = gender:lower() .. "_" .. state:lower() .. "_anim" .. anim
                local gfx = S["GFX_" .. gender .. "_" .. state]
                L.setVar(S.VAR_0x8000, gfx)
                L.setVar(S.VAR_0x8001, anim)
                L.runHeader("ElaiaEffects_StateHeader", {noSettle = true})
                local id = L.getVar(S.VAR_0x8005)
                L.expect(id < S.SPRITE_LIMIT, tag .. " allocated real object")
                local object = S.gObjectEvents + L.getVar(S.VAR_0x8006) * S.OBJECT_EVENT_SIZE
                L.expect(emu:read16(object + S.OFF_OBJ_GRAPHICS_ID) == gfx,
                         tag .. " requested graphics ID")
                L.expect(L.getVar(S.VAR_0x8007)
                         == (gender == "IANTHE" and S.PAL_IANTHE or S.PAL_THEO),
                         tag .. " correct dynamically allocated palette tag")
                local sprite = S.gSprites + id * S.SPRITE_SIZE
                local seen, count = {}, 0
                for tick = 1, state == "WATER" and 60 or 8 do
                    L.frame()
                    local value = frame(sprite)
                    if value < 0xFFFD and not seen[value] then
                        -- Sprite image copies complete at VBlank, not StartSpriteAnim.
                        L.wait(2)
                        L.expect(frame(sprite) == value, tag .. " stable rendered frame")
                        verify(sprite, value, state == "WATER" and 512 or 256,
                               gender == "IANTHE", anim == 3 or anim == 7, tag)
                        L.shot(tag .. "_frame" .. value)
                        seen[value], count = true, count + 1
                    end
                end
                L.expect(count == (anim < 4 and 1 or 3), tag .. " all declared animation frames")
                L.setVar(S.VAR_0x8002, 1)
                L.runHeader("ElaiaEffects_FreeHeader")
            end
        end
    end
end)
