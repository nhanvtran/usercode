#! /usr/bin/env python
import os
import glob
import math
import array
import sys
import time

from array import array

import ROOT
from ROOT import gROOT, gStyle, gSystem, TLatex
import subprocess
from subprocess import Popen
from optparse import OptionParser

#from condorUtils import submitBatchJob

ROOT.gStyle.SetPadLeftMargin(0.16);

############################################################
############################################
#            Job steering                  #
############################################
parser = OptionParser()

parser.add_option('-b', action='store_true', dest='noX', default=False,
                  help='no X11 windows')

parser.add_option('--makeCards', action='store_true', dest='makeCards', default=False,
                  help='no X11 windows')
parser.add_option('--computeLimits', action='store_true', dest='computeLimits', default=False,
                  help='no X11 windows')
parser.add_option('--plotLimits', action='store_true', dest='plotLimits', default=False,
                  help='no X11 windows')

# submit jobs to condor
parser.add_option('--batchMode', action='store_true', dest='batchMode', default=False,
                  help='no X11 windows')


parser.add_option('--channel',action="store",type="string",dest="channel",default="mu")
parser.add_option('--massPoint',action="store",type="int",dest="massPoint",default=-1)
parser.add_option('--cPrime',action="store",type="int",dest="cPrime",default=-1)
parser.add_option('--brNew',action="store",type="int",dest="brNew",default=-1)
parser.add_option('--odir',action="store",type="string",dest="odir",default=".")
parser.add_option('--sigChannel',action="store",type="string",dest="sigChannel",default='')


(options, args) = parser.parse_args()
############################################################

############################################################
def getAsymLimits(file):
    
    
    f = ROOT.TFile(file);
    t = f.Get("limit");
    entries = t.GetEntries();
    
    lims = [0,0,0,0,0,0];
    
    for i in range(entries):
        
        t.GetEntry(i);
        t_quantileExpected = t.quantileExpected;
        t_limit = t.limit;
        
        #print "limit: ", t_limit, ", quantileExpected: ",t_quantileExpected;
        
        if t_quantileExpected == -1.: lims[0] = t_limit;
        elif t_quantileExpected >= 0.024 and t_quantileExpected <= 0.026: lims[1] = t_limit;
        elif t_quantileExpected >= 0.15 and t_quantileExpected <= 0.17: lims[2] = t_limit;            
        elif t_quantileExpected == 0.5: lims[3] = t_limit;            
        elif t_quantileExpected >= 0.83 and t_quantileExpected <= 0.85: lims[4] = t_limit;
        elif t_quantileExpected >= 0.974 and t_quantileExpected <= 0.976: lims[5] = t_limit;
        else: print "Unknown quantile!"
    
    return lims;

############################################################
############################################################
############################################################

