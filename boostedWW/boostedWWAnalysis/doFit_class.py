#! /usr/bin/env python
import os
import glob
import math
import array

from ROOT import gROOT, gStyle, gSystem, TLatex, TString, TF1,TFile,TLine, TLegend, TH1D,TH2D, TCanvas, TMatrixDSym, TText, TPad, RooFit, RooArgSet, RooArgList, RooArgSet, RooAbsData, RooAbsPdf, RooAddPdf, RooWorkspace, RooExtendPdf,RooCBShape, RooLandau, RooFFTConvPdf, RooGaussian, RooBifurGauss, RooDataSet, RooBreitWigner, RooVoigtian, RooRealVar,RooFormulaVar, RooDataHist, RooHistPdf, RooGenericPdf, RooKeysPdf, RooHistPdf, RooEffProd, TIter, kTRUE, kFALSE, kGray, kRed, kDashed, kGreen,kAzure, kOrange, kBlack,kBlue,kYellow,kCyan
import subprocess
from subprocess import Popen

from sampleWrapperClass import *
from trainingClass      import *
from BoostedWSamples    import * 
from mvaApplication     import *

import sys

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
    def __init__(self, in_cutOnMassDrop, in_higgs_sample="ggH600", in_mlvj_signal_region_min=500, in_mlvj_signal_region_max=700, in_mj_min=30, in_mj_max=140, in_mlvj_min=300., in_mlvj_max=1400.):
        print "Begin to fit"

        RooAbsPdf.defaultIntegratorConfig().setEpsRel(1e-9) ;
        RooAbsPdf.defaultIntegratorConfig().setEpsAbs(1e-9) ;

        self.cutOnMassDrop_=in_cutOnMassDrop;

        self.higgs_sample=in_higgs_sample

        rrv_mass_j  = RooRealVar("rrv_mass_j","mass(j) [GeV/C^{2}]",(in_mj_min+in_mj_max)/2.,in_mj_min,in_mj_max);
        rrv_mass_j.setBins(55);
        rrv_mass_lvj= RooRealVar("rrv_mass_lvj","mass(lvj) [GeV/C^{2}]",(in_mlvj_min+in_mlvj_max)/2.,in_mlvj_min,in_mlvj_max);
        rrv_mass_lvj.setBins(50);

        self.workspace4fit_ = RooWorkspace("workspace4fit_","workspace4fit_");
        getattr(self.workspace4fit_,"import")(rrv_mass_j);
        getattr(self.workspace4fit_,"import")(rrv_mass_lvj);

        #prepare workspace for unbin-Limit
        self.workspace4limit_ = RooWorkspace("workspace4limit_","workspace4limit_");

        self.mj_sideband_lo_min=40;
        self.mj_sideband_lo_max=70;
        self.mj_signal_min=70;
        self.mj_signal_max=95;
        self.mj_sideband_hi_min=95;
        self.mj_sideband_hi_max=140;
        # test
        #self.mj_sideband_lo_min=30;
        #self.mj_sideband_lo_max=52;
        #self.mj_signal_min=52;
        #self.mj_signal_max=67;
        #self.mj_sideband_hi_min=100;
        #self.mj_sideband_hi_max=125;
        rrv_mass_j.setRange("sb_lo",self.mj_sideband_lo_min,self.mj_sideband_lo_max);
        rrv_mass_j.setRange("signal_region",self.mj_signal_min,self.mj_signal_max); 
        rrv_mass_j.setRange("sb_hi",self.mj_sideband_hi_min,self.mj_sideband_hi_max);
        rrv_mass_j.setRange("range4plot",in_mj_min,in_mj_max)

        self.mlvj_signal_min=in_mlvj_signal_region_min
        self.mlvj_signal_max=in_mlvj_signal_region_max
        rrv_mass_lvj.setRange("signal_region",self.mlvj_signal_min,self.mlvj_signal_max); 
        rrv_mass_lvj.setRange("range4plot",in_mlvj_min,in_mlvj_max); 

        #prepare the data and mc files
        self.file_data=("ofile_data.root");#keep blind!!!!
        #self.file_data=("ofile_fake_data.root");#keep blind!!!!
        self.file_Total_MC=("ofile_Total_MC.root");#fake data
        self.file_ggH=("ofile_%s.root"%(self.higgs_sample));

        self.file_WW_mc=("ofile_WW.root");
        self.file_WZ_mc=("ofile_WZ.root");
        self.file_VV_mc=("ofile_VV.root");# WW+WZ 
        self.file_ZZ_mc=("ofile_ZZ.root");
        self.file_WJets_mc=("ofile_WJets.root");
        self.file_ZJets_mc=("ofile_ZJets.root");
        self.file_TTbar_mc=("ofile_TTbar.root");
        self.file_STop_mc =("ofile_STop.root");#single Top
        self.file_Directory="trainingtrees/";

        #result files: The event number, parameters and error write into a txt file. The dataset and pdfs write into a root file
        self.file_rlt_txt           = "hwwlvj_%s_other.txt"%(self.higgs_sample)
        self.file_rlt_root          = "hwwlvj_%s_workspace.root"%(self.higgs_sample)
        self.file_datacard_unbin    = "hwwlvj_%s_datacard_unbin.txt"%(self.higgs_sample)
        self.file_datacard_counting = "hwwlvj_%s_datacard_counting.txt"%(self.higgs_sample)
        
        self.file_out=open(self.file_rlt_txt,"w");
        self.file_out.write("\nWelcome:\n");
        self.file_out.close()
        self.file_out=open(self.file_rlt_txt,"a+");

        #higgs XS scale
        self.higgs_xs_scale=50.;

        #color palet
        self.color_palet={
            'WJets' : kRed,
            'VV'    : kAzure+8,
            'TTbar' : kGreen,
            'STop'  : kYellow,
            'Signal': kBlack,
            'Error' : kBlack,
            'Other_Backgrounds'  : kBlue
        }

## ---------------------------------------------------
    def make_Model(self, label, in_model_name, mass_spectrum="_mj"):
        rrv_number = RooRealVar("rrv_number"+label+mass_spectrum,"rrv_number"+label+mass_spectrum,500,0.,100000);
        model_pdf  = self.make_Pdf(label,in_model_name,mass_spectrum)
        model = RooExtendPdf("model"+label+mass_spectrum,"model"+label+mass_spectrum, model_pdf, rrv_number );
        rrv_number.Print()
        model.Print()

        getattr(self.workspace4fit_,"import")(rrv_number)
        getattr(self.workspace4fit_,"import")(model)
        rrv_number.Print()
        #raw_input("Enter to continue");
        return self.workspace4fit_.pdf("model"+label+mass_spectrum)

    def make_Pdf(self, label, in_model_name, mass_spectrum="_mj"):
        if mass_spectrum=="_mj": rrv_x = self.workspace4fit_.var("rrv_mass_j"); 
        if mass_spectrum=="_mlvj": rrv_x = self.workspace4fit_.var("rrv_mass_lvj"); 
        
        if in_model_name == "Voig":
            rrv_mean_voig=RooRealVar("rrv_mean_voig"+label,"rrv_mean_voig"+label,82,78,87);# W mass: 80.385
            rrv_width_voig=RooRealVar("rrv_width_voig"+label,"rrv_width_voig"+label,7.,1,10);
            rrv_sigma_voig=RooRealVar("rrv_sigma_voig"+label,"rrv_sigma_voig"+label,5,1,15);
            model_pdf = RooVoigtian("model_pdf"+label+mass_spectrum,"model_pdf"+label+mass_spectrum, rrv_x,rrv_mean_voig,rrv_width_voig,rrv_sigma_voig);

        if in_model_name == "2Voig":
            rrv_mean_voig=RooRealVar("rrv_mean_voig"+label,"rrv_mean_voig"+label,82,78,87);#W mass 80.385
            rrv_shift_2Voig=RooRealVar("rrv_shift_2Voig"+label,"rrv_shift_2Voig"+label,10.8026)   # Z mass: 91.1876;  shift=91.1876-80.385=10.8026
            rrv_mean_shifted= RooFormulaVar("rrv_mean_voig2"+label,"@0+@1",RooArgList(rrv_mean_voig,rrv_shift_2Voig));
            rrv_width_voig=RooRealVar("rrv_width_voig"+label,"rrv_width_voig"+label,7.,1,10);
            rrv_sigma_voig=RooRealVar("rrv_sigma_voig"+label,"rrv_sigma_voig"+label,5,1,15);
            rrv_frac=RooRealVar("rrv_frac"+label,"rrv_frac"+label,1.,0.5,1.);
            model_voig1 = RooVoigtian("model_voig1"+label+mass_spectrum,"model_voig1"+label+mass_spectrum, rrv_x,rrv_mean_voig,rrv_width_voig,rrv_sigma_voig);
            model_voig2 = RooVoigtian("model_voig2"+label+mass_spectrum,"model_voig2"+label+mass_spectrum, rrv_x,rrv_mean_shifted,rrv_width_voig,rrv_sigma_voig);
            model_pdf = RooAddPdf("model_pdf"+label+mass_spectrum,"model_pdf"+label+mass_spectrum, RooArgList(model_voig1,model_voig2), RooArgList(rrv_frac));
    
        if in_model_name == "Gaus":
            rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,82,78,87);
            rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label,"rrv_sigma_gaus"+label,7,1,15);
            model_pdf = RooGaussian("model_pdf"+label+mass_spectrum,"model_pdf"+label+mass_spectrum, rrv_x,rrv_mean_gaus,rrv_sigma_gaus);

        if in_model_name == "Gaus_v1":
            if label=="_ggH600_signal_region":
                rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,600,550,650);
                rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label,"rrv_sigma_gaus"+label,67,40,80);
            if label=="_ggH700_signal_region":
                rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,700,650,750);
                rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label,"rrv_sigma_gaus"+label,100,40,150);
            if label=="_ggH800_signal_region": 
                rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,800,750,850);
                rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label,"rrv_sigma_gaus"+label,130,120,140);
            if label=="_ggH900_signal_region": 
                rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,900,850,900);
                rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label,"rrv_sigma_gaus"+label,160,140,180);
            if label=="_ggH1000_signal_region":
                rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,920,900,1000);
                rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label,"rrv_sigma_gaus"+label,200,100,300);
            #rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,700,500,1200);
            model_pdf = RooGaussian("model_pdf"+label+mass_spectrum,"model_pdf"+label+mass_spectrum, rrv_x,rrv_mean_gaus,rrv_sigma_gaus);
 
        if in_model_name == "BifurGaus_v1":
            if label=="_ggH600_signal_region":
                rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,600,550,650);
                rrv_sigma1_gaus=RooRealVar("rrv_sigma1_gaus"+label,"rrv_sigma1_gaus"+label,67,40,80);
                rrv_sigma2_gaus=RooRealVar("rrv_sigma2_gaus"+label,"rrv_sigma2_gaus"+label,67,40,80);
            if label=="_ggH700_signal_region":
                rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,700,650,750);
                rrv_sigma1_gaus=RooRealVar("rrv_sigma1_gaus"+label,"rrv_sigma1_gaus"+label,100,40,150);
                rrv_sigma2_gaus=RooRealVar("rrv_sigma2_gaus"+label,"rrv_sigma2_gaus"+label,100,40,150);
            if label=="_ggH800_signal_region": 
                rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,800,750,850);
                rrv_sigma1_gaus=RooRealVar("rrv_sigma1_gaus"+label,"rrv_sigma1_gaus"+label,130,120,140);
                rrv_sigma2_gaus=RooRealVar("rrv_sigma2_gaus"+label,"rrv_sigma2_gaus"+label,130,120,140);
            if label=="_ggH900_signal_region": 
                rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,900,850,900);
                rrv_sigma1_gaus=RooRealVar("rrv_sigma1_gaus"+label,"rrv_sigma1_gaus"+label,160,140,180);
                rrv_sigma2_gaus=RooRealVar("rrv_sigma2_gaus"+label,"rrv_sigma2_gaus"+label,160,140,180);
            if label=="_ggH1000_signal_region":
                rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,920,900,1000);
                rrv_sigma1_gaus=RooRealVar("rrv_sigma1_gaus"+label,"rrv_sigma1_gaus"+label,200,100,300);
                rrv_sigma2_gaus=RooRealVar("rrv_sigma2_gaus"+label,"rrv_sigma2_gaus"+label,200,100,300);
            #rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,700,500,1200);
            #model_pdf = RooGaussian("model_pdf"+label+mass_spectrum,"model_pdf"+label+mass_spectrum, rrv_x,rrv_mean_gaus,rrv_sigma_gaus);
            model_pdf = RooBifurGauss("model_pdf"+label+mass_spectrum,"model_pdf"+label+mass_spectrum, rrv_x,rrv_mean_gaus,rrv_sigma1_gaus,rrv_sigma2_gaus);
    
        if in_model_name == "CB":
            rrv_mean_CB=RooRealVar("rrv_mean_CB"+label,"rrv_mean_CB"+label,82,75,90);
            rrv_sigma_CB=RooRealVar("rrv_sigma_CB"+label,"rrv_sigma_CB"+label,7,1,15);
            rrv_alpha_CB=RooRealVar("rrv_alpha_CB"+label,"rrv_alpha_CB"+label,-2,-4,-0.5);
            rrv_n_CB=RooRealVar("rrv_n_CB"+label,"rrv_n_CB"+label,2,0.,4);
            model_pdf = RooCBShape("model_pdf"+label+mass_spectrum,"model_pdf"+label+mass_spectrum, rrv_x,rrv_mean_CB,rrv_sigma_CB,rrv_alpha_CB,rrv_n_CB);

        if in_model_name == "SCB_v1":
            rrv_mean_SCB=RooRealVar("rrv_mean_SCB"+label,"rrv_mean_SCB"+label,800,550,1000);
            rrv_sigma_SCB=RooRealVar("rrv_sigma_SCB"+label,"rrv_sigma_SCB"+label,70,40,300);
            rrv_alpha1_SCB=RooRealVar("rrv_alpha1_SCB"+label,"rrv_alpha1_SCB"+label,-2,-4,-0.5);
            rrv_alpha2_SCB=RooRealVar("rrv_alpha2_SCB"+label,"rrv_alpha2_SCB"+label,2,0.5,4);
            rrv_n1_SCB=RooRealVar("rrv_n1_SCB"+label,"rrv_n1_SCB"+label,2,0.,4);
            rrv_n2_SCB=RooRealVar("rrv_n2_SCB"+label,"rrv_n2_SCB"+label,2,0.,4);
            frac=RooRealVar("rrv_frac_SSCB"+label,"rrv_frac_SSCB"+label,0.5)
            scb1 = RooCBShape("model_pdf_scb1"+label+mass_spectrum,"model_pdf_scb1"+label+mass_spectrum, rrv_x,rrv_mean_SCB,rrv_sigma_SCB,rrv_alpha1_SCB,rrv_n1_SCB);
            scb2 = RooCBShape("model_pdf_scb2"+label+mass_spectrum,"model_pdf_scb2"+label+mass_spectrum, rrv_x,rrv_mean_SCB,rrv_sigma_SCB,rrv_alpha2_SCB,rrv_n2_SCB);
            model_pdf=RooAddPdf("model_pdf"+label+mass_spectrum,"model_pdf"+label+mass_spectrum,RooArgList(scb1,scb2),RooArgList(frac))

        if in_model_name == "CB_v1":
            print label;
            label_tstring=TString(label);
            if label_tstring.Contains("_ggH600"): 
                rrv_mean_CB=RooRealVar("rrv_mean_CB"+label,"rrv_mean_CB"+label,600,550,650);
                rrv_sigma_CB=RooRealVar("rrv_sigma_CB"+label,"rrv_sigma_CB"+label,67,40,80);
                rrv_alpha_CB=RooRealVar("rrv_alpha_CB"+label,"rrv_alpha_CB"+label,-2,-5,-1.2);
            if label_tstring.Contains("_ggH700"):
                rrv_mean_CB=RooRealVar("rrv_mean_CB"+label,"rrv_mean_CB"+label,700,650,750);
                rrv_sigma_CB=RooRealVar("rrv_sigma_CB"+label,"rrv_sigma_CB"+label,100,40,150);
                rrv_alpha_CB=RooRealVar("rrv_alpha_CB"+label,"rrv_alpha_CB"+label,-2,-5,-1.2);
            if label_tstring.Contains("_ggH800"): 
                rrv_mean_CB=RooRealVar("rrv_mean_CB"+label,"rrv_mean_CB"+label,800,750,850);
                rrv_sigma_CB=RooRealVar("rrv_sigma_CB"+label,"rrv_sigma_CB"+label,130,120,140);
                #rrv_alpha_CB=RooRealVar("rrv_alpha_CB"+label,"rrv_alpha_CB"+label,-2,-5,-2);
                rrv_alpha_CB=RooRealVar("rrv_alpha_CB"+label,"rrv_alpha_CB"+label,1,0.5,4);
            if label_tstring.Contains("_ggH900"):
                rrv_mean_CB=RooRealVar("rrv_mean_CB"+label,"rrv_mean_CB"+label,900,850,900);
                rrv_sigma_CB=RooRealVar("rrv_sigma_CB"+label,"rrv_sigma_CB"+label,160,140,180);
                #rrv_alpha_CB=RooRealVar("rrv_alpha_CB"+label,"rrv_alpha_CB"+label,-2,-5,-2);
                rrv_alpha_CB=RooRealVar("rrv_alpha_CB"+label,"rrv_alpha_CB"+label,1,0.5,4);
            if label_tstring.Contains("_ggH1000"): 
                rrv_mean_CB=RooRealVar("rrv_mean_CB"+label,"rrv_mean_CB"+label,920,900,1000);
                rrv_sigma_CB=RooRealVar("rrv_sigma_CB"+label,"rrv_sigma_CB"+label,200,100,300);
                #rrv_alpha_CB=RooRealVar("rrv_alpha_CB"+label,"rrv_alpha_CB"+label,-5,-7,-5);
                rrv_alpha_CB=RooRealVar("rrv_alpha_CB"+label,"rrv_alpha_CB"+label,1,0.5,4);
            #rrv_sigma_CB=RooRealVar("rrv_sigma_CB"+label,"rrv_sigma_CB"+label,150,40,400);
            rrv_n_CB=RooRealVar("rrv_n_CB"+label,"rrv_n_CB"+label,4,1.,20);
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
            rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label,"rrv_offset_ErfExp"+label,500.,300.,800.);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label,"rrv_width_ErfExp"+label,60.,10,100.);
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
            rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label,"rrv_offset_ErfExp"+label,800.,10.,1400.);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label,"rrv_width_ErfExp"+label,24.,10,150.);
            rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,700,500,1200);
            rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label,"rrv_sigma_gaus"+label,150,10,300);
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
            rrv_c_ErfExp = RooRealVar("rrv_c_ErfExp"+label,"rrv_c_ErfExp"+label,-0.05,-0.2,0.);
            rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label,"rrv_offset_ErfExp"+label,100.,10.,140.);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label,"rrv_width_ErfExp"+label,30.,10,100.);
            rrv_mean1_gaus=RooRealVar("rrv_mean1_gaus"+label,"rrv_mean1_gaus"+label,82,78,87);
            rrv_mean2_gaus=RooRealVar("rrv_mean2_gaus"+label,"rrv_mean2_gaus"+label,180,170,190);
            rrv_sigma1_gaus=RooRealVar("rrv_sigma1_gaus"+label,"rrv_sigma1_gaus"+label,7,4,10);
            rrv_sigma2_gaus=RooRealVar("rrv_sigma2_gaus"+label,"rrv_sigma2_gaus"+label,10,7,15);
            rrv_high1 = RooRealVar("rrv_high1"+label,"rrv_high1"+label,0.6,0.,1.);
            rrv_high2 = RooRealVar("rrv_high2"+label,"rrv_high2"+label,0.4,0.,1.);
            #erfExp = ROOT.RooErfExpPdf("erfExp"+label,"erfExp"+label,rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp);
            erfExp = RooGenericPdf("erfExp"+label,"erfExp"+label, "TMath::Exp(%s*%s)*(1.+TMath::Erf((%s-%s)/%s))/2."%(rrv_c_ErfExp.GetName(),rrv_x.GetName(), rrv_x.GetName(),rrv_offset_ErfExp.GetName(), rrv_width_ErfExp.GetName()), RooArgList(rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp) )
            gaus1 = RooGaussian("gaus1"+label,"gaus1"+label, rrv_x,rrv_mean1_gaus,rrv_sigma1_gaus);
            gaus2 = RooGaussian("gaus2"+label,"gaus2"+label, rrv_x,rrv_mean2_gaus,rrv_sigma2_gaus);
            model_pdf =RooAddPdf("model_pdf"+label+mass_spectrum,"model_pdf"+label+mass_spectrum,RooArgList(erfExp,gaus1,gaus2),RooArgList(rrv_high1,rrv_high2))
    
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

        if in_model_name == "Keys":
            rdataset=self.workspace4fit_.data("rdataset_%s_signal_region_mlvj"%(self.higgs_sample))
            model_pdf = RooKeysPdf("model_pdf"+label+mass_spectrum,"model_pdf"+label+mass_spectrum, rrv_x,rdataset);

        getattr(self.workspace4fit_,"import")(model_pdf)
        return self.workspace4fit_.pdf("model_pdf"+label+mass_spectrum)
    
