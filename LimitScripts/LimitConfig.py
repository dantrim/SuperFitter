#!/usr/bin python
"""
###################################################
## SuperFitter                                   ##
##                                               ##
##          HistFitter configuration             ##
##                                               ##
##           http://bit.ly/1MGZXmq               ##
##                                               ##
## --------------------------------------------- ##
##  daniel antrim                                ##
##  daniel.joseph.antrim@cern.ch                 ##
##  September 2015                               ##
###################################################
"""

### ROOT imports
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)
from ROOT import kBlack,kWhite,kGray,kRed,kPink,kMagenta,kViolet,kBlue,kAzure,kCyan,kTeal,kGreen,kSpring,kYellow,kOrange,kDashed 
from ROOT import gROOT
from ROOT import TCanvas, TLegend, TLegendEntry

### histfitter imports
from configManager import configMgr
from configWriter import fitConfig,Measurement,Channel,Sample
from systematic import Systematic

configMgr.readFromTree = True

### "std" imports
from math import sqrt
import os
import sys
from optparse import OptionParser



### SuperFitter imports
sys.path.append(os.environ['LIMITDIR'])
import RunOptions # this is where the run-time configurations will be stored
import RegionDefs # this is where all of the selections are defined
import RegionLists # this is where the SR/CR/VR are built
import GridDefs   # this is where the handling of the signal grid is performed
import SystematicObject # this is where the handling of the systematics is performed

def userPrint(msg) :
    print "SuperFitter    %s"%msg

#####################################################################
### parse the user input
myParser = OptionParser()
myParser.add_option("-r", "--signalRegion", dest="signalRegion", default="")
myParser.add_option("-g", "--sigGrid",   dest="sigGrid", default="")
myParser.add_option("-t", "--doTheoryBand", action="store_true", dest="doTheoryBand", default=False)
myParser.add_option("-s", "--outputSuffix", dest="outputSuffix", default="")
myParser.add_option("-c", "--channel", dest="channel", default="")
myParser.add_option("--doExcl", action="store_true", dest="doExcl", default=False, help="Set exclusion fit")
myParser.add_option("--doDisco", action="store_true", dest="doDisco", default=False, help="Set discovery fit")
myParser.add_option("--doBkgOnly", action="store_true", dest="doBkgOnly", default=False, help="Set background-only fit")
(options, args) = myParser.parse_args(configMgr.userArg.strip('"').split())

### container to hold the configuration
runOptions = RunOptions.RunOptions()

##########################################
## fit type
doExcl      = options.doExcl
doDisco     = options.doDisco
doBkgOnly   = options.doBkgOnly
number_of_fit_types = 0
if doExcl       : number_of_fit_types += 1
if doDisco      : number_of_fit_types += 1
if doBkgOnly    : number_of_fit_types += 1
if number_of_fit_types > 1 :
    userPrint("Number of set fit types (e.g. exclusion, bkg-only, discovery) is greater than 1. Exitting.")
    sys.exit()
if number_of_fit_types == 0 :
    userPrint("The fit type has not been set! Use '--doExcl', '--doDisco', or '--doBkgOnly'. Exitting.")
    sys.exit()

runOptions.setExclusion(doExcl)
runOptions.setDiscovery(doDisco)
runOptions.setBackground(doBkgOnly)


##########################################
## get available region definitions
userPrint("Configuring the regions.")
regContainer = RegionDefs.buildRegions()
regContainer.Print()

verbose = True # hardcode this for now to be wicked crazy

##########################################
## take in the signal region choice
userPrint("Setting up the signal region.")


## lepton channels for SR to combine
possible_channels = ["all", "ee", "mm", "df", "sf", "sfdf"]
if options.channel == "" :
    userPrint("You must provide a channel. Possible options are \"all\", \"ee\", \"mm\", \"df\", \"sf\", \"sfdf\"")
    sys.exit()
if str(options.channel).lower() not in possible_channels :
    userPrint("You have provided an unhandled option for the channel: " + str(options.channel))
    sys.exit()

