.macro def_special, ptr:req, requests_effects=0, waitstate=0
.if ALLOCATE_SPECIAL_TABLE
	.global SPECIAL_\ptr
	.set SPECIAL_\ptr, __special__
	.if \requests_effects == 0
		.4byte \ptr
	.else
		.4byte \ptr + ROM_SIZE
	.endif
.endif
.set SPECIAL_WAITSTATE_\ptr, \waitstate
.set __special__, __special__ + 1
.endm

.set __special__, 0
.if ALLOCATE_SPECIAL_TABLE
		.align 2
gSpecials::
.endif
	def_special HealPlayerParty
	def_special SetCableClubWarp
	def_special DoCableClubWarp, waitstate=1
	def_special ReturnFromLinkRoom, waitstate=1
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special CleanupLinkRoomState
#endif
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special ExitLinkRoom
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special SetPlayerSecretBase
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special CheckPlayerHasSecretBase
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special EnterSecretBase
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special ClearAndLeaveSecretBase
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special MoveOutOfSecretBase
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special IsCurSecretBaseOwnedByAnotherPlayer
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special GetCurSecretBaseRegistrationValidity
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special ToggleCurSecretBaseRegistry
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special ShowSecretBaseDecorationMenu
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special ShowSecretBaseRegistryMenu
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special PrepSecretBaseBattleFlags
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special GetSecretBaseOwnerAndState
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special InitSecretBaseDecorationSprites
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special SetDecoration
#endif
	def_special GetObjectEventLocalIdByFlag
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special GetSecretBaseTypeInFrontOfPlayer
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special SetSecretBaseOwnerGfxId
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special PutAwayDecorationIteration
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special EnterNewlyCreatedSecretBase, waitstate=1
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special SetBattledOwnerFromResult
#endif
	def_special DoSecretBasePCTurnOffEffect
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special RecordMixingPlayerSpotTriggered, waitstate=1
#endif
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special TryBattleLinkup, waitstate=1
#endif
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special TryTradeLinkup, waitstate=1
#endif
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special TryRecordMixLinkup, waitstate=1
#endif
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special ValidateMixingGameLanguage, waitstate=1
#endif
	def_special CloseLink
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special ColosseumPlayerSpotTriggered, waitstate=1
#endif
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special PlayerEnteredTradeSeat, waitstate=1
#endif
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special Script_StartWiredTrade
#endif
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special CableClubSaveGame
#endif
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special TryBerryBlenderLinkup, waitstate=1
#endif
	def_special GetLinkPartnerNames
	def_special SpawnLinkPartnerObjectEvent
	def_special SavePlayerParty
	def_special LoadPlayerParty
	def_special ChooseHalfPartyForBattle, waitstate=1
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special Script_ShowLinkTrainerCard, waitstate=1
#endif
	def_special ObjectEventInteractionGetBerryTreeData
	def_special ObjectEventInteractionGetBerryName
	def_special ObjectEventInteractionGetBerryCountString
	def_special Bag_ChooseBerry, waitstate=1
	def_special ObjectEventInteractionPlantBerryTree
	def_special ObjectEventInteractionPickBerryTree
	def_special ObjectEventInteractionRemoveBerryTree
	def_special ObjectEventInteractionWaterBerryTree
	def_special PlayerHasBerries
	def_special IsEnigmaBerryValid
	def_special ShowTrainerIntroSpeech
	def_special ShowTrainerCantBattleSpeech
	def_special GetTrainerFlag
	def_special DoTrainerApproach, waitstate=1
	def_special PlayTrainerEncounterMusic
	def_special ShouldTryRematchBattle
	def_special IsTrainerReadyForRematch
	def_special BattleSetup_StartRematchBattle, waitstate=1
	def_special ShowPokemonStorageSystemPC, waitstate=1
	def_special HasEnoughMonsForDoubleBattle
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special TurnOffTVScreen
#endif
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special DoTVShow
#endif
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special DoPokeNews
#endif
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special GetRandomActiveShowIdx
#endif
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special GetSelectedTVShow
#endif
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special InterviewBefore
#endif
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special InterviewAfter
#endif
	def_special IsLeadMonNicknamedOrNotEnglish
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special SetContestCategoryStringVarForInterview
#endif
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special IsTVShowAlreadyInQueue
#endif
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special CheckForPlayersHouseNews
#endif
	def_special GetMomOrDadStringForTVMessage
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special ResetTVShowState
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special GetContestWinnerId
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special GetContestPlayerId
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special GetNpcContestantLocalId
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special BufferContestWinnerTrainerName
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special BufferContestWinnerMonName
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special BufferContestTrainerAndMonNames
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special GetContestMonConditionRanking
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special SetContestTrainerGfxIds
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special TryEnterContestMon
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special GetContestantNamesAtRank
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special SetLinkContestPlayerGfx
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special GetContestMonCondition
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special HasMonWonThisContestBefore
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special GiveMonContestRibbon
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special IsContestDebugActive
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special GiveMonArtistRibbon
#endif
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special TryContestGModeLinkup, waitstate=1
#endif
	def_special SaveGame, waitstate=1
	def_special DoWateringBerryTreeAnim, waitstate=1
	def_special ShowEasyChatScreen
	def_special ShowEasyChatProfile
