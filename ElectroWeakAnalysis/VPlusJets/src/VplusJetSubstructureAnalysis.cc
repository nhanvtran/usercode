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
//fOutputFileName_ ( iConfig.getParameter<std::string>("HistOutFile") ),
//hOutputFile ( new TFile( fOutputFileName_.c_str(), "RECREATE" ) ), 
//myTree ( new TTree("VJetSubstructure","V+jets Tree") ),
//PatJetFiller_1 ( new PATJetTreeFiller("goodPatJetsPFlow", myTree, "goodPatJetsPFlow", 0, iConfig)),
//PatJetFiller_2 ( new PATJetTreeFiller("goodPatJetsCA8PrunedPF", myTree, "goodPatJetsCA8PrunedPF", 1, iConfig)),
//PatJetFiller_3 ( new PATJetTreeFiller("goodPatJetsCA8PF", myTree, "goodPatJetsCA8PF", 2, iConfig))
{
    std::cout << "constructor!" << std::endl;
    // output file
    fOutputFileName_ = iConfig.getParameter<std::string>("HistOutFile");
    // lepton information
    LeptonType_ = iConfig.getParameter<std::string>("LeptonType");
    VBosonType_ = iConfig.getParameter<std::string>("VBosonType");
    mInputBoson_ = iConfig.getParameter<edm::InputTag>("srcVectorBoson"); 
    // jet collections
    JetCollections_ = iConfig.getParameter< std::vector<std::string> >("JetCollections");
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
    if( iConfig.existsAs<bool>("runningOverAOD"))
        runoverAOD_ = iConfig.getParameter<bool>("runningOverAOD");
    // declare ntuple
    hOutputFile = new TFile( fOutputFileName_.c_str(), "RECREATE" );
    myTree = new TTree( "VJetSubstructure","V+jets Tree" );
    
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
    
    // jet filler
    nJetCollections_ = JetCollections_.size();

    //int njc = nJetCollections_;
    //std::vector< PATJetTreeFiller* > jetcol(njc);
    //std::cout << "nJetCollections: " << nJetCollections_ << std::endl;
    //std::vector< PATJetTreeFiller* > jetFillers;
    
    ///*
    //PATJetTreeFiller* tmp;
    for (int i = 0; i < nJetCollections_; i++){
        std::cout << "collection " << i << ": " << JetCollections_[i] << std::endl;
        //PATJetTreeFiller* tmp = new PATJetTreeFiller(JetCollections_[i].c_str(), myTree, JetCollections_[i].c_str(), i, iConfig);
        PATJetTreeFiller* tmp = new PATJetTreeFiller(JetCollections_[i].c_str(), myTree, "PF", i, iConfig);
        jetcol.push_back( tmp );
    
    }
    //*/
    //PatJetFiller_1 = new PATJetTreeFiller(JetCollections_[0].c_str(), myTree, JetCollections_[0].c_str(), 0, iConfig);
    //PatJetFiller_2 = new PATJetTreeFiller(JetCollections_[1].c_str(), myTree, JetCollections_[1].c_str(), 1, iConfig);
    //PatJetFiller_3 = new PATJetTreeFiller(JetCollections_[2].c_str(), myTree, JetCollections_[2].c_str(), 2, iConfig);

    
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
    if(runoverAOD_){
        iEvent.getByLabel(mInputBeamSpot, beamSpot);
        mBSx = beamSpot->position().X();
        mBSy = beamSpot->position().Y();
        mBSz = beamSpot->position().Z();
    }
    
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
    
    
    /////////// GenMET information & MC Pileup Summary Info  //////////
    mcPUtotnvtx = 0;
    mcPUbx[0]   = -999; mcPUbx[1]   = -999; mcPUbx[2]   = -999;
    mcPUnvtx[0] = -999; mcPUnvtx[1] = -999; mcPUnvtx[2] = -999;
    if ( runningOverMC_ ){
        edm::Handle<reco::GenMETCollection> genMETs;
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
    
    // First check if this event has at least 1 V boson
    edm::Handle<edm::View< reco::Candidate> > boson;
    iEvent.getByLabel( mInputBoson_, boson);
    mNVB = boson->size();
    if( mNVB<1 ) return; // Nothing to fill

    /**  Store reconstructed vector boson information */
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
    
    ///*
    edm::Handle<edm::View<pat::Jet> > jets_CA8PF;
    iEvent.getByLabel( "goodPatJetsCA8PFlow", jets_CA8PF );
    
    for (int i = 0; i < nJetCollections_; i++){
        
        jetcol[i]->fill(iEvent);
        
    }
     //*/
    
    //PatJetFiller_1->fill(iEvent);
    //PatJetFiller_2->fill(iEvent);
    //PatJetFiller_3->fill(iEvent);
  
    std::cout << ">>>>>overall fill! event: " << event  << std::endl;
    myTree->Fill();
    /*
    myTree->Print("numgoodPatJetsCA8PFJets*");
    myTree->Print("JetgoodPatJetsCA8PF_Mass*");
    myTree->Print("event_PVx*");
    Float_t o_JetgoodPatJetsCA8PF_Mass[6];
    myTree->SetBranchAddress("JetgoodPatJetsCA8PF_Mass",o_JetgoodPatJetsCA8PF_Mass);
    for (int i = 0; i < myTree->GetEntries(); i++){
        myTree->GetEntry(i);
        for (int k = 0; k < 6; k++){
            std::cout << "ooooooooooo mass " << i << ", " << k << ": " << o_JetgoodPatJetsCA8PF_Mass[k] << std::endl;
        }
    }
     */

    /*
    edm::Handle<edm::View<pat::Jet> > jets_CA8PFPruned;
    iEvent.getByLabel( "goodPatJetsCA8PrunedPF", jets_CA8PFPruned ); 
    for (edm::View< pat::Jet >::const_iterator jetIter = jets_CA8PFPruned->begin(); jetIter != jets_CA8PFPruned->end(); ++jetIter)
    {
        //const reco::BasicJet & fat_jet = c_jets->at(j);
        std::cout << "jets_CA8PFPruned >> number of fat_jet daughters: " << jetIter->numberOfDaughters() << std::endl;
        //std::cout << "is PFJet: " << jetIter
        std::cout << "daughter mass: " << jetIter->daughter(0)->mass() << std::endl;;
    }
    */
    //std::cout << "in the analyze Method!" << std::endl;
    /* Playing around with Jets
    edm::Handle<edm::View<pat::Jet> > jets_AK5PF;
    iEvent.getByLabel( "goodPatJetsPFlow", jets_AK5PF ); 
    
    for (edm::View< pat::Jet >::const_iterator jetIter = jets_AK5PF->begin(); jetIter != jets_AK5PF->end(); ++jetIter)
    {
        //const reco::BasicJet & fat_jet = c_jets->at(j);
        std::cout << "jets_AK5PF >> number of fat_jet daughters: " << jetIter->numberOfDaughters() << std::endl;
        //std::cout << "is PFJet: " << jetIter
    }

    edm::Handle<edm::View<pat::Jet> > jets_CA8PF;
    iEvent.getByLabel( "goodPatJetsCA8PFlow", jets_CA8PF ); 
    
    edm::Handle<edm::View<pat::Jet> > jets_CA8PFPruned;
    iEvent.getByLabel( "goodPatJetsCA8PrunedPF", jets_CA8PFPruned ); 
    for (edm::View< pat::Jet >::const_iterator jetIter = jets_CA8PFPruned->begin(); jetIter != jets_CA8PFPruned->end(); ++jetIter)
    {
        //const reco::BasicJet & fat_jet = c_jets->at(j);
        std::cout << "jets_CA8PFPruned >> number of fat_jet daughters: " << jetIter->numberOfDaughters() << std::endl;
        //std::cout << "is PFJet: " << jetIter
     }
     //*/
    
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