def makeSMLimits(SIGCH):

    mass  = [ 600, 700, 800, 900,1000]    
    cprime = 10;
    brnew = 00;
    
    xbins = array('d', [])
    xbins_env = array('d', [])
    ybins_exp = array('d', [])
    ybins_obs = array('d', [])            
    ybins_1s = array('d', [])                        
    ybins_2s = array('d', [])    
    
    for i in range(len(mass)):
        curFile = "higgsCombinehwwlvj_ggH%03d_em%s_%02d_%02d_unbin.Asymptotic.mH%03d.root"%(mass[i],SIGCH,cprime,brnew,mass[i]);
        print "curFile: ",curFile
        curAsymLimits = getAsymLimits(curFile);
        xbins.append( mass[i] );
        xbins_env.append( mass[i] );                                
        ybins_exp.append( curAsymLimits[3] );                
        ybins_obs.append( curAsymLimits[0] );                                
        ybins_2s.append( curAsymLimits[1] );                                
        ybins_1s.append( curAsymLimits[2] ); 

    for i in range( len(mass)-1, -1, -1 ):
        curFile = "higgsCombinehwwlvj_ggH%03d_em%s_%02d_%02d_unbin.Asymptotic.mH%03d.root"%(mass[i],SIGCH,cprime,brnew,mass[i]);
        curAsymLimits = getAsymLimits(curFile);   
        xbins_env.append( mass[i] );                                
        ybins_2s.append( curAsymLimits[5] );                                
        ybins_1s.append( curAsymLimits[4] ); 
    

    curGraph_exp = ROOT.TGraph(nPoints,xbins,ybins_exp);
    curGraph_obs = ROOT.TGraph(nPoints,xbins,ybins_obs);
    curGraph_1s = ROOT.TGraph(nPoints*2,xbins_env,ybins_1s);
    curGraph_2s = ROOT.TGraph(nPoints*2,xbins_env,ybins_2s);
    
    curGraph_exp.SetLineStyle(2);
    curGraph_exp.SetLineWidth(2);
    curGraph_obs.SetLineWidth(2);                    
    curGraph_exp.SetMarkerSize(2);
    curGraph_obs.SetMarkerSize(2);                    
    curGraph_1s.SetFillColor(ROOT.kGreen);
    curGraph_2s.SetFillColor(ROOT.kYellow);

    # -------
    banner = TLatex(0.4,0.91,("CMS Preliminary, 19.3 fb^{-1} at #sqrt{s}=8TeV, e+#mu"));
    banner.SetNDC(); banner.SetTextSize(0.028);
    oneLine = ROOT.TF1("oneLine","1",599,1001);
    oneLine.SetLineColor(ROOT.kRed);
    oneLine.SetLineWidth(3);

    can_SM = ROOT.TCanvas("can_SM","can_SM",800,800);
    hrl_SM = can_SM.DrawFrame(599,0.0,1001,10.0);
    hrl_SM.GetYaxis().SetTitle("#mu = #sigma_{95%} / #sigma_{SM}");
    hrl_SM.GetYaxis().SetTitleOffset(1.4);
    hrl_SM.GetXaxis().SetTitle("Higgs boson mass (GeV)");
    can_SM.SetGrid();
    
    curGraph_2s.Draw("F");
    curGraph_1s.Draw("F");
    curGraph_obs.Draw("PL");
    curGraph_exp.Draw("PL");
    
    leg2 = ROOT.TLegend(0.25,0.65,0.75,0.85);
    leg2.SetFillStyle(0);
    leg2.SetBorderSize(0);
    leg2.AddEntry(curGraph_obs,"Observed","L")
    leg2.AddEntry(curGraph_exp,"Expected","L")
    leg2.AddEntry(curGraph_1s,"Expected, #pm 1#sigma","F")
    leg2.AddEntry(curGraph_2s,"Expected, #pm 2#sigma","F")
    leg2.AddEntry(oneLine,"SM Expected","L")

    leg2.Draw();
    banner.Draw();
    oneLine.Draw("LESAMES");
    
    #ROOT.gPad.SetLogy();
    can_SM.SaveAs("limitFigs/SMLim%s.eps"%(SIGCH));                      
    can_SM.SaveAs("limitFigs/SMLim%s.png"%(SIGCH));                      
    can_SM.SaveAs("limitFigs/SMLim%s.pdf"%(SIGCH));                      

############################################################
############################################################
############################################################

