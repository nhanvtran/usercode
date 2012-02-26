# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.coreTools import *

###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register ('useData',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run this on real data")

options.register ('hltProcess',
                  'HLT',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "HLT process name to use.")

options.register ('writeFat',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Output tracks and PF candidates (and GenParticles for MC)")

options.register ('writeGenParticles',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Output GenParticles collection")

options.register ('use41x',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Use the 41x options")

options.register ('forceCheckClosestZVertex',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Force the check of the closest z vertex")


options.register ('useSusyFilter',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Use the SUSY event filter")

options.parseArguments()


if not options.useData :
    inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'])

    if options.use41x:
        process.source.fileNames = [
            '/store/relval/CMSSW_4_1_5/RelValTTbar/GEN-SIM-RECO/START311_V2-v1/0037/20A7B6E4-8F6C-E011-9E6B-003048678FE4.root',
            ]
    else :
	if not options.useSusyFilter :
		process.source.fileNames = [
			'/store/mc/Summer11/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/PU_S4_START42_V11-v1/0000/9AF32315-EC97-E011-8B25-0026189438B3.root',
			'/store/mc/Summer11/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/PU_S4_START42_V11-v1/0000/18F1D3EA-E597-E011-8452-00304867BFBC.root'
			]
	else :
		process.source.fileNames = [
			'/store/mc/Summer11/SMS-T2tt_Mstop-225to1200_mLSP-50to1025_7TeV-Pythia6Z/AODSIM/PU_START42_V11_FastSim-v1/0059/00A9721F-44CB-E011-A65A-002618943869.root',
			'/store/mc/Summer11/SMS-T2tt_Mstop-225to1200_mLSP-50to1025_7TeV-Pythia6Z/AODSIM/PU_START42_V11_FastSim-v1/0060/0001CFBE-E5CB-E011-B98A-00261894398B.root'
		]    
else :
    if options.use41x :
        inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual'])
        process.source.fileNames = [
            '/store/data/Run2011A/Jet/AOD/PromptReco-v2/000/163/738/70A9D7BA-D974-E011-8DD6-003048F118D2.root',
            '/store/data/Run2011A/Jet/AOD/PromptReco-v2/000/163/738/8A283D5E-D874-E011-B07B-0030487CD6B4.root',
            '/store/data/Run2011A/Jet/AOD/PromptReco-v2/000/163/738/A6773B09-0075-E011-B535-001D09F2423B.root',
            '/store/data/Run2011A/Jet/AOD/PromptReco-v2/000/163/738/C2A81E5B-D874-E011-9CC1-00304879FA4A.root',
            '/store/data/Run2011A/Jet/AOD/PromptReco-v2/000/163/738/EAE095DA-DB74-E011-9B0C-003048F1183E.root'

            ]
    else :
        inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual'])
        process.source.fileNames = [
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/FE6792BA-9A70-E011-940A-002618943970.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/FE0F23C8-9A70-E011-97A2-002618943821.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/FA7403C3-9A70-E011-BFE1-001A92810AA0.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/F4886DC3-9A70-E011-BCD1-003048679000.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/F232B0F1-9A70-E011-BA4E-003048678FE4.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/F0969EC4-9A70-E011-AAD9-003048678FC6.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/EEC627FE-9A70-E011-B1EA-0018F3D096C8.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/ECA837F0-9A70-E011-9637-002618943866.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/E6E258CD-9A70-E011-A3AB-001A92971B7C.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/E6249FB3-9A70-E011-88D9-003048678FB2.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/E25FFEE0-9A70-E011-BE2B-0018F3D0968A.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/E0D345D7-9A70-E011-BF5F-002618943957.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/D0EF4AC6-9A70-E011-ACD0-0026189437E8.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/CCFCF4BD-9A70-E011-B72A-0018F3D096B4.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/C68BFCEB-9A70-E011-A4BC-003048678B12.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/C04521C3-9A70-E011-9DC8-001A928116BC.root'
            ]

#process.source.eventsToProcess = cms.untracked.VEventRange( ['1:86747'] )

#process.source.skipEvents = cms.untracked.uint32(17268) 

print options

print 'Running jet corrections: '
print inputJetCorrLabel

import sys


###############################
####### Global Setup ##########
###############################


if not options.use41x :
    # 4.2.x configuration
    fileTag = '42x'
    if options.useData :
        process.GlobalTag.globaltag = cms.string( 'GR_R_42_V19::All' )
    else :
        process.GlobalTag.globaltag = cms.string( 'START42_V13::All' )

else :
    # 4.1.x configuration
    fileTag = '41x'
    if options.useData :
        process.GlobalTag.globaltag = cms.string('GR_R_41_V0::All')
    else :
        process.GlobalTag.globaltag = cms.string('START41_V0::All')



# require scraping filter
process.scrapingVeto = cms.EDFilter("FilterOutScraping",
                                    applyfilter = cms.untracked.bool(True),
                                    debugOn = cms.untracked.bool(False),
                                    numtrack = cms.untracked.uint32(10),
                                    thresh = cms.untracked.double(0.2)
                                    )
# HB + HE noise filtering
process.load('CommonTools/RecoAlgos/HBHENoiseFilter_cfi')
# Modify defaults setting to avoid an over-efficiency in the presence of OFT PU
process.HBHENoiseFilter.minIsolatedNoiseSumE = cms.double(999999.)
process.HBHENoiseFilter.minNumIsolatedNoiseChannels = cms.int32(999999)
process.HBHENoiseFilter.minIsolatedNoiseSumEt = cms.double(999999.)


# switch on PAT trigger
#from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
#switchOnTrigger( process, hltProcess=options.hltProcess )




###############################
####### DAF PV's     ##########
###############################

pvSrc = 'offlinePrimaryVertices'
if options.use41x :
    # redo DAF vertices
    process.load("RecoVertex.PrimaryVertexProducer.OfflinePrimaryVertices_cfi")
    

process.primaryVertexFilter = cms.EDFilter("GoodVertexFilter",
                                           vertexCollection = cms.InputTag("goodOfflinePrimaryVertices"),
                                           minimumNDOF = cms.uint32(3) , # this is > 3
                                           maxAbsZ = cms.double(24), 
                                           maxd0 = cms.double(2) 
                                           )




from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector

process.goodOfflinePrimaryVertices = cms.EDFilter(
    "PrimaryVertexObjectFilter",
    filterParams = pvSelector.clone( maxZ = cms.double(24.0),
                                     minNdof = cms.double(4.0) # this is >= 4
                                     ),
    src=cms.InputTag(pvSrc)
    )


###############################
########## Gen Setup ##########
###############################

process.load("RecoJets.Configuration.GenJetParticles_cff")
from RecoJets.JetProducers.ca4GenJets_cfi import ca4GenJets
process.ca8GenJetsNoNu = ca4GenJets.clone( rParam = cms.double(0.8),
                                           src = cms.InputTag("genParticlesForJetsNoNu"))

process.load("TopQuarkAnalysis.TopEventProducers.sequences.ttGenEvent_cff")

# add the flavor history
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryPaths_cfi")


# prune gen particles
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.prunedGenParticles = cms.EDProducer("GenParticlePruner",
                                            src = cms.InputTag("genParticles"),
                                            select = cms.vstring(
                                                "drop  *"
                                                ,"keep status = 3" #keeps  particles from the hard matrix element
                                                ,"keep (abs(pdgId) >= 11 & abs(pdgId) <= 16) & status = 1" #keeps e/mu and nus with status 1
                                                ,"keep (abs(pdgId)  = 15) & status = 3" #keeps taus
                                                )
                                            )


## process.prunedGenParticles = cms.EDProducer("GenParticlePruner",
##                                             src = cms.InputTag("genParticles"),
##                                             select = cms.vstring(
##                                                 "drop  *"
##                                                 ,"keep++ (abs(pdgId) =6) "
##                                                 )
##                                             )

###############################
#### Jet RECO includes ########
###############################

from RecoJets.JetProducers.SubJetParameters_cfi import SubJetParameters
from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoJets.JetProducers.CaloJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *
from RecoJets.JetProducers.CATopJetParameters_cfi import *
from RecoJets.JetProducers.GenJetParameters_cfi import *


###############################
########## PF Setup ###########
###############################

# Default PF2PAT with AK5 jets. Make sure to turn ON the L1fastjet stuff. 
from PhysicsTools.PatAlgos.tools.pfTools import *
postfix = "PFlow"
usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC=not options.useData, postfix=postfix)
process.pfPileUpPFlow.Enable = True
process.pfPileUpPFlow.Vertices = 'goodOfflinePrimaryVertices'
process.pfElectronsFromVertexPFlow.vertices = 'goodOfflinePrimaryVertices'
process.pfMuonsFromVertexPFlow.vertices = 'goodOfflinePrimaryVertices'

process.pfJetsPFlow.doAreaFastjet = True
process.pfJetsPFlow.doRhoFastjet = False
process.patJetCorrFactorsPFlow.payload = inputJetCorrLabel[0]
process.patJetCorrFactorsPFlow.levels = inputJetCorrLabel[1]
process.patJetCorrFactorsPFlow.rho = cms.InputTag("kt6PFJetsPFlow", "rho")
if not options.use41x and not options.forceCheckClosestZVertex :
    process.pfPileUpPFlow.checkClosestZVertex = False


# Adapt fine details of top projection for top group synchronization

#muons
process.isoValMuonWithNeutralPFlow.deposits[0].deltaR = 0.3
process.isoValMuonWithChargedPFlow.deposits[0].deltaR = 0.3
process.isoValMuonWithPhotonsPFlow.deposits[0].deltaR = 0.3
#electrons
process.isoValElectronWithNeutralPFlow.deposits[0].deltaR = 0.3
process.isoValElectronWithChargedPFlow.deposits[0].deltaR = 0.3
process.isoValElectronWithPhotonsPFlow.deposits[0].deltaR = 0.3

process.pfIsolatedMuonsPFlow.combinedIsolationCut = 0.2

process.pfNoTauPFlow.enable = False


# In order to have a coherent semileptonic channel also, add
# some "loose" leptons to do QCD estimates.
process.pfIsolatedMuonsLoosePFlow = process.pfIsolatedMuonsPFlow.clone(
    combinedIsolationCut = cms.double(999.0) 
    )




process.patMuonsLoosePFlow = process.patMuonsPFlow.clone(
   pfMuonSource = cms.InputTag("pfIsolatedMuonsLoosePFlow"),
   genParticleMatch = cms.InputTag("muonMatchLoosePFlow")
   )

tmp = process.muonMatchPFlow.src
adaptPFMuons( process, process.patMuonsLoosePFlow, "PFlow")
process.muonMatchPFlow.src = tmp

process.muonMatchLoosePFlow = process.muonMatchPFlow.clone(
    src = cms.InputTag("pfIsolatedMuonsLoosePFlow")
    )
process.muonMatchPFlow.src = "pfIsolatedMuonsPFlow"

process.selectedPatMuonsLoosePFlow = process.selectedPatMuonsPFlow.clone(
    src = cms.InputTag("patMuonsLoosePFlow")
    )



process.pfIsolatedElectronsLoosePFlow = process.pfIsolatedElectronsPFlow.clone(
    combinedIsolationCut = cms.double(999.0) 
    )

process.patElectronsLoosePFlow = process.patElectronsPFlow.clone(
    pfElectronSource = cms.InputTag("pfIsolatedElectronsLoosePFlow")
    )
adaptPFElectrons( process, process.patElectronsLoosePFlow, "PFlow")

process.selectedPatElectronsLoosePFlow = process.selectedPatElectronsPFlow.clone(
    src = cms.InputTag("patElectronsLoosePFlow")
    )


process.looseLeptonSequence = cms.Sequence(
    process.pfIsolatedMuonsLoosePFlow +
    process.muonMatchLoosePFlow +
    process.patMuonsLoosePFlow +
    process.selectedPatMuonsLoosePFlow +    
    process.pfIsolatedElectronsLoosePFlow +
    process.patElectronsLoosePFlow +
    process.selectedPatElectronsLoosePFlow
    )


# turn to false when running on data
if options.useData :
    removeMCMatching( process, ['All'] )
    process.looseLeptonSequence.remove( process.muonMatchLoosePFlow )


###############################
###### Electron ID ############
###############################

# NOTE: ADDING THE ELECTRON IDs FROM CiC ----- USED WITH 42X 
    

process.load('RecoEgamma.ElectronIdentification.cutsInCategoriesElectronIdentificationV06_cfi')
process.eidCiCSequence = cms.Sequence(
    process.eidVeryLooseMC *
    process.eidLooseMC *
    process.eidMediumMC*
    process.eidTightMC *
    process.eidSuperTightMC *
    process.eidHyperTight1MC *
    process.eidHyperTight2MC *
    process.eidHyperTight3MC *
    process.eidHyperTight4MC
    )

for iele in [ process.patElectrons,
              process.patElectronsPFlow,
              process.patElectronsLoosePFlow ] :
        iele.electronIDSources = cms.PSet(
            eidVeryLooseMC = cms.InputTag("eidVeryLooseMC"),
            eidLooseMC = cms.InputTag("eidLooseMC"),
            eidMediumMC = cms.InputTag("eidMediumMC"),
            eidTightMC = cms.InputTag("eidTightMC"),
            eidSuperTightMC = cms.InputTag("eidSuperTightMC"),
            eidHyperTight1MC = cms.InputTag("eidHyperTight1MC"),
            eidHyperTight2MC = cms.InputTag("eidHyperTight2MC"),
            eidHyperTight3MC = cms.InputTag("eidHyperTight3MC"),
            eidHyperTight4MC = cms.InputTag("eidHyperTight4MC")        
            )


###############################
###### Bare KT 0.6 jets #######
###############################

from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets
process.kt6PFJetsPFlowVoronoi = kt4PFJets.clone(
    rParam = cms.double(0.6),
    src = cms.InputTag('pfNoElectron'+postfix),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True),
    Rho_EtaMax = cms.double(6.0),
    voronoiRfact = cms.double(0.9)
    )
process.kt6PFJetsVoronoi = kt4PFJets.clone(
    rParam = cms.double(0.6),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True),
    Rho_EtaMax = cms.double(6.0),
    voronoiRfact = cms.double(0.9)
    )

process.kt6PFJets = kt4PFJets.clone(
    rParam = cms.double(0.6),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True)
    )
process.kt6PFJetsPFlow = kt4PFJets.clone(
    rParam = cms.double(0.6),
    src = cms.InputTag('pfNoElectron'+postfix),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True)
    )
