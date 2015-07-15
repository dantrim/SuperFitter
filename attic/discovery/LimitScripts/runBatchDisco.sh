#!/bin/bash


runGrid="SMCwslep0"
Channels=( sf ) #ee mm em )
#SignalRegions=( Super0a Super0b Super0c Super1a Super1b Super1c )
#SignalRegions=( Super1a Super1b Super1c )
SignalRegions=(Super1a Super1c)
Systematics=( NoSys ) # up down )
Slepton=NONE

for sr in ${SignalRegions[@]}; do
    for ch in ${Channels[@]}; do
        for sys in ${Systematics[@]}; do
            export SR=${sr}
            export Chan=${ch}
            export Sys=${sys}
            name=${sr}_${ch}_${grid}_${sys}_DiscoFit
            sbatch -J ${name} -o batchlog/${name}.out -e batchlog/${name}.err LimitScripts/batchDiscoSub.sh
            sleep 0.5s
        done
    done
done


echo "Finished Submitting"
echo


