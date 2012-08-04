#include "enums.h"

void runSigSepWWSingle(int higgsMass, double intLumi, int nToys,  const TestType test, int var, int toy, bool draw, const unsigned int seed);

void runSigSepWW(const Site site, 
		 const unsigned int seedOffset, const unsigned int nToys, const TestType test, double intLumi) {

    //
    // load libraries
    //

    // site specific configuration
    std::string includePath = "";
    if (site == FNAL)  {
	includePath = " -I/uscmst1/prod/sw/cms/slc5_amd64_gcc462/lcg/roofit/5.32.00-cms5/include/";
    } else if (site == UCSD) {
	includePath = " -I/code/osgcode/cmssoft/cms/slc5_amd64_gcc462/lcg/roofit/5.32.00-cms5/include/";
    } else {
	std::cout << "Invalid site - exiting" << std::endl;
	return;
    }

    // roofit
    using namespace RooFit;
    gSystem->AddIncludePath(includePath.c_str());

    // for plotting
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

    //
    // configuration
    //
  
    const int higgsMass=125;
    const bool draw=false;
    const unsigned int seed = 4126 + seedOffset;
    RooMsgService::instance().setGlobalKillBelow(RooFit::WARNING);

    //
    // run the code
    //

    runSigSepWWSingle(higgsMass, intLumi, nToys, test, MLLMT, pure, draw, seed);  
}

void runSigSepWWSingle(int higgsMass, double intLumi, int nToys,  const TestType test, int var, int toy, bool draw, const unsigned int seed) {

    // location of data
    // for ucsd batch submission
    const char *dataLocation = "root://xrootd.unl.edu//store/user/yygao/HWWAngular/datafiles/";
    // for local tests
    // const char *dataLocation = "datafiles/";
    

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
    
    RooArgSet* obs;

    if ( var == DPHI )
      obs = new RooArgSet(*dphill) ;
    
    if ( var == MLL ) 
      obs = new RooArgSet(*mll) ;
    
    if ( var == MLLMT ) 
      obs = new RooArgSet(*mll, *mt) ;

    if ( var == DPHIMT ) 
      obs = new RooArgSet(*dphill, *mt) ;

    //
    // read signal hypothesis 1 always SMHiggs
    // 
    TChain *tsigHyp1 = new TChain("angles");
    tsigHyp1->Add(Form("%s/%i/SMHiggsWW_%i_JHU.root", dataLocation, higgsMass, higgsMass));
    
    RooDataSet *sigHyp1Data = new RooDataSet("sigHyp1Data","sigHyp1Data",tsigHyp1,*obs);
    RooDataHist *sigHyp1Hist = sigHyp1Data->binnedClone(0);
    RooHistPdf* sigHyp1Pdf = new RooHistPdf("sigHyp1Pdf", "sigHyp1Pdf", *obs, *sigHyp1Hist);
      
    // read signal hypothesis 2
    TChain *tsigHyp2 = new TChain("angles");
    TString secondhypName = getSecondHypInputName(test, float(higgsMass));
    tsigHyp2->Add(Form("%s/%i/%s",dataLocation, higgsMass, secondhypName.Data()));
    
    std::cout << secondhypName << "\n";
    
    RooDataSet *sigHyp2Data = new RooDataSet("sigHyp2Data","sigHyp2Data",tsigHyp2,*obs);
    RooDataHist *sigHyp2Hist = sigHyp2Data->binnedClone(0);
    RooHistPdf* sigHyp2Pdf = new RooHistPdf("sigHyp2Pdf", "sigHyp2Pdf", *obs, *sigHyp2Hist);

    // read background
    TChain *bkgTree = new TChain("angles");
    bkgTree->Add(Form("%s/%i/WW_madgraph_8TeV.root",dataLocation,higgsMass));
    RooDataSet *bkgData = new RooDataSet("bkgData","bkgData",bkgTree,*obs);
    RooDataHist *bkgHist = bkgData->binnedClone(0);
    RooHistPdf* bkgPdf = new RooHistPdf("bkgPdf", "bkgPdf", *obs, *bkgHist);


    char statResults[50];
    statsFactory *myHypothesisSeparation;
    sprintf(statResults,"stat_%s_%s_%s_%.0ffb_%u.root",testName.Data(), toyName.Data(), varName.Data(), intLumi, seed);
    printf(statResults);
    myHypothesisSeparation = new statsFactory(obs, sigHyp1Pdf, sigHyp2Pdf, seed, statResults);
    // running pure toys
    myHypothesisSeparation->hypothesisSeparationWithBackground(sigRate*intLumi,sigRate*intLumi,nToys,bkgPdf,bkgRate*intLumi);
    delete myHypothesisSeparation;
    std::cout << "deleted myHypothesisSeparation" << std::endl;

    
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
      delete plot1;
      delete plot2;
    }

    // tidy up

    delete dphill;
    delete mt;
    delete mll;
    delete obs;
    delete tsigHyp1;
    delete sigHyp1Data;
    delete sigHyp1Pdf;
    delete tsigHyp2;
    delete sigHyp2Data;
    delete sigHyp2Pdf;
    delete bkgTree;
    delete bkgData;
    delete bkgPdf;
    delete myHypothesisSeparation;

}
