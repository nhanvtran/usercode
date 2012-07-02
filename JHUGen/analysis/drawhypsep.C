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

double intLumi = 10.;

void drawsingle(int test, int var, int toy);

void drawhypsep() {
  
  // drawsingle(zeroplusVSzerominus,MLLMT, pure);
  // drawsingle(zeroplusVSzerominus, DPHIMT, pure);

  drawsingle(zeroplusVStwoplus, DPHIMT, pure);
  drawsingle(zeroplusVStwoplus, MLLMT, pure);

  // drawsingle(zeroplusVSzerominus, MLL, pure);
  //  drawsingle(zeroplusVSzerominus, DPHI, pure);
  
  // drawsingle(zeroplusVStwoplus, DPHI, pure);
  // drawsingle(zeroplusVStwoplus, MLL, pure);

}

void drawsingle(int test, int var, int toy)
{

  gROOT->ProcessLine(".L ~/tdrstyle.C");
  gROOT->ProcessLine("setTDRStyle();");
  gROOT->ForceStyle();
  
  TString testName = getTestName(test);
  TString varName = getVarName(var);
  TString toyName = getToyName(toy);
    
  TString fileName = Form("stat_%s_%s_%s_%.0ffb.root", testName.Data(), toyName.Data(), varName.Data(), intLumi );
  TFile *file = new TFile(fileName, "READ");
  std::cout << "Opening " << fileName << "\n";
  TNtuple *hypTuple = (TNtuple*) file->Get("hypTuple");
  assert(hypTuple);

  
  int nbins = 100;
  double xmin = -10.;
  double xmax = 10.;

  if ( test & zeroplusVStwoplus) {
    if ( var == MLLMT) {
      xmin = -40.;
      xmax = 25.;
    } else {
      xmin = -25.;
      xmax = 25.;
    }
  }

  if ( (var & DPHIMT) && (test & zeroplusVSzerominus)) {
    xmin = -10.;
    xmax = 10.;
  }
   
  TCut cut("nSigFitH1>0.1");

  TH1F *S_H0 = new TH1F("S_H0", "S_H0", nbins, xmin, xmax);
  hypTuple->Project("S_H0", "S_H0", cut);
  S_H0->Fit("gaus");

  double mean_S_H0 = S_H0->GetMean();
  std::cout << "mean_S_H0 = " << mean_S_H0 << "\t";
  
  TH1F *S_H1 = new TH1F("S_H1", "S_H1", nbins, xmin, xmax);
  hypTuple->Project("S_H1", "S_H1", cut);
  S_H1->Fit("gaus");
  double mean_S_H1 = S_H1->GetMean();
  std::cout << "mean_S_H1 = " << mean_S_H1 << "\n";


  TH1F *nSigPullH0 = new TH1F("nSigPullH0", "nSigPullH0", 40, -5, 5);
  hypTuple->Project("nSigPullH0", "nSigPullH0", cut);
  nSigPullH0->Fit("gaus");
  double mean = nSigPullH0->GetMean();
  nSigPullH0->SetXTitle("[nSig(Fit) - nSig(In)]/#sigma nSig");
  nSigPullH0->SetYTitle("experiments");

  TH1F *nBkgPullH0 = new TH1F("nBkgPullH0", "nBkgPullH0", 40, -5, 5);
  hypTuple->Project("nBkgPullH0", "nBkgPullH0", cut);
  nBkgPullH0->Fit("gaus");
  mean = nBkgPullH0->GetMean();
  nBkgPullH0->SetXTitle("[nBkg(Fit) - nBkg(In)]/#sigma nBkg");
  nBkgPullH0->SetYTitle("experiments");


  TH1F *nSigPullH1 = new TH1F("nSigPullH1", "nSigPullH1", 40, -5, 5);
  hypTuple->Project("nSigPullH1", "nSigPullH1", cut);
  nSigPullH1->Fit("gaus");
  mean = nSigPullH1->GetMean();
  nSigPullH1->SetXTitle("[nSig(Fit) - nSig(In)]/#sigma nSig");
  nSigPullH1->SetYTitle("experiments");

  TH1F *nBkgPullH1 = new TH1F("nBkgPullH1", "nBkgPullH1", 40, -5, 5);
  hypTuple->Project("nBkgPullH1", "nBkgPullH1", cut);
  nBkgPullH1->Fit("gaus");
  mean = nBkgPullH1->GetMean();
  nBkgPullH1->SetXTitle("[nBkg(Fit) - nBkg(In)]/#sigma nBkg");
  nBkgPullH1->SetYTitle("experiments");



  //
  // Calculate separating in terms of sigma based on S_H0 and S_H1
  // 
  
  int nBins = S_H0->GetNbinsX();
  double norm0 = S_H0->Integral( 1, nBins );
  double norm1 = S_H1->Integral( 1, nBins );
  double int0(0.), int1(0.);
  double diff = 10.;
  double coverage = 0.;

  int nbin_eq = 0; 
  for (int i = 1; i <= nBins; i++){
    
    int0 = S_H0->Integral(1,i)/norm0;
    int1 = S_H1->Integral(i,nBins)/norm1;
    
    if (fabs(int0-int1) < diff){
      diff = fabs(int0-int1);
      coverage = 0.5*(int0+int1);
      nbin_eq = i;
    }
  }  
   
  std::cout << "coverage : " << coverage << ", for bin " << nbin_eq << "\n";
  sepH = 2*ROOT::Math::normal_quantile_c(1.0 - coverage, 1.0);
  std::cout << "histogram separatino is: " <<  sepH << ", with sigma coverage: " << coverage << std::endl;
  
  
  //
  // Plotting stuff
  // 
  
  // set line color marker color etc
  S_H0->SetLineColor(kBlue);
  S_H0->SetMarkerColor(kBlue);
  S_H1->SetLineColor(kRed);
  S_H1->SetMarkerColor(kRed);
  S_H0->SetXTitle("-2ln(L_{1}/L_{2})");
  S_H1->SetXTitle("-2ln(L_{1}/L_{2})");
  S_H0->SetYTitle("experiments");
  S_H1->SetYTitle("experiments");
  float yMax_S = S_H0->GetMaximum();
  yMax_S = yMax_S > S_H1->GetMaximum() ? yMax_S : S_H1->GetMaximum();


  TLegend *leg = new TLegend(0.65, 0.7, 0.85, 0.9);
  leg->SetFillColor(0);
  leg->SetTextSize(0.05);
  if ( test & zeroplusVSzerominus ) {
    leg->AddEntry(S_H0, "Hyp1: 0+", "lp");
    leg->AddEntry(S_H1, "Hyp2: 0-", "lp");
  }
  if ( test & zeroplusVStwoplus ) {
    leg->AddEntry(S_H0, "Hyp1: 0+", "lp");
    leg->AddEntry(S_H1, "Hyp2: 2+", "lp");
  }


  TLatex* tex_sepHeader = new TLatex(0.45, 0.88, Form("Seperation %.1f #sigma", sepH));
  tex_sepHeader->SetTextAlign(32);
  tex_sepHeader->SetTextFont(42);
  tex_sepHeader->SetTextSize(.05);
  tex_sepHeader->SetNDC(1);

  TLatex* tex_sepH = new TLatex(0.40, 0.83, Form("%.1f +/- %.1f #sigma", sepH, coverage));
  tex_sepH->SetTextAlign(32);
  tex_sepH->SetTextFont(42);
  tex_sepH->SetTextSize(.05);
  tex_sepH->SetNDC(1);


  TCanvas *c1 = new TCanvas("c1", "c1", 800, 600);
  S_H0->SetMarkerColor(kBlue);
  // S_H0->SetLineWidth(2.5);
  // S_H1->SetLineWidth(2.5);
  S_H0->SetMarkerStyle(24);
  S_H0->SetMaximum(yMax_S * 1.2);
  S_H0->Draw("e");
  S_H1->Draw("samee");
  leg->Draw("same");
  tex_sepHeader->Draw("same");
  c1->SaveAs(Form("plots/epsfiles/hypsep_%s_%s_%s_%.0ffb.eps", testName.Data(), toyName.Data(), varName.Data(), intLumi));
  c1->SaveAs(Form("plots/pngfiles/hypsep_%s_%s_%s_%.0ffb.png", testName.Data(), toyName.Data(), varName.Data(), intLumi));
  


  c1->Clear();
  nSigPullH0->SetMarkerColor(kRed);
  nSigPullH0->SetLineColor(kRed);
  nSigPullH0->Draw("e");
  c1->SaveAs(Form("plots/epsfiles/nsigpullH0_%s_%s_%s_%.0ffb.eps", testName.Data(), toyName.Data(), varName.Data(), intLumi));
  c1->SaveAs(Form("plots/pngfiles/nsigpullH0_%s_%s_%s_%.0ffb.png", testName.Data(), toyName.Data(), varName.Data(), intLumi));

  c1->Clear();
  nBkgPullH0->SetMarkerColor(kRed);
  nBkgPullH0->SetLineColor(kRed);
  nBkgPullH0->Draw("e");
  c1->SaveAs(Form("plots/epsfiles/nbkgpullH0_%s_%s_%s_%.0ffb.eps", testName.Data(), toyName.Data(), varName.Data(), intLumi));
  c1->SaveAs(Form("plots/pngfiles/nbkgpullH0_%s_%s_%s_%.0ffb.png", testName.Data(), toyName.Data(), varName.Data(), intLumi));


  c1->Clear();
  nSigPullH1->SetMarkerColor(kRed);
  nSigPullH1->SetLineColor(kRed);
  nSigPullH1->Draw("e");
  c1->SaveAs(Form("plots/epsfiles/nsigpullH1_%s_%s_%s_%.0ffb.eps", testName.Data(), toyName.Data(), varName.Data(), intLumi));
  c1->SaveAs(Form("plots/pngfiles/nsigpullH1_%s_%s_%s_%.0ffb.png", testName.Data(), toyName.Data(), varName.Data(), intLumi));

  c1->Clear();
  nBkgPullH1->SetMarkerColor(kRed);
  nBkgPullH1->SetMarkerColor(kRed);
  nBkgPullH1->Draw("e");
  c1->SaveAs(Form("plots/epsfiles/nbkgpullH1_%s_%s_%s_%.0ffb.eps", testName.Data(), toyName.Data(), varName.Data(), intLumi));
  c1->SaveAs(Form("plots/pngfiles/nbkgpullH1_%s_%s_%s_%.0ffb.png", testName.Data(), toyName.Data(), varName.Data(), intLumi));

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
