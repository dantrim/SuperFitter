
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
from CombinationUtils import *

#--------------------------------------------------------#
# User will specify the options in this region
#--------------------------------------------------------#

# Now utilize the inputs from the command line.  This will
# be strictly enforced. User must give:
# 1.) Signal region
# 2.) Channel
# 3.) The grid to consider

SignalRegionChoices = ["combJetN"]
ChannelChoices      = ["all"]
GridChoices         = ["SMCwslep","SMCwslep0","SMCwslep1","SMCwslep2","SMCwslep3","SMCwslep4"]
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
#indirMC     = "/gdata/atlas/dantrim/SuperHistFitter_00/TAnalysis/output/R8_Oct_7/Processed/"
indirMC     = "root://eosatlas//eos/atlas/user/d/dantrim/hft_inputs/R8_Oct_7/"
#indirSig    = "/gdata/atlas/dantrim/SuperHistFitter_01/TAnalysis/output/L0_Nov_7/Processed/"
indirSig    = "root://eosatlas//eos/atlas/user/d/dantrim/hft_inputs/L0_Nov_7/"
#indirData   = "/gdata/atlas/dantrim/SuperHistFitter_00/TAnalysis/output/R8_Oct_7/Processed/"
indirData   = "root://eosatlas//eos/atlas/user/d/dantrim/hft_inputs/R8_Oct_7/"

bkgFile    = indirMC + "HFT_BG8TeV.root"
dataFile   = indirData + "HFT_BG8TeV.root"
signalFile = ""
if "SMCwslep" in _grid:
    signalFile = indirSig + "HFT_SMCwslep8TeV.root"
if signalFile == "": sys.exit()

# Specify Analysis name. This will be used to identify
# the results of the run in the results directory
analysisName = _signalRegion+"_"+_channel+"_"+_grid

# Creat user defs instance
userDefs = ConfigDefs()

# Get the channel enum
# Let default be all
_ch = userDefs.all 

# Specify what backgrounds to fit
fitWW  =        True 
fitTop =        True 
fitZV  =        True 

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
                          True,                     # doExclusion
                          False,                    # doDiscovery
                          False,                    # doValidation
                          False,                    # doShapeFit
                          fitWW,                    # doSimFitWW
                          fitTop,                   # doSimFitTop
                          fitZV,                    # doSimFitZV
                          True,                     # split MC sys to individual samples (?)
                          True,                     # Blind SR
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
# TODO
fakeSample  = Sample("Fake"       , kGray)
higgsSample = Sample("Higgs"       , kYellow)
zvSample    = Sample("ZV"          , kGreen)
topSample   = Sample("Top"        , kViolet)
wwSample    = Sample("WW"          , kAzure-4)
dataSample  = Sample("Data_CENTRAL", kBlack)

mcSamples  = [zxSample, higgsSample, zvSample, topSample, wwSample, dataSample]
# TODO

bkgFiles  = []
if userOpts.do2L:
    bkgFiles.append( userOpts.bkgFile )
for sample in mcSamples :
    sample.setFileList(bkgFiles)



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


#############################################################
## Toys Vs. Asymtoptic (Asimov's)                           #
#############################################################
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

configMgr.testStatType = 3
configMgr.nPoints      = 20
configMgr.writeXML     = True # TODO make configurable

#############################################################
## Specify the Fit Mode                                     #
#############################################################
userPrint("Specifying the fit mode")

if userOpts.doDiscovery: configMgr.doExclusion = False
if userOpts.doExclusion: configMgr.doExclusion = True

# Check to make sure we are not doing validation
# and exclusion.  Only can do one, give preference
# to exclusion
if userOpts.doValidation and userOpts.doExclusion:
    print "Can't do validation and Exclusion, setting validation to false"
    userOpts.doValidation = False

#############################################################
## Specify output files                                     # 
#############################################################
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

#############################################################
## Set the luminosity                                       #
#############################################################
userPrint("Specifying Luminosity")

configMgr.inputLumi  = userOpts.inputLumi
configMgr.outputLumi = userOpts.outputLumi
configMgr.setLumiUnits( userOpts.lumiUnits )


