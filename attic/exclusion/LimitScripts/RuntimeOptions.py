
#######################################################
# This will house a class to handle the configurable  #
# options such as "doExclusion" etc.  This way we can #
# carry around one object and we know everything that #
# will be set                                         #
#######################################################


class RuntimeOptions:
        
    #------------------------------------------#
    # This will contain all the configuration
    # necessary to run the rest of the script.
    # It will allow the user to specify the
    # configuration in one place and then all
    # changes will be propagated through.
    #------------------------------------------#    
    def __init__(self,
                 do2L,          # Set to do 2 lep analysis
                 doToys,        # Turn on running of toys
                 gridForToys,   # Specify grid to use for toys
                 nToys,         # Specify how many toys to run

                 doExclusion,   # do Exclusion fit
                 doDiscovery,   # do discovry fit
                 doValidation,  # do fit in validaiton
                 doShape,       # do shape fit

                 doSimFit2LWW,  # Simultaneous fit to WW
                 doSimFit2LTop, # Simultaneous fit to Top
                 doSimFit2LZV,  # Simultaneous fit to ZV

                 splitMCSys,    # True to split MC sys into indiv. samples
                 
                 blindSR,       # Keep blind the SR
                 blindCR,       # Keep blind the CR
                 blindVR,       # Keep blind the VR

                 sigUncert,     # Specify type of sig uncert.  Ex: "NoSys"
                 sigGrid,       # Specify grid Ex: "ModeC"
                 signalRegion,  # Specify SR Ex: "SR4a"
                 leptonChannel, # Specify the two lepton channel

                 slepLimitN,    # Specify slepton Limit Number

                 bkgFile,       # input background file      
                 dataFile,      # input data file               // dantrim
                 sigFile,       # input signal file
                 anaName,       # analysis name where results saved under

                 inputLumi,     # input luminosity for tree
                 outputLumi,    # output luminosity to scale to
                 lumiUnits      # units
                 ):

        # Now initialize
        self.do2L          = do2L
        self.doToys        = doToys
        self.gridForToys   = gridForToys
        self.nToys         = nToys
        self.doExclusion   = doExclusion
        self.doDiscovery   = doDiscovery
        self.doValidation  = doValidation
        self.doShape       = doShape
        self.doSimFit2LWW  = doSimFit2LWW
        self.doSimFit2LTop = doSimFit2LTop
        self.doSimFit2LZV  = doSimFit2LZV
        self.splitMCSys    = splitMCSys
        self.blindSR       = blindSR
        self.blindCR       = blindCR
        self.blindVR       = blindVR
        self.sigUncert     = sigUncert
        self.sigGrid       = sigGrid
        self.signalRegion  = signalRegion
        self.leptonChannel = leptonChannel
        self.slepLimitN    = slepLimitN
        self.bkgFile       = bkgFile
        self.dataFile      = dataFile           # dantrim
        self.sigFile       = sigFile
        self.anaName       = anaName
        self.inputLumi     = inputLumi
        self.outputLumi    = outputLumi
        self.lumiUnits     = lumiUnits

    # end initialization of class

    #------------------------------------------#
    # Have a method to reset everyting
    # to some default values
    #------------------------------------------#
        
    def clear(self):
        self.do2L          = False
        self.doToys        = False
        self.doExclusion   = False
        self.doDiscovery   = False
        self.doValidation  = False
        self.doShape       = False
        self.doSimFit2LWW  = False
        self.doSimFit2LTop = False
        self.doSimFit2LZV  = False
        self.splitMCSys    = Flase
        self.blindSR       = False
        self.blindCR       = False
        self.blindVR       = False
        self.sigUncert     = ""
        self.sigGrid       = ""
        self.signalRegion  = ""
        self.leptonChannel = -1
        self.slepLimitN    = -1
        self.bkgFile       = ""
        self.dataFile      = ""         # dantrim
        self.sigFile       = ""
        self.anaName       = ""
        self.inputLumi     = 0.
        self.outputLumi    = 0.
        self.lumiUnits     = ""

    #end clear
