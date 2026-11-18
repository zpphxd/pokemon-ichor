#ifndef GUARD_CONSTANTS_TRADE_H
#define GUARD_CONSTANTS_TRADE_H

#define TRADE_PLAYER  0
#define TRADE_PARTNER 1

// In-game Trade IDs
enum InGameTradeID
{
    INGAME_TRADE_SEEDOT,
    INGAME_TRADE_PLUSLE,
    INGAME_TRADE_HORSEA,
    INGAME_TRADE_MEOWTH,
    // FRLG
    INGAME_TRADE_MR_MIME,
    INGAME_TRADE_JYNX,
    INGAME_TRADE_NIDORAN,
    INGAME_TRADE_FARFETCHD,
    INGAME_TRADE_NIDORINOA,
    INGAME_TRADE_LICKITUNG,
    INGAME_TRADE_ELECTRODE,
    INGAME_TRADE_TANGELA,
    INGAME_TRADE_SEEL,
    // Ichor
    INGAME_TRADE_ICHOR_ARION, // Kimon's Halcyling, for a Galekit (Elaia, Glykera's house)
    INGAME_TRADE_ICHOR_STATER, // Pheidon's Chelonet, for a Karkipool (Aegina, the mint)
    INGAME_TRADE_ICHOR_SOCRATES, // Thaletas's Narkeray, for an Onotis (Emporion, the Deigma)
    INGAME_TRADE_ICHOR_GALANTHIS, // Xenokles's Gelasable, for an Onotis (Route 5, the inn)
    INGAME_TRADE_ICHOR_CRITIC, // Euphorion's Pithound, for a Melibee (Eleusa, Euphorion's house)
    INGAME_TRADE_ICHOR_PATHOS, // Euthykles's Prosomime, for a Gelasable (Thyrsa, the mask workshop)
    INGAME_TRADE_ICHOR_ARKAS, // Hippothoos's Arkoby, for a Gelasable (Arkadia, the charcoal hut)
    INGAME_TRADE_ICHOR_ANKYRA, // Bathykleia's Telkanvil, for a Glyphlet (Skandeia)
    INGAME_TRADE_ICHOR_POTHOS, // Lysis's Himerow, for a Galenyon (Paphia)
    INGAME_TRADE_ICHOR_MALEA, // Lysandros's Kynoketos, for a Karkitox (Gytheion)
    INGAME_TRADE_ICHOR_TELCHIS, // Polypos's Karkitox, for an Aphrell (Amnisos, the fisher's hut)
    INGAME_TRADE_ICHOR_PROPHET, // Koretas's Kerazap, for a Melibee (Delphoi, Koretas's house)
};

// Return values for CanTradeSelectedMon and CanSpinTradeMon
enum CanTradeMon
{
    CAN_TRADE_MON,
    CANT_TRADE_LAST_MON,
    CANT_TRADE_NATIONAL,
    CANT_TRADE_EGG_YET,
    CANT_TRADE_INVALID_MON,
    CANT_TRADE_PARTNER_EGG_YET
};

// Return values for CheckValidityOfTradeMons
#define PLAYER_MON_INVALID   0
#define BOTH_MONS_VALID      1
#define PARTNER_MON_INVALID  2

// Return values for GetGameProgressForLinkTrade
#define TRADE_BOTH_PLAYERS_READY      0
#define TRADE_PLAYER_NOT_READY        1
#define TRADE_PARTNER_NOT_READY       2

// Message indexes for sUnionRoomTradeMessages
#define UR_TRADE_MSG_NONE                         0
#define UR_TRADE_MSG_NOT_MON_PARTNER_WANTS        1
#define UR_TRADE_MSG_NOT_EGG                      2
#define UR_TRADE_MSG_MON_CANT_BE_TRADED_NOW       3
#define UR_TRADE_MSG_MON_CANT_BE_TRADED           4
#define UR_TRADE_MSG_PARTNERS_MON_CANT_BE_TRADED  5
#define UR_TRADE_MSG_EGG_CANT_BE_TRADED           6
#define UR_TRADE_MSG_PARTNER_CANT_ACCEPT_MON      7
#define UR_TRADE_MSG_CANT_TRADE_WITH_PARTNER_1    8
#define UR_TRADE_MSG_CANT_TRADE_WITH_PARTNER_2    9

// Return values for CanRegisterMonForTradingBoard
#define CAN_REGISTER_MON      0
#define CANT_REGISTER_MON_NOW 1
#define CANT_REGISTER_MON     2
#define CANT_REGISTER_EGG     3


#endif //GUARD_CONSTANTS_TRADE_H
