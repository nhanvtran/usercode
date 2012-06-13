# A class which takes histograms and plots them in a versatile way
# inputs are file names which can be "data" or "MC"
#
# MC is an list of files which one can plot "stacked" or "added"
# MC are stored with a "key" which says which MC it is
# e.g. {1:"diboson", 1:"ttbar",

import ROOT
ROOT.gROOT.ProcessLine(".L tdrstyle.C")
from ROOT import setTDRStyle
ROOT.setTDRStyle()
ROOT.gStyle.SetPalette(1)

ROOT.gSystem.Load('RooUnfold-1.1.1/libRooUnfold.so')
from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes

ROOT.gROOT.ProcessLine('.L myutils.C++')
from ROOT import myutils, TH1F

ROOT.TH1.SetDefaultSumw2()
ROOT.TH2.SetDefaultSumw2()

ROOT.gStyle.SetPadLeftMargin(0.16);

from array import array
import math

class PlotterClass:
    def __init__(self, odir, channel):
        print "welcome"
        data1 = "dummy"; mc1f = []; mc2f = [];
        mc1 = "dummy"; mc2 = "dummy";
        data1c = "dummy"; mc1fc = []; mc2fc = [];
        self.fileNames = [data1,mc1,mc2]
        self.fileNamesStack = [data1,mc1f,mc2f]
        self.contributionNames = [data1c,mc1fc,mc2fc]

        self.theChannel = channel
        self.theOdir = odir
    
        self.ptBins = [125,200,300,400,500]


    def storeFile( self, filename, contributionname, key ): 
        # key is 0 = data, 1 = MC1, 2 = MC2, 3 = ...
            self.fileNames[key] = filename;
            #self.contributionNames[key] = contributionname

    def storeFileStack( self, filename, contributionname, key ): 
        # key is 0 = data, 1 = MC1, 2 = MC2, 3 = ...
        if key == 0:
            self.fileNamesStack[key] = filename;
            self.contributionNames[key] = contributionname
        if key > 0:
            self.fileNamesStack[key].append(filename);
            self.contributionNames[key].append(contributionname);
    
    ######################################################
    
    def GetDataMCSclFactor( self, dat, MC ):
    
        mctotweight = MC.Integral();
        datatotweight = dat.Integral();
        scl = datatotweight/mctotweight;
        MC.Scale( scl )
        print scl,":: mctotweight: ", mctotweight,", datatotweight: ", datatotweight
        return scl
    
    def NormalizeToUnity( self, h ):
        integral = h.Integral()
        h.Scale( 1./integral )

    def NormalizeStackToUnity( self, hs ):
        integral = hs.GetStack().Last().Integral()
        for ii in xrange( hs.GetStack().GetSize() ):
            hs.GetStack().At( ii ).Scale( 1./integral )    

    def SetHistProperties(self, h, linecolor, markercolor, fillcolor, linestyle, markerstyle, fillstyle):
        
        h.SetLineColor( linecolor )
        h.SetMarkerColor( markercolor )
        h.SetFillColor( fillcolor )
        h.SetLineStyle( linestyle )
        h.SetMarkerStyle( markerstyle )
        h.SetFillStyle( fillstyle )
        h.GetYaxis().SetTitleOffset( 1.5 )
        h.SetLineWidth( 2 )

    def NormalizeStackToData( self, hd, hs ):
##         print "scl data = ", hd.GetEntries()
##         print "scl mc = ", hs.GetStack().Last().Integral()
##         print "size of array = ", hs.GetStack().At(0).Integral()
##         print "size of array = ", hs.GetStack().GetSize()
        dataInt = hd.Integral()
        MCInt = hs.GetStack().Last().Integral()

        print "normalization factor = ", str( dataInt/MCInt )
        
        for ii in xrange( hs.GetStack().GetSize() ):
            hs.GetStack().At( ii ).Scale( dataInt/MCInt )

    def doStuff(self, testarg):
        print "do ",testarg," stuff"
        print self.fileNamesStack
        print self.contributionNames

    def SaveCanvas( self, canvas, name ):
        canvas.Print( self.theOdir+"/"+name+".eps", "eps" )
        canvas.Print( self.theOdir+"/"+name+".png", "png" )
        canvas.Print( self.theOdir+"/"+name+".pdf", "pdf" )

    def doUnfolding( self, hResponse_input, hMeas_input, hTrue_input, hData_input ):

        hResponse = hResponse_input
        hTrue = hTrue_input
        hMeas = hMeas_input
        hData = hData_input
        response = RooUnfoldResponse( hMeas, hTrue, hResponse, hMeas.GetName(), hMeas.GetTitle() )

        #    print "hMeas integral: ", hMeas.Integral()

        unfold= RooUnfoldBayes     (response, hData, 4);    #  OR
        # unfold= RooUnfoldSvd     (response, hMeas, 20);   #  OR
        # unfold= RooUnfoldTUnfold (response, hMeas);

        hReco= unfold.Hreco();
#        hReco.SetName( hMeas.GetName() )
#        print "histo names: ",hResponse.GetName(),",",hTrue.GetName(),",",hMeas.GetName(),",",hData.GetName(),",",hReco.GetName()
        return hReco;
###########################################################################################

    def GetHistogramDifference( self, h1, h2, hcentral, sysHistos, doFullSys ):
                
        xbins = array('d', [])
        yval = array('d', [])
        yval_unity = array('d', [])
        ex = array('d', [])
        ey_stat = array('d', [])
        ey_sys = array('d', [])
        ey_statsys = array('d', [])
        ey_stat_f = array('d', [])
        ey_sys_f = array('d', [])
        ey_statsys_f = array('d', [])

        hnamebase = h1.GetName()
        h_PUup = sysHistos[0]
        h_PUdn = sysHistos[1]
        h_JESup = sysHistos[2]
        h_JESdn = sysHistos[3]
        h_JERup = sysHistos[4]
        h_JERdn = sysHistos[5]
        h_JARup = sysHistos[6]
        h_JARdn = sysHistos[7]
        
        ctr = 0
        for ibin in range(1, h1.GetNbinsX() - 1):
            ctr = ctr + 1
            # xval
            xbins.append( h1.GetXaxis().GetBinCenter(ibin) );
            # yval
            bincentralval = hcentral.GetBinContent( ibin )
            yval.append( bincentralval) ;
            yval_unity.append( 1. );
            # xerr
            ex.append( h1.GetXaxis().GetBinWidth(ibin)/2. );
            # yerr
            bindiff = h1.GetBinContent( ibin ) - h2.GetBinContent( ibin );
            sysPS_yerror = (abs( bindiff ) * 0.5)
#            print "bin center = ",h1.GetXaxis().GetBinCenter(ibin),", and bindiff: ",bindiff,", and y error = ",yerror
            sysPU_yerror = 0;   
            sysJES_yerror = 0;   
            sysJER_yerror = 0;   
            sysJAR_yerror = 0;   
            if doFullSys:
                var_PUup = abs( h1.GetBinContent( ibin ) - h_PUup.GetBinContent( ibin ) )
                var_PUdn = abs( h1.GetBinContent( ibin ) - h_PUdn.GetBinContent( ibin ) )                
                sysPU_yerror = max( var_PUup, var_PUdn )*0.5
                var_JESup = abs( h1.GetBinContent( ibin ) - h_JESup.GetBinContent( ibin ) )
                var_JESdn = abs( h1.GetBinContent( ibin ) - h_JESdn.GetBinContent( ibin ) )                
                sysJES_yerror = max( var_JESup, var_JESdn )*0.5
                var_JERup = abs( h1.GetBinContent( ibin ) - h_JERup.GetBinContent( ibin ) )
                var_JERdn = abs( h1.GetBinContent( ibin ) - h_JERdn.GetBinContent( ibin ) )                
                sysJER_yerror = max( var_JERup, var_JERdn )*0.5
                var_JARup = abs( h1.GetBinContent( ibin ) - h_JARup.GetBinContent( ibin ) )
                var_JARdn = abs( h1.GetBinContent( ibin ) - h_JARdn.GetBinContent( ibin ) )                
                sysJAR_yerror = max( var_JARup, var_JARdn )*0.5
                
            print "individual errors: ",sysPS_yerror,",",sysPU_yerror,",",sysJES_yerror,",",sysJER_yerror,",",sysJAR_yerror
        
            #### final accounting
            sys_yerror = 0.
            if doFullSys:
                JesJerJarErr = max(sysJES_yerror, sysJER_yerror, sysJAR_yerror)
                sys_yerror = math.sqrt( sysPS_yerror**2 + JesJerJarErr**2 + sysPU_yerror**2) # place holder
            else:
                sys_yerror = sysPS_yerror        
            print "full sys err: ",sys_yerror
            stat_yerror = hcentral.GetBinError( ibin )
            sys_yerror_f = 0.
            stat_yerror_f = 0.
            if bincentralval > 0:
                stat_yerror_f = stat_yerror/bincentralval;
                sys_yerror_f = sys_yerror/bincentralval;
            else:
                stat_yerror_f = 0
                sys_yerror_f = 0
            
            ey_stat.append( stat_yerror )
            ey_sys.append( sys_yerror )
            ey_statsys.append( math.sqrt(sys_yerror**2 + stat_yerror**2) )

            ey_stat_f.append( stat_yerror_f )
            ey_sys_f.append( sys_yerror_f )
            ey_statsys_f.append( math.sqrt(sys_yerror_f**2 + stat_yerror_f**2) )

        
        tge_stat = ROOT.TGraphErrors( ctr, xbins, yval, ex, ey_stat )
        tge_sys = ROOT.TGraphErrors( ctr, xbins, yval, ex, ey_sys )
        tge_statsys = ROOT.TGraphErrors( ctr, xbins, yval, ex, ey_statsys )

        tge_stat_f = ROOT.TGraphErrors( ctr, xbins, yval_unity, ex, ey_stat_f )
        tge_sys_f = ROOT.TGraphErrors( ctr, xbins, yval_unity, ex, ey_sys_f )
        tge_statsys_f = ROOT.TGraphErrors( ctr, xbins, yval_unity, ex, ey_statsys_f )


        tges = [tge_stat,tge_sys,tge_statsys,tge_stat_f,tge_sys_f,tge_statsys_f]
        return tges

