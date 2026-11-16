-- Run with the headless mGBA runner; this model never accesses emulator memory.
local createPilot = dofile("tools/ichor/tests/slice_pilot.lua")
local keys = {UP = 1, DOWN = 2, LEFT = 3, RIGHT = 4}
local checks = 0

for count = 1, 4 do
  for start = 0, count - 1 do
    for target = 0, count - 1 do
      local cursor = start
      local pilot = createPilot({
        S = {gMoveSelectionCursor = 1},
        K = keys,
        emu = {read8 = function(_, address)
          assert(address == 1, "cursor test must not read other state")
          return cursor
        end},
        tap = function(key)
          if key == keys.UP and cursor >= 2 then cursor = cursor - 2
          elseif key == keys.DOWN and cursor + 2 < count then cursor = cursor + 2
          elseif key == keys.LEFT and cursor % 2 == 1 then cursor = cursor - 1
          elseif key == keys.RIGHT and cursor % 2 == 0 and cursor + 1 < count then cursor = cursor + 1 end
        end,
        fail = function(message) error(message, 0) end,
      })
      pilot.moveCursor(target)
      assert(cursor == target, string.format("count=%d start=%d target=%d", count, start, target))
      checks = checks + 1
    end
  end
end
console:log("PILOT CURSOR PASS: " .. checks .. " sparse-grid transitions")
console:log("PILOT CURSOR done")
