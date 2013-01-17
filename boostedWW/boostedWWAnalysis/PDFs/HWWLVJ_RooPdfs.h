/*****************************************************************************
 * Project: RooFit                                                           *
 *                                                                           *
  * This code was autogenerated by RooClassFactory                            * 
 *****************************************************************************/

#ifndef HWWLVJ_ROOPDF
#define HWWLVJ_ROOPDF

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooCategoryProxy.h"
#include "RooAbsReal.h"
#include "RooAbsCategory.h"


Double_t ErfExp(Double_t x, Double_t c, Double_t offset, Double_t width);
 
class RooErfExpPdf : public RooAbsPdf {
public:
  RooErfExpPdf() {} ; 
  RooErfExpPdf(const char *name, const char *title,
	      RooAbsReal& _x,
	      RooAbsReal& _c,
	      RooAbsReal& _offset,
	      RooAbsReal& _width);
  RooErfExpPdf(const RooErfExpPdf& other, const char* name=0) ;
  virtual TObject* clone(const char* newname) const { return new RooErfExpPdf(*this,newname); }
  inline virtual ~RooErfExpPdf() { }

  Int_t getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* rangeName=0) const ;
  Double_t analyticalIntegral(Int_t code, const char* rangeName=0) const ;

protected:

  RooRealProxy x ;
  RooRealProxy c ;
  RooRealProxy offset ;
  RooRealProxy width ;
  
  Double_t evaluate() const ;

private:

  ClassDef(RooErfExpPdf,1) // Your description goes here...
};


class RooAlpha : public RooAbsPdf {
	public:
		RooAlpha();
		RooAlpha(const char *name, const char *title,
					RooAbsReal& _x,
					RooAbsReal& _c,
					RooAbsReal& _offset,
					RooAbsReal& _width,
					RooAbsReal& _ca,
					RooAbsReal& _offseta,
					RooAbsReal& _widtha,
                    Double_t _xmin,
                    Double_t _xmax
				);
		RooAlpha(const RooAlpha& other, const char* name=0) ;
		virtual TObject* clone(const char* newname) const { return new RooAlpha(*this,newname); }
		inline virtual ~RooAlpha() { }
        Double_t xmin;
        Double_t xmax;

	protected:

		RooRealProxy x ;
		RooRealProxy c;
		RooRealProxy offset;
		RooRealProxy width;
		RooRealProxy ca;
		RooRealProxy offseta;
		RooRealProxy widtha;

		Double_t evaluate() const ;

	private:

		ClassDef(RooAlpha,1)
};


class RooAlphaExp : public RooAbsPdf {
	public:
		RooAlphaExp();
		RooAlphaExp(const char *name, const char *title,
					RooAbsReal& _x,
					RooAbsReal& _c,
					RooAbsReal& _ca,
                    Double_t _xmin,
                    Double_t _xmax
				);
		RooAlphaExp(const RooAlphaExp& other, const char* name=0) ;
		virtual TObject* clone(const char* newname) const { return new RooAlphaExp(*this,newname); }
		inline virtual ~RooAlphaExp() { }
        Double_t xmin;
        Double_t xmax;

	protected:

		RooRealProxy x ;
		RooRealProxy c;
		RooRealProxy ca;
		Double_t evaluate() const ;

	private:

		ClassDef(RooAlphaExp,1)
};


#endif