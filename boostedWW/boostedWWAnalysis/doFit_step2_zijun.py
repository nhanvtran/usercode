#! /usr/bin/env python
import os
import glob
import math
import array

from ROOT import gROOT, gStyle, gSystem, TLatex
import subprocess
from subprocess import Popen

from sampleWrapperClass import *
from trainingClass import *
from BoostedWSamples import * 

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

## Application class

class tmvaApplicator: 

    def __init__(self, listOfVars, weightfile):
        
        self.ListOfTrainingVariables = listOfVars;
        self.nameOfWeightFile = weightfile;
            
        # make a list of arrays
        self.reader = ROOT.TMVA.Reader("!Color:!Silent")
        self.listOfVarArray = [];
        for i in range(len(self.ListOfTrainingVariables)):
            #            curVar = array('f',[0.]);
            self.listOfVarArray.append( array('f',[0.]) );
            varString = self.ListOfTrainingVariables[i]+" := "+self.ListOfTrainingVariables[i];
            self.reader.AddVariable( varString, self.listOfVarArray[i] );
        
        #spectators
        spec1 = array('f',[0.]);
        spec2 = array('f',[0.]);
    #    spec3 = array('f',[0.]);
        self.reader.AddSpectator( "jet_pt_pr", spec1 )
        self.reader.AddSpectator( "jet_mass_pr", spec2 )
    #    reader.AddSpectator( "jet_massdrop_pr", spec3 )        

        self.reader.BookMVA("BDT",self.nameOfWeightFile);

    def eval(self, listOfVarVals):
        
        for i in range(len(listOfVarVals)):
            self.listOfVarArray[i][0] = listOfVarVals[i];
            
        return self.reader.EvaluateMVA("BDT");

## ---------------------------------------------------

#def setmodel (label, in_model_name)

## ---------------------------------------------------
    
def fit_general(in_file_name, label, in_model_name,cutOnMassDrop):

    # read in tree
    fileIn_name=ROOT.TString("trainingtrees/"+in_file_name);
    fileIn = ROOT.TFile(fileIn_name.Data());
    treeIn = fileIn.Get("otree");
    
    # define bdt reader
    listOfTrainingVariables1 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1"];
    bdtSimple = tmvaApplicator( listOfTrainingVariables1, "weights/Wtagger_200to275_simple_BDT.weights.xml");
        
    rrv_mass = ROOT.RooRealVar("rrv_mass","rrv_mass",30.,140.) 
    rrv_mass.setBins(50);
    #rrv_mass = ROOT.RooRealVar("rrv_mass","rrv_mass",30.,200.) 
    #rrv_mass = ROOT.RooRealVar("rrv_mass","rrv_mass",60.,100.)
    rrv_weight = ROOT.RooRealVar("rrv_weight","rrv_weight",0. ,1.) 
    rdataset = ROOT.RooDataSet("rdataset","rdataset",ROOT.RooArgSet(rrv_mass,rrv_weight),ROOT.RooFit.WeightVar(rrv_weight) ); 
    # make cuts (including mass drop) # create a RooDataSet
    print "N entries: ", treeIn.GetEntries()
    for i in range(treeIn.GetEntries()):
        if i % 10000 == 0: print "i: ",i
        treeIn.GetEntry(i);

        discriminantCut = False; 
            
        if cutOnMassDrop and treeIn.jet_massdrop_pr < 0.25: discriminantCut = True;
        elif not cutOnMassDrop:
            listOfVarVals = [];
            for kk in range(len(listOfTrainingVariables1)):
                listOfVarVals.append( getattr( treeIn, listOfTrainingVariables1[kk] ) );
            BDTval = bdtSimple.eval( listOfVarVals );