## ---------------------------------------------------
    def get_mj_Model(self,label):
        return self.workspace4fit_.pdf("model"+label+"_mj")

## ---------------------------------------------------
    def get_TTbar_mj_Model(self):
        rdataset_TTbar_mj=self.workspace4fit_.data("rdataset_TTbar_mj")
        model_TTbar=self.get_mj_Model("_TTbar");
        rdataset_TTbar_mj.Print()
        model_TTbar.Print()
        parameters_TTbar=model_TTbar.getParameters(rdataset_TTbar_mj);
        par=parameters_TTbar.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
        return self.workspace4fit_.pdf("model_TTbar_mj")

## ---------------------------------------------------
    def get_STop_mj_Model(self):
        rdataset_STop_mj=self.workspace4fit_.data("rdataset_STop_mj")
        model_STop=self.get_mj_Model("_STop");
        rdataset_STop_mj.Print()
        model_STop.Print()
        parameters_STop=model_STop.getParameters(rdataset_STop_mj);
        par=parameters_STop.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
        return self.workspace4fit_.pdf("model_STop_mj")

## ---------------------------------------------------
    def get_WW_mj_Model(self):
        rdataset_WW_mj=self.workspace4fit_.data("rdataset_WW_mj")
        model_WW=self.get_mj_Model("_WW");
        parameters_WW=model_WW.getParameters(rdataset_WW_mj);
        par=parameters_WW.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
        return self.workspace4fit_.pdf("model_WW_mj")
## ---------------------------------------------------
    def get_VV_mj_Model(self):
        rdataset_VV_mj=self.workspace4fit_.data("rdataset_VV_mj")
        model_VV=self.get_mj_Model("_VV");
        parameters_VV=model_VV.getParameters(rdataset_VV_mj);
        par=parameters_VV.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
        return self.workspace4fit_.pdf("model_VV_mj")


## ---------------------------------------------------
    def get_WJets_mj_Model(self):
        rdataset_WJets_mj=self.workspace4fit_.data("rdataset_WJets_mj")
        model_WJets=self.get_mj_Model("_WJets");
        parameters_WJets=model_WJets.getParameters(rdataset_WJets_mj);
        par=parameters_WJets.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            paraName=TString(param.GetName());
            #if not ( paraName.Contains("rrv_width_ErfExp_WJets") or paraName.Contains("rrv_c_ErfExp_WJets") or paraName.Contains("rrv_number_WJets")) :param.setConstant(kTRUE);
            #if not ( paraName.Contains("rrv_offset_ErfExp_WJets") or paraName.Contains("rrv_c_ErfExp_WJets") or paraName.Contains("rrv_number_WJets")) :param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
        return self.workspace4fit_.pdf("model_WJets_mj")
## ---------------------------------------------------
    def get_mlvj_Model(self,label, mj_region):
        return self.workspace4fit_.pdf("model"+label+mj_region+"_mlvj")
## ---------------------------------------------------
    def get_mlvj_shape(self,label, mj_region):
        rdataset_mlvj=self.workspace4fit_.data("rdataset_%s%s_mlvj"%(label,mj_region))
        model=self.workspace4fit_.pdf("model_pdf"+label+mj_region+"_mlvj")
        parameters=model.getParameters(rdataset_mlvj);
        par=parameters.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            #param.setConstant(kTRUE);
            param.Print();
            param=par.Next()

        return self.workspace4fit_.pdf("model_pdf"+label+mj_region+"_mlvj")
## ---------------------------------------------------
    def get_TTbar_mlvj_Model(self, mj_region="_signal_region"):
        rdataset_TTbar_mlvj=self.workspace4fit_.data("rdataset_TTbar%s_mlvj"%(mj_region))
        model_TTbar=self.get_mlvj_Model("_TTbar",mj_region);
        model_TTbar.Print()
        parameters_TTbar=model_TTbar.getParameters(rdataset_TTbar_mlvj);
        par=parameters_TTbar.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
        return model_TTbar

## ---------------------------------------------------
    def get_STop_mlvj_Model(self, mj_region="_signal_region"):
        rdataset_STop_mlvj=self.workspace4fit_.data("rdataset_STop%s_mlvj"%(mj_region))
        model_STop=self.get_mlvj_Model("_STop",mj_region);
        model_STop.Print()
        parameters_STop=model_STop.getParameters(rdataset_STop_mlvj);
        par=parameters_STop.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
        return model_STop


## ---------------------------------------------------
    def get_ggH_mlvj_Model(self, mj_region="_signal_region"):
        rdataset_ggH_mlvj=self.workspace4fit_.data("rdataset_%s%s"%(self.higgs_sample,mj_region)+"_mlvj")
        model_ggH=self.get_mlvj_Model("_%s"%(self.higgs_sample),mj_region);
        rdataset_ggH_mlvj.Print()
        model_ggH.Print()
        parameters_ggH=model_ggH.getParameters(rdataset_ggH_mlvj);
        par=parameters_ggH.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
        return model_ggH

## ---------------------------------------------------
    def get_WW_mlvj_Model(self, mj_region="_signal_region"):
        rdataset_WW_mlvj=self.workspace4fit_.data("rdataset_WW%s_mlvj"%(mj_region))
        model_WW=self.get_mlvj_Model("_WW",mj_region);
        model_WW.Print()
        rdataset_WW_mlvj.Print()
        parameters_WW=model_WW.getParameters(rdataset_WW_mlvj);
        par=parameters_WW.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
        return model_WW

## ---------------------------------------------------
    def get_VV_mlvj_Model(self, mj_region="_signal_region"):
        rdataset_VV_mlvj=self.workspace4fit_.data("rdataset_VV%s_mlvj"%(mj_region))
        model_VV=self.get_mlvj_Model("_VV",mj_region);
        model_VV.Print()
        rdataset_VV_mlvj.Print()
        parameters_VV=model_VV.getParameters(rdataset_VV_mlvj);
        par=parameters_VV.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
        return model_VV
    ## ---------------------------------------------------
    #def get_other_backgrounds_mlvj_Model(self, mj_region="_signal_region"):
        #rdataset_other_backgrounds_mlvj=self.workspace4fit_.data("rdataset_other_backgrounds%s_mlvj"%(mj_region))
        #model_other_backgrounds=self.get_mlvj_Model("_other_backgrounds",mj_region);
        #model_other_backgrounds.Print()
        #rdataset_other_backgrounds_mlvj.Print()
        #parameters_other_backgrounds=model_other_backgrounds.getParameters(rdataset_other_backgrounds_mlvj);
        #par=parameters_other_backgrounds.createIterator();
        #par.Reset();
        #param=par.Next()
        #while (param):
            #param.setConstant(kTRUE);
            #param.Print();
            #param=par.Next()
        #return model_other_backgrounds

    ## ---------------------------------------------------
    def get_WJets_mlvj_Model(self, mj_region="_signal_region"):
        print "get_WJets_mlvj_Model"
        rdataset_WJets_mlvj=self.workspace4fit_.data("rdataset_WJets%s_mlvj"%(mj_region))
        model_WJets=self.get_mlvj_Model("_WJets",mj_region);
        model_WJets.Print()
        rdataset_WJets_mlvj.Print()
        parameters_WJets=model_WJets.getParameters(rdataset_WJets_mlvj);
        par=parameters_WJets.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            paraName=TString(param.GetName());
            param.Print();
            if paraName.Contains("rrv_number_WJets"): 
                if self.workspace4fit_.var("rrv_number_WJets_in_mj%s_from_fitting"%(mj_region)):
                    self.workspace4fit_.var("rrv_number_WJets_in_mj%s_from_fitting"%(mj_region)).Print()
                    param.setVal( self.workspace4fit_.var("rrv_number_WJets_in_mj%s_from_fitting"%(mj_region)).getVal() )
                if mj_region=="_signal_region": param.setConstant(kTRUE);
            param.Print();
            #raw_input("ENTer")
            param=par.Next()
        return model_WJets

    ## ---------------------------------------------------
    def fix_Model(self, label, mj_region="_signal_region",mass_spectrum="_mlvj"):
        rdataset=self.workspace4fit_.data("rdataset%s%s%s"%(label,mj_region,mass_spectrum))
        model=self.get_mlvj_Model(label,mj_region);
        model.Print()
        parameters=model.getParameters(rdataset);
        par=parameters.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
    ## ---------------------------------------------------
    def fix_Pdf(self,model_pdf,argset_notparameter):
        model_pdf.Print()
        parameters=model_pdf.getParameters(argset_notparameter);
        par=parameters.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
    ## ---------------------------------------------------
    def get_WJets_mlvj_correction_sb_lo_to_signal_region(self):#exo-vv method: extract M_lvj shape of signal_region from sb_lo
        print "get_WJets_mlvj_correction_sb_lo_to_signal_region"
        rdataset_WJets_sb_lo_mlvj=self.workspace4fit_.data("rdataset_WJets_sb_lo_mlvj")
        rdataset_WJets_signal_region_mlvj=self.workspace4fit_.data("rdataset_WJets_signal_region_mlvj")
        model_sb_lo_WJets=self.get_mlvj_shape("_WJets","_sb_lo");
        model_signal_region_WJets=self.get_mlvj_shape("_WJets","_signal_region");
        model_sb_lo_WJets.Print();model_signal_region_WJets.Print()
        parameters_WJets_sb_lo=model_sb_lo_WJets.getParameters(rdataset_WJets_sb_lo_mlvj);
        parameters_WJets_signal_region=model_signal_region_WJets.getParameters(rdataset_WJets_signal_region_mlvj);

        par_sb_lo=parameters_WJets_sb_lo.createIterator();
        par_sb_lo.Reset();
        param=par_sb_lo.Next()
        index_par_sb_lo=0
        while (param):
            paraName=TString(param.GetName());
            #param.Print();
            if index_par_sb_lo==0: rrv_c_sb_lo=param;
            if index_par_sb_lo==1: rrv_offset_sb_lo=param;
            if index_par_sb_lo==2: rrv_width_sb_lo=param;
            param=par_sb_lo.Next()
            index_par_sb_lo=index_par_sb_lo+1

        par_signal_region=parameters_WJets_signal_region.createIterator();
        par_signal_region.Reset();
        param=par_signal_region.Next()
        index_par_signal_region=0
        while (param):
            paraName=TString(param.GetName());
            #param.Print();
            if index_par_signal_region==0: rrv_c_signal_region=param;
            if index_par_signal_region==1: rrv_offset_signal_region=param;
            if index_par_signal_region==2: rrv_width_signal_region=param;
            param=par_signal_region.Next()
            index_par_signal_region=index_par_signal_region+1



        rrv_c_sb_lo.setConstant(kTRUE);
        rrv_offset_sb_lo.setConstant(kTRUE);
        rrv_width_sb_lo.setConstant(kTRUE); 
        rrv_c_signal_region.setConstant(kTRUE);
        rrv_offset_signal_region.setConstant(kTRUE);
        rrv_width_signal_region.setConstant(kTRUE);
        rrv_c_sb_lo.Print();rrv_offset_sb_lo.Print();rrv_width_sb_lo.Print(); rrv_c_signal_region.Print();rrv_offset_signal_region.Print();rrv_width_signal_region.Print();

        rrv_x = self.workspace4fit_.var("rrv_mass_lvj"); 
        correct_factor = RooFormulaVar("correct_factor", "(TMath::Exp(@1*@0)*(1.+TMath::Erf((@0-@2)/@3))/2.)/(TMath::Exp(@4*@0)*(1.+TMath::Erf((@0-@5)/@6))/2.)", RooArgList(rrv_x,rrv_c_signal_region, rrv_offset_signal_region, rrv_width_signal_region, rrv_c_sb_lo, rrv_offset_sb_lo, rrv_width_sb_lo))

        f1_correct_factor = TF1("f1_correct_factor", "(TMath::Exp([0]*x)*(1.+TMath::Erf((x-[1])/[2]))/2.)/(TMath::Exp([3]*x)*(1.+TMath::Erf((x-[4])/[5]))/2.)",rrv_x.getMin(), rrv_x.getMax())#, 
        f1_correct_factor.SetParameters(rrv_c_signal_region.getVal(), rrv_offset_signal_region.getVal(), rrv_width_signal_region.getVal(), rrv_c_sb_lo.getVal(), rrv_offset_sb_lo.getVal(), rrv_width_sb_lo.getVal())
        f1_correct_factor.SetLineWidth(2);
        self.draw_canvas1(f1_correct_factor,"plots/other/","correction_WJets_M_lvj_sb_lo_to_signal_region",1);

        model_pdf_WJets_sb_lo_from_fitting_mlvj=self.workspace4fit_.pdf("model_pdf_WJets_sb_lo_from_fitting_mlvj")
        model_pdf_WJets_signal_region_after_correct=RooEffProd("model_pdf_WJets_signal_region_after_correct","model_pdf_WJets_signal_region_after_correct",model_pdf_WJets_sb_lo_from_fitting_mlvj,correct_factor)
        #model_pdf_WJets_signal_region_after_correct=model_signal_region_WJets.Clone("model_pdf_WJets_signal_region_after_correct")
        model_pdf_WJets_signal_region_after_correct.Print()
        self.fix_Pdf(model_pdf_WJets_signal_region_after_correct,RooArgSet(rrv_x))
        getattr(self.workspace4fit_,"import")(model_pdf_WJets_signal_region_after_correct)
        self.workspace4fit_.var("rrv_number_WJets_signal_region_mlvj").setVal(self.workspace4fit_.var("rrv_number_WJets_in_mj_signal_region_from_fitting").getVal());
        self.workspace4fit_.var("rrv_number_WJets_signal_region_mlvj").setConstant(kTRUE);

