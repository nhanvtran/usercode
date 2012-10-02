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

if __name__ == '__main__':
    
    # read in tree
    fileIn = ROOT.TFile("trainingtrees/ofile_WJets.root");
    treeIn = fileIn.Get("otree");

    hmass = ROOT.TH1F("hmass","hmass",40,0,200);
    
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
    
        treeIn.GetEntry(i);
#        print treeIn.jet_pt_pr,",",treeIn.jet_massdrop_pr
        
        if treeIn.jet_pt_pr > 200. and treeIn.jet_massdrop_pr < 0.25 and treeIn.jet_mass_pr > 30:
            hmass.Fill(treeIn.jet_mass_pr);
    
            rrv_mass.setVal( treeIn.jet_mass_pr );
            rdataset.add( ROOT.RooArgSet( rrv_mass ) );
            
    print "N_h: ", hmass.GetEntries();
    print "N_rdataset: ", rdataset.numEntries();

    # fit to a Landau
    bkg_Wjets.fitTo( rdataset );

    # plot on canvas
    cMass = ROOT.TCanvas("cMass","cMass",800,800);
    cMass.cd();
    hmass.Draw("hist");
    cMass.SaveAs("testNhan/mass.eps");

#RooPlot *xplot = ZZMass.frame();
#set->plotOn(xplot);
#sigPDF.plotOn(xplot);
    
    mplot = rrv_mass.frame();
    rdataset.plotOn( mplot );
    bkg_Wjets.plotOn( mplot );
    
    cMassFit = ROOT.TCanvas("cMassFit","cMassFit",800,800);
    cMassFit.cd();
    mplot.Draw();
    cMassFit.SaveAs("testNhan/massFit.eps");