###########################################################################################

    def computeSystematicsUnf( self, hunf_data, hunf_Vjets, hunf_Vjets_sys ):

        xbins = array('d', [])
        yval = array('d', [])
        yval_unity = array('d', [])
        ex = array('d', [])
        ey_stat = array('d', [])
        ey_sys = array('d', [])
        ey_statsys = array('d', [])
        ey_stat_f = array('d', [])
        ey_sys_f = array('d', [])
        ey_statsys_f = array('d', [])
        
        hnamebase = hunf_data.GetName()
        h_PUup = hunf_Vjets_sys[0]
        h_PUdn = hunf_Vjets_sys[1]
        h_JESup = hunf_Vjets_sys[2]
        h_JESdn = hunf_Vjets_sys[3]
        h_JERup = hunf_Vjets_sys[4]
        h_JERdn = hunf_Vjets_sys[5]
        h_JARup = hunf_Vjets_sys[6]
        h_JARdn = hunf_Vjets_sys[7]    
        h_PS = hunf_Vjets_sys[8]
        
        ctr = 0
        for ibin in range(1, hunf_data.GetNbinsX() - 1):
            print "ctr: ",ctr,"...",(hunf_data.GetNbinsX() - 1)
            ctr = ctr + 1
            # xval
            xbins.append( hunf_data.GetXaxis().GetBinCenter(ibin) );
            # xerr
            ex.append( hunf_data.GetXaxis().GetBinWidth(ibin)/2. );
            
            # yval
            bincentralval = hunf_data.GetBinContent( ibin )
            yval.append( bincentralval ) ;
            yval_unity.append( 1. );
            
            # yerr
            bindiff = hunf_Vjets.GetBinContent( ibin ) - h_PS.GetBinContent( ibin );
            sysPS_yerror = (abs( bindiff ) * 0.5)

            sysPU_yerror = 0;   
            sysJES_yerror = 0;   
            sysJER_yerror = 0;   
            sysJAR_yerror = 0;   

            var_PUup = abs( hunf_Vjets.GetBinContent( ibin ) - h_PUup.GetBinContent( ibin ) )
            var_PUdn = abs( hunf_Vjets.GetBinContent( ibin ) - h_PUdn.GetBinContent( ibin ) )                
            sysPU_yerror = max( var_PUup, var_PUdn )*0.5
            var_JESup = abs( hunf_Vjets.GetBinContent( ibin ) - h_JESup.GetBinContent( ibin ) )
            var_JESdn = abs( hunf_Vjets.GetBinContent( ibin ) - h_JESdn.GetBinContent( ibin ) )                
            sysJES_yerror = max( var_JESup, var_JESdn )*0.5
            var_JERup = abs( hunf_Vjets.GetBinContent( ibin ) - h_JERup.GetBinContent( ibin ) )
            var_JERdn = abs( hunf_Vjets.GetBinContent( ibin ) - h_JERdn.GetBinContent( ibin ) )                
            sysJER_yerror = max( var_JERup, var_JERdn )*0.5
            var_JARup = abs( hunf_Vjets.GetBinContent( ibin ) - h_JARup.GetBinContent( ibin ) )
            var_JARdn = abs( hunf_Vjets.GetBinContent( ibin ) - h_JARdn.GetBinContent( ibin ) )                
            sysJAR_yerror = max( var_JARup, var_JARdn )*0.5
            
            print "individual errors: ",sysPS_yerror,",",sysPU_yerror,",",sysJES_yerror,",",sysJER_yerror,",",sysJAR_yerror
            
            #### final accounting
            sys_yerror = 0.
            JesJerJarErr = max(sysJES_yerror, sysJER_yerror, sysJAR_yerror)
            sys_yerror = math.sqrt( sysPS_yerror**2 + JesJerJarErr**2 + sysPU_yerror**2) # place holder

            print "full sys err: ",sys_yerror
            stat_yerror = hunf_data.GetBinError( ibin )
            sys_yerror_f = 0.
            stat_yerror_f = 0.
            if bincentralval > 0:
                stat_yerror_f = stat_yerror/bincentralval;
                sys_yerror_f = sys_yerror/bincentralval;
            else:
                stat_yerror_f = 0
                sys_yerror_f = 0
                
            ey_stat.append( stat_yerror )
            ey_sys.append( sys_yerror )
            ey_statsys.append( math.sqrt(sys_yerror**2 + stat_yerror**2) )
                    
            ey_stat_f.append( stat_yerror_f )
            ey_sys_f.append( sys_yerror_f )
            ey_statsys_f.append( math.sqrt(sys_yerror_f**2 + stat_yerror_f**2) )
                        
        tge_stat = ROOT.TGraphErrors( ctr, xbins, yval, ex, ey_stat )
        tge_sys = ROOT.TGraphErrors( ctr, xbins, yval, ex, ey_sys )
        tge_statsys = ROOT.TGraphErrors( ctr, xbins, yval, ex, ey_statsys )
        
        tge_stat_f = ROOT.TGraphErrors( ctr, xbins, yval_unity, ex, ey_stat_f )
        tge_sys_f = ROOT.TGraphErrors( ctr, xbins, yval_unity, ex, ey_sys_f )
        tge_statsys_f = ROOT.TGraphErrors( ctr, xbins, yval_unity, ex, ey_statsys_f )
                
                
        tges = [tge_stat,tge_sys,tge_statsys,tge_stat_f,tge_sys_f,tge_statsys_f]
        return tges

###########################################################################################
###########################################################################################
###########################################################################################
#### E N D   O F   H  E L P E R S 
###########################################################################################
###########################################################################################
###########################################################################################

    def doKinematicsStacked(self,jettype):
        print "doing kinematic stacked plot"

        # get these histograms for the plot
        histnames = ["h_v_mt_"+jettype, ## 0
                     "h_v_mass_"+jettype,
                     "h_v_pt_"+jettype,
                     "h_e_met_"+jettype,
                     "h_l_pt_"+jettype, ## 4
                     "h_l_eta_"+jettype,
                     "h_lplus_pt_"+jettype,
                     "h_lplus_eta_"+jettype,                     
                     "h_e_nvert_"+jettype, ## 8
                     "h_e_nvert_weighted_"+jettype,
                     "h_"+jettype+"_pt",
                     "h_"+jettype+"_eta",
                     "h_"+jettype+"_phi"                     
                     ]
        histaxes = [";V mT;count",
                    ";V mass;count",
                    ";V pT;count",
                    ";MET;count",
                    ";lepton pT;count",
                    ";lepton #eta;count",
                    ";antilepton pT;count",
                    ";antilepton #eta;count",
                    ";n vertices;count",
                    ";n vertices;count",
                    ";jet pT ("+jettype+");count",
                    ";jet #eta ("+jettype+");count",
                    ";jet #phi ("+jettype+");count"
                    ]
        hdata = []
        hstacks = []
        ftd = ROOT.TFile(self.fileNamesStack[0])
        
        for ii in xrange(len(histnames)):
            # get data hist

            ht1 = ftd.Get(histnames[ii])
            self.SetHistProperties( ht1, 1, 1, 1, 1, 20, 0 )
            hdata.append( ht1.Clone() )
            # print "get entries: ",hdata[0].GetEntries()
            # declare stacked histogram
            hstacks.append( ROOT.THStack("st_"+histnames[ii],";"+histnames[ii]+";") )
            

        # build stacked histogram
        mcfiles = []
        leg = ROOT.TLegend(0.6,0.5,0.9,0.9)
        leg.SetFillColor(0)
        leg.SetBorderSize(0)        
        for jj in xrange(len(self.fileNamesStack[1])):
            print self.fileNamesStack[1][jj]
            mcfiles.append( ROOT.TFile(self.fileNamesStack[1][jj]) )
            for kk in xrange(len(histnames)):
                #print histnames[kk]
                htmp = mcfiles[jj].Get( histnames[kk] ).Clone()
                #print "entries: ",htmp.GetEntries()
                y = jj+2
                self.SetHistProperties( htmp, y, y, y, 1, 1, 1001 )
                hstacks[kk].Add( htmp )
                if kk == 0: leg.AddEntry( htmp, self.contributionNames[1][jj], "f")
                
        #print "get entries: ",hdata[0].GetEntries()
        # normalize the stack
        for ii in xrange(len(histnames)):
            print histnames[ii]
            self.NormalizeStackToData( hdata[ii], hstacks[ii] )

        # define what to plot for W and Z separately
        W_dict = {1:0,2:2,3:3,4:4,5:5,6:10,7:11}
        Z_dict = {1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:10,9:11}
        Whoriz = 2000; Wvert = 800;
        Zhoriz = 1600; Zvert = 1600;

        horiz=0; vert=0;
        div1=0; div2=0;
        dict={}
        if self.theChannel == 1 or self.theChannel == 2:
            horiz=Whoriz; vert=Wvert; div1=4; div2=2; dict=W_dict
        else:
            horiz=Zhoriz; vert=Zvert; div1=3; div2=3; dict=Z_dict

        cs = ROOT.TCanvas("cs","cs",horiz,vert)
        cs.Divide(div1,div2)
        for item in dict:
            cs.cd(item)
            hstacks[ dict[item] ].SetTitle( histaxes[dict[item]] )
            hstacks[ dict[item] ].Draw("hist")            
            if hstacks[ dict[item] ].GetMaximum() < hdata[ dict[item] ].GetMaximum(): 
                hstacks[ dict[item] ].SetMaximum( 1.1*hdata[ dict[item] ].GetMaximum() )
            hdata[ dict[item] ].Draw("sames")
            if item == 2: leg.Draw()
