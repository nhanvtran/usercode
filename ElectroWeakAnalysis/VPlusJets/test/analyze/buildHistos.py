from ROOT import gROOT, gStyle, gSystem, TLatex
import subprocess

############################################################
############################################################

def buildHistos(dirname,oname,isData,scaleFactors,channel):

    # Import everything from ROOT
    import ROOT
    from glob import glob
    from array import array
    
    
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
        "ca8":12,"ca8pr":13,"ca12ft":14,"ca12mdft":15}

    jtypes = []
    jtypetrans = []
    jtypesToI = []    
    if isData[0] == 0: 
        jtypes = jtypes_m
        jtypetrans = jtypetrans_m
        jtypesToI = jtypesToI_m    
    if isData[0] > 0: 
        jtypes = jtypes_d
        jtypetrans = jtypetrans_d
        jtypesToI = jtypesToI_d 

    pt_binLo = [125,125,150,200,300]
    pt_binHi = [1000,155,200,300,1000]
    
    ooo = oname+"_ch"+str(channel)+".root"
    fo = ROOT.TFile(ooo, "recreate")

    # ------------------------------------------------------
    ##### setting up the output histograms
    from ROOT import TH1F, TProfile
    # event quantities
    h_v_pt = ROOT.TH1F("h_v_pt","; V pT; count",100,0.,500.)
    h_v_mt = ROOT.TH1F("h_v_mt","; V mT; count",100,0.,200.)
    h_e_met = ROOT.TH1F("h_e_met","; MET; count",100,0.,200.)   
    h_e_nvert = ROOT.TH1F("h_e_nvert","; nvertex; count",40,0.,40.)   
    h_e_nvert_weighted = ROOT.TH1F("h_e_nvert_weighted","; nvertex; count",40,0.,40.)   
    h_l_pt = ROOT.TH1F("h_l_pt","; lepton pT; count",100,0.,300.)
    h_l_eta = ROOT.TH1F("h_l_eta","; lepton eta; count",100,-3.,3.)

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


    h_pt = []
    h_area = []   
    h_eta = []
    
    pr_ptBins = array( 'd', [ 125,150,175,200,225,250,275,300,350,425,500 ] )
    #pr_ptBins = [ 125,150,200,300,1000 ]
    npr_ptBins = 10
    for x in range(len(jtypes)):
        h_eta.append( ROOT.TH1F("h_"+jtypes[x]+"_eta",";jet eta; count",100,-3,3) )
        h_area.append( ROOT.TH1F("h_"+jtypes[x]+"_area",";jet area; count",150,0.,3.) )
        h_pt.append( ROOT.TH1F("h_"+jtypes[x]+"_pt",";jet pt; count",100,0,600) )
        # in bins of pT
        h_mass.append( ROOT.TH1F( "h_"+jtypes[x]+"_mass",";jet mass; count",30,0.,150 ))
        h_mass_0bin.append( ROOT.TH1F( "h_"+jtypes[x]+"_mass_0bin",";jet mass; count",30,0.,150 ))
        h_mass_1bin.append( ROOT.TH1F( "h_"+jtypes[x]+"_mass_1bin",";jet mass; count",30,0.,150 ))        
        h_mass_2bin.append( ROOT.TH1F( "h_"+jtypes[x]+"_mass_2bin",";jet mass; count",30,0.,150 ))        
        h_mass_3bin.append( ROOT.TH1F( "h_"+jtypes[x]+"_mass_3bin",";jet mass; count",30,0.,150 ))        
        h_mass_4bin.append( ROOT.TH1F( "h_"+jtypes[x]+"_mass_4bin",";jet mass; count",30,0.,150 ))        
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

            # if chain.eventClass == 1:
            additionalCuts = False
            if channel == 1 and chain.e_met > 35 and chain.l_pt > 35:   
                additionalCuts = True
            if channel == 2 and chain.e_met > 35 and chain.l_pt > 25:   
                additionalCuts = True
            if chain.e_class == channel and additionalCuts:
                           
                h_v_pt.Fill( chain.v_pt, curSF )
                h_v_mt.Fill( chain.v_mt, curSF )
                h_e_met.Fill( chain.e_met, curSF )
                h_e_nvert.Fill( chain.e_met )
                h_e_nvert_weighted.Fill( chain.e_met, curSF )
                h_l_pt.Fill( chain.l_pt, curSF )
                h_l_eta.Fill( chain.l_eta, curSF )   
                for jitr in range(len(jtypes)):
                    
                    cur_jpt = chain.GetLeaf("j_"+jtypes[jitr]+"_pt").GetValue()
                    
                    if cur_jpt > 125:
                    
                        cur_jm = chain.GetLeaf("j_"+jtypes[jitr]+"_mass").GetValue()
                        h_area[jitr].Fill( chain.GetLeaf("j_"+jtypes[jitr]+"_area").GetValue(), curSF )
                        h_eta[jitr].Fill( chain.GetLeaf("j_"+jtypes[jitr]+"_eta").GetValue(), curSF )                    
                        h_pt[jitr].Fill( cur_jpt, curSF )
                        h_mass[jitr].Fill( cur_jm, curSF )
                        if ( cur_jpt > pt_binLo[0] ) and ( cur_jpt < pt_binHi[0] ) : h_mass_0bin[jitr].Fill( cur_jm, curSF )
                        if ( cur_jpt > pt_binLo[1] ) and ( cur_jpt < pt_binHi[1] ) : h_mass_1bin[jitr].Fill( cur_jm, curSF )
                        if ( cur_jpt > pt_binLo[2] ) and ( cur_jpt < pt_binHi[2] ) : h_mass_2bin[jitr].Fill( cur_jm, curSF )                           
                        if ( cur_jpt > pt_binLo[3] ) and ( cur_jpt < pt_binHi[3] ) : h_mass_3bin[jitr].Fill( cur_jm, curSF )
                        if ( cur_jpt > pt_binLo[4] ) and ( cur_jpt < pt_binHi[4] ) : h_mass_4bin[jitr].Fill( cur_jm, curSF )
                    
                    
                        hrat_mass_ovAK5[jitr].Fill( cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak5"]]+"_mass").GetValue(), curSF )
                        hrat_mass_ovAK7[jitr].Fill( cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7"]]+"_mass").GetValue(), curSF )
                        hrat_mass_ovAK8[jitr].Fill( cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak8"]]+"_mass").GetValue(), curSF )
                        hrat_mass_ovCA8[jitr].Fill( cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ca8"]]+"_mass").GetValue(), curSF )
                        hrat_pt_ovAK5[jitr].Fill( cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak5"]]+"_pt").GetValue(), curSF )
                        hrat_pt_ovAK7[jitr].Fill( cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7"]]+"_pt").GetValue(), curSF )
                        hrat_pt_ovAK8[jitr].Fill( cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak8"]]+"_pt").GetValue(), curSF )
                        hrat_pt_ovCA8[jitr].Fill( cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ca8"]]+"_pt").GetValue(), curSF )
                        prPt_mass_ovAK5[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ak5"]]+"_pt").GetValue(), cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak5"]]+"_mass").GetValue() )
                        prPt_mass_ovAK7[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ak7"]]+"_pt").GetValue(), cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7"]]+"_mass").GetValue() )
                        prPt_mass_ovAK8[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ak8"]]+"_pt").GetValue(), cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak8"]]+"_mass").GetValue() )
                        prPt_mass_ovCA8[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ca8"]]+"_pt").GetValue(), cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ca8"]]+"_mass").GetValue() )
                        prPt_pt_ovAK5[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ak5"]]+"_pt").GetValue(), cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak5"]]+"_pt").GetValue() )
                        prPt_pt_ovAK7[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ak7"]]+"_pt").GetValue(), cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7"]]+"_pt").GetValue() )
                        prPt_pt_ovAK8[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ak8"]]+"_pt").GetValue(), cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak8"]]+"_pt").GetValue() )
                        prPt_pt_ovCA8[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ca8"]]+"_pt").GetValue(), cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ca8"]]+"_pt").GetValue() )
                    
                        ## for Gen, only compare against the same cone size
                        if isData[nfiles] == 0:
                            if (jtypes[jitr].find("ak5") >= 0) and chain.GetLeaf("j_"+jtypes[jtypesToI["ak5g"]]+"_mass").GetValue() > 0.:
                                #print "cur_jm: "+str(cur_jm)+", "+str(chain.GetLeaf("j_"+jtypes[jtypesToI["ak5g"]]+"_mass").GetValue())+", "+str(curSF)
                                hrat_mass_ovAK5g[jitr].Fill( cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak5g"]]+"_mass").GetValue(), curSF )
                                hrat_pt_ovAK5g[jitr].Fill( cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak5g"]]+"_pt").GetValue(), curSF )
                                prPt_mass_ovAK5g[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ak5g"]]+"_pt").GetValue(), cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak5g"]]+"_mass").GetValue() )
                                prPt_pt_ovAK5g[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ak5g"]]+"_pt").GetValue(), cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak5g"]]+"_pt").GetValue() )

                            if (jtypes[jitr].find("ak7") >= 0) and chain.GetLeaf("j_"+jtypes[jtypesToI["ak7g"]]+"_mass").GetValue() > 0.:                    
                                hrat_mass_ovAK7g[jitr].Fill( cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7g"]]+"_mass").GetValue(), curSF )                    
                                hrat_pt_ovAK7g[jitr].Fill( cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7g"]]+"_pt").GetValue(), curSF )                    
                                prPt_mass_ovAK7g[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ak7g"]]+"_pt").GetValue(), cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7g"]]+"_mass").GetValue() )                     
                                prPt_pt_ovAK7g[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ak7g"]]+"_pt").GetValue(), cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak7g"]]+"_pt").GetValue() )                    

                            if (jtypes[jitr].find("ak8") >= 0) and chain.GetLeaf("j_"+jtypes[jtypesToI["ak8g"]]+"_mass").GetValue() > 0.:                
                                    hrat_mass_ovAK8g[jitr].Fill( cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak8g"]]+"_mass").GetValue(), curSF )  
                                    hrat_pt_ovAK8g[jitr].Fill( cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak8g"]]+"_pt").GetValue(), curSF )
                                    prPt_mass_ovAK8g[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ak8g"]]+"_pt").GetValue(), cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak8g"]]+"_mass").GetValue() )
                                    prPt_pt_ovAK8g[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ak8g"]]+"_pt").GetValue(), cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ak8g"]]+"_pt").GetValue() )

                            if (jtypes[jitr].find("ca8") >= 0) and chain.GetLeaf("j_"+jtypes[jtypesToI["ca8g"]]+"_mass").GetValue() > 0.:                
                                hrat_mass_ovCA8g[jitr].Fill( cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI["ca8g"]]+"_mass").GetValue(), curSF )                    
                                hrat_pt_ovCA8g[jitr].Fill( cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ca8g"]]+"_pt").GetValue(), curSF )                                        
                                prPt_mass_ovCA8g[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ca8g"]]+"_pt").GetValue(), cur_jm/ chain.GetLeaf("j_"+jtypes[jtypesToI    ["ca8g"]]+"_mass").GetValue() )                    
                                prPt_pt_ovCA8g[jitr].Fill( chain.GetLeaf("j_"+jtypes[jtypesToI["ca8g"]]+"_pt").GetValue(), cur_jpt/ chain.GetLeaf("j_"+jtypes[jtypesToI["ca8g"]]+"_pt").GetValue() )                    
                           
    #################################################
    # Put into directories different channels
    print "Writing out the histograms into ", ooo
    fo.cd()
    h_v_pt.Write()
    h_v_mt.Write()
    h_e_met.Write()                            
    h_e_nvert.Write()                            
    h_e_nvert_weighted.Write()                            
    h_l_pt.Write()                            
    h_l_eta.Write()                                                            
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
                        
    fo.Close()

############################################################
############################################################




