
###########################################################
# This script will configure the cut dictionary. Having   #
# it in the main body seems like such a waste of space.   #
# Can move it here and then we can add cuts in a specific #
# file, incase of new signal or validaiton regions. A lot #
# of this has been ported over from Geraldine's code.     #
###########################################################


def selectionConfig(mgr, slepNumber):

    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
    #                 Specify SR-WW                  #
    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

    ## WWa
    mgr.cutsDict["SR1"] = "(isOS && nCentralLightJets==0 && nCentralBJets==0 && nForwardJets==0 && lept1Pt>35000. && lept2Pt>20000. && metrel>80000. && pTll>80000.  && mll<120000.)"
    ## WWb
    mgr.cutsDict["SR2a"] = "(isOS && nCentralLightJets==0 && nCentralBJets==0 && nForwardJets==0 && lept1Pt>35000. && lept2Pt>20000. && MT2>90000. && mll<170000)"
    ## WWc
    mgr.cutsDict["SR2b"] = "(isOS && nCentralLightJets==0 && nCentralBJets==0 && nForwardJets==0 && lept1Pt>35000. && lept2Pt>20000. && MT2>100000. )"


    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
    #                 Specify SR-mT2                 #
    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

    ## mT2a
    mgr.cutsDict["SR4a"] = "(isOS && nCentralLightJets==0 && nCentralBJets==0 && nForwardJets==0 && lept1Pt>35000. && lept2Pt>20000. && MT2>90000.)"
    ## mT2b
    mgr.cutsDict["SR4b"] = "(isOS && nCentralLightJets==0 && nCentralBJets==0 && nForwardJets==0 && lept1Pt>35000. && lept2Pt>20000. && MT2>120000.)"
    ## mT2c
    mgr.cutsDict["SR4c"] = "(isOS && nCentralLightJets==0 && nCentralBJets==0 && nForwardJets==0 && lept1Pt>35000. && lept2Pt>20000. && MT2>150000.)"

    if slepNumber == 1: # LH slepton case
        mgr.cutsDict["SR4a"] = "(" + mgr.cutsDict["SR4a"] + " && (L2finalState==-1 || L2finalState==201 || L2finalState==216))"
        mgr.cutsDict["SR4b"] = "(" + mgr.cutsDict["SR4b"] + " && (L2finalState==-1 || L2finalState==201 || L2finalState==216))"
        mgr.cutsDict["SR4c"] = "(" + mgr.cutsDict["SR4c"] + " && (L2finalState==-1 || L2finalState==201 || L2finalState==216))"
        print "\t\t*** Setting Limits for LH Slepton case Only ***"
    elif slepNumber == 2: # RH slepton case
        mgr.cutsDict["SR4a"] = "(" + mgr.cutsDict["SR4a"] + " && (L2finalState==-1 || L2finalState==202 || L2finalState==217))"
        mgr.cutsDict["SR4b"] = "(" + mgr.cutsDict["SR4b"] + " && (L2finalState==-1 || L2finalState==202 || L2finalState==217))"
        mgr.cutsDict["SR4c"] = "(" + mgr.cutsDict["SR4c"] + " && (L2finalState==-1 || L2finalState==202 || L2finalState==217))"
        print "\t\t*** Setting Limits for LH Slepton case Only ***"
        
    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
    #                 Specify SR-Zjets               #
    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
    
    mgr.cutsDict["SR5a"] = "((isElEl || isMuMu) && isOS && lept1Pt>35000. && lept2Pt>20000. && nCentralLightJets>1 && nForwardJets==0 && metrel>80000. && mll>81187.6 && mll<101187.6 && pTll>80000. && L2dRLL>0.3 && L2dRLL<1.5 && nCentralBJets==0 && L2mJJ>50000 && L2mJJ<100000 && jet1Pt>45000 && jet2Pt>45000)"


    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
    #            Specify Super0 -- DANTRIM           #
    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
    ## Super0a  
