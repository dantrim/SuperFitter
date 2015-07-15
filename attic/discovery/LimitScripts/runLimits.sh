#!/bin/bash


# Just a script to submit jobs for SRmT2 regions

HistFitter.py -twfp -d -i LimitScripts/LimitConfig.py Super0b all SMCwslep NoSys
#nohup HistFitter.py -twfp LimitScripts/LimitConfig.py SR4b all SMCwslep NoSys > SR4b_all.out &
#nohup HistFitter.py -twfp LimitScripts/LimitConfig.py SR4c all SMCwslep NoSys > SR4c_all.out &

# Sys Up
#nohup HistFitter.py -twfp LimitScripts/LimitConfig.py SR4a ee SMCwslep up > SR4a_ee_up.out &
#nohup HistFitter.py -twfp LimitScripts/LimitConfig.py SR4b all SMCwslep up > SR4b_all_up.out &
#nohup HistFitter.py -twfp LimitScripts/LimitConfig.py SR4c all SMCwslep up > SR4c_all_up.out &

# Sys Down
#nohup HistFitter.py -twfp LimitScripts/LimitConfig.py SR4a ee SMCwslep down > SR4a_ee_down.out &
#nohup HistFitter.py -twfp LimitScripts/LimitConfig.py SR4b all SMCwslep down > SR4b_all_down.out &
#nohup HistFitter.py -twfp LimitScripts/LimitConfig.py SR4c all SMCwslep down > SR4c_all_down.out &