def makeBSMLimits_versusSigmaAndMu( SIGCH, cprimes ):

    mass  = [ 600, 700, 800, 900,1000]    
    curcolors = [1,2,4,6]
    brnew = 00;
    
    massCS  = [];
    if SIGCH == "":
        massCS.append( (0.5230 + 0.09688) );
        massCS.append( (0.2288 + 0.06330) );
        massCS.append( (0.1095 + 0.04365) );
        massCS.append( (0.05684 + 0.03164) );
        massCS.append( (0.03163 + 0.02399) );
    elif SIGCH == "_ggH":
        massCS.append( (0.5230) );
        massCS.append( (0.2288) );
        massCS.append( (0.1095) );
        massCS.append( (0.05684) );
        massCS.append( (0.03163) );
    elif SIGCH == "_vbfH":
        massCS.append( (0.09688) );
        massCS.append( (0.06330) );
        massCS.append( (0.04365) );
        massCS.append( (0.03164) );
        massCS.append( (0.02399) );
    else:
        print "problem!"
    massBRWW = [5.58E-01,5.77E-01,5.94E-01,6.09E-01,6.21E-01]    
    
    gridMax = -999;
    gridMaxSig = -999;

    tGraphs_exp = [];
    tGraphs_obs = [];    
    tGraphs_csXbr_exp = [];
    tGraphs_csXbr_obs = [];    
    tGraphs_csXbr_th = [];    
    
    for j in range(len(cprimes)):
    
        xbins = array('d', [])
        ybins_exp = array('d', [])
        ybins_obs = array('d', [])            
        ybins_csXbr_exp = array('d', [])
        ybins_csXbr_obs = array('d', [])            
        ybins_csXbr_th = array('d', [])            
        
        for i in range(len(mass)):
            curFile = "higgsCombinehwwlvj_ggH%03d_em%s_%02d_%02d_unbin.Asymptotic.mH%03d.root"%(mass[i],SIGCH,cprimes[j],brnew,mass[i]);
            print "curFile: ",curFile
            curAsymLimits = getAsymLimits(curFile);
            xbins.append( mass[i] );
            ybins_exp.append( curAsymLimits[3] );                
            ybins_obs.append( curAsymLimits[0] );    
            ybins_csXbr_exp.append( curAsymLimits[3]*massCS[i]*cprime[j]*0.1*(1-brnew*0.1)*massBRWW[i] );                
            ybins_csXbr_obs.append( curAsymLimits[0]*massCS[i]*cprime[j]*0.1*(1-brnew*0.1)*massBRWW[i] );    
            ybins_csXbr_th.append( 1.*massCS[i]*cprime[j]*0.1*(1-brnew*0.1)*massBRWW[i] );    
        
            print "curAsymLimits[0]: ",curAsymLimits[0]
            
            if gridMax < curAsymLimits[3]: gridMax = curAsymLimits[3];
            cscur = ( curAsymLimits[3]*massCS[i]*cprime[j]*0.1*(1-brnew*0.1)*massBRWW[i] );
            if gridMaxSig < cscur: gridMaxSig = cscur;
        
        curGraph_exp = ROOT.TGraph(nPoints,xbins,ybins_exp);
        curGraph_obs = ROOT.TGraph(nPoints,xbins,ybins_obs);        
        curGraph_exp.SetLineStyle(2);
        curGraph_exp.SetLineWidth(2);
        curGraph_obs.SetLineWidth(2);                    
        curGraph_exp.SetMarkerSize(2);
        curGraph_obs.SetMarkerSize(2);

        curGraph_csXbr_exp = ROOT.TGraph(nPoints,xbins,ybins_csXbr_exp);
        curGraph_csXbr_obs = ROOT.TGraph(nPoints,xbins,ybins_csXbr_obs);        
        curGraph_csXbr_th = ROOT.TGraph(nPoints,xbins,ybins_csXbr_th);
        curGraph_csXbr_exp.SetLineStyle(2);
        curGraph_csXbr_exp.SetLineWidth(2);
        curGraph_csXbr_obs.SetLineWidth(2);                    
        curGraph_csXbr_exp.SetMarkerSize(2);
        curGraph_csXbr_obs.SetMarkerSize(2);
        curGraph_csXbr_th.SetLineWidth(2);        

        tGraphs_exp.append( curGraph_exp );
        tGraphs_obs.append( curGraph_obs );
        tGraphs_csXbr_exp.append( curGraph_csXbr_exp );
        tGraphs_csXbr_obs.append( curGraph_csXbr_obs );
        tGraphs_csXbr_th.append( curGraph_csXbr_th );

    # -------
    banner = TLatex(0.4,0.91,("CMS Preliminary, 19.3 fb^{-1} at #sqrt{s}=8TeV, e+#mu"));
    banner.SetNDC(); banner.SetTextSize(0.028);
    
    can_BSM = ROOT.TCanvas("can_BSM","can_BSM",800,800);
    hrl_BSM = can_BSM.DrawFrame(599,0.0,1001,gridMax*1.5);
    hrl_BSM.GetYaxis().SetTitle("#mu = #sigma_{95%} / #sigma_{SM}");
    hrl_BSM.GetYaxis().SetTitleOffset(1.4);
    hrl_BSM.GetXaxis().SetTitle("Higgs boson mass (GeV)");
    can_BSM.SetGrid();
    
    leg2 = ROOT.TLegend(0.25,0.65,0.75,0.85);
    leg2.SetFillStyle(0);
    leg2.SetBorderSize(0);
    leg2.SetNColumns(2);

    for k in range(len(cprimes)):
        print cprime[k]
        tGraphs_exp[k].SetLineStyle(2);
        tGraphs_exp[k].SetLineColor(curcolors[k]);
        tGraphs_obs[k].SetLineColor(curcolors[k]);                
        tGraphs_exp[k].SetLineWidth(2);
        tGraphs_obs[k].SetLineWidth(2);                
        tGraphs_exp[k].Draw("PL");
        tGraphs_obs[k].Draw("PL");   

        tmplabel = "exp., C'^{2} = %1.1f    "%( float((cprimes[k])/10.) )
        leg2.AddEntry(tGraphs_exp[k],tmplabel,"L")        
        tmplabel = "obs., C'^{2} = %1.1f"%( float((cprimes[k])/10.) )
        leg2.AddEntry(tGraphs_obs[k],tmplabel,"L");        
    
    leg2.Draw();
    banner.Draw();
    
    #ROOT.gPad.SetLogy();
    can_BSM.SaveAs("limitFigs/BSMLim%s_Mu.eps"%(SIGCH));                      
    can_BSM.SaveAs("limitFigs/BSMLim%s_Mu.png"%(SIGCH));                      
    can_BSM.SaveAs("limitFigs/BSMLim%s_Mu.pdf"%(SIGCH));          

    ##----

    can_BSMsig = ROOT.TCanvas("can_BSMsig","can_BSMsig",800,800);
    hrl_BSMsig = can_BSMsig.DrawFrame(599,0.0,1001,gridMaxSig*1.8);
    hrl_BSMsig.GetYaxis().SetTitle("#sigma_{95%} (pb)");
    hrl_BSMsig.GetYaxis().SetTitleOffset(1.4);
    hrl_BSMsig.GetXaxis().SetTitle("Higgs boson mass (GeV)");
    can_BSMsig.SetGrid();

    leg2 = ROOT.TLegend(0.2,0.65,0.85,0.85);
    leg2.SetFillStyle(0);
    leg2.SetBorderSize(0);
    leg2.SetNColumns(3);

    for k in range(len(cprimes)):
        print cprime[k]
        tGraphs_csXbr_exp[k].SetLineStyle(2);
        tGraphs_csXbr_exp[k].SetLineColor(curcolors[k]);
        tGraphs_csXbr_obs[k].SetLineColor(curcolors[k]);                
        tGraphs_csXbr_th[k].SetLineStyle(3);
        tGraphs_csXbr_th[k].SetLineColor(curcolors[k]);                        
        tGraphs_csXbr_exp[k].SetLineWidth(2);
        tGraphs_csXbr_obs[k].SetLineWidth(2);                
        tGraphs_csXbr_exp[k].Draw("PL");
        tGraphs_csXbr_obs[k].Draw("PL");   
        tGraphs_csXbr_th[k].Draw("PL");   
        
        tmplabel = "exp., C'^{2} = %1.1f    "%( float((cprimes[k])/10.) )
        leg2.AddEntry(tGraphs_csXbr_exp[k],tmplabel,"L")        
        tmplabel = "obs., C'^{2} = %1.1f    "%( float((cprimes[k])/10.) )
        leg2.AddEntry(tGraphs_csXbr_obs[k],tmplabel,"L");        
        tmplabel = "th., C'^{2} = %1.1f"%( float((cprimes[k])/10.) )
        leg2.AddEntry(tGraphs_csXbr_th[k],tmplabel,"L");        

    leg2.Draw();
    banner.Draw();

    #ROOT.gPad.SetLogy();
    can_BSMsig.SaveAs("limitFigs/BSMLim%s_Sigma.eps"%(SIGCH));                      
    can_BSMsig.SaveAs("limitFigs/BSMLim%s_Sigma.png"%(SIGCH));                      
    can_BSMsig.SaveAs("limitFigs/BSMLim%s_Sigma.pdf"%(SIGCH));  


