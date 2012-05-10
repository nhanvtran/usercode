from ROOT import gROOT, gStyle, gSystem, TLatex
import subprocess

jtypes_m = ["ak5","ak5tr","ak5ft","ak5pr","ak5g","ak7","ak7tr","ak7ft","ak7pr","ak7g","ak8","ak8tr","ak8ft","ak8pr","ak8g","ca8","ca8pr","ca8g","ca12ft","ca12mdft"]
jtypetrans_m = {"ak5":"AK5PF","ak5tr":"AK5TRIMMEDPF","ak5ft":"AK5FILTEREDPF","ak5pr":"AK5PRUNEDPF",
        "ak7":"AK7PF","ak7tr":"AK7TRIMMEDPF","ak7ft":"AK7FILTEREDPF","ak7pr":"AK7PRUNEDPF",
        "ak8":"AK8PF","ak8tr":"AK8TRIMMEDPF","ak8ft":"AK8FILTEREDPF","ak8pr":"AK8PRUNEDPF",
        "ca8":"CA8PF","ca8pr":"CA8PRUNEDPF","ca12ft":"CA12FILTEREDPF","ca12mdft":"CA12MASSDROPFILTEREDPF",
        "ak5g":"AK5GENJETSNONU","ak7g":"AK7GENJETSNONU","ak8g":"AK8GENJETSNONU","ca8g":"CA8GENJETSNONU"} 
jtypesToI_m = {"ak5":0,"ak5tr":1,"ak5ft":2,"ak5pr":3,"ak5g":4,
        "ak7":5,"ak7tr":6,"ak7ft":7,"ak7pr":8,"ak7g":9,
        "ak8":10,"ak8tr":11,"ak8ft":12,"ak8pr":13,"ak8g":14,
        "ca8":15,"ca8pr":16,"ca8g":17,"ca12ft":18,"ca12mdft":19}
    
jtypes_d = ["ak5","ak5tr","ak5ft","ak5pr","ak7","ak7tr","ak7ft","ak7pr","ak8","ak8tr","ak8ft","ak8pr","ca8","ca8pr"]
jtypetrans_d = {"ak5":"AK5PF","ak5tr":"AK5TRIMMEDPF","ak5ft":"AK5FILTEREDPF","ak5pr":"AK5PRUNEDPF",
        "ak7":"AK7PF","ak7tr":"AK7TRIMMEDPF","ak7ft":"AK7FILTEREDPF","ak7pr":"AK7PRUNEDPF",
        "ak8":"AK8PF","ak8tr":"AK8TRIMMEDPF","ak8ft":"AK8FILTEREDPF","ak8pr":"AK8PRUNEDPF",
        "ca8":"CA8PF","ca8pr":"CA8PRUNEDPF"} 
jtypesToI_d = {"ak5":0,"ak5tr":1,"ak5ft":2,"ak5pr":3,
        "ak7":4,"ak7tr":5,"ak7ft":6,"ak7pr":7,
        "ak8":8,"ak8tr":9,"ak8ft":10,"ak8pr":11,
        "ca8":12,"ca8pr":13}
    
jtypes = []
jtypetrans = []
jtypesToI = []
jtypesToI = jtypesToI_m

gROOT.ProcessLine('.L myutils.C++')
from ROOT import myutils, TH1F
theutils = myutils()

suffix=".png"

cmap_m = {1:1,2:2,3:3,4:4,5:5,6:1,7:2,8:3,9:4,10:5,11:1,12:2,13:3,14:4,15:5,16:6,17:7,18:8,19:9,20:10}
cmap_d = {1:1,2:2,3:3,4:4,5:1,6:2,7:3,8:4,9:1,10:2,11:3,12:4,13:5,14:6}


# Import everything from ROOT
import ROOT
from glob import glob
from array import array
    
ROOT.gStyle.SetPadLeftMargin(0.16);

############################################################
def SetHistProperties(h, linecolor, markercolor, fillcolor, linestyle, markerstyle, fillstyle):

    h.SetLineColor( linecolor )
    h.SetMarkerColor( markercolor )
    h.SetFillColor( fillcolor )
    h.SetLineStyle( linestyle )
    h.SetMarkerStyle( markerstyle )
    h.SetFillStyle( fillstyle )
    h.GetYaxis().SetTitleOffset( 1.5 )
    
def SetHistProperties_wName(h, linecolor, markercolor, fillcolor, linestyle, markerstyle, fillstyle, name):
    
    h.SetLineColor( linecolor )
    h.SetMarkerColor( markercolor )
    h.SetFillColor( fillcolor )
    h.SetLineStyle( linestyle )
    h.SetMarkerStyle( markerstyle )
    h.SetFillStyle( fillstyle )
    h.GetYaxis().SetTitleOffset( 1.5 )
    h.SetName(name)

def GetHistogramEntriesWeighted( h ):
    tot = 0;
    for i in range(h.GetNbinsX()):
        tot+=h.GetBinContent( i+1 );
    return tot


def GetDataMCSclFactor( dat,MC ):
    
    mctotweight = GetHistogramEntriesWeighted( MC );
    datatotweight = GetHistogramEntriesWeighted( dat );
    scl = datatotweight/mctotweight;
    MC.Scale( scl )
    print scl
    return scl

############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
def plotterBasic(mcname,dataname,figdir):

    fm = ROOT.TFile(mcname)
    fd = ROOT.TFile(dataname)
    
    print "files: ", mcname,", ", dataname

    hm_v_mt = fm.Get("h_v_mt") 
    hm_v_pt = fm.Get("h_v_pt") 
    hm_e_met = fm.Get("h_e_met") 
    hm_l_pt = fm.Get("h_l_pt") 
    hm_l_eta = fm.Get("h_l_eta") 
    hm_e_nvert = fm.Get("h_e_nvert")
    hm_e_nvert_weighted = fm.Get("h_e_nvert_weighted")

    hd_v_mt = fd.Get("h_v_mt") 
    hd_v_pt = fd.Get("h_v_pt") 
    hd_e_met = fd.Get("h_e_met") 
    hd_l_pt = fd.Get("h_l_pt") 
    hd_l_eta = fd.Get("h_l_eta") 
    hd_e_nvert = fd.Get("h_e_nvert")
    hd_e_nvert_weighted = fd.Get("h_e_nvert_weighted")

    cn = ROOT.TCanvas("cn","cn",800,800)
    scl = GetDataMCSclFactor( hd_e_nvert, hm_e_nvert )
    scl = GetDataMCSclFactor( hd_e_nvert, hm_e_nvert_weighted )
    SetHistProperties( hd_e_nvert,1,1,1,1,1,1 )
    SetHistProperties( hm_e_nvert,2,2,2,1,1,1 )
    SetHistProperties( hm_e_nvert_weighted,4,4,4,1,1,1 )
    hd_e_nvert.Draw()
    hm_e_nvert.Draw("sames")
    hm_e_nvert_weighted.Draw("sames")
    cn.SaveAs(figdir+"/nvert"+suffix)

    ckin = ROOT.TCanvas("ckin","ckin",1200,800)
    ckin.Divide(3,2)
    ckin.cd(1)
    SetHistProperties( hm_v_mt,2,2,2,1,1,1 )
    SetHistProperties( hd_v_mt,1,1,1,1,20,1 )
    scl = GetDataMCSclFactor( hd_v_mt, hm_v_mt )
    hm_v_mt.Draw("hist")
    hd_v_mt.Draw("pe0sames")
    ckin.cd(2)
    SetHistProperties( hm_v_pt,2,2,2,1,1,1 )
    SetHistProperties( hd_v_pt,1,1,1,1,20,1 )
    scl = GetDataMCSclFactor( hd_v_pt, hm_v_pt )
    hm_v_pt.Draw("hist")
    hd_v_pt.Draw("pe0sames")
    ckin.cd(3)
    SetHistProperties( hm_e_met,2,2,2,1,1,1 )
    SetHistProperties( hd_e_met,1,1,1,1,20,1 )
    scl = GetDataMCSclFactor( hd_e_met, hm_e_met )
    hm_e_met.Draw("hist")
    hd_e_met.Draw("pe0sames")
    ckin.cd(4)
    SetHistProperties( hm_l_pt,2,2,2,1,1,1 )
    SetHistProperties( hd_l_pt,1,1,1,1,20,1 )
    scl = GetDataMCSclFactor( hd_l_pt, hm_l_pt )
    hm_l_pt.Draw("hist")
    hd_l_pt.Draw("pe0sames")
    ckin.cd(5)
    SetHistProperties( hm_l_eta,2,2,2,1,1,1 )
    SetHistProperties( hd_l_eta,1,1,1,1,20,1 )
    scl = GetDataMCSclFactor( hd_l_eta, hm_l_eta )
    hm_l_eta.Draw("hist")
    hd_l_eta.Draw("pe0sames")
    ckin.SaveAs(figdir+"/kinematics"+suffix)

