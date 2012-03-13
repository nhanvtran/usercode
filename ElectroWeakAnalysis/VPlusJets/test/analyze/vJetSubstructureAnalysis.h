//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Mon Mar 12 11:14:34 2012 by ROOT version 5.27/06b
// from TTree VJetSubstructure/V+jets Tree
// found on file: /eos/uscms/store/user/ntran/smpjs/v10_v2/ww_vjet/outputCrabMC_ww.root
//////////////////////////////////////////////////////////

#ifndef vJetSubstructureAnalysis_h
#define vJetSubstructureAnalysis_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

class vJetSubstructureAnalysis {
    public :
    
    TFile* fout;
    TTree* otree;
    
    TTree          *fChain;   //!pointer to the analyzed TTree or TChain
    Int_t           fCurrent; //!current Tree number in a TChain
    
    double j_ak5_bdis, j_ak5_eta, j_ak5_phi, j_ak5_pt, j_ak5_mass, j_ak5_area, j_ak5_nJ, j_ak5_mu, j_ak5_p;
    double j_ak5tr_mass;
    double j_ak5pr_mass;
    double j_ak5ft_mass;
    double j_ak7_mass;
    double j_ak7tr_mass;
    double j_ak7pr_mass;
    double j_ak7ft_mass;
    double j_ca8_mass;    
    double j_ca8pr_mass;
    
    double e_nvert, l_pt, l_reliso, e_met, e_weight, w_mt, w_pt;
    double e_puwt, e_puwt_up, e_puwt_dn, e_effwt;
    
