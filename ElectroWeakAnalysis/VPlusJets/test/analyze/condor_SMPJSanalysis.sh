#!/bin/bash

totalNumberOfFiles=27
startval=0

processNtuples="False"
buildHistos="True"
channel="1"

if [ "$processNtuples" == "True" ]; then
    c=$startval
    while ((c< ${totalNumberOfFiles}))
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

if [ "$buildHistos" == "True" ]; then
    c=$startval
    while ((c< ${totalNumberOfFiles}))
    do          
        options="-b -r -n $c -c $channel"
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
