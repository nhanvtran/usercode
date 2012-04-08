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
double j_ak8_mass;
double j_ak8tr_mass;
double j_ak8pr_mass;
double j_ak8ft_mass;
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
TH1D* ExtractHisto( char* name, TTree* tree, std::string varname, char* cut, int nbins=100, double hlo=0., double hhi=1. );
TH1D* ExtractProfileVPt( char* name, TTree* tree, std::string varname, char* cut, int nbins=100, double hlo=0., double hhi=100. );
TH1D* ExtractProfileVNvert( char* name, TTree* tree, std::string varname, char* cut, int nbins, double hlo, double hhi );
void convertProfileToTH1D( TProfile* p, TH1D* h );

void plotVars(std::string dir="figs", double ilumi = 1.){
    
	//gROOT->ProcessLine(".L ~/tdrstyle.C");
	//setTDRStyle();
    setTDRStyle();
	gStyle->SetPadLeftMargin(0.16);
	
    char oname[192];
    
    double LUMI = ilumi;
    
    // list the jet typs that you are interested in
    const int nJetTypes = 14;
    std::string jetNames [nJetTypes] = {"ak5","ak5tr","ak5pr","ak5ft","ak7","ak7tr","ak7pr","ak7ft","ak8","ak8tr","ak8pr","ak8ft","ca8","ca8pr"};
    
    // ------------------------------------------
    // [ 1 ]   c u t s 
    // ------------------------------------------
    // non-jet cuts
    g_e_met = 25.;
    g_w_mt = 50.;
    g_l_pt = 35.;
    bool b_effWeighting = true;
    bool b_puWeighting = false;
    string s_effWeighting = ""; if (b_effWeighting) s_effWeighting = "e_effwt*";
    string s_puWeighting = ""; if (b_puWeighting) s_puWeighting = "e_puwt*";
    char nonjetCuts[192];
    // jet cuts
    g_j_mu = 1.0;
    g_j_pt = 50.; 
    g_j_mass_lo = 0.;
    g_j_mass_hi = 1000.;
    g_nJ = 6.;
    
    
    // ------------------------------------------
    // [ 2 ]   t r e e   n a m e s
    // ------------------------------------------
    TFile f_wjets("ntuples/test_wj.root");
    TTree* t_wjets = (TTree*) f_wjets.Get("otree");
    t_wjets->SetName("otree_wj");
    TFile f_ww("ntuples/test_ww.root");
    TTree* t_ww = (TTree*) f_ww.Get("otree");
    t_ww->SetName("otree_ww");
    
    // ----------------------------------
    // start defining histograms
    // ----------------------------------
    TH1D* hwj_mass[nJetTypes];
    TH1D* hwj_area[nJetTypes];
    TH1D* hwj_pt[nJetTypes];
    TH1D* hwj_mVpt[nJetTypes];
    TH1D* hwj_mVv[nJetTypes];
    TH1D* hww_mass[nJetTypes];
    TH1D* hww_area[nJetTypes];
    TH1D* hww_pt[nJetTypes];
    TH1D* hww_mVpt[nJetTypes];
    TH1D* hww_mVv[nJetTypes];

    TH1D* hwj_mVpt_ovAK5[nJetTypes];
    TH1D* hwj_mVpt_ovAK7[nJetTypes];
    TH1D* hwj_mVpt_ovAK8[nJetTypes];
    TH1D* hww_mVpt_ovAK5[nJetTypes];
    TH1D* hww_mVpt_ovAK7[nJetTypes];
    TH1D* hww_mVpt_ovAK8[nJetTypes];
    TH1D* hwj_ptVpt_ovAK5[nJetTypes];
    TH1D* hwj_ptVpt_ovAK7[nJetTypes];
    TH1D* hwj_ptVpt_ovAK8[nJetTypes];
    TH1D* hww_ptVpt_ovAK5[nJetTypes];
    TH1D* hww_ptVpt_ovAK7[nJetTypes];
    TH1D* hww_ptVpt_ovAK8[nJetTypes];
    // ----------------------------------
    // [ 3 ]   s t a r t   m a k i n g   h i s t o g r a m s
    // ----------------------------------
    char hn[192];
    for (int i = 0; i < nJetTypes; i++){
        
        std::cout << "jet type: " << jetNames[i] << std::endl;
        
        sprintf(nonjetCuts,"%s%s((e_met > %f)&&(l_pt > %f)&&(w_mt > %f)&&(j_%s_pt > %f)&&(j_%s_mass < %f)&& (j_%s_mass>%f)&&(j_%s_nJ<=%f))",
                s_effWeighting.c_str(), s_puWeighting.c_str(),
                g_e_met,g_l_pt,g_w_mt,
                jetNames[i].c_str(), g_j_pt,
                jetNames[i].c_str(), g_j_mass_hi,
                jetNames[i].c_str(), g_j_mass_lo,
                jetNames[i].c_str(), g_nJ);
        
        // ttbar histos
        std::string varname = "j_" + jetNames[i] + "_mass"; sprintf( hn, "j_mass_%i_%s", i);
        hwj_mass[i] = ExtractHisto( hn, t_wjets, varname.c_str(), nonjetCuts, 100, 0., 150.);
        hww_mass[i] = ExtractHisto( hn, t_ww, varname.c_str(), nonjetCuts, 100, 0., 150.);
        
        varname = "j_" + jetNames[i] + "_pt"; sprintf( hn, "j_pt_%i", i);
        hwj_pt[i] = ExtractHisto( hn, t_wjets, varname.c_str(), nonjetCuts, 100, 0., 500.);
        hww_pt[i] = ExtractHisto( hn, t_ww, varname.c_str(), nonjetCuts, 100, 0., 500.);
        
        varname = "j_" + jetNames[i] + "_area"; sprintf( hn, "j_area_%i", i);
        hwj_area[i] = ExtractHisto( hn, t_wjets, varname.c_str(), nonjetCuts, 100, 0., 5.);
        hww_area[i] = ExtractHisto( hn, t_ww, varname.c_str(), nonjetCuts, 100, 0., 5.);
        
        varname = "j_" + jetNames[i] + "_mass:j_" + jetNames[i] + "_pt"; sprintf( hn, "j_vpt_%i", i);
        hwj_mVpt[i] = ExtractProfileVPt( hn, t_wjets, varname.c_str(), nonjetCuts, 100, 0., 500.);
        hww_mVpt[i] = ExtractProfileVPt( hn, t_ww, varname.c_str(), nonjetCuts, 100, 0., 500.);
                
        varname = "j_" + jetNames[i] + "_mass:e_nvert"; sprintf( hn, "j_vnv_%i", i);
        hwj_mVv[i] = ExtractProfileVNvert( hn, t_wjets, varname.c_str(), nonjetCuts, 100, 0., 500.);
        hww_mVv[i] = ExtractProfileVNvert( hn, t_ww, varname.c_str(), nonjetCuts, 100, 0., 500.);

        // over ak5
        std::cout << "===========================" << std::endl;
        varname = "(j_" + jetNames[i] + "_mass/j_ak5_mass):j_ak5_pt"; sprintf( hn, "j_mvptak5_%i", i);
        hwj_mVpt_ovAK5[i] = ExtractProfileVPt( hn, t_wjets, varname.c_str(), nonjetCuts, 100, 0., 500.);
        hww_mVpt_ovAK5[i] = ExtractProfileVPt( hn, t_ww, varname.c_str(), nonjetCuts, 100, 0., 500.);
        varname = "(j_" + jetNames[i] + "_pt/j_ak5_pt):j_ak5_pt"; sprintf( hn, "j_ptvptak5_%i", i);
        hwj_ptVpt_ovAK5[i] = ExtractProfileVPt( hn, t_wjets, varname.c_str(), nonjetCuts, 100, 0., 500.);
        hww_ptVpt_ovAK5[i] = ExtractProfileVPt( hn, t_ww, varname.c_str(), nonjetCuts, 100, 0., 500.);
        // over ak7
        varname = "(j_" + jetNames[i] + "_mass/j_ak7_mass):j_ak7_pt"; sprintf( hn, "j_mvptak7_%i", i);
        hwj_mVpt_ovAK7[i] = ExtractProfileVPt( hn, t_wjets, varname.c_str(), nonjetCuts, 100, 0., 500.);
        hww_mVpt_ovAK7[i] = ExtractProfileVPt( hn, t_ww, varname.c_str(), nonjetCuts, 100, 0., 500.);
        varname = "(j_" + jetNames[i] + "_pt/j_ak7_pt):j_ak7_pt"; sprintf( hn, "j_ptvptak7_%i", i);
        hwj_ptVpt_ovAK7[i] = ExtractProfileVPt( hn, t_wjets, varname.c_str(), nonjetCuts, 100, 0., 500.);
        hww_ptVpt_ovAK7[i] = ExtractProfileVPt( hn, t_ww, varname.c_str(), nonjetCuts, 100, 0., 500.);
        // over ak8
        varname = "(j_" + jetNames[i] + "_mass/j_ak8_mass):j_ak8_pt"; sprintf( hn, "j_mvptak8_%i", i);
        hwj_mVpt_ovAK8[i] = ExtractProfileVPt( hn, t_wjets, varname.c_str(), nonjetCuts, 100, 0., 500.);
        hww_mVpt_ovAK8[i] = ExtractProfileVPt( hn, t_ww, varname.c_str(), nonjetCuts, 100, 0., 500.);
        varname = "(j_" + jetNames[i] + "_pt/j_ak8_pt):j_ak8_pt"; sprintf( hn, "j_ptvptak8_%i", i);
        hwj_ptVpt_ovAK8[i] = ExtractProfileVPt( hn, t_wjets, varname.c_str(), nonjetCuts, 100, 0., 500.);
        hww_ptVpt_ovAK8[i] = ExtractProfileVPt( hn, t_ww, varname.c_str(), nonjetCuts, 100, 0., 500.);

        
        // properties
        int curColor = i+1;
        if (curColor == 5) curColor = 42;
        if (curColor == 7) curColor = 46;
        int markerStyle = 20;
        if (i >= 4) markerStyle = 24;
        hwj_mass[i]->SetLineColor(curColor);
        hwj_pt[i]->SetLineColor(curColor);
        hwj_area[i]->SetLineColor(curColor);
        hwj_mVpt[i]->SetLineColor(curColor); hwj_mVpt[i]->SetMarkerColor(curColor); hwj_mVpt[i]->SetMarkerStyle(markerStyle);
        hwj_mVpt[i]->SetLineColor(curColor); hwj_mVv[i]->SetMarkerColor(curColor); hwj_mVv[i]->SetMarkerStyle(markerStyle);            
        
        hww_mass[i]->SetLineColor(curColor);
        hww_pt[i]->SetLineColor(curColor);
        hww_area[i]->SetLineColor(curColor);
        hww_mVpt[i]->SetLineColor(curColor); hww_mVpt[i]->SetMarkerColor(curColor); hww_mVpt[i]->SetMarkerStyle(markerStyle);
        hww_mVpt[i]->SetLineColor(curColor); hww_mVv[i]->SetMarkerColor(curColor); hww_mVv[i]->SetMarkerStyle(markerStyle);    

    }

    
    // ----------------------------------
    // [ 4 ]   s t a r t   m a k i n g   p l o t s
    // ----------------------------------
    
    /////////////////
    // legends
    TLegend * box1 = new TLegend(0.5,0.50,0.93,0.92);
    box1->SetFillColor(0);
    box1->SetBorderSize(0);
    box1->AddEntry(hwj_mass[0],"AK5","l");
    box1->AddEntry(hwj_mass[1],"AK5Trimmed","l");
    box1->AddEntry(hwj_mass[2],"AK5Pruned","l");
    box1->AddEntry(hwj_mass[3],"AK5Filtered","l");
    box1->AddEntry(hwj_mass[4],"AK7","l");
    box1->AddEntry(hwj_mass[5],"AK7Trimmed","l");
    box1->AddEntry(hwj_mass[6],"AK7Pruned","l");
    box1->AddEntry(hwj_mass[7],"AK7Filtered","l");
    
    TLegend * box2 = new TLegend(0.5,0.50,0.93,0.92);
    box2->SetFillColor(0);
    box2->SetBorderSize(0);
    box2->AddEntry(hwj_mass[8],"AK8","l");
    box2->AddEntry(hwj_mass[9],"AK8Trimmed","l");
    box2->AddEntry(hwj_mass[10],"AK8Pruned","l");
    box2->AddEntry(hwj_mass[11],"AK8Filtered","l");
    box2->AddEntry(hwj_mass[12],"CA8","l");
    box2->AddEntry(hwj_mass[13],"CA8Pruned","l");
    
    TLegend * box3 = new TLegend(0.5,0.70,0.93,0.92);
    box3->SetFillColor(0);
    box3->SetBorderSize(0);
    box3->AddEntry(hwj_mVpt[0],"AK5","pe");
    box3->AddEntry(hwj_mVpt[1],"AK5Trimmed","pe");
    box3->AddEntry(hwj_mVpt[2],"AK5Pruned","pe");
    box3->AddEntry(hwj_mVpt[3],"AK5Filtered","pe");
    box3->AddEntry(hwj_mVpt[4],"AK7Trimmed","pe");
    box3->AddEntry(hwj_mVpt[5],"AK7Pruned","pe");
    box3->AddEntry(hwj_mVpt[6],"AK7Filtered","pe");
    //box3->AddEntry(hwj_mass[7],"CA8","l");
    //box3->AddEntry(hwj_mass[8],"CA8Pruned","l");

    TCanvas* c = new TCanvas("c","c",1400,1400);
    c->Divide(2,2);
    c->cd(1);
    //hwj_mass[0]->GetXaxis()->SetRangeUser(0.,75);
    hwj_mass[0]->Draw();
    hwj_mass[1]->Draw("sames");
    hwj_mass[2]->Draw("sames");
    hwj_mass[3]->Draw("sames");
    hwj_mass[4]->Draw("sames");
    hwj_mass[5]->Draw("sames");
    hwj_mass[6]->Draw("sames");
    hwj_mass[7]->Draw("sames");
    box1->Draw();
    c->cd(2);
    hwj_mass[8]->Draw();
    hwj_mass[9]->Draw("sames");
    hwj_mass[10]->Draw("sames");
    hwj_mass[11]->Draw("sames");
    hwj_mass[12]->Draw("sames");
    hwj_mass[13]->Draw("sames");
    box2->Draw();
    c->cd(3);
    hwj_mass[0]->Draw();
    hwj_mass[1]->Draw("sames");
    hwj_mass[2]->Draw("sames");
    hwj_mass[3]->Draw("sames");
    hwj_mass[4]->Draw("sames");
    hwj_mass[5]->Draw("sames");
    hwj_mass[6]->Draw("sames");
    hwj_mass[7]->Draw("sames");
    gPad->SetLogy();
    c->cd(4);
    hwj_mass[8]->Draw();
    hwj_mass[9]->Draw("sames");
    hwj_mass[10]->Draw("sames");
    hwj_mass[11]->Draw("sames");
    hwj_mass[12]->Draw("sames");
    hwj_mass[13]->Draw("sames");
    gPad->SetLogy();
    c->Update();
    c->SaveAs("figs/test_mass.eps");
    
    TCanvas* c_area = new TCanvas("c_area","c_area",1400,700);
    c_area->Divide(2,1);
    c_area->cd(1);
    hwj_area[0]->Draw();
    hwj_area[1]->Draw("sames");
    hwj_area[2]->Draw("sames");
    hwj_area[3]->Draw("sames");
    hwj_area[4]->Draw("sames");
    hwj_area[5]->Draw("sames");
    hwj_area[6]->Draw("sames");
    hwj_area[7]->Draw("sames");
    box1->Draw();
    c_area->cd(2);
    hwj_area[8]->Draw();
    hwj_area[9]->Draw("sames");
    hwj_area[10]->Draw("sames");
    hwj_area[11]->Draw("sames");
    hwj_area[12]->Draw("sames");
    hwj_area[13]->Draw("sames");
    box2->Draw();
    c_area->Update();
    c_area->SaveAs("figs/test_area.eps");
    
    TCanvas* c_pt = new TCanvas("c_pt","c_pt",1000,600);
    c_pt->Divide(2,1);
    c_pt->cd(1);
    hwj_mVpt_ovAK5[0]->GetYaxis()->SetRangeUser(0.,1.1); hwj_mVpt_ovAK5[0]->SetMarkerColor(kBlack);
    hwj_mVpt_ovAK5[0]->Draw();
    hwj_mVpt_ovAK5[1]->SetMarkerColor(kRed);
    hwj_mVpt_ovAK5[1]->Draw("sames");
    hwj_mVpt_ovAK5[2]->SetMarkerColor(kBlue);
    hwj_mVpt_ovAK5[2]->Draw("sames");
    hwj_mVpt_ovAK5[3]->SetMarkerColor(kMagenta);
    hwj_mVpt_ovAK5[3]->Draw("sames");
    c_pt->cd(2);
    hwj_ptVpt_ovAK5[0]->GetYaxis()->SetRangeUser(0.,1.1); hwj_ptVpt_ovAK5[0]->SetMarkerColor(kBlack);
    hwj_ptVpt_ovAK5[0]->Draw();
    hwj_ptVpt_ovAK5[1]->SetMarkerColor(kRed);
    hwj_ptVpt_ovAK5[1]->Draw("sames");
    hwj_ptVpt_ovAK5[2]->SetMarkerColor(kBlue);
    hwj_ptVpt_ovAK5[2]->Draw("sames");
    hwj_ptVpt_ovAK5[3]->SetMarkerColor(kMagenta);
    hwj_ptVpt_ovAK5[3]->Draw("sames");
    c_pt->Update();
    c_pt->SaveAs("figs/test_pt.eps");

    TCanvas* c2 = new TCanvas("c2","c2",1400,700);
    c2->Divide(2,1);
    c2->cd(1);
    hwj_mVpt[0]->GetYaxis()->SetRangeUser(0.,100.); hwj_mVpt[0]->Draw();
    hwj_mVpt[1]->Draw("sames");
    hwj_mVpt[2]->Draw("sames");
    hwj_mVpt[3]->Draw("sames");
    hwj_mVpt[4]->Draw("sames");
    hwj_mVpt[5]->Draw("sames");
    hwj_mVpt[6]->Draw("sames");
    c2->cd(2);
    hwj_mVv[0]->GetYaxis()->SetRangeUser(0.,100.); hwj_mVv[0]->Draw();    
    hwj_mVv[1]->Draw("sames");
    hwj_mVv[2]->Draw("sames");
    hwj_mVv[3]->Draw("sames");
    hwj_mVv[4]->Draw("sames");
    hwj_mVv[5]->Draw("sames");
    hwj_mVv[6]->Draw("sames");
    box3->Draw();
    c2->Update();
    c2->SaveAs("figs/test_profile.eps");
}