#############################################################
## Specify the background input files                       #
#############################################################
userPrint("Specifying background input")

bkgFiles  = []
if userOpts.do2L:
    bkgFiles.append( userOpts.bkgFile )
for sample in mcSamples :
    sample.setFileList(bkgFiles)


#############################################################
## Configure the selection                                  #
#############################################################
userPrint("Configuring selection")

configMgr = selectionConfig(configMgr,userOpts.slepLimitN)

#############################################################
## Configure weight                                         #
#############################################################
userPrint("Specifying Weight")

if userOpts.do2L:
    configMgr.weights = ["eventweight"]

#############################################################
## Setup the systematics                                    #
#############################################################
userPrint("Configuring Systematic")

# Add all sys to SystematicObject
# where you can access the systematics
# through this object when initializing
# the backgrounds
sysObj = SystematicObject(configMgr, userOpts.doShape, userOpts.splitMCSys)
configMgr.nomName = "_CENTRAL"

#############################################################
## Setting up Samples and normalization factors             #
#############################################################
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
# TODO
    if doSimFit:
        sample.addSystematic(sysObj.AR_all_JES_CR)
        sample.addSystematic(sysObj.AR_all_JER_CR)
#        sample.addSystematic(sysObj.AR_all_JVF_CR)
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
     #   sample.addSystematic(sysObj.AR_all_PILEUP_CR)
        sample.addSystematic(sysObj.AR_all_TRIGGERE_CR)
        sample.addSystematic(sysObj.AR_all_TRIGGERM_CR)
    else:
        sample.addSystematic(sysObj.AR_all_JES_MC)
        sample.addSystematic(sysObj.AR_all_JER_MC)
#        sample.addSystematic(sysObj.AR_all_JVF_MC)
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
        #sample.addSystematic(sysObj.AR_all_PILEUP_MC)
        sample.addSystematic(sysObj.AR_all_TRIGGERE_MC)
        sample.addSystematic(sysObj.AR_all_TRIGGERM_MC)

