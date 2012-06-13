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
#### for plotting a channel
parser.add_option('-c', '--channel',
                  action='store', type='int', dest='channel',default=1)
(options, args) = parser.parse_args()



from PlotterClass import *
from PlotterSimple import *


if __name__ == '__main__':

    channel = options.channel;
    
    ## for non-single electrons
    idir="histos_v2_clean_testA/";    
    ## single electrons
#    idir="histos_v3_tight/";        
    
    odir="figs_120607/figs_ch"+str(channel)+"/";
#    odir="figs_Plotter/dummy/";
    myplotter = PlotterClass(odir, channel)

    PD = "";
    if channel == 1: PD = "SingleEl"
    if channel == 2 or channel == 4: PD = "SingleMu"
    if channel == 3: PD = "DoubleEl"
    
    # ------------------------------------
    # set up the input histograms
    myplotter.storeFile( idir+"hdat_"+PD+"_all_ch"+str(channel)+".root", "dataWenu", 0 )
    myplotter.storeFileStack( idir+"hdat_"+PD+"_all_ch"+str(channel)+".root", "dataWenu", 0 )

    myplotter.storeFile( idir+"hMC_all_MadGraph_ch"+str(channel)+".root", "allMC", 1 )
    myplotter.storeFileStack( idir+"hDiboson_all_ch"+str(channel)+".root", "Diboson", 1 )  
    myplotter.storeFileStack( idir+"hWjets_boostedMadGraph_all_ch"+str(channel)+".root", "WjetsMG", 1 )  
    myplotter.storeFileStack( idir+"hZjets_boostedMadGraph_all_ch"+str(channel)+".root", "ZjetsMG", 1 )  
    myplotter.storeFileStack( idir+"hTTbar_all_ch"+str(channel)+".root", "TTbar", 1 )  
    myplotter.storeFileStack( idir+"hsingleT_all_ch"+str(channel)+".root", "SingleTop", 1 )

    myplotter.storeFile( idir+"hMC_all_Herwig_ch"+str(channel)+".root", "allMC", 2 )
    myplotter.storeFileStack( idir+"hDiboson_all_ch"+str(channel)+".root", "Diboson", 2 )  
    myplotter.storeFileStack( idir+"hWjets_boostedHerwig_all_ch"+str(channel)+".root", "WjetsHW", 2 )  
    myplotter.storeFileStack( idir+"hZjets_boostedHerwig_all_ch"+str(channel)+".root", "ZjetsHW", 2 )  
    myplotter.storeFileStack( idir+"hTTbar_all_ch"+str(channel)+".root", "TTbar", 2 )  
    myplotter.storeFileStack( idir+"hsingleT_all_ch"+str(channel)+".root", "SingleTop", 2 )
    # ------------------------------------
    groomedfileV3 = ""
    if channel == 1 or channel == 2: groomedfileV3 = idir+"hWjets_boostedMadGraph_all_ch"+str(channel)+".root"
    if channel == 3 or channel == 4: groomedfileV3 = idir+"hZjets_boostedMadGraph_all_ch"+str(channel)+".root"
    
    myplotter.doStuff("fun")

    # -------------------------
    ## Default plots...
    # -------------------------

