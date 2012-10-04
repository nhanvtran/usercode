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
## ---------------------------------------------------
## ---------------------------------------------------
## ---------------------------------------------------
    
def fit_general(in_file_name, in_model_name,cutOnMassDrop):

    # read in tree
    fileIn_name=ROOT.TString("trainingtrees/"+in_file_name);
    fileIn = ROOT.TFile(fileIn_name.Data());
    treeIn = fileIn.Get("otree");
    
    # define bdt reader
    listOfTrainingVariables1 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1"];
    bdtSimple = tmvaApplicator( listOfTrainingVariables1, "weights/Wtagger_200to275_simple_BDT.weights.xml");
        
    rrv_mass = ROOT.RooRealVar("rrv_mass","rrv_mass",30.,200.) 
    #rrv_mass = ROOT.RooRealVar("rrv_mass","rrv_mass",30.,140.)
    rdataset = ROOT.RooDataSet("rdataset","rdataset",ROOT.RooArgSet(rrv_mass)); 
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
        
        if treeIn.jet_pt_pr > 200. and discriminantCut and treeIn.jet_mass_pr > 30 and treeIn.jet_mass_pr<200:
#            print treeIn.jet_mass_pr
            rrv_mass.setVal( treeIn.jet_mass_pr );
            rdataset.add( ROOT.RooArgSet( rrv_mass ) );
            
    print "N_rdataset: ", rdataset.numEntries();

    #model
    if in_model_name == "ErfExp" :
        rrv_c_ErfExp = ROOT.RooRealVar("rrv_c_ErfExp","rrv_c_ErfExp",-0.1,-10.,0.);
        rrv_offset_ErfExp = ROOT.RooRealVar("rrv_offset_ErfExp","rrv_offset_ErfExp",50.,10.,100.);
        rrv_sigma_ErfExp = ROOT.RooRealVar("rrv_sigma_ErfExp","rrv_sigma_ErfExp",10.,0,100.);  
        model = ROOT.RooErfExpPdf("model","model",rrv_mass,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_sigma_ErfExp);
    if in_model_name == "ErfExpGaus":
        rrv_c_ErfExp = ROOT.RooRealVar("rrv_c_ErfExp","rrv_c_ErfExp",-0.1,-10.,0.);
        rrv_offset_ErfExp = ROOT.RooRealVar("rrv_offset_ErfExp","rrv_offset_ErfExp",100.,10.,140.);
        rrv_sigma_ErfExp = ROOT.RooRealVar("rrv_sigma_ErfExp","rrv_sigma_ErfExp",30.,0,100.);
        erfExp = ROOT.RooErfExpPdf("erfExp","erfExp",rrv_mass,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_sigma_ErfExp);

        rrv_mean_gaus=ROOT.RooRealVar("rrv_mean_gaus","rrv_mean_gaus",82,78,87);
        rrv_sigma_gaus=ROOT.RooRealVar("rrv_sigma_gaus","rrv_sigma_gaus",5,0.1,100);
        gaussian = ROOT.RooGaussian("gaussian","gaussian",rrv_mass,rrv_mean_gaus,rrv_sigma_gaus);

        rrv_frac1 = ROOT.RooRealVar("rrv_frac1","rrv_frac1",0.5,0.,1.);
        model = ROOT.RooAddPdf("model","model", ROOT.RooArgList(erfExp, gaussian), ROOT.RooArgList(rrv_frac1) );
    if in_model_name == "ErfExpGausGaus":
        rrv_c_ErfExp = ROOT.RooRealVar("rrv_c_ErfExp","rrv_c_ErfExp",-0.1,-10.,0.);
        rrv_offset_ErfExp = ROOT.RooRealVar("rrv_offset_ErfExp","rrv_offset_ErfExp",100.,10.,200.);
        rrv_sigma_ErfExp = ROOT.RooRealVar("rrv_sigma_ErfExp","rrv_sigma_ErfExp",30.,0,100.);
        erfExp = ROOT.RooErfExpPdf("erfExp","erfExp",rrv_mass,rrv_c_ErfExp,rrv_offset_ErfExp,rrv_sigma_ErfExp);

        rrv_mean_gaus1=ROOT.RooRealVar("rrv_mean_gaus1","rrv_mean_gaus1",82,78,87);
        rrv_sigma_gaus1=ROOT.RooRealVar("rrv_sigma_gaus1","rrv_sigma_gaus1",5,0.1,100);
        gaussian1 = ROOT.RooGaussian("gaussian1","gaussian1",rrv_mass,rrv_mean_gaus1,rrv_sigma_gaus1);

        rrv_mean_gaus2=ROOT.RooRealVar("rrv_mean_gaus2","rrv_mean_gaus2",173,160,187);
        rrv_sigma_gaus2=ROOT.RooRealVar("rrv_sigma_gaus2","rrv_sigma_gaus2",10,1,100);
        gaussian2 = ROOT.RooGaussian("gaussian2","gaussian2",rrv_mass,rrv_mean_gaus2,rrv_sigma_gaus2);

        rrv_frac1 = ROOT.RooRealVar("rrv_frac1","rrv_frac1",0.5,0.,1.);
        rrv_frac2 = ROOT.RooRealVar("rrv_frac2","rrv_frac2",0.5,0.,1.);
        model = ROOT.RooAddPdf("model","model", ROOT.RooArgList(erfExp, gaussian1, gaussian2), ROOT.RooArgList(rrv_frac1,rrv_frac2) );
     

    # fit to a Model
    rfresult = model.fitTo( rdataset, ROOT.RooFit.Save(1) );
    rfresult = model.fitTo( rdataset, ROOT.RooFit.Save(1) );
    
    mplot = rrv_mass.frame(ROOT.RooFit.Title(in_file_name+" fitted by "+in_model_name));
    rdataset.plotOn( mplot );
    model.plotOn( mplot );
    if in_model_name == "ErfExpGaus":
        model.plotOn(mplot, ROOT.RooFit.Components("gaussian"), ROOT.RooFit.LineStyle(ROOT.RooFit.kDashed));
        model.plotOn(mplot, ROOT.RooFit.Components("erfExp"),ROOT.RooFit.LineStyle(ROOT.RooFit.kDashed),ROOT.RooFit.LineColor(ROOT.RooFit.kRed));
   
    if in_model_name == "ErfExpGausGaus":
        model.plotOn(mplot, ROOT.RooFit.Components("gaussian1"), ROOT.RooFit.LineStyle(ROOT.RooFit.kDashed));
        model.plotOn(mplot, ROOT.RooFit.Components("gaussian2"), ROOT.RooFit.LineStyle(ROOT.RooFit.kDashed),ROOT.RooFit.LineColor(6));
        model.plotOn(mplot, ROOT.RooFit.Components("erfExp"),ROOT.RooFit.LineStyle(ROOT.RooFit.kDashed),ROOT.RooFit.LineColor(ROOT.RooFit.kRed));
     
    cMassFit = ROOT.TCanvas("cMassFit","cMassFit",800,800);
    cMassFit.cd();
    mplot.Draw();

    if cutOnMassDrop : rlt_file=ROOT.TString("testNhan/mdcut/"+in_file_name);
    else : rlt_file=ROOT.TString("testNhan/BDTcut/"+in_file_name);
    rlt_file.ReplaceAll(".root","_"+in_model_name+"_rlt.png");
    cMassFit.SaveAs(rlt_file.Data());
    rlt_file.ReplaceAll(".png",".eps"); 
    cMassFit.SaveAs(rlt_file.Data());

    return rfresult;

######## ++++++++++++++


if __name__ == '__main__':

    cutOnMassDrop = True;
    #cutOnMassDrop = False;
    
    fit_general("ofile_WJets.root","ErfExp",cutOnMassDrop);
    fit_general("ofile_WW.root","ErfExpGaus",cutOnMassDrop);
    fit_general("ofile_TTbar.root","ErfExpGausGaus",cutOnMassDrop);
