#! /usr/bin/env python
import os
import glob
import math
import array

from ROOT import gROOT, gStyle, gSystem, TLatex
import subprocess
from subprocess import Popen

from sampleWrapperClass import *
from trainingClass import *
from BoostedWSamples import * 

#from helperUtils import *

############################################################
############################################
#            Job steering                  #
############################################
parser = OptionParser()

parser.add_option('-b', action='store_true', dest='noX', default=False,
                  help='no X11 windows')

parser.add_option('--createTrees', action='store_true', dest='createTrainingTrees', default=False,
                  help='creates Training Trees')
parser.add_option('--makeControlPlots', action='store_true', dest='makeControlPlots', default=False,
                  help='makeControlPlots')
parser.add_option('--makeSignalRegionControlPlots', action='store_true', dest='makeSignalRegionControlPlots', default=False,
                  help='makeSignalRegionControlPlots')
parser.add_option('--makeTTBarControlPlots', action='store_true', dest='makeTTBarControlPlots', default=False,
                  help='makeTTBarControlPlots')
parser.add_option('--doTraining', action='store_true', dest='doTraining', default=False,
                  help='does training')
parser.add_option('--makeFinalTree', action='store_true', dest='makeFinalTree', default=False,
                  help='make Final Tree')


(options, args) = parser.parse_args()
############################################################
############################################################
############################################################

