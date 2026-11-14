// TEMPORARY (world-act3, Kythera's interiors): VAR_ICHOR_ACT3, the act's one
// bank var (design/phase4/SCRIPT.md, "Flags, vars and save state"), isn't
// claimed yet. Until it is, it stands at the first offset of world-act3's bank
// var range (12-17, tools/ichor/claim_ranges.md), where claim.py would put it.
// Delete this file, and its #include at the end of vars.h, once
//   python3 tools/ichor/claim.py --range 12-17 bankvar VAR_ICHOR_ACT3 "..."
// has run. Don't claim another var at offset 12 while this stands.
#ifndef GUARD_CONSTANTS_ICHOR_VARS_STUBS_KYTHERA_TMP_H
#define GUARD_CONSTANTS_ICHOR_VARS_STUBS_KYTHERA_TMP_H

#ifndef VAR_ICHOR_ACT3
#define VAR_ICHOR_ACT3 (ICHOR_VARS_START + 0x0C)
#endif

#endif // GUARD_CONSTANTS_ICHOR_VARS_STUBS_KYTHERA_TMP_H