process.kt4PFJetsPFlow = kt4PFJets.clone(
    rParam = cms.double(0.4),
    src = cms.InputTag('pfNoElectron'+postfix),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True)
    )

###############################
###### Bare CA 0.8 jets #######
###############################
from RecoJets.JetProducers.ca4PFJets_cfi import ca4PFJets
process.ca8PFJetsPFlow = ca4PFJets.clone(
    rParam = cms.double(0.8),
    src = cms.InputTag('pfNoElectron'+postfix),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True),
    Rho_EtaMax = cms.double(6.0),
    Ghost_EtaMax = cms.double(7.0)
    )

###############################
###### Jet Pruning Setup ######
###############################
from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *
from RecoJets.JetProducers.ak5PFJets_cfi import ak5PFJets
process.ak5PrunedPFlow = ak5PFJets.clone(
                                  SubJetParameters,
                                               src = cms.InputTag('pfNoElectron'+postfix),
                                               usePruning = cms.bool(True),
                                               useExplicitGhosts = cms.bool(True),
                                               writeCompound = cms.bool(True),
                                               jetCollInstanceName=cms.string("SubJets")
                                               )
process.ak5TrimmedPFlow = ak5PFJets.clone(
                                                src = cms.InputTag('pfNoElectron'+postfix),
                                                useTrimming = cms.bool(True),
                                                rFilt = cms.double(0.2),
                                                trimPtFracMin = cms.double(0.03),
                                                useExplicitGhosts = cms.bool(True)
                                   )
