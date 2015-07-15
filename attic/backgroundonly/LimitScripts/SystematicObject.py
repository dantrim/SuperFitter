
####################################################
# This will be a configurable class where the user #
# can pass the config Manager needed by HistFitter #
# and an option for doing or not doing shape fit.  #
# All of the systematics will then be configured   #
# accordingly so the user can then use them        #
####################################################

from systematic import Systematic
from TheoryUncertainties import *

class SystematicObject:

    def __init__(self, configMgr, doShapeFit, splitMCsystsIntoSamples):


        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
        #                            JETS                            #
        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

        if not doShapeFit:
            self.AR_all_JES_MC = Systematic("AR_all_JES_MC","_CENTRAL","_JESDOWN","_JESUP","tree","overallSys")
            self.AR_all_JES_CR = Systematic("AR_all_JES_CR","_CENTRAL","_JESDOWN","_JESUP","tree","overallNormSys")
            self.AR_all_JER_MC = Systematic("AR_all_JER_MC","_CENTRAL",  "_JER","_CENTRAL","tree","histoSysOneSide") 
            self.AR_all_JER_CR = Systematic("AR_all_JER_CR","_CENTRAL","_JER","_CENTRAL","tree","histoSysOneSide") 
            self.AR_all_JVF_MC = Systematic("AR_all_JVF_MC","_CENTRAL","_JVFUP","_CENTRAL","tree","overallSys")
            self.AR_all_JVF_CR = Systematic("AR_all_JVF_CR","_CENTRAL","_JVFUP","_CENTRAL","tree","overallNormSys")
            self.AR_all_TES_MC = Systematic("AR_all_TES_MC","_CENTRAL","_TESDOWN","_TESUP","tree","overallSys")
            self.AR_all_TES_CR= Systematic("AR_all_TES_CR","_CENTRAL","_TESDOWN","_TESUP","tree","overallNormSys")
        if doShapeFit:
            self.AR_all_JES_MC= Systematic("AR_all_JES_MC","_CENTRAL","_JESDOWN","_JESUP","tree","histoSys")
            self.AR_all_JES_CR= Systematic("AR_all_JES_CR","_CENTRAL","_JESDOWN","_JESUP","tree","normHistoSys")
            self.AR_all_JER_MC= Systematic("AR_all_JER_MC","_CENTRAL","_JER","_CENTRAL","tree","histoSys")
            self.AR_all_JER_CR= Systematic("AR_all_JER_CR","_CENTRAL","_JER","_CENTRAL","tree","normHistoSys")
            self.AR_all_JVF_MC= Systematic("AR_all_JVF_MC","_CENTRAL","_JVFUP","_CENTRAL","tree","histoSys")
            self.AR_all_JVF_CR= Systematic("AR_all_JVF_CR","_CENTRAL","_JVFUP","_CENTRAL","tree","normHistoSys")
            self.AR_all_TES_MC= Systematic("AR_all_TES_MC","_CENTRAL","_TESDOWN","_TESUP","tree","histoSys")
            self.AR_all_TES_CR= Systematic("AR_all_TES_CR","_CENTRAL","_TESDOWN","_TESUP","tree","normHistoSys")

        
        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
        #                        b-TAGGING                           #
        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

        
        if not doShapeFit:
            self.AR_all_BJET_MC         = Systematic("AR_all_BJET_MC",    configMgr.weights,  ("eventweight","1.","syst_BJETUP"), 	("eventweight","1.","syst_BJETDOWN"), "weight","overallSys")
            self.AR_all_BJET_CR         = Systematic("AR_all_BJET_CR",    configMgr.weights,  ("eventweight","1.","syst_BJETUP"), 	("eventweight","1.","syst_BJETDOWN"),	"weight","overallNormSys")
            self.AR_all_CJET_MC         = Systematic("AR_all_CJET_MC",    configMgr.weights,  ("eventweight","1.","syst_CJETUP"), 	("eventweight","1.","syst_CJETDOWN"), "weight","overallSys")
            self.AR_all_CJET_CR         = Systematic("AR_all_CJET_CR",    configMgr.weights,  ("eventweight","1.","syst_CJETUP"), 	("eventweight","1.","syst_CJETDOWN"), "weight","overallNormSys")
            self.AR_all_BMISTAG_MC      = Systematic("AR_all_BMISTAG_MC", configMgr.weights,  ("eventweight","1.","syst_BMISTAGUP"), 	("eventweight","1.","syst_BMISTAGDOWN"), "weight","overallSys")
            self.AR_all_BMISTAG_CR      = Systematic("AR_all_BMISTAG_CR", configMgr.weights,  ("eventweight","1.","syst_BMISTAGUP"), 	("eventweight","1.","syst_BMISTAGDOWN"), "weight","overallNormSys")
            #
        if doShapeFit:
            self.AR_all_BJET_MC         = Systematic("AR_all_BJET_MC",    configMgr.weights,  ("eventweight","1.","syst_BJETUP"),      ("eventweight","1.","syst_BJETDOWN"), "weight","histoSys")
            self.AR_all_BJET_CR         = Systematic("AR_all_BJET_CR",    configMgr.weights,  ("eventweight","1.","syst_BJETUP"),      ("eventweight","1.","syst_BJETDOWN"), "weight","normHistoSys")
            self.AR_all_CJET_MC         = Systematic("AR_all_CJET_MC",    configMgr.weights,  ("eventweight","1.","syst_CJETUP"),      ("eventweight","1.","syst_CJETDOWN"), "weight","histoSys")
            self.AR_all_CJET_CR         = Systematic("AR_all_CJET_CR",    configMgr.weights,  ("eventweight","1.","syst_CJETUP"),      ("eventweight","1.","syst_CJETDOWN"), "weight","normHistoSys")
            self.AR_all_BMISTAG_MC      = Systematic("AR_all_BMISTAG_MC", configMgr.weights,  ("eventweight","1.","syst_BMISTAGUP"),   ("eventweight","1.","syst_BMISTAGDOWN"), "weight","histoSys")
            self.AR_all_BMISTAG_CR      = Systematic("AR_all_BMISTAG_CR", configMgr.weights,  ("eventweight","1.","syst_BMISTAGUP"),   ("eventweight","1.","syst_BMISTAGDOWN"), "weight","normHistoSys")


        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
        #                        ELECTRONS                           #
        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

        if not doShapeFit:
            self.AR_all_EER_MC        = Systematic("AR_all_EER_MC",      "_CENTRAL",  "_EERUP",        "_EERDOWN",			   "tree","overallSys")
            self.AR_all_EER_CR        = Systematic("AR_all_EER_CR",      "_CENTRAL",  "_EERUP", 	      "_EERDOWN",			   "tree","overallNormSys") 
            self.AR_all_EESLOW_MC     = Systematic("AR_all_EESLOW_MC",   "_CENTRAL",  "_EESLOWUP",     "_EESLOWDOWN",			   "tree","overallSys")
            self.AR_all_EESLOW_CR     = Systematic("AR_all_EESLOW_CR",   "_CENTRAL",  "_EESLOWUP",     "_EESLOWDOWN",			   "tree","overallNormSys")
            self.AR_all_EESMAT_MC     = Systematic("AR_all_EESMAT_MC",   "_CENTRAL",  "_EESMATUP",     "_EESMATDOWN",			   "tree","overallSys")
            self.AR_all_EESMAT_CR     = Systematic("AR_all_EESMAT_CR",   "_CENTRAL",  "_EESMATUP",     "_EESMATDOWN",			   "tree","overallNormSys")
            self.AR_all_EESPS_MC      = Systematic("AR_all_EESPS_MC",    "_CENTRAL",  "_EESPSUP",      "_EESPSDOWN",			   "tree","overallSys")
            self.AR_all_EESPS_CR      = Systematic("AR_all_EESPS_CR",    "_CENTRAL",  "_EESPSUP",      "_EESPSDOWN",			   "tree","overallNormSys")
            self.AR_all_EESZ_MC       = Systematic("AR_all_EESZ_MC",     "_CENTRAL",  "_EESZUP",       "_EESZDOWN",			   "tree","overallSys")  
            self.AR_all_EESZ_CR       = Systematic("AR_all_EESZ_CR",     "_CENTRAL",  "_EESZUP",       "_EESZDOWN",			   "tree","overallNormSys") 
            self.AR_all_ESF_MC         = Systematic("AR_all_ESF_MC",    configMgr.weights,  ("eventweight","1.","syst_ESFUP"), 	("eventweight","1.","syst_ESFDOWN"), "weight","overallSys")
            self.AR_all_ESF_CR         = Systematic("AR_all_ESF_CR",    configMgr.weights,  ("eventweight","1.","syst_ESFUP"), 	("eventweight","1.","syst_ESFDOWN"),	"weight","overallNormSys")
            #	
        if doShapeFit:
            self.AR_all_EER_MC        = Systematic("AR_all_EER_MC",      "_CENTRAL",  "_EERUP",        "_EERDOWN",                          "tree","histoSys")
            self.AR_all_EER_CR        = Systematic("AR_all_EER_CR",      "_CENTRAL",  "_EERUP",        "_EERDOWN",                          "tree","normHistoSys")
            self.AR_all_EESLOW_MC     = Systematic("AR_all_EESLOW_MC",   "_CENTRAL",  "_EESLOWUP",     "_EESLOWDOWN",                       "tree","histoSys")
            self.AR_all_EESLOW_CR     = Systematic("AR_all_EESLOW_CR",   "_CENTRAL",  "_EESLOWUP",     "_EESLOWDOWN",                       "tree","normHistoSys")
            self.AR_all_EESMAT_MC     = Systematic("AR_all_EESMAT_MC",   "_CENTRAL",  "_EESMATUP",     "_EESMATDOWN",                       "tree","histoSys")
            self.AR_all_EESMAT_CR     = Systematic("AR_all_EESMAT_CR",   "_CENTRAL",  "_EESMATUP",     "_EESMATDOWN",                       "tree","normHistoSys")
            self.AR_all_EESPS_MC      = Systematic("AR_all_EESPS_MC",    "_CENTRAL",  "_EESPSUP",      "_EESPSDOWN",                        "tree","histoSys")
            self.AR_all_EESPS_CR      = Systematic("AR_all_EESPS_CR",    "_CENTRAL",  "_EESPSUP",      "_EESPSDOWN",                        "tree","normHistoSys")
            self.AR_all_EESZ_MC       = Systematic("AR_all_EESZ_MC",     "_CENTRAL",  "_EESZUP",       "_EESZDOWN",                         "tree","histoSys")
            self.AR_all_EESZ_CR       = Systematic("AR_all_EESZ_CR",     "_CENTRAL",  "_EESZUP",       "_EESZDOWN",                         "tree","overallNormSys")
            self.AR_all_ESF_MC         = Systematic("AR_all_ESF_MC",    configMgr.weights,  ("eventweight","1.","syst_ESFUP"),         ("eventweight","1.","syst_ESFDOWN"), "weight","histoSys")
            self.AR_all_ESF_CR         = Systematic("AR_all_ESF_CR",    configMgr.weights,  ("eventweight","1.","syst_ESFUP"),         ("eventweight","1.","syst_ESFDOWN"),  "weight","normHistoSys")

            
        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
        #                          MUONS                             #
        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

        if not doShapeFit:
            #self.AR_all_MID_MC         = Systematic("AR_all_MID_MC",        "_CENTRAL",  "_MIDUP",       "_MIDDOWN",			   "tree","overallSys")  
            self.AR_all_MID_MC         = Systematic("AR_all_MID_MC",        "_CENTRAL",  "_IDUP",       "_IDDOWN",			   "tree","overallSys")  
            #self.AR_all_MID_CR         = Systematic("AR_all_MID_CR",        "_CENTRAL",  "_MIDUP",       "_MIDDOWN",			   "tree","overallNormSys")
            self.AR_all_MID_CR         = Systematic("AR_all_MID_CR",        "_CENTRAL",  "_IDUP",       "_IDDOWN",			   "tree","overallNormSys")
            #self.AR_all_MMS_MC         = Systematic("AR_all_MMS_MC",        "_CENTRAL",  "_MMSUP",       "_MMSDOWN",			   "tree","overallSys")
            self.AR_all_MMS_MC         = Systematic("AR_all_MMS_MC",        "_CENTRAL",  "_MSUP",       "_MSDOWN",			   "tree","overallSys")
            #self.AR_all_MMS_CR         = Systematic("AR_all_MMS_CR",        "_CENTRAL",  "_MMSUP",       "_MMSDOWN",			   "tree","overallNormSys")
            self.AR_all_MMS_CR         = Systematic("AR_all_MMS_CR",        "_CENTRAL",  "_MSUP",       "_MSDOWN",			   "tree","overallNormSys")
            self.AR_all_MEFF_MC         = Systematic("AR_all_MEFF_MC",    configMgr.weights,  ("eventweight","1.","syst_MEFFUP"), 	("eventweight","1.","syst_MEFFDOWN"), "weight","overallSys")
            self.AR_all_MEFF_CR         = Systematic("AR_all_MEFF_CR",    configMgr.weights,  ("eventweight","1.","syst_MEFFUP"), 	("eventweight","1.","syst_MEFFDOWN"),	"weight","overallNormSys")
            #
        if doShapeFit:
            #self.AR_all_MID_MC         = Systematic("AR_all_MID_MC",        "_CENTRAL",  "_MIDUP",       "_MIDDOWN",                        "tree","histoSys")
            self.AR_all_MID_MC         = Systematic("AR_all_MID_MC",        "_CENTRAL",  "_IDUP",       "_IDDOWN",                        "tree","histoSys")
            #self.AR_all_MID_CR         = Systematic("AR_all_MID_CR",        "_CENTRAL",  "_MIDUP",       "_MIDDOWN",                        "tree","normHistoSys")
            self.AR_all_MID_CR         = Systematic("AR_all_MID_CR",        "_CENTRAL",  "_IDUP",       "_IDDOWN",                        "tree","normHistoSys")
            #self.AR_all_MMS_MC         = Systematic("AR_all_MMS_MC",        "_CENTRAL",  "_MMSUP",       "_MMSDOWN",                        "tree","histoSys")
            self.AR_all_MMS_MC         = Systematic("AR_all_MMS_MC",        "_CENTRAL",  "_MSUP",       "_MSDOWN",                        "tree","histoSys")
            #self.AR_all_MMS_CR         = Systematic("AR_all_MMS_CR",        "_CENTRAL",  "_MMSUP",       "_MMSDOWN",                        "tree","normHistoSys")
            self.AR_all_MMS_CR         = Systematic("AR_all_MMS_CR",        "_CENTRAL",  "_MSUP",       "_MSDOWN",                        "tree","normHistoSys")
            self.AR_all_MEFF_MC         = Systematic("AR_all_MEFF_MC",    configMgr.weights,  ("eventweight","1.","syst_MEFFUP"),      ("eventweight","1.","syst_MEFFDOWN"), "weight","histoSys")
            self.AR_all_MEFF_CR         = Systematic("AR_all_MEFF_CR",    configMgr.weights,  ("eventweight","1.","syst_MEFFUP"),      ("eventweight","1.","syst_MEFFDOWN"), "weight","normHistoSys")

            
        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
        #                      MISSING ENERGY                        #
        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

        if not doShapeFit:
            self.AR_all_RESOST_MC     = Systematic("AR_all_RESOST_MC",     "_CENTRAL",  "_RESOST",    "_CENTRAL",			   "tree","histoSysOneSide")   
            self.AR_all_RESOST_CR     = Systematic("AR_all_RESOST_CR",     "_CENTRAL",  "_RESOST",    "_CENTRAL",			   "tree","histoSysOneSide") 
            self.AR_all_SCALEST_MC    = Systematic("AR_all_SCALEST_MC",    "_CENTRAL",  "_SCALESTUP", "_SCALESTDOWN",		   "tree","overallSys") 
            self.AR_all_SCALEST_CR    = Systematic("AR_all_SCALEST_CR",    "_CENTRAL",  "_SCALESTUP", "_SCALESTDOWN",	   	   "tree","overallNormSys")
        #
        if doShapeFit:
            self.AR_all_RESOST_MC     = Systematic("AR_all_RESOST_MC",     "_CENTRAL",  "_RESOST",    "_CENTRAL",                           "tree","histoSys")
            self.AR_all_RESOST_CR     = Systematic("AR_all_RESOST_CR",     "_CENTRAL",  "_RESOST",    "_CENTRAL",                           "tree","normHistoSys")
            self.AR_all_SCALEST_MC    = Systematic("AR_all_SCALEST_MC",    "_CENTRAL",  "_SCALESTUP", "_SCALESTDOWN",               "tree","histoSys")
            self.AR_all_SCALEST_CR    = Systematic("AR_all_SCALEST_CR",    "_CENTRAL",  "_SCALESTUP", "_SCALESTDOWN",               "tree","normHistoSys")

        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
        #                      PILEUP UNCERT                         #
        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

        if not doShapeFit:
            self.AR_all_PILEUP_MC         = Systematic("AR_all_PILEUP_MC",    configMgr.weights,  ("eventweight","1.","syst_PILEUPUP"),        ("eventweight","1.","syst_PILEUPUP"), "weight","overallSys")
            self.AR_all_PILEUP_CR         = Systematic("AR_all_PILEUP_CR",    configMgr.weights,  ("eventweight","1.","syst_PILEUPUP"),        ("eventweight","1.","syst_PILEUPUP"), "weight","overallNormSys")
			
        if doShapeFit:
            self.AR_all_PILEUP_MC         = Systematic("AR_all_PILEUP_MC",    configMgr.weights,  ("eventweight","1.","syst_PILEUPUP"),        ("eventweight","1.","syst_PILEUPUP"), "weight","histoSys")
            self.AR_all_PILEUP_CR         = Systematic("AR_all_PILEUP_CR",    configMgr.weights,  ("eventweight","1.","syst_PILEUPUP"),        ("eventweight","1.","syst_PILEUPUP"), "weight","normHistoSys")			

            
        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
        #                      THEORY UNCERT                         #
        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
        
        if not doShapeFit:
            self.AR_all_GENttst        = Systematic("AR_all_GENttst ",     configMgr.weights,  ("eventweight","1.","syst_GEN"),        ("eventweight","1.","syst_GEN"), "weight","overallNormSys") 
            self.AR_all_GENWW          = Systematic("AR_all_GENWW ",       configMgr.weights,  ("eventweight","1.","syst_GEN"),        ("eventweight","1.","syst_GEN"), "weight","overallNormSys") 
            self.AR_all_GENZV          = Systematic("AR_all_GENZV ",       configMgr.weights,  ("eventweight","1.","syst_GEN"),        ("eventweight","1.","syst_GEN"), "weight","overallNormSys") 
            self.AR_all_SHOWERttst     = Systematic("AR_all_SHOWERttst ",  configMgr.weights,  ("eventweight","1.","syst_PS"),        ("eventweight","1.","syst_PS"), "weight","overallNormSys")
            self.AR_all_SHOWERWW       = Systematic("AR_all_SHOWERWW ",    configMgr.weights,  ("eventweight","1.","syst_PS"),        ("eventweight","1.","syst_PS"), "weight","overallNormSys")
            self.AR_all_SHOWERZV       = Systematic("AR_all_SHOWERZV ",    configMgr.weights,  ("eventweight","1.","syst_PS"),        ("eventweight","1.","syst_PS"), "weight","overallNormSys")
            self.AR_all_IFSRttst       = Systematic("AR_all_IFSRttst ",    configMgr.weights,  ("eventweight","1.","syst_IFSR"),      ("eventweight","1.","syst_IFSR"), "weight","overallNormSys")
            self.AR_all_SCALEWW        = Systematic("AR_all_SCALEWW ",     configMgr.weights,  ("eventweight","1.","syst_SCALE"),     ("eventweight","1.","syst_SCALE"), "weight","overallNormSys")
            self.AR_all_SCALEZV        = Systematic("AR_all_SCALEZV ",     configMgr.weights,  ("eventweight","1.","syst_SCALE"),     ("eventweight","1.","syst_SCALE"), "weight","overallNormSys")
            self.AR_all_PDFWW          = Systematic("AR_all_PDFWW ",       configMgr.weights,  ("eventweight","1.","syst_PDFERRUP"),       ("eventweight","1.","syst_PDFERRDOWN"), "weight","overallNormSys")
            self.AR_all_PDFZV          = Systematic("AR_all_PDFZV ",       configMgr.weights,  ("eventweight","1.","syst_PDFERRUP"),       ("eventweight","1.","syst_PDFERRDOWN"), "weight","overallNormSys")

        if doShapeFit:
            self.AR_all_GENttst       = Systematic("AR_all_GENttst",     configMgr.weights,  ("eventweight","1.","syst_GEN"),        ("eventweight","1.","syst_GEN"), "weight","normHistoSys")
            self.AR_all_GENWW         = Systematic("AR_all_GENWW",       configMgr.weights,  ("eventweight","1.","syst_GEN"),        ("eventweight","1.","syst_GEN"), "weight","normHistoSys")
            self.AR_all_GENZV         = Systematic("AR_all_GENZV",       configMgr.weights,  ("eventweight","1.","syst_GEN"),        ("eventweight","1.","syst_GEN"), "weight","normHistoSys")
            self.AR_all_SHOWERttst    = Systematic("AR_all_SHOWERttst",  configMgr.weights,  ("eventweight","1.","syst_PS"),        ("eventweight","1.","syst_PS"), "weight","normHistoSys")
            self.AR_all_SHOWERWW      = Systematic("AR_all_SHOWERWW",    configMgr.weights,  ("eventweight","1.","syst_PS"),        ("eventweight","1.","syst_PS"), "weight","normHistoSys")
            self.AR_all_SHOWERZV      = Systematic("AR_all_SHOWERZV",    configMgr.weights,  ("eventweight","1.","syst_PS"),        ("eventweight","1.","syst_PS"), "weight","normHistoSys")
            self.AR_all_IFSRttst      = Systematic("AR_all_IFSRttst",    configMgr.weights,  ("eventweight","1.","syst_IFSR"),      ("eventweight","1.","syst_IFSR"), "weight","normHistoSys")
            self.AR_all_SCALEWW       = Systematic("AR_all_SCALEWW",     configMgr.weights,  ("eventweight","1.","syst_SCALE"),     ("eventweight","1.","syst_SCALE"), "weight","normHistoSys")
            self.AR_all_SCALEZV       = Systematic("AR_all_SCALEZV",     configMgr.weights,  ("eventweight","1.","syst_SCALE"),     ("eventweight","1.","syst_SCALE"), "weight","normHistoSys")
            self.AR_all_PDFWW         = Systematic("AR_all_PDFWW",       configMgr.weights,  ("eventweight","1.","syst_PDFERRUP"),       ("eventweight","1.","syst_PDFERRDOWN"), "weight","normHistoSys")
            self.AR_all_PDFZV         = Systematic("AR_all_PDFZV",       configMgr.weights,  ("eventweight","1.","syst_PDFERRUP"),       ("eventweight","1.","syst_PDFERRDOWN"), "weight","normHistoSys")

        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
        #                          TRIGGER                           #
        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

        if not doShapeFit:
            self.AR_all_TRIGGERE_MC = Systematic("AR_all_TRIGGERE_MC",    configMgr.weights,  ("eventweight","1.","syst_ETRIGREWDOWN"),  ("eventweight","1.","syst_ETRIGREWDOWN"), "weight","overallSys")
            self.AR_all_TRIGGERE_CR = Systematic("AR_all_TRIGGERE_CR",    configMgr.weights,  ("eventweight","1.","syst_ETRIGREWDOWN"),  ("eventweight","1.","syst_ETRIGREWDOWN"), "weight","overallNormSys")
            self.AR_all_TRIGGERM_MC = Systematic("AR_all_TRIGGERM_MC",    configMgr.weights,  ("eventweight","1.","syst_MTRIGREWDOWN"),  ("eventweight","1.","syst_MTRIGREWDOWN"), "weight","overallSys")
            self.AR_all_TRIGGERM_CR = Systematic("AR_all_TRIGGERM_CR",    configMgr.weights,  ("eventweight","1.","syst_MTRIGREWDOWN"),  ("eventweight","1.","syst_MTRIGREWDOWN"), "weight","overallNormSys")		

        if doShapeFit:
            self.AR_all_TRIGGERE_MC = Systematic("AR_all_TRIGGERE_MC",    configMgr.weights,  ("eventweight","1.","syst_ETRIGREWDOWN"),  ("eventweight","1.","syst_ETRIGREWDOWN"), "weight","histoSys")
            self.AR_all_TRIGGERE_CR = Systematic("AR_all_TRIGGERE_CR",    configMgr.weights,  ("eventweight","1.","syst_ETRIGREWDOWN"),  ("eventweight","1.","syst_ETRIGREWDOWN"), "weight","normHistoSys")
            self.AR_all_TRIGGERM_MC = Systematic("AR_all_TRIGGERM_MC",    configMgr.weights,  ("eventweight","1.","syst_MTRIGREWDOWN"),  ("eventweight","1.","syst_MTRIGREWDOWN"), "weight","histoSys")
            self.AR_all_TRIGGERM_CR = Systematic("AR_all_TRIGGERM_CR",    configMgr.weights,  ("eventweight","1.","syst_MTRIGREWDOWN"),  ("eventweight","1.","syst_MTRIGREWDOWN"), "weight","normHistoSys")			
        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
        #                         FAKE ERRORS                        #
        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

        if not doShapeFit:
            self.AR_fakes_ELFR      = Systematic("AR_fakes_ELFR",    "_CENTRAL",  "_ELFRUP","_ELFRDOWN",                      "tree","overallSys")
            self.AR_fakes_ELRE      = Systematic("AR_fakes_ELRE",    "_CENTRAL",  "_ELREUP","_ELREDOWN",                      "tree","overallSys")
            self.AR_fakes_MUFR      = Systematic("AR_fakes_MUFR",    "_CENTRAL",  "_MUFRUP","_MUFRDOWN",                      "tree","overallSys")
            self.AR_fakes_MURE      = Systematic("AR_fakes_MURE",    "_CENTRAL",  "_MUREUP","_MUREDOWN",                      "tree","overallSys")
            #
        if doShapeFit:
            self.AR_fakes_ELFR      = Systematic("AR_fakes_ELFR",    "_CENTRAL",  "_ELFRUP","_ELFRDOWN",                      "tree","histoSys")
            self.AR_fakes_ELRE      = Systematic("AR_fakes_ELRE",    "_CENTRAL",  "_ELREUP","_ELREDOWN",                      "tree","histoSys")
            self.AR_fakes_MUFR      = Systematic("AR_fakes_MUFR",    "_CENTRAL",  "_MUFRUP","_MUFRDOWN",                      "tree","histoSys")
            self.AR_fakes_MURE      = Systematic("AR_fakes_MURE",    "_CENTRAL",  "_MUREUP","_MUREDOWN",                      "tree","histoSys")

        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
        #            Statistical Error for MC if Split               #
        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

        if splitMCsystsIntoSamples:
            self.AR_mcstat_ZX   = Systematic("AR_mcstat_ZX"     , "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.AR_mcstat_FAKE = Systematic("AR_mcstat_FAKE"   , "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.AR_mcstat_H    = Systematic("AR_mcstat_H"      , "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.AR_mcstat_ZV   = Systematic("AR_mcstat_ZV"     , "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.AR_mcstat_TOP  = Systematic("AR_mcstat_TOP"    , "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.AR_mcstat_WW   = Systematic("AR_mcstat_WW"     , "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")
            self.AR_mcstat_SIG  = Systematic("AR_mcstat_SIG"    , "_CENTRAL", "_CENTRAL", "_CENTRAL", "tree", "shapeStat")


        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
        #                   THEORY UNCERTAINTIES                     #
        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

        def getTheorySys(sysName, process, region):
            return Systematic(sysName,configMgr.weights,1.0+getRelUncert(process,region),1.0-getRelUncert(process,region),"user","userOverallSys")

        # TODO : MAKE THESE CORRELATED -- SEE TABLE 74 (PDF page 152) in previous 2LOS IntNote

        ##
        ## WW
        ##

#        self.SRmT2a_WW_THEORY   = getTheorySys("SR_WW_THEORY","WW","SRmT2a")
#        self.SRmT2b_WW_THEORY   = getTheorySys("SR_WW_THEORY","WW","SRmT2b")
#        self.SRmT2c_WW_THEORY   = getTheorySys("SR_WW_THEORY","WW","SRmT2c")
#        self.SRWWa_WW_THEORY    = getTheorySys("SR_WW_THEORY","WW","SRWWa")
#        self.SRWWb_WW_THEORY    = getTheorySys("SR_WW_THEORY","WW","SRWWb")
#        self.SRWWc_WW_THEORY    = getTheorySys("SR_WW_THEORY","WW","SRWWc")
#        self.SRZjets_WW_THEORY  = getTheorySys("SR_WW_THEORY","WW","SRZjets")

        # -=-=-=-=-=-=-=-=-=-=-=-==-= #
        #       DANTRIM    WW         #
        # -=-=-=-=-=-=-=-=-=-=-=-=-=- #
        
        self.SR0a_WW_THEORY     = getTheorySys("SR_WW_THEORY", "WW", "Super0a")
        self.SR0b_WW_THEORY     = getTheorySys("SR_WW_THEORY", "WW", "Super0b")
        self.SR0c_WW_THEORY     = getTheorySys("SR_WW_THEORY", "WW", "Super0c")
        self.SR1a_WW_THEORY     = getTheorySys("SR_WW_THEORY", "WW", "Super1a")
        self.SR1b_WW_THEORY     = getTheorySys("SR_WW_THEORY", "WW", "Super1b")
        self.SR1c_WW_THEORY     = getTheorySys("SR_WW_THEORY", "WW", "Super1c") 

        ##
        ## ZV
        ##

#        self.SRmT2a_ZV_THEORY   = getTheorySys("SR_ZV_THEORY","ZV","SRmT2a")
#        self.SRmT2b_ZV_THEORY   = getTheorySys("SR_ZV_THEORY","ZV","SRmT2b")
#        self.SRmT2c_ZV_THEORY   = getTheorySys("SR_ZV_THEORY","ZV","SRmT2c")
#        self.SRWWa_ZV_THEORY    = getTheorySys("SR_ZV_THEORY","ZV","SRWWa")
#        self.SRWWb_ZV_THEORY    = getTheorySys("SR_ZV_THEORY","ZV","SRWWb")
#        self.SRWWc_ZV_THEORY    = getTheorySys("SR_ZV_THEORY","ZV","SRWWc")
#        self.SRZjets_ZV_THEORY  = getTheorySys("SR_ZV_THEORY","ZV","SRZjets")

        # -=-=-=-=-=-=-=-=-=-=-=-==-= #
        #       DANTRIM   ZV          #
        # -=-=-=-=-=-=-=-=-=-=-=-=-=- #
    

        self.SR0a_ZV_THEORY     = getTheorySys("SR_ZV_THEORY", "ZV", "Super0a")
        self.SR0b_ZV_THEORY     = getTheorySys("SR_ZV_THEORY", "ZV", "Super0b")
        self.SR0c_ZV_THEORY     = getTheorySys("SR_ZV_THEORY", "ZV", "Super0c")
        self.SR1a_ZV_THEORY     = getTheorySys("SR_ZV_THEORY", "ZV", "Super1a")
        self.SR1b_ZV_THEORY     = getTheorySys("SR_ZV_THEORY", "ZV", "Super1b")
        self.SR1c_ZV_THEORY     = getTheorySys("SR_ZV_THEORY", "ZV", "Super1c")



        ##
        ## Top
        ##

#        self.SRmT2a_Top_THEORY   = getTheorySys("SR_Top_THEORY","Top","SRmT2a")
#        self.SRmT2b_Top_THEORY   = getTheorySys("SR_Top_THEORY","Top","SRmT2b")
#        self.SRmT2c_Top_THEORY   = getTheorySys("SR_Top_THEORY","Top","SRmT2c")
#        self.SRWWa_Top_THEORY    = getTheorySys("SR_Top_THEORY","Top","SRWWa")
#        self.SRWWb_Top_THEORY    = getTheorySys("SR_Top_THEORY","Top","SRWWb")
#        self.SRWWc_Top_THEORY    = getTheorySys("SR_Top_THEORY","Top","SRWWc")
#        self.SRZjets_Top_THEORY  = getTheorySys("SR_Top_THEORY","Top","SRZjets")

        # -=-=-=-=-=-=-=-=-=-=-=-==-= #
        #       DANTRIM   TOP         #
        # -=-=-=-=-=-=-=-=-=-=-=-=-=- #
        
#        self.SR0a_Top_THEORY    = getTheorySys("SR_Top_THEORY", "Top", "Super0a")
#        self.SR0b_Top_THEORY    = getTheorySys("SR_Top_THEORY", "Top", "Super0b")
#        self.SR0c_Top_THEORY    = getTheorySys("SR_Top_THEORY", "Top", "Super0c")
#        self.SR1a_Top_THEORY    = getTheorySys("SR_Top_THEORY", "Top", "Super1a")
#        self.SR1b_Top_THEORY    = getTheorySys("SR_Top_THEORY", "Top", "Super1b")
#        self.SR1c_Top_THEORY    = getTheorySys("SR_Top_THEORY", "Top", "Super1c")


        # >> Extracting out only ttbar PS, grouping the rest
        # PS
        self.SR1a_TT_PS         = getTheorySys("TT_PS",     "Top",      "sr1a_tt_ps")
        self.SR1b_TT_PS         = getTheorySys("TT_PS",     "Top",      "sr1b_tt_ps")
        self.SR1c_TT_PS         = getTheorySys("TT_PS",     "Top",      "sr1c_tt_ps")
        
        self.CRWWb_TT_PS        = getTheorySys("TT_PS",     "Top",      "crwwb_tt_ps")
        # other
        self.SR1a_Top_Other     = getTheorySys("Top_SR_other", "Top",   "sr1a_top_other")
        self.SR1b_Top_Other     = getTheorySys("Top_SR_other", "Top",   "sr1b_top_other")
        self.SR1c_Top_Other     = getTheorySys("Top_SR_other", "Top",   "sr1c_top_other")
        
        self.CRWWb_Top_Other    = getTheorySys("Top_CR_other", "Top",   "crwwb_top_other")
         

        # >> Breaking Top uncertainties down to each component
 #       self.SR1a_TT_GEN        = getTheorySys("TT_GEN", "Top",         "sr1a_tt_gen")  
 #       self.SR1a_TT_PS         = getTheorySys("TT_PS", "Top",          "sr1a_tt_ps")
 #       self.SR1a_TT_ISRFSR     = getTheorySys("TT_ISRFSR", "Top",      "sr1a_tt_isrfsr")
 #       self.SR1a_TT_PDF        = getTheorySys("TT_PDF", "Top",         "sr1a_tt_pdf")
 #       self.SR1a_TT_QCD        = getTheorySys("TT_QCD", "Top",         "sr1a_tt_qcd")
 #       self.SR1a_ST_GEN        = getTheorySys("ST_GEN", "Top",         "sr1a_st_gen")
 #       self.SR1a_ST_PS         = getTheorySys("ST_PS", "Top",          "sr1a_st_ps")
 #       self.SR1a_ST_DSDR       = getTheorySys("ST_DSDR", "Top",        "sr1a_st_dsdr")
 #       self.SR1a_ST_ISRFSR     = getTheorySys("ST_ISRFSR", "Top",      "sr1a_st_isrfsr")
 #       self.SR1a_ST_PDF        = getTheorySys("ST_PDF", "Top",         "sr1a_st_pdf")
 #       
 #       self.SR1b_TT_GEN        = getTheorySys("TT_GEN", "Top",         "sr1b_tt_gen")  
 #       self.SR1b_TT_PS         = getTheorySys("TT_PS", "Top",          "sr1b_tt_ps")
 #       self.SR1b_TT_ISRFSR     = getTheorySys("TT_ISRFSR", "Top",      "sr1b_tt_isrfsr")
 #       self.SR1b_TT_PDF        = getTheorySys("TT_PDF", "Top",         "sr1b_tt_pdf")
 #       self.SR1b_TT_QCD        = getTheorySys("TT_QCD", "Top",         "sr1b_tt_qcd")
 #       self.SR1b_ST_GEN        = getTheorySys("ST_GEN", "Top",         "sr1b_st_gen")
 #       self.SR1b_ST_PS         = getTheorySys("ST_PS", "Top",          "sr1b_st_ps")
 #       self.SR1b_ST_DSDR       = getTheorySys("ST_DSDR", "Top",        "sr1b_st_dsdr")
 #       self.SR1b_ST_ISRFSR     = getTheorySys("ST_ISRFSR", "Top",      "sr1b_st_isrfsr")
 #       self.SR1b_ST_PDF        = getTheorySys("ST_PDF", "Top",         "sr1b_st_pdf")
 #       
 #       self.SR1c_TT_GEN        = getTheorySys("TT_GEN", "Top",         "sr1c_tt_gen")  
 #       self.SR1c_TT_PS         = getTheorySys("TT_PS", "Top",          "sr1c_tt_ps")
 #       self.SR1c_TT_ISRFSR     = getTheorySys("TT_ISRFSR", "Top",      "sr1c_tt_isrfsr")
 #       self.SR1c_TT_PDF        = getTheorySys("TT_PDF", "Top",         "sr1c_tt_pdf")
 #       self.SR1c_TT_QCD        = getTheorySys("TT_QCD", "Top",         "sr1c_tt_qcd")
 #       self.SR1c_ST_GEN        = getTheorySys("ST_GEN", "Top",         "sr1c_st_gen")
 #       self.SR1c_ST_PS         = getTheorySys("ST_PS", "Top",          "sr1c_st_ps")
 #       self.SR1c_ST_DSDR       = getTheorySys("ST_DSDR", "Top",        "sr1c_st_dsdr")
 #       self.SR1c_ST_ISRFSR     = getTheorySys("ST_ISRFSR", "Top",      "sr1c_st_isrfsr")
 #       self.SR1c_ST_PDF        = getTheorySys("ST_PDF", "Top",         "sr1c_st_pdf")
 #       

 #       self.CRWW_TT_GEN        = getTheorySys("TT_GEN", "Top",         "crww_tt_gen")
 #       self.CRWW_TT_PS         = getTheorySys("TT_PS", "Top",          "crww_tt_ps")
 #       self.CRWW_TT_ISRFSR     = getTheorySys("TT_ISRFSR", "Top",      "crww_tt_isrfsr")
 #       self.CRWW_TT_PDF        = getTheorySys("TT_PDF", "Top",         "crww_tt_pdf")
 #       self.CRWW_TT_QCD        = getTheorySys("TT_QCD", "Top",         "crww_tt_qcd")
 #       self.CRWW_ST_GEN        = getTheorySys("ST_GEN", "Top",         "crww_st_gen")
 #       self.CRWW_ST_PS         = getTheorySys("ST_PS", "Top",          "crww_st_ps")
 #       self.CRWW_ST_DSDR       = getTheorySys("ST_DSDR", "Top",        "crww_st_dsdr")
 #       self.CRWW_ST_ISRFSR     = getTheorySys("ST_ISRFSR", "Top",      "crww_st_isrfsr")
 #       self.CRWW_ST_PDF        = getTheorySys("ST_PDF", "Top",         "crww_st_pdf") 

        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
        # Do similar for preliminary fakes -- i.e. add rel uncertainty in by hand 
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
        self.eeSR0a_FakeRelUnc       = getTheorySys("Fake_RelUnc", "Fake", "eeSuper0a")
        self.mmSR0a_FakeRelUnc       = getTheorySys("Fake_RelUnc", "Fake", "mmSuper0a")
        self.emSR0a_FakeRelUnc       = getTheorySys("Fake_RelUnc", "Fake", "emSuper0a")
        self.eeSR0b_FakeRelUnc       = getTheorySys("Fake_RelUnc", "Fake", "eeSuper0b")
        self.mmSR0b_FakeRelUnc       = getTheorySys("Fake_RelUnc", "Fake", "mmSuper0b")
        self.emSR0b_FakeRelUnc       = getTheorySys("Fake_RelUnc", "Fake", "emSuper0b")
        self.eeSR0c_FakeRelUnc       = getTheorySys("Fake_RelUnc", "Fake", "eeSuper0c")
        self.mmSR0c_FakeRelUnc       = getTheorySys("Fake_RelUnc", "Fake", "mmSuper0c")
        self.emSR0c_FakeRelUnc       = getTheorySys("Fake_RelUnc", "Fake", "emSuper0c")
        self.eeSR1a_FakeRelUnc       = getTheorySys("Fake_RelUnc", "Fake", "eeSuper1a")
        self.mmSR1a_FakeRelUnc       = getTheorySys("Fake_RelUnc", "Fake", "mmSuper1a")
        self.emSR1a_FakeRelUnc       = getTheorySys("Fake_RelUnc", "Fake", "emSuper1a")
        self.eeSR1b_FakeRelUnc       = getTheorySys("Fake_RelUnc", "Fake", "eeSuper1b")
        self.mmSR1b_FakeRelUnc       = getTheorySys("Fake_RelUnc", "Fake", "mmSuper1b")
        self.emSR1b_FakeRelUnc       = getTheorySys("Fake_RelUnc", "Fake", "emSuper1b")
        self.eeSR1c_FakeRelUnc       = getTheorySys("Fake_RelUnc", "Fake", "eeSuper1c")
        self.mmSR1c_FakeRelUnc       = getTheorySys("Fake_RelUnc", "Fake", "mmSuper1c")
        self.emSR1c_FakeRelUnc       = getTheorySys("Fake_RelUnc", "Fake", "emSuper1c")
        self.emCRTop14a_FakeRelUnc   = getTheorySys("Fake_RelUnc", "Fake", "emCRTop14a")
        self.emCRTop14b_FakeRelUnc   = getTheorySys("Fake_RelUnc", "Fake", "emCRTop14b")
        self.emCRWW14a_FakeRelUnc    = getTheorySys("Fake_RelUnc", "Fake", "emCRWW14a")
        self.emCRWW14b_FakeRelUnc    = getTheorySys("Fake_RelUnc", "Fake", "emCRWW14b")
        self.emCRZV14a_FakeRelUnc    = getTheorySys("Fake_RelUnc", "Fake", "emCRZV14a")
        self.emCRZV14b_FakeRelUnc    = getTheorySys("Fake_RelUnc", "Fake", "emCRZV14b")
        self.sfSR0a_FakeRelUnc       = getTheorySys("Fake_RelUnc", "Fake", "sfSuper0a")
        self.sfSR0b_FakeRelUnc       = getTheorySys("Fake_RelUnc", "Fake", "sfSuper0b")
        self.sfSR0c_FakeRelUnc       = getTheorySys("Fake_RelUnc", "Fake", "sfSuper0c")
        self.sfSR1a_FakeRelUnc       = getTheorySys("Fake_RelUnc", "Fake", "sfSuper1a")
        self.sfSR1b_FakeRelUnc       = getTheorySys("Fake_RelUnc", "Fake", "sfSuper1b")
        self.sfSR1c_FakeRelUnc       = getTheorySys("Fake_RelUnc", "Fake", "sfSuper1c")




    # end the constructor
