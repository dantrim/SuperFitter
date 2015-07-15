
#############################################################
# In order to better undersatnd what is being set in the 2L #
# config script written by Geraldine and Pascal, I am going #
# to rewrite parts making it more modular and maybe more    #
# transparent.  Maybe this will make it easier for next     #
# analyzer that needs to run limits...  Maybe not :)        #
# --------------------------------------------------------- #
# Author: Matt Relich                                       #
# Created: 24/07/2013                                       #
#############################################################

#--------------------------------------------------------#
# Import useful python things
#--------------------------------------------------------#

import sys, os
from configManager import configMgr # This is the guy we will configure
from ROOT import kBlack,kWhite,kGray,kRed,kPink,kMagenta,kViolet,kBlue,kAzure,kCyan,kTeal,kGreen,kSpring,kYellow,kOrange,kDashed
from ROOT import TCanvas,TLegend,TLegendEntry
from configWriter import TopLevelXML,Measurement,ChannelXML,Sample
from systematic import Systematic
from math import sqrt
from ROOT import gROOT

# Load Atlas style
gROOT.LoadMacro("./macros/AtlasStyle.C")
import ROOT
ROOT.SetAtlasStyle()

# User defined Modules
#sys.path.append("./modules")
sys.path.append("./LimitScripts")
from ConfigDefs import *
from RuntimeOptions import *
from SelectionConfig import *
from SystematicObject import *
from SetSimultaneousFitOptions import *

#--------------------------------------------------------#
# User will specify the options in this region
#--------------------------------------------------------#

# Now utilize the inputs from the command line.  This will
# be strictly enforced. User must give:
# 1.) Signal region
# 2.) Channel
# 3.) The grid to consider

SignalRegionChoices = ["SR1","SR2a","SR2b","SR4a","SR4b","SR4c",
                       "Super0a","Super0b","Super0c",
                       "Super1a","Super1b","Super1c"]
ChannelChoices      = ["all","ee","mm","em","tot", "sf"]
GridChoices         = ["SMCwslep","SMCwslep0","SMCwslep1","SMCwslep2","SMCwslep3","SMCwslep4","SMCwslep5","SMCwslep6",
                       "DLiSlep0","DLiSlep1","DLiSlep2","DLiSlep3","DLiSlep4","DLiSlep5",
                       "DLiSlep6","DLiSlep7","DLiSlep8","DLiSlep9",
                       "SparseDLiSlep0","SparseDLiSlep1","SparseDLiSlep2","SparseDLiSlep3",
                       "SparseDLiSlep4","SparseDLiSlep5","SparseDLiSlep6","SparseDLiSlep7",
                       "SparseDLiSlep8","SparseDLiSlep9","SparseDLiSlep10","SparseDLiSlep11",
                       "SparseDLiSlep12","SparseDLiSlep13"]                       
SysChoices          = ["NoSys","up","down"]
HandednessChoices   = ["RandL","LOnly","ROnly"]

inputs = sys.argv
_signalRegion = ""
_channel      = ""
_grid         = ""
_sigUncert    = ""
_handedness   = "" # Only needed when running slepton limits

for inp in inputs:
    if inp in SignalRegionChoices: _signalRegion = inp
    elif inp in ChannelChoices:    _channel      = inp
    elif inp in GridChoices:       _grid         = inp
    elif inp in SysChoices:        _sigUncert    = inp
    elif inp in HandednessChoices: _handedness   = inp


if _signalRegion == "":
    print "Signal region not found in inputs"
    print inputs
    sys.exit()

if _channel == "":
    print "Channel not found in inputs"
    print inputs
    sys.exit()

if _grid == "":
    print "Grid not found in inputs"
    print inputs
    sys.exit()

if _sigUncert == "":
    print "Signal uncertainty not found in inputs"
    print inputs
    sys.exit()

if _handedness == "" and "DLiSlep" in _grid:
    print "Didn't specify handedness for slepton limits"
    print "Assuming RH+LH limit"
    _handedness = "RandL"
    

print "---------------------------------------------"
print "Signal region: ",_signalRegion
print "Channel:       ",_channel
print "Grid:          ",_grid
print "Uncert:        ",_sigUncert
print "Handedness:    ",_handedness
print "---------------------------------------------"
print


# The input files with full path
#indir      = "/gdata/atlas/mrelich/limit/SusyLimit/inputs_20130731/"
#indir      = "/gdata/atlas/mrelich/limit/SusyLimit/inputs_20130816/"
#indirFake  = "/gdata/atlas/dantrim/SuperHistFitter_01/TAnalysis/output/F0_Oct_22/Processed_razor/"
#indirData   = "/gdata/atlas/dantrim/SuperHistFitter_00/TAnalysis/output/R8_Oct_7/Processed/"
#indirData   = "/gdata/atlas/dantrim/SusyAna/histoAna/TAnaOutput/R8_Oct_7/Processed/"
#indirBkg   = "/gdata/atlas/dantrim/SuperHistFitter_00/TAnalysis/output/R8_Oct_7/Processed/"

# MC directory for WW, ZV, Higgs
indirMC     = "/gdata/atlas/dantrim/SusyAna/histoAna/TAnaOutput/R8_Oct_7/Processed/"
# MC directory for higher stat Top  
indirTop    = "/gdata/atlas/dantrim/SusyAna/histoAna/TAnaOutput/top/T0_Dec2/Processed/"
# MC directory for higher stat Z+jets
indirZjets  = "/gdata/atlas/dantrim/SusyAna/histoAna/TAnaOutput/zjets/Z0_hightstats/Processed/"
# MC directory for SMCwslep signal samples
indirSig    = "/gdata/atlas/dantrim/SusyAna/histoAna/TAnaOutput/SMCwslep/S0_Dec2/Processed/"
# Directory for Data samples
indirData   = "/gdata/atlas/dantrim/SusyAna/histoAna/TAnaOutput/R8_Oct_7/Processed/"
# Directory for fake ntuples
indirFake   = "/gdata/atlas/dantrim/SusyAna/histoAna/TAnaOutput/fakes/F1_Dec3/razor/Processed/"

# file holding WW, ZV, and Higgs samples
bkgFile    = indirMC + "HFT_BG8TeV.root"
# file holding Top sample
#topFile    = indirTop + "top_105861.root"
topFile    = indirTop + "top_117050_af2.root"
# file holding Z+jets sample
zjetsFile  = indirZjets + "zjets_upstats.root"
# file holding Data sample
dataFile   = indirData + "HFT_BG8TeV.root"
# file holding fake ntuple
fakeFile   = indirFake + "fakes_Dec3Matrix_razor.root"


# Need a catch for the signal files
signalFile = ""
if "SMCwslep" in _grid:
    signalFile = indirSig + "HFT_SMCwslep8TeV.root"

if "DLiSlep" in _grid:
    signalFile = indir + "HFT_DLiSlep8TeV.root"

if signalFile == "": sys.exit()


# Specify Analysis name. This will be used to identify
# the results of the run in the results directory
#analysisName = "SR4c_pass1"
analysisName = _signalRegion+"_"+_channel+"_"+_grid

# Creat user defs instance
userDefs = ConfigDefs()

# Get the channel enum
# Let default be all
_ch = userDefs.all 
if _channel in "ee":  _ch = userDefs.ee
if _channel in "mm":  _ch = userDefs.mm
if _channel in "em":  _ch = userDefs.em
if _channel in "tot": _ch = userDefs.tot
if _channel in "sf" : _ch = userDefs.sf

