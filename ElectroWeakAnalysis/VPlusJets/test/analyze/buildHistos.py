from ROOT import gROOT, gStyle, gSystem, TLatex
import subprocess

############################################################
############################################################

def buildHistos(dirname,oname,isData,scaleFactors,channel):

    # Import everything from ROOT
    import ROOT
    from glob import glob
    from array import array
        
#    ROOT.gSystem.Load('RooUnfold-1.1.1/libRooUnfold.so')
#    from ROOT import RooUnfoldResponse
    
    print isData
    
    # IMPORTANT FOR GETTING CORRECT ERROR BARS
    ROOT.TH1.SetDefaultSumw2()
    
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
    
    #################### --------- special ----------
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
    #################### --------- special ----------
    
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
    
    isV3MC = False

    if isData[0]== 0: 
        if dirname[0].find("WJets_boostedMadGraph") > 0 or dirname[0].find("ZJets_boostedMadGraph") > 0:
            jtypes = jtypes_mv3
            jtypetrans = jtypetrans_mv3
            jtypesToI = jtypesToI_mv3   
            isV3MC = True
            print "here in MC, v3"
        else:
            jtypes = jtypes_m
            jtypetrans = jtypetrans_m
            jtypesToI = jtypesToI_m    
            print "here in MC, v2"
    if isData[0] > 0: 
        jtypes = jtypes_d
        jtypetrans = jtypetrans_d
        jtypesToI = jtypesToI_d    
        print "here in Data"    

    pt_binLo = [125,125,150,200,300]
    pt_binHi = [1000,150,200,300,1000]
    
    ooo = oname+"_ch"+str(channel)+".root"
    fo = ROOT.TFile(ooo, "recreate")

    # ------------------------------------------------------
    ##### setting up the output histograms
    from ROOT import TH1F, TProfile
    # event quantities
    h_v_pt = ROOT.TH1F("h_v_pt","; V pT; count",50,100,500.)
    h_v_mass = ROOT.TH1F("h_v_mass","; V mass; count",30,75,105.)
    h_v_mt = ROOT.TH1F("h_v_mt","; V mT; count",50,50.,300.)
    h_e_met = ROOT.TH1F("h_e_met","; MET; count",30,0.,300.)   
    h_e_nvert = ROOT.TH1F("h_e_nvert","; nvertex; count",40,0.,40.)   
    h_e_nvert_weighted = ROOT.TH1F("h_e_nvert_weighted","; nvertex; count",40,0.,40.)   
    h_l_pt = ROOT.TH1F("h_l_pt","; lepton pT; count",100,0.,400.)
    h_l_eta = ROOT.TH1F("h_l_eta","; lepton eta; count",30,-3.,3.)
    h_lplus_pt = ROOT.TH1F("h_lplus_pt","; lepton pT; count",100,0.,400.)
    h_lplus_eta = ROOT.TH1F("h_lplus_eta","; lepton eta; count",30,-3.,3.)
    h_e_PU = ROOT.TH1F("h_e_PU","; pu weight; count", 100,0,2)

    # special jet quantities
    h_ca12ft_mass_Wtagged = ROOT.TH1F("h_ca12ft_mass_Wtagged","; ca12ft jet mass (W-tagged);",60,0,300)
    h_ca12ft_mass_toptagged = ROOT.TH1F("h_ca12ft_mass_toptagged","; ca12ft jet mass (top-tagged);",60,0,300)
    h_ca8pr_mass_Wtagged = ROOT.TH1F("h_ca8pr_mass_Wtagged","; ca8pr jet mass (W-tagged);",30,0,150)
    h_ca8pr_massdrop = ROOT.TH1F("h_ca8pr_massdrop","; ca8pr jet mass drop (W-tagged);",25,0,1)

    # individual response matrices
    rur_ak7w = ROOT.TH2F("rur_ak7w","rur_ak7w",60, 0., 300., 60, 0., 300.); 
    rur_ak7w_0bin = ROOT.TH2F("rur_ak7w_0bin","rur_ak7w_0bin",60, 0., 300., 60, 0., 300.);
    rur_ak7w_1bin = ROOT.TH2F("rur_ak7w_1bin","rur_ak7w_1bin",60, 0., 300., 60, 0., 300.);    
    rur_ak7w_2bin = ROOT.TH2F("rur_ak7w_2bin","rur_ak7w_2bin",60, 0., 300., 60, 0., 300.);
    rur_ak7w_4bin = ROOT.TH2F("rur_ak7w_4bin","rur_ak7w_4bin",60, 0., 300., 60, 0., 300.);  
    rur_ak7w_3bin = ROOT.TH2F("rur_ak7w_3bin","rur_ak7w_3bin",60, 0., 300., 60, 0., 300.);

    # individual response matrices, groomed gen jets
    rur_ak7trw = ROOT.TH2F("rur_ak7trw","rur_ak7trw",60, 0., 300., 60, 0., 300.); 
    rur_ak7trw_0bin = ROOT.TH2F("rur_ak7trw_0bin","rur_ak7trw_0bin",60, 0., 300., 60, 0., 300.);
    rur_ak7trw_1bin = ROOT.TH2F("rur_ak7trw_1bin","rur_ak7trw_1bin",60, 0., 300., 60, 0., 300.);    
    rur_ak7trw_2bin = ROOT.TH2F("rur_ak7trw_2bin","rur_ak7trw_2bin",60, 0., 300., 60, 0., 300.);
    rur_ak7trw_3bin = ROOT.TH2F("rur_ak7trw_3bin","rur_ak7trw_3bin",60, 0., 300., 60, 0., 300.);
    rur_ak7trw_4bin = ROOT.TH2F("rur_ak7trw_4bin","rur_ak7trw_4bin",60, 0., 300., 60, 0., 300.);  
    rur_ak7ftw = ROOT.TH2F("rur_ak7ftw","rur_ak7ftw",60, 0., 300., 60, 0., 300.); 
    rur_ak7ftw_0bin = ROOT.TH2F("rur_ak7ftw_0bin","rur_ak7ftw_0bin",60, 0., 300., 60, 0., 300.);
    rur_ak7ftw_1bin = ROOT.TH2F("rur_ak7ftw_1bin","rur_ak7ftw_1bin",60, 0., 300., 60, 0., 300.);    
    rur_ak7ftw_2bin = ROOT.TH2F("rur_ak7ftw_2bin","rur_ak7ftw_2bin",60, 0., 300., 60, 0., 300.);
    rur_ak7ftw_3bin = ROOT.TH2F("rur_ak7ftw_3bin","rur_ak7ftw_3bin",60, 0., 300., 60, 0., 300.);
    rur_ak7ftw_4bin = ROOT.TH2F("rur_ak7ftw_4bin","rur_ak7ftw_4bin",60, 0., 300., 60, 0., 300.);  
    rur_ak7prw = ROOT.TH2F("rur_ak7prw","rur_ak7prw",60, 0., 300., 60, 0., 300.); 
    rur_ak7prw_0bin = ROOT.TH2F("rur_ak7prw_0bin","rur_ak7prw_0bin",60, 0., 300., 60, 0., 300.);
    rur_ak7prw_1bin = ROOT.TH2F("rur_ak7prw_1bin","rur_ak7prw_1bin",60, 0., 300., 60, 0., 300.);    
    rur_ak7prw_2bin = ROOT.TH2F("rur_ak7prw_2bin","rur_ak7prw_2bin",60, 0., 300., 60, 0., 300.);
    rur_ak7prw_3bin = ROOT.TH2F("rur_ak7prw_3bin","rur_ak7prw_3bin",60, 0., 300., 60, 0., 300.);
    rur_ak7prw_4bin = ROOT.TH2F("rur_ak7prw_4bin","rur_ak7prw_4bin",60, 0., 300., 60, 0., 300.);  

#    hunf_ak7_mass = ROOT.TH1F("hunf_ak7_mass","; ak7 jet mass;",60, 0., 300.)
#    hunf_ak7g_mass = ROOT.TH1F("hunf_ak7g_mass","; ak7 jet mass;",60, 0., 300.)
    rur_ak7w_closure = ROOT.TH2F("rur_ak7w_closure","rur_ak7w_closure",60, 0., 300., 60, 0., 300.);
    hunfw_ak7_mass_closure = ROOT.TH1F("hunfw_ak7_mass_closure","; ak7 jet mass;",60, 0., 300.)
    hunfw_ak7g_mass_closure = ROOT.TH1F("hunfw_ak7g_mass_closure","; ak7 jet mass;",60, 0., 300.)