#if !ICHOR_CUT_MAUVILLE_MAN // Ichor: the Mauville Old Man is cut
	def_special Script_GetCurrentMauvilleMan
#endif
#if !ICHOR_CUT_MAUVILLE_MAN // Ichor: the Mauville Old Man is cut
	def_special HasBardSongBeenChanged
#endif
#if !ICHOR_CUT_MAUVILLE_MAN // Ichor: the Mauville Old Man is cut
	def_special SaveBardSongLyrics
#endif
#if !ICHOR_CUT_MAUVILLE_MAN // Ichor: the Mauville Old Man is cut
	def_special HasHipsterTaughtWord
#endif
#if !ICHOR_CUT_MAUVILLE_MAN // Ichor: the Mauville Old Man is cut
	def_special SetHipsterTaughtWord
#endif
#if !ICHOR_CUT_MAUVILLE_MAN // Ichor: the Mauville Old Man is cut
	def_special HipsterTryTeachWord
#endif
#if !ICHOR_CUT_MAUVILLE_MAN // Ichor: the Mauville Old Man is cut
	def_special PlayBardSong
#endif
#if !ICHOR_CUT_MAUVILLE_MAN // Ichor: the Mauville Old Man is cut
	def_special SetMauvilleOldManObjEventGfx
#endif
#if !ICHOR_CUT_MAUVILLE_MAN // Ichor: the Mauville Old Man is cut
	def_special GenerateGiddyLine
#endif
#if !ICHOR_CUT_MAUVILLE_MAN // Ichor: the Mauville Old Man is cut
	def_special GiddyShouldTellAnotherTale
#endif
#if !ICHOR_CUT_MAUVILLE_MAN // Ichor: the Mauville Old Man is cut
	def_special StorytellerGetFreeStorySlot
#endif
#if !ICHOR_CUT_MAUVILLE_MAN // Ichor: the Mauville Old Man is cut
	def_special Script_StorytellerDisplayStory
#endif
#if !ICHOR_CUT_MAUVILLE_MAN // Ichor: the Mauville Old Man is cut
	def_special StorytellerStoryListMenu, waitstate=1
#endif
#if !ICHOR_CUT_MAUVILLE_MAN // Ichor: the Mauville Old Man is cut
	def_special StorytellerUpdateStat
#endif
#if !ICHOR_CUT_MAUVILLE_MAN // Ichor: the Mauville Old Man is cut
	def_special Script_StorytellerInitializeRandomStat
#endif
#if !ICHOR_CUT_MAUVILLE_MAN // Ichor: the Mauville Old Man is cut
	def_special HasStorytellerAlreadyRecorded
#endif
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special TraderMenuGetDecoration, waitstate=1
#endif
	def_special GetTraderTradedFlag
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special DoesPlayerHaveNoDecorations
#endif
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special IsDecorationCategoryFull
#endif
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special TraderShowDecorationMenu, waitstate=1
#endif
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special TraderDoDecorationTrade
#endif
	def_special GetSeedotSizeRecordInfo
	def_special CompareSeedotSize
	def_special GetLotadSizeRecordInfo
	def_special CompareLotadSize
	def_special TryPutNameRaterShowOnTheAir
	def_special BufferMonNickname
	def_special IsMonOTIDNotPlayers
	def_special BufferTrendyPhraseString
	def_special IsTrendyPhraseBoring
	def_special BufferDeepLinkPhrase
	def_special GetDewfordHallPaintingNameIndex
	def_special SwapRegisteredBike
	def_special CalculatePlayerPartyCount
	def_special CountPartyNonEggMons
	def_special CountPartyAliveNonEggMons_IgnoreVar0x8004Slot
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special ShouldReadyContestArtist
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special SaveMuseumContestPainting
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special DoesContestCategoryHaveMuseumPainting
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special CountPlayerMuseumPaintings
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special ShowContestPainting  @ Unused, redundant with showcontestpainting command
#endif
	def_special MauvilleGymSetDefaultBarriers
	def_special MauvilleGymPressSwitch
	def_special ShowFieldMessageStringVar4
	def_special DrawWholeMapView
	def_special StorePlayerCoordsInVars
	def_special MauvilleGymDeactivatePuzzle
	def_special PetalburgGymSlideOpenRoomDoors, waitstate=1
	def_special PetalburgGymUnlockRoomDoors
	def_special GetPlayerTrainerIdOnesDigit
	def_special GetPlayerBigGuyGirlString
	def_special GetRivalSonDaughterString
	def_special SetHiddenItemFlag
	def_special CableCarWarp
	def_special CableCar, waitstate=1
	def_special Overworld_PlaySpecialMapMusic
	def_special StartWallClock, waitstate=1
	def_special Special_ViewWallClock, waitstate=1
	def_special ChooseStarter, waitstate=1
	def_special StartWallyTutorialBattle, waitstate=1
	def_special ChangePokemonNickname, waitstate=1
	def_special ChoosePartyMon, waitstate=1
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special GetFirstFreePokeblockSlot
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special DoBerryBlending, waitstate=1
#endif
#if !ICHOR_CUT_MINIGAMES // Ichor: the minigames are cut
	def_special PlayRoulette, waitstate=1
