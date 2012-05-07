#ifndef puReweighter_h
#define puReweighter_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <iostream>

#include "PhysicsTools/KinFitter/interface/TFitConstraintMGaus.h"
#include "PhysicsTools/KinFitter/interface/TFitConstraintM.h"
#include "PhysicsTools/KinFitter/interface/TFitConstraintEp.h"
#include "PhysicsTools/KinFitter/interface/TFitParticleEtEtaPhi.h"
#include "PhysicsTools/KinFitter/interface/TFitParticleCart.h"
#include "PhysicsTools/KinFitter/interface/TKinFitter.h"

#include "EffTableReader.h"
#include "EffTableLoader.h"

#include "PhysicsTools/Utilities/interface/Lumi3DReWeighting.h"
#include "PhysicsTools/Utilities/interface/LumiReweightingStandAlone.h"

class puReweighter {
    public :
    
    puReweighter(std::string inputname, std::string oname);
    double Get(double minus, double intime, double plus);
    double GetUp(double minus, double intime, double plus);
    double GetDown(double minus, double intime, double plus);   
    
    edm::Lumi3DReWeighting* LumiWeights_;
    edm::Lumi3DReWeighting* up_LumiWeights_;
    edm::Lumi3DReWeighting* dn_LumiWeights_;
};

#endif

#ifdef puReweighter_cxx
puReweighter::puReweighter(std::string mcfile, std::string datfile)
{
    
    LumiWeights_ = new edm::Lumi3DReWeighting(mcfile, datfile, "pileup", "pileup", "Weight_3D.root");
    LumiWeights_->weight3D_init( 1.08 );
    
    up_LumiWeights_ = new edm::Lumi3DReWeighting(mcfile, datfile, "pileup", "pileup", "Weight_3D_up.root");
    up_LumiWeights_->weight3D_init( 1.16 );
    
    dn_LumiWeights_ = new edm::Lumi3DReWeighting(mcfile, datfile, "pileup", "pileup", "Weight_3D_down.root");
    dn_LumiWeights_->weight3D_init( 1.00 );
    
}


#endif // #ifdef vJetSubstructureAnalysis_cxx