#            print BDTval;
            if BDTval > 0.0: discriminantCut = True;
        else: discriminantCut = False;
       
        if treeIn.jet_pt_pr > 200. and discriminantCut and treeIn.jet_mass_pr > 30 and treeIn.jet_mass_pr<140 and treeIn.njets ==0:
        #if treeIn.jet_pt_pr > 200. and discriminantCut and treeIn.jet_mass_pr > 30 and treeIn.jet_mass_pr<200:
            rrv_mass.setVal( treeIn.jet_mass_pr );
            rdataset.add( ROOT.RooArgSet( rrv_mass ), treeIn.totalEventWeight );
            #print treeIn.totalEventWeight
            
    print "N_rdataset: ", rdataset.numEntries();

    #model
    if in_model_name == "Voig":
        rrv_mean_voig=ROOT.RooRealVar("rrv_mean_voig"+label,"rrv_mean_voig"+label,82,78,87);
        rrv_width_voig=ROOT.RooRealVar("rrv_width_voig"+label,"rrv_width_voig"+label,7.,1,10);
        rrv_sigma_voig=ROOT.RooRealVar("rrv_sigma_voig"+label,"rrv_sigma_voig"+label,5,1,15);
        rrv_number = ROOT.RooRealVar("rrv_number"+label,"rrv_number"+label,50,1,100000);

        voig = ROOT.RooVoigtian("voig"+label,"voig"+label, rrv_mass,rrv_mean_voig,rrv_width_voig,rrv_sigma_voig);
        model = ROOT.RooExtendPdf("model"+label,"model"+label, voig, rrv_number );
        parameters_list=[rrv_mean_voig,rrv_width_voig,rrv_sigma_voig,rrv_number];

    if in_model_name == "Gaus":
        rrv_mean_gaus=ROOT.RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,82,78,87);
        rrv_sigma_gaus=ROOT.RooRealVar("rrv_sigma_gaus"+label,"rrv_sigma_gaus"+label,7,1,15);
        rrv_number = ROOT.RooRealVar("rrv_number"+label,"rrv_number"+label,70,1,100000);

        gaus = ROOT.RooGaussian("gaus"+label,"gaus"+label, rrv_mass,rrv_mean_gaus,rrv_sigma_gaus);
        model = ROOT.RooExtendPdf("model"+label,"model"+label, gaus, rrv_number );
        parameters_list=[rrv_mean_gaus,rrv_sigma_gaus,rrv_number];

    if in_model_name == "CB":
        rrv_mean_CB=ROOT.RooRealVar("rrv_mean_CB"+label,"rrv_mean_CB"+label,82,78,87);
        rrv_sigma_CB=ROOT.RooRealVar("rrv_sigma_CB"+label,"rrv_sigma_CB"+label,5,2,10);
        rrv_alpha_CB=ROOT.RooRealVar("rrv_alpha_CB"+label,"rrv_alpha_CB"+label,-2,-4,-1);
        rrv_n_CB=ROOT.RooRealVar("rrv_n_CB"+label,"rrv_n_CB"+label,2,0.,4);
        rrv_number = ROOT.RooRealVar("rrv_number"+label,"rrv_number"+label,1300,1,100000);

        cbshape = ROOT.RooCBShape("cbshape"+label,"cbshape"+label, rrv_mass,rrv_mean_CB,rrv_sigma_CB,rrv_alpha_CB,rrv_n_CB);
        model = ROOT.RooExtendPdf("model"+label,"model"+label, cbshape, rrv_number );
        parameters_list=[rrv_mean_CB,rrv_sigma_CB,rrv_alpha_CB,rrv_n_CB,rrv_number];

    if in_model_name == "CBBW": # FFT: BreitWigner*CBShape
        rrv_mean_CB=ROOT.RooRealVar("rrv_mean_CB"+label,"rrv_mean_CB"+label,83.5,80,87);
        rrv_sigma_CB=ROOT.RooRealVar("rrv_sigma_CB"+label,"rrv_sigma_CB"+label,6,2,10);
        rrv_alpha_CB=ROOT.RooRealVar("rrv_alpha_CB"+label,"rrv_alpha_CB"+label,-2,-4,-1);
        rrv_n_CB=ROOT.RooRealVar("rrv_n_CB"+label,"rrv_n_CB"+label,0.5,0.,2);
        rrv_mean_BW=ROOT.RooRealVar("rrv_mean_BW"+label,"rrv_mean_BW"+label,0);
        rrv_width_BW=ROOT.RooRealVar("rrv_width_BW"+label,"rrv_width_BW"+label,10,5,20);
        rrv_number = ROOT.RooRealVar("rrv_number"+label,"rrv_number"+label,1800,1,100000);

        cbshape = ROOT.RooCBShape("cbshape"+label,"cbshape"+label, rrv_mass,rrv_mean_CB,rrv_sigma_CB,rrv_alpha_CB,rrv_n_CB);
        bw = ROOT.RooBreitWigner("bw"+label,"bw"+label, rrv_mass,rrv_mean_BW,rrv_width_BW);
        #model = ROOT.RooExtendPdf("model"+label,"model"+label, cbshape, rrv_number );
        cbbw = ROOT.RooFFTConvPdf("cbbw"+label,"cbbw"+label, rrv_mass, cbshape, bw);
        model = ROOT.RooExtendPdf("model"+label,"model"+label, cbbw, rrv_number );
        parameters_list=[rrv_mean_CB,rrv_sigma_CB,rrv_alpha_CB,rrv_n_CB,rrv_mean_BW,rrv_width_BW,rrv_number];

    if in_model_name == "LDGaus": # FFT: Landau*Gaus
        rrv_mean_landau=ROOT.RooRealVar("rrv_mean_landau"+label,"rrv_mean_landau"+label,83.5,80,87);
        rrv_sigma_landau=ROOT.RooRealVar("rrv_sigma_landau"+label,"rrv_sigma_landau"+label,5,2,10);
        rrv_mean_gaus=ROOT.RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,0);
        rrv_sigma_gaus=ROOT.RooRealVar("rrv_sigma_gaus"+label,"rrv_sigma_gaus"+label,16,10,20);
        rrv_number = ROOT.RooRealVar("rrv_number"+label,"rrv_number"+label,1300,1,100000);

        landau = ROOT.RooLandau("landau"+label,"landau"+label, rrv_mass,rrv_mean_landau,rrv_sigma_landau);
        gaus = ROOT.RooBreitWigner("gaus"+label,"gaus"+label, rrv_mass,rrv_mean_gaus,rrv_sigma_gaus);
        #model = ROOT.RooExtendPdf("model"+label,"model"+label, cbshape, rrv_number );
        ldgaus = ROOT.RooFFTConvPdf("ldgaus"+label,"ldgaus"+label, rrv_mass, landau, gaus);
        model = ROOT.RooExtendPdf("model"+label,"model"+label, ldgaus, rrv_number );
        parameters_list=[rrv_mean_landau,rrv_sigma_landau,rrv_mean_gaus,rrv_sigma_gaus,rrv_number];

    if in_model_name == "ErfExp" :
        rrv_c_ErfExp = ROOT.RooRealVar("rrv_c_ErfExp"+label,"rrv_c_ErfExp"+label,-0.05,-0.2,0.);
        rrv_offset_ErfExp = ROOT.RooRealVar("rrv_offset_ErfExp"+label,"rrv_offset_ErfExp"+label,78.,10.,140.);
        rrv_width_ErfExp = ROOT.RooRealVar("rrv_width_ErfExp"+label,"rrv_width_ErfExp"+label,30.,10,100.);
        rrv_number = ROOT.RooRealVar("rrv_number"+label,"rrv_number"+label,900,1,100000);

        erfExp = ROOT.RooErfExpPdf("erfExp"+label,"erfExp"+label,rrv_mass,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp);
        model = ROOT.RooExtendPdf("model"+label,"model"+label, erfExp, rrv_number );
        parameters_list=[rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp,rrv_number];

    if in_model_name == "ErfExpGaus":
        rrv_c_ErfExp = ROOT.RooRealVar("rrv_c_ErfExp"+label,"rrv_c_ErfExp"+label,-0.05,-0.2,0.);
        rrv_offset_ErfExp = ROOT.RooRealVar("rrv_offset_ErfExp"+label,"rrv_offset_ErfExp"+label,100.,10.,140.);
        rrv_width_ErfExp = ROOT.RooRealVar("rrv_width_ErfExp"+label,"rrv_width_ErfExp"+label,30.,10,100.);
        rrv_mean_gaus=ROOT.RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,82,78,87);
        rrv_sigma_gaus=ROOT.RooRealVar("rrv_sigma_gaus"+label,"rrv_sigma_gaus"+label,7,1,20);
        #rrv_high = ROOT.RooRealVar("rrv_high"+label,"rrv_high"+label,200.,0.,1000.);
        rrv_high = ROOT.RooRealVar("rrv_high"+label,"rrv_high"+label,0.7,0.,1.);
        rrv_number = ROOT.RooRealVar("rrv_number"+label,"rrv_number"+label,140,1,100000);

        #erfExp_gaus = ROOT.RooErfExp_Gaus_Pdf("erfExp_gaus"+label,"erfExp_gaus"+label, rrv_mass,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp,rrv_mean_gaus,rrv_sigma_gaus,rrv_high );
        #model = ROOT.RooExtendPdf("model"+label,"model"+label, erfExp_gaus, rrv_number );

        erfExp = ROOT.RooErfExpPdf("erfExp"+label,"erfExp"+label,rrv_mass,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp);
        gaus = ROOT.RooGaussian("gaus"+label,"gaus"+label, rrv_mass,rrv_mean_gaus,rrv_sigma_gaus);
        erfExp_gaus =ROOT.RooAddPdf("erfExp_gaus"+label,"erfExp_gaus"+label,ROOT.RooArgList(erfExp,gaus),ROOT.RooArgList(rrv_high))
        model = ROOT.RooExtendPdf("model"+label,"model"+label, erfExp_gaus, rrv_number );
        parameters_list=[rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp,rrv_mean_gaus,rrv_sigma_gaus,rrv_high,rrv_number];