process.ak5FilteredPFlow = ak5PFJets.clone(
                                                 src = cms.InputTag('pfNoElectron'+postfix),
                                                 useFiltering = cms.bool(True),
                                                 nFilt = cms.int32(3),
                                                 rFilt = cms.double(0.3),
                                                 useExplicitGhosts = cms.bool(True),
                                                 writeCompound = cms.bool(True)
                                    )
process.ca8PrunedPFlow = process.ak5PrunedPFlow.clone(
                                                        jetAlgorithm = cms.string("CambridgeAachen"),
                                                        rParam       = cms.double(0.8)
                                                        )
process.ca8TrimmedPFlow = process.ak5TrimmedPFlow.clone(
                                                        jetAlgorithm = cms.string("CambridgeAachen"),
                                                        rParam       = cms.double(0.8)
                                                        )
######################################
##### DEPRECATED
## Pruned PF Jets
######################################

###############################
#### CATopTag Setup ###########
###############################

# CATopJet PF Jets
# with adjacency 



# CATopJet PF Jets

for ipostfix in [postfix] :
    for module in (
        getattr(process,"kt6PFJets"),
#        getattr(process,"kt6PFJetsVoronoi"),
        getattr(process,"kt6PFJets" + ipostfix),
        getattr(process,"kt4PFJets" + ipostfix),
#        getattr(process,"kt6PFJets" + ipostfix + "Voronoi"),
        getattr(process,"ca8PFJets" + ipostfix),        
                   getattr(process,"ak5Trimmed" + ipostfix),
                   getattr(process,"ak5Pruned" + ipostfix),
                   getattr(process,"ak5Filtered" + ipostfix),
                   getattr(process,"ca8Trimmed" + ipostfix),
                   getattr(process,"ca8Pruned" + ipostfix)
        ) :
        getattr(process,"patPF2PATSequence"+ipostfix).replace( getattr(process,"pfNoElectron"+ipostfix), getattr(process,"pfNoElectron"+ipostfix)*module )


