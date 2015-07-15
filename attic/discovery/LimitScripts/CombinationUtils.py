

# -------------------------------------------------- #
# Functionality for performing the 0-Jet and 1-Jet   #
# signal region combination for the 2L0S Super-Razor #
# analysis.                                          #
#                -- Dantrim 20/11/2014               #
# -------------------------------------------------- #


class CombinationUtils :

    # Dictionaries to hold best 0-Jet and 1-Jet SR
    # for each mass point determined after running
    # the limits separately for each SR, combining only
    # lepton channels

    SMCwslep_bestSRDict = {
                'SMCwslep8TeV_112.5_12.5':	['Super0a', 'Super1a'],
                'SMCwslep8TeV_112.5_47.5':	['Super0a', 'Super1a'],
                'SMCwslep8TeV_117.5_82.5':	['Super0a', 'Super1c'],
                'SMCwslep8TeV_130.0_30.0':	['Super0a', 'Super1c'],
                'SMCwslep8TeV_132.5_67.5':	['Super0a', 'Super1a'],
                'SMCwslep8TeV_142.5_107.5':	['Super0a', 'Super1a'],
                'SMCwslep8TeV_150.0_50.0':	['Super0a', 'Super1a'],
                'SMCwslep8TeV_155.0_5.0':	['Super0a', 'Super1b'],
                'SMCwslep8TeV_157.5_92.5':	['Super0a', 'Super1a'],
                'SMCwslep8TeV_175.0_25.0':	['Super0a', 'Super1c'],
                'SMCwslep8TeV_175.0_75.0':	['Super0a', 'Super1b'],
                'SMCwslep8TeV_192.5_157.5':	['Super0a', 'Super1a'],
                'SMCwslep8TeV_200.0_50.0':	['Super0a', 'Super1b'],
                'SMCwslep8TeV_207.5_142.5':	['Super0a', 'Super1a'],
                'SMCwslep8TeV_225.0_125.0':	['Super0a', 'Super1b'],
                'SMCwslep8TeV_250.0_0.0':	['Super0b', 'Super1b'],
                'SMCwslep8TeV_250.0_100.0':	['Super0b', 'Super1b'],
                'SMCwslep8TeV_267.5_232.5':	['Super0c', 'Super1c'],
                'SMCwslep8TeV_282.5_217.5':	['Super0a', 'Super1a'],
                'SMCwslep8TeV_300.0_50.0':	['Super0b', 'Super1c'],
                'SMCwslep8TeV_300.0_200.0':	['Super0a', 'Super1b'],
                'SMCwslep8TeV_325.0_175.0':	['Super0b', 'Super1b'],
                'SMCwslep8TeV_330.0_295.0':	['Super0a', 'Super1c'],
                'SMCwslep8TeV_345.0_280.0':	['Super0a', 'Super1b'],
                'SMCwslep8TeV_350.0_0.0':	['Super0c', 'Super1c'],
                'SMCwslep8TeV_362.5_262.5':	['Super0a', 'Super1b'],
                'SMCwslep8TeV_375.0_125.0':	['Super0b', 'Super1b'],
                'SMCwslep8TeV_387.5_237.5':	['Super0b', 'Super1b'],
                'SMCwslep8TeV_392.5_357.5':	['Super0a', 'Super1c'],
                'SMCwslep8TeV_407.5_342.5':	['Super0a', 'Super1b'],
                'SMCwslep8TeV_425.0_75.0':	['Super0c', 'Super1b'],
                'SMCwslep8TeV_425.0_325.0':	['Super0a', 'Super1b'],
                'SMCwslep8TeV_437.5_187.5':	['Super0b', 'Super1b'],
                'SMCwslep8TeV_450.0_300.0':	['Super0b', 'Super1b'],
                'SMCwslep8TeV_487.5_137.5':	['Super0c', 'Super1b'],
                'SMCwslep8TeV_500.0_0.0':	['Super0c', 'Super1c'],
                'SMCwslep8TeV_500.0_250.0':	['Super0c', 'Super1b'],
                'SMCwslep8TeV_517.5_482.5':	['Super0c', 'Super1c'],
                'SMCwslep8TeV_532.5_467.5':	['Super0a', 'Super1b'],
                'SMCwslep8TeV_550.0_200.0':	['Super0c', 'Super1b'],
                'SMCwslep8TeV_550.0_450.0':	['Super0a', 'Super1b'],
                'SMCwslep8TeV_562.5_62.5':	['Super0c', 'Super1b'],
                'SMCwslep8TeV_575.0_425.0':	['Super0b', 'Super1b'],
                'SMCwslep8TeV_625.0_0.0':	['Super0c', 'Super1c'],
                'SMCwslep8TeV_625.0_125.0':	['Super0c', 'Super1c'],
                'SMCwslep8TeV_625.0_375.0':	['Super0c', 'Super1b'],
                'SMCwslep8TeV_642.5_607.5':	['Super0a', 'Super1a'],
                'SMCwslep8TeV_675.0_325.0':	['Super0c', 'Super1b'],
                'SMCwslep8TeV_675.0_575.0':	['Super0a', 'Super1b'],
                'SMCwslep8TeV_687.5_62.5':	['Super0c', 'Super1b'],
                'SMCwslep8TeV_700.0_550.0':	['Super0b', 'Super1b'],
                'SMCwslep8TeV_750.0_0.0':	['Super0a', 'Super1a'],
                'SMCwslep8TeV_750.0_250.0':	['Super0a', 'Super1a'],
                'SMCwslep8TeV_750.0_500.0':	['Super0a', 'Super1a'],
                'SMCwslep8TeV_100.0_0.0':	['Super0a', 'Super1a'],
                'SMCwslep8TeV_150.0_0.0':	['Super0a', 'Super1b']  }

   
    def getSRPerPoint(self, grid) :
        if 'SMCwslep' in grid : return self.SMCwslep_bestSRDict
        
        empty = []
        return empty #when calling this function, check to see if returned list is empy or not
