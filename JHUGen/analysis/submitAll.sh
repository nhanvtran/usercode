#!/bin/bash

# variable parameters
SITE=1 #UCSD=0, FNAL=1
NJOBS=1
NTOYS=1000
LUMI=20
RUN="testRun_${LUMI}fb"

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
# very large toys
#./submit.sh ${SITE} ${RUN}_zeroplusVStwoplus  1000 ${NTOYS} ${zeroplusVStwoplus} ${LUMI} ${ANA}
#./submit.sh ${SITE} ${RUN}_zeroplusVSoneminus  ${NJOBS} ${NTOYS} ${zeroplusVSoneminus} ${LUMI} ${ANA}
#./submit.sh ${SITE} ${RUN}_zeroplusVStwohminus   ${NJOBS} ${NTOYS} ${zeroplusVStwohminus} ${LUMI} ${ANA}

# 1M is sufficient
#./submit.sh ${SITE} ${RUN}_zeroplusVSzerominus ${NJOBS} ${NTOYS} ${zeroplusVSzerominus} ${LUMI} ${ANA}
#./submit.sh ${SITE} ${RUN}_zeroplusVSzerohplus   ${NJOBS} ${NTOYS} ${zeroplusVSzerohplus} ${LUMI} ${ANA}
#./submit.sh ${SITE} ${RUN}_zeroplusVSoneplus   ${NJOBS} ${NTOYS} ${zeroplusVSoneplus} ${LUMI} ${ANA}
#./submit.sh ${SITE} ${RUN}_zeroplusVStwohplus   ${NJOBS} ${NTOYS} ${zeroplusVStwohplus} ${LUMI} ${ANA}


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
#NJOBS=10

./submit.sh ${SITE} ${RUN}_zeroplus_sig ${NJOBS} ${NTOYS} ${zeroplus} ${LUMI} ${ANA}
#./submit.sh ${SITE} ${RUN}_zerominus_sig ${NJOBS} ${NTOYS} ${zerominus} ${LUMI} ${ANA}
#./submit.sh ${SITE} ${RUN}_twoplus_sig ${NJOBS} ${NTOYS} ${twoplus} ${LUMI} ${ANA}
#./submit.sh ${SITE} ${RUN}_zerohplus_sig ${NJOBS} ${NTOYS} ${zerohplus} ${LUMI} ${ANA}
#./submit.sh ${SITE} ${RUN}_oneplus_sig ${NJOBS} ${NTOYS} ${oneplus} ${LUMI} ${ANA}
#./submit.sh ${SITE} ${RUN}_oneminus_sig ${NJOBS} ${NTOYS} ${oneminus} ${LUMI} ${ANA}
#./submit.sh ${SITE} ${RUN}_twohplus_sig ${NJOBS} ${NTOYS} ${twohplus} ${LUMI} ${ANA}
#./submit.sh ${SITE} ${RUN}_twohminus_sig ${NJOBS} ${NTOYS} ${twohminus} ${LUMI} ${ANA}

