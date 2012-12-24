#! /usr/bin/env python
import os
import glob
import math
import array

from ROOT import gROOT, gStyle, gSystem, TLatex
import subprocess
from subprocess import Popen

#from sampleWrapperClass import *
#from BoostedWSamples import * 
from sampleWrapperClass_ele import *
from BoostedWSamples_ele import * 
from trainingClass import *
#from BoostedWSmallTreeSamples import *
from BoostedWUtils import *

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
parser.add_option('--makeControlPlots', action='store_true', dest='makeControlPlots', default=False, help='makeControlPlots')
parser.add_option('--makeTMVAPlots', action='store_true', dest='makeTMVAPlots', default=False, help='makeTMVAPlots')
parser.add_option('--makeSignalRegionControlPlots', action='store_true', dest='makeSignalRegionControlPlots', default=False,
                  help='makeSignalRegionControlPlots')
parser.add_option('--makeTTBarControlPlots', action='store_true', dest='makeTTBarControlPlots', default=False,
                  help='makeTTBarControlPlots')
parser.add_option('--doTraining', action='store_true', dest='doTraining', default=False,
                  help='does training')
parser.add_option('--makeFinalTree', action='store_true', dest='makeFinalTree', default=False,
                  help='make Final Tree')
#parser.add_option('-m', '--trainingMethod',action="store",type="string",dest="trainingMethod",default="BDT")
parser.add_option('-m', '--trainingMethod',action="store",type="string",dest="trainingMethod",default="Likelihood")
parser.add_option('-i', '--graphindex',action="store",type="int",dest="graphindex",default=0)

(options, args) = parser.parse_args()
############################################################
############################################################
############################################################

