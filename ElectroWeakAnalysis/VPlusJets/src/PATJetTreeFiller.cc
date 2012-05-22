/*****************************************************************************
 * Project: CMS detector at the CERN
 *
 * Package: ElectroWeakAnalysis/VPlusJets
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

// CMS includes
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/JetReco/interface/CaloJet.h"  
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/METReco/interface/PFMET.h"
#include "DataFormats/METReco/interface/PFMETCollection.h"
#include "TMath.h" 
#include <TLorentzVector.h>
#include "JetMETCorrections/MCJet/plugins/JetUtilMC.h" // needed for dPhi,dR
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

// Monte Carlo stuff
#include "SimDataFormats/JetMatching/interface/JetFlavour.h"
#include "SimDataFormats/JetMatching/interface/JetFlavourMatching.h"
#include "SimDataFormats/JetMatching/interface/MatchedPartons.h"
#include "SimDataFormats/JetMatching/interface/JetMatchedPartons.h"
#include "DataFormats/BTauReco/interface/JetTag.h"
#include "DataFormats/BTauReco/interface/SecondaryVertexTagInfo.h"
#include "DataFormats/BTauReco/interface/TrackIPTagInfo.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

// Header file
#include "ElectroWeakAnalysis/VPlusJets/interface/PATJetTreeFiller.h"
#include "ElectroWeakAnalysis/VPlusJets/interface/METzCalculator.h"
//#include "ElectroWeakAnalysis/VPlusJets/interface/AngularVars.h"
//#include "ElectroWeakAnalysis/VPlusJets/interface/ColorCorrel.h"
#include "ElectroWeakAnalysis/VPlusJets/interface/QGLikelihoodCalculator.h"
#include <algorithm>

ewk::PATJetTreeFiller::PATJetTreeFiller(TTree* tree, const std::string jetCollName,
                                        const std::string jetCollType, const edm::ParameterSet iConfig )
{
    
    
    // jet collections
    //JetCollections_ = iConfig.getParameter< std::vector<std::string> >("JetCollections");
    //mInputJets = JetCollections_[index].c_str();
    
    JetsFor_rho_ = iConfig.getParameter<std::string>("srcJetsforRho");
    
    
    if(  iConfig.existsAs<edm::InputTag>("srcMet") )
        mInputMet = iConfig.getParameter<edm::InputTag>("srcMet");
    
    
    // ********** Vector boson ********** //
    //if(  iConfig.existsAs<edm::InputTag>("srcVectorBoson") )
    //    mInputBoson = iConfig.getParameter<edm::InputTag>("srcVectorBoson"); 
    
    //*********************  bTagger  ***********//
    if( iConfig.existsAs<std::string>("bTagger"))
        bTagger = iConfig.getParameter<std::string>("bTagger");
    
    //  ********** Jet Flavor identification (MC) ********** //
    doJetFlavorIdentification = false;
    if( (iConfig.existsAs<bool>("runningOverMC") && iConfig.getParameter<bool>("runningOverMC") && 
         iConfig.existsAs<edm::InputTag>("srcFlavorByValue") )) {
        sourceByValue = iConfig.getParameter<edm::InputTag> ("srcFlavorByValue");
        doJetFlavorIdentification = true;
    }
    
    //Vtype_    = iConfig.getParameter<std::string>("VBosonType"); 
    //LeptonType_ = iConfig.getParameter<std::string>("LeptonType");
    
    tree_     = tree;
    jetCollName_ = jetCollName;
    jetCollType_ = jetCollType;
    // collection name for output
    if (jetCollType_ == "PatJet"){
        if (jetCollName_ == "goodPatJetsPFlow") jetCollTag_ = "AK5PF";
        else {
            jetCollTag_ = jetCollName_;
            //std::cout << "JetCollTag: " << jetCollTag_ << std::endl;
            jetCollTag_.erase( 0, 11 ); // assumes form "goodPatJetsXXX"
            std::transform(jetCollTag_.begin(), jetCollTag_.end(), jetCollTag_.begin(), ::toupper);        
            //std::cout << "JetCollTag: " << jetCollTag_ << std::endl;
        }
    }
    else if (jetCollType_ == "LiteJet"){
        jetCollTag_ = jetCollName_;
        int findLite = jetCollTag_.find("Lite");
        if (findLite > 0) jetCollTag_.erase( findLite, 4 ); // assumes form "XXXXXXLite"  
        jetCollTag_ += "PF";
        std::transform(jetCollTag_.begin(), jetCollTag_.end(), jetCollTag_.begin(), ::toupper);        
        //std::cout << "JetCollTag: " << jetCollTag_ << std::endl;
        
    }
    else if (jetCollType_ == "GenJet"){
        jetCollTag_ = jetCollName_;
        std::transform(jetCollTag_.begin(), jetCollTag_.end(), jetCollTag_.begin(), ::toupper);        
        //int findLite = jetCollTag_.find("Lite");
        //jetCollTag_.erase( findLite, 4 ); // assumes form "XXXXXXLite"                
    }
    else{
        throw cms::Exception("PatJetTreeFiller") << "unexpected jetCollType type: "<< jetCollType_ ;
    }
    
    
    if( !(tree==0) ) SetBranches();
}


