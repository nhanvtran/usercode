from ROOT import gROOT, gStyle, gSystem, TLatex
import subprocess

############################################################
############################################################

def processNtuples(dirname,oname,isData):
    print  "setup has been done for inputs "+dirname
    print  "it will go into "+oname
    print  "this is data, "+str(isData)
    
    ctr1 = 0
    ctr2 = 0
    ctr3 = 0
    ctr4 = 0
    
    # Import everything from ROOT
    import ROOT
    from glob import glob
    from array import array
    from math import sqrt
    import math
    
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
    if isData == 0: 
        if dirname.find("WJets_boostedMadGraph") > 0 or dirname.find("ZJets_boostedMadGraph") > 0 or dirname.find("WJets_boostedHerwig") > 0 or dirname.find("ZJets_boostedHerwig") > 0:
            jtypes = jtypes_mv3
            jtypetrans = jtypetrans_mv3
            jtypesToI = jtypesToI_mv3   
            print "here in MC, v3"
        else:
            jtypes = jtypes_m
            jtypetrans = jtypetrans_m
            jtypesToI = jtypesToI_m    
            print "here in MC, v2"
    if isData > 0: 
        jtypes = jtypes_d
        jtypetrans = jtypetrans_d
        jtypesToI = jtypesToI_d    
        print "here in Data"    

    fo = ROOT.TFile(oname, "recreate")
    to = ROOT.TTree("otree", "otree")

    # Import stuff from FWLite
    import sys
    from DataFormats.FWLite import Events, Handle
    ROOT.gSystem.Load('libCondFormatsJetMETObjects')
    ROOT.gSystem.Load('libFWCoreFWLite');
    ROOT.gSystem.Load('libFWCoreUtilities');
    ROOT.AutoLibraryLoader.enable();
    
    ROOT.gSystem.Load("libDataFormatsFWLite.so");
    ROOT.gSystem.Load("libDataFormatsPatCandidates.so");
    ROOT.gSystem.Load("libFWCoreUtilities.so");
    ROOT.gSystem.Load("libCondFormatsJetMETObjects.so");    
#    ROOT.gSystem.Load("libPhysicsToolsUtilities.so");
    ROOT.gSystem.Load("libPhysicsToolsKinFitter.so");
#    gROOT.ProcessLine(".include ../../../..");

    #ROOT.gSystem.Load('libFWCoreUtilities')
    #ROOT.gSystem.Load('libPhysicsToolsUtilities')
    gROOT.ProcessLine(".include ../../../..")
    #gROOT.ProcessLine("#include <iostream>");
    #gROOT.ProcessLine('.L LumiReweightingStandAlone.h+')
    #gROOT.ProcessLine('.L puReweighter.C+')
    gROOT.ProcessLine('.L EffTableReader.cc+')
    gROOT.ProcessLine('.L EffTableLoader.cc+')
    from ROOT import EffTableReader, EffTableLoader   
    #from ROOT import puReweighter

    #################################################
    fDir = "EfficiencesAndCorrections/";
    # ---------- Set up PU reweighting
