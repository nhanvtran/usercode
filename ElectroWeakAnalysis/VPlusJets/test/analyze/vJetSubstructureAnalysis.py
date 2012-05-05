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

odir = ntuples_v5

dataset    = [
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_WWtoAnything/demo*.root",      
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_WJets/demo*.root",
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/ch_TTbar/demo*.root",
              "/eos/uscms/store/user/smpjs/kalanand/tlbsm_v10_FallV2/dat_ch_SingleEl_2011A_promptV4/demo*.root",
              ]
onames     = [
              odir+"/WW.root",
              odir+"/WJets.root",
              odir+"/TTbar.root",
              odir+"/dat_SingleEl_2011A_promptV4.root"
             ] 

hnames     = [
              odir+"/hWW.root",
              odir+"/hWJets.root",
              odir+"/hTTbar.root",
              odir+"/h_SingleEl_2011A_promptV4.root"  
              ] 
hnamesAll  =  odir+"/hAllMC.root"
hnamesDat  =  odir+"/hDat.root"

channels   = [
              "ch_WWtoAnything",
              "ch_WJets",
              "ch_TTbar",
              "dat_ch_SingleEl_2011A_promptV4"
              ]
isData = [0,0,0,1]

LUMI = 1.
scaleFactors = [
                LUMI*43000./4223922.,
                LUMI*31300000./80978873,
                #LUMI*163110./3683595  -- old ttbar
                LUMI*163110./59281265,
                1.
                ]

############################################################
## R U N N I N G   A N A L Y S I S
import processNtuples

if options.runAnalysis and options.runOnFile == -1:
    for i in range(len(channels)):
        processNtuples.processNtuples( dataset[i], onames[i], isData[i] )

if options.runAnalysis and options.runOnFile >= 0:
    curint = options.runOnFile
    processNtuples.processNtuples( dataset[curint], onames[curint], isData[curint] )


############################################################
## B U I L D   H I S T O G R A M S

import buildHistos
if options.makeHistos:
    
if options.makeHistos and options.runOnFile == -1:
    for i in range(len(channels)):
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
        buildHistos.buildHistos( mc_onames, hnamesAll, mc_isData, mc_SF )
        # build hiostos for all data
        print "build data histos"
        buildHistos.buildHistos( data_onames, hnamesDat, data_isData, data_SF )

if options.makeHistos and options.runOnFile >= 0:
    i = options.runOnFile
    curoname_l = []
    curoname_l.append( onames[i] )
    curhname_l = []
    curhname_l.append( hnames[i] )
    curisData_l = []
    curisData_l.append( isData[i] )
    curSF_l = []
    curSF_l.append( scaleFactors[i] )
    buildHistos.buildHistos( curoname_l, curhname_l[0], curisData_l, curSF_l )
    

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
    plotter.plotter( hnamesAll, hnamesDat, "figs" )
    