#    hunfw_ak7_mass_0bin = ROOT.TH1F("hunfw_ak7_mass_0bin","; ak7 jet mass;",60, 0., 300.)
#    hunfw_ak7g_mass_0bin = ROOT.TH1F("hunfw_ak7g_mass_0bin","; ak7 jet mass;",60, 0., 300.)
#    hunfw_ak7_mass_1bin = ROOT.TH1F("hunfw_ak7_mass_1bin","; ak7 jet mass;",60, 0., 300.)
#    hunfw_ak7g_mass_1bin = ROOT.TH1F("hunfw_ak7g_mass_1bin","; ak7 jet mass;",60, 0., 300.)
#    hunfw_ak7_mass_2bin = ROOT.TH1F("hunfw_ak7_mass_2bin","; ak7 jet mass;",60, 0., 300.)
#    hunfw_ak7g_mass_2bin = ROOT.TH1F("hunfw_ak7g_mass_2bin","; ak7 jet mass;",60, 0., 300.)
#    hunfw_ak7_mass_3bin = ROOT.TH1F("hunfw_ak7_mass_3bin","; ak7 jet mass;",60, 0., 300.)
#    hunfw_ak7g_mass_3bin = ROOT.TH1F("hunfw_ak7g_mass_3bin","; ak7 jet mass;",60, 0., 300.)
#    hunfw_ak7_mass_4bin = ROOT.TH1F("hunfw_ak7_mass_4bin","; ak7 jet mass;",60, 0., 300.)
#    hunfw_ak7g_mass_4bin = ROOT.TH1F("hunfw_ak7g_mass_4bin","; ak7 jet mass;",60, 0., 300.)

    # per jet type quantities
    """
    h_mass = [] # ! this is a 2D in bins of pT and jet type !
    hrat_mass = [] # ! this is a 2D in bins of pT and jet type ! 
    prat_mass_vPt = [] # ! this is a 2D in bins of pT and jet type ! 
    prat_pt_vPt = [] # ! this is a 2D in bins of pT and jet type ! 
    """
    h_mass = []
    h_mass_0bin = []
    h_mass_1bin = []
    h_mass_2bin = []
    h_mass_3bin = []
    h_mass_4bin = []
    
    prPt_mass = []
    prNV_mass = []
    prEta_mass = []
    
    hrat_mass_ovAK5 = []    
    hrat_mass_ovAK5g = []    
    hrat_mass_ovAK7 = []    
    hrat_mass_ovAK7g = []    
    hrat_mass_ovAK8 = []    
    hrat_mass_ovAK8g = []    
    hrat_mass_ovCA8 = []    
    hrat_mass_ovCA8g = []    

    hrat_pt_ovAK5 = []    
    hrat_pt_ovAK5g = []    
    hrat_pt_ovAK7 = []    
    hrat_pt_ovAK7g = []    
    hrat_pt_ovAK8 = []    
    hrat_pt_ovAK8g = []    
    hrat_pt_ovCA8 = []    
    hrat_pt_ovCA8g = []            
        
    # profile, ratio of mass, vs pT
    prPt_mass_ovAK5 = []    
    prPt_mass_ovAK5g = []    
    prPt_mass_ovAK7 = []    
    prPt_mass_ovAK7g = []    
    prPt_mass_ovAK8 = []    
    prPt_mass_ovAK8g = []    
    prPt_mass_ovCA8 = []    
    prPt_mass_ovCA8g = []    
    # profile, ratio of pt, vs pT
    prPt_pt_ovAK5 = []    
    prPt_pt_ovAK5g = []    
    prPt_pt_ovAK7 = []    
    prPt_pt_ovAK7g = []    
    prPt_pt_ovAK8 = []    
    prPt_pt_ovAK8g = []    
    prPt_pt_ovCA8 = []    
    prPt_pt_ovCA8g = []    

    # profile, ratio of mass, vs nV
    prNV_mass_ovAK5 = []    
    prNV_mass_ovAK5g = []    
    prNV_mass_ovAK7 = []    
    prNV_mass_ovAK7g = []    
    prNV_mass_ovAK8 = []    
    prNV_mass_ovAK8g = []    
    prNV_mass_ovCA8 = []    
    prNV_mass_ovCA8g = []    
    # profile, ratio of pt, vs nV
    prNV_pt_ovAK5 = []    
    prNV_pt_ovAK5g = []    
    prNV_pt_ovAK7 = []    
    prNV_pt_ovAK7g = []    
    prNV_pt_ovAK8 = []    
    prNV_pt_ovAK8g = []    
    prNV_pt_ovCA8 = []    
    prNV_pt_ovCA8g = []    
    
    # profile, ratio of mass, vs nV
    prEta_mass_ovAK5 = []    
    prEta_mass_ovAK5g = []    
    prEta_mass_ovAK7 = []    
    prEta_mass_ovAK7g = []    
    prEta_mass_ovAK8 = []    
    prEta_mass_ovAK8g = []    
    prEta_mass_ovCA8 = []    
    prEta_mass_ovCA8g = []    
    # profile, ratio of pt, vs nV
    prEta_pt_ovAK5 = []    
    prEta_pt_ovAK5g = []    
    prEta_pt_ovAK7 = []    
    prEta_pt_ovAK7g = []    
    prEta_pt_ovAK8 = []    
    prEta_pt_ovAK8g = []    
    prEta_pt_ovCA8 = []    
    prEta_pt_ovCA8g = []    

    #############
    # ak7 groomed GEN jets
    hrat_mass_ovAK7trg = []    
    hrat_pt_ovAK7trg = []    
    prPt_mass_ovAK7trg = []    
    prPt_pt_ovAK7trg = []    
    prNV_mass_ovAK7trg = []    
    prNV_pt_ovAK7trg = []    
    prEta_mass_ovAK7trg = []    
    prEta_pt_ovAK7trg = []    

    hrat_mass_ovAK7ftg = []    
    hrat_pt_ovAK7ftg = []    
    prPt_mass_ovAK7ftg = []    
    prPt_pt_ovAK7ftg = []    
    prNV_mass_ovAK7ftg = []    
    prNV_pt_ovAK7ftg = []    
    prEta_mass_ovAK7ftg = []    
    prEta_pt_ovAK7ftg = []    

    hrat_mass_ovAK7prg = []    
    hrat_pt_ovAK7prg = []    
    prPt_mass_ovAK7prg = []    
    prPt_pt_ovAK7prg = []    
    prNV_mass_ovAK7prg = []    
    prNV_pt_ovAK7prg = []    
    prEta_mass_ovAK7prg = []    
    prEta_pt_ovAK7prg = []    
    #############
        
    h_pt = []
    h_area = []   
    h_eta = []
    
    pr_ptBins = array( 'd', [ 125,150,175,200,225,250,275,300,350,425,500 ] )
    #pr_ptBins = [ 125,150,200,300,1000 ]
    npr_ptBins = 10
    for x in range(len(jtypes)):
        h_eta.append( ROOT.TH1F("h_"+jtypes[x]+"_eta",";jet eta; count",60,-3,3) )
        h_area.append( ROOT.TH1F("h_"+jtypes[x]+"_area",";jet area; count",150,0.,3.) )
        h_pt.append( ROOT.TH1F("h_"+jtypes[x]+"_pt",";jet pt; count",100,0,600) )
        # in bins of pT
        h_mass.append( ROOT.TH1F( "h_"+jtypes[x]+"_mass",";jet mass; count",60,0.,300 ))
        h_mass_0bin.append( ROOT.TH1F( "h_"+jtypes[x]+"_mass_0bin",";jet mass; count",60,0.,300 ))
        h_mass_1bin.append( ROOT.TH1F( "h_"+jtypes[x]+"_mass_1bin",";jet mass; count",60,0.,300 ))        
        h_mass_2bin.append( ROOT.TH1F( "h_"+jtypes[x]+"_mass_2bin",";jet mass; count",60,0.,300 ))        
        h_mass_3bin.append( ROOT.TH1F( "h_"+jtypes[x]+"_mass_3bin",";jet mass; count",60,0.,300 ))        
        h_mass_4bin.append( ROOT.TH1F( "h_"+jtypes[x]+"_mass_4bin",";jet mass; count",60,0.,300 ))  
        
        prPt_mass.append( ROOT.TH2F("prPt_mass_"+jtypes[x],"; pT; < jet mass >",npr_ptBins,pr_ptBins,300,0.,300.) )
        prNV_mass.append( ROOT.TH2F("prNV_mass_"+jtypes[x],"; pT; < jet mass >",40,0,40,300,0.,300.) )
        prEta_mass.append( ROOT.TH2F("prEta_mass_"+jtypes[x],"; pT; < jet mass >",10,-2.5,2.5,300,0.,300.) )
        
        # 1D case of mass ratios
        hrat_mass_ovAK5.append( ROOT.TH1F( "hrat_"+jtypes[x]+"_mass_ovAK5",";jet mass; count",150,0.,3. ))
        hrat_mass_ovAK5g.append( ROOT.TH1F( "hrat_"+jtypes[x]+"_mass_ovAK5g",";jet mass; count",150,0.,3. ))
        hrat_mass_ovAK7.append( ROOT.TH1F( "hrat_"+jtypes[x]+"_mass_ovAK7",";jet mass; count",150,0.,3. ))
        hrat_mass_ovAK7g.append( ROOT.TH1F( "hrat_"+jtypes[x]+"_mass_ovAK7g",";jet mass; count",150,0.,3. ))
        hrat_mass_ovAK8.append( ROOT.TH1F( "hrat_"+jtypes[x]+"_mass_ovAK8",";jet mass; count",150,0.,3. ))
        hrat_mass_ovAK8g.append( ROOT.TH1F( "hrat_"+jtypes[x]+"_mass_ovAK8g",";jet mass; count",150,0.,3. ))
        hrat_mass_ovCA8.append( ROOT.TH1F( "hrat_"+jtypes[x]+"_mass_ovCA8",";jet mass; count",150,0.,3. ))
        hrat_mass_ovCA8g.append( ROOT.TH1F( "hrat_"+jtypes[x]+"_mass_ovCA8g",";jet mass; count",150,0.,3. ))
        # 1D case of mass ratios
        hrat_pt_ovAK5.append( ROOT.TH1F( "hrat_"+jtypes[x]+"_pt_ovAK5",";jet mass; count",150,0.,3. ))
        hrat_pt_ovAK5g.append( ROOT.TH1F( "hrat_"+jtypes[x]+"_pt_ovAK5g",";jet mass; count",150,0.,3. ))
        hrat_pt_ovAK7.append( ROOT.TH1F( "hrat_"+jtypes[x]+"_pt_ovAK7",";jet mass; count",150,0.,3. ))
        hrat_pt_ovAK7g.append( ROOT.TH1F( "hrat_"+jtypes[x]+"_pt_ovAK7g",";jet mass; count",150,0.,3. ))
        hrat_pt_ovAK8.append( ROOT.TH1F( "hrat_"+jtypes[x]+"_pt_ovAK8",";jet mass; count",150,0.,3. ))
        hrat_pt_ovAK8g.append( ROOT.TH1F( "hrat_"+jtypes[x]+"_pt_ovAK8g",";jet mass; count",150,0.,3. ))
        hrat_pt_ovCA8.append( ROOT.TH1F( "hrat_"+jtypes[x]+"_pt_ovCA8",";jet mass; count",150,0.,3. ))
        hrat_pt_ovCA8g.append( ROOT.TH1F( "hrat_"+jtypes[x]+"_pt_ovCA8g",";jet mass; count",150,0.,3. ))
        # TProfile because they are non-gaussian distributions
        prPt_mass_ovAK5.append( ROOT.TH2F("prPt_mass"+jtypes[x]+"_ovAK5","; pT; ratio of masses",npr_ptBins,pr_ptBins,150,0.,3.) )
        prPt_mass_ovAK5g.append( ROOT.TH2F("prPt_mass"+jtypes[x]+"_ovAK5g","; pT; ratio of masses",npr_ptBins,pr_ptBins,150,0.,3.) )        
        prPt_mass_ovAK7.append( ROOT.TH2F("prPt_mass"+jtypes[x]+"_ovAK7","; pT; ratio of masses",npr_ptBins,pr_ptBins,150,0.,3.) )
        prPt_mass_ovAK7g.append( ROOT.TH2F("prPt_mass"+jtypes[x]+"_ovAK7g","; pT; ratio of masses",npr_ptBins,pr_ptBins,150,0.,3.) )
        prPt_mass_ovAK8.append( ROOT.TH2F("prPt_mass"+jtypes[x]+"_ovAK8","; pT; ratio of masses",npr_ptBins,pr_ptBins,150,0.,3.) )
        prPt_mass_ovAK8g.append( ROOT.TH2F("prPt_mass"+jtypes[x]+"_ovAK8g","; pT; ratio of masses",npr_ptBins,pr_ptBins,150,0.,3.) )
        prPt_mass_ovCA8.append( ROOT.TH2F("prPt_mass"+jtypes[x]+"_ovCA8","; pT; ratio of masses",npr_ptBins,pr_ptBins,150,0.,3.) )
        prPt_mass_ovCA8g.append( ROOT.TH2F("prPt_mass"+jtypes[x]+"_ovCA8g","; pT; ratio of masses",npr_ptBins,pr_ptBins,150,0.,3.) )
        # TH2F in fit slices
        prPt_pt_ovAK5.append( ROOT.TH2F("prPt_pt"+jtypes[x]+"_ovAK5","; pT; ratio of masses",npr_ptBins,pr_ptBins,150,0.,3.) )
        prPt_pt_ovAK5g.append( ROOT.TH2F("prPt_pt"+jtypes[x]+"_ovAK5g","; pT; ratio of masses",npr_ptBins,pr_ptBins,150,0.,3.) )        
        prPt_pt_ovAK7.append( ROOT.TH2F("prPt_pt"+jtypes[x]+"_ovAK7","; pT; ratio of masses",npr_ptBins,pr_ptBins,150,0.,3.) )
        prPt_pt_ovAK7g.append( ROOT.TH2F("prPt_pt"+jtypes[x]+"_ovAK7g","; pT; ratio of masses",npr_ptBins,pr_ptBins,150,0.,3.) )
        prPt_pt_ovAK8.append( ROOT.TH2F("prPt_pt"+jtypes[x]+"_ovAK8","; pT; ratio of masses",npr_ptBins,pr_ptBins,150,0.,3.) )
        prPt_pt_ovAK8g.append( ROOT.TH2F("prPt_pt"+jtypes[x]+"_ovAK8g","; pT; ratio of masses",npr_ptBins,pr_ptBins,150,0.,3.) )
        prPt_pt_ovCA8.append( ROOT.TH2F("prPt_pt"+jtypes[x]+"_ovCA8","; pT; ratio of masses",npr_ptBins,pr_ptBins,150,0.,3.) )
        prPt_pt_ovCA8g.append( ROOT.TH2F("prPt_pt"+jtypes[x]+"_ovCA8g","; pT; ratio of masses",npr_ptBins,pr_ptBins,150,0.,3.) )
        # TProfile because they are non-gaussian distributions, versus NV
        prNV_mass_ovAK5.append( ROOT.TH2F("prNV_mass"+jtypes[x]+"_ovAK5","; nV; ratio of masses",40,0,40,150,0.,3.) )
        prNV_mass_ovAK5g.append( ROOT.TH2F("prNV_mass"+jtypes[x]+"_ovAK5g","; nV; ratio of masses",40,0,40,150,0.,3.) )        
        prNV_mass_ovAK7.append( ROOT.TH2F("prNV_mass"+jtypes[x]+"_ovAK7","; nV; ratio of masses",40,0,40,150,0.,3.) )
        prNV_mass_ovAK7g.append( ROOT.TH2F("prNV_mass"+jtypes[x]+"_ovAK7g","; nV; ratio of masses",40,0,40,150,0.,3.) )
        prNV_mass_ovAK8.append( ROOT.TH2F("prNV_mass"+jtypes[x]+"_ovAK8","; nV; ratio of masses",40,0,40,150,0.,3.) )
        prNV_mass_ovAK8g.append( ROOT.TH2F("prNV_mass"+jtypes[x]+"_ovAK8g","; nV; ratio of masses",40,0,40,150,0.,3.) )
        prNV_mass_ovCA8.append( ROOT.TH2F("prNV_mass"+jtypes[x]+"_ovCA8","; nV; ratio of masses",40,0,40,150,0.,3.) )
        prNV_mass_ovCA8g.append( ROOT.TH2F("prNV_mass"+jtypes[x]+"_ovCA8g","; nV; ratio of masses",40,0,40,150,0.,3.) )
        # TH2F in fit slices
        prNV_pt_ovAK5.append( ROOT.TH2F("prNV_pt"+jtypes[x]+"_ovAK5","; nV; ratio of masses",40,0,40,150,0.,3.) )
        prNV_pt_ovAK5g.append( ROOT.TH2F("prNV_pt"+jtypes[x]+"_ovAK5g","; nV; ratio of masses",40,0,40,150,0.,3.) )        
        prNV_pt_ovAK7.append( ROOT.TH2F("prNV_pt"+jtypes[x]+"_ovAK7","; nV; ratio of masses",40,0,40,150,0.,3.) )
        prNV_pt_ovAK7g.append( ROOT.TH2F("prNV_pt"+jtypes[x]+"_ovAK7g","; nV; ratio of masses",40,0,40,150,0.,3.) )
        prNV_pt_ovAK8.append( ROOT.TH2F("prNV_pt"+jtypes[x]+"_ovAK8","; nV; ratio of masses",40,0,40,150,0.,3.) )
        prNV_pt_ovAK8g.append( ROOT.TH2F("prNV_pt"+jtypes[x]+"_ovAK8g","; nV; ratio of masses",40,0,40,150,0.,3.) )
        prNV_pt_ovCA8.append( ROOT.TH2F("prNV_pt"+jtypes[x]+"_ovCA8","; nV; ratio of masses",40,0,40,150,0.,3.) )
        prNV_pt_ovCA8g.append( ROOT.TH2F("prNV_pt"+jtypes[x]+"_ovCA8g","; nV; ratio of masses",40,0,40,150,0.,3.) )
        # TProfile because they are non-gaussian distributions, versus Eta
        prEta_mass_ovAK5.append( ROOT.TH2F("prEta_mass"+jtypes[x]+"_ovAK5","; eta; ratio of masses",10,-2.5,2.5,150,0.,3.) )
        prEta_mass_ovAK5g.append( ROOT.TH2F("prEta_mass"+jtypes[x]+"_ovAK5g","; eta; ratio of masses",10,-2.5,2.5,150,0.,3.) )        
        prEta_mass_ovAK7.append( ROOT.TH2F("prEta_mass"+jtypes[x]+"_ovAK7","; eta; ratio of masses",10,-2.5,2.5,150,0.,3.) )
        prEta_mass_ovAK7g.append( ROOT.TH2F("prEta_mass"+jtypes[x]+"_ovAK7g","; eta; ratio of masses",10,-2.5,2.5,150,0.,3.) )
        prEta_mass_ovAK8.append( ROOT.TH2F("prEta_mass"+jtypes[x]+"_ovAK8","; eta; ratio of masses",10,-2.5,2.5,150,0.,3.) )
        prEta_mass_ovAK8g.append( ROOT.TH2F("prEta_mass"+jtypes[x]+"_ovAK8g","; eta; ratio of masses",10,-2.5,2.5,150,0.,3.) )
        prEta_mass_ovCA8.append( ROOT.TH2F("prEta_mass"+jtypes[x]+"_ovCA8","; eta; ratio of masses",10,-2.5,2.5,150,0.,3.) )
        prEta_mass_ovCA8g.append( ROOT.TH2F("prEta_mass"+jtypes[x]+"_ovCA8g","; eta; ratio of masses",10,-2.5,2.5,150,0.,3.) )
        # TH2F in fit slices
        prEta_pt_ovAK5.append( ROOT.TH2F("prEta_pt"+jtypes[x]+"_ovAK5","; eta; ratio of masses",10,-2.5,2.5,150,0.,3.) )
        prEta_pt_ovAK5g.append( ROOT.TH2F("prEta_pt"+jtypes[x]+"_ovAK5g","; eta; ratio of masses",10,-2.5,2.5,150,0.,3.) )        
        prEta_pt_ovAK7.append( ROOT.TH2F("prEta_pt"+jtypes[x]+"_ovAK7","; eta; ratio of masses",10,-2.5,2.5,150,0.,3.) )
        prEta_pt_ovAK7g.append( ROOT.TH2F("prEta_pt"+jtypes[x]+"_ovAK7g","; eta; ratio of masses",10,-2.5,2.5,150,0.,3.) )
        prEta_pt_ovAK8.append( ROOT.TH2F("prEta_pt"+jtypes[x]+"_ovAK8","; eta; ratio of masses",10,-2.5,2.5,150,0.,3.) )
        prEta_pt_ovAK8g.append( ROOT.TH2F("prEta_pt"+jtypes[x]+"_ovAK8g","; eta; ratio of masses",10,-2.5,2.5,150,0.,3.) )
        prEta_pt_ovCA8.append( ROOT.TH2F("prEta_pt"+jtypes[x]+"_ovCA8","; eta; ratio of masses",10,-2.5,2.5,150,0.,3.) )
        prEta_pt_ovCA8g.append( ROOT.TH2F("prEta_pt"+jtypes[x]+"_ovCA8g","; eta; ratio of masses",10,-2.5,2.5,150,0.,3.) )
        
        if isV3MC:
            print "append for isV3MC!"  
            hrat_mass_ovAK7trg.append( ROOT.TH1F( "hrat_"+jtypes[x]+"_mass_ovAK7trg",";jet mass; count",150,0.,3. ))
            hrat_pt_ovAK7trg.append( ROOT.TH1F( "hrat_"+jtypes[x]+"_pt_ovAK7trg",";jet mass; count",150,0.,3. ))
            prPt_mass_ovAK7trg.append( ROOT.TH2F("prPt_mass"+jtypes[x]+"_ovAK7trg","; pT; ratio of masses",npr_ptBins,pr_ptBins,150,0.,3.) )
            prPt_pt_ovAK7trg.append( ROOT.TH2F("prPt_pt"+jtypes[x]+"_ovAK7trg","; pT; ratio of masses",npr_ptBins,pr_ptBins,150,0.,3.) )
            prNV_mass_ovAK7trg.append( ROOT.TH2F("prNV_mass"+jtypes[x]+"_ovAK7trg","; nV; ratio of masses",40,0,40,150,0.,3.) )
            prNV_pt_ovAK7trg.append( ROOT.TH2F("prNV_pt"+jtypes[x]+"_ovAK7trg","; nV; ratio of masses",40,0,40,150,0.,3.) )
            prEta_mass_ovAK7trg.append( ROOT.TH2F("prEta_mass"+jtypes[x]+"_ovAK7trg","; eta; ratio of masses",10,-2.5,2.5,150,0.,3.) )
            prEta_pt_ovAK7trg.append( ROOT.TH2F("prEta_pt"+jtypes[x]+"_ovAK7trg","; eta; ratio of masses",10,-2.5,2.5,150,0.,3.) )

            hrat_mass_ovAK7ftg.append( ROOT.TH1F( "hrat_"+jtypes[x]+"_mass_ovAK7ftg",";jet mass; count",150,0.,3. ))
            hrat_pt_ovAK7ftg.append( ROOT.TH1F( "hrat_"+jtypes[x]+"_pt_ovAK7ftg",";jet mass; count",150,0.,3. ))
            prPt_mass_ovAK7ftg.append( ROOT.TH2F("prPt_mass"+jtypes[x]+"_ovAK7ftg","; pT; ratio of masses",npr_ptBins,pr_ptBins,150,0.,3.) )
            prPt_pt_ovAK7ftg.append( ROOT.TH2F("prPt_pt"+jtypes[x]+"_ovAK7ftg","; pT; ratio of masses",npr_ptBins,pr_ptBins,150,0.,3.) )
            prNV_mass_ovAK7ftg.append( ROOT.TH2F("prNV_mass"+jtypes[x]+"_ovAK7ftg","; nV; ratio of masses",40,0,40,150,0.,3.) )
            prNV_pt_ovAK7ftg.append( ROOT.TH2F("prNV_pt"+jtypes[x]+"_ovAK7ftg","; nV; ratio of masses",40,0,40,150,0.,3.) )
            prEta_mass_ovAK7ftg.append( ROOT.TH2F("prEta_mass"+jtypes[x]+"_ovAK7ftg","; eta; ratio of masses",10,-2.5,2.5,150,0.,3.) )
            prEta_pt_ovAK7ftg.append( ROOT.TH2F("prEta_pt"+jtypes[x]+"_ovAK7ftg","; eta; ratio of masses",10,-2.5,2.5,150,0.,3.) )

            hrat_mass_ovAK7prg.append( ROOT.TH1F( "hrat_"+jtypes[x]+"_mass_ovAK7prg",";jet mass; count",150,0.,3. ))
            hrat_pt_ovAK7prg.append( ROOT.TH1F( "hrat_"+jtypes[x]+"_pt_ovAK7prg",";jet mass; count",150,0.,3. ))
            prPt_mass_ovAK7prg.append( ROOT.TH2F("prPt_mass"+jtypes[x]+"_ovAK7prg","; pT; ratio of masses",npr_ptBins,pr_ptBins,150,0.,3.) )
            prPt_pt_ovAK7prg.append( ROOT.TH2F("prPt_pt"+jtypes[x]+"_ovAK7prg","; pT; ratio of masses",npr_ptBins,pr_ptBins,150,0.,3.) )
            prNV_mass_ovAK7prg.append( ROOT.TH2F("prNV_mass"+jtypes[x]+"_ovAK7prg","; nV; ratio of masses",40,0,40,150,0.,3.) )
            prNV_pt_ovAK7prg.append( ROOT.TH2F("prNV_pt"+jtypes[x]+"_ovAK7prg","; nV; ratio of masses",40,0,40,150,0.,3.) )
            prEta_mass_ovAK7prg.append( ROOT.TH2F("prEta_mass"+jtypes[x]+"_ovAK7prg","; eta; ratio of masses",10,-2.5,2.5,150,0.,3.) )
            prEta_pt_ovAK7prg.append( ROOT.TH2F("prEta_pt"+jtypes[x]+"_ovAK7prg","; eta; ratio of masses",10,-2.5,2.5,150,0.,3.) )

        
        ### Fancy, but too slow
        """
        # vs jet types vs jet types
        hrat_mass_1d = []
        prat_mass_vPt_1d = []
        prat_pt_vPt_1d = []
            
        for y in range(len(pt_binLo)):
        h_mass_1d.append( ROOT.TH1F("h_"+jtypes[x]+"_mass_bin"+str(y),";jet mass; count",100,0.,200) )
        h_mass.append( h_mass_1d )
        """                           
        """
        for y in range(len(jtypes)):
            hrat_mass_1d.append( ROOT.TH1F("hrat_mass_"+jtypes[x]+"_over_"+jtypes[y],";jet mass; count",150,0.,3.) )
            prat_mass_vPt_1d.append( ROOT.TProfile("prat_mass_"+jtypes[y]+"_over_"+jtypes[x],"; pT; ratio of masses",npr_ptBins,pr_ptBins) )
            prat_pt_vPt_1d.append( ROOT.TProfile("prat_pt_"+jtypes[y]+"_over_"+jtypes[x],"; pT; ratio of masses",npr_ptBins,pr_ptBins) )
        hrat_mass.append( hrat_mass_1d )
        prat_mass_vPt.append( prat_mass_vPt_1d )
        prat_pt_vPt.append( prat_pt_vPt_1d )  
        """
        # ------------------------------------------------------
    
    for nfiles in xrange(len(dirname)):
        print  "setup has been done for inputs "+dirname[nfiles]+"\n"
        
        files = glob(dirname[nfiles]) 
        chain = ROOT.TChain("otree")
        for f in files: 
            chain.Add(f)
    
        entries = chain.GetEntries()
        print "total entries = " + str(entries)
    
        # +++++++++++++++++++++++++++++++++++++
        # per file loop
        for i in xrange(entries):
            if i%1000 == 0:   
                print "Entry: " + str(i)

            chain.GetEntry( i )
            # accumulate all the different event weights: MC scale factor, PU reweighting, trigger/ID reweighting

            curSF = scaleFactors[nfiles]*chain.e_puwt*chain.e_effwt
            if isData[nfiles] == 1: curSF = 1.
            curSF_noPUweight = scaleFactors[nfiles]*chain.e_effwt