def checkSignalRegion(region_name, region_channel, built_regions) :
    full_region = region_name + "_" + region_channel.upper()

    parent_found = False
    for built_region in built_regions :
        if region_name in built_region :
            parent_found = True

    if not parent_found and region_name == "SRwt" :
        for built_region in built_regions :
            if "SRw_" in built_region or "SRt_" in built_region :
                parent_found = True

    if not parent_found :
        x = "Base parent region requested (%s) not found in built regions. Check RegionDefs."%region_name
        userPrint(x)
        return False

    if region_channel.lower() != "all" and region_channel.lower() != "sfdf" :
        n_found = 0
        for built_region in built_regions :
            if full_region == built_region :
                n_found += 1 
        if n_found != 1 :
            x = "You have requested a specific channel (%s) for region %s but multiple channels have been found."%(region_channel, region_name)
            userPrint(x)
            x = "Region to run is ambiguous! Check RegionDefs."
            userPrint(x)
            return False

    elif region_channel.lower() != "all" and region_channel.lower() == "sfdf" and region_name != "SRwt" :
        sf_found = False
        df_found = False
        for built_region in built_regions :
            if region_name in built_region and "SF" in built_region :
                sf_found = True
            if region_name in built_region and "DF" in built_region :
                df_found = True
        all_channels_found = sf_found and df_found
        if not all_channels_found :
            sf_status = "SF: "
            df_status = "DF: "
            if sf_found : sf_status += "YES"
            else : sf_status += "NO"
            if df_found : df_status += "YES"
            else : df_status += "NO"
            x = "You have requested SF+DF channels for region %s but not all channels have been found."
            userPrint(x)
            x = " > %s  %s"%(sf_status, df_status)
            userPrint(x)
            return False

    elif region_channel.lower() != "all" and region_channel.lower() == "sfdf" and region_name == "SRwt" :
        user_regions = []
        if region_name == "SRwt" :
            user_regions += "SRw"
            user_regions += "SRt"
        else :
            user_regions += region_name

        for reg_ in user_regions :
            sf_found  = False
            df_found  = False
            for built_region in built_regions :
                if reg_ in built_region and "SF" in built_region :
                    sf_found = True
                elif reg_ in built_region and "DF" in built_region :
                    df_found = True
            all_channels_found = sf_found and df_found

            if not all_channels_found :
                sf_status = "SF: "
                df_status = "DF: "
                if sf_found : sf_status += "YES"
                else : sf_status += "NO"
                if df_found : df_status += "YES"
                else : df_status += "NO"
                x = "You have requested SF and DF channels for region %s but not all channels have been found."%reg_
                userPrint(x)
                x = " > %s  %s  %s"%(sf_status, df_status)
                userPrint(x)
                return False

    elif region_channel.lower() == "all" :
        user_regions = []
        if region_name == "SRwt" :
            user_regions += "SRw"
            user_regions += "SRt" 
        else :
            user_regions += region_name

        for reg_ in user_regions :
            ee_found = False
            mm_found = False
            df_found = False
            for built_region in built_regions :
                if reg_ in built_region and "EE" in built_region :
                    ee_found = True
                elif reg_ in built_region and "MM" in built_region :
                    mm_found = True
                elif reg_ in built_region and "DF" in built_region :
                    df_found = True
            all_channels_found = ee_found and mm_found and df_found
            if not all_channels_found :
                ee_status = "EE: "
                mm_status = "MM: "
                df_status = "DF: "
                if ee_found : ee_status += "YES"
                else : ee_status += "NO"
                if mm_found : mm_status += "YES"
                else : mm_status += "NO"
                if df_found : df_status += "YES"
                else : df_status += "NO"
                x = "You have requested all channels for region %s but not all channels have been found."%reg_
                userPrint(x)
                x = " > %s  %s  %s"%(ee_status, mm_status, df_status)
                userPrint(x)
                return False
            

       # for built_region in built_regions :
       #     if region_name in built_region and "EE" in built_region : 
       #         ee_found = True
       #     elif region_name in built_region and "MM" in built_region :
       #         mm_found = True
       #     elif region_name in built_region and "DF" in built_region :
       #         df_found = True
       # all_channels_found = ee_found and mm_found and df_found
       # if not all_channels_found :
       #     ee_status = "EE: "
       #     mm_status = "MM: "
       #     df_status = "DF: "
       #     if ee_found : ee_status += "YES"
       #     else : ee_status += "NO"
       #     if mm_found : mm_status += "YES"
       #     else : mm_status += "NO"
       #     if df_found : df_status += "YES"
       #     else : df_status += "NO"
       #     x = "You have requested all channels for region %s but not all channels have been found."%region_name
       #     userPrint(x)
       #     x = " > %s  %s  %s"%(ee_status, mm_status, df_status)
       #     userPrint(x)
       #     return False

    x = "Signal region requested seems to be OK: %s"%full_region
    userPrint(x)
    return True

print "OPTIONS SR %s"%str(options.signalRegion)
if not checkSignalRegion(str(options.signalRegion), str(options.channel), regContainer.getDict().keys()) :
    sys.exit()

runOptions.setCutDict(regContainer.getDict())
region_name = options.signalRegion + "_" + options.channel
runOptions.setSignalRegion(region_name)

#########################################
## set the simultamneous fit options
userPrint("Setting whether to do simultaneous fit.")

fitWW = True
#ttbar skip
fitTTbar =True
userPrint(" > Fit WW    : %s"%fitWW)
userPrint(" > Fit TTbar : %s"%fitTTbar)
runOptions.setFitWW(fitWW)
runOptions.setFitTTbar(fitTTbar)

userPrint("Setting the blinding options.")
## blind the SR
runOptions.setBlindSR(True)
## blind the CR
runOptions.setBlindCR(False)
## blind the VR
runOptions.setBlindVR(False)

##########################################
## construct the signal grid 
userPrint("Setting up the signal grid.")
gridname = options.sigGrid
signalGrid = GridDefs.SignalGrid(gridname, verbose)

runOptions.setGrid(signalGrid.name)

##########################################
## do we want to run the theory XS band (dashed-red lines)
doTheoryBand = options.doTheoryBand
runOptions.setTheoryBand(doTheoryBand)

#########################################
## configure input and output lumi
userPrint("Setting the luminosity.")
lumi_input  = 1.0 # the MC ntuples are normalized to 1.00/fb
lumi_output = 36.00 
lumi_units  = "fb-1"
#userPrint(" --> input  : %s"%str(lumi_input))
#userPrint(" --> output : %s"%str(lumi_output))
#userPrint(" --> units  : %s"%lumi_units)

runOptions.setInputLumi(lumi_input)
runOptions.setOutputLumi(lumi_output)
runOptions.setLumiUnits(lumi_units)



#########################################
## load the samples
userPrint("Setting up the samples.")
#hft_dir = "/data/uclhc/uci/user/dantrim/SuperFitter/"
hft_dir = "/data/uclhc/uci/user/dantrim/n0231val/SuperFitter/hft_trees/"

## data, ttbar, and ww file
data_file       = hft_dir + "HFT_Data_13TeV_19Jan17.root"
mc_file         = hft_dir + "HFT_BG_13TeV_19Jan17.root"
top_file        = hft_dir + "HFT_Top_13TeV_19Jan17.root"
ttv_higgs_file  = hft_dir + "HFT_TTV_Higgs_13TeV_19Jan17.root"
vv_df_file      = hft_dir + "HFT_VVDF_13TeV_19Jan17.root"
vv_sf_file      = hft_dir + "HFT_VVSF_13TeV_19Jan17.root" 
zjets_file      = hft_dir + "HFT_Zjets_13TeV_19Jan17.root"
fake_file       = hft_dir + "HFT_Fakes_13TeV_Jul27.root" # scaling up the fakes from ICHEP 
signal_file = ""
if gridname == "bWN" : signal_file = hft_dir + "HFT_bWN_13TeV_Nov22.root"
else : 
    userPrint('HFT not available for requested grid "%s"'%gridname)
    userPrint(' --> Exitting.')
    sys.exit()