#    puWeights = ROOT.puReweighter(fDir+"PUMC_dist.root", fDir+"PUData_dist.root")
    ROOT.gSystem.Load('libPhysicsToolsUtilities')    
    LumiWeights = ROOT.edm.Lumi3DReWeighting(fDir+"PUMC_dist.root", fDir+"PUData_dist.root","pileup", "pileup","Weight_3D.root")  
    LumiWeights.weight3D_init( 1.08 )
    up_LumiWeights = ROOT.edm.Lumi3DReWeighting(fDir+"PUMC_dist.root", fDir+"PUData_dist.root","pileup", "pileup","Weight_3D_up.root")  
    up_LumiWeights.weight3D_init( 1.16 )
    dn_LumiWeights = ROOT.edm.Lumi3DReWeighting(fDir+"PUMC_dist.root", fDir+"PUData_dist.root","pileup", "pileup","Weight_3D_dn.root")  
    dn_LumiWeights.weight3D_init( 1.00 )

    # ---------- Set up jet corrections on the fly of R >= 0.7 jets
    if isData == 0 :
         jecStr = [
                    fDir + "GR_R_42_V23_L1FastJet_AK7PFchs.txt",
                    fDir + "GR_R_42_V23_L2Relative_AK7PFchs.txt",
                    fDir + "GR_R_42_V23_L3Absolute_AK7PFchs.txt",
                   ]
    else :
        jecStr = [
                   fDir + "GR_R_42_V23_L1FastJet_AK7PFchs.txt",
                   fDir + "GR_R_42_V23_L2Relative_AK7PFchs.txt",
                   fDir + "GR_R_42_V23_L3Absolute_AK7PFchs.txt",
                   fDir + "GR_R_42_V23_L2L3Residual_AK7PFchs.txt",
                  ]
    jecPars = ROOT.std.vector(ROOT.JetCorrectorParameters)()

    for ijecStr in jecStr :
        ijec = ROOT.JetCorrectorParameters( ijecStr )
        jecPars.push_back( ijec )

    jec = ROOT.FactorizedJetCorrector(jecPars)
    jecUncStr = ROOT.std.string(fDir + "GR_R_42_V23_Uncertainty_AK7PFchs.txt")
    jecUnc = ROOT.JetCorrectionUncertainty( jecUncStr )

    # ---------- Set up Efficiency table
    muIDEff = EffTableLoader(            fDir + "muonEffsRecoToIso_ScaleFactors.txt")
    muHLTEff = EffTableLoader(           fDir + "muonEffsIsoToHLT_data_LP_LWA.txt")
    eleIdEff = EffTableLoader(           fDir + "eleEffsRecoToWP80_ScaleFactors.txt")
    eleRecoEff = EffTableLoader(         fDir + "eleEffsSCToReco_ScaleFactors.txt")
    eleHLTEff = EffTableLoader(          fDir + "eleEffsSingleElectron.txt")
    eleJ30Eff = EffTableLoader(          fDir + "FullyEfficient.txt")
    eleJ25NoJ30Eff = EffTableLoader(     fDir + "FullyEfficient_Jet2NoJet1.txt")
    eleMHTEff = EffTableLoader(          fDir + "FullyEfficient_MHT.txt")
    eleWMtEff = EffTableLoader(          fDir + "WMt50TriggerEfficiency.txt")

    #eleIdEff_WP95 = EffTableLoader(      fDir + "eleEffsRecoToWP95_ScaleFactors.txt")
    eleIdEff_WP95 = EffTableLoader(      fDir + "eleEffsRecoToWP95_ScaleFactors.txt")
    #eleHLTEffZee95toEle17 = EffTableLoader(          fDir + "eleEffsHLTZee95toEle17.txt")    
    eleHLTEffZee95toEle17 = EffTableLoader(          fDir + "eleEffsSCToReco_ScaleFactors.txt")    
    #################################################   
    

    # ------------------------------------------------------
    ##### setting up the output tree
    # list of arrays
    # need an array for the pointer to make a tree
    v_mass_ = array( 'f', [ 0. ] )
    v_mt_ = array( 'f', [ 0. ] )
    #v_mt_ = n.zeros( 1, dtype=float )
    v_pt_ = array( 'f', [ 0. ] )
    l_pt_ = array( 'f', [ 0. ] )
    l_eta_ = array( 'f', [ 0. ] )
    l_phi_ = array( 'f', [ 0. ] ) 
    l_et_ = array( 'f', [ 0. ] ) 
    #### in the case of the Z, the "l" is always minus and the "lplus" is always plus
    lplus_pt_ = array( 'f', [ 0. ] )
    lplus_eta_ = array( 'f', [ 0. ] )
    lplus_phi_ = array( 'f', [ 0. ] )   
    lplus_et_ = array( 'f', [ 0. ] )    
    #### in the case of the Z, the "l" is always minus and the "lplus" is always plus
    e_met_ = array( 'f', [ 0. ] )
    e_nvert_ = array( 'f', [ 0. ] )    
    e_effwt_ = array( 'f', [ 0. ] )  
    e_class_ = array( 'f', [ 0. ] )    
    e_puwt_ = array( 'f', [ 0. ] )    
    e_puwt_up_ = array( 'f', [ 0. ] )    
    e_puwt_dn_ = array( 'f', [ 0. ] )    
    j_mass_ = []
    j_eta_ = []
    j_phi_ = []
    j_pt_ = []
    j_px_ = []
    j_py_ = []
    j_pz_ = []
    j_e_ = []
    j_area_ = []
    j_jecfactor_ = []
    j_jecfactor_up_ = []
    j_jecfactor_dn_  = []
    j_nJ_ = []
    j_nJ30_ = []
    j_matchtype_ = [] # -1 for "fake", 0 for "miss", 1 for "match"


    j_ca8pr_m1_ = array( 'f', [ 0. ] )    
    j_ca8pr_m2_ = array( 'f', [ 0. ] )    
    j_ca8pr_pt1_ = array( 'f', [ 0. ] )    
    j_ca8pr_pt2_ = array( 'f', [ 0. ] )    
    j_ca8pr_ak5btag_ = array( 'f', [ 0. ] )    
    j_ca8pr_nak5_ = array( 'f', [ 0. ] )    

    j_ca12ft_toptag_ = array( 'f', [ 0. ] )    
    j_ca12ft_Wtag_ = array( 'f', [ 0. ] )    

    for x in range(len(jtypes)):
        j_mass_.append( array( 'f', [ 0. ] ) )
        j_eta_.append( array( 'f', [ 0. ] ) )
        j_phi_.append( array( 'f', [ 0. ] ) )
        j_pt_.append( array( 'f', [ 0. ] ) )
        j_px_.append( array( 'f', [ 0. ] ) )
        j_py_.append( array( 'f', [ 0. ] ) )
        j_pz_.append( array( 'f', [ 0. ] ) )
        j_e_.append( array( 'f', [ 0. ] ) )
        j_area_.append( array( 'f', [ 0. ] ) )
        j_jecfactor_.append( array( 'f', [ 0. ] ) )
        j_jecfactor_up_.append( array( 'f', [ 0. ] ) )
        j_jecfactor_dn_.append( array( 'f', [ 0. ] ) )
        j_nJ_.append( array( 'f', [ 0. ] ) )
        j_nJ30_.append( array( 'f', [ 0. ] ) )
        j_matchtype_.append( array( 'f', [ 0. ] ) )

    to.Branch("v_mt", v_mt_ , "v_mt/F")
    to.Branch("v_mass", v_mass_ , "v_mass/F")
    to.Branch("v_pt", v_pt_ , "v_pt/F")
    to.Branch("l_pt", l_pt_ , "l_pt/F") 
    to.Branch("l_et", l_et_ , "l_et/F")
    to.Branch("l_eta", l_eta_ , "l_eta/F")
    to.Branch("l_phi", l_phi_ , "l_phi/F")
    to.Branch("lplus_pt", lplus_pt_ , "lplus_pt/F")
    to.Branch("lplus_eta", lplus_eta_ , "lplus_eta/F")
    to.Branch("lplus_phi", lplus_phi_ , "lplus_phi/F")
    to.Branch("lplus_et", lplus_et_ , "lplus_et/F")
    to.Branch("e_met", e_met_ , "e_met/F")
    to.Branch("e_nvert", e_nvert_ , "e_nvert/F")
    
    to.Branch("j_ca8pr_m1", j_ca8pr_m1_ , "j_ca8pr_m1/F")
    to.Branch("j_ca8pr_m2", j_ca8pr_m2_ , "j_ca8pr_m2/F")
    to.Branch("j_ca8pr_pt1", j_ca8pr_pt1_ , "j_ca8pr_pt1/F")
    to.Branch("j_ca8pr_pt2", j_ca8pr_pt2_ , "j_ca8pr_pt2/F")
    to.Branch("j_ca8pr_ak5btag", j_ca8pr_ak5btag_ , "j_ca8pr_ak5btag/F")
    to.Branch("j_ca8pr_nak5", j_ca8pr_nak5_ , "j_ca8pr_nak5/F")

    to.Branch("j_ca12ft_toptag", j_ca12ft_toptag_ , "j_ca12ft_toptag/F")
    to.Branch("j_ca12ft_Wtag", j_ca12ft_Wtag_ , "j_ca12ft_Wtag/F")

    to.Branch("e_effwt", e_effwt_ , "e_effwt/F")
    to.Branch("e_class", e_class_ , "e_class/F")
    to.Branch("e_puwt", e_puwt_ , "e_puwt/F")    
    to.Branch("e_puwt_up", e_puwt_up_ , "e_puwt_up/F")
    to.Branch("e_puwt_dn", e_puwt_dn_ , "e_puwt_dn/F")

    for i in range(len(jtypes)):
        #print jtypes[i], " corresponds to ", jtypetrans[jtypes[i]]
        to.Branch("j_"+jtypes[i]+"_mass", j_mass_[i], "j_"+jtypes[i]+"_mass/F")
        to.Branch("j_"+jtypes[i]+"_eta", j_eta_[i], "j_"+jtypes[i]+"_eta/F")
        to.Branch("j_"+jtypes[i]+"_phi", j_phi_[i], "j_"+jtypes[i]+"_phi/F")
        to.Branch("j_"+jtypes[i]+"_pt", j_pt_[i], "j_"+jtypes[i]+"_pt/F")
        to.Branch("j_"+jtypes[i]+"_px", j_px_[i], "j_"+jtypes[i]+"_px/F")
        to.Branch("j_"+jtypes[i]+"_py", j_py_[i], "j_"+jtypes[i]+"_py/F")
        to.Branch("j_"+jtypes[i]+"_pz", j_pz_[i], "j_"+jtypes[i]+"_pz/F")
        to.Branch("j_"+jtypes[i]+"_e", j_e_[i], "j_"+jtypes[i]+"_pt/F")
        to.Branch("j_"+jtypes[i]+"_area", j_area_[i], "j_"+jtypes[i]+"_area/F")
        to.Branch("j_"+jtypes[i]+"_jecfactor_up", j_jecfactor_up_[i], "j_"+jtypes[i]+"_jecfactor_up/F")
        to.Branch("j_"+jtypes[i]+"_jecfactor_dn", j_jecfactor_dn_[i], "j_"+jtypes[i]+"_jecfactor_dn/F")
        to.Branch("j_"+jtypes[i]+"_jecfactor", j_jecfactor_[i], "j_"+jtypes[i]+"_jecfactor/F")
        to.Branch("j_"+jtypes[i]+"_nJ", j_nJ_[i], "j_"+jtypes[i]+"_nJ/F")
        to.Branch("j_"+jtypes[i]+"_nJ30", j_nJ30_[i], "j_"+jtypes[i]+"_nJ30/F")
        to.Branch("j_"+jtypes[i]+"_matchtype", j_matchtype_[i], "j_"+jtypes[i]+"_matchtype/F")


    # ------------------------------------------------------
    
    chain = ROOT.TChain("VJetSubstructure","VJetSubstructure")
    chain.Add(dirname)
    
    entries = chain.GetEntries()
    print "total entries = " + str(entries)
    #if entries > 50000: entries = 50000
    #entries = 10
         
    ###for envent in chain:
    passes2AK5 = 0
    nopasses2AK5 = 0
    #$getattr(ws, "import")(...)
    for i in xrange(entries):
