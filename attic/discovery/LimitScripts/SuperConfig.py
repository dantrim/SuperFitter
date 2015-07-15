#####################################################
## SuperConfig.py for the 2L Super-Razor analysis  ##
## for running limits and fits.                    ##
##                                                 ##
## - Dantrim, 5/12/2014                            ##
#####################################################

import sys
import os

# HistFitter machinery
from configManager import configMgr
from configWriter  import TopLevelXML, Measurement, ChannelXML, Sample

# ROOT ish (for making plots)
from ROOT import kBlack,kWhite,kGray,kRed,kPink,kMagenta,kViolet,kBlue,kAzure,kCyan,kTeal,kGreen,kSpring,kYellow,kOrange,kDashed
from ROOT import TCanvas,TLegend,TLegendEntry
from systematic import Systematic
from math import sqrt
from ROOT import gROOT
import ROOT
ROOT.gROOT.LoadMacro("./macros/AtlasStyle.C")
ROOT.SetAtlasStyle()

# User defined modules
sys.path.append("./LimitScripts")
from ConfigDefs                 import *
from RuntimeOptions             import *
from SelectionConfig            import *
from SystematicObject           import *
from SetSimultaneousFitOptions  import *

configName = "SuperConfig"

##############################################################
## Read-in the user-input :                                 ##
##      (1) Signal region choice                            ##
##      (2) Dilepton channel                                ##
##      (3) The signal grid/ model                          ##
##############################################################

# possible inputs
SignalRegionChoices = [ "Super0a" , "Super0b" , "Super0c" , 
                        "Super1a" , "Super1b" , "Super1c" 
                      ]
ChannelChoices      = [ "all" , "ee" , "mm" , "em" ]

GridChoices         = ["SMCwslep"  , "SMCwslep0" , "SMCwslep1" ,
                       "SMCwslep2" , "SMCwslep3" , "SMCwslep4"
                      ]
SysChoices          = [ "NoSys" , "up" , "down" ]

inputs = sys.argv
_signalRegion = ""
_channel      = ""
_grid         = ""
_sigUncert    = ""

for inp in inputs :
    if   inp in SignalRegionChoices : _signalRegion = inp
    elif inp in ChannelChoices      : _channel      = inp
    elif inp in GridChoices         : _grid         = inp
    elif inp in SysChoices          : _sigUncert    = inp

if _signalRegion == "" :
    print configName + " ! Signal region not found in inputs,"
    print inputs
    print "Exitting."
    sys.exit()
if _channel == "" :
    print configName + " ! Dilepton channel not found in inputs,"
    print inputs
    print "Exitting."
    sys.exit()
if _grid == "" :
    print configName + " ! Grid not found in inputs,"
    print inputs
    print "Exitting."
    sys.exit()
if _sigUncert == "" :
    print configName + " ! Signal uncertainty not found in inputs,"
    print inputs
    print "Exitting."  
    sys.exit()

print " ---------------------------------------------- "
print " >>> Signal region        : ", _signalRegion
print " >>> Channel              : ", _channel
print " >>> Grid                 : ", _grid
print " >>> Systematic Variation : ", _sigUncert
print " ----------------------------------------------\n "

##############################################################
## Set the input files for the samples                      ##
##############################################################
# TODO: run a check on whether the file exists or not. Exit if not. (batch node can't read /local/scratch/ !! )
#
# MC directory for WW, ZV, Higgs
indirMC     = "/gdata/atlas/dantrim/SusyAna/histoAna/TAnaOutput/R8_Oct_7/Processed/"
bkgFile     = indirMC + "HFT_BG8TeV.root"
#
# MC directory for Top  
indirTop   = "/gdata/atlas/dantrim/SusyAna/histoAna/TAnaOutput/top/T0_Dec2/Processed/"
topFile    = indirTop + "top_105861.root"
#
# MC directory for Z+jets
indirZjets  = "/gdata/atlas/dantrim/SusyAna/histoAna/TAnaOutput/zjets/Z0_hightstats/Processed/"
zjetsFile  = indirZjets + "zjets_upstats.root"
#
# Directory for Data samples
indirData   = "/gdata/atlas/dantrim/SusyAna/histoAna/TAnaOutput/R8_Oct_7/Processed/"
dataFile   = indirData + "HFT_BG8TeV.root"
#
# Directory for fake sample
indirFake   = "/gdata/atlas/dantrim/SusyAna/histoAna/TAnaOutput/fakes/F1_Dec3/razor/Processed/"
fakeFile   = indirFake + "fakes_Dec3Matrix_razor.root"
#
# MC directory for SMCwslep signal samples
indirSig    = "/gdata/atlas/dantrim/SusyAna/histoAna/TAnaOutput/SMCwslep/S0_Dec2/Processed/"
signalFile = ""
if "SMCwslep" in _grid:
    signalFile = indirSig + "HFT_SMCwslep8TeV.root"
