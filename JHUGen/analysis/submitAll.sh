#!/bin/bash

# variable parameters
RUN="testRun"
NJOBS=1
NTOYS=100

# constant parameters
# see enums.h
zeroplusVSzerominus=0
zeroplusVStwoplus=1

# submit jobs
./submit.sh ${RUN}_zeroplusVSzerominus ${NJOBS} ${NTOYS} ${zeroplusVSzerominus}
./submit.sh ${RUN}_zeroplusVStwoplus   ${NJOBS} ${NTOYS} ${zeroplusVStwoplus}