//////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////

TH1D* ExtractHisto( char* name, TTree* tree, std::string varname, char* cut, int nbins, double hlo, double hhi ){
    //std::cout << "varname: " << varname << std::endl;
    
    char hname[192];
    sprintf(hname,"h_%s_%s",name,tree->GetName());
    TH1D* h = new TH1D(hname,varname.c_str(),nbins,hlo,hhi); 
    tree->Project(hname,varname.c_str(), cut );
    
    return h;
    
}

TH1D* ExtractProfileVPt( char* name, TTree* tree, std::string varname, char* cut, int nbins, double hlo, double hhi ){
    
    char pname[192];
    sprintf(pname,"p_%s_%s",name,tree->GetName());
    char hname[192];
    sprintf(hname,"h_%s_%s",name,tree->GetName());
    
    double xbinsProfile[29] = {50,55,60,65,70,75,80,85,90,95,100,110,120,130,140,150,160,170,180,190,200,225,250,275,300,350,400,450,500};
    //TProfile* p_vPt = new TProfile(pname,"p_vPt",28,xbinsProfile, hlo, hhi);     
    TProfile* p_vPt = new TProfile(pname,"p_vPt",28,xbinsProfile, hlo, hhi);     
    TH1D* h_vPt = new TH1D(hname,"; jet pT; <m_{j}>",28,xbinsProfile);
    
    //std::cout << "varname: " << varname << std::endl;
    
    tree->Project(pname,varname.c_str(), cut );
    //p_vPt->Draw();
    
    
    convertProfileToTH1D( p_vPt, h_vPt );
    
    return h_vPt;
    
}