#            curSF = scaleFactors[nfiles]*chain.e_puwt
#            if isData[nfiles] == 1: curSF = 1.
#            curSF_noPUweight = scaleFactors[nfiles]
#
#            print "curSF = ", curSF,", e_effwt = ", chain.e_effwt, ", puwt = ", chain.e_puwt

            # if chain.eventClass == 1:
            vptcut = 120.
            additionalCuts = False
            if channel == 1 and chain.e_met > 40 and chain.l_pt > 60 and chain.v_pt > vptcut:   
                additionalCuts = True
            if channel == 2 and chain.e_met > 30 and chain.l_pt > 30 and chain.v_pt > vptcut:   
                additionalCuts = True
            if channel == 3 and chain.e_met < 50 and chain.l_pt > 20 and chain.lplus_pt > 20 and chain.v_pt > vptcut:   
                additionalCuts = True
            if channel == 4 and chain.e_met < 50 and chain.l_pt > 25 and chain.lplus_pt > 25 and chain.v_pt > vptcut: 
                additionalCuts = True

#            if channel == 2: ctr1 = ctr1+1
#            if channel == 2 and additionalCuts: ctr2 = ctr2+1
            
#            if chain.e_class == channel and additionalCuts:
            if chain.e_class == channel and additionalCuts:
                            
                if chain.GetLeaf("j_ak5_pt").GetValue() > 25 :
                    h_v_pt.Fill( chain.v_pt, curSF )
                    h_v_mass.Fill( chain.v_mass, curSF )
                    h_v_mt.Fill( chain.v_mt, curSF )
                    h_e_met.Fill( chain.e_met, curSF )
                    h_e_nvert.Fill( chain.e_nvert )
                    h_e_nvert_weighted.Fill( chain.e_nvert, curSF )
                    h_l_pt.Fill( chain.l_pt, curSF )
                    h_l_eta.Fill( chain.l_eta, curSF )   
