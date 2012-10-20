#! /usr/bin/env python
import os
import glob
import math
import array

from ROOT import gROOT, gStyle, gSystem, TLatex, TString, TFile,TLine, TLegend, TH1F, RooFit, RooArgSet, RooArgList, RooAddPdf, RooWorkspace, RooRealVar,RooDataSet, RooDataHist, RooHistPdf, TIter, kTRUE, kFALSE, kGray, kRed, kDashed, kGreen,kAzure
import subprocess
from subprocess import Popen

from sampleWrapperClass import *
from trainingClass      import *
from BoostedWSamples    import * 
from mvaApplication     import *

gROOT.ProcessLine('.L tdrstyle.C')
ROOT.setTDRStyle()

ROOT.gSystem.Load("PDFs/RooErfExpPdf_cxx.so")
#ROOT.gSystem.Load("PDFs/RooErfExp_Gaus_Pdf_cxx.so")
#ROOT.gSystem.Load("PDFs/RooErfExp_2Gaus_Pdf_cxx.so")
#ROOT.gSystem.Load("PDFs/RooErfExp_Voig_Gaus_Pdf_cxx.so")

############################################################
############################################
#            Job steering                  #
############################################
parser = OptionParser()

parser.add_option('-b', action='store_true', dest='noX', default=False,
                  help='no X11 windows')

## ---------------------------------------------------
## ---------------------------------------------------
## ---------------------------------------------------

## ---------------------------------------------------

class doFit_wj_and_wlvj:
    def __init__(self, in_cutOnMassDrop):
        print "Begin to fit"

        self.cutOnMassDrop_=in_cutOnMassDrop;

        rrv_mass_j  = RooRealVar("rrv_mass_j","mass_j",30.,140.);
        rrv_mass_lvj= RooRealVar("rrv_mass_lvj","mass_lvj",200.,1500.);
        #rrv_mass_j.setRange("ref",rrv_mass_j.getMin(),rrv_mass_j.getMax());
        #rrv_mass_lvj.setRange("ref",rrv_mass_lvj.getMin(),rrv_mass_lvj.getMax());

        self.workspace_ = RooWorkspace("workspace_","workspace_");
        ws_import=getattr(self.workspace_,"import");
        ws_import(rrv_mass_j);
        ws_import(rrv_mass_lvj);

        #prepare workspace for unbin-Limit
        self.workspace4limit_ = RooWorkspace("workspace4limit_","workspace4limit_");


        self.mj_sideband_lo_min=30;
        self.mj_sideband_lo_max=60;
        self.mj_signal_min=70;
        self.mj_signal_max=95;
        self.mj_sideband_hi_min=100;
        self.mj_sideband_hi_max=140;
        rrv_mass_j.setRange("sb_lo",self.mj_sideband_lo_min,self.mj_sideband_lo_max);
        rrv_mass_j.setRange("signal",self.mj_signal_min,self.mj_signal_max); 
        rrv_mass_j.setRange("sb_hi",self.mj_sideband_hi_min,self.mj_sideband_hi_max);

        #prepare the data and mc files
        self.file_TTB_mc=("ofile_TTbar.root");
        self.file_WW_mc=("ofile_WW.root");
        self.file_WJets_mc=("ofile_WJets.root");
        self.file_data=("ofile_data.root");
        self.file_ggH600=("ofile_ggH600.root");
        self.file_Directory="trainingtrees/";

        #result files: The event number, parameters and error write into a txt file. The dataset and pdfs write into a root file
        self.file_rlt_txt ="hww_rlt.txt"
        self.file_rlt_root="hww_lvj_rlt.root"
        
        self.file_out=open(self.file_rlt_txt,"w");
        self.file_out.write("\nWelcome:\n");
        self.file_out.close()
        self.file_out=open(self.file_rlt_txt,"a+");

