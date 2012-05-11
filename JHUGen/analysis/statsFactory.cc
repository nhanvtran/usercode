#include "TFile.h"
#include "TTree.h"
#include "TLeaf.h"
#include <iostream>
#include "TH2F.h"
#include "TH1F.h"
#include "TString.h"
#include "TRint.h"
#include "TChain.h"
#include "TROOT.h"
#include "TStopwatch.h"
#include "TAxis.h"
#include "TCanvas.h"
#include "TPad.h"
#include "TLine.h"
#include "TLegend.h"
#include "TCut.h"
#include "THStack.h"

#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif

#include <vector>
#include <string>
#include <iostream>
#include "RooAbsPdf.h"
#include "RooAddPdf.h"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooFitResult.h"
#include "TRandom.h"
#include "TFile.h"
#include "TTree.h"
#include "TNtuple.h"
#include "TH1F.h"

using namespace std;
using namespace RooFit;

class statsFactory {
    
public:
    
    //Default constructor
    
    statsFactory(RooArgSet* set, RooAbsPdf* pdf1, RooAbsPdf* pdf2, std::string outputFileName="test.root");
    ~statsFactory();
    
    RooArgSet* observables; 
    RooAbsPdf* H0pdf;
    RooAbsPdf* H1pdf;
    RooRealVar* nsig;
    RooRealVar* nbkg;
    RooAddPdf* totalPdf;
    
    TFile* fout;
    
    
    void runSignificance(double nSig, double nBkg, int nToys);
    void runSignificance(double nSig, double nBkg, int nToys,RooDataSet* sigPoolData,RooDataSet* bkgPoolData);
    void runUpperLimit(double nSig, double nBkg, int nToys);
    void runUpperLimit(double nSig, double nBkg, int nToys,RooDataSet* sigPoolData,RooDataSet* bkgPoolData);
    void hypothesisSeparation(double nH0, double nH1, int nToys);
    void hypothesisSeparationWithBackground(double nH0, double nH1, int nToys, RooAbsPdf* bkgpdf, double nBkg);
    void hypothesisSeparationWithBackground(double nH0, double nH1, int nToys, 
                                            RooDataSet* sig0PoolData, RooDataSet* sig1PoolData,
                                            RooAbsPdf* bkgpdf, double nBkg, RooDataSet* bkgPoolData);

    
    double getNUL95( TH1F* histo );
    
    TNtuple* signifTuple;
    TNtuple* signifTuple_em;
    TNtuple* ulTuple;
    TNtuple* ulTuple_em;
    
    TNtuple* hypTuple;
    TNtuple* hypTuple_em_wBkg;
};


// CONSTRUCTOR
statsFactory::statsFactory(RooArgSet* set, RooAbsPdf* pdf1, RooAbsPdf* pdf2, std::string outputFileName){
    
    std::cout << "in the constructor!" << std::endl;
    observables = set;
    H0pdf = pdf1;
    H1pdf = pdf2;
    fout = new TFile( outputFileName.c_str(), "RECREATE");
    
    nsig = new RooRealVar("nsig","number of signal events",0.,1000) ;
    nbkg = new RooRealVar("nbkg","number of background events",0.,20000) ;
    //Construct composite PDF
    totalPdf = new RooAddPdf("totalPdf","totalPdf",RooArgList(*H0pdf,*H1pdf),RooArgList(*nsig,*nbkg));
    
    signifTuple = new TNtuple("signifTuple","signifTuple", "sig:nll0:nll1:nPoiss:nSigFit:nBkgFit"); 
    signifTuple_em = new TNtuple("signifTuple_em","signifTuple_em", "sig:nll0:nll1:nPoiss:nSigFit:nBkgFit"); 
    ulTuple = new TNtuple("ulTuple","ulTuple", "UL:nPoiss"); 
    ulTuple_em = new TNtuple("ulTuple_em","ulTuple_em", "UL:nPoiss"); 
    
    hypTuple = new TNtuple("hypTuple","hypTuple", "S_H0:S_H1:nSigFitH0:nBkgFitH0:nSigPullH0:nBkgPullH0:nSigFitH1:nBkgFitH1:nSigPullH1:nBkgPullH1"); 
    hypTuple_em_wBkg = new TNtuple("hypTuple_em_wBkg","hypTuple_em_wBkg", "S_H0:S_H1"); 

}