    // Declaration of leaf types
    Float_t         Wel_mass;
    Float_t         Wel_mt;
    Float_t         Wel_px;
    Float_t         Wel_py;
    Float_t         Wel_pz;
    Float_t         Wel_e;
    Float_t         Wel_pt;
    Float_t         Wel_et;
    Float_t         Wel_eta;
    Float_t         Wel_phi;
    Float_t         Wel_vx;
    Float_t         Wel_vy;
    Float_t         Wel_vz;
    Float_t         Wel_y;
    Int_t           Wel_numTightElectrons;
    Int_t           Wel_numLooseElectrons;
    Float_t         Wel_pzNu1;
    Float_t         Wel_pzNu2;
    Float_t         Wel_electron_px;
    Float_t         Wel_electron_py;
    Float_t         Wel_electron_pz;
    Float_t         Wel_electron_e;
    Float_t         Wel_electron_pt;
    Float_t         Wel_electron_et;
    Float_t         Wel_electron_eta;
    Float_t         Wel_electron_theta;
    Float_t         Wel_electron_phi;
    Int_t           Wel_electron_charge;
    Float_t         Wel_electron_vx;
    Float_t         Wel_electron_vy;
    Float_t         Wel_electron_vz;
    Float_t         Wel_electron_y;
    Float_t         Wel_electron_trackiso;
    Float_t         Wel_electron_hcaliso;
    Float_t         Wel_electron_ecaliso;
    Int_t           Wel_electron_classification;
    Bool_t          Wel_electron_isWP95;
    Bool_t          Wel_electron_isWP80;
    Bool_t          Wel_electron_isWP70;
    Float_t         Zel_mass;
    Float_t         Zel_mt;
    Float_t         Zel_px;
    Float_t         Zel_py;
    Float_t         Zel_pz;
    Float_t         Zel_e;
    Float_t         Zel_pt;
    Float_t         Zel_et;
    Float_t         Zel_eta;
    Float_t         Zel_phi;
    Float_t         Zel_vx;
    Float_t         Zel_vy;
    Float_t         Zel_vz;
    Float_t         Zel_y;
    Int_t           Zel_numTightElectrons;
    Int_t           Zel_numLooseElectrons;
    Float_t         Zel_eplus_px;
    Float_t         Zel_eplus_py;
    Float_t         Zel_eplus_pz;
    Float_t         Zel_eplus_e;
    Float_t         Zel_eplus_pt;
    Float_t         Zel_eplus_et;
    Float_t         Zel_eplus_eta;
    Float_t         Zel_eplus_theta;
    Float_t         Zel_eplus_phi;
    Int_t           Zel_eplus_charge;
    Float_t         Zel_eplus_vx;
    Float_t         Zel_eplus_vy;
    Float_t         Zel_eplus_vz;
    Float_t         Zel_eplus_y;
    Float_t         Zel_eplus_trackiso;
    Float_t         Zel_eplus_hcaliso;
    Float_t         Zel_eplus_ecaliso;
    Int_t           Zel_eplus_classification;
    Bool_t          Zel_eplus_isWP95;
    Bool_t          Zel_eplus_isWP80;
    Bool_t          Zel_eplus_isWP70;
    Float_t         Zel_eminus_px;
    Float_t         Zel_eminus_py;
    Float_t         Zel_eminus_pz;
    Float_t         Zel_eminus_e;
    Float_t         Zel_eminus_pt;
    Float_t         Zel_eminus_et;
    Float_t         Zel_eminus_eta;
    Float_t         Zel_eminus_theta;
    Float_t         Zel_eminus_phi;
    Int_t           Zel_eminus_charge;
    Float_t         Zel_eminus_vx;
    Float_t         Zel_eminus_vy;
    Float_t         Zel_eminus_vz;
    Float_t         Zel_eminus_y;
    Float_t         Zel_eminus_trackiso;
    Float_t         Zel_eminus_hcaliso;
    Float_t         Zel_eminus_ecaliso;
    Bool_t          Zel_eminus_isWP95;
    Bool_t          Zel_eminus_isWP80;
    Bool_t          Zel_eminus_isWP70;
    Float_t         Wmu_mass;
    Float_t         Wmu_mt;
    Float_t         Wmu_px;
    Float_t         Wmu_py;
    Float_t         Wmu_pz;
    Float_t         Wmu_e;
    Float_t         Wmu_pt;
    Float_t         Wmu_et;
    Float_t         Wmu_eta;
    Float_t         Wmu_phi;
    Float_t         Wmu_vx;
    Float_t         Wmu_vy;
    Float_t         Wmu_vz;
    Float_t         Wmu_y;
    Float_t         Wmu_pzNu1;
    Float_t         Wmu_pzNu2;
    Float_t         Wmu_muon_px;
    Float_t         Wmu_muon_py;
    Float_t         Wmu_muon_pz;
    Float_t         Wmu_muon_e;
    Float_t         Wmu_muon_pt;
    Float_t         Wmu_muon_et;
    Float_t         Wmu_muon_eta;
    Float_t         Wmu_muon_theta;
    Float_t         Wmu_muon_phi;
    Int_t           Wmu_muon_charge;
    Float_t         Wmu_muon_vx;
    Float_t         Wmu_muon_vy;
    Float_t         Wmu_muon_vz;
    Float_t         Wmu_muon_y;
    Float_t         Wmu_muon_trackiso;
    Float_t         Wmu_muon_hcaliso;
    Float_t         Wmu_muon_ecaliso;
    Int_t           Wmu_muon_type;
    Int_t           Wmu_muon_numberOfChambers;
    Int_t           Wmu_muon_numberOfMatches;
    Float_t         Wmu_muon_d0bsp;
    Float_t         Wmu_muon_dz000;
    Float_t         Wmu_muon_pfiso_sumChargedHadronPt;
    Float_t         Wmu_muon_pfiso_sumChargedParticlePt;
    Float_t         Wmu_muon_pfiso_sumNeutralHadronEt;
    Float_t         Wmu_muon_pfiso_sumPhotonEt;
    Float_t         Wmu_muon_pfiso_sumPUPt;
    Float_t         Zmu_mass;
    Float_t         Zmu_mt;
    Float_t         Zmu_px;
    Float_t         Zmu_py;
    Float_t         Zmu_pz;
    Float_t         Zmu_e;
    Float_t         Zmu_pt;
    Float_t         Zmu_et;
    Float_t         Zmu_eta;
    Float_t         Zmu_phi;
    Float_t         Zmu_vx;
    Float_t         Zmu_vy;
    Float_t         Zmu_vz;
    Float_t         Zmu_y;
    Float_t         Zmu_muplus_px;
    Float_t         Zmu_muplus_py;
    Float_t         Zmu_muplus_pz;
    Float_t         Zmu_muplus_e;
    Float_t         Zmu_muplus_pt;
    Float_t         Zmu_muplus_et;
    Float_t         Zmu_muplus_eta;
    Float_t         Zmu_muplus_theta;
    Float_t         Zmu_muplus_phi;
    Int_t           Zmu_muplus_charge;
    Float_t         Zmu_muplus_vx;
    Float_t         Zmu_muplus_vy;
    Float_t         Zmu_muplus_vz;
    Float_t         Zmu_muplus_y;
    Float_t         Zmu_muplus_trackiso;
    Float_t         Zmu_muplus_hcaliso;
    Float_t         Zmu_muplus_ecaliso;
    Int_t           Zmu_muplus_type;
    Int_t           Zmu_muplus_numberOfChambers;
    Int_t           Zmu_muplus_numberOfMatches;
    Float_t         Zmu_muplus_d0bsp;
    Float_t         Zmu_muplus_dz000;
    Float_t         Zmu_muplus_pfiso_sumChargedHadronPt;
    Float_t         Zmu_muplus_pfiso_sumChargedParticlePt;
    Float_t         Zmu_muplus_pfiso_sumNeutralHadronEt;
    Float_t         Zmu_muplus_pfiso_sumPhotonEt;
    Float_t         Zmu_muplus_pfiso_sumPUPt;
    Float_t         Zmu_muminus_px;
    Float_t         Zmu_muminus_py;
    Float_t         Zmu_muminus_pz;
    Float_t         Zmu_muminus_e;
    Float_t         Zmu_muminus_pt;
    Float_t         Zmu_muminus_et;
    Float_t         Zmu_muminus_eta;
    Float_t         Zmu_muminus_theta;
    Float_t         Zmu_muminus_phi;
    Int_t           Zmu_muminus_charge;
    Float_t         Zmu_muminus_vx;
    Float_t         Zmu_muminus_vy;
    Float_t         Zmu_muminus_vz;
    Float_t         Zmu_muminus_y;
    Float_t         Zmu_muminus_trackiso;
    Float_t         Zmu_muminus_hcaliso;
    Float_t         Zmu_muminus_ecaliso;
    Int_t           Zmu_muminus_type;
    Int_t           Zmu_muminus_numberOfChambers;
    Int_t           Zmu_muminus_numberOfMatches;
    Int_t           JetAK5PF_nJets;
    Float_t         JetAK5PF_Et[6];
    Float_t         JetAK5PF_Pt[6];
    Float_t         JetAK5PF_Eta[6];
    Float_t         JetAK5PF_Phi[6];
    Float_t         JetAK5PF_Theta[6];
    Float_t         JetAK5PF_Px[6];
    Float_t         JetAK5PF_Py[6];
    Float_t         JetAK5PF_Pz[6];
    Float_t         JetAK5PF_E[6];
    Float_t         JetAK5PF_Y[6];
    Float_t         JetAK5PF_Mass[6];
    Float_t         JetAK5PF_Area[6];
    Int_t           JetAK5PF_nJetBTags;
    Int_t           JetAK5PF_nDau[6];
    Float_t         JetAK5PF_bDiscSSVHE[6];
    Float_t         JetAK5PF_bDiscTCHE[6];
    Float_t         JetAK5PF_bDiscrCSV[6];
    Float_t         JetAK5PF_bDiscJP[6];
    Float_t         JetAK5PF_bDiscrSSVHP[6];
    Float_t         JetAK5PF_bDiscTCHP[6];
    Int_t           JetCA8PRUNEDPF_nJets;
    Float_t         JetCA8PRUNEDPF_Et[6];
    Float_t         JetCA8PRUNEDPF_Pt[6];
    Float_t         JetCA8PRUNEDPF_Eta[6];
    Float_t         JetCA8PRUNEDPF_Phi[6];
    Float_t         JetCA8PRUNEDPF_Theta[6];
    Float_t         JetCA8PRUNEDPF_Px[6];
    Float_t         JetCA8PRUNEDPF_Py[6];
    Float_t         JetCA8PRUNEDPF_Pz[6];
    Float_t         JetCA8PRUNEDPF_E[6];
    Float_t         JetCA8PRUNEDPF_Y[6];
    Float_t         JetCA8PRUNEDPF_Mass[6];
    Float_t         JetCA8PRUNEDPF_Area[6];
    Int_t           JetCA8PRUNEDPF_nJetBTags;
    Int_t           JetCA8PRUNEDPF_nDau[6];
    Float_t         JetCA8PRUNEDPF_bDiscSSVHE[6];
    Float_t         JetCA8PRUNEDPF_bDiscTCHE[6];
    Float_t         JetCA8PRUNEDPF_bDiscrCSV[6];
    Float_t         JetCA8PRUNEDPF_bDiscJP[6];
    Float_t         JetCA8PRUNEDPF_bDiscrSSVHP[6];
    Float_t         JetCA8PRUNEDPF_bDiscTCHP[6];
    Float_t         JetCA8PRUNEDPF_subJet1Mass[6];
    Float_t         JetCA8PRUNEDPF_subJet2Mass[6];
    Int_t           JetCA8PF_nJets;
    Float_t         JetCA8PF_Et[6];
    Float_t         JetCA8PF_Pt[6];
    Float_t         JetCA8PF_Eta[6];
    Float_t         JetCA8PF_Phi[6];
    Float_t         JetCA8PF_Theta[6];
    Float_t         JetCA8PF_Px[6];
    Float_t         JetCA8PF_Py[6];
    Float_t         JetCA8PF_Pz[6];
    Float_t         JetCA8PF_E[6];
    Float_t         JetCA8PF_Y[6];
    Float_t         JetCA8PF_Mass[6];
    Float_t         JetCA8PF_Area[6];
    Int_t           JetCA8PF_nJetBTags;
    Int_t           JetCA8PF_nDau[6];
    Float_t         JetCA8PF_bDiscSSVHE[6];
    Float_t         JetCA8PF_bDiscTCHE[6];
    Float_t         JetCA8PF_bDiscrCSV[6];
    Float_t         JetCA8PF_bDiscJP[6];
    Float_t         JetCA8PF_bDiscrSSVHP[6];
    Float_t         JetCA8PF_bDiscTCHP[6];
    Int_t           JetAK5TRIMMEDPF_nJets;
    Float_t         JetAK5TRIMMEDPF_Et[6];
    Float_t         JetAK5TRIMMEDPF_Pt[6];
    Float_t         JetAK5TRIMMEDPF_Eta[6];
    Float_t         JetAK5TRIMMEDPF_Phi[6];
    Float_t         JetAK5TRIMMEDPF_Theta[6];
    Float_t         JetAK5TRIMMEDPF_Px[6];
    Float_t         JetAK5TRIMMEDPF_Py[6];
    Float_t         JetAK5TRIMMEDPF_Pz[6];
    Float_t         JetAK5TRIMMEDPF_E[6];
    Float_t         JetAK5TRIMMEDPF_Y[6];
    Float_t         JetAK5TRIMMEDPF_Mass[6];
    Float_t         JetAK5TRIMMEDPF_Area[6];
    Int_t           JetAK5FILTEREDPF_nJets;
    Float_t         JetAK5FILTEREDPF_Et[6];
    Float_t         JetAK5FILTEREDPF_Pt[6];
    Float_t         JetAK5FILTEREDPF_Eta[6];
    Float_t         JetAK5FILTEREDPF_Phi[6];
    Float_t         JetAK5FILTEREDPF_Theta[6];
    Float_t         JetAK5FILTEREDPF_Px[6];
    Float_t         JetAK5FILTEREDPF_Py[6];
    Float_t         JetAK5FILTEREDPF_Pz[6];
    Float_t         JetAK5FILTEREDPF_E[6];
    Float_t         JetAK5FILTEREDPF_Y[6];
    Float_t         JetAK5FILTEREDPF_Mass[6];
    Float_t         JetAK5FILTEREDPF_Area[6];
    Int_t           JetAK5PRUNEDPF_nJets;
    Float_t         JetAK5PRUNEDPF_Et[6];
    Float_t         JetAK5PRUNEDPF_Pt[6];
    Float_t         JetAK5PRUNEDPF_Eta[6];
    Float_t         JetAK5PRUNEDPF_Phi[6];
    Float_t         JetAK5PRUNEDPF_Theta[6];
    Float_t         JetAK5PRUNEDPF_Px[6];
    Float_t         JetAK5PRUNEDPF_Py[6];
    Float_t         JetAK5PRUNEDPF_Pz[6];
    Float_t         JetAK5PRUNEDPF_E[6];
    Float_t         JetAK5PRUNEDPF_Y[6];
    Float_t         JetAK5PRUNEDPF_Mass[6];
    Float_t         JetAK5PRUNEDPF_Area[6];
    Int_t           JetAK7TRIMMEDPF_nJets;
    Float_t         JetAK7TRIMMEDPF_Et[6];
    Float_t         JetAK7TRIMMEDPF_Pt[6];
    Float_t         JetAK7TRIMMEDPF_Eta[6];
    Float_t         JetAK7TRIMMEDPF_Phi[6];
    Float_t         JetAK7TRIMMEDPF_Theta[6];
    Float_t         JetAK7TRIMMEDPF_Px[6];
    Float_t         JetAK7TRIMMEDPF_Py[6];
    Float_t         JetAK7TRIMMEDPF_Pz[6];
    Float_t         JetAK7TRIMMEDPF_E[6];
    Float_t         JetAK7TRIMMEDPF_Y[6];
    Float_t         JetAK7TRIMMEDPF_Mass[6];
    Float_t         JetAK7TRIMMEDPF_Area[6];
    Int_t           JetAK7FILTEREDPF_nJets;
    Float_t         JetAK7FILTEREDPF_Et[6];
    Float_t         JetAK7FILTEREDPF_Pt[6];
    Float_t         JetAK7FILTEREDPF_Eta[6];
    Float_t         JetAK7FILTEREDPF_Phi[6];
    Float_t         JetAK7FILTEREDPF_Theta[6];
    Float_t         JetAK7FILTEREDPF_Px[6];
    Float_t         JetAK7FILTEREDPF_Py[6];
    Float_t         JetAK7FILTEREDPF_Pz[6];
    Float_t         JetAK7FILTEREDPF_E[6];
    Float_t         JetAK7FILTEREDPF_Y[6];
    Float_t         JetAK7FILTEREDPF_Mass[6];
    Float_t         JetAK7FILTEREDPF_Area[6];
    Int_t           JetAK7PRUNEDPF_nJets;
    Float_t         JetAK7PRUNEDPF_Et[6];
    Float_t         JetAK7PRUNEDPF_Pt[6];
    Float_t         JetAK7PRUNEDPF_Eta[6];
    Float_t         JetAK7PRUNEDPF_Phi[6];
    Float_t         JetAK7PRUNEDPF_Theta[6];
    Float_t         JetAK7PRUNEDPF_Px[6];
    Float_t         JetAK7PRUNEDPF_Py[6];
    Float_t         JetAK7PRUNEDPF_Pz[6];
    Float_t         JetAK7PRUNEDPF_E[6];
    Float_t         JetAK7PRUNEDPF_Y[6];
    Float_t         JetAK7PRUNEDPF_Mass[6];
    Float_t         JetAK7PRUNEDPF_Area[6];
    Int_t           JetAK5GENJETSNONU_nJets;
    Float_t         JetAK5GENJETSNONU_Et[6];
    Float_t         JetAK5GENJETSNONU_Pt[6];
    Float_t         JetAK5GENJETSNONU_Eta[6];
    Float_t         JetAK5GENJETSNONU_Phi[6];
    Float_t         JetAK5GENJETSNONU_Theta[6];
    Float_t         JetAK5GENJETSNONU_Px[6];
    Float_t         JetAK5GENJETSNONU_Py[6];
    Float_t         JetAK5GENJETSNONU_Pz[6];
    Float_t         JetAK5GENJETSNONU_E[6];
    Float_t         JetAK5GENJETSNONU_Y[6];
    Float_t         JetAK5GENJETSNONU_Mass[6];
    Float_t         JetAK5GENJETSNONU_Area[6];
    Int_t           JetAK7GENJETSNONU_nJets;
    Float_t         JetAK7GENJETSNONU_Et[6];
    Float_t         JetAK7GENJETSNONU_Pt[6];
    Float_t         JetAK7GENJETSNONU_Eta[6];
    Float_t         JetAK7GENJETSNONU_Phi[6];
    Float_t         JetAK7GENJETSNONU_Theta[6];
    Float_t         JetAK7GENJETSNONU_Px[6];
    Float_t         JetAK7GENJETSNONU_Py[6];
    Float_t         JetAK7GENJETSNONU_Pz[6];
    Float_t         JetAK7GENJETSNONU_E[6];
    Float_t         JetAK7GENJETSNONU_Y[6];
    Float_t         JetAK7GENJETSNONU_Mass[6];
    Float_t         JetAK7GENJETSNONU_Area[6];
    Int_t           JetCA8GENJETSNONU_nJets;
    Float_t         JetCA8GENJETSNONU_Et[6];
    Float_t         JetCA8GENJETSNONU_Pt[6];
    Float_t         JetCA8GENJETSNONU_Eta[6];
    Float_t         JetCA8GENJETSNONU_Phi[6];
    Float_t         JetCA8GENJETSNONU_Theta[6];
    Float_t         JetCA8GENJETSNONU_Px[6];
    Float_t         JetCA8GENJETSNONU_Py[6];
    Float_t         JetCA8GENJETSNONU_Pz[6];
    Float_t         JetCA8GENJETSNONU_E[6];
    Float_t         JetCA8GENJETSNONU_Y[6];
    Float_t         JetCA8GENJETSNONU_Mass[6];
    Float_t         JetCA8GENJETSNONU_Area[6];
    Int_t           event_runNo;
    Int_t           event_evtNo;
    Int_t           event_lumi;
    Int_t           event_bunch;
    Int_t           event_nPV;
    Float_t         event_PVx[30];
    Float_t         event_PVy[30];
    Float_t         event_PVz[30];
    Int_t           eventClass;
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
    TBranch        *b_Wel_mass;   //!
    TBranch        *b_Wel_mt;   //!
    TBranch        *b_Wel_px;   //!
    TBranch        *b_Wel_py;   //!
    TBranch        *b_Wel_pz;   //!
    TBranch        *b_Wel_e;   //!
    TBranch        *b_Wel_pt;   //!
    TBranch        *b_Wel_et;   //!
    TBranch        *b_Wel_eta;   //!
    TBranch        *b_Wel_phi;   //!
    TBranch        *b_Wel_vx;   //!
    TBranch        *b_Wel_vy;   //!
    TBranch        *b_Wel_vz;   //!
    TBranch        *b_Wel_y;   //!
    TBranch        *b_Wel_numTightElectrons;   //!
    TBranch        *b_Wel_numLooseElectrons;   //!
    TBranch        *b_Wel_pzNu1;   //!
    TBranch        *b_Wel_pzNu2;   //!
    TBranch        *b_Wel_electron_px;   //!
    TBranch        *b_Wel_electron_py;   //!
    TBranch        *b_Wel_electron_pz;   //!
    TBranch        *b_Wel_electron_e;   //!
    TBranch        *b_Wel_electron_pt;   //!
    TBranch        *b_Wel_electron_et;   //!
    TBranch        *b_Wel_electron_eta;   //!
    TBranch        *b_Wel_electron_theta;   //!
    TBranch        *b_Wel_electron_phi;   //!
    TBranch        *b_Wel_electron_charge;   //!
    TBranch        *b_Wel_electron_vx;   //!
    TBranch        *b_Wel_electron_vy;   //!
    TBranch        *b_Wel_electron_vz;   //!
    TBranch        *b_Wel_electron_y;   //!
    TBranch        *b_Wel_electron_trackiso;   //!
    TBranch        *b_Wel_electron_hcaliso;   //!
    TBranch        *b_Wel_electron_ecaliso;   //!
    TBranch        *b_Wel_electron_classification;   //!
    TBranch        *b_Wel_electron_isWP95;   //!
    TBranch        *b_Wel_electron_isWP80;   //!
    TBranch        *b_Wel_electron_isWP70;   //!
    TBranch        *b_Zel_mass;   //!
    TBranch        *b_Zel_mt;   //!
    TBranch        *b_Zel_px;   //!
    TBranch        *b_Zel_py;   //!
    TBranch        *b_Zel_pz;   //!
    TBranch        *b_Zel_e;   //!
    TBranch        *b_Zel_pt;   //!
    TBranch        *b_Zel_et;   //!
    TBranch        *b_Zel_eta;   //!
    TBranch        *b_Zel_phi;   //!
    TBranch        *b_Zel_vx;   //!
    TBranch        *b_Zel_vy;   //!
    TBranch        *b_Zel_vz;   //!
    TBranch        *b_Zel_y;   //!
    TBranch        *b_Zel_numTightElectrons;   //!
    TBranch        *b_Zel_numLooseElectrons;   //!
    TBranch        *b_Zel_eplus_px;   //!
    TBranch        *b_Zel_eplus_py;   //!
    TBranch        *b_Zel_eplus_pz;   //!
    TBranch        *b_Zel_eplus_e;   //!
    TBranch        *b_Zel_eplus_pt;   //!
    TBranch        *b_Zel_eplus_et;   //!
    TBranch        *b_Zel_eplus_eta;   //!
    TBranch        *b_Zel_eplus_theta;   //!
    TBranch        *b_Zel_eplus_phi;   //!
    TBranch        *b_Zel_eplus_charge;   //!
    TBranch        *b_Zel_eplus_vx;   //!
    TBranch        *b_Zel_eplus_vy;   //!
    TBranch        *b_Zel_eplus_vz;   //!
    TBranch        *b_Zel_eplus_y;   //!
    TBranch        *b_Zel_eplus_trackiso;   //!
    TBranch        *b_Zel_eplus_hcaliso;   //!
    TBranch        *b_Zel_eplus_ecaliso;   //!
    TBranch        *b_Zel_eplus_classification;   //!
    TBranch        *b_Zel_eplus_isWP95;   //!
    TBranch        *b_Zel_eplus_isWP80;   //!
    TBranch        *b_Zel_eplus_isWP70;   //!
    TBranch        *b_Zel_eminus_px;   //!
    TBranch        *b_Zel_eminus_py;   //!
    TBranch        *b_Zel_eminus_pz;   //!
    TBranch        *b_Zel_eminus_e;   //!
    TBranch        *b_Zel_eminus_pt;   //!
    TBranch        *b_Zel_eminus_et;   //!
    TBranch        *b_Zel_eminus_eta;   //!
    TBranch        *b_Zel_eminus_theta;   //!
    TBranch        *b_Zel_eminus_phi;   //!
    TBranch        *b_Zel_eminus_charge;   //!
    TBranch        *b_Zel_eminus_vx;   //!
    TBranch        *b_Zel_eminus_vy;   //!
    TBranch        *b_Zel_eminus_vz;   //!
    TBranch        *b_Zel_eminus_y;   //!
    TBranch        *b_Zel_eminus_trackiso;   //!
    TBranch        *b_Zel_eminus_hcaliso;   //!
    TBranch        *b_Zel_eminus_ecaliso;   //!
    TBranch        *b_Zel_eminus_isWP95;   //!
    TBranch        *b_Zel_eminus_isWP80;   //!
    TBranch        *b_Zel_eminus_isWP70;   //!
    TBranch        *b_Wmu_mass;   //!
    TBranch        *b_Wmu_mt;   //!
    TBranch        *b_Wmu_px;   //!
    TBranch        *b_Wmu_py;   //!
    TBranch        *b_Wmu_pz;   //!
    TBranch        *b_Wmu_e;   //!
    TBranch        *b_Wmu_pt;   //!
    TBranch        *b_Wmu_et;   //!
    TBranch        *b_Wmu_eta;   //!
    TBranch        *b_Wmu_phi;   //!
    TBranch        *b_Wmu_vx;   //!
    TBranch        *b_Wmu_vy;   //!
    TBranch        *b_Wmu_vz;   //!
    TBranch        *b_Wmu_y;   //!
    TBranch        *b_Wmu_pzNu1;   //!
    TBranch        *b_Wmu_pzNu2;   //!
    TBranch        *b_Wmu_muon_px;   //!
    TBranch        *b_Wmu_muon_py;   //!
    TBranch        *b_Wmu_muon_pz;   //!
    TBranch        *b_Wmu_muon_e;   //!
    TBranch        *b_Wmu_muon_pt;   //!
    TBranch        *b_Wmu_muon_et;   //!
    TBranch        *b_Wmu_muon_eta;   //!
    TBranch        *b_Wmu_muon_theta;   //!
    TBranch        *b_Wmu_muon_phi;   //!
    TBranch        *b_Wmu_muon_charge;   //!
    TBranch        *b_Wmu_muon_vx;   //!
    TBranch        *b_Wmu_muon_vy;   //!
    TBranch        *b_Wmu_muon_vz;   //!
    TBranch        *b_Wmu_muon_y;   //!
    TBranch        *b_Wmu_muon_trackiso;   //!
    TBranch        *b_Wmu_muon_hcaliso;   //!
    TBranch        *b_Wmu_muon_ecaliso;   //!
    TBranch        *b_Wmu_muon_type;   //!
    TBranch        *b_Wmu_muon_numberOfChambers;   //!
    TBranch        *b_Wmu_muon_numberOfMatches;   //!
    TBranch        *b_Wmu_muon_d0bsp;   //!
    TBranch        *b_Wmu_muon_dz000;   //!
    TBranch        *b_Wmu_muon_pfiso_sumChargedHadronPt;   //!
    TBranch        *b_Wmu_muon_pfiso_sumChargedParticlePt;   //!
    TBranch        *b_Wmu_muon_pfiso_sumNeutralHadronEt;   //!
    TBranch        *b_Wmu_muon_pfiso_sumPhotonEt;   //!
    TBranch        *b_Wmu_muon_pfiso_sumPUPt;   //!
    TBranch        *b_Zmu_mass;   //!
    TBranch        *b_Zmu_mt;   //!
    TBranch        *b_Zmu_px;   //!
    TBranch        *b_Zmu_py;   //!
    TBranch        *b_Zmu_pz;   //!
    TBranch        *b_Zmu_e;   //!
    TBranch        *b_Zmu_pt;   //!
    TBranch        *b_Zmu_et;   //!
    TBranch        *b_Zmu_eta;   //!
    TBranch        *b_Zmu_phi;   //!
    TBranch        *b_Zmu_vx;   //!
    TBranch        *b_Zmu_vy;   //!
    TBranch        *b_Zmu_vz;   //!
    TBranch        *b_Zmu_y;   //!
    TBranch        *b_Zmu_muplus_px;   //!
    TBranch        *b_Zmu_muplus_py;   //!
    TBranch        *b_Zmu_muplus_pz;   //!
    TBranch        *b_Zmu_muplus_e;   //!
    TBranch        *b_Zmu_muplus_pt;   //!
    TBranch        *b_Zmu_muplus_et;   //!
    TBranch        *b_Zmu_muplus_eta;   //!
    TBranch        *b_Zmu_muplus_theta;   //!
    TBranch        *b_Zmu_muplus_phi;   //!
    TBranch        *b_Zmu_muplus_charge;   //!
    TBranch        *b_Zmu_muplus_vx;   //!
    TBranch        *b_Zmu_muplus_vy;   //!
    TBranch        *b_Zmu_muplus_vz;   //!
    TBranch        *b_Zmu_muplus_y;   //!
    TBranch        *b_Zmu_muplus_trackiso;   //!
    TBranch        *b_Zmu_muplus_hcaliso;   //!
    TBranch        *b_Zmu_muplus_ecaliso;   //!
    TBranch        *b_Zmu_muplus_type;   //!
    TBranch        *b_Zmu_muplus_numberOfChambers;   //!
    TBranch        *b_Zmu_muplus_numberOfMatches;   //!
    TBranch        *b_Zmu_muplus_d0bsp;   //!
    TBranch        *b_Zmu_muplus_dz000;   //!
    TBranch        *b_Zmu_muplus_pfiso_sumChargedHadronPt;   //!
    TBranch        *b_Zmu_muplus_pfiso_sumChargedParticlePt;   //!
    TBranch        *b_Zmu_muplus_pfiso_sumNeutralHadronEt;   //!
    TBranch        *b_Zmu_muplus_pfiso_sumPhotonEt;   //!
    TBranch        *b_Zmu_muplus_pfiso_sumPUPt;   //!
    TBranch        *b_Zmu_muminus_px;   //!
    TBranch        *b_Zmu_muminus_py;   //!
    TBranch        *b_Zmu_muminus_pz;   //!
    TBranch        *b_Zmu_muminus_e;   //!
    TBranch        *b_Zmu_muminus_pt;   //!
    TBranch        *b_Zmu_muminus_et;   //!
    TBranch        *b_Zmu_muminus_eta;   //!
    TBranch        *b_Zmu_muminus_theta;   //!
    TBranch        *b_Zmu_muminus_phi;   //!
    TBranch        *b_Zmu_muminus_charge;   //!
    TBranch        *b_Zmu_muminus_vx;   //!
    TBranch        *b_Zmu_muminus_vy;   //!
    TBranch        *b_Zmu_muminus_vz;   //!
    TBranch        *b_Zmu_muminus_y;   //!
    TBranch        *b_Zmu_muminus_trackiso;   //!
    TBranch        *b_Zmu_muminus_hcaliso;   //!
    TBranch        *b_Zmu_muminus_ecaliso;   //!
    TBranch        *b_Zmu_muminus_type;   //!
    TBranch        *b_Zmu_muminus_numberOfChambers;   //!
    TBranch        *b_Zmu_muminus_numberOfMatches;   //!
    TBranch        *b_JetAK5PF_nJets;   //!
    TBranch        *b_JetAK5PF_Et;   //!
    TBranch        *b_JetAK5PF_Pt;   //!
    TBranch        *b_JetAK5PF_Eta;   //!
    TBranch        *b_JetAK5PF_Phi;   //!
    TBranch        *b_JetAK5PF_Theta;   //!
    TBranch        *b_JetAK5PF_Px;   //!
    TBranch        *b_JetAK5PF_Py;   //!
    TBranch        *b_JetAK5PF_Pz;   //!
    TBranch        *b_JetAK5PF_E;   //!
    TBranch        *b_JetAK5PF_Y;   //!
    TBranch        *b_JetAK5PF_Mass;   //!
    TBranch        *b_JetAK5PF_Area;   //!
    TBranch        *b_JetAK5PF_nJetBTags;   //!
    TBranch        *b_JetAK5PF_nDau;   //!
    TBranch        *b_JetAK5PF_bDiscSSVHE;   //!
    TBranch        *b_JetAK5PF_bDiscTCHE;   //!
    TBranch        *b_JetAK5PF_bDiscrCSV;   //!
    TBranch        *b_JetAK5PF_bDiscJP;   //!
    TBranch        *b_JetAK5PF_bDiscrSSVHP;   //!
    TBranch        *b_JetAK5PF_bDiscTCHP;   //!
    TBranch        *b_JetCA8PRUNEDPF_nJets;   //!
    TBranch        *b_JetCA8PRUNEDPF_Et;   //!
    TBranch        *b_JetCA8PRUNEDPF_Pt;   //!
    TBranch        *b_JetCA8PRUNEDPF_Eta;   //!
    TBranch        *b_JetCA8PRUNEDPF_Phi;   //!
    TBranch        *b_JetCA8PRUNEDPF_Theta;   //!
    TBranch        *b_JetCA8PRUNEDPF_Px;   //!
    TBranch        *b_JetCA8PRUNEDPF_Py;   //!
    TBranch        *b_JetCA8PRUNEDPF_Pz;   //!
    TBranch        *b_JetCA8PRUNEDPF_E;   //!
    TBranch        *b_JetCA8PRUNEDPF_Y;   //!
    TBranch        *b_JetCA8PRUNEDPF_Mass;   //!
    TBranch        *b_JetCA8PRUNEDPF_Area;   //!
    TBranch        *b_JetCA8PRUNEDPF_nJetBTags;   //!
    TBranch        *b_JetCA8PRUNEDPF_nDau;   //!
    TBranch        *b_JetCA8PRUNEDPF_bDiscSSVHE;   //!
    TBranch        *b_JetCA8PRUNEDPF_bDiscTCHE;   //!
    TBranch        *b_JetCA8PRUNEDPF_bDiscrCSV;   //!
    TBranch        *b_JetCA8PRUNEDPF_bDiscJP;   //!
    TBranch        *b_JetCA8PRUNEDPF_bDiscrSSVHP;   //!
    TBranch        *b_JetCA8PRUNEDPF_bDiscTCHP;   //!
    TBranch        *b_JetCA8PRUNEDPF_subJet1Mass;   //!
    TBranch        *b_JetCA8PRUNEDPF_subJet2Mass;   //!
    TBranch        *b_JetCA8PF_nJets;   //!
    TBranch        *b_JetCA8PF_Et;   //!
    TBranch        *b_JetCA8PF_Pt;   //!
    TBranch        *b_JetCA8PF_Eta;   //!
    TBranch        *b_JetCA8PF_Phi;   //!
    TBranch        *b_JetCA8PF_Theta;   //!
    TBranch        *b_JetCA8PF_Px;   //!
    TBranch        *b_JetCA8PF_Py;   //!
    TBranch        *b_JetCA8PF_Pz;   //!
    TBranch        *b_JetCA8PF_E;   //!
    TBranch        *b_JetCA8PF_Y;   //!
    TBranch        *b_JetCA8PF_Mass;   //!
    TBranch        *b_JetCA8PF_Area;   //!
    TBranch        *b_JetCA8PF_nJetBTags;   //!
    TBranch        *b_JetCA8PF_nDau;   //!
    TBranch        *b_JetCA8PF_bDiscSSVHE;   //!
    TBranch        *b_JetCA8PF_bDiscTCHE;   //!
    TBranch        *b_JetCA8PF_bDiscrCSV;   //!
    TBranch        *b_JetCA8PF_bDiscJP;   //!
    TBranch        *b_JetCA8PF_bDiscrSSVHP;   //!
    TBranch        *b_JetCA8PF_bDiscTCHP;   //!
    TBranch        *b_JetAK5TRIMMEDPF_nJets;   //!
    TBranch        *b_JetAK5TRIMMEDPF_Et;   //!
    TBranch        *b_JetAK5TRIMMEDPF_Pt;   //!
    TBranch        *b_JetAK5TRIMMEDPF_Eta;   //!
    TBranch        *b_JetAK5TRIMMEDPF_Phi;   //!
    TBranch        *b_JetAK5TRIMMEDPF_Theta;   //!
    TBranch        *b_JetAK5TRIMMEDPF_Px;   //!
    TBranch        *b_JetAK5TRIMMEDPF_Py;   //!
    TBranch        *b_JetAK5TRIMMEDPF_Pz;   //!
    TBranch        *b_JetAK5TRIMMEDPF_E;   //!
    TBranch        *b_JetAK5TRIMMEDPF_Y;   //!
    TBranch        *b_JetAK5TRIMMEDPF_Mass;   //!
    TBranch        *b_JetAK5TRIMMEDPF_Area;   //!
    TBranch        *b_JetAK5FILTEREDPF_nJets;   //!
    TBranch        *b_JetAK5FILTEREDPF_Et;   //!
    TBranch        *b_JetAK5FILTEREDPF_Pt;   //!
    TBranch        *b_JetAK5FILTEREDPF_Eta;   //!
    TBranch        *b_JetAK5FILTEREDPF_Phi;   //!
    TBranch        *b_JetAK5FILTEREDPF_Theta;   //!
    TBranch        *b_JetAK5FILTEREDPF_Px;   //!
    TBranch        *b_JetAK5FILTEREDPF_Py;   //!
    TBranch        *b_JetAK5FILTEREDPF_Pz;   //!
    TBranch        *b_JetAK5FILTEREDPF_E;   //!
    TBranch        *b_JetAK5FILTEREDPF_Y;   //!
    TBranch        *b_JetAK5FILTEREDPF_Mass;   //!
    TBranch        *b_JetAK5FILTEREDPF_Area;   //!
    TBranch        *b_JetAK5PRUNEDPF_nJets;   //!
    TBranch        *b_JetAK5PRUNEDPF_Et;   //!
    TBranch        *b_JetAK5PRUNEDPF_Pt;   //!
    TBranch        *b_JetAK5PRUNEDPF_Eta;   //!
    TBranch        *b_JetAK5PRUNEDPF_Phi;   //!
    TBranch        *b_JetAK5PRUNEDPF_Theta;   //!
    TBranch        *b_JetAK5PRUNEDPF_Px;   //!
    TBranch        *b_JetAK5PRUNEDPF_Py;   //!
    TBranch        *b_JetAK5PRUNEDPF_Pz;   //!
    TBranch        *b_JetAK5PRUNEDPF_E;   //!
    TBranch        *b_JetAK5PRUNEDPF_Y;   //!
    TBranch        *b_JetAK5PRUNEDPF_Mass;   //!
    TBranch        *b_JetAK5PRUNEDPF_Area;   //!
    TBranch        *b_JetAK7TRIMMEDPF_nJets;   //!
    TBranch        *b_JetAK7TRIMMEDPF_Et;   //!
    TBranch        *b_JetAK7TRIMMEDPF_Pt;   //!
    TBranch        *b_JetAK7TRIMMEDPF_Eta;   //!
    TBranch        *b_JetAK7TRIMMEDPF_Phi;   //!
    TBranch        *b_JetAK7TRIMMEDPF_Theta;   //!
    TBranch        *b_JetAK7TRIMMEDPF_Px;   //!
    TBranch        *b_JetAK7TRIMMEDPF_Py;   //!
    TBranch        *b_JetAK7TRIMMEDPF_Pz;   //!
    TBranch        *b_JetAK7TRIMMEDPF_E;   //!
    TBranch        *b_JetAK7TRIMMEDPF_Y;   //!
    TBranch        *b_JetAK7TRIMMEDPF_Mass;   //!
    TBranch        *b_JetAK7TRIMMEDPF_Area;   //!
    TBranch        *b_JetAK7FILTEREDPF_nJets;   //!
    TBranch        *b_JetAK7FILTEREDPF_Et;   //!
    TBranch        *b_JetAK7FILTEREDPF_Pt;   //!
    TBranch        *b_JetAK7FILTEREDPF_Eta;   //!
    TBranch        *b_JetAK7FILTEREDPF_Phi;   //!
    TBranch        *b_JetAK7FILTEREDPF_Theta;   //!
    TBranch        *b_JetAK7FILTEREDPF_Px;   //!
    TBranch        *b_JetAK7FILTEREDPF_Py;   //!
    TBranch        *b_JetAK7FILTEREDPF_Pz;   //!
    TBranch        *b_JetAK7FILTEREDPF_E;   //!
    TBranch        *b_JetAK7FILTEREDPF_Y;   //!
    TBranch        *b_JetAK7FILTEREDPF_Mass;   //!
    TBranch        *b_JetAK7FILTEREDPF_Area;   //!
    TBranch        *b_JetAK7PRUNEDPF_nJets;   //!
    TBranch        *b_JetAK7PRUNEDPF_Et;   //!
    TBranch        *b_JetAK7PRUNEDPF_Pt;   //!
    TBranch        *b_JetAK7PRUNEDPF_Eta;   //!
    TBranch        *b_JetAK7PRUNEDPF_Phi;   //!
    TBranch        *b_JetAK7PRUNEDPF_Theta;   //!
    TBranch        *b_JetAK7PRUNEDPF_Px;   //!
    TBranch        *b_JetAK7PRUNEDPF_Py;   //!
    TBranch        *b_JetAK7PRUNEDPF_Pz;   //!
    TBranch        *b_JetAK7PRUNEDPF_E;   //!
    TBranch        *b_JetAK7PRUNEDPF_Y;   //!
    TBranch        *b_JetAK7PRUNEDPF_Mass;   //!
    TBranch        *b_JetAK7PRUNEDPF_Area;   //!
    TBranch        *b_JetAK5GENJETSNONU_nJets;   //!
    TBranch        *b_JetAK5GENJETSNONU_Et;   //!
    TBranch        *b_JetAK5GENJETSNONU_Pt;   //!
    TBranch        *b_JetAK5GENJETSNONU_Eta;   //!
    TBranch        *b_JetAK5GENJETSNONU_Phi;   //!
    TBranch        *b_JetAK5GENJETSNONU_Theta;   //!
    TBranch        *b_JetAK5GENJETSNONU_Px;   //!
    TBranch        *b_JetAK5GENJETSNONU_Py;   //!
    TBranch        *b_JetAK5GENJETSNONU_Pz;   //!
    TBranch        *b_JetAK5GENJETSNONU_E;   //!
    TBranch        *b_JetAK5GENJETSNONU_Y;   //!
    TBranch        *b_JetAK5GENJETSNONU_Mass;   //!
    TBranch        *b_JetAK5GENJETSNONU_Area;   //!
    TBranch        *b_JetAK7GENJETSNONU_nJets;   //!
    TBranch        *b_JetAK7GENJETSNONU_Et;   //!
    TBranch        *b_JetAK7GENJETSNONU_Pt;   //!
    TBranch        *b_JetAK7GENJETSNONU_Eta;   //!
    TBranch        *b_JetAK7GENJETSNONU_Phi;   //!
    TBranch        *b_JetAK7GENJETSNONU_Theta;   //!
    TBranch        *b_JetAK7GENJETSNONU_Px;   //!
    TBranch        *b_JetAK7GENJETSNONU_Py;   //!
    TBranch        *b_JetAK7GENJETSNONU_Pz;   //!
    TBranch        *b_JetAK7GENJETSNONU_E;   //!
    TBranch        *b_JetAK7GENJETSNONU_Y;   //!
    TBranch        *b_JetAK7GENJETSNONU_Mass;   //!
    TBranch        *b_JetAK7GENJETSNONU_Area;   //!
    TBranch        *b_JetCA8GENJETSNONU_nJets;   //!
    TBranch        *b_JetCA8GENJETSNONU_Et;   //!
    TBranch        *b_JetCA8GENJETSNONU_Pt;   //!
    TBranch        *b_JetCA8GENJETSNONU_Eta;   //!
    TBranch        *b_JetCA8GENJETSNONU_Phi;   //!
    TBranch        *b_JetCA8GENJETSNONU_Theta;   //!
    TBranch        *b_JetCA8GENJETSNONU_Px;   //!
    TBranch        *b_JetCA8GENJETSNONU_Py;   //!
    TBranch        *b_JetCA8GENJETSNONU_Pz;   //!
    TBranch        *b_JetCA8GENJETSNONU_E;   //!
    TBranch        *b_JetCA8GENJETSNONU_Y;   //!
    TBranch        *b_JetCA8GENJETSNONU_Mass;   //!
    TBranch        *b_JetCA8GENJETSNONU_Area;   //!
    TBranch        *b_event_runNo;   //!
    TBranch        *b_event_evtNo;   //!
    TBranch        *b_event_lumi;   //!
    TBranch        *b_event_bunch;   //!
    TBranch        *b_event_nPV;   //!
    TBranch        *b_event_PVx;   //!
    TBranch        *b_event_PVy;   //!
    TBranch        *b_event_PVz;   //!
    TBranch        *b_event_Class;   //!
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
    