# Use the good primary vertices everywhere. 
for imod in [process.patMuonsPFlow,
             process.patMuonsLoosePFlow,
             process.patElectronsPFlow,
             process.patElectronsLoosePFlow,
             process.patMuons,
             process.patElectrons] :
    imod.pvSrc = "goodOfflinePrimaryVertices"
    imod.embedTrack = True
    

addJetCollection(process, 
                 cms.InputTag('ca8PFJetsPFlow'),         # Jet collection; must be already in the event when patLayer0 sequence is executed
                 'CA8', 'PF',
                 doJTA=True,            # Run Jet-Track association & JetCharge
                 doBTagging=True,       # Run b-tagging
                 jetCorrLabel=inputJetCorrLabel,
                 doType1MET=False,
                 doL1Cleaning=False,
                 doL1Counters=False,
                 genJetCollection = cms.InputTag("ca8GenJetsNoNu"),
                 doJetID = False
                 )

################################## by Nhan
addJetCollection(process, 
#                 cms.InputTag('caPrunedPFlow'),         # Jet collection; must be already in the event when patLayer0 sequence is executed
                 cms.InputTag('ak5TrimmedPFlow'),         # Jet collection; must be already in the event when patLayer0 sequence is executed
                 'AK5Trimmed', 'PF',
                 doJTA=True,            # Run Jet-Track association & JetCharge
                 doBTagging=True,       # Run b-tagging
                 jetCorrLabel=inputJetCorrLabel,
                 doType1MET=False,
                 doL1Cleaning=False,
                 doL1Counters=False,
                 genJetCollection = cms.InputTag("ca8GenJetsNoNu"),
                 doJetID = False
                 )
