
# Return the relative theory uncertainty
# Numbers from Geraldine received on 31/7/2013
def getRelUncert(process, region):
#  # WW
#  WWUncertainties = { 
#                     "SRWWa"  : 0.06, 
#                     "SRWWb"  : 0.16, 
#                     "SRWWc"  : 0.29, 
#                     "SRmT2a" : 0.18, 
#                     "SRmT2b" : 0.37, 
#                     "SRmT2c" : 0.34, 
#                     "SRZjets": 0.02 
#                    }
#  # ZV
#  ZVUncertainties = { 
#                     "SRWWa"  : 0.14, 
#                     "SRWWb"  : 0.25, 
#                     "SRWWc"  : 0.28, 
#                     "SRmT2a" : 0.23, 
#                     "SRmT2b" : 0.47, 
#                     "SRmT2c" : 0.68, 
#                     "SRZjets": 0.36 
#                    }
#  # Top
#  TopUncertainties = { 
#                     "SRWWa"  : 0.28, 
#                     "SRWWb"  : 0.14, 
#                     "SRWWc"  : 0.23, 
#                     "SRmT2a" : 0.22, 
#                     "SRmT2b" : 0.41, 
#                     "SRmT2c" : 0.61, 
#                     "SRZjets": 0.    # Missing 
#                    }
        

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #   DANTRIM : Numbers from Sarah Williams             #
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    
    # WW (still for mDR>70 in SR0a) 
    WWUncertainties = { "Super0a" : 0.0511,
                        "Super0b" : 0.3340,
                        "Super0c" : 0.4331,
                        "Super1a" : 0.1820,
                        "Super1b" : 0.3021,
                        "Super1c" : 0.2323
                      }
    # ZV (still for mDR>70 in SR0a)
    ZVUncertainties = { "Super0a" : 0.1333,
                        "Super0b" : 0.3140,
                        "Super0c" : 0.2404,
                        "Super1a" : 0.2682,
                        "Super1b" : 0.4540,
                        "Super1c" : 0.4754
                      }
#    # Top (from Sarah, ~Jan 10th 2015 --> after changing SR0a to mDR>90)
#    TopUncertainties = { "Super0a" : 0.248,
#                         "Super0b" : 0.489,
#                         "Super0c" : 0.872
#                         "Super1a" : 0.252,
#                         "Super1b" : 0.281,
#                         "Super1c" : 0.286
#                       }

    #>> Break the top uncertainty down into components
    TopUncertainties = {}
    # PS
    TopUncertainties["sr1a_tt_ps"]       = 0.23 # 22.97 pm 3.02
    TopUncertainties["sr1b_tt_ps"]       = 0.25 # 24.33 pm 5.76
    TopUncertainties["sr1c_tt_ps"]       = 0.27 # 26.72 pm 3.90
    TopUncertainties["crwwb_tt_ps"]      = 0.287 # 26.68 pm 1.30
    TopUncertainties["sr1a_top_other"]   = 0.122 # 11.55 pm 3.80
    TopUncertainties["sr1b_top_other"]   = 0.157 # 13.91 pm 7.28
    TopUncertainties["sr1c_top_other"]   = 0.12 # 10.01 pm 5.02
    TopUncertainties["crwwb_top_other"]  = 0.133 # 13.18 pm 2.00 
