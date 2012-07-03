#include "enums.h"

void runsignfiancesingle(int higgsMass, double intLumi, int nToys, int var, int spin);

void runsignificancexwwcuts() 
{

  int higgsMass=125;
  double intLumi=10.0;
  int nToys = 1000;

  // runsignfiancesingle( higgsMass, intLumi, nToys, DPHIMT, zeroplus);
  // runsignfiancesingle( higgsMass, intLumi, nToys, MLLMT, zeroplus);
  
  // runsignfiancesingle( higgsMass, intLumi, nToys, DPHIMT, zerominus);
  // runsignfiancesingle( higgsMass, intLumi, nToys, MLLMT, zerominus);

  runsignfiancesingle( higgsMass, intLumi, nToys, MLLMT, twoplus);
  // runsignfiancesingle( higgsMass, intLumi, nToys, DPHIMT, twoplus);

  // runsignfiancesingle( higgsMass, intLumi, nToys, MLL, zeroplus);

}  


void runsignfiancesingle(int higgsMass, double intLumi, int nToys, int var, int spin)
{
  using namespace RooFit;
  
  gROOT->ProcessLine(".L ~/tdrstyle.C");
  setTDRStyle();
  gStyle->SetPadLeftMargin(0.16);
  gROOT->ForceStyle();
  gROOT->ProcessLine(".L statsFactory.cc+");

  const unsigned int seed = 0762073843;
  
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
  
  
  TString fileName = getInputName(spin);
  
  // read signal hypothesis 1
  TChain *tsigHyp1 = new TChain("angles");
  tsigHyp1->Add(Form("datafiles/%i/%s_%i_JHU.root",higgsMass, fileName.Data(), higgsMass));
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
  sprintf(statResults,Form("significance_hww125_%.0ffb_xwwcuts_%s_%s.root", intLumi, varName.Data(), fileName.Data()));
  hwwsignficance = new statsFactory(obs, sigHyp1Pdf, sigHyp1Pdf, seed, statResults);
  hwwsignficance->runSignificanceWithBackground(sigRate*intLumi, bkgRate*intLumi, bkgPdf, nToys);
  delete hwwsignficance;
}