## set the samples
#ttbar skip
ttbarSample     = Sample("TTbar",   ROOT.TColor.GetColor("#FC0D1B"))
stSample        = Sample("ST",      ROOT.TColor.GetColor("#DE080C")) 
ttvSample       = Sample("TTV",      ROOT.kCyan-7)# ROOT.kRed)
vvDFSample      = Sample("VVDF",      ROOT.TColor.GetColor("#41C1FC"))
vvSFSample      = Sample("VVSF",   ROOT.TColor.GetColor("#41C1FC"))
fakeSample      = Sample("Fakes", ROOT.kOrange+7)
higgsSample     = Sample("Higgs", ROOT.TColor.GetColor("#ddc29a"))
zjetsSample     = Sample("Zjets",   ROOT.TColor.GetColor("#82DE68"))
#wwSample       = Sample("WW",      ROOT.TColor.GetColor("#41C1FC"))
#dysample        = Sample("DrellYan", ROOT.kYellow)
#wjetsSample = Sample("Wjets",   ROOT.TColor.GetColor("#5E9AD6")) 
#wzSample    = Sample("WZ",      ROOT.TColor.GetColor("#F9F549")) 
#zzSample    = Sample("ZZ",      ROOT.TColor.GetColor("#FFEF53")) 
dataSample  = Sample("Data_CENTRAL", kBlack)

## attach samples to their files
#ttbar skip
all_samples = [ ttbarSample, stSample, ttvSample, vvDFSample, vvSFSample, fakeSample, higgsSample, zjetsSample, dataSample ]
#samples_mc_noVV = [ttbarSample, stSample, zjetsSample, ttvSample, higgsSample]
#samples_mc_noVV = [ttbarSample, stSample, wjetsSample, zjetsSample, ttvSample]
samples_data = [ dataSample ]
#samples     = [ ttbarSample, vvSample, stSample, wjetsSample, zjetsSample, dataSample ]
#for s in samples_mc_noVV :
#    s.setFileList( [mc_file] )
#    userPrint(" --> Sample : %s at %s"%(s.name, mc_file))

ttbarSample.setFileList([top_file])
stSample.setFileList([top_file])
ttvSample.setFileList([ttv_higgs_file])
higgsSample.setFileList([ttv_higgs_file])
vvDFSample.setFileList([vv_df_file])
vvSFSample.setFileList([vv_sf_file])
fakeSample.setFileList([fake_file])
zjetsSample.setFileList([zjets_file])
userPrint(" --> Sample : %s at %s"%(ttbarSample.name, top_file))
userPrint(" --> Sample : %s at %s"%(stSample.name, top_file))
userPrint(" --> Sample : %s at %s"%(ttvSample.name, ttv_higgs_file))
userPrint(" --> Sample : %s at %s"%(higgsSample.name, ttv_higgs_file))
userPrint(" --> Sample : %s at %s"%(vvDFSample.name, vv_df_file))
userPrint(" --> Sample : %s at %s"%(vvSFSample.name, vv_sf_file))
userPrint(" --> Sample : %s at %s"%(fakeSample.name, fake_file))
userPrint(" --> Sample : %s at %s"%(zjetsSample.name, zjets_file))

dataSample.setFileList([data_file])
userPrint(" --> Sample : %s at %s"%(dataSample.name, data_file))


##########################################
## split MC sys --> need to look this one up again
runOptions.setSplitMCsys(False)

##########################################
## set the eventweight leaf-name
userPrint("Specifying weights.")

weights_list = ["eventweight"]
for weight_ in weights_list :
    userPrint(" --> %s"%weight_)
runOptions.setWeights(weights_list)

##########################################
## output directory suffix
userPrint("Setting the output directory suffix.")
runOptions.setOutputSuffix(options.outputSuffix)

##########################################
## misc
userPrint("Setting the calculator type.")
# CalculatorType:       0:Frequentist   1:Hybrid    2:Asymptotic
runOptions.setCalculatorType(2)
# TestStatType:         0:LEP   1:Tevatron  2:Profile likelihood    3:One sided PL
runOptions.setTestStatType(3)
# Number of scan points when scanning over mu_SIG
runOptions.setNumberOfScanPoints(20)

# Nominal name (suffix) for trees
configMgr.nomName = "_CENTRAL"

#########################################
## propagate the configuration
userPrint("Sending the configuration to configMgr.")

if runOptions.doExclusion()  : configMgr.myFitType == configMgr.FitType.Exclusion
if runOptions.doDiscovery()  : configMgr.myFitType == configMgr.FitType.Discovery
if runOptions.doBackground() : configMgr.myFitType == configMgr.FitType.Background

configMgr.blindSR = runOptions.doBlindSR()
print 60*"-"
print "HARDCODING: BLINDING SIGNAL REGIONS"
print "HARDCODING: BLINDING SIGNAL REGIONS"
print "HARDCODING: BLINDING SIGNAL REGIONS"
print "HARDCODING: BLINDING SIGNAL REGIONS"
configMgr.blindSR = True
configMgr.blindCR = runOptions.doBlindCR()
configMgr.blindVR = runOptions.doBlindVR()
print 60*"-"
print "HARDCODING: NOT BLINDING VALIDATION REGIONS"
print "HARDCODING: NOT BLINDING VALIDATION REGIONS"
print "HARDCODING: NOT BLINDING VALIDATION REGIONS"
print "HARDCODING: NOT BLINDING VALIDATION REGIONS"
print 60*"-"
configMgr.blindVR = False

configMgr.fixSigXSec = runOptions.doTheoryBand()

configMgr.analysisName   = runOptions.getSignalRegion() + "_" + runOptions.getGrid()

suffix = ""
if runOptions.getOutputSuffix() != "" :
    suffix += "_%s"%runOptions.getOutputSuffx()


configMgr.histCacheFile  = "data" + suffix + "/" + configMgr.analysisName + suffix + ".root"
configMgr.outputFileName = "results" + suffix + "/" + configMgr.analysisName + suffix + "_Output.root"