if signalFile == "": sys.exit()

checkFiles = [ bkgFile, topFile, zjetsFile, dataFile, fakeFile, signalFile ]
for file in checkFiles :
    badInputs = []
    if not os.path.exists(file) :
        badInputs.append(file)
    if len(badInputs) != 0 :
        for bad_file in badInputs :
            print " >>> File ( %s ) not found. "%bad_file
        print " >>> Exitting."
        sys.exit()


##############################################################
## Set the analysis name                                    ##
##   -- This will be used to set the name of the directory/ ##
##      workspace in the /results directory                 ##
##############################################################
analysisName = _signalRegion + "_" + _channel + "_" + _grid

##############################################################
## Create 'ConfigDefs' instance to access the run specifics ##
##############################################################
userDefs = ConfigDefs()
#
# Dilepton channel enum, default = 'all'
_ch = userDefs.all
if "ee" in _channel : _ch = userDefs.ee
if "mm" in _channel : _ch = userDefs.mm
if "em" in _channel : _ch = userDefs.em

##############################################################
## Specifiy whether to set bkg constraining samples         ##
##############################################################
fitWW   = True
fitTop  = True
fitZV   = True

##############################################################
## Communicate fit options to HistFitter through            ##
## RuntimeOptions                                           ##
##############################################################
# TODO: remove handedness
_sleptonHand = userDefs.RightLeftHand
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
                          _sleptonHand,             # slepton handedness
                          bkgFile,                  # input bkg file
                          dataFile,                 # input data file
                          signalFile,               # input signal file
                          analysisName,             # Analysis Name for saving
                          20.3,                     # Input Lumi units
                          20.3,                     # Ouput Lumi units
                          "fb-1"                    # Input Lumi units
                          )

##############################################################
## Define Data and BG samples                               ##
##############################################################
dataSample       = Sample("Data_CENTRAL", ROOT.kBlack    )
zjetsSample      = Sample("Zjets"       , ROOT.kGreen+2  )
higgsSample      = Sample("Higgs"       , ROOT.kYellow   )
zvSample         = Sample("ZV"          , ROOT.kGreen    )
wwSample         = Sample("WW"          , ROOT.kAzure-4  )
topSample        = Sample("Top"         , ROOT.kViolet   )
fakeSample       = Sample("Fake"        , ROOT.kOrange-4 )


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                 USER SHOULD NOT HAVE TO EDIT BELOW HERE                                      #
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #

##############################################################
## USER DEFINED FUNCTIONS [BEGIN]                           ##
##############################################################

# print message
def userPrint(message) :
    print "\t"+configName+":\t " + message
    return

#
# Function for adding the systematics to each Sample
#
def addSys(sample, doSimFit, sysObj):
    if doSimFit:
        sample.addSystematic(sysObj.AR_all_JES_CR)
        sample.addSystematic(sysObj.AR_all_JER_CR)
#        sample.addSystematic(sysObj.AR_all_JVF_CR)   TODO : see about JVF uncertainties
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

##############################################################
## USER DEFINED FUNCTIONS [END]                             ##
##############################################################


##############################################################
## Blind the regions set by  RuntimeOptions                 ##
##############################################################
userPrint("Specifying the options for blinding SR/CR/VR")

if userOpts.blindSR :
    userPrint(" >>> Blinding signal regions")
    configMgr.blindSR = userOpts.blindSR