# Specify what backgrounds to fit
fitWW  =        True 
fitTop =        True 
fitZV  =        True 
#if _channel == "em": fitZV = False

# Set slepton handedness based on command
# line options
_sleptonHand = userDefs.RightLeftHand
if _handedness == "LOnly":
    _sleptonHand = userDefs.LeftHandOnly
    analysisName += _handedness
if _handedness == "ROnly":
    _sleptonHand = userDefs.RightHandOnly
    analysisName += _handedness

# Initialize Runtime Options
userOpts = RuntimeOptions(True,                     # do2Lep
                          False,                    # doToys
                          "",                       # specify grid for toys
                          1000,                     # specify number of toys
                          False,                     # doExclusion
                          True,                    # doDiscovery
                          False,                    # doValidation
                          False,                    # doShapeFit
                          fitWW,                    # doSimFitWW
                          fitTop,                   # doSimFitTop
                          fitZV,                    # doSimFitZV
                          True,                     # split MC sys to individual samples (?)
                          False,                     # Blind SR
                          False,                    # Blind CR
                          True,                     # Blind VR
                          _sigUncert,               # Specify uncertainty
                          _grid,                    # Specify grid
                          _signalRegion,            # Specify the signal region
                          _ch,                      # Lepton Channel
                          _sleptonHand,             # Slepton Handedness to consider
                          bkgFile,                  # input bkg file
                          dataFile,                 # input data file   // dantrim
                          signalFile,               # input signal file
                          analysisName,             # Analysis Name for saving
                          20.3,                     # Input Lumi units
                          20.3,                     # Ouput Lumi units
                          "fb-1"                    # Input Lumi units
                          )


# Specify the samples to consider and use the correct names
# corresponding to your input trees
zxSample    = Sample("Zjets"       , kGreen+2)
fakeSample  = Sample("Fake"       , kGray)
higgsSample = Sample("Higgs"       , kYellow)
zvSample    = Sample("ZV"          , kGreen)
topSample   = Sample("Top"        , kViolet)
wwSample    = Sample("WW"          , kAzure-4)
dataSample  = Sample("Data_CENTRAL", kBlack)

#mcSamples  = [zxSample, higgsSample, zvSample, topSample, wwSample, dataSample]
##mcSamples  = [higgsSample, zvSample, wwSample, dataSample]

#bkgFiles  = []
#if userOpts.do2L:
#    bkgFiles.append( userOpts.bkgFile )
#for sample in mcSamples :
#    sample.setFileList(bkgFiles)



#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#                                 USER SHOULD NOT HAVE TO EDIT BELOW HERE                                    #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

#--------------------------------------------------------#
# maybe useful methods used below
#--------------------------------------------------------#
def userPrint(message):
    print "\tUSER MESSAGE: " + message
    return


#--------------------------------------------------------#
# Setup the various configurations
#--------------------------------------------------------#


##
## Toys Vs. Asymtoptic
##
# Serhan gave some comments as to what the following are:
# testStatType   => Test statistic type, 0: LEP,  1: Tevatron, 2: Profile likelihood, 3: One sided PL
# calculatorType => Calculator type      0: Freq., 1: Hybrid,   2: Asymptotic
# nPoints        => Number of scan points for the POI if the interval is fixed

userPrint("Setting up toys vs. Asymptotic options")

configMgr.nTOYS = userOpts.nToys
toyindex        = 2 # ???

if not userOpts.doToys:
    configMgr.calculatorType = 2 # useing 2 for asymptotic,
else:
    configMgr.calculatorType = 0 # using 0 for toys

# These are not clear to me what they mean
# copying from Geralidine
configMgr.testStatType = 3
configMgr.nPoints      = 20
configMgr.writeXML     = True # TODO make configurable

##
## Specify the Fit Mode
##
userPrint("Specifying the fit mode")

if userOpts.doDiscovery: configMgr.doExclusion = False
if userOpts.doExclusion: configMgr.doExclusion = True

# Check to make sure we are not doing validation
# and exclusion.  Only can do one, give preference
# to exclusion
if userOpts.doValidation and userOpts.doExclusion:
    print "Can't do validation and Exclusion, setting validation to false"
    userOpts.doValidation = False

##
## Specify output files 
##
userPrint("Specifying the output files for HistFitter")

# Specify ananame
if userOpts.do2L:
    configMgr.analysisName = userOpts.anaName + "_" + userOpts.sigUncert

# Specify where hist will be sent
configMgr.histCacheFile = "data/" + configMgr.analysisName + ".root"

# Specify the output file based on whether we do toys or not
if not userOpts.doToys:
    configMgr.outputFileName = "results/"+configMgr.analysisName+"_Output.root"
else:
    configMgr.outputFileName = "results/"+configMgr.analysisName+"_"+userOpts.gridForToys+"_withToys"+userOpts.sigUncert+"_"+userOpts.signalRegion+"_"+str(toyindex)+"_Output.root"

##
## Set the luminosity
##

userPrint("Specifying Luminosity")

configMgr.inputLumi  = userOpts.inputLumi
configMgr.outputLumi = userOpts.outputLumi
configMgr.setLumiUnits( userOpts.lumiUnits )


##
## Specify the background input files
##

userPrint("Specifying background input")

#mcSamples  = [zxSample, higgsSample, zvSample, topSample, wwSample, dataSample]
mcSamples  = [higgsSample, zvSample, wwSample, dataSample]

bkgFiles   = []
topFiles   = []
zjetsFiles = []

if userOpts.do2L:
    bkgFiles.append( userOpts.bkgFile )
    topFiles.append( topFile )
    zjetsFiles.append( zjetsFile )

for sample in mcSamples :
    # assign higgs, zv, ww, and data to HFT_BG8TeV
    sample.setFileList(bkgFiles)

# assign top and zjets to their specific files
topSample.setFileList(topFiles)
zxSample.setFileList(zjetsFiles)

#bkgFiles  = []
#if userOpts.do2L:
#    bkgFiles.append( userOpts.bkgFile )
#
#configMgr.setFileList( bkgFiles )


#dataSample.setFileList( [userOpts.dataFile] )     # dantrim -- separate dataSample since this data file also contains MC

##
## Configure the selection
##
userPrint("Configuring selection")

configMgr = selectionConfig(configMgr,userOpts.slepLimitN)

##
## Configure weight
##
userPrint("Specifying Weight")

if userOpts.do2L:
    configMgr.weights = ["eventweight"]


##
## Setup the systematics
##
userPrint("Configuring Systematic")

# Add all sys to SystematicObject
# where you can access the systematics
# through this object when initializing
# the backgrounds
sysObj = SystematicObject(configMgr, userOpts.doShape, userOpts.splitMCSys)
configMgr.nomName = "_CENTRAL"

##
## Setting up Samples and normalization factors
##
userPrint("Setting up samples and norm factors")

# Specify the paramater of interest
tlx = configMgr.addFitConfig("TopLvlXML")
meas = tlx.addMeasurement(name="NormalMeasurement",lumi=1.,lumiErr=0.028)
meas.addPOI("mu_SIG")  ## EXCL:mu_SIG, upper limit table

# Determine if we should use stat
useStat = True
if userOpts.splitMCSys:
    useStat = False

# If using stat set some limits
tlx.statErrThreshold = 0.001

# Now specify the samples based on if 2lep is set
# I am beginning to think the flag is useless?

# Define two quantities useful for configuring
# the signal region systematics and normalization
SR      = userOpts.signalRegion
lepChan = userOpts.leptonChannel 