#endif
	def_special IsFanClubMemberFanOfPlayer
	def_special GetNumFansOfPlayerInTrainerFanClub
	def_special BufferFanClubTrainerName
	def_special TryLoseFansFromPlayTimeAfterLinkBattle
	def_special TryLoseFansFromPlayTime
	def_special SetPlayerGotFirstFans
	def_special UpdateTrainerFanClubGameClear
	def_special Script_TryGainNewFanFromCounter
	def_special RockSmashWildEncounter
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special GabbyAndTyGetBattleNum
#endif
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special GabbyAndTyAfterInterview
#endif
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special GabbyAndTyBeforeInterview
#endif
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special DoTVShowInSearchOfTrainers
#endif
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special IsGabbyAndTyShowOnTheAir
#endif
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special GabbyAndTyGetLastQuote
#endif
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special GabbyAndTyGetLastBattleTrivia
#endif
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special GetGabbyAndTyLocalIds
#endif
	def_special GetBattleOutcome
	def_special GetDaycareMonNicknames
	def_special GetDaycareState
	def_special RejectEggFromDayCare
	def_special GiveEggFromDaycare
	def_special SetDaycareCompatibilityString
	def_special GetSelectedMonNicknameAndSpecies
	def_special StoreSelectedPokemonInDaycare
	def_special ChooseSendDaycareMon, waitstate=1
	def_special ShowDaycareLevelMenu, waitstate=1
	def_special GetNumLevelsGainedFromDaycare
	def_special GetDaycareCostAndPrepareString
	def_special TakePokemonFromDaycare
	def_special ScriptHatchMon
	def_special EggHatch, waitstate=1
	def_special CheckDaycareMonReceivedMail
	def_special ShowLinkBattleRecords
	def_special IsEnoughForCostInVar0x8005
	def_special SubtractMoneyFromVar0x8005
	def_special TryFieldPoisonWhiteOut, waitstate=1
	def_special SetCB2WhiteOut, waitstate=1
	def_special RotatingGate_InitPuzzle
	def_special RotatingGate_InitPuzzleAndGraphics
	def_special SetSSTidalFlag
	def_special ResetSSTidalFlag
	def_special EnterSafariMode
	def_special ExitSafariMode
	def_special GetPokeblockFeederInFront
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special OpenPokeblockCaseOnFeeder, waitstate=1
#endif
	def_special IsMirageIslandPresent
	def_special UpdateShoalTideFlag
	def_special InitBirchState
	def_special ScriptGetPokedexInfo
	def_special ShowPokedexRatingMessage
	def_special DoPCTurnOnEffect
	def_special DoPCTurnOffEffect
	def_special SetDeptStoreFloor
	def_special DoLotteryCornerComputerEffect
	def_special EndLotteryCornerComputerEffect
	def_special ChooseMonForMoveRelearner, waitstate=1
	def_special MoveDeleterChooseMoveToForget
	def_special MoveDeleterForgetMove
	def_special BufferMoveDeleterNicknameAndMove
	def_special GetNumMovesSelectedMonHas
	def_special TeachMoveRelearnerMove, waitstate=1
	def_special GetRecordedCyclingRoadResults
	def_special Special_BeginCyclingRoadChallenge
	def_special GetPlayerAvatarBike
	def_special FinishCyclingRoadChallenge
	def_special UpdateCyclingRoadState
	def_special GetLeadMonFriendshipScore
	def_special CallFrontierUtilFunc
	def_special CallBattleTowerFunc
	def_special CallBattleDomeFunction
	def_special CallBattlePalaceFunction
	def_special CopyEReaderTrainerGreeting
	def_special DoSpecialTrainerBattle, waitstate=1
	def_special CallBattleArenaFunction
	def_special CallBattleFactoryFunction
	def_special CallBattlePikeFunction
	def_special CallBattlePyramidFunction
	def_special StopMapMusic
	def_special CallVerdanturfTentFunction
	def_special CallFallarborTentFunction
	def_special CallSlateportTentFunction
	def_special ChoosePartyForBattleFrontier, waitstate=1
	def_special ValidateEReaderTrainer
	def_special GetBattleTowerSinglesStreak
	def_special ReducePlayerPartyToSelectedMons
	def_special BedroomPC, waitstate=1
	def_special PlayerPC, waitstate=1
	def_special FieldShowRegionMap, waitstate=1
	def_special GetInGameTradeSpeciesInfo
	def_special CreateInGameTradePokemon
	def_special DoInGameTradeScene, waitstate=1
	def_special GetTradeSpecies
	def_special GetWeekCount
#if !ICHOR_CUT_MINIGAMES // Ichor: the minigames are cut
	def_special RetrieveLotteryNumber
