#include "enums.h"

void runUPWW() {
  
  int higgsMass=125;
  double intLumi=5.1;
  int nToys = 10;
  bool draw=true;
  
  using namespace RooFit;
  
  gROOT->ProcessLine(".L ~/tdrstyle.C");
  setTDRStyle();
  gStyle->SetPadLeftMargin(0.16);
  gROOT->ForceStyle();
  gROOT->ProcessLine(".L statsFactory.cc+");
  
  //
  // set up test kind 
  // 
  
  double sigRate;
  double bkgRate;
  
  if(higgsMass==125){
    sigRate = 7.;
    bkgRate = 66.;
  }else{
    cout << "HMMMM.... I don't know that mass point...BYE!" << endl;
    return;
  }
  
  RooRealVar* mll  = new RooRealVar("mll","dilepton mass [GeV]", 12, 80.);
  mll->setBins(17);
  
  RooArgSet* obs = new RooArgSet(*mll) ;
  
  // read signal hypothesis 1
  TChain *tsigHyp1 = new TChain("angles");
  tsigHyp1->Add(Form("datafiles/bdtpresel/%i/SMHiggsWW_%i_JHU.root",higgsMass, higgsMass));
  RooDataSet *sigHyp1Data = new RooDataSet("sigHyp1Data","sigHyp1Data",tsigHyp1,*obs);
  RooDataHist *sigHyp1Hist = sigHyp1Data->binnedClone(0);
  RooHistPdf* sigHyp1Pdf = new RooHistPdf("sigHyp1Pdf", "sigHyp1Pdf", *obs, *sigHyp1Hist);

  // read background
  TChain *bkgTree = new TChain("angles");
  bkgTree->Add(Form("datafiles/bdtpresel/%i/WW_madgraph_8TeV.root",higgsMass));
  RooDataSet *bkgData = new RooDataSet("bkgData","bkgData",bkgTree,*obs);
  RooDataHist *bkgHist = bkgData->binnedClone(0);
  RooHistPdf* bkgPdf = new RooHistPdf("bkgPdf", "bkgPdf", *obs, *bkgHist);
    
  char statResults[25];
  statsFactory *hwwuls;
  sprintf(statResults,"uls_hww125_%.0ffb.root", intLumi);
  hwwuls = new statsFactory(obs, sigHyp1Pdf, sigHyp1Pdf, statResults);
  hwwuls->runUpperLimitWithBackground(sigRate*intLumi, bkgRate*intLumi, bkgPdf, nToys);
  delete hwwuls;
  

  // draw plots 
  if(draw) {
    RooPlot* plot1 = mll->frame();
    TString plot1Name = "mll";
    TCanvas* c1 = new TCanvas("c1","c1",400,400); 
    
    bkgData->plotOn(plot1,MarkerColor(kBlack));
    bkgPdf->plotOn(plot1, LineColor(kBlack), LineStyle(kDashed));
    sigHyp1Data->plotOn(plot1,MarkerColor(kRed));
    sigHyp1Pdf->plotOn(plot1,LineColor(kRed), LineStyle(kDashed));      
    
    // draw...
    plot1->Draw();
    c1->SaveAs(Form("plots/ul/epsfiles/%s.eps", plot1Name.Data()));
    c1->SaveAs(Form("plots/ul/pngfiles/%s.png", plot1Name.Data()));
    
    delete c1;
  }
  
  
}
