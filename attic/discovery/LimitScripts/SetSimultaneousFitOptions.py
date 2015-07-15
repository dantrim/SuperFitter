
############################################
# Realized that we just need a simple list #
# of the control region options which can  #
# easily be done in a module.              #
############################################

def getCRFitList(tlx, SR, lepChan, doSimFitWW, doSimFitTop, doSimFitZV, userDefs, sysObj):
    
    crList    = []
    CRcounter = 0
    
    # Define a useful method
    def addForFit(list, counter, chName,nbins,low,high):
        list.append( tlx.addChannel("cuts",[chName],nbins,low,high) )
        list[counter].useOverflowBin=True
        list[counter].useUnderflowBin=True
        return counter + 1
    
    # WW simultaneous fit
    # Use em for SRWW and SRmT2


    if doSimFitWW:
        if 'SR1' in SR:
            CRcounter = addForFit(crList, CRcounter,"emW2CRmet",1,0,1)
            #if lepChan==userDefs.all or lepChan==userDefs.ee :
            #    CRcounter = addForFit(crList, CRcounter,"eeW2CRmet",1,0,1)
            #if lepChan==userDefs.all or lepChan==userDefs.mm :
            #    CRcounter = addForFit(crList, CRcounter,"mmW2CRmet",1,0,1)
            #if lepChan==userDefs.all or lepChan==userDefs.em :
            #    CRcounter = addForFit(crList, CRcounter,"emW2CRmet",1,0,1)
        if 'SR2a' in SR or 'SR2b' in SR or 'SR4a' in SR or 'SR4b' in SR or 'SR4c' in SR:
            CRcounter = addForFit(crList, CRcounter,"emW2CRmt2",1,0,1)
            #if lepChan==userDefs.all or lepChan==userDefs.ee :
            #    CRcounter = addForFit(crList, CRcounter,"eeW2CRmt2",1,0,1)
            #if lepChan==userDefs.all or lepChan==userDefs.mm :
            #    CRcounter = addForFit(crList, CRcounter,"mmW2CRmt2",1,0,1)
            #if lepChan==userDefs.all or lepChan==userDefs.em :
            #    CRcounter = addForFit(crList, CRcounter,"emW2CRmt2",1,0,1)

        ## DANTRIM

