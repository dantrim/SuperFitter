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
myParser.add_option("--doExcl", action="store_true", dest="doExcl", default=False, help="Set exclusion fit")
myParser.add_option("--doDisco", action="store_true", dest="doDisco", default=False, help="Set discovery fit")
myParser.add_option("--doBkgOnly", action="store_true", dest="doBkgOnly", default=False, help="Set background-only fit")
(options, args) = myParser.parse_args(configMgr.userArg.strip('"').split())

channel_combine = True
channel_combine_suffix = "_ALL"


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
if str(options.signalRegion) not in regContainer.getDict().keys() :
    userPrint('SuperFitter LimitConfig ERROR    Requested signal region "%s" not supported. Check RegionDefs.buildRegions()!'%options.signalRegion)
    userPrint('SuperFitter LimitConfig ERROR    --> Exiting.')
    sys.exit()

runOptions.setCutDict(regContainer.getDict())
runOptions.setSignalRegion(options.signalRegion)

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
lumi_input  = 3.209
lumi_output = 3.209
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
hft_dir = "/data/uclhc/uci/user/dantrim/n0222val/SuperFitter/"

## data, ttbar, and ww file
data_file = hft_dir + "HFT_BG_13TeV.root"
mc_file   = hft_dir + "HFT_BG_13TeV.root"
signal_file = ""
if gridname == "bWN" : signal_file = hft_dir + "HFT_bWN_13TeV.root"
else : 
    userPrint('HFT not available for requested grid "%s"'%gridname)
    userPrint(' --> Exitting.')
    sys.exit()

## set the samples
#ttbar skip
ttbarSample = Sample("TTbar",   ROOT.TColor.GetColor("#FC0D1B"))
vvSample    = Sample("VV",      ROOT.TColor.GetColor("#41C1FC"))
#wwSample    = Sample("WW",      ROOT.TColor.GetColor("#41C1FC"))
stSample    = Sample("ST",      ROOT.TColor.GetColor("#DE080C")) 
wjetsSample = Sample("Wjets",   ROOT.TColor.GetColor("#5E9AD6")) 
zjetsSample = Sample("Zjets",   ROOT.TColor.GetColor("#82DE68"))
#wzSample    = Sample("WZ",      ROOT.TColor.GetColor("#F9F549")) 
#zzSample    = Sample("ZZ",      ROOT.TColor.GetColor("#FFEF53")) 
dataSample  = Sample("Data_CENTRAL", kBlack)

## attach samples to their files
#ttbar skip
#all_samples = [ vvSample, stSample, wjetsSample, zjetsSample, dataSample ]
all_samples = [ ttbarSample, vvSample, stSample, wjetsSample, zjetsSample, dataSample ]
#all_samples = [ ttbarSample, wwSample, stSample, wjetsSample, zjetsSample, wzSample, zzSample, dataSample ]
#ttbar skip
#samples     = [ vvSample, stSample, wjetsSample, zjetsSample, dataSample ]
samples     = [ ttbarSample, vvSample, stSample, wjetsSample, zjetsSample, dataSample ]
#samples     = [ ttbarSample, wwSample, stSample, wjetsSample, zjetsSample, wzSample, zzSample, dataSample ]
for s in samples :
    s.setFileList( [mc_file] )
    userPrint(" --> Sample : %s at %s"%(s.name, mc_file))

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
configMgr.blindSR = True
configMgr.blindCR = runOptions.doBlindCR()
configMgr.blindVR = runOptions.doBlindVR()

configMgr.fixSigXSec = runOptions.doTheoryBand()

configMgr.analysisName   = runOptions.getSignalRegion() + "_" + runOptions.getGrid()

add_suffix = ""
if channel_combine :
    add_suffx = channel_combine_suffix
    configMgr.analysisName = configMgr.analysisName + channel_combine_suffix

suffix = ""
if runOptions.getOutputSuffix() != "" :
    suffux += "_%s"%runOptions.getOutputSuffx()


