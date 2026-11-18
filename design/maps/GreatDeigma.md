# The Great Deigma (Emporion)

Built by `tools/ichor/maps/kapeleia_rooms.py` on `gTileset_Kapeleia` (`tools/ichor/art/kapeleia_art.py`). Map `MAP_EMPORION_CITY_GREAT_DEIGMA`, 30x16. Brief: design/IDEAS.md, "Grand bazaar: the Great Deigma".

## Where

The Deigma's stoa on Emporion's harbor quarter now has two doors (`tools/ichor/maps/emporion.py`): the west door (32,36) is the old merchants' exchange, where beat 12 plays as before; the east door (36,36) is the Great Deigma, the covered market behind it (city warp 11, coord trigger `GreatDeigmaDoor`, sign at (35,36)). The old Deigma room, its scene and its test are unchanged.

## The hall

A timber-roofed market hall on stone flags. Six stalls under striped awnings along the north wall, the market's official measures and notice boards between them; the fountain at the crossing on a dolphin mosaic, lampstands and four columns down the nave; the curio stall west, Phormion's trapeza east; two more stalls by the door (spices, Athenian pots); bales, carpets, oil and grain samples down the sides; a red runner from the door. Twenty-two people and a pack Onotis, most of the shoppers wandering.

| Stall | Seller | Stock (Laurel 1-3 / +after the 4th / +after the 7th) |
|---|---|---|
| Phoenician (purple) | HIRAM of Sidon | Arachne and Poseidon Balls, Mystic Water, Wave Incense / Plutus Ball, Deep Sea Scale and Tooth / Prism Scale, Shell Bell |
| Egyptian (blue) | AMASIS of Naukratis | Frankincense, Heal and Energy Powder, Energy Root, Soft Sand / Revival Herb, Odd and Rose Incense, Smooth Rock / Light Clay, Pure Incense |
| Scythian (red) | SKYLES | Sharp Beak, Never-Melt Ice, Black Belt, Quick Claw / Icy Rock, Scope Lens / Wide Lens, Power Bracer, Power Weight |
| Stones (green) | PETRAIOS | Fire, Water, Thunder, Leaf Stones, Everstone / Moon, Sun, Ice / Shiny, Dusk, Dawn |
| Techniques (saffron) | SOPHRON | TM Water Pulse, Secret Power, Light Screen, Reflect, Safeguard / Sunny Day, Rain Dance, Sandstorm, Hail, Calm Mind, Double Team / Thunderbolt, Dragon Claw, Focus Punch, Sludge Bomb |
| Berries (red) | MELIA | Oran, Pecha, Cheri, Chesto, Rawst, Aspear, Persim / Sitrus, Lum / Occa, Passho, Wacan, Rindo, Yache |
| Curios (purple) | KALLIAS | One of six pairs a day (below), plus a Choice item after the 7th Laurel |
| Spices, pottery | the spicer, the potter | Talk only: the market's colour |
| Trapeza | PHORMION | Buys Bronze Obols, Silver Owls and Gold Staters at +25% over the market (+40% after the 4th Laurel, +60% after the 7th); Pasion in the Agora pays +20% |

Every seller says something new once you hold the 4th Laurel: Act II's first, won far from Emporion, so the stock is a reason to sail back.

**The daily curio stall.** On entry, if `FLAG_DAILY_ICHOR_DEIGMA_RARE` (daily bank) is clear, the map sets it and draws `VAR_ICHOR_DEIGMA_RARE` (bank var) anew, never the same as yesterday's: Lucky Egg + PP Up; Amulet Coin + Bottle Cap; Leftovers + Destiny Knot; Focus Sash + Rare Candy; Life Orb + PP Max; Eviolite + Ability Capsule.

## Passes

Renders: `img/great_deigma_pass1.png` (the room as first laid out, no people), `_pass2.png`, `_after.png`; the stoa `img/great_deigma_stoa_before.png` and `_after.png`; in game, `img/nysa_deigma_ingame.png`.

1. **Pass 1.** Six north stalls, the fountain, the curio stall and the trapeza. Critique: the south half and the door's first screen were bare floor; the hall read as a corridor, not a market; the hall was too quiet. The first layout also ran past the tile budget with the nursery in the same set (519 of 504), so the nursery moved to its own set.
2. **Pass 2.** Two more stalls by the door (new goods: spices, Athenian pots), samples and baskets in the aisles, eight wandering shoppers, the agoranomos at the measures, a porter and his Onotis. Critique: the crossing was still an empty ring round a small fountain; the nave's columns needed light.
3. **Pass 3.** The dolphin mosaic under the fountain, the runner shortened to meet it, lampstands by the columns; the porter moved off the curio stall's approach (the walk check found the stall unreachable). After: map_style_audit WARN only (12-cell edge, no height, as every interior).