#    # return the updated sample
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
    fakeSample.buildHisto([0.99], "eeSuper0a", "cuts")
    fakeSample.buildHisto([0.1],  "mmSuper0a", "cuts")
    fakeSample.buildHisto([0.1],  "emSuper0a", "cuts")
    fakeSample.buildHisto([0.1],  "eeSuper0b", "cuts")
    fakeSample.buildHisto([0.1],  "mmSuper0b", "cuts")
    fakeSample.buildHisto([0.1],  "emSuper0b", "cuts")
    fakeSample.buildHisto([0.02], "eeSuper0c", "cuts")
    fakeSample.buildHisto([0.1],  "mmSuper0c", "cuts")
    fakeSample.buildHisto([0.1],  "emSuper0c", "cuts")
    fakeSample.buildHisto([1.07], "eeSuper1a", "cuts")
    fakeSample.buildHisto([2.12], "mmSuper1a", "cuts")
    fakeSample.buildHisto([0.37], "emSuper1a", "cuts")
    fakeSample.buildHisto([0.49], "eeSuper1b", "cuts")
    fakeSample.buildHisto([0.1],  "mmSuper1b", "cuts")
    fakeSample.buildHisto([0.1],  "emSuper1b", "cuts")
    fakeSample.buildHisto([0.31], "eeSuper1c", "cuts")
    fakeSample.buildHisto([1.35], "mmSuper1c", "cuts")
    fakeSample.buildHisto([0.1],  "emSuper1c", "cuts")
    fakeSample.buildHisto([0.1],  "emCRTop14a", "cuts")
    fakeSample.buildHisto([0.1],  "emCRTop14b", "cuts")
    fakeSample.buildHisto([85.06], "emCRWW14a", "cuts")
    fakeSample.buildHisto([21.82], "emCRWW14b", "cuts")
    fakeSample.buildHisto([0.1],  "emCRZV14a",  "cuts")
    fakeSample.buildHisto([0.1],  "emCRZV14a",  "cuts")

    fakeSample.setStatConfig(useStat)
    fakeSample.setNormByTheory()

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
    if userOpts.doSimFit2LZV:
        zvSample.setNormRegions([("emCRZV14a","cuts"),("emCRZV14b","cuts")])

    # Add Systematics
    zvSample = addSys(zvSample, userOpts.doSimFit2LZV, sysObj)

    # Additional ZV Specific systematics
    if userOpts.doSimFit2LZV:
        zvSample.setNormFactor("mu_ZV",1.,0.,10.)
    else:	
        zvSample.setNormByTheory()


    #------------------------------------------------#
    #                     TOP                        #
    #------------------------------------------------#
    topSample.setStatConfig(useStat)
    if userOpts.splitMCSys:
        topSample.addSystematic(sysObj.AR_mcstat_TOP)
    
    # Determine the normalization regions
    # This should be done only if we fit
    if userOpts.doSimFit2LTop :
        topSample.setNormRegions([("emCRTop14a","cuts"), ("emCRTop14b","cuts")])

    # Set the systematics
    topSample = addSys(topSample, userOpts.doSimFit2LTop, sysObj)

    # Add in additional top systematics and
    # specify the normative factors
    if userOpts.doSimFit2LTop:
        topSample.setNormFactor("mu_Top",1.,0.,10.)
    else:
        topSample.setNormByTheory()

    #------------------------------------------------#
    #                      WW                        #
    #------------------------------------------------#

    wwSample.setStatConfig(useStat)
    if userOpts.splitMCSys:
        wwSample.addSystematic(sysObj.AR_mcstat_WW)

    # Determine the normalization regions
    if userOpts.doSimFit2LWW :
        wwSample.setNormRegions([("emCRWW14a","cuts"),("emCRWW14b","cuts")])
    
    # Add Systematics
    wwSample = addSys(wwSample, userOpts.doSimFit2LWW, sysObj)

    # Add in additional WW systematics and
    # specify where norm comes from
    if userOpts.doSimFit2LWW:
        wwSample.setNormFactor("mu_WW",1.,0.,10.)
    else:
        wwSample.setNormByTheory()

    #------------------------------------------------#
    #                     DATA                       #
    #------------------------------------------------#

    dataSample.setData()

# End of configuration of samples

#############################################################
## Set the samples to use                                   #
#############################################################
userPrint("Setting samples to use")

tlx.addSamples([fakeSample,wwSample,topSample,zvSample,zxSample,higgsSample,dataSample])

#############################################################
## Setup plotting                                           #
#############################################################
# TODO: see about configuring nice plots from this for mDeltaR, mT2, lept1Pt, etc...
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


######################################################
# Configure control regions                          #
######################################################
userPrint("Setting up Control Regions for SimFit")

crList = []
crList_0  = getCRFitList(tlx,
                         'Super0a',
                         'all',
                         userOpts.doSimFit2LWW,
                         userOpts.doSimFit2LTop,
                         userOpts.doSimFit2LZV,
                         userDefs, sysObj)

crList_1  = getCRFitList(tlx,
                         'Super1a',
                         'all',
                         userOpts.doSimFit2LWW,
                         userOpts.doSimFit2LTop,
                         userOpts.doSimFit2LZV,
                         userDefs, sysObj)
crList += crList_0
crList += crList_1

if userOpts.doSimFit2LWW or userOpts.doSimFit2LTop or userOpts.doSImFit2LZV:
    tlx.setBkgConstrainChannels(crList)


#############################################################
##    Set up config for Discovery Fit                       #
#############################################################
userPrint("Setting up discovery fit section")

if userOpts.doDiscovery:
    # Right now only using one signal region,
    # but if we use many, then this will need
    # to be modified since can only use one
    # channel for discovery fit
    srChanName = ""
    if userOpts.leptonChannel == userDefs.ee: srChanName += "ee"
    if userOpts.leptonChannel == userDefs.mm: srChanName += "mm"
    if userOpts.leptonChannel == userDefs.em: srChanName += "em"        
    srChanName += userOpts.signalRegion
    discoChannel = tlx.addChannel("cuts",[srChanName],1,0,1)
    discoChannel.addDiscoverySamples(["SIG"],[1.],[0.],[100.],[kRed])
    if userOpts.splitMCSys:
        discoChannel.addSystematic(sysObj.AR_mcstat_SIG)
    tlx.setSignalChannels(discoChannel)

