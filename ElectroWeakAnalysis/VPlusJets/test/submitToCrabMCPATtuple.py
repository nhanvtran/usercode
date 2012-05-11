import os,sys
import string, re
from time import gmtime, localtime, strftime

dataset    = [ 
##               # diboson
##               "/WW_TuneZ2_7TeV_pythia6_tauola/kalanand-ttbsm_v10beta_WWtoAnything_Fall11-PU_S6_START42_V14B-a326ba49a16ab761c492392538b61378/USER",
##               "/WZ_TuneZ2_7TeV_pythia6_tauola/kalanand-ttbsm_v10beta_WZtoAnything_Fall11-PU_S6_START42_V14B-a326ba49a16ab761c492392538b61378/USER",
##               "/ZZ_TuneZ2_7TeV_pythia6_tauola/kalanand-ttbsm_v10beta_ZZtoAnything_Fall11-PU_S6_START42_V14B-a326ba49a16ab761c492392538b61378/USER",
##               # ttbar
##               "/TTJets_TuneZ2_7TeV-madgraph-tauola/kalanand-ttbsm_v10beta_TTJets_Fall11-PU_S6_START42_V14B-a326ba49a16ab761c492392538b61378/USER",
##               # W+jets
##               "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/ntran-ttbsm_v10_WJetsToLNu_TuneZ2_7TeV-madgraph-tauola_Fall11-PU_S6_START42_V14B-v1-a326ba49a16ab761c492392538b61378/USER",
              "/WJetsToLNu_PtW-100_TuneZ2_7TeV-madgraph/dlopes-ttbsm_v10beta_WJetsToLNu_PtW-100_TuneZ2_7TeV-madgraph-a326ba49a16ab761c492392538b61378/USER",
              "/WJetsToLNu_Pt-100_7TeV-herwigpp/dlopes-ttbsm_v10beta_WJetsToLNu_Pt-100_7TeV-herwigpp-a326ba49a16ab761c492392538b61378/USER",
              # Z+jets
              "/DYJetsToLL_PtZ-100_TuneZ2_7TeV-madgraph-tauola/mulhearn-mulhearn-ttbsm_DYJetsToLL_PtZ-100_TuneZ2_7TeV-madgraph-tauola_Fall11-a326ba49a16ab761c492392538b61378/USER",
              "/ZJetsToLL_Pt-100_7TeV-herwigpp/mulhearn-mulhearn-ttbsm_ZJetsToLL_Pt-100_7TeV-herwigpp_Fall11-a326ba49a16ab761c492392538b61378/USER",
              # single top
              "/Tbar_TuneZ2_s-channel_7TeV-powheg-tauola/kalanand-ttbsm_v10beta_Tbar_s-channel_Fall11-PU_S6_START42_V14B-a326ba49a16ab761c492392538b61378/USER",
              "/Tbar_TuneZ2_t-channel_7TeV-powheg-tauola/kalanand-ttbsm_v10beta_Tbar_t-channel_Fall11-PU_S6_START42_V14B-a326ba49a16ab761c492392538b61378/USER",
              "/Tbar_TuneZ2_tW-channel-DS_7TeV-powheg-tauola/kalanand-ttbsm_v10beta_Tbar_tW-channel-DS_Fall11-PU_S6_START42_V14B-a326ba49a16ab761c492392538b61378/USER",
              "/Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/kalanand-ttbsm_v10beta_Tbar_tW-channel-DR_Fall11-PU_S6_START42_V14B-a326ba49a16ab761c492392538b61378/USER",
              "/T_TuneZ2_s-channel_7TeV-powheg-tauola/kalanand-ttbsm_v10beta_T_s-channel_Fall11-PU_S6_START42_V14B-a326ba49a16ab761c492392538b61378/USER",
              "/T_TuneZ2_t-channel_7TeV-powheg-tauola/kalanand-ttbsm_v10beta_T_t-channel_Fall11-PU_S6_START42_V14B-a326ba49a16ab761c492392538b61378/USER",
              "/T_TuneZ2_tW-channel-DS_7TeV-powheg-tauola/kalanand-ttbsm_v10beta_T_tW-channel-DS_Fall11-PU_S6_START42_V14B-a326ba49a16ab761c492392538b61378/USER",
              "/T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/kalanand-ttbsm_v10beta_T_tW-channel-DR_Fall11-PU_S6_START42_V14B-a326ba49a16ab761c492392538b61378/USER"
              ]


channels   = [
## ##     "WJets",
##     "ch_WWtoAnything",    
##     "ch_WZtoAnything",    
##     "ch_ZZtoAnything",
    
##     "ch_TTbar",
    
##     "ch_WJets_inclusive",
    "ch_WJets_boostedMadGraph",
    "ch_WJets_boostedHerwig",

    "ch_ZJets_boostedMadGraph",              
    "ch_ZJets_boostedHerwig",     
              
    "ch_singleTbar_s",                   
    "ch_singleTbar_t",                   
    "ch_singleTbar_DS",                   
    "ch_singleTbar_DR",                                 
    "ch_singleT_s",                   
    "ch_singleT_t",                   
    "ch_singleT_DS",                   
    "ch_singleT_DR",                                 
              
]

condor   = [
##             1,1,1,1,1,
            1,1,1,1,1,
            1,1,1,1,1,
            1,1
            ]

def changeCrabTemplateFile(index):
    fin  = open("crabTemplateVJetSubstructure_MC.cfg")
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
    submitcommand = "crab -create -cfg " + "crabjob_" + channels[i] + ".cfg"
    child   = os.system(submitcommand)
    setupFJ3(i)
    child2   = os.system("crab -submit -c "+channels[i])
