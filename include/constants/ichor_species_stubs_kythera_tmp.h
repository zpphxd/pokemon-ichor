// TEMPORARY (world-act3, Kythera's interiors): stand-ins for the Aethos species
// Kythera's and Melos's homes give, trade or show, until the Aethos dex's
// stand-in header defines them. Each maps to a vanilla species of the same
// type and role. Delete this file, and its #include at the end of species.h,
// once SPECIES_<NAME> exists for all six.
#ifndef GUARD_CONSTANTS_ICHOR_SPECIES_STUBS_KYTHERA_TMP_H
#define GUARD_CONSTANTS_ICHOR_SPECIES_STUBS_KYTHERA_TMP_H

#ifndef SPECIES_TELKANVIL
#define SPECIES_TELKANVIL SPECIES_EMPOLEON   // Water/Steel sea smith: Bathykleia's Ankyra
#endif
#ifndef SPECIES_GLYPHLET
#define SPECIES_GLYPHLET SPECIES_NOSEPASS    // Rock, Sturdy, "just sits": what Bathykleia wants
#endif
#ifndef SPECIES_HIMEROW
#define SPECIES_HIMEROW SPECIES_TOGEKISS     // Fairy/Flying, Super Luck: Lysis's Pothos
#endif
#ifndef SPECIES_EROSIE
#define SPECIES_EROSIE SPECIES_TOGEPI        // Fairy, friendship evolution: Peristera's Egg
#endif
#ifndef SPECIES_GALENYON
#define SPECIES_GALENYON SPECIES_PELIPPER    // Water/Flying, Keen Eye: what Lysis wants
#endif
#ifndef SPECIES_PANACOIL
#define SPECIES_PANACOIL SPECIES_SEVIPER     // the Asclepeion healers' snake
#endif

#endif // GUARD_CONSTANTS_ICHOR_SPECIES_STUBS_KYTHERA_TMP_H