#        print "Systematic estimate"
        #rfresult_WJets_sb_lo_mlvj=self.workspace4fit_.obj("rfresult_WJets_sb_lo_mlvj");
        #rfresult_WJets_sb_lo_mlvj.Print()
        #cov_sb_lo=rfresult_WJets_sb_lo_mlvj.covarianceMatrix()
        #cov_sb_lo.Print()
        #rfresult_WJets_signal_region_mlvj=self.workspace4fit_.obj("rfresult_WJets_signal_region_mlvj");
        #rfresult_WJets_signal_region_mlvj.Print()
        #cov_signal_region=rfresult_WJets_signal_region_mlvj.covarianceMatrix()
        #cov_signal_region.Print()

        #print "formular"
        ##correct_factor = RooFormulaVar("correct_factor", "(TMath::Exp(@1*@0)*(1.+TMath::Erf((@0-@2)/@3))/2.)/(TMath::Exp(@4*@0)*(1.+TMath::Erf((@0-@5)/@6))/2.)", RooArgList(rrv_x,rrv_c_signal_region, rrv_offset_signal_region, rrv_width_signal_region, rrv_c_sb_lo, rrv_offset_sb_lo, rrv_width_sb_lo))
        #J_c_sb_lo = RooFormulaVar("J_c_sb_lo","TMath::Exp(@1*@0)*@0*(1.+TMath::Erf((@0-@2)/@3))/2.", RooArgList(rrv_x, rrv_c_sb_lo, rrv_offset_sb_lo, rrv_width_sb_lo))
        #J_offset_sb_lo = RooFormulaVar("J_offset_sb_lo","0.-TMath::Exp(@1*@0-(@0-@2)*(@0-@2)/@3/@3)/@3/1.77245385090551588", RooArgList(rrv_x, rrv_c_sb_lo, rrv_offset_sb_lo, rrv_width_sb_lo))
        #J_width_sb_lo = RooFormulaVar("J_width_sb_lo","0.-TMath::Exp(@1*@0-(@0-@2)*(@0-@2)/@3/@3)*(@0-@2)/@3/@3/1.77245385090551588", RooArgList(rrv_x, rrv_c_sb_lo, rrv_offset_sb_lo, rrv_width_sb_lo))
        #var_sb_lo=RooFormulaVar("var_sb_lo","@0*@0*%s+@0*@1*%s+@0*@2*%s + @1*@0*%s+@1*@1*%s+@1*@2*%s + @2*@0*%s+@2*@1*%s+@2*@2*%s"%(cov_sb_lo[0][0],cov_sb_lo[0][2],cov_sb_lo[0][3],cov_sb_lo[2][0],cov_sb_lo[2][2],cov_sb_lo[2][3],cov_sb_lo[3][0],cov_sb_lo[3][2],cov_sb_lo[3][3]),RooArgList(J_c_sb_lo, J_offset_sb_lo, J_width_sb_lo))
        #raw_input("ENTER")


    ############# ---------------------------------------------------
    def fit_m_j_single_MC_sample(self,in_file_name, label, in_model_name):
        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j"); 
        #dataset
        rdataset_mj = self.workspace4fit_.data("rdataset4fit"+label+"_mj"); 
        rdataset_mj.Print();

        model = self.make_Model(label,in_model_name);
        # fit to a Model
        rfresult = model.fitTo(rdataset_mj,RooFit.Save(1), RooFit.SumW2Error(kTRUE) ,RooFit.Extended(kTRUE) );
        rfresult = model.fitTo(rdataset_mj,RooFit.Save(1), RooFit.SumW2Error(kTRUE) ,RooFit.Extended(kTRUE) );
        
        mplot = rrv_mass_j.frame(RooFit.Title(in_file_name+" fitted by "+in_model_name));
        rdataset_mj.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) , RooFit.VLines());
        #model.plotOn( mplot, RooFit.VisualizeError(rfresult,1),RooFit.FillColor(kOrange) , RooFit.VLines());
        model.plotOn(mplot,RooFit.VisualizeError(rfresult,1,kFALSE),RooFit.DrawOption("F"),RooFit.FillColor(kOrange), RooFit.VLines());
        rdataset_mj.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) , RooFit.VLines());
        model.plotOn( mplot , RooFit.VLines());
        #pull
        hpull=mplot.pullHist();
        mplot_pull = rrv_mass_j.frame(RooFit.Title("Pull Distribution"));
        mplot_pull.addPlotable(hpull,"P");
        mplot_pull.SetTitle("PULL");
        mplot_pull.GetYaxis().SetRangeUser(-5,5);
         
        parameters_list=model.getParameters(rdataset_mj);
        self.draw_canvas( mplot, mplot_pull,parameters_list, "plots/m_j_BDTcut/", in_file_name, in_model_name)
        
        rfresult.Print();
        #normalize the number of total events to lumi
        self.workspace4fit_.var("rrv_number"+label+"_mj").Print()
        self.workspace4fit_.var("rrv_scale_to_lumi"+label).Print()
        self.workspace4fit_.var("rrv_number"+label+"_mj").setVal( self.workspace4fit_.var("rrv_number"+label+"_mj").getVal()*self.workspace4fit_.var("rrv_scale_to_lumi"+label).getVal()  )
        self.workspace4fit_.var("rrv_number"+label+"_mj").setError(self.workspace4fit_.var("rrv_number"+label+"_mj").getError()*self.workspace4fit_.var("rrv_scale_to_lumi"+label).getVal()  )
        if TString(label).Contains("ggH"):
            self.workspace4fit_.var("rrv_number"+label+"_mj").setVal( self.workspace4fit_.var("rrv_number"+label+"_mj").getVal()/self.higgs_xs_scale  )
            self.workspace4fit_.var("rrv_number"+label+"_mj").setError(self.workspace4fit_.var("rrv_number"+label+"_mj").getError()/self.higgs_xs_scale  )
        self.workspace4fit_.var("rrv_number"+label+"_mj").Print()

        #raw_input("ENTER")
    
        ##chi2 fit begin
        #rdataHist=rdataset_mj.binnedClone();
        #rdataHist.Print("v");
        #chi2=ROOT.RooChi2Var("chi2","chi2",model,rdataHist,RooFit.DataError(RooAbsData.SumW2));
        #m=ROOT.RooMinuit(chi2);
        #m.migrad();
        #m.hesse();
        #r_chi2_wgt=m.save();
        #mplot2 = rrv_mass_j.frame(RooFit.Title(in_file_name+" fitted by "+in_model_name));
        #rdataset_mj.plotOn( mplot2 ,RooFit.DataError(RooAbsData.SumW2) );
        #model.plotOn( mplot2, RooFit.VisualizeError(rfresult,1),RooFit.FillColor(kOrange) );
        #rdataset_mj.plotOn( mplot2 ,RooFit.DataError(RooAbsData.SumW2) );
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
    
        return [rfresult,parameters_list,rdataset_mj];
 
    ############# ---------------------------------------------------
    def fit_m_j_single_MC_sample_TTbar_contralsample(self,in_file_name, label, in_model_name):
        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j"); 
        #dataset
        #rdataset_mj = self.workspace4fit_.data("rdataset4fit"+label+"_mj"); 
        rdataset_mj = self.workspace4fit_.data("rdataset"+label+"_mj"); 
        rdataset_mj.Print();

        model = self.make_Model(label,in_model_name);
        # fit to a Model
        rfresult = model.fitTo(rdataset_mj,RooFit.Save(1), RooFit.SumW2Error(kTRUE) ,RooFit.Extended(kTRUE) );
        rfresult = model.fitTo(rdataset_mj,RooFit.Save(1), RooFit.SumW2Error(kTRUE) ,RooFit.Extended(kTRUE) );
        
        mplot = rrv_mass_j.frame(RooFit.Title(in_file_name+" fitted by "+in_model_name));
        rdataset_mj.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) , RooFit.VLines());
        model.plotOn( mplot, RooFit.VisualizeError(rfresult,1),RooFit.FillColor(kOrange) , RooFit.VLines());
        #model.plotOn(mplot,RooFit.VisualizeError(rfresult,1,kFALSE),RooFit.DrawOption("F"),RooFit.FillColor(kOrange), RooFit.VLines());
        rdataset_mj.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) , RooFit.VLines());
        model.plotOn( mplot , RooFit.VLines());
        model.plotOn( mplot, RooFit.Components("erfExp"+label), RooFit.LineStyle(kDashed),RooFit.LineColor(kGreen) , RooFit.VLines());
        model.plotOn( mplot, RooFit.Components("gaus"+label), RooFit.LineStyle(kDashed),RooFit.LineColor(kRed) , RooFit.VLines());
        model.plotOn( mplot , RooFit.VLines());
        #pull
        hpull=mplot.pullHist();
        mplot_pull = rrv_mass_j.frame(RooFit.Title("Pull Distribution"));
        mplot_pull.addPlotable(hpull,"P");
        mplot_pull.SetTitle("PULL");
        mplot_pull.GetYaxis().SetRangeUser(-5,5);
         
        parameters_list=model.getParameters(rdataset_mj);
        self.draw_canvas( mplot, mplot_pull,parameters_list, "plots/m_j_BDTcut_TTbar_contralsample/", in_file_name, in_model_name)
        
        rfresult.Print();
    
        return [rfresult,parameters_list,rdataset_mj];
    ############# ---------------------------------------------------
    def change_dataset_to_histpdf(self, x,dataset):
        datahist=dataset.binnedClone(dataset.GetName()+"_binnedClone",dataset.GetName()+"_binnedClone")
        datahist.Print()
        histpdf=RooHistPdf(dataset.GetName()+"_histpdf",dataset.GetName()+"_histpdf",RooArgSet(x),datahist)
        histpdf.Print()
        #raw_input("ENTER")
        getattr(self.workspace4fit_,"import")(histpdf)
        return self.workspace4fit_.pdf(dataset.GetName()+"_histpdf")
        
    ############# ---------------------------------------------------
    def fit_m_j_TTbar_contralsample(self,in_file_name,  in_model_name):
        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j");# rrv_mass_j.setBins(40)
        #dataset
        rdataset_data_mj = self.workspace4fit_.data("rdataset_data_mj"); 
        rdataset_TTbar_mj = self.workspace4fit_.data("rdataset_TTbar_mj"); 
        rdataset_STop_mj = self.workspace4fit_.data("rdataset_STop_mj"); 
        rdataset_VV_mj = self.workspace4fit_.data("rdataset_VV_mj"); 
        rdataset_WJets_mj = self.workspace4fit_.data("rdataset_WJets_mj"); 
        rdataset_TotalMC_mj= rdataset_TTbar_mj.Clone("rdataset_TotalMC_mj");
        rdataset_TotalMC_mj.append(rdataset_STop_mj);
        rdataset_TotalMC_mj.append(rdataset_VV_mj);
        rdataset_TotalMC_mj.append(rdataset_WJets_mj);

        self.change_dataset_to_histpdf(rrv_mass_j, rdataset_TTbar_mj);
        self.change_dataset_to_histpdf(rrv_mass_j, rdataset_STop_mj)
        self.change_dataset_to_histpdf(rrv_mass_j, rdataset_VV_mj)
        self.change_dataset_to_histpdf(rrv_mass_j, rdataset_WJets_mj)
        model_pdf_TTbar= self.workspace4fit_.pdf(rdataset_TTbar_mj.GetName()+"_histpdf")
        model_pdf_STop = self.workspace4fit_.pdf(rdataset_STop_mj.GetName()+"_histpdf")
        model_pdf_VV   = self.workspace4fit_.pdf(rdataset_VV_mj.GetName()+"_histpdf")
        model_pdf_WJets   = self.workspace4fit_.pdf(rdataset_WJets_mj.GetName()+"_histpdf")
        scale_number_STop =rdataset_STop_mj.sumEntries()/rdataset_data_mj.sumEntries()
        scale_number_TTbar=rdataset_TTbar_mj.sumEntries()/rdataset_data_mj.sumEntries()
        scale_number_VV   =rdataset_VV_mj.sumEntries()/rdataset_data_mj.sumEntries()
        scale_number_WJets=rdataset_WJets_mj.sumEntries()/rdataset_data_mj.sumEntries()
        

        model = self.make_Model("_data",in_model_name);
        model_TotalMC = self.make_Model("_TotalMC",in_model_name);
        # fit to a Model
        model.fitTo(rdataset_data_mj,RooFit.Save(1), RooFit.Extended(kTRUE) );
        rfresult = model.fitTo(rdataset_data_mj,RooFit.Save(1), RooFit.Extended(kTRUE) );
        #fit the TotalMC
        model_TotalMC.fitTo(rdataset_TotalMC_mj,RooFit.Save(1), RooFit.Extended(kTRUE) );
        model_TotalMC.fitTo(rdataset_TotalMC_mj,RooFit.Save(1), RooFit.Extended(kTRUE) );
        scale_number_TotalMC=rdataset_TotalMC_mj.sumEntries()/rdataset_data_mj.sumEntries()
        
        mplot = rrv_mass_j.frame(RooFit.Title(in_file_name+" fitted by "+in_model_name));

        rdataset_data_mj.plotOn( mplot, RooFit.Invisible() );

        model_pdf_STop.plotOn(mplot,RooFit.Normalization(scale_number_STop),RooFit.Name("STop_invisible"),RooFit.Invisible(), RooFit.VLines(),RooFit.Precision(1e-8))
        model_pdf_TTbar.plotOn(mplot,RooFit.Normalization(scale_number_TTbar),RooFit.Name("TTbar_invisible"), RooFit.AddTo("STop_invisible"),RooFit.Invisible(), RooFit.VLines(),RooFit.Precision(1e-8))
        model_pdf_VV.plotOn(mplot,RooFit.Normalization(scale_number_VV),RooFit.Name("VV_invisible"), RooFit.AddTo("TTbar_invisible"),RooFit.Invisible(), RooFit.VLines(),RooFit.Precision(1e-8))
        model_pdf_WJets.plotOn(mplot,RooFit.Normalization(scale_number_WJets),RooFit.Name("WJets_invisible"), RooFit.AddTo("VV_invisible"),RooFit.Invisible(), RooFit.VLines(),RooFit.Precision(1e-8))
        model_pdf_WJets.plotOn(mplot,RooFit.Normalization(scale_number_WJets),RooFit.Name("WJets"), RooFit.AddTo("VV_invisible"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["WJets"]), RooFit.LineColor(self.color_palet["WJets"]), RooFit.VLines(),RooFit.Precision(1e-8))
        model_pdf_VV.plotOn(mplot,RooFit.Normalization(scale_number_VV),RooFit.Name("VV"), RooFit.AddTo("TTbar_invisible"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["VV"]), RooFit.LineColor(self.color_palet["VV"]), RooFit.VLines(),RooFit.Precision(1e-8))
        model_pdf_TTbar.plotOn(mplot,RooFit.Normalization(scale_number_TTbar),RooFit.Name("TTbar"), RooFit.AddTo("STop_invisible"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["TTbar"]), RooFit.LineColor(self.color_palet["TTbar"]), RooFit.VLines(),RooFit.Precision(1e-8))
        model_pdf_STop.plotOn(mplot,RooFit.Normalization(scale_number_STop),RooFit.Name("STop"), RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["STop"]), RooFit.LineColor(self.color_palet["STop"]), RooFit.VLines(),RooFit.Precision(1e-8))

        rdataset_data_mj.plotOn( mplot,RooFit.Name("data") );
        model_TotalMC.plotOn( mplot,RooFit.Normalization(scale_number_TotalMC) ,RooFit.Name("MC fit") , RooFit.VLines(),RooFit.LineStyle(kDashed));
        model.plotOn( mplot,RooFit.Name("data fit") , RooFit.VLines());
        leg=self.legend4Plot(mplot,0)
        mplot.addObject(leg)

        #add mean and width to mplot
        parameters_list=model.getParameters(rdataset_data_mj);
        parameters_list.add( model_TotalMC.getParameters(rdataset_data_mj))
        rrv_mean_gaus_data=parameters_list.find("rrv_mean_gaus_data");
        rrv_sigma_gaus_data=parameters_list.find("rrv_sigma_gaus_data");
        rrv_mean_gaus_TotalMC=parameters_list.find("rrv_mean_gaus_TotalMC");
        rrv_sigma_gaus_TotalMC=parameters_list.find("rrv_sigma_gaus_TotalMC");
        tl_MC_mean   =TLatex(130,50, ("Mean_{MC  } = %3.1f #pm %2.1f")%(rrv_mean_gaus_TotalMC.getVal(), rrv_mean_gaus_TotalMC.getError()) );
        tl_MC_sigma  =TLatex(130,43, ("Sigma_{MC  }= %2.1f #pm %2.1f")%(rrv_sigma_gaus_TotalMC.getVal(), rrv_sigma_gaus_TotalMC.getError()) );
        tl_data_mean =TLatex(130,36, ("Mean_{data} = %3.1f #pm %2.1f")%(rrv_mean_gaus_data.getVal(), rrv_mean_gaus_data.getError()) );
        tl_data_sigma=TLatex(130,29, ("Sigma_{data}= %2.1f #pm %2.1f")%(rrv_sigma_gaus_data.getVal(), rrv_sigma_gaus_data.getError()) );
        tl_data_mean.SetTextSize(0.03)
        tl_data_sigma.SetTextSize(0.03)
        tl_MC_mean.SetTextSize(0.03)
        tl_MC_sigma.SetTextSize(0.03)
        mplot.addObject(tl_data_mean);
        mplot.addObject(tl_data_sigma);
        mplot.addObject(tl_MC_mean);
        mplot.addObject(tl_MC_sigma);
        #draw line
        lowerLine = TLine(self.mj_signal_min,0.,self.mj_signal_min,mplot.GetMaximum()); lowerLine.SetLineWidth(2); lowerLine.SetLineColor(kGray+2); lowerLine.SetLineStyle(9);
        upperLine = TLine(self.mj_signal_max,0.,self.mj_signal_max,mplot.GetMaximum()); upperLine.SetLineWidth(2); upperLine.SetLineColor(kGray+2); upperLine.SetLineStyle(9);
        mplot.addObject(lowerLine);
        mplot.addObject(upperLine);
 
        #pull
        hpull=mplot.pullHist();
        mplot_pull = rrv_mass_j.frame(RooFit.Title("Pull Distribution"));
        mplot_pull.addPlotable(hpull,"P");
        mplot_pull.SetTitle("PULL");
        mplot_pull.GetYaxis().SetRangeUser(-5,5);
         
        self.draw_canvas( mplot, mplot_pull,parameters_list, "plots/m_j_BDTcut_TTbar_contralsample/", in_file_name, in_model_name+"Total")
        
        #rfresult.Print();
        
        #calculate the mva eff
        self.workspace4fit_.var("rrv_number_dataset_signal_region_data_mj").Print()
        self.workspace4fit_.var("rrv_number_dataset_signal_region_VV_mj").Print()
        self.workspace4fit_.var("rrv_number_dataset_signal_region_WJets_mj").Print()
        self.workspace4fit_.var("rrv_number_dataset_signal_region_STop_mj").Print()
        self.workspace4fit_.var("rrv_number_dataset_signal_region_TTbar_mj").Print()

    
    ########## ---------------------------------------------------
    def get_mj_and_mlvj_dataset(self,in_file_name, label):# to get the shape of m_lvj
        # read in tree
        fileIn_name=TString(self.file_Directory+in_file_name);
        fileIn = TFile(fileIn_name.Data());
        treeIn = fileIn.Get("otree");
        
        # define bdt reader
        listOfTrainingVariables1 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1"];
        #bdtSimple = tmvaApplicator( listOfTrainingVariables1, "weights/%s/Wtagger_200to275_simple_BDT.weights.xml"%(self.higgs_sample));
        bdtSimple = tmvaApplicator( listOfTrainingVariables1, "weights/General/Wtagger_200to275_simple_BDT.weights.xml");
            
        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j") 
        rrv_mass_lvj = self.workspace4fit_.var("rrv_mass_lvj") 
        rrv_weight = RooRealVar("rrv_weight","rrv_weight",0. ,10000000.) 
        #dataset of m_j
        rdataset_mj = RooDataSet("rdataset"+label+"_mj","rdataset"+label+"_mj",RooArgSet(rrv_mass_j,rrv_weight),RooFit.WeightVar(rrv_weight) );
        rdataset4fit_mj = RooDataSet("rdataset4fit"+label+"_mj","rdataset4fit"+label+"_mj",RooArgSet(rrv_mass_j,rrv_weight),RooFit.WeightVar(rrv_weight) );
        #dataset of m_lvj
        rdataset_sb_lo_mlvj  = RooDataSet("rdataset"+label+"_sb_lo"+"_mlvj","rdataset"+label+"_sb_lo"+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        rdataset_signal_region_mlvj = RooDataSet("rdataset"+label+"_signal_region_mlvj","rdataset"+label+"_signal_region_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        rdataset_sb_hi_mlvj  = RooDataSet("rdataset"+label+"_sb_hi"+"_mlvj","rdataset"+label+"_sb_hi"+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        rdataset4fit_sb_lo_mlvj  = RooDataSet("rdataset4fit"+label+"_sb_lo"+"_mlvj","rdataset4fit"+label+"_sb_lo"+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        rdataset4fit_signal_region_mlvj = RooDataSet("rdataset4fit"+label+"_signal_region_mlvj","rdataset4fit"+label+"_signal_region_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        rdataset4fit_sb_hi_mlvj  = RooDataSet("rdataset4fit"+label+"_sb_hi"+"_mlvj","rdataset4fit"+label+"_sb_hi"+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 

        # make cuts (including mass drop) # create a RooDataSet
        print "N entries: ", treeIn.GetEntries()
        #raw_input("Enter")
        hnum_4region=TH1D("hnum_4region"+label,"hnum_4region"+label,4,-1.5,2.5);# m_j   -1: sb_lo; 0:signal_region; 1: sb_hi; 2:total
        hnum_2region=TH1D("hnum_2region"+label,"hnum_2region"+label,2,-0.5,1.5);# m_lvj  0: signal_region; 1: total
        for i in range(treeIn.GetEntries()):
            if i % 10000 == 0: print "i: ",i
            treeIn.GetEntry(i);
            if i==0: tmp_scale_to_lumi=treeIn.wSampleWeight;
    
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
             
            if treeIn.jet_pt_pr > 200. and discriminantCut and treeIn.jet_mass_pr >= rrv_mass_j.getMin() and treeIn.jet_mass_pr<rrv_mass_j.getMax() and treeIn.njets ==0 and treeIn.mass_lvj >= rrv_mass_lvj.getMin() and treeIn.mass_lvj<rrv_mass_lvj.getMax() :
                tmp_event_weight= treeIn.totalEventWeight;
                tmp_event_weight4fit= treeIn.eff_and_pu_Weight;
                tmp_interference_weight_H600=treeIn.interference_Weight_H600;
                tmp_interference_weight_H700=treeIn.interference_Weight_H700;
                tmp_interference_weight_H800=treeIn.interference_Weight_H800;
                tmp_interference_weight_H900=treeIn.interference_Weight_H900;
                tmp_interference_weight_H1000=treeIn.interference_Weight_H1000;
                if label=="_ggH600":
                    #tmp_event_weight=tmp_event_weight/self.higgs_xs_scale*tmp_interference_weight_H600
                    tmp_event_weight=tmp_event_weight*tmp_interference_weight_H600
                    tmp_event_weight4fit=tmp_event_weight4fit*tmp_interference_weight_H600
                if label=="_ggH700":
                    #tmp_event_weight=tmp_event_weight/self.higgs_xs_scale*tmp_interference_weight_H700
                    tmp_event_weight=tmp_event_weight*tmp_interference_weight_H700
                    tmp_event_weight4fit=tmp_event_weight4fit*tmp_interference_weight_H700
                if label=="_ggH800":
                    #tmp_event_weight=tmp_event_weight/self.higgs_xs_scale*tmp_interference_weight_H800
                    tmp_event_weight=tmp_event_weight*tmp_interference_weight_H800
                    tmp_event_weight4fit=tmp_event_weight4fit*tmp_interference_weight_H800
                if label=="_ggH900":
                    #tmp_event_weight=tmp_event_weight/self.higgs_xs_scale*tmp_interference_weight_H900
                    tmp_event_weight=tmp_event_weight*tmp_interference_weight_H900
                    tmp_event_weight4fit=tmp_event_weight4fit*tmp_interference_weight_H900
                if label=="_ggH1000":
                    #tmp_event_weight=tmp_event_weight/self.higgs_xs_scale*tmp_interference_weight_H1000
                    tmp_event_weight=tmp_event_weight*tmp_interference_weight_H1000
                    tmp_event_weight4fit=tmp_event_weight4fit*tmp_interference_weight_H1000
                # for multi-sample, like STop and VV. There are two sample, and two wSampleWeight_value.Use the least wSampleWeight as scale. 
                tmp_event_weight4fit=tmp_event_weight4fit*treeIn.wSampleWeight/tmp_scale_to_lumi
                rrv_mass_lvj.setVal(treeIn.mass_lvj);
                if treeIn.jet_mass_pr >= self.mj_sideband_lo_min and treeIn.jet_mass_pr < self.mj_sideband_lo_max:
                    rdataset_sb_lo_mlvj.add( RooArgSet( rrv_mass_lvj ), tmp_event_weight );
                    rdataset4fit_sb_lo_mlvj.add( RooArgSet( rrv_mass_lvj ), tmp_event_weight4fit );
                if treeIn.jet_mass_pr >= self.mj_signal_min      and treeIn.jet_mass_pr < self.mj_signal_max:
                    rdataset_signal_region_mlvj.add( RooArgSet( rrv_mass_lvj ), tmp_event_weight );
                    rdataset4fit_signal_region_mlvj.add( RooArgSet( rrv_mass_lvj ), tmp_event_weight4fit );
                    hnum_2region.Fill(1,tmp_event_weight);
                    if treeIn.mass_lvj >=self.mlvj_signal_min  and treeIn.mass_lvj <self.mlvj_signal_max: hnum_2region.Fill(0,tmp_event_weight);
                if treeIn.jet_mass_pr >= self.mj_sideband_hi_min and treeIn.jet_mass_pr < self.mj_sideband_hi_max:
                    rdataset_sb_hi_mlvj.add( RooArgSet( rrv_mass_lvj ), tmp_event_weight );
                    rdataset4fit_sb_hi_mlvj.add( RooArgSet( rrv_mass_lvj ), tmp_event_weight4fit );

                rrv_mass_j.setVal( treeIn.jet_mass_pr );
                rdataset_mj.add( RooArgSet( rrv_mass_j ), tmp_event_weight );
                rdataset4fit_mj.add( RooArgSet( rrv_mass_j ), tmp_event_weight4fit );
                if treeIn.jet_mass_pr >=self.mj_sideband_lo_min and treeIn.jet_mass_pr <self.mj_sideband_lo_max: hnum_4region.Fill(-1,tmp_event_weight );
                if treeIn.jet_mass_pr >=self.mj_signal_min      and treeIn.jet_mass_pr <self.mj_signal_max     : hnum_4region.Fill(0,tmp_event_weight);
                if treeIn.jet_mass_pr >=self.mj_sideband_hi_min and treeIn.jet_mass_pr <self.mj_sideband_hi_max: hnum_4region.Fill(1,tmp_event_weight);
                hnum_4region.Fill(2,tmp_event_weight);

        rrv_scale_to_lumi=RooRealVar("rrv_scale_to_lumi"+label,"rrv_scale_to_lumi"+label,tmp_scale_to_lumi)
        rrv_scale_to_lumi.Print()
        getattr(self.workspace4fit_,"import")(rrv_scale_to_lumi)
        #prepare m_lvj dataset
        rrv_number_dataset_signal_region_mlvj=RooRealVar("rrv_number_dataset_signal_region"+label+"_mlvj","rrv_number_dataset_signal_region"+label+"_mlvj",hnum_2region.GetBinContent(1));
        rrv_number_dataset_AllRange_mlvj=RooRealVar("rrv_number_dataset_AllRange"+label+"_mlvj","rrv_number_dataset_AllRange"+label+"_mlvj",hnum_2region.GetBinContent(2));
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_signal_region_mlvj)
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_AllRange_mlvj)
               
        getattr(self.workspace4fit_,"import")(rdataset_sb_lo_mlvj);
        getattr(self.workspace4fit_,"import")(rdataset_signal_region_mlvj);
        getattr(self.workspace4fit_,"import")(rdataset_sb_hi_mlvj); 
        getattr(self.workspace4fit_,"import")(rdataset4fit_sb_lo_mlvj);
        getattr(self.workspace4fit_,"import")(rdataset4fit_signal_region_mlvj);
        getattr(self.workspace4fit_,"import")(rdataset4fit_sb_hi_mlvj);
        self.file_out.write("\n%s events number in m_lvj from dataset: %s"%(label,rdataset_signal_region_mlvj.sumEntries()))
        #prepare m_j dataset
        rrv_number_dataset_sb_lo_mj=RooRealVar("rrv_number_dataset_sb_lo"+label+"_mj","rrv_number_dataset_sb_lo"+label+"_mj",hnum_4region.GetBinContent(1));
        rrv_number_dataset_signal_region_mj=RooRealVar("rrv_number_dataset_signal_region"+label+"_mj","rrv_number_dataset_signal_region"+label+"_mj",hnum_4region.GetBinContent(2));
        rrv_number_dataset_sb_hi_mj=RooRealVar("rrv_number_dataset_sb_hi"+label+"_mj","rrv_number_dataset_sb_hi"+label+"_mj",hnum_4region.GetBinContent(3));
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_sb_lo_mj)
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_signal_region_mj)
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_sb_hi_mj)
                
        print "N_rdataset_mj: "
        getattr(self.workspace4fit_,"import")(rdataset_mj)
        getattr(self.workspace4fit_,"import")(rdataset4fit_mj)

        rdataset_sb_lo_mlvj.Print();
        rdataset_signal_region_mlvj.Print();
        rdataset_sb_hi_mlvj.Print();
        rdataset_mj.Print();
        rdataset4fit_sb_lo_mlvj.Print();
        rdataset4fit_signal_region_mlvj.Print();
        rdataset4fit_sb_hi_mlvj.Print();
        rdataset4fit_mj.Print();
        rrv_number_dataset_signal_region_mlvj.Print()
        rrv_number_dataset_AllRange_mlvj.Print()
        rrv_number_dataset_sb_lo_mj.Print()
        rrv_number_dataset_signal_region_mj.Print()
        rrv_number_dataset_sb_hi_mj.Print()
        print rdataset_signal_region_mlvj.sumEntries()
        print rrv_number_dataset_signal_region_mlvj.getVal()
        print rrv_number_dataset_AllRange_mlvj.getVal()
         ########## ---------------------------------------------------
    def get_mj_and_mlvj_dataset_TTbar_contralsample(self,in_file_name, label):# to get the shape of m_lvj
        # read in tree
        fileIn_name=TString(self.file_Directory+in_file_name);
        fileIn = TFile(fileIn_name.Data());
        treeIn = fileIn.Get("otree");
        
        # define bdt reader
        listOfTrainingVariables1 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1"];
        #bdtSimple = tmvaApplicator( listOfTrainingVariables1, "weights/%s/Wtagger_200to275_simple_BDT.weights.xml"%(self.higgs_sample));
        bdtSimple = tmvaApplicator( listOfTrainingVariables1, "weights/General/Wtagger_200to275_simple_BDT.weights.xml");
            
        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j") 
        rrv_mass_lvj = self.workspace4fit_.var("rrv_mass_lvj") 
        rrv_weight = RooRealVar("rrv_weight","rrv_weight",0. ,10000000.) 
        #dataset of m_j
        rdataset_mj = RooDataSet("rdataset"+label+"_mj","rdataset"+label+"_mj",RooArgSet(rrv_mass_j,rrv_weight),RooFit.WeightVar(rrv_weight) );
        rdataset4fit_mj = RooDataSet("rdataset4fit"+label+"_mj","rdataset4fit"+label+"_mj",RooArgSet(rrv_mass_j,rrv_weight),RooFit.WeightVar(rrv_weight) );
        #dataset of m_lvj
        rdataset_sb_lo_mlvj  = RooDataSet("rdataset"+label+"_sb_lo"+"_mlvj","rdataset"+label+"_sb_lo"+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        rdataset_signal_region_mlvj = RooDataSet("rdataset"+label+"_signal_region_mlvj","rdataset"+label+"_signal_region_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        rdataset_sb_hi_mlvj  = RooDataSet("rdataset"+label+"_sb_hi"+"_mlvj","rdataset"+label+"_sb_hi"+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        rdataset4fit_sb_lo_mlvj  = RooDataSet("rdataset4fit"+label+"_sb_lo"+"_mlvj","rdataset4fit"+label+"_sb_lo"+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        rdataset4fit_signal_region_mlvj = RooDataSet("rdataset4fit"+label+"_signal_region_mlvj","rdataset4fit"+label+"_signal_region_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        rdataset4fit_sb_hi_mlvj  = RooDataSet("rdataset4fit"+label+"_sb_hi"+"_mlvj","rdataset4fit"+label+"_sb_hi"+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 

        # make cuts (including mass drop) # create a RooDataSet
        print "N entries: ", treeIn.GetEntries()
        #raw_input("Enter")
        hnum_4region=TH1D("hnum_4region"+label,"hnum_4region"+label,4,-1.5,2.5);# m_j   -1: sb_lo; 0:signal_region; 1: sb_hi; 2:total
        hnum_2region=TH1D("hnum_2region"+label,"hnum_2region"+label,2,-0.5,1.5);# m_lvj  0: signal_region; 1: total
        for i in range(treeIn.GetEntries()):
            if i % 10000 == 0: print "i: ",i
            treeIn.GetEntry(i);
            if i==0: tmp_scale_to_lumi=treeIn.wSampleWeight;
    
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
             
            #cuts include mva cut  
            #discriminantCut=True;
            if treeIn.jet_pt_pr > 200. and discriminantCut and treeIn.jet_mass_pr >= rrv_mass_j.getMin() and treeIn.jet_mass_pr<rrv_mass_j.getMax() and treeIn.nbjets >=1 and treeIn.mass_lvj >= rrv_mass_lvj.getMin() and treeIn.mass_lvj<rrv_mass_lvj.getMax() :
                tmp_event_weight= treeIn.totalEventWeight;
                tmp_event_weight4fit= treeIn.eff_and_pu_Weight;
                tmp_interference_weight_H600=treeIn.interference_Weight_H600;
                tmp_interference_weight_H700=treeIn.interference_Weight_H700;
                tmp_interference_weight_H800=treeIn.interference_Weight_H800;
                tmp_interference_weight_H900=treeIn.interference_Weight_H900;
                tmp_interference_weight_H1000=treeIn.interference_Weight_H1000;
                if label=="_ggH600":
                    #tmp_event_weight=tmp_event_weight/self.higgs_xs_scale*tmp_interference_weight_H600
                    tmp_event_weight=tmp_event_weight*tmp_interference_weight_H600
                    tmp_event_weight4fit=tmp_event_weight4fit*tmp_interference_weight_H600
                if label=="_ggH700":
                    #tmp_event_weight=tmp_event_weight/self.higgs_xs_scale*tmp_interference_weight_H700
                    tmp_event_weight=tmp_event_weight*tmp_interference_weight_H700
                    tmp_event_weight4fit=tmp_event_weight4fit*tmp_interference_weight_H700
                if label=="_ggH800":
                    #tmp_event_weight=tmp_event_weight/self.higgs_xs_scale*tmp_interference_weight_H800
                    tmp_event_weight=tmp_event_weight*tmp_interference_weight_H800
                    tmp_event_weight4fit=tmp_event_weight4fit*tmp_interference_weight_H800
                if label=="_ggH900":
                    #tmp_event_weight=tmp_event_weight/self.higgs_xs_scale*tmp_interference_weight_H900
                    tmp_event_weight=tmp_event_weight*tmp_interference_weight_H900
                    tmp_event_weight4fit=tmp_event_weight4fit*tmp_interference_weight_H900
                if label=="_ggH1000":
                    #tmp_event_weight=tmp_event_weight/self.higgs_xs_scale*tmp_interference_weight_H1000
                    tmp_event_weight=tmp_event_weight*tmp_interference_weight_H1000
                    tmp_event_weight4fit=tmp_event_weight4fit*tmp_interference_weight_H1000
                # for multi-sample, like STop and VV. There are two sample, and two wSampleWeight_value.Use the least wSampleWeight as scale. 
                tmp_event_weight4fit=tmp_event_weight4fit*treeIn.wSampleWeight/tmp_scale_to_lumi
                rrv_mass_lvj.setVal(treeIn.mass_lvj);
                if treeIn.jet_mass_pr >= self.mj_sideband_lo_min and treeIn.jet_mass_pr < self.mj_sideband_lo_max:
                    rdataset_sb_lo_mlvj.add( RooArgSet( rrv_mass_lvj ), tmp_event_weight );
                    rdataset4fit_sb_lo_mlvj.add( RooArgSet( rrv_mass_lvj ), tmp_event_weight4fit );
                if treeIn.jet_mass_pr >= self.mj_signal_min      and treeIn.jet_mass_pr < self.mj_signal_max:
                    rdataset_signal_region_mlvj.add( RooArgSet( rrv_mass_lvj ), tmp_event_weight );
                    rdataset4fit_signal_region_mlvj.add( RooArgSet( rrv_mass_lvj ), tmp_event_weight4fit );
                    hnum_2region.Fill(1,tmp_event_weight);
                    if treeIn.mass_lvj >=self.mlvj_signal_min  and treeIn.mass_lvj <self.mlvj_signal_max: hnum_2region.Fill(0,tmp_event_weight);
                if treeIn.jet_mass_pr >= self.mj_sideband_hi_min and treeIn.jet_mass_pr < self.mj_sideband_hi_max:
                    rdataset_sb_hi_mlvj.add( RooArgSet( rrv_mass_lvj ), tmp_event_weight );
                    rdataset4fit_sb_hi_mlvj.add( RooArgSet( rrv_mass_lvj ), tmp_event_weight4fit );

                rrv_mass_j.setVal( treeIn.jet_mass_pr );
                rdataset_mj.add( RooArgSet( rrv_mass_j ), tmp_event_weight );
                rdataset4fit_mj.add( RooArgSet( rrv_mass_j ), tmp_event_weight4fit );
                if treeIn.jet_mass_pr >=self.mj_sideband_lo_min and treeIn.jet_mass_pr <self.mj_sideband_lo_max: hnum_4region.Fill(-1,tmp_event_weight );
                if treeIn.jet_mass_pr >=self.mj_signal_min      and treeIn.jet_mass_pr <self.mj_signal_max     : hnum_4region.Fill(0,tmp_event_weight);
                if treeIn.jet_mass_pr >=self.mj_sideband_hi_min and treeIn.jet_mass_pr <self.mj_sideband_hi_max: hnum_4region.Fill(1,tmp_event_weight);
                hnum_4region.Fill(2,tmp_event_weight);

        rrv_scale_to_lumi=RooRealVar("rrv_scale_to_lumi"+label,"rrv_scale_to_lumi"+label,tmp_scale_to_lumi)
        rrv_scale_to_lumi.Print()
        getattr(self.workspace4fit_,"import")(rrv_scale_to_lumi)
        #prepare m_lvj dataset
        rrv_number_dataset_signal_region_mlvj=RooRealVar("rrv_number_dataset_signal_region"+label+"_mlvj","rrv_number_dataset_signal_region"+label+"_mlvj",hnum_2region.GetBinContent(1));
        rrv_number_dataset_AllRange_mlvj=RooRealVar("rrv_number_dataset_AllRange"+label+"_mlvj","rrv_number_dataset_AllRange"+label+"_mlvj",hnum_2region.GetBinContent(2));
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_signal_region_mlvj)
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_AllRange_mlvj)
               
        getattr(self.workspace4fit_,"import")(rdataset_sb_lo_mlvj);
        getattr(self.workspace4fit_,"import")(rdataset_signal_region_mlvj);
        getattr(self.workspace4fit_,"import")(rdataset_sb_hi_mlvj); 
        getattr(self.workspace4fit_,"import")(rdataset4fit_sb_lo_mlvj);
        getattr(self.workspace4fit_,"import")(rdataset4fit_signal_region_mlvj);
        getattr(self.workspace4fit_,"import")(rdataset4fit_sb_hi_mlvj);
        self.file_out.write("\n%s events number in m_lvj from dataset: %s"%(label,rdataset_signal_region_mlvj.sumEntries()))
        #prepare m_j dataset
        rrv_number_dataset_sb_lo_mj=RooRealVar("rrv_number_dataset_sb_lo"+label+"_mj","rrv_number_dataset_sb_lo"+label+"_mj",hnum_4region.GetBinContent(1));
        rrv_number_dataset_signal_region_mj=RooRealVar("rrv_number_dataset_signal_region"+label+"_mj","rrv_number_dataset_signal_region"+label+"_mj",hnum_4region.GetBinContent(2));
        rrv_number_dataset_sb_hi_mj=RooRealVar("rrv_number_dataset_sb_hi"+label+"_mj","rrv_number_dataset_sb_hi"+label+"_mj",hnum_4region.GetBinContent(3));
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_sb_lo_mj)
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_signal_region_mj)
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_sb_hi_mj)
                
        print "N_rdataset_mj: "
        getattr(self.workspace4fit_,"import")(rdataset_mj)
        getattr(self.workspace4fit_,"import")(rdataset4fit_mj)

        rdataset_sb_lo_mlvj.Print();
        rdataset_signal_region_mlvj.Print();
        rdataset_sb_hi_mlvj.Print();
        rdataset_mj.Print();
        rdataset4fit_sb_lo_mlvj.Print();
        rdataset4fit_signal_region_mlvj.Print();
        rdataset4fit_sb_hi_mlvj.Print();
        rdataset4fit_mj.Print();
        rrv_number_dataset_signal_region_mlvj.Print()
        rrv_number_dataset_AllRange_mlvj.Print()
        rrv_number_dataset_sb_lo_mj.Print()
        rrv_number_dataset_signal_region_mj.Print()
        rrv_number_dataset_sb_hi_mj.Print()
        print rdataset_signal_region_mlvj.sumEntries()
        print rrv_number_dataset_signal_region_mlvj.getVal()
        print rrv_number_dataset_AllRange_mlvj.getVal()
        #raw_input("ENTER");
    ########## ---------------------------------------------------
