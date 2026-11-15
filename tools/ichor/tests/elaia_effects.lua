-- Real input-triggered grass, owner-attached APIs, and forced state-table
-- fixtures. The latter do not prove that late relics are available in Elaia.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, emu = L.S, L.emu

local function sprite(id) return S.gSprites + id * S.SPRITE_SIZE end
local function callback(s) return emu:read32(s + S.OFF_SPRITE_CALLBACK) end
local function findCallback(name, moving)
    for id = 0, S.SPRITE_LIMIT - 1 do
        local s = sprite(id)
        if callback(s) == (S[name] | 1)
           and emu:read8(s + S.OFF_SPRITE_FLAGS) & 1 == 1
           and (not moving or emu:read8(s + S.OFF_SPRITE_FLAGS + 1) & 0x10 == 0)
           and (name ~= "UpdateTallGrassFieldEffect"
                or emu:read16(s + S.OFF_SPRITE_DATA + 6) >> 8 == 0xFF) then
            return id
        end
    end
end
local function shown(s)
    local num = emu:read8(s + S.OFF_SPRITE_ANIM_NUM)
    local cmd = emu:read8(s + S.OFF_SPRITE_ANIM_CMD)
    local seq = emu:read32(emu:read32(s + S.OFF_SPRITE_ANIMS) + num * 4)
    return emu:read16(seq + cmd * 4), num, seq
