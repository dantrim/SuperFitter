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

        sigweight = "eventweightNOPUPW"

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
            self.mcstat_TTbar   = Systematic("mcstat_TTbar", "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.mcstat_VVSF      = Systematic("mcstat_VVSF",    "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.mcstat_VVDF      = Systematic("mcstat_VVDF",    "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.mcstat_WW      = Systematic("mcstat_WW",    "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.mcstat_ST      = Systematic("mcstat_ST",    "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.mcstat_Wjets   = Systematic("mcstat_Wjets", "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.mcstat_Zjets   = Systematic("mcstat_Zjets", "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.mcstat_WZ      = Systematic("mcstat_WZ",    "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.mcstat_ZZ      = Systematic("mcstat_ZZ",    "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.mcstat_SIG     = Systematic("mcstat_SIG",   "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.mcstat_DY      = Systematic("mcstat_DY",   "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.mcstat_TTV     = Systematic("mcstat_TTV", "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.mcstat_Higgs   = Systematic("mcstat_Higgs","_CENTRAL","_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.mcstat_FAKE    = Systematic("mcstat_FAKE", "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")


        self.AR_PILEUP_MC = Systematic("AR_PILEUP_MC", configMgr.weights, ("eventweightNOPUPW", "1.", "pupw_up"), ("eventweightNOPUPW", "1.", "pupw_down"), "weight", "overallSys")
        self.AR_PILEUP_CR = Systematic("AR_PILEUP_CR", configMgr.weights, ("eventweightNOPUPW", "1.", "pupw_up"), ("eventweightNOPUPW", "1.", "pupw_down"), "weight", "overallNormSys")



        #######################################################
        ## e-gamma
        #######################################################
        
        ## EG_RESOLUTION_ALL
        self.AR_EG_RESOLUTION_ALL_MC = Systematic("AR_EG_RESOLUTION_ALL_MC", "_CENTRAL", "_EG_RESOLUTION_ALL_DN", "_EG_RESOLUTION_ALL_UP", "tree", "overallSys")
        self.AR_EG_RESOLUTION_ALL_CR = Systematic("AR_EG_RESOLUTION_ALL_CR", "_CENTRAL", "_EG_RESOLUTION_ALL_DN", "_EG_RESOLUTION_ALL_UP", "tree", "overallNormSys")

        ######################
        ## EG_SCALE_ALL
        self.AR_EG_SCALE_ALL_MC = Systematic("AR_EG_SCALE_ALL_MC", "_CENTRAL", "_EG_SCALE_ALL_DN", "_EG_SCALE_ALL_UP", "tree", "overallSys")
        self.AR_EG_SCALE_ALL_CR = Systematic("AR_EG_SCALE_ALL_CR", "_CENTRAL", "_EG_SCALE_ALL_DN", "_EG_SCALE_ALL_UP", "tree", "overallNormSys")

        ######################
        ## EL_EFF_ID
        self.AR_EL_EFF_ID_MC = Systematic("AR_EL_EFF_ID_MC", configMgr.weights, ("eventweight","1.","syst_EL_EFF_IDUP"), ("eventweight","1.","syst_EL_EFF_IDDOWN"), "weight", "overallSys")
        self.AR_EL_EFF_ID_CR = Systematic("AR_EL_EFF_ID_CR", configMgr.weights, ("eventweight","1.","syst_EL_EFF_IDUP"), ("eventweight","1.","syst_EL_EFF_IDDOWN"), "weight", "overallNormSys")

        ## for signal (no pupw wiehgt) 
        self.AR_EL_EFF_ID_SIG_MC = Systematic("AR_EL_EFF_ID_MC", [sigweight], (sigweight,"1.","syst_EL_EFF_IDUP"), (sigweight,"1.","syst_EL_EFF_IDDOWN"), "weight", "overallSys")
        self.AR_EL_EFF_ID_SIG_CR = Systematic("AR_EL_EFF_ID_CR", [sigweight], (sigweight,"1.","syst_EL_EFF_IDUP"), (sigweight,"1.","syst_EL_EFF_IDDOWN"), "weight", "overallNormSys")

        ######################
        ## EL_EFF_Iso
        self.AR_EL_EFF_Iso_MC = Systematic("AR_EL_EFF_Iso_MC", configMgr.weights, ("eventweight","1.","syst_EL_EFF_IsoUP"), ("eventweight","1.","syst_EL_EFF_IsoDOWN"), "weight", "overallSys")
        self.AR_EL_EFF_Iso_CR = Systematic("AR_EL_EFF_Iso_CR", configMgr.weights, ("eventweight","1.","syst_EL_EFF_IsoUP"), ("eventweight","1.","syst_EL_EFF_IsoDOWN"), "weight", "overallNormSys")

        ## for signal (no pupw weight)
        self.AR_EL_EFF_Iso_SIG_MC = Systematic("AR_EL_EFF_Iso_MC", [sigweight], (sigweight,"1.","syst_EL_EFF_IsoUP"), (sigweight,"1.","syst_EL_EFF_IsoDOWN"), "weight", "overallSys")
        self.AR_EL_EFF_Iso_SIG_CR = Systematic("AR_EL_EFF_Iso_CR", [sigweight], (sigweight,"1.","syst_EL_EFF_IsoUP"), (sigweight,"1.","syst_EL_EFF_IsoDOWN"), "weight", "overallNormSys")

        #####################
        ## EL_EFF_Reco
        self.AR_EL_EFF_Reco_MC = Systematic("AR_EL_EFF_Reco_MC", configMgr.weights, ("eventweight","1.","syst_EL_EFF_RecoUP"), ("eventweight","1.","syst_EL_EFF_RecoDOWN"), "weight", "overallSys")
        self.AR_EL_EFF_Reco_CR = Systematic("AR_EL_EFF_Reco_CR", configMgr.weights, ("eventweight","1.","syst_EL_EFF_RecoUP"), ("eventweight","1.","syst_EL_EFF_RecoDOWN"), "weight", "overallNormSys")

        ## for signal (no pupw weight)
        self.AR_EL_EFF_Reco_SIG_MC = Systematic("AR_EL_EFF_Reco_MC", [sigweight], (sigweight,"1.","syst_EL_EFF_RecoUP"), (sigweight,"1.","syst_EL_EFF_RecoDOWN"), "weight", "overallSys")
        self.AR_EL_EFF_Reco_SIG_CR = Systematic("AR_EL_EFF_Reco_CR", [sigweight], (sigweight,"1.","syst_EL_EFF_RecoUP"), (sigweight,"1.","syst_EL_EFF_RecoDOWN"), "weight", "overallNormSys")


        #######################################################
        ## muons
        #######################################################

        ######################
        ## MUON_ID
        self.AR_MUON_ID_MC = Systematic("AR_MUON_ID_MC", "_CENTRAL", "_MUON_ID_DN", "_MUON_ID_UP", "tree", "overallSys")
        self.AR_MUON_ID_CR = Systematic("AR_MUON_ID_CR", "_CENTRAL", "_MUON_ID_DN", "_MUON_ID_UP", "tree", "overallNormSys")

        ######################
        ## MUON_MS
        self.AR_MUON_MS_MC = Systematic("AR_MUON_MS_MC", "_CENTRAL", "_MUON_MS_DN", "_MUON_MS_UP", "tree", "overallSys")
        self.AR_MUON_MS_CR = Systematic("AR_MUON_MS_CR", "_CENTRAL", "_MUON_MS_DN", "_MUON_MS_UP", "tree", "overallNormSys")

        #####################
        ## MUON_SCALE
        self.AR_MUON_SCALE_MC = Systematic("AR_MUON_SCALE_MC", "_CENTRAL", "_MUON_SCALE_DN", "_MUON_SCALE_UP", "tree", "overallSys")
        self.AR_MUON_SCALE_CR = Systematic("AR_MUON_SCALE_CR", "_CENTRAL", "_MUON_SCALE_DN", "_MUON_SCALE_UP", "tree", "overallNormSys")

        ######################
        ## MUON_EFF_STAT
        self.AR_MUON_EFF_STAT_MC = Systematic("AR_MUON_EFF_STAT_MC", configMgr.weights, ("eventweight","1.","syst_MUON_EFF_STATUP"), ("eventweight","1.","syst_MUON_EFF_STATDOWN"), "weight", "overallSys")
        self.AR_MUON_EFF_STAT_CR = Systematic("AR_MUON_EFF_STAT_CR", configMgr.weights, ("eventweight","1.","syst_MUON_EFF_STATUP"), ("eventweight","1.","syst_MUON_EFF_STATDOWN"), "weight", "overallNormSys")

        ## for signal (no pupw weight)
        self.AR_MUON_EFF_STAT_SIG_MC = Systematic("AR_MUON_EFF_STAT_MC", [sigweight], (sigweight,"1.","syst_MUON_EFF_STATUP"), (sigweight,"1.","syst_MUON_EFF_STATDOWN"), "weight", "overallSys")
        self.AR_MUON_EFF_STAT_SIG_CR = Systematic("AR_MUON_EFF_STAT_CR", [sigweight], (sigweight,"1.","syst_MUON_EFF_STATUP"), (sigweight,"1.","syst_MUON_EFF_STATDOWN"), "weight", "overallNormSys")

        #######################
        ## MUON_EFF_STAT_LOWPT
        self.AR_MUON_EFF_STAT_LOWPT_MC = Systematic("AR_MUON_EFF_STAT_LOWPT_MC", configMgr.weights, ("eventweight","1.","syst_MUON_EFF_STAT_LOWPTUP"), ("eventweight","1.","syst_MUON_EFF_STAT_LOWPTDOWN"), "weight", "overallSys")
        self.AR_MUON_EFF_STAT_LOWPT_CR = Systematic("AR_MUON_EFF_STAT_LOWPT_CR", configMgr.weights, ("eventweight","1.","syst_MUON_EFF_STAT_LOWPTUP"), ("eventweight","1.","syst_MUON_EFF_STAT_LOWPTDOWN"), "weight", "overallNormSys")

        ## for signal (no pupw weight)
        self.AR_MUON_EFF_STAT_LOWPT_SIG_MC = Systematic("AR_MUON_EFF_STAT_LOWPT_MC", [sigweight], (sigweight,"1.","syst_MUON_EFF_STAT_LOWPTUP"), (sigweight,"1.","syst_MUON_EFF_STAT_LOWPTDOWN"), "weight", "overallSys")
        self.AR_MUON_EFF_STAT_LOWPT_SIG_CR = Systematic("AR_MUON_EFF_STAT_LOWPT_CR", [sigweight], (sigweight,"1.","syst_MUON_EFF_STAT_LOWPTUP"), (sigweight,"1.","syst_MUON_EFF_STAT_LOWPTDOWN"), "weight", "overallNormSys")

        #########################
        ## MUON_EFF_SYS
        self.AR_MUON_EFF_SYS_MC = Systematic("AR_MUON_EFF_SYS_MC", configMgr.weights, ("eventweight","1.","syst_MUON_EFF_SYSUP"), ("eventweight","1.","syst_MUON_EFF_SYSDOWN"), "weight", "overallSys")
        self.AR_MUON_EFF_SYS_CR = Systematic("AR_MUON_EFF_SYS_CR", configMgr.weights, ("eventweight","1.","syst_MUON_EFF_SYSUP"), ("eventweight","1.","syst_MUON_EFF_SYSDOWN"), "weight", "overallNormSys")

        ## for signal (no pupw weight)
        self.AR_MUON_EFF_SYS_SIG_MC = Systematic("AR_MUON_EFF_SYS_MC", [sigweight], (sigweight,"1.","syst_MUON_EFF_SYSUP"), (sigweight,"1.","syst_MUON_EFF_SYSDOWN"), "weight", "overallSys")
        self.AR_MUON_EFF_SYS_SIG_CR = Systematic("AR_MUON_EFF_SYS_CR", [sigweight], (sigweight,"1.","syst_MUON_EFF_SYSUP"), (sigweight,"1.","syst_MUON_EFF_SYSDOWN"), "weight", "overallNormSys")

        #########################
        ## MUON_EFF_SYS_LOWPT
        self.AR_MUON_EFF_SYS_LOWPT_MC = Systematic("AR_MUON_EFF_SYS_LOWPT_MC", configMgr.weights, ("eventweight","1.","syst_MUON_EFF_SYS_LOWPTUP"), ("eventweight","1.","syst_MUON_EFF_SYS_LOWPTDOWN"), "weight", "overallSys")
        self.AR_MUON_EFF_SYS_LOWPT_CR = Systematic("AR_MUON_EFF_SYS_LOWPT_CR", configMgr.weights, ("eventweight","1.","syst_MUON_EFF_SYS_LOWPTUP"), ("eventweight","1.","syst_MUON_EFF_SYS_LOWPTDOWN"), "weight", "overallNormSys")

        ## for signal (no pupw weight)
        self.AR_MUON_EFF_SYS_LOWPT_SIG_MC = Systematic("AR_MUON_EFF_SYS_LOWPT_MC", [sigweight], (sigweight,"1.","syst_MUON_EFF_SYS_LOWPTUP"), (sigweight,"1.","syst_MUON_EFF_SYS_LOWPTDOWN"), "weight", "overallSys")
        self.AR_MUON_EFF_SYS_LOWPT_SIG_CR = Systematic("AR_MUON_EFF_SYS_LOWPT_CR", [sigweight], (sigweight,"1.","syst_MUON_EFF_SYS_LOWPTUP"), (sigweight,"1.","syst_MUON_EFF_SYS_LOWPTDOWN"), "weight", "overallNormSys")

        ##########################
        ## MUON_ISO_STAT
        self.AR_MUON_ISO_STAT_MC = Systematic("AR_MUON_ISO_STAT_MC", configMgr.weights, ("eventweight","1.","syst_MUON_ISO_STATUP"), ("eventweight","1.","syst_MUON_ISO_STATDOWN"), "weight", "overallSys")
        self.AR_MUON_ISO_STAT_CR = Systematic("AR_MUON_ISO_STAT_CR", configMgr.weights, ("eventweight","1.","syst_MUON_ISO_STATUP"), ("eventweight","1.","syst_MUON_ISO_STATDOWN"), "weight", "overallNormSys")

        ## for signal (no pupw weight)
        self.AR_MUON_ISO_STAT_SIG_MC = Systematic("AR_MUON_ISO_STAT_MC", [sigweight], (sigweight,"1.","syst_MUON_ISO_STATUP"), (sigweight,"1.","syst_MUON_ISO_STATDOWN"), "weight", "overallSys")
        self.AR_MUON_ISO_STAT_SIG_CR = Systematic("AR_MUON_ISO_STAT_CR", [sigweight], (sigweight,"1.","syst_MUON_ISO_STATUP"), (sigweight,"1.","syst_MUON_ISO_STATDOWN"), "weight", "overallNormSys")

        ##########################
        ## MUON_ISO_SYS
        self.AR_MUON_ISO_SYS_MC = Systematic("AR_MUON_ISO_SYS_MC", configMgr.weights, ("eventweight","1.","syst_MUON_ISO_SYSUP"), ("eventweight","1.","syst_MUON_ISO_SYSDOWN"), "weight", "overallSys")
        self.AR_MUON_ISO_SYS_CR = Systematic("AR_MUON_ISO_SYS_CR", configMgr.weights, ("eventweight","1.","syst_MUON_ISO_SYSUP"), ("eventweight","1.","syst_MUON_ISO_SYSDOWN"), "weight", "overallNormSys")

        ## for signal (no pupw weight)
        self.AR_MUON_ISO_SYS_SIG_MC = Systematic("AR_MUON_ISO_SYS_MC", [sigweight], (sigweight,"1.","syst_MUON_ISO_SYSUP"), (sigweight,"1.","syst_MUON_ISO_SYSDOWN"), "weight", "overallSys")
        self.AR_MUON_ISO_SYS_SIG_CR = Systematic("AR_MUON_ISO_SYS_CR", [sigweight], (sigweight,"1.","syst_MUON_ISO_SYSUP"), (sigweight,"1.","syst_MUON_ISO_SYSDOWN"), "weight", "overallNormSys")

        #######################################################
        ## jets
        #######################################################

        ## JER
        self.AR_JER_MC = Systematic("AR_JER_MC", "_CENTRAL", "_JER", "_CENTRAL", "tree", "histoSysOneSide")
        self.AR_JER_CR = Systematic("AR_JER_CR", "_CENTRAL", "_JER", "_CENTRAL", "tree", "normHistoSysOneSide")

        ## JES Paraemter set 1
        self.AR_JET_GroupedNP_1_MC = Systematic("AR_JET_GroupedNP_1_MC", "_CENTRAL", "_JET_GroupedNP_1_DN", "_JET_GroupedNP_1_UP", "tree", "overallSys")
        self.AR_JET_GroupedNP_1_CR = Systematic("AR_JET_GroupedNP_1_CR", "_CENTRAL", "_JET_GroupedNP_1_DN", "_JET_GroupedNP_1_UP", "tree", "overallNormSys")
        ## JES Paraemter set 2
        self.AR_JET_GroupedNP_2_MC = Systematic("AR_JET_GroupedNP_2_MC", "_CENTRAL", "_JET_GroupedNP_2_DN", "_JET_GroupedNP_2_UP", "tree", "overallSys")
        self.AR_JET_GroupedNP_2_CR = Systematic("AR_JET_GroupedNP_2_CR", "_CENTRAL", "_JET_GroupedNP_2_DN", "_JET_GroupedNP_2_UP", "tree", "overallNormSys")
        ## JES Paraemter set 3
        self.AR_JET_GroupedNP_3_MC = Systematic("AR_JET_GroupedNP_3_MC", "_CENTRAL", "_JET_GroupedNP_3_DN", "_JET_GroupedNP_3_UP", "tree", "overallSys")
        self.AR_JET_GroupedNP_3_CR = Systematic("AR_JET_GroupedNP_3_CR", "_CENTRAL", "_JET_GroupedNP_3_DN", "_JET_GroupedNP_3_UP", "tree", "overallNormSys")

        ###########################
        ## JET_JVTEff
        self.AR_JET_JVTEff_MC = Systematic("AR_JET_JVTEff_MC", configMgr.weights, ("eventweight","1.","syst_JET_JVTEffUP"), ("eventweight","1.","syst_JET_JVTEffDOWN"), "weight", "overallSys")
        self.AR_JET_JVTEff_CR = Systematic("AR_JET_JVTEff_CR", configMgr.weights, ("eventweight","1.","syst_JET_JVTEffUP"), ("eventweight","1.","syst_JET_JVTEffDOWN"), "weight", "overallNormSys")

        ## for signal (no pupw weight)
        self.AR_JET_JVTEff_SIG_MC = Systematic("AR_JET_JVTEff_MC", [sigweight], (sigweight,"1.","syst_JET_JVTEffUP"), (sigweight,"1.","syst_JET_JVTEffDOWN"), "weight", "overallSys")
        self.AR_JET_JVTEff_SIG_CR = Systematic("AR_JET_JVTEff_CR", [sigweight], (sigweight,"1.","syst_JET_JVTEffUP"), (sigweight,"1.","syst_JET_JVTEffDOWN"), "weight", "overallNormSys")


        #######################################################
        ## flavor tagging
        #######################################################

        #######################
        ## FT_EFF_B 
        self.AR_FT_EFF_B_MC = Systematic("AR_FT_EFF_B_MC", configMgr.weights, ("eventweight","1.","syst_FT_EFF_BUP"), ("eventweight","1.","syst_FT_EFF_BDOWN"), "weight", "overallSys")
        self.AR_FT_EFF_B_CR = Systematic("AR_FT_EFF_B_CR", configMgr.weights, ("eventweight","1.","syst_FT_EFF_BUP"), ("eventweight","1.","syst_FT_EFF_BDOWN"), "weight", "overallNormSys")

        ## for signal
        self.AR_FT_EFF_B_SIG_MC = Systematic("AR_FT_EFF_B_MC", [sigweight], (sigweight,"1.","syst_FT_EFF_BUP"), (sigweight,"1.","syst_FT_EFF_BDOWN"), "weight", "overallSys")
        self.AR_FT_EFF_B_SIG_CR = Systematic("AR_FT_EFF_B_CR", [sigweight], (sigweight,"1.","syst_FT_EFF_BUP"), (sigweight,"1.","syst_FT_EFF_BDOWN"), "weight", "overallNormSys")

        ######################
        ## FT_EFF_C
        self.AR_FT_EFF_C_MC = Systematic("AR_FT_EFF_C_MC", configMgr.weights, ("eventweight","1.","syst_FT_EFF_CUP"), ("eventweight","1.","syst_FT_EFF_CDOWN"), "weight", "overallSys")
        self.AR_FT_EFF_C_CR = Systematic("AR_FT_EFF_C_CR", configMgr.weights, ("eventweight","1.","syst_FT_EFF_CUP"), ("eventweight","1.","syst_FT_EFF_CDOWN"), "weight", "overallNormSys")

        ## for signal
        self.AR_FT_EFF_C_SIG_MC = Systematic("AR_FT_EFF_C_MC", [sigweight], (sigweight,"1.","syst_FT_EFF_CUP"), (sigweight,"1.","syst_FT_EFF_CDOWN"), "weight", "overallSys")
        self.AR_FT_EFF_C_SIG_CR = Systematic("AR_FT_EFF_C_CR", [sigweight], (sigweight,"1.","syst_FT_EFF_CUP"), (sigweight,"1.","syst_FT_EFF_CDOWN"), "weight", "overallNormSys")

        ######################
        ## FT_EFF_Light
        self.AR_FT_EFF_Light_MC = Systematic("AR_FT_EFF_Light_MC", configMgr.weights, ("eventweight","1.","syst_FT_EFF_LightUP"), ("eventweight","1.","syst_FT_EFF_LightDOWN"), "weight", "overallSys")
        self.AR_FT_EFF_Light_CR = Systematic("AR_FT_EFF_Light_CR", configMgr.weights, ("eventweight","1.","syst_FT_EFF_LightUP"), ("eventweight","1.","syst_FT_EFF_LightDOWN"), "weight", "overallNormSys")

        ## for signal
        self.AR_FT_EFF_Light_SIG_MC = Systematic("AR_FT_EFF_Light_MC", [sigweight], (sigweight,"1.","syst_FT_EFF_LightUP"), (sigweight,"1.","syst_FT_EFF_LightDOWN"), "weight", "overallSys")
        self.AR_FT_EFF_Light_SIG_CR = Systematic("AR_FT_EFF_Light_CR", [sigweight], (sigweight,"1.","syst_FT_EFF_LightUP"), (sigweight,"1.","syst_FT_EFF_LightDOWN"), "weight", "overallNormSys")

        ######################
        ## FT_EFF_extrapolation
        self.AR_FT_EFF_extrapolation_MC = Systematic("AR_FT_EFF_extrapolation_MC", configMgr.weights, ("eventweight","1.","syst_FT_EFF_extrapolationUP"), ("eventweight","1.","syst_FT_EFF_extrapolationDOWN"), "weight", "overallSys")
        self.AR_FT_EFF_extrapolation_CR = Systematic("AR_FT_EFF_extrapolation_CR", configMgr.weights, ("eventweight","1.","syst_FT_EFF_extrapolationUP"), ("eventweight","1.","syst_FT_EFF_extrapolationDOWN"), "weight", "overallNormSys")

        ## for signal
        self.AR_FT_EFF_extrapolation_SIG_MC = Systematic("AR_FT_EFF_extrapolation_MC", [sigweight], (sigweight,"1.","syst_FT_EFF_extrapolationUP"), (sigweight,"1.","syst_FT_EFF_extrapolationDOWN"), "weight", "overallSys")
        self.AR_FT_EFF_extrapolation_SIG_CR = Systematic("AR_FT_EFF_extrapolation_CR", [sigweight], (sigweight,"1.","syst_FT_EFF_extrapolationUP"), (sigweight,"1.","syst_FT_EFF_extrapolationDOWN"), "weight", "overallNormSys")

        #######################
        ## FT_EFF_extrapolation_chram
        self.AR_FT_EFF_extrapolation_charm_MC = Systematic("AR_FT_EFF_extrapolation_charm_MC", configMgr.weights, ("eventweight","1.","syst_FT_EFF_extrapolation_charmUP"), ("eventweight","1.","syst_FT_EFF_extrapolation_charmDOWN"), "weight", "overallSys")
        self.AR_FT_EFF_extrapolation_charm_CR = Systematic("AR_FT_EFF_extrapolation_charm_CR", configMgr.weights, ("eventweight","1.","syst_FT_EFF_extrapolation_charmUP"), ("eventweight","1.","syst_FT_EFF_extrapolation_charmDOWN"), "weight", "overallNormSys")

        ## for signal
        self.AR_FT_EFF_extrapolation_charm_SIG_MC = Systematic("AR_FT_EFF_extrapolation_charm_MC", [sigweight], (sigweight,"1.","syst_FT_EFF_extrapolation_charmUP"), (sigweight,"1.","syst_FT_EFF_extrapolation_charmDOWN"), "weight", "overallSys")
        self.AR_FT_EFF_extrapolation_charm_SIG_CR = Systematic("AR_FT_EFF_extrapolation_charm_CR", [sigweight], (sigweight,"1.","syst_FT_EFF_extrapolation_charmUP"), (sigweight,"1.","syst_FT_EFF_extrapolation_charmDOWN"), "weight", "overallNormSys")


        #######################################################
        ## met
        #######################################################

        ## SoftTrk_ResoPara
        self.AR_MET_SoftTrk_ResoPara_MC = Systematic("AR_MET_SoftTrk_ResoPara_MC", "_CENTRAL", "_MET_SoftTrk_ResoPara", "_CENTRAL", "tree", "histoSysOneSide")
        self.AR_MET_SoftTrk_ResoPara_CR = Systematic("AR_MET_SoftTrk_ResoPara_CR", "_CENTRAL", "_MET_SoftTrk_ResoPara", "_CENTRAL", "tree", "normHistoSysOneSide")

        ## SoftTrk_ResoPerp
        self.AR_MET_SoftTrk_ResoPerp_MC = Systematic("AR_MET_SoftTrk_ResoPerp_MC", "_CENTRAL", "_MET_SoftTrk_ResoPerp", "_CENTRAL", "tree", "histoSysOneSide")
        self.AR_MET_SoftTrk_ResoPerp_CR = Systematic("AR_MET_SoftTrk_ResoPerp_CR", "_CENTRAL", "_MET_SoftTrk_ResoPerp", "_CENTRAL", "tree", "normHistoSysOneSide")

        ## SoftTrk_Scale
        self.AR_MET_SoftTrk_Scale_MC = Systematic("AR_MET_SoftTrk_Scale_MC", "_CENTRAL", "_MET_SoftTrk_ScaleDown", "_MET_SoftTrk_ScaleUp", "tree", "overallSys")
        self.AR_MET_SoftTrk_Scale_CR = Systematic("AR_MET_SoftTrk_Scale_CR", "_CENTRAL", "_MET_SoftTrk_ScaleDown", "_MET_SoftTrk_ScaleUp", "tree", "overallNormSys")

        #######################################################
        # theory 
        #######################################################
        def getRelUncert(process, region) :
            if process=="TTbar" :
                return 0.5
            elif process=="VVDF" :
                return 0.3
            elif process=="VVSF" :
                return 0.2
            else :
                print "Requesting theory systematic for unhandled process (%s)"%process
                return 0.

        def getTheorySys(sysName, process, region) :
            return Systematic(sysName, configMgr.weights, 1.0+getRelUncert(process, region), 1.0-getRelUncert(process, region), "user", "userOverallSys")

        self.SRwt_TTbar_THEORY        = getTheorySys("SRwt_TTbar_THEORY", "TTbar", "SRwt")
        self.SRwt_VVDF_THEORY         = getTheorySys("SRwt_VVDF_THEORY", "VVDF", "SRwt")
        self.SRwt_VVSF_THEORY         = getTheorySys("SRwt_VVSF_THEORY", "VVSF", "SRwt")


        #######################################################
        # Fake
        #######################################################
        def getFakeRelUncert(up_or_down, region) :
            uncertainties = {}
            uncertainties["SRw_EE"] = { "up" : 520,  "down" : 520  } 
            uncertainties["SRw_MM"] = { "up" : 0.95, "down" : 0.95 }
            uncertainties["SRw_SF"] = { "up" : 1.14, "down" : 1.14 }
            uncertainties["SRw_DF"] = { "up" : 1.36, "down" : 1.36 }

            # SRt_EE and SRt_MM are negative in all variations
            uncertainties["SRt_DF"] = { "up" : 0.92, "down" : 0.92 }

            uncertainties["CRTop"]  = { "up" : 9250, "down" : 9250 }
            uncertainties["VRTop"]  = { "up" : 0.52, "down" : 0.52 }

            # CRVVDF negative in all variations
            uncertainties["CRVVSF"] = { "up" : 0.88, "down" : 0.88 } 

            uncertainties["VRVVDF"] = { "up" : 0.20, "down" : 0.20 }
            uncertainties["VRVVSF"] = { "up" : 0.23, "down" : 0.23 }

            return uncertainties[region][up_or_down]

        def getFakeSys(name_of_sys, region) :
            return Systematic(name_of_sys, ["FakeWeight"], 1.0 + getFakeRelUncert("up", region), 1.0 - getFakeRelUncert("down", region), "user", "userOverallSys")


        self.SRw_DF_FakeRelUnc      = getFakeSys("FakeRelUnc", "SRw_DF")
        self.SRw_EE_FakeRelUnc      = getFakeSys("FakeRelUnc", "SRw_EE")
        self.SRw_MM_FakeRelUnc      = getFakeSys("FakeRelUnc", "SRw_MM")
        self.SRw_SF_FakeRelUnc      = getFakeSys("FakeRelUnc", "SRw_SF")

        self.SRt_DF_FakeRelUnc      = getFakeSys("FakeRelUnc", "SRt_DF")

        self.CRVVSF_FakeRelUnc      = getFakeSys("FakeRelUnc", "CRVVSF")

        self.VRVVDF_FakeRelUnc      = getFakeSys("FakeRelUnc", "VRVVDF")
        self.VRVVSF_FakeRelUnc      = getFakeSys("FakeRelUnc", "VRVVSF")

        self.CRTop_FakeRelUnc       = getFakeSys("FakeRelUnc", "CRTop")
        self.VRTop_FakeRelUnc       = getFakeSys("FakeRelUnc", "VRTop")