TH1D* ExtractProfileVNvert( char* name, TTree* tree, std::string varname, char* cut, int nbins, double hlo, double hhi ){
    
    char pname[192];
    sprintf(pname,"p_%s_%s",name,tree->GetName());
    char hname[192];
    sprintf(hname,"h_%s_%s",name,tree->GetName());
    
    TProfile* p_vV = new TProfile(pname,"p_vV",30,0.,30.,hlo, hhi); 
    TH1D* h_vV = new TH1D(hname,"; # of vertices; <m_{j}>",30,0.,30.);
    
    tree->Project(pname,varname.c_str(), cut );
    convertProfileToTH1D( p_vV, h_vV );
    
    return h_vV;
    
}

void convertProfileToTH1D( TProfile* p, TH1D* h ){
    
    for (int i = 1; i <= p->GetNbinsX(); i++){
        
        h->SetBinContent( i, p->GetBinContent( i ) );
        h->SetBinError( i, p->GetBinError( i ) );
        
        //cout << " p->GetBinContent( i ): " << p->GetBinContent( i ) << std::endl;
    }
    
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

    tree->SetBranchAddress("j_ak8_mass", &j_ak8_mass);
    tree->SetBranchAddress("j_ak8tr_mass", &j_ak8tr_mass);
    tree->SetBranchAddress("j_ak8pr_mass", &j_ak8pr_mass);
    tree->SetBranchAddress("j_ak8ft_mass", &j_ak8ft_mass);

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