if __name__ == '__main__':

    
    print "Welcome to the boosted analysis..."
    
    # ---------------------------------------------------
    # check if directories exists
    if not os.path.isdir("trainingtrees"): os.system("mkdir trainingtrees");
    if not os.path.isdir("classifier"): os.system("mkdir classifier");    

    # ---------------------------------------------------
    # define samples, this creates some trees in the "trainingtrees" directory
    isData = True;
    notData = False;
    LUMI = 9.9
    sourcefiledirectory = "/eos/uscms/store/user/lnujj/HCP2012/ReducedTrees/"
    treename = "WJet"
    lumifile = "MCScaleFactors.txt"

    boostedWSamples = Samples()
    boostedWSamples.SetFilePath(sourcefiledirectory)
    boostedWSamples.SetTreeName(treename)
    boostedWSamples.SetFileNames()
    boostedWSamples.SetLumi(LUMI)
    
    singlemu600Sample = sampleWrapperClass("data",boostedWSamples.GetFileNames()["data"],LUMI,LUMI,boostedWSamples.GetTreeName(),isData)
    
    #sigSCF = 200.;
    #ggH600SampleXS = 8.55627E1*sigSCF;
    #ggH600Sample_EffLumi = 197170/ggH600SampleXS;
    ggH600Sample = sampleWrapperClass("ggH600",boostedWSamples.GetFileNames()["ggH600"],1.0/(boostedWSamples.GetLumiScaleFactor(lumifile,"ggH600")),LUMI,boostedWSamples.GetTreeName(),notData)

    #boostedWXS = 1.3*228.9E3;
    #WJetsSample_EffLumi = 8955318/boostedWXS;
    WJetsSample = sampleWrapperClass("WJets",boostedWSamples.GetFileNames()["WJets"],1.0/(boostedWSamples.GetLumiScaleFactor(lumifile,"WJets")),LUMI,boostedWSamples.GetTreeName(),notData)
    
    #TTbarSample_EffLumi = 6893735/225197.;
    TTbarSample = sampleWrapperClass("TTbar",boostedWSamples.GetFileNames()["TTbar"],1.0/(boostedWSamples.GetLumiScaleFactor(lumifile,"TTbar")),LUMI,boostedWSamples.GetTreeName(),notData);

    #WWSample_EffLumi = 9450414/33.61E3;
    WWSample = sampleWrapperClass("WW",boostedWSamples.GetFileNames()["WW"],1.0/(boostedWSamples.GetLumiScaleFactor(lumifile,"WW")),LUMI,boostedWSamples.GetTreeName(),notData);
   # WZSample_EffLumi = 10000267/12.63E3;
    WZSample = sampleWrapperClass("WZ",boostedWSamples.GetFileNames()["WZ"],1.0/(boostedWSamples.GetLumiScaleFactor(lumifile,"WZ")),LUMI,boostedWSamples.GetTreeName(),notData);
    #ZZSample_EffLumi = 9702850/5.196E3;
    ZZSample = sampleWrapperClass("ZZ",boostedWSamples.GetFileNames()["ZZ"],1.0/(boostedWSamples.GetLumiScaleFactor(lumifile,"ZZ")),LUMI,boostedWSamples.GetTreeName(),notData);

    #mcbackgrounds = [WJetsSample,WWSample,WZSample,ZZSample,TTbarSample]
    #myPlotter = plotterClass( ggH600Sample, mcbackgrounds, singlemu600Sample );

    if options.createTrainingTrees:
        
        # ---------------------------------------------------
        # create training tree
        ggH600Sample.createTrainingTree();        
        singlemu600Sample.createTrainingTree();
        ggH600Sample.createTrainingTree();
        WJetsSample.createTrainingTree();
        TTbarSample.createTrainingTree();
        WWSample.createTrainingTree();
        WZSample.createTrainingTree();
        ZZSample.createTrainingTree();

    #mcbackgrounds = [WJetsSample,WWSample,WZSample,ZZSample,TTbarSample]
    #myPlotter = plotterClass( ggH600Sample, mcbackgrounds, singlemu600Sample );    
    
    if options.makeControlPlots:
                
        # ---------------------------------------------------
        # make control plots based on the same cuts as the training trees
        if not os.path.isdir("controlPlots"): os.system("mkdir controlPlots");
        #myPlotter.makeControlPlots("controlPlots","nocuts");
        print "Please Check the Cuts used on the BoostedWControlPlots.py is reasonable"
        Cuts = "W_pt > 180 && GroomedJet_CA8_pt_pr[0] > 180 && ggdboostedWevt == 1 && event_metMVA_met > 50"
        print "Cuts we apply: " + Cuts
        if options.noX:
           p = subprocess.Popen(["python","BoostedWControlPlots.py","-b","-f","%s"%sourcefiledirectory,"-t","%s"%treename,"-l","%f"%LUMI,"-s","%s"%lumifile,"-c","%s"%Cuts])
           if(p.wait() != None): raw_input( 'Press ENTER to continue\n ' )
        else:
           p = subprocess.Popen(["python","BoostedWControlPlots.py","-f","%s"%sourcefiledirectory,"-t","%s"%treename,"-l","%f"%LUMI,"-s","%s"%lumifile,"-c","%s"%Cuts])
           if(p.wait() != None): raw_input( 'Press ENTER to continue\n ' )
    
    if options.makeTTBarControlPlots:        
        
        # ---------------------------------------------------
        # make control plots based on the same cuts as the training trees
        if not os.path.isdir("controlPlots_ttbar"): os.system("mkdir controlPlots_ttbar");
        #myPlotter.makeControlPlots("controlPlots_ttbar","ttbar");
        print "Please Check the Cuts used on the BoostedWTopControlPlots.py is reasonable"
        Cuts = "W_pt > 180 && GroomedJet_CA8_pt_pr[0] > 180 && ggdboostedWevt == 1 && event_metMVA_met > 50 && GroomedJet_numberbjets >= 1"
        print "Cuts we apply: " + Cuts
        print "We don't put the cuts on the signal and try to compare the W jet performance with TTbar and Data!!!!"
        print "Make Sure the numberbjets cut is the last cut in the cut sequence"
        if options.noX:
           p = subprocess.Popen(["python","BoostedWTopControlPlots.py","-b","-f","%s"%sourcefiledirectory,"-t","%s"%treename,"-l","%f"%LUMI,"-s","%s"%lumifile,"-c","%s"%Cuts])
           if(p.wait() != None): raw_input( 'Press ENTER to continue\n ' )
        else:
           p = subprocess.Popen(["python","BoostedWTopControlPlots.py","-f","%s"%sourcefiledirectory,"-t","%s"%treename,"-l","%f"%LUMI,"-s","%s"%lumifile,"-c","%s"%Cuts])
           if(p.wait() != None): raw_input( 'Press ENTER to continue\n ' )

    if options.makeSignalRegionControlPlots:        
        
        # ---------------------------------------------------
        # make control plots based on the same cuts as the training trees
        if not os.path.isdir("controlPlots_signalregion"): os.system("mkdir controlPlots_signalregion");
        #myPlotter.makeControlPlots("controlPlots_signalregion","signalregion");
        print "Please Check the Cuts used on the BoostedWWWControlPlots.py is reasonable"
        Cuts = ""
        print "Cuts we apply: " + Cuts
        if options.noX:
           p = subprocess.Popen(["python","BoostedWWWControlPlots.py","-b","-f","%s"%sourcefiledirectory,"-t","%s"%treename,"-l","%f"%LUMI,"-s","%s"%lumifile,"-c","%s"%Cuts])
           if(p.wait() != None): raw_input( 'Press ENTER to continue\n ' )
        else:
           p = subprocess.Popen(["python","BoostedWWWControlPlots.py","-f","%s"%sourcefiledirectory,"-t","%s"%treename,"-l","%f"%LUMI,"-s","%s"%lumifile,"-c","%s"%Cuts])
           if(p.wait() != None): raw_input( 'Press ENTER to continue\n ' )

    # ---------------------------------------------------
    # do the training
    # get the training tree names
    signalTrainingTreeName = ggH600Sample.getTrainingTreeName();
    backgroundTrainingTreeNames = WJetsSample.getTrainingTreeName();

    # Trainings
    # --------- #1 -----------
    listOfTrainingVariables1 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1"];
    WWTraining1 = trainingClass( signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables1, "simple" );
    # --------- #2 -----------
