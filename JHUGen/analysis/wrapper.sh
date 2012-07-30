#!/bin/bash

#
# configuration
#

if [ ! $# -eq 4 ]; then
    echo "USAGE: ./wrapper.sh SEED NTOYS TESTTYPE 
        SEED  - the random seed
        NTOYS - the number of toys
        TESTTYPE - the TestType (see enums.h)
	ANA - the anaysis, either hypsep or sig	"
    exit 1
fi

SEED=$1
NTOYS=$2
TESTTYPE=$3
ANA=$4
 
#
# set up environment
#

echo "[wrapper] setting env"
export SCRAM_ARCH=slc5_amd64_gcc462
source /code/osgcode/cmssoft/cms/cmsset_default.sh
source /code/osgcode/ucsdt2/gLite32/etc/profile.d/grid_env.sh
export ROOTSYS=/code/osgcode/cmssoft/cms/slc5_amd64_gcc462/cms/cmssw/CMSSW_5_2_3/external/slc5_amd64_gcc462/
export LD_LIBRARY_PATH=$ROOTSYS/lib:${CMS_PATH}/slc5_amd64_gcc462/external/gcc/4.6.2/lib64/:$LD_LIBRARY_PATH
export PATH=$HOME/bin:$ROOTSYS/bin:$PATH
export PYTHONPATH=$ROOTSYS/lib:$PYTHONPATH

#
# print debug information
#

#hostname
#date
#ls

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
    echo "[wrapper] running root -b -q runSigSepWW.C\(${SEED},${NTOYS},${TESTTYPE}\)"
    root -b -q runSigSepWW.C\(${SEED},${NTOYS},${TESTTYPE}\)
fi


if [ "${ANA}" == "sig" ]; then
    echo "[wrapper] running root -b -q runsignificancexwwcuts.C\(${SEED},${NTOYS},${TESTTYPE}\)"
    root -b -q runsignificancexwwcuts.C\(${SEED},${NTOYS},${TESTTYPE}\)
fi


#
# clean up
#

echo "[wrapper] copying output to initial dir"
cp *.root ${WORKDIR}
cd ${WORKDIR}
ls

