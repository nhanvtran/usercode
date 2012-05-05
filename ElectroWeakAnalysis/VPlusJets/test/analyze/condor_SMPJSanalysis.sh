#!/bin/bash

totalNumberOfFiles=1

processNtuples="True"
buildHistos="False"

if [ "$processNtuples" == "True" ]; then
    c=0
    while ((c< ${totalNumberOfFiles}))
    do      
        options="-b -r -n $c"
        location=`pwd`
        echo $options
        echo $location
        sed -e "s|OPTIONS|${options}|g" -e "s|LOCATION|${options}|g" < condor_scriptTpl.sh > condor_tmp_$c.sh
        echo $c
        sed -e "s|INDEX|${c}|g" < condor_submit > condor_submit_$c
        condor_submit condor_submit_$c
        let c=$c+1
    done
fi

if [ "$buildHistos" == "True" ]; then
    c=0
    while ((c< ${totalNumberOfFiles}))
    do          
        options="-b -r -n $c"
        location=`pwd`
        echo $options
        echo $location
        sed -e "s|OPTIONS|${options}|g" -e "s|LOCATION|${options}|g" < condor_scriptTpl.sh > condor_tmp_$c.sh
        echo $c
        sed -e "s|INDEX|${c}|g" < condor_submit > condor_submit_$c
        condor_submit condor_submit_$c
        let c=$c+1
    done
fi