## ---------------------------------------------------
    def make_Model(self, label, in_model_name, mass_spectrum="mj"):
        rrv_number = RooRealVar("rrv_number"+label+mass_spectrum,"rrv_number"+label+mass_spectrum,500,1,100000);
        model_raw  = self.make_Pdf(label,in_model_name,mass_spectrum)
        model = ROOT.RooExtendPdf("model"+label+mass_spectrum,"model"+label+mass_spectrum, model_raw, rrv_number );

        getattr(self.workspace_,"import")(rrv_number)
        getattr(self.workspace_,"import")(model)
        return self.workspace_.pdf("model"+label+mass_spectrum)

    def make_Pdf(self, label, in_model_name, mass_spectrum="mj"):
        if mass_spectrum=="mj": rrv_mass_j = self.workspace_.var("rrv_mass_j"); 
        if mass_spectrum=="mlvj": rrv_mass_j = self.workspace_.var("rrv_mass_lvj"); 
        
        if in_model_name == "Voig":
            rrv_mean_voig=RooRealVar("rrv_mean_voig"+label,"rrv_mean_voig"+label,82,78,87);
            rrv_width_voig=RooRealVar("rrv_width_voig"+label,"rrv_width_voig"+label,7.,1,10);
            rrv_sigma_voig=RooRealVar("rrv_sigma_voig"+label,"rrv_sigma_voig"+label,5,1,15);
            model_raw = ROOT.RooVoigtian("model_raw"+label+mass_spectrum,"model_raw"+label+mass_spectrum, rrv_mass_j,rrv_mean_voig,rrv_width_voig,rrv_sigma_voig);
    
        if in_model_name == "Gaus":
            rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,82,78,87);
            rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label,"rrv_sigma_gaus"+label,7,1,15);
            model_raw = ROOT.RooGaussian("model_raw"+label+mass_spectrum,"model_raw"+label+mass_spectrum, rrv_mass_j,rrv_mean_gaus,rrv_sigma_gaus);
    
        if in_model_name == "CB":
            rrv_mean_CB=RooRealVar("rrv_mean_CB"+label,"rrv_mean_CB"+label,82,78,87);
            rrv_sigma_CB=RooRealVar("rrv_sigma_CB"+label,"rrv_sigma_CB"+label,5,2,10);
            rrv_alpha_CB=RooRealVar("rrv_alpha_CB"+label,"rrv_alpha_CB"+label,-2,-4,-1);
            rrv_n_CB=RooRealVar("rrv_n_CB"+label,"rrv_n_CB"+label,2,0.,4);
            model_raw = ROOT.RooCBShape("model_raw"+label+mass_spectrum,"model_raw"+label+mass_spectrum, rrv_mass_j,rrv_mean_CB,rrv_sigma_CB,rrv_alpha_CB,rrv_n_CB);
    
        if in_model_name == "CBBW": # FFT: BreitWigner*CBShape
            rrv_mean_CB=RooRealVar("rrv_mean_CB"+label,"rrv_mean_CB"+label,83.5,80,87);
            rrv_sigma_CB=RooRealVar("rrv_sigma_CB"+label,"rrv_sigma_CB"+label,6,2,10);
            rrv_alpha_CB=RooRealVar("rrv_alpha_CB"+label,"rrv_alpha_CB"+label,-2,-4,-1);
            rrv_n_CB=RooRealVar("rrv_n_CB"+label,"rrv_n_CB"+label,0.5,0.,2);
            rrv_mean_BW=RooRealVar("rrv_mean_BW"+label,"rrv_mean_BW"+label,0);
            rrv_width_BW=RooRealVar("rrv_width_BW"+label,"rrv_width_BW"+label,10,5,20);
            cbshape = ROOT.RooCBShape("cbshape"+label,"cbshape"+label, rrv_mass_j,rrv_mean_CB,rrv_sigma_CB,rrv_alpha_CB,rrv_n_CB);
            bw = ROOT.RooBreitWigner("bw"+label,"bw"+label, rrv_mass_j,rrv_mean_BW,rrv_width_BW);
            model_raw = ROOT.RooFFTConvPdf("model_raw"+label+mass_spectrum,"model_raw"+label+mass_spectrum, rrv_mass_j, cbshape, bw);

        if in_model_name == "LDGaus": # FFT: Landau*Gaus
            rrv_mean_landau=RooRealVar("rrv_mean_landau"+label,"rrv_mean_landau"+label,83.5,80,87);
            rrv_sigma_landau=RooRealVar("rrv_sigma_landau"+label,"rrv_sigma_landau"+label,5,2,10);
            rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,0);
            rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label,"rrv_sigma_gaus"+label,16,10,20);
            landau = ROOT.RooLandau("landau"+label,"landau"+label, rrv_mass_j,rrv_mean_landau,rrv_sigma_landau);
            gaus = ROOT.RooBreitWigner("gaus"+label,"gaus"+label, rrv_mass_j,rrv_mean_gaus,rrv_sigma_gaus);
            model_raw = ROOT.RooFFTConvPdf("model_raw"+label+mass_spectrum,"model_raw"+label+mass_spectrum, rrv_mass_j, landau, gaus);

        if in_model_name == "ErfExp" :
            rrv_c_ErfExp = RooRealVar("rrv_c_ErfExp"+label,"rrv_c_ErfExp"+label,-0.05,-0.1,0.);
            #rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label,"rrv_offset_ErfExp"+label,78.,10.,140.);
            rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label,"rrv_offset_ErfExp"+label,78.,10.,1400.);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label,"rrv_width_ErfExp"+label,30.,10,100.);
            model_raw = ROOT.RooErfExpPdf("model_raw"+label+mass_spectrum,"model_raw"+label+mass_spectrum,rrv_mass_j,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp);
    
        if in_model_name == "ErfExpGaus":
            rrv_c_ErfExp = RooRealVar("rrv_c_ErfExp"+label,"rrv_c_ErfExp"+label,-0.05,-0.2,0.);
            rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label,"rrv_offset_ErfExp"+label,100.,10.,140.);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label,"rrv_width_ErfExp"+label,30.,10,100.);
            rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,82,78,87);
            rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label,"rrv_sigma_gaus"+label,7,1,20);
            rrv_high = RooRealVar("rrv_high"+label,"rrv_high"+label,0.7,0.,1.);
            erfExp = ROOT.RooErfExpPdf("erfExp"+label,"erfExp"+label,rrv_mass_j,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp);
            gaus = ROOT.RooGaussian("gaus"+label,"gaus"+label, rrv_mass_j,rrv_mean_gaus,rrv_sigma_gaus);
            model_raw =RooAddPdf("model_raw"+label+mass_spectrum,"model_raw"+label+mass_spectrum,RooArgList(erfExp,gaus),RooArgList(rrv_high))
    
        if in_model_name == "ErfExpGaus_v1":
            rrv_c_ErfExp = RooRealVar("rrv_c_ErfExp"+label,"rrv_c_ErfExp"+label,-0.007,-0.1,0.);
            rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label,"rrv_offset_ErfExp"+label,700.,10.,1400.);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label,"rrv_width_ErfExp"+label,24.,10,150.);
            rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,600,500,700);
            rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label,"rrv_sigma_gaus"+label,70,10,150);
            rrv_high = RooRealVar("rrv_high"+label,"rrv_high"+label,0.1,0.,1.);
            erfExp = ROOT.RooErfExpPdf("erfExp"+label,"erfExp"+label,rrv_mass_j,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp);
            gaus = ROOT.RooGaussian("gaus"+label,"gaus"+label, rrv_mass_j,rrv_mean_gaus,rrv_sigma_gaus);
            model_raw =RooAddPdf("model_raw"+label+mass_spectrum,"model_raw"+label+mass_spectrum,RooArgList(erfExp,gaus),RooArgList(rrv_high))
    
        if in_model_name == "ErfExpGaus_v2":
            rrv_c_ErfExp = RooRealVar("rrv_c_ErfExp"+label,"rrv_c_ErfExp"+label,-0.05,-10.,0.);
            rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label,"rrv_offset_ErfExp"+label,100.,10.,140.);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label,"rrv_width_ErfExp"+label,30.,10,100.);
            rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,82,78,87);
            rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label,"rrv_sigma_gaus"+label,7,1,20);
            rrv_high = RooRealVar("rrv_high"+label,"rrv_high"+label,200.,0.,1000.);
            model_raw = ROOT.RooErfExp_Gaus_Pdf("model_raw"+label+mass_spectrum,"model_raw"+label+mass_spectrum, rrv_mass_j,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp,rrv_mean_gaus,rrv_sigma_gaus,rrv_high );
    
        if in_model_name == "ErfExp2Gaus":
            rrv_c_ErfExp = RooRealVar("rrv_c_ErfExp"+label,"rrv_c_ErfExp"+label,-0.1,-10.,0.);
            rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label,"rrv_offset_ErfExp"+label,100.,10.,140.);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label,"rrv_width_ErfExp"+label,30.,10,100.);
            rrv_mean_gaus1=RooRealVar("rrv_mean_gaus1"+label,"rrv_mean_gaus1"+label,82,78,87);
            rrv_sigma_gaus1=RooRealVar("rrv_sigma_gaus1"+label,"rrv_sigma_gaus1"+label,10,0.1,100);
            rrv_high1 = RooRealVar("rrv_high1"+label,"rrv_high1"+label,1,0.,10.);
            rrv_mean_gaus2=RooRealVar("rrv_mean_gaus2"+label,"rrv_mean_gaus2"+label,174,160,187);
            rrv_sigma_gaus2=RooRealVar("rrv_sigma_gaus2"+label,"rrv_sigma_gaus2"+label,20,0.1,100);
            rrv_high2 = RooRealVar("rrv_high2"+label,"rrv_high2"+label,0.1,0.,10.);
            model_raw = ROOT.RooErfExp_2Gaus_Pdf("model_raw"+label+mass_spectrum,"model_raw"+label+mass_spectrum, rrv_mass_j,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp,rrv_mean_gaus1,rrv_sigma_gaus1,rrv_high1,rrv_mean_gaus2,rrv_sigma_gaus2,rrv_high2 );
    
        if in_model_name == "ErfExpVoigGaus":
            rrv_c_ErfExp = RooRealVar("rrv_c_ErfExp"+label,"rrv_c_ErfExp"+label,-0.1,-10.,0.);
            rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label,"rrv_offset_ErfExp"+label,100.,10.,140.);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label,"rrv_width_ErfExp"+label,30.,10,100.);
            rrv_mean_voig=RooRealVar("rrv_mean_voig"+label,"rrv_mean_voig"+label,82,78,87);
            rrv_width_voig=RooRealVar("rrv_width_voig"+label,"rrv_width_voig"+label,5,1,20);
            rrv_sigma_voig=RooRealVar("rrv_sigma_voig"+label,"rrv_sigma_voig"+label,5,1,100);
            rrv_high1 = RooRealVar("rrv_high1"+label,"rrv_high1"+label,1,0.,200.);
            rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,174)#,160,187);
            rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label,"rrv_sigma_gaus"+label,20)#,0.1,100);
            rrv_high2 = RooRealVar("rrv_high2"+label,"rrv_high2"+label,0.)#,0.,0.);
            model_raw = ROOT.RooErfExp_Voig_Gaus_Pdf("model_raw"+label+mass_spectrum,"model_raw"+label+mass_spectrum, rrv_mass_j,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp,rrv_mean_voig,rrv_width_voig,rrv_sigma_voig,rrv_high1,rrv_mean_gaus,rrv_sigma_gaus,rrv_high2 );

        getattr(self.workspace_,"import")(model_raw)
        return self.workspace_.pdf("model_raw"+label+mass_spectrum)
    
## ---------------------------------------------------
    def get_mj_Model(self,label):
        return self.workspace_.pdf("model"+label+"mj")

## ---------------------------------------------------
    def get_TTB_mj_Model(self):
        rdataset_MC_TTB=self.workspace_.data("rdataset_MC_TTB")
        model_TTB=self.get_mj_Model("_TTB");
        parameters_TTB=model_TTB.getParameters(rdataset_MC_TTB);
        par=parameters_TTB.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
        return self.workspace_.pdf("model_TTBmj")

## ---------------------------------------------------
    def get_WW_mj_Model(self):
        rdataset_MC_WW=self.workspace_.data("rdataset_MC_WW")
        model_WW=self.get_mj_Model("_WW");
        parameters_WW=model_WW.getParameters(rdataset_MC_WW);
        par=parameters_WW.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
        return self.workspace_.pdf("model_WWmj")

## ---------------------------------------------------
    def get_WJets_mj_Model(self):
        rdataset_MC_WJets=self.workspace_.data("rdataset_MC_WJets")
        model_WJets=self.get_mj_Model("_WJets");
        parameters_WJets=model_WJets.getParameters(rdataset_MC_WJets);
        par=parameters_WJets.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            paraName=TString(param.GetName());
            if not ( paraName.Contains("rrv_c_ErfExp_WJets") or paraName.Contains("rrv_number_WJets")) :param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
        return self.workspace_.pdf("model_WJetsmj")
## ---------------------------------------------------
    def get_mlvj_Model(self,label):
        return self.workspace_.pdf("model"+label+"_lvjSignalRegionmlvj")

## ---------------------------------------------------
    def get_TTB_mlvj_Model(self):
        rdataset_MC_TTB=self.workspace_.data("rdataset_TTB_lvj_SignalRegion")
        model_TTB=self.get_mlvj_Model("_TTB");
        parameters_TTB=model_TTB.getParameters(rdataset_MC_TTB);
        par=parameters_TTB.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
        #return self.workspace_.pdf("model_TTBmj")
        return model_TTB


