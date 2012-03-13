#include <iostream>
#include <TH1.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TLorentzVector.h>
#include <algorithm>	
#include <vector>



void runVJetSubstructureAnalysis(){

	gROOT->ProcessLine(".L ~/tdrstyle.C");
	setTDRStyle();
    
	gStyle->SetPadLeftMargin(0.16);
    gSystem->Load("libFWCoreFWLite.so");
    gSystem->Load("libPhysicsToolsUtilities.so");
    gSystem->Load("libPhysicsToolsKinFitter.so");
    gROOT->ProcessLine(".include ../../../..");
    
    gROOT->ProcessLine(".L EffTableReader.cc+");
    gROOT->ProcessLine(".L EffTableLoader.cc+");
    
    gROOT->ProcessLine(".L vJetSubstructureAnalysis.C+g");

    

    bool runMuons = true;
    bool runElectrons = false;

    double scf = 1/5.000; // one over integrated lumi of the sample
    vJetSubstructureAnalysis test_ttbar("/eos/uscms/store/user/ntran/smpjs/v10_v2/ttbar_vjet/demo*.root","ntuples/test.root");
    //vJetSubstructureAnalysis test_ttbar("root://xrootd.unl.edu//store//ntran/smpjs/v10_v2/ttbar_vjet/demo_10_1_K4Z.root","ntuples/test.root");
    //vJetSubstructureAnalysis test_ttbar("tmp/demo*.root","ntuples/test.root");
    test_ttbar.Loop(20000);
    
    
}