configMgr.histCacheFile  = "data" + suffix + "/" + configMgr.analysisName + add_suffix + ".root"
configMgr.outputFileName = "results" + suffix + "/" + configMgr.analysisName + add_suffix + "_Output.root"

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
meas = tlx.addMeasurement(name="NormalMeasurement", lumi = 1., lumiErr = 0.001)
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
def addSys(sample, doSimFit, sysObject) :
    if doSimFit :

        #############################################################
        ## weight systematics
        #############################################################

        ## e-gamma
        sample.addSystematic(sysObject.AR_EL_EFF_ID_CR)
        sample.addSystematic(sysObject.AR_EL_EFF_Iso_CR)
        sample.addSystematic(sysObject.AR_EL_EFF_Reco_CR)

        ## muons
        sample.addSystematic(sysObject.AR_MUON_EFF_STAT_CR)
        sample.addSystematic(sysObject.AR_MUON_EFF_STAT_LOWPT_CR)
        sample.addSystematic(sysObject.AR_MUON_EFF_SYS_CR)
        sample.addSystematic(sysObject.AR_MUON_EFF_SYS_LOWPT_CR)
        sample.addSystematic(sysObject.AR_MUON_ISO_STAT_CR)
        sample.addSystematic(sysObject.AR_MUON_ISO_SYS_CR)

        ## jets
        sample.addSystematic(sysObject.AR_JET_JVTEff_CR)

        ## flavor tagging
        sample.addSystematic(sysObject.AR_FT_EFF_B_CR)
        sample.addSystematic(sysObject.AR_FT_EFF_C_CR)
        sample.addSystematic(sysObject.AR_FT_EFF_Light_CR)
        sample.addSystematic(sysObject.AR_FT_EFF_extrapolation_CR)
        sample.addSystematic(sysObject.AR_FT_EFF_extrapolation_charm_CR)

        #############################################################
        ## shape systematics
        #############################################################

        ## e-gamma
        sample.addSystematic(sysObject.AR_EG_RESOLUTION_ALL_CR)
        sample.addSystematic(sysObject.AR_EG_SCALE_ALL_CR)
        ## muons
        sample.addSystematic(sysObject.AR_MUONS_ID_CR)
        sample.addSystematic(sysObject.AR_MUONS_MS_CR)
        sample.addSystematic(sysObject.AR_MUONS_SCALE_CR)
        ## jets
        sample.addSystematic(sysObject.AR_JER_CR)
        sample.addSystematic(sysObject.AR_JET_GroupedNP_1_CR)
        ## met
        sample.addSystematic(sysObject.AR_MET_SoftTrk_ResoPara_CR)
        sample.addSystematic(sysObject.AR_MET_SoftTrk_ResoPerp_CR)
        sample.addSystematic(sysObject.AR_MET_SoftTrk_Scale_CR)
    else :

        #############################################################
        ## weight systematics
        #############################################################

        ## e-gamma
        sample.addSystematic(sysObject.AR_EL_EFF_ID_MC)
        sample.addSystematic(sysObject.AR_EL_EFF_Iso_MC)
        sample.addSystematic(sysObject.AR_EL_EFF_Reco_MC)

        ## muons
        sample.addSystematic(sysObject.AR_MUON_EFF_STAT_MC)
        sample.addSystematic(sysObject.AR_MUON_EFF_STAT_LOWPT_MC)
        sample.addSystematic(sysObject.AR_MUON_EFF_SYS_MC)
        sample.addSystematic(sysObject.AR_MUON_EFF_SYS_LOWPT_MC)
        sample.addSystematic(sysObject.AR_MUON_ISO_STAT_MC)
        sample.addSystematic(sysObject.AR_MUON_ISO_SYS_MC)

        ## jets
        sample.addSystematic(sysObject.AR_JET_JVTEff_MC)

        ## flavor tagging
        sample.addSystematic(sysObject.AR_FT_EFF_B_MC)
        sample.addSystematic(sysObject.AR_FT_EFF_C_MC)
        sample.addSystematic(sysObject.AR_FT_EFF_Light_MC)
        sample.addSystematic(sysObject.AR_FT_EFF_extrapolation_MC)
        sample.addSystematic(sysObject.AR_FT_EFF_extrapolation_charm_MC)

        #############################################################
        ## shape systematics
        #############################################################

        ## e-gamma
        sample.addSystematic(sysObject.AR_EG_RESOLUTION_ALL_MC)
        sample.addSystematic(sysObject.AR_EG_SCALE_ALL_MC)
        ## muons
        sample.addSystematic(sysObject.AR_MUONS_ID_MC)
        sample.addSystematic(sysObject.AR_MUONS_MS_MC)
        sample.addSystematic(sysObject.AR_MUONS_SCALE_MC)
        ## jets
        sample.addSystematic(sysObject.AR_JER_MC)
        sample.addSystematic(sysObject.AR_JET_GroupedNP_1_MC)
        ## met
        sample.addSystematic(sysObject.AR_MET_SoftTrk_ResoPara_MC)
        sample.addSystematic(sysObject.AR_MET_SoftTrk_ResoPerp_MC)
        sample.addSystematic(sysObject.AR_MET_SoftTrk_Scale_MC)

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
            if "SRw" in runOptions.getSignalRegion() or "SRt" in runOptions.getSignalRegion() :
                sample.setNormFactor("mu_TTbar", 1., 0., 10.)
                sample.setNormRegions([("CRTop", "cuts")])
        else : 
            sample.setNormByTheory() # i.e. use MC-only for normalization (no fitting, etc...)
    # ----------------------------------------------- #
    #  VV                                             #
    # ----------------------------------------------- #
    elif "VV" in sample.name :
        sample.setStatConfig( not runOptions.doSplitMCsys() )

        if runOptions.doSplitMCsys() :
            sample.addSystematic( sysObj.mcstat_VV )

        ## add systematics
        sample = addSys(sample, fitWW, sysObj)

        #sample.addSystematic( sysObj.dummySyst )
        if runOptions.doFitWW() :
            if "SRw" in runOptions.getSignalRegion() or "SRt" in runOptions.getSignalRegion() :
                sample.setNormFactor("mu_VV", 1., 0., 10.)
                sample.setNormRegions([("CRVV", "cuts")])
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
userPrint("Getting up the CR's.")
crList = RegionLists.getCRList(tlx, runOptions.getSignalRegion(), fitWW = runOptions.doFitWW(), fitTTbar = runOptions.doFitTTbar())
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
    if channel_combine :
        srList_a = RegionLists.getSRList(tlx, "cuts", "SRw_DF", 1., 0.5, 1.5)
        srList_b = RegionLists.getSRList(tlx, "cuts", "SRw_EE", 1., 0.5, 1.5) 
        srList_c = RegionLists.getSRList(tlx, "cuts", "SRw_MM", 1., 0.5, 1.5) 
        srList.append(srList_a[0])
        srList.append(srList_b[0])
        srList.append(srList_c[0])
    else : 
        srList = RegionLists.getSRList(tlx, "cuts", runOptions.getSignalRegion(), 1., 0.5, 1.5)

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
nice_names["VV"]    = "Diboson"
nice_names["WW"]    = "WW"
nice_names["ST"]    = "tW + single-top"
nice_names["Wjets"] = "W+jets"
nice_names["Zjets"] = "Z+jets"
nice_names["WZ"]    = "WZ"
nice_names["ZZ"]    = "ZZ"
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

    signals = signalGrid.getSampleList()
    userPrint(" !! Only running over first signal point !! ")
    for s in signals :
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

        if runOptions.doTheoryBand() : ### TODO check if we need the configMgr setRunOnlyNominalXSec 
            sigXSSyst = Systematic("SigXSec", configMgr.weights, 1.07, 0.93, "user", "overallSys") ### TODO add xsec util to grab the uncertainties on xsec (rather than storing in tree)
            sigSample_.addSystematic(sigXSSyst)

        ## add systematics
        sigSample_ = addSys(sigSample_, False, sysObj)

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
    userPrint("Discovery fit config not ready yet! Exitting.")
    sys.exit()