// DESTRUCTOR
statsFactory::~statsFactory(){

    fout->cd();

    // write out tuples
    signifTuple->Write();
    signifTuple_em->Write();
    ulTuple->Write();
    hypTuple->Write();
    ulTuple_em->Write();
    hypTuple_em_wBkg->Write();
    fout->Close();
    
}

// ----------------------------------------------------------------------
// ----------------------------------------------------------------------
// ----------------------------------------------------------------------

// SIGNIFICANCE CALCULATION WITH EMBEDDED
void statsFactory::runSignificance(double nSig, double nBkg, int nToys,
                                   RooDataSet* sigPoolData,RooDataSet* bkgPoolData){
    
    //Extended Likelihood Formalism
    double nsignal=nSig;
    double nbackground=nBkg;
    double nPoissSig,nPoissBkg;
    int sigPlaceHolder=0;
    int bkgPlaceHolder=0;
    
    nsig->setVal(nsignal);
    nbkg->setVal(nbackground);
    
    // --- ntuple
    TRandom rng;
    
    // --- histogram
    TH1F* signifHisto = new TH1F("signifHisto","signifHisto",100,0.,20.);
    TH1F* pullHisto = new TH1F("pullHisto","pullHisto",100,-5.,5.);
    
    std::cout << "Performing " << nToys << " toys..." << std::endl;
    for (int i = 0; i < nToys; i++){
        
        nPoissSig = rng.Poisson(nsignal);
        nPoissBkg = rng.Poisson(nbackground);
        nsig->setVal(nsignal);
        nbkg->setVal(nbackground);
        //--------------------------------------------------------------------------------------------
        // generating dataset
        
        RooDataSet* data = new RooDataSet("data","data",*observables);
        RooArgSet *temp;
        for(int iSig=0; iSig<nPoissSig; iSig++){
            
            if(sigPlaceHolder>=sigPoolData->sumEntries()){
	      cout << "Sorry, your sig tree only has " << sigPoolData->sumEntries() << "entries. Bye!" << endl;
                return;
            }else{
                temp = (RooArgSet*)(sigPoolData->get(sigPlaceHolder));
                sigPlaceHolder++;
            }
            
            data->add(*temp);
            
        }
        
        for(int iBkg=0; iBkg<nPoissBkg; iBkg++){
            
            if(bkgPlaceHolder>=bkgPoolData->sumEntries()){
	      cout << "Sorry, your bkg tree only has " << bkgPoolData->sumEntries() << "entries.  Bye!" << endl;
                return;
            }else{
                temp = (RooArgSet*)(bkgPoolData->get(bkgPlaceHolder));
                bkgPlaceHolder++;
            }
            
            data->add(*temp);
            
        }
        
        //--------------------------------------------------------------------------------------------
        
        // fit full float
        nsig->setConstant(kFALSE); nbkg->setConstant(kFALSE);
        RooFitResult* r = totalPdf->fitTo(*data,Extended(kTRUE),Minos(kFALSE),Save(kTRUE),Verbose(kFALSE),PrintLevel(-1));
        /////r->Print();
        double nSigFit = nsig->getVal();
        double nBkgFit = nbkg->getVal();
        
        // fit fix signal to zero
        nsig->setVal(0.000001); nsig->setConstant(kTRUE); nbkg->setConstant(kFALSE);
        RooFitResult* r0 = totalPdf->fitTo(*data,Extended(kTRUE),Minos(kFALSE),Save(kTRUE),Verbose(kFALSE), PrintLevel(-1));
        
        std::cout << "FCN r: " << r->minNll() << std::endl;
        std::cout << "FCN r0: " << r0->minNll() << std::endl;
        
        Double_t significance = sqrt(2*fabs(r->minNll() - r0->minNll()));
        std::cout << "significance: " << significance << std::endl;
        
        double nPoissToy = nPoissSig+nPoissBkg;
        signifTuple_em->Fill( significance,r->minNll(),r0->minNll(), nPoissToy, nSigFit, nBkgFit );
        pullHisto->Fill( (nSigFit-nSig)/nsig->getError() );
        signifHisto->Fill( significance );
        
        delete data;
        delete r;  
        delete r0;  
    }
    
    fout->cd();
    signifHisto->Write("h_significance");
    pullHisto->Write("h_pull");
    delete signifHisto;
    delete pullHisto;
    
}

