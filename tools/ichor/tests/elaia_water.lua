-- Forced actual-ROM mount and underwater state evidence, not relic eligibility.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, emu = L.S, L.emu
local function sprite(id) return S.gSprites + id * S.SPRITE_SIZE end
local function signed(value) return value >= 0x8000 and value - 0x10000 or value end
local function image(s)
    local anim = emu:read8(s + S.OFF_SPRITE_ANIM_NUM)
    local cmd = emu:read8(s + S.OFF_SPRITE_ANIM_CMD)
    local seq = emu:read32(emu:read32(s + S.OFF_SPRITE_ANIMS) + anim * 4)
    return emu:read16(seq + cmd * 4), anim
end
local function palette(s, address)
    local slot = emu:read16(s + 4) >> 12
    return L.snapshot(S.gPlttBufferUnfaded + (256 + slot * 16) * 2, 32)
           == L.snapshot(address, 32)
end
local function nativeTiles(s)
    local value = image(s)
    local table = emu:read32(s + S.OFF_SPRITE_IMAGES)
    local source
    if emu:read8(table + 6) ~= 0 then
        source = emu:read32(table) + value * emu:read16(table + 4)
    else
        source = emu:read32(table + value * 8)
    end
    local tiles = 0x06010000 + (emu:read16(s + 4) & 0x3FF) * 32
    return L.snapshot(tiles, 512) == L.snapshot(source, 512)
end
local function start(gender, gfx, anim, direction)
    L.setVar(0x8000, gfx)
    L.setVar(0x8001, anim)
    L.setVar(0x8003, gender)
    L.setVar(0x8004, direction)
    L.runHeader("ElaiaWater_StateHeader", {noSettle = true})
    local id, helper = L.getVar(0x8005), L.getVar(0x800B)
    L.expect(id < S.SPRITE_LIMIT and helper < S.SPRITE_LIMIT, "state and native helper allocated")
    local s = sprite(id)
    local object = S.gObjectEvents + L.getVar(0x8006) * S.OBJECT_EVENT_SIZE
    L.expect(emu:read16(object + S.OFF_OBJ_GRAPHICS_ID) == gfx, "actual graphics ID bound")
    return s, sprite(helper)
