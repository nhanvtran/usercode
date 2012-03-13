
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

void calculateAngles(TLorentzVector p4H, TLorentzVector p4Z1, TLorentzVector p4M11, TLorentzVector p4M12, TLorentzVector p4Z2, TLorentzVector p4M21, TLorentzVector p4M22, double& costheta1, double& costheta2, double& phi, double& costhetastar, double& phistar1, double& phistar2, double& phistar12, double& phi1, double& phi2);

void readOutAngles_LMH(std::string filename){
	
	ifstream fin;
    std::string filenameT = filename + ".txt";
    std::cout << "Processing " << filenameT << std::endl;
	fin.open(filenameT.c_str());
	int maxEvents = 10000;
	
    char oname[192];
    sprintf(oname,"%s.root",filename.c_str());
	TFile fout(oname, "RECREATE");
	TTree* tree = new TTree("angles", "angles");
	
	Double_t m_costheta1, m_costheta2, m_phi, m_costhetastar, m_phistar1, m_phistar2, m_phistar12, m_phi1, m_phi2;
	Double_t m_zzmass, m_z1mass, m_z2mass;
	
	tree->Branch("zzmass", &m_zzmass, "zzmass/D");
	tree->Branch("z1mass", &m_z1mass, "z1mass/D");
	tree->Branch("z2mass", &m_z2mass, "z2mass/D");
	
	tree->Branch("costheta1", &m_costheta1, "costheta1/D");
	tree->Branch("costheta2", &m_costheta2, "costheta2/D");
	tree->Branch("phi", &m_phi, "phi/D");
	tree->Branch("costhetastar", &m_costhetastar, "costhetastar/D");
	tree->Branch("phi1", &m_phi1, "phi1/D");
	tree->Branch("phi2", &m_phi2, "phi2/D");
	tree->Branch("phistar1", &m_phistar1, "phistar1/D");
	tree->Branch("phistar2", &m_phistar2, "phistar2/D");
	tree->Branch("phistar12", &m_phistar12, "phistar12/D");
	
	Double_t m_l1minus_pT, m_l1plus_pT, m_l2minus_pT, m_l2plus_pT;
	tree->Branch("l1m_pT", &m_l1minus_pT, "l1m_pT/D");
	tree->Branch("l1p_pT", &m_l1plus_pT, "l1p_pT/D");
	tree->Branch("l2m_pT", &m_l2minus_pT, "l2m_pT/D");
	tree->Branch("l2p_pT", &m_l2plus_pT, "l2p_pT/D");
	
	int ctr = 0;
	int iFile = 0;
	while (!fin.eof() && fin.good()){
	  
		std::vector <double> listOfMom;
		int idup[4], istup[4], mothup[4][2], icolup[4][2];
		double pup[4][5], vtimup[4], spinup[4];
		
		//std::cout << "------------" << std::endl;
		//int var1, var2;
		//double var3, var4, var5, var6;
		//fin >> var1 >> var2 >> var3 >> var4 >> var5 >> var6;
		for (int a = 0; a < 4; a++){
			fin >> idup[a] >> istup[a] >> mothup[a][0] >> mothup[a][1] >> icolup[a][0] >> icolup[a][1];
			//std::cout << idup[a] << ", " << istup[a] << std::endl;
			for (int i = 0; i < 5; i++)
		    {
				fin >> pup[a][i];
			}
			fin >> vtimup[a] >> spinup[a];
		}
		
		//std::cout << "var1: " << var1 << ", " << var2 << ", " << var3 << std::endl;
		
		/*
		if ((idup[0] != 23)||(idup[1] != 23)){
			std::cout << "there is a mismatch!" << std::endl;
			std::cout << "idup[0]:  " << idup[0] << " " << istup[0] << " " << pup[0][0] << " " << pup[0][1] << " " << pup[0][2] << std::endl;
			std::cout << "idup[1]:  " << idup[1] << " " << istup[1] << " " << pup[1][0] << " " << pup[1][1] << " " << pup[1][2] << std::endl;
			std::cout << "idup[2]:  " << idup[2] << " " << istup[2] << " " << pup[2][0] << " " << pup[2][1] << " " << pup[2][2] << std::endl;
			std::cout << "pup[2][2]: " << pup[2][2] << std::endl;
			break;
		}
		*/
		
		// check if mother is the same
		bool takeEvent = true;

		if (takeEvent){
			TLorentzVector l1_minus, l1_plus, l2_minus, l2_plus;
			/*
			 l1_plus = new TLorentzVector(pup[2][0], pup[2][1], pup[2][2], pup[2][3]);
			 l1_minus = new TLorentzVector(pup[3][0], pup[3][1], pup[3][2], pup[3][3]);
			 l2_plus = new TLorentzVector(pup[4][0], pup[4][1], pup[4][2], pup[4][3]);
			 l2_minus = new TLorentzVector(pup[5][0], pup[5][1], pup[5][2], pup[5][3]);
			 */
			
			if (mothup[0][0] == mothup[1][0]){
				l1_minus = new TLorentzVector(pup[0][0], pup[0][1], pup[0][2], pup[0][3]);
				l1_plus = new TLorentzVector(pup[1][0], pup[1][1], pup[1][2], pup[1][3]);
				if (idup[2] < 0){
					l2_minus = new TLorentzVector(pup[2][0], pup[2][1], pup[2][2], pup[2][3]);
					l2_plus = new TLorentzVector(pup[3][0], pup[3][1], pup[3][2], pup[3][3]);		
				}
				else {
					l2_plus = new TLorentzVector(pup[2][0], pup[2][1], pup[2][2], pup[2][3]);
					l2_minus = new TLorentzVector(pup[3][0], pup[3][1], pup[3][2], pup[3][3]);						
				}
			}
			else if (mothup[0][0] == mothup[2][0]){
				l1_minus = new TLorentzVector(pup[0][0], pup[0][1], pup[0][2], pup[0][3]);
				l1_plus = new TLorentzVector(pup[2][0], pup[2][1], pup[2][2], pup[2][3]);
				if (idup[1] < 0){
					l2_minus = new TLorentzVector(pup[1][0], pup[1][1], pup[1][2], pup[1][3]);
					l2_plus = new TLorentzVector(pup[3][0], pup[3][1], pup[3][2], pup[3][3]);		
				}
				else {
					l2_plus = new TLorentzVector(pup[1][0], pup[1][1], pup[1][2], pup[1][3]);
					l2_minus = new TLorentzVector(pup[3][0], pup[3][1], pup[3][2], pup[3][3]);			
				}
			}
			else if (mothup[0][0] == mothup[3][0]){
				l1_minus = new TLorentzVector(pup[0][0], pup[0][1], pup[0][2], pup[0][3]);
				l1_plus = new TLorentzVector(pup[3][0], pup[3][1], pup[3][2], pup[3][3]);
				if (idup[1] < 0){
					l2_minus = new TLorentzVector(pup[1][0], pup[1][1], pup[1][2], pup[1][3]);
					l2_plus = new TLorentzVector(pup[2][0], pup[2][1], pup[2][2], pup[2][3]);		
				}
				else {
					l2_plus = new TLorentzVector(pup[1][0], pup[1][1], pup[1][2], pup[1][3]);
					l2_minus = new TLorentzVector(pup[2][0], pup[2][1], pup[2][2], pup[2][3]);		
				}				
			}
			
			
			//std::cout << "l1m: " << l1_minus.E() << std::endl;
			
			TLorentzVector Z1 = l1_minus+l1_plus;
			TLorentzVector Z2 = l2_minus+l2_plus;
			TLorentzVector Graviton = Z1+Z2;
			
			const double PDGZmass = 91.2;
			TLorentzVector pZ1; TLorentzVector pl1_m; TLorentzVector pl1_p;
			TLorentzVector pZ2; TLorentzVector pl2_m; TLorentzVector pl2_p;
            
            ///*
			if ( fabs(PDGZmass-Z1.M()) > fabs(PDGZmass-Z2.M()) ){				
			//if ( false ){				
				pZ1 = Z2; pl1_m = l2_minus; pl1_p = l2_plus;
				pZ2 = Z1; pl2_m = l1_minus; pl2_p = l1_plus;
			}
			else {
				pZ1 = Z1; pl1_m = l1_minus; pl1_p = l1_plus;
				pZ2 = Z2; pl2_m = l2_minus; pl2_p = l2_plus;
			}
			//*/
			
			double angle_costheta1, angle_costheta2, angle_phi, angle_costhetastar, angle_phistar1, angle_phistar2, angle_phistar12, angle_phi1, angle_phi2;
			//calculateAngles( Graviton, Z1, l1_minus, l1_plus, Z2, l2_minus, l2_plus, angle_costheta1, angle_costheta2, angle_phi, angle_costhetastar, angle_phistar1, angle_phistar2, angle_phistar12, angle_phi1, angle_phi2);
			calculateAngles( Graviton, pZ1, pl1_m, pl1_p, pZ2, pl2_m, pl2_p, angle_costheta1, angle_costheta2, angle_phi, angle_costhetastar, angle_phistar1, angle_phistar2, angle_phistar12, angle_phi1, angle_phi2);
						
			m_costheta1 = angle_costheta1;
			m_costheta2 = angle_costheta2;
			m_phi = angle_phi;
			m_costhetastar = angle_costhetastar;
			m_phistar1 = angle_phistar1;
			m_phistar2 = angle_phistar2;
			m_phistar12 = angle_phistar12;
			m_phi1 = angle_phi1;
			m_phi2 = angle_phi2;
			
			m_zzmass = Graviton.M();
			m_z1mass = pZ1.M();
			m_z2mass = pZ2.M();
			
			m_l1minus_pT = pl1_m.Pt();
			m_l1plus_pT = pl1_p.Pt();
			m_l2minus_pT = pl2_m.Pt();
			m_l2plus_pT = pl2_p.Pt();
			
			tree->Fill();
		}
		
		// counter
		ctr++;
		if (ctr%1000 == 0) std::cout << "event number: " << ctr << std::endl;
		if (ctr == maxEvents) break;
	}
	
	fout.cd();
	tree->Write();
	fout.Close();
	
}

