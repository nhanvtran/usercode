from ROOT import gROOT, gStyle, gSystem, TLatex
import subprocess

############################################################
############################################################

def processNtuples(dirname,oname,isData):
    print  "setup has been done for inputs "+dirname+"\n"
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
    if isData == 0: 
        jtypes = jtypes_m
        jtypetrans = jtypetrans_m
        jtypesToI = jtypesToI_m    
    if isData > 0: 
        jtypes = jtypes_d
        jtypetrans = jtypetrans_d
        jtypesToI = jtypesToI_d    
    
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
    #ROOT.gSystem.Load("libPhysicsToolsUtilities.so");
    ROOT.gSystem.Load("libPhysicsToolsKinFitter.so");
    gROOT.ProcessLine(".include ../../../..");

    #ROOT.gSystem.Load('libFWCoreUtilities')
    #ROOT.gSystem.Load('libPhysicsToolsUtilities')
    gROOT.ProcessLine(".include ../../../..")
    #gROOT.ProcessLine("#include <iostream>");
    #gROOT.ProcessLine('.L LumiReweightingStandAlone.h+')
    gROOT.ProcessLine('.L puReweighter.C+')
    gROOT.ProcessLine('.L EffTableReader.cc+')
    gROOT.ProcessLine('.L EffTableLoader.cc+')
    from ROOT import EffTableReader, EffTableLoader   


    
    from ROOT import puReweighter

    #################################################
    fDir = "EfficiencesAndCorrections/";
    # ---------- Set up PU reweighting
    puWeights = ROOT.puReweighter(fDir+"PUMC_dist.root", fDir+"PUData_dist.root")
    
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
    muIDEff = EffTableLoader(            fDir + "muonEffsRecoToIso_ScaleFactors.txt");
    muHLTEff = EffTableLoader(           fDir + "muonEffsIsoToHLT_data_LP_LWA.txt");
    eleIdEff = EffTableLoader(           fDir + "eleEffsRecoToWP80_ScaleFactors.txt");
    eleRecoEff = EffTableLoader(         fDir + "eleEffsSCToReco_ScaleFactors.txt");
    eleHLTEff = EffTableLoader(          fDir + "eleEffsSingleElectron.txt");
    eleJ30Eff = EffTableLoader(          fDir + "FullyEfficient.txt");
    eleJ25NoJ30Eff = EffTableLoader(     fDir + "FullyEfficient_Jet2NoJet1.txt");
    eleMHTEff = EffTableLoader(          fDir + "FullyEfficient_MHT.txt");
    eleWMtEff = EffTableLoader(          fDir + "WMt50TriggerEfficiency.txt");
    #################################################   
    

    # ------------------------------------------------------
    ##### setting up the output tree
    # list of arrays
    # need an array for the pointer to make a tree
    v_mt_ = array( 'f', [ 0. ] )
    #v_mt_ = n.zeros( 1, dtype=float )
    v_pt_ = array( 'f', [ 0. ] )
    l_pt_ = array( 'f', [ 0. ] )
    l_eta_ = array( 'f', [ 0. ] )
    l_phi_ = array( 'f', [ 0. ] )    
    e_met_ = array( 'f', [ 0. ] )
    e_nvert_ = array( 'f', [ 0. ] )    
    e_effwt_ = array( 'f', [ 0. ] )    
    e_puwt_ = array( 'f', [ 0. ] )    
    e_puwt_up_ = array( 'f', [ 0. ] )    
    e_puwt_dn_ = array( 'f', [ 0. ] )    
    j_ca8pr_m1_ = array( 'f', [ 0. ] )    
    j_ca8pr_m2_ = array( 'f', [ 0. ] )    
    j_mass_ = []
    j_eta_ = []
    j_phi_ = []
    j_pt_ = []
    j_area_ = []
    j_jecfactor_ = []
    j_nJ_ = []
    for x in range(len(jtypes)):
        j_mass_.append( array( 'f', [ 0. ] ) )
        j_eta_.append( array( 'f', [ 0. ] ) )
        j_phi_.append( array( 'f', [ 0. ] ) )
        j_pt_.append( array( 'f', [ 0. ] ) )
        j_area_.append( array( 'f', [ 0. ] ) )
        j_jecfactor_.append( array( 'f', [ 0. ] ) )
        j_nJ_.append( array( 'f', [ 0. ] ) )

    to.Branch("v_mt", v_mt_ , "v_mt/F")
    to.Branch("v_pt", v_pt_ , "v_pt/F")
    to.Branch("l_pt", l_pt_ , "l_pt/F")
    to.Branch("l_eta", l_eta_ , "l_eta/F")
    to.Branch("l_phi", l_phi_ , "l_phi/F")
    to.Branch("e_met", e_met_ , "e_met/F")
    to.Branch("e_nvert", e_nvert_ , "e_nvert/F")
    to.Branch("j_ca8pr_m1", j_ca8pr_m1_ , "j_ca8pr_m1/F")
    to.Branch("j_ca8pr_m2", j_ca8pr_m2_ , "j_ca8pr_m2/F")
    to.Branch("e_effwt", e_effwt_ , "e_effwt/F")
    to.Branch("e_puwt", e_puwt_ , "e_puwt/F")    
    to.Branch("e_puwt_up", e_puwt_up_ , "e_puwt_up/F")
    to.Branch("e_puwt_dn", e_puwt_dn_ , "e_puwt_dn/F")
    for i in range(len(jtypes)):
        #print jtypes[i], " corresponds to ", jtypetrans[jtypes[i]]
        to.Branch("j_"+jtypes[i]+"_mass", j_mass_[i], "j_"+jtypes[i]+"_mass/F")
        to.Branch("j_"+jtypes[i]+"_eta", j_eta_[i], "j_"+jtypes[i]+"_eta/F")
        to.Branch("j_"+jtypes[i]+"_phi", j_phi_[i], "j_"+jtypes[i]+"_phi/F")
        to.Branch("j_"+jtypes[i]+"_pt", j_pt_[i], "j_"+jtypes[i]+"_pt/F")
        to.Branch("j_"+jtypes[i]+"_area", j_area_[i], "j_"+jtypes[i]+"_area/F")
        to.Branch("j_"+jtypes[i]+"_jecfactor", j_jecfactor_[i], "j_"+jtypes[i]+"_jecfactor/F")
        to.Branch("j_"+jtypes[i]+"_nJ", j_jecfactor_[i], "j_"+jtypes[i]+"_nJ/F")

    # ------------------------------------------------------
    
    chain = ROOT.TChain("VJetSubstructure","VJetSubstructure")
    chain.Add(dirname)
    
    entries = chain.GetEntries()
    print "total entries = " + str(entries)
    #if entries > 50000: entries = 50000
    #entries = 10
         
    ###for envent in chain:
    #$getattr(ws, "import")(...)
    for i in xrange(entries):
        if i%10000 == 0:   
            print "Entry: " + str(i)

        chain.GetEntry( i )
        # Selection for the Wenu events
        if chain.eventClass == 1 and chain.Wel_electron_isWP80 and chain.Wel_electron_pt > 35 and chain.Wel_pt > 120: 

            v_mt_[0] = chain.Wel_mt
            v_pt_[0] = chain.Wel_pt
            l_pt_[0] = chain.Wel_electron_pt
            l_eta_[0] = chain.Wel_electron_eta    
            l_phi_[0] = chain.Wel_electron_phi    
            e_met_[0] = chain.event_met_pfmet
            e_nvert_[0] = float(chain.event_nPV)
            j_ca8pr_m1_[0] = chain.GetLeaf("JetCA8PRUNEDPF_subJet1Mass").GetValue(0)
            j_ca8pr_m2_[0] = chain.GetLeaf("JetCA8PRUNEDPF_subJet2Mass").GetValue(0)
                        
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
                        j_jecfactor_[jitr][0] = factor                    
                    else:
                        j_mass_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Mass").GetValue(0)
                        j_eta_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Eta").GetValue(0)
                        j_phi_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Phi").GetValue(0)
                        j_pt_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Pt").GetValue(0)
                        j_jecfactor_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_JecFactor").GetValue(0)

                    j_area_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Area").GetValue(0)
                    j_nJ_[jitr][0] = float( chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_nJets").GetValue() )
                
                # gen jets, have to do matching
                elif (jtypes[jitr].find("g") > 0) and (isData == 0): 
                    # get matching reco collection
                    scur = jtypes[jitr]
                    scur = scur[:-1]
                    # loop through gen jets and find closest Dr
                    #                            Double_t deta = JetCA8PF_Eta[0]-JetCA8GENJETSNONU_Eta[k];
                    #   Double_t dphi = TVector2::Phi_mpi_pi(JetCA8PF_Phi[0]-JetCA8GENJETSNONU_Phi[k]);
                    #   double deltaR = TMath::Sqrt( deta*deta+dphi*dphi );
                    #   //std::cout << "deltaR (ca8): " << deltaR << std::endl;
                    #   if (deltaR < 0.3 && deltaR < toler){ matchIndex_ca8 = k; toler = deltaR; }
                    toler = 100.
                    matchindex = -1
                    for k in range(6):
                        #print jtypetrans[jtypes[jtypesToI[scur]]]
                        deta = chain.GetLeaf("Jet"+jtypetrans[jtypes[jtypesToI[scur]]]+"_Eta").GetValue(0) - chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_Eta").GetValue(k)
                        #print str(deta)
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
                        j_jecfactor_[jitr][0] = chain.GetLeaf("Jet"+jtypetrans[jtypes[jitr]]+"_JecFactor").GetValue(matchindex)    

                else: continue
            # ------------------   
            ## Wenu efficiencies
            eff_eleid = eleIdEff.GetEfficiency(l_pt_[0], l_eta_[0])
            eff_elereco = eleRecoEff.GetEfficiency(l_pt_[0], l_eta_[0])
            eff_elehlt = eleHLTEff.GetEfficiency(l_pt_[0], l_eta_[0])
            eff_elemht = eleMHTEff.GetEfficiency(e_met_[0], 0)
            eff_elewmt = eleWMtEff.GetEfficiency(v_mt_[0], l_eta_[0])
            e_effwt_[0] = eff_eleid*eff_elereco*eff_elehlt*eff_elemht*eff_elewmt
            # ------------------  
            ## PU weights
            if isData == 0:
                e_puwt_[0] = puWeights.Get( chain.GetLeaf("event_mcPU_nvtx").GetValue(0), chain.GetLeaf("event_mcPU_nvtx").GetValue(1), chain.GetLeaf("event_mcPU_nvtx").GetValue(2) )
                e_puwt_up_[0] = puWeights.GetUp( chain.GetLeaf("event_mcPU_nvtx").GetValue(0), chain.GetLeaf("event_mcPU_nvtx").GetValue(1), chain.GetLeaf("event_mcPU_nvtx").GetValue(2) )
                e_puwt_dn_[0] = puWeights.GetDown( chain.GetLeaf("event_mcPU_nvtx").GetValue(0), chain.GetLeaf("event_mcPU_nvtx").GetValue(1), chain.GetLeaf("event_mcPU_nvtx").GetValue(2) )        
            else:         
                e_puwt_[0] = -1.
                e_puwt_up_[0] = -1.  
                e_puwt_dn_[0] = -1.
                    
            to.Fill()
    
    print "Writing out the reduce analysis tuples into ", oname
    fo.cd()
    to.Write()        
    fo.Close()

############################################################
############################################################




