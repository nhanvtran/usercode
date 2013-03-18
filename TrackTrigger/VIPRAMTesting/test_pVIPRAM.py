#! /usr/bin/env python
import ROOT

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
        nRows = 128;
        nColumns = 32;
        for i in range(nRows):
            for j in range(nColumns):
                tmpInput = inputBuilder("testInputSingle/testSingle_%03d_%03d.root"%(i,j));
                tmpInput.initializeLoadPhase();
                tmpInput.loadUniformPatterns(0, 0, 8); # row, col, input value
                tmpInput.initializeRunPhase( [1,0,0,0] ); # choose majority logic (miss0, miss1, miss2, layerA)
                tmpInput.checkPattern( [8,8,8,8] ); # run mode, look for a single pattern
                tmpInput.doRowChecker( i ); # cheat mode, look at a particular row
                tmpInput.close();

                tmpVisualizer = inputVisualizer( tmpInput.getFilename() );
                #tmpVisualizer.textVisualizer();
                #tmpVisualizer.visualize("test.eps");
                tmpVisualizer.writeToText( "testInputSingle/testSingle_%03d_%03d.txt"%(i,j) );

    # -------------------------------------------------    
    # testing disable road
    if options.testB:
        tmpInput_disabled = inputBuilder( "testDisableBit/testDisableBit.root" );
        tmpInput_disabled.initializeLoadPhase();
        tmpInput_disabled.loadUniformPatterns(0, 0, 2, 0); # row, col, input value, disable road
        tmpInput_disabled.initializeRunPhase( [1,0,0,0] ); # choose majority logic (miss0, miss1, miss2, layerA)
        tmpInput_disabled.checkPattern( [2,2,2,2] ); # run mode, look for a single pattern
        tmpInput_disabled.doRowChecker( 0 ); # cheat mode, look at a particular row
        tmpInput_disabled.close();
            
        tmpVisualizer_disabled = inputVisualizer( tmpInput_disabled.getFilename() );
        tmpVisualizer_disabled.writeToText( "testDisableBit/testDisableBit.txt" );
    
    # -------------------------------------------------    
    # testing walking
    if options.testC:
        nRows = 128;
        nColumns = 32;
        tmpWalking = inputBuilder( "testWalking/testWalking.root" );
        tmpWalking.initializeLoadPhase();
        print "Loading..."
        for i in range(nRows):
            print "row: ",i
            for j in range(nColumns):
                tmpWalking.loadUniformPatterns(i, j, i+j); # row, col, input value, disable road
        tmpWalking.initializeRunPhase( [1,0,0,0] ); # choose majority logic (miss0, miss1, miss2, layerA)
        print "Running..."
        for i in range(nRows):
            print "row: ",i
            for j in range(nColumns):
                tmpWalking.checkPattern( [i+j,i+j,i+j,i+j] ); # run mode, look for a single pattern
        print "Cheating..."
        for i in range(nRows):
            print "row: ",i
            for j in range(nColumns):
                tmpWalking.doRowChecker( 0 ); # cheat mode, look at a particular row
        tmpWalking.close();
            
        tmpWalkingVisualizer = inputVisualizer( tmpWalking.getFilename() );
        tmpWalkingVisualizer.writeToText( "testWalking/testWalking.txt" );

    # -------------------------------------------------    
    # testing majority logic
    if options.testD:
        tmpInput_miss0 = inputBuilder( "testMajorityLogic/tmpInput_miss0.root" );
        tmpInput_miss0.initializeLoadPhase();
        tmpInput_miss0.loadSinglePattern(0, 0, [2,2,2,2]); # row, col, input value
        tmpInput_miss0.initializeRunPhase( [1,0,0,0] ); # choose majority logic (miss0, miss1, miss2, layerA)
        tmpInput_miss0.checkPattern( [2,2,2,2] ); # run mode, look for a single pattern
        tmpInput_miss0.doRowChecker( 0 ); # cheat mode, look at a particular row
        tmpInput_miss0.close();
        tmpVisualizer_miss0 = inputVisualizer( tmpInput_miss0.getFilename() );
        tmpVisualizer_miss0.writeToText( "testMajorityLogic/tmpInput_miss0.txt" );

        tmpInput_miss1 = inputBuilder( "testMajorityLogic/tmpInput_miss1.root" );
        tmpInput_miss1.initializeLoadPhase();
        tmpInput_miss1.loadSinglePattern(0, 0, [2,99,2,2]); # row, col, input value
        tmpInput_miss1.initializeRunPhase( [0,1,0,0] ); # choose majority logic (miss1, miss1, miss2, layerA)
        tmpInput_miss1.checkPattern( [2,0,2,2] ); # run mode, look for a single pattern
        tmpInput_miss1.doRowChecker( 0 ); # cheat mode, look at a particular row
        tmpInput_miss1.close();
        tmpVisualizer_miss1 = inputVisualizer( tmpInput_miss1.getFilename() );
        tmpVisualizer_miss1.writeToText( "testMajorityLogic/tmpInput_miss1.txt" );

        tmpInput_miss2 = inputBuilder( "testMajorityLogic/tmpInput_miss2.root" );
        tmpInput_miss2.initializeLoadPhase();
        tmpInput_miss2.loadSinglePattern(0, 0, [2,99,99,2]); # row, col, input value
        tmpInput_miss2.initializeRunPhase( [0,0,1,0] ); # choose majority logic (miss2, miss1, miss2, layerA)
        tmpInput_miss2.checkPattern( [2,0,0,2] ); # run mode, look for a single pattern
        tmpInput_miss2.doRowChecker( 0 ); # cheat mode, look at a particular row
        tmpInput_miss2.close();
        tmpVisualizer_miss2 = inputVisualizer( tmpInput_miss2.getFilename() );
        tmpVisualizer_miss2.writeToText( "testMajorityLogic/tmpInput_miss2.txt" );

        tmpInput_layerA = inputBuilder( "testMajorityLogic/tmpInput_layerA.root" );
        tmpInput_layerA.initializeLoadPhase();
        tmpInput_layerA.loadSinglePattern(0, 0, [2,99,99,99]); # row, col, input value
        tmpInput_layerA.initializeRunPhase( [0,0,0,1] ); # choose majority logic (layerA, miss1, miss2, layerA)
        tmpInput_layerA.checkPattern( [2,0,0,0] ); # run mode, look for a single pattern
        tmpInput_layerA.doRowChecker( 0 ); # cheat mode, look at a particular row
        tmpInput_layerA.close();
        tmpVisualizer_layerA = inputVisualizer( tmpInput_layerA.getFilename() );
        tmpVisualizer_layerA.writeToText( "testMajorityLogic/tmpInput_layerA.txt" );











