import FWCore.ParameterSet.Config as cms

WToMunu = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("selectedPatMuonsPFlow patMETsPFlow"),
## Note: the 'mt()' method doesn't compute the transverse mass correctly, so we have to do it by hand.
    cut = cms.string('daughter(0).pt >20 && daughter(1).pt >20  && sqrt(2*daughter(0).pt*daughter(1).pt*(1-cos(daughter(0).phi-daughter(1).phi)))>40'), 
    checkCharge = cms.bool(False),
)

bestWmunu = cms.EDFilter("LargestPtCandViewSelector",
    maxNumber = cms.uint32(10),
    src = cms.InputTag("WToMunu")
)


ElectronFilter = cms.EDFilter("PATCandViewCountFilter",
                              minNumber = cms.uint32(0),
                              maxNumber = cms.uint32(0),
                              src = cms.InputTag("selectedPatElectronsPFlow")                     
                              )

MuonFilter = cms.EDFilter("PATCandViewCountFilter",
                          minNumber = cms.uint32(1),
                          maxNumber = cms.uint32(1),
                          src = cms.InputTag("selectedPatMuonsPFlow")                     
                          )


VetoSequence = cms.Sequence( 
                            ElectronFilter *
                            MuonFilter
                            )