#        self.SaveCanvas( cs, "kinematicsStacked_"+jettype )
        cs.SaveAs( self.theOdir+"/kinematicsStacked_"+jettype+".png" )
        cs.SaveAs( self.theOdir+"/kinematicsStacked_"+jettype+".eps" )
        cs.SaveAs( self.theOdir+"/kinematicsStacked_"+jettype+".pdf" )
            
        cnv = ROOT.TCanvas("cnv","cnv",800,800)
        cnv.cd()
        hA = hstacks[9].GetStack().Last()
        self.SetHistProperties( hA, 2, 2, 2, 1, 1, 0 )
        hA.Draw("hist")
        hB = hstacks[8].GetStack().Last()
        self.SetHistProperties( hB, 4, 4, 4, 1, 1, 0 )
        hB.Draw("histsames")
        hdata[8].Draw("sames")
        cnv.SaveAs( self.theOdir+"/nvert_"+jettype+".png" )
        cnv.SaveAs( self.theOdir+"/nvert_"+jettype+".eps" )
        cnv.SaveAs( self.theOdir+"/nvert_"+jettype+".pdf" )

###########################################################################################

    def doSimpleStack(self,histname,xaxis,canname):

        ftd = ROOT.TFile(self.fileNamesStack[0])
        hd = ftd.Get(histname)
        self.SetHistProperties( hd, 1, 1, 1, 1, 20, 0 )
        hs = ROOT.THStack("st_"+histname,";"+xaxis+";count")
        
        mcfiles = []
        leg = ROOT.TLegend(0.7,0.6,0.9,0.9)
        leg.SetFillColor(0)
        leg.SetBorderSize(0)        
        for jj in xrange(len(self.fileNamesStack[1])):
#            print self.fileNamesStack[1][jj]
            mcfiles.append( ROOT.TFile(self.fileNamesStack[1][jj]) )
            htmp = mcfiles[jj].Get( histname ).Clone()
            y = jj+2
            self.SetHistProperties( htmp, y, y, y, 1, 1, 1001 )
            hs.Add( htmp )
            leg.AddEntry( htmp, self.contributionNames[1][jj], "f")

        self.NormalizeStackToData( hd, hs )

        c0 = ROOT.TCanvas("c0","c0",800,800)
        c0.cd()
        if hs.GetStack().Last().GetMaximum() < hd.GetMaximum(): hs.SetMaximum( hd.GetMaximum()*1.1 )
        hs.Draw("hist")
        hd.Draw("sames")
        leg.Draw()
        c0.Print( self.theOdir+"/"+canname+".png","png" )
        c0.Print( self.theOdir+"/"+canname+".eps","eps" )
        c0.Print( self.theOdir+"/"+canname+".pdf","pdf" )

###########################################################################################

    def doJetMass(self,jettype):
    
        files = []
        jm_histos = []
        for ii in range(3):
            files.append( ROOT.TFile(self.fileNames[ii]) )
            rowhistos = []     
            for jj in range(5): 
                hname =  "h_"+jettype+"_mass_"+str(jj)+"bin"
                print hname
                tmph = files[ii].Get( hname )
                print tmph.GetEntries()
                if ii == 0: self.SetHistProperties( tmph, 1, 1, 1, 1, 20, 0 )
                if ii == 1: self.SetHistProperties( tmph, 2, 2, 2, 1, 20, 0 )
                if ii == 2: self.SetHistProperties( tmph, 4, 4, 4, 1, 20, 0 )                
                rowhistos.append( files[ii].Get( hname ) )
                              
            jm_histos.append( rowhistos )
        ## normalize
        for kk in range(5): 
            self.GetDataMCSclFactor( jm_histos[0][kk], jm_histos[1][kk] )
            self.GetDataMCSclFactor( jm_histos[0][kk], jm_histos[2][kk] )

        ## make ratios
        ratio_m = []
        for ii in range(3):
            row_m = []
            for jj in range(5): 
                tmpr = jm_histos[ii][jj].Clone();
                tmpr.Divide( jm_histos[0][jj] );
                tmpr.GetYaxis().SetRangeUser( 0,2 )
                tmpr.Sumw2()
                if ii == 0: self.SetHistProperties( tmpr, 1, 1, 1, 1, 20, 0 )
                if ii == 1: self.SetHistProperties( tmpr, 2, 2, 2, 1, 20, 0 )
                if ii == 2: self.SetHistProperties( tmpr, 4, 4, 4, 1, 20, 0 )                                
                row_m.append( tmpr )
            ratio_m.append( row_m )
        
        ############################################################
        # plotting
        leg = ROOT.TLegend(0.6,0.6,0.9,0.8)
        leg.SetFillColor(0)
        leg.SetBorderSize(0)
        leg.AddEntry( jm_histos[0][0], "Data", "l" )
        leg.AddEntry( jm_histos[1][0], "Pythia", "l" )
        leg.AddEntry( jm_histos[2][0], "Herwig", "l" )

        leg2 = ROOT.TLegend(0.6,0.3,0.9,0.6)
        leg2.SetFillColor(0)
        leg2.SetBorderSize(0)
        leg2.AddEntry( jm_histos[0][0], "Data", "l" )
        leg2.AddEntry( jm_histos[1][0], "Pythia", "l" )
        leg2.AddEntry( jm_histos[2][0], "Herwig", "l" )

        #        text1 = TLatex()
        #        text1.SetNDC()
        #        text1.SetTextFont(42)
        #        text1.DrawLatex(0.13,0.86, "#scale[1.0]{CMS Preliminary, L = 5 fb^{-1} at  #sqrt{s} = 7 TeV}")
        #        texts.append(text1)

        ptlabel = []
    
        # top part
        c0 = ROOT.TCanvas( "c0", "c0", 800, 800 )
        p1 = ROOT.TPad("p1","p1",0.0,0.3,1.0,0.97)
        p1.SetBottomMargin(0.05)
        p1.SetNumber(1)
        p2 = ROOT.TPad("p2","p2",0.0,0.00,1.0,0.3)
        p2.SetNumber(2)
        p2.SetTopMargin(0.05)
        p2.SetBottomMargin(0.30)
        c0.cd()
        p1.Draw(); p1.cd();
        p1.SetGrid();
        hrl = p1.DrawFrame(0,1,300.,1e4);
        hrl.GetYaxis().SetTitle("count")
        jm_histos[0][0].Draw("sames")
        jm_histos[1][0].Draw("histsames")
        jm_histos[2][0].Draw("histsames") 
        leg.Draw()
        ROOT.gPad.SetLogy()
        # bottom part
        c0.cd()
        p2.Draw(); p2.cd();
        p2.SetGrid();
        hrl2 = p2.DrawFrame(0,0,300.,2);
        hrl2.GetXaxis().SetTitle("jet mass (GeV)"); hrl2.GetXaxis().SetTitleSize(0.14);
        hrl2.GetYaxis().SetTitle("MC/Data"); hrl2.GetYaxis().SetTitleSize(0.14); hrl2.GetYaxis().SetTitleOffset(0.42);
#        ratio_m[0][0].Draw("histsames")
        ratio_m[1][0].Draw("histsames")
        ratio_m[2][0].Draw("histsames")    
        
        self.SaveCanvas( c0, "jetmassReco_"+jettype+"_allpT")
        
        p1s = []
        p2s = []
        c4 = ROOT.TCanvas( "c4", "c4", 1600, 1600 )
        for ii in range(4):
            p1t = ROOT.TPad("p1t"+str(ii),"p1t"+str(ii),0.0,0.3,1.0,0.97)
            p1t.SetBottomMargin(0.05)
            p1t.SetNumber(1)
            p2t = ROOT.TPad("p2t"+str(ii),"p2t"+str(ii),0.0,0.00,1.0,0.3)
            p2t.SetNumber(2)
            p2t.SetTopMargin(0.05)
            p2t.SetBottomMargin(0.30)
            
            p1s.append( p1t )
            p2s.append( p2t )
        
        c4.Divide(2,2)
        xranges_ptbins = [150,150,200,300]
        for ii in range(4):
            
            c4.cd( ii   +1 )
            p1s[ii].Draw(); p1s[ii].cd();
            p1s[ii].SetGrid();
            hr = p1s[ii].DrawFrame(0,1,xranges_ptbins[ii],1e4);
            hr.GetYaxis().SetTitle("count")            
            jm_histos[0][ii+1].Draw("sames")
            jm_histos[1][ii+1].Draw("histsames")
            jm_histos[2][ii+1].Draw("histsames") 
            if ii == 0: leg2.Draw()
            
            text2 = ROOT.TLatex()
            text2.SetNDC()
            text2.SetTextFont(42)
            text2.SetTextSize(0.07)
            text2.DrawLatex( 0.55, 0.75, str(self.ptBins[ii]) + ' < p_{T}^{j} < ' + str(self.ptBins[ii+1])  )
            
            ROOT.gPad.SetLogy()            
            c4.cd( ii   +1 )
            p2s[ii].Draw(); p2s[ii].cd();
            p2s[ii].SetGrid();
            hr2 = p2s[ii].DrawFrame(0,0,xranges_ptbins[ii],2);
            hr2.GetXaxis().SetTitle("jet mass (GeV)"); hr2.GetXaxis().SetTitleSize(0.14);
            hr2.GetYaxis().SetTitle("MC/Data"); hr2.GetYaxis().SetTitleSize(0.14); hr2.GetYaxis().SetTitleOffset(0.42);
