/*****************************************************************************
 * Project: RooFit                                                           *
 *                                                                           *
  * This code was autogenerated by RooClassFactory                            * 
 *****************************************************************************/

#ifndef ROOSPINONE_DECAY
#define ROOSPINONE_DECAY

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooCategoryProxy.h"
#include "RooAbsReal.h"
#include "RooAbsCategory.h"
 
using namespace TMath;

class RooSpinOne_Decay : public RooAbsPdf {
public:
  RooSpinOne_Decay() {} ; 
  RooSpinOne_Decay(const char *name, const char *title,
		RooAbsReal& _mzz,
		RooAbsReal& _m1,
		RooAbsReal& _m2,
		RooAbsReal& _h1,
		RooAbsReal& _h2,
		RooAbsReal& _Phi,
		RooAbsReal& _g1Val,
		RooAbsReal& _g2Val,
		RooAbsReal& _R1Val,
		RooAbsReal& _R2Val,
		RooAbsReal& _aParam,
                RooAbsReal& _mZ,
                RooAbsReal& _gamZ);
  RooSpinOne_Decay(const RooSpinOne_Decay& other, const char* name=0) ;
  virtual TObject* clone(const char* newname) const { return new RooSpinOne_Decay(*this,newname); }
  inline virtual ~RooSpinOne_Decay() { }
  Int_t getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* rangeName=0) const ;
  Double_t analyticalIntegral(Int_t code, const char* rangeName=0) const ;
  
 protected:

	RooRealProxy mzz ;
	RooRealProxy m1 ;
	RooRealProxy m2 ;
	RooRealProxy h1 ;
	RooRealProxy h2 ;
	RooRealProxy Phi ;
	RooRealProxy g1Val ;
	RooRealProxy g2Val ;
	RooRealProxy R1Val ;
	RooRealProxy R2Val ;
	RooRealProxy aParam ;
	RooRealProxy mZ ;
	RooRealProxy gamZ ;
	Double_t evaluate() const ;
	
 private:
	
	//	ClassDef(RooSpinOne_Decay,1) // Your description goes here...
};

#endif