#    if in_model_name == "ErfExpGaus_v2":
        #rrv_c_ErfExp = ROOT.RooRealVar("rrv_c_ErfExp"+label,"rrv_c_ErfExp"+label,-0.05,-10.,0.);
        #rrv_offset_ErfExp = ROOT.RooRealVar("rrv_offset_ErfExp"+label,"rrv_offset_ErfExp"+label,100.,10.,140.);
        #rrv_width_ErfExp = ROOT.RooRealVar("rrv_width_ErfExp"+label,"rrv_width_ErfExp"+label,30.,10,100.);
        #rrv_mean_gaus=ROOT.RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,82,78,87);
        #rrv_sigma_gaus=ROOT.RooRealVar("rrv_sigma_gaus"+label,"rrv_sigma_gaus"+label,7,1,20);
        ##rrv_high = ROOT.RooRealVar("rrv_high"+label,"rrv_high"+label,200.,0.,1000.);
        #rrv_high = ROOT.RooRealVar("rrv_high"+label,"rrv_high"+label,1,0.,10);
        #rrv_number = ROOT.RooRealVar("rrv_number"+label,"rrv_number"+label,700,1,100000);

        #erfExp_gaus = ROOT.RooErfExp_Gaus_Pdf("erfExp_gaus"+label,"erfExp_gaus"+label, rrv_mass,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp,rrv_mean_gaus,rrv_sigma_gaus,rrv_high );
        #model = ROOT.RooExtendPdf("model"+label,"model"+label, erfExp_gaus, rrv_number );

        ##erfExp = ROOT.RooErfExpPdf("erfExp"+label,"erfExp"+label,rrv_mass,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp);
        ##gaus = ROOT.RooGaussian("gaus"+label,"gaus"+label, rrv_mass,rrv_mean_gaus,rrv_sigma_gaus);
        ##erfExp_gaus =ROOT.RooAddPdf("erfExp_gaus"+label,"erfExp_gaus"+label,ROOT.RooArgList(erfExp,gaus),ROOT.RooArgList(rrv_high))
        ##model = ROOT.RooExtendPdf("model"+label,"model"+label, erfExp_gaus, rrv_number );
        #parameters_list=[rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp,rrv_mean_gaus,rrv_sigma_gaus,rrv_high,rrv_number];

    if in_model_name == "ErfExp2Gaus":
        rrv_c_ErfExp = ROOT.RooRealVar("rrv_c_ErfExp"+label,"rrv_c_ErfExp"+label,-0.1,-10.,0.);
        rrv_offset_ErfExp = ROOT.RooRealVar("rrv_offset_ErfExp"+label,"rrv_offset_ErfExp"+label,100.,10.,140.);
        rrv_width_ErfExp = ROOT.RooRealVar("rrv_width_ErfExp"+label,"rrv_width_ErfExp"+label,30.,10,100.);
        rrv_mean_gaus1=ROOT.RooRealVar("rrv_mean_gaus1"+label,"rrv_mean_gaus1"+label,82,78,87);
        rrv_sigma_gaus1=ROOT.RooRealVar("rrv_sigma_gaus1"+label,"rrv_sigma_gaus1"+label,10,0.1,100);
        rrv_high1 = ROOT.RooRealVar("rrv_high1"+label,"rrv_high1"+label,1,0.,10.);
        rrv_mean_gaus2=ROOT.RooRealVar("rrv_mean_gaus2"+label,"rrv_mean_gaus2"+label,174,160,187);
        rrv_sigma_gaus2=ROOT.RooRealVar("rrv_sigma_gaus2"+label,"rrv_sigma_gaus2"+label,20,0.1,100);
        rrv_high2 = ROOT.RooRealVar("rrv_high2"+label,"rrv_high2"+label,0.1,0.,10.);
        rrv_number = ROOT.RooRealVar("rrv_number"+label,"rrv_number"+label,2000,1,100000);

        erfExp_2gaus = ROOT.RooErfExp_2Gaus_Pdf("erfExp_2gaus"+label,"erfExp_2gaus"+label, rrv_mass,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp,rrv_mean_gaus1,rrv_sigma_gaus1,rrv_high1,rrv_mean_gaus2,rrv_sigma_gaus2,rrv_high2 );
        model = ROOT.RooExtendPdf("model"+label,"model"+label, erfExp_2gaus, rrv_number );
        parameters_list=[rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp,rrv_mean_gaus1,rrv_sigma_gaus1,rrv_high1,rrv_mean_gaus2,rrv_sigma_gaus2,rrv_high2,rrv_number];

    if in_model_name == "ErfExpVoigGaus":
        rrv_c_ErfExp = ROOT.RooRealVar("rrv_c_ErfExp"+label,"rrv_c_ErfExp"+label,-0.1,-10.,0.);
        rrv_offset_ErfExp = ROOT.RooRealVar("rrv_offset_ErfExp"+label,"rrv_offset_ErfExp"+label,100.,10.,140.);
        rrv_width_ErfExp = ROOT.RooRealVar("rrv_width_ErfExp"+label,"rrv_width_ErfExp"+label,30.,10,100.);
        rrv_mean_voig=ROOT.RooRealVar("rrv_mean_voig"+label,"rrv_mean_voig"+label,82,78,87);
        rrv_width_voig=ROOT.RooRealVar("rrv_width_voig"+label,"rrv_width_voig"+label,5,1,20);
        rrv_sigma_voig=ROOT.RooRealVar("rrv_sigma_voig"+label,"rrv_sigma_voig"+label,5,1,100);
        rrv_high1 = ROOT.RooRealVar("rrv_high1"+label,"rrv_high1"+label,1,0.,200.);
        rrv_mean_gaus=ROOT.RooRealVar("rrv_mean_gaus"+label,"rrv_mean_gaus"+label,174)#,160,187);
        rrv_sigma_gaus=ROOT.RooRealVar("rrv_sigma_gaus"+label,"rrv_sigma_gaus"+label,20)#,0.1,100);
        #rrv_high2 = ROOT.RooRealVar("rrv_high2"+label,"rrv_high2"+label,0.1,0.,10.);
        rrv_high2 = ROOT.RooRealVar("rrv_high2"+label,"rrv_high2"+label,0.)#,0.,0.);
        rrv_number = ROOT.RooRealVar("rrv_number"+label,"rrv_number"+label,2000,1,100000);

        erfExp_voig_gaus = ROOT.RooErfExp_Voig_Gaus_Pdf("erfExp_voig_gaus"+label,"erfExp_voig_gaus"+label, rrv_mass,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp,rrv_mean_voig,rrv_width_voig,rrv_sigma_voig,rrv_high1,rrv_mean_gaus,rrv_sigma_gaus,rrv_high2 );
        model = ROOT.RooExtendPdf("model"+label,"model"+label, erfExp_voig_gaus, rrv_number );
        parameters_list=[rrv_c_ErfExp,rrv_offset_ErfExp,rrv_width_ErfExp,rrv_mean_voig,rrv_width_voig,rrv_sigma_voig,rrv_high1,rrv_mean_gaus,rrv_sigma_gaus,rrv_high2,rrv_number];


    # fit to a Model
    #rfresult = model.fitTo( rdataset, ROOT.RooFit.Save(1) ,ROOT.RooFit.Extended(ROOT.kTRUE) );
    #rrv_mass.setRange("sb_lo",rrv_mass.getMin(),65); rrv_mass.setRange("sb_hi",95,rrv_mass.getMax());
    rfresult = model.fitTo( rdataset, ROOT.RooFit.Save(1), ROOT.RooFit.SumW2Error(ROOT.kTRUE) ,ROOT.RooFit.Extended(ROOT.kTRUE) );
    #rfresult = model.fitTo( rdataset, ROOT.RooFit.Save(1), ROOT.RooFit.SumW2Error(ROOT.kTRUE),ROOT.RooFit.Range("sb_lo,sb_hi") ,ROOT.RooFit.Extended(ROOT.kTRUE) );
    #rfresult = model.fitTo( rdataset, ROOT.RooFit.Save(1), ROOT.RooFit.Range("sb_lo,sb_hi"), ROOT.RooFit.SumCoefRange("sb_lo,sb_hi") ,ROOT.RooFit.Extended(ROOT.kTRUE));
    
    mplot = rrv_mass.frame(ROOT.RooFit.Title(in_file_name+" fitted by "+in_model_name));
    rdataset.plotOn( mplot ,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2) );
    #model.plotOn( mplot, ROOT.RooFit.VisualizeError(rfresult,1),ROOT.RooFit.FillColor(ROOT.kOrange) );
    #model.plotOn( mplot,ROOT.RooFit.VisualizeError(rfresult,1,ROOT.kFALSE),ROOT.RooFit.DrawOption("L"),ROOT.RooFit.LineWidth(2),ROOT.RooFit.LineColor(ROOT.kRed), ROOT.RooFit.LineStyle(ROOT.kDashed) );
    model.plotOn(mplot,ROOT.RooFit.VisualizeError(rfresult,1,ROOT.kFALSE),ROOT.RooFit.DrawOption("F"),ROOT.RooFit.FillColor(ROOT.kOrange));
    rdataset.plotOn( mplot ,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2) );
    model.plotOn( mplot );
    #model.plotOn( mplot, ROOT.RooFit.Range(rrv_mass.getMin(),rrv_mass.getMax()),ROOT.RooFit.LineStyle(2) );
    #pull
    hpull=mplot.pullHist();
    mplot_pull = rrv_mass.frame(ROOT.RooFit.Title("Pull Distribution"));
    mplot_pull.addPlotable(hpull,"P");
    mplot_pull.SetTitle("PULL");
    mplot_pull.GetYaxis().SetRangeUser(-5,5);
     
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
    #parameters_list.sort();
    for i in range(len(parameters_list)):
        latex.DrawLatex(0,0.9-i*0.08,"%s"%(parameters_list[i].GetName()) );
        latex.DrawLatex(0,0.9-i*0.08-0.04," %4.3e +/- %2.1e"%(parameters_list[i].getVal(),parameters_list[i].getError()) );
        #print "%s:  %s +/- %s"%(parameters_list[i].GetName(),parameters_list[i].getVal(),parameters_list[i].getError()) ;

    if cutOnMassDrop : rlt_file=ROOT.TString("testNhan/mdcut/"+in_file_name);
    else : rlt_file=ROOT.TString("testNhan/BDTcut/"+in_file_name);
    rlt_file.ReplaceAll(".root","_"+in_model_name+"_rlt_weight.png");
    #rlt_file.ReplaceAll(".root","_"+in_model_name+"_rlt.png");
    cMassFit.SaveAs(rlt_file.Data());
    rlt_file.ReplaceAll(".png",".eps"); 
    cMassFit.SaveAs(rlt_file.Data());
    
    rfresult.Print();

    ##chi2 fit begin
    #rdataHist=rdataset.binnedClone();
    #rdataHist.Print("v");
    #chi2=ROOT.RooChi2Var("chi2","chi2",model,rdataHist,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2));
    #m=ROOT.RooMinuit(chi2);
    #m.migrad();
    #m.hesse();
    #r_chi2_wgt=m.save();
    #mplot2 = rrv_mass.frame(ROOT.RooFit.Title(in_file_name+" fitted by "+in_model_name));
    #rdataset.plotOn( mplot2 ,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2) );
    #model.plotOn( mplot2, ROOT.RooFit.VisualizeError(rfresult,1),ROOT.RooFit.FillColor(ROOT.kOrange) );
    #rdataset.plotOn( mplot2 ,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2) );
    #model.plotOn( mplot2 );
    #cMassFit2 = ROOT.TCanvas("cMassFit2","cMassFit2",1000,800);
    #mplot2.Draw();
    #cMassFit2.SaveAs("testNhan/BDTcut/chi2.png");
    #r_chi2_wgt.Print();
    ##chi2 fit end

    ##calculate the area fraction range(60--100)/range(30--200)
    #rrv_mass.setRange("total",30,140);
    #igx_total=model.createIntegral(ROOT.RooArgSet(rrv_mass),ROOT.RooFit.NormSet(ROOT.RooArgSet(rrv_mass)),ROOT.RooFit.Range("total"));
    #rrv_mass.setRange("signal",60,100);
    #igx_signal=model.createIntegral(ROOT.RooArgSet(rrv_mass),ROOT.RooFit.NormSet(ROOT.RooArgSet(rrv_mass)),ROOT.RooFit.Range("signal"));
    #print "%s: %s"%(parameters_list[-1].GetName, parameters_list[-1].getVal());
    #parameters_list[-1].setVal(parameters_list[-1].getVal()*(1-igx_signal.getVal()/igx_total.getVal()) );
    #print "%s: %s"%(parameters_list[-1].GetName, parameters_list[-1].getVal());

    return [rfresult,parameters_list,rdataset];

