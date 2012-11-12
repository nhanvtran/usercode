combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n HWWlvjj_counting -m  600 -d  hwwlvj_ggH600_datacard_counting.txt   -S 0 
combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n HWWlvjj_counting -m  700 -d  hwwlvj_ggH700_datacard_counting.txt   -S 0
combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n HWWlvjj_counting -m  800 -d  hwwlvj_ggH800_datacard_counting.txt   -S 0
combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n HWWlvjj_counting -m  900 -d  hwwlvj_ggH900_datacard_counting.txt   -S 0
combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n HWWlvjj_counting -m 1000 -d hwwlvj_ggH1000_datacard_counting.txt   -S 0 

hadd -f higgisCombin_counting.root higgsCombineHWWlvjj_counting.Asymptotic.mH600.root  higgsCombineHWWlvjj_counting.Asymptotic.mH700.root  higgsCombineHWWlvjj_counting.Asymptotic.mH800.root  higgsCombineHWWlvjj_counting.Asymptotic.mH900.root  higgsCombineHWWlvjj_counting.Asymptotic.mH1000.root
