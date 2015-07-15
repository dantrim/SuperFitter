#!/bin/bash

###############################################################
# This script will setup the directory structure to use these #
# scripts as well as:                                         #
#    - Check out the specified HistFitter package             #
#    - Check out the plotting scripts to make final plots     #
#    - Compile and run all setup scripts                      #
###############################################################


#---------------------------#
# User specifications
#---------------------------#

# HF package tag you want
HFTag="HistFitter-00-00-29"

# The directory name you want
# to run limits from
#dirName="LimitTest1"
#dirName="LimitTest2"
#dirName="Pass1"
#dirName="Pass3"
dirName="SysPlots"

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
#                Don't Edit Below Here                    #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

#---------------------------#
# Make directory
#---------------------------#

echo "Making Directory"

# Save current Directory
currentDir=$PWD

# Move up one dir
cd ../
mkdir ${dirName}
cd ${dirName}

#---------------------------#
# Check out Histfitter
#---------------------------#

echo "Getting HistFitter package"

# Check out HF
svn co svn+ssh://svn.cern.ch/reps/atlasphys/Physics/SUSY/Analyses/HistFitter/tags/${HFTag} HistFitter
cd HistFitter

#---------------------------#
# Compile hist fitter
#---------------------------#

echo "Compiling HistFitter"

source setup.sh
cd src/
make
cd ../

#---------------------------#
# Checkout plotting script
#---------------------------#

echo "Getting plotting scripts"

svn co svn+ssh://svn.cern.ch/reps/atlasinst/Institutes/UCIrvine/mrelich/PlotScripts/trunk PlotScripts
cd PlotScripts/
source setup.sh
cd ../

#---------------------------#
# Move Original directory
#---------------------------#

echo "Copying over LimitScripts directory"

mv ${currentDir} .

echo "Done"