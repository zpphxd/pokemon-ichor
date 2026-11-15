@ Ichor: stand-ins for labels in the Hoenn-only systems' scripts, which hoenn-cut
@ batch 3 drops (include/config/ichor.h). Kept upstream code still names them.
@ None of it can run: the maps that led there are gone. Texts keep their words.

#if ICHOR_CUT_LINK
CableClub_EventScript_AbortLinkConnectionError::  @ from data/scripts/cable_club.inc
	end

CableClub_EventScript_AbortLinkSomeoneNotReady::  @ from data/scripts/cable_club.inc
	end

CableClub_EventScript_Colosseum::  @ from data/scripts/cable_club.inc
	end

CableClub_EventScript_DirectCornerAttendant::  @ from data/scripts/cable_club.inc
	end

CableClub_EventScript_MysteryGiftMan::  @ from data/scripts/cable_club.inc
	end

CableClub_EventScript_ReadTrainerCard::  @ from data/scripts/cable_club.inc
	end

CableClub_EventScript_ReadTrainerCardColored::  @ from data/scripts/cable_club.inc
	end

CableClub_EventScript_RecordCorner::  @ from data/scripts/cable_club.inc
	end

CableClub_EventScript_TooBusyToNotice::  @ from data/scripts/cable_club.inc
	end

CableClub_EventScript_TradeCenter::  @ from data/scripts/cable_club.inc
	end

CableClub_EventScript_TryBecomeLinkLeader::  @ from data/scripts/cable_club.inc
	end

CableClub_EventScript_TryJoinLinkGroup::  @ from data/scripts/cable_club.inc
	end

CableClub_EventScript_UnionRoomAttendant::  @ from data/scripts/cable_club.inc
	end

CableClub_EventScript_WirelessClubAttendant::  @ from data/scripts/cable_club.inc
	end

CableClub_OnFrame::  @ from data/scripts/cable_club.inc
	end

CableClub_OnLoad::  @ from data/scripts/cable_club.inc
	end

CableClub_OnResume::  @ from data/scripts/cable_club.inc
	end

CableClub_OnTransition::  @ from data/scripts/cable_club.inc
	end

CableClub_OnWarp::  @ from data/scripts/cable_club.inc
	end

EventScript_BattleColosseum_2P_PlayerSpot0::  @ from data/scripts/cable_club.inc
	end

EventScript_BattleColosseum_2P_PlayerSpot1::  @ from data/scripts/cable_club.inc
	end

EventScript_BattleColosseum_4P_PlayerSpot0::  @ from data/scripts/cable_club.inc
	end

EventScript_BattleColosseum_4P_PlayerSpot1::  @ from data/scripts/cable_club.inc
	end

EventScript_BattleColosseum_4P_PlayerSpot2::  @ from data/scripts/cable_club.inc
	end

EventScript_BattleColosseum_4P_PlayerSpot3::  @ from data/scripts/cable_club.inc
	end

EventScript_CableBoxResults::  @ from data/scripts/cable_club.inc
	end

EventScript_ConfirmLeaveCableClubRoom::  @ from data/scripts/cable_club.inc
	end

EventScript_DoLinkRoomExit::  @ from data/scripts/cable_club.inc
	end

EventScript_RecordCenter_Spot0::  @ from data/scripts/cable_club.inc
	end

EventScript_RecordCenter_Spot1::  @ from data/scripts/cable_club.inc
	end

EventScript_RecordCenter_Spot2::  @ from data/scripts/cable_club.inc
	end

EventScript_RecordCenter_Spot3::  @ from data/scripts/cable_club.inc
	end

EventScript_TerminateLink::  @ from data/scripts/cable_club.inc
	end

EventScript_TradeCenter_Chair0::  @ from data/scripts/cable_club.inc
	end

EventScript_TradeCenter_Chair1::  @ from data/scripts/cable_club.inc
	end

EventScript_WirelessBoxResults::  @ from data/scripts/cable_club.inc
	end

#endif

#if ICHOR_CUT_CONTESTS
ContestHall_Movement_Heart::  @ from data/scripts/contest_hall.inc
	end

#endif

#if ICHOR_CUT_SECRET_BASES
SecretBase_Text_Trainer0Defeated::
	.string "$"

SecretBase_Text_Trainer1Defeated::
	.string "$"

SecretBase_Text_Trainer2Defeated::
	.string "$"

SecretBase_Text_Trainer3Defeated::
	.string "$"

SecretBase_Text_Trainer4Defeated::
	.string "$"

SecretBase_Text_Trainer5Defeated::
	.string "$"

SecretBase_Text_Trainer6Defeated::
	.string "$"

SecretBase_Text_Trainer7Defeated::
	.string "$"

SecretBase_Text_Trainer8Defeated::
	.string "$"

SecretBase_Text_Trainer9Defeated::
	.string "$"

SecretBase_EventScript_CaveUseSecretPower::  @ from data/scripts/secret_base.inc
	end

SecretBase_EventScript_CheckEntrance::  @ from data/scripts/secret_base.inc
	end

