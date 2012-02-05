/*****************************************************************************
 * Project: CMS detector at the CERN
 *
 * Package: ElectroWeakAnalysis/VPlusJets
 *
 *
 * Authors:
 *
 *   Kalanand Mishra, Fermilab - kalanand@fnal.gov
 *   Anil Singh, Punjab University - anil79@fnal.gov
 *
 * Description:
 *   To fill W--> munu or Z-->mumu  related quantities into a specified TTree
 *   Can work with jets in RECO/AOD/PAT data formats.
 * History:
 *   
 *
 * Copyright (C) 2010 FNAL 
 *****************************************************************************/

// CMS includes
#include "TMath.h" 

// Header file
#include "DataFormats/Candidate/interface/ShallowCloneCandidate.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/METReco/interface/PFMET.h"
#include "DataFormats/METReco/interface/PFMETCollection.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"

#include "ElectroWeakAnalysis/VPlusJets/interface/VtoMuonTreeFiller.h"
#include "ElectroWeakAnalysis/VPlusJets/interface/METzCalculator.h"

ewk::VtoMuonTreeFiller::VtoMuonTreeFiller(const char *name, TTree* tree, 
                                          const edm::ParameterSet iConfig)
{
    
    // ********** Vector boson ********** //
    if( iConfig.existsAs<bool>("runningOverAOD"))
        runoverAOD = iConfig.getParameter<bool>("runningOverAOD");
    if(  iConfig.existsAs<edm::InputTag>("srcVectorBoson") )
        mInputBoson = iConfig.getParameter<edm::InputTag>("srcVectorBoson"); 
    else std::cout << "***Error:" << name << 
        " Collection not specified !" << std::endl;
    
    if(  iConfig.existsAs<edm::InputTag>("srcBeamSpot") )
		mInputBeamSpot  = iConfig.getParameter<edm::InputTag>("srcBeamSpot");
    tree_     = tree;
    name_     = name;
    Vtype_    = iConfig.getParameter<std::string>("VBosonType"); 
    LeptonType_ = iConfig.getParameter<std::string>("LeptonType");
    if(  iConfig.existsAs<edm::InputTag>("srcMet") )
        mInputMet = iConfig.getParameter<edm::InputTag>("srcMet");
    
    
    if( !(tree==0) && LeptonType_=="muon") SetBranches();
    
}