#endif
#if !ICHOR_CUT_MINIGAMES // Ichor: the minigames are cut
	def_special PickLotteryCornerTicket
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special ShowBerryBlenderRecordWindow
#endif
	def_special ResetTrickHouseNuggetFlag
	def_special SetTrickHouseNuggetFlag
	def_special ScriptMenu_CreatePCMultichoice, waitstate=1
	def_special AccessHallOfFamePC, waitstate=1
	def_special Special_ShowDiploma, waitstate=1
	def_special CheckLeadMonCool
	def_special CheckLeadMonBeauty
	def_special CheckLeadMonCute
	def_special CheckLeadMonSmart
	def_special CheckLeadMonTough
	def_special LookThroughPorthole, waitstate=1
	def_special DoSoftReset
	def_special GameClear, waitstate=1
	def_special MoveElevator, waitstate=1
	def_special ShowGlassWorkshopMenu
	def_special SpawnCameraObject
	def_special RemoveCameraObject
	def_special GetPokeblockNameByMonNature
	def_special GetSecretBaseNearbyMapName
	def_special CheckRelicanthWailord
	def_special ShouldDoBrailleRegirockEffectOld
	def_special DoOrbEffect
	def_special FadeOutOrbEffect, waitstate=1
	def_special WaitWeather, waitstate=1
	def_special BufferEReaderTrainerName
	def_special GetSlotMachineId
	def_special GetPlayerFacingDirection, requests_effects=TRUE
	def_special FoundAbandonedShipRoom1Key
	def_special FoundAbandonedShipRoom2Key
	def_special FoundAbandonedShipRoom4Key
	def_special FoundAbandonedShipRoom6Key
	def_special LeadMonHasEffortRibbon
	def_special GiveLeadMonEffortRibbon
	def_special Special_AreLeadMonEVsMaxedOut
	def_special Script_FacePlayer
	def_special Script_ClearHeldMovement
	def_special InitRoamer
	def_special TryUpdateRusturfTunnelState
	def_special IsGrassTypeInParty
	def_special DoContestHallWarp, waitstate=1
	def_special LoadWallyZigzagoon
	def_special IsStarterInParty
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special CopyCurSecretBaseOwnerName_StrVar1
#endif
	def_special ScriptCheckFreePokemonStorageSpace
	def_special DoSealedChamberShakingEffect_Long, waitstate=1
	def_special ShowDeptStoreElevatorFloorSelect
	def_special InteractWithShieldOrTVDecoration
	def_special IsPokerusInParty
	def_special SetSootopolisGymCrackedIceMetatiles
	def_special ShakeCamera
	def_special StartGroudonKyogreBattle
	def_special BattleSetup_StartLegendaryBattle, waitstate=1
	def_special StartRegiBattle, waitstate=1
	def_special SetTrainerFacingDirection
	def_special DoSealedChamberShakingEffect_Short, waitstate=1
	def_special FoundBlackGlasses
	def_special StartDroughtWeatherBlend
	def_special DoDiveWarp
	def_special DoFallWarp, waitstate=1
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special ShowContestEntryMonPic
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special HideContestEntryMonPic
#endif
	def_special SetEReaderTrainerGfxId
	def_special BattleSetup_StartLatiBattle, waitstate=1
	def_special SetRoute119Weather
	def_special SetRoute123Weather
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special GetContestMultiplayerId
#endif
	def_special ScriptGetPartyMonSpecies
	def_special IsSelectedMonEgg
	def_special Special_HasMoveToRelearn
	def_special TryInitBattleTowerAwardManObjectEvent
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special MoveOutOfSecretBaseFromOutside
#endif
	def_special LoadPlayerBag
	def_special Script_FadeOutMapMusic, waitstate=1
	def_special SetPacifidlogTMReceivedDay
	def_special GetDaysUntilPacifidlogTMAvailable
	def_special HasAllHoennMons
	def_special MonOTNameNotPlayer
	def_special BufferLottoTicketNumber
	def_special TryHideBattleTowerReporter
	def_special DoesPartyHaveEnigmaBerry
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special GenerateContestRand
#endif
	def_special SetChampionSaveWarp
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special TryPutTreasureInvestigatorsOnAir
#endif
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special TryPutLotteryWinnerReportOnAir
#endif
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special TryPutTrainerFanClubOnAir
#endif
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special ShouldHideFanClubInterviewer
#endif
	def_special ShowGlassWorkshopMenu
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special PutFanClubSpecialOnTheAir
#endif
	def_special IncrementDailyPlantedBerries
	def_special IncrementDailyPickedBerries
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special InitSecretBaseVars
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special CheckInteractedWithFriendsSandOrnament
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special DeclinedSecretBaseBattle
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special DrewSecretBaseBattle
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special WonSecretBaseBattle
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special LostSecretBaseBattle
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special CheckInteractedWithFriendsDollDecor
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special CheckInteractedWithFriendsCushionDecor
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special CheckInteractedWithFriendsFurnitureBottom
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special CheckInteractedWithFriendsFurnitureMiddle
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special CheckInteractedWithFriendsFurnitureTop
#endif
#if !ICHOR_CUT_SECRET_BASES // Ichor: secret bases and decorations are cut
	def_special CheckInteractedWithFriendsPosterDecor
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special SetLilycoveLadyGfx
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special Script_GetLilycoveLadyId
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special GetFavorLadyState
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special BufferFavorLadyRequest
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special HasAnotherPlayerGivenFavorLadyItem
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special BufferFavorLadyItemName
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special BufferFavorLadyPlayerName
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special DidFavorLadyLikeItem
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special Script_FavorLadyOpenBagMenu, waitstate=1
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special Script_DoesFavorLadyLikeItem
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special IsFavorLadyThresholdMet
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special FavorLadyGetPrize
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special SetFavorLadyState_Complete
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special GetQuizLadyState
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special GetQuizAuthor
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special IsQuizLadyWaitingForChallenger
#endif
	def_special QuizLadyShowQuizQuestion, waitstate=1
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special QuizLadyGetPlayerAnswer, waitstate=1
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special IsQuizAnswerCorrect
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special BufferQuizPrizeItem
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special SetQuizLadyState_Complete
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special BufferQuizAuthorNameAndCheckIfLady
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special SetQuizLadyState_GivePrize
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special ClearQuizLadyPlayerAnswer
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special Script_QuizLadyOpenBagMenu, waitstate=1
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special ClearQuizLadyQuestionAndAnswer
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special QuizLadySetCustomQuestion, waitstate=1
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special QuizLadyTakePrizeForCustomQuiz
#endif
	def_special GetMysteryGiftCardStat
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special QuizLadyRecordCustomQuizData
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special QuizLadySetWaitingForChallenger
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special BufferQuizCorrectAnswer
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special BufferQuizPrizeName
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special QuizLadyPickNewQuestion
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special ShouldContestLadyShowGoOnAir
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special HasPlayerGivenContestLadyPokeblock
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special Script_BufferContestLadyCategoryAndMonName
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special OpenPokeblockCaseForContestLady, waitstate=1
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special SetContestLadyGivenPokeblock
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special GetContestLadyMonSpecies
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special GetContestLadyCategory
#endif
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special PutLilycoveContestLadyShowOnTheAir
#endif
	def_special CloseBattlePikeCurtain, waitstate=1
	def_special CallApprenticeFunction
	def_special ShouldTryGetTrainerScript
	def_special ShowMapNamePopup
	def_special ShowMapNamePopup
