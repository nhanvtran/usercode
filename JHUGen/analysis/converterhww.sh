#!/bin/bash

f=$1
if [ ! $# -eq 1 ]; then
    echo "USAGE: ./converthww.sh file.lhe
      file - the lhe file "
    exit 1
fi

fr="${f%.*}"
ff="${f%.*}.txt"
echo $f, $ff

awk '/<event>/,/LesHouchesEvents>/' $f | grep -iv "<event>" | grep -iv "</event>" | grep -iv "</LesHouchesEvents>" | grep -iv "9 100" | grep -iv "1 -1  0"  | grep -iv "2 -1  0" | grep -iv "3 -1  0" | grep -iv "4 -1  0" | grep -iv "5 -1  0"  | grep -iv "21 -1  0" | grep -iv "24  2  3" | grep -iv "39  2  1" | grep -iv "# " | grep -iv "<!-- " > $ff

frt='"'$fr'"'
echo $frt
root -l -q -b "readOutAnglesHWW_LMH.C(${frt})"
rm $ff

echo "done"