void ewk::VtoMuonTreeFiller::SetBranches()
{
    // Declare jet branches
    std::string lept1 = "muplus";
    std::string lept2 = "muminus";
    if( !(Vtype_=="Z") ) lept1 = "muon";
    
    SetBranch( &V_mass,        "mass");
    SetBranch( &V_mt,        "mt");
    SetBranch( &V_px,        "px");
    SetBranch( &V_py,        "py");
    SetBranch( &V_pz,        "pz");
    SetBranch( &V_E,         "e");
    SetBranch( &V_Pt,        "pt");
    SetBranch( &V_Et,        "et");
    SetBranch( &V_Eta,       "eta");    
    SetBranch( &V_Phi,       "phi");
    SetBranch( &V_Vx,        "vx");
    SetBranch( &V_Vy,        "vy");
    SetBranch( &V_Vz,        "vz");
    SetBranch( &V_Y,         "y");
    if(Vtype_=="W") {
        SetBranch( &V_pzNu1,     "pzNu1");
        SetBranch( &V_pzNu2,     "pzNu2");
    }
    ///////////////////////////////////////////////
    SetBranch( &mu1px,             lept1+"_px" );
    SetBranch( &mu1py,             lept1+"_py" );
    SetBranch( &mu1pz,             lept1+"_pz" );
    SetBranch( &mu1E,              lept1+"_e" );
    SetBranch( &mu1Pt,             lept1+"_pt" );
    SetBranch( &mu1Et,             lept1+"_et" );
    SetBranch( &mu1Eta,            lept1+"_eta" ); 
    SetBranch( &mu1Theta,          lept1+"_theta" ); 
    SetBranch( &mu1Phi,            lept1+"_phi" );
    SetBranch( &mu1Charge,         lept1+"_charge" );
    SetBranch( &mu1Vx,             lept1+"_vx" );
    SetBranch( &mu1Vy,             lept1+"_vy" );
    SetBranch( &mu1Vz,             lept1+"_vz" );
    SetBranch( &mu1Y,              lept1+"_y" );
    SetBranch( &mu1_trackiso,      lept1+"_trackiso" );
    SetBranch( &mu1_hcaliso,       lept1+"_hcaliso" );
    SetBranch( &mu1_ecaliso,       lept1+"_ecaliso" );
    SetBranch( &mu1Type, lept1+"_type" );
    SetBranch( &mu1_numberOfChambers, lept1+"_numberOfChambers" );
    SetBranch( &mu1_numberOfMatches,  lept1+"_numberOfMatches" );	  
    
    SetBranch( &mu1d0bsp,          lept1+"_d0bsp" );
    SetBranch( &mu1dz000,          lept1+"_dz000" );
    
    SetBranch( &mu1pfiso_sumChargedHadronPt,            lept1+"_pfiso_sumChargedHadronPt" );
    SetBranch( &mu1pfiso_sumChargedParticlePt,          lept1+"_pfiso_sumChargedParticlePt" );
    SetBranch( &mu1pfiso_sumNeutralHadronEt,            lept1+"_pfiso_sumNeutralHadronEt" );
    SetBranch( &mu1pfiso_sumPhotonEt,                   lept1+"_pfiso_sumPhotonEt" );
    SetBranch( &mu1pfiso_sumPUPt,                       lept1+"_pfiso_sumPUPt" );
    
    
    ////////////////////////////////////////////////////////
    if(Vtype_=="Z") {	  
        SetBranch( &mu2px,             lept2+"_px" );
        SetBranch( &mu2py,             lept2+"_py" );
        SetBranch( &mu2pz,             lept2+"_pz" );
        SetBranch( &mu2E,              lept2+"_e" );
        SetBranch( &mu2Pt,             lept2+"_pt" );
        SetBranch( &mu2Et,             lept2+"_et" );
        SetBranch( &mu2Eta,            lept2+"_eta" ); 
        SetBranch( &mu2Theta,          lept2+"_theta" );    
        SetBranch( &mu2Phi,            lept2+"_phi" );
        SetBranch( &mu2Charge,         lept2+"_charge" );
        SetBranch( &mu2Vx,             lept2+"_vx" );
        SetBranch( &mu2Vy,             lept2+"_vy" );
        SetBranch( &mu2Vz,             lept2+"_vz" );
        SetBranch( &mu2Y,              lept2+"_y" );
        SetBranch( &mu2_trackiso,      lept2+"_trackiso" );
        SetBranch( &mu2_hcaliso,       lept2+"_hcaliso" );
        SetBranch( &mu2_ecaliso,       lept2+"_ecaliso");
        SetBranch( &mu2Type, lept2+"_type" );
        SetBranch( &mu2_numberOfChambers, lept2+"_numberOfChambers" );
        SetBranch( &mu2_numberOfMatches,  lept2+"_numberOfMatches" );
    }	  
}
/////////////////////////////////////////////////////////////////////////






void ewk::VtoMuonTreeFiller::init()   
{
    // initialize private data members
    V_mass                  = -1.;
    V_mt                  = -1.;
    V_px                  = -99999.;
    V_py                  = -99999.;
    V_pz                  = -99999.;
    V_E                   = -1.;
    V_Pt                  = -1.;
    V_Et                  = -1.;
    V_Eta                 = -10.;
    V_Phi                 = -10.;
    V_Vx                  = -10.;
    V_Vy                  = -10.;
    V_Vz                  = -10.;
    V_Y                   = -10.;
    V_pzNu1               = -10000.0;
    V_pzNu2               = -10000.0;
    
    mu1Type   = -1; 
    mu1Charge           = -10;
    mu2Type  = -1;
    mu2Charge          = -10;
    
    
    mu1px               = -99999.;
    mu1py               = -99999.;
    mu1pz               = -99999.;
    mu1E                = -1.;
    mu1Et               = -1.;
    mu1Pt               = -1.;
    mu1Eta              = -10.;
    mu1Theta            = -99999.;
    mu1Phi              = -10.;
    mu1Vx               = -10.;
    mu1Vy               = -10.;
    mu1Vz               = -10.;
    mu1Y                = -10.;
    mu1_numberOfChambers   = -10.;
    mu1_numberOfMatches    = -1.;
    
    mu1d0bsp            = -99999.;
    mu1dz000            = -99999.;
    
    mu1pfiso_sumChargedHadronPt   = -99999.;
    mu1pfiso_sumChargedParticlePt = -99999.;
    mu1pfiso_sumNeutralHadronEt   = -99999.;
    mu1pfiso_sumPhotonEt          = -99999.;
    mu1pfiso_sumPUPt              = -99999.;
    
    mu2px              = -99999.;
    mu2py              = -99999.;
    mu2pz              = -99999.;
    mu2E               = -1.;
    mu2Pt              = -1.;
    mu2Et              = -1.;
    mu2Eta             = -10.;
    mu2Theta           = -99999.;
    mu2Phi             = -10.;
    mu2Vx              = -10.;
    mu2Vy              = -10.;
    mu2Vz              = -10.;
    mu2Y               = -10.;
    mu2_numberOfChambers   = -10.;
    mu2_numberOfMatches    = -1.;
    //////////////
    mu1_trackiso     = 500.0;
    mu1_hcaliso      = 500.0;
    mu1_ecaliso      = 500.0;
    mu2_trackiso    = 500.0;
    mu2_hcaliso     = 500.0;
    mu2_ecaliso     = 500.0;
    
    // initialization done
}







