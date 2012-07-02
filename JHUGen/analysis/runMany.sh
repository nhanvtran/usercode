#!/bin/bash

# run the code...

for SEED in 9472010 2316565 4849736 9574769 7443053 5400436 7399529 7599437 6586366 3156376; do
    nice nohup root -l  -q runSigSepWW.C\(${SEED}\) >& temp_${SEED}.log &
done

