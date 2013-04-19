#include <string>
#include <sstream>
#include <iostream>
#include <fstream>
#include <vector>
#include <iomanip>
#include <cstdlib>
#include "TFile.h"
#include "TList.h"
#include "TNtuple.h"
#include "TTree.h"
#include "TRandom.h"
#include "TLorentzVector.h"

using namespace std;

TRandom randomForSmearing;

TLorentzVector applyResolution(TLorentzVector l_gen);

void calculateAngles(TLorentzVector p4H, TLorentzVector p4Z1, TLorentzVector p4M11, TLorentzVector p4M12, TLorentzVector p4Z2, TLorentzVector p4M21, TLorentzVector p4M22, double& costheta1, double& costheta2, double& phi, double& costhetastar, double& phistar1, double& phistar2, double& phistar12, double& phi1, double& phi2);

const float Zmass = 91.19;

enum Flavors {electron, muon, tau, e2mu2, e2tau2, mu2tau2, NumFlavors};

void readOutAngles_LMH(std::string filename, bool applyRes=false){
  
    ifstream fin;
    std::string filenameT = filename + ".txt";
    std::cout << "Processing " << filenameT << std::endl;
    fin.open(filenameT.c_str());
    
    int maxEvents = 20000000;
    bool debug = false; 
	
    char oname[250];
    if(applyRes)
      sprintf(oname,"%s_wResolution.root",filename.c_str());
    else
      sprintf(oname,"%s.root",filename.c_str());
    TFile fout(oname, "RECREATE");
    TTree* tree = new TTree("SelectedTree", "SelectedTree");
    
    Float_t m_costheta1, m_costheta2, m_phi, m_costhetastar, m_phistar1;
    //Float_t m_phistar2, m_phistar12, m_phi1, m_phi2;
    Float_t m_zzmass, m_z1mass, m_z2mass;
    
    tree->Branch("ZZMass", &m_zzmass, "ZZMass/F");
    tree->Branch("Z1Mass", &m_z1mass, "Z1Mass/F");
    tree->Branch("Z2Mass", &m_z2mass, "Z2Mass/F");
    
    tree->Branch("helcosthetaZ1", &m_costheta1, "helcosthetaZ1/F");
    tree->Branch("helcosthetaZ2", &m_costheta2, "helcosthetaZ2/F");
    tree->Branch("helphi", &m_phi, "helphi/F");
    tree->Branch("costhetastar", &m_costhetastar, "costhetastar/F");
    // tree->Branch("upsilon1", &m_phi1, "phi1/F");
    // tree->Branch("upsilon2", &m_phi2, "phi2/F");
    tree->Branch("phistarZ1", &m_phistar1, "phistarZ1/F");
    // tree->Branch("phistar2", &m_phistar2, "phistar2/F");
    // tree->Branch("phistar12", &m_phistar12, "phistar12/F");
    
    Float_t m_l1minus_pT, m_l1plus_pT, m_l2minus_pT, m_l2plus_pT;
    Float_t m_l1minus_eta, m_l1plus_eta, m_l2minus_eta, m_l2plus_eta;
    Float_t Y4l, eta4l, pT4l,interf;
    tree->Branch("l1m_pT", &m_l1minus_pT, "l1m_pT/F");
    tree->Branch("l1p_pT", &m_l1plus_pT, "l1p_pT/F");
    tree->Branch("l2m_pT", &m_l2minus_pT, "l2m_pT/F");
    tree->Branch("l2p_pT", &m_l2plus_pT, "l2p_pT/F");
    tree->Branch("l1m_eta", &m_l1minus_eta, "l1m_eta/F");
    tree->Branch("l1p_eta", &m_l1plus_eta, "l1p_eta/F");
    tree->Branch("l2m_eta", &m_l2minus_eta, "l2m_eta/F");
    tree->Branch("l2p_eta", &m_l2plus_eta, "l2p_eta/F");
    tree->Branch("interf", &interf, "interf/F");
    tree->Branch("Y4l",&Y4l,"Y4l/F");
    tree->Branch("eta4l",&eta4l,"eta4l/F");
    tree->Branch("pT4l",&pT4l,"pT4l/F");

    int flatype;
    tree->Branch("flavortype",&flatype,"flavortype/i");
    
    int ctr = 0;
    int FourlCount = 0;
    std::vector <float> listOfMom;
    int idup[4], istup[4], mothup[4][2], icolup[4][2];
    float pup[4][5], vtimup[4], spinup[4];
    TLorentzVector l1_minus, l1_plus, l2_minus, l2_plus;
    while (!fin.eof() && fin.good()){
      for (int a = 0; a < 4; a++){
	fin >> idup[a] >> istup[a] >> mothup[a][0] >> mothup[a][1] >> icolup[a][0] >> icolup[a][1];
	for (int i = 0; i < 5; i++){
	  fin >> pup[a][i];
	}
	fin >> vtimup[a] >> spinup[a];
      }
      // electron = 11, muon = 13, tau = 15
      if( ( fabs(idup[0])==11&&fabs(idup[1])==11&&fabs(idup[2])==11&&fabs(idup[3])==11 ) || (fabs(idup[0])==13&&fabs(idup[1])==13&&fabs(idup[2])==13&&fabs(idup[3])==13 ) || (fabs(idup[0])==15&&fabs(idup[1])==15&&fabs(idup[2])==15&&fabs(idup[3])==15 ) ) interf=1;  
      else interf=0;
      
      if(interf==1) FourlCount++;
      
      TLorentzVector Graviton;
      TLorentzVector pZ1; TLorentzVector pl1_m; TLorentzVector pl1_p;
      TLorentzVector pZ2; TLorentzVector pl2_m; TLorentzVector pl2_p;
      
      //Distinguish the flavor type: 0 = mixed leptons, 1 4mu, 2 4e, 3 = tau
      if(abs(idup[0])==abs(idup[1]) && abs(idup[0])==abs(idup[2]) && abs(idup[0])==abs(idup[3]) ){
	if(abs(idup[0])==13){
	  flatype = muon; 
	}
	else if(abs(idup[0])==11){
	  flatype = electron;
        }
        else if(abs(idup[0])==15){    
          flatype = tau;
        }
	else{
	  cout<<"not 4l process"<<endl;
	  break;}
      }
      //else flatype = mixedFlavor;
      else { // find the final state
        int num_e=0, num_mu=0, num_tau=0;
        for (int lep = 0; lep<4; lep++) { // count the number of each particle
          if (idup[lep] == 11) {
            num_e++;
          } else if (idup[lep] == 13) {
            num_mu++;
          } else if (idup[lep] == 15) {
            num_tau++;
          } 
        }
        if (num_e == num_mu) {
          flatype = e2mu2;
        } else if (num_e == num_tau) {
          flatype = e2tau2;
        } else if (num_mu == num_tau) {
          flatype = mu2tau2;  
        } else {
          cout<<"could not determine 2l2l final state"<<endl;
        }
      }
      
      
      int l1p,l1m,l2p,l2m; // record the reading order of each lepton in the lhe file, for debug use. 
      
      //For flavor type mixed, treat as uninterferenced
      if( (flatype== e2mu2) || (flatype == e2tau2) || (flatype == mu2tau2) ){	     
	
	if (mothup[0][0] == mothup[1][0]){
	  l1_minus.SetPxPyPzE(pup[0][0], pup[0][1], pup[0][2], pup[0][3]);
	  l1_plus.SetPxPyPzE(pup[1][0], pup[1][1], pup[1][2], pup[1][3]);
	  
	  if (idup[2] > 0){
	    l2_minus.SetPxPyPzE(pup[2][0], pup[2][1], pup[2][2], pup[2][3]);
	    l2_plus.SetPxPyPzE(pup[3][0], pup[3][1], pup[3][2], pup[3][3]);	
	  }
	  else {
	    l2_plus.SetPxPyPzE(pup[2][0], pup[2][1], pup[2][2], pup[2][3]);
	    l2_minus.SetPxPyPzE(pup[3][0], pup[3][1], pup[3][2], pup[3][3]);						
	  }
	}
	else if (mothup[0][0] == mothup[2][0]){
	  if (idup[1] > 0){
	    l2_minus.SetPxPyPzE(pup[1][0], pup[1][1], pup[1][2], pup[1][3]);
	    l2_plus.SetPxPyPzE(pup[3][0], pup[3][1], pup[3][2], pup[3][3]);	
	  }
	  else {
	    l2_plus.SetPxPyPzE(pup[1][0], pup[1][1], pup[1][2], pup[1][3]);
	    l2_minus.SetPxPyPzE(pup[3][0], pup[3][1], pup[3][2], pup[3][3]);			
	  }
	}
	else if (mothup[0][0] == mothup[3][0]){
	  l1_minus.SetPxPyPzE(pup[0][0], pup[0][1], pup[0][2], pup[0][3]);
	  l1_plus.SetPxPyPzE(pup[3][0], pup[3][1], pup[3][2], pup[3][3]);
	  if (idup[1] > 0){
	    l2_minus.SetPxPyPzE(pup[1][0], pup[1][1], pup[1][2], pup[1][3]);
	    l2_plus.SetPxPyPzE(pup[2][0], pup[2][1], pup[2][2], pup[2][3]);		
	  }
	  else {
	    l1_plus.SetPxPyPzE(pup[1][0], pup[1][1], pup[1][2], pup[1][3]);
	    l1_minus.SetPxPyPzE(pup[2][0], pup[2][1], pup[2][2], pup[2][3]);		
	  }				
	}else{continue;}
	
	if(applyRes){
	  l1_minus = applyResolution(l1_minus);
	  l2_minus = applyResolution(l2_minus);
	  l1_plus  = applyResolution(l1_plus);
	  l2_plus  = applyResolution(l2_plus);
	}
	
	TLorentzVector Z1 = l1_minus + l1_plus;
	TLorentzVector Z2 = l2_minus + l2_plus;
	Graviton = l1_minus+l1_plus+l2_minus+l2_plus;

	pl1_m=l1_minus;
	pl1_p=l1_plus;
	pl2_m=l2_minus;
	pl2_p=l2_plus;
	
	if ( fabs(Zmass-Z1.M()) > fabs(Zmass-Z2.M()) ){				
	  pZ1 = Z2; pl1_m = l2_minus; pl1_p = l2_plus;
	  pZ2 = Z1; pl2_m = l1_minus; pl2_p = l1_plus;
	}
	else {
	  pZ1 = Z1; pl1_m = l1_minus; pl1_p = l1_plus;
	  pZ2 = Z2; pl2_m = l2_minus; pl2_p = l2_plus;
	}
      }
      
      
      //type electron, muon, or tau: interference
      else{
	if(idup[0]>0){
	  l1_minus.SetPxPyPzE(pup[0][0], pup[0][1], pup[0][2], pup[0][3]);
	  if(idup[1]>0){
	    l2_minus.SetPxPyPzE(pup[1][0], pup[1][1], pup[1][2], pup[1][3]);
	    l1_plus.SetPxPyPzE(pup[2][0], pup[2][1], pup[2][2], pup[2][3]);
	    l2_plus.SetPxPyPzE(pup[3][0], pup[3][1], pup[3][2], pup[3][3]);
	    l1p=2; l1m=0; l2p=3; l2m=1;
	    if (debug) cout << "case1" << endl;
	  }
	  else if(idup[2]>0){
	    l1_plus.SetPxPyPzE(pup[1][0], pup[1][1], pup[1][2], pup[1][3]);
	    l2_minus.SetPxPyPzE(pup[2][0], pup[2][1], pup[2][2], pup[2][3]);
	    l2_plus.SetPxPyPzE(pup[3][0], pup[3][1], pup[3][2], pup[3][3]);
	    l1p=1; l1m=0; l2p=3; l2m=2;
	    if (debug) cout << "case2" << endl; 
	  }
	  else{
	    l1_plus.SetPxPyPzE(pup[1][0], pup[1][1], pup[1][2], pup[1][3]);
	    l2_plus.SetPxPyPzE(pup[2][0], pup[2][1], pup[2][2], pup[2][3]);
	    l2_minus.SetPxPyPzE(pup[3][0], pup[3][1], pup[3][2], pup[3][3]);
	    l1p=1; l1m=0; l2p=2; l2m=3;
	    if (debug) cout << "case3" << endl;
	  }
	}
	else{
	  l1_plus.SetPxPyPzE(pup[0][0], pup[0][1], pup[0][2], pup[0][3]);
	  if(idup[1]<0){
	    l2_plus.SetPxPyPzE(pup[1][0], pup[1][1], pup[1][2], pup[1][3]);
	    l1_minus.SetPxPyPzE(pup[2][0], pup[2][1], pup[2][2], pup[2][3]);
	    l2_minus.SetPxPyPzE(pup[3][0], pup[3][1], pup[3][2], pup[3][3]);
	    l1p=0; l1m=2; l2p=1; l2m=3;
	    if (debug) cout << "case4" << endl;
	  }
	  else if(idup[2]<0){
	    l1_minus.SetPxPyPzE(pup[1][0], pup[1][1], pup[1][2], pup[1][3]);
	    l2_plus.SetPxPyPzE(pup[2][0], pup[2][1], pup[2][2], pup[2][3]);
	    l2_minus.SetPxPyPzE(pup[3][0], pup[3][1], pup[3][2], pup[3][3]);
	    l1p=0; l1m=1; l2p=2; l2m=3;
	    if (debug) cout << "case5" << endl;  
	  }
	  else{
	    l1_minus.SetPxPyPzE(pup[1][0], pup[1][1], pup[1][2], pup[1][3]);
	    l2_minus.SetPxPyPzE(pup[2][0], pup[2][1], pup[2][2], pup[2][3]);
	    l2_plus.SetPxPyPzE(pup[3][0], pup[3][1], pup[3][2], pup[3][3]);		      	
	    l1p=0; l1m=1; l2p=3; l2m=2;
	    if (debug) cout << "case6" << endl;
	  }
	}
	
	TLorentzVector Z1 = l1_minus + l1_plus;
	TLorentzVector Z2 = l2_minus + l2_plus;
	TLorentzVector Z1alt = l1_minus + l2_plus;
	TLorentzVector Z2alt = l2_minus + l1_plus;
	Graviton = l1_minus+l1_plus+l2_minus+l2_plus;
	
	if(fabs(Z1.M()-Zmass)>fabs(Z2.M()-Zmass)) swap(Z1,Z2);
	if(fabs(Z1alt.M()-Zmass)>fabs(Z2alt.M()-Zmass)) swap(Z1alt,Z2alt);
	if (debug) std::cout << "Before swap: Z1: " << Z1.M() << " Z2: " << Z2.M() << " Z1alt: " << Z1alt.M() << " Z2alt: " << Z2alt.M() << endl;  
	if(fabs(Z1alt.M()-Zmass)<fabs(Z1.M()-Zmass)){
	  swap(l1m,l2m);
	  swap(l1_minus,l2_minus);
	}
	Z1 = l1_minus + l1_plus;
	Z2 = l2_minus + l2_plus;
	
	if (debug) std::cout << "After swap: Z1: " << Z1.M() << " Z2: " << Z2.M() << " Z1alt: " << Z1alt.M() << " Z2alt: " << Z2alt.M() << endl;  
	
	// order Z1/Z2
	if ( fabs(Zmass-Z1.M()) > fabs(Zmass-Z2.M()) ){				
	  pZ1 = Z2; pl1_m = l2_minus; pl1_p = l2_plus;
	  pZ2 = Z1; pl2_m = l1_minus; pl2_p = l1_plus;
	}
	else {
	  pZ1 = Z1; pl1_m = l1_minus; pl1_p = l1_plus;
	  pZ2 = Z2; pl2_m = l2_minus; pl2_p = l2_plus;
	}	  
		  
	//debug for interference
	
	if (debug){
	  cout << "flavor type is " << flatype << std::endl;
	  std::cout << "l1minus: " << l1m << "," << idup[l1m] << ", l1plus: " << l1p << "," << idup[l1p] << std::endl;
	  std::cout << "l2minus: " << l2m << "," << idup[l2m] << ", l2plus: " << l2p << "," << idup[l2p] << std::endl;
	} 
      }
      
      
      
      double angle_costheta1, angle_costheta2, angle_phi, angle_costhetastar, angle_phistar1, angle_phistar2, angle_phistar12, angle_phi1, angle_phi2;
      calculateAngles( Graviton, pZ1, pl1_m, pl1_p, pZ2, pl2_m, pl2_p, angle_costheta1, angle_costheta2, angle_phi, angle_costhetastar, angle_phistar1, angle_phistar2, angle_phistar12, angle_phi1, angle_phi2);
      
      Y4l = Graviton.Rapidity();//0; //
      eta4l = Graviton.Rapidity();//0; //
      pT4l = Graviton.Rapidity();//0; //
      
      m_costheta1 = float(angle_costheta1);
      m_costheta2 = float(angle_costheta2);
      m_phi = float(angle_phi);
      m_costhetastar = float(angle_costhetastar);
      m_phistar1 = float(angle_phistar1);
      //m_phistar2 = float(angle_phistar2);
      //m_phistar12 = float(angle_phistar12);
      //m_phi1 = float(angle_phi1);
      //m_phi2 = float(angle_phi2);
      
      m_zzmass = float(Graviton.M());
      m_z1mass = float(pZ1.M());
      m_z2mass = float(pZ2.M());
      
      m_l1minus_pT = pl1_m.Pt();
      m_l1plus_pT = pl1_p.Pt();
      m_l2minus_pT = pl2_m.Pt();
      m_l2plus_pT = pl2_p.Pt();
      
      m_l1minus_eta = pl1_m.Eta();
      m_l1plus_eta = pl1_p.Eta();
      m_l2minus_eta = pl2_m.Eta();
      m_l2plus_eta = pl2_p.Eta();
      
      tree->Fill();
      
      // counter
      ctr++;
      if (ctr%1000 == 0) std::cout << "event number: " << ctr << std::endl;
      if (ctr == maxEvents) break;	
    }

    cout << "4l count: " << FourlCount << endl;
    
    fout.cd();
    tree->Write();
    fout.Close();
	
}

