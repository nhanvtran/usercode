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
    vJetSubstructureAnalysis test_ww("/eos/uscms/store/user/smpjs/ntran/tlbsm_v10/nt_ww_vj/demo*.root","ntuples/test_ww.root");
    test_ww.Loop(-1);
    
    vJetSubstructureAnalysis test_wj("/eos/uscms/store/user/smpjs/ntran/tlbsm_v10/nt_wj_vj/demo*.root","ntuples/test_wj.root");
    test_wj.Loop(-1);
    
}