#        if 'Super0a' in SR or 'Super0b' in SR or 'Super0c' in SR or 'Super0d' in SR:
        if 'Super0a' in SR or 'Super0b' in SR or 'Super0c' in SR:
            CRcounter = addForFit(crList, CRcounter, "emCRWW14a",1,0,1)
            crList[0].getSample("Fake").addSystematic( sysObj.emCRWW14a_FakeRelUnc )
        if 'Super1a' in SR or 'Super1b' in SR or 'Super1c' in SR:
            CRcounter = addForFit(crList, CRcounter, "emCRWW14b",1,0,1)
            crList[0].getSample("Fake").addSystematic( sysObj.emCRWW14b_FakeRelUnc )
            
            # add components of Top uncertainties 
            crList[0].getSample("Top").addSystematic( sysObj.CRWWb_TT_PS)
            crList[0].getSample("Top").addSystematic( sysObj.CRWWb_Top_Other)
       #     crList[0].getSample("Top").addSystematic( sysObj.CRWW_TT_GEN)
       #     crList[0].getSample("Top").addSystematic( sysObj.CRWW_TT_PS)
       #     crList[0].getSample("Top").addSystematic( sysObj.CRWW_TT_ISRFSR)
       #     crList[0].getSample("Top").addSystematic( sysObj.CRWW_TT_PDF)
       #     crList[0].getSample("Top").addSystematic( sysObj.CRWW_TT_QCD)
       #     crList[0].getSample("Top").addSystematic( sysObj.CRWW_ST_GEN)
       #     crList[0].getSample("Top").addSystematic( sysObj.CRWW_ST_PS)
       #     crList[0].getSample("Top").addSystematic( sysObj.CRWW_ST_DSDR)
       #     crList[0].getSample("Top").addSystematic( sysObj.CRWW_ST_ISRFSR)
       #     crList[0].getSample("Top").addSystematic( sysObj.CRWW_ST_PDF)
            

    
    # Top simultaneous fit
    # Use em for SRWW and SRmT2
    if doSimFitTop:
        if 'SR1' in SR:
            CRcounter = addForFit(crList, CRcounter,"emTopCRmet",1,0,1)
            #if lepChan==userDefs.all or lepChan==userDefs.ee :
            #    CRcounter = addForFit(crList, CRcounter,"eeTopCRmet",1,0,1)
            #if lepChan==userDefs.all or lepChan==userDefs.mm :
            #    CRcounter = addForFit(crList, CRcounter,"mmTopCRmet",1,0,1)
            #if lepChan==userDefs.all or lepChan==userDefs.em :
            #    CRcounter = addForFit(crList, CRcounter,"emTopCRmet",1,0,1)
        if 'SR2a' in SR or 'SR2b' in SR or 'SR4a' in SR or 'SR4b' in SR or 'SR4c' in SR:
            CRcounter = addForFit(crList, CRcounter,"emTopCRmt2",1,0,1)
            #if lepChan==userDefs.all or lepChan==userDefs.ee :
            #    CRcounter = addForFit(crList, CRcounter,"eeTopCRmt2",1,0,1)
            #if lepChan==userDefs.all or lepChan==userDefs.mm :
            #    CRcounter = addForFit(crList, CRcounter,"mmTopCRmt2",1,0,1)
            #if lepChan==userDefs.all or lepChan==userDefs.em :
            #    CRcounter = addForFit(crList, CRcounter,"emTopCRmt2",1,0,1)
        if 'SR5a' in SR:
            if lepChan==userDefs.all or lepChan==userDefs.ee or lepChan==userDefs.eemm :
                CRcounter = addForFit(crList, CRcounter,"eeTopCRZjets",1,0,1)
            if lepChan==userDefs.all or lepChan==userDefs.mm or lepChan==userDefs.eemm :
                CRcounter = addForFit(crList, CRcounter,"mmTopCRZjets",1,0,1)

        ## DANTRIM

        if 'Super0a' in SR or 'Super0b' in SR or 'Super0c' in SR:
            CRcounter = addForFit(crList, CRcounter, "emCRTop14a",1,0,1)
            crList[1].getSample("Fake").addSystematic( sysObj.emCRTop14a_FakeRelUnc )
        if 'Super1a' in SR or 'Super1b' in SR or 'Super1c' in SR:
            CRcounter = addForFit(crList, CRcounter, "emCRTop14b",1,0,1)
            crList[1].getSample("Fake").addSystematic( sysObj.emCRTop14b_FakeRelUnc )


    # ZV simultaneous fit
    # Update: For all mT2 signal regions we will fit in mT2a 02/08/2013
    # Update: For SRWW and SRmT2 we fit in em now
    if doSimFitZV:
        if 'SR1' in SR:
            CRcounter = addForFit(crList, CRcounter,"emZVCRmet",1,0,1)
            #if lepChan==userDefs.all or lepChan==userDefs.ee :
            #    CRcounter = addForFit(crList, CRcounter,"eeZVCRmet",1,0,1)
            #if lepChan==userDefs.all or lepChan==userDefs.mm :
            #    CRcounter = addForFit(crList, CRcounter,"mmZVCRmet",1,0,1)
            #if lepChan==userDefs.all or lepChan==userDefs.em :
            #    CRcounter = addForFit(crList, CRcounter,"emZVCRmet",1,0,1)
        if 'SR2a' in SR or 'SR2b' in SR or 'SR4a' in SR or 'SR4b' in SR or 'SR4c' in SR:
            CRcounter = addForFit(crList, CRcounter,"emZVCRmt2a",1,0,1)
            #if lepChan==userDefs.all or lepChan==userDefs.ee :
            #    CRcounter = addForFit(crList, CRcounter,"eeZVCRmt2a",1,0,1)
            #if lepChan==userDefs.all or lepChan==userDefs.mm :
            #    CRcounter = addForFit(crList, CRcounter,"mmZVCRmt2a",1,0,1)
            #if lepChan==userDefs.all or lepChan==userDefs.em :
            #    CRcounter = addForFit(crList, CRcounter,"emZVCRmt2a",1,0,1)
        #if 'SR2b' in SR:
        #    if lepChan==userDefs.all or lepChan==userDefs.ee :
        #        CRcounter = addForFit(crList, CRcounter,"eeZVCRmt2b",1,0,1)
        #    if lepChan==userDefs.all or lepChan==userDefs.mm :
        #        CRcounter = addForFit(crList, CRcounter,"mmZVCRmt2b",1,0,1)
        #    if lepChan==userDefs.all or lepChan==userDefs.em :
        #        CRcounter = addForFit(crList, CRcounter,"emZVCRmt2b",1,0,1)
        #if 'SR4b' in SR:
        #    if lepChan==userDefs.all or lepChan==userDefs.ee :
        #        CRcounter = addForFit(crList, CRcounter,"eeZVCRmt2c",1,0,1)                
        #    if lepChan==userDefs.all or lepChan==userDefs.mm :
        #        CRcounter = addForFit(crList, CRcounter,"mmZVCRmt2c",1,0,1)
        #    if lepChan==userDefs.all or lepChan==userDefs.em :
        #        CRcounter = addForFit(crList, CRcounter,"emZVCRmt2c",1,0,1)
        #if 'SR4c' in SR:
        #    if lepChan==userDefs.all or lepChan==userDefs.ee :
        #        CRcounter = addForFit(crList, CRcounter,"eeZVCRmt2d",1,0,1)
        #    if lepChan==userDefs.all or lepChan==userDefs.mm :
        #        CRcounter = addForFit(crList, CRcounter,"mmZVCRmt2d",1,0,1)
        #    if lepChan==userDefs.all or lepChan==userDefs.em :
        #        CRcounter = addForFit(crList, CRcounter,"emZVCRmt2d",1,0,1)
        if 'SR5a' in SR:
            if lepChan==userDefs.all or lepChan==userDefs.ee or lepChan==userDefs.eemm :
                CRcounter = addForFit(crList, CRcounter,"eeZVCRZjets",1,0,1)
            if lepChan==userDefs.all or lepChan==userDefs.mm :
                CRcounter = addForFit(crList, CRcounter,"mmZVCRZjets",1,0,1)

        ## DANTRIM
        if 'Super0a' in SR or 'Super0b' in SR or 'Super0c' in SR:
            CRcounter = addForFit(crList, CRcounter,"emCRZV14a",1,0,1)
            crList[2].getSample("Fake").addSystematic( sysObj.emCRZV14a_FakeRelUnc )
        if 'Super1a' in SR or 'Super1b' in SR or 'Super1c' in SR:
            CRcounter = addForFit(crList, CRcounter,"emCRZV14b",1,0,1)
            crList[2].getSample("Fake").addSystematic( sysObj.emCRZV14b_FakeRelUnc )
 #       if 'Super0a' in SR or 'Super0b' in SR or 'Super0c' in SR:
 #           CRcounter = addForFit(crList, CRcounter,"emCRZV14a",1,0,1)
 #       if 'Super1a' in SR or 'Super1b' in SR or 'Super1c' in SR:
 #           CRcounter = addForFit(crList, CRcounter,"emCRZV14b",1,0,1)


    # Now return the control list
    return crList

