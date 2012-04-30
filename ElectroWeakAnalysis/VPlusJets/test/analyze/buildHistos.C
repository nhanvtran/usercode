#define buildHistos_cxx
#include "buildHistos.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <iostream>

void buildHistos::Loop(std::string inputname, double sampleSclFactor)
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
        
    // ==========================
    char fname[192];
    sprintf(fname,"%s",inputname.c_str());
    TFile* tmpF = new TFile( fname );
    TTree* tree = (TTree*) tmpF->Get("otree");
    //tree->Add(fname);
    ReadTree( tree );
    // ==========================
    
    std::cout << "inputname: " << inputname << ", entries: " << tree->GetEntries() << std::endl;
    
    
    
    double sclF_fromMC = sampleSclFactor;
    
    int i_ak5 = findIndexForJetType( "ak5" );
    int i_ak7 = findIndexForJetType( "ak7" );        
    int i_ak8 = findIndexForJetType( "ak8" );
    
    if (tree == 0) return;
    
    int nentries = tree->GetEntries();
    
    double totalSampleWeight = 0.;
    Long64_t nbytes = 0, nb = 0;
    for (int jentry=0; jentry<nentries;jentry++) {
        
        //std::cout << "are we even in here?" << std::endl;
        
        //Long64_t ientry = LoadTree(jentry);
        //if (ientry < 0) break;
        
        nb = tree->GetEntry(jentry);   nbytes += nb;
        
        if (jentry % 100000 == 0) std::cout << "jentry: " << jentry << std::endl;
        
        // code for combining scale factors
        // get PU SF
        // get trigger SF
        // get lepton SF
        double totSF = sclF_fromMC;
        //std::cout << "totSF: " << totSF << std::endl;
        totalSampleWeight+=totSF;
        
        ////////////////////////////////////////////////////////////
        // put in some further cuts
        if (w_mt < 50) continue;
        if (e_met < 35) continue;
        if (l_pt < 35) continue;
        double jetThresh = 200;
        ////////////////////////////////////////////////////////////
        
        //std::cout << "l_pt: " << l_pt << std::endl;

        h_w_mt->Fill( w_mt, totSF );
        h_w_pt->Fill( w_pt, totSF );
        h_e_met->Fill( e_met, totSF );
        h_l_pt->Fill( l_pt, totSF );
        
        
        // -----------------------------------------
        // filling jet histograms
        for (int i = 0; i < nJetTypes; i++){            
            
            if (j_pt[i] >= jetThresh){
            //if ((j_pt[i] >= jetThresh)&&(j_ak5_nBtags == 2)&&( (j_ca8pr_m1/j_mass[i]) < 0.3)){
                
                bool matchedGenJet = false;
                if (jetTypes[i].find("ak5") && j_ak5_match > 0) matchedGenJet = true;
                if (jetTypes[i].find("ak7") && j_ak7_match > 0) matchedGenJet = true;
                if (jetTypes[i].find("ak8") && j_ak8_match > 0) matchedGenJet = true;
                if (jetTypes[i].find("ca8") && j_ca8_match > 0) matchedGenJet = true;
                if (_isData) matchedGenJet = true;
                
                if (matchedGenJet){
                    
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

                    if ( jetTypes[i] == "ca8pr" ){
                        h_j_ca8pr_mu->Fill( j_ca8pr_m1/j_mass[i], totSF );
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
                    p_j_massOverAK5vNV[i]->Fill( e_nvert, j_mass[i]/j_mass[i_ak5], totSF );
                    p_j_massOverAK7vNV[i]->Fill( e_nvert, j_mass[i]/j_mass[i_ak7], totSF );
                    p_j_massOverAK8vNV[i]->Fill( e_nvert, j_mass[i]/j_mass[i_ak8], totSF );
                    p_j_ptOverAK5vNV[i]->Fill( e_nvert, j_pt[i]/j_pt[i_ak5], totSF );
                    p_j_ptOverAK7vNV[i]->Fill( e_nvert, j_pt[i]/j_pt[i_ak7], totSF );
                    p_j_ptOverAK8vNV[i]->Fill( e_nvert, j_pt[i]/j_pt[i_ak8], totSF );
                    
                    // gen jets
                    h_j_massOverAK5g[i]->Fill( j_mass[i]/j_mass[i_ak5], totSF );
                    h_j_massOverAK7g[i]->Fill( j_mass[i]/j_mass[i_ak7], totSF );
                    h_j_massOverAK8g[i]->Fill( j_mass[i]/j_mass[i_ak8], totSF );
                    h_j_ptOverAK5g[i]->Fill( j_pt[i]/j_pt[i_ak5], totSF );
                    h_j_ptOverAK7g[i]->Fill( j_pt[i]/j_pt[i_ak7], totSF );
                    h_j_ptOverAK8g[i]->Fill( j_pt[i]/j_pt[i_ak8], totSF );
                    
                    p_j_massOverAK5g[i]->Fill( j_pt[i], j_mass[i]/j_mass[i_ak5], totSF );
                    p_j_massOverAK7g[i]->Fill( j_pt[i], j_mass[i]/j_mass[i_ak7], totSF );
                    p_j_massOverAK8g[i]->Fill( j_pt[i], j_mass[i]/j_mass[i_ak8], totSF );
                    p_j_ptOverAK5g[i]->Fill( j_pt[i], j_pt[i]/j_pt[i_ak5], totSF );
                    p_j_ptOverAK7g[i]->Fill( j_pt[i], j_pt[i]/j_pt[i_ak7], totSF );
                    p_j_ptOverAK8g[i]->Fill( j_pt[i], j_pt[i]/j_pt[i_ak8], totSF );
                    
                }
            }
            
        }
        // -----------------------------------------
    }
    
    std::cout << "totalSampleWeight: " << totalSampleWeight << std::endl;
    
}

