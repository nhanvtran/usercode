#!/bin/bash

#
# configuration
#

if [ ! $# -eq 7 ]; then
    echo "USAGE: ./submit.sh SITE RUN NJOBS NTOYS TESTTYPE ANA
	SITE - UCSD=0, FNAL=1
        RUN - name of run (will be a directory for this job)
        NJOBS - the number of jobs to submit
        NTOYS - the number of toys per job
        TESTTYPE - the TestType (see enums.h)
        LUMI -  luminosity in /fb  in integer
	ANA  - the analysis, choose from hypsep and sig"
    exit 1
fi

SITE=$1
RUN=$2
NJOBS=$3
NTOYS=$4
TESTTYPE=$5
LUMI=$6
ANA=$7

PROXY="/tmp/x509up_u${UID}"

#
# make input sandbox
#

if [ -d "${RUN}" ]; 
then 
    echo "Job directory ${RUN} already exists"
    exit 1
else 
    mkdir -p ${RUN}/log
fi

if [ -e input.tar ]; then rm input.tar; fi   
tar -cf input.tar statsFactory.cc tdrstyle.C runSigSepWW.C enums.h runsignificancexwwcuts.C
mv input.tar ${RUN}
cp wrapper.sh ${RUN}

#
# print the submit file
#

DESIRED_SITE=""
if [ $SITE == 0 ]; then
    DESIRED_SITE="UCSD"
elif [ $SITE == 1 ]; then
    DESIRED_SITE="FNAL"
fi


echo "
# condor parameters
universe=vanilla
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
+DESIRED_Sites=\"${DESIRED_SITE}\"
+Owner = undefined
notification=Never
x509userproxy=${PROXY}

# job parameters
Executable=wrapper.sh
transfer_input_files=input.tar
arguments= $SITE \$(Process) ${NTOYS} ${TESTTYPE} ${LUMI} ${ANA}
Error=log/err_\$(Cluster).\$(Process)
Output=log/out_\$(Cluster).\$(Process)
Log=log/log_\$(Cluster).log

# how many jobs to submit
Queue ${NJOBS}" > ${RUN}/condor_config.cmd

#
# submit
#

WORKDIR=`pwd`
cd ${RUN}
condor_submit condor_config.cmd
cd ${WORKDIR}

