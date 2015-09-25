#!/usr/bin python

#########################################
## Place here a container to hold all of 
## the running options
#########################################

import sys

class RunOptions :
    """
    Force the configuration to set all
    by hand
    """
    def __init__(self) :
        self.doExcl         = False
        self.doDisco        = False
        self.doBkgOnly      = False
        self.blindSR        = True
        self.blindCR        = True
        self.blindVR        = True
        self.doTheorySys    = False
        self.calculator     = 2
        self.teststat       = 3
        self.nScanPoints    = 20
        self.grid           = ""
        self.signalRegion   = ""
        self.inputLumi      = 1.0
        self.outputLumi     = 1.0
        self.lumiUnits      = ""
        self.cutDict        = {}
        self.splitMCsys     = False ## does not need to be propagated to configMgr
        self.weights        = []

        self.n  = 0
        self.m = 0
        self.total_opt_n = 18
        self.total_opt_m = 17

        self.doCheck = True

    def setExclusion(self, doExcl_ = True) :
        self.doExcl = doExcl_
        self.n += 1
    def doExclusion(self) :
        self.m += 1
        return self.doExcl

    def setDiscovery(self, doDisco_ = True) :
        self.doDisco = doDisco_
        self.n += 1
    def doDiscovery(self) :
        self.m += 1
        return self.doDisco

    def setBackground(self, doBkg = True) :
        self.doBkgOnly = doBkg
        self.n += 1
    def doBackground(self) :
        self.m += 1
        return self.doBkgOnly

    def setBlindSR(self, blindSR = True) :
        self.blindSR = blindSR
        self.n += 1
    def doBlindSR(self) :
        self.m += 1
        return self.blindSR

    def setBlindCR(self, blindCR = True) :
        self.blindCR = blindCR
        self.n += 1
    def doBlindCR(self) :
        self.m += 1
        return self.blindCR

    def setBlindVR(self, blindVR = True) :
        self.blindVR = blindVR
        self.n += 1
    def doBlindVR(self) :
        self.m += 1
        return self.blindVR

    def setTheoryBand(self, doband_ = True) :
        self.doTheorySys = doband_
        self.n += 1
    def doTheoryBand(self) :
        self.m += 1
        return self.doTheorySys

    def setCalculatorType(self, type_ = 2) :
        self.calculator = type_
        self.n += 1
    def getCalculatorType(self) :
        self.m += 1
        return self.calculator

    def setTestStatType(self, type_ = 3) :
        self.teststat = type_
        self.n += 1
    def getTestStatType(self) :
        self.m += 1
        return self.teststat

    def setNumberOfScanPoints(self, number_ = 20) :
        self.nScanPoints = number_
        self.n += 1
    def getNumberOfScanPoints(self) :
        self.m += 1
        return self.nScanPoints

    def setGrid(self, grid = "") :
        self.grid = grid
        self.n += 1
    def getGrid(self) :
        self.m += 1
        return self.grid

    def setSignalRegion(self, sr = "") :
        self.signalRegion = sr
        self.n += 1
    def getSignalRegion(self) :
        self.m += 1
        return self.signalRegion

    def setInputLumi(self, inlumi = 1.0) :
        self.inputLumi = inlumi
        self.n += 1
    def getInputLumi(self) :
        self.m += 1
        return self.inputLumi

    def setOutputLumi(self, outlumi = 1.0) :
        self.outputLumi = outlumi
        self.n += 1
    def getOutputLumi(self) :
        self.m += 1
        return self.outputLumi

    def setLumiUnits(self, unit = "") :
        self.lumiUnits = unit
        self.n += 1
    def getLumiUnits(self) :
        self.m += 1
        return self.lumiUnits

    def setCutDict(self, indict = {} ) :
        self.cutDict = indict
        self.n += 1
    def getCutDict(self) :
        self.m += 1
        return self.cutDict

    def setSplitMCsys(self, split = False) :
        self.splitMCsys = split
        self.n += 1
    def doSplitMCsys(self) :
        self.m += 1
        return self.splitMCsys

    def setWeights(self, weights_ = [] ) :
        for w in weights_ :
            self.weights.append(w) 
        self.n += 1
    def getWeights(self) :
        self.m += 1
        return self.weights

    def check(self) :
        if self.doCheck :
            self.doCheck = False
            is_ok = False
            if self.n == self.total_opt_n : is_ok = True
            else :
                print "RunOptions ERROR    You must set all of the options!"
                print "RunOptions ERROR    Only %d/%d of the options have been set."%(self.n, self.total_opt_n)
                is_ok = False
            if self.m == self.total_opt_m : is_ok =  True
            else :
                print "RunOptions ERROR    You must propagate all of the options to configMgr!"
                print "RunOptions ERROR    Only %d/%d of the options have been retrieved."%(self.m, self.total_opt_m)
                is_ok = False

            return is_ok
        else :
            return True
        