#            ratio_m[0][ii+1].Draw("sames")
            ratio_m[1][ii+1].Draw("histsames")
            ratio_m[2][ii+1].Draw("histsames")            
    
        self.SaveCanvas( c4, "jetmassReco_"+jettype+"_pTbins")

###########################################################################################

    def doJetMassUnfolded(self,jettype,responseMatrixFile):
        
        files = []
        
        systags = ["_PUup","_PUdn","_JESup","_JESdn","_JERup","_JERdn","_JARup","_JARdn"]
        
        ## --------------------
        ## Get the RECO and GEN level histograms
        jm_histos = [] ## 2d list [dataOrMC1orMC2][ptbins]
        jm_histosGEN = []
        jm_histosSYS = [] ## different 2d list [ptbins][systags] for MC1
        for ii in range(3):
            files.append( ROOT.TFile(self.fileNames[ii]) )
            rowhistos = []     
            rowhistosGEN = []
            for jj in range(5): 
                hname =  "h_"+jettype+"_mass_"+str(jj)+"bin"
                tmph = files[ii].Get( hname )
                if ii == 0: self.SetHistProperties( tmph, 1, 1, 1, 1, 20, 0 )
                if ii == 1: self.SetHistProperties( tmph, 2, 2, 2, 1, 20, 0 )
                if ii == 2: self.SetHistProperties( tmph, 4, 4, 4, 1, 20, 0 )                
                rowhistos.append( tmph )
                # gen jets for ii > 0
                if ii == 1:
                    hnameGEN =  "h_"+jettype+"g_mass_"+str(jj)+"bin"
#                    print "hnameGEN: ",hnameGEN
                    tmphGEN = files[ii].Get( hnameGEN )
                    if ii == 0: self.SetHistProperties( tmphGEN, 1, 1, 1, 1, 20, 0 )
                    if ii == 1: self.SetHistProperties( tmphGEN, 2, 2, 2, 1, 20, 0 )
                    if ii == 2: self.SetHistProperties( tmphGEN, 4, 4, 4, 1, 20, 0 )                
                    rowhistosGEN.append( tmphGEN )
                    # get sys
                    row_hsys = []
                    for kk in xrange(len(systags)):
                        row_hsys.append( files[ii].Get( hname+systags[kk] ) )
                    jm_histosSYS.append( row_hsys )
            
                else: rowhistosGEN.append( ROOT.TH1F('dummy'+str(ii)+str(jj),'dummy'+str(ii)+str(jj),100,0,1) )  
            
            jm_histos.append( rowhistos )
            jm_histosGEN.append( rowhistosGEN )
        
        ## --------------------
        ## Get the response matrices, either from [1] or from arg                
        frFN = ""
        if responseMatrixFile == "NONE": frfN = self.fileNames[1]
        else: frfN = responseMatrixFile            
        fr = ROOT.TFile( frfN )
        jm_responses = []
        for jj in range(5): 
            rname = "rur_"+jettype+"w_"+str(jj)+"bin"
            jm_responses.append( fr.Get( rname ) )

        ## save response matrices
        c0r = ROOT.TCanvas( "c0r", "c0r", 800, 800 )
        c0r.cd()
        jm_responses[0].GetXaxis().SetTitle("generated jet mass")
        jm_responses[0].GetYaxis().SetTitle("reconstructed jet mass")
        jm_responses[0].Draw("colz")
        ROOT.gPad.SetLogx();ROOT.gPad.SetLogy();
        self.SaveCanvas( c0r, "unf_resrponse_"+jettype+"_allpT")
        c4r = ROOT.TCanvas( "c4r", "c4", 1200, 1200 )
        c4r.Divide(2,2)
        for ii in range(4):
            c4r.cd( ii   +1 )
            jm_responses[ii+1].GetXaxis().SetTitle("generated jet mass")
            jm_responses[ii+1].GetYaxis().SetTitle("reconstructed jet mass")
            jm_responses[ii+1].Draw("colz")
            ROOT.gPad.SetLogx();ROOT.gPad.SetLogy();
            text2 = ROOT.TLatex()
            text2.SetNDC()
            text2.SetTextFont(42)
            text2.SetTextSize(0.07)
            text2.DrawLatex( 0.20, 0.80, str(self.ptBins[ii]) + ' < p_{T}^{j} < ' + str(self.ptBins[ii+1])  )
        self.SaveCanvas( c4r, "unf_response_"+jettype+"_pTbins")

        ## --------------------
        ## do the unfolding 
        jm_unf = []
        jm_unfSYS = []
        for ii in range(3):
            row_unf = []
            for jj in range(5): 
                tmph = self.doUnfolding( jm_responses[jj], jm_histos[1][jj], jm_histosGEN[1][jj], jm_histos[ii][jj] )
                if ii == 0: self.SetHistProperties( tmph, 1, 1, 1, 1, 20, 0 )
                if ii == 1: self.SetHistProperties( tmph, 2, 2, 2, 1, 20, 0 )
                if ii == 2: self.SetHistProperties( tmph, 4, 4, 4, 1, 20, 0 )                                
                row_unf.append( tmph )
                if ii == 1:
                    row_sys = []
                    for kk in xrange(len(systags)):
                        tmpsys = self.doUnfolding( jm_responses[jj], jm_histos[1][jj], jm_histosGEN[1][jj], jm_histosSYS[jj][kk] )
                        row_sys.append( tmpsys )
                    jm_unfSYS.append( row_sys )
            jm_unf.append( row_unf )

        ## normalize
        ## must divide by bin width too
        for kk in range(5): 
            self.GetDataMCSclFactor( jm_unf[0][kk], jm_unf[1][kk] )
            self.GetDataMCSclFactor( jm_unf[0][kk], jm_unf[2][kk] )
            self.NormalizeToUnity( jm_unf[0][kk] )
            self.NormalizeToUnity( jm_unf[1][kk] )
            self.NormalizeToUnity( jm_unf[2][kk] )
            jm_unf[0][kk].Scale( 1./jm_unf[0][kk].GetBinWidth(1) )
            jm_unf[1][kk].Scale( 1./jm_unf[1][kk].GetBinWidth(1) )
            jm_unf[2][kk].Scale( 1./jm_unf[2][kk].GetBinWidth(1) )
            for ll in xrange(len(systags)):
                self.NormalizeToUnity( jm_unfSYS[kk][ll] )
                jm_unfSYS[kk][ll].Scale( 1./jm_unfSYS[kk][ll].GetBinWidth(1) )

        ## make ratios
        rat_unf = []
        for ii in range(3):
            row_unf = []
            for jj in range(5): 
                tmpr = jm_unf[ii][jj].Clone();
                tmpr.Divide( jm_unf[0][jj] );
                tmpr.GetYaxis().SetRangeUser( 0,2 )
                tmpr.Sumw2()
                if ii == 0: self.SetHistProperties( tmpr, 1, 1, 1, 1, 20, 0 )
                if ii == 1: self.SetHistProperties( tmpr, 2, 2, 2, 1, 20, 0 )
                if ii == 2: self.SetHistProperties( tmpr, 4, 4, 4, 1, 20, 0 )                                
                row_unf.append( tmpr )
            rat_unf.append( row_unf )

        ############################################################
        # shower systematics + all other systematics

        tge_stat = []
        tge_showersys = []
        tge_statsys = []
        tge_stat_f = []
        tge_showersys_f = []
        tge_statsys_f = []

        # eitehr shower systematics or full systematics (+JES+JER+JAR+PU)
        doFullSys = True;

        for jj in range(5):
            curtge = self.GetHistogramDifference( jm_unf[1][jj], jm_unf[2][jj], jm_unf[0][jj], jm_unfSYS[jj], doFullSys )
            curtge[0].SetFillStyle( 1001 ); curtge[0].SetFillColor( ROOT.kYellow );
            curtge[1].SetFillStyle( 1001 ); curtge[1].SetFillColor( ROOT.kYellow-2 );
            curtge[2].SetFillStyle( 1001 ); curtge[2].SetFillColor( ROOT.kCyan-2 );            
            curtge[3].SetFillStyle( 1001 ); curtge[3].SetFillColor( ROOT.kYellow );
            curtge[4].SetFillStyle( 1001 ); curtge[4].SetFillColor( ROOT.kYellow-2 );
            curtge[5].SetFillStyle( 1001 ); curtge[5].SetFillColor( ROOT.kCyan-2 );            
            tge_stat.append( curtge[0] )
            tge_showersys.append( curtge[1] )
            tge_statsys.append( curtge[2] )
            tge_stat_f.append( curtge[3] )
            tge_showersys_f.append( curtge[4] )
            tge_statsys_f.append( curtge[5] )

        c0 = ROOT.TCanvas( "c0", "c0", 800, 800 )
        p1 = ROOT.TPad("p1","p1",0.0,0.3,1.0,0.97)
        p1.SetBottomMargin(0.05)
        p1.SetNumber(1)
        p2 = ROOT.TPad("p2","p2",0.0,0.00,1.0,0.3)
        p2.SetNumber(2)
        p2.SetTopMargin(0.05)
        p2.SetBottomMargin(0.30)
        
        ############################################################
        # plotting
        leg = ROOT.TLegend(0.6,0.6,0.9,0.8)
        leg.SetFillColor(0)
        leg.SetBorderSize(0)
        leg.AddEntry( tge_stat[0], "Data", "p" )
        leg.AddEntry( tge_statsys[0], "Tot. Uncertainty", "f" )
        leg.AddEntry( tge_stat[0], "Stat. Uncertainty", "f" )
        leg.AddEntry( jm_unf[1][0], "Pythia", "l" )
        leg.AddEntry( jm_unf[2][0], "Herwig", "l" )

        leg2 = ROOT.TLegend(0.6,0.3,0.9,0.6)
        leg2.SetFillColor(0)
        leg2.SetBorderSize(0)
        leg2.AddEntry( tge_stat[0], "Data", "p" )
        leg2.AddEntry( tge_statsys[0], "Tot. Uncertainty", "f" )
        leg2.AddEntry( tge_stat[0], "Stat. Uncertainty", "f" )
        leg2.AddEntry( jm_unf[1][0], "Pythia", "l" )
        leg2.AddEntry( jm_unf[2][0], "Herwig", "l" )

