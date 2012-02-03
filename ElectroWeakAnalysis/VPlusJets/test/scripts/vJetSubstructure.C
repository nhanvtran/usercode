#define vJetSubstructure_cxx
#include "vJetSubstructure.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

#include <iostream>
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TLorentzVector.h>
#include <algorithm>
#include <vector>

using namespace std;

void vJetSubstructure::Loop()
{
    //   In a ROOT session, you can do:
    //      Root > .L vJetSubstructure.C
    //      Root > vJetSubstructure t
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
    if (fChain == 0) return;
    
    Long64_t nentries = fChain->GetEntriesFast();
    
    Long64_t nbytes = 0, nb = 0;
    
    //TH1F* h_jmass_ak5
    /*
	 for (int i = 0; i < nentries; i++){
     fChain->GetEntry(i);
     std::cout << "i " << i << ", event_evtNo: " << event_evtNo;
     std::cout << ", JetgoodPatJetsCA8PF_Mass[0]: " << JetgoodPatJetsCA8PF_Mass[0] << ", " << JetgoodPatJetsCA8PF_Pt[0] << ", nJets: " << numgoodPatJetsCA8PFJets << std::endl;
     
	 }
     //*/
    ///*
    
    TH1F* h_mass_ak5 = new TH1F("h_mass_ak5","h_mass_ak5",150,0,150);
    TH1F* h_mass_ca8 = new TH1F("h_mass_ca8","h_mass_ca8",150,0,150);
    TH1F* h_mass_ca8Pr = new TH1F("h_mass_ca8Pr","h_mass_ca8Pr",150,0,150);
    TH1F* h_mass_ca8Pr_Sel = new TH1F("h_mass_ca8Pr_Sel","h_mass_ca8Pr_Sel",150,0,150);
    
    TH1F* h_massZ_ak5 = new TH1F("h_massZ_ak5","h_massZ_ak5",50,50,100);
    TH1F* h_massZ_ca8 = new TH1F("h_massZ_ca8","h_massZ_ca8",50,50,100);
    TH1F* h_massZ_ca8Pr = new TH1F("h_massZ_ca8Pr","h_massZ_ca8Pr",50,50,100);
    
    TH1F* h_relIso_PF = new TH1F("h_relIso_PF","h_relIso_PF",50,0,1);
    TH1F* h_massdrop = new TH1F("h_massdrop","h_massdrop",100,0,1);
    
    // signal histograms
    TH1F* hsig_lepPt = new TH1F("hsig_lepPt",";lep Pt;",100,0,500);
    TH1F* hsig_ca8Pr_Pt = new TH1F("hsig_ca8Pr_Pt",";ca8Pr;",100,0,500);
    TH1F* hsig_ca8Pr_ak5_dR = new TH1F("hsig_ca8Pr_ak5_dR",";matched dR;",100,0,1);
    TH1F* hsig_ak5matched_Pt = new TH1F("hsig_ak5matched_Pt",";matched ak5 Pt;",100,0,500);
    TH1F* hsig_ak5matched_PtRatio = new TH1F("hsig_ak5matched_PtRatio",";ak5/ca8Pr Pt;",100,0,2);
    TH1F* hsig_pfmet = new TH1F("hsig_pfmet",";met;",100,0,500);
    
    int ctr_signalEvents = 0;
    int ctr_signalEvents_wMatch = 0;
    
    std::cout << "nentries: " << nentries << std::endl;
    //nentries = 15155362/4;
    for (Long64_t jentry=0; jentry<nentries;jentry++) {
        //for (Long64_t jentry=0; jentry<10000;jentry++) {
        Long64_t ientry = LoadTree(jentry);
        if (ientry < 0) break;
        nb = fChain->GetEntry(jentry);   nbytes += nb;
        // if (Cut(ientry) < 0) continue;
        
        if (ientry % 100000 == 0) std::cout << " === ientry: " << ientry << std::endl;
        
        // -----
        // electron isolation
        float relIso = (W_electron_pfiso_chargedHadronIso + W_electron_pfiso_photonIso + W_electron_pfiso_neutralHadronIso)/W_electron_et;
        h_relIso_PF->Fill(relIso);
        
        // -----
        double jmass_ak5 = -1.;
        double jpT_ak5 = -1.;
        for (int i = 0; i < numgoodPatJetsPFlowJets; i++){
            if (jpT_ak5 < JetgoodPatJetsPFlow_Pt[i]){ 
                jmass_ak5 = JetgoodPatJetsPFlow_Mass[i];
                jpT_ak5 = JetgoodPatJetsPFlow_Pt[i];
            }
        }
        h_mass_ak5->Fill(jmass_ak5);
        h_massZ_ak5->Fill(jmass_ak5);
        
        // -----
        double jmass_ca8 = -1.;
        double jpT_ca8 = -1.;
        for (int i = 0; i < numgoodPatJetsCA8PFJets; i++){
            if (jpT_ca8 < JetgoodPatJetsCA8PF_Pt[i]){ 
                jmass_ca8 = JetgoodPatJetsCA8PF_Mass[i];
                jpT_ca8 = JetgoodPatJetsCA8PF_Pt[i];
            }
        }
        h_mass_ca8->Fill(jmass_ca8);
        h_massZ_ca8->Fill(jmass_ca8);
        
        // -----
        double jmass_ca8Pr = -1.;
        double jpT_ca8Pr = -1.;
        int index_ca8Pr = -1;
        int nDau_ca8Pr = -1;
        double subjetMass1 = -1.;
        double subjetMass2 = -1.;
        for (int i = 0; i < numgoodPatJetsCA8PrunedPFJets; i++){
            if (jpT_ca8Pr < JetgoodPatJetsCA8PrunedPF_Pt[i]){ 
                nDau_ca8Pr = JetgoodPatJetsCA8PrunedPF_nJetDaughters[i];
                jmass_ca8Pr = JetgoodPatJetsCA8PrunedPF_Mass[i];
                jpT_ca8Pr = JetgoodPatJetsCA8PrunedPF_Pt[i];
                subjetMass1 = JetgoodPatJetsCA8PrunedPF_subJet1Mass[i];
                subjetMass2 = JetgoodPatJetsCA8PrunedPF_subJet2Mass[i];
                index_ca8Pr = i;
            }
        }
        //std::cout << "nDau_ca8Pr: " << nDau_ca8Pr << ", m1: " << subjetMass1 << ", m2: " << subjetMass2 << std::endl;
        
        h_mass_ca8Pr->Fill(jmass_ca8Pr);
        h_massZ_ca8Pr->Fill(jmass_ca8Pr);
        double massDropVar = max(subjetMass1,subjetMass2)/jmass_ca8Pr;
        //h_massdrop->Fill(massDropVar);
        
        ////////////////////////////////////////////
        /// If you find a signal event
        ////////////////////////////////////////////
        
        //if (true && (relIso < 0.2) && (fabs(W_electron_eta) < 2.5) && (W_electron_pt > 30) && (jpT_ak5 > 125) && (massDropVar < 0.35)){
        if (true && (relIso < 0.2) && (fabs(W_electron_eta) < 2.5) && (jpT_ak5 > 125) && (jpT_ca8 > 150) && (W_electron_pt > 30)){
            h_massdrop->Fill(massDropVar);            
            
            if (massDropVar < 0.35){
                 
                h_mass_ca8Pr_Sel->Fill(jmass_ca8Pr);
                if ((jmass_ca8Pr < 100)&&(jmass_ca8Pr > 60)){    
                    //if (massDropVar < 0.35){
                    
                    // electron requirement
                    //std::cout << "Found signal event with jet mass = " << jmass_ca8Pr << " and rel iso: " << eleRelIso << std::endl;
                    
                    //std::cout << W_electron_isWP70 << ", " << fabs(W_electron_eta) << ", " << eleRelIso << std::endl;
                    ctr_signalEvents++;
                    
                    // get lepton information
                    hsig_lepPt->Fill(W_electron_pt);
                    
                    // get ca8Pr jet information
                    hsig_ca8Pr_Pt->Fill(JetgoodPatJetsCA8PrunedPF_Pt[index_ca8Pr]);
                    
                    // get matching with ak5 information
                    TLorentzVector* p4_signalJet = new TLorentzVector(JetgoodPatJetsCA8PrunedPF_Px[index_ca8Pr],
                                                                      JetgoodPatJetsCA8PrunedPF_Py[index_ca8Pr],
                                                                      JetgoodPatJetsCA8PrunedPF_Pz[index_ca8Pr],
                                                                      JetgoodPatJetsCA8PrunedPF_E[index_ca8Pr]);
                    
                    float dR_minimum = 10.;
                    int index_ak5matched = -1;
                    for (int i = 0; i < numgoodPatJetsPFlowJets; i++){
                        
                        TLorentzVector* p4_curAK5Jet = new TLorentzVector(JetgoodPatJetsPFlow_Px[i],
                                                                          JetgoodPatJetsPFlow_Py[i],
                                                                          JetgoodPatJetsPFlow_Pz[i],
                                                                          JetgoodPatJetsPFlow_E[i]);
                        float dR = p4_signalJet->DeltaR(*p4_curAK5Jet);
                        if (dR < dR_minimum) { float tmp = dR; dR_minimum = tmp; index_ak5matched = i; }
                    }
                    hsig_ca8Pr_ak5_dR->Fill(dR_minimum);
                    if (dR_minimum < 0.4){
                        ctr_signalEvents_wMatch++;
                        // found matching ak5 Jet!
                        hsig_ak5matched_Pt->Fill(JetgoodPatJetsPFlow_Pt[index_ak5matched]);
                        hsig_ak5matched_PtRatio->Fill(JetgoodPatJetsPFlow_Pt[index_ak5matched]/JetgoodPatJetsCA8PrunedPF_Pt[index_ca8Pr]);
                    }
                    
                    // get MET information
                    hsig_pfmet->Fill(event_met_pfmet);
                }
            }
        }
        ////////////////////////////////////////////        
    }
    
    std::cout << "number of signal events: " << ctr_signalEvents << ", number of matched events: " << ctr_signalEvents_wMatch << std::endl;
    std::cout << "Efficiency: " << ((double) ctr_signalEvents_wMatch/ctr_signalEvents) << std::endl;
    
    //*/
    h_mass_ca8->SetLineColor( kRed );
    h_mass_ca8Pr->SetLineColor( kBlue );
    h_massZ_ca8->SetLineColor( kRed );
    h_massZ_ca8Pr->SetLineColor( kBlue );
    
    double nloXS = 43000; // fb
    double lumi = 1; // fb-1
    double nEventsInSample = 2061760;
    double sclFactor = nloXS*lumi/nEventsInSample;
    sclFactor = 1.; // for Higgs
    
    h_mass_ak5->Scale( sclFactor );
    h_massZ_ak5->Scale( sclFactor );
    h_mass_ca8->Scale( sclFactor );
    h_mass_ca8Pr->Scale( sclFactor );
    h_massZ_ca8->Scale( sclFactor );
    h_massZ_ca8Pr->Scale( sclFactor );
    
    TCanvas* cIso = new TCanvas("cIso","cIso",800,600);
    h_relIso_PF->GetYaxis()->SetTitle("a.u."); h_relIso_PF->GetXaxis()->SetTitle("Relative PF Isolation");
    h_relIso_PF->Draw();
    cIso->SaveAs("figs/testIso.eps");
    TCanvas* cMassDrop = new TCanvas("cMassDrop","cMassDrop",800,600);
    h_massdrop->GetYaxis()->SetTitle("a.u."); h_massdrop->GetXaxis()->SetTitle("mass drop, #mu");
    h_massdrop->Draw();
    cMassDrop->SaveAs("figs/testMassDrop.eps");
    
    TCanvas* c1 = new TCanvas("c1","c1",800,600);
    //h_mass_ak5->GetYaxis()->SetTitle("events/1 GeV/fb^{-1}"); h_mass_ak5->GetXaxis()->SetTitle("Jet Mass (GeV)");
    h_mass_ak5->GetYaxis()->SetTitle("a.u."); h_mass_ak5->GetXaxis()->SetTitle("Jet Mass (GeV)");
    h_mass_ak5->Draw();
    h_mass_ca8->Draw("sames");
    h_mass_ca8Pr->Draw("sames");
    c1->SaveAs("figs/test.eps");
    TCanvas* c1log = new TCanvas("c1log","c1log",800,600);
    gPad->SetLogy();
    //h_mass_ak5->GetYaxis()->SetTitle("events/1 GeV/fb^{-1}"); h_mass_ak5->GetXaxis()->SetTitle("Jet Mass (GeV)");
    h_mass_ak5->GetYaxis()->SetTitle("a.u."); h_mass_ak5->GetXaxis()->SetTitle("Jet Mass (GeV)");
    h_mass_ak5->Draw();
    h_mass_ca8->Draw("sames");
    h_mass_ca8Pr->Draw("sames");
    c1log->SaveAs("figs/test_log.eps");
    TCanvas* c1zoom = new TCanvas("c1zoom","c1zoom",800,600);
    //h_massZ_ca8->GetYaxis()->SetTitle("events/1 GeV/fb^{-1}"); h_massZ_ca8->GetXaxis()->SetTitle("Jet Mass (GeV)");
    h_massZ_ca8->GetYaxis()->SetTitle("a.u."); h_massZ_ca8->GetXaxis()->SetTitle("Jet Mass (GeV)");
    h_massZ_ca8->SetMinimum(0);
    h_massZ_ca8Pr->Draw();
    h_massZ_ak5->Draw("sames");
    h_massZ_ca8->Draw("sames");
    c1zoom->SaveAs("figs/test_zoom.eps");
    
    TFile* fout = new TFile("fout.root","RECREATE");
    fout->cd();
    h_mass_ca8Pr->Write();
    h_mass_ca8Pr_Sel->Write();
    fout->Close();
    
    ////////////////////////////////////////////
    /// If you find a signal event
    ////////////////////////////////////////////
    TCanvas* c2 = new TCanvas("c2","c2",1200,800);
    c2->Divide(3,2);
    c2->cd(1);
    hsig_lepPt->Draw();
    c2->cd(2);
    hsig_ca8Pr_Pt->Draw();
    c2->cd(3);
    hsig_ca8Pr_ak5_dR->Draw();
    c2->cd(4);
    hsig_ak5matched_Pt->Draw();
    c2->cd(5);
    hsig_ak5matched_PtRatio->Draw();
    c2->cd(6);
    hsig_pfmet->Draw();
    c2->SaveAs("figs/signalPlot.eps");
    
}
