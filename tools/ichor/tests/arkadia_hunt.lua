local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local T = "Arkadia_TempleOfArtemis_EventScript_"
for k, v in pairs(dofile(L.OUT .. "hunt_symbols.lua")) do S.SCRIPTS[k] = v end

local cached, danger = -1, {}
local function moon(x, y)
    return (x >= 4 and x <= 11 and y >= 23 and y <= 26)
        or (x >= 18 and x <= 25 and y >= 24 and y <= 29)
        or (x >= 21 and x <= 26 and y >= 8 and y <= 13)
end
-- A conservative walking policy, not a bypass: keep off both sides of each
-- live patrol and replan as it moves. The actual engine still catches mistakes.
local function avoid(x, y)
    if cached ~= L.now() then
        cached, danger = L.now(), {}
        if not L.getFlag(S.FLAG_TRIAL) then
            local stage = L.getVar(S.VAR_STAGE)
            for _, o in ipairs(L.mapEvents().objects) do
                if o.script == S.SCRIPTS[T .. "Hound"] then
                    local hx, hy = L.objectAt(o.localId)
                    local hs = o.y >= 36 and 0 or (o.y >= 22 and 1 or 2)
                    if hx and hs == stage then
                        for xx = 0, 29 do
                            if math.abs(xx - hx) <= (moon(xx, hy) and 7 or 4) then
                                danger[xx .. "," .. hy] = true
                            end
                        end
                    end
                end
            end
        end
    end
    return danger[x .. "," .. y] == true
end
local function talk(name, opts)
    opts = opts or {}
    opts.avoid = avoid
    L.talk(L.npc(T .. name), opts)
end
-- Controlled sight-boundary probes; restore before the ordinary key-play path.
local function sentry(localId, x, y)
    local target
    for i = 0, S.OBJECT_EVENTS_COUNT - 1 do
        local o = S.gObjectEvents + i * S.OBJECT_EVENT_SIZE
        local id = emu:read8(o + S.OFF_OBJ_LOCAL_ID)
        if emu:read8(o) & 1 == 1 and id >= 1 and id <= 7
            and emu:read8(o + S.OFF_OBJ_MAP_GROUP) * 256
                + emu:read8(o + S.OFF_OBJ_MAP_NUM) == S.MAP_TEMPLE then
            emu:write8(o + 1, emu:read8(o + 1) | 1)
            if id == localId then target = o end
        end
    end
    L.expect(target ~= nil, "the sight probe uses a real spawned hound")
    for offset = S.OFF_OBJ_CURRENT_COORDS - 4, S.OFF_OBJ_CURRENT_COORDS + 4, 4 do
        emu:write16(target + offset, x + S.MAP_OFFSET)
        emu:write16(target + offset + 2, y + S.MAP_OFFSET)
    end
    emu:write8(target + 0x18, 0x44)
end
local function caught(stage, touches, x, y)
    L.waitUntil(L.scriptRunning, 120, "the native hound sight to start its catch script")
    L.settle()
    local px, py = L.pos()
    L.expect(px == x and py == y and L.getVar(S.VAR_STAGE) == stage
             and L.getVar(S.VAR_TOUCHES) == touches,
             "a real hound catch restores only the current glade and preserves progress")
end
local function cap(expected)
    L.setVar(S.VAR_DIFFICULTY, 2)
    L.runHeader("Hunt_CapHeader")
    L.expect(L.getVar(S.VAR_RESULT) == expected, "native Spartan cap is " .. expected)
    L.setVar(S.VAR_DIFFICULTY, 1)
