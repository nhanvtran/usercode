#include "RooDataSet.h"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "RooPlot.h"
using namespace RooFit ;

void plotPdf_5D(){
    
    gROOT->ProcessLine(".L ~ntran/tdrstyle.C");
    setTDRStyle();
    gStyle->SetPadLeftMargin(0.16);
    
    // Declaration of the PDFs to use
    //gSystem->Load("../PDFs/RooHZsZs_m1m2_cxx");
    //gSystem->Load("../PDFs/RooAZsZs_m1m2_cxx");
    gSystem->Load("../PDFs/RooXZsZs_5D_cxx");

    // Observables (5D)
    RooRealVar* m1 = new RooRealVar("z1mass","m1",10,120);
    RooRealVar* m2 = new RooRealVar("z2mass","m2",10,120);
    RooRealVar* h1 = new RooRealVar("costheta1","h1",-1,1);
    RooRealVar* h2 = new RooRealVar("costheta2","h2",-1,1);
    RooRealVar* Phi = new RooRealVar("phi","Phi",-TMath::Pi(),TMath::Pi());
    
    
    
    // Parameters
    RooRealVar* mZ = new RooRealVar("mZ","mZ",91.188);
    RooRealVar* mX = new RooRealVar("mX","mX",125.);
    RooRealVar* gamZ = new RooRealVar("gamZ","gamZ",2.5);
    // More parameters, these are the couplings "a1","a2","a3" which are _complex_ (which is why there are phases "phi*Val")
    RooRealVar* a1Val = new RooRealVar("a1Val","a1Val",1);
    RooRealVar* phi1Val = new RooRealVar("phi1Val","phi1Val",0);
    RooRealVar* a2Val = new RooRealVar("a2Val","a2Val",0);
    RooRealVar* phi2Val = new RooRealVar("phi2Val","phi2Val",0);
    RooRealVar* a3Val = new RooRealVar("a3Val","a3Val",0);
    RooRealVar* phi3Val = new RooRealVar("phi3Val","phi3Val",0);
    // Even more parameters, do not have to touch, based on Z couplings
    RooRealVar* R1Val = new RooRealVar("R1Val","R1Val",0.15);
    RooRealVar* R2Val = new RooRealVar("R2Val","R2Val",0.15);
    
    // PDF definition SM Higgs (JP = 0+)
    RooXZsZs_5D *myPDF = new RooXZsZs_5D("myPDF","myPDF",*m1,*m2,*h1,*h2,*Phi,*a1Val,*phi1Val,*a2Val,*phi2Val,*a3Val,*phi3Val,*mZ,*gamZ,*mX,*R1Val,*R2Val);

    // PDF definition Pseudoscalar Higgs (JP = 0-)
    RooRealVar* a1Valp = new RooRealVar("a1Valp","a1Valp",0);
    RooRealVar* a3Valp = new RooRealVar("a3Valp","a3Valp",1);
    RooXZsZs_5D *myPDFA = new RooXZsZs_5D("myPDF","myPDF",*m1,*m2,*h1,*h2,*Phi,*a1Valp,*phi1Val,*a2Val,*phi2Val,*a3Valp,*phi3Val,*mZ,*gamZ,*mX,*R1Val,*R2Val);
    
    // Grab input file to convert to RooDataSet
    TFile* fin = new TFile("SMHiggs_125_JHU.root");
    TTree* tin = (TTree*) fin->Get("angles");
    RooDataSet data("data","data",tin,RooArgSet(*m1,*m2,*h1,*h2,*Phi));
    
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
    box3->AddEntry(dum0,"JHU generator simulation: JP = 0+","p");
    
	RooPlot* z1frame =  m1->frame(55);
    data.plotOn(z1frame);
	myPDF->plotOn(z1frame);
    myPDFA->plotOn(z1frame, LineColor(2));

    RooPlot* z2frame =  m2->frame(55);
    data.plotOn(z2frame);
	myPDF->plotOn(z2frame);
    myPDFA->plotOn(z2frame, LineColor(2));

    RooPlot* h1frame =  h1->frame(55);
    data.plotOn(h1frame);
	myPDF->plotOn(h1frame);
    myPDFA->plotOn(h1frame, LineColor(2));

    RooPlot* h2frame =  h2->frame(55);
    data.plotOn(h2frame);
	myPDF->plotOn(h2frame);
    myPDFA->plotOn(h2frame, LineColor(2));

    RooPlot* Phiframe =  Phi->frame(55);
    data.plotOn(Phiframe);
	myPDF->plotOn(Phiframe);
    myPDFA->plotOn(Phiframe, LineColor(2));

	TCanvas* czz = new TCanvas( "czz", "czz", 1000, 600 );
	czz->Divide(3,2);
    czz->cd(1);
	z1frame->Draw();
    czz->cd(2);
	z2frame->Draw();
    czz->cd(3);
    box3->Draw();
    czz->cd(4);
	h1frame->Draw();
    czz->cd(5);
	h2frame->Draw();
    czz->cd(6);
	Phiframe->Draw();
}