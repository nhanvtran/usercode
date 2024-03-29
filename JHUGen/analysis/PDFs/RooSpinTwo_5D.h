/*****************************************************************************
 * Project: RooFit                                                           *
 *                                                                           *
 * This code was autogenerated by RooClassFactory                            * 
 *****************************************************************************/

#ifndef ROOSPINTWO_5D
#define ROOSPINTWO_5D

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooCategoryProxy.h"
#include "RooAbsReal.h"
#include "RooAbsCategory.h"

class RooSpinTwo_5D : public RooAbsPdf {
public:
	RooSpinTwo_5D() {} ; 
	RooSpinTwo_5D(const char *name, const char *title,
				  RooAbsReal& _h1,
				  RooAbsReal& _h2,
				  RooAbsReal& _hs,
				  RooAbsReal& _Phi,
				  RooAbsReal& _Phi1,
				  RooAbsReal& _fppVal,
				  RooAbsReal& _fmmVal,
				  RooAbsReal& _fpmVal,
				  RooAbsReal& _fp0Val,
				  RooAbsReal& _f0mVal,
				  RooAbsReal& _phippVal,
				  RooAbsReal& _phimmVal,
				  RooAbsReal& _phipmVal,
				  RooAbsReal& _phip0Val,
				  RooAbsReal& _phi0mVal,
				  RooAbsReal& _fz1Val,
				  RooAbsReal& _fz2Val,
				  RooAbsReal& _R1Val,
				  RooAbsReal& _R2Val,
				  RooAbsReal& _para2,
				  RooAbsReal& _para4,
				  RooAbsReal& _para6,
				  RooAbsReal& _para8,
				  RooAbsReal& _acca0,
				  RooAbsReal& _acca1,
				  RooAbsReal& _acca2,
				  RooAbsReal& _acca4);
	RooSpinTwo_5D(const RooSpinTwo_5D& other, const char* name=0) ;
	virtual TObject* clone(const char* newname) const { return new RooSpinTwo_5D(*this,newname); }
	inline virtual ~RooSpinTwo_5D() { }
	
	Int_t getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* rangeName=0) const ;
	Double_t analyticalIntegral(Int_t code, const char* rangeName=0) const ;
	
	
protected:
	
	RooRealProxy h1 ;
	RooRealProxy h2 ;
	RooRealProxy hs ;
	RooRealProxy Phi ;
	RooRealProxy Phi1 ;
	RooRealProxy fppVal ;
	RooRealProxy fmmVal ;
	RooRealProxy fpmVal ;
	RooRealProxy fp0Val ;
	RooRealProxy f0mVal ;
	RooRealProxy phippVal ;
	RooRealProxy phimmVal ;
	RooRealProxy phipmVal ;
	RooRealProxy phip0Val ;
	RooRealProxy phi0mVal ;
	RooRealProxy fz1Val ;
	RooRealProxy fz2Val ;
	RooRealProxy R1Val ;
	RooRealProxy R2Val ;
	RooRealProxy para2 ;
	RooRealProxy para4 ;
	RooRealProxy para6 ;
	RooRealProxy para8 ;
	RooRealProxy acca0 ;
	RooRealProxy acca1 ;
	RooRealProxy acca2 ;
	RooRealProxy acca4 ;
	
	Double_t evaluate() const ;
	
private:
	
	ClassDef(RooSpinTwo_5D,1) // Your description goes here...
};

#endif