##    # kinetmatic distributions
#    myplotter.doKinematicsStacked("ak5");
#    myplotter.doKinematicsStacked("ak7");
#    myplotter.doKinematicsStacked("ca8");
#    myplotter.doKinematicsStacked("ca12mdft");
##
##    # detector-level distributions
#    myplotter.doJetMass("ak7")
#    myplotter.doJetMass("ak7ft")
#    myplotter.doJetMass("ak7tr")
#    myplotter.doJetMass("ak7pr")
#    myplotter.doJetMass("ca8pr")
#    myplotter.doJetMass("ca12mdft")
##
##    # Unfolded distributions
##    myplotter.doClosureTest()
#    myplotter.doJetMassUnfolded("ak7","NONE")
#    myplotter.doJetMassUnfolded("ak7ft",groomedfileV3)
#    myplotter.doJetMassUnfolded("ak7tr",groomedfileV3)
#    myplotter.doJetMassUnfolded("ak7pr",groomedfileV3)
#
#    for i in range(5):
#        myplotter.doJetMassUnfolded_BkgSubtraction("ak7",groomedfileV3,i)
#        myplotter.doJetMassUnfolded_BkgSubtraction("ak7ft",groomedfileV3,i)
#        myplotter.doJetMassUnfolded_BkgSubtraction("ak7tr",groomedfileV3,i)
#        myplotter.doJetMassUnfolded_BkgSubtraction("ak7pr",groomedfileV3,i)
#
##
#    # top- and W-tagged plots
#    if channel == 1 or channel == 2:
#        myplotter.doSimpleStack( "h_ca8pr_mass_Wtagged", "jet mass (ca8pr), W-tagged", "taggedW_ca8pr" )
#        myplotter.doSimpleStack( "h_ca8pr_massdrop", "mass drop, #mu", "tagged_ca8pr_massdrop" )
#        myplotter.doSimpleStack( "h_ca12ft_mass_Wtagged", "jet mass (ca12ft), W-tagged", "taggedW_ca12ft" )
#        myplotter.doSimpleStack( "h_ca12ft_mass_toptagged", "jet mass (ca12ft), top-tagged", "taggedTop_ca12ft" )
#
#    myplotter.doJetResponse( groomedfileV3, "ak7" )
#    myplotter.doJetMassRatio( groomedfileV3, "ak7" )
#
###    # ratio plots
#    jetResponseTypes = ["ak7","ak7ft","ak7tr","ak7pr"]
#    
#    jetMassProjection1 = ["ak7","ak7ft","ak7tr","ak7pr"]
#    jetMassProjection2 = ["ak5","ak7","ak8"]
#    myplotter.doJetMassProjection(jetMassProjection1,"set1")
#    myplotter.doJetMassProjection(jetMassProjection2,"set2")

    # -------------------------
    ## Quick Plots
    # -------------------------
    channel1 = 1;
    channel2 = 2;
    channel3 = 3;
    channel4 = 4;
    PD1 = "";
    if channel1 == 1: PD1 = "SingleEl"
    if channel1 == 2 or channel1 == 4: PD1 = "SingleMu"
    if channel1 == 3: PD1 = "DoubleEl"
    PD2 = "";
    if channel2 == 1: PD2 = "SingleEl"
    if channel2 == 2 or channel2 == 4: PD2 = "SingleMu"
    if channel2 == 3: PD2 = "DoubleEl"
    PD3 = "";
    if channel3 == 1: PD3 = "SingleEl"
    if channel3 == 2 or channel3 == 4: PD3 = "SingleMu"
    if channel3 == 3: PD3 = "DoubleEl"
    PD4 = "";
    if channel4 == 1: PD4 = "SingleEl"
    if channel4 == 2 or channel4 == 4: PD4 = "SingleMu"
    if channel4 == 3: PD4 = "DoubleEl"

    ## input is simply two files and a histogram name
    hn_j_m = ["ak7","ak7tr","ak7ft","ak7pr"]    
    
    simplePlotter_1v2_data = PlotterSimple( idir+"hdat_"+PD1+"_all_ch"+str(channel1)+".root", idir+"hdat_"+PD2+"_all_ch"+str(channel2)+".root", "simplePlots/test1v2" );
    simplePlotter_1v2_data.setLabels( "Wenu", "Wmunu" );
    simplePlotter_1v2_mc = PlotterSimple( idir+"hMC_all_MadGraph_ch"+str(channel1)+".root", idir+"hMC_all_MadGraph_ch"+str(channel2)+".root", "simplePlots/test1v2" );
    simplePlotter_1v2_mc.setLabels( "Wenu", "Wmunu" );

    simplePlotter_3v4_data = PlotterSimple( idir+"hdat_"+PD3+"_all_ch"+str(channel3)+".root", idir+"hdat_"+PD4+"_all_ch"+str(channel4)+".root", "simplePlots/test3v4" );
    simplePlotter_3v4_data.setLabels( "Zee", "Zmumu" );
    simplePlotter_3v4_mc = PlotterSimple( idir+"hMC_all_MadGraph_ch"+str(channel3)+".root", idir+"hMC_all_MadGraph_ch"+str(channel4)+".root", "simplePlots/test3v4" );
    simplePlotter_3v4_mc.setLabels( "Zee", "Zmumu" );

    for i in xrange(len(hn_j_m)):
        for j in range(5):
            simplePlotter_1v2_data.plotSingle( "h_"+hn_j_m[i]+"_mass_"+str(j)+"bin", "h_"+hn_j_m[i]+"_mass_"+str(j)+"bin_data" )
            simplePlotter_1v2_mc.plotSingle( "h_"+hn_j_m[i]+"_mass_"+str(j)+"bin", "h_"+hn_j_m[i]+"_mass_"+str(j)+"bin_mc" )    
            simplePlotter_3v4_data.plotSingle( "h_"+hn_j_m[i]+"_mass_"+str(j)+"bin", "h_"+hn_j_m[i]+"_mass_"+str(j)+"bin_data" )
            simplePlotter_3v4_mc.plotSingle( "h_"+hn_j_m[i]+"_mass_"+str(j)+"bin", "h_"+hn_j_m[i]+"_mass_"+str(j)+"bin_mc" )






