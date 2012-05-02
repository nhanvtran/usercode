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
 *   To fill jet related quantities into a specified TTree
 *   Can work with CaloJet, GenJet, JPT jet, PF jet.
 *   Can work with jets in RECO/AOD/PAT data formats.
 * History:
 *   
 *
 * Copyright (C) 2010 FNAL 
 *****************************************************************************/


// user include files
#include "ElectroWeakAnalysis/VPlusJets/interface/VplusJetSubstructureAnalysis.h" 
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/METReco/interface/METCollection.h"
#include "DataFormats/METReco/interface/CaloMET.h"
#include "DataFormats/METReco/interface/CaloMETCollection.h"
#include "DataFormats/METReco/interface/PFMET.h"
#include "DataFormats/METReco/interface/PFMETCollection.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "DataFormats/METReco/interface/GenMETCollection.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h" 

#include "DataFormats/PatCandidates/interface/Jet.h"

ewk::VplusJetSubstructureAnalysis::VplusJetSubstructureAnalysis(const edm::ParameterSet& iConfig)
{
    std::cout << "constructor!" << std::endl;
    
    // output file
    fOutputFileName_ = iConfig.getParameter<std::string>("HistOutFile");
    
    // lepton information
    LeptonType_ = iConfig.getParameter<std::string>("LeptonType");
    VBosonType_ = iConfig.getParameter<std::string>("VBosonType");
    //mInputBoson_ = iConfig.getParameter<edm::InputTag>("srcVectorBoson"); 
    
    // jet collections
    PatJetCollections_ = iConfig.getParameter< std::vector<std::string> >("PatJetCollections");
    LiteJetCollections_ = iConfig.getParameter< std::vector<std::string> >("LiteJetCollections");
    GenJetCollections_ = iConfig.getParameter< std::vector<std::string> >("GenJetCollections");
    
    // met information
    mInputMet_ = iConfig.getParameter<edm::InputTag>("srcMet"); 
    
    // pileup information
    JetsFor_rho_ =  iConfig.getParameter<std::string>("srcJetsforRho") ; 
    JetsFor_rho_lepIso_ =  iConfig.getParameter<std::string>("srcJetsforRho_lepIso") ;
    if(  iConfig.existsAs<edm::InputTag>("srcPrimaryVertex") )
        mPrimaryVertex_ = iConfig.getParameter<edm::InputTag>("srcPrimaryVertex"); 
    
    // flags
    if( iConfig.existsAs<bool>("runningOverMC") ) 
        runningOverMC_=iConfig.getParameter< bool >("runningOverMC");
    else runningOverMC_= false;
    
    // declare ntuple
    hOutputFile = new TFile( fOutputFileName_.c_str(), "RECREATE" );
    myTree = new TTree( "VJetSubstructure","V+jets Tree" );
    
    /*
    // boson filler 
    if (LeptonType_ == "electron"){
        recoBosonFillerE = new VtoElectronTreeFiller( VBosonType_.c_str(), myTree, iConfig);
    }
    else if (LeptonType_ == "muon"){
        recoBosonFillerMu = new VtoMuonTreeFiller( VBosonType_.c_str(), myTree, iConfig);
    }
    else {
        std::cout << "Error: invalid lepton type" << std::endl;
    }
    //*/
    
    recoWBosonFillerE = new VtoElectronTreeFiller( "W", "electron", myTree, iConfig);
    recoZBosonFillerE = new VtoElectronTreeFiller( "Z", "electron", myTree, iConfig);
    recoWBosonFillerMu = new VtoMuonTreeFiller( "W", "muon", myTree, iConfig);
    recoZBosonFillerMu = new VtoMuonTreeFiller( "Z", "muon", myTree, iConfig);

    
    
    ////////////////////////////////////
    for (unsigned int i = 0; i < PatJetCollections_.size(); i++){
        std::cout << "collection " << i << ": " << PatJetCollections_[i] << std::endl;
        PATJetTreeFiller* tmp = new PATJetTreeFiller(myTree, PatJetCollections_[i].c_str(), "PatJet", iConfig);
        jetcol.push_back( tmp );
        
    }
    for (unsigned int i = 0; i < LiteJetCollections_.size(); i++){
        std::cout << "collection " << i << ": " << LiteJetCollections_[i] << std::endl;
        PATJetTreeFiller* tmp = new PATJetTreeFiller(myTree, LiteJetCollections_[i].c_str(), "LiteJet", iConfig);
        jetcol.push_back( tmp );
    }
    for (unsigned int i = 0; i < GenJetCollections_.size(); i++){
        std::cout << "collection " << i << ": " << LiteJetCollections_[i] << std::endl;
        PATJetTreeFiller* tmp = new PATJetTreeFiller(myTree, GenJetCollections_[i].c_str(), "GenJet", iConfig);
        jetcol.push_back( tmp );
    }
    ////////////////////////////////////
    
}



