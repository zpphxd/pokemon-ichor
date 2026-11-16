#include "global.h"
#include "event_data.h"
#include "ichor_calendar.h"
#include "ichor_deeds.h"
#include "ichor_dig.h"
#include "ichor_herms.h"
#include "list_menu.h"
#include "malloc.h"
#include "script_menu.h"
#include "string_util.h"
#include "constants/ichor.h"
#include "constants/vars.h"

struct Deed
{
    const u8 *name;
    const u8 *objective;
    const u8 *hint;
    u16 prerequisite;
    u16 receipt;
};

static const struct Deed sStoryDeeds[] =
{
    {COMPOUND_STRING("First partner"), COMPOUND_STRING("Meet Daphne and choose a partner."),
     COMPOUND_STRING("Visit the Akademia in Elaia."), 0, FLAG_ICHOR_GOT_STARTER},
    {COMPOUND_STRING("Hearth Laurel"), COMPOUND_STRING("Earn Hestia's Laurel on Kalliste."),
     COMPOUND_STRING("Follow the road to Akti.\lClimb to Hestia's temple."), FLAG_ICHOR_GOT_STARTER, FLAG_BADGE01_GET},
    {COMPOUND_STRING("Across the sea"), COMPOUND_STRING("Sail from Akti to Emporion."),
     COMPOUND_STRING("Alethea's ship waits at Akti."), FLAG_BADGE01_GET, FLAG_ICHOR_ARRIVED_EMPORION},
    {COMPOUND_STRING("Herald Laurel"), COMPOUND_STRING("Earn Hermes's Laurel in Emporion."),
     COMPOUND_STRING("Carry the runners' three scrolls.\lThen visit the Temple of Hermes."), FLAG_ICHOR_ARRIVED_EMPORION, FLAG_BADGE02_GET},
    {COMPOUND_STRING("Harvest Laurel"), COMPOUND_STRING("Follow the procession to Eleusa."),
     COMPOUND_STRING("Take the north road from Emporion.\lChloe waits in the Telesterion."), FLAG_BADGE02_GET, FLAG_BADGE03_GET},
    {COMPOUND_STRING("Night of the Mysteries"), COMPOUND_STRING("Join the night rites in Eleusa."),
     COMPOUND_STRING("Speak to Kerykos outside the hall."), FLAG_BADGE03_GET, FLAG_ICHOR_MYSTERIES_NIGHT},
    {COMPOUND_STRING("The stolen fragment"), COMPOUND_STRING("Follow the Titans below Eleusa."),
     COMPOUND_STRING("Descend beneath the Telesterion.\lThe trail leads to the lowest hall."), FLAG_ICHOR_MYSTERIES_NIGHT, FLAG_ICHOR_FRAGMENT_STOLEN},
    {COMPOUND_STRING("Kleon's departure"), COMPOUND_STRING("Speak to Kleon after the theft."),
     COMPOUND_STRING("He waits inside the Telesterion."), FLAG_ICHOR_FRAGMENT_STOLEN, FLAG_ICHOR_KLEON_LEFT_FOR_THYRSA},
    {COMPOUND_STRING("The Unwoven"), COMPOUND_STRING("Hear Daphne's account of the tablet."),
     COMPOUND_STRING("Return to the hall with Bag space."), FLAG_ICHOR_KLEON_LEFT_FOR_THYRSA, FLAG_ICHOR_ACT1_COMPLETE},
    {COMPOUND_STRING("Letter home"), COMPOUND_STRING("Send word to Mom in Elaia."),
     COMPOUND_STRING("Ask the runners in Emporion."), FLAG_ICHOR_ACT1_COMPLETE, FLAG_ICHOR_WROTE_TO_MOM},
    {COMPOUND_STRING("Mom's parcel"), COMPOUND_STRING("Collect Mom's gift when you return."),
     COMPOUND_STRING("Visit Mom with room in your Bag."), FLAG_ICHOR_WROTE_TO_MOM, FLAG_ICHOR_GOT_MOMS_HONEY},
    {COMPOUND_STRING("Daedalus's pages"), NULL, NULL, FLAG_ICHOR_GOT_TROWEL, 0},
};

