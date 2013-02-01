# A class which takes histograms and plots them in a versatile way
# inputs are file names which can be "data" or "MC"

import ROOT
ROOT.gROOT.ProcessLine(".L ~/tdrstyle.C")
from ROOT import setTDRStyle
from ROOT import TTree
from ROOT import gROOT
ROOT.setTDRStyle()
ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetOptFit(0)

ROOT.TH1.SetDefaultSumw2()
ROOT.TH2.SetDefaultSumw2()

ROOT.gStyle.SetPadTopMargin(0.09);
ROOT.gStyle.SetPadLeftMargin(0.16);

import os
import sys

from array import array
import math
from optparse import OptionParser

from bsmReweighter import *


# FWLITE stuff
import sys
from DataFormats.FWLite import Events, Handle
ROOT.gSystem.Load('libCondFormatsJetMETObjects')
ROOT.gSystem.Load('libFWCoreFWLite');
ROOT.gSystem.Load('libFWCoreUtilities');  

### ------------ h e l p e r s --------------------

def getListRMS(list):
    mean = sum(list)/float(len(list));
    return math.sqrt(sum((n-mean)*(n-mean) for n in list)/len(list));

def getListMean(list):
    return sum(list)/float(len(list));

class sampleWrapperClass:

    ### ------------------------------------------------
    def __init__(self, label, file, channel, sampleEffLumi, lumi, treename, isData):

        
        self.IsData_ = isData;
        self.FileName_ = file;
        self.File_ = ROOT.TFile(file);
        self.InputTree_ = self.File_.Get(treename);
        
        self.SampleWeight_ = lumi/sampleEffLumi;
        
        self.JetPrefix_ = "GroomedJet_CA8";
        self.Label_ = label;
        self.Channel_ = channel
        self.OFileName_ = "trainingtrees_"+channel+"/ofile_"+label+".root";
    
        # initialization for doing BSM reweighting
        self.SignalMass_ = -1;
        if file.find("HWW") > 0 and file.find("600") > 0: self.SignalMass_ = 600;
        if file.find("HWW") > 0 and file.find("700") > 0: self.SignalMass_ = 700;
        if file.find("HWW") > 0 and file.find("800") > 0: self.SignalMass_ = 800;
        if file.find("HWW") > 0 and file.find("900") > 0: self.SignalMass_ = 900;    
        if file.find("HWW") > 0 and file.find("1000") > 0: self.SignalMass_ = 1000;   
        self.FitSMSignal = False;
        self.FitSMSignal_mean = -1;
        self.FitSMSignal_gamma = -1;
    
        # ---------- Set up jet corrections on the fly of R >= 0.7 jets
        fDir = "JECs/"      
        jecUncStr = ROOT.std.string(fDir + "GR_R_53_V10_Uncertainty_AK7PFchs.txt")
        self.jecUnc_ = ROOT.JetCorrectionUncertainty(jecUncStr)
            
    def createTrainingTree(self):
        
        print self.FileName_
        self.File_ = ROOT.TFile(self.FileName_);
        self.InputTree_ = self.File_.Get("WJet");
        self.NTree_ = self.InputTree_.GetEntries();
        
        print "Turning off branches...", self.FileName_

        # turn off unnecessary branches
        self.turnOffBranches();
        
        print "Initializing sample: ", self.FileName_
        print "Nentries = ", self.NTree_
        
        # fill histograms
        self.createBRDTree();
        self.File_.Close();

#    def createTTbarTree(self):
#        
#        print "Initializing sample: ", self.FileName_
#        print "Nentries = ", self.NTree_
#        
#        # fill histograms
#        self.fillHistograms(True);

    ### produce weights for alternative models
    def GetInteferenceWeights(self, mass, Cprime, BRnew=0):
        
        massin = self.SignalMass_;
        if massin < 0: return;
        
        massmin = {600:200,700:200,800:400,900:400,1000:400};
        massmax = {600:1200,700:1200,800:1500,900:1600,1000:1800};

        # read in original file and get lineshape 
        if not self.FitSMSignal: 
            fitSM = FitMassPoint(self.FileName_, massin, massmin[massin], massmax[massin]);
            self.FitSMSignal_mean = fitSM[0];
            self.FitSMSignal_gamma = fitSM[1];
            self.FitSMSignal = True;
    
        # create a weight for the given event after switch is turned
        weight_width = lineshapeWidthReweight(mass, self.FitSMSignal_mean, self.FitSMSignal_gamma, Cprime/(1.-BRnew), massmin[massin], massmax[massin]);
        weight_xs = Cprime*(1-BRnew);   
        return (weight_width*weight_xs);

    ### ------------------------------------------------
    def createBRDTree(self):

        #weight1_ = "weights/Wtagger_200to275_0to100_tau2tau1qjet_Likelihood.weights.xml"
        #weight2_ = "weights/Wtagger_275to500_0to100_tau2tau1qjet_Likelihood.weights.xml"
        #ungroomed_weight1_ = "weights/ungroomed_Wtagger_200to275_0to100_tau2tau1qjet_Likelihood.weights.xml"
        #ungroomed_weight2_ = "weights/ungroomed_Wtagger_275to500_0to100_tau2tau1qjet_Likelihood.weights.xml"
        reader1_ = ROOT.TMVA.Reader("!Color:!Silent")
        reader2_ = ROOT.TMVA.Reader("!Color:!Silent")
        ungroomed_reader1_ = ROOT.TMVA.Reader("!Color:!Silent")
        ungroomed_reader2_ = ROOT.TMVA.Reader("!Color:!Silent")

        fname = self.OFileName_;
        
        self.OFile_ = ROOT.TFile(fname,"RECREATE");        

        otree = ROOT.TTree("otree","otree");        
        
        mass_lvj_ = array( 'f', [ 0. ] );
        v_pt_ = array( 'f', [ 0. ] );
        jet_mass_pr_ = array( 'f', [ 0. ] );
        jet_pt_pr_ = array( 'f', [ 0. ] );
        ungroomed_jet_pt_ = array( 'f', [ 0. ] );
        j_jecfactor_up_ = array( 'f', [ 0. ] );
        j_jecfactor_dn_ = array( 'f', [ 0. ] );
        jet_mass_pr_up_ = array( 'f', [ 0. ] );
        jet_mass_pr_dn_ = array( 'f', [ 0. ] );

        isttbar_ = array( 'i', [ 0 ] );     
        issignal_ = array( 'i', [ 0 ] );             
        jet_mass_pr_ttbar_ = array( 'f', [ 0. ] );        
        jet_pt_ttbar_ = array( 'f', [ 0. ] );        
        tau2tau1_ttbar_ = array( 'f', [ 0. ] );                
        
        l_pt_ = array( 'f', [ 0. ] );
        l_eta_ = array( 'f', [ 0. ] );        
        mvaMET_ = array( 'f', [ 0. ] );                
        pfMET_ = array( 'f', [ 0. ] );                
        nPV_ = array( 'f', [ 0. ] );                        
        totalEventWeight_ = array( 'f', [ 0. ] );                                
        eff_and_pu_Weight_ = array( 'f', [ 0. ] );                                
        wSampleWeight_ = array( 'f', [ 0. ] ); #wSampleWeight*effwt*puwt                               
        interference_Weight_H600_ = array( 'f', [ 0. ] );                                
        interference_Weight_H700_ = array( 'f', [ 0. ] );                                
        interference_Weight_H800_ = array( 'f', [ 0. ] );                                
        interference_Weight_H900_ = array( 'f', [ 0. ] );                                
        interference_Weight_H1000_ = array( 'f', [ 0. ] );                                
        cps_Weight_H600_ = array( 'f', [ 0. ] );                                
        cps_Weight_H700_ = array( 'f', [ 0. ] );                                
        cps_Weight_H800_ = array( 'f', [ 0. ] );                                
        cps_Weight_H900_ = array( 'f', [ 0. ] );                                
        cps_Weight_H1000_ = array( 'f', [ 0. ] );                                
        
        jet_grsens_ft_ = array( 'f', [ 0. ] );
        jet_grsens_tr_ = array( 'f', [ 0. ] );
        jet_massdrop_pr_ = array( 'f', [ 0. ] );    
        jet_qjetvol_ = array( 'f', [ 0. ] ); 
        jet_tau2tau1_ = array( 'f', [ 0. ] );     
        jet_jetconstituents_ = array( 'f', [ 0. ] );     
        
        jet_rcore4_ = array( 'f', [ 0. ] );
        jet_rcore5_ = array( 'f', [ 0. ] );
        jet_rcore6_ = array( 'f', [ 0. ] );
        jet_rcore7_ = array( 'f', [ 0. ] );
        
        # n bjets
