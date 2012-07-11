/*
   This script skims the angular ntuples for a given higgs mass selections
   run by root -l wwskim.C+
*/

#include "TFile.h"
#include "TTree.h"
#include "TLeaf.h"
#include <iostream>
#include <fstream>
#include "TH2F.h"
#include "TH1F.h"
#include "TString.h"
#include "TRint.h"
#include "TChain.h"
#include "TROOT.h"
#include "TStopwatch.h"
#include "TAxis.h"
#include "TMath.h"
#include "TCut.h"

using namespace std;

//###################
//# main function
//###################

void skimsingle(TString inputFDir, TString fileName, TString outputDir, float mH);


void wwskim() {

  TString inputFDir = "./";
  TString outputFDir = "datafiles/bdtpresel/";
  float mH = 125; 
  
  skimsingle(inputFDir, "WW_madgraph_8TeV.root", outputFDir, mH);
  skimsingle(inputFDir, "PSHiggsWW_125_JHU.root", outputFDir, mH);
  skimsingle(inputFDir, "SMHiggsWW_125_JHU.root", outputFDir, mH);
  skimsingle(inputFDir, "TWW_125_JHU.root", outputFDir, mH);

}

void skimsingle(TString inputFDir, TString fileName, TString outputDir, float mH) {

  TString inputFileName  = inputFDir + fileName; 

  TFile* fin = new TFile(inputFileName);
  TTree* ch=(TTree*)fin->Get("angles"); 
  if (ch==0x0) return; 
  
  TString outputFileName = Form("%s/%.0f/%s", outputDir.Data(), mH, fileName.Data());
  
  TFile *newfile= new TFile(outputFileName,"recreate");
  TTree* evt_tree=(TTree*) ch->CloneTree(0, "fast");
  
  // get event based branches..
  double mll_ = 0.;
  double mt_ = 0.;
  double dilpt_ = 0.;
  
  ch->SetBranchAddress( "mt"         , &mt_     );     
  ch->SetBranchAddress( "mll"        , &mll_     );     
  ch->SetBranchAddress( "dilpt"      , &dilpt_     );     
  

  
  //==========================================
  // Loop All Events
  //==========================================
  
  std::cout << inputFileName << " has " << ch->GetEntries() << " entries; \n";

  for(int ievt = 0; ievt < ch->GetEntries() ;ievt++){
    ch->GetEntry(ievt); 
    if ( mll_ < 12.0) continue;
    if ( mll_ > 80.0) continue;
    if ( mt_ > mH ) continue;
    // bdt preselections
    if ( dilpt_ < 45. ) continue;
    if ( mt_ < 80. ) continue;
    
    evt_tree->Fill();
  }   //nevent
  
  std::cout << outputFileName << " has " << evt_tree->GetEntries() << " entries; \n";
  newfile->cd(); 
  evt_tree->Write(); 
  newfile->Close();
}  
