#!/usr/bin/env python
from ROOT import *
from ProducePlot import *
import os
import os.path
import optparse

usage = "usage: %prog [options] arg"
parser = optparse.OptionParser(usage)
parser.add_option("-b","--batch",action="store_true",default=False)
parser.add_option("-f","--sourcefilename",action="store",type="string",dest="sourcefilename")
parser.add_option("-t","--treename",action="store",type="string",dest="treename")
parser.add_option("-l","--lumi",action="store",type="float",dest="lumi")
parser.add_option("-s","--scalefilename",action="store",type="string",dest="scalefilename")
parser.add_option("-c","--cuts",action="store",type="string",dest="cuts")
(options, args) = parser.parse_args()

if os.path.isfile('tdrstyle.C'):
   gROOT.ProcessLine('.L tdrstyle.C')
   ROOT.setTDRStyle()
   print "Found tdrstyle.C file, using this style."
   HasCMSStyle = True
   if os.path.isfile('CMSTopStyle.cc'):
      gROOT.ProcessLine('.L CMSTopStyle.cc+')
      style = CMSTopStyle()
      style.setupICHEPv1()
      print "Found CMSTopStyle.cc file, use TOP style if requested in xml file."

#Settings
cut = ""
cutforfile = "controlPlots"
plotdirectort = "controlPlots"
filedirectory = ""
LUMI = 2.374
Treename = "WJet"
Scalefilename = "MCScaleFactors.txt"

if options.batch:
   gROOT.SetBatch()

if options.sourcefilename:
   filedirectory = options.sourcefilename
   
if options.treename:
   Treename = options.treename

if options.lumi:
   LUMI = float(options.lumi)

if options.scalefilename:
   Scalefilename = options.scalefilename

if options.cuts:
   cut = options.cuts
   #print cut

plot0 = ProducePlot()
plot0.SetBinMinMax(50,200,800)
plot0.SetCutWeightName(cut,"effwt*puwt")
plot0.SetFilePath(filedirectory)
plot0.SetLumiTree(LUMI,Treename)
plot0.SetPlotDir(plotdirectort)
plot0.SetLogy(True)
plot0.DrawTHStack("boostedW_lvj_m",0,"Mass(lvj)","GeV",Scalefilename,2,0.01,cutforfile)

plot1 = ProducePlot()
plot1.SetBinMinMax(20,0,400)
plot1.SetCutWeightName(cut,"effwt*puwt")
plot1.SetFilePath(filedirectory)
plot1.SetLumiTree(LUMI,Treename)
plot1.SetPlotDir(plotdirectort)
plot1.SetLogy(True)
plot1.DrawTHStack("W_muon_pt",0,"Muon Pt[GeV/c]","GeV",Scalefilename,2,0.01,cutforfile)

plot2 = ProducePlot()
plot2.SetBinMinMax(21,-2.1,2.1)
plot2.SetCutWeightName(cut,"effwt*puwt")
plot2.SetFilePath(filedirectory)
plot2.SetLumiTree(LUMI,Treename)
plot2.SetPlotDir(plotdirectort)
plot2.SetLogy(True)
plot2.DrawTHStack("W_muon_eta",0,"Muon #eta","",Scalefilename,2,0.01,cutforfile)

plot3 = ProducePlot()
plot3.SetBinMinMax(50,0,500)
plot3.SetCutWeightName(cut,"effwt*puwt")
plot3.SetFilePath(filedirectory)
plot3.SetLumiTree(LUMI,Treename)
plot3.SetPlotDir(plotdirectort)
plot3.SetLogy(True)
plot3.DrawTHStack("event_metMVA_met",0,"MVAMET[GeV/c]","GeV",Scalefilename,2,0.01,cutforfile)

plot4 = ProducePlot()
plot4.SetBinMinMax(40,0,140)
plot4.SetCutWeightName(cut,"effwt*puwt")
plot4.SetFilePath(filedirectory)
plot4.SetLumiTree(LUMI,Treename)
plot4.SetPlotDir(plotdirectort)
plot4.SetLogy(True)
plot4.DrawTHStack("GroomedJet_CA8_mass_pr",0,"CA8 Pruned Jet Mass [GeV/c]","GeV",Scalefilename,2,0.01,cutforfile)

plot5 = ProducePlot()
plot5.SetBinMinMax(40,0,40)
plot5.SetCutWeightName(cut,"effwt*puwt")
plot5.SetFilePath(filedirectory)
plot5.SetLumiTree(LUMI,Treename)
plot5.SetPlotDir(plotdirectort)
plot5.SetLogy(True)
plot5.DrawTHStack("event_nPV",0,"Number of Primary Vertices","",Scalefilename,2,0.01,cutforfile)

