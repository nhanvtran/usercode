/*****************************************************************************
 * Project: RooFit                                                           *
 *                                                                           *
 * This code was autogenerated by RooClassFactory                            * 
 *****************************************************************************/

#ifndef ROOSPINTWOXZSZS_5D
#define ROOSPINTWOXZSZS_5D

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooCategoryProxy.h"
#include "RooAbsReal.h"
#include "RooAbsCategory.h"

class RooSpinTwoXZsZs : public RooAbsPdf {
public:
    RooSpinTwoXZsZs() {} ; 
    RooSpinTwoXZsZs(const char *name, const char *title,
                RooAbsReal& _mzz,
                RooAbsReal& _m1,
                RooAbsReal& _m2,
		RooAbsReal& _hs,
                RooAbsReal& _h1,
                RooAbsReal& _h2,
                RooAbsReal& _Phi,
                RooAbsReal& _Phi1,
		RooAbsReal& _c1,
		RooAbsReal& _phi1,
		RooAbsReal& _c2,
		RooAbsReal& _phi2,
		RooAbsReal& _c3,
		RooAbsReal& _phi3,
		RooAbsReal& _c4,
		RooAbsReal& _phi4,
		RooAbsReal& _c5,
		RooAbsReal& _phi5,
		RooAbsReal& _c6,
		RooAbsReal& _phi6,
		RooAbsReal& _c7,
		RooAbsReal& _phi7,
		RooAbsReal& _fz1Val,
		RooAbsReal& _fz2Val,
                RooAbsReal& _R1Val,
                RooAbsReal& _R2Val
		);

    RooSpinTwoXZsZs(const RooSpinTwoXZsZs& other, const char* name=0) ;
    virtual TObject* clone(const char* newname) const { return new RooSpinTwoXZsZs(*this,newname); }
    inline virtual ~RooSpinTwoXZsZs() { }
    
    Int_t getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* rangeName=0) const ;
    Double_t analyticalIntegral(Int_t code, const char* rangeName=0) const ;
    
protected:
    
    RooRealProxy mzz ;
    RooRealProxy m1 ;
    RooRealProxy m2 ;
    RooRealProxy hs ;
    RooRealProxy h1 ;
    RooRealProxy h2 ;
    RooRealProxy Phi ;
    RooRealProxy Phi1 ;
    RooRealProxy c1;
    RooRealProxy phi1;
    RooRealProxy c2;
    RooRealProxy phi2;
    RooRealProxy c3;
    RooRealProxy phi3;
    RooRealProxy c4;
    RooRealProxy phi4;
    RooRealProxy c5;
    RooRealProxy phi5;
    RooRealProxy c6;
    RooRealProxy phi6;
    RooRealProxy c7;
    RooRealProxy phi7;
    RooRealProxy fz1Val ;
    RooRealProxy fz2Val ;
    RooRealProxy R1Val ;
    RooRealProxy R2Val ;
    
    Double_t evaluate() const ;
    
private:
    
    ClassDef(RooSpinTwoXZsZs,1) // Your description goes here...
};

#endif