#    def get_mj_and_mlvj_dataset_TTbar_contralsample(self,in_file_name, label):# to get the shape of m_lvj
#        # read in tree
#        fileIn_name=TString(self.file_Directory+in_file_name);
#        fileIn = TFile(fileIn_name.Data());
#        treeIn = fileIn.Get("otree");
#        
#        # define bdt reader
#        listOfTrainingVariables1 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1"];
#        #bdtSimple = tmvaApplicator( listOfTrainingVariables1, "weights/%s/Wtagger_200to275_simple_BDT.weights.xml"%(self.higgs_sample));
#        bdtSimple = tmvaApplicator( listOfTrainingVariables1, "weights/General/Wtagger_200to275_simple_BDT.weights.xml");
#            
#        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j") 
#        rrv_mass_lvj = self.workspace4fit_.var("rrv_mass_lvj") 
#        rrv_weight = RooRealVar("rrv_weight","rrv_weight",0. ,1000000.) 
#        #dataset of m_j
#        rdataset_mj = RooDataSet("rdataset"+label+"_mj","rdataset"+label+"_mj",RooArgSet(rrv_mass_j,rrv_weight),RooFit.WeightVar(rrv_weight) );
#        #dataset of m_lvj
#        rdataset_sb_lo  = RooDataSet("rdataset"+label+"_sb_lo"+"_mlvj","rdataset"+label+"_sb_lo"+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
#        rdataset_signal_region = RooDataSet("rdataset"+label+"_signal_region"+"_mlvj","rdataset"+label+"_signal_region"+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
#        rdataset_sb_hi  = RooDataSet("rdataset"+label+"_sb_hi"+"_mlvj","rdataset"+label+"_sb_hi"+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
#
#        # make cuts (including mass drop) # create a RooDataSet
#        print "N entries: ", treeIn.GetEntries()
#        #raw_input("Enter")
#        hnum_4region=TH1D("hnum_4region"+label,"hnum_4region"+label,4,-1.5,2.5);# m_j   -1: sb_lo; 0:signal_region; 1: sb_hi; 2:total
#        hnum_2region=TH1D("hnum_2region"+label,"hnum_2region"+label,2,-0.5,1.5);# m_lvj  0: signal_region; 1: total
#        for i in range(treeIn.GetEntries()):
#            if i % 10000 == 0: print "i: ",i
#            treeIn.GetEntry(i);
#    
#            discriminantCut = False; 
#            if self.cutOnMassDrop_ and treeIn.jet_massdrop_pr < 0.25: discriminantCut = True;
#            elif not self.cutOnMassDrop_:
#                listOfVarVals = [];
#                for kk in range(len(listOfTrainingVariables1)):
#                    listOfVarVals.append( getattr( treeIn, listOfTrainingVariables1[kk] ) );
#                BDTval = bdtSimple.eval( listOfVarVals );
#                #print BDTval;
#                if BDTval > 0.0: discriminantCut = True;
#            else: discriminantCut = False;
#    
#            if treeIn.jet_pt_pr > 200. and discriminantCut and treeIn.jet_mass_pr >= rrv_mass_j.getMin() and treeIn.jet_mass_pr<rrv_mass_j.getMax() and treeIn.mass_lvj >= rrv_mass_lvj.getMin() and treeIn.mass_lvj<rrv_mass_lvj.getMax() and treeIn.nbjets >= 1 :
#
#                tmp_event_weight= treeIn.totalEventWeight;
#                tmp_interference_weight_H600=treeIn.interference_Weight_H600;
#                tmp_interference_weight_H700=treeIn.interference_Weight_H700;
#                tmp_interference_weight_H800=treeIn.interference_Weight_H800;
#                tmp_interference_weight_H900=treeIn.interference_Weight_H900;
#                tmp_interference_weight_H1000=treeIn.interference_Weight_H1000;
#                #if label=="_ggH600": tmp_event_weight=tmp_event_weight/self.higgs_xs_scale*tmp_interference_weight_H600
#                #if label=="_ggH700": tmp_event_weight=tmp_event_weight/self.higgs_xs_scale*tmp_interference_weight_H700
#                #if label=="_ggH800": tmp_event_weight=tmp_event_weight/self.higgs_xs_scale*tmp_interference_weight_H800
#                #if label=="_ggH900": tmp_event_weight=tmp_event_weight/self.higgs_xs_scale*tmp_interference_weight_H900
#                #if label=="_ggH1000":tmp_event_weight=tmp_event_weight/self.higgs_xs_scale*tmp_interference_weight_H1000
#                if label=="_ggH600": tmp_event_weight=tmp_event_weight*tmp_interference_weight_H600
#                if label=="_ggH700": tmp_event_weight=tmp_event_weight*tmp_interference_weight_H700
#                if label=="_ggH800": tmp_event_weight=tmp_event_weight*tmp_interference_weight_H800
#                if label=="_ggH900": tmp_event_weight=tmp_event_weight*tmp_interference_weight_H900
#                if label=="_ggH1000":tmp_event_weight=tmp_event_weight*tmp_interference_weight_H1000
#
#                rrv_mass_lvj.setVal( treeIn.mass_lvj );
#                if treeIn.jet_mass_pr >= self.mj_sideband_lo_min and treeIn.jet_mass_pr < self.mj_sideband_lo_max:
#                    rdataset_sb_lo.add( RooArgSet( rrv_mass_lvj ), tmp_event_weight );
#                if treeIn.jet_mass_pr >= self.mj_signal_min      and treeIn.jet_mass_pr < self.mj_signal_max:
#                    rdataset_signal_region.add( RooArgSet( rrv_mass_lvj ), tmp_event_weight );
#                if treeIn.jet_mass_pr >= self.mj_sideband_hi_min and treeIn.jet_mass_pr < self.mj_sideband_hi_max:
#                    rdataset_sb_hi.add( RooArgSet( rrv_mass_lvj ), tmp_event_weight );
#                if treeIn.jet_mass_pr >= self.mj_signal_min      and treeIn.jet_mass_pr < self.mj_signal_max and treeIn.mass_lvj >=self.mlvj_signal_min  and treeIn.mass_lvj <self.mlvj_signal_max     : hnum_2region.Fill(0,tmp_event_weight);
#                if treeIn.jet_mass_pr >= self.mj_signal_min      and treeIn.jet_mass_pr < self.mj_signal_max : hnum_2region.Fill(1,tmp_event_weight);
#
#                rrv_mass_j.setVal( treeIn.jet_mass_pr );
#                rdataset_mj.add( RooArgSet( rrv_mass_j ), tmp_event_weight );
#                if treeIn.jet_mass_pr >=self.mj_sideband_lo_min and treeIn.jet_mass_pr <self.mj_sideband_lo_max: hnum_4region.Fill(-1,tmp_event_weight );
#                if treeIn.jet_mass_pr >=self.mj_signal_min      and treeIn.jet_mass_pr <self.mj_signal_max     : hnum_4region.Fill(0,tmp_event_weight);
#                if treeIn.jet_mass_pr >=self.mj_sideband_hi_min and treeIn.jet_mass_pr <self.mj_sideband_hi_max: hnum_4region.Fill(1,tmp_event_weight);
#                hnum_4region.Fill(2,tmp_event_weight);
#
#        #prepare m_lvj dataset
#        rrv_number_dataset_signal_region=RooRealVar("rrv_number_dataset_signal_region"+label+"_mlvj","rrv_number_dataset_signal_region"+label+"_mlvj",hnum_2region.GetBinContent(1));
#        rrv_number_dataset_AllRange=RooRealVar("rrv_number_dataset_AllRange"+label+"_mlvj","rrv_number_dataset_AllRange"+label+"_mlvj",hnum_2region.GetBinContent(2));
#        rrv_number_dataset_signal_region.Print()
#        rrv_number_dataset_AllRange.Print()
#        getattr(self.workspace4fit_,"import")(rrv_number_dataset_signal_region)
#        getattr(self.workspace4fit_,"import")(rrv_number_dataset_AllRange)
#                
#        rdataset_sb_lo.Print();
#        rdataset_signal_region.Print();
#        rdataset_sb_hi.Print();
#        getattr(self.workspace4fit_,"import")(rdataset_sb_lo);
#        getattr(self.workspace4fit_,"import")(rdataset_signal_region);
#        getattr(self.workspace4fit_,"import")(rdataset_sb_hi);
#        rdataset_signal_region.Print()
#        self.file_out.write("\n%s events number in m_lvj from dataset: %s"%(label,rdataset_signal_region.sumEntries()))
#        #prepare m_j dataset
#        rrv_number_dataset_sb_lo=RooRealVar("rrv_number_dataset_sb_lo"+label+"_mj","rrv_number_dataset_sb_lo"+label+"_mj",hnum_4region.GetBinContent(1));
#        rrv_number_dataset_signal_region=RooRealVar("rrv_number_dataset_signal_region"+label+"_mj","rrv_number_dataset_signal_region"+label+"_mj",hnum_4region.GetBinContent(2));
#        rrv_number_dataset_sb_hi=RooRealVar("rrv_number_dataset_sb_hi"+label+"_mj","rrv_number_dataset_sb_hi"+label+"_mj",hnum_4region.GetBinContent(3));
#        getattr(self.workspace4fit_,"import")(rrv_number_dataset_sb_lo)
#        getattr(self.workspace4fit_,"import")(rrv_number_dataset_signal_region)
#        getattr(self.workspace4fit_,"import")(rrv_number_dataset_sb_hi)
#                
#        print "N_rdataset_mj: "
#        rdataset_mj.Print();
#        getattr(self.workspace4fit_,"import")(rdataset_mj)
#        #raw_input( 'Press ENTER to continue\n ' )
#    ######## ++++++++++++++## ---------------------------------------------------
    def fit_mlvj_shape_single_MC_sample(self,in_file_name, label, in_range, in_model_name):# to get the shape of m_lvj
    
        rrv_mass_lvj = self.workspace4fit_.var("rrv_mass_lvj") 
        #dataset
        rdataset = self.workspace4fit_.data("rdataset4fit"+label+"_"+in_range+"_mlvj"); 
        rdataset.Print();
        #model function
        model = self.make_Pdf(label+in_range,in_model_name,"_mlvj");
    
        rfresult = model.fitTo( rdataset, RooFit.Save(1), RooFit.SumW2Error(kTRUE));
        rfresult = model.fitTo( rdataset, RooFit.Save(1), RooFit.SumW2Error(kTRUE));
        
        mplot = rrv_mass_lvj.frame(RooFit.Title("M_{lvj_"+in_range+"} fitted by "+in_model_name));
        rdataset.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) , RooFit.VLines());
        model.plotOn( mplot, RooFit.VisualizeError(rfresult,1),RooFit.FillColor(kOrange) , RooFit.VLines());
        #model.plotOn(mplot,RooFit.VisualizeError(rfresult,1,kFALSE),RooFit.DrawOption("F"),RooFit.FillColor(kOrange), RooFit.VLines());
        rdataset.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) , RooFit.VLines());
        model.plotOn( mplot , RooFit.VLines());
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
        rdataset = self.workspace4fit_.data("rdataset4fit"+label+in_range+"_mlvj"); 
        rdataset.Print();
        #model function
        model = self.make_Model(label+in_range,in_model_name,"_mlvj");
        model.Print()
        #raw_input( 'Press ENTER to continue\n ' )
        model.fitTo( rdataset, RooFit.Save(1), RooFit.SumW2Error(kTRUE) ,RooFit.Extended(kTRUE) );
        rfresult = model.fitTo( rdataset, RooFit.Save(1), RooFit.SumW2Error(kTRUE) ,RooFit.Extended(kTRUE) );
        rfresult.SetName("rfresult"+label+in_range+"_mlvj")
        getattr(self.workspace4fit_,"import")(rfresult)
        
        mplot = rrv_mass_lvj.frame(RooFit.Title("M_{lvj_"+in_range+"} fitted by "+in_model_name));
        rdataset.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) , RooFit.VLines());
        model.plotOn( mplot, RooFit.VisualizeError(rfresult,1),RooFit.FillColor(kOrange) , RooFit.VLines());
        #model.plotOn(mplot,RooFit.VisualizeError(rfresult,1,kFALSE),RooFit.DrawOption("F"),RooFit.FillColor(kOrange), RooFit.VLines());
        rdataset.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) , RooFit.VLines());
        model.plotOn( mplot , RooFit.VLines());
        #pull
        hpull=mplot.pullHist();
        mplot_pull = rrv_mass_lvj.frame(RooFit.Title("Pull Distribution"));
        mplot_pull.addPlotable(hpull,"P");
        mplot_pull.SetTitle("PULL");
        mplot_pull.GetYaxis().SetRangeUser(-5,5);
         
        parameters_list=model.getParameters(rdataset);
        self.draw_canvas( mplot, mplot_pull,parameters_list,"plots/m_lvj_BDTcut/", in_file_name,"m_lvj"+in_range+in_model_name)
        rfresult.Print();

        #normalize the number of total events to lumi
        self.workspace4fit_.var("rrv_number"+label+in_range+"_mlvj").Print()
        self.workspace4fit_.var("rrv_scale_to_lumi"+label).Print()
        self.workspace4fit_.var("rrv_number"+label+in_range+"_mlvj").setVal( self.workspace4fit_.var("rrv_number"+label+in_range+"_mlvj").getVal()*self.workspace4fit_.var("rrv_scale_to_lumi"+label).getVal()  )
        self.workspace4fit_.var("rrv_number"+label+in_range+"_mlvj").setError(self.workspace4fit_.var("rrv_number"+label+in_range+"_mlvj").getError()*self.workspace4fit_.var("rrv_scale_to_lumi"+label).getVal()  )
        if TString(label).Contains("ggH"):
            self.workspace4fit_.var("rrv_number"+label+in_range+"_mlvj").setVal( self.workspace4fit_.var("rrv_number"+label+in_range+"_mlvj").getVal()/self.higgs_xs_scale  )
            self.workspace4fit_.var("rrv_number"+label+in_range+"_mlvj").setError(self.workspace4fit_.var("rrv_number"+label+in_range+"_mlvj").getError()/self.higgs_xs_scale  )

        self.workspace4fit_.var("rrv_number"+label+in_range+"_mlvj").Print()
        #raw_input("ENTER")

        return model;
    ######## ++++++++++++++
    
    def fit_alpha_WJets(self):# get the shape of WJets in sb_lo, sb_hi, and signal_region. fit to get alpha
        self.get_mj_and_mlvj_dataset(self.file_WJets_mc,"_WJets")# to get the shape of m_lvj
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
        rdataset.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) , RooFit.VLines());
        model_WJets_signal.plotOn( mplot, RooFit.VisualizeError(rfresult,1),RooFit.FillColor(kOrange) , RooFit.VLines());
        #model_WJets_signal.plotOn(mplot,RooFit.VisualizeError(rfresult,1,kFALSE),RooFit.DrawOption("F"),RooFit.FillColor(kOrange), RooFit.VLines());
        rdataset.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) , RooFit.VLines());
        model_WJets_signal.plotOn( mplot , RooFit.VLines());
        #model_WJets_signal.plotOn( mplot, RooFit.Components("model_WJets_sb_lo"), RooFit.LineStyle(kDashed),RooFit.LineColor(kBlack) , RooFit.VLines());
        #model_WJets_signal.plotOn( mplot, RooFit.Components("model_WJets_sb_hi"), RooFit.LineStyle(kDashed),RooFit.LineColor(kRed) , RooFit.VLines());
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

        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j") 
        rrv_mass_lvj = self.workspace4fit_.var("rrv_mass_lvj") 

        rdataset_data_mj=self.workspace4fit_.data("rdataset_data_mj")

        model_TTbar=self.get_TTbar_mj_Model();
        model_STop=self.get_STop_mj_Model();
        model_VV=self.get_VV_mj_Model();
        model_WJets=self.get_WJets_mj_Model();
        model_data=RooAddPdf("model_data_mj","model_data_mj",RooArgList(model_WJets,model_VV,model_TTbar,model_STop));
        getattr(self.workspace4fit_,"import")(model_data)
        # fit the sideband range
        rfresult = model_data.fitTo( rdataset_data_mj, RooFit.Save(1) , RooFit.Range("sb_lo,sb_hi") ,RooFit.Extended(kTRUE) );

        print "N_rdataset: ", rdataset_data_mj.Print();
        #rrv_number_data_mj=RooRealVar("rrv_number_data_mj","rrv_number_data_mj",rdataset_data_mj.sumEntries());
        rrv_number_data_mj=RooRealVar("rrv_number_data_mj","rrv_number_data_mj", self.workspace4fit_.var("rrv_number_TTbar_mj").getVal()+self.workspace4fit_.var("rrv_number_STop_mj").getVal()+self.workspace4fit_.var("rrv_number_VV_mj").getVal()+self.workspace4fit_.var("rrv_number_WJets_mj").getVal() );
        getattr(self.workspace4fit_,"import")(rrv_number_data_mj)
        
        mplot = rrv_mass_j.frame(RooFit.Title("Closure test: WJets+TTbar+STop+VV"));
        rdataset_data_mj.plotOn(mplot);
        #model_data.plotOn(mplot,RooFit.VisualizeError(rfresult,1,kFALSE),RooFit.DrawOption("F"),RooFit.FillColor(kOrange),RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()), RooFit.VLines());
        model_data.plotOn(mplot , RooFit.VLines());
        model_data.plotOn(mplot, RooFit.Components("model_VV_mj"),RooFit.LineColor(self.color_palet["VV"]),RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()), RooFit.VLines() );
        model_data.plotOn(mplot, RooFit.Components("model_STop_mj,model_VV_mj"), RooFit.LineColor(self.color_palet["STop"]),RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()) , RooFit.VLines());
        model_data.plotOn(mplot, RooFit.Components("model_TTbar_mj,model_STop_mj,model_VV_mj"), RooFit.LineColor(self.color_palet["TTbar"]),RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()) , RooFit.VLines());
        model_data.plotOn(mplot, RooFit.Components("model_WJets_mj,model_TTbar_mj,model_STop_mj,model_VV_mj"), RooFit.LineColor(self.color_palet["WJets"]),RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()), RooFit.VLines() );
        model_data.plotOn(mplot, RooFit.Components("model_WJets_mj,model_TTbar_mj,model_STop_mj,model_VV_mj"), RooFit.Name("WJets"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["WJets"]), RooFit.LineColor(self.color_palet["WJets"]), RooFit.VLines(),RooFit.Precision(1e-8)) ;
        model_data.plotOn(mplot, RooFit.Components("model_TTbar_mj,model_STop_mj,model_VV_mj"), RooFit.Name("TTbar"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["TTbar"]), RooFit.LineColor(self.color_palet["TTbar"]), RooFit.VLines(),RooFit.Precision(1e-8));
        model_data.plotOn(mplot, RooFit.Components("model_STop_mj,model_VV_mj"), RooFit.Name("STop"), RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["STop"]), RooFit.LineColor(self.color_palet["STop"]), RooFit.VLines(),RooFit.Precision(1e-8));
        model_data.plotOn(mplot, RooFit.Components("model_VV_mj"),RooFit.Name("VV"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["VV"]), RooFit.LineColor(self.color_palet["VV"]), RooFit.VLines(),RooFit.Precision(1e-8)) ;
        model_data.plotOn(mplot,RooFit.VisualizeError(rfresult,1),RooFit.FillColor(self.color_palet["Error"]),RooFit.FillStyle(3013),RooFit.LineColor(self.color_palet["Error"]),RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()), RooFit.VLines());
        rdataset_data_mj.plotOn(mplot);
        model_data.plotOn( mplot , RooFit.VLines());
        model_data.plotOn( mplot, RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()),RooFit.LineStyle(kDashed) , RooFit.VLines());

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
        
        parameters_list=model_data.getParameters(rdataset_data_mj);
        if inject_signal: self.draw_canvas( mplot, mplot_pull,parameters_list,"plots/m_j_BDTcut/", "m_j_sideband_inject_signal","",1)
        else: self.draw_canvas( mplot, mplot_pull,parameters_list,"plots/m_j_BDTcut/", "m_j_sideband_not_inject_signal","",1)

        rfresult.Print();

        self.get_mj_normalization("_data");
        self.get_mj_normalization("_TTbar");
        self.get_mj_normalization("_STop");
        self.get_mj_normalization("_VV");
        self.get_mj_normalization("_WJets");

        # to calculate the WJets's normalization in M_J signal_region
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
        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j") 
        rrv_mass_lvj = self.workspace4fit_.var("rrv_mass_lvj") 
        rdataset_data_signal_region_mlvj=self.workspace4fit_.data("rdataset_data_signal_region_mlvj")
        print "N_rdataset: ", rdataset_data_signal_region_mlvj.Print();
        self.file_out.write("\ndata_obs event number: %s\n"%(rdataset_data_signal_region_mlvj.sumEntries()) )

        model_ggH   = self.get_ggH_mlvj_Model("_signal_region");
        model_TTbar   = self.get_TTbar_mlvj_Model("_signal_region");
        model_STop   = self.get_STop_mlvj_Model("_signal_region");
        model_VV    = self.get_VV_mlvj_Model("_signal_region");
        model_WJets = self.get_WJets_mlvj_Model("_signal_region");
        model_TTbar.Print();
        model_STop.Print();
        model_VV.Print();
        model_WJets.Print();
       
        model_data=RooAddPdf("model_data_signal_region_mlvj","model_data_signal_region_mlvj",RooArgList(model_WJets,model_VV,model_TTbar,model_STop));
        getattr(self.workspace4fit_,"import")(model_data)

        rfresult = model_data.fitTo( rdataset_data_signal_region_mlvj, RooFit.Save(1) ,RooFit.Extended(kTRUE) );
        self.fix_Model("_WJets")
        
        mplot = rrv_mass_lvj.frame(RooFit.Title("Closure test: WJets+TTbar+STop+VV"));
        rdataset_data_signal_region_mlvj.plotOn( mplot );
        model_data.plotOn(mplot,RooFit.VisualizeError(rfresult,1),RooFit.FillColor(kOrange), RooFit.VLines());
        rdataset_data_signal_region_mlvj.plotOn( mplot );
        #model_ggH.plotOn( mplot, RooFit.LineColor(kBlack) , RooFit.VLines());
        model_data.plotOn(mplot , RooFit.VLines());
        model_data.plotOn(mplot, RooFit.Components(model_VV.GetName()),RooFit.LineColor(kAzure+8), RooFit.VLines());
        model_data.plotOn(mplot, RooFit.Components(model_TTbar.GetName()), RooFit.LineColor(kGreen), RooFit.VLines());
        model_data.plotOn(mplot, RooFit.Components(model_STop.GetName()), RooFit.LineColor(kGreen),RooFit.LineStyle(2), RooFit.VLines());
        model_data.plotOn(mplot, RooFit.Components(model_WJets.GetName()), RooFit.LineColor(kRed), RooFit.VLines());
        model_data.plotOn( mplot , RooFit.VLines());
        #model_data.plotOn( mplot, RooFit.Range(rrv_mass_lvj.getMin(),rrv_mass_lvj.getMax()),RooFit.LineStyle(kDashed) , RooFit.VLines());
    
        #pull
        hpull=mplot.pullHist();
        mplot_pull = rrv_mass_lvj.frame(RooFit.Title("Pull Distribution"));
        mplot_pull.addPlotable(hpull,"P");
        mplot_pull.SetTitle("PULL");
        mplot_pull.GetYaxis().SetRangeUser(-5,5);
    
        parameters_list=model_data.getParameters(rdataset_data_signal_region_mlvj);
        if inject_signal: self.draw_canvas( mplot, mplot_pull,parameters_list,"plots/m_lvj_BDTcut/", "m_lvj_total_inject_signal","",1)
        else: self.draw_canvas( mplot, mplot_pull,parameters_list,"plots/m_lvj_BDTcut/", "m_lvj_total_not_inject_signal","",1)

        self.get_mlvj_normalization("_%s"%(self.higgs_sample));
        self.get_mlvj_normalization("_TTbar");
        self.get_mlvj_normalization("_STop");
        self.get_mlvj_normalization("_VV");
        self.get_mlvj_normalization("_WJets");

        rfresult.Print();


    ######## ++++++++++++++
    def fit_mlvj_in_Mj_sideband(self, mj_region="_sb_lo",inject_signal=0): 
    
        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j") 
        rrv_mass_lvj = self.workspace4fit_.var("rrv_mass_lvj") 
        rdataset_data_mlvj=self.workspace4fit_.data("rdataset_data%s_mlvj"%(mj_region))
        print "N_rdataset: ", rdataset_data_mlvj.Print();

        model_ggH   = self.get_ggH_mlvj_Model("_sb_lo");
        number_ggH_sb_lo_mlvj=self.workspace4fit_.var("rrv_number_ggH_sb_lo_mlvj")
        model_VV_backgrounds    = self.get_VV_mlvj_Model("_sb_lo"); number_VV_sb_lo_mlvj=self.workspace4fit_.var("rrv_number_VV_sb_lo_mlvj")
        model_TTbar_backgrounds    = self.get_TTbar_mlvj_Model("_sb_lo"); number_TTbar_sb_lo_mlvj=self.workspace4fit_.var("rrv_number_TTbar_sb_lo_mlvj")
        model_STop_backgrounds    = self.get_STop_mlvj_Model("_sb_lo"); number_STop_sb_lo_mlvj=self.workspace4fit_.var("rrv_number_STop_sb_lo_mlvj")

        model_pdf_WJets = self.make_Pdf("_WJets_sb_lo_from_fitting","ErfExp_v1","_mlvj");
        number_WJets_sb_lo=self.workspace4fit_.var("rrv_number_WJets_sb_lo_mlvj").clone("rrv_number_WJets_sb_lo_mlvj_from_fitting");
        model_pdf_WJets.Print()
        number_WJets_sb_lo.Print()
        model_WJets=RooExtendPdf("model_WJets_sb_lo_mlvj_from_fitting","model_WJets_sb_lo_mlvj_from_fitting",model_pdf_WJets,number_WJets_sb_lo)

        model_data=RooAddPdf("model_data%s_mlvj"%(mj_region),"model_data%s_mlvj"%(mj_region),RooArgList(model_WJets,model_VV_backgrounds, model_TTbar_backgrounds, model_STop_backgrounds));
        getattr(self.workspace4fit_,"import")(model_data)

        rfresult = model_data.fitTo( rdataset_data_mlvj, RooFit.Save(1) ,RooFit.Extended(kTRUE) );
        getattr(self.workspace4fit_,"import")(model_pdf_WJets);
        getattr(self.workspace4fit_,"import")(number_WJets_sb_lo);
        
        mplot = rrv_mass_lvj.frame(RooFit.Title("M_lvj fitted in M_j sideband "));
        rdataset_data_mlvj.plotOn( mplot ,RooFit.Name("data_invisible") );
        model_data.plotOn(mplot, RooFit.Components("model_WJets_sb_lo_mlvj_from_fitting,model_TTbar_sb_lo_mlvj,model_STop_sb_lo_mlvj,model_VV_sb_lo_mlvj"), RooFit.Name("WJets"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["WJets"]), RooFit.LineColor(self.color_palet["WJets"]), RooFit.VLines(),RooFit.Precision(1e-8)) ;
        model_data.plotOn(mplot, RooFit.Components("model_TTbar_sb_lo_mlvj,model_STop_sb_lo_mlvj,model_VV_sb_lo_mlvj"), RooFit.Name("TTbar"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["TTbar"]), RooFit.LineColor(self.color_palet["TTbar"]), RooFit.VLines(),RooFit.Precision(1e-8));
        model_data.plotOn(mplot, RooFit.Components("model_STop_sb_lo_mlvj,model_VV_sb_lo_mlvj"), RooFit.Name("STop"), RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["STop"]), RooFit.LineColor(self.color_palet["STop"]), RooFit.VLines(),RooFit.Precision(1e-8));
        model_data.plotOn(mplot, RooFit.Components("model_VV_sb_lo_mlvj"),RooFit.Name("VV"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["VV"]), RooFit.LineColor(self.color_palet["VV"]), RooFit.VLines(),RooFit.Precision(1e-8)) ;
        rdataset_data_mlvj.plotOn(mplot,RooFit.Name("data"));
        model_data.plotOn(mplot,RooFit.VisualizeError(rfresult,1), RooFit.Name("Uncertainty"),RooFit.FillColor(self.color_palet["Error"]),RooFit.FillStyle(3013),RooFit.LineColor(self.color_palet["Error"]), RooFit.VLines());
        model_data.plotOn( mplot , RooFit.VLines(), RooFit.Invisible());

        leg=self.legend4Plot(mplot,0)
        mplot.addObject(leg)
    
        #pull
        hpull=mplot.pullHist();
        mplot_pull = rrv_mass_lvj.frame(RooFit.Title("Pull Distribution"));
        mplot_pull.addPlotable(hpull,"P");
        mplot_pull.SetTitle("PULL");
        mplot_pull.GetYaxis().SetRangeUser(-5,5);
    
        parameters_list=model_data.getParameters(rdataset_data_mlvj);
        if inject_signal: self.draw_canvas( mplot, mplot_pull,parameters_list,"plots/m_lvj_BDTcut/", "m_lvj_sb_lo_inject_signal","",1)
        else: self.draw_canvas( mplot, mplot_pull,parameters_list,"plots/m_lvj_BDTcut/", "m_lvj_sb_lo_not_inject_signal","",1)

        #get the correlation of: P(M_lvj, WJets, signal_region)/P(M_lvj, WJets, sideband) 
        self.get_WJets_mlvj_correction_sb_lo_to_signal_region()

        self.fix_Model("_%s"%(self.higgs_sample))
        self.fix_Model("_TTbar")
        self.fix_Model("_STop")
        self.fix_Model("_VV")

        self.get_mlvj_normalization("_%s"%(self.higgs_sample));
        self.get_mlvj_normalization("_TTbar");
        self.get_mlvj_normalization("_STop");
        self.get_mlvj_normalization("_VV");
        self.get_mlvj_normalization("_WJets","model_pdf_WJets_signal_region_after_correct");
        rfresult.Print();

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
        #print label+"sb_loInt=%s"%(sb_loInt_val)
        #print label+"signalInt=%s"%(signalInt_val)
        #print label+"sb_hiInt=%s"%(sb_hiInt_val)

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
        self.file_out.write( "\nTotal  Number in sidebands     from dataset:%s"%(self.workspace4fit_.var("rrv_number_dataset_sb_lo"+label+"_mj").getVal()+ self.workspace4fit_.var("rrv_number_dataset_sb_hi"+label+"_mj").getVal() ) )
        self.file_out.write( "\nRatio signal_region/sidebands  from dataset:%s"%(self.workspace4fit_.var("rrv_number_dataset_signal_region"+label+"_mj").getVal()/(self.workspace4fit_.var("rrv_number_dataset_sb_lo"+label+"_mj").getVal()+ self.workspace4fit_.var("rrv_number_dataset_sb_hi"+label+"_mj").getVal()) ) )

        self.file_out.write( "\nEvents Number in sideband_low  from fitting:%s"%(rrv_tmp.getVal()*sb_loInt_val) )
        self.file_out.write( "\nEvents Number in Signal Region from fitting:%s"%(rrv_tmp.getVal()*signalInt_val) )
        self.file_out.write( "\nEvents Number in sideband_high from fitting:%s"%(rrv_tmp.getVal()*sb_hiInt_val) )
        self.file_out.write( "\nTotal  Number in sidebands     from fitting:%s"%(rrv_tmp.getVal()*(sb_loInt_val+sb_hiInt_val)  ) )
        self.file_out.write( "\nRatio signal_region/sidebands  from fitting:%s"%(signalInt_val/(sb_loInt_val+sb_hiInt_val)  ) )

        if label=="_WJets": #prepare Limit of WJet Norm
            self.number_WJets_insideband=int(round( rrv_tmp.getVal()*(sb_loInt_val+sb_hiInt_val) ))
            #self.datadriven_alpha_WJets_unbin =signalInt_val/(sb_loInt_val+sb_hiInt_val)
            self.datadriven_alpha_WJets_unbin =rrv_tmp.getVal()*signalInt_val/self.number_WJets_insideband


    ######## ++++++++++++++
    def get_mlvj_normalization(self, label, model_name=""):
        print "get mlvj normalization"
        print model_name
        if model_name=="": model = self.workspace4fit_.pdf("model"+label+"_signal_region_mlvj");
        else: model = self.workspace4fit_.pdf(model_name);

        model.Print()
        #raw_input("ENTER")
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
        print rrv_tmp.getVal()
        print signalInt_val
        print rrv_tmp.getVal()*signalInt_val
        getattr(self.workspace4fit_,"import")(rrv_number_fitting_signal_region_mlvj)

        if label=="_WJets": #prepare Limit of WJet Norm
            self.datadriven_alpha_WJets_counting = rrv_tmp.getVal()*signalInt_val/self.number_WJets_insideband 
        #self.workspace4fit_.var("rrv_number"+label+"_mlvj").Print();
        #raw_input("ENTER")
    ######## ++++++++++++++
    def print_limit_datacard_unbin(self, params_list):
        print "print_limit_datacard_unbin"
        datacard_out=open(self.file_datacard_unbin,"w");

        datacard_out.write( "imax 1" )
        datacard_out.write( "\njmax 4" )
        datacard_out.write( "\nkmax *" )
        datacard_out.write( "\n--------------- ")
        datacard_out.write( "\nshapes * * %s %s:$PROCESS "%(self.file_rlt_root, self.workspace4limit_.GetName()))
        datacard_out.write( "\n--------------- ")
        datacard_out.write( "\nbin 1 ")
        datacard_out.write( "\nobservation %s "%(self.workspace4limit_.data("data_obs").sumEntries()) )
        datacard_out.write( "\n------------------------------" )
        datacard_out.write( "\nbin                1         1        1        1      1" )
        datacard_out.write( "\nprocess            %s    WJets    TTbar    STop   VV "%(self.higgs_sample) )
        datacard_out.write( "\nprocess            0         1        2        3      4" )
        #datacard_out.write( "\nrate               %s        %s       %s       %s     %s "%(self.workspace4fit_.var("rrv_number_%s_signal_region_mlvj"%(self.higgs_sample)).getVal()/50., self.workspace4fit_.var("rrv_number_WJets_signal_region_mlvj").getVal(), self.workspace4fit_.var("rrv_number_TTbar_signal_region_mlvj").getVal(), self.workspace4fit_.var("rrv_number_STop_signal_region_mlvj").getVal(), self.workspace4fit_.var("rrv_number_VV_signal_region_mlvj").getVal()  ) )
        #datacard_out.write( "\nrate               %s        %s       %s       %s     %s "%(self.workspace4fit_.var("rrv_number_%s_signal_region_mlvj"%(self.higgs_sample)).getVal(), self.workspace4fit_.var("rrv_number_WJets_signal_region_mlvj").getVal(), self.workspace4fit_.var("rrv_number_TTbar_signal_region_mlvj").getVal(), self.workspace4fit_.var("rrv_number_STop_signal_region_mlvj").getVal(), self.workspace4fit_.var("rrv_number_VV_signal_region_mlvj").getVal()  ) )
        datacard_out.write( "\nrate               %s        %s       %s       %s     %s "%(self.workspace4limit_.var("rate_%s_for_unbin"%(self.higgs_sample)).getVal(), self.workspace4limit_.var("rate_WJets_for_unbin").getVal(), self.workspace4limit_.var("rate_TTbar_for_unbin").getVal(), self.workspace4limit_.var("rate_STop_for_unbin").getVal(), self.workspace4limit_.var("rate_VV_for_unbin").getVal()  ) )
        datacard_out.write( "\n-------------------------------- " )
        datacard_out.write( "\n#lumi    lnN        1.044     -        1.044  1.044    1.044" )
        datacard_out.write( "\n#pdf_gg  lnN        1.099     -        -      -        -" )
        datacard_out.write( "\n#XS_hig  lnN        1.137     -        -      -        -" )
        datacard_out.write( "\n#WJ_norm gmN %s     -         %s       -      -        -"%(self.number_WJets_insideband, self.datadriven_alpha_WJets_unbin) )
        datacard_out.write( "\n#XS_TTbar lnN       -         -        1.07   -        -" )
        datacard_out.write( "\n#XS_STop  lnN       -         -        -      1.07     -" )
        datacard_out.write( "\n#XS_VV   lnN        -         -        -      -        1.10 " )
        for i in range(len(params_list)):
            datacard_out.write( "\n%s param  %s  %s "%( params_list[i].GetName(), params_list[i].getVal(), params_list[i].getError() ) ) 

    ######## ++++++++++++++
    def print_limit_datacard_counting(self):
        print "print_limit_datacard_counting"

        datacard_out=open(self.file_datacard_counting,"w");
        datacard_out.write( "imax 1" )
        datacard_out.write( "\njmax 4" )
        datacard_out.write( "\nkmax *" )
        datacard_out.write( "\n--------------- " )
        datacard_out.write( "\nbin 1 " )
        #datacard_out.write( "\nobservation %s "%(self.workspace4fit_.var("rrv_number_dataset_signal_region_data_mlvj").getVal()) )
        datacard_out.write( "\nobservation %s "%(self.workspace4limit_.var("observation_for_counting").getVal()) )
        datacard_out.write( "\n------------------------------" )
        datacard_out.write( "\nbin                1         1        1        1      1" )
        datacard_out.write( "\nprocess            %s    WJets    TTbar    STop   VV "%(self.higgs_sample) )
        datacard_out.write( "\nprocess            0         1        2        3      4" )
        datacard_out.write( "\nrate               %s        %s       %s     %s     %s"%(self.workspace4limit_.var("rate_%s_for_counting"%(self.higgs_sample)).getVal(), self.workspace4limit_.var("rate_WJets_for_counting").getVal(), self.workspace4limit_.var("rate_TTbar_for_counting").getVal(), self.workspace4limit_.var("rate_STop_for_counting").getVal(), self.workspace4limit_.var("rate_VV_for_counting").getVal()  ) )
        #datacard_out.write( "\nrate               %s        %s       %s     %s     %s"%(self.workspace4fit_.var("rrv_number_fitting_signal_region_%s_mlvj"%(self.higgs_sample)).getVal(), self.workspace4fit_.var("rrv_number_fitting_signal_region_WJets_mlvj").getVal(), self.workspace4fit_.var("rrv_number_fitting_signal_region_TTbar_mlvj").getVal(), self.workspace4fit_.var("rrv_number_fitting_signal_region_STop_mlvj").getVal(), self.workspace4fit_.var("rrv_number_fitting_signal_region_VV_mlvj").getVal()  ) )
        #datacard_out.write( "\nrate               %s        %s       %s     %s     %s"%(self.workspace4fit_.var("rrv_number_fitting_signal_region_%s_mlvj"%(self.higgs_sample)).getVal()/50., self.workspace4fit_.var("rrv_number_fitting_signal_region_WJets_mlvj").getVal(), self.workspace4fit_.var("rrv_number_fitting_signal_region_TTbar_mlvj").getVal(), self.workspace4fit_.var("rrv_number_fitting_signal_region_STop_mlvj").getVal(), self.workspace4fit_.var("rrv_number_fitting_signal_region_VV_mlvj").getVal()  ) )
        datacard_out.write( "\n-------------------------------- " )
        datacard_out.write( "\n#lumi    lnN        1.044     -        1.044  1.044    1.044" )
        datacard_out.write( "\n#pdf_gg  lnN        1.099     -        -      -        -" )
        datacard_out.write( "\n#XS_hig  lnN        1.137     -        -      -        -" )
        datacard_out.write( "\n#WJ_norm gmN %s     -         %s       -      -        -"%(self.number_WJets_insideband, self.datadriven_alpha_WJets_counting) )
        datacard_out.write( "\n#XS_TTbar lnN       -         -        1.07   -        - " )
        datacard_out.write( "\n#XS_STop  lnN       -         -        -      1.07     -  " )
        datacard_out.write( "\n#XS_VV   lnN        -         -        -      -        1.10\n" )

    ######## ++++++++++++++
    def prepare_limit_fitting_method(self):
        print "prepare_limit_fitting_method"
        #prepare for Limit
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_mass_lvj"));
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_fitting_signal_region_%s_mlvj"%(self.higgs_sample)).clone("rate_%s_for_counting"%(self.higgs_sample) ) )
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_fitting_signal_region_WJets_mlvj").clone("rate_WJets_for_counting"))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_fitting_signal_region_VV_mlvj").clone("rate_VV_for_counting"))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_fitting_signal_region_TTbar_mlvj").clone("rate_TTbar_for_counting"))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_fitting_signal_region_STop_mlvj").clone("rate_STop_for_counting"))

        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_%s_signal_region_mlvj"%(self.higgs_sample)).clone("rate_%s_for_unbin"%(self.higgs_sample)));
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_WJets_signal_region_mlvj").clone("rate_WJets_for_unbin"));
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_VV_signal_region_mlvj").clone("rate_VV_for_unbin"));
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_TTbar_signal_region_mlvj").clone("rate_TTbar_for_unbin"));
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_STop_signal_region_mlvj").clone("rate_STop_for_unbin"));
 
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.data("rdataset_data_signal_region_mlvj").Clone("data_obs"))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.pdf("model_pdf_WJets_signal_region_mlvj").clone("WJets"))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.pdf("model_pdf_TTbar_signal_region_mlvj").clone("TTbar"))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.pdf("model_pdf_STop_signal_region_mlvj").clone("STop"))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.pdf("model_pdf_VV_signal_region_mlvj").clone("VV"))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.pdf("model_pdf_%s_signal_region_mlvj"%(self.higgs_sample)).clone(self.higgs_sample))

        self.save_for_limit();
        params_list=[]
        params_list.append(self.workspace4fit_.var("rrv_c_ErfExp_WJets_signal_region"))
        params_list.append(self.workspace4fit_.var("rrv_offset_ErfExp_WJets_signal_region"))
        params_list.append(self.workspace4fit_.var("rrv_width_ErfExp_WJets_signal_region"))
        self.print_limit_datacard_unbin(params_list);
        self.print_limit_datacard_counting();
    ######## ++++++++++++++
    def prepare_limit_sideband_correction_method(self):
        print "prepare_limit_sideband_correction_method"
        ##prepare for Limit
        #getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_mass_lvj").clone("x"));
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_mass_lvj"));
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_fitting_signal_region_%s_mlvj"%(self.higgs_sample)).clone("rate_%s_for_counting"%(self.higgs_sample) ) )
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_fitting_signal_region_WJets_mlvj").clone("rate_WJets_for_counting"))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_fitting_signal_region_VV_mlvj").clone("rate_VV_for_counting"))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_fitting_signal_region_TTbar_mlvj").clone("rate_TTbar_for_counting"))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_fitting_signal_region_STop_mlvj").clone("rate_STop_for_counting"))

        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_%s_signal_region_mlvj"%(self.higgs_sample)).clone("rate_%s_for_unbin"%(self.higgs_sample)));
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_WJets_signal_region_mlvj").clone("rate_WJets_for_unbin"));
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_VV_signal_region_mlvj").clone("rate_VV_for_unbin"));
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_TTbar_signal_region_mlvj").clone("rate_TTbar_for_unbin"));
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_STop_signal_region_mlvj").clone("rate_STop_for_unbin"));

        getattr(self.workspace4limit_,"import")(self.workspace4fit_.data("rdataset_data_signal_region_mlvj").Clone("data_obs"))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.pdf("model_pdf_WJets_signal_region_after_correct").clone("WJets"))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.pdf("model_pdf_TTbar_signal_region_mlvj").clone("TTbar"))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.pdf("model_pdf_STop_signal_region_mlvj").clone("STop"))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.pdf("model_pdf_VV_signal_region_mlvj").clone("VV"))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.pdf("model_pdf_%s_signal_region_mlvj"%(self.higgs_sample)).clone(self.higgs_sample))

        self.save_for_limit();
        params_list=[]
        params_list.append(self.workspace4fit_.var("rrv_c_ErfExp_WJets_sb_lo_from_fitting"))
        params_list.append(self.workspace4fit_.var("rrv_offset_ErfExp_WJets_sb_lo_from_fitting"))
        params_list.append(self.workspace4fit_.var("rrv_width_ErfExp_WJets_sb_lo_from_fitting"))
        self.print_limit_datacard_unbin(params_list);
        self.print_limit_datacard_counting();
         

    ######## ++++++++++++++
    def read_workspace(self):
        file = TFile(self.file_rlt_root) ;
        workspace = file.Get("workspace4limit_") ;
        workspace.Print()

        parameters_workspace=workspace.allVars();
        par=parameters_workspace.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            param.Print();
            param=par.Next()
        print "___________________________________________________"

        workspace.data("data_obs").Print()
        print "___________________________________________________"
        pdfs_workspace=workspace.allPdfs();
        par=pdfs_workspace.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            param.Print();
            param=par.Next()
        print "___________________________________________________"



        rrv_x=workspace.var("rrv_mass_lvj")
        rrv_x.setBins(50)
        data_obs=workspace.data("data_obs")
        model_pdf_ggH=workspace.pdf("%s"%(self.higgs_sample))
        model_pdf_WJets=workspace.pdf("WJets")
        model_pdf_VV=workspace.pdf("VV")
        model_pdf_TTbar=workspace.pdf("TTbar")
        model_pdf_STop=workspace.pdf("STop")
        rrv_number_ggH=workspace.var("rate_%s_for_unbin"%(self.higgs_sample))
        rrv_number_WJets=workspace.var("rate_WJets_for_unbin")
        rrv_number_VV=workspace.var("rate_VV_for_unbin")
        rrv_number_TTbar=workspace.var("rate_TTbar_for_unbin")
        rrv_number_STop=workspace.var("rate_STop_for_unbin")

        scale_number_ggH=rrv_number_ggH.getVal()/data_obs.sumEntries()
        scale_number_WJets=rrv_number_WJets.getVal()/data_obs.sumEntries()
        scale_number_VV=rrv_number_VV.getVal()/data_obs.sumEntries()
        scale_number_TTbar=rrv_number_TTbar.getVal()/data_obs.sumEntries()
        scale_number_STop=rrv_number_STop.getVal()/data_obs.sumEntries()


        model_Total_background_MC=RooAddPdf("model_Total_background_MC","model_Total_background_MC",RooArgList(model_pdf_WJets,model_pdf_VV,model_pdf_TTbar,model_pdf_STop),RooArgList(rrv_number_WJets,rrv_number_VV,rrv_number_TTbar,rrv_number_STop));

        mplot=rrv_x.frame(RooFit.Title("check"));
        data_obs.plotOn(mplot ,RooFit.DataError(RooAbsData.SumW2), RooFit.Name("data_invisible"),RooFit.Invisible());

        model_pdf_STop.plotOn(mplot,RooFit.Normalization(scale_number_STop),RooFit.Name("STop_invisible"),RooFit.Invisible(), RooFit.VLines(),RooFit.Precision(1e-8))
        model_pdf_TTbar.plotOn(mplot,RooFit.Normalization(scale_number_TTbar),RooFit.Name("TTbar_invisible"), RooFit.AddTo("STop_invisible"),RooFit.Invisible(), RooFit.VLines(),RooFit.Precision(1e-8))
        model_pdf_VV.plotOn(mplot,RooFit.Normalization(scale_number_VV),RooFit.Name("VV_invisible"), RooFit.AddTo("TTbar_invisible"),RooFit.Invisible(), RooFit.VLines(),RooFit.Precision(1e-8))
        model_pdf_WJets.plotOn(mplot,RooFit.Normalization(scale_number_WJets),RooFit.Name("WJets_invisible"), RooFit.AddTo("VV_invisible"),RooFit.Invisible(), RooFit.VLines(),RooFit.Precision(1e-8))
        model_pdf_WJets.plotOn(mplot,RooFit.Normalization(scale_number_WJets),RooFit.Name("WJets"), RooFit.AddTo("VV_invisible"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["WJets"]), RooFit.LineColor(self.color_palet["WJets"]), RooFit.VLines(),RooFit.Precision(1e-8))
        model_pdf_VV.plotOn(mplot,RooFit.Normalization(scale_number_VV),RooFit.Name("VV"), RooFit.AddTo("TTbar_invisible"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["VV"]), RooFit.LineColor(self.color_palet["VV"]), RooFit.VLines(),RooFit.Precision(1e-8))
        model_pdf_TTbar.plotOn(mplot,RooFit.Normalization(scale_number_TTbar),RooFit.Name("TTbar"), RooFit.AddTo("STop_invisible"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["TTbar"]), RooFit.LineColor(self.color_palet["TTbar"]), RooFit.VLines(),RooFit.Precision(1e-8))
        model_pdf_STop.plotOn(mplot,RooFit.Normalization(scale_number_STop),RooFit.Name("STop"), RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["STop"]), RooFit.LineColor(self.color_palet["STop"]), RooFit.VLines(),RooFit.Precision(1e-8))
        model_pdf_ggH.plotOn(mplot,RooFit.Normalization(scale_number_ggH),RooFit.Name("%s"%(self.higgs_sample)),RooFit.DrawOption("L"), RooFit.LineColor(self.color_palet["Signal"]), RooFit.VLines(),RooFit.Precision(1e-8))
        data_obs.plotOn(mplot ,RooFit.DataError(RooAbsData.SumW2), RooFit.Name("data"))
        
        mplot.Print()
        leg=self.legend4Plot(mplot,0)
        mplot.addObject(leg)
        self.draw_canvas1(mplot,"plots/m_lvj_BDTcut/","check_workspace_for_limit");

    ######## ++++++++++++++
    def save_for_limit(self):
        self.workspace4limit_.Print()
        self.workspace4limit_.var("rrv_mass_lvj").Print()
        self.workspace4limit_.writeToFile(self.file_rlt_root);
        self.file_out.close()
    ######## ++++++++++++++
    def legend4Plot(self, plot, left=1):
        if left: 
            theLeg = TLegend(0.2, 0.62, 0.55, 0.92, "", "NDC");
        else:
            theLeg = TLegend(0.65, 0.57, 0.92, 0.87, "", "NDC");
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
        for obj in range(int(plot.numItems()) ):
            objName = plot.nameOf(obj);
            if not ( (plot.getInvisible(objName)) or TString(objName).Contains("invisi") ): 
                theObj = plot.getObject(obj);
                objTitle = objName;
                drawoption= plot.getDrawOptions(objName).Data()
                if drawoption=="P":drawoption="PE"
                theLeg.AddEntry(theObj, objTitle,drawoption);
                entryCnt=entryCnt+1;

        theLeg.SetY1NDC(0.9 - 0.05*entryCnt - 0.005);
        theLeg.SetY1(theLeg.GetY1NDC());
        return theLeg;

    ######## ++++++++++++++
    def draw_canvas(self, mplot, mplot_pull,parameters_list,in_directory, in_file_name, in_model_name="", show_constant_parameter=0):

        mplot.GetXaxis().SetTitleOffset(1.1);
        mplot.GetYaxis().SetTitleOffset(1.1);
        mplot.GetXaxis().SetTitleSize(0.04);
        mplot.GetYaxis().SetTitleSize(0.04);
        mplot.GetXaxis().SetLabelSize(0.04);
        mplot.GetYaxis().SetLabelSize(0.04);
        mplot_pull.GetYaxis().SetTitleOffset(1.0);
        xtitle=TString(mplot.GetXaxis().GetTitle());
        num_unit_start=xtitle.First("[");
        num_unit_end=xtitle.First("]");
        unit_string=TString("");
        for i in range(num_unit_start+1,num_unit_end):
            unit_string.Append(xtitle[i]);
        unit=unit_string.Data();
        ytitle=("Evetns / %s %s")%(mplot.GetXaxis().GetBinWidth(1),unit);
        mplot.GetYaxis().SetTitle(ytitle);

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
                latex.DrawLatex(0,0.9-i*0.04,"#color[%s]{%s}"%(icolor,param.GetName()) );
                latex.DrawLatex(0,0.9-i*0.04-0.02," #color[%s]{%4.3e +/- %2.1e}"%(icolor,param.getVal(),param.getError()) );
                i=i+1;
            param=par.Next();

        Directory=TString(in_directory+self.higgs_sample+"/");
        if not Directory.EndsWith("/"):Directory=Directory.Append("/");
        if not os.path.isdir(Directory.Data()): os.system("mkdir -p  "+Directory.Data());

        rlt_file=TString(Directory.Data()+in_file_name);
        if rlt_file.EndsWith(".root"):
            rlt_file.ReplaceAll(".root","_"+in_model_name+"_rlt.png");
        else:
            rlt_file=rlt_file.Append("_"+in_model_name+"_rlt.png");
        cMassFit.SaveAs(rlt_file.Data());
        rlt_file.ReplaceAll(".png",".eps"); 
        cMassFit.SaveAs(rlt_file.Data());

        self.draw_canvas1(mplot,in_directory,in_file_name,0,0);
        #cMassFit.SetLogy() ;
        #cMassFit.Update();
        #rlt_file.ReplaceAll(".eps","_log.eps"); 
        #cMassFit.SaveAs(rlt_file.Data());
        #rlt_file.ReplaceAll(".eps",".png"); 
        #cMassFit.SaveAs(rlt_file.Data());   
        
    ######## ++++++++++++++
    def draw_canvas1(self, in_obj,in_directory, in_file_name, is_range=0, log=1):
        cMassFit = TCanvas("cMassFit","cMassFit",1000,800);
        if is_range:
            h2=TH2D("h2","",100,400,1400,4,0.00001,4); h2.Draw(); in_obj.Draw("same")
        else : 
            in_obj.Draw()

        Directory=TString(in_directory+self.higgs_sample+"/");
        if not Directory.EndsWith("/"):Directory=Directory.Append("/");
        if not os.path.isdir(Directory.Data()): os.system("mkdir -p  "+Directory.Data());

        rlt_file=TString(Directory.Data()+in_file_name);
        if rlt_file.EndsWith(".root"):
            rlt_file.ReplaceAll(".root","_rlt_without_pull_and_paramters.png");
        else:
            rlt_file=rlt_file.Append("_rlt_without_pull_and_paramters.png");
        cMassFit.SaveAs(rlt_file.Data());
        rlt_file.ReplaceAll(".png",".eps"); 
        cMassFit.SaveAs(rlt_file.Data());

        if log:
            cMassFit.SetLogy() ;
            cMassFit.Update();
            rlt_file.ReplaceAll(".eps","_log.eps"); 
            cMassFit.SaveAs(rlt_file.Data());
            rlt_file.ReplaceAll(".eps",".png"); 
            cMassFit.SaveAs(rlt_file.Data());

    ######## ++++++++++++++
    def get_data(self, bool_fake_data=1):
        print "get_data"
        if bool_fake_data:
            rdataset_WJets_mj=self.workspace4fit_.data("rdataset_WJets_mj")
            rdataset_VV_mj=self.workspace4fit_.data("rdataset_VV_mj")
            rdataset_TTbar_mj=self.workspace4fit_.data("rdataset_TTbar_mj")
            rdataset_STop_mj=self.workspace4fit_.data("rdataset_STop_mj")
            rdataset_data_mj = rdataset_WJets_mj.Clone("rdataset_data_mj");
            rdataset_data_mj.append(rdataset_VV_mj)
            rdataset_data_mj.append(rdataset_TTbar_mj)
            rdataset_data_mj.append(rdataset_STop_mj)

            rdataset_WJets_sb_lo_mlvj=self.workspace4fit_.data("rdataset_WJets_sb_lo_mlvj")
            rdataset_VV_sb_lo_mlvj=self.workspace4fit_.data("rdataset_VV_sb_lo_mlvj")
            rdataset_TTbar_sb_lo_mlvj=self.workspace4fit_.data("rdataset_TTbar_sb_lo_mlvj")
            rdataset_STop_sb_lo_mlvj=self.workspace4fit_.data("rdataset_STop_sb_lo_mlvj")
            rdataset_data_sb_lo_mlvj =rdataset_WJets_sb_lo_mlvj.Clone("rdataset_data_sb_lo_mlvj")
            rdataset_data_sb_lo_mlvj.append(rdataset_VV_sb_lo_mlvj)
            rdataset_data_sb_lo_mlvj.append(rdataset_TTbar_sb_lo_mlvj)
            rdataset_data_sb_lo_mlvj.append(rdataset_STop_sb_lo_mlvj)   

            rdataset_WJets_signal_region_mlvj=self.workspace4fit_.data("rdataset_WJets_signal_region_mlvj")
            rdataset_VV_signal_region_mlvj=self.workspace4fit_.data("rdataset_VV_signal_region_mlvj")
            rdataset_TTbar_signal_region_mlvj=self.workspace4fit_.data("rdataset_TTbar_signal_region_mlvj")
            rdataset_STop_signal_region_mlvj=self.workspace4fit_.data("rdataset_STop_signal_region_mlvj")
            rdataset_data_signal_region_mlvj =rdataset_WJets_signal_region_mlvj.Clone("rdataset_data_signal_region_mlvj")
            rdataset_data_signal_region_mlvj.append(rdataset_VV_signal_region_mlvj)
            rdataset_data_signal_region_mlvj.append(rdataset_TTbar_signal_region_mlvj)
            rdataset_data_signal_region_mlvj.append(rdataset_STop_signal_region_mlvj)   

            rdataset_WJets_sb_hi_mlvj=self.workspace4fit_.data("rdataset_WJets_sb_hi_mlvj")
            rdataset_VV_sb_hi_mlvj=self.workspace4fit_.data("rdataset_VV_sb_hi_mlvj")
            rdataset_TTbar_sb_hi_mlvj=self.workspace4fit_.data("rdataset_TTbar_sb_hi_mlvj")
            rdataset_STop_sb_hi_mlvj=self.workspace4fit_.data("rdataset_STop_sb_hi_mlvj")
            rdataset_data_sb_hi_mlvj =rdataset_WJets_sb_hi_mlvj.Clone("rdataset_data_sb_hi_mlvj")
            rdataset_data_sb_hi_mlvj.append(rdataset_VV_sb_hi_mlvj)
            rdataset_data_sb_hi_mlvj.append(rdataset_TTbar_sb_hi_mlvj)
            rdataset_data_sb_hi_mlvj.append(rdataset_STop_sb_hi_mlvj)    

            getattr(self.workspace4fit_,"import")(rdataset_data_mj)
            getattr(self.workspace4fit_,"import")(rdataset_data_sb_lo_mlvj)
            getattr(self.workspace4fit_,"import")(rdataset_data_signal_region_mlvj)
            getattr(self.workspace4fit_,"import")(rdataset_data_sb_hi_mlvj)

            rrv_number_dataset_signal_region_mlvj=RooRealVar("rrv_number_dataset_signal_region_data_mlvj","rrv_number_dataset_signal_region_data_mlvj",self.workspace4fit_.var("rrv_number_dataset_signal_region_WJets_mlvj").getVal()+self.workspace4fit_.var("rrv_number_dataset_signal_region_VV_mlvj").getVal()+self.workspace4fit_.var("rrv_number_dataset_signal_region_TTbar_mlvj").getVal()+self.workspace4fit_.var("rrv_number_dataset_signal_region_STop_mlvj").getVal());
            rrv_number_dataset_AllRange_mlvj=RooRealVar("rrv_number_dataset_AllRange_data_mlvj","rrv_number_dataset_AllRange_data_mlvj",rdataset_data_signal_region_mlvj.sumEntries());
            rrv_number_dataset_signal_region_mlvj.Print()
            rrv_number_dataset_AllRange_mlvj.Print()
            getattr(self.workspace4fit_,"import")(rrv_number_dataset_signal_region_mlvj)
            getattr(self.workspace4limit_,"import")(rrv_number_dataset_signal_region_mlvj.clone("rate_data_for_unbin"));
            getattr(self.workspace4fit_,"import")(rrv_number_dataset_AllRange_mlvj)
            
            rrv_number_dataset_sb_lo_mj=RooRealVar("rrv_number_dataset_sb_lo_data_mj","rrv_number_dataset_sb_lo_data_mj",self.workspace4fit_.var("rrv_number_dataset_sb_lo_WJets_mj").getVal()+self.workspace4fit_.var("rrv_number_dataset_sb_lo_VV_mj").getVal()+self.workspace4fit_.var("rrv_number_dataset_sb_lo_TTbar_mj").getVal()+self.workspace4fit_.var("rrv_number_dataset_sb_lo_STop_mj").getVal());
            rrv_number_dataset_signal_region_mj=RooRealVar("rrv_number_dataset_signal_region_data_mj","rrv_number_dataset_signal_region_data_mj",self.workspace4fit_.var("rrv_number_dataset_signal_region_WJets_mj").getVal()+self.workspace4fit_.var("rrv_number_dataset_signal_region_VV_mj").getVal()+self.workspace4fit_.var("rrv_number_dataset_signal_region_TTbar_mj").getVal()+self.workspace4fit_.var("rrv_number_dataset_signal_region_STop_mj").getVal());
            rrv_number_dataset_sb_hi_mj=RooRealVar("rrv_number_dataset_sb_hi_data_mj","rrv_number_dataset_sb_hi_data_mj",self.workspace4fit_.var("rrv_number_dataset_sb_hi_WJets_mj").getVal()+self.workspace4fit_.var("rrv_number_dataset_sb_hi_VV_mj").getVal()+self.workspace4fit_.var("rrv_number_dataset_sb_hi_TTbar_mj").getVal()+self.workspace4fit_.var("rrv_number_dataset_sb_hi_STop_mj").getVal());
            getattr(self.workspace4fit_,"import")(rrv_number_dataset_sb_lo_mj)
            getattr(self.workspace4fit_,"import")(rrv_number_dataset_signal_region_mj)
            getattr(self.workspace4fit_,"import")(rrv_number_dataset_sb_hi_mj)
            
            rrv_number_dataset_sb_lo_mj.Print()
            rrv_number_dataset_signal_region_mj.Print()
            rrv_number_dataset_sb_hi_mj.Print()
            rrv_number_dataset_signal_region_mlvj.Print()
            rrv_number_dataset_AllRange_mlvj.Print()
            print rrv_number_dataset_signal_region_mlvj.getVal()
            print rrv_number_dataset_AllRange_mlvj.getVal()
            print rdataset_data_signal_region_mlvj.sumEntries()

        else:
            self.get_mj_and_mlvj_dataset(self.file_data,"_data")
            print "blind!!!"
        #self.get_mj_and_mlvj_dataset(self.file_data,"_data")
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_dataset_signal_region_data_mlvj").clone("observation_for_counting"))
        print "________________________________________________________________________"
 
    ######## ++++++++++++++
    #def get_other_backgrounds_mj_and_mlvj_dataset(self):# VV+TTbar+STop
    #    print "get_other_backgrounds_mj_and_mlvj_dataset"
    #    rdataset_VV_mj=self.workspace4fit_.data("rdataset_VV_mj")
    #    rdataset_TTbar_mj=self.workspace4fit_.data("rdataset_TTbar_mj")
    #    rdataset_STop_mj=self.workspace4fit_.data("rdataset_STop_mj")
    #    rdataset_other_backgrounds_mj = rdataset_VV_mj.Clone("rdataset_other_backgrounds_mj");
    #    rdataset_other_backgrounds_mj.append(rdataset_TTbar_mj)
    #    rdataset_other_backgrounds_mj.append(rdataset_STop_mj)

    #    rdataset_VV_sb_lo_mlvj=self.workspace4fit_.data("rdataset_VV_sb_lo_mlvj")
    #    rdataset_TTbar_sb_lo_mlvj=self.workspace4fit_.data("rdataset_TTbar_sb_lo_mlvj")
    #    rdataset_STop_sb_lo_mlvj=self.workspace4fit_.data("rdataset_STop_sb_lo_mlvj")
    #    rdataset_other_backgrounds_sb_lo_mlvj =rdataset_VV_sb_lo_mlvj.Clone("rdataset_other_backgrounds_sb_lo_mlvj")
    #    rdataset_other_backgrounds_sb_lo_mlvj.append(rdataset_TTbar_sb_lo_mlvj)
    #    rdataset_other_backgrounds_sb_lo_mlvj.append(rdataset_STop_sb_lo_mlvj)   

    #    rdataset_VV_signal_region_mlvj=self.workspace4fit_.data("rdataset_VV_signal_region_mlvj")
    #    rdataset_TTbar_signal_region_mlvj=self.workspace4fit_.data("rdataset_TTbar_signal_region_mlvj")
    #    rdataset_STop_signal_region_mlvj=self.workspace4fit_.data("rdataset_STop_signal_region_mlvj")
    #    rdataset_other_backgrounds_signal_region_mlvj =rdataset_VV_signal_region_mlvj.Clone("rdataset_other_backgrounds_signal_region_mlvj")
    #    rdataset_other_backgrounds_signal_region_mlvj.append(rdataset_TTbar_signal_region_mlvj)
    #    rdataset_other_backgrounds_signal_region_mlvj.append(rdataset_STop_signal_region_mlvj)   

    #    rdataset_VV_sb_hi_mlvj=self.workspace4fit_.data("rdataset_VV_sb_hi_mlvj")
    #    rdataset_TTbar_sb_hi_mlvj=self.workspace4fit_.data("rdataset_TTbar_sb_hi_mlvj")
    #    rdataset_STop_sb_hi_mlvj=self.workspace4fit_.data("rdataset_STop_sb_hi_mlvj")
    #    rdataset_other_backgrounds_sb_hi_mlvj =rdataset_VV_sb_hi_mlvj.Clone("rdataset_other_backgrounds_sb_hi_mlvj")
    #    rdataset_other_backgrounds_sb_hi_mlvj.append(rdataset_TTbar_sb_hi_mlvj)
    #    rdataset_other_backgrounds_sb_hi_mlvj.append(rdataset_STop_sb_hi_mlvj)    

    #    getattr(self.workspace4fit_,"import")(rdataset_other_backgrounds_mj)
    #    getattr(self.workspace4fit_,"import")(rdataset_other_backgrounds_sb_lo_mlvj)
    #    getattr(self.workspace4fit_,"import")(rdataset_other_backgrounds_signal_region_mlvj)
    #    getattr(self.workspace4fit_,"import")(rdataset_other_backgrounds_sb_hi_mlvj)
    #    
    #    self.workspace4fit_.var("rrv_scale_to_lumi_WJets").Print()
    #    self.workspace4fit_.var("rrv_scale_to_lumi_VV").Print()
    #    self.workspace4fit_.var("rrv_scale_to_lumi_TTbar").Print()
    #    self.workspace4fit_.var("rrv_scale_to_lumi_STop").Print()
    #    print "________________________________________________________________________"
    #    raw_input("ENTER")
    ######## ++++++++++++++
    def fit_Signal(self):
        print "fit_Signal"
        self.get_mj_and_mlvj_dataset(self.file_ggH,"_%s"%(self.higgs_sample))# to get the shape of m_lvj
        self.fit_m_j_single_MC_sample(self.file_ggH,"_%s"%(self.higgs_sample),"Voig");
        #self.fit_mlvj_model_single_MC_sample(self.file_ggH,"_%s"%(self.higgs_sample),"_signal_region","ErfExpGaus_v1");
        #self.fit_mlvj_model_single_MC_sample(self.file_ggH,"_%s"%(self.higgs_sample),"_signal_region","Keys");
        #self.fit_mlvj_model_single_MC_sample(self.file_ggH,"_%s"%(self.higgs_sample),"_signal_region","BifurGaus_v1");
        self.fit_mlvj_model_single_MC_sample(self.file_ggH,"_%s"%(self.higgs_sample),"_sb_lo","CB_v1");
        self.fit_mlvj_model_single_MC_sample(self.file_ggH,"_%s"%(self.higgs_sample),"_signal_region","CB_v1");
        print "________________________________________________________________________"

    ######## ++++++++++++++
    #def fit_other_backgrounds(self):
    #    print "fit_other_backgrounds"
    #    self.get_other_backgrounds_mj_and_mlvj_dataset()
    #    self.fit_m_j_single_MC_sample("other_backgrounds","_other_backgrounds","ErfExpGaus");
    #    self.fit_mlvj_model_single_MC_sample("other_backgrounds","_other_backgrounds","_sb_lo","ErfExp_v1");
    #    #self.fit_mlvj_model_single_MC_sample("other_backgrounds","_other_backgrounds","_signal_region","ErfExp_v1");
    #    print "________________________________________________________________________"

    ######## ++++++++++++++
    def fit_WJets(self):
        print "fit_WJets"
        self.get_mj_and_mlvj_dataset(self.file_WJets_mc,"_WJets")# to get the shape of m_lvj
        self.fit_m_j_single_MC_sample(self.file_WJets_mc,"_WJets","ErfExp");
        self.fit_mlvj_model_single_MC_sample(self.file_WJets_mc,"_WJets","_sb_lo","ErfExp_v1");
        self.fit_mlvj_model_single_MC_sample(self.file_WJets_mc,"_WJets","_signal_region","ErfExp_v1");
        #self.fit_mlvj_model_single_MC_sample(self.file_WJets_mc,"_WJets","_sb_hi","ErfExp_v1");
        print "________________________________________________________________________" 
    ######## ++++++++++++++
    def fit_ZJets(self):
        print "fit_ZJets"
        self.get_mj_and_mlvj_dataset(self.file_ZJets_mc,"_ZJets")# to get the shape of m_lvj
        self.fit_m_j_single_MC_sample(self.file_ZJets_mc,"_ZJets","ErfExp");
        self.fit_mlvj_model_single_MC_sample(self.file_ZJets_mc,"_ZJets","_sb_lo","ErfExp_v1");
        self.fit_mlvj_model_single_MC_sample(self.file_ZJets_mc,"_ZJets","_signal_region","ErfExp_v1");
        #self.fit_mlvj_model_single_MC_sample(self.file_ZJets_mc,"_ZJets","_sb_hi","ErfExp_v1");
        print "________________________________________________________________________" 
    ######## ++++++++++++++
    def fit_WW(self):
        print "fit_WW"
        self.get_mj_and_mlvj_dataset(self.file_WW_mc,"_WW")# to get the shape of m_lvj
        self.fit_m_j_single_MC_sample(self.file_WW_mc,"_WW","Voig");
        self.fit_mlvj_model_single_MC_sample(self.file_WW_mc,"_WW","_sb_lo","ErfExp_v1");
        self.fit_mlvj_model_single_MC_sample(self.file_WW_mc,"_WW","_signal_region","ErfExp_v1");
        #self.fit_mlvj_model_single_MC_sample(self.file_WW_mc,"_WW","_sb_hi","ErfExp_v1");
        print "________________________________________________________________________"
    ######## ++++++++++++++
    def fit_WZ(self):
        print "fit_WZ"
        self.get_mj_and_mlvj_dataset(self.file_WZ_mc,"_WZ")# to get the shape of m_lvj
        self.fit_m_j_single_MC_sample(self.file_WZ_mc,"_WZ","Voig");
        self.fit_mlvj_model_single_MC_sample(self.file_WZ_mc,"_WZ","_sb_lo","ErfExp_v1");
        self.fit_mlvj_model_single_MC_sample(self.file_WZ_mc,"_WZ","_signal_region","ErfExp_v1");
        #self.fit_mlvj_model_single_MC_sample(self.file_WZ_mc,"_WZ","_sb_hi","ErfExp_v1");
        print "________________________________________________________________________"
 
    ######## ++++++++++++++
    def fit_VV(self):
        print "fit_VV"
        self.get_mj_and_mlvj_dataset(self.file_VV_mc,"_VV")# to get the shape of m_lvj
        self.fit_m_j_single_MC_sample(self.file_VV_mc,"_VV","2Voig");
        self.fit_mlvj_model_single_MC_sample(self.file_VV_mc,"_VV","_sb_lo","ErfExp_v1");
        self.fit_mlvj_model_single_MC_sample(self.file_VV_mc,"_VV","_signal_region","ErfExp_v1");
        #self.fit_mlvj_model_single_MC_sample(self.file_VV_mc,"_VV","_sb_hi","ErfExp_v1");
        print "________________________________________________________________________"
    ######## ++++++++++++++
    def fit_ZZ(self):
        print "fit_ZZ"
        self.get_mj_and_mlvj_dataset(self.file_ZZ_mc,"_ZZ")# to get the shape of m_lvj
        self.fit_m_j_single_MC_sample(self.file_ZZ_mc,"_ZZ","Voig");
        self.fit_mlvj_model_single_MC_sample(self.file_ZZ_mc,"_ZZ","_sb_lo","ErfExp_v1");
        self.fit_mlvj_model_single_MC_sample(self.file_ZZ_mc,"_ZZ","_signal_region","ErfExp_v1");
        #self.fit_mlvj_model_single_MC_sample(self.file_ZZ_mc,"_ZZ","_sb_hi","ErfExp_v1");
        print "________________________________________________________________________"

    ######## ++++++++++++++
    def fit_TTbar(self):
        print "fit_TTbar"
        self.get_mj_and_mlvj_dataset(self.file_TTbar_mc,"_TTbar")# to get the shape of m_lvj
        self.fit_m_j_single_MC_sample(self.file_TTbar_mc,"_TTbar","ErfExpGaus");
        self.fit_mlvj_model_single_MC_sample(self.file_TTbar_mc,"_TTbar","_sb_lo","ErfExp_v1");
        self.fit_mlvj_model_single_MC_sample(self.file_TTbar_mc,"_TTbar","_signal_region","ErfExp_v1");
        #self.fit_mlvj_model_single_MC_sample(self.file_TTbar_mc,"_TTbar","_sb_hi","ErfExp_v1");
        print "________________________________________________________________________"
 
    ######## ++++++++++++++
    def fit_STop(self):
        print "fit_STop"
        self.get_mj_and_mlvj_dataset(self.file_STop_mc,"_STop")# to get the shape of m_lvj
        self.fit_m_j_single_MC_sample(self.file_STop_mc,"_STop","ErfExpGaus");
        self.fit_mlvj_model_single_MC_sample(self.file_STop_mc,"_STop","_sb_lo","ErfExp_v1");
        self.fit_mlvj_model_single_MC_sample(self.file_STop_mc,"_STop","_signal_region","ErfExp_v1");
        #self.fit_mlvj_model_single_MC_sample(self.file_STop_mc,"_STop","_sb_hi","ErfExp_v1");
        print "________________________________________________________________________" 

    ######## ++++++++++++++
    def fit_AllSamples_Mlvj(self):
        print "fit_AllSamples_Mlvj"
        #self.fit_WW() #self.fit_WZ() #self.fit_TTbar() #self.fit_ZZ() #self.fit_ZJets()

        self.fit_Signal()
        self.fit_VV()
        self.fit_TTbar()
        self.fit_STop()
        self.fit_WJets()
        #self.fit_other_backgrounds()
        print "________________________________________________________________________" 
    ####### +++++++++++++++
    def fit_TTbar_contralsample(self):
        print "fit_TTbar_contralsample"
        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j"); rrv_mass_j.setBins(40)
        self.get_mj_and_mlvj_dataset_TTbar_contralsample(self.file_TTbar_mc,"_TTbar");self.fit_m_j_single_MC_sample_TTbar_contralsample(self.file_TTbar_mc,"_TTbar","ErfExpGaus");
        self.get_mj_and_mlvj_dataset_TTbar_contralsample(self.file_VV_mc,"_VV");self.fit_m_j_single_MC_sample_TTbar_contralsample(self.file_VV_mc,"_VV","ErfExpGaus");
        self.get_mj_and_mlvj_dataset_TTbar_contralsample(self.file_STop_mc,"_STop");self.fit_m_j_single_MC_sample_TTbar_contralsample(self.file_STop_mc,"_STop","ErfExpGaus");
        self.get_mj_and_mlvj_dataset_TTbar_contralsample(self.file_WJets_mc,"_WJets");self.fit_m_j_single_MC_sample_TTbar_contralsample(self.file_WJets_mc,"_WJets","ErfExpGaus");

        self.get_mj_and_mlvj_dataset_TTbar_contralsample(self.file_data,"_data"); self.fit_m_j_single_MC_sample_TTbar_contralsample(self.file_data,"_data","ErfExpGaus");
        self.fit_m_j_TTbar_contralsample(self.file_data,"ErfExpGaus");

    ####### +++++++++++++++
    def analysis_fitting_method(self,inject_signal):
        self.fit_AllSamples_Mlvj()
        self.get_data(0)
        self.fit_WJetsNormalization_in_Mj_signal_region(inject_signal);
        self.fit_mlvj_in_Mj_signal_region(inject_signal)
        self.prepare_limit_fitting_method()
        self.read_workspace()

    ####### +++++++++++++++
    def analysis_sideband_correction_method(self,inject_signal):
        self.fit_AllSamples_Mlvj()
        self.get_data(0)
        self.fit_WJetsNormalization_in_Mj_signal_region(inject_signal);
        self.fit_mlvj_in_Mj_sideband("_sb_lo",inject_signal)
        self.prepare_limit_sideband_correction_method()
        self.read_workspace()

