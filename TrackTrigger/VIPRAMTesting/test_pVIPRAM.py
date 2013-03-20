#! /usr/bin/env python
import ROOT
import os

from pVIPRAM_inputBuilderClass import *
from pVIPRAM_inputVisualizerClass import *

ROOT.gStyle.SetPalette(1);

from optparse import OptionParser
############################################
#            Job steering                  #
############################################
parser = OptionParser()

parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
parser.add_option('--testA', action='store_true', dest='testA', default=False, help='run testA')
parser.add_option('--testB', action='store_true', dest='testB', default=False, help='run testB')
parser.add_option('--testC', action='store_true', dest='testC', default=False, help='run testC')
parser.add_option('--testD', action='store_true', dest='testD', default=False, help='run testD')

(options, args) = parser.parse_args()
############################################


# -------------------------------------------------
# -------------------------------------------------
# --->   m a i n
# -------------------------------------------------
# -------------------------------------------------
if __name__ == '__main__':


    # -------------------------------------------------
    # testing individual rows and columns
    if options.testA:
        if not os.path.isdir("testInputSingle"): os.system("mkdir testInputSingle");
        nRows = 128;
        nColumns = 32;
        tmpInput = inputBuilder("testInputSingle/testSingle.root");
        for i in range(nRows):
            print "row: ",i
            for j in range(nColumns):
                tmpInput.initializeLoadPhase();
                tmpInput.loadUniformPatterns(0, 0, 8); # row, col, input value
                tmpInput.initializeRunPhase( [1,0,0,0] ); # choose majority logic (miss0, miss1, miss2, layerA)
                tmpInput.checkPattern( [8,8,8,8] ); # run mode, look for a single pattern
                #tmpInput.doRowChecker( i ); # cheat mode, look at a particular row

        tmpInput.close();

        tmpVisualizer = inputVisualizer( tmpInput.getFilename() );
        #tmpVisualizer.textVisualizer();
        #tmpVisualizer.visualize("test.eps");
        tmpVisualizer.writeToText( "testInputSingle/testSingle.txt" );

    # -------------------------------------------------    
    # testing disable road
    if options.testB:
        if not os.path.isdir("testDisableBit"): os.system("mkdir testDisableBit");
        tmpInput_disabled = inputBuilder( "testDisableBit/testDisableBit.root" );
        tmpInput_disabled.initializeLoadPhase();
        tmpInput_disabled.loadUniformPatterns(0, 0, 2, 0); # row, col, input value, disable road
        tmpInput_disabled.initializeRunPhase( [1,0,0,0] ); # choose majority logic (miss0, miss1, miss2, layerA)
        tmpInput_disabled.checkPattern( [2,2,2,2] ); # run mode, look for a single pattern
        #tmpInput_disabled.doRowChecker( 0 ); # cheat mode, look at a particular row
        tmpInput_disabled.close();
            
        tmpVisualizer_disabled = inputVisualizer( tmpInput_disabled.getFilename() );
        tmpVisualizer_disabled.writeToText( "testDisableBit/testDisableBit.txt" );
    
    # -------------------------------------------------    
    # testing walking
    if options.testC:
        if not os.path.isdir("testWalking"): os.system("mkdir testWalking");
        nRows = 128;
        nColumns = 32;
        tmpWalking = inputBuilder( "testWalking/testWalking.root" );
        tmpWalking.initializeLoadPhase();
        print "Loading..."
        ctr = 0;
        for i in range(nRows):
            print "row: ",i
            for j in range(nColumns):
                tmpWalking.loadUniformPatterns(i, j, ctr); # row, col, input value, disable road
                ctr += 1;
        tmpWalking.initializeRunPhase( [1,0,0,0] ); # choose majority logic (miss0, miss1, miss2, layerA)

        print "Running..."
        ctr = 0;
        for i in range(nRows):
            print "row: ",i
            for j in range(nColumns):
                tmpWalking.checkPattern( [ctr,ctr,ctr,ctr] ); # run mode, look for a single pattern
                #tmpWalking.printInternalPatterns( i );
                #tmpWalking.doRowChecker( i ); # cheat mode, look at a particular row
                ctr += 1;
        tmpWalking.close();
            
        tmpWalkingVisualizer = inputVisualizer( tmpWalking.getFilename() );
        tmpWalkingVisualizer.textVisualizer();
        tmpWalkingVisualizer.writeToText( "testWalking/testWalking.txt" );


        tmpWalking2 = inputBuilder( "testWalking/testWalking.root" );
        tmpWalking2.initializeLoadPhase();
        print "Loading..."
        ctr = 0;
        for i in range(nRows):
            print "row: ",i
            for j in range(nColumns):
                tmpWalking2.loadUniformPatterns(i, j, ctr); # row, col, input value, disable road
                ctr += 1;
        tmpWalking2.initializeRunPhase( [1,0,0,0] ); # choose majority logic (miss0, miss1, miss2, layerA)

        print "Running..."
        ctr = 0;
        for i in range(nRows):
            print "row: ",i
            for j in range(nColumns):
                if j % 2 == 0: tmpWalking2.checkPattern( [ctr,ctr,ctr,ctr] ); # run mode, look for a single pattern
                #tmpWalking2.printInternalPatterns( i );
                #tmpWalking2.doRowChecker( i ); # cheat mode, look at a particular row
                ctr += 1;
