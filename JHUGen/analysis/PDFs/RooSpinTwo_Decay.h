/*****************************************************************************
 * Project: RooFit                                                           *
 *                                                                           *
 * This code was autogenerated by RooClassFactory                            * 
 *****************************************************************************/

#ifndef ROOSPINTWO_DECAY
#define ROOSPINTWO_DECAY

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooCategoryProxy.h"
#include "RooAbsReal.h"
#include "RooAbsCategory.h"

using namespace TMath;

class RooSpinTwo_Decay : public RooAbsPdf {
public:
    RooSpinTwo_Decay() {} ; 
    RooSpinTwo_Decay(const char *name, const char *title,
                RooAbsReal& _mzz,
                RooAbsReal& _m1,
                RooAbsReal& _m2,
                RooAbsReal& _h1,
                RooAbsReal& _h2,
                RooAbsReal& _Phi,
		RooAbsReal& _c1Val,
		RooAbsReal& _c2Val,
		RooAbsReal& _c3Val,
		RooAbsReal& _c4Val,
		RooAbsReal& _c5Val,
		RooAbsReal& _c6Val,
		RooAbsReal& _c7Val,
		RooAbsReal& _useGTerm,
		RooAbsReal& _g1Val,
		RooAbsReal& _g2Val,
		RooAbsReal& _g3Val,
		RooAbsReal& _g4Val,
		RooAbsReal& _g5Val,
		RooAbsReal& _g6Val,
		RooAbsReal& _g7Val,
		RooAbsReal& _g8Val,
		RooAbsReal& _g9Val,
		RooAbsReal& _g10Val,
		RooAbsReal& _fz1Val,
		RooAbsReal& _fz2Val,
                RooAbsReal& _R1Val,
		RooAbsReal& _R2Val,
		RooAbsReal& _mZ,
   	        RooAbsReal& _gamZ
		);

    RooSpinTwo_Decay(const RooSpinTwo_Decay& other, const char* name=0) ;
    virtual TObject* clone(const char* newname) const { return new RooSpinTwo_Decay(*this,newname); }
    inline virtual ~RooSpinTwo_Decay() { }
    
    Int_t getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* rangeName=0) const ;
    Double_t analyticalIntegral(Int_t code, const char* rangeName=0) const ;
    
protected:
    
    RooRealProxy mzz ;
    RooRealProxy m1 ;
    RooRealProxy m2 ;
    RooRealProxy h1 ;
    RooRealProxy h2 ;
    RooRealProxy Phi ;
    RooRealProxy c1Val;
    RooRealProxy c2Val;
    RooRealProxy c3Val;
    RooRealProxy c4Val;
    RooRealProxy c5Val;
    RooRealProxy c6Val;
    RooRealProxy c7Val;
    RooRealProxy useGTerm;
    RooRealProxy g1Val;
    RooRealProxy g2Val;
    RooRealProxy g3Val;
    RooRealProxy g4Val;
    RooRealProxy g5Val;
    RooRealProxy g6Val;
    RooRealProxy g7Val;
    RooRealProxy g8Val;
    RooRealProxy g9Val;
    RooRealProxy g10Val;
    RooRealProxy fz1Val ;
    RooRealProxy fz2Val ;
    RooRealProxy R1Val ;
    RooRealProxy R2Val ;
    RooRealProxy mZ;
    RooRealProxy gamZ;
    
    
    Double_t evaluate() const ;
    
private:
    
    //    ClassDef(RooSpinTwo_Decay,1) // Your description goes here...
};

#endif