//////////////////////////////////////////////////////////////////
/////// Helper for above function ////////////////////////////////
//////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

void ewk::PATJetTreeFiller::SetBranchSingle( float* x, std::string name)
{
    tree_->Branch( name.c_str(), x, ( name+"/F").c_str() );
    bnames.push_back( name );
}

void ewk::PATJetTreeFiller::SetBranchSingle( int* x, std::string name)
{
    tree_->Branch( name.c_str(), x, ( name+"/I").c_str() );
    bnames.push_back( name );
}


void ewk::PATJetTreeFiller::SetBranch( float* x, std::string name)
{
    tree_->Branch( name.c_str(), x, ( name+"[8]/F").c_str() );
    bnames.push_back( name );
}


void ewk::PATJetTreeFiller::SetBranch( int* x, std::string name)
{
    tree_->Branch( name.c_str(), x, ( name+"[8]/I").c_str() );
    bnames.push_back( name );
}

//////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////







void ewk::PATJetTreeFiller::FillBranches() const 
{
    //std::cout << "(c) NumJets == " << NumJets << std::endl;
    for (int k = 0; k < 6; k++){
        //std::cout << "(c) Mass Jet " << k << " == " << Mass[k] << std::endl;   
    }
    //std::cout << "---------- things are getting filled!!!!" << std::endl;
	
    for(std::vector<std::string>::iterator it = bnames.begin(); it != bnames.end(); ++it) {
        //std::cout << "br: " << (*it) << std::endl;
        /////if(TBranch *br = tree_->GetBranch( (*it).c_str() ) ) br->Fill();
        //if ((*it) == "numgoodPatJetsCA8PFJets") std::cout << "(d) NumJets == " << NumJets << std::endl;
        //if ((*it) == "JetgoodPatJetsCA8PF_Mass") std::cout << "(d) Mass Jet == " << Mass[0] << std::endl;
        
    }
    
}


