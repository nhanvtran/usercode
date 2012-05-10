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
    AutoLibraryLoader::enable();
    
    gSystem->Load("libCondFormatsJetMETObjects.so");
    gSystem->Load("libFWCoreUtilities.so");
    //gSystem->Load("libPhysicsToolsUtilities.so");
    //gSystem->Load("libPhysicsToolsKinFitter.so");
    //gROOT->ProcessLine(".include ../../../..");
    
    gROOT->ProcessLine(".L EffTableReader.cc+");
    gROOT->ProcessLine(".L EffTableLoader.cc+");
    
    gROOT->ProcessLine(".L vJetSubstructureAnalysis.C++");
    gROOT->ProcessLine(".L buildHistos.C+g");

    bool b_runAnalysis = true;
    bool b_buildHistos = false;
    bool isData = false;
    
    //bool b_runMuons = true;
    //bool b_runElectrons = false;

    // ---------------
    double LUMI = 1.;
    // ---------------
    
    
    if (b_runAnalysis){
        
        ///*
        //vJetSubstructureAnalysis test_ww("/eos/uscms/store/user/smpjs/ntran/tlbsm_v10/nt_ww_vj/demo*.root","ntuples_v4/test_ww.root");
        vJetSubstructureAnalysis test_ww("/eos/uscms/store/user/smpjs/ntran/tlbsm_v10_FallV1/ch_WWtoAnything/demo*.root","ntuples_v4/test_ww.root");
        test_ww.Loop(100);

        
        //vJetSubstructureAnalysis test_wj("/eos/uscms/store/user/smpjs/ntran/tlbsm_v10/nt_wj_vj/demo*.root","ntuples_v4/test_wj_dummy.root");
        //test_wj.Loop(100000);

        //vJetSubstructureAnalysis test_tt("/eos/uscms/store/user/smpjs/kalanand/ttbar-Summer11/demo*.root","ntuples_v4/test_tt.root");
        //test_tt.Loop(-1);
        // */
        ///*
        std::cout << "hi tt" << std::endl;
        //vJetSubstructureAnalysis test_dat("/eos/uscms/store/user/smpjs/ntran/tlbsm_v10/ntdata_SingleElectron_Prompt-v4/demo*.root","ntuples_v4/test_data_SingleElectron_Prompt-v4.root");
        //test_dat.Loop(-1);
        std::cout << "bi tt" << std::endl;
        //*/
        
        /*
        //vJetSubstructureAnalysis test_tt("/eos/uscms/store/user/smpjs/ntran/tlbsm_v10/nt_tt_vj/demo*.root","ntuples_v2/dummy.root");
        vJetSubstructureAnalysis test_tt("/eos/uscms/store/user/smpjs/kalanand/ttbar-Summer11/demo*.root","ntuples_v2/test_tt.root");
        test_tt.Loop(-1);
         //*/
    }
    
    if (b_buildHistos){
        ///*
        double sclfactor = LUMI*43000./4223922.;
        buildHistos ht_ww("ntuples_v2/test_ww.root","histos_v2_50/histos_ww.root", isData);
        ht_ww.Loop( sclfactor );
        
        ///*
        //sclfactor = LUMI*43000./4223922;
        sclfactor = LUMI*31300000./80978873;
        buildHistos ht_wj("ntuples_v2/test_wj.root","histos_v2_50/histos_wj.root", isData);
        ht_wj.Loop( sclfactor );
        //*/

        sclfactor = LUMI*163110./3683595;
        buildHistos ht_tt("ntuples_v2/test_tt.root","histos_v2_50/histos_tt.root", isData);
        ht_tt.Loop( sclfactor );
        //*/
        
        isData = true;
        sclfactor = 1;
        buildHistos ht_dat("ntuples_v2/test_data_SingleElectron_Prompt-v4.root","histos_v2_50/histos_data_SingleElectron_Prompt-v4.root", isData);
        ht_dat.Loop( sclfactor );
    }
    
}