# Write a simple function to add systematics to a sample
# it seems that most of them have the same systematics.
# For generator sys, we can add them on individually
# for the relevant samples
def addSys(sample, doSimFit, sysObj):
    if doSimFit:
        sample.addSystematic(sysObj.AR_all_JES_CR)
        sample.addSystematic(sysObj.AR_all_JER_CR)
#        sample.addSystematic(sysObj.AR_all_JVF_CR)   ####
        sample.addSystematic(sysObj.AR_all_TES_CR)
        sample.addSystematic(sysObj.AR_all_BJET_CR)
        sample.addSystematic(sysObj.AR_all_CJET_CR)
        sample.addSystematic(sysObj.AR_all_BMISTAG_CR)
        sample.addSystematic(sysObj.AR_all_EER_CR)
        sample.addSystematic(sysObj.AR_all_EESLOW_CR)
        sample.addSystematic(sysObj.AR_all_EESMAT_CR)
        sample.addSystematic(sysObj.AR_all_EESPS_CR)
        sample.addSystematic(sysObj.AR_all_EESZ_CR)
        sample.addSystematic(sysObj.AR_all_ESF_CR)
        sample.addSystematic(sysObj.AR_all_MID_CR)
        sample.addSystematic(sysObj.AR_all_MMS_CR)
        sample.addSystematic(sysObj.AR_all_MEFF_CR)
        sample.addSystematic(sysObj.AR_all_RESOST_CR)
        sample.addSystematic(sysObj.AR_all_SCALEST_CR)
        sample.addSystematic(sysObj.AR_all_PILEUP_CR)  ####
        sample.addSystematic(sysObj.AR_all_TRIGGERE_CR)
        sample.addSystematic(sysObj.AR_all_TRIGGERM_CR)
    else:
        sample.addSystematic(sysObj.AR_all_JES_MC)
        sample.addSystematic(sysObj.AR_all_JER_MC)
#        sample.addSystematic(sysObj.AR_all_JVF_MC)               ####
        sample.addSystematic(sysObj.AR_all_TES_MC)
        sample.addSystematic(sysObj.AR_all_BJET_MC)
        sample.addSystematic(sysObj.AR_all_CJET_MC)
        sample.addSystematic(sysObj.AR_all_BMISTAG_MC)
        sample.addSystematic(sysObj.AR_all_EER_MC)
        sample.addSystematic(sysObj.AR_all_EESLOW_MC)
        sample.addSystematic(sysObj.AR_all_EESMAT_MC)
        sample.addSystematic(sysObj.AR_all_EESPS_MC)
        sample.addSystematic(sysObj.AR_all_EESZ_MC)
        sample.addSystematic(sysObj.AR_all_ESF_MC)
        sample.addSystematic(sysObj.AR_all_MID_MC)
        sample.addSystematic(sysObj.AR_all_MMS_MC)
        sample.addSystematic(sysObj.AR_all_MEFF_MC)
        sample.addSystematic(sysObj.AR_all_RESOST_MC)
        sample.addSystematic(sysObj.AR_all_SCALEST_MC)
        sample.addSystematic(sysObj.AR_all_PILEUP_MC)                   ####
        sample.addSystematic(sysObj.AR_all_TRIGGERE_MC)
        sample.addSystematic(sysObj.AR_all_TRIGGERM_MC)

    # return the updated sample
    return sample


if userOpts.do2L:

    
    #------------------------------------------------#
    #                   ZX SAMPLE                    #
    #------------------------------------------------#

    zxSample.setStatConfig(useStat)
    if userOpts.splitMCSys:
        zxSample.addSystematic(sysObj.AR_mcstat_ZX)
    zxSample.setNormByTheory()
    zxSample = addSys(zxSample, False, sysObj)

    #------------------------------------------------#
    #                     FAKES                      #
    #------------------------------------------------#
    # As we don't have the final fake estimates, use the preliminary results per region
    # and take negative yields to be 0.1 (we expect the fake to not contribute so we take
    # this small value and use the relative uncertainty of stat+syst to cover our asses)
    fakeSample.buildHisto([0.24],   "eeSuper0a",  "cuts")
    fakeSample.buildHisto([0.1],   "mmSuper0a",  "cuts")
    fakeSample.buildHisto([0.37],   "emSuper0a",  "cuts")
    fakeSample.buildHisto([0.1],   "eeSuper0b",  "cuts")
    fakeSample.buildHisto([0.1],   "mmSuper0b",  "cuts")
    fakeSample.buildHisto([0.1],   "emSuper0b",  "cuts")
    fakeSample.buildHisto([0.02],  "eeSuper0c",  "cuts")
    fakeSample.buildHisto([0.1],   "mmSuper0c",  "cuts")
    fakeSample.buildHisto([0.1],   "emSuper0c",  "cuts")
    fakeSample.buildHisto([3.85],  "eeSuper1a",  "cuts")
    fakeSample.buildHisto([8.09],  "mmSuper1a",  "cuts")
    fakeSample.buildHisto([5.76],  "emSuper1a",  "cuts")
    fakeSample.buildHisto([0.65],  "eeSuper1b",  "cuts")
    fakeSample.buildHisto([0.09],   "mmSuper1b",  "cuts")
    fakeSample.buildHisto([0.64],  "emSuper1b",  "cuts")
    fakeSample.buildHisto([1.88],  "eeSuper1c",  "cuts")
    fakeSample.buildHisto([8.12],  "mmSuper1c",  "cuts")
    fakeSample.buildHisto([2.82],  "emSuper1c",  "cuts")
    fakeSample.buildHisto([84.95], "emCRTop14a", "cuts")
    fakeSample.buildHisto([12.35],  "emCRTop14b", "cuts")
    fakeSample.buildHisto([60.87], "emCRWW14a",  "cuts")
    fakeSample.buildHisto([53.22], "emCRWW14b",  "cuts")
    fakeSample.buildHisto([0.1],   "emCRZV14a",  "cuts")
    fakeSample.buildHisto([0.1],   "emCRZV14b",  "cuts")
    #sf
    fakeSample.buildHisto([0.34],   "sfSuper0a",  "cuts")
    fakeSample.buildHisto([0.2],    "sfSuper0b",  "cuts")
    fakeSample.buildHisto([0.12],   "sfSuper0c",  "cuts")
    fakeSample.buildHisto([11.94],  "sfSuper1a",  "cuts")
    fakeSample.buildHisto([0.74],   "sfSuper1b",  "cuts")
    fakeSample.buildHisto([10.0],   "sfSuper1c",  "cuts")

    fakeSample.setStatConfig(useStat)
    fakeSample.setNormByTheory()

    
