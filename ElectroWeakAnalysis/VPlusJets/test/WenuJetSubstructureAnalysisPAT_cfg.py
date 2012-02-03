import FWCore.ParameterSet.Config as cms
import pprint
isMC = True

process = cms.Process("demo")

##---------  Load standard Reco modules ------------
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')



##----- this config frament brings you the generator information ----
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load("PhysicsTools.HepMCCandAlgos.genParticles_cfi")
process.load("Configuration.StandardSequences.Generator_cff")


##----- Detector geometry : some of these needed for b-tag -------
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Geometry.CMSCommonData.cmsIdealGeometryXML_cfi")
process.load("Geometry.CommonDetUnit.globalTrackingGeometry_cfi")
process.load("RecoMuon.DetLayers.muonDetLayerGeometry_cfi")


##----- B-tags --------------
process.load("RecoBTag.Configuration.RecoBTag_cff")


##----- Global tag: conditions database ------------
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

## import skeleton process
#from PhysicsTools.PatAlgos.patTemplate_cfg import *


############################################
if not isMC:
    process.GlobalTag.globaltag = 'GR_R_42_V19::All'
else:
    process.GlobalTag.globaltag = 'START42_V13::All'

OutputFileName = "demo.root"
numEventsToRun = 1000
############################################
########################################################################################
########################################################################################
# Configure to use PF2PAT jets instead of reco::Jets
#from PhysicsTools.PatAlgos.tools.pfTools import *
#usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC=isMC, postfix="")
#process.pfPileUp.Enable = True
#process.pfPileUp.checkClosestZVertex = cms.bool(False)
#process.pfPileUp.Vertices = cms.InputTag('primaryVertex')
#process.pfJets.doAreaFastjet = True
#process.pfJets.doRhoFastjet = False

########################################################################################
########################################################################################

##---------  W-->enu Collection ------------
process.load("ElectroWeakAnalysis.VPlusJets.WenuCollections_cfi")
process.load("ElectroWeakAnalysis.VPlusJets.WmunuCollections_cfi")

##---------  Jet Collection ----------------
process.load("ElectroWeakAnalysis.VPlusJets.JetCollections_cfi")

##---------  Vertex and track Collections -----------
process.load("ElectroWeakAnalysis.VPlusJets.TrackCollections_cfi")
#


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(numEventsToRun)
)

process.MessageLogger.destinations = ['cout', 'cerr']
process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

#process.options = cms.untracked.PSet( SkipEvent = cms.untracked.vstring('ProductNotFound')
#)
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(
 #   'file:ttbsm_42x_mc_16_1_pBY.root'
#    'file:pat_42x_fall11_89_1_5da.root'
   "/store/user/lpctlbsm/weizou/WW_TuneZ2_7TeV_pythia6_tauola/ttbsm_v9_Summer11-PU_S4_-START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_10_1_OKP.root",
   "/store/user/lpctlbsm/weizou/WW_TuneZ2_7TeV_pythia6_tauola/ttbsm_v9_Summer11-PU_S4_-START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_98_1_uE9.root",
   "/store/user/lpctlbsm/weizou/WW_TuneZ2_7TeV_pythia6_tauola/ttbsm_v9_Summer11-PU_S4_-START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_81_1_ITA.root"
 #   '/store/user/skhalil/DYJetsToLL_TuneD6T_M-50_7TeV-madgraph-tauola/shyft_414_v1/c43141acf8ecb16bf2b2a65d482d5d16/shyft_414patch1_mc_3_2_33t.root'
   #     '/store/data/Run2011A/SingleElectron/AOD/05Aug2011-v1/0000/00111ED4-C8BF-E011-BBC1-003048D43942.root',
 #       '/store/data/Run2011A/SingleElectron/AOD/05Aug2011-v1/0000/003EF3F8-B5BF-E011-8FF9-003048D439AA.root',

############ Techni-color samples ############################
##        '/store/user/andersj/Technirho_Wjj_4_2_3_SIM/Technirho_Wjj_4_2_3_AODSIM/f71d043e41acd38c60e3392468355a0e/tc_AODSIM_5_1_vVp.root',
##        '/store/user/andersj/Technirho_Wjj_4_2_3_SIM/Technirho_Wjj_4_2_3_AODSIM/f71d043e41acd38c60e3392468355a0e/tc_AODSIM_4_1_Yg1.root',
    
############ Summer11 W+jets samples ############################
 #      '/store/mc/Summer11/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/AODSIM/PU_S4_START42_V11-v1/0001/FED96BE1-859A-E011-836E-001A92971B56.root',
##        '/store/mc/Summer11/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/AODSIM/PU_S4_START42_V11-v1/0001/FED7DD5E-9D9A-E011-A3BD-002618943954.root',
) )



#### HLT configuration
##-------- Electron events of interest --------
#process.HLTEle =cms.EDFilter("HLTHighLevel",
#     TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
#     HLTPaths = cms.vstring("HLT_Photon15_Cleaned_L1R", "HLT_Ele15_*", "HLT_Ele17_*", "HLT_Ele22_*", "HLT_Ele25_*","HLT_Ele27_*", "HLT_Ele32_*"),
#     eventSetupPathsKey = cms.string(''),
#     andOr = cms.bool(True), #----- True = OR, False = AND between the HLTPaths
#     throw = cms.bool(False) # throw exception on unknown path names
# )


