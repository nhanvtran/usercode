combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n emWWlvjj_unbin -m  1000 -d  wwlvj_BulkG_c0p2_M1000_em_10_00_unbin.txt  -t -1 
combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n emWWlvjj_unbin -m  1200 -d  wwlvj_BulkG_c0p2_M1200_em_10_00_unbin.txt  -t -1 
combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n emWWlvjj_unbin -m  1500 -d  wwlvj_BulkG_c0p2_M1500_em_10_00_unbin.txt  -t -1 
combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n emWWlvjj_unbin -m  1600 -d  wwlvj_BulkG_c0p2_M1600_em_10_00_unbin.txt  -t -1 

hadd -f higgisCombin_em_unbin.root higgsCombineemWWlvjj_unbin.Asymptotic.mH1000.root  higgsCombineemWWlvjj_unbin.Asymptotic.mH1200.root  higgsCombineemWWlvjj_unbin.Asymptotic.mH1500.root  higgsCombineemWWlvjj_unbin.Asymptotic.mH1600.root
root -b ../../DrawLimit.C\(\"em\",\"unbin\"\) -q