void calculateAngles(TLorentzVector thep4H, TLorentzVector thep4Z1, TLorentzVector thep4M11, TLorentzVector thep4M12, TLorentzVector thep4Z2, TLorentzVector thep4M21, TLorentzVector thep4M22, double& costheta1, double& costheta2, double& phi, double& costhetastar, double& phistar1, double& phistar2, double& phistar12, double& phi1, double& phi2){
	
	
	//std::cout << "In calculate angles..." << std::endl;
	
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
	
	///////////////////////////////////////////////
	// check for z1/z2 convention, redefine all 4 vectors with convention
	///////////////////////////////////////////////	
	TLorentzVector p4H, p4Z1, p4M11, p4M12, p4Z2, p4M21, p4M22;
	p4H = thep4H;
	if ((phi1 < 0)&&(phi1 >= -TMath::Pi())){
		p4Z1 = thep4Z2; p4M11 = thep4M21; p4M12 = thep4M22;
		p4Z2 = thep4Z1; p4M21 = thep4M11; p4M22 = thep4M12;		
		costhetastar = theZ2X_p3.CosTheta();
	}
	else{
		p4Z1 = thep4Z1; p4M11 = thep4M11; p4M12 = thep4M12;
		p4Z2 = thep4Z2; p4M21 = thep4M21; p4M22 = thep4M22;
		costhetastar = theZ1X_p3.CosTheta();
	}
	
	
	//std::cout << "phi1: " << phi1 << ", phi2: " << phi2 << std::endl;
	
	// now helicity angles................................
	// ...................................................
	TVector3 boostZ1 = -(p4Z1.BoostVector());
	TLorentzVector p4Z2Z1(p4Z2);
	p4Z2Z1.Boost(boostZ1);
	//find the decay axis
	/////TVector3 unitx_1 = -Hep3Vector(p4Z2Z1);
	TVector3 unitx_1( -p4Z2Z1.X(), -p4Z2Z1.Y(), -p4Z2Z1.Z() );
	norm = 1/(unitx_1.Mag());
	unitx_1*=norm;
	//boost daughters of z2
	TLorentzVector p4M21Z1(p4M21);
	TLorentzVector p4M22Z1(p4M22);
	p4M21Z1.Boost(boostZ1);
	p4M22Z1.Boost(boostZ1);
	//create z and y axes
	/////TVector3 unitz_1 = Hep3Vector(p4M21Z1).cross(Hep3Vector(p4M22Z1));
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
	//std::cout << "theta1: " << M11_Z1frame.Theta() << std::endl;
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
	
	///////-----------------new way of calculating phi-----------------///////
	//double phi_n =  n_p4M21inXFrame_unitprime.Phi();
	/*
	 std::cout << "---------------------------" << std::endl;
	 std::cout << "phi: " << phi << std::endl;
	 std::cout << "phi_n: " << phi_n << std::endl;
	 std::cout << "phi + phi_n: " << (phi+phi_n) << std::endl;
	 */
	/// and then calculate phistar1
	TVector3 n_p4PartoninXFrame_unit( 0.0, 0.0, 1.0 );
	TVector3 n_p4PartoninXFrame_unitprime( n_p4PartoninXFrame_unit.Dot(n_unitx_1), n_p4PartoninXFrame_unit.Dot(n_unity_1), n_p4PartoninXFrame_unit.Dot(n_unitz_1) );
	// negative sign is for arrow convention in paper
	phistar1 = (n_p4PartoninXFrame_unitprime.Phi());
	
	// and the calculate phistar2
	TLorentzVector n_p4Z2inXFrame( p4Z2 );
	n_p4Z2inXFrame.Boost( boostX );
	TVector3 n_p4Z2inXFrame_unit = n_p4Z2inXFrame.Vect().Unit();
	///////TLorentzVector n_p4M21inXFrame( p4M21 );
	//////n_p4M21inXFrame.Boost( boostX );        
	////TVector3 n_p4M21inXFrame_unit = n_p4M21inXFrame.Vect().Unit();  
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
	
	/*
	 //// let's try doing it by normals
	 TVector3 crossedProdPlaneNormal = n_p4Z2inXFrame_unit.Cross( n_p4PartoninXFrame_unit );
	 TLorentzVector n_p4M22inXFrame( p4M22 );
	 n_p4M22inXFrame.Boost( boostX );
	 TVector3 n_p4M22inXFrame_unit = n_p4M22inXFrame.Vect().Unit();
	 TVector3 crossedZ2PlaneNormal = n_p4M21inXFrame_unit.Cross( n_p4M22inXFrame_unit );
	 double phistar2prime = acos(crossedProdPlaneNormal.Dot(crossedZ2PlaneNormal)/crossedProdPlaneNormal.Mag()/crossedZ2PlaneNormal.Mag());
	 
	 std::cout << "phistar2: " << phistar2 << ", phistar2prime: " << phistar2prime << std::endl;
	 //*/
	
	//std::cout << "phi: " << phi << ", phi_n: " << phi_n << ", phistar1: " << phistar1 << ", phistar2: " << phistar2 << ", 2-1: " << (phistar2-phistar1) << std::endl;
}






