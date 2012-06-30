#include "enums.h"

void runSigSepWWSingle(int higgsMass, double intLumi, int nToys,  int test, int var, int toy, bool draw);

void runSigSepWW() {
  
  int higgsMass=125;
  double intLumi=20.0;
  int nToys = 1000;
  bool draw=false;

  // runSigSepWWSingle(higgsMass, intLumi, nToys,  zeroplusVSzerominus, MLLMT, pure, draw);
  // runSigSepWWSingle(higgsMass, intLumi, nToys,  zeroplusVSzerominus, MLL, pure, draw);
  // runSigSepWWSingle(higgsMass, intLumi, nToys,  zeroplusVSzerominus, DPHIMT, pure, draw);
  // runSigSepWWSingle(higgsMass, intLumi, nToys,  zeroplusVSzerominus, DPHI, pure, draw);

  // runSigSepWWSingle(higgsMass, intLumi, nToys,  zeroplusVStwoplus, DPHI, pure, draw);
  // runSigSepWWSingle(higgsMass, intLumi, nToys,  zeroplusVStwoplus, MLL, pure, draw);
  // runSigSepWWSingle(higgsMass, intLumi, nToys,  zeroplusVStwoplus, DPHIMT, pure, draw);
  runSigSepWWSingle(higgsMass, intLumi, nToys,  zeroplusVStwoplus, MLLMT, pure, draw);


}
void runSigSepWWSingle(int higgsMass, double intLumi, int nToys,  int test, int var, int toy, bool draw) {
    
    using namespace RooFit;
    
    gROOT->ProcessLine(".L ~/tdrstyle.C");
    setTDRStyle();
    gStyle->SetPadLeftMargin(0.16);
    gROOT->ForceStyle();
    gROOT->ProcessLine(".L statsFactory.cc+");
    
    //
    // set up test kind 
    // 

    TString testName = getTestName(test);
    TString varName = getVarName(var);
    TString toyName = getToyName(toy);
    
    std::cout << "Doing " << toyName << " studies on " << testName << " separation based on " << varName << "\n";

    double lowMt(0.);
    double highMt = higgsMass;
    double sigRate;
    double bkgRate;
    
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
    
    RooArgSet* obs;

    if ( var == DPHI )
      obs = new RooArgSet(*dphill) ;
    
    if ( var == MLL ) 
      obs = new RooArgSet(*mll) ;
    
    if ( var == MLLMT ) 
      obs = new RooArgSet(*mll, *mt) ;

    if ( var == DPHIMT ) 
      obs = new RooArgSet(*dphill, *mt) ;

    // read signal hypothesis 1
    TChain *tsigHyp1 = new TChain("angles");
    
    if ( test & ( zeroplusVSzerominus | zeroplusVStwoplus) )  {
      tsigHyp1->Add(Form("datafiles/%i/SMHiggsWW_%i_JHU.root",higgsMass, higgsMass));
    }

    RooDataSet *sigHyp1Data = new RooDataSet("sigHyp1Data","sigHyp1Data",tsigHyp1,*obs);
    RooDataHist *sigHyp1Hist = sigHyp1Data->binnedClone(0);
    RooHistPdf* sigHyp1Pdf = new RooHistPdf("sigHyp1Pdf", "sigHyp1Pdf", *obs, *sigHyp1Hist);

      
    // read signal hypothesis 2
    TChain *tsigHyp2 = new TChain("angles");
    if ( test & zeroplusVSzerominus ) 
      tsigHyp2->Add(Form("datafiles/%i/PSHiggsWW_%i_JHU.root",higgsMass, higgsMass));
    if ( test & zeroplusVStwoplus ) 
      tsigHyp2->Add(Form("datafiles/%i/TWW_%i_JHU.root",higgsMass, higgsMass));
    
    RooDataSet *sigHyp2Data = new RooDataSet("sigHyp2Data","sigHyp2Data",tsigHyp2,*obs);
    RooDataHist *sigHyp2Hist = sigHyp2Data->binnedClone(0);
    RooHistPdf* sigHyp2Pdf = new RooHistPdf("sigHyp2Pdf", "sigHyp2Pdf", *obs, *sigHyp2Hist);

    // read background
    TChain *bkgTree = new TChain("angles");
    bkgTree->Add(Form("datafiles/%i/WW_madgraph_8TeV.root",higgsMass));
    RooDataSet *bkgData = new RooDataSet("bkgData","bkgData",bkgTree,*obs);
    RooDataHist *bkgHist = bkgData->binnedClone(0);
    RooHistPdf* bkgPdf = new RooHistPdf("bkgPdf", "bkgPdf", *obs, *bkgHist);


    char statResults[25];
    statsFactory *myHypothesisSeparation;
    sprintf(statResults,"stat_%s_%s_%s_%.0ffb.root",testName.Data(), toyName.Data(), varName.Data(), intLumi);
    myHypothesisSeparation = new statsFactory(obs, sigHyp1Pdf, sigHyp2Pdf, statResults);
    // running pure toys
    myHypothesisSeparation->hypothesisSeparationWithBackground(sigRate*intLumi,sigRate*intLumi,nToys,bkgPdf,bkgRate*intLumi);
    delete myHypothesisSeparation;
    
    // draw plots 
    if(draw) {
      RooPlot* plot1;
      TString plot1Name;
      TCanvas* c1 = new TCanvas("c1","c1",400,400); 
      
      if ( var == DPHIMT || var == DPHI) {
	plot1 = dphill->frame();
	plot1Name = Form("MELAproj_%s_%s_%s_dphi", testName.Data(), toyName.Data(), varName.Data());
      }
      if ( var == MLL || var == MLLMT) {
	plot1 = mll->frame();
	plot1Name = Form("MELAproj_%s_%s_%s_mll", testName.Data(), toyName.Data(), varName.Data());
      }
      
      bkgData->plotOn(plot1,MarkerColor(kBlack));
      bkgPdf->plotOn(plot1, LineColor(kBlack), LineStyle(kDashed));
      sigHyp1Data->plotOn(plot1,MarkerColor(kRed));
      sigHyp1Pdf->plotOn(plot1,LineColor(kRed), LineStyle(kDashed));      
      sigHyp2Data->plotOn(plot1,MarkerColor(kBlue));
      sigHyp2Pdf->plotOn(plot1,LineColor(kBlue), LineStyle(kDashed));
      
      // draw...
      plot1->Draw();
      c1->SaveAs(Form("plots/epsfiles/%s.eps", plot1Name.Data()));
      c1->SaveAs(Form("plots/pngfiles/%s.png", plot1Name.Data()));

      
      if ( var  == DPHIMT || var == MLLMT ) {
	RooPlot* plot2 = mt->frame();
	TString	plot2Name;
	plot2Name = Form("MELAproj_%s_%s_%s_mt", testName.Data(), toyName.Data(), varName.Data());
	bkgData->plotOn(plot2,MarkerColor(kBlack));
	bkgPdf->plotOn(plot2, LineColor(kBlack), LineStyle(kDashed));
	sigHyp1Data->plotOn(plot2,MarkerColor(kRed));
	sigHyp1Pdf->plotOn(plot2,LineColor(kRed), LineStyle(kDashed));
	sigHyp2Data->plotOn(plot2,MarkerColor(kBlue));
	sigHyp2Pdf->plotOn(plot2,LineColor(kBlue), LineStyle(kDashed));
	c1->Clear();
	plot2->Draw();
	c1->SaveAs(Form("plots/epsfiles/%s.eps", plot2Name.Data()));
	c1->SaveAs(Form("plots/pngfiles/%s.png", plot2Name.Data()));
      }

      delete c1;
    }


}
