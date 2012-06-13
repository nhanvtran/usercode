import ROOT
ROOT.gROOT.ProcessLine(".L tdrstyle.C")
from ROOT import setTDRStyle
ROOT.setTDRStyle()
ROOT.gStyle.SetPalette(1)

ROOT.gSystem.Load('RooUnfold-1.1.1/libRooUnfold.so')
from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes

#ROOT.gROOT.ProcessLine('.L myutils.C++')
from ROOT import myutils, TH1F

ROOT.TH1.SetDefaultSumw2()
ROOT.TH2.SetDefaultSumw2()

ROOT.gStyle.SetPadLeftMargin(0.16);

from array import array
import math

def NormalizeToUnity( h1 ):
    h1.Scale( 1./h1.Integral() );

class PlotterSimple: 

    def __init__( self, file1, file2, odir ):
        self.fin1 = ROOT.TFile( file1 );
        self.fin2 = ROOT.TFile( file2 );    
        self.theOdir = odir;
        self.label1 = "chan1"
        self.label2 = "chan2"
    
    def setLabels( self, label1, label2 ):
        self.label1 = label1;
        self.label2 = label2;
    
    def plotSingle( self, hname, canname ):
        
        leg = ROOT.TLegend(0.7,0.7,0.9,0.9)
        leg.SetFillColor(0)
        leg.SetBorderSize(0)
            
        h1o = self.fin1.Get(hname);
        h2o = self.fin2.Get(hname);
    
        h1 = h1o.Rebin(2);
        h2 = h2o.Rebin(2);
        
        NormalizeToUnity( h1 );
        NormalizeToUnity( h2 );        
        h1.SetLineColor( ROOT.kRed );
        h2.SetLineColor( ROOT.kBlue );
        leg.AddEntry( h1, self.label1, "l" )
        leg.AddEntry( h2, self.label2, "l" )        
        
        c0 = ROOT.TCanvas("c0","c0",800,800)
        c0.cd()
#        h1.SetMinimum(1e-6);
#        h1.SetMaximum(1);        
        h1.Draw("histe");
        h2.Draw("histesames");
#        ROOT.gPad.SetLogy();
        leg.Draw()
        c0.Print( self.theOdir+"/"+canname+".eps", "eps");