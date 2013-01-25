#! /usr/bin/env python
import os
import glob
import math
import array
import ROOT
from array import array
from ROOT import gROOT, gStyle, gSystem, TLatex
import subprocess
from subprocess import Popen

ROOT.gROOT.ProcessLine(".L ~/tdrstyle.C")
from ROOT import setTDRStyle
ROOT.setTDRStyle()
ROOT.gStyle.SetPadTopMargin(0.09);
ROOT.gStyle.SetPadLeftMargin(0.16);
ROOT.gStyle.SetPalette(1);

from optparse import OptionParser

############################################################

parser = OptionParser()

parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
parser.add_option('-c', '--channel',action="store",type="string",dest="channel",default="mu")
parser.add_option('-m','--mass', action="store", type="int", dest="mass", default=600, help='mass to check')

(options, args) = parser.parse_args()
############################################################

if __name__ == '__main__':

    fileName = "../trainingtrees_"+options.channel+"/ofile_ggH"+str(options.mass)+".root";
    file = ROOT.TFile(fileName);
    tree = file.Get("otree");
    
    print "n: ", tree.GetEntries()


    masses_min = {600:200, 700:200, 800:250, 900:400, 1000:400}
    masses_max = {600:1000, 700:1000, 800:1200, 900:1600, 1000:1600}
    
    h_01 = ROOT.TH1F("h_01","h_01",50,masses_min[options.mass],masses_max[options.mass]);
    h_02 = ROOT.TH1F("h_02","h_02",50,masses_min[options.mass],masses_max[options.mass]);
    h_03 = ROOT.TH1F("h_03","h_03",50,masses_min[options.mass],masses_max[options.mass]);
    h_04 = ROOT.TH1F("h_04","h_04",50,masses_min[options.mass],masses_max[options.mass]);    
    h_05 = ROOT.TH1F("h_05","h_05",50,masses_min[options.mass],masses_max[options.mass]);    
    h_07 = ROOT.TH1F("h_07","h_07",50,masses_min[options.mass],masses_max[options.mass]);    
    h_10 = ROOT.TH1F("h_10","h_10",50,masses_min[options.mass],masses_max[options.mass]);        

    for i in range(tree.GetEntries()):
        
        tree.GetEntry(i);
        h_01.Fill( tree.genHMass,tree.interference_Weight_H600*tree.bsmReweight_cPrime01_brNew00 );
        h_02.Fill( tree.genHMass,tree.interference_Weight_H600*tree.bsmReweight_cPrime02_brNew00 );
        h_03.Fill( tree.genHMass,tree.interference_Weight_H600*tree.bsmReweight_cPrime03_brNew00 );
        h_04.Fill( tree.genHMass,tree.interference_Weight_H600*tree.bsmReweight_cPrime04_brNew00 );
        h_05.Fill( tree.genHMass,tree.interference_Weight_H600*tree.bsmReweight_cPrime05_brNew00 );
        h_07.Fill( tree.genHMass,tree.interference_Weight_H600*tree.bsmReweight_cPrime07_brNew00 );    
        h_10.Fill( tree.genHMass,tree.interference_Weight_H600*tree.bsmReweight_cPrime10_brNew00 );        
        

    can = ROOT.TCanvas("can","can",800,800);

    maxY = max(h_01.GetMaximum(),h_02.GetMaximum(),h_03.GetMaximum(),h_04.GetMaximum(),h_05.GetMaximum(),h_07.GetMaximum(),h_10.GetMaximum());

    h_01.SetLineColor(ROOT.kBlue-3);
    h_02.SetLineColor(ROOT.kBlue-2);
    h_03.SetLineColor(ROOT.kBlue-1);
    h_04.SetLineColor(ROOT.kMagenta);
    h_05.SetLineColor(ROOT.kRed+1);
    h_07.SetLineColor(ROOT.kRed+2);
    h_10.SetLineColor(ROOT.kRed+3);
    h_01.SetMaximum( 2.0*maxY );
    h_01.Draw();
    h_02.Draw("sames");
    h_03.Draw("sames");
    h_04.Draw("sames");
    h_05.Draw("sames");
    h_07.Draw("sames");
    h_10.Draw("sames");
    
    ROOT.gPad.SetLogy();
    can.SaveAs("test_"+options.channel+"_"+str(options.mass)+".eps");

    print "end"
        

    