#        text1 = TLatex()
#        text1.SetNDC()
#        text1.SetTextFont(42)
#        text1.DrawLatex(0.13,0.86, "#scale[1.0]{CMS Preliminary, L = 5 fb^{-1} at  #sqrt{s} = 7 TeV}")
#        texts.append(text1)
        
        ptlabel = []

        # top part
        c0.cd()
        p1.Draw(); p1.cd();
        p1.SetGrid();
        hrl = p1.DrawFrame(0,1e-5,300.,1);
        hrl.GetYaxis().SetTitle("(1/#sigma)(d#sigma/dm)")
        tge_statsys[0].Draw("2p")
        tge_stat[0].SetMarkerStyle( 20 )
        tge_stat[0].Draw("2psames")
        jm_unf[1][0].Draw("histsames")
        jm_unf[2][0].Draw("histsames") 
        leg.Draw()
        ROOT.gPad.SetLogy()
        # bottom part
        c0.cd()
        p2.Draw(); p2.cd();
        p2.SetGrid();
        hrl2 = p2.DrawFrame(0,0,300.,2);
        hrl2.GetXaxis().SetTitle("jet mass (GeV)"); hrl2.GetXaxis().SetTitleSize(0.14);
        hrl2.GetYaxis().SetTitle("MC/Data"); hrl2.GetYaxis().SetTitleSize(0.14); hrl2.GetYaxis().SetTitleOffset(0.42);
        tge_statsys_f[0].Draw("2")
        tge_stat_f[0].SetMarkerStyle( 0 )
        tge_stat_f[0].Draw("2sames")
        rat_unf[1][0].Draw("histsames")
        rat_unf[2][0].Draw("histsames")    

        self.SaveCanvas( c0, "jetmassunf_"+jettype+"_allpT")

        p1s = []
        p2s = []
        c4 = ROOT.TCanvas( "c4", "c4", 1600, 1600 )
        for ii in range(4):
            p1t = ROOT.TPad("p1t"+str(ii),"p1t"+str(ii),0.0,0.3,1.0,0.97)
            p1t.SetBottomMargin(0.05)
            p1t.SetNumber(1)
            p2t = ROOT.TPad("p2t"+str(ii),"p2t"+str(ii),0.0,0.00,1.0,0.3)
            p2t.SetNumber(2)
            p2t.SetTopMargin(0.05)
            p2t.SetBottomMargin(0.30)

            p1s.append( p1t )
            p2s.append( p2t )

        c4.Divide(2,2)
        xranges_ptbins = [150,150,200,300]
        for ii in range(4):

            c4.cd( ii   +1 )
            p1s[ii].Draw(); p1s[ii].cd();
            p1s[ii].SetGrid();
            hr = p1s[ii].DrawFrame(0,1e-5,xranges_ptbins[ii],1);
            hr.GetYaxis().SetTitle("(1/#sigma)(d#sigma/dm)")            
            tge_statsys[ii+1].Draw("2p")
            tge_stat[ii+1].SetMarkerStyle( 20 )
            tge_stat[ii+1].Draw("2psames")
            jm_unf[1][ii+1].Draw("histsames")
            jm_unf[2][ii+1].Draw("histsames") 
            if ii == 0: leg2.Draw()
            
            text2 = ROOT.TLatex()
            text2.SetNDC()
            text2.SetTextFont(42)
            text2.SetTextSize(0.07)
            text2.DrawLatex( 0.55, 0.75, str(self.ptBins[ii]) + ' < p_{T}^{j} < ' + str(self.ptBins[ii+1])  )
            
            ROOT.gPad.SetLogy()            
            c4.cd( ii   +1 )
            p2s[ii].Draw(); p2s[ii].cd();
            p2s[ii].SetGrid();
            hr2 = p2s[ii].DrawFrame(0,0,xranges_ptbins[ii],2);
            hr2.GetXaxis().SetTitle("jet mass (GeV)"); hr2.GetXaxis().SetTitleSize(0.14);
            hr2.GetYaxis().SetTitle("MC/Data"); hr2.GetYaxis().SetTitleSize(0.14); hr2.GetYaxis().SetTitleOffset(0.42);
            tge_statsys_f[ii+1].Draw("2")
            tge_stat_f[ii+1].SetMarkerStyle( 0 )
            tge_stat_f[ii+1].Draw("2sames")
            rat_unf[1][ii+1].Draw("histsames")
            rat_unf[2][ii+1].Draw("histsames")            

        self.SaveCanvas( c4, "jetmassunf_"+jettype+"_pTbins")
        ############################################################

###########################################################################################

    def doJetMassUnfolded_BkgSubtraction(self,jettype,responseMatrixFile, ptBin):

        histname = "h_"+jettype+"_mass_"+str(ptBin)+"bin"
        
        responseMatrixFile_psSystematic = responseMatrixFile.replace("MadGraph","Herwig")
        print "responseMatrixFile_psSystematic: ",responseMatrixFile_psSystematic

        chanName = ""
        if self.theChannel == 1 or self.theChannel == 2: chanName = "Wjets"
        else: chanName = "Zjets"
        
        # build stacked histogram
        datafile = ROOT.TFile( self.fileNames[0] )
        mcfile_Vjets = ROOT.TFile( responseMatrixFile )
        mcfile_Vjets_psSystematic = ROOT.TFile( responseMatrixFile_psSystematic )
        mcfiles_Bkgs = []        
        for jj in xrange(len(self.fileNamesStack[1])):
            if self.contributionNames[1][jj].find(chanName) < 0:
                mcfiles_Bkgs.append( ROOT.TFile(self.fileNamesStack[1][jj]) )
                print "filenames for bkg: ",self.fileNamesStack[1][jj]
            
        systags = ["_PUup","_PUdn","_JESup","_JESdn","_JERup","_JERdn","_JARup","_JARdn"]

        h_Vjets = mcfile_Vjets.Get(histname)
        h_data = datafile.Get(histname)
        h_Bkgs = []
        h_Vjets_sys = []
        for i in xrange(len(mcfiles_Bkgs)):
            h_Bkgs.append( mcfiles_Bkgs[i].Get(histname) )
        for i in xrange(len(systags)):
            h_Vjets_sys.append( mcfile_Vjets.Get(histname+systags[i]) )

        response_matrix = mcfile_Vjets.Get( "rur_"+jettype+"w_"+str(ptBin)+"bin" )
        response_meas = mcfile_Vjets.Get( "h_"+jettype+"_mass_"+str(ptBin)+"bin" )
        response_true = mcfile_Vjets.Get( "h_"+jettype+"g_mass_"+str(ptBin)+"bin" )

        h_Vjets_ps = mcfile_Vjets_psSystematic.Get( "h_"+jettype+"_mass_"+str(ptBin)+"bin" )
        response_matrix_psSystematic = mcfile_Vjets_psSystematic.Get( "rur_"+jettype+"w_"+str(ptBin)+"bin" )
        response_meas_psSystematic = mcfile_Vjets_psSystematic.Get( "h_"+jettype+"_mass_"+str(ptBin)+"bin" )
        response_true_psSystematic = mcfile_Vjets_psSystematic.Get( "h_"+jettype+"g_mass_"+str(ptBin)+"bin" )

            
        ## ---- subtract backgrounds, put in by hand difference between theory and measured XS if needed            
        print "integral before = ",h_data.Integral()
        for i in xrange(len(mcfiles_Bkgs)):
            h_data.Add( h_Bkgs[i], -1 )
            print "n bkg: ",h_Bkgs[i].GetEntries()
        print "integral after = ",h_data.Integral()
    
        ## ---- unfold all matrices (PS uncertainty needs a different response matrix)
        hunf_Vjets = self.doUnfolding( response_matrix, response_meas, response_true, h_Vjets )
        hunf_Vjets_ps = self.doUnfolding( response_matrix, response_meas, response_true, h_Vjets_ps )
        hunf_data = self.doUnfolding( response_matrix, response_meas, response_true, h_data )
        hunf_Vjets_sys = []
        for i in xrange(len(systags)):
            hunf_Vjets_sys.append( self.doUnfolding( response_matrix, response_meas, response_true, h_Vjets_sys[i] ) )
        # append the PS systematic at the end
