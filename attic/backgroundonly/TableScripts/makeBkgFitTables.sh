#!/bin/bash


backgrounds="Top,WW,ZV,Zjets,Higgs,Fake"
zeroJet="../results/Super1c_all_SMCwslep0_NoSys/TopLvlXML_combined_NormalMeasurement_model_afterFit.root"
singleJet="../results/Super1a_all_SMCwslep0_NoSys/TopLvlXML_combined_NormalMeasurement_model_afterFit.root"


fitFile="TopLvlXML_combined_NormalMeasurement_model_afterFit.root"

zeroJetSR=(Super0a Super0b Super0c)
zeroJetCR=emCRTop14a,emCRWW14a,emCRZV14a

#oneJetSR=(Super1a Super1b Super1c)
oneJetSR=(Super1a Super1c)
oneJetCR=emCRTop14b,emCRWW14b,emCRZV14b

#for sr in ${zeroJetSR[@]}; do
#    YieldsTable.py -b -c ${zeroJetCR},ee${sr},mm${sr},em${sr} -s ${backgrounds} -w ../results/${sr}_all_SMCwslep0_NoSys/${fitFile} &&
#    mv *.tex bkgFitYields/ &&
#    mv *.pickle bkgFitYields/pickle/ &&
#    sleep 0.1s
#done
YieldsTable.py -b -c eeSuper1a -s "SMCwslep8TeV_112.5_12.5" -w /gdata/atlas/dantrim/SusyAna/SuperFitter/HistFitter/T0_HistFitter-00-00-29/results/Super1a_all_SMCwslep0_NoSys/TopLvlXML_Exclusion_SMCwslep8TeV_112.5_12.5_combined_NormalMeasurement_model.root
#for sr in ${oneJetSR[@]}; do
#    #YieldsTable.py -b -c ${oneJetCR},ee${sr},mm${sr},em${sr} -s ${backgrounds} -w ../results/${sr}_all_SMCwslep0_NoSys/${fitFile} &&
#    YieldsTable.py -b -c ${oneJetCR},sf${sr} -s ${backgrounds} -w ../results/${sr}_sf_SMCwslep0_NoSys/${fitFile} &&
#    mv *.tex bkgFitYields/ &&
#    mv *.pickle bkgFitYields/pickle/ &&
#    sleep 0.1s
#done


#YieldsTable.py -b -c emCRTop14b,emCRWW14b,emCRZV14b,eeSuper1c,mmSuper1c,emSuper1c -s $backgrounds -w $zeroJet 
##YieldsTable.py -b -c emCRWW14a  -s $backgrounds -w $zeroJet |tee   emCRWW14a_yld.log  &&
##YieldsTable.py -b -c emCRZV14a  -s $backgrounds -w $zeroJet |tee   emCRZV14a_yld.log  && 
##YieldsTable.py -b -c emCRTop14b -s $backgrounds -w $singleJet |tee emCRTop14b_yld.log &&
##YieldsTable.py -b -c emCRWW14b  -s $backgrounds -w $singleJet |tee emCRWW14b_yld.log  &&
##YieldsTable.py -b -c emCRZV14b  -s $backgrounds -w $singleJet |tee emCRZV14b_yld.log  &&
#mv *.tex CRYields/ &&
#mv *.pickle CRYields/pickle/ &&
#mv *.log CRYields/logs/



