#ifndef JETSUBSTRUCTURETOOLS_H
#define JETSUBSTRUCTURETOOLS_H


#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h" 

#include "VHbbAnalysis/VHbbDataFormats/interface/VHbbEventAuxInfo.h"
#include "VHbbAnalysis/VHbbDataFormats/interface/VHbbEvent.h"

#include <fastjet/ClusterSequence.hh>
#include <fastjet/GhostedAreaSpec.hh>
#include <fastjet/ClusterSequenceArea.hh>
#include "fastjet/tools/Filter.hh"
#include "fastjet/tools/Pruner.hh"
#include "fastjet/tools/MassDropTagger.hh"
#include "fastjet/GhostedAreaSpec.hh"

//#include "VHbbAnalysis/VHbbDataFormats/interface/Nsubjettiness.h"
#include "JetSubstructure/SubstructureTools/interface/NjettinessPlugin.hh"
#include "JetSubstructure/SubstructureTools/interface/Nsubjettiness.hh"
#include "JetSubstructure/SubstructureTools/src/QjetsPlugin.h"

#include <iostream>

class JetSubstructureTools {
    
    // member functions
 public:
    
    // constructor
    JetSubstructureTools( double radii, std::vector<float> c_px, std::vector<float> c_py, std::vector<float> c_pz, std::vector<float> c_e, std::vector<float> c_pdgId );    
    ~JetSubstructureTools(){}
    
    fastjet::PseudoJet getPrunedJet(){ return prunedJet_; }
    fastjet::PseudoJet getTrimmedJet(){ return trimmedJet_; }
    fastjet::PseudoJet getFilteredJet(){ return filteredJet_; }    
    float getPrunedJetArea(){ return prunedJetArea_; }
    float getTrimmedJetArea(){ return trimmedJetArea_; }
    float getFilteredJetArea(){ return filteredJetArea_; }
    
    float getTau1(){ return tau1_; }
    float getTau2(){ return tau2_; }
    float getTau3(){ return tau3_; }
    float getTau4(){ return tau4_; }    
    
    fastjet::PseudoJet getPrunedSubJet(int i){ 
        if (i == 0) return prunedSubJet1_;
        else if (i == 1) return prunedSubJet2_;
        else throw cms::Exception("JetSubstructureTools") << "Too many subjets..." << std::endl;
    }
    double getQjetVolatility(int seed);
    // data members
    
  private: 
    float FindRMS( std::vector< float > qjetmasses ){
        
        float total = 0.;
        float ctr = 0.;
        for (unsigned int i = 0; i < qjetmasses.size(); i++){
            total = total + qjetmasses[i];
            ctr++;
        }
        float mean =  total/ctr;
        
        float totalsquared = 0.;
        for (unsigned int i = 0; i < qjetmasses.size(); i++){
            totalsquared += (qjetmasses[i] - mean)*(qjetmasses[i] - mean) ;
        }
        float RMS = sqrt( totalsquared/ctr );
        return RMS;
    }
    
    float FindMean( std::vector< float > qjetmasses ){
        float total = 0.;
        float ctr = 0.;
        for (unsigned int i = 0; i < qjetmasses.size(); i++){
            total = total + qjetmasses[i];
            ctr++;
        }
        return total/ctr;
    }
 
  public:
    
    std::vector<fastjet::PseudoJet> FJconstituents_;
    std::vector<float> c_pdgIds_; 
    
    fastjet::PseudoJet prunedJet_;
    fastjet::PseudoJet trimmedJet_;
    fastjet::PseudoJet filteredJet_;
    
    float prunedJetMass_;
    float trimmedJetMass_;
    float filteredJetMass_;
    float ungroomedJetMass_;
    
    float prunedJetArea_;
    float trimmedJetArea_;
    float filteredJetArea_;
    
    float tau1_;
    float tau2_;
    float tau3_;
    float tau4_;
    
    float rcore01_;
    float rcore02_;
    float rcore03_;
    float rcore04_;
    float rcore05_;
    float rcore06_;
    float rcore07_;
    float rcore08_;
    float rcore09_;
    float rcore10_;
    float rcore11_;
    float rcore12_;

    fastjet::PseudoJet prunedSubJet1_;
    fastjet::PseudoJet prunedSubJet2_;    
    