if __name__ == '__main__':

    
    print "Welcome to the boosted analysis..."
    
    # ---------------------------------------------------
    # check if directories exists
    if not os.path.isdir("trainingtrees"): os.system("mkdir trainingtrees");
    if not os.path.isdir("trainingtrees_ele"): os.system("mkdir trainingtrees_ele");
    if not os.path.isdir("classifier"): os.system("mkdir classifier");    

    # ---------------------------------------------------
    # define samples, this creates some trees in the "trainingtrees" directory
    isData = True;
    notData = False;
    #LUMI = 5.3
    #LUMI = 14.0
    LUMI = 13.9
    #sourcefiledirectory = ""
    #sourcefiledirectory = "./trainingtrees/"
    sourcefiledirectory = "/eos/uscms/store/user/lnujj/Moriond2013/ReducedTrees/"
    treename = ""
    if options.makeControlPlots or options.makeTTBarControlPlots: 
       sourcefiledirectory = "/eos/uscms/store/user/lnujj/Moriond2013/ReducedTrees/"
       treename = "WJet"
    if options.makeTMVAPlots:
       sourcefiledirectory = "/uscms_data/d3/weizou/VBFHiggsAnalysis/BoostedWAnalysis2012/boostedWWAnalysis/trainingtrees/"
       treename = "otree"
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
    ggH700Sample = sampleWrapperClass("ggH700",boostedWSamples.GetFileNames()["ggH700"],1.0/(boostedWSamples.GetLumiScaleFactor(lumifile,"ggH700")),LUMI,boostedWSamples.GetTreeName(),notData)
    ggH800Sample = sampleWrapperClass("ggH800",boostedWSamples.GetFileNames()["ggH800"],1.0/(boostedWSamples.GetLumiScaleFactor(lumifile,"ggH800")),LUMI,boostedWSamples.GetTreeName(),notData)
    ggH900Sample = sampleWrapperClass("ggH900",boostedWSamples.GetFileNames()["ggH900"],1.0/(boostedWSamples.GetLumiScaleFactor(lumifile,"ggH900")),LUMI,boostedWSamples.GetTreeName(),notData)
    ggH1000Sample = sampleWrapperClass("ggH1000",boostedWSamples.GetFileNames()["ggH1000"],1.0/(boostedWSamples.GetLumiScaleFactor(lumifile,"ggH1000")),LUMI,boostedWSamples.GetTreeName(),notData)

    #boostedWXS = 1.3*228.9E3;
    #WJetsSample_EffLumi = 8955318/boostedWXS;
    WJetsSample = sampleWrapperClass("WJets",boostedWSamples.GetFileNames()["WJets"],1.0/(boostedWSamples.GetLumiScaleFactor(lumifile,"WJets")),LUMI,boostedWSamples.GetTreeName(),notData)
    ZJetsSample = sampleWrapperClass("ZJets",boostedWSamples.GetFileNames()["ZJets"],1.0/(boostedWSamples.GetLumiScaleFactor(lumifile,"ZJets")),LUMI,boostedWSamples.GetTreeName(),notData)

    #TTbarSample_EffLumi = 6893735/225197.;
    TTbarSample = sampleWrapperClass("TTbar",boostedWSamples.GetFileNames()["TTbar"],1.0/(boostedWSamples.GetLumiScaleFactor(lumifile,"TTbar")),LUMI,boostedWSamples.GetTreeName(),notData);

    #WWSample_EffLumi = 9450414/33.61E3;
    WWSample = sampleWrapperClass("WW",boostedWSamples.GetFileNames()["WW"],1.0/(boostedWSamples.GetLumiScaleFactor(lumifile,"WW")),LUMI,boostedWSamples.GetTreeName(),notData);
   # WZSample_EffLumi = 10000267/12.63E3;
    WZSample = sampleWrapperClass("WZ",boostedWSamples.GetFileNames()["WZ"],1.0/(boostedWSamples.GetLumiScaleFactor(lumifile,"WZ")),LUMI,boostedWSamples.GetTreeName(),notData);
    #ZZSample_EffLumi = 9702850/5.196E3;
    ZZSample = sampleWrapperClass("ZZ",boostedWSamples.GetFileNames()["ZZ"],1.0/(boostedWSamples.GetLumiScaleFactor(lumifile,"ZZ")),LUMI,boostedWSamples.GetTreeName(),notData);
   
    tchSample = sampleWrapperClass("tch",boostedWSamples.GetFileNames()["tch"],1.0/(boostedWSamples.GetLumiScaleFactor(lumifile,"tch")),LUMI,boostedWSamples.GetTreeName(),notData);
    tWchSample = sampleWrapperClass("tWch",boostedWSamples.GetFileNames()["tWch"],1.0/(boostedWSamples.GetLumiScaleFactor(lumifile,"tWch")),LUMI,boostedWSamples.GetTreeName(),notData);
    schSample = sampleWrapperClass("sch",boostedWSamples.GetFileNames()["sch"],1.0/(boostedWSamples.GetLumiScaleFactor(lumifile,"sch")),LUMI,boostedWSamples.GetTreeName(),notData);
    tch_barSample = sampleWrapperClass("tch_bar",boostedWSamples.GetFileNames()["tch_bar"],1.0/(boostedWSamples.GetLumiScaleFactor(lumifile,"tch_bar")),LUMI,boostedWSamples.GetTreeName(),notData);
    tWch_barSample = sampleWrapperClass("tWch_bar",boostedWSamples.GetFileNames()["tWch_bar"],1.0/(boostedWSamples.GetLumiScaleFactor(lumifile,"tWch_bar")),LUMI,boostedWSamples.GetTreeName(),notData);
    sch_barSample = sampleWrapperClass("sch_bar",boostedWSamples.GetFileNames()["sch_bar"],1.0/(boostedWSamples.GetLumiScaleFactor(lumifile,"sch_bar")),LUMI,boostedWSamples.GetTreeName(),notData);

    #mcbackgrounds = [WJetsSample,WWSample,WZSample,ZZSample,TTbarSample]
    #myPlotter = plotterClass( ggH600Sample, mcbackgrounds, singlemu600Sample );

    if options.createTrainingTrees:
        
        # ---------------------------------------------------
        # create training tree
        #WJetsSample.createTrainingTree();

        singlemu600Sample.createTrainingTree();
        ggH600Sample.createTrainingTree();
        ggH700Sample.createTrainingTree();        
        ggH800Sample.createTrainingTree();        
        ggH900Sample.createTrainingTree();        
        ggH1000Sample.createTrainingTree();        
        WJetsSample.createTrainingTree();
        ZJetsSample.createTrainingTree();
        TTbarSample.createTrainingTree();
        WWSample.createTrainingTree();
        WZSample.createTrainingTree();
        ZZSample.createTrainingTree();
        tchSample.createTrainingTree();
        tWchSample.createTrainingTree();
        schSample.createTrainingTree();
        tch_barSample.createTrainingTree();
        tWch_barSample.createTrainingTree();
        sch_barSample.createTrainingTree();

    #mcbackgrounds = [WJetsSample,WWSample,WZSample,ZZSample,TTbarSample]
    #myPlotter = plotterClass( ggH600Sample, mcbackgrounds, singlemu600Sample );    
    
    if options.makeControlPlots:
                
        # ---------------------------------------------------
        # make control plots based on the same cuts as the training trees
        if not os.path.isdir("controlPlots"): os.system("mkdir controlPlots");
        #myPlotter.makeControlPlots("controlPlots","nocuts");
        print "Please Check the Cuts used on the BoostedWControlPlots.py is reasonable"
        Cuts = "W_pt > 180 && GroomedJet_CA8_pt_pr[0] > 180 && ggdboostedWevt == 1 && event_metMVA_met > 50"
        #Cuts = "W_pt > 180 && GroomedJet_CA8_pt_pr[0] > 180 && ggdboostedWevt == 1 && event_metMVA_met > 50 && GroomedJet_numberjets <= 1"
        #Cuts = "W_pt > 180 && GroomedJet_CA8_pt_pr[0] > 180 && ggdboostedWevt == 1 && event_metMVA_met > 50 && GroomedJet_numberbjets == 0"
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

    if options.makeTMVAPlots:
                
        # ---------------------------------------------------
        # make control plots based on the same cuts as the training trees
        if not os.path.isdir("controlPlots"): os.system("mkdir controlPlots");
        #myPlotter.makeControlPlots("controlPlots","nocuts");
        print "Please Check the Cuts used on the BoostedWTMVAPlots.py is reasonable"
        #Cuts = "W_pt > 180 && GroomedJet_CA8_pt_pr[0] > 180 && ggdboostedWevt == 1 && event_metMVA_met > 50"
        #Cuts = "W_pt > 180 && GroomedJet_CA8_pt_pr[0] > 180 && ggdboostedWevt == 1 && event_metMVA_met > 50 && GroomedJet_numberjets <= 1"
        #Cuts = "W_pt > 180 && GroomedJet_CA8_pt_pr[0] > 180 && ggdboostedWevt == 1 && event_metMVA_met > 50 && GroomedJet_numberbjets == 0"
        Cuts = "jet_mass_pr > 60 && jet_mass_pr < 100"
        #Cuts = "1 > 0"
        print "Cuts we apply: " + Cuts
        if options.noX:
           p = subprocess.Popen(["python","BoostedWTMVAPlots.py","-b","-f","%s"%sourcefiledirectory,"-t","%s"%treename,"-l","%f"%LUMI,"-s","%s"%lumifile,"-c","%s"%Cuts])
           if(p.wait() != None): raw_input( 'Press ENTER to continue\n ' )
        else:
           p = subprocess.Popen(["python","BoostedWTMVAPlots.py","-f","%s"%sourcefiledirectory,"-t","%s"%treename,"-l","%f"%LUMI,"-s","%s"%lumifile,"-c","%s"%Cuts])
           if(p.wait() != None): raw_input( 'Press ENTER to continue\n ' )
    # ---------------------------------------------------
    # do the training
    # get the training tree names
    signalTrainingTreeName = ggH600Sample.getTrainingTreeName();
    backgroundTrainingTreeNames = WJetsSample.getTrainingTreeName();
    
    trainingMethod = options.trainingMethod
    # Trainings
    # --------- #1 -----------
 #   listOfTrainingVariables1 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1"];
 #   WWTraining1 = trainingClass( signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables1, "simple" );
