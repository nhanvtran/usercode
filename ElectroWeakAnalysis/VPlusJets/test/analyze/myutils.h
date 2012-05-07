#ifndef myutils_h
#define myutils_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <iostream>
#include "TH1F.h"
#include "TH2F.h"

class myutils {
    public :
    
    myutils();
    ~myutils();
    TH1F* GetFitSlicesY(TH2F* h2d, int param);


};

#endif

#ifdef myutils_cxx
myutils::myutils()
{
    std::cout << "building utilities" << std::endl;
}

myutils::~myutils()
{
    
}


#endif // #ifdef vJetSubstructureAnalysis_cxx