plot6 = ProducePlot()
plot6.SetBinMinMax(35,150,500)
plot6.SetCutWeightName(cut,"effwt*puwt")
plot6.SetFilePath(filedirectory)
plot6.SetLumiTree(LUMI,Treename)
plot6.SetPlotDir(plotdirectort)
plot6.SetLogy(True)
plot6.DrawTHStack("W_pt",0,"Leptonic W Pt [GeV/c]","GeV",Scalefilename,2,0.01,cutforfile)

plot7 = ProducePlot()
plot7.SetBinMinMax(35,150,500)
plot7.SetCutWeightName(cut,"effwt*puwt")
plot7.SetFilePath(filedirectory)
plot7.SetLumiTree(LUMI,Treename)
plot7.SetPlotDir(plotdirectort)
plot7.SetLogy(True)
plot7.DrawTHStack("GroomedJet_CA8_pt_pr",0,"CA8 Pruned Jet Pt [GeV/c]","GeV",Scalefilename,2,0.01,cutforfile)

plot8 = ProducePlot()
plot8.SetBinMinMax(20,0,1)
plot8.SetCutWeightName(cut,"effwt*puwt")
plot8.SetFilePath(filedirectory)
plot8.SetLumiTree(LUMI,Treename)
plot8.SetPlotDir(plotdirectort)
plot8.SetLogy(True)
plot8.DrawTHStack("GroomedJet_CA8_massdrop_pr",0,"CA8 Pruned Jet Mass Drop","",Scalefilename,2,0.01,cutforfile)

plot9 = ProducePlot()
plot9.SetBinMinMax(20,0.,1)
plot9.SetCutWeightName(cut,"effwt*puwt")
plot9.SetFilePath(filedirectory)
plot9.SetLumiTree(LUMI,Treename)
plot9.SetPlotDir(plotdirectort)
plot9.SetLogy(True)
plot9.DrawTHStack("GroomedJet_CA8_mass_sensi_tr",0,"CA8 Trimmed Jet Mass Sensitivity","",Scalefilename,2,0.01,cutforfile)

plot10 = ProducePlot()
plot10.SetBinMinMax(20,0.2,1)
plot10.SetCutWeightName(cut,"effwt*puwt")
plot10.SetFilePath(filedirectory)
plot10.SetLumiTree(LUMI,Treename)
plot10.SetPlotDir(plotdirectort)
plot10.SetLogy(True)
plot10.DrawTHStack("GroomedJet_CA8_mass_sensi_ft",0,"CA8 Filter Jet Mass Sensitivity","",Scalefilename,2,0.01,cutforfile)

plot11 = ProducePlot()
plot11.SetBinMinMax(20,0,1)
plot11.SetCutWeightName(cut,"effwt*puwt")
plot11.SetFilePath(filedirectory)
plot11.SetLumiTree(LUMI,Treename)
plot11.SetPlotDir(plotdirectort)
plot11.SetLogy(True)
plot11.DrawTHStack("GroomedJet_CA8_mass_sensi_pr",0,"CA8 Pruned Jet Mass Sensitivity","",Scalefilename,2,0.01,cutforfile)

plot12 = ProducePlot()
plot12.SetBinMinMax(20,0,1.5)
plot12.SetCutWeightName(cut,"effwt*puwt")
plot12.SetFilePath(filedirectory)
plot12.SetLumiTree(LUMI,Treename)
plot12.SetPlotDir(plotdirectort)
plot12.SetLogy(True)
plot12.DrawTHStack("GroomedJet_CA8_tau2tau1",0,"n-subjettiness Tau2/Tau1","",Scalefilename,2,0.01,cutforfile)

plot13 = ProducePlot()
plot13.SetBinMinMax(20,0,0.5)
plot13.SetCutWeightName(cut,"effwt*puwt")
plot13.SetFilePath(filedirectory)
plot13.SetLumiTree(LUMI,Treename)
plot13.SetPlotDir(plotdirectort)
plot13.SetLogy(True)
plot13.DrawTHStack("GroomedJet_CA8_qjetmassvolatility",0,"CA8 QJet Mass Volatility","",Scalefilename,2,0.01,cutforfile)