static const u8 *const sAmphoraLeads[ICHOR_AMPHORA_COUNT] =
{
    COMPOUND_STRING("Kronion Hill's broken altar hums\nat night. Listen there."),
    COMPOUND_STRING("Something waits in Eleusa's meadow\nat dusk."),
    COMPOUND_STRING("A web-spinner waits in the web\nchamber of Hecate's Hollow."),
    COMPOUND_STRING("Backward hoofprints on a beach\npoint toward a hidden grotto."),
    COMPOUND_STRING("Hephaestus remembers your work.\nWatch for a rare forge-side visitor."),
    COMPOUND_STRING("Look for a sea-bird's dawn roost\nalong the Ikarian coasts."),
    COMPOUND_STRING("One thing stayed in Pandora's jar:\nHope. Remember that."),
    COMPOUND_STRING("Orpheus's song belongs to Arkadia's\ngrove at night."),
    COMPOUND_STRING("Atalanta's race points toward a\nfast visitor's hidden path."),
    COMPOUND_STRING("Watch Kaldera's rim for a rare\nFire-type."),
    COMPOUND_STRING("Aphrodite remembers the apple.\nLook for a golden-apple tree."),
    COMPOUND_STRING("Show this painting to Ariadne.\nShe remembers a different story."),
};

static const u8 *const sMonths[ICHOR_MONTH_COUNT] =
{
    COMPOUND_STRING("Hekatombaion"), COMPOUND_STRING("Metageitnion"),
    COMPOUND_STRING("Boedromion"), COMPOUND_STRING("Pyanepsion"),
    COMPOUND_STRING("Maimakterion"), COMPOUND_STRING("Poseideon"),
    COMPOUND_STRING("Gamelion"), COMPOUND_STRING("Anthesterion"),
    COMPOUND_STRING("Elaphebolion"), COMPOUND_STRING("Mounichion"),
    COMPOUND_STRING("Thargelion"), COMPOUND_STRING("Skirophorion"),
};

static const u8 *const sFestivals[ICHOR_MONTH_COUNT] =
{
    COMPOUND_STRING("Panathenaia"), COMPOUND_STRING("Karneia"),
    COMPOUND_STRING("The Mysteries"), COMPOUND_STRING("Pyanopsia"),
    COMPOUND_STRING(""), COMPOUND_STRING("Poseidea"),
    COMPOUND_STRING("Theogamia"), COMPOUND_STRING("Anthesteria"),
    COMPOUND_STRING("City Dionysia"), COMPOUND_STRING("Mounichia"),
    COMPOUND_STRING("Thargelia"), COMPOUND_STRING("Kronia"),
};

static u16 AmphoraReceipt(u32 amphora)
{
    switch (amphora)
    {
    case ICHOR_AMPHORA_KRONOS: return FLAG_ICHOR_KRONION_ALTAR_STONE;
    case ICHOR_AMPHORA_PERSEPHONE: return FLAG_ICHOR_ELEUSA_PERSENYX;
    case ICHOR_AMPHORA_ARACHNE: return FLAG_ICHOR_HOLLOW_RAKNIT;
    default: return 0;
    }
}

u16 Ichor_DeedState(u32 deed)
{
    if (deed < ARRAY_COUNT(sStoryDeeds))
    {
        const struct Deed *entry = &sStoryDeeds[deed];
        if (entry->receipt != 0 && FlagGet(entry->receipt))
            return ICHOR_DEED_DONE;
        if (entry->prerequisite != 0 && !FlagGet(entry->prerequisite))
            return ICHOR_DEED_HIDDEN;
        if (entry->receipt == 0 && Ichor_CountFlags(FLAG_ICHOR_PAGES_START, 7) == 7)
            return ICHOR_DEED_DONE;
        return ICHOR_DEED_OPEN;
    }
    if (deed >= ICHOR_DEED_AMPHORA_START && deed < ICHOR_DEED_AMPHORA_START + ICHOR_AMPHORA_COUNT)
    {
        u32 amphora = deed - ICHOR_DEED_AMPHORA_START;
        u16 receipt = AmphoraReceipt(amphora);
        if (Ichor_AmphoraStatus(amphora) == ICHOR_AMPHORA_RESTORED)
            return receipt == 0 ? ICHOR_DEED_RECORDED : FlagGet(receipt) ? ICHOR_DEED_DONE : ICHOR_DEED_OPEN;
        if (Ichor_CountFlags(FLAG_ICHOR_SHERDS_START + amphora * ICHOR_SHERDS_PER_AMPHORA, ICHOR_SHERDS_PER_AMPHORA) != 0)
            return ICHOR_DEED_OPEN;
        return ICHOR_DEED_HIDDEN;
    }
    if (deed == ICHOR_DEED_HERMS || deed == ICHOR_DEED_CALENDAR)
        return ICHOR_DEED_RECORDED;
    return ICHOR_DEED_HIDDEN;
}

static void AppendCount(u32 count, u32 total)
{
    u8 *end = gStringVar4 + StringLength(gStringVar4);
    end = ConvertIntToDecimalStringN(end, count, STR_CONV_MODE_LEFT_ALIGN, 2);
    end = StringCopy(end, COMPOUND_STRING(" of "));
    ConvertIntToDecimalStringN(end, total, STR_CONV_MODE_LEFT_ALIGN, 2);
}