void ewk::PATJetTreeFiller::fill(const edm::Event& iEvent)
{
    // first initialize to the default values
    init();
    
    //////////////////////////////////////////////
    // N o w   d o   j e t   s t u f f
    //////////////////////////////////////////////
    
    // P A T   J E T S
    if (jetCollType_ == "PatJet"){
        
        edm::Handle<edm::View<pat::Jet> > jets;
        iEvent.getByLabel( jetCollName_.c_str(), jets ); 
        
        NumJets = jets->size(); 
        numBTags = 0;
        size_t iJet = 0;
        edm::View<pat::Jet>::const_iterator jet, endpjets = jets->end(); 
        for (jet = jets->begin();  jet != endpjets;  ++jet, ++iJet) {
            
            if( !(iJet< (unsigned int) NUM_JET_MAX) ) break;
            Et[iJet] = jet->et();
            Pt[iJet] = jet->pt();
            Eta[iJet] = jet->eta();
            Phi[iJet] = jet->phi();
            Theta[iJet] = jet->theta();
            Px[iJet] = jet->px();
            Py[iJet] = jet->py();
            Pz[iJet] = jet->pz();
            E[iJet]  = jet->energy();
            Y[iJet]  = jet->rapidity();
            Mass[iJet] = jet->mass(); 
            Area[iJet] = jet->jetArea();
            JecFactor[iJet] = jet->jecFactor(0);
            nJetDaughters[iJet] = jet->numberOfDaughters();
            
            bDiscriminatorSSVHE[iJet] = jet->bDiscriminator("simpleSecondaryVertexHighEffBJetTags");
            bDiscriminatorTCHE[iJet] = jet->bDiscriminator("trackCountingHighEffBJetTags");
            bDiscriminatorSSVHP[iJet] = jet->bDiscriminator("simpleSecondaryVertexHighPurBJetTags");
            bDiscriminatorTCHP[iJet] = jet->bDiscriminator("trackCountingHighPurBJetTags");
            bDiscriminatorCSV[iJet] = jet->bDiscriminator("combinedSecondaryVertexBJetTags");
            bDiscriminatorJP[iJet] = jet->bDiscriminator("jetProbabilityBJetTags");
            
            if (bDiscriminatorSSVHE[iJet] > 1.74) numBTags++;
            
            // algo specific
            if (jetCollTag_ == "CA8PRUNEDPF"){
                subJet1Mass[iJet] = jet->daughter(0)->mass();
                subJet2Mass[iJet] = jet->daughter(1)->mass();
            }
            if (jetCollTag_ == "CA12FILTEREDPF"){

                edm::Handle<edm::View<reco::Jet> > subjets;
                iEvent.getByLabel( "caFilteredPFlow","SubJets", subjets );
                sjNumJets = subjets->size(); 
                std::cout << "NumSubJets: " << sjNumJets << std::endl;


                edm::View<reco::Jet>::const_iterator subjet, endpjets = subjets->end(); 
                size_t iSubJet = 0;
                for (subjet = subjets->begin();  subjet != endpjets;  ++subjet, ++iSubJet) {
                    if( !(iSubJet< (unsigned int) NUM_JET_MAX) ) break;   
                    sjEt[iJet] = subjet->et();
                    sjPt[iJet] = subjet->pt();
                    sjEta[iJet] = subjet->eta();
                    sjPhi[iJet] = subjet->phi();
                    sjTheta[iJet] = subjet->theta();
                    sjE[iJet]  = subjet->energy();
                    sjMass[iJet] = subjet->mass(); 
//                    sjbDiscriminatorCSV[iJet] = subjet->bDiscriminator("combinedSecondaryVertexBJetTags");
                }
							
//                if (iJet == 0){
//                    for (int kk = 0; kk < nJetDaughters[0]; kk++){
//                        Jet1subjetMass[kk] = jet->daughter(kk)->mass();
//                        Jet1subjetPt[kk] = jet->daughter(kk)->pt();
//                        Jet1subjetPx[kk] = jet->daughter(kk)->pz();
//                        Jet1subjetPy[kk] = jet->daughter(kk)->py();
//                        Jet1subjetPz[kk] = jet->daughter(kk)->pz();
//                        Jet1subjetE[kk] = jet->daughter(kk)->energy();
//                        Jet1subjetBtagCSV[kk] = jet->daughter(kk)->bDiscriminator("combinedSecondaryVertexBJetTags");
//                    }
//                }
//                if (iJet == 1){
//                    for (int kk = 0; kk < nJetDaughters[0]; kk++){
//                        Jet2subjetMass[kk] = jet->daughter(kk)->mass();
//                        Jet2subjetPt[kk] = jet->daughter(kk)->pt();
//                        Jet2subjetPx[kk] = jet->daughter(kk)->pz();
//                        Jet2subjetPy[kk] = jet->daughter(kk)->py();
//                        Jet2subjetPz[kk] = jet->daughter(kk)->pz();
//                        Jet2subjetE[kk] = jet->daughter(kk)->energy();
//                        Jet2subjetBtagCSV[kk] = jet->daughter(kk)->bDiscriminator("combinedSecondaryVertexBJetTags");
//                    }
//                }
							
            }
        }
        
    }
    else if (jetCollType_ == "LiteJet"){
        
        
        std::string px_s = jetCollName_ + "_px";        
        std::string py_s = jetCollName_ + "_py";
        std::string pz_s = jetCollName_ + "_pz";
        std::string e_s = jetCollName_ + "_energy";
        std::string area_s = jetCollName_ + "_jetArea";
        std::string jecFactor_s = jetCollName_ + "_jecFactor";
         
        
        edm::Handle< std::vector< float > > j_px;
        edm::Handle< std::vector< float > > j_py;
        edm::Handle< std::vector< float > > j_pz;
        edm::Handle< std::vector< float > > j_e;
        edm::Handle< std::vector< float > > j_area;
        edm::Handle< std::vector< float > > j_jecFactor;

        iEvent.getByLabel( jetCollName_.c_str(), "px", j_px ); 
        iEvent.getByLabel( jetCollName_.c_str(), "py", j_py ); 
        iEvent.getByLabel( jetCollName_.c_str(), "pz", j_pz ); 
        iEvent.getByLabel( jetCollName_.c_str(), "energy", j_e ); 
        iEvent.getByLabel( jetCollName_.c_str(), "jetArea", j_area ); 
        iEvent.getByLabel( jetCollName_.c_str(), "jecFactor", j_jecFactor ); 

        NumJets = j_px->size(); 

        size_t iJet = 0;
        std::vector< float >::const_iterator jit_px, endpjets = j_px->end(); 
        std::vector< float >::const_iterator jit_py = j_py->begin();
        std::vector< float >::const_iterator jit_pz = j_pz->begin();
        std::vector< float >::const_iterator jit_e = j_e->begin();
        std::vector< float >::const_iterator jit_area = j_area->begin();
        std::vector< float >::const_iterator jit_jecFactor = j_jecFactor->begin();

        for (jit_px = j_px->begin();  jit_px != endpjets;  ++jit_px, ++jit_py, ++jit_pz, ++jit_e, ++jit_area, ++jit_jecFactor, ++iJet) {
            
            if( !(iJet< (unsigned int) NUM_JET_MAX) ) break;
            
            math::XYZTLorentzVector* curJet = new math::XYZTLorentzVector( *jit_px, *jit_py, *jit_pz, *jit_e ); 
            
            Et[iJet] = curJet->Et();
            Pt[iJet] = curJet->Pt();
            Eta[iJet] = curJet->Eta();
            Phi[iJet] = curJet->Phi();
            Theta[iJet] = curJet->Theta();
            Px[iJet] = curJet->Px();
            Py[iJet] = curJet->Py();
            Pz[iJet] = curJet->Pz();
            E[iJet]  = curJet->E();
            Y[iJet]  = curJet->Rapidity();
            Mass[iJet] = curJet->M(); 
            Area[iJet] = *jit_area;
            JecFactor[iJet] = *jit_jecFactor;
            
            //std::cout << "p4: " << curJet->Px() << ", " << curJet->Py() << ", " << curJet->Pz() << ", " << curJet->E() << std::endl;
            
        }
    }
    
    else if (jetCollType_ == "GenJet"){
        
        edm::Handle<edm::View<reco::GenJet> > jets;
        iEvent.getByLabel( jetCollName_.c_str(), jets ); 

        NumJets = jets->size(); 
        numBTags = 0;
        size_t iJet = 0;
        edm::View<reco::GenJet>::const_iterator jet, endpjets = jets->end(); 
        for (jet = jets->begin();  jet != endpjets;  ++jet, ++iJet) {
            
            if( !(iJet< (unsigned int) NUM_JET_MAX) ) break;
            Et[iJet] = jet->et();
            Pt[iJet] = jet->pt();
            Eta[iJet] = jet->eta();
            Phi[iJet] = jet->phi();
            Theta[iJet] = jet->theta();
            Px[iJet] = jet->px();
            Py[iJet] = jet->py();
            Pz[iJet] = jet->pz();
            E[iJet]  = jet->energy();
            Y[iJet]  = jet->rapidity();
            Mass[iJet] = jet->mass(); 
            Area[iJet] = jet->jetArea();
            nJetDaughters[iJet] = jet->numberOfDaughters();
        }
    }
    else{
        throw cms::Exception("PatJetTreeFiller") << "unexpected jetCollType type: "<< jetCollType_ ;
        
    }
    //std::cout << "after fill,.." << std::endl;
    

}

