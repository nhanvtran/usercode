#include "TChain.h"
#include "TH1F.h"
#include "TCanvas.h"
#include "TROOT.h"
#include "TLegend.h"
#include "THStack.h"
#include "TStyle.h"
#include "TLatex.h"
#include "TFile.h"
#include "TTree.h"
#include "TArrow.h"
#include "TStyle.h"
#include <vector>
#include <math.h>
#include <iostream>
#include <fstream>
#include "TH2F.h"
#include "TF1.h"
#include "Math/LorentzVector.h"
#include "TMath.h"
#include "Math/VectorUtil.h"

typedef ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double> > LorentzVector; 

void createPlot(std::vector<TString> samples, std::vector<TString> files, std::vector<TString> legend);
void drawsingle(TString var, const int nHist, TH1F** hist, std::vector<TString> samples, std::vector<TString> legend, TString x_title);
bool higgselection(int mH, double mt, double mll, double dphill, double leadleppt, double trailleppt);

// WW process for the 6 final states
// 61 '  f(p1)+f(p2) --> W^+(-->nu(p3)+e^+(p4)) +W^-(-->e^-(p5)+nu~(p6))' 'N'
int mH = 125;

TFile *output_file = new TFile("samplecomparison.root", "RECREATE");
ofstream text; 

void comparesample()
{  
  // load macros  
  gROOT->ProcessLine(".L ~/tdrstyle.C");
  gROOT->ProcessLine("setTDRStyle()"); 
  
  // load macros  
  std::vector<TString> samples;
  std::vector<TString> files;
  std::vector<TString> legend;
  
  samples.push_back("SMHiggs");
  files.push_back(Form("SMHiggsWW_%i_JHU.root", mH));
  legend.push_back("SMHiggs JP = 0+");

  samples.push_back("PSHiggs");
  files.push_back(Form("PSHiggsWW_%i_JHU.root", mH));
  legend.push_back("PSHiggs JP = 0-");

  samples.push_back("T");
  files.push_back(Form("TWW_%i_JHU.root", mH));
  legend.push_back("Tensor X JP = 2+");

  samples.push_back("WW");
  files.push_back(Form("WW_MCFM.root", mH));
  legend.push_back("Non-resonant WW");
  


  createPlot(samples, files, legend);

}

