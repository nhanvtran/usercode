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

void plotPdf_7D_XWW(double mH = 250, bool draw=true) {
    
    gROOT->ProcessLine(".L ~/tdrstyle.C");
    setTDRStyle();
    gStyle->SetPadLeftMargin(0.16);
    
    // Declaration of the PDFs to use
    gROOT->ProcessLine(".L  PDFs/RooSpinTwoXZsZs.cxx+");

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
    RooRealVar* wplusmass = new RooRealVar("wplusmass","m(W+)",mV,4,120);
    RooRealVar* wminusmass = new RooRealVar("wminusmass","m(W-)",mV,4,120);
    RooRealVar* hs = new RooRealVar("costhetastar","hs",-1,1);
    RooRealVar* h1 = new RooRealVar("costheta1","h1",-1,1);
    RooRealVar* h2 = new RooRealVar("costheta2","h2",-1,1);
    RooRealVar* Phi = new RooRealVar("phi","Phi",-TMath::Pi(),TMath::Pi());
    RooRealVar* Phi1 = new RooRealVar("phistar1","Phi1",-TMath::Pi(),TMath::Pi());
    
    //
    // coupling constants for 2m+
    // RooRealVar* mX = new RooRealVar("mX","mX",mH);
    double s = (mH*mH-2*mV*mV)/2.;
    double c1 = 2*(1+mV*mV/s);
    std::cout << "c1 = " << c1 << "\n"; 

    RooRealVar* c1Val = new RooRealVar("c1Val", "c1Val", c1);
    RooRealVar* c2Val = new RooRealVar("c2Val", "c2Val", -0.5);
    RooRealVar* c3Val = new RooRealVar("c3Val", "c3Val", 0.);
    RooRealVar* c4Val = new RooRealVar("c4Val", "c4Val", -1);
    RooRealVar* c5Val = new RooRealVar("c5Val", "c5Val", 0.);
    RooRealVar* c6Val = new RooRealVar("c6Val", "c6Val", 0.);
    RooRealVar* c7Val = new RooRealVar("c7Val", "c7Val", 0.);

    // related to the gg/qq productions 
    RooRealVar* fz1Val = new RooRealVar("fz1Val", "fz1Val", 0);
    RooRealVar* fz2Val = new RooRealVar("fz2Val", "fz2Val", 1.0);

    // Even more parameters, do not have to touch, based on Z couplings
    RooRealVar* R1Val = new RooRealVar("R1Val","R1Val",1);
    RooRealVar* R2Val = new RooRealVar("R2Val","R2Val",1);
    
      
    // PDF definition SM Higgs (JP = 2+)
    RooSpinTwoXZsZs *myPDF;
    if ( offshell )
      myPDF = new RooSpinTwoXZsZs("myPDF","myPDF", *mX, *wplusmass, *wminusmass, *hs, *h1,*h2, *Phi, *Phi1, *c1Val, *c2Val, *c3Val, *c4Val, *c5Val, *c6Val, *c7Val, *fz1Val, *fz2Val, *R1Val, *R2Val, *mW, *gamW);
    else 
      myPDF = new RooSpinTwoXZsZs("myPDF","myPDF", *mX, *mW, *mW, *hs, *h1,*h2, *Phi, *Phi1, *c1Val, *c2Val, *c3Val, *c4Val, *c5Val, *c6Val, *c7Val, *fz1Val, *fz2Val, *R1Val, *R2Val, *mW, *gamW);
      
    // dataset for (JP = 2+)
    TFile* fin = new TFile(Form("TWW_%.0f_JHU.root", mH));
    TTree* tin = (TTree*) fin->Get("angles");
    
    if ( offshell) 
      RooDataSet data("data","data",tin,RooArgSet(*wplusmass, *wminusmass, *hs, *h1, *h2, *Phi, *Phi1));
    else 
      RooDataSet data("data","data",tin,RooArgSet(*hs, *h1, *h2, *Phi, *Phi1));

    if ( draw ) {
      // P L O T   . . .  
      // (All parameters fixed, no fitting, just looking at the shape of the PDFs w.r.t. the data)
      TH1F* dum0 = new TH1F("dum0","dum0",1,0,1); dum0->SetLineColor(kRed); dum0->SetMarkerColor(kBlack); dum0->SetLineWidth(3); // 2m+
      
      TLegend * box3 = new TLegend(0.1,0.1,0.9,0.92);
      box3->SetFillColor(0);
      box3->SetBorderSize(0);
      box3->AddEntry(dum0,"X#rightarrow WW JP = 2m+","lp");
      
      if ( offshell ) {
      RooPlot* wplusmassframe =  wplusmass->frame(55);
      data.plotOn(wplusmassframe, LineColor(kBlack));
      myPDF->plotOn(wplusmassframe, LineColor(kRed));
      
      RooPlot* wminusmassframe =  wminusmass->frame(55);
      data.plotOn(wminusmassframe, LineColor(kBlack));
      myPDF->plotOn(wminusmassframe, LineColor(kRed));
      }
      
      RooPlot* h1frame =  h1->frame(55);
      data.plotOn(h1frame, LineColor(kBlack));
      myPDF->plotOn(h1frame, LineColor(kRed));
      
      RooPlot* h2frame =  h2->frame(55);
      data.plotOn(h2frame, LineColor(kBlack));
      myPDF->plotOn(h2frame, LineColor(kRed));
      
      RooPlot* hsframe =  hs->frame(55);
      data.plotOn(hsframe, LineColor(kBlack));
      myPDF->plotOn(hsframe, LineColor(kRed));
      
      RooPlot* Phiframe =  Phi->frame(55);
      data.plotOn(Phiframe, LineColor(kBlack));
      myPDF->plotOn(Phiframe, LineColor(kRed));
      
      RooPlot* Phi1frame =  Phi1->frame(55);
      data.plotOn(Phi1frame, LineColor(kBlack));
      myPDF->plotOn(Phi1frame, LineColor(kRed));
      
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
      
      czz->SaveAs(Form("epsfiles/angles_TWW%.0f_JHU_7D.eps", mH));
      czz->SaveAs(Form("pngfiles/angles_TWW%.0f_JHU_7D.png", mH));
      
      delete czz;
    }
}
