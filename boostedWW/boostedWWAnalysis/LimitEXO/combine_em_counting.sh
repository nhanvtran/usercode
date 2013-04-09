combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n emWWlvjj_counting -m  1000 -d  wwlvj_BulkG_c0p2_M1000_em_10_00_counting.txt  -t -1 
combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n emWWlvjj_counting -m  1200 -d  wwlvj_BulkG_c0p2_M1200_em_10_00_counting.txt  -t -1 
combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n emWWlvjj_counting -m  1500 -d  wwlvj_BulkG_c0p2_M1500_em_10_00_counting.txt  -t -1 
combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n emWWlvjj_counting -m  1600 -d  wwlvj_BulkG_c0p2_M1600_em_10_00_counting.txt  -t -1 

hadd -f higgisCombin_em_counting.root higgsCombineemWWlvjj_counting.Asymptotic.mH1000.root  higgsCombineemWWlvjj_counting.Asymptotic.mH1200.root  higgsCombineemWWlvjj_counting.Asymptotic.mH1500.root  higgsCombineemWWlvjj_counting.Asymptotic.mH1600.root
root -b ../../DrawLimit.C\(\"em\",\"counting\"\) -q
