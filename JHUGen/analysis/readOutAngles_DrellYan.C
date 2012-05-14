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
#include<math.h>

using namespace std;

double CM_ENERGY=0;

void calCSVariables( TLorentzVector& mu, TLorentzVector& mubar, double& costheta, double& sin2theta, double& tanphi, double& phi, bool swap);

void readOutAnglesPy(){
	
	//--------------------------------------------------------------------
	ifstream fin;
	fin.open("PythiaData_v1/Z_Zg_1M_LHC.txt");
	int startingEvent = 1;
	int maxEvents = 5000;
	
	//TFile fout("dataJHU_v10/fPMDominated_v3_newAnglesD.root", "RECREATE");
	TFile fout("PythiaRootFiles_v1_wreco/Z_Zg_1M_LHC.root", "RECREATE");
	TTree* tree = new TTree("angles", "angles");
	
	int i_process = 1;
	CM_ENERGY = 1000.;
	bool bool_Tevatron = false;
	//---------------------------------------------------------------------
	
	double m_Mll;
	double m_costheta, m_costheta_meas, m_phi, m_phi_meas;
	double m_yZ, m_zpT;
	int m_process, m_p1id, m_p2id, m_l_id, m_lbar_id;
	double m_p1_px, m_p1_py, m_p1_pz, m_p1_E;
	double m_p2_px, m_p2_py, m_p2_pz, m_p2_E;
	double m_l_px, m_l_py, m_l_pz, m_l_E;
	double m_lbar_px, m_lbar_py, m_lbar_pz, m_lbar_E;
	double m_mistag;
	//moments
	double m_m0, m_m1, m_m2, m_m3, m_m4, m_m5, m_m6, m_m7;
	
	tree->Branch("Mll", &m_Mll, "Mll/D");
	tree->Branch("costheta", &m_costheta, "costheta/D");
	tree->Branch("phi", &m_phi, "phi/D");
	tree->Branch("costheta_meas", &m_costheta_meas, "costheta_meas/D");
	tree->Branch("phi_meas", &m_phi_meas, "phi_meas/D");
	tree->Branch("yZ", &m_yZ, "yZ/D");
	tree->Branch("zpT", &m_zpT, "zpT/D");
	
	tree->Branch("process", &m_process, "process/I");
	tree->Branch("p1id", &m_p1id, "p1id/I");
	tree->Branch("p2id", &m_p2id, "p2id/I");
	
	tree->Branch("p1_px", &m_p1_px, "p1_px/D");
	tree->Branch("p1_py", &m_p1_py, "p1_py/D");
	tree->Branch("p1_pz", &m_p1_pz, "p1_pz/D");
	tree->Branch("p1_E", &m_p1_E, "p1_E/D");
	tree->Branch("p2_px", &m_p2_px, "p2_px/D");
	tree->Branch("p2_py", &m_p2_py, "p2_py/D");
	tree->Branch("p2_pz", &m_p2_pz, "p2_pz/D");
	tree->Branch("p2_E", &m_p2_E, "p2_E/D");
	
	tree->Branch("l_px", &m_l_px, "l_px/D");
	tree->Branch("l_py", &m_l_py, "l_py/D");
	tree->Branch("l_pz", &m_l_pz, "l_pz/D");
	tree->Branch("l_E", &m_l_E, "l_E/D");
	tree->Branch("lbar_px", &m_lbar_px, "lbar_px/D");
	tree->Branch("lbar_py", &m_lbar_py, "lbar_py/D");
	tree->Branch("lbar_pz", &m_lbar_pz, "lbar_pz/D");
	tree->Branch("lbar_E", &m_lbar_E, "lbar_E/D");
	
	// 0 if no mistag, 1 if mistag ... for dilution plot
	tree->Branch("mistag", &m_mistag, "mistag/D");
	
	tree->Branch("m0", &m_m0, "m_m0/D");
	tree->Branch("m1", &m_m1, "m_m1/D");
	tree->Branch("m2", &m_m2, "m_m2/D");
	tree->Branch("m3", &m_m3, "m_m3/D");
	tree->Branch("m4", &m_m4, "m_m4/D");
	tree->Branch("m5", &m_m5, "m_m5/D");
	tree->Branch("m6", &m_m6, "m_m6/D");
	tree->Branch("m7", &m_m7, "m_m7/D");
	
	// after smearing
	double m_l_px_reco, m_l_py_reco, m_l_pz_reco, m_l_E_reco, m_l_eta_reco;
	double m_lbar_px_reco, m_lbar_py_reco, m_lbar_pz_reco, m_lbar_E_reco, m_lbar_eta_reco;
	double m_Mll_reco, m_yZ_reco, m_zpT_reco, m_phi_reco, m_costheta_reco;
	
	tree->Branch("l_px_reco", &m_l_px_reco, "l_px_reco/D");
	tree->Branch("l_py_reco", &m_l_py_reco, "l_py_reco/D");
	tree->Branch("l_pz_reco", &m_l_pz_reco, "l_pz_reco/D");
	tree->Branch("l_E_reco", &m_l_E_reco, "l_E_reco/D");
	tree->Branch("l_eta_reco", &m_l_eta_reco, "l_eta_reco/D");
	tree->Branch("lbar_px_reco", &m_lbar_px_reco, "lbar_px_reco/D");
	tree->Branch("lbar_py_reco", &m_lbar_py_reco, "lbar_py_reco/D");
	tree->Branch("lbar_pz_reco", &m_lbar_pz_reco, "lbar_pz_reco/D");
	tree->Branch("lbar_E_reco", &m_lbar_E_reco, "lbar_E_reco/D");
	tree->Branch("lbar_eta_reco", &m_lbar_eta_reco, "lbar_eta_reco/D");
	
	tree->Branch("Mll_reco", &m_Mll_reco, "Mll_reco/D");
	tree->Branch("yZ_reco", &m_yZ_reco, "yZ_reco/D");
	tree->Branch("zpT_reco", &m_zpT_reco, "zpT_reco/D");
	tree->Branch("costheta_reco", &m_costheta_reco, "costheta_reco/D");
	tree->Branch("phi_reco", &m_phi_reco, "phi_reco/D");
	
	
	int ctr = 0;
	int iFile = 0;
	while (!fin.eof() && fin.good()){
		
		ctr++;
		if (ctr%1000 == 0) std::cout << "event: " << ctr << std::endl;
		if (ctr > maxEvents) break;		
		
		if (ctr > startingEvent){
			std::vector <double> listOfMom;
			
			// output momentums
			TLorentzVector parton1, parton2;
			TLorentzVector lep, lepbar;
			int parton1id, parton2id, lid, lbarid;
			
			// parton information
			for (int a = 0; a < 4; a++){
				
				int idup;
				double pup[5];
				
				fin >> idup;
				
				for (int i = 0; i < 4; i++)
				{
					fin >> pup[i];
				}			
				
				//std::cout << idup << " " << istup << " " << mothup[0] << " " << mothup[1];
				//std::cout << " " << pup[0] << " " << pup[1] << " " << pup[2] << " " << pup[3] << " " << pup[4] << std::endl;
				
				if (a == 0){
					parton1 = new TLorentzVector(pup[0], pup[1], pup[2], pup[3]);
					parton1id = idup;
				}
				if (a == 1){
					parton2 = new TLorentzVector(pup[0], pup[1], pup[2], pup[3]);
					parton2id = idup;
				}
				if ((idup > 0)&&(a>1)){
					lep = new TLorentzVector(pup[0], pup[1], pup[2], pup[3]);
					lid = idup;
				}
				if ((idup < 0)&&(a>1)){
					lepbar = new TLorentzVector(pup[0], pup[1], pup[2], pup[3]);
					lbarid = idup;
				}
				
			}
			
			TLorentzVector mll = lep+lepbar;
			//std::cout << "mll: " << mll.Px() << ", " << mll.Py() << ", " << mll.Pz() << ", pT: " << mll.Pt() << std::endl;
			m_Mll = mll.M();
			m_zpT = mll.Pt();
			//m_yZ = mll.Eta();
			
			double qplus = (1/sqrt(2.))*(mll.E() + mll.Pz());
			double qminus = (1/sqrt(2.))*(mll.E() - mll.Pz());
			m_yZ = 0.5*log(qplus/qminus);
			
			///*
			m_process = i_process;
			
			m_p1id = parton1id;
			m_p2id = parton2id;
			m_p1_px = parton1.Px();
			m_p1_py = parton1.Py();
			m_p1_pz = parton1.Pz();
			m_p1_E = parton1.E();
			m_p2_px = parton2.Px();
			m_p2_py = parton2.Py();
			m_p2_pz = parton2.Pz();
			m_p2_E = parton2.E();
			
			m_l_id = lid; 
			m_lbar_id = lbarid;
			m_l_px = lep.Px();
			m_l_py = lep.Py();
			m_l_pz = lep.Pz();
			m_l_E = lep.E();
			m_lbar_px = lepbar.Px();
			m_lbar_py = lepbar.Py();
			m_lbar_pz = lepbar.Pz();
			m_lbar_E = lepbar.E();
			
			
			
			bool zAxisNeg = false;
			// find the direction of the quark...
			// what to do in the case of qg? direction of quark (antiquark) is the positive (negative) Z direction
			
			// if this is the tevatron, all of this is moot
			if (bool_Tevatron){
				zAxisNeg = false;
			}
			else{
				// qg process
				if ((m_p1id > 20)||(m_p2id > 20)) {
					// p1 is the (anti-)quark
					if (abs(m_p1id) < 20){
						if ((abs(m_p1id) > 0)&&(m_p1_pz > 0.)){ zAxisNeg = false; }
						if ((abs(m_p1id) > 0)&&(m_p1_pz < 0.)){ zAxisNeg = true; }
						if ((abs(m_p1id) < 0)&&(m_p1_pz > 0.)){ zAxisNeg = true; }
						if ((abs(m_p1id) < 0)&&(m_p1_pz < 0.)){ zAxisNeg = false; }
					}
					else if (abs(m_p2id) < 20){
						if ((abs(m_p2id) > 0)&&(m_p2_pz > 0.)){ zAxisNeg = false; }
						if ((abs(m_p2id) > 0)&&(m_p2_pz < 0.)){ zAxisNeg = true; }
						if ((abs(m_p2id) < 0)&&(m_p2_pz > 0.)){ zAxisNeg = true; }
						if ((abs(m_p2id) < 0)&&(m_p2_pz < 0.)){ zAxisNeg = false; }
					}	
					else {
						std::cout << "disaster!" << std::endl;
					}
				}
				// qqbar process
				else {
					if ((m_p1id > 0)&&(m_p1_pz > 0.)) { zAxisNeg = false; }
					if ((m_p1id > 0)&&(m_p1_pz < 0.)) { zAxisNeg = true; }
					if ((m_p1id < 0)&&(m_p1_pz > 0.)) { zAxisNeg = true; }
					if ((m_p1id < 0)&&(m_p1_pz < 0.)) { zAxisNeg = false; }
				}
			}
			
			// true value (undiluted)
			double angle_costheta_t, angle_sin2theta_t, angle_tanphi_t, angle_phi_t;
			calCSVariables(lep, lepbar, angle_costheta_t, angle_sin2theta_t, angle_tanphi_t, angle_phi_t, zAxisNeg);
			
			// measured value (diluted)
			double angle_costheta_m, angle_sin2theta_m, angle_tanphi_m, angle_phi_m;
			bool YdirectionFlip = false;
			if ((m_yZ < 0.)&&(!bool_Tevatron)) { YdirectionFlip = true; }
			calCSVariables(lep, lepbar, angle_costheta_m, angle_sin2theta_m, angle_tanphi_m, angle_phi_m, YdirectionFlip);
			
			// reco part
			TLorentzVector l_gen( m_l_px, m_l_py, m_l_pz, m_l_E );
			TLorentzVector lbar_gen( m_lbar_px, m_lbar_py, m_lbar_pz, m_lbar_E );
			
			double l_Perp = l_gen.Perp()+(gRandom->Gaus(0,0.025)*l_gen.Perp())+(gRandom->Gaus(0,0.0001)*l_gen.Perp()*l_gen.Perp());
			double l_Theta = l_gen.Theta()+(gRandom->Gaus(0,0.001));
			double l_Phi = l_gen.Phi()+(gRandom->Gaus(0,0.001));
			double lbar_Perp = lbar_gen.Perp()+(gRandom->Gaus(0,0.025)*lbar_gen.Perp())+(gRandom->Gaus(0,0.0001)*lbar_gen.Perp()*lbar_gen.Perp());
			double lbar_Theta = lbar_gen.Theta()+(gRandom->Gaus(0,0.001));
			double lbar_Phi = lbar_gen.Phi()+(gRandom->Gaus(0,0.001));
			
			double l_Px = l_Perp*cos(l_Phi);
			double l_Py = l_Perp*sin(l_Phi);
			double l_Pz = l_Perp/tan(l_Theta);
			double l_E = sqrt(l_Px*l_Px+l_Py*l_Py+l_Pz*l_Pz);
			double lbar_Px = lbar_Perp*cos(lbar_Phi);
			double lbar_Py = lbar_Perp*sin(lbar_Phi);
			double lbar_Pz = lbar_Perp/tan(lbar_Theta);
			double lbar_E = sqrt(lbar_Px*lbar_Px+lbar_Py*lbar_Py+lbar_Pz*lbar_Pz);
			
			TLorentzVector l_reco( l_Px, l_Py, l_Pz, l_E );
			TLorentzVector lbar_reco( lbar_Px, lbar_Py, lbar_Pz, lbar_E );
			TLorentzVector mll_reco = l_reco+lbar_reco;
			
			m_Mll_reco = mll_reco.M();
			m_zpT_reco = mll_reco.Pt();
			double qplus = (1/sqrt(2.))*(mll_reco.E() + mll_reco.Pz());
			double qminus = (1/sqrt(2.))*(mll_reco.E() - mll_reco.Pz());
			m_yZ_reco = 0.5*log(qplus/qminus);
			
			m_l_px_reco = l_reco.Px();
			m_l_py_reco = l_reco.Py();
			m_l_pz_reco = l_reco.Pz();
			m_l_E_reco = l_reco.E();
			m_l_eta_reco = l_reco.Eta();
			m_lbar_px_reco = lbar_reco.Px();
			m_lbar_py_reco = lbar_reco.Py();
			m_lbar_pz_reco = lbar_reco.Pz();
			m_lbar_E_reco = lbar_reco.E();
			m_lbar_eta_reco = lbar_reco.Eta();
			
			// measured reconstructed value (reco)
			double angle_costheta_r, angle_sin2theta_r, angle_tanphi_r, angle_phi_r;
			bool YdirectionFlipReco = false;
			if ((m_yZ_reco < 0.)&&(!bool_Tevatron)) { YdirectionFlipReco = true; }
			calCSVariables(l_reco, lbar_reco, angle_costheta_r, angle_sin2theta_r, angle_tanphi_r, angle_phi_r, YdirectionFlipReco);
			
			m_costheta_reco = angle_costheta_r;
			m_phi_reco = angle_phi_r;
			
			
			// mistag
			if ( zAxisNeg && YdirectionFlip ) { m_mistag = 0.; }
			if ( (!zAxisNeg) && (!YdirectionFlip) ) { m_mistag = 0.; }
			if ( (!zAxisNeg) && YdirectionFlip ) { m_mistag = 1.; }
			if ( zAxisNeg && (!YdirectionFlip) ) { m_mistag = 1.; }
			
			m_costheta = angle_costheta_t;
			m_costheta_meas = angle_costheta_m;
			m_phi = angle_phi_t;
			m_phi_meas = angle_phi_m;
			
			if (angle_phi_m < -100.){
				m_m0 = (1./2.)*(1.-3.*pow(angle_costheta_m,2));
				m_m1 = -999.;
				m_m2 = -999.;
				m_m3 = -999.;
				m_m4 = angle_costheta_m;
				m_m5 = -999.;
				m_m6 = -999.;
				m_m7 = -999.;
			}
			else{
				//moments
				double theta_m = TMath::ACos(angle_costheta_m);
				m_m0 = (1./2.)*(1.-3.*pow(angle_costheta_m,2));
				//m_m1 = angle_sin2theta*cos(angle_phi);
				m_m1 = sin(2.*theta_m)*cos(angle_phi_m);
				m_m2 = sin(theta_m)*sin(theta_m)*cos(2.*angle_phi_m);
				m_m3 = sin(theta_m)*cos(angle_phi_m);
				m_m4 = angle_costheta_m;
				m_m5 = sin(theta_m)*sin(theta_m)*sin(2.*angle_phi_m);
				m_m6 = sin(2.*theta_m)*sin(angle_phi_m);
				m_m7 = sqrt(theta_m)*sin(angle_phi_m); 
			}
			
			tree->Fill();
			
		}
	}
	
	fout.cd();
	tree->Write();
	fout.Close();
	
}

