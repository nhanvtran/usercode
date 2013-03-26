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
#parser.add_option('--testA', action='store_true', dest='testA', default=False, help='run testA')
#parser.add_option('--testB', action='store_true', dest='testB', default=False, help='run testB')
#parser.add_option('--testC', action='store_true', dest='testC', default=False, help='run testC')
#parser.add_option('--testD', action='store_true', dest='testD', default=False, help='run testD')

(options, args) = parser.parse_args()
############################################


# =================================================
# ===>   m a i n
# =================================================
if __name__ == '__main__':

    if not os.path.isdir("test_v2"): os.system("mkdir test_v2");
    
    # -------------------------------------------------
    # Power Test - every row/col matches
    testA = inputBuilder("test_v2/testA.root");
    testA.initializeLoadPhase();
    for i in range(128):
        for j in range(32):
            testA.loadUniformPatterns(i, j, 8); # fill every row and col with [8,8,8,8]                
    testA.initializeRunPhase( [1,0,0,0] ); # choose majority logic 'miss0' ONLY
    testA.checkPattern( [8,8,8,8] ); # run mode, look for a single pattern [8,8,8,8]
    testA.readOutMode(); # keep same logic 'miss0' when reading out
    testA.close();
    visuA = inputVisualizer( testA.getFilename() );
    visuA.writeToText( "test_v2/testA.txt" ); # write outputs to test_v2/testA.txt

    # -------------------------------------------------
    # Comprehensive test: testing majority logic, disable bit (in both load and run mode)
    testB = inputBuilder("test_v2/testB.root");
    
    #### load phase
    testB.initializeLoadPhase();
    ctr = 0;
    for i in range(0,1):
        for j in range(32):
            testB.loadSinglePattern(i, j, [ctr,ctr,ctr,ctr], 0); # disable row 1
            ctr += 1;
    for i in range(1,32):
        for j in range(32):
            testB.loadSinglePattern(i, j, [ctr,ctr,ctr,ctr]);    # row 2-32, fill with '[ctr,ctr,ctr,ctr]'
            ctr += 1;
    for i in range(32,64):
        for j in range(32):
            testB.loadSinglePattern(i, j, [ctr,9999,ctr,ctr]);   # row 33-64, fill with '[ctr,9999,ctr,ctr]'
            ctr += 1;
    for i in range(64,96):
        for j in range(32):
            testB.loadSinglePattern(i, j, [ctr,9999,9999,ctr]);  # row 65-96, fill with '[ctr,9999,9999,ctr]'
            ctr += 1;
    for i in range(96,128):
        for j in range(32):
            testB.loadSinglePattern(i, j, [ctr,9999,9999,9999]); # row 97-128, fill with '[ctr,9999,9999,9999]'
            ctr += 1;

    #### run phase
    testB.initializeRunPhase();
    ctr = 0;
    for i in range(0,1):
        for j in range(32):
            testB.checkPattern( [ctr,ctr,ctr,ctr] );        # check for what would have been in row 1
            ctr += 1;
    for i in range(1,32):
        for j in range(32):
            if j % 2 == 0: testB.checkPattern([ctr,ctr,ctr,ctr]);       # check what is in row 2-32, '[ctr,ctr,ctr,ctr]'
            if j % 2 == 1: testB.checkPattern([ctr,8888,ctr,ctr]);      # check what is in row 2-32, '[ctr,8888,ctr,ctr]'
            ctr += 1;
    for i in range(32,64):
        for j in range(32):
            if j % 2 == 0: testB.checkPattern([ctr,8888,ctr,ctr]);      # check what is in row 33-64, '[ctr,ctr,ctr,ctr]'
            if j % 2 == 1: testB.checkPattern([ctr,8888,8888,ctr]);     # check what is in row 33-64, '[ctr,8888,ctr,ctr]'
            ctr += 1;
    for i in range(64,96):
        for j in range(32): 
            if j % 2 == 0: testB.checkPattern([ctr,-1,-1,ctr]);         # check what is in row 65-96, '[ctr,ctr,ctr,ctr]', testing the disable input during run mode functionality
            if j % 2 == 1: testB.checkPattern([ctr,-1,-1,-1]);          # check what is in row 65-96, '[ctr,8888,ctr,ctr]', testing the disable input during run mode functionality
            ctr += 1;
    for i in range(96,128):
        for j in range(32):
            if j % 2 == 0: testB.checkPattern([ctr,8888,8888,8888]);    # check what is in row 97-128, '[ctr,ctr,ctr,ctr]'
            if j % 2 == 1: testB.checkPattern([8888,8888,8888,8888]);   # check what is in row 97-128, '[ctr,8888,ctr,ctr]'
            ctr += 1;

    #### read out mode
    testB.readOutMode( [1,0,0,0] ); # read out only miss0 logics
    testB.readOutMode( [0,1,0,0] ); # read out only miss1 logics
    testB.readOutMode( [0,0,1,0] ); # read out only miss2 logics
    testB.readOutMode( [0,0,0,1] ); # read out only layerA logics
    testB.readOutMode( [1,1,1,0] ); # read out only miss0,miss1,miss2 logics

    testB.close();
    visuB = inputVisualizer( testB.getFilename() );
    visuB.writeToText( "test_v2/testB.txt" ); # write outputs to test_v2/testB.txt


    # -------------------------------------------------
    # Realistic test (10 events), one load mode, 10 run modes with event reset in middle
    testC = inputBuilder("test_v2/testC.root");

    #### load phase
    testC.initializeLoadPhase();
    for i in range(128):
        for j in range(32):
            if j % 2 == 0: testC.loadSinglePattern(i, j, [8,8,8,8]); # fill even cols with [8,8,8,8]                
            if j % 2 == 1: testC.loadSinglePattern(i, j, [5,5,5,5]); # fill odd cols with [5,5,5,5]                

    #### run/readout phase
    for event in range(10):
        testC.initializeRunPhase();
        testC.checkPattern([event,event,event,event]); # should only find something on the 6th and 9th event
        testC.readOutMode( [1,0,0,0] ); # read out only miss0 logics

    testC.close();
    visuC = inputVisualizer( testC.getFilename() );
    visuC.writeToText( "test_v2/testC.txt" ); # write outputs to test_v2/testC.txt




