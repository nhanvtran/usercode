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
    
    if (fChain == 0) return;
    
    Long64_t nentries = fChain->GetEntriesFast();
    std::cout << "nentries: " << nentries << std::endl;
    
    Long64_t nbytes = 0, nb = 0;
    Long64_t ctr = 0.;
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

            
            if (b_eleWP80 && b_phasespace && b_trigger){
                
                //std::cout << "good event with e_pt = " << l_pt << std::endl;
                j_ak5_bdis = JetAK5PF_bDiscSSVHE[0];
                j_ak5_eta = JetAK5PF_Eta[0];
                j_ak5_phi = JetAK5PF_Phi[0];
                j_ak5_pt = JetAK5PF_Pt[0];
                j_ak5_mass = JetAK5PF_Mass[0];
                j_ak5_area = JetAK5PF_Area[0];
                j_ak5_nJ = JetAK5PF_nJets;

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

                otree->Fill();
            }
        }
        
        /////////////////////////////////////////
        
        ctr++;
        if (ctr % 10000 == 0) std::cout << "cur ctr: " << ctr << std::endl;
        if ((ctr > MAXEVENTS)&&(MAXEVENTS > 0)) break;
    }
    std::cout << "ctr: " << ctr << std::endl;
}