#if !ICHOR_CUT_MIRAGE_TOWER // Ichor: Mirage Tower is cut
	def_special DoMirageTowerCeilingCrumble, waitstate=1
#endif
#if !ICHOR_CUT_MIRAGE_TOWER // Ichor: Mirage Tower is cut
	def_special SetMirageTowerVisibility
#endif
#if !ICHOR_CUT_MIRAGE_TOWER // Ichor: Mirage Tower is cut
	def_special StartPlayerDescendMirageTower, waitstate=1
#endif
	def_special BufferTMHMMoveName
	def_special IsWirelessAdapterConnected
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special TryBecomeLinkLeader, waitstate=1
#endif
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special TryJoinLinkGroup, waitstate=1
#endif
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special RunUnionRoom
#endif
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special ShowWirelessCommunicationScreen, waitstate=1
#endif
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special InitUnionRoom
#endif
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special BufferUnionRoomPlayerName
#endif
#if !ICHOR_CUT_MYSTERY_GIFT // Ichor: Mystery Gift is cut
	def_special WonderNews_GetRewardInfo
#endif
	def_special ChooseMonForWirelessMinigame, waitstate=1
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special Script_ResetUnionRoomTrade
#endif
	def_special IsBadEggInParty
#if !ICHOR_CUT_MYSTERY_GIFT // Ichor: Mystery Gift is cut
	def_special ValidateSavedWonderCard
#endif
	def_special HasAtLeastOneBerry
#if !ICHOR_CUT_MINIGAMES // Ichor: the minigames are cut
	def_special IsPokemonJumpSpeciesInParty
#endif
#if !ICHOR_CUT_MINIGAMES // Ichor: the minigames are cut
	def_special ShowPokemonJumpRecords, waitstate=1
#endif
#if !ICHOR_CUT_MINIGAMES // Ichor: the minigames are cut
	def_special IsDodrioInParty
#endif
#if !ICHOR_CUT_MINIGAMES // Ichor: the minigames are cut
	def_special ShowDodrioBerryPickingRecords, waitstate=1
#endif
	def_special OffsetCameraForBattle
	def_special GetDeptStoreDefaultFloorChoice
	def_special BufferVarsForIVRater
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special LinkContestWaitForConnection, waitstate=1
#endif
	def_special GetWirelessCommType
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special LinkContestTryShowWirelessIndicator
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special LinkContestTryHideWirelessIndicator
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special IsWirelessContest
#endif
	def_special ShowRankingHallRecordsWindow
	def_special ScrollRankingHallRecordsWindow
	def_special ShowFrontierManiacMessage
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special IsContestWithRSPlayer
#endif
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special ClearLinkContestFlags
#endif
#if !ICHOR_CUT_LINK // Ichor: link features are cut
	def_special TryContestEModeLinkup, waitstate=1
