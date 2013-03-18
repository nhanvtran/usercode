#! /usr/bin/env python
import ROOT

from pVIPRAM_inputBuilderClass import *
from pVIPRAM_inputVisualizerClass import *

ROOT.gStyle.SetPalette(1);

if __name__ == '__main__':

    test1 = inputBuilder("testInputs/test1.root")

    test1.initializeLoadPhase();
    test1.loadUniformPatterns(0,0,2);
    test1.initializeRunPhase( [1,0,0,0] );
    test1.checkPattern( [2,2,2,2] );
    test1.close();

    visualizer1 = inputVisualizer( test1.getFilename() );
    visualizer1.textVisualizer();
    visualizer1.visualize("test.eps");
    visualizer1.writeToText();