#    mgr.cutsDict["Super0a"] =  "(isOS && lept1Pt>35000. && lept2Pt>20000. && nCentralLightJets==0 && nCentralBJets==0 && nForwardJets==0 && mDeltaR>45000.)"
    ## Super0b  REMOVED SR0a -- Super0b --> Super0a
    mgr.cutsDict["Super0a"] =  "(isOS && lept1Pt>35000. && lept2Pt>20000. && nCentralLightJets==0 && nCentralBJets==0 && nForwardJets==0 && mDeltaR>90000.)"
    ## Super0c
    mgr.cutsDict["Super0b"] =  "(isOS && lept1Pt>35000. && lept2Pt>20000. && nCentralLightJets==0 && nCentralBJets==0 && nForwardJets==0 && mDeltaR>120000.)"
    ## Super0d
    mgr.cutsDict["Super0c"] =  "(isOS && lept1Pt>35000. && lept2Pt>20000. && nCentralLightJets==0 && nCentralBJets==0 && nForwardJets==0 && mDeltaR>150000.)"
    
    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
    #            Specify Super1 -- DANTRIM           #
    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

    ## Super1a
    mgr.cutsDict["Super1a"] =  "(isOS && jet1Pt>80000. && nCentralLightJets==1 && nCentralBJets==0 && nForwardJets==0 && mDeltaR>20000.)" 
    ## Super1b
    mgr.cutsDict["Super1b"] =  "(isOS && jet1Pt>80000. && nCentralLightJets==1 && nCentralBJets==0 && nForwardJets==0 && mDeltaR>50000.)" 
    #### Super1c
    ##mgr.cutsDict["Super1c"] =  "(isOS && jet1Pt>80000. && nCentralLightJets==1 && nCentralBJets==0 && nForwardJets==0 && mDeltaR>90000.)" 

    ## Super1c -- Updated OCT 22
    mgr.cutsDict["Super1c"] =  "(isOS && nCentralLightJets==1 && nCentralBJets==0 && nForwardJets==0 && mDeltaR>20000.)" 

    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
    #                 Specify CR-WW                  #
    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

    ## CRWWMet
    mgr.cutsDict["W2CRmet"] = "(isOS && nCentralLightJets==0 && nCentralBJets==0 && nForwardJets==0 && lept1Pt>35000. && lept2Pt>20000. && metrel<80000. && metrel>60000. && pTll>40000 && mll<120000 && isElMu )"
    ## CRWWmT2
    mgr.cutsDict["W2CRmt2"] = "(isOS && nCentralLightJets==0 && nCentralBJets==0 && nForwardJets==0 && lept1Pt>35000. && lept2Pt>20000. && MT2<90000.  && MT2>50000. && isElMu)"

    ## CRWW14a -- DANTRIM
    mgr.cutsDict["CRWW14a"] = "(isOS && nCentralLightJets==0 && nCentralBJets==0 && nForwardJets==0 && mDeltaR<70000. && pTll>40000. && lept1Pt>35000. && lept2Pt>20000. && isElMu)"
    ## CRWW14b -- DANTRIM
    mgr.cutsDict["CRWW14b"] = "(isOS && nCentralLightJets==1 && nCentralBJets==0 && nForwardJets==0 && mDeltaR>20000. && pTll>70000. && dphi_ll_vBetaT<2.0 && isElMu)"
     


    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
    #                 Specify CR-Top                 #
    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

    ## CRTopMet
    mgr.cutsDict["TopCRmet"] = "(isOS && nCentralBJets>=1 && nCentralLightJets==0 && nForwardJets==0 && lept1Pt>35000. && lept2Pt>20000. && metrel>80000. && pTll>80000.  && mll<120000. && isElMu )"
    ## CRTopmT2
    mgr.cutsDict["TopCRmt2"]= "(isOS && nCentralBJets>=1 && nCentralLightJets==0 && nForwardJets==0 && lept1Pt>35000. && lept2Pt>20000. && MT2>70000. && isElMu)"
    ## CRTopZjets
    mgr.cutsDict["TopCRZjets"] = "((isElEl || isMuMu) && isOS && lept1Pt>35000. && lept2Pt>20000. && nForwardJets==0 && nCentralBJets>0 && metrel>80000. && !(mll>81187.6 && mll<101187.6) && pTll>80000. && L2dRLL>0.3 && L2dRLL<1.5)"

    ## CRTop14a -- DANTRIM
    mgr.cutsDict["CRTop14a"] = "(isOS && isElMu && nCentralBJets>=1 && nForwardJets==0 && nCentralLightJets==0 && mDeltaR>20000. && pTll>20000.)"

    ## CRTop14b -- DANTRIM
    mgr.cutsDict["CRTop14b"] = "(isOS && isElMu && nCentralBJets>=1 && nForwardJets==0 && nCentralLightJets==1 && mDeltaR>20000. && jet1Pt>80000.)"


    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
    #                 Specify CR-ZV                  #
    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

    ##
    ## Control regions for ZV
    ##

    ## CRZVMet
    mgr.cutsDict["ZVCRmet"] = "(isOS && nCentralLightJets==0 && nCentralBJets==0 && nForwardJets==0 && lept1Pt>35000. && lept2Pt>20000. && metrel>80000. && pTll>80000. && (mll>81187.6 && mll<101187.6))"
    ## CRZVmT2a
    mgr.cutsDict["ZVCRmt2a"]= "(isOS && nCentralLightJets==0 && nCentralBJets==0 && nForwardJets==0 && lept1Pt>35000. && lept2Pt>20000. && MT2>90000. && (mll>81187.6 && mll<101187.6) )"
    ## CRZVmT2b
    mgr.cutsDict["ZVCRmt2b"]= "(isOS && nCentralLightJets==0 && nCentralBJets==0 && nForwardJets==0 && lept1Pt>35000. && lept2Pt>20000. && MT2>100000. && (mll>81187.6 && mll<101187.6) )"
    ## CRZVmT2c
    mgr.cutsDict["ZVCRmt2c"]= "(isOS && nCentralLightJets==0 && nCentralBJets==0 && nForwardJets==0 && lept1Pt>35000. && lept2Pt>20000. && MT2>120000. && (mll>81187.6 && mll<101187.6) )"
    ## CRZVmT2d
    mgr.cutsDict["ZVCRmt2d"]= "(isOS && nCentralLightJets==0 && nCentralBJets==0 && nForwardJets==0 && lept1Pt>35000. && lept2Pt>20000. && MT2>150000. && (mll>81187.6 && mll<101187.6) )"
    ## CRZVZjets
    mgr.cutsDict["ZVCRZjets"]= "(isOS && nCentralLightJets==0 && nCentralBJets==0 && nForwardJets==0 && lept1Pt>35000. && lept2Pt>20000. && (mll>81187.6 && mll<101187.6))"

    ## CRZV14a -- DANTRIM
    mgr.cutsDict["CRZV14a"]  = "((isElEl || isMuMu) && isOS && nCentralBJets==0 && nForwardJets==0 && nCentralLightJets==0 && (mll>81187.6 && mll<101187.6) && mDeltaR>70000. && pTll>40000.)"
    
    ## CRZV14b -- DANTRIM
    mgr.cutsDict["CRZV14b"]  = "((isElEl || isMuMu) && isOS && nCentralBJets==0 && nForwardJets==0 && nCentralLightJets==1 && (mll>81187.6 && mll<101187.6) && mDeltaR>20000. && pTll>70000. && dphi_ll_vBetaT>2.0)"


    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
    #      Add on individual channels for SRs        #
    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

    ###
    ### Now Add all the single channel signal regions
    ###

    #
    ## EE CASE ##
    #
    # Signal Regions
    mgr.cutsDict["eeSR1"]        ="("+str( mgr.cutsDict["SR1"])        +" && isElEl && !(mll>81187.6 && mll<101187.6))"	
    mgr.cutsDict["eeSR2a"]       ="("+str( mgr.cutsDict["SR2a"])       +" && isElEl && !(mll>81187.6 && mll<101187.6))"	
    mgr.cutsDict["eeSR2b"]       ="("+str( mgr.cutsDict["SR2b"])       +" && isElEl && !(mll>81187.6 && mll<101187.6))"	
    mgr.cutsDict["eeSR4a"]       ="("+str( mgr.cutsDict["SR4a"])       +" && isElEl && !(mll>81187.6 && mll<101187.6))"	
    mgr.cutsDict["eeSR4b"]       ="("+str( mgr.cutsDict["SR4b"])       +" && isElEl && !(mll>81187.6 && mll<101187.6))"	
    mgr.cutsDict["eeSR4c"]       ="("+str( mgr.cutsDict["SR4c"])       +" && isElEl && !(mll>81187.6 && mll<101187.6))"
    mgr.cutsDict["eeSR5a"]       ="("+str( mgr.cutsDict["SR5a"])       +" && isElEl )"