#    for i in xrange(11000):        
        if i%10000 == 0:   
            print "Entry: " + str(i)
        chain.GetEntry( i )

        # ------------------  
        ## PU weights
        if isData == 0:
            minusV = chain.GetLeaf("event_mcPU_nvtx").GetValue(0)
            intimeV = chain.GetLeaf("event_mcPU_nvtx").GetValue(1)
            plusV = chain.GetLeaf("event_mcPU_nvtx").GetValue(2)
#            print minusV,",",intimeV,",",plusV
            e_puwt_[0] = LumiWeights.weight3D( int(minusV), int(intimeV), int(plusV) ) 
            e_puwt_up_[0] = up_LumiWeights.weight3D( int(minusV), int(intimeV), int(plusV) )
            e_puwt_dn_[0] = dn_LumiWeights.weight3D( int(minusV), int(intimeV), int(plusV) )        
        else:         
            e_puwt_[0] = -1.
            e_puwt_up_[0] = -1.  
            e_puwt_dn_[0] = -1.
        # ------------------  
        # control region, class 11    
        passesAsClass11 = False
        passesAsClass1 = False
        passesAsClass2 = False
        passesAsClass3 = False
        passesAsClass4 = False

        ###################################################################
        ###################################################################
        # S e l e c t i o n   f o r   t h e   W e n u   e v e n t s
        electroniso = (chain.Wel_electron_trackiso+chain.Wel_electron_hcaliso+chain.Wel_electron_ecaliso-chain.event_fastJetRho*3.141592653589*0.09)/chain.Wel_electron_pt
        if chain.eventClass == 1 and chain.Wel_electron_isWP70Good and chain.Wel_electron_pt > 35 and electroniso < 0.05 and chain.Wel_mt > 50 and chain.Wel_pt > 50 and chain.event_met_pfmet > 30: 

            passesAsClass1 = True
            e_class_[0] = 1
            
            v_mt_[0] = chain.Wel_mt
            v_pt_[0] = chain.Wel_pt
            l_pt_[0] = chain.Wel_electron_pt
            l_et_[0] = chain.Wel_electron_et    
            l_eta_[0] = chain.Wel_electron_eta    
            l_phi_[0] = chain.Wel_electron_phi    
            e_met_[0] = chain.event_met_pfmet
            e_nvert_[0] = float(chain.event_nPV)
            
            # ------------------   
            ## Wenu efficiencies
            eff_eleid = eleIdEff.GetEfficiency(l_pt_[0], l_eta_[0])
            eff_elereco = eleRecoEff.GetEfficiency(l_pt_[0], l_eta_[0])
            eff_elehlt = eleHLTEff.GetEfficiency(l_pt_[0], l_eta_[0])
            eff_elemht = eleMHTEff.GetEfficiency(e_met_[0], 0)
            eff_elewmt = eleWMtEff.GetEfficiency(v_mt_[0], l_eta_[0])