configMgr.inputLumi  = runOptions.getInputLumi()
configMgr.outputLumi = runOptions.getOutputLumi()
configMgr.setLumiUnits(runOptions.getLumiUnits())

configMgr.cutsDict = runOptions.getCutDict()

configMgr.weights = runOptions.getWeights()

configMgr.calculatorType = runOptions.getCalculatorType()
configMgr.testStatType   = runOptions.getTestStatType()
configMgr.nPoints        = runOptions.getNumberOfScanPoints()
configMgr.writeXML = True

if not runOptions.check() :
    sys.exit()
else :
    userPrint(" --> RunOptions consistent.")
    runOptions.Print()
    print "      Data file   : ", data_file
    print "      MC file     : ", mc_file
    print "      Signal file : ", signal_file
    print "      Samples"
    for s in all_samples :
        print "        > ", s.name 
    print " + ---------------------------------------- + "


######################################################################
## setup the fitconfig
userPrint("Setting up the FitConfig and POI.")
tlx = configMgr.addFitConfig("BkgOnly")
#tlx = configMgr.addFitConfig("Bkg_TopLvlXML")
meas = tlx.addMeasurement(name="NormalMeasurement", lumi = 1., lumiErr = 0.05)
meas.addPOI("mu_SIG")

tlx.statErrThreshold = 0.001

######################################################################
## set up the systematic object
userPrint("Setting up the SystematicObject.")
sysObj = SystematicObject.SystematicObject(configMgr, runOptions.doSplitMCsys())

######################################################################
## configure the backgrounds/samples
userPrint("Configuring the samples.")