def test():
    cutOnMassDrop = False;
    boostedW_fitter=doFit_wj_and_wlvj(cutOnMassDrop,"ggH600"); 
    boostedW_fitter.fit_AllSamples_Mlvj()
    #boostedW_fitter.fit_other_backgrounds()
    boostedW_fitter=doFit_wj_and_wlvj(cutOnMassDrop,"ggH700"); boostedW_fitter.fit_AllSamples_Mlvj()
    boostedW_fitter=doFit_wj_and_wlvj(cutOnMassDrop,"ggH800"); boostedW_fitter.fit_AllSamples_Mlvj()
    boostedW_fitter=doFit_wj_and_wlvj(cutOnMassDrop,"ggH900"); boostedW_fitter.fit_AllSamples_Mlvj()
    boostedW_fitter=doFit_wj_and_wlvj(cutOnMassDrop,"ggH1000"); boostedW_fitter.fit_AllSamples_Mlvj()

def get_alpha():
    cutOnMassDrop = False;
    boostedW_fitter=doFit_wj_and_wlvj(cutOnMassDrop)
    boostedW_fitter.fit_alpha_WJets();

def contral_sample():
    cutOnMassDrop = False;
    boostedW_fitter=doFit_wj_and_wlvj(cutOnMassDrop,"ggH600",500,700,0,200)
    boostedW_fitter.fit_TTbar_contralsample();