// SIGNIFICANCE CALCULATION
void statsFactory::runSignificance(double nSig, double nBkg, int nToys){
    
    //Extended Likelihood Formalism
    double nsignal=nSig;
    double nbackground=nBkg;
    double nPoiss;
    
    nsig->setVal(nsignal);
    nbkg->setVal(nbackground);
    
    // --- ntuple
    TRandom rng;
    
    // --- histogram 
    TH1F* signifHisto = new TH1F("signifHisto","signifHisto",100,0.,20.);    
    TH1F* pullHisto = new TH1F("pullHisto","pullHisto",100,-5.,5.);    
    
    std::cout << "Performing " << nToys << " toys..." << std::endl;
    for (int i = 0; i < nToys; i++){
        
        if(i%100==0) cout << "toy number " << i << endl;
        
        nPoiss = rng.Poisson(nsignal+nbackground);
        nsig->setVal(nsignal);
        nbkg->setVal(nbackground);
        //--------------------------------------------------------------------------------------------
        // generating dataset
        RooDataSet* data = totalPdf->generate(*observables, (int) nPoiss);
        
        // fit full float
        nsig->setConstant(kFALSE); nbkg->setConstant(kFALSE);
        RooFitResult* r = totalPdf->fitTo(*data,Extended(kTRUE),Minos(kFALSE),Save(kTRUE),Verbose(kFALSE),PrintLevel(-1));
        /////r->Print();
        double nSigFit = nsig->getVal();
        double nBkgFit = nbkg->getVal();
        
        // fit fix signal to zero
	nsig->setVal(0.000001); nsig->setConstant(kTRUE); nbkg->setConstant(kFALSE);
        RooFitResult* r0 = totalPdf->fitTo(*data,Extended(kTRUE),Minos(kFALSE),Save(kTRUE),Verbose(kFALSE), PrintLevel(-1));
        
        //std::cout << "FCN r: " << r->minNll() << std::endl;
        //std::cout << "FCN r0: " << r0->minNll() << std::endl;
        
        Double_t significance = sqrt(2*fabs(r->minNll() - r0->minNll()));
        std::cout << "significance: " << significance << std::endl;
        pullHisto->Fill( (nSigFit-nSig)/nsig->getError() );
        
        std::cout << significance << ", " << r->minNll() << ", " << r0->minNll() << ", " << nPoiss << ", " << nSigFit << ", " << nBkgFit << std::endl;
        signifTuple->Fill( significance,r->minNll(),r0->minNll(), nPoiss, nSigFit, nBkgFit );
        signifHisto->Fill( significance );
        
        delete data;
        delete r;  
        delete r0;  
    }
    
    fout->cd();
    signifHisto->Write("h_significance");
    pullHisto->Write("h_pull");
    delete signifHisto;
    delete pullHisto;
}

