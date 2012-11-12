nohup combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n HWWlvjj_unbin -m 600 -d hwwlvj_ggH600_datacard_unbin.txt --unbinned -S 0  >> rlt600.txt &
nohup combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n HWWlvjj_unbin -m 700 -d hwwlvj_ggH700_datacard_unbin.txt --unbinned -S 0   >> rlt700.txt &
nohup combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n HWWlvjj_unbin -m 800 -d hwwlvj_ggH800_datacard_unbin.txt --unbinned -S 0   >> rlt800.txt &
nohup combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n HWWlvjj_unbin -m 900 -d hwwlvj_ggH900_datacard_unbin.txt --unbinned -S 0   >> rlt900.txt &
nohup combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n HWWlvjj_unbin -m 1000 -d hwwlvj_ggH1000_datacard_unbin.txt --unbinned  -S 0  >> rlt1000.txt &

#hadd -f higgisCombin_unbin.root higgsCombineHWWlvjj_unbin.Asymptotic.mH600.root higgsCombineHWWlvjj_unbin.Asymptotic.mH700.root higgsCombineHWWlvjj_unbin.Asymptotic.mH800.root higgsCombineHWWlvjj_unbin.Asymptotic.mH900.root higgsCombineHWWlvjj_unbin.Asymptotic.mH1000.root
