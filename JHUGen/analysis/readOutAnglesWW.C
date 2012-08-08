#include <string>
#include <sstream>
#include <iostream>
#include "TFile.h"
#include "TList.h"
#include "TNtuple.h"
#include "TTree.h"
#include <vector>
#include <iomanip>
#include <cstdlib>
#include "TLorentzVector.h"


using namespace std;

void calculateAngles(TLorentzVector p4H, TLorentzVector p4Z1, TLorentzVector p4M11, TLorentzVector p4M12, TLorentzVector p4Z2, TLorentzVector p4M21, TLorentzVector p4M22, double& costheta1, double& costheta2, double& phi, double& costhetastar, double& phistar1, double& phistar2, double& phistar12, double& phi1, double& phi2, bool verbose);

void readOutAnglesWW(std::string filename, bool debug = false ) {
  
  ifstream fin;
  std::string filenameT = filename + ".txt";
  std::cout << "Processing " << filenameT << std::endl;
  fin.open(filenameT.c_str());
  int maxEvents = 1000000;
  
  char oname[192];
  sprintf(oname,"%s.root",filename.c_str());
  TFile fout(oname, "RECREATE");
  TTree* tree = new TTree("angles", "angles");
  
  Double_t m_costheta1, m_costheta2, m_phi, m_costhetastar, m_phistar1, m_phistar2, m_phistar12, m_phi1, m_phi2;
  Double_t m_wwmass, m_wplusmass, m_wminusmass;
  
  tree->Branch("wwmass", &m_wwmass, "wwmass/D");
  tree->Branch("wplusmass", &m_wplusmass, "wplusmass/D");
  tree->Branch("wminusmass", &m_wminusmass, "wminusmass/D");
  
  tree->Branch("costheta1", &m_costheta1, "costheta1/D");
  tree->Branch("costheta2", &m_costheta2, "costheta2/D");
  tree->Branch("phi", &m_phi, "phi/D");
  tree->Branch("costhetastar", &m_costhetastar, "costhetastar/D");
  tree->Branch("phi1", &m_phi1, "phi1/D");
  tree->Branch("phi2", &m_phi2, "phi2/D");
  tree->Branch("phistar1", &m_phistar1, "phistar1/D");
  tree->Branch("phistar2", &m_phistar2, "phistar2/D");
  tree->Branch("phistar12", &m_phistar12, "phistar12/D");
  
  Double_t m_lplus_pT, m_nu_pT, m_lminus_pT, m_nubar_pT;
  tree->Branch("lp_pT", &m_lplus_pT, "lp_pT/D");
  tree->Branch("nu_pT", &m_nu_pT, "nu_pT/D");
  tree->Branch("lm_pT", &m_lminus_pT, "lm_pT/D");
  tree->Branch("nubar_pT", &m_nubar_pT, "nubar_pT/D");
  
  //
  // WW analysis specific variables
  // 
  Double_t m_dphill, m_mll, m_leadleppt, m_trailleppt, m_met, m_dilpt, m_mt, m_leadlepeta, m_traillepeta;
  tree->Branch("dphill", &m_dphill, "dphill/D");
  tree->Branch("mll", &m_mll, "mll/D");
  tree->Branch("leadleppt", &m_leadleppt, "leadleppt/D");
  tree->Branch("trailleppt", &m_trailleppt, "trailleppt/D");
  tree->Branch("leadlepeta", &m_leadlepeta, "leadlepeta/D");
  tree->Branch("traillepeta", &m_traillepeta, "traillepeta/D");
  tree->Branch("met", &m_met, "met/D");	
  tree->Branch("mt", &m_mt, "mt/D");
  tree->Branch("dilpt", &m_dilpt, "dilpt/D");
  
  // 
  // resonance pT
  // 
  Double_t m_xpt, m_xmass;
  tree->Branch("xpt", &m_xpt, "xpt/D");
  tree->Branch("xmass", &m_xmass, "xmass/D");


  int ctr = 0;
  int iFile = 0;
  while (!fin.eof() && fin.good()) {
    
    std::vector <double> listOfMom;
    int idup[4], istup[4], mothup[4][2], icolup[4][2];
    double pup[4][5], vtimup[4], spinup[4];
    
    for (int a = 0; a < 4; a++){
      fin >> idup[a] >> istup[a] >> mothup[a][0] >> mothup[a][1] >> icolup[a][0] >> icolup[a][1];
      // std::cout <<  idup[a] << " " << istup[a] << " " <<  mothup[a][0]  << " " << mothup[a][1] << " " <<  icolup[a][0] << " " << icolup[a][1] << "\n";
      for (int i = 0; i < 5; i++)
	{
	  fin >> pup[a][i];
	}
      fin >> vtimup[a] >> spinup[a];
    }
    
    bool takeEvent = true;
    // check if one of the Id is tau or nu tau
    if ( TMath::Abs(idup[0]) == 15 || TMath::Abs(idup[1]) == 15 || TMath::Abs(idup[2]) == 15 || TMath::Abs(idup[2]) == 15 ) takeEvent = false;
    if ( TMath::Abs(idup[0]) == 16 || TMath::Abs(idup[1]) == 16 || TMath::Abs(idup[2]) == 16 || TMath::Abs(idup[2]) == 16 ) takeEvent = false;

    if ( !takeEvent && debug ) {
      std::cout << "--------------------------------\n";
      std::cout << "Event rejected \n";
      std::cout << idup[0] << ": " << pup[0][0] << "\t" << pup[0][1] << "\t" << pup[0][2] << "\t" << pup[0][3] << "\n";
      std::cout << idup[1] << ": " << pup[1][0] << "\t" << pup[1][1] << "\t" << pup[1][2] << "\t" << pup[1][3] << "\n";
      std::cout << idup[2] << ": " << pup[2][0] << "\t" << pup[2][1] << "\t" << pup[2][2] << "\t" << pup[2][3] << "\n";
      std::cout << idup[3] << ": " << pup[3][0] << "\t" << pup[3][1] << "\t" << pup[3][2] << "\t" << pup[3][3] << "\n";
    }


    TLorentzVector nu, lplus, nubar, lminus;    
    if (takeEvent) {
      
      if (mothup[0][0] == mothup[1][0]){
	lplus = new TLorentzVector(pup[0][0], pup[0][1], pup[0][2], pup[0][3]);
	nu = new TLorentzVector(pup[1][0], pup[1][1], pup[1][2], pup[1][3]);
	if (idup[2] < 0){
	  nubar = new TLorentzVector(pup[2][0], pup[2][1], pup[2][2], pup[2][3]);
	  lminus = new TLorentzVector(pup[3][0], pup[3][1], pup[3][2], pup[3][3]);		
	}
	else {
	  lminus = new TLorentzVector(pup[2][0], pup[2][1], pup[2][2], pup[2][3]);
	  nubar = new TLorentzVector(pup[3][0], pup[3][1], pup[3][2], pup[3][3]);						
	}
      }
      else if (mothup[0][0] == mothup[2][0]){
	lplus = new TLorentzVector(pup[0][0], pup[0][1], pup[0][2], pup[0][3]);
	nu = new TLorentzVector(pup[2][0], pup[2][1], pup[2][2], pup[2][3]);
	if (idup[1] < 0){
	  nubar = new TLorentzVector(pup[1][0], pup[1][1], pup[1][2], pup[1][3]);
	  lminus = new TLorentzVector(pup[3][0], pup[3][1], pup[3][2], pup[3][3]);		
	}
	else {
	  lminus = new TLorentzVector(pup[1][0], pup[1][1], pup[1][2], pup[1][3]);
	  nubar = new TLorentzVector(pup[3][0], pup[3][1], pup[3][2], pup[3][3]);			
	}
      }
      else if (mothup[0][0] == mothup[3][0]){
	lplus = new TLorentzVector(pup[0][0], pup[0][1], pup[0][2], pup[0][3]);
	nu = new TLorentzVector(pup[3][0], pup[3][1], pup[3][2], pup[3][3]);
	if (idup[1] < 0){
	  nubar = new TLorentzVector(pup[1][0], pup[1][1], pup[1][2], pup[1][3]);
	  lminus = new TLorentzVector(pup[2][0], pup[2][1], pup[2][2], pup[2][3]);		
	}
	else {
	  lminus = new TLorentzVector(pup[1][0], pup[1][1], pup[1][2], pup[1][3]);
	  nubar = new TLorentzVector(pup[2][0], pup[2][1], pup[2][2], pup[2][3]);		
	}				
      }
     
      TLorentzVector Wplus = nu+lplus;
      TLorentzVector Wminus = nubar+lminus;
      TLorentzVector X = Wplus + Wminus;

      if ( debug ) {
	std::cout << "--------------------------------\n";
	std::cout << "Event accepted \n";
	std::cout << Form("nu (px, py, pz, E): (%.3f, %.3f, %.3f, %.3f) \n", nu.Px(), nu.Py(), nu.Pz(), nu.E());
	std::cout << Form("lplus (px, py, pz, E): (%.3f, %.3f, %.3f, %.3f) \n", lplus.Px(), lplus.Py(), lplus.Pz(), lplus.E());
	std::cout << Form("lminus (px, py, pz, E): (%.3f, %.3f, %.3f, %.3f) \n", lminus.Px(), lminus.Py(), lminus.Pz(), lminus.E());
	std::cout << Form("nubar (px, py, pz, E): (%.3f, %.3f, %.3f, %.3f) \n", nubar.Px(), nubar.Py(), nubar.Pz(), nubar.E());
	std::cout << Form("WW pT: %.3f \n", X.Pt() );
      }
      
      double angle_costheta1, angle_costheta2, angle_phi, angle_costhetastar, angle_phistar1, angle_phistar2, angle_phistar12, angle_phi1, angle_phi2;
      calculateAngles( X, Wplus, nu, lplus,  Wminus, lminus, nubar, angle_costheta1, angle_costheta2, angle_phi, angle_costhetastar, angle_phistar1, angle_phistar2, angle_phistar12, angle_phi1, angle_phi2, false);
      
      m_costheta1 = angle_costheta1;
      m_costheta2 = angle_costheta2;
      m_phi = angle_phi;
      m_costhetastar = angle_costhetastar;
      m_phistar1 = angle_phistar1;
      m_phistar2 = angle_phistar2;
      m_phistar12 = angle_phistar12;
      m_phi1 = angle_phi1;
      m_phi2 = angle_phi2;
      
      m_wwmass = X.M();
      m_wplusmass = Wplus.M();
      m_wminusmass = Wminus.M();
      
      m_lplus_pT = lplus.Pt();
      m_nu_pT = nu.Pt();
      m_lminus_pT = lminus.Pt();
      m_nubar_pT = nubar.Pt();
      
      // 
      // get the WW analysis variables
      // 
      double dphillvalue = lplus.Phi() - lminus.Phi();
      while (dphillvalue > TMath::Pi()) dphillvalue -= 2*TMath::Pi();
      while (dphillvalue <= -TMath::Pi()) dphillvalue += 2*TMath::Pi();
      m_dphill  = TMath::Abs(dphillvalue);
      m_mll = (lplus + lminus).M();
      
      m_leadleppt = lplus.Pt() > lminus.Pt() ? lplus.Pt() : lminus.Pt();
      m_trailleppt = lplus.Pt() < lminus.Pt() ? lplus.Pt() : lminus.Pt();
      m_leadlepeta = lplus.Pt() > lminus.Pt() ? lplus.Eta() : lminus.Eta();
      m_traillepeta = lplus.Pt() < lminus.Pt() ? lplus.Eta() : lminus.Eta();
      m_met = sqrt(pow(nu.Px()+nubar.Px(), 2) + pow(nu.Py()+nubar.Py(), 2));
      m_dilpt = (lplus+lminus).Pt();
      double dphidilmet = (lplus+lminus).Phi() - (nu+nubar).Phi();
      while (dphidilmet > TMath::Pi()) dphidilmet -= 2*TMath::Pi();
      while (dphidilmet <= -TMath::Pi()) dphidilmet += 2*TMath::Pi();
      m_mt  = 2*sqrt(m_dilpt * m_met ) * fabs(sin(dphidilmet / 2.));
      m_xpt = X.Pt();
      m_xmass = X.M();
      // std::cout << __LINE__ << "\n";
      tree->Fill();
    }
    
    // counter
    ctr++;
    if (ctr%10000 == 0) std::cout << "event number: " << ctr << std::endl;
    if (ctr == maxEvents) break;
  }
  
  fout.cd();
  tree->Write();
  fout.Close();
  
}
void calculateAngles(TLorentzVector thep4H, TLorentzVector thep4Z1, TLorentzVector thep4M11, TLorentzVector thep4M12, TLorentzVector thep4Z2, TLorentzVector thep4M21, TLorentzVector thep4M22, double& costheta1, double& costheta2, double& phi, double& costhetastar, double& phistar1, double& phistar2, double& phistar12, double& phi1, double& phi2, bool verbose)
{
  
  if ( verbose) 
    std::cout << "In calculate angles..." << std::endl;
  
  double norm;
  
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
  
  TLorentzVector p4H, p4Z1, p4M11, p4M12, p4Z2, p4M21, p4M22;
  p4H = thep4H;
  p4Z1 = thep4Z1; p4M11 = thep4M11; p4M12 = thep4M12;
  p4Z2 = thep4Z2; p4M21 = thep4M21; p4M22 = thep4M22;
  costhetastar = theZ1X_p3.CosTheta();
  
    
    if (verbose) 
      std::cout << "phi1: " << phi1 << ", phi2: " << phi2 << std::endl;
    
    // now helicity angles................................
    // ...................................................
    TVector3 boostZ1 = -(p4Z1.BoostVector());
    TLorentzVector p4Z2Z1(p4Z2);
    p4Z2Z1.Boost(boostZ1);
    //find the decay axis
    TVector3 unitx_1( -p4Z2Z1.X(), -p4Z2Z1.Y(), -p4Z2Z1.Z() );
    norm = 1/(unitx_1.Mag());
    unitx_1*=norm;
    //boost daughters of z2
    TLorentzVector p4M21Z1(p4M21);
    TLorentzVector p4M22Z1(p4M22);
    p4M21Z1.Boost(boostZ1);
    p4M22Z1.Boost(boostZ1);
    //create z and y axes
    TVector3 p4M21Z1_p3( p4M21Z1.X(), p4M21Z1.Y(), p4M21Z1.Z() );
    TVector3 p4M22Z1_p3( p4M22Z1.X(), p4M22Z1.Y(), p4M22Z1.Z() );
    TVector3 unitz_1 = p4M21Z1_p3.Cross( p4M22Z1_p3 );
    norm = 1/(unitz_1.Mag());
    unitz_1 *= norm;
    TVector3 unity_1 = unitz_1.Cross(unitx_1);
    
    //caculate theta1
    TLorentzVector p4M11Z1(p4M11);
    p4M11Z1.Boost(boostZ1);
    TVector3 p3M11( p4M11Z1.X(), p4M11Z1.Y(), p4M11Z1.Z() );
    TVector3 unitM11 = p3M11.Unit();
    double x_m11 = unitM11.Dot(unitx_1); double y_m11 = unitM11.Dot(unity_1); double z_m11 = unitM11.Dot(unitz_1);
    TVector3 M11_Z1frame(y_m11, z_m11, x_m11);
    costheta1 = M11_Z1frame.CosTheta();
    if (verbose) 
      std::cout << "theta1: " << M11_Z1frame.Theta() << std::endl;
    
    //////-----------------------old way of calculating phi---------------/////////
    phi = M11_Z1frame.Phi();
    
    //set axes for other system
    TVector3 boostZ2 = -(p4Z2.BoostVector());
    TLorentzVector p4Z1Z2(p4Z1);
    p4Z1Z2.Boost(boostZ2);
    TVector3 unitx_2( -p4Z1Z2.X(), -p4Z1Z2.Y(), -p4Z1Z2.Z() );
    norm = 1/(unitx_2.Mag());
    unitx_2*=norm;
    //boost daughters of z2
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
    //calcuate theta2
    TLorentzVector p4M21Z2(p4M21);
    p4M21Z2.Boost(boostZ2);
    TVector3 p3M21( p4M21Z2.X(), p4M21Z2.Y(), p4M21Z2.Z() );
    TVector3 unitM21 = p3M21.Unit();
    double x_m21 = unitM21.Dot(unitx_2); double y_m21 = unitM21.Dot(unity_2); double z_m21 = unitM21.Dot(unitz_2);
    TVector3 M21_Z2frame(y_m21, z_m21, x_m21);
    costheta2 = M21_Z2frame.CosTheta();
    // calculate phi
    //calculating phi_n
    TLorentzVector n_p4Z1inXFrame( p4Z1 );
    TLorentzVector n_p4M11inXFrame( p4M11 );
    n_p4Z1inXFrame.Boost( boostX );
    n_p4M11inXFrame.Boost( boostX );        
    TVector3 n_p4Z1inXFrame_unit = n_p4Z1inXFrame.Vect().Unit();
    TVector3 n_p4M11inXFrame_unit = n_p4M11inXFrame.Vect().Unit();  
    TVector3 n_unitz_1( n_p4Z1inXFrame_unit );
    //// y-axis is defined by neg lepton cross z-axis
    //// the subtle part is here...
    //////////TVector3 n_unity_1 = n_p4M11inXFrame_unit.Cross( n_unitz_1 );
    TVector3 n_unity_1 = n_unitz_1.Cross( n_p4M11inXFrame_unit );
    TVector3 n_unitx_1 = n_unity_1.Cross( n_unitz_1 );
    
    TLorentzVector n_p4M21inXFrame( p4M21 );
    n_p4M21inXFrame.Boost( boostX );
    TVector3 n_p4M21inXFrame_unit = n_p4M21inXFrame.Vect().Unit();
    //rotate into other plane
    TVector3 n_p4M21inXFrame_unitprime( n_p4M21inXFrame_unit.Dot(n_unitx_1), n_p4M21inXFrame_unit.Dot(n_unity_1), n_p4M21inXFrame_unit.Dot(n_unitz_1) );
    
    //-----------------new way of calculating phi-----------------///////
    // and then calculate phistar1
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
    //////TVector3 n_unity_2 = n_p4M21inXFrame_unit.Cross( n_unitz_2 );
    TVector3 n_unity_2 = n_unitz_2.Cross( n_p4M21inXFrame_unit );
    TVector3 n_unitx_2 = n_unity_2.Cross( n_unitz_2 );
    TVector3 n_p4PartoninZ2PlaneFrame_unitprime( n_p4PartoninXFrame_unit.Dot(n_unitx_2), n_p4PartoninXFrame_unit.Dot(n_unity_2), n_p4PartoninXFrame_unit.Dot(n_unitz_2) );
    phistar2 = (n_p4PartoninZ2PlaneFrame_unitprime.Phi());
    
    double phistar12_0 = phistar1 + phistar2;
    if (phistar12_0 > TMath::Pi()) phistar12 = phistar12_0 - 2*TMath::Pi();
    else if (phistar12_0 < (-1.)*TMath::Pi()) phistar12 = phistar12_0 + 2*TMath::Pi();
    else phistar12 = phistar12_0;
}