    vJetSubstructureAnalysis(std::string inputname, std::string oname);
    virtual ~vJetSubstructureAnalysis();
    virtual Int_t    Cut(Long64_t entry);
    virtual Int_t    GetEntry(Long64_t entry);
    virtual Long64_t LoadTree(Long64_t entry);
    virtual void     Init(TTree *tree);
    virtual void     Loop(Long64_t maxevents=-1);
    virtual Bool_t   Notify();
    virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef vJetSubstructureAnalysis_cxx
vJetSubstructureAnalysis::vJetSubstructureAnalysis(std::string inputname, std::string oname)
{
    
    char fname[192];
    sprintf(fname,"%s",inputname.c_str());
    
    TChain* tree = new TChain("VJetSubstructure","VJetSubstructure");
    tree->Add(fname);
    
    fout = new TFile(oname.c_str(),"RECREATE");
    
    /*
     TFile* f = new TFile(fname);
     
     TTree* tree = (TTree*)gDirectory->Get("VJetSubstructure");
     fout = new TFile(oname.c_str(),"RECREATE");
     */
    Init( tree );
}

vJetSubstructureAnalysis::~vJetSubstructureAnalysis()
{
    if (!fChain) return;
    delete fChain->GetCurrentFile();
    
    fout->cd();
    otree->Write();
    fout->Close();

}

Int_t vJetSubstructureAnalysis::GetEntry(Long64_t entry)
{
    // Read contents of entry.
    if (!fChain) return 0;
    return fChain->GetEntry(entry);
}
Long64_t vJetSubstructureAnalysis::LoadTree(Long64_t entry)
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

void vJetSubstructureAnalysis::Init(TTree *tree)
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
    
