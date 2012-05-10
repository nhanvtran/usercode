#define myutils_cxx
#include "myutils.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <iostream>
#include "TH1F.h"

TH1F * myutils::GetFitSlicesY(TH2F* h2d, int param){
    
    TObjArray aSlices;
    h2d->FitSlicesY(0, 0, -1, 0, "QNR", &aSlices);
    TH1F* h1 = (TH1F*) aSlices[1];
    TH1F* h2 = (TH1F*) aSlices[2];    
    // have to clone because aslices goes away after de-scoping
    TH1F* hcl1 = (TH1F*) h1->Clone();
    TH1F* hcl2 = (TH1F*) h2->Clone();
    
    hcl1->SetLineColor( h2d->GetLineColor() );
    hcl1->SetMarkerColor( h2d->GetMarkerColor() ); 
    hcl1->SetFillColor( h2d->GetFillColor() ); 
    hcl1->SetLineStyle( h2d->GetLineStyle() );
    hcl1->SetMarkerStyle( h2d->GetMarkerStyle() ); 
    hcl1->SetFillStyle( h2d->GetFillStyle() ); 
    hcl2->SetLineColor( h2d->GetLineColor() );
    hcl2->SetMarkerColor( h2d->GetMarkerColor() ); 
    hcl2->SetFillColor( h2d->GetFillColor() ); 
    hcl2->SetLineStyle( h2d->GetLineStyle() );
    hcl2->SetMarkerStyle( h2d->GetMarkerStyle() ); 
    hcl2->SetFillStyle( h2d->GetFillStyle() ); 
    
    if (param == 1){ return hcl1; }
    else if (param == 2){ return hcl2; }
    else{ std::cout << "WARNING INVALID PARAM!!!!" << std::endl; }
}