#                    h_l_pt.Fill( chain.l_pt, curSF )
#                    h_l_eta.Fill( chain.l_eta, curSF )                   
                    h_lplus_pt.Fill( chain.lplus_pt, curSF )
                    h_lplus_eta.Fill( chain.lplus_eta, curSF ) 
                    # what is the normalization offset coming from PU?
                    h_e_PU.Fill( chain.e_puwt, curSF_noPUweight )

#               simple unfolding test, when get full set of gen jets, will update this...
                if chain.GetLeaf("j_ak7_pt").GetValue() > 125 and isData[nfiles] == 0:
                    cur_jpt = chain.GetLeaf("j_ak7_pt").GetValue()
                    tmp_ak7_mass = chain.GetLeaf("j_ak7_mass").GetValue()
                    tmp_ak7g_mass = chain.GetLeaf("j_ak7g_mass").GetValue()                        
                    rur_ak7w.Fill(tmp_ak7_mass,tmp_ak7g_mass,curSF)
                    if ( cur_jpt > pt_binLo[0] ) and ( cur_jpt < pt_binHi[0] ) : rur_ak7w_0bin.Fill(tmp_ak7_mass,tmp_ak7g_mass,curSF); 
                    if ( cur_jpt > pt_binLo[1] ) and ( cur_jpt < pt_binHi[1] ) : rur_ak7w_1bin.Fill(tmp_ak7_mass,tmp_ak7g_mass,curSF); 
                    if ( cur_jpt > pt_binLo[2] ) and ( cur_jpt < pt_binHi[2] ) : rur_ak7w_2bin.Fill(tmp_ak7_mass,tmp_ak7g_mass,curSF); 
                    if ( cur_jpt > pt_binLo[3] ) and ( cur_jpt < pt_binHi[3] ) : rur_ak7w_3bin.Fill(tmp_ak7_mass,tmp_ak7g_mass,curSF); 
                    if ( cur_jpt > pt_binLo[4] ) and ( cur_jpt < pt_binHi[4] ) : rur_ak7w_4bin.Fill(tmp_ak7_mass,tmp_ak7g_mass,curSF);   

                    if i%2 == 0: rur_ak7w_closure.Fill(tmp_ak7_mass, tmp_ak7g_mass,curSF)
                    if i%2 == 1:
                        hunfw_ak7_mass_closure.Fill( tmp_ak7_mass, curSF )
                        hunfw_ak7g_mass_closure.Fill( tmp_ak7g_mass, curSF )

                if isV3MC:
                    if chain.GetLeaf("j_ak7tr_pt").GetValue() > 125 and isData[nfiles] == 0:
                        cur_jpt = chain.GetLeaf("j_ak7tr_pt").GetValue()
                        tmp_ak7_mass = chain.GetLeaf("j_ak7tr_mass").GetValue()
                        tmp_ak7g_mass = chain.GetLeaf("j_ak7trg_mass").GetValue()                        
                        rur_ak7trw.Fill(tmp_ak7_mass,tmp_ak7g_mass,curSF)
                        if ( cur_jpt > pt_binLo[0] ) and ( cur_jpt < pt_binHi[0] ) : rur_ak7trw_0bin.Fill(tmp_ak7_mass,tmp_ak7g_mass,curSF); 
                        if ( cur_jpt > pt_binLo[1] ) and ( cur_jpt < pt_binHi[1] ) : rur_ak7trw_1bin.Fill(tmp_ak7_mass,tmp_ak7g_mass,curSF); 
                        if ( cur_jpt > pt_binLo[2] ) and ( cur_jpt < pt_binHi[2] ) : rur_ak7trw_2bin.Fill(tmp_ak7_mass,tmp_ak7g_mass,curSF); 
                        if ( cur_jpt > pt_binLo[3] ) and ( cur_jpt < pt_binHi[3] ) : rur_ak7trw_3bin.Fill(tmp_ak7_mass,tmp_ak7g_mass,curSF); 
                        if ( cur_jpt > pt_binLo[4] ) and ( cur_jpt < pt_binHi[4] ) : rur_ak7trw_4bin.Fill(tmp_ak7_mass,tmp_ak7g_mass,curSF);   
                    if chain.GetLeaf("j_ak7ft_pt").GetValue() > 125 and isData[nfiles] == 0:
                        cur_jpt = chain.GetLeaf("j_ak7ft_pt").GetValue()
                        tmp_ak7_mass = chain.GetLeaf("j_ak7ft_mass").GetValue()
                        tmp_ak7g_mass = chain.GetLeaf("j_ak7ftg_mass").GetValue()                        
                        rur_ak7ftw.Fill(tmp_ak7_mass,tmp_ak7g_mass,curSF)
                        if ( cur_jpt > pt_binLo[0] ) and ( cur_jpt < pt_binHi[0] ) : rur_ak7ftw_0bin.Fill(tmp_ak7_mass,tmp_ak7g_mass,curSF); 
                        if ( cur_jpt > pt_binLo[1] ) and ( cur_jpt < pt_binHi[1] ) : rur_ak7ftw_1bin.Fill(tmp_ak7_mass,tmp_ak7g_mass,curSF); 
                        if ( cur_jpt > pt_binLo[2] ) and ( cur_jpt < pt_binHi[2] ) : rur_ak7ftw_2bin.Fill(tmp_ak7_mass,tmp_ak7g_mass,curSF); 
                        if ( cur_jpt > pt_binLo[3] ) and ( cur_jpt < pt_binHi[3] ) : rur_ak7ftw_3bin.Fill(tmp_ak7_mass,tmp_ak7g_mass,curSF); 
                        if ( cur_jpt > pt_binLo[4] ) and ( cur_jpt < pt_binHi[4] ) : rur_ak7ftw_4bin.Fill(tmp_ak7_mass,tmp_ak7g_mass,curSF);   
                    if chain.GetLeaf("j_ak7pr_pt").GetValue() > 125 and isData[nfiles] == 0:
                        cur_jpt = chain.GetLeaf("j_ak7pr_pt").GetValue()
                        tmp_ak7_mass = chain.GetLeaf("j_ak7pr_mass").GetValue()
                        tmp_ak7g_mass = chain.GetLeaf("j_ak7prg_mass").GetValue()                        
                        rur_ak7prw.Fill(tmp_ak7_mass,tmp_ak7g_mass,curSF)
                        if ( cur_jpt > pt_binLo[0] ) and ( cur_jpt < pt_binHi[0] ) : rur_ak7prw_0bin.Fill(tmp_ak7_mass,tmp_ak7g_mass,curSF); 
                        if ( cur_jpt > pt_binLo[1] ) and ( cur_jpt < pt_binHi[1] ) : rur_ak7prw_1bin.Fill(tmp_ak7_mass,tmp_ak7g_mass,curSF); 
                        if ( cur_jpt > pt_binLo[2] ) and ( cur_jpt < pt_binHi[2] ) : rur_ak7prw_2bin.Fill(tmp_ak7_mass,tmp_ak7g_mass,curSF); 
                        if ( cur_jpt > pt_binLo[3] ) and ( cur_jpt < pt_binHi[3] ) : rur_ak7prw_3bin.Fill(tmp_ak7_mass,tmp_ak7g_mass,curSF); 
                        if ( cur_jpt > pt_binLo[4] ) and ( cur_jpt < pt_binHi[4] ) : rur_ak7prw_4bin.Fill(tmp_ak7_mass,tmp_ak7g_mass,curSF);   

                
                if chain.GetLeaf("j_ca12ft_pt").GetValue() > 125:
                    if chain.GetLeaf("j_ca12ft_toptag").GetValue() > 0.: h_ca12ft_mass_toptagged.Fill( chain.GetLeaf("j_ca12ft_mass").GetValue(), curSF  )
                    if chain.GetLeaf("j_ca12ft_Wtag").GetValue() > 0.: h_ca12ft_mass_Wtagged.Fill( chain.GetLeaf("j_ca12ft_mass").GetValue(), curSF  )

                if chain.GetLeaf("j_ca8pr_pt").GetValue() > 200 and chain.GetLeaf("j_ca8pr_ak5btag").GetValue() > 0.: 
                        curmassdrop = chain.GetLeaf("j_ca8pr_m1").GetValue() / chain.GetLeaf("j_ca8pr_mass").GetValue()
                        h_ca8pr_massdrop.Fill( curmassdrop, curSF   )