## helper function to add common MC systematics
def addSys(sample, doSimFit, sysObject, is_signal=False) :
    if doSimFit :

        #############################################################
        ## weight systematics
        #############################################################

        # pileup
        if not is_signal :
            sample.addSystematic(sysObject.AR_PILEUP_CR)

        # e-gamma
        if not is_signal :
            sample.addSystematic(sysObject.AR_EL_EFF_ID_CR)
            #sample.addSystematic(sysObject.AR_EL_EFF_Iso_CR)
            #sample.addSystematic(sysObject.AR_EL_EFF_Reco_CR)
        elif is_signal :
            sample.addSystematic(sysObject.AR_EL_EFF_ID_SIG_CR)
            #sample.addSystematic(sysObject.AR_EL_EFF_Iso_SIG_CR)
            #sample.addSystematic(sysObject.AR_EL_EFF_Reco_SIG_CR)

        ## muons
        #if not is_signal :
        #    #sample.addSystematic(sysObject.AR_MUON_EFF_STAT_CR)
        #    #sample.addSystematic(sysObject.AR_MUON_EFF_STAT_LOWPT_CR)
        #    sample.addSystematic(sysObject.AR_MUON_EFF_SYS_CR)
        #    sample.addSystematic(sysObject.AR_MUON_EFF_SYS_LOWPT_CR)
        #    sample.addSystematic(sysObject.AR_MUON_ISO_STAT_CR)
        #    sample.addSystematic(sysObject.AR_MUON_ISO_SYS_CR)
        #elif is_signal :
        #    #sample.addSystematic(sysObject.AR_MUON_EFF_STAT_SIG_CR)
        #    #sample.addSystematic(sysObject.AR_MUON_EFF_STAT_LOWPT_SIG_CR)
        #    sample.addSystematic(sysObject.AR_MUON_EFF_SYS_SIG_CR)
        #    sample.addSystematic(sysObject.AR_MUON_EFF_SYS_LOWPT_SIG_CR)
        #    sample.addSystematic(sysObject.AR_MUON_ISO_STAT_SIG_CR)
        #    sample.addSystematic(sysObject.AR_MUON_ISO_SYS_SIG_CR)

        # jets
        if not is_signal :
            sample.addSystematic(sysObject.AR_JET_JVTEff_CR)
        elif is_signal :
            sample.addSystematic(sysObject.AR_JET_JVTEff_SIG_CR)

        ## flavor tagging
        if not is_signal :
            sample.addSystematic(sysObject.AR_FT_EFF_B_CR)
        #    sample.addSystematic(sysObject.AR_FT_EFF_C_CR)
            sample.addSystematic(sysObject.AR_FT_EFF_Light_CR)
        #    sample.addSystematic(sysObject.AR_FT_EFF_extrapolation_CR)
        #    sample.addSystematic(sysObject.AR_FT_EFF_extrapolation_charm_CR)
        elif is_signal :
            sample.addSystematic(sysObject.AR_FT_EFF_B_SIG_CR)
        #    sample.addSystematic(sysObject.AR_FT_EFF_C_SIG_CR)
            sample.addSystematic(sysObject.AR_FT_EFF_Light_SIG_CR)
        #    sample.addSystematic(sysObject.AR_FT_EFF_extrapolation_SIG_CR)
        #    sample.addSystematic(sysObject.AR_FT_EFF_extrapolation_charm_SIG_CR)

        #############################################################
        ## shape systematics
        #############################################################

        ## e-gamma
        sample.addSystematic(sysObject.AR_EG_RESOLUTION_ALL_CR)
        #sample.addSystematic(sysObject.AR_EG_SCALE_ALL_CR)
        ## muons
        #sample.addSystematic(sysObject.AR_MUON_ID_CR)
        sample.addSystematic(sysObject.AR_MUON_MS_CR)
        sample.addSystematic(sysObject.AR_MUON_SCALE_CR)
        ## jets
        sample.addSystematic(sysObject.AR_JER_CR)
        sample.addSystematic(sysObject.AR_JET_GroupedNP_1_CR)
        sample.addSystematic(sysObject.AR_JET_GroupedNP_2_CR)
        sample.addSystematic(sysObject.AR_JET_GroupedNP_3_CR)
        ## met
        #sample.addSystematic(sysObject.AR_MET_SoftTrk_ResoPara_CR)
        #sample.addSystematic(sysObject.AR_MET_SoftTrk_ResoPerp_CR)
        #sample.addSystematic(sysObject.AR_MET_SoftTrk_Scale_CR)
    else :

        #############################################################
        ## weight systematics
        #############################################################

        # pileup
        if not is_signal :
            sample.addSystematic(sysObject.AR_PILEUP_MC)

        # e-gamma
        if not is_signal :
            sample.addSystematic(sysObject.AR_EL_EFF_ID_MC)
           # sample.addSystematic(sysObject.AR_EL_EFF_Iso_MC)
           # sample.addSystematic(sysObject.AR_EL_EFF_Reco_MC)
        elif is_signal :
            sample.addSystematic(sysObject.AR_EL_EFF_ID_SIG_MC)
           # sample.addSystematic(sysObject.AR_EL_EFF_Iso_SIG_MC)
           # sample.addSystematic(sysObject.AR_EL_EFF_Reco_SIG_MC)

        ## muons
        #if not is_signal :
        #    #sample.addSystematic(sysObject.AR_MUON_EFF_STAT_MC)
        #    #sample.addSystematic(sysObject.AR_MUON_EFF_STAT_LOWPT_MC)
        #    sample.addSystematic(sysObject.AR_MUON_EFF_SYS_MC)
        #    sample.addSystematic(sysObject.AR_MUON_EFF_SYS_LOWPT_MC)
        #    sample.addSystematic(sysObject.AR_MUON_ISO_STAT_MC)
        #    sample.addSystematic(sysObject.AR_MUON_ISO_SYS_MC)
        #elif is_signal :
        #    #sample.addSystematic(sysObject.AR_MUON_EFF_STAT_SIG_MC)
        #    #sample.addSystematic(sysObject.AR_MUON_EFF_STAT_LOWPT_SIG_MC)
        #    sample.addSystematic(sysObject.AR_MUON_EFF_SYS_SIG_MC)
        #    sample.addSystematic(sysObject.AR_MUON_EFF_SYS_LOWPT_SIG_MC)
        #    sample.addSystematic(sysObject.AR_MUON_ISO_STAT_SIG_MC)
        #    sample.addSystematic(sysObject.AR_MUON_ISO_SYS_SIG_MC)

        # jets
        if not is_signal :
            sample.addSystematic(sysObject.AR_JET_JVTEff_MC)
        elif is_signal :
            sample.addSystematic(sysObject.AR_JET_JVTEff_SIG_MC)

        ## flavor tagging
        if not is_signal :
            sample.addSystematic(sysObject.AR_FT_EFF_B_MC)
        #    sample.addSystematic(sysObject.AR_FT_EFF_C_MC)
            sample.addSystematic(sysObject.AR_FT_EFF_Light_MC)
        #    sample.addSystematic(sysObject.AR_FT_EFF_extrapolation_MC)
        #    sample.addSystematic(sysObject.AR_FT_EFF_extrapolation_charm_MC)
        elif is_signal :
            sample.addSystematic(sysObject.AR_FT_EFF_B_SIG_MC)
        #    sample.addSystematic(sysObject.AR_FT_EFF_C_SIG_MC)
            sample.addSystematic(sysObject.AR_FT_EFF_Light_SIG_MC)
        #    sample.addSystematic(sysObject.AR_FT_EFF_extrapolation_SIG_MC)
        #    sample.addSystematic(sysObject.AR_FT_EFF_extrapolation_charm_SIG_MC)

        #############################################################
        ## shape systematics
        #############################################################

        ## e-gamma
        sample.addSystematic(sysObject.AR_EG_RESOLUTION_ALL_MC)
        #sample.addSystematic(sysObject.AR_EG_SCALE_ALL_MC)
        ## muons
        #sample.addSystematic(sysObject.AR_MUON_ID_MC)
        sample.addSystematic(sysObject.AR_MUON_MS_MC)
        sample.addSystematic(sysObject.AR_MUON_SCALE_MC)
        ## jets
        sample.addSystematic(sysObject.AR_JER_MC)
        sample.addSystematic(sysObject.AR_JET_GroupedNP_1_MC)
        sample.addSystematic(sysObject.AR_JET_GroupedNP_2_MC)
        sample.addSystematic(sysObject.AR_JET_GroupedNP_3_MC)
        ## met
        #sample.addSystematic(sysObject.AR_MET_SoftTrk_ResoPara_MC)
        #sample.addSystematic(sysObject.AR_MET_SoftTrk_ResoPerp_MC)
        #sample.addSystematic(sysObject.AR_MET_SoftTrk_Scale_MC)

    return sample


