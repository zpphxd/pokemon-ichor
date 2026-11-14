#ifndef GUARD_CONSTANTS_ICHOR_SPECIES_STUBS_ACT3_H
#define GUARD_CONSTANTS_ICHOR_SPECIES_STUBS_ACT3_H

// ICHOR_STUB_AETHOS_DEX: stand-ins for all 152 Aethos species, for Act III.
//
// Phase 4's script (design/phase4/SCRIPT.md) names Aethos species (the dex is
// design/dex/ on claude/aethos-dex-a7c73a). Until they exist in the species
// enum, each name maps to a vanilla species of the same or the closest types
// and a similar stage and base-stat total, so trainers.party ("Aphrell" ->
// SPECIES_APHRELL), the wild tables, givemon and the overworld sprites build.
// Each comment gives the dex number, the Aethos species' own types and its myth.
// No vanilla species stands in for two Aethos ones.
//
// It coexists with world-act1's constants/ichor_species_stubs.h, whichever is
// included first: every name is guarded on its own, and the 43 species that
// file covers use its exact stand-in, so a repeated #define is identical.
// The legendaries map to vanilla legendaries of fitting type: the Fates to the
// lake trio, the Lord of Time to Dialga, the Moment to Lugia.
//
// When the dex lands, define ICHOR_AETHOS_DEX (or delete this file and its
// include at the end of constants/species.h). The enum then provides the real
// constants and nothing else changes.

#ifndef ICHOR_AETHOS_DEX

