import os
import glob
import math
import time

import ROOT
from ROOT import *
from ROOT import gROOT, gStyle, gSystem, TLatex
import subprocess

from subprocess import Popen
from optparse import OptionParser

############################################################
############################################
#            Job steering                  #
############################################
parser = OptionParser()

parser.add_option('-b', action='store_true', dest='noX', default=False,
                  help='no X11 windows')

parser.add_option('--createTree', action='store_true', dest='createTree', default=False,
                  help='no X11 windows')

# submit jobs to condor
parser.add_option('--batchMode', action='store_true', dest='batchMode', default=False,
                  help='no X11 windows')
parser.add_option('--sampleToProcess',action="store",type="string",dest="sampleToProcess",default=None)

parser.add_option('--channel',action="store",type="string",dest="channel",default="mu")


(options, args) = parser.parse_args()
############################################################
############################################################


def submitBatchJob( command, fn ):

    currentDir = os.getcwd();
    
    # create a dummy bash/csh
    outScript=open(fn+".sh","w");

    outScript.write('#!/bin/bash');
    outScript.write("\n"+'date');
    outScript.write("\n"+'source /uscmst1/prod/sw/cms/bashrc prod');
    outScript.write("\n"+'cd '+currentDir);
    outScript.write("\n"+'eval `scram runtime -sh`');
    outScript.write("\n"+command);
    outScript.close();

    # link a condor script to your shell script
    condorScript=open("condor_"+fn,"w");
    condorScript.write('universe = vanilla')
    condorScript.write("\n"+"Executable = "+fn+".sh")
    condorScript.write("\n"+'Requirements = Memory >= 199 &&OpSys == "LINUX"&& (Arch != "DUMMY" )&& Disk > 1000000')
    condorScript.write("\n"+'Should_Transfer_Files = YES')
    condorScript.write("\n"+'WhenToTransferOutput  = ON_EXIT_OR_EVICT')
    condorScript.write("\n"+'Output = out_$(Cluster).stdout')
    condorScript.write("\n"+'Error  = out_$(Cluster).stderr')
    condorScript.write("\n"+'Error  = out_$(Cluster).stderr')
    condorScript.write("\n"+'Log    = out_$(Cluster).log')
    condorScript.write("\n"+'Notification    = Error')
    condorScript.write("\n"+'Queue 1')
    condorScript.close();

    # submit the condor job 

    os.system("condor_submit "+"condor_"+fn)
    
#    time.sleep(0.5);
#    os.system("mv "+"condor_"+fn+" "+fn+".sh"+" condorTmp/.");


if __name__ == '__main__':

    all = [
           "data",
           "ggH600",
           "ggH700",
           "ggH800",
           "ggH900",           
           "ggH1000",
           "vbfH600",
           "vbfH700",
           "vbfH800",
           "vbfH900",           
           "vbfH1000",
           "WJets_Pythia",
           "WJets_Herwig",
           "ZJets",
           "TTbar",
           "TTbar_Powheg",           
           "TTbar_matchDn",           
           "TTbar_matchUp",                      
           "TTbar_scaleDn",           
           "TTbar_scaleUp",                      
           "WW",           
           "WZ",                      
           "ZZ",
           "tch",
           "tWch",
           "sch",
           "tch_bar",
           "tWch_bar",
           "sch_bar"
           ]
        
    if options.sampleToProcess == "all" and options.batchMode and options.createTree:
    
        for i in range(len(all)):
            
            cmmd = "python runAnalysis.py -b --createTrees --channel "+options.channel+" --sampleToProcess "+ all[i]
            print cmmd
            fn = "createTreeScript_%s_%s"%(options.channel,all[i]);
            submitBatchJob( cmmd, fn );

    
    elif options.createTree and options.batchMode and not options.sampleToProcess == None:

        cmmd = "python runAnalysis.py -b --createTrees --channel "+options.channel+" --sampleToProcess "+ options.sampleToProcess
        print cmmd
        fn = "createTreeScript_%s_%s"%(options.channel,options.sampleToProcess);
        submitBatchJob( cmmd, fn );

    else:
        print "do nothing"






