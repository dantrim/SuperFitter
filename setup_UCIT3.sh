
# Setup ROOT
ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh --quiet
source ${ATLAS_LOCAL_ROOT_BASE}/packageSetups/atlasLocalROOTSetup.sh --skipConfirm --rootVersion=6.04.02-x86_64-slc6-gcc48-opt

# Setup HistFitter package
export HF=$PWD
export HISTFITTER=$PWD
export SUSYFITTER=$PWD # for backwards compatibility

# Put ROOT & Python stuff into PATH, LD_LIBRARY_PATH
export PATH=$HISTFITTER/bin:$HISTFITTER/scripts:${PATH}
export LD_LIBRARY_PATH=$HISTFITTER/lib:${LD_LIBRARY_PATH}
# PYTHONPATH contains all directories that are used for 'import bla' commands
export PYTHONPATH=$HISTFITTER/python:$HISTFITTER/scripts:$HISTFITTER/macros:$HISTFITTER/lib:$PYTHONPATH

# set SVN path to defaults
export SVNTEST="svn+ssh://svn.cern.ch/reps/atlastest"
export SVNROOT="svn+ssh://svn.cern.ch/reps/atlasoff"
export SVNPHYS="svn+ssh://svn.cern.ch/reps/atlasphys"

# Hack for ssh from mac 
export LC_ALL=C 




#### original script
## Setup ROOT
#ATLAS_LOCAL_ROOT_BASE=/export/home/atlasadmin/ATLASLocalRootBase
#source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh --quiet
#source ${ATLAS_LOCAL_ROOT_BASE}/packageSetups/atlasLocalROOTSetup.sh --skipConfirm --rootVersion=5.34.14-x86_64-slc5-gcc4.3
#
## Setup HistFitter package
#export HF=$PWD
#export HISTFITTER=$PWD
#export SUSYFITTER=$PWD # for backwards compatibility
#
## Put ROOT & Python stuff into PATH, LD_LIBRARY_PATH
#export PATH=$HISTFITTER/bin:$HISTFITTER/scripts:${PATH}
#export LD_LIBRARY_PATH=$HISTFITTER/lib:${LD_LIBRARY_PATH}
## PYTHONPATH contains all directories that are used for 'import bla' commands
#export PYTHONPATH=$HISTFITTER/python:$HISTFITTER/scripts:$HISTFITTER/macros:$HISTFITTER/lib:$PYTHONPATH
#
## set SVN path to defaults
#export SVNTEST="svn+ssh://svn.cern.ch/reps/atlastest"
#export SVNROOT="svn+ssh://svn.cern.ch/reps/atlasoff"
#export SVNPHYS="svn+ssh://svn.cern.ch/reps/atlasphys"
#
## Hack for ssh from mac 
#export LC_ALL=C 