addJetCollection(process, 
                 #                 cms.InputTag('caPrunedPFlow'),         # Jet collection; must be already in the event when patLayer0 sequence is executed
                 cms.InputTag('ak5PrunedPFlow'),         # Jet collection; must be already in the event when patLayer0 sequence is executed
                 'AK5Pruned', 'PF',
                 doJTA=True,            # Run Jet-Track association & JetCharge
                 doBTagging=True,       # Run b-tagging
                 jetCorrLabel=inputJetCorrLabel,
                 doType1MET=False,
                 doL1Cleaning=False,
                 doL1Counters=False,
                 genJetCollection = cms.InputTag("ca8GenJetsNoNu"),
                 doJetID = False
                 )
addJetCollection(process, 
                 #                 cms.InputTag('caPrunedPFlow'),         # Jet collection; must be already in the event when patLayer0 sequence is executed
                 cms.InputTag('ak5FilteredPFlow'),         # Jet collection; must be already in the event when patLayer0 sequence is executed
                 'AK5Filtered', 'PF',
                 doJTA=True,            # Run Jet-Track association & JetCharge
                 doBTagging=True,       # Run b-tagging
                 jetCorrLabel=inputJetCorrLabel,
                 doType1MET=False,
                 doL1Cleaning=False,
                 doL1Counters=False,
                 genJetCollection = cms.InputTag("ca8GenJetsNoNu"),
                 doJetID = False
                 )
addJetCollection(process, 
                 #                 cms.InputTag('caPrunedPFlow'),         # Jet collection; must be already in the event when patLayer0 sequence is executed
                 cms.InputTag('ca8TrimmedPFlow'),         # Jet collection; must be already in the event when patLayer0 sequence is executed
                 'CA8Trimmed', 'PF',
                 doJTA=True,            # Run Jet-Track association & JetCharge
                 doBTagging=True,       # Run b-tagging
                 jetCorrLabel=inputJetCorrLabel,
                 doType1MET=False,
                 doL1Cleaning=False,
                 doL1Counters=False,
                 genJetCollection = cms.InputTag("ca8GenJetsNoNu"),
                 doJetID = False
                 )
