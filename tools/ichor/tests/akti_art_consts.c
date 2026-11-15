#include "engine_consts.h"
#include "sprite.h"
#include "data.h"
#include "constants/species.h"
#include "constants/trainers.h"

K(NEMECUB, SPECIES_NEMECUB)
K(NEMELEON, SPECIES_NEMELEON)
K(SHEPHERD, TRAINER_PIC_SHEPHERD)
K(HARVESTER, TRAINER_PIC_HARVESTER)
K(GOATHERD, TRAINER_PIC_GOATHERD)
K(HOPLITE, TRAINER_PIC_HOPLITE)
K(AUGUR, TRAINER_PIC_AUGUR)
K(ACOLYTE_M, TRAINER_PIC_ACOLYTE_M)
K(ACOLYTE_F, TRAINER_PIC_ACOLYTE_F)
K(SPRITE_SIZE, sizeof(struct Sprite))
K(OFF_SPRITE_IMAGES, offsetof(struct Sprite, images))
K(OFF_SPRITE_ANIM_NUM, offsetof(struct Sprite, animNum))
K(FRAME_IMAGE_SIZE, sizeof(struct SpriteFrameImage))
K(PIC_BYTES, MON_PIC_SIZE)
K(SPRITE_LIMIT, MAX_SPRITES)
K(TRAINER_INFO_SIZE, sizeof(struct TrainerPicInfo))
K(OFF_TRAINER_FRONT, offsetof(struct TrainerPicInfo, frontPic))
K(OFF_TRAINER_PALETTE, offsetof(struct TrainerFrontPicInfo, paletteData))
