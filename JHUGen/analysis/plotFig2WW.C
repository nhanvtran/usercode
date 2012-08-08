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

void plotFig2WW(float mH = 125) {
  
    gROOT->ProcessLine(".L tdrstyle.C");
    setTDRStyle();
    TGaxis::SetMaxDigits(3);
    gROOT->ForceStyle();
    
    // Declaration of the PDFs to use
    gROOT->ProcessLine(".L PDFs/RooSpinZero_7D.cxx+");
    gROOT->ProcessLine(".L PDFs/RooSpinTwo_7D.cxx+");

    // W/Z mass and decay width constants
    double mV = 80.399;
    double gamV = 2.085;
    bool offshell = false;
    if ( mH < 2 * mV ) offshell = true;

    // Observables (7D)
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
    TString fileNameSM = Form("SMHiggsWW_%.0f_JHU.root", mH);
    TFile* fin = new TFile(fileNameSM);
    std::cout << "Opening " << fileNameSM << "\n";
    TTree* tin = (TTree*) fin->Get("angles");
    
    // for weighted events
    if ( offshell ) {
      RooDataSet data("data","data",tin,RooArgSet(*m1,*m2,*h1,*h2,*hs,*Phi,*Phi1));
    }
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
    TString fileNamePS = Form("PSHiggsWW_%.0f_JHU.root", mH);
    TFile* fin2 = new TFile(fileNamePS);
    std::cout << "Opening " << fileNamePS << "\n";
    TTree* tin2 = (TTree*) fin2->Get("angles");
    
    if ( offshell ) 
      RooDataSet data2("data2","data2",tin2,RooArgSet(*m1,*m2,*h1,*h2,*hs,*Phi,*Phi1));
    else 
      RooDataSet data2("data2","data2",tin2,RooArgSet(*h1,*h2,*hs,*Phi,*Phi1));
    
    // 
    // For 2m+
    // 
    
    double s = (mH*mH-2*mV*mV)/2.;
    RooRealVar* c1Val = new RooRealVar("c1Val", "c1Val", 2.*(1+mV*mV/s));
    RooRealVar* c2Val = new RooRealVar("c2Val", "c2Val", -0.5);
    RooRealVar* c3Val = new RooRealVar("c3Val", "c3Val", 0.);
    RooRealVar* c4Val = new RooRealVar("c4Val", "c4Val", -1.);
    RooRealVar* c5Val = new RooRealVar("c5Val", "c5Val", 0.);
    RooRealVar* c6Val = new RooRealVar("c6Val", "c6Val", 0.);
    RooRealVar* c7Val = new RooRealVar("c7Val", "c7Val", 0.);
    
    // 
    // Alternative definition in terms of g1->g10
    // 
    RooRealVar* g1Val2m = new RooRealVar("g1Val2m", "g1Val2m", 1);
    RooRealVar* g2Val2m = new RooRealVar("g2Val2m", "g2Val2m", 0.);
    RooRealVar* g3Val2m = new RooRealVar("g3Val2m", "g3Val2m", 0.);
    RooRealVar* g4Val2m = new RooRealVar("g4Val2m", "g4Val2m", 0.);
    RooRealVar* g5Val2m = new RooRealVar("g5Val2m", "g5Val2m", 1.);
    RooRealVar* g6Val2m = new RooRealVar("g6Val2m", "g6Val2m", 0.);
    RooRealVar* g7Val2m = new RooRealVar("g7Val2m", "g7Val2m", 0.);
    RooRealVar* g8Val2m = new RooRealVar("g8Val2m", "g8Val2m", 0.);
    RooRealVar* g9Val2m = new RooRealVar("g9Val2m", "g9Val2m", 0.);
    RooRealVar* g10Val2m = new RooRealVar("g10Val2m", "g10Val2m", 0.);

    // related to the gg/qq productions 
    RooRealVar* fz1Val = new RooRealVar("fz1Val", "fz1Val", 0);
    RooRealVar* fz2Val = new RooRealVar("fz2Val", "fz2Val", 1.0);

      // PDF definition SM Higgs (JP = 2+)
    RooSpinTwo_7D *myPDF2m;
    if ( offshell )
      myPDF2m = new RooSpinTwo_7D("myPDF","myPDF", *mX, *m1, *m2, *hs, *h1,*h2, *Phi, *Phi1, 
				  *c1Val, *c2Val, *c3Val, *c4Val, *c5Val, *c6Val, *c7Val, 
				  *useGTerm, *g1Val2m, *g2Val2m, *g3Val2m, *g4Val2m, *g5Val2m, *g6Val2m, *g7Val2m, *g8Val2m, *g9Val2m, *g10Val2m,
				  *fz1Val, *fz2Val, *R1Val, *R2Val, *mW, *gamW);
    else 
      myPDF2m = new RooSpinTwo_7D("myPDF","myPDF", *mX, *m1, *m2, *hs, *h1,*h2, *Phi, *Phi1, 
				  *c1Val, *c2Val, *c3Val, *c4Val, *c5Val, *c6Val, *c7Val, 
				  *useGTerm, *g1Val2m, *g2Val2m, *g3Val2m, *g4Val2m, *g5Val2m, *g6Val2m, *g7Val2m, *g8Val2m, *g9Val2m, *g10Val2m,
				  *fz1Val, *fz2Val, *R1Val, *R2Val, *mW, *gamW);
    // dataset for (JP = 2+)
    TString fileName2m;
    if ( useGTerm->getVal() > 0.) {
      fileName2m = Form("TWW_2mplus_%.0f_JHU.root", mH);
    }
    else {
      fileName2m = Form("TWW_%.0f_JHU_GenFromC.root", mH);
    }
    std::cout << "Opening " << fileName2m << "\n";
    TFile* fin2m = new TFile(fileName2m);
    TTree* tin2m = (TTree*) fin2m->Get("angles");

    if ( offshell) 
      RooDataSet data2m("data2m","data2m",tin2m,RooArgSet(*m1, *m2, *hs, *h1, *h2, *Phi, *Phi1));
    else 
      RooDataSet data2m("data2m","data2m",tin2m,RooArgSet(*hs, *h1, *h2, *Phi, *Phi1));


    // 
    // 2h+
    // 
    
    RooRealVar* g1Val2HPlus = new RooRealVar("g1Val2HPlus", "g1Val2HPlus", 0);
    RooRealVar* g2Val2HPlus = new RooRealVar("g2Val2HPlus", "g2Val2HPlus", 0.);
    RooRealVar* g3Val2HPlus = new RooRealVar("g3Val2HPlus", "g3Val2HPlus", 0.);
    RooRealVar* g4Val2HPlus = new RooRealVar("g4Val2HPlus", "g4Val2HPlus", 1.);
    RooRealVar* g5Val2HPlus = new RooRealVar("g5Val2HPlus", "g5Val2HPlus", 0.);
    RooRealVar* g6Val2HPlus = new RooRealVar("g6Val2HPlus", "g6Val2HPlus", 0.);
    RooRealVar* g7Val2HPlus = new RooRealVar("g7Val2HPlus", "g7Val2HPlus", 0.);
    RooRealVar* g8Val2HPlus = new RooRealVar("g8Val2HPlus", "g8Val2HPlus", 0.);
    RooRealVar* g9Val2HPlus = new RooRealVar("g9Val2HPlus", "g9Val2HPlus", 0.);
    RooRealVar* g10Val2HPlus = new RooRealVar("g10Val2HPlus", "g10Val2HPlus", 0.);
    RooRealVar* fz1Val2HPlus = new RooRealVar("fz1Val2HPlus", "fz1Val2HPlus", 0.0);
    RooRealVar* fz2Val2HPlus = new RooRealVar("fz2Val2HPlus", "fz2Val2HPlus", 0.0);

    RooSpinTwo_7D *myPDF2HPlus;
    if ( offshell )
      myPDF2HPlus = new RooSpinTwo_7D("myPDF2HPlus","myPDF2HPlus", *mX, *m1, *m2, *hs, *h1,*h2, *Phi, *Phi1, 
				       *c1Val, *c2Val, *c3Val, *c4Val, *c5Val, *c6Val, *c7Val, 
				       *useGTerm, *g1Val2HPlus, *g2Val2HPlus, *g3Val2HPlus, *g4Val2HPlus, 
				       *g5Val2HPlus, *g6Val2HPlus, *g7Val2HPlus, *g8Val2HPlus, *g9Val2HPlus, *g10Val2HPlus,
				       *fz1Val2HPlus, *fz2Val2HPlus, *R1Val, *R2Val, *mW, *gamW);
    else 
      myPDF2HPlus = new RooSpinTwo_7D("myPDF2HPlus","myPDF2HPlus", *mX, *mW, *mW, *hs, *h1,*h2, *Phi, *Phi1, 
				       *c1Val, *c2Val, *c3Val, *c4Val, *c5Val, *c6Val, *c7Val, 
				       *useGTerm, *g1Val2HPlus, *g2Val2HPlus, *g3Val2HPlus, *g4Val2HPlus, 
				       *g5Val2HPlus, *g6Val2HPlus, *g7Val2HPlus, *g8Val2HPlus, *g9Val2HPlus, *g10Val2HPlus,
				       *fz1Val2HPlus, *fz2Val2HPlus, *R1Val, *R2Val, *mW, *gamW);
    TString fileName2HPlus;
    if ( useGTerm->getVal() > 0.) {
      fileName2HPlus = Form("TWW_2hplus_%.0f_JHU.root", mH);
    }
    std::cout << "Opening " << fileName2HPlus << "\n";
    TFile* fin2HPlus = new TFile(fileName2HPlus);
    TTree* tin2HPlus = (TTree*) fin2HPlus->Get("angles");

    if ( offshell) 
      RooDataSet data2HPlus("data2HPlus","data2HPlus",tin2HPlus,RooArgSet(*m1, *m2, *hs, *h1, *h2, *Phi, *Phi1));
    else 
      RooDataSet data2HPlus("data2HPlus","data2HPlus",tin2HPlus,RooArgSet(*hs, *h1, *h2, *Phi, *Phi1));




    // P L O T   . . . 
    
    double rescale = 0.001;
    //
    // Phi
    // 
    RooPlot* Phiframe =  Phi->frame();
    Phiframe->GetXaxis()->CenterTitle();
    Phiframe->GetYaxis()->CenterTitle();
    Phiframe->GetYaxis()->SetTitle(" ");
    Phiframe->GetYaxis()->SetTitle(" ");
    Phiframe->GetXaxis()->SetNdivisions(505);


    double ymax_Phi;
    TH1F *Phi_sm = new TH1F("Phi_sm", "Phi_sm", 20,  -TMath::Pi(), TMath::Pi());
    tin->Project("Phi_sm", "phi");
    ymax_Phi = Phi_sm->GetMaximum();

    TH1F *Phi_hminus = new TH1F("Phi_hminus", "Phi_hminus", 20,  -TMath::Pi(), TMath::Pi());
    tin2->Project("Phi_hminus", "phi");
    ymax_Phi = Phi_hminus->GetMaximum() > ymax_Phi ? Phi_hminus->GetMaximum() : ymax_Phi;

    TH1F *Phi_2m = new TH1F("Phi_2m", "Phi_2m", 20,  -TMath::Pi(), TMath::Pi());
    tin2m->Project("Phi_2m", "phi");
    ymax_Phi = Phi_2m->GetMaximum() > ymax_Phi ? Phi_2m->GetMaximum() : ymax_Phi;

    TH1F *Phi_2HPlus = new TH1F("Phi_2HPlus", "Phi_2HPlus", 20,  -TMath::Pi(), TMath::Pi());
    tin2m->Project("Phi_2HPlus", "phi");
    ymax_Phi = Phi_2HPlus->GetMaximum() > ymax_Phi ? Phi_2HPlus->GetMaximum() : ymax_Phi;
    
    data.plotOn(Phiframe, MarkerColor(kRed),MarkerStyle(4),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
    myPDF->plotOn(Phiframe, LineColor(kRed),LineWidth(2), Normalization(rescale));
    
    data2.plotOn(Phiframe, MarkerColor(kMagenta+1),MarkerStyle(25),MarkerSize(1.9),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
    myPDFA->plotOn(Phiframe, LineColor(kMagenta+1),LineWidth(2), Normalization(rescale));
    
    data2m.plotOn(Phiframe, MarkerColor(kBlue),MarkerStyle(32),MarkerSize(1.5),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
    myPDF2m->plotOn(Phiframe, LineColor(kBlue),LineWidth(2), Normalization(rescale));

    data2HPlus.plotOn(Phiframe, MarkerColor(kGreen+3),MarkerStyle(27),MarkerSize(1.5),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
    myPDF2HPlus->plotOn(Phiframe, LineColor(kGreen+3),LineWidth(2), Normalization(rescale));
    
    if ( rescale != 1. )
      Phiframe->GetYaxis()->SetRangeUser(0, ymax_Phi *rescale  * 1.3);
    
    TCanvas* c1 = new TCanvas( "c1", "c1", 600, 600 );
    Phiframe->Draw();
    c1->SaveAs(Form("paperplots/phi_%.0fGeV_WW.eps", mH));
    c1->SaveAs(Form("paperplots/phi_%.0fGeV_WW.png", mH));
    c1->SaveAs(Form("paperplots/phi_%.0fGeV_WW.C", mH));

}
