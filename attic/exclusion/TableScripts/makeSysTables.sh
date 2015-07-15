#!/bin/bash

#SignalRegions=(Super0b Super0c Super0d Super1a Super1b) # Super1c is located in another HF directory
#SignalRegions=(Super1c) # Super1c is located in another HF directory
#channel=(ee) # mm em

#SignalRegions=(Super0a Super0b Super0c Super1a Super1b Super1c)
#SignalRegions=(Super1a Super1b Super1c)
SignalRegions=(Super1a Super1c)
#channel=(ee mm em)
#channel=(mm)
channel=(sf) # em)


#SignalRegions=(Super0c)
#channel=(ee mm)

SysTable.py -% -w ../results/Super1a_all_SMCwslep0_NoSys/TopLvlXML_Exclusion_SMCwslep8TeV_112.5_12.5_combined_NormalMeasurement_model.root -c "SMCwslep8TeV_112.5_12.5" -o blah.tex




#for sr in ${SignalRegions[@]}; do
#    for ch in ${channel[@]}; do
#        echo SysTable for ${ch}${sr} 
#        SysTable.py -% -w ../results/${sr}_sf_SMCwslep0_NoSys/TopLvlXML_combined_NormalMeasurement_model_afterFit.root -c ${ch}${sr} -s Top,WW,ZV -o sysTable_${ch}${sr}_afterFit.tex &&
#        mv *tex sysTables/
#        sleep 0.5s
#
#        
##        SysTable.py -% -w ../results/${sr}_all_SMCwslep0_NoSys/TopLvlXML_combined_NormalMeasurement_model_afterFit.root -c ${ch}${sr} -s WW,ZV,Higgs -o sysTable_${ch}${sr}_afterFit.tex > sysTable_${ch}${sr}.log & 
#    done
#done