#    # --------- #2 -----------
##    listOfTrainingVariables2 = ["jet_grsens_tr","jet_grsens_ft","jet_massdrop_pr","jet_qjetvol","jet_tau2tau1","jet_rcore4","jet_rcore7","jet_planarflow04","jet_planarflow07"];
##    WWTraining2 = trainingClass( signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables2, "no subjets" );
#    listOfTrainingVariables2 = ["jet_grsens_tr","jet_grsens_ft","jet_massdrop_pr","jet_qjetvol","jet_tau2tau1","jet_sjdr","jet_rcore4","jet_rcore7","jet_planarflow04","jet_planarflow07"];
#    WWTraining2 = trainingClass( signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables2, "optimal" );
#
   # listOfTrainingVariables3 = ["jet_massdrop_pr"]
   # WWTraining3 = trainingClass(signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables3, trainingMethod, "massdrop")
#
#    listOfTrainingVariables4 = ["jet_massdrop_pr", "jet_tau2tau1"]
#    WWTraining4 = trainingClass(signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables4, "massdroptau2tau1")
#
#    listOfTrainingVariables5 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1","jet_rcore4"]
#    WWTraining5 = trainingClass(signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables5, "simplercore4")
#
#    listOfTrainingVariables6 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1","jet_rcore4","jet_rcore5"]
#    WWTraining6 = trainingClass(signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables6, "simplercore45")
#
#    listOfTrainingVariables7 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1","jet_rcore4","jet_rcore5","jet_rcore6"]
#    WWTraining7 = trainingClass(signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables7, "simplercore456")
#
#    listOfTrainingVariables8 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1","jet_rcore4","jet_rcore5","jet_rcore6","jet_rcore7"]
#    WWTraining8 = trainingClass(signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables8, "simplercore4567")
#
#    listOfTrainingVariables9 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1","jet_rcore4","jet_rcore5","jet_rcore6","jet_rcore7","jet_planarflow04"]
#    WWTraining9 = trainingClass(signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables9, "simplercore4567planarflow4")
#
#    listOfTrainingVariables10 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1","jet_rcore4","jet_rcore5","jet_rcore6","jet_rcore7","jet_planarflow04","jet_planarflow05"]
#    WWTraining10 = trainingClass(signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables10, "simplercore4567planarflow45")
#
#    listOfTrainingVariables11 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1","jet_rcore4","jet_rcore5","jet_rcore6","jet_rcore7","jet_planarflow04","jet_planarflow05","jet_planarflow06"]
#    WWTraining11 = trainingClass(signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables11, "simplercore4567planarflow456")
#
#    listOfTrainingVariables12 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1","jet_rcore4","jet_rcore5","jet_rcore6","jet_rcore7","jet_planarflow04","jet_planarflow05","jet_planarflow06","jet_planarflow07"]
#    WWTraining12 = trainingClass(signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables12, "simplercore4567planarflow4567")
#
#    listOfTrainingVariables13 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1","jet_rcore4","jet_rcore5","jet_rcore6","jet_rcore7","jet_planarflow04","jet_planarflow05","jet_planarflow06","jet_planarflow07","jet_pt1frac"]
#    WWTraining13 = trainingClass(signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables13, "simplercore4567planarflow4567subjet1")
#
#    listOfTrainingVariables14 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1","jet_rcore4","jet_rcore5","jet_rcore6","jet_rcore7","jet_planarflow04","jet_planarflow05","jet_planarflow06","jet_planarflow07","jet_pt2frac"]
#    WWTraining14 = trainingClass(signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables14, "simplercore4567planarflow4567subjet2")
#
#    listOfTrainingVariables15 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1","jet_rcore4","jet_rcore5","jet_rcore6","jet_rcore7","jet_planarflow04","jet_planarflow05","jet_planarflow06","jet_planarflow07","jet_pt1frac","jet_sjdr"]
#    WWTraining15 = trainingClass(signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables15, "simplercore4567planarflow4567subjet1sjdr")
#
#    listOfTrainingVariables16 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1","jet_rcore4","jet_rcore5","jet_rcore6","jet_rcore7","jet_planarflow04","jet_planarflow05","jet_planarflow06","jet_planarflow07","jet_pt1frac","jet_sjdr","jet_grsens_ft","jet_grsens_tr"]
#    WWTraining16 = trainingClass(signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables16, "simplercore4567planarflow4567subjet1sjdrgrsens_ftgrsens_tr")
#    # --------- #3 -----------
#    listOfTrainingVariables3 = ["jet_grsens_tr","jet_grsens_ft","jet_massdrop_pr","jet_qjetvol","jet_tau2tau1","jet_rcore7","jet_planarflow07"];
#    WWTraining3 = trainingClass( signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables3, "optimal2" );
#    # --------- #4 -----------
#    listOfTrainingVariables4 = ["jet_grsens_tr","jet_grsens_ft","jet_massdrop_pr","jet_qjetvol","jet_tau2tau1","jet_pt1frac","jet_sjdr","jet_jetconstituents","jet_rcore4","jet_rcore5","jet_rcore6","jet_rcore7","jet_planarflow04","jet_planarflow05","jet_planarflow06","jet_planarflow07"];
#    WWTraining4 = trainingClass( signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables4, "all" );
#    listOfTrainingVariables17 = ["jet_massdrop_pr","jet_qjetvol"];
#    WWTraining17 = trainingClass( signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables17, "massdropqjet" );
#    
    listOfTrainingVariables18 = ["jet_qjetvol","jet_tau2tau1"];
    WWTraining18 = trainingClass( signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables18,trainingMethod,"tau2tau1qjet" );
    ungroomed_WWTraining18 = ungroomed_trainingClass( signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables18,trainingMethod,"tau2tau1qjet" );