end
local function expected(seq)
    local order = {}
    for cmd = 0, 99 do
        local value = emu:read16(seq + cmd * 4)
        if value == 0xFFFD then
            local repeats = emu:read16(seq + cmd * 4 + 2)
            local length = #order
            for repeatIndex = 1, repeats do
                for i = 1, length do order[#order + 1] = order[i] end
            end
        elseif value >= 0xFFFE then
            return order, value == 0xFFFE
        elseif order[#order] ~= value then
            order[#order + 1] = value
        end
    end
    L.fail("unbounded animation table")
end
local function capture(id, tag, checkEnd)
    local s = sprite(id)
    local first, anim, seq = shown(s)
    local want, looping = expected(seq)
    local order, last, due = {}, nil, nil
    local cb = callback(s)
    local shots = 0
    for f = 0, 250 do
        if callback(s) ~= cb or emu:read8(s + S.OFF_SPRITE_FLAGS) & 1 == 0 then break end
        local value, num = shown(s)
        if num ~= anim then L.fail(tag .. " unexpectedly changed animation") end
        if value < 0xFFFD and value ~= last then
            order[#order + 1] = value
            last = value
            due = f + 2
        end
        if f == due then
            shots = shots + 1
            L.shot(tag .. "_frame" .. value .. "_" .. shots)
        end
        if looping and #order >= #want and shots >= #want then break end
        if #order >= #want and f > 100 then break end
        L.frame()
    end
    L.expect(table.concat(order, ",") == table.concat(want, ","),
             tag .. " sequence " .. table.concat(want, ",") .. "; got " .. table.concat(order, ","))
    L.expect(shots > 0, tag .. " rendered capture")
    L.expect(emu:read8(s + S.OFF_SPRITE_ANIM_NUM) == anim or callback(s) ~= cb,
             tag .. " retains the requested animation")
    if checkEnd and not looping then
        L.runHeader("ElaiaEffects_InspectHeader", { noSettle = true })
        L.expect(L.getVar(0x800A) == 1,
                 tag .. " reaches animation end")
    end
end
local function start(effect, anim, header)
    L.setVar(S.VAR_0x8000, effect)
    L.setVar(S.VAR_0x8001, anim or 0)
    L.runHeader(header or "ElaiaEffects_StartHeader", { noSettle = true })
    local id = L.getVar(S.VAR_0x8005)
    L.expect(id < S.SPRITE_LIMIT, "field/state fixture allocated a sprite")
    if header == "ElaiaEffects_StateHeader" then
        local object = S.gObjectEvents + L.getVar(S.VAR_0x8006) * S.OBJECT_EVENT_SIZE
        L.expect(emu:read16(object + S.OFF_OBJ_GRAPHICS_ID) == effect,
                 "state uses the requested native graphics ID")
        local slot = emu:read16(sprite(id) + 4) >> 12
        local female = effect == S.GFX_IANTHE_FISH or effect == S.GFX_IANTHE_SURF or effect == S.GFX_IANTHE_RELIC
        L.expect(L.getVar(S.VAR_0x8007) == (female and S.PAL_IANTHE or S.PAL_THEO),
                 "state binds its actual dynamically allocated player palette tag")
        local palette = female and S.gObjectEventPal_May or S.gObjectEventPal_Brendan
        L.expect(L.snapshot(S.gPlttBufferUnfaded + (256 + slot * 16) * 2, 32)
                 == L.snapshot(palette, 32), "state loads its matching ROM palette")
    end
    return id
end
local function free(state)
    L.setVar(S.VAR_0x8002, state and 1 or 0)
    L.runHeader("ElaiaEffects_FreeHeader")
end

L.start(function()
    L.quickstart()
    for flag = S.TRAINER_FLAGS_START, S.TRAINER_FLAGS_END do L.setFlag(flag) end
    L.runHeader("ElaiaEffects_SetupHeader")
    L.waitUntil(function() local x, y = L.pos() return x == 10 and y == 39 and L.idle() end,
                2000, "Route1's unmodified grass approach")
    L.wait(40) -- Let map-entry and follower palette fades finish before capture.
    L.log("NOTE gameplay grass uses actual Route1 terrain; no production layout edits")
    emu:addKey(L.K.RIGHT)
    L.waitUntil(function() return findCallback("UpdateTallGrassFieldEffect", true) ~= nil end,
                60, "input-triggered tall grass")
    emu:clearKey(L.K.RIGHT)
    local grass = findCallback("UpdateTallGrassFieldEffect", true)
    L.setVar(S.VAR_0x8005, grass)
    capture(grass, "gameplay_tall_grass")
    L.settle()
    L.go(13, 41)
    L.wait(40)
    L.expect(findCallback("UpdateTallGrassFieldEffect") == nil, "grass cleans up after walking away")
    L.shot("gameplay_grass_exit")

    L.log("NOTE following captures are explicitly forced engine API/state fixtures")
    for _, entry in ipairs({
        {"exclamation", S.EFFECT_EXCLAMATION, 0},
        {"question", S.EFFECT_QUESTION, -1},
        {"double_exclamation", S.EFFECT_DOUBLE, 0},
        {"x", S.EFFECT_X, 0}, {"heart", S.EFFECT_HEART, 0},
    }) do
        local id = start(entry[2], entry[3])
        L.expect(callback(sprite(id)) == (S.SpriteCB_TrainerIcons | 1),
                 entry[1] .. " uses real owner-tracking callback")
        L.expect(emu:read16(sprite(id) + S.OFF_SPRITE_DATA) == 0xFF,
                 entry[1] .. " attaches to the player owner")
        capture(id, "engine_field_" .. entry[1])
        L.wait(60)
        L.expect(callback(sprite(id)) ~= (S.SpriteCB_TrainerIcons | 1),
                 entry[1] .. " deletes after its animation")
    end
    local emotions = {"happy", "neutral", "sad", "upset", "angry", "pensive",
                      "love", "surprise", "curious", "music", "poisoned"}
    L.runHeader("ElaiaEffects_FollowerHeader")
    L.expect(L.getVar(S.VAR_0x8005) < S.SPRITE_LIMIT, "actual Nebrel follower is visible")
    L.log("NOTE emotion indices are forced on the actual follower, not selected by dialogue")
    for index, name in ipairs(emotions) do
        local id = start(S.EFFECT_QUESTION, index - 1)
        L.expect(emu:read16(sprite(id) + S.OFF_SPRITE_DATA) == 0xFE,
                 name .. " emotion attaches to its Pokemon owner")
        capture(id, "engine_follower_emotion_" .. name)
        L.wait(60)
        L.expect(callback(sprite(id)) ~= (S.SpriteCB_TrainerIcons | 1),
                 name .. " emotion cleans up")
    end
    L.setVar(S.VAR_0x8002, 2)
    L.runHeader("ElaiaEffects_FreeHeader")
    for dir = 1, 4 do
        local id = start(0, dir, "ElaiaEffects_ArrowHeader")
        local owner = sprite(emu:read8(L.playerObject() + S.OFF_OBJ_SPRITE_ID))
        L.expect(emu:read16(sprite(id) + 0x20) == emu:read16(owner + 0x20) + 16,
                 "warp arrow is visibly adjacent in the engine's offset map coordinates")
        L.expect(emu:read8(sprite(id) + S.OFF_SPRITE_FLAGS) & 4 == 0,
                 "warp arrow is not hidden")
        capture(id, "engine_warp_direction" .. dir)
        free()
    end
    for size = 0, 3 do
        local id = start(S.EFFECT_SHADOW, size, "ElaiaEffects_ShadowHeader")
        L.wait(5)
        L.expect(callback(sprite(id)) == (S.UpdateShadowFieldEffect | 1),
                 "shadow template " .. size .. " tracks its real owner")
        L.expect((emu:read16(sprite(id)) >> 10) & 3 == 1, "shadow uses hardware OBJ blend")
        L.expect(L.getVar(S.VAR_0x8007) == S.PAL_SHADOW, "shadow uses the actual weather palette")
        local slot = emu:read16(sprite(id) + 4) >> 12
        L.expect(emu:read16(S.gPlttBufferUnfaded + (256 + slot * 16 + 9) * 2) == 0,
                 "shadow index 9 is hardware black")
        L.shot("engine_shadow_size" .. size)
        free()
    end
    for anim = 0, 1 do
        local id = start(S.EFFECT_SAND, anim)
        capture(id, "engine_sandal_direction" .. anim)
        free()
    end
    for _, entry in ipairs({{"jump_tall", S.EFFECT_JUMP_TALL},
                            {"jump_long", S.EFFECT_JUMP_LONG}}) do
        local id = start(entry[2])
        capture(id, "engine_" .. entry[1])
        L.wait(60)
    end
    L.log("NOTE reed capture temporarily changes only one live RAM metatile")
    L.setVar(S.VAR_0x8000, 0x3015)
    L.runHeader("ElaiaEffects_TerrainHeader")
    local terrain = L.getVar(S.VAR_0x8007)
    local reeds = start(S.EFFECT_LONG)
    capture(reeds, "engine_RAM_reed_rustle")
    free()
    L.setVar(S.VAR_0x8000, terrain)
    L.runHeader("ElaiaEffects_TerrainHeader")
    for _, gender in ipairs({"THEO", "IANTHE"}) do
        for anim = 0, 11 do
            local id = start(S["GFX_" .. gender .. "_FISH"], anim, "ElaiaEffects_StateHeader")
            capture(id, "engine_" .. gender:lower() .. "_fish" .. anim, true)
            free(true)
        end
        for _, base in ipairs({0, 4, S.ANIM_SURF_TRANSITION}) do
            for dir = 0, 3 do
                local id = start(S["GFX_" .. gender .. "_SURF"], base + dir, "ElaiaEffects_StateHeader")
                capture(id, "engine_" .. gender:lower() .. "_surf" .. (base + dir), true)
                free(true)
            end
        end
        local id = start(S["GFX_" .. gender .. "_RELIC"], 0, "ElaiaEffects_StateHeader")
        capture(id, "engine_" .. gender:lower() .. "_relic", true)
        free(true)
    end
end)
