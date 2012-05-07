from ROOT import gROOT, gStyle, gSystem, TLatex
import subprocess

jtypes_m = ["ak5","ak5tr","ak5ft","ak5pr","ak7","ak7tr","ak7ft","ak7pr","ak8","ak8tr","ak8ft","ak8pr","ca8","ca8pr","ca12ft","ca12mdft","ak5g","ak7g","ak8g","ca8g"]
jtypetrans_m = {"ak5":"AK5PF","ak5tr":"AK5TRIMMEDPF","ak5ft":"AK5FILTEREDPF","ak5pr":"AK5PRUNEDPF",
        "ak7":"AK7PF","ak7tr":"AK7TRIMMEDPF","ak7ft":"AK7FILTEREDPF","ak7pr":"AK7PRUNEDPF",
        "ak8":"AK8PF","ak8tr":"AK8TRIMMEDPF","ak8ft":"AK8FILTEREDPF","ak8pr":"AK8PRUNEDPF",
        "ca8":"CA8PF","ca8pr":"CA8PRUNEDPF","ca12ft":"CA12FILTEREDPF","ca12mdft":"CA12MASSDROPFILTEREDPF",
        "ak5g":"AK5GENJETSNONU","ak7g":"AK7GENJETSNONU","ak8g":"AK8GENJETSNONU","ca8g":"CA8GENJETSNONU"} 
