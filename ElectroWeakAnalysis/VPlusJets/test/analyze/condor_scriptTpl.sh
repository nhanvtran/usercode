#!/bin/bash

date

source /uscmst1/prod/sw/cms/bashrc prod

cd LOCATION
eval `scram runtime -sh`
python vJetSubstructureAnalysis.py OPTIONS