#        nbjets_ = array( 'f', [ 0. ] );
        nbjets_cvsl_ = array( 'f', [ 0. ] );
        nbjets_cvsm_ = array( 'f', [ 0. ] );
        nbjets_ssvhem_ = array( 'f', [ 0. ] );
        nbjets_csvl_veto_ = array( 'f', [ 0. ] );
        nbjets_csvm_veto_ = array( 'f', [ 0. ] );
        nbjets_ssvhem_veto_ = array( 'f', [ 0. ] );
        
        nbjetsCSV_ = array( 'f', [ 0. ] );
        nbjetsSSVHE_ = array( 'f', [ 0. ] );        
        njets_ = array( 'f', [ 0. ] );        
        jet_pt1frac_ = array( 'f', [ 0. ] );
        jet_pt2frac_ = array( 'f', [ 0. ] );
        jet_sjdr_ = array( 'f', [ 0. ] );       
        
        jet_planarlow04_ = array( 'f', [0.] );
        jet_planarlow05_ = array( 'f', [0.] );
        jet_planarlow06_ = array( 'f', [0.] );
        jet_planarlow07_ = array( 'f', [0.] );
        
        deltaR_lca8jet_ = array( 'f', [0.] );
        deltaphi_METca8jet_ = array( 'f', [0.] );
        deltaphi_Vca8jet_ = array( 'f', [0.] );

        ##TMVA Output
        #ca8wjettaggerpt200_275_ = array( 'f', [0.] )
        #ca8wjettaggerpt275_500_ = array( 'f', [0.] )

        #ungroomedwjettaggerpt200_275_ = array( 'f', [0.] )
        #ungroomedwjettaggerpt275_500_ = array( 'f', [0.] )
    
        otree.Branch("mass_lvj", mass_lvj_ , "mass_lvj/F");
        otree.Branch("v_pt", v_pt_ , "v_pt/F");
        otree.Branch("jet_pt_pr", jet_pt_pr_ , "jet_pt_pr/F");
        otree.Branch("ungroomed_jet_pt", ungroomed_jet_pt_, "ungroomed_jet_pt/F");
        otree.Branch("jet_mass_pr", jet_mass_pr_ , "jet_mass_pr/F");
        otree.Branch("j_jecfactor_up", j_jecfactor_up_ , "j_jecfactor_up/F");
        otree.Branch("j_jecfactor_dn", j_jecfactor_dn_ , "j_jecfactor_dn/F");        
        otree.Branch("jet_mass_pr_up", jet_mass_pr_up_ , "jet_mass_pr_up/F");
        otree.Branch("jet_mass_pr_dn", jet_mass_pr_dn_ , "jet_mass_pr_dn/F");

        otree.Branch("issignal", issignal_ , "issignal/I");        
        otree.Branch("isttbar", isttbar_ , "isttbar/I");        
        otree.Branch("jet_pt_ttbar", jet_pt_ttbar_ , "jet_pt_ttbar/F");        
        otree.Branch("tau2tau1_ttbar", tau2tau1_ttbar_ , "tau2tau1_ttbar/F");        
        otree.Branch("jet_mass_pr_ttbar", jet_mass_pr_ttbar_ , "jet_mass_pr_ttbar/F");        
        
        otree.Branch("l_pt", l_pt_ , "l_pt/F");
        otree.Branch("l_eta", l_eta_ , "l_eta/F");
        otree.Branch("mvaMET", mvaMET_ , "mvaMET/F");
        otree.Branch("pfMET", pfMET_ , "pfMET/F");        
        otree.Branch("nPV", nPV_ , "nPV/F");
        otree.Branch("totalEventWeight", totalEventWeight_ , "totalEventWeight/F");
        otree.Branch("eff_and_pu_Weight", eff_and_pu_Weight_ , "eff_and_pu_Weight/F");
        otree.Branch("wSampleWeight", wSampleWeight_ , "wSampleWeight/F");
        otree.Branch("interference_Weight_H600", interference_Weight_H600_ , "interference_Weight_H600/F");
        otree.Branch("interference_Weight_H700", interference_Weight_H700_ , "interference_Weight_H700/F");
        otree.Branch("interference_Weight_H800", interference_Weight_H800_ , "interference_Weight_H800/F");
        otree.Branch("interference_Weight_H900", interference_Weight_H900_ , "interference_Weight_H900/F");
        otree.Branch("interference_Weight_H1000", interference_Weight_H1000_ , "interference_Weight_H1000/F");
        otree.Branch("cps_Weight_H600", cps_Weight_H600_ , "cps_Weight_H600/F");
        otree.Branch("cps_Weight_H700", cps_Weight_H700_ , "cps_Weight_H700/F");
        otree.Branch("cps_Weight_H800", cps_Weight_H800_ , "cps_Weight_H800/F");
        otree.Branch("cps_Weight_H900", cps_Weight_H900_ , "cps_Weight_H900/F");
        otree.Branch("cps_Weight_H1000", cps_Weight_H1000_ , "cps_Weight_H1000/F");

        otree.Branch("jet_grsens_ft", jet_grsens_ft_ , "jet_grsens_ft/F");
        otree.Branch("jet_grsens_tr", jet_grsens_tr_ , "jet_grsens_tr/F");
        otree.Branch("jet_massdrop_pr", jet_massdrop_pr_ , "jet_massdrop_pr/F");
        otree.Branch("jet_qjetvol", jet_qjetvol_ , "jet_qjetvol/F");
        otree.Branch("jet_tau2tau1", jet_tau2tau1_ , "jet_tau2tau1/F");
        otree.Branch("jet_jetconstituents", jet_jetconstituents_ , "jet_jetconstituents/F");
        otree.Branch("jet_rcore4", jet_rcore4_ , "jet_rcore4/F");
        otree.Branch("jet_rcore5", jet_rcore5_ , "jet_rcore5/F");
        otree.Branch("jet_rcore6", jet_rcore6_ , "jet_rcore6/F");
        otree.Branch("jet_rcore7", jet_rcore7_ , "jet_rcore7/F");