ewk::VplusJetSubstructureAnalysis::~VplusJetSubstructureAnalysis() {}


void ewk::VplusJetSubstructureAnalysis::beginJob() {
    // Declare all the branches of the tree
    std::cout << "start begin job" << std::endl;
    declareTreeBranches();
    std::cout << "finish begin job" << std::endl;
}




// ------------ method called to produce the data  ------------
void ewk::VplusJetSubstructureAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    
    
    // write event information
    run   = 0;
    event = 0;
    lumi  = 0;
    bunch = 0;
    nPV   = 0; 
    
    // run, event, bunch crossing, ....
    run   = iEvent.id().run();
    event = iEvent.id().event();
    lumi  = iEvent.luminosityBlock();
    bunch = iEvent.bunchCrossing();
    
    
    // primary/secondary vertices
    // edm::Handle<reco::VertexCollection > recVtxs;
    edm::Handle <edm::View<reco::Vertex> > recVtxs;
    iEvent.getByLabel( mPrimaryVertex_, recVtxs);
    for(unsigned int ind=0;ind<recVtxs->size();ind++) 
    {
        if(nPV>30) continue;
        mPVx[nPV] =   -10000.0;
        mPVy[nPV] =   -10000.0;
        mPVz[nPV] =   -10000.0;
        
        if (!((*recVtxs)[ind].isFake()) && ((*recVtxs)[ind].ndof()>=4) 
            && (fabs((*recVtxs)[ind].z())<=24.0) &&  
            ((*recVtxs)[ind].position().Rho()<=2.0) ) {
            
            mPVx[nPV] =  (*recVtxs)[ind].x() ;
            mPVy[nPV] =  (*recVtxs)[ind].y() ;
            mPVz[nPV] =  (*recVtxs)[ind].z() ;
            nPV += 1;
        }
    }
    
    //////////// Beam spot //////////////
    //  if(runOverAOD){
    edm::Handle<reco::BeamSpot >beamSpot;
    /*
     if(runoverAOD_){
     iEvent.getByLabel(mInputBeamSpot, beamSpot);
     mBSx = beamSpot->position().X();
     mBSy = beamSpot->position().Y();
     mBSz = beamSpot->position().Z();
     }
     */
    
    /////// PfMET information /////
    edm::Handle<edm::View<reco::MET> > pfmet;
    iEvent.getByLabel(mInputMet_, pfmet);
    if (pfmet->size() == 0) {
        mpfMET   = -1;
        mpfSumET = -1;
        mpfMETSign = -1;
        mpfMETPhi   = -10.0;
    }
    else {
        mpfMET   = (*pfmet)[0].et();
        mpfSumET = (*pfmet)[0].sumEt();
        mpfMETSign = (*pfmet)[0].significance();
        mpfMETPhi   = (*pfmet)[0].phi();
    }
    
    ///*
    /////// Pileup density "rho" in the event from fastJet pileup calculation /////
    edm::Handle<double> rho;
    const edm::InputTag eventrho(JetsFor_rho_, "rho");
    iEvent.getByLabel(eventrho,rho);
    if( *rho == *rho) fastJetRho = *rho;
    else  fastJetRho =  -999999.9;
    
    
    
    /////// Pileup density "rho" for lepton isolation subtraction /////
    edm::Handle<double> rhoLepIso;
    const edm::InputTag eventrhoLepIso(JetsFor_rho_lepIso_, "rho");
    iEvent.getByLabel(eventrhoLepIso, rhoLepIso);
    if( *rhoLepIso == *rhoLepIso) lepIsoRho = *rhoLepIso;
    else  lepIsoRho =  -999999.9;
    //*/
    
    //std::cout << "runningOverMC_: " << runningOverMC_ << std::endl;
    if (runningOverMC_){
        /////////// GenMET information & MC Pileup Summary Info  //////////
        mcPUtotnvtx = 0;
        mcPUbx[0]   = -999; mcPUbx[1]   = -999; mcPUbx[2]   = -999;
        mcPUnvtx[0] = -999; mcPUnvtx[1] = -999; mcPUnvtx[2] = -999;
        if ( runningOverMC_ ){
            edm::Handle<reco::GenMETCollection> genMETs;
            /*
             if(runoverAOD_){
             iEvent.getByLabel(mInputgenMet,genMETs);
             if ( genMETs->size() == 0) {
             genMET   = -1.0;
             genSumET = -1.0;
             genMETSign  = -1.0;
             genMETPhi   = -10.0;
             } else {
             genMET = (*genMETs)[0].et();
             genSumET = (*genMETs)[0].sumEt();  
             genMETSign = (*genMETs)[0].significance();  
             genMETPhi = (*genMETs)[0].phi();
             }
             */
        }
        // MC Pileup Summary Info
        const edm::InputTag PileupSrc("addPileupInfo");
        edm::Handle<std::vector< PileupSummaryInfo > >  PupInfo;
        iEvent.getByLabel(PileupSrc, PupInfo);
        std::vector<PileupSummaryInfo>::const_iterator PVI;
        int ctid = 0;
        for(PVI = PupInfo->begin(); PVI != PupInfo->end(); ++PVI) {
            if (ctid>2) break;
            mcPUbx[ctid]   =  PVI->getBunchCrossing();
            mcPUnvtx[ctid] =  PVI->getPU_NumInteractions();
            mcPUtotnvtx   +=  PVI->getPU_NumInteractions();
            ctid++;
        }
    }
    
    // ---------------------------------------------------------
    // V e c t o r   b o s o n   c l a s s i f i c a t i o n   a n d   i d e n t i f i c i a t i o n
    // count total number of candidates and then select good ones based on lepton identification
    ///*
    edm::Handle<edm::View< reco::Candidate> > We_boson;
    iEvent.getByLabel( "WToEnu", We_boson);
    edm::Handle<edm::View< reco::Candidate> > Wm_boson;
    iEvent.getByLabel( "WToMunu", Wm_boson);
    edm::Handle<edm::View< reco::Candidate> > Ze_boson;
    iEvent.getByLabel( "ZToEE", Ze_boson);
    edm::Handle<edm::View< reco::Candidate> > Zm_boson;
    iEvent.getByLabel( "ZToMM", Zm_boson);

    edm::Handle<edm::View<pat::Muon> > muonHandle;
    iEvent.getByLabel("selectedPatMuonsPFlow",muonHandle);
    edm::View<pat::Muon> muons = *muonHandle;
    
    edm::Handle<edm::View<pat::Electron> > electronHandle;
    iEvent.getByLabel("selectedPatElectronsPFlow",electronHandle);
    edm::View<pat::Electron> electrons = *electronHandle;
        
    int n_We = We_boson->size(), n_Wm = Wm_boson->size();
    int n_Ze = Ze_boson->size(), n_Zm = Zm_boson->size();
    int n_e = electrons.size(), n_m = muons.size();
    int nTotCands = n_We + n_Wm + n_Ze + n_Zm; 
    
    
    // can refine selections later...
    if ( nTotCands == 0 ) return;
    else {
        
        //std::cout << "n electrons: " << electrons.size() << std::endl;
        //std::cout << "n muons: " << muons.size() << std::endl;
        
        // numbers of V candidates
        //std::cout << "We_boson size: " << We_boson->size() << std::endl;
        //std::cout << "Wm_boson size: " << Wm_boson->size() << std::endl;
        //std::cout << "Ze_boson size: " << Ze_boson->size() << std::endl;
        //std::cout << "Zm_boson size: " << Zm_boson->size() << std::endl;
                
        if ( nTotCands == 1 ) {
            //std::cout << "hooray!" << std::endl;
            if (n_We == 1) eventClass = 1;   
            if (n_Wm == 1) eventClass = 2;   
            if (n_Ze == 1) eventClass = 3;   
            if (n_Zm == 1) eventClass = 4;   
        }
        else {
            
            if (n_We == 1 && n_e == 1 && n_Wm == 0 && n_m == 0 && n_Ze == 0 && n_Zm == 0){
                std::cout << "this is a W->enu event" << std::endl;
                eventClass = 1;
            }
            else if (n_We == 0 && n_e == 0 && n_Wm == 1 && n_m == 1 && n_Ze == 0 && n_Zm == 0){
                std::cout << "this is a W->munu event" << std::endl;
                eventClass = 2;
            }
            else if (n_We >= 0 && n_e == 2 && n_Wm == 0 && n_m == 0 && n_Ze == 1 && n_Zm == 0){
                std::cout << "this is a Z->ee event" << std::endl;
                eventClass = 3;
            }
            else if (n_We == 0 && n_e == 0 && n_Wm >= 0 && n_m == 2 && n_Ze == 0 && n_Zm == 1){
                std::cout << "this is a Z->mumu event" << std::endl;
                eventClass = 4;
            }
            else{
                std::cout << "throw out this event" << std::endl;
                eventClass = -1;
                return;
            }
        }
        
        recoWBosonFillerE->fill(iEvent, 0);
        recoWBosonFillerMu->fill(iEvent);
        recoZBosonFillerE->fill(iEvent, 0);
        recoZBosonFillerMu->fill(iEvent);

    }
    
    //*/
    
    /*
    // First check if this event has at least 1 V boson
    edm::Handle<edm::View< reco::Candidate> > boson;
    iEvent.getByLabel( mInputBoson_, boson);
    mNVB = boson->size();
    if( mNVB<1 ) return; // Nothing to fill
    
    //  Store reconstructed vector boson information
    if (LeptonType_ == "electron"){
        recoBosonFillerE->fill(iEvent, 0);
        if(mNVB==2) recoBosonFillerE->fill(iEvent, 1);
    }
    else if (LeptonType_ == "muon"){
        std::cout << "fill Muons!" << std::endl;
        recoBosonFillerMu->fill(iEvent);
    }
    else {
        std::cout << "Error: invalid lepton type" << std::endl;
    }
    */
    
    ///*
    //edm::Handle<edm::View<pat::Jet> > jets_CA8PF;
    //iEvent.getByLabel( "goodPatJetsCA8PFlow", jets_CA8PF );
    
    unsigned int nAllCollections = PatJetCollections_.size() + LiteJetCollections_.size() + GenJetCollections_.size();
    for (unsigned int i = 0; i < nAllCollections; i++){
        //std::cout << "------- i coll: " << i << std::endl; 
        jetcol[i]->fill(iEvent);
    }
    //myTree->Print("V");
    myTree->Fill();

    
} // analyze method


