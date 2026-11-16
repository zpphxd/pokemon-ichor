-- Native artifact writes and modeled failures; not progression evidence.
local L = dofile("tools/ichor/tests/slice_lib.lua")
local OUT = "build/slice-persistence/"
L.init{tag = "SLICE PERSISTENCE", out = OUT, symbols = "build/slice/symbols.lua"}
L.statesDir = OUT .. "states/"
L.mapId = function() return 0 end
L.inOverworld = function() return false end
L.inBattle = function() return false end

L.start(function()
  L.wait(120)
  L.shot("native")
  L.setBeat("native")
  local original = assert(io.open(OUT .. "shots/0001_boot_native.png", "rb"))
  local png = original:read("a")
  original:close()
  local stale = assert(io.open(OUT .. "shots/0002_native_missing.png", "wb"))
  assert(stale:write(png))
  assert(stale:close())
  local screenshot, saveState = L.emu.screenshot, L.emu.saveStateFile
  L.emu.screenshot = function() end
  local ok, err = pcall(L.shot, "missing")
  assert(not ok and tostring(err):find("could not save screenshot", 1, true),
         "a failed replacement must not accept a stale screenshot")
  L.emu.screenshot = function(_, path)
    local file = assert(io.open(path, "wb"))
    assert(file:write("\137PNG\r\n\26\n"))
    assert(file:close())
  end
  ok, err = pcall(L.shot, "truncated")
  assert(not ok and tostring(err):find("incomplete PNG", 1, true),
         "a truncated screenshot must not count as persisted evidence")
  L.emu.screenshot = screenshot
  L.emu.saveStateFile = function() return false end
  ok, err = pcall(L.setBeat, "missing")
  assert(not ok and tostring(err):find("could not save diagnostic state", 1, true),
         "failed diagnostic state writes must stop the run")
  L.emu.saveStateFile = saveState
  L.log("PASS: actual PNG/state writes and explicit missing/truncated artifact failures")
end)