void buildHistos::WriteOut(){
    
    //TFile* fout = new TFile("out.root","RECREATE");
    fout->cd();
    h_w_mt->Write();
    h_w_pt->Write();
    h_e_met->Write();
    h_l_pt->Write();
    std::cout << "nJetTypes: " << nJetTypes << std::endl;
    
    h_j_ca8pr_mu->Write();
    
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
        
        p_j_massOverAK5vNV[i]->Write();
        p_j_massOverAK7vNV[i]->Write();
        p_j_massOverAK8vNV[i]->Write();
        p_j_ptOverAK5vNV[i]->Write();
        p_j_ptOverAK7vNV[i]->Write();
        p_j_ptOverAK8vNV[i]->Write();
        
        if (!_isData){
            h_j_massOverAK5g[i]->Write();
            h_j_massOverAK7g[i]->Write();
            h_j_massOverAK8g[i]->Write();
            h_j_ptOverAK5g[i]->Write();
            h_j_ptOverAK7g[i]->Write();
            h_j_ptOverAK8g[i]->Write();
            
            p_j_massOverAK5g[i]->Write();
            p_j_massOverAK7g[i]->Write();
            p_j_massOverAK8g[i]->Write();
            p_j_ptOverAK5g[i]->Write();
            p_j_ptOverAK7g[i]->Write();
            p_j_ptOverAK8g[i]->Write();
        }
    }
    fout->Close();
    
    std::cout << "finished loop..." << std::endl;
    
    //delete tmpF;
    //delete tree;
}

void buildHistos::ReadTree( TTree *tree ){
    
    /*
    // Set branch addresses and branch pointers
    if (!tree) return;
    fChain = tree;
    fCurrent = -1;
    fChain->SetMakeClass(1);
    */
    
    tree->SetBranchAddress("e_puwt", &e_puwt);
    tree->SetBranchAddress("e_puwt_up", &e_puwt_up);
    tree->SetBranchAddress("e_puwt_dn", &e_puwt_dn);
    tree->SetBranchAddress("e_effwt", &e_effwt);
    tree->SetBranchAddress("e_met", &e_met);
    tree->SetBranchAddress("e_nvert", &e_nvert);
    tree->SetBranchAddress("e_weight", &e_weight);
    tree->SetBranchAddress("w_mt", &w_mt);
    tree->SetBranchAddress("w_pt", &w_pt);
    tree->SetBranchAddress("l_pt", &l_pt);
    tree->SetBranchAddress("l_reliso", &l_reliso);
    
    tree->SetBranchAddress("j_ak5_match", &j_ak5_match);
    tree->SetBranchAddress("j_ak7_match", &j_ak7_match);
    tree->SetBranchAddress("j_ak8_match", &j_ak8_match);
    tree->SetBranchAddress("j_ca8_match", &j_ca8_match);

    tree->SetBranchAddress("j_ak5_nBtags", &j_ak5_nBtags);
    tree->SetBranchAddress("j_ca8pr_m1", &j_ca8pr_m1);
    tree->SetBranchAddress("j_ca8pr_m2", &j_ca8pr_m2);
    
    for (int i = 0; i < nJetTypes; i++){
        
        std::cout << "string: " << ("j_" + jetTypes[i] + "_nJ") << std::endl;
        j_nJ[i] = 0.;
        j_mass[i] = 0.;
        j_bdis[i] = 0.;
        j_eta[i] = 0.;
        j_phi[i] = 0.;
        j_pt[i] = 0.;
        j_p[i] = 0.;
        
        tree->SetBranchAddress( ("j_" + jetTypes[i] + "_nJ").c_str(), &j_nJ[i]);// , &b_j_ak5_nJ);
        tree->SetBranchAddress( ("j_" + jetTypes[i] + "_mass").c_str(), &j_mass[i]);// , &b_j_ak5_nJ);
        tree->SetBranchAddress( ("j_" + jetTypes[i] + "_area").c_str(), &j_area[i]);
        tree->SetBranchAddress( ("j_" + jetTypes[i] + "_pt").c_str(), &j_pt[i]);// , &b_j_ak5_nJ);
        
        if ( jetTypes[i] == "ak5" ){
            tree->SetBranchAddress( ("j_" + jetTypes[i] + "_bdis").c_str(), &j_bdis[i]);// , &b_j_ak5_nJ);
            tree->SetBranchAddress( ("j_" + jetTypes[i] + "_eta").c_str(), &j_eta[i]);// , &b_j_ak5_nJ);
            tree->SetBranchAddress( ("j_" + jetTypes[i] + "_phi").c_str(), &j_phi[i]);// , &b_j_ak5_nJ);
            tree->SetBranchAddress( ("j_" + jetTypes[i] + "_p").c_str(), &j_p[i]);// , &b_j_ak5_nJ);        
        }
        
    }
    
}
