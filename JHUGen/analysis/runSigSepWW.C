void runSigSepWW(int higgsMass=125, double intLumi=20.0, int nToys = 1000, bool draw=false){
    
    using namespace RooFit;
    
    gROOT->ProcessLine(".L ~/tdrstyle.C");
    setTDRStyle();
    gStyle->SetPadLeftMargin(0.16);
    gROOT->ForceStyle();
    
    gROOT->ProcessLine(".L statsFactory.cc+");
    
    double lowMll(12.);
    double highMll = higgsMass;
    double lowMt(0.);
    double highMt = higgsMass;
    double sigRate;
    double bkgRate;
    
    if(higgsMass==125){
      sigRate = 26.;
      bkgRate = 600.;
    }else{
      cout << "HMMMM.... I don't know that mass point...BYE!" << endl;
      return;
    }
         
    RooRealVar* mll = new RooRealVar("mll","Dilepton Mass [GeV]",lowMll, highMll);
    RooRealVar* mt  = new RooRealVar("mt","transverse higgs mass", lowMt, highMt);
    RooArgSet* obs2d = new RooArgSet(*mll, *mt);
    
    const char* cuts = Form("mll<%i&&mll>12&&mt<%i", higgsMass, higgsMass);
    
    // read 0+
    TChain *tplus = new TChain("angles");
    char sigFile[150];
    sprintf(sigFile,"SMHiggsWW_%i_JHU.root",higgsMass);
    tplus->Add(sigFile);
    RooDataSet *zeroPlusData2d = new RooDataSet("sigData2d","sigData2d",tplus,*obs2d, cuts);
    RooDataHist *zeroPlusHist = zeroPlusData2d->binnedClone();
    RooHistPdf* zeroPlusPdf = new RooHistPdf("zeroPlusPdf", "zeroPlusPdf", *obs2d, *zeroPlusHist);

    // read 0-
    TChain *tminus = new TChain("angles");
    sprintf(sigFile,"PSHiggsWW_%i_JHU.root",higgsMass);
    tminus->Add(sigFile);
    RooDataSet *zeroMinusData2d = new RooDataSet("sigData2d","sigData2d",tminus,*obs2d, cuts);
    RooDataHist *zeroMinusHist = zeroMinusData2d->binnedClone();
    RooHistPdf* zeroMinusPdf = new RooHistPdf("zeroMinusPdf", "zeroMinusPdf", *obs2d, *zeroMinusHist);

    // read background
    TChain *bkgTree = new TChain("angles");
    bkgTree->Add("WW_madgraph_8TeV.root");
    RooDataSet *bkgData2d = new RooDataSet("bkgData2d","bkgData2d",bkgTree,*obs2d, cuts);
    RooDataHist *bkgHist = bkgData2d->binnedClone();
    RooHistPdf* bkgPdf = new RooHistPdf("bkgPdf", "bkgPdf", *obs2d, *bkgHist);
    
    RooPlot* plot1 = mll->frame(20);
    RooPlot* plot2 = mt->frame(20);

    if(draw){
    
      // plot 1
      /*
      zeroPlusData2d->plotOn(plot1,MarkerColor(kRed));
      zeroPlusPdf->plotOn(plot1,LineColor(kRed), LineStyle(kDashed));
      */
      zeroMinusData2d->plotOn(plot1,MarkerColor(kBlue));
      zeroMinusPdf->plotOn(plot1,LineColor(kBlue), LineStyle(kDashed));
      /*
      bkgData2d->plotOn(plot1,MarkerColor(kBlack));
      bkgPdf->plotOn(plot1, LineColor(kBlack), LineStyle(kDashed));
      zeroPlusData2d->plotOn(plot2,MarkerColor(kRed));
      zeroPlusPdf->plotOn(plot2,LineColor(kRed), LineStyle(kDashed));
      */
      zeroMinusData2d->plotOn(plot2,MarkerColor(kBlue));
      zeroMinusPdf->plotOn(plot2,LineColor(kBlue), LineStyle(kDashed));
      /*
      bkgData2d->plotOn(plot2,MarkerColor(kBlack));
      bkgPdf->plotOn(plot2, LineColor(kBlack), LineStyle(kDashed));
      */
      TCanvas* fitCan = new TCanvas("fitCan","fitCan",400,400);
      plot1->Draw();
      fitCan->SaveAs(Form("plots/epsfiles/MELAproj2d_0plusVS0minus_125GeV_mll.eps"));

      fitCan->Clear();
      plot2->Draw();
      fitCan->SaveAs(Form("plots/epsfiles/MELAproj2d_0plusVS0minus_125GeV_mt.eps"));
    }

    char statResults2d[25];
    sprintf(statResults2d,"stat_0plusVS0minus_%iGeV_pure_2d.root",higgsMass);
    statsFactory *my2dHypothesisSeparation = new statsFactory(obs2d, zeroPlusPdf, zeroMinusPdf, statResults2d);
    // running the embedded toys
    // my2dHypothesisSeparation->hypothesisSeparationWithBackground(sigRate*intLumi,sigRate*intLumi,nToys, zeroPlusData2d, zeroMinusData2d, bkgPdf,bkgRate*intLumi, bkgData2d);
    // running pure toys
    my2dHypothesisSeparation->hypothesisSeparationWithBackground(sigRate*intLumi,sigRate*intLumi,nToys, bkgPdf,bkgRate*intLumi);
    delete my2dHypothesisSeparation;
    
}
