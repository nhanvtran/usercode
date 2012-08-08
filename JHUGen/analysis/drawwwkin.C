
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
#include "enums.h"


void drawsingle( int spin, TString varName, TString varTitle, int nbins, float xmin, float xmax);
void drawsingleforpaper(TString varName, TString varTitle, int nbins, float xmin, float xmax);
void drawsingle2d(int hypType); 
void drawwwkin() {

  bool drawpaper = true;

  // arbitary rescale to make the maximum ~ 1.
  drawsingle2d(zeroplus);
  drawsingle2d(twoplus);
  drawsingle2d(twohplus);
  drawsingle2d(ww);

  
  if ( drawpaper ) {
    drawsingleforpaper("mt", "m_{T} [GeV]", 10, 50, 130);
    drawsingleforpaper("mll", "m_{ll} [GeV]", 10, 10, 90);
    drawsingleforpaper("dphill", "#Delta#phi_{ll}", 20, 0, TMath::Pi());

  }

  if ( ! drawpaper ) {
    // spin = 3 is for WW 
    for (int spin = 0; spin < 4; spin ++ ) {
      drawsingle(spin, "mt", "m_{T} [GeV]", 10, 50, 130);
      drawsingle(spin, "mll", "m_{ll} [GeV]", 10, 10, 90.);
    }
  }

  
}

