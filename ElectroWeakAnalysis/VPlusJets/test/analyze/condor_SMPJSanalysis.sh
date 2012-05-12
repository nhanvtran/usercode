#!/bin/bash

totalNumberOfFiles=66
startval=0

processNtuples="True"
buildHistos="False"
channel="4"

if [ "$processNtuples" == "True" ]; then
    c=$startval
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

if [ "$buildHistos" == "True" ]; then
    c=$startval
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
