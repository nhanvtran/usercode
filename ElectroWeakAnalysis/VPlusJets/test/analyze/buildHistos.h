//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Fri Apr  6 11:23:31 2012 by ROOT version 5.27/06b
// from TTree otree/otree
// found on file: ntuples/test_ww.root
//////////////////////////////////////////////////////////

#ifndef buildHistos_h
#define buildHistos_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include "TH1F.h"
#include "TProfile.h"
#include <iostream>

class buildHistos {
    public :
    
    bool _isData;
    
    std::vector < std::string > jetTypes;
    int nJetTypes;
    TFile* fout;
    TTree* otree;
    
    TH1D *h_w_mt;
    TH1D *h_w_pt;
    TH1D *h_e_met;
    TH1D *h_l_pt;
    
    TH1D *h_j_nJ[25];    
    TH1D *h_j_bdis[25];
    TH1D *h_j_eta[25];
    TH1D *h_j_phi[25];
    TH1D *h_j_pt[25];
    TH1D *h_j_p[25];
    TH1D *h_j_mass[25];
    TH1D *h_j_area[25];

    TH1D *h_j_ca8pr_mu;
    
    TH1D *h_j_mass_pt50to100[25];    
    TH1D *h_j_mass_pt100to150[25];
    TH1D *h_j_mass_pt150to200[25];
    TH1D *h_j_mass_pt200to300[25];
    TH1D *h_j_mass_pt300andup[25];
    
    ///*
    TProfile *p_j_massvpt[25];
    TProfile *p_j_massvNV[25];
    TProfile *p_j_massOverAK5[25];
    TProfile *p_j_massOverAK7[25];
    TProfile *p_j_massOverAK8[25];
    TProfile *p_j_ptOverAK5[25];
    TProfile *p_j_ptOverAK7[25];
    TProfile *p_j_ptOverAK8[25];
    TProfile *p_j_massOverAK5vNV[25];
    TProfile *p_j_massOverAK7vNV[25];
    TProfile *p_j_massOverAK8vNV[25];
    TProfile *p_j_ptOverAK5vNV[25];
    TProfile *p_j_ptOverAK7vNV[25];
    TProfile *p_j_ptOverAK8vNV[25];
    //*/
    
    // gen jet histograms
    TH1D *h_j_massOverAK5g[25];    
    TH1D *h_j_massOverAK7g[25];    
    TH1D *h_j_massOverAK8g[25];    
    TH1D *h_j_massOverCA8g[25];    
    TH1D *h_j_ptOverAK5g[25];    
    TH1D *h_j_ptOverAK7g[25];    
    TH1D *h_j_ptOverAK8g[25];    
    TH1D *h_j_ptOverCA8g[25];    

    TProfile *p_j_massOverAK5g[25];    
    TProfile *p_j_massOverAK7g[25];    
    TProfile *p_j_massOverAK8g[25];    
    TProfile *p_j_massOverCA8g[25];    
    TProfile *p_j_ptOverAK5g[25];    
    TProfile *p_j_ptOverAK7g[25];    
    TProfile *p_j_ptOverAK8g[25];    
    TProfile *p_j_ptOverCA8g[25];    

    
    
    TTree          *fChain;   //!pointer to the analyzed TTree or TChain
    Int_t           fCurrent; //!current Tree number in a TChain
    
    // Declaration of leaf types
    Double_t        e_puwt;
    Double_t        e_puwt_up;
    Double_t        e_puwt_dn;
    Double_t        e_effwt;
    Double_t        e_met;
    Double_t        e_nvert;
    Double_t        e_weight;
    Double_t        w_mt;
    Double_t        w_pt;
    Double_t        l_pt;
    Double_t        l_reliso;
    
    Int_t j_ak5_match;
    Int_t j_ak7_match;
    Int_t j_ak8_match;
    Int_t j_ca8_match;
    
    Double_t j_ak5_nBtags;
    Double_t j_ca8pr_m1;
    Double_t j_ca8pr_m2;
    
    Double_t j_nJ[25];
    Double_t j_bdis[25]; 
    Double_t j_eta[25]; 
    Double_t j_phi[25]; 
    Double_t j_pt[25]; 
    Double_t j_p[25]; 
    Double_t j_mass[25]; 
    Double_t j_area[25];     

    buildHistos( std::string oname, bool isData);
    virtual ~buildHistos();
    virtual int    findIndexForJetType( std::string name );
    virtual Int_t    Cut(Long64_t entry);
    virtual Int_t    GetEntry(Long64_t entry);
    virtual Long64_t LoadTree(Long64_t entry);
    virtual void     Init( );
    virtual void     Loop(std::string inputname, double sampleSclFactor);
    virtual Bool_t   Notify();
    virtual void     Show(Long64_t entry = -1);
    virtual void     ReadTree( TTree* tree );
    virtual void     WriteOut();
    
};