    fChain->SetBranchAddress("Wel_mass", &Wel_mass, &b_Wel_mass);
    fChain->SetBranchAddress("Wel_mt", &Wel_mt, &b_Wel_mt);
    fChain->SetBranchAddress("Wel_px", &Wel_px, &b_Wel_px);
    fChain->SetBranchAddress("Wel_py", &Wel_py, &b_Wel_py);
    fChain->SetBranchAddress("Wel_pz", &Wel_pz, &b_Wel_pz);
    fChain->SetBranchAddress("Wel_e", &Wel_e, &b_Wel_e);
    fChain->SetBranchAddress("Wel_pt", &Wel_pt, &b_Wel_pt);
    fChain->SetBranchAddress("Wel_et", &Wel_et, &b_Wel_et);
    fChain->SetBranchAddress("Wel_eta", &Wel_eta, &b_Wel_eta);
    fChain->SetBranchAddress("Wel_phi", &Wel_phi, &b_Wel_phi);
    fChain->SetBranchAddress("Wel_vx", &Wel_vx, &b_Wel_vx);
    fChain->SetBranchAddress("Wel_vy", &Wel_vy, &b_Wel_vy);
    fChain->SetBranchAddress("Wel_vz", &Wel_vz, &b_Wel_vz);
    fChain->SetBranchAddress("Wel_y", &Wel_y, &b_Wel_y);
    fChain->SetBranchAddress("Wel_numTightElectrons", &Wel_numTightElectrons, &b_Wel_numTightElectrons);
    fChain->SetBranchAddress("Wel_numLooseElectrons", &Wel_numLooseElectrons, &b_Wel_numLooseElectrons);
    fChain->SetBranchAddress("Wel_pzNu1", &Wel_pzNu1, &b_Wel_pzNu1);
    fChain->SetBranchAddress("Wel_pzNu2", &Wel_pzNu2, &b_Wel_pzNu2);
    fChain->SetBranchAddress("Wel_electron_px", &Wel_electron_px, &b_Wel_electron_px);
    fChain->SetBranchAddress("Wel_electron_py", &Wel_electron_py, &b_Wel_electron_py);
    fChain->SetBranchAddress("Wel_electron_pz", &Wel_electron_pz, &b_Wel_electron_pz);
    fChain->SetBranchAddress("Wel_electron_e", &Wel_electron_e, &b_Wel_electron_e);
    fChain->SetBranchAddress("Wel_electron_pt", &Wel_electron_pt, &b_Wel_electron_pt);
    fChain->SetBranchAddress("Wel_electron_et", &Wel_electron_et, &b_Wel_electron_et);
    fChain->SetBranchAddress("Wel_electron_eta", &Wel_electron_eta, &b_Wel_electron_eta);
    fChain->SetBranchAddress("Wel_electron_theta", &Wel_electron_theta, &b_Wel_electron_theta);
    fChain->SetBranchAddress("Wel_electron_phi", &Wel_electron_phi, &b_Wel_electron_phi);
    fChain->SetBranchAddress("Wel_electron_charge", &Wel_electron_charge, &b_Wel_electron_charge);
    fChain->SetBranchAddress("Wel_electron_vx", &Wel_electron_vx, &b_Wel_electron_vx);
    fChain->SetBranchAddress("Wel_electron_vy", &Wel_electron_vy, &b_Wel_electron_vy);
    fChain->SetBranchAddress("Wel_electron_vz", &Wel_electron_vz, &b_Wel_electron_vz);
    fChain->SetBranchAddress("Wel_electron_y", &Wel_electron_y, &b_Wel_electron_y);
    fChain->SetBranchAddress("Wel_electron_trackiso", &Wel_electron_trackiso, &b_Wel_electron_trackiso);
    fChain->SetBranchAddress("Wel_electron_hcaliso", &Wel_electron_hcaliso, &b_Wel_electron_hcaliso);
    fChain->SetBranchAddress("Wel_electron_ecaliso", &Wel_electron_ecaliso, &b_Wel_electron_ecaliso);
    fChain->SetBranchAddress("Wel_electron_classification", &Wel_electron_classification, &b_Wel_electron_classification);
    fChain->SetBranchAddress("Wel_electron_isWP95", &Wel_electron_isWP95, &b_Wel_electron_isWP95);
    fChain->SetBranchAddress("Wel_electron_isWP80", &Wel_electron_isWP80, &b_Wel_electron_isWP80);
    fChain->SetBranchAddress("Wel_electron_isWP70", &Wel_electron_isWP70, &b_Wel_electron_isWP70);
    fChain->SetBranchAddress("Zel_mass", &Zel_mass, &b_Zel_mass);
    fChain->SetBranchAddress("Zel_mt", &Zel_mt, &b_Zel_mt);
    fChain->SetBranchAddress("Zel_px", &Zel_px, &b_Zel_px);
    fChain->SetBranchAddress("Zel_py", &Zel_py, &b_Zel_py);
    fChain->SetBranchAddress("Zel_pz", &Zel_pz, &b_Zel_pz);
    fChain->SetBranchAddress("Zel_e", &Zel_e, &b_Zel_e);
    fChain->SetBranchAddress("Zel_pt", &Zel_pt, &b_Zel_pt);
    fChain->SetBranchAddress("Zel_et", &Zel_et, &b_Zel_et);
    fChain->SetBranchAddress("Zel_eta", &Zel_eta, &b_Zel_eta);
    fChain->SetBranchAddress("Zel_phi", &Zel_phi, &b_Zel_phi);
    fChain->SetBranchAddress("Zel_vx", &Zel_vx, &b_Zel_vx);
    fChain->SetBranchAddress("Zel_vy", &Zel_vy, &b_Zel_vy);
    fChain->SetBranchAddress("Zel_vz", &Zel_vz, &b_Zel_vz);
    fChain->SetBranchAddress("Zel_y", &Zel_y, &b_Zel_y);
    fChain->SetBranchAddress("Zel_numTightElectrons", &Zel_numTightElectrons, &b_Zel_numTightElectrons);
    fChain->SetBranchAddress("Zel_numLooseElectrons", &Zel_numLooseElectrons, &b_Zel_numLooseElectrons);
    fChain->SetBranchAddress("Zel_eplus_px", &Zel_eplus_px, &b_Zel_eplus_px);
    fChain->SetBranchAddress("Zel_eplus_py", &Zel_eplus_py, &b_Zel_eplus_py);
    fChain->SetBranchAddress("Zel_eplus_pz", &Zel_eplus_pz, &b_Zel_eplus_pz);
    fChain->SetBranchAddress("Zel_eplus_e", &Zel_eplus_e, &b_Zel_eplus_e);
    fChain->SetBranchAddress("Zel_eplus_pt", &Zel_eplus_pt, &b_Zel_eplus_pt);
    fChain->SetBranchAddress("Zel_eplus_et", &Zel_eplus_et, &b_Zel_eplus_et);
    fChain->SetBranchAddress("Zel_eplus_eta", &Zel_eplus_eta, &b_Zel_eplus_eta);
    fChain->SetBranchAddress("Zel_eplus_theta", &Zel_eplus_theta, &b_Zel_eplus_theta);
    fChain->SetBranchAddress("Zel_eplus_phi", &Zel_eplus_phi, &b_Zel_eplus_phi);
    fChain->SetBranchAddress("Zel_eplus_charge", &Zel_eplus_charge, &b_Zel_eplus_charge);
    fChain->SetBranchAddress("Zel_eplus_vx", &Zel_eplus_vx, &b_Zel_eplus_vx);
    fChain->SetBranchAddress("Zel_eplus_vy", &Zel_eplus_vy, &b_Zel_eplus_vy);
    fChain->SetBranchAddress("Zel_eplus_vz", &Zel_eplus_vz, &b_Zel_eplus_vz);
    fChain->SetBranchAddress("Zel_eplus_y", &Zel_eplus_y, &b_Zel_eplus_y);
    fChain->SetBranchAddress("Zel_eplus_trackiso", &Zel_eplus_trackiso, &b_Zel_eplus_trackiso);
    fChain->SetBranchAddress("Zel_eplus_hcaliso", &Zel_eplus_hcaliso, &b_Zel_eplus_hcaliso);
    fChain->SetBranchAddress("Zel_eplus_ecaliso", &Zel_eplus_ecaliso, &b_Zel_eplus_ecaliso);
    fChain->SetBranchAddress("Zel_eplus_classification", &Zel_eplus_classification, &b_Zel_eplus_classification);
    fChain->SetBranchAddress("Zel_eplus_isWP95", &Zel_eplus_isWP95, &b_Zel_eplus_isWP95);
    fChain->SetBranchAddress("Zel_eplus_isWP80", &Zel_eplus_isWP80, &b_Zel_eplus_isWP80);
    fChain->SetBranchAddress("Zel_eplus_isWP70", &Zel_eplus_isWP70, &b_Zel_eplus_isWP70);
    fChain->SetBranchAddress("Zel_eminus_px", &Zel_eminus_px, &b_Zel_eminus_px);
    fChain->SetBranchAddress("Zel_eminus_py", &Zel_eminus_py, &b_Zel_eminus_py);
    fChain->SetBranchAddress("Zel_eminus_pz", &Zel_eminus_pz, &b_Zel_eminus_pz);
    fChain->SetBranchAddress("Zel_eminus_e", &Zel_eminus_e, &b_Zel_eminus_e);
    fChain->SetBranchAddress("Zel_eminus_pt", &Zel_eminus_pt, &b_Zel_eminus_pt);
    fChain->SetBranchAddress("Zel_eminus_et", &Zel_eminus_et, &b_Zel_eminus_et);
    fChain->SetBranchAddress("Zel_eminus_eta", &Zel_eminus_eta, &b_Zel_eminus_eta);
    fChain->SetBranchAddress("Zel_eminus_theta", &Zel_eminus_theta, &b_Zel_eminus_theta);
    fChain->SetBranchAddress("Zel_eminus_phi", &Zel_eminus_phi, &b_Zel_eminus_phi);
    fChain->SetBranchAddress("Zel_eminus_charge", &Zel_eminus_charge, &b_Zel_eminus_charge);
    fChain->SetBranchAddress("Zel_eminus_vx", &Zel_eminus_vx, &b_Zel_eminus_vx);
    fChain->SetBranchAddress("Zel_eminus_vy", &Zel_eminus_vy, &b_Zel_eminus_vy);
    fChain->SetBranchAddress("Zel_eminus_vz", &Zel_eminus_vz, &b_Zel_eminus_vz);
    fChain->SetBranchAddress("Zel_eminus_y", &Zel_eminus_y, &b_Zel_eminus_y);
    fChain->SetBranchAddress("Zel_eminus_trackiso", &Zel_eminus_trackiso, &b_Zel_eminus_trackiso);
    fChain->SetBranchAddress("Zel_eminus_hcaliso", &Zel_eminus_hcaliso, &b_Zel_eminus_hcaliso);
    fChain->SetBranchAddress("Zel_eminus_ecaliso", &Zel_eminus_ecaliso, &b_Zel_eminus_ecaliso);
    fChain->SetBranchAddress("Zel_eminus_isWP95", &Zel_eminus_isWP95, &b_Zel_eminus_isWP95);
    fChain->SetBranchAddress("Zel_eminus_isWP80", &Zel_eminus_isWP80, &b_Zel_eminus_isWP80);
    fChain->SetBranchAddress("Zel_eminus_isWP70", &Zel_eminus_isWP70, &b_Zel_eminus_isWP70);
    fChain->SetBranchAddress("Wmu_mass", &Wmu_mass, &b_Wmu_mass);
    fChain->SetBranchAddress("Wmu_mt", &Wmu_mt, &b_Wmu_mt);
    fChain->SetBranchAddress("Wmu_px", &Wmu_px, &b_Wmu_px);
    fChain->SetBranchAddress("Wmu_py", &Wmu_py, &b_Wmu_py);
    fChain->SetBranchAddress("Wmu_pz", &Wmu_pz, &b_Wmu_pz);
    fChain->SetBranchAddress("Wmu_e", &Wmu_e, &b_Wmu_e);
    fChain->SetBranchAddress("Wmu_pt", &Wmu_pt, &b_Wmu_pt);
    fChain->SetBranchAddress("Wmu_et", &Wmu_et, &b_Wmu_et);
    fChain->SetBranchAddress("Wmu_eta", &Wmu_eta, &b_Wmu_eta);
    fChain->SetBranchAddress("Wmu_phi", &Wmu_phi, &b_Wmu_phi);
    fChain->SetBranchAddress("Wmu_vx", &Wmu_vx, &b_Wmu_vx);
    fChain->SetBranchAddress("Wmu_vy", &Wmu_vy, &b_Wmu_vy);
    fChain->SetBranchAddress("Wmu_vz", &Wmu_vz, &b_Wmu_vz);
    fChain->SetBranchAddress("Wmu_y", &Wmu_y, &b_Wmu_y);
    fChain->SetBranchAddress("Wmu_pzNu1", &Wmu_pzNu1, &b_Wmu_pzNu1);
    fChain->SetBranchAddress("Wmu_pzNu2", &Wmu_pzNu2, &b_Wmu_pzNu2);
    fChain->SetBranchAddress("Wmu_muon_px", &Wmu_muon_px, &b_Wmu_muon_px);
    fChain->SetBranchAddress("Wmu_muon_py", &Wmu_muon_py, &b_Wmu_muon_py);
    fChain->SetBranchAddress("Wmu_muon_pz", &Wmu_muon_pz, &b_Wmu_muon_pz);
    fChain->SetBranchAddress("Wmu_muon_e", &Wmu_muon_e, &b_Wmu_muon_e);
    fChain->SetBranchAddress("Wmu_muon_pt", &Wmu_muon_pt, &b_Wmu_muon_pt);
    fChain->SetBranchAddress("Wmu_muon_et", &Wmu_muon_et, &b_Wmu_muon_et);
    fChain->SetBranchAddress("Wmu_muon_eta", &Wmu_muon_eta, &b_Wmu_muon_eta);
    fChain->SetBranchAddress("Wmu_muon_theta", &Wmu_muon_theta, &b_Wmu_muon_theta);
    fChain->SetBranchAddress("Wmu_muon_phi", &Wmu_muon_phi, &b_Wmu_muon_phi);
    fChain->SetBranchAddress("Wmu_muon_charge", &Wmu_muon_charge, &b_Wmu_muon_charge);
    fChain->SetBranchAddress("Wmu_muon_vx", &Wmu_muon_vx, &b_Wmu_muon_vx);
    fChain->SetBranchAddress("Wmu_muon_vy", &Wmu_muon_vy, &b_Wmu_muon_vy);
    fChain->SetBranchAddress("Wmu_muon_vz", &Wmu_muon_vz, &b_Wmu_muon_vz);
    fChain->SetBranchAddress("Wmu_muon_y", &Wmu_muon_y, &b_Wmu_muon_y);
    fChain->SetBranchAddress("Wmu_muon_trackiso", &Wmu_muon_trackiso, &b_Wmu_muon_trackiso);
    fChain->SetBranchAddress("Wmu_muon_hcaliso", &Wmu_muon_hcaliso, &b_Wmu_muon_hcaliso);
    fChain->SetBranchAddress("Wmu_muon_ecaliso", &Wmu_muon_ecaliso, &b_Wmu_muon_ecaliso);
    fChain->SetBranchAddress("Wmu_muon_type", &Wmu_muon_type, &b_Wmu_muon_type);
    fChain->SetBranchAddress("Wmu_muon_numberOfChambers", &Wmu_muon_numberOfChambers, &b_Wmu_muon_numberOfChambers);
    fChain->SetBranchAddress("Wmu_muon_numberOfMatches", &Wmu_muon_numberOfMatches, &b_Wmu_muon_numberOfMatches);
    fChain->SetBranchAddress("Wmu_muon_d0bsp", &Wmu_muon_d0bsp, &b_Wmu_muon_d0bsp);
    fChain->SetBranchAddress("Wmu_muon_dz000", &Wmu_muon_dz000, &b_Wmu_muon_dz000);
    fChain->SetBranchAddress("Wmu_muon_pfiso_sumChargedHadronPt", &Wmu_muon_pfiso_sumChargedHadronPt, &b_Wmu_muon_pfiso_sumChargedHadronPt);
    fChain->SetBranchAddress("Wmu_muon_pfiso_sumChargedParticlePt", &Wmu_muon_pfiso_sumChargedParticlePt, &b_Wmu_muon_pfiso_sumChargedParticlePt);
    fChain->SetBranchAddress("Wmu_muon_pfiso_sumNeutralHadronEt", &Wmu_muon_pfiso_sumNeutralHadronEt, &b_Wmu_muon_pfiso_sumNeutralHadronEt);
    fChain->SetBranchAddress("Wmu_muon_pfiso_sumPhotonEt", &Wmu_muon_pfiso_sumPhotonEt, &b_Wmu_muon_pfiso_sumPhotonEt);
    fChain->SetBranchAddress("Wmu_muon_pfiso_sumPUPt", &Wmu_muon_pfiso_sumPUPt, &b_Wmu_muon_pfiso_sumPUPt);
    fChain->SetBranchAddress("Zmu_mass", &Zmu_mass, &b_Zmu_mass);
    fChain->SetBranchAddress("Zmu_mt", &Zmu_mt, &b_Zmu_mt);
    fChain->SetBranchAddress("Zmu_px", &Zmu_px, &b_Zmu_px);
    fChain->SetBranchAddress("Zmu_py", &Zmu_py, &b_Zmu_py);
    fChain->SetBranchAddress("Zmu_pz", &Zmu_pz, &b_Zmu_pz);
    fChain->SetBranchAddress("Zmu_e", &Zmu_e, &b_Zmu_e);
    fChain->SetBranchAddress("Zmu_pt", &Zmu_pt, &b_Zmu_pt);
    fChain->SetBranchAddress("Zmu_et", &Zmu_et, &b_Zmu_et);
    fChain->SetBranchAddress("Zmu_eta", &Zmu_eta, &b_Zmu_eta);
    fChain->SetBranchAddress("Zmu_phi", &Zmu_phi, &b_Zmu_phi);
    fChain->SetBranchAddress("Zmu_vx", &Zmu_vx, &b_Zmu_vx);
    fChain->SetBranchAddress("Zmu_vy", &Zmu_vy, &b_Zmu_vy);
    fChain->SetBranchAddress("Zmu_vz", &Zmu_vz, &b_Zmu_vz);
    fChain->SetBranchAddress("Zmu_y", &Zmu_y, &b_Zmu_y);
    fChain->SetBranchAddress("Zmu_muplus_px", &Zmu_muplus_px, &b_Zmu_muplus_px);
    fChain->SetBranchAddress("Zmu_muplus_py", &Zmu_muplus_py, &b_Zmu_muplus_py);
    fChain->SetBranchAddress("Zmu_muplus_pz", &Zmu_muplus_pz, &b_Zmu_muplus_pz);
    fChain->SetBranchAddress("Zmu_muplus_e", &Zmu_muplus_e, &b_Zmu_muplus_e);
    fChain->SetBranchAddress("Zmu_muplus_pt", &Zmu_muplus_pt, &b_Zmu_muplus_pt);
    fChain->SetBranchAddress("Zmu_muplus_et", &Zmu_muplus_et, &b_Zmu_muplus_et);
    fChain->SetBranchAddress("Zmu_muplus_eta", &Zmu_muplus_eta, &b_Zmu_muplus_eta);
    fChain->SetBranchAddress("Zmu_muplus_theta", &Zmu_muplus_theta, &b_Zmu_muplus_theta);
    fChain->SetBranchAddress("Zmu_muplus_phi", &Zmu_muplus_phi, &b_Zmu_muplus_phi);
    fChain->SetBranchAddress("Zmu_muplus_charge", &Zmu_muplus_charge, &b_Zmu_muplus_charge);
    fChain->SetBranchAddress("Zmu_muplus_vx", &Zmu_muplus_vx, &b_Zmu_muplus_vx);
    fChain->SetBranchAddress("Zmu_muplus_vy", &Zmu_muplus_vy, &b_Zmu_muplus_vy);
    fChain->SetBranchAddress("Zmu_muplus_vz", &Zmu_muplus_vz, &b_Zmu_muplus_vz);
    fChain->SetBranchAddress("Zmu_muplus_y", &Zmu_muplus_y, &b_Zmu_muplus_y);
    fChain->SetBranchAddress("Zmu_muplus_trackiso", &Zmu_muplus_trackiso, &b_Zmu_muplus_trackiso);
    fChain->SetBranchAddress("Zmu_muplus_hcaliso", &Zmu_muplus_hcaliso, &b_Zmu_muplus_hcaliso);
    fChain->SetBranchAddress("Zmu_muplus_ecaliso", &Zmu_muplus_ecaliso, &b_Zmu_muplus_ecaliso);
    fChain->SetBranchAddress("Zmu_muplus_type", &Zmu_muplus_type, &b_Zmu_muplus_type);
    fChain->SetBranchAddress("Zmu_muplus_numberOfChambers", &Zmu_muplus_numberOfChambers, &b_Zmu_muplus_numberOfChambers);
    fChain->SetBranchAddress("Zmu_muplus_numberOfMatches", &Zmu_muplus_numberOfMatches, &b_Zmu_muplus_numberOfMatches);
    fChain->SetBranchAddress("Zmu_muplus_d0bsp", &Zmu_muplus_d0bsp, &b_Zmu_muplus_d0bsp);
    fChain->SetBranchAddress("Zmu_muplus_dz000", &Zmu_muplus_dz000, &b_Zmu_muplus_dz000);
    fChain->SetBranchAddress("Zmu_muplus_pfiso_sumChargedHadronPt", &Zmu_muplus_pfiso_sumChargedHadronPt, &b_Zmu_muplus_pfiso_sumChargedHadronPt);
    fChain->SetBranchAddress("Zmu_muplus_pfiso_sumChargedParticlePt", &Zmu_muplus_pfiso_sumChargedParticlePt, &b_Zmu_muplus_pfiso_sumChargedParticlePt);
    fChain->SetBranchAddress("Zmu_muplus_pfiso_sumNeutralHadronEt", &Zmu_muplus_pfiso_sumNeutralHadronEt, &b_Zmu_muplus_pfiso_sumNeutralHadronEt);
    fChain->SetBranchAddress("Zmu_muplus_pfiso_sumPhotonEt", &Zmu_muplus_pfiso_sumPhotonEt, &b_Zmu_muplus_pfiso_sumPhotonEt);
    fChain->SetBranchAddress("Zmu_muplus_pfiso_sumPUPt", &Zmu_muplus_pfiso_sumPUPt, &b_Zmu_muplus_pfiso_sumPUPt);
    fChain->SetBranchAddress("Zmu_muminus_px", &Zmu_muminus_px, &b_Zmu_muminus_px);
    fChain->SetBranchAddress("Zmu_muminus_py", &Zmu_muminus_py, &b_Zmu_muminus_py);
    fChain->SetBranchAddress("Zmu_muminus_pz", &Zmu_muminus_pz, &b_Zmu_muminus_pz);
    fChain->SetBranchAddress("Zmu_muminus_e", &Zmu_muminus_e, &b_Zmu_muminus_e);
    fChain->SetBranchAddress("Zmu_muminus_pt", &Zmu_muminus_pt, &b_Zmu_muminus_pt);
    fChain->SetBranchAddress("Zmu_muminus_et", &Zmu_muminus_et, &b_Zmu_muminus_et);
    fChain->SetBranchAddress("Zmu_muminus_eta", &Zmu_muminus_eta, &b_Zmu_muminus_eta);
    fChain->SetBranchAddress("Zmu_muminus_theta", &Zmu_muminus_theta, &b_Zmu_muminus_theta);
    fChain->SetBranchAddress("Zmu_muminus_phi", &Zmu_muminus_phi, &b_Zmu_muminus_phi);
    fChain->SetBranchAddress("Zmu_muminus_charge", &Zmu_muminus_charge, &b_Zmu_muminus_charge);
    fChain->SetBranchAddress("Zmu_muminus_vx", &Zmu_muminus_vx, &b_Zmu_muminus_vx);
    fChain->SetBranchAddress("Zmu_muminus_vy", &Zmu_muminus_vy, &b_Zmu_muminus_vy);
    fChain->SetBranchAddress("Zmu_muminus_vz", &Zmu_muminus_vz, &b_Zmu_muminus_vz);
    fChain->SetBranchAddress("Zmu_muminus_y", &Zmu_muminus_y, &b_Zmu_muminus_y);
    fChain->SetBranchAddress("Zmu_muminus_trackiso", &Zmu_muminus_trackiso, &b_Zmu_muminus_trackiso);
    fChain->SetBranchAddress("Zmu_muminus_hcaliso", &Zmu_muminus_hcaliso, &b_Zmu_muminus_hcaliso);
    fChain->SetBranchAddress("Zmu_muminus_ecaliso", &Zmu_muminus_ecaliso, &b_Zmu_muminus_ecaliso);
    fChain->SetBranchAddress("Zmu_muminus_type", &Zmu_muminus_type, &b_Zmu_muminus_type);
    fChain->SetBranchAddress("Zmu_muminus_numberOfChambers", &Zmu_muminus_numberOfChambers, &b_Zmu_muminus_numberOfChambers);
    fChain->SetBranchAddress("Zmu_muminus_numberOfMatches", &Zmu_muminus_numberOfMatches, &b_Zmu_muminus_numberOfMatches);
    fChain->SetBranchAddress("JetAK5PF_nJets", &JetAK5PF_nJets, &b_JetAK5PF_nJets);
    fChain->SetBranchAddress("JetAK5PF_Et", JetAK5PF_Et, &b_JetAK5PF_Et);
    fChain->SetBranchAddress("JetAK5PF_Pt", JetAK5PF_Pt, &b_JetAK5PF_Pt);
    fChain->SetBranchAddress("JetAK5PF_Eta", JetAK5PF_Eta, &b_JetAK5PF_Eta);
    fChain->SetBranchAddress("JetAK5PF_Phi", JetAK5PF_Phi, &b_JetAK5PF_Phi);
    fChain->SetBranchAddress("JetAK5PF_Theta", JetAK5PF_Theta, &b_JetAK5PF_Theta);
    fChain->SetBranchAddress("JetAK5PF_Px", JetAK5PF_Px, &b_JetAK5PF_Px);
    fChain->SetBranchAddress("JetAK5PF_Py", JetAK5PF_Py, &b_JetAK5PF_Py);
    fChain->SetBranchAddress("JetAK5PF_Pz", JetAK5PF_Pz, &b_JetAK5PF_Pz);
    fChain->SetBranchAddress("JetAK5PF_E", JetAK5PF_E, &b_JetAK5PF_E);
    fChain->SetBranchAddress("JetAK5PF_Y", JetAK5PF_Y, &b_JetAK5PF_Y);
    fChain->SetBranchAddress("JetAK5PF_Mass", JetAK5PF_Mass, &b_JetAK5PF_Mass);
    fChain->SetBranchAddress("JetAK5PF_Area", JetAK5PF_Area, &b_JetAK5PF_Area);
    fChain->SetBranchAddress("JetAK5PF_nJetBTags", &JetAK5PF_nJetBTags, &b_JetAK5PF_nJetBTags);
    fChain->SetBranchAddress("JetAK5PF_nDau", JetAK5PF_nDau, &b_JetAK5PF_nDau);
    fChain->SetBranchAddress("JetAK5PF_bDiscSSVHE", JetAK5PF_bDiscSSVHE, &b_JetAK5PF_bDiscSSVHE);
    fChain->SetBranchAddress("JetAK5PF_bDiscTCHE", JetAK5PF_bDiscTCHE, &b_JetAK5PF_bDiscTCHE);
    fChain->SetBranchAddress("JetAK5PF_bDiscrCSV", JetAK5PF_bDiscrCSV, &b_JetAK5PF_bDiscrCSV);
    fChain->SetBranchAddress("JetAK5PF_bDiscJP", JetAK5PF_bDiscJP, &b_JetAK5PF_bDiscJP);
    fChain->SetBranchAddress("JetAK5PF_bDiscrSSVHP", JetAK5PF_bDiscrSSVHP, &b_JetAK5PF_bDiscrSSVHP);
    fChain->SetBranchAddress("JetAK5PF_bDiscTCHP", JetAK5PF_bDiscTCHP, &b_JetAK5PF_bDiscTCHP);
    fChain->SetBranchAddress("JetCA8PRUNEDPF_nJets", &JetCA8PRUNEDPF_nJets, &b_JetCA8PRUNEDPF_nJets);
    fChain->SetBranchAddress("JetCA8PRUNEDPF_Et", JetCA8PRUNEDPF_Et, &b_JetCA8PRUNEDPF_Et);
    fChain->SetBranchAddress("JetCA8PRUNEDPF_Pt", JetCA8PRUNEDPF_Pt, &b_JetCA8PRUNEDPF_Pt);
    fChain->SetBranchAddress("JetCA8PRUNEDPF_Eta", JetCA8PRUNEDPF_Eta, &b_JetCA8PRUNEDPF_Eta);
    fChain->SetBranchAddress("JetCA8PRUNEDPF_Phi", JetCA8PRUNEDPF_Phi, &b_JetCA8PRUNEDPF_Phi);
    fChain->SetBranchAddress("JetCA8PRUNEDPF_Theta", JetCA8PRUNEDPF_Theta, &b_JetCA8PRUNEDPF_Theta);
    fChain->SetBranchAddress("JetCA8PRUNEDPF_Px", JetCA8PRUNEDPF_Px, &b_JetCA8PRUNEDPF_Px);
    fChain->SetBranchAddress("JetCA8PRUNEDPF_Py", JetCA8PRUNEDPF_Py, &b_JetCA8PRUNEDPF_Py);
    fChain->SetBranchAddress("JetCA8PRUNEDPF_Pz", JetCA8PRUNEDPF_Pz, &b_JetCA8PRUNEDPF_Pz);
    fChain->SetBranchAddress("JetCA8PRUNEDPF_E", JetCA8PRUNEDPF_E, &b_JetCA8PRUNEDPF_E);
    fChain->SetBranchAddress("JetCA8PRUNEDPF_Y", JetCA8PRUNEDPF_Y, &b_JetCA8PRUNEDPF_Y);
    fChain->SetBranchAddress("JetCA8PRUNEDPF_Mass", JetCA8PRUNEDPF_Mass, &b_JetCA8PRUNEDPF_Mass);
    fChain->SetBranchAddress("JetCA8PRUNEDPF_Area", JetCA8PRUNEDPF_Area, &b_JetCA8PRUNEDPF_Area);
    fChain->SetBranchAddress("JetCA8PRUNEDPF_nJetBTags", &JetCA8PRUNEDPF_nJetBTags, &b_JetCA8PRUNEDPF_nJetBTags);
    fChain->SetBranchAddress("JetCA8PRUNEDPF_nDau", JetCA8PRUNEDPF_nDau, &b_JetCA8PRUNEDPF_nDau);
    fChain->SetBranchAddress("JetCA8PRUNEDPF_bDiscSSVHE", JetCA8PRUNEDPF_bDiscSSVHE, &b_JetCA8PRUNEDPF_bDiscSSVHE);
    fChain->SetBranchAddress("JetCA8PRUNEDPF_bDiscTCHE", JetCA8PRUNEDPF_bDiscTCHE, &b_JetCA8PRUNEDPF_bDiscTCHE);
    fChain->SetBranchAddress("JetCA8PRUNEDPF_bDiscrCSV", JetCA8PRUNEDPF_bDiscrCSV, &b_JetCA8PRUNEDPF_bDiscrCSV);
    fChain->SetBranchAddress("JetCA8PRUNEDPF_bDiscJP", JetCA8PRUNEDPF_bDiscJP, &b_JetCA8PRUNEDPF_bDiscJP);
    fChain->SetBranchAddress("JetCA8PRUNEDPF_bDiscrSSVHP", JetCA8PRUNEDPF_bDiscrSSVHP, &b_JetCA8PRUNEDPF_bDiscrSSVHP);
    fChain->SetBranchAddress("JetCA8PRUNEDPF_bDiscTCHP", JetCA8PRUNEDPF_bDiscTCHP, &b_JetCA8PRUNEDPF_bDiscTCHP);
    fChain->SetBranchAddress("JetCA8PRUNEDPF_subJet1Mass", JetCA8PRUNEDPF_subJet1Mass, &b_JetCA8PRUNEDPF_subJet1Mass);
    fChain->SetBranchAddress("JetCA8PRUNEDPF_subJet2Mass", JetCA8PRUNEDPF_subJet2Mass, &b_JetCA8PRUNEDPF_subJet2Mass);
    fChain->SetBranchAddress("JetCA8PF_nJets", &JetCA8PF_nJets, &b_JetCA8PF_nJets);
    fChain->SetBranchAddress("JetCA8PF_Et", JetCA8PF_Et, &b_JetCA8PF_Et);
    fChain->SetBranchAddress("JetCA8PF_Pt", JetCA8PF_Pt, &b_JetCA8PF_Pt);
    fChain->SetBranchAddress("JetCA8PF_Eta", JetCA8PF_Eta, &b_JetCA8PF_Eta);
    fChain->SetBranchAddress("JetCA8PF_Phi", JetCA8PF_Phi, &b_JetCA8PF_Phi);
    fChain->SetBranchAddress("JetCA8PF_Theta", JetCA8PF_Theta, &b_JetCA8PF_Theta);
    fChain->SetBranchAddress("JetCA8PF_Px", JetCA8PF_Px, &b_JetCA8PF_Px);
    fChain->SetBranchAddress("JetCA8PF_Py", JetCA8PF_Py, &b_JetCA8PF_Py);
    fChain->SetBranchAddress("JetCA8PF_Pz", JetCA8PF_Pz, &b_JetCA8PF_Pz);
    fChain->SetBranchAddress("JetCA8PF_E", JetCA8PF_E, &b_JetCA8PF_E);
    fChain->SetBranchAddress("JetCA8PF_Y", JetCA8PF_Y, &b_JetCA8PF_Y);
    fChain->SetBranchAddress("JetCA8PF_Mass", JetCA8PF_Mass, &b_JetCA8PF_Mass);
    fChain->SetBranchAddress("JetCA8PF_Area", JetCA8PF_Area, &b_JetCA8PF_Area);
    fChain->SetBranchAddress("JetCA8PF_nJetBTags", &JetCA8PF_nJetBTags, &b_JetCA8PF_nJetBTags);
    fChain->SetBranchAddress("JetCA8PF_nDau", JetCA8PF_nDau, &b_JetCA8PF_nDau);
    fChain->SetBranchAddress("JetCA8PF_bDiscSSVHE", JetCA8PF_bDiscSSVHE, &b_JetCA8PF_bDiscSSVHE);
    fChain->SetBranchAddress("JetCA8PF_bDiscTCHE", JetCA8PF_bDiscTCHE, &b_JetCA8PF_bDiscTCHE);
    fChain->SetBranchAddress("JetCA8PF_bDiscrCSV", JetCA8PF_bDiscrCSV, &b_JetCA8PF_bDiscrCSV);
    fChain->SetBranchAddress("JetCA8PF_bDiscJP", JetCA8PF_bDiscJP, &b_JetCA8PF_bDiscJP);
    fChain->SetBranchAddress("JetCA8PF_bDiscrSSVHP", JetCA8PF_bDiscrSSVHP, &b_JetCA8PF_bDiscrSSVHP);
    fChain->SetBranchAddress("JetCA8PF_bDiscTCHP", JetCA8PF_bDiscTCHP, &b_JetCA8PF_bDiscTCHP);
    fChain->SetBranchAddress("JetAK5TRIMMEDPF_nJets", &JetAK5TRIMMEDPF_nJets, &b_JetAK5TRIMMEDPF_nJets);
    fChain->SetBranchAddress("JetAK5TRIMMEDPF_Et", JetAK5TRIMMEDPF_Et, &b_JetAK5TRIMMEDPF_Et);
    fChain->SetBranchAddress("JetAK5TRIMMEDPF_Pt", JetAK5TRIMMEDPF_Pt, &b_JetAK5TRIMMEDPF_Pt);
    fChain->SetBranchAddress("JetAK5TRIMMEDPF_Eta", JetAK5TRIMMEDPF_Eta, &b_JetAK5TRIMMEDPF_Eta);
    fChain->SetBranchAddress("JetAK5TRIMMEDPF_Phi", JetAK5TRIMMEDPF_Phi, &b_JetAK5TRIMMEDPF_Phi);
    fChain->SetBranchAddress("JetAK5TRIMMEDPF_Theta", JetAK5TRIMMEDPF_Theta, &b_JetAK5TRIMMEDPF_Theta);
    fChain->SetBranchAddress("JetAK5TRIMMEDPF_Px", JetAK5TRIMMEDPF_Px, &b_JetAK5TRIMMEDPF_Px);
    fChain->SetBranchAddress("JetAK5TRIMMEDPF_Py", JetAK5TRIMMEDPF_Py, &b_JetAK5TRIMMEDPF_Py);
    fChain->SetBranchAddress("JetAK5TRIMMEDPF_Pz", JetAK5TRIMMEDPF_Pz, &b_JetAK5TRIMMEDPF_Pz);
    fChain->SetBranchAddress("JetAK5TRIMMEDPF_E", JetAK5TRIMMEDPF_E, &b_JetAK5TRIMMEDPF_E);
    fChain->SetBranchAddress("JetAK5TRIMMEDPF_Y", JetAK5TRIMMEDPF_Y, &b_JetAK5TRIMMEDPF_Y);
    fChain->SetBranchAddress("JetAK5TRIMMEDPF_Mass", JetAK5TRIMMEDPF_Mass, &b_JetAK5TRIMMEDPF_Mass);
    fChain->SetBranchAddress("JetAK5TRIMMEDPF_Area", JetAK5TRIMMEDPF_Area, &b_JetAK5TRIMMEDPF_Area);
    fChain->SetBranchAddress("JetAK5FILTEREDPF_nJets", &JetAK5FILTEREDPF_nJets, &b_JetAK5FILTEREDPF_nJets);
    fChain->SetBranchAddress("JetAK5FILTEREDPF_Et", JetAK5FILTEREDPF_Et, &b_JetAK5FILTEREDPF_Et);
    fChain->SetBranchAddress("JetAK5FILTEREDPF_Pt", JetAK5FILTEREDPF_Pt, &b_JetAK5FILTEREDPF_Pt);
    fChain->SetBranchAddress("JetAK5FILTEREDPF_Eta", JetAK5FILTEREDPF_Eta, &b_JetAK5FILTEREDPF_Eta);
    fChain->SetBranchAddress("JetAK5FILTEREDPF_Phi", JetAK5FILTEREDPF_Phi, &b_JetAK5FILTEREDPF_Phi);
    fChain->SetBranchAddress("JetAK5FILTEREDPF_Theta", JetAK5FILTEREDPF_Theta, &b_JetAK5FILTEREDPF_Theta);
    fChain->SetBranchAddress("JetAK5FILTEREDPF_Px", JetAK5FILTEREDPF_Px, &b_JetAK5FILTEREDPF_Px);
    fChain->SetBranchAddress("JetAK5FILTEREDPF_Py", JetAK5FILTEREDPF_Py, &b_JetAK5FILTEREDPF_Py);
    fChain->SetBranchAddress("JetAK5FILTEREDPF_Pz", JetAK5FILTEREDPF_Pz, &b_JetAK5FILTEREDPF_Pz);
    fChain->SetBranchAddress("JetAK5FILTEREDPF_E", JetAK5FILTEREDPF_E, &b_JetAK5FILTEREDPF_E);
    fChain->SetBranchAddress("JetAK5FILTEREDPF_Y", JetAK5FILTEREDPF_Y, &b_JetAK5FILTEREDPF_Y);
    fChain->SetBranchAddress("JetAK5FILTEREDPF_Mass", JetAK5FILTEREDPF_Mass, &b_JetAK5FILTEREDPF_Mass);
    fChain->SetBranchAddress("JetAK5FILTEREDPF_Area", JetAK5FILTEREDPF_Area, &b_JetAK5FILTEREDPF_Area);
    fChain->SetBranchAddress("JetAK5PRUNEDPF_nJets", &JetAK5PRUNEDPF_nJets, &b_JetAK5PRUNEDPF_nJets);
    fChain->SetBranchAddress("JetAK5PRUNEDPF_Et", JetAK5PRUNEDPF_Et, &b_JetAK5PRUNEDPF_Et);
    fChain->SetBranchAddress("JetAK5PRUNEDPF_Pt", JetAK5PRUNEDPF_Pt, &b_JetAK5PRUNEDPF_Pt);
    fChain->SetBranchAddress("JetAK5PRUNEDPF_Eta", JetAK5PRUNEDPF_Eta, &b_JetAK5PRUNEDPF_Eta);
    fChain->SetBranchAddress("JetAK5PRUNEDPF_Phi", JetAK5PRUNEDPF_Phi, &b_JetAK5PRUNEDPF_Phi);
    fChain->SetBranchAddress("JetAK5PRUNEDPF_Theta", JetAK5PRUNEDPF_Theta, &b_JetAK5PRUNEDPF_Theta);
    fChain->SetBranchAddress("JetAK5PRUNEDPF_Px", JetAK5PRUNEDPF_Px, &b_JetAK5PRUNEDPF_Px);
    fChain->SetBranchAddress("JetAK5PRUNEDPF_Py", JetAK5PRUNEDPF_Py, &b_JetAK5PRUNEDPF_Py);
    fChain->SetBranchAddress("JetAK5PRUNEDPF_Pz", JetAK5PRUNEDPF_Pz, &b_JetAK5PRUNEDPF_Pz);
    fChain->SetBranchAddress("JetAK5PRUNEDPF_E", JetAK5PRUNEDPF_E, &b_JetAK5PRUNEDPF_E);
    fChain->SetBranchAddress("JetAK5PRUNEDPF_Y", JetAK5PRUNEDPF_Y, &b_JetAK5PRUNEDPF_Y);
    fChain->SetBranchAddress("JetAK5PRUNEDPF_Mass", JetAK5PRUNEDPF_Mass, &b_JetAK5PRUNEDPF_Mass);
    fChain->SetBranchAddress("JetAK5PRUNEDPF_Area", JetAK5PRUNEDPF_Area, &b_JetAK5PRUNEDPF_Area);
    fChain->SetBranchAddress("JetAK7TRIMMEDPF_nJets", &JetAK7TRIMMEDPF_nJets, &b_JetAK7TRIMMEDPF_nJets);
    fChain->SetBranchAddress("JetAK7TRIMMEDPF_Et", JetAK7TRIMMEDPF_Et, &b_JetAK7TRIMMEDPF_Et);
    fChain->SetBranchAddress("JetAK7TRIMMEDPF_Pt", JetAK7TRIMMEDPF_Pt, &b_JetAK7TRIMMEDPF_Pt);
    fChain->SetBranchAddress("JetAK7TRIMMEDPF_Eta", JetAK7TRIMMEDPF_Eta, &b_JetAK7TRIMMEDPF_Eta);
    fChain->SetBranchAddress("JetAK7TRIMMEDPF_Phi", JetAK7TRIMMEDPF_Phi, &b_JetAK7TRIMMEDPF_Phi);
    fChain->SetBranchAddress("JetAK7TRIMMEDPF_Theta", JetAK7TRIMMEDPF_Theta, &b_JetAK7TRIMMEDPF_Theta);
    fChain->SetBranchAddress("JetAK7TRIMMEDPF_Px", JetAK7TRIMMEDPF_Px, &b_JetAK7TRIMMEDPF_Px);
    fChain->SetBranchAddress("JetAK7TRIMMEDPF_Py", JetAK7TRIMMEDPF_Py, &b_JetAK7TRIMMEDPF_Py);
    fChain->SetBranchAddress("JetAK7TRIMMEDPF_Pz", JetAK7TRIMMEDPF_Pz, &b_JetAK7TRIMMEDPF_Pz);
    fChain->SetBranchAddress("JetAK7TRIMMEDPF_E", JetAK7TRIMMEDPF_E, &b_JetAK7TRIMMEDPF_E);
    fChain->SetBranchAddress("JetAK7TRIMMEDPF_Y", JetAK7TRIMMEDPF_Y, &b_JetAK7TRIMMEDPF_Y);
    fChain->SetBranchAddress("JetAK7TRIMMEDPF_Mass", JetAK7TRIMMEDPF_Mass, &b_JetAK7TRIMMEDPF_Mass);
    fChain->SetBranchAddress("JetAK7TRIMMEDPF_Area", JetAK7TRIMMEDPF_Area, &b_JetAK7TRIMMEDPF_Area);
    fChain->SetBranchAddress("JetAK7FILTEREDPF_nJets", &JetAK7FILTEREDPF_nJets, &b_JetAK7FILTEREDPF_nJets);
    fChain->SetBranchAddress("JetAK7FILTEREDPF_Et", JetAK7FILTEREDPF_Et, &b_JetAK7FILTEREDPF_Et);
    fChain->SetBranchAddress("JetAK7FILTEREDPF_Pt", JetAK7FILTEREDPF_Pt, &b_JetAK7FILTEREDPF_Pt);
    fChain->SetBranchAddress("JetAK7FILTEREDPF_Eta", JetAK7FILTEREDPF_Eta, &b_JetAK7FILTEREDPF_Eta);
    fChain->SetBranchAddress("JetAK7FILTEREDPF_Phi", JetAK7FILTEREDPF_Phi, &b_JetAK7FILTEREDPF_Phi);
    fChain->SetBranchAddress("JetAK7FILTEREDPF_Theta", JetAK7FILTEREDPF_Theta, &b_JetAK7FILTEREDPF_Theta);
    fChain->SetBranchAddress("JetAK7FILTEREDPF_Px", JetAK7FILTEREDPF_Px, &b_JetAK7FILTEREDPF_Px);
    fChain->SetBranchAddress("JetAK7FILTEREDPF_Py", JetAK7FILTEREDPF_Py, &b_JetAK7FILTEREDPF_Py);
    fChain->SetBranchAddress("JetAK7FILTEREDPF_Pz", JetAK7FILTEREDPF_Pz, &b_JetAK7FILTEREDPF_Pz);
    fChain->SetBranchAddress("JetAK7FILTEREDPF_E", JetAK7FILTEREDPF_E, &b_JetAK7FILTEREDPF_E);
    fChain->SetBranchAddress("JetAK7FILTEREDPF_Y", JetAK7FILTEREDPF_Y, &b_JetAK7FILTEREDPF_Y);
    fChain->SetBranchAddress("JetAK7FILTEREDPF_Mass", JetAK7FILTEREDPF_Mass, &b_JetAK7FILTEREDPF_Mass);
    fChain->SetBranchAddress("JetAK7FILTEREDPF_Area", JetAK7FILTEREDPF_Area, &b_JetAK7FILTEREDPF_Area);
    fChain->SetBranchAddress("JetAK7PRUNEDPF_nJets", &JetAK7PRUNEDPF_nJets, &b_JetAK7PRUNEDPF_nJets);
    fChain->SetBranchAddress("JetAK7PRUNEDPF_Et", JetAK7PRUNEDPF_Et, &b_JetAK7PRUNEDPF_Et);
    fChain->SetBranchAddress("JetAK7PRUNEDPF_Pt", JetAK7PRUNEDPF_Pt, &b_JetAK7PRUNEDPF_Pt);
    fChain->SetBranchAddress("JetAK7PRUNEDPF_Eta", JetAK7PRUNEDPF_Eta, &b_JetAK7PRUNEDPF_Eta);
    fChain->SetBranchAddress("JetAK7PRUNEDPF_Phi", JetAK7PRUNEDPF_Phi, &b_JetAK7PRUNEDPF_Phi);
    fChain->SetBranchAddress("JetAK7PRUNEDPF_Theta", JetAK7PRUNEDPF_Theta, &b_JetAK7PRUNEDPF_Theta);
    fChain->SetBranchAddress("JetAK7PRUNEDPF_Px", JetAK7PRUNEDPF_Px, &b_JetAK7PRUNEDPF_Px);
    fChain->SetBranchAddress("JetAK7PRUNEDPF_Py", JetAK7PRUNEDPF_Py, &b_JetAK7PRUNEDPF_Py);
    fChain->SetBranchAddress("JetAK7PRUNEDPF_Pz", JetAK7PRUNEDPF_Pz, &b_JetAK7PRUNEDPF_Pz);
    fChain->SetBranchAddress("JetAK7PRUNEDPF_E", JetAK7PRUNEDPF_E, &b_JetAK7PRUNEDPF_E);
    fChain->SetBranchAddress("JetAK7PRUNEDPF_Y", JetAK7PRUNEDPF_Y, &b_JetAK7PRUNEDPF_Y);
    fChain->SetBranchAddress("JetAK7PRUNEDPF_Mass", JetAK7PRUNEDPF_Mass, &b_JetAK7PRUNEDPF_Mass);
    fChain->SetBranchAddress("JetAK7PRUNEDPF_Area", JetAK7PRUNEDPF_Area, &b_JetAK7PRUNEDPF_Area);
    fChain->SetBranchAddress("JetAK5GENJETSNONU_nJets", &JetAK5GENJETSNONU_nJets, &b_JetAK5GENJETSNONU_nJets);
    fChain->SetBranchAddress("JetAK5GENJETSNONU_Et", JetAK5GENJETSNONU_Et, &b_JetAK5GENJETSNONU_Et);
    fChain->SetBranchAddress("JetAK5GENJETSNONU_Pt", JetAK5GENJETSNONU_Pt, &b_JetAK5GENJETSNONU_Pt);
    fChain->SetBranchAddress("JetAK5GENJETSNONU_Eta", JetAK5GENJETSNONU_Eta, &b_JetAK5GENJETSNONU_Eta);
    fChain->SetBranchAddress("JetAK5GENJETSNONU_Phi", JetAK5GENJETSNONU_Phi, &b_JetAK5GENJETSNONU_Phi);
    fChain->SetBranchAddress("JetAK5GENJETSNONU_Theta", JetAK5GENJETSNONU_Theta, &b_JetAK5GENJETSNONU_Theta);
    fChain->SetBranchAddress("JetAK5GENJETSNONU_Px", JetAK5GENJETSNONU_Px, &b_JetAK5GENJETSNONU_Px);
    fChain->SetBranchAddress("JetAK5GENJETSNONU_Py", JetAK5GENJETSNONU_Py, &b_JetAK5GENJETSNONU_Py);
    fChain->SetBranchAddress("JetAK5GENJETSNONU_Pz", JetAK5GENJETSNONU_Pz, &b_JetAK5GENJETSNONU_Pz);
    fChain->SetBranchAddress("JetAK5GENJETSNONU_E", JetAK5GENJETSNONU_E, &b_JetAK5GENJETSNONU_E);
    fChain->SetBranchAddress("JetAK5GENJETSNONU_Y", JetAK5GENJETSNONU_Y, &b_JetAK5GENJETSNONU_Y);
    fChain->SetBranchAddress("JetAK5GENJETSNONU_Mass", JetAK5GENJETSNONU_Mass, &b_JetAK5GENJETSNONU_Mass);
    fChain->SetBranchAddress("JetAK5GENJETSNONU_Area", JetAK5GENJETSNONU_Area, &b_JetAK5GENJETSNONU_Area);
    fChain->SetBranchAddress("JetAK7GENJETSNONU_nJets", &JetAK7GENJETSNONU_nJets, &b_JetAK7GENJETSNONU_nJets);
    fChain->SetBranchAddress("JetAK7GENJETSNONU_Et", JetAK7GENJETSNONU_Et, &b_JetAK7GENJETSNONU_Et);
    fChain->SetBranchAddress("JetAK7GENJETSNONU_Pt", JetAK7GENJETSNONU_Pt, &b_JetAK7GENJETSNONU_Pt);
    fChain->SetBranchAddress("JetAK7GENJETSNONU_Eta", JetAK7GENJETSNONU_Eta, &b_JetAK7GENJETSNONU_Eta);
    fChain->SetBranchAddress("JetAK7GENJETSNONU_Phi", JetAK7GENJETSNONU_Phi, &b_JetAK7GENJETSNONU_Phi);
    fChain->SetBranchAddress("JetAK7GENJETSNONU_Theta", JetAK7GENJETSNONU_Theta, &b_JetAK7GENJETSNONU_Theta);
    fChain->SetBranchAddress("JetAK7GENJETSNONU_Px", JetAK7GENJETSNONU_Px, &b_JetAK7GENJETSNONU_Px);
    fChain->SetBranchAddress("JetAK7GENJETSNONU_Py", JetAK7GENJETSNONU_Py, &b_JetAK7GENJETSNONU_Py);
    fChain->SetBranchAddress("JetAK7GENJETSNONU_Pz", JetAK7GENJETSNONU_Pz, &b_JetAK7GENJETSNONU_Pz);
    fChain->SetBranchAddress("JetAK7GENJETSNONU_E", JetAK7GENJETSNONU_E, &b_JetAK7GENJETSNONU_E);
    fChain->SetBranchAddress("JetAK7GENJETSNONU_Y", JetAK7GENJETSNONU_Y, &b_JetAK7GENJETSNONU_Y);
    fChain->SetBranchAddress("JetAK7GENJETSNONU_Mass", JetAK7GENJETSNONU_Mass, &b_JetAK7GENJETSNONU_Mass);
    fChain->SetBranchAddress("JetAK7GENJETSNONU_Area", JetAK7GENJETSNONU_Area, &b_JetAK7GENJETSNONU_Area);
    fChain->SetBranchAddress("JetCA8GENJETSNONU_nJets", &JetCA8GENJETSNONU_nJets, &b_JetCA8GENJETSNONU_nJets);
    fChain->SetBranchAddress("JetCA8GENJETSNONU_Et", JetCA8GENJETSNONU_Et, &b_JetCA8GENJETSNONU_Et);
    fChain->SetBranchAddress("JetCA8GENJETSNONU_Pt", JetCA8GENJETSNONU_Pt, &b_JetCA8GENJETSNONU_Pt);
    fChain->SetBranchAddress("JetCA8GENJETSNONU_Eta", JetCA8GENJETSNONU_Eta, &b_JetCA8GENJETSNONU_Eta);
    fChain->SetBranchAddress("JetCA8GENJETSNONU_Phi", JetCA8GENJETSNONU_Phi, &b_JetCA8GENJETSNONU_Phi);
    fChain->SetBranchAddress("JetCA8GENJETSNONU_Theta", JetCA8GENJETSNONU_Theta, &b_JetCA8GENJETSNONU_Theta);
    fChain->SetBranchAddress("JetCA8GENJETSNONU_Px", JetCA8GENJETSNONU_Px, &b_JetCA8GENJETSNONU_Px);
    fChain->SetBranchAddress("JetCA8GENJETSNONU_Py", JetCA8GENJETSNONU_Py, &b_JetCA8GENJETSNONU_Py);
    fChain->SetBranchAddress("JetCA8GENJETSNONU_Pz", JetCA8GENJETSNONU_Pz, &b_JetCA8GENJETSNONU_Pz);
    fChain->SetBranchAddress("JetCA8GENJETSNONU_E", JetCA8GENJETSNONU_E, &b_JetCA8GENJETSNONU_E);
    fChain->SetBranchAddress("JetCA8GENJETSNONU_Y", JetCA8GENJETSNONU_Y, &b_JetCA8GENJETSNONU_Y);
    fChain->SetBranchAddress("JetCA8GENJETSNONU_Mass", JetCA8GENJETSNONU_Mass, &b_JetCA8GENJETSNONU_Mass);
    fChain->SetBranchAddress("JetCA8GENJETSNONU_Area", JetCA8GENJETSNONU_Area, &b_JetCA8GENJETSNONU_Area);
    fChain->SetBranchAddress("event_runNo", &event_runNo, &b_event_runNo);
    fChain->SetBranchAddress("event_evtNo", &event_evtNo, &b_event_evtNo);
    fChain->SetBranchAddress("event_lumi", &event_lumi, &b_event_lumi);
    fChain->SetBranchAddress("event_bunch", &event_bunch, &b_event_bunch);
    fChain->SetBranchAddress("event_nPV", &event_nPV, &b_event_nPV);
    fChain->SetBranchAddress("event_PVx", event_PVx, &b_event_PVx);
    fChain->SetBranchAddress("event_PVy", event_PVy, &b_event_PVy);
    fChain->SetBranchAddress("event_PVz", event_PVz, &b_event_PVz);
    fChain->SetBranchAddress("eventClass", &eventClass, &b_event_Class);
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
    
    
    otree = new TTree( "otree", "otree" );
    
