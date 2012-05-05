    //  Adapted From:
    //----------------
    // Original Author:  Fedor Ratnikov Nov 9, 2007
    // $Id: EffTableReader.h,v 1.1 2012/03/13 04:11:47 ntran Exp $
    //-----------------------------------------------------------------------


#ifndef PUReweighter_h
#define PUReweighter_h

#include <string>
#include <vector>
#include <iostream>

#include "LumiReweightingStandAlone.h"

using namespace std;

class PUReweighter {
public:
    
    PUReweighter () {}
    PUReweighter ( std::string fFileMC, std::string fFileDat);
    
        /// total # of bands
    void Get(double minus1, double intime, double plus1) ;
    
private:
    
    std::string _fileMC;
    std::string _fileData;
};

PUReweighter::PUReweighter(std::string fFileMC, std::string fFileDat){
    
    LumiReWeighting LumiWeights_ = LumiReWeighting(fFileMC, fFileDat, "pileup", "pileup");
    LumiWeights_.weight3D_init( 1.08 );
    
    LumiReWeighting up_LumiWeights_ = LumiReWeighting(fFileMC, fFileDat, "pileup", "pileup");
    up_LumiWeights_.weight3D_init( 1.16 );
    
    LumiReWeighting dn_LumiWeights_ = LumiReWeighting(fFileMC, fFileDat, "pileup", "pileup");
    dn_LumiWeights_.weight3D_init( 1.00 );

}

void PUReweighter::Get(double minus1, double intime, double plus1){
    
    std::cout << "hi" << std::endl;
    
}

#endif
