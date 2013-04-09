combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n muWWlvjj_counting -m  1000 -d  wwlvj_BulkG_c0p2_M1000_mu_10_00_counting.txt  -t -1 
combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n muWWlvjj_counting -m  1200 -d  wwlvj_BulkG_c0p2_M1200_mu_10_00_counting.txt  -t -1 
combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n muWWlvjj_counting -m  1500 -d  wwlvj_BulkG_c0p2_M1500_mu_10_00_counting.txt  -t -1 
combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n muWWlvjj_counting -m  1600 -d  wwlvj_BulkG_c0p2_M1600_mu_10_00_counting.txt  -t -1 

hadd -f higgisCombin_mu_counting.root higgsCombinemuWWlvjj_counting.Asymptotic.mH1000.root  higgsCombinemuWWlvjj_counting.Asymptotic.mH1200.root  higgsCombinemuWWlvjj_counting.Asymptotic.mH1500.root  higgsCombinemuWWlvjj_counting.Asymptotic.mH1600.root
root -b ../../DrawLimit.C\(\"mu\",\"counting\"\) -q
