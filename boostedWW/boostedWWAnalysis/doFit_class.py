#! /usr/bin/env python
import os
import glob
import math
import array

from ROOT import gROOT, gStyle, gSystem, TLatex, TString, TF1,TFile,TLine, TLegend, TH1D,TH2D,THStack,TChain, TCanvas, TMatrixDSym, TMath, TText, TPad, RooFit, RooArgSet, RooArgList, RooArgSet, RooAbsData, RooAbsPdf, RooAddPdf, RooWorkspace, RooExtendPdf,RooCBShape, RooLandau, RooFFTConvPdf, RooGaussian, RooBifurGauss, RooDataSet, RooExponential,RooBreitWigner, RooVoigtian, RooNovosibirsk, RooRealVar,RooFormulaVar, RooDataHist, RooHistPdf,RooCategory, RooSimultaneous, RooGenericPdf, RooKeysPdf, RooHistPdf, RooEffProd, RooProdPdf, TIter, kTRUE, kFALSE, kGray, kRed, kDashed, kGreen,kAzure, kOrange, kBlack,kBlue,kYellow,kCyan
import subprocess
from subprocess import Popen

from sampleWrapperClass import *
from trainingClass      import *
from BoostedWSamples    import * 
from mvaApplication     import *

import sys

if os.path.isfile('tdrstyle.C'):
   gROOT.ProcessLine('.L tdrstyle.C')
   ROOT.setTDRStyle()
   print "Found tdrstyle.C file, using this style."
   if os.path.isfile('CMSTopStyle.cc'):
      gROOT.ProcessLine('.L CMSTopStyle.cc+')
      style = ROOT.CMSTopStyle()
      style.setupICHEPv1()
      print "Found CMSTopStyle.cc file, use TOP style if requested in xml file."


ROOT.gSystem.Load("PDFs/Util_cxx.so")
ROOT.gSystem.Load("PDFs/PdfDiagonalizer_cc.so")
ROOT.gSystem.Load("PDFs/HWWLVJ_RooPdfs_cxx.so")
ROOT.gSystem.Load("PDFs/RooEXO2011414Pdf_cxx.so")

from ROOT import draw_error_band, draw_error_band_extendPdf, draw_error_band_Decor, Calc_error_extendPdf, RooErfExpPdf, RooAlpha,PdfDiagonalizer, RooEXO2011414Pdf

############################################################
############################################
#            Job steering                  #
############################################
parser = OptionParser()

parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
parser.add_option('-f','--fitwtagger', action='store_true', dest='fitwtagger', default=False, help='fit wtagger jet in ttbar control sample')
parser.add_option('-s','--single', action='store_true', dest='single', default=True, help='pre-limit in single mode')
parser.add_option('-m','--multi', action='store_true', dest='multi', default=False, help='pre-limit in multi mode')
parser.add_option('--check', action='store_true', dest='check', default=False, help='check the workspace for limit setting')
parser.add_option('--control', action='store_true', dest='control', default=False, help='control plot')

parser.add_option('-c', '--channel',action="store",type="string",dest="channel",default="mu")

(options, args) = parser.parse_args()
############################################################