if userOpts.blindCR :
    userPrint(" >>> Blinding control regions")
    configMgr.blindCR = userOpts.blindCR
if userOpts.blindVR :
    userPrint(" >>> Blinding validation regions")
    configMgr.blindVR = userOpts.blindVR

##############################################################
## Toys vs. asymptotic                                      ##
##############################################################
userPrint("Setting up toys vs. asymptotic calculation")

# calculatorType  ==> Calculator type   0: Frequentist, 1: Hybrid, 2: Asymptotic
# testStatType    ==> Test statistic type       0: LEP, 1: Tevatron, 2: Profile Likelihood, 3: One sided PL
# nPoints         ==> Number of scan points for the POI if the interval is fixed

calculators = [ "Frequentist", "Hybrid", "Asymptotic" ]
teststatistics = [ "LEP", "Tevatron" , "Profile-Likelihood", "One-sided PL" ]

if not userOpts.doToys :
    configMgr.calculatorType = 2
else :
    configMgr.calculatorType = 0
    configMgr.nTOYS = userOpts.nToys
    toyindex = 2
configMgr.testStatType = 3
configMgr.nPoints      = 20
configMgr.writeXML     = True

userPrint(" >>> Calculator type: %s"%calculators[configMgr.calculatorType])
if configMgr.calculatorType == 0 :
    userPrint(" >>> Number of toys: %d"%configMgr.nTOYS)
userPrint(" >>> Test statistic type: %s"%teststatistics[configMgr.testStatType])
userPrint(" >>> Number of scan points for POI: %d"%configMgr.nPoints)

##############################################################
## Specify the fit mode                                     ##
##############################################################
userPrint("Specifiying the Fit Mode")

if userOpts.doExclusion : configMgr.doExclusion = True
if userOpts.doDiscovery : configMgr.doExclusion = False

# cannot do validation and exclusion at the same time, choose one
if userOpts.doValidation and userOpts.doExclusion :
    userPrint(" >>> Can't do validation and exclusion at the same time, setting validation to false")
    userOpts.doValidation = False

if userOpts.doExclusion :
    userPrint( " >>> Running Exclusion (model-dependent) fit")
if userOpts.doDiscovery :
    userPrint( " >>> Running Discovery (model-independent) fit")
if userOpts.doValidation :
    userPrint( " >>> Running Background-Only fit")

##############################################################
## Specify the output files                                 ##
##############################################################
userPrint("Specifying the output files for HistFitter")

# ananame
configMgr.analysisName = userOpts.anaName + "_" + userOpts.sigUncert

# specify where histos will be sent
configMgr.histCacheFile = "data/" + configMgr.analysisName + ".root"

# specify the output file based on wehter we do toys or not
if not userOpts.doToys :
    configMgr.outputFileName = "results/"+configMgr.analysisName + "_Output.root"
else :
    configMgr.outputFileName = "results/"+configMgr.analysisName+"_"+userOpts.gridForToys+"_withToys"+userOpts.sigUncert+"_"+userOpts.signalRegion+"_"+str(toyindex)+"_Output.root"

##############################################################
## Set the luminosity                                       ##
##############################################################
userPrint("Specifying Luminosity")

configMgr.inputLumi     = userOpts.inputLumi
configMgr.outputLumi    = userOpts.outputLumi
configMgr.setLumiUnits( userOpts.lumiUnits )

userPrint(" >>> Input luminosity  : %s"%str(configMgr.inputLumi))
userPrint(" >>> Output luminosity : %s"%str(configMgr.outputLumi))
userPrint(" >>> Luminosity units  : %s"%str(userOpts.lumiUnits))

##############################################################
## Specify the background MC input files                    ##
##############################################################
userPrint("Specifying the background input")

mcSamples = [ higgsSample, zvSample, wwSample, dataSample ]

bkgFiles   = []
topFiles   = []
zjetsFiles = []

bkgFiles.append( userOpts.bkgFile )
topFiles.append( topFile )
zjetsFiles.append( zjetsFile )

for sample in mcSamples :
    # assign higgs, zv, ww, and data to HFT_BG8TeV
    sample.setFileList(bkgFiles)