#    mgr.cutsDict["eeSuper0a"]    ="("+str( mgr.cutsDict["Super0a"])    +" && isElEl && !(mll>81187.6 && mll<101187.6))"
    mgr.cutsDict["eeSuper0a"]    ="("+str( mgr.cutsDict["Super0a"])    +" && isElEl && !(mll>81187.6 && mll<101187.6))"
    mgr.cutsDict["sfSuper0a"]    ="("+str( mgr.cutsDict["Super0a"])    +" && (isElEl || isMuMu) && !(mll>81187.6 && mll<101187.6))"
    mgr.cutsDict["eeSuper0b"]    ="("+str( mgr.cutsDict["Super0b"])    +" && isElEl && !(mll>81187.6 && mll<101187.6))"
    mgr.cutsDict["sfSuper0b"]    ="("+str( mgr.cutsDict["Super0b"])    +" && (isElEl || isMuMu) && !(mll>81187.6 && mll<101187.6))"
    mgr.cutsDict["eeSuper0c"]    ="("+str( mgr.cutsDict["Super0c"])    +" && isElEl && !(mll>81187.6 && mll<101187.6))"
    mgr.cutsDict["sfSuper0c"]    ="("+str( mgr.cutsDict["Super0c"])    +" && (isElEl || isMuMu) && !(mll>81187.6 && mll<101187.6))"
    mgr.cutsDict["eeSuper1a"]    ="("+str( mgr.cutsDict["Super1a"])    +" && dphi_ll_vBetaT>2.0 && R2>0.5 && isElEl && !(mll>81187.6 && mll<101187.6))"
    mgr.cutsDict["sfSuper1a"]    ="("+str( mgr.cutsDict["Super1a"])    +" && dphi_ll_vBetaT>2.0 && R2>0.5 && (isElEl || isMuMu) && !(mll>81187.6 && mll<101187.6))"
    mgr.cutsDict["eeSuper1b"]    ="("+str( mgr.cutsDict["Super1b"])    +" && dphi_ll_vBetaT>2.0 && R2>0.5 && isElEl && !(mll>81187.6 && mll<101187.6))"
    mgr.cutsDict["sfSuper1b"]    ="("+str( mgr.cutsDict["Super1b"])    +" && dphi_ll_vBetaT>2.0 && R2>0.5 && (isElEl || isMuMu) && !(mll>81187.6 && mll<101187.6))"
    mgr.cutsDict["eeSuper1c"]    ="("+str( mgr.cutsDict["Super1c"])    +" && jet1Pt>60000. && pTll<40000. && dphi_ll_vBetaT>2.0 && R2>0.65 && isElEl && !(mll>81187.6 && mll<101187.6))"
    mgr.cutsDict["sfSuper1c"]    ="("+str( mgr.cutsDict["Super1c"])    +" && jet1Pt>60000. && pTll<40000. && dphi_ll_vBetaT>2.0 && R2>0.65 && (isElEl || isMuMu) && !(mll>81187.6 && mll<101187.6))"
    # WW Control Regions => em only
    mgr.cutsDict["eeW2CRmet"]    ="("+str( mgr.cutsDict["W2CRmet"])    +")"
    mgr.cutsDict["eeW2CRmt2"]    ="("+str( mgr.cutsDict["W2CRmt2"])    +")"
    mgr.cutsDict["eeTopCRmet"]   ="("+str( mgr.cutsDict["TopCRmet"])   +")"	
    mgr.cutsDict["eeCRWW14a"]    ="("+str( mgr.cutsDict["CRWW14a"])    +")"
    mgr.cutsDict["eeCRWW14b"]    ="("+str( mgr.cutsDict["CRWW14b"])    +")"
    # Top Control Regions => em only
    mgr.cutsDict["eeTopCRmt2"]   ="("+str( mgr.cutsDict["TopCRmt2"])   +")"		
    mgr.cutsDict["eeTopCRZjets"] ="("+str( mgr.cutsDict["TopCRZjets"]) +" && isElEl )"
    mgr.cutsDict["eeCRTop14a"]   ="("+str( mgr.cutsDict["CRTop14a"])   +")"
    mgr.cutsDict["eeCRTop14b"]   ="("+str( mgr.cutsDict["CRTop14b"])   +")"
    # ZV Control Regions => ee+mm
    mgr.cutsDict["eeZVCRmet"]    ="("+str( mgr.cutsDict["ZVCRmet"])    +" && (isElEl || isMuMu))"	
    mgr.cutsDict["eeZVCRmt2a"]   ="("+str( mgr.cutsDict["ZVCRmt2a"])   +" && (isElEl || isMuMu))"	
    mgr.cutsDict["eeZVCRmt2b"]   ="("+str( mgr.cutsDict["ZVCRmt2b"])   +" && (isElEl || isMuMu))"
    mgr.cutsDict["eeZVCRmt2c"]   ="("+str( mgr.cutsDict["ZVCRmt2c"])   +" && (isElEl || isMuMu))"
    mgr.cutsDict["eeZVCRmt2d"]   ="("+str( mgr.cutsDict["ZVCRmt2d"])   +" && (isElEl || isMuMu))"
    ##mgr.cutsDict["eeZVCRmet"]  ="("+str( mgr.cutsDict["ZVCRmet"])    +" && isElEl)"	
    ##mgr.cutsDict["eeZVCRmt2a"] ="("+str( mgr.cutsDict["ZVCRmt2a"])   +" && isElEl)"	
    ##mgr.cutsDict["eeZVCRmt2b"] ="("+str( mgr.cutsDict["ZVCRmt2b"])   +" && isElEl)"
    ##mgr.cutsDict["eeZVCRmt2c"] ="("+str( mgr.cutsDict["ZVCRmt2c"])   +" && isElEl)"
    ##mgr.cutsDict["eeZVCRmt2d"] ="("+str( mgr.cutsDict["ZVCRmt2d"])   +" && isElEl)"
    mgr.cutsDict["eeZVCRZjets"]  ="("+str( mgr.cutsDict["ZVCRZjets"])  +" && isElEl)"
    mgr.cutsDict["eeCRZV14a"]    ="("+str( mgr.cutsDict["CRZV14a"])    +")"
    mgr.cutsDict["eeCRZV14b"]    ="("+str( mgr.cutsDict["CRZV14b"])    +")"
    #
    ## MUMU CASE ##
    #
    # Signal Regions
    mgr.cutsDict["mmSR1"]        ="("+str( mgr.cutsDict["SR1"])        +" && isMuMu && !(mll>81187.6 && mll<101187.6))"	
    mgr.cutsDict["mmSR2a"]       ="("+str( mgr.cutsDict["SR2a"])       +" && isMuMu && !(mll>81187.6 && mll<101187.6))"	
    mgr.cutsDict["mmSR2b"]       ="("+str( mgr.cutsDict["SR2b"])       +" && isMuMu && !(mll>81187.6 && mll<101187.6))"	
    mgr.cutsDict["mmSR4a"]       ="("+str( mgr.cutsDict["SR4a"])       +" && isMuMu && !(mll>81187.6 && mll<101187.6))"	
    mgr.cutsDict["mmSR4b"]       ="("+str( mgr.cutsDict["SR4b"])       +" && isMuMu && !(mll>81187.6 && mll<101187.6))"
    mgr.cutsDict["mmSR4c"]       ="("+str( mgr.cutsDict["SR4c"])       +" && isMuMu && !(mll>81187.6 && mll<101187.6))"
    mgr.cutsDict["mmSR5a"]       ="("+str( mgr.cutsDict["SR5a"])       +" && isMuMu) "