    float QJetVolatility_;
    
    double mJetRadius;
};

    // -------------------------------------------
    // -------------------------------------------
    // -------------------------------------------
    // -------------------------------------------

    // constructor
JetSubstructureTools::JetSubstructureTools( double radii, std::vector<float> c_px, std::vector<float> c_py, std::vector<float> c_pz, std::vector<float> c_e, std::vector<float> c_pdgId )   
{

    
    mJetRadius = radii;
        // check that they are all the same size
    if ((c_px.size() == c_py.size())&&(c_py.size() == c_pz.size())&&(c_pz.size() == c_e.size())&&(c_e.size() == c_pdgId.size())){
        for (unsigned int i = 0; i < c_px.size(); i++){
            
            FJconstituents_.push_back( fastjet::PseudoJet( c_px[i], c_py[i], c_pz[i], c_e[i] ) );
            c_pdgIds_.push_back( c_pdgId[i] );
            
        }
    }
    else throw cms::Exception("JetSubstructureTools") << "Constituent size mismatch..." << std::endl;
    
        // -------------------------------------------
        // recluster on the fly....

    fastjet::JetDefinition jetDef(fastjet::cambridge_algorithm, mJetRadius);
    
    int activeAreaRepeats = 1;
    double ghostArea = 0.01;
    double ghostEtaMax = 5.0;

    fastjet::GhostedAreaSpec fjActiveArea(ghostEtaMax,activeAreaRepeats,ghostArea);
    fjActiveArea.set_fj2_placement(true);
    fastjet::AreaDefinition fjAreaDefinition( fastjet::active_area_explicit_ghosts, fjActiveArea );

    fastjet::ClusterSequenceArea thisClustering(FJconstituents_, jetDef, fjAreaDefinition);
    std::vector<fastjet::PseudoJet> out_jets = sorted_by_pt(thisClustering.inclusive_jets(50.0));

    fastjet::ClusterSequence thisClustering_basic(FJconstituents_, jetDef);
    std::vector<fastjet::PseudoJet> out_jets_basic = sorted_by_pt(thisClustering_basic.inclusive_jets(50.0));

        // -------------------------------------------
        // define groomers
    fastjet::Filter trimmer( fastjet::Filter(fastjet::JetDefinition(fastjet::kt_algorithm, 0.2), fastjet::SelectorPtFractionMin(0.03)));
    fastjet::Filter filter( fastjet::Filter(fastjet::JetDefinition(fastjet::cambridge_algorithm, 0.3), fastjet::SelectorNHardest(3)));
    fastjet::Pruner pruner(fastjet::cambridge_algorithm, 0.1, 0.5);
    
    std::vector<fastjet::Transformer const *> transformers;
    transformers.push_back(&trimmer);
    transformers.push_back(&filter);
    transformers.push_back(&pruner);

//        // define n-subjettiness
//    float mNsubjettinessKappa = 1.;
//    NsubParameters paraNsub = NsubParameters(mNsubjettinessKappa, mJetRadius);   
//    Nsubjettiness routine(nsub_kt_axes, paraNsub);
    
        // define n-subjettiness
    float mNsubjettinessKappa = 1.;
    double beta = mNsubjettinessKappa; // power for angular dependence, e.g. beta = 1 --> linear k-means, beta = 2 --> quadratic/classic k-means
    double R0 = mJetRadius; // Characteristic jet radius for normalization            
    double Rcut = mJetRadius; // maximum R particles can be from axis to be included in jet           

    
    ungroomedJetMass_ = out_jets.at(0).m();
        // -------------------------------------------    
        // compute pruning, trimming, filtering  -------------    
    int transctr = 0;
    for ( std::vector<fastjet::Transformer const *>::const_iterator 
         itransf = transformers.begin(), itransfEnd = transformers.end(); 
         itransf != itransfEnd; ++itransf ) {  
        
        fastjet::PseudoJet transformedJet = out_jets.at(0);
        transformedJet = (**itransf)(transformedJet);
        
        if (transctr == 0){ // trimmed
            trimmedJet_ = transformedJet;
            trimmedJetMass_ = transformedJet.m();            
            trimmedJetArea_ = transformedJet.area();
        }
        else if (transctr == 1){ // filtered
            filteredJet_ = transformedJet;
            filteredJetMass_ = transformedJet.m();            
            filteredJetArea_ = transformedJet.area();
        }
        else if (transctr == 2){ // pruned
            prunedJet_ = transformedJet;
            prunedJetMass_ = transformedJet.m();            
            prunedJetArea_ = transformedJet.area();
            
                //decompose into requested number of subjets:
            if (transformedJet.constituents().size() > 1){
                
                int nsubjetstokeep = 2;
                std::vector<fastjet::PseudoJet> prunedSubjets = transformedJet.associated_cluster_sequence()->exclusive_subjets(transformedJet,nsubjetstokeep);    
                
                prunedSubJet1_ = prunedSubjets.at(0);
                prunedSubJet2_ = prunedSubjets.at(1);
                
            }
        }
        else{ std::cout << "error in number of transformers" << std::endl;}                    
        transctr++;
    }        
    
        // -------------------------------------------    
        // compute n-subjettiness  -------------
    fastjet::Nsubjettiness nSub1KT(1, Njettiness::onepass_kt_axes, beta, R0, Rcut);
    tau1_ = nSub1KT(out_jets.at(0));
    fastjet::Nsubjettiness nSub2KT(2, Njettiness::onepass_kt_axes, beta, R0, Rcut);
    tau2_ = nSub2KT(out_jets.at(0));
    fastjet::Nsubjettiness nSub3KT(3, Njettiness::onepass_kt_axes, beta, R0, Rcut);
    tau3_ = nSub3KT(out_jets.at(0));
    fastjet::Nsubjettiness nSub4KT(4, Njettiness::onepass_kt_axes, beta, R0, Rcut);
    tau4_ = nSub4KT(out_jets.at(0));  
    
}
    // -------------------------------------------
    // -------------------------------------------