#        hunf_Vjets_sys.append( self.doUnfolding( response_matrix_psSystematic, response_meas_psSystematic, response_true_psSystematic, h_Vjets ) )
        hunf_Vjets_sys.append( self.doUnfolding(  response_matrix, response_meas, response_true, h_Vjets ) )

        ## ---- normalize all histograms
        self.NormalizeToUnity( hunf_Vjets )
        self.NormalizeToUnity( hunf_Vjets_ps )
        self.NormalizeToUnity( hunf_data )
        for i in xrange(len(systags)+1):
            self.NormalizeToUnity( hunf_Vjets_sys[i] )
        hunf_Vjets.Scale( 1./h_data.GetBinWidth(1) )
        hunf_Vjets_ps.Scale( 1./h_data.GetBinWidth(1) )
        hunf_data.Scale( 1./h_data.GetBinWidth(1) )
        for i in xrange(len(systags)+1):
            hunf_Vjets_sys[i].Scale( 1./h_data.GetBinWidth(1) )

        ## ---- compute all systematics
        curtge = self.computeSystematicsUnf( hunf_data, hunf_Vjets, hunf_Vjets_sys )
       
        # --- MC/data    
        hunf_Vjets_f = hunf_Vjets.Clone()
        hunf_Vjets_f.Divide( hunf_data );
        hunf_Vjets_f.GetYaxis().SetRangeUser( 0,2 )
        hunf_Vjets_f.Sumw2()
        hunf_Vjets_ps_f = hunf_Vjets_ps.Clone()
        hunf_Vjets_ps_f.Divide( hunf_data );
        hunf_Vjets_ps_f.GetYaxis().SetRangeUser( 0,2 )
        hunf_Vjets_ps_f.Sumw2()

        self.SetHistProperties( hunf_Vjets, 2, 2, 2, 1, 0, 0 )
        self.SetHistProperties( hunf_Vjets_ps, 4, 4, 4, 1, 0, 0 )
        self.SetHistProperties( hunf_Vjets_f, 2, 2, 2, 1, 0, 0 )
        self.SetHistProperties( hunf_Vjets_ps_f, 4, 4, 4, 1, 0, 0 )

        ## ---- plot!  
        curtge[0].SetFillStyle( 1001 ); curtge[0].SetFillColor( ROOT.kYellow );
        curtge[1].SetFillStyle( 1001 ); curtge[1].SetFillColor( ROOT.kYellow-2 );
        curtge[2].SetFillStyle( 1001 ); curtge[2].SetFillColor( ROOT.kCyan-2 );            
        curtge[3].SetFillStyle( 1001 ); curtge[3].SetFillColor( ROOT.kYellow );
        curtge[4].SetFillStyle( 1001 ); curtge[4].SetFillColor( ROOT.kYellow-2 );
        curtge[5].SetFillStyle( 1001 ); curtge[5].SetFillColor( ROOT.kCyan-2 );            
        tge_stat = curtge[0]
        tge_sys = curtge[1] 
        tge_statsys = curtge[2] 
        tge_stat_f = curtge[3] 
        tge_sys_f = curtge[4] 
        tge_statsys_f = curtge[5] 

        c0 = ROOT.TCanvas( "c0", "c0", 800, 800 )
        p1 = ROOT.TPad("p1","p1",0.0,0.3,1.0,0.97)
        p1.SetBottomMargin(0.05)
        p1.SetNumber(1)
        p2 = ROOT.TPad("p2","p2",0.0,0.00,1.0,0.3)
        p2.SetNumber(2)
        p2.SetTopMargin(0.05)
        p2.SetBottomMargin(0.30)

        ############################################################
        # plotting
        leg = ROOT.TLegend(0.6,0.6,0.9,0.8)
        leg.SetFillColor(0)
        leg.SetBorderSize(0)
        leg.AddEntry( tge_stat, "Data", "p" )
        leg.AddEntry( tge_statsys, "Tot. Uncertainty", "f" )
        leg.AddEntry( tge_stat, "Stat. Uncertainty", "f" )
        leg.AddEntry( hunf_Vjets, "Pythia", "l" )
        leg.AddEntry( hunf_Vjets_ps, "Herwig", "l" )

        ptlabel = []

        # top part
        c0.cd()
        p1.Draw(); p1.cd();
        p1.SetGrid();
        hrl = p1.DrawFrame(0,1e-5,300.,1.0);
        hrl.GetYaxis().SetTitle("(1/#sigma)(d#sigma/dm)")
        tge_statsys.Draw("2p")
        tge_stat.SetMarkerStyle( 20 )
        tge_stat.Draw("2psames")
        hunf_Vjets.Draw("histsames"); hunf_Vjets.SetMinimum( 1e-5 );
        hunf_Vjets_ps.Draw("histsames"); hunf_Vjets_ps.SetMinimum( 1e-5 ); 
        hunf_Vjets_clone = hunf_Vjets_f.Clone()
        hunf_Vjets_ps_clone = hunf_Vjets_ps_f.Clone()    
        hunf_Vjets_clone.Draw("pesames")
        hunf_Vjets_ps_clone.Draw("pesames")    
        leg.Draw()
        ROOT.gPad.SetLogy()
        # bottom part
        c0.cd()
        p2.Draw(); p2.cd();
        p2.SetGrid();
        hrl2 = p2.DrawFrame(0,0,300.,2);
        hrl2.GetXaxis().SetTitle("jet mass (GeV)"); hrl2.GetXaxis().SetTitleSize(0.14);
        hrl2.GetYaxis().SetTitle("MC/Data"); hrl2.GetYaxis().SetTitleSize(0.14); hrl2.GetYaxis().SetTitleOffset(0.42);
        tge_statsys_f.Draw("2")
        tge_stat_f.SetMarkerStyle( 0 )
        tge_stat_f.Draw("2sames")
        hunf_Vjets_f.Draw("histsames")
        hunf_Vjets_ps_f.Draw("histsames")    
        hunf_Vjets_f_clone = hunf_Vjets_f.Clone()
        hunf_Vjets_ps_f_clone = hunf_Vjets_ps_f.Clone()    
        hunf_Vjets_f_clone.Draw("pesames")
        hunf_Vjets_ps_f_clone.Draw("pesames")    

        if ptBin == 0:
            self.SaveCanvas( c0, "jetmassunf_"+jettype+"_allpT")
        else:
            self.SaveCanvas( c0, "jetmassunf_"+jettype+"_pTBin"+str(ptBin))
            

###########################################################################################

    def doClosureTest(self):
        
        # get histograms (x3)
        fm = ROOT.TFile( self.fileNames[1] )
        hresp = fm.Get("rur_ak7w_closure")
        hmeas = fm.Get("h_ak7_mass")
        htrue = fm.Get("h_ak7g_mass")
        hdata = fm.Get("hunfw_ak7_mass_closure")
        print htrue.GetEntries()
        print hdata.GetEntries()
        # do unfolding
        hunf = self.doUnfolding( hresp, hmeas, htrue, hdata )
        # normalize
        self.NormalizeToUnity( hmeas )
        self.NormalizeToUnity( htrue )
        self.NormalizeToUnity( hdata )
        self.NormalizeToUnity( hunf )        
        self.SetHistProperties( htrue, 4, 4, 4, 1, 1, 0 )
        self.SetHistProperties( hmeas, 6, 6, 6, 2, 1, 0 )        
        self.SetHistProperties( hunf, 1, 1, 1, 1, 20, 0 )        
        
        text2 = ROOT.TLatex()
        text2.SetNDC()
        text2.SetTextFont(42)
        text2.SetTextSize(0.07)
        
        leg = ROOT.TLegend(0.6,0.6,0.9,0.8)
        leg.SetFillColor(0)
        leg.SetBorderSize(0)
        leg.AddEntry(hmeas, "Raw", "l")
        leg.AddEntry(htrue, "True", "l")
        leg.AddEntry(hunf, "Unfolded", "pl")
        
        # plot
        c0 = ROOT.TCanvas("c0","c0",800,800)
        hmeas.GetXaxis().SetTitle("jet mass, AK7 (GeV)")
        hmeas.Draw("hist")
        htrue.Draw("histsames")
#        hdata.Draw("sames")
        hunf.Draw("sames")
        text2.DrawLatex( 0.55, 0.85, "closure test"  )
        leg.Draw()
        ROOT.gPad.SetLogy()
        self.SaveCanvas( c0, "closureTest_ak7" )
            