for sample in all_samples :
    # ----------------------------------------------- #
    #  TTbar                                          #
    # ----------------------------------------------- #
    if "TTbar" in sample.name :
        sample.setStatConfig( not runOptions.doSplitMCsys() )

        if runOptions.doSplitMCsys() :
            sample.addSystematic( sysObj.mcstat_TTbar )

        ## add systematics
        sample = addSys(sample, fitTTbar, sysObj) 

        #sample.addSystematic( sysObj.dummySyst )
        if runOptions.doFitTTbar() :
            if "SRw" in runOptions.getSignalRegion() or "SRt" in runOptions.getSignalRegion() or "SRwt" in runOptions.getSignalRegion() :
                sample.setNormFactor("mu_TTbar", 1., 0., 10.)
                sample.setNormRegions([("CRTop", "cuts")])
        else : 
            sample.setNormByTheory() # i.e. use MC-only for normalization (no fitting, etc...)
    # ----------------------------------------------- #
    # TTV
    # ----------------------------------------------- #
    elif "TTV" in sample.name :
        sample.setStatConfig( not runOptions.doSplitMCsys() )

        if runOptions.doSplitMCsys() :
            sample.addSystematic( sysObj.mcstat_TTV )

        ## add systematics
        sample = addSys(sample, False, sysObj)

        sample.setNormByTheory()
    # ----------------------------------------------- #
    #  Higgs
    # ----------------------------------------------- #
    elif "Higgs" in sample.name :
        sample.setStatConfig( not runOptions.doSplitMCsys() )

        if runOptions.doSplitMCsys() :
            sample.addSystematic( sysObj.mcstat_Higgs )

        ## add systematics
        sample = addSys(sample, False, sysObj)

        sample.setNormByTheory()
    # ----------------------------------------------- #
    #  VV - SF                                        #
    # ----------------------------------------------- #
    elif "VVSF" in sample.name :
        sample.setStatConfig( not runOptions.doSplitMCsys() )

        if runOptions.doSplitMCsys() :
            sample.addSystematic( sysObj.mcstat_VVSF )

        ## add systematics
        sample = addSys(sample, fitWW, sysObj)

        #sample.addSystematic( sysObj.dummySyst )
        if runOptions.doFitWW() :
            if "SRw" in runOptions.getSignalRegion() or "SRt" in runOptions.getSignalRegion() or "SRwt" in runOptions.getSignalRegion() :
                sample.setNormFactor("mu_VVSF", 1., 0., 10.)
                sample.setNormRegions([("CRVVSF", "cuts")])
        else :
            sample.setNormByTheory()
    # ----------------------------------------------- #
    #  VV - DF                                        #
    # ----------------------------------------------- #
    elif "VVDF" in sample.name :
        sample.setStatConfig( not runOptions.doSplitMCsys() )

        if runOptions.doSplitMCsys() :
            sample.addSystematic( sysObj.mcstat_VVDF )

        ## add systematics
        sample = addSys(sample, fitWW, sysObj)

        #sample.addSystematic( sysObj.dummySyst )
        if runOptions.doFitWW() :
            if "SRw" in runOptions.getSignalRegion() or "SRt" in runOptions.getSignalRegion() or "SRwt" in runOptions.getSignalRegion() :
                sample.setNormFactor("mu_VVDF", 1., 0., 10.)
                sample.setNormRegions([("CRVVDF", "cuts")])
        else :
            sample.setNormByTheory()

    # ----------------------------------------------- #
    #  WW                                             #
    # ----------------------------------------------- #
    elif "WW" in sample.name :
        sample.setStatConfig( not runOptions.doSplitMCsys() ) 

        if runOptions.doSplitMCsys() :
            sample.addSystematic( sysObj.mcstat_WW )

        ## add sys
        sample = addSys(sample, False, sysObj)

        sample.setNormByTheory()

    # ----------------------------------------------- #
    #  ST
    # ----------------------------------------------- #
    elif "ST" in sample.name :
        sample.setStatConfig( not runOptions.doSplitMCsys() )

        if runOptions.doSplitMCsys() :
            sample.addSystematic( sysObj.mcstat_ST )

        ## add systematics
        sample = addSys(sample, False, sysObj)

        #sample.addSystematic( sysObj.dummySyst )
        sample.setNormByTheory()

    # ----------------------------------------------- #
    #  DY
    # ----------------------------------------------- #
    elif "DrellYan" in sample.name :
        sample.setStatConfig( not runOptions.doSplitMCsys() )

        if runOptions.doSplitMCsys() :
            sample.addSystematic( sysObj.mcstat_DY )

        ## add systematics
        sample = addSys(sample, False, sysObj)

        #sample.addSystematic( sysObj.dummySyst )
        sample.setNormByTheory()

    # ----------------------------------------------- #
    #  Wjets                                          #
    # ----------------------------------------------- #
    elif "Wjets" in sample.name :
        sample.setStatConfig( not runOptions.doSplitMCsys() )

        if runOptions.doSplitMCsys() :
            sample.addSystematic( sysObj.mcstat_Wjets )

        ## add systematics
        sample = addSys(sample, False, sysObj)

        #sample.addSystematic( sysObj.dummySyst )
        sample.setNormByTheory()
        
    # ----------------------------------------------- #
    #  Zjets                                          #
    # ----------------------------------------------- #
    elif "Zjets" in sample.name :
        sample.setStatConfig( not runOptions.doSplitMCsys() )

        if runOptions.doSplitMCsys() :
            sample.addSystematic( sysObj.mcstat_Zjets )

        ## add systematics
        sample = addSys(sample, False, sysObj)

        #sample.addSystematic( sysObj.dummySyst )
        sample.setNormByTheory()
    # ----------------------------------------------- #
    #  WZ                                             #
    # ----------------------------------------------- #
    elif "WZ" in sample.name :
        sample.setStatConfig( not runOptions.doSplitMCsys() )

        if runOptions.doSplitMCsys() :
            sample.addSystematic( sysObj.mcstat_WZ )

        ## add sys
        sample = addSys(sample, False, sysObj)

        sample.setNormByTheory()

    # ----------------------------------------------- #
    #  ZZ                                             #
    # ----------------------------------------------- #
    elif "ZZ" in sample.name :
        sample.setStatConfig( not runOptions.doSplitMCsys() )

        if runOptions.doSplitMCsys() :
            sample.addSystematic( sysObj.mcstat_ZZ )

        ## add sys
        sample = addSys(sample, False, sysObj)

        sample.setNormByTheory()

    # ----------------------------------------------- #
    #  Fake                                           #
    # ----------------------------------------------- #
    elif "Fake" in sample.name :
        sample.setStatConfig( not runOptions.doSplitMCsys() )
        sample.setNormByTheory()
        # the sample will be scaled by the lumi input/output ratio
        # and we have run the fakes over 12.2/fb --
        # scale back to 1.0/fb from 12.2 by dividing by 12.2
        sample.weights = ["(FakeWeight / 12.2)"]
        if runOptions.doSplitMCsys() :
            sample.addSystematic( sysObj.mcstat_FAKE )

        #SRw-DF
        #sample.buildHisto([0.58],   "SRw_DF", "cuts")
        ##SRw-EE
        #sample.buildHisto([0.001],  "SRw_EE", "cuts")
        ##SRw-MM
        #sample.buildHisto([1.02],   "SRw_MM", "cuts")
        ##SRw-SF
        #sample.buildHisto([0.98],   "SRw_SF", "cuts")

        ##SRt-DF
        #sample.buildHisto([0.90],   "SRt_DF", "cuts")
        ##SRt-EE
        #sample.buildHisto([0.0],    "SRt_EE", "cuts")
        ##SRt-MM
        #sample.buildHisto([0.0],    "SRt_MM", "cuts")
        ##SRt-SF
        #sample.buildHisto([0.0],    "SRt_SF", "cuts")

        ##CRVV-DF
        #sample.buildHisto([0.0],    "CRVVDF", "cuts")
        ##CRVV-SF 
        #sample.buildHisto([4.78],   "CRVVSF", "cuts")

        ##VRVVVDF
        #sample.buildHisto([17.23],  "VRVVDF", "cuts")
        ##VRVVSF
        #sample.buildHisto([22.49],  "VRVVSF", "cuts")

        #CRTop
        #sample.buildHisto([0.001],  "CRTop", "cuts")
        #sample.buildHisto([1.0],  "CRTop", "cuts")
        ##VRTop
        #sample.buildHisto([7.11],   "VRTop", "cuts")

    # ----------------------------------------------- #
    #  Data                                           #
    # ----------------------------------------------- #
    elif "Data" in sample.name :
        # let HF know that this sample is data
        sample.setData()