/*
{
	
	
	//std::cout << "In calculate angles..." << std::endl;
	
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
	
	///////////////////////////////////////////////
	// check for z1/z2 convention, redefine all 4 vectors with convention
	///////////////////////////////////////////////	
	TLorentzVector p4H, p4Z1, p4M11, p4M12, p4Z2, p4M21, p4M22;
	p4H = thep4H;
	if ((phi1 < 0)&&(phi1 >= -TMath::Pi())){
		p4Z1 = thep4Z2; p4M11 = thep4M21; p4M12 = thep4M22;
		p4Z2 = thep4Z1; p4M21 = thep4M11; p4M22 = thep4M12;		
		costhetastar = theZ2X_p3.CosTheta();
	}
	else{
		p4Z1 = thep4Z1; p4M11 = thep4M11; p4M12 = thep4M12;
		p4Z2 = thep4Z2; p4M21 = thep4M21; p4M22 = thep4M22;
		costhetastar = theZ1X_p3.CosTheta();
	}
	
	
	//std::cout << "phi1: " << phi1 << ", phi2: " << phi2 << std::endl;
	
	// now helicity angles................................
	// ...................................................
	TVector3 boostZ1 = -(p4Z1.BoostVector());
	TLorentzVector p4Z2Z1(p4Z2);
	p4Z2Z1.Boost(boostZ1);
	//find the decay axis
	/////TVector3 unitx_1 = -Hep3Vector(p4Z2Z1);
	TVector3 unitx_1( -p4Z2Z1.X(), -p4Z2Z1.Y(), -p4Z2Z1.Z() );
	norm = 1/(unitx_1.Mag());
	unitx_1*=norm;
	//boost daughters of z2
	TLorentzVector p4M21Z1(p4M21);
	TLorentzVector p4M22Z1(p4M22);
	p4M21Z1.Boost(boostZ1);
	p4M22Z1.Boost(boostZ1);
	//create z and y axes
	/////TVector3 unitz_1 = Hep3Vector(p4M21Z1).cross(Hep3Vector(p4M22Z1));
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
	//std::cout << "theta1: " << M11_Z1frame.Theta() << std::endl;
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
	TVector3 n_unity_1 = n_p4M11inXFrame_unit.Cross( n_unitz_1 );
	/////TVector3 n_unity_1 = n_unitz_1.Cross( n_p4M11inXFrame_unit );
	TVector3 n_unitx_1 = n_unity_1.Cross( n_unitz_1 );
	
	TLorentzVector n_p4M21inXFrame( p4M21 );
	n_p4M21inXFrame.Boost( boostX );
	TVector3 n_p4M21inXFrame_unit = n_p4M21inXFrame.Vect().Unit();
	//rotate into other plane
	TVector3 n_p4M21inXFrame_unitprime( n_p4M21inXFrame_unit.Dot(n_unitx_1), n_p4M21inXFrame_unit.Dot(n_unity_1), n_p4M21inXFrame_unit.Dot(n_unitz_1) );
	
	///////-----------------new way of calculating phi-----------------///////
	//double phi_n =  n_p4M21inXFrame_unitprime.Phi();
	/*
	 std::cout << "---------------------------" << std::endl;
	 std::cout << "phi: " << phi << std::endl;
	 std::cout << "phi_n: " << phi_n << std::endl;
	 std::cout << "phi + phi_n: " << (phi+phi_n) << std::endl;
	 
	/// and then calculate phistar1
	TVector3 n_p4PartoninXFrame_unit( 0.0, 0.0, 1.0 );
	TVector3 n_p4PartoninXFrame_unitprime( n_p4PartoninXFrame_unit.Dot(n_unitx_1), n_p4PartoninXFrame_unit.Dot(n_unity_1), n_p4PartoninXFrame_unit.Dot(n_unitz_1) );
	phistar1 = n_p4PartoninXFrame_unitprime.Phi();
	
	// and the calculate phistar2
	TLorentzVector n_p4Z2inXFrame( p4Z2 );
	n_p4Z2inXFrame.Boost( boostX );
	TVector3 n_p4Z2inXFrame_unit = n_p4Z2inXFrame.Vect().Unit();
	///////TLorentzVector n_p4M21inXFrame( p4M21 );
	//////n_p4M21inXFrame.Boost( boostX );        
	////TVector3 n_p4M21inXFrame_unit = n_p4M21inXFrame.Vect().Unit();  
	TVector3 n_unitz_2( n_p4Z2inXFrame_unit );
	//// y-axis is defined by neg lepton cross z-axis
	//// the subtle part is here...
	TVector3 n_unity_2 = n_p4M21inXFrame_unit.Cross( n_unitz_2 );
	TVector3 n_unitx_2 = n_unity_2.Cross( n_unitz_2 );
	TVector3 n_p4PartoninZ2PlaneFrame_unitprime( n_p4PartoninXFrame_unit.Dot(n_unitx_2), n_p4PartoninXFrame_unit.Dot(n_unity_2), n_p4PartoninXFrame_unit.Dot(n_unitz_2) );
	phistar2 = n_p4PartoninZ2PlaneFrame_unitprime.Phi();
	
	double phistar12_0 = phistar1 + phistar2;
	if (phistar12_0 > TMath::Pi()) phistar12 = phistar12_0 - 2*TMath::Pi();
	else if (phistar12_0 < (-1.)*TMath::Pi()) phistar12 = phistar12_0 + 2*TMath::Pi();
	else phistar12 = phistar12_0;
	
	/*
	 //// let's try doing it by normals
	 TVector3 crossedProdPlaneNormal = n_p4Z2inXFrame_unit.Cross( n_p4PartoninXFrame_unit );
	 TLorentzVector n_p4M22inXFrame( p4M22 );
	 n_p4M22inXFrame.Boost( boostX );
	 TVector3 n_p4M22inXFrame_unit = n_p4M22inXFrame.Vect().Unit();
	 TVector3 crossedZ2PlaneNormal = n_p4M21inXFrame_unit.Cross( n_p4M22inXFrame_unit );
	 double phistar2prime = acos(crossedProdPlaneNormal.Dot(crossedZ2PlaneNormal)/crossedProdPlaneNormal.Mag()/crossedZ2PlaneNormal.Mag());
	 
	 std::cout << "phistar2: " << phistar2 << ", phistar2prime: " << phistar2prime << std::endl;
	 //
	
}


*/


