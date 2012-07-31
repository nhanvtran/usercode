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
    
    gROOT->ProcessLine(".L ~/tdrstyle.C");
    setTDRStyle();
    gStyle->SetPadLeftMargin(0.16);
    
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
    RooRealVar* wminusmass = new RooRealVar("wminusmass","m(W-)",mV,1e-09,120);
    RooRealVar* hs = new RooRealVar("costhetastar","hs",-1,1);
    RooRealVar* h1 = new RooRealVar("costheta1","h1",-1,1);
    RooRealVar* h2 = new RooRealVar("costheta2","h2",-1,1);
    RooRealVar* Phi = new RooRealVar("phi","Phi",-TMath::Pi(),TMath::Pi());
    RooRealVar* Phi1 = new RooRealVar("phistar1","Phi1",-TMath::Pi(),TMath::Pi());
    
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
      
      TH1F* dum0 = new TH1F("dum0","dum0",1,0,1); dum0->SetLineColor(kRed); dum0->SetMarkerColor(kBlack); dum0->SetLineWidth(3);
      TH1F* dum1 = new TH1F("dum1","dum1",1,0,1); dum1->SetLineColor(kBlue); dum1->SetMarkerColor(kBlack); dum1->SetMarkerStyle(24), dum1->SetLineWidth(3);  
      TH1F* dum2 = new TH1F("dum2","dum2",1,0,1); dum2->SetLineColor(kGreen); dum2->SetMarkerColor(kBlack); dum2->SetMarkerStyle(21), dum2->SetLineWidth(3); // 2L+
      
      TLegend * box3 = new TLegend(0.1,0.1,0.9,0.92);
      box3->SetFillColor(0);
      box3->SetBorderSize(0);
      box3->AddEntry(dum0,Form("X(%.0f)#rightarrow WW JP = 2m+", mH),"lp");
      box3->AddEntry(dum1,Form("X(%.0f)#rightarrow WW JP = 2h-", mH),"lp");
      box3->AddEntry(dum2,Form("X(%.0f)#rightarrow WW JP = 2h+,", mH),"lp");
      
      bool drawmplus = false;
      bool drawhminus = false;
      bool drawhplus = true;

      if ( offshell ) {
	RooPlot* wplusmassframe =  wplusmass->frame(55);
	if ( drawmplus ) {
	  data.plotOn(wplusmassframe, LineColor(kBlack));
	  myPDF->plotOn(wplusmassframe, LineColor(kRed));
	}
	if ( drawhminus ) {
	  dataMinus.plotOn(wplusmassframe, LineColor(kBlack), MarkerStyle(24));
	  myPDFMinus->plotOn(wplusmassframe, LineColor(kBlue));
	}
	if ( drawhplus ) {
	  dataHPlus.plotOn(wplusmassframe, LineColor(kBlack), MarkerStyle(21));
	  myPDFHPlus->plotOn(wplusmassframe, LineColor(kGreen));
	}
	
	RooPlot* wminusmassframe =  wminusmass->frame(55);
	if ( drawmplus ) {
	  data.plotOn(wminusmassframe, LineColor(kBlack));
	  myPDF->plotOn(wminusmassframe, LineColor(kRed));
	} 
	if ( drawhminus ) {
	  dataMinus.plotOn(wminusmassframe, LineColor(kBlack), MarkerStyle(24));
	  myPDFMinus->plotOn(wminusmassframe, LineColor(kBlue));
	}
	if ( drawhplus ) {
	  dataHPlus.plotOn(wminusmassframe, LineColor(kBlack), MarkerStyle(21));
	  myPDFHPlus->plotOn(wminusmassframe, LineColor(kGreen));
	}
      }
      
      RooPlot* h1frame =  h1->frame(55);
      if ( drawmplus ) {
	data.plotOn(h1frame, LineColor(kBlack));
	myPDF->plotOn(h1frame, LineColor(kRed));
      }
      if ( drawhminus ) {
      dataMinus.plotOn(h1frame, LineColor(kBlack), MarkerStyle(24));
      myPDFMinus->plotOn(h1frame, LineColor(kBlue));
      } 
      if ( drawhplus ) {
	dataHPlus.plotOn(h1frame, LineColor(kBlack), MarkerStyle(21));
	myPDFHPlus->plotOn(h1frame, LineColor(kGreen));
      }
      RooPlot* h2frame =  h2->frame(55);
      if ( drawmplus ) {
	data.plotOn(h2frame, LineColor(kBlack));
	myPDF->plotOn(h2frame, LineColor(kRed));
      }
      if ( drawhminus ) {
	dataMinus.plotOn(h2frame, LineColor(kBlack), MarkerStyle(24));
	myPDFMinus->plotOn(h2frame, LineColor(kBlue));
      }
      if ( drawhplus ) {
	dataHPlus.plotOn(h2frame, LineColor(kBlack), MarkerStyle(21));
	myPDFHPlus->plotOn(h2frame, LineColor(kGreen));
      }
      RooPlot* hsframe =  hs->frame(55);
      if ( drawmplus ) {
	data.plotOn(hsframe, LineColor(kBlack));
	myPDF->plotOn(hsframe, LineColor(kRed));
      }
      if ( drawhminus ) {
	dataMinus.plotOn(hsframe, LineColor(kBlack), MarkerStyle(24));
	myPDFMinus->plotOn(hsframe, LineColor(kBlue));
      }
      if ( drawhplus ) {
	dataHPlus.plotOn(hsframe, LineColor(kBlack), MarkerStyle(21));
	myPDFHPlus->plotOn(hsframe, LineColor(kGreen));
      }
      RooPlot* Phiframe =  Phi->frame(55);
      if ( drawmplus ) {
	data.plotOn(Phiframe, LineColor(kBlack));
	myPDF->plotOn(Phiframe, LineColor(kRed));
      }
      if ( drawhminus ) {
	dataMinus.plotOn(Phiframe, LineColor(kBlack), MarkerStyle(24));
	myPDFMinus->plotOn(Phiframe, LineColor(kBlue));
      }
      if ( drawhplus ) {
	dataHPlus.plotOn(Phiframe, LineColor(kBlack), MarkerStyle(21));
	myPDFHPlus->plotOn(Phiframe, LineColor(kGreen));
      }
      RooPlot* Phi1frame =  Phi1->frame(55);
      if ( drawmplus ) {
	data.plotOn(Phi1frame, LineColor(kBlack));
	myPDF->plotOn(Phi1frame, LineColor(kRed));
      }
      if ( drawhminus ) {
	dataMinus.plotOn(Phi1frame, LineColor(kBlack), MarkerStyle(24));
	myPDFMinus->plotOn(Phi1frame, LineColor(kBlue));
      }
      if ( drawhplus ) {
	dataHPlus.plotOn(Phi1frame, LineColor(kBlack), MarkerStyle(21));
	myPDFHPlus->plotOn(Phi1frame, LineColor(kGreen));
      }

      TCanvas* czz = new TCanvas( "czz", "czz", 1000, 600 );
      czz->Divide(4,2);
      
      if ( offshell ) {
	czz->cd(1);
	wplusmassframe->Draw();
	
	czz->cd(2);
	wminusmassframe->Draw();
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
