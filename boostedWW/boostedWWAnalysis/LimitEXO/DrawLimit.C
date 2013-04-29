Bool_t same(Float_t a1, Float_t a2){
    if(TMath::Abs(a1-a2) < 0.001)return 1;
    else return 0;
}

//https://twiki.cern.ch/twiki/bin/viewauth/CMS/ExoDiBosonResonancesSamples
Double_t XS4Graviton(char* theory_model, Double_t m, Double_t c){//"BulkG"
	Double_t tmp_xs=-1.;
	Double_t tmp_branch_ww_lvjj=0.2882464;
	if(theory_model=="BulkG"){
		if(c==0.2){// TeV, Pb
			/*if(m==0.6){tmp_xs= 0.015     ;}   
			if(m==0.7){tmp_xs= 0.005478  ;}    
			if(m==0.8){tmp_xs= 0.00228   ;}    
			if(m==0.9){tmp_xs= 0.001048  ;}    
			if(m==1.0){tmp_xs= 0.0005114 ;}   
			if(m==1.1){tmp_xs= 0.0002646 ;}   
			if(m==1.2){tmp_xs= 0.00014120;}  
			if(m==1.3){tmp_xs= 7.9031e-05;} 
			if(m==1.4){tmp_xs= 4.5246e-05;} 
			if(m==1.5){tmp_xs= 2.654e-05 ;}   
			if(m==1.6){tmp_xs= 1.5771e-05;} 
			if(m==1.7){tmp_xs= 9.5695e-06;} 
			if(m==1.8){tmp_xs= 5.871e-06 ;}    
			if(m==1.9){tmp_xs= 3.6674e-06;} 
			if(m==2.0){tmp_xs= 2.3073e-06;} 
			if(m==2.1){tmp_xs= 2.3073e-06;} 
			if(m==2.2){tmp_xs= 9.399e-07 ;}  
			if(m==2.3){tmp_xs= 6.0353e-07;} 
			if(m==2.4){tmp_xs= 3.91e-07  ;}  
			if(m==2.5){tmp_xs= 2.5515e-07;} 
			tmp_xs=tmp_xs/tmp_branch_ww_lvjj;*/
			if(m==0.6){tmp_xs= 0.052087;}   
			if(m==0.7){tmp_xs= 0.019006;}    
			if(m==0.8){tmp_xs= 0.0079064;}    
			if(m==0.9){tmp_xs= 0.0036364;}    
			if(m==1.0){tmp_xs= 0.0017742;}   
			if(m==1.1){tmp_xs= 0.00091785;}   
			if(m==1.2){tmp_xs= 0.00049262;}  
			if(m==1.3){tmp_xs= 0.00027418;} 
			if(m==1.4){tmp_xs= 0.00015697;} 
			if(m==1.5){tmp_xs= 9.2073e-05;}   
			if(m==1.6){tmp_xs= 5.4715e-05;} 
			if(m==1.7){tmp_xs= 3.3199e-05;} 
			if(m==1.8){tmp_xs= 2.0367e-05;}    
			if(m==1.9){tmp_xs= 1.2723e-05;} 
			if(m==2.0){tmp_xs= 8.0046e-06;} 
			if(m==2.1){tmp_xs= 5.0566e-06;} 
			if(m==2.2){tmp_xs= 3.2608e-06;}  
			if(m==2.3){tmp_xs= 2.0938e-06;} 
			if(m==2.4){tmp_xs= 1.3566e-06;}  
			if(m==2.5){tmp_xs= 8.8518e-07;}  
		}
		if(c==0.5){// TeV, Pb
			if(m==0.6){tmp_xs= 0.32298;}   
			if(m==0.7){tmp_xs= 0.11827;}    
			if(m==0.8){tmp_xs= 0.04931;}    
			if(m==0.9){tmp_xs= 0.022506;}    
			if(m==1.0){tmp_xs= 0.011035;}   
			if(m==1.1){tmp_xs= 0.0056883;}   
			if(m==1.2){tmp_xs= 0.0030626;}  
			if(m==1.3){tmp_xs= 0.0017003;} 
			if(m==1.4){tmp_xs= 0.00097456;} 
			if(m==1.5){tmp_xs= 0.00056979;}   
			if(m==1.6){tmp_xs= 0.00034149;} 
			if(m==1.7){tmp_xs= 0.00020677;} 
			if(m==1.8){tmp_xs= 0.000127;}    
			if(m==1.9){tmp_xs= 7.9677e-05;} 
			if(m==2.0){tmp_xs= 5.0345e-05;} 
			if(m==2.1){tmp_xs= 3.198e-05;} 
			if(m==2.2){tmp_xs= 2.0502e-05;}  
			if(m==2.3){tmp_xs= 1.324e-05;} 
			if(m==2.4){tmp_xs= 8.6099e-06;}  
			if(m==2.5){tmp_xs= 5.6338e-06;} 
		}
	}

	if(theory_model=="RSG_PY"){//RS Gravition from Pythia
		if(c==0.1){// TeV, Pb
			if(m==0.75){tmp_xs= 2.22    ;}   
			if(m==1.0 ){tmp_xs= 4.254e-1  ;}   
			if(m==1.5 ){tmp_xs= 3.298e-2  ;}   
			if(m==2.0 ){tmp_xs= 4.083e-3  ;} 
			if(m==3.0 ){tmp_xs= 1.01e-4   ;} 
		}
	}
	if(theory_model=="RSG_HW"){//RS Gravition from Pythia
		if(c==0.1){// TeV, Pb
			if(m==0.75){tmp_xs= 9.35    ;}   
			if(m==1.0 ){tmp_xs= 1.82      ;}   
			if(m==1.5 ){tmp_xs= 1.364e-1  ;}   
			if(m==2.0 ){tmp_xs= 1.61e-2   ;} 
			if(m==3.0 ){tmp_xs= 3.72e-4   ;} 
		}
	}

	return tmp_xs;//pb
	//return tmp_xs*1e3;//fb
}