addJetCollection(process, 
                 #                 cms.InputTag('caPrunedPFlow'),         # Jet collection; must be already in the event when patLayer0 sequence is executed
                 cms.InputTag('ca8PrunedPFlow'),         # Jet collection; must be already in the event when patLayer0 sequence is executed
                 'CA8Pruned', 'PF',
                 doJTA=True,            # Run Jet-Track association & JetCharge
                 doBTagging=True,       # Run b-tagging
                 jetCorrLabel=inputJetCorrLabel,
                 doType1MET=False,
                 doL1Cleaning=False,
                 doL1Counters=False,
                 genJetCollection = cms.InputTag("ca8GenJetsNoNu"),
                 doJetID = False
                 )
################################## by Nhan



for icorr in [process.patJetCorrFactorsAK5TrimmedPF,
              process.patJetCorrFactorsAK5PrunedPF,
              process.patJetCorrFactorsAK5FilteredPF,
              process.patJetCorrFactorsCA8TrimmedPF,
              process.patJetCorrFactorsCA8PrunedPF,              
              process.patJetCorrFactorsCA8PF ] :
    icorr.rho = cms.InputTag("kt6PFJetsPFlow", "rho")


###############################
### TagInfo and Matching Setup#
###############################

# Do some configuration of the jet substructure things
        #for jetcoll in (process.patJetsPFlow,
        #       process.patJetsCA8PF,
        #        process.patJetCorrFactorsAK5TrimmedPF,
        #        process.patJetCorrFactorsAK5PrunedPF,
        #        process.patJetCorrFactorsAK5FilteredPF,
        #        process.patJetCorrFactorsCA8TrimmedPF,
        #        process.patJetCorrFactorsCA8PrunedPF,  
        #        process.patJetsCATopTagPF
#        ) :
        #...    if options.useData == False :
## see original for full stuff


#################################################
#### Fix the PV collections for the future ######
#################################################
for module in [process.patJetCorrFactors,
               process.patJetCorrFactorsPFlow,
               process.patJetCorrFactorsAK5TrimmedPF,
               process.patJetCorrFactorsAK5PrunedPF,
               process.patJetCorrFactorsAK5FilteredPF,
               process.patJetCorrFactorsCA8TrimmedPF,
               process.patJetCorrFactorsCA8PrunedPF,  
               process.patJetCorrFactorsCA8PF
               ]:
    module.primaryVertices = "goodOfflinePrimaryVertices"


###############################
#### Selections Setup #########
###############################

# AK5 Jets
process.selectedPatJetsPFlow.cut = cms.string("pt > 20 & abs(eta) < 2.5")
process.patJetsPFlow.addTagInfos = True
process.patJetsPFlow.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAODPFlow")
    )
process.patJetsPFlow.userData.userFunctions = cms.vstring( "? hasTagInfo('secondaryVertex') && tagInfoSecondaryVertex('secondaryVertex').nVertices() > 0 ? "
                                                      "tagInfoSecondaryVertex('secondaryVertex').secondaryVertex(0).p4().mass() : 0")
process.patJetsPFlow.userData.userFunctionLabels = cms.vstring('secvtxMass')

# CA8 jets
process.selectedPatJetsCA8PF.cut = cms.string("pt > 20 & abs(rapidity) < 2.5")

# CA8 Pruned jets
process.selectedPatJetsAK5TrimmedPF.cut = cms.string("pt > 20 & abs(rapidity) < 2.5")
process.selectedPatJetsAK5PrunedPF.cut = cms.string("pt > 20 & abs(rapidity) < 2.5")
process.selectedPatJetsAK5FilteredPF.cut = cms.string("pt > 20 & abs(rapidity) < 2.5")
process.selectedPatJetsCA8TrimmedPF.cut = cms.string("pt > 20 & abs(rapidity) < 2.5")
process.selectedPatJetsCA8PrunedPF.cut = cms.string("pt > 20 & abs(rapidity) < 2.5")


# electrons
process.selectedPatElectrons.cut = cms.string('pt > 10.0 & abs(eta) < 2.5')
process.patElectrons.embedTrack = cms.bool(True)
process.selectedPatElectronsPFlow.cut = cms.string('pt > 10.0 & abs(eta) < 2.5')
process.patElectronsPFlow.embedTrack = cms.bool(True)
process.selectedPatElectronsLoosePFlow.cut = cms.string('pt > 10.0 & abs(eta) < 2.5')
process.patElectronsLoosePFlow.embedTrack = cms.bool(True)
# muons
process.selectedPatMuons.cut = cms.string('pt > 10.0 & abs(eta) < 2.5')
process.patMuons.embedTrack = cms.bool(True)
process.selectedPatMuonsPFlow.cut = cms.string("pt > 10.0 & abs(eta) < 2.5")
process.patMuonsPFlow.embedTrack = cms.bool(True)
process.selectedPatMuonsLoosePFlow.cut = cms.string("pt > 10.0 & abs(eta) < 2.5")
process.patMuonsLoosePFlow.embedTrack = cms.bool(True)
# taus
process.selectedPatTausPFlow.cut = cms.string("pt > 10.0 & abs(eta) < 3")
process.selectedPatTaus.cut = cms.string("pt > 10.0 & abs(eta) < 3")
process.patTausPFlow.isoDeposits = cms.PSet()
process.patTaus.isoDeposits = cms.PSet()
# photons
process.patPhotonsPFlow.isoDeposits = cms.PSet()
process.patPhotons.isoDeposits = cms.PSet()


