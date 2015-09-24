#!/usr/bin python
"""
###################################################
## SuperFitter                                   ##
##                                               ##
##          HistFitter configuration             ##
##                                               ##
##           http://bit.ly/1KTbAoV               ##
##                                               ##
## --------------------------------------------- ##
##  daniel antrim                                ##
##  daniel.joseph.antrim@cern.ch                 ##
##  September 2015                               ##
###################################################
"""
### histfitter imports
from configManager import configMgr
from configWriter import fitConfig,Measurement,Channel,Sample
from systematic import Systematic

### "std" imports
from math import sqrt
import os
import sys
from optparse import OptionParser


### ROOT imports
from ROOT import kBlack,kWhite,kGray,kRed,kPink,kMagenta,kViolet,kBlue,kAzure,kCyan,kTeal,kGreen,kSpring,kYellow,kOrange 
from ROOT import gROOT
import ROOT

### SuperFitter imports
sys.path.append(os.environ['LIMITDIR'])
import RegionDefs # this is where all of the selections are defined

regContainer = RegionDefs.buildRegions()
regContainer.Print()
cutdict = regContainer.getDict()
print cutdict

#####################################################################
### parse the user input
parser = OptionParser()
parser.add_option("-r", "--signalRegion", dest="signalRegion", default="")
parser.add_option("-t", "--doTheoryBand", action="store_true", dest="doTheoryBand", default=False)
(options, args) = parser.parse_args()

## take in the signal region choice
if str(options.signalRegion) not in cutdict.keys() :
    print 'SuperFitter LimitConfig ERROR    Requested signal region "%s" not supported. Check RegionDefs.buildRegions()!'%options.signalRegion
    print 'SuperFitter LimitConfig ERROR    --> Exiting.'
    sys.exit()
signalRegion = options.signalRegion

## do we want to run the theory XS band
doTheoryBand = options.doTheoryBand

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
