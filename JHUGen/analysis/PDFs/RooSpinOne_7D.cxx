 /***************************************************************************** 
  * Project: RooFit                                                           * 
  *                                                                           * 
  * This code was autogenerated by RooClassFactory                            * 
  *****************************************************************************/ 

 // Your description goes here... 

#include "Riostream.h" 
#include "RooSpinOne_7D.h" 
#include "RooAbsReal.h" 
#include "RooAbsCategory.h" 
#include <math.h> 
#include "TMath.h" 

using namespace TMath;

ClassImp(RooSpinOne_7D) 
  
  RooSpinOne_7D::RooSpinOne_7D(const char *name, const char *title, 
			       RooAbsReal& _mzz,
			       RooAbsReal& _m1,
			       RooAbsReal& _m2,
			       RooAbsReal& _h1,
			       RooAbsReal& _h2,
			       RooAbsReal& _hs,
			       RooAbsReal& _Phi,
			       RooAbsReal& _Phi1,
			       RooAbsReal& _g1Val,
			       RooAbsReal& _g2Val,
			       RooAbsReal& _R1Val,
			       RooAbsReal& _R2Val,
			       RooAbsReal& _aParam,
			       RooAbsReal& _mZ,
			       RooAbsReal& _gamZ) :
    RooAbsPdf(name,title), 
    mzz("mzz","mzz",this,_mzz),
    m1("m1","m1",this,_m1),
    m2("m2","m2",this,_m2),
    h1("h1","h1",this,_h1),
    h2("h2","h2",this,_h2),
    hs("hs","hs",this,_hs),
    Phi("Phi","Phi",this,_Phi),
    Phi1("Phi1","Phi1",this,_Phi1),
    g1Val("g1Val","g1Val",this,_g1Val),
    g2Val("g2Val","g2Val",this,_g2Val),
    R1Val("R1Val","R1Val",this,_R1Val),
    R2Val("R2Val","R2Val",this,_R2Val),
    aParam("aParam","aParam",this,_aParam),
    mZ("mZ","mZ",this,_mZ),
    gamZ("gamZ","gamZ",this,_gamZ)
{ 
} 


RooSpinOne_7D::RooSpinOne_7D(const RooSpinOne_7D& other, const char* name) :  
  RooAbsPdf(other,name), 
  mzz("mzz",this,other.mzz),
  m1("m1",this,other.m1),
  m2("m2",this,other.m2),
  h1("h1",this,other.h1),
  h2("h2",this,other.h2),
  hs("hs",this,other.hs),
  Phi("Phi",this,other.Phi),
  Phi1("Phi1",this,other.Phi1),
  g1Val("g1Val",this,other.g1Val),
  g2Val("g2Val",this,other.g2Val),
  R1Val("R1Val",this,other.R1Val),
  R2Val("R2Val",this,other.R2Val),
  aParam("aParam",this,other.aParam),
  mZ("mZ",this,other.mZ),
  gamZ("gamZ",this,other.gamZ)
{ 
} 



