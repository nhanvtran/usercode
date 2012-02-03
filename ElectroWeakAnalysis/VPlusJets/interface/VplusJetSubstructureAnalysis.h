/*****************************************************************************
 * Project: CMS detector at the CERN
 *
 * Package: ElectroWeakAnalysis/VplusJetSubstructure
 *
 *
 * Authors:
 *
 *   Kalanand Mishra, Fermilab - kalanand@fnal.gov
 *
 * Description:
 *   To fill W/Z + jets related quantities into a specified TTree
 *   Can work with CaloJet, GenJet, JPT jet, PF jet.
 *   Can work with jets in RECO/AOD/PAT data formats.
 * History:
 *   
 *
 * Copyright (C) 2010 FNAL 
 *****************************************************************************/

#ifndef VplusJetSubstructureAnalysis_h
#define VplusJetSubstructureAnalysis_h

// system include files
#include <memory>
#include <string>
#include <iostream>
#include <map>
#include <fstream>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h" 

#include "TFile.h"
#include "TTree.h"

#include "ElectroWeakAnalysis/VPlusJets/interface/PATJetTreeFiller.h"
//#include "ElectroWeakAnalysis/VPlusJets/interface/JetTreeFiller.h"
#include "ElectroWeakAnalysis/VPlusJets/interface/VtoElectronTreeFiller.h"
#include "ElectroWeakAnalysis/VPlusJets/interface/VtoMuonTreeFiller.h"
#include "ElectroWeakAnalysis/VPlusJets/interface/MCTreeFiller.h"

//
// class decleration
//
namespace ewk
{
    class VplusJetSubstructureAnalysis : public edm::EDAnalyzer {
    public:
        explicit VplusJetSubstructureAnalysis(const edm::ParameterSet&);
        ~VplusJetSubstructureAnalysis();
        
        virtual void beginJob();
        virtual void analyze(const edm::Event&, const edm::EventSetup& iSetup);
        virtual void endJob() ;
        
        virtual void declareTreeBranches();
        
        
        
    private:
        // ----------member data ---------------------------
        // names of modules, producing object collections
        
        // flags
        bool runningOverMC_;
        bool runoverAOD_;
        
        /// output ROOT file for the tree and histograms
        std::string fOutputFileName_ ;
        TFile*  hOutputFile ;
        TTree*  myTree;

        // V information
        std::string VBosonType_;
        std::string LeptonType_;
        edm::InputTag mInputBoson_;
        // Jet information
        std::vector< std::string > JetCollections_;
        int nJetCollections_;
        std::vector< PATJetTreeFiller* > jetcol;
        // MET information
        edm::InputTag mInputMet_;
        // Rho for pileup
        std::string JetsFor_rho_;
        std::string JetsFor_rho_lepIso_;
        // Primary Vertex        
        edm::InputTag mPrimaryVertex_;
        
        edm::InputTag mInputBeamSpot;
        edm::InputTag mInputgenMet;
        
        /// The objects that actually computes variables and fill the tree 
        std::auto_ptr<ewk::PATJetTreeFiller> PatJetFiller_1;
        std::auto_ptr<ewk::PATJetTreeFiller> PatJetFiller_2;
        std::auto_ptr<ewk::PATJetTreeFiller> PatJetFiller_3;
        //PATJetTreeFiller* PatJetFiller_1;
        //PATJetTreeFiller* PatJetFiller_2;
        //PATJetTreeFiller* PatJetFiller_3;
        /*
        std::auto_ptr<ewk::JetTreeFiller> CaloJetFiller;
        std::auto_ptr<ewk::JetTreeFiller> CorrectedCaloJetFiller;
        std::auto_ptr<ewk::JetTreeFiller> CorrectedPFJetFiller;
        std::auto_ptr<ewk::JetTreeFiller> CorrectedPFJetFillerVBFTag; //For VBF Tag Jets
        std::auto_ptr<ewk::JetTreeFiller> CorrectedJPTJetFiller;
        std::auto_ptr<ewk::JetTreeFiller> GenJetFiller;
        std::auto_ptr<ewk::JetTreeFiller> PFJetFiller; 
        std::auto_ptr<ewk::JetTreeFiller> JPTJetFiller;
         */
        //std::auto_ptr<ewk::VtoElectronTreeFiller> recoBosonFillerE;
        ewk::VtoElectronTreeFiller* recoBosonFillerE;
        //std::auto_ptr<ewk::VtoMuonTreeFiller> recoBosonFillerMu;
        ewk::VtoMuonTreeFiller* recoBosonFillerMu;

        std::auto_ptr<ewk::MCTreeFiller> genBosonFiller;
        
        // private data members
        int run;
        int event; 
        int lumi; 
        int bunch; 
        int nPV; 
        int mNVB;
        float mPVx[30];
        float mPVy[30];
        float mPVz[30];
        float mBSx;
        float mBSy;
        float mBSz;
        float mMET;
        float mSumET;
        float mMETSign;
        float mMETPhi;
        float mtcMET;
        float mtcSumET;
        float mtcMETSign;
        float mtcMETPhi;
        float mpfMET;
        float mpfSumET;
        float mpfMETSign;
        float mpfMETPhi;
        float fastJetRho;
        float lepIsoRho;
        float genMET;
        float genSumET;
        float genMETSign;
        float genMETPhi;
        
        float mcPUtotnvtx;
        float mcPUbx[3];
        float mcPUnvtx[3];
    };
}
#endif