#    fakeSample.setFileList([fakeFile])
#    fakeSample.setStatConfig(useStat)
#    if userOpts.splitMCSys:
#        fakeSample.addSystematic(sysObj.AR_mcstat_FAKE)
#    fakeSample.setNormByTheory()
#    fakeSample.addSystematic(sysObj.AR_fakes_ELFR)
#    fakeSample.addSystematic(sysObj.AR_fakes_ELRE)
#    fakeSample.addSystematic(sysObj.AR_fakes_MUFR)
#    fakeSample.addSystematic(sysObj.AR_fakes_MURE)


    #------------------------------------------------#
    #                     HIGGS                      #
    #------------------------------------------------#

    higgsSample.setStatConfig(useStat)
    if userOpts.splitMCSys:
        higgsSample.addSystematic(sysObj.AR_mcstat_H)
    higgsSample.setNormByTheory()  
    higgsSample = addSys(higgsSample, False, sysObj)


    #------------------------------------------------#
    #                      ZV                        #
    #------------------------------------------------#

    zvSample.setStatConfig(useStat)
    if userOpts.splitMCSys:
        zvSample.addSystematic(sysObj.AR_mcstat_ZV)

    # Determine the normalization region
    # This should be done only if we fit
    # Regardless of channel combined ee+mm
    if 'SR1' in SR and userOpts.doSimFit2LZV:
        zvSample.setNormRegions([("emZVCRmet","cuts")])  

    if 'SR2a' in SR and userOpts.doSimFit2LZV:
        zvSample.setNormRegions([("emZVCRmt2a","cuts")])

    if 'SR2b' in SR and userOpts.doSimFit2LZV:
        zvSample.setNormRegions([("emZVCRmt2a","cuts")])

    if 'SR4a' in SR and userOpts.doSimFit2LZV:
        zvSample.setNormRegions([("emZVCRmt2a","cuts")])

    if 'SR4b' in SR and userOpts.doSimFit2LZV:
        zvSample.setNormRegions([("emZVCRmt2a","cuts")])

    if 'SR4c' in SR and userOpts.doSimFit2LZV:
        zvSample.setNormRegions([("emZVCRmt2a","cuts")])
    if userOpts.doSimFit2LZV:
        if('Super0a' in SR or 'Super0b' in SR or 'Super0c' in SR):
            zvSample.setNormRegions([("emCRZV14a","cuts")])
        elif('Super1a' in SR or 'Super1b' in SR or 'Super1c' in SR):
            zvSample.setNormRegions([("emCRZV14b","cuts")])

    # Add Systematics
    zvSample = addSys(zvSample, userOpts.doSimFit2LZV, sysObj)

    # Additional ZV Specific systematics
    if userOpts.doSimFit2LZV:
        #zvSample.addSystematic(sysObj.AR_all_GENZV)
        #zvSample.addSystematic(sysObj.AR_all_SCALEZV)
        #zvSample.addSystematic(sysObj.AR_all_SHOWERZV)
        #zvSample.addSystematic(sysObj.AR_all_PDFZV)

        # Specify where to take the normalization if
        # we are doing the simultaneous fit
        if 'SR1' in SR:
            zvSample.setNormFactor("mu_2LZV1",1.,0.,10.)
        elif('SR2a' in SR or 'SR2b' in SR or 'SR4a' in SR or 'SR4b' in SR or 'SR4c' in SR):
            zvSample.setNormFactor("mu_2LZV2a",1.,0.,10.)
        elif userOpts.doSimFit2LZV and 'SR5a' in SR:
            zvSample.setNormFactor("mu_2LZV5a",1.,0.,10.)
        elif('Super0a' in SR or 'Super0b' in SR or 'Super0c' in SR):
            zvSample.setNormFactor("mu_ZV14a",1.,0.,10.)
        elif('Super1a' in SR or 'Super1b' in SR or 'Super1c' in SR):
            zvSample.setNormFactor("mu_ZV14b",1.,0.,10.)
    else:	
        zvSample.setNormByTheory()
        #zvSample.addSystematic(sysObj.AR_all_GENZV)
        #zvSample.addSystematic(sysObj.AR_all_SCALEZV)
        #zvSample.addSystematic(sysObj.AR_all_SHOWERZV)
        #zvSample.addSystematic(sysObj.AR_all_PDFZV)		

    # Add in the gen systematic based on the signal region
    ##if 'SR1' in SR:    zvSample.addSystematic(sysObj.SRWWa_ZV_THEORY)
    ##elif 'SR2a' in SR: zvSample.addSystematic(sysObj.SRWWb_ZV_THEORY)
    ##elif 'SR2b' in SR: zvSample.addSystematic(sysObj.SRWWc_ZV_THEORY)
    ##elif 'SR4a' in SR: zvSample.addSystematic(sysObj.SRmT2a_ZV_THEORY)
    ##elif 'SR4b' in SR: zvSample.addSystematic(sysObj.SRmT2b_ZV_THEORY)
    ##elif 'SR4c' in SR: zvSample.addSystematic(sysObj.SRmT2c_ZV_THEORY)

#    if   'Super0a' in SR :      zvSample.addSystematic(sysObj.SR0a_ZV_THEORY)
#    elif 'Super0b' in SR :      zvSample.addSystematic(sysObj.SR0b_ZV_THEORY)
#    elif 'Super0c' in SR :      zvSample.addSystematic(sysObj.SR0c_ZV_THEORY)
#    elif 'Super1a' in SR :      zvSample.addSystematic(sysObj.SR1a_ZV_THEORY)
#    elif 'Super1b' in SR :      zvSample.addSystematic(sysObj.SR1b_ZV_THEORY)
#    elif 'Super1c' in SR :      zvSample.addSystematic(sysObj.SR1c_ZV_THEORY)

    #------------------------------------------------#
    #                     TOP                        #
    #------------------------------------------------#
    topSample.setStatConfig(useStat)
    if userOpts.splitMCSys:
        topSample.addSystematic(sysObj.AR_mcstat_TOP)

    
    # Determine the normalization regions
    # This should be done only if we fit
    if 'SR1' in SR and userOpts.doSimFit2LTop:
        topSample.setNormRegions([("emTopCRmet","cuts")])        ## Regarless of channel, always fit in em 
    if ('SR2a' in SR or 'SR2b' in SR or 'SR4a' in SR or 'SR4b' in SR or 'SR4c' in SR) and userOpts.doSimFit2LTop :
        topSample.setNormRegions([("emTopCRmt2","cuts")])        ## Regarless of channel, always fit in em
    if 'SR5a' in SR :
        if lepChan==userDefs.all or lepChan==userDefs.ee or lepChan==userDefs.eemm :
            topSample.setNormRegions([("eeTopCRZjets","cuts")])
        if lepChan==userDefs.all or lepChan==userDefs.mm or lepChan==userDefs.eemm :
            topSample.setNormRegions([("mmTopCRZjets","cuts")])
    if userOpts.doSimFit2LTop :
        if('Super0a' in SR or 'Super0b' in SR or 'Super0c' in SR):
            topSample.setNormRegions([("emCRTop14a","cuts")])
        elif('Super1a' in SR or 'Super1b' in SR or 'Super1c' in SR):
            topSample.setNormRegions([("emCRTop14b","cuts")])

    # Set the systematics
    topSample = addSys(topSample, userOpts.doSimFit2LTop, sysObj)

    # Add in additional top systematics and
    # specify the normative factors
    if userOpts.doSimFit2LTop:
	#topSample.addSystematic(sysObj.AR_all_GENTop)
        #topSample.addSystematic(sysObj.AR_all_SCALETop)
        #topSample.addSystematic(sysObj.AR_all_SHOWERTop)
        #topSample.addSystematic(sysObj.AR_all_IFSRTop)

        if 'SR1' in SR:
            topSample.setNormFactor("mu_2LTop1",1.,0.,10.)
        elif 'SR2a' in SR or 'SR2b' in SR or 'SR4a' in SR or 'SR4b' in SR or 'SR4c' in SR:
            topSample.setNormFactor("mu_2LTop2a",1.,0.,10.)
        elif 'SR5a' in SR:
            topSample.setNormFactor("mu_2LTop5a",1.,0.,10.)
        elif('Super0a' in SR or 'Super0b' in SR or 'Super0c' in SR):
            topSample.setNormFactor("mu_Top14a",1.,0.,10.)
        elif('Super1a' in SR or 'Super1b' in SR or 'Super1c' in SR):
            topSample.setNormFactor("mu_Top14b",1.,0.,10.)
        
    else:
        topSample.setNormByTheory()
	#topSample.addSystematic(sysObj.AR_all_GENTop)
        ##topSample.addSystematic(sysObj.AR_all_SCALETop)
        #topSample.addSystematic(sysObj.AR_all_SHOWERTop)
        #topSample.addSystematic(sysObj.AR_all_IFSRTop)

    # Add in the gen systematic based on the signal region
    ##if 'SR1' in SR:    topSample.addSystematic(sysObj.SRWWa_Top_THEORY)
    ##elif 'SR2a' in SR: topSample.addSystematic(sysObj.SRWWb_Top_THEORY)
    ##elif 'SR2b' in SR: topSample.addSystematic(sysObj.SRWWc_Top_THEORY)
    ##elif 'SR4a' in SR: topSample.addSystematic(sysObj.SRmT2a_Top_THEORY)
    ##elif 'SR4b' in SR: topSample.addSystematic(sysObj.SRmT2b_Top_THEORY)
    ##elif 'SR4c' in SR: topSample.addSystematic(sysObj.SRmT2c_Top_THEORY)


