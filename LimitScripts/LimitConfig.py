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
from ROOT import kBlack,kWhite,kGray,kRed,kPink,kMagenta,kViolet,kBlue,kAzure,kCyan,kTeal,kGreen,kSpring,kYellow,kOrange 
from ROOT import gROOT

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
import GridDefs # this is where the handling of the signal grid is performed

def userPrint(msg) :
    print "SuperFitter    %s"%msg

#####################################################################
### parse the user input
parser = OptionParser()
parser.add_option("-r", "--signalRegion", dest="signalRegion", default="")
parser.add_option("-g", "--sigGrid",   dest="sigGrid", default="")
parser.add_option("-t", "--doTheoryBand", action="store_true", dest="doTheoryBand", default=False)
parser.add_option("--doExcl", action="store_true", dest="doExcl", default=False, help="Set exclusion fit")
parser.add_option("--doDisco", action="store_true", dest="doDisco", default=False, help="Set discovery fit")
parser.add_option("--doBkgOnly", action="store_true", dest="doBkgOnly", default=False, help="Set background-only fit")
(options, args) = parser.parse_args()

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
if str(options.signalRegion) not in regContainer.getDict() :
    userPrint('SuperFitter LimitConfig ERROR    Requested signal region "%s" not supported. Check RegionDefs.buildRegions()!'%options.signalRegion)
    userPrint('SuperFitter LimitConfig ERROR    --> Exiting.')
    sys.exit()

runOptions.setCutDict(regContainer.getDict())
runOptions.setSignalRegion(options.signalRegion)

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
## do we want to run the theory XS band
doTheoryBand = options.doTheoryBand
runOptions.setTheoryBand(doTheoryBand)

#########################################
## configure input and output lumi
userPrint("Setting the luminosity.")
lumi_input  = 2.0
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
    s.setFileList( mc_file )
    userPrint(" --> Sample : %s at %s"%(s.name, mc_file))

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
## misc
userPrint("Setting the calculator type.")
# CalculatorType:       0:Frequentist   1:Hybrid    2:Asymptotic
runOptions.setCalculatorType(2)
# TestStatType:         0:LEP   1:Tevatron  2:Profile likelihood    3:One sided PL
runOptions.setTestStatType(3)
# Number of scan points when scanning over mu_SIG
runOptions.setNumberOfScanPoints(20)

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
configMgr.histCacheFile  = "data/" + configMgr.analysisName + ".root"
configMgr.outputFileName = "results/" + configMgr.analysisName + "_Output.root"

configMgr.inputLumi = runOptions.getInputLumi()
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
######################################################################
## configure the backgrounds/samples
userPrint("Configuring the samples.")
#for sample in all_samples :
#    # ----------------------------------------------- #
#    #  TTbar                                          #
#    # ----------------------------------------------- #
#    if sample.name == "TTbar" 


#####################################################################
## SETUP "BACKGROUND-ONLY" FIT                                     ##
## SETUP "BACKGROUND-ONLY" FIT                                     ##
## SETUP "BACKGROUND-ONLY" FIT                                     ##
#####################################################################


#####################################################################
## SETUP "DISCOVERY" FIT                                           ##
## SETUP "DISCOVERY" FIT                                           ##
## SETUP "DISCOVERY" FIT                                           ##
#####################################################################

#####################################################################
## SETUP "EXCLUSION" FIT                                           ##
## SETUP "EXCLUSION" FIT                                           ##
## SETUP "EXCLUSION" FIT                                           ##
#####################################################################