#     
#    listOfTrainingVariables19 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1","jet_pt1frac"];
#    WWTraining19 = trainingClass( signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables19, "simplesubjet1pt" );
#
#    listOfTrainingVariables20 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1","jet_pt1frac","jet_sjdr"];
#    WWTraining20 = trainingClass( signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables20, "simplesubjet1ptsjdr" );

    #listOfTrainingVariables21 = ["jet_massdrop_pr","jet_qjetvol","jet_pt1frac","jet_sjdr"];
    #WWTraining21 = trainingClass( signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables21, "massdropqjetsubjet1ptsjdr" );

##    listOfTrainingVariables22 = ["jet_qjetvol"];
##    WWTraining22 = trainingClass( signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables22,trainingMethod,"qjet" );

##    listOfTrainingVariables23 = ["jet_tau2tau1"];
##    WWTraining23 = trainingClass( signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables23,trainingMethod, "tau2tau1" );

#    listOfTrainingVariables24 = ["jet_qjetvol","jet_tau2tau1","jet_pt1frac","jet_sjdr"];
#    WWTraining24 = trainingClass( signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables24, trainingMethod, "tau2tau1qjetsubjet1ptsjdr" );
   
    #listOfTrainingVariables25 = ["jet_massdrop_pr","jet_qjetvol"];
    #WWTraining25 = trainingClass( signalTrainingTreeName, backgroundTrainingTreeNames, listOfTrainingVariables25,trainingMethod,"massdropqjet" );

    PrimaryVertex1 = 0
    PrimaryVertex2 = 15
    PrimaryVertex3 = 30
    PrimaryVertex4 = 40

    if options.doTraining:        
##        WWTraining18.doTraining( 200, 275, PrimaryVertex1, PrimaryVertex2);
##        WWTraining18.doTraining( 200, 275, PrimaryVertex2, PrimaryVertex3);
##        #WWTraining18.doTraining( 200, 275, PrimaryVertex3, PrimaryVertex4);
##        WWTraining18.doTraining( 275, 500, PrimaryVertex1, PrimaryVertex2);
##        WWTraining18.doTraining( 275, 500, PrimaryVertex2, PrimaryVertex3);
##        #WWTraining18.doTraining( 275, 500, PrimaryVertex3, PrimaryVertex4);
##        WWTraining18.plotTrainingResults( 200, 275, PrimaryVertex1, PrimaryVertex2);
##        WWTraining18.plotTrainingResults( 200, 275, PrimaryVertex2, PrimaryVertex3);
##        #WWTraining18.plotTrainingResults( 200, 275, PrimaryVertex3, PrimaryVertex4);
##        WWTraining18.plotTrainingResults( 275, 500, PrimaryVertex1, PrimaryVertex2);
##        WWTraining18.plotTrainingResults( 275, 500, PrimaryVertex2, PrimaryVertex3);
##        #WWTraining18.plotTrainingResults( 275, 500, PrimaryVertex3, PrimaryVertex4);


        WWTraining18.doTraining( 200, 275, 0, 100);
        WWTraining18.doTraining( 275, 500, 0, 100);
        
        ungroomed_WWTraining18.doTraining( 200, 275, 0, 100);
        ungroomed_WWTraining18.doTraining( 275, 500, 0, 100);


        WWTraining18.plotTrainingResults( 200, 275, 0, 100);
        WWTraining18.plotTrainingResults( 275, 500, 0, 100);       


#        WWTraining1.doTraining( 200, 275 );
#        WWTraining1.doTraining( 275, 500 );
#
#        WWTraining1.doTraining( 200, 275, 0,  10);
#        WWTraining1.doTraining( 200, 275, 10, 20);
#        WWTraining1.doTraining( 200, 275, 20, 30);
#        WWTraining1.doTraining( 275, 500, 0,  10);
#        WWTraining1.doTraining( 275, 500, 10, 20);
#        WWTraining1.doTraining( 275, 500, 20, 30);

##        WWTraining18.doTraining( 200, 275, PrimaryVertex1, PrimaryVertex2);
##        WWTraining18.doTraining( 200, 275, PrimaryVertex2, PrimaryVertex3);
##        #WWTraining18.doTraining( 200, 275, PrimaryVertex3, PrimaryVertex4);
##        WWTraining18.doTraining( 275, 500, PrimaryVertex1, PrimaryVertex2);
##        WWTraining18.doTraining( 275, 500, PrimaryVertex2, PrimaryVertex3);
##        #WWTraining18.doTraining( 275, 500, PrimaryVertex3, PrimaryVertex4);
#
##        WWTraining22.doTraining( 200, 275, PrimaryVertex1, PrimaryVertex2);
##        WWTraining22.doTraining( 200, 275, PrimaryVertex2, PrimaryVertex3);
        #WWTraining22.doTraining( 200, 275, PrimaryVertex3, PrimaryVertex4);
##        WWTraining22.doTraining( 275, 500, PrimaryVertex1, PrimaryVertex2);
##        WWTraining22.doTraining( 275, 500, PrimaryVertex2, PrimaryVertex3);
        #WWTraining22.doTraining( 275, 500, PrimaryVertex3, PrimaryVertex4);
#
##        WWTraining23.doTraining( 200, 275, PrimaryVertex1, PrimaryVertex2);
##        WWTraining23.doTraining( 200, 275, PrimaryVertex2, PrimaryVertex3);
        #WWTraining23.doTraining( 200, 275, PrimaryVertex3, PrimaryVertex4);
##        WWTraining23.doTraining( 275, 500, PrimaryVertex1, PrimaryVertex2);
##        WWTraining23.doTraining( 275, 500, PrimaryVertex2, PrimaryVertex3);
        #WWTraining23.doTraining( 275, 500, PrimaryVertex3, PrimaryVertex4);
