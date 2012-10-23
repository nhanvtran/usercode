#! /usr/bin/env python
import os
import glob
import math
import array

from ROOT import gROOT, gStyle, gSystem, TLatex, TString, TFile,TLine, TLegend, TH1F, TCanvas, TPad, RooFit, RooArgSet, RooArgList, RooArgSet, RooAbsData, RooAddPdf, RooWorkspace, RooExtendPdf,RooCBShape, RooLandau, RooFFTConvPdf, RooGaussian, RooDataSet, RooBreitWigner, RooVoigtian, RooRealVar, RooDataHist, RooHistPdf, RooGenericPdf, TIter, kTRUE, kFALSE, kGray, kRed, kDashed, kGreen,kAzure, kOrange, kBlack, Form
import subprocess
from subprocess import Popen

from sampleWrapperClass import *
from trainingClass      import *
from BoostedWSamples    import * 
from mvaApplication     import *

gROOT.ProcessLine('.L tdrstyle.C')
ROOT.setTDRStyle()

#ROOT.gSystem.Load("PDFs/RooErfExpPdf_cxx.so")
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

class doFit_wj_and_wlvj:
    def __init__(self, in_cutOnMassDrop):
        print "Begin to fit"

        self.cutOnMassDrop_=in_cutOnMassDrop;

        rrv_mass_j  = RooRealVar("rrv_mass_j","mass_j",30.,140.);
        rrv_mass_lvj= RooRealVar("rrv_mass_lvj","mass_lvj",200.,1500.);

        self.workspace4fit_ = RooWorkspace("workspace4fit_","workspace4fit_");
        getattr(self.workspace4fit_,"import")(rrv_mass_j);
        getattr(self.workspace4fit_,"import")(rrv_mass_lvj);

        #prepare workspace for unbin-Limit
        self.workspace4limit_ = RooWorkspace("workspace4limit_","workspace4limit_");


        self.mj_sideband_lo_min=30;
        self.mj_sideband_lo_max=60;
        self.mj_signal_min=70;
        self.mj_signal_max=95;
        self.mj_sideband_hi_min=100;
        self.mj_sideband_hi_max=140;
        rrv_mass_j.setRange("sb_lo",self.mj_sideband_lo_min,self.mj_sideband_lo_max);
        rrv_mass_j.setRange("signal_region",self.mj_signal_min,self.mj_signal_max); 
        rrv_mass_j.setRange("sb_hi",self.mj_sideband_hi_min,self.mj_sideband_hi_max);

        self.mlvj_signal_min=500
        self.mlvj_signal_max=700
        rrv_mass_lvj.setRange("signal_region",self.mlvj_signal_min,self.mlvj_signal_max); 

        #prepare the data and mc files
        self.file_TTbar_mc=("ofile_TTbar.root");
        self.file_WW_mc=("ofile_WW.root");
        self.file_WJets_mc=("ofile_WJets.root");
        self.file_data=("ofile_data.root");
        self.file_ggH600=("ofile_ggH600.root");
        self.file_Directory="trainingtrees/";

        #result files: The event number, parameters and error write into a txt file. The dataset and pdfs write into a root file
        self.file_rlt_txt ="hwwlvj_data.txt"
        self.file_rlt_root="hwwlvj_workspace.root"
        self.file_datacard_unbin ="hwwlvj_datacard_unbin.txt"
        self.file_datacard_counting ="hwwlvj_datacard_counting.txt"
        
        self.file_out=open(self.file_rlt_txt,"w");
        self.file_out.write("\nWelcome:\n");
        self.file_out.close()
        self.file_out=open(self.file_rlt_txt,"a+");

        #higgs XS scale
        self.higgs_xs_scale=50.;

