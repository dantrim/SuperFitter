#!/bin/bash


############################################
#               RUN OPTIONS                #
############################################

# Specify which Grid
# Options are:
#   * ModeCwslep
#   * Sleptons
#   * SleptonsRH
#   * SleptonsLH
#   * SleptonsALL

runGrid="ModeCwslep"
#runGrid="Sleptons"
#runGrid="SleptonsRH"
#runGrid="SleptonsLH"
#runGrid="ModeCwslepVariableAll"
#runGrid="ModeCwslepVariable005"
#runGrid="ModeCwslepVariable025"
#runGrid="ModeCwslepVariable075"
#runGrid="ModeCwslepVariable095"
Channels=(all)
#Channels=(all ee mm)
#Channels=(all ee mm)
#SignalRegions=(SR4a SR4b SR4c)
SignalRegions=(Super0a Super0b Super0c Super1a Super1b Super1c)
#SignalRegions=(Super1a Super1b Super1c)
#SignalRegions=(Super0a Super0b Super0c Super0d)
Systematics=(NoSys up down)

############################################
#         Below will submit jobs           #
############################################

# Mode C points to run over
if [ $runGrid == "ModeCwslep" ]
    then
    Grids=(
	SMCwslep0 
	SMCwslep1 
	SMCwslep2 
	SMCwslep3 
	SMCwslep4
    )
	
    SleptonOption=(NONE)
fi

# Varible Mode C

# 5%
if [ $runGrid == "ModeCwslepVariable005" ]
    then
    Grids=(
        SMCVarwslep005
    )

    SleptonOption=(NONE)
fi

# 25%
if [ $runGrid == "ModeCwslepVariable025" ]
    then
    Grids=(
        SMCVarwslep025
    )

    SleptonOption=(NONE)
fi

# 75%
if [ $runGrid == "ModeCwslepVariable075" ]
    then
    Grids=(
        SMCVarwslep075
    )

    SleptonOption=(NONE)
fi

# 95%
if [ $runGrid == "ModeCwslepVariable095" ]
    then
    Grids=(
        SMCVarwslep095
    )

    SleptonOption=(NONE)
fi

# All Variable
if [ $runGrid == "ModeCwslepVariableAll" ]
    then
    Grids=(
        SMCVarwslep005
        SMCVarwslep025
        SMCVarwslep075
        SMCVarwslep095
    )

    SleptonOption=(NONE)
fi

# Slepton Grid RH+LH
if [ $runGrid == "Sleptons" ]
    then
    Grids=(
	SparseDLiSlep0
	SparseDLiSlep1
	SparseDLiSlep2
	SparseDLiSlep3
	SparseDLiSlep4
	SparseDLiSlep5
	SparseDLiSlep6
	SparseDLiSlep7
	SparseDLiSlep8
	SparseDLiSlep9
	SparseDLiSlep10
	SparseDLiSlep11
	SparseDLiSlep12
	SparseDLiSlep13
    )
    SleptonOption=(RandL)
fi

# Slepton Grid RH
if [ $runGrid == "SleptonsRH" ]
    then
    Grids=(
	SparseDLiSlep0
	SparseDLiSlep1
	SparseDLiSlep2
	SparseDLiSlep3
	SparseDLiSlep4
	SparseDLiSlep5
	SparseDLiSlep6
	SparseDLiSlep7
	SparseDLiSlep8
	SparseDLiSlep9
	SparseDLiSlep10
	SparseDLiSlep11
	SparseDLiSlep12
	SparseDLiSlep13
    )
    SleptonOption=(ROnly)
fi

# Slepton Grid LH
if [ $runGrid == "SleptonsLH" ]
    then
    Grids=(
	SparseDLiSlep0
	SparseDLiSlep1
	SparseDLiSlep2
	SparseDLiSlep3
	SparseDLiSlep4
	SparseDLiSlep5
	SparseDLiSlep6
	SparseDLiSlep7
	SparseDLiSlep8
	SparseDLiSlep9
	SparseDLiSlep10
	SparseDLiSlep11
	SparseDLiSlep12
	SparseDLiSlep13
    )
    SleptonOption=(LOnly)
fi

# Slepton Grid LH
if [ $runGrid == "SleptonsALL" ]
    then
    Grids=(
	SparseDLiSlep0
	SparseDLiSlep1
	SparseDLiSlep2
	SparseDLiSlep3
	SparseDLiSlep4
	SparseDLiSlep5
	SparseDLiSlep6
	SparseDLiSlep7
	SparseDLiSlep8
	SparseDLiSlep9
	SparseDLiSlep10
	SparseDLiSlep11
	SparseDLiSlep12
	SparseDLiSlep13
    )
    SleptonOption=(RandL ROnly LOnly)
fi

for sr in ${SignalRegions[@]}; do
    for ch in ${Channels[@]}; do
	for grid in ${Grids[@]}; do
	    for sys in ${Systematics[@]}; do
		for slepOpt in ${SleptonOption[@]}; do

		    name=${sr}_${ch}_${grid}_${sys}_${slepOpt}

		    #qsub -j oe -V -v SR=${sr},Chan=${ch},Grid=${grid},Sys=${sys},SlepOpt=${slepOpt} -N ${name} -o batchlog LimitScripts/batchLimitSub.sh
		    export SR=${sr}
		    export Chan=${ch}
		    export Grid=${grid}
		    export Sys=${sys}
		    export SlepOpt=${slepOpt}
                    sbatch -J ${name} -o batchlog/${name}.out -e batchlog/${name}.err LimitScripts/batchLimitSub.sh
		    sleep 0.5s
		done
	    done
	done
    done
done


echo "Finished Submitting"
echo

