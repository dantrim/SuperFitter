#!/usr/bin python

#############################################
## This script will parse a set of filelists

import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(True)
import glob

import os
import sys
sys.path.append(os.environ['LIMITDIR'])

class Background :
    def __init__(self, name_ = "", filelist_= "", dbg = False) :
        self.verbose = dbg
        self.name = name_
        self.filelist = filelist_
        self.dsid_list = []
        self.treefiles = {} # { sysname : list containing trees }

    def setSample(self, sample_dir = "", systematic = "") :
        self.treefiles[systematic] = []
        if len(self.dsid_list) == 0 :
            dsids = []
            lines = open(self.filelist).readlines()
            for line in lines :
                if not line : continue
                if line.startswith("#") : continue
                if "Data" not in self.name :
                    dsids.append(line[line.find('mc15_13TeV.')+11 : line.find('mc15_13TeV.')+17])
                else :
                    dsids.append(line[line.find('data15_13TeV.00')+15 : line.find('data15_13TeV.')+21])
            self.dsid_list = dsids
        raw_files = glob.glob(sample_dir + "*.root")
        files = []
        for dataset in dsids :
            for f in raw_files :
                if 'entrylist' in f : continue
                if dataset in f and systematic in f :
                    files.append(f)
                    break # move to next dsid

        self.treefiles[systematic] = files 
                     
        

###########################
## available systematics
syst = [ 'CENTRAL' ]

###########################
## backgrounds
backgrounds = []
filelist_dir      = "/gdata/atlas/dantrim/SusyAna/n0213val/Superflow/run/filelists/" 
mc_sample_dir     = "/gdata/atlas/dantrim/SusyAna/histoAna/run2early/n0213/mc/rfsr2/Raw/"
data_sample_dir   = "/gdata/atlas/dantrim/SusyAna/histoAna/run2early/n0213/data/Sep12/Raw/"

bkg_data    = Background("Data", filelist_dir + "data15_periodA_n0213.txt")
backgrounds.append(bkg_data)
bkg_ttbar   = Background("TTbar", filelist_dir + "ttbar_powheg_n0213.txt")
backgrounds.append(bkg_ttbar)
bkg_ww      = Background("WW", filelist_dir + "ww_powheg_n0213.txt")
backgrounds.append(bkg_ww)

############################
## signals

## will parse through ./LimitScripts/susyinfo/
signals = []
grid = "bWN"
sig_bWN = Background("BWN", filelist_dir + "bwn_n0213.txt")
signals.append(sig_bWN)

###################################
## setup the output file name and location
output_dir  = "./" 
output_name = "HFT_BG_13TeV.root"
output_name_sig = "HFT_bWN_13TeV.root"


if __name__=="__main__" :

    ## load the backgrounds and locate the files
    for bkg in backgrounds :
        for sys in syst :
            if "Data" in bkg.name and "CENTRAL" in sys : 
                bkg.setSample(data_sample_dir, sys)
            else :
                bkg.setSample(mc_sample_dir, sys)

    ## check that for each loaded systeamtic we have the same number
    ## of datasets loaded
    for bkg in backgrounds :
        for sys in syst :
            if len(bkg.treefiles[sys]) != len(bkg.dsid_list) :
                for ds in bkg.dsid_list :
                    found_sample = False
                    for x in bkg.treefiles[sys] :
                        if ds in x : 
                            found_sample = True
                    if not found_sample :
                        print "############################## ERROR    Systematic (%s) tree not found for dataset %s (%s)"%(sys, str(ds), bkg.name)

    ## get the output file
    outfile = r.TFile(output_name, "RECREATE")
    outfile.Close()
    outfile.Delete()

    for bkg in backgrounds :
        for sys in syst :
            print " + ------------------------------- + "
            print "    Combining                        "
            print "       (Bkg, Sys) : (%s, %s)         "%(bkg.name, sys)
            print ""
            merge_chain = r.TChain(bkg.name + "_" + sys)
            #r.TTree.SetMaxtreeSize(137438953472LL)

            outfile = r.TFile(output_name, "UPDATE")
            outfile.cd()

            num_files = 0
            sum_entries = 0
            sample_list = bkg.treefiles[sys]
            treename = "superNt"
            for sample in sample_list :
                dsid = ""
                for ds in bkg.dsid_list :
                    if ds in sample : dsid = str(ds)
                in_file = r.TFile(sample)
                in_tree = in_file.Get(treename)

                if in_tree.GetEntries() > 0 :
                    print "%s %s (%s) : "%(bkg.name, dsid, sys), in_tree.GetEntries()
                    sum_entries += in_tree.GetEntries()
                    num_files += 1

                merge_chain.AddFile(sample, 0,  treename)

            print "sum entries : ", sum_entries
            print "    Sample summary"
            print "         total number of files merged : ", num_files
            print "         total number of entries      : ", sum_entries
            outfile.cd() 
            merge_chain.Merge(outfile, 0, "fast")

    ######################################################
    ## now merge the signal files
    for sig in signals :
        for sys in syst :
            sig.setSample(mc_sample_dir, sys)
    ## check that for each loaded systeamtic we have the same number
    ## of datasets loaded
    for sig in signals :
        for sys in syst :
            if len(sig.treefiles[sys]) != len(sig.dsid_list) :
                for ds in sig.dsid_list :
                    found_sample = False
                    for x in sig.treefiles[sys] :
                        if ds in x : 
                            found_sample = True
                    if not found_sample :
                        print "############################## ERROR    Systematic (%s) tree not found for dataset %s (%s)"%(sys, str(ds), sig.name)

    outfile_sig = r.TFile(output_name_sig, "RECREATE")
    outfile_sig.Close()
    outfile_sig.Delete()

    for sig in signals :
        for sys in syst :

            treename = "superNt"

            filename = "./LimitScripts/susyinfo/grid_" + grid + ".txt" 
            lines = open(filename).readlines()
            for line in lines :
                if not line : continue
                if line.startswith("#") : continue
                line = line.strip()
                line = line.split()
                for ds in sig.dsid_list :
                    if line[0] != ds : continue
                    print line
                    signame = grid + "_" + "%.1f"%float(line[1]) + "_" + "%.1f"%float(line[2])
                    chain_name = signame + "_" + sys

                    print " + ------------------------------- + "
                    print "    Combining                        "
                    print "       (Sig, Sys) : (%s, %s)         "%(signame, sys)
                    print ""

                    merge_chain = r.TChain(chain_name)
                    outfile = r.TFile(output_name_sig, "UPDATE")
                    outfile.cd()

                    sum_entries = 0
                    sample = ""
                    for sample_ in sig.treefiles[sys] :
                        if ds not in sample_ : continue
                        sample = sample_ 
                    in_file = r.TFile(sample)
                    in_tree = in_file.Get(treename)

                    if in_tree.GetEntries() > 0 :
                        print "%s %s (%s) : "%(signame, ds, sys), in_tree.GetEntries()

                    merge_chain.AddFile(sample, 0, treename)
                    outfile.cd()
                    merge_chain.Merge(outfile, 0, "fast")

                    

    
        
        


            


    
    
