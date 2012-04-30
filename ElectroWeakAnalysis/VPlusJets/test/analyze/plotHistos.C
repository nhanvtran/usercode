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

void SetHistProperties( TH1F* h, int lineColor, int lineStyle, int lineWidth, int markerColor, int markerStyle, int markerSize, int fillColor, int fillStyle){
    
    if (lineColor >= 0) h->SetLineColor( lineColor );
    if (lineStyle >= 0) h->SetLineStyle( lineStyle );
    if (lineWidth >= 0) h->SetLineWidth( lineWidth );
    
    if (markerColor >= 0) h->SetMarkerColor( markerColor );
    if (markerStyle >= 0) h->SetMarkerStyle( markerStyle );
    if (markerSize >= 0) h->SetMarkerSize( markerSize );
    
    if (fillColor >= 0) h->SetFillColor( fillColor );
    if (fillStyle >= 0) h->SetFillStyle( fillStyle );
    
}

void SetProfileProperties( TProfile* h, int lineColor, int lineStyle, int lineWidth, int markerColor, int markerStyle, int markerSize, int fillColor, int fillStyle){
    
    if (lineColor > 0) h->SetLineColor( lineColor );
    if (lineStyle > 0) h->SetLineStyle( lineStyle );
    if (lineWidth > 0) h->SetLineWidth( lineWidth );
    
    if (markerColor >= 0) h->SetMarkerColor( markerColor );
    if (markerStyle >= 0) h->SetMarkerStyle( markerStyle );
    if (markerSize >= 0) h->SetMarkerSize( markerSize );
    
    if (fillColor > 0) h->SetFillColor( fillColor );
    if (fillStyle > 0) h->SetFillStyle( fillStyle );
    
}

double GetHistogramEntriesWeighted( TH1F* h ){
    double tot = 0;
    for (int i = 1; i <= h->GetNbinsX(); i++){
        tot+=h->GetBinContent( i );
    }
    return tot;
}

double GetDataMCSclFactor( TH1F* dat, TH1F* MC ){
    
    double mctotweight = GetHistogramEntriesWeighted( MC );
    double datatotweight = GetHistogramEntriesWeighted( dat );
    double scl = datatotweight/mctotweight;
    MC->Scale( scl );
    return scl;
}

