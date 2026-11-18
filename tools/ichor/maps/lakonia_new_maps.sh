#!/bin/sh
# One-time: create Lakonia's chapter maps (design/phase4/SCRIPT.md Part 2) and
# register them. Layouts are placeholders until the builders write them:
# tools/ichor/maps/lakonia_maps.py (outdoors) and lakonia_rooms.py (rooms).
set -e
cd "$(dirname "$0")/../../.."
N="python3 tools/ichor/new_map.py"
G=gMapGroup_Lakonia
ROOM=LAYOUT_KYTHERA_SKANDEIA_AXYLOS_HOUSE
OUT=LAYOUT_KYTHERA_SKANDEIA

$N Gytheion --group $G --layout-from $OUT --primary gTileset_Aethos --secondary gTileset_Gytheion \
   --mapsec MAPSEC_GYTHEION --music MUS_ICHOR_AKTI --type MAP_TYPE_TOWN --show-name
$N Route25_Eurotas --group $G --layout-from $OUT --primary gTileset_Aethos --secondary gTileset_Eurotas \
   --mapsec MAPSEC_AETHOS_ROUTE_25 --music MUS_ICHOR_ROAD --type MAP_TYPE_ROUTE --show-name
$N Lakonia --group $G --layout-from $OUT --primary gTileset_Aethos --secondary gTileset_Lakonia \
   --mapsec MAPSEC_LAKONIA --music MUS_ICHOR_ELEUSA --type MAP_TYPE_TOWN --show-name

for r in Asclepeion:MUS_ICHOR_ASCLEPEION Dyeworks:MUS_ICHOR_AKTI LysandrosHouse:MUS_ICHOR_AKTI \
         TimaiaHouse:MUS_ICHOR_AKTI KranaiShrine:MUS_ICHOR_AKTI; do
  $N Gytheion_${r%%:*} --group $G --layout-from $ROOM --mapsec MAPSEC_GYTHEION --music ${r#*:}
done
for r in Asclepeion:MUS_ICHOR_ASCLEPEION Agora:MUS_ICHOR_AGORA LampitosHouse:MUS_ICHOR_ELEUSA \
         GylipposHouse:MUS_ICHOR_ELEUSA Syssition:MUS_ICHOR_ELEUSA Agoge:MUS_ICHOR_ELEUSA \
         Palaestra:MUS_ICHOR_ELEUSA Orthia:MUS_ICHOR_TEMPLE ChilonHouse:MUS_ICHOR_ELEUSA \
         LichasHouse:MUS_ICHOR_ELEUSA; do
  $N Lakonia_${r%%:*} --group $G --layout-from $ROOM --mapsec MAPSEC_LAKONIA --music ${r#*:}
done
