#! /usr/bin/env python
import os
import glob
import math

from optparse import OptionParser
from ROOT import TH1F, TCanvas, gROOT

############################################
#            Job steering                  #
############################################
parser = OptionParser()
parser.add_option('-b', action='store_true', dest='noX', default=False,
                  help='no X11 windows')
#### for processing nutples
parser.add_option('-r', '--runAnalysis', action='store_true', dest='runAnalysis', default=False, 
                  help='include if you want to do analysis')
parser.add_option('-n', '--numfile',
                  action='store', type='int', dest='runOnFile',default=-1)
#### for making histograms
parser.add_option('-m', '--makeHistos', action='store_true', dest='makeHistos', default=False, 
                  help='include if you want to build histograms on the fly')
parser.add_option('-c', '--channel',
                  action='store', type='int', dest='channelToBuild',default=1)

#### for ploting
parser.add_option('-p', '--writePlots', action='store_true', dest='writePlots', default=False, 
                  help='include if you want to produce plots')
parser.add_option('-a', '--addFiles', action='store_true', dest='addFiles', default=False, 
                  help='when producing plots, if you need to merge histogram files')


(options, args) = parser.parse_args()

# Input files to use. This is in "glob" format, so you can use wildcards.
# If you get a "cannot find file" type of error, be sure to use "\*" instead
# of "*" to make sure you don't confuse the shell. 
#parser.add_option('--files', metavar='F', type='string', action='store',
#                  dest='files',help='Input files')

(options, args) = parser.parse_args()

argv = []

odir = "ntuples_v1"
#odir = "ntuples_v21"
chan = options.channelToBuild

