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
using namespace RooFit ;

void plotPdf_5D_HWW(float mH = 125, TString mode="JHU", TString dataType = "SM"){
    
    gROOT->ProcessLine(".L ~/tdrstyle.C");
    setTDRStyle();
    gStyle->SetPadLeftMargin(0.16);
    
    // Declaration of the PDFs to use
    gROOT->ProcessLine(".L PDFs/RooHWW_5D.cxx+");
    gSystem->Load("PDFs/RooHWW.cxx");

    // Observables (5D)
    RooRealVar* m1 = new RooRealVar("wplusmass","m1",10,120);
    RooRealVar* m2 = new RooRealVar("wminusmass","m2",10,120);
    RooRealVar* h1 = new RooRealVar("costheta1","h1",-1,1);
    RooRealVar* h2 = new RooRealVar("costheta2","h2",-1,1);
    RooRealVar* Phi = new RooRealVar("phi","Phi",-TMath::Pi(),TMath::Pi());
    RooRealVar* wt = new RooRealVar("wt", "wt", 0.0, 10);
    
    
    // Parameters
    RooRealVar* mW = new RooRealVar("mW","mW",80.398);
    RooRealVar* mX = new RooRealVar("mX","mX",mH);
    RooRealVar* gamW = new RooRealVar("gamW","gamW",2.1);
    // More parameters, these are the couplings "a1","a2","a3" which are _complex_ (which is why there are phases "phi*Val")
    RooRealVar* a1Val = new RooRealVar("a1Val","a1Val",1);
    RooRealVar* phi1Val = new RooRealVar("phi1Val","phi1Val", 0);
    RooRealVar* a2Val = new RooRealVar("a2Val","a2Val",0);
    RooRealVar* phi2Val = new RooRealVar("phi2Val","phi2Val", 0);
    RooRealVar* a3Val = new RooRealVar("a3Val","a3Val",0);
    RooRealVar* phi3Val = new RooRealVar("phi3Val","phi3Val",0);
    
    //
    // alternative defintions in terms of the g1->g4
    // 
    RooRealVar* useGTerm = new RooRealVar("useGTerm", "useGTerm",1.); // set to 1 if using g coupling
    RooRealVar* g1Val = new RooRealVar("g1Val", "g1Val", 1);
    RooRealVar* g2Val = new RooRealVar("g2Val", "g2Val", 0.);
    RooRealVar* g3Val = new RooRealVar("g3Val", "g3Val", 0.);
    RooRealVar* g4Val = new RooRealVar("g4Val", "g4Val", 0.);
    
    // Even more parameters, do not have to touch, based on W couplings
    RooRealVar* R1Val = new RooRealVar("R1Val","R1Val",1);
    RooRealVar* R2Val = new RooRealVar("R2Val","R2Val",1);
    
    // PDF definition SM Higgs (JP = 0+)
    RooHWW_5D *myPDF = new RooHWW_5D("myPDF","myPDF",*m1,*m2,*h1,*h2,*Phi,
				     *a1Val,*phi1Val,*a2Val,*phi2Val,*a3Val,*phi3Val,
				     *useGTerm, *g1Val, *g2Val, *g3Val, *g4Val,
				     *mW,*gamW,*mX,*R1Val,*R2Val);

    // PDF definition Pseudoscalar Higgs (JP = 0-)
    RooRealVar* a1Valp = new RooRealVar("a1Valp","a1Valp",0);
    RooRealVar* a3Valp = new RooRealVar("a3Valp","a3Valp",1);
    RooRealVar* g1Valp = new RooRealVar("g1Valp", "g1Valp", 0);
    RooRealVar* g2Valp = new RooRealVar("g2Valp", "g2Valp", 0.);
    RooRealVar* g3Valp = new RooRealVar("g3Valp", "g3Valp", 0.);
    RooRealVar* g4Valp = new RooRealVar("g4Valp", "g4Valp", 1.);

    RooHWW_5D *myPDFA = new RooHWW_5D("myPDF","myPDF",*m1,*m2,*h1,*h2,*Phi,
				      *a1Valp,*phi1Val,*a2Val,*phi2Val,*a3Valp,*phi3Val,
				      *useGTerm, *g1Valp, *g2Valp, *g3Valp, *g4Valp,
				      *mW,*gamW,*mX,*R1Val,*R2Val);
    
    // Grab input file to convert to RooDataSet
    TFile* fin = new TFile(Form("%sHiggsWW_%.0f_%s.root", dataType.Data(), mH, mode.Data()));
    TTree* tin = (TTree*) fin->Get("angles");
    
    // for weighted events
    if ( mode == "MCFM") {
      RooDataSet dataTMP("dataTMP","dataTMP",tin,RooArgSet(*m1,*m2,*h1,*h2,*Phi,*wt));
      RooDataSet data("data","data",RooArgList(*m1,*m2,*h1,*h2,*Phi,*wt), WeightVar("wt"), Import(dataTMP));
    } else {
      RooDataSet data("data","data",tin,RooArgSet(*m1,*m2,*h1,*h2,*Phi));
    }
    /*
    for (int i=1;i<10;i++) {
      RooArgSet* row = data.get(i);
      row->Print("v");
      std::cout << "weight: " << data.weight() << std::endl;
    }
    */

    // read another input file
    TFile* fin2 = new TFile(Form("PSHiggsWW_%.0f_%s.root", mH, mode.Data()));
    TTree* tin2 = (TTree*) fin2->Get("angles");
    
    // for weighted events
    if ( mode == "MCFM") {
      RooDataSet dataTMP2("dataTMP2","dataTMP2",tin,RooArgSet(*m1,*m2,*h1,*h2,*Phi,*wt));
      RooDataSet data2("data2","data2",RooArgList(*m1,*m2,*h1,*h2,*Phi,*wt), WeightVar("wt"), Import(dataTMP));
    } else {
      RooDataSet data2("data2","data2",tin2,RooArgSet(*m1,*m2,*h1,*h2,*Phi));
    }

    
    // P L O T   . . . 
    // (All parameters fixed, no fitting, just looking at the shape of the PDFs w.r.t. the data)
    TH1F* dum0 = new TH1F("dum0","dum0",1,0,1); dum0->SetLineColor(kRed); dum0->SetMarkerColor(kBlack); dum0->SetLineWidth(3);
    TH1F* dum1 = new TH1F("dum1","dum1",1,0,1); dum1->SetLineColor(kBlue); dum1->SetMarkerColor(kBlack); dum1->SetMarkerStyle(24), dum1->SetLineWidth(3);
    TH1F* dum2 = new TH1F("dum2","dum2",1,0,1); dum2->SetLineColor(kGreen); dum2->SetMarkerColor(kBlack); dum2->SetMarkerStyle(21), dum2->SetLineWidth(3);
    TLegend * box3 = new TLegend(0.1,0.1,0.9,0.92);
    box3->SetFillColor(0);
    box3->SetBorderSize(0);
    box3->AddEntry(dum0,Form("X(%.0f)#rightarrow WW: JP = 0+", mH),"lp");
    box3->AddEntry(dum1,Form("X(%.0f)#rightarrow WW: JP = 0-", mH),"lp");
    box3->AddEntry(dum2,Form("X(%.0f)#rightarrow WW: JP = 0h+", mH),"lp");

    RooPlot* w1frame =  m1->frame(55);
    data.plotOn(w1frame, MarkerColor(kBlack));
    myPDF->plotOn(w1frame, LineColor(kRed));
    data2.plotOn(w1frame, MarkerColor(kBlue), MarkerStyle(24));
    myPDFA->plotOn(w1frame, LineColor(kBlack));
    
    RooPlot* w2frame =  m2->frame(55);
    data.plotOn(w2frame, MarkerColor(kBlack));
    myPDF->plotOn(w2frame, LineColor(kRed));
    data2.plotOn(w2frame, MarkerColor(kBlack), MarkerStyle(24));
    myPDFA->plotOn(w2frame, LineColor(kBlue));
    
    RooPlot* h1frame =  h1->frame(55);
    data.plotOn(h1frame, MarkerColor(kBlack));
    myPDF->plotOn(h1frame, LineColor(kRed));
    data2.plotOn(h1frame, MarkerColor(kBlack), MarkerStyle(24));
    myPDFA->plotOn(h1frame, LineColor(kBlue));
    
    RooPlot* h2frame =  h2->frame(55);
    data.plotOn(h2frame, MarkerColor(kBlack));
    myPDF->plotOn(h2frame, LineColor(kRed));
    data2.plotOn(h2frame, MarkerColor(kBlack), MarkerStyle(24));
    myPDFA->plotOn(h2frame, LineColor(kBlue));
    
    
    RooPlot* Phiframe =  Phi->frame(55);
    data.plotOn(Phiframe, MarkerColor(kBlack));
    myPDF->plotOn(Phiframe, LineColor(kRed));
    data2.plotOn(Phiframe, MarkerColor(kBlack), MarkerStyle(24));
    myPDFA->plotOn(Phiframe, LineColor(kBlue));
    
    TCanvas* cww = new TCanvas( "cww", "cww", 1000, 600 );

    cww->Divide(3,2);
    cww->cd(1);
    w1frame->Draw();
    cww->cd(2);
    w2frame->Draw();
    cww->cd(3);
    box3->Draw();
    cww->cd(4);
    h1frame->Draw();
    cww->cd(5);
    h2frame->Draw();
    cww->cd(6);
    Phiframe->Draw();
    
    cww->Print(Form("epsfiles/angles_HWW%.0f_%s.eps", mH, mode.Data()));
    cww->Print(Form("pngfiles/angles_HWW%.0f_%s.png", mH, mode.Data()));


}
