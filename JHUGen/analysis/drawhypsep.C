//
// This code draws the various plots for the signal separtion
// run by root -l drawhypsep.C 
// 

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
#include "TNtuple.h"
#include "enums.h"

double intLumi = 20.;

void drawsingle(int test, int var, int toy);

void drawhypsep() {
 
  drawsingle(zeroplusVSzerominus, MLL, pure);
  drawsingle(zeroplusVSzerominus, DPHIMT, pure);
  drawsingle(zeroplusVSzerominus, DPHI, pure);
  
  drawsingle(zeroplusVStwoplus, DPHIMT, pure);
  drawsingle(zeroplusVStwoplus, DPHI, pure);
  drawsingle(zeroplusVStwoplus, MLL, pure);
  
}

void drawsingle(int test, int var, int toy)
{

  gROOT->ProcessLine(".L ~/tdrstyle.C");
  gROOT->ProcessLine("setTDRStyle();");
  gROOT->ForceStyle();
  
  TString testName = getTestName(test);
  TString varName = getVarName(var);
  TString toyName = getToyName(toy);
    
  TString fileName = Form("stat_%s_%s_%s_%.0fb.root", testName.Data(), toyName.Data(), varName.Data(), intLumi );
  TFile *file = new TFile(fileName, "READ");
  std::cout << "Opening " << fileName << "\n";
  TNtuple *hypTuple = (TNtuple*) file->Get("hypTuple");
  assert(hypTuple);

  
  double xmin = -20.;
  double xmax = 20.;

  if ( test & zeroplusVStwoplus) {
    xmin = -100.;
    xmax = 100.;
  }
    

  TH1F *S_H0 = new TH1F("S_H0", "S_H0", 20, xmin, xmax);
  hypTuple->Project("S_H0", "S_H0");

  TH1F *S_H1 = new TH1F("S_H1", "S_H1", 20, xmin, xmax);
  hypTuple->Project("S_H1", "S_H1");



  TH1F *nSigPullH0 = new TH1F("nSigPullH0", "nSigPullH0", 20, -5, 5);
  hypTuple->Project("nSigPullH0", "nSigPullH0");
  nSigPullH0->SetXTitle("[nSig(Fit) - nSig(In)]/#sigma nSig");
  nSigPullH0->SetYTitle("experiments");

  TH1F *nBkgPullH0 = new TH1F("nBkgPullH0", "nBkgPullH0", 20, -5, 5);
  hypTuple->Project("nBkgPullH0", "nBkgPullH0");
  nBkgPullH0->SetXTitle("[nBkg(Fit) - nBkg(In)]/#sigma nBkg");
  nBkgPullH0->SetYTitle("experiments");


  TH1F *nSigPullH1 = new TH1F("nSigPullH1", "nSigPullH1", 20, -5, 5);
  hypTuple->Project("nSigPullH1", "nSigPullH1");
  nSigPullH1->SetXTitle("[nSig(Fit) - nSig(In)]/#sigma nSig");
  nSigPullH1->SetYTitle("experiments");

  TH1F *nBkgPullH1 = new TH1F("nBkgPullH1", "nBkgPullH1", 20, -5, 5);
  hypTuple->Project("nBkgPullH1", "nBkgPullH1");
  nBkgPullH1->SetXTitle("[nBkg(Fit) - nBkg(In)]/#sigma nBkg");
  nBkgPullH1->SetYTitle("experiments");

  
  // set line color marker color etc
  S_H0->SetLineColor(kRed);
  S_H0->SetMarkerColor(kRed);
  S_H1->SetLineColor(kBlue);
  S_H1->SetMarkerColor(kBlue);
  S_H0->SetXTitle("2lnL_{1}/L_{2}");
  S_H1->SetXTitle("2lnL_{1}/L_{2}");
  S_H0->SetYTitle("experiments");
  S_H1->SetYTitle("experiments");
  float yMax_S = S_H0->GetMaximum();
  yMax_S = yMax_S > S_H1->GetMaximum() ? yMax_S : S_H1->GetMaximum();


  TLegend *leg = new TLegend(0.65, 0.7, 0.85, 0.9);
  leg->SetFillColor(0);
  if ( test & zeroplusVSzerominus ) {
    leg->AddEntry(S_H0, "Hyp1: 0+", "lp");
    leg->AddEntry(S_H1, "Hyp2: 0-", "lp");
  }
  if ( test & zeroplusVStwoplus ) {
    leg->AddEntry(S_H0, "Hyp1: 0+", "lp");
    leg->AddEntry(S_H1, "Hyp2: 2+", "lp");
  }

  TCanvas *c1 = new TCanvas();
  S_H0->SetMaximum(yMax_S * 1.1);
  S_H0->Draw("histe");
  S_H1->Draw("samehiste");
  leg->Draw("same");
  c1->SaveAs(Form("plots/epsfiles/hypsep_%s_%s_%s.eps", testName.Data(), toyName.Data(), varName.Data()));
  c1->SaveAs(Form("plots/pngfiles/hypsep_%s_%s_%s.png", testName.Data(), toyName.Data(), varName.Data()));
  

  c1->Clear();
  nSigPullH0->Draw("histe");
  c1->SaveAs(Form("plots/epsfiles/nsigpullH0_%s_%s_%s.eps", testName.Data(), toyName.Data(), varName.Data()));
  c1->SaveAs(Form("plots/pngfiles/nsigpullH0_%s_%s_%s.png", testName.Data(), toyName.Data(), varName.Data()));

  c1->Clear();
  nBkgPullH0->Draw("histe");
  c1->SaveAs(Form("plots/epsfiles/nbkgpullH0_%s_%s_%s.eps", testName.Data(), toyName.Data(), varName.Data()));
  c1->SaveAs(Form("plots/pngfiles/nbkgpullH0_%s_%s_%s.png", testName.Data(), toyName.Data(), varName.Data()));


  c1->Clear();
  nSigPullH1->Draw("histe");
  c1->SaveAs(Form("plots/epsfiles/nsigpullH1_%s_%s_%s.eps", testName.Data(), toyName.Data(), varName.Data()));
  c1->SaveAs(Form("plots/pngfiles/nsigpullH1_%s_%s_%s.png", testName.Data(), toyName.Data(), varName.Data()));

  c1->Clear();
  nBkgPullH1->Draw("histe");
  c1->SaveAs(Form("plots/epsfiles/nbkgpullH1_%s_%s_%s.eps", testName.Data(), toyName.Data(), varName.Data()));
  c1->SaveAs(Form("plots/pngfiles/nbkgpullH1_%s_%s_%s.png", testName.Data(), toyName.Data(), varName.Data()));



  // tidy up
  delete S_H0;
  delete S_H1;
  delete nSigPullH0;
  delete nBkgPullH0;
  delete nSigPullH1;
  delete nBkgPullH1;
  delete c1;
  file->Close();

}