# assign top and zjets to their specific files
topSample.setFileList(topFiles)
zjetsSample.setFileList(zjetsFiles)

##############################################################
## Configure the selection                                  ##
##############################################################
userPrint("Configuring selection")
configMgr = selectionConfig(configMgr, userOpts.slepLimitN)

##############################################################
## Configure weight                                         ##
##############################################################
userPrint("Specifying Weight")
configMgr.weights = ["eventweight"]

##############################################################
## Set up the systematics                                   ##
##############################################################
userPrint("Configuring systematic")
configMgr.nomName = "_CENTRAL"
sysObj = SystematicObject(configMgr, userOpts.doShape, userOpts.splitMCSys)

##############################################################
## Set up Samples and normalization factors                 ##
##############################################################
userPrint("Setting up samples, norm factors, and systematics")

# specify the parameter of interest 
tlx  = configMgr.addFitConfig("TopLvlXML")
meas = tlx.addMeasurement(name="NormalMeasurement", lumi=1., lumiErr=0.028)
meas.addPOI("mu_SIG") ## EXCL: mu_SIG, upper limi table

# determine if we should use stat
useStat = True
if userOpts.splitMCSys :
    useStat = False

# If using stat set some limits
tlx.statErrThreshold = 0.001

# define quantities to make configuration below easier
SR      = userOpts.signalRegion
lepChan = userOpts.leptonChannel