#            print eff_elewmt,"...wmt"
#            e_effwt_[0] = eff_eleid*eff_elereco*eff_elehlt*eff_elemht*eff_elewmt
            e_effwt_[0] = eff_eleid*eff_elereco*eff_elehlt   

        ###################################################################
        ###################################################################
        # S e l e c t i o n   f o r   t h e   W e n u   Q C D   C O N T R O L   R E G I O N
#        if (isData == 1):
#            electroniso = (chain.Wel_electron_trackiso+chain.Wel_electron_hcaliso+chain.Wel_electron_ecaliso-chain.event_fastJetRho*3.141592653589*0.09)/chain.Wel_electron_pt
#            if chain.eventClass == 1 and chain.Wel_electron_pt > 30 and electroniso > 0.1 and electroniso > 0.2 and chain.Wel_mt > 50 and chain.Wel_pt > 50 and chain.event_met_pfmet > 20: 
#
#                passesAsClass11 = True
#                e_class_[0] = 11
#
#                v_mt_[0] = chain.Wel_mt
#                v_pt_[0] = chain.Wel_pt
#                l_pt_[0] = chain.Wel_electron_pt
#                l_et_[0] = chain.Wel_electron_et    
#                l_eta_[0] = chain.Wel_electron_eta    
#                l_phi_[0] = chain.Wel_electron_phi    
#                e_met_[0] = chain.event_met_pfmet
#                e_nvert_[0] = float(chain.event_nPV)
        
        ###################################################################
        ###################################################################
        # S e l e c t i o n   f o r   t h e   W m u n u   e v e n t s
        muoniso = (chain.Wmu_muon_trackiso+chain.Wmu_muon_hcaliso+chain.Wmu_muon_ecaliso-chain.event_fastJetRho*3.1415939*0.09)/chain.Wmu_muon_pt;