SecretBase_EventScript_CushionInteract::  @ from data/scripts/secret_base.inc
	end

SecretBase_EventScript_DollInteract::  @ from data/scripts/secret_base.inc
	end

SecretBase_EventScript_Enter::  @ from data/scripts/secret_base.inc
	end

SecretBase_EventScript_InitDecorations::  @ from data/scripts/secret_base.inc
	end

SecretBase_EventScript_PC::  @ from data/scripts/shared_secret_base.inc
	end

SecretBase_EventScript_PCCancel::  @ from data/scripts/shared_secret_base.inc
	end

SecretBase_EventScript_PutAwayDecoration::  @ from data/scripts/secret_base.inc
	end

SecretBase_EventScript_RecordMixingPC::  @ from data/scripts/shared_secret_base.inc
	end

SecretBase_EventScript_SandOrnament::  @ from data/scripts/shared_secret_base.inc
	end

SecretBase_EventScript_SetDecoration::  @ from data/scripts/secret_base.inc
	end

SecretBase_EventScript_ShieldOrToyTV::  @ from data/scripts/shared_secret_base.inc
	end

SecretBase_EventScript_ShowRegisterMenu::  @ from data/scripts/shared_secret_base.inc
	end

SecretBase_EventScript_ShrubUseSecretPower::  @ from data/scripts/secret_base.inc
	end

SecretBase_EventScript_TreeUseSecretPower::  @ from data/scripts/secret_base.inc
	end

#endif

#if ICHOR_CUT_TV
BattleFrontier_BattleTowerLobby_EventScript_Reporter::  @ from data/scripts/interview.inc
	end

BattleFrontier_BattleTowerLobby_EventScript_ShowOrHideReporter::  @ from data/scripts/interview.inc
	end

EventScript_TV::  @ from data/scripts/tv.inc
	end

#endif

@ Stand-ins the test build needs as well (it links some unreachable Hoenn tables).
#if ICHOR_CUT_MAUVILLE_MAN
MauvilleCity_PokemonCenter_1F_Text_BattleTowerChallengesAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_BattleTowerChallengesStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_BattleTowerChallengesTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_BerriesPlantedAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_BerriesPlantedStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_BerriesPlantedTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_BikeTradesAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_BikeTradesStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_BikeTradesTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_CheckedClockAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_CheckedClockStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_CheckedClockTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_CheckedPokedexAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_CheckedPokedexStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_CheckedPokedexTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_EggsHatchedAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_EggsHatchedStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_EggsHatchedTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_EnteredContestsAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_EnteredContestsStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_EnteredContestsTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_FishingPokemonCaughtAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_FishingPokemonCaughtStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_FishingPokemonCaughtTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_HotSpringsAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_HotSpringsStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_HotSpringsTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_InterviewsAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_InterviewsStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_InterviewsTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_LedgesJumpedAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_LedgesJumpedStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_LedgesJumpedTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_MadePokeblocksAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_MadePokeblocksStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_MadePokeblocksTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_MovedBasesAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_MovedBasesStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_MovedBasesTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_PokemonCaughtAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_PokemonCaughtStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_PokemonCaughtTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_PokemonEvolvedAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_PokemonEvolvedStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_PokemonEvolvedTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_ReceivedRibbonsAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_ReceivedRibbonsStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_ReceivedRibbonsTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_RestedAtHomeAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_RestedAtHomeStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_RestedAtHomeTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_RodeCableCarAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_RodeCableCarStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_RodeCableCarTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_RouletteWinsAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_RouletteWinsStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_RouletteWinsTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_SafariGamesAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_SafariGamesStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_SafariGamesTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_SavedGameAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_SavedGameStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_SavedGameTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_SlotJackpotsAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_SlotJackpotsStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_SlotJackpotsTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_TVWatchedAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_TVWatchedStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_TVWatchedTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_TimesRainedAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_TimesRainedStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_TimesRainedTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_TimesShoppedAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_TimesShoppedStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_TimesShoppedTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_TrainerBattlesAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_TrainerBattlesStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_TrainerBattlesTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_TrendsStartedAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_TrendsStartedStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_TrendsStartedTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_UsedCutAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_UsedCutStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_UsedCutTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_UsedDaycareAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_UsedDaycareStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_UsedDaycareTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_UsedItemFinderAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_UsedItemFinderStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_UsedItemFinderTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_UsedPokemonCenterAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_UsedPokemonCenterStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_UsedPokemonCenterTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_UsedRockSmashAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_UsedRockSmashStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_UsedRockSmashTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_UsedSplashAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_UsedSplashStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_UsedSplashTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_UsedStruggleAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_UsedStruggleStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_UsedStruggleTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_WonContestsAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_WonContestsStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_WonContestsTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_WonLotteryAction::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_WonLotteryStory::  @ from data/scripts/mauville_man.inc
	.string "$"

MauvilleCity_PokemonCenter_1F_Text_WonLotteryTitle::  @ from data/scripts/mauville_man.inc
	.string "$"

#endif
