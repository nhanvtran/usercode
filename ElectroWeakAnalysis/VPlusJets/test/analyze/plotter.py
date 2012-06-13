from ROOT import gROOT, gStyle, gSystem, TLatex, gPad
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

jtypes_mv3 = ["ak5","ak5tr","ak5ft","ak5pr","ak7","ak7tr","ak7ft","ak7pr","ak8","ak8tr","ak8ft","ak8pr","ca8","ca8pr","ca12ft","ca12mdft","ak5g","ak7g","ak8g","ca8g","ak7trg","ak7ftg","ak7prg"]
jtypetrans_mv3 = {"ak5":"AK5PF","ak5tr":"AK5TRIMMEDPF","ak5ft":"AK5FILTEREDPF","ak5pr":"AK5PRUNEDPF",
    "ak7":"AK7PF","ak7tr":"AK7TRIMMEDPF","ak7ft":"AK7FILTEREDPF","ak7pr":"AK7PRUNEDPF",
    "ak8":"AK8PF","ak8tr":"AK8TRIMMEDPF","ak8ft":"AK8FILTEREDPF","ak8pr":"AK8PRUNEDPF",
    "ca8":"CA8PF","ca8pr":"CA8PRUNEDPF","ca12ft":"CA12FILTEREDPF","ca12mdft":"CA12MASSDROPFILTEREDPF",
    "ak5g":"AK5GENJETSNONU","ak7g":"AK7GENJETSNONU","ak8g":"AK8GENJETSNONU","ca8g":"CA8GENJETSNONU",
    "ak7trg":"AK7TRIMMEDGENPF","ak7ftg":"AK7FILTEREDGENPF","ak7prg":"AK7PRUNEDGENPF"} 
jtypesToI_mv3 = {"ak5":0,"ak5tr":1,"ak5ft":2,"ak5pr":3,
    "ak7":4,"ak7tr":5,"ak7ft":6,"ak7pr":7,
    "ak8":8,"ak8tr":9,"ak8ft":10,"ak8pr":11,
    "ca8":12,"ca8pr":13,"ca12ft":14,"ca12mdft":15,
    "ak5g":16,"ak7g":17,"ak8g":18,"ca8g":19,
    "ak7trg":20,"ak7ftg":21,"ak7prg":22}
    
jtypes_d = ["ak5","ak5tr","ak5ft","ak5pr","ak7","ak7tr","ak7ft","ak7pr","ak8","ak8tr","ak8ft","ak8pr","ca8","ca8pr","ca12ft","ca12mdft"]
jtypetrans_d = {"ak5":"AK5PF","ak5tr":"AK5TRIMMEDPF","ak5ft":"AK5FILTEREDPF","ak5pr":"AK5PRUNEDPF",
        "ak7":"AK7PF","ak7tr":"AK7TRIMMEDPF","ak7ft":"AK7FILTEREDPF","ak7pr":"AK7PRUNEDPF",
        "ak8":"AK8PF","ak8tr":"AK8TRIMMEDPF","ak8ft":"AK8FILTEREDPF","ak8pr":"AK8PRUNEDPF",
        "ca8":"CA8PF","ca8pr":"CA8PRUNEDPF","ca12ft":"CA12FILTEREDPF","ca12mdft":"CA12MASSDROPFILTEREDPF"} 
jtypesToI_d = {"ak5":0,"ak5tr":1,"ak5ft":2,"ak5pr":3,
        "ak7":4,"ak7tr":5,"ak7ft":6,"ak7pr":7,
        "ak8":8,"ak8tr":9,"ak8ft":10,"ak8pr":11,
        "ca8":12,"ca8pr":13,"ca12ft":14,"ca12mdft":15}
    
jtypes = []
jtypetrans = []
jtypesToI = []
jtypesToI = jtypesToI_m

gROOT.ProcessLine('.L myutils.C++')
from ROOT import myutils, TH1F
theutils = myutils()

suffix=".eps"
suffix2=".gif"
suffix3=".pdf"

cmap_m = {1:1,2:2,3:3,4:4,5:5,6:1,7:2,8:3,9:4,10:5,11:1,12:2,13:3,14:4,15:5,16:6,17:7,18:8,19:9,20:10}
cmap_mv3 = {1:1,2:2,3:3,4:4,5:1,6:2,7:3,8:4,9:1,10:2,11:3,12:4,13:6,14:7,15:2,16:4,17:5,18:5,19:5,20:5,21:2,22:3,23:4}
cmap_d = {1:1,2:2,3:3,4:4,5:1,6:2,7:3,8:4,9:1,10:2,11:3,12:4,13:5,14:6,15:2,16:4}


# Import everything from ROOT
import ROOT
from glob import glob
from array import array
    
ROOT.gStyle.SetPadLeftMargin(0.16);
ROOT.TH1.SetDefaultSumw2()

gSystem.Load('RooUnfold-1.1.1/libRooUnfold.so')
from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes


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
    print scl,":: mctotweight: ", mctotweight,", datatotweight: ", datatotweight
    return scl

def doUnfolding_closure( hResponse_input, hMeas_input, hTrue_input, canvasname ):

    hResponse = hResponse_input
    hTrue = hTrue_input
    hMeas = hMeas_input
    response = RooUnfoldResponse( hMeas, hTrue, hResponse, hResponse.GetName(), hResponse.GetTitle() )

#    print "hMeas integral: ", hMeas.Integral()

    unfold= RooUnfoldBayes     (response, hMeas, 4);    #  OR
    # unfold= RooUnfoldSvd     (response, hMeas, 20);   #  OR
    # unfold= RooUnfoldTUnfold (response, hMeas);

    hReco= unfold.Hreco();
    #unfold.PrintTable (cout, hTrue);

    SetHistProperties(hMeas, 4, 4, 0, 2, 0, 0)
    SetHistProperties(hTrue, 8, 8, 0, 1, 0, 0)
    SetHistProperties(hReco, 1, 1, 0, 1, 20, 0)
    
    lstack = ROOT.TLegend(0.6,0.6,0.9,0.8)
    lstack.SetFillColor(0)
    lstack.SetBorderSize(0)
    lstack.AddEntry( hMeas, "Raw", "l" )
    lstack.AddEntry( hTrue, "True", "l" )
    lstack.AddEntry( hReco, "Unfolded", "l" )
    
    txtbox = ROOT.TPaveText(0.6,0.85,0.9,0.9,"NDC")
    txtbox.SetFillColor(0)
    lstack.SetBorderSize(0)
    txtbox.AddText("closure test")
    
    can = ROOT.TCanvas("can","can",1200,600);
    can.Divide(2,1)
    can.cd(1)
    hMeas.Draw("HIST");
    hReco.Draw("SAME");
    hTrue.Draw("HISTSAME");
    lstack.Draw()
    can.cd(2)
    hMeas.Draw("HIST");
    hReco.Draw("SAME");
    hTrue.Draw("HISTSAME");
    txtbox.Draw()
    ROOT.gPad.SetLogy();
    can.SaveAs(canvasname+suffix);
    can.SaveAs(canvasname+suffix2);
    can.SaveAs(canvasname+suffix3);

def doUnfolding_data( hResponse_input, hMeas_input, hTrue_input, hData_input, canvasname ):
    
    hResponse = hResponse_input
    hTrue = hTrue_input
    hMeas = hMeas_input
    hData = hData_input
    response = RooUnfoldResponse( hMeas, hTrue, hResponse, hResponse.GetName(), hResponse.GetTitle() )
        
#    print "hMeas integral: ", hMeas.Integral()
    
    unfold= RooUnfoldBayes     (response, hData, 4);    #  OR
    # unfold= RooUnfoldSvd     (response, hMeas, 20);   #  OR
    # unfold= RooUnfoldTUnfold (response, hMeas);
    
    hReco= unfold.Hreco();
    #unfold.PrintTable (cout, hTrue);
    
    scl1 = GetDataMCSclFactor( hReco, hMeas )
    scl2 = GetDataMCSclFactor( hReco, hTrue )
    
    SetHistProperties(hMeas, 4, 4, 0, 2, 0, 0)
    SetHistProperties(hTrue, 8, 8, 0, 1, 0, 0)
    SetHistProperties(hReco, 1, 1, 0, 1, 20, 0)
    
    lstack = ROOT.TLegend(0.6,0.6,0.9,0.9)
    lstack.SetFillColor(0)
    lstack.SetBorderSize(0)
    lstack.AddEntry( hMeas, "MC", "l" )
    lstack.AddEntry( hTrue, "True", "l" )
    lstack.AddEntry( hReco, "Unfolded data", "l" )
    lstack.Draw()
    hMeas.SetTitle("; jet mass ;")
    
    can = ROOT.TCanvas("can","can",1200,600);
    can.Divide(2,1)
    can.cd(1)
    hMeas.Draw("HIST");
    hReco.Draw("SAME");
    hTrue.Draw("HISTSAME");
    lstack.Draw()
    can.cd(2)
    hMeas.Draw("HIST");
    hReco.Draw("SAME");
    hTrue.Draw("HISTSAME");
    ROOT.gPad.SetLogy();
    can.SaveAs(canvasname+suffix);
    can.SaveAs(canvasname+suffix2);
    can.SaveAs(canvasname+suffix3);

def doUnfolding_data_MCcomp( hResponse_input, hMeas_input, hTrue_input, hData_input, hmc1_Meas_input, hmc2_Meas_input, canvasname ):
    
    hResponse = hResponse_input
    hTrue = hTrue_input
    hMeas = hMeas_input
    hData = hData_input
    hMeas1 = hmc1_Meas_input
    hMeas2 = hmc2_Meas_input
    response = RooUnfoldResponse( hMeas, hTrue, hResponse, hResponse.GetName(), hResponse.GetTitle() )
    
    #    print "hMeas integral: ", hMeas.Integral()
    
    unfold= RooUnfoldBayes     (response, hData, 4);    #  OR
    unfold1= RooUnfoldBayes     (response, hMeas1, 4);    #  OR
    unfold2= RooUnfoldBayes     (response, hMeas2, 4);    #  OR

    # unfold= RooUnfoldSvd     (response, hMeas, 20);   #  OR
    # unfold= RooUnfoldTUnfold (response, hMeas);
    
    hReco= unfold.Hreco();
    hRecoMC1 = unfold1.Hreco();
    hRecoMC2 = unfold2.Hreco();
    #unfold.PrintTable (cout, hTrue);
    
    scl1 = GetDataMCSclFactor( hReco, hMeas )
    scl2 = GetDataMCSclFactor( hReco, hTrue )
    scl3 = GetDataMCSclFactor( hReco, hRecoMC1 )    
    scl4 = GetDataMCSclFactor( hReco, hRecoMC2 )
    
    SetHistProperties(hMeas, 2, 2, 0, 2, 0, 0)
    SetHistProperties(hTrue, 8, 8, 8, 1, 0, 3001)
    SetHistProperties(hReco, 1, 1, 0, 1, 20, 0)
    SetHistProperties(hRecoMC2, 4, 4, 0, 2, 0, 0)
    SetHistProperties(hRecoMC1, 2, 2, 2, 1, 0, 3001)

    tmp1 = hRecoMC1.Clone()
    SetHistProperties(tmp1, 2, 2, 0, 1, 0, 0)    
    
    lstack = ROOT.TLegend(0.6,0.6,0.9,0.9)
    lstack.SetFillColor(0)
    lstack.SetBorderSize(0)
    lstack.AddEntry( hRecoMC2, "Herwig", "l" )
    lstack.AddEntry( hRecoMC1, "Pythia", "l" )
    lstack.AddEntry( hReco, "Unfolded data", "l" )
    lstack.Draw()
    hMeas.SetTitle("; jet mass ;")
    
    if canvasname.find( "1bin" ) >= 0 or canvasname.find( "2bin" ) >= 0:
        hRecoMC1.GetXaxis().SetRangeUser( 0., 200. )
    
    if hRecoMC2.GetMaximum() > hRecoMC1.GetMaximum(): hRecoMC1.SetMaximum( hRecoMC2.GetMaximum()*1.1 )
    if hReco.GetMaximum() > hRecoMC1.GetMaximum(): hRecoMC1.SetMaximum( hReco.GetMaximum()*1.1 )
    
    can = ROOT.TCanvas("can","can",1200,600);
    can.Divide(2,1)
    can.cd(1)
    hRecoMC1.Draw("e2");
    tmp1.Draw("histsame");
    hRecoMC2.Draw("HISTSAME");
    hReco.Draw("SAME");
    lstack.Draw()
    can.cd(2)
    hRecoMC1.Draw("e2");
    tmp1.Draw("histsame");
    hRecoMC2.Draw("HISTSAME");
    hReco.Draw("SAME");
    ROOT.gPad.SetLogy();
    can.SaveAs(canvasname+suffix);
    can.SaveAs(canvasname+suffix2);
    can.SaveAs(canvasname+suffix3);

    canResponse = ROOT.TCanvas("canResponse","canResponse",800,800);
    hResponse.Draw("colz");
    canResponse.SaveAs(canvasname+"_response"+suffix);
    canResponse.SaveAs(canvasname+"_response"+suffix2);
    canResponse.SaveAs(canvasname+"_response"+suffix3);


############################################################
############################################################
############################################################
############################################################
############################################################
########## S T A C K / B A S I C   P L O T S
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
    
    hm_v_mt = fm.Get("h_v_mt_ak5") 
    print "entries: ",hm_v_mt.GetEntries()
    hm_v_mass = fm.Get("h_v_mass_ak5") 
    hm_v_pt = fm.Get("h_v_pt_ak5") 
    hm_e_met = fm.Get("h_e_met_ak5") 
    hm_l_pt = fm.Get("h_l_pt_ak5") 
    hm_l_eta = fm.Get("h_l_eta_ak5") 
    hm_lplus_pt = fm.Get("h_lplus_pt_ak5") 
    hm_lplus_eta = fm.Get("h_lplus_eta_ak5") 
    hm_e_nvert = fm.Get("h_e_nvert_ak5")
    hm_e_nvert_weighted = fm.Get("h_e_nvert_weighted_ak5")
    hm_e_PU = fm.Get("h_e_PU_ak5")
    hm_j_ak5_pt = fm.Get("h_ak5_pt")
    
    hd_v_mt = fd.Get("h_v_mt_ak5") 
    hd_v_mass = fd.Get("h_v_mass_ak5")     
    hd_v_pt = fd.Get("h_v_pt_ak5") 
    hd_e_met = fd.Get("h_e_met_ak5") 
    hd_l_pt = fd.Get("h_l_pt_ak5") 
    hd_l_eta = fd.Get("h_l_eta_ak5") 
    hd_lplus_pt = fd.Get("h_lplus_pt_ak5") 
    hd_lplus_eta = fd.Get("h_lplus_eta_ak5") 
    hd_e_nvert = fd.Get("h_e_nvert_ak5")
    hd_e_nvert_weighted = fd.Get("h_e_nvert_weighted_ak5")
    hd_e_PU = fd.Get("h_e_PU_ak5")
    hd_j_ak5_pt = fd.Get("h_ak5_pt")
    
    SetHistProperties( hm_v_mt,2,2,0,1,1,1 )
    SetHistProperties( hd_v_mt,1,1,0,1,20,1 )
    SetHistProperties( hm_v_mass,2,2,0,1,1,1 )
    SetHistProperties( hd_v_mass,1,1,0,1,20,1 )
    SetHistProperties( hm_v_pt,2,2,0,1,1,1 )
    SetHistProperties( hd_v_pt,1,1,0,1,20,1 )
    SetHistProperties( hm_e_met,2,2,0,1,1,1 )
    SetHistProperties( hd_e_met,1,1,0,1,20,1 )
    SetHistProperties( hm_l_pt,2,2,0,1,1,1 )
    SetHistProperties( hd_l_pt,1,1,0,1,20,1 )
    SetHistProperties( hm_l_eta,2,2,0,1,1,1 )
    SetHistProperties( hd_l_eta,1,1,0,1,20,1 )
    SetHistProperties( hm_lplus_pt,2,2,0,1,1,1 )
    SetHistProperties( hd_lplus_pt,1,1,0,1,20,1 )
    SetHistProperties( hm_lplus_eta,2,2,0,1,1,1 )
    SetHistProperties( hd_lplus_eta,1,1,0,1,20,1 )
    SetHistProperties( hd_e_nvert,1,1,0,1,20,1 )
    SetHistProperties( hm_e_nvert,2,2,0,1,1,1 )
    SetHistProperties( hm_e_nvert_weighted,4,4,0,1,1,1 )

    SetHistProperties( hm_e_PU,2,2,0,1,1,1 )
    SetHistProperties( hd_e_PU,1,1,0,1,20,1 )

    SetHistProperties( hm_j_ak5_pt,2,2,0,1,1,1 )
    SetHistProperties( hd_j_ak5_pt,1,1,0,1,20,1 )
    
    scl_v_mt = GetDataMCSclFactor( hd_v_mt, hm_v_mt )
    scl_v_mass = GetDataMCSclFactor( hd_v_mass, hm_v_mass )    
    scl_v_pt = GetDataMCSclFactor( hd_v_pt, hm_v_pt )
    scl_e_met = GetDataMCSclFactor( hd_e_met, hm_e_met )
    scl_l_pt = GetDataMCSclFactor( hd_l_pt, hm_l_pt )
    scl_l_eta = GetDataMCSclFactor( hd_l_eta, hm_l_eta )
    scl_lplus_pt = GetDataMCSclFactor( hd_lplus_pt, hm_lplus_pt )
    scl_lplus_eta = GetDataMCSclFactor( hd_lplus_eta, hm_lplus_eta )
    scl_e_dummy = GetDataMCSclFactor( hd_e_nvert, hm_e_nvert )
    scl_e_nvert = GetDataMCSclFactor( hd_e_nvert, hm_e_nvert_weighted )
    scl_j_ak5_pt = GetDataMCSclFactor( hd_j_ak5_pt, hm_j_ak5_pt )

    hms_v_mt = ROOT.THStack("hms_v_mt","; V mT;")
    hms_v_mass = ROOT.THStack("hms_v_mass","; V mass;")    
    hms_v_pt = ROOT.THStack("hms_v_pt","; V pT;")
    hms_e_met = ROOT.THStack("hms_e_met","; MET;")
    hms_l_pt = ROOT.THStack("hms_l_pt","; lepton pT;")
    hms_l_eta = ROOT.THStack("hms_l_eta","; lepton eta;")
    hms_lplus_pt = ROOT.THStack("hms_lplus_pt","; lbar pT;")
    hms_lplus_eta = ROOT.THStack("hms_lplus_eta","; lbar eta;")
    hms_e_nvert_weighted = ROOT.THStack("hms_e_nvert_weighted","; n vertices;")    
    hms_j_ak5_pt = ROOT.THStack("hms_j_ak5_pt","; ak5 jet pT;")    

    mcnamesLeg= ["WW,WZ,ZZ","W+jets","Z+jets","ttbar","single top"]
    lstack = ROOT.TLegend(0.6,0.6,0.9,0.9)
    lstack.SetFillColor(0)
    lstack.SetBorderSize(0)

    print mcnamesStack
    for x in range(len(mcnamesStack)):
        ft = ROOT.TFile(mcnamesStack[x]) 
        hs_v_mt =  ft.Get("h_v_mt_ak5") 
        hs_v_mass =  ft.Get("h_v_mass_ak5") 
        hs_v_pt = ft.Get("h_v_pt_ak5")
        hs_e_met = ft.Get("h_e_met_ak5")
        hs_l_pt = ft.Get("h_l_pt_ak5")
        hs_l_eta = ft.Get("h_l_eta_ak5")
        hs_lplus_pt = ft.Get("h_lplus_pt_ak5")
        hs_lplus_eta = ft.Get("h_lplus_eta_ak5")
        hs_e_nvert_weighted = ft.Get("h_e_nvert_weighted_ak5")
        hs_j_ak5_pt = ft.Get("h_ak5_pt")

        gROOT.cd()
        hs_v_mt_new = hs_v_mt.Clone()
        hs_v_mass_new = hs_v_mass.Clone()        
        hs_v_pt_new = hs_v_pt.Clone()
        hs_e_met_new = hs_e_met.Clone()
        hs_l_pt_new = hs_l_pt.Clone()
        hs_l_eta_new = hs_l_eta.Clone()
        hs_lplus_pt_new = hs_lplus_pt.Clone()
        hs_lplus_eta_new = hs_lplus_eta.Clone()
        hs_e_nvert_weighted_new = hs_e_nvert_weighted.Clone()
        hs_j_ak5_pt_new = hs_j_ak5_pt.Clone()

        hs_v_mt_new.Scale( scl_v_mt )
        hs_v_mass_new.Scale( scl_v_mass )        
        hs_v_pt_new.Scale( scl_v_pt )
        hs_e_met_new.Scale( scl_e_met )
        hs_l_pt_new.Scale( scl_l_pt )
        hs_l_eta_new.Scale( scl_l_eta )
        hs_lplus_pt_new.Scale( scl_lplus_pt )
        hs_lplus_eta_new.Scale( scl_lplus_eta )
        hs_e_nvert_weighted_new.Scale( scl_e_nvert )
        hs_j_ak5_pt_new.Scale( scl_j_ak5_pt )

        y=x+2
        SetHistProperties(hs_v_mt_new,y,y,y,1,1,1001)
        SetHistProperties(hs_v_mass_new,y,y,y,1,1,1001)        
        SetHistProperties(hs_v_pt_new,y,y,y,1,1,1001)
        SetHistProperties(hs_e_met_new,y,y,y,1,1,1001)
        SetHistProperties(hs_l_pt_new,y,y,y,1,1,1001)
        SetHistProperties(hs_l_eta_new,y,y,y,1,1,1001)
        SetHistProperties(hs_lplus_pt_new,y,y,y,1,1,1001)
        SetHistProperties(hs_lplus_eta_new,y,y,y,1,1,1001)
        SetHistProperties(hs_e_nvert_weighted_new,y,y,y,1,1,1001)
        SetHistProperties(hs_j_ak5_pt_new,y,y,y,1,1,1001)

        hms_v_mt.Add(hs_v_mt_new)
        hms_v_mass.Add(hs_v_mass_new)        
        hms_v_pt.Add(hs_v_pt_new)
        hms_e_met.Add(hs_e_met_new)
        hms_l_pt.Add(hs_l_pt_new)
        hms_l_eta.Add(hs_l_eta_new)
        hms_lplus_pt.Add(hs_lplus_pt_new)
        hms_lplus_eta.Add(hs_lplus_eta_new)        
        hms_e_nvert_weighted.Add(hs_e_nvert_weighted_new)
        hms_j_ak5_pt.Add(hs_j_ak5_pt_new)

        lstack.AddEntry(hs_v_mt_new,mcnamesLeg[x],"f")
    
    ln = ROOT.TLegend(0.6,0.6,0.9,0.9)
    ln.SetFillColor(0)
    ln.SetBorderSize(0)
    ln.AddEntry(hm_e_nvert,"MC","l")
    ln.AddEntry(hm_e_nvert_weighted,"MC reweighted","l")
    ln.AddEntry(hd_e_nvert,"data","p")
    cn = ROOT.TCanvas("cn","cn",800,800)
    hd_e_nvert.Draw("pe0")
    hm_e_nvert.Draw("histsames")
    hm_e_nvert_weighted.Draw("histsames")
    ln.Draw()
    cn.SaveAs(figdir+"/n_vertices"+suffix)
    cn.SaveAs(figdir+"/n_vertices"+suffix2)
    cn.SaveAs(figdir+"/n_vertices"+suffix3)

    cpu = ROOT.TCanvas("cpu","cpu",800,800)