// ----------------------------------------------------------------------
// ----------------------------------------------------------------------
// ----------------------------------------------------------------------
// UPPER LIMIT CALCULATION WITH EMBEDDED
void statsFactory::runUpperLimit(double nSig, double nBkg, int nToys,
                                 RooDataSet* sigPoolData,RooDataSet* bkgPoolData){
    
    // internal parameters
    int iLoopScans = 200;  // number of steps to take to scan in nSig
    double sclFactor = nBkg*.03; // how far w.r.t. the input nBkg to scan in 
    
    
    double nsignal=nSig;
    double nbackground=nBkg;
    double nPoiss;
    int bkgPlaceHolder=0;

    nsig->setVal(nsignal);
    nbkg->setVal(nbackground);
    
    double stepSize = nbackground*sclFactor/( (double) iLoopScans);
    TH1F* ulHisto = new TH1F("ulHisto","ulHisto",100,0,nSig*2);
    TRandom rng;
    
    // start running toys
    for (int i = 0; i < nToys; i++) {
        
        nPoiss = rng.Poisson( 0. + nbackground );  // fix number of signal events to 0
        
        nsig->setVal(0.);
        nbkg->setVal(nbackground);
        
        //--------------------------------------------------------------------------------------------        
        RooDataSet* data = new RooDataSet("data","data",*observables);
        RooArgSet *temp;
        for(int iBkg=0; iBkg<nPoiss; iBkg++){
            
            if(bkgPlaceHolder>=bkgPoolData->sumEntries()){
	      cout << "Sorry, your bkg tree only has " << bkgPoolData->sumEntries() << "entries.  Bye!" << endl;
                return;
            }else{
                temp = (RooArgSet*)(bkgPoolData->get(bkgPlaceHolder));
                bkgPlaceHolder++;
            }
            
            data->add(*temp);
            
        }
        //--------------------------------------------------------------------------------------------   
        
        TH1F* h_chi2Scan = new TH1F( "h_chi2Scan","h_chi2Scan", iLoopScans, 0., nbackground*sclFactor );
        TH1F* h_chi2Scan_reScl = new TH1F( "h_chi2Scan_reScl","h_chi2Scan_reScl", iLoopScans, 0., nbackground*sclFactor );
        TH1F* h_likeliScan_reScl = new TH1F( "h_likeliScan_reScl","h_likeliScan_reScl", iLoopScans, 0., nbackground*sclFactor );
        
        for (int j = 0; j < iLoopScans; j++){
            
            std::cout << "Experiment: " << i << ", Loop: " << j << std::endl;
            
            nsig->setConstant(kTRUE); 
            nbkg->setConstant(kFALSE);
            
            const Double_t vall = (Double_t) j*stepSize+.0001;
            //std::cout << vall << std::endl;
            
            nsig->setVal( vall );
            
            RooFitResult* r = totalPdf->fitTo(*data,Extended(kTRUE),Minos(kTRUE),Save(kTRUE),Verbose(kFALSE), PrintLevel(-1), Warnings(kFALSE), PrintEvalErrors(-1));
            
            // fill histo
            //h_likeliScan->SetBinContent( j+1, likeli );
            h_chi2Scan->SetBinContent( j+1, (r->minNll()) );
	    cout << "minNLL: " << r->minNll() << endl;
            
            delete r; 
            
        }
        
        std::cout << "min Val of chi2 Scan: " << h_chi2Scan->GetMinimum() << std::endl;
        Double_t minR = h_chi2Scan->GetMinimum();
        for (int aa = 1; aa <= iLoopScans; aa++){
            Double_t curR = h_chi2Scan->GetBinContent( aa );
            h_chi2Scan_reScl->SetBinContent( aa, curR - minR ); 
            h_likeliScan_reScl->SetBinContent( aa, exp(minR - curR) );
        }
        
        Double_t nUL = getNUL95( h_likeliScan_reScl );
        ulTuple_em->Fill( nUL, nPoiss );
        ulHisto->Fill( nUL );
        
        delete data;
        delete h_likeliScan_reScl;
        delete h_chi2Scan;
        delete h_chi2Scan_reScl;
    }
    
    fout->cd();
    ulHisto->Write("h_nUL");
    
}

// UPPER LIMIT CALCULATION
void statsFactory::runUpperLimit(double nSig, double nBkg, int nToys){
    
    // internal parameters
    int iLoopScans = 200;  // number of steps to take to scan in nSig
    double sclFactor = nBkg*.03; // how far w.r.t. the input nBkg to scan in 
    
    
    double nsignal=nSig;
    double nbackground=nBkg;
    double nPoiss;
    
    nsig->setVal(nsignal);
    nbkg->setVal(nbackground);
    
    double stepSize = nbackground*sclFactor/( (double) iLoopScans);
    TH1F* ulHisto = new TH1F("ulHisto","ulHisto",100,0,nSig*2);
    TRandom rng;
    
    // start running toys
    for (int i = 0; i < nToys; i++) {
        
        nPoiss = rng.Poisson( 0. + nbackground );  // fix number of signal events to 0
        
        nsig->setVal(0.);
        nbkg->setVal(nbackground);
        RooDataSet* data = totalPdf->generate(*observables, (int) nPoiss) ;
        
        TH1F* h_chi2Scan = new TH1F( "h_chi2Scan","h_chi2Scan", iLoopScans, 0., nbackground*sclFactor );
        TH1F* h_chi2Scan_reScl = new TH1F( "h_chi2Scan_reScl","h_chi2Scan_reScl", iLoopScans, 0., nbackground*sclFactor );
        TH1F* h_likeliScan_reScl = new TH1F( "h_likeliScan_reScl","h_likeliScan_reScl", iLoopScans, 0., nbackground*sclFactor );
        
        for (int j = 0; j < iLoopScans; j++){
            
            std::cout << "Experiment: " << i << ", Loop: " << j << std::endl;
            
            nsig->setConstant(kTRUE); 
            nbkg->setConstant(kFALSE);
            
            const Double_t vall = (Double_t) j*stepSize;
            //std::cout << vall << std::endl;
            
            nsig->setVal( vall );
            
            RooFitResult* r = totalPdf->fitTo(*data,Extended(kTRUE),Minos(kTRUE),Save(kTRUE),Verbose(kFALSE), PrintLevel(-1), Warnings(kFALSE), PrintEvalErrors(-1));
            
            // fill histo
            //h_likeliScan->SetBinContent( j+1, likeli );
            h_chi2Scan->SetBinContent( j+1, (r->minNll()) );
            
            delete r; 
            
        }
        
        std::cout << "min Val of chi2 Scan: " << h_chi2Scan->GetMinimum() << std::endl;
        Double_t minR = h_chi2Scan->GetMinimum();
        for (int aa = 1; aa <= iLoopScans; aa++){
            Double_t curR = h_chi2Scan->GetBinContent( aa );
            h_chi2Scan_reScl->SetBinContent( aa, curR - minR ); 
            h_likeliScan_reScl->SetBinContent( aa, exp(minR - curR) );
        }
        
        Double_t nUL = getNUL95( h_likeliScan_reScl );
        ulTuple->Fill( nUL, nPoiss );
        ulHisto->Fill( nUL );
        
        delete data;
        delete h_likeliScan_reScl;
        delete h_chi2Scan;
        delete h_chi2Scan_reScl;
    }
    
    fout->cd();
    ulHisto->Write("h_nUL");
    
}

