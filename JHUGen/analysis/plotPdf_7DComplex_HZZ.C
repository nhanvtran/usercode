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

// TString filemode = "1minus2p5ig4";
// TString filemode = "minus2p5ig4";
// TString filemode = "allrealg";
TString filemode = "complexg2g4";
void plotPdf_7DComplex_HZZ(float mH = 126) {
  
    gROOT->ProcessLine(".L tdrstyle.C");
    setTDRStyle();
    gStyle->SetPadLeftMargin(0.16);
    
    // Declaration of the PDFs to use
    gROOT->ProcessLine(".L PDFs/RooSpinZero_7DComplex.cc+");

    // W/Z mass and decay width constants
    double mV = 91.1876;
    double gamV = 2.4952;

    // Observables (5D)
    RooRealVar* z1mass = new RooRealVar("Z1Mass","m_{Z1}",mV,40,110);
    RooRealVar* z2mass = new RooRealVar("Z2Mass","m_{Z2}",mV,1e-09,65);
    RooRealVar* h1 = new RooRealVar("helcosthetaZ1","h1",-1,1);
    RooRealVar* h2 = new RooRealVar("helcosthetaZ2","h2",-1,1);
    RooRealVar* Phi = new RooRealVar("helphi","Phi",-TMath::Pi(),TMath::Pi());
    RooRealVar* hs = new RooRealVar("costhetastar","hs",-1,1);
    RooRealVar* Phi1 = new RooRealVar("phistarZ1","Phi1",-TMath::Pi(),TMath::Pi());
    RooRealVar* flavortype = new RooRealVar("flavortype", "flavortype", 0.0, 10);
    RooRealVar* wt = new RooRealVar("wt", "wt", 0, 10.);
    
    // for the pole mass and decay width of Z 
    RooRealVar* mX = new RooRealVar("mX","mX", mH);
    RooRealVar* mZ = new RooRealVar("mZ","mZ", mV);
    RooRealVar* gamZ = new RooRealVar("gamZ","gamZ",gamV);
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
    RooRealVar* g2Val = new RooRealVar("g2Val", "g2Val", 1.);
    RooRealVar* g3Val = new RooRealVar("g3Val", "g3Val", 0.);
    RooRealVar* g4Val = new RooRealVar("g4Val", "g4Val", 1);

    RooRealVar* g1ValIm = new RooRealVar("g1ValIm", "g1ValIm", 0);
    RooRealVar* g2ValIm = new RooRealVar("g2ValIm", "g2ValIm", 2.5);
    RooRealVar* g3ValIm = new RooRealVar("g3ValIm", "g3ValIm", 0.);
    RooRealVar* g4ValIm = new RooRealVar("g4ValIm", "g4ValIm", 2.5);
    
    // Even more parameters, do not have to touch, based on W couplings
    RooRealVar* R1Val = new RooRealVar("R1Val","R1Val",0.15);
    RooRealVar* R2Val = new RooRealVar("R2Val","R2Val",0.15);
    
   RooRealVar* fg2  = new RooRealVar("fg2","f_{g2}",0.,0.,1.0);
   RooRealVar* fg4  = new RooRealVar("fg4","f_{g4}",0.,0.,1.0);
   RooRealVar* phig2  = new RooRealVar("phig2","#phi_{g2}",0.,0.,2*TMath::Pi());
   RooRealVar* phig4  = new RooRealVar("phig4","#phi_{g4}",0.,0.,2*TMath::Pi());
   
   // use the parameterization of real and im of the g-couplings
   int parameterization = 1;
    
    // PDF definition SM Higgs (JP = 0+)
    RooSpinZero_7DComplex *myPDF;
    myPDF = new RooSpinZero_7DComplex("PDF","PDF",*z1mass,*z2mass,*h1,*h2,*hs,*Phi,*Phi1,*a1Val,*phi1Val,*a2Val,*phi2Val,*a3Val,*phi3Val,parameterization,*g1Val,*g2Val,*g3Val,*g4Val,*g1ValIm,*g2ValIm,*g3ValIm,*g4ValIm,*fg2,*fg4,*phig2,*phig4,*mZ,*gamZ,*mX,*R1Val,*R2Val);

    
    // Grab input file to convert to RooDataSet
    TFile* fin = new TFile(Form("0mixp_%s_8_%.0f_comb.root", filemode.Data(), mH));
    TTree* tin = (TTree*) fin->Get("SelectedTree");
    
    RooDataSet dataTMP("dataTMP","dataTMP",tin,RooArgSet(*z1mass,*z2mass,*hs,*h1,*h2,*Phi,*Phi1,*flavortype));
    RooDataSet data("data","data",RooArgSet(*z1mass, *z2mass, *hs, *h1, *h2, *Phi, *Phi1,*flavortype), Cut("flavortype==3"), Import(dataTMP));
    
    // Plot
    // (All parameters fixed, no fitting, just looking at the shape of the PDFs w.r.t. the data)
    TH1F* dum0 = new TH1F("dum0","dum0",1,0,1); dum0->SetLineColor(kRed); dum0->SetMarkerColor(kBlack); dum0->SetLineWidth(3); // 2m+
    
    TLegend * box3 = new TLegend(0.1,0.1,0.9,0.92);
    box3->SetFillColor(0);
    box3->SetBorderSize(0);
    box3->SetTextSize(0.06);
    box3->AddEntry(dum0,Form("X#rightarrow ZZ JP = 0 %s", filemode.Data()),"lp");
    
    RooPlot* w1frame =  z1mass->frame(20);
    data.plotOn(w1frame, MarkerColor(kBlack));
    myPDF->plotOn(w1frame, LineColor(kRed));
    
    RooPlot* w2frame =  z2mass->frame(20);
    data.plotOn(w2frame, MarkerColor(kBlack));
    myPDF->plotOn(w2frame, LineColor(kRed));
    
    RooPlot* h1frame =  h1->frame(10);
    data.plotOn(h1frame, MarkerColor(kBlack));
    myPDF->plotOn(h1frame, LineColor(kRed));
    
    RooPlot* h2frame =  h2->frame(10);
    data.plotOn(h2frame, MarkerColor(kBlack));
    myPDF->plotOn(h2frame, LineColor(kRed));

    RooPlot* hsframe =  hs->frame(10);
    data.plotOn(hsframe, MarkerColor(kBlack));
    myPDF->plotOn(hsframe, LineColor(kRed));    

    RooPlot* Phiframe =  Phi->frame(10);
    data.plotOn(Phiframe, MarkerColor(kBlack));
    myPDF->plotOn(Phiframe, LineColor(kRed));
        
    RooPlot* Phi1frame =  Phi1->frame(10);
    data.plotOn(Phi1frame, MarkerColor(kBlack));
    myPDF->plotOn(Phi1frame, LineColor(kRed));
    
    TCanvas* cww = new TCanvas( "cww", "cww", 1000, 600 );

    cww->Divide(4,2);
    cww->cd(1);
    w1frame->Draw();
    cww->cd(2);
    w2frame->Draw();
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
    
    cww->Print(Form("epsfiles/angles_HZZ%.0f_%s_JHU_7DComplex_emfixyy.eps", mH, filemode.Data()));
    cww->Print(Form("pngfiles/angles_HZZ%.0f_%s_JHU_7DComplex_emfixyy.png", mH, filemode.Data()));
    
}
