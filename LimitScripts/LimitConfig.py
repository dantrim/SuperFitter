#!/usr/bin python
"""
###################################################
## SuperFitter                                   ##
##                                               ##
##          HistFitter configuration             ##
##                                               ##
##           https://xkcd.com/882/               ##
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

verbose = True # hardcode this for now

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

runOptions.setFitWW(False)
runOptions.setFitTTbar(True)

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

##

##########################################
## do we want to run the theory XS band (dashed-red lines)
doTheoryBand = options.doTheoryBand
runOptions.setTheoryBand(doTheoryBand)

#########################################
## configure input and output lumi
userPrint("Setting the luminosity.")
lumi_input  = 0.0783
lumi_output = 2.0
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
hft_dir = "/gdata/atlas/dantrim/SusyAna/n0213val/SuperFitter/"

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
ttbarSample = Sample("TTbar",   ROOT.TColor.GetColor("#FC0D1B"))
wwSample    = Sample("WW",      ROOT.TColor.GetColor("#41C1FC"))
dataSample  = Sample("Data_CENTRAL", kBlack)

## attach samples to their files
all_samples = [ ttbarSample, wwSample, dataSample ]
samples = [ ttbarSample, wwSample, dataSample ]
for s in samples :
    s.setFileList( [mc_file] )
    userPrint(" --> Sample : %s at %s"%(s.name, mc_file))


##########################################
## split MC sys --> need to look this one up again
runOptions.setSplitMCsys(True)

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
configMgr.blindCR = runOptions.doBlindCR()
configMgr.blindVR = runOptions.doBlindVR()

configMgr.fixSigXSec = runOptions.doTheoryBand()

configMgr.analysisName   = runOptions.getSignalRegion() + "_" + runOptions.getGrid()
suffix = ""
if runOptions.getOutputSuffix() != "" :
    suffux += "_%s"%runOptions.getOutputSuffx()
configMgr.histCacheFile  = "data" + suffix + "/" + configMgr.analysisName + ".root"
configMgr.outputFileName = "results" + suffix + "/" + configMgr.analysisName + "_Output.root"

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
tlx = configMgr.addFitConfig("TopLvlXML")
meas = tlx.addMeasurement(name="NormalMeasurement", lumi = 1., lumiErr = 0.028)
meas.addPOI("mu_SIG")

tlx.statErrThreshold = 0.001

######################################################################
## set up the systematic object
userPrint("Setting up the SystematicObject.")
sysObj = SystematicObject.SystematicObject(configMgr, runOptions.doSplitMCsys())

######################################################################
## configure the backgrounds/samples
userPrint("Configuring the samples.")

for sample in all_samples :
    print sample.name
    # ----------------------------------------------- #
    #  TTbar                                          #
    # ----------------------------------------------- #
    if "TTbar" in sample.name :
        print "TTBAR IN SAMPLE NAME"
        sample.setStatConfig( not runOptions.doSplitMCsys() )

        if runOptions.doSplitMCsys() :
            print "TTBAR SPLIT MCSYS"
            sample.addSystematic( sysObj.mcstat_TTbar )

        sample.addSystematic( sysObj.dummySyst )
        if runOptions.doFitTTbar() :
            print "TTBAR DO FITTABAR"
            if runOptions.getSignalRegion() == "SR4" or runOptions.getSignalRegion() == "SRz" :
                sample.setNormFactor("mu_TTbar", 1., 0., 10.)
            if runOptions.getSignalRegion() == "SR4" or runOptions.getSignalRegion() == "SRz" :
             sample.setNormRegions([("CR", "cuts")])

        else : 
            sample.setNormByTheory() # i.e. use MC-only for normalization (no fitting, etc...)

    # ----------------------------------------------- #
    #  WW                                             #
    # ----------------------------------------------- #
    elif "WW" in sample.name :
        sample.setStatConfig( not runOptions.doSplitMCsys() ) 

        if runOptions.doSplitMCsys() :
            sample.addSystematic( sysObj.mcstat_WW )

        sample.addSystematic( sysObj.dummySyst )
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
crList = RegionLists.getCRList(tlx, runOptions.getSignalRegion(), fitWW = False, fitTTbar = True)
if runOptions.doFitTTbar() or runOptions.doFitWW() :
    tlx.setBkgConstrainChannels(crList)

for sam in all_samples :
    print " REG : ", configMgr.normList

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

    srList = RegionLists.getSRList(tlx, "cuts", runOptions.getSignalRegion(), 1., 0.5, 1.5)
    if runOptions.doExclusion() :
        tlx.setSignalChannels(srList)
    elif runOptions.doBackground() :
        tlx.setValidationChannels(srList)
        

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
nice_names["WW"]    = "WW"
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

#####################################################################
## SETUP "EXCLUSION" FIT                                           ##
## SETUP "EXCLUSION" FIT                                           ##
## SETUP "EXCLUSION" FIT                                           ##
#####################################################################
if runOptions.doExclusion() :
    userPrint("Exclusion fit config not ready yet! Exitting.")
    sys.exit()


#####################################################################
## SETUP "DISCOVERY" FIT                                           ##
## SETUP "DISCOVERY" FIT                                           ##
## SETUP "DISCOVERY" FIT                                           ##
#####################################################################
if runOptions.doDiscovery() :
    userPrint("Discovery fit config not ready yet! Exitting.")
    sys.exit()