void ewk::VtoMuonTreeFiller::fill(const edm::Event& iEvent)
{
    
    // protection
    if( (tree_==0) || !(LeptonType_=="muon") )  return;
    
    // first initialize to the default values
    init();
    
    edm::Handle<reco::CandidateView> boson;
    iEvent.getByLabel( mInputBoson, boson);
    if( boson->size()<1 ) return; // Nothing to fill
    
    const reco::Candidate *Vboson = &((*boson)[0]); 
    if( Vboson == 0) return;
    
    // edm::Handle<reco::PFMETCollection> pfmet;
    //iEvent.getByLabel("pfMet", pfmet);
    
    edm::Handle<edm::View<reco::MET> > pfmet;
    iEvent.getByLabel(mInputMet, pfmet);
    ////////// Vector boson quantities //////////////
    V_mass = Vboson->mass();
    V_mt = sqrt(2.0*Vboson->daughter(0)->pt()*Vboson->daughter(1)->pt()*
                (1.0-cos(Vboson->daughter(0)->phi()-Vboson->daughter(1)->phi())));
    V_Eta = Vboson->eta();   
    V_Phi = Vboson->phi();
    V_Vx = Vboson->vx();
    V_Vy = Vboson->vy();
    V_Vz = Vboson->vz();
    V_Y  = Vboson->rapidity();
    V_px = Vboson->px();
    V_py = Vboson->py();
    V_pz = Vboson->pz();
    V_E  = Vboson->energy();
    V_Pt = Vboson->pt();
    V_Et = Vboson->et();
    
    // now iterate over the daughters  
    if(Vboson->numberOfDaughters()<2 ) {
        throw cms::Exception( "***Error: V boson has < 2 daughters !\n");
        return;  // if no muon found, then return
    } 
    
    // get the two daughters
    reco::CandidateBaseRef m0 = Vboson->daughter(0)->masterClone();
    reco::CandidateBaseRef m1 = Vboson->daughter(1)->masterClone();
    
    const reco::Muon * mu1=NULL;
    const reco::Muon * mu2=NULL;
    const std::type_info & type0 = typeid(*m0);
    const std::type_info & type1 = typeid(*m1);
    
    std::cout << "Dynamic casting!!" << std::endl;
    if( type0 == typeid(pat::Muon) ) 
        mu1 = dynamic_cast<const pat::Muon *>( &*m0 ); 
    if( type1 == typeid(pat::Muon) )
        mu2 = dynamic_cast<const pat::Muon *>( &*m1 ); 
    
    if(0==mu1 && 0==mu2) {
        throw cms::Exception("***Error: couldn't do dynamic" 
                             " cast of vector boson daughters !\n");
        return;  // if no muon found, then return
    } 
    
    const reco::Muon * muon1=NULL;
    const reco::Muon * muon2=NULL;
    // if Z--> mu+mu- then muon1 = mu+, muon2 = mu-
    if(Vtype_=="Z") {
        if(mu1->charge() > 0) {  muon1 = mu1;   muon2 = mu2; }
        else { muon1 = mu2;  muon2 = mu1; }
    }
    // if W--> munu then muon1 = mu, muon2 = NULL 
    if(Vtype_=="W") {
        if( abs(mu1->charge())==1 ) muon1  = mu1;
        else if( abs(mu2->charge())==1 ) muon1  = mu2;
        
        if( !(muon1 == NULL) ) {
            // estimate Pz of neutrino
            TLorentzVector p4MET((*pfmet)[0].px(), (*pfmet)[0].py(), (*pfmet)[0].pz(), (*pfmet)[0].energy());
            TLorentzVector p4lepton(muon1->px(), muon1->py(), muon1->pz(), muon1->energy());
            METzCalculator metz;
            metz.SetMET(p4MET);
            metz.SetLepton(p4lepton);
            if (LeptonType_=="electron") metz.SetLeptonType("electron");
            if (LeptonType_=="muon")     metz.SetLeptonType("muon");
            V_pzNu1 = metz.Calculate();
            V_pzNu2 = metz.getOther();
        }
    }
    
    ////////// muon #1 quantities //////////////
    if( !(muon1 == NULL) ) {
        mu1Charge           = muon1-> charge();
        mu1Vx               = muon1->vx();
        mu1Vy               = muon1->vy();
        mu1Vz               = muon1->vz();
        mu1Y                = muon1->rapidity();
        /// isolation 
        mu1_trackiso       = muon1->isolationR03().sumPt;
        mu1_ecaliso        = muon1->isolationR03().emEt;
        mu1_hcaliso        = muon1->isolationR03().hadEt;
        
        mu1Type  = muon1->type();
        mu1_numberOfChambers  = muon1->numberOfChambers();      
        mu1_numberOfMatches   = muon1->numberOfMatches();
        mu1Theta          = muon1->theta();
        mu1Eta            = muon1->eta();    
        mu1Phi            = muon1->phi();
        mu1E              = muon1->energy();
        mu1px             = muon1->px();
        mu1py             = muon1->py();
        mu1pz             = muon1->pz();
        mu1Pt             = muon1->pt();
        mu1Et             = muon1->et();	  
        
        // vertex 
        edm::Handle<reco::BeamSpot>  beamSpot;
        if(runoverAOD){
            iEvent.getByLabel(mInputBeamSpot, beamSpot);
            mu1d0bsp = muon1->innerTrack()->dxy( beamSpot->position() ) ;
            mu1dz000 = muon1->vertex().z();
        }
        // pf isolation
        //mu1pfiso_sumChargedHadronPt   = muon1->pfIsolationR03().sumChargedHadronPt;
        //mu1pfiso_sumChargedParticlePt = muon1->pfIsolationR03().sumChargedParticlePt;
        //mu1pfiso_sumNeutralHadronEt   = muon1->pfIsolationR03().sumNeutralHadronEt;
        //mu1pfiso_sumPhotonEt          = muon1->pfIsolationR03().sumPhotonEt;
        //mu1pfiso_sumPUPt              = muon1->pfIsolationR03().sumPUPt;
    }
    
    ////////// muon #2 quantities //////////////
    if( !(muon2 == NULL) ) {
        mu2Charge          = muon2->charge();
        mu2Vx              = muon2->vx();
        mu2Vy              = muon2->vy();
        mu2Vz              = muon2->vz();
        mu2Y               = muon2->rapidity();
        /// isolation 
        mu2_trackiso       = muon2->isolationR03().sumPt;
        mu2_ecaliso        = muon2->isolationR03().emEt;
        mu2_hcaliso        = muon2->isolationR03().hadEt;
        
        mu2Type  = muon2->type();
        mu2_numberOfChambers = muon2->numberOfChambers();
        mu2_numberOfMatches  = muon2->numberOfMatches();
        mu2Theta          = muon2->theta();
        mu2Eta            = muon2->eta();    
        mu2Phi            = muon2->phi();
        mu2E              = muon2->energy();
        mu2px             = muon2->px();
        mu2py             = muon2->py();
        mu2pz             = muon2->pz();
        mu2Pt             = muon2->pt();
        mu2Et             = muon2->et();	 
    } 
    
}





////////////////// utilities, helpers ///////////////////

void ewk::VtoMuonTreeFiller::SetBranch( float* x, std::string name)
{
    std::string brName = std::string(name_) + "_" + name;
    tree_->Branch( brName.c_str(), x, ( brName+"/F").c_str() );
}


void ewk::VtoMuonTreeFiller::SetBranch( int* x, std::string name)
{
    std::string brName = std::string(name_) + "_" + name;
    tree_->Branch( brName.c_str(), x, ( brName+"/I").c_str() );
}


void ewk::VtoMuonTreeFiller::SetBranch( bool* x, std::string name)
{
    std::string brName = std::string(name_) + "_" + name;
    tree_->Branch( brName.c_str(), x, ( brName+"/O").c_str() );
}

