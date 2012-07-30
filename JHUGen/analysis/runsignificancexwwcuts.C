#include "enums.h"

void runsignfiancesingle(int higgsMass, double intLumi, int nToys, int var, const spinType spin, const unsigned int seed);

void runsignificancexwwcuts(const unsigned int seedOffset, const unsigned int nToys, const spinType spin) {

  int higgsMass=125;
  double intLumi=10.0;
  const unsigned int seed = 4126 + seedOffset;
  
  runsignfiancesingle( higgsMass, intLumi, nToys, MLLMT, spin, seed);
  
}  


 void runsignfiancesingle(int higgsMass, double intLumi, int nToys, int var, const spinType spin, const unsigned int seed)
{
  using namespace RooFit;
  
  gROOT->ProcessLine(".L ~/tdrstyle.C");
  setTDRStyle();
  gStyle->SetPadLeftMargin(0.16);
  gROOT->ForceStyle();

   // for the ucsd batch submission
  // gSystem->AddIncludePath(" -I/code/osgcode/cmssoft/cms/slc5_amd64_gcc462/lcg/roofit/5.32.00-cms5/include/");
  gROOT->ProcessLine(".L statsFactory.cc++");

  //
  // set up test kind 
  // 
  
  double sigRate;
  double bkgRate;
  double lowMt(0.);
  double highMt = higgsMass;
  
  if(higgsMass==125){
    sigRate = 25.;
    bkgRate = 250.;
  }else{
    cout << "HMMMM.... I don't know that mass point...BYE!" << endl;
    return;
  }
  
  RooRealVar* dphill = new RooRealVar("dphill","#Delta#phi(leptons) [radian]", 0, TMath::Pi());
  dphill->setBins(20);
  RooRealVar* mt  = new RooRealVar("mt","transverse higgs mass", lowMt, highMt);
  mt->setBins(20);
  RooRealVar* mll  = new RooRealVar("mll","dilepton mass [GeV]", 12, 80.);
  mll->setBins(17);
  
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
  // const char *dataLocation = "/hadoop/cms/store/user/yygao/HWWAngular/datafiles/";
  const char *dataLocation = "datafiles/";
  
  // read signal hypothesis
  TChain *tsigHyp1 = new TChain("angles");
  TString sigFileName = getInputName(spin);
  tsigHyp1->Add(Form("%s/%i/%s_%i_JHU.root", dataLocation.Data(), higgsMass, sigFileName.Data(), higgsMass));
  RooDataSet *sigHyp1Data = new RooDataSet("sigHyp1Data","sigHyp1Data",tsigHyp1,*obs);
  RooDataHist *sigHyp1Hist = sigHyp1Data->binnedClone(0);
  RooHistPdf* sigHyp1Pdf = new RooHistPdf("sigHyp1Pdf", "sigHyp1Pdf", *obs, *sigHyp1Hist);

  // read background
  TChain *bkgTree = new TChain("angles");
  bkgTree->Add(Form("datafiles/%i/WW_madgraph_8TeV.root",higgsMass));
  RooDataSet *bkgData = new RooDataSet("bkgData","bkgData",bkgTree,*obs);
  RooDataHist *bkgHist = bkgData->binnedClone(0);
  RooHistPdf* bkgPdf = new RooHistPdf("bkgPdf", "bkgPdf", *obs, *bkgHist);
    
  char statResults[50];
  statsFactory *hwwsignficance;
  sprintf(statResults,Form("significance_%.0ffb_xww%.0fcuts_%s_%s.root", intLumi, float(higgsMass), varName.Data(), sigFileName.Data()));
  hwwsignficance = new statsFactory(obs, sigHyp1Pdf, sigHyp1Pdf, seed, statResults);
  hwwsignficance->runSignificanceWithBackground(sigRate*intLumi, bkgRate*intLumi, bkgPdf, nToys);
  delete hwwsignficance;
}