if userOpts.do2L :
    # ----------------------------------------------------- #
    #                        Zjets                          # 
    # ----------------------------------------------------- #
    zjetsSample.setStatConfig(useStat)
    if userOpts.splitMCSys :
        zjetsSample.addSystematic(sysObj.AR_mcstat_ZX)
    zjetsSample.setNormByTheory()
    zjetsSample = addSys(zjetsSample, False, sysObj)
    
    # ----------------------------------------------------- #
    #                        Higgs                          # 
    # ----------------------------------------------------- #
    higgsSample.setStatConfig(useStat)
    if userOpts.splitMCSys :
        higgsSample.addSystematic(sysObj.AR_mcstat_H)
    higgsSample.setNormByTheory()
    higgsSample = addSys(higgsSample, False, sysObj)

    # ----------------------------------------------------- #
    #                          ZV                           # 
    # ----------------------------------------------------- #

    zvSample.setStatConfig(useStat)
    if userOpts.splitMCSys :
        zvSample.addSystematic(sysObj.AR_mcstat_ZV)

    # Determine the normalization region :
    #    --> If zero jet : pick "a" CR
    #    --> If one jet  : pick "b" CR
    if userOpts.doSimFit2LZV :
        if('Super0a' in SR or 'Super0b' in SR or 'Super0c' in SR) :
            zvSample.setNormRegions([("emCRZV14a", "cuts")])
            userPrint(" >>> Normalization region for ZV : emCRZV14a")
        elif('Super1a' in SR or 'Super1b' in SR or 'Super1c' in SR) :
            zvSample.setNormRegions([("emCRZV14b", "cuts")])
            userPrint(" >>> Normalization region for ZV : emCRZV14b")
    # add systematics
    zvSample = addSys(zvSample, userOpts.doSimFit2LZV, sysObj)
    # set normalization factor
    if userOpts.doSimFit2LZV :
        if('Super0a' in SR or 'Super0b' in SR or 'Super0c' in SR) :
            zvSample.setNormFactor("mu_ZV14a", 1.,0.,10.)
            userPrint(" >>> Normalization factor for ZV : mu_ZV14a")
        elif('Super1a' in SR or 'Super1b' in SR or 'Super1c' in SR) :
            zvSample.setNormFactor("mu_ZV14b", 1., 0., 10.)
            userPrint(" >>> Normalization factor for ZV : mu_ZV14b")
    else :
        zvSample.setNormByTheory()

    # ----------------------------------------------------- #
    #                         TOP                           # 
    # ----------------------------------------------------- #

    topSample.setStatConfig(useStat)
    if userOpts.splitMCSys :
        topSample.addSystematic(sysObj.AR_mcstat_TOP)

    # Determine the normalization region :
    #    --> If zero jet : pick "a" CR
    #    --> If one jet  : pick "b" CR
    if userOpts.doSimFit2LTop :
        if('Super0a' in SR or 'Super0b' in SR or 'Super0c' in SR) :
            topSample.setNormRegions([("emCRTop14a", "cuts")])
            userPrint(" >>> Normalization region for Top : emCRTop14a")
        elif('Super1a' in SR or 'Super1b' in SR or 'Super1c' in SR) :
            topSample.setNormRegions([("emCRTop14b", "cuts")])
            userPrint(" >>> Normalization region for Top : emCRTop14b")
    # add systematics
    topSample = addSys(topSample, userOpts.doSimFit2LTop, sysObj)
    # set normalization factor
    if userOpts.doSimFit2LTop :
        if('Super0a' in SR or 'Super0b' in SR or 'Super0c' in SR) :
            topSample.setNormFactor("mu_Top14a", 1.,0.,10.)
            userPrint(" >>> Normalization factor for Top : mu_Top14a")
        elif('Super1a' in SR or 'Super1b' in SR or 'Super1c' in SR) :
            topSample.setNormFactor("mu_Top14b", 1., 0., 10.)
            userPrint(" >>> Normalization factor for Top : mu_Top14b")
    else :
        topSample.setNormByTheory()
    
    # ----------------------------------------------------- #
    #                         WW                            # 
    # ----------------------------------------------------- #

    wwSample.setStatConfig(useStat)
    if userOpts.splitMCSys :
        wwSample.addSystematic(sysObj.AR_mcstat_WW)

    # Determine the normalization region :
    #    --> If zero jet : pick "a" CR
    #    --> If one jet  : pick "b" CR
    if userOpts.doSimFit2LWW :
        if('Super0a' in SR or 'Super0b' in SR or 'Super0c' in SR) :
            wwSample.setNormRegions([("emCRWW14a", "cuts")])
            userPrint(" >>> Normalization region for WW : emCRWW14a")
        elif('Super1a' in SR or 'Super1b' in SR or 'Super1c' in SR) :
            wwSample.setNormRegions([("emCRWW14b", "cuts")])
            userPrint(" >>> Normalization region for WW : emCRWW14b")
    # add systematics
    wwSample = addSys(wwSample, userOpts.doSimFit2LWW, sysObj)
    # set normalization factor
    if userOpts.doSimFit2LWW :
        if('Super0a' in SR or 'Super0b' in SR or 'Super0c' in SR) :
            wwSample.setNormFactor("mu_WW14a", 1.,0.,10.)
            userPrint(" >>> Normalization factor for WW : mu_WW14a")
        elif('Super1a' in SR or 'Super1b' in SR or 'Super1c' in SR) :
            wwSample.setNormFactor("mu_WW14b", 1., 0., 10.)
            userPrint(" >>> Normalization factor for WW : mu_WW14b")
    else :
        wwSample.setNormByTheory()
    
    # ----------------------------------------------------- #
    #                        Data                           # 
    # ----------------------------------------------------- #

    dataSample.setData()

    # ----------------------------------------------------- #
    #                        Fakes                          # 
    # ----------------------------------------------------- #
    
    # Set by hand the fake estimates per-region.
    # The regions in which we expect a negative yield, set the
    # yield to 0.1 but keep the overal relative uncertainty

    fakeSample.buildHisto([0.1],   "eeSuper0a",  "cuts")
    fakeSample.buildHisto([0.1],   "mmSuper0a",  "cuts")
    fakeSample.buildHisto([0.1],   "emSuper0a",  "cuts")
    fakeSample.buildHisto([0.1],   "eeSuper0b",  "cuts")
    fakeSample.buildHisto([0.1],   "mmSuper0b",  "cuts")
    fakeSample.buildHisto([0.1],   "emSuper0b",  "cuts")
    fakeSample.buildHisto([0.02],  "eeSuper0c",  "cuts")
    fakeSample.buildHisto([0.1],   "mmSuper0c",  "cuts")
    fakeSample.buildHisto([0.1],   "emSuper0c",  "cuts")
    fakeSample.buildHisto([3.46],  "eeSuper1a",  "cuts")
    fakeSample.buildHisto([4.18],  "mmSuper1a",  "cuts")
    fakeSample.buildHisto([3.62],  "emSuper1a",  "cuts")
    fakeSample.buildHisto([0.55],  "eeSuper1b",  "cuts")
    fakeSample.buildHisto([0.1],   "mmSuper1b",  "cuts")
    fakeSample.buildHisto([0.57],  "emSuper1b",  "cuts")
    fakeSample.buildHisto([1.70],  "eeSuper1c",  "cuts")
    fakeSample.buildHisto([4.23],  "mmSuper1c",  "cuts")
    fakeSample.buildHisto([1.72],  "emSuper1c",  "cuts")
    fakeSample.buildHisto([37.91], "emCRTop14a", "cuts")
    fakeSample.buildHisto([3.46],  "emCRTop14b", "cuts")
    fakeSample.buildHisto([46.96], "emCRWW14a",  "cuts")
    fakeSample.buildHisto([35.64], "emCRWW14b",  "cuts")
    fakeSample.buildHisto([0.1],   "emCRZV14a",  "cuts")
    fakeSample.buildHisto([0.1],   "emCRZV14a",  "cuts")

    fakeSample.setStatConfig(useStat)
    fakeSample.setNormByTheory()



