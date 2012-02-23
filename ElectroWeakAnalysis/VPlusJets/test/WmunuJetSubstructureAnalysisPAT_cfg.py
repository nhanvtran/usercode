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

##---------  W-->enu Collection ------------
process.load("ElectroWeakAnalysis.VPlusJets.WenuCollections_cfi")
process.load("ElectroWeakAnalysis.VPlusJets.WmunuCollections_cfi")

##---------  Jet Collection ----------------
#process.load("ElectroWeakAnalysis.VPlusJets.JetCollections_cfi")

##---------  Vertex and track Collections -----------
#process.load("ElectroWeakAnalysis.VPlusJets.TrackCollections_cfi")
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
   "/store/user/lpctlbsm/weizou/WW_TuneZ2_7TeV_pythia6_tauola/ttbsm_v9_Summer11-PU_S4_-START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_10_1_OKP.root",
   "/store/user/lpctlbsm/weizou/WW_TuneZ2_7TeV_pythia6_tauola/ttbsm_v9_Summer11-PU_S4_-START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_98_1_uE9.root",
   "/store/user/lpctlbsm/weizou/WW_TuneZ2_7TeV_pythia6_tauola/ttbsm_v9_Summer11-PU_S4_-START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_81_1_ITA.root"
) )

#### HLT configuration
##-------- Muon events of interest --------
process.HLTMu =cms.EDFilter("HLTHighLevel",
                            TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
                            HLTPaths = cms.vstring('HLT_Mu9','HLT_Mu11','HLT_Mu13','HLT_Mu15_v*','HLT_Mu17_v*','HLT_Mu24_v*','HLT_Mu30_v*','HLT_IsoMu17_v*','HLT_IsoMu24_v*','HLT_IsoMu30_v*'),
                            eventSetupPathsKey = cms.string(''),
                            andOr = cms.bool(True), #----- True = OR, False = AND between the HLTPaths
                            throw = cms.bool(False) # throw exception on unknown path names
                            )

##process.tightElectrons("selectedPatElectronsPFlow");
##-------- Save V+jets trees --------
process.VplusJetSubstructure = cms.EDAnalyzer("VplusJetSubstructureAnalysis",   
                                              HistOutFile = cms.string( OutputFileName ),
                                              srcVectorBoson = cms.InputTag("bestWmunu"),
                                              VBosonType     = cms.string('W'),
                                              LeptonType     = cms.string('muon'),    

                                              JetCollections = cms.vstring('goodPatJetsPFlow','goodPatJetsCA8PrunedPF','goodPatJetsCA8PF'),    
                                              
                                              srcMet = cms.InputTag("patMETsPFlow"),

                                              srcJetsforRho = cms.string("kt6PFJetsPFlow"),
                                              srcJetsforRho_lepIso = cms.string("kt6PFJetsPFlow"),
                                              srcPrimaryVertex = cms.InputTag("goodOfflinePrimaryVertices"),                               
                                              
                                              srcElectrons  = cms.InputTag("selectedPatMuonsPFlow"),
                                              
                                              runningOverMC = cms.bool(isMC),			
                                              runningOverAOD = cms.bool(False)	

                                              )


process.myseq = cms.Sequence(
#    process.TrackVtxPath *
#    getattr(process,"patPF2PATSequence") *
#    process.HLTEle *
    process.WToMunu *
    process.bestWmunu*
    process.VetoSequence
                             
##    process.GenJetPath *
##    process.btagging * 
##    process.TagJetPath 
#    process.PFJetPath *
#    process.CorPFJetPath
    )


if isMC:
    process.myseq.remove ( process.HLTMu)


##---- if do not want to require >= 2 jets then disable that filter ---
##process.myseq.remove ( process.RequireTwoJets)  

#process.outpath.remove(process.out)
process.p = cms.Path( process.myseq  * process.VplusJetSubstructure)






