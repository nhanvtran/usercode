combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n elWWlvjj_counting -m  1000 -d  wwlvj_BulkG_c0p2_M1000_el_10_00_counting.txt  -t -1 
combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n elWWlvjj_counting -m  1200 -d  wwlvj_BulkG_c0p2_M1200_el_10_00_counting.txt  -t -1 
combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n elWWlvjj_counting -m  1500 -d  wwlvj_BulkG_c0p2_M1500_el_10_00_counting.txt  -t -1 
combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n elWWlvjj_counting -m  1600 -d  wwlvj_BulkG_c0p2_M1600_el_10_00_counting.txt  -t -1 

hadd -f higgisCombin_el_counting.root higgsCombineelWWlvjj_counting.Asymptotic.mH1000.root  higgsCombineelWWlvjj_counting.Asymptotic.mH1200.root  higgsCombineelWWlvjj_counting.Asymptotic.mH1500.root  higgsCombineelWWlvjj_counting.Asymptotic.mH1600.root
root -b ../../DrawLimit.C\(\"el\",\"counting\"\) -q
