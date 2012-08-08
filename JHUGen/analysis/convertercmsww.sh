#!/bin/bash

f=$1
if [ ! $# -eq 1 ]; then
    echo "USAGE: ./convertcmsww.sh file.lhe
      file - the lhe file "
    exit 1
fi

fr="${f%.*}"
ff="${f%.*}.txt"
echo $f, $ff

# these lines grab only the 2l and 2nu lines from the .lhe files
# grep -iv suppress the unwanted lines

awk '/<event>/,/LesHouchesEvents>/' $f | grep -iv "<event>" | grep -iv "</event>" | grep -iv "</LesHouchesEvents>" | grep -iv "9 100"  | grep -iv "21 1 1" | grep -iv "21    1    1" | grep -iv "24    2    1" | grep -iv "8 1" | grep -iv "9 2" | grep -iv "9 1" | grep -iv "10 3" | grep -iv "10 2" | grep -iv "11 3" |  grep -iv "1   -1    0"  | grep -iv "1    1    1" |  grep -iv "2   -1    0" | grep -iv "2    1    1" | grep -iv "3    1    0"  | grep -iv "3   -1    0"  | grep -iv "3    1    1" | grep -iv "3   1    1" | grep -iv "4   -1    0" | grep -iv "4    1    1" | grep -iv "1    1    1" | grep -iv "5    1    1" | grep -iv "5   -1    0" | grep -iv "21   -1    0" | grep -iv "# " |  grep -iv "24    2    1" | grep -iv "24    2    3" | grep -iv "23    2    1 " | grep -iv "<!-- " > $ff

frt='"'$fr'"'
echo $frt
root -l -q -b "readOutAnglesWW.C(${frt})"
#rm $ff

echo "done"