#        otree.Branch("nbjets", nbjets_ , "nbjets/F");
        otree.Branch("nbjets_cvsl", nbjets_cvsl_ , "nbjets_cvsl/F");
        otree.Branch("nbjets_cvsm", nbjets_cvsm_ , "nbjets_cvsm/F");
        otree.Branch("nbjets_ssvhem", nbjets_ssvhem_ , "nbjets_ssvhem/F");
        otree.Branch("nbjets_csvl_veto", nbjets_csvl_veto_ , "nbjets_csvl_veto/F");
        otree.Branch("nbjets_csvm_veto", nbjets_csvm_veto_ , "nbjets_csvm_veto/F");        
        otree.Branch("nbjets_ssvhem_veto", nbjets_ssvhem_veto_ , "nbjets_ssvhem_veto/F");                
        otree.Branch("nbjetsCSV", nbjetsCSV_ , "nbjetsCSV_/F");
        otree.Branch("nbjetsSSVHE", nbjetsSSVHE_ , "nbjetsSSVHE_/F");        
        otree.Branch("njets", njets_ , "njets/F");
        otree.Branch("jet_pt1frac", jet_pt1frac_ , "jet_pt1frac/F");
        otree.Branch("jet_pt2frac", jet_pt2frac_ , "jet_pt2frac/F");
        otree.Branch("jet_sjdr", jet_sjdr_ , "jet_sjdr/F");
        
        otree.Branch("jet_planarflow04", jet_planarlow04_, "jet_planarflow04/F");
        otree.Branch("jet_planarflow05", jet_planarlow05_, "jet_planarflow05/F");
        otree.Branch("jet_planarflow06", jet_planarlow06_, "jet_planarflow06/F");
        otree.Branch("jet_planarflow07", jet_planarlow07_, "jet_planarflow07/F");
        
        otree.Branch("deltaR_lca8jet", deltaR_lca8jet_, "deltaR_lca8jet/F");
        otree.Branch("deltaphi_METca8jet", deltaphi_METca8jet_, "deltaphi_METca8jet/F");
        otree.Branch("deltaphi_Vca8jet", deltaphi_Vca8jet_, "deltaphi_Vca8jet/F");

        #otree.Branch("ca8wjettaggerpt200_275", ca8wjettaggerpt200_275_, "ca8wjettaggerpt200_275/F")
        #otree.Branch("ca8wjettaggerpt275_500", ca8wjettaggerpt275_500_, "ca8wjettaggerpt275_500/F")
        
        #otree.Branch("ungroomedwjettaggerpt200_275", ungroomedwjettaggerpt200_275_, "ungroomedwjettaggerpt200_275/F")
        #otree.Branch("ungroomedwjettaggerpt275_500", ungroomedwjettaggerpt275_500_, "ungroomedwjettaggerpt275_500/F")

        ##########################
        # variables for BSM reweighting
        genHMass_ = array( 'f', [ 0. ] );              
        bsmReweight_cPrime01_brNew00_ = array( 'f', [ 0. ] );      
        bsmReweight_cPrime02_brNew00_ = array( 'f', [ 0. ] );      
        bsmReweight_cPrime03_brNew00_ = array( 'f', [ 0. ] );      
        bsmReweight_cPrime04_brNew00_ = array( 'f', [ 0. ] );      
        bsmReweight_cPrime05_brNew00_ = array( 'f', [ 0. ] );      
        bsmReweight_cPrime07_brNew00_ = array( 'f', [ 0. ] );      
        bsmReweight_cPrime10_brNew00_ = array( 'f', [ 0. ] );              
        otree.Branch("genHMass", genHMass_ , "genHMass/F");        
        otree.Branch("bsmReweight_cPrime01_brNew00", bsmReweight_cPrime01_brNew00_ , "bsmReweight_cPrime01_brNew00/F");        
        otree.Branch("bsmReweight_cPrime02_brNew00", bsmReweight_cPrime02_brNew00_ , "bsmReweight_cPrime02_brNew00/F");        
        otree.Branch("bsmReweight_cPrime03_brNew00", bsmReweight_cPrime03_brNew00_ , "bsmReweight_cPrime03_brNew00/F");        
        otree.Branch("bsmReweight_cPrime04_brNew00", bsmReweight_cPrime04_brNew00_ , "bsmReweight_cPrime04_brNew00/F");        
        otree.Branch("bsmReweight_cPrime05_brNew00", bsmReweight_cPrime05_brNew00_ , "bsmReweight_cPrime05_brNew00/F");        
        otree.Branch("bsmReweight_cPrime07_brNew00", bsmReweight_cPrime07_brNew00_ , "bsmReweight_cPrime07_brNew00/F");        
        otree.Branch("bsmReweight_cPrime10_brNew00", bsmReweight_cPrime10_brNew00_ , "bsmReweight_cPrime10_brNew00/F");        
        ##########################
        prefix = self.JetPrefix_;
        
        NLoop = min(self.NTree_,1e9);
        NLoopWeight = self.NTree_/NLoop;
        
        wSampleWeight = NLoopWeight*self.SampleWeight_;


        wjettaggervariables = []
        wjettaggervariables.append("jet_qjetvol")
        wjettaggervariables.append("jet_tau2tau1")
        listOfVarArray1 = []
        listOfVarArray2 = []
        for i in range(len(wjettaggervariables)):
            listOfVarArray1.append( array('f',[0.]) )
            listOfVarArray2.append( array('f',[0.]) )
            varString = wjettaggervariables[i] + " := " + wjettaggervariables[i]
            reader1_.AddVariable(varString, listOfVarArray1[i])
            reader2_.AddVariable(varString, listOfVarArray2[i])
            ungroomed_reader1_.AddVariable(varString, listOfVarArray1[i])
            ungroomed_reader2_.AddVariable(varString, listOfVarArray2[i])
        
        spec11 = array('f',[0.])
        spec12 = array('f',[0.])
        spec13 = array('f',[0.])
        spec14 = array('f',[0.])
        spec21 = array('f',[0.])
        spec22 = array('f',[0.])
        spec23 = array('f',[0.])
        spec24 = array('f',[0.])
         
        ungroomed_spec11 = array('f',[0.])
        ungroomed_spec12 = array('f',[0.])
        ungroomed_spec13 = array('f',[0.])
        ungroomed_spec14 = array('f',[0.])
        ungroomed_spec21 = array('f',[0.])
        ungroomed_spec22 = array('f',[0.])
        ungroomed_spec23 = array('f',[0.])
        ungroomed_spec24 = array('f',[0.])
        reader1_.AddSpectator( "jet_pt_pr", spec11 )
        reader1_.AddSpectator( "jet_mass_pr", spec12 )
        reader1_.AddSpectator( "nPV", spec13 )
        reader1_.AddSpectator( "jet_massdrop_pr", spec14 )
        reader2_.AddSpectator( "jet_pt_pr", spec21 )
        reader2_.AddSpectator( "jet_mass_pr", spec22 )
        reader2_.AddSpectator( "nPV", spec23 )
        reader2_.AddSpectator( "jet_massdrop_pr", spec24 )

        ungroomed_reader1_.AddSpectator( "ungroomed_jet_pt", ungroomed_spec11 )
        ungroomed_reader1_.AddSpectator( "jet_mass_pr", ungroomed_spec12 )
        ungroomed_reader1_.AddSpectator( "nPV", ungroomed_spec13 )
        ungroomed_reader1_.AddSpectator( "jet_massdrop_pr", ungroomed_spec14 )
        ungroomed_reader2_.AddSpectator( "ungroomed_jet_pt", ungroomed_spec21 )
        ungroomed_reader2_.AddSpectator( "jet_mass_pr", ungroomed_spec22 )
        ungroomed_reader2_.AddSpectator( "nPV", ungroomed_spec23 )
        ungroomed_reader2_.AddSpectator( "jet_massdrop_pr", ungroomed_spec24 )

        TMVAMethod = "Likelihood" 
        #reader1_.BookMVA(TMVAMethod,weight1_)
        #reader2_.BookMVA(TMVAMethod,weight2_)
        #ungroomed_reader1_.BookMVA(TMVAMethod,ungroomed_weight1_)
        #ungroomed_reader2_.BookMVA(TMVAMethod,ungroomed_weight2_)

        for i in range(NLoop):
            
            if i % 1000 == 0: print "i = ", i
            
            self.InputTree_.GetEntry(i);
                                    
            ttbarlike = 0;

            if self.Channel_ == 'mu': lepLabel = "muon";
            if self.Channel_ == 'el': lepLabel = "electron";
            index_ca8_in_oppoHemi = [];
            for i in range(6):
                if getattr( self.InputTree_, "GroomedJet_CA8_pt" )[i] > 200:
                    j_ca8_eta = getattr( self.InputTree_, "GroomedJet_CA8_eta" )[i]
                    j_ca8_phi = getattr( self.InputTree_, "GroomedJet_CA8_phi" )[i]
                    l_eta = getattr( self.InputTree_, "W_"+lepLabel+"_eta" )
                    l_phi = getattr( self.InputTree_, "W_"+lepLabel+"_phi" )
                    dR_lj = math.sqrt( (l_eta - j_ca8_eta)**2 + (l_phi - j_ca8_phi)**2 );
