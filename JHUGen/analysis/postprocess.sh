#!/bin/bash

if [ ! $# -eq 1 ]; then
    echo "USAGE: ./postprocess.sh DIR
    DIR - output directory"
    exit 1
fi

DIR=$1

PREFIX=`ls ${DIR}/*10fb_*.root | sed 's/\(.*\)_10fb_.*/\1_10fb/' | uniq` 
echo $PREFIX
hadd $PREFIX.root ${PREFIX}_*.root
rm -f  ${PREFIX}_*.root