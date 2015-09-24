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
    #  Test Regions                                          #
    # ------------------------------------------------------ #
    rc.Add("SR4", "nLeptons==2 && nMuons==1 && nElectrons==1 && mt2>120 && l_pt[0]>35 && l_pt[1]>20 && (l_q[0]*l_q[1])<0")
    rc.Add("SRz", "nLeptons==2 && nMuons==1 && nElectrons==1 && mDeltaR>120 && l_pt[0]>35 && l_pt[1]>20 && (l_q[0]*l_q[1])<0")

    return rc
