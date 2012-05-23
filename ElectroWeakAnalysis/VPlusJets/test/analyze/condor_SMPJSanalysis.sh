#!/bin/bash

###### job steering
RUN=0; if [[ "$1" == "-r" ]]; then RUN=1; shift; fi;
PLOT=0; CHAN=0; if [[ "$1" == "-m" ]]; then PLOT=1; CHAN="$2"; shift; shift; fi;

echo $RUN, $PLOT, $CHAN

#totalNumberOfFiles=96
#startval=0
totalNumberOfFiles=15
startval=11

processNtuples=$RUN
buildHistos=$PLOT
channel=$CHAN

echo $processNtuples, $buildHistos, $channel


if [ $processNtuples == 1 ]; then
    c=$startval
    echo "Processing Ntuples..."
    while ((c < ${totalNumberOfFiles}))
    do      
        options="-b -r -n $c"
        location=`pwd`
        echo $options
        echo $location
        sed -e "s|OPTIONS|${options}|g" -e "s|LOCATION|${location}|g" < condor_scriptTpl.sh > condor_tmp_$c.sh
        echo $c
        sed -e "s|INDEX|${c}|g" < condor_submit > condor_submit_$c
        condor_submit condor_submit_$c
        let c=$c+1
    done
fi

if [ $buildHistos == 1 ]; then
    c=$startval
    echo "Building histograms ... channel $CHAN ..."
    while ((c < ${totalNumberOfFiles}))
    do          
        options="-b -m -n $c -c $channel"
        location=`pwd`
        echo $options
        echo $location
        sed -e "s|OPTIONS|${options}|g" -e "s|LOCATION|${location}|g" < condor_scriptTpl.sh > condor_tmp2_${c}_ch${channel}.sh
        echo "condor_tmp2_${c}_ch${channel}.sh"
        echo $c
        sed -e "s|INDEX|${c}|g" -e "s|CHANNEL|${channel}|g" < condor_submit2 > condor_submit_2_${c}_ch${channel}
        condor_submit condor_submit_2_${c}_ch${channel}
        let c=$c+1
    done
fi
