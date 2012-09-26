#! /usr/bin/env python
import os
import glob
import math
import array

from ROOT import gROOT, gStyle, gSystem, TLatex
import subprocess

from sampleWrapperClass import *
from trainingClass import *
from helperUtils import *

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
    LUMI = 9.9;
    
    singlemu600Sample = sampleWrapperClass("singleMu","/eos/uscms/store/user/lnujj/HCP2012/ReducedTrees/RD_WmunuJets_DataAll_GoldenJSON_9p9invfb.root",LUMI,LUMI, isData);
    
    sigSCF = 200.;
    ggH600SampleXS = 8.55627E1*sigSCF;
    ggH600Sample_EffLumi = 197170/ggH600SampleXS;
    ggH600Sample = sampleWrapperClass("ggH600","/eos/uscms/store/user/smpjs/weizou/HCP2012/RDtreesPUCMSSW532/RD_mu_HWWMH600_CMSSW532_private.root",ggH600Sample_EffLumi,LUMI,notData);

    boostedWXS = 1.3*228.9E3;
    WJetsSample_EffLumi = 8955318/boostedWXS;
    WJetsSample = sampleWrapperClass("WJets","/eos/uscms/store/user/lnujj/HCP2012/ReducedTrees/RD_mu_WpJPt100_CMSSW532.root",WJetsSample_EffLumi,LUMI,notData);
    
    TTbarSample_EffLumi = 6893735/225197.;
    TTbarSample = sampleWrapperClass("TTbar","/eos/uscms/store/user/lnujj/HCP2012/ReducedTrees/RD_mu_TTbar_CMSSW532.root",TTbarSample_EffLumi,LUMI,notData);

    WWSample_EffLumi = 9450414/33.61E3;
    WWSample = sampleWrapperClass("WW","/eos/uscms/store/user/lnujj/HCP2012/ReducedTrees/RD_mu_WW_CMSSW532.root",WWSample_EffLumi,LUMI,notData);
    WZSample_EffLumi = 10000267/12.63E3;
    WZSample = sampleWrapperClass("WZ","/eos/uscms/store/user/lnujj/HCP2012/ReducedTrees/RD_mu_WZ_CMSSW532.root",WZSample_EffLumi,LUMI,notData);
    ZZSample_EffLumi = 9702850/5.196E3;
    ZZSample = sampleWrapperClass("ZZ","/eos/uscms/store/user/lnujj/HCP2012/ReducedTrees/RD_mu_ZZ_CMSSW532.root",ZZSample_EffLumi,LUMI,notData);

    mcbackgrounds = [WJetsSample,WWSample,WZSample,ZZSample,TTbarSample]
    myPlotter = plotterClass( ggH600Sample, mcbackgrounds, singlemu600Sample );

    if options.createTrainingTrees:
        
        # ---------------------------------------------------
        # create training tree
        singlemu600Sample.createTrainingTree();
        ggH600Sample.createTrainingTree();
        WJetsSample.createTrainingTree();
        TTbarSample.createTrainingTree();
        WWSample.createTrainingTree();
        WZSample.createTrainingTree();
        ZZSample.createTrainingTree();

    if options.makeControlPlots:
                
        # ---------------------------------------------------
        # make control plots based on the same cuts as the training trees
        if not os.path.isdir("controlPlots"): os.system("mkdir controlPlots");
        myPlotter.makeControlPlots("controlPlots","nocuts");
    
    if options.makeTTBarControlPlots:        
        
        # ---------------------------------------------------
        # make control plots based on the same cuts as the training trees
        if not os.path.isdir("controlPlots_ttbar"): os.system("mkdir controlPlots_ttbar");
        myPlotter.makeControlPlots("controlPlots_ttbar","ttbar");

    if options.makeSignalRegionControlPlots:        
        
        # ---------------------------------------------------
        # make control plots based on the same cuts as the training trees
        if not os.path.isdir("controlPlots_signalregion"): os.system("mkdir controlPlots_signalregion");
        myPlotter.makeControlPlots("controlPlots_signalregion","signalregion");


    # ---------------------------------------------------
    # do the training
    # get the training tree names
    signalTrainingTreeName = ggH600Sample.getTrainingTreeName();
    backgroundTrainingTreeNames = WJetsSample.getTrainingTreeName();

    # Trainings
    # --------- #1 -----------
    listOfTrainingVariables1 = ["jet_pt1frac","jet_pt2frac","jet_massdrop_pr"];
    WWTraining1 = trainingClass( signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables1, "noCores" );
    # --------- #2 -----------
    listOfTrainingVariables2 = ["jet_grsens_tr","jet_grsens_ft","jet_massdrop_pr","jet_qjetvol","jet_tau2tau1","jet_pt1frac","jet_sjdr","jet_jetconstituents","jet_rcore4","jet_rcore5","jet_rcore6","jet_rcore7"];
    WWTraining2 = trainingClass( signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables2, "cores" );
    # --------- #3 -----------
    listOfTrainingVariables3 = ["jet_grsens_tr","jet_grsens_ft","jet_massdrop_pr","jet_qjetvol","jet_tau2tau1","jet_planarflow05","jet_planarflow07","jet_pt1frac","jet_sjdr"];
    WWTraining3 = trainingClass( signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables3, "planflow" );
    # --------- #4 -----------
    listOfTrainingVariables4 = ["jet_grsens_tr","jet_grsens_ft","jet_massdrop_pr","jet_qjetvol","jet_tau2tau1","jet_rcore5","jet_rcore7","jet_pt1frac","jet_pt2frac","jet_sjdr","jet_planarflow05","jet_jetconstituents"];
    WWTraining4 = trainingClass( signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables4, "optimal" );

    if options.doTraining:        
        
        WWTraining1.doTraining( 200, 275 );
        WWTraining1.doTraining( 275, 500 );

        WWTraining1.plotTrainingResults( 200, 275 );
        WWTraining1.plotTrainingResults( 275, 500 );

        
        WWTraining2.doTraining( 200, 275 );
        WWTraining2.doTraining( 275, 500 );
        
        WWTraining2.plotTrainingResults( 200, 275 );
        WWTraining2.plotTrainingResults( 275, 500 );
        
        WWTraining3.doTraining( 200, 275 );
        WWTraining3.doTraining( 275, 500 );
        
        WWTraining3.plotTrainingResults( 200, 275 );
        WWTraining3.plotTrainingResults( 275, 500 );

        WWTraining4.doTraining( 200, 275 );
        WWTraining4.doTraining( 275, 500 );

        WWTraining4.plotTrainingResults( 200, 275 );
        WWTraining4.plotTrainingResults( 275, 500 );

    if options.makeFinalTree:

        # ---------------------------------------------------   
        # make the final trees
        print "making final trees"
        
        # get name from training class (if name is MassDrop, special case)
        # give it the same set of variables
        # give it samples
        rocs1 = WWTraining1.makeFinalPlotsInternal( 200, 275 );
        rocs2 = WWTraining2.makeFinalPlotsInternal( 200, 275 );
        rocs3 = WWTraining3.makeFinalPlotsInternal( 200, 275 );
        rocs4 = WWTraining4.makeFinalPlotsInternal( 200, 275 );
        rocs4ex = WWTraining4.makeFinalPlots( 200, 275, 0. );
        
        canBdtRoc = ROOT.TCanvas("canBdtRoc","canBdtRoc",800,800);    
        canBdtRoc.cd();
        hrl = canBdtRoc.DrawFrame(0,0,1.0,1.0);
        hrl.GetXaxis().SetTitle("#epsilon_{sig}");
        hrl.GetYaxis().SetTitle("1 - #epsilon_{bkg}");
        canBdtRoc.SetGrid();
