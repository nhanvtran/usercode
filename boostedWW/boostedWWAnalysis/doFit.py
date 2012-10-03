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
    
def fitWJets(cutOnMassDrop):

    # read in tree
    fileIn = ROOT.TFile("trainingtrees/ofile_WJets.root");
    treeIn = fileIn.Get("otree");
    
    # define bdt reader
    listOfTrainingVariables1 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1"];
    bdtSimple = tmvaApplicator( listOfTrainingVariables1, "weights/Wtagger_200to275_simple_BDT.weights.xml");
        
    rrv_mass = ROOT.RooRealVar("rrv_mass","rrv_mass",30.,200.)
    rdataset = ROOT.RooDataSet("rdataset","rdataset",ROOT.RooArgSet(rrv_mass));
    
    rrv_c = ROOT.RooRealVar("rrv_c","rrv_c",-0.1,-10.,0.)
    rrv_offset = ROOT.RooRealVar("rrv_offset","rrv_offset",50.,10.,100.)    
    rrv_sigma = ROOT.RooRealVar("rrv_sigma","rrv_sigma",10.,0,100.)        
    bkg_Wjets = ROOT.RooErfExpPdf("bkg_Wjets","bkg_Wjets",rrv_mass,rrv_c,rrv_offset,rrv_sigma) 
    
    # make cuts (including mass drop)
    # create a RooDataSet
    print "N entries: ", treeIn.GetEntries()
    for i in range(treeIn.GetEntries()):
        
        if i % 1000 == 0: print "i: ",i
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
    
        if treeIn.jet_pt_pr > 200. and discriminantCut and treeIn.jet_mass_pr > 30:
#            print treeIn.jet_mass_pr
            rrv_mass.setVal( treeIn.jet_mass_pr );
            rdataset.add( ROOT.RooArgSet( rrv_mass ) );
            
    print "N_rdataset: ", rdataset.numEntries();

    # fit to a Landau
    rfresult = bkg_Wjets.fitTo( rdataset, ROOT.RooFit.Save(1) );
    
    mplot = rrv_mass.frame();
    rdataset.plotOn( mplot );
    bkg_Wjets.plotOn( mplot );
    
    cMassFit = ROOT.TCanvas("cMassFit","cMassFit",800,800);
    cMassFit.cd();
    mplot.Draw();
    cMassFit.SaveAs("testNhan/massFitWjets.eps");

    return rfresult;

######## ++++++++++++++

def fitTTbar(cutOnMassDrop):
    
    # read in tree
    fileIn = ROOT.TFile("trainingtrees/ofile_TTbar.root");
    treeIn = fileIn.Get("otree");
    
    # define bdt reader
    listOfTrainingVariables1 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1"];
    bdtSimple = tmvaApplicator( listOfTrainingVariables1, "weights/Wtagger_200to275_simple_BDT.weights.xml");
    
    rrv_mass = ROOT.RooRealVar("rrv_mass","rrv_mass",30.,200.)
    rdataset = ROOT.RooDataSet("rdataset","rdataset",ROOT.RooArgSet(rrv_mass));
    
    rrv_c = ROOT.RooRealVar("rrv_c","rrv_c",-0.1,-10.,0.)
    rrv_offset = ROOT.RooRealVar("rrv_offset","rrv_offset",50.,10.,100.)    
    rrv_sigma = ROOT.RooRealVar("rrv_sigma","rrv_sigma",10.,0,100.)        
    bkg_continuum = ROOT.RooErfExpPdf("bkg_Wjets","bkg_Wjets",rrv_mass,rrv_c,rrv_offset,rrv_sigma) 
#    rrv_offset = ROOT.RooRealVar("rrv_offset","rrv_offset",50.,10.,80.)    
#    rrv_sigma = ROOT.RooRealVar("rrv_sigma","rrv_sigma",20.,0,50.)        
#    bkg_continuum = ROOT.RooLandau("bkg_Wjets","bkg_Wjets",rrv_mass,rrv_offset,rrv_sigma) 
#    rrv_m = ROOT.RooRealVar("rrv_m","rrv_m",85,70,90)
#    rrv_offsetL = ROOT.RooRealVar("rrv_offsetL","rrv_offsetL",25,1.,40)    
#    rrv_offsetR = ROOT.RooRealVar("rrv_offsetR","rrv_offsetR",30,1.,40)        
#    bkg_continuum = ROOT.RooBifurGauss("bkg_continuum","bkg_continuum",rrv_mass,rrv_m,rrv_offsetL,rrv_offsetR)        
    
    rrv_gmean = ROOT.RooRealVar("rrv_gmean","rrv_gmean",83.,75.,90.)    
    rrv_gsigma = ROOT.RooRealVar("rrv_gsigma","rrv_gsigma",8.,0,50.)        
    bkg_peak = ROOT.RooGaussian("bkg_peak","bkg_peak",rrv_mass,rrv_gmean,rrv_gsigma) 
    
    rrv_gmean2 = ROOT.RooRealVar("rrv_gmean2","rrv_gmean2",173.)    
    rrv_gsigma2 = ROOT.RooRealVar("rrv_gsigma2","rrv_gsigma2",5.,0.,10.)        
    bkg_peak2 = ROOT.RooGaussian("bkg_peak2","bkg_peak2",rrv_mass,rrv_gmean2,rrv_gsigma2) 
    
    rrv_frac = ROOT.RooRealVar("rrv_frac","rrv_frac",0.7,0.,1.)        
    bkg_all0 = ROOT.RooAddPdf("bkg_all0","bkg_all0",bkg_continuum,bkg_peak,rrv_frac);

    rrv_frac2 = ROOT.RooRealVar("rrv_frac2","rrv_frac2",0.5,0,1.)        
    bkg_all = ROOT.RooAddPdf("bkg_all","bkg_all",bkg_all0,bkg_peak2,rrv_frac2);
    
    # make cuts (including mass drop)
    # create a RooDataSet
    print "N entries: ", treeIn.GetEntries()
    for i in range(treeIn.GetEntries()):
        
        if i % 1000 == 0: print "i: ",i
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
        
        if treeIn.jet_pt_pr > 200. and discriminantCut and treeIn.jet_mass_pr > 30:
            #            print treeIn.jet_mass_pr
            rrv_mass.setVal( treeIn.jet_mass_pr );
            rdataset.add( ROOT.RooArgSet( rrv_mass ) );
    
    print "N_rdataset: ", rdataset.numEntries();
    
    # fit to a Landau
    rfresult = bkg_all.fitTo( rdataset, ROOT.RooFit.Save(1) );
    
    mplot = rrv_mass.frame();
    rdataset.plotOn( mplot );
    bkg_all.plotOn( mplot );
    
    cMassFit = ROOT.TCanvas("cMassFit","cMassFit",800,800);
    cMassFit.cd();
    mplot.Draw();
    cMassFit.SaveAs("testNhan/massFitTTbar.eps");
    