u16 Ichor_BufferDeed(void)
{
    u32 deed = gSpecialVar_0x8004;
    u16 state = Ichor_DeedState(deed);

    if (state == ICHOR_DEED_HIDDEN)
    {
        StringCopy(gStringVar4, COMPOUND_STRING("This page is not in your scroll."));
        return FALSE;
    }
    if (deed < ARRAY_COUNT(sStoryDeeds))
    {
        StringCopy(gStringVar4, sStoryDeeds[deed].name);
        StringAppend(gStringVar4, state == ICHOR_DEED_DONE ? COMPOUND_STRING("\nDone.") : COMPOUND_STRING("\nOpen."));
        if (sStoryDeeds[deed].receipt == 0)
        {
            StringAppend(gStringVar4, COMPOUND_STRING("\pPages found: "));
            AppendCount(Ichor_CountFlags(FLAG_ICHOR_PAGES_START, 7), 7);
            StringAppend(gStringVar4, COMPOUND_STRING("."));
        }
        else if (state == ICHOR_DEED_OPEN)
        {
            StringAppend(gStringVar4, COMPOUND_STRING("\p"));
            StringAppend(gStringVar4, sStoryDeeds[deed].objective);
        }
        if (state == ICHOR_DEED_OPEN && FlagGet(FLAG_ICHOR_ATHENAS_STYLUS))
        {
            StringAppend(gStringVar4, COMPOUND_STRING("\pAthena's hint:\n"));
            if (sStoryDeeds[deed].receipt != 0)
                StringAppend(gStringVar4, sStoryDeeds[deed].hint);
            else if (!FlagGet(FLAG_ICHOR_PAGES_START))
                StringAppend(gStringVar4, COMPOUND_STRING("Trade oil with Glykera in Emporion."));
            else if (!FlagGet(FLAG_ICHOR_PAGES_START + 1))
                StringAppend(gStringVar4, COMPOUND_STRING("Search the sanctum's lowest hall."));
            else
                StringAppend(gStringVar4, COMPOUND_STRING("More pages lie beyond Eleusa."));
        }
    }
    else if (deed >= ICHOR_DEED_AMPHORA_START && deed < ICHOR_DEED_AMPHORA_START + ICHOR_AMPHORA_COUNT)
    {
        u32 amphora = deed - ICHOR_DEED_AMPHORA_START;
        u16 status;
        gSpecialVar_0x8004 = amphora;
        status = Ichor_BufferAmphora();
        StringCopy(gStringVar4, gStringVar1);
        if (status == ICHOR_AMPHORA_RESTORED)
        {
            StringAppend(gStringVar4, state == ICHOR_DEED_DONE ? COMPOUND_STRING("\nLead done.") : COMPOUND_STRING("\nRestored."));
            StringAppend(gStringVar4, COMPOUND_STRING("\p"));
            StringAppend(gStringVar4, sAmphoraLeads[amphora]);
        }
        else
        {
            StringAppend(gStringVar4, COMPOUND_STRING("\pSherds collected: "));
            AppendCount(Ichor_CountFlags(FLAG_ICHOR_SHERDS_START + amphora * ICHOR_SHERDS_PER_AMPHORA, ICHOR_SHERDS_PER_AMPHORA), ICHOR_SHERDS_PER_AMPHORA);
            StringAppend(gStringVar4, status == ICHOR_AMPHORA_READY ? COMPOUND_STRING(".\nReady for Daphne's shelf.") : COMPOUND_STRING(".\nThe painting still has gaps."));
        }
        if (state == ICHOR_DEED_OPEN && FlagGet(FLAG_ICHOR_ATHENAS_STYLUS))
        {
            StringAppend(gStringVar4, COMPOUND_STRING("\pAthena's hint:\n"));
            if (status != ICHOR_AMPHORA_RESTORED)
                StringAppend(gStringVar4, COMPOUND_STRING("Dig in its region; use Elaia's shelf."));
            else if (amphora == ICHOR_AMPHORA_KRONOS)
                StringAppend(gStringVar4, COMPOUND_STRING("Approach the altar from the west."));
            else if (amphora == ICHOR_AMPHORA_PERSEPHONE)
                StringAppend(gStringVar4, COMPOUND_STRING("Search the meadow beside the field."));
            else
                StringAppend(gStringVar4, COMPOUND_STRING("Burn the chamber's web with the Torch."));
        }
        gSpecialVar_0x8004 = deed;
    }
    else if (deed == ICHOR_DEED_HERMS)
    {
        StringCopy(gStringVar4, COMPOUND_STRING("Herms anointed: "));
        AppendCount(Ichor_CountAnointedHerms(), HERM_COUNT);
        StringAppend(gStringVar4, COMPOUND_STRING(".\pAnoint great herms with Olive Oil.\nTheir roads remember you."));
    }
    else
    {
        u32 day = VarGet(VAR_DAYS);
        u32 month = Ichor_GetMonthOfDay(day);
        u32 until;
        StringCopy(gStringVar4, sMonths[month]);
        StringAppend(gStringVar4, COMPOUND_STRING(".\nDay "));
        AppendCount(day % ICHOR_DAYS_PER_MONTH + 1, ICHOR_DAYS_PER_MONTH);
        if (month == ICHOR_MONTH_MAIMAKTERION)
            StringAppend(gStringVar4, COMPOUND_STRING(".\pThe month of storms.\nNo festival this month."));
        else
        {
            gSpecialVar_0x8004 = month + 1;
            until = Ichor_DaysToFestival();
            StringAppend(gStringVar4, COMPOUND_STRING(".\p"));
            StringAppend(gStringVar4, sFestivals[month]);
            if (until == 0)
                StringAppend(gStringVar4, month == ICHOR_MONTH_BOEDROMION ? COMPOUND_STRING(" are today.") : COMPOUND_STRING(" is today."));
            else
            {
                StringAppend(gStringVar4, COMPOUND_STRING("\nin "));
                ConvertIntToDecimalStringN(gStringVar4 + StringLength(gStringVar4), until, STR_CONV_MODE_LEFT_ALIGN, 2);
                StringAppend(gStringVar4, until == 1 ? COMPOUND_STRING(" day.") : COMPOUND_STRING(" days."));
            }
            gSpecialVar_0x8004 = deed;
        }
    }
    return TRUE;
}

