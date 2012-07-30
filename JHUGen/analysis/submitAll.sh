#!/bin/bash

# variable parameters
RUN="testRun"
NJOBS=10
NTOYS=1000

#
# hypothesis separation constant parameters
# see enums.h
zeroplusVSzerominus=0
zeroplusVStwoplus=1
ANA=hypsep

# submit jobs for hypothesis separation
./submit.sh ${RUN}_zeroplusVSzerominus ${NJOBS} ${NTOYS} ${zeroplusVSzerominus} ${ANA}
./submit.sh ${RUN}_zeroplusVStwoplus   ${NJOBS} ${NTOYS} ${zeroplusVStwoplus} ${ANA}

#
# significance constant parameters
# see enums.h
zeroplus=0 
ANA=sig

./submit.sh ${RUN}_zeroplus_sig ${NJOBS} ${NTOYS} ${zeroplus} ${ANA}

