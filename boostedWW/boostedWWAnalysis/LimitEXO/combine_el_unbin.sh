combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n elWWlvjj_unbin -m  1000 -d  wwlvj_BulkG_c0p2_M1000_el_10_00_unbin.txt  -t -1 
combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n elWWlvjj_unbin -m  1200 -d  wwlvj_BulkG_c0p2_M1200_el_10_00_unbin.txt  -t -1 
combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n elWWlvjj_unbin -m  1500 -d  wwlvj_BulkG_c0p2_M1500_el_10_00_unbin.txt  -t -1 
combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -n elWWlvjj_unbin -m  1600 -d  wwlvj_BulkG_c0p2_M1600_el_10_00_unbin.txt  -t -1 

hadd -f higgisCombin_el_unbin.root higgsCombineelWWlvjj_unbin.Asymptotic.mH1000.root  higgsCombineelWWlvjj_unbin.Asymptotic.mH1200.root  higgsCombineelWWlvjj_unbin.Asymptotic.mH1500.root  higgsCombineelWWlvjj_unbin.Asymptotic.mH1600.root
root -b ../../DrawLimit.C\(\"el\",\"unbin\"\) -q