plot14 = ProducePlot()
plot14.SetBinMinMax(20,0.5,1)
plot14.SetCutWeightName(cut + "(GroomedJet_CA8_prsubjet1ptoverjetpt > GroomedJet_CA8_prsubjet2ptoverjetpt)","effwt*puwt")
plot14.SetFilePath(filedirectory)
plot14.SetLumiTree(LUMI,Treename)
plot14.SetPlotDir(plotdirectort)
plot14.SetLogy(True)
plot14.DrawTHStack("GroomedJet_CA8_prsubjet1ptoverjetpt",0,"CA8 Pruned SubJet1 Pt/ Jet Pt","",Scalefilename,2,0.01,cutforfile)

plot15 = ProducePlot()
plot15.SetBinMinMax(20,0,0.5)
plot15.SetCutWeightName(cut + "(GroomedJet_CA8_prsubjet1ptoverjetpt > GroomedJet_CA8_prsubjet2ptoverjetpt)","effwt*puwt")
plot15.SetFilePath(filedirectory)
plot15.SetLumiTree(LUMI,Treename)
plot15.SetPlotDir(plotdirectort)
plot15.SetLogy(True)
plot15.DrawTHStack("GroomedJet_CA8_prsubjet2ptoverjetpt",0,"CA8 Pruned SubJet2 Pt/ Jet Pt","",Scalefilename,2,0.01,cutforfile)

plot16 = ProducePlot()
plot16.SetBinMinMax(25,0,1.)
plot16.SetCutWeightName(cut,"effwt*puwt")
plot16.SetFilePath(filedirectory)
plot16.SetLumiTree(LUMI,Treename)
plot16.SetPlotDir(plotdirectort)
plot16.SetLogy(True)
plot16.DrawTHStack("GroomedJet_CA8_prsubjet1subjet2_deltaR",0,"CA8 #DeltaR(Subjet1, Subjet2)","",Scalefilename,2,0.01,cutforfile)

plot17 = ProducePlot()
plot17.SetBinMinMax(95,5,100)
plot17.SetCutWeightName(cut,"effwt*puwt")
plot17.SetFilePath(filedirectory)
plot17.SetLumiTree(LUMI,Treename)
plot17.SetPlotDir(plotdirectort)
plot17.SetLogy(True)
plot17.DrawTHStack("GroomedJet_CA8_jetconstituents",0,"CA8 Jet Constituents","",Scalefilename,2,0.01,cutforfile)

plot18 = ProducePlot()
plot18.SetBinMinMax(4,-0.5,3.5)
plot18.SetCutWeightName(cut,"effwt*puwt")
plot18.SetFilePath(filedirectory)
plot18.SetLumiTree(LUMI,Treename)
plot18.SetPlotDir(plotdirectort)
plot18.SetLogy(True)
plot18.DrawTHStack("GroomedJet_numberbjets",0,"Number of Btagged Jets","",Scalefilename,2,0.01,cutforfile)

plot19 = ProducePlot()
plot19.SetBinMinMax(20,0,1)
plot19.SetCutWeightName(cut,"effwt*puwt")
plot19.SetFilePath(filedirectory)
plot19.SetLumiTree(LUMI,Treename)
plot19.SetPlotDir(plotdirectort)
plot19.SetLogy(True)
plot19.DrawTHStack("GroomedJet_CA8_rcores01",0,"CA8 Jet R-Cores 0.1","",Scalefilename,2,0.01,cutforfile)

plot20 = ProducePlot()
plot20.SetBinMinMax(20,0,1)
plot20.SetCutWeightName(cut,"effwt*puwt")
plot20.SetFilePath(filedirectory)
plot20.SetLumiTree(LUMI,Treename)
plot20.SetPlotDir(plotdirectort)
plot20.SetLogy(True)
plot20.DrawTHStack("GroomedJet_CA8_rcores02",0,"CA8 Jet R-Cores 0.2","",Scalefilename,2,0.01,cutforfile)

plot21 = ProducePlot()
plot21.SetBinMinMax(20,0,1)
plot21.SetCutWeightName(cut,"effwt*puwt")
plot21.SetFilePath(filedirectory)
plot21.SetLumiTree(LUMI,Treename)
plot21.SetPlotDir(plotdirectort)
plot21.SetLogy(True)
plot21.DrawTHStack("GroomedJet_CA8_rcores03",0,"CA8 Jet R-Cores 0.3","",Scalefilename,2,0.01,cutforfile)

plot22 = ProducePlot()
plot22.SetBinMinMax(20,0,1)
plot22.SetCutWeightName(cut,"effwt*puwt")
plot22.SetFilePath(filedirectory)
plot22.SetLumiTree(LUMI,Treename)
plot22.SetPlotDir(plotdirectort)
plot22.SetLogy(True)
plot22.DrawTHStack("GroomedJet_CA8_rcores04",0,"CA8 Jet R-Cores 0.4","",Scalefilename,2,0.01,cutforfile)