#    if   'Super0a' in SR :      topSample.addSystematic(sysObj.SR0a_Top_THEORY)
#    elif 'Super0b' in SR :      topSample.addSystematic(sysObj.SR0b_Top_THEORY)
#    elif 'Super0c' in SR :      topSample.addSystematic(sysObj.SR0c_Top_THEORY)
#    elif 'Super1a' in SR :      topSample.addSystematic(sysObj.SR1a_Top_THEORY)
#    elif 'Super1b' in SR :      topSample.addSystematic(sysObj.SR1b_Top_THEORY)
#    elif 'Super1c' in SR :      topSample.addSystematic(sysObj.SR1c_Top_THEORY)

    #------------------------------------------------#
    #                      WW                        #
    #------------------------------------------------#

    wwSample.setStatConfig(useStat)
    if userOpts.splitMCSys:
        wwSample.addSystematic(sysObj.AR_mcstat_WW)

    
    # Determine the normalization regions
    if 'SR1' in SR and userOpts.doSimFit2LWW:
        wwSample.setNormRegions([("emW2CRmet","cuts")])     ## Regarless of channel, always fit in em
    if ('SR2a' in SR or 'SR2b' in SR or 'SR4a' in SR or 'SR4b' in SR or 'SR4c' in SR) and userOpts.doSimFit2LWW:
        wwSample.setNormRegions([("emW2CRmt2","cuts")])    ## Regarless of channel, always fit in em
    if userOpts.doSimFit2LWW :
        if('Super0a' in SR or 'Super0b' in SR or 'Super0c' in SR):
            wwSample.setNormRegions([("emCRWW14a","cuts")])
        elif('Super1a' in SR or 'Super1b' in SR or 'Super1c' in SR):
            wwSample.setNormRegions([("emCRWW14b","cuts")])

    # Add Systematics
    wwSample = addSys(wwSample, userOpts.doSimFit2LWW, sysObj)

    # Add in additional WW systematics and
    # specify where norm comes from
    if userOpts.doSimFit2LWW:
        #wwSample.addSystematic(sysObj.AR_all_GENWW)
        #wwSample.addSystematic(sysObj.AR_all_SCALEWW)
        #wwSample.addSystematic(sysObj.AR_all_SHOWERWW)
        #wwSample.addSystematic(sysObj.AR_all_PDFWW)

        if 'SR1' in SR:
            wwSample.setNormFactor("mu_2LWW1",1.,0.,10.)
        elif 'SR2a' in SR or 'SR2b' in SR or 'SR4a' in SR or 'SR4b' in SR or 'SR4c' in SR:
            wwSample.setNormFactor("mu_2LWW2a",1.,0.,10.)
        elif('Super0a' in SR or 'Super0b' in SR or 'Super0c' in SR):
            wwSample.setNormFactor("mu_WW14a",1.,0.,10.)
        elif('Super1a' in SR or 'Super1b' in SR or 'Super1c' in SR):
            wwSample.setNormFactor("mu_WW14b",1.,0.,10.)

    else:
        wwSample.setNormByTheory()
        #wwSample.addSystematic(sysObj.AR_all_GENWW)
        #wwSample.addSystematic(sysObj.AR_all_SCALEWW)
        #wwSample.addSystematic(sysObj.AR_all_SHOWERWW)
        #wwSample.addSystematic(sysObj.AR_all_PDFWW)

    # Add in the gen systematic based on the signal region
    ##if 'SR1' in SR:    wwSample.addSystematic(sysObj.SRWWa_WW_THEORY)
    ##elif 'SR2a' in SR: wwSample.addSystematic(sysObj.SRWWb_WW_THEORY)
    ##elif 'SR2b' in SR: wwSample.addSystematic(sysObj.SRWWc_WW_THEORY)
    ##elif 'SR4a' in SR: wwSample.addSystematic(sysObj.SRmT2a_WW_THEORY)
    ##elif 'SR4b' in SR: wwSample.addSystematic(sysObj.SRmT2b_WW_THEORY)
    ##elif 'SR4c' in SR: wwSample.addSystematic(sysObj.SRmT2c_WW_THEORY)

#    if   'Super0a' in SR :      wwSample.addSystematic(sysObj.SR0a_WW_THEORY)
#    elif 'Super0b' in SR :      wwSample.addSystematic(sysObj.SR0b_WW_THEORY)
#    elif 'Super0c' in SR :      wwSample.addSystematic(sysObj.SR0c_WW_THEORY)
#    elif 'Super1a' in SR :      wwSample.addSystematic(sysObj.SR1a_WW_THEORY)
#    elif 'Super1b' in SR :      wwSample.addSystematic(sysObj.SR1b_WW_THEORY)
#    elif 'Super1c' in SR :      wwSample.addSystematic(sysObj.SR1c_WW_THEORY)


    #------------------------------------------------#
    #                     DATA                       #
    #------------------------------------------------#

    dataSample.setData()


# End of configuration of samples

##
## Set the samples to use
##
userPrint("Setting samples to use")
# Don't have the fakes for now, so remove them
#tlx.addSamples([wwSample,topSample,zvSample,zxSample,higgsSample,fakeSample,dataSample])
tlx.addSamples([fakeSample,wwSample,topSample,zvSample,zxSample,higgsSample,dataSample])


##
## Setup plotting
##
userPrint("Setting up plotting")

# Generic things for the manager
tlx.dataColor = dataSample.color
tlx.totalPdfColor = kRed
tlx.errorFillColor = kBlack
tlx.errorFillStyle = 3004
tlx.errorLineStyle = kDashed
tlx.errorLineColor = kBlue-5

# Make a Canvas and legend
c = TCanvas()
compFillStyle = 1001 # see ROOT for Fill styles
leg = TLegend(0.75,0.6,0.94,0.94,"")
leg.SetFillStyle(0)
leg.SetFillColor(0)
leg.SetBorderSize(0)

# Make a LegendEntry
entry = TLegendEntry()
entry = leg.AddEntry("","Data 2012 (#sqrt{s}=8 TeV)","p") 
entry.SetMarkerColor(tlx.dataColor)
entry.SetMarkerStyle(20)