def pre_limit_fitting_method(higgs_sample="ggH600", in_mlvj_signal_region_min=500, in_mlvj_signal_region_max=700, in_mj_min=30, in_mj_max=140, in_mlvj_min=400, in_mlvj_max=1400): 
    inject_signal=0;# 0: not inject_signal; 1: inject_signal
    cutOnMassDrop = False;
    boostedW_fitter=doFit_wj_and_wlvj(cutOnMassDrop, higgs_sample, in_mlvj_signal_region_min, in_mlvj_signal_region_max, in_mj_min, in_mj_max, in_mlvj_min, in_mlvj_max)
    boostedW_fitter.analysis_fitting_method(inject_signal)

def pre_limit_sb_correction_method(higgs_sample="ggH600", in_mlvj_signal_region_min=500, in_mlvj_signal_region_max=700, in_mj_min=30, in_mj_max=140, in_mlvj_min=400, in_mlvj_max=1400): 
    inject_signal=0;# 0: not inject_signal; 1: inject_signal
    cutOnMassDrop = False;
    boostedW_fitter=doFit_wj_and_wlvj(cutOnMassDrop, higgs_sample, in_mlvj_signal_region_min, in_mlvj_signal_region_max, in_mj_min, in_mj_max, in_mlvj_min, in_mlvj_max)
    boostedW_fitter.analysis_sideband_correction_method(inject_signal)