    otree->Branch("e_puwt", &e_puwt, "e_puwt/D");
    otree->Branch("e_puwt_up", &e_puwt_up, "e_puwt_up/D");
    otree->Branch("e_puwt_dn", &e_puwt_dn, "e_puwt_dn/D");
    otree->Branch("e_effwt", &e_effwt, "e_effwt/D");
    
    otree->Branch("e_met", &e_met, "e_met/D");
    otree->Branch("e_nvert", &e_nvert, "e_nvert/D");
    otree->Branch("e_weight", &e_weight, "e_weight/D");
    otree->Branch("w_mt", &w_mt, "w_mt/D");
    otree->Branch("w_pt", &w_pt, "w_pt/D");
    otree->Branch("l_pt", &l_pt, "l_pt/D");
    otree->Branch("l_reliso", &l_reliso, "l_reliso/D");
    otree->Branch("j_ak5_nJ", &j_ak5_nJ, "j_ak5_nJ/D");
    otree->Branch("j_ak5_mu", &j_ak5_mu, "j_ak5_mu/D");
    otree->Branch("j_ak5_bdis", &j_ak5_bdis, "j_ak5_bdis/D");
    otree->Branch("j_ak5_eta", &j_ak5_eta, "j_ak5_eta/D");
    otree->Branch("j_ak5_phi", &j_ak5_phi, "j_ak5_phi/D");
    otree->Branch("j_ak5_pt", &j_ak5_pt, "j_ak5_pt/D");
    otree->Branch("j_ak5_p", &j_ak5_p, "j_ak5_p/D");
    otree->Branch("j_ak5_mass", &j_ak5_mass, "j_ak5_mass/D");
    otree->Branch("j_ak5_area", &j_ak5_area, "j_ak5_area/D");
    