#############################################################
## Set up config for Exclusion Fit                          #
#############################################################
userPrint("Set the grid for exclusions")

sigSamples = []
if userOpts.doExclusion:

    # Currently only one grid defined.
    # Work on adding others later
    if "SMCwslep" in userOpts.sigGrid: sigSamples = userDefs.getGrid(userOpts.sigGrid)
    else:
        userPrint("Could not determine a grid to run on.")
        userPrint("Exitting")
        sys.exit()

    # Grab the dictionary that has the best 0- and 1-jet SR for each point
    combinationUtil = CombinationUtils()
    bestSRdict = combinationUtil.getSRPerPoint(userOpts.sigGrid)  # { SMCwslep8TeV_mC1_mN1 : [ bestSR0, bestSR1 ] }

    # Now loop over signal samples
    userPrint("Looping over Signal Samples")
    for s in sigSamples[10:11] :
        signame = s # why?

        # ---------------------------------------------------- #
        # Set up the signal regions on a point-by-point basis  #
        # ---------------------------------------------------- #
        userPrint("Setting up signal regions [BEGIN]")
        
        srList = []
        srCounter = 0

        lepChan = userOpts.leptonChannel
        channels = []
        if lepChan == userDefs.all : channels = ['ee', 'mm', 'em']

        srs = []
        if SR == 'combJetN' : srs = bestSRdict[signame]
        else :
            print " >>> This module is for combining 0- and 1-Jet SRs. SR choice must be 'combJetN'. Exitting."
            sys.exit()

        # ---------------------------------------------------------------- #
        # Define a simple function for setting up the SR lists and SR      #
        # specific samples/systematics                                     #
        # ---------------------------------------------------------------- #
        def addSR(type, channels, counter, srs, cr_list, nbins, low, high) :
          #  tlx.channels = [] 
            for sr in srs :
                for chan in channels :
                    currentChannel = tlx.addChannel(type, [chan+sr],nbins,low,high)
                    # ---------------------------------------------------- #
                    # Add theory uncertainties only in the SR              #
                    # ---------------------------------------------------- #
                    # TODO: before running, update these uncertainties with latest from Sarah
                    if 'Super0a' in sr :
                        currentChannel.getSample("ZV").addSystematic(  sysObj.SR0a_ZV_THEORY )
                        currentChannel.getSample("Top").addSystematic( sysObj.SR0a_Top_THEORY )
                        currentChannel.getSample("WW").addSystematic(  sysObj.SR0a_WW_THEORY)
                        if chan=='ee':
                            currentChannel.getSample("Fake").addSystematic( sysObj.eeSR0a_FakeRelUnc )
                        elif chan=='mm':
                            currentChannel.getSample("Fake").addSystematic( sysObj.mmSR0a_FakeRelUnc )
                        elif chan=='em':
                            currentChannel.getSample("Fake").addSystematic( sysObj.emSR0a_FakeRelUnc )
                    elif 'Super0b' in sr :
                        currentChannel.getSample("ZV").addSystematic(  sysObj.SR0b_ZV_THEORY )
                        currentChannel.getSample("Top").addSystematic( sysObj.SR0b_Top_THEORY )
                        currentChannel.getSample("WW").addSystematic(  sysObj.SR0b_WW_THEORY)
                        if chan=='ee':
                            currentChannel.getSample("Fake").addSystematic( sysObj.eeSR0b_FakeRelUnc )
                        elif chan=='mm':
                            currentChannel.getSample("Fake").addSystematic( sysObj.mmSR0b_FakeRelUnc )
                        elif chan=='em':
                            currentChannel.getSample("Fake").addSystematic( sysObj.emSR0b_FakeRelUnc )
                    elif 'Super0c' in sr :
                        currentChannel.getSample("ZV").addSystematic(  sysObj.SR0c_ZV_THEORY )
                        currentChannel.getSample("Top").addSystematic( sysObj.SR0c_Top_THEORY )
                        currentChannel.getSample("WW").addSystematic(  sysObj.SR0c_WW_THEORY)
                        if chan=='ee':
                            currentChannel.getSample("Fake").addSystematic( sysObj.eeSR0c_FakeRelUnc )
                        elif chan=='mm':
                            currentChannel.getSample("Fake").addSystematic( sysObj.mmSR0c_FakeRelUnc )
                        elif chan=='em':
                            currentChannel.getSample("Fake").addSystematic( sysObj.emSR0c_FakeRelUnc )
                    elif 'Super1a' in sr :
                        currentChannel.getSample("ZV").addSystematic(  sysObj.SR1a_ZV_THEORY )
                        currentChannel.getSample("Top").addSystematic( sysObj.SR1a_Top_THEORY )
                        currentChannel.getSample("WW").addSystematic(  sysObj.SR1a_WW_THEORY)
                        if chan=='ee':
                            currentChannel.getSample("Fake").addSystematic( sysObj.eeSR1a_FakeRelUnc )
                        elif chan=='mm':
                            currentChannel.getSample("Fake").addSystematic( sysObj.mmSR1a_FakeRelUnc )
                        elif chan=='em':
                            currentChannel.getSample("Fake").addSystematic( sysObj.emSR1a_FakeRelUnc )
                    elif 'Super1b' in sr :
                        currentChannel.getSample("ZV").addSystematic(  sysObj.SR1b_ZV_THEORY )
                        currentChannel.getSample("Top").addSystematic( sysObj.SR1b_Top_THEORY )
                        currentChannel.getSample("WW").addSystematic(  sysObj.SR1b_WW_THEORY)
                        if chan=='ee':
                            currentChannel.getSample("Fake").addSystematic( sysObj.eeSR1b_FakeRelUnc )
                        elif chan=='mm':
                            currentChannel.getSample("Fake").addSystematic( sysObj.mmSR1b_FakeRelUnc )
                        elif chan=='em':
                            currentChannel.getSample("Fake").addSystematic( sysObj.emSR1b_FakeRelUnc )
                    elif 'Super1c' in sr :
                        currentChannel.getSample("ZV").addSystematic(  sysObj.SR1c_ZV_THEORY )
                        currentChannel.getSample("Top").addSystematic( sysObj.SR1c_Top_THEORY )
                        currentChannel.getSample("WW").addSystematic(  sysObj.SR1c_WW_THEORY)
                        if chan=='ee':
                            currentChannel.getSample("Fake").addSystematic( sysObj.eeSR1c_FakeRelUnc )
                        elif chan=='mm':
                            currentChannel.getSample("Fake").addSystematic( sysObj.mmSR1c_FakeRelUnc )
                        elif chan=='em':
                            currentChannel.getSample("Fake").addSystematic( sysObj.emSR1c_FakeRelUnc )

                    # ---------------------------------------------------- #

                    srList.append( currentChannel )
                    srList[counter].userOverflowBing=True
                    srList[counter].userUnderflowBing=True
            
                    counter += 1
            
            return counter
        # ---------------------------------------------------------------- #
        
        # Now add the channels
        srCounter = addSR("cuts", channels, srCounter, srs, crList, 1, 0.5, 1.5)
        tlx.setSignalChannels(srList)
        userPrint("Setting up signal [END]")

        # ---------------------------------------------------------------- #

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
# TODO
            sigSample.addSystematic(sysObj.AR_all_JES_MC)
            sigSample.addSystematic(sysObj.AR_all_JER_MC)
#            sigSample.addSystematic(sysObj.AR_all_JVF_MC)
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
            #sigSample.addSystematic(sysObj.AR_all_PILEUP_MC)
            sigSample.addSystematic(sysObj.AR_all_TRIGGERE_MC)
            sigSample.addSystematic(sysObj.AR_all_TRIGGERM_MC)
            sigSample.setNormFactor('mu_SIG',1.,0.,10.)

            # Add the sample to the exclusion
            exclusion.addSamples(sigSample)
            exclusion.setSignalSample(sigSample)

            print s, 'Leaving LOOP ---!!!'
