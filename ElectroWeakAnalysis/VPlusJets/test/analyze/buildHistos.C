#define buildHistos_cxx
#include "buildHistos.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <iostream>

void buildHistos::Loop(double sampleSclFactor)
{
    //   In a ROOT session, you can do:
    //      Root > .L buildHistos.C
    //      Root > buildHistos t
    //      Root > t.GetEntry(12); // Fill t data members with entry number 12
    //      Root > t.Show();       // Show values of entry 12
    //      Root > t.Show(16);     // Read and show values of entry 16
    //      Root > t.Loop();       // Loop on all entries
    //
    
    //     This is the loop skeleton where:
    //    jentry is the global entry number in the chain
    //    ientry is the entry number in the current Tree
    //  Note that the argument to GetEntry must be:
    //    jentry for TChain::GetEntry
    //    ientry for TTree::GetEntry and TBranch::GetEntry
    //
    //       To read only selected branches, Insert statements like:
    // METHOD1:
    //    fChain->SetBranchStatus("*",0);  // disable all branches
    //    fChain->SetBranchStatus("branchname",1);  // activate branchname
    // METHOD2: replace line
    //    fChain->GetEntry(jentry);       //read all branches
    //by  b_branchname->GetEntry(ientry); //read only this branch
   
    // things left to do
    // 1. put in profile plots
    // 2. get gen-matched jets
    // 3. compare to data
    // 4. include mechanism for weights
    // 5. put in something for the different files - check
    
    double sclF_fromMC = sampleSclFactor;
    
    int i_ak5 = findIndexForJetType( "ak5" );
    int i_ak7 = findIndexForJetType( "ak7" );        
    int i_ak8 = findIndexForJetType( "ak8" );
    
    if (fChain == 0) return;
    
    Long64_t nentries = fChain->GetEntriesFast();
    
    Long64_t nbytes = 0, nb = 0;
    for (Long64_t jentry=0; jentry<nentries;jentry++) {
        Long64_t ientry = LoadTree(jentry);
        if (ientry < 0) break;
        nb = fChain->GetEntry(jentry);   nbytes += nb;
                
        // code for combining scale factors
        // get PU SF
        // get trigger SF
        // get lepton SF
        double totSF = 1./sclF_fromMC;
        
        
        h_w_mt->Fill( w_mt, totSF );
        h_w_pt->Fill( w_pt, totSF );
        h_e_met->Fill( e_met, totSF );
        h_l_pt->Fill( w_pt, totSF );
        
        // -----------------------------------------
        // filling jet histograms
        for (int i = 0; i < nJetTypes; i++){            

            h_j_nJ[i]->Fill( j_nJ[i], totSF );
            h_j_mass[i]->Fill( j_mass[i], totSF );
            h_j_area[i]->Fill( j_area[i], totSF );
            h_j_pt[i]->Fill( j_pt[i], totSF );
            
            
            if ( jetTypes[i] == "ak5" ){
                h_j_bdis[i]->Fill( j_bdis[i], totSF );
                h_j_eta[i]->Fill( j_eta[i], totSF );
                h_j_phi[i]->Fill( j_phi[i], totSF );
                h_j_p[i]->Fill( j_p[i], totSF );
            }
            
            // in bins of pT
            if ((j_pt[i] > 50)&&(j_pt[i] <= 100)){ h_j_mass_pt50to100[i]->Fill(j_mass[i], totSF); }
            else if ((j_pt[i] > 100)&&(j_pt[i] <= 150)){ h_j_mass_pt100to150[i]->Fill(j_mass[i], totSF); }
            else if ((j_pt[i] > 150)&&(j_pt[i] <= 200)){ h_j_mass_pt150to200[i]->Fill(j_mass[i], totSF); }
            else if ((j_pt[i] > 200)&&(j_pt[i] <= 300)){ h_j_mass_pt200to300[i]->Fill(j_mass[i], totSF); }
            else if (j_pt[i] > 300){ h_j_mass_pt300andup[i]->Fill(j_mass[i], totSF); }
            else { continue; }
            
            //profile
            p_j_massvpt[i]->Fill( j_pt[i], j_mass[i], totSF );
            p_j_massvNV[i]->Fill( e_nvert, j_mass[i], totSF );            
            // ratios
            p_j_massOverAK5[i]->Fill( j_pt[i], j_mass[i]/j_mass[i_ak5], totSF );
            p_j_massOverAK7[i]->Fill( j_pt[i], j_mass[i]/j_mass[i_ak7], totSF );
            p_j_massOverAK8[i]->Fill( j_pt[i], j_mass[i]/j_mass[i_ak8], totSF );
            p_j_ptOverAK5[i]->Fill( j_pt[i], j_pt[i]/j_pt[i_ak5], totSF );
            p_j_ptOverAK7[i]->Fill( j_pt[i], j_pt[i]/j_pt[i_ak7], totSF );
            p_j_ptOverAK8[i]->Fill( j_pt[i], j_pt[i]/j_pt[i_ak8], totSF );

            
        }
        // -----------------------------------------
        
        
        if (jentry % 100000 == 0) std::cout << "jentry: " << jentry << std::endl;
    }
    
    
    //TFile* fout = new TFile("out.root","RECREATE");
    fout->cd();
    h_w_mt->Write();
    h_w_pt->Write();
    h_e_met->Write();
    h_l_pt->Write();
    std::cout << "nJetTypes: " << nJetTypes << std::endl;
    for (int i = 0; i < nJetTypes; i++){
        
        h_j_nJ[i]->Write();
        h_j_mass[i]->Write();
        h_j_area[i]->Write();
        h_j_pt[i]->Write();
        
        if ( jetTypes[i] == "ak5" ){
            h_j_bdis[i]->Write();
            h_j_eta[i]->Write();
            h_j_phi[i]->Write();
            h_j_p[i]->Write();
        }        
        
        h_j_mass_pt50to100[i]->Write();
        h_j_mass_pt100to150[i]->Write();
        h_j_mass_pt150to200[i]->Write();
        h_j_mass_pt200to300[i]->Write();
        h_j_mass_pt300andup[i]->Write();
        
        p_j_massvpt[i]->Write();
        p_j_massvNV[i]->Write();
        
        p_j_massOverAK5[i]->Write();
        p_j_massOverAK7[i]->Write();
        p_j_massOverAK8[i]->Write();
        p_j_ptOverAK5[i]->Write();
        p_j_ptOverAK7[i]->Write();
        p_j_ptOverAK8[i]->Write();
        
    }
    fout->Close();
    
}