#                    print "dR_lj: ", dR_lj
                    if dR_lj > ROOT.TMath.Pi()/2.: index_ca8_in_oppoHemi.append(i);

            minMass = -1;
            theca8Index = -1;
            for i in range(len(index_ca8_in_oppoHemi)):
                curmass = getattr( self.InputTree_, "GroomedJet_CA8_mass_pr" )[index_ca8_in_oppoHemi[i]]
                if curmass > minMass: 
                    minMass = curmass;
                    theca8Index = index_ca8_in_oppoHemi[i];

            if theca8Index >= 0:
                for i in range(6):
                    if getattr( self.InputTree_, "JetPFCor_Pt" )[i] > 30:
                        j_ca8_eta = getattr( self.InputTree_, "GroomedJet_CA8_eta" )[theca8Index]
                        j_ca8_phi = getattr( self.InputTree_, "GroomedJet_CA8_phi" )[theca8Index]
                        j_ak5_eta = getattr( self.InputTree_, "JetPFCor_Eta" )[i]
                        j_ak5_phi = getattr( self.InputTree_, "JetPFCor_Phi" )[i]
                        l_eta = getattr( self.InputTree_, "W_"+lepLabel+"_eta" )
                        l_phi = getattr( self.InputTree_, "W_"+lepLabel+"_phi" )                
                        dR_jj = math.sqrt( (j_ak5_eta - j_ca8_eta)**2 + (j_ak5_phi - j_ca8_phi)**2 );
                        dR_lj = math.sqrt( (l_eta - j_ca8_eta)**2 + (l_phi - j_ca8_phi)**2 );