## ---------------------------------------------------
    def make_Model(self, label, in_model_name, mass_spectrum="_mj"):
        rrv_number = RooRealVar("rrv_number"+label+mass_spectrum,"rrv_number"+label+mass_spectrum,500,1,100000);
        model_pdf  = self.make_Pdf(label,in_model_name,mass_spectrum)
        model = RooExtendPdf("model"+label+mass_spectrum,"model"+label+mass_spectrum, model_pdf, rrv_number );
        rrv_number.Print()
        model.Print()
        #raw_input("ENTER")

        getattr(self.workspace4fit_,"import")(rrv_number)
        getattr(self.workspace4fit_,"import")(model)
        rrv_number.Print()
        #raw_input("Enter to continue");
        return self.workspace4fit_.pdf("model"+label+mass_spectrum)

    def make_Pdf(self, label, in_model_name, mass_spectrum="_mj"):
        if mass_spectrum=="_mj": rrv_x = self.workspace4fit_.var("rrv_mass_j"); 
        if mass_spectrum=="_mlvj": rrv_x = self.workspace4fit_.var("rrv_mass_lvj"); 
        
        if in_model_name == "Voig":
            rrv_mean_voig=RooRealVar("rrv_mean_voig"+label,"rrv_mean_voig"+label,82,78,87);
            rrv_width_voig=RooRealVar("rrv_width_voig"+label,"rrv_width_voig"+label,7.,1,10);
            rrv_sigma_voig=RooRealVar("rrv_sigma_voig"+label,"rrv_sigma_voig"+label,5,1,15);
            model_pdf = RooVoigtian("model_pdf"+label+mass_spectrum,"model_pdf"+label+mass_spectrum, rrv_x,rrv_mean_voig,rrv_width_voig,rrv_sigma_voig);
    
        if in_model_name == "Gaus":
            rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,82,78,87);
            rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label,"rrv_sigma_gaus"+label,7,1,15);
            model_pdf = RooGaussian("model_pdf"+label+mass_spectrum,"model_pdf"+label+mass_spectrum, rrv_x,rrv_mean_gaus,rrv_sigma_gaus);
    
        if in_model_name == "CB":
            rrv_mean_CB=RooRealVar("rrv_mean_CB"+label,"rrv_mean_CB"+label,82,78,87);
            rrv_sigma_CB=RooRealVar("rrv_sigma_CB"+label,"rrv_sigma_CB"+label,5,2,10);
            rrv_alpha_CB=RooRealVar("rrv_alpha_CB"+label,"rrv_alpha_CB"+label,-2,-4,-1);
            rrv_n_CB=RooRealVar("rrv_n_CB"+label,"rrv_n_CB"+label,2,0.,4);
            model_pdf = RooCBShape("model_pdf"+label+mass_spectrum,"model_pdf"+label+mass_spectrum, rrv_x,rrv_mean_CB,rrv_sigma_CB,rrv_alpha_CB,rrv_n_CB);
    
        if in_model_name == "CBBW": # FFT: BreitWigner*CBShape
            rrv_mean_CB=RooRealVar("rrv_mean_CB"+label,"rrv_mean_CB"+label,83.5,80,87);
            rrv_sigma_CB=RooRealVar("rrv_sigma_CB"+label,"rrv_sigma_CB"+label,6,2,10);
            rrv_alpha_CB=RooRealVar("rrv_alpha_CB"+label,"rrv_alpha_CB"+label,-2,-4,-1);
            rrv_n_CB=RooRealVar("rrv_n_CB"+label,"rrv_n_CB"+label,0.5,0.,2);
            rrv_mean_BW=RooRealVar("rrv_mean_BW"+label,"rrv_mean_BW"+label,0);
            rrv_width_BW=RooRealVar("rrv_width_BW"+label,"rrv_width_BW"+label,10,5,20);
            cbshape = RooCBShape("cbshape"+label,"cbshape"+label, rrv_x,rrv_mean_CB,rrv_sigma_CB,rrv_alpha_CB,rrv_n_CB);
            bw = RooBreitWigner("bw"+label,"bw"+label, rrv_x,rrv_mean_BW,rrv_width_BW);
            model_pdf = RooFFTConvPdf("model_pdf"+label+mass_spectrum,"model_pdf"+label+mass_spectrum, rrv_x, cbshape, bw);

        if in_model_name == "LDGaus": # FFT: Landau*Gaus
            rrv_mean_landau=RooRealVar("rrv_mean_landau"+label,"rrv_mean_landau"+label,83.5,80,87);
            rrv_sigma_landau=RooRealVar("rrv_sigma_landau"+label,"rrv_sigma_landau"+label,5,2,10);
            rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,0);
            rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label,"rrv_sigma_gaus"+label,16,10,20);
            landau = RooLandau("landau"+label,"landau"+label, rrv_x,rrv_mean_landau,rrv_sigma_landau);
            gaus = RooBreitWigner("gaus"+label,"gaus"+label, rrv_x,rrv_mean_gaus,rrv_sigma_gaus);
            model_pdf = RooFFTConvPdf("model_pdf"+label+mass_spectrum,"model_pdf"+label+mass_spectrum, rrv_x, landau, gaus);

        if in_model_name == "ErfExp" :
            rrv_c_ErfExp = RooRealVar("rrv_c_ErfExp"+label,"rrv_c_ErfExp"+label,-0.05,-0.1,0.);
            #rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label,"rrv_offset_ErfExp"+label,78.,10.,140.);
            rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label,"rrv_offset_ErfExp"+label,78.,10.,1400.);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label,"rrv_width_ErfExp"+label,30.,10,100.);
            #model_pdf = ROOT.RooErfExpPdf("model_pdf"+label+mass_spectrum,"model_pdf"+label+mass_spectrum,rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp);
            model_pdf = RooGenericPdf("model_pdf"+label+mass_spectrum,"model_pdf"+label+mass_spectrum, "TMath::Exp(%s*%s)*(1.+TMath::Erf((%s-%s)/%s))/2."%(rrv_c_ErfExp.GetName(),rrv_x.GetName(), rrv_x.GetName(),rrv_offset_ErfExp.GetName(), rrv_width_ErfExp.GetName()), RooArgList(rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp) )

        if in_model_name == "ErfExp_v1" : #different init-value and range
            rrv_c_ErfExp = RooRealVar("rrv_c_ErfExp"+label,"rrv_c_ErfExp"+label,-0.005,-0.1,0.);
            #rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label,"rrv_offset_ErfExp"+label,78.,10.,140.);
            rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label,"rrv_offset_ErfExp"+label,500.,300.,800.);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label,"rrv_width_ErfExp"+label,60.,30,100.);
            #model_pdf = ROOT.RooErfExpPdf("model_pdf"+label+mass_spectrum,"model_pdf"+label+mass_spectrum,rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp);
            model_pdf = RooGenericPdf("model_pdf"+label+mass_spectrum,"model_pdf"+label+mass_spectrum, "TMath::Exp(%s*%s)*(1.+TMath::Erf((%s-%s)/%s))/2."%(rrv_c_ErfExp.GetName(),rrv_x.GetName(), rrv_x.GetName(),rrv_offset_ErfExp.GetName(), rrv_width_ErfExp.GetName()), RooArgList(rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp) )
            
        if in_model_name == "ErfExpGaus":
            rrv_c_ErfExp = RooRealVar("rrv_c_ErfExp"+label,"rrv_c_ErfExp"+label,-0.05,-0.2,0.);
            rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label,"rrv_offset_ErfExp"+label,100.,10.,140.);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label,"rrv_width_ErfExp"+label,30.,10,100.);
            rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,82,78,87);
            rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label,"rrv_sigma_gaus"+label,7,1,20);
            rrv_high = RooRealVar("rrv_high"+label,"rrv_high"+label,0.7,0.,1.);
            #erfExp = ROOT.RooErfExpPdf("erfExp"+label,"erfExp"+label,rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp);
            erfExp = RooGenericPdf("erfExp"+label,"erfExp"+label, "TMath::Exp(%s*%s)*(1.+TMath::Erf((%s-%s)/%s))/2."%(rrv_c_ErfExp.GetName(),rrv_x.GetName(), rrv_x.GetName(),rrv_offset_ErfExp.GetName(), rrv_width_ErfExp.GetName()), RooArgList(rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp) )
            gaus = RooGaussian("gaus"+label,"gaus"+label, rrv_x,rrv_mean_gaus,rrv_sigma_gaus);
            model_pdf =RooAddPdf("model_pdf"+label+mass_spectrum,"model_pdf"+label+mass_spectrum,RooArgList(erfExp,gaus),RooArgList(rrv_high))
    
        if in_model_name == "ErfExpGaus_v1":
            rrv_c_ErfExp = RooRealVar("rrv_c_ErfExp"+label,"rrv_c_ErfExp"+label,-0.007,-0.1,0.);
            rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label,"rrv_offset_ErfExp"+label,700.,10.,1400.);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label,"rrv_width_ErfExp"+label,24.,10,150.);
            rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,600,500,700);
            rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label,"rrv_sigma_gaus"+label,70,10,150);
            rrv_high = RooRealVar("rrv_high"+label,"rrv_high"+label,0.1,0.,1.);
            #erfExp = ROOT.RooErfExpPdf("erfExp"+label,"erfExp"+label,rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp);
            erfExp = RooGenericPdf("erfExp"+label,"erfExp"+label, "TMath::Exp(%s*%s)*(1.+TMath::Erf((%s-%s)/%s))/2."%(rrv_c_ErfExp.GetName(),rrv_x.GetName(), rrv_x.GetName(),rrv_offset_ErfExp.GetName(), rrv_width_ErfExp.GetName()), RooArgList(rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp) )
            gaus = RooGaussian("gaus"+label,"gaus"+label, rrv_x,rrv_mean_gaus,rrv_sigma_gaus);
            model_pdf =RooAddPdf("model_pdf"+label+mass_spectrum,"model_pdf"+label+mass_spectrum,RooArgList(erfExp,gaus),RooArgList(rrv_high))
    
        if in_model_name == "ErfExpGaus_v2":
            rrv_c_ErfExp = RooRealVar("rrv_c_ErfExp"+label,"rrv_c_ErfExp"+label,-0.05,-10.,0.);
            rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label,"rrv_offset_ErfExp"+label,100.,10.,140.);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label,"rrv_width_ErfExp"+label,30.,10,100.);
            rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,82,78,87);
            rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label,"rrv_sigma_gaus"+label,7,1,20);
            rrv_high = RooRealVar("rrv_high"+label,"rrv_high"+label,200.,0.,1000.);
            model_pdf = ROOT.RooErfExp_Gaus_Pdf("model_pdf"+label+mass_spectrum,"model_pdf"+label+mass_spectrum, rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp,rrv_mean_gaus,rrv_sigma_gaus,rrv_high );
    
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
            model_pdf = ROOT.RooErfExp_2Gaus_Pdf("model_pdf"+label+mass_spectrum,"model_pdf"+label+mass_spectrum, rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp,rrv_mean_gaus1,rrv_sigma_gaus1,rrv_high1,rrv_mean_gaus2,rrv_sigma_gaus2,rrv_high2 );
    
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
            model_pdf = ROOT.RooErfExp_Voig_Gaus_Pdf("model_pdf"+label+mass_spectrum,"model_pdf"+label+mass_spectrum, rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp,rrv_mean_voig,rrv_width_voig,rrv_sigma_voig,rrv_high1,rrv_mean_gaus,rrv_sigma_gaus,rrv_high2 );

        getattr(self.workspace4fit_,"import")(model_pdf)
        return self.workspace4fit_.pdf("model_pdf"+label+mass_spectrum)
    
## ---------------------------------------------------
    def get_mj_Model(self,label):
        return self.workspace4fit_.pdf("model"+label+"_mj")

## ---------------------------------------------------
    def get_TTbar_mj_Model(self):
        rdataset_MC_TTbar=self.workspace4fit_.data("rdataset_MC_TTbar"+"_mj")
        model_TTbar=self.get_mj_Model("_TTbar");
        rdataset_MC_TTbar.Print()
        model_TTbar.Print()
        parameters_TTbar=model_TTbar.getParameters(rdataset_MC_TTbar);
        par=parameters_TTbar.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
        return self.workspace4fit_.pdf("model_TTbar_mj")

## ---------------------------------------------------
    def get_WW_mj_Model(self):
        rdataset_MC_WW=self.workspace4fit_.data("rdataset_MC_WW"+"_mj")
        model_WW=self.get_mj_Model("_WW");
        parameters_WW=model_WW.getParameters(rdataset_MC_WW);
        par=parameters_WW.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
        return self.workspace4fit_.pdf("model_WW_mj")

## ---------------------------------------------------
    def get_WJets_mj_Model(self):
        rdataset_MC_WJets=self.workspace4fit_.data("rdataset_MC_WJets"+"_mj")
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
        return self.workspace4fit_.pdf("model_WJets_mj")