############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
def plotterStack(mcnamesStack, mcname,dataname,figdir, chan):
    
    fm = ROOT.TFile(mcname)
    fd = ROOT.TFile(dataname)
    
    print "stack files: ", mcname,", ", dataname
    
    hm_v_mt = fm.Get("h_v_mt") 
    hm_v_mass = fm.Get("h_v_mass") 
    hm_v_pt = fm.Get("h_v_pt") 
    hm_e_met = fm.Get("h_e_met") 
    hm_l_pt = fm.Get("h_l_pt") 
    hm_l_eta = fm.Get("h_l_eta") 
    hm_e_nvert = fm.Get("h_e_nvert")
    hm_e_nvert_weighted = fm.Get("h_e_nvert_weighted")
    
    hd_v_mt = fd.Get("h_v_mt") 
    hd_v_mass = fd.Get("h_v_mass")     
    hd_v_pt = fd.Get("h_v_pt") 
    hd_e_met = fd.Get("h_e_met") 
    hd_l_pt = fd.Get("h_l_pt") 
    hd_l_eta = fd.Get("h_l_eta") 
    hd_e_nvert = fd.Get("h_e_nvert")
    hd_e_nvert_weighted = fd.Get("h_e_nvert_weighted")

    SetHistProperties( hm_v_mt,2,2,2,1,1,1 )
    SetHistProperties( hd_v_mt,1,1,1,1,20,1 )
    SetHistProperties( hm_v_mass,2,2,2,1,1,1 )
    SetHistProperties( hd_v_mass,1,1,1,1,20,1 )
    SetHistProperties( hm_v_pt,2,2,2,1,1,1 )
    SetHistProperties( hd_v_pt,1,1,1,1,20,1 )
    SetHistProperties( hm_e_met,2,2,2,1,1,1 )
    SetHistProperties( hd_e_met,1,1,1,1,20,1 )
    SetHistProperties( hm_l_pt,2,2,2,1,1,1 )
    SetHistProperties( hd_l_pt,1,1,1,1,20,1 )
    SetHistProperties( hm_l_eta,2,2,2,1,1,1 )
    SetHistProperties( hd_l_eta,1,1,1,1,20,1 )
    SetHistProperties( hd_e_nvert,1,1,1,1,20,1 )
    SetHistProperties( hm_e_nvert,2,2,2,1,1,1 )
    SetHistProperties( hm_e_nvert_weighted,4,4,4,1,1,1 )

    
    scl_v_mt = GetDataMCSclFactor( hd_v_mt, hm_v_mt )
    scl_v_mass = GetDataMCSclFactor( hd_v_mass, hm_v_mass )    
    scl_v_pt = GetDataMCSclFactor( hd_v_pt, hm_v_pt )
    scl_e_met = GetDataMCSclFactor( hd_e_met, hm_e_met )
    scl_l_pt = GetDataMCSclFactor( hd_l_pt, hm_l_pt )
    scl_l_eta = GetDataMCSclFactor( hd_l_eta, hm_l_eta )
    scl_e_dummy = GetDataMCSclFactor( hd_e_nvert, hm_e_nvert )
    scl_e_nvert = GetDataMCSclFactor( hd_e_nvert, hm_e_nvert_weighted )

    hms_v_mt = ROOT.THStack("hms_v_mt","hms_v_mt")
    hms_v_mass = ROOT.THStack("hms_v_mass","hms_v_mass")    
    hms_v_pt = ROOT.THStack("hms_v_pt","hms_v_pt")
    hms_e_met = ROOT.THStack("hms_e_met","hms_e_met")
    hms_l_pt = ROOT.THStack("hms_l_pt","hms_l_pt")
    hms_l_eta = ROOT.THStack("hms_l_eta","hms_l_eta")
    hms_e_nvert_weighted = ROOT.THStack("hms_e_nvert_weighted","hms_e_nvert_weighted")    
    
    print mcnamesStack
    for x in range(len(mcnamesStack)):
        ft = ROOT.TFile(mcnamesStack[x]) 
        hs_v_mt =  ft.Get("h_v_mt") 
        hs_v_mass =  ft.Get("h_v_mass") 
        hs_v_pt = ft.Get("h_v_pt")
        hs_e_met = ft.Get("h_e_met")
        hs_l_pt = ft.Get("h_l_pt")
        hs_l_eta = ft.Get("h_l_eta")
        hs_e_nvert_weighted = ft.Get("h_e_nvert_weighted")
        gROOT.cd()
        hs_v_mt_new = hs_v_mt.Clone()
        hs_v_mass_new = hs_v_mass.Clone()        
        hs_v_pt_new = hs_v_pt.Clone()
        hs_e_met_new = hs_e_met.Clone()
        hs_l_pt_new = hs_l_pt.Clone()
        hs_l_eta_new = hs_l_eta.Clone()
        hs_e_nvert_weighted_new = hs_e_nvert_weighted.Clone()
        
        hs_v_mt_new.Scale( scl_v_mt )
        hs_v_mass_new.Scale( scl_v_mass )        
        hs_v_pt_new.Scale( scl_v_pt )
        hs_e_met_new.Scale( scl_e_met )
        hs_l_pt_new.Scale( scl_l_pt )
        hs_l_eta_new.Scale( scl_l_eta )
        hs_e_nvert_weighted_new.Scale( scl_e_nvert )
        
        y=x+2
        SetHistProperties(hs_v_mt_new,y,y,y,1,1,1001)
        SetHistProperties(hs_v_mass_new,y,y,y,1,1,1001)        
        SetHistProperties(hs_v_pt_new,y,y,y,1,1,1001)
        SetHistProperties(hs_e_met_new,y,y,y,1,1,1001)
        SetHistProperties(hs_l_pt_new,y,y,y,1,1,1001)
        SetHistProperties(hs_l_eta_new,y,y,y,1,1,1001)
        SetHistProperties(hs_e_nvert_weighted_new,y,y,y,1,1,1001)
        
        hms_v_mt.Add(hs_v_mt_new)
        hms_v_mass.Add(hs_v_mass_new)        
        hms_v_pt.Add(hs_v_pt_new)
        hms_e_met.Add(hs_e_met_new)
        hms_l_pt.Add(hs_l_pt_new)
        hms_l_eta.Add(hs_l_eta_new)
        hms_e_nvert_weighted.Add(hs_e_nvert_weighted_new)
    
    cn = ROOT.TCanvas("cn","cn",800,800)
    hd_e_nvert.Draw()
    hm_e_nvert.Draw("sames")
    hm_e_nvert_weighted.Draw("sames")
    cn.SaveAs(figdir+"/nvert"+suffix)
    
    ckin = ROOT.TCanvas("ckin","ckin",1200,800)
    ckin.Divide(3,2)
    ckin.cd(1)
    if chan == 1 or chan == 2:
        hm_v_mt.Draw("hist")
        hd_v_mt.Draw("pe0sames")
    if chan == 3 or chan == 4:
        hm_v_mass.Draw("hist")
        hd_v_mass.Draw("pe0sames")
    ckin.cd(2)
    hm_v_pt.Draw("hist")
    hd_v_pt.Draw("pe0sames")
    ckin.cd(3)
    hm_e_met.Draw("hist")
    hd_e_met.Draw("pe0sames")
    ckin.cd(4)
    hm_l_pt.Draw("hist")
    hd_l_pt.Draw("pe0sames")
    ckin.cd(5)
    hm_l_eta.Draw("hist")
    hd_l_eta.Draw("pe0sames")
    ckin.SaveAs(figdir+"/kinematics"+suffix)

    ckins = ROOT.TCanvas("ckins","ckins",1200,800)
    ckins.Divide(3,2)
    ckins.cd(1)
    if chan == 1 or chan == 2:
        hms_v_mt.Draw("hist")
        hd_v_mt.Draw("pe0sames")
    if chan == 3 or chan == 4:
        hms_v_mass.Draw("hist")
        hd_v_mass.Draw("pe0sames")
    ckins.cd(2)
    hms_v_pt.Draw("hist")
    hd_v_pt.Draw("pe0sames")
    ckins.cd(3)
    hms_e_met.Draw("hist")
    hd_e_met.Draw("pe0sames")
    ckins.cd(4)
    hms_l_pt.Draw("hist")
    hd_l_pt.Draw("pe0sames")
    ckins.cd(5)
    hms_l_eta.Draw("hist")
    hd_l_eta.Draw("pe0sames")
    ckins.cd(6)
    hms_e_nvert_weighted.Draw("hist")
    hd_e_nvert.Draw("pe0sames")
    ckins.SaveAs(figdir+"/st_kinematics"+suffix)



############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################