#                        print "dR_jj: ", dR_jj
                        if dR_lj > ROOT.TMath.Pi()/2. and dR_jj > 0.8 and getattr( self.InputTree_, "JetPFCor_bDiscriminatorCSV" )[i] > 0.244: 
                            ttbarlike = 1

            # make cuts
            leptonCut = 30;
            leptonCutString = "W_muon_pt";
            metCut = 50;
            if self.Channel_ == "el": 
                leptonCut = 35;    
                leptonCutString = "W_electron_pt";
                metCut = 70;

            signallike = 0;
            if getattr( self.InputTree_, "W_pt" ) > 200 and getattr( self.InputTree_, "GroomedJet_CA8_pt" )[0] > 200 and self.InputTree_.ggdboostedWevt == 1 and getattr( self.InputTree_, "event_met_pfmet" ) > metCut and getattr( self.InputTree_, leptonCutString ) > leptonCut and getattr( self.InputTree_, "GroomedJet_CA8_deltaphi_METca8jet") > 2.0 and getattr( self.InputTree_, "GroomedJet_CA8_deltaR_lca8jet") > 1.57: signallike = 1;

            if (ttbarlike and getattr( self.InputTree_, "W_pt" ) > 100) or signallike == True:                
 
                effwt = getattr( self.InputTree_, "effwt" );
                puwt = getattr( self.InputTree_, "puwt" ); 
                totSampleWeight = 1.;
                if self.IsData_: totSampleWeight = wSampleWeight;
                else: totSampleWeight = wSampleWeight*effwt*puwt;
                #print puwt;

                #interference weight
                complexpolewtggH600    = getattr(self.InputTree_,"complexpolewtggH600"); 
                interferencewtggH600   = getattr(self.InputTree_,"interferencewtggH600");
                avecomplexpolewtggH600 = getattr(self.InputTree_,"avecomplexpolewtggH600"); 
                infe_Weight_H600 = complexpolewtggH600*interferencewtggH600/avecomplexpolewtggH600;

                complexpolewtggH700    = getattr(self.InputTree_,"complexpolewtggH700"); 
                interferencewtggH700   = getattr(self.InputTree_,"interferencewtggH700");
                avecomplexpolewtggH700 = getattr(self.InputTree_,"avecomplexpolewtggH700"); 
                infe_Weight_H700 = complexpolewtggH700*interferencewtggH700/avecomplexpolewtggH700;

                complexpolewtggH800    = getattr(self.InputTree_,"complexpolewtggH800"); 
                interferencewtggH800   = getattr(self.InputTree_,"interferencewtggH800");
                avecomplexpolewtggH800 = getattr(self.InputTree_,"avecomplexpolewtggH800"); 
                infe_Weight_H800 = complexpolewtggH800*interferencewtggH800/avecomplexpolewtggH800;

                complexpolewtggH900    = getattr(self.InputTree_,"complexpolewtggH900"); 
                interferencewtggH900   = getattr(self.InputTree_,"interferencewtggH900");
                avecomplexpolewtggH900 = getattr(self.InputTree_,"avecomplexpolewtggH900"); 
                infe_Weight_H900 = complexpolewtggH900*interferencewtggH900/avecomplexpolewtggH900;

                complexpolewtggH1000    = getattr(self.InputTree_,"complexpolewtggH1000"); 
                interferencewtggH1000   = getattr(self.InputTree_,"interferencewtggH1000");
                avecomplexpolewtggH1000 = getattr(self.InputTree_,"avecomplexpolewtggH1000"); 
                infe_Weight_H1000 = complexpolewtggH1000*interferencewtggH1000/avecomplexpolewtggH1000;

                # produce weights for alternative models
#                if self.SignalMass_ > 0:
                if False:                    
                    curIntfRw = getattr(self.InputTree_,"interferencewtggH%03d"%(self.SignalMass_));
                    
#                    print "new: ",IntfRescale(curIntfRw,0.1,0.)*curIntfRw,", old: ",curIntfRw
#                    print "new: ",IntfRescale(curIntfRw,1.0,0.)*curIntfRw,", old: ",curIntfRw                                        
                    
                    genHMass_[0] = getattr(self.InputTree_,"W_H_mass_gen");
                    bsmReweight_cPrime01_brNew00_[0] = self.GetInteferenceWeights( getattr(self.InputTree_,"W_H_mass_gen"), 0.1, 0. )*IntfRescale(curIntfRw,0.1,0.);
                    bsmReweight_cPrime02_brNew00_[0] = self.GetInteferenceWeights( getattr(self.InputTree_,"W_H_mass_gen"), 0.2, 0. )*IntfRescale(curIntfRw,0.2,0.);
                    bsmReweight_cPrime03_brNew00_[0] = self.GetInteferenceWeights( getattr(self.InputTree_,"W_H_mass_gen"), 0.3, 0. )*IntfRescale(curIntfRw,0.3,0.);
                    bsmReweight_cPrime04_brNew00_[0] = self.GetInteferenceWeights( getattr(self.InputTree_,"W_H_mass_gen"), 0.4, 0. )*IntfRescale(curIntfRw,0.4,0.);                
                    bsmReweight_cPrime05_brNew00_[0] = self.GetInteferenceWeights( getattr(self.InputTree_,"W_H_mass_gen"), 0.5, 0. )*IntfRescale(curIntfRw,0.5,0.);
                    bsmReweight_cPrime07_brNew00_[0] = self.GetInteferenceWeights( getattr(self.InputTree_,"W_H_mass_gen"), 0.7, 0. )*IntfRescale(curIntfRw,0.7,0.);
                    bsmReweight_cPrime10_brNew00_[0] = self.GetInteferenceWeights( getattr(self.InputTree_,"W_H_mass_gen"), 1.0, 0. )*IntfRescale(curIntfRw,1.0,0.);                
                else:   
                    genHMass_[0] = -1;
                    bsmReweight_cPrime01_brNew00_[0] = -1;
                    bsmReweight_cPrime02_brNew00_[0] = -1;
                    bsmReweight_cPrime03_brNew00_[0] = -1;
                    bsmReweight_cPrime04_brNew00_[0] = -1;
                    bsmReweight_cPrime05_brNew00_[0] = -1;
                    bsmReweight_cPrime07_brNew00_[0] = -1;
                    bsmReweight_cPrime10_brNew00_[0] = -1;
                
                
                ###################################
                # make training tree
                mass_lvj_[0] = getattr( self.InputTree_, "boostedW_lvj_m" );
                v_pt_[0] = getattr( self.InputTree_, "W_pt" );
                jet_mass_pr_[0] = getattr( self.InputTree_, prefix + "_mass_pr" )[0];

                issignal_[0] = signallike;
                isttbar_[0] = ttbarlike;
            
