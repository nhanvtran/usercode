enum TestType{
  zeroplusVSzerominus = 1UL<<0,
  zeroplusVStwoplus   = 1UL<<1,
};

enum VarType{
  DPHI,
  MLL,
  DPHIMT,
};

enum ToyType {
  embed,
  pure,
};

TString getTestName( int test )
{
  if ( test & zeroplusVSzerominus) 
    return "0plusVS0minus";
  if ( test & zeroplusVStwoplus) 
    return "0plusVS2plus";
  
  return "unKnown";
}


TString getVarName( int var) {
  if ( var == DPHIMT ) 
    return "2ddphimt";
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