#    return rfresult;

######## ++++++++++++++

def fitWW(cutOnMassDrop):
    
    # read in tree
    fileIn = ROOT.TFile("trainingtrees/ofile_WW.root");
    treeIn = fileIn.Get("otree");
    
    # define bdt reader
    listOfTrainingVariables1 = ["jet_massdrop_pr","jet_qjetvol","jet_tau2tau1"];
    bdtSimple = tmvaApplicator( listOfTrainingVariables1, "weights/Wtagger_200to275_simple_BDT.weights.xml");
    
    rrv_mass = ROOT.RooRealVar("rrv_mass","rrv_mass",30.,200.)
    rdataset = ROOT.RooDataSet("rdataset","rdataset",ROOT.RooArgSet(rrv_mass));
    
#    rrv_c = ROOT.RooRealVar("rrv_c","rrv_c",-0.1,-10.,0.)
#    rrv_offset = ROOT.RooRealVar("rrv_offset","rrv_offset",50.,10.,100.)    
#    rrv_sigma = ROOT.RooRealVar("rrv_sigma","rrv_sigma",10.,0,100.)        
#    bkg_continuum = ROOT.RooErfExpPdf("bkg_Wjets","bkg_Wjets",rrv_mass,rrv_c,rrv_offset,rrv_sigma) 
    rrv_offset = ROOT.RooRealVar("rrv_offset","rrv_offset",50.,10.,100.)    
    rrv_sigma = ROOT.RooRealVar("rrv_sigma","rrv_sigma",10.,0,100.)        
    bkg_continuum = ROOT.RooLandau("bkg_Wjets","bkg_Wjets",rrv_mass,rrv_offset,rrv_sigma) 

    rrv_gmean = ROOT.RooRealVar("rrv_gmean","rrv_gmean",50.,10.,100.)    
    rrv_gsigma = ROOT.RooRealVar("rrv_gsigma","rrv_gsigma",10.,0,100.)        
    bkg_peak = ROOT.RooGaussian("bkg_peak","bkg_peak",rrv_mass,rrv_gmean,rrv_gsigma) 

    rrv_frac = ROOT.RooRealVar("rrv_frac","rrv_frac",0.5,0,1.)        
    bkg_all = ROOT.RooAddPdf("bkg_all","bkg_all",bkg_continuum,bkg_peak,rrv_frac);
    
    # make cuts (including mass drop)
    # create a RooDataSet
    print "N entries: ", treeIn.GetEntries()
    for i in range(treeIn.GetEntries()):
        
        if i % 1000 == 0: print "i: ",i
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
        
        if treeIn.jet_pt_pr > 200. and discriminantCut and treeIn.jet_mass_pr > 30:
            #            print treeIn.jet_mass_pr
            rrv_mass.setVal( treeIn.jet_mass_pr );
            rdataset.add( ROOT.RooArgSet( rrv_mass ) );
    
    print "N_rdataset: ", rdataset.numEntries();
    
    # fit to a Landau
    rfresult = bkg_all.fitTo( rdataset, ROOT.RooFit.Save(1) );
    
    mplot = rrv_mass.frame();
    rdataset.plotOn( mplot );
    bkg_all.plotOn( mplot );
    
    cMassFit = ROOT.TCanvas("cMassFit","cMassFit",800,800);
    cMassFit.cd();
    mplot.Draw();
    cMassFit.SaveAs("testNhan/massFitWW.eps");
    
    return rfresult;

######## ++++++++++++++


if __name__ == '__main__':

    cutOnMassDrop = True;
    
#    fitWJets(cutOnMassDrop);
    fitTTbar(cutOnMassDrop);
#    fitWW(cutOnMassDrop);
