#!/usr/bin python

#########################################
## Place for holding information about
## the signal grid
## We will store the signal point information
## in the susyinfo/ directory and this
## class will parse the files there
## for the mass info for the requested
## grid.
#########################################

import os
import sys
sys.path.append(os.environ['LIMITDIR'])


class SignalGrid :
    def __init__(self, name_ = "", dbg_ = False) :
        self.name = name_
        self.verbose = dbg_

        self.sampleList = self.buildSamples(name_)

    def getSampleList(self) :
        return self.sampleList


    def buildSamples(self, name) :
        """
        Expects first line to be header.
        Subsequent lines have first entry the DSID
        and others the particle masses:
            DSID mX mY mZ ...
        """
        samples = []

        info_dir = os.environ['LIMITDIR'] + "/susyinfo/" 
        grid_info = "grid_" + name + ".txt"
        if self.verbose :
            print "Looking for signal grid info in file: %s"%(info_dir + grid_info)
        filename = info_dir + grid_info 
        if os.path.isfile(filename) :
            print " > File found."
            lines = open(filename).readlines()
            for line in lines :
                sample_info = ""
                if not line : continue
                if line.startswith('#') : continue
                line = line.strip()
                line = line.split()


                ###############################################
                ### 3-body grid
                ### stop -> bWN
                ###############################################
                if 'bWN' in name :
                    sample_info += "bWN_" + "%.1f"%(float(line[1])) + "_" + "%.1f"%(float(line[2]))
                    samples.append(sample_info)

        else :
            print 'Signal info for requested grid "%s" not located in expected directory (%s)'%(name, filename)
            print ' --> Exitting.'
            sys.exit()

        if len(samples)==0 :
            print 'No samples found in requested file: %s'%(info_dir + grid_info)
            print ' --> Exitting.'
            sys.exit()

        return samples


