#!/usr/bin/env python

########################################
##     
##       Author: Wei Zou
##       
##       Email: weizou.pku@gmail.com
#######################################

from ROOT import *

class Samples:
      
      def __init__(self, CHANNEL):
          
          self.filenames = {}
          self.filepath = ""
          self.luminosity = 0.
          self.treename = ""
          self.channel = CHANNEL

      def SetFilePath(self,path):

          self.filepath = path

      def SetLumi(self,lumi):

          self.luminosity = lumi
      
      def SetTreeName(self,tree):

          self.treename = tree

      def SetFileNames(self):
          if self.channel == "mu":
              self.filenames["data"] = self.filepath + "RD_WmunuJets_DataAll_GoldenJSON_19p3invfb.root"
#              self.filenames["data"] = "extraScripts/RDclone.root" 
#              self.filenames["data"] = "/eos/uscms/store/user/lnujj/Moriond2013/ReducedTrees/RD_WmunuJets_DataAll_GoldenJSON_5p3invfb.root" 
              self.filenames["TTbar"] = self.filepath + "RD_mu_TTbar_CMSSW532.root"
              self.filenames["WJets_Pythia"] = self.filepath + "RD_mu_WJets_madgraph_CMSSW532.root"
#              self.filenames["WJets_Pythia"] = self.filepath + "RD_el_WpJPt100_CMSSW532.root"
              self.filenames["WJets_Herwig"] = self.filepath + "RD_mu_WJets_herwig_CMSSW532.root";
              self.filenames["ZJets"] = self.filepath + "RD_mu_ZpJ_CMSSW532.root"
              self.filenames["tch"] = self.filepath + "RD_mu_STopT_T_CMSSW532.root"
              self.filenames["tWch"] = self.filepath + "RD_mu_STopTW_T_CMSSW532.root"
              self.filenames["sch"] = self.filepath + "RD_mu_STopS_T_CMSSW532.root"
              self.filenames["tch_bar"] = self.filepath + "RD_mu_STopT_Tbar_CMSSW532.root"
              self.filenames["tWch_bar"] = self.filepath + "RD_mu_STopTW_Tbar_CMSSW532.root"
              self.filenames["sch_bar"] = self.filepath + "RD_mu_STopS_Tbar_CMSSW532.root"
              self.filenames["WW"] = self.filepath + "RD_mu_WW_CMSSW532.root"
              self.filenames["WZ"] = self.filepath + "RD_mu_WZ_CMSSW532.root"
              self.filenames["ZZ"] = self.filepath + "RD_mu_ZZ_CMSSW532.root"
              self.filenames["ggH600"] = self.filepath + "RD_mu_HWWMH600_CMSSW532_private.root"
              self.filenames["ggH700"] = self.filepath + "RD_mu_HWWMH700_CMSSW532_private.root"
              self.filenames["ggH800"] = self.filepath + "RD_mu_HWWMH800_CMSSW532_private.root"
              self.filenames["ggH900"] = self.filepath + "RD_mu_HWWMH900_CMSSW532_private.root"
              self.filenames["ggH1000"] = self.filepath + "RD_mu_HWWMH1000_CMSSW532_private.root"
              self.filenames["vbfH600"] = self.filepath + "RD_mu_VBFHWWMH600_CMSSW532_private.root"
              self.filenames["vbfH700"] = self.filepath + "RD_mu_VBFHWWMH700_CMSSW532_private.root"
              self.filenames["vbfH800"] = self.filepath + "RD_mu_VBFHWWMH800_CMSSW532_private.root"
              self.filenames["vbfH900"] = self.filepath + "RD_mu_VBFHWWMH900_CMSSW532_private.root"
              self.filenames["vbfH1000"] = self.filepath + "RD_mu_VBFHWWMH1000_CMSSW532_private.root"
          elif self.channel == "el":
              self.filenames["data"] = self.filepath + "RD_WenuJets_DataAllSingleElectronTrigger_GoldenJSON_19p2invfb.root"
#              self.filenames["data"] = "/uscms_data/d3/zixu/Data/RD_Tree_data12_ele/RD_WenuJets_DataAllSingleElectronTrigger_GoldenJSON_5p145.root"                            
              self.filenames["TTbar"] = self.filepath + "RD_el_TTbar_CMSSW532.root";
              self.filenames["WJets_Pythia"] = self.filepath + "RD_el_WJets_madgraph_CMSSW532.root";
#              self.filenames["WJets_Pythia"] = self.filepath + "RD_el_WpJPt100_CMSSW532.root";              
              self.filenames["WJets_Herwig"] = self.filepath + "RD_el_WJets_herwig_CMSSW532.root";
              self.filenames["ZJets"] = self.filepath + "RD_el_ZpJ_CMSSW532.root"
              self.filenames["tch"] = self.filepath + "RD_el_STopT_T_CMSSW532.root"
              self.filenames["tWch"] = self.filepath + "RD_el_STopTW_T_CMSSW532.root"
              self.filenames["sch"] = self.filepath + "RD_el_STopS_T_CMSSW532.root"
              self.filenames["tch_bar"] = self.filepath + "RD_el_STopT_Tbar_CMSSW532.root"
              self.filenames["tWch_bar"] = self.filepath + "RD_el_STopTW_Tbar_CMSSW532.root"
              self.filenames["sch_bar"] = self.filepath + "RD_el_STopS_Tbar_CMSSW532.root"
              self.filenames["WW"] = self.filepath + "RD_el_WW_CMSSW532.root"
              self.filenames["WZ"] = self.filepath + "RD_el_WZ_CMSSW532.root"
              self.filenames["ZZ"] = self.filepath + "RD_el_ZZ_CMSSW532.root"
              self.filenames["ggH600"] = self.filepath + "RD_el_HWWMH600_CMSSW532_private.root"
              self.filenames["ggH700"] = self.filepath + "RD_el_HWWMH700_CMSSW532_private.root"
              self.filenames["ggH800"] = self.filepath + "RD_el_HWWMH800_CMSSW532_private.root"
              self.filenames["ggH900"] = self.filepath + "RD_el_HWWMH900_CMSSW532_private.root"
              self.filenames["ggH1000"] = self.filepath + "RD_el_HWWMH1000_CMSSW532_private.root"
              self.filenames["vbfH600"] = self.filepath + "RD_el_VBFHWWMH600_CMSSW532_private.root"
              self.filenames["vbfH700"] = self.filepath + "RD_el_VBFHWWMH700_CMSSW532_private.root"
              self.filenames["vbfH800"] = self.filepath + "RD_el_VBFHWWMH800_CMSSW532_private.root"
              self.filenames["vbfH900"] = self.filepath + "RD_el_VBFHWWMH900_CMSSW532_private.root"
              self.filenames["vbfH1000"] = self.filepath + "RD_el_VBFHWWMH1000_CMSSW532_private.root"


      def GetLumiScaleFactor(self,txtfile,keyname):
          
          multiplicitylabel = 1.0
          scalefactor = 1.0
          SFfile = open(txtfile)
          for sfline in SFfile:
              if sfline.find("#")!=-1: continue
              if(sfline.find(keyname) != -1):
                 scalefactor = float(sfline.split()[1])
                 if len(sfline.split()) > 2:
                    multiplicitylabel = float(sfline.split()[2])
                 scalefactor = scalefactor * multiplicitylabel
                 break 
          SFfile.close()
          return scalefactor

      def GetFileNames(self):
         
          return self.filenames

      def GetLumi(self):
          
          return self.luminosity

      def GetTreeName(self):
          
          return self.treename
      