// ----------------------------------------------------------------------
// ----------------------------------------------------------------------
// ----------------------------------------------------------------------

// HYPOTHESIS TESTING WITH EMBEDDED BACKGROUND
void statsFactory::hypothesisSeparationWithBackground(double nH0, double nH1, int nToys, 
                                                      RooDataSet* sig0PoolData, RooDataSet* sig1PoolData,
                                                      RooAbsPdf* bkgpdf, double nBkg, RooDataSet* bkgPoolData){
    
    //Extended Likelihood Formalism
    double nPoiss1_sig, nPoiss2_sig;
    double nPoiss1_bkg, nPoiss2_bkg;    
    
    //nsig->setVal(nsignal);
    //nbkg->setVal(nbackground);
    
    // make the composite models
    RooRealVar* nsig0 = new RooRealVar("nsig0","number of signal events", nH0, -1000., nH0*2.0) ;
    RooRealVar* nbkg0 = new RooRealVar("nbkg0","number of background events", nBkg, 0., nBkg*2.0);
    //Construct composite PDF
    RooAddPdf* totalPdf0 = new RooAddPdf("totalPdf0","totalPdf0",RooArgList(*H0pdf,*bkgpdf),RooArgList(*nsig0,*nbkg0));
    // make the composite models
    RooRealVar* nsig1 = new RooRealVar("nsig1","number of signal events", nH1, -1000., nH1*2.0) ;
    RooRealVar* nbkg1 = new RooRealVar("nbkg1","number of background events", nBkg, 0., nBkg*2.0);
    //Construct composite PDF
    RooAddPdf* totalPdf1 = new RooAddPdf("totalPdf1","totalPdf1",RooArgList(*H1pdf,*bkgpdf),RooArgList(*nsig1,*nbkg1));
    
    // --- ntuple
    TRandom rng;
    
    std::cout << "Performing " << nToys << " toys..." << std::endl;
    int sig0PlaceHolder = 0;
    int sig1PlaceHolder = 0;
    int bkgPlaceHolder = 0;
    for (int i = 0; i < nToys; i++){
        
        cout << "toy number " << i << endl;
	cout << "sig0PlaceHolder=" << sig0PlaceHolder << endl;
	cout << "sig1PlaceHolder=" << sig1PlaceHolder << endl;
	cout << "bkgPlaceHolder=" << bkgPlaceHolder << endl;
        
        nPoiss1_sig = rng.Poisson(nH0);
        nPoiss2_sig = rng.Poisson(nH1);
        nPoiss1_bkg = rng.Poisson(nBkg);
        nPoiss2_bkg = rng.Poisson(nBkg);
        
        //--------------------------------------------------------------------------------------------
        // generating dataset
        //RooDataSet* data_H0 = totalPdf0->generate(*observables, (int) nPoiss1);
        //--------------------------------------------------------------------------------------------
        // generating dataset
        RooDataSet* data_H0 = new RooDataSet("data_H0","data_H0",*observables);
        RooArgSet *temp0;
        std::cout << "generating..." << std::endl;
        for(int iSig=0; iSig<nPoiss1_sig; iSig++){
	  if ( iSig%100 == 0 )  
	    std::cout << "generating signal " << iSig << " th event.\n"; 
            
            if(sig0PlaceHolder>=sig0PoolData->sumEntries()){
              cout << "Sorry, your sig0 tree only has " << sig0PoolData->sumEntries() << "entries.  Bye!" << endl;
	      return;
            }else{
                temp0 = (RooArgSet*)(sig0PoolData->get(sig0PlaceHolder));
                sig0PlaceHolder++;
            }
            
            data_H0->add(*temp0);
            
        }
        
        for(int iBkg=0; iBkg<nPoiss1_bkg; iBkg++){

	  if ( iBkg %1000 == 0 )  
	    std::cout << "generating background " << iBkg << " th event.\n"; 
            
            if(bkgPlaceHolder>=bkgPoolData->sumEntries()){
              cout << "Sorry, your bkg tree only has " << bkgPoolData->sumEntries() << "entries.  Bye!" << endl;
	      return;
            }else{
                temp0 = (RooArgSet*)(bkgPoolData->get(bkgPlaceHolder));
                bkgPlaceHolder++;
            }
            
            data_H0->add(*temp0);
            
        }
        //--------------------------------------------------------------------------------------------
        nsig0->setConstant( kFALSE ); nbkg0->setConstant( kFALSE );
        nsig1->setConstant( kFALSE ); nbkg1->setConstant( kFALSE );
        std::cout << "fitting..." << std::endl;
        // fit H0
        RooFitResult* r_H0 = totalPdf0->fitTo(*data_H0,Minos(kFALSE),Save(kTRUE),Verbose(kFALSE),PrintLevel(-1));
        std::cout << "done fitting 0..." << std::endl;
        // fit H1
        RooFitResult* r0_H0 = totalPdf1->fitTo(*data_H0,Minos(kFALSE),Save(kTRUE),Verbose(kFALSE), PrintLevel(-1));
        std::cout << "done fitting 1..." << std::endl;

        //std::cout << "FCN r: " << r->minNll() << std::endl;
        //std::cout << "FCN r0: " << r0->minNll() << std::endl;
        
        double s_estimator_H0 = 2.*(r_H0->minNll() - r0_H0->minNll());
        
        //--------------------------------------------------------------------------------------------
        // generating dataset
        //RooDataSet* data_H1 = totalPdf1->generate(*observables, (int) nPoiss2);
        //--------------------------------------------------------------------------------------------
        // generating dataset
        RooDataSet* data_H1 = new RooDataSet("data_H1","data_H1",*observables);
        RooArgSet *temp1;
        std::cout << "generating..." << std::endl;
        for(int iSig=0; iSig<nPoiss1_sig; iSig++){
            
            if(sig1PlaceHolder>=sig1PoolData->sumEntries()){
              cout << "Sorry, your sig1 tree only has " << sig1PoolData->sumEntries() << "entries.  Bye!" << endl;
	      return;
            }else{
                temp1 = (RooArgSet*)(sig1PoolData->get(sig1PlaceHolder));
                sig1PlaceHolder++;
            }
            
            data_H1->add(*temp1);
            
        }
        
        for(int iBkg=0; iBkg<nPoiss1_bkg; iBkg++){
            
            if(bkgPlaceHolder>=bkgPoolData->sumEntries()){
	      cout << "Sorry, your bkg tree only has " << bkgPoolData->sumEntries() << "entries.  Bye!" << endl;
	      return;
            }else{
                temp1 = (RooArgSet*)(bkgPoolData->get(bkgPlaceHolder));
                bkgPlaceHolder++;
            }
            
            data_H1->add(*temp1);
            
        }
        //--------------------------------------------------------------------------------------------
        nsig0->setConstant( kFALSE ); nbkg0->setConstant( kFALSE );
        nsig1->setConstant( kFALSE ); nbkg1->setConstant( kFALSE );
        // fit H0
        RooFitResult* r_H1 = totalPdf0->fitTo(*data_H1,Minos(kFALSE),Save(kTRUE),Verbose(kFALSE),PrintLevel(-1));
        // fit H1
        RooFitResult* r0_H1 = totalPdf1->fitTo(*data_H1,Minos(kFALSE),Save(kTRUE),Verbose(kFALSE), PrintLevel(-1));
        //std::cout << "FCN r: " << r->minNll() << std::endl;
        //std::cout << "FCN r0: " << r0->minNll() << std::endl;
        
        double s_estimator_H1 = 2.*(r_H1->minNll() - r0_H1->minNll());
        
        std::cout << "s_H0: " << s_estimator_H0 << ", s_H1: " << s_estimator_H1 << std::endl;
        hypTuple_em_wBkg->Fill( s_estimator_H0, s_estimator_H1 );
        
        
        delete data_H0;
        delete data_H1;
        delete r_H0;  
        delete r0_H0;  
        delete r_H1;  
        delete r0_H1;  
        
    }
    
}

