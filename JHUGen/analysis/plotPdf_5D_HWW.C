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

void plotPdf_5D_HWW(float mH = 125, TString mode="MCFM", TString dataType = "SM"){
    
    gROOT->ProcessLine(".L ~/tdrstyle.C");
    setTDRStyle();
    gStyle->SetPadLeftMargin(0.16);
    
    // Declaration of the PDFs to use
    gROOT->ProcessLine(".L PDFs/RooHWW_5D.cxx++");
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
    RooRealVar* a3Val = new Roo RealVar("a3Val","a3Val",0);
    RooRealVar* phi3Val = new RooRealVar("phi3Val","phi3Val",0);
    // Even more parameters, do not have to touch, based on W couplings
    RooRealVar* R1Val = new RooRealVar("R1Val","R1Val",1);
    RooRealVar* R2Val = new RooRealVar("R2Val","R2Val",-1);
    
    // PDF definition SM Higgs (JP = 0+)
    RooHWW_5D *myPDF = new RooHWW_5D("myPDF","myPDF",*m1,*m2,*h1,*h2,*Phi,*a1Val,*phi1Val,*a2Val,*phi2Val,*a3Val,*phi3Val,*mW,*gamW,*mX,*R1Val,*R2Val);

    // PDF definition Pseudoscalar Higgs (JP = 0-)
    RooRealVar* a1Valp = new RooRealVar("a1Valp","a1Valp",0);
    RooRealVar* a3Valp = new RooRealVar("a3Valp","a3Valp",1);
    RooHWW_5D *myPDFA = new RooHWW_5D("myPDF","myPDF",*m1,*m2,*h1,*h2,*Phi,*a1Valp,*phi1Val,*a2Val,*phi2Val,*a3Valp,*phi3Val,*mW,*gamW,*mX,*R1Val,*R2Val);
    
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

    // P L O T   . . . 
    // (All parameters fixed, no fitting, just looking at the shape of the PDFs w.r.t. the data)
    TH1F* dum0 = new TH1F("dum0","dum0",1,0,1); dum0->SetLineColor(kBlue); dum0->SetLineWidth(3);
    TH1F* dum1 = new TH1F("dum1","dum1",1,0,1); dum1->SetLineColor(kBlue); dum1->SetLineWidth(3);
    TH1F* dum2 = new TH1F("dum2","dum2",1,0,1); dum2->SetLineColor(kRed);  dum2->SetLineWidth(3);
    TLegend * box3 = new TLegend(0.1,0.1,0.9,0.92);
    box3->SetFillColor(0);
    box3->SetBorderSize(0);
    box3->AddEntry(dum1,"5D Model: JP = 0+","l");
    box3->AddEntry(dum2,"5D Model: JP = 0-","l");
    if ( dataType == "SM" )
      box3->AddEntry(dum0, Form("%s JP = 0+", mode.Data()),"p");
    if ( dataType == "PS" )
      box3->AddEntry(dum0, Form("%s JP = 0-", mode.Data()),"p");
    RooPlot* wplusframe =  m1->frame(55);
    data.plotOn(wplusframe);
    myPDF->plotOn(wplusframe);
    myPDFA->plotOn(wplusframe, LineColor(2));
    
    RooPlot* wminusframe =  m2->frame(55);
    data.plotOn(wminusframe);
    myPDF->plotOn(wminusframe);
    myPDFA->plotOn(wminusframe, LineColor(2));
    
    RooPlot* h1frame =  h1->frame(55);
    data.plotOn(h1frame);
    myPDF->plotOn(h1frame);
    myPDFA->plotOn(h1frame, LineColor(2));
    
    RooPlot* h2frame =  h2->frame(55);
    data.plotOn(h2frame);
    myPDF->plotOn(h2frame);
    myPDFA->plotOn(h2frame, LineColor(2));
    
    
    RooPlot* Phiframe =  Phi->frame(55);
    data.plotOn(Phiframe, DataError(RooAbsData::SumW2));
    myPDF->plotOn(Phiframe);
    myPDFA->plotOn(Phiframe, LineColor(2));
    
    TCanvas* cww = new TCanvas( "cww", "cww", 1000, 600 );

    cww->Divide(3,2);
    cww->cd(1);
    wplusframe->Draw();
    cww->cd(2);
    wminusframe->Draw();
    cww->cd(3);
    box3->Draw();
    cww->cd(4);
    h1frame->Draw();
    cww->cd(5);
    h2frame->Draw();
    cww->cd(6);
    Phiframe->Draw();
    
    cww->Print(Form("angles_%sHWW%.0f_%s.eps", dataType.Data(), mH, mode.Data()));
    cww->Print(Form("angles_%sHWW%.0f_%s.png", dataType.Data(), mH, mode.Data()));


}
