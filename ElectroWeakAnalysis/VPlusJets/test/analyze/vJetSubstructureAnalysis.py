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

(options, args) = parser.parse_args()

# Input files to use. This is in "glob" format, so you can use wildcards.
# If you get a "cannot find file" type of error, be sure to use "\*" instead
# of "*" to make sure you don't confuse the shell. 
#parser.add_option('--files', metavar='F', type='string', action='store',
#                  dest='files',help='Input files')

(options, args) = parser.parse_args()

argv = []

odir = "ntuples_v6"

dataset    = [
              # ww sample
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_WWtoAnything/demo*.root",      
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_WZtoAnything/demo*.root",         
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_ZZtoAnything/demo*.root",      
              ## w + jets sample, split into 8
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_WJets/demo_1[0-4]*_*.root",
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_WJets/demo_1[5-9]*_*.root",
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_WJets/demo_2[0-4]*_*.root",
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_WJets/demo_2[5-9]*_*.root",
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_WJets/demo_3[0-9]*_*.root",
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_WJets/demo_[1-4][0-9]_*.root",   
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_WJets/demo_[5-9][0-9]_*.root",   
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_WJets/demo_[1-9]_*_*.root",
              ## ttbar sample -- this one is huge, split into 12
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_TTbar/demo_1[0-1][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_TTbar/demo_1[2-3][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_TTbar/demo_1[4-5][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_TTbar/demo_1[6-7][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_TTbar/demo_1[8-9][0-9]_*.root",              
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_TTbar/demo_2[0-2][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_TTbar/demo_2[3-4][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_TTbar/demo_[1-2][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_TTbar/demo_[3-4][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_TTbar/demo_[5-6][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_TTbar/demo_[7-9][0-9]_*.root",
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_TTbar/demo_[1-9]_*_*.root",
              ###################
              ## data, single el and elehad
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/dat_ch_SingleEl_2011A_promptV4/demo_[1-4]*.root",
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/dat_ch_SingleEl_2011A_promptV4/demo_[5-9]*.root",
              ## data, single mu  
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/dat_ch_SingleMu_2011A_promptV4/demo_[1-4]*.root",
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/dat_ch_SingleMu_2011A_promptV4/demo_[5-9]*.root"              
              ]
onames     = [
              odir+"/WW.root",
              odir+"/WZ.root",
              odir+"/ZZ.root",
              #
              odir+"/WJets_1.root",
              odir+"/WJets_2.root",
              odir+"/WJets_3.root",
              odir+"/WJets_4.root",
              odir+"/WJets_5.root",
              odir+"/WJets_6.root",
              odir+"/WJets_7.root",
              odir+"/WJets_8.root",
              #
              odir+"/TTbar_1.root",
              odir+"/TTbar_2.root",
              odir+"/TTbar_3.root",
              odir+"/TTbar_4.root",
              odir+"/TTbar_5.root",
              odir+"/TTbar_6.root",
              odir+"/TTbar_7.root",
              odir+"/TTbar_8.root",
              odir+"/TTbar_9.root",
              odir+"/TTbar_10.root",
              odir+"/TTbar_11.root",
              odir+"/TTbar_12.root",
              #
              odir+"/dat_SingleEl_2011A_promptV4_1.root",
              odir+"/dat_SingleEl_2011A_promptV4_2.root",             
              #
              odir+"/dat_SingleMu_2011A_promptV4_1.root",
              odir+"/dat_SingleMu_2011A_promptV4_2.root"              
             ] 

hnames     = [
              odir+"/hWW",
              odir+"/hWZ",
              odir+"/hZZ",
              
              odir+"/hWJets_1",
              odir+"/hWJets_2",
              odir+"/hWJets_3",
              odir+"/hWJets_4",
              odir+"/hWJets_5",
              odir+"/hWJets_6",
              odir+"/hWJets_7",
              odir+"/hWJets_8",

              odir+"/hTTbar_1",
              odir+"/hTTbar_2",
              odir+"/hTTbar_3",
              odir+"/hTTbar_4",
              odir+"/hTTbar_5",
              odir+"/hTTbar_6",
              odir+"/hTTbar_7",
              odir+"/hTTbar_8",
              odir+"/hTTbar_9",
              odir+"/hTTbar_10",
              odir+"/hTTbar_11",
              odir+"/hTTbar_12",

              odir+"/h_SingleEl_2011A_promptV4_1",  
              odir+"/h_SingleEl_2011A_promptV4_2",  

              odir+"/h_SingleMu_2011A_promptV4_1",  
              odir+"/h_SingleMu_2011A_promptV4_2"  

              ] 
hnamesAll  =  odir+"/hAllMC"
hnamesDat  =  odir+"/hDat"

isData = [
          0,0,0,
          0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,0,0,
          1,1,
          1,1
          ]

LUMI = 1.
sf_WW = LUMI*43000./4216917.
sf_WZ = LUMI*43000./4259651.
sf_ZZ = LUMI*43000./4173452.
sf_Wjets = LUMI*31300000./80978873
sf_ttbar = LUMI*163110./59281265
scaleFactors = [
                sf_WW,sf_WZ,sf_ZZ,
                sf_Wjets,sf_Wjets,sf_Wjets,sf_Wjets,sf_Wjets,sf_Wjets,sf_Wjets,sf_Wjets,
                sf_ttbar,sf_ttbar,sf_ttbar,sf_ttbar,sf_ttbar,sf_ttbar,sf_ttbar,sf_ttbar,sf_ttbar,sf_ttbar,sf_ttbar,sf_ttbar,
                1.,1.,
                1.,1.
                ]

############################################################
## R U N N I N G   A N A L Y S I S
import processNtuples

if options.runAnalysis and options.runOnFile == -1:
    for i in range(len(dataset)):
        processNtuples.processNtuples( dataset[i], onames[i], isData[i] )

if options.runAnalysis and options.runOnFile >= 0:
    curint = options.runOnFile
    processNtuples.processNtuples( dataset[curint], onames[curint], isData[curint] )


############################################################
## B U I L D   H I S T O G R A M S

import buildHistos
chan = options.channelToBuild

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
    
    # do the hadd-ing here....
    
    # run plotter
    #plotter.plotter( hnamesAll, hnamesDat, "figs" )
    #plotter.plotter1D( "ntuples_v5/hWW.root", "ntuples_v5/hWW.root", "figstest" )
    plotter.plotter2D( "ntuples_v5/hWW.root", "ntuples_v5/hWW.root", "figstest" )