def plotter1D(mcname,dataname,figdir):
    
    fm = ROOT.TFile(mcname)
    fd = ROOT.TFile(dataname)

    print "1D files: ", mcname,", ", dataname

    ############################################################
    # S P E C I F I C   P L O T S
    ##### 
    hm_mass = []
    hm_mass_0bin = []
    hm_mass_1bin = []
    hm_mass_2bin = []
    hm_mass_3bin = []
    hm_mass_4bin = []    
    hd_mass = []
    hd_mass_0bin = []
    hd_mass_1bin = []
    hd_mass_2bin = []
    hd_mass_3bin = []
    hd_mass_4bin = []    
    
    for x in range(len(jtypes_m)):
        print jtypes_m[x]
        hm_mass.append( fm.Get("h_"+jtypes_m[x]+"_mass") )
        hm_mass_0bin.append( fm.Get("h_"+jtypes_m[x]+"_mass_0bin") )
        hm_mass_1bin.append( fm.Get("h_"+jtypes_m[x]+"_mass_1bin") )                       
        hm_mass_2bin.append( fm.Get("h_"+jtypes_m[x]+"_mass_2bin") )                       
        hm_mass_3bin.append( fm.Get("h_"+jtypes_m[x]+"_mass_3bin") )                       
        hm_mass_4bin.append( fm.Get("h_"+jtypes_m[x]+"_mass_4bin") )   
        y = x+1
        SetHistProperties(hm_mass[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 1, 1)
        SetHistProperties(hm_mass_0bin[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 1, 1)
        SetHistProperties(hm_mass_1bin[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 1, 1)
        SetHistProperties(hm_mass_2bin[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 1, 1)
        SetHistProperties(hm_mass_3bin[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 1, 1)
        SetHistProperties(hm_mass_4bin[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 1, 1)    

    for x in range(len(jtypes_d)):
        hd_mass.append( fd.Get("h_"+jtypes_d[x]+"_mass") )
        hd_mass_0bin.append( fd.Get("h_"+jtypes_d[x]+"_mass_0bin") )
        hd_mass_1bin.append( fd.Get("h_"+jtypes_d[x]+"_mass_1bin") )                       
        hd_mass_2bin.append( fd.Get("h_"+jtypes_d[x]+"_mass_2bin") )                       
        hd_mass_3bin.append( fd.Get("h_"+jtypes_d[x]+"_mass_3bin") )                       
        hd_mass_4bin.append( fd.Get("h_"+jtypes_d[x]+"_mass_4bin") )
        y = x+1
        SetHistProperties(hd_mass[x], cmap_d[y],cmap_d[y],cmap_d[y], 1, 1, 1)
        SetHistProperties(hd_mass_0bin[x], cmap_d[y],cmap_d[y],cmap_d[y], 1, 1, 1)
        SetHistProperties(hd_mass_1bin[x], cmap_d[y],cmap_d[y],cmap_d[y], 1, 1, 1)
        SetHistProperties(hd_mass_2bin[x], cmap_d[y],cmap_d[y],cmap_d[y], 1, 1, 1)
        SetHistProperties(hd_mass_3bin[x], cmap_d[y],cmap_d[y],cmap_d[y], 1, 1, 1)
        SetHistProperties(hd_mass_4bin[x], cmap_d[y],cmap_d[y],cmap_d[y], 1, 1, 1)

    c1 = ROOT.TCanvas("c1","c1",600,600)
    c1.cd()
    SetHistProperties( hm_mass[jtypesToI_m["ak5"]],2,2,2,1,1,3003 )
    SetHistProperties( hm_mass[jtypesToI_m["ak5g"]],4,4,4,1,1,1 )    
    SetHistProperties( hd_mass[jtypesToI_d["ak5"]],1,1,1,1,20,1 )
    scl = GetDataMCSclFactor( hd_mass[jtypesToI_d["ak5"]], hm_mass[jtypesToI_m["ak5"]] )
    hm_mass[jtypesToI_m["ak5g"]].Scale( scl )

    tmph = hm_mass[jtypesToI_m["ak5"]].Clone()
    SetHistProperties( tmph, 2,0,0,1,0,0 )
    print "sclfctr: ",str(scl)
    hm_mass[jtypesToI_m["ak5"]].SetMinimum(0)
    hm_mass[jtypesToI_m["ak5"]].Draw("e2")
    tmph.Draw("sames")    
    hm_mass[jtypesToI_m["ak5g"]].Draw("sames")
    hd_mass[jtypesToI_d["ak5"]].Draw("pe1x0sames")        
    c1.SaveAs( figdir+"/test"+suffix )

    c17 = ROOT.TCanvas("c17","c17",600,600)
    c17.cd()
    SetHistProperties( hm_mass[jtypesToI_m["ak7"]],2,2,2,1,1,3003 )
    SetHistProperties( hm_mass[jtypesToI_m["ak7g"]],4,4,4,1,1,1 )    
    SetHistProperties( hd_mass[jtypesToI_d["ak7"]],1,1,1,1,20,1 )
    scl = GetDataMCSclFactor( hd_mass[jtypesToI_d["ak7"]], hm_mass[jtypesToI_m["ak7"]] )
    hm_mass[jtypesToI_m["ak7g"]].Scale( scl )

    tmph = hm_mass[jtypesToI_m["ak7"]].Clone()
    SetHistProperties( tmph, 2,0,0,1,0,0 )
    print "sclfctr: ",str(scl)
    hm_mass[jtypesToI_m["ak7"]].SetMinimum(0)
    hm_mass[jtypesToI_m["ak7"]].Draw("e2")
    tmph.Draw("sames")    
    hm_mass[jtypesToI_m["ak7g"]].Draw("sames")
    hd_mass[jtypesToI_d["ak7"]].Draw("pe1x0sames")        
    c17.SaveAs( figdir+"/test_ak7"+suffix )

    c18 = ROOT.TCanvas("c18","c18",600,600)
    c18.cd()
    SetHistProperties( hm_mass[jtypesToI_m["ak8"]],2,2,2,1,1,3003 )
    SetHistProperties( hm_mass[jtypesToI_m["ak8g"]],4,4,4,1,1,1 )    
    SetHistProperties( hd_mass[jtypesToI_d["ak8"]],1,1,1,1,20,1 )
    scl = GetDataMCSclFactor( hd_mass[jtypesToI_d["ak8"]], hm_mass[jtypesToI_m["ak8"]] )
    hm_mass[jtypesToI_m["ak8g"]].Scale( scl )

    tmph = hm_mass[jtypesToI_m["ak8"]].Clone()
    SetHistProperties( tmph, 2,0,0,1,0,0 )
    print "sclfctr: ",str(scl)
    hm_mass[jtypesToI_m["ak8"]].SetMinimum(0)
    hm_mass[jtypesToI_m["ak8"]].Draw("e2")
    tmph.Draw("sames")    
    hm_mass[jtypesToI_m["ak8g"]].Draw("sames")
    hd_mass[jtypesToI_d["ak8"]].Draw("pe1x0sames")        
    c18.SaveAs( figdir+"/test_ak8"+suffix )

    # simple comparisons
    for x in range(len(jtypes_d)):
        ctmp = ROOT.TCanvas("ctmp","ctmp",600,600)
        ctmp.cd()
        SetHistProperties( hm_mass[jtypesToI_m[jtypes_d[x]]],2,2,2,1,1,3003 )
        SetHistProperties( hd_mass[jtypesToI_d[jtypes_d[x]]],1,1,1,1,20,1 )
        scl = GetDataMCSclFactor( hd_mass[jtypesToI_d[jtypes_d[x]]], hm_mass[jtypesToI_m[jtypes_d[x]]] )

        tmph = hm_mass[jtypesToI_m[jtypes_d[x]]].Clone()
        SetHistProperties( tmph, 2,0,0,1,0,0 )
        hm_mass[jtypesToI_m[jtypes_d[x]]].SetMinimum(0)
        
        hm_mass[jtypesToI_m[jtypes_d[x]]].Draw("e2")
        tmph.Draw("sames")    
        hd_mass[jtypesToI_d[jtypes_d[x]]].Draw("pe1x0sames")        
        
        ctmp.SaveAs( figdir+"/test_m_"+jtypes_d[x]+suffix )
        del ctmp
        del tmph
    
    #################    #################    #################

    c2 = ROOT.TCanvas("c2","c2",1600,800)
    c2.Divide(3,2)
    c2.cd(1)
    hd_mass[jtypesToI_d['ak5pr']].Draw()
    hd_mass[jtypesToI_d['ak5tr']].Draw("sames")
    hd_mass[jtypesToI_d['ak5ft']].Draw("sames")
    hd_mass[jtypesToI_d['ak5']].Draw("sames")

    c2.cd(2)
    hd_mass_0bin[jtypesToI_d['ak5ft']].Draw()
    hd_mass_0bin[jtypesToI_d['ak5tr']].Draw("sames")
    hd_mass_0bin[jtypesToI_d['ak5pr']].Draw("sames")
    hd_mass_0bin[jtypesToI_d['ak5']].Draw("sames")

    c2.cd(3)
    hd_mass_1bin[jtypesToI_d['ak5ft']].Draw()
    hd_mass_1bin[jtypesToI_d['ak5tr']].Draw("sames")
    hd_mass_1bin[jtypesToI_d['ak5pr']].Draw("sames")
    hd_mass_1bin[jtypesToI_d['ak5']].Draw("sames")

    c2.cd(4)
    hd_mass_2bin[jtypesToI_d['ak5ft']].Draw()
    hd_mass_2bin[jtypesToI_d['ak5tr']].Draw("sames")
    hd_mass_2bin[jtypesToI_d['ak5pr']].Draw("sames")
    hd_mass_2bin[jtypesToI_d['ak5']].Draw("sames")

    c2.cd(5)
    hd_mass_3bin[jtypesToI_d['ak5ft']].Draw()
    hd_mass_3bin[jtypesToI_d['ak5tr']].Draw("sames")
    hd_mass_3bin[jtypesToI_d['ak5pr']].Draw("sames")
    hd_mass_3bin[jtypesToI_d['ak5']].Draw("sames")

    c2.cd(6)
    hd_mass_4bin[jtypesToI_d['ak5ft']].Draw()
    hd_mass_4bin[jtypesToI_d['ak5tr']].Draw("sames")
    hd_mass_4bin[jtypesToI_d['ak5pr']].Draw("sames")
    hd_mass_4bin[jtypesToI_d['ak5']].Draw("sames")

    c2.SaveAs(figdir+"/test0"+suffix)

    #################

    c27 = ROOT.TCanvas("c27","c27",1600,800)
    c27.Divide(3,2)
    c27.cd(1)
    hd_mass[jtypesToI_d['ak7pr']].Draw()
    hd_mass[jtypesToI_d['ak7tr']].Draw("sames")
    hd_mass[jtypesToI_d['ak7ft']].Draw("sames")
    hd_mass[jtypesToI_d['ak7']].Draw("sames")

    c27.cd(2)
    hd_mass_0bin[jtypesToI_d['ak7ft']].Draw()
    hd_mass_0bin[jtypesToI_d['ak7tr']].Draw("sames")
    hd_mass_0bin[jtypesToI_d['ak7pr']].Draw("sames")
    hd_mass_0bin[jtypesToI_d['ak7']].Draw("sames")

    c27.cd(3)
    hd_mass_1bin[jtypesToI_d['ak7ft']].Draw()
    hd_mass_1bin[jtypesToI_d['ak7tr']].Draw("sames")
    hd_mass_1bin[jtypesToI_d['ak7pr']].Draw("sames")
    hd_mass_1bin[jtypesToI_d['ak7']].Draw("sames")

    c27.cd(4)
    hd_mass_2bin[jtypesToI_d['ak7ft']].Draw()
    hd_mass_2bin[jtypesToI_d['ak7tr']].Draw("sames")
    hd_mass_2bin[jtypesToI_d['ak7pr']].Draw("sames")
    hd_mass_2bin[jtypesToI_d['ak7']].Draw("sames")

    c27.cd(5)
    hd_mass_3bin[jtypesToI_d['ak7ft']].Draw()
    hd_mass_3bin[jtypesToI_d['ak7tr']].Draw("sames")
    hd_mass_3bin[jtypesToI_d['ak7pr']].Draw("sames")
    hd_mass_3bin[jtypesToI_d['ak7']].Draw("sames")

    c27.cd(6)
    hd_mass_4bin[jtypesToI_d['ak7ft']].Draw()
    hd_mass_4bin[jtypesToI_d['ak7tr']].Draw("sames")
    hd_mass_4bin[jtypesToI_d['ak7pr']].Draw("sames")
    hd_mass_4bin[jtypesToI_d['ak7']].Draw("sames")

    c27.SaveAs(figdir+"/test0_ak7"+suffix)

    #################
    
    c28 = ROOT.TCanvas("c28","c28",1600,800)
    c28.Divide(3,2)
    c28.cd(1)
    hd_mass[jtypesToI_d['ak8pr']].Draw()
    hd_mass[jtypesToI_d['ak8tr']].Draw("sames")
    hd_mass[jtypesToI_d['ak8ft']].Draw("sames")
    hd_mass[jtypesToI_d['ak8']].Draw("sames")
    
    c28.cd(2)
    hd_mass_0bin[jtypesToI_d['ak8ft']].Draw()
    hd_mass_0bin[jtypesToI_d['ak8tr']].Draw("sames")
    hd_mass_0bin[jtypesToI_d['ak8pr']].Draw("sames")
    hd_mass_0bin[jtypesToI_d['ak8']].Draw("sames")
    
    c28.cd(3)
    hd_mass_1bin[jtypesToI_d['ak8ft']].Draw()
    hd_mass_1bin[jtypesToI_d['ak8tr']].Draw("sames")
    hd_mass_1bin[jtypesToI_d['ak8pr']].Draw("sames")
    hd_mass_1bin[jtypesToI_d['ak8']].Draw("sames")
    
    c28.cd(4)
    hd_mass_2bin[jtypesToI_d['ak8ft']].Draw()
    hd_mass_2bin[jtypesToI_d['ak8tr']].Draw("sames")
    hd_mass_2bin[jtypesToI_d['ak8pr']].Draw("sames")
    hd_mass_2bin[jtypesToI_d['ak8']].Draw("sames")
    
    c28.cd(5)
    hd_mass_3bin[jtypesToI_d['ak8ft']].Draw()
    hd_mass_3bin[jtypesToI_d['ak8tr']].Draw("sames")
    hd_mass_3bin[jtypesToI_d['ak8pr']].Draw("sames")
    hd_mass_3bin[jtypesToI_d['ak8']].Draw("sames")
    
    c28.cd(6)
    hd_mass_4bin[jtypesToI_d['ak8ft']].Draw()
    hd_mass_4bin[jtypesToI_d['ak8tr']].Draw("sames")
    hd_mass_4bin[jtypesToI_d['ak8pr']].Draw("sames")
    hd_mass_4bin[jtypesToI_d['ak8']].Draw("sames")
    
    c28.SaveAs(figdir+"/test0_ak8"+suffix)

    ############################################################
    # C O M P R E H E N S I V E   P L O T S 
    
    


    ############################################################

############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################

def plotter2D(mcname,dataname,figdir):
        
    fm = ROOT.TFile(mcname)
    fd = ROOT.TFile(dataname)
    
    print "2D files: ", mcname,", ", dataname
    #theutils = myutils()

    ############################################################
    # S P E C I F I C   P L O T S
    ##### 
    hmrat_mass_ovAK5 = []
    hmrat_pt_ovAK5 = []    
    hmrat_mass_ovAK5g = []
    hmrat_pt_ovAK5g = []    
    hmrat_mass_ovAK7 = []
    hmrat_pt_ovAK7 = []    
    hmrat_mass_ovAK7g = []
    hmrat_pt_ovAK7g = []    
    hmrat_mass_ovAK8 = []
    hmrat_pt_ovAK8 = []    
    hmrat_mass_ovAK8g = []
    hmrat_pt_ovAK8g = []    
    
    ## pt ratio in MC 
    pmrPt_pt_ovAK5 = []     
    pmrPt_pt_ovAK5g = []         
    pmrPt_pt_ovAK7 = []     
    pmrPt_pt_ovAK7g = []         
    pmrPt_pt_ovAK8 = []     
    pmrPt_pt_ovAK8g = []         
    pmrNV_pt_ovAK5 = []     
    pmrNV_pt_ovAK5g = []         
    pmrNV_pt_ovAK7 = []     
    pmrNV_pt_ovAK7g = []         
    pmrNV_pt_ovAK8 = []     
    pmrNV_pt_ovAK8g = []         
    pmrEta_pt_ovAK8g = []         
    pmrEta_pt_ovAK5 = []     
    pmrEta_pt_ovAK5g = []         
    pmrEta_pt_ovAK7 = []     
    pmrEta_pt_ovAK7g = []         
    pmrEta_pt_ovAK8 = []     
    pmrEta_pt_ovAK8g = []         
    
    # profile, ratio of mass, vs pT
    pmrPt_mass_ovAK5 = []    
    
    hdrat_mass_ovAK5 = []
    hdrat_pt_ovAK5 = []    
    pdrPt_mass_ovAK5 = []    
    pdrPt_pt_ovAK5 = []    

    for x in range(len(jtypes_m)):
        hmrat_mass_ovAK5.append( fm.Get("hrat_"+jtypes_m[x]+"_mass_ovAK5") ) 
        hmrat_pt_ovAK5.append( fm.Get("hrat_"+jtypes_m[x]+"_pt_ovAK5") ) 
        hmrat_mass_ovAK5g.append( fm.Get("hrat_"+jtypes_m[x]+"_mass_ovAK5g") ) 
        hmrat_pt_ovAK5g.append( fm.Get("hrat_"+jtypes_m[x]+"_pt_ovAK5g") ) 
        hmrat_mass_ovAK7.append( fm.Get("hrat_"+jtypes_m[x]+"_mass_ovAK7") ) 
        hmrat_pt_ovAK7.append( fm.Get("hrat_"+jtypes_m[x]+"_pt_ovAK7") ) 
        hmrat_mass_ovAK7g.append( fm.Get("hrat_"+jtypes_m[x]+"_mass_ovAK7g") ) 
        hmrat_pt_ovAK7g.append( fm.Get("hrat_"+jtypes_m[x]+"_pt_ovAK7g") ) 
        hmrat_mass_ovAK8.append( fm.Get("hrat_"+jtypes_m[x]+"_mass_ovAK8") ) 
        hmrat_pt_ovAK8.append( fm.Get("hrat_"+jtypes_m[x]+"_pt_ovAK8") ) 
        hmrat_mass_ovAK8g.append( fm.Get("hrat_"+jtypes_m[x]+"_mass_ovAK8g") ) 
        hmrat_pt_ovAK8g.append( fm.Get("hrat_"+jtypes_m[x]+"_pt_ovAK8g") ) 

        pmrPt_pt_ovAK5.append( fm.Get("prPt_pt"+jtypes_m[x]+"_ovAK5") ) 
        pmrPt_pt_ovAK5g.append( fm.Get("prPt_pt"+jtypes_m[x]+"_ovAK5g") ) 
        pmrPt_pt_ovAK7.append( fm.Get("prPt_pt"+jtypes_m[x]+"_ovAK7") ) 
        pmrPt_pt_ovAK7g.append( fm.Get("prPt_pt"+jtypes_m[x]+"_ovAK7g") ) 
        pmrPt_pt_ovAK8.append( fm.Get("prPt_pt"+jtypes_m[x]+"_ovAK8") ) 
        pmrPt_pt_ovAK8g.append( fm.Get("prPt_pt"+jtypes_m[x]+"_ovAK8g") ) 
        pmrNV_pt_ovAK5.append( fm.Get("prNV_pt"+jtypes_m[x]+"_ovAK5") ) 
        pmrNV_pt_ovAK5g.append( fm.Get("prNV_pt"+jtypes_m[x]+"_ovAK5g") ) 
        pmrNV_pt_ovAK7.append( fm.Get("prNV_pt"+jtypes_m[x]+"_ovAK7") ) 
        pmrNV_pt_ovAK7g.append( fm.Get("prNV_pt"+jtypes_m[x]+"_ovAK7g") ) 
        pmrNV_pt_ovAK8.append( fm.Get("prNV_pt"+jtypes_m[x]+"_ovAK8") ) 
        pmrNV_pt_ovAK8g.append( fm.Get("prNV_pt"+jtypes_m[x]+"_ovAK8g") ) 
        pmrEta_pt_ovAK5.append( fm.Get("prEta_pt"+jtypes_m[x]+"_ovAK5") ) 
        pmrEta_pt_ovAK5g.append( fm.Get("prEta_pt"+jtypes_m[x]+"_ovAK5g") ) 
        pmrEta_pt_ovAK7.append( fm.Get("prEta_pt"+jtypes_m[x]+"_ovAK7") ) 
        pmrEta_pt_ovAK7g.append( fm.Get("prEta_pt"+jtypes_m[x]+"_ovAK7g") ) 
        pmrEta_pt_ovAK8.append( fm.Get("prEta_pt"+jtypes_m[x]+"_ovAK8") ) 
        pmrEta_pt_ovAK8g.append( fm.Get("prEta_pt"+jtypes_m[x]+"_ovAK8g") ) 

        pmrPt_mass_ovAK5.append( fm.Get("prPt_mass"+jtypes_m[x]+"_ovAK5") ) 

        y = x+1
        SetHistProperties(hmrat_pt_ovAK5[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 1, 1)
        SetHistProperties(hmrat_mass_ovAK5[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 1, 1)
        SetHistProperties(hmrat_pt_ovAK5g[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 1, 1)
        SetHistProperties(hmrat_mass_ovAK5g[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 1, 1)
        SetHistProperties(hmrat_pt_ovAK7[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 1, 1)
        SetHistProperties(hmrat_mass_ovAK7[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 1, 1)
        SetHistProperties(hmrat_pt_ovAK7g[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 1, 1)
        SetHistProperties(hmrat_mass_ovAK7g[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 1, 1)
        SetHistProperties(hmrat_pt_ovAK8[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 1, 1)
        SetHistProperties(hmrat_mass_ovAK8[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 1, 1)
        SetHistProperties(hmrat_pt_ovAK8g[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 1, 1)
        SetHistProperties(hmrat_mass_ovAK8g[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 1, 1)

        SetHistProperties(pmrPt_pt_ovAK5[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 20, 1)
        SetHistProperties(pmrPt_pt_ovAK5g[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 20, 1)
        SetHistProperties(pmrPt_pt_ovAK7[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 20, 1)
        SetHistProperties(pmrPt_pt_ovAK7g[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 20, 1)
        SetHistProperties(pmrPt_pt_ovAK8[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 20, 1)
        SetHistProperties(pmrPt_pt_ovAK8g[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 20, 1)
        SetHistProperties(pmrNV_pt_ovAK5[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 20, 1)
        SetHistProperties(pmrNV_pt_ovAK5g[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 20, 1)
        SetHistProperties(pmrNV_pt_ovAK7[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 20, 1)
        SetHistProperties(pmrNV_pt_ovAK7g[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 20, 1)
        SetHistProperties(pmrNV_pt_ovAK8[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 20, 1)
        SetHistProperties(pmrNV_pt_ovAK8g[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 20, 1)
        SetHistProperties(pmrEta_pt_ovAK5[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 20, 1)
        SetHistProperties(pmrEta_pt_ovAK5g[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 20, 1)
        SetHistProperties(pmrEta_pt_ovAK7[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 20, 1)
        SetHistProperties(pmrEta_pt_ovAK7g[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 20, 1)
        SetHistProperties(pmrEta_pt_ovAK8[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 20, 1)
        SetHistProperties(pmrEta_pt_ovAK8g[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 20, 1)

        SetHistProperties(pmrPt_mass_ovAK5[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 1, 1)

    for x in range(len(jtypes_d)):        
        hdrat_mass_ovAK5.append( fd.Get("hrat_"+jtypes_d[x]+"_mass_ovAK5") ) 
        hdrat_pt_ovAK5.append( fd.Get("hrat_"+jtypes_d[x]+"_pt_ovAK5") ) 
        pdrPt_mass_ovAK5.append( fd.Get("prPt_mass"+jtypes_d[x]+"_ovAK5") ) 
        pdrPt_pt_ovAK5.append( fd.Get("prPt_pt"+jtypes_d[x]+"_ovAK5") ) 
        y = x+1
        SetHistProperties(hdrat_pt_ovAK5[x], cmap_d[y],cmap_d[y],cmap_d[y], 1, 1, 1)
        SetHistProperties(hdrat_mass_ovAK5[x], cmap_d[y],cmap_d[y],cmap_d[y], 1, 1, 1)
        SetHistProperties(pdrPt_mass_ovAK5[x], cmap_d[y],cmap_d[y],cmap_d[y], 1, 1, 1)
        SetHistProperties(pdrPt_pt_ovAK5[x], cmap_d[y],cmap_d[y],cmap_d[y], 1, 1, 1)

    
    c1 = ROOT.TCanvas("c1","c1",1200,800)
    c1.Divide(2,1)
    c1.cd(1)
    hmrat_mass_ovAK5g[jtypesToI_m['ak5']].Draw()
    hmrat_mass_ovAK5g[jtypesToI_m['ak5ft']].Draw("sames")
    hmrat_mass_ovAK5g[jtypesToI_m['ak5tr']].Draw("sames")
    hmrat_mass_ovAK5g[jtypesToI_m['ak5pr']].Draw("sames")
    c1.cd(2)
    hmrat_pt_ovAK5g[jtypesToI_m['ak5']].Draw()
    hmrat_pt_ovAK5g[jtypesToI_m['ak5ft']].Draw("sames")
    hmrat_pt_ovAK5g[jtypesToI_m['ak5tr']].Draw("sames")
    hmrat_pt_ovAK5g[jtypesToI_m['ak5pr']].Draw("sames")
    c1.SaveAs(figdir+"/ratio1D_ak5"+suffix)
    c17 = ROOT.TCanvas("c17","c17",1200,800)
    c17.Divide(2,1)
    c17.cd(1)
    hmrat_mass_ovAK7g[jtypesToI_m['ak7']].Draw()
    hmrat_mass_ovAK7g[jtypesToI_m['ak7ft']].Draw("sames")
    hmrat_mass_ovAK7g[jtypesToI_m['ak7tr']].Draw("sames")
    hmrat_mass_ovAK7g[jtypesToI_m['ak7pr']].Draw("sames")
    c17.cd(2)
    hmrat_pt_ovAK7g[jtypesToI_m['ak7']].Draw()
    hmrat_pt_ovAK7g[jtypesToI_m['ak7ft']].Draw("sames")
    hmrat_pt_ovAK7g[jtypesToI_m['ak7tr']].Draw("sames")
    hmrat_pt_ovAK7g[jtypesToI_m['ak7pr']].Draw("sames")
    c17.SaveAs(figdir+"/ratio1D_ak7"+suffix)
    c18 = ROOT.TCanvas("c18","c18",1200,800)
    c18.Divide(2,1)
    c18.cd(1)
    hmrat_mass_ovAK8g[jtypesToI_m['ak8']].Draw()
    hmrat_mass_ovAK8g[jtypesToI_m['ak8ft']].Draw("sames")
    hmrat_mass_ovAK8g[jtypesToI_m['ak8tr']].Draw("sames")
    hmrat_mass_ovAK8g[jtypesToI_m['ak8pr']].Draw("sames")
    c18.cd(2)
    hmrat_pt_ovAK8g[jtypesToI_m['ak8']].Draw()
    hmrat_pt_ovAK8g[jtypesToI_m['ak8ft']].Draw("sames")
    hmrat_pt_ovAK8g[jtypesToI_m['ak8tr']].Draw("sames")
    hmrat_pt_ovAK8g[jtypesToI_m['ak8pr']].Draw("sames")
    c18.SaveAs(figdir+"/ratio1D_ak8"+suffix)

    c2 = ROOT.TCanvas("c2","c2",1800,800)
    c2.Divide(3,1)
    c2.cd(1)
    h5 = theutils.GetFitSlicesY( pmrPt_pt_ovAK5g[jtypesToI_m['ak5']], 1 )
    h5.GetYaxis().SetRangeUser(0.8,1.1)
    h5.Draw()
    h5f = theutils.GetFitSlicesY( pmrPt_pt_ovAK5g[jtypesToI_m['ak5ft']], 1 )
    h5f.Draw("sames")
    h5t = theutils.GetFitSlicesY( pmrPt_pt_ovAK5g[jtypesToI_m['ak5tr']], 1 )
    h5t.Draw("sames")
    h5p = theutils.GetFitSlicesY( pmrPt_pt_ovAK5g[jtypesToI_m['ak5pr']], 1 )
    h5p.Draw("sames")
    c2.cd(2)
    h7 = theutils.GetFitSlicesY( pmrPt_pt_ovAK7g[jtypesToI_m['ak7']], 1 )
    h7.GetYaxis().SetRangeUser(0.8,1.1)
    h7.Draw()
    h7f = theutils.GetFitSlicesY( pmrPt_pt_ovAK7g[jtypesToI_m['ak7ft']], 1 )
    h7f.Draw("sames")
    h7t = theutils.GetFitSlicesY( pmrPt_pt_ovAK7g[jtypesToI_m['ak7tr']], 1 )
    h7t.Draw("sames")
    h7p = theutils.GetFitSlicesY( pmrPt_pt_ovAK7g[jtypesToI_m['ak7pr']], 1 )
    h7p.Draw("sames")
    c2.cd(3)
    h8 = theutils.GetFitSlicesY( pmrPt_pt_ovAK8g[jtypesToI_m['ak8']], 1 )
    h8.GetYaxis().SetRangeUser(0.8,1.1)
    h8.Draw()
    h8f = theutils.GetFitSlicesY( pmrPt_pt_ovAK8g[jtypesToI_m['ak8ft']], 1 )
    h8f.Draw("sames")
    h8t = theutils.GetFitSlicesY( pmrPt_pt_ovAK8g[jtypesToI_m['ak8tr']], 1 )
    h8t.Draw("sames")
    h8p = theutils.GetFitSlicesY( pmrPt_pt_ovAK8g[jtypesToI_m['ak8pr']], 1 )
    h8p.Draw("sames")
    c2.SaveAs(figdir+"/ptRatioVsPt_mean"+suffix)

    c2s = ROOT.TCanvas("c2s","c2s",1800,800)
    c2s.Divide(3,1)
    c2s.cd(1)
    hs5 = theutils.GetFitSlicesY( pmrPt_pt_ovAK5g[jtypesToI_m['ak5']], 2 )
    hs5.GetYaxis().SetRangeUser(0.,0.25)
    hs5.Draw()
    hs5f = theutils.GetFitSlicesY( pmrPt_pt_ovAK5g[jtypesToI_m['ak5ft']], 2 )
    hs5f.Draw("sames")
    hs5t = theutils.GetFitSlicesY( pmrPt_pt_ovAK5g[jtypesToI_m['ak5tr']], 2 )
    hs5t.Draw("sames")
    hs5p = theutils.GetFitSlicesY( pmrPt_pt_ovAK5g[jtypesToI_m['ak5pr']], 2 )
    hs5p.Draw("sames")
    c2s.cd(2)
    hs7 = theutils.GetFitSlicesY( pmrPt_pt_ovAK7g[jtypesToI_m['ak7']], 2 )
    hs7.GetYaxis().SetRangeUser(0.,0.25)
    hs7.Draw()
    hs7f = theutils.GetFitSlicesY( pmrPt_pt_ovAK7g[jtypesToI_m['ak7ft']], 2 )
    hs7f.Draw("sames")
    hs7t = theutils.GetFitSlicesY( pmrPt_pt_ovAK7g[jtypesToI_m['ak7tr']], 2 )
    hs7t.Draw("sames")
    hs7p = theutils.GetFitSlicesY( pmrPt_pt_ovAK7g[jtypesToI_m['ak7pr']], 2 )
    hs7p.Draw("sames")
    c2s.cd(3)
    hs8 = theutils.GetFitSlicesY( pmrPt_pt_ovAK8g[jtypesToI_m['ak8']], 2 )
    hs8.GetYaxis().SetRangeUser(0.,0.25)
    hs8.Draw()
    hs8f = theutils.GetFitSlicesY( pmrPt_pt_ovAK8g[jtypesToI_m['ak8ft']], 2 )
    hs8f.Draw("sames")
    hs8t = theutils.GetFitSlicesY( pmrPt_pt_ovAK8g[jtypesToI_m['ak8tr']], 2 )
    hs8t.Draw("sames")
    hs8p = theutils.GetFitSlicesY( pmrPt_pt_ovAK8g[jtypesToI_m['ak8pr']], 2 )
    hs8p.Draw("sames")
    c2s.SaveAs(figdir+"/ptRatioVsPt_sigma"+suffix)
    
    c2nvs = ROOT.TCanvas("c2nvs","c2nvs",1800,800)
    c2nvs.Divide(3,1)
    c2nvs.cd(1)
    h5 = theutils.GetFitSlicesY( pmrNV_pt_ovAK5g[jtypesToI_m['ak5']], 1 )
    h5.GetYaxis().SetRangeUser(0.8,1.1)
    h5.Draw()
    h5f = theutils.GetFitSlicesY( pmrNV_pt_ovAK5g[jtypesToI_m['ak5ft']], 1 )
    h5f.Draw("sames")
    h5t = theutils.GetFitSlicesY( pmrNV_pt_ovAK5g[jtypesToI_m['ak5tr']], 1 )
    h5t.Draw("sames")
    h5p = theutils.GetFitSlicesY( pmrNV_pt_ovAK5g[jtypesToI_m['ak5pr']], 1 )
    h5p.Draw("sames")
    c2nvs.cd(2)
    h7 = theutils.GetFitSlicesY( pmrNV_pt_ovAK7g[jtypesToI_m['ak7']], 1 )
    h7.GetYaxis().SetRangeUser(0.8,1.1)
    h7.Draw()
    h7f = theutils.GetFitSlicesY( pmrNV_pt_ovAK7g[jtypesToI_m['ak7ft']], 1 )
    h7f.Draw("sames")
    h7t = theutils.GetFitSlicesY( pmrNV_pt_ovAK7g[jtypesToI_m['ak7tr']], 1 )
    h7t.Draw("sames")
    h7p = theutils.GetFitSlicesY( pmrNV_pt_ovAK7g[jtypesToI_m['ak7pr']], 1 )
    h7p.Draw("sames")
    c2nvs.cd(3)
    h8 = theutils.GetFitSlicesY( pmrNV_pt_ovAK8g[jtypesToI_m['ak8']], 1 )
    h8.GetYaxis().SetRangeUser(0.8,1.1)
    h8.Draw()
    h8f = theutils.GetFitSlicesY( pmrNV_pt_ovAK8g[jtypesToI_m['ak8ft']], 1 )
    h8f.Draw("sames")
    h8t = theutils.GetFitSlicesY( pmrNV_pt_ovAK8g[jtypesToI_m['ak8tr']], 1 )
    h8t.Draw("sames")
    h8p = theutils.GetFitSlicesY( pmrNV_pt_ovAK8g[jtypesToI_m['ak8pr']], 1 )
    h8p.Draw("sames")
    c2nvs.SaveAs(figdir+"/ptRatioVsNV_mean"+suffix)

    c2nvss = ROOT.TCanvas("c2nvss","c2nvss",1800,800)
    c2nvss.Divide(3,1)
    c2nvss.cd(1)
    hs5 = theutils.GetFitSlicesY( pmrNV_pt_ovAK5g[jtypesToI_m['ak5']], 2 )
    hs5.GetYaxis().SetRangeUser(0.,0.25)
    hs5.Draw()
    hs5f = theutils.GetFitSlicesY( pmrNV_pt_ovAK5g[jtypesToI_m['ak5ft']], 2 )
    hs5f.Draw("sames")
    hs5t = theutils.GetFitSlicesY( pmrNV_pt_ovAK5g[jtypesToI_m['ak5tr']], 2 )
    hs5t.Draw("sames")
    hs5p = theutils.GetFitSlicesY( pmrNV_pt_ovAK5g[jtypesToI_m['ak5pr']], 2 )
    hs5p.Draw("sames")
    c2nvss.cd(2)
    hs7 = theutils.GetFitSlicesY( pmrNV_pt_ovAK7g[jtypesToI_m['ak7']], 2 )
    hs7.GetYaxis().SetRangeUser(0.,0.25)
    hs7.Draw()
    hs7f = theutils.GetFitSlicesY( pmrNV_pt_ovAK7g[jtypesToI_m['ak7ft']], 2 )
    hs7f.Draw("sames")
    hs7t = theutils.GetFitSlicesY( pmrNV_pt_ovAK7g[jtypesToI_m['ak7tr']], 2 )
    hs7t.Draw("sames")
    hs7p = theutils.GetFitSlicesY( pmrNV_pt_ovAK7g[jtypesToI_m['ak7pr']], 2 )
    hs7p.Draw("sames")
    c2nvss.cd(3)
    hs8 = theutils.GetFitSlicesY( pmrNV_pt_ovAK8g[jtypesToI_m['ak8']], 2 )
    hs8.GetYaxis().SetRangeUser(0.,0.25)
    hs8.Draw()
    hs8f = theutils.GetFitSlicesY( pmrNV_pt_ovAK8g[jtypesToI_m['ak8ft']], 2 )
    hs8f.Draw("sames")
    hs8t = theutils.GetFitSlicesY( pmrNV_pt_ovAK8g[jtypesToI_m['ak8tr']], 2 )
    hs8t.Draw("sames")
    hs8p = theutils.GetFitSlicesY( pmrNV_pt_ovAK8g[jtypesToI_m['ak8pr']], 2 )
    hs8p.Draw("sames")
    c2nvss.SaveAs(figdir+"/ptRatioVsNV_sigma"+suffix)

    c2etas = ROOT.TCanvas("c2etas","c2etas",1800,800)
    c2etas.Divide(3,1)
    c2etas.cd(1)
    h5 = theutils.GetFitSlicesY( pmrEta_pt_ovAK5g[jtypesToI_m['ak5']], 1 )
    h5.GetYaxis().SetRangeUser(0.8,1.1)
    h5.Draw()
    h5f = theutils.GetFitSlicesY( pmrEta_pt_ovAK5g[jtypesToI_m['ak5ft']], 1 )
    h5f.Draw("sames")
    h5t = theutils.GetFitSlicesY( pmrEta_pt_ovAK5g[jtypesToI_m['ak5tr']], 1 )
    h5t.Draw("sames")
    h5p = theutils.GetFitSlicesY( pmrEta_pt_ovAK5g[jtypesToI_m['ak5pr']], 1 )
    h5p.Draw("sames")
    c2etas.cd(2)
    h7 = theutils.GetFitSlicesY( pmrEta_pt_ovAK7g[jtypesToI_m['ak7']], 1 )
    h7.GetYaxis().SetRangeUser(0.8,1.1)
    h7.Draw()
    h7f = theutils.GetFitSlicesY( pmrEta_pt_ovAK7g[jtypesToI_m['ak7ft']], 1 )
    h7f.Draw("sames")
    h7t = theutils.GetFitSlicesY( pmrEta_pt_ovAK7g[jtypesToI_m['ak7tr']], 1 )
    h7t.Draw("sames")
    h7p = theutils.GetFitSlicesY( pmrEta_pt_ovAK7g[jtypesToI_m['ak7pr']], 1 )
    h7p.Draw("sames")
    c2etas.cd(3)
    h8 = theutils.GetFitSlicesY( pmrEta_pt_ovAK8g[jtypesToI_m['ak8']], 1 )
    h8.GetYaxis().SetRangeUser(0.8,1.1)
    h8.Draw()
    h8f = theutils.GetFitSlicesY( pmrEta_pt_ovAK8g[jtypesToI_m['ak8ft']], 1 )
    h8f.Draw("sames")
    h8t = theutils.GetFitSlicesY( pmrEta_pt_ovAK8g[jtypesToI_m['ak8tr']], 1 )
    h8t.Draw("sames")
    h8p = theutils.GetFitSlicesY( pmrEta_pt_ovAK8g[jtypesToI_m['ak8pr']], 1 )
    h8p.Draw("sames")
    c2etas.SaveAs(figdir+"/ptRatioVsEta_mean"+suffix)

    c2etass = ROOT.TCanvas("c2etass","c2etass",1800,800)
    c2etass.Divide(3,1)
    c2etass.cd(1)
    hs5 = theutils.GetFitSlicesY( pmrEta_pt_ovAK5g[jtypesToI_m['ak5']], 2 )
    hs5.GetYaxis().SetRangeUser(0.,0.25)
    hs5.Draw()
    hs5f = theutils.GetFitSlicesY( pmrEta_pt_ovAK5g[jtypesToI_m['ak5ft']], 2 )
    hs5f.Draw("sames")
    hs5t = theutils.GetFitSlicesY( pmrEta_pt_ovAK5g[jtypesToI_m['ak5tr']], 2 )
    hs5t.Draw("sames")
    hs5p = theutils.GetFitSlicesY( pmrEta_pt_ovAK5g[jtypesToI_m['ak5pr']], 2 )
    hs5p.Draw("sames")
    c2etass.cd(2)
    hs7 = theutils.GetFitSlicesY( pmrEta_pt_ovAK7g[jtypesToI_m['ak7']], 2 )
    hs7.GetYaxis().SetRangeUser(0.,0.25)
    hs7.Draw()
    hs7f = theutils.GetFitSlicesY( pmrEta_pt_ovAK7g[jtypesToI_m['ak7ft']], 2 )
    hs7f.Draw("sames")
    hs7t = theutils.GetFitSlicesY( pmrEta_pt_ovAK7g[jtypesToI_m['ak7tr']], 2 )
    hs7t.Draw("sames")
    hs7p = theutils.GetFitSlicesY( pmrEta_pt_ovAK7g[jtypesToI_m['ak7pr']], 2 )
    hs7p.Draw("sames")
    c2etass.cd(3)
    hs8 = theutils.GetFitSlicesY( pmrEta_pt_ovAK8g[jtypesToI_m['ak8']], 2 )
    hs8.GetYaxis().SetRangeUser(0.,0.25)
    hs8.Draw()
    hs8f = theutils.GetFitSlicesY( pmrEta_pt_ovAK8g[jtypesToI_m['ak8ft']], 2 )
    hs8f.Draw("sames")
    hs8t = theutils.GetFitSlicesY( pmrEta_pt_ovAK8g[jtypesToI_m['ak8tr']], 2 )
    hs8t.Draw("sames")
    hs8p = theutils.GetFitSlicesY( pmrEta_pt_ovAK8g[jtypesToI_m['ak8pr']], 2 )
    hs8p.Draw("sames")
    c2etass.SaveAs(figdir+"/ptRatioVsEta_sigma"+suffix)

############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################

def plotter2D_mass(mcname,dataname,figdir):
    
    #gROOT.ProcessLine('.L myutils.C++')
    #from ROOT import myutils, TH1F
    
    fm = ROOT.TFile(mcname)
    fd = ROOT.TFile(dataname)
    
    print "2D mass files: ", mcname,", ", dataname
    print "--------> 0"
    #theutils = myutils()

    print "--------> 1"
    ############################################################
    # S P E C I F I C   P L O T S
    #####       
    
    # profile, ratio of mass, vs pT
    pmrPt_mass_ovAK5 = []    
    pmrPt_mass_ovAK5g = []    
    pmrPt_mass_ovAK7 = []    
    pmrPt_mass_ovAK7g = []    
    pmrPt_mass_ovAK8 = []    
    pmrPt_mass_ovAK8g = []    
    pmrNV_mass_ovAK5 = []    
    pmrNV_mass_ovAK5g = []    
    pmrNV_mass_ovAK7 = []    
    pmrNV_mass_ovAK7g = []    
    pmrNV_mass_ovAK8 = []    
    pmrNV_mass_ovAK8g = []    
    pmrEta_mass_ovAK5 = []    
    pmrEta_mass_ovAK5g = []    
    pmrEta_mass_ovAK7 = []    
    pmrEta_mass_ovAK7g = []    
    pmrEta_mass_ovAK8 = []    
    pmrEta_mass_ovAK8g = []    
    
    pdrPt_mass_ovAK5 = []    
    pdrPt_mass_ovAK7 = []    
    pdrPt_mass_ovAK8 = []    
    pdrNV_mass_ovAK5 = []    
    pdrNV_mass_ovAK7 = []    
    pdrNV_mass_ovAK8 = []    
    pdrEta_mass_ovAK5 = []    
    pdrEta_mass_ovAK7 = []    
    pdrEta_mass_ovAK8 = []    

    
    print "--------> 2" 
    for x in range(len(jtypes_m)):
        
        pmrPt_mass_ovAK5.append( fm.Get("prPt_mass"+jtypes_m[x]+"_ovAK5") ) 
        pmrPt_mass_ovAK5g.append( fm.Get("prPt_mass"+jtypes_m[x]+"_ovAK5g") ) 
        pmrPt_mass_ovAK7.append( fm.Get("prPt_mass"+jtypes_m[x]+"_ovAK7") ) 
        pmrPt_mass_ovAK7g.append( fm.Get("prPt_mass"+jtypes_m[x]+"_ovAK7g") ) 
        pmrPt_mass_ovAK8.append( fm.Get("prPt_mass"+jtypes_m[x]+"_ovAK8") ) 
        pmrPt_mass_ovAK8g.append( fm.Get("prPt_mass"+jtypes_m[x]+"_ovAK8g") ) 
        pmrNV_mass_ovAK5.append( fm.Get("prNV_mass"+jtypes_m[x]+"_ovAK5") ) 
        pmrNV_mass_ovAK5g.append( fm.Get("prNV_mass"+jtypes_m[x]+"_ovAK5g") ) 
        pmrNV_mass_ovAK7.append( fm.Get("prNV_mass"+jtypes_m[x]+"_ovAK7") ) 
        pmrNV_mass_ovAK7g.append( fm.Get("prNV_mass"+jtypes_m[x]+"_ovAK7g") ) 
        pmrNV_mass_ovAK8.append( fm.Get("prNV_mass"+jtypes_m[x]+"_ovAK8") ) 
        pmrNV_mass_ovAK8g.append( fm.Get("prNV_mass"+jtypes_m[x]+"_ovAK8g") ) 
        pmrEta_mass_ovAK5.append( fm.Get("prEta_mass"+jtypes_m[x]+"_ovAK5") ) 
        pmrEta_mass_ovAK5g.append( fm.Get("prEta_mass"+jtypes_m[x]+"_ovAK5g") ) 
        pmrEta_mass_ovAK7.append( fm.Get("prEta_mass"+jtypes_m[x]+"_ovAK7") ) 
        pmrEta_mass_ovAK7g.append( fm.Get("prEta_mass"+jtypes_m[x]+"_ovAK7g") ) 
        pmrEta_mass_ovAK8.append( fm.Get("prEta_mass"+jtypes_m[x]+"_ovAK8") ) 
        pmrEta_mass_ovAK8g.append( fm.Get("prEta_mass"+jtypes_m[x]+"_ovAK8g") ) 
        
        y = x+1
        SetHistProperties_wName(pmrPt_mass_ovAK5[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 21, 1, "pmrPt_mass"+jtypes_m[x]+"_ovAK5")
        SetHistProperties_wName(pmrPt_mass_ovAK5g[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 21, 1, "pmrPt_mass"+jtypes_m[x]+"_ovAK5g")    
        SetHistProperties_wName(pmrPt_mass_ovAK7[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 21, 1, "pmrPt_mass"+jtypes_m[x]+"_ovAK7")
        SetHistProperties_wName(pmrPt_mass_ovAK7g[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 21, 1, "pmrPt_mass"+jtypes_m[x]+"_ovAK7g")    
        SetHistProperties_wName(pmrPt_mass_ovAK8[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 21, 1, "pmrPt_mass"+jtypes_m[x]+"_ovAK8")
        SetHistProperties_wName(pmrPt_mass_ovAK8g[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 21, 1, "pmrPt_mass"+jtypes_m[x]+"_ovAK8g")    
        SetHistProperties_wName(pmrNV_mass_ovAK5[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 21, 1, "pmrNV_mass"+jtypes_m[x]+"_ovAK5")
        SetHistProperties_wName(pmrNV_mass_ovAK5g[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 21, 1, "pmrNV_mass"+jtypes_m[x]+"_ovAK5g")    
        SetHistProperties_wName(pmrNV_mass_ovAK7[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 21, 1, "pmrNV_mass"+jtypes_m[x]+"_ovAK7")
        SetHistProperties_wName(pmrNV_mass_ovAK7g[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 21, 1, "pmrNV_mass"+jtypes_m[x]+"_ovAK7g")    
        SetHistProperties_wName(pmrNV_mass_ovAK8[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 21, 1, "pmrNV_mass"+jtypes_m[x]+"_ovAK8")
        SetHistProperties_wName(pmrNV_mass_ovAK8g[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 21, 1, "pmrNV_mass"+jtypes_m[x]+"_ovAK8g")    
        SetHistProperties_wName(pmrEta_mass_ovAK5[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 21, 1, "pmrEta_mass"+jtypes_m[x]+"_ovAK5")
        SetHistProperties_wName(pmrEta_mass_ovAK5g[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 21, 1, "pmrEta_mass"+jtypes_m[x]+"_ovAK5g")    
        SetHistProperties_wName(pmrEta_mass_ovAK7[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 21, 1, "pmrEta_mass"+jtypes_m[x]+"_ovAK7")
        SetHistProperties_wName(pmrEta_mass_ovAK7g[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 21, 1, "pmrEta_mass"+jtypes_m[x]+"_ovAK7g")    
        SetHistProperties_wName(pmrEta_mass_ovAK8[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 21, 1, "pmrEta_mass"+jtypes_m[x]+"_ovAK8")
        SetHistProperties_wName(pmrEta_mass_ovAK8g[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 21, 1, "pmrEta_mass"+jtypes_m[x]+"_ovAK8g")    
    
    for x in range(len(jtypes_d)):        

        pdrPt_mass_ovAK5.append( fd.Get("prPt_mass"+jtypes_d[x]+"_ovAK5") ) 
        pdrPt_mass_ovAK7.append( fd.Get("prPt_mass"+jtypes_d[x]+"_ovAK7") ) 
        pdrPt_mass_ovAK8.append( fd.Get("prPt_mass"+jtypes_d[x]+"_ovAK8") ) 
        pdrNV_mass_ovAK5.append( fd.Get("prNV_mass"+jtypes_d[x]+"_ovAK5") ) 
        pdrNV_mass_ovAK7.append( fd.Get("prNV_mass"+jtypes_d[x]+"_ovAK7") ) 
        pdrNV_mass_ovAK8.append( fd.Get("prNV_mass"+jtypes_d[x]+"_ovAK8") ) 
        pdrEta_mass_ovAK5.append( fd.Get("prEta_mass"+jtypes_d[x]+"_ovAK5") ) 
        pdrEta_mass_ovAK7.append( fd.Get("prEta_mass"+jtypes_d[x]+"_ovAK7") ) 
        pdrEta_mass_ovAK8.append( fd.Get("prEta_mass"+jtypes_d[x]+"_ovAK8") ) 
        
        y = x+1
        SetHistProperties(pdrPt_mass_ovAK5[x], cmap_d[y],cmap_d[y],cmap_d[y], 1, 24, 1)
        SetHistProperties(pdrPt_mass_ovAK7[x], cmap_d[y],cmap_d[y],cmap_d[y], 1, 24, 1)
        SetHistProperties(pdrPt_mass_ovAK8[x], cmap_d[y],cmap_d[y],cmap_d[y], 1, 24, 1)
        SetHistProperties(pdrNV_mass_ovAK5[x], cmap_d[y],cmap_d[y],cmap_d[y], 1, 24, 1)
        SetHistProperties(pdrNV_mass_ovAK7[x], cmap_d[y],cmap_d[y],cmap_d[y], 1, 24, 1)
        SetHistProperties(pdrNV_mass_ovAK8[x], cmap_d[y],cmap_d[y],cmap_d[y], 1, 24, 1)
        SetHistProperties(pdrEta_mass_ovAK5[x], cmap_d[y],cmap_d[y],cmap_d[y], 1, 24, 1)
        SetHistProperties(pdrEta_mass_ovAK7[x], cmap_d[y],cmap_d[y],cmap_d[y], 1, 24, 1)
        SetHistProperties(pdrEta_mass_ovAK8[x], cmap_d[y],cmap_d[y],cmap_d[y], 1, 24, 1)


    print "--------> 3"    
    cm1 = ROOT.TCanvas("cm1","cm1",1800,800)
    cm1.Divide(3,1)
    cm1.cd(1)
    h5 = pmrPt_mass_ovAK5g[jtypesToI_m['ak5']].ProfileX()
    h5f = pmrPt_mass_ovAK5g[jtypesToI_m['ak5ft']].ProfileX()
    h5t = pmrPt_mass_ovAK5g[jtypesToI_m['ak5tr']].ProfileX()
    h5p = pmrPt_mass_ovAK5g[jtypesToI_m['ak5pr']].ProfileX()
    h5.GetYaxis().SetRangeUser( 0.3,1.5 )
    h5.Draw()
    h5f.Draw("sames")
    h5t.Draw("sames")
    h5p.Draw("sames")
    cm1.cd(2)
    h7 = pmrPt_mass_ovAK7g[jtypesToI_m['ak7']].ProfileX()
    h7f = pmrPt_mass_ovAK7g[jtypesToI_m['ak7ft']].ProfileX()
    h7t = pmrPt_mass_ovAK7g[jtypesToI_m['ak7tr']].ProfileX()
    h7p = pmrPt_mass_ovAK7g[jtypesToI_m['ak7pr']].ProfileX()
    h7.GetYaxis().SetRangeUser( 0.3,1.5 )
    h7.Draw()
    h7f.Draw("sames")
    h7t.Draw("sames")
    h7p.Draw("sames")
    cm1.cd(3)
    h8 = pmrPt_mass_ovAK8g[jtypesToI_m['ak8']].ProfileX()
    h8f = pmrPt_mass_ovAK8g[jtypesToI_m['ak8ft']].ProfileX()
    h8t = pmrPt_mass_ovAK8g[jtypesToI_m['ak8tr']].ProfileX()
    h8p = pmrPt_mass_ovAK8g[jtypesToI_m['ak8pr']].ProfileX()
    h8.GetYaxis().SetRangeUser( 0.3,1.5 )
    h8.Draw()
    h8f.Draw("sames")
    h8t.Draw("sames")
    h8p.Draw("sames")
    cm1.SaveAs(figdir+"/massRatioOvGen_vsPt"+suffix)

    print "--------> 4"    

    cm2 = ROOT.TCanvas("cm2","cm2",1800,800)
    cm2.Divide(3,1)
    cm2.cd(1)
    h5 = pmrNV_mass_ovAK5g[jtypesToI_m['ak5']].ProfileX()
    h5f = pmrNV_mass_ovAK5g[jtypesToI_m['ak5ft']].ProfileX()
    h5t = pmrNV_mass_ovAK5g[jtypesToI_m['ak5tr']].ProfileX()
    h5p = pmrNV_mass_ovAK5g[jtypesToI_m['ak5pr']].ProfileX()
    h5.GetYaxis().SetRangeUser( 0.3,1.5 )
    h5.Draw()
    h5f.Draw("sames")
    h5t.Draw("sames")
    h5p.Draw("sames")
    cm2.cd(2)
    h7 = pmrNV_mass_ovAK7g[jtypesToI_m['ak7']].ProfileX()
    h7f = pmrNV_mass_ovAK7g[jtypesToI_m['ak7ft']].ProfileX()
    h7t = pmrNV_mass_ovAK7g[jtypesToI_m['ak7tr']].ProfileX()
    h7p = pmrNV_mass_ovAK7g[jtypesToI_m['ak7pr']].ProfileX()
    h7.GetYaxis().SetRangeUser( 0.3,1.5 )
    h7.Draw()
    h7f.Draw("sames")
    h7t.Draw("sames")
    h7p.Draw("sames")
    cm2.cd(3)
    h8 = pmrNV_mass_ovAK8g[jtypesToI_m['ak8']].ProfileX()
    h8f = pmrNV_mass_ovAK8g[jtypesToI_m['ak8ft']].ProfileX()
    h8t = pmrNV_mass_ovAK8g[jtypesToI_m['ak8tr']].ProfileX()
    h8p = pmrNV_mass_ovAK8g[jtypesToI_m['ak8pr']].ProfileX()
    h8.GetYaxis().SetRangeUser( 0.3,1.5 )
    h8.Draw()
    h8f.Draw("sames")
    h8t.Draw("sames")
    h8p.Draw("sames")
    cm2.SaveAs(figdir+"/massRatioOvGen_vsNV"+suffix)

    cm3 = ROOT.TCanvas("cm3","cm3",1800,800)
    cm3.Divide(3,1)
    cm3.cd(1)
    h5 = pmrEta_mass_ovAK5g[jtypesToI_m['ak5']].ProfileX()
    h5f = pmrEta_mass_ovAK5g[jtypesToI_m['ak5ft']].ProfileX()
    h5t = pmrEta_mass_ovAK5g[jtypesToI_m['ak5tr']].ProfileX()
    h5p = pmrEta_mass_ovAK5g[jtypesToI_m['ak5pr']].ProfileX()
    h5.GetYaxis().SetRangeUser( 0.3,1.5 )
    h5.Draw()
    h5f.Draw("sames")
    h5t.Draw("sames")
    h5p.Draw("sames")
    cm3.cd(2)
    h7 = pmrEta_mass_ovAK7g[jtypesToI_m['ak7']].ProfileX()
    h7f = pmrEta_mass_ovAK7g[jtypesToI_m['ak7ft']].ProfileX()
    h7t = pmrEta_mass_ovAK7g[jtypesToI_m['ak7tr']].ProfileX()
    h7p = pmrEta_mass_ovAK7g[jtypesToI_m['ak7pr']].ProfileX()
    h7.GetYaxis().SetRangeUser( 0.3,1.5 )
    h7.Draw()
    h7f.Draw("sames")
    h7t.Draw("sames")
    h7p.Draw("sames")
    cm3.cd(3)
    h8 = pmrEta_mass_ovAK8g[jtypesToI_m['ak8']].ProfileX()
    h8f = pmrEta_mass_ovAK8g[jtypesToI_m['ak8ft']].ProfileX()
    h8t = pmrEta_mass_ovAK8g[jtypesToI_m['ak8tr']].ProfileX()
    h8p = pmrEta_mass_ovAK8g[jtypesToI_m['ak8pr']].ProfileX()
    h8.GetYaxis().SetRangeUser( 0.3,1.5 )
    h8.Draw()
    h8f.Draw("sames")
    h8t.Draw("sames")
    h8p.Draw("sames")
    cm3.SaveAs(figdir+"/massRatioOvGen_vsEta"+suffix)

    #########################################################################
    print "--------> 5"    
    
    c1 = ROOT.TCanvas("c1","c1",1800,800)
    c1.Divide(3,1)
    c1.cd(1)
    h5f = pmrPt_mass_ovAK5[jtypesToI_m['ak5ft']].ProfileX()
    h5t = pmrPt_mass_ovAK5[jtypesToI_m['ak5tr']].ProfileX()
    h5p = pmrPt_mass_ovAK5[jtypesToI_m['ak5pr']].ProfileX()
    hd5f = pdrPt_mass_ovAK5[jtypesToI_d['ak5ft']].ProfileX()
    hd5t = pdrPt_mass_ovAK5[jtypesToI_d['ak5tr']].ProfileX()
    hd5p = pdrPt_mass_ovAK5[jtypesToI_d['ak5pr']].ProfileX()
    h5f.GetYaxis().SetRangeUser( 0.3,1.5 )
    h5f.Draw()
    h5t.Draw("sames")
    h5p.Draw("sames")
    hd5f.Draw("sames")
    hd5t.Draw("sames")
    hd5p.Draw("sames")
    c1.cd(2)
    h7f = pmrPt_mass_ovAK7[jtypesToI_m['ak7ft']].ProfileX()
    h7t = pmrPt_mass_ovAK7[jtypesToI_m['ak7tr']].ProfileX()
    h7p = pmrPt_mass_ovAK7[jtypesToI_m['ak7pr']].ProfileX()
    h7f.GetYaxis().SetRangeUser( 0.3,1.5 )
    h7f.Draw()
    h7t.Draw("sames")
    h7p.Draw("sames")
    hd7f = pdrPt_mass_ovAK7[jtypesToI_d['ak7ft']].ProfileX()
    hd7t = pdrPt_mass_ovAK7[jtypesToI_d['ak7tr']].ProfileX()
    hd7p = pdrPt_mass_ovAK7[jtypesToI_d['ak7pr']].ProfileX()
    hd7f.Draw("sames")
    hd7t.Draw("sames")
    hd7p.Draw("sames")
    c1.cd(3)
    h8f = pmrPt_mass_ovAK8[jtypesToI_m['ak8ft']].ProfileX()
    h8t = pmrPt_mass_ovAK8[jtypesToI_m['ak8tr']].ProfileX()
    h8p = pmrPt_mass_ovAK8[jtypesToI_m['ak8pr']].ProfileX()
    h8f.GetYaxis().SetRangeUser( 0.3,1.5 )
    h8f.Draw()
    h8t.Draw("sames")
    h8p.Draw("sames")
    hd8f = pdrPt_mass_ovAK8[jtypesToI_d['ak8ft']].ProfileX()
    hd8t = pdrPt_mass_ovAK8[jtypesToI_d['ak8tr']].ProfileX()
    hd8p = pdrPt_mass_ovAK8[jtypesToI_d['ak8pr']].ProfileX()
    hd8f.Draw("sames")
    hd8t.Draw("sames")
    hd8p.Draw("sames")
    c1.SaveAs(figdir+"/massRatioOvReco_vsPt"+suffix)

    c2 = ROOT.TCanvas("c2","c2",1800,800)
    c2.Divide(3,1)
    c2.cd(1)
    h5f = pmrNV_mass_ovAK5[jtypesToI_m['ak5ft']].ProfileX()
    h5t = pmrNV_mass_ovAK5[jtypesToI_m['ak5tr']].ProfileX()
    h5p = pmrNV_mass_ovAK5[jtypesToI_m['ak5pr']].ProfileX()
    h5f.GetYaxis().SetRangeUser( 0.3,1.5 )
    h5f.Draw()
    h5t.Draw("sames")
    h5p.Draw("sames")
    hd5f = pdrNV_mass_ovAK5[jtypesToI_d['ak5ft']].ProfileX()
    hd5t = pdrNV_mass_ovAK5[jtypesToI_d['ak5tr']].ProfileX()
    hd5p = pdrNV_mass_ovAK5[jtypesToI_d['ak5pr']].ProfileX()
    hd5f.Draw("sames")
    hd5t.Draw("sames")
    hd5p.Draw("sames")
    c2.cd(2)
    h7f = pmrNV_mass_ovAK7[jtypesToI_m['ak7ft']].ProfileX()
    h7t = pmrNV_mass_ovAK7[jtypesToI_m['ak7tr']].ProfileX()
    h7p = pmrNV_mass_ovAK7[jtypesToI_m['ak7pr']].ProfileX()
    h7f.GetYaxis().SetRangeUser( 0.3,1.5 )
    h7f.Draw()
    h7t.Draw("sames")
    h7p.Draw("sames")
    hd7f = pdrNV_mass_ovAK7[jtypesToI_d['ak7ft']].ProfileX()
    hd7t = pdrNV_mass_ovAK7[jtypesToI_d['ak7tr']].ProfileX()
    hd7p = pdrNV_mass_ovAK7[jtypesToI_d['ak7pr']].ProfileX()
    hd7f.Draw("sames")
    hd7t.Draw("sames")
    hd7p.Draw("sames")
    c2.cd(3)
    h8f = pmrNV_mass_ovAK8[jtypesToI_m['ak8ft']].ProfileX()
    h8t = pmrNV_mass_ovAK8[jtypesToI_m['ak8tr']].ProfileX()
    h8p = pmrNV_mass_ovAK8[jtypesToI_m['ak8pr']].ProfileX()
    h8f.GetYaxis().SetRangeUser( 0.3,1.5 )
    h8f.Draw()
    h8t.Draw("sames")
    h8p.Draw("sames")
    hd8f = pdrNV_mass_ovAK8[jtypesToI_d['ak8ft']].ProfileX()
    hd8t = pdrNV_mass_ovAK8[jtypesToI_d['ak8tr']].ProfileX()
    hd8p = pdrNV_mass_ovAK8[jtypesToI_d['ak8pr']].ProfileX()
    hd8f.Draw("sames")
    hd8t.Draw("sames")
    hd8p.Draw("sames")
    c2.SaveAs(figdir+"/massRatioOvReco_vsNV"+suffix)

    c3 = ROOT.TCanvas("c3","c3",1800,800)
    c3.Divide(3,1)
    c3.cd(1)
    h5f = pmrEta_mass_ovAK5[jtypesToI_m['ak5ft']].ProfileX()
    h5t = pmrEta_mass_ovAK5[jtypesToI_m['ak5tr']].ProfileX()
    h5p = pmrEta_mass_ovAK5[jtypesToI_m['ak5pr']].ProfileX()
    h5f.GetYaxis().SetRangeUser( 0.3,1.5 )
    h5f.Draw()
    h5t.Draw("sames")
    h5p.Draw("sames")
    hd5f = pdrEta_mass_ovAK5[jtypesToI_d['ak5ft']].ProfileX()
    hd5t = pdrEta_mass_ovAK5[jtypesToI_d['ak5tr']].ProfileX()
    hd5p = pdrEta_mass_ovAK5[jtypesToI_d['ak5pr']].ProfileX()
    hd5f.Draw("sames")
    hd5t.Draw("sames")
    hd5p.Draw("sames")
    c3.cd(2)
    h7f = pmrEta_mass_ovAK7[jtypesToI_m['ak7ft']].ProfileX()
    h7t = pmrEta_mass_ovAK7[jtypesToI_m['ak7tr']].ProfileX()
    h7p = pmrEta_mass_ovAK7[jtypesToI_m['ak7pr']].ProfileX()
    h7f.GetYaxis().SetRangeUser( 0.3,1.5 )
    h7f.Draw()
    h7t.Draw("sames")
    h7p.Draw("sames")
    hd7f = pdrEta_mass_ovAK7[jtypesToI_d['ak7ft']].ProfileX()
    hd7t = pdrEta_mass_ovAK7[jtypesToI_d['ak7tr']].ProfileX()
    hd7p = pdrEta_mass_ovAK7[jtypesToI_d['ak7pr']].ProfileX()
    hd7f.Draw("sames")
    hd7t.Draw("sames")
    hd7p.Draw("sames")
    c3.cd(3)
    h8f = pmrEta_mass_ovAK8[jtypesToI_m['ak8ft']].ProfileX()
    h8t = pmrEta_mass_ovAK8[jtypesToI_m['ak8tr']].ProfileX()
    h8p = pmrEta_mass_ovAK8[jtypesToI_m['ak8pr']].ProfileX()
    h8f.GetYaxis().SetRangeUser( 0.3,1.5 )
    h8f.Draw()
    h8t.Draw("sames")
    h8p.Draw("sames")
    hd8f = pdrEta_mass_ovAK8[jtypesToI_d['ak8ft']].ProfileX()
    hd8t = pdrEta_mass_ovAK8[jtypesToI_d['ak8tr']].ProfileX()
    hd8p = pdrEta_mass_ovAK8[jtypesToI_d['ak8pr']].ProfileX()
    hd8f.Draw("sames")
    hd8t.Draw("sames")
    hd8p.Draw("sames")
    c3.SaveAs(figdir+"/massRatioOvReco_vsEta"+suffix)