###########################################################################################

    def doJetResponse(self, mcfilename, jettype):

        theutils = myutils()
        
        prPt_names = []
        prNV_names = []
        prEta_names = []      
        groomedsuffix = ["","tr","ft","pr"]
        groomedname = ["ungroomed","trimmed","filtered","pruned"]
        
        fmc = ROOT.TFile(mcfilename)

        for ii in xrange(len(groomedsuffix)):
            prPt_names.append( "prPt_pt"+jettype+groomedsuffix[ii]+"_ov"+jettype.upper()+groomedsuffix[ii]+"g" )
            prNV_names.append( "prNV_pt"+jettype+groomedsuffix[ii]+"_ov"+jettype.upper()+groomedsuffix[ii]+"g" )
            prEta_names.append( "prEta_pt"+jettype+groomedsuffix[ii]+"_ov"+jettype.upper()+groomedsuffix[ii]+"g" )

        prPt_mean = []
        prNV_mean = []
        prEta_mean = []
        prPt_sigma = []
        prNV_sigma = []
        prEta_sigma = []

        leg = ROOT.TLegend(0.4,0.2,0.65,0.4)
        leg.SetFillColor(0)
        leg.SetBorderSize(0)
        leg2 = ROOT.TLegend(0.4,0.7,0.65,0.9)
        leg2.SetFillColor(0)
        leg2.SetBorderSize(0)

        for ii in xrange(len(groomedsuffix)):
            tmp = fmc.Get( prPt_names[ii] )
            print "entries: ",tmp.GetEntries()

            tmp0 = theutils.GetFitSlicesY( fmc.Get( prPt_names[ii] ), 1 ); tmp0.SetName("prPt_mean"+str(ii));
            tmp1 = theutils.GetFitSlicesY( fmc.Get( prNV_names[ii] ), 1 ); tmp1.SetName("prNV_mean"+str(ii));
            tmp2 = theutils.GetFitSlicesY( fmc.Get( prEta_names[ii] ), 1 ); tmp2.SetName("prEta_mean"+str(ii));
            tmp3 = theutils.GetFitSlicesY( fmc.Get( prPt_names[ii] ), 2 ); tmp3.SetName("prPt_sigma"+str(ii));
            tmp4 = theutils.GetFitSlicesY( fmc.Get( prNV_names[ii] ), 2 ); tmp4.SetName("prNV_sigma"+str(ii));
            tmp5 = theutils.GetFitSlicesY( fmc.Get( prEta_names[ii] ), 2 ); tmp5.SetName("prEta_sigma"+str(ii));

            prPt_mean.append( tmp0 )            
            prNV_mean.append( tmp1 )            
            prEta_mean.append( tmp2 )            
            prPt_sigma.append( tmp3 )            
            prNV_sigma.append( tmp4 )            
            prEta_sigma.append( tmp5 )
        
            yy = ii+1
            self.SetHistProperties( prPt_mean[ii], yy, yy, yy, 1, 20+ii, 0 )
            self.SetHistProperties( prNV_mean[ii], yy, yy, yy, 1, 20+ii, 0 )
            self.SetHistProperties( prEta_mean[ii], yy, yy, yy, 1, 20+ii, 0 )
            self.SetHistProperties( prPt_sigma[ii], yy, yy, yy, 1, 20+ii, 0 )
            self.SetHistProperties( prNV_sigma[ii], yy, yy, yy, 1, 20+ii, 0 )
            self.SetHistProperties( prEta_sigma[ii], yy, yy, yy, 1, 20+ii, 0 )                
            
            leg.AddEntry( prPt_mean[ii], groomedname[ii], "pe" )
            leg2.AddEntry( prPt_mean[ii], groomedname[ii], "pe" )


        cpr0 = ROOT.TCanvas("cpr0","cpr0",800,800)
        cpr0.cd();
        cpr0.SetGrid();
        h0 = cpr0.DrawFrame(125,0.8,500,1.2)
        h0.GetYaxis().SetTitle("fitted mean, pT_{RECO}/pT_{GEN}")
        h0.GetXaxis().SetTitle("pT_{RECO}")
        for ii in xrange(len(groomedsuffix)):
            prPt_mean[ii].Draw("pesames")
        leg.Draw()
        self.SaveCanvas( cpr0, "jetResponse_vPt_mean_"+jettype )

        cpr1 = ROOT.TCanvas("cpr1","cpr1",800,800)
        cpr1.cd();
        cpr1.SetGrid();
        h1 = cpr1.DrawFrame(0,0.8,40,1.2)
        h1.GetYaxis().SetTitle("fitted mean, pT_{RECO}/pT_{GEN}")
        h1.GetXaxis().SetTitle("N_{PV}")
        for ii in xrange(len(groomedsuffix)):
            prNV_mean[ii].Draw("pesames")
        leg.Draw()
        self.SaveCanvas( cpr1, "jetResponse_vNV_mean_"+jettype )

        cpr2 = ROOT.TCanvas("cpr2","cpr2",800,800)
        cpr2.cd();
        cpr2.SetGrid();
        h2 = cpr2.DrawFrame(-3,0.8,3,1.2)
        h2.GetYaxis().SetTitle("fitted mean, pT_{RECO}/pT_{GEN}")
        h2.GetXaxis().SetTitle("#eta_{RECO}")
        for ii in xrange(len(groomedsuffix)):
            prEta_mean[ii].Draw("pesames")
        leg.Draw()
        self.SaveCanvas( cpr2, "jetResponse_vEta_mean_"+jettype )
            
        cpr3 = ROOT.TCanvas("cpr3","cpr3",800,800)
        cpr3.cd();
        cpr3.SetGrid();
        h3 = cpr3.DrawFrame(125,0.,500,0.2)
        h3.GetYaxis().SetTitle("fitted #sigma, pT_{RECO}/pT_{GEN}")
        h3.GetXaxis().SetTitle("pT_{RECO}")
        for ii in xrange(len(groomedsuffix)):
            prPt_sigma[ii].Draw("pesames")
        leg2.Draw()
        self.SaveCanvas( cpr3, "jetResponse_vPt_sigma_"+jettype )

        cpr4 = ROOT.TCanvas("cpr4","cpr4",800,800)
        cpr4.cd();
        cpr4.SetGrid();
        h4 = cpr4.DrawFrame(0,0,40,0.2)
        h4.GetYaxis().SetTitle("fitted #sigma,pT_{RECO}/pT_{GEN}")
        h4.GetXaxis().SetTitle("N_{PV}")
        for ii in xrange(len(groomedsuffix)):
            prNV_sigma[ii].Draw("pesames")
        leg2.Draw()
        self.SaveCanvas( cpr4, "jetResponse_vNV_sigma_"+jettype )

        cpr5 = ROOT.TCanvas("cpr5","cpr5",800,800)
        cpr5.cd();
        cpr5.SetGrid();
        h5 = cpr5.DrawFrame(-3,0,3,0.2)
        h5.GetYaxis().SetTitle("fitted #sigma,pT_{RECO}/pT_{GEN}")
        h5.GetXaxis().SetTitle("#eta_{RECO}")
        for ii in xrange(len(groomedsuffix)):
            prEta_sigma[ii].Draw("pesames")
        leg2.Draw()
        self.SaveCanvas( cpr5, "jetResponse_vEta_sigma_"+jettype )            