# Now specify for the samples
# Write simple method to take
# care of doing this neatly
def addEntry(legEntry, legend, name, color, fillColor, fillStyle):
    legEntry = legend.AddEntry("",name,"lf")
    legEntry.SetLineColor(color)
    legEntry.SetFillColor(fillColor)
    legEntry.SetFillStyle(fillStyle)
    return legEntry

if userOpts.do2L:

    # Total PDF
    entry = addEntry(entry,leg,"Total pdf",tlx.totalPdfColor,tlx.errorFillColor,tlx.errorFillStyle)
    entry.SetLineWidth(2)
    # fakes
    entry = addEntry(entry,leg,"Fakes",fakeSample.color,fakeSample.color,compFillStyle)
    # ttbar
    entry = addEntry(entry,leg,"t#bar{t}, single top",topSample.color,topSample.color,compFillStyle)
    # WW
    entry = addEntry(entry,leg,"WW",wwSample.color,wwSample.color,compFillStyle)
    # Higgs
    entry = addEntry(entry,leg,"Higgs",higgsSample.color,higgsSample.color,compFillStyle)
    # ZV
    entry = addEntry(entry,leg,"ZV",zvSample.color,zvSample.color,compFillStyle)
    # Zjets
    entry = addEntry(entry,leg,"Z+jets",zxSample.color,zxSample.color,compFillStyle)

# Set the legend
tlx.tLegend = leg


##
## Setup the Simultaneous fit options
##
userPrint("Setting up simultaneous fit options")

# Get the control region list for fitting
crList    = getCRFitList(tlx,
                         userOpts.signalRegion,
                         userOpts.leptonChannel,
                         userOpts.doSimFit2LWW,
                         userOpts.doSimFit2LTop,
                         userOpts.doSimFit2LZV,
                         userDefs, sysObj)



if userOpts.doSimFit2LWW or userOpts.doSimFit2LTop or userOpts.doSimFit2LZV:
    tlx.setBkgConstrainChannels(crList)


##
## Setup the signal regions
##
userPrint("Setting up signal regions")

if userOpts.doExclusion or userOpts.doValidation:

    srList    = []
    srCounter = 0
    lepChan   = userOpts.leptonChannel
    SR        = userOpts.signalRegion

    channels = []
    if lepChan == userDefs.all  : channels = ['ee','mm','em']
    if lepChan == userDefs.ee   : channels = ['ee']
    if lepChan == userDefs.mm   : channels = ['mm']
    if lepChan == userDefs.em   : channels = ['em']
    if lepChan == userDefs.eemm : channels = ['ee','mm']
    if lepChan == userDefs.tot  : channels = ['tot']
    if lepChan == userDefs.sf   : channels = ['sf']

    # Define simple function
    def addSR(type, channels, counter, SR, nbins, low, high, shapeFit):
        for chan in channels:
            userPrint("~~~ Adding SR for chan: "+chan+"~~~")
            currentChannel = tlx.addChannel(type,[chan+SR],nbins,low,high)
            ## Add theory uncertainties only in the SR!
            if 'Super0a' in SR :
                currentChannel.getSample("ZV").addSystematic( sysObj.SR0a_ZV_THEORY)
                currentChannel.getSample("Top").addSystematic(sysObj.SR0a_Top_THEORY)
                currentChannel.getSample("WW").addSystematic( sysObj.SR0a_WW_THEORY)
                if chan=='ee':
                    currentChannel.getSample("Fake").addSystematic( sysObj.eeSR0a_FakeRelUnc)
                elif chan=='mm':
                    currentChannel.getSample("Fake").addSystematic( sysObj.mmSR0a_FakeRelUnc)
                elif chan=='em':
                    currentChannel.getSample("Fake").addSystematic( sysObj.emSR0a_FakeRelUnc)
                elif chan=='sf':
                    currentChannel.getSample("Fake").addSystematic( sysObj.sfSR0a_FakeRelUnc)
            elif 'Super0b' in SR :
                currentChannel.getSample("ZV").addSystematic( sysObj.SR0b_ZV_THEORY)
                currentChannel.getSample("Top").addSystematic(sysObj.SR0b_Top_THEORY)
                currentChannel.getSample("WW").addSystematic( sysObj.SR0b_WW_THEORY)
                if chan=='ee':
                    currentChannel.getSample("Fake").addSystematic( sysObj.eeSR0b_FakeRelUnc)
                elif chan=='mm':
                    currentChannel.getSample("Fake").addSystematic( sysObj.mmSR0b_FakeRelUnc)
                elif chan=='em':
                    currentChannel.getSample("Fake").addSystematic( sysObj.emSR0b_FakeRelUnc)
                elif chan=='sf':
                    currentChannel.getSample("Fake").addSystematic( sysObj.sfSR0b_FakeRelUnc)
            elif 'Super0c' in SR :
                currentChannel.getSample("ZV").addSystematic( sysObj.SR0c_ZV_THEORY)
                currentChannel.getSample("Top").addSystematic(sysObj.SR0c_Top_THEORY)
                currentChannel.getSample("WW").addSystematic( sysObj.SR0c_WW_THEORY)
                if chan=='ee':
                    currentChannel.getSample("Fake").addSystematic( sysObj.eeSR0c_FakeRelUnc)
                elif chan=='mm':
                    currentChannel.getSample("Fake").addSystematic( sysObj.mmSR0c_FakeRelUnc)
                elif chan=='em':
                    currentChannel.getSample("Fake").addSystematic( sysObj.emSR0c_FakeRelUnc)
                elif chan=='sf':
                    currentChannel.getSample("Fake").addSystematic( sysObj.sfSR0c_FakeRelUnc)
            elif 'Super1a' in SR :
                currentChannel.getSample("ZV").addSystematic( sysObj.SR1a_ZV_THEORY)
            #    currentChannel.getSample("Top").addSystematic(sysObj.SR1a_Top_THEORY)
                currentChannel.getSample("WW").addSystematic( sysObj.SR1a_WW_THEORY)
                # top uncertainties broken down to components
                # TT PS
                currentChannel.getSample("Top").addSystematic(sysObj.SR1a_TT_PS)
                currentChannel.getSample("Top").addSystematic(sysObj.SR1a_Top_Other)
    #            currentChannel.getSample("Top").addSystematic(sysObj.SR1a_TT_GEN)
    #            currentChannel.getSample("Top").addSystematic(sysObj.SR1a_TT_PS)
    #            currentChannel.getSample("Top").addSystematic(sysObj.SR1a_TT_ISRFSR)
    #            currentChannel.getSample("Top").addSystematic(sysObj.SR1a_TT_PDF)
    #            currentChannel.getSample("Top").addSystematic(sysObj.SR1a_TT_QCD)
    #            currentChannel.getSample("Top").addSystematic(sysObj.SR1a_ST_GEN)
    #            currentChannel.getSample("Top").addSystematic(sysObj.SR1a_ST_PS)
    #            currentChannel.getSample("Top").addSystematic(sysObj.SR1a_ST_DSDR)
    #            currentChannel.getSample("Top").addSystematic(sysObj.SR1a_ST_ISRFSR)
    #            currentChannel.getSample("Top").addSystematic(sysObj.SR1a_ST_PDF)

                if chan=='ee':
                    currentChannel.getSample("Fake").addSystematic( sysObj.eeSR1a_FakeRelUnc)
                elif chan=='mm':
                    currentChannel.getSample("Fake").addSystematic( sysObj.mmSR1a_FakeRelUnc)
                elif chan=='em':
                    currentChannel.getSample("Fake").addSystematic( sysObj.emSR1a_FakeRelUnc)
                elif chan=='sf':
                    currentChannel.getSample("Fake").addSystematic( sysObj.sfSR1a_FakeRelUnc)
            elif 'Super1b' in SR :
                currentChannel.getSample("ZV").addSystematic( sysObj.SR1b_ZV_THEORY)
            #    currentChannel.getSample("Top").addSystematic(sysObj.SR1b_Top_THEORY)
                currentChannel.getSample("WW").addSystematic( sysObj.SR1b_WW_THEORY)
                # top uncertainties broken down to components
                currentChannel.getSample("Top").addSystematic(sysObj.SR1b_TT_PS)
                currentChannel.getSample("Top").addSystematic(sysObj.SR1b_Top_Other)
         #       currentChannel.getSample("Top").addSystematic(sysObj.SR1b_TT_GEN)
         #       currentChannel.getSample("Top").addSystematic(sysObj.SR1b_TT_PS)
         #       currentChannel.getSample("Top").addSystematic(sysObj.SR1b_TT_ISRFSR)
         #       currentChannel.getSample("Top").addSystematic(sysObj.SR1b_TT_PDF)
         #       currentChannel.getSample("Top").addSystematic(sysObj.SR1b_TT_QCD)
         #       currentChannel.getSample("Top").addSystematic(sysObj.SR1b_ST_GEN)
         #       currentChannel.getSample("Top").addSystematic(sysObj.SR1b_ST_PS)
         #       currentChannel.getSample("Top").addSystematic(sysObj.SR1b_ST_DSDR)
         #       currentChannel.getSample("Top").addSystematic(sysObj.SR1b_ST_ISRFSR)
         #       currentChannel.getSample("Top").addSystematic(sysObj.SR1b_ST_PDF)

                if chan=='ee':
                    currentChannel.getSample("Fake").addSystematic( sysObj.eeSR1b_FakeRelUnc)
                elif chan=='mm':
                    currentChannel.getSample("Fake").addSystematic( sysObj.mmSR1b_FakeRelUnc)
                elif chan=='em':
                    currentChannel.getSample("Fake").addSystematic( sysObj.emSR1b_FakeRelUnc)
                elif chan=='sf':
                    currentChannel.getSample("Fake").addSystematic( sysObj.sfSR1b_FakeRelUnc)
            elif 'Super1c' in SR :
                currentChannel.getSample("ZV").addSystematic( sysObj.SR1c_ZV_THEORY)
              #  currentChannel.getSample("Top").addSystematic(sysObj.SR1c_Top_THEORY)
                currentChannel.getSample("WW").addSystematic( sysObj.SR1c_WW_THEORY)
                # top uncertainties broken down to components
                currentChannel.getSample("Top").addSystematic(sysObj.SR1c_TT_PS)
                currentChannel.getSample("Top").addSystematic(sysObj.SR1c_Top_Other)
          #      currentChannel.getSample("Top").addSystematic(sysObj.SR1c_TT_GEN)
          #      currentChannel.getSample("Top").addSystematic(sysObj.SR1c_TT_PS)
          #      currentChannel.getSample("Top").addSystematic(sysObj.SR1c_TT_ISRFSR)
          #      currentChannel.getSample("Top").addSystematic(sysObj.SR1c_TT_PDF)
          #      currentChannel.getSample("Top").addSystematic(sysObj.SR1c_TT_QCD)
          #      currentChannel.getSample("Top").addSystematic(sysObj.SR1c_ST_GEN)
          #      currentChannel.getSample("Top").addSystematic(sysObj.SR1c_ST_PS)
          #      currentChannel.getSample("Top").addSystematic(sysObj.SR1c_ST_DSDR)
          #      currentChannel.getSample("Top").addSystematic(sysObj.SR1c_ST_ISRFSR)
          #      currentChannel.getSample("Top").addSystematic(sysObj.SR1c_ST_PDF)

                if chan=='ee':
                    currentChannel.getSample("Fake").addSystematic( sysObj.eeSR1c_FakeRelUnc)
                elif chan=='mm':
                    currentChannel.getSample("Fake").addSystematic( sysObj.mmSR1c_FakeRelUnc)
                elif chan=='em':
                    currentChannel.getSample("Fake").addSystematic( sysObj.emSR1c_FakeRelUnc)
                elif chan=='sf':
                    currentChannel.getSample("Fake").addSystematic( sysObj.sfSR1c_FakeRelUnc)

                
            srList.append( currentChannel )
            srList[counter].userOverflowBin=True
            if shapeFit:
                srList[counter].userUnderflowBin=False
            else:
                srList[counter].userUnderflowBin=True

            counter+=1
        return counter

    # At this point it seems Geraldin'e script has a list for sr, but right now
    # I only have one SR option.  Think about updating this for future

    if not userOpts.doShape:
        srCounter = addSR("cuts",channels,srCounter,SR,1,0.5,1.5,False) # Updated to 0.5-1.5 from Serhan
    else:
        srCounter = addSR("2LMT2",channels,srCounter,SR,90000,120000,True)

    if userOpts.doValidation:
        tlx.setValidationChannels(srList)
    else:
        tlx.setSignalChannels(srList)
        
