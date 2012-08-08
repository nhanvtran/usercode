// 
// Do not change the order of the enums, always append
// 
enum TestType{
  zeroplusVSzerominus = 0, 
  zeroplusVStwoplus   = 1,
  zeroplusVSzerohplus   = 2,
  zeroplusVSoneplus   = 3,
  zeroplusVSoneminus   = 4,
  zeroplusVStwohplus  = 5,
  zeroplusVStwohminus  = 6,
};

enum VarType{
  DPHI = 0,
  MLL = 1,
  DPHIMT = 2,
  MLLMT = 3,
};

enum spinType{
  zeroplus = 0 ,
  zerominus = 1,
  zerohplus = 2,
  oneplus = 3,
  oneminus = 4,
  twoplus = 5,
  twohplus = 6,
  twohminus = 7,
  ww = 8,
};


enum ToyType {
  embed = 0,
  pure = 1,
};

enum Site {
   UCSD=0,
   FNAL=1,
};

TString getTestName( int test )
{
  switch (test ) {
  
  case zeroplusVSzerominus:
    return "0plusVS0minus";
    break;
  
  case zeroplusVStwoplus:
    return "0plusVS2plus";
    break;
  
  case zeroplusVSzerohplus:
    return "0plusVS0hplus";
    break;
    
  case zeroplusVSoneminus:
    return "0plusVS1minus";
    break;

  case zeroplusVSoneplus:
    return "0plusVS1plus";
    break;

  case zeroplusVStwohplus:
    return "0plusVS2hplus";
    break;

  case zeroplusVStwohminus:
    return "0plusVS2hminus";
    break;
    
  default: 
    return "unKnown";
    break;
  }
}

TString getSecondHypInputName (int test, float higgsMass )
{
  switch ( test )    { 
  
  case zeroplusVSzerominus:
    return Form("PSHiggsWW_%.0f_JHU.root", higgsMass) ;
    break;
    
  case zeroplusVSzerohplus:
    return Form("SMHiggsWW_0hplus_%.0f_JHU.root", higgsMass) ;
    break;

  case zeroplusVSoneminus:
    return Form("VWW_%.0f_JHU.root", higgsMass) ;
    return;

  case zeroplusVSoneplus:
    return Form("AVWW_%.0f_JHU.root", higgsMass) ;
    return;

  case zeroplusVStwoplus:
    return Form("TWW_2mplus_%.0f_JHU.root", higgsMass) ;
    break;

  case zeroplusVStwohplus:
    return Form("TWW_2hplus_%.0f_JHU.root", higgsMass) ;
    break;

  case zeroplusVStwohminus:
    return Form("TWW_2hminus_%.0f_JHU.root", higgsMass) ;
    break;

  default:
    return "unKnown";
    break;
  }
}



TString getVarName( int var) {
  if ( var == DPHIMT ) 
    return "2ddphimt";
  if ( var == MLLMT ) 
    return "2dmllmt";
  if ( var  == DPHI ) 
    return "1ddphi";
  if ( var  == MLL ) 
    return "1dmll";
  return "unKnown";
}


TString getToyName( int toy) {
  if ( toy == embed )
    return "embed";
  if ( toy == pure ) 
    return "pure";
  return "unKnown";
}

TString getInputName(int spin) {
  if ( spin == zeroplus )
    return "SMHiggsWW";
  if ( spin == zerominus )
    return "PSHiggsWW";
  if ( spin == zerohplus )
    return "SMHiggsWW_0hplus";
  if ( spin == oneminus )
    return "VWW";
  if ( spin == oneplus )
    return "AVWW";
  if ( spin == twoplus ) 
    return "TWW_2mplus";
  if ( spin == twohplus )
    return "TWW_2hplus";
  if ( spin == twohminus )
    return "TWW_2hminus";
  if ( spin == ww )
    return "WW_madgraph_8TeV_0j";
  return "unKnown";
}

TString getSpinName(int spin) {
  if ( spin == zeroplus )
    return "0m+";
  if ( spin == zerominus )
    return "0-";
  if ( spin == zerohplus )
    return "0h+";
  if ( spin == oneplus )
    return "1+";
  if ( spin == oneminus )
    return "1-";
  if ( spin == twoplus ) 
    return "2m+";
  if ( spin == twohminus ) 
    return "2-";
  if ( spin == twohplus ) 
    return "2h+";
  return "unKnown";
}
