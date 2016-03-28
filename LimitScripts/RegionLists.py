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
def getSRList(fitConfig = None, srType = "", srName = "", nBins = 1., binLow = 0.5, binHigh = 1.5) :
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
        if srName == "SRSF" or srName == "SRDF" :
            userPrint("RegionLists getCRList    Adding control region 'CRTop' to fit configuration")
            cr_list.append(addCR(fitConfig, "CRTop", 1, 0, 1))
    if fitWW :
        if srName == "SRSF" or srName == "SRDF" :
            userPrint("RegionLists getCRList    Adding control region 'CRVV' to fit configuration")
            cr_list.append(addCR(fitConfig, "CRVV", 1, 0, 1))

    return cr_list
    
##############################################
### validation regions
def addVR(fitConfig = None, vrName = "", nBins = 1, binLow = 0, binHigh = 1) :
    if not fitConfig :
        userPrint("RegionLists addVR ERROR    fitConfig not provided. Exiting.")
        sys.exit()

    currentChannel = fitConfig.addChannel("cuts", [vrName], nBins, binLow, binHigh)
    currentChannel.useOverflowBin  = True
    currentChannel.useUnderflowBin = True
    return currentChannel

def getVRList(fitConfig = None, srName = "") :
    if not fitConfig :
        userPrint("RegionLists getVRList ERROR    fitConfig not provided. Exiting.")
        sys.exit()
    
    vr_list = []
    if srName == "SRSF" or srName == "SRDF" :
        userPrint("RegionLists getVRList    Adding validation region 'VRTop' to fit configuration")
        vr_list.append(addVR(fitConfig, "VRTop", 1, 0, 1))
        userPrint("RegionLists getVRList    Adding validation region 'VRVV' to fit configuration")
        vr_list.append(addVR(fitConfig, "VRVV", 1, 0, 1))
    return vr_list

