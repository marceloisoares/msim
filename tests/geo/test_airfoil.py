from collections    import namedtuple
import numpy        as np
import msim.lib     as mlib
import msim.helpers as mHelp
import msim.geo.airfoil as mfoil

# -------------------------------------------------------------------------
# Ports
# -------------------------------------------------------------------------

class Test_Naca4:
    def setup_class(self):
        # Class setup:
        pass

    def teardown_class(self):
        # Class teardown:
        pass

    def setup(self):
        # Method setup:
        pass

    def teardown(self):
        # Method teardown:
        pass

    def test_basicData(self):

        naca4 = mfoil.Naca4(2,4,12)

        # Basic data
        assert naca4._M == 2
        assert naca4._P == 4
        assert naca4._XX == 12

    def test_maxChamber(self):

        naca4 = mfoil.Naca4(2,4,12)

        # Expect max chamber of M (2%) at 40%
        yc = naca4._getCamber(0.4)

        # Test
        isEqual, msg = mHelp.verifyEqual(yc,
                                         0.02,
                                         0.0001) # tol
        assert isEqual, msg


    