//  **** Utility: declare TTree branches for ntuple variables ***
void ewk::VplusJetSubstructureAnalysis::declareTreeBranches() {
    
    myTree->Branch("event_runNo",  &run,   "event_runNo/I");
    myTree->Branch("event_evtNo",  &event, "event_evtNo/I");
    myTree->Branch("event_lumi",   &lumi,  "event_lumi/I"); 
    myTree->Branch("event_bunch",  &bunch, "event_bunch/I"); 
    myTree->Branch("event_nPV",    &nPV,   "event_nPV/I"); 
    myTree->Branch("event_PVx",    mPVx,   "event_PVx[30]/F"); 
    myTree->Branch("event_PVy",    mPVy,   "event_PVy[30]/F"); 
    myTree->Branch("event_PVz",    mPVz,   "event_PVz[30]/F");
    myTree->Branch("eventClass",   &eventClass, "event_Class/I");
    /*
     if(runoverAOD_){
     myTree->Branch("event_met_calomet",    &mMET,  "event_met_calomet/F"); 
     myTree->Branch("event_met_calosumet",  &mSumET,"event_met_calosumet/F"); 
     myTree->Branch("event_met_calometsignificance", &mMETSign,  "event_met_calometsignificance/F"); 
     myTree->Branch("event_met_calometPhi",    &mMETPhi,  "event_met_calometPhi/F"); 
     myTree->Branch("event_met_tcmet",    &mtcMET,  "event_met_tcmet/F"); 
     myTree->Branch("event_met_tcsumet",  &mtcSumET,"event_met_tcsumet/F"); 
     myTree->Branch("event_met_tcmetsignificance", &mtcMETSign,  "event_met_tcmetsignificance/F"); 
     myTree->Branch("event_met_tcmetPhi",    &mtcMETPhi,  "event_met_tcmetPhi/F");
     }
     */
    myTree->Branch("event_met_pfmet",    &mpfMET,  "event_met_pfmet/F"); 
    myTree->Branch("event_met_pfsumet",  &mpfSumET,"event_met_pfsumet/F"); 
    myTree->Branch("event_met_pfmetsignificance", &mpfMETSign,  "event_met_pfmetsignificance/F"); 
    myTree->Branch("event_met_pfmetPhi",    &mpfMETPhi,  "event_met_pfmetPhi/F"); 
    myTree->Branch("event_fastJetRho",      &fastJetRho, "event_fastJetRho/F"); 
    myTree->Branch("event_RhoForLeptonIsolation",  &lepIsoRho, "event_RhoForLeptonIsolation/F");
    
    myTree->Branch("event_BeamSpot_x"       ,&mBSx              ,"event_BeamSpot_x/F");
    myTree->Branch("event_BeamSpot_y"       ,&mBSy              ,"event_BeamSpot_y/F");
    myTree->Branch("event_BeamSpot_z"       ,&mBSz              ,"event_BeamSpot_z/F");
    
    
    myTree->Branch(("num"+VBosonType_).c_str(),&mNVB ,("num"+VBosonType_+"/I").c_str());
    
    if ( runningOverMC_ ){
        
        myTree->Branch("event_met_genmet",    &genMET,  "event_met_genmet/F"); 
        myTree->Branch("event_met_gensumet",  &genSumET,"event_met_gensumet/F"); 
        myTree->Branch("event_met_genmetsignificance", &genMETSign,  "event_met_genmetsignificance/F"); 
        myTree->Branch("event_met_genmetPhi",    &genMETPhi,  "event_met_genmetPhi/F"); 
        
        myTree->Branch("event_mcPU_totnvtx",    &mcPUtotnvtx,  "event_mcPU_totnvtx/F"); 
        myTree->Branch("event_mcPU_bx",         mcPUbx ,       "event_mcPU_bx[3]/F"); 
        myTree->Branch("event_mcPU_nvtx",       mcPUnvtx,      "event_mcPU_nvtx[3]/F"); 
        
    }
    
}  




void ewk::VplusJetSubstructureAnalysis::endJob()
{
    hOutputFile->SetCompressionLevel(2);
    hOutputFile->cd();
    myTree->Write();
    
    delete myTree;
    hOutputFile->Close();
    delete hOutputFile;
}



// declare this class as a plugin
#include "FWCore/PluginManager/interface/ModuleDef.h"
#include "FWCore/Framework/interface/MakerMacros.h"
using ewk::VplusJetSubstructureAnalysis;
DEFINE_FWK_MODULE(VplusJetSubstructureAnalysis);