## ---------------------------------------------------
    def get_mlvj_Model(self,label):
        return self.workspace4fit_.pdf("model"+label+"_signal_region_mlvj")

## ---------------------------------------------------
    def get_TTbar_mlvj_Model(self):
        rdataset_MC_TTbar=self.workspace4fit_.data("rdataset_TTbar_signal_region"+"_mlvj")
        model_TTbar=self.get_mlvj_Model("_TTbar");
        model_TTbar.Print()
        parameters_TTbar=model_TTbar.getParameters(rdataset_MC_TTbar);
        par=parameters_TTbar.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
        #return self.workspace4fit_.pdf("model_TTbar_mj")
        return model_TTbar


## ---------------------------------------------------
    def get_ggH_mlvj_Model(self):
        rdataset_MC_ggH=self.workspace4fit_.data("rdataset_ggH600_signal_region"+"_mlvj")
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
        #return self.workspace4fit_.pdf("model_ggH_mj")
        #raw_input("ENTER ot continue");
        return model_ggH

## ---------------------------------------------------
    def get_WW_mlvj_Model(self):
        rdataset_MC_WW=self.workspace4fit_.data("rdataset_WW_signal_region"+"_mlvj")
        model_WW=self.get_mlvj_Model("_WW");
        model_WW.Print()
        rdataset_MC_WW.Print()
        parameters_WW=model_WW.getParameters(rdataset_MC_WW);
        par=parameters_WW.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
        #return self.workspace4fit_.pdf("model_WW_mj")
        return model_WW

