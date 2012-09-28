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
    
    if (lineColor > 0) h->SetLineColor( lineColor );
    if (lineStyle > 0) h->SetLineStyle( lineStyle );
    if (lineWidth > 0) h->SetLineWidth( lineWidth );

    if (markerColor > 0) h->SetMarkerColor( markerColor );
    if (markerStyle > 0) h->SetMarkerStyle( markerStyle );
    if (markerSize > 0) h->SetMarkerSize( markerSize );

    if (fillColor > 0) h->SetFillColor( fillColor );
    if (fillStyle > 0) h->SetFillStyle( fillStyle );
    
}

void SetProfileProperties( TProfile* h, int lineColor, int lineStyle, int lineWidth, int markerColor, int markerStyle, int markerSize, int fillColor, int fillStyle){
    
    if (lineColor > 0) h->SetLineColor( lineColor );
    if (lineStyle > 0) h->SetLineStyle( lineStyle );
    if (lineWidth > 0) h->SetLineWidth( lineWidth );
    
    if (markerColor > 0) h->SetMarkerColor( markerColor );
    if (markerStyle > 0) h->SetMarkerStyle( markerStyle );
    if (markerSize > 0) h->SetMarkerSize( markerSize );
    
    if (fillColor > 0) h->SetFillColor( fillColor );
    if (fillStyle > 0) h->SetFillStyle( fillStyle );
    
}