###########################################################################################

    def doJetMassRatio(self, mcfilename, jettype):
    
        print jettype.upper()
        histnames = []
        histnamesGEN = []   
        prPt_names = []
        prNV_names = []
        prEta_names = []        
        prPt_namesGEN = []
        prNV_namesGEN = []
        prEta_namesGEN = []        
        groomedsuffix = ["tr","ft","pr"]
        groomedname = ["trimmed","filtered","pruned"]
        
        for ii in xrange(len(groomedsuffix)):
            histnames.append( "hrat_"+jettype+groomedsuffix[ii]+"_mass_ov"+jettype.upper() )
            histnamesGEN.append( "hrat_"+jettype+groomedsuffix[ii]+"g_mass_ov"+jettype.upper()+"g" )            

            prPt_names.append( "prPt_mass"+jettype+groomedsuffix[ii]+"_ov"+jettype.upper() )
            prPt_namesGEN.append( "prPt_mass"+jettype+groomedsuffix[ii]+"g_ov"+jettype.upper()+"g" )            
            prNV_names.append( "prNV_mass"+jettype+groomedsuffix[ii]+"_ov"+jettype.upper() )
            prNV_namesGEN.append( "prNV_mass"+jettype+groomedsuffix[ii]+"g_ov"+jettype.upper()+"g" )            
            prEta_names.append( "prEta_mass"+jettype+groomedsuffix[ii]+"_ov"+jettype.upper() )
            prEta_namesGEN.append( "prEta_mass"+jettype+groomedsuffix[ii]+"g_ov"+jettype.upper()+"g" )            
            
            print histnames[ii],",",histnamesGEN[ii]

        jmrat_d = []
        jmrat_mc = []        
        jmrat_gen = []  
        prPt_d = []
        prPt_mc = []        
        prPt_gen = []  
        prNV_d = []
        prNV_mc = []        
        prNV_gen = []  
        prEta_d = []
        prEta_mc = []        
        prEta_gen = []  
        fd = ROOT.TFile(self.fileNames[0])
        fmc = ROOT.TFile(mcfilename)
        fgen = ROOT.TFile(mcfilename)
        for ii in xrange(len(groomedsuffix)):
            yy = ii+2
            
            tmpd = fd.Get( histnames[ii] )
            self.NormalizeToUnity( tmpd )
            self.SetHistProperties( tmpd, yy, yy, yy, 1, 20, 0 )
            jmrat_d.append( tmpd )

            tmpmc = fmc.Get( histnames[ii] )
            self.NormalizeToUnity( tmpmc )
            self.SetHistProperties( tmpmc, yy, yy, yy, 1, 1, 0 )
            tmpmc.SetLineWidth( 2 )
            jmrat_mc.append( tmpmc )

            tmpgen = fgen.Get( histnamesGEN[ii] )
            self.NormalizeToUnity( tmpgen )
            self.SetHistProperties( tmpgen, yy, yy, yy, 2, 1, 0 )
            tmpgen.SetLineWidth( 2 )
            jmrat_gen.append( tmpgen )      

            prPt_d.append( fd.Get( prPt_names[ii] ).ProfileX() ); prPt_d[ii].SetName("prPt_d_"+str(ii));
            prPt_mc.append( fmc.Get( prPt_names[ii] ).ProfileX() ); prPt_mc[ii].SetName("prPt_mc_"+str(ii)); 
            prPt_gen.append( fgen.Get( prPt_namesGEN[ii] ).ProfileX() ); 
            prNV_d.append( fd.Get( prNV_names[ii] ).ProfileX() ); prNV_d[ii].SetName("prNV_d_"+str(ii));
            prNV_mc.append( fmc.Get( prNV_names[ii] ).ProfileX() ); prNV_mc[ii].SetName("prNV_mc_"+str(ii));
            prNV_gen.append( fgen.Get( prNV_namesGEN[ii] ).ProfileX() )
            prEta_d.append( fd.Get( prEta_names[ii] ).ProfileX() ); prEta_d[ii].SetName("prEta_d_"+str(ii));
            prEta_mc.append( fmc.Get( prEta_names[ii] ).ProfileX() ); prEta_d[ii].SetName("prEta_mc_"+str(ii));
            prEta_gen.append( fgen.Get( prEta_namesGEN[ii] ).ProfileX() )

            self.SetHistProperties( prPt_d[ii], yy, yy, yy, 1, 20, 0 )
            self.SetHistProperties( prNV_d[ii], yy, yy, yy, 1, 20, 0 )
            self.SetHistProperties( prEta_d[ii], yy, yy, yy, 1, 20, 0 )
            self.SetHistProperties( prPt_mc[ii], yy, yy, yy, 1, 0, 3244 )
            self.SetHistProperties( prNV_mc[ii], yy, yy, yy, 1, 0, 3244 )
            self.SetHistProperties( prEta_mc[ii], yy, yy, yy, 1, 0, 3244 )
            self.SetHistProperties( prPt_gen[ii], yy, yy, yy, 1, 0, 1001 )
            self.SetHistProperties( prNV_gen[ii], yy, yy, yy, 1, 0, 1001 )
            self.SetHistProperties( prEta_gen[ii], yy, yy, yy, 1, 0, 1001 )

        leg = ROOT.TLegend(0.2,0.5,0.6,0.9)
        leg.SetFillColor(0)
        leg.SetBorderSize(0)
        for ii in xrange(len(groomedsuffix)): leg.AddEntry( jmrat_d[ii], "data, "+groomedname[ii]+"/ungroomed", "pl")
        for ii in xrange(len(groomedsuffix)): leg.AddEntry( jmrat_mc[ii], "mc (reco) , "+groomedname[ii]+"/ungroomed", "l")
        for ii in xrange(len(groomedsuffix)): leg.AddEntry( jmrat_gen[ii], "mc (gen), "+groomedname[ii]+"/ungroomed", "l")

        leg2 = ROOT.TLegend(0.35,0.58,0.75,0.9)
        leg2.SetFillColor(0)
        leg2.SetBorderSize(0)
        for ii in xrange(len(groomedsuffix)): leg2.AddEntry( prPt_d[ii], "data, "+groomedname[ii]+"/ungroomed", "pl")
        for ii in xrange(len(groomedsuffix)): leg2.AddEntry( prPt_mc[ii], "mc (reco) , "+groomedname[ii]+"/ungroomed", "f")
        for ii in xrange(len(groomedsuffix)): leg2.AddEntry( prPt_gen[ii], "mc (gen), "+groomedname[ii]+"/ungroomed", "f")
    
        crat = ROOT.TCanvas("crat","crat",1200,800)
        crat.cd();
        hrl = crat.DrawFrame(0,0,1,0.15)
        hrl.GetXaxis().SetTitle( "jet mass ratio, "+jettype )
        hrl.GetYaxis().SetTitle( "a.u." )
        for ii in xrange(len(groomedsuffix)):
            jmrat_d[ii].Draw("psames")
            jmrat_mc[ii].Draw("histsames")
            jmrat_gen[ii].Draw("histsames")
        leg.Draw()
        self.SaveCanvas( crat, "jetmass_1Dratio_"+jettype )
            
        cratPt = ROOT.TCanvas("cratPt","cratPt",800,800)
        cratPt.cd();
        hrl1 = cratPt.DrawFrame(125,0,500,2)
        hrl1.GetXaxis().SetTitle( "jet pT" )
        hrl1.GetYaxis().SetTitle( "<jet mass ratio>" )
        for ii in xrange(len(groomedsuffix)):
            prPt_d[ii].Draw("pex0sames")
            prPt_mc[ii].Draw("e2sames")
            prPt_gen[ii].Draw("e2sames")
        leg2.Draw()
        self.SaveCanvas( cratPt, "jetmass_ratioprofilePt_"+jettype )                    

        cratNV = ROOT.TCanvas("cratNV","cratNV",800,800)
        cratNV.cd();
        cratNV.SetGrid();
        hrl2 = cratNV.DrawFrame(0,0,40,2)
        hrl2.GetXaxis().SetTitle( "N_{PV}" )
        hrl2.GetYaxis().SetTitle( "<jet mass ratio>" )
        for ii in xrange(len(groomedsuffix)):
            prNV_d[ii].Draw("pex0sames")
            prNV_mc[ii].Draw("e2sames")
            prNV_gen[ii].Draw("e2sames")
        leg2.Draw()
        self.SaveCanvas( cratNV, "jetmass_ratioprofileNV_"+jettype )            
    
        cratEta = ROOT.TCanvas("cratEta","cratEta",800,800)
        cratEta.cd();
        cratEta.SetGrid();
        hrl3 = cratEta.DrawFrame(-3,0,3,2)
        hrl3.GetXaxis().SetTitle( "jet #eta" )
        hrl3.GetYaxis().SetTitle( "<jet mass ratio>" )
        for ii in xrange(len(groomedsuffix)):
            prEta_d[ii].Draw("pex0sames")
            prEta_mc[ii].Draw("e2sames")
            prEta_gen[ii].Draw("e2sames")
        leg2.Draw()
        self.SaveCanvas( cratEta, "jetmass_ratioprofileEta_"+jettype )            
            

###########################################################################################
    
    def doJetMassProjection(self,jetMassProjection,canvasname):
        
        fd = ROOT.TFile(self.fileNames[0])
        fmc = ROOT.TFile(self.fileNames[1])

        print self.fileNames[0],",",self.fileNames[1]
        
        prPt_d = [];
        prNV_d = [];
        prEta_d = [];        
        prPt_mc = [];
        prNV_mc = [];
        prEta_mc = [];    
        
        leg = ROOT.TLegend(0.2,0.6,0.45,0.9)
        leg.SetFillColor(0)
        leg.SetBorderSize(0)
        for ii in xrange(len(jetMassProjection)):
            print jetMassProjection[ii]
            prPt_d.append( fd.Get("prPt_mass_"+jetMassProjection[ii]).ProfileX() )
            prNV_d.append( fd.Get("prNV_mass_"+jetMassProjection[ii]).ProfileX() )
            prEta_d.append( fd.Get("prEta_mass_"+jetMassProjection[ii]).ProfileX() )
            prPt_d[ii].SetName( "dprPt_mass_"+jetMassProjection[ii] )
            prNV_d[ii].SetName( "dprNV_mass_"+jetMassProjection[ii] )
            prEta_d[ii].SetName( "dprEta_mass_"+jetMassProjection[ii] )

            prPt_mc.append( fmc.Get("prPt_mass_"+jetMassProjection[ii]).ProfileX() )
            prNV_mc.append( fmc.Get("prNV_mass_"+jetMassProjection[ii]).ProfileX() )
            prEta_mc.append( fmc.Get("prEta_mass_"+jetMassProjection[ii]).ProfileX() )
            prPt_mc[ii].SetName( "mprPt_mass_"+jetMassProjection[ii] )
            prNV_mc[ii].SetName( "mprNV_mass_"+jetMassProjection[ii] )
            prEta_mc[ii].SetName( "mprEta_mass_"+jetMassProjection[ii] )

            self.SetHistProperties( prPt_d[ii], ii+1,ii+1,0,1,24,0 )
            self.SetHistProperties( prNV_d[ii], ii+1,ii+1,0,1,24,0 )
            self.SetHistProperties( prEta_d[ii], ii+1,ii+1,0,1,24,0 )

            self.SetHistProperties( prPt_mc[ii], ii+1,ii+1,ii+1,1,0,3244 )
            self.SetHistProperties( prNV_mc[ii], ii+1,ii+1,ii+1,1,0,3244 )
            self.SetHistProperties( prEta_mc[ii], ii+1,ii+1,ii+1,1,0,3244 )
            
            leg.AddEntry( prPt_d[ii], "data, "+jetMassProjection[ii], "pe" )
            leg.AddEntry( prPt_mc[ii], "mc, "+jetMassProjection[ii], "f" )
        
        ## add legend...
        
        c0 = ROOT.TCanvas("c0","c0",800,800)
        c0.cd();
        c0.SetGrid();
        hrl = c0.DrawFrame(120,0,500,100)
        hrl.GetXaxis().SetTitle("jet pT (GeV)")
        hrl.GetYaxis().SetTitle("<jet mass> (GeV)")
        for ii in xrange(len(jetMassProjection)):
            prPt_d[ii].Draw("pex0sames")
            prPt_mc[ii].DrawCopy("e2sames")  
        leg.Draw()
        self.SaveCanvas( c0, "jetmassproj_vPt_"+canvasname )


        c1 = ROOT.TCanvas("c1","c1",800,800)
        c1.cd();
        c1.SetGrid();
        hrl1 = c1.DrawFrame(0,0,40,100)
        hrl1.GetXaxis().SetTitle("N_{PV}")
        hrl1.GetYaxis().SetTitle("<jet mass> (GeV)")
        for ii in xrange(len(jetMassProjection)):
            prNV_d[ii].Draw("pex0sames")
            prNV_mc[ii].DrawCopy("e2sames")  
        leg.Draw()
        c1.SaveAs("test.eps")
        self.SaveCanvas( c1, "jetmassproj_vNV_"+canvasname )

        c2 = ROOT.TCanvas("c2","c2",800,800)
        c2.cd();
        c2.SetGrid();
        hrl2 = c2.DrawFrame(-3,0,3,100)
        hrl2.GetXaxis().SetTitle("jet #eta")
        hrl2.GetYaxis().SetTitle("<jet mass> (GeV)")
        for ii in xrange(len(jetMassProjection)):
            prEta_d[ii].Draw("pex0sames")
            prEta_mc[ii].DrawCopy("e2sames")  
        leg.Draw()
        self.SaveCanvas( c2, "jetmassproj_vEta_"+canvasname )