#    listOfTrainingVariables2 = ["jet_grsens_tr","jet_grsens_ft","jet_massdrop_pr","jet_qjetvol","jet_tau2tau1","jet_rcore4","jet_rcore7","jet_planarflow04","jet_planarflow07"];
#    WWTraining2 = trainingClass( signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables2, "no subjets" );
    listOfTrainingVariables2 = ["jet_grsens_tr","jet_grsens_ft","jet_massdrop_pr","jet_qjetvol","jet_tau2tau1","jet_sjdr","jet_rcore4","jet_rcore7","jet_planarflow04","jet_planarflow07"];
    WWTraining2 = trainingClass( signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables2, "optimal" );
#    # --------- #3 -----------
#    listOfTrainingVariables3 = ["jet_grsens_tr","jet_grsens_ft","jet_massdrop_pr","jet_qjetvol","jet_tau2tau1","jet_rcore7","jet_planarflow07"];
#    WWTraining3 = trainingClass( signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables3, "optimal2" );
#    # --------- #4 -----------
#    listOfTrainingVariables4 = ["jet_grsens_tr","jet_grsens_ft","jet_massdrop_pr","jet_qjetvol","jet_tau2tau1","jet_pt1frac","jet_sjdr","jet_jetconstituents","jet_rcore4","jet_rcore5","jet_rcore6","jet_rcore7","jet_planarflow04","jet_planarflow05","jet_planarflow06","jet_planarflow07"];
#    WWTraining4 = trainingClass( signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables4, "all" );

    if options.doTraining:        
        
        WWTraining1.doTraining( 200, 275 );
        WWTraining1.doTraining( 275, 500 );
        
        WWTraining2.doTraining( 200, 275 );
        WWTraining2.doTraining( 275, 500 );
        
#        WWTraining3.doTraining( 200, 275 );
#        WWTraining3.doTraining( 275, 500 );
#
#        WWTraining4.doTraining( 200, 275 );
#        WWTraining4.doTraining( 275, 500 );
        
        WWTraining1.plotTrainingResults( 200, 275 );
        WWTraining1.plotTrainingResults( 275, 500 );

        WWTraining2.plotTrainingResults( 200, 275 );
        WWTraining2.plotTrainingResults( 275, 500 );
                