##
## Do discovery fit
##

if userOpts.doDiscovery:
    userPrint("Setting up discovery fit section")
    # Right now only using one signal region,
    # but if we use many, then this will need
    # to be modified since can only use one
    # channel for discovery fit
    srChanName = ""
    chan = ""
    if userOpts.leptonChannel == userDefs.ee : 
        srChanName += "ee"
        chan = "ee"
    if userOpts.leptonChannel == userDefs.mm :
        srChanName += "mm"
        chan = "mm"
    if userOpts.leptonChannel == userDefs.em :
        srChanName += "em"
        chan = "em"        
    if userOpts.leptonChannel == userDefs.sf :
        srChanName += "sf"
        chan = "sf"
    srChanName += userOpts.signalRegion
    discoChannel = tlx.addChannel("cuts",[srChanName],1,0,1)
    discoChannel.addDiscoverySamples(["SIG"],[1.],[0.],[100.],[kRed])
    if userOpts.splitMCSys:
        discoChannel.addSystematic(sysObj.AR_mcstat_SIG)
    # SR-specific uncertainties
    if 'Super0a' in srChanName :
        discoChannel.getSample("ZV").addSystematic( sysObj.SR0a_ZV_THEORY)
        discoChannel.getSample("Top").addSystematic(sysObj.SR0a_Top_THEORY)
        discoChannel.getSample("WW").addSystematic( sysObj.SR0a_WW_THEORY)
        if chan=='ee':
            discoChannel.getSample("Fake").addSystematic( sysObj.eeSR0a_FakeRelUnc)
        elif chan=='mm':
            discoChannel.getSample("Fake").addSystematic( sysObj.mmSR0a_FakeRelUnc)
        elif chan=='em':
            discoChannel.getSample("Fake").addSystematic( sysObj.emSR0a_FakeRelUnc)
    elif 'Super0b' in SR :
        discoChannel.getSample("ZV").addSystematic( sysObj.SR0b_ZV_THEORY)
        discoChannel.getSample("Top").addSystematic(sysObj.SR0b_Top_THEORY)
        discoChannel.getSample("WW").addSystematic( sysObj.SR0b_WW_THEORY)
        if chan=='ee':
            discoChannel.getSample("Fake").addSystematic( sysObj.eeSR0b_FakeRelUnc)
        elif chan=='mm':
            discoChannel.getSample("Fake").addSystematic( sysObj.mmSR0b_FakeRelUnc)
        elif chan=='em':
            discoChannel.getSample("Fake").addSystematic( sysObj.emSR0b_FakeRelUnc)
    elif 'Super0c' in SR :
        discoChannel.getSample("ZV").addSystematic( sysObj.SR0c_ZV_THEORY)
        discoChannel.getSample("Top").addSystematic(sysObj.SR0c_Top_THEORY)
        discoChannel.getSample("WW").addSystematic( sysObj.SR0c_WW_THEORY)
        if chan=='ee':
            discoChannel.getSample("Fake").addSystematic( sysObj.eeSR0c_FakeRelUnc)
        elif chan=='mm':
            discoChannel.getSample("Fake").addSystematic( sysObj.mmSR0c_FakeRelUnc)
        elif chan=='em':
            discoChannel.getSample("Fake").addSystematic( sysObj.emSR0c_FakeRelUnc)
    elif 'Super1a' in SR :
        discoChannel.getSample("ZV").addSystematic( sysObj.SR1a_ZV_THEORY)
        discoChannel.getSample("WW").addSystematic( sysObj.SR1a_WW_THEORY)
       # discoChannel.getSample("Top").addSystematic(sysObj.SR1a_Top_THEORY)
        # top uncertainties broken down to components
        # TT PS
        discoChannel.getSample("Top").addSystematic(sysObj.SR1a_TT_PS)
        discoChannel.getSample("Top").addSystematic(sysObj.SR1a_Top_Other)
        if chan=='ee':
            discoChannel.getSample("Fake").addSystematic( sysObj.eeSR1a_FakeRelUnc)
        elif chan=='mm':
            discoChannel.getSample("Fake").addSystematic( sysObj.mmSR1a_FakeRelUnc)
        elif chan=='em':
            discoChannel.getSample("Fake").addSystematic( sysObj.emSR1a_FakeRelUnc)
        elif chan=='sf':
            discoChannel.getSample("Fake").addSystematic( sysObj.sfSR1a_FakeRelUnc)
    elif 'Super1b' in SR :
        discoChannel.getSample("ZV").addSystematic( sysObj.SR1b_ZV_THEORY)
        discoChannel.getSample("WW").addSystematic( sysObj.SR1b_WW_THEORY)
        # top uncertainties broken down to components
        discoChannel.getSample("Top").addSystematic(sysObj.SR1b_TT_PS)
        discoChannel.getSample("Top").addSystematic(sysObj.SR1b_Top_Other)
        if chan=='ee':
            discoChannel.getSample("Fake").addSystematic( sysObj.eeSR1b_FakeRelUnc)
        elif chan=='mm':
            discoChannel.getSample("Fake").addSystematic( sysObj.mmSR1b_FakeRelUnc)
        elif chan=='em':
            discoChannel.getSample("Fake").addSystematic( sysObj.emSR1b_FakeRelUnc)
        elif chan=='sf':
            discoChannel.getSample("Fake").addSystematic( sysObj.sfSR1b_FakeRelUnc)
    elif 'Super1c' in SR :
        discoChannel.getSample("ZV").addSystematic( sysObj.SR1c_ZV_THEORY)
        discoChannel.getSample("WW").addSystematic( sysObj.SR1c_WW_THEORY)
        # top uncertainties broken down to components
        discoChannel.getSample("Top").addSystematic(sysObj.SR1c_TT_PS)
        discoChannel.getSample("Top").addSystematic(sysObj.SR1c_Top_Other)
        if chan=='ee':
            discoChannel.getSample("Fake").addSystematic( sysObj.eeSR1c_FakeRelUnc)
        elif chan=='mm':
            discoChannel.getSample("Fake").addSystematic( sysObj.mmSR1c_FakeRelUnc)
        elif chan=='em':
            discoChannel.getSample("Fake").addSystematic( sysObj.emSR1c_FakeRelUnc)
        elif chan=='sf':
            discoChannel.getSample("Fake").addSystematic( sysObj.sfSR1c_FakeRelUnc)
    tlx.setSignalChannels(discoChannel)