# Apply jet ID to all of the jets upstream. We aren't going to screw around
# with this, most likely. So, we don't really to waste time with it
# at the analysis level. 
from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector
process.goodPatJetsPFlow = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                        filterParams = pfJetIDSelector.clone(),
                                        src = cms.InputTag("selectedPatJetsPFlow")
                                        )
process.goodPatJetsCA8PF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                        filterParams = pfJetIDSelector.clone(),
                                        src = cms.InputTag("selectedPatJetsCA8PF")
                                        )
#####
process.goodPatJetsAK5TrimmedPF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                              filterParams = pfJetIDSelector.clone(),
                                              src = cms.InputTag("selectedPatJetsAK5TrimmedPF")
                                              )
process.goodPatJetsAK5PrunedPF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                              filterParams = pfJetIDSelector.clone(),
                                              src = cms.InputTag("selectedPatJetsAK5PrunedPF")
                                              )
process.goodPatJetsAK5FilteredPF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                              filterParams = pfJetIDSelector.clone(),
                                              src = cms.InputTag("selectedPatJetsAK5FilteredPF")
                                              )
process.goodPatJetsCA8TrimmedPF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                              filterParams = pfJetIDSelector.clone(),
                                              src = cms.InputTag("selectedPatJetsCA8TrimmedPF")
                                              )
process.goodPatJetsCA8PrunedPF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                              filterParams = pfJetIDSelector.clone(),
                                              src = cms.InputTag("selectedPatJetsCA8PrunedPF")
                                              )
#####


# let it run

process.patseq = cms.Sequence(
    process.scrapingVeto*
    process.HBHENoiseFilter*
    #process.offlinePrimaryVerticesDAF*    
    process.goodOfflinePrimaryVertices*
    process.primaryVertexFilter*
    process.genParticlesForJetsNoNu*
    process.ca8GenJetsNoNu*
    getattr(process,"patPF2PATSequence"+postfix)*
    process.looseLeptonSequence*
    process.patDefaultSequence*
    process.goodPatJetsPFlow*
    process.goodPatJetsCA8PF*
                              process.goodPatJetsAK5TrimmedPF*
                              process.goodPatJetsAK5PrunedPF*
                              process.goodPatJetsAK5FilteredPF*
                              process.goodPatJetsCA8TrimmedPF*
                              process.goodPatJetsCA8PrunedPF*
#    process.goodPatJetsCATopTagPF*
    process.flavorHistorySeq*
    process.prunedGenParticles
#    process.caPrunedGen*
#    process.caTopTagGen*
#    process.CATopTagInfosGen
    )


if options.use41x :

    process.patseq.replace( process.goodOfflinePrimaryVertices,
                            process.offlinePrimaryVertices*
                            process.goodOfflinePrimaryVertices *
                            process.eidCiCSequence )
else :
    process.patseq.replace( process.goodOfflinePrimaryVertices,
                            process.goodOfflinePrimaryVertices *
                            process.eidCiCSequence )

if options.useData == True :
    process.patseq.remove( process.genParticlesForJetsNoNu )
    process.patseq.remove( process.genJetParticles )    
    process.patseq.remove( process.ca8GenJetsNoNu )
    process.patseq.remove( process.flavorHistorySeq )
#    process.patseq.remove( process.caPrunedGen )
    process.patseq.remove( process.caTopTagGen )
    process.patseq.remove( process.CATopTagInfosGen )
    process.patseq.remove( process.prunedGenParticles )



if options.useSusyFilter :
	process.patseq.remove( process.HBHENoiseFilter )
	process.load( 'PhysicsTools.HepMCCandAlgos.modelfilter_cfi' )
	process.modelSelector.parameterMins = [500.,    0.] # mstop, mLSP
	process.modelSelector.parameterMaxs  = [7000., 200.] # mstop, mLSP
	process.p0 = cms.Path(
		process.modelSelector *
		process.patseq
	)