##############################################################
## Set the samples to use                                   ##
##############################################################
userPrint("Setting samples to use")

tlx.addSamples([fakeSample, wwSample, topSample, zvSample, zjetsSample, higgsSample, dataSample] )

##############################################################
## Setup plotting                                           ##
##############################################################
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
    entry = addEntry(entry,leg,"Z+jets",zjetsSample.color,zjetsSample.color,compFillStyle)

# Set the legend
tlx.tLegend = leg

##############################################################
## Setup the simultaneous fit options                       ##
##############################################################
userPrint("Setting up simultaneous fit options")

# get the control region list for fitting
crList  = getCRFitList(tlx,
                        userOpts.signalRegion,
                        userOpts.leptonChannel,
                        userOpts.doSimFit2LWW,
                        userOpts.doSimFit2LTop,
                        userOpts.doSimFit2LZV,
                        userDefs,
                        sysObj )

if userOpts.doSimFit2LWW or userOpts.doSimFit2LTop or userOpts.doSimFit2LZV :
    tlx.setBkgConstrainChannels(crList)

##############################################################
## Setup the signal regions                                 ##
##############################################################

if userOpts.doExclusion or userOpts.doValidation :
    userPrint("Setting up signal/validation regions")
    
    srList      = []
    srCounter   = 0
    lepChan     = userOpts.leptonChannel
    SR          = userOpts.signalRegion

    channels = []
    if lepChan == userDefs.all  : channels = [ 'ee' , 'mm' , 'em' ]
    if lepChan == userDefs.ee   : channels = [ 'ee' ]
    if lepChan == userDefs.mm   : channels = [ 'mm' ]
    if lepChan == userDefs.em   : channels = [ 'em' ]
    if lepChan == userDefs.eemm : channels = [ 'ee' , 'mm' ]

    
    # function for configuring the signal regions and signal region specifics
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
            elif 'Super1a' in SR :
                currentChannel.getSample("ZV").addSystematic( sysObj.SR1a_ZV_THEORY)
                currentChannel.getSample("Top").addSystematic(sysObj.SR1a_Top_THEORY)
                currentChannel.getSample("WW").addSystematic( sysObj.SR1a_WW_THEORY)
                if chan=='ee':
                    currentChannel.getSample("Fake").addSystematic( sysObj.eeSR1a_FakeRelUnc)
                elif chan=='mm':
                    currentChannel.getSample("Fake").addSystematic( sysObj.mmSR1a_FakeRelUnc)
                elif chan=='em':
                    currentChannel.getSample("Fake").addSystematic( sysObj.emSR1a_FakeRelUnc)
            elif 'Super1b' in SR :
                currentChannel.getSample("ZV").addSystematic( sysObj.SR1b_ZV_THEORY)
                currentChannel.getSample("Top").addSystematic(sysObj.SR1b_Top_THEORY)
                currentChannel.getSample("WW").addSystematic( sysObj.SR1b_WW_THEORY)
                if chan=='ee':
                    currentChannel.getSample("Fake").addSystematic( sysObj.eeSR1b_FakeRelUnc)
                elif chan=='mm':
                    currentChannel.getSample("Fake").addSystematic( sysObj.mmSR1b_FakeRelUnc)
                elif chan=='em':
                    currentChannel.getSample("Fake").addSystematic( sysObj.emSR1b_FakeRelUnc)
            elif 'Super1c' in SR :
                currentChannel.getSample("ZV").addSystematic( sysObj.SR1c_ZV_THEORY)
                currentChannel.getSample("Top").addSystematic(sysObj.SR1c_Top_THEORY)
                currentChannel.getSample("WW").addSystematic( sysObj.SR1c_WW_THEORY)
                if chan=='ee':
                    currentChannel.getSample("Fake").addSystematic( sysObj.eeSR1c_FakeRelUnc)
                elif chan=='mm':
                    currentChannel.getSample("Fake").addSystematic( sysObj.mmSR1c_FakeRelUnc)
                elif chan=='em':
                    currentChannel.getSample("Fake").addSystematic( sysObj.emSR1c_FakeRelUnc)
    
                
            srList.append( currentChannel )
            srList[counter].userOverflowBin=True
            if shapeFit:
                srList[counter].userUnderflowBin=False
            else:
                srList[counter].userUnderflowBin=True
    
            counter+=1
        return counter

    # add the channels
    srCounter = addSR("cuts", channels, srCounter, SR, 1, 0.5, 1.5, False)
    
    if userOpts.doValidation :
        tlx.setValidationChannels(srList)
        for valchan in srList :
            userPrint(" >>> Setting validation channel: %s"%str(valchan.channelName))
    else:
        tlx.setSignalChannels(srList)
        for sigchan in srList :
            userPrint(" >>> Setting signal channel: %s"%str(sigchan.channelName))
        