##
## Setting grid to do exclusions
##
userPrint("Set the grid for exclusions")

sigSamples = []
if userOpts.doExclusion:

    # Currently only one grid defined.
    # Work on adding others later
    if "SMCwslep" in userOpts.sigGrid: sigSamples = userDefs.getGrid(userOpts.sigGrid)
    elif "DLiSlep"  in userOpts.sigGrid: sigSamples = userDefs.getGrid(userOpts.sigGrid)
    else:
        userPrint("Could not determine a grid to run on.")
        userPrint("Exitting")
        sys.exit()

    # Now loop over signal samples
    userPrint("Looping over Signal Samples")
    for s in sigSamples:
        signame = s # why?

        doToys   = userOpts.doToys
        hasHippo = doToys and 'hippo' in userOpts.gridForToys
        hasSig   = doToys and signame in userOpts.gridForToys
        if not doToys or hasHippo or hasSig:
            exclusion = configMgr.addFitConfigClone(tlx,'TopLvlXML_Exclusion_%s'%s)
            print '!!!--- in LOOP ', s
            sigSample = Sample(s, kRed)
            sigSample.setStatConfig(useStat)
            if userOpts.splitMCSys:
                sigSample.addSystematic(sysObj.AR_mcstat_SIG)

            sigUncert = userOpts.sigUncert

            sigSample.setFileList([userOpts.sigFile])
            if sigUncert == "up":
                sigSample.setWeights(("eventweight","syst_XSUP","1.0"))
            elif sigUncert == "down":
                sigSample.setWeights(("eventweight","syst_XSDOWN","1.0"))

            sigSample.addSystematic(sysObj.AR_all_JES_MC)
            sigSample.addSystematic(sysObj.AR_all_JER_MC)
#          sigSample.addSystematic(sysObj.AR_all_JVF_MC)
            sigSample.addSystematic(sysObj.AR_all_TES_MC)
            sigSample.addSystematic(sysObj.AR_all_BJET_MC)
            sigSample.addSystematic(sysObj.AR_all_CJET_MC)
            sigSample.addSystematic(sysObj.AR_all_BMISTAG_MC)
            sigSample.addSystematic(sysObj.AR_all_EER_MC)
            sigSample.addSystematic(sysObj.AR_all_EESLOW_MC)
            sigSample.addSystematic(sysObj.AR_all_EESMAT_MC)
            sigSample.addSystematic(sysObj.AR_all_EESPS_MC)
            sigSample.addSystematic(sysObj.AR_all_EESZ_MC)
            sigSample.addSystematic(sysObj.AR_all_ESF_MC)
            sigSample.addSystematic(sysObj.AR_all_MID_MC)
            sigSample.addSystematic(sysObj.AR_all_MMS_MC)
            sigSample.addSystematic(sysObj.AR_all_MEFF_MC)
            sigSample.addSystematic(sysObj.AR_all_RESOST_MC)
            sigSample.addSystematic(sysObj.AR_all_SCALEST_MC)
            sigSample.addSystematic(sysObj.AR_all_PILEUP_MC)
            sigSample.addSystematic(sysObj.AR_all_TRIGGERE_MC)
            sigSample.addSystematic(sysObj.AR_all_TRIGGERM_MC)
            sigSample.setNormFactor('mu_SIG',1.,0.,10.)

            # Add the sample to the exclusion
            exclusion.addSamples(sigSample)
            exclusion.setSignalSample(sigSample)
            #exclusion.setSignalChannels(srList) <-- don't need this: SERHAN: 30/7/2013

            print s, 'Leaving LOOP ---!!!'