def pre_limit_All():
    #pre_limit_fitting_method("ggH600",500,700)
    #pre_limit_fitting_method("ggH700" ,600,850)
    #pre_limit_fitting_method("ggH800" ,650,1000)
    #pre_limit_fitting_method("ggH900" ,750,1100)
    #pre_limit_fitting_method("ggH1000",800,1150)

    pre_limit_sb_correction_method("ggH600",500,700)
    #pre_limit_sb_correction_method("ggH700" ,600,850)
    #pre_limit_sb_correction_method("ggH800" ,650,1000)
    #pre_limit_sb_correction_method("ggH900" ,750,1100)
    #pre_limit_sb_correction_method("ggH1000",800,1150)

def check_workspace():
    cutOnMassDrop = False;
    boostedW_fitter=doFit_wj_and_wlvj(cutOnMassDrop,"ggH600"); boostedW_fitter.read_workspace()
    #boostedW_fitter=doFit_wj_and_wlvj(cutOnMassDrop,"ggH700"); boostedW_fitter.read_workspace()
    #boostedW_fitter=doFit_wj_and_wlvj(cutOnMassDrop,"ggH800"); boostedW_fitter.read_workspace()
    #boostedW_fitter=doFit_wj_and_wlvj(cutOnMassDrop,"ggH900"); boostedW_fitter.read_workspace()
    #boostedW_fitter=doFit_wj_and_wlvj(cutOnMassDrop,"ggH1000"); boostedW_fitter.read_workspace()

if __name__ == '__main__':
    #get_WJets_normalization()
    #get_alpha()
    #pre_limit_fitting_method()
    #test()
    #check_workspace()
    #contral_sample()
    pre_limit_All()


    ##print sys.argv
    ##print len(sys.argv)
    ##if len(sys.argv)==4 or len(sys.argv)==5: 
    ##    pre_limit_fitting_method(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))
    ##    #pre_limit_sb_correction_method(sys.argv[1],sys.argv[2],sys.argv[3])
    ##else:
    ##    pre_limit_fitting_method()
    ##    #pre_limit_sb_correction_method()