void plotHistos(std::string dir="figs", double ilumi = 1.){
  
    setTDRStyle();
    gStyle->SetPadLeftMargin(0.16);
    
    // files
    TFile f_wj("ntuples/histos_wj.root");
    TFile f_ww("ntuples/histos_ww.root");    
    TFile f_tt("ntuples/histos_tt.root");    
    // combination of wj, ww, tt
    TFile f_all("ntuples/histos_tt.root");    
    
    // jet collections
    const int nJetTypes_C = 14;
    std::string jetNames[nJetTypes_C] = {"ak5","ak5tr","ak5pr","ak5ft","ak7","ak7tr","ak7pr","ak7ft","ak8","ak8tr","ak8pr","ak8ft","ca8","ca8pr"};
    int nJetTypes = nJetTypes_C;
    
    TH1F* wj_h_j_mass[nJetTypes_C];
    TH1F* ww_h_j_mass[nJetTypes_C];
    TH1F* tt_h_j_mass[nJetTypes_C];
    THStack* hs_mass_ak5[nJetTypes_C];
    
    TH1F* all_h_j_mass_pt50to100[nJetTypes_C];
    TH1F* all_h_j_mass_pt100to150[nJetTypes_C];
    TH1F* all_h_j_mass_pt150to200[nJetTypes_C];
    TH1F* all_h_j_mass_pt200to300[nJetTypes_C];
    TH1F* all_h_j_mass_pt300andup[nJetTypes_C];
    
    TProfile* all_p_j_massvpt[nJetTypes_C];
    TProfile* all_p_j_massvNV[nJetTypes_C];

    // -----------------------------------------------
    // canvasii
    char hname[192];
    char cname[192];
    TCanvas *c1 = new TCanvas("c1","c1",1200,600);
    c1->Divide(2,1);
    TCanvas *c2 = new TCanvas("c2","c2",1200,600);
    c2->Divide(2,1);

    
    // jet-related plots for each individual jet species
    for (int i = 0; i < nJetTypes; i++){
        
        // -----------------------------------------------
        // jet mass plots
        sprintf( hname, "h_j_%s_mass", jetNames[i].c_str() );
        wj_h_j_mass[i] = (TH1F*) f_wj.Get(hname); SetHistProperties( wj_h_j_mass[i], 0, 0, 0, 0, 0, 0, 2, 1001 );
        ww_h_j_mass[i] = (TH1F*) f_ww.Get(hname); SetHistProperties( ww_h_j_mass[i], 0, 0, 0, 0, 0, 0, 7, 1001 );   
        tt_h_j_mass[i] = (TH1F*) f_tt.Get(hname); SetHistProperties( tt_h_j_mass[i], 0, 0, 0, 0, 0, 0, 6, 1001 );   
        
        hs_mass_ak5[i] = new THStack( "hs_mass_ak5", "hs_mass_ak5" ); 
        hs_mass_ak5[i]->Add( wj_h_j_mass[i] );
        hs_mass_ak5[i]->Add( ww_h_j_mass[i] );
        hs_mass_ak5[i]->Add( tt_h_j_mass[i] );
        
        c1->cd(1);
        //hs_mass_ak5[i]->SetMinimum( 1. );
        //hs_mass_ak5[i]->SetMaximum( 1.e8 );
        hs_mass_ak5[i]->Draw();
        c1->cd(2);
        gPad->SetLogy();
        hs_mass_ak5[i]->Draw();
        sprintf( cname, "figs/j_mass_%s.eps", jetNames[i].c_str() );
        c1->SaveAs(cname);
        
        // jet mass (in pt bins) plot
        sprintf( hname, "h_j_%s_mass_pt50to100", jetNames[i].c_str() );
        all_h_j_mass_pt50to100[i] = (TH1F*) f_all.Get(hname); SetHistProperties( all_h_j_mass_pt50to100[i], 1, 0, 0, 0, 0, 0, 0, 0 );
        sprintf( hname, "h_j_%s_mass_pt100to150", jetNames[i].c_str() );
        all_h_j_mass_pt100to150[i] = (TH1F*) f_all.Get(hname); SetHistProperties( all_h_j_mass_pt100to150[i], 2, 0, 0, 0, 0, 0, 0, 0 );
        sprintf( hname, "h_j_%s_mass_pt150to200", jetNames[i].c_str() );
        all_h_j_mass_pt150to200[i] = (TH1F*) f_all.Get(hname); SetHistProperties( all_h_j_mass_pt150to200[i], 3, 0, 0, 0, 0, 0, 0, 0 );
        sprintf( hname, "h_j_%s_mass_pt200to300", jetNames[i].c_str() );
        all_h_j_mass_pt200to300[i] = (TH1F*) f_all.Get(hname); SetHistProperties( all_h_j_mass_pt200to300[i], 4, 0, 0, 0, 0, 0, 0, 0 );
        sprintf( hname, "h_j_%s_mass_pt300andup", jetNames[i].c_str() );
        all_h_j_mass_pt300andup[i] = (TH1F*) f_all.Get(hname); SetHistProperties( all_h_j_mass_pt300andup[i], 5, 0, 0, 0, 0, 0, 0, 0 );

        c2->cd(1);
        all_h_j_mass_pt50to100[i]->Draw();
        all_h_j_mass_pt100to150[i]->Draw("sames");
        all_h_j_mass_pt150to200[i]->Draw("sames");
        all_h_j_mass_pt200to300[i]->Draw("sames");
        all_h_j_mass_pt300andup[i]->Draw("sames");
        c2->cd(2);
        gPad->SetLogy();
        all_h_j_mass_pt50to100[i]->Draw();
        all_h_j_mass_pt100to150[i]->Draw("sames");
        all_h_j_mass_pt150to200[i]->Draw("sames");
        all_h_j_mass_pt200to300[i]->Draw("sames");
        all_h_j_mass_pt300andup[i]->Draw("sames");
        sprintf( cname, "figs/j_massInBins_%s.eps", jetNames[i].c_str() );
        c2->SaveAs(cname);
        
        // ratio plots
        sprintf( hname, "p_j_%s_massvpt", jetNames[i].c_str() );
        all_p_j_massvpt[i] = (TProfile*) f_all.Get(hname); 
        sprintf( hname, "p_j_%s_massvNV", jetNames[i].c_str() );
        all_p_j_massvNV[i] = (TProfile*) f_all.Get(hname); 

    }

    TCanvas *cp1 = new TCanvas( "cp1", "cp1", 1200, 600 );
    cp1->Divide(2,1);
    cp1->cd(1);
    SetProfileProperties( all_p_j_massvpt[0], 1, 1, 1, 1, 20, 1, 0, 0 );
    all_p_j_massvpt[0]->Draw("ep");     
    SetProfileProperties( all_p_j_massvpt[1], 2, 1, 1, 2, 20, 1, 0, 0 );
    all_p_j_massvpt[1]->Draw("epsames");     
    SetProfileProperties( all_p_j_massvpt[2], 4, 1, 1, 4, 20, 1, 0, 0 );
    all_p_j_massvpt[2]->Draw("epsames");     
    SetProfileProperties( all_p_j_massvpt[3], 6, 1, 1, 6, 20, 1, 0, 0 );
    all_p_j_massvpt[3]->Draw("epsames");     
    cp1->cd(2);
    SetProfileProperties( all_p_j_massvNV[0], 1, 1, 1, 1, 20, 1, 0, 0 );
    all_p_j_massvNV[0]->Draw("ep"); 
    SetProfileProperties( all_p_j_massvNV[1], 2, 1, 1, 2, 20, 1, 0, 0 );
    all_p_j_massvNV[1]->Draw("epsames"); 
    SetProfileProperties( all_p_j_massvNV[2], 4, 1, 1, 4, 20, 1, 0, 0 );
    all_p_j_massvNV[2]->Draw("epsames"); 
    SetProfileProperties( all_p_j_massvNV[3], 6, 1, 1, 6, 20, 1, 0, 0 );
    all_p_j_massvNV[3]->Draw("epsames"); 
    sprintf( cname, "figs/j_massprofile_ak5.eps");
    cp1->SaveAs(cname);

    
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