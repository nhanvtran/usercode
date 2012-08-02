#!/bin/bash

# variable parameters
SITE=1 #UCSD=0, FNAL=1
RUN="testRun"
#NJOBS=100
#NTOYS=10000

NJOBS=10
NTOYS=1000


#
# hypothesis separation constant parameters
# see http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/UserCode/ntran/JHUGen/analysis/enums.h
zeroplusVSzerominus=0
zeroplusVStwoplus=1
zeroplusVSzerohplus=2
zeroplusVSoneplus=3
zeroplusVSoneminus=4
zeroplusVStwohplus=5
zeroplusVStwohminus=6
ANA=hypsep

# submit jobs for hypothesis separation
# ./submit.sh ${SITE} ${RUN}_zeroplusVSzerominus ${NJOBS} ${NTOYS} ${zeroplusVSzerominus} ${ANA}
# ./submit.sh ${SITE} ${RUN}_zeroplusVStwoplus   ${NJOBS} ${NTOYS} ${zeroplusVStwoplus} ${ANA}
./submit.sh ${SITE} ${RUN}_zeroplusVSzerohplus   ${NJOBS} ${NTOYS} ${zeroplusVSzerohplus} ${ANA}
./submit.sh ${SITE} ${RUN}_zeroplusVSoneplus   ${NJOBS} ${NTOYS} ${zeroplusVSoneplus} ${ANA}
./submit.sh ${SITE} ${RUN}_zeroplusVSoneminus   ${NJOBS} ${NTOYS} ${zeroplusVSoneminus} ${ANA}
./submit.sh ${SITE} ${RUN}_zeroplusVStwohplus   ${NJOBS} ${NTOYS} ${zeroplusVStwohplus} ${ANA}
./submit.sh ${SITE} ${RUN}_zeroplusVStwohminus   ${NJOBS} ${NTOYS} ${zeroplusVStwohminus} ${ANA}

#
# significance constant parameters
# see enums.h
zeroplus=0 
zerominus=1
zerohplus=2
oneplus=3
oneminus=4
twoplus=5
twohplus=6
twohminus=7

ANA=sig
#./submit.sh ${SITE} ${RUN}_zeroplus_sig ${NJOBS} ${NTOYS} ${zeroplus} ${ANA}
#./submit.sh ${SITE} ${RUN}_zerominus_sig ${NJOBS} ${NTOYS} ${zerominus} ${ANA}
#./submit.sh ${SITE} ${RUN}_twoplus_sig ${NJOBS} ${NTOYS} ${twoplus} ${ANA}
./submit.sh ${SITE} ${RUN}_zerohplus_sig ${NJOBS} ${NTOYS} ${zerohplus} ${ANA}
./submit.sh ${SITE} ${RUN}_oneplus_sig ${NJOBS} ${NTOYS} ${oneplus} ${ANA}
./submit.sh ${SITE} ${RUN}_oneminus_sig ${NJOBS} ${NTOYS} ${oneminus} ${ANA}
./submit.sh ${SITE} ${RUN}_twohplus_sig ${NJOBS} ${NTOYS} ${twohplus} ${ANA}
./submit.sh ${SITE} ${RUN}_twohminus_sig ${NJOBS} ${NTOYS} ${twohminus} ${ANA}

