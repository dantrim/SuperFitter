#!/usr/bin python

###########################################
class RegionContainer :
    """
    Container class for all regions
    """
    def __init__(self) :
        self.regionList = []

    def Add(self, name_="", tcut_="") :
        x = Region(name_)
        x.setCut(tcut_)
        self.regionList.append(x)

    def getDict(self) :
        cut_dict = {}
        for reg in self.regionList :
            cut_dict[reg.name] = "(" + reg.tcut + ")"
        return cut_dict

    def Print(self) :
        for r in self.regionList :
            r.Print()

###########################################
class Region :
    """
    Simple class to hold the name of the
    region and the selection.

    The name will be what goes into the
    workspace creation"
    """
    def __init__(self, name_ = "") :
        self.name = name_
        self.tcut = ""

    def setCut(self, tcut_ = "") :
        self.tcut = tcut_
    def name(self) :
        return self.name
    def getCut(self) :
        return self.tcut
    def Print(self) :
        print "Region  name: %s    tcut: %s"%(self.name, self.tcut)

###########################################

#########################################################################################
## BUILD THE SELECTIONS HERE                                                           ##
#########################################################################################
def buildRegions() :
    """
    This is where you should define the different
    signal/control/validation regions for the
    analyses
    """
    rc = RegionContainer()
    # ------------------------------------------------------ #
    #  Stop-2L WW-like regions
    # ------------------------------------------------------ #
    isDF = "nLeptons==2 && nMuons==1 && nElectrons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20"
    isEE = "nLeptons==2 && nElectrons==2 && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20 && abs(mll-91.2)>10."
    isMM = "nLeptons==2 && nMuons==2     && (l_q[0]*l_q[1])<0 && l_pt[0]>25 && l_pt[1]>20 && abs(mll-91.2)>10."
    #isSF = "nLeptons==2 && (nElectrons==2 || nMuons==2) && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && abs(mll-91.2)>10"
    isSF = "(nLeptons==2 && ( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20)) && abs(mll-91.2)>10 && (l_q[0]*l_q[1])<0)"
    isDFOS = "nLeptons==2 && nElectrons==1 && nMuons==1 && l_pt[0]>25 && l_pt[1]>20 && (l_q[0]*l_q[1])<0"
    isSFOS = "(( (nMuons==2 && l_pt[0]>25 && l_pt[1]>20) || (nElectrons==2 && l_pt[0]>25 && l_pt[1]>20)) && abs(mll-91.2)>10 && (l_q[0]*l_q[1])<0)"
    trigger = "((year==2015 && trig_pass2015==1) || (year==2016 && trig_pass2016update==1))"

    ###################################
    ##### signal regions
    ###################################

    ## m_W sr
    sr_w_def = "nBJets==0 && RPT>0.7 && gamInvRp1>0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && MDR>95 && mll>20 && " + trigger # Moriond 2017 
    #sr_w_def = "nBJets==0 && RPT>0.65 && gamInvRp1>0.75 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && MDR>95 && mll>20 && " + trigger # 2016 EYOJamboree
    rc.Add("SRw_DF", isDF + " && " + sr_w_def)
    rc.Add("SRw_EE", isEE + " && " + sr_w_def)
    rc.Add("SRw_MM", isMM + " && " + sr_w_def)
    rc.Add("SRw_SF", isSF + " && " + sr_w_def)

    ### m_T sr
    sr_t_def = "nBJets>0 && RPT>0.7 && gamInvRp1>0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && MDR>110 && mll>20 && " + trigger # Moriond 2017 
    #sr_t_def = "nBJets>0 && RPT>0.65 && gamInvRp1>0.75 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && MDR>110 && mll>20 && " + trigger # 2016 EYOJamer
    rc.Add("SRt_DF", isDF + " && " + sr_t_def)
    rc.Add("SRt_EE", isEE + " && " + sr_t_def)
    rc.Add("SRt_MM", isMM + " && " + sr_t_def)
    rc.Add("SRt_SF", isSF + " && " + sr_t_def)

    ######################################
    ###### Top CR/VR
    ######################################
    crt_def = isDF + " && nBJets>0 && MDR>80 && RPT>0.7 && DPB_vSS<(0.9*abs(cosThetaB)+1.6) && mll>20 && " + trigger # Moriond 2017 
    #crt_def = isDF + " && nBJets>0 && MDR>80 && RPT>0.65 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && mll>20 && " + trigger # 2016 EYOJamboree
    rc.Add("CRTop", crt_def)

    vrt_def = isDF + " && nBJets==0 && MDR>80 && RPT<0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && mll>20 && " + trigger #Moriond 2017 
    #vrt_def = isDF + " && nBJets==0 && MDR>80 && RPT<0.65 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && mll>20 && " + trigger # 2016 EYOJamboree
    rc.Add("VRTop", vrt_def)

    ######################################
    #### Diboson CR/VR
    ######################################
    crvdf_def = isDF + " && nBJets==0 && MDR>50 && RPT<0.5 && gamInvRp1>0.7 && DPB_vSS<(0.9*abs(cosThetaB)+1.6) && mll>20 && " + trigger # Moriond 2017
    #crvdf_def = isDF + " && nBJets==0 && MDR>30 && RPT<0.5 && gamInvRp1>0.75 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && mll>20 && " + trigger # 2016 EYOJamboree
    rc.Add("CRVVDF", crvdf_def)

    crvsf_def = isSF + " && nBJets==0 && MDR>70 && RPT<0.5 && gamInvRp1>0.7 && DPB_vSS<(0.9*abs(cosThetaB)+1.6) && mll>20 && " + trigger # Moriond 2017
    #crvsf_def = isSF + " && nBJets==0 && MDR>30 && RPT<0.5 && gamInvRp1>0.75 && DPB_vSS<(0.85*abs(cosThetaB)+1.8) && mll>20 && met>80 && " + trigger # 2016 EYOJamboree
    rc.Add("CRVVSF", crvsf_def)

    vrvdf_def = isDF + " && nBJets==0 && MDR>50 && MDR<95 && RPT<0.7 && gamInvRp1>0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && mll>20 && " + trigger # Moriond 2017 
    #vrvdf_def = isDF + " && nBJets==0 && MDR>30 && MDR<80  && RPT<0.5 && gamInvRp1>0.75 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && mll>20 && " + trigger # 2016 EYOJamboree
    rc.Add("VRVVDF", vrvdf_def)

    vrvsf_def = isSF + " && nBJets==0 && MDR>60 && MDR<95 && RPT<0.4 && gamInvRp1>0.7 && DPB_vSS>(0.9*abs(cosThetaB)+1.6) && mll>20 && " + trigger # Moriond 2017 
    #vrvsf_def = isSF + " && nBJets==0 && MDR>30 && MDR<80  && RPT<0.5 && gamInvRp1>0.75 && DPB_vSS>(0.85*abs(cosThetaB)+1.8) && mll>20 && met>80 && " + trigger # 2016 EYOJamboree
    rc.Add("VRVVSF", vrvsf_def)


    return rc