void Ichor_BuildDeedsMenu(void)
{
    u32 category = gSpecialVar_0x8004;
    u32 selected = gSpecialVar_0x800A;
    u32 i, count = 0;
    u32 entries = category == 0 ? 4 : category == 1 ? ARRAY_COUNT(sStoryDeeds) : ICHOR_AMPHORA_COUNT;

    if (category > 2)
    {
        gSpecialVar_Result = ICHOR_DEEDS_MENU_ERROR;
        return;
    }
    if (category == 0)
    {
        if (selected < ARRAY_COUNT(sStoryDeeds))
            selected = 100;
        else if (selected >= ICHOR_DEED_AMPHORA_START && selected < ICHOR_DEED_AMPHORA_START + ICHOR_AMPHORA_COUNT)
            selected = 101;
    }
    gSpecialVar_0x8000 = 0xFFFF;
    for (i = 0; i < entries; i++)
    {
        struct ListMenuItem item;
        u32 deed = category == 1 ? i : ICHOR_DEED_AMPHORA_START + i;
        u16 state = Ichor_DeedState(deed);
        u8 *label;
        if (category != 0 && state == ICHOR_DEED_HIDDEN)
            continue;
        label = Alloc(48);
        if (label == NULL)
        {
            struct ListMenuItem *queued;
            while ((queued = MultichoiceDynamic_PopElement()) != NULL)
                Free((void *)queued->name);
            if (count != 0)
                MultichoiceDynamic_DestroyStack();
            gSpecialVar_Result = ICHOR_DEEDS_MENU_ERROR;
            return;
        }
        item.name = label;
        item.id = deed;
        if (category == 0)
        {
            static const u8 *const names[] = {COMPOUND_STRING("Act I"), COMPOUND_STRING("Amphorae"), COMPOUND_STRING("Herms"), COMPOUND_STRING("Calendar")};
            static const u16 ids[] = {100, 101, ICHOR_DEED_HERMS, ICHOR_DEED_CALENDAR};
            StringCopy(label, names[i]);
            item.id = ids[i];
        }
        else
        {
            if (category == 1)
                StringCopy(label, sStoryDeeds[i].name);
            else
            {
                gSpecialVar_0x8004 = i;
                Ichor_BufferAmphora();
                StringCopy(label, gStringVar1);
            }
            StringAppend(label, state == ICHOR_DEED_DONE ? COMPOUND_STRING(" done") : state == ICHOR_DEED_RECORDED ? COMPOUND_STRING(" noted") : COMPOUND_STRING(" open"));
        }
        if (item.id == selected)
            gSpecialVar_0x8000 = item.id;
        MultichoiceDynamic_PushElement(item);
        count++;
    }
    gSpecialVar_0x8004 = category;
    gSpecialVar_Result = count;
}
