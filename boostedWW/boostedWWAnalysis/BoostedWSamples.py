#!/usr/bin/env python

########################################
##     
##       Author: Wei Zou
##       
##       Email: weizou.pku@gmail.com
#######################################

from ROOT import *

class Samples:
      
      def __init__(self):
          
          self.filenames = {}
          self.filepath = ""
          self.luminosity = 0.
          self.treename = ""

      def SetFilePath(self,path):

          self.filepath = path

      def SetLumi(self,lumi):

          self.luminosity = lumi
      
      def SetTreeName(self,tree):

          self.treename = tree

      def SetFileNames(self):
          
          self.filenames["data"] = self.filepath + "RD_WmunuJets_DataAll_GoldenJSON_9p9invfb.root"
           
          self.filenames["TTbar"] = self.filepath + "RD_mu_TTbar_CMSSW532.root"
         
          self.filenames["WJets"] = self.filepath + "RD_mu_WpJPt100_CMSSW532.root"

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
      
