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
    gROOT->ProcessLine(".L buildHistos.C+g");

    bool b_runAnalysis = false;
    bool b_buildHistos = true;
    
    //bool b_runMuons = true;
    //bool b_runElectrons = false;

    // ---------------
    double LUMI = 1.;
    // ---------------
    
    
    if (b_runAnalysis){
        
        vJetSubstructureAnalysis test_ww("/eos/uscms/store/user/smpjs/ntran/tlbsm_v10/nt_ww_vj/demo*.root","ntuples/test_ww.root");
        test_ww.Loop(-1);
        
        vJetSubstructureAnalysis test_wj("/eos/uscms/store/user/smpjs/ntran/tlbsm_v10/nt_wj_vj/demo*.root","ntuples/test_wj.root");
        test_wj.Loop(-1);

        vJetSubstructureAnalysis test_tt("/eos/uscms/store/user/smpjs/kalanand/ttbar-Summer11/demo*.root","ntuples/test_tt.root");
        test_tt.Loop(-1);

    }
    
    if (b_buildHistos){

        double sclfactor = LUMI*31300000./80978873;
        buildHistos ht_ww("ntuples/test_ww.root","ntuples/histos_ww.root");
        ht_ww.Loop( sclfactor );
        
        sclfactor = LUMI*43000./4223922;
        buildHistos ht_wj("ntuples/test_wj.root","ntuples/histos_wj.root");
        ht_wj.Loop( sclfactor );

        sclfactor = LUMI*163110./3683595;
        buildHistos ht_tt("ntuples/test_tt.root","ntuples/histos_tt.root");
        ht_tt.Loop( sclfactor );

    }
    
}