class doFit_wj_and_wlvj:
    def __init__(self, in_channel="mu",in_higgs_sample="ggH600", in_mlvj_signal_region_min=500, in_mlvj_signal_region_max=700, in_mj_min=30, in_mj_max=140, in_mlvj_min=400., in_mlvj_max=1400., fit_model="ErfExp_v1"):
        print "Begin to fit"

        RooAbsPdf.defaultIntegratorConfig().setEpsRel(1e-9) ;
        RooAbsPdf.defaultIntegratorConfig().setEpsAbs(1e-9) ;

        self.channel=in_channel;#el or muon
        self.higgs_sample=in_higgs_sample;

        self.BinWidth_mlvj=40.;
        self.BinWidth_mj=4;
        nbins_mlvj=int((in_mlvj_max-in_mlvj_min)/self.BinWidth_mlvj);
        in_mlvj_max=in_mlvj_min+nbins_mlvj*self.BinWidth_mlvj;
        nbins_mj=int((in_mj_max-in_mj_min)/self.BinWidth_mj);
        in_mj_max=in_mj_min+nbins_mj*self.BinWidth_mj;

        rrv_mass_j  = RooRealVar("rrv_mass_j","mass(j)",(in_mj_min+in_mj_max)/2.,in_mj_min,in_mj_max,"GeV/c^{2}");
        rrv_mass_j.setBins(nbins_mj);
        rrv_mass_lvj= RooRealVar("rrv_mass_lvj","mass(lvj)",(in_mlvj_min+in_mlvj_max)/2.,in_mlvj_min,in_mlvj_max,"GeV/c^{2}");
        rrv_mass_lvj.setBins(nbins_mlvj);

        self.workspace4fit_ = RooWorkspace("workspace4fit_","workspace4fit_");
        getattr(self.workspace4fit_,"import")(rrv_mass_j);
        getattr(self.workspace4fit_,"import")(rrv_mass_lvj);

        #prepare workspace for unbin-Limit
        self.workspace4limit_ = RooWorkspace("workspace4limit_","workspace4limit_");

        self.mj_sideband_lo_min=30;
        self.mj_sideband_lo_max=70;
        self.mj_signal_min=70;
        self.mj_signal_max=100;
        self.mj_sideband_hi_min=100;
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
        rrv_mass_j.setRange("sblo_to_sbhi",self.mj_sideband_lo_min,self.mj_sideband_hi_max);
        rrv_mass_j.setRange("controlsample_fitting_range",40,130);

        self.mlvj_signal_min=in_mlvj_signal_region_min
        self.mlvj_signal_max=in_mlvj_signal_region_max
        rrv_mass_lvj.setRange("signal_region",self.mlvj_signal_min,self.mlvj_signal_max); 

        #prepare the data and mc files
        self.file_Directory="trainingtrees_%s/"%(self.channel);

        self.file_data=("ofile_data.root");#keep blind!!!!
        #self.file_data=("ofile_pseudodata.root");#keep blind!!!!
        #self.file_data=("ofile_pseudodata_with_ggH600.root");#keep blind!!!!
        #self.file_data=("ofile_pseudodata_with_ggH700.root");#keep blind!!!!
        #self.file_data=("ofile_pseudodata_with_ggH800.root");#keep blind!!!!
        #self.file_data=("ofile_pseudodata_with_ggH900.root");#keep blind!!!!
        #self.file_data=("ofile_pseudodata_with_ggH1000.root");#keep blind!!!!
        self.file_pseudodata=("ofile_pseudodata.root");#fake data
        self.file_ggH=("ofile_%s.root"%(self.higgs_sample));
        self.file_WJets_mc=("ofile_WJets.root");
        #self.file_WJets_mc=("ofile_WJets_Herwig.root");
        self.file_VV_mc=("ofile_VV.root");# WW+WZ 
        self.file_TTbar_mc=("ofile_TTbar.root");
        self.file_STop_mc =("ofile_STop.root");#single Top

        #result files: The event number, parameters and error write into a txt file. The dataset and pdfs write into a root file
        self.file_rlt_txt           = "other_hwwlvj_%s_%s.txt"%(self.higgs_sample,self.channel)
        self.file_rlt_root          = "hwwlvj_%s_%s_workspace.root"%(self.higgs_sample,self.channel)
        self.file_datacard_unbin    = "hwwlvj_%s_%s_unbin.txt"%(self.higgs_sample,self.channel)
        self.file_datacard_counting = "hwwlvj_%s_%s_counting.txt"%(self.higgs_sample,self.channel)
        
        self.file_out=open(self.file_rlt_txt,"w");
        self.file_out.write("Welcome:\n");
        self.file_out.close()
        self.file_out=open(self.file_rlt_txt,"a+");

        self.higgs_xs_scale=1.0; #higgs XS scale
        
        self.color_palet={ #color palet
            #'WJets' : style.WJetsColor,
            #'VV'    : style.DibosonsColor,
            #'TTbar' : style.TtbarColor,
            #'STop'  : style.SingleTopColor,
            'data'  : kBlack,
            'WJets' : kRed,
            'VV'    : kAzure+8,
            'TTbar' : kGreen,
            'STop'  : kYellow,
            'Signal': kBlack,
            'Uncertainty' : kBlack,
            'Other_Backgrounds'  : kBlue
        }

        #self.wtagger_lable="tight";#50%
        self.wtagger_lable="media";#75%
        #self.wtagger_lable="loose";#90%
        #self.wtagger_lable="nocut";#nocut
        if self.wtagger_lable=="tight":
            if self.channel=="el":self.wtagger_cut=0.4085;
            if self.channel=="mu":self.wtagger_cut=0.4105;
        if self.wtagger_lable=="media":
            if self.channel=="el":self.wtagger_cut=0.5285;
            if self.channel=="mu":self.wtagger_cut=0.5235;
        if self.wtagger_lable=="loose":
            if self.channel=="el":self.wtagger_cut=0.6425;
            if self.channel=="mu":self.wtagger_cut=0.6275;
        if self.wtagger_lable=="nocut": self.wtagger_cut=10000;
        #el: tight 0.4085; media: 0.5285; loose:0.6425;
        #mu: tight 0.4105; media: 0.5235; loose:0.6275;

        #PU study: 0-11,11-15,15-100
        self.nPV_min=  0;
        self.nPV_max= 100;

        self.file_ttbar_control_txt = "ttbar_control_%s_%s_wtaggercut%s.txt"%(self.higgs_sample,self.channel,self.wtagger_cut);
        self.file_out_ttbar_control=open(self.file_ttbar_control_txt,"w");

        #wtagger_eff reweight between data and mc
        if self.channel=="mu":
            self.rrv_wtagger_eff_reweight=RooRealVar("rrv_wtagger_eff_reweight","rrv_wtagger_eff_reweight",0.956498564381);
            self.rrv_wtagger_eff_reweight.setError(0.0737415002928);
        if self.channel=="el":
            self.rrv_wtagger_eff_reweight=RooRealVar("rrv_wtagger_eff_reweight","rrv_wtagger_eff_reweight",0.929218115583);
            self.rrv_wtagger_eff_reweight.setError(0.0770257798254);
        print "wtagger efficiency correction: %s +/- %s"%(self.rrv_wtagger_eff_reweight.getVal, self.rrv_wtagger_eff_reweight.getError());

        self.model_4_mlvj=fit_model;

        # parameters of data-driven method to get the WJets background event number.
        self.number_WJets_insideband=-1;
        self.datadriven_alpha_WJets_unbin=-1;
        self.datadriven_alpha_WJets_counting=-1;

    ##################### ---------------------------------------------------
    def make_Pdf(self, label, in_model_name, mass_spectrum="_mj"):
        if TString(mass_spectrum).Contains("_mj"): rrv_x = self.workspace4fit_.var("rrv_mass_j"); 
        if TString(mass_spectrum).Contains("_mlvj"): rrv_x = self.workspace4fit_.var("rrv_mass_lvj"); 
        
        if in_model_name == "Voig":
            rrv_mean_voig=RooRealVar("rrv_mean_voig"+label+"_"+self.channel,"rrv_mean_voig"+label+"_"+self.channel,84,78,88);# W mass: 80.385
            rrv_width_voig=RooRealVar("rrv_width_voig"+label+"_"+self.channel,"rrv_width_voig"+label+"_"+self.channel,7.,1,40);
            rrv_sigma_voig=RooRealVar("rrv_sigma_voig"+label+"_"+self.channel,"rrv_sigma_voig"+label+"_"+self.channel,5,0.01,20);
            model_pdf = RooVoigtian("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum, rrv_x,rrv_mean_voig,rrv_width_voig,rrv_sigma_voig);

        if in_model_name == "Voig_v1":
            rrv_mean_voig=RooRealVar("rrv_mean_voig"+label+"_"+self.channel,"rrv_mean_voig"+label+"_"+self.channel,650,550,1200);# Higgs mass 600-1000
            rrv_width_voig=RooRealVar("rrv_width_voig"+label+"_"+self.channel,"rrv_width_voig"+label+"_"+self.channel,60.,10,200);
            rrv_sigma_voig=RooRealVar("rrv_sigma_voig"+label+"_"+self.channel,"rrv_sigma_voig"+label+"_"+self.channel,100,10,200);
            model_pdf = RooVoigtian("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum, rrv_x,rrv_mean_voig,rrv_width_voig,rrv_sigma_voig);
    
        if in_model_name == "BW": # FFT: BreitWigner*CBShape
            rrv_mean_BW=RooRealVar("rrv_mean_BW"+label+"_"+self.channel,"rrv_mean_BW"+label+"_"+self.channel,84,78, 88);
            rrv_width_BW=RooRealVar("rrv_width_BW"+label+"_"+self.channel,"rrv_width_BW"+label+"_"+self.channel,20,1,40);
            model_pdf = RooBreitWigner("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum, rrv_x,rrv_mean_BW,rrv_width_BW);

        if in_model_name == "2Voig":
            rrv_mean_voig=RooRealVar("rrv_mean_voig"+label+"_"+self.channel,"rrv_mean_voig"+label+"_"+self.channel,84,78,88);#W mass 80.385
            rrv_shift_2Voig=RooRealVar("rrv_shift_2Voig"+label+"_"+self.channel,"rrv_shift_2Voig"+label+"_"+self.channel,10.8026)   # Z mass: 91.1876;  shift=91.1876-80.385=10.8026
            rrv_mean_shifted= RooFormulaVar("rrv_mean_voig2"+label+"_"+self.channel,"@0+@1",RooArgList(rrv_mean_voig,rrv_shift_2Voig));
            rrv_width_voig=RooRealVar("rrv_width_voig"+label+"_"+self.channel,"rrv_width_voig"+label+"_"+self.channel,7.,1,30);
            rrv_sigma_voig=RooRealVar("rrv_sigma_voig"+label+"_"+self.channel,"rrv_sigma_voig"+label+"_"+self.channel,5,0.01,20);
            rrv_frac=RooRealVar("rrv_frac"+label+"_"+self.channel,"rrv_frac"+label+"_"+self.channel,1.,0.5,1.);
            model_voig1 = RooVoigtian("model_voig1"+label+"_"+self.channel+mass_spectrum,"model_voig1"+label+"_"+self.channel+mass_spectrum, rrv_x,rrv_mean_voig,rrv_width_voig,rrv_sigma_voig);
            model_voig2 = RooVoigtian("model_voig2"+label+"_"+self.channel+mass_spectrum,"model_voig2"+label+"_"+self.channel+mass_spectrum, rrv_x,rrv_mean_shifted,rrv_width_voig,rrv_sigma_voig);
            model_pdf = RooAddPdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum, RooArgList(model_voig1,model_voig2), RooArgList(rrv_frac));
    
        if in_model_name == "Gaus":
            rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label+"_"+self.channel,"rrv_mean_gaus"+label+"_"+self.channel,84,78,88);
            rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label+"_"+self.channel,"rrv_sigma_gaus"+label+"_"+self.channel,7,1,15);
            model_pdf = RooGaussian("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum, rrv_x,rrv_mean_gaus,rrv_sigma_gaus);

        if in_model_name == "Gaus_v1":
            if label=="_ggH600_signal_region" or label=="_ggH600_sb_lo":
                rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label+"_"+self.channel,"rrv_mean_gaus"+label+"_"+self.channel,580,550,620);
                rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label+"_"+self.channel,"rrv_sigma_gaus"+label+"_"+self.channel,65,40,80);
            if label=="_ggH700_signal_region" or label=="_ggH700_sb_lo":
                rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label+"_"+self.channel,"rrv_mean_gaus"+label+"_"+self.channel,700,650,750);
                rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label+"_"+self.channel,"rrv_sigma_gaus"+label+"_"+self.channel,100,40,150);
            if label=="_ggH800_signal_region" or label=="_ggH800_sb_lo": 
                rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label+"_"+self.channel,"rrv_mean_gaus"+label+"_"+self.channel,800,750,850);
                rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label+"_"+self.channel,"rrv_sigma_gaus"+label+"_"+self.channel,130,120,140);
            if label=="_ggH900_signal_region" or label=="_ggH900_sb_lo": 
                rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label+"_"+self.channel,"rrv_mean_gaus"+label+"_"+self.channel,900,850,900);
                rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label+"_"+self.channel,"rrv_sigma_gaus"+label+"_"+self.channel,160,140,180);
            if label=="_ggH1000_signal_region" or label=="_ggH1000_sb_lo":
                rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label+"_"+self.channel,"rrv_mean_gaus"+label+"_"+self.channel,920,900,1000);
                rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label+"_"+self.channel,"rrv_sigma_gaus"+label+"_"+self.channel,200,100,300);
            model_pdf = RooGaussian("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum, rrv_x,rrv_mean_gaus,rrv_sigma_gaus);
 
        if in_model_name == "BifurGaus_v1":
            if label=="_ggH600_signal_region":
                rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label+"_"+self.channel,"rrv_mean_gaus"+label+"_"+self.channel,600,550,650);
                rrv_sigma1_gaus=RooRealVar("rrv_sigma1_gaus"+label+"_"+self.channel,"rrv_sigma1_gaus"+label+"_"+self.channel,67,40,80);
                rrv_sigma2_gaus=RooRealVar("rrv_sigma2_gaus"+label+"_"+self.channel,"rrv_sigma2_gaus"+label+"_"+self.channel,67,40,80);
            if label=="_ggH700_signal_region":
                rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label+"_"+self.channel,"rrv_mean_gaus"+label+"_"+self.channel,700,650,750);
                rrv_sigma1_gaus=RooRealVar("rrv_sigma1_gaus"+label+"_"+self.channel,"rrv_sigma1_gaus"+label+"_"+self.channel,100,40,150);
                rrv_sigma2_gaus=RooRealVar("rrv_sigma2_gaus"+label+"_"+self.channel,"rrv_sigma2_gaus"+label+"_"+self.channel,100,40,150);
            if label=="_ggH800_signal_region": 
                rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label+"_"+self.channel,"rrv_mean_gaus"+label+"_"+self.channel,800,750,850);
                rrv_sigma1_gaus=RooRealVar("rrv_sigma1_gaus"+label+"_"+self.channel,"rrv_sigma1_gaus"+label+"_"+self.channel,130,120,140);
                rrv_sigma2_gaus=RooRealVar("rrv_sigma2_gaus"+label+"_"+self.channel,"rrv_sigma2_gaus"+label+"_"+self.channel,130,120,140);
            if label=="_ggH900_signal_region": 
                rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label+"_"+self.channel,"rrv_mean_gaus"+label+"_"+self.channel,900,850,900);
                rrv_sigma1_gaus=RooRealVar("rrv_sigma1_gaus"+label+"_"+self.channel,"rrv_sigma1_gaus"+label+"_"+self.channel,160,140,180);
                rrv_sigma2_gaus=RooRealVar("rrv_sigma2_gaus"+label+"_"+self.channel,"rrv_sigma2_gaus"+label+"_"+self.channel,160,140,180);
            if label=="_ggH1000_signal_region":
                rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label+"_"+self.channel,"rrv_mean_gaus"+label+"_"+self.channel,920,900,1000);
                rrv_sigma1_gaus=RooRealVar("rrv_sigma1_gaus"+label+"_"+self.channel,"rrv_sigma1_gaus"+label+"_"+self.channel,200,100,300);
                rrv_sigma2_gaus=RooRealVar("rrv_sigma2_gaus"+label+"_"+self.channel,"rrv_sigma2_gaus"+label+"_"+self.channel,200,100,300);
            model_pdf = RooBifurGauss("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum, rrv_x,rrv_mean_gaus,rrv_sigma1_gaus,rrv_sigma2_gaus);
    
        if in_model_name == "CB":
            rrv_mean_CB=RooRealVar("rrv_mean_CB"+label+"_"+self.channel,"rrv_mean_CB"+label+"_"+self.channel,84,78,88);
            rrv_sigma_CB=RooRealVar("rrv_sigma_CB"+label+"_"+self.channel,"rrv_sigma_CB"+label+"_"+self.channel,7,4,10);
            rrv_alpha_CB=RooRealVar("rrv_alpha_CB"+label+"_"+self.channel,"rrv_alpha_CB"+label+"_"+self.channel,-2,-4,-0.5);
            rrv_n_CB=RooRealVar("rrv_n_CB"+label+"_"+self.channel,"rrv_n_CB"+label+"_"+self.channel,2,0.,4);
            model_pdf = RooCBShape("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum, rrv_x,rrv_mean_CB,rrv_sigma_CB,rrv_alpha_CB,rrv_n_CB);

        if in_model_name == "SCB_v1":
            rrv_mean_SCB=RooRealVar("rrv_mean_SCB"+label+"_"+self.channel,"rrv_mean_SCB"+label+"_"+self.channel,800,550,1000);
            rrv_sigma_SCB=RooRealVar("rrv_sigma_SCB"+label+"_"+self.channel,"rrv_sigma_SCB"+label+"_"+self.channel,70,40,300);
            rrv_alpha1_SCB=RooRealVar("rrv_alpha1_SCB"+label+"_"+self.channel,"rrv_alpha1_SCB"+label+"_"+self.channel,-2,-4,-0.5);
            rrv_alpha2_SCB=RooRealVar("rrv_alpha2_SCB"+label+"_"+self.channel,"rrv_alpha2_SCB"+label+"_"+self.channel,2,0.5,4);
            rrv_n1_SCB=RooRealVar("rrv_n1_SCB"+label+"_"+self.channel,"rrv_n1_SCB"+label+"_"+self.channel,2,0.,4);
            rrv_n2_SCB=RooRealVar("rrv_n2_SCB"+label+"_"+self.channel,"rrv_n2_SCB"+label+"_"+self.channel,2,0.,4);
            frac=RooRealVar("rrv_frac_SSCB"+label+"_"+self.channel,"rrv_frac_SSCB"+label+"_"+self.channel,0.5)
            scb1 = RooCBShape("model_pdf_scb1"+label+"_"+self.channel+mass_spectrum,"model_pdf_scb1"+label+"_"+self.channel+mass_spectrum, rrv_x,rrv_mean_SCB,rrv_sigma_SCB,rrv_alpha1_SCB,rrv_n1_SCB);
            scb2 = RooCBShape("model_pdf_scb2"+label+"_"+self.channel+mass_spectrum,"model_pdf_scb2"+label+"_"+self.channel+mass_spectrum, rrv_x,rrv_mean_SCB,rrv_sigma_SCB,rrv_alpha2_SCB,rrv_n2_SCB);
            model_pdf=RooAddPdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum,RooArgList(scb1,scb2),RooArgList(frac))

        if in_model_name == "CB_v1":
            label_tstring=TString(label);
            if label_tstring.Contains("_ggH600"): 
                rrv_mean_CB=RooRealVar("rrv_mean_CB"+label+"_"+self.channel,"rrv_mean_CB"+label+"_"+self.channel,600,550,650);
                rrv_sigma_CB=RooRealVar("rrv_sigma_CB"+label+"_"+self.channel,"rrv_sigma_CB"+label+"_"+self.channel,67,40,80);
                rrv_alpha_CB=RooRealVar("rrv_alpha_CB"+label+"_"+self.channel,"rrv_alpha_CB"+label+"_"+self.channel,-1,-5,-0.1);
            if label_tstring.Contains("_ggH700"):
                rrv_mean_CB=RooRealVar("rrv_mean_CB"+label+"_"+self.channel,"rrv_mean_CB"+label+"_"+self.channel,700,650,750);
                rrv_sigma_CB=RooRealVar("rrv_sigma_CB"+label+"_"+self.channel,"rrv_sigma_CB"+label+"_"+self.channel,100,40,150);
                rrv_alpha_CB=RooRealVar("rrv_alpha_CB"+label+"_"+self.channel,"rrv_alpha_CB"+label+"_"+self.channel,-1,-3,-0.1);
            if label_tstring.Contains("_ggH800"): 
                rrv_mean_CB=RooRealVar("rrv_mean_CB"+label+"_"+self.channel,"rrv_mean_CB"+label+"_"+self.channel,800,750,850);
                rrv_sigma_CB=RooRealVar("rrv_sigma_CB"+label+"_"+self.channel,"rrv_sigma_CB"+label+"_"+self.channel,130,120,140);
                rrv_alpha_CB=RooRealVar("rrv_alpha_CB"+label+"_"+self.channel,"rrv_alpha_CB"+label+"_"+self.channel,1,0.5,4);
            if label_tstring.Contains("_ggH900"):
                rrv_mean_CB=RooRealVar("rrv_mean_CB"+label+"_"+self.channel,"rrv_mean_CB"+label+"_"+self.channel,900,850,950);
                rrv_sigma_CB=RooRealVar("rrv_sigma_CB"+label+"_"+self.channel,"rrv_sigma_CB"+label+"_"+self.channel,130,100,140);
                rrv_alpha_CB=RooRealVar("rrv_alpha_CB"+label+"_"+self.channel,"rrv_alpha_CB"+label+"_"+self.channel,1,0.5,4);
            if label_tstring.Contains("_ggH1000"): 
                rrv_mean_CB=RooRealVar("rrv_mean_CB"+label+"_"+self.channel,"rrv_mean_CB"+label+"_"+self.channel,920,900,1000);
                rrv_sigma_CB=RooRealVar("rrv_sigma_CB"+label+"_"+self.channel,"rrv_sigma_CB"+label+"_"+self.channel,200,100,300);
                rrv_alpha_CB=RooRealVar("rrv_alpha_CB"+label+"_"+self.channel,"rrv_alpha_CB"+label+"_"+self.channel,1,0.5,4);
            rrv_n_CB=RooRealVar("rrv_n_CB"+label+"_"+self.channel,"rrv_n_CB"+label+"_"+self.channel,6.,2,10);
            model_pdf = RooCBShape("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum, rrv_x,rrv_mean_CB,rrv_sigma_CB,rrv_alpha_CB,rrv_n_CB);
    
        if in_model_name == "CBBW": # FFT: BreitWigner*CBShape
            rrv_mean_CB=RooRealVar("rrv_mean_CB"+label+"_"+self.channel,"rrv_mean_CB"+label+"_"+self.channel,84.0,78,88);
            rrv_sigma_CB=RooRealVar("rrv_sigma_CB"+label+"_"+self.channel,"rrv_sigma_CB"+label+"_"+self.channel,7,4,10);
            rrv_alpha_CB=RooRealVar("rrv_alpha_CB"+label+"_"+self.channel,"rrv_alpha_CB"+label+"_"+self.channel,-2,-4,-1);
            rrv_n_CB=RooRealVar("rrv_n_CB"+label+"_"+self.channel,"rrv_n_CB"+label+"_"+self.channel,0.5,0.,2);
            rrv_mean_BW=RooRealVar("rrv_mean_BW"+label+"_"+self.channel,"rrv_mean_BW"+label+"_"+self.channel,0);
            rrv_width_BW=RooRealVar("rrv_width_BW"+label+"_"+self.channel,"rrv_width_BW"+label+"_"+self.channel,10,5,20);
            cbshape = RooCBShape("cbshape"+label+"_"+self.channel,"cbshape"+label+"_"+self.channel, rrv_x,rrv_mean_CB,rrv_sigma_CB,rrv_alpha_CB,rrv_n_CB);
            bw = RooBreitWigner("bw"+label+"_"+self.channel,"bw"+label+"_"+self.channel, rrv_x,rrv_mean_BW,rrv_width_BW);
            model_pdf = RooFFTConvPdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum, rrv_x, cbshape, bw);

        if in_model_name == "LDGaus": # FFT: Landau*Gaus
            rrv_mean_landau=RooRealVar("rrv_mean_landau"+label+"_"+self.channel,"rrv_mean_landau"+label+"_"+self.channel,84.0,78,88);
            rrv_sigma_landau=RooRealVar("rrv_sigma_landau"+label+"_"+self.channel,"rrv_sigma_landau"+label+"_"+self.channel,7,4,10);
            rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label+"_"+self.channel,"rrv_mean_gaus"+label+"_"+self.channel,0);
            rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label+"_"+self.channel,"rrv_sigma_gaus"+label+"_"+self.channel,16,10,20);
            landau = RooLandau("landau"+label+"_"+self.channel,"landau"+label+"_"+self.channel, rrv_x,rrv_mean_landau,rrv_sigma_landau);
            gaus = RooBreitWigner("gaus"+label+"_"+self.channel,"gaus"+label+"_"+self.channel, rrv_x,rrv_mean_gaus,rrv_sigma_gaus);
            model_pdf = RooFFTConvPdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum, rrv_x, landau, gaus);

        if in_model_name == "Exp" :
            rrv_c_Exp = RooRealVar("rrv_c_Exp"+label+"_"+self.channel,"rrv_c_Exp"+label+"_"+self.channel,-0.05,-0.1,0.);
            model_pdf = ROOT.RooExponential("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum,rrv_x,rrv_c_Exp);

        if in_model_name == "ErfExp" :
            rrv_c_ErfExp = RooRealVar("rrv_c_ErfExp"+label+"_"+self.channel,"rrv_c_ErfExp"+label+"_"+self.channel,-0.05,-0.2,0.);
            rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label+"_"+self.channel,"rrv_offset_ErfExp"+label+"_"+self.channel,60.,30.,120);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label+"_"+self.channel,"rrv_width_ErfExp"+label+"_"+self.channel,30.,10, 60.);
            model_pdf = ROOT.RooErfExpPdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum,rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp);
            #model_pdf = RooGenericPdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum, "TMath::Exp(%s*%s)*(1.+TMath::Erf((%s-%s)/%s))/2."%(rrv_c_ErfExp.GetName(),rrv_x.GetName(), rrv_x.GetName(),rrv_offset_ErfExp.GetName(), rrv_width_ErfExp.GetName()), RooArgList(rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp) )


            ##add a little shift
            #rrv_c_ErfExp = RooRealVar("rrv_c_ErfExp"+label+"_"+self.channel,"rrv_c_ErfExp"+label+"_"+self.channel,-0.05,-0.2,0.);
            #rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label+"_"+self.channel,"rrv_offset_ErfExp"+label+"_"+self.channel,78.,10.,1400.);
            #rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label+"_"+self.channel,"rrv_width_ErfExp"+label+"_"+self.channel,30.,10,100.);
            #rrv_deltax = RooRealVar("rrv_deltax"+label+"_"+self.channel,"rrv_deltax"+label+"_"+self.channel,0,-10,10);
            #rrv_deltax.setConstant(1);
            #rrv_x_shift = RooFormulaVar("rrv_x_shift"+label+"_"+self.channel,"@0+@1",RooArgList(rrv_x, rrv_deltax));
            #model_pdf = ROOT.RooErfExpPdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum,rrv_x_shift,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp);


        if in_model_name == "ErfExp_v1" : #different init-value and range
            rrv_c_ErfExp = RooRealVar("rrv_c_ErfExp"+label+"_"+self.channel,"rrv_c_ErfExp"+label+"_"+self.channel,-0.006,-0.1,0.);
            rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label+"_"+self.channel,"rrv_offset_ErfExp"+label+"_"+self.channel,450.,400.,500.);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label+"_"+self.channel,"rrv_width_ErfExp"+label+"_"+self.channel,50.,10,100.);
            model_pdf = ROOT.RooErfExpPdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum,rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp);
            #model_pdf = RooGenericPdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum, "TMath::Exp(%s*%s)*(1.+TMath::Erf((%s-%s)/%s))/2."%(rrv_c_ErfExp.GetName(),rrv_x.GetName(), rrv_x.GetName(),rrv_offset_ErfExp.GetName(), rrv_width_ErfExp.GetName()), RooArgList(rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp) )

        if in_model_name == "ErfExp_v2" : #different init-value and range
            rrv_c_ErfExp = RooRealVar("rrv_c_ErfExp"+label+"_"+self.channel,"rrv_c_ErfExp"+label+"_"+self.channel,-0.005,-0.1,0.);
            rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label+"_"+self.channel,"rrv_offset_ErfExp"+label+"_"+self.channel,450.,400.,500.);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label+"_"+self.channel,"rrv_width_ErfExp"+label+"_"+self.channel, 50.,10,100.);
            rrv_residue_ErfExp = RooRealVar("rrv_residue_ErfExp"+label+"_"+self.channel,"rrv_residue_ErfExp"+label+"_"+self.channel,0.,0.,1.);
            #model_pdf = ROOT.RooErfExpPdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum,rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp);
            model_pdf = RooGenericPdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum, "(TMath::Exp(%s*%s) + %s)*(1.+TMath::Erf((%s-%s)/%s))/2. "%(rrv_c_ErfExp.GetName(),rrv_x.GetName(), rrv_residue_ErfExp.GetName(), rrv_x.GetName(),rrv_offset_ErfExp.GetName(), rrv_width_ErfExp.GetName()), RooArgList(rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp,rrv_residue_ErfExp) )

        if in_model_name == "ErfExp_v3" : #different init-value and range
            rrv_c_ErfExp = RooRealVar("rrv_c_ErfExp"+label+"_"+self.channel,"rrv_c_ErfExp"+label+"_"+self.channel,-0.005,-0.1,0.);
            rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label+"_"+self.channel,"rrv_offset_ErfExp"+label+"_"+self.channel,450.,400,500.);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label+"_"+self.channel,"rrv_width_ErfExp"+label+"_"+self.channel, 50.,10,100.);
            rrv_residue_ErfExp = RooRealVar("rrv_residue_ErfExp"+label+"_"+self.channel,"rrv_residue_ErfExp"+label+"_"+self.channel,0.,0.,1.);
            rrv_high_ErfExp = RooRealVar("rrv_high_ErfExp"+label+"_"+self.channel,"rrv_high_ErfExp"+label+"_"+self.channel,1.,0.,400);
            rrv_high_ErfExp.setConstant(kTRUE);
            model_pdf = RooGenericPdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum, "(TMath::Exp(%s*%s) + %s)* TMath::Power( ((1+TMath::Erf((%s-%s)/%s))/2.), %s )"%(rrv_c_ErfExp.GetName(),rrv_x.GetName(), rrv_residue_ErfExp.GetName(),rrv_x.GetName(),rrv_offset_ErfExp.GetName(), rrv_width_ErfExp.GetName(), rrv_high_ErfExp.GetName()), RooArgList(rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_high_ErfExp,rrv_width_ErfExp,rrv_residue_ErfExp) )
      
            
        if in_model_name == "ErfExpGaus":
            rrv_c_ErfExp = RooRealVar("rrv_c_ErfExp"+label+"_"+self.channel,"rrv_c_ErfExp"+label+"_"+self.channel,-0.05,-0.4,0.);
            rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label+"_"+self.channel,"rrv_offset_ErfExp"+label+"_"+self.channel,100.,10.,300.);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label+"_"+self.channel,"rrv_width_ErfExp"+label+"_"+self.channel,30.,10,100.);
            rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label+"_"+self.channel,"rrv_mean_gaus"+label+"_"+self.channel,82,78,87);
            rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label+"_"+self.channel,"rrv_sigma_gaus"+label+"_"+self.channel,7,4,10);
            rrv_high = RooRealVar("rrv_high"+label+"_"+self.channel,"rrv_high"+label+"_"+self.channel,0.7,0.,1.);
            erfExp = ROOT.RooErfExpPdf("erfExp"+label+"_"+self.channel,"erfExp"+label+"_"+self.channel,rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp);
            #erfExp = RooGenericPdf("erfExp"+label+"_"+self.channel,"erfExp"+label+"_"+self.channel, "TMath::Exp(%s*%s)*(1.+TMath::Erf((%s-%s)/%s))/2."%(rrv_c_ErfExp.GetName(),rrv_x.GetName(), rrv_x.GetName(),rrv_offset_ErfExp.GetName(), rrv_width_ErfExp.GetName()), RooArgList(rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp) )
            gaus = RooGaussian("gaus"+label+"_"+self.channel,"gaus"+label+"_"+self.channel, rrv_x,rrv_mean_gaus,rrv_sigma_gaus);
            model_pdf =RooAddPdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum,RooArgList(erfExp,gaus),RooArgList(rrv_high))

        if in_model_name == "ErfExpGaus_sp":#offset == mean
            rrv_c_ErfExp = RooRealVar("rrv_c_ErfExp"+label+"_"+self.channel,"rrv_c_ErfExp"+label+"_"+self.channel,-0.05,-0.2,0.);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label+"_"+self.channel,"rrv_width_ErfExp"+label+"_"+self.channel,30.,10,200.);
            rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label+"_"+self.channel,"rrv_mean_gaus"+label+"_"+self.channel,84,78,88);
            rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label+"_"+self.channel,"rrv_sigma_gaus"+label+"_"+self.channel,7,4,10);
            rrv_high = RooRealVar("rrv_high"+label+"_"+self.channel,"rrv_high"+label+"_"+self.channel,0.7,0.,1.);
            erfExp = ROOT.RooErfExpPdf("erfExp"+label+"_"+self.channel,"erfExp"+label+"_"+self.channel,rrv_x,rrv_c_ErfExp,rrv_mean_gaus,rrv_width_ErfExp);
            gaus = RooGaussian("gaus"+label+"_"+self.channel,"gaus"+label+"_"+self.channel, rrv_x,rrv_mean_gaus,rrv_sigma_gaus);
            model_pdf =RooAddPdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum,RooArgList(erfExp,gaus),RooArgList(rrv_high))

        if in_model_name == "ErfExpGaus_v0":
            rrv_c_ErfExp = RooRealVar("rrv_c_ErfExp"+label+"_"+self.channel,"rrv_c_ErfExp"+label+"_"+self.channel,-0.05,-0.2,0.);
            rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label+"_"+self.channel,"rrv_offset_ErfExp"+label+"_"+self.channel,100.,10.,140.);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label+"_"+self.channel,"rrv_width_ErfExp"+label+"_"+self.channel,30.,10,100.);
            rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label+"_"+self.channel,"rrv_mean_gaus"+label+"_"+self.channel,84,78,88);
            rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label+"_"+self.channel,"rrv_sigma_gaus"+label+"_"+self.channel,7,4,10);
            rrv_high = RooRealVar("rrv_high"+label+"_"+self.channel,"rrv_high"+label+"_"+self.channel,0.7,0.,1.);
            erfExp = ROOT.RooErfExpPdf("erfExp"+label+"_"+self.channel,"erfExp"+label+"_"+self.channel,rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp);
            #erfExp = RooGenericPdf("erfExp"+label+"_"+self.channel,"erfExp"+label+"_"+self.channel, "TMath::Exp(%s*%s)*(1.+TMath::Erf((%s-%s)/%s))/2."%(rrv_c_ErfExp.GetName(),rrv_x.GetName(), rrv_x.GetName(),rrv_offset_ErfExp.GetName(), rrv_width_ErfExp.GetName()), RooArgList(rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp) )
            gaus = RooGaussian("gaus"+label+"_"+self.channel,"gaus"+label+"_"+self.channel, rrv_x,rrv_mean_gaus,rrv_sigma_gaus);
            model_pdf =RooAddPdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum,RooArgList(erfExp,gaus),RooArgList(rrv_high))
    
        if in_model_name == "ErfExpGaus_v1":
            rrv_c_ErfExp = RooRealVar("rrv_c_ErfExp"+label+"_"+self.channel,"rrv_c_ErfExp"+label+"_"+self.channel,-0.007,-0.1,0.);
            rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label+"_"+self.channel,"rrv_offset_ErfExp"+label+"_"+self.channel,800.,10.,1400.);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label+"_"+self.channel,"rrv_width_ErfExp"+label+"_"+self.channel,24.,10,150.);
            rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label+"_"+self.channel,"rrv_mean_gaus"+label+"_"+self.channel,700,500,1200);
            rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label+"_"+self.channel,"rrv_sigma_gaus"+label+"_"+self.channel,150,10,300);
            rrv_high = RooRealVar("rrv_high"+label+"_"+self.channel,"rrv_high"+label+"_"+self.channel,0.1,0.,1.);
            erfExp = ROOT.RooErfExpPdf("erfExp"+label+"_"+self.channel,"erfExp"+label+"_"+self.channel,rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp);
            #erfExp = RooGenericPdf("erfExp"+label+"_"+self.channel,"erfExp"+label+"_"+self.channel, "TMath::Exp(%s*%s)*(1.+TMath::Erf((%s-%s)/%s))/2."%(rrv_c_ErfExp.GetName(),rrv_x.GetName(), rrv_x.GetName(),rrv_offset_ErfExp.GetName(), rrv_width_ErfExp.GetName()), RooArgList(rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp) )
            gaus = RooGaussian("gaus"+label+"_"+self.channel,"gaus"+label+"_"+self.channel, rrv_x,rrv_mean_gaus,rrv_sigma_gaus);
            model_pdf =RooAddPdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum,RooArgList(erfExp,gaus),RooArgList(rrv_high))
        if in_model_name == "ErfExpGaus_sp_v1":
            rrv_c_ErfExp = RooRealVar("rrv_c_ErfExp"+label+"_"+self.channel,"rrv_c_ErfExp"+label+"_"+self.channel,-0.007,-0.1,0.);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label+"_"+self.channel,"rrv_width_ErfExp"+label+"_"+self.channel,24.,10,150.);
            rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label+"_"+self.channel,"rrv_mean_gaus"+label+"_"+self.channel,900,860,1200);
            rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label+"_"+self.channel,"rrv_sigma_gaus"+label+"_"+self.channel,150,10,300);
            rrv_high = RooRealVar("rrv_high"+label+"_"+self.channel,"rrv_high"+label+"_"+self.channel,0.1,0.,1.);
            #erfExp = ROOT.RooErfExpPdf("erfExp"+label+"_"+self.channel,"erfExp"+label+"_"+self.channel,rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp);
            erfExp = ROOT.RooErfExpPdf("erfExp"+label+"_"+self.channel,"erfExp"+label+"_"+self.channel,rrv_x,rrv_c_ErfExp,rrv_mean_gaus,rrv_width_ErfExp);
            gaus = RooGaussian("gaus"+label+"_"+self.channel,"gaus"+label+"_"+self.channel, rrv_x,rrv_mean_gaus,rrv_sigma_gaus);
            model_pdf =RooAddPdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum,RooArgList(erfExp,gaus),RooArgList(rrv_high))
    
        if in_model_name == "ErfExpGaus_v2":
            rrv_c_ErfExp = RooRealVar("rrv_c_ErfExp"+label+"_"+self.channel,"rrv_c_ErfExp"+label+"_"+self.channel,-0.05,-10.,0.);
            rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label+"_"+self.channel,"rrv_offset_ErfExp"+label+"_"+self.channel,100.,10.,140.);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label+"_"+self.channel,"rrv_width_ErfExp"+label+"_"+self.channel,30.,10,100.);
            rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label+"_"+self.channel,"rrv_mean_gaus"+label+"_"+self.channel,84,78,88);
            rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label+"_"+self.channel,"rrv_sigma_gaus"+label+"_"+self.channel,7,4,10);
            rrv_high = RooRealVar("rrv_high"+label+"_"+self.channel,"rrv_high"+label+"_"+self.channel,200.,0.,1000.);
            model_pdf = ROOT.RooErfExp_Gaus_Pdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum, rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp,rrv_mean_gaus,rrv_sigma_gaus,rrv_high );
    
        if in_model_name == "ErfExp2Gaus":
            rrv_c_ErfExp = RooRealVar("rrv_c_ErfExp"+label+"_"+self.channel,"rrv_c_ErfExp"+label+"_"+self.channel,-0.05,-0.2,0.);
            rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label+"_"+self.channel,"rrv_offset_ErfExp"+label+"_"+self.channel,100.,10.,140.);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label+"_"+self.channel,"rrv_width_ErfExp"+label+"_"+self.channel,30.,10,100.);
            rrv_mean1_gaus=RooRealVar("rrv_mean1_gaus"+label+"_"+self.channel,"rrv_mean1_gaus"+label+"_"+self.channel,84,78,88);
            rrv_mean2_gaus=RooRealVar("rrv_mean2_gaus"+label+"_"+self.channel,"rrv_mean2_gaus"+label+"_"+self.channel,180,170,190);
            rrv_sigma1_gaus=RooRealVar("rrv_sigma1_gaus"+label+"_"+self.channel,"rrv_sigma1_gaus"+label+"_"+self.channel,7,4,10);
            rrv_sigma2_gaus=RooRealVar("rrv_sigma2_gaus"+label+"_"+self.channel,"rrv_sigma2_gaus"+label+"_"+self.channel,10,7,15);
            rrv_high1 = RooRealVar("rrv_high1"+label+"_"+self.channel,"rrv_high1"+label+"_"+self.channel,0.6,0.,1.);
            rrv_high2 = RooRealVar("rrv_high2"+label+"_"+self.channel,"rrv_high2"+label+"_"+self.channel,0.4,0.,1.);
            erfExp = ROOT.RooErfExpPdf("erfExp"+label+"_"+self.channel,"erfExp"+label+"_"+self.channel,rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp);
            #erfExp = RooGenericPdf("erfExp"+label+"_"+self.channel,"erfExp"+label+"_"+self.channel, "TMath::Exp(%s*%s)*(1.+TMath::Erf((%s-%s)/%s))/2."%(rrv_c_ErfExp.GetName(),rrv_x.GetName(), rrv_x.GetName(),rrv_offset_ErfExp.GetName(), rrv_width_ErfExp.GetName()), RooArgList(rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp) )
            gaus1 = RooGaussian("gaus1"+label+"_"+self.channel,"gaus1"+label+"_"+self.channel, rrv_x,rrv_mean1_gaus,rrv_sigma1_gaus);
            gaus2 = RooGaussian("gaus2"+label+"_"+self.channel,"gaus2"+label+"_"+self.channel, rrv_x,rrv_mean2_gaus,rrv_sigma2_gaus);
            model_pdf =RooAddPdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum,RooArgList(erfExp,gaus1,gaus2),RooArgList(rrv_high1,rrv_high2))
    
        if in_model_name == "ErfExpVoigGaus":
            rrv_c_ErfExp = RooRealVar("rrv_c_ErfExp"+label+"_"+self.channel,"rrv_c_ErfExp"+label+"_"+self.channel,-0.1,-10.,0.);
            rrv_offset_ErfExp = RooRealVar("rrv_offset_ErfExp"+label+"_"+self.channel,"rrv_offset_ErfExp"+label+"_"+self.channel,100.,10.,140.);
            rrv_width_ErfExp = RooRealVar("rrv_width_ErfExp"+label+"_"+self.channel,"rrv_width_ErfExp"+label+"_"+self.channel,30.,10,100.);
            rrv_mean_voig=RooRealVar("rrv_mean_voig"+label+"_"+self.channel,"rrv_mean_voig"+label+"_"+self.channel,84,78,88);
            rrv_width_voig=RooRealVar("rrv_width_voig"+label+"_"+self.channel,"rrv_width_voig"+label+"_"+self.channel,7,1,20);
            rrv_sigma_voig=RooRealVar("rrv_sigma_voig"+label+"_"+self.channel,"rrv_sigma_voig"+label+"_"+self.channel,5,1,100);
            rrv_high1 = RooRealVar("rrv_high1"+label+"_"+self.channel,"rrv_high1"+label+"_"+self.channel,1,0.,200.);
            rrv_mean_gaus=RooRealVar("rrv_mean_gaus"+label+"_"+self.channel,"rrv_mean_gaus"+label+"_"+self.channel,174)#,160,187);
            rrv_sigma_gaus=RooRealVar("rrv_sigma_gaus"+label+"_"+self.channel,"rrv_sigma_gaus"+label+"_"+self.channel,20)#,0.1,100);
            rrv_high2 = RooRealVar("rrv_high2"+label+"_"+self.channel,"rrv_high2"+label+"_"+self.channel,0.)#,0.,0.);
            model_pdf = ROOT.RooErfExp_Voig_Gaus_Pdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum, rrv_x,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp,rrv_mean_voig,rrv_width_voig,rrv_sigma_voig,rrv_high1,rrv_mean_gaus,rrv_sigma_gaus,rrv_high2 );

        if in_model_name == "EXO2011414":
            rrv_p0=RooRealVar("rrv_p0_EXO2011414"+label+"_"+self.channel,"rrv_p0_EXO2011414"+label+"_"+self.channel,-500,-1000,0);
            rrv_p1=RooRealVar("rrv_p1_EXO2011414"+label+"_"+self.channel,"rrv_p1_EXO2011414"+label+"_"+self.channel,200,0,1000);
            rrv_p2=RooRealVar("rrv_p2_EXO2011414"+label+"_"+self.channel,"rrv_p2_EXO2011414"+label+"_"+self.channel,50,0,500);
            model_pdf=RooEXO2011414Pdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum,rrv_x,rrv_p0,rrv_p1,rrv_p2);
            #model_pdf=RooGenericPdf("RooEXO2011414Pdf"+label+"_"+self.channel+mass_spectrum,"RooEXO2011414Pdf"+label+"_"+self.channel+mass_spectrum,()%s()RooArgList(rrv_x,rrv_p0,rrv_p1,rrv_p2));

        if in_model_name == "Keys":
            rdataset=self.workspace4fit_.data("rdataset_%s_signal_region_mlvj"%(self.higgs_sample))
            model_pdf = RooKeysPdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum, rrv_x,rdataset);

        if in_model_name == "Seymour_0":
            rrv_mean_Seymour = RooRealVar("rrv_mean_Seymour"+label+"_"+self.channel,"rrv_mean_Seymour"+label+"_"+self.channel,800,400,1200);
            rrv_sigma_Seymour= RooRealVar("rrv_sigma_Seymour"+label+"_"+self.channel,"rrv_sigma_Seymour"+label+"_"+self.channel,100,70,200);
            model_pdf = RooGenericPdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum, "TMath::Power(%s/%s,4)/( TMath::Power(%s*%s-%s*%s,2)+TMath::Power(%s*%s*%s/%s,2) )"%(rrv_x.GetName(), rrv_mean_Seymour.GetName(), rrv_mean_Seymour.GetName(), rrv_mean_Seymour.GetName(),rrv_x.GetName(),rrv_x.GetName(),rrv_sigma_Seymour.GetName(), rrv_mean_Seymour.GetName(),rrv_mean_Seymour.GetName(), rrv_x.GetName() ), RooArgList(rrv_x,rrv_mean_Seymour,rrv_sigma_Seymour) );

        if in_model_name == "Seymour_1":
            rrv_mean_Seymour = RooRealVar("rrv_mean_Seymour"+label+"_"+self.channel,"rrv_mean_Seymour"+label+"_"+self.channel,800,400,1200);
            rrv_sigma_Seymour= RooRealVar("rrv_sigma_Seymour"+label+"_"+self.channel,"rrv_sigma_Seymour"+label+"_"+self.channel, 70,30,200);
            #model_pdf = RooGenericPdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum, "TMath::Power(%s/%s,4)/( TMath::Power(%s*%s-%s*%s,2)+TMath::Power(%s*%s*%s/%s,2) )"%(rrv_x.GetName(), rrv_mean_Seymour.GetName(), rrv_mean_Seymour.GetName(), rrv_mean_Seymour.GetName(),rrv_x.GetName(),rrv_x.GetName(),rrv_sigma_Seymour.GetName(), rrv_mean_Seymour.GetName(),rrv_mean_Seymour.GetName(), rrv_x.GetName() ), RooArgList(rrv_x,rrv_mean_Seymour,rrv_sigma_Seymour) );
            seymour = RooGenericPdf("seymour"+label+"_"+self.channel+mass_spectrum,"seymour"+label+"_"+self.channel+mass_spectrum, "TMath::Power(%s/%s,4)/( TMath::Power(%s*%s-%s*%s,2)+TMath::Power(%s*%s*%s/%s,2) )"%(rrv_x.GetName(), rrv_mean_Seymour.GetName(), rrv_mean_Seymour.GetName(), rrv_mean_Seymour.GetName(),rrv_x.GetName(),rrv_x.GetName(),rrv_sigma_Seymour.GetName(), rrv_mean_Seymour.GetName(),rrv_mean_Seymour.GetName(), rrv_x.GetName() ), RooArgList(rrv_x,rrv_mean_Seymour,rrv_sigma_Seymour) );

            rrv_mean_cb = RooRealVar("rrv_mean_cb"+label+"_"+self.channel,"rrv_mean_cb"+label+"_"+self.channel,0);
            rrv_width_cb = RooRealVar("rrv_width_cb"+label+"_"+self.channel,"rrv_width_cb"+label+"_"+self.channel,60,10,200);
            #rrv_alpha_cb = RooRealVar("rrv_alpha_cb"+label+"_"+self.channel,"rrv_alpha_cb"+label+"_"+self.channel,3,1,5);
            rrv_alpha_cb = RooRealVar("rrv_alpha_cb"+label+"_"+self.channel,"rrv_alpha_cb"+label+"_"+self.channel,-9,-20,-5);
            rrv_n_cb = RooRealVar("rrv_n_cb"+label+"_"+self.channel,"rrv_n_cb"+label+"_"+self.channel,3,1,5);
            #gaus = RooGaussian("gaus"+label+"_"+self.channel,"gaus"+label+"_"+self.channel, rrv_x,rrv_mean_cb,rrv_width_cb);
            cbshape = RooCBShape("cbshape"+label+"_"+self.channel,"cbshape"+label+"_"+self.channel, rrv_x,rrv_mean_cb,rrv_width_cb,rrv_alpha_cb,rrv_n_cb);

            model_pdf = RooFFTConvPdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum, rrv_x, seymour, cbshape);
        if in_model_name == "Seymour":
            label_tstring=TString(label);
            if label_tstring.Contains("_ggH600"): 
                rrv_mean_Seymour = RooRealVar("rrv_mean_Seymour"+label+"_"+self.channel,"rrv_mean_Seymour"+label+"_"+self.channel,600,550,650 );
                rrv_width_novo = RooRealVar("rrv_width_novo"+label+"_"+self.channel,"rrv_width_novo"+label+"_"+self.channel, 60,40, 80);
            if label_tstring.Contains("_ggH700"):
                rrv_mean_Seymour = RooRealVar("rrv_mean_Seymour"+label+"_"+self.channel,"rrv_mean_Seymour"+label+"_"+self.channel,700,650,750 );
                rrv_width_novo = RooRealVar("rrv_width_novo"+label+"_"+self.channel,"rrv_width_novo"+label+"_"+self.channel, 95,80,120);
            if label_tstring.Contains("_ggH800"): 
                rrv_mean_Seymour = RooRealVar("rrv_mean_Seymour"+label+"_"+self.channel,"rrv_mean_Seymour"+label+"_"+self.channel,800,750,850 );
                rrv_width_novo = RooRealVar("rrv_width_novo"+label+"_"+self.channel,"rrv_width_novo"+label+"_"+self.channel,130,110,150);
            if label_tstring.Contains("_ggH900"):
                rrv_mean_Seymour = RooRealVar("rrv_mean_Seymour"+label+"_"+self.channel,"rrv_mean_Seymour"+label+"_"+self.channel,900,850,950 );
                rrv_width_novo = RooRealVar("rrv_width_novo"+label+"_"+self.channel,"rrv_width_novo"+label+"_"+self.channel,150,120,180);
            if label_tstring.Contains("_ggH1000"): 
                rrv_mean_Seymour = RooRealVar("rrv_mean_Seymour"+label+"_"+self.channel,"rrv_mean_Seymour"+label+"_"+self.channel,1000,900,1150 );
                rrv_width_novo = RooRealVar("rrv_width_novo"+label+"_"+self.channel,"rrv_width_novo"+label+"_"+self.channel,200,150,250);

            rrv_sigma_Seymour= RooRealVar("rrv_sigma_Seymour"+label+"_"+self.channel,"rrv_sigma_Seymour"+label+"_"+self.channel, 30, 1, 50);
            rrv_alpha_novo = RooRealVar("rrv_alpha_novo"+label+"_"+self.channel,"rrv_alpha_novo"+label+"_"+self.channel,1e-1,1e-4,3);

            rrv_mean_novo = RooRealVar("rrv_mean_novo"+label+"_"+self.channel,"rrv_mean_novo"+label+"_"+self.channel,0);

            seymour = RooGenericPdf("seymour"+label+"_"+self.channel+mass_spectrum,"seymour"+label+"_"+self.channel+mass_spectrum, "TMath::Power(%s/%s,4)/( TMath::Power(%s*%s-%s*%s,2)+TMath::Power(%s*%s*%s/%s,2) )"%(rrv_x.GetName(), rrv_mean_Seymour.GetName(), rrv_mean_Seymour.GetName(), rrv_mean_Seymour.GetName(),rrv_x.GetName(),rrv_x.GetName(),rrv_sigma_Seymour.GetName(), rrv_mean_Seymour.GetName(),rrv_mean_Seymour.GetName(), rrv_x.GetName() ), RooArgList(rrv_x,rrv_mean_Seymour,rrv_sigma_Seymour) );
            novo = RooNovosibirsk("novo"+label+"_"+self.channel,"novo"+label+"_"+self.channel, rrv_x,rrv_mean_novo,rrv_width_novo,rrv_alpha_novo);

            model_pdf = RooFFTConvPdf("model_pdf"+label+"_"+self.channel+mass_spectrum,"model_pdf"+label+"_"+self.channel+mass_spectrum, rrv_x, seymour, novo);

        getattr(self.workspace4fit_,"import")(model_pdf)
        return self.workspace4fit_.pdf("model_pdf"+label+"_"+self.channel+mass_spectrum)

    ##################### ---------------------------------------------------
    def make_Model(self, label, in_model_name, mass_spectrum="_mj"):
        rrv_number = RooRealVar("rrv_number"+label+"_"+self.channel+mass_spectrum,"rrv_number"+label+"_"+self.channel+mass_spectrum,500,0.,1e7);
        model_pdf  = self.make_Pdf(label,in_model_name,mass_spectrum)
        model_pdf.Print();
        model = RooExtendPdf("model"+label+"_"+self.channel+mass_spectrum,"model"+label+"_"+self.channel+mass_spectrum, model_pdf, rrv_number );
        getattr(self.workspace4fit_,"import")(rrv_number)
        getattr(self.workspace4fit_,"import")(model)
        model.Print();
        print "model"+label+"_"+self.channel+mass_spectrum 
        self.workspace4fit_.pdf("model"+label+"_"+self.channel+mass_spectrum).Print();
        return self.workspace4fit_.pdf("model"+label+"_"+self.channel+mass_spectrum)
    
    ##################### ---------------------------------------------------
    def get_mj_Model(self,label):
        return self.workspace4fit_.pdf("model"+label+"_"+self.channel+"_mj")

    ##################### ---------------------------------------------------
    def get_General_mj_Model(self, label):
        rdataset_General_mj=self.workspace4fit_.data("rdataset%s_%s_mj"%(label,self.channel))
        model_General=self.get_mj_Model(label);
        #rdataset_General_mj.Print()
        #model_General.Print()
        parameters_General=model_General.getParameters(rdataset_General_mj);
        par=parameters_General.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            param.setConstant(kTRUE);
            #param.Print();
            param=par.Next()
        return self.workspace4fit_.pdf("model%s_%s_mj"%(label,self.channel))

    ###################### ---------------------------------------------------
    def get_TTbar_mj_Model(self):
        return self.get_General_mj_Model("_TTbar");
    ###################### ---------------------------------------------------
    def get_STop_mj_Model(self):
        return self.get_General_mj_Model("_STop");
    ###################### ---------------------------------------------------
    def get_VV_mj_Model(self):
        return self.get_General_mj_Model("_VV");

    ##################### ---------------------------------------------------
    def get_WJets_mj_Model(self):
        rdataset_WJets_mj=self.workspace4fit_.data("rdataset_WJets_%s_mj"%(self.channel))
        model_WJets=self.get_mj_Model("_WJets");
        parameters_WJets=model_WJets.getParameters(rdataset_WJets_mj);
        par=parameters_WJets.createIterator(); par.Reset();
        param=par.Next()
        while (param):
            paraName=TString(param.GetName());
            #if not ( paraName.Contains("rrv_c_ErfExp_WJets") or paraName.Contains("rrv_offset_ErfExp_WJets") or paraName.Contains("rrv_number_WJets")) :param.setConstant(kTRUE);
            if not ( paraName.Contains("rrv_c_ErfExp_WJets") or paraName.Contains("rrv_number_WJets") or paraName.Contains("rrv_deltax")) :param.setConstant(kTRUE);
            else: param.setConstant(0);
            #if not ( paraName.Contains("rrv_width_ErfExp_WJets") or paraName.Contains("rrv_c_ErfExp_WJets") or paraName.Contains("rrv_number_WJets")) :param.setConstant(kTRUE);
            param=par.Next()
        return self.workspace4fit_.pdf("model_WJets_%s_mj"%(self.channel))

    ##################### ---------------------------------------------------
    def get_mlvj_Model(self,label, mlvj_region):
        return self.workspace4fit_.pdf("model"+label+mlvj_region+"_"+self.channel+"_mlvj");

    ##################### ---------------------------------------------------
    def get_General_mlvj_Model(self, label, mlvj_region="_signal_region"):
        rdataset_General_mlvj=self.workspace4fit_.data("rdataset%s%s_%s_mlvj"%(label, mlvj_region,self.channel))
        model_General=self.get_mlvj_Model(label,mlvj_region);
        model_General.Print()
        parameters_General=model_General.getParameters(rdataset_General_mlvj);
        par=parameters_General.createIterator(); par.Reset();
        param=par.Next()
        while (param):
            param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
        return self.get_mlvj_Model(label,mlvj_region);

    ##################### ---------------------------------------------------
    def get_TTbar_mlvj_Model(self, mlvj_region="_signal_region"):
        return self.get_General_mlvj_Model("_TTbar",mlvj_region);
    ##################### ---------------------------------------------------
    def get_STop_mlvj_Model(self, mlvj_region="_signal_region"):
        return self.get_General_mlvj_Model("_STop",mlvj_region);

    ##################### ---------------------------------------------------
    def get_ggH_mlvj_Model(self, mlvj_region="_signal_region"):
        return self.get_General_mlvj_Model("_%s"%(self.higgs_sample),mlvj_region);

    ##################### ---------------------------------------------------
    def get_VV_mlvj_Model(self, mlvj_region="_signal_region"):
        return self.get_General_mlvj_Model("_VV",mlvj_region);

    ##################### ---------------------------------------------------
    def get_WJets_mlvj_Model(self, mlvj_region="_signal_region"):
        print "get_WJets_mlvj_Model"
        rdataset_WJets_mlvj=self.workspace4fit_.data("rdataset_WJets%s_mlvj"%(mlvj_region))
        model_WJets=self.get_mlvj_Model("_WJets",mlvj_region);
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
                if self.workspace4fit_.var("rrv_number_WJets_in_mj%s_from_fitting"%(mlvj_region)):
                    self.workspace4fit_.var("rrv_number_WJets_in_mj%s_from_fitting"%(mlvj_region)).Print()
                    param.setVal( self.workspace4fit_.var("rrv_number_WJets_in_mj%s_from_fitting"%(mlvj_region)).getVal() )
                if mlvj_region=="_signal_region": param.setConstant(kTRUE);
            param.Print();
            param=par.Next()
	    return self.get_mlvj_Model("_WJets",mlvj_region);

    ##################### ---------------------------------------------------
    def fix_Model(self, label, mlvj_region="_signal_region",mass_spectrum="_mlvj"):
        rdataset=self.workspace4fit_.data("rdataset%s%s_%s%s"%(label,mlvj_region,self.channel,mass_spectrum))
        model=self.get_mlvj_Model(label,mlvj_region);
        parameters=model.getParameters(rdataset);
        par=parameters.createIterator(); par.Reset();
        param=par.Next()
        while (param):
            param.setConstant(kTRUE);
            param=par.Next()

    ##################### ---------------------------------------------------
    def fix_Pdf(self,model_pdf,argset_notparameter):
        model_pdf.Print()
        parameters=model_pdf.getParameters(argset_notparameter);
        par=parameters.createIterator(); par.Reset();
        param=par.Next()
        while (param):
            param.setConstant(kTRUE);
            param.Print();
            param=par.Next()

    ##################### ---------------------------------------------------
    def get_WJets_mlvj_correction_sb_lo_to_signal_region(self):#exo-vv method: extract M_lvj shape of signal_region from sb_lo
        print "get_WJets_mlvj_correction_sb_lo_to_signal_region"
        rrv_x = self.workspace4fit_.var("rrv_mass_lvj"); 
        rdataset_WJets_sb_lo_mlvj=self.workspace4fit_.data("rdataset_WJets_sb_lo_%s_mlvj"%(self.channel))
        rdataset_WJets_signal_region_mlvj=self.workspace4fit_.data("rdataset_WJets_signal_region_%s_mlvj"%(self.channel))
        model_sb_lo_WJets         = self.workspace4fit_.pdf("model_pdf_WJets_sb_lo_%s_mlvj"%(self.channel));
        model_signal_region_WJets = self.workspace4fit_.pdf("model_pdf_WJets_signal_region_%s_mlvj"%(self.channel));

        mplot = rrv_x.frame(RooFit.Title("correlation_pdf"));
        mplot2 = rrv_x.frame(RooFit.Title("correction"));
        mplot2.GetYaxis().SetRangeUser(1e-2,1.5);
        if self.model_4_mlvj=="Exp":
            mplot2.GetYaxis().SetRangeUser(1e-2,2.5);
        mplot2.GetYaxis().SetTitle("alpha");

        if self.model_4_mlvj=="ErfExp_v1":
            #correct_factor_pdf = RooAlpha("correct_factor_pdf","correct_factor_pdf",rrv_x,self.workspace4fit_.function("Deco_WJets_signal_region_%s_mlvj_eigLin_0"%(self.channel)),self.workspace4fit_.function("Deco_WJets_signal_region_%s_mlvj_eigLin_2"%(self.channel)),self.workspace4fit_.function("Deco_WJets_signal_region_%s_mlvj_eigLin_3"%(self.channel)),self.workspace4fit_.function("Deco_WJets_sb_lo_%s_mlvj_eigLin_0"%(self.channel)),self.workspace4fit_.function("Deco_WJets_sb_lo_%s_mlvj_eigLin_2"%(self.channel)),self.workspace4fit_.function("Deco_WJets_sb_lo_%s_mlvj_eigLin_3"%(channel)),rrv_x.getMin(),rrv_x.getMax());
            correct_factor_pdf = RooAlpha("correct_factor_pdf","correct_factor_pdf",
                    rrv_x,
                    self.workspace4fit_.function("Deco_WJets_signal_region_%s_mlvj_eigLin_0"%(self.channel)),
                    self.workspace4fit_.function("Deco_WJets_signal_region_%s_mlvj_eigLin_2"%(self.channel)),
                    self.workspace4fit_.function("Deco_WJets_signal_region_%s_mlvj_eigLin_3"%(self.channel)),
                    self.workspace4fit_.function("Deco_WJets_sb_lo_%s_mlvj_eigLin_0"%(self.channel)),
                    self.workspace4fit_.function("Deco_WJets_sb_lo_%s_mlvj_eigLin_2"%(self.channel)),
                    self.workspace4fit_.function("Deco_WJets_sb_lo_%s_mlvj_eigLin_3"%(self.channel)),
                    rrv_x.getMin(),
                    rrv_x.getMax());
            getattr(self.workspace4fit_,"import")(correct_factor_pdf);
            correct_factor_pdf.plotOn(mplot, RooFit.LineColor(kBlack) );
            model_sb_lo_WJets.plotOn(mplot);
            model_signal_region_WJets.plotOn(mplot, RooFit.LineColor(kRed) );

            #correct_factor_pdf.Print("v");
            correct_factor_pdf.getParameters(rdataset_WJets_sb_lo_mlvj).Print("v");
            #raw_input("ENTER");

            paras=RooArgList();
            paras.add(self.workspace4fit_.var("Deco_WJets_signal_region_%s_mlvj_eig0"%(self.channel)));
            paras.add(self.workspace4fit_.var("Deco_WJets_signal_region_%s_mlvj_eig1"%(self.channel)));
            paras.add(self.workspace4fit_.var("Deco_WJets_signal_region_%s_mlvj_eig2"%(self.channel)));
            paras.add(self.workspace4fit_.var("Deco_WJets_signal_region_%s_mlvj_eig3"%(self.channel)));
            paras.add(self.workspace4fit_.var("Deco_WJets_sb_lo_%s_mlvj_eig0"%(self.channel)));
            paras.add(self.workspace4fit_.var("Deco_WJets_sb_lo_%s_mlvj_eig1"%(self.channel)));
            paras.add(self.workspace4fit_.var("Deco_WJets_sb_lo_%s_mlvj_eig2"%(self.channel)));
            paras.add(self.workspace4fit_.var("Deco_WJets_sb_lo_%s_mlvj_eig3"%(self.channel)));

        if self.model_4_mlvj=="Exp":
            delta_c=RooFormulaVar("delta_c", "@0-@1",RooArgList( self.workspace4fit_.function("Deco_WJets_signal_region_%s_mlvj_eigLin_0"%(self.channel)), self.workspace4fit_.function("Deco_WJets_sb_lo_%s_mlvj_eigLin_0"%(self.channel))));
            c_sideband=self.workspace4fit_.var("rrv_c_Exp_WJets_sb_lo_%s_from_fitting"%(self.channel));
            c_signal_region=RooFormulaVar("c_signal_region", "@0+@1",RooArgList(delta_c, c_sideband)) ;

            correct_factor_pdf = RooExponential("correct_factor_pdf","correct_factor_pdf",rrv_x,delta_c);

            getattr(self.workspace4fit_,"import")(correct_factor_pdf);
            correct_factor_pdf.plotOn(mplot, RooFit.LineColor(kBlack) );
            model_sb_lo_WJets.plotOn(mplot);
            model_signal_region_WJets.plotOn( mplot, RooFit.LineColor(kRed) );

            #correct_factor_pdf.Print("v");
            correct_factor_pdf.getParameters(rdataset_WJets_sb_lo_mlvj).Print("v");
            #raw_input("ENTER");

            paras=RooArgList();
            paras.add(self.workspace4fit_.var("Deco_WJets_signal_region_%s_mlvj_eig0"%(self.channel)));
            paras.add(self.workspace4fit_.var("Deco_WJets_signal_region_%s_mlvj_eig1"%(self.channel)));
            paras.add(self.workspace4fit_.var("Deco_WJets_sb_lo_%s_mlvj_eig0"%(self.channel)));
            paras.add(self.workspace4fit_.var("Deco_WJets_sb_lo_%s_mlvj_eig1"%(self.channel)));

        signal_number=self.workspace4fit_.var("rrv_number_WJets_signal_region_%s_mlvj"%(self.channel)).getVal();
        sb_number    =self.workspace4fit_.var("rrv_number_WJets_sb_lo_%s_mlvj"%(self.channel)).getVal();
        scale_signal_sb=signal_number/sb_number;
        scale_signal_sb_error=TMath.Sqrt(1./signal_number+1./sb_number)*scale_signal_sb;
        rrv_scale_siginal_sb=RooRealVar("rrv_scale_siginal_sb","rrv_scale_siginal_sb",scale_signal_sb);
        rrv_scale_siginal_sb.setError(scale_signal_sb_error);
        #rrv_scale_siginal_sb.Print();
        draw_error_band_Decor("correct_factor_pdf","rrv_mass_lvj", paras, self.workspace4fit_,rrv_scale_siginal_sb,mplot2);

        mplot.GetYaxis().SetRangeUser(1e-2,mplot.GetMaximum()*1.1);
        self.draw_canvas1(mplot,"plots_%s/other/"%(self.channel),"correction_pdf_WJets_M_lvj_signal_region_to_sideband",0,0);
        self.draw_canvas1(mplot2,"plots_%s/other/"%(self.channel),"correction_WJets_M_lvj_signal_region_to_sideband",0.,0);

        model_pdf_WJets_sb_lo_from_fitting_mlvj_Deco=self.workspace4fit_.pdf("model_pdf_WJets_sb_lo_%s_from_fitting_mlvj_Deco_WJets_sb_lo_%s_from_fitting_mlvj"%(self.channel, self.channel));
        model_pdf_WJets_sb_lo_from_fitting_mlvj_Deco.Print("v");

        model_pdf_WJets_signal_region_after_correct_mlvj=RooProdPdf("model_pdf_WJets_signal_region_%s_after_correct_mlvj"%(self.channel),"model_pdf_WJets_signal_region_%s_after_correct_mlvj"%(self.channel),model_pdf_WJets_sb_lo_from_fitting_mlvj_Deco,self.workspace4fit_.pdf("correct_factor_pdf"));
        model_pdf_WJets_signal_region_after_correct_mlvj.Print()
        self.fix_Pdf(model_pdf_WJets_signal_region_after_correct_mlvj,RooArgSet(rrv_x))
        #raw_input("ENTER");
        getattr(self.workspace4fit_,"import")(model_pdf_WJets_signal_region_after_correct_mlvj)

        #calculate the normalization and alpha for limit datacard
        if self.workspace4fit_.var("rrv_number_WJets_in_mj_signal_region_%s_from_fitting"%(self.channel)):
            self.workspace4fit_.var("rrv_number_WJets_signal_region_%s_mlvj"%(self.channel)).setVal(self.workspace4fit_.var("rrv_number_WJets_in_mj_signal_region_%s_from_fitting"%(self.channel)).getVal());
            self.workspace4fit_.var("rrv_number_WJets_signal_region_%s_mlvj"%(self.channel)).setError(self.workspace4fit_.var("rrv_number_WJets_in_mj_signal_region_%s_from_fitting"%(self.channel)).getError());
        else:
            self.number_WJets_insideband=int(round(self.workspace4fit_.var("rrv_number_WJets_sb_lo_mlvj_from_fitting").getVal()));
            number_tmp=self.workspace4fit_.var("rrv_number_WJets_sb_lo_%s_mlvj_from_fitting"%(self.channel)).getVal()*self.workspace4fit_.var("rrv_number_WJets_signal_region_%s_mlvj"%(self.channel)).getVal()/self.workspace4fit_.var("rrv_number_WJets_sb_lo_%s_mlvj"%(self.channel)).getVal();
            self.workspace4fit_.var("rrv_number_WJets_signal_region_%s_mlvj"%(self.channel)).setVal(number_tmp);
            self.datadriven_alpha_WJets_unbin =number_tmp/self.number_WJets_insideband;

        self.workspace4fit_.var("rrv_number_WJets_signal_region_%s_mlvj"%(self.channel)).setConstant(kTRUE);

    ############# ---------------------------------------------------
    def fit_m_j_single_MC(self,in_file_name, label, in_model_name):
        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j"); 
        rdataset_mj = self.workspace4fit_.data("rdataset4fit"+label+"_"+self.channel+"_mj"); 
        rdataset_mj.Print();

        model = self.make_Model(label,in_model_name);
        rfresult = model.fitTo(rdataset_mj,RooFit.Save(1),RooFit.Extended(kTRUE) );
        rfresult = model.fitTo(rdataset_mj,RooFit.Save(1), RooFit.SumW2Error(kTRUE) ,RooFit.Extended(kTRUE) );
        rfresult = model.fitTo(rdataset_mj,RooFit.Save(1), RooFit.SumW2Error(kTRUE) ,RooFit.Extended(kTRUE) );

        mplot = rrv_mass_j.frame(RooFit.Title(in_file_name+" fitted by "+in_model_name));
        rdataset_mj.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2));
        model.plotOn(mplot,RooFit.VisualizeError(rfresult,1,kFALSE),RooFit.DrawOption("F"),RooFit.FillColor(kOrange), RooFit.VLines());
        #draw_error_band(rdataset_mj, model,self.workspace4fit_.var("rrv_number"+label+"_"+self.channel+"_mj") ,rfresult,mplot,6,"L");
        draw_error_band_extendPdf(rdataset_mj, model, rfresult,mplot,6,"L");
        rdataset_mj.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) );
        model.plotOn( mplot , RooFit.VLines());

        #pull
        hpull=mplot.pullHist();
        mplot_pull = rrv_mass_j.frame(RooFit.Title("Pull Distribution"));
        mplot_pull.addPlotable(hpull,"P");
        mplot_pull.SetTitle("PULL");
        mplot_pull.GetYaxis().SetRangeUser(-5,5);
         
        parameters_list=model.getParameters(rdataset_mj);
        mplot.GetYaxis().SetRangeUser(1e-2,mplot.GetMaximum()*1.1);
        self.draw_canvas( mplot, mplot_pull,parameters_list, "plots_%s/m_j_fitting_wtaggercut%s_nPV%sto%s/"%(self.channel, self.wtagger_cut, self.nPV_min, self.nPV_max), in_file_name, in_model_name)
        rfresult.Print(); 
        rfresult.covarianceMatrix().Print(); #raw_input("ENTER"); 
        
        #normalize the number of total events to lumi
        self.workspace4fit_.var("rrv_number"+label+"_"+self.channel+"_mj").setVal( self.workspace4fit_.var("rrv_number"+label+"_"+self.channel+"_mj").getVal()*self.workspace4fit_.var("rrv_scale_to_lumi"+label+"_"+self.channel).getVal()  )
        self.workspace4fit_.var("rrv_number"+label+"_"+self.channel+"_mj").setError(self.workspace4fit_.var("rrv_number"+label+"_"+self.channel+"_mj").getError()*self.workspace4fit_.var("rrv_scale_to_lumi"+label+"_"+self.channel).getVal()  )
        if TString(label).Contains("ggH"):
            self.workspace4fit_.var("rrv_number"+label+"_"+self.channel+"_mj").setVal( self.workspace4fit_.var("rrv_number"+label+"_"+self.channel+"_mj").getVal()  )
            self.workspace4fit_.var("rrv_number"+label+"_"+self.channel+"_mj").setError(self.workspace4fit_.var("rrv_number"+label+"_"+self.channel+"_mj").getError()  )
        self.workspace4fit_.var("rrv_number"+label+"_"+self.channel+"_mj").Print();
        #rfresult.Print(); model.getParameters(rdataset_mj).Print("v"); model_pdf=self.workspace4fit_.pdf("model_pdf"+label+"_"+self.channel+"_mj"); model_pdf.getParameters(rdataset_mj).Print("v"); raw_input("ENTER");

    ############# ---------------------------------------------------
    def fit_m_j_singlebackground_MC_TTbar_controlsample(self,in_file_name, label, in_model_name):
        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j"); 
        rdataset_mj = self.workspace4fit_.data("rdataset4fit"+label+"_"+self.channel+"_mj"); 
        model = self.make_Model(label,in_model_name);
        rfresult = model.fitTo(rdataset_mj,RooFit.Save(1), RooFit.SumW2Error(kTRUE) ,RooFit.Extended(kTRUE), RooFit.Range("controlsample_fitting_range") );
        rfresult = model.fitTo(rdataset_mj,RooFit.Save(1), RooFit.SumW2Error(kTRUE) ,RooFit.Extended(kTRUE), RooFit.Range("controlsample_fitting_range") );
        
        mplot = rrv_mass_j.frame(RooFit.Title(in_file_name+" fitted by "+in_model_name));
        rdataset_mj.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) );
        model.plotOn( mplot, RooFit.VisualizeError(rfresult,1),RooFit.FillColor(kOrange) , RooFit.VLines(),RooFit.NormRange("controlsample_fitting_range"));
        #model.plotOn(mplot,RooFit.VisualizeError(rfresult,1,kFALSE),RooFit.DrawOption("F"),RooFit.FillColor(kOrange), RooFit.VLines(),RooFit.NormRange("controlsample_fitting_range"));
        model.plotOn( mplot , RooFit.VLines(),RooFit.NormRange("controlsample_fitting_range"));
        model.plotOn( mplot, RooFit.Components("erfExp"+label+"_"+self.channel), RooFit.LineStyle(kDashed),RooFit.LineColor(kGreen) , RooFit.VLines(),RooFit.NormRange("controlsample_fitting_range"));
        model.plotOn( mplot, RooFit.Components("gaus"+label+"_"+self.channel), RooFit.LineStyle(kDashed),RooFit.LineColor(kRed) , RooFit.VLines(),RooFit.NormRange("controlsample_fitting_range"));
        model.plotOn( mplot , RooFit.VLines(),RooFit.NormRange("controlsample_fitting_range"));
        rdataset_mj.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) );
        #pull
        hpull=mplot.pullHist();
        mplot_pull = rrv_mass_j.frame(RooFit.Title("Pull Distribution"));
        mplot_pull.addPlotable(hpull,"P");
        mplot_pull.SetTitle("PULL");
        mplot_pull.GetYaxis().SetRangeUser(-5,5);
         
        parameters_list=model.getParameters(rdataset_mj);
        mplot.GetYaxis().SetRangeUser(1e-2,mplot.GetMaximum()*1.1);
        self.draw_canvas( mplot, mplot_pull,parameters_list, "plots_%s/m_j_fitting_TTbar_controlsample_wtaggercut%s_nPV%sto%s/"%(self.channel, self.wtagger_cut, self.nPV_min, self.nPV_max), in_file_name, in_model_name)
        rfresult.Print();

    ############# ---------------------------------------------------
    def change_dataset_to_histpdf(self, x,dataset):
        datahist=dataset.binnedClone(dataset.GetName()+"_binnedClone",dataset.GetName()+"_binnedClone")
        histpdf=RooHistPdf(dataset.GetName()+"_histpdf",dataset.GetName()+"_histpdf",RooArgSet(x),datahist)
        getattr(self.workspace4fit_,"import")(histpdf)

    ############# ---------------------------------------------------
    def change_dataset_to_histogram(self, x,dataset):
        datahist=dataset.binnedClone(dataset.GetName()+"_binnedClone",dataset.GetName()+"_binnedClone")
        return datahist.createHistogram("histo_%s"%(dataset.GetName()),x, RooFit.Binning(x.getBin(),x.getMin(),x.getMax()));
        
    ############# ---------------------------------------------------
    def fit_m_j_TTbar_controlsample(self,in_file_name,  in_model_name):
        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j");# rrv_mass_j.setBins(40)
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

        model_data = self.make_Model("_data",in_model_name);
        model_TotalMC = self.make_Model("_TotalMC",in_model_name);

        model_data.fitTo(rdataset_data_mj,RooFit.Save(1), RooFit.Extended(kTRUE) , RooFit.Range("controlsample_fitting_range") );
        rfresult = model_data.fitTo(rdataset_data_mj,RooFit.Save(1), RooFit.Extended(kTRUE) , RooFit.Range("controlsample_fitting_range") );

        model_TotalMC.fitTo(rdataset_TotalMC_mj, RooFit.SumW2Error(kTRUE),RooFit.Save(1), RooFit.Extended(kTRUE), RooFit.Range("controlsample_fitting_range") );
        model_TotalMC.fitTo(rdataset_TotalMC_mj, RooFit.SumW2Error(kTRUE),RooFit.Save(1), RooFit.Extended(kTRUE), RooFit.Range("controlsample_fitting_range") );
        scale_number_TotalMC=rdataset_TotalMC_mj.sumEntries()/rdataset_data_mj.sumEntries()
        
        mplot = rrv_mass_j.frame(RooFit.Title(in_file_name+" fitted by "+in_model_name));

        rdataset_data_mj.plotOn( mplot, RooFit.Invisible() );

        model_pdf_STop.plotOn(mplot,RooFit.Normalization(scale_number_STop),RooFit.Name("STop_invisible"),RooFit.Invisible(), RooFit.VLines())
        model_pdf_TTbar.plotOn(mplot,RooFit.Normalization(scale_number_TTbar),RooFit.Name("TTbar_invisible"), RooFit.AddTo("STop_invisible"),RooFit.Invisible(), RooFit.VLines())
        model_pdf_VV.plotOn(mplot,RooFit.Normalization(scale_number_VV),RooFit.Name("VV_invisible"), RooFit.AddTo("TTbar_invisible"),RooFit.Invisible(), RooFit.VLines())
        model_pdf_WJets.plotOn(mplot,RooFit.Normalization(scale_number_WJets),RooFit.Name("WJets_invisible"), RooFit.AddTo("VV_invisible"),RooFit.Invisible(), RooFit.VLines())
        model_pdf_WJets.plotOn(mplot,RooFit.Normalization(scale_number_WJets),RooFit.Name("WJets"), RooFit.AddTo("VV_invisible"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["WJets"]), RooFit.LineColor(self.color_palet["WJets"]), RooFit.VLines())
        model_pdf_VV.plotOn(mplot,RooFit.Normalization(scale_number_VV),RooFit.Name("VV"), RooFit.AddTo("TTbar_invisible"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["VV"]), RooFit.LineColor(self.color_palet["VV"]), RooFit.VLines())
        model_pdf_TTbar.plotOn(mplot,RooFit.Normalization(scale_number_TTbar),RooFit.Name("TTbar"), RooFit.AddTo("STop_invisible"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["TTbar"]), RooFit.LineColor(self.color_palet["TTbar"]), RooFit.VLines())
        model_pdf_STop.plotOn(mplot,RooFit.Normalization(scale_number_STop),RooFit.Name("STop"), RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["STop"]), RooFit.LineColor(self.color_palet["STop"]), RooFit.VLines())

        rdataset_data_mj.plotOn( mplot,RooFit.Name("data") );
        if self.wtagger_cut<10:
            model_TotalMC.plotOn( mplot,RooFit.Normalization(scale_number_TotalMC) ,RooFit.Name("MC fit") ,RooFit.NormRange("controlsample_fitting_range") , RooFit.LineStyle(kDashed));
            model_data.plotOn( mplot,RooFit.Name("data fit"), RooFit.NormRange("controlsample_fitting_range") );
        leg=self.legend4Plot(mplot,0)
        mplot.addObject(leg)

        #add mean and width to mplot
        parameters_list=model_data.getParameters(rdataset_data_mj);
        parameters_list.add( model_TotalMC.getParameters(rdataset_data_mj))
        rrv_mean_gaus_data=parameters_list.find("rrv_mean_gaus_data");
        rrv_sigma_gaus_data=parameters_list.find("rrv_sigma_gaus_data");
        rrv_mean_gaus_TotalMC=parameters_list.find("rrv_mean_gaus_TotalMC");
        rrv_sigma_gaus_TotalMC=parameters_list.find("rrv_sigma_gaus_TotalMC");
        tl_MC_mean   =TLatex(0.65 ,0.45, ("Mean_{MC  } = %3.1f #pm %2.1f")%(rrv_mean_gaus_TotalMC.getVal(), rrv_mean_gaus_TotalMC.getError()) );
        tl_MC_sigma  =TLatex(0.65 ,0.40, ("Sigma_{MC  }= %2.1f #pm %2.1f")%(rrv_sigma_gaus_TotalMC.getVal(), rrv_sigma_gaus_TotalMC.getError()) );
        tl_data_mean =TLatex(0.65 ,0.35, ("Mean_{data} = %3.1f #pm %2.1f")%(rrv_mean_gaus_data.getVal(), rrv_mean_gaus_data.getError()) );
        tl_data_sigma=TLatex(0.65 ,0.30, ("Sigma_{data}= %2.1f #pm %2.1f")%(rrv_sigma_gaus_data.getVal(), rrv_sigma_gaus_data.getError()) );
        tl_MC_mean.SetNDC(); tl_MC_sigma.SetNDC(); tl_data_mean.SetNDC(); tl_data_sigma.SetNDC();
        tl_data_mean.SetTextSize(0.03)
        tl_data_sigma.SetTextSize(0.03)
        tl_MC_mean.SetTextSize(0.03)
        tl_MC_sigma.SetTextSize(0.03)
        if self.wtagger_cut<10:
            mplot.addObject(tl_data_mean);
            mplot.addObject(tl_data_sigma);
            mplot.addObject(tl_MC_mean);
            mplot.addObject(tl_MC_sigma);
        #signal window
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
         
        mplot.GetYaxis().SetRangeUser(1e-2,mplot.GetMaximum()*1.1);
        self.draw_canvas( mplot, mplot_pull,parameters_list, "plots_%s/m_j_fitting_TTbar_controlsample_wtaggercut%s_nPV%sto%s/"%(self.channel, self.wtagger_cut, self.nPV_min, self.nPV_max), in_file_name, in_model_name+"Total")
        self.draw_canvas1(mplot,"plots_%s/m_j_fitting_TTbar_controlsample_wtaggercut%s_nPV%sto%s/"%(self.channel, self.wtagger_cut, self.nPV_min, self.nPV_max),"control_%s_%s"%(self.wtagger_lable,self.channel));
        
        #calculate the mva eff
        self.workspace4fit_.var("rrv_number_dataset_signal_region_data_mj").Print()
        self.workspace4fit_.var("rrv_number_dataset_signal_region_VV_mj").Print()
        self.workspace4fit_.var("rrv_number_dataset_signal_region_WJets_mj").Print()
        self.workspace4fit_.var("rrv_number_dataset_signal_region_STop_mj").Print()
        self.workspace4fit_.var("rrv_number_dataset_signal_region_TTbar_mj").Print()

        number_dataset_signal_region_data_mj=self.workspace4fit_.var("rrv_number_dataset_signal_region_data_mj").getVal();
        number_dataset_signal_region_error2_data_mj=self.workspace4fit_.var("rrv_number_dataset_signal_region_error2_data_mj").getVal();
        print "event number of data in signal_region: %s +/- %s"%(number_dataset_signal_region_data_mj, number_dataset_signal_region_error2_data_mj);
        self.file_out_ttbar_control.write("event number of data in signal_region: %s +/- %s\n"%(number_dataset_signal_region_data_mj, number_dataset_signal_region_error2_data_mj));
        number_dataset_signal_region_pseudodata_mj=self.workspace4fit_.var("rrv_number_dataset_signal_region_pseudodata_mj").getVal();
        number_dataset_signal_region_error2_pseudodata_mj=self.workspace4fit_.var("rrv_number_dataset_signal_region_error2_pseudodata_mj").getVal();
        print "event number of pseudodata in signal_region: %s +/- %s "%(number_dataset_signal_region_pseudodata_mj, number_dataset_signal_region_error2_pseudodata_mj);
        self.file_out_ttbar_control.write("event number of pseudodata in signal_region: %s +/- %s \n"%(number_dataset_signal_region_pseudodata_mj, number_dataset_signal_region_error2_pseudodata_mj));


        number_dataset_signal_region_before_mva_data_mj=self.workspace4fit_.var("rrv_number_dataset_signal_region_before_mva_data_mj").getVal();
        number_dataset_signal_region_before_mva_error2_data_mj=self.workspace4fit_.var("rrv_number_dataset_signal_region_before_mva_error2_data_mj").getVal();
        print "event number of data in signal_region before_mva: %s +/- %s"%(number_dataset_signal_region_before_mva_data_mj, number_dataset_signal_region_before_mva_error2_data_mj);
        self.file_out_ttbar_control.write("event number of data in signal_region before_mva: %s +/- %s\n"%(number_dataset_signal_region_before_mva_data_mj, number_dataset_signal_region_before_mva_error2_data_mj));

        number_dataset_signal_region_before_mva_pseudodata_mj=self.workspace4fit_.var("rrv_number_dataset_signal_region_before_mva_pseudodata_mj").getVal();
        number_dataset_signal_region_before_mva_error2_pseudodata_mj=self.workspace4fit_.var("rrv_number_dataset_signal_region_before_mva_error2_pseudodata_mj").getVal();
        print "event number of pseudodata in signal_region before_mva: %s +/- %s "%(number_dataset_signal_region_before_mva_pseudodata_mj, number_dataset_signal_region_before_mva_error2_pseudodata_mj);
        self.file_out_ttbar_control.write("event number of pseudodata in signal_region before_mva: %s +/- %s \n"%(number_dataset_signal_region_before_mva_pseudodata_mj, number_dataset_signal_region_before_mva_error2_pseudodata_mj));

        # wtagger_eff reweight: only reweight the efficiency difference between MC and data
        wtagger_eff_MC  = number_dataset_signal_region_pseudodata_mj/number_dataset_signal_region_before_mva_pseudodata_mj;
        wtagger_eff_data= number_dataset_signal_region_data_mj/number_dataset_signal_region_before_mva_data_mj;

        wtagger_eff_reweight=wtagger_eff_data/wtagger_eff_MC;
        wtagger_eff_reweight_err=wtagger_eff_reweight*TMath.Sqrt(
                number_dataset_signal_region_error2_data_mj/number_dataset_signal_region_data_mj/number_dataset_signal_region_data_mj +  
                number_dataset_signal_region_error2_pseudodata_mj/number_dataset_signal_region_pseudodata_mj/number_dataset_signal_region_pseudodata_mj +  
                number_dataset_signal_region_before_mva_error2_data_mj/number_dataset_signal_region_before_mva_data_mj/number_dataset_signal_region_data_mj +  
                number_dataset_signal_region_before_mva_error2_pseudodata_mj/number_dataset_signal_region_before_mva_pseudodata_mj/number_dataset_signal_region_before_mva_pseudodata_mj 
                );
        
        print "wtagger_eff_MC   = %s "%(wtagger_eff_MC )
        print "wtagger_eff_data = %s "%(wtagger_eff_data )
        print "wtagger_eff_reweight = %s +/- %s"%(wtagger_eff_reweight, wtagger_eff_reweight_err)
        self.file_out_ttbar_control.write("wtagger_eff_MC   = %s \n"%(wtagger_eff_MC ));
        self.file_out_ttbar_control.write("wtagger_eff_data = %s \n"%(wtagger_eff_data ));
        self.file_out_ttbar_control.write("wtagger_eff_reweight = %s +/- %s\n"%(wtagger_eff_reweight, wtagger_eff_reweight_err));

        # wtagger reweight: reweight the event number difference in signal region after mva cut between MC and data
        wtagger_reweight=number_dataset_signal_region_data_mj/number_dataset_signal_region_pseudodata_mj;
        wtagger_reweight_err=wtagger_reweight*TMath.Sqrt( 
                number_dataset_signal_region_error2_data_mj/number_dataset_signal_region_data_mj/number_dataset_signal_region_data_mj +  
                number_dataset_signal_region_error2_pseudodata_mj/number_dataset_signal_region_pseudodata_mj/number_dataset_signal_region_pseudodata_mj 
                );
        print "wtagger_reweight = %s +/- %s"%(wtagger_reweight, wtagger_reweight_err)
        self.file_out_ttbar_control.write("wtagger_reweight = %s +/- %s\n"%(wtagger_reweight, wtagger_reweight_err));

    ########## ---------------------------------------------------
    def get_mj_and_mlvj_dataset(self,in_file_name, label):# to get the shape of m_lvj
        # read in tree
        fileIn_name=TString(self.file_Directory+in_file_name);
        fileIn = TFile(fileIn_name.Data());
        treeIn = fileIn.Get("otree");
        
        ## define bdt reader
        #listOfTrainingVariables1 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1"];
        ##bdtSimple = tmvaApplicator( listOfTrainingVariables1, "weights/%s/Wtagger_200to275_simple_BDT.weights.xml"%(self.higgs_sample));
        #bdtSimple = tmvaApplicator( listOfTrainingVariables1, "weights/General/Wtagger_200to275_simple_BDT.weights.xml");
            
        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j") 
        rrv_mass_lvj = self.workspace4fit_.var("rrv_mass_lvj") 
        rrv_weight = RooRealVar("rrv_weight","rrv_weight",0. ,10000000.) 
        #dataset of m_j
        rdataset_mj     = RooDataSet("rdataset"+label+"_"+self.channel+"_mj","rdataset"+label+"_"+self.channel+"_mj",RooArgSet(rrv_mass_j,rrv_weight),RooFit.WeightVar(rrv_weight) );
        rdataset4fit_mj = RooDataSet("rdataset4fit"+label+"_"+self.channel+"_mj","rdataset4fit"+label+"_"+self.channel+"_mj",RooArgSet(rrv_mass_j,rrv_weight),RooFit.WeightVar(rrv_weight) );
        #dataset of m_lvj
        rdataset_sb_lo_mlvj         = RooDataSet("rdataset"+label+"_sb_lo"+"_"+self.channel+"_mlvj","rdataset"+label+"_sb_lo"+"_"+self.channel+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        rdataset_signal_region_mlvj = RooDataSet("rdataset"+label+"_signal_region"+"_"+self.channel+"_mlvj","rdataset"+label+"_signal_region"+"_"+self.channel+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        rdataset_sb_hi_mlvj         = RooDataSet("rdataset"+label+"_sb_hi"+"_"+self.channel+"_mlvj","rdataset"+label+"_sb_hi"+"_"+self.channel+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        rdataset4fit_sb_lo_mlvj     = RooDataSet("rdataset4fit"+label+"_sb_lo"+"_"+self.channel+"_mlvj","rdataset4fit"+label+"_sb_lo"+"_"+self.channel+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        rdataset4fit_signal_region_mlvj = RooDataSet("rdataset4fit"+label+"_signal_region"+"_"+self.channel+"_mlvj","rdataset4fit"+label+"_signal_region"+"_"+self.channel+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        rdataset4fit_sb_hi_mlvj     = RooDataSet("rdataset4fit"+label+"_sb_hi"+"_"+self.channel+"_mlvj","rdataset4fit"+label+"_sb_hi"+"_"+self.channel+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 

        rdataset4fit_sb_lo_mlvj.Print();
        rdataset4fit_signal_region_mlvj.Print();
        #raw_input("ENTER");
        data_category=RooCategory("data_category","data_category");
        data_category.defineType("sideband");
        data_category.defineType("signal_region");
        combData=RooDataSet("combData"+label+"_"+self.channel,"combData"+label+"_"+self.channel,RooArgSet(rrv_mass_lvj, data_category, rrv_weight),RooFit.WeightVar(rrv_weight) );

        print "N entries: ", treeIn.GetEntries()
        hnum_4region=TH1D("hnum_4region"+label+"_"+self.channel,"hnum_4region"+label+"_"+self.channel,4,-1.5,2.5);# m_j   -1: sb_lo; 0:signal_region; 1: sb_hi; 2:total
        hnum_2region=TH1D("hnum_2region"+label+"_"+self.channel,"hnum_2region"+label+"_"+self.channel,2,-0.5,1.5);# m_lvj  0: signal_region; 1: total
        for i in range(treeIn.GetEntries()):
            if i % 10000 == 0: print "i: ",i
            treeIn.GetEntry(i);
            if i==0:
                tmp_scale_to_lumi=treeIn.wSampleWeight;
    
            discriminantCut = False; 
            #    listOfVarVals = [];
            #    for kk in range(len(listOfTrainingVariables1)):
            #        listOfVarVals.append( getattr( treeIn, listOfTrainingVariables1[kk] ) );
            #    BDTval = bdtSimple.eval( listOfVarVals );
            #    #print BDTval;
            #    if BDTval > 0.0: discriminantCut = True;
            #else: discriminantCut = False;

            # new mva cut
            #print "%s, %s, %s"%(treeIn.jet_pt_pr, treeIn.ca8wjettaggerpt200_275, treeIn.ca8wjettaggerpt275_500 );
            #wtagger=-1;
            #if treeIn.jet_pt_pr>200 and treeIn.jet_pt_pr<275: wtagger=treeIn.ca8wjettaggerpt200_275;
            #if treeIn.jet_pt_pr>275 and treeIn.jet_pt_pr<500: wtagger=treeIn.ca8wjettaggerpt275_500;
            #if wtagger >=self.wtagger_cut:
            #    discriminantCut=True;
            #else:
            #    discriminantCut=False;

            wtagger=-1;
            wtagger=treeIn.jet_tau2tau1;
            if wtagger <self.wtagger_cut:
                discriminantCut=True;
            else:
                discriminantCut=False;
             
            if treeIn.ungroomed_jet_pt > 200. and discriminantCut and treeIn.jet_mass_pr >= rrv_mass_j.getMin() and treeIn.jet_mass_pr<=rrv_mass_j.getMax() and treeIn.nbjets <1 and treeIn.mass_lvj >= rrv_mass_lvj.getMin() and treeIn.mass_lvj<=rrv_mass_lvj.getMax() and  treeIn.nPV >=self.nPV_min and treeIn.nPV<=self.nPV_max :
            #if treeIn.ungroomed_jet_pt > 200. and discriminantCut and treeIn.jet_mass_pr >= rrv_mass_j.getMin() and treeIn.jet_mass_pr<=rrv_mass_j.getMax() and treeIn.njets ==0 and treeIn.mass_lvj >= rrv_mass_lvj.getMin() and treeIn.mass_lvj<=rrv_mass_lvj.getMax() and  treeIn.nPV >=self.nPV_min and treeIn.nPV<=self.nPV_max :
            #if treeIn.ungroomed_jet_pt > 200. and discriminantCut and treeIn.jet_mass_pr >= rrv_mass_j.getMin() and treeIn.jet_mass_pr<rrv_mass_j.getMax() and treeIn.njets ==0 and treeIn.mass_lvj >= rrv_mass_lvj.getMin() and treeIn.mass_lvj<rrv_mass_lvj.getMax() :
            #if treeIn.jet_pt_pr > 200. and discriminantCut and treeIn.jet_mass_pr >= rrv_mass_j.getMin() and treeIn.jet_mass_pr<rrv_mass_j.getMax() and treeIn.njets <2 and treeIn.nbjets==0 and treeIn.mass_lvj >= rrv_mass_lvj.getMin() and treeIn.mass_lvj<rrv_mass_lvj.getMax() :
                tmp_event_weight= treeIn.totalEventWeight;
                tmp_event_weight4fit= treeIn.eff_and_pu_Weight;
                tmp_interference_weight_H600=treeIn.interference_Weight_H600;
                tmp_interference_weight_H700=treeIn.interference_Weight_H700;
                tmp_interference_weight_H800=treeIn.interference_Weight_H800;
                tmp_interference_weight_H900=treeIn.interference_Weight_H900;
                tmp_interference_weight_H1000=treeIn.interference_Weight_H1000;
                if label=="_ggH600":
                    tmp_event_weight=tmp_event_weight*tmp_interference_weight_H600
                    tmp_event_weight4fit=tmp_event_weight4fit*tmp_interference_weight_H600
                if label=="_ggH700":
                    tmp_event_weight=tmp_event_weight*tmp_interference_weight_H700
                    tmp_event_weight4fit=tmp_event_weight4fit*tmp_interference_weight_H700
                if label=="_ggH800":
                    tmp_event_weight=tmp_event_weight*tmp_interference_weight_H800
                    tmp_event_weight4fit=tmp_event_weight4fit*tmp_interference_weight_H800
                if label=="_ggH900":
                    tmp_event_weight=tmp_event_weight*tmp_interference_weight_H900
                    tmp_event_weight4fit=tmp_event_weight4fit*tmp_interference_weight_H900
                if label=="_ggH1000":
                    tmp_event_weight=tmp_event_weight*tmp_interference_weight_H1000
                    tmp_event_weight4fit=tmp_event_weight4fit*tmp_interference_weight_H1000
                # for multi-sample, like STop and VV. There are two sample, and two wSampleWeight_value.Use the least wSampleWeight as scale. 
                tmp_event_weight4fit=tmp_event_weight4fit*treeIn.wSampleWeight/tmp_scale_to_lumi

                if TString(label).Contains("ggH"):tmp_event_weight=tmp_event_weight/self.higgs_xs_scale; 
                if TString(label).Contains("ggH"):tmp_event_weight4fit=tmp_event_weight4fit/self.higgs_xs_scale; 

                #wtagger_eff_reweight
                if not label=="_data": tmp_event_weight=tmp_event_weight*self.rrv_wtagger_eff_reweight.getVal();

                rrv_mass_lvj.setVal(treeIn.mass_lvj);
                if treeIn.jet_mass_pr >= self.mj_sideband_lo_min and treeIn.jet_mass_pr < self.mj_sideband_lo_max:
                    rdataset_sb_lo_mlvj.add( RooArgSet( rrv_mass_lvj ), tmp_event_weight );
                    rdataset4fit_sb_lo_mlvj.add( RooArgSet( rrv_mass_lvj ), tmp_event_weight4fit );
                    data_category.setLabel("sideband"); combData.add(RooArgSet(rrv_mass_lvj,data_category),tmp_event_weight);
                if treeIn.jet_mass_pr >= self.mj_signal_min      and treeIn.jet_mass_pr < self.mj_signal_max:
                    rdataset_signal_region_mlvj.add( RooArgSet( rrv_mass_lvj ), tmp_event_weight );
                    rdataset4fit_signal_region_mlvj.add( RooArgSet( rrv_mass_lvj ), tmp_event_weight4fit );
                    data_category.setLabel("signal_region"); combData.add(RooArgSet(rrv_mass_lvj,data_category),tmp_event_weight);
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

        if not label=="_data": tmp_scale_to_lumi=tmp_scale_to_lumi*self.rrv_wtagger_eff_reweight.getVal();
        rrv_scale_to_lumi=RooRealVar("rrv_scale_to_lumi"+label+"_"+self.channel,"rrv_scale_to_lumi"+label+"_"+self.channel,tmp_scale_to_lumi)
        rrv_scale_to_lumi.Print()
        getattr(self.workspace4fit_,"import")(rrv_scale_to_lumi)
        #prepare m_lvj dataset
        rrv_number_dataset_signal_region_mlvj=RooRealVar("rrv_number_dataset_signal_region"+label+"_"+self.channel+"_mlvj","rrv_number_dataset_signal_region"+label+"_"+self.channel+"_mlvj",hnum_2region.GetBinContent(1));
        rrv_number_dataset_AllRange_mlvj=RooRealVar("rrv_number_dataset_AllRange"+label+"_"+self.channel+"_mlvj","rrv_number_dataset_AllRange"+label+"_"+self.channel+"_mlvj",hnum_2region.GetBinContent(2));
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_signal_region_mlvj)
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_AllRange_mlvj)
               
        getattr(self.workspace4fit_,"import")(rdataset_sb_lo_mlvj);
        getattr(self.workspace4fit_,"import")(rdataset_signal_region_mlvj);
        getattr(self.workspace4fit_,"import")(rdataset_sb_hi_mlvj); 
        getattr(self.workspace4fit_,"import")(rdataset4fit_sb_lo_mlvj);
        getattr(self.workspace4fit_,"import")(rdataset4fit_signal_region_mlvj);
        getattr(self.workspace4fit_,"import")(rdataset4fit_sb_hi_mlvj);
        getattr(self.workspace4fit_,"import")(combData);
        self.file_out.write("\n%s events number in m_lvj from dataset: %s"%(label,rdataset_signal_region_mlvj.sumEntries()))
        #prepare m_j dataset
        rrv_number_dataset_sb_lo_mj=RooRealVar("rrv_number_dataset_sb_lo"+label+"_"+self.channel+"_mj","rrv_number_dataset_sb_lo"+label+"_"+self.channel+"_mj",hnum_4region.GetBinContent(1));
        rrv_number_dataset_signal_region_mj=RooRealVar("rrv_number_dataset_signal_region"+label+"_"+self.channel+"_mj","rrv_number_dataset_signal_region"+label+"_"+self.channel+"_mj",hnum_4region.GetBinContent(2));
        rrv_number_dataset_sb_hi_mj=RooRealVar("rrv_number_dataset_sb_hi"+label+"_"+self.channel+"_mj","rrv_number_dataset_sb_hi"+label+"_"+self.channel+"_mj",hnum_4region.GetBinContent(3));
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
    def get_mj_and_mlvj_dataset_TTbar_controlsample(self,in_file_name, label):# to get the shape of m_lvj
        # read in tree
        fileIn_name=TString(self.file_Directory+in_file_name);
        fileIn = TFile(fileIn_name.Data());
        treeIn = fileIn.Get("otree");
        
        # define bdt reader
        #listOfTrainingVariables1 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1"];
        #bdtSimple = tmvaApplicator( listOfTrainingVariables1, "weights/%s/Wtagger_200to275_simple_BDT.weights.xml"%(self.higgs_sample));
        #bdtSimple = tmvaApplicator( listOfTrainingVariables1, "weights/General/Wtagger_200to275_simple_BDT.weights.xml");
            
        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j") 
        rrv_mass_lvj = self.workspace4fit_.var("rrv_mass_lvj") 
        rrv_weight = RooRealVar("rrv_weight","rrv_weight",0. ,10000000.) 
        #dataset of m_j
        rdataset_mj = RooDataSet("rdataset"+label+"_"+self.channel+"_mj","rdataset"+label+"_"+self.channel+"_mj",RooArgSet(rrv_mass_j,rrv_weight),RooFit.WeightVar(rrv_weight) );
        rdataset4fit_mj = RooDataSet("rdataset4fit"+label+"_"+self.channel+"_mj","rdataset4fit"+label+"_"+self.channel+"_mj",RooArgSet(rrv_mass_j,rrv_weight),RooFit.WeightVar(rrv_weight) );
        #dataset of m_lvj
        rdataset_sb_lo_mlvj  = RooDataSet("rdataset"+label+"_sb_lo"+"_"+self.channel+"_mlvj","rdataset"+label+"_sb_lo"+"_"+self.channel+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        rdataset_signal_region_mlvj = RooDataSet("rdataset"+label+"_signal_region"+"_"+self.channel+"_mlvj","rdataset"+label+"_signal_region"+"_"+self.channel+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        rdataset_sb_hi_mlvj  = RooDataSet("rdataset"+label+"_sb_hi"+"_"+self.channel+"_mlvj","rdataset"+label+"_sb_hi"+"_"+self.channel+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        rdataset4fit_sb_lo_mlvj  = RooDataSet("rdataset4fit"+label+"_sb_lo"+"_"+self.channel+"_mlvj","rdataset4fit"+label+"_sb_lo"+"_"+self.channel+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        rdataset4fit_signal_region_mlvj = RooDataSet("rdataset4fit"+label+"_signal_region"+"_"+self.channel+"_mlvj","rdataset4fit"+label+"_signal_region"+"_"+self.channel+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 
        rdataset4fit_sb_hi_mlvj  = RooDataSet("rdataset4fit"+label+"_sb_hi"+"_"+self.channel+"_mlvj","rdataset4fit"+label+"_sb_hi"+"_"+self.channel+"_mlvj",RooArgSet(rrv_mass_lvj,rrv_weight),RooFit.WeightVar(rrv_weight) ); 

        # make cuts (including mass drop) # create a RooDataSet
        print "N entries: ", treeIn.GetEntries()
        #raw_input("Enter")
        hnum_4region=TH1D("hnum_4region"+label+"_"+self.channel,"hnum_4region"+label+"_"+self.channel,4,-1.5,2.5);# m_j   -1: sb_lo; 0:signal_region; 1: sb_hi; 2:total
        hnum_4region_error2=TH1D("hnum_4region_error2"+label+"_"+self.channel,"hnum_4region_error2"+label+"_"+self.channel,4,-1.5,2.5);# m_j   -1: sb_lo; 0:signal_region; 1: sb_hi; 2:total
        hnum_4region_before_mva=TH1D("hnum_4region_before_mva"+label+"_"+self.channel,"hnum_4region_before_mva"+label+"_"+self.channel,4,-1.5,2.5);# m_j   -1: sb_lo; 0:signal_region; 1: sb_hi; 2:total
        hnum_4region_before_mva_error2=TH1D("hnum_4region_before_mva_error2"+label+"_"+self.channel,"hnum_4region_before_mva_error2"+label+"_"+self.channel,4,-1.5,2.5);# m_j   -1: sb_lo; 0:signal_region; 1: sb_hi; 2:total
        hnum_2region=TH1D("hnum_2region"+label+"_"+self.channel,"hnum_2region"+label+"_"+self.channel,2,-0.5,1.5);# m_lvj  0: signal_region; 1: total
        hnum_2region_error2=TH1D("hnum_2region_error2"+label+"_"+self.channel,"hnum_2region_error2"+label+"_"+self.channel,2,-0.5,1.5);# m_lvj  0: signal_region; 1: total
        for i in range(treeIn.GetEntries()):
            if i % 10000 == 0: print "i: ",i
            treeIn.GetEntry(i);
            if i==0: tmp_scale_to_lumi=treeIn.wSampleWeight;
    
            discriminantCut = False; 

            wtagger=-1;
            #if treeIn.ungroomed_jet_pt>200 and treeIn.ungroomed_jet_pt<=275:
            #    #wtagger=treeIn.ca8wjettaggerpt200_275;
            #    wtagger=treeIn.ungroomedwjettaggerpt200_275;
            #if treeIn.ungroomed_jet_pt>275 and treeIn.ungroomed_jet_pt<=500:
            #    #wtagger=treeIn.ca8wjettaggerpt275_500;
            #    wtagger=treeIn.ungroomedwjettaggerpt275_500;
            wtagger=treeIn.jet_tau2tau1;
            if wtagger <self.wtagger_cut:
                discriminantCut=True;
            else:
                discriminantCut=False;

            if treeIn.ungroomed_jet_pt > 200. and discriminantCut and treeIn.jet_mass_pr >= rrv_mass_j.getMin() and treeIn.jet_mass_pr<=rrv_mass_j.getMax() and treeIn.nbjets >=1 and treeIn.mass_lvj >= rrv_mass_lvj.getMin() and treeIn.mass_lvj<=rrv_mass_lvj.getMax() and  treeIn.nPV >=self.nPV_min and treeIn.nPV<=self.nPV_max  :
                tmp_event_weight= treeIn.totalEventWeight;
                tmp_event_weight4fit= treeIn.eff_and_pu_Weight;
                tmp_interference_weight_H600=treeIn.interference_Weight_H600;
                tmp_interference_weight_H700=treeIn.interference_Weight_H700;
                tmp_interference_weight_H800=treeIn.interference_Weight_H800;
                tmp_interference_weight_H900=treeIn.interference_Weight_H900;
                tmp_interference_weight_H1000=treeIn.interference_Weight_H1000;
                if label=="_ggH600": 
                    tmp_event_weight=tmp_event_weight*tmp_interference_weight_H600
                    tmp_event_weight4fit=tmp_event_weight4fit*tmp_interference_weight_H600
                if label=="_ggH700":
                    tmp_event_weight=tmp_event_weight*tmp_interference_weight_H700
                    tmp_event_weight4fit=tmp_event_weight4fit*tmp_interference_weight_H700
                if label=="_ggH800":
                    tmp_event_weight=tmp_event_weight*tmp_interference_weight_H800
                    tmp_event_weight4fit=tmp_event_weight4fit*tmp_interference_weight_H800
                if label=="_ggH900":
                    tmp_event_weight=tmp_event_weight*tmp_interference_weight_H900
                    tmp_event_weight4fit=tmp_event_weight4fit*tmp_interference_weight_H900
                if label=="_ggH1000":
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
                if treeIn.jet_mass_pr >=self.mj_signal_min      and treeIn.jet_mass_pr <self.mj_signal_max     :
                    hnum_4region.Fill(0,tmp_event_weight);
                    hnum_4region_error2.Fill(0,tmp_event_weight*tmp_event_weight);
                if treeIn.jet_mass_pr >=self.mj_sideband_hi_min and treeIn.jet_mass_pr <self.mj_sideband_hi_max: hnum_4region.Fill(1,tmp_event_weight);
                hnum_4region.Fill(2,tmp_event_weight);

            if treeIn.ungroomed_jet_pt > 200. and treeIn.jet_mass_pr >= rrv_mass_j.getMin() and treeIn.jet_mass_pr<=rrv_mass_j.getMax() and treeIn.nbjets >=1 and treeIn.mass_lvj >= rrv_mass_lvj.getMin() and treeIn.mass_lvj<=rrv_mass_lvj.getMax() and  treeIn.nPV >=self.nPV_min and treeIn.nPV<=self.nPV_max  :
                tmp_event_weight= treeIn.totalEventWeight;
                tmp_event_weight4fit= treeIn.eff_and_pu_Weight;
                tmp_interference_weight_H600=treeIn.interference_Weight_H600;
                tmp_interference_weight_H700=treeIn.interference_Weight_H700;
                tmp_interference_weight_H800=treeIn.interference_Weight_H800;
                tmp_interference_weight_H900=treeIn.interference_Weight_H900;
                tmp_interference_weight_H1000=treeIn.interference_Weight_H1000;
                if label=="_ggH600":
                    tmp_event_weight=tmp_event_weight*tmp_interference_weight_H600
                    tmp_event_weight4fit=tmp_event_weight4fit*tmp_interference_weight_H600
                if label=="_ggH700":
                    tmp_event_weight=tmp_event_weight*tmp_interference_weight_H700
                    tmp_event_weight4fit=tmp_event_weight4fit*tmp_interference_weight_H700
                if label=="_ggH800":
                    tmp_event_weight=tmp_event_weight*tmp_interference_weight_H800
                    tmp_event_weight4fit=tmp_event_weight4fit*tmp_interference_weight_H800
                if label=="_ggH900":
                    tmp_event_weight=tmp_event_weight*tmp_interference_weight_H900
                    tmp_event_weight4fit=tmp_event_weight4fit*tmp_interference_weight_H900
                if label=="_ggH1000":
                    tmp_event_weight=tmp_event_weight*tmp_interference_weight_H1000
                    tmp_event_weight4fit=tmp_event_weight4fit*tmp_interference_weight_H1000
                tmp_event_weight4fit=tmp_event_weight4fit*treeIn.wSampleWeight/tmp_scale_to_lumi
                rrv_mass_lvj.setVal(treeIn.mass_lvj);

                if treeIn.jet_mass_pr >=self.mj_signal_min      and treeIn.jet_mass_pr <self.mj_signal_max     :
                    hnum_4region_before_mva.Fill(0,tmp_event_weight);
                    hnum_4region_before_mva_error2.Fill(0,tmp_event_weight*tmp_event_weight);

        rrv_scale_to_lumi=RooRealVar("rrv_scale_to_lumi"+label+"_"+self.channel,"rrv_scale_to_lumi"+label+"_"+self.channel,tmp_scale_to_lumi)
        rrv_scale_to_lumi.Print()
        getattr(self.workspace4fit_,"import")(rrv_scale_to_lumi)
        #prepare m_lvj dataset
        rrv_number_dataset_signal_region_mlvj=RooRealVar("rrv_number_dataset_signal_region"+label+"_"+self.channel+"_mlvj","rrv_number_dataset_signal_region"+label+"_"+self.channel+"_mlvj",hnum_2region.GetBinContent(1));
        rrv_number_dataset_AllRange_mlvj=RooRealVar("rrv_number_dataset_AllRange"+label+"_"+self.channel+"_mlvj","rrv_number_dataset_AllRange"+label+"_"+self.channel+"_mlvj",hnum_2region.GetBinContent(2));
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
        rrv_number_dataset_sb_lo_mj=RooRealVar("rrv_number_dataset_sb_lo"+label+"_"+self.channel+"_mj","rrv_number_dataset_sb_lo"+label+"_"+self.channel+"_mj",hnum_4region.GetBinContent(1));
        rrv_number_dataset_signal_region_mj=RooRealVar("rrv_number_dataset_signal_region"+label+"_"+self.channel+"_mj","rrv_number_dataset_signal_region"+label+"_"+self.channel+"_mj",hnum_4region.GetBinContent(2));
        rrv_number_dataset_signal_region_error2_mj=RooRealVar("rrv_number_dataset_signal_region_error2"+label+"_"+self.channel+"_mj","rrv_number_dataset_signal_region_error2"+label+"_"+self.channel+"_mj",hnum_4region_error2.GetBinContent(2));
        rrv_number_dataset_signal_region_before_mva_mj=RooRealVar("rrv_number_dataset_signal_region_before_mva"+label+"_"+self.channel+"_mj","rrv_number_dataset_signal_region_before_mva"+label+"_"+self.channel+"_mj",hnum_4region_before_mva.GetBinContent(2));
        rrv_number_dataset_signal_region_before_mva_error2_mj=RooRealVar("rrv_number_dataset_signal_region_before_mva_error2"+label+"_"+self.channel+"_mj","rrv_number_dataset_signal_region_before_mva_error2"+label+"_"+self.channel+"_mj",hnum_4region_before_mva_error2.GetBinContent(2));
        rrv_number_dataset_sb_hi_mj=RooRealVar("rrv_number_dataset_sb_hi"+label+"_"+self.channel+"_mj","rrv_number_dataset_sb_hi"+label+"_"+self.channel+"_mj",hnum_4region.GetBinContent(3));
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_sb_lo_mj)
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_signal_region_mj)
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_signal_region_error2_mj)
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_signal_region_before_mva_mj)
        getattr(self.workspace4fit_,"import")(rrv_number_dataset_signal_region_before_mva_error2_mj)
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
        rrv_number_dataset_signal_region_before_mva_mj.Print()
        rrv_number_dataset_sb_hi_mj.Print()
        print rdataset_signal_region_mlvj.sumEntries()
        print rrv_number_dataset_signal_region_mlvj.getVal()
        print rrv_number_dataset_AllRange_mlvj.getVal()

    ######## ++++++++++++++
    def ControlPlots(self):
        #cut="ungroomed_jet_pt>200 && jet_tau2tau1<0.525 && nbjets >=1 && mass_lvj>400 && mass_lvj <1400 && nPV>=%s && nPV<=%s"%(self.nPV_min,self.nPV_max);#ttbar control sample
        #self.make_controlplots(cut,"ttbar_control_sample");

        cut="ungroomed_jet_pt>200 && jet_tau2tau1<0.525 && jet_mass_pr>=70 && jet_mass_pr<=100 && nbjets>0 && mass_lvj>400 && mass_lvj <1400 && nPV>=%s && nPV<=%s"%(self.nPV_min,self.nPV_max);#before_cut
        self.make_controlplots(cut,"ttbar");

        cut="ungroomed_jet_pt>200 && jet_tau2tau1<0.525 && jet_mass_pr>=70 && jet_mass_pr<=100  && mass_lvj>400 && mass_lvj <1400 && nPV>=%s && nPV<=%s"%(self.nPV_min,self.nPV_max);#before_cut
        self.make_controlplots(cut,"before_cut");

        cut="ungroomed_jet_pt>200 && jet_tau2tau1<0.525 && jet_mass_pr>=70 && jet_mass_pr<=100 && nbjets<1 && mass_lvj>400 && mass_lvj <1400 && nPV>=%s && nPV<=%s"%(self.nPV_min,self.nPV_max);#before_cut
        self.make_controlplots(cut,"bf_cut");

        cut="ungroomed_jet_pt>200 && jet_tau2tau1<0.525 && jet_mass_pr>=70 && jet_mass_pr<=100 && njets<2 && nbjets <1 && mass_lvj>400 && mass_lvj <1400 && nPV>=%s && nPV<=%s"%(self.nPV_min,self.nPV_max);#signal region
        self.make_controlplots(cut,"signal_region");

        #cut="ungroomed_jet_pt>200 && jet_tau2tau1<0.525 && jet_mass_pr>=30 && jet_mass_pr<=70 && njets <1 && mass_lvj>400 && mass_lvj <1400 && nPV>=%s && nPV<=%s"%(self.nPV_min,self.nPV_max);#sb_lo
        #self.make_controlplots(cut,"sd_lo");

        #cut="ungroomed_jet_pt>200 && jet_tau2tau1<0.525 && jet_mass_pr>=100 && jet_mass_pr<=130 && njets <1 && mass_lvj>400 && mass_lvj <1400 && nPV>=%s && nPV<=%s"%(self.nPV_min,self.nPV_max);#sb_hi
        #self.make_controlplots(cut,"sd_hi");

        #cut="ungroomed_jet_pt>200 && jet_tau2tau1<0.525 && njets <1 && mass_lvj>400 && mass_lvj <1400 && nPV>=%s && nPV<=%s"%(self.nPV_min,self.nPV_max);#without jet_mass cut
        #self.make_controlplots(cut,"all_range");

    ######## ++++++++++++++
    def make_controlplots(self,cut,tag):
        self.make_controlplot("mass_lvj",cut,tag,25,400,1400,xtitle="mass(lvj)",ytitle="Events",logy=0 );
        self.make_controlplot("jet_mass_pr",cut,tag,55,0,220,xtitle="mass(j)",ytitle="Events",logy=0 );
        self.make_controlplot("v_pt",cut,tag,40,0, 800,xtitle="v_pt",ytitle="Events",logy=0 );
        self.make_controlplot("l_pt",cut,tag,30,0, 600,xtitle="l_pt",ytitle="Events",logy=0 );
        self.make_controlplot("l_eta",cut,tag,25,-2.5,2.5,xtitle="l_eta",ytitle="Events",logy=0 );
        self.make_controlplot("mvaMET",cut,tag,25,0,500,xtitle="mvaMET",ytitle="Events",logy=0 );
        self.make_controlplot("nPV",cut,tag,40,0,40,xtitle="nPV",ytitle="Events",logy=0 );
        self.make_controlplot("jet_tau2tau1",cut,tag,50,0,1,xtitle="jet_tau2tau1",ytitle="Events",logy=0 );
        self.make_controlplot("nbjets",cut,tag,5,-0.5,4.5,xtitle="number of b-jets",ytitle="Events",logy=0 );
        self.make_controlplot("njets",cut,tag,5,-0.5,4.5,xtitle="number of jets",ytitle="Events",logy=0 );
 
    ######## ++++++++++++++
    def make_controlplot(self,variable,cut,tag,nbin,min,max,xtitle="",ytitle="",logy=0 ):
        #weight_mc="totalEventWeight";
        weight_mc="totalEventWeight*%s"%(self.rrv_wtagger_eff_reweight.getVal());

        weightcut_mc="(%s)*(%s)"%(weight_mc,cut);
        weightcut_data="%s"%(cut);
        print "weightcut_mc="+weightcut_mc;
        hist_data =TH1D("hist_data","hist_data"+";%s;%s"%(xtitle,ytitle),nbin,min,max);
        hist_Signal =TH1D("hist_Signal","hist_Signal"+";%s;%s"%(xtitle,ytitle),nbin,min,max);
        hist_WJets=TH1D("hist_WJets","hist_WJets"+";%s;%s"%(xtitle,ytitle),nbin,min,max);
        hist_TTbar=TH1D("hist_TTbar","hist_TTbar"+";%s;%s"%(xtitle,ytitle),nbin,min,max);
        hist_STop =TH1D("hist_STop","hist_STop"+";%s;%s"%(xtitle,ytitle),nbin,min,max);
        hist_VV   =TH1D("hist_VV","hist_VV"+";%s;%s"%(xtitle,ytitle),nbin,min,max);
        hist_TotalMC =TH1D("hist_TotalMC","hist_TotalMC"+";%s;%s"%(xtitle,ytitle),nbin,min,max);

        hstack_TotalMC = THStack("hstack_TotalMC","hstack_TotalMC"+";%s;%s"%(xtitle,ytitle))
        hstack_TotalMC.Add(hist_STop);
        hstack_TotalMC.Add(hist_TTbar);
        hstack_TotalMC.Add(hist_VV);
        hstack_TotalMC.Add(hist_WJets); 

        hist_data.SetLineColor(self.color_palet["data"]); hist_data.SetFillColor(self.color_palet["data"]);
        hist_Signal.SetLineColor(self.color_palet["Signal"]); hist_Signal.SetFillColor(self.color_palet["Signal"]); hist_Signal.SetFillStyle(0);hist_Signal.SetLineWidth(2);
        hist_WJets.SetLineColor(self.color_palet["WJets"]); hist_WJets.SetFillColor(self.color_palet["WJets"]);
        hist_TTbar.SetLineColor(self.color_palet["TTbar"]); hist_TTbar.SetFillColor(self.color_palet["TTbar"]);
        hist_STop.SetLineColor(self.color_palet["STop"]); hist_STop.SetFillColor(self.color_palet["STop"]);
        hist_VV.SetLineColor(self.color_palet["VV"]); hist_VV.SetFillColor(self.color_palet["VV"]);

        tree_data =TChain("otree");  tree_data.Add(self.file_Directory+self.file_data);
        tree_Signal =TChain("otree");  tree_Signal.Add(self.file_Directory+self.file_ggH);
        tree_WJets =TChain("otree");tree_WJets.Add(self.file_Directory+self.file_WJets_mc);
        tree_TTbar =TChain("otree");tree_TTbar.Add(self.file_Directory+self.file_TTbar_mc);
        tree_STop =TChain("otree");  tree_STop.Add(self.file_Directory+self.file_STop_mc);
        tree_VV =TChain("otree");      tree_VV.Add(self.file_Directory+self.file_VV_mc);

        tree_data.Draw("%s >> hist_data"%(variable), weightcut_data);
        tree_Signal.Draw("%s >> hist_Signal"%(variable), weightcut_mc);
        tree_WJets.Draw("%s >> hist_WJets"%(variable), weightcut_mc);
        tree_TTbar.Draw("%s >> hist_TTbar"%(variable), weightcut_mc);
        tree_STop.Draw("%s >> hist_STop"%(variable), weightcut_mc);
        tree_VV.Draw("%s >> hist_VV"%(variable), weightcut_mc);

        hist_TotalMC.Add(hist_WJets); hist_TotalMC.Add(hist_TTbar); hist_TotalMC.Add(hist_STop); hist_TotalMC.Add(hist_VV);

        canvas_controlplot = TCanvas("canvas_controlplot","canvas_controlplot",1000,800);
        canvas_controlplot.cd();
        hist_data.GetYaxis().SetRangeUser(1e-2,TMath.Max(hist_data.GetMaximum(),hist_TotalMC.GetMaximum())*1.2);
        hist_data.Draw("e");
        hstack_TotalMC.Draw("HIST same");
        hist_data.Draw("same e");
        hist_Signal.Draw("same HIST");

        hist_data.GetXaxis().SetTitleOffset(1.1);
        hist_data.GetYaxis().SetTitleOffset(1.1);
        hist_data.GetXaxis().SetTitleSize(0.04);
        hist_data.GetYaxis().SetTitleSize(0.04);
        hist_data.GetXaxis().SetLabelSize(0.04);
        hist_data.GetYaxis().SetLabelSize(0.04);

        banner = TLatex(0.18,0.85,("#splitline{CMS Preliminary}{%.1f fb^{-1} at #sqrt{s}=8TeV %s+jets}"%(self.GetLumi(),self.channel)));
        banner.SetNDC(); banner.SetTextSize(0.025);
        banner.Draw();

        theLeg = TLegend(0.65, 0.57, 0.92, 0.87, "", "NDC");
        theLeg.SetName("theLegend"); theLeg.SetBorderSize(0); theLeg.SetLineColor(0); theLeg.SetFillColor(0);
        theLeg.SetFillStyle(0); theLeg.SetLineWidth(0); theLeg.SetLineStyle(0); theLeg.SetTextFont(42);
        theLeg.SetTextSize(.045);
        
        theLeg.AddEntry(hist_WJets, "WJets","F");
        theLeg.AddEntry(hist_TTbar, "TTbar","F");
        theLeg.AddEntry(hist_STop, "Single-T","F");
        theLeg.AddEntry(hist_VV, "VV","F");
        theLeg.AddEntry(hist_Signal, self.higgs_sample+" #times 50","L");
        theLeg.AddEntry(hist_data, "data","ep");
        theLeg.SetY1NDC(0.9 - 0.05*6 - 0.005);
        theLeg.SetY1(theLeg.GetY1NDC());
        theLeg.Draw();

        Directory=TString("plots_%s/controlplot_wtaggercut%s_nPV%sto%s/"%(self.channel, self.wtagger_cut, self.nPV_min, self.nPV_max)+self.higgs_sample+"/");
        if not Directory.EndsWith("/"):Directory=Directory.Append("/");
        if not os.path.isdir(Directory.Data()): os.system("mkdir -p  "+Directory.Data());

        rlt_file=TString(Directory.Data()+"controlplot_"+variable+"_"+tag+".png");
        canvas_controlplot.SaveAs(rlt_file.Data());
        rlt_file.ReplaceAll(".png",".eps"); 
        canvas_controlplot.SaveAs(rlt_file.Data());

        if logy:
            canvas_controlplot.SetLogy() ;
            canvas_controlplot.Update();
            rlt_file.ReplaceAll(".eps","_log.eps"); 
            canvas_controlplot.SaveAs(rlt_file.Data());
            rlt_file.ReplaceAll(".eps",".png"); 
            canvas_controlplot.SaveAs(rlt_file.Data());

    ######## ++++++++++++++
    def fit_mlvj_model_single_MC(self,in_file_name, label, in_range, in_model_name):# model = shape + normalization
        rrv_mass_lvj = self.workspace4fit_.var("rrv_mass_lvj") 
        rdataset = self.workspace4fit_.data("rdataset4fit"+label+in_range+"_"+self.channel+"_mlvj"); 
        model = self.make_Model(label+in_range,in_model_name,"_mlvj");
        model.fitTo( rdataset, RooFit.Save(1), RooFit.SumW2Error(kTRUE) ,RooFit.Extended(kTRUE) );
        rfresult = model.fitTo( rdataset, RooFit.Save(1), RooFit.SumW2Error(kTRUE) ,RooFit.Extended(kTRUE) );
        #rfresult = model.fitTo( rdataset, RooFit.Save(1),RooFit.Extended(kTRUE) );
        rfresult.SetName("rfresult"+label+in_range+"_"+self.channel+"_mlvj")
        getattr(self.workspace4fit_,"import")(rfresult)
        
        mplot = rrv_mass_lvj.frame(RooFit.Title("M_{lvj"+in_range+"} fitted by "+in_model_name));
        #if label=="_WJets": mplot.GetYaxis().SetRangeUser(1e-2,310);
        rdataset.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) );
        #model.plotOn(mplot,RooFit.VisualizeError(rfresult,1,kFALSE),RooFit.DrawOption("F"),RooFit.FillColor(kOrange), RooFit.VLines());
        #model.plotOn(mplot,RooFit.VisualizeError(rfresult,1),RooFit.FillColor(kOrange), RooFit.VLines());
        #draw_error_band(rdataset, model,self.workspace4fit_.var("rrv_number"+label+in_range+"_"+self.channel+"_mlvj") ,rfresult,mplot,6,"L")
        draw_error_band_extendPdf(rdataset, model, rfresult,mplot,6,"L")
        rdataset.plotOn( mplot ,RooFit.DataError(RooAbsData.SumW2) );
        model.plotOn( mplot , RooFit.VLines());

        if label=="_WJets":
            wsfit_tmp=RooWorkspace("wsfit_tmp"+label+in_range+"_"+self.channel+"_mlvj");
            Deco=PdfDiagonalizer("Deco"+label+in_range+"_"+self.channel+"_mlvj",wsfit_tmp,rfresult);
            model_deco=Deco.diagonalize(model);
            #rfresult.covarianceMatrix().Print(); 
            model_deco.Print("v");
            model_deco.getParameters(rdataset).Print("v");
            getattr(self.workspace4fit_,"import")(model_deco);

        #pull
        hpull=mplot.pullHist();
        mplot_pull = rrv_mass_lvj.frame(RooFit.Title("Pull Distribution"));
        mplot_pull.addPlotable(hpull,"P");
        mplot_pull.SetTitle("PULL");
        mplot_pull.GetYaxis().SetRangeUser(-5,5);
         
        parameters_list=model.getParameters(rdataset);
        mplot.GetYaxis().SetRangeUser(1e-2,mplot.GetMaximum()*1.1);
        self.draw_canvas( mplot, mplot_pull,parameters_list,"plots_%s/m_lvj_fitting/"%(self.channel), in_file_name,"m_lvj"+in_range+in_model_name)
        #rfresult.Print(); rfresult.covarianceMatrix().Print(); raw_input("ENTER");

        #normalize the number of total events to lumi
        #self.workspace4fit_.var("rrv_number"+label+in_range+"_"+self.channel+"_mlvj").Print()
        #self.workspace4fit_.var("rrv_scale_to_lumi"+label+"_"+self.channel).Print()

        print self.workspace4fit_.var("rrv_number"+label+in_range+"_"+self.channel+"_mlvj").getVal()
        print self.workspace4fit_.var("rrv_scale_to_lumi"+label+"_"+self.channel).getVal()
        self.workspace4fit_.var("rrv_number"+label+in_range+"_"+self.channel+"_mlvj").setVal( self.workspace4fit_.var("rrv_number"+label+in_range+"_"+self.channel+"_mlvj").getVal()*self.workspace4fit_.var("rrv_scale_to_lumi"+label+"_"+self.channel).getVal()  )
        self.workspace4fit_.var("rrv_number"+label+in_range+"_"+self.channel+"_mlvj").setError(self.workspace4fit_.var("rrv_number"+label+in_range+"_"+self.channel+"_mlvj").getError()*self.workspace4fit_.var("rrv_scale_to_lumi"+label+"_"+self.channel).getVal()  )
        if TString(label).Contains("ggH"):
            self.workspace4fit_.var("rrv_number"+label+in_range+"_"+self.channel+"_mlvj").setVal( self.workspace4fit_.var("rrv_number"+label+in_range+"_"+self.channel+"_mlvj").getVal()  )
            self.workspace4fit_.var("rrv_number"+label+in_range+"_"+self.channel+"_mlvj").setError(self.workspace4fit_.var("rrv_number"+label+in_range+"_"+self.channel+"_mlvj").getError()  )

    ######## ++++++++++++++
    def fit_WJetsNormalization_in_Mj_signal_region(self): # to  get the normalization of WJets in signal_region
        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j") 
        rdataset_data_mj=self.workspace4fit_.data("rdataset_data_%s_mj"%(self.channel))

        model_TTbar=self.get_TTbar_mj_Model();
        model_STop=self.get_STop_mj_Model();
        model_VV=self.get_VV_mj_Model();
        model_WJets=self.get_WJets_mj_Model();
        model_data=RooAddPdf("model_data_%s_mj"%(self.channel),"model_data_%s_mj"%(self.channel),RooArgList(model_WJets,model_VV,model_TTbar,model_STop));
        # fit the sideband range
        rfresult = model_data.fitTo( rdataset_data_mj, RooFit.Save(1) , RooFit.Range("sb_lo,sb_hi") ,RooFit.Extended(kTRUE) );
        rfresult = model_data.fitTo( rdataset_data_mj, RooFit.Save(1) , RooFit.Range("sb_lo,sb_hi") ,RooFit.Extended(kTRUE) );
        #rfresult = model_data.fitTo( rdataset_data_mj, RooFit.Save(1) , RooFit.Range("sb_lo,sb_hi") ,RooFit.Extended(kTRUE) );
        #rfresult = model_data.fitTo( rdataset_data_mj, RooFit.Save(1) , RooFit.Range("sb_lo,sb_hi") ,RooFit.Extended(kTRUE) );
        rfresult.Print();
        rfresult.covarianceMatrix().Print();
        getattr(self.workspace4fit_,"import")(model_data);

        rrv_number_data_mj=RooRealVar("rrv_number_data_%s_mj"%(self.channel),"rrv_number_data_%s_mj"%(self.channel), self.workspace4fit_.var("rrv_number_TTbar_%s_mj"%(self.channel)).getVal()+self.workspace4fit_.var("rrv_number_STop_%s_mj"%(self.channel)).getVal()+self.workspace4fit_.var("rrv_number_VV_%s_mj"%(self.channel)).getVal()+self.workspace4fit_.var("rrv_number_WJets_%s_mj"%(self.channel)).getVal() );
        rrv_number_data_mj.setError(self.workspace4fit_.var("rrv_number_TTbar_%s_mj"%(self.channel)).getError()+self.workspace4fit_.var("rrv_number_STop_%s_mj"%(self.channel)).getError()+self.workspace4fit_.var("rrv_number_VV_%s_mj"%(self.channel)).getError()+self.workspace4fit_.var("rrv_number_WJets_%s_mj"%(self.channel)).getError() );
        getattr(self.workspace4fit_,"import")(rrv_number_data_mj);
        scale_model_to_data=rrv_number_data_mj.getVal()/rdataset_data_mj.sumEntries();
        #print scale_model_to_data; raw_input("ENTER");
        
        mplot = rrv_mass_j.frame(RooFit.Title(""));
        rdataset_data_mj.plotOn(mplot, RooFit.Name("data_invisible"));
        #print "zixu1";raw_input("ENTER");

        model_data.plotOn(mplot,RooFit.Normalization(scale_model_to_data),RooFit.Name("VV"), RooFit.Components("model_WJets_%s_mj,model_STop_%s_mj,model_TTbar_%s_mj,model_VV_%s_mj"%(self.channel,self.channel,self.channel,self.channel)),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["VV"]), RooFit.LineColor(self.color_palet["VV"]),RooFit.NormRange("sb_lo,sb_hi"), RooFit.VLines());
        model_data.plotOn(mplot,RooFit.Normalization(scale_model_to_data),RooFit.Name("TTbar"), RooFit.Components("model_WJets_%s_mj,model_STop_%s_mj,model_TTbar_%s_mj"%(self.channel,self.channel,self.channel)),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["TTbar"]), RooFit.LineColor(self.color_palet["TTbar"]),RooFit.NormRange("sb_lo,sb_hi"), RooFit.VLines());
        model_data.plotOn(mplot,RooFit.Normalization(scale_model_to_data),RooFit.Name("STop"), RooFit.Components("model_WJets_%s_mj,model_STop_%s_mj"%(self.channel,self.channel)),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["STop"]), RooFit.LineColor(self.color_palet["STop"]),RooFit.NormRange("sb_lo,sb_hi"), RooFit.VLines());
        model_data.plotOn(mplot,RooFit.Normalization(scale_model_to_data),RooFit.Name("WJets"), RooFit.Components("model_WJets_%s_mj"%(self.channel)),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["WJets"]), RooFit.LineColor(self.color_palet["WJets"]),RooFit.NormRange("sb_lo,sb_hi"), RooFit.VLines());
        #print "zixu2";raw_input("ENTER");

        model_data.plotOn(mplot,RooFit.Normalization(scale_model_to_data),RooFit.Name("VV_invisible"), RooFit.Components("model_WJets_%s_mj,model_STop_%s_mj,model_TTbar_%s_mj,model_VV_%s_mj"%(self.channel,self.channel,self.channel,self.channel)),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["VV"]), RooFit.LineColor(self.color_palet["VV"]),RooFit.FillStyle(3003),RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()),RooFit.NormRange("sb_lo,sb_hi"), RooFit.VLines());
        model_data.plotOn(mplot,RooFit.Normalization(scale_model_to_data),RooFit.Name("TTbar_invisible"), RooFit.Components("model_WJets_%s_mj,model_STop_%s_mj,model_TTbar_%s_mj"%(self.channel,self.channel,self.channel)),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["TTbar"]), RooFit.LineColor(self.color_palet["TTbar"]),RooFit.FillStyle(3003),RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()),RooFit.NormRange("sb_lo,sb_hi"), RooFit.VLines());
        model_data.plotOn(mplot,RooFit.Normalization(scale_model_to_data),RooFit.Name("STop_invisible"), RooFit.Components("model_WJets_%s_mj,model_STop_%s_mj"%(self.channel,self.channel)),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["STop"]), RooFit.LineColor(self.color_palet["STop"]),RooFit.FillStyle(3003),RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()),RooFit.NormRange("sb_lo,sb_hi"), RooFit.VLines());
        model_data.plotOn(mplot,RooFit.Normalization(scale_model_to_data),RooFit.Name("WJets_invisible"), RooFit.Components("model_WJets_%s_mj"%(self.channel)),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["WJets"]),RooFit.FillStyle(3003),RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()), RooFit.LineColor(self.color_palet["WJets"]),RooFit.NormRange("sb_lo,sb_hi"), RooFit.VLines());

        #model_data.plotOn(mplot,RooFit.Normalization(scale_model_to_data),RooFit.Name("_invisible"),RooFit.VisualizeError(rfresult,1,kFALSE),RooFit.DrawOption("F"),RooFit.FillColor(self.color_palet["Uncertainty"]),RooFit.FillStyle(3013),RooFit.LineColor(self.color_palet["Uncertainty"]),RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()),RooFit.NormRange("sb_lo,sb_hi"), RooFit.VLines());
        #draw_error_band(rdataset_data_mj, model_data, rrv_number_data_mj,rfresult,mplot,6,"L");
        model_data.plotOn( mplot,RooFit.Normalization(scale_model_to_data),RooFit.Name("_invisible"), RooFit.Components("model_WJets_%s_mj"%(self.channel)), RooFit.LineColor(self.color_palet["WJets"]), RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()),RooFit.LineStyle(kDashed) ,RooFit.NormRange("sb_lo,sb_hi"), RooFit.VLines());
        model_data.plotOn( mplot,RooFit.Normalization(scale_model_to_data),RooFit.Name("_invisible"), RooFit.Components("model_WJets_%s_mj,model_STop_%s_mj"%(self.channel,self.channel)), RooFit.LineColor(self.color_palet["STop"]), RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()),RooFit.LineStyle(kDashed) ,RooFit.NormRange("sb_lo,sb_hi"), RooFit.VLines());
        model_data.plotOn( mplot,RooFit.Normalization(scale_model_to_data),RooFit.Name("_invisible"), RooFit.Components("model_WJets_%s_mj,model_STop_%s_mj,model_TTbar_%s_mj"%(self.channel,self.channel,self.channel)), RooFit.LineColor(self.color_palet["TTbar"]), RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()),RooFit.LineStyle(kDashed) ,RooFit.NormRange("sb_lo,sb_hi"), RooFit.VLines());
        model_data.plotOn( mplot,RooFit.Normalization(scale_model_to_data),RooFit.Name("_invisible"), RooFit.Components("model_WJets_%s_mj,model_STop_%s_mj,model_TTbar_%s_mj,model_VV_%s_mj"%(self.channel,self.channel,self.channel,self.channel)),RooFit.LineColor(self.color_palet["VV"]), RooFit.Range(rrv_mass_j.getMin(),rrv_mass_j.getMax()),RooFit.LineStyle(kDashed) ,RooFit.NormRange("sb_lo,sb_hi"), RooFit.VLines());
        draw_error_band(rdataset_data_mj, model_data, rrv_number_data_mj,rfresult,mplot,self.color_palet["Uncertainty"],"F");
        rdataset_data_mj.plotOn(mplot, RooFit.Name("data"));

        leg=self.legend4Plot(mplot,0);
        mplot.addObject(leg);

        #pull
        hpull=mplot.pullHist();
        mplot_pull = rrv_mass_j.frame(RooFit.Title("Pull Distribution"));
        mplot_pull.addPlotable(hpull,"P");
        mplot_pull.SetTitle("PULL");
        mplot_pull.GetYaxis().SetRangeUser(-5,5);
        #signal window
        lowerLine = TLine(self.mj_signal_min,0.,self.mj_signal_min,mplot.GetMaximum()); lowerLine.SetLineWidth(2); lowerLine.SetLineColor(kGray+2); lowerLine.SetLineStyle(9);
        upperLine = TLine(self.mj_signal_max,0.,self.mj_signal_max,mplot.GetMaximum()); upperLine.SetLineWidth(2); upperLine.SetLineColor(kGray+2); upperLine.SetLineStyle(9);
        mplot.addObject(lowerLine); mplot.addObject(upperLine);
        
        parameters_list=model_data.getParameters(rdataset_data_mj);
        mplot.GetYaxis().SetRangeUser(1e-2,mplot.GetMaximum()*1.1);
        self.draw_canvas( mplot, mplot_pull,parameters_list,"plots_%s/m_j_fitting_wtaggercut%s_nPV%sto%s/"%(self.channel, self.wtagger_cut, self.nPV_min, self.nPV_max), "m_j_sideband","",1)

        self.get_mj_normalization_insignalregion("_data");
        self.get_mj_normalization_insignalregion("_TTbar");
        self.get_mj_normalization_insignalregion("_STop");
        self.get_mj_normalization_insignalregion("_VV");
        self.get_mj_normalization_insignalregion("_WJets");

        # to calculate the WJets's normalization and error in M_J signal_region. The error must contain the shape error
        fullInt   = model_WJets.createIntegral(RooArgSet(rrv_mass_j),RooArgSet(rrv_mass_j) );
        signalInt = model_WJets.createIntegral(RooArgSet(rrv_mass_j),RooArgSet(rrv_mass_j),("signal_region"));
        fullInt_val=fullInt.getVal()
        signalInt_val=signalInt.getVal()/fullInt_val
        rrv_number_WJets_in_mj_signal_region_from_fitting=RooRealVar("rrv_number_WJets_in_mj_signal_region_%s_from_fitting"%(self.channel),"rrv_number_WJets_in_mj_signal_region_%s_from_fitting"%(self.channel),self.workspace4fit_.var("rrv_number_WJets_%s_mj"%(self.channel)).getVal()*signalInt_val);

        #error
        rrv_number_WJets_in_mj_signal_region_from_fitting.setError( Calc_error_extendPdf(rdataset_data_mj, model_WJets, rfresult) );
        print "error=%s"%(rrv_number_WJets_in_mj_signal_region_from_fitting.getError());
        getattr(self.workspace4fit_,"import")(rrv_number_WJets_in_mj_signal_region_from_fitting);
        rrv_number_WJets_in_mj_signal_region_from_fitting.Print();

    ######## ++++++++++++++
    def fit_mlvj_in_Mj_signal_region(self): # fix other background's model and  WJets normalization, floating WJets shape
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

        rfresult = model_data.fitTo( rdataset_data_signal_region_mlvj, RooFit.Save(1) ,RooFit.Extended(kTRUE) );
        getattr(self.workspace4fit_,"import")(model_data);
        self.fix_Model("_WJets","_signal_region","_mlvj");
        
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
    
        #pull
        hpull=mplot.pullHist();
        mplot_pull = rrv_mass_lvj.frame(RooFit.Title("Pull Distribution"));
        mplot_pull.addPlotable(hpull,"P");
        mplot_pull.SetTitle("PULL");
        mplot_pull.GetYaxis().SetRangeUser(-5,5);
    
        parameters_list=model_data.getParameters(rdataset_data_signal_region_mlvj);
        mplot.GetYaxis().SetRangeUser(1e-2,mplot.GetMaximum()*1.1);
        self.draw_canvas( mplot, mplot_pull,parameters_list,"plots_%s/m_lvj_fitting/"%(self.channel), "m_lvj_total","",1,1)

        self.get_mlvj_normalization_insignalregion("_%s"%(self.higgs_sample));
        self.get_mlvj_normalization_insignalregion("_TTbar");
        self.get_mlvj_normalization_insignalregion("_STop");
        self.get_mlvj_normalization_insignalregion("_VV");
        self.get_mlvj_normalization_insignalregion("_WJets");

        rfresult.Print();
    ######## ++++++++++++++
    def fit_mlvj_in_Mj_sideband(self, mlvj_region="_sb_lo"): 
        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j") 
        rrv_mass_lvj = self.workspace4fit_.var("rrv_mass_lvj") 
        rdataset_data_mlvj=self.workspace4fit_.data("rdataset_data%s_%s_mlvj"%(mlvj_region,self.channel))

        model_VV_backgrounds    = self.get_VV_mlvj_Model("_sb_lo");    number_VV_sb_lo_mlvj   =self.workspace4fit_.var("rrv_number_VV_sb_lo_%s_mlvj"%(self.channel))
        model_TTbar_backgrounds = self.get_TTbar_mlvj_Model("_sb_lo"); number_TTbar_sb_lo_mlvj=self.workspace4fit_.var("rrv_number_TTbar_sb_lo_%s_mlvj"%(self.channel))
        model_STop_backgrounds  = self.get_STop_mlvj_Model("_sb_lo");  number_STop_sb_lo_mlvj =self.workspace4fit_.var("rrv_number_STop_sb_lo_%s_mlvj"%(self.channel))

        model_pdf_WJets = self.make_Pdf("_WJets_sb_lo",self.model_4_mlvj,"_from_fitting_mlvj");model_pdf_WJets.Print();
        #model_pdf_WJets = self.make_Pdf("_WJets_sb_lo_from_fitting","EXO2011414","_mlvj");
        number_WJets_sb_lo=self.workspace4fit_.var("rrv_number_WJets_sb_lo_%s_mlvj"%(self.channel)).clone("rrv_number_WJets_sb_lo_%s_mlvj_from_fitting"%(self.channel));
        model_WJets=RooExtendPdf("model_WJets_sb_lo_%s_mlvj_from_fitting"%(self.channel),"model_WJets_sb_lo_%s_mlvj_from_fitting"%(self.channel),model_pdf_WJets,number_WJets_sb_lo);
        model_pdf_WJets.Print(); number_WJets_sb_lo.Print()
        #model_WJets.Print();raw_input("ENTER");

        model_data=RooAddPdf("model_data%s_mlvj"%(mlvj_region),"model_data%s_mlvj"%(mlvj_region),RooArgList(model_WJets,model_VV_backgrounds, model_TTbar_backgrounds, model_STop_backgrounds));
        rfresult = model_data.fitTo( rdataset_data_mlvj, RooFit.Save(1) ,RooFit.Extended(kTRUE) );
        rfresult = model_data.fitTo( rdataset_data_mlvj, RooFit.Save(1) ,RooFit.Extended(kTRUE) );
        getattr(self.workspace4fit_,"import")(model_data)
        rrv_number_data_sb_lo_mlvj=RooRealVar("rrv_number_data_sb_lo_%s_mlvj"%(self.channel),"rrv_number_data_sb_lo_%s_mlvj"%(self.channel), self.workspace4fit_.var("rrv_number_TTbar_sb_lo_%s_mlvj"%(self.channel)).getVal()+self.workspace4fit_.var("rrv_number_STop_sb_lo_%s_mlvj"%(self.channel)).getVal()+self.workspace4fit_.var("rrv_number_VV_sb_lo_%s_mlvj"%(self.channel)).getVal()+self.workspace4fit_.var("rrv_number_WJets_sb_lo_%s_mlvj_from_fitting"%(self.channel)).getVal() );
        rrv_number_data_sb_lo_mlvj.setError( TMath.Sqrt(
            self.workspace4fit_.var("rrv_number_WJets_sb_lo_%s_mlvj_from_fitting"%(self.channel)).getError()*self.workspace4fit_.var("rrv_number_WJets_sb_lo_%s_mlvj_from_fitting"%(self.channel)).getError() 
            #+self.workspace4fit_.var("rrv_number_TTbar_sb_lo_mlvj").getError()*self.workspace4fit_.var("rrv_number_TTbar_sb_lo_mlvj").getError()
            #+self.workspace4fit_.var("rrv_number_STop_sb_lo_mlvj").getError()*self.workspace4fit_.var("rrv_number_STop_sb_lo_mlvj").getError()
            #+self.workspace4fit_.var("rrv_number_VV_sb_lo_mlvj").getError()*self.workspace4fit_.var("rrv_number_VV_sb_lo_mlvj").getError() 
            ) );
        getattr(self.workspace4fit_,"import")(rrv_number_data_sb_lo_mlvj)
        #rdataset_data_mlvj.Print(); #rrv_number_data_sb_lo_mlvj.Print();# raw_input("ENTER");

        mplot = rrv_mass_lvj.frame(RooFit.Title("M_lvj fitted in M_j sideband "));
        rdataset_data_mlvj.plotOn( mplot , RooFit.Invisible());
        model_data.plotOn(mplot, RooFit.Components("model_WJets_sb_lo_%s_mlvj_from_fitting,model_TTbar_sb_lo_%s_mlvj,model_STop_sb_lo_%s_mlvj,model_VV_sb_lo_%s_mlvj"%(self.channel,self.channel,self.channel,self.channel)), RooFit.Name("WJets"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["WJets"]), RooFit.LineColor(self.color_palet["WJets"]), RooFit.VLines()) ;
        model_data.plotOn(mplot, RooFit.Components("model_TTbar_sb_lo_%s_mlvj,model_STop_sb_lo_%s_mlvj,model_VV_sb_lo_%s_mlvj"%(self.channel,self.channel,self.channel)), RooFit.Name("TTbar"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["TTbar"]), RooFit.LineColor(self.color_palet["TTbar"]), RooFit.VLines());
        model_data.plotOn(mplot, RooFit.Components("model_STop_sb_lo_%s_mlvj,model_VV_sb_lo_%s_mlvj"%(self.channel,self.channel)), RooFit.Name("STop"), RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["STop"]), RooFit.LineColor(self.color_palet["STop"]), RooFit.VLines());
        model_data.plotOn(mplot, RooFit.Components("model_VV_sb_lo_%s_mlvj"%(self.channel)),RooFit.Name("VV"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["VV"]), RooFit.LineColor(self.color_palet["VV"]), RooFit.VLines()) ;
        rdataset_data_mlvj.plotOn(mplot,RooFit.Name("data"));
        #model_data.plotOn(mplot,RooFit.VisualizeError(rfresult,1), RooFit.Name("Uncertainty"),RooFit.FillColor(self.color_palet["Uncertainty"]),RooFit.FillStyle(3013),RooFit.LineColor(self.color_palet["Uncertainty"]), RooFit.VLines(), RooFit.Invisible());#use draw_error_band to replace the roofit default algorithm
        draw_error_band(rdataset_data_mlvj, model_data,self.workspace4fit_.var("rrv_number_data_sb_lo_%s_mlvj"%(self.channel)) ,rfresult,mplot,self.color_palet["Uncertainty"],"F");
        model_data.plotOn( mplot , RooFit.VLines(), RooFit.Invisible());
        rdataset_data_mlvj.plotOn(mplot,RooFit.Name("data_invisible1"));

        leg=self.legend4Plot(mplot,0);#add legend
        mplot.addObject(leg)

        #chi2
        nPar_float_in_fitTo=rfresult.floatParsFinal().getSize();
        nBinX=mplot.GetNbinsX();
        ndof= nBinX-nPar_float_in_fitTo;
        print mplot.chiSquare();
        print "nPar=%s,  chiSquare=%s/%s"%(nPar_float_in_fitTo ,mplot.chiSquare(nPar_float_in_fitTo)*ndof, ndof ); #raw_input("ENTER");
        self.file_out.write("\n fit_mlvj_in_Mj_sideband: nPar=%s, chiSquare=%s/%s"%(nPar_float_in_fitTo, mplot.chiSquare( nPar_float_in_fitTo )*ndof, ndof ) );
    
        #pull
        hpull=mplot.pullHist();
        mplot_pull = rrv_mass_lvj.frame(RooFit.Title("Pull Distribution"));
        mplot_pull.addPlotable(hpull,"P");
        mplot_pull.SetTitle("PULL");
        mplot_pull.GetYaxis().SetRangeUser(-5,5);
    
        parameters_list=model_data.getParameters(rdataset_data_mlvj);
        mplot.GetYaxis().SetRangeUser(1e-2,mplot.GetMaximum()*1.1)
        self.draw_canvas( mplot, mplot_pull,parameters_list,"plots_%s/m_lvj_fitting/"%(self.channel), "m_lvj_sb_lo","",1,1)

        #model deco
        wsfit_tmp=RooWorkspace("wsfit_tmp_WJets_sb_lo_from_fitting_mlvj");
        Deco=PdfDiagonalizer("Deco_WJets_sb_lo_%s_from_fitting_mlvj"%(self.channel),wsfit_tmp,rfresult);
        model_pdf_WJets_deco=Deco.diagonalize(model_pdf_WJets); model_pdf_WJets_deco.Print("v");
        model_pdf_WJets_deco.getParameters(rdataset_data_mlvj).Print("") ;wsfit_tmp.allVars().Print("v");
        getattr(self.workspace4fit_,"import")(model_pdf_WJets_deco);

        self.get_WJets_mlvj_correction_sb_lo_to_signal_region()

        self.fix_Model("_%s"%(self.higgs_sample),"_signal_region","_mlvj")
        self.fix_Model("_TTbar","_signal_region","_mlvj")
        self.fix_Model("_STop","_signal_region","_mlvj")
        self.fix_Model("_VV","_signal_region","_mlvj")

        self.get_mlvj_normalization_insignalregion("_%s"%(self.higgs_sample));
        self.get_mlvj_normalization_insignalregion("_TTbar");
        self.get_mlvj_normalization_insignalregion("_STop");
        self.get_mlvj_normalization_insignalregion("_VV");
        self.get_mlvj_normalization_insignalregion("_WJets","model_pdf_WJets_signal_region_%s_after_correct_mlvj"%(self.channel));
        rfresult.Print();

    ######## ++++++++++++++
    def fit_mlvj_in_Mj_signal_region_for_sideband_correction_method3(self): # fix other background's model and  WJets normalization, floating WJets shape
        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j") 
        rrv_mass_lvj = self.workspace4fit_.var("rrv_mass_lvj") 
        rdataset_data_signal_region_mlvj=self.workspace4fit_.data("rdataset_data_signal_region_mlvj")
        print "N_rdataset: ", rdataset_data_signal_region_mlvj.Print();
        self.file_out.write("\ndata_obs event number: %s\n"%(rdataset_data_signal_region_mlvj.sumEntries()) )

        model_ggH   = self.get_ggH_mlvj_Model("_signal_region");
        model_TTbar   = self.get_TTbar_mlvj_Model("_signal_region");
        model_STop   = self.get_STop_mlvj_Model("_signal_region");
        model_VV    = self.get_VV_mlvj_Model("_signal_region");
        model_pdf_WJets = self.workspace4fit_.pdf("model_pdf_WJets_signal_region_%s_after_correct_mlvj"%(self.channel));
        number_WJets = self.workspace4fit_.var("rrv_number_WJets_signal_region_mlvj");
        number_WJets.setConstant(kFALSE);
        number_WJets.setRange(number_WJets.getVal()/3., number_WJets.getVal()*3.);
        model_WJets=RooExtendPdf("model_WJets_signal_region_after_correct_mlvj","model_WJets_signal_region_after_correct_mlvj",model_pdf_WJets,number_WJets);
        getattr(self.workspace4fit_,"import")(model_WJets);
        #model_TTbar.Print(); model_STop.Print(); model_VV.Print(); model_WJets.Print(); #raw_input("ENTER");
       
        model_data=RooAddPdf("model_data_signal_region_mlvj","model_data_signal_region_mlvj",RooArgList(model_WJets,model_VV,model_TTbar,model_STop));

        rfresult = model_data.fitTo( rdataset_data_signal_region_mlvj, RooFit.Save(1) ,RooFit.Extended(kTRUE) );
        
        mplot = rrv_mass_lvj.frame(RooFit.Title("Closure test: WJets+TTbar+STop+VV"));
        rdataset_data_signal_region_mlvj.plotOn( mplot, RooFit.Invisible() );
        model_data.plotOn(mplot, RooFit.Components("%s,%s,%s,%s"%(model_WJets.GetName(),model_VV.GetName(),model_TTbar.GetName(),model_STop.GetName() )), RooFit.Name("WJets"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["WJets"]), RooFit.LineColor(self.color_palet["WJets"]), RooFit.VLines()) ;
        model_data.plotOn(mplot, RooFit.Components("%s,%s,%s"%(model_VV.GetName(),model_TTbar.GetName(),model_STop.GetName() )), RooFit.Name("VV"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["VV"]), RooFit.LineColor(self.color_palet["VV"]), RooFit.VLines()) ;
        model_data.plotOn(mplot, RooFit.Components("%s,%s"%(model_TTbar.GetName(),model_STop.GetName() )), RooFit.Name("TTbar"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["TTbar"]), RooFit.LineColor(self.color_palet["TTbar"]), RooFit.VLines()) ;
        model_data.plotOn(mplot, RooFit.Components("%s"%(model_STop.GetName() )), RooFit.Name("STop"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["STop"]), RooFit.LineColor(self.color_palet["STop"]), RooFit.VLines()) ;
        #draw_error_band(rdataset_data_signal_region_mlvj, model_data, rrv_number_data_signal_region_mlvj ,rfresult,mplot,6,"F");
        model_data.plotOn(mplot, RooFit.Components("%s,%s,%s,%s"%(model_WJets.GetName(),model_VV.GetName(),model_TTbar.GetName(),model_STop.GetName() )), RooFit.Name("Total_invisible"), RooFit.LineColor(self.color_palet["WJets"]),RooFit.Invisible(), RooFit.VLines() ) ;
        rdataset_data_signal_region_mlvj.plotOn( mplot, RooFit.Name("data") );

        #chi2
        nPar_float_in_fitTo=rfresult.floatParsFinal().getSize();
        nBinX=mplot.GetNbinsX();
        ndof= nBinX-nPar_float_in_fitTo; 
        print "nPar=%s,  chiSquare=%s/%s"%(nPar_float_in_fitTo,  mplot.chiSquare(nPar_float_in_fitTo)*ndof, ndof ); #raw_input("ENTER");
        self.file_out.write("\n fit_mlvj_in_Mj_signal_region_for_sideband_correction_method3: nPar=%s, chiSquare=%s/%s"%(nPar_float_in_fitTo, mplot.chiSquare(nPar_float_in_fitTo)*ndof, ndof ) );
   
        #pull
        hpull=mplot.pullHist();
        mplot_pull = rrv_mass_lvj.frame(RooFit.Title("Pull Distribution"));
        mplot_pull.addPlotable(hpull,"P");
        mplot_pull.SetTitle("PULL");
        mplot_pull.GetYaxis().SetRangeUser(-5,5);
    
        parameters_list_orig=model_data.getParameters(rdataset_data_signal_region_mlvj);
        parameters_list=RooArgList();
        par=parameters_list_orig.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            if not param.isConstant(): parameters_list.add(param);
            param=par.Next();
        mplot.GetYaxis().SetRangeUser(1e-2,mplot.GetMaximum()*1.1);
        self.draw_canvas( mplot, mplot_pull,parameters_list,"plots_%s/m_lvj_fitting/"%(self.channel), "m_lvj_total","",1,1);

        #self.get_mlvj_normalization_insignalregion("_%s"%(self.higgs_sample));
        #self.get_mlvj_normalization_insignalregion("_TTbar");
        #self.get_mlvj_normalization_insignalregion("_STop");
        #self.get_mlvj_normalization_insignalregion("_VV");
        self.get_mlvj_normalization_insignalregion("_WJets","model_pdf_WJets_signal_region_%s_after_correct_mlvj"%(self.channel));

        rfresult.Print();

    ######## ++++++++++++++
    def fit_simultaneous_mlvj_in_Mj_signal_region_and_sideband(self, mlvj_region="_sb_lo"): # fix other background's model and  WJets normalization, floating WJets shape
        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j") 
        rrv_mass_lvj = self.workspace4fit_.var("rrv_mass_lvj") 
        rdataset_data_sideband_mlvj=self.workspace4fit_.data("rdataset_data%s_mlvj"%(mlvj_region));
        rdataset_data_signal_region_mlvj=self.workspace4fit_.data("rdataset_data_signal_region_mlvj");
        rdataset_data_sideband_mlvj.Print();
        rdataset_data_signal_region_mlvj.Print();

        model_VV_sideband    = self.get_VV_mlvj_Model("_sb_lo"); number_VV_sb_lo_mlvj=self.workspace4fit_.var("rrv_number_VV_sb_lo_mlvj")
        model_TTbar_sideband    = self.get_TTbar_mlvj_Model("_sb_lo"); number_TTbar_sb_lo_mlvj=self.workspace4fit_.var("rrv_number_TTbar_sb_lo_mlvj")
        model_STop_sideband    = self.get_STop_mlvj_Model("_sb_lo"); number_STop_sb_lo_mlvj=self.workspace4fit_.var("rrv_number_STop_sb_lo_mlvj")

        model_ggH_signal_region   = self.get_ggH_mlvj_Model("_signal_region");
        model_TTbar_signal_region   = self.get_TTbar_mlvj_Model("_signal_region");
        model_STop_signal_region   = self.get_STop_mlvj_Model("_signal_region");
        model_VV_signal_region    = self.get_VV_mlvj_Model("_signal_region");

        model_sb_lo_WJets=self.workspace4fit_.pdf("model_pdf_WJets_sb_lo_mlvj_Deco_WJets_sb_lo_%s_mlvj"%(self.channel));
        model_signal_region_WJets=self.workspace4fit_.pdf("model_pdf_WJets_signal_region_mlvj_Deco_WJets_signal_region_%s_mlvj"%(self.channel));
        self.fix_Pdf(model_sb_lo_WJets,RooArgSet(rrv_mass_lvj));
        self.fix_Pdf(model_signal_region_WJets,RooArgSet(rrv_mass_lvj));

        #model_pdf_WJets_sideband = self.make_Pdf("_WJets_sb_lo_from_fitting","ErfExp_v1","_mlvj");
        model_pdf_WJets_sideband = self.make_Pdf("_WJets_sb_lo_from_fitting",self.model_4_mlvj,"_mlvj");model_pdf_WJets_sideband.Print();
        number_WJets_sb_lo=self.workspace4fit_.var("rrv_number_WJets_sb_lo_mlvj").clone("rrv_number_WJets_sb_lo_mlvj_from_fitting");
        model_WJets_sideband=RooExtendPdf("model_WJets_sb_lo_%s_mlvj_from_fitting","model_WJets_sb_lo_%s_mlvj_from_fitting",model_pdf_WJets_sideband,number_WJets_sb_lo)
         
        if self.model_4_mlvj=="ErfExp_v1":
            #print "ErfExp_v1"; raw_input("ENTER");
            correct_factor_pdf = RooAlpha("correct_factor_pdf","correct_factor_pdf",rrv_mass_lvj,
                    self.workspace4fit_.function("Deco_WJets_signal_region_%s_mlvj_eigLin_0"%(self.channel)),
                    self.workspace4fit_.function("Deco_WJets_signal_region_%s_mlvj_eigLin_2"%(self.channel)),
                    self.workspace4fit_.function("Deco_WJets_signal_region_%s_mlvj_eigLin_3"%(self.channel)),
                    self.workspace4fit_.function("Deco_WJets_sb_lo_%s_mlvj_eigLin_0"%(self.channel)),
                    self.workspace4fit_.function("Deco_WJets_sb_lo_%s_mlvj_eigLin_2"%(self.channel)),
                    self.workspace4fit_.function("Deco_WJets_sb_lo_%s_mlvj_eigLin_3"%(self.channel)),
                    rrv_mass_lvj.getMin(),rrv_mass_lvj.getMax());
            getattr(self.workspace4fit_,"import")(correct_factor_pdf);
            mplot_alpha=rrv_mass_lvj.frame(RooFit.Title("Alpha"));
            correct_factor_pdf.plotOn(mplot_alpha);
            model_sb_lo_WJets.plotOn(mplot_alpha);
            model_signal_region_WJets.plotOn(mplot_alpha, RooFit.LineColor(kRed) );
            self.draw_canvas1(mplot_alpha,"plots_%s/other/"%(self.channel),"correction_pdf_WJets_M_lvj_signal_region_to_sideband",0,0);

            correct_factor=RooFormulaVar("correct_factor", "(TMath::Exp(@1*@0)*(1.+TMath::Erf((@0-@2)/@3))/2.)/(TMath::Exp(@4*@0)*(1.+TMath::Erf((@0-@5)/@6))/2.)",RooArgList(
                rrv_mass_lvj,
                self.workspace4fit_.function("Deco_WJets_signal_region_%s_mlvj_eigLin_0"%(self.channel)),
                self.workspace4fit_.function("Deco_WJets_signal_region_%s_mlvj_eigLin_2"%(self.channel)),
                self.workspace4fit_.function("Deco_WJets_signal_region_%s_mlvj_eigLin_3"%(self.channel)),
                self.workspace4fit_.function("Deco_WJets_sb_lo_%s_mlvj_eigLin_0"%(self.channel)),
                self.workspace4fit_.function("Deco_WJets_sb_lo_%s_mlvj_eigLin_2"%(self.channel)),
                self.workspace4fit_.function("Deco_WJets_sb_lo_%s_mlvj_eigLin_3"%(self.channel)),
                ))

            #model_pdf_WJets_signal_region=RooProdPdf("model_pdf_WJets_signal_region_%s_after_correct_mlvj"%(self.channel),"model_pdf_WJets_signal_region_%s_after_correct_mlvj"%(self.channel),model_pdf_WJets_sideband,self.workspace4fit_.pdf("correct_factor_pdf"));
            model_pdf_WJets_signal_region = RooEffProd("model_pdf_WJets_signal_region_%s_after_correct_mlvj"%(self.channel),"model_pdf_WJets_signal_region_%s_after_correct_mlvj"%(self.channel),model_pdf_WJets_sideband,correct_factor)
        if self.model_4_mlvj=="Exp":
            #print "Exp"; raw_input("ENTER");

            delta_c=RooFormulaVar("delta_c", "@0-@1",RooArgList( self.workspace4fit_.function("Deco_WJets_signal_region_%s_mlvj_eigLin_0"%(self.channel)), self.workspace4fit_.function("Deco_WJets_sb_lo_%s_mlvj_eigLin_0"%(self.channel))));
            c_sideband=self.workspace4fit_.var("rrv_c_Exp_WJets_sb_lo_from_fitting");
            c_signal_region=RooFormulaVar("c_signal_region", "@0+@1",RooArgList(delta_c, c_sideband)) ;

            correct_factor_pdf = RooExponential("correct_factor_pdf","correct_factor_pdf",rrv_mass_lvj,delta_c);
            mplot_alpha=rrv_mass_lvj.frame(RooFit.Title("Alpha"));
            correct_factor_pdf.plotOn(mplot_alpha);
            model_sb_lo_WJets.plotOn(mplot_alpha);
            model_signal_region_WJets.plotOn(mplot_alpha, RooFit.LineColor(kRed) );
            self.draw_canvas1(mplot_alpha,"plots_%s/other/"%(self.channel),"correction_pdf_WJets_M_lvj_signal_region_to_sideband",0,0);

            model_pdf_WJets_signal_region = RooExponential("model_pdf_WJets_signal_region_%s_after_correct_mlvj"%(self.channel),"model_pdf_WJets_signal_region_%s_after_correct_mlvj"%(self.channel),rrv_mass_lvj,c_signal_region);
        number_WJets = self.workspace4fit_.var("rrv_number_WJets_signal_region_mlvj");
        number_WJets.setConstant(kFALSE);
        number_WJets.setRange(number_WJets.getVal()/3., number_WJets.getVal()*30.);
        #number_WJets.Print();raw_input("ENTER");
        model_WJets_signal_region=RooExtendPdf("model_WJets_signal_region_after_correct_mlvj","model_WJets_signal_region_after_correct_mlvj",model_pdf_WJets_signal_region,number_WJets);
        model_WJets_signal_region.getParameters(rdataset_data_signal_region_mlvj).Print("v");
 
        model_data_sideband=RooAddPdf("model_data%s_mlvj"%(mlvj_region),"model_data%s_mlvj"%(mlvj_region),RooArgList(model_WJets_sideband,model_VV_sideband, model_TTbar_sideband, model_STop_sideband));
        model_data_signal_region=RooAddPdf("model_data_signal_region_mlvj","model_data_signal_region_mlvj",RooArgList(model_WJets_signal_region,model_VV_signal_region,model_TTbar_signal_region,model_STop_signal_region));

        data_category=RooCategory("data_category","data_category");
        data_category.defineType("sideband");
        data_category.defineType("signal_region");
        #combData=RooDataSet("combData","combData",RooArgSet(rrv_mass_lvj),RooFit.Index(data_category),RooFit.Import("sideband",rdataset_data_sideband_mlvj ),RooFit.Import("signal_region",rdataset_data_signal_region_mlvj) );
        combData=self.workspace4fit_.data("combData_data");
        #combData.Print();raw_input("ENTER");
        simPdf=RooSimultaneous("simPdf","simPdf",data_category);
        simPdf.addPdf(model_data_sideband,"sideband");
        simPdf.addPdf(model_data_signal_region,"signal_region");

        model_data_sideband.fitTo(rdataset_data_sideband_mlvj ,RooFit.Extended(kTRUE),RooFit.Save(kTRUE),RooFit.SumW2Error(kFALSE)).Print();
        model_data_signal_region.fitTo(rdataset_data_signal_region_mlvj ,RooFit.Extended(kTRUE),RooFit.Save(kTRUE),RooFit.SumW2Error(kFALSE)).Print();
        rfresult=simPdf.fitTo(combData,RooFit.Save(kTRUE),RooFit.Extended(kTRUE)); rfresult.Print();
        rfresult.covarianceMatrix().Print();

        #deco
        wsfit_tmp=RooWorkspace("wsfit_tmp_data");
        Deco=PdfDiagonalizer("Deco_data_signal_region_mlvj",wsfit_tmp,rfresult);
        model_WJets_signal_region_deco=Deco.diagonalize(model_WJets_signal_region);
        model_WJets_signal_region_deco.Print("v");
        #self.fix_Pdf(model_WJets_signal_region,RooArgSet(rrv_mass_lvj));
        self.fix_Pdf(model_WJets_signal_region_deco,RooArgSet(rrv_mass_lvj));
        #getattr(self.workspace4fit_,"import")(model_WJets_signal_region);
        getattr(self.workspace4fit_,"import")(model_WJets_signal_region_deco);

        mplot_sideband = rrv_mass_lvj.frame(RooFit.Title("M_lvj fitted in M_j sideband "));
        rdataset_data_sideband_mlvj.plotOn( mplot_sideband , RooFit.Invisible());
        model_data_sideband.plotOn(mplot_sideband, RooFit.Components("model_WJets_sb_lo_%s_mlvj_from_fitting,model_TTbar_sb_lo_%s_mlvj,model_STop_sb_lo_%s_mlvj,model_VV_sb_lo_%s_mlvj"), RooFit.Name("WJets"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["WJets"]), RooFit.LineColor(self.color_palet["WJets"]), RooFit.VLines()) ;
        model_data_sideband.plotOn(mplot_sideband, RooFit.Components("model_TTbar_sb_lo_%s_mlvj,model_STop_sb_lo_%s_mlvj,model_VV_sb_lo_%s_mlvj"), RooFit.Name("TTbar"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["TTbar"]), RooFit.LineColor(self.color_palet["TTbar"]), RooFit.VLines());
        model_data_sideband.plotOn(mplot_sideband, RooFit.Components("model_STop_sb_lo_%s_mlvj,model_VV_sb_lo_%s_mlvj"), RooFit.Name("STop"), RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["STop"]), RooFit.LineColor(self.color_palet["STop"]), RooFit.VLines());
        model_data_sideband.plotOn(mplot_sideband, RooFit.Components("model_VV_sb_lo_%s_mlvj"),RooFit.Name("VV"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["VV"]), RooFit.LineColor(self.color_palet["VV"]), RooFit.VLines()) ;
        rdataset_data_sideband_mlvj.plotOn(mplot_sideband,RooFit.Name("data"));
        model_data_sideband.plotOn( mplot_sideband , RooFit.VLines(), RooFit.Invisible());
        rdataset_data_sideband_mlvj.plotOn(mplot_sideband,RooFit.Name("data_invisible1"));

        leg=self.legend4Plot(mplot_sideband,0);#add legend
        mplot_sideband.addObject(leg)
    
        #pull
        hpull=mplot_sideband.pullHist();
        mplot_pull_sideband = rrv_mass_lvj.frame(RooFit.Title("Pull Distribution"));
        mplot_pull_sideband.addPlotable(hpull,"P");
        mplot_pull_sideband.SetTitle("PULL");
        mplot_pull_sideband.GetYaxis().SetRangeUser(-5,5);
    
        parameters_list=model_data_sideband.getParameters(rdataset_data_sideband_mlvj);
        mplot.GetYaxis().SetRangeUser(1e-2,mplot.GetMaximum()*1.1);
        self.draw_canvas( mplot_sideband, mplot_pull_sideband,parameters_list,"plots_%s/m_lvj_fitting/"%(self.channel), "m_lvj_sb_lo","",1,1)

        print "N_rdataset: ", rdataset_data_signal_region_mlvj.Print();
        self.file_out.write("\ndata_obs event number: %s\n"%(rdataset_data_signal_region_mlvj.sumEntries()) )

        mplot_signal_region = rrv_mass_lvj.frame(RooFit.Title("Signal Region"));
        rdataset_data_signal_region_mlvj.plotOn( mplot_signal_region, RooFit.Invisible() );
        model_data_signal_region.plotOn(mplot_signal_region, RooFit.Components("%s,%s,%s,%s"%(model_WJets_signal_region.GetName(),model_VV_signal_region.GetName(),model_TTbar_signal_region.GetName(),model_STop_signal_region.GetName() )), RooFit.Name("WJets"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["WJets"]), RooFit.LineColor(self.color_palet["WJets"]), RooFit.VLines()) ;
        model_data_signal_region.plotOn(mplot_signal_region, RooFit.Components("%s,%s,%s"%(model_VV_signal_region.GetName(),model_TTbar_signal_region.GetName(),model_STop_signal_region.GetName() )), RooFit.Name("VV"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["VV"]), RooFit.LineColor(self.color_palet["VV"]), RooFit.VLines()) ;
        model_data_signal_region.plotOn(mplot_signal_region, RooFit.Components("%s,%s"%(model_TTbar_signal_region.GetName(),model_STop_signal_region.GetName() )), RooFit.Name("TTbar"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["TTbar"]), RooFit.LineColor(self.color_palet["TTbar"]), RooFit.VLines()) ;
        model_data_signal_region.plotOn(mplot_signal_region, RooFit.Components("%s"%(model_STop_signal_region.GetName() )), RooFit.Name("STop"),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["STop"]), RooFit.LineColor(self.color_palet["STop"]), RooFit.VLines()) ;
        #model_data_signal_region.plotOn(mplot_signal_region,RooFit.VisualizeError(rfresult,1),RooFit.FillColor(kOrange), RooFit.VLines());
        #draw_error_band(rdataset_data_signal_region_mlvj, model_data_signal_region, rrv_number_data_signal_region_mlvj ,rfresult,mplot_signal_region,6,"F");
        model_data_signal_region.plotOn(mplot_signal_region, RooFit.Components("%s,%s,%s,%s"%(model_WJets_signal_region.GetName(),model_VV_signal_region.GetName(),model_TTbar_signal_region.GetName(),model_STop_signal_region.GetName() )), RooFit.Name("Total_invisible"), RooFit.LineColor(self.color_palet["WJets"]),RooFit.Invisible(), RooFit.VLines() ) ;
        rdataset_data_signal_region_mlvj.plotOn( mplot_signal_region, RooFit.Name("data") );

        #pull
        hpull=mplot_signal_region.pullHist();
        mplot_pull_signal_region = rrv_mass_lvj.frame(RooFit.Title("Pull Distribution"));
        mplot_pull_signal_region.addPlotable(hpull,"P");
        mplot_pull_signal_region.SetTitle("PULL");
        mplot_pull_signal_region.GetYaxis().SetRangeUser(-5,5);
    
        parameters_list_orig=model_data_signal_region.getParameters(rdataset_data_signal_region_mlvj);
        parameters_list=RooArgList();
        par=parameters_list_orig.createIterator();
        par.Reset();
        param=par.Next()
        while (param):
            if not param.isConstant(): parameters_list.add(param);
            param=par.Next();
        mplot_signal_region.GetYaxis().SetRangeUser(1e-2,mplot.GetMaximum()*1.1);
        self.draw_canvas( mplot_signal_region, mplot_pull_signal_region,parameters_list,"plots_%s/m_lvj_fitting/"%(self.channel), "m_lvj_total","",1,1);

        self.fix_Model("_%s"%(self.higgs_sample),"_signal_region","_mlvj")
        self.fix_Model("_TTbar","_signal_region","_mlvj")
        self.fix_Model("_STop","_signal_region","_mlvj")
        self.fix_Model("_VV","_signal_region","_mlvj")

        self.get_mlvj_normalization_insignalregion("_%s"%(self.higgs_sample));
        self.get_mlvj_normalization_insignalregion("_TTbar");
        self.get_mlvj_normalization_insignalregion("_STop");
        self.get_mlvj_normalization_insignalregion("_VV");
        #self.get_mlvj_normalization_insignalregion("_WJets","model_pdf_WJets_signal_region_%s_after_correct_mlvj"%(self.channel));
        self.get_mlvj_normalization_insignalregion("_WJets","model_pdf_WJets_signal_region_after_correct_mlvj_Deco_data_signal_region_mlvj");

    ######## ++++++++++++++
    def get_mj_normalization_insignalregion(self, label):
        print "get mj normalization "+ label
        model = self.workspace4fit_.pdf("model"+label+"_"+self.channel+"_mj");
        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j");

        fullInt   = model.createIntegral(RooArgSet(rrv_mass_j),RooArgSet(rrv_mass_j) );
        sb_loInt   = model.createIntegral(RooArgSet(rrv_mass_j),RooArgSet(rrv_mass_j),("sb_lo"));
        signalInt = model.createIntegral(RooArgSet(rrv_mass_j),RooArgSet(rrv_mass_j),("signal_region"));
        sb_hiInt   = model.createIntegral(RooArgSet(rrv_mass_j),RooArgSet(rrv_mass_j),("sb_hi"));
        
        fullInt_val=fullInt.getVal()
        sb_loInt_val=sb_loInt.getVal()/fullInt_val
        sb_hiInt_val=sb_hiInt.getVal()/fullInt_val
        signalInt_val=signalInt.getVal()/fullInt_val

        print "Events Number in MC Dataset:"
        self.workspace4fit_.var("rrv_number_dataset_sb_lo"+label+"_"+self.channel+"_mj").Print();
        self.workspace4fit_.var("rrv_number_dataset_signal_region"+label+"_"+self.channel+"_mj").Print();
        self.workspace4fit_.var("rrv_number_dataset_sb_hi"+label+"_"+self.channel+"_mj").Print();

        print "Events Number get from fit:"
        rrv_tmp=self.workspace4fit_.var("rrv_number"+label+"_"+self.channel+"_mj");
        rrv_tmp.Print();
        print "Events Number in sideband_low :%s"%(rrv_tmp.getVal()*sb_loInt_val)
        print "Events Number in Signal Region:%s"%(rrv_tmp.getVal()*signalInt_val)
        print "Events Number in sideband_high:%s"%(rrv_tmp.getVal()*sb_hiInt_val)
        print "Total Number in sidebands     :%s"%(rrv_tmp.getVal()*(sb_loInt_val+sb_hiInt_val)  )
        print "Ratio signal_region/sidebands        :%s"%(signalInt_val/(sb_loInt_val+sb_hiInt_val)  )

        #save to file
        self.file_out.write( "\n%s++++++++++++++++++++++++++++++++++++"%(label) )
        self.file_out.write( "\nEvents Number in sideband_low  from dataset:%s"%(self.workspace4fit_.var("rrv_number_dataset_sb_lo"+label+"_"+self.channel+"_mj").getVal() ) )
        self.file_out.write( "\nEvents Number in Signal Region from dataset:%s"%(self.workspace4fit_.var("rrv_number_dataset_signal_region"+label+"_"+self.channel+"_mj").getVal() ) )
        self.file_out.write( "\nEvents Number in sideband_high from dataset:%s"%(self.workspace4fit_.var("rrv_number_dataset_sb_hi"+label+"_"+self.channel+"_mj").getVal() ) )
        self.file_out.write( "\nTotal  Number in sidebands     from dataset:%s"%(self.workspace4fit_.var("rrv_number_dataset_sb_lo"+label+"_"+self.channel+"_mj").getVal()+ self.workspace4fit_.var("rrv_number_dataset_sb_hi"+label+"_"+self.channel+"_mj").getVal() ) )
        self.file_out.write( "\nRatio signal_region/sidebands  from dataset:%s"%(self.workspace4fit_.var("rrv_number_dataset_signal_region"+label+"_"+self.channel+"_mj").getVal()/(self.workspace4fit_.var("rrv_number_dataset_sb_lo"+label+"_"+self.channel+"_mj").getVal()+ self.workspace4fit_.var("rrv_number_dataset_sb_hi"+label+"_"+self.channel+"_mj").getVal()) ) )

        self.file_out.write( "\nEvents Number in sideband_low  from fitting:%s"%(rrv_tmp.getVal()*sb_loInt_val) )
        self.file_out.write( "\nEvents Number in Signal Region from fitting:%s"%(rrv_tmp.getVal()*signalInt_val) )
        self.file_out.write( "\nEvents Number in sideband_high from fitting:%s"%(rrv_tmp.getVal()*sb_hiInt_val) )
        self.file_out.write( "\nTotal  Number in sidebands     from fitting:%s"%(rrv_tmp.getVal()*(sb_loInt_val+sb_hiInt_val)  ) )
        self.file_out.write( "\nRatio signal_region/sidebands  from fitting:%s"%(signalInt_val/(sb_loInt_val+sb_hiInt_val)  ) )

        #if label=="_WJets": #prepare Limit of WJet Norm
        #    self.number_WJets_insideband=int(round( rrv_tmp.getVal()*(sb_loInt_val+sb_hiInt_val) ));
        #    self.datadriven_alpha_WJets_unbin =rrv_tmp.getVal()*signalInt_val/self.number_WJets_insideband

    ######## ++++++++++++++
    def get_mlvj_normalization_insignalregion(self, label, model_name=""):
        print "get mlvj normalization"
        print model_name
        if model_name=="": model = self.workspace4fit_.pdf("model"+label+"_signal_region"+"_"+self.channel+"_mlvj");
        else: model = self.workspace4fit_.pdf(model_name);

        rrv_mass_lvj = self.workspace4fit_.var("rrv_mass_lvj");

        fullInt   = model.createIntegral(RooArgSet(rrv_mass_lvj),RooArgSet(rrv_mass_lvj) );
        signalInt = model.createIntegral(RooArgSet(rrv_mass_lvj),RooArgSet(rrv_mass_lvj),("signal_region"));
        
        fullInt_val=fullInt.getVal()
        signalInt_val=signalInt.getVal()/fullInt_val

        print label+"signalInt=%s"%(signalInt_val)

        print "Events Number in MC Dataset:"
        self.workspace4fit_.var("rrv_number_dataset_signal_region"+label+"_"+self.channel+"_mlvj").Print();
        self.workspace4fit_.var("rrv_number_dataset_AllRange"+label+"_"+self.channel+"_mlvj").Print();

        print "Events Number get from fit:"
        rrv_tmp=self.workspace4fit_.var("rrv_number"+label+"_signal_region"+"_"+self.channel+"_mlvj");
        rrv_tmp.Print();
        print "\nEvents Number in Signal Region from fitting: %s"%(rrv_tmp.getVal()*signalInt_val)

        #save to file
        self.file_out.write( "\n%s++++++++++++++++++++++++++++++++++++"%(label) )
        self.file_out.write( "\nEvents Number in All Region from dataset   : %s"%(self.workspace4fit_.var("rrv_number_dataset_AllRange"+label+"_"+self.channel+"_mlvj").getVal()) )
        self.file_out.write( "\nEvents Number in Signal Region from dataset: %s"%(self.workspace4fit_.var("rrv_number_dataset_signal_region"+label+"_"+self.channel+"_mlvj").getVal()) )
        self.file_out.write( "\nRatio signal_region/all_range from dataset  :%s"%(self.workspace4fit_.var("rrv_number_dataset_signal_region"+label+"_"+self.channel+"_mlvj").getVal()/self.workspace4fit_.var("rrv_number_dataset_AllRange"+label+"_"+self.channel+"_mlvj").getVal() ) )
        self.file_out.write( "\nEvents Number in All Region from fitting   : %s\n"%(rrv_tmp.getVal()) )
        self.file_out.write( "\nEvents Number in Signal Region from fitting: %s\n"%(rrv_tmp.getVal()*signalInt_val) )
        self.file_out.write( "\nRatio signal_region/all_range from fitting :%s"%(signalInt_val ) )

        if not self.workspace4fit_.var("rrv_number_fitting_signal_region"+label+"_"+self.channel+"_mlvj"):
            rrv_number_fitting_signal_region_mlvj=RooRealVar("rrv_number_fitting_signal_region"+label+"_"+self.channel+"_mlvj","rrv_number_fitting_signal_region"+label+"_"+self.channel+"_mlvj", rrv_tmp.getVal()*signalInt_val );
            getattr(self.workspace4fit_,"import")(rrv_number_fitting_signal_region_mlvj);
        else :
            self.workspace4fit_.var("rrv_number_fitting_signal_region"+label+"_"+self.channel+"_mlvj").setVal(rrv_tmp.getVal()*signalInt_val);
            
        if label=="_WJets" and self.number_WJets_insideband!=-1: #prepare Limit of WJet Norm
            self.datadriven_alpha_WJets_counting = rrv_tmp.getVal()*signalInt_val/self.number_WJets_insideband 

    ######## ++++++++++++++
    def print_limit_datacard(self, mode ,params_list=[] ): #mode:unbin or counting
        print "print_limit_datacard for %s"%(mode)
        if not (mode == "unbin" or mode == "counting"):
            print "print_limit_datacard use wrong mode: %s"%(mode);raw_input("ENTER");
        datacard_out=open(getattr(self,"file_datacard_%s"%(mode)),"w");

        datacard_out.write( "imax 1" )
        datacard_out.write( "\njmax 4" )
        datacard_out.write( "\nkmax *" )
        datacard_out.write( "\n--------------- ")
        if mode == "unbin":
            datacard_out.write( "\nshapes * * %s %s:$PROCESS_%s"%(self.file_rlt_root, self.workspace4limit_.GetName(), self.channel))
            datacard_out.write( "\n--------------- ")
        datacard_out.write( "\nbin 1 ")
        if mode == "unbin":
            datacard_out.write( "\nobservation %s "%(self.workspace4limit_.data("data_obs_%s"%(self.channel)).sumEntries()) )
        if mode == "counting":
            datacard_out.write( "\nobservation %s "%(self.workspace4limit_.var("observation_for_counting").getVal()) )
        datacard_out.write( "\n------------------------------" )
        datacard_out.write( "\nbin                1         1        1        1      1" )
        #datacard_out.write( "\nprocess        %s_%s  WJets_%s TTbar_%s  STop_%s  VV_%s "%(self.higgs_sample, self.channel, self.channel, self.channel, self.channel, self.channel ) )
        datacard_out.write( "\nprocess            %s    WJets    TTbar     STop     VV "%(self.higgs_sample) )
        datacard_out.write( "\nprocess            0         1        2        3      4" )
        if mode == "unbin":
            datacard_out.write( "\nrate               %s        %s       %s       %s     %s "%(self.workspace4limit_.var("rate_%s_for_unbin"%(self.higgs_sample)).getVal(), self.workspace4limit_.var("rate_WJets_for_unbin").getVal(), self.workspace4limit_.var("rate_TTbar_for_unbin").getVal(), self.workspace4limit_.var("rate_STop_for_unbin").getVal(), self.workspace4limit_.var("rate_VV_for_unbin").getVal()  ) )
        if mode == "counting":
            datacard_out.write( "\nrate               %s        %s       %s     %s     %s"%(self.workspace4limit_.var("rate_%s_for_counting"%(self.higgs_sample)).getVal(), self.workspace4limit_.var("rate_WJets_for_counting").getVal(), self.workspace4limit_.var("rate_TTbar_for_counting").getVal(), self.workspace4limit_.var("rate_STop_for_counting").getVal(), self.workspace4limit_.var("rate_VV_for_counting").getVal()  ) )
        datacard_out.write( "\n-------------------------------- " )
        datacard_out.write( "\nlumi     lnN       1.044     -        1.044  1.044    1.044" )
        datacard_out.write( "\npdf_gg   lnN       1.099     -        -      -        -" )
        datacard_out.write( "\nXS_hig   lnN       1.137     -        -      -        -" )
        #print self.number_WJets_insideband; raw_input("ENTER");
        if self.number_WJets_insideband >0:
            datacard_out.write( "\nWJ_norm gmN %s     -         %s       -      -        -"%(self.number_WJets_insideband, getattr(self, "datadriven_alpha_WJets_%s"%(mode)) ) )
        else:
            datacard_out.write( "\nWJ_norm lnN    -         %s        -      -        -"%(1+ self.workspace4limit_.var("rate_WJets_for_unbin").getError()/self.workspace4limit_.var("rate_WJets_for_unbin").getVal()) )
        datacard_out.write( "\nXS_TTbar lnN       -         -        1.07   -        -" )
        datacard_out.write( "\nXS_STop  lnN       -         -        -      1.07     -" )
        datacard_out.write( "\nXS_VV    lnN       -         -        -      -        1.10 " )
        datacard_out.write( "\nwtagger  lnN       %s        -        %s     %s       %s   "%(1+self.rrv_wtagger_eff_reweight.getError()/self.rrv_wtagger_eff_reweight.getVal(),1+self.rrv_wtagger_eff_reweight.getError()/self.rrv_wtagger_eff_reweight.getVal(), 1+self.rrv_wtagger_eff_reweight.getError()/self.rrv_wtagger_eff_reweight.getVal(), 1+self.rrv_wtagger_eff_reweight.getError()/self.rrv_wtagger_eff_reweight.getVal() ) );
        if mode == "unbin":
            for i in range(len(params_list)):
                datacard_out.write( "\n%s param  %s  %s "%( params_list[i].GetName(), params_list[i].getVal(), params_list[i].getError() ) ) 

    ######## ++++++++++++++
    def prepare_limit(self,mode):
        print "prepare_limit for %s method"%(mode);
        #prepare for Limit
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_mass_lvj"));
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_fitting_signal_region_%s_%s_mlvj"%(self.higgs_sample,self.channel)).clone("rate_%s_for_counting"%(self.higgs_sample) ) )
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_fitting_signal_region_WJets_%s_mlvj"%(self.channel)).clone("rate_WJets_for_counting"))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_fitting_signal_region_VV_%s_mlvj"%(self.channel)).clone("rate_VV_for_counting"))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_fitting_signal_region_TTbar_%s_mlvj"%(self.channel)).clone("rate_TTbar_for_counting"))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_fitting_signal_region_STop_%s_mlvj"%(self.channel)).clone("rate_STop_for_counting"))

        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_%s_signal_region_%s_mlvj"%(self.higgs_sample, self.channel)).clone("rate_%s_for_unbin"%(self.higgs_sample)));
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_WJets_signal_region_%s_mlvj"%(self.channel)).clone("rate_WJets_for_unbin"));
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_VV_signal_region_%s_mlvj"%(self.channel)).clone("rate_VV_for_unbin"));
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_TTbar_signal_region_%s_mlvj"%(self.channel)).clone("rate_TTbar_for_unbin"));
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_STop_signal_region_%s_mlvj"%(self.channel)).clone("rate_STop_for_unbin"));
 
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.data("rdataset_data_signal_region_%s_mlvj"%(self.channel)).Clone("data_obs_%s"%(self.channel)))
        if mode=="fitting_method":
            getattr(self.workspace4limit_,"import")(self.workspace4fit_.pdf("model_pdf_WJets_signal_region_%s_mlvj"%(self.channel)).clone("WJets_%s"%(self.channel)))
        if mode=="sideband_correction_method1":
            getattr(self.workspace4limit_,"import")(self.workspace4fit_.pdf("model_pdf_WJets_signal_region_%s_after_correct_mlvj"%(self.channel)).clone("WJets_%s"%(self.channel)))
            self.workspace4limit_.allVars().Print();
        if mode=="sideband_correction_method2":
            getattr(self.workspace4limit_,"import")(self.workspace4fit_.pdf("model_pdf_WJets_signal_region_%s_after_correct_mlvj"%(self.channel)).clone("WJets_%s"%(self.channel)))
        if mode=="sideband_correction_method3":
            getattr(self.workspace4limit_,"import")(self.workspace4fit_.pdf("model_pdf_WJets_signal_region_%s_after_correct_mlvj"%(self.channel)).clone("WJets_%s"%(self.channel)))
        if mode=="sideband_correction_method4":
            getattr(self.workspace4limit_,"import")(self.workspace4fit_.pdf("model_pdf_WJets_signal_region_%s_after_correct_mlvj_Deco_data_signal_region_%s_mlvj"%(self.channel,self.channel)).clone("WJets_%s"%(self.channel)))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.pdf("model_pdf_TTbar_signal_region_%s_mlvj"%(self.channel)).clone("TTbar_%s"%(self.channel)))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.pdf("model_pdf_STop_signal_region_%s_mlvj"%(self.channel)).clone("STop_%s"%(self.channel)))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.pdf("model_pdf_VV_signal_region_%s_mlvj"%(self.channel)).clone("VV_%s"%(self.channel)))
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.pdf("model_pdf_%s_signal_region_%s_mlvj"%(self.higgs_sample,self.channel)).clone(self.higgs_sample+"_%s"%(self.channel)))

        self.save_workspace_to_file();

        params_list=[]
        if mode=="fitting_method":
            params_list.append(self.workspace4fit_.var("rrv_c_ErfExp_WJets_%s_signal_region"%(self.channel)))
            params_list.append(self.workspace4fit_.var("rrv_offset_ErfExp_WJets_%s_signal_region"%(self.channel)))
            params_list.append(self.workspace4fit_.var("rrv_width_ErfExp_WJets_%s_signal_region"%(self.channel)))
        if mode=="sideband_correction_method1":
            if self.model_4_mlvj=="ErfExp_v1":
                self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig0"%(self.channel)).setError(1.);
                self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig1"%(self.channel)).setError(1.);
                self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig2"%(self.channel)).setError(1.);
                self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig3"%(self.channel)).setError(1.);
                params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig0"%(self.channel)));
                params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig1"%(self.channel)));
                params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig2"%(self.channel)));
                params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig3"%(self.channel)));
                self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig0"%(self.channel)).setError(1.);
                self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig1"%(self.channel)).setError(1.);
                self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig2"%(self.channel)).setError(1.);
                self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig3"%(self.channel)).setError(1.);
                params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig0"%(self.channel)))
                params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig1"%(self.channel)))
                params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig2"%(self.channel)))
                params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig3"%(self.channel))) 
                self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig0"%(self.channel)).setError(1.);
                self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig1"%(self.channel)).setError(1.);
                self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig2"%(self.channel)).setError(1.);
                self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig3"%(self.channel)).setError(1.);
                params_list.append(self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig0"%(self.channel)))
                params_list.append(self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig1"%(self.channel)))
                params_list.append(self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig2"%(self.channel)))
                params_list.append(self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig3"%(self.channel))) 
            if self.model_4_mlvj=="Exp":
                self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig0"%(self.channel)).setError(1.);
                self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig1"%(self.channel)).setError(1.);
                params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig0"%(self.channel)));
                params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig1"%(self.channel)));
                self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig0"%(self.channel)).setError(1.);
                self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig1"%(self.channel)).setError(1.);
                params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig0"%(self.channel)))
                params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig1"%(self.channel)))
                self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig0"%(self.channel)).setError(1.);
                self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig1"%(self.channel)).setError(1.);
                params_list.append(self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig0"%(self.channel)))
                params_list.append(self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig1"%(self.channel)))

            #params_list.append(self.workspace4fit_.var("rrv_c_ErfExp_WJets_sb_lo_from_fitting"))
            #params_list.append(self.workspace4fit_.var("rrv_offset_ErfExp_WJets_sb_lo_from_fitting"))
            #params_list.append(self.workspace4fit_.var("rrv_width_ErfExp_WJets_sb_lo_from_fitting"))
        if mode=="sideband_correction_method2":
            self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig0"%(self.channel)).setError(1.);
            self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig1"%(self.channel)).setError(1.);
            self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig2"%(self.channel)).setError(1.);
            self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig3"%(self.channel)).setError(1.);
            self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig0"%(self.channel)).setError(1.);
            self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig1"%(self.channel)).setError(1.);
            self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig2"%(self.channel)).setError(1.);
            self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig3"%(self.channel)).setError(1.);
            self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig0"%(self.channel)).setError(1.);
            self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig1"%(self.channel)).setError(1.);
            self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig2"%(self.channel)).setError(1.);
            self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig3"%(self.channel)).setError(1.);
            #self.workspace4limit_.var("Deco_WJets_signal_region_mlvj_eig3").Print(); raw_input("ENTER");
            params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig0"%(self.channel)))
            params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig1"%(self.channel)))
            params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig2"%(self.channel)))
            params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig3"%(self.channel)))
            params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig0"%(self.channel)))
            params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig1"%(self.channel)))
            params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig2"%(self.channel)))
            params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig3"%(self.channel)))
            params_list.append(self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig0"%(self.channel)))
            params_list.append(self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig1"%(self.channel)))
            params_list.append(self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig2"%(self.channel)))
            params_list.append(self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig3"%(self.channel)))
        if mode=="sideband_correction_method3":
            self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig0"%(self.channel)).setError(1.);
            self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig1"%(self.channel)).setError(1.);
            self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig2"%(self.channel)).setError(1.);
            self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig3"%(self.channel)).setError(1.);
            self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig0"%(self.channel)).setError(1.);
            self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig1"%(self.channel)).setError(1.);
            self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig2"%(self.channel)).setError(1.);
            self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig3"%(self.channel)).setError(1.);
            self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig0"%(self.channel)).setError(1.);
            self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig1"%(self.channel)).setError(1.);
            self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig2"%(self.channel)).setError(1.);
            self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig3"%(self.channel)).setError(1.);
            #self.workspace4limit_.var("Deco_WJets_signal_region_mlvj_eig3").Print(); raw_input("ENTER");
            params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig0"%(self.channel)))
            params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig1"%(self.channel)))
            params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig2"%(self.channel)))
            params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_from_fitting_mlvj_eig3"%(self.channel)))
            params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig0"%(self.channel)))
            params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig1"%(self.channel)))
            params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig2"%(self.channel)))
            params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig3"%(self.channel)))
            params_list.append(self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig0"%(self.channel)))
            params_list.append(self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig1"%(self.channel)))
            params_list.append(self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig2"%(self.channel)))
            params_list.append(self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig3"%(self.channel)))
        if mode=="sideband_correction_method4":
            if self.model_4_mlvj=="ErfExp_v1":
                self.workspace4limit_.var("Deco_data_signal_region_mlvj_eig0").setError(1.);
                self.workspace4limit_.var("Deco_data_signal_region_mlvj_eig1").setError(1.);
                self.workspace4limit_.var("Deco_data_signal_region_mlvj_eig2").setError(1.);
                self.workspace4limit_.var("Deco_data_signal_region_mlvj_eig3").setError(1.);
                self.workspace4limit_.var("Deco_data_signal_region_mlvj_eig4").setError(1.);
                params_list.append(self.workspace4limit_.var("Deco_data_signal_region_mlvj_eig0"));
                params_list.append(self.workspace4limit_.var("Deco_data_signal_region_mlvj_eig1"));
                params_list.append(self.workspace4limit_.var("Deco_data_signal_region_mlvj_eig2"));
                params_list.append(self.workspace4limit_.var("Deco_data_signal_region_mlvj_eig3"));
                params_list.append(self.workspace4limit_.var("Deco_data_signal_region_mlvj_eig4"));
                self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig0"%(self.channel)).setError(1.);
                self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig1"%(self.channel)).setError(1.);
                self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig2"%(self.channel)).setError(1.);
                self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig3"%(self.channel)).setError(1.);
                params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig0"%(self.channel)))
                params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig1"%(self.channel)))
                params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig2"%(self.channel)))
                params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig3"%(self.channel))) 
                self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig0"%(self.channel)).setError(1.);
                self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig1"%(self.channel)).setError(1.);
                self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig2"%(self.channel)).setError(1.);
                self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig3"%(self.channel)).setError(1.);
                params_list.append(self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig0"%(self.channel)))
                params_list.append(self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig1"%(self.channel)))
                params_list.append(self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig2"%(self.channel)))
                params_list.append(self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig3"%(self.channel))) 
            if self.model_4_mlvj=="Exp":
                self.workspace4limit_.var("Deco_data_signal_region_mlvj_eig0").setError(1.);
                self.workspace4limit_.var("Deco_data_signal_region_mlvj_eig1").setError(1.);
                self.workspace4limit_.var("Deco_data_signal_region_mlvj_eig2").setError(1.);
                params_list.append(self.workspace4limit_.var("Deco_data_signal_region_mlvj_eig0"));
                params_list.append(self.workspace4limit_.var("Deco_data_signal_region_mlvj_eig1"));
                params_list.append(self.workspace4limit_.var("Deco_data_signal_region_mlvj_eig2"));
                self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig0"%(self.channel)).setError(1.);
                self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig1"%(self.channel)).setError(1.);
                params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig0"%(self.channel)))
                params_list.append(self.workspace4limit_.var("Deco_WJets_sb_lo_%s_mlvj_eig1"%(self.channel)))
                self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig0"%(self.channel)).setError(1.);
                self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig1"%(self.channel)).setError(1.);
                params_list.append(self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig0"%(self.channel)))
                params_list.append(self.workspace4limit_.var("Deco_WJets_signal_region_%s_mlvj_eig1"%(self.channel)))

        self.print_limit_datacard("unbin",params_list);
        self.print_limit_datacard("counting");

    ######### ++++++++++++++
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

        workspace.data("data_obs_%s"%(self.channel)).Print()
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
        #rrv_x.setBins(50)
        data_obs=workspace.data("data_obs_%s"%(self.channel))
        model_pdf_ggH=workspace.pdf("%s_%s"%(self.higgs_sample,self.channel))
        model_pdf_WJets=workspace.pdf("WJets_%s"%(self.channel))
        model_pdf_VV=workspace.pdf("VV_%s"%(self.channel))
        model_pdf_TTbar=workspace.pdf("TTbar_%s"%(self.channel))
        model_pdf_STop=workspace.pdf("STop_%s"%(self.channel))

        model_pdf_ggH.Print();
        model_pdf_WJets.Print();
        model_pdf_VV.Print();
        model_pdf_TTbar.Print();
        model_pdf_STop.Print();

        rrv_number_ggH=workspace.var("rate_%s_for_unbin"%(self.higgs_sample))
        rrv_number_WJets=workspace.var("rate_WJets_for_unbin")
        rrv_number_VV=workspace.var("rate_VV_for_unbin")
        rrv_number_TTbar=workspace.var("rate_TTbar_for_unbin")
        rrv_number_STop=workspace.var("rate_STop_for_unbin")

        rrv_number_ggH.Print();
        rrv_number_WJets.Print();
        rrv_number_VV.Print();
        rrv_number_TTbar.Print();
        rrv_number_STop.Print();

        rrv_number_Total_background_MC = RooRealVar("rrv_number_Total_background_MC","rrv_number_Total_background_MC",rrv_number_WJets.getVal()+rrv_number_VV.getVal()+rrv_number_TTbar.getVal()+rrv_number_STop.getVal());
        model_Total_background_MC = RooAddPdf("model_Total_background_MC","model_Total_background_MC",RooArgList(model_pdf_WJets,model_pdf_VV,model_pdf_TTbar,model_pdf_STop),RooArgList(rrv_number_WJets,rrv_number_VV,rrv_number_TTbar,rrv_number_STop));

        scale_number_ggH=rrv_number_ggH.getVal()/data_obs.sumEntries()
        scale_number_Total_background_MC=rrv_number_Total_background_MC.getVal()/data_obs.sumEntries()

        mplot=rrv_x.frame(RooFit.Title("check_workspace"));
        #data_obs.plotOn(mplot ,RooFit.DataError(RooAbsData.SumW2), RooFit.Name("data_invisible"),RooFit.Invisible());
        data_obs.plotOn(mplot , RooFit.Name("data_invisible"));

        model_Total_background_MC.plotOn(mplot,RooFit.Normalization(scale_number_Total_background_MC),RooFit.Name("WJets"), RooFit.Components("WJets_%s,VV_%s,TTbar_%s,STop_%s"%(self.channel,self.channel,self.channel,self.channel)),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["WJets"]), RooFit.LineColor(self.color_palet["WJets"]), RooFit.VLines());
        model_Total_background_MC.plotOn(mplot,RooFit.Normalization(scale_number_Total_background_MC),RooFit.Name("VV"), RooFit.Components("VV_%s,TTbar_%s,STop_%s"%(self.channel,self.channel,self.channel)),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["VV"]), RooFit.LineColor(self.color_palet["VV"]), RooFit.VLines());
        model_Total_background_MC.plotOn(mplot,RooFit.Normalization(scale_number_Total_background_MC),RooFit.Name("TTbar"), RooFit.Components("TTbar_%s,STop_%s"%(self.channel,self.channel)),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["TTbar"]), RooFit.LineColor(self.color_palet["TTbar"]), RooFit.VLines());
        model_Total_background_MC.plotOn(mplot,RooFit.Normalization(scale_number_Total_background_MC),RooFit.Name("STop"), RooFit.Components("STop_%s"%(self.channel)),RooFit.DrawOption("F"), RooFit.FillColor(self.color_palet["STop"]), RooFit.LineColor(self.color_palet["STop"]), RooFit.VLines());
        model_pdf_ggH.plotOn(mplot,RooFit.Normalization(scale_number_ggH),RooFit.Name("%s"%(self.higgs_sample)),RooFit.DrawOption("L"), RooFit.LineColor(self.color_palet["Signal"]), RooFit.VLines());
        data_obs.plotOn(mplot, RooFit.Name("data"));
        model_Total_background_MC.plotOn(mplot,RooFit.Normalization(scale_number_Total_background_MC),RooFit.Invisible());
        
        mplot.Print();
        leg=self.legend4Plot(mplot,0);
        mplot.addObject(leg);
        mplot.GetYaxis().SetRangeUser(1e-2,mplot.GetMaximum()*1.1);
        self.draw_canvas1(mplot,"plots_%s/m_lvj_fitting/"%(self.channel),"check_workspace_for_limit",0,1);

        if workspace.var("rrv_num_floatparameter_in_last_fitting"):   nPar_float_in_fitTo= int(workspace.var("rrv_num_floatparameter_in_last_fitting").getVal());
        else:
            nPar_float_in_fitTo=1;
        nBinX=mplot.GetNbinsX();
        ndof= nBinX-nPar_float_in_fitTo; 
        print "nPar=%s, chiSquare=%s/%s"%(nPar_float_in_fitTo, mplot.chiSquare( nPar_float_in_fitTo )*ndof, ndof );

    ######## ++++++++++++++
    def save_workspace_to_file(self):
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
        objName_before = "";
        for obj in range(int(plot.numItems()) ):
            objName = plot.nameOf(obj);
            if not ( ( (plot.getInvisible(objName)) and (not TString(objName).Contains("Uncertainty")) ) or TString(objName).Contains("invisi") or objName==objName_before  ): 
                theObj = plot.getObject(obj);
                objTitle = objName;
                drawoption= plot.getDrawOptions(objName).Data()
                if drawoption=="P":drawoption="PE"
                if TString(objName).Contains("Graph"): theLeg.AddEntry(theObj, "Uncertainty","F");
                else: 
                    if TString(objName).Contains("STop"): theLeg.AddEntry(theObj, "Single-Top","F");
                    else : theLeg.AddEntry(theObj, objTitle,drawoption);
                entryCnt=entryCnt+1;
            objName_before=objName;

        theLeg.SetY1NDC(0.9 - 0.05*entryCnt - 0.005);
        theLeg.SetY1(theLeg.GetY1NDC());
        return theLeg;

    ######## ++++++++++++++
    def draw_canvas(self, mplot, mplot_pull,parameters_list,in_directory, in_file_name, in_model_name="", show_constant_parameter=0, log=0):# mplot + pull + parameters
        mplot.GetXaxis().SetTitleOffset(1.1);
        mplot.GetYaxis().SetTitleOffset(1.1);
        mplot.GetXaxis().SetTitleSize(0.04);
        mplot.GetYaxis().SetTitleSize(0.04);
        mplot.GetXaxis().SetLabelSize(0.04);
        mplot.GetYaxis().SetLabelSize(0.04);
        mplot_pull.GetYaxis().SetTitleOffset(1.0);

        cMassFit = TCanvas("cMassFit","cMassFit",1000,800);
        pad1=TPad("pad1","pad1",0.,0. ,0.8,0.2);
        pad2=TPad("pad2","pad2",0.,0.2,0.8,1. );
        pad3=TPad("pad3","pad3",0.8,0.,1,1);
        pad1.Draw();
        pad2.Draw();
        pad3.Draw();

        pad2.cd();
        mplot.Draw();
        banner = TLatex(0.18,0.85,("#splitline{CMS Preliminary}{%.1f fb^{-1} at #sqrt{s}=8TeV %s+jets}"%(self.GetLumi(),self.channel)));
        banner.SetNDC(); banner.SetTextSize(0.025);
        banner.Draw();

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

        string_file_name=TString(in_file_name);
        if string_file_name.EndsWith(".root"): string_file_name.ReplaceAll(".root",in_model_name);
        else: rlt_file.Append(in_model_name);
        self.draw_canvas1(mplot,in_directory,string_file_name.Data(),0,log);

    ######## ++++++++++++++
    def draw_canvas_MCscale(self, mplot, mplot_addition,in_directory, in_file_name, in_model_name="", show_constant_parameter=0, log=0):#mplot + MC/data scale

        mplot.GetXaxis().SetTitleOffset(1.1);
        mplot.GetYaxis().SetTitleOffset(1.1);
        mplot.GetXaxis().SetTitleSize(0.04);
        mplot.GetYaxis().SetTitleSize(0.04);
        mplot.GetXaxis().SetLabelSize(0.04);
        mplot.GetYaxis().SetLabelSize(0.04);
        mplot_addition.GetYaxis().SetTitleOffset(1.0);

        cMassFit = TCanvas("cMassFit","cMassFit",1000,800);
        pad1=TPad("pad1","pad1",0.00,0.25,1.00,0.97);
        pad2=TPad("pad2","pad2",0.00,0.00,1.00,0.25);
        pad1.Draw();
        pad2.Draw();

        pad1.cd();
        mplot.Draw();
        banner = TLatex(0.18,0.85,("#splitline{CMS Preliminary}{%.1f fb^{-1} at #sqrt{s}=8TeV %s+jets}"%(self.GetLumi(),self.channel)));
        banner.SetNDC(); banner.SetTextSize(0.025);
        banner.Draw();

        pad2.cd();
        mplot_addition.Draw();

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

        string_file_name=TString(in_file_name);
        if string_file_name.EndsWith(".root"): string_file_name.ReplaceAll(".root",in_model_name);
        else: rlt_file.Append(in_model_name);
        self.draw_canvas1(mplot,in_directory,string_file_name.Data(),0,log);
        
    ######## ++++++++++++++
    def draw_canvas1(self, in_obj,in_directory, in_file_name, is_range=0, log=0):
        cMassFit = TCanvas("cMassFit","cMassFit",1000,800);
        if is_range:
            h2=TH2D("h2","",100,400,1400,4,0.00001,4); h2.Draw(); in_obj.Draw("same")
        else : 
            in_obj.Draw()

        in_obj.GetXaxis().SetTitleOffset(1.1);
        in_obj.GetYaxis().SetTitleOffset(1.1);
        in_obj.GetXaxis().SetTitleSize(0.04);
        in_obj.GetYaxis().SetTitleSize(0.04);
        in_obj.GetXaxis().SetLabelSize(0.04);
        in_obj.GetYaxis().SetLabelSize(0.04);

        banner = TLatex(0.18,0.85,("#splitline{CMS Preliminary}{%.1f fb^{-1} at #sqrt{s}=8TeV %s+jets}"%(self.GetLumi(),self.channel)));
        banner.SetNDC(); banner.SetTextSize(0.025);
        banner.Draw();

        Directory=TString(in_directory+self.higgs_sample+"/");
        if not Directory.EndsWith("/"):Directory=Directory.Append("/");
        if not os.path.isdir(Directory.Data()): os.system("mkdir -p  "+Directory.Data());

        rlt_file=TString(Directory.Data()+in_file_name);
        if rlt_file.EndsWith(".root"):
            rlt_file.ReplaceAll(".root","_rlt_without_pull_and_paramters.png");
        else:
            #rlt_file=rlt_file.Append("_rlt_without_pull_and_paramters.png");
            rlt_file=rlt_file.Append(".png");
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
    def GetLumi(self):
        if self.channel=="el": return 5.1#13.9;
        if self.channel=="mu": return 5.3#14.0;

    ######## ++++++++++++++
    def get_data(self, bool_fake_data):
        print "get_data"
        if bool_fake_data:
            rdataset_WJets_mj=self.workspace4fit_.data("rdataset_WJets_mj")
            rdataset_VV_mj=self.workspace4fit_.data("rdataset_VV_mj")
            rdataset_TTbar_mj=self.workspace4fit_.data("rdataset_TTbar_mj")
            rdataset_STop_mj=self.workspace4fit_.data("rdataset_STop_mj")
            rdataset_signal_mj=self.workspace4fit_.data("rdataset_%s_mj"%(self.higgs_sample))
            rdataset_data_mj = rdataset_WJets_mj.Clone("rdataset_data_mj");
            rdataset_data_mj.append(rdataset_VV_mj)
            rdataset_data_mj.append(rdataset_TTbar_mj)
            rdataset_data_mj.append(rdataset_STop_mj)

            rdataset_WJets_sb_lo_mlvj=self.workspace4fit_.data("rdataset_WJets_sb_lo_mlvj")
            rdataset_VV_sb_lo_mlvj=self.workspace4fit_.data("rdataset_VV_sb_lo_mlvj")
            rdataset_TTbar_sb_lo_mlvj=self.workspace4fit_.data("rdataset_TTbar_sb_lo_mlvj")
            rdataset_STop_sb_lo_mlvj=self.workspace4fit_.data("rdataset_STop_sb_lo_mlvj")
            rdataset_signal_sb_lo_mlvj=self.workspace4fit_.data("rdataset_%s_sb_lo_mlvj"%(self.higgs_sample))
            rdataset_data_sb_lo_mlvj =rdataset_WJets_sb_lo_mlvj.Clone("rdataset_data_sb_lo_mlvj")
            rdataset_data_sb_lo_mlvj.append(rdataset_VV_sb_lo_mlvj)
            rdataset_data_sb_lo_mlvj.append(rdataset_TTbar_sb_lo_mlvj)
            rdataset_data_sb_lo_mlvj.append(rdataset_STop_sb_lo_mlvj)   

            rdataset_WJets_signal_region_mlvj=self.workspace4fit_.data("rdataset_WJets_signal_region_mlvj")
            rdataset_VV_signal_region_mlvj=self.workspace4fit_.data("rdataset_VV_signal_region_mlvj")
            rdataset_TTbar_signal_region_mlvj=self.workspace4fit_.data("rdataset_TTbar_signal_region_mlvj")
            rdataset_STop_signal_region_mlvj=self.workspace4fit_.data("rdataset_STop_signal_region_mlvj")
            rdataset_signal_signal_region_mlvj=self.workspace4fit_.data("rdataset_%s_signal_region_mlvj"%(self.higgs_sample))
            rdataset_data_signal_region_mlvj =rdataset_WJets_signal_region_mlvj.Clone("rdataset_data_signal_region_mlvj")
            rdataset_data_signal_region_mlvj.append(rdataset_VV_signal_region_mlvj)
            rdataset_data_signal_region_mlvj.append(rdataset_TTbar_signal_region_mlvj)
            rdataset_data_signal_region_mlvj.append(rdataset_STop_signal_region_mlvj)   

            rdataset_WJets_sb_hi_mlvj=self.workspace4fit_.data("rdataset_WJets_sb_hi_mlvj")
            rdataset_VV_sb_hi_mlvj=self.workspace4fit_.data("rdataset_VV_sb_hi_mlvj")
            rdataset_TTbar_sb_hi_mlvj=self.workspace4fit_.data("rdataset_TTbar_sb_hi_mlvj")
            rdataset_STop_sb_hi_mlvj=self.workspace4fit_.data("rdataset_STop_sb_hi_mlvj")
            rdataset_signal_sb_hi_mlvj=self.workspace4fit_.data("rdataset_%s_sb_hi_mlvj"%(self.higgs_sample))
            rdataset_data_sb_hi_mlvj =rdataset_WJets_sb_hi_mlvj.Clone("rdataset_data_sb_hi_mlvj")
            rdataset_data_sb_hi_mlvj.append(rdataset_VV_sb_hi_mlvj)
            rdataset_data_sb_hi_mlvj.append(rdataset_TTbar_sb_hi_mlvj)
            rdataset_data_sb_hi_mlvj.append(rdataset_STop_sb_hi_mlvj)    

            combData_WJets=self.workspace4fit_.data("combData_WJets")
            combData_VV   =self.workspace4fit_.data("combData_VV")
            combData_TTbar=self.workspace4fit_.data("combData_TTbar")
            combData_STop =self.workspace4fit_.data("combData_STop")
            combData_signal =self.workspace4fit_.data("combData_%s"%(self.higgs_sample))
            combData_data = combData_WJets.Clone("combData_data");
            combData_data.append(combData_VV)
            combData_data.append(combData_TTbar)
            combData_data.append(combData_STop)

            getattr(self.workspace4fit_,"import")(rdataset_data_mj);
            getattr(self.workspace4fit_,"import")(rdataset_data_sb_lo_mlvj);
            getattr(self.workspace4fit_,"import")(rdataset_data_signal_region_mlvj);
            getattr(self.workspace4fit_,"import")(rdataset_data_sb_hi_mlvj);
            getattr(self.workspace4fit_,"import")(combData_data);

            rrv_number_dataset_signal_region_mlvj=RooRealVar("rrv_number_dataset_signal_region_data_%s_mlvj"%(self.channel),"rrv_number_dataset_signal_region_data_%s_mlvj"%(self.channel),self.workspace4fit_.var("rrv_number_dataset_signal_region_WJets_mlvj").getVal()+self.workspace4fit_.var("rrv_number_dataset_signal_region_VV_mlvj").getVal()+self.workspace4fit_.var("rrv_number_dataset_signal_region_TTbar_mlvj").getVal()+self.workspace4fit_.var("rrv_number_dataset_signal_region_STop_mlvj").getVal());
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
        getattr(self.workspace4limit_,"import")(self.workspace4fit_.var("rrv_number_dataset_signal_region_data_%s_mlvj"%(self.channel)).clone("observation_for_counting"))
 
    ######## ++++++++++++++
    def fit_Signal(self):
        print "fit_Signal"
        self.get_mj_and_mlvj_dataset(self.file_ggH,"_%s"%(self.higgs_sample))# to get the shape of m_lvj
        self.fit_m_j_single_MC(self.file_ggH,"_%s"%(self.higgs_sample),"Voig");
        #self.fit_mlvj_model_single_MC(self.file_ggH,"_%s"%(self.higgs_sample),"_signal_region","Seymour");
        if self.higgs_sample=="ggH600":
            self.fit_mlvj_model_single_MC(self.file_ggH,"_%s"%(self.higgs_sample),"_sb_lo","CB_v1");
            self.fit_mlvj_model_single_MC(self.file_ggH,"_%s"%(self.higgs_sample),"_signal_region","CB_v1");
        if self.higgs_sample=="ggH700":
            self.fit_mlvj_model_single_MC(self.file_ggH,"_%s"%(self.higgs_sample),"_sb_lo","Voig_v1");
            self.fit_mlvj_model_single_MC(self.file_ggH,"_%s"%(self.higgs_sample),"_signal_region","CB_v1");
        if self.higgs_sample=="ggH800":
            self.fit_mlvj_model_single_MC(self.file_ggH,"_%s"%(self.higgs_sample),"_sb_lo","Voig_v1");
            self.fit_mlvj_model_single_MC(self.file_ggH,"_%s"%(self.higgs_sample),"_signal_region","Voig_v1");
        if self.higgs_sample=="ggH900":
            self.fit_mlvj_model_single_MC(self.file_ggH,"_%s"%(self.higgs_sample),"_sb_lo","Voig_v1");
            self.fit_mlvj_model_single_MC(self.file_ggH,"_%s"%(self.higgs_sample),"_signal_region","Voig_v1"); 
        if self.higgs_sample=="ggH1000":
            self.fit_mlvj_model_single_MC(self.file_ggH,"_%s"%(self.higgs_sample),"_sb_lo","Voig_v1");
            self.fit_mlvj_model_single_MC(self.file_ggH,"_%s"%(self.higgs_sample),"_signal_region","Voig_v1");  
        #raw_input("ENTER");
        print "________________________________________________________________________"

    ######## ++++++++++++++
    def fit_WJets(self):
        print "fit_WJets"
        self.get_mj_and_mlvj_dataset(self.file_WJets_mc,"_WJets")# to get the shape of m_lvj
        self.fit_m_j_single_MC(self.file_WJets_mc,"_WJets","ErfExp");
        self.fit_mlvj_model_single_MC(self.file_WJets_mc,"_WJets","_sb_lo",self.model_4_mlvj);
        self.fit_mlvj_model_single_MC(self.file_WJets_mc,"_WJets","_signal_region",self.model_4_mlvj);
        print "________________________________________________________________________"

    ######## ++++++++++++++
    def fit_VV(self):
        print "fit_VV"
        self.get_mj_and_mlvj_dataset(self.file_VV_mc,"_VV")# to get the shape of m_lvj
        self.fit_m_j_single_MC(self.file_VV_mc,"_VV","2Voig");
        self.fit_mlvj_model_single_MC(self.file_VV_mc,"_VV","_sb_lo",self.model_4_mlvj);
        self.fit_mlvj_model_single_MC(self.file_VV_mc,"_VV","_signal_region",self.model_4_mlvj);
 
        print "________________________________________________________________________"

    ######## ++++++++++++++
    def fit_TTbar(self):
        print "fit_TTbar"
        self.get_mj_and_mlvj_dataset(self.file_TTbar_mc,"_TTbar")# to get the shape of m_lvj
        self.fit_m_j_single_MC(self.file_TTbar_mc,"_TTbar","ErfExpGaus_sp");
        self.fit_mlvj_model_single_MC(self.file_TTbar_mc,"_TTbar","_sb_lo",self.model_4_mlvj);
        self.fit_mlvj_model_single_MC(self.file_TTbar_mc,"_TTbar","_signal_region",self.model_4_mlvj);
 
        print "________________________________________________________________________"

    ######## ++++++++++++++
    def fit_STop(self):
        print "fit_STop"
        self.get_mj_and_mlvj_dataset(self.file_STop_mc,"_STop")# to get the shape of m_lvj
        self.fit_m_j_single_MC(self.file_STop_mc,"_STop","ErfExpGaus_sp");
        self.fit_mlvj_model_single_MC(self.file_STop_mc,"_STop","_sb_lo",self.model_4_mlvj);
        self.fit_mlvj_model_single_MC(self.file_STop_mc,"_STop","_signal_region",self.model_4_mlvj);
        print "________________________________________________________________________"  

    ######## ++++++++++++++
    def fit_AllSamples_Mlvj(self):
        print "fit_AllSamples_Mlvj"
        self.fit_Signal()
        self.fit_WJets()
        self.fit_TTbar()
        self.fit_STop()
        self.fit_VV()
        print "________________________________________________________________________" 

    ####### +++++++++++++++
    def fit_TTbar_controlsample(self):
        print "fit_TTbar_controlsample"

        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j");
        self.get_mj_and_mlvj_dataset_TTbar_controlsample(self.file_WJets_mc,"_WJets");#self.fit_m_j_singlebackground_MC_TTbar_controlsample(self.file_WJets_mc,"_WJets","ErfExp");
        self.get_mj_and_mlvj_dataset_TTbar_controlsample(self.file_TTbar_mc,"_TTbar");#self.fit_m_j_singlebackground_MC_TTbar_controlsample(self.file_TTbar_mc,"_TTbar","ErfExpGaus");
        self.get_mj_and_mlvj_dataset_TTbar_controlsample(self.file_VV_mc,"_VV");      #self.fit_m_j_singlebackground_MC_TTbar_controlsample(self.file_VV_mc,"_VV","ErfExpGaus");
        self.get_mj_and_mlvj_dataset_TTbar_controlsample(self.file_STop_mc,"_STop");  #self.fit_m_j_singlebackground_MC_TTbar_controlsample(self.file_STop_mc,"_STop","ErfExpGaus");
        self.get_mj_and_mlvj_dataset_TTbar_controlsample(self.file_pseudodata,"_pseudodata");self.fit_m_j_singlebackground_MC_TTbar_controlsample(self.file_pseudodata,"_pseudodata","ErfExpGaus");

        self.get_mj_and_mlvj_dataset_TTbar_controlsample(self.file_data,"_data"); #self.fit_m_j_singlebackground_MC_TTbar_controlsample(self.file_data,"_data","ErfExpGaus");
        self.fit_m_j_TTbar_controlsample(self.file_data,"ErfExpGaus");

    ####### +++++++++++++++
    def analysis_fitting_method(self):
        self.fit_AllSamples_Mlvj()
        self.get_data(0)
        self.fit_WJetsNormalization_in_Mj_signal_region();
        self.fit_mlvj_in_Mj_signal_region()
        self.prepare_limit("fitting_method")
        self.read_workspace()

    ####### +++++++++++++++
    def analysis_sideband_correction_method1(self):
        self.fit_AllSamples_Mlvj()
        self.get_data(0)
        self.fit_WJetsNormalization_in_Mj_signal_region();
        self.fit_mlvj_in_Mj_sideband("_sb_lo")
        self.prepare_limit("sideband_correction_method1")
        self.read_workspace()

    ####### +++++++++++++++
    def analysis_sideband_correction_method2(self):
        self.fit_AllSamples_Mlvj()
        self.get_data(0);# 1: dummy data; 0: true data
        self.fit_mlvj_in_Mj_sideband("_sb_lo")
        self.prepare_limit("sideband_correction_method2")
        self.read_workspace()

    ####### +++++++++++++++
    def analysis_sideband_correction_method3(self):
        self.fit_AllSamples_Mlvj()
        self.get_data(0);# 1: dummy data; 0: true data
        self.fit_mlvj_in_Mj_sideband("_sb_lo")
        self.fit_mlvj_in_Mj_signal_region_for_sideband_correction_method3();
        self.prepare_limit("sideband_correction_method3")
        self.read_workspace()

    ####### +++++++++++++++
    def analysis_sideband_correction_method4(self):
        self.fit_AllSamples_Mlvj()
        self.get_data(0);# 1: dummy data; 0: true data
        self.fit_simultaneous_mlvj_in_Mj_signal_region_and_sideband("_sb_lo");
        self.prepare_limit("sideband_correction_method4")
        self.read_workspace()

def control_sample(channel="mu"):
    print "control sample "+channel;
    boostedW_fitter=doFit_wj_and_wlvj(channel,"ggH600",500,700,0,220) #(channel,"ggH600",500,700,40,140)
    boostedW_fitter.fit_TTbar_controlsample();


def pre_limit_fitting_method(channel, higgs_sample="ggH600", in_mlvj_signal_region_min=500, in_mlvj_signal_region_max=700, in_mj_min=30, in_mj_max=140, in_mlvj_min=400, in_mlvj_max=1400): 
    print "pre_limit_fitting_method for %s sample"%(channel)
    boostedW_fitter=doFit_wj_and_wlvj(channel, higgs_sample, in_mlvj_signal_region_min, in_mlvj_signal_region_max, in_mj_min, in_mj_max, in_mlvj_min, in_mlvj_max)
    boostedW_fitter.analysis_fitting_method()

def pre_limit_sb_correction(method, channel, higgs_sample="ggH600", in_mlvj_signal_region_min=500, in_mlvj_signal_region_max=700, in_mj_min=30, in_mj_max=140, in_mlvj_min=400, in_mlvj_max=1400, fit_model="ErfExp_v1"): # the WJets M_lvj shape and normalization are from sb_correction
    print "pre_limit_sb_correction with %s for %s sample"%(method, channel)
    boostedW_fitter=doFit_wj_and_wlvj(channel, higgs_sample, in_mlvj_signal_region_min, in_mlvj_signal_region_max, in_mj_min, in_mj_max, in_mlvj_min, in_mlvj_max,fit_model);
    #boostedW_fitter.ControlPlots();
    getattr(boostedW_fitter,"analysis_sideband_correction_%s"%(method) )();

def control_single_sb_correction(method, channel, higgs_sample="ggH600", in_mlvj_signal_region_min=500, in_mlvj_signal_region_max=700, in_mj_min=30, in_mj_max=140, in_mlvj_min=400, in_mlvj_max=1400, fit_model="ErfExp_v1"): # the WJets M_lvj shape and normalization are from sb_correction
    print "pre_limit_sb_correction with %s for %s sample"%(method, channel)
    boostedW_fitter=doFit_wj_and_wlvj(channel, higgs_sample, in_mlvj_signal_region_min, in_mlvj_signal_region_max, in_mj_min, in_mj_max, in_mlvj_min, in_mlvj_max,fit_model);
    boostedW_fitter.ControlPlots();
 
def pre_limit_single(channel):
    print "pre_limit_single for %s sampel"%(channel)
    #pre_limit_fitting_method(channel, "ggH600",500,700)
    #pre_limit_fitting_method(channel, "ggH700" ,600,850)
    #pre_limit_fitting_method(channel, "ggH800" ,650,1000)
    #pre_limit_fitting_method(channel, "ggH900" ,750,1100)
    #pre_limit_fitting_method(channel, "ggH1000",800,1150)

    pre_limit_sb_correction("method1",channel, "ggH600",500,700,30,140,400,1000,"ErfExp_v1")
    #pre_limit_sb_correction("method1",channel, "ggH700",500,700,30,140,400,1200,"ErfExp_v1")
    #pre_limit_sb_correction("method1",channel, "ggH800",500,700,30,140,400,1600,"ErfExp_v1")
    #pre_limit_sb_correction("method1",channel, "ggH900",500,700,30,140,400,1600,"ErfExp_v1")
    #pre_limit_sb_correction("method1",channel,"ggH1000",500,700,30,140,400,1600,"ErfExp_v1")
  
def control_single(channel):
    print "control_single for %s sampel"%(channel)
    #control_single_sb_correction("method1",channel, "ggH600",500,700,30,140,400,1000,"ErfExp_v1")
    control_single_sb_correction("method1",channel, "ggH800",500,1300,30,140,400,1400,"ErfExp_v1")

def check_workspace(channel, higgs):
    boostedW_fitter=doFit_wj_and_wlvj(channel,higgs); boostedW_fitter.read_workspace()
    #boostedW_fitter=doFit_wj_and_wlvj(channel,"ggH600"); boostedW_fitter.read_workspace()
    #boostedW_fitter=doFit_wj_and_wlvj(channel, "ggH1000"); boostedW_fitter.read_workspace()

if __name__ == '__main__':
    channel=options.channel;#mu or el; default is mu;

    if options.fitwtagger:
        print 'fitwtagger for %s sample'%(channel)
        control_sample(channel);#mu for muon sample; el for el sample
        
    if options.control:
        print 'control for %s sample'%(channel);
        control_single(channel);

    if options.check:
        print 'check workspace for %s sample'%(channel);
        check_workspace(channel,"ggH600");

    if options.single and (not options.fitwtagger) and ( not options.multi) and ( not options.control) and ( not options.check):
        print 'single mode for %s sample'%(channel)
        pre_limit_single(channel)

    if options.multi:
        print 'multi mode for %s sample'%(channel)
        #pre_limit_fitting_method(channel, sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))
        #pre_limit_sb_correction("method1" sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))
        #pre_limit_sb_correction("method2",sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))
        #pre_limit_sb_correction("method3",sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))
        pre_limit_sb_correction("method1",sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]),int(sys.argv[7]),int(sys.argv[8]), sys.argv[9] )
