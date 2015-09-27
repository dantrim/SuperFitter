#!/usr/bin python

##############################################
## Container module for building the SR/CR/VR
## region lists
##############################################
import sys

def userPrint(msg) :
    print "SuperFitter    %s"%msg

#############################################
### signal regions
def getSRList(fitConfig = None, srType = "", srName = "", nBins = 1., binLow = 0.5, binHigh = 1.0) :
    if not fitConfig :
        userPrint("RegionLists getSRList ERROR    fitConfig not provided. Exiting.")
        sys.exit()

    sr_list = []
    userPrint(" > %s "%srName)
    currentChannel = fitConfig.addChannel(srType, [srName], nBins, binLow, binHigh)
    currentChannel.useOverflowBin = True
    currentChannel.useUnderflowBin = True
    sr_list.append(currentChannel)

    return sr_list

##############################################
### control regions

def addCR(fitConfig = None, crName = "", nBins = 1, binLow = 0, binHigh = 1) :
    if not fitConfig :
        userPrint("RegionLists addCR ERROR    fitConfig not provided. Exiting.")
        sys.exit()

    currentChannel = fitConfig.addChannel("cuts", [crName], nBins, binLow, binHigh)
    currentChannel.useOverflowBin  = True
    currentChannel.useUnderflowBin = True
    return currentChannel
    
def getCRList(fitConfig = None, srName = "", fitWW = False, fitTTbar = False) :

    if not fitConfig :
        userPrint("RegionLists getCRList ERROR    fitConfig not provided. Exiting.")
        sys.exit()

    cr_list = []

    ### add WW CR
    if fitTTbar :
        if "SR4" or "SRz" in srName :
            cr_list.append(addCR(fitConfig, "CR", 1, 0, 1))

    return cr_list
    