#    TopUncertainties["sr1a_tt_gen"]     = 0.102 #10.2
#    TopUncertainties["sr1a_tt_ps"]      = 0.232 #23.17
#    TopUncertainties["sr1a_tt_isrfsr"]  = 0.031 #3.06
#    TopUncertainties["sr1a_tt_pdf"]     = 0.013 #1.34
#    TopUncertainties["sr1a_tt_qcd"]     = 0.061 #6.13
#    TopUncertainties["sr1a_st_gen"]     = 0.034 #3.39
#    TopUncertainties["sr1a_st_ps"]      = 0.041 #4.08
#    TopUncertainties["sr1a_st_dsdr"]    = 0.04  #3.60
#    TopUncertainties["sr1a_st_isrfsr"]  = 0.03  #2.65
#    TopUncertainties["sr1a_st_pdf"]     = 0.014 #1.42
#
#    TopUncertainties["sr1b_tt_gen"]     = 0.135 #13.54 
#    TopUncertainties["sr1b_tt_ps"]      = 0.25  #25.01
#    TopUncertainties["sr1b_tt_isrfsr"]  = 0.061 #6.07
#    TopUncertainties["sr1b_tt_pdf"]     = 0.012 #1.21
#    TopUncertainties["sr1b_tt_qcd"]     = 0.067  #6.70
#    TopUncertainties["sr1b_st_gen"]     = 0.067 #6.73
#    TopUncertainties["sr1b_st_ps"]      = 0.068 #6.75
#    TopUncertainties["sr1b_st_dsdr"]    = 0.08  #7.99
#    TopUncertainties["sr1b_st_isrfsr"]  = 0.033 #3.34
#    TopUncertainties["sr1b_st_pdf"]     = 0.012 #1.24
#
#    TopUncertainties["sr1c_tt_gen"]     = 0.092 #9.15 
#    TopUncertainties["sr1c_tt_ps"]      = 0.27  #27.00
#    TopUncertainties["sr1c_tt_isrfsr"]  = 0.03  #2.99
#    TopUncertainties["sr1c_tt_pdf"]     = 0.014 #1.42
#    TopUncertainties["sr1c_tt_qcd"]     = 0.042 #4.15
#    TopUncertainties["sr1c_st_gen"]     = 0.047 #4.74
#    TopUncertainties["sr1c_st_ps"]      = 0.068 #6.82
#    TopUncertainties["sr1c_st_dsdr"]    = 0.05  #4.92
#    TopUncertainties["sr1c_st_isrfsr"]  = 0.05  #5.03
#    TopUncertainties["sr1c_st_pdf"]     = 0.011 #1.17
#
#    TopUncertainties["crww_tt_gen"]     = 0.12  #12.02 
#    TopUncertainties["crww_tt_ps"]      = 0.267 #26.71
#    TopUncertainties["crww_tt_isrfsr"]  = 0.011 #1.13
#    TopUncertainties["crww_tt_pdf"]     = 0.015 #1.47
#    TopUncertainties["crww_tt_qcd"]     = 0.016 #1.62
#    TopUncertainties["crww_st_gen"]     = 0.025 #2.54
#    TopUncertainties["crww_st_ps"]      = 0.05  #5.02
#    TopUncertainties["crww_st_dsdr"]    = 0.017 #1.71
#    TopUncertainties["crww_st_isrfsr"]  = 0.015 #1.49
#    TopUncertainties["crww_st_pdf"]     = 0.014 #1.43

    # Preliminary fakes added in by hand
    # from FakeMatrix_Nov26_wSys from Davide (adding elfrac/mufrac) 
    # January 19, 2015
    FakeUncertainties   = { "eeSuper0a" : 1.83, 
                            "mmSuper0a" : 0.189,
                            "emSuper0a" : 1.57,
                            "eeSuper0b" : 1.71,
                            "mmSuper0b" : 0.50,
                            "emSuper0b" : 1.83,
                            "eeSuper0c" : 5.50,
                            "mmSuper0c" : 1.00,
                            "emSuper0c" : 0.60,
                            "eeSuper1a" : 0.34,
                            "mmSuper1a" : 0.716,
                            "emSuper1a" : 0.343,
                            "eeSuper1b" : 0.877,
                            "mmSuper1b" : 15.22,
                            "emSuper1b" : 0.91,
                            "eeSuper1c" : 0.383,
                            "mmSuper1c" : 0.447,
                            "emSuper1c" : 0.397,
                            "emCRTop14a" : 1.64,
                            "emCRTop14b" : 2.90,
                            "emCRWW14a"  : 0.820,
                            "emCRWW14b"  : 0.434,
                            "emCRZV14a"  : 0.155,
                            "emCRZV14b"  : 1.28,
                            "sfSuper0a" : 0.86,
                            "sfSuper0b" : 0.65,
                            "sfSuper0c" : 0.92,
                            "sfSuper1a" : 0.49,
                            "sfSuper1b" : 0.95,
                            "sfSuper1c" : 0.37
                          }
                
    
  # Return the value
    if process=="WW":
        return WWUncertainties[region]
    elif process=="ZV":
        return ZVUncertainties[region]
    elif process=="Top":
        return TopUncertainties[region]
    elif process=="Fake":
        return FakeUncertainties[region]
    else:
        return 0.

# Testing
#print "WW  - SRWWa   = ", getRelativeTheoryUncertainty("WW","SRWWa")
#print "ZV  - SRZjets = ", getRelativeTheoryUncertainty("ZV","SRZjets")
#print "Top - SRmT2a  = ", getRelativeTheoryUncertainty("Top","SRmT2a")