## ---------------------------------------------------
    def get_WJets_mlvj_Model(self):
        print "get_WJets_mlvj_Model"
        rdataset_MC_WJets=self.workspace4fit_.data("rdataset_WJets_signal_region"+"_mlvj")
        model_WJets=self.get_mlvj_Model("_WJets");
        model_WJets.Print()
        rdataset_MC_WJets.Print()
        parameters_WJets=model_WJets.getParameters(rdataset_MC_WJets);
        par=parameters_WJets.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            paraName=TString(param.GetName());
            param.Print();
            if paraName.Contains("rrv_number_WJets"): 
                if self.workspace4fit_.var("rrv_number_WJets_in_mj_signal_region_from_fitting"):
                    self.workspace4fit_.var("rrv_number_WJets_in_mj_signal_region_from_fitting").Print()
                    param.setVal( self.workspace4fit_.var("rrv_number_WJets_in_mj_signal_region_from_fitting").getVal() )
                param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
        #raw_input("ENTER ot continue");
        #return self.workspace4fit_.pdf("model_WJets_mj")
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
            
        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j"); 
        rrv_mass_j.setBins(55);
        rrv_weight = RooRealVar("rrv_weight","rrv_weight",0. ,1.) 
        rdataset_MC = RooDataSet("rdataset_MC"+label+"_mj","rdataset_MC"+label+"_mj",RooArgSet(rrv_mass_j,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        # make cuts (including mass drop) # create a RooDataSet
        print "N entries: ", treeIn.GetEntries()
        hnum_4region=TH1F("hnum_4region"+label,"hnum_4region"+label,4,-1.5,2.5);#-1: sb_lo; 0:signal_region; 1: sb_hi; 2:total
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
                rdataset_MC.add( RooArgSet( rrv_mass_j ), treeIn.totalEventWeight );
                if treeIn.jet_mass_pr >=self.mj_sideband_lo_min and treeIn.jet_mass_pr <self.mj_sideband_lo_max: hnum_4region.Fill(-1,treeIn.totalEventWeight );
                if treeIn.jet_mass_pr >=self.mj_signal_min      and treeIn.jet_mass_pr <self.mj_signal_max     : hnum_4region.Fill(0,treeIn.totalEventWeight);
                if treeIn.jet_mass_pr >=self.mj_sideband_hi_min and treeIn.jet_mass_pr <self.mj_sideband_hi_max: hnum_4region.Fill(1,treeIn.totalEventWeight);
                hnum_4region.Fill(2,treeIn.totalEventWeight);
        rrv_number_dataset_sb_lo=RooRealVar("rrv_number_dataset_sb_lo"+label+"_mj","rrv_number_dataset_sb_lo"+label+"_mj",hnum_4region.GetBinContent(1));
        rrv_number_dataset_signal_region=RooRealVar("rrv_number_dataset_signal_region"+label+"_mj","rrv_number_dataset_signal_region"+label+"_mj",hnum_4region.GetBinContent(2));
        rrv_number_dataset_sb_hi=RooRealVar("rrv_number_dataset_sb_hi"+label+"_mj","rrv_number_dataset_sb_hi"+label+"_mj",hnum_4region.GetBinContent(3));
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_sb_lo)
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_signal_region)
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_sb_hi)
                
        print "N_rdataset_MC: ", rdataset_MC.Print();
        getattr(self.workspace4fit_,"import")(rdataset_MC)

        model = self.make_Model(label,in_model_name);
        # fit to a Model
        rfresult = model.fitTo(rdataset_MC,RooFit.Save(1), RooFit.SumW2Error(kTRUE) ,RooFit.Extended(kTRUE) );
        rfresult = model.fitTo(rdataset_MC,RooFit.Save(1), RooFit.SumW2Error(kTRUE) ,RooFit.Extended(kTRUE) );
        
        mplot = rrv_mass_j.frame(RooFit.Title(in_file_name+" fitted by "+in_model_name));
        rdataset_MC.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) );
        #model.plotOn( mplot, RooFit.VisualizeError(rfresult,1),RooFit.FillColor(kOrange) );
        model.plotOn(mplot,RooFit.VisualizeError(rfresult,1,kFALSE),RooFit.DrawOption("F"),RooFit.FillColor(kOrange));
        rdataset_MC.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) );
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
        #chi2=ROOT.RooChi2Var("chi2","chi2",model,rdataHist,RooFit.DataError(RooAbsData.SumW2));
        #m=ROOT.RooMinuit(chi2);
        #m.migrad();
        #m.hesse();
        #r_chi2_wgt=m.save();
        #mplot2 = rrv_mass_j.frame(RooFit.Title(in_file_name+" fitted by "+in_model_name));
        #rdataset_MC.plotOn( mplot2 ,RooFit.DataError(RooAbsData.SumW2) );
        #model.plotOn( mplot2, RooFit.VisualizeError(rfresult,1),RooFit.FillColor(kOrange) );
        #rdataset_MC.plotOn( mplot2 ,RooFit.DataError(RooAbsData.SumW2) );
        #model.plotOn( mplot2 );
        #cMassFit2 = TCanvas("cMassFit2","cMassFit2",1000,800);
        #mplot2.Draw();
        #cMassFit2.SaveAs("plots/BDTcut/chi2.png");
        #r_chi2_wgt.Print();
        ##chi2 fit end
    
        ##calculate the area fraction range(60--100)/range(30--200)
        #igx_total=model.createIntegral(RooArgSet(rrv_mass_j),RooFit.NormSet(RooArgSet(rrv_mass_j)),RooFit.Range("total"));
        #igx_signal=model.createIntegral(RooArgSet(rrv_mass_j),RooFit.NormSet(RooArgSet(rrv_mass_j)),RooFit.Range("signal_region"));
        #print "%s: %s"%(parameters_list[-1].GetName, parameters_list[-1].getVal());
        #parameters_list[-1].setVal(parameters_list[-1].getVal()*(1-igx_signal.getVal()/igx_total.getVal()) );
        #print "%s: %s"%(parameters_list[-1].GetName, parameters_list[-1].getVal());
    
        return [rfresult,parameters_list,rdataset_MC];
    
    ######## ++++++++++++++## ---------------------------------------------------
        
    def get_mlvj_dataset(self,in_file_name, label):# to get the shape of m_lvj
    
        # read in tree
        fileIn_name=TString(self.file_Directory+in_file_name);
        fileIn = TFile(fileIn_name.Data());
        treeIn = fileIn.Get("otree");
        
        # define bdt reader
        listOfTrainingVariables1 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1"];
        bdtSimple = tmvaApplicator( listOfTrainingVariables1, "weights/Wtagger_200to275_simple_BDT.weights.xml");
            
        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j") 
        rrv_mass_lvj = self.workspace4fit_.var("rrv_mass_lvj") 
        rrv_mass_lvj.setBins(52);
        rrv_weight = RooRealVar("rrv_weight","rrv_weight",0. ,1.) 
        rdataset_sb_lo  = RooDataSet("rdataset"+label+"_sb_lo"+"_mlvj","rdataset"+label+"_sb_lo"+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        rdataset_signal_region = RooDataSet("rdataset"+label+"_signal_region"+"_mlvj","rdataset"+label+"_signal_region"+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        rdataset_sb_hi  = RooDataSet("rdataset"+label+"_sb_hi"+"_mlvj","rdataset"+label+"_sb_hi"+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        # make cuts (including mass drop) # create a RooDataSet
        print "N entries: ", treeIn.GetEntries()
        hnum_2region=TH1F("hnum_2region"+label,"hnum_2region"+label,2,-0.5,1.5);# 0: signal_region; 1: total
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
    
            if treeIn.jet_pt_pr > 200. and discriminantCut and treeIn.jet_mass_pr >= rrv_mass_j.getMin() and treeIn.jet_mass_pr<rrv_mass_j.getMax() and treeIn.njets ==0 and treeIn.mass_lvj >= rrv_mass_lvj.getMin() and treeIn.mass_lvj<rrv_mass_lvj.getMax() :
                rrv_mass_lvj.setVal( treeIn.mass_lvj );
                if treeIn.jet_mass_pr >= self.mj_sideband_lo_min and treeIn.jet_mass_pr < self.mj_sideband_lo_max:
                    rdataset_sb_lo.add( RooArgSet( rrv_mass_lvj ), treeIn.totalEventWeight );
                if treeIn.jet_mass_pr >= self.mj_signal_min      and treeIn.jet_mass_pr < self.mj_signal_max:
                    rdataset_signal_region.add( RooArgSet( rrv_mass_lvj ), treeIn.totalEventWeight );
                if treeIn.jet_mass_pr >= self.mj_sideband_hi_min and treeIn.jet_mass_pr < self.mj_sideband_hi_max:
                    rdataset_sb_hi.add( RooArgSet( rrv_mass_lvj ), treeIn.totalEventWeight );
                
                if treeIn.jet_mass_pr >= self.mj_signal_min      and treeIn.jet_mass_pr < self.mj_signal_max and treeIn.mass_lvj >=self.mlvj_signal_min  and treeIn.mass_lvj <self.mlvj_signal_max     : hnum_2region.Fill(0,treeIn.totalEventWeight);
                if treeIn.jet_mass_pr >= self.mj_signal_min      and treeIn.jet_mass_pr < self.mj_signal_max : hnum_2region.Fill(1,treeIn.totalEventWeight);
        rrv_number_dataset_signal_region=RooRealVar("rrv_number_dataset_signal_region"+label+"_mlvj","rrv_number_dataset_signal_region"+label+"_mlvj",hnum_2region.GetBinContent(1));
        rrv_number_dataset_AllRange=RooRealVar("rrv_number_dataset_AllRange"+label+"_mlvj","rrv_number_dataset_AllRange"+label+"_mlvj",hnum_2region.GetBinContent(2));
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_signal_region)
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_AllRange)
        rrv_number_dataset_signal_region.Print()
        rrv_number_dataset_AllRange.Print()
        #raw_input("Enter to continue");
                
        rdataset_sb_lo.Print();
        rdataset_signal_region.Print();
        rdataset_sb_hi.Print();
        getattr(self.workspace4fit_,"import")(rdataset_sb_lo);
        getattr(self.workspace4fit_,"import")(rdataset_signal_region);
        getattr(self.workspace4fit_,"import")(rdataset_sb_hi);
        rdataset_signal_region.Print()
        self.file_out.write("\n%s events number in m_lvj from dataset: %s"%(label,rdataset_signal_region.sumEntries()))
        #raw_input( 'Press ENTER to continue\n ' )


     ######## ++++++++++++++## ---------------------------------------------------
        
    def fit_mlvj_shape_single_MC_sample(self,in_file_name, label, in_range, in_model_name):# to get the shape of m_lvj
    
        rrv_mass_lvj = self.workspace4fit_.var("rrv_mass_lvj") 
        #dataset
        rdataset = self.workspace4fit_.data("rdataset"+label+"_"+in_range+"_mlvj"); 
        rdataset.Print();
        #model function
        model = self.make_Pdf(label+in_range,in_model_name,"_mlvj");
    
        rfresult = model.fitTo( rdataset, RooFit.Save(1), RooFit.SumW2Error(kTRUE));
        
        mplot = rrv_mass_lvj.frame(RooFit.Title("M_{lvj_"+in_range+"} fitted by "+in_model_name));
        rdataset.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) );
        model.plotOn( mplot, RooFit.VisualizeError(rfresult,1),RooFit.FillColor(kOrange) );
        #model.plotOn(mplot,RooFit.VisualizeError(rfresult,1,kFALSE),RooFit.DrawOption("F"),RooFit.FillColor(kOrange));
        rdataset.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) );
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
    
        rrv_mass_lvj = self.workspace4fit_.var("rrv_mass_lvj") 
        #dataset
        rdataset = self.workspace4fit_.data("rdataset"+label+in_range+"_mlvj"); 
        rdataset.Print();
        #model function
        model = self.make_Model(label+in_range,in_model_name,"_mlvj");
        model.Print()
        #raw_input( 'Press ENTER to continue\n ' )
        rfresult = model.fitTo( rdataset, RooFit.Save(1), RooFit.SumW2Error(kTRUE) ,RooFit.Extended(kTRUE) );
        
        mplot = rrv_mass_lvj.frame(RooFit.Title("M_{lvj_"+in_range+"} fitted by "+in_model_name));
        rdataset.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) );
        model.plotOn( mplot, RooFit.VisualizeError(rfresult,1),RooFit.FillColor(kOrange) );
        #model.plotOn(mplot,RooFit.VisualizeError(rfresult,1,kFALSE),RooFit.DrawOption("F"),RooFit.FillColor(kOrange));
        rdataset.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) );
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
    
    def fit_alpha_WJets(self):# get the shape of WJets in sb_lo, sb_hi, and signal_region. fit to get alpha
        self.get_mlvj_dataset(self.file_WJets_mc,"_WJets")# to get the shape of m_lvj
        model_WJets_sb_lo=self.fit_mlvj_shape_single_MC_sample(self.file_WJets_mc,"_WJets","_sb_lo","ErfExp");
        model_WJets_sb_hi=self.fit_mlvj_shape_single_MC_sample(self.file_WJets_mc,"_WJets","_sb_hi","ErfExp");
        #model_WJets_signal=self.fit_mlvj_shape_single_MC_sample(self.file_WJets_mc,"_WJets","_signal_region","ErfExp");

        #dataset
        rdataset = self.workspace4fit_.data("rdataset_WJets_signal_region"+"_mlvj"); 
        alpha=RooRealVar("alpha","alpha",0.5,0.,1.);
        getattr(self.workspace4fit_,"import")(alpha)
        model_WJets_signal=RooAddPdf("model_WJets_signal","model_WJets_signal",RooArgList(model_WJets_sb_lo,model_WJets_sb_hi),RooArgList(alpha));
        rfresult=model_WJets_signal.fitTo(rdataset, RooFit.Save(1), RooFit.SumW2Error(kTRUE));

        rrv_mass_lvj = self.workspace4fit_.var("rrv_mass_lvj")
        mplot = rrv_mass_lvj.frame(RooFit.Title("M_{lvj_signal_region} fitted by #alpha*M_{lvj_sb_lo} + (1-#alpha)*M_{lvj_sb_hi}"));
        rdataset.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) );
        model_WJets_signal.plotOn( mplot, RooFit.VisualizeError(rfresult,1),RooFit.FillColor(kOrange) );
        #model_WJets_signal.plotOn(mplot,RooFit.VisualizeError(rfresult,1,kFALSE),RooFit.DrawOption("F"),RooFit.FillColor(kOrange));
        rdataset.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) );
        model_WJets_signal.plotOn( mplot );
        #model_WJets_signal.plotOn( mplot, RooFit.Components("model_WJets_sb_lo"), RooFit.LineStyle(kDashed),RooFit.LineColor(kBlack) );
        #model_WJets_signal.plotOn( mplot, RooFit.Components("model_WJets_sb_hi"), RooFit.LineStyle(kDashed),RooFit.LineColor(kRed) );
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
    def fit_WJetsNormalization_in_Mj_signal_region(self, inject_signal=0): # to  get the normalization of WJets in signal_region
        self.fit_m_j_single_MC_sample(self.file_TTbar_mc,"_TTbar","ErfExpGaus");
        self.fit_m_j_single_MC_sample(self.file_WW_mc,"_WW","Voig");
        self.fit_m_j_single_MC_sample(self.file_WJets_mc,"_WJets","ErfExp");
        self.fit_m_j_single_MC_sample(self.file_ggH600,"_ggH600","Voig");
    
        fileIn_name=[TString(self.file_Directory+self.file_WW_mc),TString(self.file_Directory+self.file_TTbar_mc),TString(self.file_Directory+self.file_WJets_mc), TString(self.file_Directory+self.file_ggH600), TString(self.file_Directory+self.file_data)];
    
        listOfTrainingVariables1 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1"];
        bdtSimple = tmvaApplicator( listOfTrainingVariables1, "weights/Wtagger_200to275_simple_BDT.weights.xml");
    
        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j") 
        rrv_mass_j.setBins(55);
        rrv_mass_lvj = self.workspace4fit_.var("rrv_mass_lvj") 
        rrv_weight = RooRealVar("rrv_weight","rrv_weight",0. ,1.) 
        rdataset_Total_mj = RooDataSet("rdataset_Total_mj","rdataset_Total_mj",RooArgSet(rrv_mass_j,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
    
        label="_Total"
        hnum_4region=TH1F("hnum_4region"+label,"hnum_4region"+label,4,-1.5,2.5);
        #prepare the dataset: WJets+TTbar+WW
        for j in range(3+inject_signal): #closure test
        #for j in range(4,5):# true data
            fileIn = TFile(fileIn_name[j].Data());
            treeIn = fileIn.Get("otree");
            mc_scale=1.0;# for background MC, mc_scale=1; for higgs MC, mc_scale=50
            if j==3: mc_scale=self.higgs_xs_scale;
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
                    rdataset_Total_mj.add( RooArgSet( rrv_mass_j ), treeIn.totalEventWeight/mc_scale );
                    if treeIn.jet_mass_pr >=self.mj_sideband_lo_min and treeIn.jet_mass_pr <self.mj_sideband_lo_max: hnum_4region.Fill(-1,treeIn.totalEventWeight/mc_scale );
                    if treeIn.jet_mass_pr >=self.mj_signal_min      and treeIn.jet_mass_pr <self.mj_signal_max     : hnum_4region.Fill(0,treeIn.totalEventWeight/mc_scale);
                    if treeIn.jet_mass_pr >=self.mj_sideband_hi_min and treeIn.jet_mass_pr <self.mj_sideband_hi_max: hnum_4region.Fill(1,treeIn.totalEventWeight/mc_scale); 
                    hnum_4region.Fill(2,treeIn.totalEventWeight/mc_scale);
        rrv_number_Total=RooRealVar("rrv_number"+label+"_mj","rrv_number"+label+"_mj",hnum_4region.GetBinContent(4));
        rrv_number_dataset_sb_lo=RooRealVar("rrv_number_dataset_sb_lo"+label+"_mj","rrv_number_dataset_sb_lo"+label+"_mj",hnum_4region.GetBinContent(1));
        rrv_number_dataset_signal_region=RooRealVar("rrv_number_dataset_signal_region"+label+"_mj","rrv_number_dataset_signal_region"+label+"_mj",hnum_4region.GetBinContent(2));
        rrv_number_dataset_sb_hi=RooRealVar("rrv_number_dataset_sb_hi"+label+"_mj","rrv_number_dataset_sb_hi"+label+"_mj",hnum_4region.GetBinContent(3));
        getattr(self.workspace4fit_,"import")(rrv_number_Total)
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_sb_lo)
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_signal_region)
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_sb_hi)
        print "N_rdataset: ", rdataset_Total_mj.Print();
        getattr(self.workspace4fit_,"import")(rdataset_Total_mj)

        model_TTbar=self.get_TTbar_mj_Model();
        model_WW=self.get_WW_mj_Model();
        model_WJets=self.get_WJets_mj_Model();
        model_Total=RooAddPdf("model_Total_mj","model_Total_mj",RooArgList(model_WJets,model_WW,model_TTbar));
        #model_Total.fixCoefRange("ref");
        getattr(self.workspace4fit_,"import")(model_Total)
        # fit the sideband range

        #rfresult = model_Total.fitTo( rdataset_Total_mj, RooFit.Save(1),RooFit.SumCoefRange("ref") , RooFit.Range("sb_lo,sb_hi") ,RooFit.SumW2Error(kTRUE) ,RooFit.Extended(kTRUE) );
        rfresult = model_Total.fitTo( rdataset_Total_mj, RooFit.Save(1) , RooFit.Range("sb_lo,sb_hi") ,RooFit.SumW2Error(kTRUE) ,RooFit.Extended(kTRUE) );

        
        mplot = rrv_mass_j.frame(RooFit.Title("Closure test: WJets+TTbar+WW"));
        rdataset_Total_mj.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) );
        model_Total.plotOn(mplot,RooFit.VisualizeError(rfresult,1,kFALSE),RooFit.DrawOption("F"),RooFit.FillColor(kOrange),RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()));
        rdataset_Total_mj.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) );
        model_Total.plotOn(mplot );
        #DrawOption("LF"), FillStyle(1001), FillColor(DibosonColor)
        #model_Total.plotOn(mplot, RooFit.Components("model_WJets_mj"),RooFit.LineStyle(kDashed),RooFit.LineColor(kBlack),RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()) );
        #model_Total.plotOn(mplot, RooFit.Components("model_WW_mj"),RooFit.LineStyle(kDashed),RooFit.LineColor(kRed),RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()));
        #model_Total.plotOn(mplot, RooFit.Components("model_TTbar_mj"),RooFit.LineStyle(kDashed),RooFit.LineColor(6),RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()));
        model_Total.plotOn(mplot, RooFit.Components("model_WW_mj"),RooFit.LineColor(kAzure+8),RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()) );
        model_Total.plotOn(mplot, RooFit.Components("model_TTbar_mj"), RooFit.LineColor(kGreen),RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()) );
        model_Total.plotOn(mplot, RooFit.Components("model_WJets_mj"), RooFit.LineColor(kRed),RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()) );
        model_Total.plotOn( mplot );
        model_Total.plotOn( mplot, RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()),RooFit.LineStyle(kDashed) );
    
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

        self.get_mj_normalization("_Total");
        self.get_mj_normalization("_TTbar");
        self.get_mj_normalization("_WW");
        self.get_mj_normalization("_WJets");

        # to calculate the WJets's normalization in M_J signal_region
        #model_WJets = self.workspace4fit_.pdf("model_WJets_mj");

        fullInt   = model_WJets.createIntegral(RooArgSet(rrv_mass_j),RooArgSet(rrv_mass_j) );
        signalInt = model_WJets.createIntegral(RooArgSet(rrv_mass_j),RooArgSet(rrv_mass_j),("signal_region"));
        fullInt_val=fullInt.getVal()
        signalInt_val=signalInt.getVal()/fullInt_val
        rrv_number_WJets_in_mj_signal_region_from_fitting=RooRealVar("rrv_number_WJets_in_mj_signal_region_from_fitting","rrv_number_WJets_in_mj_signal_region_from_fitting",self.workspace4fit_.var("rrv_number_WJets_mj").getVal()*signalInt_val);
        getattr(self.workspace4fit_,"import")(rrv_number_WJets_in_mj_signal_region_from_fitting)
        rrv_number_WJets_in_mj_signal_region_from_fitting.Print();

        #raw_input("WJets normalization over! Plean ENTER to continue!");

    ######## ++++++++++++++
    def fit_mlvj_in_Mj_signal_region(self, inject_signal=0): # fix other background's model and  WJets normalization, floating WJets shape
        self.fit_Signal()
        self.fit_WJets()
        self.fit_WW()
        self.fit_TTbar()
        #raw_input("Fit all MC samples! Plean ENTER to continue!");


        fileIn_name=[TString(self.file_Directory+self.file_WW_mc),TString(self.file_Directory+self.file_TTbar_mc),TString(self.file_Directory+self.file_WJets_mc), TString(self.file_Directory+self.file_ggH600), TString(self.file_Directory+self.file_data)];
    
        listOfTrainingVariables1 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1"];
        bdtSimple = tmvaApplicator( listOfTrainingVariables1, "weights/Wtagger_200to275_simple_BDT.weights.xml");
    
        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j") 
        rrv_mass_lvj = self.workspace4fit_.var("rrv_mass_lvj") 
        rrv_mass_lvj.setBins(52);
        rrv_weight = RooRealVar("rrv_weight","rrv_weight",0. ,1.) 
        rdataset_Total_mlvj = RooDataSet("rdataset_Total_mlvj","rdataset_Total_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
 
        #prepare the dataset: WJets+TTbar+WW
        label="_Total"
        hnum_2region=TH1F("hnum_2region"+label,"hnum_2region"+label,2,-0.5,1.5);
        for j in range(3+inject_signal): #closuer test
        #for j in range(4,5):# true data
            fileIn = TFile(fileIn_name[j].Data());
            treeIn = fileIn.Get("otree");
            # make cuts (including mass drop) # create a RooDataSet
            print "N entries: ", treeIn.GetEntries()
            mc_scale=1.0;# for background MC, mc_scale=1; for higgs MC, mc_scale=50
            if j==3: mc_scale=self.higgs_xs_scale;
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
                    rdataset_Total_mlvj.add( RooArgSet( rrv_mass_lvj ), treeIn.totalEventWeight/mc_scale );

                    if treeIn.jet_mass_pr >= self.mj_signal_min      and treeIn.jet_mass_pr < self.mj_signal_max and treeIn.mass_lvj >=self.mlvj_signal_min  and treeIn.mass_lvj <self.mlvj_signal_max : hnum_2region.Fill(0,treeIn.totalEventWeight/mc_scale);
                    if treeIn.jet_mass_pr >= self.mj_signal_min      and treeIn.jet_mass_pr < self.mj_signal_max : hnum_2region.Fill(1,treeIn.totalEventWeight/mc_scale);

        rrv_number_dataset_signal_region=RooRealVar("rrv_number_dataset_signal_region"+label+"_mlvj","rrv_number_dataset_signal_region"+label+"_mlvj",hnum_2region.GetBinContent(1));
        rrv_number_dataset_AllRange=RooRealVar("rrv_number_dataset_AllRange"+label+"_mlvj","rrv_number_dataset_AllRange"+label+"_mlvj",hnum_2region.GetBinContent(2));
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_signal_region)
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_AllRange)

        rrv_number_dataset_signal_region.Print()
        rrv_number_dataset_AllRange.Print()

        print "N_rdataset: ", rdataset_Total_mlvj.Print();
        self.file_out.write("\ndata_obs event number: %s\n"%(rdataset_Total_mlvj.sumEntries()) )
        self.file_out.write("\ndata_obs event number in m_lvj_signal_region: %s\n"%(hnum_2region.GetBinContent(1)) )
        self.file_out.write("\ndata_obs event number in m_lvj_All_region: %s\n"%(hnum_2region.GetBinContent(2)) )
        #raw_input("Fit all MC samples! Plean ENTER to continue!");
        getattr(self.workspace4fit_,"import")(rdataset_Total_mlvj)
        #prepare Limit: data_obs
        getattr(self.workspace4limit_,"import")(rdataset_Total_mlvj.Clone("data_obs"))

        model_TTbar   = self.get_TTbar_mlvj_Model();
        model_WW    = self.get_WW_mlvj_Model();
        model_WJets = self.get_WJets_mlvj_Model();
        model_ggH   = self.get_ggH_mlvj_Model();
        model_TTbar.Print();
        model_WW.Print();
        model_WJets.Print();
        #prepare for Limit
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.pdf("model_pdf_TTbar_signal_region_mlvj").clone("TTbar"))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.pdf("model_pdf_WJets_signal_region_mlvj").clone("WJets"))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.pdf("model_pdf_WW_signal_region_mlvj").clone("WW"))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.pdf("model_pdf_ggH600_signal_region_mlvj").clone("ggH600"))

        model_Total=RooAddPdf("model_Total_signal_region_mlvj","model_Total_signal_region_mlvj",RooArgList(model_WJets,model_WW,model_TTbar));
        getattr(self.workspace4fit_,"import")(model_Total)

        rfresult = model_Total.fitTo( rdataset_Total_mlvj, RooFit.Save(1) ,RooFit.SumW2Error(kTRUE) ,RooFit.Extended(kTRUE) );
        
        mplot = rrv_mass_lvj.frame(RooFit.Title("Closure test: WJets+TTbar+WW"));
        rdataset_Total_mlvj.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) );
        model_Total.plotOn(mplot,RooFit.VisualizeError(rfresult,1,kFALSE),RooFit.DrawOption("F"),RooFit.FillColor(kOrange));
        rdataset_Total_mlvj.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) );
        model_Total.plotOn(mplot );
        #model_Total.plotOn(mplot, RooFit.Components("model_WJets_mj"),RooFit.LineStyle(kDashed),RooFit.LineColor(kBlack),RooFit.Range(rrv_mass_lvj.getMin(),rrv_mass_lvj.getMax()) );
        #model_Total.plotOn(mplot, RooFit.Components("model_WW_mj"),RooFit.LineStyle(kDashed),RooFit.LineColor(kRed),RooFit.Range(rrv_mass_lvj.getMin(),rrv_mass_lvj.getMax()));
        #model_Total.plotOn(mplot, RooFit.Components("model_TTbar_mj"),RooFit.LineStyle(kDashed),RooFit.LineColor(6),RooFit.Range(rrv_mass_lvj.getMin(),rrv_mass_lvj.getMax()));
        model_Total.plotOn(mplot, RooFit.Components("model_WW_signal_region_mlvj"),RooFit.LineColor(kAzure+8));
        model_Total.plotOn(mplot, RooFit.Components("model_TTbar_signal_region_mlvj"), RooFit.LineColor(kGreen));
        model_Total.plotOn(mplot, RooFit.Components("model_WJets_signal_region_mlvj"), RooFit.LineColor(kRed));
        model_Total.plotOn( mplot );
        model_Total.plotOn( mplot, RooFit.Range(rrv_mass_lvj.getMin(),rrv_mass_lvj.getMax()),RooFit.LineStyle(kDashed) );
    
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


        self.get_mlvj_normalization("_ggH600");
        self.get_mlvj_normalization("_TTbar");
        self.get_mlvj_normalization("_WW");
        self.get_mlvj_normalization("_WJets");

        rfresult.Print();
        self.workspace4limit_.data("data_obs").Print()

    ######## ++++++++++++++
    def get_mj_normalization(self, label):
        print "________________________________________________________________________________________________"
        print "get mj normalization"
        model = self.workspace4fit_.pdf("model"+label+"_mj");
        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j");

        fullInt   = model.createIntegral(RooArgSet(rrv_mass_j),RooArgSet(rrv_mass_j) );
        sb_loInt   = model.createIntegral(RooArgSet(rrv_mass_j),RooArgSet(rrv_mass_j),("sb_lo"));
        signalInt = model.createIntegral(RooArgSet(rrv_mass_j),RooArgSet(rrv_mass_j),("signal_region"));
        sb_hiInt   = model.createIntegral(RooArgSet(rrv_mass_j),RooArgSet(rrv_mass_j),("sb_hi"));
        
        fullInt_val=fullInt.getVal()
        sb_loInt_val=sb_loInt.getVal()/fullInt_val
        sb_hiInt_val=sb_hiInt.getVal()/fullInt_val
        signalInt_val=signalInt.getVal()/fullInt_val

        print label+"sb_loInt=%s"%(sb_loInt_val)
        print label+"signalInt=%s"%(signalInt_val)
        print label+"sb_hiInt=%s"%(sb_hiInt_val)

        print "Events Number in MC Dataset:"
        self.workspace4fit_.var("rrv_number_dataset_sb_lo"+label+"_mj").Print();
        self.workspace4fit_.var("rrv_number_dataset_signal_region"+label+"_mj").Print();
        self.workspace4fit_.var("rrv_number_dataset_sb_hi"+label+"_mj").Print();

        print "Events Number get from fit:"
        rrv_tmp=self.workspace4fit_.var("rrv_number"+label+"_mj");
        rrv_tmp.Print();
        print "Events Number in sideband_low :%s"%(rrv_tmp.getVal()*sb_loInt_val)
        print "Events Number in Signal Region:%s"%(rrv_tmp.getVal()*signalInt_val)
        print "Events Number in sideband_high:%s"%(rrv_tmp.getVal()*sb_hiInt_val)
        print "Total Number in sidebands     :%s"%(rrv_tmp.getVal()*(sb_loInt_val+sb_hiInt_val)  )
        print "Ratio signal_region/sidebands        :%s"%(signalInt_val/(sb_loInt_val+sb_hiInt_val)  )

        #save to file
        self.file_out.write( "\n%s++++++++++++++++++++++++++++++++++++"%(label) )
        self.file_out.write( "\nEvents Number in sideband_low  from dataset:%s"%(self.workspace4fit_.var("rrv_number_dataset_sb_lo"+label+"_mj").getVal() ) )
        self.file_out.write( "\nEvents Number in Signal Region from dataset:%s"%(self.workspace4fit_.var("rrv_number_dataset_signal_region"+label+"_mj").getVal() ) )
        self.file_out.write( "\nEvents Number in sideband_high from dataset:%s"%(self.workspace4fit_.var("rrv_number_dataset_sb_hi"+label+"_mj").getVal() ) )
        self.file_out.write( "\nTotal Number in sidebands      from dataset:%s"%(self.workspace4fit_.var("rrv_number_dataset_sb_lo"+label+"_mj").getVal()+ self.workspace4fit_.var("rrv_number_dataset_sb_hi"+label+"_mj").getVal() ) )
        self.file_out.write( "\nRatio signal_region/sidebands  from dataset:%s"%(self.workspace4fit_.var("rrv_number_dataset_signal_region"+label+"_mj").getVal()/(self.workspace4fit_.var("rrv_number_dataset_sb_lo"+label+"_mj").getVal()+ self.workspace4fit_.var("rrv_number_dataset_sb_hi"+label+"_mj").getVal()) ) )

        self.file_out.write( "\nEvents Number in sideband_low  from fitting:%s"%(rrv_tmp.getVal()*sb_loInt_val) )
        self.file_out.write( "\nEvents Number in Signal Region from fitting:%s"%(rrv_tmp.getVal()*signalInt_val) )
        self.file_out.write( "\nEvents Number in sideband_high from fitting:%s"%(rrv_tmp.getVal()*sb_hiInt_val) )
        self.file_out.write( "\nTotal Number in sidebands      from fitting:%s"%(rrv_tmp.getVal()*(sb_loInt_val+sb_hiInt_val)  ) )
        self.file_out.write( "\nRatio signal_region/sidebands  from fitting:%s"%(signalInt_val/(sb_loInt_val+sb_hiInt_val)  ) )

        if label=="_WJets": #prepare Limit of WJet Norm
            self.number_WJets_insideband=int(round( rrv_tmp.getVal()*(sb_loInt_val+sb_hiInt_val) ))
            #self.datadriven_alpha_WJets_unbin =signalInt_val/(sb_loInt_val+sb_hiInt_val)
            self.datadriven_alpha_WJets_unbin =rrv_tmp.getVal()*signalInt_val/self.number_WJets_insideband