#ifndef SPECIES_NEBREL
#define SPECIES_NEBREL      SPECIES_SNIVY               //   1. Grass
#endif
#ifndef SPECIES_KLADOE
#define SPECIES_KLADOE      SPECIES_SERVINE             //   2. Grass
#endif
#ifndef SPECIES_DAPHNYAD
#define SPECIES_DAPHNYAD    SPECIES_SERPERIOR           //   3. Grass/Fairy
#endif
#ifndef SPECIES_KYNDER
#define SPECIES_KYNDER      SPECIES_CYNDAQUIL           //   4. Fire
#endif
#ifndef SPECIES_DIKYON
#define SPECIES_DIKYON      SPECIES_QUILAVA             //   5. Fire
#endif
#ifndef SPECIES_PYLAKYON
#define SPECIES_PYLAKYON    SPECIES_TYPHLOSION          //   6. Fire/Ghost
#endif
#ifndef SPECIES_HIPLING
#define SPECIES_HIPLING     SPECIES_PIPLUP              //   7. Water
#endif
#ifndef SPECIES_THALAMARE
#define SPECIES_THALAMARE   SPECIES_PRINPLUP            //   8. Water
#endif
#ifndef SPECIES_SEISMARE
#define SPECIES_SEISMARE    SPECIES_EMPOLEON            //   9. Water/Ground
#endif
#ifndef SPECIES_EPOPOI
#define SPECIES_EPOPOI      SPECIES_PIDGEY              //  10. Normal/Flying, the hoopoe
#endif
#ifndef SPECIES_LOPHOPS
#define SPECIES_LOPHOPS     SPECIES_PIDGEOTTO           //  11. Normal/Flying
#endif
#ifndef SPECIES_BASILOPS
#define SPECIES_BASILOPS    SPECIES_PIDGEOT             //  12. Normal/Flying
#endif
#ifndef SPECIES_GALEKIT
#define SPECIES_GALEKIT     SPECIES_SENTRET             //  13. Normal, the weasel
#endif
#ifndef SPECIES_GELASABLE
#define SPECIES_GELASABLE   SPECIES_FURRET              //  14. Normal
#endif
#ifndef SPECIES_KAMPILLAR
#define SPECIES_KAMPILLAR   SPECIES_WURMPLE             //  15. Bug, Psyche's butterfly, as a caterpillar
#endif
#ifndef SPECIES_NYMVEIL
#define SPECIES_NYMVEIL     SPECIES_SILCOON             //  16. Bug, Psyche's butterfly, the chrysalis
#endif
#ifndef SPECIES_PSYCHORA
#define SPECIES_PSYCHORA    SPECIES_RIBOMBEE            //  17. Bug/Fairy, Psyche, the soul-moth
#endif
#ifndef SPECIES_ELALEAF
#define SPECIES_ELALEAF     SPECIES_SMOLIV              //  18. Grass, Athena's olive
#endif
#ifndef SPECIES_ELAPLING
#define SPECIES_ELAPLING    SPECIES_DOLLIV              //  19. Grass, Athena's olive, the sapling
#endif
#ifndef SPECIES_HIEROLIVE
#define SPECIES_HIEROLIVE   SPECIES_ARBOLIVA            //  20. Grass/Fighting, the sacred olive
#endif
#ifndef SPECIES_ERGANT
#define SPECIES_ERGANT      SPECIES_NINCADA             //  21. Bug, the Myrmidon ant
#endif
#ifndef SPECIES_HOPLOMEX
#define SPECIES_HOPLOMEX    SPECIES_HERACROSS           //  22. Bug/Fighting
#endif
#ifndef SPECIES_PEBBLITH
#define SPECIES_PEBBLITH    SPECIES_GEODUDE             //  23. Rock/Ground
#endif
#ifndef SPECIES_CAIRNOLITH
#define SPECIES_CAIRNOLITH  SPECIES_GRAVELER            //  24. Rock/Ground
#endif
#ifndef SPECIES_LAOLITH
#define SPECIES_LAOLITH     SPECIES_GOLEM               //  25. Rock/Fighting
#endif
#ifndef SPECIES_ERIPIP
#define SPECIES_ERIPIP      SPECIES_MAREEP              //  26. Electric, Amalthea's kid
#endif
#ifndef SPECIES_KERAZAP
#define SPECIES_KERAZAP     SPECIES_FLAAFFY             //  27. Electric
#endif
#ifndef SPECIES_KERASTORM
#define SPECIES_KERASTORM   SPECIES_AMPHAROS            //  28. Electric/Fairy
#endif
#ifndef SPECIES_HALCYLING
#define SPECIES_HALCYLING   SPECIES_WINGULL             //  29. Water/Flying, the halcyon
#endif
#ifndef SPECIES_GALENYON
#define SPECIES_GALENYON    SPECIES_PELIPPER            //  30. Water/Flying
#endif
#ifndef SPECIES_KETOFRY
#define SPECIES_KETOFRY     SPECIES_HORSEA              //  31. Water, the ketos
#endif
#ifndef SPECIES_KYNOKETOS
#define SPECIES_KYNOKETOS   SPECIES_SEADRA              //  32. Water/Dragon
#endif
#ifndef SPECIES_KARKIPOOL
#define SPECIES_KARKIPOOL   SPECIES_KRABBY              //  33. Water, Hera's crab
#endif
#ifndef SPECIES_KARKITOX
#define SPECIES_KARKITOX    SPECIES_KINGLER             //  34. Water/Poison
#endif
#ifndef SPECIES_NEMECUB
#define SPECIES_NEMECUB     SPECIES_LITLEO              //  35. Normal, the Nemean lion
#endif
#ifndef SPECIES_NEMELEON
#define SPECIES_NEMELEON    SPECIES_PYROAR              //  36. Normal
#endif
#ifndef SPECIES_EOPEEP
#define SPECIES_EOPEEP      SPECIES_MANKEY              //  37. Fighting, Alectryon
#endif
#ifndef SPECIES_ALEKROW
#define SPECIES_ALEKROW     SPECIES_PRIMEAPE            //  38. Fighting
#endif
#ifndef SPECIES_HOPLEKTOR
#define SPECIES_HOPLEKTOR   SPECIES_HAWLUCHA            //  39. Fighting/Flying
#endif
#ifndef SPECIES_ONOTIS
#define SPECIES_ONOTIS      SPECIES_LILLIPUP            //  40. Normal, Midas's donkey
#endif
#ifndef SPECIES_MIDONOS
#define SPECIES_MIDONOS     SPECIES_HERDIER             //  41. Normal/Steel
#endif
#ifndef SPECIES_HARPECK
#define SPECIES_HARPECK     SPECIES_MURKROW             //  42. Dark/Flying, the snatcher
#endif
#ifndef SPECIES_HARPELLE
#define SPECIES_HARPELLE    SPECIES_HONCHKROW           //  43. Dark/Flying
#endif
#ifndef SPECIES_CHELONET
#define SPECIES_CHELONET    SPECIES_SANDSHREW           //  44. Ground, Hermes's tortoise
#endif
#ifndef SPECIES_CHELYRA
#define SPECIES_CHELYRA     SPECIES_SANDSLASH           //  45. Ground/Fairy
#endif
#ifndef SPECIES_PITHOUND
#define SPECIES_PITHOUND    SPECIES_POOCHYENA           //  46. Dark/Psychic, Diogenes's dog
#endif
#ifndef SPECIES_MELIBEE
#define SPECIES_MELIBEE     SPECIES_COMBEE              //  47. Bug, the Melissai, the bee-priestesses
#endif
#ifndef SPECIES_MELISSEER
#define SPECIES_MELISSEER   SPECIES_VESPIQUEN           //  48. Bug/Psychic, the bee-seer; evolves from females only
#endif
#ifndef SPECIES_NARKERAY
#define SPECIES_NARKERAY    SPECIES_CHINCHOU            //  49. Water/Electric, the torpedo ray
#endif
#ifndef SPECIES_STACHYSS
#define SPECIES_STACHYSS    SPECIES_APPLIN              //  50. Grass, Triptolemus's grain
#endif
#ifndef SPECIES_STACHYPTER
#define SPECIES_STACHYPTER  SPECIES_FLAPPLE             //  51. Grass/Dragon, Triptolemus's winged dragon
#endif
#ifndef SPECIES_RHOARIL
#define SPECIES_RHOARIL     SPECIES_COTTONEE            //  52. Grass, Persephone's pomegranate
#endif
#ifndef SPECIES_KORANTHA
#define SPECIES_KORANTHA    SPECIES_WHIMSICOTT          //  53. Grass/Fairy, Persephone the Maiden, by day
#endif
#ifndef SPECIES_PERSENYX
#define SPECIES_PERSENYX    SPECIES_TREVENANT           //  54. Grass/Ghost, Persephone the Queen below, by night
#endif
#ifndef SPECIES_KAPLET
#define SPECIES_KAPLET      SPECIES_SANDILE             //  55. Ground, the Erymanthian boar
#endif
#ifndef SPECIES_KAPRODON
#define SPECIES_KAPRODON    SPECIES_KROOKODILE          //  56. Dark/Ground, the Erymanthian boar, grown
#endif
#ifndef SPECIES_SPALUNK
#define SPECIES_SPALUNK     SPECIES_DIGLETT             //  57. Ground, Ploutos's mole
#endif
#ifndef SPECIES_PLOUTERAS
#define SPECIES_PLOUTERAS   SPECIES_DUGTRIO             //  58. Ground
#endif
#ifndef SPECIES_AMPELIX
#define SPECIES_AMPELIX     SPECIES_BELLSPROUT          //  59. Grass/Poison, Dionysus's vine
#endif
#ifndef SPECIES_THYRSIVY
#define SPECIES_THYRSIVY    SPECIES_VICTREEBEL          //  60. Grass/Poison, Dionysus's ivy thyrsus
#endif
#ifndef SPECIES_BOTRYKIT
#define SPECIES_BOTRYKIT    SPECIES_STUNKY              //  61. Poison, Dionysus's leopard
#endif
#ifndef SPECIES_OINOPARD
#define SPECIES_OINOPARD    SPECIES_SKUNTANK            //  62. Poison/Dark, Dionysus's leopard, grown
#endif
#ifndef SPECIES_PROSOMIME
#define SPECIES_PROSOMIME   SPECIES_SLOWBRO_GALAR       //  63. Psychic/Poison, the theater's mask
#endif
#ifndef SPECIES_LYKOPUP
#define SPECIES_LYKOPUP     SPECIES_ZORUA               //  64. Dark, Lycaon the wolf-king
#endif
#ifndef SPECIES_LYKANAX
#define SPECIES_LYKANAX     SPECIES_ZOROARK             //  65. Dark, Lycaon; evolves by night
#endif
#ifndef SPECIES_ARKOBY
#define SPECIES_ARKOBY      SPECIES_IMPIDIMP            //  66. Dark, Kallisto the bear
#endif
#ifndef SPECIES_STARKOS
#define SPECIES_STARKOS     SPECIES_GRIMMSNARL          //  67. Dark/Fairy, Kallisto as the Great Bear
#endif
#ifndef SPECIES_SKYLAPS
#define SPECIES_SKYLAPS     SPECIES_BOLTUND             //  68. Electric, Laelaps, the hound that always catches
#endif
#ifndef SPECIES_KERDOVIX
#define SPECIES_KERDOVIX    SPECIES_THIEVUL             //  69. Dark/Fairy, the Teumessian vixen
#endif
#ifndef SPECIES_RAKNIT
#define SPECIES_RAKNIT      SPECIES_NYMBLE              //  70. Bug, Arachne the weaver
#endif
#ifndef SPECIES_HYPHANTIS
#define SPECIES_HYPHANTIS   SPECIES_LOKIX               //  71. Bug/Dark, Arachne, grown
#endif
#ifndef SPECIES_AMNOZE
#define SPECIES_AMNOZE      SPECIES_GIRAFARIG           //  72. Normal/Psychic, Endymion, asleep forever
#endif
#ifndef SPECIES_GLAUKOIN
#define SPECIES_GLAUKOIN    SPECIES_NATU                //  73. Psychic/Flying, Athena's owl
#endif
#ifndef SPECIES_SOPHOWL
#define SPECIES_SOPHOWL     SPECIES_XATU                //  74. Psychic/Flying, Athena's owl, grown
#endif
#ifndef SPECIES_OPHIDROP
#define SPECIES_OPHIDROP    SPECIES_EKANS               //  75. Poison, Asclepius's snake
#endif
#ifndef SPECIES_PANACOIL
#define SPECIES_PANACOIL    SPECIES_WEEZING_GALAR       //  76. Poison/Fairy, Panacea and the rod of Asclepius
#endif
#ifndef SPECIES_OBOLORN
#define SPECIES_OBOLORN     SPECIES_GIMMIGHOUL          //  77. Ghost, Charon's obol
#endif
#ifndef SPECIES_KALYPTOR
#define SPECIES_KALYPTOR    SPECIES_DUSCLOPS            //  78. Ghost, Charon, the hooded ferryman
#endif
#ifndef SPECIES_CHARONAUT
#define SPECIES_CHARONAUT   SPECIES_JELLICENT           //  79. Ghost/Water, Charon on the Styx
#endif
#ifndef SPECIES_ENIGMAW
#define SPECIES_ENIGMAW     SPECIES_GALLADE             //  80. Psychic/Fighting, the Sphinx's riddle
#endif
#ifndef SPECIES_KAMINOO
#define SPECIES_KAMINOO     SPECIES_TEPIG               //  81. Fire, the Khalkotauroi, the bronze bulls
#endif
#ifndef SPECIES_TAURIVET
#define SPECIES_TAURIVET    SPECIES_TAUROS_PALDEA_BLAZE //  82. Fire/Steel, Hephaestus's fire-breathing bronze bull
#endif
#ifndef SPECIES_KAPNUB
#define SPECIES_KAPNUB      SPECIES_NUMEL               //  83. Fire, Polybotes, the giant under Nisyros
#endif
#ifndef SPECIES_GIGANTOMB
#define SPECIES_GIGANTOMB   SPECIES_COALOSSAL           //  84. Fire/Rock, Polybotes, buried in his island
#endif
#ifndef SPECIES_TELPUP
#define SPECIES_TELPUP      SPECIES_SEEL                //  85. Water, the Telchines, seal-dog smiths
#endif
#ifndef SPECIES_TELKANVIL
#define SPECIES_TELKANVIL   SPECIES_DEWGONG             //  86. Water/Steel, the Telchines at the anvil
#endif
#ifndef SPECIES_NARTHIP
#define SPECIES_NARTHIP     SPECIES_CAPSAKID            //  87. Grass, Prometheus's fennel stalk
#endif
#ifndef SPECIES_PROMETHEX
#define SPECIES_PROMETHEX   SPECIES_SCOVILLAIN          //  88. Grass/Fire, the fire stolen in the fennel
#endif
#ifndef SPECIES_APHRELL
#define SPECIES_APHRELL     SPECIES_CLAMPERL            //  89. Water, Aphrodite's foam and scallop shell
#endif
#ifndef SPECIES_APHROGENE
#define SPECIES_APHROGENE   SPECIES_PRIMARINA           //  90. Water/Fairy, Aphrodite, foam-born
#endif
#ifndef SPECIES_NARCIBULB
#define SPECIES_NARCIBULB   SPECIES_PETILIL             //  91. Grass, Narcissus
#endif
#ifndef SPECIES_NARCISHEEN
#define SPECIES_NARCISHEEN  SPECIES_LUDICOLO            //  92. Grass/Water, Narcissus at his pool
#endif
#ifndef SPECIES_ECHOLALI
#define SPECIES_ECHOLALI    SPECIES_CHATOT              //  93. Normal, Echo, who can only repeat
#endif
#ifndef SPECIES_EROSIE
#define SPECIES_EROSIE      SPECIES_TOGEPI              //  94. Fairy, Eros
#endif
#ifndef SPECIES_HIMEROW
#define SPECIES_HIMEROW     SPECIES_TOGETIC             //  95. Fairy/Flying, Himeros, longing; evolves by friendship
#endif
#ifndef SPECIES_GLYPHLET
#define SPECIES_GLYPHLET    SPECIES_ROGGENROLA          //  96. Rock, Galatea, Pygmalion's carving
#endif
#ifndef SPECIES_KALLIGLYPH
#define SPECIES_KALLIGLYPH  SPECIES_CARBINK             //  97. Rock/Fairy, Galatea, the living marble
#endif
#ifndef SPECIES_ASTERLORN
#define SPECIES_ASTERLORN   SPECIES_PANGORO             //  98. Fighting/Dark, Asterion, the Minotaur
#endif
#ifndef SPECIES_MITOCLEW
#define SPECIES_MITOCLEW    SPECIES_KECLEON             //  99. Normal, Ariadne's clew of thread
#endif
#ifndef SPECIES_IKAROTH
#define SPECIES_IKAROTH     SPECIES_MASQUERAIN          // 100. Bug/Flying, Icarus
#endif
#ifndef SPECIES_KOLOSSETTE
#define SPECIES_KOLOSSETTE  SPECIES_KLINK               // 101. Steel, Talos, the bronze guardian
#endif
#ifndef SPECIES_KOLOSSARD
#define SPECIES_KOLOSSARD   SPECIES_STEELIX             // 102. Steel/Ground, Talos; evolves by trade with a Metal Coat
#endif
#ifndef SPECIES_KYMBASH
#define SPECIES_KYMBASH     SPECIES_BRONZOR             // 103. Steel, the Kouretes and their clashing bronze
#endif
#ifndef SPECIES_KOURODIN
#define SPECIES_KOURODIN    SPECIES_LUCARIO             // 104. Steel/Fighting, the Kouretes, the dancing guards
#endif
#ifndef SPECIES_MONOPHANT
#define SPECIES_MONOPHANT   SPECIES_RHYHORN             // 105. Rock/Normal, the Cyclopes
#endif
#ifndef SPECIES_POLYPHANT
#define SPECIES_POLYPHANT   SPECIES_RHYDON              // 106. Rock/Normal, Polyphemus
#endif
#ifndef SPECIES_SEPIDART
#define SPECIES_SEPIDART    SPECIES_OMANYTE             // 107. Rock/Electric, the belemnite, a thunderbolt stone
#endif
#ifndef SPECIES_SEPIVOLT
#define SPECIES_SEPIVOLT    SPECIES_OMASTAR             // 108. Rock/Electric, the belemnite, grown
#endif
#ifndef SPECIES_CHALKIP
#define SPECIES_CHALKIP     SPECIES_ROOKIDEE            // 109. Steel/Flying, the Stymphalian birds
#endif
#ifndef SPECIES_BELORNIS
#define SPECIES_BELORNIS    SPECIES_CORVIKNIGHT         // 110. Steel/Flying, the bronze-feathered Stymphalian birds
#endif
#ifndef SPECIES_SPORADON
#define SPECIES_SPORADON    SPECIES_JANGMO_O            // 111. Dragon, the Spartoi, sown dragon teeth
#endif
#ifndef SPECIES_DORYDRAKE
#define SPECIES_DORYDRAKE   SPECIES_HAKAMO_O            // 112. Dragon/Fighting, the Spartoi, armed men from the furrow
#endif
#ifndef SPECIES_GEOGRIP
#define SPECIES_GEOGRIP     SPECIES_THROH               // 113. Fighting/Ground, Antaeus the wrestler
#endif
#ifndef SPECIES_PELYTHON
#define SPECIES_PELYTHON    SPECIES_DRATINI             // 114. Dragon, Python of Delphi
#endif
#ifndef SPECIES_PYTHOROS
#define SPECIES_PYTHOROS    SPECIES_FLYGON              // 115. Dragon/Ground, Python, in the earth
#endif
#ifndef SPECIES_PYRAPOD
#define SPECIES_PYRAPOD     SPECIES_FENNEKIN            // 116. Fire, the Pythia's tripod
#endif
#ifndef SPECIES_MANTIPOD
#define SPECIES_MANTIPOD    SPECIES_DELPHOX             // 117. Fire/Psychic, the Delphic tripod and its smoke
#endif
#ifndef SPECIES_HYMNET
#define SPECIES_HYMNET      SPECIES_TORCHIC             // 118. Fire, Apollo's swan
#endif
#ifndef SPECIES_HYMNARIA
#define SPECIES_HYMNARIA    SPECIES_TALONFLAME          // 119. Fire/Flying, Apollo's singing swan
#endif
#ifndef SPECIES_ELEKTEAR
#define SPECIES_ELEKTEAR    SPECIES_ROTOM_MOW           // 120. Electric/Grass, the Heliades' amber tears
#endif
#ifndef SPECIES_AETLING
#define SPECIES_AETLING     SPECIES_RUFFLET             // 121. Flying, Zeus's eagle
#endif
#ifndef SPECIES_AETARCH
#define SPECIES_AETARCH     SPECIES_KILOWATTREL         // 122. Electric/Flying, Zeus's eagle, bearer of the bolt
#endif
#ifndef SPECIES_NIFLAKE
#define SPECIES_NIFLAKE     SPECIES_VULPIX_ALOLA        // 123. Ice, Chione, the snow-nymph
#endif
#ifndef SPECIES_CHIONYAD
#define SPECIES_CHIONYAD    SPECIES_NINETALES_ALOLA     // 124. Ice/Fairy, Chione; evolves with an Ice Stone
#endif
#ifndef SPECIES_KRYOPUFF
#define SPECIES_KRYOPUFF    SPECIES_DELIBIRD            // 125. Ice, Boreas, the north wind
#endif
#ifndef SPECIES_BORAPTERYX
#define SPECIES_BORAPTERYX  SPECIES_FROSMOTH            // 126. Ice/Flying, Boreas, winged
#endif
#ifndef SPECIES_PAGOSHARD
#define SPECIES_PAGOSHARD   SPECIES_BERGMITE            // 127. Ice, krystallos, ice turned to stone
#endif
#ifndef SPECIES_KRYSTOLOS
#define SPECIES_KRYSTOLOS   SPECIES_AVALUGG_HISUI       // 128. Ice/Rock, krystallos, rock crystal
#endif
#ifndef SPECIES_DAKROCK
#define SPECIES_DAKROCK     SPECIES_RELICANTH           // 129. Rock/Water, Niobe, the weeping rock
#endif
#ifndef SPECIES_LEBETRON
#define SPECIES_LEBETRON    SPECIES_MAGNETON            // 130. Steel/Electric, Salmoneus's bronze thunder
#endif
#ifndef SPECIES_BOULDYPHUS
#define SPECIES_BOULDYPHUS  SPECIES_RUNERIGUS           // 131. Rock/Ghost, Sisyphus's boulder
#endif
#ifndef SPECIES_ELEGULL
#define SPECIES_ELEGULL     SPECIES_DRIFLOON            // 132. Ghost, the Sirens
#endif
#ifndef SPECIES_SEIRENADE
#define SPECIES_SEIRENADE   SPECIES_DRIFBLIM            // 133. Ghost/Flying, the Sirens, grown
#endif
#ifndef SPECIES_STYGIAD
#define SPECIES_STYGIAD     SPECIES_FROSLASS            // 134. Ice/Ghost, the Styx
#endif
#ifndef SPECIES_HEXYLLA
#define SPECIES_HEXYLLA     SPECIES_SHARPEDO            // 135. Water/Dark, Scylla
#endif
#ifndef SPECIES_TRYBDIS
#define SPECIES_TRYBDIS     SPECIES_GASTRODON           // 136. Water/Ground, Charybdis, the whirlpool
#endif
#ifndef SPECIES_HALIGERON
#define SPECIES_HALIGERON   SPECIES_GOLDUCK             // 137. Water, Proteus, the old man of the sea
#endif
#ifndef SPECIES_NOSTAIL
#define SPECIES_NOSTAIL     SPECIES_FURFROU             // 138. Normal, Argos, Odysseus's dog
#endif
#ifndef SPECIES_MELODRAKON
#define SPECIES_MELODRAKON  SPECIES_ALTARIA             // 139. Dragon/Fairy, Ladon, the singing dragon of the Hesperides
#endif
#ifndef SPECIES_LERNIP
#define SPECIES_LERNIP      SPECIES_DEINO               // 140. Dragon/Poison, the Lernaean Hydra
#endif
#ifndef SPECIES_TRILERNA
#define SPECIES_TRILERNA    SPECIES_ZWEILOUS            // 141. Dragon/Poison, the Hydra, three heads
#endif
#ifndef SPECIES_LERNATHAN
#define SPECIES_LERNATHAN   SPECIES_HYDREIGON           // 142. Dragon/Poison, the Hydra, grown
#endif
#ifndef SPECIES_NEMIRA
#define SPECIES_NEMIRA      SPECIES_MESPRIT             // 143. Psychic/Fairy, Klotho the Spinner, a Fate
#endif
#ifndef SPECIES_LOTIRA
#define SPECIES_LOTIRA      SPECIES_UXIE                // 144. Psychic/Normal, Lachesis the Measurer, a Fate
#endif
#ifndef SPECIES_THANIRA
#define SPECIES_THANIRA     SPECIES_AZELF               // 145. Psychic/Ghost, Atropos the Cutter, a Fate
#endif
#ifndef SPECIES_KRONOLITH
#define SPECIES_KRONOLITH   SPECIES_DIALGA              // 146. Ground/Psychic, Kronos, the Lord of Time
#endif
#ifndef SPECIES_KAIRAZOR
#define SPECIES_KAIRAZOR    SPECIES_LUGIA               // 147. Flying/Psychic, Kairos, the Moment
#endif
#ifndef SPECIES_PEGAUNOS
#define SPECIES_PEGAUNOS    SPECIES_ZAPDOS              // 148. Electric/Flying, Pegasus, who carries the thunderbolt
#endif
#ifndef SPECIES_OLYMPANAX
#define SPECIES_OLYMPANAX   SPECIES_RAIKOU              // 149. Electric, Zeus
#endif
#ifndef SPECIES_PONTANAX
#define SPECIES_PONTANAX    SPECIES_SUICUNE             // 150. Water, Poseidon
#endif
#ifndef SPECIES_NEKRANAX
#define SPECIES_NEKRANAX    SPECIES_SPECTRIER           // 151. Ghost, Hades
#endif
#ifndef SPECIES_ICHORIN
#define SPECIES_ICHORIN     SPECIES_MEW                 // 152. Psychic, ichor, the blood of the gods
#endif

#endif // ICHOR_AETHOS_DEX

#endif // GUARD_CONSTANTS_ICHOR_SPECIES_STUBS_ACT3_H