######################################################################
## Give the fit config the samples
userPrint("Propagating samples to the fit config.")
tlx.addSamples(all_samples)


######################################################################
## set up the CR's for simultaneous fit
userPrint("Setting up the CR's.")
crList = RegionLists.getCRList(tlx, runOptions.getSignalRegion(), fitWW = runOptions.doFitWW(), fitTTbar = runOptions.doFitTTbar())
print crList
if runOptions.doFitTTbar() or runOptions.doFitWW() :
    tlx.setBkgConstrainChannels(crList)

######################################################################
## Setup the SR for bkg-only and exclusion
if runOptions.doExclusion() or runOptions.doBackground() : # include background-only fit so that we can use the SR's for VR
    userPrint("Setting up signal region.")

#    def add_SRs(srType = "", srName = "", nBins = 1., binLow = 0.5, binHigh = 1.0) :
#        sr_list = []
#        userPrint(" > %s "%srName)
#        currentChannel = tlx.addChannel(srType, [srName], nBins, binLow, binHigh)
#        currentChannel.useOverflowBin = True
#        currentChannel.useUnderflowBin = True
#        sr_list.append(currentChannel)
#
#        return sr_list

    srList = []
    if "all" in runOptions.getSignalRegion().lower() :
        base_region = runOptions.getSignalRegion().split("_all")[0] 
        flavors = []
        if base_region != "SRwt" :
            flavors = ["%s_%s"%(base_region, f) for f in ["DF","EE","MM"]]
        else :
            flavors =  ["SRw_%s"%f for f in ["DF", "EE", "MM"]]
            flavors += ["SRt_%s"%f for f in ["DF", "EE", "MM"]]

        for flav in flavors :
            srList_x = RegionLists.getSRList(tlx, "cuts", flav, 1., 0.5, 1.5)
            userPrint("Adding signal region: %s"%flav)

            if "SRw_" in flav or "SRt_" in flav :
                srList_x[0].getSample("TTbar").addSystematic( sysObj.SRwt_TTbar_THEORY )
                srList_x[0].getSample("VVDF").addSystematic( sysObj.SRwt_VVDF_THEORY )
                srList_x[0].getSample("VVSF").addSystematic( sysObj.SRwt_VVSF_THEORY)

            srList.append(srList_x[0])

    elif "sfdf" in runOptions.getSignalRegion().lower() :
        base_region = runOptions.getSignalRegion().split("_sfdf")[0]
        flavors = []
        if base_region != "SRwt" :
            flavors = ["%s_%s"%(base_region, f) for f in ["SF", "DF"]]
        else :
            flavors = ["SRw_%s"%f for f in ["SF", "DF"]]
            flavors += ["SRt_%s"%f for f in ["SF", "DF"]]
        for flav in flavors :
            srList_x = RegionLists.getSRList(tlx, "cuts", flav, 1., 0.5, 1.5)
            userPrint("Adding signal region: %s"%flav)

            if "SRw_" in flav or "SRt_" in flav :
                srList_x[0].getSample("TTbar").addSystematic( sysObj.SRwt_TTbar_THEORY )
                srList_x[0].getSample("VVDF").addSystematic( sysObj.SRwt_VVDF_THEORY )
                srList_x[0].getSample("VVSF").addSystematic( sysObj.SRwt_VVSF_THEORY )

            srList.append(srList_x[0])
    else : 
        srList = RegionLists.getSRList(tlx, "cuts", runOptions.getSignalRegion(), 1., 0.5, 1.5)
        userPrint("Adding signal region: %s"%runOptions.getSignalRegion())

    if runOptions.doExclusion() :
        userPrint("Setting signal regions to SignalChannels.")
        tlx.setSignalChannels(srList)
    elif runOptions.doBackground() :
        userPrint("Setting signal regions to ValidationChannels.")
        tlx.setValidationChannels(srList)

######################################################################
## Add the validation regions
if runOptions.doBackground() :
    # for some reason HistFitter will not distinguish between VR and SR
    # in exclusion and discovery fits?
    userPrint("Setting up validation regions.") 

    vrList = RegionLists.getVRList(tlx, runOptions.getSignalRegion())
    tlx.setValidationChannels(vrList) # this function appends to a list, so does not overwrite previous setValidationChannels calls

#####################################################################
## SETUP PLOTTING                                                  ##
## SETUP PLOTTING                                                  ##
## SETUP PLOTTING                                                  ##
#####################################################################
userPrint("Setting up the sample plot options.")
tlx.dataColor = dataSample.color
tlx.totalPdfColor = kBlue
tlx.errorFillColor = kBlue - 5
tlx.errorFillStyle = 3004
tlx.errorLineStyle = kDashed
tlx.errorLineColor = kBlue - 5

for cr in crList :
    cr.titleY = "Number of Entries"
    cr.ATLASLabelX = 0.25
    cr.ATLASLabelY = 0.85
    cr.ATLASLabelText = "Work in Progress"