void drawsingle2d(int hypType) {
  gROOT->ProcessLine(".L ~/tdrstyle.C");
  gROOT->ProcessLine("setTDRStyle();");
  gStyle->SetPadRightMargin(0.15);
  gStyle->SetPadBottomMargin(0.15);
  gStyle->SetTitleXOffset(1.1);                                                                                   
  TGaxis::SetMaxDigits(3);
  gStyle->SetNdivisions(505, "Z");                                               
  gROOT->ForceStyle();


  TString datadir = "datafiles/125/";
    
  TH2F *h2 = new TH2F("h2","h2", 10, 50, 130, 10, 10, 90);
  TString inputName = getInputName(hypType);
  TString fileName; 
  if ( hypType != ww )
    fileName = Form("%s/%s_125_JHU.root", datadir.Data(),  inputName.Data()); 
  else 
    fileName = Form("%s/%s.root", datadir.Data(),  inputName.Data()); 

  TFile *f = TFile::Open(fileName, "READ");
  TTree *tree = (TTree*)f->Get("angles");
  gROOT->cd();
  tree->Project("h2", "mll:mt");
  f->Close();
  
  h2->Scale(1./h2->GetMaximum());
  

  TCanvas *c1 = new TCanvas();
  h2->SetXTitle("m_{T} [GeV]");
  h2->SetYTitle("m_{ll} [GeV]");
  h2->GetXaxis()->CenterTitle();
  h2->GetYaxis()->CenterTitle();
  h2->Draw("colz");
  c1->SaveAs(Form("paperplots/mtvsmll_%s.eps", inputName.Data()));
  c1->SaveAs(Form("paperplots/mtvsmll_%s.png", inputName.Data()));
  c1->SaveAs(Form("paperplots/mtvsmll_%s.C", inputName.Data()));
	     

  delete c1;
  delete h2;

  
}
void drawsingle( int spin, TString varName, TString varTitle, int nbins, float xmin, float xmax)
{
  gROOT->ProcessLine(".L tdrstyle.C");
  gROOT->ProcessLine("setTDRStyle();");
  gStyle->SetPadRightMargin(0.05);
  gStyle->SetPadLeftMargin(0.16);
  gStyle->SetPadBottomMargin(0.14);
  gStyle->SetTitleXOffset(1.0);                                                                                   
  gStyle->SetTitleYOffset(1.4);                                                                                   
  TGaxis::SetMaxDigits(3);
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
    // fileName4  = Form("%s/WW_madgraph_8TeV.root", datadir.Data());
    fileName4  = Form("%s/WW_madgraph_8TeV_0j.root", datadir.Data());
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
  

  
  
  //
  // Plot
  // 

  if ( spin <= 2  ) {
    // J+
    h1->SetLineColor(kRed);
    h1->SetMarkerColor(kRed);
    h1->SetLineWidth(2);
    h1->SetMarkerStyle(4);
    h1->SetMarkerSize(1.5);
    h1->Scale(1./h1->Integral(0, 1000));
    
    // J-
    h2->SetLineColor(kBlue);
    h2->SetMarkerColor(kBlue);
    h2->SetLineWidth(2);
    h2->SetMarkerStyle(27);
    h2->SetMarkerSize(1.5);
    h2->Scale(1./h2->Integral(0, 1000));
    
    // Jh+
    if ( spin != 1 ) {
      h3->SetLineColor(kGreen+3);
      h3->SetMarkerColor(kGreen+3);
      h3->SetLineWidth(2);
      h3->SetMarkerStyle(25);
      h3->SetMarkerSize(1.5);
      h3->Scale(1./h2->Integral(0, 1000));
      h3->Scale(1./h3->Integral(0, 1000));
    }
  } 

  if ( spin == 3 ) {
    // WW
    h4->SetLineColor(kBlack);
    h4->SetMarkerColor(kBlack);
    h4->SetLineWidth(2);
    h4->SetMarkerStyle(20);
    h4->SetMarkerSize(1.5);
    h4->Scale(1./h4->Integral(0, 1000));
  }
  
  TLegend *leg = new TLegend(leg_xmin, leg_ymin, leg_xmax, leg_ymax);
  leg->SetBorderSize(0);
  leg->SetFillStyle(0);
  leg->SetShadowColor(0);
  leg->SetTextSize(0.04);
  leg->SetTextFont(42);
  if ( spin <= 2) {
    leg->AddEntry(h1, Form("X(%i_{m}^{+})", spin), "lp");
    leg->AddEntry(h2, Form("X(%i^{-})", spin), "lp");
    if ( spin != 1 ) 
      leg->AddEntry(h3, Form("X(%i_{h}^{+})", spin), "lp");
  } 

  if ( spin == 3 ) 
    leg->AddEntry(h4, "WW", "lp");

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
  // h1->SetYTitle("normalized entries");
  h1->GetXaxis()->CenterTitle();  
  h1->GetYaxis()->CenterTitle();
  h1->SetMaximum(yMax*1.2);
  h1->SetMinimum(0);

  h4->SetXTitle(varTitle);
  // h4->SetYTitle("normalized entries");
  h4->SetMaximum(yMax*1.2);
  h4->SetMinimum(0);
  h4->GetXaxis()->CenterTitle();  
  h4->GetYaxis()->CenterTitle();
  
  if ( spin <= 2 ) {
    h1->Draw("h");
    h2->Draw("sameh");
    if ( spin != 1 ) 
      h3->Draw("sameh");
    // leg->Draw("same");
  }

  if ( spin == 3 ) 
    h4->Draw("h");

  TString plotName = Form("%s_spin%i", varName.Data(), spin);
  if ( spin == 3 ) 
    plotName = Form("%s_WW", varName.Data()); 

  c1->SaveAs(Form("paperplots/%s.eps", plotName.Data()));
  c1->SaveAs(Form("paperplots/%s.png", plotName.Data()));
  c1->SaveAs(Form("paperplots/%s.C", plotName.Data()));

  delete h1;
  delete h2;
  delete h3;
  delete h4;
  delete c1;
  
}