#    ROOT.gStyle.SetOptStat("emr")
    hm_e_PU.SetStats( True )    
    hm_e_PU.GetXaxis().SetTitle("PU weights"); hm_e_PU.Draw("hist");
    cpu.SaveAs(figdir+"/e_PUwt"+suffix)
    cpu.SaveAs(figdir+"/e_PUwt"+suffix2)
    cpu.SaveAs(figdir+"/e_PUwt"+suffix3)

    divider=0
    if chan == 1 or chan == 2: divider=3
    if chan == 3 or chan == 4: divider=4 

    lkin = ROOT.TLegend(0.6,0.6,0.9,0.9)
    lkin.SetFillColor(0)
    lkin.SetBorderSize(0)
    lkin.AddEntry(hm_v_pt,"MC","l")
    lkin.AddEntry(hd_v_pt,"data","p")
    ckin = ROOT.TCanvas("ckin","ckin",1200,800)
    ckin.Divide(divider,2)
    ckin.cd(1)
    if chan == 1 or chan == 2:
        hm_v_mt.Draw("hist")
        hd_v_mt.Draw("pe0sames")
    if chan == 3 or chan == 4:
        hm_v_mass.Draw("hist")
        hd_v_mass.Draw("pe0sames")
    lkin.Draw()
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
    if chan == 3 or chan == 4:
        ckin.cd(7)
        hm_lplus_pt.Draw("hist")
        hd_lplus_pt.Draw("pe0sames")
        ckin.cd(8)
        hm_lplus_eta.Draw("hist")
        hd_lplus_eta.Draw("pe0sames")
    ckin.SaveAs(figdir+"/kinematics"+suffix)
    ckin.SaveAs(figdir+"/kinematics"+suffix2)
    ckin.SaveAs(figdir+"/kinematics"+suffix3)

    ckins = ROOT.TCanvas("ckins","ckins",1200,800)
    ckins.Divide(divider,2)
    ckins.cd(1)
    if chan == 1 or chan == 2:
        hms_v_mt.Draw("hist")
        hd_v_mt.Draw("pe0sames")
        if hms_v_mt.GetMaximum() < hd_v_mt.GetMaximum(): hms_v_mt.SetMaximum( 1.1*hd_v_mt.GetMaximum() )
    if chan == 3 or chan == 4:
        hms_v_mass.Draw("hist")
        hd_v_mass.Draw("pe0sames")
    ckins.cd(2)
    hms_v_pt.Draw("hist")
    hd_v_pt.Draw("pe0sames")
    if hms_v_pt.GetMaximum() < hd_v_pt.GetMaximum(): hms_v_pt.SetMaximum( 1.1*hd_v_pt.GetMaximum() )
    lstack.Draw()
    ckins.cd(3)
    hms_e_met.Draw("hist")
    hd_e_met.Draw("pe0sames")
    if hms_e_met.GetMaximum() < hd_e_met.GetMaximum(): hms_e_met.SetMaximum( 1.1*hd_e_met.GetMaximum() )
    ckins.cd(4)
    hms_l_pt.Draw("hist")
    hd_l_pt.Draw("pe0sames")
    if hms_l_pt.GetMaximum() < hd_l_pt.GetMaximum(): hms_l_pt.SetMaximum( 1.1*hd_l_pt.GetMaximum() )
    ckins.cd(5)
    hms_l_eta.Draw("hist")
    hd_l_eta.Draw("pe0sames")
    if hms_l_eta.GetMaximum() < hd_l_eta.GetMaximum(): hms_l_eta.SetMaximum( 1.1*hd_l_eta.GetMaximum() )
    ckins.cd(6)
    hms_j_ak5_pt.Draw("hist")
    hd_j_ak5_pt.Draw("pe0sames")
#    hms_e_nvert_weighted.Draw("hist")
#    hd_e_nvert.Draw("pe0sames")
#    if hms_e_nvert_weighted.GetMaximum() < hd_e_nvert.GetMaximum(): hms_e_nvert_weighted.SetMaximum( 1.1*hd_e_nvert.GetMaximum() )
    if chan == 3 or chan == 4:
        ckins.cd(7)
        hms_lplus_pt.Draw("hist")
        hd_lplus_pt.Draw("pe0sames")
        ckins.cd(8)
        hms_lplus_eta.Draw("hist")
        hd_lplus_eta.Draw("pe0sames")
    ckins.SaveAs(figdir+"/kinematics_stack"+suffix)
    ckins.SaveAs(figdir+"/kinematics_stack"+suffix2)
    ckins.SaveAs(figdir+"/kinematics_stack"+suffix3)

############################################################
############################################################
############################################################
############################################################
############################################################
########## S T A C K  P L O T S   F O R   T A G G E R S
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
def plotterStack_taggers(mcnamesStack, mcname,dataname,figdir, chan):
    
    fm = ROOT.TFile(mcname)
    fd = ROOT.TFile(dataname)
    
    print "stack files: ", mcname,", ", dataname
    
    hm_ca12ft_mass_Wtagged = fm.Get("h_ca12ft_mass_Wtagged") 
    hm_ca12ft_mass_toptagged = fm.Get("h_ca12ft_mass_toptagged") 
    hm_ca8pr_mass_Wtagged = fm.Get("h_ca8pr_mass_Wtagged") 
    hm_ca8pr_massdrop = fm.Get("h_ca8pr_massdrop") 

    hd_ca12ft_mass_Wtagged = fd.Get("h_ca12ft_mass_Wtagged") 
    hd_ca12ft_mass_toptagged = fd.Get("h_ca12ft_mass_toptagged")     
    hd_ca8pr_mass_Wtagged = fd.Get("h_ca8pr_mass_Wtagged") 
    hd_ca8pr_massdrop = fd.Get("h_ca8pr_massdrop") 
    
    SetHistProperties( hm_ca12ft_mass_Wtagged,2,2,0,1,1,1 )
    SetHistProperties( hd_ca12ft_mass_Wtagged,1,1,0,1,20,1 )
    SetHistProperties( hm_ca12ft_mass_toptagged,2,2,0,1,1,1 )
    SetHistProperties( hd_ca12ft_mass_toptagged,1,1,0,1,20,1 )
    SetHistProperties( hm_ca8pr_mass_Wtagged,2,2,0,1,1,1 )
    SetHistProperties( hd_ca8pr_mass_Wtagged,1,1,0,1,20,1 )
    SetHistProperties( hm_ca8pr_massdrop,2,2,0,1,1,1 )
    SetHistProperties( hd_ca8pr_massdrop,1,1,0,1,20,1 )
    
    scl_ca12ft_mass_Wtagged = GetDataMCSclFactor( hd_ca12ft_mass_Wtagged, hm_ca12ft_mass_Wtagged )
    scl_ca12ft_mass_toptagged = GetDataMCSclFactor( hd_ca12ft_mass_toptagged, hm_ca12ft_mass_toptagged )    
#
#    scl_ca8pr_mass_Wtagged = GetDataMCSclFactor( hd_ca8pr_mass_Wtagged, hm_ca8pr_mass_Wtagged )
    scl_ca8pr_mass_Wtagged = 1
#    
    scl_ca8pr_massdrop = GetDataMCSclFactor( hd_ca8pr_massdrop, hm_ca8pr_massdrop )
    
    hms_ca12ft_mass_Wtagged = ROOT.THStack("hms_ca12ft_mass_Wtagged","; ca12ft jet mass (W-tagged);")
    hms_ca12ft_mass_toptagged = ROOT.THStack("hms_ca12ft_mass_toptagged","; ca12ft jet mass (top-tagged);")    
    hms_ca8pr_mass_Wtagged = ROOT.THStack("hms_ca8pr_mass_Wtagged","; ca8pr jet mass;")
    hms_ca8pr_massdrop = ROOT.THStack("hms_ca8pr_massdrop","; mass drop;")
    
    mcnamesLeg= ["WW,WZ,ZZ","W+jets","Z+jets","ttbar","single top"]
    lstack = ROOT.TLegend(0.65,0.6,0.85,0.9)
    lstack.SetFillColor(0)
    lstack.SetBorderSize(0)
    
    print mcnamesStack
    for x in range(len(mcnamesStack)):
        ft = ROOT.TFile(mcnamesStack[x]) 
        hs_ca12ft_mass_Wtagged =  ft.Get("h_ca12ft_mass_Wtagged") 
        hs_ca12ft_mass_toptagged =  ft.Get("h_ca12ft_mass_toptagged") 
        hs_ca8pr_mass_Wtagged = ft.Get("h_ca8pr_mass_Wtagged")
        hs_ca8pr_massdrop = ft.Get("h_ca8pr_massdrop")
        gROOT.cd()
        hs_ca12ft_mass_Wtagged_new = hs_ca12ft_mass_Wtagged.Clone()
        hs_ca12ft_mass_toptagged_new = hs_ca12ft_mass_toptagged.Clone()        
        hs_ca8pr_mass_Wtagged_new = hs_ca8pr_mass_Wtagged.Clone()
        hs_ca8pr_massdrop_new = hs_ca8pr_massdrop.Clone()
             
        hs_ca12ft_mass_Wtagged_new.Scale( scl_ca12ft_mass_Wtagged )
        hs_ca12ft_mass_toptagged_new.Scale( scl_ca12ft_mass_toptagged )        
        hs_ca8pr_mass_Wtagged_new.Scale( scl_ca8pr_mass_Wtagged )
        hs_ca8pr_massdrop_new.Scale( scl_ca8pr_massdrop )
         
        y=x+2
        SetHistProperties(hs_ca12ft_mass_Wtagged_new,y,y,y,1,1,1001)
        SetHistProperties(hs_ca12ft_mass_toptagged_new,y,y,y,1,1,1001)        
        SetHistProperties(hs_ca8pr_mass_Wtagged_new,y,y,y,1,1,1001)
        SetHistProperties(hs_ca8pr_massdrop_new,y,y,y,1,1,1001)
        
        hms_ca12ft_mass_Wtagged.Add(hs_ca12ft_mass_Wtagged_new)
        hms_ca12ft_mass_toptagged.Add(hs_ca12ft_mass_toptagged_new)        
        hms_ca8pr_mass_Wtagged.Add(hs_ca8pr_mass_Wtagged_new)
        hms_ca8pr_massdrop.Add(hs_ca8pr_massdrop_new)
        
        lstack.AddEntry(hs_ca12ft_mass_Wtagged_new,mcnamesLeg[x],"f")
    
    c_ca12ft_Wtagged = ROOT.TCanvas("c_ca12ft_Wtagged","c_ca12ft_Wtagged",800,800)
    hms_ca12ft_mass_Wtagged.Draw("hist")
    hd_ca12ft_mass_Wtagged.Draw("pe0sames")
    lstack.Draw()
    c_ca12ft_Wtagged.SaveAs(figdir+"/ca12ft_Wtagged_jetmass"+suffix)
    c_ca12ft_Wtagged.SaveAs(figdir+"/ca12ft_Wtagged_jetmass"+suffix2)
    c_ca12ft_Wtagged.SaveAs(figdir+"/ca12ft_Wtagged_jetmass"+suffix3)

    c_ca12ft_toptagged = ROOT.TCanvas("c_ca12ft_toptagged","c_ca12ft_toptagged",800,800)
    hms_ca12ft_mass_toptagged.Draw("hist")
    hd_ca12ft_mass_toptagged.Draw("pe0sames")
    lstack.Draw()
    c_ca12ft_toptagged.SaveAs(figdir+"/ca12ft_toptagged_jetmass"+suffix)
    c_ca12ft_toptagged.SaveAs(figdir+"/ca12ft_toptagged_jetmass"+suffix2)
    c_ca12ft_toptagged.SaveAs(figdir+"/ca12ft_toptagged_jetmass"+suffix3)

    c_ca8pr_Wtagged = ROOT.TCanvas("c_ca8pr_Wtagged","c_ca8pr_Wtagged",800,800)
    hms_ca8pr_mass_Wtagged.Draw("hist")
    hd_ca8pr_mass_Wtagged.Draw("pe0sames")
    lstack.Draw()
    c_ca8pr_Wtagged.SaveAs(figdir+"/ca8pr_Wtagged_jetmass"+suffix)
    c_ca8pr_Wtagged.SaveAs(figdir+"/ca8pr_Wtagged_jetmass"+suffix2)
    c_ca8pr_Wtagged.SaveAs(figdir+"/ca8pr_Wtagged_jetmass"+suffix3)

    c_ca8pr_massdrop = ROOT.TCanvas("c_ca8pr_massdrop","c_ca8pr_massdrop",800,800)
    hms_ca8pr_massdrop.Draw("hist")
    hd_ca8pr_massdrop.Draw("pe0sames")
    lstack.Draw()
    c_ca8pr_massdrop.SaveAs(figdir+"/ca8pr_massdrop"+suffix)
    c_ca8pr_massdrop.SaveAs(figdir+"/ca8pr_massdrop"+suffix2)
    c_ca8pr_massdrop.SaveAs(figdir+"/ca8pr_massdrop"+suffix3)