void plotHistos(std::string dir="figs", double ilumi = 1.){
    
    setTDRStyle();
    gStyle->SetPadLeftMargin(0.16);
        
    // files
    TFile f_wj( (dir+"/histos_wj.root").c_str() );
    TFile f_ww( (dir+"/histos_ww.root").c_str() );    
    TFile f_tt( (dir+"/histos_tt.root").c_str() );    
    // combination of wj, ww, tt
    TFile f_all( (dir+"/histos_all.root").c_str() );  
    
    // data
    TFile f_dat( (dir+"/histos_dat.root").c_str());  
    
    // jet collections
    const int nJetTypes_C = 18;
    std::string jetNames[nJetTypes_C] = {"ak5","ak5tr","ak5pr","ak5ft","ak7","ak7tr","ak7pr","ak7ft","ak8","ak8tr","ak8pr","ak8ft","ca8","ca8pr","ak5g","ak7g","ak8g","ca8g"};
    int nJetTypes = nJetTypes_C;
    
    TH1F* wj_h_j_mass[nJetTypes_C];
    TH1F* ww_h_j_mass[nJetTypes_C];
    TH1F* tt_h_j_mass[nJetTypes_C];
    THStack* hs_mass[nJetTypes_C];
    TH1F* all_h_j_mass[nJetTypes_C];
    TH1F* dat_h_j_mass[nJetTypes_C];
    
    TH1F* all_h_j_mass_pt50to100[nJetTypes_C];
    TH1F* all_h_j_mass_pt100to150[nJetTypes_C];
    TH1F* all_h_j_mass_pt150to200[nJetTypes_C];
    TH1F* all_h_j_mass_pt200to300[nJetTypes_C];
    TH1F* all_h_j_mass_pt300andup[nJetTypes_C];
    TH1F* dat_h_j_mass_pt50to100[nJetTypes_C];
    TH1F* dat_h_j_mass_pt100to150[nJetTypes_C];
    TH1F* dat_h_j_mass_pt150to200[nJetTypes_C];
    TH1F* dat_h_j_mass_pt200to300[nJetTypes_C];
    TH1F* dat_h_j_mass_pt300andup[nJetTypes_C];
    
    TProfile* all_p_j_massvpt[nJetTypes_C];
    TProfile* all_p_j_massvNV[nJetTypes_C];
    TProfile* all_p_j_massOverAK5[nJetTypes_C];
    TProfile* all_p_j_massOverAK7[nJetTypes_C];
    TProfile* all_p_j_massOverAK8[nJetTypes_C];
    TProfile* all_p_j_ptOverAK5[nJetTypes_C];
    TProfile* all_p_j_ptOverAK7[nJetTypes_C];
    TProfile* all_p_j_ptOverAK8[nJetTypes_C];
    
    TProfile* all_p_j_massOverAK5vNV[nJetTypes_C];
    TProfile* all_p_j_massOverAK7vNV[nJetTypes_C];
    TProfile* all_p_j_massOverAK8vNV[nJetTypes_C];
    TProfile* all_p_j_ptOverAK5vNV[nJetTypes_C];
    TProfile* all_p_j_ptOverAK7vNV[nJetTypes_C];
    TProfile* all_p_j_ptOverAK8vNV[nJetTypes_C];
    
    TProfile* dat_p_j_massvpt[nJetTypes_C];
    TProfile* dat_p_j_massvNV[nJetTypes_C];
    TProfile* dat_p_j_massOverAK5[nJetTypes_C];
    TProfile* dat_p_j_massOverAK7[nJetTypes_C];
    TProfile* dat_p_j_massOverAK8[nJetTypes_C];
    TProfile* dat_p_j_ptOverAK5[nJetTypes_C];
    TProfile* dat_p_j_ptOverAK7[nJetTypes_C];
    TProfile* dat_p_j_ptOverAK8[nJetTypes_C];
    
    TProfile* dat_p_j_massOverAK5vNV[nJetTypes_C];
    TProfile* dat_p_j_massOverAK7vNV[nJetTypes_C];
    TProfile* dat_p_j_massOverAK8vNV[nJetTypes_C];
    TProfile* dat_p_j_ptOverAK5vNV[nJetTypes_C];
    TProfile* dat_p_j_ptOverAK7vNV[nJetTypes_C];
    TProfile* dat_p_j_ptOverAK8vNV[nJetTypes_C];

    TH1F* all_h_j_area[nJetTypes_C];
    TH1F* dat_h_j_area[nJetTypes_C];
    
    char hname[192];
    char cname[192];
    
    // kinematics

    sprintf( hname, "h_w_mt" );
    TH1F* wj_h_w_mt = (TH1F*) f_wj.Get(hname); SetHistProperties( wj_h_w_mt, 2, 1, 1, 0, 0, 0, 2, 1001 );
    TH1F* ww_h_w_mt = (TH1F*) f_ww.Get(hname); SetHistProperties( ww_h_w_mt, 4, 1, 1, 0, 0, 0, 4, 1001 );   
    TH1F* tt_h_w_mt = (TH1F*) f_tt.Get(hname); SetHistProperties( tt_h_w_mt, 6, 1, 1, 0, 0, 0, 6, 1001 );   
    TH1F* all_h_w_mt = (TH1F*) f_all.Get(hname); SetHistProperties( all_h_w_mt, 6, 1, 1, 0, 0, 0, 6, 1001 );   
    THStack* hs_w_mt = new THStack( "hs_w_mt", "hs_w_mt" ); 
    hs_w_mt->Add( wj_h_w_mt );
    hs_w_mt->Add( ww_h_w_mt );
    hs_w_mt->Add( tt_h_w_mt );
    // =================================================
    // for comparisons with data, need to scale MC...
    double sclfactor_dataVmc = 1.;
    TH1F* dat_h_w_mt = (TH1F*) f_dat.Get(hname); SetHistProperties( dat_h_w_mt, 1, 1, 1, 1, 10, 1, 6, 1001 );
    sclfactor_dataVmc = GetDataMCSclFactor( dat_h_w_mt, all_h_w_mt);
    wj_h_w_mt->Scale(sclfactor_dataVmc);
    ww_h_w_mt->Scale(sclfactor_dataVmc);
    tt_h_w_mt->Scale(sclfactor_dataVmc);
    // =================================================
    
    sprintf( hname, "h_w_pt" );
    TH1F* wj_h_w_pt = (TH1F*) f_wj.Get(hname); SetHistProperties( wj_h_w_pt, 2, 1, 1, 0, 0, 0, 2, 1001 );
    TH1F* ww_h_w_pt = (TH1F*) f_ww.Get(hname); SetHistProperties( ww_h_w_pt, 4, 1, 1, 0, 0, 0, 4, 1001 );   
    TH1F* tt_h_w_pt = (TH1F*) f_tt.Get(hname); SetHistProperties( tt_h_w_pt, 6, 1, 1, 0, 0, 0, 6, 1001 );   
    TH1F* all_h_w_pt = (TH1F*) f_all.Get(hname); SetHistProperties( all_h_w_pt, 6, 1, 1, 0, 0, 0, 6, 1001 );   
    // =================================================
    // for comparisons with data, need to scale MC...
    sclfactor_dataVmc = 1.;
    TH1F* dat_h_w_pt = (TH1F*) f_dat.Get(hname); SetHistProperties( dat_h_w_pt, 1, 1, 1, 1, 10, 1, 6, 1001 );
    sclfactor_dataVmc = GetDataMCSclFactor( dat_h_w_pt, all_h_w_pt);
    wj_h_w_pt->Scale(sclfactor_dataVmc);
    ww_h_w_pt->Scale(sclfactor_dataVmc);
    tt_h_w_pt->Scale(sclfactor_dataVmc);
    // =================================================
    THStack* hs_w_pt = new THStack( "hs_w_pt", "hs_w_pt" ); 
    hs_w_pt->Add( wj_h_w_pt );
    hs_w_pt->Add( ww_h_w_pt );
    hs_w_pt->Add( tt_h_w_pt );
    
    sprintf( hname, "h_e_met" );
    TH1F* wj_h_e_met = (TH1F*) f_wj.Get(hname); SetHistProperties( wj_h_e_met, 2, 1, 1, 0, 0, 0, 2, 1001 );
    TH1F* ww_h_e_met = (TH1F*) f_ww.Get(hname); SetHistProperties( ww_h_e_met, 4, 1, 1, 0, 0, 0, 4, 1001 );   
    TH1F* tt_h_e_met = (TH1F*) f_tt.Get(hname); SetHistProperties( tt_h_e_met, 6, 1, 1, 0, 0, 0, 6, 1001 );   
    TH1F* all_h_e_met = (TH1F*) f_all.Get(hname); SetHistProperties( all_h_e_met, 6, 1, 1, 0, 0, 0, 6, 1001 );   
    // =================================================
    // for comparisons with data, need to scale MC...
    sclfactor_dataVmc = 1.;
    TH1F* dat_h_e_met = (TH1F*) f_dat.Get(hname); SetHistProperties( dat_h_e_met, 1, 1, 1, 1, 10, 1, 6, 1001 );
    sclfactor_dataVmc = GetDataMCSclFactor( dat_h_e_met, all_h_e_met);
    wj_h_e_met->Scale(sclfactor_dataVmc);
    ww_h_e_met->Scale(sclfactor_dataVmc);
    tt_h_e_met->Scale(sclfactor_dataVmc);
    // =================================================
    THStack* hs_e_met = new THStack( "hs_e_met", "hs_e_met" ); 
    hs_e_met->Add( wj_h_e_met );
    hs_e_met->Add( ww_h_e_met );
    hs_e_met->Add( tt_h_e_met );
    
    sprintf( hname, "h_l_pt" );
    TH1F* wj_h_l_pt = (TH1F*) f_wj.Get(hname); SetHistProperties( wj_h_l_pt, 2, 1, 1, 0, 0, 0, 2, 1001 );
    TH1F* ww_h_l_pt = (TH1F*) f_ww.Get(hname); SetHistProperties( ww_h_l_pt, 4, 1, 1, 0, 0, 0, 4, 1001 );   
    TH1F* tt_h_l_pt = (TH1F*) f_tt.Get(hname); SetHistProperties( tt_h_l_pt, 6, 1, 1, 0, 0, 0, 6, 1001 );   
    TH1F* all_h_l_pt = (TH1F*) f_all.Get(hname); SetHistProperties( all_h_l_pt, 6, 1, 1, 0, 0, 0, 6, 1001 );   
    // =================================================
    // for comparisons with data, need to scale MC...
    sclfactor_dataVmc = 1.;
    TH1F* dat_h_l_pt = (TH1F*) f_dat.Get(hname); SetHistProperties( dat_h_l_pt, 1, 1, 1, 1, 10, 1, 6, 1001 );
    sclfactor_dataVmc = GetDataMCSclFactor( dat_h_l_pt, all_h_l_pt);
    wj_h_l_pt->Scale(sclfactor_dataVmc);
    ww_h_l_pt->Scale(sclfactor_dataVmc);
    tt_h_l_pt->Scale(sclfactor_dataVmc);
    // =================================================
    THStack* hs_l_pt = new THStack( "hs_l_pt", "hs_l_pt" ); 
    hs_l_pt->Add( wj_h_l_pt );
    hs_l_pt->Add( ww_h_l_pt );
    hs_l_pt->Add( tt_h_l_pt );
    
    TCanvas *c0 = new TCanvas("c0","c0",1200,1200);
    c0->Divide(2,2);
    c0->cd(1);
    hs_w_mt->Draw();
    dat_h_w_mt->Draw("pe1x0sames");
    c0->cd(2);
    hs_w_pt->Draw();
    dat_h_w_pt->Draw("pe1x0sames");
    c0->cd(3);
    hs_e_met->Draw();
    dat_h_e_met->Draw("pe1x0sames");
    c0->cd(4);
    hs_l_pt->Draw();
    dat_h_l_pt->Draw("pe1x0sames");
    sprintf( cname, "%s/figs/basic_kin.png", dir.c_str() );
    c0->SaveAs(cname);
    

    /////////////////////
    sprintf( hname, "h_j_ca8pr_mu" );
    TH1F* wj_h_j_ca8pr_mu = (TH1F*) f_wj.Get(hname); SetHistProperties( wj_h_j_ca8pr_mu, 2, 1, 1, 0, 0, 0, 2, 1001 );
    TH1F* ww_h_j_ca8pr_mu = (TH1F*) f_ww.Get(hname); SetHistProperties( ww_h_j_ca8pr_mu, 7, 1, 1, 0, 0, 0, 7, 1001 );   
    TH1F* tt_h_j_ca8pr_mu = (TH1F*) f_tt.Get(hname); SetHistProperties( tt_h_j_ca8pr_mu, 4, 1, 1, 0, 0, 0, 4, 1001 );   
    TH1F* all_h_j_ca8pr_mu = (TH1F*) f_all.Get(hname); SetHistProperties( all_h_j_ca8pr_mu, 6, 1, 1, 0, 0, 0, 6, 1001 );   
    // =================================================
    // for comparisons with data, need to scale MC...
    sclfactor_dataVmc = 1.;
    TH1F* dat_h_j_ca8pr_mu = (TH1F*) f_dat.Get(hname); SetHistProperties( dat_h_j_ca8pr_mu, 1, 1, 1, 1, 10, 1, 6, 1001 );
    sclfactor_dataVmc = GetDataMCSclFactor( dat_h_j_ca8pr_mu, all_h_j_ca8pr_mu);
    wj_h_j_ca8pr_mu->Scale(sclfactor_dataVmc);
    ww_h_j_ca8pr_mu->Scale(sclfactor_dataVmc);
    tt_h_j_ca8pr_mu->Scale(sclfactor_dataVmc);
    // =================================================
    THStack* hs_j_ca8pr_mu = new THStack( "hs_j_ca8pr_mu", "hs_j_ca8pr_mu" ); 
    hs_j_ca8pr_mu->Add( wj_h_j_ca8pr_mu );
    hs_j_ca8pr_mu->Add( ww_h_j_ca8pr_mu );
    hs_j_ca8pr_mu->Add( tt_h_j_ca8pr_mu );
    
    //TH1F* all_h_j_cap8pr_mu = (TH1F*) f_all.Get("h_j_cap8pr_mu"); SetHistProperties( all_h_j_cap8pr_mu, 6, 1, 1, 0, 0, 0, 6, 1001  );
    //TH1F* dat_h_j_cap8pr_mu = (TH1F*) f_dat.Get("h_j_cap8pr_mu"); SetHistProperties( dat_h_j_cap8pr_mu, 1, 1, 1, 1, 10, 1, 6, 1001 );
    TCanvas *cmu = new TCanvas("cmu","cmu",600,600);
    hs_j_ca8pr_mu->Draw();
    dat_h_j_ca8pr_mu->Draw("pe1x0sames");
    sprintf( cname, "%s/figs/cmu.png", dir.c_str() );
    cmu->SaveAs(cname);
    /////////////////////
    
    // -----------------------------------------------
    // canvasii
    TCanvas *c1 = new TCanvas("c1","c1",1000,1000);
    c1->Divide(2,2);
    TCanvas *c2 = new TCanvas("c2","c2",1200,600);
    c2->Divide(2,1);
    ///*
    // jet-related plots for each individual jet species
    for (int i = 0; i < nJetTypes; i++){
        
        // -----------------------------------------------
        // jet mass plots
        // -----------------------------------------------
        std::cout << "mass..." << std::endl;
        sprintf( hname, "h_j_%s_mass", jetNames[i].c_str() );
        wj_h_j_mass[i] = (TH1F*) f_wj.Get(hname); SetHistProperties( wj_h_j_mass[i], 2, 1, 1, 0, 0, 0, 2, 1001 );
        ww_h_j_mass[i] = (TH1F*) f_ww.Get(hname); SetHistProperties( ww_h_j_mass[i], 7, 1, 1, 0, 0, 0, 7, 1001 );   
        tt_h_j_mass[i] = (TH1F*) f_tt.Get(hname); SetHistProperties( tt_h_j_mass[i], 4, 1, 1, 0, 0, 0, 4, 1001 );   
        
        all_h_j_mass[i] = (TH1F*) f_all.Get(hname); SetHistProperties( all_h_j_mass[i], 4, 1, 1, 0, 0, 0, 4, 3001 );   
        // =================================================
        // for comparisons with data, need to scale MC...
        sclfactor_dataVmc = 1.;
        if ( i < 14 ){ 
            dat_h_j_mass[i] = (TH1F*) f_dat.Get(hname); SetHistProperties( dat_h_j_mass[i], 1, 1, 1, 1, 24, 1, 6, 1001 ); 
            sclfactor_dataVmc = GetDataMCSclFactor( dat_h_j_mass[i], all_h_j_mass[i]); 
        }
        std::cout << "sclfactor_dataVmc: " << sclfactor_dataVmc << std::endl;
        wj_h_j_mass[i]->Scale(sclfactor_dataVmc);
        ww_h_j_mass[i]->Scale(sclfactor_dataVmc);
        tt_h_j_mass[i]->Scale(sclfactor_dataVmc);
        // =================================================
        hs_mass[i] = new THStack( "hs_mass", "hs_mass" ); 
        hs_mass[i]->Add( wj_h_j_mass[i] );
        hs_mass[i]->Add( ww_h_j_mass[i] );
        hs_mass[i]->Add( tt_h_j_mass[i] );
        c1->cd(1);
        hs_mass[i]->Draw();
        if ( i < 14 ) dat_h_j_mass[i]->Draw("pe1x0sames");
        c1->cd(2);
        gPad->SetLogy();
        hs_mass[i]->SetMinimum( 0.1 );
        //hs_mass[i]->SetMaximum( 1.e8 );
        hs_mass[i]->Draw();
        if ( i < 14 ) dat_h_j_mass[i]->Draw("pe1x0sames");
        c1->cd(3);
        all_h_j_mass[i]->Draw("e2");
        TH1F* tmp0b = (TH1F*) all_h_j_mass[i]->Clone();
        SetHistProperties( tmp0b, 4, 0, 0, 0, 0, 0, 0, 0 );
        tmp0b->Draw("sames");
        if ( i < 14 ) dat_h_j_mass[i]->Draw("pe1x0sames");
        c1->cd(4);
        gPad->SetLogy();
        all_h_j_mass[i]->SetMinimum( 0.1 );
        all_h_j_mass[i]->Draw("e2");
        tmp0b->Draw("sames");
        if ( i < 14 ) dat_h_j_mass[i]->Draw("pe1x0sames");
        sprintf( cname, "%s/figs/j_mass_%s.png", dir.c_str(), jetNames[i].c_str() );
        c1->SaveAs(cname);
        // -----------------------------------------------
        // jet mass plots in bins of pT
        // -----------------------------------------------
        std::cout << "in bins of pT plots..." << std::endl;
        sprintf( hname, "h_j_%s_mass_pt50to100", jetNames[i].c_str() );
        all_h_j_mass_pt50to100[i] = (TH1F*) f_all.Get(hname); SetHistProperties( all_h_j_mass_pt50to100[i], 1, 0, 0, 0, 0, 0, 1, 3001 );
        sprintf( hname, "h_j_%s_mass_pt100to150", jetNames[i].c_str() );
        all_h_j_mass_pt100to150[i] = (TH1F*) f_all.Get(hname); SetHistProperties( all_h_j_mass_pt100to150[i], 2, 0, 0, 0, 0, 0, 2, 3001 );
        sprintf( hname, "h_j_%s_mass_pt150to200", jetNames[i].c_str() );
        all_h_j_mass_pt150to200[i] = (TH1F*) f_all.Get(hname); SetHistProperties( all_h_j_mass_pt150to200[i], 3, 0, 0, 0, 0, 0, 3, 3001 );
        sprintf( hname, "h_j_%s_mass_pt200to300", jetNames[i].c_str() );
        all_h_j_mass_pt200to300[i] = (TH1F*) f_all.Get(hname); SetHistProperties( all_h_j_mass_pt200to300[i], 4, 0, 0, 0, 0, 0, 4, 3001 );
        sprintf( hname, "h_j_%s_mass_pt300andup", jetNames[i].c_str() );
        all_h_j_mass_pt300andup[i] = (TH1F*) f_all.Get(hname); SetHistProperties( all_h_j_mass_pt300andup[i], 6, 0, 0, 0, 0, 0, 6, 3001 );
        // =================================================
        // for comparisons with data, need to scale MC...
        sclfactor_dataVmc = 1.;
        if ( i < 14 ){
            sprintf( hname, "h_j_%s_mass_pt50to100", jetNames[i].c_str() );
            dat_h_j_mass_pt50to100[i] = (TH1F*) f_dat.Get(hname); SetHistProperties( dat_h_j_mass_pt50to100[i], 1, 1, 1, 1, 24, 1, 1, 1001 ); 
            sclfactor_dataVmc = GetDataMCSclFactor( dat_h_j_mass_pt50to100[i], all_h_j_mass_pt50to100[i]);
            sprintf( hname, "h_j_%s_mass_pt100to150", jetNames[i].c_str() );
            dat_h_j_mass_pt100to150[i] = (TH1F*) f_dat.Get(hname); SetHistProperties( dat_h_j_mass_pt100to150[i], 1, 1, 1, 2, 24, 1, 2, 1001 ); 
            sclfactor_dataVmc = GetDataMCSclFactor( dat_h_j_mass_pt100to150[i], all_h_j_mass_pt100to150[i]);
            sprintf( hname, "h_j_%s_mass_pt150to200", jetNames[i].c_str() );
            dat_h_j_mass_pt150to200[i] = (TH1F*) f_dat.Get(hname); SetHistProperties( dat_h_j_mass_pt150to200[i], 1, 1, 1, 3, 24, 1, 3, 1001 ); 
            sclfactor_dataVmc = GetDataMCSclFactor( dat_h_j_mass_pt150to200[i], all_h_j_mass_pt150to200[i]);
            sprintf( hname, "h_j_%s_mass_pt200to300", jetNames[i].c_str() );
            dat_h_j_mass_pt200to300[i] = (TH1F*) f_dat.Get(hname); SetHistProperties( dat_h_j_mass_pt200to300[i], 1, 1, 1, 4, 24, 1, 4, 1001 ); 
            sclfactor_dataVmc = GetDataMCSclFactor( dat_h_j_mass_pt200to300[i], all_h_j_mass_pt200to300[i]);
            sprintf( hname, "h_j_%s_mass_pt300andup", jetNames[i].c_str() );
            dat_h_j_mass_pt300andup[i] = (TH1F*) f_dat.Get(hname); SetHistProperties( dat_h_j_mass_pt300andup[i], 1, 1, 1, 6, 24, 1, 6, 1001 ); 
            sclfactor_dataVmc = GetDataMCSclFactor( dat_h_j_mass_pt300andup[i], all_h_j_mass_pt300andup[i]);
        }

        // =================================================
        c2->cd(1);
        all_h_j_mass_pt50to100[i]->Draw("e2");
        TH1F* tmp1a = (TH1F*) all_h_j_mass_pt50to100[i]->Clone(); SetHistProperties( tmp1a, 1, 0, 0, 0, 0, 0, 0, 0 );
        tmp1a->Draw("sames");
        if ( i < 14 ) dat_h_j_mass_pt50to100[i]->Draw("pe1x0sames");
        all_h_j_mass_pt100to150[i]->Draw("e2sames");
        TH1F* tmp2a = (TH1F*) all_h_j_mass_pt100to150[i]->Clone(); SetHistProperties( tmp2a, 2, 0, 0, 0, 0, 0, 0, 0 );
        tmp2a->Draw("sames");
        if ( i < 14 ) dat_h_j_mass_pt100to150[i]->Draw("pe1x0sames");
        all_h_j_mass_pt150to200[i]->Draw("e2sames");
        TH1F* tmp3a = (TH1F*) all_h_j_mass_pt150to200[i]->Clone(); SetHistProperties( tmp3a, 3, 0, 0, 0, 0, 0, 0, 0 );
        tmp3a->Draw("sames");
        if ( i < 14 ) dat_h_j_mass_pt150to200[i]->Draw("pe1x0sames");
        all_h_j_mass_pt200to300[i]->Draw("e2sames");
        TH1F* tmp4a = (TH1F*) all_h_j_mass_pt200to300[i]->Clone(); SetHistProperties( tmp4a, 4, 0, 0, 0, 0, 0, 0, 0 );
        tmp4a->Draw("sames");
        if ( i < 14 ) dat_h_j_mass_pt200to300[i]->Draw("pe1x0sames");
        all_h_j_mass_pt300andup[i]->Draw("e2sames");
        TH1F* tmp5a = (TH1F*) all_h_j_mass_pt300andup[i]->Clone(); SetHistProperties( tmp5a, 6, 0, 0, 0, 0, 0, 0, 0 );
        tmp5a->Draw("sames");
        if ( i < 14 ) dat_h_j_mass_pt300andup[i]->Draw("pe1x0sames");
        c2->cd(2);
        gPad->SetLogy();
        all_h_j_mass_pt50to100[i]->Draw("e2");
        tmp1a->Draw("sames");
        if ( i < 14 ) dat_h_j_mass_pt50to100[i]->Draw("pe1x0sames");
        all_h_j_mass_pt100to150[i]->Draw("e2sames");
        tmp2a->Draw("sames");
        if ( i < 14 ) dat_h_j_mass_pt100to150[i]->Draw("pe1x0sames");
        all_h_j_mass_pt150to200[i]->Draw("e2sames");
        tmp3a->Draw("sames");
        if ( i < 14 ) dat_h_j_mass_pt150to200[i]->Draw("pe1x0sames");
        all_h_j_mass_pt200to300[i]->Draw("e2sames");
        tmp4a->Draw("sames");
        if ( i < 14 ) dat_h_j_mass_pt200to300[i]->Draw("pe1x0sames");
        all_h_j_mass_pt300andup[i]->Draw("e2sames");
        tmp5a->Draw("sames");
        if ( i < 14 ) dat_h_j_mass_pt300andup[i]->Draw("pe1x0sames");
        sprintf( cname, "%s/figs/j_massInBins_%s.png", dir.c_str(), jetNames[i].c_str() );
        c2->SaveAs(cname);
        
        // -----------------------------------------------
        // ratio plots
        // -----------------------------------------------
        std::cout << "ratio plots..." << std::endl;
        sprintf( hname, "p_j_%s_massvpt", jetNames[i].c_str() );
        all_p_j_massvpt[i] = (TProfile*) f_all.Get(hname); 
        if ( i < 14 ) dat_p_j_massvpt[i] = (TProfile*) f_dat.Get(hname); 
        sprintf( hname, "p_j_%s_massvNV", jetNames[i].c_str() );
        if ( i < 14 ) all_p_j_massvNV[i] = (TProfile*) f_all.Get(hname); 
        dat_p_j_massvNV[i] = (TProfile*) f_dat.Get(hname); 
        
        sprintf( hname, "p_j_%s_massOverAK5", jetNames[i].c_str() );
        all_p_j_massOverAK5[i] = (TProfile*) f_all.Get(hname); 
        if ( i < 14 ) dat_p_j_massOverAK5[i] = (TProfile*) f_dat.Get(hname); 
        sprintf( hname, "p_j_%s_massOverAK7", jetNames[i].c_str() );
        all_p_j_massOverAK7[i] = (TProfile*) f_all.Get(hname); 
        if ( i < 14 ) dat_p_j_massOverAK7[i] = (TProfile*) f_dat.Get(hname); 
        sprintf( hname, "p_j_%s_massOverAK8", jetNames[i].c_str() );
        all_p_j_massOverAK8[i] = (TProfile*) f_all.Get(hname); 
        if ( i < 14 ) dat_p_j_massOverAK8[i] = (TProfile*) f_dat.Get(hname); 
        
        sprintf( hname, "p_j_%s_ptOverAK5", jetNames[i].c_str() );
        all_p_j_ptOverAK5[i] = (TProfile*) f_all.Get(hname); 
        if ( i < 14 ) dat_p_j_ptOverAK5[i] = (TProfile*) f_dat.Get(hname); 
        sprintf( hname, "p_j_%s_ptOverAK7", jetNames[i].c_str() );
        all_p_j_ptOverAK7[i] = (TProfile*) f_all.Get(hname); 
        if ( i < 14 ) dat_p_j_ptOverAK7[i] = (TProfile*) f_dat.Get(hname); 
        sprintf( hname, "p_j_%s_ptOverAK8", jetNames[i].c_str() );
        all_p_j_ptOverAK8[i] = (TProfile*) f_all.Get(hname); 
        if ( i < 14 ) dat_p_j_ptOverAK8[i] = (TProfile*) f_dat.Get(hname); 
        
        sprintf( hname, "p_j_%s_massOverAK5vNV", jetNames[i].c_str() );
        all_p_j_massOverAK5vNV[i] = (TProfile*) f_all.Get(hname); 
        if ( i < 14 ) dat_p_j_massOverAK5vNV[i] = (TProfile*) f_dat.Get(hname); 
        sprintf( hname, "p_j_%s_massOverAK7vNV", jetNames[i].c_str() );
        all_p_j_massOverAK7vNV[i] = (TProfile*) f_all.Get(hname); 
        if ( i < 14 ) dat_p_j_massOverAK7vNV[i] = (TProfile*) f_dat.Get(hname); 
        sprintf( hname, "p_j_%s_massOverAK8vNV", jetNames[i].c_str() );
        all_p_j_massOverAK8vNV[i] = (TProfile*) f_all.Get(hname); 
        if ( i < 14 ) dat_p_j_massOverAK8vNV[i] = (TProfile*) f_dat.Get(hname); 
        
        sprintf( hname, "p_j_%s_ptOverAK5vNV", jetNames[i].c_str() );
        all_p_j_ptOverAK5vNV[i] = (TProfile*) f_all.Get(hname); 
        if ( i < 14 ) dat_p_j_ptOverAK5vNV[i] = (TProfile*) f_dat.Get(hname); 
        sprintf( hname, "p_j_%s_ptOverAK7vNV", jetNames[i].c_str() );
        all_p_j_ptOverAK7vNV[i] = (TProfile*) f_all.Get(hname); 
        if ( i < 14 ) dat_p_j_ptOverAK7vNV[i] = (TProfile*) f_dat.Get(hname); 
        sprintf( hname, "p_j_%s_ptOverAK8vNV", jetNames[i].c_str() );
        all_p_j_ptOverAK8vNV[i] = (TProfile*) f_all.Get(hname); 
        if ( i < 14 ) dat_p_j_ptOverAK8vNV[i] = (TProfile*) f_dat.Get(hname); 
        
        // -----------------------------------------------
        // jet area
        // -----------------------------------------------
        sprintf( hname, "h_j_%s_area", jetNames[i].c_str() );
        all_h_j_area[i] = (TH1F*) f_all.Get(hname); SetHistProperties( all_h_j_area[i], 4, 1, 1, 0, 0, 0, 4, 3001 );   
        sclfactor_dataVmc = 1.;
        if ( i < 14 ){ 
            dat_h_j_area[i] = (TH1F*) f_dat.Get(hname); SetHistProperties( dat_h_j_area[i], 1, 1, 1, 1, 24, 1, 6, 1001 ); 
            sclfactor_dataVmc = GetDataMCSclFactor( dat_h_j_area[i], all_h_j_area[i]); 
        }
    }
    
    // plotting profile of jet mass as a function of pT and nV
    TCanvas *cp1 = new TCanvas( "cp1", "cp1", 1200, 600 );
    cp1->Divide(2,1);
    cp1->cd(1);
    SetProfileProperties( all_p_j_massvpt[0], 1, 1, 1, 1, 0, 0, 1, 3001 );
    all_p_j_massvpt[0]->Draw("e2");     
    SetProfileProperties( all_p_j_massvpt[1], 2, 1, 1, 2, 0, 0, 2, 3001 );
    all_p_j_massvpt[1]->Draw("e2sames");     
    SetProfileProperties( all_p_j_massvpt[2], 4, 1, 1, 4, 0, 0, 4, 3001 );
    all_p_j_massvpt[2]->Draw("e2sames");     
    SetProfileProperties( all_p_j_massvpt[3], 6, 1, 1, 6, 0, 0, 6, 3001 );
    all_p_j_massvpt[3]->Draw("e2sames");     
    SetProfileProperties( dat_p_j_massvpt[0], 1, 1, 1, 1, 24, 1, 1, 3001 );
    dat_p_j_massvpt[0]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massvpt[1], 2, 1, 1, 2, 24, 1, 2, 3001 );
    dat_p_j_massvpt[1]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massvpt[2], 4, 1, 1, 4, 24, 1, 4, 3001 );
    dat_p_j_massvpt[2]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massvpt[3], 6, 1, 1, 6, 24, 1, 6, 3001 );
    dat_p_j_massvpt[3]->Draw("pe1x0sames");     
    
    cp1->cd(2);
    SetProfileProperties( all_p_j_massvNV[0], 1, 1, 1, 1, 0, 0, 1, 3001 );
    all_p_j_massvNV[0]->Draw("e2"); 
    SetProfileProperties( all_p_j_massvNV[1], 2, 1, 1, 2, 0, 0, 2, 3001 );
    all_p_j_massvNV[1]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_massvNV[2], 4, 1, 1, 4, 0, 0, 4, 3001 );
    all_p_j_massvNV[2]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_massvNV[3], 6, 1, 1, 6, 0, 0, 6, 3001 );
    all_p_j_massvNV[3]->Draw("e2sames"); 
    SetProfileProperties( dat_p_j_massvNV[0], 1, 1, 1, 1, 24, 1, 1, 3001 );
    dat_p_j_massvNV[0]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massvNV[1], 2, 1, 1, 2, 24, 1, 2, 3001 );
    dat_p_j_massvNV[1]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massvNV[2], 4, 1, 1, 4, 24, 1, 4, 3001 );
    dat_p_j_massvNV[2]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massvNV[3], 6, 1, 1, 6, 24, 1, 6, 3001 );
    dat_p_j_massvNV[3]->Draw("pe1x0sames");     
    sprintf( cname, "%s/figs/j_massprofile_ak5.png", dir.c_str() );
    cp1->SaveAs(cname);
    
    // plotting profile of jet mass as a function of pT and nV
    TCanvas *cp1b = new TCanvas( "cp1b", "cp1b", 1200, 600 );
    cp1b->Divide(2,1);
    cp1b->cd(1);
    SetProfileProperties( all_p_j_massvpt[4], 1, 1, 1, 1, 0, 0, 1, 3001 );
    all_p_j_massvpt[4]->Draw("e2");     
    SetProfileProperties( all_p_j_massvpt[5], 2, 1, 1, 2, 0, 0, 2, 3001 );
    all_p_j_massvpt[5]->Draw("e2sames");     
    SetProfileProperties( all_p_j_massvpt[6], 4, 1, 1, 4, 0, 0, 4, 3001 );
    all_p_j_massvpt[6]->Draw("e2sames");     
    SetProfileProperties( all_p_j_massvpt[7], 6, 1, 1, 6, 0, 0, 6, 3001 );
    all_p_j_massvpt[7]->Draw("e2sames");     
    SetProfileProperties( dat_p_j_massvpt[4], 1, 1, 1, 1, 24, 1, 1, 3001 );
    dat_p_j_massvpt[4]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massvpt[5], 2, 1, 1, 2, 24, 1, 2, 3001 );
    dat_p_j_massvpt[5]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massvpt[6], 4, 1, 1, 4, 24, 1, 4, 3001 );
    dat_p_j_massvpt[6]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massvpt[7], 6, 1, 1, 6, 24, 1, 6, 3001 );
    dat_p_j_massvpt[7]->Draw("pe1x0sames");     
    
    cp1b->cd(2);
    SetProfileProperties( all_p_j_massvNV[4], 1, 1, 1, 1, 0, 0, 1, 3001 );
    all_p_j_massvNV[4]->Draw("e2"); 
    SetProfileProperties( all_p_j_massvNV[5], 2, 1, 1, 2, 0, 0, 2, 3001 );
    all_p_j_massvNV[5]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_massvNV[6], 4, 1, 1, 4, 0, 0, 4, 3001 );
    all_p_j_massvNV[6]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_massvNV[7], 6, 1, 1, 6, 0, 0, 6, 3001 );
    all_p_j_massvNV[7]->Draw("e2sames"); 
    SetProfileProperties( dat_p_j_massvNV[4], 1, 1, 1, 1, 24, 1, 1, 3001 );
    dat_p_j_massvNV[4]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massvNV[5], 2, 1, 1, 2, 24, 1, 2, 3001 );
    dat_p_j_massvNV[5]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massvNV[6], 4, 1, 1, 4, 24, 1, 4, 3001 );
    dat_p_j_massvNV[6]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massvNV[7], 6, 1, 1, 6, 24, 1, 6, 3001 );
    dat_p_j_massvNV[7]->Draw("pe1x0sames");     
    sprintf( cname, "%s/figs/j_massprofile_ak7.png", dir.c_str() );
    cp1b->SaveAs(cname);
    
    
    // plotting profile of jet mass as a function of pT and nV
    TCanvas *cp1c = new TCanvas( "cp1c", "cp1c", 1200, 600 );
    cp1c->Divide(2,1);
    cp1c->cd(1);
    SetProfileProperties( all_p_j_massvpt[8], 1, 1, 1, 1, 0, 0, 1, 3001 );
    all_p_j_massvpt[8]->Draw("e2");     
    SetProfileProperties( all_p_j_massvpt[9], 2, 1, 1, 2, 0, 0, 2, 3001 );
    all_p_j_massvpt[9]->Draw("e2sames");     
    SetProfileProperties( all_p_j_massvpt[10], 4, 1, 1, 4, 0, 0, 4, 3001 );
    all_p_j_massvpt[10]->Draw("e2sames");     
    SetProfileProperties( all_p_j_massvpt[11], 6, 1, 1, 6, 0, 0, 6, 3001 );
    all_p_j_massvpt[11]->Draw("e2sames");     
    SetProfileProperties( all_p_j_massvpt[12], 3, 1, 1, 3, 0, 0, 3, 3001 );
    all_p_j_massvpt[12]->Draw("e2sames");     
    SetProfileProperties( all_p_j_massvpt[13], 7, 1, 1, 7, 0, 0, 7, 3001 );
    all_p_j_massvpt[13]->Draw("e2sames");     
    SetProfileProperties( dat_p_j_massvpt[8], 1, 1, 1, 1, 24, 1, 1, 3001 );
    dat_p_j_massvpt[8]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massvpt[9], 2, 1, 1, 2, 24, 1, 2, 3001 );
    dat_p_j_massvpt[9]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massvpt[10], 4, 1, 1, 4, 24, 1, 4, 3001 );
    dat_p_j_massvpt[10]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massvpt[11], 6, 1, 1, 6, 24, 1, 6, 3001 );
    dat_p_j_massvpt[11]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massvpt[12], 3, 1, 1, 3, 24, 1, 3, 3001 );
    dat_p_j_massvpt[12]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massvpt[13], 7, 1, 1, 7, 24, 1, 7, 3001 );
    dat_p_j_massvpt[13]->Draw("pe1x0sames");     
    
    cp1c->cd(2);
    SetProfileProperties( all_p_j_massvNV[8], 1, 1, 1, 1, 0, 0, 1, 3001 );
    all_p_j_massvNV[8]->Draw("e2");     
    SetProfileProperties( all_p_j_massvNV[9], 2, 1, 1, 2, 0, 0, 2, 3001 );
    all_p_j_massvNV[9]->Draw("e2sames");     
    SetProfileProperties( all_p_j_massvNV[10], 4, 1, 1, 4, 0, 0, 4, 3001 );
    all_p_j_massvNV[10]->Draw("e2sames");     
    SetProfileProperties( all_p_j_massvNV[11], 6, 1, 1, 6, 0, 0, 6, 3001 );
    all_p_j_massvNV[11]->Draw("e2sames");     
    SetProfileProperties( all_p_j_massvNV[12], 3, 1, 1, 3, 0, 0, 3, 3001 );
    all_p_j_massvNV[12]->Draw("e2sames");     
    SetProfileProperties( all_p_j_massvNV[13], 7, 1, 1, 7, 0, 0, 7, 3001 );
    all_p_j_massvNV[13]->Draw("e2sames");     
    SetProfileProperties( dat_p_j_massvNV[8], 1, 1, 1, 1, 24, 1, 1, 3001 );
    dat_p_j_massvNV[8]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massvNV[9], 2, 1, 1, 2, 24, 1, 2, 3001 );
    dat_p_j_massvNV[9]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massvNV[10], 4, 1, 1, 4, 24, 1, 4, 3001 );
    dat_p_j_massvNV[10]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massvNV[11], 6, 1, 1, 6, 24, 1, 6, 3001 );
    dat_p_j_massvNV[11]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massvNV[12], 3, 1, 1, 3, 24, 1, 3, 3001 );
    dat_p_j_massvNV[12]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massvNV[13], 7, 1, 1, 7, 24, 1, 7, 3001 );
    dat_p_j_massvNV[13]->Draw("pe1x0sames");    
    sprintf( cname, "%s/figs/j_massprofile_ak8.png", dir.c_str() );
    cp1c->SaveAs(cname);
    
    // plotting ratio of masses for ak5, ak7, ak8 versus pT
    TCanvas *cp2 = new TCanvas( "cp2", "cp2", 1500, 600 );
    cp2->Divide(3,1);
    cp2->cd(1);
    SetProfileProperties( all_p_j_massOverAK5[0], 1, 1, 1, 24, 0, 0, 0, 0 );
    all_p_j_massOverAK5[0]->Draw("hist");     
    SetProfileProperties( all_p_j_massOverAK5[1], 1, 1, 2, 24, 1, 1, 2, 1001 );
    all_p_j_massOverAK5[1]->Draw("e2sames");     
    SetProfileProperties( all_p_j_massOverAK5[2], 1, 1, 4, 24, 1, 1, 4, 1001 );
    all_p_j_massOverAK5[2]->Draw("e2sames");     
    SetProfileProperties( all_p_j_massOverAK5[3], 1, 1, 6, 24, 1, 1, 6, 1001 );
    all_p_j_massOverAK5[3]->Draw("e2sames");     
    SetProfileProperties( all_p_j_massOverAK5[14], 1, 1, 1, 24, 1, 1, 1, 3001 );
    all_p_j_massOverAK5[14]->Draw("e2sames");     
    // data
    SetProfileProperties( dat_p_j_massOverAK5[1], 2, 1, 1, 2, 24, 1, 2, 3001 );
    dat_p_j_massOverAK5[1]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massOverAK5[2], 4, 1, 1, 4, 24, 1, 4, 3001 );
    dat_p_j_massOverAK5[2]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massOverAK5[3], 6, 1, 1, 6, 24, 1, 6, 3001 );
    dat_p_j_massOverAK5[3]->Draw("pe1x0sames");     
    cp2->cd(2);
    SetProfileProperties( all_p_j_massOverAK7[4], 1, 1, 1, 24, 0, 1, 0, 0 );
    all_p_j_massOverAK7[4]->Draw("hist"); 
    SetProfileProperties( all_p_j_massOverAK7[5], 1, 1, 2, 24, 1, 1, 2, 1001 );
    all_p_j_massOverAK7[5]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_massOverAK7[6], 1, 1, 4, 24, 1, 1, 4, 1001 );
    all_p_j_massOverAK7[6]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_massOverAK7[7], 1, 1, 6, 24, 1, 1, 6, 1001 );
    all_p_j_massOverAK7[7]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_massOverAK7[15], 1, 1, 1, 24, 1, 1, 1, 3001 );
    all_p_j_massOverAK7[15]->Draw("e2sames");    
    // data
    SetProfileProperties( dat_p_j_massOverAK7[5], 2, 1, 1, 2, 24, 1, 2, 3001 );
    dat_p_j_massOverAK7[5]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massOverAK7[6], 4, 1, 1, 4, 24, 1, 4, 3001 );
    dat_p_j_massOverAK7[6]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massOverAK7[7], 6, 1, 1, 6, 24, 1, 6, 3001 );
    dat_p_j_massOverAK7[7]->Draw("pe1x0sames");     
    cp2->cd(3);
    SetProfileProperties( all_p_j_massOverAK8[8], 1, 1, 1, 24, 0, 1, 0, 0 );
    all_p_j_massOverAK8[8]->Draw("lhist"); 
    SetProfileProperties( all_p_j_massOverAK8[9], 1, 1, 2, 24, 1, 1, 2, 1001 );
    all_p_j_massOverAK8[9]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_massOverAK8[10], 1, 1, 4, 24, 1, 1, 4, 1001 );
    all_p_j_massOverAK8[10]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_massOverAK8[11], 1, 1, 6, 24, 1, 1, 6, 1001 );
    all_p_j_massOverAK8[11]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_massOverAK8[12], 1, 1, 3, 24, 1, 1, 3, 1001 );
    all_p_j_massOverAK8[12]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_massOverAK8[13], 1, 1, 7, 24, 1, 1, 7, 1001 );
    all_p_j_massOverAK8[13]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_massOverAK8[16], 1, 1, 1, 24, 1, 1, 1, 3001 );
    all_p_j_massOverAK8[16]->Draw("e2sames");     
    // data
    SetProfileProperties( dat_p_j_massOverAK8[9], 2, 1, 1, 2, 24, 1, 2, 3001 );
    dat_p_j_massOverAK8[9]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massOverAK8[10], 4, 1, 1, 4, 24, 1, 4, 3001 );
    dat_p_j_massOverAK8[10]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massOverAK8[11], 6, 1, 1, 6, 24, 1, 6, 3001 );
    dat_p_j_massOverAK8[11]->Draw("pe1x0sames"); 
    SetProfileProperties( dat_p_j_massOverAK8[12], 3, 1, 1, 3, 24, 1, 3, 3001 );
    dat_p_j_massOverAK8[12]->Draw("pe1x0sames"); 
    SetProfileProperties( dat_p_j_massOverAK8[13], 7, 1, 1, 7, 24, 1, 7, 3001 );
    dat_p_j_massOverAK8[13]->Draw("pe1x0sames"); 
    sprintf( cname, "%s/figs/j_massratioprofile_ak.png", dir.c_str() );
    cp2->SaveAs(cname);
    
    // plotting ratio of pts for ak5, ak7, ak8 versus pT
    TCanvas *cp3 = new TCanvas( "cp3", "cp3", 1500, 600 );
    cp3->Divide(3,1);
    cp3->cd(1);
    SetProfileProperties( all_p_j_ptOverAK5[0], 1, 1, 1, 24, 0, 1, 0, 0 );
    all_p_j_ptOverAK5[0]->SetMinimum(0.8);
    all_p_j_ptOverAK5[0]->SetMaximum(1.6);
    all_p_j_ptOverAK5[0]->Draw("hist");     
    SetProfileProperties( all_p_j_ptOverAK5[1], 1, 1, 2, 24, 1, 1, 2, 1001 );
    all_p_j_ptOverAK5[1]->Draw("e2sames");     
    SetProfileProperties( all_p_j_ptOverAK5[2], 1, 1, 4, 24, 1, 1, 4, 1001 );
    all_p_j_ptOverAK5[2]->Draw("e2sames");     
    SetProfileProperties( all_p_j_ptOverAK5[3], 1, 1, 6, 24, 1, 1, 6, 1001 );
    all_p_j_ptOverAK5[3]->Draw("e2sames");     
    SetProfileProperties( all_p_j_ptOverAK5[14], 1, 1, 1, 24, 1, 1, 1, 3001 );
    all_p_j_ptOverAK5[14]->Draw("e2sames");     
    // data
    SetProfileProperties( dat_p_j_ptOverAK5[1], 2, 1, 1, 2, 24, 1, 2, 3001 );
    dat_p_j_ptOverAK5[1]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_ptOverAK5[2], 4, 1, 1, 4, 24, 1, 4, 3001 );
    dat_p_j_ptOverAK5[2]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_ptOverAK5[3], 6, 1, 1, 6, 24, 1, 6, 3001 );
    dat_p_j_ptOverAK5[3]->Draw("pe1x0sames");    
    cp3->cd(2);
    SetProfileProperties( all_p_j_ptOverAK7[4], 1, 1, 1, 24, 0, 1, 0, 0 );
    all_p_j_ptOverAK7[4]->SetMinimum(0.8);
    all_p_j_ptOverAK7[4]->SetMaximum(1.6);
    all_p_j_ptOverAK7[4]->Draw("hist"); 
    SetProfileProperties( all_p_j_ptOverAK7[5], 1, 1, 2, 24, 1, 1, 2, 1001 );
    all_p_j_ptOverAK7[5]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_ptOverAK7[6], 1, 1, 4, 24, 1, 1, 4, 1001 );
    all_p_j_ptOverAK7[6]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_ptOverAK7[7], 1, 1, 6, 24, 1, 1, 6, 1001 );
    all_p_j_ptOverAK7[7]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_ptOverAK7[15], 1, 1, 1, 24, 1, 1, 1, 3001 );
    all_p_j_ptOverAK7[15]->Draw("e2sames");  
    // data
    SetProfileProperties( dat_p_j_ptOverAK7[5], 2, 1, 1, 2, 24, 1, 2, 3001 );
    dat_p_j_ptOverAK7[5]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_ptOverAK7[6], 4, 1, 1, 4, 24, 1, 4, 3001 );
    dat_p_j_ptOverAK7[6]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_ptOverAK7[7], 6, 1, 1, 6, 24, 1, 6, 3001 );
    dat_p_j_ptOverAK7[7]->Draw("pe1x0sames");  
    cp3->cd(3);
    SetProfileProperties( all_p_j_ptOverAK8[8], 1, 1, 1, 24, 0, 1, 0, 0 );
    all_p_j_ptOverAK8[8]->SetMinimum(0.8);
    all_p_j_ptOverAK8[8]->SetMaximum(1.6);
    all_p_j_ptOverAK8[8]->Draw("hist"); 
    SetProfileProperties( all_p_j_ptOverAK8[9], 1, 1, 2, 24, 1, 1, 2, 1001 );
    all_p_j_ptOverAK8[9]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_ptOverAK8[10], 1, 1, 4, 24, 1, 1, 4, 1001 );
    all_p_j_ptOverAK8[10]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_ptOverAK8[11], 1, 1, 6, 24, 1, 1, 6, 1001 );
    all_p_j_ptOverAK8[11]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_ptOverAK8[12], 1, 1, 3, 24, 1, 1, 3, 1001 );
    all_p_j_ptOverAK8[12]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_ptOverAK8[13], 1, 1, 7, 24, 1, 1, 7, 1001 );
    all_p_j_ptOverAK8[13]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_ptOverAK8[16], 1, 1, 1, 24, 1, 1, 1, 3001 );
    all_p_j_ptOverAK8[16]->Draw("e2sames");
    // data
    SetProfileProperties( dat_p_j_ptOverAK8[9], 2, 1, 1, 2, 24, 1, 2, 3001 );
    dat_p_j_ptOverAK8[9]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_ptOverAK8[10], 4, 1, 1, 4, 24, 1, 4, 3001 );
    dat_p_j_ptOverAK8[10]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_ptOverAK8[11], 6, 1, 1, 6, 24, 1, 6, 3001 );
    dat_p_j_ptOverAK8[11]->Draw("pe1x0sames");
    SetProfileProperties( dat_p_j_ptOverAK8[12], 3, 1, 1, 3, 24, 1, 3, 3001 );
    dat_p_j_ptOverAK8[12]->Draw("pe1x0sames");
    SetProfileProperties( dat_p_j_ptOverAK8[13], 7, 1, 1, 7, 24, 1, 7, 3001 );
    dat_p_j_ptOverAK8[13]->Draw("pe1x0sames");
    sprintf( cname, "%s/figs/j_ptratioprofile_ak.png", dir.c_str() );
    cp3->SaveAs(cname);
    
    // plotting ratio of mass for ak5, ak7, ak8 versus nvert
    TCanvas *cp4 = new TCanvas( "cp4", "cp4", 1500, 600 );
    cp4->Divide(3,1);
    cp4->cd(1);
    SetProfileProperties( all_p_j_massOverAK5vNV[0], 1, 1, 1, 24, 0, 1, 0, 0 );
    all_p_j_massOverAK5vNV[0]->SetMinimum(0.4);
    all_p_j_massOverAK5vNV[0]->SetMaximum(1.6);
    all_p_j_massOverAK5vNV[0]->Draw("hist");     
    SetProfileProperties( all_p_j_massOverAK5vNV[1], 1, 1, 2, 24, 1, 1, 2, 1001 );
    all_p_j_massOverAK5vNV[1]->Draw("e2sames");     
    SetProfileProperties( all_p_j_massOverAK5vNV[2], 1, 1, 4, 24, 1, 1, 4, 1001 );
    all_p_j_massOverAK5vNV[2]->Draw("e2sames");     
    SetProfileProperties( all_p_j_massOverAK5vNV[3], 1, 1, 6, 24, 1, 1, 6, 1001 );
    all_p_j_massOverAK5vNV[3]->Draw("e2sames");     
    SetProfileProperties( all_p_j_massOverAK5vNV[14], 1, 1, 1, 24, 1, 1, 1, 3001 );
    all_p_j_massOverAK5vNV[14]->Draw("e2sames");     
    // data
    SetProfileProperties( dat_p_j_massOverAK5vNV[1], 2, 1, 1, 2, 24, 1, 2, 3001 );
    dat_p_j_massOverAK5vNV[1]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massOverAK5vNV[2], 4, 1, 1, 4, 24, 1, 4, 3001 );
    dat_p_j_massOverAK5vNV[2]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massOverAK5vNV[3], 6, 1, 1, 6, 24, 1, 6, 3001 );
    dat_p_j_massOverAK5vNV[3]->Draw("pe1x0sames");    
    cp4->cd(2);
    SetProfileProperties( all_p_j_massOverAK7vNV[4], 1, 1, 1, 24, 0, 1, 0, 0 );
    all_p_j_massOverAK7vNV[4]->SetMinimum(0.4);
    all_p_j_massOverAK7vNV[4]->SetMaximum(1.6);
    all_p_j_massOverAK7vNV[4]->Draw("hist"); 
    SetProfileProperties( all_p_j_massOverAK7vNV[5], 1, 1, 2, 24, 1, 1, 2, 1001 );
    all_p_j_massOverAK7vNV[5]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_massOverAK7vNV[6], 1, 1, 4, 24, 1, 1, 4, 1001 );
    all_p_j_massOverAK7vNV[6]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_massOverAK7vNV[7], 1, 1, 6, 24, 1, 1, 6, 1001 );
    all_p_j_massOverAK7vNV[7]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_massOverAK7vNV[15], 1, 1, 1, 24, 1, 1, 1, 3001 );
    all_p_j_massOverAK7vNV[15]->Draw("e2sames");  
    // data
    SetProfileProperties( dat_p_j_massOverAK7vNV[5], 2, 1, 1, 2, 24, 1, 2, 3001 );
    dat_p_j_massOverAK7vNV[5]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massOverAK7vNV[6], 4, 1, 1, 4, 24, 1, 4, 3001 );
    dat_p_j_massOverAK7vNV[6]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massOverAK7vNV[7], 6, 1, 1, 6, 24, 1, 6, 3001 );
    dat_p_j_massOverAK7vNV[7]->Draw("pe1x0sames");  
    cp4->cd(3);
    SetProfileProperties( all_p_j_massOverAK8vNV[8], 1, 1, 1, 24, 0, 1, 0, 0 );
    all_p_j_massOverAK8vNV[8]->SetMinimum(0.4);
    all_p_j_massOverAK8vNV[8]->SetMaximum(1.6);
    all_p_j_massOverAK8vNV[8]->Draw("hist"); 
    SetProfileProperties( all_p_j_massOverAK8vNV[9], 1, 1, 2, 24, 1, 1, 2, 1001 );
    all_p_j_massOverAK8vNV[9]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_massOverAK8vNV[10], 1, 1, 4, 24, 1, 1, 4, 1001 );
    all_p_j_massOverAK8vNV[10]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_massOverAK8vNV[11], 1, 1, 6, 24, 1, 1, 6, 1001 );
    all_p_j_massOverAK8vNV[11]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_massOverAK8vNV[12], 1, 1, 3, 24, 1, 1, 3, 1001 );
    all_p_j_massOverAK8vNV[12]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_massOverAK8vNV[13], 1, 1, 7, 24, 1, 1, 7, 1001 );
    all_p_j_massOverAK8vNV[13]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_massOverAK8vNV[16], 1, 1, 1, 24, 1, 1, 1, 3001 );
    all_p_j_massOverAK8vNV[16]->Draw("e2sames");
    // data
    SetProfileProperties( dat_p_j_massOverAK8vNV[9], 2, 1, 1, 2, 24, 1, 2, 3001 );
    dat_p_j_massOverAK8vNV[9]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massOverAK8vNV[10], 4, 1, 1, 4, 24, 1, 4, 3001 );
    dat_p_j_massOverAK8vNV[10]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_massOverAK8vNV[11], 6, 1, 1, 6, 24, 1, 6, 3001 );
    dat_p_j_massOverAK8vNV[11]->Draw("pe1x0sames");
    SetProfileProperties( dat_p_j_massOverAK8vNV[12], 3, 1, 1, 3, 24, 1, 3, 3001 );
    dat_p_j_massOverAK8vNV[12]->Draw("pe1x0sames");
    SetProfileProperties( dat_p_j_massOverAK8vNV[13], 7, 1, 1, 7, 24, 1, 7, 3001 );
    dat_p_j_massOverAK8vNV[13]->Draw("pe1x0sames");
    sprintf( cname, "%s/figs/j_massratioprofilevNV.png", dir.c_str() );
    cp4->SaveAs(cname);

    // plotting ratio of pts for ak5, ak7, ak8 versus nvert
    TCanvas *cp5 = new TCanvas( "cp5", "cp5", 1500, 600 );
    cp5->Divide(3,1);
    cp5->cd(1);
    SetProfileProperties( all_p_j_ptOverAK5vNV[0], 1, 1, 1, 24, 0, 1, 0, 0 );
    all_p_j_ptOverAK5vNV[0]->SetMinimum(0.8);
    all_p_j_ptOverAK5vNV[0]->SetMaximum(1.6);
    all_p_j_ptOverAK5vNV[0]->Draw("hist");     
    SetProfileProperties( all_p_j_ptOverAK5vNV[1], 1, 1, 2, 24, 1, 1, 2, 1001 );
    all_p_j_ptOverAK5vNV[1]->Draw("e2sames");     
    SetProfileProperties( all_p_j_ptOverAK5vNV[2], 1, 1, 4, 24, 1, 1, 4, 1001 );
    all_p_j_ptOverAK5vNV[2]->Draw("e2sames");     
    SetProfileProperties( all_p_j_ptOverAK5vNV[3], 1, 1, 6, 24, 1, 1, 6, 1001 );
    all_p_j_ptOverAK5vNV[3]->Draw("e2sames");     
    SetProfileProperties( all_p_j_ptOverAK5vNV[14], 1, 1, 1, 24, 1, 1, 1, 3001 );
    all_p_j_ptOverAK5vNV[14]->Draw("e2sames");     
    // data
    SetProfileProperties( dat_p_j_ptOverAK5vNV[1], 2, 1, 1, 2, 24, 1, 2, 3001 );
    dat_p_j_ptOverAK5vNV[1]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_ptOverAK5vNV[2], 4, 1, 1, 4, 24, 1, 4, 3001 );
    dat_p_j_ptOverAK5vNV[2]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_ptOverAK5vNV[3], 6, 1, 1, 6, 24, 1, 6, 3001 );
    dat_p_j_ptOverAK5vNV[3]->Draw("pe1x0sames");    
    cp5->cd(2);
    SetProfileProperties( all_p_j_ptOverAK7vNV[4], 1, 1, 1, 24, 0, 1, 0, 0 );
    all_p_j_ptOverAK7vNV[4]->SetMinimum(0.8);
    all_p_j_ptOverAK7vNV[4]->SetMaximum(1.6);
    all_p_j_ptOverAK7vNV[4]->Draw("hist"); 
    SetProfileProperties( all_p_j_ptOverAK7vNV[5], 1, 1, 2, 24, 1, 1, 2, 1001 );
    all_p_j_ptOverAK7vNV[5]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_ptOverAK7vNV[6], 1, 1, 4, 24, 1, 1, 4, 1001 );
    all_p_j_ptOverAK7vNV[6]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_ptOverAK7vNV[7], 1, 1, 6, 24, 1, 1, 6, 1001 );
    all_p_j_ptOverAK7vNV[7]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_ptOverAK7vNV[15], 1, 1, 1, 24, 1, 1, 1, 3001 );
    all_p_j_ptOverAK7vNV[15]->Draw("e2sames");  
    // data
    SetProfileProperties( dat_p_j_ptOverAK7vNV[5], 2, 1, 1, 2, 24, 1, 2, 3001 );
    dat_p_j_ptOverAK7vNV[5]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_ptOverAK7vNV[6], 4, 1, 1, 4, 24, 1, 4, 3001 );
    dat_p_j_ptOverAK7vNV[6]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_ptOverAK7vNV[7], 6, 1, 1, 6, 24, 1, 6, 3001 );
    dat_p_j_ptOverAK7vNV[7]->Draw("pe1x0sames");  
    cp5->cd(3);
    SetProfileProperties( all_p_j_ptOverAK8vNV[8], 1, 1, 1, 24, 0, 1, 0, 0 );
    all_p_j_ptOverAK8vNV[8]->SetMinimum(0.8);
    all_p_j_ptOverAK8vNV[8]->SetMaximum(1.6);
    all_p_j_ptOverAK8vNV[8]->Draw("hist"); 
    SetProfileProperties( all_p_j_ptOverAK8vNV[9], 1, 1, 2, 24, 1, 1, 2, 1001 );
    all_p_j_ptOverAK8vNV[9]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_ptOverAK8vNV[10], 1, 1, 4, 24, 1, 1, 4, 1001 );
    all_p_j_ptOverAK8vNV[10]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_ptOverAK8vNV[11], 1, 1, 6, 24, 1, 1, 6, 1001 );
    all_p_j_ptOverAK8vNV[11]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_ptOverAK8vNV[12], 1, 1, 3, 24, 1, 1, 3, 1001 );
    all_p_j_ptOverAK8vNV[12]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_ptOverAK8vNV[13], 1, 1, 7, 24, 1, 1, 7, 1001 );
    all_p_j_ptOverAK8vNV[13]->Draw("e2sames"); 
    SetProfileProperties( all_p_j_ptOverAK8vNV[16], 1, 1, 1, 24, 1, 1, 1, 3001 );
    all_p_j_ptOverAK8vNV[16]->Draw("e2sames");
    // data
    SetProfileProperties( dat_p_j_ptOverAK8vNV[9], 2, 1, 1, 2, 24, 1, 2, 3001 );
    dat_p_j_ptOverAK8vNV[9]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_ptOverAK8vNV[10], 4, 1, 1, 4, 24, 1, 4, 3001 );
    dat_p_j_ptOverAK8vNV[10]->Draw("pe1x0sames");     
    SetProfileProperties( dat_p_j_ptOverAK8vNV[11], 6, 1, 1, 6, 24, 1, 6, 3001 );
    dat_p_j_ptOverAK8vNV[11]->Draw("pe1x0sames");
    SetProfileProperties( dat_p_j_ptOverAK8vNV[12], 3, 1, 1, 3, 24, 1, 3, 3001 );
    dat_p_j_ptOverAK8vNV[12]->Draw("pe1x0sames");
    SetProfileProperties( dat_p_j_ptOverAK8vNV[13], 7, 1, 1, 7, 24, 1, 7, 3001 );
    dat_p_j_ptOverAK8vNV[13]->Draw("pe1x0sames");
    sprintf( cname, "%s/figs/j_ptratioprofilevNV.png", dir.c_str() );
    cp5->SaveAs(cname);

    // plotting jet areas
    // plotting ratio of mass for ak5, ak7, ak8 versus nvert
    TCanvas *ca = new TCanvas( "ca", "ca", 1500, 600 );
    ca->Divide(3,1);
    ca->cd(1);
    all_h_j_area[0]->Draw("hist"); SetHistProperties( all_h_j_area[0], 1, 1, 2, 24, 1, 1, 1, 0 );
    all_h_j_area[1]->Draw("histsames"); SetHistProperties( all_h_j_area[1], 3, 1, 2, 24, 1, 1, 2, 0 ); 
    all_h_j_area[2]->Draw("histsames"); SetHistProperties( all_h_j_area[2], 4, 1, 2, 24, 1, 1, 4, 0 );
    all_h_j_area[3]->Draw("histsames"); SetHistProperties( all_h_j_area[3], 6, 1, 2, 24, 1, 1, 6, 0 );
    dat_h_j_area[0]->Draw("pe1x0sames"); SetHistProperties( dat_h_j_area[0], 1, 1, 1, 1, 24, 1, 6, 1001 );
    dat_h_j_area[1]->Draw("pe1x0sames"); SetHistProperties( dat_h_j_area[1], 2, 1, 1, 2, 24, 1, 6, 1001 );
    dat_h_j_area[2]->Draw("pe1x0sames"); SetHistProperties( dat_h_j_area[2], 4, 1, 1, 4, 24, 1, 6, 1001 );
    dat_h_j_area[3]->Draw("pe1x0sames"); SetHistProperties( dat_h_j_area[3], 6, 1, 1, 6, 24, 1, 6, 1001 );
    ca->cd(2);
    all_h_j_area[4]->Draw("hist"); SetHistProperties( all_h_j_area[4], 1, 1, 2, 24, 1, 1, 1, 0 ); 
    all_h_j_area[5]->Draw("histsames"); SetHistProperties( all_h_j_area[5], 2, 1, 2, 24, 1, 1, 2, 0 );
    all_h_j_area[6]->Draw("histsames"); SetHistProperties( all_h_j_area[6], 4, 1, 2, 24, 1, 1, 4, 0 );
    all_h_j_area[7]->Draw("histsames"); SetHistProperties( all_h_j_area[7], 6, 1, 2, 24, 1, 1, 6, 0 );
    dat_h_j_area[4]->Draw("pe1x0sames"); SetHistProperties( dat_h_j_area[4], 1, 1, 1, 1, 24, 1, 6, 1001 );
    dat_h_j_area[5]->Draw("pe1x0sames"); SetHistProperties( dat_h_j_area[5], 2, 1, 1, 2, 24, 1, 6, 1001 );
    dat_h_j_area[6]->Draw("pe1x0sames"); SetHistProperties( dat_h_j_area[6], 4, 1, 1, 4, 24, 1, 6, 1001 );
    dat_h_j_area[7]->Draw("pe1x0sames"); SetHistProperties( dat_h_j_area[7], 6, 1, 1, 6, 24, 1, 6, 1001 );
    ca->cd(3);
    all_h_j_area[8]->Draw("hist"); SetHistProperties( all_h_j_area[8], 1, 1, 2, 24, 1, 1, 1, 0 );
    all_h_j_area[9]->Draw("histsames"); SetHistProperties( all_h_j_area[9], 2, 1, 2, 24, 1, 1, 2, 0 );
    all_h_j_area[10]->Draw("histsames"); SetHistProperties( all_h_j_area[10], 4, 1, 2, 24, 1, 1, 4, 0 );
    all_h_j_area[11]->Draw("histsames"); SetHistProperties( all_h_j_area[11], 6, 1, 2, 24, 1, 1, 6, 0 );
    all_h_j_area[12]->Draw("histsames"); SetHistProperties( all_h_j_area[12], 3, 1, 2, 24, 1, 1, 6, 0 );
    all_h_j_area[13]->Draw("histsames"); SetHistProperties( all_h_j_area[13], 7, 1, 2, 24, 1, 1, 6, 0 );
    dat_h_j_area[8]->Draw("pe1x0sames"); SetHistProperties( dat_h_j_area[8], 1, 1, 1, 1, 24, 1, 6, 1001 );
    dat_h_j_area[9]->Draw("pe1x0sames"); SetHistProperties( dat_h_j_area[9], 2, 1, 1, 2, 24, 1, 6, 1001 );
    dat_h_j_area[10]->Draw("pe1x0sames"); SetHistProperties( dat_h_j_area[10], 4, 1, 1, 4, 24, 1, 6, 1001 );
    dat_h_j_area[11]->Draw("pe1x0sames"); SetHistProperties( dat_h_j_area[11], 6, 1, 1, 6, 24, 1, 6, 1001 );
    dat_h_j_area[12]->Draw("pe1x0sames"); SetHistProperties( dat_h_j_area[12], 3, 1, 1, 3, 24, 1, 3, 1001 );
    dat_h_j_area[13]->Draw("pe1x0sames"); SetHistProperties( dat_h_j_area[13], 7, 1, 1, 7, 24, 1, 7, 1001 );
    sprintf( cname, "%s/figs/j_areas.png", dir.c_str() );
    ca->SaveAs(cname);

    // plotting boosted regime (n bjets?)
    
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
    //tdrStyle->SetErrorX(0.);
    
    //tdrStyle->SetMarkerStyle(20);
    
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