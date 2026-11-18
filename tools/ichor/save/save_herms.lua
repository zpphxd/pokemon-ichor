-- Read (and optionally fix up) a real battery save: where the player is, their
-- Laurels and which travel herms are registered. Run by tools/ichor/save/save_herms.sh.
--   SAVE_IN   the .sav to load (a copy; never OpenEmu's own file)
--   HERMS     comma-separated TOWN_HERM ids to register, then save in game (empty: read only)
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local log = L.log

local function report(tag)
  local sb = L.sb1()
  local g, n = emu:read8(sb + S.OFF_SB1_LOCATION), emu:read8(sb + S.OFF_SB1_LOCATION + 1)
  local x, y = emu:read16(sb + S.OFF_SB1_POS), emu:read16(sb + S.OFF_SB1_POS + 2)
  local badges = {}
  for i = 0, 7 do if L.getFlag(S.FLAG_BADGE01_GET + i) then badges[#badges + 1] = i + 1 end end
  local herms = {}
  for t = 0, S.TOWN_HERM_COUNT - 1 do if L.getFlag(S.FLAG_ICHOR_TOWN_HERMS_START + t) then herms[#herms + 1] = t end end
  log(string.format("%s MAP %d.%d POS %d,%d LAURELS %s ACT1 %s ACT3 %d CLEAR %s HERMS %s", tag, g, n, x, y,
    table.concat(badges, ","), tostring(L.getFlag(S.FLAG_ICHOR_ACT1_COMPLETE)), L.getVar(S.VAR_ICHOR_ACT3),
    tostring(L.getFlag(S.FLAG_SYS_GAME_CLEAR)), table.concat(herms, ",")))
end

L.start(function()
  local path = os.getenv("SAVE_IN")
  L.expect(emu:loadSaveFile(path, false), "loaded " .. path)
  emu:reset()
  L.continueSave()
  L.shot("continued")
  report("BEFORE")
  local want = os.getenv("HERMS") or ""
  if want ~= "" then
    for t in want:gmatch("%d+") do L.setFlag(S.FLAG_ICHOR_TOWN_HERMS_START + tonumber(t), true) end
    report("SET")
    L.runHeader("SaveHerms_SaveHeader")
    L.wait(300)
    emu:reset()
    L.continueSave()
    report("AFTER")
    L.shot("after")
  end
end)
