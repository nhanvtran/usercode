#!/bin/bash
# run 20 jobs simultaneously

for SEED in 9472010 2316565 4849736 9997417 7443053 5400436 7399529 7599437 6586366 3156376 9574769 8044030 3156379 5196721 1685724 4755297 3923139 2216676 2131904 3033528; do
    #echo $SEED
    #echo "nohup root -l  -q runSigSepWW.C\(${SEED}\) >& temp_${SEED}.log & "
    nice nohup root -l  -q runSigSepWW.C\(${SEED}\) >& temp_${SEED}.log &
done

# echo $RANDOM
