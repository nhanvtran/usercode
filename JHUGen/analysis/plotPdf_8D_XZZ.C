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

void plotPdf_8D_XZZ() {
    
    gROOT->ProcessLine(".L ~/tdrstyle.C");
    setTDRStyle();
    gStyle->SetPadLeftMargin(0.16);
    
    // Declaration of the PDFs to use
    gROOT->ProcessLine(".L  PDFs/RooSpinTwoXZsZs.cxx+");
    
    // Observables (8D)
    RooRealVar* zzmass = new RooRealVar("zzmass","m_{ZZ}",250,100,800);
    RooRealVar* z1mass = new RooRealVar("z1mass","m_{Z1}",91.188,4,120);
    RooRealVar* z2mass = new RooRealVar("z2mass","m_{Z2}",91.188,4,120);
    RooRealVar* h1 = new RooRealVar("costheta1","h1",-1,1);
    RooRealVar* h2 = new RooRealVar("costheta2","h2",-1,1);
    RooRealVar* hs = new RooRealVar("costhetastar","hs",-1,1);
    RooRealVar* Phi = new RooRealVar("phi","Phi",-TMath::Pi(),TMath::Pi());
    RooRealVar* Phi1 = new RooRealVar("phistar1","Phi1",-TMath::Pi(),TMath::Pi());
    
    // angular variables
    // These values correspond to the 2m+

    RooRealVar* c1 = new RooRealVar("c1", "c1", 2+2*91.188*91.188/(250*250)); // 2(1+mZ^2/mX^2)
    RooRealVar* c2 = new RooRealVar("c2", "c2", -0.5);
    RooRealVar* c3 = new RooRealVar("c3", "c3", 0.);
    RooRealVar* c4 = new RooRealVar("c4", "c4", -1);
    RooRealVar* c5 = new RooRealVar("c5", "c5", 0.);
    RooRealVar* c6 = new RooRealVar("c6", "c6", 0.);
    RooRealVar* c7 = new RooRealVar("c7", "c7", 0.);

    RooRealVar* phi1 = new RooRealVar("phi1", "phi1", 0.);
    RooRealVar* phi2 = new RooRealVar("phi2", "phi2", 0.);
    RooRealVar* phi3 = new RooRealVar("phi3", "phi3", 0.);
    RooRealVar* phi4 = new RooRealVar("phi4", "phi4", 0.);
    RooRealVar* phi5 = new RooRealVar("phi5", "phi5", 0.);
    RooRealVar* phi6 = new RooRealVar("phi6", "phi6", 0.);
    RooRealVar* phi7 = new RooRealVar("phi7", "phi7", 0.);

    // related to the gg/qq productions 
    RooRealVar* fz1Val = new RooRealVar("fz1Val", "fz1Val", 0);
    RooRealVar* fz2Val = new RooRealVar("fz2Val", "fz2Val", 1.0);

    // Even more parameters, do not have to touch, based on Z couplings
    RooRealVar* R1Val = new RooRealVar("R1Val","R1Val",0.15);
    RooRealVar* R2Val = new RooRealVar("R2Val","R2Val",0.15);

    // PDF definition SM Higgs (JP = 2+)
    RooSpinTwoXZsZs *myPDF = new RooSpinTwoXZsZs("myPDF","myPDF", *zzmass, *z1mass, *z2mass, *hs, *h1,*h2, *Phi, *Phi1, *c1, *phi1, *c2, *phi2, *c3, *phi3, *c4, *phi4, *c5, *phi5, *c6, *phi6, *c7, *phi7, *fz1Val, *fz2Val, *R1Val, *R2Val);
    
    // dataset for (JP = 2+)
    TFile* fin = new TFile("THiggsZZ_250_JHU.root");
    TTree* tin = (TTree*) fin->Get("angles");
    RooDataSet data("data","data",tin,RooArgSet(*zzmass, *z1mass, *z2mass, *h1, *h2, *hs, *Phi, *Phi1));
 
    // P L O T   . . .  
    // (All parameters fixed, no fitting, just looking at the shape of the PDFs w.r.t. the data)
    TH1F* dum0 = new TH1F("dum0","dum0",1,0,1); dum0->SetLineColor(kRed); dum0->SetMarkerColor(kBlack); dum0->SetLineWidth(3); // 2m+

    TLegend * box3 = new TLegend(0.1,0.1,0.9,0.92);
    box3->SetFillColor(0);
    box3->SetBorderSize(0);
    box3->AddEntry(dum0,"X#rightarrow ZZ JP = 2m+","lp");
    
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
    
    czz->SaveAs("epsfiles/angles_TZZ250_JHU_8D.eps");
    czz->SaveAs("pngfiles/angles_TZZ250_JHU_8D.png");

}
