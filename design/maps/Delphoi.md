# Delphoi

Real-world model: Delphi on the south face of Parnassos. The temenos of Apollo
climbs a steep slope under the Phaedriades: the Sacred Way enters at the
south-east corner and zigzags up past the treasuries (Siphnian, Athenian),
votive statues (Kleobis and Biton) and the Rock of the Sibyl, under the
polygonal wall to the temple terrace, with the altar of the Chians before the
temple and the Omphalos; above it the theatre, and at the top the stadium. The
Kastalian spring rises in the cleft east of the sanctuary; the pilgrims'
village lies below the temenos.

- **Sentence:** the navel of the world, a sanctuary terraced up a mountain under two shining cliffs, its Sacred Way switching back past treasuries to the temple on its terrace.
- **Land:** a south-facing slope rising some forty tiles from the falls' top to the stadium terrace; the Phaedriades as a pale cliff wall along the north-east, split by the cleft of the spring; terraces held by the polygonal wall; the laurel grove on the terraces east of the theatre.
- **Settlement logic:** pilgrims arrive by the falls at the south-east, so the Asclepeion and Agora stand on the little square at the top of the falls path, with the lower town's lane of houses running west along the bottom terrace. The sanctuary's wall, with its gate at the foot of the Sacred Way, separates town from temenos. Inside, every terrace holds what a city dedicated: treasuries on the switchbacks, the Sibyl's rock with the oldest altar, the lesche in the north-east. The temple faces south on the highest built terrace with its altar outside in front of it; the theatre is cut into the slope above it; the stadium takes the only long flat at the top.
- **Reveal:** at the last switchback the temple's whole facade fills the screen above the Omphalos court, framed by the polygonal wall.
- **Signature:** the zigzag Sacred Way with its treasuries, and the Omphalos in its net of knotted wool in its own court.

## Passes and hooks

- **Pass 1** (`design/maps/img/delphoi_pass1.png`): a stray warp at (23,16); the pilgrims' queue blocked the Sacred Way.
- **Pass 2** (`..._pass2.png`): warp removed, pilgrims moved to the lane's side (19-22,31), the entrance herm at (37,41) by the arrival from the falls.
- **The arrival, an awe pass** (before: `design/maps/img/delphoi_full_before.png` and `delphoi_arrival_*_before.png`; after: `delphoi_full_after.png`, `delphoi_arrival_*_after.png` and the in-game frame `delphoi_arrival_ingame_after.png`). These are 15×10 crops made by `tools/ichor/maps/delphoi_frames.py`.
  - *Critique:* the Phaedriades read as a grey-brown heap; the first screen was orchard; nothing looked south.
  - *Pass A:* the cliffs redrawn as upright sunlit slabs (`phaedriades_face` in delphoi_art.py, warmed palette). They read as organ pipes, too regular.
  - *Pass B:* one broad slab per 32 px, with jogged joints, cracks, fluting and rose stains, and low contrast. It read as a flat yellow sheet, especially on the big east mass.
  - *Pass C:* contrast balanced; scrub ledges (`scree/face_scrub`) scattered through the faces to break the repeat; a spur of the Phaedriades put straight behind the temple (rows 4-7); the arrival scene now pans the camera up the Sacred Way to stop on the temple terrace under the cliffs ("The Shining Ones…"), then back; a lookout at the lane's west end (parapet, stele, a boy who watches the gulf) over the olive sea.
  - *Still open:* the cliff texture still repeats every two cells. A 64-px variant would cost about 16 of the 28 free tiles.
- **Hooks:** the stadium is the post-game Pythian games venue; the Kitharode's house quiz carries on there.