jtypesToI_m = {"ak5":0,"ak5tr":1,"ak5ft":2,"ak5pr":3,
        "ak7":4,"ak7tr":5,"ak7ft":6,"ak7pr":7,
        "ak8":8,"ak8tr":9,"ak8ft":10,"ak8pr":11,
        "ca8":12,"ca8pr":13,"ca12ft":14,"ca12mdft":15,
        "ak5g":16,"ak7g":17,"ak8g":18,"ca8g":19}
    
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
    return scl

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

    print "files: ", mcname,", ", dataname

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
        SetHistProperties(hm_mass[x], y, y, y, 1, 1, 1)
        SetHistProperties(hm_mass_0bin[x], y, y, y, 1, 1, 1)
        SetHistProperties(hm_mass_1bin[x], y, y, y, 1, 1, 1)
        SetHistProperties(hm_mass_2bin[x], y, y, y, 1, 1, 1)
        SetHistProperties(hm_mass_3bin[x], y, y, y, 1, 1, 1)
        SetHistProperties(hm_mass_4bin[x], y, y, y, 1, 1, 1)    

    for x in range(len(jtypes_d)):
        hd_mass.append( fd.Get("h_"+jtypes_d[x]+"_mass") )
        hd_mass_0bin.append( fd.Get("h_"+jtypes_d[x]+"_mass_0bin") )
        hd_mass_1bin.append( fd.Get("h_"+jtypes_d[x]+"_mass_1bin") )                       
        hd_mass_2bin.append( fd.Get("h_"+jtypes_d[x]+"_mass_2bin") )                       
        hd_mass_3bin.append( fd.Get("h_"+jtypes_d[x]+"_mass_3bin") )                       
        hd_mass_4bin.append( fd.Get("h_"+jtypes_d[x]+"_mass_4bin") )
        y = x+1
        SetHistProperties(hd_mass[x], y, y, y, 1, 1, 1)
        SetHistProperties(hd_mass_0bin[x], y, y, y, 1, 1, 1)
        SetHistProperties(hd_mass_1bin[x], y, y, y, 1, 1, 1)
        SetHistProperties(hd_mass_2bin[x], y, y, y, 1, 1, 1)
        SetHistProperties(hd_mass_3bin[x], y, y, y, 1, 1, 1)
        SetHistProperties(hd_mass_4bin[x], y, y, y, 1, 1, 1)

   
            
    c1 = ROOT.TCanvas("c1","c1",600,600)
    c1.cd()
    SetHistProperties( hm_mass[jtypesToI["ak5"]],2,2,2,1,1,3003 )
    SetHistProperties( hm_mass[jtypesToI["ak5g"]],4,4,4,1,1,1 )    
    SetHistProperties( hd_mass[jtypesToI["ak5"]],1,1,1,1,20,1 )
    scl = GetDataMCSclFactor( hd_mass[jtypesToI["ak5"]], hm_mass[jtypesToI["ak5"]] )
    hm_mass[jtypesToI["ak5g"]].Scale( scl )

    tmph = hm_mass[jtypesToI["ak5"]].Clone()
    SetHistProperties( tmph, 2,0,0,1,0,0 )
    print "sclfctr: ",str(scl)
    hm_mass[jtypesToI["ak5"]].SetMinimum(0)
    hm_mass[jtypesToI["ak5"]].Draw("e2")
    tmph.Draw("sames")    
    hm_mass[jtypesToI["ak5g"]].Draw("sames")
    hd_mass[jtypesToI["ak5"]].Draw("pe1x0sames")        
    c1.SaveAs( figdir+"/test.eps" )

    c2 = ROOT.TCanvas("c2","c2",1600,800)
    c2.Divide(3,2)
    c2.cd(1)
    hd_mass[jtypesToI['ak5pr']].Draw()
    hd_mass[jtypesToI['ak5tr']].Draw("sames")
    hd_mass[jtypesToI['ak5ft']].Draw("sames")
    hd_mass[jtypesToI['ak5']].Draw("sames")

    c2.cd(2)
    hd_mass_0bin[jtypesToI['ak5ft']].Draw()
    hd_mass_0bin[jtypesToI['ak5tr']].Draw("sames")
    hd_mass_0bin[jtypesToI['ak5pr']].Draw("sames")
    hd_mass_0bin[jtypesToI['ak5']].Draw("sames")

    c2.cd(3)
    hd_mass_1bin[jtypesToI['ak5ft']].Draw()
    hd_mass_1bin[jtypesToI['ak5tr']].Draw("sames")
    hd_mass_1bin[jtypesToI['ak5pr']].Draw("sames")
    hd_mass_1bin[jtypesToI['ak5']].Draw("sames")

    c2.cd(4)
    hd_mass_2bin[jtypesToI['ak5ft']].Draw()
    hd_mass_2bin[jtypesToI['ak5tr']].Draw("sames")
    hd_mass_2bin[jtypesToI['ak5pr']].Draw("sames")
    hd_mass_2bin[jtypesToI['ak5']].Draw("sames")

    c2.cd(5)
    hd_mass_3bin[jtypesToI['ak5ft']].Draw()
    hd_mass_3bin[jtypesToI['ak5tr']].Draw("sames")
    hd_mass_3bin[jtypesToI['ak5pr']].Draw("sames")
    hd_mass_3bin[jtypesToI['ak5']].Draw("sames")

    c2.cd(6)
    hd_mass_4bin[jtypesToI['ak5ft']].Draw()
    hd_mass_4bin[jtypesToI['ak5tr']].Draw("sames")
    hd_mass_4bin[jtypesToI['ak5pr']].Draw("sames")
    hd_mass_4bin[jtypesToI['ak5']].Draw("sames")

    c2.SaveAs(figdir+"/test0.eps")


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
    
    gROOT.ProcessLine('.L myutils.C++')
    from ROOT import myutils, TH1F
    
    fm = ROOT.TFile(mcname)
    fd = ROOT.TFile(dataname)
    
    print "files: ", mcname,", ", dataname
    
    ############################################################
    # S P E C I F I C   P L O T S
    ##### 
    hmrat_mass_ovAK5 = []
    hmrat_pt_ovAK5 = []    
    # profile, ratio of mass, vs pT
    pmrPt_mass_ovAK5 = []    
    # profile, ratio of pt, vs pT
    pmrPt_pt_ovAK5 = []    
    
    hdrat_mass_ovAK5 = []
    hdrat_pt_ovAK5 = []    
    pdrPt_mass_ovAK5 = []    
    pdrPt_pt_ovAK5 = []    

    for x in range(len(jtypes_m)):
        hmrat_mass_ovAK5.append( fm.Get("hrat_"+jtypes_m[x]+"_mass_ovAK5") ) 
        hmrat_pt_ovAK5.append( fm.Get("hrat_"+jtypes_m[x]+"_pt_ovAK5") ) 
        pmrPt_mass_ovAK5.append( fm.Get("prPt_mass"+jtypes_m[x]+"_ovAK5") ) 
        pmrPt_pt_ovAK5.append( fm.Get("prPt_pt"+jtypes_m[x]+"_ovAK5") ) 
        y = x+1
        SetHistProperties(hmrat_pt_ovAK5[x], y, y, y, 1, 1, 1)
        SetHistProperties(hmrat_mass_ovAK5[x], y, y, y, 1, 1, 1)
        SetHistProperties(pmrPt_mass_ovAK5[x], y, y, y, 1, 1, 1)
        SetHistProperties(pmrPt_pt_ovAK5[x], y, y, y, 1, 1, 1)

    for x in range(len(jtypes_d)):        
        hdrat_mass_ovAK5.append( fd.Get("hrat_"+jtypes_d[x]+"_mass_ovAK5") ) 
        hdrat_pt_ovAK5.append( fd.Get("hrat_"+jtypes_d[x]+"_pt_ovAK5") ) 
        pdrPt_mass_ovAK5.append( fd.Get("prPt_mass"+jtypes_d[x]+"_ovAK5") ) 
        pdrPt_pt_ovAK5.append( fd.Get("prPt_pt"+jtypes_d[x]+"_ovAK5") ) 
        y = x+1
        SetHistProperties(hdrat_pt_ovAK5[x], y, y, y, 1, 1, 1)
        SetHistProperties(hdrat_mass_ovAK5[x], y, y, y, 1, 1, 1)
        SetHistProperties(pdrPt_mass_ovAK5[x], y, y, y, 1, 1, 1)
        SetHistProperties(pdrPt_pt_ovAK5[x], y, y, y, 1, 1, 1)

    
    c1 = ROOT.TCanvas("c1","c1",1600,1200)
    c1.Divide(3,2)
    c1.cd(1)
    hmrat_mass_ovAK5[jtypesToI['ak5g']].Draw()
    hmrat_mass_ovAK5[jtypesToI['ak5ft']].Draw("sames")
    hmrat_mass_ovAK5[jtypesToI['ak5tr']].Draw("sames")
    hmrat_mass_ovAK5[jtypesToI['ak5pr']].Draw("sames")
    c1.cd(2)
    hmrat_pt_ovAK5[jtypesToI['ak5g']].Draw()
    hmrat_pt_ovAK5[jtypesToI['ak5ft']].Draw("sames")
    hmrat_pt_ovAK5[jtypesToI['ak5tr']].Draw("sames")
    hmrat_pt_ovAK5[jtypesToI['ak5pr']].Draw("sames")
    c1.cd(3)
    pmrPt_mass_ovAK5[jtypesToI['ak5g']].Draw()
    pmrPt_mass_ovAK5[jtypesToI['ak5ft']].Draw("sames")
    pmrPt_mass_ovAK5[jtypesToI['ak5tr']].Draw("sames")
    pmrPt_mass_ovAK5[jtypesToI['ak5pr']].Draw("sames")
    c1.cd(4)
    pmrPt_pt_ovAK5[jtypesToI['ak5g']].Draw()
    pmrPt_pt_ovAK5[jtypesToI['ak5ft']].Draw("sames")
    pmrPt_pt_ovAK5[jtypesToI['ak5tr']].Draw("sames")
    pmrPt_pt_ovAK5[jtypesToI['ak5pr']].Draw("sames")
    c1.cd(5)
    p1tmp = pmrPt_mass_ovAK5[jtypesToI['ak5g']].ProfileX()
    p1tmp.SetMinimum( 0.5 )
    p1tmp.SetMaximum( 1.25 )
    p1tmp.Draw()
    pmrPt_mass_ovAK5[jtypesToI['ak5ft']].ProfileX().Draw("sames")
    pmrPt_mass_ovAK5[jtypesToI['ak5tr']].ProfileX().Draw("sames")
    pmrPt_mass_ovAK5[jtypesToI['ak5pr']].ProfileX().Draw("sames")
    c1.cd(6)
    theutils = myutils()
    h1 = theutils.GetFitSlicesY( pmrPt_pt_ovAK5[jtypesToI['ak5g']], 1 )
    h1.GetYaxis().SetRangeUser(0.4,1.1)
    h1.Draw()
    h2a = theutils.GetFitSlicesY( pmrPt_pt_ovAK5[jtypesToI['ak5ft']], 1 )
    h2a.Draw("sames")
    h2 = theutils.GetFitSlicesY( pmrPt_pt_ovAK5[jtypesToI['ak5tr']], 1 )
    h2.Draw("sames")
    h3 = theutils.GetFitSlicesY( pmrPt_pt_ovAK5[jtypesToI['ak5pr']], 1 )
    h3.Draw("sames")
    c1.SaveAs(figdir+"/test2D.eps")

