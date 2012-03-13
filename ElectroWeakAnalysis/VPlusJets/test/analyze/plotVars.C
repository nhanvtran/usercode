#include <iostream>
#include <TH1D.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TLorentzVector.h>
#include <algorithm>	
#include <vector>
#include "TProfile.h"

#include "TCanvas.h"
#include "TString.h"
#include "TAxis.h"
#include "TFile.h"
#include "TLegend.h"
#include "TChain.h"
#include "TH1D.h"
#include "TH2F.h"
#include "TH3F.h"
#include "TF1.h"
#include "TString.h"
#include <sstream>
#include <string>
#include <vector>
#include "THStack.h"

using namespace std;
void setTDRStyle();

double j_ak5_bdis, j_ak5_eta, j_ak5_phi, j_ak5_pt, j_ak5_mass, j_ak5_area, j_ak5_nJ, j_ak5_mu, j_ak5_p;
double j_ak5tr_mass;
double j_ak5pr_mass;
double j_ak5ft_mass;
double j_ak7_mass;
double j_ak7tr_mass;
double j_ak7pr_mass;
double j_ak7ft_mass;
double j_ca8_mass;    
double j_ca8pr_mass;

double e_nvert, l_pt, l_reliso, e_met, e_weight, w_mt, w_pt;
double e_puwt, e_puwt_up, e_puwt_dn, e_effwt;

double g_j_pt = 50.;
double g_j_mass_lo = 0.;
double g_j_mass_hi = 1000.;
double g_e_met = 25.;
double g_w_mt = 50.;
double g_nJ = 6.;
double g_l_pt = 35.;
double g_j_mu = 1.0;

void InitTree( TTree* tree );
TH1D* ExtractHisto( TTree* tree, std::string varname, char* cut, int nbins=100, double hlo=0., double hhi=1. );

void plotVars(std::string dir="figs", double ilumi = 1.){
    
	//gROOT->ProcessLine(".L ~/tdrstyle.C");
	//setTDRStyle();
    setTDRStyle();
	gStyle->SetPadLeftMargin(0.16);
	
    char oname[192];
    
    double LUMI = ilumi;
    
    // list the jet typs that you are interested in
    const int nJetTypes = 10;
    std::string jetNames [nJetTypes] = {"ak5","ak5tr","ak5pr","ak5ft","ak7tr","ak7pr","ak7ft","ca8","ca8pr"};
 
    // ------------------------------------------
    // cuts
    // non-jet cuts
    g_e_met = 25.;
    g_w_mt = 50.;
    g_l_pt = 35.;
    bool b_effWeighting = true;
    bool b_puWeighting = false;
    string s_effWeighting = ""; if (b_effWeighting) s_effWeighting = "e_effwt*";
    string s_puWeighting = ""; if (b_puWeighting) s_puWeighting = "e_puwt*";
    char nonjetCuts[192];
    
    //sprintf(nonjetCuts,"e_effwt*((e_met > %f)&&(l_pt > %f)&&(w_mt > %f))",g_e_met,g_l_pt,g_w_mt);
    std::string dummyjettype = "ak5";
    sprintf(nonjetCuts,"%s%s((e_met > %f)&&(l_pt > %f)&&(w_mt > %f)&&(j_%s_pt > %f)&&(j_%s_mass < %f)&& (j_%s_mass>%f)&&(j_%s_nJ<=%f))",
            s_effWeighting.c_str(), s_puWeighting.c_str(),
            g_e_met,g_l_pt,g_w_mt,
            dummyjettype.c_str(), g_j_pt,
            dummyjettype.c_str(), g_j_mass_hi,
            dummyjettype.c_str(), g_j_mass_lo,
            dummyjettype.c_str(), g_nJ);
    
    // jet cuts
    g_j_mu = 1.0;
    g_j_pt = 50.; 
    g_j_mass_lo = 0.;
    g_j_mass_hi = 1000.;
    g_nJ = 6.;
            
    // tree names
    TFile f_ttbar("ntuples/test.root");
    TTree* t_ttbar = (TTree*) f_ttbar.Get("otree");
    //InitTree(t_ttbar);
   
    // extract histos!
    TH1D* test = ExtractHisto( t_ttbar, "j_ak5_pt", nonjetCuts, 100, 0., 200.);

    TCanvas* c = new TCanvas("c","c",700,700);
    c->cd();
    std::cout << "mean: " << test->GetMean() << std::endl;
    test->Draw();
    c->SaveAs("test.eps");
}

//////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////