## ---------------------------------------------------
    def get_ggH_mlvj_Model(self):
        rdataset_MC_ggH=self.workspace_.data("rdataset_ggH600_lvj_SignalRegion")
        model_ggH=self.get_mlvj_Model("_ggH600");
        rdataset_MC_ggH.Print()
        model_ggH.Print()
        parameters_ggH=model_ggH.getParameters(rdataset_MC_ggH);
        par=parameters_ggH.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
        #return self.workspace_.pdf("model_ggHmj")
        #raw_input("ENTER ot continue");
        return model_ggH

## ---------------------------------------------------
    def get_WW_mlvj_Model(self):
        rdataset_MC_WW=self.workspace_.data("rdataset_WW_lvj_SignalRegion")
        model_WW=self.get_mlvj_Model("_WW");
        parameters_WW=model_WW.getParameters(rdataset_MC_WW);
        par=parameters_WW.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
        #return self.workspace_.pdf("model_WWmj")
        return model_WW

## ---------------------------------------------------
    def get_WJets_mlvj_Model(self):
        print "get_WJets_mlvj_Model"
        rdataset_MC_WJets=self.workspace_.data("rdataset_WJets_lvj_SignalRegion")
        model_WJets=self.get_mlvj_Model("_WJets");
        model_WJets.Print()
        parameters_WJets=model_WJets.getParameters(rdataset_MC_WJets);
        par=parameters_WJets.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            paraName=TString(param.GetName());
            param.Print();
            if paraName.Contains("rrv_number_WJets"): 
                if self.workspace_.var("rrv_number_WJets_in_mj_SignalRegion_from_fitting"):
                    self.workspace_.var("rrv_number_WJets_in_mj_SignalRegion_from_fitting").Print()
                    param.setVal( self.workspace_.var("rrv_number_WJets_in_mj_SignalRegion_from_fitting").getVal() )
                param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
        #raw_input("ENTER ot continue");
        #return self.workspace_.pdf("model_WJetsmj")
        return model_WJets

