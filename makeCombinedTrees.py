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
        global isCondor
        self.treefiles[systematic] = []
        if len(self.dsid_list) == 0 :
            if isCondor and self.name != "Fakes" :
                print "Looking for samples for process %s in %s"%(self.name, self.filelist)
                dsids = []
                txt_files = glob.glob(self.filelist + "*.txt")
                for tf in txt_files :
                    if "Data" not in self.name :
                        dsids.append(tf[tf.find('mc15_13TeV.')+11 : tf.find('mc15_13TeV.')+17])
                    else :
                        if "data15" in tf :
                            dsids.append(tf[tf.find('data15_13TeV.00')+15 : tf.find('data15_13TeV.')+21])
                        elif "data16" in tf :
                            dsids.append(tf[tf.find('data16_13TeV.00')+15 : tf.find('data16_13TeV.')+21])
                self.dsid_list = dsids
            elif isCondor and self.name == "Fakes" :
                print "Looking for samples for process %s in %s"%(self.name, self.filelist)
                fake_files = glob.glob(self.filelist + "*.root")
                if len(fake_files) == 0 :
                    print "WARNING No fake ntuples found in directory: %s"%self.filelist
                    sys.exit()
                self.dsid_list.append("3body_v02")
            else :
                print "Looking for samples for process %s in %s"%(self.name, self.filelist)
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
        print "Looking for files in %s"%sample_dir
        for dataset in self.dsid_list :
        #for dataset in dsids :
            for f in raw_files :
                if 'entrylist' in f : continue
                if dataset in f and systematic in f :
                    files.append(f)
                    break # move to next dsid

        self.treefiles[systematic] = files 
                     
###########################
## are you using CONDOR-style filelists?
isCondor = True
        

###########################
## available systematics
syst = []
syst.append('CENTRAL')

# egamma
syst.append('EG_RESOLUTION_ALL_UP')
syst.append('EG_RESOLUTION_ALL_DN')
syst.append('EG_SCALE_ALL_UP')
syst.append('EG_SCALE_ALL_DN')

# muons
syst.append('MUONS_ID_DN')
syst.append('MUONS_ID_UP')
syst.append('MUONS_MS_DN')
syst.append('MUONS_MS_UP')
syst.append('MUONS_SCALE_DN')
syst.append('MUONS_SCALE_UP')

# jet
syst.append('JER')
syst.append('JET_GroupedNP_1_DN')
syst.append('JET_GroupedNP_1_UP')

# met
#syst.append('MET_SoftTrk_ResoPara')
#syst.append('MET_SoftTrk_ResoPerp')
#syst.append('MET_SoftTrk_ScaleDown')
#syst.append('MET_SoftTrk_ScaleUp')

###########################
## backgrounds
backgrounds = []
filelist_dir      = "/data/uclhc/uci/user/dantrim/n0225val/filelists/"
#mc_sample_dir     = "/data/uclhc/uci/user/dantrim/ntuples/n0224/may25/mc/Raw/"
#mc_sample_dir     = "/data/uclhc/uci/user/dantrim/ntuples/n0224/hftrees/mc/Raw/"
#mc_sample_dir     = "/data/uclhc/uci/user/dantrim/ntuples/n0225/jul6/mc/Raw/"
#mc_sample_dir     = "/data/uclhc/uci/user/dantrim/ntuples/n0225/jun30/mc/sf_diboson/Raw/"
mc_sample_dir = "/data/uclhc/uci/user/dantrim/ntuples/n0225/jul6/mc/sf_diboson/Raw/"
#data_sample_dir   = "/data/uclhc/uci/user/dantrim/ntuples/n0224/may25/data/Raw/"
#data_sample_dir   = "/data/uclhc/uci/user/dantrim/ntuples/n0224/hftrees/data15/Raw/"
#data_sample_dir   = "/data/uclhc/uci/user/dantrim/ntuples/n0225/jun30/data15/Raw/"
data_sample_dir   = "/data/uclhc/uci/user/dantrim/ntuples/n0225/jul6/n0225_data/Raw/"
fake_sample_dir   = "/data/uclhc/uci/user/dantrim/ntuples/n0224/fakes_jun13/"

# data
#bkg_data    = Background("Data", filelist_dir + "n0225_data_2015DSW/")
##bkg_data    = Background("Data", filelist_dir + "n0225_data15/")
#backgrounds.append(bkg_data)
## ttbar
#bkg_ttbar   = Background("TTbar", filelist_dir + "ttbar/")
#backgrounds.append(bkg_ttbar)
# diboson
bkg_diboson = Background("VVSF", filelist_dir + "diboson_sherpa_lvlv/")
backgrounds.append(bkg_diboson)
#bkg_dy = Background("DrellYan", filelist_dir + "drellyan_sherpa/")
#backgrounds.append(bkg_dy)
## single top
#bkg_st      = Background("ST", filelist_dir + "singletop/")
#backgrounds.append(bkg_st)
## wjets
#bkg_wjets   = Background("Wjets", filelist_dir + "wjets_sherpa22/")
#backgrounds.append(bkg_wjets)
## zjets
#bkg_zjets   = Background("Zjets", filelist_dir + "zjets_sherpa22/")
#backgrounds.append(bkg_zjets)
## fakes
#bkg_fakes   = Background("Fakes", "/data/uclhc/uci/user/dantrim/ntuples/n0224/fakes_jun13/") 
#backgrounds.append(bkg_fakes)

############################
## signals

## will parse through ./LimitScripts/susyinfo/
signals = []
grid = "bWNnew"
sig_bWN = Background("BWN", filelist_dir + "bwn/")
signals.append(sig_bWN)

