// 
// Do not change the order of the enums, always append
// 
enum TestType{
  zeroplusVSzerominus = 0, 
  zeroplusVStwoplus   = 1,
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
  twoplus = 2,
};


enum ToyType {
  embed = 0,
  pure = 1,
};

TString getTestName( int test )
{
  if ( test == zeroplusVSzerominus) 
    return "0plusVS0minus";
  if ( test == zeroplusVStwoplus) 
    return "0plusVS2plus";
  
  return "unKnown";
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
  if ( spin == twoplus ) 
    return "TWW";
  return "unKnown";
}

TString getSpinName(int spin) {
  if ( spin == zeroplus )
    return "0+";
  if ( spin == zerominus )
    return "0-";
  if ( spin == twoplus ) 
    return "2+";
  return "unKnown";
}