#process.tightElectrons.src= "selectedPatElectronsPFlow";
#process.tightElectrons.cut= " ";
#process.looseElectrons.src= "selectedPatElectronsLoosePFlow";
#process.looseElectrons.cut= " ";

#process.tightMuons.src= cms.InputTag("selectedPatMuonsPFlow");
#process.tightMuons.cut= cms.string(" ");
#process.looseMuons.src= cms.InputTag("selectedPatMuonsLoosePFlow");
#process.looseMuons.cut= cms.string(" ");
process.primaryVertex.src = cms.InputTag("goodOfflinePrimaryVertices");
process.primaryVertex.cut = cms.string(" ");
process.WToMunu.decay = cms.string("selectedPatMuonsPFlow patMETsPFlow");
#process.WToEnu.decay = cms.string("selectedPatElectronsPFlow patMETsPFlow");
process.WToEnu = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("selectedPatElectronsPFlow patMETs"),
## Note: the 'mt()' method doesn't compute the transverse mass correctly, so we have to do it by hand.
 #  cut = cms.string('daughter(0).pt >20 && daughter(1).pt >20  && sqrt(2*daughter(0).pt*daughter(1).pt*(1-cos(daughter(0).phi-daughter(1).phi)))>40'),
 cut = cms.string('1'),
      checkCharge = cms.bool(False),
)


process.bestWToEnu =cms.EDFilter("LargestPtCandViewSelector",
    maxNumber = cms.uint32(10),
    src = cms.InputTag("WToEnu")                 
)

## change the leptons collections, for the patTuples
process.electronFilter.src= cms.InputTag("selectedPatElectronsLoosePFlow");
process.looseElectronFilter.src= cms.InputTag("selectedPatElectronsLoosePFlow");
process.looseMuonFilter.src= cms.InputTag("selectedPatMuonsLoosePFlow");
process.muonFilter.src= cms.InputTag("selectedPatMuonsLoosePFlow");
process.myPartons.src= cms.InputTag("prunedGenParticles");
process.genParticlesForJets.src= cms.InputTag("prunedGenParticles");
process.ak5flavourByRef.jets= cms.InputTag("goodPatJetsPFlow");
##-------- Save V+jets trees --------
process.VplusJetSubstructure = cms.EDAnalyzer("VplusJetSubstructureAnalysis",   
                                              HistOutFile = cms.string( OutputFileName ),
                                              srcVectorBoson = cms.InputTag("bestWToEnu"),
                                              VBosonType     = cms.string('W'),
                                              LeptonType     = cms.string('electron'),    

                                              JetCollections = cms.vstring('goodPatJetsPFlow','goodPatJetsCA8PrunedPF','goodPatJetsCA8PF'),    
                                              
                                              srcMet = cms.InputTag("patMETsPFlow"),

                                              srcJetsforRho = cms.string("kt6PFJetsPFlow"),
                                              srcJetsforRho_lepIso = cms.string("kt6PFJetsPFlow"),
                                              srcPrimaryVertex = cms.InputTag("goodOfflinePrimaryVertices"),                               
                                              
                                              srcElectrons  = cms.InputTag("selectedPatElectronsPFlow"),
                                              
                                              runningOverMC = cms.bool(isMC),			
                                              runningOverAOD = cms.bool(False)	

                                              )



# Add the KT6 producer to the sequence
#getattr(process,"patPF2PATSequence").replace(
#    getattr(process,"pfNoElectron"),
#    getattr(process,"pfNoElectron")*process.kt6PFJets )


process.myseq = cms.Sequence(
    process.TrackVtxPath *
#    getattr(process,"patPF2PATSequence") *
#    process.HLTEle *
#    process.WPath *
    process.WToEnu *
    process.bestWToEnu*
#    VetoSequence*                  

    process.GenJetPath *
##    process.btagging * 
    process.TagJetPath 
#    process.PFJetPath *
#    process.CorPFJetPath
    )

process.myseq.remove ( process.tightElectrons)
process.myseq.remove ( process.looseElectrons)
process.myseq.remove ( process.tightMuons)
process.myseq.remove ( process.looseMuons)

if isMC:
    process.myseq.remove ( process.noscraping)
    process.myseq.remove ( process.HBHENoiseFilter)
 #   process.myseq.remove ( process.HLTEle)
else:
    process.myseq.remove ( process.noscraping)
    process.myseq.remove ( process.HBHENoiseFilter)
    process.myseq.remove ( process.GenJetPath)
    process.myseq.remove ( process.TagJetPath)


##---- if do not want to require >= 2 jets then disable that filter ---
##process.myseq.remove ( process.RequireTwoJets)  

#process.outpath.remove(process.out)
process.p = cms.Path( process.myseq  * process.VplusJetSubstructure)