## ---------------------------------------------------
    def fit_m_j_single_MC_sample(self,in_file_name, label, in_model_name):
    
        # read in tree
        fileIn_name=TString(self.file_Directory+in_file_name);
        fileIn = TFile(fileIn_name.Data());
        treeIn = fileIn.Get("otree");
        
        # define bdt reader
        listOfTrainingVariables1 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1"];
        bdtSimple = tmvaApplicator( listOfTrainingVariables1, "weights/Wtagger_200to275_simple_BDT.weights.xml");
            
        rrv_mass_j = self.workspace_.var("rrv_mass_j"); 
        rrv_mass_j.setBins(55);
        rrv_weight = RooRealVar("rrv_weight","rrv_weight",0. ,1.) 
        rdataset_MC = ROOT.RooDataSet("rdataset_MC"+label,"rdataset_MC"+label,ROOT.RooArgSet(rrv_mass_j,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        # make cuts (including mass drop) # create a RooDataSet
        print "N entries: ", treeIn.GetEntries()
        hnum_3region=TH1F("hnum_3region"+label,"hnum_3region"+label,4,-1.5,2.5);#-1: sblo; 0:signal; 1: sbhi; 2:total
        for i in range(treeIn.GetEntries()):
            if i % 10000 == 0: print "i: ",i
            treeIn.GetEntry(i);
    
            discriminantCut = False; 
                
            if self.cutOnMassDrop_ and treeIn.jet_massdrop_pr < 0.25: discriminantCut = True;
            elif not self.cutOnMassDrop_:
                listOfVarVals = [];
                for kk in range(len(listOfTrainingVariables1)):
                    listOfVarVals.append( getattr( treeIn, listOfTrainingVariables1[kk] ) );
                BDTval = bdtSimple.eval( listOfVarVals );
                if BDTval > 0.0: discriminantCut = True;
            else: discriminantCut = False;
           
            if treeIn.jet_pt_pr > 200. and discriminantCut and treeIn.jet_mass_pr >= rrv_mass_j.getMin() and treeIn.jet_mass_pr<rrv_mass_j.getMax() and treeIn.njets ==0:
                rrv_mass_j.setVal( treeIn.jet_mass_pr );
                rdataset_MC.add( ROOT.RooArgSet( rrv_mass_j ), treeIn.totalEventWeight );
                #if treeIn.jet_mass_pr<=60: hnum_3region.Fill(-1,treeIn.totalEventWeight );
                #elif treeIn.jet_mass_pr>100: hnum_3region.Fill(1,treeIn.totalEventWeight);
                #else: hnum_3region.Fill(0,treeIn.totalEventWeight);
                if treeIn.jet_mass_pr >=self.mj_sideband_lo_min and treeIn.jet_mass_pr <self.mj_sideband_lo_max: hnum_3region.Fill(-1,treeIn.totalEventWeight );
                if treeIn.jet_mass_pr >=self.mj_signal_min      and treeIn.jet_mass_pr <self.mj_signal_max     : hnum_3region.Fill(0,treeIn.totalEventWeight);
                if treeIn.jet_mass_pr >=self.mj_sideband_hi_min and treeIn.jet_mass_pr <self.mj_sideband_hi_max: hnum_3region.Fill(1,treeIn.totalEventWeight);
                hnum_3region.Fill(2,treeIn.totalEventWeight);
        rrv_number_sblo=RooRealVar("rrv_number_sblo"+label+"mj","rrv_number_sblo"+label+"mj",hnum_3region.GetBinContent(1));
        rrv_number_signal=RooRealVar("rrv_number_signal"+label+"mj","rrv_number_signal"+label+"mj",hnum_3region.GetBinContent(2));
        rrv_number_sbhi=RooRealVar("rrv_number_sbhi"+label+"mj","rrv_number_sbhi"+label+"mj",hnum_3region.GetBinContent(3));
        getattr(self.workspace_,"import")(rrv_number_sblo)
        getattr(self.workspace_,"import")(rrv_number_signal)
        getattr(self.workspace_,"import")(rrv_number_sbhi)
                
        print "N_rdataset_MC: ", rdataset_MC.Print();
        getattr(self.workspace_,"import")(rdataset_MC)

        model = self.make_Model(label,in_model_name);
        # fit to a Model
        rfresult = model.fitTo(rdataset_MC,RooFit.Save(1), RooFit.SumW2Error(kTRUE) ,RooFit.Extended(kTRUE) );
        rfresult = model.fitTo(rdataset_MC,RooFit.Save(1), RooFit.SumW2Error(kTRUE) ,RooFit.Extended(kTRUE) );
        
        mplot = rrv_mass_j.frame(RooFit.Title(in_file_name+" fitted by "+in_model_name));
        rdataset_MC.plotOn( mplot ,RooFit.DataError(ROOT.RooAbsData.SumW2) );
        #model.plotOn( mplot, RooFit.VisualizeError(rfresult,1),RooFit.FillColor(ROOT.kOrange) );
        model.plotOn(mplot,RooFit.VisualizeError(rfresult,1,kFALSE),RooFit.DrawOption("F"),RooFit.FillColor(ROOT.kOrange));
        rdataset_MC.plotOn( mplot ,RooFit.DataError(ROOT.RooAbsData.SumW2) );
        model.plotOn( mplot );
        #pull
        hpull=mplot.pullHist();
        mplot_pull = rrv_mass_j.frame(RooFit.Title("Pull Distribution"));
        mplot_pull.addPlotable(hpull,"P");
        mplot_pull.SetTitle("PULL");
        mplot_pull.GetYaxis().SetRangeUser(-5,5);
         
        parameters_list=model.getParameters(rdataset_MC);
        self.draw_canvas( mplot, mplot_pull,parameters_list, "plots/m_j_single_BDTcut/", in_file_name, in_model_name)
        
        rfresult.Print();
    
        ##chi2 fit begin
        #rdataHist=rdataset_MC.binnedClone();
        #rdataHist.Print("v");
        #chi2=ROOT.RooChi2Var("chi2","chi2",model,rdataHist,RooFit.DataError(ROOT.RooAbsData.SumW2));
        #m=ROOT.RooMinuit(chi2);
        #m.migrad();
        #m.hesse();
        #r_chi2_wgt=m.save();
        #mplot2 = rrv_mass_j.frame(RooFit.Title(in_file_name+" fitted by "+in_model_name));
        #rdataset_MC.plotOn( mplot2 ,RooFit.DataError(ROOT.RooAbsData.SumW2) );
        #model.plotOn( mplot2, RooFit.VisualizeError(rfresult,1),RooFit.FillColor(ROOT.kOrange) );
        #rdataset_MC.plotOn( mplot2 ,RooFit.DataError(ROOT.RooAbsData.SumW2) );
        #model.plotOn( mplot2 );
        #cMassFit2 = ROOT.TCanvas("cMassFit2","cMassFit2",1000,800);
        #mplot2.Draw();
        #cMassFit2.SaveAs("plots/BDTcut/chi2.png");
        #r_chi2_wgt.Print();
        ##chi2 fit end
    
        ##calculate the area fraction range(60--100)/range(30--200)
        #igx_total=model.createIntegral(ROOT.RooArgSet(rrv_mass_j),RooFit.NormSet(ROOT.RooArgSet(rrv_mass_j)),RooFit.Range("total"));
        #igx_signal=model.createIntegral(ROOT.RooArgSet(rrv_mass_j),RooFit.NormSet(ROOT.RooArgSet(rrv_mass_j)),RooFit.Range("signal"));
        #print "%s: %s"%(parameters_list[-1].GetName, parameters_list[-1].getVal());
        #parameters_list[-1].setVal(parameters_list[-1].getVal()*(1-igx_signal.getVal()/igx_total.getVal()) );
        #print "%s: %s"%(parameters_list[-1].GetName, parameters_list[-1].getVal());
    
        return [rfresult,parameters_list,rdataset_MC];
    
    ######## ++++++++++++++## ---------------------------------------------------
        
    def get_mlvj_dataset(self,in_file_name, label):# to get the shape of m_lvj
    
        # read in tree
        fileIn_name=ROOT.TString(self.file_Directory+in_file_name);
        fileIn = ROOT.TFile(fileIn_name.Data());
        treeIn = fileIn.Get("otree");
        
        # define bdt reader
        listOfTrainingVariables1 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1"];
        bdtSimple = tmvaApplicator( listOfTrainingVariables1, "weights/Wtagger_200to275_simple_BDT.weights.xml");
            
        rrv_mass_j = self.workspace_.var("rrv_mass_j") 
        rrv_mass_lvj = self.workspace_.var("rrv_mass_lvj") 
        rrv_mass_lvj.setBins(52);
        rrv_weight = RooRealVar("rrv_weight","rrv_weight",0. ,1.) 
        rdataset_SideBand_lo  = ROOT.RooDataSet("rdataset"+label+"_SideBand_lo","rdataset"+label+"_SideBand_lo",ROOT.RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        rdataset_SignalRegion = ROOT.RooDataSet("rdataset"+label+"_SignalRegion","rdataset"+label+"_SignalRegion",ROOT.RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        rdataset_SideBand_hi  = ROOT.RooDataSet("rdataset"+label+"_SideBand_hi","rdataset"+label+"_SideBand_hi",ROOT.RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        # make cuts (including mass drop) # create a RooDataSet
        print "N entries: ", treeIn.GetEntries()
        for i in range(treeIn.GetEntries()):
            if i % 10000 == 0: print "i: ",i
            treeIn.GetEntry(i);
    
            discriminantCut = False; 
                
            if self.cutOnMassDrop_ and treeIn.jet_massdrop_pr < 0.25: discriminantCut = True;
            elif not self.cutOnMassDrop_:
                listOfVarVals = [];
                for kk in range(len(listOfTrainingVariables1)):
                    listOfVarVals.append( getattr( treeIn, listOfTrainingVariables1[kk] ) );
                BDTval = bdtSimple.eval( listOfVarVals );
    #            print BDTval;
                if BDTval > 0.0: discriminantCut = True;
            else: discriminantCut = False;
    
            #mass_j_=self.mj_signal_min; mass_j_region_high=self.mj_signal_max;
            #mass_j_region_low=self.mj_sideband_lo_min; mass_j_region_high=self.mj_sideband_lo_max;
            #mass_j_region_low=self.mj_sideband_hi_min; mass_j_region_high=self.mj_sideband_hi_max;
            if treeIn.jet_pt_pr > 200. and discriminantCut and treeIn.jet_mass_pr >= rrv_mass_j.getMin() and treeIn.jet_mass_pr<rrv_mass_j.getMax() and treeIn.njets ==0 and treeIn.mass_lvj >= rrv_mass_lvj.getMin() and treeIn.mass_lvj<rrv_mass_lvj.getMax() :
            #if treeIn.jet_pt_pr > 200. and discriminantCut and treeIn.jet_mass_pr >= rrv_mass_j.getMin() and treeIn.jet_mass_pr<rrv_mass_j.getMax() and treeIn.njets ==0  :
                rrv_mass_lvj.setVal( treeIn.mass_lvj );
                if treeIn.jet_mass_pr >= self.mj_sideband_lo_min and treeIn.jet_mass_pr < self.mj_sideband_lo_max:
                    rdataset_SideBand_lo.add( ROOT.RooArgSet( rrv_mass_lvj ), treeIn.totalEventWeight );
                if treeIn.jet_mass_pr >= self.mj_signal_min      and treeIn.jet_mass_pr < self.mj_signal_max:
                    rdataset_SignalRegion.add( ROOT.RooArgSet( rrv_mass_lvj ), treeIn.totalEventWeight );
                if treeIn.jet_mass_pr >= self.mj_sideband_hi_min and treeIn.jet_mass_pr < self.mj_sideband_hi_max:
                    rdataset_SideBand_hi.add( ROOT.RooArgSet( rrv_mass_lvj ), treeIn.totalEventWeight );
                
        rdataset_SideBand_lo.Print();
        rdataset_SignalRegion.Print();
        rdataset_SideBand_hi.Print();
        getattr(self.workspace_,"import")(rdataset_SideBand_lo);
        getattr(self.workspace_,"import")(rdataset_SignalRegion);
        getattr(self.workspace_,"import")(rdataset_SideBand_hi);
        rdataset_SignalRegion.Print()
        self.file_out.write("\n%s events number: %s"%(label,rdataset_SignalRegion.sumEntries()))
        #raw_input( 'Press ENTER to continue\n ' )


     ######## ++++++++++++++## ---------------------------------------------------
        
    def fit_mlvj_shape_single_MC_sample(self,in_file_name, label, in_range, in_model_name):# to get the shape of m_lvj
    
        rrv_mass_lvj = self.workspace_.var("rrv_mass_lvj") 
        #dataset
        rdataset = self.workspace_.data("rdataset"+label+"_"+in_range); 
        rdataset.Print();
        #model function
        model = self.make_Pdf(label+in_range,in_model_name,"mlvj");
    
        rfresult = model.fitTo( rdataset, RooFit.Save(1), RooFit.SumW2Error(kTRUE));
        
        mplot = rrv_mass_lvj.frame(RooFit.Title("M_{lvj_"+in_range+"} fitted by "+in_model_name));
        rdataset.plotOn( mplot ,RooFit.DataError(ROOT.RooAbsData.SumW2) );
        model.plotOn( mplot, RooFit.VisualizeError(rfresult,1),RooFit.FillColor(ROOT.kOrange) );
        #model.plotOn(mplot,RooFit.VisualizeError(rfresult,1,kFALSE),RooFit.DrawOption("F"),RooFit.FillColor(ROOT.kOrange));
        rdataset.plotOn( mplot ,RooFit.DataError(ROOT.RooAbsData.SumW2) );
        model.plotOn( mplot );
        #pull
        hpull=mplot.pullHist();
        mplot_pull = rrv_mass_lvj.frame(RooFit.Title("Pull Distribution"));
        mplot_pull.addPlotable(hpull,"P");
        mplot_pull.SetTitle("PULL");
        mplot_pull.GetYaxis().SetRangeUser(-5,5);
         
        parameters_list=model.getParameters(rdataset);
        self.draw_canvas( mplot, mplot_pull,parameters_list,"plots/m_lvj_BDTcut/", in_file_name,"_m_lvj"+in_range+in_model_name)
        rfresult.Print();

        # fix the shape
        par=parameters_list.createIterator();
        par.Reset();
        param=par.Next()
        while param:
            param.setConstant(kTRUE)
            param=par.Next();


        return model;
  
    ######## ++++++++++++++

    def fit_mlvj_model_single_MC_sample(self,in_file_name, label, in_range, in_model_name):# model = shape + normalization
    
        rrv_mass_lvj = self.workspace_.var("rrv_mass_lvj") 
        #dataset
        rdataset = self.workspace_.data("rdataset"+label+"_"+in_range); 
        rdataset.Print();
        #model function
        model = self.make_Model(label+in_range,in_model_name,"mlvj");
        model.Print()
        #raw_input( 'Press ENTER to continue\n ' )
        rfresult = model.fitTo( rdataset, RooFit.Save(1), RooFit.SumW2Error(kTRUE) ,RooFit.Extended(kTRUE) );
        
        mplot = rrv_mass_lvj.frame(RooFit.Title("M_{lvj_"+in_range+"} fitted by "+in_model_name));
        rdataset.plotOn( mplot ,RooFit.DataError(ROOT.RooAbsData.SumW2) );
        model.plotOn( mplot, RooFit.VisualizeError(rfresult,1),RooFit.FillColor(ROOT.kOrange) );
        #model.plotOn(mplot,RooFit.VisualizeError(rfresult,1,kFALSE),RooFit.DrawOption("F"),RooFit.FillColor(ROOT.kOrange));
        rdataset.plotOn( mplot ,RooFit.DataError(ROOT.RooAbsData.SumW2) );
        model.plotOn( mplot );
        #pull
        hpull=mplot.pullHist();
        mplot_pull = rrv_mass_lvj.frame(RooFit.Title("Pull Distribution"));
        mplot_pull.addPlotable(hpull,"P");
        mplot_pull.SetTitle("PULL");
        mplot_pull.GetYaxis().SetRangeUser(-5,5);
         
        parameters_list=model.getParameters(rdataset);
        self.draw_canvas( mplot, mplot_pull,parameters_list,"plots/m_lvj_BDTcut/", in_file_name,"_m_lvj"+in_range+in_model_name)
        rfresult.Print();

        return model;
    ######## ++++++++++++++
    
    def fit_alpha_WJets(self):# get the shape of WJets in sblo, sbhi, and signal region. fit to get alpha
        self.get_mlvj_dataset(self.file_WJets_mc,"_WJets_lvj")# to get the shape of m_lvj
        model_WJets_sblo=self.fit_mlvj_shape_single_MC_sample(self.file_WJets_mc,"_WJets_lvj","SideBand_lo","ErfExp");
        model_WJets_sbhi=self.fit_mlvj_shape_single_MC_sample(self.file_WJets_mc,"_WJets_lvj","SideBand_hi","ErfExp");
        #model_WJets_signal=self.fit_mlvj_shape_single_MC_sample(self.file_WJets_mc,"_WJets_lvj","SignalRegion","ErfExp");

        #dataset
        rdataset = self.workspace_.data("rdataset_WJets_lvj_SignalRegion"); 
        alpha=RooRealVar("alpha","alpha",0.5,0.,1.);
        getattr(self.workspace_,"import")(alpha)
        model_WJets_signal=RooAddPdf("model_WJets_signal","model_WJets_signal",RooArgList(model_WJets_sblo,model_WJets_sbhi),RooArgList(alpha));
        rfresult=model_WJets_signal.fitTo(rdataset, RooFit.Save(1), RooFit.SumW2Error(kTRUE));

        rrv_mass_lvj = self.workspace_.var("rrv_mass_lvj")
        mplot = rrv_mass_lvj.frame(RooFit.Title("M_{lvj_SignalRegion} fitted by #alpha*M_{lvj_sblo} + (1-#alpha)*M_{lvj_sbhi}"));
        rdataset.plotOn( mplot ,RooFit.DataError(ROOT.RooAbsData.SumW2) );
        model_WJets_signal.plotOn( mplot, RooFit.VisualizeError(rfresult,1),RooFit.FillColor(ROOT.kOrange) );
        #model_WJets_signal.plotOn(mplot,RooFit.VisualizeError(rfresult,1,kFALSE),RooFit.DrawOption("F"),RooFit.FillColor(ROOT.kOrange));
        rdataset.plotOn( mplot ,RooFit.DataError(ROOT.RooAbsData.SumW2) );
        model_WJets_signal.plotOn( mplot );
        #model_WJets_signal.plotOn( mplot, RooFit.Components("model_WJets_sblo"), RooFit.LineStyle(RooFit.kDashed),RooFit.LineColor(ROOT.kBlack) );
        #model_WJets_signal.plotOn( mplot, RooFit.Components("model_WJets_sbhi"), RooFit.LineStyle(RooFit.kDashed),RooFit.LineColor(ROOT.kRed) );
        #pull
        hpull=mplot.pullHist();
        mplot_pull = rrv_mass_lvj.frame(RooFit.Title("Pull Distribution"));
        mplot_pull.addPlotable(hpull,"P");
        mplot_pull.SetTitle("PULL");
        mplot_pull.GetYaxis().SetRangeUser(-5,5);
        parameters_list=model_WJets_signal.getParameters(rdataset);
        #self.draw_canvas( mplot, mplot_pull,parameters_list,"plots/m_lvj_BDTcut/", "m_lvj_signal")
        self.draw_canvas( mplot, mplot_pull,parameters_list,"plots/m_lvj_BDTcut/", self.file_WJets_mc)

    ######## ++++++++++++++
    def fit_WJetsNormalization_in_MjSignalRegion(self, inject_signal=0): # to  get the normalization of WJets in signal region
        self.fit_m_j_single_MC_sample(self.file_TTB_mc,"_TTB","ErfExpGaus");
        self.fit_m_j_single_MC_sample(self.file_WW_mc,"_WW","Voig");
        self.fit_m_j_single_MC_sample(self.file_WJets_mc,"_WJets","ErfExp");
        self.fit_m_j_single_MC_sample(self.file_ggH600,"_ggH600","Voig");
    
        fileIn_name=[TString(self.file_Directory+self.file_WW_mc),TString(self.file_Directory+self.file_TTB_mc),TString(self.file_Directory+self.file_WJets_mc), TString(self.file_Directory+self.file_ggH600), TString(self.file_Directory+self.file_data)];
    
        listOfTrainingVariables1 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1"];
        bdtSimple = tmvaApplicator( listOfTrainingVariables1, "weights/Wtagger_200to275_simple_BDT.weights.xml");
    
        rrv_mass_j = self.workspace_.var("rrv_mass_j") 
        rrv_mass_j.setBins(55);
        rrv_mass_lvj = self.workspace_.var("rrv_mass_lvj") 
        rrv_weight = RooRealVar("rrv_weight","rrv_weight",0. ,1.) 
        rdataset_Total_mj = ROOT.RooDataSet("rdataset_Total_mj","rdataset_Total_mj",ROOT.RooArgSet(rrv_mass_j,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
    
        label="_Total"
        hnum_3region=TH1F("hnum_3region"+label,"hnum_3region"+label,4,-1.5,2.5);
        #prepare the dataset: WJets+TTB+WW
        for j in range(3+inject_signal): #closure test
        #for j in range(4,5):# true data
            fileIn = ROOT.TFile(fileIn_name[j].Data());
            treeIn = fileIn.Get("otree");
            mc_scale=1.0;# for background MC, mc_scale=1; for signal MC, mc_scale=50
            if j==3: mc_scale=50.0;
            # make cuts (including mass drop) # create a RooDataSet
            print "N entries: ", treeIn.GetEntries()
            for i in range(treeIn.GetEntries()):
                if i % 10000 == 0: print "i: ",i
                treeIn.GetEntry(i);
                discriminantCut = False; 
                    
                if self.cutOnMassDrop_ and treeIn.jet_massdrop_pr < 0.25: discriminantCut = True;
                elif not self.cutOnMassDrop_:
                    listOfVarVals = [];
                    for kk in range(len(listOfTrainingVariables1)):
                        listOfVarVals.append( getattr( treeIn, listOfTrainingVariables1[kk] ) );
                    BDTval = bdtSimple.eval( listOfVarVals );
                    #print BDTval;
                    if BDTval > 0.0: discriminantCut = True;
                else: discriminantCut = False;
                
                #if treeIn.jet_pt_pr > 200. and discriminantCut and treeIn.jet_mass_pr > 30 and treeIn.jet_mass_pr<140:
                #if treeIn.njets==0 and treeIn.nbjets>0 : print "jets num= %s, %s"%(treeIn.njets,treeIn.nbjets);
                if treeIn.jet_pt_pr > 200. and discriminantCut and treeIn.jet_mass_pr >= rrv_mass_j.getMin() and treeIn.jet_mass_pr<rrv_mass_j.getMax() and treeIn.mass_lvj >= rrv_mass_lvj.getMin() and treeIn.mass_lvj<rrv_mass_lvj.getMax() and treeIn.njets == 0:
                    rrv_mass_j.setVal( treeIn.jet_mass_pr );
                    rdataset_Total_mj.add( ROOT.RooArgSet( rrv_mass_j ), treeIn.totalEventWeight/mc_scale );
                    if treeIn.jet_mass_pr >=self.mj_sideband_lo_min and treeIn.jet_mass_pr <self.mj_sideband_lo_max: hnum_3region.Fill(-1,treeIn.totalEventWeight/mc_scale );
                    if treeIn.jet_mass_pr >=self.mj_signal_min      and treeIn.jet_mass_pr <self.mj_signal_max     : hnum_3region.Fill(0,treeIn.totalEventWeight/mc_scale);
                    if treeIn.jet_mass_pr >=self.mj_sideband_hi_min and treeIn.jet_mass_pr <self.mj_sideband_hi_max: hnum_3region.Fill(1,treeIn.totalEventWeight/mc_scale); 
                    hnum_3region.Fill(2,treeIn.totalEventWeight/mc_scale);
        rrv_number_Total=RooRealVar("rrv_number"+label+"mj","rrv_number"+label+"mj",hnum_3region.GetBinContent(4));
        rrv_number_sblo=RooRealVar("rrv_number_sblo"+label+"mj","rrv_number_sblo"+label+"mj",hnum_3region.GetBinContent(1));
        rrv_number_signal=RooRealVar("rrv_number_signal"+label+"mj","rrv_number_signal"+label+"mj",hnum_3region.GetBinContent(2));
        rrv_number_sbhi=RooRealVar("rrv_number_sbhi"+label+"mj","rrv_number_sbhi"+label+"mj",hnum_3region.GetBinContent(3));
        getattr(self.workspace_,"import")(rrv_number_Total)
        getattr(self.workspace_,"import")(rrv_number_sblo)
        getattr(self.workspace_,"import")(rrv_number_signal)
        getattr(self.workspace_,"import")(rrv_number_sbhi)
        print "N_rdataset: ", rdataset_Total_mj.Print();
        getattr(self.workspace_,"import")(rdataset_Total_mj)

        model_TTB=self.get_TTB_mj_Model();
        model_WW=self.get_WW_mj_Model();
        model_WJets=self.get_WJets_mj_Model();
        model_Total=RooAddPdf("model_Totalmj","model_Totalmj",RooArgList(model_WJets,model_WW,model_TTB));
        #model_Total.fixCoefRange("ref");
        getattr(self.workspace_,"import")(model_Total)
        # fit the sideband range

        #rfresult = model_Total.fitTo( rdataset_Total_mj, RooFit.Save(1),RooFit.SumCoefRange("ref") , RooFit.Range("sb_lo,sb_hi") ,RooFit.SumW2Error(kTRUE) ,RooFit.Extended(kTRUE) );
        rfresult = model_Total.fitTo( rdataset_Total_mj, RooFit.Save(1) , RooFit.Range("sb_lo,sb_hi") ,RooFit.SumW2Error(kTRUE) ,RooFit.Extended(kTRUE) );

        
        mplot = rrv_mass_j.frame(RooFit.Title("Closure test: WJets+TTBar+WW"));
        rdataset_Total_mj.plotOn( mplot ,RooFit.DataError(ROOT.RooAbsData.SumW2) );
        model_Total.plotOn(mplot,RooFit.VisualizeError(rfresult,1,kFALSE),RooFit.DrawOption("F"),RooFit.FillColor(ROOT.kOrange),RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()));
        rdataset_Total_mj.plotOn( mplot ,RooFit.DataError(ROOT.RooAbsData.SumW2) );
        model_Total.plotOn(mplot );
        #DrawOption("LF"), FillStyle(1001), FillColor(DibosonColor)
        #model_Total.plotOn(mplot, RooFit.Components("model_WJetsmj"),RooFit.LineStyle(RooFit.kDashed),RooFit.LineColor(ROOT.kBlack),RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()) );
        #model_Total.plotOn(mplot, RooFit.Components("model_WWmj"),RooFit.LineStyle(RooFit.kDashed),RooFit.LineColor(ROOT.kRed),RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()));
        #model_Total.plotOn(mplot, RooFit.Components("model_TTBmj"),RooFit.LineStyle(RooFit.kDashed),RooFit.LineColor(6),RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()));
        model_Total.plotOn(mplot, RooFit.Components("model_WWmj"),RooFit.LineColor(kAzure+8),RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()) );
        model_Total.plotOn(mplot, RooFit.Components("model_TTBmj"), RooFit.LineColor(kGreen),RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()) );
        model_Total.plotOn(mplot, RooFit.Components("model_WJetsmj"), RooFit.LineColor(kRed),RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()) );
        model_Total.plotOn( mplot );
        model_Total.plotOn( mplot, RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()),RooFit.LineStyle(ROOT.kDashed) );
    
        #pull
        hpull=mplot.pullHist();
        mplot_pull = rrv_mass_j.frame(RooFit.Title("Pull Distribution"));
        mplot_pull.addPlotable(hpull,"P");
        mplot_pull.SetTitle("PULL");
        mplot_pull.GetYaxis().SetRangeUser(-5,5);
    
        #draw line
        lowerLine = TLine(self.mj_signal_min,0.,self.mj_signal_min,mplot.GetMaximum()); lowerLine.SetLineWidth(2); lowerLine.SetLineColor(kGray+2); lowerLine.SetLineStyle(9);
        upperLine = TLine(self.mj_signal_max,0.,self.mj_signal_max,mplot.GetMaximum()); upperLine.SetLineWidth(2); upperLine.SetLineColor(kGray+2); upperLine.SetLineStyle(9);
        mplot.addObject(lowerLine);
        mplot.addObject(upperLine);
        #TLegend
        #legend=self.legend4Plot(mplot,1);
        #mplot.GetYaxis().SetTitle("")
        
        parameters_list=model_Total.getParameters(rdataset_Total_mj);
        if inject_signal: self.draw_canvas( mplot, mplot_pull,parameters_list,"plots/m_j_sideband_BDTcut/", "m_j_sideband_inject_signal","",1)
        else: self.draw_canvas( mplot, mplot_pull,parameters_list,"plots/m_j_sideband_BDTcut/", "m_j_sideband_not_inject_signal","",1)

        rfresult.Print();

        self.get_normalization("_Total");
        self.get_normalization("_TTB");
        self.get_normalization("_WW");
        self.get_normalization("_WJets");

        # to calculate the WJets's normalization in M_J signal-region
        #model_WJets = self.workspace_.pdf("model_WJetsmj");

        fullInt   = model_WJets.createIntegral(RooArgSet(rrv_mass_j),RooArgSet(rrv_mass_j) );
        signalInt = model_WJets.createIntegral(RooArgSet(rrv_mass_j),RooArgSet(rrv_mass_j),("signal"));
        fullInt_val=fullInt.getVal()
        signalInt_val=signalInt.getVal()/fullInt_val
        rrv_number_WJets_in_mj_SignalRegion_from_fitting=RooRealVar("rrv_number_WJets_in_mj_SignalRegion_from_fitting","rrv_number_WJets_in_mj_SignalRegion_from_fitting",self.workspace_.var("rrv_number_WJetsmj").getVal()*signalInt_val);
        getattr(self.workspace_,"import")(rrv_number_WJets_in_mj_SignalRegion_from_fitting)
        rrv_number_WJets_in_mj_SignalRegion_from_fitting.Print();

        raw_input("WJets normalization over! Plean ENTER to continue!");

    ######## ++++++++++++++
    def fit_mlvj_in_MjSignalRegion(self, inject_signal=0): # fix other background's model and  WJets normalization, floating WJets shape
        self.fit_Signal()
        self.fit_WJets()
        self.fit_WW()
        self.fit_TTB()
        #raw_input("Fit all MC samples! Plean ENTER to continue!");


        fileIn_name=[TString(self.file_Directory+self.file_WW_mc),TString(self.file_Directory+self.file_TTB_mc),TString(self.file_Directory+self.file_WJets_mc), TString(self.file_Directory+self.file_ggH600), TString(self.file_Directory+self.file_data)];
    
        listOfTrainingVariables1 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1"];
        bdtSimple = tmvaApplicator( listOfTrainingVariables1, "weights/Wtagger_200to275_simple_BDT.weights.xml");
    
        rrv_mass_j = self.workspace_.var("rrv_mass_j") 
        rrv_mass_lvj = self.workspace_.var("rrv_mass_lvj") 
        rrv_mass_lvj.setBins(52);
        rrv_weight = RooRealVar("rrv_weight","rrv_weight",0. ,1.) 
        rdataset_Total_mlvj = ROOT.RooDataSet("rdataset_Total_mlvj","rdataset_Total_mlvj",ROOT.RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
    
        #prepare the dataset: WJets+TTB+WW
        for j in range(3+inject_signal): #closuer test
        #for j in range(4,5):# true data
            fileIn = ROOT.TFile(fileIn_name[j].Data());
            treeIn = fileIn.Get("otree");
            # make cuts (including mass drop) # create a RooDataSet
            print "N entries: ", treeIn.GetEntries()
            mc_scale=1.0;# for background MC, mc_scale=1; for signal MC, mc_scale=50
            if j==3: mc_scale=50.0;
            for i in range(treeIn.GetEntries()):
                if i % 10000 == 0: print "i: ",i
                treeIn.GetEntry(i);
                discriminantCut = False; 
                    
                if self.cutOnMassDrop_ and treeIn.jet_massdrop_pr < 0.25: discriminantCut = True;
                elif not self.cutOnMassDrop_:
                    listOfVarVals = [];
                    for kk in range(len(listOfTrainingVariables1)):
                        listOfVarVals.append( getattr( treeIn, listOfTrainingVariables1[kk] ) );
                    BDTval = bdtSimple.eval( listOfVarVals );
                    #print BDTval;
                    if BDTval > 0.0: discriminantCut = True;
                else: discriminantCut = False;
                
                if treeIn.jet_pt_pr > 200. and discriminantCut and treeIn.jet_mass_pr >= self.mj_signal_min  and treeIn.jet_mass_pr < self.mj_signal_max and treeIn.mass_lvj >= rrv_mass_lvj.getMin() and treeIn.mass_lvj<rrv_mass_lvj.getMax() and treeIn.njets == 0:
                    rrv_mass_lvj.setVal( treeIn.mass_lvj );
                    rdataset_Total_mlvj.add( ROOT.RooArgSet( rrv_mass_lvj ), treeIn.totalEventWeight/mc_scale );
        print "N_rdataset: ", rdataset_Total_mlvj.Print();
        self.file_out.write("\ndata_obs event number: %s\n"%(rdataset_Total_mlvj.sumEntries()) )
        #raw_input("Fit all MC samples! Plean ENTER to continue!");
        getattr(self.workspace_,"import")(rdataset_Total_mlvj)
        #prepare Limit: data_obs
        #getattr(self.workspace4limit_,"import")(rdataset_Total_mlvj, RooFit.Rename("data_obs"))
        getattr(self.workspace4limit_,"import")(rdataset_Total_mlvj.Clone("data_obs"))

        model_TTB   = self.get_TTB_mlvj_Model();
        model_WW    = self.get_WW_mlvj_Model();
        model_WJets = self.get_WJets_mlvj_Model();
        model_ggH   = self.get_ggH_mlvj_Model();
        model_TTB.Print();
        model_WW.Print();
        model_WJets.Print();
        #prepare for Limit
        #getattr(self.workspace4limit_,"import")(model_WJets, RooFit.Rename("WJets"))
        #getattr(self.workspace4limit_,"import")(model_WW, RooFit.Rename("WW"))
        #getattr(self.workspace4limit_,"import")(model_TTB, RooFit.Rename("TTbar"))
        #getattr(self.workspace4limit_,"import")(model_ggH, RooFit.Rename("ggH600"))

        getattr(self.workspace4limit_,"import")(self.workspace_.pdf("model_raw_TTB_lvjSignalRegionmlvj").clone("TTbar"))
        getattr(self.workspace4limit_,"import")(self.workspace_.pdf("model_raw_WJets_lvjSignalRegionmlvj").clone("WJets"))
        getattr(self.workspace4limit_,"import")(self.workspace_.pdf("model_raw_WW_lvjSignalRegionmlvj").clone("WW"))
        getattr(self.workspace4limit_,"import")(self.workspace_.pdf("model_raw_ggH600_lvjSignalRegionmlvj").clone("ggH600"))

        #raw_input( 'Press ENTER to continue\n ' ) 
        model_Total=RooAddPdf("model_Totalmlvj","model_Totalmlvj",RooArgList(model_WJets,model_WW,model_TTB));
        #model_Total.fixCoefRange("ref");
        getattr(self.workspace_,"import")(model_Total)

        rfresult = model_Total.fitTo( rdataset_Total_mlvj, RooFit.Save(1) ,RooFit.SumW2Error(kTRUE) ,RooFit.Extended(kTRUE) );
        
        mplot = rrv_mass_lvj.frame(RooFit.Title("Closure test: WJets+TTBar+WW"));
        rdataset_Total_mlvj.plotOn( mplot ,RooFit.DataError(ROOT.RooAbsData.SumW2) );
        model_Total.plotOn(mplot,RooFit.VisualizeError(rfresult,1,kFALSE),RooFit.DrawOption("F"),RooFit.FillColor(ROOT.kOrange));
        rdataset_Total_mlvj.plotOn( mplot ,RooFit.DataError(ROOT.RooAbsData.SumW2) );
        model_Total.plotOn(mplot );
        #model_Total.plotOn(mplot, RooFit.Components("model_WJetsmj"),RooFit.LineStyle(RooFit.kDashed),RooFit.LineColor(ROOT.kBlack),RooFit.Range(rrv_mass_lvj.getMin(),rrv_mass_lvj.getMax()) );
        #model_Total.plotOn(mplot, RooFit.Components("model_WWmj"),RooFit.LineStyle(RooFit.kDashed),RooFit.LineColor(ROOT.kRed),RooFit.Range(rrv_mass_lvj.getMin(),rrv_mass_lvj.getMax()));
        #model_Total.plotOn(mplot, RooFit.Components("model_TTBmj"),RooFit.LineStyle(RooFit.kDashed),RooFit.LineColor(6),RooFit.Range(rrv_mass_lvj.getMin(),rrv_mass_lvj.getMax()));
        model_Total.plotOn(mplot, RooFit.Components("model_WW_lvjSignalRegionmlvj"),RooFit.LineColor(kAzure+8));
        model_Total.plotOn(mplot, RooFit.Components("model_TTB_lvjSignalRegionmlvj"), RooFit.LineColor(kGreen));
        model_Total.plotOn(mplot, RooFit.Components("model_WJets_lvjSignalRegionmlvj"), RooFit.LineColor(kRed));
        model_Total.plotOn( mplot );
        model_Total.plotOn( mplot, RooFit.Range(rrv_mass_lvj.getMin(),rrv_mass_lvj.getMax()),RooFit.LineStyle(ROOT.kDashed) );
    
        #pull
        hpull=mplot.pullHist();
        mplot_pull = rrv_mass_lvj.frame(RooFit.Title("Pull Distribution"));
        mplot_pull.addPlotable(hpull,"P");
        mplot_pull.SetTitle("PULL");
        mplot_pull.GetYaxis().SetRangeUser(-5,5);
    
        #draw line
        #TLegend
        #legend=self.legend4Plot(mplot,1);
        #mplot.GetYaxis().SetTitle("")
        
        parameters_list=model_Total.getParameters(rdataset_Total_mlvj);
        if inject_signal: self.draw_canvas( mplot, mplot_pull,parameters_list,"plots/m_lvj_BDTcut/", "m_lvj_total_inject_signal","",1)
        else: self.draw_canvas( mplot, mplot_pull,parameters_list,"plots/m_lvj_BDTcut/", "m_lvj_total_not_inject_signal","",1)

        rfresult.Print();

    ######## ++++++++++++++
    def get_normalization(self, label):
        print "________________________________________________________________________________________________"
        print "get normalization"
        model = self.workspace_.pdf("model"+label+"mj");
        rrv_mass_j = self.workspace_.var("rrv_mass_j");

        fullInt   = model.createIntegral(RooArgSet(rrv_mass_j),RooArgSet(rrv_mass_j) );
        sbloInt   = model.createIntegral(RooArgSet(rrv_mass_j),RooArgSet(rrv_mass_j),("sb_lo"));
        signalInt = model.createIntegral(RooArgSet(rrv_mass_j),RooArgSet(rrv_mass_j),("signal"));
        sbhiInt   = model.createIntegral(RooArgSet(rrv_mass_j),RooArgSet(rrv_mass_j),("sb_hi"));
        
        fullInt_val=fullInt.getVal()
        sbloInt_val=sbloInt.getVal()/fullInt_val
        sbhiInt_val=sbhiInt.getVal()/fullInt_val
        signalInt_val=signalInt.getVal()/fullInt_val

        print label+"sbloInt=%s"%(sbloInt_val)
        print label+"signalInt=%s"%(signalInt_val)
        print label+"sbhiInt=%s"%(sbhiInt_val)

        print "Events Number in MC Dataset:"
        self.workspace_.var("rrv_number_sblo"+label+"mj").Print();
        self.workspace_.var("rrv_number_signal"+label+"mj").Print();
        self.workspace_.var("rrv_number_sbhi"+label+"mj").Print();

        print "Events Number get from fit:"
        rrv_tmp=self.workspace_.var("rrv_number"+label+"mj");
        rrv_tmp.Print();
        print "Events Number in sideband_low :%s"%(rrv_tmp.getVal()*sbloInt_val)
        print "Events Number in Signal Region:%s"%(rrv_tmp.getVal()*signalInt_val)
        print "Events Number in sideband_high:%s"%(rrv_tmp.getVal()*sbhiInt_val)
        print "Total Number in sidebands     :%s"%(rrv_tmp.getVal()*(sbloInt_val+sbhiInt_val)  )
        print "Ratio signal/sidebands        :%s"%(signalInt_val/(sbloInt_val+sbhiInt_val)  )

        #save to file
        self.file_out.write( "\n%s++++++++++++++++++++++++++++++++++++"%(label) )
        self.file_out.write( "\nEvents Number get from fit:")
        self.file_out.write( "\nEvents Number in sideband_low :%s"%(rrv_tmp.getVal()*sbloInt_val) )
        self.file_out.write( "\nEvents Number in Signal Region:%s"%(rrv_tmp.getVal()*signalInt_val) )
        self.file_out.write( "\nEvents Number in sideband_high:%s"%(rrv_tmp.getVal()*sbhiInt_val) )
        self.file_out.write( "\nTotal Number in sidebands     :%s"%(rrv_tmp.getVal()*(sbloInt_val+sbhiInt_val)  ) )
        self.file_out.write( "\nRatio signal/sidebands        :%s"%(signalInt_val/(sbloInt_val+sbhiInt_val)  ) )
        
        #self.workspace_.var("rrv_number"+label+"mlvj").Print();
    ######## ++++++++++++++
    def read_workspace(self,filename="tmp_workspace.root"):
        #file = TFile(filename) ;
        file = TFile(self.file_rlt_root) ;
        self.workspace_ = file.Get("workspace_") ;

    ######## ++++++++++++++
    def save_workspace(self,filename="tmp_workspace.root"):
        #self.workspace_.writeToFile(filename);
        self.workspace_.writeToFile(self.file_rlt_root);
    ######## ++++++++++++++
    def save_for_limit(self):
        self.workspace4limit_.Print()
        self.workspace4limit_.writeToFile(self.file_rlt_root);
        self.file_out.close()
    ######## ++++++++++++++
    def legend4Plot(self, plot, left):
        if left: 
            theLeg = TLegend(0.2, 0.62, 0.55, 0.92, "", "NDC");
        else:
            theLeg = TLegend(0.65, 0.62, 0.92, 0.92, "", "NDC");
        theLeg.SetName("theLegend");
        theLeg.SetBorderSize(0);
        theLeg.SetLineColor(0);
        theLeg.SetFillColor(0);
        theLeg.SetFillStyle(0);
        theLeg.SetLineWidth(0);
        theLeg.SetLineStyle(0);
        theLeg.SetTextFont(42);
        theLeg.SetTextSize(.045);
        
        entryCnt = 0;
        for obj in range(plot.numItems()):
            objName = plot.nameOf(obj);
            if not (plot.getInvisible(objName)): 
                theObj = plot.getObject(obj);
                objTitle = theObj.GetTitle();
                if objTitle.Length() < 1:
                    objTitle = objName;
                    theLeg.AddEntry(theObj, objTitle, plot.getDrawOptions(objName));
                    entryCnt=entryCnt+1;

        theLeg.SetY1NDC(0.9 - 0.05*entryCnt - 0.005);
        theLeg.SetY1(theLeg.GetY1NDC());
        return theLeg;

    ######## ++++++++++++++
    def draw_canvas(self, mplot, mplot_pull,parameters_list,in_directory, in_file_name, in_model_name="", show_constant_parameter=0):
        cMassFit = ROOT.TCanvas("cMassFit","cMassFit",1000,800);
        pad1=ROOT.TPad("pad1","pad1",0.,0. ,0.8,0.2);
        pad2=ROOT.TPad("pad2","pad2",0.,0.2,0.8,1. );
        pad3=ROOT.TPad("pad3","pad3",0.8,0.,1,1);
        pad1.Draw();
        pad2.Draw();
        pad3.Draw();

        pad2.cd();
        mplot.Draw();
        pad1.cd();
        mplot_pull.Draw();

        pad3.cd();
        latex=ROOT.TLatex();
        latex.SetTextSize(0.1);
        par=parameters_list.createIterator();
        par.Reset();
        param=par.Next()
        i=0;
        while param:
            if (not  param.isConstant() ) or show_constant_parameter:
                param.Print();
                icolor=1;#if a paramenter is constant, color is 2
                if param.isConstant(): icolor=2
                latex.DrawLatex(0,0.9-i*0.08,"#color[%s]{%s}"%(icolor,param.GetName()) );
                latex.DrawLatex(0,0.9-i*0.08-0.04," #color[%s]{%4.3e +/- %2.1e}"%(icolor,param.getVal(),param.getError()) );
                i=i+1;
            param=par.Next();
        #mplot.Draw();


        Directory=TString(in_directory);
        if not Directory.EndsWith("/"):Directory=Directory.Append("/");
        if not os.path.isdir(Directory.Data()): os.system("mkdir -p  "+Directory.Data());

        rlt_file=ROOT.TString(Directory.Data()+in_file_name);
        if rlt_file.EndsWith(".root"):
            rlt_file.ReplaceAll(".root","_"+in_model_name+"_rlt_weight.png");
        else:
            rlt_file=rlt_file.Append("_"+in_model_name+"_rlt_weight.png");
        cMassFit.SaveAs(rlt_file.Data());
        rlt_file.ReplaceAll(".png",".eps"); 
        cMassFit.SaveAs(rlt_file.Data());
    ######## ++++++++++++++
    def fit_data(self):
        print "fit_data"
        self.fit_m_j_single_MC_sample(self.file_data,"_data","ErfExpGaus");
        self.get_mlvj_dataset(self.file_data,"_data_lvj")# to get the shape of m_lvj
        #self.fit_mlvj_model_single_MC_sample(self.file_data,"_data_lvj","SideBand_lo","ErfExp");
        #self.fit_mlvj_model_single_MC_sample(self.file_data,"_data_lvj","SideBand_hi","ErfExp");
        self.fit_mlvj_model_single_MC_sample(self.file_data,"_data_lvj","SignalRegion","ErfExp");
        print "________________________________________________________________________"
    ######## ++++++++++++++
    def fit_Signal(self):
        print "fit_Signal"
        #self.fit_m_j_single_MC_sample(self.file_ggH600,"_ggH600","Voig");
        self.get_mlvj_dataset(self.file_ggH600,"_ggH600_lvj")# to get the shape of m_lvj
        #self.fit_mlvj_model_single_MC_sample(self.file_ggH600,"_ggH600_lvj","SideBand_lo","ErfExp");
        #self.fit_mlvj_model_single_MC_sample(self.file_ggH600,"_ggH600_lvj","SideBand_hi","ErfExp");
        self.fit_mlvj_model_single_MC_sample(self.file_ggH600,"_ggH600_lvj","SignalRegion","ErfExpGaus_v1");
        print "________________________________________________________________________"
    ######## ++++++++++++++
    def fit_WJets(self):
        print "fit_WJets"
        self.get_mlvj_dataset(self.file_WJets_mc,"_WJets_lvj")# to get the shape of m_lvj
        self.fit_mlvj_model_single_MC_sample(self.file_WJets_mc,"_WJets_lvj","SignalRegion","ErfExp");
        print "________________________________________________________________________" 
    ######## ++++++++++++++
    def fit_WW(self):
        print "fit_WW"
        self.get_mlvj_dataset(self.file_WW_mc,"_WW_lvj")# to get the shape of m_lvj
        self.fit_mlvj_model_single_MC_sample(self.file_WW_mc,"_WW_lvj","SignalRegion","ErfExp");
        print "________________________________________________________________________"
    ######## ++++++++++++++
    def fit_TTB(self):
        print "fit_TTB"
        self.get_mlvj_dataset(self.file_TTB_mc,"_TTB_lvj")# to get the shape of m_lvj
        self.fit_mlvj_model_single_MC_sample(self.file_TTB_mc,"_TTB_lvj","SignalRegion","ErfExp");
        print "________________________________________________________________________"
    ######## ++++++++++++++
    def fit_AllSamples_Mlvj(self):
        print "fit_AllSamples_Mlvj"
        self.fit_Signal()
        #self.fit_alpha_WJets();
        self.fit_WJets()
        self.fit_WW()
        self.fit_TTB()
        print "________________________________________________________________________" 

def get_WJets_normalization():
    cutOnMassDrop = False;
    boostedW_fitter=doFit_wj_and_wlvj(cutOnMassDrop)
    boostedW_fitter.fit_WJetsNormalization_in_MjSignalRegion();
    boostedW_fitter.save_workspace();

def get_alpha():
    cutOnMassDrop = False;
    boostedW_fitter=doFit_wj_and_wlvj(cutOnMassDrop)
    boostedW_fitter.fit_alpha_WJets();
    boostedW_fitter.save_workspace();

def fit_data():
    cutOnMassDrop = False;
    boostedW_fitter=doFit_wj_and_wlvj(cutOnMassDrop)
    #boostedW_fitter.fit_WJetsNormalization_in_MjSignalRegion();
    boostedW_fitter.fit_data();
    #boostedW_fitter.save_workspace();


def pre_limit(): 
    cutOnMassDrop = False;
    boostedW_fitter=doFit_wj_and_wlvj(cutOnMassDrop)

    inject_signal=0;# 0: not inject_signal; 1: inject_signal
    boostedW_fitter.fit_WJetsNormalization_in_MjSignalRegion(inject_signal);
    boostedW_fitter.fit_mlvj_in_MjSignalRegion(inject_signal)
    boostedW_fitter.save_for_limit();

if __name__ == '__main__':
    #get_WJets_normalization()
    #get_alpha()
    #fit_data()
    pre_limit()

