-- Matching native sprite review shots, without progressing the town story.
-- mkdir -p build/akti_sprites && build/tools/ichor-mgba-headless \
--   --script tools/ichor/tests/akti_sprites.lua --frames 7000 \
--   --until "AKTI_SPRITES done" pokeemerald.gba
-- SPRITE_OUT selects an existing output directory.
local L = dofile("tools/ichor/tests/ichor_lib.lua")
local OUT = os.getenv("SPRITE_OUT") or "build/akti_sprites/"
local places = {
    {"MAP_KALLISTE_ROUTE1", "route1", 12, 2},
    {"MAP_KALLISTE_ROUTE1_KRONION_HILL", "kronion_cast", 9, 10},
    {"MAP_AKTI_TOWN", "akti_boat", 8, 27},
    {"MAP_AKTI_TOWN", "akti_sailor", 7, 11},
    {"MAP_AKTI_TOWN", "akti_diver", 25, 8},
    {"MAP_AKTI_TOWN_TEMPLE_OF_HESTIA", "temple", 8, 6},
    {"MAP_AKTI_TOWN_ASCLEPEION", "asclepeion", 6, 5},
    {"MAP_AKTI_TOWN_AGORA", "agora", 5, 5},
    {"MAP_AKTI_TOWN_FISHERS_HOUSE", "fishers_house", 4, 5},
    {"MAP_AKTI_TOWN_DIVERS_HOUSE", "divers_house", 4, 5},
    {"MAP_AKTI_TOWN_GOATHERDS_HOUSE", "goatherds_house", 4, 5},
}
local steps = L.quickstart()
for _, place in ipairs(places) do
    local group, number = L.map(place[1])
    table.insert(steps, {warp = {group, number, -1, place[3], place[4]}, wait = 240})
    table.insert(steps, {check = function()
        local sb = L.sb1()
        local g, n = emu:read8(sb + 4), emu:read8(sb + 5)
        return g == group and n == number,
            string.format("%s loaded %d.%d, expected %d.%d", place[2], g, n, group, number)
    end})
    table.insert(steps, {shot = place[2] .. ".png"})
end
L.run("AKTI_SPRITES", OUT, steps)
