#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif

#include "RooDataSet.h"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "RooPlot.h"
#include "TROOT.h"
using namespace RooFit ;

void plotPdf_5D_XWW() {
    
    gROOT->ProcessLine(".L ~/tdrstyle.C");
    setTDRStyle();
    gStyle->SetPadLeftMargin(0.16);
    
    // Declaration of the PDFs to use
    gROOT->ProcessLine(".L PDFs/RooSpinTwo_5D.cxx++");
    
    // Observables (5D)
    RooRealVar* h1 = new RooRealVar("costheta1","h1",-1,1);
    RooRealVar* h2 = new RooRealVar("costheta2","h2",-1,1);
    RooRealVar* hs = new RooRealVar("costhetastar","hs",-1,1);
    RooRealVar* Phi = new RooRealVar("phi","Phi",-TMath::Pi(),TMath::Pi());
    RooRealVar* Phi1 = new RooRealVar("phistar1","Phi1",-TMath::Pi(),TMath::Pi());
    
    // angular variables
    // These values correspond to the 2m+
    RooRealVar* fppVal = new RooRealVar("fppVal", "fppVal", 0.0089);
    RooRealVar* fmmVal = new RooRealVar("fmmVal", "fmmVal", 0.0089);
    RooRealVar* fpmVal = new RooRealVar("fpmVal", "fpmVal", 0.3108);
    RooRealVar* fp0Val = new RooRealVar("fp0Val", "fp0Val", 0.0643);
    RooRealVar* f0mVal = new RooRealVar("f0mVal", "f0mVal", 0.0643);
    
    RooRealVar* phippVal = new RooRealVar("phippVal", "phippVal", 0);
    RooRealVar* phimmVal = new RooRealVar("phimmVal", "phimmVal", 0);
    RooRealVar* phipmVal = new RooRealVar("phipmVal", "phipmVal", 0);
    RooRealVar* phip0Val = new RooRealVar("phip0Val", "phip0Val", 0);
    RooRealVar* phi0mVal = new RooRealVar("phi0mVal", "phi0mVal", 0);

    // related to the gg/qq productions 
    RooRealVar* fz1Val = new RooRealVar("fz1Val", "fz1Val", 0);
    RooRealVar* fz2Val = new RooRealVar("fz2Val", "fz2Val", 1.0);

    // Even more parameters, do not have to touch, based on W couplings
    RooRealVar* R1Val = new RooRealVar("R1Val","R1Val",1);
    RooRealVar* R2Val = new RooRealVar("R2Val","R2Val",1);

    // these are the acceptance terms associated with the production angles
    // the default setting is for setting no-acceptance
    RooRealVar* para2 = new RooRealVar("para2", "para2", 0);
    RooRealVar* para4 = new RooRealVar("para4", "para4", 0);
    RooRealVar* para6 = new RooRealVar("para6", "para6", 0);	
    RooRealVar* para8 = new RooRealVar("para8", "para8", 0);

    RooRealVar* acca0 = new RooRealVar("acca0", "acca0", 1);
    RooRealVar* acca1 = new RooRealVar("acca1", "acca1", 0);
    RooRealVar* acca2 = new RooRealVar("acca2", "acca2", 0);
    RooRealVar* acca4 = new RooRealVar("acca4", "acca4", 0);
    
    // PDF definition SM Higgs (JP = 2+)
    RooSpinTwo_5D *myPDF = new RooSpinTwo_5D("myPDF","myPDF", *h1, *h2, *hs, *Phi, *Phi1, *fppVal, *fmmVal, *fpmVal, *fp0Val, *f0mVal, *phippVal, *phimmVal, *phipmVal, *phip0Val, *phi0mVal, *fz1Val, *fz2Val, *R1Val, *R2Val, *para2, *para4, *para6, *para8, *acca0, *acca1, *acca2, *acca4);
    
    // Grab input file to convert to RooDataSet
    TFile* fin = new TFile("THiggsWW_250_JHU.root");
    TTree* tin = (TTree*) fin->Get("angles");
    RooDataSet data("data","data",tin,RooArgSet(*h1,*h2, *hs, *Phi, *Phi1));


    // setting for 2-
    RooRealVar* fppValp = new RooRealVar("fppValp", "fppValp", 0.102);
    RooRealVar* fmmValp = new RooRealVar("fmmValp", "fmmValp", 0.102);
    RooRealVar* fpmValp = new RooRealVar("fpmValp", "fpmValp", 0.);
    RooRealVar* fp0Valp = new RooRealVar("fp0Valp", "fp0Valp", 0.199);
    RooRealVar* f0mValp = new RooRealVar("f0mValp", "f0mValp", 0.199);

    RooRealVar* phippValp = new RooRealVar("phippValp", "phippValp", TMath::Pi());
    RooRealVar* phimmValp = new RooRealVar("phimmValp", "phimmValp", 0);
    RooRealVar* phipmValp = new RooRealVar("phipmValp", "phipmValp", 0);
    RooRealVar* phip0Valp = new RooRealVar("phip0Valp", "phip0Valp", TMath::Pi());
    RooRealVar* phi0mValp = new RooRealVar("phi0mValp", "phi0mValp", 0);

    RooSpinTwo_5D *myPDFA = new RooSpinTwo_5D("myPDF","myPDF", *h1, *h2, *hs, *Phi, *Phi1, *fppValp, *fmmValp, *fpmValp, *fp0Valp, *f0mValp, *phippValp, *phimmValp, *phipmValp, *phip0Valp, *phi0mValp, *fz1Val, *fz2Val, *R1Val, *R2Val, *para2, *para4, *para6, *para8, *acca0, *acca1, *acca2, *acca4);

  
    
    /*
    for (int i=1;i<10;i++) {
      RooArgSet* row = data.get(i);
      row->Print("v");
      std::cout << "weight: " << data.weight() << std::endl;
    }
    */
    
    // read another input file
    TFile* fin2 = new TFile("PTHiggsWW_250_JHU.root");
    TTree* tin2 = (TTree*) fin2->Get("angles");
    RooDataSet data2("data2","data2",tin2,RooArgSet(*h1,*h2, *hs, *Phi, *Phi1));
    
    // setting for 2L+
    
    RooRealVar* fppVal2L = new RooRealVar("fppVal2L", "fppVal2L", 0.063);
    RooRealVar* fmmVal2L = new RooRealVar("fmmVal2L", "fmmVal2L", 0.063);
    RooRealVar* fpmVal2L = new RooRealVar("fpmVal2L", "fpmVal2L", 0.);
    RooRealVar* fp0Val2L = new RooRealVar("fp0Val2L", "fp0Val2L", 0.);
    RooRealVar* f0mVal2L = new RooRealVar("f0mVal2L", "f0mVal2L", 0.);

    RooRealVar* phippVal2L = new RooRealVar("phippVal2L", "phippVal2L", TMath::Pi());
    RooRealVar* phimmVal2L = new RooRealVar("phimmVal2L", "phimmVal2L", TMath::Pi());
    RooRealVar* phipmVal2L = new RooRealVar("phipmVal2L", "phipmVal2L", 0);
    RooRealVar* phip0Val2L = new RooRealVar("phip0Val2L", "phip0Val2L", 0);
    RooRealVar* phi0mVal2L = new RooRealVar("phi0mVal2L", "phi0mVal2L", 0);

    RooRealVar* fz1Val2L = new RooRealVar("fz1Val2L", "fz1Val2L", 0);
    RooRealVar* fz2Val2L = new RooRealVar("fz2Val2L", "fz2Val2L", 0.4);

    RooSpinTwo_5D *myPDF2L = new RooSpinTwo_5D("myPDF","myPDF", *h1, *h2, *hs, *Phi, *Phi1, *fppVal2L, *fmmVal2L, *fpmVal2L, *fp0Val2L, *f0mVal2L, *phippVal2L, *phimmVal2L, *phipmVal2L, *phip0Val2L, *phi0mVal2L, *fz1Val2L, *fz2Val2L, *R1Val, *R2Val, *para2, *para4, *para6, *para8, *acca0, *acca1, *acca2, *acca4);

    // dataset for (JP = 2-)
    TFile* fin3 = new TFile("2LWW_250_JHU.root");
    TTree* tin3 = (TTree*) fin3->Get("angles");
    RooDataSet data3("data3","data3",tin3,RooArgSet(*h1,*h2, *hs, *Phi, *Phi1));



    // P L O T   . . .  
    // (All parameters fixed, no fitting, just looking at the shape of the PDFs w.r.t. the data)
    TH1F* dum0 = new TH1F("dum0","dum0",1,0,1); dum0->SetLineColor(kRed); dum0->SetMarkerColor(kBlack); dum0->SetLineWidth(3);
    TH1F* dum1 = new TH1F("dum1","dum1",1,0,1); dum1->SetLineColor(kBlue); dum1->SetMarkerColor(kBlack); dum1->SetMarkerStyle(24), dum1->SetLineWidth(3);  
    TH1F* dum2 = new TH1F("dum2","dum2",1,0,1); dum2->SetLineColor(kGreen); dum2->SetMarkerColor(kBlack); dum2->SetMarkerStyle(21), dum2->SetLineWidth(3); // 2L+

    TLegend * box3 = new TLegend(0.1,0.1,0.9,0.92);
    box3->SetFillColor(0);
    box3->SetBorderSize(0);
    box3->AddEntry(dum0,"X#rightarrow WW JP = 2m+","lp");
    box3->AddEntry(dum1,"X#rightarrow WW JP = 2-","lp");
    box3->AddEntry(dum2,"X#rightarrow WW JP = 2L+","lp");
    

    RooPlot* h1frame =  h1->frame(55);
    data.plotOn(h1frame, LineColor(kBlack));
    myPDF->plotOn(h1frame, LineColor(kRed));
    data2.plotOn(h1frame, LineColor(kBlack), MarkerStyle(24));
    myPDFA->plotOn(h1frame, LineColor(kBlue));
    data3.plotOn(h1frame, LineColor(kBlack), MarkerStyle(21));
    myPDF2L->plotOn(h1frame, LineColor(kGreen));    

    RooPlot* h2frame =  h2->frame(55);
    data.plotOn(h2frame, LineColor(kBlack));
    myPDF->plotOn(h2frame, LineColor(kRed));
    data2.plotOn(h2frame, LineColor(kBlack), MarkerStyle(24));
    myPDFA->plotOn(h2frame, LineColor(kBlue));
    data3.plotOn(h2frame, LineColor(kBlack), MarkerStyle(21));
    myPDF2L->plotOn(h2frame, LineColor(kGreen));
    
    
    RooPlot* hsframe =  hs->frame(55);
    data.plotOn(hsframe, LineColor(kBlack));
    myPDF->plotOn(hsframe, LineColor(kRed));
    data2.plotOn(hsframe, LineColor(kBlack), MarkerStyle(24));
    myPDFA->plotOn(hsframe, LineColor(kBlue));
    data3.plotOn(hsframe, LineColor(kBlack), MarkerStyle(21));
    myPDF2L->plotOn(hsframe, LineColor(kGreen));


    RooPlot* Phiframe =  Phi->frame(55);
    data.plotOn(Phiframe, LineColor(kBlack));
    myPDF->plotOn(Phiframe, LineColor(kRed));
    data2.plotOn(Phiframe, LineColor(kBlack), MarkerStyle(24));
    myPDFA->plotOn(Phiframe, LineColor(kBlue));
    data3.plotOn(Phiframe, LineColor(kBlack), MarkerStyle(21));
    myPDF2L->plotOn(Phiframe, LineColor(kGreen));
    

    RooPlot* Phi1frame =  Phi1->frame(55);
    data.plotOn(Phi1frame, LineColor(kBlack));
    myPDF->plotOn(Phi1frame, LineColor(kRed));
    data2.plotOn(Phi1frame, LineColor(kBlack), MarkerStyle(24));
    myPDFA->plotOn(Phi1frame, LineColor(kBlue));
    data3.plotOn(Phi1frame, LineColor(kBlack), MarkerStyle(21));
    myPDF2L->plotOn(Phi1frame, LineColor(kGreen));
    
    TCanvas* czz = new TCanvas( "czz", "czz", 1000, 600 );
    czz->Divide(3,2);
    czz->cd(1);
    hsframe->Draw();
    czz->cd(2);
    Phi1frame->Draw();
    czz->cd(3);
    box3->Draw();
    czz->cd(4);
    h1frame->Draw();
    czz->cd(5);
    h2frame->Draw();
    czz->cd(6);
    Phiframe->Draw();
    
    czz->SaveAs("epsfiles/angles_TWW250_JHU.eps");
    czz->SaveAs("pngfiles/angles_TWW250_JHU.png");

}