#    mgr.cutsDict["mmSuper0a"]    ="("+str( mgr.cutsDict["Super0a"])    +" && isMuMu && !(mll>81187.6 && mll<101187.6))"
    mgr.cutsDict["mmSuper0a"]    ="("+str( mgr.cutsDict["Super0a"])    +" && isMuMu && !(mll>81187.6 && mll<101187.6))"
    mgr.cutsDict["mmSuper0b"]    ="("+str( mgr.cutsDict["Super0b"])    +" && isMuMu && !(mll>81187.6 && mll<101187.6))"
    mgr.cutsDict["mmSuper0c"]    ="("+str( mgr.cutsDict["Super0c"])    +" && isMuMu && !(mll>81187.6 && mll<101187.6))"
    mgr.cutsDict["mmSuper1a"]    ="("+str( mgr.cutsDict["Super1a"])    +" && dphi_ll_vBetaT>2.0 && R2>0.5 && isMuMu && !(mll>81187.6 && mll<101187.6))"
    mgr.cutsDict["mmSuper1b"]    ="("+str( mgr.cutsDict["Super1b"])    +" && dphi_ll_vBetaT>2.0 && R2>0.5 && isMuMu && !(mll>81187.6 && mll<101187.6))"
   # mgr.cutsDict["mmSuper1c"]    ="("+str( mgr.cutsDict["Super1c"])    +" && dphi_ll_vBetaT>2.0 && R2>0.5 && isMuMu && !(mll>81187.6 && mll<101187.6))"
    mgr.cutsDict["mmSuper1c"]    ="("+str( mgr.cutsDict["Super1c"])    +" && jet1Pt>60000. && pTll<40000. && dphi_ll_vBetaT>2.0 && R2>0.65 && isMuMu && !(mll>81187.6 && mll<101187.6))"
    # WW Control Regions => em only
    mgr.cutsDict["mmW2CRmet"]    ="("+str( mgr.cutsDict["W2CRmet"])    +")"
    mgr.cutsDict["mmW2CRmt2"]    ="("+str( mgr.cutsDict["W2CRmt2"])    +")"
    mgr.cutsDict["mmTopCRmet"]   ="("+str( mgr.cutsDict["TopCRmet"])   +")"	
    mgr.cutsDict["mmCRWW14a"]   ="("+str( mgr.cutsDict["CRWW14a"])   +")"
    mgr.cutsDict["mmCRWW14b"]   ="("+str( mgr.cutsDict["CRWW14b"])   +")"
    # Top Control Regions => em only
    mgr.cutsDict["mmTopCRmt2"]   ="("+str( mgr.cutsDict["TopCRmt2"])   +")"	
    mgr.cutsDict["mmTopCRZjets"] ="("+str( mgr.cutsDict["TopCRZjets"]) +" && isMuMu)"
    mgr.cutsDict["mmCRTop14a"]   ="("+str( mgr.cutsDict["CRTop14a"])   +")"
    mgr.cutsDict["mmCRTop14b"]   ="("+str( mgr.cutsDict["CRTop14b"])   +")"
    # ZV Control Regions => ee+mm
    mgr.cutsDict["mmZVCRmet"]    ="("+str( mgr.cutsDict["ZVCRmet"])    +" && (isElEl || isMuMu))"	
    mgr.cutsDict["mmZVCRmt2a"]   ="("+str( mgr.cutsDict["ZVCRmt2a"])   +" && (isElEl || isMuMu))"	
    mgr.cutsDict["mmZVCRmt2b"]   ="("+str( mgr.cutsDict["ZVCRmt2b"])   +" && (isElEl || isMuMu))"
    mgr.cutsDict["mmZVCRmt2c"]   ="("+str( mgr.cutsDict["ZVCRmt2c"])   +" && (isElEl || isMuMu))"
    mgr.cutsDict["mmZVCRmt2d"]   ="("+str( mgr.cutsDict["ZVCRmt2d"])   +" && (isElEl || isMuMu))"
    ##mgr.cutsDict["mmZVCRmet"]  ="("+str( mgr.cutsDict["ZVCRmet"])    +" && isMuMu)"	
    ##mgr.cutsDict["mmZVCRmt2a"] ="("+str( mgr.cutsDict["ZVCRmt2a"])   +" && isMuMu)"
    ##mgr.cutsDict["mmZVCRmt2b"] ="("+str( mgr.cutsDict["ZVCRmt2b"])   +" && isMuMu)"
    ##mgr.cutsDict["mmZVCRmt2c"] ="("+str( mgr.cutsDict["ZVCRmt2c"])   +" && isMuMu)"
    ##mgr.cutsDict["mmZVCRmt2d"] ="("+str( mgr.cutsDict["ZVCRmt2d"])   +" && isMuMu)"
    mgr.cutsDict["mmZVCRZjets"]  ="("+str( mgr.cutsDict["ZVCRZjets"])  +" && isMuMu)"
    mgr.cutsDict["mmCRZV14a"]    ="("+str( mgr.cutsDict["CRZV14a"])    +")"
    mgr.cutsDict["mmCRZV14b"]    ="("+str( mgr.cutsDict["CRZV14b"])    +")"
    #
    ## EMU CASE
    #
    # Signal Regions
    mgr.cutsDict["emSR1"]        ="("+str( mgr.cutsDict["SR1"])        +" && isElMu)"	
    mgr.cutsDict["emSR2a"]       ="("+str( mgr.cutsDict["SR2a"])       +" && isElMu)"	
    mgr.cutsDict["emSR2b"]       ="("+str( mgr.cutsDict["SR2b"])       +" && isElMu)"	
    mgr.cutsDict["emSR4a"]       ="("+str( mgr.cutsDict["SR4a"])       +" && isElMu)"	
    mgr.cutsDict["emSR4b"]       ="("+str( mgr.cutsDict["SR4b"])       +" && isElMu)"	
    mgr.cutsDict["emSR4c"]       ="("+str( mgr.cutsDict["SR4c"])       +" && isElMu)"
