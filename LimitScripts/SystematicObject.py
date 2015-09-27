#!/usr/bin python

##########################################
# Container class for configuring the
# systematics
##########################################

from systematic import Systematic
import sys

class SystematicObject :
    def __init__(self, configMgr = None, splitMCSysBySample = False ) :
        if not configMgr :
            print "SystematicObject ERROR    Did not provide configMgr to SystematicObject! Exiting."
            sys.exit()

        #######################################################
        ## Dummy test
        #######################################################
        test_rel = 0.20
        self.dummySyst = Systematic("TestDummy", configMgr.weights, 1.0 + test_rel, 1.0 - test_rel, "user", "userOverallSys")


        #######################################################
        ## Get statistical uncertainty per sample if splitting
        #######################################################
        ## shapeStat : shapeSys applied to an individual sample
        ## shapeSys  : uncertainty of statistical nature applied to a sum of samples, bin by bin (hence "shape")
        if splitMCSysBySample :
            self.mcstat_TTbar = Systematic("mcstat_TTbar", "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.mcstat_WW    = Systematic("mcstat_WW",    "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
