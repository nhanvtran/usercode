//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Wed Jan 18 15:53:46 2012 by ROOT version 5.27/06b
// from TTree VJetSubstructure/V+jets Tree
// found on file: outputCrab_WW_full.root
//////////////////////////////////////////////////////////

#ifndef vJetSubstructure_h
#define vJetSubstructure_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

class vJetSubstructure {
    public :
    TTree          *fChain;   //!pointer to the analyzed TTree or TChain
    Int_t           fCurrent; //!current Tree number in a TChain
    
    // Declaration of leaf types
    Float_t         W_mass;
    Float_t         W_mt;
    Float_t         W_px;
    Float_t         W_py;
    Float_t         W_pz;
    Float_t         W_e;
    Float_t         W_pt;
    Float_t         W_et;
    Float_t         W_eta;
    Float_t         W_phi;
    Float_t         W_vx;
    Float_t         W_vy;
    Float_t         W_vz;
    Float_t         W_y;
    Int_t           W_numTightElectrons;
    Int_t           W_numLooseElectrons;
    Float_t         W_pzNu1;
    Float_t         W_pzNu2;
    Float_t         W_electron_px;
    Float_t         W_electron_py;
    Float_t         W_electron_pz;
    Float_t         W_electron_e;
    Float_t         W_electron_pt;
    Float_t         W_electron_et;
    Float_t         W_electron_eta;
    Float_t         W_electron_theta;
    Float_t         W_electron_phi;
    Int_t           W_electron_charge;
    Float_t         W_electron_vx;
    Float_t         W_electron_vy;
    Float_t         W_electron_vz;
    Float_t         W_electron_y;
    Float_t         W_electron_trackiso;
    Float_t         W_electron_hcaliso;
    Float_t         W_electron_ecaliso;
    Int_t           W_electron_classification;
    Float_t         W_electron_sc_x;
    Float_t         W_electron_sc_y;
    Float_t         W_electron_sc_z;
    Float_t         W_electron_sc_Theta;
    Float_t         W_electron_sc_Eta;
    Float_t         W_electron_sc_Phi;
    Float_t         W_electron_sc_E;
    Float_t         W_electron_sc_px;
    Float_t         W_electron_sc_py;
    Float_t         W_electron_sc_pz;
    Float_t         W_electron_sc_Pt;
    Float_t         W_electron_sc_Et;
    Float_t         W_electron_eoverp_out;
    Float_t         W_electron_eoverp_in;
    Float_t         W_electron_numbrem;
    Float_t         W_electron_fbrem;
    Float_t         W_electron_deltaeta_in;
    Float_t         W_electron_deltaphi_in;
    Float_t         W_electron_deltaphi_out;
    Float_t         W_electron_deltaeta_out;
    Float_t         W_electron_trackmom_calo;
    Float_t         W_electron_trackmom_vtx;
    Float_t         W_electron_hovere;
    Float_t         W_electron_e9e25;
    Float_t         W_electron_sigmaetaeta;
    Float_t         W_electron_sigmaietaieta;
    Int_t           W_electron_missingHits;
    Float_t         W_electron_dist;
    Float_t         W_electron_dcot;
    Float_t         W_electron_convradius;
    Bool_t          W_electron_isWP95;
    Bool_t          W_electron_isWP80;
    Bool_t          W_electron_isWP70;
    Float_t         W_electron_d0bsp;
    Float_t         W_electron_dz000;
    Float_t         W_electron_pfiso_chargedHadronIso;
    Float_t         W_electron_pfiso_photonIso;
    Float_t         W_electron_pfiso_neutralHadronIso;
    Int_t           numgoodPatJetsPFlowJets;
    Int_t           numgoodPatJetsPFlowJetBTags;
    Float_t         JetgoodPatJetsPFlow_Et[6];
    Float_t         JetgoodPatJetsPFlow_Pt[6];
    Float_t         JetgoodPatJetsPFlow_Eta[6];
    Float_t         JetgoodPatJetsPFlow_Phi[6];
    Float_t         JetgoodPatJetsPFlow_Theta[6];
    Float_t         JetgoodPatJetsPFlow_Px[6];
    Float_t         JetgoodPatJetsPFlow_Py[6];
    Float_t         JetgoodPatJetsPFlow_Pz[6];
    Float_t         JetgoodPatJetsPFlow_E[6];
    Float_t         JetgoodPatJetsPFlow_Y[6];
    Float_t         JetgoodPatJetsPFlow_Mass[6];
    Int_t           JetgoodPatJetsPFlow_nJetDaughters[6];
    Float_t         JetgoodPatJetsPFlow_subJet1Mass[6];
    Float_t         JetgoodPatJetsPFlow_subJet2Mass[6];
    Float_t         JetgoodPatJetsPFlow_etaetaMoment[6];
    Float_t         JetgoodPatJetsPFlow_phiphiMoment[6];
    Float_t         JetgoodPatJetsPFlow_etaphiMoment[6];
    Float_t         JetgoodPatJetsPFlow_maxDistance[6];
    Int_t           JetgoodPatJetsPFlow_nConstituents[6];
    Float_t         JetgoodPatJetsPFlow_Area[6];
    Float_t         VplusgoodPatJetsPFlowJet_Mass[6];
    Float_t         JetgoodPatJetsPFlow_dphiBoson[6];
    Float_t         JetgoodPatJetsPFlow_detaBoson[6];
    Float_t         JetgoodPatJetsPFlow_dRBoson[6];
    Float_t         JetgoodPatJetsPFlow_dphiMET[6];
    Float_t         JetgoodPatJetsPFlow_Response[6];
    Float_t         JetgoodPatJetsPFlow_bDiscriminator[6];
    Float_t         JetgoodPatJetsPFlow_bDiscriminatorSSVHE[6];
    Float_t         JetgoodPatJetsPFlow_bDiscriminatorTCHE[6];
    Float_t         JetgoodPatJetsPFlow_bDiscriminatorCSV[6];
    Float_t         JetgoodPatJetsPFlow_bDiscriminatorJP[6];
    Float_t         JetgoodPatJetsPFlow_bDiscriminatorSSVHP[6];
    Float_t         JetgoodPatJetsPFlow_bDiscriminatorTCHP[6];
    Float_t         JetgoodPatJetsPFlow_secVertexMass[6];
    Float_t         JetgoodPatJetsPFlow_dphiBoson2[6];
    Float_t         JetgoodPatJetsPFlow_detaBoson2[6];
    Float_t         JetgoodPatJetsPFlow_dRBoson2[6];
    Float_t         VplusgoodPatJetsPFlowJet_Mass2[6];
    Float_t         JetgoodPatJetsPFlow_Response2[6];
    Int_t           numgoodPatJetsCA8PrunedPFJets;
    Int_t           numgoodPatJetsCA8PrunedPFJetBTags;
    Float_t         JetgoodPatJetsCA8PrunedPF_Et[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_Pt[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_Eta[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_Phi[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_Theta[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_Px[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_Py[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_Pz[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_E[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_Y[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_Mass[6];
    Int_t           JetgoodPatJetsCA8PrunedPF_nJetDaughters[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_subJet1Mass[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_subJet2Mass[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_etaetaMoment[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_phiphiMoment[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_etaphiMoment[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_maxDistance[6];
    Int_t           JetgoodPatJetsCA8PrunedPF_nConstituents[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_Area[6];
    Float_t         VplusgoodPatJetsCA8PrunedPFJet_Mass[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_dphiBoson[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_detaBoson[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_dRBoson[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_dphiMET[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_Response[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_bDiscriminator[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_bDiscriminatorSSVHE[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_bDiscriminatorTCHE[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_bDiscriminatorCSV[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_bDiscriminatorJP[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_bDiscriminatorSSVHP[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_bDiscriminatorTCHP[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_secVertexMass[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_dphiBoson2[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_detaBoson2[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_dRBoson2[6];
    Float_t         VplusgoodPatJetsCA8PrunedPFJet_Mass2[6];
    Float_t         JetgoodPatJetsCA8PrunedPF_Response2[6];
    Int_t           numgoodPatJetsCA8PFJets;
    Int_t           numgoodPatJetsCA8PFJetBTags;
    Float_t         JetgoodPatJetsCA8PF_Et[6];
    Float_t         JetgoodPatJetsCA8PF_Pt[6];
    Float_t         JetgoodPatJetsCA8PF_Eta[6];
    Float_t         JetgoodPatJetsCA8PF_Phi[6];
    Float_t         JetgoodPatJetsCA8PF_Theta[6];
    Float_t         JetgoodPatJetsCA8PF_Px[6];
    Float_t         JetgoodPatJetsCA8PF_Py[6];
    Float_t         JetgoodPatJetsCA8PF_Pz[6];
    Float_t         JetgoodPatJetsCA8PF_E[6];
    Float_t         JetgoodPatJetsCA8PF_Y[6];
    Float_t         JetgoodPatJetsCA8PF_Mass[6];
    Int_t           JetgoodPatJetsCA8PF_nJetDaughters[6];
    Float_t         JetgoodPatJetsCA8PF_subJet1Mass[6];
    Float_t         JetgoodPatJetsCA8PF_subJet2Mass[6];
    Float_t         JetgoodPatJetsCA8PF_etaetaMoment[6];
    Float_t         JetgoodPatJetsCA8PF_phiphiMoment[6];
    Float_t         JetgoodPatJetsCA8PF_etaphiMoment[6];
    Float_t         JetgoodPatJetsCA8PF_maxDistance[6];
    Int_t           JetgoodPatJetsCA8PF_nConstituents[6];
    Float_t         JetgoodPatJetsCA8PF_Area[6];
    Float_t         VplusgoodPatJetsCA8PFJet_Mass[6];
    Float_t         JetgoodPatJetsCA8PF_dphiBoson[6];
    Float_t         JetgoodPatJetsCA8PF_detaBoson[6];
    Float_t         JetgoodPatJetsCA8PF_dRBoson[6];
    Float_t         JetgoodPatJetsCA8PF_dphiMET[6];
    Float_t         JetgoodPatJetsCA8PF_Response[6];
    Float_t         JetgoodPatJetsCA8PF_bDiscriminator[6];
    Float_t         JetgoodPatJetsCA8PF_bDiscriminatorSSVHE[6];
    Float_t         JetgoodPatJetsCA8PF_bDiscriminatorTCHE[6];
    Float_t         JetgoodPatJetsCA8PF_bDiscriminatorCSV[6];
    Float_t         JetgoodPatJetsCA8PF_bDiscriminatorJP[6];
    Float_t         JetgoodPatJetsCA8PF_bDiscriminatorSSVHP[6];
    Float_t         JetgoodPatJetsCA8PF_bDiscriminatorTCHP[6];
    Float_t         JetgoodPatJetsCA8PF_secVertexMass[6];
    Float_t         JetgoodPatJetsCA8PF_dphiBoson2[6];
    Float_t         JetgoodPatJetsCA8PF_detaBoson2[6];
    Float_t         JetgoodPatJetsCA8PF_dRBoson2[6];
    Float_t         VplusgoodPatJetsCA8PFJet_Mass2[6];
    Float_t         JetgoodPatJetsCA8PF_Response2[6];
    Int_t           event_runNo;
    Int_t           event_evtNo;
    Int_t           event_lumi;
    Int_t           event_bunch;
    Int_t           event_nPV;
    Float_t         event_PVx[30];
    Float_t         event_PVy[30];
    Float_t         event_PVz[30];
    Float_t         event_met_pfmet;
    Float_t         event_met_pfsumet;
    Float_t         event_met_pfmetsignificance;
    Float_t         event_met_pfmetPhi;
    Float_t         event_fastJetRho;
    Float_t         event_RhoForLeptonIsolation;
    Float_t         event_BeamSpot_x;
    Float_t         event_BeamSpot_y;
    Float_t         event_BeamSpot_z;
    Int_t           numW;
    Float_t         event_met_genmet;
    Float_t         event_met_gensumet;
    Float_t         event_met_genmetsignificance;
    Float_t         event_met_genmetPhi;
    Float_t         event_mcPU_totnvtx;
    Float_t         event_mcPU_bx[3];
    Float_t         event_mcPU_nvtx[3];
    
    // List of branches
    TBranch        *b_W_mass;   //!
    TBranch        *b_W_mt;   //!
    TBranch        *b_W_px;   //!
    TBranch        *b_W_py;   //!
    TBranch        *b_W_pz;   //!
    TBranch        *b_W_e;   //!
    TBranch        *b_W_pt;   //!
    TBranch        *b_W_et;   //!
    TBranch        *b_W_eta;   //!
    TBranch        *b_W_phi;   //!
    TBranch        *b_W_vx;   //!
    TBranch        *b_W_vy;   //!
    TBranch        *b_W_vz;   //!
    TBranch        *b_W_y;   //!
    TBranch        *b_W_numTightElectrons;   //!
    TBranch        *b_W_numLooseElectrons;   //!
    TBranch        *b_W_pzNu1;   //!
    TBranch        *b_W_pzNu2;   //!
    TBranch        *b_W_electron_px;   //!
    TBranch        *b_W_electron_py;   //!
    TBranch        *b_W_electron_pz;   //!
    TBranch        *b_W_electron_e;   //!
    TBranch        *b_W_electron_pt;   //!
    TBranch        *b_W_electron_et;   //!
    TBranch        *b_W_electron_eta;   //!
    TBranch        *b_W_electron_theta;   //!
    TBranch        *b_W_electron_phi;   //!
    TBranch        *b_W_electron_charge;   //!
    TBranch        *b_W_electron_vx;   //!
    TBranch        *b_W_electron_vy;   //!
    TBranch        *b_W_electron_vz;   //!
    TBranch        *b_W_electron_y;   //!
    TBranch        *b_W_electron_trackiso;   //!
    TBranch        *b_W_electron_hcaliso;   //!
    TBranch        *b_W_electron_ecaliso;   //!
    TBranch        *b_W_electron_classification;   //!
    TBranch        *b_W_electron_sc_x;   //!
    TBranch        *b_W_electron_sc_y;   //!
    TBranch        *b_W_electron_sc_z;   //!
    TBranch        *b_W_electron_sc_Theta;   //!
    TBranch        *b_W_electron_sc_Eta;   //!
    TBranch        *b_W_electron_sc_Phi;   //!
    TBranch        *b_W_electron_sc_E;   //!
    TBranch        *b_W_electron_sc_px;   //!
    TBranch        *b_W_electron_sc_py;   //!
    TBranch        *b_W_electron_sc_pz;   //!
    TBranch        *b_W_electron_sc_Pt;   //!
    TBranch        *b_W_electron_sc_Et;   //!
    TBranch        *b_W_electron_eoverp_out;   //!
    TBranch        *b_W_electron_eoverp_in;   //!
    TBranch        *b_W_electron_numbrem;   //!
    TBranch        *b_W_electron_fbrem;   //!
    TBranch        *b_W_electron_deltaeta_in;   //!
    TBranch        *b_W_electron_deltaphi_in;   //!
    TBranch        *b_W_electron_deltaphi_out;   //!
    TBranch        *b_W_electron_deltaeta_out;   //!
    TBranch        *b_W_electron_trackmom_calo;   //!
    TBranch        *b_W_electron_trackmom_vtx;   //!
    TBranch        *b_W_electron_hovere;   //!
    TBranch        *b_W_electron_e9e25;   //!
    TBranch        *b_W_electron_sigmaetaeta;   //!
    TBranch        *b_W_electron_sigmaietaieta;   //!
    TBranch        *b_W_electron_missingHits;   //!
    TBranch        *b_W_electron_dist;   //!
    TBranch        *b_W_electron_dcot;   //!
    TBranch        *b_W_electron_convradius;   //!
    TBranch        *b_W_electron_isWP95;   //!
    TBranch        *b_W_electron_isWP80;   //!
    TBranch        *b_W_electron_isWP70;   //!
    TBranch        *b_W_electron_d0bsp;   //!
    TBranch        *b_W_electron_dz000;   //!
    TBranch        *b_W_electron_pfiso_chargedHadronIso;   //!
    TBranch        *b_W_electron_pfiso_photonIso;   //!
    TBranch        *b_W_electron_pfiso_neutralHadronIso;   //!
    TBranch        *b_numgoodPatJetsPFlowJets;   //!
    TBranch        *b_numgoodPatJetsPFlowJetBTags;   //!
    TBranch        *b_JetgoodPatJetsPFlow_Et;   //!
    TBranch        *b_JetgoodPatJetsPFlow_Pt;   //!
    TBranch        *b_JetgoodPatJetsPFlow_Eta;   //!
    TBranch        *b_JetgoodPatJetsPFlow_Phi;   //!
    TBranch        *b_JetgoodPatJetsPFlow_Theta;   //!
    TBranch        *b_JetgoodPatJetsPFlow_Px;   //!
    TBranch        *b_JetgoodPatJetsPFlow_Py;   //!
    TBranch        *b_JetgoodPatJetsPFlow_Pz;   //!
    TBranch        *b_JetgoodPatJetsPFlow_E;   //!
    TBranch        *b_JetgoodPatJetsPFlow_Y;   //!
    TBranch        *b_JetgoodPatJetsPFlow_Mass;   //!
    TBranch        *b_JetgoodPatJetsPFlow_nJetDaughters;   //!
    TBranch        *b_JetgoodPatJetsPFlow_subJet1Mass;   //!
    TBranch        *b_JetgoodPatJetsPFlow_subJet2Mass;   //!
    TBranch        *b_JetgoodPatJetsPFlow_etaetaMoment;   //!
    TBranch        *b_JetgoodPatJetsPFlow_phiphiMoment;   //!
    TBranch        *b_JetgoodPatJetsPFlow_etaphiMoment;   //!
    TBranch        *b_JetgoodPatJetsPFlow_maxDistance;   //!
    TBranch        *b_JetgoodPatJetsPFlow_nConstituents;   //!
    TBranch        *b_JetgoodPatJetsPFlow_Area;   //!
    TBranch        *b_VplusgoodPatJetsPFlowJet_Mass;   //!
    TBranch        *b_JetgoodPatJetsPFlow_dphiBoson;   //!
    TBranch        *b_JetgoodPatJetsPFlow_detaBoson;   //!
    TBranch        *b_JetgoodPatJetsPFlow_dRBoson;   //!
    TBranch        *b_JetgoodPatJetsPFlow_dphiMET;   //!
    TBranch        *b_JetgoodPatJetsPFlow_Response;   //!
    TBranch        *b_JetgoodPatJetsPFlow_bDiscriminator;   //!
    TBranch        *b_JetgoodPatJetsPFlow_bDiscriminatorSSVHE;   //!
    TBranch        *b_JetgoodPatJetsPFlow_bDiscriminatorTCHE;   //!
    TBranch        *b_JetgoodPatJetsPFlow_bDiscriminatorCSV;   //!
    TBranch        *b_JetgoodPatJetsPFlow_bDiscriminatorJP;   //!
    TBranch        *b_JetgoodPatJetsPFlow_bDiscriminatorSSVHP;   //!
    TBranch        *b_JetgoodPatJetsPFlow_bDiscriminatorTCHP;   //!
    TBranch        *b_JetgoodPatJetsPFlow_secVertexMass;   //!
    TBranch        *b_JetgoodPatJetsPFlow_dphiBoson2;   //!
    TBranch        *b_JetgoodPatJetsPFlow_detaBoson2;   //!
    TBranch        *b_JetgoodPatJetsPFlow_dRBoson2;   //!
    TBranch        *b_VplusgoodPatJetsPFlowJet_Mass2;   //!
    TBranch        *b_JetgoodPatJetsPFlow_Response2;   //!
    TBranch        *b_numgoodPatJetsCA8PrunedPFJets;   //!
    TBranch        *b_numgoodPatJetsCA8PrunedPFJetBTags;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_Et;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_Pt;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_Eta;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_Phi;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_Theta;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_Px;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_Py;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_Pz;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_E;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_Y;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_Mass;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_nJetDaughters;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_subJet1Mass;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_subJet2Mass;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_etaetaMoment;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_phiphiMoment;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_etaphiMoment;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_maxDistance;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_nConstituents;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_Area;   //!
    TBranch        *b_VplusgoodPatJetsCA8PrunedPFJet_Mass;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_dphiBoson;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_detaBoson;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_dRBoson;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_dphiMET;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_Response;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_bDiscriminator;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_bDiscriminatorSSVHE;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_bDiscriminatorTCHE;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_bDiscriminatorCSV;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_bDiscriminatorJP;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_bDiscriminatorSSVHP;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_bDiscriminatorTCHP;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_secVertexMass;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_dphiBoson2;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_detaBoson2;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_dRBoson2;   //!
    TBranch        *b_VplusgoodPatJetsCA8PrunedPFJet_Mass2;   //!
    TBranch        *b_JetgoodPatJetsCA8PrunedPF_Response2;   //!
    TBranch        *b_numgoodPatJetsCA8PFJets;   //!
    TBranch        *b_numgoodPatJetsCA8PFJetBTags;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_Et;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_Pt;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_Eta;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_Phi;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_Theta;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_Px;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_Py;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_Pz;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_E;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_Y;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_Mass;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_nJetDaughters;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_subJet1Mass;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_subJet2Mass;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_etaetaMoment;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_phiphiMoment;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_etaphiMoment;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_maxDistance;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_nConstituents;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_Area;   //!
    TBranch        *b_VplusgoodPatJetsCA8PFJet_Mass;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_dphiBoson;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_detaBoson;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_dRBoson;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_dphiMET;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_Response;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_bDiscriminator;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_bDiscriminatorSSVHE;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_bDiscriminatorTCHE;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_bDiscriminatorCSV;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_bDiscriminatorJP;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_bDiscriminatorSSVHP;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_bDiscriminatorTCHP;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_secVertexMass;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_dphiBoson2;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_detaBoson2;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_dRBoson2;   //!
    TBranch        *b_VplusgoodPatJetsCA8PFJet_Mass2;   //!
    TBranch        *b_JetgoodPatJetsCA8PF_Response2;   //!
    TBranch        *b_event_runNo;   //!
    TBranch        *b_event_evtNo;   //!
    TBranch        *b_event_lumi;   //!
    TBranch        *b_event_bunch;   //!
    TBranch        *b_event_nPV;   //!
    TBranch        *b_event_PVx;   //!
    TBranch        *b_event_PVy;   //!
    TBranch        *b_event_PVz;   //!
    TBranch        *b_event_met_pfmet;   //!
    TBranch        *b_event_met_pfsumet;   //!
    TBranch        *b_event_met_pfmetsignificance;   //!
    TBranch        *b_event_met_pfmetPhi;   //!
    TBranch        *b_event_fastJetRho;   //!
    TBranch        *b_event_RhoForLeptonIsolation;   //!
    TBranch        *b_event_BeamSpot_x;   //!
    TBranch        *b_event_BeamSpot_y;   //!
    TBranch        *b_event_BeamSpot_z;   //!
    TBranch        *b_numW;   //!
    TBranch        *b_event_met_genmet;   //!
    TBranch        *b_event_met_gensumet;   //!
    TBranch        *b_event_met_genmetsignificance;   //!
    TBranch        *b_event_met_genmetPhi;   //!
    TBranch        *b_event_mcPU_totnvtx;   //!
    TBranch        *b_event_mcPU_bx;   //!
    TBranch        *b_event_mcPU_nvtx;   //!
    
    vJetSubstructure(std::string inputname,TTree *tree=0);
    virtual ~vJetSubstructure();
    virtual Int_t    Cut(Long64_t entry);
    virtual Int_t    GetEntry(Long64_t entry);
    virtual Long64_t LoadTree(Long64_t entry);
    virtual void     Init(TTree *tree);
    virtual void     Loop();
    virtual Bool_t   Notify();
    virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef vJetSubstructure_cxx
vJetSubstructure::vJetSubstructure(std::string inputname,TTree *tree)
{
    /*
     // if parameter tree is not specified (or zero), connect the file
     // used to generate this class and read the Tree.
     if (tree == 0) {
     //TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("outputCrab_WW_full_v2.root");
     TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("outputCrab_HWW600_full.root");
     //TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("demo.root");
     if (!f) {
     //f = new TFile("demo.root");
     //f = new TFile("outputCrab_WW_full_v2.root");
     f = new TFile("outputCrab_HWW600_full.root");
     }
     //*/
    
    char fname[192];
    sprintf(fname,"%s",inputname.c_str());
    TFile* f = new TFile(fname);
    
    tree = (TTree*)gDirectory->Get("VJetSubstructure");
    
    Init(tree);
}

vJetSubstructure::~vJetSubstructure()
{
    if (!fChain) return;
    delete fChain->GetCurrentFile();
}

Int_t vJetSubstructure::GetEntry(Long64_t entry)
{
    // Read contents of entry.
    if (!fChain) return 0;
    return fChain->GetEntry(entry);
}
Long64_t vJetSubstructure::LoadTree(Long64_t entry)
{
    // Set the environment to read one entry
    if (!fChain) return -5;
    Long64_t centry = fChain->LoadTree(entry);
    if (centry < 0) return centry;
    if (!fChain->InheritsFrom(TChain::Class()))  return centry;
    TChain *chain = (TChain*)fChain;
    if (chain->GetTreeNumber() != fCurrent) {
        fCurrent = chain->GetTreeNumber();
        Notify();
    }
    return centry;
}

void vJetSubstructure::Init(TTree *tree)
{
    // The Init() function is called when the selector needs to initialize
    // a new tree or chain. Typically here the branch addresses and branch
    // pointers of the tree will be set.
    // It is normally not necessary to make changes to the generated
    // code, but the routine can be extended by the user if needed.
    // Init() will be called many times when running on PROOF
    // (once per file to be processed).
    
    // Set branch addresses and branch pointers
    if (!tree) return;
    fChain = tree;
    fCurrent = -1;
    fChain->SetMakeClass(1);
    
    fChain->SetBranchAddress("W_mass", &W_mass, &b_W_mass);
    fChain->SetBranchAddress("W_mt", &W_mt, &b_W_mt);
    fChain->SetBranchAddress("W_px", &W_px, &b_W_px);
    fChain->SetBranchAddress("W_py", &W_py, &b_W_py);
    fChain->SetBranchAddress("W_pz", &W_pz, &b_W_pz);
    fChain->SetBranchAddress("W_e", &W_e, &b_W_e);
    fChain->SetBranchAddress("W_pt", &W_pt, &b_W_pt);
    fChain->SetBranchAddress("W_et", &W_et, &b_W_et);
    fChain->SetBranchAddress("W_eta", &W_eta, &b_W_eta);
    fChain->SetBranchAddress("W_phi", &W_phi, &b_W_phi);
    fChain->SetBranchAddress("W_vx", &W_vx, &b_W_vx);
    fChain->SetBranchAddress("W_vy", &W_vy, &b_W_vy);
    fChain->SetBranchAddress("W_vz", &W_vz, &b_W_vz);
    fChain->SetBranchAddress("W_y", &W_y, &b_W_y);
    fChain->SetBranchAddress("W_numTightElectrons", &W_numTightElectrons, &b_W_numTightElectrons);
    fChain->SetBranchAddress("W_numLooseElectrons", &W_numLooseElectrons, &b_W_numLooseElectrons);
    fChain->SetBranchAddress("W_pzNu1", &W_pzNu1, &b_W_pzNu1);
    fChain->SetBranchAddress("W_pzNu2", &W_pzNu2, &b_W_pzNu2);
    fChain->SetBranchAddress("W_electron_px", &W_electron_px, &b_W_electron_px);
    fChain->SetBranchAddress("W_electron_py", &W_electron_py, &b_W_electron_py);
    fChain->SetBranchAddress("W_electron_pz", &W_electron_pz, &b_W_electron_pz);
    fChain->SetBranchAddress("W_electron_e", &W_electron_e, &b_W_electron_e);
    fChain->SetBranchAddress("W_electron_pt", &W_electron_pt, &b_W_electron_pt);
    fChain->SetBranchAddress("W_electron_et", &W_electron_et, &b_W_electron_et);
    fChain->SetBranchAddress("W_electron_eta", &W_electron_eta, &b_W_electron_eta);
    fChain->SetBranchAddress("W_electron_theta", &W_electron_theta, &b_W_electron_theta);
    fChain->SetBranchAddress("W_electron_phi", &W_electron_phi, &b_W_electron_phi);
    fChain->SetBranchAddress("W_electron_charge", &W_electron_charge, &b_W_electron_charge);
    fChain->SetBranchAddress("W_electron_vx", &W_electron_vx, &b_W_electron_vx);
    fChain->SetBranchAddress("W_electron_vy", &W_electron_vy, &b_W_electron_vy);
    fChain->SetBranchAddress("W_electron_vz", &W_electron_vz, &b_W_electron_vz);
    fChain->SetBranchAddress("W_electron_y", &W_electron_y, &b_W_electron_y);
    fChain->SetBranchAddress("W_electron_trackiso", &W_electron_trackiso, &b_W_electron_trackiso);
    fChain->SetBranchAddress("W_electron_hcaliso", &W_electron_hcaliso, &b_W_electron_hcaliso);
    fChain->SetBranchAddress("W_electron_ecaliso", &W_electron_ecaliso, &b_W_electron_ecaliso);
    fChain->SetBranchAddress("W_electron_classification", &W_electron_classification, &b_W_electron_classification);
    fChain->SetBranchAddress("W_electron_sc_x", &W_electron_sc_x, &b_W_electron_sc_x);
    fChain->SetBranchAddress("W_electron_sc_y", &W_electron_sc_y, &b_W_electron_sc_y);
    fChain->SetBranchAddress("W_electron_sc_z", &W_electron_sc_z, &b_W_electron_sc_z);
    fChain->SetBranchAddress("W_electron_sc_Theta", &W_electron_sc_Theta, &b_W_electron_sc_Theta);
    fChain->SetBranchAddress("W_electron_sc_Eta", &W_electron_sc_Eta, &b_W_electron_sc_Eta);
    fChain->SetBranchAddress("W_electron_sc_Phi", &W_electron_sc_Phi, &b_W_electron_sc_Phi);
    fChain->SetBranchAddress("W_electron_sc_E", &W_electron_sc_E, &b_W_electron_sc_E);
    fChain->SetBranchAddress("W_electron_sc_px", &W_electron_sc_px, &b_W_electron_sc_px);
    fChain->SetBranchAddress("W_electron_sc_py", &W_electron_sc_py, &b_W_electron_sc_py);
    fChain->SetBranchAddress("W_electron_sc_pz", &W_electron_sc_pz, &b_W_electron_sc_pz);
    fChain->SetBranchAddress("W_electron_sc_Pt", &W_electron_sc_Pt, &b_W_electron_sc_Pt);
    fChain->SetBranchAddress("W_electron_sc_Et", &W_electron_sc_Et, &b_W_electron_sc_Et);
    fChain->SetBranchAddress("W_electron_eoverp_out", &W_electron_eoverp_out, &b_W_electron_eoverp_out);
    fChain->SetBranchAddress("W_electron_eoverp_in", &W_electron_eoverp_in, &b_W_electron_eoverp_in);
    fChain->SetBranchAddress("W_electron_numbrem", &W_electron_numbrem, &b_W_electron_numbrem);
    fChain->SetBranchAddress("W_electron_fbrem", &W_electron_fbrem, &b_W_electron_fbrem);
    fChain->SetBranchAddress("W_electron_deltaeta_in", &W_electron_deltaeta_in, &b_W_electron_deltaeta_in);
    fChain->SetBranchAddress("W_electron_deltaphi_in", &W_electron_deltaphi_in, &b_W_electron_deltaphi_in);
    fChain->SetBranchAddress("W_electron_deltaphi_out", &W_electron_deltaphi_out, &b_W_electron_deltaphi_out);
    fChain->SetBranchAddress("W_electron_deltaeta_out", &W_electron_deltaeta_out, &b_W_electron_deltaeta_out);
    fChain->SetBranchAddress("W_electron_trackmom_calo", &W_electron_trackmom_calo, &b_W_electron_trackmom_calo);
    fChain->SetBranchAddress("W_electron_trackmom_vtx", &W_electron_trackmom_vtx, &b_W_electron_trackmom_vtx);
    fChain->SetBranchAddress("W_electron_hovere", &W_electron_hovere, &b_W_electron_hovere);
    fChain->SetBranchAddress("W_electron_e9e25", &W_electron_e9e25, &b_W_electron_e9e25);
    fChain->SetBranchAddress("W_electron_sigmaetaeta", &W_electron_sigmaetaeta, &b_W_electron_sigmaetaeta);
    fChain->SetBranchAddress("W_electron_sigmaietaieta", &W_electron_sigmaietaieta, &b_W_electron_sigmaietaieta);
    fChain->SetBranchAddress("W_electron_missingHits", &W_electron_missingHits, &b_W_electron_missingHits);
    fChain->SetBranchAddress("W_electron_dist", &W_electron_dist, &b_W_electron_dist);
    fChain->SetBranchAddress("W_electron_dcot", &W_electron_dcot, &b_W_electron_dcot);
    fChain->SetBranchAddress("W_electron_convradius", &W_electron_convradius, &b_W_electron_convradius);
    fChain->SetBranchAddress("W_electron_isWP95", &W_electron_isWP95, &b_W_electron_isWP95);
    fChain->SetBranchAddress("W_electron_isWP80", &W_electron_isWP80, &b_W_electron_isWP80);
    fChain->SetBranchAddress("W_electron_isWP70", &W_electron_isWP70, &b_W_electron_isWP70);
    fChain->SetBranchAddress("W_electron_d0bsp", &W_electron_d0bsp, &b_W_electron_d0bsp);
    fChain->SetBranchAddress("W_electron_dz000", &W_electron_dz000, &b_W_electron_dz000);
    fChain->SetBranchAddress("W_electron_pfiso_chargedHadronIso", &W_electron_pfiso_chargedHadronIso, &b_W_electron_pfiso_chargedHadronIso);
    fChain->SetBranchAddress("W_electron_pfiso_photonIso", &W_electron_pfiso_photonIso, &b_W_electron_pfiso_photonIso);
    fChain->SetBranchAddress("W_electron_pfiso_neutralHadronIso", &W_electron_pfiso_neutralHadronIso, &b_W_electron_pfiso_neutralHadronIso);
    fChain->SetBranchAddress("numgoodPatJetsPFlowJets", &numgoodPatJetsPFlowJets, &b_numgoodPatJetsPFlowJets);
    fChain->SetBranchAddress("numgoodPatJetsPFlowJetBTags", &numgoodPatJetsPFlowJetBTags, &b_numgoodPatJetsPFlowJetBTags);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_Et", JetgoodPatJetsPFlow_Et, &b_JetgoodPatJetsPFlow_Et);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_Pt", JetgoodPatJetsPFlow_Pt, &b_JetgoodPatJetsPFlow_Pt);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_Eta", JetgoodPatJetsPFlow_Eta, &b_JetgoodPatJetsPFlow_Eta);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_Phi", JetgoodPatJetsPFlow_Phi, &b_JetgoodPatJetsPFlow_Phi);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_Theta", JetgoodPatJetsPFlow_Theta, &b_JetgoodPatJetsPFlow_Theta);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_Px", JetgoodPatJetsPFlow_Px, &b_JetgoodPatJetsPFlow_Px);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_Py", JetgoodPatJetsPFlow_Py, &b_JetgoodPatJetsPFlow_Py);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_Pz", JetgoodPatJetsPFlow_Pz, &b_JetgoodPatJetsPFlow_Pz);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_E", JetgoodPatJetsPFlow_E, &b_JetgoodPatJetsPFlow_E);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_Y", JetgoodPatJetsPFlow_Y, &b_JetgoodPatJetsPFlow_Y);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_Mass", JetgoodPatJetsPFlow_Mass, &b_JetgoodPatJetsPFlow_Mass);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_nJetDaughters", JetgoodPatJetsPFlow_nJetDaughters, &b_JetgoodPatJetsPFlow_nJetDaughters);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_subJet1Mass", JetgoodPatJetsPFlow_subJet1Mass, &b_JetgoodPatJetsPFlow_subJet1Mass);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_subJet2Mass", JetgoodPatJetsPFlow_subJet2Mass, &b_JetgoodPatJetsPFlow_subJet2Mass);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_etaetaMoment", JetgoodPatJetsPFlow_etaetaMoment, &b_JetgoodPatJetsPFlow_etaetaMoment);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_phiphiMoment", JetgoodPatJetsPFlow_phiphiMoment, &b_JetgoodPatJetsPFlow_phiphiMoment);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_etaphiMoment", JetgoodPatJetsPFlow_etaphiMoment, &b_JetgoodPatJetsPFlow_etaphiMoment);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_maxDistance", JetgoodPatJetsPFlow_maxDistance, &b_JetgoodPatJetsPFlow_maxDistance);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_nConstituents", JetgoodPatJetsPFlow_nConstituents, &b_JetgoodPatJetsPFlow_nConstituents);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_Area", JetgoodPatJetsPFlow_Area, &b_JetgoodPatJetsPFlow_Area);
    fChain->SetBranchAddress("VplusgoodPatJetsPFlowJet_Mass", VplusgoodPatJetsPFlowJet_Mass, &b_VplusgoodPatJetsPFlowJet_Mass);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_dphiBoson", JetgoodPatJetsPFlow_dphiBoson, &b_JetgoodPatJetsPFlow_dphiBoson);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_detaBoson", JetgoodPatJetsPFlow_detaBoson, &b_JetgoodPatJetsPFlow_detaBoson);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_dRBoson", JetgoodPatJetsPFlow_dRBoson, &b_JetgoodPatJetsPFlow_dRBoson);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_dphiMET", JetgoodPatJetsPFlow_dphiMET, &b_JetgoodPatJetsPFlow_dphiMET);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_Response", JetgoodPatJetsPFlow_Response, &b_JetgoodPatJetsPFlow_Response);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_bDiscriminator", JetgoodPatJetsPFlow_bDiscriminator, &b_JetgoodPatJetsPFlow_bDiscriminator);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_bDiscriminatorSSVHE", JetgoodPatJetsPFlow_bDiscriminatorSSVHE, &b_JetgoodPatJetsPFlow_bDiscriminatorSSVHE);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_bDiscriminatorTCHE", JetgoodPatJetsPFlow_bDiscriminatorTCHE, &b_JetgoodPatJetsPFlow_bDiscriminatorTCHE);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_bDiscriminatorCSV", JetgoodPatJetsPFlow_bDiscriminatorCSV, &b_JetgoodPatJetsPFlow_bDiscriminatorCSV);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_bDiscriminatorJP", JetgoodPatJetsPFlow_bDiscriminatorJP, &b_JetgoodPatJetsPFlow_bDiscriminatorJP);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_bDiscriminatorSSVHP", JetgoodPatJetsPFlow_bDiscriminatorSSVHP, &b_JetgoodPatJetsPFlow_bDiscriminatorSSVHP);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_bDiscriminatorTCHP", JetgoodPatJetsPFlow_bDiscriminatorTCHP, &b_JetgoodPatJetsPFlow_bDiscriminatorTCHP);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_secVertexMass", JetgoodPatJetsPFlow_secVertexMass, &b_JetgoodPatJetsPFlow_secVertexMass);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_dphiBoson2", JetgoodPatJetsPFlow_dphiBoson2, &b_JetgoodPatJetsPFlow_dphiBoson2);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_detaBoson2", JetgoodPatJetsPFlow_detaBoson2, &b_JetgoodPatJetsPFlow_detaBoson2);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_dRBoson2", JetgoodPatJetsPFlow_dRBoson2, &b_JetgoodPatJetsPFlow_dRBoson2);
    fChain->SetBranchAddress("VplusgoodPatJetsPFlowJet_Mass2", VplusgoodPatJetsPFlowJet_Mass2, &b_VplusgoodPatJetsPFlowJet_Mass2);
    fChain->SetBranchAddress("JetgoodPatJetsPFlow_Response2", JetgoodPatJetsPFlow_Response2, &b_JetgoodPatJetsPFlow_Response2);
    fChain->SetBranchAddress("numgoodPatJetsCA8PrunedPFJets", &numgoodPatJetsCA8PrunedPFJets, &b_numgoodPatJetsCA8PrunedPFJets);
    fChain->SetBranchAddress("numgoodPatJetsCA8PrunedPFJetBTags", &numgoodPatJetsCA8PrunedPFJetBTags, &b_numgoodPatJetsCA8PrunedPFJetBTags);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_Et", JetgoodPatJetsCA8PrunedPF_Et, &b_JetgoodPatJetsCA8PrunedPF_Et);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_Pt", JetgoodPatJetsCA8PrunedPF_Pt, &b_JetgoodPatJetsCA8PrunedPF_Pt);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_Eta", JetgoodPatJetsCA8PrunedPF_Eta, &b_JetgoodPatJetsCA8PrunedPF_Eta);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_Phi", JetgoodPatJetsCA8PrunedPF_Phi, &b_JetgoodPatJetsCA8PrunedPF_Phi);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_Theta", JetgoodPatJetsCA8PrunedPF_Theta, &b_JetgoodPatJetsCA8PrunedPF_Theta);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_Px", JetgoodPatJetsCA8PrunedPF_Px, &b_JetgoodPatJetsCA8PrunedPF_Px);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_Py", JetgoodPatJetsCA8PrunedPF_Py, &b_JetgoodPatJetsCA8PrunedPF_Py);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_Pz", JetgoodPatJetsCA8PrunedPF_Pz, &b_JetgoodPatJetsCA8PrunedPF_Pz);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_E", JetgoodPatJetsCA8PrunedPF_E, &b_JetgoodPatJetsCA8PrunedPF_E);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_Y", JetgoodPatJetsCA8PrunedPF_Y, &b_JetgoodPatJetsCA8PrunedPF_Y);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_Mass", JetgoodPatJetsCA8PrunedPF_Mass, &b_JetgoodPatJetsCA8PrunedPF_Mass);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_nJetDaughters", JetgoodPatJetsCA8PrunedPF_nJetDaughters, &b_JetgoodPatJetsCA8PrunedPF_nJetDaughters);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_subJet1Mass", JetgoodPatJetsCA8PrunedPF_subJet1Mass, &b_JetgoodPatJetsCA8PrunedPF_subJet1Mass);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_subJet2Mass", JetgoodPatJetsCA8PrunedPF_subJet2Mass, &b_JetgoodPatJetsCA8PrunedPF_subJet2Mass);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_etaetaMoment", JetgoodPatJetsCA8PrunedPF_etaetaMoment, &b_JetgoodPatJetsCA8PrunedPF_etaetaMoment);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_phiphiMoment", JetgoodPatJetsCA8PrunedPF_phiphiMoment, &b_JetgoodPatJetsCA8PrunedPF_phiphiMoment);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_etaphiMoment", JetgoodPatJetsCA8PrunedPF_etaphiMoment, &b_JetgoodPatJetsCA8PrunedPF_etaphiMoment);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_maxDistance", JetgoodPatJetsCA8PrunedPF_maxDistance, &b_JetgoodPatJetsCA8PrunedPF_maxDistance);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_nConstituents", JetgoodPatJetsCA8PrunedPF_nConstituents, &b_JetgoodPatJetsCA8PrunedPF_nConstituents);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_Area", JetgoodPatJetsCA8PrunedPF_Area, &b_JetgoodPatJetsCA8PrunedPF_Area);
    fChain->SetBranchAddress("VplusgoodPatJetsCA8PrunedPFJet_Mass", VplusgoodPatJetsCA8PrunedPFJet_Mass, &b_VplusgoodPatJetsCA8PrunedPFJet_Mass);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_dphiBoson", JetgoodPatJetsCA8PrunedPF_dphiBoson, &b_JetgoodPatJetsCA8PrunedPF_dphiBoson);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_detaBoson", JetgoodPatJetsCA8PrunedPF_detaBoson, &b_JetgoodPatJetsCA8PrunedPF_detaBoson);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_dRBoson", JetgoodPatJetsCA8PrunedPF_dRBoson, &b_JetgoodPatJetsCA8PrunedPF_dRBoson);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_dphiMET", JetgoodPatJetsCA8PrunedPF_dphiMET, &b_JetgoodPatJetsCA8PrunedPF_dphiMET);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_Response", JetgoodPatJetsCA8PrunedPF_Response, &b_JetgoodPatJetsCA8PrunedPF_Response);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_bDiscriminator", JetgoodPatJetsCA8PrunedPF_bDiscriminator, &b_JetgoodPatJetsCA8PrunedPF_bDiscriminator);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_bDiscriminatorSSVHE", JetgoodPatJetsCA8PrunedPF_bDiscriminatorSSVHE, &b_JetgoodPatJetsCA8PrunedPF_bDiscriminatorSSVHE);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_bDiscriminatorTCHE", JetgoodPatJetsCA8PrunedPF_bDiscriminatorTCHE, &b_JetgoodPatJetsCA8PrunedPF_bDiscriminatorTCHE);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_bDiscriminatorCSV", JetgoodPatJetsCA8PrunedPF_bDiscriminatorCSV, &b_JetgoodPatJetsCA8PrunedPF_bDiscriminatorCSV);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_bDiscriminatorJP", JetgoodPatJetsCA8PrunedPF_bDiscriminatorJP, &b_JetgoodPatJetsCA8PrunedPF_bDiscriminatorJP);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_bDiscriminatorSSVHP", JetgoodPatJetsCA8PrunedPF_bDiscriminatorSSVHP, &b_JetgoodPatJetsCA8PrunedPF_bDiscriminatorSSVHP);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_bDiscriminatorTCHP", JetgoodPatJetsCA8PrunedPF_bDiscriminatorTCHP, &b_JetgoodPatJetsCA8PrunedPF_bDiscriminatorTCHP);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_secVertexMass", JetgoodPatJetsCA8PrunedPF_secVertexMass, &b_JetgoodPatJetsCA8PrunedPF_secVertexMass);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_dphiBoson2", JetgoodPatJetsCA8PrunedPF_dphiBoson2, &b_JetgoodPatJetsCA8PrunedPF_dphiBoson2);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_detaBoson2", JetgoodPatJetsCA8PrunedPF_detaBoson2, &b_JetgoodPatJetsCA8PrunedPF_detaBoson2);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_dRBoson2", JetgoodPatJetsCA8PrunedPF_dRBoson2, &b_JetgoodPatJetsCA8PrunedPF_dRBoson2);
    fChain->SetBranchAddress("VplusgoodPatJetsCA8PrunedPFJet_Mass2", VplusgoodPatJetsCA8PrunedPFJet_Mass2, &b_VplusgoodPatJetsCA8PrunedPFJet_Mass2);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PrunedPF_Response2", JetgoodPatJetsCA8PrunedPF_Response2, &b_JetgoodPatJetsCA8PrunedPF_Response2);
    fChain->SetBranchAddress("numgoodPatJetsCA8PFJets", &numgoodPatJetsCA8PFJets, &b_numgoodPatJetsCA8PFJets);
    fChain->SetBranchAddress("numgoodPatJetsCA8PFJetBTags", &numgoodPatJetsCA8PFJetBTags, &b_numgoodPatJetsCA8PFJetBTags);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_Et", JetgoodPatJetsCA8PF_Et, &b_JetgoodPatJetsCA8PF_Et);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_Pt", JetgoodPatJetsCA8PF_Pt, &b_JetgoodPatJetsCA8PF_Pt);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_Eta", JetgoodPatJetsCA8PF_Eta, &b_JetgoodPatJetsCA8PF_Eta);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_Phi", JetgoodPatJetsCA8PF_Phi, &b_JetgoodPatJetsCA8PF_Phi);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_Theta", JetgoodPatJetsCA8PF_Theta, &b_JetgoodPatJetsCA8PF_Theta);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_Px", JetgoodPatJetsCA8PF_Px, &b_JetgoodPatJetsCA8PF_Px);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_Py", JetgoodPatJetsCA8PF_Py, &b_JetgoodPatJetsCA8PF_Py);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_Pz", JetgoodPatJetsCA8PF_Pz, &b_JetgoodPatJetsCA8PF_Pz);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_E", JetgoodPatJetsCA8PF_E, &b_JetgoodPatJetsCA8PF_E);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_Y", JetgoodPatJetsCA8PF_Y, &b_JetgoodPatJetsCA8PF_Y);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_Mass", JetgoodPatJetsCA8PF_Mass, &b_JetgoodPatJetsCA8PF_Mass);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_nJetDaughters", JetgoodPatJetsCA8PF_nJetDaughters, &b_JetgoodPatJetsCA8PF_nJetDaughters);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_subJet1Mass", JetgoodPatJetsCA8PF_subJet1Mass, &b_JetgoodPatJetsCA8PF_subJet1Mass);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_subJet2Mass", JetgoodPatJetsCA8PF_subJet2Mass, &b_JetgoodPatJetsCA8PF_subJet2Mass);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_etaetaMoment", JetgoodPatJetsCA8PF_etaetaMoment, &b_JetgoodPatJetsCA8PF_etaetaMoment);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_phiphiMoment", JetgoodPatJetsCA8PF_phiphiMoment, &b_JetgoodPatJetsCA8PF_phiphiMoment);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_etaphiMoment", JetgoodPatJetsCA8PF_etaphiMoment, &b_JetgoodPatJetsCA8PF_etaphiMoment);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_maxDistance", JetgoodPatJetsCA8PF_maxDistance, &b_JetgoodPatJetsCA8PF_maxDistance);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_nConstituents", JetgoodPatJetsCA8PF_nConstituents, &b_JetgoodPatJetsCA8PF_nConstituents);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_Area", JetgoodPatJetsCA8PF_Area, &b_JetgoodPatJetsCA8PF_Area);
    fChain->SetBranchAddress("VplusgoodPatJetsCA8PFJet_Mass", VplusgoodPatJetsCA8PFJet_Mass, &b_VplusgoodPatJetsCA8PFJet_Mass);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_dphiBoson", JetgoodPatJetsCA8PF_dphiBoson, &b_JetgoodPatJetsCA8PF_dphiBoson);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_detaBoson", JetgoodPatJetsCA8PF_detaBoson, &b_JetgoodPatJetsCA8PF_detaBoson);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_dRBoson", JetgoodPatJetsCA8PF_dRBoson, &b_JetgoodPatJetsCA8PF_dRBoson);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_dphiMET", JetgoodPatJetsCA8PF_dphiMET, &b_JetgoodPatJetsCA8PF_dphiMET);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_Response", JetgoodPatJetsCA8PF_Response, &b_JetgoodPatJetsCA8PF_Response);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_bDiscriminator", JetgoodPatJetsCA8PF_bDiscriminator, &b_JetgoodPatJetsCA8PF_bDiscriminator);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_bDiscriminatorSSVHE", JetgoodPatJetsCA8PF_bDiscriminatorSSVHE, &b_JetgoodPatJetsCA8PF_bDiscriminatorSSVHE);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_bDiscriminatorTCHE", JetgoodPatJetsCA8PF_bDiscriminatorTCHE, &b_JetgoodPatJetsCA8PF_bDiscriminatorTCHE);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_bDiscriminatorCSV", JetgoodPatJetsCA8PF_bDiscriminatorCSV, &b_JetgoodPatJetsCA8PF_bDiscriminatorCSV);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_bDiscriminatorJP", JetgoodPatJetsCA8PF_bDiscriminatorJP, &b_JetgoodPatJetsCA8PF_bDiscriminatorJP);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_bDiscriminatorSSVHP", JetgoodPatJetsCA8PF_bDiscriminatorSSVHP, &b_JetgoodPatJetsCA8PF_bDiscriminatorSSVHP);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_bDiscriminatorTCHP", JetgoodPatJetsCA8PF_bDiscriminatorTCHP, &b_JetgoodPatJetsCA8PF_bDiscriminatorTCHP);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_secVertexMass", JetgoodPatJetsCA8PF_secVertexMass, &b_JetgoodPatJetsCA8PF_secVertexMass);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_dphiBoson2", JetgoodPatJetsCA8PF_dphiBoson2, &b_JetgoodPatJetsCA8PF_dphiBoson2);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_detaBoson2", JetgoodPatJetsCA8PF_detaBoson2, &b_JetgoodPatJetsCA8PF_detaBoson2);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_dRBoson2", JetgoodPatJetsCA8PF_dRBoson2, &b_JetgoodPatJetsCA8PF_dRBoson2);
    fChain->SetBranchAddress("VplusgoodPatJetsCA8PFJet_Mass2", VplusgoodPatJetsCA8PFJet_Mass2, &b_VplusgoodPatJetsCA8PFJet_Mass2);
    fChain->SetBranchAddress("JetgoodPatJetsCA8PF_Response2", JetgoodPatJetsCA8PF_Response2, &b_JetgoodPatJetsCA8PF_Response2);
    fChain->SetBranchAddress("event_runNo", &event_runNo, &b_event_runNo);
    fChain->SetBranchAddress("event_evtNo", &event_evtNo, &b_event_evtNo);
    fChain->SetBranchAddress("event_lumi", &event_lumi, &b_event_lumi);
    fChain->SetBranchAddress("event_bunch", &event_bunch, &b_event_bunch);
    fChain->SetBranchAddress("event_nPV", &event_nPV, &b_event_nPV);
    fChain->SetBranchAddress("event_PVx", event_PVx, &b_event_PVx);
    fChain->SetBranchAddress("event_PVy", event_PVy, &b_event_PVy);
    fChain->SetBranchAddress("event_PVz", event_PVz, &b_event_PVz);
    fChain->SetBranchAddress("event_met_pfmet", &event_met_pfmet, &b_event_met_pfmet);
    fChain->SetBranchAddress("event_met_pfsumet", &event_met_pfsumet, &b_event_met_pfsumet);
    fChain->SetBranchAddress("event_met_pfmetsignificance", &event_met_pfmetsignificance, &b_event_met_pfmetsignificance);
    fChain->SetBranchAddress("event_met_pfmetPhi", &event_met_pfmetPhi, &b_event_met_pfmetPhi);
    fChain->SetBranchAddress("event_fastJetRho", &event_fastJetRho, &b_event_fastJetRho);
    fChain->SetBranchAddress("event_RhoForLeptonIsolation", &event_RhoForLeptonIsolation, &b_event_RhoForLeptonIsolation);
    fChain->SetBranchAddress("event_BeamSpot_x", &event_BeamSpot_x, &b_event_BeamSpot_x);
    fChain->SetBranchAddress("event_BeamSpot_y", &event_BeamSpot_y, &b_event_BeamSpot_y);
    fChain->SetBranchAddress("event_BeamSpot_z", &event_BeamSpot_z, &b_event_BeamSpot_z);
    fChain->SetBranchAddress("numW", &numW, &b_numW);
    fChain->SetBranchAddress("event_met_genmet", &event_met_genmet, &b_event_met_genmet);
    fChain->SetBranchAddress("event_met_gensumet", &event_met_gensumet, &b_event_met_gensumet);
    fChain->SetBranchAddress("event_met_genmetsignificance", &event_met_genmetsignificance, &b_event_met_genmetsignificance);
    fChain->SetBranchAddress("event_met_genmetPhi", &event_met_genmetPhi, &b_event_met_genmetPhi);
    fChain->SetBranchAddress("event_mcPU_totnvtx", &event_mcPU_totnvtx, &b_event_mcPU_totnvtx);
    fChain->SetBranchAddress("event_mcPU_bx", event_mcPU_bx, &b_event_mcPU_bx);
    fChain->SetBranchAddress("event_mcPU_nvtx", event_mcPU_nvtx, &b_event_mcPU_nvtx);
    Notify();
}

Bool_t vJetSubstructure::Notify()
{
    // The Notify() function is called when a new file is opened. This
    // can be either for a new TTree in a TChain or when when a new TTree
    // is started when using PROOF. It is normally not necessary to make changes
    // to the generated code, but the routine can be extended by the
    // user if needed. The return value is currently not used.
    
    return kTRUE;
}

void vJetSubstructure::Show(Long64_t entry)
{
    // Print contents of entry.
    // If entry is not specified, print current entry
    if (!fChain) return;
    fChain->Show(entry);
}
Int_t vJetSubstructure::Cut(Long64_t entry)
{
    // This function may be called from Loop.
    // returns  1 if entry is accepted.
    // returns -1 otherwise.
    return 1;
}
#endif // #ifdef vJetSubstructure_cxx