#    mgr.cutsDict["emSuper0a"]    ="("+str( mgr.cutsDict["Super0a"])    +" && isElMu)"
    mgr.cutsDict["emSuper0a"]    ="("+str( mgr.cutsDict["Super0a"])    +" && isElMu)"
    mgr.cutsDict["emSuper0b"]    ="("+str( mgr.cutsDict["Super0b"])    +" && isElMu)"
    mgr.cutsDict["emSuper0c"]    ="("+str( mgr.cutsDict["Super0c"])    +" && isElMu)"
    mgr.cutsDict["emSuper1a"]    ="("+str( mgr.cutsDict["Super1a"])    +" && dphi_ll_vBetaT>2.5 && R2>0.7 && isElMu)"
    mgr.cutsDict["emSuper1b"]    ="("+str( mgr.cutsDict["Super1b"])    +" && dphi_ll_vBetaT>2.5 && R2>0.7 && isElMu)"
    mgr.cutsDict["emSuper1c"]    ="("+str( mgr.cutsDict["Super1c"])    +" && jet1Pt>80000. && pTll<50000. && dphi_ll_vBetaT>2.5 && R2>0.75 && isElMu)"
    # WW Control Regions => em only
    mgr.cutsDict["emW2CRmet"]    ="("+str( mgr.cutsDict["W2CRmet"])    +" && isElMu)"
    mgr.cutsDict["emW2CRmt2"]    ="("+str( mgr.cutsDict["W2CRmt2"])    +" && isElMu)"
    mgr.cutsDict["emCRWW14a"]    ="("+str( mgr.cutsDict["CRWW14a"])    +")"
    mgr.cutsDict["emCRWW14b"]    ="("+str( mgr.cutsDict["CRWW14b"])    +")"
    # Top Control Regions => em only
    mgr.cutsDict["emTopCRmet"]   ="("+str( mgr.cutsDict["TopCRmet"])   +" && isElMu)"	
    mgr.cutsDict["emTopCRmt2"]   ="("+str( mgr.cutsDict["TopCRmt2"])   +" && isElMu)"
    mgr.cutsDict["emCRTop14a"]   ="("+str( mgr.cutsDict["CRTop14a"])   +")"
    mgr.cutsDict["emCRTop14b"]   ="("+str( mgr.cutsDict["CRTop14b"])   +")"
    # ZV Control Regions => ee+mm
    mgr.cutsDict["emZVCRmet"]    ="("+str( mgr.cutsDict["ZVCRmet"])    +" && (isElEl || isMuMu))"	
    mgr.cutsDict["emZVCRmt2a"]   ="("+str( mgr.cutsDict["ZVCRmt2a"])   +" && (isElEl || isMuMu))"	
    mgr.cutsDict["emZVCRmt2b"]   ="("+str( mgr.cutsDict["ZVCRmt2b"])   +" && (isElEl || isMuMu))"
    mgr.cutsDict["emZVCRmt2c"]   ="("+str( mgr.cutsDict["ZVCRmt2c"])   +" && (isElEl || isMuMu))"
    mgr.cutsDict["emZVCRmt2d"]   ="("+str( mgr.cutsDict["ZVCRmt2d"])   +" && (isElEl || isMuMu))"
    mgr.cutsDict["emCRZV14a"]    ="("+str( mgr.cutsDict["CRZV14a"])    +")"
    mgr.cutsDict["emCRZV14b"]    ="("+str( mgr.cutsDict["CRZV14b"])    +")"

    #
    ## Total Case
    #
    mgr.cutsDict["totSR4a"]       ="("+str( mgr.cutsDict["SR4a"])       +" && (((isElEl||isMuMu) && !(mll>81187.6 && mll<101187.6)) || isElMu))"
    mgr.cutsDict["totSR4b"]       ="("+str( mgr.cutsDict["SR4b"])       +" && (((isElEl||isMuMu) && !(mll>81187.6 && mll<101187.6)) || isElMu))"
    mgr.cutsDict["totSR4c"]       ="("+str( mgr.cutsDict["SR4c"])       +" && (((isElEl||isMuMu) && !(mll>81187.6 && mll<101187.6)) || isElMu))" 