############################################################
############################################################
############################################################
############################################################
############################################################
########## 1 D   P L O T S
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
        SetHistProperties(hm_mass[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
        SetHistProperties(hm_mass_0bin[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
        SetHistProperties(hm_mass_1bin[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
        SetHistProperties(hm_mass_2bin[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
        SetHistProperties(hm_mass_3bin[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
        SetHistProperties(hm_mass_4bin[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)    
        hm_mass_1bin[x].SetTitle("; jet mass (pT: 125-200 GeV);")
        hm_mass_2bin[x].SetTitle("; jet mass (pT: 200-300 GeV);")
        hm_mass_3bin[x].SetTitle("; jet mass (pT: 300-400 GeV);")
        hm_mass_4bin[x].SetTitle("; jet mass (pT: 400-500 GeV);")

    for x in range(len(jtypes_d)):
        hd_mass.append( fd.Get("h_"+jtypes_d[x]+"_mass") )
        hd_mass_0bin.append( fd.Get("h_"+jtypes_d[x]+"_mass_0bin") )
        hd_mass_1bin.append( fd.Get("h_"+jtypes_d[x]+"_mass_1bin") )                       
        hd_mass_2bin.append( fd.Get("h_"+jtypes_d[x]+"_mass_2bin") )                       
        hd_mass_3bin.append( fd.Get("h_"+jtypes_d[x]+"_mass_3bin") )                       
        hd_mass_4bin.append( fd.Get("h_"+jtypes_d[x]+"_mass_4bin") )
        y = x+1
        SetHistProperties(hd_mass[x], cmap_d[y],cmap_d[y],0, 1, 1, 1)
        SetHistProperties(hd_mass_0bin[x], cmap_d[y],cmap_d[y],0, 1, 1, 1)
        SetHistProperties(hd_mass_1bin[x], cmap_d[y],cmap_d[y],0, 1, 1, 1)
        SetHistProperties(hd_mass_2bin[x], cmap_d[y],cmap_d[y],0, 1, 1, 1)
        SetHistProperties(hd_mass_3bin[x], cmap_d[y],cmap_d[y],0, 1, 1, 1)
        SetHistProperties(hd_mass_4bin[x], cmap_d[y],cmap_d[y],0, 1, 1, 1)
        hd_mass_1bin[x].SetTitle("; jet mass (pT: 125-200 GeV);")
        hd_mass_2bin[x].SetTitle("; jet mass (pT: 200-300 GeV);")
        hd_mass_3bin[x].SetTitle("; jet mass (pT: 300-400 GeV);")
        hd_mass_4bin[x].SetTitle("; jet mass (pT: 400-500 GeV);")


#    c1 = ROOT.TCanvas("c1","c1",600,600)
#    c1.cd()
#    SetHistProperties( hm_mass[jtypesToI_m["ak5"]],2,2,2,1,1,3003 )
#    SetHistProperties( hm_mass[jtypesToI_m["ak5g"]],4,4,4,1,1,1 )    
#    SetHistProperties( hd_mass[jtypesToI_d["ak5"]],1,1,1,1,20,1 )
#    scl = GetDataMCSclFactor( hd_mass[jtypesToI_d["ak5"]], hm_mass[jtypesToI_m["ak5"]] )
#    hm_mass[jtypesToI_m["ak5g"]].Scale( scl )
#
#    tmph = hm_mass[jtypesToI_m["ak5"]].Clone()
#    SetHistProperties( tmph, 2,0,0,1,0,0 )
#    print "sclfctr: ",str(scl)
#    hm_mass[jtypesToI_m["ak5"]].SetMinimum(0)
#    hm_mass[jtypesToI_m["ak5"]].Draw("e2")
#    tmph.Draw("sames")    
#    hm_mass[jtypesToI_m["ak5g"]].Draw("sames")
#    hd_mass[jtypesToI_d["ak5"]].Draw("pe1x0sames")        
#    c1.SaveAs( figdir+"/test"+suffix )
#    c1.SaveAs( figdir+"/test"+suffix2 )
#    c1.SaveAs( figdir+"/test"+suffix3 )
#
#    c17 = ROOT.TCanvas("c17","c17",600,600)
#    c17.cd()
#    SetHistProperties( hm_mass[jtypesToI_m["ak7"]],2,2,2,1,1,3003 )
#    SetHistProperties( hm_mass[jtypesToI_m["ak7g"]],4,4,4,1,1,1 )    
#    SetHistProperties( hd_mass[jtypesToI_d["ak7"]],1,1,1,1,20,1 )
#    scl = GetDataMCSclFactor( hd_mass[jtypesToI_d["ak7"]], hm_mass[jtypesToI_m["ak7"]] )
#    hm_mass[jtypesToI_m["ak7g"]].Scale( scl )
#
#    tmph = hm_mass[jtypesToI_m["ak7"]].Clone()
#    SetHistProperties( tmph, 2,0,0,1,0,0 )
#    print "sclfctr: ",str(scl)
#    hm_mass[jtypesToI_m["ak7"]].SetMinimum(0)
#    hm_mass[jtypesToI_m["ak7"]].Draw("e2")
#    tmph.Draw("sames")    
#    hm_mass[jtypesToI_m["ak7g"]].Draw("sames")
#    hd_mass[jtypesToI_d["ak7"]].Draw("pe1x0sames")        
#    c17.SaveAs( figdir+"/test_ak7"+suffix )
#    c17.SaveAs( figdir+"/test_ak7"+suffix2 )
#    c17.SaveAs( figdir+"/test_ak7"+suffix3 )
#
#    c18 = ROOT.TCanvas("c18","c18",600,600)
#    c18.cd()
#    SetHistProperties( hm_mass[jtypesToI_m["ak8"]],2,2,2,1,1,3003 )
#    SetHistProperties( hm_mass[jtypesToI_m["ak8g"]],4,4,4,1,1,1 )    
#    SetHistProperties( hd_mass[jtypesToI_d["ak8"]],1,1,1,1,20,1 )
#    scl = GetDataMCSclFactor( hd_mass[jtypesToI_d["ak8"]], hm_mass[jtypesToI_m["ak8"]] )
#    hm_mass[jtypesToI_m["ak8g"]].Scale( scl )
#
#    tmph = hm_mass[jtypesToI_m["ak8"]].Clone()
#    SetHistProperties( tmph, 2,0,0,1,0,0 )
#    print "sclfctr: ",str(scl)
#    hm_mass[jtypesToI_m["ak8"]].SetMinimum(0)
#    hm_mass[jtypesToI_m["ak8"]].Draw("e2")
#    tmph.Draw("sames")    
#    hm_mass[jtypesToI_m["ak8g"]].Draw("sames")
#    hd_mass[jtypesToI_d["ak8"]].Draw("pe1x0sames")        
#    c18.SaveAs( figdir+"/test_ak8"+suffix )
#    c18.SaveAs( figdir+"/test_ak8"+suffix2 )
#    c18.SaveAs( figdir+"/test_ak8"+suffix3 )
#
#    # simple comparisons
#    for x in range(len(jtypes_d)):
#        ctmp = ROOT.TCanvas("ctmp","ctmp",600,600)
#        ctmp.cd()
#        SetHistProperties( hm_mass[jtypesToI_m[jtypes_d[x]]],2,2,2,1,1,3003 )
#        SetHistProperties( hd_mass[jtypesToI_d[jtypes_d[x]]],1,1,1,1,20,1 )
#        scl = GetDataMCSclFactor( hd_mass[jtypesToI_d[jtypes_d[x]]], hm_mass[jtypesToI_m[jtypes_d[x]]] )
#
#        tmph = hm_mass[jtypesToI_m[jtypes_d[x]]].Clone()
#        SetHistProperties( tmph, 2,0,0,1,0,0 )
#        hm_mass[jtypesToI_m[jtypes_d[x]]].SetMinimum(0)
#        
#        hm_mass[jtypesToI_m[jtypes_d[x]]].Draw("e2")
#        tmph.Draw("sames")    
#        hd_mass[jtypesToI_d[jtypes_d[x]]].Draw("pe1x0sames")        
#        
#        ctmp.SaveAs( figdir+"/jetmass_"+jtypes_d[x]+suffix )
#        ctmp.SaveAs( figdir+"/jetmass_"+jtypes_d[x]+suffix2 )
#        ctmp.SaveAs( figdir+"/jetmass_"+jtypes_d[x]+suffix3 )
#        
#        del ctmp
#        del tmph
    
    #################    #################    #################
    ## 2 x 2 plots fully compilated
    #################    #################    #################
    leg22 = ROOT.TLegend(0.50,0.6,0.95,0.9)
    leg22.SetFillColor(0)
    leg22.SetBorderSize(0)
    leg22.AddEntry( hd_mass_1bin[jtypesToI_d['ak5ft']], "Filtered", "l")
    leg22.AddEntry( hd_mass_1bin[jtypesToI_d['ak5tr']], "Trimmed", "l")
    leg22.AddEntry( hd_mass_1bin[jtypesToI_d['ak5pr']], "Pruned", "l")
    leg22.AddEntry( hd_mass_1bin[jtypesToI_d['ak5']], "Ungroomed", "l")

    c25 = ROOT.TCanvas("c25","c25",1600,1600)
    c25.Divide(2,2)

    c25.cd(1)
    hd_mass_1bin[jtypesToI_d['ak5ft']].GetXaxis().SetRangeUser(0.,200.)
    hd_mass_1bin[jtypesToI_d['ak5ft']].Draw("hist")
    hd_mass_1bin[jtypesToI_d['ak5tr']].Draw("histsames")
    hd_mass_1bin[jtypesToI_d['ak5pr']].Draw("histsames")
    hd_mass_1bin[jtypesToI_d['ak5']].Draw("histsames")
    leg22.Draw()

    c25.cd(2)
    hd_mass_2bin[jtypesToI_d['ak5ft']].GetXaxis().SetRangeUser(0.,200.)
    hd_mass_2bin[jtypesToI_d['ak5ft']].Draw("hist")
    hd_mass_2bin[jtypesToI_d['ak5tr']].Draw("histsames")
    hd_mass_2bin[jtypesToI_d['ak5pr']].Draw("histsames")
    hd_mass_2bin[jtypesToI_d['ak5']].Draw("histsames")

    c25.cd(3)
    hd_mass_3bin[jtypesToI_d['ak5ft']].Draw("hist")
    hd_mass_3bin[jtypesToI_d['ak5tr']].Draw("histsames")
    hd_mass_3bin[jtypesToI_d['ak5pr']].Draw("histsames")
    hd_mass_3bin[jtypesToI_d['ak5']].Draw("histsames")

    c25.cd(4)
    hd_mass_4bin[jtypesToI_d['ak5ft']].Draw("hist")
    hd_mass_4bin[jtypesToI_d['ak5tr']].Draw("histsames")
    hd_mass_4bin[jtypesToI_d['ak5pr']].Draw("histsames")
    hd_mass_4bin[jtypesToI_d['ak5']].Draw("histsames")

    c25.SaveAs(figdir+"/allAlgos_2x2PtBins_ak5"+suffix)
    c25.SaveAs(figdir+"/allAlgos_2x2PtBins_ak5"+suffix2)
    c25.SaveAs(figdir+"/allAlgos_2x2PtBins_ak5"+suffix3)

    #################

    c27 = ROOT.TCanvas("c27","c27",1600,1600)
    c27.Divide(2,2)

    c27.cd(1)
    hd_mass_1bin[jtypesToI_d['ak7ft']].GetXaxis().SetRangeUser(0.,200.)
    hd_mass_1bin[jtypesToI_d['ak7ft']].Draw("hist")
    hd_mass_1bin[jtypesToI_d['ak7tr']].Draw("histsames")
    hd_mass_1bin[jtypesToI_d['ak7pr']].Draw("histsames")
    hd_mass_1bin[jtypesToI_d['ak7']].Draw("histsames")
    leg22.Draw()

    c27.cd(2)
    hd_mass_2bin[jtypesToI_d['ak7ft']].GetXaxis().SetRangeUser(0.,200.)
    hd_mass_2bin[jtypesToI_d['ak7ft']].Draw("hist")
    hd_mass_2bin[jtypesToI_d['ak7tr']].Draw("histsames")
    hd_mass_2bin[jtypesToI_d['ak7pr']].Draw("histsames")
    hd_mass_2bin[jtypesToI_d['ak7']].Draw("histsames")

    c27.cd(3)
    hd_mass_3bin[jtypesToI_d['ak7ft']].Draw("hist")
    hd_mass_3bin[jtypesToI_d['ak7tr']].Draw("histsames")
    hd_mass_3bin[jtypesToI_d['ak7pr']].Draw("histsames")
    hd_mass_3bin[jtypesToI_d['ak7']].Draw("histsames")

    c27.cd(4)
    hd_mass_4bin[jtypesToI_d['ak7ft']].Draw("hist")
    hd_mass_4bin[jtypesToI_d['ak7tr']].Draw("histsames")
    hd_mass_4bin[jtypesToI_d['ak7pr']].Draw("histsames")
    hd_mass_4bin[jtypesToI_d['ak7']].Draw("histsames")

    c27.SaveAs(figdir+"/allAlgos_2x2PtBins_ak7"+suffix)
    c27.SaveAs(figdir+"/allAlgos_2x2PtBins_ak7"+suffix2)
    c27.SaveAs(figdir+"/allAlgos_2x2PtBins_ak7"+suffix3)

    #################
    
    c28 = ROOT.TCanvas("c28","c28",1600,1600)
    c28.Divide(2,2)
    
    c28.cd(1)
    hd_mass_1bin[jtypesToI_d['ak8ft']].GetXaxis().SetRangeUser(0.,200.)
    hd_mass_1bin[jtypesToI_d['ak8ft']].Draw("hist")
    hd_mass_1bin[jtypesToI_d['ak8tr']].Draw("histsames")
    hd_mass_1bin[jtypesToI_d['ak8pr']].Draw("histsames")
    hd_mass_1bin[jtypesToI_d['ak8']].Draw("histsames")
    leg22.Draw()

    c28.cd(2)
    hd_mass_2bin[jtypesToI_d['ak8ft']].GetXaxis().SetRangeUser(0.,200.)
    hd_mass_2bin[jtypesToI_d['ak8ft']].Draw("hist")
    hd_mass_2bin[jtypesToI_d['ak8tr']].Draw("histsames")
    hd_mass_2bin[jtypesToI_d['ak8pr']].Draw("histsames")
    hd_mass_2bin[jtypesToI_d['ak8']].Draw("histsames")
    
    c28.cd(3)
    hd_mass_3bin[jtypesToI_d['ak8ft']].Draw("hist")
    hd_mass_3bin[jtypesToI_d['ak8tr']].Draw("histsames")
    hd_mass_3bin[jtypesToI_d['ak8pr']].Draw("histsames")
    hd_mass_3bin[jtypesToI_d['ak8']].Draw("histsames")
    
    c28.cd(4)
    hd_mass_4bin[jtypesToI_d['ak8ft']].Draw("hist")
    hd_mass_4bin[jtypesToI_d['ak8tr']].Draw("histsames")
    hd_mass_4bin[jtypesToI_d['ak8pr']].Draw("histsames")
    hd_mass_4bin[jtypesToI_d['ak8']].Draw("histsames")
    
    c28.SaveAs(figdir+"/allAlgos_2x2PtBins_ak8"+suffix)
    c28.SaveAs(figdir+"/allAlgos_2x2PtBins_ak8"+suffix2)
    c28.SaveAs(figdir+"/allAlgos_2x2PtBins_ak8"+suffix3)


############################################################
############################################################
############################################################
############################################################
############################################################
########## 1 D   P L O T S :   M G   v s   H W 
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################

def plotter1D_MCcomp(mcname1,mcname2,dataname,figdir):
    
    fm1 = ROOT.TFile(mcname1)
    fm2 = ROOT.TFile(mcname2)  
    fd = ROOT.TFile(dataname)
        
    ############################################################
    # S P E C I F I C   P L O T S
    ##### 
    hm1_mass = []
    hm1_mass_0bin = []
    hm1_mass_1bin = []
    hm1_mass_2bin = []
    hm1_mass_3bin = []
    hm1_mass_4bin = []    
    hm2_mass = []
    hm2_mass_0bin = []
    hm2_mass_1bin = []
    hm2_mass_2bin = []
    hm2_mass_3bin = []
    hm2_mass_4bin = []    
    hd_mass = []
    hd_mass_0bin = []
    hd_mass_1bin = []
    hd_mass_2bin = []
    hd_mass_3bin = []
    hd_mass_4bin = []    
    
    for x in range(len(jtypes_m)):
        print jtypes_m[x]
        hm1_mass.append( fm1.Get("h_"+jtypes_m[x]+"_mass") )
        hm1_mass_0bin.append( fm1.Get("h_"+jtypes_m[x]+"_mass_0bin") )
        hm1_mass_1bin.append( fm1.Get("h_"+jtypes_m[x]+"_mass_1bin") )                       
        hm1_mass_2bin.append( fm1.Get("h_"+jtypes_m[x]+"_mass_2bin") )                       
        hm1_mass_3bin.append( fm1.Get("h_"+jtypes_m[x]+"_mass_3bin") )                       
        hm1_mass_4bin.append( fm1.Get("h_"+jtypes_m[x]+"_mass_4bin") )   
        y = x+1
        SetHistProperties(hm1_mass[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
        SetHistProperties(hm1_mass_0bin[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
        SetHistProperties(hm1_mass_1bin[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
        SetHistProperties(hm1_mass_2bin[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
        SetHistProperties(hm1_mass_3bin[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
        SetHistProperties(hm1_mass_4bin[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)    
        hm1_mass[x].SetTitle(";"+jtypes_m[x]+" jet mass;")
        hm1_mass_0bin[x].SetTitle(";"+jtypes_m[x]+" jet mass;")
        hm1_mass_1bin[x].SetTitle(";"+jtypes_m[x]+" jet mass (pT: 125-200 GeV);")
        hm1_mass_2bin[x].SetTitle(";"+jtypes_m[x]+" jet mass (pT: 200-300 GeV);")
        hm1_mass_3bin[x].SetTitle(";"+jtypes_m[x]+" jet mass (pT: 300-400 GeV);")
        hm1_mass_4bin[x].SetTitle(";"+jtypes_m[x]+" jet mass (pT: 400-500 GeV);")
        
        hm2_mass.append( fm2.Get("h_"+jtypes_m[x]+"_mass") )
        hm2_mass_0bin.append( fm2.Get("h_"+jtypes_m[x]+"_mass_0bin") )
        hm2_mass_1bin.append( fm2.Get("h_"+jtypes_m[x]+"_mass_1bin") )                       
        hm2_mass_2bin.append( fm2.Get("h_"+jtypes_m[x]+"_mass_2bin") )                       
        hm2_mass_3bin.append( fm2.Get("h_"+jtypes_m[x]+"_mass_3bin") )                       
        hm2_mass_4bin.append( fm2.Get("h_"+jtypes_m[x]+"_mass_4bin") )   
        SetHistProperties(hm2_mass[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
        SetHistProperties(hm2_mass_0bin[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
        SetHistProperties(hm2_mass_1bin[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
        SetHistProperties(hm2_mass_2bin[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
        SetHistProperties(hm2_mass_3bin[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
        SetHistProperties(hm2_mass_4bin[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)    
        hm2_mass[x].SetTitle(";"+jtypes_m[x]+" jet mass;")
        hm2_mass_0bin[x].SetTitle(";"+jtypes_m[x]+" jet mass;")
        hm2_mass_1bin[x].SetTitle(";"+jtypes_m[x]+" jet mass (pT: 125-200 GeV);")
        hm2_mass_2bin[x].SetTitle(";"+jtypes_m[x]+" jet mass (pT: 200-300 GeV);")
        hm2_mass_3bin[x].SetTitle(";"+jtypes_m[x]+" jet mass (pT: 300-400 GeV);")
        hm2_mass_4bin[x].SetTitle(";"+jtypes_m[x]+" jet mass (pT: 400-500 GeV);")
    
    for x in range(len(jtypes_d)):
        hd_mass.append( fd.Get("h_"+jtypes_d[x]+"_mass") )
        hd_mass_0bin.append( fd.Get("h_"+jtypes_d[x]+"_mass_0bin") )
        hd_mass_1bin.append( fd.Get("h_"+jtypes_d[x]+"_mass_1bin") )                       
        hd_mass_2bin.append( fd.Get("h_"+jtypes_d[x]+"_mass_2bin") )                       
        hd_mass_3bin.append( fd.Get("h_"+jtypes_d[x]+"_mass_3bin") )                       
        hd_mass_4bin.append( fd.Get("h_"+jtypes_d[x]+"_mass_4bin") )
        y = x+1
        SetHistProperties(hd_mass[x], cmap_d[y],cmap_d[y],0, 1, 1, 1)
        SetHistProperties(hd_mass_0bin[x], cmap_d[y],cmap_d[y],0, 1, 1, 1)
        SetHistProperties(hd_mass_1bin[x], cmap_d[y],cmap_d[y],0, 1, 1, 1)
        SetHistProperties(hd_mass_2bin[x], cmap_d[y],cmap_d[y],0, 1, 1, 1)
        SetHistProperties(hd_mass_3bin[x], cmap_d[y],cmap_d[y],0, 1, 1, 1)
        SetHistProperties(hd_mass_4bin[x], cmap_d[y],cmap_d[y],0, 1, 1, 1)
        hd_mass[x].SetTitle(";"+jtypes_d[x]+" jet mass;")
        hd_mass_0bin[x].SetTitle(";"+jtypes_d[x]+" jet mass;")
        hd_mass_1bin[x].SetTitle(";"+jtypes_d[x]+" jet mass (pT: 125-200 GeV);")
        hd_mass_2bin[x].SetTitle(";"+jtypes_d[x]+" jet mass (pT: 200-300 GeV);")
        hd_mass_3bin[x].SetTitle(";"+jtypes_d[x]+" jet mass (pT: 300-400 GeV);")
        hd_mass_4bin[x].SetTitle(";"+jtypes_d[x]+" jet mass (pT: 400-500 GeV);")
    
##############################################    
######### Plots for the purposes of unfolding, move elsewhere...
##############################################
#    c1 = ROOT.TCanvas("c1","c1",600,600)
#    c1.cd()
#    SetHistProperties( hm_mass[jtypesToI_m["ak5"]],2,2,2,1,1,3003 )
#    SetHistProperties( hm_mass[jtypesToI_m["ak5g"]],4,4,4,1,1,1 )    
#    SetHistProperties( hd_mass[jtypesToI_d["ak5"]],1,1,1,1,20,1 )
#    scl = GetDataMCSclFactor( hd_mass[jtypesToI_d["ak5"]], hm_mass[jtypesToI_m["ak5"]] )
#    hm_mass[jtypesToI_m["ak5g"]].Scale( scl )
#    
#    tmph = hm_mass[jtypesToI_m["ak5"]].Clone()
#    SetHistProperties( tmph, 2,0,0,1,0,0 )
#    print "sclfctr: ",str(scl)
#    hm_mass[jtypesToI_m["ak5"]].SetMinimum(0)
#    hm_mass[jtypesToI_m["ak5"]].Draw("e2")
#    tmph.Draw("sames")    
#    hm_mass[jtypesToI_m["ak5g"]].Draw("sames")
#    hd_mass[jtypesToI_d["ak5"]].Draw("pe1x0sames")        
#    c1.SaveAs( figdir+"/test"+suffix )
#    c1.SaveAs( figdir+"/test"+suffix2 )
#    c1.SaveAs( figdir+"/test"+suffix3 )
#    
#    c17 = ROOT.TCanvas("c17","c17",600,600)
#    c17.cd()
#    SetHistProperties( hm_mass[jtypesToI_m["ak7"]],2,2,2,1,1,3003 )
#    SetHistProperties( hm_mass[jtypesToI_m["ak7g"]],4,4,4,1,1,1 )    
#    SetHistProperties( hd_mass[jtypesToI_d["ak7"]],1,1,1,1,20,1 )
#    scl = GetDataMCSclFactor( hd_mass[jtypesToI_d["ak7"]], hm_mass[jtypesToI_m["ak7"]] )
#    hm_mass[jtypesToI_m["ak7g"]].Scale( scl )
#    
#    tmph = hm_mass[jtypesToI_m["ak7"]].Clone()
#    SetHistProperties( tmph, 2,0,0,1,0,0 )
#    print "sclfctr: ",str(scl)
#    hm_mass[jtypesToI_m["ak7"]].SetMinimum(0)
#    hm_mass[jtypesToI_m["ak7"]].Draw("e2")
#    tmph.Draw("sames")    
#    hm_mass[jtypesToI_m["ak7g"]].Draw("sames")
#    hd_mass[jtypesToI_d["ak7"]].Draw("pe1x0sames")        
#    c17.SaveAs( figdir+"/test_ak7"+suffix )
#    c17.SaveAs( figdir+"/test_ak7"+suffix2 )
#    c17.SaveAs( figdir+"/test_ak7"+suffix3 )
#    
#    c18 = ROOT.TCanvas("c18","c18",600,600)
#    c18.cd()
#    SetHistProperties( hm_mass[jtypesToI_m["ak8"]],2,2,2,1,1,3003 )
#    SetHistProperties( hm_mass[jtypesToI_m["ak8g"]],4,4,4,1,1,1 )    
#    SetHistProperties( hd_mass[jtypesToI_d["ak8"]],1,1,1,1,20,1 )
#    scl = GetDataMCSclFactor( hd_mass[jtypesToI_d["ak8"]], hm_mass[jtypesToI_m["ak8"]] )
#    hm_mass[jtypesToI_m["ak8g"]].Scale( scl )
#    
#    tmph = hm_mass[jtypesToI_m["ak8"]].Clone()
#    SetHistProperties( tmph, 2,0,0,1,0,0 )
#    print "sclfctr: ",str(scl)
#    hm_mass[jtypesToI_m["ak8"]].SetMinimum(0)
#    hm_mass[jtypesToI_m["ak8"]].Draw("e2")
#    tmph.Draw("sames")    
#    hm_mass[jtypesToI_m["ak8g"]].Draw("sames")
#    hd_mass[jtypesToI_d["ak8"]].Draw("pe1x0sames")        
#    c18.SaveAs( figdir+"/test_ak8"+suffix )
#    c18.SaveAs( figdir+"/test_ak8"+suffix2 )
#    c18.SaveAs( figdir+"/test_ak8"+suffix3 )
    
    # simple comparisons
    for x in range(len(jtypes_d)):
        
        ctmp = ROOT.TCanvas("ctmp","ctmp",1200,600)
        ctmp.Divide(2,1)
        SetHistProperties( hm1_mass[jtypesToI_m[jtypes_d[x]]],2,2,2,1,1,3001 )
        SetHistProperties( hm2_mass[jtypesToI_m[jtypes_d[x]]],4,4,4,1,1,3001 )
        SetHistProperties( hd_mass[jtypesToI_d[jtypes_d[x]]],1,1,1,1,20,1 )
        scl1 = GetDataMCSclFactor( hd_mass[jtypesToI_d[jtypes_d[x]]], hm1_mass[jtypesToI_m[jtypes_d[x]]] )
        scl2 = GetDataMCSclFactor( hd_mass[jtypesToI_d[jtypes_d[x]]], hm2_mass[jtypesToI_m[jtypes_d[x]]] )

        legTmp = ROOT.TLegend(0.50,0.6,0.95,0.9)
        legTmp.SetFillColor(0)
        legTmp.SetBorderSize(0)
        legTmp.AddEntry( hm1_mass[jtypesToI_m[jtypes_d[x]]], "Pythia, MC", "l")
        legTmp.AddEntry( hm2_mass[jtypesToI_m[jtypes_d[x]]], "Herwig, MC", "l")
        legTmp.AddEntry( hd_mass[jtypesToI_d[jtypes_d[x]]], "Data", "l")

        
        tmph1 = hm1_mass[jtypesToI_m[jtypes_d[x]]].Clone()
        SetHistProperties( tmph1, 2,0,0,1,0,0 )
        tmph2 = hm2_mass[jtypesToI_m[jtypes_d[x]]].Clone()
        SetHistProperties( tmph2, 4,0,0,1,0,0 )
        
        ctmp.cd(1)
        hm1_mass[jtypesToI_m[jtypes_d[x]]].SetMinimum(0)
        hm1_mass[jtypesToI_m[jtypes_d[x]]].Draw("e2")
        tmph1.Draw("histsames")    
        hm2_mass[jtypesToI_m[jtypes_d[x]]].Draw("e2sames")
        tmph2.Draw("histsames")    
        hd_mass[jtypesToI_d[jtypes_d[x]]].Draw("pe1x0sames")        
        legTmp.Draw()
        
        ctmp.cd(2)
        hm1_mass[jtypesToI_m[jtypes_d[x]]].SetMinimum(0.1)
        hm1_mass[jtypesToI_m[jtypes_d[x]]].Draw("e2")   
        tmph1.Draw("histsames")    
        hm2_mass[jtypesToI_m[jtypes_d[x]]].Draw("e2sames")
        tmph2.Draw("histsames")    
        hd_mass[jtypesToI_d[jtypes_d[x]]].Draw("pe1x0sames")        
        gPad.SetLogy()
        ctmp.Update()

        ctmp.SaveAs( figdir+"/jetmass_"+jtypes_d[x]+suffix )
        ctmp.SaveAs( figdir+"/jetmass_"+jtypes_d[x]+suffix2 )
        ctmp.SaveAs( figdir+"/jetmass_"+jtypes_d[x]+suffix3 )
        
        ## ----------------------
        
        ctmp_1bin = ROOT.TCanvas("ctmp_1bin","ctmp_1bin",1200,600)
        ctmp_1bin.Divide(2,1)
        SetHistProperties( hm1_mass_1bin[jtypesToI_m[jtypes_d[x]]],2,2,2,1,1,3001 )
        SetHistProperties( hm2_mass_1bin[jtypesToI_m[jtypes_d[x]]],4,4,4,1,1,3001 )
        SetHistProperties( hd_mass_1bin[jtypesToI_d[jtypes_d[x]]],1,1,1,1,20,1 )
        scl1 = GetDataMCSclFactor( hd_mass_1bin[jtypesToI_d[jtypes_d[x]]], hm1_mass_1bin[jtypesToI_m[jtypes_d[x]]] )
        scl2 = GetDataMCSclFactor( hd_mass_1bin[jtypesToI_d[jtypes_d[x]]], hm2_mass_1bin[jtypesToI_m[jtypes_d[x]]] )
        
        tmph1_1bin = hm1_mass_1bin[jtypesToI_m[jtypes_d[x]]].Clone()
        SetHistProperties( tmph1_1bin, 2,0,0,1,0,0 )
        tmph2_1bin = hm2_mass_1bin[jtypesToI_m[jtypes_d[x]]].Clone()
        SetHistProperties( tmph2_1bin, 4,0,0,1,0,0 )
        
        hm1_mass_1bin[jtypesToI_m[jtypes_d[x]]].SetMinimum(0)
        
        hm1_mass_1bin[jtypesToI_m[jtypes_d[x]]].GetXaxis().SetRangeUser(0.,200.)
        ctmp_1bin.cd(1)
        hm1_mass_1bin[jtypesToI_m[jtypes_d[x]]].Draw("e2")
        tmph1_1bin.Draw("histsames")    
        hm2_mass_1bin[jtypesToI_m[jtypes_d[x]]].Draw("e2sames")
        tmph2_1bin.Draw("histsames")    
        hd_mass_1bin[jtypesToI_d[jtypes_d[x]]].Draw("pe1x0sames")        
        legTmp.Draw()   
        ctmp_1bin.cd(2)
        hm1_mass_1bin[jtypesToI_m[jtypes_d[x]]].SetMinimum(0.1)
        hm1_mass_1bin[jtypesToI_m[jtypes_d[x]]].Draw("e2")
        tmph1_1bin.Draw("histsames")    
        hm2_mass_1bin[jtypesToI_m[jtypes_d[x]]].Draw("e2sames")
        tmph2_1bin.Draw("histsames")    
        hd_mass_1bin[jtypesToI_d[jtypes_d[x]]].Draw("pe1x0sames")        
        gPad.SetLogy()
        ctmp.Update()

        ctmp_1bin.SaveAs( figdir+"/jetmass_1bin_"+jtypes_d[x]+suffix )
        ctmp_1bin.SaveAs( figdir+"/jetmass_1bin_"+jtypes_d[x]+suffix2 )
        ctmp_1bin.SaveAs( figdir+"/jetmass_1bin_"+jtypes_d[x]+suffix3 )

        ## ----------------------
        
        ctmp_2bin = ROOT.TCanvas("ctmp_2bin","ctmp_2bin",1200,600)
        ctmp_2bin.Divide(2,1)
        SetHistProperties( hm1_mass_2bin[jtypesToI_m[jtypes_d[x]]],2,2,2,1,1,3001 )
        SetHistProperties( hm2_mass_2bin[jtypesToI_m[jtypes_d[x]]],4,4,4,1,1,3001 )
        SetHistProperties( hd_mass_2bin[jtypesToI_d[jtypes_d[x]]],1,1,1,1,20,1 )
        scl1 = GetDataMCSclFactor( hd_mass_2bin[jtypesToI_d[jtypes_d[x]]], hm1_mass_2bin[jtypesToI_m[jtypes_d[x]]] )
        scl2 = GetDataMCSclFactor( hd_mass_2bin[jtypesToI_d[jtypes_d[x]]], hm2_mass_2bin[jtypesToI_m[jtypes_d[x]]] )
        
        tmph1_2bin = hm1_mass_2bin[jtypesToI_m[jtypes_d[x]]].Clone()
        SetHistProperties( tmph1_2bin, 2,0,0,1,0,0 )
        tmph2_2bin = hm2_mass_2bin[jtypesToI_m[jtypes_d[x]]].Clone()
        SetHistProperties( tmph2_2bin, 4,0,0,1,0,0 )
        
        hm1_mass_2bin[jtypesToI_m[jtypes_d[x]]].SetMinimum(0)
        
        hm1_mass_2bin[jtypesToI_m[jtypes_d[x]]].GetXaxis().SetRangeUser(0.,200.)
        ctmp_2bin.cd(1)
        hm1_mass_2bin[jtypesToI_m[jtypes_d[x]]].Draw("e2")
        tmph1_2bin.Draw("histsames")    
        hm2_mass_2bin[jtypesToI_m[jtypes_d[x]]].Draw("e2sames")
        tmph2_2bin.Draw("histsames")    
        hd_mass_2bin[jtypesToI_d[jtypes_d[x]]].Draw("pe1x0sames")   
        legTmp.Draw()
        ctmp_2bin.cd(2)
        hm1_mass_2bin[jtypesToI_m[jtypes_d[x]]].SetMinimum(0.1)
        hm1_mass_2bin[jtypesToI_m[jtypes_d[x]]].Draw("e2")
        tmph1_2bin.Draw("histsames")    
        hm2_mass_2bin[jtypesToI_m[jtypes_d[x]]].Draw("e2sames")
        tmph2_2bin.Draw("histsames")    
        hd_mass_2bin[jtypesToI_d[jtypes_d[x]]].Draw("pe1x0sames")        
        gPad.SetLogy()
        ctmp.Update()

        
        ctmp_2bin.SaveAs( figdir+"/jetmass_2bin_"+jtypes_d[x]+suffix )
        ctmp_2bin.SaveAs( figdir+"/jetmass_2bin_"+jtypes_d[x]+suffix2 )
        ctmp_2bin.SaveAs( figdir+"/jetmass_2bin_"+jtypes_d[x]+suffix3 )

        ## ----------------------
        
        ctmp_3bin = ROOT.TCanvas("ctmp_3bin","ctmp_3bin",1200,600)
        ctmp_3bin.Divide(2,1)
        SetHistProperties( hm1_mass_3bin[jtypesToI_m[jtypes_d[x]]],2,2,2,1,1,3001 )
        SetHistProperties( hm2_mass_3bin[jtypesToI_m[jtypes_d[x]]],4,4,4,1,1,3001 )
        SetHistProperties( hd_mass_3bin[jtypesToI_d[jtypes_d[x]]],1,1,1,1,20,1 )
        scl1 = GetDataMCSclFactor( hd_mass_3bin[jtypesToI_d[jtypes_d[x]]], hm1_mass_3bin[jtypesToI_m[jtypes_d[x]]] )
        scl2 = GetDataMCSclFactor( hd_mass_3bin[jtypesToI_d[jtypes_d[x]]], hm2_mass_3bin[jtypesToI_m[jtypes_d[x]]] )
        
        tmph1_3bin = hm1_mass_3bin[jtypesToI_m[jtypes_d[x]]].Clone()
        SetHistProperties( tmph1_3bin, 2,0,0,1,0,0 )
        tmph2_3bin = hm2_mass_3bin[jtypesToI_m[jtypes_d[x]]].Clone()
        SetHistProperties( tmph2_3bin, 4,0,0,1,0,0 )
        
        hm1_mass_3bin[jtypesToI_m[jtypes_d[x]]].SetMinimum(0)
        
        ctmp_3bin.cd(1)        
        hm1_mass_3bin[jtypesToI_m[jtypes_d[x]]].Draw("e2")
        tmph1_3bin.Draw("histsames")    
        hm2_mass_3bin[jtypesToI_m[jtypes_d[x]]].Draw("e2sames")
        tmph2_3bin.Draw("histsames")    
        hd_mass_3bin[jtypesToI_d[jtypes_d[x]]].Draw("pe1x0sames")  
        legTmp.Draw()
        ctmp_3bin.cd(2)
        hm1_mass_3bin[jtypesToI_m[jtypes_d[x]]].SetMinimum(0.1)
        hm1_mass_3bin[jtypesToI_m[jtypes_d[x]]].Draw("e2")
        tmph1_3bin.Draw("histsames")    
        hm2_mass_3bin[jtypesToI_m[jtypes_d[x]]].Draw("e2sames")
        tmph2_3bin.Draw("histsames")    
        hd_mass_3bin[jtypesToI_d[jtypes_d[x]]].Draw("pe1x0sames")        
        gPad.SetLogy()
        ctmp.Update()

        ctmp_3bin.SaveAs( figdir+"/jetmass_3bin_"+jtypes_d[x]+suffix )
        ctmp_3bin.SaveAs( figdir+"/jetmass_3bin_"+jtypes_d[x]+suffix2 )
        ctmp_3bin.SaveAs( figdir+"/jetmass_3bin_"+jtypes_d[x]+suffix3 )

        ## ----------------------
        
        ctmp_4bin = ROOT.TCanvas("ctmp_4bin","ctmp_4bin",1200,600)
        ctmp_4bin.Divide(2,1)
        SetHistProperties( hm1_mass_4bin[jtypesToI_m[jtypes_d[x]]],2,2,2,1,1,3001 )
        SetHistProperties( hm2_mass_4bin[jtypesToI_m[jtypes_d[x]]],4,4,4,1,1,3001 )
        SetHistProperties( hd_mass_4bin[jtypesToI_d[jtypes_d[x]]],1,1,1,1,20,1 )
        scl1 = GetDataMCSclFactor( hd_mass_4bin[jtypesToI_d[jtypes_d[x]]], hm1_mass_4bin[jtypesToI_m[jtypes_d[x]]] )
        scl2 = GetDataMCSclFactor( hd_mass_4bin[jtypesToI_d[jtypes_d[x]]], hm2_mass_4bin[jtypesToI_m[jtypes_d[x]]] )
        
        tmph1_4bin = hm1_mass_4bin[jtypesToI_m[jtypes_d[x]]].Clone()
        SetHistProperties( tmph1_4bin, 2,0,0,1,0,0 )
        tmph2_4bin = hm2_mass_4bin[jtypesToI_m[jtypes_d[x]]].Clone()
        SetHistProperties( tmph2_4bin, 4,0,0,1,0,0 )
        
        hm1_mass_4bin[jtypesToI_m[jtypes_d[x]]].SetMinimum(0)
        
        ctmp_4bin.cd(1)
        hm1_mass_4bin[jtypesToI_m[jtypes_d[x]]].Draw("e2")
        tmph1_4bin.Draw("histsames")    
        hm2_mass_4bin[jtypesToI_m[jtypes_d[x]]].Draw("e2sames")
        tmph2_4bin.Draw("histsames")    
        hd_mass_4bin[jtypesToI_d[jtypes_d[x]]].Draw("pe1x0sames")
        legTmp.Draw()
        ctmp_4bin.cd(2)
        hm1_mass_4bin[jtypesToI_m[jtypes_d[x]]].SetMinimum(0.1)
        hm1_mass_4bin[jtypesToI_m[jtypes_d[x]]].Draw("e2")
        tmph1_4bin.Draw("histsames")    
        hm2_mass_4bin[jtypesToI_m[jtypes_d[x]]].Draw("e2sames")
        tmph2_4bin.Draw("histsames")    
        hd_mass_4bin[jtypesToI_d[jtypes_d[x]]].Draw("pe1x0sames")        
        gPad.SetLogy()
        ctmp.Update()
        
        ctmp_4bin.SaveAs( figdir+"/jetmass_4bin_"+jtypes_d[x]+suffix )
        ctmp_4bin.SaveAs( figdir+"/jetmass_4bin_"+jtypes_d[x]+suffix2 )
        ctmp_4bin.SaveAs( figdir+"/jetmass_4bin_"+jtypes_d[x]+suffix3 )

        del ctmp
        del tmph1; del tmph2;
        del ctmp_1bin
        del tmph1_1bin; del tmph2_1bin;
        del ctmp_2bin
        del tmph1_2bin; del tmph2_2bin;
        del ctmp_3bin
        del tmph1_3bin; del tmph2_3bin;
        del ctmp_4bin
        del tmph1_4bin; del tmph2_4bin;
        del legTmp

############################################################
############################################################
############################################################
############################################################
############################################################
########## 2 D   V A L I D A T I O N   P L O T S 
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
        SetHistProperties(hmrat_pt_ovAK5[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
        SetHistProperties(hmrat_mass_ovAK5[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
        SetHistProperties(hmrat_pt_ovAK5g[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
        SetHistProperties(hmrat_mass_ovAK5g[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
        SetHistProperties(hmrat_pt_ovAK7[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
        SetHistProperties(hmrat_mass_ovAK7[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
        SetHistProperties(hmrat_pt_ovAK7g[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
        SetHistProperties(hmrat_mass_ovAK7g[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
        SetHistProperties(hmrat_pt_ovAK8[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
        SetHistProperties(hmrat_mass_ovAK8[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
        SetHistProperties(hmrat_pt_ovAK8g[x], cmap_m[y],cmap_m[y],0, 1, 1, 1)
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

        pmrPt_pt_ovAK5[x].SetTitle("; (ak5) reco pT; pT reco - pT ak5 gen;")
        pmrPt_pt_ovAK5g[x].SetTitle("; (ak5) reco pT; pT reco - pT ak5 gen;")
        pmrPt_pt_ovAK7[x].SetTitle("; (ak7) reco pT; pT reco - pT ak7 gen;")
        pmrPt_pt_ovAK7g[x].SetTitle("; (ak7) reco pT; pT reco - pT ak7 gen;")
        pmrPt_pt_ovAK8[x].SetTitle("; (ak8) reco pT; pT reco - pT ak8 gen;")
        pmrPt_pt_ovAK8g[x].SetTitle("; (ak8) reco pT; pT reco - pT ak8 gen;")
        pmrNV_pt_ovAK5[x].SetTitle("; (ak5) nVertices; pT reco - pT ak5 gen;")
        pmrNV_pt_ovAK5g[x].SetTitle("; (ak5) nVertices; pT reco - pT ak5 gen;")
        pmrNV_pt_ovAK7[x].SetTitle("; (ak7) nVertices; pT reco - pT ak7 gen;")
        pmrNV_pt_ovAK7g[x].SetTitle("; (ak7) nVertices; pT reco - pT ak7 gen;")
        pmrNV_pt_ovAK8[x].SetTitle("; (ak8) nVertices; pT reco - pT ak8 gen;")
        pmrNV_pt_ovAK8g[x].SetTitle("; (ak8) nVertices; pT reco - pT ak8 gen;")
        pmrEta_pt_ovAK5[x].SetTitle("; (ak5) reco eta; pT reco - pT ak5 gen;")
        pmrEta_pt_ovAK5g[x].SetTitle("; (ak5) reco eta; pT reco - pT ak5 gen;")
        pmrEta_pt_ovAK7[x].SetTitle("; (ak7) reco eta; pT reco - pT ak7 gen;")
        pmrEta_pt_ovAK7g[x].SetTitle("; (ak7) reco eta; pT reco - pT ak7 gen;")
        pmrEta_pt_ovAK8[x].SetTitle("; (ak8) reco eta; pT reco - pT ak8 gen;")
        pmrEta_pt_ovAK8g[x].SetTitle("; (ak8) reco eta; pT reco - pT ak8 gen;")
        
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

    leg22 = ROOT.TLegend(0.50,0.6,0.95,0.9)
    leg22.SetFillColor(0)
    leg22.SetBorderSize(0)
    leg22.AddEntry( hmrat_mass_ovAK5g[jtypesToI_m['ak5ft']], "Filtered", "l")
    leg22.AddEntry( hmrat_mass_ovAK5g[jtypesToI_m['ak5tr']], "Trimmed", "l")
    leg22.AddEntry( hmrat_mass_ovAK5g[jtypesToI_m['ak5pr']], "Pruned", "l")
    leg22.AddEntry( hmrat_mass_ovAK5g[jtypesToI_m['ak5']], "Ungroomed", "l") 
    legPr1 = ROOT.TLegend(0.25,0.20,0.75,0.45)
    legPr1.SetFillColor(0)
    legPr1.SetBorderSize(0)
    legPr1.AddEntry( hmrat_mass_ovAK5g[jtypesToI_m['ak5ft']], "Filtered", "l")
    legPr1.AddEntry( hmrat_mass_ovAK5g[jtypesToI_m['ak5tr']], "Trimmed", "l")
    legPr1.AddEntry( hmrat_mass_ovAK5g[jtypesToI_m['ak5pr']], "Pruned", "l")
    legPr1.AddEntry( hmrat_mass_ovAK5g[jtypesToI_m['ak5']], "Ungroomed", "l")   
    legPr2 = ROOT.TLegend(0.25,0.65,0.75,0.90)
    legPr2.SetFillColor(0)
    legPr2.SetBorderSize(0)
    legPr2.AddEntry( hmrat_mass_ovAK5g[jtypesToI_m['ak5ft']], "Filtered", "l")
    legPr2.AddEntry( hmrat_mass_ovAK5g[jtypesToI_m['ak5tr']], "Trimmed", "l")
    legPr2.AddEntry( hmrat_mass_ovAK5g[jtypesToI_m['ak5pr']], "Pruned", "l")
    legPr2.AddEntry( hmrat_mass_ovAK5g[jtypesToI_m['ak5']], "Ungroomed", "l")   
    
    c1 = ROOT.TCanvas("c1","c1",1200,800)
    c1.Divide(2,1)
    c1.cd(1)
    hmrat_mass_ovAK5g[jtypesToI_m['ak5']].Draw("hist")
    hmrat_mass_ovAK5g[jtypesToI_m['ak5ft']].Draw("histsames")
    hmrat_mass_ovAK5g[jtypesToI_m['ak5tr']].Draw("histsames")
    hmrat_mass_ovAK5g[jtypesToI_m['ak5pr']].Draw("histsames")
    c1.cd(2)
    hmrat_pt_ovAK5g[jtypesToI_m['ak5']].Draw("hist")
    hmrat_pt_ovAK5g[jtypesToI_m['ak5ft']].Draw("histsames")
    hmrat_pt_ovAK5g[jtypesToI_m['ak5tr']].Draw("histsames")
    hmrat_pt_ovAK5g[jtypesToI_m['ak5pr']].Draw("histsames")
    leg22.Draw()
    c1.SaveAs(figdir+"/ratio1D_ak5"+suffix)
    c1.SaveAs(figdir+"/ratio1D_ak5"+suffix2)
    c1.SaveAs(figdir+"/ratio1D_ak5"+suffix3)
    c17 = ROOT.TCanvas("c17","c17",1200,800)
    c17.Divide(2,1)
    c17.cd(1)
    hmrat_mass_ovAK7g[jtypesToI_m['ak7']].Draw("hist")
    hmrat_mass_ovAK7g[jtypesToI_m['ak7ft']].Draw("histsames")
    hmrat_mass_ovAK7g[jtypesToI_m['ak7tr']].Draw("histsames")
    hmrat_mass_ovAK7g[jtypesToI_m['ak7pr']].Draw("histsames")
    c17.cd(2)
    hmrat_pt_ovAK7g[jtypesToI_m['ak7']].Draw("hist")
    hmrat_pt_ovAK7g[jtypesToI_m['ak7ft']].Draw("histsames")
    hmrat_pt_ovAK7g[jtypesToI_m['ak7tr']].Draw("histsames")
    hmrat_pt_ovAK7g[jtypesToI_m['ak7pr']].Draw("histsames")
    leg22.Draw()                                      
    c17.SaveAs(figdir+"/ratio1D_ak7"+suffix)
    c17.SaveAs(figdir+"/ratio1D_ak7"+suffix2)
    c17.SaveAs(figdir+"/ratio1D_ak7"+suffix3)
    c18 = ROOT.TCanvas("c18","c18",1200,800)
    c18.Divide(2,1)
    c18.cd(1)
    hmrat_mass_ovAK8g[jtypesToI_m['ak8']].Draw("hist")
    hmrat_mass_ovAK8g[jtypesToI_m['ak8ft']].Draw("histsames")
    hmrat_mass_ovAK8g[jtypesToI_m['ak8tr']].Draw("histsames")
    hmrat_mass_ovAK8g[jtypesToI_m['ak8pr']].Draw("histsames")
    c18.cd(2)
    hmrat_pt_ovAK8g[jtypesToI_m['ak8']].Draw("hist")
    hmrat_pt_ovAK8g[jtypesToI_m['ak8ft']].Draw("histsames")
    hmrat_pt_ovAK8g[jtypesToI_m['ak8tr']].Draw("histsames")
    hmrat_pt_ovAK8g[jtypesToI_m['ak8pr']].Draw("histsames")
    leg22.Draw()                                      
    c18.SaveAs(figdir+"/ratio1D_ak8"+suffix)
    c18.SaveAs(figdir+"/ratio1D_ak8"+suffix2)
    c18.SaveAs(figdir+"/ratio1D_ak8"+suffix3)

    ## ----------------------------------------------
    ## fit slice plots
    
    c2 = ROOT.TCanvas("c2","c2",1800,600)
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
    legPr1.Draw()
    c2.SaveAs(figdir+"/ptRatioVsPt_mean"+suffix)
    c2.SaveAs(figdir+"/ptRatioVsPt_mean"+suffix2)
    c2.SaveAs(figdir+"/ptRatioVsPt_mean"+suffix3)

    c2s = ROOT.TCanvas("c2s","c2s",1800,600)
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
    legPr2.Draw()
    c2s.SaveAs(figdir+"/ptRatioVsPt_sigma"+suffix)
    c2s.SaveAs(figdir+"/ptRatioVsPt_sigma"+suffix2)
    c2s.SaveAs(figdir+"/ptRatioVsPt_sigma"+suffix3)

    c2nvs = ROOT.TCanvas("c2nvs","c2nvs",1800,600)
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
    legPr1.Draw()
    c2nvs.SaveAs(figdir+"/ptRatioVsNV_mean"+suffix)
    c2nvs.SaveAs(figdir+"/ptRatioVsNV_mean"+suffix2)
    c2nvs.SaveAs(figdir+"/ptRatioVsNV_mean"+suffix3)

    c2nvss = ROOT.TCanvas("c2nvss","c2nvss",1800,600)
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
    legPr2.Draw()
    c2nvss.SaveAs(figdir+"/ptRatioVsNV_sigma"+suffix)
    c2nvss.SaveAs(figdir+"/ptRatioVsNV_sigma"+suffix2)
    c2nvss.SaveAs(figdir+"/ptRatioVsNV_sigma"+suffix3)

    c2etas = ROOT.TCanvas("c2etas","c2etas",1800,600)
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
    legPr1.Draw()
    c2etas.SaveAs(figdir+"/ptRatioVsEta_mean"+suffix)
    c2etas.SaveAs(figdir+"/ptRatioVsEta_mean"+suffix2)
    c2etas.SaveAs(figdir+"/ptRatioVsEta_mean"+suffix3)

    c2etass = ROOT.TCanvas("c2etass","c2etass",1800,600)
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
    legPr2.Draw()
    c2etass.SaveAs(figdir+"/ptRatioVsEta_sigma"+suffix)
    c2etass.SaveAs(figdir+"/ptRatioVsEta_sigma"+suffix2)
    c2etass.SaveAs(figdir+"/ptRatioVsEta_sigma"+suffix3)

############################################################
############################################################
############################################################
############################################################
############################################################
########## 2 D   V A L I D A T I O N   P L O T S   ( V 3 ) 
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################

def plotter2D_V3(mcname,dataname,figdir):
    
    fm = ROOT.TFile(mcname)
    fd = ROOT.TFile(dataname)
    
    print "2D files: ", mcname,", ", dataname
    #theutils = myutils()
    
    ############################################################
    # S P E C I F I C   P L O T S
    ##### 
    hmrat_mass_ovAK7 = []
    hmrat_pt_ovAK7 = []    
    hmrat_mass_ovAK7g = []
    hmrat_pt_ovAK7g = []    
    hmrat_mass_ovAK7trg = []
    hmrat_mass_ovAK7ftg = [] 
    hmrat_mass_ovAK7prg = []
    hmrat_pt_ovAK7trg = []
    hmrat_pt_ovAK7ftg = [] 
    hmrat_pt_ovAK7prg = []
    
    hdrat_mass_ovAK7 = []
    hdrat_pt_ovAK7 = []    

    ## pt ratio in MC 
    pmrPt_pt_ovAK7 = []     
    pmrPt_pt_ovAK7g = []         
    pmrNV_pt_ovAK7 = []     
    pmrNV_pt_ovAK7g = []         
    pmrEta_pt_ovAK8g = []         
    pmrEta_pt_ovAK7 = []     
    pmrEta_pt_ovAK7g = []         
    
    pmrPt_mass_ovAK7 = []     
    pmrPt_mass_ovAK7g = []         
    pmrNV_mass_ovAK7 = []     
    pmrNV_mass_ovAK7g = []         
    pmrEta_mass_ovAK7 = []     
    pmrEta_mass_ovAK7g = []         
    
    pmrPt_mass_ovAK7trg = []         
    pmrNV_mass_ovAK7trg = []         
    pmrEta_mass_ovAK7trg = []         
    pmrPt_pt_ovAK7trg = []         
    pmrNV_pt_ovAK7trg = []         
    pmrEta_pt_ovAK7trg = []         
    pmrPt_mass_ovAK7ftg = []         
    pmrNV_mass_ovAK7ftg = []         
    pmrEta_mass_ovAK7ftg = []         
    pmrPt_pt_ovAK7ftg = []         
    pmrNV_pt_ovAK7ftg = []         
    pmrEta_pt_ovAK7ftg = []         
    pmrPt_mass_ovAK7prg = []         
    pmrNV_mass_ovAK7prg = []         
    pmrEta_mass_ovAK7prg = []         
    pmrPt_pt_ovAK7prg = []         
    pmrNV_pt_ovAK7prg = []         
    pmrEta_pt_ovAK7prg = []         
    
    for x in range(len(jtypes_mv3)):
        
        hmrat_mass_ovAK7.append( fm.Get("hrat_"+jtypes_mv3[x]+"_mass_ovAK7") ) 
        hmrat_pt_ovAK7.append( fm.Get("hrat_"+jtypes_mv3[x]+"_pt_ovAK7") ) 
        
        hmrat_mass_ovAK7g.append( fm.Get("hrat_"+jtypes_mv3[x]+"_mass_ovAK7g") ) 
        hmrat_pt_ovAK7g.append( fm.Get("hrat_"+jtypes_mv3[x]+"_pt_ovAK7g") ) 
        
        pmrPt_pt_ovAK7.append( fm.Get("prPt_pt"+jtypes_mv3[x]+"_ovAK7") ) 
        pmrPt_pt_ovAK7g.append( fm.Get("prPt_pt"+jtypes_mv3[x]+"_ovAK7g") ) 
        pmrNV_pt_ovAK7.append( fm.Get("prNV_pt"+jtypes_mv3[x]+"_ovAK7") ) 
        pmrNV_pt_ovAK7g.append( fm.Get("prNV_pt"+jtypes_mv3[x]+"_ovAK7g") ) 
        pmrEta_pt_ovAK7.append( fm.Get("prEta_pt"+jtypes_mv3[x]+"_ovAK7") ) 
        pmrEta_pt_ovAK7g.append( fm.Get("prEta_pt"+jtypes_mv3[x]+"_ovAK7g") ) 

        pmrPt_mass_ovAK7.append( fm.Get("prPt_mass"+jtypes_mv3[x]+"_ovAK7") ) 
        pmrPt_mass_ovAK7g.append( fm.Get("prPt_mass"+jtypes_mv3[x]+"_ovAK7g") ) 
        pmrNV_mass_ovAK7.append( fm.Get("prNV_mass"+jtypes_mv3[x]+"_ovAK7") ) 
        pmrNV_mass_ovAK7g.append( fm.Get("prNV_mass"+jtypes_mv3[x]+"_ovAK7g") ) 
        pmrEta_mass_ovAK7.append( fm.Get("prEta_mass"+jtypes_mv3[x]+"_ovAK7") ) 
        pmrEta_mass_ovAK7g.append( fm.Get("prEta_mass"+jtypes_mv3[x]+"_ovAK7g") ) 
        
        pmrPt_pt_ovAK7trg.append( fm.Get("prPt_pt"+jtypes_mv3[x]+"_ovAK7trg") ) 
        pmrNV_pt_ovAK7trg.append( fm.Get("prNV_pt"+jtypes_mv3[x]+"_ovAK7trg") ) 
        pmrEta_pt_ovAK7trg.append( fm.Get("prEta_pt"+jtypes_mv3[x]+"_ovAK7trg") ) 
        pmrPt_mass_ovAK7trg.append( fm.Get("prPt_mass"+jtypes_mv3[x]+"_ovAK7trg") ) 
        pmrNV_mass_ovAK7trg.append( fm.Get("prNV_mass"+jtypes_mv3[x]+"_ovAK7trg") ) 
        pmrEta_mass_ovAK7trg.append( fm.Get("prEta_mass"+jtypes_mv3[x]+"_ovAK7trg") ) 
        pmrPt_pt_ovAK7ftg.append( fm.Get("prPt_pt"+jtypes_mv3[x]+"_ovAK7ftg") ) 
        pmrNV_pt_ovAK7ftg.append( fm.Get("prNV_pt"+jtypes_mv3[x]+"_ovAK7ftg") ) 
        pmrEta_pt_ovAK7ftg.append( fm.Get("prEta_pt"+jtypes_mv3[x]+"_ovAK7ftg") ) 
        pmrPt_mass_ovAK7ftg.append( fm.Get("prPt_mass"+jtypes_mv3[x]+"_ovAK7ftg") ) 
        pmrNV_mass_ovAK7ftg.append( fm.Get("prNV_mass"+jtypes_mv3[x]+"_ovAK7ftg") ) 
        pmrEta_mass_ovAK7ftg.append( fm.Get("prEta_mass"+jtypes_mv3[x]+"_ovAK7ftg") ) 
        pmrPt_pt_ovAK7prg.append( fm.Get("prPt_pt"+jtypes_mv3[x]+"_ovAK7prg") ) 
        pmrNV_pt_ovAK7prg.append( fm.Get("prNV_pt"+jtypes_mv3[x]+"_ovAK7prg") ) 
        pmrEta_pt_ovAK7prg.append( fm.Get("prEta_pt"+jtypes_mv3[x]+"_ovAK7prg") ) 
        pmrPt_mass_ovAK7prg.append( fm.Get("prPt_mass"+jtypes_mv3[x]+"_ovAK7prg") ) 
        pmrNV_mass_ovAK7prg.append( fm.Get("prNV_mass"+jtypes_mv3[x]+"_ovAK7prg") ) 
        pmrEta_mass_ovAK7prg.append( fm.Get("prEta_mass"+jtypes_mv3[x]+"_ovAK7prg") ) 
        
        y = x+1
        SetHistProperties(hmrat_pt_ovAK7[x], cmap_mv3[y],cmap_mv3[y],0, 1, 1, 1)
        SetHistProperties(hmrat_mass_ovAK7[x], cmap_mv3[y],cmap_mv3[y],0, 1, 1, 1)
        
        SetHistProperties(hmrat_pt_ovAK7g[x], cmap_mv3[y],cmap_mv3[y],0, 1, 1, 1)
        SetHistProperties(hmrat_mass_ovAK7g[x], cmap_mv3[y],cmap_mv3[y],0, 1, 1, 1)
        
        SetHistProperties(pmrPt_pt_ovAK7[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrPt_pt_ovAK7g[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrNV_pt_ovAK7[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrNV_pt_ovAK7g[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrEta_pt_ovAK7[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrEta_pt_ovAK7g[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        
        SetHistProperties(pmrPt_pt_ovAK7trg[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrNV_pt_ovAK7trg[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrEta_pt_ovAK7trg[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrPt_pt_ovAK7ftg[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrNV_pt_ovAK7ftg[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrEta_pt_ovAK7ftg[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrPt_pt_ovAK7prg[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrNV_pt_ovAK7prg[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrEta_pt_ovAK7prg[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
    
        SetHistProperties(pmrPt_mass_ovAK7[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrPt_mass_ovAK7g[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrNV_mass_ovAK7[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrNV_mass_ovAK7g[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrEta_mass_ovAK7[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrEta_mass_ovAK7g[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
    
        SetHistProperties(pmrPt_mass_ovAK7trg[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrNV_mass_ovAK7trg[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrEta_mass_ovAK7trg[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrPt_mass_ovAK7ftg[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrNV_mass_ovAK7ftg[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrEta_mass_ovAK7ftg[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrPt_mass_ovAK7prg[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrNV_mass_ovAK7prg[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        SetHistProperties(pmrEta_mass_ovAK7prg[x], cmap_mv3[y],cmap_mv3[y],cmap_mv3[y], 1, 20, 1)
        
        pmrPt_pt_ovAK7[x].SetTitle("; (ak7) reco pT; pT reco - pT ak7 gen;")
        pmrPt_pt_ovAK7g[x].SetTitle("; (ak7) reco pT; pT reco - pT ak7 gen;")
        pmrNV_pt_ovAK7[x].SetTitle("; (ak7) nVertices; pT reco - pT ak7 gen;")
        pmrNV_pt_ovAK7g[x].SetTitle("; (ak7) nVertices; pT reco - pT ak7 gen;")
        pmrEta_pt_ovAK7[x].SetTitle("; (ak7) reco eta; pT reco - pT ak7 gen;")
        pmrEta_pt_ovAK7g[x].SetTitle("; (ak7) reco eta; pT reco - pT ak7 gen;")
    
    for x in range(len(jtypes_d)):
        hdrat_mass_ovAK7.append( fd.Get("hrat_"+jtypes_d[x]+"_mass_ovAK7") ) 
        hdrat_pt_ovAK7.append( fd.Get("hrat_"+jtypes_d[x]+"_pt_ovAK7") ) 
        y = x+1
        SetHistProperties(hdrat_pt_ovAK7[x], cmap_d[y],cmap_d[y],0, 1, 20, 1)
        SetHistProperties(hdrat_mass_ovAK7[x], cmap_d[y],cmap_d[y],0, 1, 20, 1)

            
    leg22 = ROOT.TLegend(0.20,0.6,0.55,0.9)
    leg22.SetFillColor(0)
    leg22.SetBorderSize(0)
    leg22.AddEntry( hmrat_mass_ovAK7[jtypesToI_mv3['ak7ft']], "Filtered/Ungroomed (MC/RECO)", "l")
    leg22.AddEntry( hmrat_mass_ovAK7[jtypesToI_mv3['ak7tr']], "Trimmed/Ungroomed (MC/RECO)", "l")
    leg22.AddEntry( hmrat_mass_ovAK7[jtypesToI_mv3['ak7pr']], "Pruned/Ungroomed (MC/RECO)", "l")
    leg22.AddEntry( hmrat_mass_ovAK7g[jtypesToI_mv3['ak7ftg']], "Filtered/Ungroomed (MC/GEN)", "l") 
    leg22.AddEntry( hmrat_mass_ovAK7g[jtypesToI_mv3['ak7trg']], "Trimmed/Ungroomed (MC/GEN)", "l") 
    leg22.AddEntry( hmrat_mass_ovAK7g[jtypesToI_mv3['ak7prg']], "Pruned/Ungroomed (MC/GEN)", "l") 
    leg22.AddEntry( hdrat_mass_ovAK7[jtypesToI_d['ak7ft']], "Filtered/Ungroomed (data)", "l")
    leg22.AddEntry( hdrat_mass_ovAK7[jtypesToI_d['ak7tr']], "Trimmed/Ungroomed (data)", "l")
    leg22.AddEntry( hdrat_mass_ovAK7[jtypesToI_d['ak7pr']], "Pruned/Ungroomed (data)", "l")
    
    c17 = ROOT.TCanvas("c17","c17",1200,800)
    scl = GetDataMCSclFactor(hdrat_mass_ovAK7[jtypesToI_mv3['ak7ft']], hmrat_mass_ovAK7[jtypesToI_mv3['ak7ft']]) 
    scl = GetDataMCSclFactor(hdrat_mass_ovAK7[jtypesToI_mv3['ak7ft']], hmrat_mass_ovAK7[jtypesToI_mv3['ak7tr']]) 
    scl = GetDataMCSclFactor(hdrat_mass_ovAK7[jtypesToI_mv3['ak7ft']], hmrat_mass_ovAK7[jtypesToI_mv3['ak7pr']]) 
    scl = GetDataMCSclFactor(hdrat_mass_ovAK7[jtypesToI_mv3['ak7ft']], hmrat_mass_ovAK7g[jtypesToI_mv3['ak7ftg']]) 
    scl = GetDataMCSclFactor(hdrat_mass_ovAK7[jtypesToI_mv3['ak7ft']], hmrat_mass_ovAK7g[jtypesToI_mv3['ak7trg']]) 
    scl = GetDataMCSclFactor(hdrat_mass_ovAK7[jtypesToI_mv3['ak7ft']], hmrat_mass_ovAK7g[jtypesToI_mv3['ak7prg']]) 
    scl = GetDataMCSclFactor(hdrat_mass_ovAK7[jtypesToI_mv3['ak7ft']], hdrat_mass_ovAK7[jtypesToI_mv3['ak7tr']]) 
    scl = GetDataMCSclFactor(hdrat_mass_ovAK7[jtypesToI_mv3['ak7ft']], hdrat_mass_ovAK7[jtypesToI_mv3['ak7pr']]) 

    hmrat_mass_ovAK7[jtypesToI_mv3['ak7ft']].GetXaxis().SetRangeUser(0.,1.1)
    hmrat_mass_ovAK7[jtypesToI_mv3['ak7ft']].SetMaximum( hmrat_mass_ovAK7g[jtypesToI_mv3['ak7ftg']].GetMaximum()*1.1 )
    hmrat_mass_ovAK7[jtypesToI_mv3['ak7ft']].GetXaxis().SetTitle("ak7 jet mass ratio")
    hmrat_mass_ovAK7[jtypesToI_mv3['ak7ft']].Draw("hist")
    hmrat_mass_ovAK7[jtypesToI_mv3['ak7tr']].Draw("histsames")
    hmrat_mass_ovAK7[jtypesToI_mv3['ak7pr']].Draw("histsames")
    hdrat_mass_ovAK7[jtypesToI_mv3['ak7ft']].Draw("pe1x0sames")
    hdrat_mass_ovAK7[jtypesToI_mv3['ak7tr']].Draw("pe1x0sames")
    hdrat_mass_ovAK7[jtypesToI_mv3['ak7pr']].Draw("pe1x0sames")
    hmrat_mass_ovAK7g[jtypesToI_mv3['ak7ftg']].SetLineStyle( 2 )
    hmrat_mass_ovAK7g[jtypesToI_mv3['ak7ftg']].Draw("histsames")
    hmrat_mass_ovAK7g[jtypesToI_mv3['ak7trg']].SetLineStyle( 2 )
    hmrat_mass_ovAK7g[jtypesToI_mv3['ak7trg']].Draw("histsames")
    hmrat_mass_ovAK7g[jtypesToI_mv3['ak7prg']].SetLineStyle( 2 )
    hmrat_mass_ovAK7g[jtypesToI_mv3['ak7prg']].Draw("histsames")    
    leg22.Draw()                                      
    c17.SaveAs(figdir+"/ratio1D_ak7_wGroomedGenJets"+suffix)
    c17.SaveAs(figdir+"/ratio1D_ak7_wGroomedGenJets"+suffix2)
    c17.SaveAs(figdir+"/ratio1D_ak7_wGroomedGenJets"+suffix3)
    


    cprpt = ROOT.TCanvas("cprpt","cprpt",800,800)
    h7 = theutils.GetFitSlicesY( pmrPt_pt_ovAK7g[jtypesToI_mv3['ak7']], 1 )
    h7tr = theutils.GetFitSlicesY( pmrPt_pt_ovAK7trg[jtypesToI_mv3['ak7tr']], 1 )
    h7ft = theutils.GetFitSlicesY( pmrPt_pt_ovAK7ftg[jtypesToI_mv3['ak7ft']], 1 )
    h7pr = theutils.GetFitSlicesY( pmrPt_pt_ovAK7prg[jtypesToI_mv3['ak7pr']], 1 )
    h7.GetYaxis().SetRangeUser( 0.8, 1.2 )
    h7.Draw()
    h7tr.Draw("sames")
    h7ft.Draw("sames")
    h7pr.Draw("sames")
    cprpt.SaveAs(figdir+"/ptRatioVsPt_mean_wGroomedGenJets"+suffix)
    cprpt.SaveAs(figdir+"/ptRatioVsPt_mean_wGroomedGenJets"+suffix2)
    cprpt.SaveAs(figdir+"/ptRatioVsPt_mean_wGroomedGenJets"+suffix3)

    cprnv = ROOT.TCanvas("cprnv","cprnv",800,800)
    h7NV = theutils.GetFitSlicesY( pmrNV_pt_ovAK7g[jtypesToI_mv3['ak7']], 1 )
    h7trNV = theutils.GetFitSlicesY( pmrNV_pt_ovAK7trg[jtypesToI_mv3['ak7tr']], 1 )
    h7ftNV = theutils.GetFitSlicesY( pmrNV_pt_ovAK7ftg[jtypesToI_mv3['ak7ft']], 1 )
    h7prNV = theutils.GetFitSlicesY( pmrNV_pt_ovAK7prg[jtypesToI_mv3['ak7pr']], 1 )
    h7NV.GetYaxis().SetRangeUser( 0.8, 1.2 )
    h7NV.Draw()
    h7trNV.Draw("sames")
    h7ftNV.Draw("sames")
    h7prNV.Draw("sames")
    cprnv.SaveAs(figdir+"/ptRatioVsNV_mean_wGroomedGenJets"+suffix)
    cprnv.SaveAs(figdir+"/ptRatioVsNV_mean_wGroomedGenJets"+suffix2)
    cprnv.SaveAs(figdir+"/ptRatioVsNV_mean_wGroomedGenJets"+suffix3)

    ## ----------------------------------------------
    ## fit slice plots
    
#    c2 = ROOT.TCanvas("c2","c2",1800,600)
#    c2.Divide(3,1)
#    c2.cd(1)
#    h5 = theutils.GetFitSlicesY( pmrPt_pt_ovAK5g[jtypesToI_m['ak5']], 1 )
#    h5.GetYaxis().SetRangeUser(0.8,1.1)
#    h5.Draw()
#    h5f = theutils.GetFitSlicesY( pmrPt_pt_ovAK5g[jtypesToI_m['ak5ft']], 1 )
#    h5f.Draw("sames")
#    h5t = theutils.GetFitSlicesY( pmrPt_pt_ovAK5g[jtypesToI_m['ak5tr']], 1 )
#    h5t.Draw("sames")
#    h5p = theutils.GetFitSlicesY( pmrPt_pt_ovAK5g[jtypesToI_m['ak5pr']], 1 )
#    h5p.Draw("sames")
#    c2.cd(2)
#    h7 = theutils.GetFitSlicesY( pmrPt_pt_ovAK7g[jtypesToI_m['ak7']], 1 )
#    h7.GetYaxis().SetRangeUser(0.8,1.1)
#    h7.Draw()
#    h7f = theutils.GetFitSlicesY( pmrPt_pt_ovAK7g[jtypesToI_m['ak7ft']], 1 )
#    h7f.Draw("sames")
#    h7t = theutils.GetFitSlicesY( pmrPt_pt_ovAK7g[jtypesToI_m['ak7tr']], 1 )
#    h7t.Draw("sames")
#    h7p = theutils.GetFitSlicesY( pmrPt_pt_ovAK7g[jtypesToI_m['ak7pr']], 1 )
#    h7p.Draw("sames")
#    c2.cd(3)
#    h8 = theutils.GetFitSlicesY( pmrPt_pt_ovAK8g[jtypesToI_m['ak8']], 1 )
#    h8.GetYaxis().SetRangeUser(0.8,1.1)
#    h8.Draw()
#    h8f = theutils.GetFitSlicesY( pmrPt_pt_ovAK8g[jtypesToI_m['ak8ft']], 1 )
#    h8f.Draw("sames")
#    h8t = theutils.GetFitSlicesY( pmrPt_pt_ovAK8g[jtypesToI_m['ak8tr']], 1 )
#    h8t.Draw("sames")
#    h8p = theutils.GetFitSlicesY( pmrPt_pt_ovAK8g[jtypesToI_m['ak8pr']], 1 )
#    h8p.Draw("sames")
#    legPr1.Draw()
#    c2.SaveAs(figdir+"/ptRatioVsPt_mean"+suffix)
#    c2.SaveAs(figdir+"/ptRatioVsPt_mean"+suffix2)
#    c2.SaveAs(figdir+"/ptRatioVsPt_mean"+suffix3)
#    
#    c2s = ROOT.TCanvas("c2s","c2s",1800,600)
#    c2s.Divide(3,1)
#    c2s.cd(1)
#    hs5 = theutils.GetFitSlicesY( pmrPt_pt_ovAK5g[jtypesToI_m['ak5']], 2 )
#    hs5.GetYaxis().SetRangeUser(0.,0.25)
#    hs5.Draw()
#    hs5f = theutils.GetFitSlicesY( pmrPt_pt_ovAK5g[jtypesToI_m['ak5ft']], 2 )
#    hs5f.Draw("sames")
#    hs5t = theutils.GetFitSlicesY( pmrPt_pt_ovAK5g[jtypesToI_m['ak5tr']], 2 )
#    hs5t.Draw("sames")
#    hs5p = theutils.GetFitSlicesY( pmrPt_pt_ovAK5g[jtypesToI_m['ak5pr']], 2 )
#    hs5p.Draw("sames")
#    c2s.cd(2)
#    hs7 = theutils.GetFitSlicesY( pmrPt_pt_ovAK7g[jtypesToI_m['ak7']], 2 )
#    hs7.GetYaxis().SetRangeUser(0.,0.25)
#    hs7.Draw()
#    hs7f = theutils.GetFitSlicesY( pmrPt_pt_ovAK7g[jtypesToI_m['ak7ft']], 2 )
#    hs7f.Draw("sames")
#    hs7t = theutils.GetFitSlicesY( pmrPt_pt_ovAK7g[jtypesToI_m['ak7tr']], 2 )
#    hs7t.Draw("sames")
#    hs7p = theutils.GetFitSlicesY( pmrPt_pt_ovAK7g[jtypesToI_m['ak7pr']], 2 )
#    hs7p.Draw("sames")
#    c2s.cd(3)
#    hs8 = theutils.GetFitSlicesY( pmrPt_pt_ovAK8g[jtypesToI_m['ak8']], 2 )
#    hs8.GetYaxis().SetRangeUser(0.,0.25)
#    hs8.Draw()
#    hs8f = theutils.GetFitSlicesY( pmrPt_pt_ovAK8g[jtypesToI_m['ak8ft']], 2 )
#    hs8f.Draw("sames")
#    hs8t = theutils.GetFitSlicesY( pmrPt_pt_ovAK8g[jtypesToI_m['ak8tr']], 2 )
#    hs8t.Draw("sames")
#    hs8p = theutils.GetFitSlicesY( pmrPt_pt_ovAK8g[jtypesToI_m['ak8pr']], 2 )
#    hs8p.Draw("sames")
#    legPr2.Draw()
#    c2s.SaveAs(figdir+"/ptRatioVsPt_sigma"+suffix)
#    c2s.SaveAs(figdir+"/ptRatioVsPt_sigma"+suffix2)
#    c2s.SaveAs(figdir+"/ptRatioVsPt_sigma"+suffix3)
#    
#    c2nvs = ROOT.TCanvas("c2nvs","c2nvs",1800,600)
#    c2nvs.Divide(3,1)
#    c2nvs.cd(1)
#    h5 = theutils.GetFitSlicesY( pmrNV_pt_ovAK5g[jtypesToI_m['ak5']], 1 )
#    h5.GetYaxis().SetRangeUser(0.8,1.1)
#    h5.Draw()
#    h5f = theutils.GetFitSlicesY( pmrNV_pt_ovAK5g[jtypesToI_m['ak5ft']], 1 )
#    h5f.Draw("sames")
#    h5t = theutils.GetFitSlicesY( pmrNV_pt_ovAK5g[jtypesToI_m['ak5tr']], 1 )
#    h5t.Draw("sames")
#    h5p = theutils.GetFitSlicesY( pmrNV_pt_ovAK5g[jtypesToI_m['ak5pr']], 1 )
#    h5p.Draw("sames")
#    c2nvs.cd(2)
#    h7 = theutils.GetFitSlicesY( pmrNV_pt_ovAK7g[jtypesToI_m['ak7']], 1 )
#    h7.GetYaxis().SetRangeUser(0.8,1.1)
#    h7.Draw()
#    h7f = theutils.GetFitSlicesY( pmrNV_pt_ovAK7g[jtypesToI_m['ak7ft']], 1 )
#    h7f.Draw("sames")
#    h7t = theutils.GetFitSlicesY( pmrNV_pt_ovAK7g[jtypesToI_m['ak7tr']], 1 )
#    h7t.Draw("sames")
#    h7p = theutils.GetFitSlicesY( pmrNV_pt_ovAK7g[jtypesToI_m['ak7pr']], 1 )
#    h7p.Draw("sames")
#    c2nvs.cd(3)
#    h8 = theutils.GetFitSlicesY( pmrNV_pt_ovAK8g[jtypesToI_m['ak8']], 1 )
#    h8.GetYaxis().SetRangeUser(0.8,1.1)
#    h8.Draw()
#    h8f = theutils.GetFitSlicesY( pmrNV_pt_ovAK8g[jtypesToI_m['ak8ft']], 1 )
#    h8f.Draw("sames")
#    h8t = theutils.GetFitSlicesY( pmrNV_pt_ovAK8g[jtypesToI_m['ak8tr']], 1 )
#    h8t.Draw("sames")
#    h8p = theutils.GetFitSlicesY( pmrNV_pt_ovAK8g[jtypesToI_m['ak8pr']], 1 )
#    h8p.Draw("sames")
#    legPr1.Draw()
#    c2nvs.SaveAs(figdir+"/ptRatioVsNV_mean"+suffix)
#    c2nvs.SaveAs(figdir+"/ptRatioVsNV_mean"+suffix2)
#    c2nvs.SaveAs(figdir+"/ptRatioVsNV_mean"+suffix3)
#    
#    c2nvss = ROOT.TCanvas("c2nvss","c2nvss",1800,600)
#    c2nvss.Divide(3,1)
#    c2nvss.cd(1)
#    hs5 = theutils.GetFitSlicesY( pmrNV_pt_ovAK5g[jtypesToI_m['ak5']], 2 )
#    hs5.GetYaxis().SetRangeUser(0.,0.25)
#    hs5.Draw()
#    hs5f = theutils.GetFitSlicesY( pmrNV_pt_ovAK5g[jtypesToI_m['ak5ft']], 2 )
#    hs5f.Draw("sames")
#    hs5t = theutils.GetFitSlicesY( pmrNV_pt_ovAK5g[jtypesToI_m['ak5tr']], 2 )
#    hs5t.Draw("sames")
#    hs5p = theutils.GetFitSlicesY( pmrNV_pt_ovAK5g[jtypesToI_m['ak5pr']], 2 )
#    hs5p.Draw("sames")
#    c2nvss.cd(2)
#    hs7 = theutils.GetFitSlicesY( pmrNV_pt_ovAK7g[jtypesToI_m['ak7']], 2 )
#    hs7.GetYaxis().SetRangeUser(0.,0.25)
#    hs7.Draw()
#    hs7f = theutils.GetFitSlicesY( pmrNV_pt_ovAK7g[jtypesToI_m['ak7ft']], 2 )
#    hs7f.Draw("sames")
#    hs7t = theutils.GetFitSlicesY( pmrNV_pt_ovAK7g[jtypesToI_m['ak7tr']], 2 )
#    hs7t.Draw("sames")
#    hs7p = theutils.GetFitSlicesY( pmrNV_pt_ovAK7g[jtypesToI_m['ak7pr']], 2 )
#    hs7p.Draw("sames")
#    c2nvss.cd(3)
#    hs8 = theutils.GetFitSlicesY( pmrNV_pt_ovAK8g[jtypesToI_m['ak8']], 2 )
#    hs8.GetYaxis().SetRangeUser(0.,0.25)
#    hs8.Draw()
#    hs8f = theutils.GetFitSlicesY( pmrNV_pt_ovAK8g[jtypesToI_m['ak8ft']], 2 )
#    hs8f.Draw("sames")
#    hs8t = theutils.GetFitSlicesY( pmrNV_pt_ovAK8g[jtypesToI_m['ak8tr']], 2 )
#    hs8t.Draw("sames")
#    hs8p = theutils.GetFitSlicesY( pmrNV_pt_ovAK8g[jtypesToI_m['ak8pr']], 2 )
#    hs8p.Draw("sames")
#    legPr2.Draw()
#    c2nvss.SaveAs(figdir+"/ptRatioVsNV_sigma"+suffix)
#    c2nvss.SaveAs(figdir+"/ptRatioVsNV_sigma"+suffix2)
#    c2nvss.SaveAs(figdir+"/ptRatioVsNV_sigma"+suffix3)
#    
#    c2etas = ROOT.TCanvas("c2etas","c2etas",1800,600)
#    c2etas.Divide(3,1)
#    c2etas.cd(1)
#    h5 = theutils.GetFitSlicesY( pmrEta_pt_ovAK5g[jtypesToI_m['ak5']], 1 )
#    h5.GetYaxis().SetRangeUser(0.8,1.1)
#    h5.Draw()
#    h5f = theutils.GetFitSlicesY( pmrEta_pt_ovAK5g[jtypesToI_m['ak5ft']], 1 )
#    h5f.Draw("sames")
#    h5t = theutils.GetFitSlicesY( pmrEta_pt_ovAK5g[jtypesToI_m['ak5tr']], 1 )
#    h5t.Draw("sames")
#    h5p = theutils.GetFitSlicesY( pmrEta_pt_ovAK5g[jtypesToI_m['ak5pr']], 1 )
#    h5p.Draw("sames")
#    c2etas.cd(2)
#    h7 = theutils.GetFitSlicesY( pmrEta_pt_ovAK7g[jtypesToI_m['ak7']], 1 )
#    h7.GetYaxis().SetRangeUser(0.8,1.1)
#    h7.Draw()
#    h7f = theutils.GetFitSlicesY( pmrEta_pt_ovAK7g[jtypesToI_m['ak7ft']], 1 )
#    h7f.Draw("sames")
#    h7t = theutils.GetFitSlicesY( pmrEta_pt_ovAK7g[jtypesToI_m['ak7tr']], 1 )
#    h7t.Draw("sames")
#    h7p = theutils.GetFitSlicesY( pmrEta_pt_ovAK7g[jtypesToI_m['ak7pr']], 1 )
#    h7p.Draw("sames")
#    c2etas.cd(3)
#    h8 = theutils.GetFitSlicesY( pmrEta_pt_ovAK8g[jtypesToI_m['ak8']], 1 )
#    h8.GetYaxis().SetRangeUser(0.8,1.1)
#    h8.Draw()
#    h8f = theutils.GetFitSlicesY( pmrEta_pt_ovAK8g[jtypesToI_m['ak8ft']], 1 )
#    h8f.Draw("sames")
#    h8t = theutils.GetFitSlicesY( pmrEta_pt_ovAK8g[jtypesToI_m['ak8tr']], 1 )
#    h8t.Draw("sames")
#    h8p = theutils.GetFitSlicesY( pmrEta_pt_ovAK8g[jtypesToI_m['ak8pr']], 1 )
#    h8p.Draw("sames")
#    legPr1.Draw()
#    c2etas.SaveAs(figdir+"/ptRatioVsEta_mean"+suffix)
#    c2etas.SaveAs(figdir+"/ptRatioVsEta_mean"+suffix2)
#    c2etas.SaveAs(figdir+"/ptRatioVsEta_mean"+suffix3)
#    
#    c2etass = ROOT.TCanvas("c2etass","c2etass",1800,600)
#    c2etass.Divide(3,1)
#    c2etass.cd(1)
#    hs5 = theutils.GetFitSlicesY( pmrEta_pt_ovAK5g[jtypesToI_m['ak5']], 2 )
#    hs5.GetYaxis().SetRangeUser(0.,0.25)
#    hs5.Draw()
#    hs5f = theutils.GetFitSlicesY( pmrEta_pt_ovAK5g[jtypesToI_m['ak5ft']], 2 )
#    hs5f.Draw("sames")
#    hs5t = theutils.GetFitSlicesY( pmrEta_pt_ovAK5g[jtypesToI_m['ak5tr']], 2 )
#    hs5t.Draw("sames")
#    hs5p = theutils.GetFitSlicesY( pmrEta_pt_ovAK5g[jtypesToI_m['ak5pr']], 2 )
#    hs5p.Draw("sames")
#    c2etass.cd(2)
#    hs7 = theutils.GetFitSlicesY( pmrEta_pt_ovAK7g[jtypesToI_m['ak7']], 2 )
#    hs7.GetYaxis().SetRangeUser(0.,0.25)
#    hs7.Draw()
#    hs7f = theutils.GetFitSlicesY( pmrEta_pt_ovAK7g[jtypesToI_m['ak7ft']], 2 )
#    hs7f.Draw("sames")
#    hs7t = theutils.GetFitSlicesY( pmrEta_pt_ovAK7g[jtypesToI_m['ak7tr']], 2 )
#    hs7t.Draw("sames")
#    hs7p = theutils.GetFitSlicesY( pmrEta_pt_ovAK7g[jtypesToI_m['ak7pr']], 2 )
#    hs7p.Draw("sames")
#    c2etass.cd(3)
#    hs8 = theutils.GetFitSlicesY( pmrEta_pt_ovAK8g[jtypesToI_m['ak8']], 2 )
#    hs8.GetYaxis().SetRangeUser(0.,0.25)
#    hs8.Draw()
#    hs8f = theutils.GetFitSlicesY( pmrEta_pt_ovAK8g[jtypesToI_m['ak8ft']], 2 )
#    hs8f.Draw("sames")
#    hs8t = theutils.GetFitSlicesY( pmrEta_pt_ovAK8g[jtypesToI_m['ak8tr']], 2 )
#    hs8t.Draw("sames")
#    hs8p = theutils.GetFitSlicesY( pmrEta_pt_ovAK8g[jtypesToI_m['ak8pr']], 2 )
#    hs8p.Draw("sames")
#    legPr2.Draw()
#    c2etass.SaveAs(figdir+"/ptRatioVsEta_sigma"+suffix)
#    c2etass.SaveAs(figdir+"/ptRatioVsEta_sigma"+suffix2)
#    c2etass.SaveAs(figdir+"/ptRatioVsEta_sigma"+suffix3)


############################################################
############################################################
############################################################
############################################################
############################################################
########## 2 D   P L O T S   W I T H   J E T   M A S S 
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
    
    prmPt_mass = []
    prmNV_mass = []
    
    pdrPt_mass_ovAK5 = []    
    pdrPt_mass_ovAK7 = []    
    pdrPt_mass_ovAK8 = []    
    pdrNV_mass_ovAK5 = []    
    pdrNV_mass_ovAK7 = []    
    pdrNV_mass_ovAK8 = []    
    pdrEta_mass_ovAK5 = []    
    pdrEta_mass_ovAK7 = []    
    pdrEta_mass_ovAK8 = []    
    
    prdPt_mass = []
    prdNV_mass = []


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
        
        prmPt_mass.append( fm.Get("prPt_mass_"+jtypes_m[x]) )
        prmNV_mass.append( fm.Get("prNV_mass_"+jtypes_m[x]) )
        
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
        
        SetHistProperties_wName(prmPt_mass[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 21, 1, "prmPt_mass"+jtypes_m[x])    
        SetHistProperties_wName(prmNV_mass[x], cmap_m[y],cmap_m[y],cmap_m[y], 1, 21, 1, "prmNV_mass"+jtypes_m[x])


        pmrPt_mass_ovAK5[x].SetTitle("; pT (ak5 jets); m_{j}/m{j0}")
        pmrPt_mass_ovAK5g[x].SetTitle("; pT (ak5 jets); m_{j}/m{j0}")
        pmrPt_mass_ovAK7[x].SetTitle("; pT (ak5 jets); m_{j}/m{j0}")
        pmrPt_mass_ovAK7g[x].SetTitle("; pT (ak5 jets); m_{j}/m{j0}")
        pmrPt_mass_ovAK8[x].SetTitle("; pT (ak5 jets); m_{j}/m{j0}")
        pmrPt_mass_ovAK8g[x].SetTitle("; pT (ak5 jets); m_{j}/m{j0}")
        pmrNV_mass_ovAK5[x].SetTitle("; pT (ak5 jets); m_{j}/m{j0}")
        pmrNV_mass_ovAK5g[x].SetTitle("; pT (ak5 jets); m_{j}/m{j0}")
        pmrNV_mass_ovAK7[x].SetTitle("; pT (ak5 jets); m_{j}/m{j0}")
        pmrNV_mass_ovAK7g[x].SetTitle("; pT (ak5 jets); m_{j}/m{j0}")
        pmrNV_mass_ovAK8[x].SetTitle("; pT (ak5 jets); m_{j}/m{j0}")
        pmrNV_mass_ovAK8g[x].SetTitle("; pT (ak5 jets); m_{j}/m{j0}")
        pmrEta_mass_ovAK5[x].SetTitle("; pT (ak5 jets); m_{j}/m{j0}")
        pmrEta_mass_ovAK5g[x].SetTitle("; pT (ak5 jets); m_{j}/m{j0}")
        pmrEta_mass_ovAK7[x].SetTitle("; pT (ak5 jets); m_{j}/m{j0}")
        pmrEta_mass_ovAK7g[x].SetTitle("; pT (ak5 jets); m_{j}/m{j0}")
        pmrEta_mass_ovAK8[x].SetTitle("; pT (ak5 jets); m_{j}/m{j0}")
        pmrEta_mass_ovAK8g[x].SetTitle("; pT (ak5 jets); m_{j}/m{j0}")

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
        
        prdPt_mass.append( fd.Get("prPt_mass_"+jtypes_d[x]) )
        prdNV_mass.append( fd.Get("prNV_mass_"+jtypes_d[x]) )

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

        SetHistProperties(prdPt_mass[x], cmap_d[y],cmap_d[y],cmap_d[y], 1, 24, 1)
        SetHistProperties(prdNV_mass[x], cmap_d[y],cmap_d[y],cmap_d[y], 1, 24, 1)


    legPr1 = ROOT.TLegend(0.25,0.6,0.75,0.9)
    legPr1.SetFillColor(0)
    legPr1.SetBorderSize(0)
    legPr1.AddEntry( pdrPt_mass_ovAK5[jtypesToI_m['ak5ft']], "Filtered", "l")
    legPr1.AddEntry( pdrPt_mass_ovAK5[jtypesToI_m['ak5tr']], "Trimmed", "l")
    legPr1.AddEntry( pdrPt_mass_ovAK5[jtypesToI_m['ak5pr']], "Pruned", "l")
    legPr1.AddEntry( pdrPt_mass_ovAK5[jtypesToI_m['ak5']], "Ungroomed", "l")   
    legPr2 = ROOT.TLegend(0.25,0.6,0.75,0.9)
    legPr2.SetFillColor(0)
    legPr2.SetBorderSize(0)
    legPr2.AddEntry( pmrPt_mass_ovAK5[jtypesToI_m['ak5ft']], "Filtered", "lp")
    legPr2.AddEntry( pmrPt_mass_ovAK5[jtypesToI_m['ak5tr']], "Trimmed", "lp")
    legPr2.AddEntry( pmrPt_mass_ovAK5[jtypesToI_m['ak5pr']], "Pruned", "lp")
    legPr2.AddEntry( pdrPt_mass_ovAK5[jtypesToI_m['ak5ft']], "Filtered", "lp")
    legPr2.AddEntry( pdrPt_mass_ovAK5[jtypesToI_m['ak5tr']], "Trimmed", "lp")
    legPr2.AddEntry( pdrPt_mass_ovAK5[jtypesToI_m['ak5pr']], "Pruned", "lp")

    mmvp = prmPt_mass[jtypesToI_m['ak7']].ProfileX()
    mmvpt = prmPt_mass[jtypesToI_m['ak7tr']].ProfileX()
    mmvpf = prmPt_mass[jtypesToI_m['ak7ft']].ProfileX()
    mmvpp = prmPt_mass[jtypesToI_m['ak7pr']].ProfileX()
    mmvn = prmNV_mass[jtypesToI_m['ak7']].ProfileX()
    mmvnt = prmNV_mass[jtypesToI_m['ak7tr']].ProfileX()
    mmvnf = prmNV_mass[jtypesToI_m['ak7ft']].ProfileX()
    mmvnp = prmNV_mass[jtypesToI_m['ak7pr']].ProfileX()

    dmvp = prdPt_mass[jtypesToI_d['ak7']].ProfileX()
    dmvpt = prdPt_mass[jtypesToI_d['ak7tr']].ProfileX()
    dmvpf = prdPt_mass[jtypesToI_d['ak7ft']].ProfileX()
    dmvpp = prdPt_mass[jtypesToI_d['ak7pr']].ProfileX()
    dmvn = prdNV_mass[jtypesToI_d['ak7']].ProfileX()
    dmvnt = prdNV_mass[jtypesToI_d['ak7tr']].ProfileX()
    dmvnf = prdNV_mass[jtypesToI_d['ak7ft']].ProfileX()
    dmvnp = prdNV_mass[jtypesToI_d['ak7pr']].ProfileX()

    cm = ROOT.TCanvas("cm1","cm1",1400,800)
    cm.Divide(2,1)
    cm.cd(1)
    mmvp.GetYaxis().SetRangeUser( 0., 100. )
    mmvp.Draw()
    mmvpt.Draw("sames")
    mmvpf.Draw("sames")
    mmvpp.Draw("sames")
    dmvp.Draw("sames")
    dmvpt.Draw("sames")
    dmvpf.Draw("sames")
    dmvpp.Draw("sames")
    cm.cd(2)
    mmvn.GetYaxis().SetRangeUser( 0., 100. )
    mmvn.GetXaxis().SetTitle("nV")
    mmvn.Draw()
    mmvnt.Draw("sames")
    mmvnf.Draw("sames")
    mmvnp.Draw("sames")
    dmvn.Draw("sames")
    dmvnt.Draw("sames")
    dmvnf.Draw("sames")
    dmvnp.Draw("sames")
    cm.SaveAs(figdir+"/mass_vsPtNV"+suffix)
    cm.SaveAs(figdir+"/mass_vsPtNV"+suffix2)
    cm.SaveAs(figdir+"/mass_vsPtNV"+suffix3)
    
    print "--------> 3"    
    cm1 = ROOT.TCanvas("cm1","cm1",1800,800)
    cm1.Divide(3,1)
    cm1.cd(1)
    h5 = pmrPt_mass_ovAK5g[jtypesToI_m['ak5']].ProfileX()
    h5f = pmrPt_mass_ovAK5g[jtypesToI_m['ak5ft']].ProfileX()
    h5t = pmrPt_mass_ovAK5g[jtypesToI_m['ak5tr']].ProfileX()
    h5p = pmrPt_mass_ovAK5g[jtypesToI_m['ak5pr']].ProfileX()
    h5.GetYaxis().SetRangeUser( 0.3,2.0 )
    h5.Draw()
    h5f.Draw("sames")
    h5t.Draw("sames")
    h5p.Draw("sames")
    cm1.cd(2)
    h7 = pmrPt_mass_ovAK7g[jtypesToI_m['ak7']].ProfileX()
    h7f = pmrPt_mass_ovAK7g[jtypesToI_m['ak7ft']].ProfileX()
    h7t = pmrPt_mass_ovAK7g[jtypesToI_m['ak7tr']].ProfileX()
    h7p = pmrPt_mass_ovAK7g[jtypesToI_m['ak7pr']].ProfileX()
    h7.GetYaxis().SetRangeUser( 0.3,2.0 )
    h7.Draw()
    h7f.Draw("sames")
    h7t.Draw("sames")
    h7p.Draw("sames")
    cm1.cd(3)
    h8 = pmrPt_mass_ovAK8g[jtypesToI_m['ak8']].ProfileX()
    h8f = pmrPt_mass_ovAK8g[jtypesToI_m['ak8ft']].ProfileX()
    h8t = pmrPt_mass_ovAK8g[jtypesToI_m['ak8tr']].ProfileX()
    h8p = pmrPt_mass_ovAK8g[jtypesToI_m['ak8pr']].ProfileX()
    h8.GetYaxis().SetRangeUser( 0.3,2.0 )
    h8.Draw()
    h8f.Draw("sames")
    h8t.Draw("sames")
    h8p.Draw("sames")
    legPr1.Draw() 
    cm1.SaveAs(figdir+"/massRatioOvGen_vsPt"+suffix)
    cm1.SaveAs(figdir+"/massRatioOvGen_vsPt"+suffix2)
    cm1.SaveAs(figdir+"/massRatioOvGen_vsPt"+suffix3)

    print "--------> 4"    

    cm2 = ROOT.TCanvas("cm2","cm2",1800,800)
    cm2.Divide(3,1)
    cm2.cd(1)
    h5 = pmrNV_mass_ovAK5g[jtypesToI_m['ak5']].ProfileX()
    h5f = pmrNV_mass_ovAK5g[jtypesToI_m['ak5ft']].ProfileX()
    h5t = pmrNV_mass_ovAK5g[jtypesToI_m['ak5tr']].ProfileX()
    h5p = pmrNV_mass_ovAK5g[jtypesToI_m['ak5pr']].ProfileX()
    h5.GetYaxis().SetRangeUser( 0.3,2.0 )
    h5.Draw()
    h5f.Draw("sames")
    h5t.Draw("sames")
    h5p.Draw("sames")
    legPr1.Draw()  
    cm2.cd(2)
    h7 = pmrNV_mass_ovAK7g[jtypesToI_m['ak7']].ProfileX()
    h7f = pmrNV_mass_ovAK7g[jtypesToI_m['ak7ft']].ProfileX()
    h7t = pmrNV_mass_ovAK7g[jtypesToI_m['ak7tr']].ProfileX()
    h7p = pmrNV_mass_ovAK7g[jtypesToI_m['ak7pr']].ProfileX()
    h7.GetYaxis().SetRangeUser( 0.3,2.0 )
    h7.Draw()
    h7f.Draw("sames")
    h7t.Draw("sames")
    h7p.Draw("sames")
    cm2.cd(3)
    h8 = pmrNV_mass_ovAK8g[jtypesToI_m['ak8']].ProfileX()
    h8f = pmrNV_mass_ovAK8g[jtypesToI_m['ak8ft']].ProfileX()
    h8t = pmrNV_mass_ovAK8g[jtypesToI_m['ak8tr']].ProfileX()
    h8p = pmrNV_mass_ovAK8g[jtypesToI_m['ak8pr']].ProfileX()
    h8.GetYaxis().SetRangeUser( 0.3,2.0 )
    h8.Draw()
    h8f.Draw("sames")
    h8t.Draw("sames")
    h8p.Draw("sames")
    cm2.SaveAs(figdir+"/massRatioOvGen_vsNV"+suffix)
    cm2.SaveAs(figdir+"/massRatioOvGen_vsNV"+suffix2)
    cm2.SaveAs(figdir+"/massRatioOvGen_vsNV"+suffix3)

    cm3 = ROOT.TCanvas("cm3","cm3",1800,800)
    cm3.Divide(3,1)
    cm3.cd(1)
    h5 = pmrEta_mass_ovAK5g[jtypesToI_m['ak5']].ProfileX()
    h5f = pmrEta_mass_ovAK5g[jtypesToI_m['ak5ft']].ProfileX()
    h5t = pmrEta_mass_ovAK5g[jtypesToI_m['ak5tr']].ProfileX()
    h5p = pmrEta_mass_ovAK5g[jtypesToI_m['ak5pr']].ProfileX()
    h5.GetYaxis().SetRangeUser( 0.3,2.0 )
    h5.Draw()
    h5f.Draw("sames")
    h5t.Draw("sames")
    h5p.Draw("sames")
    cm3.cd(2)
    h7 = pmrEta_mass_ovAK7g[jtypesToI_m['ak7']].ProfileX()
    h7f = pmrEta_mass_ovAK7g[jtypesToI_m['ak7ft']].ProfileX()
    h7t = pmrEta_mass_ovAK7g[jtypesToI_m['ak7tr']].ProfileX()
    h7p = pmrEta_mass_ovAK7g[jtypesToI_m['ak7pr']].ProfileX()
    h7.GetYaxis().SetRangeUser( 0.3,2.0 )
    h7.Draw()
    h7f.Draw("sames")
    h7t.Draw("sames")
    h7p.Draw("sames")
    cm3.cd(3)
    h8 = pmrEta_mass_ovAK8g[jtypesToI_m['ak8']].ProfileX()
    h8f = pmrEta_mass_ovAK8g[jtypesToI_m['ak8ft']].ProfileX()
    h8t = pmrEta_mass_ovAK8g[jtypesToI_m['ak8tr']].ProfileX()
    h8p = pmrEta_mass_ovAK8g[jtypesToI_m['ak8pr']].ProfileX()
    h8.GetYaxis().SetRangeUser( 0.3,2.0 )
    h8.Draw()
    h8f.Draw("sames")
    h8t.Draw("sames")
    h8p.Draw("sames")
    legPr1.Draw() 
    cm3.SaveAs(figdir+"/massRatioOvGen_vsEta"+suffix)
    cm3.SaveAs(figdir+"/massRatioOvGen_vsEta"+suffix2)
    cm3.SaveAs(figdir+"/massRatioOvGen_vsEta"+suffix3)

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
    legPr2.Draw() 
    c1.SaveAs(figdir+"/massRatioOvReco_vsPt"+suffix)
    c1.SaveAs(figdir+"/massRatioOvReco_vsPt"+suffix2)
    c1.SaveAs(figdir+"/massRatioOvReco_vsPt"+suffix3)

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
    legPr2.Draw()   
    c2.SaveAs(figdir+"/massRatioOvReco_vsNV"+suffix)
    c2.SaveAs(figdir+"/massRatioOvReco_vsNV"+suffix2)
    c2.SaveAs(figdir+"/massRatioOvReco_vsNV"+suffix3)

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
    legPr2.Draw() 
    c3.SaveAs(figdir+"/massRatioOvReco_vsEta"+suffix)
    c3.SaveAs(figdir+"/massRatioOvReco_vsEta"+suffix2)
    c3.SaveAs(figdir+"/massRatioOvReco_vsEta"+suffix3)

############################################################
############################################################
############################################################
############################################################
############################################################
########## 2 D   P L O T S   W I T H   J E T   M A S S 
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################

def plotter_unfolding(mcname,dataname,figdir):

    fm = ROOT.TFile(mcname)
    fd = ROOT.TFile(dataname)

    # get ingredients for ak7 unfolding
    hResponse = fm.Get("rur_ak7w")
    hMeas = fm.Get("h_ak7_mass")
    hTrue = fm.Get("h_ak7g_mass")
    hData = fd.Get("h_ak7_mass")
    hMeas.SetTitle("; jet mass;")
    doUnfolding_closure(hResponse, hMeas, hTrue, figdir+"/unfolding_closure_ak7")
    doUnfolding_data(hResponse, hMeas, hTrue, hData, figdir+"/unfolding_data_ak7")
    
    # get ingredients for ak7_1bin unfolding
    hResponse_1bin = fm.Get("rur_ak7w_1bin")
    hMeas_1bin = fm.Get("h_ak7_mass_1bin")
    hTrue_1bin = fm.Get("h_ak7g_mass_1bin")
    hData_1bin = fd.Get("h_ak7_mass_1bin")
    hMeas.SetTitle("; jet mass (jet pT [125-200]);")
    doUnfolding_closure(hResponse_1bin, hMeas_1bin, hTrue_1bin, figdir+"/unfolding_closure_ak7_1bin")
    doUnfolding_data(hResponse_1bin, hMeas_1bin, hTrue_1bin, hData_1bin, figdir+"/unfolding_data_ak7_1bin")

    # get ingredients for ak7_2bin unfolding
    hResponse_2bin = fm.Get("rur_ak7w_2bin")
    hMeas_2bin = fm.Get("h_ak7_mass_2bin")
    hTrue_2bin = fm.Get("h_ak7g_mass_2bin")
    hData_2bin = fd.Get("h_ak7_mass_2bin")
    hMeas.SetTitle("; jet mass (jet pT [200-300]);")
    doUnfolding_closure(hResponse_2bin, hMeas_2bin, hTrue_2bin, figdir+"/unfolding_closure_ak7_2bin")
    doUnfolding_data(hResponse_2bin, hMeas_2bin, hTrue_2bin, hData_2bin, figdir+"/unfolding_data_ak7_2bin")

    # get ingredients for ak7_3bin unfolding
    hResponse_3bin = fm.Get("rur_ak7w_3bin")
    hMeas_3bin = fm.Get("h_ak7_mass_3bin")
    hTrue_3bin = fm.Get("h_ak7g_mass_3bin")
    hData_3bin = fd.Get("h_ak7_mass_3bin")
    hMeas.SetTitle("; jet mass (jet pT [300-400]);")
    doUnfolding_closure(hResponse_3bin, hMeas_3bin, hTrue_3bin, figdir+"/unfolding_closure_ak7_3bin")
    doUnfolding_data(hResponse_3bin, hMeas_3bin, hTrue_3bin, hData_3bin, figdir+"/unfolding_data_ak7_3bin")

    # get ingredients for ak7_4bin unfolding
    hResponse_4bin = fm.Get("rur_ak7w_4bin")
    hMeas_4bin = fm.Get("h_ak7_mass_4bin")
    hTrue_4bin = fm.Get("h_ak7g_mass_4bin")
    hData_4bin = fd.Get("h_ak7_mass_4bin")
    hMeas.SetTitle("; jet mass (jet pT [400-500]);")
    doUnfolding_closure(hResponse_4bin, hMeas_4bin, hTrue_4bin, figdir+"/unfolding_closure_ak7_4bin")
    doUnfolding_data(hResponse_4bin, hMeas_4bin, hTrue_4bin, hData_4bin, figdir+"/unfolding_data_ak7_4bin")

def plotter_unfolding_MCcomp(mcname1, mcname2, dataname,figdir):
    
    fm1 = ROOT.TFile(mcname1)
    fm2 = ROOT.TFile(mcname2)
    fd = ROOT.TFile(dataname)
    
    # get ingredients for ak7 unfolding
    hResponse = fm1.Get("rur_ak7w")
    hMeas = fm1.Get("h_ak7_mass")
    hTrue = fm1.Get("h_ak7g_mass")
    hData = fd.Get("h_ak7_mass")
    hMC2_Meas = fm2.Get("h_ak7_mass")
    hMeas.SetTitle("; jet mass;")
    doUnfolding_closure(hResponse, hMeas, hTrue, figdir+"/unfolding_closure_ak7")
    doUnfolding_data_MCcomp(hResponse, hMeas, hTrue, hData, hMeas, hMC2_Meas, figdir+"/unfolding_data_ak7")
    
    # get ingredients for ak7_1bin unfolding    
    hResponse_1bin = fm1.Get("rur_ak7w_1bin")
    hMeas_1bin = fm1.Get("h_ak7_mass")
    hTrue_1bin = fm1.Get("h_ak7g_mass")
    hData_1bin = fd.Get("h_ak7_mass")
    hMC2_Meas_1bin = fm2.Get("h_ak7_mass")
    hMeas_1bin.SetTitle("; jet mass (jet pT [125-200]);")
    doUnfolding_closure(hResponse_1bin, hMeas_1bin, hTrue_1bin, figdir+"/unfolding_closure_ak7")
    doUnfolding_data_MCcomp(hResponse_1bin, hMeas_1bin, hTrue_1bin, hData_1bin, hMeas_1bin, hMC2_Meas_1bin, figdir+"/unfolding_data_ak7_1bin")
    
    # get ingredients for ak7_2bin unfolding    
    hResponse_2bin = fm1.Get("rur_ak7w_2bin")
    hMeas_2bin = fm1.Get("h_ak7_mass")
    hTrue_2bin = fm1.Get("h_ak7g_mass")
    hData_2bin = fd.Get("h_ak7_mass")
    hMC2_Meas_2bin = fm2.Get("h_ak7_mass")
    hMeas_2bin.SetTitle("; jet mass (jet pT [125-200]);")
    doUnfolding_closure(hResponse_2bin, hMeas_2bin, hTrue_2bin, figdir+"/unfolding_closure_ak7")
    doUnfolding_data_MCcomp(hResponse_2bin, hMeas_2bin, hTrue_2bin, hData_2bin, hMeas_2bin, hMC2_Meas_2bin, figdir+"/unfolding_data_ak7_2bin")

    # get ingredients for ak7_3bin unfolding    
    hResponse_3bin = fm1.Get("rur_ak7w_3bin")
    hMeas_3bin = fm1.Get("h_ak7_mass")
    hTrue_3bin = fm1.Get("h_ak7g_mass")
    hData_3bin = fd.Get("h_ak7_mass")
    hMC2_Meas_3bin = fm2.Get("h_ak7_mass")
    hMeas_3bin.SetTitle("; jet mass (jet pT [125-200]);")
    doUnfolding_closure(hResponse_3bin, hMeas_3bin, hTrue_3bin, figdir+"/unfolding_closure_ak7")
    doUnfolding_data_MCcomp(hResponse_3bin, hMeas_3bin, hTrue_3bin, hData_3bin, hMeas_3bin, hMC2_Meas_3bin, figdir+"/unfolding_data_ak7_3bin")

    # get ingredients for ak7_4bin unfolding    
    hResponse_4bin = fm1.Get("rur_ak7w_4bin")
    hMeas_4bin = fm1.Get("h_ak7_mass")
    hTrue_4bin = fm1.Get("h_ak7g_mass")
    hData_4bin = fd.Get("h_ak7_mass")
    hMC2_Meas_4bin = fm2.Get("h_ak7_mass")
    hMeas_4bin.SetTitle("; jet mass (jet pT [125-200]);")
    doUnfolding_closure(hResponse_4bin, hMeas_4bin, hTrue_4bin, figdir+"/unfolding_closure_ak7")
    doUnfolding_data_MCcomp(hResponse_4bin, hMeas_4bin, hTrue_4bin, hData_4bin, hMeas_4bin, hMC2_Meas_4bin, figdir+"/unfolding_data_ak7_4bin")

def plotter_unfolding_MCcomp_V3(fileWithResponseMatrices, mcname1, mcname2, dataname,figdir):
    
    fm1 = ROOT.TFile(mcname1)
    fm2 = ROOT.TFile(mcname2)
    fd = ROOT.TFile(dataname)
    fr = ROOT.TFile(fileWithResponseMatrices)
    

    responsejets = ["ak7tr","ak7ft","ak7pr"]
    groomedjets = ["ak7tr","ak7ft","ak7pr"]
    
    for x in range(len(groomedjets)):
    
        # get ingredients for ak7 unfolding
        hResponse = fr.Get("rur_"+responsejets[x]+"w")
        hMeas = fm1.Get("h_"+responsejets[x]+"_mass")
        hTrue = fm1.Get("h_"+responsejets[x]+"g_mass")
        hData = fd.Get("h_"+groomedjets[x]+"_mass")
        hMC1_Meas = fm1.Get("h_"+groomedjets[x]+"_mass")
        hMC2_Meas = fm2.Get("h_"+groomedjets[x]+"_mass")
        hMeas.SetTitle("; jet mass;")
#        doUnfolding_closure(hResponse, hMeas, hTrue, figdir+"/unfolding_closure_"+groomedjets[x]+"")
        doUnfolding_data_MCcomp(hResponse, hMeas, hTrue, hData, hMC1_Meas, hMC2_Meas, figdir+"/unfolding_data_"+groomedjets[x]+"")
        
        # get ingredients for ak7_1bin unfolding    
        hResponse_1bin = fm1.Get("rur_"+responsejets[x]+"w_1bin")
        hMeas_1bin = fm1.Get("h_"+responsejets[x]+"_mass_1bin")
        hTrue_1bin = fm1.Get("h_"+responsejets[x]+"g_mass_1bin")
        hData_1bin = fd.Get("h_"+groomedjets[x]+"_mass_1bin")
        hMC1_Meas_1bin = fm1.Get("h_"+groomedjets[x]+"_mass_1bin")
        hMC2_Meas_1bin = fm2.Get("h_"+groomedjets[x]+"_mass_1bin")
        hMeas_1bin.SetTitle("; jet mass (jet pT [125-200]);")
#        doUnfolding_closure(hResponse_1bin, hMeas_1bin, hTrue_1bin, figdir+"/unfolding_closure_"+groomedjets[x]+"")
        doUnfolding_data_MCcomp(hResponse_1bin, hMeas_1bin, hTrue_1bin, hData_1bin, hMC1_Meas_1bin, hMC2_Meas_1bin, figdir+"/unfolding_data_"+groomedjets[x]+"_1bin")
        
        # get ingredients for ak7_2bin unfolding    
        hResponse_2bin = fm1.Get("rur_"+responsejets[x]+"w_2bin")
        hMeas_2bin = fm1.Get("h_"+responsejets[x]+"_mass_2bin")
        hTrue_2bin = fm1.Get("h_"+responsejets[x]+"g_mass_2bin")
        hData_2bin = fd.Get("h_"+groomedjets[x]+"_mass_2bin")
        hMC1_Meas_2bin = fm1.Get("h_"+groomedjets[x]+"_mass_2bin")
        hMC2_Meas_2bin = fm2.Get("h_"+groomedjets[x]+"_mass_2bin")
        hMeas_2bin.SetTitle("; jet mass (jet pT [125-200]);")
#        doUnfolding_closure(hResponse_2bin, hMeas_2bin, hTrue_2bin, figdir+"/unfolding_closure_"+groomedjets[x]+"")
        doUnfolding_data_MCcomp(hResponse_2bin, hMeas_2bin, hTrue_2bin, hData_2bin, hMC1_Meas_2bin, hMC2_Meas_2bin, figdir+"/unfolding_data_"+groomedjets[x]+"_2bin")
        
        # get ingredients for ak7_3bin unfolding    
        hResponse_3bin = fm1.Get("rur_"+responsejets[x]+"w_3bin")
        hMeas_3bin = fm1.Get("h_"+responsejets[x]+"_mass_3bin")
        hTrue_3bin = fm1.Get("h_"+responsejets[x]+"g_mass_3bin")
        hData_3bin = fd.Get("h_"+groomedjets[x]+"_mass_3bin")
        hMC1_Meas_3bin = fm1.Get("h_"+groomedjets[x]+"_mass_3bin")
        hMC2_Meas_3bin = fm2.Get("h_"+groomedjets[x]+"_mass_3bin")
        hMeas_3bin.SetTitle("; jet mass (jet pT [125-200]);")
#        doUnfolding_closure(hResponse_3bin, hMeas_3bin, hTrue_3bin, figdir+"/unfolding_closure_"+groomedjets[x]+"")
        doUnfolding_data_MCcomp(hResponse_3bin, hMeas_3bin, hTrue_3bin, hData_3bin, hMC1_Meas_3bin, hMC2_Meas_3bin, figdir+"/unfolding_data_"+groomedjets[x]+"_3bin")
        
        # get ingredients for ak7_4bin unfolding    
        hResponse_4bin = fm1.Get("rur_"+responsejets[x]+"w_4bin")
        hMeas_4bin = fm1.Get("h_"+responsejets[x]+"_mass_4bin")
        hTrue_4bin = fm1.Get("h_"+responsejets[x]+"g_mass_4bin")
        hData_4bin = fd.Get("h_"+groomedjets[x]+"_mass_4bin")
        hMC1_Meas_4bin = fm1.Get("h_"+groomedjets[x]+"_mass_4bin")
        hMC2_Meas_4bin = fm2.Get("h_"+groomedjets[x]+"_mass_4bin")
        hMeas_4bin.SetTitle("; jet mass (jet pT [125-200]);")
#        doUnfolding_closure(hResponse_4bin, hMeas_4bin, hTrue_4bin, figdir+"/unfolding_closure_"+groomedjets[x]+"")
        doUnfolding_data_MCcomp(hResponse_4bin, hMeas_4bin, hTrue_4bin, hData_4bin, hMC1_Meas_4bin, hMC2_Meas_4bin, figdir+"/unfolding_data_"+groomedjets[x]+"_4bin")