#        rocs1[0].Draw();
        rocs1[1].SetLineColor(ROOT.kRed);
        rocs1[1].Draw();
#        rocs2[0].SetLineColor(ROOT.kBlue);
#        rocs2[0].Draw();
#        rocs3[0].SetLineColor(ROOT.kMagenta);
#        rocs3[0].Draw();
        rocs4[0].SetLineColor(ROOT.kCyan+2);
        rocs4[0].Draw();
        rocs4ex[0].SetLineColor(ROOT.kRed+2);
        rocs4ex[0].Draw();
        
#        rocs4[2].SetLineColor(ROOT.kCyan+2);
#        rocs4[2].SetLineStyle(2);
#        rocs4[2].Draw();
        
        leg = ROOT.TLegend(0.25,0.2,0.55,0.5)
        leg.SetFillColor(0)
        leg.SetBorderSize(0)                
#        leg.AddEntry( rocs1[0], "noCores", 'l' );
        leg.AddEntry( rocs1[1], "mass drop only", 'l' ); 
#        leg.AddEntry( rocs2[0], "cores", 'l' );
#        leg.AddEntry( rocs3[0], "planflow", 'l' ); 
        leg.AddEntry( rocs4[0], "optimal", 'l' );         
        leg.AddEntry( rocs4ex[0], "optimal ex", 'l' );         
        leg.Draw();
        
        canBdtRoc.SaveAs("finalPlot/testROC_compex.eps");
        canBdtRoc.SaveAs("finalPlot/testROC_compex.png");

        hs = rocs4ex[2];
        hs.SetLineColor(4);        
        hs.Scale(1./hs.Integral());                
        hb = rocs4ex[3];
        hb.SetLineColor(2);        
        hb.Scale(1./hb.Integral());                
        canMassPrBdtCut = ROOT.TCanvas("canMassPrBdtCut","canMassPrBdtCut",800,800);    
        hs.Draw("hist");
        hb.Draw("histsames");
        canMassPrBdtCut.SaveAs("finalPlot/testmasspr.eps");
        canMassPrBdtCut.SaveAs("finalPlot/testmasspr.png");



