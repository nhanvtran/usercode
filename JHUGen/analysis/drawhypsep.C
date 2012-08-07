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

// 
// gloabl variables
// 
double intLumi = 20.;
bool drawpaper = true;


void drawsingle(int test, int var, int toy);
int getMedianBin(TH1F& *h);
void drawhypsep() {

  drawsingle(zeroplusVStwoplus, MLLMT, pure);

  drawsingle(zeroplusVSzerominus,MLLMT, pure);
  drawsingle(zeroplusVSzerohplus, MLLMT, pure);
  
  drawsingle(zeroplusVSoneplus, MLLMT, pure);
  drawsingle(zeroplusVSoneminus, MLLMT, pure);

  drawsingle(zeroplusVStwoplus, MLLMT, pure);
  drawsingle(zeroplusVStwohplus, MLLMT, pure);
  drawsingle(zeroplusVStwohminus, MLLMT, pure);

}

void drawsingle(int test, int var, int toy)
{
  gROOT->ProcessLine(".L ~/tdrstyle.C");
  gROOT->ProcessLine("setTDRStyle();");

  gStyle->SetPadRightMargin(0.05);
  gStyle->SetPadLeftMargin(0.13);
  gStyle->SetPadBottomMargin(0.15);
  gStyle->SetTitleXOffset(1.1);                                                                                   
  gStyle->SetTitleYOffset(1.1);
  TGaxis *gaxis = new TGaxis();
  gaxis->SetMaxDigits(3);
  gROOT->ForceStyle();


  TString testName = getTestName(test);
  TString varName = getVarName(var);
  TString toyName = getToyName(toy);
    
  TString fileName = Form("stat_%s_%s_%s_%.0ffb.root", testName.Data(), toyName.Data(), varName.Data(), intLumi );
  TFile *file = new TFile(fileName, "READ");
  std::cout << "Opening " << fileName << "\n";
  TNtuple *hypTuple = (TNtuple*) file->Get("hypTuple");
  assert(hypTuple);

  
  int nbins = 200;
  double xmin = -20.;
  double xmax = 20.;

  switch (test) {
  case zeroplusVSoneminus:
  case zeroplusVStwohminus:
  case zeroplusVStwoplus:
    xmin = -30.;
    xmax = 30.;
    break;
  default:
    break;
  }
  
  
  // TCut cut("nSigFitH1>0.1");
  TCut cut("1");

  TH1F *S_H0 = new TH1F("S_H0", "S_H0", nbins, xmin, xmax);
  hypTuple->Project("S_H0", "S_H0", cut);
  
  double mean_S_H0 = S_H0->GetMean();
  std::cout << "mean_S_H0 = " << mean_S_H0 << "\t";
  
  TH1F *S_H1 = new TH1F("S_H1", "S_H1", nbins, xmin, xmax);
  hypTuple->Project("S_H1", "S_H1", cut);
  
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
  double sepH = 2*ROOT::Math::normal_quantile_c(1.0 - coverage, 1.0);
  std::cout << "histogram separatino is: " <<  sepH << ", with sigma coverage: " << coverage << std::endl;
  
  // 
  // Calculate the fraction of events of the hypothesis 2 in the hyp1's plot
  //
  int bin_median_H1 = getMedianBin(S_H1);
  std::cout << "bin_median_H1 = " << bin_median_H1 << "\n";
  
  double frac_H0_beyondH1Median = S_H0->Integral(bin_median_H1, nBins) / norm0;
  double sepH0vsH1 = ROOT::Math::normal_quantile_c(frac_H0_beyondH1Median, 1.0);
  std::cout << "frac of H0 histogram beyond the H1 median " << frac_H0_beyondH1Median << ", correspond to " << sepH0vsH1 << " sigma\n";
  

  int bin_median_H0 = getMedianBin(S_H0);
  std::cout << "bin_median_H0 = " << bin_median_H0 << "\n";
  
  double frac_H1_beyondH0Median = S_H1->Integral(1, bin_median_H0) / norm1;
  double sepH1vsH0 = ROOT::Math::normal_quantile_c(frac_H1_beyondH0Median, 1.0);
  std::cout << "frac of H1 histogram beyond the H0 median " << frac_H1_beyondH0Median << ", correspond to " << sepH1vsH0 << " sigma\n";
  //
  // Plotting stuff
  // 
  // set line color marker color etc
  // set line color marker color etc
  S_H0->SetLineColor(kRed);
  S_H0->SetMarkerColor(kRed);
  S_H0->SetMarkerStyle(8);
  S_H0->SetXTitle("-2ln(L_{1}/L_{2})");
  S_H0->SetYTitle("experiments");
  S_H0->GetXaxis()->CenterTitle();
  S_H0->GetYaxis()->CenterTitle();

  S_H1->SetMarkerStyle(24);
  S_H1->SetLineColor(kBlue);
  S_H1->SetMarkerColor(kBlue);
  S_H1->SetXTitle("-2ln(L_{1}/L_{2})");
  S_H1->SetYTitle("experiments");
  S_H1->GetXaxis()->CenterTitle();
  S_H1->GetYaxis()->CenterTitle();

  TLegend *leg = new TLegend(0.68, 0.7, 0.8, 0.9);
  leg->SetFillColor(0);
  leg->SetTextSize(0.05);
  leg->SetTextFont(42);
  leg->AddEntry(S_H0, "Hyp1: 0m+", "lp");
  switch (test ) {
  case zeroplusVSzerominus:
    leg->AddEntry(S_H1, "Hyp2: 0-", "lp");
    break;
  case zeroplusVSzerohplus:
    leg->AddEntry(S_H1, "Hyp2: 0h+", "lp");
    break;
  case zeroplusVSoneplus:
    leg->AddEntry(S_H1, "Hyp2: 1+", "lp");
    break;
  case zeroplusVSoneminus:
    leg->AddEntry(S_H1, "Hyp2: 1-", "lp");
    break;
  case zeroplusVStwoplus:
    leg->AddEntry(S_H1, "Hyp2: 2+", "lp");
    break;
  case zeroplusVStwohplus:
    leg->AddEntry(S_H1, "Hyp2: 2h+", "lp");
    break;
  case zeroplusVStwohminus:
    leg->AddEntry(S_H1, "Hyp2: 2h-", "lp");
    break;
  default:
    break;
  }

  TLatex* tex_sepH = new TLatex(0.2, 0.85, Form("S = %.1f #sigma", sepH));
  tex_sepH->SetTextFont(42);
  tex_sepH->SetTextSize(.05);
  tex_sepH->SetNDC(1);
  
  TLatex* tex_sepH0vsH1 = new TLatex(0.2, 0.80, Form("S_{1} =  %.1f #sigma", sepH0vsH1));
  tex_sepH0vsH1->SetTextFont(42);
  tex_sepH0vsH1->SetTextSize(.05);
  tex_sepH0vsH1->SetNDC(1);

  TLatex* tex_sepH1vsH0 = new TLatex(0.2, 0.75, Form("S_{2} = %.1f #sigma", sepH1vsH0));
  tex_sepH1vsH0->SetTextFont(42);
  tex_sepH1vsH0->SetTextSize(.05);
  tex_sepH1vsH0->SetNDC(1);

  /*
  if ( nbins > 200 ) {
    S_H0->Rebin(int(nbins/200));
    S_H1->Rebin(int(nbins/200));
  }
  */
  
  float yMax_S = S_H0->GetMaximum();
  yMax_S = yMax_S > S_H1->GetMaximum() ? yMax_S : S_H1->GetMaximum();
  S_H0->SetMaximum(yMax_S * 1.1);
  
  //added by sara
  double xline= S_H0->GetBinCenter(nbin_eq)+ S_H0->GetBinWidth(1)/2.;
  double yline= S_H0->GetMaximum();
  TLine *line = new TLine(xline,yline,xline,0);
  double xline0=  S_H0->GetBinCenter(bin_median_H0 )+ S_H0->GetBinWidth(1)/2.;
  line->SetLineWidth(2);
  TLine *line0 = new TLine(xline0,yline,xline0,0);
  line0->SetLineStyle(2);
  line0->SetLineWidth(2);
  double xline1=  S_H1->GetBinCenter(bin_median_H1) - S_H1->GetBinWidth(1)/2.;
  TLine *line1 = new TLine(xline1,yline,xline1,0);
  line1->SetLineStyle(2);
  line1->SetLineWidth(2);

    TH1F *S_H1_tail = new TH1F("S_H1_tail", "S_H1_tail", nbin_eq, xmin, S_H1->GetBinCenter(nbin_eq)+S_H1->GetBinWidth(nbin_eq)/2.);
  for (int i=0;i<=nbin_eq;i++){
    S_H1_tail->SetBinContent(i,S_H1->GetBinContent(i));
  }
  
  S_H1_tail->SetFillColor(kBlue);
  S_H1_tail->SetLineColor(kWhite);
  S_H1_tail->SetFillStyle(3244);

  double xmaxH1=S_H1->GetBinCenter(bin_median_H0)+S_H1->GetBinWidth(bin_median_H0)/2.;
  TH1F *S_H1_tailSmall = new TH1F("S_H1_tailSmall", "S_H1_tailSmall", (int)((xmaxH1-xmin)/S_H1->GetBinWidth(1)), xmin, xmaxH1);
  for (int i=0;i<=(bin_median_H0);i++){
      S_H1_tailSmall->SetBinContent(i,S_H1->GetBinContent(i));
  }
  S_H1_tailSmall->SetFillColor(kBlue);
  S_H1_tailSmall->SetLineColor(kBlue);

  TH1F *S_H0_tail = new TH1F("S_H0_tail", "S_H0_tail", nbin_eq, S_H0->GetBinCenter(nbin_eq)+S_H0->GetBinWidth(nbin_eq)/2.,xmax);
  for (int i=1;i<=nbin_eq;i++){
    if(i+nbin_eq<(nbins+1))
      S_H0_tail->SetBinContent(i,S_H0->GetBinContent(i+nbin_eq));
  }
  S_H0_tail->SetFillColor(kRed);
  S_H0_tail->SetLineColor(kWhite);
  S_H0_tail->SetFillStyle(3244);

  double xminH0=S_H0->GetBinCenter(bin_median_H1)-S_H0->GetBinWidth(bin_median_H1)/2.,
    TH1F *S_H0_tailSmall = new TH1F("S_H0_tailSmall", "S_H0_tailSmall", (int)((xmax-xminH0)/S_H0->GetBinWidth(1)),xminH0, xmax);
  for (int i=0;i<=bin_median_H1;i++){
    S_H0_tailSmall->SetBinContent(i,S_H0->GetBinContent(i+bin_median_H1-1));
  }
  S_H0_tailSmall->SetFillColor(kRed);
  S_H0_tailSmall->SetLineColor(kRed);


  TCanvas *c1 = new TCanvas("c1", "c1", 800, 800);
  S_H0->Draw("e");
  S_H1_tail->Draw("same");
  S_H0_tail->Draw("same");
  S_H1_tailSmall->Draw("same");
  S_H0_tailSmall->Draw("same");
  S_H0->Draw("samee");
  S_H1->Draw("samee");
  line->Draw("same");
  line0->Draw("same");
  line1->Draw("same");
  
  if ( ! drawpaper ) {
    S_H0->Fit("gaus");
    S_H1->Fit("gaus");
    leg->Draw("same");
    tex_sepH->Draw("same");
    tex_sepH0vsH1->Draw("same");
    tex_sepH1vsH0->Draw("same");
  }
  c1->SaveAs(Form("plots/epsfiles/hypsep_%s_%s_%s_%.0ffb.eps", testName.Data(), toyName.Data(), varName.Data(), intLumi));
  c1->SaveAs(Form("plots/pngfiles/hypsep_%s_%s_%s_%.0ffb.png", testName.Data(), toyName.Data(), varName.Data(), intLumi));
  if ( drawpaper ) {
    c1->SaveAs(Form("paperplots/hypsep_%s_%s_%s_%.0ffb.eps", testName.Data(), toyName.Data(), varName.Data(), intLumi));
    c1->SaveAs(Form("paperplots/hypsep_%s_%s_%s_%.0ffb.png", testName.Data(), toyName.Data(), varName.Data(), intLumi));
    c1->SaveAs(Form("paperplots/hypsep_%s_%s_%s_%.0ffb.C", testName.Data(), toyName.Data(), varName.Data(), intLumi));
  }


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


int getMedianBin(TH1F& *h) {
  
  if ( h == 0 ) {
    return 0;
  }
  int nBins = h->GetNbinsX();
  
  double norm = h->Integral(1, nBins);
  int bin_median = 1;
  double diff = 1;

  for ( int i = 1; i < nBins; i++) {
    double frac = h->Integral(1, i) / norm;
    double diff_bin = fabs(frac - 0.5 );
    if ( diff_bin < diff ) {
      diff = diff_bin;
      bin_median = i;
    }
    // std::cout << "Bin " << i << ", frac " << frac << ", diff_bin " << diff_bin << "\n";
  }
  
  return bin_median;
}


