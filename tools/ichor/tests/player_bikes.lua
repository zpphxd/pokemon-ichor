-- Real retained bike atlases/tables in ROM; only NPC renderer states are forced.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, emu = L.S, L.emu
local FACE, WALK = {0, 1, 2, 2}, {3, 5, 7, 7}
local STUNTS = {
    {9, 10}, {13, 14}, {17, 18}, {17, 18},
    {11, 12}, {15, 16}, {19, 20}, {19, 20},
    {9, 0}, {13, 1}, {17, 2}, {17, 2},
    {11, 0}, {15, 1}, {19, 2}, {19, 2},
    {21, 10, 22, 10}, {23, 14, 24, 14},
    {25, 18, 26, 18}, {25, 18, 26, 18},
}

local function contract(anim)
    local direction = anim % 4 + 1
    if anim < 4 then return {FACE[direction]}, 16, false end
    if anim < S.ANIM_STD_COUNT then
        return {WALK[direction], FACE[direction], WALK[direction] + 1, FACE[direction]},
               ({8, 4, 2, 1})[anim // 4], false
    end
    return STUNTS[anim - S.ANIM_STD_COUNT + 1], 4, anim < S.ANIM_STD_COUNT + 16
end

local function value(sprite)
    local anim = emu:read8(sprite + S.OFF_SPRITE_ANIM_NUM)
    local cmd = emu:read8(sprite + S.OFF_SPRITE_ANIM_CMD)
    local seq = emu:read32(emu:read32(sprite + S.OFF_SPRITE_ANIMS) + anim * 4)
    return emu:read16(seq + cmd * 4), cmd, seq
end

local function verify(sprite, expected, female, mirror, source, tag)
    local images = emu:read32(sprite + S.OFF_SPRITE_IMAGES)
    L.expect(emu:read32(images) == source and emu:read16(images + 4) == 512
             and emu:read8(images + 6) == 1, tag .. " native relative-frame table")
    local attr2 = emu:read16(sprite + 4)
    local vram = 0x06010000 + (attr2 & 0x3FF) * 32
    L.expect(L.snapshot(vram, 512) == L.snapshot(source + expected * 512, 512),
             tag .. " complete 32x32 native OBJ VRAM transfer")
    local palette = female and S.gObjectEventPal_May or S.gObjectEventPal_Brendan
    L.expect(L.snapshot(S.gPlttBufferUnfaded + (256 + (attr2 >> 12) * 16) * 2, 32)
             == L.snapshot(palette, 32), tag .. " all sixteen live palette words")
    L.expect((emu:read16(sprite + 2) & 0x1000 ~= 0) == mirror,
             tag .. " east hardware mirror")
    L.expect(emu:read16(sprite + 2) & 0x2000 == 0, tag .. " no vertical mirror")
end

L.start(function()
    L.quickstart()
    L.runHeader("PlayerBikes_SetupHeader")
    L.log("NOTE TEST_ONLY: retained bike NPC renderer fixtures, not controller gameplay")
    local captures = 0
    for _, gender in ipairs({"THEO", "IANTHE"}) do
        for _, bike in ipairs({"MACH", "ACRO"}) do
            local female = gender == "IANTHE"
            local name = female and "May" or "Brendan"
            local source = S["gObjectEventPic_" .. name .. (bike == "MACH" and "MachBike" or "AcroBike")]
            for _, alias in ipairs({"", "RIVAL_"}) do
                local covered = {}
                for anim = 0, (bike == "MACH" and 19 or 39) do
                    local tag = alias:lower() .. gender:lower() .. "_" .. bike:lower() .. "_anim" .. anim
                    local gfx = S["GFX_" .. alias .. gender .. "_" .. bike]
                    L.setVar(S.VAR_0x8000, gfx)
                    L.setVar(S.VAR_0x8001, anim)
                    L.runHeader("ElaiaEffects_StateHeader", {noSettle = true})
                    local id = L.getVar(S.VAR_0x8005)
                    L.expect(id < S.SPRITE_LIMIT, tag .. " actual object allocated")
                    local sprite = S.gSprites + id * S.SPRITE_SIZE
                    local object = S.gObjectEvents + L.getVar(S.VAR_0x8006) * S.OBJECT_EVENT_SIZE
                    L.expect(emu:read16(object + S.OFF_OBJ_GRAPHICS_ID) == gfx, tag .. " graphics ID")
                    L.expect(L.getVar(S.VAR_0x8007) == (female and S.PAL_IANTHE or S.PAL_THEO),
                             tag .. " dynamically allocated palette tag")
                    local expected, duration, finite = contract(anim)
                    local seq = emu:read32(emu:read32(sprite + S.OFF_SPRITE_ANIMS) + anim * 4)
                    for phase, frame in ipairs(expected) do
                        local addr = seq + (phase - 1) * 4
                        L.expect(emu:read16(addr) == frame, tag .. " declared phase" .. phase)
                        local flags = emu:read16(addr + 2)
                        L.expect(flags & 63 == duration and (flags & 64 ~= 0) == (anim % 4 == 3)
                                 and flags & 128 == 0, tag .. " declared phase duration/mirror")
                    end
                    L.expect(emu:read16(seq + #expected * 4) == (finite and 0xFFFF or 0xFFFE),
                             tag .. " finite/loop table contract")
                    local seen, nextPhase, previous, cycle, pending = {}, 0, -1, false, nil
                    local initialFrame, initialCmd = value(sprite)
                    L.expect(initialCmd == 0 and initialFrame == expected[1],
                             tag .. " initial ordered phase0")
                    seen[0], covered[initialFrame] = true, true
                    nextPhase, previous, pending = 1, 0, {cmd = 0, frame = initialFrame}
                    -- Duration-one fastest movement must be observed at every VBlank;
                    -- delaying screenshots would skip its intermediate source frames.
                    for tick = 1, #expected * (duration + 1) * 3 + 8 do
                        L.frame()
                        -- Image copies queued by animation run after the observed
                        -- command; verify its pixels on the following VBlank.
                        if pending then
                            verify(sprite, pending.frame, female, anim % 4 == 3, source, tag)
                            local label = tag .. "_phase" .. pending.cmd .. "_frame" .. pending.frame
                            L.log("NOTE capture " .. label .. " "
                                  .. (emu:read16(sprite + 2) & 0x1FF) .. " "
                                  .. (emu:read16(sprite) & 0xFF))
                            L.shot(label)
                            captures = captures + 1
                            pending = nil
                        end
                        local frame, cmd = value(sprite)
                        if cmd < #expected and cmd ~= previous then
                            if nextPhase == #expected and cmd == 0 then cycle = true end
                            if not seen[cmd] then
                                L.expect(cmd == nextPhase and frame == expected[cmd + 1],
                                         tag .. " observed ordered phase" .. cmd)
                                pending = {cmd = cmd, frame = frame}
                                seen[cmd], covered[frame] = true, true
                                nextPhase = nextPhase + 1
                            end
                            previous = cmd
                        end
                    end
                    L.expect(nextPhase == #expected, tag .. " every declared phase rendered")
                    local ended = emu:read8(sprite + 0x3F) & 16 ~= 0
                    L.expect(finite and ended or not finite and not ended,
                             tag .. " finite completion versus loop")
                    if not finite and #expected > 1 then L.expect(cycle, tag .. " complete loop cycle") end
                    L.setVar(S.VAR_0x8002, 1)
                    L.runHeader("ElaiaEffects_FreeHeader")
                end
                local count = 0
                for _ in pairs(covered) do count = count + 1 end
                L.expect(count == (bike == "MACH" and 9 or 27),
                         alias .. gender .. bike .. " every source frame reached by native tables")
            end
        end
    end
    L.expect(captures == 736, "all 240 actual graphics/animation cases, 736 ordered phases")
end)
