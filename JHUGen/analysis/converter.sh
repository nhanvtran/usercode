#!/bin/bash

f=$1

if [ $# == 1 ] 
    then 
    applySmear="false"
    elif [ $# == 2 ] 
    then
    applySmear=$2
    fi

fr="${f%.*}"
ff="${f%.*}_${applySmear}.txt"
echo $f, $ff

awk '/<event>/,/LesHouchesEvents>/' $f | grep -iv "<event>" | grep -iv "</event>" | grep -iv "</LesHouchesEvents>" | grep -iv "9 100" | grep -iv "1 -1  0"  | grep -iv "2 -1  0" | grep -iv "3 -1  0" | grep -iv "4 -1  0" | grep -iv "5 -1  0"  | grep -iv "21 -1  0" | grep -iv "23  2  3" | grep -iv "39  2  1" | grep -iv "# " | grep -iv "<!-- " > $ff

frt='"'"${ff%.txt}"'"'
echo $frt

sed -e 's|<NAME>|'$frt'|' <loadReadOutAngles.tpl >loadReadOutAngles.C

root -l -n -q loadReadOutAngles.C

echo "done"


