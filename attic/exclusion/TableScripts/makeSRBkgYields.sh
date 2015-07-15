#!/bin/bash

backgrounds="Top,WW,ZV,Zjets,Higgs,Fake"

zeroJet_a="../results/Super0a_all_SMCwslep0_NoSys/TopLvlXML_combined_NormalMeasurement_model_afterFit.root"
zeroJet_b="../results/Super0b_all_SMCwslep0_NoSys/TopLvlXML_combined_NormalMeasurement_model_afterFit.root"
zeroJet_c="../results/Super0c_all_SMCwslep0_NoSys/TopLvlXML_combined_NormalMeasurement_model_afterFit.root"
zeroJet_d="../results/Super0d_all_SMCwslep0_NoSys/TopLvlXML_combined_NormalMeasurement_model_afterFit.root"
singleJet_a="../results/Super1a_all_SMCwslep0_NoSys/TopLvlXML_combined_NormalMeasurement_model_afterFit.root"
singleJet_b="../results/Super1b_all_SMCwslep0_NoSys/TopLvlXML_combined_NormalMeasurement_model_afterFit.root"
singleJet_c="../results/Super1c_all_SMCwslep0_NoSys/TopLvlXML_combined_NormalMeasurement_model_afterFit.root"

fitFile="TopLvlXML_combined_NormalMeasurement_model_afterFit.root"

signalRegions=(Super0a Super0b Super0c Super1a Super1b Super1c)
leptonChannels=(ee mm em)

for sr in ${signalRegions[@]}; do
    for ch in ${leptonChannels[@]}; do
        YieldsTable.py -b -c ${ch}${sr} -s ${backgrounds} -w ../results/${sr}_${ch}_SMCwslep0_NoSys/${fitFile} |tee ${ch}${sr}_bkgYld.log &&
        mv *tex SRBkgYields/ &&
        mv *.pickle SRBkgYields/pickle/ &&
        mv *.log SRBkgYields/logs/
        sleep 0.1s
    done
done





#YieldsTable.py -b -c eeSuper0a,mmSuper0a,emSuper0a -s $backgrounds -w $zeroJet_a |tee        SR0a_bkgYld.log && 
#YieldsTable.py -b -c eeSuper0b,mmSuper0b,emSuper0b -s $backgrounds -w $zeroJet_b |tee        SR0b_bkgYld.log &&
#YieldsTable.py -b -c eeSuper0c,mmSuper0c,emSuper0c -s $backgrounds -w $zeroJet_c |tee        SR0c_bkgYld.log &&
#YieldsTable.py -b -c eeSuper0d,mmSuper0d,emSuper0d -s $backgrounds -w $zeroJet_d |tee        SR0d_bkgYld.log &&
#YieldsTable.py -b -c eeSuper1a,mmSuper1a,emSuper1a -s $backgrounds -w $singleJet_a |tee      SR1a_bkgYld.log &&
#YieldsTable.py -b -c eeSuper1b,mmSuper1b,emSuper1b -s $backgrounds -w $singleJet_b |tee      SR1b_bkgYld.log &&
#YieldsTable.py -b -c eeSuper1c,mmSuper1c,emSuper1c -s $backgrounds -w $singleJet_c |tee      SR1c_bkgYld.log &&
##YieldsTable.py -b -c emSuper1c -s $backgrounds -w $singleJet_c |tee      eeSR1c_bkgYld.log &&
#mv *.tex SRBkgYields/ &&
#mv *.pickle SRBkgYields/pickle/ &&
#mv *.log SRBkgYields/logs/