void calCSVariables( TLorentzVector& mu, TLorentzVector& mubar, double& costheta, double& sin2theta, double& tanphi, double& phi, bool swap) {
	
	// convention. beam direction is on the positive Z direction.
	// beam contains quark flux.
	TLorentzVector Pbeam  (0, 0,  CM_ENERGY/2.0, CM_ENERGY/2.0);
	TLorentzVector Ptarget(0, 0, -CM_ENERGY/2.0, CM_ENERGY/2.0);
	
	TLorentzVector Q(mu+mubar);
	/************************************************************************
	 *
	 * 1) cos(theta) = 2 Q^-1 (Q^2+Qt^2)^-(1/2) (mu^+ mubar^- - mu^- mubar^+)
	 * 
	 *
	 ************************************************************************/ 
	double muplus  = 1.0/sqrt(2.0) * (mu.E() + mu.Z());
	double muminus = 1.0/sqrt(2.0) * (mu.E() - mu.Z());
	
	double mubarplus  = 1.0/sqrt(2.0) * (mubar.E() + mubar.Z());
	double mubarminus = 1.0/sqrt(2.0) * (mubar.E() - mubar.Z());
	
	//double costheta = 2.0 / Q.Mag() / sqrt(pow(Q.Mag(), 2) + pow(Q.Pt(), 2)) * (muplus * mubarminus - muminus * mubarplus);
	costheta = 2.0 / Q.Mag() / sqrt(pow(Q.Mag(), 2) + pow(Q.Pt(), 2)) * (muplus * mubarminus - muminus * mubarplus);
	if (swap) costheta = -costheta;
	
	/************************************************************************
	 *
	 * 2) sin2(theta) = Q^-2 Dt^2 - Q^-2 (Q^2 + Qt^2)^-1 * (Dt dot Qt)^2 
	 *
	 ************************************************************************/
	TLorentzVector D(mu-mubar);
	double dt_qt = D.X()*Q.X() + D.Y()*Q.Y();
	double sin2theta = pow(D.Pt()/Q.Mag(), 2) - 1.0/pow(Q.Mag(), 2)/(pow(Q.Mag(), 2) + pow(Q.Pt(), 2))*pow(dt_qt, 2);
	
	
	/************************************************************************
	 *
	 * 3) tanphi = (Q^2 + Qt^2)^1/2 / Q (Dt dot R unit) /(Dt dot Qt unit)
	 *
	 ************************************************************************/
	if (Q.Pt() == 0.){
		tanphi = 1e10;
		///phi = TMath::Pi()/2.;
		phi = -999.;
	}
	else{
		// unit vector on R direction
		TVector3 R = Pbeam.Vect().Cross(Q.Vect());
		TVector3 Runit = R.Unit();
		
		// unit vector on Qt
		TVector3 Qt = Q.Vect(); Qt.SetZ(0);
		TVector3 Qtunit = Qt.Unit();
		
		TVector3 Dt = D.Vect(); Dt.SetZ(0);
		double tanphi = sqrt(pow(Q.Mag(),2)+pow(Q.Pt(), 2))/Q.Mag()*Dt.Dot(Runit)/Dt.Dot(Qtunit);
		if (swap) tanphi = -tanphi;
		
		///double phi = TMath::ATan2(sqrt(pow(Q.Mag(),2)+pow(Q.Pt(),2))*Dt.Dot(Runit),Q.Mag()*Dt.Dot(Qtunit));
		phi = TMath::ATan2(sqrt(pow(Q.Mag(),2)+pow(Q.Pt(),2))*Dt.Dot(Runit),Q.Mag()*Dt.Dot(Qtunit));
		if (swap) phi = TMath::ATan2(sqrt(pow(Q.Mag(),2)+pow(Q.Pt(),2))*Dt.Dot(Runit),-1.*Q.Mag()*Dt.Dot(Qtunit));
	}
	/*
	 res[0] = costheta;
	 res[1] = sin2theta;
	 res[2] = tanphi;
	 res[3] = phi;
	 */
}