#        if chain.eventClass == 2: ctr1 = ctr1 + 1
#        if muoniso < 0.1: ctr2 = ctr2 + 1    
#        if chain.Wmu_pt > 120: ctr3 = ctr3 + 1
        muonSel = muoniso < 0.10 and chain.Wmu_muon_pt > 25 and chain.Wmu_muon_numberOfMatches > 0 and chain.Wmu_muon_nchi2 < 10. and chain.Wmu_muon_pixelHits > 0 and chain.Wmu_muon_trackerHits > 10 and chain.Wmu_muon_muonHits > 0
    
        if chain.eventClass == 2 and muonSel and abs(chain.Wmu_muon_eta) < 2.1 and chain.Wmu_mt > 50 and chain.Wmu_pt > 50  and chain.event_met_pfmet > 30: 

            passesAsClass2 = True
            e_class_[0] = 2
            ctr4 = ctr4 + 1
            
            v_mt_[0] = chain.Wmu_mt
            v_pt_[0] = chain.Wmu_pt
            l_pt_[0] = chain.Wmu_muon_pt
            l_eta_[0] = chain.Wmu_muon_eta    
            l_phi_[0] = chain.Wmu_muon_phi    
            e_met_[0] = chain.event_met_pfmet
            e_nvert_[0] = float(chain.event_nPV)
            
            # ------------------   
            ## Wmunu efficiencies
            e_effwt_[0] =muIDEff.GetEfficiency(chain.Wmu_muon_pt, chain.Wmu_muon_eta) * muHLTEff.GetEfficiency(chain.Wmu_muon_pt, chain.Wmu_muon_eta)
#            print muHLTEff.GetEfficiency(chain.Wmu_muon_pt, chain.Wmu_muon_eta),"...muhlt"
        ###################################################################
        ###################################################################
        # S e l e c t i o n   f o r   t h e   Z e e   e v e n t s
        eplus_iso = (chain.Zel_eplus_trackiso+chain.Zel_eplus_hcaliso+chain.Zel_eplus_ecaliso-chain.event_fastJetRho*3.141592653589*0.09)/chain.Zel_eplus_pt
        eminus_iso = (chain.Zel_eminus_trackiso+chain.Zel_eminus_hcaliso+chain.Zel_eminus_ecaliso-chain.event_fastJetRho*3.141592653589*0.09)/chain.Zel_eminus_pt
        eplusSel =  chain.Zel_eplus_pt > 20 and chain.Zel_eplus_isWP95
        eminusSel = chain.Zel_eminus_pt > 20 and chain.Zel_eminus_isWP95
        if chain.eventClass == 3 and eplusSel and eminusSel and chain.Zel_mass > 80 and chain.Zel_mass < 100 and chain.Zel_pt > 50 and chain.event_met_pfmet < 50: 
            
            passesAsClass3 = True
            e_class_[0] = 3
            
            v_mass_[0] = chain.Zel_mass
            v_pt_[0] = chain.Zel_pt
            l_pt_[0] = chain.Zel_eminus_pt
            l_et_[0] = chain.Zel_eminus_et            
            l_eta_[0] = chain.Zel_eminus_eta    
            l_phi_[0] = chain.Zel_eminus_phi    
            lplus_pt_[0] = chain.Zel_eplus_pt
            lplus_eta_[0] = chain.Zel_eplus_eta    
            lplus_phi_[0] = chain.Zel_eplus_phi    
            lplus_et_[0] = chain.Zel_eplus_et
            e_met_[0] = chain.event_met_pfmet
            e_nvert_[0] = float(chain.event_nPV)
            
            # ------------------   
            ## Zee efficiencies
            #print str(l_pt_[0])+" and "+str(l_eta_[0])
            eff_eleid = eleIdEff_WP95.GetEfficiency( l_pt_[0], l_eta_[0] )
            eff_eleid2 = eleIdEff_WP95.GetEfficiency(lplus_pt_[0], lplus_eta_[0]) 
            eff_elereco = eleRecoEff.GetEfficiency(l_pt_[0], l_eta_[0])
            eff_elereco2 = eleRecoEff.GetEfficiency(lplus_pt_[0], lplus_eta_[0]) 
            eff_elehlt = eleHLTEffZee95toEle17.GetEfficiency(l_pt_[0], l_eta_[0])
            eff_elehlt2 = eleHLTEffZee95toEle17.GetEfficiency(lplus_pt_[0], lplus_eta_[0])
            e_effwt_[0] = eff_eleid*eff_eleid2*eff_elereco*eff_elereco2*(1-(1-eff_elehlt)*(1-eff_elehlt2))
                
        ###################################################################
        ###################################################################
        # S e l e c t i o n   f o r   t h e   Z m m   e v e n t s
        muonplus_iso = (chain.Zmu_muplus_trackiso+chain.Zmu_muplus_hcaliso+chain.Zmu_muplus_ecaliso-chain.event_fastJetRho*3.1415939*0.09)/chain.Zmu_muplus_pt;
        muonminus_iso = (chain.Zmu_muminus_trackiso+chain.Zmu_muminus_hcaliso+chain.Zmu_muminus_ecaliso-chain.event_fastJetRho*3.1415939*0.09)/chain.Zmu_muminus_pt;
        muonplusSel = muonplus_iso < 0.10 and chain.Zmu_muplus_pt > 25 and chain.Zmu_muplus_numberOfMatches > 0 and chain.Zmu_muplus_nchi2 < 10. and chain.Zmu_muplus_pixelHits > 0 and chain.Zmu_muplus_trackerHits > 10 and chain.Zmu_muplus_muonHits > 0
        muonminusSel = muonminus_iso < 0.10  and chain.Zmu_muminus_pt > 25 and chain.Zmu_muminus_numberOfMatches > 0 and chain.Zmu_muminus_nchi2 < 10. and chain.Zmu_muminus_pixelHits > 0 and chain.Zmu_muminus_trackerHits > 10 and chain.Zmu_muminus_muonHits > 0
        if chain.eventClass == 4 and muonplusSel and muonminusSel and chain.Zmu_mass > 80 and chain.Zmu_mass < 100 and chain.Zmu_pt > 50 and chain.event_met_pfmet < 50: 
            
            passesAsClass4 = True
            e_class_[0] = 4
            
            v_mass_[0] = chain.Zmu_mass
            v_pt_[0] = chain.Zmu_pt
            l_pt_[0] = chain.Zmu_muminus_pt
            l_eta_[0] = chain.Zmu_muminus_eta    
            l_phi_[0] = chain.Zmu_muminus_phi    
            lplus_pt_[0] = chain.Zmu_muplus_pt
            lplus_eta_[0] = chain.Zmu_muplus_eta    
            lplus_phi_[0] = chain.Zmu_muplus_phi    
            e_met_[0] = chain.event_met_pfmet
            e_nvert_[0] = float(chain.event_nPV)
         
            # ------------------   
            ## Zmm efficiencies
            eff_muid1 = muIDEff.GetEfficiency(chain.Zmu_muminus_pt, chain.Zmu_muminus_eta)
            eff_muid2 = muIDEff.GetEfficiency(chain.Zmu_muplus_pt, chain.Zmu_muplus_eta)
            eff_muhlt1 = muHLTEff.GetEfficiency(chain.Zmu_muminus_pt, chain.Zmu_muminus_eta)
            eff_muhlt2 = muHLTEff.GetEfficiency(chain.Zmu_muplus_pt, chain.Zmu_muplus_eta)
            e_effwt_[0] = eff_muid1*eff_muid2*(1.-(1-eff_muhlt1)*(1-eff_muhlt2))
        
        ###################################################################
        ###################################################################
        # F i l l   j e t   i n f o r m a t i o n
        if passesAsClass1 == True or passesAsClass2 == True or passesAsClass3 == True or passesAsClass4 == True:
            
            ##########################################################################
            ##  A L G O   S P E C I F I C   S T U F F ,   C A 8 P R U N E D ,   C A 1 2 F I L T E R E D ,   . . . 

            ##### a little test for david...
