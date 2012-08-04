#!/bin/bash

#
# configuration
#

if [ ! $# -eq 6 ]; then
    echo "USAGE: ./wrapper.sh SITE SEED NTOYS TESTTYPE 
	SITE  - UCSD=0, FNAL=1
        SEED  - the random seed
        NTOYS - the number of toys
        TESTTYPE - the TestType (see enums.h)
	LUMI - the luminosity in fb integer
	ANA - the anaysis, either hypsep or sig	"
    exit 1
fi

SITE=$1
SEED=$2
NTOYS=$3
TESTTYPE=$4
LUMI=$5
ANA=$6

#
# set up environment
#

echo "[wrapper] setting env"
export SCRAM_ARCH=slc5_amd64_gcc462

if [ $SITE == 0 ]; then
    source /code/osgcode/cmssoft/cms/cmsset_default.sh
    source /code/osgcode/ucsdt2/gLite32/etc/profile.d/grid_env.sh
    export ROOTSYS=/code/osgcode/cmssoft/cms/slc5_amd64_gcc462/cms/cmssw/CMSSW_5_2_3/external/slc5_amd64_gcc462/
elif [ $SITE == 1 ]; then
    source /uscmst1/prod/sw/cms/shrc prod
    export ROOTSYS=/uscmst1/prod/sw/cms/slc5_amd64_gcc462/cms/cmssw/CMSSW_5_2_5/external/slc5_amd64_gcc462/
fi

export LD_LIBRARY_PATH=$ROOTSYS/lib:${CMS_PATH}/slc5_amd64_gcc462/external/gcc/4.6.2/lib64/:$LD_LIBRARY_PATH
export PATH=$HOME/bin:$ROOTSYS/bin:$PATH
export PYTHONPATH=$ROOTSYS/lib:$PYTHONPATH

#
# print debug information
#

hostname
date
ls

#
# untar and run
#
echo "[wrapper] untarring"
WORKDIR=`pwd`
mkdir tmp
mv input.tar tmp/
cd tmp/
tar -xvf input.tar

if [ "${ANA}" == "hypsep" ]; then
    echo "[wrapper] running root -b -q runSigSepWW.C\(${SITE},${SEED},${NTOYS},${TESTTYPE},${LUMI}\)"
    root -b -q runSigSepWW.C\(${SITE},${SEED},${NTOYS},${TESTTYPE},${LUMI}\)
fi


if [ "${ANA}" == "sig" ]; then
    echo "[wrapper] running root -b -q runsignificancexwwcuts.C\(${SITE},${SEED},${NTOYS},${TESTTYPE},${LUMI}\)"
    root -b -q runsignificancexwwcuts.C\(${SITE},${SEED},${NTOYS},${TESTTYPE},${LUMI}\)
fi


#
# clean up
#

echo "[wrapper] copying output to initial dir"
cp *.root ${WORKDIR}
cd ${WORKDIR}
ls