plot23 = ProducePlot()
plot23.SetBinMinMax(20,0,1)
plot23.SetCutWeightName(cut,"effwt*puwt")
plot23.SetFilePath(filedirectory)
plot23.SetLumiTree(LUMI,Treename)
plot23.SetPlotDir(plotdirectort)
plot23.SetLogy(True)
plot23.DrawTHStack("GroomedJet_CA8_rcores05",0,"CA8 Jet R-Cores 0.5","",Scalefilename,2,0.01,cutforfile)

plot24 = ProducePlot()
plot24.SetBinMinMax(20,0,1)
plot24.SetCutWeightName(cut,"effwt*puwt")
plot24.SetFilePath(filedirectory)
plot24.SetLumiTree(LUMI,Treename)
plot24.SetPlotDir(plotdirectort)
plot24.SetLogy(True)
plot24.DrawTHStack("GroomedJet_CA8_rcores06",0,"CA8 Jet R-Cores 0.6","",Scalefilename,2,0.01,cutforfile)

plot25 = ProducePlot()
plot25.SetBinMinMax(20,0,1)
plot25.SetCutWeightName(cut,"effwt*puwt")
plot25.SetFilePath(filedirectory)
plot25.SetLumiTree(LUMI,Treename)
plot25.SetPlotDir(plotdirectort)
plot25.SetLogy(True)
plot25.DrawTHStack("GroomedJet_CA8_rcores07",0,"CA8 Jet R-Cores 0.7","",Scalefilename,2,0.01,cutforfile)

plot26 = ProducePlot()
plot26.SetBinMinMax(20,0,1)
plot26.SetCutWeightName(cut,"effwt*puwt")
plot26.SetFilePath(filedirectory)
plot26.SetLumiTree(LUMI,Treename)
plot26.SetPlotDir(plotdirectort)
plot26.SetLogy(True)
plot26.DrawTHStack("GroomedJet_CA8_ptcores01",0,"CA8 Jet Pt-Cores 0.1","",Scalefilename,2,0.01,cutforfile)

plot27 = ProducePlot()
plot27.SetBinMinMax(20,0,1)
plot27.SetCutWeightName(cut,"effwt*puwt")
plot27.SetFilePath(filedirectory)
plot27.SetLumiTree(LUMI,Treename)
plot27.SetPlotDir(plotdirectort)
plot27.SetLogy(True)
plot27.DrawTHStack("GroomedJet_CA8_ptcores02",0,"CA8 Jet Pt-Cores 0.2","",Scalefilename,2,0.01,cutforfile)

plot28 = ProducePlot()
plot28.SetBinMinMax(20,0.2,1)
plot28.SetCutWeightName(cut,"effwt*puwt")
plot28.SetFilePath(filedirectory)
plot28.SetLumiTree(LUMI,Treename)
plot28.SetPlotDir(plotdirectort)
plot28.SetLogy(True)
plot28.DrawTHStack("GroomedJet_CA8_ptcores03",0,"CA8 Jet Pt-Cores 0.3","",Scalefilename,2,0.01,cutforfile)

plot29 = ProducePlot()
plot29.SetBinMinMax(20,0.2,1)
plot29.SetCutWeightName(cut,"effwt*puwt")
plot29.SetFilePath(filedirectory)
plot29.SetLumiTree(LUMI,Treename)
plot29.SetPlotDir(plotdirectort)
plot29.SetLogy(True)
plot29.DrawTHStack("GroomedJet_CA8_ptcores04",0,"CA8 Jet Pt-Cores 0.4","",Scalefilename,2,0.01,cutforfile)

plot30 = ProducePlot()
plot30.SetBinMinMax(20,0.2,1)
plot30.SetCutWeightName(cut,"effwt*puwt")
plot30.SetFilePath(filedirectory)
plot30.SetLumiTree(LUMI,Treename)
plot30.SetPlotDir(plotdirectort)
plot30.SetLogy(True)
plot30.DrawTHStack("GroomedJet_CA8_ptcores05",0,"CA8 Jet Pt-Cores 0.5","",Scalefilename,2,0.01,cutforfile)