#                        print curmassdrop,", and ",chain.GetLeaf("j_ca8pr_ak5btag").GetValue()
                        if curmassdrop < 0.3 and chain.GetLeaf("j_ca8pr_ak5btag").GetValue() > 0:
                            h_ca8pr_mass_Wtagged.Fill( chain.GetLeaf("j_ca8pr_mass").GetValue(), curSF  )

#                for jitr in range(len(jtypes)):
#                    
#                    cur_jpt = chain.GetLeaf("j_"+jtypes[jitr]+"_pt").GetValue()
#                    
#                    if cur_jpt > 125:
#                    
#                        cur_jm = chain.GetLeaf("j_"+jtypes[jitr]+"_mass").GetValue()
#                        cur_jeta = chain.GetLeaf("j_"+jtypes[jitr]+"_eta").GetValue()
#                        cur_nv = chain.e_nvert
#                        h_area[jitr].Fill( chain.GetLeaf("j_"+jtypes[jitr]+"_area").GetValue(), curSF )
#                        h_eta[jitr].Fill( cur_jeta, curSF )                    
#                        h_pt[jitr].Fill( cur_jpt, curSF )
#                        h_mass[jitr].Fill( cur_jm, curSF )
#                        if ( cur_jpt > pt_binLo[0] ) and ( cur_jpt < pt_binHi[0] ) : h_mass_0bin[jitr].Fill( cur_jm, curSF )
#                        if ( cur_jpt > pt_binLo[1] ) and ( cur_jpt < pt_binHi[1] ) : h_mass_1bin[jitr].Fill( cur_jm, curSF )
#                        if ( cur_jpt > pt_binLo[2] ) and ( cur_jpt < pt_binHi[2] ) : h_mass_2bin[jitr].Fill( cur_jm, curSF )                           
#                        if ( cur_jpt > pt_binLo[3] ) and ( cur_jpt < pt_binHi[3] ) : h_mass_3bin[jitr].Fill( cur_jm, curSF )
#                        if ( cur_jpt > pt_binLo[4] ) and ( cur_jpt < pt_binHi[4] ) : h_mass_4bin[jitr].Fill( cur_jm, curSF )
#                        prPt_mass[jitr].Fill( cur_jpt, cur_jm, curSF )
#                        prNV_mass[jitr].Fill( cur_nv, cur_jm, curSF )
#                        prEta_mass[jitr].Fill( cur_jeta, cur_jm, curSF )
#                        
#                        hrat_mass_ovAK5[jitr].Fill( cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak5"]]+"_mass").GetValue(), curSF )
#                        hrat_mass_ovAK7[jitr].Fill( cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7"]]+"_mass").GetValue(), curSF )
#                        hrat_mass_ovAK8[jitr].Fill( cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak8"]]+"_mass").GetValue(), curSF )
#                        hrat_mass_ovCA8[jitr].Fill( cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ca8"]]+"_mass").GetValue(), curSF )
#                        hrat_pt_ovAK5[jitr].Fill( cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak5"]]+"_pt").GetValue(), curSF )
#                        hrat_pt_ovAK7[jitr].Fill( cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7"]]+"_pt").GetValue(), curSF )
#                        hrat_pt_ovAK8[jitr].Fill( cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak8"]]+"_pt").GetValue(), curSF )
#                        hrat_pt_ovCA8[jitr].Fill( cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ca8"]]+"_pt").GetValue(), curSF )
#
#                        prPt_mass_ovAK5[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ak5"]]+"_pt").GetValue(), cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak5"]]+"_mass").GetValue(), curSF )
#                        prPt_mass_ovAK7[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ak7"]]+"_pt").GetValue(), cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7"]]+"_mass").GetValue(), curSF )
#                        prPt_mass_ovAK8[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ak8"]]+"_pt").GetValue(), cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak8"]]+"_mass").GetValue(), curSF )
#                        prPt_mass_ovCA8[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ca8"]]+"_pt").GetValue(), cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ca8"]]+"_mass").GetValue(), curSF )
#                        prPt_pt_ovAK5[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ak5"]]+"_pt").GetValue(), cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak5"]]+"_pt").GetValue(), curSF )
#                        prPt_pt_ovAK7[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ak7"]]+"_pt").GetValue(), cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7"]]+"_pt").GetValue(), curSF )
#                        prPt_pt_ovAK8[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ak8"]]+"_pt").GetValue(), cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak8"]]+"_pt").GetValue(), curSF )
#                        prPt_pt_ovCA8[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ca8"]]+"_pt").GetValue(), cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ca8"]]+"_pt").GetValue(), curSF )
#
#                        prNV_mass_ovAK5[jitr].Fill( cur_nv, cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak5"]]+"_mass").GetValue(), curSF_noPUweight )
#                        prNV_mass_ovAK7[jitr].Fill( cur_nv, cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7"]]+"_mass").GetValue(), curSF_noPUweight )
#                        prNV_mass_ovAK8[jitr].Fill( cur_nv, cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak8"]]+"_mass").GetValue(), curSF_noPUweight )
#                        prNV_mass_ovCA8[jitr].Fill( cur_nv, cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ca8"]]+"_mass").GetValue(), curSF_noPUweight )
#                        prNV_pt_ovAK5[jitr].Fill( cur_nv, cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak5"]]+"_pt").GetValue(), curSF_noPUweight )
#                        prNV_pt_ovAK7[jitr].Fill( cur_nv, cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7"]]+"_pt").GetValue(), curSF_noPUweight )
#                        prNV_pt_ovAK8[jitr].Fill( cur_nv, cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak8"]]+"_pt").GetValue(), curSF_noPUweight )
#                        prNV_pt_ovCA8[jitr].Fill( cur_nv, cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ca8"]]+"_pt").GetValue(), curSF_noPUweight )
#
#                        prEta_mass_ovAK5[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ak5"]]+"_eta").GetValue(), cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak5"]]+"_mass").GetValue(), curSF )
#                        prEta_mass_ovAK7[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ak7"]]+"_eta").GetValue(), cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7"]]+"_mass").GetValue(), curSF )
#                        prEta_mass_ovAK8[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ak8"]]+"_eta").GetValue(), cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak8"]]+"_mass").GetValue(), curSF )
#                        prEta_mass_ovCA8[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ca8"]]+"_eta").GetValue(), cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ca8"]]+"_mass").GetValue(), curSF )
#                        prEta_pt_ovAK5[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ak5"]]+"_eta").GetValue(), cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak5"]]+"_pt").GetValue(), curSF )
#                        prEta_pt_ovAK7[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ak7"]]+"_eta").GetValue(), cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7"]]+"_pt").GetValue(), curSF )
#                        prEta_pt_ovAK8[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ak8"]]+"_eta").GetValue(), cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak8"]]+"_pt").GetValue(), curSF )
#                        prEta_pt_ovCA8[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ca8"]]+"_eta").GetValue(), cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ca8"]]+"_pt").GetValue(), curSF )
#
#                        
#                        ## for Gen, only compare against the same cone size
#                        ## make it versus RECO quantities!!!
#                        if isData[nfiles] == 0:
#                            if (jtypes[jitr].find("ak5") >= 0) and chain.GetLeaf("j_"+jtypes[jtypesToI["ak5g"]]+"_mass").GetValue() > 0.:
#                                #print "cur_jm: "+str(cur_jm)+", "+str(chain.GetLeaf("j_"+jtypes[jtypesToI["ak5g"]]+"_mass").GetValue())+", "+str(curSF)
#                                hrat_mass_ovAK5g[jitr].Fill( cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak5g"]]+"_mass").GetValue(), curSF )
#                                hrat_pt_ovAK5g[jitr].Fill( cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak5g"]]+"_pt").GetValue(), curSF )
#                                
#                                prPt_mass_ovAK5g[jitr].Fill( cur_jpt, cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak5g"]]+"_mass").GetValue() )
#                                prPt_pt_ovAK5g[jitr].Fill( cur_jpt, cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak5g"]]+"_pt").GetValue() )
#                                prNV_mass_ovAK5g[jitr].Fill( cur_nv, cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak5g"]]+"_mass").GetValue() )
#                                prNV_pt_ovAK5g[jitr].Fill( cur_nv, cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak5g"]]+"_pt").GetValue() )
#                                prEta_mass_ovAK5g[jitr].Fill( cur_jeta, cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak5g"]]+"_mass").GetValue() )
#                                prEta_pt_ovAK5g[jitr].Fill( cur_jeta, cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak5g"]]+"_pt").GetValue() )
#
#                            if (jtypes[jitr].find("ak7") >= 0) and chain.GetLeaf("j_"+jtypes[jtypesToI["ak7g"]]+"_mass").GetValue() > 0.:                    
#                                hrat_mass_ovAK7g[jitr].Fill( cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7g"]]+"_mass").GetValue(), curSF )                    
#                                hrat_pt_ovAK7g[jitr].Fill( cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7g"]]+"_pt").GetValue(), curSF )                    
#                                
#                                prPt_mass_ovAK7g[jitr].Fill( cur_jpt, cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7g"]]+"_mass").GetValue() )                     
#                                prPt_pt_ovAK7g[jitr].Fill( cur_jpt, cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7g"]]+"_pt").GetValue() )                    
#                                prNV_mass_ovAK7g[jitr].Fill( cur_nv, cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7g"]]+"_mass").GetValue() )
#                                prNV_pt_ovAK7g[jitr].Fill( cur_nv, cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7g"]]+"_pt").GetValue() )
#                                prEta_mass_ovAK7g[jitr].Fill( cur_jeta, cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7g"]]+"_mass").GetValue() )
#                                prEta_pt_ovAK7g[jitr].Fill( cur_jeta, cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7g"]]+"_pt").GetValue() )
#
#                            if (jtypes[jitr].find("ak8") >= 0) and chain.GetLeaf("j_"+jtypes[jtypesToI["ak8g"]]+"_mass").GetValue() > 0.:                
#                                hrat_mass_ovAK8g[jitr].Fill( cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak8g"]]+"_mass").GetValue(), curSF )  
#                                hrat_pt_ovAK8g[jitr].Fill( cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak8g"]]+"_pt").GetValue(), curSF )
#                                
#                                prPt_mass_ovAK8g[jitr].Fill( cur_jpt, cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak8g"]]+"_mass").GetValue() )
#                                prPt_pt_ovAK8g[jitr].Fill( cur_jpt, cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak8g"]]+"_pt").GetValue() )
#                                prNV_mass_ovAK8g[jitr].Fill( cur_nv, cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak8g"]]+"_mass").GetValue() )
#                                prNV_pt_ovAK8g[jitr].Fill( cur_nv, cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak8g"]]+"_pt").GetValue() )
#                                prEta_mass_ovAK8g[jitr].Fill( cur_jeta, cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak8g"]]+"_mass").GetValue() )
#                                prEta_pt_ovAK8g[jitr].Fill( cur_jeta, cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak8g"]]+"_pt").GetValue() )
#
#                            if (jtypes[jitr].find("ca8") >= 0) and chain.GetLeaf("j_"+jtypes[jtypesToI["ca8g"]]+"_mass").GetValue() > 0.:                
#                                hrat_mass_ovCA8g[jitr].Fill( cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ca8g"]]+"_mass").GetValue(), curSF )                    
#                                hrat_pt_ovCA8g[jitr].Fill( cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ca8g"]]+"_pt").GetValue(), curSF )                                        
#                                
#                                prPt_mass_ovCA8g[jitr].Fill( cur_jpt, cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ca8g"]]+"_mass").GetValue() )                    
#                                prPt_pt_ovCA8g[jitr].Fill( cur_jpt, cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ca8g"]]+"_pt").GetValue() )                    
#                                prNV_mass_ovCA8g[jitr].Fill( cur_nv, cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ca8g"]]+"_mass").GetValue() )
#                                prNV_pt_ovCA8g[jitr].Fill( cur_nv, cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ca8g"]]+"_pt").GetValue() )
#                                prEta_mass_ovCA8g[jitr].Fill( cur_jeta, cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ca8g"]]+"_mass").GetValue() )
#                                prEta_pt_ovCA8g[jitr].Fill( cur_jeta, cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ca8g"]]+"_pt").GetValue() )
#                                    
#                            if isV3MC:
#                                if (jtypes[jitr].find("ak7") >= 0) and chain.GetLeaf("j_"+jtypes[jtypesToI["ak7trg"]]+"_mass").GetValue() > 0.:                    
#                                    hrat_mass_ovAK7trg[jitr].Fill( cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7trg"]]+"_mass").GetValue(), curSF )                    
#                                    hrat_pt_ovAK7trg[jitr].Fill( cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7trg"]]+"_pt").GetValue(), curSF )                    
#                                    prPt_mass_ovAK7trg[jitr].Fill( cur_jpt, cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7trg"]]+"_mass").GetValue() )                     
#                                    prPt_pt_ovAK7trg[jitr].Fill( cur_jpt, cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7trg"]]+"_pt").GetValue() )                    
#                                    prNV_mass_ovAK7trg[jitr].Fill( cur_nv, cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7trg"]]+"_mass").GetValue() )
#                                    prNV_pt_ovAK7trg[jitr].Fill( cur_nv, cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7trg"]]+"_pt").GetValue() )
#                                    prEta_mass_ovAK7trg[jitr].Fill( cur_jeta, cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7trg"]]+"_mass").GetValue() )
#                                    prEta_pt_ovAK7trg[jitr].Fill( cur_jeta, cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7trg"]]+"_pt").GetValue() )
#                                if (jtypes[jitr].find("ak7") >= 0) and chain.GetLeaf("j_"+jtypes[jtypesToI["ak7ftg"]]+"_mass").GetValue() > 0.:                    
#                                    hrat_mass_ovAK7ftg[jitr].Fill( cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7ftg"]]+"_mass").GetValue(), curSF )                    
#                                    hrat_pt_ovAK7ftg[jitr].Fill( cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7ftg"]]+"_pt").GetValue(), curSF )                    
#                                    prPt_mass_ovAK7ftg[jitr].Fill( cur_jpt, cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7ftg"]]+"_mass").GetValue() )                     
#                                    prPt_pt_ovAK7ftg[jitr].Fill( cur_jpt, cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7ftg"]]+"_pt").GetValue() )                    
#                                    prNV_mass_ovAK7ftg[jitr].Fill( cur_nv, cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7ftg"]]+"_mass").GetValue() )
#                                    prNV_pt_ovAK7ftg[jitr].Fill( cur_nv, cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7ftg"]]+"_pt").GetValue() )
#                                    prEta_mass_ovAK7ftg[jitr].Fill( cur_jeta, cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7ftg"]]+"_mass").GetValue() )
#                                    prEta_pt_ovAK7ftg[jitr].Fill( cur_jeta, cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7ftg"]]+"_pt").GetValue() )
#                                if (jtypes[jitr].find("ak7") >= 0) and chain.GetLeaf("j_"+jtypes[jtypesToI["ak7prg"]]+"_mass").GetValue() > 0.:                    
#                                    hrat_mass_ovAK7prg[jitr].Fill( cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7prg"]]+"_mass").GetValue(), curSF )                    
#                                    hrat_pt_ovAK7prg[jitr].Fill( cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7prg"]]+"_pt").GetValue(), curSF )                    
#                                    prPt_mass_ovAK7prg[jitr].Fill( cur_jpt, cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7prg"]]+"_mass").GetValue() )                     
#                                    prPt_pt_ovAK7prg[jitr].Fill( cur_jpt, cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7prg"]]+"_pt").GetValue() )                    
#                                    prNV_mass_ovAK7prg[jitr].Fill( cur_nv, cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7prg"]]+"_mass").GetValue() )
#                                    prNV_pt_ovAK7prg[jitr].Fill( cur_nv, cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7prg"]]+"_pt").GetValue() )
#                                    prEta_mass_ovAK7prg[jitr].Fill( cur_jeta, cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7prg"]]+"_mass").GetValue() )
#                                    prEta_pt_ovAK7prg[jitr].Fill( cur_jeta, cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7prg"]]+"_pt").GetValue() )
                                    
                           
    #################################################
    # Put into directories different channels
    print "Writing out the histograms into ", ooo
    fo.cd()
    h_v_pt.Write()
    h_v_mt.Write()
    h_v_mass.Write()
    h_e_met.Write()                            
    h_e_nvert.Write()                            
    h_e_nvert_weighted.Write()                            
    h_l_pt.Write()                            
    h_l_eta.Write()                                                            
    h_lplus_pt.Write()                            
    h_lplus_eta.Write()     
    h_e_PU.Write()
                                        
    h_ca12ft_mass_Wtagged.Write()
    h_ca12ft_mass_toptagged.Write()
    h_ca8pr_mass_Wtagged.Write()
    h_ca8pr_massdrop.Write()

    rur_ak7w_closure.Write()
    rur_ak7w.Write()
    rur_ak7w_0bin.Write()
    rur_ak7w_1bin.Write()
    rur_ak7w_2bin.Write()
    rur_ak7w_3bin.Write()
    rur_ak7w_4bin.Write()
    hunfw_ak7_mass_closure.Write()
    hunfw_ak7g_mass_closure.Write()
                                        
    if isV3MC:
        rur_ak7trw.Write()
        rur_ak7trw_0bin.Write()
        rur_ak7trw_1bin.Write()
        rur_ak7trw_2bin.Write()
        rur_ak7trw_3bin.Write()
        rur_ak7trw_4bin.Write()
        rur_ak7ftw.Write()
        rur_ak7ftw_0bin.Write()
        rur_ak7ftw_1bin.Write()
        rur_ak7ftw_2bin.Write()
        rur_ak7ftw_3bin.Write()
        rur_ak7ftw_4bin.Write()
        rur_ak7prw.Write()
        rur_ak7prw_0bin.Write()
        rur_ak7prw_1bin.Write()
        rur_ak7prw_2bin.Write()
        rur_ak7prw_3bin.Write()
        rur_ak7prw_4bin.Write()
                            
    for x in range(len(jtypes)):
        h_eta[x].Write()
        h_pt[x].Write()
        h_area[x].Write()
        h_mass[x].Write()
        h_mass_0bin[x].Write()
        h_mass_1bin[x].Write()
        h_mass_2bin[x].Write()
        h_mass_3bin[x].Write()
        h_mass_4bin[x].Write()
        prPt_mass[x].Write()
        prNV_mass[x].Write()
        prEta_mass[x].Write()
            
        hrat_mass_ovAK5[x].Write()
        hrat_mass_ovAK5g[x].Write()
        hrat_mass_ovAK7[x].Write()
        hrat_mass_ovAK7g[x].Write()            
        hrat_mass_ovAK8[x].Write()
        hrat_mass_ovAK8g[x].Write()
        hrat_mass_ovCA8[x].Write()
        hrat_mass_ovCA8g[x].Write()            

        hrat_pt_ovAK5[x].Write()
        hrat_pt_ovAK5g[x].Write()
        hrat_pt_ovAK7[x].Write()
        hrat_pt_ovAK7g[x].Write()            
        hrat_pt_ovAK8[x].Write()
        hrat_pt_ovAK8g[x].Write()
        hrat_pt_ovCA8[x].Write()
        hrat_pt_ovCA8g[x].Write()            

        prPt_mass_ovAK5[x].Write()
        prPt_mass_ovAK5g[x].Write()
        prPt_mass_ovAK7[x].Write()
        prPt_mass_ovAK7g[x].Write()
        prPt_mass_ovAK8[x].Write()
        prPt_mass_ovAK8g[x].Write()
        prPt_mass_ovCA8[x].Write()
        prPt_mass_ovCA8g[x].Write()
        prPt_pt_ovAK5[x].Write()            
        prPt_pt_ovAK5g[x].Write()            
        prPt_pt_ovAK7[x].Write()            
        prPt_pt_ovAK7g[x].Write()            
        prPt_pt_ovAK8[x].Write()            
        prPt_pt_ovAK8g[x].Write()            
        prPt_pt_ovCA8[x].Write()            
        prPt_pt_ovCA8g[x].Write()            

        prNV_mass_ovAK5[x].Write()
        prNV_mass_ovAK5g[x].Write()
        prNV_mass_ovAK7[x].Write()
        prNV_mass_ovAK7g[x].Write()
        prNV_mass_ovAK8[x].Write()
        prNV_mass_ovAK8g[x].Write()
        prNV_mass_ovCA8[x].Write()
        prNV_mass_ovCA8g[x].Write()
        prNV_pt_ovAK5[x].Write()            
        prNV_pt_ovAK5g[x].Write()            
        prNV_pt_ovAK7[x].Write()            
        prNV_pt_ovAK7g[x].Write()            
        prNV_pt_ovAK8[x].Write()            
        prNV_pt_ovAK8g[x].Write()            
        prNV_pt_ovCA8[x].Write()            
        prNV_pt_ovCA8g[x].Write()            

        prEta_mass_ovAK5[x].Write()
        prEta_mass_ovAK5g[x].Write()
        prEta_mass_ovAK7[x].Write()
        prEta_mass_ovAK7g[x].Write()
        prEta_mass_ovAK8[x].Write()
        prEta_mass_ovAK8g[x].Write()
        prEta_mass_ovCA8[x].Write()
        prEta_mass_ovCA8g[x].Write()
        prEta_pt_ovAK5[x].Write()            
        prEta_pt_ovAK5g[x].Write()            
        prEta_pt_ovAK7[x].Write()            
        prEta_pt_ovAK7g[x].Write()            
        prEta_pt_ovAK8[x].Write()            
        prEta_pt_ovAK8g[x].Write()            
        prEta_pt_ovCA8[x].Write()            
        prEta_pt_ovCA8g[x].Write()          
                                    
        if isV3MC:
            hrat_mass_ovAK7trg[x].Write()    
            hrat_pt_ovAK7trg[x].Write()    
            prPt_mass_ovAK7trg[x].Write()    
            prPt_pt_ovAK7trg[x].Write()    
            prNV_mass_ovAK7trg[x].Write()    
            prNV_pt_ovAK7trg[x].Write()    
            prEta_mass_ovAK7trg[x].Write()    
            prEta_pt_ovAK7trg[x].Write()    
            
            hrat_mass_ovAK7ftg[x].Write()    
            hrat_pt_ovAK7ftg[x].Write()    
            prPt_mass_ovAK7ftg[x].Write()    
            prPt_pt_ovAK7ftg[x].Write()    
            prNV_mass_ovAK7ftg[x].Write()    
            prNV_pt_ovAK7ftg[x].Write()    
            prEta_mass_ovAK7ftg[x].Write()    
            prEta_pt_ovAK7ftg[x].Write()    
            
            hrat_mass_ovAK7prg[x].Write()    
            hrat_pt_ovAK7prg[x].Write()    
            prPt_mass_ovAK7prg[x].Write()    
            prPt_pt_ovAK7prg[x].Write()    
            prNV_mass_ovAK7prg[x].Write()    
            prNV_pt_ovAK7prg[x].Write()    
            prEta_mass_ovAK7prg[x].Write()    
            prEta_pt_ovAK7prg[x].Write()    

                                    
    fo.Close()

############################################################
############################################################




