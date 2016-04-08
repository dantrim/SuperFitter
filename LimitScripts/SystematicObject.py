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
            self.mcstat_TTbar   = Systematic("mcstat_TTbar", "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.mcstat_VV      = Systematic("mcstat_VV",    "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.mcstat_WW      = Systematic("mcstat_WW",    "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.mcstat_ST      = Systematic("mcstat_ST",    "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.mcstat_Wjets   = Systematic("mcstat_Wjets", "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.mcstat_Zjets   = Systematic("mcstat_Zjets", "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.mcstat_WZ      = Systematic("mcstat_WZ",    "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.mcstat_ZZ      = Systematic("mcstat_ZZ",    "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.mcstat_SIG     = Systematic("mcstat_SIG",   "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")


        #######################################################
        ## e-gamma
        #######################################################
        
        ## EG_RESOLUTION_ALL
        self.AR_EG_RESOLUTION_ALL_MC = Systematic("AR_EG_RESOLUTION_ALL_MC", "_CENTRAL", "_EG_RESOLUTION_ALL_DN", "_EG_RESOLUTION_ALL_UP", "tree", "overallSys")
        self.AR_EG_RESOLUTION_ALL_CR = Systematic("AR_EG_RESOLUTION_ALL_CR", "_CENTRAL", "_EG_RESOLUTION_ALL_DN", "_EG_RESOLUTION_ALL_UP", "tree", "overallNormSys")

        ## EG_SCALE_ALL
        self.AR_EG_SCALE_ALL_MC = Systematic("AR_EG_SCALE_ALL_MC", "_CENTRAL", "_EG_SCALE_ALL_DN", "_EG_SCALE_ALL_UP", "tree", "overallSys")
        self.AR_EG_SCALE_ALL_CR = Systematic("AR_EG_SCALE_ALL_CR", "_CENTRAL", "_EG_SCALE_ALL_DN", "_EG_SCALE_ALL_UP", "tree", "overallNormSys")

        ## EL_EFF_ID
        self.AR_EL_EFF_ID_MC = Systematic("AR_EL_EFF_ID_MC", configMgr.weights, ("eventweight","1.","syst_EL_EFF_IDUP"), ("eventweight","1.","syst_EL_EFF_IDDOWN"), "weight", "overallSys")
        self.AR_EL_EFF_ID_CR = Systematic("AR_EL_EFF_ID_CR", configMgr.weights, ("eventweight","1.","syst_EL_EFF_IDUP"), ("eventweight","1.","syst_EL_EFF_IDDOWN"), "weight", "overallNormSys")

        ## EL_EFF_Iso
        self.AR_EL_EFF_Iso_MC = Systematic("AR_EL_EFF_Iso_MC", configMgr.weights, ("eventweight","1.","syst_EL_EFF_IsoUP"), ("eventweight","1.","syst_EL_EFF_IsoDOWN"), "weight", "overallSys")
        self.AR_EL_EFF_Iso_CR = Systematic("AR_EL_EFF_Iso_CR", configMgr.weights, ("eventweight","1.","syst_EL_EFF_IsoUP"), ("eventweight","1.","syst_EL_EFF_IsoDOWN"), "weight", "overallNormSys")

        ## EL_EFF_Reco
        self.AR_EL_EFF_Reco_MC = Systematic("AR_EL_EFF_Reco_MC", configMgr.weights, ("eventweight","1.","syst_EL_EFF_RecoUP"), ("eventweight","1.","syst_EL_EFF_RecoDOWN"), "weight", "overallSys")
        self.AR_EL_EFF_Reco_CR = Systematic("AR_EL_EFF_Reco_CR", configMgr.weights, ("eventweight","1.","syst_EL_EFF_RecoUP"), ("eventweight","1.","syst_EL_EFF_RecoDOWN"), "weight", "overallNormSys")


        #######################################################
        ## muons
        #######################################################

        ## MUONS_ID
        self.AR_MUONS_ID_MC = Systematic("AR_MUONS_ID_MC", "_CENTRAL", "_MUONS_ID_DN", "_MUONS_ID_UP", "tree", "overallSys")
        self.AR_MUONS_ID_CR = Systematic("AR_MUONS_ID_CR", "_CENTRAL", "_MUONS_ID_DN", "_MUONS_ID_UP", "tree", "overallNormSys")

        ## MUONS_MS
        self.AR_MUONS_MS_MC = Systematic("AR_MUONS_MS_MC", "_CENTRAL", "_MUONS_MS_DN", "_MUONS_MS_UP", "tree", "overallSys")
        self.AR_MUONS_MS_CR = Systematic("AR_MUONS_MS_CR", "_CENTRAL", "_MUONS_MS_DN", "_MUONS_MS_UP", "tree", "overallNormSys")

        ## MUONS_SCALE
        self.AR_MUONS_SCALE_MC = Systematic("AR_MUONS_SCALE_MC", "_CENTRAL", "_MUONS_SCALE_DN", "_MUONS_SCALE_UP", "tree", "overallSys")
        self.AR_MUONS_SCALE_CR = Systematic("AR_MUONS_SCALE_CR", "_CENTRAL", "_MUONS_SCALE_DN", "_MUONS_SCALE_UP", "tree", "overallNormSys")


        ## MUON_EFF_STAT
        self.AR_MUON_EFF_STAT_MC = Systematic("AR_MUON_EFF_STAT_MC", configMgr.weights, ("eventweight","1.","syst_MUON_EFF_STATUP"), ("eventweight","1.","syst_MUON_EFF_STATDOWN"), "weight", "overallSys")
        self.AR_MUON_EFF_STAT_CR = Systematic("AR_MUON_EFF_STAT_CR", configMgr.weights, ("eventweight","1.","syst_MUON_EFF_STATUP"), ("eventweight","1.","syst_MUON_EFF_STATDOWN"), "weight", "overallNormSys")

        ## MUON_EFF_STAT_LOWPT
        self.AR_MUON_EFF_STAT_LOWPT_MC = Systematic("AR_MUON_EFF_STAT_LOWPT_MC", configMgr.weights, ("eventweight","1.","syst_MUON_EFF_STAT_LOWPTUP"), ("eventweight","1.","syst_MUON_EFF_STAT_LOWPTDOWN"), "weight", "overallSys")
        self.AR_MUON_EFF_STAT_LOWPT_CR = Systematic("AR_MUON_EFF_STAT_LOWPT_CR", configMgr.weights, ("eventweight","1.","syst_MUON_EFF_STAT_LOWPTUP"), ("eventweight","1.","syst_MUON_EFF_STAT_LOWPTDOWN"), "weight", "overallNormSys")

        ## MUON_EFF_SYS
        self.AR_MUON_EFF_SYS_MC = Systematic("AR_MUON_EFF_SYS_MC", configMgr.weights, ("eventweight","1.","syst_MUON_EFF_SYSUP"), ("eventweight","1.","syst_MUON_EFF_SYSDOWN"), "weight", "overallSys")
        self.AR_MUON_EFF_SYS_CR = Systematic("AR_MUON_EFF_SYS_CR", configMgr.weights, ("eventweight","1.","syst_MUON_EFF_SYSUP"), ("eventweight","1.","syst_MUON_EFF_SYSDOWN"), "weight", "overallNormSys")

        ## MUON_EFF_SYS_LOWPT
        self.AR_MUON_EFF_SYS_LOWPT_MC = Systematic("AR_MUON_EFF_SYS_LOWPT_MC", configMgr.weights, ("eventweight","1.","syst_MUON_EFF_SYS_LOWPTUP"), ("eventweight","1.","syst_MUON_EFF_SYS_LOWPTDOWN"), "weight", "overallSys")
        self.AR_MUON_EFF_SYS_LOWPT_CR = Systematic("AR_MUON_EFF_SYS_LOWPT_CR", configMgr.weights, ("eventweight","1.","syst_MUON_EFF_SYS_LOWPTUP"), ("eventweight","1.","syst_MUON_EFF_SYS_LOWPTDOWN"), "weight", "overallNormSys")

        ## MUON_ISO_STAT
        self.AR_MUON_ISO_STAT_MC = Systematic("AR_MUON_ISO_STAT_MC", configMgr.weights, ("eventweight","1.","syst_MUON_ISO_STATUP"), ("eventweight","1.","syst_MUON_ISO_STATDOWN"), "weight", "overallSys")
        self.AR_MUON_ISO_STAT_CR = Systematic("AR_MUON_ISO_STAT_CR", configMgr.weights, ("eventweight","1.","syst_MUON_ISO_STATUP"), ("eventweight","1.","syst_MUON_ISO_STATDOWN"), "weight", "overallNormSys")

        ## MUON_ISO_SYS
        self.AR_MUON_ISO_SYS_MC = Systematic("AR_MUON_ISO_SYS_MC", configMgr.weights, ("eventweight","1.","syst_MUON_ISO_SYSUP"), ("eventweight","1.","syst_MUON_ISO_SYSDOWN"), "weight", "overallSys")
        self.AR_MUON_ISO_SYS_CR = Systematic("AR_MUON_ISO_SYS_CR", configMgr.weights, ("eventweight","1.","syst_MUON_ISO_SYSUP"), ("eventweight","1.","syst_MUON_ISO_SYSDOWN"), "weight", "overallNormSys")

        #######################################################
        ## jets
        #######################################################

        ## JER
        self.AR_JER_MC = Systematic("AR_JER_MC", "_CENTRAL", "_JER", "_CENTRAL", "tree", "histoSysOneSide")
        self.AR_JER_CR = Systematic("AR_JER_CR", "_CENTRAL", "_JER", "_CENTRAL", "tree", "normHistoSysOneSide")

        ## JES Paraemter set 1
        self.AR_JET_GroupedNP_1_MC = Systematic("AR_JET_GroupedNP_1_MC", "_CENTRAL", "_JET_GroupedNP_1_DN", "_JET_GroupedNP_1_UP", "tree", "overallSys")
        self.AR_JET_GroupedNP_1_CR = Systematic("AR_JET_GroupedNP_1_CR", "_CENTRAL", "_JET_GroupedNP_1_DN", "_JET_GroupedNP_1_UP", "tree", "overallNormSys")

        ## JET_JVTEff
        self.AR_JET_JVTEff_MC = Systematic("AR_JET_JVTEff_MC", configMgr.weights, ("eventweight","1.","syst_JET_JVTEffUP"), ("eventweight","1.","syst_JET_JVTEffDOWN"), "weight", "overallSys")
        self.AR_JET_JVTEff_CR = Systematic("AR_JET_JVTEff_CR", configMgr.weights, ("eventweight","1.","syst_JET_JVTEffUP"), ("eventweight","1.","syst_JET_JVTEffDOWN"), "weight", "overallNormSys")


        #######################################################
        ## flavor tagging
        #######################################################

        ## FT_EFF_B 
        self.AR_FT_EFF_B_MC = Systematic("AR_FT_EFF_B_MC", configMgr.weights, ("eventweight","1.","syst_FT_EFF_BUP"), ("eventweight","1.","syst_FT_EFF_BDOWN"), "weight", "overallSys")
        self.AR_FT_EFF_B_CR = Systematic("AR_FT_EFF_B_CR", configMgr.weights, ("eventweight","1.","syst_FT_EFF_BUP"), ("eventweight","1.","syst_FT_EFF_BDOWN"), "weight", "overallNormSys")

        ## FT_EFF_C
        self.AR_FT_EFF_C_MC = Systematic("AR_FT_EFF_C_MC", configMgr.weights, ("eventweight","1.","syst_FT_EFF_CUP"), ("eventweight","1.","syst_FT_EFF_CDOWN"), "weight", "overallSys")
        self.AR_FT_EFF_C_CR = Systematic("AR_FT_EFF_C_CR", configMgr.weights, ("eventweight","1.","syst_FT_EFF_CUP"), ("eventweight","1.","syst_FT_EFF_CDOWN"), "weight", "overallNormSys")

        ## FT_EFF_Light
        self.AR_FT_EFF_Light_MC = Systematic("AR_FT_EFF_Light_MC", configMgr.weights, ("eventweight","1.","syst_FT_EFF_LightUP"), ("eventweight","1.","syst_FT_EFF_LightDOWN"), "weight", "overallSys")
        self.AR_FT_EFF_Light_CR = Systematic("AR_FT_EFF_Light_CR", configMgr.weights, ("eventweight","1.","syst_FT_EFF_LightUP"), ("eventweight","1.","syst_FT_EFF_LightDOWN"), "weight", "overallNormSys")

        ## FT_EFF_extrapolation
        self.AR_FT_EFF_extrapolation_MC = Systematic("AR_FT_EFF_extrapolation_MC", configMgr.weights, ("eventweight","1.","syst_FT_EFF_extrapolationUP"), ("eventweight","1.","syst_FT_EFF_extrapolationDOWN"), "weight", "overallSys")
        self.AR_FT_EFF_extrapolation_CR = Systematic("AR_FT_EFF_extrapolation_CR", configMgr.weights, ("eventweight","1.","syst_FT_EFF_extrapolationUP"), ("eventweight","1.","syst_FT_EFF_extrapolationDOWN"), "weight", "overallNormSys")

        ## FT_EFF_extrapolation_chram
        self.AR_FT_EFF_extrapolation_charm_MC = Systematic("AR_FT_EFF_extrapolation_charm_MC", configMgr.weights, ("eventweight","1.","syst_FT_EFF_extrapolation_charmUP"), ("eventweight","1.","syst_FT_EFF_extrapolation_charmDOWN"), "weight", "overallSys")
        self.AR_FT_EFF_extrapolation_charm_CR = Systematic("AR_FT_EFF_extrapolation_charm_CR", configMgr.weights, ("eventweight","1.","syst_FT_EFF_extrapolation_charmUP"), ("eventweight","1.","syst_FT_EFF_extrapolation_charmDOWN"), "weight", "overallNormSys")


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


