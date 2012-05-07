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
    TH1F* h = (TH1F*) aSlices[param];
    
    // have to clone because aslices goes away after de-scoping
    TH1F* hcl = (TH1F*) h->Clone();
    return hcl;
    
}