end
local function capture(s, helper, label, anim, underwater, gender, direction)
    L.wait(2) -- Finish the queued OBJ tile copy before the first screenshot.
    local seen, low, high, count = {}, 100, -100, 0
    local paletteTag = underwater and S.PAL_UNDERWATER or (gender == 0 and S.PAL_THEO or S.PAL_IANTHE)
    local paletteAddress = underwater and S.gObjectEventPal_PlayerUnderwater
                           or (gender == 0 and S.gObjectEventPal_Brendan or S.gObjectEventPal_May)
    L.expect(L.getVar(0x8007) == paletteTag, "actual dynamically allocated state palette tag")
    L.expect(palette(s, paletteAddress), "matching live state palette bytes")
    if not underwater then
        L.expect(L.getVar(0x800A) == paletteTag, "dolphin palette follows the requested gender")
        L.expect(palette(helper, paletteAddress), "matching live dolphin palette bytes")
    else
        L.expect(emu:read32(helper + S.OFF_SPRITE_CALLBACK) == (S.SpriteCB_UnderwaterSurfBlob | 1),
                 "native underwater bob callback")
        L.expect(emu:read8(helper + S.OFF_SPRITE_FLAGS) & 4 ~= 0,
                 "underwater bob helper is invisible")
        L.expect(emu:read16(helper + S.OFF_SPRITE_DATA) == L.getVar(0x8005),
                 "underwater helper tracks the requested swimmer")
    end
    for frame = 1, 64 do
        L.frame()
        local value, actualAnim = image(s)
        L.expect(actualAnim == anim, "selected state animation retained")
        local y2 = signed(emu:read16(s + S.OFF_SPRITE_Y2))
        low, high = math.min(low, y2), math.max(high, y2)
        if frame == 32 then
            L.expect(nativeTiles(s), "state VRAM tiles match its selected native ROM frame")
            if not underwater then
                L.expect(nativeTiles(helper), "dolphin VRAM tiles match its selected native ROM frame")
            end
        end
        if not underwater then
            L.expect(emu:read32(helper + S.OFF_SPRITE_CALLBACK) == (S.UpdateSurfBlobFieldEffect | 1),
                     "native mount tracking callback")
            L.expect(emu:read8(helper + S.OFF_SPRITE_ANIM_NUM) == direction - 1, "native direction synchronization")
            local mountFrame = image(helper)
            local mountTable = emu:read32(helper + S.OFF_SPRITE_IMAGES)
            L.expect(emu:read32(mountTable) == S.gFieldEffectObjectPic_SurfBlob
                     and emu:read16(mountTable + 4) == 512
                     and emu:read8(mountTable + 6) == 1
                     and mountFrame == (direction == 4 and 2 or direction - 1),
                     "mount binds its native relative-frame ROM table")
            L.expect(emu:read16(helper + S.OFF_SPRITE_X) == emu:read16(s + S.OFF_SPRITE_X)
                     and emu:read16(helper + S.OFF_SPRITE_Y) == emu:read16(s + S.OFF_SPRITE_Y) + 8
                     and emu:read16(helper + S.OFF_SPRITE_Y2) == emu:read16(s + S.OFF_SPRITE_Y2),
                     "unchanged rider/mount anchors and shared bob")
        end
        if value < 0xFFFD then
            local table = emu:read32(s + S.OFF_SPRITE_IMAGES)
            local pixels = emu:read32(table + value * 8)
            if underwater then
                local base = gender == 0 and S.gObjectEventPic_BrendanUnderwater or S.gObjectEventPic_MayUnderwater
                L.expect(pixels == base or pixels == base + 512 or pixels == base + 1024,
                         "underwater logical slots alias the three ROM frames")
            end
            local key = value .. ":" .. y2
            if not seen[key] and (frame % 4 == 0 or frame == 1) then
                seen[key] = true
                count = count + 1
                L.shot(label .. "_image" .. value .. "_bob" .. y2)
            end
        end
    end
    L.expect(high > low, "native bob movement observed")
    L.expect(count > 0, "rendered state evidence captured")
    if not underwater and anim >= S.ANIM_SURF_TRANSITION then
        local seq = emu:read32(emu:read32(s + S.OFF_SPRITE_ANIMS) + anim * 4)
        L.expect(emu:read16(seq + 4) == 0xFFFE and emu:read16(seq + 6) == 0,
                 "native get-on/off pose retains its controller-held loop")
    end
end
L.start(function()
    L.quickstart()
    L.runHeader("ElaiaWater_SetupHeader")
    L.wait(40)
    L.log("NOTE forced Route1 state fixtures: no production map edits or early Surf/Dive eligibility")
    for gender = 0, 1 do
        local name = gender == 0 and "theo" or "ianthe"
        for _, base in ipairs({0, 4, S.ANIM_SURF_TRANSITION}) do
            for direction = 1, 4 do
                local anim = base + direction - 1
                local gfx = gender == 0 and S.GFX_THEO_SURF or S.GFX_IANTHE_SURF
                local s, mount = start(gender, gfx, anim, direction)
                capture(s, mount, "engine_mount_" .. name .. "_anim" .. anim, anim, false, gender, direction)
                L.runHeader("ElaiaWater_FreeHeader")
            end
        end
        for anim = 0, 19 do
            local direction = anim % 4 + 1
            local gfx = gender == 0 and S.GFX_THEO_UNDERWATER or S.GFX_IANTHE_UNDERWATER
            local s, helper = start(gender, gfx, anim, direction)
            capture(s, helper, "engine_underwater_" .. name .. "_anim" .. anim, anim, true, gender, direction)
            L.runHeader("ElaiaWater_FreeHeader")
        end
    end
end)