// HYPOTHESIS TESTING WITH BACKGROUND based on pure toy
void statsFactory::hypothesisSeparationWithBackground(double nH0, double nH1, int nToys, RooAbsPdf* bkgpdf, double nBkg){
    
    //Extended Likelihood Formalism
    double nPoiss1, nPoiss2;
    
    //nsig->setVal(nsignal);
    //nbkg->setVal(nbackground);
    
    // make the composite models
    RooRealVar* nsig0 = new RooRealVar("nsig0","number of signal events", nH0, -1000., nH0*10.0);
    RooRealVar* nbkg0 = new RooRealVar("nbkg0","number of background events", nBkg, -1000., nBkg*10.0) ;
    //Construct composite PDF
    RooAddPdf* totalPdf0 = new RooAddPdf("totalPdf0","totalPdf0",RooArgList(*H0pdf,*bkgpdf),RooArgList(*nsig0,*nbkg0));
    // make the composite models
    RooRealVar* nsig1 = new RooRealVar("nsig1","number of signal events", nH1, -1000., nH1*10.0) ;
    RooRealVar* nbkg1 = new RooRealVar("nbkg1","number of background events", nBkg, -1000., nBkg*10.0);
    //Construct composite PDF
    RooAddPdf* totalPdf1 = new RooAddPdf("totalPdf1","totalPdf1",RooArgList(*H1pdf,*bkgpdf),RooArgList(*nsig1,*nbkg1));
    
    // --- ntuple
    TRandom rng;
    
    std::cout << "Performing " << nToys << " toys..." << std::endl;
    for (int i = 0; i < nToys; i++){
        cout << "toy number " << i << endl;
      
        nPoiss1 = rng.Poisson(nH0 + nBkg);
        nPoiss2 = rng.Poisson(nH1 + nBkg);
        
        //--------------------------------------------------------------------------------------------
        // generating dataset
        RooDataSet* data_H0 = totalPdf0->generate(*observables, (int) nPoiss1);
        
	// fit H0
        RooFitResult* r_H0 = totalPdf0->fitTo(*data_H0,Minos(kFALSE),Save(kTRUE),Verbose(kFALSE),PrintLevel(-1));
	double nSigFitH0 = nsig0->getVal();
        double nBkgFitH0 = nbkg0->getVal();
	double nSigPullH0 = nsig0->getError() > 0 ? (nsig0->getVal() - nH0) / nsig0->getError() : -999;
	double nBkgPullH0 = nbkg0->getError() > 0 ? (nbkg0->getVal() - nBkg) / nbkg0->getError() : -999;
	// fit H1
        RooFitResult* r0_H0 = totalPdf1->fitTo(*data_H0,Minos(kFALSE),Save(kTRUE),Verbose(kFALSE), PrintLevel(-1));
        double s_estimator_H0 = 2.*(r_H0->minNll() - r0_H0->minNll());
        
        //--------------------------------------------------------------------------------------------
        // generating dataset
        RooDataSet* data_H1 = totalPdf1->generate(*observables, (int) nPoiss2);
        // fit H0
        RooFitResult* r_H1 = totalPdf0->fitTo(*data_H1,Minos(kFALSE),Save(kTRUE),Verbose(kFALSE),PrintLevel(-1));
        // fit H1
        RooFitResult* r0_H1 = totalPdf1->fitTo(*data_H1,Minos(kFALSE),Save(kTRUE),Verbose(kFALSE), PrintLevel(-1));
	double nSigFitH1 = nsig1->getVal();
        double nBkgFitH1 = nbkg1->getVal();
	double nSigPullH1 = nsig0->getError() > 0 ? (nsig1->getVal() - nH1) / nsig1->getError() : -999;
	double nBkgPullH1 = nbkg0->getError() > 0 ? (nbkg1->getVal() - nBkg) / nbkg1->getError() : -999;

        
        double s_estimator_H1 = 2.*(r_H1->minNll() - r0_H1->minNll());
        
        std::cout << "s_H0: " << s_estimator_H0 << ", s_H1: " << s_estimator_H1 << std::endl;
	
        hypTuple->Fill( s_estimator_H0, s_estimator_H1, nSigFitH0, nBkgFitH0, nSigPullH0, nBkgPullH0, nSigFitH1, nBkgFitH1, nSigPullH1, nBkgPullH1 );
        
        
        delete data_H0;
        delete data_H1;
        delete r_H0;  
        delete r0_H0;  
        delete r_H1;  
        delete r0_H1;  
        
    }
    
}