#                print "signallike: ",signallike,",",issignal_[0];
#                print "ttbarlike: ",ttbarlike,",",isttbar_[0];            
                if ttbarlike == 1:
                    jet_mass_pr_ttbar_[0] = getattr( self.InputTree_, prefix + "_mass_pr" )[theca8Index];
                    jet_pt_ttbar_[0] = getattr( self.InputTree_, prefix + "_pt" )[theca8Index];
                    tau2tau1_ttbar_[0] = getattr( self.InputTree_, prefix + "_tau2tau1" )[theca8Index];                    
                else:
                    jet_mass_pr_ttbar_[0] = -1;
                    jet_pt_ttbar_[0] = -1;
                    tau2tau1_ttbar_[0] = -1;

                jet_pt_pr_[0] = getattr( self.InputTree_, prefix + "_pt_pr" )[0];
                ungroomed_jet_pt_[0] = getattr( self.InputTree_, prefix+"_pt" )[0];
                
                self.jecUnc_.setJetEta( getattr( self.InputTree_, prefix+"_eta" )[0] )
                self.jecUnc_.setJetPt( getattr( self.InputTree_, prefix+"_pt" )[0] );                        
                j_jecfactor_up_[0] = self.jecUnc_.getUncertainty( True )
                self.jecUnc_.setJetEta( getattr( self.InputTree_, prefix+"_eta" )[0] )
                self.jecUnc_.setJetPt( getattr( self.InputTree_, prefix+"_pt" )[0] );               
                j_jecfactor_dn_[0] = self.jecUnc_.getUncertainty( False ) 

                j_jecfactor_up_[0] = math.sqrt( j_jecfactor_up_[0]**2 + 0.02**2 );
                j_jecfactor_dn_[0] = math.sqrt( j_jecfactor_dn_[0]**2 + 0.02**2 );
                curjes_up = 1 + j_jecfactor_up_[0]
                curjes_dn = 1 - j_jecfactor_dn_[0]

                jorig_pt = getattr( self.InputTree_, prefix + "_pt_pr" )[0];    
                jorig_eta = getattr( self.InputTree_, prefix + "_eta_pr" )[0];    
                jorig_phi = getattr( self.InputTree_, prefix + "_phi_pr" )[0];    
                jorig_e = getattr( self.InputTree_, prefix + "_e_pr" )[0];                        
                jdef_ptetaphie = ROOT.TLorentzVector();
                jdef_ptetaphie.SetPtEtaPhiE(jorig_pt, jorig_eta, jorig_phi, jorig_e)
                jdef_up = ROOT.TLorentzVector(jdef_ptetaphie.Px() * curjes_up, jdef_ptetaphie.Py() * curjes_up, jdef_ptetaphie.Pz() * curjes_up, jdef_ptetaphie.E() * curjes_up)                    
                jdef_dn = ROOT.TLorentzVector(jdef_ptetaphie.Px() * curjes_dn, jdef_ptetaphie.Py() * curjes_dn, jdef_ptetaphie.Pz() * curjes_dn, jdef_ptetaphie.E() * curjes_dn)
                jet_mass_pr_up_[0] = jdef_up.M();  
                jet_mass_pr_dn_[0] = jdef_dn.M();  
                    
                if self.Channel_ == "mu" :
                    l_pt_[0] = getattr( self.InputTree_, "W_muon_pt" );
                    l_eta_[0] = getattr( self.InputTree_, "W_muon_eta" );
                elif self.Channel_ == "el":
                    l_pt_[0] = getattr( self.InputTree_, "W_electron_pt" );
                    l_eta_[0] = getattr( self.InputTree_, "W_electron_eta" );

                mvaMET_[0] = getattr( self.InputTree_, "event_metMVA_met" );
                pfMET_[0] = getattr( self.InputTree_, "event_met_pfmet" );        
                nPV_[0] = getattr( self.InputTree_, "event_nPV" );
                totalEventWeight_[0] = totSampleWeight;
                eff_and_pu_Weight_[0] = effwt*puwt;
                wSampleWeight_[0]     = wSampleWeight;
                interference_Weight_H600_[0] = infe_Weight_H600;
                interference_Weight_H700_[0] = infe_Weight_H700;
                interference_Weight_H800_[0] = infe_Weight_H800;
                interference_Weight_H900_[0] = infe_Weight_H900;
                interference_Weight_H1000_[0] = infe_Weight_H1000;
                cps_Weight_H600_[0] = complexpolewtggH600/avecomplexpolewtggH600;
                cps_Weight_H700_[0] = complexpolewtggH700/avecomplexpolewtggH700;
                cps_Weight_H800_[0] = complexpolewtggH800/avecomplexpolewtggH800;
                cps_Weight_H900_[0] = complexpolewtggH900/avecomplexpolewtggH900;
                cps_Weight_H1000_[0] = complexpolewtggH1000/avecomplexpolewtggH1000;

                jet_grsens_ft_[0] = getattr( self.InputTree_, prefix + "_mass_ft" )[0] / getattr( self.InputTree_, prefix + "_mass" )[0];
                jet_grsens_tr_[0] = getattr( self.InputTree_, prefix + "_mass_tr" )[0] / getattr( self.InputTree_, prefix + "_mass" )[0];
                jet_massdrop_pr_[0] = getattr( self.InputTree_, prefix + "_massdrop_pr" )[0];    

                qjetmassdistribution = getattr( self.InputTree_, prefix+"_qjetmass" );
                qjetvol = getListRMS(qjetmassdistribution)/getListMean(qjetmassdistribution);
                jet_qjetvol_[0] = qjetvol;

                jet_tau2tau1_[0] = getattr( self.InputTree_, prefix + "_tau2tau1" )[0];     
                jet_jetconstituents_[0] = getattr( self.InputTree_, prefix + "_jetconstituents" )[0];     

                jet_rcore4_[0] = getattr( self.InputTree_, prefix + "_rcores")[3*6 + 0];
                jet_rcore5_[0] = getattr( self.InputTree_, prefix + "_rcores")[4*6 + 0];
                jet_rcore6_[0] = getattr( self.InputTree_, prefix + "_rcores")[5*6 + 0];
                jet_rcore7_[0] = getattr( self.InputTree_, prefix + "_rcores")[6*6 + 0];

                jet_planarlow04_[0] = getattr( self.InputTree_, prefix + "_planarflow04");
                jet_planarlow05_[0] = getattr( self.InputTree_, prefix + "_planarflow05");
                jet_planarlow06_[0] = getattr( self.InputTree_, prefix + "_planarflow06");
                jet_planarlow07_[0] = getattr( self.InputTree_, prefix + "_planarflow07");
                
