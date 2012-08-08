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

void plotData_qqWW() {
  
    gROOT->ProcessLine(".L tdrstyle.C");
    setTDRStyle();
    TGaxis::SetMaxDigits(3);
    gROOT->ForceStyle();
    
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


    // Grab input file to convert to RooDataSet
    TFile* fin = new TFile("WW_madgraph_8TeV.root");
    TTree* tin = (TTree*) fin->Get("angles");
    
    // for weighted events
    RooDataSet data("data","data",tin,RooArgSet(*m1,*m2,*h1,*h2,*hs,*Phi,*Phi1));
    

    // P L O T   . . . 
    double rescale = 0.0005;
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
    data.plotOn(h1frame, MarkerColor(kBlack),MarkerStyle(20),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
    if ( rescale != 1.) 
      h1frame->GetYaxis()->SetRangeUser(0, ymax_h1 * rescale * 1.3);
    
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
    data.plotOn(Phiframe, MarkerColor(kBlack),MarkerStyle(20),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
    if ( rescale != 1. )
      Phiframe->GetYaxis()->SetRangeUser(0, ymax_Phi *rescale * 1.3 );
    
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
    data.plotOn(hsframe, MarkerColor(kBlack),MarkerStyle(20),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
    if ( rescale != 1. )
      hsframe->GetYaxis()->SetRangeUser(0, ymax_hs * rescale * 1.3 );

    
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
    data.plotOn(Phi1frame, MarkerColor(kBlack),MarkerStyle(20),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
    if ( rescale != 1. )
      Phi1frame->GetYaxis()->SetRangeUser(0, ymax_Phi1 * rescale * 1.3);

    //
    // W mass
    // 
    RooPlot* w1frame =  m1->frame(50);
    w1frame->GetXaxis()->CenterTitle();
    w1frame->GetYaxis()->CenterTitle();
    w1frame->GetYaxis()->SetTitle(" ");
    
    double ymax_w1;
    TH1F *w1_sm = new TH1F("w1_sm", "w1_sm", 50, 1e-09, 120);
    tin->Project("w1_sm", "wplusmass");
    ymax_w1 = w1_sm->GetMaximum();
    data.plotOn(w1frame, MarkerColor(kBlack),MarkerStyle(20),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
    if ( rescale != 1. ) 
      w1frame->GetYaxis()->SetRangeUser(0, ymax_w1 * rescale * 1.3 );
    
    
    TCanvas* can =new TCanvas("can","can",600,600);
    
    w1frame->GetXaxis()->SetTitle("m_{l#nu} [GeV]");
    w1frame->Draw();
    can->SaveAs("paperplots/wplusmass_qqWW.eps");
    can->SaveAs("paperplots/wplusmass_qqWW.C");
    
    can->Clear();
    hsframe->Draw();
    can->SaveAs("paperplots/costhetastar_qqWW.eps");
    can->SaveAs("paperplots/costhetastar_qqWW.C");

    
    can->Clear();
    Phi1frame->Draw();
    can->SaveAs("paperplots/phistar1_qqWW.eps");
    can->SaveAs("paperplots/phistar1_qqWW.C");
    
    can->Clear();
    h1frame->GetXaxis()->SetTitle("cos#theta_{1} or cos#theta_{2}");
    h1frame->Draw();
    can->SaveAs("paperplots/costheta1_qqWW.eps");
    can->SaveAs("paperplots/costheta1_qqWW.C");

    can->Clear();
    Phiframe->Draw();
    can->SaveAs("paperplots/phi_qqWW.eps");
    can->SaveAs("paperplots/phi_qqWW.C");
    
}
