import FWCore.ParameterSet.Config as cms


ZToMM = cms.EDProducer("CandViewShallowCloneCombiner",
                        decay = cms.string("selectedPatMuonsPFlow@+ selectedPatMuonsPFlow@-"),
                        cut = cms.string('60 < mass < 120'),
                        checkCharge = cms.bool(False),
                        )


bestZmm = cms.EDFilter("LargestPtCandViewSelector",
                       maxNumber = cms.uint32(1),
                       src = cms.InputTag("ZToMM")
                       )


ElectronFilter = cms.EDFilter("PATCandViewCountFilter",
                                   minNumber = cms.uint32(0),
                                   maxNumber = cms.uint32(10),
                                   src = cms.InputTag("selectedPatElectronsPFlow")                     
                                   )

MuonFilter = cms.EDFilter("PATCandViewCountFilter",
                               minNumber = cms.uint32(2),
                               maxNumber = cms.uint32(10),
                               src = cms.InputTag("selectedPatMuonsPFlow")                     
                               )


VetoSequence = cms.Sequence( 
                            ElectronFilter *
                            MuonFilter
                            )