void ewk::PATJetTreeFiller::SetBranches()
{
    
    // There are types of jet collections: PatJet, LiteJet, GenJet
    // kinematics (same for all)
    // Declare jet branches
    SetBranchSingle( &NumJets, "Jet" + jetCollTag_ + "_nJets");
    
    SetBranch( Et, "Jet" + jetCollTag_ + "_Et");
    SetBranch( Pt, "Jet" + jetCollTag_ + "_Pt");
    SetBranch( Eta, "Jet" + jetCollTag_ + "_Eta");
    SetBranch( Phi, "Jet" + jetCollTag_ + "_Phi");
    SetBranch( Theta, "Jet" + jetCollTag_ + "_Theta");
    SetBranch( Px, "Jet" + jetCollTag_ + "_Px");
    SetBranch( Py, "Jet" + jetCollTag_ + "_Py");
    SetBranch( Pz, "Jet" + jetCollTag_ + "_Pz");
    SetBranch( E, "Jet" + jetCollTag_ + "_E");
    SetBranch( Y, "Jet" + jetCollTag_ + "_Y");
    SetBranch( Mass, "Jet" + jetCollTag_ + "_Mass");
    SetBranch( Area, "Jet" + jetCollTag_ + "_Area");
    SetBranch( JecFactor, "Jet" + jetCollTag_ + "_JecFactor");

    
    if (jetCollType_ == "PatJet"){
        SetBranchSingle( &numBTags, "Jet" + jetCollTag_ + "_nJetBTags");
        SetBranch( nJetDaughters, "Jet" + jetCollTag_ + "_nDau");
        
        SetBranch( bDiscriminatorSSVHE, "Jet" + jetCollTag_ + "_bDiscSSVHE");
        SetBranch( bDiscriminatorTCHE, "Jet" + jetCollTag_ + "_bDiscTCHE");
        SetBranch( bDiscriminatorCSV, "Jet" + jetCollTag_ + "_bDiscrCSV");
        SetBranch( bDiscriminatorJP, "Jet" + jetCollTag_ + "_bDiscJP");
        SetBranch( bDiscriminatorSSVHP, "Jet" + jetCollTag_ + "_bDiscrSSVHP");
        SetBranch( bDiscriminatorTCHP, "Jet" + jetCollTag_ + "_bDiscTCHP");
        
        if (jetCollTag_ == "CA8PRUNEDPF"){
            SetBranch( subJet1Mass, "Jet" + jetCollTag_ + "_subJet1Mass");
            SetBranch( subJet2Mass, "Jet" + jetCollTag_ + "_subJet2Mass");
        }
        if (jetCollTag_ == "CA12FILTEREDPF"){
            SetBranchSingle( &sjNumJets, "Jet" + jetCollTag_ + "_sjNumJets");

            SetBranch( sjEt, "Jet" + jetCollTag_ + "_sjEt");
            SetBranch( sjPt, "Jet" + jetCollTag_ + "_sjPt");
            SetBranch( sjEta, "Jet" + jetCollTag_ + "_sjEta");
            SetBranch( sjPhi, "Jet" + jetCollTag_ + "_sjPhi");
            SetBranch( sjTheta, "Jet" + jetCollTag_ + "_sjTheta");
            SetBranch( sjE, "Jet" + jetCollTag_ + "_sjE");
            SetBranch( sjMass, "Jet" + jetCollTag_ + "_sjMass");
          
        }
    }
    
}

