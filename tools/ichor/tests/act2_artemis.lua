-- The Hunt for the Hind check, run by tools/ichor/tests/act2_artemis.sh (read it first).
--
-- Plays the Temple of Artemis as a player would, with key presses on slice_lib's walker,
-- and checks the hunt's state after each beat: VAR_ICHOR_HUNT, trainer flags, the stair's
-- hedge and Anthia's gate metatiles, the hind's clearing, and the rewards.
--
-- The hounds are crossed by watching them. Each one's patrol comes from the map's builder
-- (hunt.lua); the test syncs each patrol to the live hound (a walker's every new step, a
-- turner's every turn re-anchors it), then plans the player's walk tile by tile over time,
-- never standing where a hound will look, and re-plans after every step.
--
-- Prints "ARTEMIS ok ..." per check, "ARTEMIS shot ..." per screenshot, and ends with
-- "ARTEMIS done"; any failure prints "ARTEMIS FAIL: ..." first.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local log, expect, wait, shot, settle = L.log, L.expect, L.wait, L.shot, L.settle
for k, v in pairs(dofile(L.OUT .. "temple_scripts.lua")) do S.SCRIPTS[k] = v end
local HUNT = dofile(L.OUT .. "hunt.lua")
local P = "Arkadia_TempleOfArtemis_EventScript_"

local function hunt() return L.getVar(S.VAR_HUNT) end
local function at(x, y) local px, py = L.pos() return px == x and py == y end
local function mt(x, y) return (L.grid().tile(x, y)) end
local function key(x, y) return x * 64 + y end

-- --- The hounds, live ----------------------------------------------------------------------

local DIRCODE = { [1] = "S", [2] = "N", [3] = "W", [4] = "E" }
local DV = { S = { 0, 1 }, N = { 0, -1 }, W = { -1, 0 }, E = { 1, 0 } }

-- Each hound's patrol from hunt.lua: walkers as their points and step directions.
local hounds = {}
for n, h in ipairs(HUNT.hounds) do
  local d = { n = n, stage = h.stage, kind = h.kind, seq = h.seq, sight = h.sight, pts = { { h.x, h.y } } }
  if h.kind == "walk" then
    for i = 1, #h.seq do
      local v = DV[h.seq:sub(i, i)]
      local p = d.pts[#d.pts]
      d.pts[#d.pts + 1] = { p[1] + v[1], p[2] + v[2] }
    end
  end
  hounds[n] = d
end
local STEP, TURN = HUNT.step, HUNT.turn
local measured = { step = {}, turn = {} }

local function houndLocalIds()
  for n, d in ipairs(hounds) do d.lid = L.npc(P .. "Hound", n).localId end
end

-- (x, y, facing letter) of the live object with this local id, or nil off screen.
local function objState(lid)
  for i = 0, S.OBJECT_EVENTS_COUNT - 1 do
    local o = S.gObjectEvents + i * S.OBJECT_EVENT_SIZE
    if emu:read8(o) & 1 == 1 and emu:read8(o + S.OFF_OBJ_LOCAL_ID) == lid then
      local c = o + S.OFF_OBJ_CURRENT_COORDS
      return emu:read16(c) - S.MAP_OFFSET, emu:read16(c + 2) - S.MAP_OFFSET,
             DIRCODE[emu:read8(o + S.OFF_OBJ_FACING) & 0xF]
    end
  end
end

-- Watch every hound one frame: a change of tile or facing re-anchors its patrol.
local function track()
  local now = L.now()
  for _, d in ipairs(hounds) do
    local x, y, f = objState(d.lid)
    if not x then
      d.synced, d.last = false, nil
    else
      local last = d.last
      if last and (last[1] ~= x or last[2] ~= y or last[3] ~= f) then
        if d.kind == "walk" and (last[1] ~= x or last[2] ~= y) then
          for k = 1, #d.seq do
            local p = d.pts[k + 1]
            if p[1] == x and p[2] == y and d.seq:sub(k, k) == f then
              if d.changed then measured.step[#measured.step + 1] = now - d.changed end
              d.anchor, d.synced, d.changed = now - (k - 1) * STEP, true, now
              break
            end
          end
        elseif d.kind == "turn" and last[3] ~= f then
          local idx = ({ S = 0, W = 1, N = 2, E = 3 })[f]
          if d.changed then measured.turn[#measured.turn + 1] = now - d.changed end
          d.anchor, d.synced, d.changed = now - idx * TURN, true, now
        end
      end
      d.last = { x, y, f }
    end
  end
end

local function tick(n)
  for _ = 1, n or 1 do L.frame(); track() end
end

-- After a script ran the hounds stood frozen: learn them again.
local function unsync()
  for _, d in ipairs(hounds) do d.synced, d.last, d.changed = false, nil, nil end
end

-- A hound's (now, from, facing) at absolute frame t, if synced.
local function houndAt(d, t)
  if d.kind == "turn" then
    local i = ((t - d.anchor) // TURN) % 4
    local p = d.pts[1]
    return p, p, ("SWNE"):sub(i + 1, i + 1)
  end
  local k = ((t - d.anchor) // STEP) % #d.seq + 1
  return d.pts[k + 1], d.pts[k], d.seq:sub(k, k)
end

local function stageHounds(stage)
  local out = {}
  for _, d in ipairs(hounds) do if d.stage == stage then out[#out + 1] = d end end
  return out
end

local function syncAll(stage, limit)
  local t0 = L.now()
  while true do
    local ok = true
    for _, d in ipairs(stageHounds(stage)) do
      if objState(d.lid) and not d.synced then ok = false end
    end
    if ok then return end
    if L.now() - t0 > (limit or 400) then L.fail("the stage " .. stage .. " hounds never showed their patrols") end
    tick()
  end
end

-- --- The plan --------------------------------------------------------------------------------
-- Breadth-first over (tile, frame): a step takes MOVE frames (sneakStep makes it exactly
-- that), a wait WAITF. The tile stepped into is in view from the step's first frame (the
-- engine polls trainer sight every frame, against the tile the player is walking into).

local MOVE, WAITF, MARGIN, HORIZON = 24, 4, 4, 1200
local KEYS = { { 0, -1, K.UP }, { 0, 1, K.DOWN }, { -1, 0, K.LEFT }, { 1, 0, K.RIGHT } }

local function planner(stage)
  local g = L.grid()
  local hs = stageHounds(stage)
  local fixed = {}
  for k, _ in pairs(g.people) do fixed[k] = true end
  for _, d in ipairs(hs) do
    local x, y = objState(d.lid)
    if x then fixed[x .. "," .. y] = nil end
  end
  local function open(x, y)
    local mid, solid = g.tile(x, y)
    return mid ~= nil and not solid
  end
  local live = {}
  for _, d in ipairs(hs) do if objState(d.lid) then live[#live + 1] = d end end
  local openCache = {}
  local function isOpen(x, y)
    local k = key(x, y)
    local o = openCache[k]
    if o == nil then o = open(x, y) and not fixed[x .. "," .. y]; openCache[k] = o end
    return o
  end
  -- Every frame of the plan's window, once: danger[tile] = { [frame] = true } for the
  -- frames some hound looks at the tile, and bodies[frame] the tiles hounds stand on.
  local t0 = L.now()
  local lo, hi = t0 - MARGIN - 1, t0 + HORIZON + MOVE + MARGIN + 1
  local danger, bodiesAt = {}, {}
  for t = lo, hi do
    local states, bodies = {}, {}
    for _, d in ipairs(live) do
      local now, from, f = houndAt(d, t)
      states[#states + 1] = { d, now, from, f }
      bodies[key(now[1], now[2])] = true
      bodies[key(from[1], from[2])] = true
    end
    bodiesAt[t] = bodies
    for _, st in ipairs(states) do
      local d, now, from, f = st[1], st[2], st[3], st[4]
      local v = DV[f]
      for _, src in ipairs({ now, from }) do
        for k = 1, d.sight do
          local x, y = src[1] + v[1] * k, src[2] + v[2] * k
          local kk = key(x, y)
          local dt = danger[kk]
          if not dt then dt = {}; danger[kk] = dt end
          dt[t] = true
          if not isOpen(x, y) or (bodies[kk] and not (x == now[1] and y == now[2])
                                  and not (x == from[1] and y == from[2])) then
            break
          end
        end
      end
    end
  end
  local function safe(x, y, a, b)
    local dt = danger[key(x, y)]
    if not dt then return true end
    for t = a - MARGIN, b + MARGIN do
      if dt[t] then return false end
    end
    return true
  end
  local function blocked(x, y, t)
    if fixed[x .. "," .. y] then return true end
    local b = bodiesAt[t]
    return b ~= nil and b[key(x, y)] == true
  end
  return { open = isOpen, safe = safe, blocked = blocked }
end

-- The first move toward a goal: { wait = frames } or { key = K.*, to = {x, y} }, or nil.
local function firstMove(stage, goals)
  local pl = planner(stage)
  local sx, sy = L.pos()
  local t0 = L.now()
  if goals[key(sx, sy)] then return { done = true } end
  local function sk(x, y, t) return (key(x, y) << 13) | ((t - t0) // WAITF) end
  local start = sk(sx, sy, t0)
  -- node[k] = { parent key, x, y, t }
  local node = { [start] = { nil, sx, sy, t0 } }
  local queue, head = { start }, 1
  local function push(k2, parent, x, y, t)
    if node[k2] == nil then
      node[k2] = { parent, x, y, t }
      queue[#queue + 1] = k2
    end
  end
  while head <= #queue do
    local k = queue[head]
    head = head + 1
    local _, x, y, t = table.unpack(node[k])
    if goals[key(x, y)] then
      -- the chain from the start to here; its first link is the first action
      local chain = {}
      local c = k
      while c ~= start do chain[#chain + 1] = c; c = node[c][1] end
      local first = node[chain[#chain]]
      if first[2] == sx and first[3] == sy then
        local n = 0
        for i = #chain, 1, -1 do
          local s = node[chain[i]]
          if s[2] == sx and s[3] == sy then n = n + 1 else break end
        end
        return { wait = n * WAITF }
      end
      for _, kk in ipairs(KEYS) do
        if sx + kk[1] == first[2] and sy + kk[2] == first[3] then
          return { key = kk[3], to = { first[2], first[3] } }
        end
      end
    end
    if t + MOVE <= t0 + HORIZON then
      if pl.safe(x, y, t, t + WAITF) then push(sk(x, y, t + WAITF), k, x, y, t + WAITF) end
      for _, kk in ipairs(KEYS) do
        local qx, qy = x + kk[1], y + kk[2]
        if pl.open(qx, qy) and not pl.blocked(qx, qy, t) and not pl.blocked(qx, qy, t + MOVE)
           and pl.safe(qx, qy, t, t + MOVE) then
          push(sk(qx, qy, t + MOVE), k, qx, qy, t + MOVE)
        end
      end
    end
  end
  return nil
end

-- One step that takes exactly MOVE frames, watching the hounds all the while.
local function sneakStep(k)
  local x0, y0 = L.pos()
  local t0 = L.now()
  emu:addKey(k)
  repeat
    tick()
    local x, y = L.pos()
    if x ~= x0 or y ~= y0 then break end
  until L.now() - t0 > 30 or L.scriptRunning()
  emu:clearKey(k)
  local x, y = L.pos()
  if x == x0 and y == y0 then return L.scriptRunning() and "taken" or "blocked" end
  -- the walk itself, then the frames the plan gave it
  local moved = L.now()
  while not L.idle() and L.now() - moved < 40 do
    if L.scriptRunning() then return "taken" end
    tick()
  end
  while L.now() - t0 < MOVE do
    if L.scriptRunning() then return "taken" end
    tick()
  end
  if L.scriptRunning() or not L.idle() then return "taken" end
  return "moved"
end

-- Cross a stage to any of `goals` ({ {x, y}, ... }) without being seen.
local function sneak(stage, goals, what)
  local gs = {}
  for _, q in ipairs(goals) do gs[key(q[1], q[2])] = true end
  local waited, steps = 0, 0
  syncAll(stage)
  for _ = 1, 900 do
    local m = firstMove(stage, gs)
    if m and m.done then
      log(string.format("ok sneaked %s in %d steps, %d frames waiting", what, steps, waited))
      return
    end
    if not m then
      tick(WAITF); waited = waited + WAITF
    elseif m.wait then
      tick(m.wait); waited = waited + m.wait
    else
      local r = sneakStep(m.key)
      if r == "taken" then
        shot("caught_" .. what:gsub("%W", "_"))
        L.fail(string.format("a hound saw the player stepping to (%d,%d) on the way to %s", m.to[1], m.to[2], what))
      end
      steps = steps + 1
    end
    syncAll(stage)
  end
  L.fail("never got to " .. what)
end

-- Walk into a hound's view on purpose: wait for hound n to face (dx, dy) toward tile
-- (x, y) from within its sight, then step onto (x, y) from the safe tile next to it.
local function getCaught(n, x, y, fromKey)
  local d = hounds[n]
  syncAll(d.stage)
  for _ = 1, 2000 do
    local hx, hy, f = objState(d.lid)
    if hx then
      local v = DV[f]
      for k = 1, d.sight do
        if hx + v[1] * k == x and hy + v[2] * k == y then
          local r = L.step(fromKey)
          expect(r == "taken", string.format("H%d sees the player stepping into its line at (%d,%d)", n, x, y))
          settle()
          unsync()
          return
        end
      end
    end
    tick()
  end
  L.fail("H" .. n .. " never looked at (" .. x .. "," .. y .. ")")
end

-- Touch the golden hind from wherever the player stands next to her.
local function touchHind(shotName)
  local h = L.npc(P .. "Hind")
  local x, y = L.pos()
  local face = (h.x > x and K.RIGHT) or (h.x < x and K.LEFT) or (h.y > y and K.DOWN) or K.UP
  L.face(face)
  L.tap(K.A)
  wait(10)
  settle({ shots = { [1] = shotName } })
  unsync()
end

local function nextTo(x, y)
  return { { x + 1, y }, { x - 1, y }, { x, y + 1 }, { x, y - 1 } }
end

L.start(function()
  L.quickstart()
  L.runHeader("ArtemisTest_SetupHeader", { noSettle = true })
  L.waitUntil(function() return L.mapId() == S.MAP_TEMPLE and L.idle() end, 4000, "the temple")
  wait(30)
  houndLocalIds()

  -- The porch: Phylonoe's welcome, her answers, the great altar.
  L.setBeat("porch")
  expect(at(14, 49), "arrived on the temple's doormat")
  expect(hunt() == 0, "the hunt hasn't begun")
  expect(mt(14, 8) == S.MT_STAIR_HEDGE_L, "the hedge stands across the rock's stair")
  shot("door")
  expect(L.step(K.UP) == "taken", "Phylonoe calls out inside the door")
  settle({ every = true })
  expect(hunt() == 10, "the welcome begins the hunt (Stage I)")
  L.talk(L.npc(P .. "Phylonoe"), { shots = { [1] = "phylonoe_menu", [2] = "phylonoe_rules" }, answers = { "yes" } })
  L.talk(L.sign(P .. "Altar"), { shots = { [1] = "altar" }, answers = { "yes" } })
  L.talk(L.sign(P .. "Statue"), { shots = { [1] = "statue" } })
  L.talk(L.sign(P .. "Kennel"), { shots = { [1] = "kennel" } })

  -- Stage I: three walks back from the hound (Phylonoe's hint), then past it.
  L.setBeat("stage1")
  L.go(14, 41)
  shot("stage1_forecourt")
  for i = 1, 3 do
    L.go(14, 40)
    getCaught(1, 14, 39, K.UP)
    expect(at(14, 43), string.format("walk-back %d: the hound leaves the player under the first arch", i))
    expect(hunt() == 10 + i, string.format("walk-back %d is counted (VAR_ICHOR_HUNT %d)", i, hunt()))
    if i == 1 then shot("stage1_walked_back") end
  end
  L.talk(L.npc(P .. "Phylonoe"), { shots = { [1] = "phylonoe_hint" }, answers = { "down" } })
  expect(hunt() == 13, "asking Phylonoe keeps the count")
  L.go(14, 41)
  sneak(1, { { 21, 37 } }, "past the first hound")
  shot("stage1_past_the_hound")
  L.go(22, 36)
  expect(L.defeated(S.TRAINER_KYRENE), "Kyrene battled the player at the second arch")
  L.go(22, 33)
  expect(hunt() == 20, "through the second arch: Stage II")

  -- Stage II: a walk back to the second arch, then past the turning hound and the stele's
  -- hound to Anthia's grove; her gate; the shortcut to the third arch.
  L.setBeat("stage2")
  shot("stage2_arch")
  L.go(24, 28)
  getCaught(2, 24, 27, K.UP)
  expect(at(22, 34) and hunt() == 21, "H2 walks the player back to the second arch")
  sneak(2, { { 8, 30 } }, "through the first clearing and past the stele")
  shot("stage2_middle")
  L.go(5, 31)
  L.talk(L.npc(P .. "Anthia"), { shots = { [1] = "anthia" } })
  expect(L.defeated(S.TRAINER_ANTHIA), "beat Anthia, the optional huntress")
  expect(mt(2, 28) == S.MT_GATE_OPEN and mt(2, 27) == S.MT_GATE_TOP_OPEN, "Anthia's gate stands open")
  L.talk(L.npc(P .. "ItemPrettyFeather"), { shots = { [1] = "feather" } })
  expect(L.getFlag(S.FLAG_FEATHER) and L.itemCount(S.ITEM_PRETTY_FEATHER) == 1, "the Pretty Feather by her bench")
  L.go(2, 29)
  sneak(2, { { 6, 23 } }, "by Anthia's gate to the third arch")
  shot("stage2_shortcut")
  L.go(6, 20)
  expect(hunt() == 30, "through the third arch: Stage III")

  -- Stage III: the hind's three touches.
  L.setBeat("stage3")
  shot("stage3_arch")
  local A = HUNT.hind.A
  sneak(3, nextTo(A[1], A[2]), "to the hind at A")
  touchHind("hind_touch_1")
  local h = L.npc(P .. "Hind")
  expect(hunt() == 40 and h.x == HUNT.hind.B[1] and h.y == HUNT.hind.B[2], "the first touch: she bolts to B")
  local B = HUNT.hind.B
  sneak(3, nextTo(B[1], B[2]), "after her to B")
  touchHind("hind_touch_2")
  h = L.npc(P .. "Hind")
  expect(hunt() == 50 and h.x == HUNT.hind.C[1] and h.y == HUNT.hind.C[2], "the second touch: she bolts to C")
  local C = HUNT.hind.C
  sneak(3, nextTo(C[1], C[2]), "after her to C")
  touchHind("hind_touch_3")
  expect(hunt() == 60 and L.getFlag(S.FLAG_HUNT_DONE), "the third touch: the hunt is won")
  expect(L.getFlag(S.FLAG_SAGITTA), "Sagitta on the Star Chart")
  expect(mt(14, 8) == S.MT_STAIR_HEDGE_LOWERED_L and mt(15, 8) == S.MT_STAIR_HEDGE_LOWERED_R,
         "the hedge across the stair has sunk to its roots")
  sneak(3, { { 14, 9 }, { 15, 9 } }, "from C to the stair")
  shot("stage3_stair")
  L.go(14, 8)
  L.go(14, 7)
  expect(L.defeated(S.TRAINER_PROKRIS), "Prokris battled the player at the stair's foot")

  -- Kallisto.
  L.setBeat("kallisto")
  L.go(14, 5)
  expect(L.step(K.UP) == "taken", "Kallisto's scene starts at the top of the stair")
  settle({ shots = { [1] = "kallisto_sky", [4] = "kallisto_looks", [8] = "kallisto_laurel",
                     [10] = "ursa_major" }, every = true, limit = 60000 })
  unsync()
  expect(L.defeated(S.TRAINER_KALLISTO), "beat Kallisto")
  expect(L.getFlag(S.FLAG_BADGE05_GET), "the Moon Laurel")
  expect(L.getFlag(S.FLAG_URSA_MAJOR), "Ursa Major on the Star Chart")
  expect(L.getFlag(S.FLAG_TM_DARK_PULSE), "Kallisto's TM Dark Pulse (a flag until the TM is numbered)")
  expect(L.getFlag(S.FLAG_RITE) and L.getFlag(S.FLAG_ARTEMIS_RITE_GIFT), "Artemis's rite taught")
  expect(L.itemCount(S.ITEM_PRETTY_FEATHER) == 2, "the rite's Pretty Feather")
  expect(hunt() == 70, "the hunt's state is the laurel given")
  shot("after_laurel")
  L.talk(L.npc(P .. "Kallisto"), { shots = { [1] = "kallisto_after" } })
  L.talk(L.sign(P .. "Pool"), { shots = { [1] = "pool" } })

  -- Back in through the door: the garden stays solved, its hounds asleep.
  L.setBeat("reentry")
  L.runHeader("ArtemisTest_ReenterHeader", { noSettle = true })
  L.waitUntil(function() return L.mapId() == S.MAP_TEMPLE and L.idle() and at(14, 49) end, 4000, "the temple again")
  wait(30)
  expect(hunt() == 70, "re-entered: the hunt stays won")
  expect(not L.getFlag(S.FLAG_HIDE_ASLEEP), "the sleeping hounds are shown")
  expect(not L.npc(P .. "Hound", 1).present, "the waking hounds are gone")
  expect(mt(14, 8) == S.MT_STAIR_HEDGE_LOWERED_L and mt(2, 28) == S.MT_GATE_OPEN,
         "re-entered: the stair's hedge down, Anthia's gate open")
  h = L.npc(P .. "Hind")
  expect(h.x == A[1] and h.y == A[2], "the hind grazes in clearing A again")
  L.go(14, 41)
  shot("reentry_stage1")
  L.talk(L.npc(P .. "SleepingHound", 1), { shots = { [1] = "hound_asleep" } })
  L.talk(L.npc(P .. "Phylonoe"), { shots = { [1] = "phylonoe_after" } })
  local ms, mt2 = measured.step, measured.turn
  table.sort(ms); table.sort(mt2)
  L.note(string.format("measured: a hound's step %s frames, a turn %s frames",
                       ms[#ms // 2 + 1] or "?", mt2[#mt2 // 2 + 1] or "?"))
  log("ok " .. L.bugs .. " bugs")
end)
