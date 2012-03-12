/*****************************************************************************
 * Project: CMS detector at the CERN
 *
 * Package: ElectroWeakAnalysis/DiJetSubstructure
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
#include "ElectroWeakAnalysis/VPlusJets/interface/DiJetSubstructureAnalysis.h" 
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

ewk::DiJetSubstructureAnalysis::DiJetSubstructureAnalysis(const edm::ParameterSet& iConfig)
{
    std::cout << "constructor!" << std::endl;
    
    // output file
    fOutputFileName_ = iConfig.getParameter<std::string>("HistOutFile");
    
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
    myTree = new TTree( "DiJetSubstructure","dijets Tree" );    
    
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



ewk::DiJetSubstructureAnalysis::~DiJetSubstructureAnalysis() {}


void ewk::DiJetSubstructureAnalysis::beginJob() {
    // Declare all the branches of the tree
    std::cout << "start begin job" << std::endl;
    declareTreeBranches();
    std::cout << "finish begin job" << std::endl;
}




// ------------ method called to produce the data  ------------
void ewk::DiJetSubstructureAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    
    
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
    
    /*
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
    */
    
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
    
    unsigned int nAllCollections = PatJetCollections_.size() + LiteJetCollections_.size() + GenJetCollections_.size();
    for (unsigned int i = 0; i < nAllCollections; i++){
        //std::cout << "------- i coll: " << i << std::endl; 
        jetcol[i]->fill(iEvent);
    }
    //std::cout << "after..." << std::endl;
    //myTree->Print("V");
    //std::cout << ">>>>>overall fill! event: " << event  << std::endl;
    myTree->Fill();
    
} // analyze method


//  **** Utility: declare TTree branches for ntuple variables ***
void ewk::DiJetSubstructureAnalysis::declareTreeBranches() {
    
    myTree->Branch("event_runNo",  &run,   "event_runNo/I");
    myTree->Branch("event_evtNo",  &event, "event_evtNo/I");
    myTree->Branch("event_lumi",   &lumi,  "event_lumi/I"); 
    myTree->Branch("event_bunch",  &bunch, "event_bunch/I"); 
    myTree->Branch("event_nPV",    &nPV,   "event_nPV/I"); 
    myTree->Branch("event_PVx",    mPVx,   "event_PVx[30]/F"); 
    myTree->Branch("event_PVy",    mPVy,   "event_PVy[30]/F"); 
    myTree->Branch("event_PVz",    mPVz,   "event_PVz[30]/F");

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




void ewk::DiJetSubstructureAnalysis::endJob()
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
using ewk::DiJetSubstructureAnalysis;
DEFINE_FWK_MODULE(DiJetSubstructureAnalysis);