void createPlot(std::vector<TString> samples, std::vector<TString> files, std::vector<TString> legend)
{

  TString y_title = "Number of Entries";
  const int nHist = files.size(); // number of files

  // Declare the histograms to be saved 
  TH1F *h_mll[nHist];
  TH1F *h_dilpt[nHist];
  TH1F *h_dphill[nHist];
  TH1F *h_leadleppt[nHist];
  TH1F *h_trailleppt[nHist];
  TH1F *h_met[nHist];
  TH1F *h_mt[nHist];
  
  // Get the histograms from the ntuples
  for (int i=0;i<nHist;i++) {
    TString treeName = "angles";
    TChain *chain = new TChain(treeName);
    chain->Add(files[i]);
    assert(chain);
    
    // declare histograms  to fill
    Color_t color = kBlack;
    TString sampleName = samples[i];
    if ( sampleName.Contains("SMHiggs",TString::kExact )) color = kBlue;
    if ( sampleName.Contains("PSHiggs", TString::kExact)) color = kMagenta;
    if ( sampleName.Contains("T",  TString::kExact)) color = kRed;
    if ( sampleName.Contains("THiggs",  TString::kExact)) color = kRed;


    
    // define the histograms to plot
    
    // dilmass 
    h_mll[i] = new TH1F(TString("HWW_"+sampleName+"_hdilmass"), TString("HWW_"+sampleName+"_hdilmass"), 20, 0, 200);
    h_mll[i]->SetLineColor(color);
    h_mll[i]->SetMarkerColor(color);
    
    // leading lepton pT
    h_leadleppt[i] = new TH1F(TString("HWW_"+sampleName+"_hleadleppt"), TString("HWW_"+sampleName+"_hleadleppt"), 20, 0, 100);
    h_leadleppt[i]->SetLineColor(color);
    h_leadleppt[i]->SetMarkerColor(color);
   
    // trailing lepton pT
    h_trailleppt[i] = new TH1F(TString("HWW_"+sampleName+"_htrailleppt"), TString("HWW_"+sampleName+"_htrailleppt"), 20, 0, 100);
    h_trailleppt[i]->SetLineColor(color);
    h_trailleppt[i]->SetMarkerColor(color);
    
    // MET
    h_met[i] = new TH1F(TString("HWW_"+sampleName+"_hmet"), TString("HWW_"+sampleName+"_hmet"), 20, 0, 100);
    h_met[i]->SetLineColor(color);
    h_met[i]->SetMarkerColor(color);
    
    
    // dilepton pT
    h_dilpt[i] = new TH1F(TString("HWW_"+sampleName+"_hdilpt"), TString("HWW_"+sampleName+"_hdilpt"), 30, 20, 100);
    h_dilpt[i]->SetLineColor(color);
    h_dilpt[i]->SetMarkerColor(color);
    
    // deltaphi (ll)
    h_dphill[i] = new TH1F(TString("HWW_"+sampleName+"_hdphi"), TString("HWW_"+sampleName+"_hdphi"), 18, 0, 180.0);
    h_dphill[i]->SetLineColor(color);
    h_dphill[i]->SetMarkerColor(color);
    
    // transverse mass
    h_mt[i] = new TH1F(TString("HWW_"+sampleName+"_hmt"), TString("HWW_"+sampleName+"_hmt"), 20, 0, 200);
    h_mt[i]->SetLineColor(color);
    h_mt[i]->SetMarkerColor(color);
    

    std::cout  << "Processing " << chain->GetEntries() << " entries. \n";
    int nEntries =  chain->GetEntries() ;
    int nSelected = 0;
    
    // mcfm variables to be used
    double mll_ = 0.0;
    double leadleppt_ = 0.0;
    double trailleppt_ = 0.0;
    double leadlepeta_ = 0.0;
    double traillepeta_ = 0.0;
    double dphill_ = 0.0;
    double met_ = 0.0;
    double mt_ = 0.0;
    double dilpt_ = 0.0;
    double wt_ = 1.0;

    if (chain->GetBranchStatus("mll"))
      chain->SetBranchAddress("mll", &mll_);

    if (chain->GetBranchStatus("leadleppt"))
      chain->SetBranchAddress("leadleppt", &leadleppt_);

    if (chain->GetBranchStatus("trailleppt"))
      chain->SetBranchAddress("trailleppt", &trailleppt_);

    if (chain->GetBranchStatus("dphill"))
      chain->SetBranchAddress("dphill", &dphill_);

    if (chain->GetBranchStatus("met"))
      chain->SetBranchAddress("met", &met_);
    
    if (chain->GetBranchStatus("mt"))
      chain->SetBranchAddress("mt", &mt_);

    if (chain->GetBranchStatus("dilpt"))
      chain->SetBranchAddress("dilpt", &dilpt_);
    
      if (chain->GetBranchStatus("leadlepeta"))
      chain->SetBranchAddress("leadlepeta", &leadlepeta_);

    if (chain->GetBranchStatus("traillepeta"))
      chain->SetBranchAddress("traillepeta", &traillepeta_);

    if (chain->GetBranchStatus("wt"))
      chain->SetBranchAddress("wt", &wt_);
   
    for ( int ievt = 0; ievt < chain->GetEntries(); ievt++) {
      chain->GetEntry(ievt);
      
      //
      // apply WW selections
      // 
      
      if ( ievt == 0 ) 
	std::cout << leadleppt_ << "\t" << trailleppt_ << "\t" << dilpt_ << "\t" << met_ << "\t" << mll_ << "\n";

      float weight = wt_;

      if ( leadleppt_ < 20. ) continue;
      if ( trailleppt_ < 10. ) continue;
      if ( TMath::Abs(leadlepeta_) > 2.5) continue;
      if ( TMath::Abs(traillepeta_) > 2.5) continue;
      
      /*
      if ( dilpt_ < 45.) continue;
      if ( mll_ < 12.) continue;
      if ( met_ < 20.) continue;

      */
      
      h_mll[i]->Fill(mll_, weight);
      h_dilpt[i]->Fill(dilpt_, weight);
      h_dphill[i]->Fill(dphill_ * 180. / TMath::Pi(), weight);
      h_leadleppt[i]->Fill(leadleppt_, weight);
      h_trailleppt[i]->Fill(trailleppt_, weight);
      h_mt[i]->Fill(mt_, weight);
      h_met[i]->Fill(met_, weight);

      // 
      // apply HWW selections for 125 
      // 
      
      if ( higgselection(mH, mt_, mll_, dphill_, leadleppt_, trailleppt_) ) 
	nSelected++;
    } // end of event loop in each sample
    
    std::cout << Form("sample %s: selection effiency is %i / %i = %.2f\n", samples[i].Data(), nSelected, nEntries, float(nSelected)/float(nEntries));
  }
  
  drawsingle("mll", nHist, h_mll, samples, legend, "Dilepton Invariant Mass [GeV]");
  drawsingle("dphill", nHist, h_dphill, samples, legend, "#Delta#phi(leptons) [degrees]");
  drawsingle("mt", nHist, h_mt, samples, legend, "Transverse Higgs Mass [GeV]");
  drawsingle("met", nHist, h_met, samples, legend, "Transverse Missing Energy [GeV]");
  drawsingle("dilpt", nHist, h_dilpt, samples, legend, "Dilepton pT [GeV]");
  
  output_file->cd();
  
  for(int i=0;i<nHist;i++) {
    h_mll[i]->Write();
    h_dphill[i]->Write();
    h_leadleppt[i]->Write();
    h_trailleppt[i]->Write();
    h_met[i]->Write();
    h_mt[i]->Write();
    h_dilpt[i]->Write();
    
  }
  
  // tidy up
  
  for ( int i = 0; i<nHist;i++) {
    delete h_mll[i];
    delete h_dphill[i];
    delete h_leadleppt[i];
    delete h_trailleppt[i];
    delete h_met[i];
    delete h_mt[i];
    delete h_dilpt[i];
  }

}