end
local function fullScrollPocket()
    local saved = {}
    local pocket = L.sb1() + S.OFF_SB1_BAG + S.OFF_BAG_SCROLLS
    local key = emu:read32(L.sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
    for i = 0, S.BAG_SCROLL_COUNT - 1 do
        local slot = pocket + i * S.ITEM_SLOT_SIZE
        saved[i] = {emu:read16(slot), emu:read16(slot + 2) ~ key}
        emu:write16(slot, S.ITEM_OTHER_SCROLL)
        emu:write16(slot + 2, 1 ~ key)
    end
    local restorePithos = L.fillPithos()   -- or the scroll would go to the Pithos
    return function()
        restorePithos()
        local live = L.sb1() + S.OFF_SB1_BAG + S.OFF_BAG_SCROLLS
        local liveKey = emu:read32(L.sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
        for i = 0, S.BAG_SCROLL_COUNT - 1 do
            emu:write16(live + i * S.ITEM_SLOT_SIZE, saved[i][1])
            emu:write16(live + i * S.ITEM_SLOT_SIZE + 2, saved[i][2] ~ liveKey)
        end
    end
end
L.start(function()
    L.quickstart()
    L.runHeader("Approach_SetupHeader")
    L.runHeader("Hunt_SetupHeader")
    L.useWarp(S.MAP_TEMPLE)
    L.setBeat("hunt_teach", false)
    L.expect(L.mapId() == S.MAP_TEMPLE and emu:read8(S.gTimeOfDay) == S.TIME_NIGHT,
             "the real temple entrance reaches the endless-night grove")
    L.talk(L.sign(T .. "Instructions"))
    L.go(7, 42)
    L.expect(emu:saveStateFile(L.OUT .. "before_sight_probe.ss", 31), "saved the ordinary patrol before controlled sight checks")
    sentry(1, 5, 42)
    L.wait(60)
    L.expect(L.idle(), "the actual cypress blocks a hound two tiles away")
    L.go(12, 41)
    sentry(1, 8, 41)
    L.wait(60)
    L.expect(L.idle(), "normal sight does not reach four clear tiles")
    sentry(1, 9, 41)
    caught(0, 0, 14, 42)
    L.expect(emu:loadStateFile(L.OUT .. "before_sight_probe.ss", 31), "restored the actual moving patrol")
    L.wait(30)
    talk("Teach")
    L.go(23, 33, {avoid = avoid})
    L.expect(L.getVar(S.VAR_STAGE) == 1 and L.defeated(S.TRAINER_HUNT_TEACH),
             "crossing the first patrol and winning its huntress unlocks stage two")
    L.shot("three_hounds")
    L.setBeat("hunt_test", false)
    L.go(25, 27, {avoid = avoid})
    L.expect(emu:saveStateFile(L.OUT .. "before_moon_probe.ss", 31), "saved stage two before moonlight boundary checks")
    sentry(3, 18, 27)
    L.wait(60)
    L.expect(L.idle(), "moonlight does not reveal the player seven tiles away")
    sentry(3, 19, 27)
    caught(1, 0, 23, 33)
    L.expect(emu:loadStateFile(L.OUT .. "before_moon_probe.ss", 31), "restored all three moving hounds after the boundary probe")
    L.wait(30)
    L.go(6, 20, {avoid = avoid})
    L.expect(L.getVar(S.VAR_STAGE) == 2 and not L.defeated(S.TRAINER_HUNT_TEST),
             "the three-hound stage can be completed without its optional acolyte")
    L.setBeat("golden_hind", false)
    for touch = 1, 3 do
        talk("Hind", {every = true})
        L.expect(L.getVar(S.VAR_TOUCHES) == touch, "actual antler touch " .. touch)
        if touch < 3 then
            L.expect(not L.getFlag(S.FLAG_TRIAL), "the hind's relocation cannot prematurely quiet the hounds")
        end
        L.shot("antler_" .. touch)
        if touch == 1 then
            local px, py = L.pos()
            sentry(5, px - 3, py)
            caught(2, 1, 6, 20)
            local hind = L.npc(T .. "Hind")
            L.expect(hind.x == 4 and hind.y == 11, "the next clearing survives a real hound reset")
        end
    end
    L.expect(L.getFlag(S.FLAG_TRIAL) and L.getVar(S.VAR_STAGE) == 3,
             "three different clearings complete the hunt and quiet the hounds")
    talk("Master")
    L.go(14, 4)
    cap(37)
    L.expect(emu:saveStateFile(L.OUT .. "before_kallisto.ss", 31), "saved the completed hunt before Kallisto")
    emu:write16(L.partyMon(0) + S.OFF_MON_HP, 1)
    L.battleMode = "lose"
    talk("Kallisto")
    L.battleMode = nil
    L.expect(L.battles[#L.battles].outcome == S.B_OUTCOME_LOST
             and L.mapId() == S.MAP_ARKADIA and not L.getFlag(S.FLAG_BADGE05),
             "actual Kallisto defeat returns to Arkadia without awarding a Laurel")
    L.expect(L.getFlag(S.FLAG_TRIAL) and L.getVar(S.VAR_TOUCHES) == 3,
             "losing the boss does not erase the hunt")
    L.expect(emu:read8(L.ichor() + S.OFF_HELD_TIME) == 0,
             "whiteout recovery releases the temple's held night")
    L.shot("kallisto_recovery")
    L.expect(emu:loadStateFile(L.OUT .. "before_kallisto.ss", 31), "restored the completed hunt for the win")
    L.wait(30)
    L.waitUntil(L.idle, 600, "control after restoring Kallisto")
    local restoreScrolls = fullScrollPocket()
    talk("Kallisto", {every = true})
    L.expect(L.getFlag(S.FLAG_BADGE05) and L.defeated(S.TRAINER_KALLISTO)
             and not L.getFlag(S.FLAG_SCROLL) and L.itemCount(S.ITEM_TORMENT) == 0,
             "a full scroll pocket cannot lose the Laurel or falsely claim Torment")
    cap(40)
    local battles = #L.battles
    restoreScrolls()
    talk("Kallisto")
    L.expect(#L.battles == battles and L.getFlag(S.FLAG_SCROLL) and L.itemCount(S.ITEM_TORMENT) == 1,
             "making room grants the deferred scroll without fighting Kallisto again")
    talk("Kallisto")
    L.expect(#L.battles == battles and L.itemCount(S.ITEM_TORMENT) == 1,
             "Kallisto's battle and scroll do not replay")
    local favor = emu:read8(L.ichor() + S.OFF_ICHOR_FAVOR + S.GOD_ARTEMIS)
    L.talk(L.sign(T .. "Altar"), {answers = {1, 0}})
    L.expect(L.itemCount(S.ITEM_FEATHER) == 0
             and emu:read8(L.ichor() + S.OFF_ICHOR_FAVOR + S.GOD_ARTEMIS) == favor + 10,
             "the actual Artemis altar consumes the loved feather for double temple Favor")
    L.runHeader("Approach_SaveHeader")
    emu:reset()
    L.continueSave()
    L.expect(L.getFlag(S.FLAG_BADGE05) and L.getFlag(S.FLAG_TRIAL)
             and L.getVar(S.VAR_TOUCHES) == 3, "the Moon Laurel and hunt survive save/reset/CONTINUE")
    L.useWarp(S.MAP_ARKADIA)
    L.expect(L.mapId() == S.MAP_ARKADIA, "the completed grove has a working return to town")
    L.expect(emu:read8(L.ichor() + S.OFF_HELD_TIME) == 0,
             "leaving the grove restores normal world time")
    L.shot("moon_laurel")
end)