#
#        WWTraining24.doTraining( 200, 275, PrimaryVertex1, PrimaryVertex2);
#        WWTraining24.doTraining( 200, 275, PrimaryVertex2, PrimaryVertex3);
#        #WWTraining24.doTraining( 200, 275, PrimaryVertex3, PrimaryVertex4);
#        WWTraining24.doTraining( 275, 500, PrimaryVertex1, PrimaryVertex2);
#        WWTraining24.doTraining( 275, 500, PrimaryVertex2, PrimaryVertex3);
#        #WWTraining24.doTraining( 275, 500, PrimaryVertex3, PrimaryVertex4);

#        WWTraining2.doTraining( 200, 275 );
#        WWTraining2.doTraining( 275, 500 );
#        
     #   WWTraining3.doTraining( 200, 275, 0, 100);
     #   WWTraining3.doTraining( 275, 500, 0, 100);
#
#        WWTraining4.doTraining( 200, 275 );
#        WWTraining4.doTraining( 275, 500 );
#
#        WWTraining5.doTraining( 200, 275 );
#        WWTraining5.doTraining( 275, 500 );
#
#        WWTraining6.doTraining( 200, 275 );
#        WWTraining6.doTraining( 275, 500 );
#
#        WWTraining7.doTraining( 200, 275 );
#        WWTraining7.doTraining( 275, 500 );
#
#        WWTraining8.doTraining( 200, 275 );
#        WWTraining8.doTraining( 275, 500 );
#
#        WWTraining9.doTraining( 200, 275 );
#        WWTraining9.doTraining( 275, 500 );
#
#        WWTraining10.doTraining( 200, 275 );
#        WWTraining10.doTraining( 275, 500 );
#
#        WWTraining11.doTraining( 200, 275 );
#        WWTraining11.doTraining( 275, 500 );
#
#        WWTraining12.doTraining( 200, 275 );
#        WWTraining12.doTraining( 275, 500 );
#
#        WWTraining13.doTraining( 200, 275 );
#        WWTraining13.doTraining( 275, 500 );
#
#        WWTraining14.doTraining( 200, 275 );
#        WWTraining14.doTraining( 275, 500 );
#
#        WWTraining15.doTraining( 200, 275 );
#        WWTraining15.doTraining( 275, 500 );
#
#        WWTraining16.doTraining( 200, 275 );
#        WWTraining16.doTraining( 275, 500 );
#        WWTraining3.doTraining( 200, 275 );
#        WWTraining3.doTraining( 275, 500 );
#
#        WWTraining4.doTraining( 200, 275 );
#        WWTraining4.doTraining( 275, 500 );
#
#        WWTraining17.doTraining( 200, 275 );
#        WWTraining17.doTraining( 275, 500 );
#        
#        WWTraining18.doTraining( 200, 275, 0, 100);
#        WWTraining18.doTraining( 275, 500, 0, 100);
#
#        WWTraining19.doTraining( 200, 275 );
#        WWTraining19.doTraining( 275, 500 );
#
#        WWTraining20.doTraining( 200, 275 );
#        WWTraining20.doTraining( 275, 500 );
#
#        WWTraining21.doTraining( 200, 275 );
#        WWTraining21.doTraining( 275, 500 );

#        WWTraining22.doTraining( 200, 275, 0, 100);
#        WWTraining22.doTraining( 275, 500, 0, 100);
#
#        WWTraining23.doTraining( 200, 275, 0, 100);
#        WWTraining23.doTraining( 275, 500, 0, 100);

#        WWTraining24.doTraining( 200, 275 );
#        WWTraining24.doTraining( 275, 500 );

      #  WWTraining25.doTraining( 200, 275, 0, 100);
      #  WWTraining25.doTraining( 275, 500, 0, 100);
#        WWTraining1.plotTrainingResults( 200, 275 );
#        WWTraining1.plotTrainingResults( 275, 500 );

#        WWTraining1.plotTrainingResults( 200, 275, 0, 10);
#        WWTraining1.plotTrainingResults( 200, 275, 10, 20);
#        WWTraining1.plotTrainingResults( 200, 275, 20, 30);
#        WWTraining1.plotTrainingResults( 275, 500, 0, 10);
#        WWTraining1.plotTrainingResults( 275, 500, 10, 20);
#        WWTraining1.plotTrainingResults( 275, 500, 20, 30);
##
##        WWTraining18.plotTrainingResults( 200, 275, PrimaryVertex1, PrimaryVertex2);
##        WWTraining18.plotTrainingResults( 200, 275, PrimaryVertex2, PrimaryVertex3);
##        #WWTraining18.plotTrainingResults( 200, 275, PrimaryVertex3, PrimaryVertex4);
##        WWTraining18.plotTrainingResults( 275, 500, PrimaryVertex1, PrimaryVertex2);
##        WWTraining18.plotTrainingResults( 275, 500, PrimaryVertex2, PrimaryVertex3);
##        #WWTraining18.plotTrainingResults( 275, 500, PrimaryVertex3, PrimaryVertex4);
##
##        WWTraining22.plotTrainingResults( 200, 275, PrimaryVertex1, PrimaryVertex2);
##        WWTraining22.plotTrainingResults( 200, 275, PrimaryVertex2, PrimaryVertex3);
        #WWTraining22.plotTrainingResults( 200, 275, PrimaryVertex3, PrimaryVertex4);
##        WWTraining22.plotTrainingResults( 275, 500, PrimaryVertex1, PrimaryVertex2);
##        WWTraining22.plotTrainingResults( 275, 500, PrimaryVertex2, PrimaryVertex3);
        #WWTraining22.plotTrainingResults( 275, 500, PrimaryVertex3, PrimaryVertex4);

##        WWTraining23.plotTrainingResults( 200, 275, PrimaryVertex1, PrimaryVertex2);
##        WWTraining23.plotTrainingResults( 200, 275, PrimaryVertex2, PrimaryVertex3);
        #WWTraining23.plotTrainingResults( 200, 275, PrimaryVertex3, PrimaryVertex4);