void ewk::PATJetTreeFiller::init()   
{
    // initialize private data members
    NumJets = 0; 
    numBTags = 0;
    sjNumJets = 0.;

    for (int j =0; j< NUM_JET_MAX; ++j) {
        Et[j] = -1.0;
        Pt[j] = -1.0;
        Eta[j] = -10.0;
        Phi[j] = -10.0;
        Theta[j] = -10.0;
        Px[j] = -1.0;
        Py[j] = -1.0;
        Pz[j] = -1.0;
        E[j] = -1.0;
        Y[j] = -10.0;
        Mass[j] = -1.0;
        Area[j] = -1.0;
        JecFactor[j] = -1.0;
        nJetDaughters[j] = -1;
        
        bDiscriminatorSSVHE[j] = -1.0;
        bDiscriminatorTCHE[j] = -1.0;
        bDiscriminatorCSV[j] = -1.0;
        bDiscriminatorJP[j] = -1.0;
        bDiscriminatorSSVHP[j] = -1.0;
        bDiscriminatorTCHP[j] = -1.0;
        
        subJet1Mass[j] = -1;
        subJet2Mass[j] = -1;

        sjEt[j] = 0.;
        sjPt[j] = -1.;
        sjEta[j] = -10.;
        sjPhi[j] = -10.;
        sjTheta[j] = -10.;
        sjE[j] = -1.;
        sjMass[j] = -1.;

    }    
    
}
