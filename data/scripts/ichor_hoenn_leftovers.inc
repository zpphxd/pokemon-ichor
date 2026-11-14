@ Ichor: labels the deleted Hoenn maps used to define (hoenn-cut batch 2) that
@ upstream C code and shared scripts still name. Texts are copied over unchanged,
@ because data/scripts/players_house.inc (Elaia's player house) still prints some.
@ Scripts are reduced to 'end': only Hoenn-only code paths (Match Call, the Trick
@ House, the Sootopolis and Sky Pillar doors, ferries) ever ran them.

@ from data/maps/LittlerootTown_BrendansHouse_2F/scripts.inc
Common_Text_LookCloserAtMap::
	.string "{PLAYER} took a closer look at the\n"
	.string "{REGION} region map.$"

@ from data/maps/SootopolisCity/scripts.inc
EventScript_ClosedSootopolisDoor::
	end

@ from data/maps/FarawayIsland_Interior/scripts.inc
FarawayIsland_Interior_EventScript_HideMewWhenGrassCut::
	end

@ from data/maps/SouthernIsland_Exterior/scripts.inc
Ferry_EventScript_DepartIslandSouth::
	end

@ from data/maps/SouthernIsland_Exterior/scripts.inc
Ferry_EventScript_DepartIslandWest::
	end

@ from data/maps/IslandCave/scripts.inc
IslandCave_EventScript_OpenRegiEntrance::
	end

@ from data/maps/LittlerootTown_BrendansHouse_2F/scripts.inc
LittlerootTown_BrendansHouse_2F_EventScript_PC::
	end

@ from data/maps/LittlerootTown_BrendansHouse_2F/scripts.inc
LittlerootTown_BrendansHouse_2F_EventScript_TurnOffPlayerPC::
	end

@ from data/maps/LittlerootTown_MaysHouse_2F/scripts.inc
LittlerootTown_MaysHouse_2F_EventScript_PC::
	end

@ from data/maps/LittlerootTown_MaysHouse_2F/scripts.inc
LittlerootTown_MaysHouse_2F_EventScript_TurnOffPlayerPC::
	end

@ from data/maps/LittlerootTown_ProfessorBirchsLab/scripts.inc
LittlerootTown_ProfessorBirchsLab_EventScript_ScottAboardSSTidalCall::
	end

@ from data/maps/MauvilleCity/scripts.inc
MauvilleCity_EventScript_RegisterWallyCall::
	end

@ from data/maps/MossdeepCity_SpaceCenter_2F/scripts.inc
MossdeepCity_SpaceCenter_2F_EventScript_ChoosePartyForMultiBattle::
	end

@ from data/maps/MossdeepCity_SpaceCenter_2F/scripts.inc
MossdeepCity_SpaceCenter_2F_EventScript_RivalRayquazaCall::
	end

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_ArentYouInterestedInRoom::
	.string "MOM: Well, {PLAYER}?\p"
	.string "Aren't you interested in seeing your\n"
	.string "very own room?$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_BetterGetBackToGym::
	.string "I'd better get back to PETALBURG GYM.\p"
	.string "MOM, thanks for looking after the house\n"
	.string "while I'm away.$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_DadShouldStayLonger::
	.string "MOM: That DAD of yours…\p"
	.string "He comes home for the first time in a\n"
	.string "while, but all he talks about is POKéMON.\p"
	.string "He should relax and stay a little longer.$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_DidYouMeetProfBirch::
	.string "MOM: Did you introduce yourself to\n"
	.string "PROF. BIRCH?$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_DontPushYourselfTooHard::
	.string "Don't push yourself too hard, dear.\n"
	.string "You can always come home.\p"
	.string "Go for it, honey!$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_GoIntroduceYourselfNextDoor::
	.string "Oh, yes.\n"
	.string "One of DAD's friends lives in town.\p"
	.string "PROF. BIRCH is his name.\p"
	.string "He lives right next door, so you should\n"
	.string "go over and introduce yourself.$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_GotDadsBadgeHeresSomethingFromMom::
	.string "MOM: Oh? Did DAD give you that BADGE?\p"
	.string "Then here's something from your MOM!$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_IsThatABreakingStory::
	.string "MOM: Is that a breaking news story?$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_IsThatAPokenav::
	.string "MOM: What is that, honey? A POKéNAV?\n"
	.string "Someone from DEVON gave it to you?\p"
	.string "Well, honey, how about registering\n"
	.string "your mom?\p"
	.string "… … …$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_IsntItNiceInHere::
	.string "MOM: See, {PLAYER}?\n"
	.string "Isn't it nice in here, too?$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_ItsOverWeMissedHim::
	.string "MOM: Oh… It's over.\p"
	.string "I think DAD was on, but we missed him.\n"
	.string "Too bad.$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_LatiEmergencyNewsFlash::
	.string "We bring you this emergency\n"
	.string "news flash!\p"
	.string "In various HOENN locales, there have\n"
	.string "been reports of a BZZT…colored\l"
	.string "POKéMON in flight.\p"
	.string "The identity of this POKéMON is\n"
	.string "currently unknown.\p"
	.string "We now return you to the regular\n"
	.string "movie program.$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_MaybeDadWillBeOn::
	.string "MOM: Look! It's PETALBURG GYM!\n"
	.string "Maybe DAD will be on!$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_MoversPokemonGoSetClock::
	.string "The mover's POKéMON do all the work\n"
	.string "of moving us in and cleaning up after.\l"
	.string "This is so convenient!\p"
	.string "{PLAYER}, your room is upstairs.\n"
	.string "Go check it out, dear!\p"
	.string "DAD bought you a new clock to mark\n"
	.string "our move here.\l"
	.string "Don't forget to set it!$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_OhComeQuickly::
	.string "MOM: Oh! {PLAYER}, {PLAYER}!\n"
	.string "Quick! Come quickly!$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_PortsInSlateportLilycove::
	.string "DAD: Hm, a TICKET for a ferry?\p"
	.string "If I recall, there are ferry ports in\n"
	.string "SLATEPORT and LILYCOVE.$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_RegisteredMom::
	.string "Registered MOM\n"
	.string "in the POKéNAV.$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_ReportFromPetalburgGym::
	.string "INTERVIEWER: …We brought you this\n"
	.string "report from in front of PETALBURG GYM.$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_RunningShoesManual::
	.string "It's the instruction booklet for the\n"
	.string "RUNNING SHOES.\p"
	.string "“Press the B Button to run while\n"
	.string "wearing your RUNNING SHOES.\p"
	.string "“Lace up your RUNNING SHOES and hit\n"
	.string "the road running!”$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_SeeYouHoney::
	.string "MOM: See you, honey!$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_StillUnknownPokemon::
	.string "MOM: Well, isn't that something!\n"
	.string "There are still unknown POKéMON.$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_TakeCareHoney::
	.string "MOM: Take care, honey!$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_TheresAMovieOnTV::
	.string "There is a movie on TV.\p"
	.string "Two men are dancing on a big piano\n"
	.string "keyboard.\p"
	.string "Better get going!$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_TicketFromBrineyCameForYou::
	.string "DAD: Hm?\p"
	.string "Hey, it's {PLAYER}!\p"
	.string "It's been a while since I saw you,\n"
	.string "but you look…stronger, somehow.\p"
	.string "That's the impression I get.\n"
	.string "But your old man hasn't given up yet!\p"
	.string "Oh, yes, I have something for you.\n"
	.string "This came to you from someone named\l"
	.string "MR. BRINEY.$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_Vigoroth1::
	.string "Fugiiiiih!$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_Vigoroth2::
	.string "Huggoh, uggo uggo…$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_WhatColorDidTheySay::
	.string "MOM: {PLAYER}, did you catch that?\p"
	.string "What color did the announcer say\n"
	.string "that POKéMON was?$"

@ from data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
PlayersHouse_1F_Text_YouShouldRestABit::
	.string "MOM: How are you doing, {PLAYER}?\n"
	.string "You look a little tired.\p"
	.string "I think you should rest a bit.$"

@ from data/maps/LittlerootTown_BrendansHouse_2F/scripts.inc
PlayersHouse_2F_Text_ClockIsStopped::
	.string "The clock is stopped…\p"
	.string "Better set it and start it!$"

@ from data/maps/LittlerootTown_BrendansHouse_2F/scripts.inc
PlayersHouse_2F_Text_HowDoYouLikeYourRoom::
	.string "MOM: {PLAYER}, how do you like your\n"
	.string "new room?\p"
	.string "Good! Everything's put away neatly!\p"
	.string "They finished moving everything in\n"
	.string "downstairs, too.\p"
	.string "POKéMON movers are so convenient!\p"
	.string "Oh, you should make sure that\n"
	.string "everything's all there on your desk.$"

@ from data/maps/Route110_TrickHouseEntrance/scripts.inc
Route110_TrickHousePuzzle_EventScript_Door::
	end

@ from data/maps/Route119/scripts.inc
Route119_EventScript_ScottWonAtFortreeGymCall::
	end

@ from data/maps/RustboroCity_Gym/scripts.inc
RustboroCity_Gym_EventScript_RegisterRoxanne::
	end

@ from data/maps/SSTidalCorridor/scripts.inc
SSTidalCorridor_EventScript_ReachedStepCount::
	end

@ from data/maps/SkyPillar_Outside/scripts.inc
SkyPillar_Outside_EventScript_ClosedDoor::
	end