######## ++++++++++++++
    def get_mlvj_normalization(self, label):
        print "________________________________________________________________________________________________"
        print "get mlvj normalization"
        model = self.workspace4fit_.pdf("model"+label+"_signal_region_mlvj");
        model.Print()
        rrv_mass_lvj = self.workspace4fit_.var("rrv_mass_lvj");

        fullInt   = model.createIntegral(RooArgSet(rrv_mass_lvj),RooArgSet(rrv_mass_lvj) );
        signalInt = model.createIntegral(RooArgSet(rrv_mass_lvj),RooArgSet(rrv_mass_lvj),("signal_region"));
        
        fullInt_val=fullInt.getVal()
        signalInt_val=signalInt.getVal()/fullInt_val

        print label+"signalInt=%s"%(signalInt_val)

        print "Events Number in MC Dataset:"
        self.workspace4fit_.var("rrv_number_dataset_signal_region"+label+"_mlvj").Print();
        self.workspace4fit_.var("rrv_number_dataset_AllRange"+label+"_mlvj").Print();

        print "Events Number get from fit:"
        rrv_tmp=self.workspace4fit_.var("rrv_number"+label+"_signal_region_mlvj");
        rrv_tmp.Print();
        print "\nEvents Number in Signal Region from fitting: %s"%(rrv_tmp.getVal()*signalInt_val)

        #save to file
        self.file_out.write( "\n%s++++++++++++++++++++++++++++++++++++"%(label) )
        self.file_out.write( "\nEvents Number in All Region from dataset   : %s"%(self.workspace4fit_.var("rrv_number_dataset_AllRange"+label+"_mlvj").getVal()) )
        self.file_out.write( "\nEvents Number in Signal Region from dataset: %s"%(self.workspace4fit_.var("rrv_number_dataset_signal_region"+label+"_mlvj").getVal()) )
        self.file_out.write( "\nRatio signal_region/all_range from dataset  :%s"%(self.workspace4fit_.var("rrv_number_dataset_signal_region"+label+"_mlvj").getVal()/self.workspace4fit_.var("rrv_number_dataset_AllRange"+label+"_mlvj").getVal() ) )
        self.file_out.write( "\nEvents Number in All Region from fitting   : %s\n"%(rrv_tmp.getVal()) )
        self.file_out.write( "\nEvents Number in Signal Region from fitting: %s\n"%(rrv_tmp.getVal()*signalInt_val) )
        self.file_out.write( "\nRatio signal_region/all_range from fitting :%s"%(signalInt_val ) )

        rrv_number_fitting_signal_region_mlvj=RooRealVar("rrv_number_fitting_signal_region"+label+"_mlvj","rrv_number_fitting_signal_region"+label+"_mlvj", rrv_tmp.getVal()*signalInt_val )
        getattr(self.workspace4fit_,"import")(rrv_number_fitting_signal_region_mlvj)

       
        if label=="_WJets": #prepare Limit of WJet Norm
            self.datadriven_alpha_WJets_counting = rrv_tmp.getVal()*signalInt_val/self.number_WJets_insideband 

 
        #self.workspace4fit_.var("rrv_number"+label+"_mlvj").Print();
    ######## ++++++++++++++
    def print_limit_datacard_unbin(self):
        print "print_limit_datacard_unbin"
        datacard_out=open(self.file_datacard_unbin,"w");

        datacard_out.write( "imax 1" )
        datacard_out.write( "\njmax 3" )
        datacard_out.write( "\nkmax *" )
        datacard_out.write( "\n--------------- ")
        datacard_out.write( "\nshapes * * %s %s:$PROCESS "%(self.file_rlt_root, self.workspace4limit_.GetName()))
        datacard_out.write( "\n--------------- ")
        datacard_out.write( "\nbin 1 ")
        datacard_out.write( "\nobservation %s "%(self.workspace4limit_.data("data_obs").sumEntries()) )
        datacard_out.write( "\n------------------------------" )
        datacard_out.write( "\nbin                1         1        1      1 " )
        datacard_out.write( "\nprocess            ggH600    WJets    TTbar  WW " )
        datacard_out.write( "\nprocess            0         1        2      3 " )
        datacard_out.write( "\nrate               %s        %s       %s     %s "%(self.workspace4fit_.var("rrv_number_ggH600_signal_region_mlvj").getVal()/self.higgs_xs_scale, self.workspace4fit_.var("rrv_number_WJets_signal_region_mlvj").getVal(), self.workspace4fit_.var("rrv_number_TTbar_signal_region_mlvj").getVal(), self.workspace4fit_.var("rrv_number_WW_signal_region_mlvj").getVal()  ) )
        datacard_out.write( "\n-------------------------------- " )
        datacard_out.write( "\nlumi    lnN        1.022     -        1.022  1.022" )
        datacard_out.write( "\npdf_gg  lnN        1.099     -        -      - " )
        datacard_out.write( "\nXS_hig  lnN        1.137     -        -      - " )
        datacard_out.write( "\nWJ_norm gmN %s     -         %s       -      - "%(self.number_WJets_insideband, self.datadriven_alpha_WJets_unbin) )
        datacard_out.write( "\nXS_TTbar lnN       -         -        1.07   -  " )
        datacard_out.write( "\nXS_WW   lnN        -         -        -      1.10 " )
        rrv_c=self.workspace4fit_.var("rrv_c_ErfExp_WJets_signal_region")
        rrv_offset=self.workspace4fit_.var("rrv_offset_ErfExp_WJets_signal_region")
        rrv_width=self.workspace4fit_.var("rrv_width_ErfExp_WJets_signal_region")
        datacard_out.write( "\n%s param  %s  %s "%( rrv_c.GetName(), rrv_c.getVal(), rrv_c.getError() ) )
        datacard_out.write( "\n%s param  %s  %s "%( rrv_offset.GetName(), rrv_offset.getVal(), rrv_offset.getError() ) )
        datacard_out.write( "\n%s param  %s  %s \n"%( rrv_width.GetName(), rrv_width.getVal(), rrv_width.getError() ) )

    ######## ++++++++++++++
    def print_limit_datacard_counting(self):
        print "print_limit_datacard_counting"

        datacard_out=open(self.file_datacard_counting,"w");
        datacard_out.write( "imax 1" )
        datacard_out.write( "\njmax 3" )
        datacard_out.write( "\nkmax *" )
        datacard_out.write( "\n--------------- " )
        datacard_out.write( "\nbin 1 " )
        datacard_out.write( "\nobservation %s "%(self.workspace4fit_.var("rrv_number_dataset_signal_region_Total_mlvj").getVal()) )
        datacard_out.write( "\n------------------------------" )
        datacard_out.write( "\nbin                1         1        1      1 " )
        datacard_out.write( "\nprocess            ggH600    WJets    TTbar  WW " )
        datacard_out.write( "\nprocess            0         1        2      3 " )
        datacard_out.write( "\nrate               %s        %s       %s     %s "%(self.workspace4fit_.var("rrv_number_fitting_signal_region_ggH600_mlvj").getVal()/self.higgs_xs_scale, self.workspace4fit_.var("rrv_number_fitting_signal_region_WJets_mlvj").getVal(), self.workspace4fit_.var("rrv_number_fitting_signal_region_TTbar_mlvj").getVal(), self.workspace4fit_.var("rrv_number_fitting_signal_region_WW_mlvj").getVal()  ) )
        datacard_out.write( "\n-------------------------------- " )
        datacard_out.write( "\nlumi    lnN        1.022     -        1.022  1.022" )
        datacard_out.write( "\npdf_gg  lnN        1.099     -        -      - " )
        datacard_out.write( "\nXS_hig  lnN        1.137     -        -      - " )
        datacard_out.write( "\nWJ_norm gmN %s     -         %s       -      - "%(self.number_WJets_insideband, self.datadriven_alpha_WJets_counting) )
        datacard_out.write( "\nXS_TTbar lnN       -         -        1.07   -  " )
        datacard_out.write( "\nXS_WW   lnN        -         -        -      1.10\n" )

    ######## ++++++++++++++
    def read_workspace(self,filename="tmp_workspace.root"):
        file = TFile(self.file_rlt_root) ;
        self.workspace4fit_ = file.Get("workspace4fit_") ;

    ######## ++++++++++++++
    def save_workspace(self,filename="tmp_workspace.root"):
        #self.workspace4fit_.writeToFile(filename);
        self.workspace4fit_.writeToFile(self.file_rlt_root);
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
        cMassFit = TCanvas("cMassFit","cMassFit",1000,800);
        pad1=TPad("pad1","pad1",0.,0. ,0.8,0.2);
        pad2=TPad("pad2","pad2",0.,0.2,0.8,1. );
        pad3=TPad("pad3","pad3",0.8,0.,1,1);
        pad1.Draw();
        pad2.Draw();
        pad3.Draw();

        pad2.cd();
        mplot.Draw();
        pad1.cd();
        mplot_pull.Draw();

        pad3.cd();
        latex=TLatex();
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

        Directory=TString(in_directory);
        if not Directory.EndsWith("/"):Directory=Directory.Append("/");
        if not os.path.isdir(Directory.Data()): os.system("mkdir -p  "+Directory.Data());

        rlt_file=TString(Directory.Data()+in_file_name);
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
        self.get_mlvj_dataset(self.file_data,"_data")# to get the shape of m_lvj
        #self.fit_mlvj_model_single_MC_sample(self.file_data,"_data","_sb_lo","ErfExp");
        #self.fit_mlvj_model_single_MC_sample(self.file_data,"_data","_sb_hi","ErfExp");
        self.fit_mlvj_model_single_MC_sample(self.file_data,"_data","_signal_region","ErfExp");
        print "________________________________________________________________________"
    ######## ++++++++++++++
    def fit_Signal(self):
        print "fit_Signal"
        #self.fit_m_j_single_MC_sample(self.file_ggH600,"_ggH600","Voig");
        self.get_mlvj_dataset(self.file_ggH600,"_ggH600")# to get the shape of m_lvj
        #self.fit_mlvj_model_single_MC_sample(self.file_ggH600,"_ggH600","_sb_lo","ErfExp");
        #self.fit_mlvj_model_single_MC_sample(self.file_ggH600,"_ggH600","_sb_hi","ErfExp");
        self.fit_mlvj_model_single_MC_sample(self.file_ggH600,"_ggH600","_signal_region","ErfExpGaus_v1");
        print "________________________________________________________________________"
    ######## ++++++++++++++
    def fit_WJets(self):
        print "fit_WJets"
        self.get_mlvj_dataset(self.file_WJets_mc,"_WJets")# to get the shape of m_lvj
        self.fit_mlvj_model_single_MC_sample(self.file_WJets_mc,"_WJets","_signal_region","ErfExp_v1");
        print "________________________________________________________________________" 
    ######## ++++++++++++++
    def fit_WW(self):
        print "fit_WW"
        self.get_mlvj_dataset(self.file_WW_mc,"_WW")# to get the shape of m_lvj
        self.fit_mlvj_model_single_MC_sample(self.file_WW_mc,"_WW","_signal_region","ErfExp_v1");
        print "________________________________________________________________________"
    ######## ++++++++++++++
    def fit_TTbar(self):
        print "fit_TTbar"
        self.get_mlvj_dataset(self.file_TTbar_mc,"_TTbar")# to get the shape of m_lvj
        self.fit_mlvj_model_single_MC_sample(self.file_TTbar_mc,"_TTbar","_signal_region","ErfExp_v1");
        print "________________________________________________________________________"
    ######## ++++++++++++++
    def fit_AllSamples_Mlvj(self):
        print "fit_AllSamples_Mlvj"
        #self.fit_Signal()
        #self.fit_alpha_WJets();
        #self.fit_WJets()
        self.fit_WW()
        self.fit_TTbar()
        print "________________________________________________________________________" 