void drawsingleforpaper(TString varName, TString varTitle, int nbins, float xmin, float xmax)
{
  gROOT->ProcessLine(".L tdrstyle.C");
  gROOT->ProcessLine("setTDRStyle();");
  TGaxis::SetMaxDigits(3);
  gStyle->SetNdivisions(505, "XY");
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
  
  
  TString fileName1 = Form("%s/SMHiggsWW_125_JHU.root", datadir.Data());
  TFile *f1 = TFile::Open(fileName1, "READ");
  TTree *tree1 = (TTree*)f1->Get("angles");
  gROOT->cd();
  tree1->Project("h1", varName);
  f1->Close();
  
  TString fileName2 = Form("%s/TWW_2hminus_125_JHU.root", datadir.Data());
  TFile *file2 = TFile::Open(fileName2, "READ");
  TTree *tree2 = (TTree*)file2->Get("angles");
  gROOT->cd();
  tree2->Project("h2", varName);
  file2->Close();
  
  // TString fileName3 = Form("%s/WW_madgraph_8TeV.root", datadir.Data());
  TString fileName3 = Form("%s/WW_madgraph_8TeV_0j.root", datadir.Data());
  TFile *file3 = TFile::Open(fileName3, "READ");
  TTree *tree3 = (TTree*)file3->Get("angles");
  gROOT->cd();
  tree3->Project("h3", varName);
  file3->Close();
  
  TString fileName4 = Form("%s/TWW_2hplus_125_JHU.root", datadir.Data());
  TFile *file4 = TFile::Open(fileName4, "READ");
  TTree *tree4 = (TTree*)file4->Get("angles");
  gROOT->cd();
  tree4->Project("h4", varName);
  file4->Close();
  


  //
  // Plot
  // 

  // 0m+
  h1->SetLineColor(2);
  h1->SetMarkerColor(2);
  h1->SetLineWidth(2);
  h1->SetMarkerStyle(4);
  h1->SetMarkerSize(1.5);
  h1->Scale(1./h1->Integral(0, 1000));
  h1->SetLineStyle(1);

  
  // 2m+
  h2->SetLineColor(kBlue);
  h2->SetMarkerColor(kBlue);
  h2->SetLineWidth(2);
  h2->SetMarkerStyle(32);
  h2->SetMarkerSize(1.5);
  h2->Scale(1./h2->Integral(0, 1000));
  
  // WW
  h3->SetLineColor(kBlack);
  h3->SetMarkerColor(kBlack);
  h3->SetLineWidth(2);
  h3->SetMarkerStyle(20);
  h3->SetMarkerSize(1.5);
  h3->Scale(1./h3->Integral(0, 1000));

  // 2h+
  h4->SetLineColor(kGreen+3);
  h4->SetMarkerColor(kGreen+3);
  h4->SetLineWidth(2);
  h4->SetMarkerStyle(27);
  h4->SetMarkerSize(1.5);
  h4->Scale(1./h4->Integral(0, 1000));
  
  float yMax;

  yMax = h1->GetMaximum();
  yMax = yMax > h2->GetMaximum() ? yMax : h2->GetMaximum();
  yMax = yMax > h3->GetMaximum() ? yMax : h3->GetMaximum();


  h1->SetXTitle(varTitle);
  // h1->SetYTitle("normalized entries");
  h1->GetXaxis()->CenterTitle();  
  h1->GetYaxis()->CenterTitle();
  h1->SetMaximum(yMax*1.3);
  h1->SetMinimum(0);

  h2->SetMinimum(0);
  h3->SetMinimum(0);
  h4->SetMinimum(0);
  
  TCanvas *c1 = new TCanvas();
  h1->Draw("h");
  h2->Draw("sameh");
  h3->Draw("sameh");
  
  TString plotName = Form("%s_XWW", varName.Data());
  
  c1->SaveAs(Form("paperplots/%s.eps", plotName.Data()));
  c1->SaveAs(Form("paperplots/%s.png", plotName.Data()));
  c1->SaveAs(Form("paperplots/%s.C", plotName.Data()));

  c1->Clear();
  
  yMax = yMax > h4->GetMaximum() ? yMax : h4->GetMaximum();

  h1->SetXTitle(varTitle);
  // h1->SetYTitle("normalized entries");
  h1->GetXaxis()->CenterTitle();  
  h1->GetYaxis()->CenterTitle();
  h1->SetMaximum(yMax*1.2);
  h1->SetMinimum(0);
  h1->Draw("h");
  h2->Draw("sameh");
  h3->Draw("sameh");
  h4->Draw("sameh");
  c1->SaveAs(Form("paperplots/%s_with2hplus.eps", plotName.Data()));
  c1->SaveAs(Form("paperplots/%s_with2hplus.png", plotName.Data()));
  c1->SaveAs(Form("paperplots/%s_with2hplus.C", plotName.Data()));
  

  delete h1;
  delete h2;
  delete h3;
  delete h4;
  delete c1;
  
}