else :
	process.p0 = cms.Path(
		process.patseq
	)

process.out.SelectEvents.SelectEvents = cms.vstring('p0')

# rename output file
if options.useData :
    if options.writeFat :
        process.out.fileName = cms.untracked.string('ttbsm_' + fileTag + '_data_fat.root')
    else :
        process.out.fileName = cms.untracked.string('ttbsm_' + fileTag + '_data.root')
else :
    if options.writeFat :
        process.out.fileName = cms.untracked.string('ttbsm_' + fileTag + '_mc_fat.root')
    else :
        process.out.fileName = cms.untracked.string('ttbsm_' + fileTag + '_mc.root')


# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)


# process all the events
process.maxEvents.input = 10
process.options.wantSummary = True
process.out.dropMetaData = cms.untracked.string("DROPPED")


process.source.inputCommands = cms.untracked.vstring("keep *", "drop *_MEtoEDMConverter_*_*")



process.out.outputCommands = [
    'drop *_cleanPat*_*_*',
    'keep *_selectedPat*_*_*',
    'keep *_goodPat*_*_*',
    'drop patJets_selectedPat*_*_*',
    'drop *_selectedPatJets_*_*',    
    'keep *_patMETs*_*_*',
#    'keep *_offlinePrimaryVertices*_*_*',
#    'keep *_kt6PFJets*_*_*',
    'keep *_goodOfflinePrimaryVertices*_*_*',    
    'drop patPFParticles_*_*_*',
    'drop patTaus_*_*_*',
                              'keep recoPFJets_*Trimmed*_*_*',
                              'keep recoPFJets_*Pruned*_*_*',
                              'keep recoPFJets_*Filtered*_*_*',
    'keep recoPFJets_caTopTag*_*_*',
    'keep patTriggerObjects_patTriggerPFlow_*_*',
    'keep patTriggerFilters_patTriggerPFlow_*_*',
    'keep patTriggerPaths_patTriggerPFlow_*_*',
    'keep patTriggerEvent_patTriggerEventPFlow_*_*',
    'keep *_cleanPatPhotonsTriggerMatch*_*_*',
    'keep *_cleanPatElectronsTriggerMatch*_*_*',
    'keep *_cleanPatMuonsTriggerMatch*_*_*',
    'keep *_cleanPatTausTriggerMatch*_*_*',
    'keep *_cleanPatJetsTriggerMatch*_*_*',
    'keep *_patMETsTriggerMatch*_*_*',
    'keep double_*_*_PAT',
    'keep *_TriggerResults_*_*',
    'keep *_hltTriggerSummaryAOD_*_*',
    'keep *_ak5GenJetsNoNu_*_*',
    'keep *_ca8GenJetsNoNu_*_*',
    'keep *_caPrunedGen_*_*',
    'keep *_caTopTagPFlow_*_*',
    'keep *_CATopTagInfosPFlow_*_*',
    'keep *_prunedGenParticles_*_*',
    'drop recoPFCandidates_selectedPatJets*_*_*',
    'drop CaloTowers_selectedPatJets*_*_*'
    #'keep recoTracks_generalTracks_*_*'
    ]

if options.useData :
    process.out.outputCommands += ['drop *_MEtoEDMConverter_*_*',
                                   'keep LumiSummary_lumiProducer_*_*'
                                   ]
else :
    process.out.outputCommands += ['keep *_ca8GenJetsNoNu_*_*',
                                   'keep *_ak5GenJetsNoNu_*_*',                                   
                                   'keep GenRunInfoProduct_generator_*_*',
                                   'keep GenEventInfoProduct_generator_*_*',
                                   'keep *_flavorHistoryFilter_*_*',
                                   'keep PileupSummaryInfos_*_*_*'
                                   ]

if options.writeFat :

    process.out.outputCommands += [
        'keep *_pfNoElectron*_*_*',
        'keep recoTracks_generalTracks_*_*',
        'keep recoPFCandidates_selectedPatJets*_*_*',
        'keep recoBaseTagInfosOwned_selectedPatJets*_*_*',
        'keep CaloTowers_selectedPatJets*_*_*'
        ]
if options.writeFat or options.writeGenParticles :
    if options.useData == False :
        process.out.outputCommands += [
            'keep *_genParticles_*_*'
            ]

open('junk.py','w').write(process.dumpPython())
