#!/bin/env python

#############################################
# Script to clean up the names in the       #
# bkg-fit and sys tables to match those     #
# in the support note                       #
#                                           #
# author: Daniel Antrim                     #
# date  : January 20, 2015                  #
#############################################

import glob
import optparse
import sys

#############################################
#               name-maps                   #
##                                         ##

labels={}
labels["eeSuper0a"] = "eeSR0a"
labels["mmSuper0a"] = "mmSR0a"
labels["emSuper0a"] = "emSR0a"

labels["eeSuper0b"] = "eeSR0b"
labels["mmSuper0b"] = "mmSR0b"
labels["emSuper0b"] = "emSR0b"

labels["eeSuper0c"] = "eeSR0c"
labels["mmSuper0c"] = "mmSR0c"
labels["emSuper0c"] = "emSR0c"

labels["eeSuper1a"] = "eeSR1a"
labels["mmSuper1a"] = "mmSR1a"
labels["emSuper1a"] = "emSR1a"

labels["eeSuper1b"] = "eeSR1b"
labels["mmSuper1b"] = "mmSR1b"
labels["emSuper1b"] = "emSR1b"

labels["eeSuper1c"] = "eeSR1c"
labels["mmSuper1c"] = "mmSR1c"
labels["emSuper1c"] = "emSR1c"

namemap={}
# bkg naming
namemap['emCRTop14a'] = "CRTop$_a$"
namemap['emCRTop14b'] = "CRTop$_b$"
namemap['emCRWW14a']  = "CRWW$_a$"
namemap['emCRWW14b']  = "CRWW$_b$"
namemap['emCRZV14a']  = "CRZV$_a$"
namemap['emCRZV14b']  = "CRZV$_b$"
namemap['Super0']     = "SR2\lep-0"
namemap['Super1']     = "SR2\lep-1"

def set_naming(type, file, region) :
    lines = open(file).readlines()
    with open(file, 'w') as f:
        for line in lines:
            if type=='sys' :
                if 'gamma' in line and region not in line :
                    line = "%" + line
                if "(MC)" in line :
                    line = "%" + line
            if "label" in line and "Super0" in region :
                line = line.replace("table.results.yields.fit.emCRTop14a_emCRWW14a_emCRZV14a_%s"%region, "tab:DISCO%s"%labels[region])
            elif "label" in line and "Super1" in region :
                line = line.replace("table.results.yields.fit.emCRTop14b_emCRWW14b_emCRZV14b_%s"%region, "tab:DISCO%s"%labels[region])
        
            for old, new in namemap.iteritems() :
                line = line.replace(old, new)
            line = line.replace("\\begin{center}", "\\centering")
            line = line.replace("\\end{center}", "")
            line = line.replace("\\end{tabular*}", "\\end{tabular*}")
            line = line.replace("20.5","20.3")
            line = line.replace("Background fit results", "Discovery fit results")
            line = line.replace("DiscoveryMode_SIG", "DiscoverMode\\_SIG")
    

            f.write(line)

def parse_options():
    parser = optparse.OptionParser()
    parser.add_option('-t', '--type', default='bkg', help='cleaning up "bkg" or "sys" tables')
    parser.add_option('-i', '--input', default='./bkgFitYields/', help='give directory containing the .tex tables')
    (options, args) = parser.parse_args()
    return options

def grabfiles(dir) :
    files = glob.glob(dir + "*.tex")
    return files

def region_from_filename(file) :
    lep = ''
    reg = ''
    if 'ee' in file : lep = 'ee'
    elif 'mm' in file : lep = 'mm'
    elif 'em' in file : lep = 'em'

    if 'Super0a' in file   : reg = 'Super0a'
    elif 'Super0b' in file : reg = 'Super0b'
    elif 'Super0c' in file : reg = 'Super0c'
    elif 'Super1a' in file : reg = 'Super1a'
    elif 'Super1b' in file : reg = 'Super1b'
    elif 'Super1c' in file : reg = 'Super1c'

    return lep + reg
    



##############################################
if __name__=='__main__' :

    options = parse_options()
    type = options.type
    indir = options.input

    table_files = grabfiles(indir)
    
   
    for file in table_files : 
        region = region_from_filename(file)
        set_naming(type, file, str(region))