plot31 = ProducePlot()
plot31.SetBinMinMax(20,0.2,1)
plot31.SetCutWeightName(cut,"effwt*puwt")
plot31.SetFilePath(filedirectory)
plot31.SetLumiTree(LUMI,Treename)
plot31.SetPlotDir(plotdirectort)
plot31.SetLogy(True)
plot31.DrawTHStack("GroomedJet_CA8_ptcores06",0,"CA8 Jet Pt-Cores 0.6","",Scalefilename,2,0.01,cutforfile)

plot32 = ProducePlot()
plot32.SetBinMinMax(20,0.3,1)
plot32.SetCutWeightName(cut,"effwt*puwt")
plot32.SetFilePath(filedirectory)
plot32.SetLumiTree(LUMI,Treename)
plot32.SetPlotDir(plotdirectort)
plot32.SetLogy(True)
plot32.DrawTHStack("GroomedJet_CA8_ptcores07",0,"CA8 Jet Pt-Cores 0.7","",Scalefilename,2,0.01,cutforfile)

plot33 = ProducePlot()
plot33.SetBinMinMax(20,0,1)
plot33.SetCutWeightName(cut,"effwt*puwt")
plot33.SetFilePath(filedirectory)
plot33.SetLumiTree(LUMI,Treename)
plot33.SetPlotDir(plotdirectort)
plot33.SetLogy(True)
plot33.DrawTHStack("GroomedJet_CA8_planarflow01",0,"CA8 Jet Plannar-Flow 0.1","",Scalefilename,2,0.01,cutforfile)

plot34 = ProducePlot()
plot34.SetBinMinMax(20,0,1)
plot34.SetCutWeightName(cut,"effwt*puwt")
plot34.SetFilePath(filedirectory)
plot34.SetLumiTree(LUMI,Treename)
plot34.SetPlotDir(plotdirectort)
plot34.SetLogy(True)
plot34.DrawTHStack("GroomedJet_CA8_planarflow02",0,"CA8 Jet Plannar-Flow 0.2","",Scalefilename,2,0.01,cutforfile)

plot35 = ProducePlot()
plot35.SetBinMinMax(20,0,1)
plot35.SetCutWeightName(cut,"effwt*puwt")
plot35.SetFilePath(filedirectory)
plot35.SetLumiTree(LUMI,Treename)
plot35.SetPlotDir(plotdirectort)
plot35.SetLogy(True)
plot35.DrawTHStack("GroomedJet_CA8_planarflow03",0,"CA8 Jet Plannar-Flow 0.3","",Scalefilename,2,0.01,cutforfile)

plot36 = ProducePlot()
plot36.SetBinMinMax(20,0,1)
plot36.SetCutWeightName(cut,"effwt*puwt")
plot36.SetFilePath(filedirectory)
plot36.SetLumiTree(LUMI,Treename)
plot36.SetPlotDir(plotdirectort)
plot36.SetLogy(True)
plot36.DrawTHStack("GroomedJet_CA8_planarflow04",0,"CA8 Jet Plannar-Flow 0.4","",Scalefilename,2,0.01,cutforfile)

plot37 = ProducePlot()
plot37.SetBinMinMax(20,0,1)
plot37.SetCutWeightName(cut,"effwt*puwt")
plot37.SetFilePath(filedirectory)
plot37.SetLumiTree(LUMI,Treename)
plot37.SetPlotDir(plotdirectort)
plot37.SetLogy(True)
plot37.DrawTHStack("GroomedJet_CA8_planarflow05",0,"CA8 Jet Plannar-Flow 0.5","",Scalefilename,2,0.01,cutforfile)

plot38 = ProducePlot()
plot38.SetBinMinMax(20,0,1)
plot38.SetCutWeightName(cut,"effwt*puwt")
plot38.SetFilePath(filedirectory)
plot38.SetLumiTree(LUMI,Treename)
plot38.SetPlotDir(plotdirectort)
plot38.SetLogy(True)
plot38.DrawTHStack("GroomedJet_CA8_planarflow06",0,"CA8 Jet Plannar-Flow 0.6","",Scalefilename,2,0.01,cutforfile)

plot39 = ProducePlot()
plot39.SetBinMinMax(20,0,1)
plot39.SetCutWeightName(cut,"effwt*puwt")
plot39.SetFilePath(filedirectory)
plot39.SetLumiTree(LUMI,Treename)
plot39.SetPlotDir(plotdirectort)
plot39.SetLogy(True)
plot39.DrawTHStack("GroomedJet_CA8_planarflow07",0,"CA8 Jet Plannar-Flow 0.7","",Scalefilename,2,0.01,cutforfile)

#raw_input( 'Press ENTER to continue\n ' )