void drawsingle(TString var, const int nHist, TH1F** hist, std::vector<TString> samples, std::vector<TString> legend, TString x_title)
{
  
  
  // make plots
  TCanvas *c1 = new TCanvas("c1","c1");
  c1->cd();  
  
  TLegend *leg = new TLegend(0.55, 0.78, 0.68, 0.92);
  leg->SetFillColor(0);
  leg->SetTextSize(0.035);
  leg->SetBorderSize(0);
  leg->SetFillStyle(0);
  leg->SetShadowColor(0);

  float yMax = 0;
  
  for(int i=0;i<nHist;i++) {
    hist[i]->Scale(1./hist[i]->Integral(0,1000));
    yMax = yMax > hist[i]->GetMaximum() ? yMax : hist[i]->GetMaximum();
    hist[i]->SetXTitle(x_title);
    hist[i]->SetLineWidth(2);
    Color_t color = kBlack;
    if ( samples[i].Contains("SMHiggs", TString::kExact) )       color = kBlue;
    if ( samples[i].Contains("PSHiggs", TString::kExact) )       color = kMagenta;
    if ( samples[i].Contains("THiggs", TString::kExact) )       color = kRed;
    if ( samples[i].Contains("T", TString::kExact) )       color = kRed;

    hist[i]->SetLineColor(color);
    leg->AddEntry(hist[i], legend[i], "l");
  }
  
  for ( int i=0; i<nHist;i++) {
    hist[i]->SetMaximum(yMax*1.2);
    hist[i]->SetMinimum(0.);
    if ( i == 0) 
      hist[i]->Draw("HIST");
    else 
      hist[i]->Draw("sameHIST");
  }
  leg->Draw("SAME"); 
  c1->Print(Form("epsfiles/nocut/%s_mH%i.eps", var.Data(), mH ));
  c1->Print(Form("pngfiles/nocut/%s_mH%i.png", var.Data(), mH ));
  //c1->Print(Form("epsfiles/wwselection/%s_mH%i.eps", var.Data(), mH ));
  //c1->Print(Form("pngfiles/wwselection/%s_mH%i.png", var.Data(), mH ));
  
	    
  // tidy up
  delete leg;  
  delete c1;
  
}


bool higgselection(int mH, double mt, double mll, double dphill, double leadleppt, double trailleppt)
{
  
  double lep1ptCut(20.), lep2ptCut(10.), mllCut(9999.), dPhiCut(180.), mtHighCut(mH), mtLowCut(80.);
  
  
  if ( mH == 125.) {
    lep1ptCut = 25.;
    lep2ptCut = 10.;
    mllCut = 45;
    dPhiCut = 90;
    mtHighCut = 125;
  }


  if ( mH == 170.) {
    lep1ptCut = 34.;
    lep2ptCut = 25.;
    mllCut = 50;
    dPhiCut = 60;
    mtLowCut = 110.;
  }

  if ( mt < mtLowCut ) return false;
  if ( mt > mtHighCut ) return false;
  if ( mll > mllCut ) return false;
  if ( dphill > (dPhiCut * TMath::Pi() / 180) ) return false;
  if ( leadleppt < lep1ptCut) return false;
  if ( trailleppt < lep2ptCut) return false;

  return true;
  
}