void DrawLimit(char*channel, char* model="unbin", double el_lumi=19.2, double mu_lumi=19.3, bool showobs=0, char* theory_model="BulkG")//"SM"
{
	TFile inFile(Form("higgisCombin_%s_%s.root",channel,model)) ;
    TTree* tree_limit=inFile.Get("limit");

    Double_t tmp_mh;
    Float_t  tmp_quantileExpected;
    Double_t tmp_limit;

    tree_limit->SetBranchAddress("limit",&tmp_limit);
    tree_limit->SetBranchAddress("mh",&tmp_mh);
    tree_limit->SetBranchAddress("quantileExpected",&tmp_quantileExpected);

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
	double XS_theory[nmass];


	int masspoint=-1;
    for(Int_t i=0;i<nmass*6;i++){
        masspoint=i/6;
        tree_limit->GetEntry(i);

        Mass[masspoint]=tmp_mh;
        XS_theory[masspoint]=XS4Graviton("BulkG",tmp_mh/1000.,0.2);

        if( same(tmp_quantileExpected,0.025)) N2S[masspoint]     =tmp_limit*XS_theory[masspoint];
        if( same(tmp_quantileExpected,0.16 )) N1S[masspoint]     =tmp_limit*XS_theory[masspoint];
        if( same(tmp_quantileExpected,0.5  )) Median[masspoint]  =tmp_limit*XS_theory[masspoint];
        if( same(tmp_quantileExpected,0.84 )) P1S[masspoint]     =tmp_limit*XS_theory[masspoint];
        if( same(tmp_quantileExpected,0.975)) P2S[masspoint]     =tmp_limit*XS_theory[masspoint];
        if( same(tmp_quantileExpected,-1.0 )) Observed[masspoint]=tmp_limit*XS_theory[masspoint];
		cout<<"m="<<tmp_mh/1000<<" c="<<0.2<<" XS_theory="<<XS_theory[masspoint]<<" N2S="<<N2S[masspoint]<<" P2S="<<P2S[masspoint]<<endl;
    }

	for (int i=0 ;i<nmass ;i++ )
	{
        cout<<"------------------------------------------"<<endl;
        cout<<"Mass = "<<Mass[i]<<endl;
        cout<<"Observed="<<Observed[i]<<endl;
        cout<<"N2S="<<N2S[i]<<endl;
        cout<<"N1S="<<N1S[i]<<endl;
        cout<<"mid="<<Median[i]<<endl;
        cout<<"P1S="<<P1S[i]<<endl;
        cout<<"P2S="<<P2S[i]<<endl;
		N1S [i] = Median[i] - N1S [i];
		P1S [i] = P1S [i]   - Median[i];

		N2S [i] = Median[i] - N2S [i];
		P2S [i] = P2S [i]   - Median[i];
	}
        cout<<"------------------------------------------"<<endl;


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


	TMultiGraph *likelihd_limit = new TMultiGraph("exclusionlimit_p",";m_{G} [GeV]; 95% CL limit on #sigma#times B(Pb)" );  
	likelihd_limit->Add(likelihd_limit_2sigma,"E3");
	likelihd_limit->Add(likelihd_limit_1sigma,"E3");
	likelihd_limit->Add(likelihd_limit_c, "L");
	if(showobs){ likelihd_limit->Add(likelihd_limit_d, "LP"); }

	TCanvas *c1 = new TCanvas();
	gStyle->SetOptStat(0);
	//gStyle->SetOptTitle(0);
	TLegend * title = new TLegend (0.7, 0.92, 0.93, 1, "channel e+mu", "brNDC") ;
	title->SetTextFont (42) ;
	title->SetTextSize (0.04) ;
	title->SetBorderSize (2.3) ;

	//	c1->DrawFrame (225, 0.5, 625, 25) ;
	c1->SetLogy () ;
	c1->SetGridx(1);
	c1->SetGridy(1);


    Double_t y_max_h2=TMath::Max(P2S[0]+Median[0]+1, Observed[0]+1);
    //Double_t y_max_h2=TMath::Max(P2S[nmass-1]+Median[nmass-1]+1, Observed[nmass-1]+1);
	y_max_h2=1e3;
    cout<<y_max_h2<<" : "<<P2S[nmass-1]+Median[nmass-1]+1<<","<<Observed[nmass-1]+1<<" y_max_h2="<<y_max_h2<<endl;;
	y_min_h2=1e-4;

    TH2D *h2;
	cout<<Mass[0]-30<<" "<<Mass[nmass-1]+30<<" "<< y_max_h2<<endl;
    if(channel=="el"){
	    //TH2F *h2=new TH2F("h2",Form("CMS preliminary   #int^{}_{}L dt=%gfb^{-1}(el)   #sqrt{s}=8TeV;m_{Bulk} [GeV]; 95\% CL limit on #sigma#times B",el_lumi),100,Mass[0]-30,Mass[nmass-1]+30,20,y_min_h2, y_max_h2);
	    TH2F *h2=new TH2F("h2",Form("CMS preliminary   #int^{}_{}L dt=%gfb^{-1}(el)   #sqrt{s}=8TeV;m_{Bulk} [GeV]; 95\% CL limit on #sigma#times B",el_lumi),100,1000,2600,20,0.0000005, 10);
    }
    if(channel=="mu"){
	    //TH2F *h2=new TH2F("h2",Form("CMS preliminary   #int^{}_{}L dt=%gfb^{-1}(mu)   #sqrt{s}=8TeV;m_{Bulk} [GeV]; 95\% CL limit on #sigma#times B",mu_lumi),100,Mass[0]-30,Mass[nmass-1]+30,20,y_min_h2, y_max_h2);
	    TH2F *h2=new TH2F("h2",Form("CMS preliminary   #int^{}_{}L dt=%gfb^{-1}(mu)   #sqrt{s}=8TeV;m_{Bulk} [GeV]; 95\% CL limit on #sigma#times B",mu_lumi),100,1000,2600,20,0.0000005, 10);
    }
    if(channel=="em"){
	    //TH2F *h2=new TH2F("h2",Form("CMS preliminary   #int^{}_{}L dt=%gfb^{-1}(el)+%gfb^{-1}(mu)   #sqrt{s}=8TeV;m_{Bulk} [GeV]; 95\% CL limit on #sigma#times B",el_lumi,mu_lumi),100,Mass[0]-30,Mass[nmass-1]+30,20,y_min_h2, y_max_h2);
	    TH2F *h2=new TH2F("h2",Form("CMS preliminary   #int^{}_{}L dt=%gfb^{-1}(el)+%gfb^{-1}(mu)   #sqrt{s}=8TeV;m_{Bulk} [GeV]; 95\% CL limit on #sigma#times B",el_lumi,mu_lumi),100,1000,2600,20,0.0000005, 10);
    }
    h2->GetYaxis()->SetTitle("95% CL limit on #sigma#times B(Pb)");
	//h2->GetYaxis()->SetMoreLogLabels();
 	h2->Draw();

	likelihd_limit->Draw("");	

	double min = h2->GetXaxis ()->GetXmin () ;
	double max = h2->GetXaxis ()->GetXmax () ;
    double min_y=Mass[0]-30;
    double max_y=P2S[nmass-1]+Median[nmass-1]+1;


	/*TLine *line = new TLine(min,1,max,1);
	line->SetLineColor(kRed); line->SetLineWidth(2);
	line->Draw();*/

	//Draw a smooth XS_theory: 600-2500;
	//double xs_theory_scale=10.;
	double xs_theory_scale=1.;
	double mass_smooth[20];
	double xs_theory_smooth_0p2[20];
	double xs_theory_smooth_0p5[20];
	for(Int_t i=0;i<20;i++){
		mass_smooth[i]=600+100*i;
		xs_theory_smooth_0p2[i]=XS4Graviton("BulkG",mass_smooth[i]/1000.,0.2)*xs_theory_scale;
		xs_theory_smooth_0p5[i]=XS4Graviton("BulkG",mass_smooth[i]/1000.,0.5)*xs_theory_scale;
		cout<<"mass="<<mass_smooth[i]<<" xs="<<xs_theory_smooth_0p2[i]<<endl;
	}
	TGraph *gr_xs_theory_0p2 = new TGraph(20, mass_smooth, xs_theory_smooth_0p2); 
	TGraph *gr_xs_theory_0p5 = new TGraph(20, mass_smooth, xs_theory_smooth_0p5); 
	gr_xs_theory_0p2->SetLineColor(kRed); gr_xs_theory_0p2->SetLineWidth(2); gr_xs_theory_0p2->Draw("");
	gr_xs_theory_0p5->SetLineColor(kRed); gr_xs_theory_0p5->SetLineWidth(2); gr_xs_theory_0p5->SetLineStyle(2); gr_xs_theory_0p5->Draw("");

	/*for(int i=2;i<=y_max_h2;i++){
		if (i%10==0){
			TLine *line=new TLine(min,i,max,i);
			line->SetLineColor(kGray+3);line->SetLineStyle(3);
			line->Draw("same");
		}
	}*/
	/*  double lines_y[9]={1e-4, 1e-3, 1e-2, 1e-1, 1, 1e1, 1e2, 1e3, 1e4};
	for(int i=0;i<9;i++){
		if( lines_y[i]> y_min_h2 &&  lines_y[i]< y_max_h2 ){
			TLine *line=new TLine(min, lines_y[i], max, lines_y[i]);
			line->SetLineColor(kGray+3);line->SetLineStyle(3);
			line->Draw("same");
		}
	}*/

        //draw grid on top of limits
    TH1D* postGrid=new TH1D("postGrid","postGrid",1,600,1000);
    postGrid->GetYaxis()->SetRangeUser(0.0000005, 10);
    postGrid->Draw("AXISSAME");
    postGrid->Draw("AXIGSAME");


	TLegend * leg = new TLegend (0.6, 0.65, 0.9, 0.87, NULL, "brNDC") ;
	if(xs_theory_scale==1.){
		leg->AddEntry(gr_xs_theory_0p2, Form("BulkG->WW, c=0.2"),"l");
		leg->AddEntry(gr_xs_theory_0p5, Form("BulkG->WW, c=0.5"),"l");
	}else{
		leg->AddEntry(gr_xs_theory_0p2, Form("BulkG->WW #times %g, c=0.2",xs_theory_scale),"l");
		leg->AddEntry(gr_xs_theory_0p5, Form("BulkG->WW #times %g, c=0.5",xs_theory_scale),"l");
	}
	leg->AddEntry(likelihd_limit_d, "95% C.L.Observed Limit","l");
	leg->AddEntry(likelihd_limit_c, "95% C.L.Expected Limit","l");
	leg->AddEntry(likelihd_limit_1sigma, "#pm1 #sigma Expected Limit","f");
	leg->AddEntry(likelihd_limit_2sigma, "#pm2 #sigma Expected Limit","f");
	leg->SetBorderSize (2.3) ;

	//	title->Draw();
	//h2->Draw();
	leg->Draw();
	c1->SetGridy(1);
	c1->Update();
	c1->Print(Form("CL_%s_%s_log.pdf",channel,model),"pdf");
	//c1->Print(Form("CL_%s_%s_log.eps",channel,model),"eps");
	c1->Print(Form("CL_%s_%s_log.png",channel,model),"png");
	//c1->SetLogy(0);
	//c1->SetGridy(1);
	//c1->Update();
	//c1->Print(Form("CL_%s_%s.pdf",channel,model),"pdf");
	//c1->Print(Form("CL_%s_%s.eps",channel,model),"eps");
	//c1->Print(Form("CL_%s_%s.png",channel,model),"png");
}
