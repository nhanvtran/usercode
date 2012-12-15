Bool_t same(Float_t a1, Float_t a2){
    if(TMath::Abs(a1-a2) < 0.001)return 1;
    else return 0;
}

//void DrawLimit_unbin(char* model="unbin")
void DrawLimit_counting(char* model="counting")
{
	TFile inFile(Form("higgisCombin_%s.root",model)) ;
    TTree* tree_limit=inFile.Get("limit");

    Double_t tmp_mh;
    Float_t  tmp_quantileExpected;
    Double_t tmp_limit;

    limit->SetBranchAddress("limit",&tmp_limit);
    limit->SetBranchAddress("mh",&tmp_mh);
    limit->SetBranchAddress("quantileExpected",&tmp_quantileExpected);

	const double nmass = tree_limit.GetEntries()/6.;
	double Mass[nmass] ;
	double Zero[nmass];
    for(Int_t i=0;i<nmass;i++)Zero[i]=0.;

	double Observed[nmass];
	double Median[nmass];
	double N1S [nmass];
	double P1S [nmass];
	double N2S [nmass];
	double P2S [nmass];


	int masspoint=-1;
    for(Int_t i=0;i<nmass*6;i++){
        masspoint=i/6;
        //cout<<"masspoint="<<masspoint<<endl;
        tree_limit->GetEntry(i);

        //cout<<"tmp_quantileExpected="<<tmp_quantileExpected;
        //cout<<"   tmp_limit="<<tmp_limit<<endl;
        if( same(tmp_quantileExpected,0.025)) N2S[masspoint]=tmp_limit;
        if( same(tmp_quantileExpected,0.16 )) N1S[masspoint]=tmp_limit;
        if( same(tmp_quantileExpected,0.5  )) Median[masspoint]=tmp_limit;
        if( same(tmp_quantileExpected,0.84 )) P1S[masspoint]=tmp_limit;
        if( same(tmp_quantileExpected,0.975)) P2S[masspoint]=tmp_limit;
        if( same(tmp_quantileExpected,-1.0 )) Observed[masspoint]=tmp_limit;
        Mass[masspoint]=tmp_mh;
    }

	for (int i=0 ;i<nmass ;i++ )
	{

       // cout<<"Observed="<<Observed[i]<<endl;
       // cout<<"N2S="<<N2S[i]<<endl;
       // cout<<"N1S="<<N1S[i]<<endl;
       // cout<<"mid="<<Median[i]<<endl;
       // cout<<"P1S="<<P1S[i]<<endl;
       // cout<<"P2S="<<P2S[i]<<endl;
		N1S [i] = Median[i] - N1S [i];
		P1S [i] = P1S [i]   - Median[i];

		N2S [i] = Median[i] - N2S [i];
		P2S [i] = P2S [i]   - Median[i];

	}



	TGraph *likelihd_limit_d = new TGraph(nmass,Mass,Observed);                                                                                              
	likelihd_limit_d->SetLineColor(kBlack);                                                                                                                  
	likelihd_limit_d->SetLineWidth(2);                                                                                                                       
	likelihd_limit_d->SetLineStyle(1);
    likelihd_limit_d->SetMarkerStyle(20);


	TGraph *likelihd_limit_c = new TGraph(nmass,Mass,Median);                                                                                                
	likelihd_limit_c->SetLineColor(kBlack);                                                                                                                  
	likelihd_limit_c->SetLineWidth(2);                                                                                                                       
	likelihd_limit_c->SetLineStyle(2);


	TGraphAsymmErrors *likelihd_limit_1sigma = new TGraphAsymmErrors(nmass,Mass,Median,Zero,Zero,N1S,P1S);                                                                                                  
	likelihd_limit_1sigma->SetFillColor(kGreen);


	TGraphAsymmErrors *likelihd_limit_2sigma = new TGraphAsymmErrors(nmass,Mass,Median,Zero,Zero,N2S,P2S);                                                                                                  
	likelihd_limit_2sigma->SetFillColor(kYellow);   


	//  TMultiGraph *likelihd_limit = new TMultiGraph("exclusionlimit_p","CL_{S} Exclusion Limits ;m_{H} [GeV]; 95% CL limit on #sigma/#sigma_{SM}");
	TMultiGraph *likelihd_limit = new TMultiGraph("exclusionlimit_p",";m_{H} [GeV]; 95% CL limit on #sigma/#sigma_{SM}");  
	likelihd_limit->Add(likelihd_limit_2sigma,"E3");                                                                                                         
	likelihd_limit->Add(likelihd_limit_1sigma,"E3");                                                                                                         
	likelihd_limit->Add(likelihd_limit_c, "L");                                                                                                              
	likelihd_limit->Add(likelihd_limit_d, "LP");

	TCanvas *c1 = new TCanvas();
	gStyle->SetOptStat(0);
	//gStyle->SetOptTitle(0);

	TLegend * leg = new TLegend (0.1, 0.65, 0.4, 0.87, NULL, "brNDC") ;
	leg->AddEntry(likelihd_limit_d, "95% C.L.Observed Limit","l");
	leg->AddEntry(likelihd_limit_c, "95% C.L.Expected Limit","l");
	leg->AddEntry(likelihd_limit_1sigma, "#pm1 #sigma Expected Limit","f");
	leg->AddEntry(likelihd_limit_2sigma, "#pm2 #sigma Expected Limit","f");

	leg->SetBorderSize (2.3) ;


	TLegend * title = new TLegend (0.7, 0.92, 0.93, 1, "channel e+mu", "brNDC") ;
	title->SetTextFont (42) ;
	title->SetTextSize (0.04) ;
	title->SetBorderSize (2.3) ;

	//	c1->DrawFrame (225, 0.5, 625, 25) ;
	c1->SetLogy () ;
	//c1->SetGridy(1);


    Double_t y_max_h2=TMath::Max(P2S[nmass-1]+Median[nmass-1]+1, Observed[nmass-1]+1);
    cout<<P2S[nmass-1]+Median[nmass-1]+1<<","<<Observed[nmass-1]+1<<endl;

	//TH2F *h2=new TH2F("h2","CMS preliminary   #int^{}_{}L dt=11.5fb^{-1}(mu)   #sqrt{s}=8TeV;m_{H} [GeV]; 95% CL limit on #sigma/#sigma_{SM}",100,Mass[0]-30,Mass[nmass-1]+30,20,0, y_max_h2);
	TH2F *h2=new TH2F("h2","CMS preliminary   #int^{}_{}L dt=5.3fb^{-1}(mu)   #sqrt{s}=8TeV;m_{H} [GeV]; 95% CL limit on #sigma/#sigma_{SM}",100,Mass[0]-30,Mass[nmass-1]+30,20,0, y_max_h2);
	h2->Draw();



	likelihd_limit->Draw("");	

	//double min = likelihd_limit->GetXaxis ()->GetXmin () ;
	//double max = likelihd_limit->GetXaxis ()->GetXmax () ;
	double min = h2->GetXaxis ()->GetXmin () ;
	double max = h2->GetXaxis ()->GetXmax () ;
    double min_y=Mass[0]-30;
    double max_y=P2S[nmass-1]+Median[nmass-1]+1;


	TLine *line = new TLine(min,1,max,1);
	line->SetLineColor(kRed); line->SetLineWidth(2);
	line->Draw();
    
    for(int i=2;i<max_y;i++){
        TLine *line=new TLine(min,i,max,i);
        line->SetLineColor(kGray+3);line->SetLineStyle(3);
        line->Draw("same");
    }

	//	title->Draw();
    //h2->Draw();
	leg->Draw();
	c1->Update();
	//c1->Print(Form("CL_%s_log.eps",model),"eps");
	//c1->Print(Form("CL_%s_log.png",model),"png");

	c1->SetLogy(0);
	//c1->SetGridy(1);
	c1->Update();
	c1->Print(Form("CL_%s.eps",model),"eps");
	c1->Print(Form("CL_%s.png",model),"png");
}
