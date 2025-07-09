import matplotlib.pylab as plt
import numpy            as np
import msim.lib         as mlib
import msim.helpers     as mHelp
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
        assert naca4._M == 0.02
        assert naca4._P == 0.4
        assert naca4._XX == 0.12

    def test_maxchamber(self):

        naca4 = mfoil.Naca4(2,4,12)

        # expect max chamber of m (2%) at 40%
        yc = naca4._getCamber(0.4)

        # test
        isequal, msg = mHelp.verifyEqual(yc,
                                         0.02,
                                         0.0001) # tol
        assert isequal, msg

    def test_minGradient(self):

        naca4 = mfoil.Naca4(2,4,12)

        # expect max chamber of m (2%) at 40%
        yc = naca4._getGradient(0.4)

        # test
        isequal, msg = mHelp.verifyEqual(yc,
                                         0.0,
                                         0.0001) # tol
        assert isequal, msg        

    def test_plotAirfoil(self):

        naca4 = mfoil.Naca4(2,4,5)

        # Create airfoil
        nPoints = 50
        (x,xu,yu,xl,yl,yc) = naca4.getSurf(nPoints)
        
        # Plot results:
        plt.style.use('fivethirtyeight')
        fH = plt.figure()
        aH = fH.add_subplot(1, 1, 1)
        aH.axis('equal')
        plt.ion()
        plt.show(block=False)

        # Camber line
        aH.plot(x,
                yc,
                linestyle='-',
                marker='o',
                color='r',
                markerfacecolor='r',
                markeredgecolor='r')
        
        aH.plot(xu,
                yu,
                linestyle='-',
                marker='o',
                color='b',
                markerfacecolor='b',
                markeredgecolor='b')
        
        aH.plot(xl,
                yl,
                linestyle='-',
                marker='o',
                color='b',
                markerfacecolor='b',
                markeredgecolor='b')
        
        plt.draw()
        plt.close(fH)

        

    