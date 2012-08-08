//
// WARNING for the paper plots you have to make sure all the inputs have the same number of events, taken as 100K for now
// 


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

void plotPdf_7D_VWW(double mH=125) {
    
    gROOT->ProcessLine(".L tdrstyle.C");
    setTDRStyle();
    TGaxis::SetMaxDigits(3);
    gROOT->ForceStyle();
    

    // Declaration of the PDFs to use
    gROOT->ProcessLine(".L PDFs/RooSpinOne_7D.cxx++");
    
    // W/Z mass and decay width constants
    double mV = 80.399;
    double gamV = 2.085;
    bool offshell = false;
    if ( mH < 2 * mV ) offshell = true;

    // for the pole mass and decay width of W 
    RooRealVar* mX = new RooRealVar("mX","mX", mH);
    RooRealVar* mW = new RooRealVar("mW","mW", mV);
    RooRealVar* gamW = new RooRealVar("gamW","gamW",gamV);

    //
    // Observables (7D)
    // 
    RooRealVar* wplusmass = new RooRealVar("wplusmass","m(W+)",mV,1e-09,120);
    wplusmass->setBins(50);
    RooRealVar* wminusmass = new RooRealVar("wminusmass","m(W-)",mV,1e-09,120);
    wminusmass->setBins(50);
    RooRealVar* hs = new RooRealVar("costhetastar","cos#theta*",-1,1);
    hs->setBins(20);
    RooRealVar* Phi1 = new RooRealVar("phistar1","#Phi_{1}",-TMath::Pi(),TMath::Pi());
    Phi1->setBins(20);
    RooRealVar* h1 = new RooRealVar("costheta1","cos#theta_{1}",-1,1);
    h1->setBins(20);
    RooRealVar* h2 = new RooRealVar("costheta2","cos#theta_{2}",-1,1);
    h2->setBins(20);
    RooRealVar* Phi = new RooRealVar("phi","#Phi",-TMath::Pi(),TMath::Pi());
    Phi->setBins(20);
    
    // 1-
    RooRealVar* g1ValV = new RooRealVar("g1ValV","g1ValV",1.);
    RooRealVar* g2ValV = new RooRealVar("g2ValV","g2ValV",0.);
    // Even more parameters, do not have to touch, based on W couplings
    RooRealVar* R1Val = new RooRealVar("R1Val","R1Val",-1.);
    RooRealVar* R2Val = new RooRealVar("R2Val","R2Val",-1.);
    
    // these are the acceptance terms associated with the production angles
    // the default setting is for setting no-acceptance
    RooRealVar* aParam = new RooRealVar("aParam","aParam",0);
    
    RooSpinOne_7D *myPDFV;

    if ( offshell ) 
      myPDFV = new RooSpinOne_7D("myPDF","myPDF", *mX, *wplusmass, *wminusmass, *h1, *h2, *hs, *Phi, *Phi1, 
				 *g1ValV, *g2ValV, *R1Val, *R2Val, *aParam, *mW, *gamW);
    else 
      myPDFV = new RooSpinOne_7D("myPDF","myPDF", *mX, *mW, *mW, *h1, *h2, *hs, *Phi, *Phi1, 
				*g1ValV, *g2ValV, *R1Val, *R2Val, *aParam, *mW, *gamW);
    
    // Grab input file to convert to RooDataSet
    TFile* finV = new TFile(Form("VWW_%.0f_JHU.root", mH));
    TTree* tinV = (TTree*) finV->Get("angles");
    if ( offshell ) 
      RooDataSet dataV("dataV","dataV",tinV,RooArgSet(*wplusmass, *wminusmass, *h1,*h2, *hs, *Phi, *Phi1));
    else 
      RooDataSet dataV("dataV","dataV",tinV,RooArgSet(*h1,*h2, *hs, *Phi, *Phi1));
    
    for (int i=1;i<1;i++) {
      RooArgSet* row = dataV.get(i);
      row->Print("v");
    }
    

    // 
    // 1+
    // 
    RooRealVar* g1ValA = new RooRealVar("g1ValA","g1ValA",0);
    RooRealVar* g2ValA = new RooRealVar("g2ValA","g2ValA",1);
    RooSpinOne_7D *myPDFA;
    
    if ( offshell ) 
      myPDFA = new RooSpinOne_7D("myPDF","myPDF", *mX, *wplusmass, *wminusmass, *h1, *h2, *hs, *Phi, *Phi1,
				 *g1ValA, *g2ValA, *R1Val, *R2Val, *aParam, *mW, *gamW);
    else 
      myPDFA = new RooSpinOne_7D("myPDF","myPDF", *mX, *mW, *mW, *h1, *h2, *hs, *Phi, *Phi1,
				 *g1ValA, *g2ValA, *R1Val, *R2Val, *aParam, *mW, *gamW);

    TFile* finA = new TFile(Form("AVWW_%.0f_JHU.root", mH));
    TTree* tinA = (TTree*) finA->Get("angles");
    if ( offshell ) 
      RooDataSet dataA("dataA","dataA",tinA,RooArgSet(*wplusmass, *wminusmass, *hs, *h1, *h2, *Phi, *Phi1));
     else 
       RooDataSet dataA("dataA","dataA",tinA,RooArgSet(*h1,*h2, *hs, *Phi, *Phi1));
    //
    // P L O T   . . .  
    // 

    bool drawv = true;
    bool drawa = true;
    bool drawpaper = true;

    double rescale = 1.0;
    if (drawpaper ) 
      rescale = 0.001;


    // for 1-
    TH1F* dum0 = new TH1F("dum0","dum0",1,0,1); dum0->SetLineColor(kRed); dum0->SetMarkerColor(kBlack); dum0->SetLineWidth(3);
    // for 1+
    TH1F* dum1 = new TH1F("dum1","dum1",1,0,1); dum1->SetLineColor(kBlue); dum1->SetMarkerColor(kBlack); dum1->SetMarkerStyle(24), dum1->SetLineWidth(3);
    TLegend * box3 = new TLegend(0.1,0.1,0.9,0.92);
    box3->SetFillColor(0);
    box3->SetBorderSize(0);
    if ( drawa ) 
      box3->AddEntry(dum0,"X#rightarrow WW JP = 1+","lp");
    if ( drawv )
    box3->AddEntry(dum1,"X#rightarrow WW JP = 1-","lp");

    // 
    //  h1
    // 
    RooPlot* h1frame =  h1->frame(20);
    h1frame->GetXaxis()->CenterTitle();
    h1frame->GetYaxis()->CenterTitle();
    h1frame->GetYaxis()->SetTitle(" ");

    double ymax_h1;
    TH1F *h1a = new TH1F("h1a", "h1a", 20, -1, 1);
    tinA->Project("h1a", "costheta1");
    ymax_h1 = h1a->GetMaximum();

    TH1F *h1_minus = new TH1F("h1_minus", "h1_minus", 20, -1, 1);
    tinV->Project("h1_minus", "costheta1");
    ymax_h1 = h1_minus->GetMaximum() > ymax_h1 ? h1_minus->GetMaximum() : ymax_h1;
    
    if ( drawa ) {
      dataA.plotOn(h1frame, MarkerColor(kRed),MarkerStyle(4),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
      myPDFA->plotOn(h1frame, LineColor(kRed),LineWidth(2), Normalization(rescale));
    }
    if ( drawv ) {
      //dataV.plotOn(h1frame, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
      //myPDFV->plotOn(h1frame, LineColor(kBlue),LineWidth(2), Normalization(rescale));
      // tempoary
      dataV.plotOn(h1frame, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale*.95823), DataError(RooAbsData::None));
      myPDFV->plotOn(h1frame, LineColor(kBlue),LineWidth(2), Normalization(rescale*.95823));
    }
    if ( rescale != 1.)
      h1frame->GetYaxis()->SetRangeUser(0, ymax_h1 / 1000. * 1.3);

    
    // 
    //  h2
    // 
    
    RooPlot* h2frame =  h2->frame(20);
    h2frame->GetXaxis()->CenterTitle();
    h2frame->GetYaxis()->CenterTitle();
    h2frame->GetYaxis()->SetTitle(" ");

    double ymax_h2;
    TH1F *h2a = new TH1F("h2a", "h2a", 20, -1, 1);
    tinA->Project("h2a", "costheta2");
    ymax_h2 = h2a->GetMaximum();

    TH1F *h2_minus = new TH1F("h2_minus", "h2_minus", 20, -1, 1);
    tinV->Project("h2_minus", "costheta2");
    ymax_h2 = h2_minus->GetMaximum() > ymax_h2 ? h2_minus->GetMaximum() : ymax_h2;

    if ( drawa ) {
      dataA.plotOn(h2frame, MarkerColor(kRed),MarkerStyle(4),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
      myPDFA->plotOn(h2frame, LineColor(kRed),LineWidth(2), Normalization(rescale));
    }
    if ( drawv ) {
      // dataV.plotOn(h2frame, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale), yDataError(RooAbsData::None));
      // myPDFV->plotOn(h2frame, LineColor(kBlue),LineWidth(2), Normalization(rescale));
      dataV.plotOn(h2frame, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale*.95823), DataError(RooAbsData::None));
      myPDFV->plotOn(h2frame, LineColor(kBlue),LineWidth(2), Normalization(rescale*.95823));
    }
    if ( rescale != 1.) 
      h2frame->GetYaxis()->SetRangeUser(0, ymax_h2 / 1000. * 1.3);

    //
    // Phi
    // 
    RooPlot* Phiframe =  Phi->frame(20);
    Phiframe->GetXaxis()->CenterTitle();
    Phiframe->GetYaxis()->CenterTitle();
    Phiframe->GetYaxis()->SetTitle(" ");

    double ymax_Phi;
    TH1F *Phia = new TH1F("Phia", "Phia", 20,  -TMath::Pi(), TMath::Pi());
    tinA->Project("Phia", "phi");
    ymax_Phi = Phia->GetMaximum();

    TH1F *Phi_minus = new TH1F("Phi_minus", "Phi_minus", 20,  -TMath::Pi(), TMath::Pi());
    tinV->Project("Phi_minus", "phi");
    ymax_Phi = Phi_minus->GetMaximum() > ymax_Phi ? Phi_minus->GetMaximum() : ymax_Phi;
    
    if ( drawa ) {
      dataA.plotOn(Phiframe, MarkerColor(kRed),MarkerStyle(4),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
      myPDFA->plotOn(Phiframe, LineColor(kRed),LineWidth(2), Normalization(rescale));
    }
    if ( drawv ) {
      //dataV.plotOn(Phiframe, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
      //myPDFV->plotOn(Phiframe, LineColor(kBlue),LineWidth(2), Normalization(rescale));
      dataV.plotOn(Phiframe, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale*.95823), DataError(RooAbsData::None));
      myPDFV->plotOn(Phiframe, LineColor(kBlue),LineWidth(2), Normalization(rescale*.95823));
    }
    if ( rescale != 1. ) 
      Phiframe->GetYaxis()->SetRangeUser(0, ymax_Phi / 1000. * 1.3);
    
    // 
    //  hs 
    // 
    RooPlot* hsframe =  hs->frame(20);

    hsframe->GetXaxis()->CenterTitle();
    hsframe->GetYaxis()->CenterTitle();
    hsframe->GetYaxis()->SetTitle(" ");

    double ymax_hs;
    TH1F *hsa = new TH1F("hsa", "hsa", 20, -1, 1);
    tinA->Project("hsa", "costhetastar");
    ymax_hs = hsa->GetMaximum();

    TH1F *hs_minus = new TH1F("hs_minus", "hs_minus", 20, -1, 1);
    tinV->Project("hs_minus", "costhetastar");
    ymax_hs = hs_minus->GetMaximum() > ymax_hs ? hs_minus->GetMaximum() : ymax_hs;
    
    if ( drawa ) {
      dataA.plotOn(hsframe, MarkerColor(kRed),MarkerStyle(4),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
      myPDFA->plotOn(hsframe, LineColor(kRed),LineWidth(2), Normalization(rescale));
    }
    if ( drawv ) {
      //dataV.plotOn(hsframe, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
      //myPDFV->plotOn(hsframe, LineColor(kBlue),LineWidth(2), Normalization(rescale));
      dataV.plotOn(hsframe, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale*.95823), DataError(RooAbsData::None));
      myPDFV->plotOn(hsframe, LineColor(kBlue),LineWidth(2), Normalization(rescale*.95823));
    }
    if ( rescale != 1. ) 
      hsframe->GetYaxis()->SetRangeUser(0, ymax_hs / 1000. * 1.3);

    
    //
    // Phi1
    // 
    RooPlot* Phi1frame =  Phi1->frame(20);
 
    Phi1frame->GetXaxis()->CenterTitle();
    Phi1frame->GetYaxis()->CenterTitle();
    Phi1frame->GetYaxis()->SetTitle(" ");

    double ymax_Phi1;
    TH1F *Phi1a = new TH1F("Phi1a", "Phi1a", 20, -TMath::Pi(), TMath::Pi());
    tinA->Project("Phi1a", "phistar1");
    ymax_Phi1 = Phi1a->GetMaximum();

    TH1F *Phi1_minus = new TH1F("Phi1_minus", "Phi1_minus", 20, -TMath::Pi(), TMath::Pi());
    tinV->Project("Phi1_minus", "phistar1");
    ymax_Phi1 = Phi1_minus->GetMaximum() > ymax_Phi1 ? Phi1_minus->GetMaximum() : ymax_Phi1;
    
    if ( drawa ) {
      dataA.plotOn(Phi1frame, MarkerColor(kRed),MarkerStyle(4),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
      myPDFA->plotOn(Phi1frame, LineColor(kRed),LineWidth(2), Normalization(rescale));
    }
    if ( drawv ) {
      // dataV.plotOn(Phi1frame, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
      // myPDFV->plotOn(Phi1frame, LineColor(kBlue),LineWidth(2), Normalization(rescale));
      dataV.plotOn(Phi1frame, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale*.95823), DataError(RooAbsData::None));
      myPDFV->plotOn(Phi1frame, LineColor(kBlue),LineWidth(2), Normalization(rescale*.95823));
    }
    if ( rescale != 1. ) 
      Phi1frame->GetYaxis()->SetRangeUser(0, ymax_Phi1 / 1000. * 1.3);


    if ( offshell ) {
      RooPlot* w1frame =  wplusmass->frame(50);
      w1frame->GetXaxis()->CenterTitle();
      w1frame->GetYaxis()->CenterTitle();
      w1frame->GetYaxis()->SetTitle(" ");
      
      double ymax_w1;
      TH1F *w1a = new TH1F("w1a", "w1a", 50, 1e-09, 120);
      tinA->Project("w1a", "wplusmass");
      ymax_w1 = w1a->GetMaximum();
      
      TH1F *w1_minus = new TH1F("w1_minus", "w1_minus", 50, 1e-09, 120);
      tinV->Project("w1_minus", "wplusmass")
      ymax_w1 = w1_minus->GetMaximum() > ymax_w1 ? w1_minus->GetMaximum() : ymax_w1;
      
      if ( drawa ) {
	dataA.plotOn(w1frame, MarkerColor(kRed),MarkerStyle(4),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
	myPDFA->plotOn(w1frame, LineColor(kRed),LineWidth(2), Normalization(rescale));
      }
      if ( drawv ) {
	// dataV.plotOn(w1frame, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
	// myPDFV->plotOn(w1frame, LineColor(kBlue),LineWidth(2), Normalization(rescale));
	dataV.plotOn(w1frame, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale*.95823), DataError(RooAbsData::None));
	myPDFV->plotOn(w1frame, LineColor(kBlue),LineWidth(2), Normalization(rescale*.95823));
      }
      if ( rescale != 1. )
      w1frame->GetYaxis()->SetRangeUser(0, ymax_w1 / 1000. * 1.5);

      // 
      //  wminus
      // 
      RooPlot* w2frame =  wminusmass->frame(50);

      w2frame->GetXaxis()->CenterTitle();
      w2frame->GetYaxis()->CenterTitle();
      w2frame->GetYaxis()->SetTitle(" ");
      
      double ymax_w2;
      TH1F *w2a = new TH1F("w2a", "w2a", 50, 1e-09, 120);
      tinA->Project("w2a", "wminusmass");
      ymax_w2 = w2a->GetMaximum();
      
      TH1F *w2_minus = new TH1F("w2_minus", "w2_minus", 50, 1e-09, 120);
      tinV->Project("w2_minus", "wminusmass")
      ymax_w2 = w2_minus->GetMaximum() > ymax_w2 ? w2_minus->GetMaximum() : ymax_w2;
      
      if ( drawa ) {
	dataA.plotOn(w2frame, MarkerColor(kRed),MarkerStyle(4),MarkerSize(1.5),LineWidth(0),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
	myPDFA->plotOn(w2frame, LineColor(kRed),LineWidth(2), Normalization(rescale));
      }
      if ( drawv ) {
	//dataV.plotOn(w2frame, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale), DataError(RooAbsData::None));
	//myPDFV->plotOn(w2frame, LineColor(kBlue),LineWidth(2), Normalization(rescale));
	dataV.plotOn(w2frame, MarkerColor(kBlue),MarkerStyle(27),MarkerSize(1.9),XErrorSize(0), Rescale(rescale*.95823), DataError(RooAbsData::None));
	myPDFV->plotOn(w2frame, LineColor(kBlue),LineWidth(2), Normalization(rescale*.95823));
      }
      if ( rescale != 1. ) 
	w2frame->GetYaxis()->SetRangeUser(0, ymax_w2 / 1000. * 1.5);
    }
    if ( drawpaper ) {
      TCanvas* can =new TCanvas("can","can",600,600);

      if ( offshell ) {
	w1frame->GetXaxis()->SetTitle("m_{l#nu} [GeV]");
	w1frame->Draw();
	can->Print(Form("paperplots/wplusmass_%.0fGeV_spin1_2in1_ww.eps", mH));
	can->SaveAs(Form("paperplots/wplusmass_%.0fGeV_spin1_2in1_ww.C", mH));
      }
      
      can->Clear();
      hsframe->Draw();
      can->Print(Form("paperplots/costhetastar_%.0fGeV_spin1_2in1_ww.eps", mH));      
      can->SaveAs(Form("paperplots/costhetastar_%.0fGeV_spin1_2in1_ww.C", mH));      
      
      can->Clear();
      Phi1frame->Draw();
      can->Print(Form("paperplots/phistar1_%.0fGeV_spin1_2in1_ww.eps", mH));      
      can->SaveAs(Form("paperplots/phistar1_%.0fGeV_spin1_2in1_ww.C", mH));      

      can->Clear();
      h1frame->GetXaxis()->SetTitle("cos#theta_{1} or cos#theta_{2}");
      h1frame->Draw();
      can->Print(Form("paperplots/costheta1_%.0fGeV_spin1_2in1_ww.eps", mH));
      can->SaveAs(Form("paperplots/costheta1_%.0fGeV_spin1_2in1_ww.C", mH));

      can->Clear();
      Phiframe->Draw();
      can->Print(Form("paperplots/phi_%.0fGeV_spin1_2in1_ww.eps", mH));      
      can->SaveAs(Form("paperplots/phi_%.0fGeV_spin1_2in1_ww.C", mH));      


    }

    else {
      
      TCanvas* cww = new TCanvas( "cww", "cww", 1000, 600 );
      cww->Divide(4,2);
      if ( offshell ) {
	cww->cd(1);
	w1frame->Draw();
	cww->cd(2);
	w2frame->Draw();
      }
      cww->cd(3);
      hsframe->Draw();
      cww->cd(4);
      box3->Draw();
      cww->cd(5);
      Phi1frame->Draw();
      cww->cd(6);
      h1frame->Draw();
      cww->cd(7);
      h2frame->Draw();
      cww->cd(8);
      Phiframe->Draw();
      
      cww->Print(Form("epsfiles/angles_VWW%.0f_JHU_7D.eps", mH));
      cww->Print(Form("pngfiles/angles_VWW%.0f_JHU_7D.png", mH));
      delete cww;
    }

}
