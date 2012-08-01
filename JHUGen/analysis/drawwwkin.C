
#include "TFile.h"
#include "TTree.h"
#include "TLeaf.h"
#include <iostream>
#include "TH2F.h"
#include "TH1F.h"
#include "TString.h"
#include "TRint.h"
#include "TChain.h"
#include "TROOT.h"
#include "TStopwatch.h"
#include "TAxis.h"
#include "TCanvas.h"
#include "TPad.h"
#include "TLine.h"
#include "TLegend.h"
#include "TCut.h"
#include "THStack.h"


void drawsingle( int spin, TString varName, TString varTitle, int nbins, float xmin, float xmax);

void drawwwkin() {

  // spin = 3 is for WW 
  for (int spin = 0; spin < 4; spin ++ ) {
    drawsingle(spin, "mt", "WW Transverse Mass [GeV]", 20, 0, 125);
    drawsingle(spin, "mll", "Dilepton Mass [GeV]", 17, 12, 80.);
  }
}

void drawsingle( int spin, TString varName, TString varTitle, int nbins, float xmin, float xmax)
{
  gROOT->ProcessLine(".L ~/tdrstyle.C");
  gROOT->ProcessLine("setTDRStyle();");
  gROOT->ForceStyle();

  TString datadir = "datafiles/125/";
  
  
  TH1F *h1 = new TH1F("h1", "h1", nbins, xmin, xmax);
  h1->Sumw2();
  TH1F *h2 = new TH1F("h2", "h2", nbins, xmin, xmax);
  h2->Sumw2();
  TH1F *h3 = new TH1F("h3", "h3", nbins, xmin, xmax);
  h3->Sumw2();
  TH1F *h4 = new TH1F("h4", "h4", nbins, xmin, xmax);
  h4->Sumw2();


  if ( spin < 3 ) {
    TString fileName1;
    if ( spin == 0 ) 
      fileName1  = Form("%s/SMHiggsWW_125_JHU.root", datadir.Data());
    if ( spin == 1 ) 
      fileName1  = Form("%s/AVWW_125_JHU.root", datadir.Data());
    if ( spin == 2 ) 
      fileName1  = Form("%s/TWW_2mplus_125_JHU.root", datadir.Data());
    
    TFile *f1 = TFile::Open(fileName1, "READ");
    TTree *tree1 = (TTree*)f1->Get("angles");
    gROOT->cd();
    tree1->Project("h1", varName);
    f1->Close();
    
    TString fileName2;
    if ( spin == 0 ) 
      fileName2  = Form("%s/PSHiggsWW_125_JHU.root", datadir.Data());
    if ( spin == 1 ) 
      fileName2  = Form("%s/VWW_125_JHU.root", datadir.Data());
    if ( spin == 2 ) 
      fileName2  = Form("%s/TWW_2hminus_125_JHU.root", datadir.Data());
    
    TFile *file2 = TFile::Open(fileName2, "READ");
    TTree *tree2 = (TTree*)file2->Get("angles");
    gROOT->cd();
    tree2->Project("h2", varName);
    file2->Close();
    
    if ( spin != 1 ) {
      TString fileName3;
      if ( spin == 0 ) 
	fileName3  = Form("%s/SMHiggsWW_0hplus_125_JHU.root", datadir.Data());
      if ( spin == 2 ) 
	fileName3  = Form("%s/TWW_2hplus_125_JHU.root", datadir.Data());
      TFile *file3 = TFile::Open(fileName3, "READ");
      TTree *tree3 = (TTree*)file3->Get("angles");
      gROOT->cd();
      tree3->Project("h3", varName);
      file3->Close();
    }
  }

  if ( spin == 3 ) {
    TString fileName4;
    fileName4  = Form("%s/WW_madgraph_8TeV.root", datadir.Data());
    TFile *file4 = TFile::Open(fileName4, "READ");
    TTree *tree4 = (TTree*)file4->Get("angles");
    gROOT->cd();
    tree4->Project("h4", varName);
    file4->Close();
  }
    
  float leg_xmin = 0.25;
  float leg_xmax = 0.45;
  float leg_ymin = 0.7;
  float leg_ymax = 0.9;

  if ( varName.Contains("mll", TString::kExact)) {
    leg_xmin = 0.65;
    leg_xmax = 0.85;
  }
  
  TLegend *leg = new TLegend(leg_xmin, leg_ymin, leg_xmax, leg_ymax);
  leg->SetBorderSize(0);
  leg->SetFillStyle(0);
  leg->SetShadowColor(0);
  leg->SetTextSize(0.04);
  leg->SetTextFont(42);
  if ( spin <= 2) {
    leg->AddEntry(h1, Form("X(%i_{m}^{+})", spin), "l");
    leg->AddEntry(h2, Form("X(%i^{-})", spin), "l");
    if ( spin != 1 ) 
      leg->AddEntry(h3, Form("X(%i_{h}^{+})", spin), "l");
  } 

  if ( spin == 3 ) 
    leg->AddEntry(h4, "WW", "l");
  
  
  //
  // Plot
  // 

  if ( spin <= 2  ) {
    // J+
    h1->SetLineColor(kRed);
    h1->SetLineWidth(3);
    h1->Scale(1./h1->Integral(0, 1000));
    
    // J-
    h2->SetLineColor(kBlue);
    h2->SetLineWidth(3);
    h2->Scale(1./h2->Integral(0, 1000));
    
    // Jh+
    if ( spin != 1 ) {
      h3->SetLineColor(kGreen);
      h3->SetLineWidth(3);
      h3->Scale(1./h3->Integral(0, 1000));
    }
  } 

  if ( spin == 3 ) {
    // WW
    h4->SetLineColor(kBlack);
    h4->SetLineWidth(3);
    h4->Scale(1./h4->Integral(0, 1000));
  }
  
  float yMax;

  if ( spin <= 2 ) {
    yMax = h1->GetMaximum();
    yMax = yMax > h2->GetMaximum() ? yMax : h2->GetMaximum();
    if ( spin != 1 ) 
      yMax = yMax > h3->GetMaximum() ? yMax : h3->GetMaximum();
  }

  if ( spin == 3 ) 
    yMax = h4->GetMaximum();
  
  
  TCanvas *c1 = new TCanvas();
  h1->SetXTitle(varTitle);
  h1->SetYTitle("Normalized Entries");
  h1->SetMaximum(yMax*1.2);
  h1->SetMinimum(0);

  h4->SetXTitle(varTitle);
  h4->SetYTitle("Normalized Entries");
  h4->SetMaximum(yMax*1.2);
  h4->SetMinimum(0);

  
  if ( spin <= 2 ) {
    h1->Draw("hist");
    h2->Draw("samehist");
    if ( spin != 1 ) 
      h3->Draw("samehist");
    leg->Draw("same");
  }

  if ( spin == 3 ) 
    h4->Draw("hist");

  TString plotName = Form("%s_spin%i", varName.Data(), spin);
  if ( spin == 3 ) 
    plotName = Form("%s_WW", varName.Data()); 

  c1->SaveAs(Form("wwkinplots/%s.eps", plotName.Data()));
  c1->SaveAs(Form("wwkinplots/%s.png", plotName.Data()));

  delete h1;
  delete h2;
  delete h3;
  delete h4;
  delete c1;
  
}
