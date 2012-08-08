#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif

#include "RooDataSet.h"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "RooPlot.h"
#include "TROOT.h"
using namespace RooFit ;

void plotPdf_7D_XWW(double mH = 125, bool draw=true) {

    gROOT->ProcessLine(".L tdrstyle.C");
    setTDRStyle();
    TGaxis::SetMaxDigits(3);
    gROOT->ForceStyle();
    
    // Declaration of the PDFs to use
    gROOT->ProcessLine(".L  PDFs/RooSpinTwo_7D.cxx+");

    // W/Z mass and decay width constants
    double mV = 80.399;
    double gamV = 2.085;
    bool offshell = false;
    if ( mH < 2 * mV ) offshell = true;

    
    // for the pole mass and decay width of W 
    RooRealVar* mX = new RooRealVar("mX","mX", mH);
    RooRealVar* mW = new RooRealVar("mW","mW", mV);
    RooRealVar* gamW = new RooRealVar("gamW","gamW",gamV);

    //
    // Observables (7D)
    // 
    RooRealVar* wplusmass = new RooRealVar("wplusmass","m(W+)",mV,1e-09,120);
    wplusmass->setBins(50);
    RooRealVar* wminusmass = new RooRealVar("wminusmass","m(W-)",mV,1e-09,120);
    wminusmass->setBins(50);
    RooRealVar* hs = new RooRealVar("costhetastar","cos#theta*",-1,1);
    hs->setBins(20);
    RooRealVar* Phi1 = new RooRealVar("phistar1","#Phi_{1}",-TMath::Pi(),TMath::Pi());
    Phi1->setBins(20);
    RooRealVar* h1 = new RooRealVar("costheta1","cos#theta_{1}",-1,1);
    h1->setBins(20);
    RooRealVar* h2 = new RooRealVar("costheta2","cos#theta_{2}",-1,1);
    h2->setBins(20);
    RooRealVar* Phi = new RooRealVar("phi","#Phi",-TMath::Pi(),TMath::Pi());
    Phi->setBins(20);
    
    //
    // coupling constants for 2m+
    // See equation 5,6,7 in PRD 91, 075022
    //
    double s = (mH*mH-2*mV*mV)/2.;
    double c1 = 2*(1+mV*mV/s);
    c1 = c1 * 2.0; // scale up to be consistent with the generator
    // std::cout << "c1 = " << c1 << "\n"; 

    RooRealVar* c1Val = new RooRealVar("c1Val", "c1Val", c1);
    RooRealVar* c2Val = new RooRealVar("c2Val", "c2Val", -0.5);
    RooRealVar* c3Val = new RooRealVar("c3Val", "c3Val", 0.);
    RooRealVar* c4Val = new RooRealVar("c4Val", "c4Val", -1.);
    RooRealVar* c5Val = new RooRealVar("c5Val", "c5Val", 0.);
    RooRealVar* c6Val = new RooRealVar("c6Val", "c6Val", 0.);
    RooRealVar* c7Val = new RooRealVar("c7Val", "c7Val", 0.);
    
    // 
    // Alternative definition in terms of g1->g10
    // 
    RooRealVar* useGTerm = new RooRealVar("useGTerm", "useGTerm",1.); // set to 1 if using g couplings
    RooRealVar* g1Val = new RooRealVar("g1Val", "g1Val", 1);
    RooRealVar* g2Val = new RooRealVar("g2Val", "g2Val", 0.);
    RooRealVar* g3Val = new RooRealVar("g3Val", "g3Val", 0.);
    RooRealVar* g4Val = new RooRealVar("g4Val", "g4Val", 0.);
    RooRealVar* g5Val = new RooRealVar("g5Val", "g5Val", 1.);
    RooRealVar* g6Val = new RooRealVar("g6Val", "g6Val", 0.);
    RooRealVar* g7Val = new RooRealVar("g7Val", "g7Val", 0.);
    RooRealVar* g8Val = new RooRealVar("g8Val", "g8Val", 0.);
    RooRealVar* g9Val = new RooRealVar("g9Val", "g9Val", 0.);
    RooRealVar* g10Val = new RooRealVar("g10Val", "g10Val", 0.);

    // related to the gg/qq productions 
    RooRealVar* fz1Val = new RooRealVar("fz1Val", "fz1Val", 0);
    RooRealVar* fz2Val = new RooRealVar("fz2Val", "fz2Val", 1.0);

    // Even more parameters, do not have to touch, based on Z couplings
    RooRealVar* R1Val = new RooRealVar("R1Val","R1Val",1);
    RooRealVar* R2Val = new RooRealVar("R2Val","R2Val",1);
    
      
    // PDF definition SM Higgs (JP = 2+)
    RooSpinTwo_7D *myPDF;
    if ( offshell )
      myPDF = new RooSpinTwo_7D("myPDF","myPDF", *mX, *wplusmass, *wminusmass, *hs, *h1,*h2, *Phi, *Phi1, 
				  *c1Val, *c2Val, *c3Val, *c4Val, *c5Val, *c6Val, *c7Val, 
				  *useGTerm, *g1Val, *g2Val, *g3Val, *g4Val, *g5Val, *g6Val, *g7Val, *g8Val, *g9Val, *g10Val,
				  *fz1Val, *fz2Val, *R1Val, *R2Val, *mW, *gamW);
    else 
      myPDF = new RooSpinTwo_7D("myPDF","myPDF", *mX, *mW, *mW, *hs, *h1,*h2, *Phi, *Phi1, 
				  *c1Val, *c2Val, *c3Val, *c4Val, *c5Val, *c6Val, *c7Val, 
				  *useGTerm, *g1Val, *g2Val, *g3Val, *g4Val, *g5Val, *g6Val, *g7Val, *g8Val, *g9Val, *g10Val,
				  *fz1Val, *fz2Val, *R1Val, *R2Val, *mW, *gamW);
    // dataset for (JP = 2+)
    TString fileName;
    if ( useGTerm->getVal() > 0.) {
      fileName = Form("TWW_2mplus_%.0f_JHU.root", mH);
    }
    else {
      fileName = Form("TWW_%.0f_JHU_GenFromC.root", mH);
    }
    std::cout << "Opening " << fileName << "\n";
    TFile* fin = new TFile(fileName);
    TTree* tin = (TTree*) fin->Get("angles");

    if ( offshell) 
      RooDataSet data("data","data",tin,RooArgSet(*wplusmass, *wminusmass, *hs, *h1, *h2, *Phi, *Phi1));
    else 
      RooDataSet data("data","data",tin,RooArgSet(*hs, *h1, *h2, *Phi, *Phi1));

    // 
    //  2h-
    // 
    RooRealVar* g1ValMinus = new RooRealVar("g1ValMinus", "g1ValMinus", 0);
    RooRealVar* g2ValMinus = new RooRealVar("g2ValMinus", "g2ValMinus", 0.);
    RooRealVar* g3ValMinus = new RooRealVar("g3ValMinus", "g3ValMinus", 0.);
    RooRealVar* g4ValMinus = new RooRealVar("g4ValMinus", "g4ValMinus", 0.);
    RooRealVar* g5ValMinus = new RooRealVar("g5ValMinus", "g5ValMinus", 0.);
    RooRealVar* g6ValMinus = new RooRealVar("g6ValMinus", "g6ValMinus", 0.);
    RooRealVar* g7ValMinus = new RooRealVar("g7ValMinus", "g7ValMinus", 0.);
    RooRealVar* g8ValMinus = new RooRealVar("g8ValMinus", "g8ValMinus", 1.);
    RooRealVar* g9ValMinus = new RooRealVar("g9ValMinus", "g9ValMinus", 0.);
    RooRealVar* g10ValMinus = new RooRealVar("g10ValMinus", "g10ValMinus", 0.);
    RooRealVar* fz1ValMinus = new RooRealVar("fz1ValMinus", "fz1ValMinus", 0.0);
    RooRealVar* fz2ValMinus = new RooRealVar("fz2ValMinus", "fz2ValMinus", 0.0);

    RooSpinTwo_7D *myPDFMinus;
    if ( offshell )
      myPDFMinus = new RooSpinTwo_7D("myPDFMinus","myPDFMinus", *mX, *wplusmass, *wminusmass, *hs, *h1,*h2, *Phi, *Phi1, 
				       *c1Val, *c2Val, *c3Val, *c4Val, *c5Val, *c6Val, *c7Val, 
				       *useGTerm, *g1ValMinus, *g2ValMinus, *g3ValMinus, *g4ValMinus, 
				       *g5ValMinus, *g6ValMinus, *g7ValMinus, *g8ValMinus, *g9ValMinus, *g10ValMinus,
				       *fz1ValMinus, *fz2ValMinus, *R1Val, *R2Val, *mW, *gamW);
    else 
      myPDFMinus = new RooSpinTwo_7D("myPDFMinus","myPDFMinus", *mX, *mW, *mW, *hs, *h1,*h2, *Phi, *Phi1, 
				       *c1Val, *c2Val, *c3Val, *c4Val, *c5Val, *c6Val, *c7Val, 
				       *useGTerm, *g1ValMinus, *g2ValMinus, *g3ValMinus, *g4ValMinus, 
				       *g5ValMinus, *g6ValMinus, *g7ValMinus, *g8ValMinus, *g9ValMinus, *g10ValMinus,
				       *fz1ValMinus, *fz2ValMinus, *R1Val, *R2Val, *mW, *gamW);

    // dataset for (JP = 2-)
    TString fileNameMinus;
    if ( useGTerm->getVal() > 0.) {
      fileNameMinus = Form("TWW_2hminus_%.0f_JHU.root", mH);
    }
    
    std::cout << "Opening " << fileNameMinus << "\n";
    TFile* finMinus = new TFile(fileNameMinus);
    TTree* tinMinus = (TTree*) finMinus->Get("angles");

    if ( offshell) 
      RooDataSet dataMinus("dataMinus","dataMinus",tinMinus,RooArgSet(*wplusmass, *wminusmass, *hs, *h1, *h2, *Phi, *Phi1));
    else 
      RooDataSet dataMinus("dataMinus","dataMinus",tinMinus,RooArgSet(*hs, *h1, *h2, *Phi, *Phi1));

    // 
    //  2h+
    // 
    RooRealVar* g1ValHPlus = new RooRealVar("g1ValHPlus", "g1ValHPlus", 0);
    RooRealVar* g2ValHPlus = new RooRealVar("g2ValHPlus", "g2ValHPlus", 0.);
    RooRealVar* g3ValHPlus = new RooRealVar("g3ValHPlus", "g3ValHPlus", 0.);
    RooRealVar* g4ValHPlus = new RooRealVar("g4ValHPlus", "g4ValHPlus", 1.);
    RooRealVar* g5ValHPlus = new RooRealVar("g5ValHPlus", "g5ValHPlus", 0.);
    RooRealVar* g6ValHPlus = new RooRealVar("g6ValHPlus", "g6ValHPlus", 0.);
    RooRealVar* g7ValHPlus = new RooRealVar("g7ValHPlus", "g7ValHPlus", 0.);
    RooRealVar* g8ValHPlus = new RooRealVar("g8ValHPlus", "g8ValHPlus", 0.);
    RooRealVar* g9ValHPlus = new RooRealVar("g9ValHPlus", "g9ValHPlus", 0.);
    RooRealVar* g10ValHPlus = new RooRealVar("g10ValHPlus", "g10ValHPlus", 0.);
    RooRealVar* fz1ValHPlus = new RooRealVar("fz1ValHPlus", "fz1ValHPlus", 0.0);
    RooRealVar* fz2ValHPlus = new RooRealVar("fz2ValHPlus", "fz2ValHPlus", 0.0);

    RooSpinTwo_7D *myPDFHPlus;
    if ( offshell )
      myPDFHPlus = new RooSpinTwo_7D("myPDFHPlus","myPDFHPlus", *mX, *wplusmass, *wminusmass, *hs, *h1,*h2, *Phi, *Phi1, 
				       *c1Val, *c2Val, *c3Val, *c4Val, *c5Val, *c6Val, *c7Val, 
				       *useGTerm, *g1ValHPlus, *g2ValHPlus, *g3ValHPlus, *g4ValHPlus, 
				       *g5ValHPlus, *g6ValHPlus, *g7ValHPlus, *g8ValHPlus, *g9ValHPlus, *g10ValHPlus,
				       *fz1ValHPlus, *fz2ValHPlus, *R1Val, *R2Val, *mW, *gamW);
    else 
      myPDFHPlus = new RooSpinTwo_7D("myPDFHPlus","myPDFHPlus", *mX, *mW, *mW, *hs, *h1,*h2, *Phi, *Phi1, 
				       *c1Val, *c2Val, *c3Val, *c4Val, *c5Val, *c6Val, *c7Val, 
				       *useGTerm, *g1ValHPlus, *g2ValHPlus, *g3ValHPlus, *g4ValHPlus, 
				       *g5ValHPlus, *g6ValHPlus, *g7ValHPlus, *g8ValHPlus, *g9ValHPlus, *g10ValHPlus,
				       *fz1ValHPlus, *fz2ValHPlus, *R1Val, *R2Val, *mW, *gamW);
    TString fileNameHPlus;
    if ( useGTerm->getVal() > 0.) {
      fileNameHPlus = Form("TWW_2hplus_%.0f_JHU.root", mH);
    }
    
    std::cout << "Opening " << fileNameHPlus << "\n";
    TFile* finHPlus = new TFile(fileNameHPlus);
    TTree* tinHPlus = (TTree*) finHPlus->Get("angles");

    if ( offshell) 
      RooDataSet dataHPlus("dataHPlus","dataHPlus",tinHPlus,RooArgSet(*wplusmass, *wminusmass, *hs, *h1, *h2, *Phi, *Phi1));
    else 
      RooDataSet dataHPlus("dataHPlus","dataHPlus",tinHPlus,RooArgSet(*hs, *h1, *h2, *Phi, *Phi1));



    
    // P L O T   . . .  
    // (All parameters fixed, no fitting, just looking at the shape of the PDFs w.r.t. the data)
    if ( draw ) {

      bool drawmplus = true;
      bool drawhminus = true;
      bool drawhplus = true;
      bool drawpaper = true;
      double rescale = 1.0;
      if ( drawpaper ) 
	rescale = .001;

      TH1F* dum0 = new TH1F("dum0","dum0",1,0,1); dum0->SetLineColor(kRed); dum0->SetMarkerColor(kBlack); dum0->SetLineWidth(3);
      TH1F* dum1 = new TH1F("dum1","dum1",1,0,1); dum1->SetLineColor(kBlue); dum1->SetMarkerColor(kBlack); dum1->SetMarkerStyle(24), dum1->SetLineWidth(3);  
      TH1F* dum2 = new TH1F("dum2","dum2",1,0,1); dum2->SetLineColor(kGreen); dum2->SetMarkerColor(kBlack); dum2->SetMarkerStyle(21), dum2->SetLineWidth(3); // 2L+
      
      TLegend * box3 = new TLegend(0.1,0.1,0.9,0.92);
      box3->SetFillColor(0);
      box3->SetBorderSize(0);

      if ( drawmplus ) 
	box3->AddEntry(dum0,Form("X(%.0f)#rightarrow WW JP = 2m+", mH),"lp");
      if ( drawhminus )
	box3->AddEntry(dum1,Form("X(%.0f)#rightarrow WW JP = 2h-", mH),"lp");
      if ( drawhplus ) 
	box3->AddEntry(dum2,Form("X(%.0f)#rightarrow WW JP = 2h+,", mH),"lp");
  
      
      // 
      //  h1
      // 
      RooPlot* h1frame =  h1->frame(20);
      h1frame->GetXaxis()->CenterTitle();
      h1frame->GetYaxis()->CenterTitle();
      h1frame->GetYaxis()->SetTitle(" ");
      
      double ymax_h1;
      TH1F *h1_mplus = new TH1F("h1_mplus", "h1_mplus", 20, -1, 1);
      tin->Project("h1_mplus", "costheta1");
      ymax_h1 = h1_mplus->GetMaximum();
      
      TH1F *h1_hminus = new TH1F("h1_hminus", "h1_hminus", 20, -1, 1);
      tinMinus->Project("h1_hminus", "costheta1");
      ymax_h1 = h1_hminus->GetMaximum() > ymax_h1 ? h1_hminus->GetMaximum() : ymax_h1;
      
      TH1F *h1_hplus = new TH1F("h1_hplus", "h1_hplus", 20, -1, 1);
      tinHPlus->Project("h1_hplus", "costheta1");
      ymax_h1 = h1_hplus->GetMaximum() > ymax_h1 ? h1_hplus->GetMaximum() : ymax_h1;
      
      if ( drawmplus ) {
	data.plotOn(h1frame, MarkerColor(kRed),MarkerStyle(4),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
	myPDF->plotOn(h1frame, LineColor(kRed),LineWidth(2), Normalization(rescale));
      }
      if ( drawhminus ) {
	dataMinus.plotOn(h1frame, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
	myPDFMinus->plotOn(h1frame, LineColor(kBlue),LineWidth(2), Normalization(rescale));
      }
      if ( drawhplus ) {
	dataHPlus.plotOn(h1frame, MarkerColor(kGreen+3),MarkerStyle(25),MarkerSize(1.5),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
	myPDFHPlus->plotOn(h1frame, LineColor(kGreen+3),LineWidth(2), Normalization(rescale));
      }
      if ( rescale != 1. )
	h1frame->GetYaxis()->SetRangeUser(0, ymax_h1  * rescale * 1.3);
      
      
      // 
      //  h2
      // 
      
      RooPlot* h2frame =  h2->frame(20);
      h2frame->GetXaxis()->CenterTitle();
      h2frame->GetYaxis()->CenterTitle();
      h2frame->GetYaxis()->SetTitle(" ");
      
      double ymax_h2;
      TH1F *h2_mplus = new TH1F("h2_mplus", "h2_mplus", 20, -1, 1);
      tin->Project("h2_mplus", "costheta2");
      ymax_h2 = h2_mplus->GetMaximum();
      
      TH1F *h2_hminus = new TH1F("h2_hminus", "h2_hminus", 20, -1, 1);
      tinMinus->Project("h2_hminus", "costheta2");
      ymax_h2 = h2_hminus->GetMaximum() > ymax_h2 ? h2_hminus->GetMaximum() : ymax_h2;
      
      TH1F *h2_hplus = new TH1F("h2_hplus", "h2_hplus", 20, -1, 1);
      tinHPlus->Project("h2_hplus", "costheta2");
      ymax_h2 = h2_hplus->GetMaximum() > ymax_h2 ? h2_hplus->GetMaximum() : ymax_h2;
      
      
      if ( drawmplus ) {
	data.plotOn(h2frame, MarkerColor(kRed),MarkerStyle(4),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
	myPDF->plotOn(h2frame, LineColor(kRed),LineWidth(2), Normalization(rescale));
      }
      if ( drawhminus ) {
	dataMinus.plotOn(h2frame, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
	myPDFMinus->plotOn(h2frame, LineColor(kBlue),LineWidth(2), Normalization(rescale));
      }
      if ( drawhplus ) {
	dataHPlus.plotOn(h2frame, MarkerColor(kGreen+3),MarkerStyle(25),MarkerSize(1.5),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
	myPDFHPlus->plotOn(h1frame, LineColor(kGreen+3),LineWidth(2), Normalization(rescale));
      }
      if ( rescale != 1. ) 
	h2frame->GetYaxis()->SetRangeUser(0, ymax_h2  * rescale * 1.3);
      
      //
      // Phi
      // 
      RooPlot* Phiframe =  Phi->frame(20);
      
      Phiframe->GetXaxis()->CenterTitle();
      Phiframe->GetYaxis()->CenterTitle();
      Phiframe->GetYaxis()->SetTitle(" ");
      
      double ymax_Phi;
      TH1F *Phi_mplus = new TH1F("Phi_mplus", "Phi_mplus", 20,  -TMath::Pi(), TMath::Pi());
      tin->Project("Phi_mplus", "phi");
      ymax_Phi = Phi_mplus->GetMaximum();
      
      TH1F *Phi_hminus = new TH1F("Phi_hminus", "Phi_hminus", 20,  -TMath::Pi(), TMath::Pi());
      tinMinus->Project("Phi_hminus", "phi");
      ymax_Phi = Phi_hminus->GetMaximum() > ymax_Phi ? Phi_hminus->GetMaximum() : ymax_Phi;
      
      TH1F *Phi_hplus = new TH1F("Phi_hplus", "Phi_hplus", 20,  -TMath::Pi(), TMath::Pi());
      tinHPlus->Project("Phi_hplus", "phi");
      ymax_Phi = Phi_hplus->GetMaximum() > ymax_Phi ? Phi_hplus->GetMaximum() : ymax_Phi;
      
      if ( drawmplus ) {
	data.plotOn(Phiframe, MarkerColor(kRed),MarkerStyle(4),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
	myPDF->plotOn(Phiframe, LineColor(kRed),LineWidth(2), Normalization(rescale));
      }
      if ( drawhminus ) {
	dataMinus.plotOn(Phiframe, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
	myPDFMinus->plotOn(Phiframe, LineColor(kBlue),LineWidth(2), Normalization(rescale));
      }
      if ( drawhplus ) {
	dataHPlus.plotOn(Phiframe, MarkerColor(kGreen+3),MarkerStyle(25),MarkerSize(1.5),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
	myPDFHPlus->plotOn(Phiframe, LineColor(kGreen+3),LineWidth(2), Normalization(rescale));
      }
      if ( rescale != 1. ) 
	Phiframe->GetYaxis()->SetRangeUser(0, ymax_Phi  * rescale * 1.3);
      
      // 
      //  hs 
      // 
      RooPlot* hsframe =  hs->frame(20);
      
      hsframe->GetXaxis()->CenterTitle();
      hsframe->GetYaxis()->CenterTitle();
      hsframe->GetYaxis()->SetTitle(" ");
      
      double ymax_hs;
      TH1F *hs_mplus = new TH1F("hs_mplus", "hs_mplus", 20, -1, 1);
      tin->Project("hs_mplus", "costhetastar");
      ymax_hs = hs_mplus->GetMaximum();
      
      TH1F *hs_hminus = new TH1F("hs_hminus", "hs_hminus", 20, -1, 1);
      tinMinus->Project("hs_hminus", "costhetastar");
      ymax_hs = hs_hminus->GetMaximum() > ymax_hs ? hs_hminus->GetMaximum() : ymax_hs;
      
      TH1F *hs_hplus = new TH1F("hs_hplus", "hs_hplus", 20, -1, 1);
      tinHPlus->Project("hs_hplus", "costhetastar");
      ymax_hs = hs_hplus->GetMaximum() > ymax_hs ? hs_hplus->GetMaximum() : ymax_hs;
      
      if ( drawmplus ) {
	data.plotOn(hsframe, MarkerColor(kRed),MarkerStyle(4),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
	myPDF->plotOn(hsframe, LineColor(kRed),LineWidth(2), Normalization(rescale));
      }
      if ( drawhminus ) {
	dataMinus.plotOn(hsframe, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
	myPDFMinus->plotOn(hsframe, LineColor(kBlue),LineWidth(2), Normalization(rescale));
      }
      if ( drawhplus ) {
	dataHPlus.plotOn(hsframe, MarkerColor(kGreen+3),MarkerStyle(25),MarkerSize(1.5),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
	myPDFHPlus->plotOn(hsframe, LineColor(kGreen+3),LineWidth(2), Normalization(rescale));
      }
      if ( rescale != 1. )
	hsframe->GetYaxis()->SetRangeUser(0, ymax_hs  * rescale * 1.3);
      
      
      //
      // Phi1
      // 
      RooPlot* Phi1frame =  Phi1->frame(20);
      
      Phi1frame->GetXaxis()->CenterTitle();
      Phi1frame->GetYaxis()->CenterTitle();
      Phi1frame->GetYaxis()->SetTitle(" ");
      
      double ymax_Phi1;
      TH1F *Phi1_mplus = new TH1F("Phi1_mplus", "Phi1_mplus", 20, -TMath::Pi(), TMath::Pi());
      tin->Project("Phi1_mplus", "phistar1");
      ymax_Phi1 = Phi1_mplus->GetMaximum();
      
      TH1F *Phi1_hminus = new TH1F("Phi1_hminus", "Phi1_hminus", 20, -TMath::Pi(), TMath::Pi());
      tinMinus->Project("Phi1_hminus", "phistar1");
      ymax_Phi1 = Phi1_hminus->GetMaximum() > ymax_Phi1 ? Phi1_hminus->GetMaximum() : ymax_Phi1;
      
      TH1F *Phi1_hplus = new TH1F("Phi1_hplus", "Phi1_hplus", 20, -TMath::Pi(), TMath::Pi());
      tinHPlus->Project("Phi1_hplus", "phistar1");
      ymax_Phi1 = Phi1_hplus->GetMaximum() > ymax_Phi1 ? Phi1_hplus->GetMaximum() : ymax_Phi1;
      
      if ( drawmplus ) {
	data.plotOn(Phi1frame, MarkerColor(kRed),MarkerStyle(4),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
	myPDF->plotOn(Phi1frame, LineColor(kRed),LineWidth(2), Normalization(rescale));
      }
      if ( drawhminus ) {
	dataMinus.plotOn(Phi1frame, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
	myPDFMinus->plotOn(Phi1frame, LineColor(kBlue),LineWidth(2), Normalization(rescale));
      }
      if ( drawhplus ) {
	dataHPlus.plotOn(Phi1frame, MarkerColor(kGreen+3),MarkerStyle(25),MarkerSize(1.5),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
	myPDFHPlus->plotOn(Phi1frame, LineColor(kGreen+3),LineWidth(2), Normalization(rescale));
      }
      if ( rescale != 1. ) 
	Phi1frame->GetYaxis()->SetRangeUser(0, ymax_Phi1  * rescale * 1.3);
      
      
      
      if ( offshell ) {
	RooPlot* w1frame =  wplusmass->frame(50);
	w1frame->GetXaxis()->CenterTitle();
	w1frame->GetYaxis()->CenterTitle();
	w1frame->GetYaxis()->SetTitle(" ");
	
	double ymax_w1;
	TH1F *w1_mplus = new TH1F("w1_mplus", "w1_mplus", 50, 1e-09, 120);
	tin->Project("w1_mplus", "wplusmass");
	ymax_w1 = w1_mplus->GetMaximum();
	
	TH1F *w1_hminus = new TH1F("w1_hminus", "w1_hminus", 50, 1e-09, 120);
	tinMinus->Project("w1_hminus", "wplusmass");
	ymax_w1 = w1_hminus->GetMaximum() > ymax_w1 ? w1_hminus->GetMaximum() : ymax_w1;
	
	TH1F *w1_hplus = new TH1F("w1_hplus", "w1_hplus", 50, 1e-09, 120);
	tinHPlus->Project("w1_hplus", "wplusmass");
	ymax_w1 = w1_hplus->GetMaximum() > ymax_w1 ? w1_hplus->GetMaximum() : ymax_w1;
	
	if ( drawmplus ) {
	  data.plotOn(w1frame, MarkerColor(kRed),MarkerStyle(4),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
	  myPDF->plotOn(w1frame, LineColor(kRed),LineWidth(2), Normalization(rescale));
	}
	if ( drawhminus ) {
	  dataMinus.plotOn(w1frame, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
	  myPDFMinus->plotOn(w1frame, LineColor(kBlue),LineWidth(2), Normalization(rescale));
	}
	if ( drawhplus ) {
	  dataHPlus.plotOn(w1frame, MarkerColor(kGreen+3),MarkerStyle(25),MarkerSize(1.5),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
	  myPDFHPlus->plotOn(w1frame, LineColor(kGreen+3),LineWidth(2), Normalization(rescale));
	}
	if ( rescale != 1. ) 
	  w1frame->GetYaxis()->SetRangeUser(0, ymax_w1  * rescale * 1.5);
	
	// 
	//  wminus
	// 
	RooPlot* w2frame =  wminusmass->frame(50);
	
	w2frame->GetXaxis()->CenterTitle();
	w2frame->GetYaxis()->CenterTitle();
	w2frame->GetYaxis()->SetTitle(" ");
	
	double ymax_w2;
	TH1F *w2_mplus = new TH1F("w2_mplus", "w2_mplus", 50, 1e-09, 120);
	tin->Project("w2_mplus", "wminusmass");
	ymax_w2 = w2_mplus->GetMaximum();
	
	TH1F *w2_hminus = new TH1F("w2_hminus", "w2_hminus", 50, 1e-09, 120);
	tinMinus->Project("w2_hminus", "wminusmass");
	ymax_w2 = w2_hminus->GetMaximum() > ymax_w2 ? w2_hminus->GetMaximum() : ymax_w2;
	
	TH1F *w2_hplus = new TH1F("w2_hplus", "w2_hplus", 50, 1e-09, 120);
	tinHPlus->Project("w2_hplus", "wminusmass");
	ymax_w2 = w2_hplus->GetMaximum() > ymax_w2 ? w2_hplus->GetMaximum() : ymax_w2;
	
	if ( drawmplus ) {
	  data.plotOn(w2frame, MarkerColor(kRed),MarkerStyle(4),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
	  myPDF->plotOn(w2frame, LineColor(kRed),LineWidth(2), Normalization(rescale));
	}
	if ( drawhminus ) {
	  dataMinus.plotOn(w2frame, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
	  myPDFMinus->plotOn(w2frame, LineColor(kBlue),LineWidth(2), Normalization(rescale));
	}
	if ( drawhplus ) {
	  dataHPlus.plotOn(w2frame, MarkerColor(kGreen+3),MarkerStyle(25),MarkerSize(1.5),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
	  myPDFHPlus->plotOn(w2frame, LineColor(kGreen+3),LineWidth(2), Normalization(rescale));
	}
	if ( rescale != 1. ) 
	  w2frame->GetYaxis()->SetRangeUser(0, ymax_w2  * rescale * 1.5);
      }
    }
    if ( drawpaper ) {
      TCanvas* can =new TCanvas("can","can",600,600);
      
      if ( offshell ) {
	w1frame->GetXaxis()->SetTitle("m_{l#nu} [GeV]");
	w1frame->Draw();
	can->Print(Form("paperplots/wplusmass_%.0fGeV_spin2_3in1_ww.eps", mH));
	can->SaveAs(Form("paperplots/wplusmass_%.0fGeV_spin2_3in1_ww.C", mH));
      }
      
      can->Clear();
      hsframe->Draw();
      can->Print(Form("paperplots/costhetastar_%.0fGeV_spin2_3in1_ww.eps", mH));      
      can->SaveAs(Form("paperplots/costhetastar_%.0fGeV_spin2_3in1_ww.C", mH));      
      
      can->Clear();
      Phi1frame->Draw();
      can->Print(Form("paperplots/phistar1_%.0fGeV_spin2_3in1_ww.eps", mH));      
      can->SaveAs(Form("paperplots/phistar1_%.0fGeV_spin2_3in1_ww.C", mH));      

      can->Clear();
      h1frame->GetXaxis()->SetTitle("cos#theta_{1} or cos#theta_{2}");
      h1frame->Draw();
      can->Print(Form("paperplots/costheta1_%.0fGeV_spin2_3in1_ww.eps", mH));
      can->SaveAs(Form("paperplots/costheta1_%.0fGeV_spin2_3in1_ww.C", mH));

      can->Clear();
      Phiframe->Draw();
      can->Print(Form("paperplots/phi_%.0fGeV_spin2_3in1_ww.eps", mH));      
      can->SaveAs(Form("paperplots/phi_%.0fGeV_spin2_3in1_ww.C", mH));      

      }      else {
      
      TCanvas* czz = new TCanvas( "czz", "czz", 1000, 600 );
      czz->Divide(4,2);
      
      if ( offshell ) {
	czz->cd(1);
	w1frame->Draw();
	
	czz->cd(2);
	w2frame->Draw();
      }
      
      czz->cd(3);
      hsframe->Draw();
      
      czz->cd(4);
      box3->Draw();
      
      czz->cd(5);
      Phi1frame->Draw();
      
      czz->cd(6);
      h1frame->Draw();
      
      czz->cd(7);
      h2frame->Draw();
      
      czz->cd(8);
      Phiframe->Draw();
      
      if ( useGTerm->getVal() > 0.) {
	czz->SaveAs(Form("epsfiles/angles_TWW%.0f_JHU_7D.eps", mH));
	czz->SaveAs(Form("pngfiles/angles_TWW%.0f_JHU_7D.png", mH));
      } else {
	czz->SaveAs(Form("epsfiles/angles_TWW%.0f_JHU_7D_GenFromC.eps", mH));
	czz->SaveAs(Form("pngfiles/angles_TWW%.0f_JHU_7D_GenFromC.png", mH));
      }
    }
}
