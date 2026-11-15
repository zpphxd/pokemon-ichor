local L = dofile("tools/ichor/tests/ichor_lib.lua")
local OUT = assert(os.getenv("BOW_OUT"))
local S = {}
local file = assert(io.open(assert(os.getenv("HEAL_SYMBOLS"))))
for line in file:lines() do
    local address, name = line:match("^(%x+)%s+%a%s+(%S+)")
    if address then S[name] = tonumber(address, 16) end
end
file:close()
for _, name in ipairs({
    "gSprites", "SpriteCB_PokecenterMonitor", "SpriteCB_PokeballGlow",
    "gFieldEffectObjectPalette0", "gSpritePalette_PokeballGlow",
    "gPlttBufferUnfaded", "gPlttBufferFaded",
}) do
    assert(S[name], "missing healing symbol " .. name)
end

local commands, orbSeen, errors, run = {}, false, {}, 1
local function expect(ok, description)
    if not ok then errors[description] = true end
end

local function palette_matches(sprite, source)
    local slot = emu:read16(sprite + 4) >> 12
    local palette = S.gPlttBufferUnfaded + (256 + slot * 16) * 2
    for i = 0, 15 do
        expect(emu:read16(palette + i * 2) == emu:read16(source + i * 2),
            "live healing palette differs from its ROM source")
    end
    return slot
end

callbacks:add("frame", function()
    for i = 0, 63 do
        local sprite = S.gSprites + i * 0x44
        local flags = emu:read8(sprite + 0x3E)
        if flags & 1 == 1 then
            local callback = emu:read32(sprite + 0x1C) & 0xFFFFFFFE
            if callback == S.SpriteCB_PokecenterMonitor & 0xFFFFFFFE then
                palette_matches(sprite, S.gFieldEffectObjectPalette0)
                expect(emu:read16(sprite + 0x20) == 124
                    and emu:read16(sprite + 0x22) == 24, "relief registration moved")
                local command = emu:read8(sprite + 0x2B)
                if flags & 4 == 0 and emu:read8(sprite + 0x2C) & 63 == 2
                    and not commands[command] then
                    commands[command] = true
                    emu:screenshot(OUT .. string.format("heal_%d_%d.png", run, command))
                end
            elseif callback == S.SpriteCB_PokeballGlow & 0xFFFFFFFE then
                orbSeen = true
                local source = emu:read32(S.gSpritePalette_PokeballGlow)
                local slot = palette_matches(sprite, source)
                for _, index in ipairs({12, 13}) do
                    expect(emu:read16(S.gPlttBufferFaded + (256 + slot * 16 + index) * 2)
                        == emu:read16(source + index * 2), "waterline flashed with the orb")
                end
            end
        end
    end
end)

local M = {}
function M.prepare_player()
    -- SaveBlock2 offsets from include/global.h; THEO bytes from charmap.txt.
    local save = emu:read32(assert(L.SB2))
    local name = {0xCE, 0xC2, 0xBF, 0xC9, 0xFF, 0xFF, 0xFF, 0xFF}
    for index, value in ipairs(name) do emu:write8(save + index - 1, value) end
    emu:write8(save + 0x08, 0)
    local matches = emu:read8(save + 0x08) == 0
    for index, value in ipairs(name) do
        matches = matches and emu:read8(save + index - 1) == value
    end
    return matches, "deterministic Theo name/gender before the clinic warp"
end

function M.validate(phase)
    expect(orbSeen, "healing orb never rendered")
    for command = 0, 7 do
        expect(commands[command], "missing relief command " .. command)
    end
    for i = 0, 63 do
        local sprite = S.gSprites + i * 0x44
        local callback = emu:read32(sprite + 0x1C) & 0xFFFFFFFE
        expect(emu:read8(sprite + 0x3E) & 1 == 0
            or (callback ~= S.SpriteCB_PokecenterMonitor & 0xFFFFFFFE
                and callback ~= S.SpriteCB_PokeballGlow & 0xFFFFFFFE),
            "healing sprite survived completion")
    end
    local ok = next(errors) == nil
    if ok then
        console:log("HEAL " .. phase .. ": eight relief commands, live palettes, stable waterline and cleanup pass")
    else
        for message in pairs(errors) do console:log("HEAL FAIL " .. phase .. ": " .. message) end
    end
    commands, orbSeen, errors, run = {}, false, {}, run + 1
    return ok
end
return M