def test():
    cutOnMassDrop = False;
    boostedW_fitter=doFit_wj_and_wlvj(cutOnMassDrop)
    boostedW_fitter.fit_AllSamples_Mlvj()

def get_WJets_normalization():
    cutOnMassDrop = False;
    boostedW_fitter=doFit_wj_and_wlvj(cutOnMassDrop)
    boostedW_fitter.fit_WJetsNormalization_in_Mj_signal_region();
    boostedW_fitter.save_workspace();

def get_alpha():
    cutOnMassDrop = False;
    boostedW_fitter=doFit_wj_and_wlvj(cutOnMassDrop)
    boostedW_fitter.fit_alpha_WJets();
    boostedW_fitter.save_workspace();

def fit_data():
    cutOnMassDrop = False;
    boostedW_fitter=doFit_wj_and_wlvj(cutOnMassDrop)
    boostedW_fitter.fit_WJetsNormalization_in_Mj_signal_region();
    boostedW_fitter.fit_data();
    #boostedW_fitter.save_workspace();


def pre_limit(): 
    cutOnMassDrop = False;
    boostedW_fitter=doFit_wj_and_wlvj(cutOnMassDrop)

    inject_signal=0;# 0: not inject_signal; 1: inject_signal
    boostedW_fitter.fit_WJetsNormalization_in_Mj_signal_region(inject_signal);
    boostedW_fitter.fit_mlvj_in_Mj_signal_region(inject_signal)
    boostedW_fitter.save_for_limit();
    boostedW_fitter.print_limit_datacard_unbin();
    boostedW_fitter.print_limit_datacard_counting();

if __name__ == '__main__':
    #get_WJets_normalization()
    #get_alpha()
    #fit_data()
    pre_limit()
    #test()