    otree->Branch("j_ak5tr_mass", &j_ak5tr_mass, "j_ak5tr_mass/D");
    otree->Branch("j_ak5pr_mass", &j_ak5pr_mass, "j_ak5pr_mass/D");
    otree->Branch("j_ak5ft_mass", &j_ak5ft_mass, "j_ak5ft_mass/D");

    otree->Branch("j_ak7_mass", &j_ak7_mass, "j_ak7_mass/D");
    otree->Branch("j_ak7tr_mass", &j_ak7tr_mass, "j_ak7tr_mass/D");
    otree->Branch("j_ak7pr_mass", &j_ak7pr_mass, "j_ak7pr_mass/D");
    otree->Branch("j_ak7ft_mass", &j_ak7ft_mass, "j_ak7ft_mass/D");

    otree->Branch("j_ca8_mass", &j_ca8_mass, "j_ca8_mass/D");
    otree->Branch("j_ca8pr_mass", &j_ca8pr_mass, "j_ca8pr_mass/D");

}

Bool_t vJetSubstructureAnalysis::Notify()
{
    // The Notify() function is called when a new file is opened. This
    // can be either for a new TTree in a TChain or when when a new TTree
    // is started when using PROOF. It is normally not necessary to make changes
    // to the generated code, but the routine can be extended by the
    // user if needed. The return value is currently not used.
    
    return kTRUE;
}

void vJetSubstructureAnalysis::Show(Long64_t entry)
{
    // Print contents of entry.
    // If entry is not specified, print current entry
    if (!fChain) return;
    fChain->Show(entry);
}
Int_t vJetSubstructureAnalysis::Cut(Long64_t entry)
{
    // This function may be called from Loop.
    // returns  1 if entry is accepted.
    // returns -1 otherwise.
    return 1;
}
#endif // #ifdef vJetSubstructureAnalysis_cxx
