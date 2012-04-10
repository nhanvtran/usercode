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

void plotPdf_5D_VWW() {
    
    gROOT->ProcessLine(".L ~/tdrstyle.C");
    setTDRStyle();
    gStyle->SetPadLeftMargin(0.16);
    
    // Declaration of the PDFs to use
    gROOT->ProcessLine(".L PDFs/RooSpinOne_5D.cxx++");
    
    // Observables (5D)
    RooRealVar* h1 = new RooRealVar("costheta1","h1",-1,1);
    RooRealVar* h2 = new RooRealVar("costheta2","h2",-1,1);
    RooRealVar* hs = new RooRealVar("costhetastar","hs",-1,1);
    RooRealVar* Phi = new RooRealVar("phi","Phi",-TMath::Pi(),TMath::Pi());
    RooRealVar* Phi1 = new RooRealVar("phistar1","Phi1",-TMath::Pi(),TMath::Pi());
    
    // angular variables
    // 1+
    RooRealVar* fp0Val = new RooRealVar("fp0Val", "fp0Val", 0.25);
    RooRealVar* phip0Val = new RooRealVar("phip0Val", "phip0Val", 0);
    RooRealVar* phi0mVal = new RooRealVar("phi0mVal", "phi0mVal", 0);

    // Even more parameters, do not have to touch, based on W couplings
    RooRealVar* R1Val = new RooRealVar("R1Val","R1Val",1);
    RooRealVar* R2Val = new RooRealVar("R2Val","R2Val",-1);


    // these are the acceptance terms associated with the production angles
    // the default setting is for setting no-acceptance
    RooRealVar* aParam = new RooRealVar("aParam","aParam",0);
    
    // PDF definition X (JP = 1+)
    RooSpinOne_5D *myPDF = new RooSpinOne_5D("myPDF","myPDF", *h1, *h2, *hs, *Phi, *Phi1, *fp0Val, *phip0Val, *phi0mVal, *R1Val, *R2Val, *aParam);
    
    // different parameters for 1-
    RooRealVar* phip0ValV = new RooRealVar("phip0ValV", "phip0ValV", TMath::Pi());
    RooSpinOne_5D *myPDFA = new RooSpinOne_5D("myPDF","myPDF", *h1, *h2, *hs, *Phi, *Phi1, *fp0Val, *phip0ValV, *phi0mVal, *R1Val, *R2Val, *aParam);

    // Grab input file to convert to RooDataSet

    TFile* fin = new TFile("AVWW_250_JHU.root");
    TTree* tin = (TTree*) fin->Get("angles");
    RooDataSet data("data","data",tin,RooArgSet(*h1,*h2, *hs, *Phi, *Phi1));
    
    /*
    for (int i=1;i<10;i++) {
      RooArgSet* row = data.get(i);
      row->Print("v");
      std::cout << "weight: " << data.weight() << std::endl;
    }
    */

    // read another input file
    TFile* fin2 = new TFile("VWW_250_JHU.root");
    TTree* tin2 = (TTree*) fin2->Get("angles");
    RooDataSet data2("data2","data2",tin2,RooArgSet(*h1,*h2, *hs, *Phi, *Phi1));
    
    // P L O T   . . .  
    // (All parameters fixed, no fitting, just looking at the shape of the PDFs w.r.t. the data)
    TH1F* dum0 = new TH1F("dum0","dum0",1,0,1); dum0->SetLineColor(kRed); dum0->SetMarkerColor(kBlack); dum0->SetLineWidth(3);
    TH1F* dum1 = new TH1F("dum1","dum1",1,0,1); dum1->SetLineColor(kBlue); dum1->SetMarkerColor(kBlack); dum1->SetMarkerStyle(24), dum1->SetLineWidth(3);
    TLegend * box3 = new TLegend(0.1,0.1,0.9,0.92);
    box3->SetFillColor(0);
    box3->SetBorderSize(0);
    box3->AddEntry(dum0,"X#rightarrow WW JP = 1+","lp");
    box3->AddEntry(dum1,"X#rightarrow WW JP = 1-","lp");
    
    RooPlot* h1frame =  h1->frame(55);
    data.plotOn(h1frame, LineColor(kBlack));
    myPDF->plotOn(h1frame, LineColor(kRed));
    data2.plotOn(h1frame, LineColor(kBlack), MarkerStyle(24));
    myPDFA->plotOn(h1frame, LineColor(kBlue));
    
    RooPlot* h2frame =  h2->frame(55);
    data.plotOn(h2frame, LineColor(kBlack));
    myPDF->plotOn(h2frame, LineColor(kRed));
    data2.plotOn(h2frame, LineColor(kBlack), MarkerStyle(24));
    myPDFA->plotOn(h2frame, LineColor(kBlue));
    
    RooPlot* hsframe =  hs->frame(55);
    data.plotOn(hsframe, LineColor(kBlack));
    myPDF->plotOn(hsframe, LineColor(kRed));
    data2.plotOn(hsframe, LineColor(kBlack), MarkerStyle(24));
    myPDFA->plotOn(hsframe, LineColor(kBlue));
    
    RooPlot* Phiframe =  Phi->frame(55);
    data.plotOn(Phiframe, LineColor(kBlack));
    myPDF->plotOn(Phiframe, LineColor(kRed));
    data2.plotOn(Phiframe, LineColor(kBlack), MarkerStyle(24));
    myPDFA->plotOn(Phiframe, LineColor(kBlue));
    
    RooPlot* Phi1frame =  Phi1->frame(55);
    data.plotOn(Phi1frame, LineColor(kBlack));
    myPDF->plotOn(Phi1frame, LineColor(kRed));
    data2.plotOn(Phi1frame, LineColor(kBlack), MarkerStyle(24));
    myPDFA->plotOn(Phi1frame, LineColor(kBlue));
    
    TCanvas* czz = new TCanvas( "czz", "czz", 1000, 600 );
    czz->Divide(3,2);
    czz->cd(1);
    hsframe->Draw();
    czz->cd(2);
    Phi1frame->Draw();
    czz->cd(3);
    box3->Draw();
    czz->cd(4);
    h1frame->Draw();
    czz->cd(5);
    h2frame->Draw();
    czz->cd(6);
    Phiframe->Draw();
    
    czz->SaveAs("epsfiles/angles_VWW250_JHU.eps");
    czz->SaveAs("pngfiles/angles_VWW250_JHU.png");

}
