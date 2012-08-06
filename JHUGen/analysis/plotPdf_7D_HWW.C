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
using namespace RooFit ;

void plotPdf_7D_HWW(float mH = 125) {
  
    gROOT->ProcessLine(".L ~/tdrstyle.C");
    setTDRStyle();
    gStyle->SetPadLeftMargin(0.06);
    gStyle->SetPadBottomMargin(0.15);
    gStyle->SetTitleXOffset(1.1);
    TGaxis::SetMaxDigits(3);
    gROOT->ForceStyle();
    
    // Declaration of the PDFs to use
    gROOT->ProcessLine(".L PDFs/RooSpinZero_7D.cxx+");

    // W/Z mass and decay width constants
    double mV = 80.399;
    double gamV = 2.085;
    bool offshell = false;
    if ( mH < 2 * mV ) offshell = true;

    // Observables (5D)
    RooRealVar* m1 = new RooRealVar("wplusmass","m(W+)",1e-09,120);
    m1->setBins(50);
    RooRealVar* m2 = new RooRealVar("wminusmass","m(W-)",1e-09,120);
    m2->setBins(50);
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
    RooRealVar* wt = new RooRealVar("wt", "wt", 0.0, 10);
    
    
    // Parameters
    RooRealVar* mW = new RooRealVar("mW","mW",80.398);
    RooRealVar* mX = new RooRealVar("mX","mX",mH);
    RooRealVar* gamW = new RooRealVar("gamW","gamW",2.1);
    // More parameters, these are the couplings "a1","a2","a3" which are _complex_ (which is why there are phases "phi*Val")
    RooRealVar* a1Val = new RooRealVar("a1Val","a1Val",1);
    RooRealVar* phi1Val = new RooRealVar("phi1Val","phi1Val", 0);
    RooRealVar* a2Val = new RooRealVar("a2Val","a2Val",0);
    RooRealVar* phi2Val = new RooRealVar("phi2Val","phi2Val", 0);
    RooRealVar* a3Val = new RooRealVar("a3Val","a3Val",0);
    RooRealVar* phi3Val = new RooRealVar("phi3Val","phi3Val",0);
    
    //
    // alternative defintions in terms of the g1->g4
    // 
    RooRealVar* useGTerm = new RooRealVar("useGTerm", "useGTerm",1.); // set to 1 if using g coupling
    RooRealVar* g1Val = new RooRealVar("g1Val", "g1Val", 1);
    RooRealVar* g2Val = new RooRealVar("g2Val", "g2Val", 0.);
    RooRealVar* g3Val = new RooRealVar("g3Val", "g3Val", 0.);
    RooRealVar* g4Val = new RooRealVar("g4Val", "g4Val", 0.);
    
    // Even more parameters, do not have to touch, based on W couplings
    RooRealVar* R1Val = new RooRealVar("R1Val","R1Val",1);
    RooRealVar* R2Val = new RooRealVar("R2Val","R2Val",1);
    
    // PDF definition SM Higgs (JP = 0+)
    RooSpinZero_7D *myPDF;
    if ( offshell ) 
      myPDF = new RooSpinZero_7D("myPDF","myPDF",*m1,*m2,*h1,*h2,*hs,*Phi,*Phi1,
				     *a1Val,*phi1Val,*a2Val,*phi2Val,*a3Val,*phi3Val,
				     *useGTerm, *g1Val, *g2Val, *g3Val, *g4Val,
				     *mW,*gamW,*mX,*R1Val,*R2Val);
    else 
      myPDF = new RooSpinZero_7D("myPDF","myPDF",*mW,*mW,*h1,*h2,*hs,*Phi,*Phi1,
				     *a1Val,*phi1Val,*a2Val,*phi2Val,*a3Val,*phi3Val,
				     *useGTerm, *g1Val, *g2Val, *g3Val, *g4Val,
				     *mW,*gamW,*mX,*R1Val,*R2Val);

    // Grab input file to convert to RooDataSet
    TFile* fin = new TFile(Form("SMHiggsWW_%.0f_JHU.root", mH));
    TTree* tin = (TTree*) fin->Get("angles");
    
    // for weighted events
    if ( offshell ) 
      RooDataSet data("data","data",tin,RooArgSet(*m1,*m2,*h1,*h2,*hs,*Phi,*Phi1));
    else 
      RooDataSet data("data","data",tin,RooArgSet(*h1,*h2,*hs,*Phi,*Phi1));
    
    // 
    //  0-
    // 
    
    // PDF definition Pseudoscalar Higgs (JP = 0-)
    RooRealVar* a1Valp = new RooRealVar("a1Valp","a1Valp",0);
    RooRealVar* a3Valp = new RooRealVar("a3Valp","a3Valp",1);
    RooRealVar* g1Valp = new RooRealVar("g1Valp", "g1Valp", 0);
    RooRealVar* g2Valp = new RooRealVar("g2Valp", "g2Valp", 0.);
    RooRealVar* g3Valp = new RooRealVar("g3Valp", "g3Valp", 0.);
    RooRealVar* g4Valp = new RooRealVar("g4Valp", "g4Valp", 1.);

    RooSpinZero_7D *myPDFA;
    if ( offshell ) 
      myPDFA = new RooSpinZero_7D("myPDFA","myPDFA",*m1,*m2,*h1,*h2,*hs,*Phi,*Phi1,
				      *a1Valp,*phi1Val,*a2Val,*phi2Val,*a3Valp,*phi3Val,
				      *useGTerm, *g1Valp, *g2Valp, *g3Valp, *g4Valp,
				      *mW,*gamW,*mX,*R1Val,*R2Val);
    else
      myPDFA = new RooSpinZero_7D("myPDFA","myPDFA",*mW,*mW,*h1,*h2,*hs,*Phi,*Phi1,
				      *a1Valp,*phi1Val,*a2Val,*phi2Val,*a3Valp,*phi3Val,
				      *useGTerm, *g1Valp, *g2Valp, *g3Valp, *g4Valp,
				      *mW,*gamW,*mX,*R1Val,*R2Val);


    // read another input file
    TFile* fin2 = new TFile(Form("PSHiggsWW_%.0f_JHU.root", mH));
    TTree* tin2 = (TTree*) fin2->Get("angles");
    
    if ( offshell ) 
      RooDataSet data2("data2","data2",tin2,RooArgSet(*m1,*m2,*h1,*h2,*hs,*Phi,*Phi1));
    else 
      RooDataSet data2("data2","data2",tin2,RooArgSet(*h1,*h2,*hs,*Phi,*Phi1));
    
    // 
    // For 0h+
    // only implemented the g-couplings since the a-couplings are mass-dependent
    // 

    // PDF definition Pseudoscalar Higgs (JP = 0-)
    RooRealVar* a1Valhp = new RooRealVar("a1Valhp","a1Valhp",0); // meaningless
    RooRealVar* a2Valhp = new RooRealVar("a2Valhp","a2Valhp",1.); // meaningless
    RooRealVar* a3Valhp = new RooRealVar("a3Valhp","a3Valhp",0); // meaningless
    RooRealVar* g1Valhp = new RooRealVar("g1Valhp", "g1Valhp", 0);
    RooRealVar* g2Valhp = new RooRealVar("g2Valhp", "g2Valhp", 1.);
    RooRealVar* g3Valhp = new RooRealVar("g3Valhp", "g3Valhp", 0.);
    RooRealVar* g4Valhp = new RooRealVar("g4Valhp", "g4Valhp", 0.);

    RooSpinZero_7D *myPDFHP; 
    if ( offshell ) 
      myPDFHP = new RooSpinZero_7D("myPDFHP","myPDFHP",*m1,*m2,*h1,*h2,*hs,*Phi,*Phi1,
				      *a1Valhp,*phi1Val,*a2Valhp,*phi2Val,*a3Valhp,*phi3Val,
				      *useGTerm, *g1Valhp, *g2Valhp, *g3Valhp, *g4Valhp,
				      *mW,*gamW,*mX,*R1Val,*R2Val);
    else 
      myPDFHP = new RooSpinZero_7D("myPDFHP","myPDFHP",*mW,*mW,*h1,*h2,*hs,*Phi,*Phi1,
				      *a1Valhp,*phi1Val,*a2Valhp,*phi2Val,*a3Valhp,*phi3Val,
				      *useGTerm, *g1Valhp, *g2Valhp, *g3Valhp, *g4Valhp,
				      *mW,*gamW,*mX,*R1Val,*R2Val);
    
    // read another input file
    // TFile* finhp = new TFile(Form("SMHiggsWW_0hplus_%.0f_JHU.root", mH));
    TFile* finhp = new TFile(Form("SMHiggsWW_0hplus_125_JHU.root", mH));
    TTree* tinhp = (TTree*) finhp->Get("angles");
    
    if ( offshell ) 
      RooDataSet datahp("datahp","datahp",tinhp,RooArgSet(*m1,*m2,*h1,*h2,*hs,*Phi,*Phi1));
    else 
      RooDataSet datahp("datahp","datahp",tinhp,RooArgSet(*h1,*h2,*hs,*Phi,*Phi1));
    

    // P L O T   . . . 
    bool drawsm = true;
    bool drawhminus = true;
    bool drawhplus = true;
    bool drawpaper = false;
    double rescale = 1.;
    if ( drawpaper ) rescale = .001;


    // (All parameters fixed, no fitting, just looking at the shape of the PDFs w.r.t. the data)
    TH1F* dum0 = new TH1F("dum0","dum0",1,0,1); dum0->SetLineColor(kRed); dum0->SetMarkerColor(kBlack); dum0->SetLineWidth(3);
    TH1F* dum1 = new TH1F("dum1","dum1",1,0,1); dum1->SetLineColor(kBlue); dum1->SetMarkerColor(kBlack); dum1->SetMarkerStyle(24), dum1->SetLineWidth(3);
    TH1F* dum2 = new TH1F("dum2","dum2",1,0,1); dum2->SetLineColor(kGreen); dum2->SetMarkerColor(kBlack); dum2->SetMarkerStyle(21), dum2->SetLineWidth(3);
    TLegend * box3 = new TLegend(0.1,0.1,0.9,0.92);
    box3->SetFillColor(0);
    box3->SetBorderSize(0);
    if ( drawsm ) 
      box3->AddEntry(dum0,Form("X(%.0f)#rightarrow WW: JP = 0+", mH),"lp");
    if ( drawhminus )
      box3->AddEntry(dum1,Form("X(%.0f)#rightarrow WW: JP = 0-", mH),"lp");
    if ( drawhplus ) 
      box3->AddEntry(dum2,Form("X(%.0f)#rightarrow WW: JP = 0h+", mH),"lp");
    
    // 
    //  h1
    // 
    RooPlot* h1frame =  h1->frame(20);
    h1frame->GetXaxis()->CenterTitle();
    h1frame->GetYaxis()->CenterTitle();
    h1frame->GetYaxis()->SetTitle(" ");

    double ymax_h1;
    TH1F *h1_sm = new TH1F("h1_sm", "h1_sm", 20, -1, 1);
    tin->Project("h1_sm", "costheta1");
    ymax_h1 = h1_sm->GetMaximum();

    TH1F *h1_hminus = new TH1F("h1_hminus", "h1_hminus", 20, -1, 1);
    tin2->Project("h1_hminus", "costheta1");
    ymax_h1 = h1_hminus->GetMaximum() > ymax_h1 ? h1_hminus->GetMaximum() : ymax_h1;

    TH1F *h1_hplus = new TH1F("h1_hplus", "h1_hplus", 20, -1, 1);
    tinhp->Project("h1_hplus", "costheta1");
    ymax_h1 = h1_hplus->GetMaximum() > ymax_h1 ? h1_hplus->GetMaximum() : ymax_h1;
    
    if ( drawsm ) {
      data.plotOn(h1frame, MarkerColor(kRed),MarkerStyle(4),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale));
      myPDF->plotOn(h1frame, LineColor(kRed),LineWidth(2), Normalization(rescale));
    }
    if ( drawhminus ) {
      data2.plotOn(h1frame, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale));
      myPDFA->plotOn(h1frame, LineColor(kBlue),LineWidth(2), Normalization(rescale));
    }
    if ( drawhplus ) {
      datahp.plotOn(h1frame, MarkerColor(kGreen+3),MarkerStyle(25),MarkerSize(1.5),XErrorSize(0), Rescale(rescale));
      myPDFHP->plotOn(h1frame, LineColor(kGreen+3),LineWidth(2), Normalization(rescale));
    }
    if ( rescale != 1.) 
      h1frame->GetYaxis()->SetRangeUser(0, ymax_h1 * rescale * 1.3);

    
    // 
    //  h2
    // 
    
    RooPlot* h2frame =  h2->frame(20);
    h2frame->GetXaxis()->CenterTitle();
    h2frame->GetYaxis()->CenterTitle();
    h2frame->GetYaxis()->SetTitle(" ");

    double ymax_h2;
    TH1F *h2_sm = new TH1F("h2_sm", "h2_sm", 20, -1, 1);
    tin->Project("h2_sm", "costheta2");
    ymax_h2 = h2_sm->GetMaximum();

    TH1F *h2_hminus = new TH1F("h2_hminus", "h2_hminus", 20, -1, 1);
    tin2->Project("h2_hminus", "costheta2");
    ymax_h2 = h2_hminus->GetMaximum() > ymax_h2 ? h2_hminus->GetMaximum() : ymax_h2;

    TH1F *h2_hplus = new TH1F("h2_hplus", "h2_hplus", 20, -1, 1);
    tinhp->Project("h2_hplus", "costheta2");
    ymax_h2 = h2_hplus->GetMaximum() > ymax_h2 ? h2_hplus->GetMaximum() : ymax_h2;


    if ( drawsm ) {
      data.plotOn(h2frame, MarkerColor(kRed),MarkerStyle(4),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale));
      myPDF->plotOn(h2frame, LineColor(kRed),LineWidth(2), Normalization(rescale));
    }
    if ( drawhminus ) {
      data2.plotOn(h2frame, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale));
      myPDFA->plotOn(h2frame, LineColor(kBlue),LineWidth(2), Normalization(rescale));
    }
    if ( drawhplus ) {
      datahp.plotOn(h2frame, MarkerColor(kGreen+3),MarkerStyle(25),MarkerSize(1.5),XErrorSize(0), Rescale(rescale));
      myPDFHP->plotOn(h1frame, LineColor(kGreen+3),LineWidth(2), Normalization(rescale));
    }
    if ( rescale != 1. ) 
      h2frame->GetYaxis()->SetRangeUser(0, ymax_h2 * rescale * 1.3);

    //
    // Phi
    // 
    RooPlot* Phiframe =  Phi->frame(20);
 
    Phiframe->GetXaxis()->CenterTitle();
    Phiframe->GetYaxis()->CenterTitle();
    Phiframe->GetYaxis()->SetTitle(" ");

    double ymax_Phi;
    TH1F *Phi_sm = new TH1F("Phi_sm", "Phi_sm", 20,  -TMath::Pi(), TMath::Pi());
    tin->Project("Phi_sm", "phi");
    ymax_Phi = Phi_sm->GetMaximum();

    TH1F *Phi_hminus = new TH1F("Phi_hminus", "Phi_hminus", 20,  -TMath::Pi(), TMath::Pi());
    tin2->Project("Phi_hminus", "phi");
    ymax_Phi = Phi_hminus->GetMaximum() > ymax_Phi ? Phi_hminus->GetMaximum() : ymax_Phi;

    TH1F *Phi_hplus = new TH1F("Phi_hplus", "Phi_hplus", 20,  -TMath::Pi(), TMath::Pi());
    tinhp->Project("Phi_hplus", "phi");
    ymax_Phi = Phi_hplus->GetMaximum() > ymax_Phi ? Phi_hplus->GetMaximum() : ymax_Phi;
    
    if ( drawsm ) {
      data.plotOn(Phiframe, MarkerColor(kRed),MarkerStyle(4),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale));
      myPDF->plotOn(Phiframe, LineColor(kRed),LineWidth(2), Normalization(rescale));
    }
    if ( drawhminus ) {
      data2.plotOn(Phiframe, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale));
      myPDFA->plotOn(Phiframe, LineColor(kBlue),LineWidth(2), Normalization(rescale));
    }
    if ( drawhplus ) {
      datahp.plotOn(Phiframe, MarkerColor(kGreen+3),MarkerStyle(25),MarkerSize(1.5),XErrorSize(0), Rescale(rescale));
      myPDFHP->plotOn(Phiframe, LineColor(kGreen+3),LineWidth(2), Normalization(rescale));
    }
    if ( rescale != 1. )
      Phiframe->GetYaxis()->SetRangeUser(0, ymax_Phi *rescale  * 1.3);
    
    // 
    //  hs 
    // 
    RooPlot* hsframe =  hs->frame(20);

    hsframe->GetXaxis()->CenterTitle();
    hsframe->GetYaxis()->CenterTitle();
    hsframe->GetYaxis()->SetTitle(" ");

    double ymax_hs;
    TH1F *hs_sm = new TH1F("hs_sm", "hs_sm", 20, -1, 1);
    tin->Project("hs_sm", "costhetastar");
    ymax_hs = hs_sm->GetMaximum();

    TH1F *hs_hminus = new TH1F("hs_hminus", "hs_hminus", 20, -1, 1);
    tin2->Project("hs_hminus", "costhetastar");
    ymax_hs = hs_hminus->GetMaximum() > ymax_hs ? hs_hminus->GetMaximum() : ymax_hs;

    TH1F *hs_hplus = new TH1F("hs_hplus", "hs_hplus", 20, -1, 1);
    tinhp->Project("hs_hplus", "costhetastar");
    ymax_hs = hs_hplus->GetMaximum() > ymax_hs ? hs_hplus->GetMaximum() : ymax_hs;
    
    if ( drawsm ) {
      data.plotOn(hsframe, MarkerColor(kRed),MarkerStyle(4),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale));
      myPDF->plotOn(hsframe, LineColor(kRed),LineWidth(2), Normalization(rescale));
    }
    if ( drawhminus ) {
      data2.plotOn(hsframe, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale));
      myPDFA->plotOn(hsframe, LineColor(kBlue),LineWidth(2), Normalization(rescale));
    }
    if ( drawhplus ) {
      datahp.plotOn(hsframe, MarkerColor(kGreen+3),MarkerStyle(25),MarkerSize(1.5),XErrorSize(0), Rescale(rescale));
      myPDFHP->plotOn(hsframe, LineColor(kGreen+3),LineWidth(2), Normalization(rescale));
    }
    if ( rescale != 1. )
      hsframe->GetYaxis()->SetRangeUser(0, ymax_hs * rescale * 1.3);

    
    //
    // Phi1
    // 
    RooPlot* Phi1frame =  Phi1->frame(20);
 
    Phi1frame->GetXaxis()->CenterTitle();
    Phi1frame->GetYaxis()->CenterTitle();
    Phi1frame->GetYaxis()->SetTitle(" ");

    double ymax_Phi1;
    TH1F *Phi1_sm = new TH1F("Phi1_sm", "Phi1_sm", 20, -TMath::Pi(), TMath::Pi());
    tin->Project("Phi1_sm", "phistar1");
    ymax_Phi1 = Phi1_sm->GetMaximum();

    TH1F *Phi1_hminus = new TH1F("Phi1_hminus", "Phi1_hminus", 20, -TMath::Pi(), TMath::Pi());
    tin2->Project("Phi1_hminus", "phistar1");
    ymax_Phi1 = Phi1_hminus->GetMaximum() > ymax_Phi1 ? Phi1_hminus->GetMaximum() : ymax_Phi1;

    TH1F *Phi1_hplus = new TH1F("Phi1_hplus", "Phi1_hplus", 20, -TMath::Pi(), TMath::Pi());
    tinhp->Project("Phi1_hplus", "phistar1");
    ymax_Phi1 = Phi1_hplus->GetMaximum() > ymax_Phi1 ? Phi1_hplus->GetMaximum() : ymax_Phi1;
    
    if ( drawsm ) {
      data.plotOn(Phi1frame, MarkerColor(kRed),MarkerStyle(4),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale));
      myPDF->plotOn(Phi1frame, LineColor(kRed),LineWidth(2), Normalization(rescale));
    }
    if ( drawhminus ) {
      data2.plotOn(Phi1frame, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale));
      myPDFA->plotOn(Phi1frame, LineColor(kBlue),LineWidth(2), Normalization(rescale));
    }
    if ( drawhplus ) {
      datahp.plotOn(Phi1frame, MarkerColor(kGreen+3),MarkerStyle(25),MarkerSize(1.5),XErrorSize(0), Rescale(rescale));
      myPDFHP->plotOn(Phi1frame, LineColor(kGreen+3),LineWidth(2), Normalization(rescale));
    }
    if ( rescale != 1. )
      Phi1frame->GetYaxis()->SetRangeUser(0, ymax_Phi1 * rescale * 1.3);



    if ( offshell ) {
      RooPlot* w1frame =  m1->frame(50);
      w1frame->GetXaxis()->CenterTitle();
      w1frame->GetYaxis()->CenterTitle();
      w1frame->GetYaxis()->SetTitle(" ");
      
      double ymax_w1;
      TH1F *w1_sm = new TH1F("w1_sm", "w1_sm", 50, 1e-09, 120);
      tin->Project("w1_sm", "wplusmass");
      ymax_w1 = w1_sm->GetMaximum();
      
      TH1F *w1_hminus = new TH1F("w1_hminus", "w1_hminus", 50, 1e-09, 120);
      tin2->Project("w1_hminus", "wplusmass")
      ymax_w1 = w1_hminus->GetMaximum() > ymax_w1 ? w1_hminus->GetMaximum() : ymax_w1;
      
      TH1F *w1_hplus = new TH1F("w1_hplus", "w1_hplus", 50, 1e-09, 120);
      tinhp->Project("w1_hplus", "wplusmass");
      ymax_w1 = w1_hplus->GetMaximum() > ymax_w1 ? w1_hplus->GetMaximum() : ymax_w1;
      
      if ( drawsm ) {
	data.plotOn(w1frame, MarkerColor(kRed),MarkerStyle(4),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale));
	myPDF->plotOn(w1frame, LineColor(kRed),LineWidth(2), Normalization(rescale));
      }
      if ( drawhminus ) {
	data2.plotOn(w1frame, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale));
	myPDFA->plotOn(w1frame, LineColor(kBlue),LineWidth(2), Normalization(rescale));
      }
      if ( drawhplus ) {
	datahp.plotOn(w1frame, MarkerColor(kGreen+3),MarkerStyle(25),MarkerSize(1.5),XErrorSize(0), Rescale(rescale));
	myPDFHP->plotOn(w1frame, LineColor(kGreen+3),LineWidth(2), Normalization(rescale));
      }
      if ( rescale != 1. ) 
	w1frame->GetYaxis()->SetRangeUser(0, ymax_w1 * rescale * 1.5);

      // 
      //  wminus
      // 
      RooPlot* w2frame =  m2->frame(50);

      w2frame->GetXaxis()->CenterTitle();
      w2frame->GetYaxis()->CenterTitle();
      w2frame->GetYaxis()->SetTitle(" ");
      
      double ymax_w2;
      TH1F *w2_sm = new TH1F("w2_sm", "w2_sm", 50, 1e-09, 120);
      tin->Project("w2_sm", "wminusmass");
      ymax_w2 = w2_sm->GetMaximum();
      
      TH1F *w2_hminus = new TH1F("w2_hminus", "w2_hminus", 50, 1e-09, 120);
      tin2->Project("w2_hminus", "wminusmass")
      ymax_w2 = w2_hminus->GetMaximum() > ymax_w2 ? w2_hminus->GetMaximum() : ymax_w2;
      
      TH1F *w2_hplus = new TH1F("w2_hplus", "w2_hplus", 50, 1e-09, 120);
      tinhp->Project("w2_hplus", "wminusmass");
      ymax_w2 = w2_hplus->GetMaximum() > ymax_w2 ? w2_hplus->GetMaximum() : ymax_w2;
      
      if ( drawsm ) {
	data.plotOn(w2frame, MarkerColor(kRed),MarkerStyle(4),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale));
	myPDF->plotOn(w2frame, LineColor(kRed),LineWidth(2), Normalization(rescale));
      }
      if ( drawhminus ) {
	data2.plotOn(w2frame, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale));
	myPDFA->plotOn(w2frame, LineColor(kBlue),LineWidth(2), Normalization(rescale));
      }
      if ( drawhplus ) {
	datahp.plotOn(w2frame, MarkerColor(kGreen+3),MarkerStyle(25),MarkerSize(1.5),XErrorSize(0), Rescale(rescale));
	myPDFHP->plotOn(w2frame, LineColor(kGreen+3),LineWidth(2), Normalization(rescale));
      }
      if ( rescale != 1. ) 
	w2frame->GetYaxis()->SetRangeUser(0, ymax_w2 * rescale * 1.5);
    }
    if ( drawpaper ) {
      TCanvas* can =new TCanvas("can","can",600,600);

      if ( offshell ) {
	w1frame->GetXaxis()->SetTitle("m_{l#nu} [GeV]");
	w1frame->Draw();
	can->Print(Form("paperplots/wplusmass_%.0fGeV_spin0_3in1_ww.eps", mH));
	can->SaveAs(Form("paperplots/wplusmass_%.0fGeV_spin0_3in1_ww.C", mH));
      }
      
      can->Clear();
      hsframe->Draw();
      can->Print(Form("paperplots/costhetastar_%.0fGeV_spin0_3in1_ww.eps", mH));      
      can->SaveAs(Form("paperplots/costhetastar_%.0fGeV_spin0_3in1_ww.C", mH));      
      
      can->Clear();
      Phi1frame->Draw();
      can->Print(Form("paperplots/phistar1_%.0fGeV_spin0_3in1_ww.eps", mH));      
      can->SaveAs(Form("paperplots/phistar1_%.0fGeV_spin0_3in1_ww.C", mH));      

      can->Clear();
      h1frame->GetXaxis()->SetTitle("cos#theta_{1} or cos#theta_{2}");
      h1frame->Draw();
      can->Print(Form("paperplots/costheta1_%.0fGeV_spin0_3in1_ww.eps", mH));
      can->SaveAs(Form("paperplots/costheta1_%.0fGeV_spin0_3in1_ww.C", mH));

      can->Clear();
      Phiframe->Draw();
      can->Print(Form("paperplots/phi_%.0fGeV_spin0_3in1_ww.eps", mH));      
      can->SaveAs(Form("paperplots/phi_%.0fGeV_spin0_3in1_ww.C", mH));      


    }

    else {
      
      TCanvas* cww = new TCanvas( "cww", "cww", 1000, 600 );
      cww->Divide(4,2);
      if ( offshell ) {
	cww->cd(1);
	w1frame->Draw();
	cww->cd(2);
	w2frame->Draw();
      }
      cww->cd(3);
      hsframe->Draw();
      cww->cd(4);
      box3->Draw();
      cww->cd(5);
      Phi1frame->Draw();
      cww->cd(6);
      h1frame->Draw();
      cww->cd(7);
      h2frame->Draw();
      cww->cd(8);
      Phiframe->Draw();
      
      cww->Print(Form("epsfiles/angles_HWW%.0f_JHU_7D.eps", mH));
      cww->Print(Form("pngfiles/angles_HWW%.0f_JHU_7D.png", mH));
      delete cww;
    }
}