#endif

#ifdef buildHistos_cxx
buildHistos::buildHistos( std::string oname, bool isData)
{
    
    _isData = isData;
    
    /*
    // if parameter tree is not specified (or zero), connect the file
    // used to generate this class and read the Tree.
    if (tree == 0) {
        TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("ntuples/test_ww.root");
        if (!f) {
            f = new TFile("ntuples/test_ww.root");
        }
        tree = (TTree*)gDirectory->Get("otree");
        
    }
    Init(tree);
     */
    
    fout = new TFile(oname.c_str(),"RECREATE");
    
    Init( );
}

buildHistos::~buildHistos()
{
    if (!fChain) return;
    delete fChain->GetCurrentFile();
}

int buildHistos::findIndexForJetType(std::string name){
    
    int indextosave = -1;
    for (int i = 0; i < nJetTypes; i++){
        if (name == jetTypes[i]) indextosave = i;
    }
    
    if (indextosave < 0) std::cout << "WARNING, invalid jet type!" << std::endl;
    return indextosave;
}


Int_t buildHistos::GetEntry(Long64_t entry)
{
    // Read contents of entry.
    if (!fChain) return 0;
    return fChain->GetEntry(entry);
}
Long64_t buildHistos::LoadTree(Long64_t entry)
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

void buildHistos::Init( )
{
    
    const int nJetTypes_C = 18;
    std::string jetNames[nJetTypes_C] = {"ak5","ak5tr","ak5pr","ak5ft","ak7","ak7tr","ak7pr","ak7ft","ak8","ak8tr","ak8pr","ak8ft","ca8","ca8pr","ak5g","ak7g","ak8g","ca8g"};
    for (int i = 0; i < nJetTypes_C; i++){
        jetTypes.push_back( jetNames[i] );
    }
    nJetTypes = jetTypes.size();
    
    // --------------------------------------------
    // don't run over gen jet collections if data!!
    if (_isData) nJetTypes -= 4;
    // --------------------------------------------
    
    //std::cout << "nJetTypes: " << nJetTypes << std::endl;
    
    h_w_mt = new TH1D("h_w_mt", "h_w_mt", 100, 0., 200);
    h_w_pt = new TH1D("h_w_pt", "h_w_pt", 100, 0., 500);
    h_e_met = new TH1D("h_e_met", "h_e_met", 100, 0., 300);
    h_l_pt = new TH1D("h_l_pt", "h_l_pt", 100, 0., 300);

    h_j_ca8pr_mu = new TH1D("h_j_ca8pr_mu", "h_j_ca8pr_mu", 100, 0., 1.);

    
    int nBins = 20;
    
    // DECLARATION OF HISTOGRAMS
    double xbinsProfile[29] = {50,55,60,65,70,75,80,85,90,95,100,110,120,130,140,150,160,170,180,190,200,225,250,275,300,350,400,450,500};
    for (int i = 0; i < nJetTypes; i++){
        h_j_nJ[i] = new TH1D( ("h_j_" + jetTypes[i] + "_nJ").c_str(), ("; n Jets (" + jetTypes[i] + ");count").c_str(), 10,0., 10. ); 
        h_j_mass[i] = new TH1D( ("h_j_" + jetTypes[i] + "_mass").c_str(), ("; jet mass (" + jetTypes[i] + ");count").c_str(), nBins,0.,200. );
        h_j_area[i] = new TH1D( ("h_j_" + jetTypes[i] + "_area").c_str(), ("; jet area (" + jetTypes[i] + ");count").c_str(), nBins,0.,4. );
        h_j_bdis[i] = new TH1D( ("h_j_" + jetTypes[i] + "_bdis").c_str(), ("; ejt b disc (" + jetTypes[i] + ");count").c_str(), nBins,0.,10. );
        h_j_eta[i] = new TH1D( ("h_j_" + jetTypes[i] + "_eta").c_str(), ("; jet eta (" + jetTypes[i] + ");count").c_str(), nBins,-5.,5. );
        h_j_phi[i] = new TH1D( ("h_j_" + jetTypes[i] + "_phi").c_str(), ("; jet phi (" + jetTypes[i] + ");count").c_str(), nBins,-10.,10. );
        h_j_pt[i] = new TH1D( ("h_j_" + jetTypes[i] + "_pt").c_str(), ("; jet pT (" + jetTypes[i] + ");count").c_str(), nBins,0.,500 );
        h_j_p[i] = new TH1D( ("h_j_" + jetTypes[i] + "_p").c_str(), ("; jet pT (" + jetTypes[i] + ");count").c_str(), nBins,0.,500 );
        
        // in bins of pT
        h_j_mass_pt50to100[i] = new TH1D( ("h_j_" + jetTypes[i] + "_mass_pt50to100").c_str(), ("; jet mass (" + jetTypes[i] + ");count").c_str(), nBins,0., 200. ); 
        h_j_mass_pt100to150[i] = new TH1D( ("h_j_" + jetTypes[i] + "_mass_pt100to150").c_str(), ("; jet mass (" + jetTypes[i] + ");count").c_str(), nBins,0., 200. ); 
        h_j_mass_pt150to200[i] = new TH1D( ("h_j_" + jetTypes[i] + "_mass_pt150to200").c_str(), ("; jet mass (" + jetTypes[i] + ");count").c_str(), nBins,0., 200. ); 
        h_j_mass_pt200to300[i] = new TH1D( ("h_j_" + jetTypes[i] + "_mass_pt200to300").c_str(), ("; jet mass (" + jetTypes[i] + ");count").c_str(), nBins,0., 200. ); 
        h_j_mass_pt300andup[i] = new TH1D( ("h_j_" + jetTypes[i] + "_mass_pt300andup").c_str(), ("; jet mass (" + jetTypes[i] + ");count").c_str(), nBins,0., 200. ); 
        
        // profile
        p_j_massvpt[i] = new TProfile(("p_j_" + jetTypes[i] + "_massvpt").c_str(),("; jet pT; jet mass (" + jetTypes[i] + ")").c_str(),28,xbinsProfile, 0., 1000.);   
        p_j_massvNV[i] = new TProfile(("p_j_" + jetTypes[i] + "_massvNV").c_str(),("; n vertices; jet mass (" + jetTypes[i] + ")").c_str(),30,0, 30., 0, 1000.);   
        
        // profile, ratio plots
        p_j_massOverAK5[i] = new TProfile(("p_j_" + jetTypes[i] + "_massOverAK5").c_str(),("; jet pT; jet mass ratio (" + jetTypes[i] + "/ak5)").c_str(),28,xbinsProfile, 0., 5.);   
        p_j_massOverAK7[i] = new TProfile(("p_j_" + jetTypes[i] + "_massOverAK7").c_str(),("; jet pT; jet mass ratio (" + jetTypes[i] + "/ak7)").c_str(),28,xbinsProfile, 0., 5.);   
        p_j_massOverAK8[i] = new TProfile(("p_j_" + jetTypes[i] + "_massOverAK8").c_str(),("; jet pT; jet mass ratio (" + jetTypes[i] + "/ak8)").c_str(),28,xbinsProfile, 0., 5.);   
        p_j_ptOverAK5[i] = new TProfile(("p_j_" + jetTypes[i] + "_ptOverAK5").c_str(),("; jet pT; jet pT ratio (" + jetTypes[i] + "/ak5)").c_str(),28,xbinsProfile, 0., 5.);   
        p_j_ptOverAK7[i] = new TProfile(("p_j_" + jetTypes[i] + "_ptOverAK7").c_str(),("; jet pT; jet pT ratio (" + jetTypes[i] + "/ak7)").c_str(),28,xbinsProfile, 0., 5.);   
        p_j_ptOverAK8[i] = new TProfile(("p_j_" + jetTypes[i] + "_ptOverAK8").c_str(),("; jet pT; jet pT ratio (" + jetTypes[i] + "/ak8)").c_str(),28,xbinsProfile, 0., 5.);   

        p_j_massOverAK5vNV[i] = new TProfile(("p_j_" + jetTypes[i] + "_massOverAK5vNV").c_str(),("; n vertices; jet mass ratio (" + jetTypes[i] + "/ak5)").c_str(),30,0, 30., 0, 1000.);   
        p_j_massOverAK7vNV[i] = new TProfile(("p_j_" + jetTypes[i] + "_massOverAK7vNV").c_str(),("; n vertices; jet mass ratio (" + jetTypes[i] + "/ak7)").c_str(),30,0, 30., 0, 1000.);   
        p_j_massOverAK8vNV[i] = new TProfile(("p_j_" + jetTypes[i] + "_massOverAK8vNV").c_str(),("; n vertices; jet mass ratio (" + jetTypes[i] + "/ak8)").c_str(),30,0, 30., 0, 1000.);   
        p_j_ptOverAK5vNV[i] = new TProfile(("p_j_" + jetTypes[i] + "_ptOverAK5vNV").c_str(),("; n vertices; jet pT ratio (" + jetTypes[i] + "/ak5)").c_str(),30,0, 30., 0, 1000.);   
        p_j_ptOverAK7vNV[i] = new TProfile(("p_j_" + jetTypes[i] + "_ptOverAK7vNV").c_str(),("; n vertices; jet pT ratio (" + jetTypes[i] + "/ak7)").c_str(),30,0, 30., 0, 1000.);   
        p_j_ptOverAK8vNV[i] = new TProfile(("p_j_" + jetTypes[i] + "_ptOverAK8vNV").c_str(),("; n vertices; jet pT ratio (" + jetTypes[i] + "/ak8)").c_str(),30,0, 30., 0, 1000.);   

        
        // gen jets
        h_j_massOverAK5g[i] = new TProfile(("h_j_" + jetTypes[i] + "_massOverAK5g").c_str(),("; jet mass ratio (" + jetTypes[i] + "/ak5g);").c_str(),nBins, 0., 2.);   
        h_j_massOverAK7g[i] = new TProfile(("h_j_" + jetTypes[i] + "_massOverAK7g").c_str(),("; jet mass ratio (" + jetTypes[i] + "/ak7g);").c_str(),nBins, 0., 2.);   
        h_j_massOverAK8g[i] = new TProfile(("h_j_" + jetTypes[i] + "_massOverAK8g").c_str(),("; jet mass ratio (" + jetTypes[i] + "/ak8g);").c_str(),nBins, 0., 2.);   
        h_j_ptOverAK5g[i] = new TProfile(("h_j_" + jetTypes[i] + "_ptOverAK5g").c_str(),("; jet pT ratio (" + jetTypes[i] + "/ak5g);").c_str(),nBins, 0., 2.);   
        h_j_ptOverAK7g[i] = new TProfile(("h_j_" + jetTypes[i] + "_ptOverAK7g").c_str(),("; jet pT ratio (" + jetTypes[i] + "/ak7g);").c_str(),nBins, 0., 2.);   
        h_j_ptOverAK8g[i] = new TProfile(("h_j_" + jetTypes[i] + "_ptOverAK8g").c_str(),("; jet pT ratio (" + jetTypes[i] + "/ak8g);").c_str(),nBins, 0., 2.);   
        
        p_j_massOverAK5g[i] = new TProfile(("p_j_" + jetTypes[i] + "_massOverAK5g").c_str(),("; jet pT; jet mass ratio (" + jetTypes[i] + "/ak5g)").c_str(),28,xbinsProfile, 0., 5.);   
        p_j_massOverAK7g[i] = new TProfile(("p_j_" + jetTypes[i] + "_massOverAK7g").c_str(),("; jet pT; jet mass ratio (" + jetTypes[i] + "/ak7g)").c_str(),28,xbinsProfile, 0., 5.);   
        p_j_massOverAK8g[i] = new TProfile(("p_j_" + jetTypes[i] + "_massOverAK8g").c_str(),("; jet pT; jet mass ratio (" + jetTypes[i] + "/ak8g)").c_str(),28,xbinsProfile, 0., 5.);   
        p_j_ptOverAK5g[i] = new TProfile(("p_j_" + jetTypes[i] + "_ptOverAK5g").c_str(),("; jet pT; jet pT ratio (" + jetTypes[i] + "/ak5g)").c_str(),28,xbinsProfile, 0., 5.);   
        p_j_ptOverAK7g[i] = new TProfile(("p_j_" + jetTypes[i] + "_ptOverAK7g").c_str(),("; jet pT; jet pT ratio (" + jetTypes[i] + "/ak7g)").c_str(),28,xbinsProfile, 0., 5.);   
        p_j_ptOverAK8g[i] = new TProfile(("p_j_" + jetTypes[i] + "_ptOverAK8g").c_str(),("; jet pT; jet pT ratio (" + jetTypes[i] + "/ak8g)").c_str(),28,xbinsProfile, 0., 5.);   
    
    }
    
    
    Notify();
}

Bool_t buildHistos::Notify()
{
    // The Notify() function is called when a new file is opened. This
    // can be either for a new TTree in a TChain or when when a new TTree
    // is started when using PROOF. It is normally not necessary to make changes
    // to the generated code, but the routine can be extended by the
    // user if needed. The return value is currently not used.
    
    return kTRUE;
}

void buildHistos::Show(Long64_t entry)
{
    // Print contents of entry.
    // If entry is not specified, print current entry
    if (!fChain) return;
    fChain->Show(entry);
}
Int_t buildHistos::Cut(Long64_t entry)
{
    // This function may be called from Loop.
    // returns  1 if entry is accepted.
    // returns -1 otherwise.
    return 1;
}
#endif // #ifdef buildHistos_cxx