#        WWTraining3.plotTrainingResults( 200, 275 );
#        WWTraining3.plotTrainingResults( 275, 500 );
#
#        WWTraining4.plotTrainingResults( 200, 275 );
#        WWTraining4.plotTrainingResults( 275, 500 );

    if options.makeFinalTree:

        # ---------------------------------------------------   
        # make the final trees
        print "making final trees"
        
        # get name from training class (if name is MassDrop, special case)
        # give it the same set of variables
        # give it samples
        rocs1 = WWTraining1.makeFinalPlotsInternal( 200, 275 );
        rocs2 = WWTraining2.makeFinalPlotsInternal( 200, 275 );
#        rocs3 = WWTraining3.makeFinalPlotsInternal( 200, 275 );
#        rocs4 = WWTraining4.makeFinalPlotsInternal( 200, 275 );

#        rocs1ex = WWTraining1.makeFinalPlots( 200, 275, 0. );
        rocs2ex = WWTraining2.makeFinalPlots( 200, 275, 0. );
#        rocs3ex = WWTraining3.makeFinalPlots( 200, 275, 0. );        
#        rocs4ex = WWTraining4.makeFinalPlots( 200, 275, 0. );
        
        canBdtRoc = ROOT.TCanvas("canBdtRoc","canBdtRoc",800,800);    
        canBdtRoc.cd();
        hrl = canBdtRoc.DrawFrame(0,0,1.0,1.0);
        hrl.GetXaxis().SetTitle("#epsilon_{sig}");
        hrl.GetYaxis().SetTitle("1 - #epsilon_{bkg}");
        canBdtRoc.SetGrid();
        rocs1[0].Draw();
        rocs1[1].SetLineColor(ROOT.kRed);
        rocs1[1].Draw();
        rocs2[0].SetLineColor(ROOT.kBlue);
        rocs2[0].Draw();
#        rocs3[0].SetLineColor(ROOT.kMagenta);
#        rocs3[0].Draw();
#        rocs4[0].SetLineColor(ROOT.kGreen+2);
#        rocs4[0].Draw();

#        rocs1[2].SetLineWidth(2);
#        rocs1[2].SetLineColor(ROOT.kBlack);
#        rocs1[2].Draw();
#        rocs2[2].SetLineWidth(2);
#        rocs2[2].SetLineColor(ROOT.kBlue);
#        rocs2[2].Draw();
#        rocs3[2].SetLineWidth(2);
#        rocs3[2].SetLineColor(ROOT.kMagenta);
#        rocs3[2].Draw();
#        rocs4[2].SetLineWidth(2);
#        rocs4[2].SetLineColor(ROOT.kGreen+2);
#        rocs4[2].Draw();
        
#        rocs4[2].SetLineColor(ROOT.kCyan+2);
#        rocs4[2].SetLineStyle(2);
#        rocs4[2].Draw();
        
        leg = ROOT.TLegend(0.25,0.2,0.55,0.5)
        leg.SetFillColor(0)
        leg.SetBorderSize(0)                
        leg.AddEntry( rocs1[0], "simple", 'l' );
        leg.AddEntry( rocs1[1], "mass drop only", 'l' ); 
        leg.AddEntry( rocs2[0], "optimal", 'l' );
#        leg.AddEntry( rocs3[0], "optimal2", 'l' ); 
#        leg.AddEntry( rocs4[0], "all", 'l' );         
#        leg.AddEntry( rocs4ex[0], "all ex", 'l' );         
        leg.Draw();
        
        canBdtRoc.SaveAs("finalPlot/testROC_compall.eps");
        canBdtRoc.SaveAs("finalPlot/testROC_compall.png");

        hs = rocs2ex[2];
        hs.SetLineColor(4);        
        hs.Scale(1./hs.Integral());                
        hb = rocs2ex[3];
        hb.SetLineColor(2);        
        hb.Scale(1./hb.Integral());                
        canMassPrBdtCut = ROOT.TCanvas("canMassPrBdtCut","canMassPrBdtCut",800,800);    
        hs.Draw("hist");
        hb.Draw("histsames");
        canMassPrBdtCut.SaveAs("finalPlot/testmasspr.eps");
        canMassPrBdtCut.SaveAs("finalPlot/testmasspr.png");



