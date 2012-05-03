import os,sys
import string, re
from time import gmtime, localtime, strftime

dataset    = [ 
              # Single Electrons done so far
              "/SingleElectron/ntran-ttbsm_v10_SingleElectron_Run2011A-PromptReco-v4-2900f36c5423fd804f580f1efac6dc75/USER",
              # Single Mu
              "/SingleMu/ntran-ttbsm_v10_SingleMu_Run2011A-May10ReReco-v1-2900f36c5423fd804f580f1efac6dc75/USER#b9858555-a16d-48c2-9727-9eefe7ce2fdd",
              # Double Electron
              "/DoubleElectron/dlopes-ttbsm_v10beta_Run2011A_May10ReReco-2900f36c5423fd804f580f1efac6dc75/USER",
              "/DoubleElectron/dlopes-ttbsm_v10beta_Run2011A_PromptRecoV4-2900f36c5423fd804f580f1efac6dc75/USER",
              "/DoubleElectron/dlopes-ttbsm_v10beta_Run2011A_Aug05ReReco-2900f36c5423fd804f580f1efac6dc75/USER",
              "/DoubleElectron/dlopes-ttbsm_v10beta_Run2011B_PromptRecoV1-2900f36c5423fd804f580f1efac6dc75/USER"
              ]


channels   = [
              # Single Electrons done so far
              "dat_ch_SingleEl_2011A_promptV4",
              # Single Mu
              "dat_ch_SingleMu_2011A_promptV4",
              # Double Electron
              "dat_ch_DoubleEl_2011A_May10",
              "dat_ch_DoubleEl_2011A_promptV4",
              "dat_ch_DoubleEl_2011A_Aug05",
              "dat_ch_DoubleEl_2011B_promptV1"
              ]

condor   = [1,1,1,1,1,1]



def changeCrabTemplateFile(index):
    fin  = open("crabTemplateVJetSubstructure_Data.cfg")
    pset_crab     = "crabjob_" + channels[index] + ".cfg"
    fout = open(pset_crab,"w")
    for line in fin.readlines():
        if  line.find("mydataset")!=-1:
            line=line.replace("mydataset",dataset[index])
            fout.write("\n")
        if  line.find("mypublishdataname")!=-1:
            line=line.replace("mypublishdataname", "ttbsm_v10beta_"+channels[index]+"_Fall11-PU_S6_START42_V14B")
        if  line.find("mypdirname")!=-1:
            line=line.replace("mypdirname",channels[index])                        
        if line.find("glite")!=-1 and condor[index]!=0:
            line=line.replace("glite", "condor")        
        fout.write(line)        
    if condor[index]!=0:
        fout.write("ce_white_list = cmssrm.fnal.gov")
      
    print pset_crab + " has been written.\n"



def setupFJ3(index):
    jobfile = channels[index]+"/job/CMSSW.sh"
    fin  = open(jobfile)
    fout = open(jobfile+".tmp","w")
    for line in fin.readlines():
        fout.write(line)
        if  line.find("eval `scram runtime -sh | grep -v SCRAMRT_LSB_JOBNAME`")!=-1:
            fout.write("\n")    
            fout.write("scram setup $CMS_PATH/slc5_amd64_gcc434/external/fastjet-toolfile/1.0-cms7/etc/scram.d/fastjet.xml")   
            fout.write("\n")
    child0 = os.system("mv " + jobfile+".tmp " + jobfile)
    print  "setup FJ3 has been done in file "+jobfile+"\n"

            
###################
for i in range(len(channels)):
    changeCrabTemplateFile(i)    
    #submitcommand = "crab -create -cfg " + "crabjob_" + channels[i] + ".cfg"
    #child   = os.system(submitcommand)
    #setupFJ3(i)
    #child2   = os.system("crab -submit -c "+channels[i])