##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
################################ M A I N #################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################

if __name__ == '__main__':
    
    
    ###############
    
    CHAN = options.channel;
    DIR = "cards_"+CHAN;
    SIGCH = "";
    if options.sigChannel.find("H") >= 0: SIGCH = "_"+options.sigChannel;
        
    
    mass  = [ 600, 700, 800, 900,1000]
    ccmlo = [ 550, 600, 700, 750, 800]  
    ccmhi = [ 700, 850, 950,1100,1200]  
    mjlo  = [  40,  40,  40,  40,  40]  
    mjhi  = [ 130, 130, 130, 130, 130]  
    mlo   = [ 400, 400, 600, 600, 600]      
    mhi   = [1000,1000,1400,1400,1400]          
    shape    = ["ErfPowExp_v1","ErfPowExp_v1","Exp","Exp","Exp"]
    shapeAlt = [  "ErfPow2_v1",  "ErfPow2_v1","Pow","Pow","Pow"]
        
    BRnew = [0,1,2,3,4,5];
    cprime = [1,2,3,4,5,6,7,8,9,10];    
    massCS  = [];
    massCS.append( (0.5230 + 0.09688) );
    massCS.append( (0.2288 + 0.06330) );
    massCS.append( (0.1095 + 0.04365) );
    massCS.append( (0.05684 + 0.03164) );
    massCS.append( (0.03163 + 0.02399) );
    massBRWW = [5.58E-01,5.77E-01,5.94E-01,6.09E-01,6.21E-01]

    moreCombineOpts = "";
    
    ###############

    if options.computeLimits or options.plotLimits: os.chdir("cards_em");

    # put in functionality to test just one mass point or just one cprime
    nMasses = len(mass);
    mLo = 0;
    mHi = nMasses;
    nCprimes = len(cprime);
    cpLo = 0;
    cpHi = nCprimes;
    nBRnews = len(BRnew);
    brLo = 0;
    brHi = nBRnews;
    
    if options.massPoint > 0:   
        curIndex = mass.index(options.massPoint);
        mLo = curIndex;
        mHi = curIndex+1;
    if options.cPrime > 0:   
        curIndex = cprime.index(options.cPrime);
        cpLo = curIndex;
        cpHi = curIndex+1;
        nCprimes = 1;
    if options.brNew >= 0:   
        curIndex = BRnew.index(options.brNew);
        brLo = curIndex;
        brHi = curIndex+1;
        nBRnews = 1;  