c = TCanvas()
fillStyle = 1001
leg = TLegend(0.6, 0.475, 0.9, 0.925, "")
leg.SetFillStyle(0)
leg.SetFillColor(0)
leg.SetBorderSize(0)

entry = TLegendEntry()
entry = leg.AddEntry("", "Data (#sqrt{s} = 13 TeV)", "p")
entry.SetMarkerColor(tlx.dataColor)
entry.SetMarkerStyle(20)
#
entry = leg.AddEntry("", "Total pdf", "lf")
entry.SetLineColor(tlx.totalPdfColor)
entry.SetLineWidth(2)
entry.SetFillColor(tlx.errorFillColor)
entry.SetFillStyle(tlx.errorFillStyle)

#
nice_names = {}
nice_names["TTbar"] = "t#bar{t}"
nice_names["Fakes"] = "Non-Prompt"
nice_names["VVDF"]    = "Diboson (DF)"
nice_names["VVSF"]    = "Diboson (SF)"
nice_names["WW"]    = "WW"
nice_names["ST"]    = "tW + single-top"
nice_names["Wjets"] = "W+jets"
nice_names["Zjets"] = "Z+jets"
nice_names["WZ"]    = "WZ"
nice_names["ZZ"]    = "ZZ"
nice_names["DrellYan"] = "Drell-Yan"
nice_names["TTV"] = "t#bar{t}+V"
nice_names["Higgs"] = "Higgs"
for sam in all_samples :
    if "Data" in sam.name : continue
    entry = leg.AddEntry("", nice_names[sam.name], "lf")
    entry.SetLineColor(kBlack)
    entry.SetLineWidth(2)
    entry.SetFillColor(sam.color)
    entry.SetFillStyle(fillStyle)

tlx.tLegend = leg
c.Close()


#####################################################################
## SETUP "BACKGROUND-ONLY" FIT                                     ##
## SETUP "BACKGROUND-ONLY" FIT                                     ##
## SETUP "BACKGROUND-ONLY" FIT                                     ##
#####################################################################
if runOptions.doBackground() :
    userPrint("Setting up background-only fit config.")
    userPrint("Running background-only fit.")

#####################################################################
## SETUP "EXCLUSION" FIT                                           ##
## SETUP "EXCLUSION" FIT                                           ##
## SETUP "EXCLUSION" FIT                                           ##
#####################################################################
if runOptions.doExclusion() :
    userPrint("Setting up exclusion fit config.")

    signal_files = [ signal_file ]

    configMgr.runOnlyNominalXSec = not runOptions.doTheoryBand()

    signals = signalGrid.getSampleList() # returns list of <Grid>_mX_mY
    #userPrint(" !! Only running over first signal point !! ")
    ok_samples = ["250.0_160.0","225.0_135.0","300.0_180.0","300.0_150.0"]
    for s in signals :
        #use_this = False
        #for oksampk in ok_samples :
        #    if oksampk in s : use_this = True
        #if not use_this : continue
        #if "225" not in s : continue
        #if "135" not in s : continue
        #s_ = s.replace(".0", "")
        s_=s
        extlx = configMgr.addFitConfigClone(tlx, "Sig_%s"%s_) 

        userPrint(" > Adding signal sample to exclusion fit config : %s"%s)
   
        sigSample_ = Sample(s, kPink)
        sigSample_.setFileList(signal_files)
        sigSample_.setNormByTheory()
        sigSample_.setStatConfig( not runOptions.doSplitMCsys() )
        if runOptions.doSplitMCsys() :
            sigSample_.addSystematic( sysObj.mcstat_SIG )
        ## set the signal weight to be the weight with no PUPW
        sigSample_.weights = ["eventweightNOPUPW"]

        if runOptions.doTheoryBand() : ### TODO check if we need the configMgr setRunOnlyNominalXSec 
            sigXSSyst = Systematic("SigXSec", ["eventweightNOPUPW"], 1.07, 0.93, "user", "overallSys") ### TODO add xsec util to grab the uncertainties on xsec (rather than storing in tree)
            #sigXSSyst = Systematic("SigXSec", configMgr.weights, 1.07, 0.93, "user", "overallSys") ### TODO add xsec util to grab the uncertainties on xsec (rather than storing in tree)
            sigSample_.addSystematic(sigXSSyst)

        ## add systematics
        sigSample_ = addSys(sigSample_, False, sysObj, True)

        ## attach the signal strength
        sigSample_.setNormFactor('mu_SIG', 1., 0., 5.)

        extlx.addSamples(sigSample_)
        extlx.setSignalSample(sigSample_)
        #tlx.addSamples(sigSample_)
        #tlx.setSignalSample(sigSample_)
        

#####################################################################
## SETUP "DISCOVERY" FIT                                           ##
## SETUP "DISCOVERY" FIT                                           ##
## SETUP "DISCOVERY" FIT                                           ##
#####################################################################
if runOptions.doDiscovery() :
    userPrint("Setting up discovery fit")

    sr_bin = runOptions.getSignalRegion()
    if "SRwt" in sr_bin :
        userPrint("Attempting discovery fit with combined region '%s'! Exitting.")
        sys.exit()

    # add a single-bin region
    discoChannel = tlx.addChannel("cuts", [sr_bin], 1,0.5,1.5)
    discoChannel.addDiscoverySamples(["SIG"],[1.],[0.],[100.],[kRed])
    if runOptions.doSplitMCsys() :
        discoChannel.addSystematic(sysObj.mcstat_SIG)

        if "SRw_" in sr_bin or "SRt_" in sr_bin :
            discoChannel.getSample("TTbar").addSystematic( sysObj.SRwt_TTbar_THEORY )
            discoChannel.getSample("VVDF").addSystematic( sysObj.SRwt_VVDF_THEORY )
            discoChannel.getSample("VVSF").addSystematic( sysObj.SRwt_VVSF_THEORY)
    tlx.setSignalChannels(discoChannel)