##        WWTraining23.plotTrainingResults( 275, 500, PrimaryVertex1, PrimaryVertex2);
##        WWTraining23.plotTrainingResults( 275, 500, PrimaryVertex2, PrimaryVertex3);
        #WWTraining23.plotTrainingResults( 275, 500, PrimaryVertex3, PrimaryVertex4);

#        WWTraining24.plotTrainingResults( 200, 275, PrimaryVertex1, PrimaryVertex2);
#        WWTraining24.plotTrainingResults( 200, 275, PrimaryVertex2, PrimaryVertex3);
#        #WWTraining24.plotTrainingResults( 200, 275, PrimaryVertex3, PrimaryVertex4);
#        WWTraining24.plotTrainingResults( 275, 500, PrimaryVertex1, PrimaryVertex2);
#        WWTraining24.plotTrainingResults( 275, 500, PrimaryVertex2, PrimaryVertex3);
#        #WWTraining24.plotTrainingResults( 275, 500, PrimaryVertex3, PrimaryVertex4);

#        WWTraining2.plotTrainingResults( 200, 275 );
#        WWTraining2.plotTrainingResults( 275, 500 );
                
#        WWTraining3.plotTrainingResults( 200, 275, 0, 100);
#        WWTraining3.plotTrainingResults( 275, 500, 0, 100);
#
#        WWTraining4.plotTrainingResults( 200, 275 );
#        WWTraining4.plotTrainingResults( 275, 500 );
#
#        WWTraining5.plotTrainingResults( 200, 275 );
#        WWTraining5.plotTrainingResults( 275, 500 );
#
#        WWTraining6.plotTrainingResults( 200, 275 );
#        WWTraining6.plotTrainingResults( 275, 500 );
#
#        WWTraining7.plotTrainingResults( 200, 275 );
#        WWTraining7.plotTrainingResults( 275, 500 );
#
#        WWTraining8.plotTrainingResults( 200, 275 );
#        WWTraining8.plotTrainingResults( 275, 500 );
#
#        WWTraining9.plotTrainingResults( 200, 275 );
#        WWTraining9.plotTrainingResults( 275, 500 );
#
#        WWTraining10.plotTrainingResults( 200, 275 );
#        WWTraining10.plotTrainingResults( 275, 500 );
#
#        WWTraining11.plotTrainingResults( 200, 275 );
#        WWTraining11.plotTrainingResults( 275, 500 );
#
#        WWTraining12.plotTrainingResults( 200, 275 );
#        WWTraining12.plotTrainingResults( 275, 500 );
#
#        WWTraining13.plotTrainingResults( 200, 275 );
#        WWTraining13.plotTrainingResults( 275, 500 );
#
#        WWTraining14.plotTrainingResults( 200, 275 );
#        WWTraining14.plotTrainingResults( 275, 500 );
#
#        WWTraining15.plotTrainingResults( 200, 275 );
#        WWTraining15.plotTrainingResults( 275, 500 );
#
#        WWTraining16.plotTrainingResults( 200, 275 );
#        WWTraining16.plotTrainingResults( 275, 500 );
#        WWTraining3.plotTrainingResults( 200, 275 );
#        WWTraining3.plotTrainingResults( 275, 500 );
#
#        WWTraining4.plotTrainingResults( 200, 275 );
#        WWTraining4.plotTrainingResults( 275, 500 );
#        WWTraining17.plotTrainingResults( 200, 275 );
#        WWTraining17.plotTrainingResults( 275, 500 );
#
#        WWTraining18.plotTrainingResults( 200, 275, 0, 100);
#        WWTraining18.plotTrainingResults( 275, 500, 0, 100);
#
#        WWTraining19.plotTrainingResults( 200, 275 );
#        WWTraining19.plotTrainingResults( 275, 500 );
#
#        WWTraining20.plotTrainingResults( 200, 275 );
#        WWTraining20.plotTrainingResults( 275, 500 );

#        WWTraining21.plotTrainingResults( 200, 275 );
#        WWTraining21.plotTrainingResults( 275, 500 );
        
#        WWTraining22.plotTrainingResults( 200, 275, 0, 100);
#        WWTraining22.plotTrainingResults( 275, 500, 0, 100);
#        
#        WWTraining23.plotTrainingResults( 200, 275, 0, 100);
#        WWTraining23.plotTrainingResults( 275, 500, 0, 100);

#        WWTraining24.plotTrainingResults( 200, 275 );
#        WWTraining24.plotTrainingResults( 275, 500 );

#        WWTraining25.plotTrainingResults( 200, 275, 0, 100);
#        WWTraining25.plotTrainingResults( 275, 500, 0, 100);

    if options.makeFinalTree:

        # ---------------------------------------------------   
        # make the final trees
        print "making final trees"
        if not os.path.isdir("finalPlot"): os.system("mkdir finalPlot");
        if options.noX: gROOT.SetBatch()
        
        # get name from training class (if name is MassDrop, special case)
        # give it the same set of variables
        # give it samples
        Signalefficiency = 0.6
        graphindex = options.graphindex
#        
        rocs18ptv1 = WWTraining18.makeFinalPlotsInternal( 200, 275, PrimaryVertex1, PrimaryVertex2);
        rocs18ptv2 = WWTraining18.makeFinalPlotsInternal( 200, 275, PrimaryVertex2, PrimaryVertex3);
        #rocs18ptv3 = WWTraining18.makeFinalPlotsInternal( 200, 275, PrimaryVertex3, PrimaryVertex4);
        PrintTable(rocs18ptv1[graphindex], rocs18ptv2[graphindex], WWTraining18, 200, 275, PrimaryVertex1, PrimaryVertex2, PrimaryVertex3, Signalefficiency)
        rocs18ptv4 = WWTraining18.makeFinalPlotsInternal( 275, 500, PrimaryVertex1, PrimaryVertex2);
        rocs18ptv5 = WWTraining18.makeFinalPlotsInternal( 275, 500, PrimaryVertex2, PrimaryVertex3);
        #rocs18ptv6 = WWTraining18.makeFinalPlotsInternal( 275, 500, PrimaryVertex3, PrimaryVertex4);
        PrintTable(rocs18ptv4[graphindex], rocs18ptv5[graphindex], WWTraining18, 275, 500, PrimaryVertex1, PrimaryVertex2, PrimaryVertex3, Signalefficiency)