Double_t RooSpinOne_7D::evaluate() const 
{ 
  
  
  bool isZZ = true;
  if ( mZ < 90.) isZZ = false;
  if ( isZZ ) {
    if( (m1+m2) > mzz || m2>m1 ) return 1e-9; 
  } else {
    if( (m1+m2) > mzz ) return 1e-9; 
  }
  double nanval = sqrt((1 - TMath::Power(m1 - m2,2)/TMath::Power(mzz,2))*(1 - TMath::Power(m1 + m2,2)/TMath::Power(mzz,2)));
  if (nanval != nanval) return 1e-9;
  
  //-----------------------------------------------------------------------
  // propagator
  //-----------------------------------------------------------------------
  
  Double_t betaValSquared = (1.-(pow(m1-m2,2)/pow(mzz,2)))*(1.-(pow(m1+m2,2)/pow(mzz,2)));
  Double_t betaVal = sqrt(betaValSquared);
  
  Double_t term1Coeff = (pow(m1,3))/( (pow(m1,2)-pow(mZ,2))*(pow(m1,2)-pow(mZ,2))+pow(mZ,2)*pow(gamZ,2) );
  Double_t term2Coeff = (pow(m2,3))/( (pow(m2,2)-pow(mZ,2))*(pow(m2,2)-pow(mZ,2))+pow(mZ,2)*pow(gamZ,2) );
  
  //-----------------------------------------------------------------------
  // Helicity Amplitudes
  //-----------------------------------------------------------------------
  
  // calculating the angular parameters from the coupling constants 
  // See http://www.pha.jhu.edu/~gritsan/FORM/result_spin1.txt
  Double_t x = (mzz*mzz-m1*m1-m2*m2)/(2.0*m1*m2);

  Double_t fp0Real =  m1*g1Val * ( sqrt(x*x-1) ); 
  Double_t fp0Imag =  Power(mzz,-2.)*Power(m2,3)*g2Val * (  - 1./2. )
    + Power(mzz,-2.)*m1*m1*m2*g2Val * ( 1 + 2*(x*x-1) )
    + Power(mzz,-2.)*Power(m1,4)*Power(m2,-1)*g2Val * (  - 1./2. )
    + m2*g2Val * (  - 1./2. )
    + m1*m1*Power(m2,-1)*g2Val * ( 1./2. );
  
  Double_t f0pReal = m2*g1Val * (  - sqrt(x*x-1) );
  Double_t f0pImag = Power(mzz,-2.)*Power(m1,-1)*Power(m2,4)*g2Val * ( 1./2. )
    + Power(mzz,-2.)*m1*Power(m2,2)*g2Val * (  - 1 - 2*(x*x-1) )
    + Power(mzz,-2.)*Power(m1,3)*g2Val * ( 1./2. )
    + Power(m1,-1)*Power(m2,2)*g2Val * (  - 1./2. )
    + m1*g2Val * ( 1./2. );

  
  Double_t f0mReal =  m2*g1Val * (  - sqrt(x*x-1) );
  Double_t f0mImag =  Power(mzz,-2.)*Power(m1,-1)*Power(m2,4)*g2Val * (  - 1./2. )
    + Power(mzz,-2.)*m1*Power(m2,2)*g2Val * ( 1 + 2*(x*x-1) )
    + Power(mzz,-2.)*Power(m1,3)*g2Val * (  - 1./2. )
    + Power(m1,-1)*Power(m2,2)*g2Val * ( 1./2. )
    + m1*g2Val * (  - 1./2. );
  
  Double_t fm0Real =  m1*g1Val * ( sqrt(x*x-1) ); 
  Double_t fm0Imag = Power(mzz,-2.)*Power(m2,3)*g2Val * ( 1./2. )
    + Power(mzz,-2.)*m1*m1*m2*g2Val * (  - 1 - 2*(x*x-1) )
    + Power(mzz,-2.)*Power(m1,4)*Power(m2,-1)*g2Val * ( 1./2. )
    + m2*g2Val * ( 1./2. )
    + m1*m1*Power(m2,-1)*g2Val * (  - 1./2. );
  
  Double_t fp0 = fp0Imag*fp0Imag + fp0Real*fp0Real;
  Double_t f0p = f0pImag*f0pImag + f0pReal*f0pReal;
  Double_t fm0 = fm0Imag*fm0Imag + fm0Real*fm0Real;
  Double_t f0m = f0mImag*f0mImag + f0mReal*f0mReal;
  
  Double_t phip0=atan2(fp0Imag,fp0Real);
  Double_t phi0p=atan2(f0pImag,f0pReal);
  Double_t phim0=atan2(fm0Imag,fm0Real);
  Double_t phi0m=atan2(f0mImag,f0mReal);

  Double_t norm = fp0 + f0p + fm0 + f0m;


  // term 1-10
  Double_t value=0;
  value +=  (fp0*(-1 + 2.*R1Val*h1 - Power(h1,2))*(-1 + Power(h2,2))*(1 + Power(hs,2)))/32.; // terms[1]
  value += -(f0m*(-1 + Power(h1,2))*(1 + 2.*R2Val*h2 + Power(h2,2))*(1 + Power(hs,2)))/32.; // terms[2]
  value += (f0p*(-1 + Power(h1,2))*(-1 + 2.*R2Val*h2 - Power(h2,2))*(1 + Power(hs,2)))/32.; // terms[3]
  value += -(fm0*(1 + 2.*R1Val*h1 + Power(h1,2))*(-1 + Power(h2,2))*(1 + Power(hs,2)))/32.; // terms[4]
  value += (Sqrt(f0m)*Sqrt(fp0)*(R1Val - h1)*Sqrt(1 - Power(h1,2))*(R2Val + h2)*Sqrt(1 - Power(h2,2))*(1 + Power(hs,2))*Cos(Phi - phi0m + phip0))/16.; // terms[5]
  value += -(Sqrt(f0p)*Sqrt(fp0)*(-R1Val + h1)*Sqrt(1 - Power(h1,2))*(-R2Val + h2)*Sqrt(1 - Power(h2,2))*(-1 + Power(hs,2))*Cos(Phi + phi0p - phip0 + 2.*Phi1))/16.; // terms[6]
  value += -(Sqrt(fm0)*Sqrt(fp0)*(-1 + Power(h1,2))*(-1 + Power(h2,2))*(-1 + Power(hs,2))*Cos(phim0 - phip0 + 2.*Phi))/16.; // terms[7]
  value += -(Sqrt(f0m)*Sqrt(f0p)*(-1 + Power(h1,2))*(-1 + Power(h2,2))*(-1 + Power(hs,2))* Cos(2.*Phi - phi0m + phi0p + 2.*Phi1))/16.; // terms[8]
  value += -(Sqrt(f0m)*Sqrt(fm0)*(R1Val + h1)*Sqrt(1 - Power(h1,2))*(R2Val + h2)*Sqrt(1 - Power(h2,2))*(-1 + Power(hs,2))* Cos(Phi - phi0m + phim0 + 2.*Phi1))/16.; // terms[9]
  value += (Sqrt(f0p)*Sqrt(fm0)*(R1Val + h1)*Sqrt(1 - Power(h1,2))*(R2Val - h2)* Sqrt(1 - Power(h2,2))*(1 + Power(hs,2))*Cos(Phi + phi0p - phim0))/16.; // terms[10]
  return value*term1Coeff*term2Coeff*betaVal;
  
} 

