#!/bin/bash

#SignalRegions=( Super0a Super0b Super0c Super1a Super1b Super1c )
#SignalRegions=( Super1a Super1b Super1c )
SignalRegions=(Super1a Super1c)
#Channels=( ee mm em )
Channels=(sf)

tablePath=/gdata/atlas/dantrim/SusyAna/SuperFitter/HistFitter/T2_HistFitter-00-00-29/TableScripts/
cd tablePath
date='May19'

for sr in ${SignalRegions[@]}; do
    for ch in ${Channels[@]}; do
        echo UpperLimitTable for ${ch}${sr}
        chanPath=${tablePath}UpperLimit/${date}/${sr}/${ch}/
        mkdir -p ${chanPath}
        cd ${chanPath}
        nohup UpperLimitTable.py -c ${ch}${sr} -w /gdata/atlas/dantrim/SusyAna/SuperFitter/HistFitter/T2_HistFitter-00-00-29/results/${sr}_${ch}_SMCwslep0_NoSys/TopLvlXML_combined_NormalMeasurement_model.root -l 20.3 -p mu_SIG -a -o ${sr}_${ch}_upperlimit.tex > UL_${ch}${sr}.log &
        sleep 0.5s
       # mv UL_${ch}${sr}.log UpperLimit/${sr}/logs/  &&
       # mv ${sr}_${ch}_upperlimit.tex UpperLimit/${sr}/
        cd ${tablePath}
    done
done