#    mgr.cutsDict["totSuper0a"]    ="("+str( mgr.cutsDict["Super0a"])    +" && (((isElEl||isMuMu) && !(mll>81187.6 && mll<101187.6)) || isElMu))"
    mgr.cutsDict["totSuper0a"]    ="("+str( mgr.cutsDict["Super0a"])    +" && (((isElEl||isMuMu) && !(mll>81187.6 && mll<101187.6)) || isElMu))"
    mgr.cutsDict["totSuper0b"]    ="("+str( mgr.cutsDict["Super0b"])    +" && (((isElEl||isMuMu) && !(mll>81187.6 && mll<101187.6)) || isElMu))"
    mgr.cutsDict["totSuper0c"]    ="("+str( mgr.cutsDict["Super0c"])    +" && (((isElEl||isMuMu) && !(mll>81187.6 && mll<101187.6)) || isElMu))"
    mgr.cutsDict["totSuper1a"]    ="("+str( mgr.cutsDict["Super1a"])    +" && (((isElEl||isMuMu) && !(mll>81187.6 && mll<101187.6) && dphi_ll_vBetaT>2.0 && R2>0.5) || (dphi_ll_vBetaT>2.5 && R2>0.7 && isElMu)))"
    mgr.cutsDict["totSuper1b"]    ="("+str( mgr.cutsDict["Super1b"])    +" && (((isElEl||isMuMu) && !(mll>81187.6 && mll<101187.6) && dphi_ll_vBetaT>2.0 && R2>0.5) || (dphi_ll_vBetaT>2.5 && R2>0.7 && isElMu))"
    mgr.cutsDict["totSuper1c"]    ="("+str( mgr.cutsDict["Super1c"])    +" && (((isElEl||isMuMu) && !(mll>81187.6 && mll<101187.6) && jet1Pt>60000. && dphi_ll_vBetaT>2.0 && R2>0.65 && pTll<40000.) || (jet1Pt>80000. && pTll<50000. && dphi_ll_vBetaT>2.5 && R2>0.75 && isElMu))"


    return mgr
