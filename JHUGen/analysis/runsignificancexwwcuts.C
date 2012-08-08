#include "enums.h"

void runsignfiancesingle(int higgsMass, double intLumi, int nToys, int var, const spinType spin, const unsigned int seed);

void runsignificancexwwcuts(const Site site, const unsigned int seedOffset, const unsigned int nToys, const spinType spin, double intLumi) {

  //
  // load libraries
  //

  // site specific configuration
  std::string includePath = "";
  if (site == FNAL) {
    includePath = " -I/uscmst1/prod/sw/cms/slc5_amd64_gcc462/lcg/roofit/5.32.00-cms5/include/";
  } else if (site == UCSD) {
    includePath = " -I/code/osgcode/cmssoft/cms/slc5_amd64_gcc462/lcg/roofit/5.32.00-cms5/include/";
  } else {
    std::cout << "Invalid site - exiting" << std::endl;
    return;
  }

  using namespace RooFit;
  gSystem->AddIncludePath(includePath.c_str());
  
  gROOT->ProcessLine(".L tdrstyle.C");
  setTDRStyle();
  gStyle->SetPadLeftMargin(0.16);
  gROOT->ForceStyle();

  // load libraries
  gROOT->ProcessLine(".L statsFactory.cc++");
  gSystem->Load("libTree.so");
  gSystem->Load("libPhysics.so");
  gSystem->Load("libEG.so");
  gSystem->Load("libMathCore.so");

  int higgsMass=125;
  const unsigned int seed = 4126 + seedOffset;


  
  runsignfiancesingle( higgsMass, intLumi, nToys, MLLMT, spin, seed);
  
}  


 void runsignfiancesingle(int higgsMass, double intLumi, int nToys, int var, const spinType spin, const unsigned int seed)
{
  //
  // set up test kind 
  // 
  
  double sigRate;
  double bkgRate;
  if(higgsMass==125){
    sigRate = 13.4;
    bkgRate = 162.;
  }else{
    cout << "HMMMM.... I don't know that mass point...BYE!" << endl;
    return;
  }
  
  RooRealVar* dphill = new RooRealVar("dphill","#Delta#phi(leptons) [radian]", 0, TMath::Pi());
  dphill->setBins(20);
  RooRealVar* mt  = new RooRealVar("mt","transverse higgs mass", 50, 130);
  mt->setBins(10);
  RooRealVar* mll  = new RooRealVar("mll","dilepton mass [GeV]", 10, 90.);
  mll->setBins(10);
  
  TString varName = getVarName(var);
  
  RooArgSet* obs; 

  if ( var == DPHI )
    obs = new RooArgSet(*dphill) ;
  
  if ( var == MLL ) 
    obs = new RooArgSet(*mll) ;
    
  if ( var == MLLMT ) 
    obs = new RooArgSet(*mll, *mt) ;
  
  if ( var == DPHIMT ) 
    obs = new RooArgSet(*dphill, *mt) ;
  
  // for the ucsd batch submission
  const char *dataLocation =  "root://xrootd.unl.edu//store/user/yygao/HWWAngular/datafiles/";
  // const char *dataLocation = "datafiles/";
  
  // read signal hypothesis
  TChain *tsigHyp1 = new TChain("angles");
  TString sigFileName = getInputName(spin);
  tsigHyp1->Add(Form("%s/%i/%s_%i_JHU.root", dataLocation, higgsMass, sigFileName.Data(), higgsMass));
  RooDataSet *sigHyp1Data = new RooDataSet("sigHyp1Data","sigHyp1Data",tsigHyp1,*obs);
  RooDataHist *sigHyp1Hist = sigHyp1Data->binnedClone(0);
  RooHistPdf* sigHyp1Pdf = new RooHistPdf("sigHyp1Pdf", "sigHyp1Pdf", *obs, *sigHyp1Hist);

  // read background
  TChain *bkgTree = new TChain("angles");
  bkgTree->Add(Form("%s/%i/WW_madgraph_8TeV_0j.root",dataLocation, higgsMass));
  RooDataSet *bkgData = new RooDataSet("bkgData","bkgData",bkgTree,*obs);
  RooDataHist *bkgHist = bkgData->binnedClone(0);
  RooHistPdf* bkgPdf = new RooHistPdf("bkgPdf", "bkgPdf", *obs, *bkgHist);
    
  char statResults[50];
  statsFactory *hwwsignficance;
  sprintf(statResults,Form("significance_xww%.0fcuts_%s_%s_%.0ffb_%u.root", float(higgsMass), varName.Data(), sigFileName.Data(), intLumi, seed));
  hwwsignficance = new statsFactory(obs, sigHyp1Pdf, sigHyp1Pdf, seed, statResults);
  hwwsignficance->runSignificanceWithBackground(sigRate*intLumi, bkgRate*intLumi, bkgPdf, nToys);
  delete hwwsignficance;
}
