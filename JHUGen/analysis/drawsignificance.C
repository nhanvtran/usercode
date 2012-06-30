//
// This code draws the various plots for the signal separtion
// run by root -l drawsignificance.C
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

void drawsingle(double higgsMass, double intLumi, int spin, int var, int toy);

void   drawsignificance ()
{
  
  double higgsMass = 125.;
  double intLumi = 20.;
  
  drawsingle(higgsMass, intLumi, zeroplus, DPHIMT, pure);
  drawsingle(higgsMass, intLumi, zeroplus, MLLMT, pure);

  drawsingle(higgsMass, intLumi, zerominus, DPHIMT, pure);
  drawsingle(higgsMass, intLumi, zerominus, MLLMT, pure);

  drawsingle(higgsMass, intLumi, twoplus, DPHIMT, pure);
  drawsingle(higgsMass, intLumi, twoplus, MLLMT, pure);

}

void drawsingle(double higgsMass, double intLumi, int spin, int var, int toy)
{

  gROOT->ProcessLine(".L ~/tdrstyle.C");
  gROOT->ProcessLine("setTDRStyle();");
  gROOT->ForceStyle();
  
  TString varName = getVarName(var);
  TString toyName = getToyName(toy);
  TString inputName = getInputName(spin);
  
  TString fileName = Form("significance_hww%.0f_%.0ffb_xwwcuts_%s_%s.root", higgsMass, intLumi, varName.Data(), inputName.Data());
  
  TFile *file = new TFile(fileName, "READ");
  std::cout << "Opening " << fileName << "\n";
  TNtuple *signifTuple = (TNtuple*) file->Get("signifTuple");
  assert(signifTuple);
  
  int nbins = 40;
  double xmin = 0.;
  double xmax = 10.;
  
  TH1F *sig = new TH1F("sig", "sig", nbins, xmin, xmax);
  signifTuple->Project("sig", "sig");
  sig->SetLineWidth(3);

  double mean = sig->GetMean();
  double err_mean = sig->GetMeanError();

  double rms = sig->GetRMS();
  double err_rms = sig->GetRMSError();
  
  double xtex = 0.86;
  double ytex_test = 0.86;
  double ytex_mean = 0.80;
  double ytex_rms = 0.75;

  if ( ( spin == zeroplus || spin == zerominus) && var == MLLMT ) 
    xtex = 0.50;

  
  TLatex* tex_test = new TLatex(xtex, ytex_test, Form("%s/%.0ffb/%s", getSpinName(spin).Data(), intLumi, varName.Data()));
  tex_test->SetTextAlign(32);
  tex_test->SetTextFont(42);
  tex_test->SetTextSize(.05);
  tex_test->SetNDC(1);


  TLatex* tex_mean = new TLatex(xtex, ytex_mean, Form("Mean = %.1f +/- %.1f", mean, err_mean));
  tex_mean->SetTextAlign(32);
  tex_mean->SetTextFont(42);
  tex_mean->SetTextSize(.05);
  tex_mean->SetNDC(1);


  TLatex* tex_rms = new TLatex(xtex, ytex_rms, Form("RMS = %.1f +/- %.1f", rms, err_rms));
  tex_rms->SetTextAlign(32);
  tex_rms->SetTextFont(42);
  tex_rms->SetTextSize(.05);
  tex_rms->SetNDC(1);

    

  //
  // Plotting stuff
  // 
  
  // set line color marker color etc
  sig->SetXTitle("Significance");
  sig->SetYTitle("experiments");

  TCanvas *c1 = new TCanvas("c1", "c1", 800, 600);
  sig->Draw("hist");
  tex_test->Draw("same");
  tex_mean->Draw("same");
  tex_rms->Draw("same");
  c1->SaveAs(Form("plots/epsfiles/sigificance_mH%.0f_%.0ffb_%s_%s.eps", higgsMass, intLumi, varName.Data(), inputName.Data()));
  c1->SaveAs(Form("plots/pngfiles/sigificance_mH%.0f_%.0ffb_%s_%s.png", higgsMass, intLumi, varName.Data(), inputName.Data()));

  
  // tidy up
  delete sig;
  delete c1;
  file->Close();
  
}
