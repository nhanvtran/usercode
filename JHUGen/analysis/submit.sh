#!/bin/bash

#
# Note, you need to have the same version of the root for the library, do this first
# root [0] gSystem->AddIncludePath(" -I/code/osgcode/cmssoft/cms/slc5_amd64_gcc462/lcg/roofit/5.32.00-cms5/include/");
# root [1] .L statsFactory.cc++

#
# configuration
#

if [ ! $# -eq 3 ]; then
    echo "USAGE: ./submit.sh NJOBS NTOYS
        NJOBS - the number of jobs to submit
        NTOYS - the number of toys per job
        RUN - name of run (will be a directory for this job)"
    exit 1
fi

NJOBS=$1
NTOYS=$2
RUN=$3
PROXY="/tmp/x509up_u${UID}"

#
# make input sandbox
#

if [ -d "${RUN}" ]; 
then 
    echo "Job directory already exists"
    exit 1
else 
    mkdir -p ${RUN}/log
fi

if [ -e input.tar ]; then rm input.tar; fi   
tar -cf input.tar statsFactory.cc tdrstyle.C runSigSepWW.C enums.h
mv input.tar ${RUN}
cp wrapper.sh ${RUN}

#
# print the submit file
#

echo "
# condor parameters
universe=vanilla
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
+DESIRED_Sites=\"UCSD\"
+Owner = undefined
notification=Never
x509userproxy=${PROXY}

# job parameters
Executable=wrapper.sh
transfer_input_files=input.tar
arguments=${NTOYS} \$(Process)
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