Int_t RooSpinOne_7D::getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* /*rangeName*/) const
{
  if (matchArgs(allVars,analVars,RooArgSet(*hs.absArg(),*h1.absArg(),*h2.absArg(),*Phi.absArg(),*Phi1.absArg()))) return 6 ;
  if (matchArgs(allVars,analVars,hs,h1,h2,Phi)) return 5 ;
  if (matchArgs(allVars,analVars,hs,h1,h2,Phi1)) return 4 ;
  if (matchArgs(allVars,analVars,hs,h1,Phi,Phi1)) return 3 ;
  if (matchArgs(allVars,analVars,hs,h2,Phi,Phi1)) return 2 ;
  if (matchArgs(allVars,analVars,h1,h2,Phi,Phi1)) return 1 ;
  return 0 ;
}

Double_t RooSpinOne_7D::analyticalIntegral(Int_t code, const char* rangeName) const
{
  
  bool isZZ = true;
  if ( mZ < 90.) isZZ = false;
  if ( isZZ ) {
    if( (m1+m2) > mzz || m2>m1 ) return 1e-9; 
  } else {
    if( (m1+m2) > mzz ) return 1e-9; 
  }
  double nanval = sqrt((1 - TMath::Power(m1 - m2,2)/TMath::Power(mzz,2))*(1 - TMath::Power(m1 + m2,2)/TMath::Power(mzz,2)));
  if (nanval != nanval) return 1e-9;
  
  //-----------------------------------------------------------------------
  // propagator
  //-----------------------------------------------------------------------
  
  Double_t betaValSquared = (1.-(pow(m1-m2,2)/pow(mzz,2)))*(1.-(pow(m1+m2,2)/pow(mzz,2)));
  Double_t betaVal = sqrt(betaValSquared);
  
  Double_t term1Coeff = (pow(m1,3))/( (pow(m1,2)-pow(mZ,2))*(pow(m1,2)-pow(mZ,2))+pow(mZ,2)*pow(gamZ,2) );
  Double_t term2Coeff = (pow(m2,3))/( (pow(m2,2)-pow(mZ,2))*(pow(m2,2)-pow(mZ,2))+pow(mZ,2)*pow(gamZ,2) );
  
  //-----------------------------------------------------------------------
  // Helicity Amplitudes
  //-----------------------------------------------------------------------
  // calculating the angular parameters from the coupling constants 
  // See http://www.pha.jhu.edu/~gritsan/FORM/result_spin1.txt
  
  Double_t x = (mzz*mzz-m1*m1-m2*m2)/(2.0*m1*m2);

  Double_t fp0Real =  m1*g1Val * ( sqrt(x*x-1) ); 
  Double_t fp0Imag =  Power(mzz,-2.)*Power(m2,3)*g2Val * (  - 1./2. )
    + Power(mzz,-2.)*m1*m1*m2*g2Val * ( 1 + 2*(x*x-1) )
    + Power(mzz,-2.)*Power(m1,4)*Power(m2,-1)*g2Val * (  - 1./2. )
    + m2*g2Val * (  - 1./2. )
    + m1*m1*Power(m2,-1)*g2Val * ( 1./2. );
  
  Double_t f0pReal = m2*g1Val * (  - sqrt(x*x-1) );
  Double_t f0pImag = Power(mzz,-2.)*Power(m1,-1)*Power(m2,4)*g2Val * ( 1./2. )
    + Power(mzz,-2.)*m1*Power(m2,2)*g2Val * (  - 1 - 2*(x*x-1) )
    + Power(mzz,-2.)*Power(m1,3)*g2Val * ( 1./2. )
    + Power(m1,-1)*Power(m2,2)*g2Val * (  - 1./2. )
    + m1*g2Val * ( 1./2. );

  
  Double_t f0mReal =  m2*g1Val * (  - sqrt(x*x-1) );
  Double_t f0mImag =  Power(mzz,-2.)*Power(m1,-1)*Power(m2,4)*g2Val * (  - 1./2. )
    + Power(mzz,-2.)*m1*Power(m2,2)*g2Val * ( 1 + 2*(x*x-1) )
    + Power(mzz,-2.)*Power(m1,3)*g2Val * (  - 1./2. )
    + Power(m1,-1)*Power(m2,2)*g2Val * ( 1./2. )
    + m1*g2Val * (  - 1./2. );
  
  Double_t fm0Real =  m1*g1Val * ( sqrt(x*x-1) ); 
  Double_t fm0Imag = Power(mzz,-2.)*Power(m2,3)*g2Val * ( 1./2. )
    + Power(mzz,-2.)*m1*m1*m2*g2Val * (  - 1 - 2*(x*x-1) )
    + Power(mzz,-2.)*Power(m1,4)*Power(m2,-1)*g2Val * ( 1./2. )
    + m2*g2Val * ( 1./2. )
    + m1*m1*Power(m2,-1)*g2Val * (  - 1./2. );

  Double_t fp0 = fp0Imag*fp0Imag + fp0Real*fp0Real;
  Double_t f0p = f0pImag*f0pImag + f0pReal*f0pReal;
  Double_t fm0 = fm0Imag*fm0Imag + fm0Real*fm0Real;
  Double_t f0m = f0mImag*f0mImag + f0mReal*f0mReal;
  
  Double_t phip0=atan2(fp0Imag,fp0Real);
  Double_t phi0p=atan2(f0pImag,f0pReal);
  Double_t phim0=atan2(fm0Imag,fm0Real);
  Double_t phi0m=atan2(f0mImag,f0mReal);

  Double_t integral=0;

  switch(code)
    {
    case 6:
      {
	integral = 0.;
	integral+= 
	  (32.*fp0*Power(Pi(),2))/27.;
	integral+= 
	  (32.*f0m*Power(Pi(),2))/27.;
	integral+= 
	  (32.*f0p*Power(Pi(),2))/27.;
	integral+= 
	  (32.*fm0*Power(Pi(),2))/27.;
	return term1Coeff*term2Coeff*betaVal*integral;

      }
      
      // projections onto Phi1, integrate all other angles
    case 5:
      {
	integral = 0.;
	integral += 
	  (16*fp0*Pi())/27.; 
	integral += 
	  (16*f0m*Pi())/27.;
	integral += 
	  (16*f0p*Pi())/27.;
	integral += 
	  (16*fm0*Pi())/27.;
	integral += 
	  (8*Sqrt(fm0)*Sqrt(fp0)*Pi()*Cos(2.*Phi1 + phim0 - phip0))/27.;
	return term1Coeff*term2Coeff*betaVal*integral;

      }
     // projection to Phi, integrate all other angles
    case 4:
      {
	integral = 0.;
	integral += 
	  (16*fp0*Pi())/27.;
	integral += 
	  (16*f0m*Pi())/27.;
	integral += 
	  (16*f0p*Pi())/27.;
	integral += 
	  (16*fm0*Pi())/27.;
	integral += 
	  (Sqrt(f0m)*Sqrt(fp0)*Power(Pi(),3)*R1Val*R2Val*
	   Cos(Phi - phi0m + phip0))/12.;
	integral +=
	  (Sqrt(f0p)*Sqrt(fm0)*Power(Pi(),3)*R1Val*R2Val*
		Cos(Phi + phi0p - phim0))/12.;
	return term1Coeff*term2Coeff*betaVal*integral;
      }
      
      // projections to h2, integrate over all others
    case 3:
      {
     integral = 0.;
     integral += 
       (-8*fp0*Power(Pi(),2)*(-1 + Power(h2,2)))/9.;
     integral += 
       (4*f0m*Power(Pi(),2)*(1 + 2.*R2Val*h2 + Power(h2,2)))/9.;
     integral += 
       (4*f0p*Power(Pi(),2)*(1 - 2.*R2Val*h2 + Power(h2,2)))/9.;
     integral += 
       (-8*fm0*Power(Pi(),2)*(-1 + Power(h2,2)))/9.;
     return term1Coeff*term2Coeff*betaVal*integral;
   }
      // projections to h1, integrate all others
    case 2:
      {
	integral=0.;
	integral += 
	  (4*fp0*Power(Pi(),2)*(1 - 2.*R1Val*h1 + Power(h1,2)))/9.;
	integral += 
	  (-8*f0m*Power(Pi(),2)*(-1 + Power(h1,2)))/9.;
	integral += 
	  (-8*f0p*Power(Pi(),2)*(-1 + Power(h1,2)))/9.;
	integral += 
	  (4*fm0*Power(Pi(),2)*(1 + 2.*R1Val*h1 + Power(h1,2)))/9.;
	
	return term1Coeff*term2Coeff*betaVal*integral;	
      }

      // projections to hs, integrate all others
    case 1:
      {
	integral = 0.;
	integral += 
	  (4*fp0*Power(Pi(),2)*(1 + Power(hs,2)))/9.;
	integral += 
	  (4*f0m*Power(Pi(),2)*(1 + Power(hs,2)))/9.;
	integral += 
	  (4*f0p*Power(Pi(),2)*(1 + Power(hs,2)))/9.;
	integral += 
	  (4*fm0*Power(Pi(),2)*(1 + Power(hs,2)))/9.;
	return term1Coeff*term2Coeff*betaVal*integral;	

      }
    }
  assert(0) ;
  return 0 ;
}