#        
        rocs22ptv1 = WWTraining22.makeFinalPlotsInternal( 200, 275, PrimaryVertex1, PrimaryVertex2);
        rocs22ptv2 = WWTraining22.makeFinalPlotsInternal( 200, 275, PrimaryVertex2, PrimaryVertex3);
        #rocs22ptv3 = WWTraining22.makeFinalPlotsInternal( 200, 275, PrimaryVertex3, PrimaryVertex4);
        PrintTable(rocs22ptv1[graphindex], rocs22ptv2[graphindex], WWTraining22, 200, 275, PrimaryVertex1, PrimaryVertex2, PrimaryVertex3, Signalefficiency)
        rocs22ptv4 = WWTraining22.makeFinalPlotsInternal( 275, 500, PrimaryVertex1, PrimaryVertex2);
        rocs22ptv5 = WWTraining22.makeFinalPlotsInternal( 275, 500, PrimaryVertex2, PrimaryVertex3);
        #rocs22ptv6 = WWTraining22.makeFinalPlotsInternal( 275, 500, PrimaryVertex3, PrimaryVertex4);
        PrintTable(rocs22ptv4[graphindex], rocs22ptv5[graphindex], WWTraining22, 275, 500, PrimaryVertex1, PrimaryVertex2, PrimaryVertex3, Signalefficiency)
        
        rocs23ptv1 = WWTraining23.makeFinalPlotsInternal( 200, 275, PrimaryVertex1, PrimaryVertex2);
        rocs23ptv2 = WWTraining23.makeFinalPlotsInternal( 200, 275, PrimaryVertex2, PrimaryVertex3);
        #rocs23ptv3 = WWTraining23.makeFinalPlotsInternal( 200, 275, PrimaryVertex3, PrimaryVertex4);
        PrintTable(rocs23ptv1[graphindex], rocs23ptv2[graphindex], WWTraining23, 200, 275, PrimaryVertex1, PrimaryVertex2, PrimaryVertex3, Signalefficiency)
        rocs23ptv4 = WWTraining23.makeFinalPlotsInternal( 275, 500, PrimaryVertex1, PrimaryVertex2);
        rocs23ptv5 = WWTraining23.makeFinalPlotsInternal( 275, 500, PrimaryVertex2, PrimaryVertex3);
        #rocs23ptv6 = WWTraining23.makeFinalPlotsInternal( 275, 500, PrimaryVertex3, PrimaryVertex4);
        PrintTable(rocs23ptv4[graphindex], rocs23ptv5[graphindex], WWTraining23, 275, 500, PrimaryVertex1, PrimaryVertex2, PrimaryVertex3, Signalefficiency)
        
