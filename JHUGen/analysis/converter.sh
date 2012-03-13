#!/bin/bash

f=$1
fr="${f%.*}"
ff="${f%.*}.txt"
echo $f, $ff

awk '/<event>/,/LesHouchesEvents>/' $f | grep -iv "<event>" | grep -iv "</event>" | grep -iv "</LesHouchesEvents>" | grep -iv "9 100" | grep -iv "1 -1  0"  | grep -iv "2 -1  0" | grep -iv "3 -1  0" | grep -iv "4 -1  0" | grep -iv "5 -1  0"  | grep -iv "21 -1  0" | grep -iv "23  2  3" | grep -iv "39  2  1" | grep -iv "# " | grep -iv "<!-- " > $ff

frt='"'$fr'"'
echo $frt
root -l -q -b "readOutAngles_LMH.C(${frt})"
rm $ff

echo "done"