##############################################################
## Setup discovery fit                                      ##
##############################################################
if userOpts.doDiscovery :
    userPrint("Setting up discovery fit")
    
    srChanName = ""
    if userOpts.leptonChannel == userDefs.ee : srChanName += "ee"
    if userOpts.leptonChannel == userDefs.mm : srChanName += "mm"
    if userOpts.leptonChannel == userDefs.em : srChanName += "em"
    srChanName += userOpts.signalRegion
    discoChannel = tlx.addChannel("cuts", [srChanName], 1, 0, 1)
    discoChannel.addDiscoverySamples(["SIG"], [1.], [0.], [100.], [kRed])
    if userOpts.splitMCSys :
        discoChannel.addSystematic(sysObj.AR_mcstat_SIG)
    tlx.setSignalChannels(discoChannel)

##############################################################
## Setting grid to do exclusion                             ##
##############################################################
if userOpts.doExclusion :
    userPrint("Setting the grid for exclusion")
    sigSamples = []
    
    if "SMCwslep" in userOpts.sigGrid : sigSamples = userDefs.getGrid(userOpts.sigGrid)
    else :
        userPrint(" >>> Could not determine a grid to run on.")
        userPrint(" >>> Exitting.")
        sys.exit()

    # now loop over signal samples
    userPrint(" >>> Looping over signal samples")
    for s in sigSamples[:1] :
        signame = s
        
        doToys   = userOpts.doToys
        hasHippo = doToys and 'hippo' in userOpts.gridForToys
        hasSig   = doToys and signame in userOpts.gridForToys
        
        if not doToys or hasHippo or hasSig :
            exclusion = configMgr.addFitConfig(tlx, 'TopLvlXML_Exclusion_%s'%s)
            userPrint(" >>> !!! --- in LOOP %s"%s)
            sigSample = Sample(s, kRed)
            sigSample.setStatConfig(useStat)
            if userOpts.splitMCSys :
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

            userPrint(" >>> %s Leaving LOOP --- !!!"%s)



