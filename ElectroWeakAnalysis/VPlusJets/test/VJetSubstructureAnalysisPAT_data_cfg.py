import FWCore.ParameterSet.Config as cms
import pprint
#isMC = True
isMC = False

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
numEventsToRun = 10000
############################################

##---------  W-->enu Collection ------------
process.load("ElectroWeakAnalysis.VPlusJets.WenuCollections_cfi")
process.load("ElectroWeakAnalysis.VPlusJets.WmunuCollections_cfi")
process.load("ElectroWeakAnalysis.VPlusJets.ZeeCollections_cfi")
process.load("ElectroWeakAnalysis.VPlusJets.ZmumuCollections_cfi")

##---------  Jet Collection ----------------
#process.load("ElectroWeakAnalysis.VPlusJets.JetCollections_cfi")

##---------  Vertex and track Collections -----------
#process.load("ElectroWeakAnalysis.VPlusJets.TrackCollections_cfi")
#


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(numEventsToRun)
)

process.MessageLogger.destinations = ['cout', 'cerr']
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

#process.options = cms.untracked.PSet( SkipEvent = cms.untracked.vstring('ProductNotFound')
#)
process.source = cms.Source("PoolSource", 
                            fileNames = cms.untracked.vstring(
#   "/store/user/lpctlbsm/weizou/WW_TuneZ2_7TeV_pythia6_tauola/ttbsm_v9_Summer11-PU_S4_-START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_10_1_OKP.root",
#   "/store/user/lpctlbsm/weizou/WW_TuneZ2_7TeV_pythia6_tauola/ttbsm_v9_Summer11-PU_S4_-START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_98_1_uE9.root",
#   "/store/user/lpctlbsm/weizou/WW_TuneZ2_7TeV_pythia6_tauola/ttbsm_v9_Summer11-PU_S4_-START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_81_1_ITA.root"

##### test data samples                                                                            
#    '/store/user/lpctlbsm/samvel/SingleElectron/tlbsm_v9_Summer11-PU_S4_START42_V11-v1_2011_10_12_21_06_34/f8e845a0332c56398831da6c30999af1/ttbsm_42x_data_428_1_upi.root'
## #v10
'/store/user/smpjs/ntran/SingleElectron/ttbsm_v10_SingleElectron_Run2011A-PromptReco-v4/2900f36c5423fd804f580f1efac6dc75/ttbsm_42x_data_157_1_enm.root',
                                                              #'/store/user/ntran/ntran/WW_TuneZ2_7TeV_pythia6_tauola/ttbsm_v10_v2_WW_TuneZ2_7TeV_pythia6_tauola/9b28f3f8b392373f53b6169b6cb537b0/ttbsm_42x_mc_10_1_ZKo.root'
                                                              #'file:ttbsm_42x_mc.root'
                                                              ) 
                            )



#### HLT configuration
##-------- Electron events of interest --------
process.HLTEle =cms.EDFilter("HLTHighLevel",
     TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
     HLTPaths = cms.vstring('HLT_Photon15_Cleaned_L1R', 'HLT_Ele15_*', 'HLT_Ele17_*', 'HLT_Ele22_*', 'HLT_Ele25_*','HLT_Ele27_*', 'HLT_Ele32_*','HLT_Mu9','HLT_Mu11','HLT_Mu13','HLT_Mu15_v*','HLT_Mu17_v*','HLT_Mu24_v*','HLT_Mu30_v*','HLT_IsoMu17_v*','HLT_IsoMu24_v*','HLT_IsoMu30_v*','HLT_Ele17_CaloIdL_CaloIsoVL_Ele8_CaloIdL_CaloIsoVL_v*','HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*'),
     eventSetupPathsKey = cms.string(''),
     andOr = cms.bool(True), #----- True = OR, False = AND between the HLTPaths
     throw = cms.bool(False) # throw exception on unknown path names
 )


##-------- Muon events of interest --------
#process.HLTMu =cms.EDFilter("HLTHighLevel",
#TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
#HLTPaths = cms.vstring('HLT_Mu9','HLT_Mu11','HLT_Mu13','HLT_Mu15_v*','HLT_Mu17_v*','HLT_Mu24_v*','HLT_Mu30_v*','HLT_IsoMu17_v*','HLT_IsoMu24_v*','HLT_IsoMu30_v*','HLT_DoubleMu*'),


##process.tightElectrons("selectedPatElectronsPFlow");
##-------- Save V+jets trees --------
process.VplusJetSubstructure = cms.EDAnalyzer("VplusJetSubstructureAnalysis",   
                                              HistOutFile = cms.string( OutputFileName ),
                                              srcVectorBosonWe = cms.InputTag("WToEnu"),
                                              srcVectorBosonWm = cms.InputTag("WToMunu"),
                                              srcVectorBosonZe = cms.InputTag("ZToEE"),
                                              srcVectorBosonZm = cms.InputTag("ZToMM"),
                                              VBosonType     = cms.string('W'),
                                              LeptonType     = cms.string('electron'),    

                                              PatJetCollections = cms.vstring('goodPatJetsPFlow','goodPatJetsCA8PrunedPF','goodPatJetsCA8PF','goodPatJetsCA12FilteredPF','goodPatJetsCA12MassDropFilteredPF'),    
                                              LiteJetCollections = cms.vstring('ak5TrimmedLite','ak5FilteredLite','ak5PrunedLite','ak7Lite','ak7TrimmedLite','ak7FilteredLite','ak7PrunedLite','ak8Lite','ak8TrimmedLite','ak8FilteredLite','ak8PrunedLite'),    
                                              #GenJetCollections = cms.vstring('ak5GenJetsNoNu','ak7GenJetsNoNu','ak8GenJetsNoNu','ca8GenJetsNoNu'),    
                                              GenJetCollections = cms.vstring(),    
                                              
                                              srcElectrons  = cms.InputTag("selectedPatElectronsPFlow"), # matches VBoson src
                                              srcMet = cms.InputTag("patMETsPFlow"),

                                              srcJetsforRho = cms.string("kt6PFJets"),
                                              srcJetsforRho_lepIso = cms.string("kt6PFJets"),
                                              srcPrimaryVertex = cms.InputTag("goodOfflinePrimaryVertices"),                               
                                              
                                              runningOverMC = cms.bool(isMC),			
                                              runningOverAOD = cms.bool(False)	

                                              )


process.myseq = cms.Sequence(
#    process.TrackVtxPath *
    process.HLTEle *
    process.WToMunu *
    process.ZToEE *
    process.ZToMM *
    process.WToEnu                             
                             #    process.bestWToEnu*
                             #    process.bestWmunu*
                             #    process.bestZee*
                             #    process.bestZmm*
                             #process.VetoSequence  

##    process.GenJetPath *
##    process.btagging * 
#    process.TagJetPath 
#    process.PFJetPath *
#    process.CorPFJetPath
    )

if isMC:
    process.myseq.remove ( process.HLTEle )



##---- if do not want to require >= 2 jets then disable that filter ---
##process.myseq.remove ( process.RequireTwoJets)  

#process.outpath.remove(process.out)
process.p = cms.Path( process.myseq  * process.VplusJetSubstructure)






