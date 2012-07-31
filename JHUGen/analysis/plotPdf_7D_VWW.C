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

void plotPdf_7D_VWW(double mH=125) {
    
    gROOT->ProcessLine(".L ~/tdrstyle.C");
    setTDRStyle();
    gStyle->SetPadLeftMargin(0.16);
    
    // Declaration of the PDFs to use
    gROOT->ProcessLine(".L PDFs/RooSpinOne_7D.cxx++");
    
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
    RooRealVar* h1 = new RooRealVar("costheta1","h1",-1,1);
    RooRealVar* h2 = new RooRealVar("costheta2","h2",-1,1);
    RooRealVar* hs = new RooRealVar("costhetastar","hs",-1,1);
    RooRealVar* Phi = new RooRealVar("phi","Phi",-TMath::Pi(),TMath::Pi());
    RooRealVar* Phi1 = new RooRealVar("phistar1","Phi1",-TMath::Pi(),TMath::Pi());
    
    // 1-
    RooRealVar* g1ValV = new RooRealVar("g1ValV","g1ValV",1.);
    RooRealVar* g2ValV = new RooRealVar("g2ValV","g2ValV",0.);
    // Even more parameters, do not have to touch, based on W couplings
    RooRealVar* R1Val = new RooRealVar("R1Val","R1Val",-1.);
    RooRealVar* R2Val = new RooRealVar("R2Val","R2Val",-1.);
    
    // these are the acceptance terms associated with the production angles
    // the default setting is for setting no-acceptance
    RooRealVar* aParam = new RooRealVar("aParam","aParam",0);
    
    RooSpinOne_7D *myPDFV;

    if ( offshell ) 
      myPDFV = new RooSpinOne_7D("myPDF","myPDF", *mX, *wplusmass, *wminusmass, *h1, *h2, *hs, *Phi, *Phi1, 
				 *g1ValV, *g2ValV, *R1Val, *R2Val, *aParam, *mW, *gamW);
    else 
      myPDFV = new RooSpinOne_7D("myPDF","myPDF", *mX, *mW, *mW, *h1, *h2, *hs, *Phi, *Phi1, 
				*g1ValV, *g2ValV, *R1Val, *R2Val, *aParam, *mW, *gamW);
    
    // Grab input file to convert to RooDataSet
    TFile* finV = new TFile(Form("VWW_%.0f_JHU.root", mH));
    // TFile* finV = new TFile(Form("VWW_%.0f_LProd_JHU.root", mH));
    TTree* tinV = (TTree*) finV->Get("angles");
    if ( offshell ) 
      RooDataSet dataV("dataV","dataV",tinV,RooArgSet(*wplusmass, *wminusmass, *h1,*h2, *hs, *Phi, *Phi1));
    else 
      RooDataSet dataV("dataV","dataV",tinV,RooArgSet(*h1,*h2, *hs, *Phi, *Phi1));
    
    for (int i=1;i<1;i++) {
      RooArgSet* row = dataV.get(i);
      row->Print("v");
    }
    

    // 
    // 1-
    // 
    RooRealVar* g1ValA = new RooRealVar("g1ValA","g1ValA",0);
    RooRealVar* g2ValA = new RooRealVar("g2ValA","g2ValA",1);
    RooSpinOne_7D *myPDFA;
    
    if ( offshell ) 
      myPDFA = new RooSpinOne_7D("myPDF","myPDF", *mX, *wplusmass, *wminusmass, *h1, *h2, *hs, *Phi, *Phi1,
				 *g1ValA, *g2ValA, *R1Val, *R2Val, *aParam, *mW, *gamW);
    else 
      myPDFA = new RooSpinOne_7D("myPDF","myPDF", *mX, *mW, *mW, *h1, *h2, *hs, *Phi, *Phi1,
				 *g1ValA, *g2ValA, *R1Val, *R2Val, *aParam, *mW, *gamW);

    TFile* finA = new TFile(Form("AVWW_%.0f_JHU.root", mH));
    TTree* tinA = (TTree*) finA->Get("angles");
    if ( offshell ) 
      RooDataSet dataA("dataA","dataA",tinA,RooArgSet(*wplusmass, *wminusmass, *hs, *h1, *h2, *Phi, *Phi1));
     else 
       RooDataSet dataA("dataA","dataA",tinA,RooArgSet(*h1,*h2, *hs, *Phi, *Phi1));
    //
    // P L O T   . . .  
    // 

    bool drawv = false;
    bool drawa = true;
    // for 1-
    TH1F* dum0 = new TH1F("dum0","dum0",1,0,1); dum0->SetLineColor(kRed); dum0->SetMarkerColor(kBlack); dum0->SetLineWidth(3);
    // for 1+
    TH1F* dum1 = new TH1F("dum1","dum1",1,0,1); dum1->SetLineColor(kBlue); dum1->SetMarkerColor(kBlack); dum1->SetMarkerStyle(24), dum1->SetLineWidth(3);
    TLegend * box3 = new TLegend(0.1,0.1,0.9,0.92);
    box3->SetFillColor(0);
    box3->SetBorderSize(0);
    if ( drawa ) 
      box3->AddEntry(dum0,"X#rightarrow WW JP = 1+","lp");
    if ( drawv )
    box3->AddEntry(dum1,"X#rightarrow WW JP = 1-","lp");
    
    if ( offshell ) {
        RooPlot* wplusmassframe =  wplusmass->frame(55);
        if ( drawv ) {
	  dataV.plotOn(wplusmassframe, LineColor(kBlack), MarkerStyle(24));
	  myPDFV->plotOn(wplusmassframe, LineColor(kBlue));
	}
	if ( drawa ) {
	  dataA.plotOn(wplusmassframe, LineColor(kBlack));
	  myPDFA->plotOn(wplusmassframe, LineColor(kRed));
        }
        RooPlot* wminusmassframe =  wminusmass->frame(55);
	if ( drawv ) {
	  dataV.plotOn(wminusmassframe, LineColor(kBlack), MarkerStyle(24));
	  myPDFV->plotOn(wminusmassframe, LineColor(kBlue));
	}
	if ( drawa ) {
	  dataA.plotOn(wminusmassframe, LineColor(kBlack));
	  myPDFA->plotOn(wminusmassframe, LineColor(kRed));
	}
    }
    
    RooPlot* h1frame =  h1->frame(55);
    if ( drawv ) {
      dataV.plotOn(h1frame, LineColor(kBlack), MarkerStyle(24));
      myPDFV->plotOn(h1frame, LineColor(kBlue));
    }
    if ( drawa ) {
      dataA.plotOn(h1frame, LineColor(kBlack));
      myPDFA->plotOn(h1frame, LineColor(kRed));
    }
    RooPlot* h2frame =  h2->frame(55);
    if ( drawv ) {
      dataV.plotOn(h2frame, LineColor(kBlack), MarkerStyle(24));
      myPDFV->plotOn(h2frame, LineColor(kBlue));
    }
    if ( drawa ) {
      dataA.plotOn(h2frame, LineColor(kBlack));
      myPDFA->plotOn(h2frame, LineColor(kRed));
    }
    RooPlot* hsframe =  hs->frame(55);
    if ( drawv ) {
      dataV.plotOn(hsframe, LineColor(kBlack), MarkerStyle(24));
      myPDFV->plotOn(hsframe, LineColor(kBlue));
    }
    if ( drawa ) {
      dataA.plotOn(hsframe, LineColor(kBlack));
      myPDFA->plotOn(hsframe, LineColor(kRed));
    }
    RooPlot* Phiframe =  Phi->frame(55);
    if ( drawv ) {
      dataV.plotOn(Phiframe, LineColor(kBlack), MarkerStyle(24));
      myPDFV->plotOn(Phiframe, LineColor(kBlue));
    }
    if ( drawa ) {
      dataA.plotOn(Phiframe, LineColor(kBlack));
      myPDFA->plotOn(Phiframe, LineColor(kRed));
    }
    RooPlot* Phi1frame =  Phi1->frame(55);
    if ( drawv ) {
      dataV.plotOn(Phi1frame, LineColor(kBlack), MarkerStyle(24));
      myPDFV->plotOn(Phi1frame, LineColor(kBlue));
    }
    if ( drawa ) {
      dataA.plotOn(Phi1frame, LineColor(kBlack));
      myPDFA->plotOn(Phi1frame, LineColor(kRed));
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
    
    
    czz->SaveAs(Form("epsfiles/angles_VWW%.0f_JHU_7D.eps", mH));
    czz->SaveAs(Form("pngfiles/angles_VWW%.0f_JHU_7D.png", mH));
    
    // czz->SaveAs(Form("epsfiles/angles_VWW%.0f_LProd_JHU_7D.eps", mH));
    // czz->SaveAs(Form("pngfiles/angles_VWW%.0f_LProd_JHU_7D.png", mH));

}
