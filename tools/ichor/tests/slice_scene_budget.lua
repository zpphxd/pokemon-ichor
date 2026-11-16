-- Isolated scene-clock regression: modeled inputs, no emulator memory access.
local function scene(battleFrames, limit, locked)
  local L = dofile("tools/ichor/tests/slice_lib.lua")
  L.init{tag = "SCENE MODEL", out = "", symbols = "build/slice/symbols.lua"}
  local completed = 0
  L.idle = function() return not locked and completed == #battleFrames end
  L.inBattle = function() return completed < #battleFrames end
  L.on = function() return false end
  L.taskRunning = function() return false end
  L.boxUp = function() return false end
  L.inOverworld = function() return false end
  L.where = function() return "modeled locked scene" end
  L.shot = function() end
  L.battle = function()
    for _ = 1, battleFrames[completed + 1] do L.frame() end
    completed = completed + 1
    return {outcome = 1}
  end
  local co = coroutine.create(function() return L.settle{limit = limit} end)
  local result = table.pack(coroutine.resume(co))
  local frames = 0
  while result[1] and coroutine.status(co) ~= "dead" do
    local kind = result[2]
    if kind == "frame" then
      frames = frames + 1
      assert(frames < 25000, "a modeled scene must remain bounded")
      result = table.pack(coroutine.resume(co))
    elseif kind == "log" then
      result = table.pack(coroutine.resume(co))
    else
      assert(kind == "call", "unexpected modeled coroutine request")
      local method = result[3]
      assert(method == "read8" or method == "read32" or method == "addKey" or method == "clearKey",
             "scene model must not access the real emulator: " .. tostring(method))
      result = table.pack(coroutine.resume(co, 0))
    end
  end
  return result, frames, completed
end

local result, frames, completed = scene({11000, 11000})
assert(result[1], "two legal battles must not consume the scene's own deadline: " .. tostring(result[2]))
assert(completed == 2 and frames == 22020 and #result[3] == 2,
       "both battles and the full 20-frame field-control check must finish")
result, frames = scene({}, 30, true)
assert(not result[1] and tostring(result[2]):find("the player never got control back", 1, true),
       "a genuinely locked non-battle scene must still fail")
assert(frames > 30 and frames < 100, "the requested non-battle deadline must remain effective")
result, frames, completed = scene({11000, 11000}, 30, true)
assert(not result[1] and completed == 2 and frames > 22030 and frames < 22100,
       "excluding battle time must not disable the post-battle scene deadline")
console:log("SCENE BUDGET PASS: two long battles, bounded scene lock and bounded post-battle lock")
console:log("SCENE BUDGET done")