#endif
	def_special ShowScrollableMultichoice, waitstate=1
	def_special ScrollableMultichoice_TryReturnToList
	def_special BufferBattleTowerElevatorFloors
	def_special TryStoreHeldItemsInPyramidBag
	def_special ChooseItemsToTossFromPyramidBag, waitstate=1
	def_special DoBattlePyramidMonsHaveHeldItem
	def_special BattlePyramidChooseMonHeldItems, waitstate=1
	def_special SetBattleTowerLinkPlayerGfx
	def_special ShowNatureGirlMessage
	def_special ShowBattlePointsWindow
	def_special UpdateBattlePointsWindow
	def_special CloseBattlePointsWindow
	def_special GiveFrontierBattlePoints
	def_special TakeFrontierBattlePoints
	def_special GetFrontierBattlePoints
	def_special ShowFrontierExchangeCornerItemIconWindow
	def_special CloseFrontierExchangeCornerItemIconWindow
	def_special DisplayBerryPowderVendorMenu
	def_special RemoveBerryPowderVendorMenu
	def_special HasEnoughBerryPowder
	def_special TakeBerryPowder
	def_special PrintPlayerBerryPowderAmount
	def_special ShowFrontierGamblerLookingMessage
	def_special ShowFrontierGamblerGoMessage
	def_special Script_DoRayquazaScene, waitstate=1
#if !ICHOR_CUT_POKENAV // Ichor: the PokéNav is cut
	def_special OpenPokenavForTutorial, waitstate=1
#endif
	def_special ScriptMenu_CreateStartMenuForPokenavTutorial, waitstate=1
	def_special CountPlayerTrainerStars
	def_special BufferBattleFrontierTutorMoveName
	def_special CloseBattleFrontierTutorWindow
	def_special ScrollableMultichoice_RedrawPersistentMenu
	def_special ChooseMonForMoveTutor, waitstate=1
	def_special ScrollableMultichoice_ClosePersistentMenu
	def_special DoDeoxysRockInteraction, waitstate=1
	def_special SetDeoxysRockPalette
	def_special CreateEnemyEventMon
#if !ICHOR_CUT_MIRAGE_TOWER // Ichor: Mirage Tower is cut
	def_special StartMirageTowerDisintegration, waitstate=1
#endif
#if !ICHOR_CUT_MIRAGE_TOWER // Ichor: Mirage Tower is cut
	def_special StartMirageTowerShake, waitstate=1
#endif
#if !ICHOR_CUT_MIRAGE_TOWER // Ichor: Mirage Tower is cut
	def_special StartMirageTowerFossilFallAndSink, waitstate=1
#endif
	def_special GetPCBoxToSendMon
	def_special ShouldShowBoxWasFullMessage
#if !ICHOR_CUT_POKENAV // Ichor: the PokéNav is cut
	def_special SetMatchCallRegisteredFlag
#endif
	def_special DoDomeConfetti
	def_special CreateAbnormalWeatherEvent
	def_special GetAbnormalWeatherMapNameAndType
	def_special GetMartEmployeeObjectEventId
	def_special SaveForBattleTowerLink, waitstate=1
	def_special Unused_SetWeatherSunny
	def_special SetUnlockedPokedexFlags
	def_special IsTrainerRegistered
	def_special ShouldDoBrailleRegicePuzzle
	def_special EnableNationalPokedex
	def_special ScriptMenu_CreateLilycoveSSTidalMultichoice, waitstate=1
	def_special GetLilycoveSSTidalSelection
#if !ICHOR_CUT_TV // Ichor: TV is cut
	def_special TurnOnTVScreen
#endif
	def_special SetMewAboveGrass
	def_special ShouldDistributeEonTicket
	def_special LinkRetireStatusWithBattleTowerPartner, waitstate=1
	def_special BattleTowerReconnectLink
	def_special CallTrainerHillFunction
	def_special Script_DoRayquazaScene, waitstate=1 @ Listed twice
	def_special LoopWingFlapSE
	def_special DestroyMewEmergingGrassSprite
#if !ICHOR_CUT_MINIGAMES // Ichor: the minigames are cut
	def_special ShowBerryCrushRankings, waitstate=1
#endif
	def_special TryBufferWaldaPhrase
	def_special DoWaldaNamingScreen, waitstate=1
	def_special TryGetWallpaperWithWaldaPhrase
	def_special PlayerNotAtTrainerHillEntrance
	def_special GetBattlePyramidHint
#if !ICHOR_CUT_CONTESTS // Ichor: contests, the Berry Blender and Pokéblocks are cut
	def_special LoadLinkContestPlayerPalettes
