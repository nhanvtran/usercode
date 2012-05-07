#define puReweighter_cxx
#include "puReweighter.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <iostream>


//#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
//#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"

using namespace std;

double puReweighter::Get( double minus, double intime, double plus)
{
    
    double e_puwt =  LumiWeights_->weight3D(minus, intime, plus);   
    return e_puwt;
}
double puReweighter::GetUp( double minus, double intime, double plus)
{
    
    double e_puwt =  up_LumiWeights_->weight3D(minus, intime, plus);   
    return e_puwt;
}
double puReweighter::GetDown( double minus, double intime, double plus)
{
    
    double e_puwt =  dn_LumiWeights_->weight3D(minus, intime, plus);   
    return e_puwt;
}
