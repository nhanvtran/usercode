#define vJetSubstructureAnalysis_cxx
#include "vJetSubstructureAnalysis.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <iostream>

#include "PhysicsTools/KinFitter/interface/TFitConstraintMGaus.h"
#include "PhysicsTools/KinFitter/interface/TFitConstraintM.h"
#include "PhysicsTools/KinFitter/interface/TFitConstraintEp.h"
#include "PhysicsTools/KinFitter/interface/TFitParticleEtEtaPhi.h"
#include "PhysicsTools/KinFitter/interface/TFitParticleCart.h"
#include "PhysicsTools/KinFitter/interface/TKinFitter.h"

#include "EffTableReader.h"
#include "EffTableLoader.h"

#include "PhysicsTools/Utilities/interface/Lumi3DReWeighting.h"
#include "PhysicsTools/Utilities/interface/LumiReweightingStandAlone.h"

#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"

using namespace std;

void vJetSubstructureAnalysis::Loop(Long64_t maxevents)
{
    
    Long64_t MAXEVENTS = maxevents;
    
    /////////////////////////////////////////
    // P i l e   u p   R e - w e i g h t i n g 
    edm::Lumi3DReWeighting LumiWeights_ = edm::Lumi3DReWeighting("PUMC_dist.root", "PUData_dist.root", "pileup", "pileup", "Weight_3D.root");
    LumiWeights_.weight3D_init( 1.08 );
    
    edm::Lumi3DReWeighting up_LumiWeights_ = edm::Lumi3DReWeighting("PUMC_dist.root", "PUData_dist.root", "pileup", "pileup", "Weight_3D_up.root");
    up_LumiWeights_.weight3D_init( 1.16 );
    
    edm::Lumi3DReWeighting dn_LumiWeights_ = edm::Lumi3DReWeighting("PUMC_dist.root", "PUData_dist.root", "pileup", "pileup", "Weight_3D_down.root");
    dn_LumiWeights_.weight3D_init( 1.00 );
    /////////////////////////////////////////
    
    /////////////////////////////////////////
    // E f f i c i e n c y   C o r r e c t i o n s
    const std::string fDir   = "EffTableDir/";
    // For Muon Efficiency Correction
    EffTableLoader muIDEff(            fDir + "muonEffsRecoToIso_ScaleFactors.txt");
    EffTableLoader muHLTEff(           fDir + "muonEffsIsoToHLT_data_LP_LWA.txt");

    // For Electron Efficiency Correction
    EffTableLoader eleIdEff(         fDir + "eleEffsRecoToWP80_ScaleFactors.txt");
    EffTableLoader eleRecoEff(       fDir + "eleEffsSCToReco_ScaleFactors.txt");
    EffTableLoader eleHLTEff(        fDir + "eleEffsSingleElectron.txt");
    EffTableLoader eleJ30Eff(        fDir + "FullyEfficient.txt");
    EffTableLoader eleJ25NoJ30Eff(   fDir + "FullyEfficient_Jet2NoJet1.txt");
    EffTableLoader eleMHTEff(        fDir + "FullyEfficient_MHT.txt");
    EffTableLoader eleWMtEff(        fDir + "WMt50TriggerEfficiency.txt");
    /////////////////////////////////////////
    
    /////////////////////////////////////////
    // J e t   c o r r e c t i o n s   o n   t h e   f l y
    
    ///*
    std::string L1Tag    = "../data/Jec11V0_L1Offset_AK5JPT.txt"; 
    std::string L1JPTTag = "../data/Jec11V0_L1JPTOffset_AK5JPT.txt"; 
    JetCorrectorParameters *L1Par    = new JetCorrectorParameters(L1Tag);
    JetCorrectorParameters *L1JPTPar = new JetCorrectorParameters(L1JPTTag);
    vector<JetCorrectorParameters> vPar;
    vPar.push_back(*L1Par);
     vPar.push_back(*L1JPTPar);
    //*/
    ////////////// Construct a FactorizedJetCorrector object //////////////////////
    //FactorizedJetCorrector *JetCorrector = new FactorizedJetCorrector(vPar);
    //FactorizedJetCorrector *JetCorrector;
    /////////////////////////////////////////
    
    if (fChain == 0) return;
    
    Long64_t nentries = fChain->GetEntriesFast();
    std::cout << "nentries: " << nentries << std::endl;
    
    Long64_t nbytes = 0, nb = 0;
    Long64_t ctr = 0.;
    
    // counters
    ctr_class1_matched_ak5 = 0.;
    ctr_class1_unmatched_ak5 = 0.;
    ctr_class1_matched_ak7 = 0.;
    ctr_class1_unmatched_ak7 = 0.;
    ctr_class1_matched_ak8 = 0.;
    ctr_class1_unmatched_ak8 = 0.;
    ctr_class1_matched_ca8 = 0.;
    ctr_class1_unmatched_ca8 = 0.;
    
    ctr50_class1_matched_ak5 = 0.;
    ctr50_class1_unmatched_ak5 = 0.;
    ctr50_class1_matched_ak7 = 0.;
    ctr50_class1_unmatched_ak7 = 0.;
    ctr50_class1_matched_ak8 = 0.;
    ctr50_class1_unmatched_ak8 = 0.;
    ctr50_class1_matched_ca8 = 0.;
    ctr50_class1_unmatched_ca8 = 0.;
        
    for (Long64_t jentry=0; jentry<nentries;jentry++) {
        Long64_t ientry = LoadTree(jentry);
        if (ientry < 0) break;
        nb = fChain->GetEntry(jentry);   nbytes += nb;
        /////////////////////////////////////////
        // P i l e   u p   R e - w e i g h t i n g 
        e_puwt      =    LumiWeights_.weight3D(event_mcPU_nvtx[0], event_mcPU_nvtx[1], event_mcPU_nvtx[2]);   
        e_puwt_up   = up_LumiWeights_.weight3D(event_mcPU_nvtx[0], event_mcPU_nvtx[1], event_mcPU_nvtx[2]);   
        e_puwt_dn = dn_LumiWeights_.weight3D(event_mcPU_nvtx[0], event_mcPU_nvtx[1], event_mcPU_nvtx[2]);   
        
        /////////////////////////////////////////
        // E V E N T   L O O P   C O R E 
        // Wenu event loop
        if (eventClass == 1){
            
            // 1. Make some loose W selections
            bool b_eleWP80 = Wel_electron_isWP80;
            
            bool b_trigger1 = false; if ((JetAK5PF_Pt[0] > 0)&&(Wel_electron_pt > 27)) b_trigger1 = true;
            bool b_trigger2 = false; if (Wel_electron_pt > 40) b_trigger2 = true;
            bool b_trigger = b_trigger1 || b_trigger2;
            
            bool b_elept = false; if (Wel_electron_pt > 35) b_elept = true;
            //bool b_jetpt = false; if (JetgoodPatJetsCA8PrunedPF_Mass[0] > 150) b_jetpt = true;
            bool b_phasespace = b_elept;// && b_jetpt;
            
            double ele_reliso = (Wel_electron_trackiso + Wel_electron_hcaliso + Wel_electron_ecaliso)/Wel_electron_et;

            b_trigger = true;
            
            w_mt = Wel_mt;
            w_pt = Wel_pt;
            e_met = event_met_pfmet;
            l_pt = Wel_electron_pt;
            l_reliso = ele_reliso;
            e_nvert = (double) event_nPV;
            //e_weight = weightFactor;
            
            /////////////////////////////////////////
            // Calculate efficiency
            e_effwt = eleIdEff.GetEfficiency(Wel_electron_pt, Wel_electron_eta) * 
            eleRecoEff.GetEfficiency(Wel_electron_pt, Wel_electron_eta) *
            eleHLTEff.GetEfficiency(Wel_electron_pt, Wel_electron_eta) *
            eleMHTEff.GetEfficiency(event_met_pfmet, 0) *
            eleWMtEff.GetEfficiency(Wel_mt, Wel_electron_eta);
            /////////////////////////////////////////

            bool b_jets = false;
            if ((JetAK5PF_nJets + JetAK7PF_nJets + JetAK8PF_nJets + JetCA8PF_nJets) > 0) b_jets = true;
            
            
            if (b_eleWP80 && b_phasespace && b_trigger && b_jets){
                
                FillTree();

            }

        }
        
        /////////////////////////////////////////
        
        ctr++;
        if (ctr % 10000 == 0) std::cout << "cur ctr: " << ctr << std::endl;
        if ((ctr > MAXEVENTS)&&(MAXEVENTS > 0)) break;
    }
    std::cout << "ctr: " << ctr << std::endl;
    std::cout << "ctr_class1_matched_ak5: " << ctr_class1_matched_ak5 << std::endl;
    std::cout << "ctr_class1_unmatched_ak5: " << ctr_class1_unmatched_ak5 << std::endl;
    std::cout << "ctr_class1_matched_ak7: " << ctr_class1_matched_ak7 << std::endl;
    std::cout << "ctr_class1_unmatched_ak7: " << ctr_class1_unmatched_ak7 << std::endl;
    std::cout << "ctr_class1_matched_ak8: " << ctr_class1_matched_ak8 << std::endl;
    std::cout << "ctr_class1_unmatched_ak8: " << ctr_class1_unmatched_ak8 << std::endl;
    std::cout << "ctr_class1_matched_ca8: " << ctr_class1_matched_ca8 << std::endl;
    std::cout << "ctr_class1_unmatched_ca8: " << ctr_class1_unmatched_ca8 << std::endl;

    std::cout << "ctr50_class1_matched_ak5: " << ctr50_class1_matched_ak5 << std::endl;
    std::cout << "ctr50_class1_unmatched_ak5: " << ctr50_class1_unmatched_ak5 << std::endl;
    std::cout << "ctr50_class1_matched_ak7: " << ctr50_class1_matched_ak7 << std::endl;
    std::cout << "ctr50_class1_unmatched_ak7: " << ctr50_class1_unmatched_ak7 << std::endl;
    std::cout << "ctr50_class1_matched_ak8: " << ctr50_class1_matched_ak8 << std::endl;
    std::cout << "ctr50_class1_unmatched_ak8: " << ctr50_class1_unmatched_ak8 << std::endl;
    std::cout << "ctr50_class1_matched_ca8: " << ctr50_class1_matched_ca8 << std::endl;
    std::cout << "ctr50_class1_unmatched_ca8: " << ctr50_class1_unmatched_ca8 << std::endl;
}