#endif
	def_special ShowTrainerHillRecords, waitstate=1
	def_special PlayerFaceTrainerAfterBattle
	def_special ResetHealLocationFromDewford
	def_special IsLastMonThatKnowsSurf
	def_special CountPartyAliveNonEggMons
	def_special TryPrepareSecondApproachingTrainer
	def_special PrepareSecondApproachingTrainer
	def_special RemoveRecordsWindow
	def_special CloseDeptStoreElevatorWindow
	def_special TrySetBattleTowerLinkType
	def_special GetNumberSprayStrength
	def_special GetSprayId
	def_special GetLastUsedSprayType
	def_special TrySkyBattle
	def_special VsSeekerResetObjectMovementAfterChargeComplete
	def_special VsSeekerFreezeObjectsAfterChargeComplete
	def_special PlayerHasMulch
	def_special Bag_ChooseMulch
	def_special ObjectEventInteractionApplyMulch
	def_special ObjectEventInteractionPullBerryWeed
	def_special ObjectEventInteractionClearBerryPests
	def_special ObjectEventInteractionBerryHasWeed
	def_special ObjectEventInteractionBerryHasPests
	def_special CanWaterBerryPlot
	def_special Script_GetChosenMonOffensiveEVs
	def_special Script_GetChosenMonDefensiveEVs
	def_special Script_GetChosenMonOffensiveIVs
	def_special Script_GetChosenMonDefensiveIVs
	def_special UseBlankMessageToCancelPokemonPic
	def_special EnterCode
	def_special GetCodeFeedback
	def_special SetHiddenNature
	def_special SetAbility
	def_special CanTeachMoveBoxMon
	def_special ObjectEventInteractionGetApricornTreeData
	def_special ObjectEventInteractionPickApricornTree
	def_special GetFrlgPokedexCount
	def_special HasAllMons
	def_special GetProfOaksRatingMessage
	def_special UpdatePickStateFromSpecialVar8005
	def_special SetFlavorTextFlagFromSpecialVars
	def_special DisableMsgBoxWalkaway
	def_special SetWalkingIntoSignVars
	def_special StartOldManTutorialBattle
	def_special DaisyMassageServices
	def_special GetLeadMonFriendship
	def_special OpenMuseumFossilPic
	def_special CloseMuseumFossilPic
	def_special CapeBrinkGetMoveToTeachLeadPokemon
	def_special HasLearnedAllMovesFromCapeBrinkTutor
	def_special SetSeenMon
	def_special AnimateTeleporterHousing
	def_special AnimateTeleporterCable
	def_special IsThereMonInRoute5Daycare
	def_special PutMonInRoute5Daycare
	def_special GetNumLevelsGainedForRoute5DaycareMon
	def_special TakePokemonFromRoute5Daycare
	def_special GetCostToWithdrawRoute5DaycareMon
	def_special DrawSeagallopDestinationMenu
	def_special GetSelectedSeagallopDestination
	def_special GetSeagallopNumber
	def_special DoSeagallopFerryScene
	def_special IsPlayerLeftOfVermilionSailor
	def_special SetVermilionTrashCans
	def_special DoSSAnneDepartureCutscene
	def_special StartMarowakBattle
	def_special DoesPlayerPartyContainSpecies
	def_special GetMagikarpSizeRecordInfo
	def_special CompareMagikarpSize
	def_special GetHeracrossSizeRecordInfo
	def_special CompareHeracrossSize
	def_special GetRandomSlotMachineId
	def_special HasAllKantoMons
	def_special AnimateElevator
	def_special InitElevatorFloorSelectMenuPos
	def_special CloseElevatorCurrentFloorWindow
	def_special DrawElevatorCurrentFloorWindow
	def_special GetElevatorFloor
	def_special ForcePlayerOntoBike
	def_special Script_IsFanClubMemberFanOfPlayer
	def_special Script_GetNumFansOfPlayerInTrainerFanClub
	def_special Script_BufferFanClubTrainerName
	def_special Script_TryLoseFansFromPlayTimeAfterLinkBattle
	def_special Script_TryLoseFansFromPlayTime
	def_special Script_SetPlayerGotFirstFans
	def_special Script_UpdateTrainerFanClubGameClear
	def_special Script_TryGainNewFanFromCounterFrlg
	def_special IsNationalPokedexEnabled
	def_special SetPostgameFlags
	def_special IsPlayerNotInTrainerTowerLobby
	def_special BrailleCursorToggle
	def_special EnterHallOfFame
	def_special CB2_StartCreditsSequence
	def_special DoPokemonLeagueLightingEffect
	def_special GetStarterPokemon
	def_special SetIcefallCaveCrackedIceMetatiles
	def_special UpdateLoreleiDollCollection
	def_special SampleResortGorgeousMonAndReward
	def_special PlayerPartyContainsSpeciesWithPlayerID
	def_special ShakeScreen
	def_special CallTrainerTowerFunc
	def_special ForcePlayerToStartSurfing
	def_special SeafoamIslandsB4F_CurrentDumpsPlayerOnLand
	def_special UpdateTrainerCardPhotoIcons
	def_special StickerManGetBragFlags
	def_special CheckAddCoins
	def_special Ichor_SetHoursOverride
	def_special Ichor_ShowTabletPicture
	def_special Ichor_HideScenePicture
	def_special Ichor_ShowActOneCard
	def_special Ichor_HideActOneCard
	def_special Ichor_ChooseDifficulty
	def_special Ichor_ChooseStartingOath
	def_special Ichor_GetStepGlassLimit
	def_special Ichor_GetStepGlassHalf
	@ Ichor: relics (src/ichor_relics.c)
	def_special Ichor_CanUseRelic
	def_special Ichor_RelicPromptsAuto
	def_special Ichor_RelicPose, waitstate=1
	def_special Ichor_FollowerHop
	def_special Ichor_CheckFlagInVar
	def_special Ichor_SetFlagInVar
	def_special Ichor_AnimateTorchFlash, waitstate=1
	def_special Ichor_IsInDarkMap
	def_special Ichor_SetTorchDoused
	def_special Ichor_ClearFog
	def_special Ichor_BuildRelicRing
	def_special Ichor_UseRingChoice
	@ Ichor: rites (src/ichor_rites.c)
	def_special Ichor_AddFavor
	def_special Ichor_GetFavorOf
	def_special Ichor_GetBlessingGod
	def_special Ichor_GrantBlessing
	def_special Ichor_BuildOfferingMenu
	def_special Ichor_BufferAltar
	def_special Ichor_BuildAltarMenu
	def_special Ichor_CheckBlessingConflict
	def_special Ichor_Pray
	def_special Ichor_MakeOffering
	def_special Ichor_BufferFavor
	def_special Ichor_NextGiftDue
	def_special Ichor_TakeGift
	def_special Ichor_BufferLesson
	def_special Ichor_GetLovedOffering
	def_special Ichor_UseHearthfire
	def_special Ichor_HasHearthfire
	def_special Ichor_CheckGiftTaken
	def_special Ichor_CheckAltarCleansed
	def_special Ichor_CleanseAltar
	def_special Ichor_AresVictory
	@ Ichor: herm waystones (src/ichor_herms.c)
	def_special Ichor_CountHerms
	def_special Ichor_GetHermState
	def_special Ichor_AnointHerm
	@ Ichor: the Frozen Hour (src/ichor_frozen.c)
	def_special Ichor_FrozenHourBegin, waitstate=1
	def_special Ichor_UnfreezeObject
	def_special Ichor_SepiaMemoryBegin
	def_special Ichor_SepiaMemoryEnd
	def_special Ichor_ColorReturnStep
	def_special Ichor_FrozenScriptsHere
	@ Ichor: carried flames (src/ichor_relics.c)
	def_special Ichor_TakeFlame
	def_special Ichor_PutOutFlame
	def_special Ichor_GetFlameKind
	def_special Ichor_GetFlameSteps
	def_special Ichor_FrozenGenericLine
	@ Ichor: the Labyrinth (src/ichor_labyrinth.c)
	def_special Ichor_AddThreadFloor
	def_special Ichor_AddThreadAnchor
	def_special Ichor_AddCrackedWall
	def_special Ichor_DrawThread
	def_special Ichor_StartAsterion
	def_special Ichor_AddDrift
	def_special Ichor_AsterionRest
	def_special Ichor_AsterionKnockdown
	def_special Ichor_BuildThreadMenu
	def_special Ichor_ThreadTieOff
	def_special Ichor_ThreadWindIn
	def_special Ichor_BuildThreadReturnMenu
	def_special Ichor_ThreadReturnTo
	def_special Ichor_TurnDial
	@ Ichor: scripts' small needs (src/ichor_save.c, ichor_time.c, ichor_omen.c)
	def_special Ichor_CountFlagRange
	def_special Ichor_HoldTimeOfDay
	def_special Ichor_ReleaseTimeOfDay
	def_special Ichor_ForceOmen
	def_special Ichor_CheckOmen
	def_special Ichor_GetOmen
	def_special Ichor_DigStart
	def_special Ichor_DigPuff
	def_special Ichor_DigFindKind
	def_special Ichor_DigFinish
	def_special Ichor_SellToMoneychanger
	def_special Ichor_GetMonth
	def_special Ichor_GetFestival
	def_special Ichor_DaysToFestival
	def_special Ichor_JoinFestival
	def_special Ichor_GetHighestPartyLevel
	def_special Ichor_BuildRestMenu
	def_special Ichor_RestUntil
	def_special Ichor_BonesStart
	def_special Ichor_BonesPlayerThrow
	def_special Ichor_BonesBuildMenu
	def_special Ichor_BonesToggle
	def_special Ichor_BonesRethrow
	def_special Ichor_BonesOpponentThrow
	def_special Ichor_BonesScore
	def_special Ichor_BonesCallLoaded
	def_special Ichor_BonesMatchOver
	def_special Ichor_GetMomRecord
	def_special Ichor_QuoteToMoneychanger
	def_special Ichor_SetOmenWeather
	def_special Ichor_BuildAmphoraMenu
	def_special Ichor_BufferAmphora
	def_special Ichor_RestoreAmphora
	def_special Ichor_BufferAmphoraNotes
	def_special Ichor_ShowAmphoraPicture
	def_special Ichor_HideAmphoraPicture
	def_special Ichor_SetPersephoneVisitor
	def_special Ichor_GetTimeOfDay
	def_special Ichor_BuildDeedsMenu
	def_special Ichor_BufferDeed
	def_special Ichor_PlaceConstellation
	def_special Ichor_CountConstellations
	def_special Ichor_ShowNightSky
	def_special Ichor_TakeFirstFruits
	@ Ichor: Act III engine (design/phase4/ENGINE_ACT3.md E7)
	def_special Ichor_BullLeap
	// Ichor: the beam trace (E9), ported from world-act3 for the Pythian Light
	def_special Ichor_TraceBeam
