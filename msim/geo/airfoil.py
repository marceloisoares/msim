# [Description]: 
#   - This module includes the primitives required to generate airfoil shapes

# -------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------

# Abstract base class
from   abc   import ABC, abstractmethod
import numpy as     np

from msim import helpers as mhelp


# -------------------------------------------------------------------------
# NACA 4-series
# -------------------------------------------------------------------------


class Naca4():

    def __init__(self,M: int, P: int, XX: int) -> None:
        # Description:
        #   - Maintain most relevant properties to calculate a NACA 4 series 
        #     airfoil, including thickness, gradient, upper/lower surfaces
        #     Consider: airfoiltools.com (NACA 4 digit airfoil calculation)           
        # Inputs:
        #   - M: maximum camber divided by 100 (E.g. M=2, camber is 2% of the chord)
        #   - P: position of the maximum camber divided by 10. (E.g. P=4, maximum camber is at 40% of the chord)
        #   - XX: thickness divided by 100. (E.g. XX=12, thiickness is 12% of the chord.
        # Example:
        #   - Naca4(2,4,12): Corresponds to NACA 2412

        # Basic properties:
        self._M = M * 0.01
        self._P = P * 0.1
        self._XX = XX * 0.01

    def _getCamber(self,x: float) -> float:
        # Description:
        #   - Get chamber position yC
        P = self._P
        M = self._M
        assert x >= 0.0 and x <= 1.0

        if(x < P):
            yc = (M/P**2) * (2 * P * x - x**2)
        else:
            yc = (M/(1 - 2 * P + P**2)) * (1 - 2 * P + 2 * P * x - x**2)

        return yc

    def _getGradient(self,x: float) -> float:
        # Description:
        #   - Get chamber gradient dyc_dx at position x
        P = self._P
        M = self._M


        assert x >= 0.0 and x <= 1.0

        if(x < P):
            dyc_dx = ((2 * M)/P**2) * (P - x)
        else:
            dyc_dx = ((2 * M)/(1 - 2 * P + P**2)) * (P - x)

        return dyc_dx

    def _getThickness(self,x: float) -> float:
        # Description:
        #   - Get chamber position at position x
        P  = self._P
        M  = self._M
        XX = self._XX

        a0 =  0.2969
        a1 = -0.1260
        a2 = -0.3516
        a3 =  0.2843
        a4 = -0.1015

        yt =(XX/0.2)*(a0 * np.sqrt(x) +
                      a1 * x         +
                      a2 * x**2      +
                      a3 * x**3      +
                      a4 * x**4 ) 
        
        return yt

    def _getUpperLowerPos(self,x: float) -> tuple:
        # Description:
        #   - Get the upper/lower surface position corresponding to chord position x
        
        # Gradient:
        theta_rad = np.atan(self._getGradient(x))

        # Chamber position:
        yc = self._getCamber(x)

        # Thickness:
        yt = self._getThickness(x)

        # Upper
        xu = x  - yt * np.sin(theta_rad)
        yu = yc + yt * np.cos(theta_rad)

        # Lower
        xl = x  + yt * np.sin(theta_rad)
        yl = yc - yt * np.cos(theta_rad)

        return (xu, yu, xl, yl)

    def getSurf(self,nPoints: int) -> tuple:
        # Description:
        #   - Get the upper/lower surface 
        # Inputs:
        #   - nPoints: number of points
        # Output:
        #   - (x,xu,yu,xl,yl,yc)
        
        # list of points using cos spacing:
        xAng = np.linspace(0,np.pi,nPoints)
        x    = (1 - np.cos(xAng))/2

        # Pre-allocation:
        xu = np.zeros_like(x)
        yu = np.zeros_like(x)
        xl = np.zeros_like(x)
        yl = np.zeros_like(x)
        yc = np.zeros_like(x)

        for i,ix in enumerate(x):
            xu[i], yu[i], xl[i], yl[i] = self._getUpperLowerPos(ix)
            yc[i] = self._getCamber(ix)

        return (x,xu,yu,xl,yl,yc)