// HYPOTHESIS TESTING
void statsFactory::hypothesisSeparation(double nH0, double nH1, int nToys){
    
    //Extended Likelihood Formalism
    double nH0_val=nH0;
    double nH1_val=nH1;
    double nPoiss1, nPoiss2;
    
    //nsig->setVal(nsignal);
    //nbkg->setVal(nbackground);
    
    // --- ntuple
    TRandom rng;
    
    std::cout << "Performing " << nToys << " toys..." << std::endl;
    for (int i = 0; i < nToys; i++){
        
        cout << "toy number " << i << endl;
        
        nPoiss1 = rng.Poisson(nH0_val);
        nPoiss2 = rng.Poisson(nH1_val);

        //--------------------------------------------------------------------------------------------
        // generating dataset
        RooDataSet* data_H0 = H0pdf->generate(*observables, (int) nPoiss1);
        // fit H0
        RooFitResult* r_H0 = H0pdf->fitTo(*data_H0,Minos(kFALSE),Save(kTRUE),Verbose(kFALSE),PrintLevel(-1));
        // fit H1
        RooFitResult* r0_H0 = H1pdf->fitTo(*data_H0,Minos(kFALSE),Save(kTRUE),Verbose(kFALSE), PrintLevel(-1));
        //std::cout << "FCN r: " << r->minNll() << std::endl;
        //std::cout << "FCN r0: " << r0->minNll() << std::endl;
        
        double s_estimator_H0 = 2.*(r_H0->minNll() - r0_H0->minNll());
        
        //--------------------------------------------------------------------------------------------
        // generating dataset
        RooDataSet* data_H1 = H1pdf->generate(*observables, (int) nPoiss2);
        // fit H0
        RooFitResult* r_H1 = H0pdf->fitTo(*data_H1,Minos(kFALSE),Save(kTRUE),Verbose(kFALSE),PrintLevel(-1));
        // fit H1
        RooFitResult* r0_H1 = H1pdf->fitTo(*data_H1,Minos(kFALSE),Save(kTRUE),Verbose(kFALSE), PrintLevel(-1));
        //std::cout << "FCN r: " << r->minNll() << std::endl;
        //std::cout << "FCN r0: " << r0->minNll() << std::endl;
        
        double s_estimator_H1 = 2.*(r_H1->minNll() - r0_H1->minNll());

        hypTuple->Fill( s_estimator_H0, s_estimator_H1 );

        
        delete data_H0;
        delete data_H1;
        delete r_H0;  
        delete r0_H0;  
        delete r_H1;  
        delete r0_H1;  
        
    }
    
}


// ------------------------------
// ------------------------------
// UTILITIES
double statsFactory::getNUL95( TH1F* histo ){
    
    // first integrate
    Double_t totIntegral = 0;
    for (int i = 1; i <= histo->GetNbinsX(); i++){
        //std::cout << histo->GetBinContent( i ) << std::endl;
        totIntegral += histo->GetBinContent( i );
    }
    //std::cout << "total integral: " << totIntegral << std::endl;
    
    Double_t limit95 = totIntegral*0.95;
    Double_t ctrForLimit = 0;
    Int_t stoppingBin = 0;
    for (int i = 1; i <= histo->GetNbinsX(); i++){
        ctrForLimit += histo->GetBinContent( i );
        if (ctrForLimit >= limit95){
            stoppingBin = i;
            break;
        }
    }
    //std::cout << "ctrForLimit: " << ctrForLimit << ", stopping Bin: " << stoppingBin << std::endl;
    
    return histo->GetBinCenter( stoppingBin );
    
}