#        print "Cheating..."
#        for i in range(nRows):
#            print "row: ",i
#            tmpWalking2.doRowChecker( i ); # cheat mode, look at a particular row
        tmpWalking2.close();

        tmpWalking2Visualizer = inputVisualizer( tmpWalking2.getFilename() );
        tmpWalking2Visualizer.textVisualizer();
        tmpWalking2Visualizer.writeToText( "testWalking/testWalking2.txt" );
            
    # -------------------------------------------------    
    # testing majority logic
    if options.testD:
        if not os.path.isdir("testMajorityLogic"): os.system("mkdir testMajorityLogic");
        tmpInput_miss0 = inputBuilder( "testMajorityLogic/tmpInput_miss0.root" );
        tmpInput_miss0.initializeLoadPhase();
        tmpInput_miss0.loadSinglePattern(0, 0, [2,2,2,2]); # row, col, input value
        tmpInput_miss0.initializeRunPhase( [1,0,0,0] ); # choose majority logic (miss0, miss1, miss2, layerA)
        tmpInput_miss0.checkPattern( [2,2,2,2] ); # run mode, look for a single pattern
        #tmpInput_miss0.doRowChecker( 0 ); # cheat mode, look at a particular row
        tmpInput_miss0.close();
        tmpVisualizer_miss0 = inputVisualizer( tmpInput_miss0.getFilename() );
        tmpVisualizer_miss0.writeToText( "testMajorityLogic/tmpInput_miss0.txt" );

        tmpInput_miss1 = inputBuilder( "testMajorityLogic/tmpInput_miss1.root" );
        tmpInput_miss1.initializeLoadPhase();
        tmpInput_miss1.loadSinglePattern(0, 0, [2,99,2,2]); # row, col, input value
        tmpInput_miss1.initializeRunPhase( [0,1,0,0] ); # choose majority logic (miss1, miss1, miss2, layerA)
        tmpInput_miss1.checkPattern( [2,0,2,2] ); # run mode, look for a single pattern
        #tmpInput_miss1.doRowChecker( 0 ); # cheat mode, look at a particular row
        tmpInput_miss1.close();
        tmpVisualizer_miss1 = inputVisualizer( tmpInput_miss1.getFilename() );
        tmpVisualizer_miss1.writeToText( "testMajorityLogic/tmpInput_miss1.txt" );

        tmpInput_miss2 = inputBuilder( "testMajorityLogic/tmpInput_miss2.root" );
        tmpInput_miss2.initializeLoadPhase();
        tmpInput_miss2.loadSinglePattern(0, 0, [2,99,99,2]); # row, col, input value
        tmpInput_miss2.initializeRunPhase( [0,0,1,0] ); # choose majority logic (miss2, miss1, miss2, layerA)
        tmpInput_miss2.checkPattern( [2,999,999,2] ); # run mode, look for a single pattern
        #tmpInput_miss2.doRowChecker( 0 ); # cheat mode, look at a particular row
        tmpInput_miss2.close();
        tmpVisualizer_miss2 = inputVisualizer( tmpInput_miss2.getFilename() );
        tmpVisualizer_miss2.writeToText( "testMajorityLogic/tmpInput_miss2.txt" );

        tmpInput_layerA = inputBuilder( "testMajorityLogic/tmpInput_layerA.root" );
        tmpInput_layerA.initializeLoadPhase();
        tmpInput_layerA.loadSinglePattern(0, 0, [2,99,99,99]); # row, col, input value
        tmpInput_layerA.initializeRunPhase( [0,0,0,1] ); # choose majority logic (layerA, miss1, miss2, layerA)
        tmpInput_layerA.checkPattern( [2,0,0,0] ); # run mode, look for a single pattern
        #tmpInput_layerA.doRowChecker( 0 ); # cheat mode, look at a particular row
        tmpInput_layerA.close();
        tmpVisualizer_layerA = inputVisualizer( tmpInput_layerA.getFilename() );
        tmpVisualizer_layerA.writeToText( "testMajorityLogic/tmpInput_layerA.txt" );