void calculateAngles(TLorentzVector thep4H, TLorentzVector thep4Z1, TLorentzVector thep4M11, TLorentzVector thep4M12, TLorentzVector thep4Z2, TLorentzVector thep4M21, TLorentzVector thep4M22, double& costheta1, double& costheta2, double& phi, double& costhetastar, double& phistar1, double& phistar2, double& phistar12, double& phi1, double& phi2){
	
  float norm;
  
  TVector3 boostX = -(thep4H.BoostVector());
  TLorentzVector thep4Z1inXFrame( thep4Z1 );
  TLorentzVector thep4Z2inXFrame( thep4Z2 );	
  thep4Z1inXFrame.Boost( boostX );
  thep4Z2inXFrame.Boost( boostX );
  TVector3 theZ1X_p3 = TVector3( thep4Z1inXFrame.X(), thep4Z1inXFrame.Y(), thep4Z1inXFrame.Z() );
  TVector3 theZ2X_p3 = TVector3( thep4Z2inXFrame.X(), thep4Z2inXFrame.Y(), thep4Z2inXFrame.Z() );
  
  // calculate phi1, phi2, costhetastar
  phi1 = theZ1X_p3.Phi();
  phi2 = theZ2X_p3.Phi();
  
  ///////////////////////////////////////////////
  // check for z1/z2 convention, redefine all 4 vectors with convention
  ///////////////////////////////////////////////	
  TLorentzVector p4H, p4Z1, p4M11, p4M12, p4Z2, p4M21, p4M22;
  p4H = thep4H;
  
  /* ORDER OF Z1 AND Z2 ALREADY CHOSEN IN MAIN FUNCTION!!!!!! - - - - - - 
     if ((phi1 < 0)&&(phi1 >= -TMath::Pi())){   // old convention based on phi
     p4Z1 = thep4Z2; p4M11 = thep4M21; p4M12 = thep4M22;
     p4Z2 = thep4Z1; p4M21 = thep4M11; p4M22 = thep4M12;		
     costhetastar = theZ2X_p3.CosTheta();
     }
     else{
     p4Z1 = thep4Z1; p4M11 = thep4M11; p4M12 = thep4M12;
     p4Z2 = thep4Z2; p4M21 = thep4M21; p4M22 = thep4M22;
     costhetastar = theZ1X_p3.CosTheta();
     }
     - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - -*/
  
  p4Z1 = thep4Z1; p4M11 = thep4M11; p4M12 = thep4M12;
  p4Z2 = thep4Z2; p4M21 = thep4M21; p4M22 = thep4M22;
  costhetastar = theZ1X_p3.CosTheta();
	
  // now helicity angles................................
  // ...................................................
  TVector3 boostZ1 = -(p4Z1.BoostVector());
  TLorentzVector p4Z2Z1(p4Z2);
  p4Z2Z1.Boost(boostZ1);
  // find the decay axis
  TVector3 unitx_1( -p4Z2Z1.X(), -p4Z2Z1.Y(), -p4Z2Z1.Z() );
  norm = 1/(unitx_1.Mag());
  unitx_1*=norm;
  // boost daughters of z2
  TLorentzVector p4M21Z1(p4M21);
  TLorentzVector p4M22Z1(p4M22);
  p4M21Z1.Boost(boostZ1);
  p4M22Z1.Boost(boostZ1);
  // create z and y axes
  TVector3 p4M21Z1_p3( p4M21Z1.X(), p4M21Z1.Y(), p4M21Z1.Z() );
  TVector3 p4M22Z1_p3( p4M22Z1.X(), p4M22Z1.Y(), p4M22Z1.Z() );
  TVector3 unitz_1 = p4M21Z1_p3.Cross( p4M22Z1_p3 );
  norm = 1/(unitz_1.Mag());
  unitz_1 *= norm;
  TVector3 unity_1 = unitz_1.Cross(unitx_1);
  
  // calculate theta1
  TLorentzVector p4M11Z1(p4M11);
  p4M11Z1.Boost(boostZ1);
  TVector3 p3M11( p4M11Z1.X(), p4M11Z1.Y(), p4M11Z1.Z() );
  TVector3 unitM11 = p3M11.Unit();
  float x_m11 = unitM11.Dot(unitx_1); float y_m11 = unitM11.Dot(unity_1); float z_m11 = unitM11.Dot(unitz_1);
  TVector3 M11_Z1frame(y_m11, z_m11, x_m11);
  costheta1 = M11_Z1frame.CosTheta();

  //////-----------------------old way of calculating phi---------------/////////
  phi = M11_Z1frame.Phi();
  
  // set axes for other system
  TVector3 boostZ2 = -(p4Z2.BoostVector());
  TLorentzVector p4Z1Z2(p4Z1);
  p4Z1Z2.Boost(boostZ2);
  TVector3 unitx_2( -p4Z1Z2.X(), -p4Z1Z2.Y(), -p4Z1Z2.Z() );
  norm = 1/(unitx_2.Mag());
  unitx_2*=norm;
  // boost daughters of z2
  TLorentzVector p4M11Z2(p4M11);
  TLorentzVector p4M12Z2(p4M12);
  p4M11Z2.Boost(boostZ2);
  p4M12Z2.Boost(boostZ2);
  TVector3 p4M11Z2_p3( p4M11Z2.X(), p4M11Z2.Y(), p4M11Z2.Z() );
  TVector3 p4M12Z2_p3( p4M12Z2.X(), p4M12Z2.Y(), p4M12Z2.Z() );
  TVector3 unitz_2 = p4M11Z2_p3.Cross( p4M12Z2_p3 );
  norm = 1/(unitz_2.Mag());
  unitz_2*=norm;
  TVector3 unity_2 = unitz_2.Cross(unitx_2);
  // calcuate theta2
  TLorentzVector p4M21Z2(p4M21);
  p4M21Z2.Boost(boostZ2);
  TVector3 p3M21( p4M21Z2.X(), p4M21Z2.Y(), p4M21Z2.Z() );
  TVector3 unitM21 = p3M21.Unit();
  float x_m21 = unitM21.Dot(unitx_2); float y_m21 = unitM21.Dot(unity_2); float z_m21 = unitM21.Dot(unitz_2);
  TVector3 M21_Z2frame(y_m21, z_m21, x_m21);
  costheta2 = M21_Z2frame.CosTheta();
  
  // calculate phi
  // calculating phi_n
  TLorentzVector n_p4Z1inXFrame( p4Z1 );
  TLorentzVector n_p4M11inXFrame( p4M11 );
  n_p4Z1inXFrame.Boost( boostX );
  n_p4M11inXFrame.Boost( boostX );        
  TVector3 n_p4Z1inXFrame_unit = n_p4Z1inXFrame.Vect().Unit();
  TVector3 n_p4M11inXFrame_unit = n_p4M11inXFrame.Vect().Unit();  
  TVector3 n_unitz_1( n_p4Z1inXFrame_unit );
  //// y-axis is defined by neg lepton cross z-axis
  //// the subtle part is here...
  TVector3 n_unity_1 = n_unitz_1.Cross( n_p4M11inXFrame_unit );
  TVector3 n_unitx_1 = n_unity_1.Cross( n_unitz_1 );
  
  TLorentzVector n_p4M21inXFrame( p4M21 );
  n_p4M21inXFrame.Boost( boostX );
  TVector3 n_p4M21inXFrame_unit = n_p4M21inXFrame.Vect().Unit();
  //rotate into other plane
  TVector3 n_p4M21inXFrame_unitprime( n_p4M21inXFrame_unit.Dot(n_unitx_1), n_p4M21inXFrame_unit.Dot(n_unity_1), n_p4M21inXFrame_unit.Dot(n_unitz_1) );
  
  ///////-----------------new way of calculating phi-----------------///////
  // float phi_n =  n_p4M21inXFrame_unitprime.Phi();
  /// and then calculate phistar1
  TVector3 n_p4PartoninXFrame_unit( 0.0, 0.0, 1.0 );
  TVector3 n_p4PartoninXFrame_unitprime( n_p4PartoninXFrame_unit.Dot(n_unitx_1), n_p4PartoninXFrame_unit.Dot(n_unity_1), n_p4PartoninXFrame_unit.Dot(n_unitz_1) );
  // negative sign is for arrow convention in paper
  phistar1 = (n_p4PartoninXFrame_unitprime.Phi());
  
  // and the calculate phistar2
  TLorentzVector n_p4Z2inXFrame( p4Z2 );
  n_p4Z2inXFrame.Boost( boostX );
  TVector3 n_p4Z2inXFrame_unit = n_p4Z2inXFrame.Vect().Unit();
  TVector3 n_unitz_2( n_p4Z2inXFrame_unit );
  //// y-axis is defined by neg lepton cross z-axis
  //// the subtle part is here...
  TVector3 n_unity_2 = n_unitz_2.Cross( n_p4M21inXFrame_unit );
  TVector3 n_unitx_2 = n_unity_2.Cross( n_unitz_2 );
  TVector3 n_p4PartoninZ2PlaneFrame_unitprime( n_p4PartoninXFrame_unit.Dot(n_unitx_2), n_p4PartoninXFrame_unit.Dot(n_unity_2), n_p4PartoninXFrame_unit.Dot(n_unitz_2) );
  phistar2 = (n_p4PartoninZ2PlaneFrame_unitprime.Phi());
  
  float phistar12_0 = phistar1 + phistar2;
  if (phistar12_0 > TMath::Pi()) phistar12 = phistar12_0 - 2*TMath::Pi();
  else if (phistar12_0 < (-1.)*TMath::Pi()) phistar12 = phistar12_0 + 2*TMath::Pi();
  else phistar12 = phistar12_0;
	
}
TLorentzVector applyResolution(TLorentzVector l_gen){

  float l_Perp, l_Theta, l_Phi;

  if(randomForSmearing.Uniform()<.9){
    l_Perp = l_gen.Perp()+(randomForSmearing.Gaus(0,0.012*1.15*l_gen.Perp()+0.00000*1.15* l_gen.Perp()* l_gen.Perp() ));
    l_Theta = l_gen.Theta()+(randomForSmearing.Gaus(0,0.001));
    l_Phi = l_gen.Phi()+(randomForSmearing.Gaus(0,0.001));
  }else{
    l_Perp = l_gen.Perp()+randomForSmearing.Gaus(-l_gen.Perp()*.04,l_gen.Perp()*.08);
    l_Theta = l_gen.Theta()+(randomForSmearing.Gaus(0,0.001));
    l_Phi = l_gen.Phi()+(randomForSmearing.Gaus(0,0.001));
  }
  float l_Px = l_Perp*cos(l_Phi);
  float l_Py = l_Perp*sin(l_Phi);
  float l_Pz = l_Perp/tan(l_Theta);
  float l_E = sqrt(l_Px*l_Px+l_Py*l_Py+l_Pz*l_Pz);

  TLorentzVector final_l;

  final_l.SetPxPyPzE(l_Px,l_Py,l_Pz,l_E);

  return (final_l);

}






