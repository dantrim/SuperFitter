#!/usr/bin bash

echo "Checking out HistFitter-${1}"

export SVNPHYS="svn+ssh://${USER}@svn.cern.ch/reps/atlasphys-susy"
setup_script=setup_UCIT3.sh
dirname=HistFitter-${1}

if [ -d $dirname ];
then
    echo "Directory $dirname already exists!"
else
    echo "svn co $SVNPHYS/Physics/SUSY/Analyses/HistFitter/tags/HistFitter-${1} HistFitter-${1}"
    svn co $SVNPHYS/Physics/SUSY/Analyses/HistFitter/tags/HistFitter-${1} HistFitter-${1}

    if [ -f $setup_script ];
    then
        echo "cp $setup_script $dirname"
        cp $setup_script $dirname
    else
        echo "$setup_script does not exist in current directory."
    fi
fi
