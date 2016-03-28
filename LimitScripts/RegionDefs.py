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
    isDF = "nLeptons==2 && nMuons==1 && nElectrons==1 && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20"
    isSF = "nLeptons==2 && (nElectrons==2 || nMuons==2) && (l_q[0]*l_q[1])<0 && l_pt[0]>20 && l_pt[1]>20 && abs(mll-91.2)>10"


    ###################################
    ##### signal regions
    ###################################
    sr_def = "nBJets==0 && MDR>95 && RPT>0.5 && gamInvRp1>0.8 && DPB_vSS>(0.8*abs(cosThetaB)+1.8)"
    rc.Add("SRDF", isDF + " && " + sr_def)
    rc.Add("SRSF", isSF + " && " + sr_def)

    ###################################
    ##### Top CR/VR
    ###################################
    rc.Add("CRTop", isDF + " && nBJets>0 && MDR>30 && RPT>0.5 && DPB_vSS<(0.8*abs(cosThetaB)+1.8)")
    rc.Add("VRTop", isDF + " && nSJets>0 && nBJets==0 && MDR>30 && RPT<0.5 && DPB_vSS>(0.8*abs(cosThetaB)+1.8)")

    ###################################
    ##### Diboson CR/VR
    ###################################
    rc.Add("CRVV", isDF + " && nSJets==0 && nBJets==0 && MDR>30 && RPT<0.5 && DPB_vSS<(0.8*abs(cosThetaB)+1.8) && DPB_vSS>(0.8*abs(cosThetaB)+1)")
    rc.Add("VRVV", isDF + " && nSJets==0 && nBJets==0 && MDR>30 && RPT<0.5 && DPB_vSS>(0.8*abs(cosThetaB)+1.8)")
    
    return rc
