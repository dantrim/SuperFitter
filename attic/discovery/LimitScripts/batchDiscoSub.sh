#!/bin/bash

#SBATCH -p atlas_all
#SBATCH --exclude=c-12-15,c-12-19
##SBATCH --distribution=cyclic
#SBATCH -N 1 -n 1
#SBATCH --mem-per-cpu=1gb
#SBATCH --time=8:00:00

# cd to working directory
cd /gdata/atlas/dantrim/SusyAna/SuperFitter/HistFitter/T2_HistFitter-00-00-29/

# setup ROOT
source setup_UCIT3.sh

source setup.sh


HistFitter.py -twfz LimitScripts/LimitConfig.py ${SR} ${Chan} SMCwslep0 ${Sys} > batchLog/${SR}_${Chan}_SMCwslep0_${Sys}.log