dataset    = [
              # ww sample (0-2)
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_WWtoAnything/demo*.root",      
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_WZtoAnything/demo*.root",         
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_ZZtoAnything/demo*.root",      
#              ## w + jets sample, split into 8 (3-10), 324 CRAB jobs
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_WJets_inclusive/demo_1[0-4]*_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_WJets_inclusive/demo_1[5-9]*_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_WJets_inclusive/demo_2[0-4]*_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_WJets_inclusive/demo_2[5-9]*_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_WJets_inclusive/demo_3[0-9]*_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_WJets_inclusive/demo_[1-4][0-9]_*.root",   
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_WJets_inclusive/demo_[5-9][0-9]_*.root",   
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_WJets_inclusive/demo_[1-9]_*_*.root",
              ## w + jets boosted, madgraph (11-14), 4, 33 CRAB jobs
              ## 33
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_WJets_boostedMadGraph/demo_[1-9]_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_WJets_boostedMadGraph/demo_[1][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_WJets_boostedMadGraph/demo_[2][0-9]_*.root",  
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_WJets_boostedMadGraph/demo_[3][0-9]_*.root",                
              ## w + jets boosted, herwig (15-23), 9, 88 CRAB jobs
              ## 88
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_WJets_boostedHerwig/demo_[1-9]_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_WJets_boostedHerwig/demo_[1][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_WJets_boostedHerwig/demo_[2][0-9]_*.root",  
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_WJets_boostedHerwig/demo_[3][0-9]_*.root",                
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_WJets_boostedHerwig/demo_[4][0-9]_*.root",                
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_WJets_boostedHerwig/demo_[5][0-9]_*.root",                    
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_WJets_boostedHerwig/demo_[6][0-9]_*.root",                
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_WJets_boostedHerwig/demo_[7][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_WJets_boostedHerwig/demo_[8][0-9]_*.root",              
              ## Z + jets inclusive, 145 CRAB jobs
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_ZJets_inclusive/demo_[0-9]_*.root",                            
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_ZJets_inclusive/demo_[1-2][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_ZJets_inclusive/demo_[3-4][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_ZJets_inclusive/demo_[5-6][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_ZJets_inclusive/demo_[7-8][0-9]_*.root",              
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_ZJets_inclusive/demo_[9][0-9]_*.root",                            
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_ZJets_inclusive/demo_1[0-2][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_ZJets_inclusive/demo_1[3-9][0-9]_*.root",
              ## Z + jets boosted, madgraph (24-27), 4, 5 CRAB jobs
              ## 5
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_ZJets_boostedMadGraph/demo_1*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_ZJets_boostedMadGraph/demo_2*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_ZJets_boostedMadGraph/demo_3*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_ZJets_boostedMadGraph/demo_4*.root",              
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_ZJets_boostedMadGraph/demo_[5-9]*.root",                            
              ## Z + jets boosted, herwig (27-30), 4, 11 CRAB jobs
              ## 11
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_ZJets_boostedHerwig/demo_1*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_ZJets_boostedHerwig/demo_[2-4]*.root",    
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_ZJets_boostedHerwig/demo_[5-7]*.root",                  
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_ZJets_boostedHerwig/demo_[8-9]*.root",                                
              ## ttbar sample -- this one is huge, split into 12 (31-42), 238 CRAB jobs
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_TTbar/demo_1[0-1][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_TTbar/demo_1[2-3][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_TTbar/demo_1[4-5][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_TTbar/demo_1[6-7][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_TTbar/demo_1[8-9][0-9]_*.root",              
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_TTbar/demo_2[0-2][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_TTbar/demo_2[3-4][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_TTbar/demo_[1-2][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_TTbar/demo_[3-4][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_TTbar/demo_[5-6][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_TTbar/demo_[7-9][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_TTbar/demo_[1-9]_*_*.root",
              ## single top - 8 samples (43-50)
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_singleTbar_s/demo_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_singleTbar_t/demo_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_singleTbar_DR/demo_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_singleTbar_DS/demo_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_singleT_s/demo_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_singleT_t/demo_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_singleT_DR/demo_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/ch_singleT_DS/demo_*.root",
              ###################
              ###################
              ###################
              ## data, single el and elehad (51-61), 51/83/24/40/94
              ## 51/83/24/40/93
              #"/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleEl_2011A_promptV4/demo_[1-4]*.root",
              #"/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleEl_2011A_promptV4/demo_[5-9]*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleEl_2011A_May10/demo_[1-3]*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleEl_2011A_May10/demo_[4-9]*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleEl_2011A_promptV4/demo_[1-4]*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleEl_2011A_promptV4/demo_[5-9]*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleEl_2011A_Aug05/demo_*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleEl_2011A_promptV6/demo_[1-2]*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleEl_2011A_promptV6/demo_[3-9]*.root",              
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleEl_2011B_promptV1/demo_[1-2]*.root", 
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleEl_2011B_promptV1/demo_[3-4]*.root", 
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleEl_2011B_promptV1/demo_[5-6]*.root", 
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleEl_2011B_promptV1/demo_[7-9]*.root", 
              ## data, double el (62-72), 52/90/24/40/94 CRAB jobs
              ## 51/90/24/40/94
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_DoubleEl_2011A_May10/demo_[1-3]*.root",               
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_DoubleEl_2011A_May10/demo_[4-9]*.root",                             
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_DoubleEl_2011A_promptV4/demo_[1-4]*.root", 
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_DoubleEl_2011A_promptV4/demo_[5-9]*.root",                             
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_DoubleEl_2011A_Aug05/demo_*.root",               
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_DoubleEl_2011A_promptV6/demo_[1-2]*.root",               
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_DoubleEl_2011A_promptV6/demo_[3-9]*.root",                             
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_DoubleEl_2011B_promptV1/demo_[1-2]*.root",    
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_DoubleEl_2011B_promptV1/demo_[3-4]*.root",                             
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_DoubleEl_2011B_promptV1/demo_[5-6]*.root",                             
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_DoubleEl_2011B_promptV1/demo_[7-9]*.root",                                           
              ## data, single mu (73-78), 53/91/25/40/94 CRAB jobs
              ## 52/91/25/40/93
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleMu_2011A_May10/demo_[1-3]*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleMu_2011A_May10/demo_[4-9]*.root",              
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleMu_2011A_promptV4/demo_[1-4]*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleMu_2011A_promptV4/demo_[5-9]*.root",
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleMu_2011A_Aug05/demo_*.root", 
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleMu_2011A_promptV6/demo_[1-2]*.root",                             
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleMu_2011A_promptV6/demo_[3-9]*.root",                             
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleMu_2011B_promptV1/demo_[1-2]*.root",                
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleMu_2011B_promptV1/demo_[3-4]*.root",              
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleMu_2011B_promptV1/demo_[5-6]*.root",              
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleMu_2011B_promptV1/demo_[7]*.root",                            
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleMu_2011B_promptV1/demo_[8]*.root",                            
              "/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV9/dat_ch_SingleMu_2011B_promptV1/demo_[9]*.root"                            
              ]
onames     = [
              odir+"/WW.root",odir+"/WZ.root",odir+"/ZZ.root",
#              #
              odir+"/WJetsInclusive_1.root",odir+"/WJetsInclusive_2.root",odir+"/WJetsInclusive_3.root",odir+"/WJetsInclusive_4.root",
              odir+"/WJetsInclusive_5.root",odir+"/WJetsInclusive_6.root",odir+"/WJetsInclusive_7.root",odir+"/WJetsInclusive_8.root",
              #
              odir+"/WJets_boostedMadGraph_1.root",odir+"/WJets_boostedMadGraph_2.root",odir+"/WJets_boostedMadGraph_3.root",odir+"/WJets_boostedMadGraph_4.root",
              #
              odir+"/WJets_boostedHerwig_1.root",odir+"/WJets_boostedHerwig_2.root",odir+"/WJets_boostedHerwig_3.root",odir+"/WJets_boostedHerwig_4.root",
              odir+"/WJets_boostedHerwig_5.root",odir+"/WJets_boostedHerwig_6.root",odir+"/WJets_boostedHerwig_7.root",odir+"/WJets_boostedHerwig_8.root",
              odir+"/WJets_boostedHerwig_9.root",
              #
              odir+"/ZJetsInclusive_1.root",odir+"/ZJetsInclusive_2.root",odir+"/ZJetsInclusive_3.root",
              odir+"/ZJetsInclusive_4.root",odir+"/ZJetsInclusive_5.root",odir+"/ZJetsInclusive_6.root",
              odir+"/ZJetsInclusive_7.root",odir+"/ZJetsInclusive_8.root",
              #
              odir+"/ZJets_boostedMadGraph_1.root",odir+"/ZJets_boostedMadGraph_2.root",odir+"/ZJets_boostedMadGraph_3.root",odir+"/ZJets_boostedMadGraph_4.root",odir+"/ZJets_boostedMadGraph_5.root",
              odir+"/ZJets_boostedHerwig_1.root",odir+"/ZJets_boostedHerwig_2.root",odir+"/ZJets_boostedHerwig_3.root",odir+"/ZJets_boostedHerwig_4.root",              
              #
              odir+"/TTbar_1.root",odir+"/TTbar_2.root",odir+"/TTbar_3.root",odir+"/TTbar_4.root",
              odir+"/TTbar_5.root",odir+"/TTbar_6.root",odir+"/TTbar_7.root",odir+"/TTbar_8.root",
              odir+"/TTbar_9.root",odir+"/TTbar_10.root",odir+"/TTbar_11.root",odir+"/TTbar_12.root",
              #
              odir+"/singleT_s.root",odir+"/singleT_t.root",odir+"/singleT_dr.root",odir+"/singleT_ds.root",
              odir+"/singleTbar_s.root",odir+"/singleTbar_t.root",odir+"/singleTbar_dr.root",odir+"/singleTbar_ds.root",
              #
              #
              #
              odir+"/dat_SingleEl_2011A_May10_1.root",
              odir+"/dat_SingleEl_2011A_May10_2.root",             
              odir+"/dat_SingleEl_2011A_promptV4_1.root",                           
              odir+"/dat_SingleEl_2011A_promptV4_2.root",                  
              odir+"/dat_SingleEl_2011A_Aug05_1.root",                  
              odir+"/dat_SingleEl_2011A_promptV6_1.root",                                
              odir+"/dat_SingleEl_2011A_promptV6_2.root",
              odir+"/dat_SingleEl_2011B_promptV1_1.root",              
              odir+"/dat_SingleEl_2011B_promptV1_2.root",              
              odir+"/dat_SingleEl_2011B_promptV1_3.root",              
              odir+"/dat_SingleEl_2011B_promptV1_4.root",                            
              #
              odir+"/dat_DoubleEl_2011A_May10_1.root",
              odir+"/dat_DoubleEl_2011A_May10_2.root",             
              odir+"/dat_DoubleEl_2011A_promptV4_1.root",                           
              odir+"/dat_DoubleEl_2011A_promptV4_2.root",                  
              odir+"/dat_DoubleEl_2011A_Aug05_1.root",                  
              odir+"/dat_DoubleEl_2011A_promptV6_1.root",                                
              odir+"/dat_DoubleEl_2011A_promptV6_2.root",
              odir+"/dat_DoubleEl_2011B_promptV1_1.root",              
              odir+"/dat_DoubleEl_2011B_promptV1_2.root",              
              odir+"/dat_DoubleEl_2011B_promptV1_3.root",              
              odir+"/dat_DoubleEl_2011B_promptV1_4.root",                            
              #
              odir+"/dat_SingleMu_2011A_May10_1.root",
              odir+"/dat_SingleMu_2011A_May10_2.root",             
              odir+"/dat_SingleMu_2011A_promptV4_1.root",
              odir+"/dat_SingleMu_2011A_promptV4_2.root",
              odir+"/dat_SingleMu_2011A_Aug05_1.root",
              odir+"/dat_SingleMu_2011A_promptV6_1.root",
              odir+"/dat_SingleMu_2011A_promptV6_2.root",              
              odir+"/dat_SingleMu_2011B_promptV1_1.root",
              odir+"/dat_SingleMu_2011B_promptV1_2.root",
              odir+"/dat_SingleMu_2011B_promptV1_3.root",
              odir+"/dat_SingleMu_2011B_promptV1_4.root",              
              odir+"/dat_SingleMu_2011B_promptV1_5.root",              
              odir+"/dat_SingleMu_2011B_promptV1_6.root"                            
              ] 

hnames     = [
              odir+"/hWW",odir+"/hWZ",odir+"/hZZ",
              # W jets
              odir+"/hWJetsInclusive_1",odir+"/hWJetsInclusive_2",odir+"/hWJetsInclusive_3",odir+"/hWJetsInclusive_4",
              odir+"/hWJetsInclusive_5",odir+"/hWJetsInclusive_6",odir+"/hWJetsInclusive_7",odir+"/hWJetsInclusive_8",
              # W jets, boosted madgraph
              odir+"/hWJets_boostedMadGraph_1",odir+"/hWJets_boostedMadGraph_2",odir+"/hWJets_boostedMadGraph_3",odir+"/hWJets_boostedMadGraph_4",
              # W jets, boosted herwig
              odir+"/hWJets_boostedHerwig_1",odir+"/hWJets_boostedHerwig_2",odir+"/hWJets_boostedHerwig_3",odir+"/hWJets_boostedHerwig_4",
              odir+"/hWJets_boostedHerwig_5",odir+"/hWJets_boostedHerwig_6",odir+"/hWJets_boostedHerwig_7",odir+"/hWJets_boostedHerwig_8",
              odir+"/hWJets_boostedHerwig_9",
              # Z jets
              odir+"/hZJetsInclusive_1",odir+"/hZJetsInclusive_2",odir+"/hZJetsInclusive_3",
              odir+"/hZJetsInclusive_4",odir+"/hZJetsInclusive_5",odir+"/hZJetsInclusive_6",
              odir+"/hZJetsInclusive_7",odir+"/hZJetsInclusive_8",
              # Z jets, boosted madgraph
              odir+"/hZJets_boostedMadGraph_1",odir+"/hZJets_boostedMadGraph_2",odir+"/hZJets_boostedMadGraph_3",odir+"/hZJets_boostedMadGraph_4",odir+"/hZJets_boostedMadGraph_5",
              # Z jets, boosted herwig
              odir+"/hZJets_boostedHerwig_1",odir+"/hZJets_boostedHerwig_2",odir+"/hZJets_boostedHerwig_3",odir+"/hZJets_boostedHerwig_4",
              #
              odir+"/hTTbar_1",odir+"/hTTbar_2",odir+"/hTTbar_3",odir+"/hTTbar_4",
              odir+"/hTTbar_5",odir+"/hTTbar_6",odir+"/hTTbar_7",odir+"/hTTbar_8",
              odir+"/hTTbar_9",odir+"/hTTbar_10",odir+"/hTTbar_11",odir+"/hTTbar_12",
              #
              odir+"/hsingleT_s",odir+"/hsingleT_t",odir+"/hsingleT_dr",odir+"/hsingleT_ds",
              odir+"/hsingleTbar_s",odir+"/hsingleTbar_t",odir+"/hsingleTbar_dr",odir+"/hsingleTbar_ds",
              #
              #
              #
              odir+"/hSingleEl_2011A_May10_1",
              odir+"/hSingleEl_2011A_May10_2",             
              odir+"/hSingleEl_2011A_promptV4_1",                           
              odir+"/hSingleEl_2011A_promptV4_2",                  
              odir+"/hSingleEl_2011A_Aug05_1",                  
              odir+"/hSingleEl_2011A_promptV6_1",                                
              odir+"/hSingleEl_2011A_promptV6_2",
              odir+"/hSingleEl_2011B_promptV1_1",              
              odir+"/hSingleEl_2011B_promptV1_2",              
              odir+"/hSingleEl_2011B_promptV1_3",              
              odir+"/hSingleEl_2011B_promptV1_4",                            
              #
              odir+"/hDoubleEl_2011A_May10_1",
              odir+"/hDoubleEl_2011A_May10_2",             
              odir+"/hDoubleEl_2011A_promptV4_1",                           
              odir+"/hDoubleEl_2011A_promptV4_2",                  
              odir+"/hDoubleEl_2011A_Aug05_1",                  
              odir+"/hDoubleEl_2011A_promptV6_1",                                
              odir+"/hDoubleEl_2011A_promptV6_2",
              odir+"/hDoubleEl_2011B_promptV1_1",              
              odir+"/hDoubleEl_2011B_promptV1_2",              
              odir+"/hDoubleEl_2011B_promptV1_3",              
              odir+"/hDoubleEl_2011B_promptV1_4",                            
              #
              odir+"/hSingleMu_2011A_May10_1",
              odir+"/hSingleMu_2011A_May10_2",             
              odir+"/hSingleMu_2011A_promptV4_1",
              odir+"/hSingleMu_2011A_promptV4_2",             
              odir+"/hSingleMu_2011A_Aug05_1",
              odir+"/hSingleMu_2011A_promptV6_1",
              odir+"/hSingleMu_2011A_promptV6_2",             
              odir+"/hSingleMu_2011B_promptV1_1",
              odir+"/hSingleMu_2011B_promptV1_2",
              odir+"/hSingleMu_2011B_promptV1_3",
              odir+"/hSingleMu_2011B_promptV1_4",              
              odir+"/hSingleMu_2011B_promptV1_5",
              odir+"/hSingleMu_2011B_promptV1_6"              
              ] 
hnamesAll  =  odir+"/hAllMC"
hnamesDat  =  odir+"/hDat"

isData = [
          0,0,0,
          # wj
          0,0,0,0,0,0,0,0,
          0,0,0,0,
          0,0,0,0,0,0,0,0,0,
          # zj
          0,0,0,0,0,0,0,0,
          0,0,0,0,0,
          0,0,0,0,
          # ttbar
          0,0,0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,
          #
          1,1,1,1,1,1,1,1,1,1,1,
          1,1,1,1,1,1,1,1,1,1,1,
          1,1,1,1,1,1,1,1,1,1,1,1,1
          ]


LUMI = 4.980
sf_WW = LUMI*47000./4216917.
sf_WZ = LUMI*18600./4259651.
sf_ZZ = LUMI*6400./4173452.
sf_Wjets = LUMI*31300000./80978873
sf_Wjets_bMG = LUMI*251800/8070702
sf_Wjets_bHW = LUMI*251800/21908218
sf_Zjets = LUMI*3048000/36186671
sf_Zjets_bMG = LUMI*33540/1134992
sf_Zjets_bHW = LUMI*33540/2743732
sf_ttbar = LUMI*163110./59281265
sf_t_s = LUMI*1440/134808
sf_t_t = LUMI*22650/1929272
sf_t_dr = LUMI*7870/319742
sf_t_ds = LUMI*7870/783022
sf_tbar_s = LUMI*3190/250958
sf_tbar_t = LUMI*41920/3760239
sf_tbar_dr = LUMI*7870/804375
sf_tbar_ds = LUMI*7870/771637

scaleFactors = [
                sf_WW,sf_WZ,sf_ZZ,
                sf_Wjets,sf_Wjets,sf_Wjets,sf_Wjets,sf_Wjets,sf_Wjets,sf_Wjets,sf_Wjets,
                sf_Wjets_bMG,sf_Wjets_bMG,sf_Wjets_bMG,sf_Wjets_bMG,
                sf_Wjets_bHW,sf_Wjets_bHW,sf_Wjets_bHW,sf_Wjets_bHW,sf_Wjets_bHW,sf_Wjets_bHW,sf_Wjets_bHW,sf_Wjets_bHW,sf_Wjets_bHW,
                sf_Zjets,sf_Zjets,sf_Zjets,sf_Zjets,sf_Zjets,sf_Zjets,sf_Zjets,sf_Zjets,
                sf_Zjets_bMG,sf_Zjets_bMG,sf_Zjets_bMG,sf_Zjets_bMG,sf_Zjets_bMG,
                sf_Zjets_bHW,sf_Zjets_bHW,sf_Zjets_bHW,sf_Zjets_bHW,
                sf_ttbar,sf_ttbar,sf_ttbar,sf_ttbar,sf_ttbar,sf_ttbar,sf_ttbar,sf_ttbar,sf_ttbar,sf_ttbar,sf_ttbar,sf_ttbar,
                sf_t_s,sf_t_t,sf_t_dr,sf_t_ds,
                sf_tbar_s,sf_tbar_t,sf_tbar_dr,sf_tbar_ds,
                #
                1,1,1,1,1,1,1,1,1,1,1,
                1,1,1,1,1,1,1,1,1,1,1,
                1,1,1,1,1,1,1,1,1,1,1,1,1                
                ]

dummylist = [0,0,0]
print "ndummy: ",len(dummylist)
print "number of entries (dirnames): ",len(dataset)
print "number of entries (onames): ",len(onames)
print "number of entries (hnames): ",len(hnames)
print "number of entries (isData): ",len(isData)
print "number of entries (scaleFactors): ",len(scaleFactors)
#for x in range(len(dataset)):
#    print hnames[x]," at index: ",x," with SF: ", scaleFactors[x]
#    os.system("ls -lrt " + dataset[x] + "| wc -l")
    


############################################################
## R U N N I N G   A N A L Y S I S
import processNtuples

if options.runAnalysis and options.runOnFile == -1:
    for i in range(len(dataset)):
        processNtuples.processNtuples( dataset[i], onames[i], isData[i] )

if options.runAnalysis and options.runOnFile >= 0:
    curint = options.runOnFile
#    if not os.path.isfile(onames[curint]):    
#        processNtuples.processNtuples( dataset[curint], onames[curint], isData[curint] )
#    else:   
#        print "file already exists!"
    processNtuples.processNtuples( dataset[curint], onames[curint], isData[curint] )
############################################################
## B U I L D   H I S T O G R A M S

import buildHistos
if options.makeHistos and options.runOnFile == -1:
    for i in range(len(dataset)):
        # build histos for all MC
        mc_onames = []
        data_onames = []
        mc_isData = []
        data_isData = []
        mc_SF = []
        data_SF = []
        for x in range(len(isData)):
            if isData[x] == 0:
                print "there"+str(isData[x])
                mc_onames.append( onames[x] )
                mc_isData.append( isData[x] )
                mc_SF.append( scaleFactors[x] )
            else:
                print "here"+str(isData[x])
                data_onames.append( onames[x] )
                data_isData.append( isData[x] )
                data_SF.append( scaleFactors[x] )
    
        # build hiostos for all mc
        buildHistos.buildHistos( mc_onames, hnamesAll, mc_isData, mc_SF, chan )
        # build hiostos for all data
        print "build data histos"
        buildHistos.buildHistos( data_onames, hnamesDat, data_isData, data_SF, chan )

if options.makeHistos and options.runOnFile >= 0:
    i = options.runOnFile
    #print "current file: "+onames[i]
    #print scaleFactors    
    #print scaleFactors[i]
    curoname_l = []
    curoname_l.append( onames[i] )
    curhname_l = []
    curhname_l.append( hnames[i] )
    curisData_l = []
    curisData_l.append( isData[i] )
    curSF_l = []
    curSF_l.append( scaleFactors[i] )
    buildHistos.buildHistos( curoname_l, curhname_l[0], curisData_l, curSF_l, chan )
    

############################################################
## P L O T T E R

if options.writePlots:

    import plotter
    import ROOT
    gROOT.ProcessLine(".L tdrstyle.C")
    from ROOT import setTDRStyle
    ROOT.setTDRStyle()
    
    #gROOT.ProcessLine('.L myutils.C++')

    #### -------------------------------------------------------
    # do the hadd-ing here....
    # but have to be careful to mix the right samples together with W+jets and Z+jets 
    # 2 different samples of "boosted" with W/Z herwig or madgraph
    
    ## MC 
    ## -------------------------
    ## Diboson
    haddCmd_DiBoson = "hadd -f "+odir+"/hDiboson_all_ch"+str(chan)+".root"
    for x in range(len(hnames)):
        if hnames[x].find("WW") >= 0 or hnames[x].find("WZ") >= 0 or hnames[x].find("ZZ") >= 0: 
            haddCmd_DiBoson += (" "+hnames[x]+"_ch"+str(chan)+".root")
    ## Wjets, Inclusive
    haddCmd_Wjets_WJI = "hadd -f "+odir+"/hWjetsInclusive_all_ch"+str(chan)+".root"
    for x in range(len(hnames)):
        if hnames[x].find("WJetsInclusive") >= 0: 
            haddCmd_Wjets_WJI += (" "+hnames[x]+"_ch"+str(chan)+".root")
    ## Wjets, boosted Madgraph
    haddCmd_Wjets_bMG = "hadd -f "+odir+"/hWjets_boostedMadGraph_all_ch"+str(chan)+".root"
    for x in range(len(hnames)):
        if hnames[x].find("WJets_boostedMadGraph") >= 0: 
            haddCmd_Wjets_bMG += (" "+hnames[x]+"_ch"+str(chan)+".root")
    ## Wjets, boosted Herwig
    haddCmd_Wjets_bHW = "hadd -f "+odir+"/hWjets_boostedHerwig_all_ch"+str(chan)+".root"
    for x in range(len(hnames)):
        if hnames[x].find("WJets_boostedHerwig") >= 0: 
            haddCmd_Wjets_bHW += (" "+hnames[x]+"_ch"+str(chan)+".root")
    
    ## Zjets, Inclusive
    haddCmd_Zjets_WJI = "hadd -f "+odir+"/hZjetsInclusive_all_ch"+str(chan)+".root"
    for x in range(len(hnames)):
        if hnames[x].find("ZJetsInclusive") >= 0: 
            haddCmd_Zjets_WJI += (" "+hnames[x]+"_ch"+str(chan)+".root")
    ## Zjets, boosted Madgraph
    haddCmd_Zjets_bMG = "hadd -f "+odir+"/hZjets_boostedMadGraph_all_ch"+str(chan)+".root"
    for x in range(len(hnames)):
        if hnames[x].find("ZJets_boostedMadGraph") >= 0: 
            haddCmd_Zjets_bMG += (" "+hnames[x]+"_ch"+str(chan)+".root")
    ## Zjets, boosted Herwig
    haddCmd_Zjets_bHW = "hadd -f "+odir+"/hZjets_boostedHerwig_all_ch"+str(chan)+".root"
    for x in range(len(hnames)):
        if hnames[x].find("ZJets_boostedHerwig") >= 0: 
            haddCmd_Zjets_bHW += (" "+hnames[x]+"_ch"+str(chan)+".root")

    ## ttbar
    haddCmd_ttbar = "hadd -f "+odir+"/hTTbar_all_ch"+str(chan)+".root"
    for x in range(len(hnames)):
        if hnames[x].find("TTbar") >= 0: 
            haddCmd_ttbar += (" "+hnames[x]+"_ch"+str(chan)+".root")

    ## single T
    haddCmd_singleT = "hadd -f "+odir+"/hsingleT_all_ch"+str(chan)+".root"
    for x in range(len(hnames)):
        if hnames[x].find("singleT") >= 0: 
            haddCmd_singleT += (" "+hnames[x]+"_ch"+str(chan)+".root")

    ## Data 
    ## -------------------------
    ## SingleEl/EleHad
    haddCmd_SingleEl = "hadd -f "+odir+"/hdat_SingleEl_all_ch"+str(chan)+".root"
    for x in range(len(hnames)):
        if hnames[x].find("SingleEl") >= 0 or hnames[x].find("EleHad") >= 0 : 
            haddCmd_SingleEl += (" "+hnames[x]+"_ch"+str(chan)+".root")
    ## DoubleEl
    haddCmd_DoubleEl = "hadd -f "+odir+"/hdat_DoubleEl_all_ch"+str(chan)+".root"
    for x in range(len(hnames)):
        if hnames[x].find("DoubleEl") >= 0: 
            haddCmd_DoubleEl += (" "+hnames[x]+"_ch"+str(chan)+".root")
    ## SingleMu
    haddCmd_SingleMu = "hadd -f "+odir+"/hdat_SingleMu_all_ch"+str(chan)+".root"
    for x in range(len(hnames)):
        if hnames[x].find("SingleMu") >= 0: 
            haddCmd_SingleMu += (" "+hnames[x]+"_ch"+str(chan)+".root")

    if options.addFiles:
        
        print haddCmd_DiBoson
        os.system( haddCmd_DiBoson )
        print haddCmd_Wjets_bMG
        os.system( haddCmd_Wjets_WJI )
        os.system( haddCmd_Wjets_bMG )
        os.system( haddCmd_Wjets_bHW )
        os.system( haddCmd_Zjets_WJI )
        os.system( haddCmd_Zjets_bMG )
        os.system( haddCmd_Zjets_bHW )
        os.system( haddCmd_ttbar )
        os.system( haddCmd_singleT )

        os.system( haddCmd_SingleEl )
        os.system( haddCmd_DoubleEl )
        os.system( haddCmd_SingleMu )

        os.system( "hadd -f "+odir+"/hMC_all_Inclusive_ch"+str(chan)+".root "+odir+"/hDiboson_all_ch"+str(chan)+".root "+odir+"/hWjetsInclusive_all_ch"+str(chan)+".root "+odir+"/hZjetsInclusive_all_ch"+str(chan)+".root "+odir+"/hTTbar_all_ch"+str(chan)+".root "+odir+"/hsingleT_all_ch"+str(chan)+".root" )
        os.system( "hadd -f "+odir+"/hMC_all_MadGraph_ch"+str(chan)+".root "+odir+"/hDiboson_all_ch"+str(chan)+".root "+odir+"/hWjets_boostedMadGraph_all_ch"+str(chan)+".root "+odir+"/hZjets_boostedMadGraph_all_ch"+str(chan)+".root "+odir+"/hTTbar_all_ch"+str(chan)+".root "+odir+"/hsingleT_all_ch"+str(chan)+".root" )
        os.system( "hadd -f "+odir+"/hMC_all_Herwig_ch"+str(chan)+".root "+odir+"/hDiboson_all_ch"+str(chan)+".root "+odir+"/hWjets_boostedHerwig_all_ch"+str(chan)+".root "+odir+"/hZjets_boostedHerwig_all_ch"+str(chan)+".root "+odir+"/hTTbar_all_ch"+str(chan)+".root "+odir+"/hsingleT_all_ch"+str(chan)+".root" )             

#    #### -------------------------------------------------------
    stacklist_Inclusive = []
    stacklist_Inclusive.append(odir+"/hDiboson_all_ch"+str(chan)+".root")
    stacklist_Inclusive.append(odir+"/hWjetsInclusive_all_ch"+str(chan)+".root")
    stacklist_Inclusive.append(odir+"/hZjetsInclusive_all_ch"+str(chan)+".root")
    stacklist_Inclusive.append(odir+"/hTTbar_all_ch"+str(chan)+".root")
    stacklist_Inclusive.append(odir+"/hsingleT_all_ch"+str(chan)+".root")

    stacklist_MadGraph = []
    stacklist_MadGraph.append(odir+"/hDiboson_all_ch"+str(chan)+".root")
    stacklist_MadGraph.append(odir+"/hWjets_boostedMadGraph_all_ch"+str(chan)+".root")
    stacklist_MadGraph.append(odir+"/hZjets_boostedMadGraph_all_ch"+str(chan)+".root")
    stacklist_MadGraph.append(odir+"/hTTbar_all_ch"+str(chan)+".root")
    stacklist_MadGraph.append(odir+"/hsingleT_all_ch"+str(chan)+".root")

    stacklist_Herwig = []
    stacklist_Herwig.append(odir+"/hDiboson_all_ch"+str(chan)+".root")
    stacklist_Herwig.append(odir+"/hWjets_boostedHerwig_all_ch"+str(chan)+".root")
    stacklist_Herwig.append(odir+"/hZjets_boostedHerwig_all_ch"+str(chan)+".root")
    stacklist_Herwig.append(odir+"/hTTbar_all_ch"+str(chan)+".root")
    stacklist_Herwig.append(odir+"/hsingleT_all_ch"+str(chan)+".root")

    PD = ""
    if chan == 1: PD = "SingleEl"
    elif chan == 2 or chan == 4: PD = "SingleMu"
    elif chan == 3: PD = "DoubleEl"
    else: print "-------------> Not a valid channel!"

    ####### for Wmunu and Zmumu
###    plotter.plotterStack( stacklist_MadGraph, odir+"/hMC_all_MadGraph_ch"+str(chan)+".root", odir+"/hdat_"+PD+"_all_ch"+str(chan)+".root", "figstest_ch"+str(chan)+"_mg", chan)
#    plotter.plotterStack( stacklist_MadGraph, odir+"/hMC_all_MadGraph_ch"+str(chan)+".root", "ntuples_v10_clean/hSingleEl_2011B_promptV1_3_ch1.root", "figstest_ch"+str(chan)+"_mg", chan)
    ###    plotter.plotterStack( stacklist_Inclusive, odir+"/hMC_all_Inclusive_ch"+str(chan)+".root", odir+"/hdat_"+PD+"_all_ch"+str(chan)+".root", "figstest_ch"+str(chan)+"_mg", chan)

    #plotter.plotterStack( stacklist_Inclusive, odir+"/hMC_all_Inclusive_ch"+str(chan)+".root", odir+"/h"+PD+"_2011A_May10_1_ch"+str(chan)+".root", "figstest_ch"+str(chan)+"_mg", chan)
    #plotter.plotterStack( stacklist_Inclusive, odir+"/hMC_all_Inclusive_ch"+str(chan)+".root", odir+"/h"+PD+"_2011A_promptV6_2_ch"+str(chan)+".root", "figstest_ch"+str(chan)+"_mg", chan)
    #plotter.plotterStack( stacklist_Inclusive, odir+"/hMC_all_Inclusive_ch"+str(chan)+".root", odir+"/h"+PD+"_2011B_promptV1_1_ch"+str(chan)+".root", "figstest_ch"+str(chan)+"_mg", chan)

#    plotter.plotterStack( stacklist_MadGraph, odir+"/hMC_all_MadGraph_ch"+str(chan)+".root", odir+"/hdat_"+PD+"_all_ch"+str(chan)+".root", "figstest_ch"+str(chan)+"_mg", chan)
#    plotter.plotter1D( odir+"/hMC_all_MadGraph_ch"+str(chan)+".root", odir+"/hdat_"+PD+"_all_ch"+str(chan)+".root", "figstest_ch"+str(chan)+"_mg" )
#    plotter.plotter1D_MCcomp( odir+"/hMC_all_MadGraph_ch"+str(chan)+".root", odir+"/hMC_all_Herwig_ch"+str(chan)+".root", odir+"/hdat_"+PD+"_all_ch"+str(chan)+".root", "figstest_ch"+str(chan)+"_mg" )
#    plotter.plotter2D( odir+"/hMC_all_MadGraph_ch"+str(chan)+".root", odir+"/hdat_"+PD+"_all_ch"+str(chan)+".root", "figstest_ch"+str(chan)+"_mg" )
##    plotter.plotter_unfolding( odir+"/hMC_all_MadGraph_ch"+str(chan)+".root", odir+"/hdat_"+PD+"_all_ch"+str(chan)+".root", "figstest_ch"+str(chan)+"_mg" )
    plotter.plotter2D_mass( odir+"/hMC_all_MadGraph_ch"+str(chan)+".root", odir+"/hdat_"+PD+"_all_ch"+str(chan)+".root", "figstest_ch"+str(chan)+"_mg" )
#    plotter.plotter_unfolding_MCcomp( odir+"/hMC_all_MadGraph_ch"+str(chan)+".root", odir+"/hMC_all_Herwig_ch"+str(chan)+".root", odir+"/hdat_"+PD+"_all_ch"+str(chan)+".root", "figstest_ch"+str(chan)+"_mg" )

#    if chan==1 or chan==2: plotter.plotterStack_taggers( stacklist_MadGraph, odir+"/hMC_all_MadGraph_ch"+str(chan)+".root", odir+"/hdat_"+PD+"_all_ch"+str(chan)+".root", "figstest_ch"+str(chan)+"_mg", chan)
    if chan==1 or chan==2: plotter.plotter2D_V3( odir+"/hWjets_boostedMadGraph_all_ch"+str(chan)+".root", odir+"/hdat_"+PD+"_all_ch"+str(chan)+".root", "figstest_ch"+str(chan)+"_mg" )
#    if chan==3 or chan==4: plotter.plotter2D_V3( odir+"/hZjets_boostedMadGraph_all_ch"+str(chan)+".root", odir+"/hdat_"+PD+"_all_ch"+str(chan)+".root", "figstest_ch"+str(chan)+"_mg" )
#    if chan==1 or chan==2: plotter.plotter_unfolding_MCcomp_V3( odir+"/hWjets_boostedMadGraph_all_ch"+str(chan)+".root", odir+"/hMC_all_MadGraph_ch"+str(chan)+".root", odir+"/hMC_all_Herwig_ch"+str(chan)+".root", odir+"/hdat_"+PD+"_all_ch"+str(chan)+".root", "figstest_ch"+str(chan)+"_mg" )
#    if chan==3 or chan==4: plotter.plotter_unfolding_MCcomp_V3( odir+"/hZjets_boostedMadGraph_all_ch"+str(chan)+".root", odir+"/hMC_all_MadGraph_ch"+str(chan)+".root", odir+"/hMC_all_Herwig_ch"+str(chan)+".root", odir+"/hdat_"+PD+"_all_ch"+str(chan)+".root", "figstest_ch"+str(chan)+"_mg" )

#    plotter.plotter1D_MCcomp( odir+"/hMC_all_MadGraph_ch"+str(chan)+".root", odir+"/hMC_all_Herwig_ch"+str(chan)+".root", odir+"/hdat_"+PD+"_all_ch"+str(chan)+".root", "figstest_ch"+str(chan)+"_mg" )
#    plotter.plotter2D( odir+"/hMC_all_MadGraph_ch"+str(chan)+".root", odir+"/hdat_"+PD+"_all_ch"+str(chan)+".root", "figstest_ch"+str(chan)+"_mg" )
#    plotter.plotter2D_mass( odir+"/hMC_all_MadGraph_ch"+str(chan)+".root", odir+"/hdat_"+PD+"_all_ch"+str(chan)+".root", "figstest_ch"+str(chan)+"_mg" )
#    plotter.plotter_unfolding( odir+"/hMC_all_MadGraph_ch"+str(chan)+".root", odir+"/hdat_"+PD+"_all_ch"+str(chan)+".root", "figstest_ch"+str(chan)+"_mg" )
    
#    plotter.plotterStack( stacklist_Herwig, odir+"/hMC_all_Herwig_ch"+str(chan)+".root", odir+"/hdat_"+PD+"_all_ch"+str(chan)+".root", "figstest_ch"+str(chan)+"_hw", chan)
#    plotter.plotter1D( odir+"/hMC_all_Herwig_ch"+str(chan)+".root", odir+"/hdat_"+PD+"_all_ch"+str(chan)+".root", "figstest_ch"+str(chan)+"_hw" )
#    plotter.plotter2D( odir+"/hMC_all_Herwig_ch"+str(chan)+".root", odir+"/hdat_"+PD+"_all_ch"+str(chan)+".root", "figstest_ch"+str(chan)+"_hw" )
#    plotter.plotter2D_mass( odir+"/hMC_all_Herwig_ch"+str(chan)+".root", odir+"/hdat_"+PD+"_all_ch"+str(chan)+".root", "figstest_ch"+str(chan)+"_hw" )


