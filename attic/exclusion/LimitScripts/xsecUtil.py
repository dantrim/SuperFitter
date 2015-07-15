#################################################
# Functionality for obtaining the up and down   #
# variation of the signal cross-section since   #
# 'syst_XSUP', 'sys_XSDOWN' in HistFitter/      #
# Superflow is not implemented correctly.       #
#                                               #
# author: Daniel Antrim                         #
# date  : January 17, 2015                      #
#################################################



class xsecUtil :

    # dictionaries to hold the up- and down- variation
    # of the cross section in terms of the relative uncertainties
    # on the xsec calculations found in SUSYTools
    #
    # format: { gridpoint (following tree-naming in HFT) : [ xsec_UP, xsec_DOWN ] }

    SMCwslep_xsecDict = {
        'SMCwslep8TeV_112.5_12.5'   : [ 1.0718, 0.9282 ],
        'SMCwslep8TeV_112.5_47.5'   : [ 1.0718, 0.9282 ],
        'SMCwslep8TeV_117.5_82.5'   : [ 1.0712, 0.9288 ],
        'SMCwslep8TeV_130.0_30.0'   : [ 1.0716, 0.9284 ],
        'SMCwslep8TeV_132.5_67.5'   : [ 1.0698, 0.9302 ],
        'SMCwslep8TeV_142.5_107.5'  : [ 1.0683, 0.9317 ],
        'SMCwslep8TeV_150.0_50.0'   : [ 1.0709, 0.9291 ],
        'SMCwslep8TeV_155.0_5.0'    : [ 1.0660, 0.9340 ],
        'SMCwslep8TeV_157.5_92.5'   : [ 1.0654, 0.9346 ],
        'SMCwslep8TeV_175.0_25.0'   : [ 1.0658, 0.9342 ],
        'SMCwslep8TeV_175.0_75.0'   : [ 1.0658, 0.9342 ],
        'SMCwslep8TeV_192.5_157.5'  : [ 1.0638, 0.9362 ],
        'SMCwslep8TeV_200.0_50.0'   : [ 1.0640, 0.9360 ],
        'SMCwslep8TeV_207.5_142.5'  : [ 1.0636, 0.9364 ],
        'SMCwslep8TeV_225.0_125.0'  : [ 1.0625, 0.9375 ],
        'SMCwslep8TeV_250.0_0.0'    : [ 1.0669, 0.9340 ],
        'SMCwslep8TeV_250.0_100.0'  : [ 1.0660, 0.9340 ],
        'SMCwslep8TeV_267.5_232.5'  : [ 1.0610, 0.9390 ],
        'SMCwslep8TeV_282.5_217.5'  : [ 1.0648, 0.9352 ],
        'SMCwslep8TeV_300.0_50.0'   : [ 1.0659, 0.9341 ],
        'SMCwslep8TeV_300.0_200.0'  : [ 1.0659, 0.9341 ],
        'SMCwslep8TeV_325.0_175.0'  : [ 1.0697, 0.9303 ],
        'SMCwslep8TeV_330.0_295.0'  : [ 1.0694, 0.9306 ],
        'SMCwslep8TeV_345.0_280.0'  : [ 1.0689, 0.9311 ],
        'SMCwslep8TeV_350.0_0.0'    : [ 1.0695, 0.9305 ],
        'SMCwslep8TeV_362.5_262.5'  : [ 1.0677, 0.9323 ],
        'SMCwslep8TeV_375.0_125.0'  : [ 1.0717, 0.9283 ],
        'SMCwslep8TeV_387.5_237.5'  : [ 1.0715, 0.9285 ],
        'SMCwslep8TeV_392.5_357.5'  : [ 1.0724, 0.9276 ],
        'SMCwslep8TeV_407.5_342.5'  : [ 1.0700, 0.9300 ],
        'SMCwslep8TeV_425.0_75.0'   : [ 1.0755, 0.9245 ],
        'SMCwslep8TeV_425.0_325.0'  : [ 1.0755, 0.9245 ],
        'SMCwslep8TeV_437.5_187.5'  : [ 1.0728, 0.9272 ],
        'SMCwslep8TeV_450.0_300.0'  : [ 1.0759, 0.9241 ],
        'SMCwslep8TeV_487.5_137.5'  : [ 1.0791, 0.9209 ],
        'SMCwslep8TeV_500.0_0.0'    : [ 1.0795, 0.9205 ],
        'SMCwslep8TeV_500.0_250.0'  : [ 1.0795, 0.9205 ],
        'SMCwslep8TeV_517.5_482.5'  : [ 1.0807, 0.9193 ],
        'SMCwslep8TeV_532.5_467.5'  : [ 1.0792, 0.9208 ],
        'SMCwslep8TeV_550.0_200.0'  : [ 1.0840, 0.9160 ],
        'SMCwslep8TeV_550.0_450.0'  : [ 1.0840, 0.9160 ],
        'SMCwslep8TeV_562.5_62.5'   : [ 1.0831, 0.9169 ],
        'SMCwslep8TeV_575.0_425.0'  : [ 1.0859, 0.9141 ],
        'SMCwslep8TeV_625.0_0.0'    : [ 1.0856, 0.9144 ],
        'SMCwslep8TeV_625.0_125.0'  : [ 1.0856, 0.9144 ],
        'SMCwslep8TeV_625.0_375.0'  : [ 1.0856, 0.9144 ],
        'SMCwslep8TeV_642.5_607.5'  : [ 1.0879, 0.9121 ],
        'SMCwslep8TeV_675.0_325.0'  : [ 1.0943, 0.9057 ],
        'SMCwslep8TeV_675.0_575.0'  : [ 1.0943, 0.9057 ],
        'SMCwslep8TeV_687.5_62.5'   : [ 1.0913, 0.9087 ],
        'SMCwslep8TeV_700.0_550.0'  : [ 1.0936, 0.9064 ],
        'SMCwslep8TeV_750.0_0.0'    : [ 1.0937, 0.9063 ],
        'SMCwslep8TeV_750.0_250.0'  : [ 1.0937, 0.9063 ],
        'SMCwslep8TeV_750.0_500.0'  : [ 1.0937, 0.9063 ],
        'SMCwslep8TeV_100.0_0.0'    : [ 1.0743, 0.9257 ],
        'SMCwslep8TeV_150.0_0.0'    : [ 1.0709, 0.9291 ],
        'SMCwslep8TeV_100.0_35.0'   : [ 1.0743, 0.9257 ],
        'SMCwslep8TeV_100.0_65.0'   : [ 1.0743, 0.9257 ],
        'SMCwslep8TeV_100.0_80.0'   : [ 1.0743, 0.9257 ],
        'SMCwslep8TeV_110.0_90.0'   : [ 1.0720, 0.9280 ],
        'SMCwslep8TeV_135.0_115.0'  : [ 1.0684, 0.9316 ] }

    def getXsecUncertainty(self, grid) :
        if 'SMCwslep' in grid : return self.SMCwslep_xsecDict

        empty = []
        return empty # when calling this function, check to see if return object is empty