# =====================================
    
    nGraphs = nCprimes*2 + 2;
    
    tGraphs = [];
    tGraphs_csXbr_exp = [];
    tGraphs_csXbr_obs = [];
    tGraphs_csXbr_vsBRnew_exp = [];
    tGraphs_csXbr_vsBRnew_obs = [];    
    tGraphs_csXbr_obs = [];

    nPoints = len(mass);
    
    if options.plotLimits:
        
        makeSMLimits( SIGCH );
        cprimes = [3,6,8,10];    
        makeBSMLimits_versusSigmaAndMu( SIGCH, cprimes );
#        makeBSMLimits_2D( SIGCH );
        
        
#        ##        for i in range(mLo,mHi):
#        ##            for j in range(cpLo,cpHi):
#        for j in range(cpHi-1,cpLo-1,-1):
#            
#            xbins = array('d', [])
#            xbins_brnew = array('d', [])
#            ybins_exp = array('d', [])
#            ybins_obs = array('d', [])            
#            ybins_exp_csXbr_exp = array('d', [])
#            ybins_obs_csXbr_obs = array('d', [])            
#            ybins_csXbr_vsBRnew_exp = array('d', [])
#            ybins_csXbr_vsBRnew_obs = array('d', [])            
#            xbins_env = array('d', [])
#            ybins_1s = array('d', [])                        
#            ybins_2s = array('d', [])                        
#            
#            for i in range(mLo,mHi):
#                
#                curFile = "higgsCombinehwwlvj_ggH%03d_em_%02d_00_unbin.Asymptotic.mH%03d.root"%(mass[i],cprime[j],mass[i]);
#                curAsymLimits = getAsymLimits(curFile);
#                
#                xbins.append( mass[i] );
#                ybins_exp.append( curAsymLimits[3] );                
#                ybins_obs.append( curAsymLimits[0] );                                
#                xbins_env.append( mass[i] );                                
#                ybins_2s.append( curAsymLimits[1] );                                
#                ybins_1s.append( curAsymLimits[2] );   
#                
#                # for cs x br:
#                ybins_exp_csXbr_exp.append( curAsymLimits[3]*massCS[i]*massBRWW[i]*cprime[j]*0.1 );                
#                ybins_obs_csXbr_obs.append( curAsymLimits[0]*massCS[i]*massBRWW[i]*cprime[j]*0.1 );          
#            
#            
#            for i in range(nBRnews):
#                
#                print "BRnew[i]: ",BRnew[i],", cprime[j]: ",cprime[j],", mu' = ",massCS[0]*cprime[j]*0.1*(1-BRnew[i]*0.1)
#                
#                curFile = "higgsCombinehwwlvj_ggH600_em_%02d_%02d_unbin.Asymptotic.mH%03d.root"%(cprime[j],BRnew[i],mass[0]);
#                curAsymLimits = getAsymLimits(curFile);
#                
#                xbins_brnew.append( BRnew[i]*0.1 );                
#                # for cs x br:
#                ybins_csXbr_vsBRnew_exp.append( curAsymLimits[3]*massCS[0]*cprime[j]*0.1*(1-BRnew[i]*0.1)*massBRWW[0] );                
#                ybins_csXbr_vsBRnew_obs.append( curAsymLimits[0]*massCS[0]*cprime[j]*0.1*(1-BRnew[i]*0.1)*massBRWW[0] );              
#
#                
#            #print "mass: ", mass[i], ", cprime: ", cprime[j], " -- obs: ", curAsymLimits[0], ", exp: ", curAsymLimits[3];
#            
#            #                if nCprimes > 1:
#            #                    limitsHist_exp.SetBinContent(i+1,j+1,curAsymLimits[3]);
#            #                    limitsHist_obs.SetBinContent(i+1,j+1,curAsymLimits[0]);                    
#            
#            for i in range(mHi-1,mLo-1,-1):
#                curFile = "higgsCombinehwwlvj_ggH%03d_em_%02d_00_unbin.Asymptotic.mH%03d.root"%(mass[i],cprime[j],mass[i]);
#                curAsymLimits = getAsymLimits(curFile);
#                
#                xbins_env.append( mass[i] );                                
#                ybins_2s.append( curAsymLimits[5] );                                
#                ybins_1s.append( curAsymLimits[4] );                                                
#            
#            curGraph_exp = ROOT.TGraph(nPoints,xbins,ybins_exp);
#            curGraph_obs = ROOT.TGraph(nPoints,xbins,ybins_obs);
#            curGraph_1s = ROOT.TGraph(nPoints*2,xbins_env,ybins_1s);
#            curGraph_2s = ROOT.TGraph(nPoints*2,xbins_env,ybins_2s);
#            
#            curGraph_exp.SetLineStyle(2);
#            curGraph_exp.SetLineWidth(2);
#            curGraph_obs.SetLineWidth(2);                    
#            curGraph_exp.SetMarkerSize(2);
#            curGraph_obs.SetMarkerSize(2);                    
#            curGraph_1s.SetFillColor(ROOT.kGreen);
#            curGraph_2s.SetFillColor(ROOT.kYellow);
#            
#            tGraphs.append(curGraph_exp);
#            tGraphs.append(curGraph_obs);
#            tGraphs.append(curGraph_1s);
#            tGraphs.append(curGraph_2s);
#        
#            curGraph_csXbr_exp = ROOT.TGraph(nPoints,xbins,ybins_exp_csXbr_exp);
#            curGraph_csXbr_obs = ROOT.TGraph(nPoints,xbins,ybins_obs_csXbr_obs);
#            tGraphs_csXbr_exp.append(curGraph_csXbr_exp);
#            tGraphs_csXbr_obs.append(curGraph_csXbr_obs);
#
#            curGraph_csXbr_vsBRnew_exp = ROOT.TGraph(6,xbins_brnew,ybins_csXbr_vsBRnew_exp);
#            curGraph_csXbr_vsBRnew_obs = ROOT.TGraph(6,xbins_brnew,ybins_csXbr_vsBRnew_obs);
#            tGraphs_csXbr_vsBRnew_exp.append(curGraph_csXbr_vsBRnew_exp);
#            tGraphs_csXbr_vsBRnew_obs.append(curGraph_csXbr_vsBRnew_obs);
#    
#        # -------
#        banner = TLatex(0.17,0.91,("CMS Preliminary, 19.3 fb^{-1} at #sqrt{s}=8TeV, e+#mu"));
#        banner.SetNDC(); banner.SetTextSize(0.028);
#
#        can_xs = ROOT.TCanvas("can_xs","can_xs",800,800);
#        hrl_xs = can_xs.DrawFrame(599,0.015,1001,2.0);
#        hrl_xs.GetYaxis().SetTitle("#sigma_{95%} #times  BR_{WW} (pb)");
#        hrl_xs.GetXaxis().SetTitle("mass (GeV)");
#        can_xs.SetGrid();
#        
#        curcolors = [1,2,4,6]
#        kc = 0;
#        for k in range(nCprimes):
#            print cprime[k]
#            if cprime[k] == 3 or cprime[k] == 6 or cprime[k] == 8 or cprime[k] == 10:
#                tGraphs_csXbr_exp[k].SetLineStyle(2);
#                tGraphs_csXbr_exp[k].SetLineColor(curcolors[kc]);
#                tGraphs_csXbr_obs[k].SetLineColor(curcolors[kc]);                
#                tGraphs_csXbr_exp[k].SetLineWidth(2);
#                tGraphs_csXbr_obs[k].SetLineWidth(2);                
#                tGraphs_csXbr_exp[k].Draw("PL");
#                tGraphs_csXbr_obs[k].Draw("PL");   
#                kc += 1;                    
#        
#        leg2 = ROOT.TLegend(0.25,0.65,0.75,0.85);
#        leg2.SetFillStyle(0);
#        leg2.SetBorderSize(0);
#        leg2.SetNColumns(2);
#        leg2.AddEntry(tGraphs_csXbr_exp[0],"BR_{new} = 0","")
#        leg2.AddEntry(0,"","")
#        for k in range(nCprimes):
#            if cprime[k] == 3 or cprime[k] == 6 or cprime[k] == 8 or cprime[k] == 10:            
#                tmplabel = "exp., C'^{2} = %1.1f    "%( float((cprime[k])/10.) )
#                leg2.AddEntry(tGraphs_csXbr_exp[k],tmplabel,"L")
#                tmplabel = "obs., C'^{2} = %1.1f"%( float((cprime[k])/10.) )
#                leg2.AddEntry(tGraphs_csXbr_obs[k],tmplabel,"L");        
#
#        leg2.Draw();
#        banner.Draw();
#        
#        ROOT.gPad.SetLogy();
#        can_xs.SaveAs("limitFigs/test_cPrime_csXbr.eps");    
#                    
#        # -------
#        banner = TLatex(0.17,0.91,("CMS Preliminary, 19.3 fb^{-1} at #sqrt{s}=8TeV, e+#mu"));
#        banner.SetNDC(); banner.SetTextSize(0.028);
#        
#        can_xs_vsBRnew = ROOT.TCanvas("can_xs_vsBRnew","can_xs_vsBRnew",800,800);
#        hrl_xs_vsBRnew = can_xs_vsBRnew.DrawFrame(-0.01,0.02,0.51,2.0);
#        hrl_xs_vsBRnew.GetYaxis().SetTitle("#sigma_{95%} #times  BR_{WW} (pb)");
#        hrl_xs_vsBRnew.GetXaxis().SetTitle("BR_{new}");
#        can_xs_vsBRnew.SetGrid();
#        
#        curcolors = [1,2,4,6]
#        kc = 0;
#        for k in range(nCprimes):
#            print cprime[k]
#            if cprime[k] == 3 or cprime[k] == 6 or cprime[k] == 8 or cprime[k] == 10:
#                tGraphs_csXbr_vsBRnew_exp[k].SetLineStyle(2);
#                tGraphs_csXbr_vsBRnew_exp[k].SetLineColor(curcolors[kc]);
#                tGraphs_csXbr_vsBRnew_obs[k].SetLineColor(curcolors[kc]);                
#                tGraphs_csXbr_vsBRnew_exp[k].SetLineWidth(2);
#                tGraphs_csXbr_vsBRnew_obs[k].SetLineWidth(2);                
#                tGraphs_csXbr_vsBRnew_exp[k].Draw("PL");
#                tGraphs_csXbr_vsBRnew_obs[k].Draw("PL");   
#                kc += 1;                    
#        
#        leg2 = ROOT.TLegend(0.25,0.65,0.75,0.85);
#        leg2.SetFillStyle(0);
#        leg2.SetBorderSize(0);
#        leg2.SetNColumns(2);
#        leg2.AddEntry(tGraphs_csXbr_exp[0],"m_{H} = 600 GeV","")
#        leg2.AddEntry(0,"","")
#        for k in range(nCprimes):
#            if cprime[k] == 3 or cprime[k] == 6 or cprime[k] == 8 or cprime[k] == 10:            
#                tmplabel = "exp., C'^{2} = %1.1f    "%( float((cprime[k])/10.) )
#                leg2.AddEntry(tGraphs_csXbr_vsBRnew_exp[k],tmplabel,"L")
#                tmplabel = "obs., C'^{2} = %1.1f"%( float((cprime[k])/10.) )
#                leg2.AddEntry(tGraphs_csXbr_vsBRnew_obs[k],tmplabel,"L");        
#        
#        leg2.Draw();
#        banner.Draw();
#        
#        ROOT.gPad.SetLogy();
#        can_xs_vsBRnew.SaveAs("limitFigs/test_cPrime_csXbr_vsBRnew800.eps");                      
#        
#        # ----------
#        # ----------
#        # ----------
#        # ----------
#        # ----------
#        # ----------
#        # ----------
#        # ----------
#                
#        cprimeHist = [0.05,0.15,0.25,0.35,0.45,0.6,0.8,1.2];
#        massHist = [550,650,750,850,950,1050];
#        limitsHist_exp = ROOT.TH2F("limitsHist_exp","",nPoints,550,1050,nCprimes,0.05,1.05);
#        limitsHist_obs = ROOT.TH2F("limitsHist_obs","",nPoints,550,1050,nCprimes,0.05,1.05);
#        
#        limitsHist_exp_600_2D = ROOT.TH2F("limitsHist_exp_600_2D","",nCprimes,0.05,1.05,nBRnews,-0.05,0.55);
#        limitsHist_obs_600_2D = ROOT.TH2F("limitsHist_obs_600_2D","",nCprimes,0.05,1.05,nBRnews,-0.05,0.55); 
#        
#        for j in range(cpLo,cpHi):
#            for i in range(mLo,mHi):
#                curFile = "higgsCombinehwwlvj_ggH%03d_em_%02d_00_unbin.Asymptotic.mH%03d.root"%(mass[i],cprime[j],mass[i]);
#                curAsymLimits = getAsymLimits(curFile);
#                limitsHist_exp.SetBinContent(i+1,j+1,curAsymLimits[3]);
#                limitsHist_obs.SetBinContent(i+1,j+1,curAsymLimits[0]);          
#        
#        for j in range(cpLo,cpHi):
#            for i in range(brLo,brHi):
#                curFile = "higgsCombinehwwlvj_ggH%03d_em_%02d_%02d_unbin.Asymptotic.mH%03d.root"%(600,cprime[j],BRnew[i],600);
#                curAsymLimits = getAsymLimits(curFile);
#                limitsHist_exp_600_2D.SetBinContent(j+1,i+1,curAsymLimits[3]);
#                limitsHist_obs_600_2D.SetBinContent(j+1,i+1,curAsymLimits[0]);          
#        
#        
#        limitsHist_exp.SetTitle("; mass (GeV); C'^{2}; Expected Upper Limit, #mu'");
#        limitsHist_obs.SetTitle("; mass (GeV); C'^{2}; Observed Upper Limit, #mu'");
#        limitsHist_exp.GetZaxis().RotateTitle(1);
#        limitsHist_obs.GetZaxis().RotateTitle(1);
#        
#        limitsHist_exp_600_2D.SetTitle("; C'^{2}; BR_{New}; Expected Upper Limit, #mu'");
#        limitsHist_obs_600_2D.SetTitle("; C'^{2}; BR_{New}; Observed Upper Limit, #mu'");
#        limitsHist_exp_600_2D.GetZaxis().RotateTitle(1);
#        limitsHist_obs_600_2D.GetZaxis().RotateTitle(1);
#        
#        can2d_exp = ROOT.TCanvas("can2d_exp","can2d_exp",1000,800);
#        limitsHist_exp.SetStats(0);
#        limitsHist_exp.Draw("colz");
#        banner.Draw();
#        can2d_exp.SaveAs("limitFigs/test2D_exp.eps");
#        
#        can2d_obs = ROOT.TCanvas("can2d_obs","can2d_obs",1000,800);
#        limitsHist_obs.SetStats(0);
#        limitsHist_obs.Draw("colz");
#        banner.Draw();
#        can2d_obs.SaveAs("limitFigs/test2D_obs.eps");
#        
#        can2dbr_exp = ROOT.TCanvas("can2dbr_exp","can2dbr_exp",1000,800);
#        limitsHist_exp_600_2D.SetStats(0);
#        limitsHist_exp_600_2D.Draw("colz");
#        banner.Draw();
#        can2dbr_exp.SaveAs("limitFigs/test2Dbr_exp.eps");
#        
#        can2dbr_obs = ROOT.TCanvas("can2dbr_obs","can2dbr_obs",1000,800);
#        limitsHist_obs_600_2D.SetStats(0);
#        limitsHist_obs_600_2D.Draw("colz");
#        banner.Draw();
#        can2dbr_obs.SaveAs("limitFigs/test2Dbr_obs.eps");