######## ++++++++++++++
def fit_ClosureTest():
    #cutOnMassDrop = True;
    cutOnMassDrop = False;
    #rlt_TTB=fit_general("ofile_TTbar.root","_TTB","CBBW",cutOnMassDrop);
    rlt_TTB=fit_general("ofile_TTbar.root","_TTB","ErfExpGaus",cutOnMassDrop);
    rlt_WW=fit_general("ofile_WW.root","_WW","Voig",cutOnMassDrop);
    rlt_WJets=fit_general("ofile_WJets.root","_WJets","ErfExp",cutOnMassDrop);

    parameters_list_WJets=rlt_WJets[1];
    parameters_list_TTB=rlt_TTB[1];
    parameters_list_WW=rlt_WW[1];

    fileIn_name=[ROOT.TString("trainingtrees/ofile_WJets.root"),ROOT.TString("trainingtrees/ofile_WW.root"),ROOT.TString("trainingtrees/ofile_TTbar.root")];

    listOfTrainingVariables1 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1"];
    bdtSimple = tmvaApplicator( listOfTrainingVariables1, "weights/Wtagger_200to275_simple_BDT.weights.xml");

    rrv_mass = ROOT.RooRealVar("rrv_mass","rrv_mass",30.,140.) 
    rrv_mass.setBins(50);
    rrv_weight = ROOT.RooRealVar("rrv_weight","rrv_weight",0. ,1.) 
    rdataset = ROOT.RooDataSet("rdataset","rdataset",ROOT.RooArgSet(rrv_mass,rrv_weight),ROOT.RooFit.WeightVar(rrv_weight) ); 

    #prepare the dataset: WJets+TTB+WW
    for j in range(3):
    #for j in range(1):
        fileIn = ROOT.TFile(fileIn_name[j].Data());
        treeIn = fileIn.Get("otree");
        # make cuts (including mass drop) # create a RooDataSet
        print "N entries: ", treeIn.GetEntries()
        for i in range(treeIn.GetEntries()):
            if i % 10000 == 0: print "i: ",i
            treeIn.GetEntry(i);
            discriminantCut = False; 
                
            if cutOnMassDrop and treeIn.jet_massdrop_pr < 0.25: discriminantCut = True;
            elif not cutOnMassDrop:
                listOfVarVals = [];
                for kk in range(len(listOfTrainingVariables1)):
                    listOfVarVals.append( getattr( treeIn, listOfTrainingVariables1[kk] ) );
                BDTval = bdtSimple.eval( listOfVarVals );
                #print BDTval;
                if BDTval > 0.0: discriminantCut = True;
            else: discriminantCut = False;
            
            #if treeIn.jet_pt_pr > 200. and discriminantCut and treeIn.jet_mass_pr > 30 and treeIn.jet_mass_pr<140:
            #if treeIn.njets==0 and treeIn.nbjets>0 : print "jets num= %s, %s"%(treeIn.njets,treeIn.nbjets);
            if treeIn.jet_pt_pr > 200. and discriminantCut and treeIn.jet_mass_pr > 30 and treeIn.jet_mass_pr<140 and treeIn.njets == 0:
                rrv_mass.setVal( treeIn.jet_mass_pr );
                rdataset.add( ROOT.RooArgSet( rrv_mass ), treeIn.totalEventWeight );
    print "N_rdataset: ", rdataset.numEntries();

    #prepare the model
    #WJets shape
    rrv_c_ErfExp_WJets      = parameters_list_WJets[0];
    rrv_offset_ErfExp_WJets = parameters_list_WJets[1];
    rrv_width_ErfExp_WJets  = parameters_list_WJets[2];
    rrv_number_WJets        = parameters_list_WJets[3];
    erfExp_WJets = ROOT.RooErfExpPdf("erfExp_WJets","erfExp_WJets",rrv_mass,rrv_c_ErfExp_WJets,rrv_offset_ErfExp_WJets,rrv_width_ErfExp_WJets);
    model_WJets=ROOT.RooExtendPdf("model_WJets","model_WJets",erfExp_WJets,rrv_number_WJets);
    #rrv_c_ErfExp_WJets.setConstant(1);
    rrv_offset_ErfExp_WJets.setConstant(1);
    #rrv_width_ErfExp_WJets.setConstant(1);
    #rrv_number_WJets.setConstant(1);

    #WW shape
    rrv_mean_voig_WW  = parameters_list_WW[0];
    rrv_width_voig_WW = parameters_list_WW[1];
    rrv_sigma_voig_WW = parameters_list_WW[2];
    rrv_number_WW     = parameters_list_WW[3];
    voig_WW = ROOT.RooVoigtian("voig_WW","voig_WW", rrv_mass,rrv_mean_voig_WW,rrv_width_voig_WW,rrv_sigma_voig_WW);
    model_WW=ROOT.RooExtendPdf("model_WW","model_WW",voig_WW,rrv_number_WW);
    rrv_mean_voig_WW.setConstant(1);
    rrv_width_voig_WW.setConstant(1);
    rrv_sigma_voig_WW.setConstant(1);
    rrv_number_WW.setConstant(1);

    #TTB shape
    #rrv_mean_CB_TTB  = parameters_list_TTB[0];
    #rrv_sigma_CB_TTB = parameters_list_TTB[1];
    #rrv_alpha_CB_TTB = parameters_list_TTB[2];
    #rrv_n_CB_TTB     = parameters_list_TTB[3];
    #rrv_mean_BW_TTB  = parameters_list_TTB[4];
    #rrv_width_BW_TTB = parameters_list_TTB[5];
    #rrv_number_TTB   = parameters_list_TTB[6];
    #cbshape_TTB = ROOT.RooCBShape("cbshape_TTB","cbshape_TTB", rrv_mass,rrv_mean_CB_TTB,rrv_sigma_CB_TTB,rrv_alpha_CB_TTB,rrv_n_CB_TTB);
    #bw_TTB = ROOT.RooBreitWigner("bw_TTB","bw_TTB", rrv_mass,rrv_mean_BW_TTB,rrv_width_BW_TTB);
    #cbbw_TTB = ROOT.RooFFTConvPdf("cbbw_TTB","cbbw_TTB", rrv_mass, cbshape_TTB, bw_TTB);
    #model_TTB=ROOT.RooExtendPdf("model_TTB","model_TTB",cbbw_TTB,rrv_number_TTB);
    #rrv_mean_CB_TTB.setConstant(1);
    #rrv_sigma_CB_TTB.setConstant(1);
    #rrv_alpha_CB_TTB.setConstant(1);
    #rrv_n_CB_TTB.setConstant(1);
    #rrv_mean_BW_TTB.setConstant(1);
    #rrv_width_BW_TTB.setConstant(1);
    #rrv_number_TTB.setConstant(1);
    rrv_c_ErfExp_TTB      = parameters_list_TTB[0]
    rrv_offset_ErfExp_TTB = parameters_list_TTB[1];
    rrv_width_ErfExp_TTB  = parameters_list_TTB[2];
    rrv_mean_gaus_TTB     = parameters_list_TTB[3];
    rrv_sigma_gaus_TTB    = parameters_list_TTB[4];
    rrv_high_TTB          = parameters_list_TTB[5];
    rrv_number_TTB        = parameters_list_TTB[6];
    erfExp_TTB = ROOT.RooErfExpPdf("erfExp_TTB","erfExp_TTB",rrv_mass,rrv_c_ErfExp_TTB,rrv_offset_ErfExp_TTB,rrv_width_ErfExp_TTB);
    gaus_TTB = ROOT.RooGaussian("gaus_TTB","gaus_TTB", rrv_mass,rrv_mean_gaus_TTB,rrv_sigma_gaus_TTB);
    erfExp_gaus_TTB =ROOT.RooAddPdf("erfExp_gaus_TTB","erfExp_gaus_TTB",ROOT.RooArgList(erfExp_TTB,gaus_TTB),ROOT.RooArgList(rrv_high_TTB))
    model_TTB = ROOT.RooExtendPdf("model_TTB","model_TTB", erfExp_gaus_TTB, rrv_number_TTB );
    rrv_c_ErfExp_TTB.setConstant(1);
    rrv_offset_ErfExp_TTB.setConstant(1);
    rrv_width_ErfExp_TTB.setConstant(1);
    rrv_mean_gaus_TTB.setConstant(1);
    rrv_sigma_gaus_TTB.setConstant(1);
    rrv_high_TTB.setConstant(1);
    rrv_number_TTB.setConstant(1);

    model=ROOT.RooAddPdf("model","model",ROOT.RooArgList(model_WJets,model_WW,model_TTB));
    #model=model_WJets;
    parameters_list_orig=[rrv_c_ErfExp_WJets,rrv_offset_ErfExp_WJets,rrv_width_ErfExp_WJets,rrv_number_WJets];
    parameters_list=[];
    for para in parameters_list_orig:
        if not para.isConstant():parameters_list.append(para);
    #parameters_list=[rrv_c_ErfExp_WJets,rrv_number_WJets];
    # fit the sideband range
    rrv_mass.setRange("sb_lo",rrv_mass.getMin(),60); rrv_mass.setRange("sb_hi",100,rrv_mass.getMax());
    rfresult = model.fitTo( rdataset, ROOT.RooFit.Save(1) , ROOT.RooFit.Range("sb_lo,sb_hi") ,ROOT.RooFit.SumW2Error(ROOT.kTRUE) ,ROOT.RooFit.Extended(ROOT.kTRUE) );
    #rfresult = model.fitTo( rdataset, ROOT.RooFit.Save(1) ,ROOT.RooFit.Range("sb_lo,sb_hi")  ,ROOT.RooFit.Extended(ROOT.kTRUE));
    #rfresult = model.fitTo( rdataset, ROOT.RooFit.Save(1) ,ROOT.RooFit.SumW2Error(ROOT.kTRUE)  ,ROOT.RooFit.Extended(ROOT.kTRUE));

    mplot = rrv_mass.frame(ROOT.RooFit.Title("Closure test: WJets+TTBar+WW"));
    rdataset.plotOn( mplot ,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2) );
    #model.plotOn(mplot, ROOT.RooFit.VisualizeError(rfresult,1), ROOT.RooFit.FillColor(ROOT.kOrange), ROOT.RooFit.Range(rrv_mass.getMin(),rrv_mass.getMax()) );
    model.plotOn(mplot,ROOT.RooFit.VisualizeError(rfresult,1,ROOT.kFALSE),ROOT.RooFit.DrawOption("F"),ROOT.RooFit.FillColor(ROOT.kOrange),ROOT.RooFit.Range(rrv_mass.getMin(),rrv_mass.getMax()));
    rdataset.plotOn( mplot ,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2) );
    model.plotOn(mplot );
    model.plotOn(mplot, ROOT.RooFit.Components("model_WJets"), ROOT.RooFit.LineStyle(ROOT.RooFit.kDashed),ROOT.RooFit.LineColor(ROOT.kBlack) );
    model.plotOn(mplot, ROOT.RooFit.Components("model_WW"),ROOT.RooFit.LineStyle(ROOT.RooFit.kDashed),ROOT.RooFit.LineColor(ROOT.kRed));
    model.plotOn(mplot, ROOT.RooFit.Components("model_TTB"),ROOT.RooFit.LineStyle(ROOT.RooFit.kDashed),ROOT.RooFit.LineColor(6));
    model.plotOn( mplot );
    model.plotOn( mplot, ROOT.RooFit.Range(rrv_mass.getMin(),rrv_mass.getMax()),ROOT.RooFit.LineStyle(ROOT.kDashed) );

    #pull
    hpull=mplot.pullHist();
    mplot_pull = rrv_mass.frame(ROOT.RooFit.Title("Pull Distribution"));
    mplot_pull.addPlotable(hpull,"P");
    mplot_pull.SetTitle("PULL");
    mplot_pull.GetYaxis().SetRangeUser(-5,5);

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
    #parameters_list.sort();
    for i in range(len(parameters_list)):
        latex.DrawLatex(0,0.9-i*0.08,"%s"%(parameters_list[i].GetName()) );
        latex.DrawLatex(0,0.9-i*0.08-0.04," %4.3e +/- %2.1e"%(parameters_list[i].getVal(),parameters_list[i].getError()) );

    if cutOnMassDrop : rlt_file=ROOT.TString("testNhan/mdcut/closure_test.png");
    else : rlt_file=ROOT.TString("testNhan/BDTcut/closure_test.png");
    cMassFit.SaveAs(rlt_file.Data());
    rlt_file.ReplaceAll(".png",".eps"); 
    cMassFit.SaveAs(rlt_file.Data());
    

    rfresult.Print();
 ######## ++++++++++++++

def fit_AllSamples():
    #cutOnMassDrop = True;
    cutOnMassDrop = False;
    #rlt_WW=fit_general("ofile_WW.root","_WW","Voig",cutOnMassDrop);
    rlt_TTB=fit_general("ofile_TTbar.root","_TTB","ErfExpGaus",cutOnMassDrop);
    #rlt_TTB=fit_general("ofile_TTbar.root","_TTB","Voig",cutOnMassDrop);
    #rlt_WJets=fit_general("ofile_WJets.root","_WJets","ErfExp",cutOnMassDrop);
    print "________________________________________________________________________"
    #rlt_WJets[0].Print();
    #rlt_WW[0].Print();
    #rlt_TTB[0].Print();

if __name__ == '__main__':
    #fit_AllSamples();
    fit_ClosureTest();