#            if passesAsClass1 == True:
#                #ca8_j1 = chain.GetLeaf("JetCA8PF_Pt").GetValue(0)
#                #ca8_j2 = chain.GetLeaf("JetCA8PF_Pt").GetValue(1)            
#                ca8_j1 = chain.GetLeaf("JetCA12FILTEREDPF_Pt").GetValue(0)
#                ca8_j2 = chain.GetLeaf("JetCA12FILTEREDPF_Pt").GetValue(1)            
#                ak5_j1 = chain.GetLeaf("JetAK5PF_Pt").GetValue(0)
#                ak5_j2 = chain.GetLeaf("JetAK5PF_Pt").GetValue(1)
#                if ca8_j1 > 125 and ca8_j2 < 25:
#                    #print "ca8_j1: ",ca8_j1,", ca8_j2: ",ca8_j2
#                    #print "ak5_j1: ",ak5_j1,", ak5_j2: ",ak5_j2            
#                    if ak5_j1 > 25 and ak5_j2 > 25: 
#                        passes2AK5 = passes2AK5+1
#                    else:
#                        nopasses2AK5 = nopasses2AK5+1
            
            
            
            ## ---------------------------
            ## for ca8pruned 
            ## "W tag", 2 subjets with mu < 0.25 (do not tag it!) additional AK5 jets not within cone with tight b-tag
            ## ---------------------------            
            j_ca8pr_m1_[0] = chain.GetLeaf("JetCA8PRUNEDPF_subJet1Mass").GetValue(0)
            j_ca8pr_m2_[0] = chain.GetLeaf("JetCA8PRUNEDPF_subJet2Mass").GetValue(0)
            j_ca8pr_pt1_[0] = chain.GetLeaf("JetCA8PRUNEDPF_subJet1Pt").GetValue(0)
            j_ca8pr_pt2_[0] = chain.GetLeaf("JetCA8PRUNEDPF_subJet2Pt").GetValue(0)
            nak5_dummy = chain.GetLeaf("JetAK5PF_nJets").GetValue()
            nAK5btag = 0.
            nAK5 = 0.            
            for kk in range( int(nak5_dummy) ):
                deta = chain.GetLeaf("JetCA8PRUNEDPF_Eta").GetValue(0) - chain.GetLeaf("JetAK5PF_Eta").GetValue(kk)
                dphi = chain.GetLeaf("JetCA8PRUNEDPF_Phi").GetValue(0) - chain.GetLeaf("JetAK5PF_Phi").GetValue(kk)
                deltaR = math.sqrt( deta*deta+dphi*dphi )
                if deltaR > 0.8:
                    nAK5 = nAK5 + 1.
                    bD_csv = chain.GetLeaf("JetAK5PF_bDiscrCSV").GetValue(kk)
                    if bD_csv > 0.898: nAK5btag = nAK5btag + 1.

            j_ca8pr_nak5_[0] = nAK5
            j_ca8pr_ak5btag_[0] = nAK5btag

            ## ---------------------------
            ## for ca12filtered 
            ## "top tag", 3 filtered subjets all within CA12 and with pt > 30, at least one tight b-tag [no b info, sorry!], > 0 additional AK5 jets not within cone
            ## "W tag", 2 filtered subjets all within CA12 and with pt > 30, if there is a 3rd it has pt < 20, anti-b-tag on all 3 [no b info, sorry!], > 0 additional AK5 jets not within cone with tight b-tag
            ## ---------------------------            
            nsj_dummy = chain.GetLeaf("JetCA12FILTEREDPF_sjNumJets").GetValue()