#        rocs24ptv1 = WWTraining24.makeFinalPlotsInternal( 200, 275, PrimaryVertex1, PrimaryVertex2);
#        rocs24ptv2 = WWTraining24.makeFinalPlotsInternal( 200, 275, PrimaryVertex2, PrimaryVertex3);
#        #rocs24ptv3 = WWTraining24.makeFinalPlotsInternal( 200, 275, PrimaryVertex3, PrimaryVertex4);
#        PrintTable(rocs24ptv1[graphindex], rocs24ptv2[graphindex], WWTraining24, 200, 275, PrimaryVertex1, PrimaryVertex2, PrimaryVertex3, Signalefficiency)
#        rocs24ptv4 = WWTraining24.makeFinalPlotsInternal( 275, 500, PrimaryVertex1, PrimaryVertex2);
#        rocs24ptv5 = WWTraining24.makeFinalPlotsInternal( 275, 500, PrimaryVertex2, PrimaryVertex3);
#        #rocs24ptv6 = WWTraining24.makeFinalPlotsInternal( 275, 500, PrimaryVertex3, PrimaryVertex4);
#        PrintTable(rocs24ptv4[graphindex], rocs24ptv5[graphindex], WWTraining24, 275, 500, PrimaryVertex1, PrimaryVertex2, PrimaryVertex3, Signalefficiency)
##        
#        rocs3ptv1 = WWTraining3.makeFinalPlotsInternal( 200, 275, 0, 100);
#        rocs3ptv2 = WWTraining3.makeFinalPlotsInternal( 200, 275, 0, 100);
#        PrintTotalTable(rocs3ptv1[graphindex], rocs3ptv2[graphindex], WWTraining3, 200, 275, 0, 100, Signalefficiency)
#
#        rocs18ptv1 = WWTraining18.makeFinalPlotsInternal( 200, 275, 0, 100);
#        rocs18ptv2 = WWTraining18.makeFinalPlotsInternal( 200, 275, 0, 100);
#        PrintTotalTable(rocs18ptv1[graphindex], rocs18ptv2[graphindex], WWTraining18, 200, 275, 0, 100, Signalefficiency)
#
#        rocs22ptv1 = WWTraining22.makeFinalPlotsInternal( 200, 275, 0, 100);
#        rocs22ptv2 = WWTraining22.makeFinalPlotsInternal( 200, 275, 0, 100);
#        PrintTotalTable(rocs22ptv1[graphindex], rocs22ptv2[graphindex], WWTraining22, 200, 275, 0, 100, Signalefficiency)
#
#        rocs23ptv1 = WWTraining23.makeFinalPlotsInternal( 200, 275, 0, 100);
#        rocs23ptv2 = WWTraining23.makeFinalPlotsInternal( 200, 275, 0, 100);
#        PrintTotalTable(rocs23ptv1[graphindex], rocs23ptv2[graphindex], WWTraining23, 200, 275, 0, 100, Signalefficiency)
#
#        rocs25ptv1 = WWTraining25.makeFinalPlotsInternal( 200, 275, 0, 100);
#        rocs25ptv2 = WWTraining25.makeFinalPlotsInternal( 200, 275, 0, 100);
#        PrintTotalTable(rocs25ptv1[graphindex], rocs25ptv2[graphindex], WWTraining25, 200, 275, 0, 100, Signalefficiency)
#
#        rocs3ptv1 = WWTraining3.makeFinalPlotsInternal( 275, 500, 0, 100);
#        rocs3ptv2 = WWTraining3.makeFinalPlotsInternal( 275, 500, 0, 100);
#        PrintTotalTable(rocs3ptv1[graphindex], rocs3ptv2[graphindex], WWTraining3, 275, 500, 0, 100, Signalefficiency)
#
#        rocs18ptv1 = WWTraining18.makeFinalPlotsInternal( 275, 500, 0, 100);
#        rocs18ptv2 = WWTraining18.makeFinalPlotsInternal( 275, 500, 0, 100);
#        PrintTotalTable(rocs18ptv1[graphindex], rocs18ptv2[graphindex], WWTraining18, 275, 500, 0, 100, Signalefficiency)
#
#        rocs22ptv1 = WWTraining22.makeFinalPlotsInternal( 275, 500, 0, 100);
#        rocs22ptv2 = WWTraining22.makeFinalPlotsInternal( 275, 500, 0, 100);
#        PrintTotalTable(rocs22ptv1[graphindex], rocs22ptv2[graphindex], WWTraining22, 275, 500, 0, 100, Signalefficiency)
#
#        rocs23ptv1 = WWTraining23.makeFinalPlotsInternal( 275, 500, 0, 100);
#        rocs23ptv2 = WWTraining23.makeFinalPlotsInternal( 275, 500, 0, 100);
#        PrintTotalTable(rocs23ptv1[graphindex], rocs23ptv2[graphindex], WWTraining23, 275, 500, 0, 100, Signalefficiency)
#
#        rocs25ptv1 = WWTraining25.makeFinalPlotsInternal( 275, 500, 0, 100);
#        rocs25ptv2 = WWTraining25.makeFinalPlotsInternal( 275, 500, 0, 100);
#        PrintTotalTable(rocs25ptv1[graphindex], rocs25ptv2[graphindex], WWTraining25, 275, 500, 0, 100, Signalefficiency)
#
#        rocs2 = WWTraining2.makeFinalPlotsInternal( 200, 275 );
##        rocs3 = WWTraining3.makeFinalPlotsInternal( 200, 275 );
##        rocs4 = WWTraining4.makeFinalPlotsInternal( 200, 275 );
#
##        rocs1ex = WWTraining1.makeFinalPlots( 200, 275, 0. );
#        rocs2ex = WWTraining2.makeFinalPlots( 200, 275, 0. );
##        rocs3ex = WWTraining3.makeFinalPlots( 200, 275, 0. );        
##        rocs4ex = WWTraining4.makeFinalPlots( 200, 275, 0. );
#        
#        canBdtRoc = ROOT.TCanvas("canBdtRoc","canBdtRoc",800,800);    
#        canBdtRoc.cd();
#        hrl = canBdtRoc.DrawFrame(0,0,1.0,1.0);
#        hrl.GetXaxis().SetTitle("#epsilon_{sig}");
#        hrl.GetYaxis().SetTitle("1 - #epsilon_{bkg}");
#        canBdtRoc.SetGrid();
#        rocs1[0].Draw();
#        rocs1[1].SetLineColor(ROOT.kRed);
#        rocs1[1].Draw();
#        rocs2[0].SetLineColor(ROOT.kBlue);
#        rocs2[0].Draw();
##        rocs3[0].SetLineColor(ROOT.kMagenta);
##        rocs3[0].Draw();
##        rocs4[0].SetLineColor(ROOT.kGreen+2);
##        rocs4[0].Draw();
#
##        rocs1[2].SetLineWidth(2);
##        rocs1[2].SetLineColor(ROOT.kBlack);
##        rocs1[2].Draw();
##        rocs2[2].SetLineWidth(2);
##        rocs2[2].SetLineColor(ROOT.kBlue);
##        rocs2[2].Draw();
##        rocs3[2].SetLineWidth(2);
##        rocs3[2].SetLineColor(ROOT.kMagenta);
##        rocs3[2].Draw();
##        rocs4[2].SetLineWidth(2);
##        rocs4[2].SetLineColor(ROOT.kGreen+2);
##        rocs4[2].Draw();
#        
##        rocs4[2].SetLineColor(ROOT.kCyan+2);
##        rocs4[2].SetLineStyle(2);
##        rocs4[2].Draw();
#        
#        leg = ROOT.TLegend(0.25,0.2,0.55,0.5)
#        leg.SetFillColor(0)
#        leg.SetBorderSize(0)                
#        leg.AddEntry( rocs1[0], "simple", 'l' );
#        leg.AddEntry( rocs1[1], "mass drop only", 'l' ); 
#        leg.AddEntry( rocs2[0], "optimal", 'l' );
##        leg.AddEntry( rocs3[0], "optimal2", 'l' ); 
##        leg.AddEntry( rocs4[0], "all", 'l' );         
##        leg.AddEntry( rocs4ex[0], "all ex", 'l' );         
#        leg.Draw();
#        
#        canBdtRoc.SaveAs("finalPlot/testROC_compall.eps");
#        canBdtRoc.SaveAs("finalPlot/testROC_compall.png");
#
#        hs = rocs2ex[2];
#        hs.SetLineColor(4);        
#        hs.Scale(1./hs.Integral());                
#        hb = rocs2ex[3];
#        hb.SetLineColor(2);        
#        hb.Scale(1./hb.Integral());                
#        canMassPrBdtCut = ROOT.TCanvas("canMassPrBdtCut","canMassPrBdtCut",800,800);    
#        hs.Draw("hist");
#        hb.Draw("histsames");
#        canMassPrBdtCut.SaveAs("finalPlot/testmasspr.eps");
#        canMassPrBdtCut.SaveAs("finalPlot/testmasspr.png");
        raw_input( 'Press ENTER to continue\n ' )
