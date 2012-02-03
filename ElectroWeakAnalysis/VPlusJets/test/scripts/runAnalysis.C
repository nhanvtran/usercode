#include <iostream>
#include <TH1.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TLorentzVector.h>
#include <algorithm>	
#include <vector>



void runAnalysis(){

	gROOT->ProcessLine(".L ~/tdrstyle.C");
	setTDRStyle();

	gStyle->SetPadLeftMargin(0.16);
	
	gROOT->ProcessLine(".L vJetSubstructure.C+g");
	vJetSubstructure tt("data_v1/outputCrab_WW_full_v4.root");
    //vJetSubstructure tt("data_v1/outputCrab_Wjets_full_v2.root");
    
    //vJetSubstructure tt("data_v1/outputCrab_Wjets_full_45files.root");
    //vJetSubstructure tt("oldFiles/outputCrab_WW_full_v2.root");
	tt.Loop();

	



}