#            print "nsj_dummy: ",nsj_dummy
            nca12ft_sjInside = 0.
            nca12ft_sjInside_gt30 = 0.
            nca12ft_sjInside_lt20 = 0.
            for kk in range( int(nsj_dummy) ):
#                print kk,", ",chain.GetLeaf("JetCA12FILTEREDPF_sjEta").GetValue(kk),", ",chain.GetLeaf("JetCA12FILTEREDPF_sjPhi").GetValue(kk)
                deta = chain.GetLeaf("JetCA12FILTEREDPF_Eta").GetValue(0) - chain.GetLeaf("JetCA12FILTEREDPF_sjEta").GetValue(kk)
                dphi = chain.GetLeaf("JetCA12FILTEREDPF_Phi").GetValue(0) - chain.GetLeaf("JetCA12FILTEREDPF_sjPhi").GetValue(kk)
                deltaR = math.sqrt( deta*deta+dphi*dphi )
                if deltaR < 1.2:
                    nca12ft_sjInside = nca12ft_sjInside + 1.
                    if chain.GetLeaf("JetCA12FILTEREDPF_sjPt").GetValue(kk) > 30: nca12ft_sjInside_gt30 = nca12ft_sjInside_gt30 + 1.
                    if chain.GetLeaf("JetCA12FILTEREDPF_sjPt").GetValue(kk) < 20: nca12ft_sjInside_lt20 = nca12ft_sjInside_lt20 + 1.

            nak5_dummy = chain.GetLeaf("JetAK5PF_nJets").GetValue()
            nca12ft_AK5btag = 0.
            nca12ft_AK5 = 0.
            for kk in range( int(nak5_dummy) ):
                deta = chain.GetLeaf("JetCA12FILTEREDPF_Eta").GetValue(0) - chain.GetLeaf("JetAK5PF_Eta").GetValue(kk)
                dphi = chain.GetLeaf("JetCA12FILTEREDPF_Phi").GetValue(0) - chain.GetLeaf("JetAK5PF_Phi").GetValue(kk)
                deltaR = math.sqrt( deta*deta+dphi*dphi )
                if deltaR > 1.2:
                    nca12ft_AK5 = nca12ft_AK5 + 1.;
                    bD_csv = chain.GetLeaf("JetAK5PF_bDiscrCSV").GetValue(kk)
                    if bD_csv > 0.898: nca12ft_AK5btag = nca12ft_AK5btag + 1.

            # top tag
            j_ca12ft_toptag_[0] = 0.
            j_ca12ft_Wtag_[0] = 0.
#            print nca12ft_sjInside," ",nca12ft_sjInside_gt30," ",nca12ft_sjInside_lt20," ",nca12ft_AK5," ",nca12ft_AK5btag
            if nca12ft_sjInside == 3 and nca12ft_sjInside_gt30 == 3 and nca12ft_AK5 > 0 and nca12ft_AK5btag > 0: j_ca12ft_toptag_[0] = 1
            if nca12ft_sjInside == 3 and nca12ft_sjInside_gt30 == 2 and nca12ft_sjInside_lt20 <= 1 and nca12ft_AK5btag > 0: j_ca12ft_Wtag_[0] = 1

            ##########################################################################
            
            for jitr in range(len(jtypes)):
                #print "----" + str(jitr) + "----"
                # do not loop on the gen jets if it is data
                if (jtypes[jitr].find("g") < 0):
                        
                    if jtypes[jitr].find("7") > 0 or jtypes[jitr].find("8") > 0 or jtypes[jitr].find("12") > 0:
                        # put in the corrections for R >= 0.7 jets
                        jpx = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Px").GetValue(0)
                        jpy = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Py").GetValue(0)
                        jpz = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Pz").GetValue(0)
                        je = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_E").GetValue(0)
                        jarea = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Area").GetValue(0)
                        origcor = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_JecFactor").GetValue(0) 
                        jdefRaw = ROOT.TLorentzVector(jpx * origcor,jpy * origcor,jpz * origcor,je * origcor)
                        jec.setJetEta(jdefRaw.Eta())
                        jec.setJetPt(jdefRaw.Perp())    
                        jec.setJetA(jarea)
                        jec.setRho( chain.event_fastJetRho ) 
                        factor = jec.getCorrection()
                        jdef = ROOT.TLorentzVector(jdefRaw.Px() * factor,jdefRaw.Py() * factor,jdefRaw.Pz() * factor,jdefRaw.Energy() * factor)
                        j_mass_[jitr][0] = jdef.M()
                        j_eta_[jitr][0] = jdef.Eta()
                        j_phi_[jitr][0] = jdef.Phi()
                        j_pt_[jitr][0] = jdef.Pt()
                        j_px_[jitr][0] = jdef.Px()
                        j_py_[jitr][0] = jdef.Py()
                        j_pz_[jitr][0] = jdef.Pz()                        
                        j_e_[jitr][0] = jdef.E()                          
                        j_jecfactor_[jitr][0] = factor    
                        jecUnc.setJetEta( jdefRaw.Eta() )
                        jecUnc.setJetPt( jdefRaw.Perp() * factor );                        
                        j_jecfactor_up_[jitr][0] = jecUnc.getUncertainty( True )
                        jecUnc.setJetEta( jdefRaw.Eta() )
                        jecUnc.setJetPt( jdefRaw.Perp() * factor );                        
                        j_jecfactor_dn_[jitr][0] = jecUnc.getUncertainty( False )   
