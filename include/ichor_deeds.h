#ifndef GUARD_ICHOR_DEEDS_H
#define GUARD_ICHOR_DEEDS_H

enum
{
    ICHOR_DEED_HIDDEN,
    ICHOR_DEED_OPEN,
    ICHOR_DEED_DONE,
    ICHOR_DEED_RECORDED,
};

#define ICHOR_DEED_AMPHORA_START 16
#define ICHOR_DEED_HERMS 40
#define ICHOR_DEED_CALENDAR 41
#define ICHOR_DEEDS_MENU_ERROR 0xFFFF

u16 Ichor_DeedState(u32 deed);
void Ichor_BuildDeedsMenu(void);
u16 Ichor_BufferDeed(void);

#endif