TH1D* ExtractHisto( TTree* tree, std::string varname, char* cut, int nbins, double hlo, double hhi ){
    
    TH1D* h = new TH1D("h","h",nbins,hlo,hhi); 
    
    tree->Project("h",varname.c_str(), cut );
    
    //for (int i = 0; i < tree->GetEntries(); i++){
    //    tree->GetEntry(i);
    //}
    
    return h;
    
}

void InitTree( TTree* tree ){
    
    tree->SetBranchAddress("e_puwt", &e_puwt);
    tree->SetBranchAddress("e_puwt_up", &e_puwt_up);
    tree->SetBranchAddress("e_puwt_dn", &e_puwt_dn);
    tree->SetBranchAddress("e_effwt", &e_effwt);
    
    tree->SetBranchAddress("e_met", &e_met);
    tree->SetBranchAddress("e_nvert", &e_nvert);
    tree->SetBranchAddress("e_weight", &e_weight);
    tree->SetBranchAddress("w_mt", &w_mt);
    tree->SetBranchAddress("w_pt", &w_pt);
    tree->SetBranchAddress("l_pt", &l_pt);
    tree->SetBranchAddress("l_reliso", &l_reliso);
    tree->SetBranchAddress("j_ak5_nJ", &j_ak5_nJ);
    tree->SetBranchAddress("j_ak5_mu", &j_ak5_mu);
    tree->SetBranchAddress("j_ak5_bdis", &j_ak5_bdis);
    tree->SetBranchAddress("j_ak5_eta", &j_ak5_eta);
    tree->SetBranchAddress("j_ak5_phi", &j_ak5_phi);
    tree->SetBranchAddress("j_ak5_pt", &j_ak5_pt);
    tree->SetBranchAddress("j_ak5_p", &j_ak5_p);
    tree->SetBranchAddress("j_ak5_mass", &j_ak5_mass);
    tree->SetBranchAddress("j_ak5_area", &j_ak5_area);
    
    tree->SetBranchAddress("j_ak5tr_mass", &j_ak5tr_mass);
    tree->SetBranchAddress("j_ak5pr_mass", &j_ak5pr_mass);
    tree->SetBranchAddress("j_ak5ft_mass", &j_ak5ft_mass);
    
    tree->SetBranchAddress("j_ak7_mass", &j_ak7_mass);
    tree->SetBranchAddress("j_ak7tr_mass", &j_ak7tr_mass);
    tree->SetBranchAddress("j_ak7pr_mass", &j_ak7pr_mass);
    tree->SetBranchAddress("j_ak7ft_mass", &j_ak7ft_mass);
    
    tree->SetBranchAddress("j_ca8_mass", &j_ca8_mass);
    tree->SetBranchAddress("j_ca8pr_mass", &j_ca8pr_mass);
    
}





//////////////
//////////////
//////////////
//////////////

