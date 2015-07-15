# Dump Tables

region=${1}  # i.e. SR4a
channel=${2} # i.e. em
#runChannel=${3} # since we typicall run the first limits with "all" the results directory will have all as the channel 
grid="SMCwslep0"
sys="NoSys"

# First fit
HistFitter.py -twf -m all -D corrMatrix LimitScripts/LimitConfig.py ${region} ${channel} ${grid} ${sys} 2>&1 |tee FitLog_${region}_${channel}.txt;
# Dump yield table
#YieldsTable.py -b    -c ${channel}${region} -s Top,WW,ZV,Zjets,Higgs -w results/${region}_${runChannel}_${grid}_${sys}/TopLvlXML_combined_NormalMeasurement_model_afterFit.root -o ${region}_${grid}_${channel}_${sys}.tex;
# Before-fit Syst Table
#SysTable.py    -b -% -c ${channel}${region} -s Top,WW,ZV,Zjets,Higgs       -w results/${region}_${runChannel}_${grid}_${sys}/TopLvlXML_combined_NormalMeasurement_model_afterFit.root -o ${region}_${grid}_${channel}_${sys}_systBeforeFit.tex;
## After-fit Syst Table
#SysTable.py       -% -c ${channel}${region} -s Top,WW,ZV,Zjets,Higgs       -w results/${region}_${runChannel}_${grid}_${sys}/TopLvlXML_combined_NormalMeasurement_model_afterFit.root -o ${region}_${grid}_${channel}_${sys}_systAfterFit.tex;