double JetSubstructureTools::getQjetVolatility(int seed){
    
    fastjet::JetDefinition jetDef(fastjet::cambridge_algorithm, mJetRadius);    
    int mQJetsN = 50;
    int mQJetsPreclustering = 30;
    
    std::vector< float > qjetmasses;
    
    fastjet::ClusterSequence thisClustering_basic(FJconstituents_, jetDef);
    std::vector<fastjet::PseudoJet> out_jets_basic = sorted_by_pt(thisClustering_basic.inclusive_jets(50.0));
    
    int j = 0; // the hardest jet
    
    double zcut(0.1), dcut_fctr(0.5), exp_min(0.), exp_max(0.), rigidity(0.1);          
    
    vector<fastjet::PseudoJet> constits;
    unsigned int nqjetconstits = out_jets_basic.at(j).constituents().size();
    if (nqjetconstits < (unsigned int) mQJetsPreclustering) constits = out_jets_basic.at(j).constituents();
    else constits = out_jets_basic.at(j).associated_cluster_sequence()->exclusive_subjets_up_to(out_jets_basic.at(j),mQJetsPreclustering);
    for(unsigned int ii = 0 ; ii < (unsigned int) mQJetsN ; ii++){
        QjetsPlugin qjet_plugin(zcut, dcut_fctr, exp_min, exp_max, rigidity);
				qjet_plugin.SetRandSeed(seed+ii); // new feature in Qjets to set the random seed
        fastjet::JetDefinition qjet_def(&qjet_plugin);
        fastjet::ClusterSequence qjet_seq(constits, qjet_def);
        vector<fastjet::PseudoJet> inclusive_jets2 = sorted_by_pt(qjet_seq.inclusive_jets(50.0));
        
        if (inclusive_jets2.size()>0) { qjetmasses.push_back( inclusive_jets2[0].m() ); }
        
    }
    
        // find RMS of a vector
    float qjetsRMS = FindRMS( qjetmasses );
        // find mean of a vector
    float qjetsMean = FindMean( qjetmasses );
//    std::cout << "qjetmasses size: " << qjetmasses.size() << std::endl;    
//    std::cout << "qjetsRMS: " << qjetsRMS << ", qjetsMean: " << qjetsMean << std::endl;    
        // compute QJets volatility
    float qjetsVolatility = qjetsRMS/qjetsMean;
    return qjetsVolatility;
}
    // -------------------------------------------
    // -------------------------------------------


#endif