###################################
## setup the output file name and location
output_dir  = "./" 
output_name = "HFT_BG_13TeV_VVSF_Jul7.root"
output_name_sig = "HFT_bWN_13TeV.root"


if __name__=="__main__" :

    ## load the backgrounds and locate the files
    for bkg in backgrounds :
        for sys_ in syst :
            if "Data" in bkg.name and "CENTRAL" in sys_ : 
                bkg.setSample(data_sample_dir, sys_)
            elif "Data" in bkg.name and "CENTRAL" not in sys_ : continue
            elif "Fakes" in bkg.name and "CENTRAL" in sys_ :
                bkg.setSample(fake_sample_dir, sys_)
            elif "Fakes" in bkg.name and "CENTRAL" not in sys_ : continue
            else :
                bkg.setSample(mc_sample_dir, sys_)
                print "Loaded %d tree files for sample %s for systematic %s"%(len(bkg.treefiles), bkg.name, sys_)
           #     print bkg.treefiles

    ## check that for each loaded systeamtic we have the same number
    ## of datasets loaded
    for bkg in backgrounds :
        if "Data" in bkg.name : continue
        if "Fakes" in bkg.name : continue
        for sys_ in syst :
            if len(bkg.treefiles[sys_]) != len(bkg.dsid_list) :
                for ds in bkg.dsid_list :
                    found_sample = False
                    for x in bkg.treefiles[sys_] :
                        if ds in x : 
                            found_sample = True
                    if not found_sample :
                        print "############################## ERROR    Systematic (%s) tree not found for dataset %s (%s)"%(sys_, str(ds), bkg.name)

    ## get the output file
    outfile = r.TFile(output_name, "RECREATE")
    outfile.Close()
    outfile.Delete()

    for bkg in backgrounds :
        for sys_ in syst :
            if "Data" in bkg.name and "CENTRAL" not in sys_ : continue
            if "Fakes" in bkg.name and "CENTRAL" not in sys_ : continue
            print " + ------------------------------- + "
            print "    Combining                        "
            print "       (Bkg, Sys) : (%s, %s)         "%(bkg.name, sys_)
            print ""
            merge_chain = r.TChain(bkg.name + "_" + sys_)

            #r.TTree.SetMaxtreeSize(137438953472LL)

            outfile = r.TFile(output_name, "UPDATE")
            outfile.cd()

            num_files = 0
            sum_entries = 0
            sample_list = bkg.treefiles[sys_]
            treename = "superNt"
            for sample in sample_list :
                dsid = ""
                for ds in bkg.dsid_list :
                    if ds in sample : dsid = str(ds)
                in_file = r.TFile(sample)
                in_tree = in_file.Get(treename)

                if in_tree.GetEntries() > 0 :
                    print "%s %s (%s) : "%(bkg.name, dsid, sys_), in_tree.GetEntries()
                    sum_entries += in_tree.GetEntries()
                    num_files += 1

                merge_chain.AddFile(sample, 0,  treename)

            print "sum entries : ", sum_entries
            print "    Sample summary"
            print "         total number of files merged : ", num_files
            print "         total number of entries      : ", sum_entries
            outfile.cd() 
            merge_chain.Merge(outfile, 0, "fast")

#    ######################################################
#    ## now merge the signal files
#    for sig in signals :
#        for sys_ in syst :
#            sig.setSample(mc_sample_dir, sys_)
#    ## check that for each loaded systeamtic we have the same number
#    ## of datasets loaded
#    for sig in signals :
#        for sys_ in syst :
#            if len(sig.treefiles[sys_]) != len(sig.dsid_list) :
#                for ds in sig.dsid_list :
#                    found_sample = False
#                    for x in sig.treefiles[sys_] :
#                        if ds in x : 
#                            found_sample = True
#                    if not found_sample :
#                        print "############################## ERROR    Systematic (%s) tree not found for dataset %s (%s)"%(sys_, str(ds), sig.name)
#
#    outfile_sig = r.TFile(output_name_sig, "RECREATE")
#    outfile_sig.Close()
#    outfile_sig.Delete()
#
#    for sig in signals :
#        for sys_ in syst :
#
#            treename = "superNt"
#
#            filename = "./LimitScripts/susyinfo/grid_" + grid + ".txt" 
#            lines = open(filename).readlines()
#            for line in lines :
#                if not line : continue
#                if line.startswith("#") : continue
#                line = line.strip()
#                line = line.split()
#                for ds in sig.dsid_list :
#                    if line[0] != ds : continue
#                    print line
#                    signame = grid.replace("new","") + "_" + "%.1f"%float(line[1]) + "_" + "%.1f"%float(line[2])
#                    chain_name = signame + "_" + sys_
#
#                    print " + ------------------------------- + "
#                    print "    Combining                        "
#                    print "       (Sig, Sys) : (%s, %s)         "%(signame, sys_)
#                    print ""
#
#                    merge_chain = r.TChain(chain_name)
#                    outfile = r.TFile(output_name_sig, "UPDATE")
#                    outfile.cd()
#
#                    sum_entries = 0
#                    sample = ""
#                    for sample_ in sig.treefiles[sys_] :
#                        if ds not in sample_ : continue
#                        sample = sample_ 
#                    in_file = r.TFile(sample)
#                    in_tree = in_file.Get(treename)
#
#                    if in_tree.GetEntries() > 0 :
#                        print "%s %s (%s) : "%(signame, ds, sys_), in_tree.GetEntries()
#
#                    merge_chain.AddFile(sample, 0, treename)
#                    outfile.cd()
#                    merge_chain.Merge(outfile, 0, "fast")