void vJetSubstructureAnalysis::FillTree()
{
    
    j_ak5_bdis = JetAK5PF_bDiscSSVHE[0];
    j_ak5_eta = JetAK5PF_Eta[0];
    j_ak5_phi = JetAK5PF_Phi[0];
    j_ak5_pt = JetAK5PF_Pt[0];
    j_ak5_mass = JetAK5PF_Mass[0];
    j_ak5_area = JetAK5PF_Area[0];
    j_ak5_nJ = JetAK5PF_nJets;
    j_ak5_nBtags = JetAK5PF_nJetBTags;
    j_ak5_jecfactor = (double) JetAK5PF_JecFactor[0];

    j_ak5tr_mass = JetAK5TRIMMEDPF_Mass[0];
    j_ak5pr_mass = JetAK5PRUNEDPF_Mass[0];
    j_ak5ft_mass = JetAK5FILTEREDPF_Mass[0];
    j_ak7_mass = JetAK7PF_Mass[0];
    j_ak7tr_mass = JetAK7TRIMMEDPF_Mass[0];
    j_ak7pr_mass = JetAK7PRUNEDPF_Mass[0];
    j_ak7ft_mass = JetAK7FILTEREDPF_Mass[0];
    j_ak8_mass = JetAK8PF_Mass[0];
    j_ak8tr_mass = JetAK8TRIMMEDPF_Mass[0];
    j_ak8pr_mass = JetAK8PRUNEDPF_Mass[0];
    j_ak8ft_mass = JetAK8FILTEREDPF_Mass[0];
    j_ca8_mass = JetCA8PF_Mass[0];
    j_ca8pr_mass = JetCA8PRUNEDPF_Mass[0];
    j_ca12ft_mass = (double) JetCA12FILTEREDPF_Mass[0];
    j_ca12mdft_mass = (double) JetCA12MASSDROPFILTEREDPF_Mass[0];

    j_ak5tr_pt = JetAK5TRIMMEDPF_Pt[0];
    j_ak5pr_pt = JetAK5PRUNEDPF_Pt[0];
    j_ak5ft_pt = JetAK5FILTEREDPF_Pt[0];
    j_ak7_pt = JetAK7PF_Pt[0];
    j_ak7tr_pt = JetAK7TRIMMEDPF_Pt[0];
    j_ak7pr_pt = JetAK7PRUNEDPF_Pt[0];
    j_ak7ft_pt = JetAK7FILTEREDPF_Pt[0];
    j_ak8_pt = JetAK8PF_Pt[0];
    j_ak8tr_pt = JetAK8TRIMMEDPF_Pt[0];
    j_ak8pr_pt = JetAK8PRUNEDPF_Pt[0];
    j_ak8ft_pt = JetAK8FILTEREDPF_Pt[0];
    j_ca8_pt = JetCA8PF_Pt[0];
    j_ca8pr_pt = JetCA8PRUNEDPF_Pt[0];
    j_ca12ft_pt = (double) JetCA12FILTEREDPF_Pt[0];
    j_ca12mdft_pt = (double) JetCA12MASSDROPFILTEREDPF_Pt[0];

    j_ak5tr_nJ = (double) JetAK5TRIMMEDPF_nJets;
    j_ak5pr_nJ = (double) JetAK5PRUNEDPF_nJets;
    j_ak5ft_nJ = (double) JetAK5FILTEREDPF_nJets;
    j_ak7_nJ = (double) JetAK7PF_nJets;
    j_ak7tr_nJ = (double) JetAK7TRIMMEDPF_nJets;
    j_ak7pr_nJ = (double) JetAK7PRUNEDPF_nJets;
    j_ak7ft_nJ = (double) JetAK7FILTEREDPF_nJets;
    j_ak8_nJ = (double) JetAK8PF_nJets;
    j_ak8tr_nJ = (double) JetAK8TRIMMEDPF_nJets;
    j_ak8pr_nJ = (double) JetAK8PRUNEDPF_nJets;
    j_ak8ft_nJ = (double) JetAK8FILTEREDPF_nJets;
    j_ca8_nJ = (double) JetCA8PF_nJets;
    j_ca8pr_nJ = (double) JetCA8PRUNEDPF_nJets;
    j_ca12ft_nJ = (double) JetCA12FILTEREDPF_nJets;
    j_ca12mdft_nJ = (double) JetCA12MASSDROPFILTEREDPF_nJets;

    j_ak5tr_area = (double) JetAK5TRIMMEDPF_Area[0];
    j_ak5pr_area = (double) JetAK5PRUNEDPF_Area[0];
    j_ak5ft_area = (double) JetAK5FILTEREDPF_Area[0];
    j_ak7_area = (double) JetAK7PF_Area[0];
    j_ak7tr_area = (double) JetAK7TRIMMEDPF_Area[0];
    j_ak7pr_area = (double) JetAK7PRUNEDPF_Area[0];
    j_ak7ft_area = (double) JetAK7FILTEREDPF_Area[0];
    j_ak8_area = (double) JetAK8PF_Area[0];
    j_ak8tr_area = (double) JetAK8TRIMMEDPF_Area[0];
    j_ak8pr_area = (double) JetAK8PRUNEDPF_Area[0];
    j_ak8ft_area = (double) JetAK8FILTEREDPF_Area[0];
    j_ca8_area = (double) JetCA8PF_Area[0];
    j_ca8pr_area = (double) JetCA8PRUNEDPF_Area[0];
    j_ca12ft_area = (double) JetCA12FILTEREDPF_Area[0];
    j_ca12mdft_area = (double) JetCA12MASSDROPFILTEREDPF_Area[0];

    j_ak5tr_jecfactor = (double) JetAK5TRIMMEDPF_JecFactor[0];
    j_ak5pr_jecfactor = (double) JetAK5PRUNEDPF_JecFactor[0];
    j_ak5ft_jecfactor = (double) JetAK5FILTEREDPF_JecFactor[0];
    j_ak7_jecfactor = (double) JetAK7PF_JecFactor[0];
    j_ak7tr_jecfactor = (double) JetAK7TRIMMEDPF_JecFactor[0];
    j_ak7pr_jecfactor = (double) JetAK7PRUNEDPF_JecFactor[0];
    j_ak7ft_jecfactor = (double) JetAK7FILTEREDPF_JecFactor[0];
    j_ak8_jecfactor = (double) JetAK8PF_JecFactor[0];
    j_ak8tr_jecfactor = (double) JetAK8TRIMMEDPF_JecFactor[0];
    j_ak8pr_jecfactor = (double) JetAK8PRUNEDPF_JecFactor[0];
    j_ak8ft_jecfactor = (double) JetAK8FILTEREDPF_JecFactor[0];
    j_ca8_jecfactor = (double) JetCA8PF_JecFactor[0];
    j_ca8pr_jecfactor = (double) JetCA8PRUNEDPF_JecFactor[0];
    j_ca12ft_jecfactor = (double) JetCA12FILTEREDPF_JecFactor[0];
    j_ca12mdft_jecfactor = (double) JetCA12MASSDROPFILTEREDPF_JecFactor[0];
    
    j_ca8pr_m1 = (double) JetCA8PRUNEDPF_subJet1Mass[0];
    j_ca8pr_m2 = (double) JetCA8PRUNEDPF_subJet2Mass[0];
    
    int ngenjets = 8;
    
    // gen jet information
    // do a delta R matching of 0.3                                
    int matchIndex_ak5 = -1;
    double toler = 100.;
    int maxLoop = JetAK5GENJETSNONU_nJets;
    if (maxLoop > ngenjets) maxLoop = ngenjets;
    for (int k = 0; k < maxLoop; k++){
        Double_t deta = JetAK5PF_Eta[0]-JetAK5GENJETSNONU_Eta[k];
        Double_t dphi = TVector2::Phi_mpi_pi(JetAK5PF_Phi[0]-JetAK5GENJETSNONU_Phi[k]);
        double deltaR = TMath::Sqrt( deta*deta+dphi*dphi );
        //std::cout << "deltaR (ak5): " << deltaR << std::endl;
        if (deltaR < 0.3 && deltaR < toler){ matchIndex_ak5 = k; toler = deltaR; }
    }
    int matchIndex_ak7 = -1;
    toler = 100.;
    maxLoop = JetAK7GENJETSNONU_nJets;
    if (maxLoop > ngenjets) maxLoop = ngenjets;
    for (int k = 0; k < maxLoop; k++){
        Double_t deta = JetAK7PF_Eta[0]-JetAK7GENJETSNONU_Eta[k];
        Double_t dphi = TVector2::Phi_mpi_pi(JetAK7PF_Phi[0]-JetAK7GENJETSNONU_Phi[k]);
        double deltaR = TMath::Sqrt( deta*deta+dphi*dphi );
        //std::cout << "deltaR (ak7): " << deltaR << std::endl;
        if (deltaR < 0.3 && deltaR < toler){ matchIndex_ak7 = k; toler = deltaR; }
    }
    int matchIndex_ak8 = -1;
    toler = 100.;
    maxLoop = JetAK8GENJETSNONU_nJets;
    if (maxLoop > ngenjets) maxLoop = ngenjets;
    for (int k = 0; k < maxLoop; k++){
        Double_t deta = JetAK8PF_Eta[0]-JetAK8GENJETSNONU_Eta[k];
        Double_t dphi = TVector2::Phi_mpi_pi(JetAK8PF_Phi[0]-JetAK8GENJETSNONU_Phi[k]);
        double deltaR = TMath::Sqrt( deta*deta+dphi*dphi );
        //std::cout << "deltaR (ak8): " << deltaR << std::endl;
        if (deltaR < 0.3 && deltaR < toler){ matchIndex_ak8 = k; toler = deltaR; }
    }
    int matchIndex_ca8 = -1;
    toler = 100.;
    maxLoop = JetCA8GENJETSNONU_nJets;
    if (maxLoop > ngenjets) maxLoop = ngenjets;
    for (int k = 0; k < maxLoop; k++){
        Double_t deta = JetCA8PF_Eta[0]-JetCA8GENJETSNONU_Eta[k];
        Double_t dphi = TVector2::Phi_mpi_pi(JetCA8PF_Phi[0]-JetCA8GENJETSNONU_Phi[k]);
        double deltaR = TMath::Sqrt( deta*deta+dphi*dphi );
        //std::cout << "deltaR (ca8): " << deltaR << std::endl;
        if (deltaR < 0.3 && deltaR < toler){ matchIndex_ca8 = k; toler = deltaR; }
    }
    
    
    ////////////////////////
    // M a t c h   c o u n t i n g
    if (matchIndex_ak5 < 0){
        //std::cout << "WARNING -- No Gen Jet Match for ak5! " << std::endl;
        ctr_class1_unmatched_ak5++;
        j_ak5_match = 0;
        if (JetAK5PF_Pt[0] > 50){
            ctr50_class1_unmatched_ak5++;
        }
    }
    else{
        ctr_class1_matched_ak5++;
        j_ak5_match = 1;
        if (JetAK5PF_Pt[0] > 50){
            ctr50_class1_matched_ak5++;
        }
    }
    ////////////////////////
    if (matchIndex_ak7 < 0){
        //std::cout << "WARNING -- No Gen Jet Match for ak7! " << std::endl;
        ctr_class1_unmatched_ak7++;
        j_ak7_match = 0;
        if (JetAK7PF_Pt[0] > 50){
            ctr50_class1_unmatched_ak7++;
        }
    }
    else{
        ctr_class1_matched_ak7++;
        j_ak7_match = 1;
        if (JetAK7PF_Pt[0] > 50){
            ctr50_class1_matched_ak7++;
        }                }
    ////////////////////////
    if (matchIndex_ak8 < 0){
        //std::cout << "WARNING -- No Gen Jet Match for ak8! " << std::endl;
        ctr_class1_unmatched_ak8++;
        j_ak8_match = 0;
        if (JetAK8PF_Pt[0] > 50){
            ctr50_class1_unmatched_ak8++;
        }
    }
    else{
        ctr_class1_matched_ak8++;
        j_ak8_match = 1;
        if (JetAK8PF_Pt[0] > 50){
            ctr50_class1_matched_ak8++;
        }                }
    ////////////////////////
    if (matchIndex_ca8 < 0){
        //std::cout << "WARNING -- No Gen Jet Match for ca8! " << std::endl;
        ctr_class1_unmatched_ca8++;
        j_ca8_match = 0;
        if (JetCA8PF_Pt[0] > 50){
            ctr50_class1_unmatched_ca8++;
        }
    }
    else{
        ctr_class1_matched_ca8++;
        j_ca8_match = 1;
        if (JetCA8PF_Pt[0] > 50){
            ctr50_class1_matched_ca8++;
        }
    }
    ////////////////////////
    
    //std::cout << "-----------" << std::endl;
    j_ak5g_mass = JetAK5GENJETSNONU_Mass[matchIndex_ak5];
    j_ak5g_pt = JetAK5GENJETSNONU_Pt[matchIndex_ak5];
    j_ak5g_nJ = JetAK5GENJETSNONU_nJets;
    j_ak5g_area = JetAK5GENJETSNONU_Area[matchIndex_ak5];
    
    j_ak7g_mass = JetAK7GENJETSNONU_Mass[matchIndex_ak7];
    j_ak7g_pt = JetAK7GENJETSNONU_Pt[matchIndex_ak7];
    j_ak7g_nJ = JetAK7GENJETSNONU_nJets;
    j_ak7g_area = JetAK7GENJETSNONU_Area[matchIndex_ak7];
    
    j_ak8g_mass = JetAK8GENJETSNONU_Mass[matchIndex_ak8];
    j_ak8g_pt = JetAK8GENJETSNONU_Pt[matchIndex_ak8];
    j_ak8g_nJ = JetAK8GENJETSNONU_nJets;
    j_ak8g_area = JetAK8GENJETSNONU_Area[matchIndex_ak8];
    
    j_ca8g_mass = JetCA8GENJETSNONU_Mass[matchIndex_ca8];
    j_ca8g_pt = JetCA8GENJETSNONU_Pt[matchIndex_ca8];
    j_ca8g_nJ = JetCA8GENJETSNONU_nJets;
    j_ca8g_area = JetCA8GENJETSNONU_Area[matchIndex_ca8];
    
    //
    
    otree->Fill();
    
    
}
