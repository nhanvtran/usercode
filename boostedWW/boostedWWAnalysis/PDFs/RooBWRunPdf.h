/*****************************************************************************
 * Project: RooFit                                                           *
 *                                                                           *
  * This code was autogenerated by RooClassFactory                            * 
 *****************************************************************************/

#ifndef ROOBWRUNPDF
#define ROOBWRUNPDF

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooCategoryProxy.h"
#include "RooAbsReal.h"
#include "RooAbsCategory.h"
 
class RooBWRunPdf : public RooAbsPdf {
public:
  RooBWRunPdf() {} ; 
  RooBWRunPdf(const char *name, const char *title,
	      RooAbsReal& _x,
	      RooAbsReal& _mean,
	      RooAbsReal& _width);
  RooBWRunPdf(const RooBWRunPdf& other, const char* name=0) ;
  virtual TObject* clone(const char* newname) const { return new RooBWRunPdf(*this,newname); }
  inline virtual ~RooBWRunPdf() { }

protected:

  RooRealProxy x ;
  RooRealProxy mean ;
  RooRealProxy width ;
  
  Double_t evaluate() const ;

private:

  ClassDef(RooBWRunPdf,1) // Your description goes here...
};
 
#endif