void setTDRStyle() {
    TStyle *tdrStyle = new TStyle("tdrStyle","Style for P-TDR");
    
    // For the canvas:
    tdrStyle->SetCanvasBorderMode(0);
    tdrStyle->SetCanvasColor(kWhite);
    tdrStyle->SetCanvasDefH(750); //Height of canvas
    tdrStyle->SetCanvasDefW(1050); //Width of canvas
    tdrStyle->SetCanvasDefX(0);   //POsition on screen
    tdrStyle->SetCanvasDefY(0);
    
    // For the Pad:
    tdrStyle->SetPadBorderMode(0);
    // tdrStyle->SetPadBorderSize(Width_t size = 1);
    tdrStyle->SetPadColor(kWhite);
    tdrStyle->SetPadGridX(false);
    tdrStyle->SetPadGridY(false);
    tdrStyle->SetGridColor(0);
    tdrStyle->SetGridStyle(3);
    tdrStyle->SetGridWidth(1);
    
    // For the frame:
    tdrStyle->SetFrameBorderMode(0);
    tdrStyle->SetFrameBorderSize(1);
    tdrStyle->SetFrameFillColor(0);
    tdrStyle->SetFrameFillStyle(0);
    tdrStyle->SetFrameLineColor(1);
    tdrStyle->SetFrameLineStyle(1);
    tdrStyle->SetFrameLineWidth(1);
    
    // For the histo:
    // tdrStyle->SetHistFillColor(1);
    // tdrStyle->SetHistFillStyle(0);
    tdrStyle->SetHistLineColor(1);
    tdrStyle->SetHistLineStyle(0);
    tdrStyle->SetHistLineWidth(1);
    // tdrStyle->SetLegoInnerR(Float_t rad = 0.5);
    // tdrStyle->SetNumberContours(Int_t number = 20);
    
    tdrStyle->SetEndErrorSize(2);
    //  tdrStyle->SetErrorMarker(20);
    tdrStyle->SetErrorX(0.);
    
    tdrStyle->SetMarkerStyle(20);
    
    //For the fit/function:
    tdrStyle->SetOptFit(1);
    tdrStyle->SetFitFormat("5.4g");
    tdrStyle->SetFuncColor(2);
    tdrStyle->SetFuncStyle(1);
    tdrStyle->SetFuncWidth(1);
    
    //For the date:
    tdrStyle->SetOptDate(0);
    // tdrStyle->SetDateX(Float_t x = 0.01);
    // tdrStyle->SetDateY(Float_t y = 0.01);
    
    // For the statistics box:
    tdrStyle->SetOptFile(0);
    tdrStyle->SetOptStat(0); // To display the mean and RMS:   SetOptStat("mr");
    tdrStyle->SetStatColor(kWhite);
    tdrStyle->SetStatFont(42);
    tdrStyle->SetStatFontSize(0.010);
    tdrStyle->SetStatTextColor(1);
    tdrStyle->SetStatFormat("6.4g");
    tdrStyle->SetStatBorderSize(1);
    tdrStyle->SetStatH(0.25);
    tdrStyle->SetStatW(0.15);
    // tdrStyle->SetStatStyle(Style_t style = 1001);
    // tdrStyle->SetStatX(Float_t x = 0);
    // tdrStyle->SetStatY(Float_t y = 0);
    
    // Margins:
    tdrStyle->SetPadTopMargin(0.05);
    tdrStyle->SetPadBottomMargin(0.13);
    tdrStyle->SetPadLeftMargin(0.14);
    tdrStyle->SetPadRightMargin(0.04);
    
    // For the Global title:
    
    tdrStyle->SetOptTitle(0);
    tdrStyle->SetTitleFont(42);
    tdrStyle->SetTitleColor(1);
    tdrStyle->SetTitleTextColor(1);
    tdrStyle->SetTitleFillColor(10);
    tdrStyle->SetTitleFontSize(0.005);
    // tdrStyle->SetTitleH(0); // Set the height of the title box
    // tdrStyle->SetTitleW(0); // Set the width of the title box
    // tdrStyle->SetTitleX(0); // Set the position of the title box
    // tdrStyle->SetTitleY(0.985); // Set the position of the title box
    // tdrStyle->SetTitleStyle(Style_t style = 1001);
    // For the axis titles:
    
    tdrStyle->SetTitleColor(1, "XYZ");
    tdrStyle->SetTitleFont(42, "XYZ");
    tdrStyle->SetTitleSize(0.06, "XYZ");
    // tdrStyle->SetTitleXSize(Float_t size = 0.02); // Another way to set the size?
    // tdrStyle->SetTitleYSize(Float_t size = 0.02);
    tdrStyle->SetTitleXOffset(0.9);
    tdrStyle->SetTitleYOffset(1.25);
    // tdrStyle->SetTitleOffset(1.1, "Y"); // Another way to set the Offset
    
    // For the axis labels:
    
    tdrStyle->SetLabelColor(1, "XYZ");
    tdrStyle->SetLabelFont(42, "XYZ");
    tdrStyle->SetLabelOffset(0.007, "XYZ");
    tdrStyle->SetLabelSize(0.05, "XYZ");
    
    // For the axis:
    
    tdrStyle->SetAxisColor(1, "XYZ");
    tdrStyle->SetStripDecimals(kTRUE);
    tdrStyle->SetTickLength(0.03, "XYZ");
    tdrStyle->SetNdivisions(505, "XYZ");
    tdrStyle->SetPadTickX(1);  // To get tick marks on the opposite side of the frame
    tdrStyle->SetPadTickY(1);
    
    // Change for log plots:
    tdrStyle->SetOptLogx(0);
    tdrStyle->SetOptLogy(0);
    tdrStyle->SetOptLogz(0);
    
    // Postscript options:
    tdrStyle->SetPaperSize(20.,20.);
    // tdrStyle->SetLineScalePS(Float_t scale = 3);
    // tdrStyle->SetLineStyleString(Int_t i, const char* text);
    // tdrStyle->SetHeaderPS(const char* header);
    // tdrStyle->SetTitlePS(const char* pstitle);
    
    // tdrStyle->SetBarOffset(Float_t baroff = 0.5);
    // tdrStyle->SetBarWidth(Float_t barwidth = 0.5);
    // tdrStyle->SetPaintTextFormat(const char* format = "g");
    // tdrStyle->SetPalette(Int_t ncolors = 0, Int_t* colors = 0);
    // tdrStyle->SetTimeOffset(Double_t toffset);
    // tdrStyle->SetHistMinimumZero(kTRUE);
    
    tdrStyle->cd();
}