#                nbjets_[0] = getattr( self.InputTree_, "GroomedJet_numberbjets" );
                nbjets_cvsl_[0] = getattr( self.InputTree_, "GroomedJet_numberbjets_csvl" );
                nbjets_cvsm_[0] = getattr( self.InputTree_, "GroomedJet_numberbjets_csvm" );
                nbjets_ssvhem_[0] = getattr( self.InputTree_, "GroomedJet_numberbjets_ssvhem" );
                nbjets_csvl_veto_[0] = getattr( self.InputTree_, "GroomedJet_numberbjets_csvl_veto" );
                nbjets_csvm_veto_[0] = getattr( self.InputTree_, "GroomedJet_numberbjets_csvm_veto" );
                nbjets_ssvhem_veto_[0] = getattr( self.InputTree_, "GroomedJet_numberbjets_ssvhem_veto" );

                nbjetsCSV_[0] =0 ;
                for i in range(0,6):
                    if  getattr(self.InputTree_, "JetPFCor_bDiscriminatorCSV")[i] >=0.244 :nbjetsCSV_[0]=nbjetsCSV_[0]+1;
                    #print i, getattr(self.InputTree_, "JetPFCor_bDiscriminatorCSV")[i], nbjetsCSV_[0];
                nbjetsSSVHE_[0] = getattr( self.InputTree_, "numPFCorJetBTags");
                
                njets_[0] = getattr( self.InputTree_, "GroomedJet_numberjets" );
                pt1FracVal = max( getattr( self.InputTree_, prefix + "_prsubjet1ptoverjetpt" ), getattr( self.InputTree_, prefix + "_prsubjet2ptoverjetpt" ) );
                pt2FracVal = min( getattr( self.InputTree_, prefix + "_prsubjet1ptoverjetpt" ), getattr( self.InputTree_, prefix + "_prsubjet2ptoverjetpt" ) );
                jet_pt1frac_[0] = pt1FracVal;
                jet_pt2frac_[0] = pt2FracVal;
                jet_sjdr_[0] = getattr( self.InputTree_, prefix + "_prsubjet1subjet2_deltaR" );       
                
                deltaR_lca8jet_[0] = getattr( self.InputTree_, prefix + "_deltaR_lca8jet" );       
                deltaphi_METca8jet_[0] = getattr( self.InputTree_, prefix + "_deltaphi_METca8jet" );       
                deltaphi_Vca8jet_[0] = getattr( self.InputTree_, prefix + "_deltaphi_Vca8jet" );       
                
                listOfVarArray1[0][0] = jet_qjetvol_[0]
                listOfVarArray1[1][0] = jet_tau2tau1_[0]

                listOfVarArray2[0][0] = jet_qjetvol_[0]
                listOfVarArray2[1][0] = jet_tau2tau1_[0]
               
                #if jet_pt_pr_[0] > 200 and jet_pt_pr_[0] < 275: 
                #   ca8wjettaggerpt200_275_[0] = reader1_.EvaluateMVA(TMVAMethod)
                #   ca8wjettaggerpt275_500_[0] = -1;

                #if jet_pt_pr_[0] > 275 and jet_pt_pr_[0] < 500: 
                #   ca8wjettaggerpt200_275_[0] = -1.;
                #   ca8wjettaggerpt275_500_[0] = float(reader2_.EvaluateMVA(TMVAMethod))

                #if jet_pt_pr_[0] > 200 and jet_pt_pr_[0] <= 275: 
                #   ca8wjettaggerpt200_275_[0] = float(reader1_.EvaluateMVA(TMVAMethod))
                #   ca8wjettaggerpt275_500_[0] = -1;
                #if jet_pt_pr_[0] > 275 and jet_pt_pr_[0] <= 500: 
                #   ca8wjettaggerpt200_275_[0] = -1.;
                #   ca8wjettaggerpt275_500_[0] = float(reader2_.EvaluateMVA(TMVAMethod))

                #if ungroomed_jet_pt_[0] > 200 and ungroomed_jet_pt_[0]<=275:
                #   ungroomedwjettaggerpt200_275_[0] = float(ungroomed_reader1_.EvaluateMVA(TMVAMethod))
                #   ungroomedwjettaggerpt275_500_[0] = -1;
                #if ungroomed_jet_pt_[0] > 275 and ungroomed_jet_pt_[0]<=500:
                #   ungroomedwjettaggerpt200_275_[0] = -1.;
                #   ungroomedwjettaggerpt275_500_[0] = float(ungroomed_reader2_.EvaluateMVA(TMVAMethod))

                otree.Fill();
                ###################################

        self.OFile_.cd();
        otree.Write();
        self.OFile_.Close();

    ## training tree name
    def getTrainingTreeName(self):
        return self.OFileName_
    
    def getSampleLabel(self):
        return self.Label_

    ### ------------------------------------------

    def turnOffBranches(self):
        
        prefix = self.JetPrefix_;
        
        self.InputTree_.SetBranchStatus("*",0);
        
        self.InputTree_.SetBranchStatus("ggdboostedWevt",1);
        self.InputTree_.SetBranchStatus("effwt",1);
        self.InputTree_.SetBranchStatus("puwt",1);
        self.InputTree_.SetBranchStatus("puwt_up",1);
        self.InputTree_.SetBranchStatus("puwt_down",1);

        if self.Channel_ == "mu" :
            self.InputTree_.SetBranchStatus("W_muon_pt",1);
            self.InputTree_.SetBranchStatus("W_muon_eta",1);
            self.InputTree_.SetBranchStatus("W_muon_phi",1);
        
        elif self.Channel_ == "el":
            self.InputTree_.SetBranchStatus("W_electron_pt",1);
            self.InputTree_.SetBranchStatus("W_electron_eta",1);
            self.InputTree_.SetBranchStatus("W_electron_phi",1);


        self.InputTree_.SetBranchStatus("event_metMVA_met",1);
        self.InputTree_.SetBranchStatus("event_met_pfmet",1);
        self.InputTree_.SetBranchStatus("event_nPV",1);
        self.InputTree_.SetBranchStatus("boostedW_lvj_m",1);
        self.InputTree_.SetBranchStatus("W_pt",1);
        self.InputTree_.SetBranchStatus(prefix + "_pt_pr",1);
        self.InputTree_.SetBranchStatus(prefix + "_eta_pr",1);
        self.InputTree_.SetBranchStatus(prefix + "_phi_pr",1);
        self.InputTree_.SetBranchStatus(prefix + "_e_pr",1);
        self.InputTree_.SetBranchStatus(prefix + "_eta",1);
        self.InputTree_.SetBranchStatus(prefix + "_pt",1);
        self.InputTree_.SetBranchStatus(prefix + "_massdrop_pr",1);
        self.InputTree_.SetBranchStatus(prefix + "_mass",1);
        self.InputTree_.SetBranchStatus(prefix + "_mass_pr",1);        
        self.InputTree_.SetBranchStatus(prefix + "_mass_tr",1);
        self.InputTree_.SetBranchStatus(prefix + "_mass_ft",1);
        self.InputTree_.SetBranchStatus(prefix + "_tau2tau1",1);
        self.InputTree_.SetBranchStatus(prefix + "_qjetmass",1);
        self.InputTree_.SetBranchStatus(prefix + "_rcores",1);
        self.InputTree_.SetBranchStatus(prefix + "_jetconstituents",1);

        self.InputTree_.SetBranchStatus("GroomedJet_numberjets",1);
        self.InputTree_.SetBranchStatus("GroomedJet_numberbjets",1);

        self.InputTree_.SetBranchStatus("GroomedJet_numberbjets_csvl",1);
        self.InputTree_.SetBranchStatus("GroomedJet_numberbjets_csvm",1);
        self.InputTree_.SetBranchStatus("GroomedJet_numberbjets_ssvhem",1);
        self.InputTree_.SetBranchStatus("GroomedJet_numberbjets_csvl_veto",1);
        self.InputTree_.SetBranchStatus("GroomedJet_numberbjets_csvm_veto",1);
        self.InputTree_.SetBranchStatus("GroomedJet_numberbjets_ssvhem_veto",1);

        self.InputTree_.SetBranchStatus("JetPFCor_Pt",1);
        self.InputTree_.SetBranchStatus("JetPFCor_Eta",1);
        self.InputTree_.SetBranchStatus("JetPFCor_Phi",1);
        self.InputTree_.SetBranchStatus("JetPFCor_bDiscriminatorCSV",1);
        self.InputTree_.SetBranchStatus("numPFCorJetBTags",1);
        self.InputTree_.SetBranchStatus(prefix + "_prsubjet1ptoverjetpt",1);
        self.InputTree_.SetBranchStatus(prefix + "_prsubjet2ptoverjetpt",1);
        self.InputTree_.SetBranchStatus(prefix + "_prsubjet1subjet2_deltaR",1);
        self.InputTree_.SetBranchStatus(prefix + "_planarflow04",1);
        self.InputTree_.SetBranchStatus(prefix + "_planarflow05",1);
        self.InputTree_.SetBranchStatus(prefix + "_planarflow06",1);
        self.InputTree_.SetBranchStatus(prefix + "_planarflow07",1);

        self.InputTree_.SetBranchStatus(prefix + "_deltaR_lca8jet",1);
        self.InputTree_.SetBranchStatus(prefix + "_deltaphi_METca8jet",1);
        self.InputTree_.SetBranchStatus(prefix + "_deltaphi_Vca8jet",1);

        if self.SignalMass_ > 0: self.InputTree_.SetBranchStatus("W_H_mass_gen",1)
        self.InputTree_.SetBranchStatus("avecomplexpolewtggH600",1)
        self.InputTree_.SetBranchStatus("avecomplexpolewtggH700",1)
        self.InputTree_.SetBranchStatus("avecomplexpolewtggH800",1)
        self.InputTree_.SetBranchStatus("avecomplexpolewtggH900",1)
        self.InputTree_.SetBranchStatus("avecomplexpolewtggH1000",1)
        self.InputTree_.SetBranchStatus("complexpolewtggH600",1)
        self.InputTree_.SetBranchStatus("complexpolewtggH700",1)
        self.InputTree_.SetBranchStatus("complexpolewtggH800",1)
        self.InputTree_.SetBranchStatus("complexpolewtggH900",1)
        self.InputTree_.SetBranchStatus("complexpolewtggH1000",1)
        self.InputTree_.SetBranchStatus("interferencewtggH600",1)
        self.InputTree_.SetBranchStatus("interferencewtggH700",1)
        self.InputTree_.SetBranchStatus("interferencewtggH800",1)
        self.InputTree_.SetBranchStatus("interferencewtggH900",1)
        self.InputTree_.SetBranchStatus("interferencewtggH1000",1)



