#!/bin/bash

#
# configuration
#

if [ ! $# -eq 2 ]; then
    echo "USAGE: ./submit.sh NTOYS SEEDS
        NTOYS - the number of toys
        SEED  - the random seed"
    exit 1
fi

NTOYS=$1
SEED=$2

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

echo "[wrapper] running root -b -q runSigSepWW.C\(${NTOYS},${SEED}\)"
root -b -q runSigSepWW.C\(${NTOYS},${SEED}\)

#
# clean up
#

echo "[wrapper] copying output to initial dir"
cp *.root ${WORKDIR}
cd ${WORKDIR}
ls