#                        print j_jecfactor_up_[jitr][0],",",j_jecfactor_dn_[jitr][0]
                    else:
                        j_mass_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Mass").GetValue(0)
                        j_eta_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Eta").GetValue(0)
                        j_phi_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Phi").GetValue(0)
                        j_pt_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Pt").GetValue(0)
                        j_px_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Px").GetValue(0)
                        j_py_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Py").GetValue(0)
                        j_pz_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Pz").GetValue(0) 
                        j_e_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_E").GetValue(0)
                        j_jecfactor_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_JecFactor").GetValue(0)
                        j_jecfactor_up_[jitr][0] = 0.
                        j_jecfactor_dn_[jitr][0] = 0.      
#                        print "factor: ",chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_JecFactor").GetValue(0),", jet pt: ",j_pt_[jitr][0],", jet eta: ",j_eta_[jitr][0]
                        
                    j_area_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Area").GetValue(0)
                    j_nJ_[jitr][0] = float( chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_nJets").GetValue() )
                    j30ctr = 0
                    if (j_nJ_ > 0):
                        for x in range( int(j_nJ_[jitr][0]) ):
                            if chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Pt").GetValue(0) > 30: j30ctr = j30ctr + 1
                    
                    j_nJ30_[jitr][0] = float(j30ctr)
                    j_matchtype_[jitr][0] = -99.
                    
                ###############################################################
                # gen jets, have to do matching
                elif (jtypes[jitr].find("g") >= 0) and (isData == 0): 
                    # get matching reco collection
                    scur = jtypes[jitr]
                    scur = scur[:-1]
                    # loop through gen jets and find closest Dr
                    toler = 100.
                    matchindex = -1
                    
                    ###############################################################
                    ## hard-coded!
                    for k in range(9):
                        deta = chain.GetLeaf("Jet"+jtypetrans[jtypes[jtypesToI[scur]]]+"_Eta").GetValue(0) - chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Eta").GetValue(k)
                        dphi = chain.GetLeaf("Jet"+jtypetrans[jtypes[jtypesToI[scur]]]+"_Phi").GetValue(0) - chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Phi").GetValue(k)
                        deltaR = math.sqrt( deta*deta+dphi*dphi )
                        if (deltaR < 0.3) and (deltaR < toler): 
                            matchindex = k
                            toler = deltaR
                        
                    # fill information for it
                    if matchindex >= 0:
                        j_mass_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Mass").GetValue(matchindex)
                        j_eta_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Eta").GetValue(matchindex)
                        j_phi_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Phi").GetValue(matchindex)
                        j_pt_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Pt").GetValue(matchindex)
                        j_px_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Px").GetValue(matchindex)
                        j_py_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Py").GetValue(matchindex)
                        j_pz_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Pz").GetValue(matchindex) 
                        j_e_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_E").GetValue(matchindex)                        
                        j_jecfactor_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_JecFactor").GetValue(matchindex)  
                        j_matchtype_[jitr][0] = 1.
                    else:
                        j_mass_[jitr][0] = 0.
                        j_eta_[jitr][0] = 0.
                        j_phi_[jitr][0] = 0.
                        j_pt_[jitr][0] = 0.
                        j_px_[jitr][0] = 0.
                        j_py_[jitr][0] = 0.
                        j_pz_[jitr][0] = 0.
                        j_e_[jitr][0] = 0.
                        j_jecfactor_[jitr][0] = 0.
                        j_matchtype_[jitr][0] = -1.
                    ###############################################################
                    
                else: continue
                
            to.Fill()
        
        ###################################################################
        ###################################################################

            
    print "Writing out the reduce analysis tuples into ", oname
    fo.cd()
    to.Write()        
    fo.Close()

    totalcounts = passes2AK5+nopasses2AK5
    print "passes: ",passes2AK5,"/",totalcounts
    print "ctr1 = ", ctr1,", ctr2 = ", ctr2,", ctr3 = ", ctr3,", ctr4 = ", ctr4

############################################################
############################################################




