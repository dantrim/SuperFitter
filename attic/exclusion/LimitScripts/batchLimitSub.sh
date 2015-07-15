#!/bin/bash

#SBATCH -p atlas_slow
##SBATCH --exclude=c-12-35,c-12-31,c-12-39,c-12-15,c-12-19,c-12-23
#SBATCH --distribution=cyclic
#SBATCH -N 1 -n 1
#SBATCH --mem-per-cpu=1gb
#SBATCH --time=12:00:00

# cd to working directory
#cd $PBS_O_WORKDIR
#cd /home/amete/ReinterpretationLimits2014/HistFitter-00-00-39/
cd /gdata/atlas/dantrim/SusyAna/SuperFitter/HistFitter/T0_HistFitter-00-00-29/

# Setup ROOT
source setup_UCIT3.sh

# run setup script for limits so knows
# where to find HistFitter.py
source setup.sh

#run job
HistFitter.py -twfp LimitScripts/LimitConfig.py ${SR} ${Chan} ${Grid} ${Sys} ${SlepOpt} > batchLog/${SR}_${Chan}_${Grid}_${Sys}_${SlepOpt}.log  &&
HistFitter.py -fl LimitScripts/LimitConfig.py ${SR} ${Chan} ${Grid} ${Sys} ${SlepOpt} > batchLog/${SR}_${Chan}_${Grid}_${Sys}_${SlepOpt}_limitOnMu.log
