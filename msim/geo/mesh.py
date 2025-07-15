# [Description]: 
#   - This module includes the primitives required to generate airfoil shapes

# -------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------
import numpy            as     np
import msim.helpers     as mHelp
import msim.geo.airfoil as mfoil
from collections        import namedtuple
from typing             import Optional
from scipy.spatial.transform import Rotation as mRot

# -------------------------------------------------------------------------
# Basic mesh shapes
# -------------------------------------------------------------------------


class Vert():

    def __init__(self,x: float, y: float, z: float) -> None:
        # Description:
        #   - Basic Vertex
        # Inputs:
        #   - x,y,z: local Vertex position. Objects using this class may use
        #            transformation matrix

        # Basic properties:
        self._vert = np.array([x, y, z])

    def getPos(self) -> namedtuple:
        # Description:
        #   - Return vertex position as a namedtuple
        
        Vertex = namedtuple('Vert',['x','y','z'])

        return Vertex(self._vert[0],self._vert[1],self._vert[2])
    
    def asVector(self) -> np.array:
        # Description:
        #   - Return vertex position as a namedtuple
        
        return self._vert
    
    def translate(self,t: np.array) -> None:
        # Description:
        #   - t: translation matrix (x,y,z)
        
        self._vert = t + self._vert

    def scale(self,s: np.array) -> None:
        # Description:
        #   - t: translation matrix (x,y,z)
        
        self._vert = s * self._vert

    def rotate(self,x_deg: float = 0,
                    y_deg: float = 0,
                    z_deg: float = 0) -> None:
        # Description:
        #   - phi_deg, theta_deg, psi_deg: rotation angles
        
        rAcToAirfoil = mRot.from_euler('xyz', 
                                       [x_deg, y_deg, z_deg], 
                                       degrees = True)
        self._vert = rAcToAirfoil.apply(self._vert)
    
    def rotateAtPoint(self,
                      x_deg: float = 0,
                      y_deg: float = 0,
                      z_deg: float = 0,
                      t = np.array([0,0,0])) -> None:
        # Description:
        #   - phi_deg, theta_deg, psi_deg: rotation angles
        
        self.translate(-t)
        self.rotate(x_deg,y_deg,z_deg)
        self.translate(t)

        return
    
    def disp(self) -> None:
        # Print vertex position:
        #   - Return vertex position as a namedtuple
        
        print( str(round(self._vert[0],2)) + ',' +  
               str(round(self._vert[1],2)) + ',' + 
               str(round(self._vert[2],2)) )


class edge():

    def __init__(self,aVert: Vert, bVert: Vert) -> None:
        # Description:
        #   - Basic vertex
        # Inputs:
        #   - x,y,z: local vertex position. Objects using this class may use
        #            transformation matrix

        # Basic properties:
        self._aVert = aVert
        self._bVert = bVert

    def getVerts(self) -> namedtuple:
        # Description:
        #   - Return vertex position as a namedtuple
        
        Edge = namedtuple('Edge',['a','b'])

        return Edge(self._aVert,self._bVert)

class Face():

    def __init__(self,aVerts: list) -> None:
        # Description:
        #   - Basic vertex
        # Inputs:
        #   - x,y,z: local vertex position. Objects using this class may use
        #            transformation matrix

        # Ensure at least 3 verts
        assert len(aVerts) >= 3, "at least 3 verts expected"

        # Basic properties:
        self._vertLst = aVerts

    def getVerts(self) -> tuple:
        # Description:
        #   - Return vertex position as a namedtuple

        return self._vertLst
    
    @staticmethod
    def getVertIndex(aFace, aVert: tuple) -> tuple:
        # Description:
        #   - Return the indexes of a Verts in a Face given 
        #     a list of Verts
        # Inputs:
        #   - aFace: Face to be assessed
        #   - aVertList: list of vertices

        vertIndex = tuple( aVert.index(iVert) for iVert in aFace.getVerts() )

        return vertIndex
    
class Airfoil():

    def __init__(self,
                 M: int, 
                 P: int, 
                 XX: int, 
                 nPoints: int,
                 x_deg: int = 0,
                 y_deg: int = 0,
                 z_deg: int = 0,
                 t = np.array([0,0,0]),
                 scale:float = 1) -> None:
        # Description:
        #   - Maintain most relevant properties to calculate a NACA 4 series 
        #     airfoil, including thickness, gradient, upper/lower surfaces
        #     Consider: airfoiltools.com (NACA 4 digit airfoil calculation)           
        # Inputs:
        #   - M: maximum camber divided by 100 (E.g. M=2, camber is 2% of the chord)
        #   - P: position of the maximum camber divided by 10. (E.g. P=4, maximum camber is at 40% of the chord)
        #   - XX: thickness divided by 100. (E.g. XX=12, thiickness is 12% of the chord.
        #   - nPoints: Number of x position in airfoil
        #   - phi_deg, theta_deg, psi_deg: rotation angles
        #   - t: translation vector (3)
        #   - scale: airfoil scale factor

        # Example:
        #   - Naca4(2,4,12): Corresponds to NACA 2412

        # Description:
        #   - Basic vertex
        # Inputs:
        #   - x,y,z: local vertex position. Objects using this class may use
        #            transformation matrix

        _airfoil = mfoil.Naca4(M,P,XX)

        (x,xu,yu,xl,yl,yc) = _airfoil.getSurf(nPoints)
        
        upperVert = [ Vert(ix,iy,0.0) for ix,iy in zip(xu,yu)]
        lowerVert = [ Vert(ix,iy,0.0) for ix,iy in zip(xl,yl)]

        self._vertLst = upperVert + lowerVert[:0:-1]

    def vertList(self) -> Vert:
        # Print vertex position:
        #   - Return vertex position as a namedtuple
        
        return self._vertLst
    
    def vert(self,i) -> Vert:
        # Print vertex position:
        #   - Return vertex position as a namedtuple
        
        return self._vertLst[i]
    
    def translate(self,t: np.ndarray) -> None:
        # Print vertex position:
        #   - Return vertex position as a namedtuple
        
        for iVert in self._vertLst:
            iVert.translate(t)

    def scale(self,s: np.ndarray) -> None:
        # Print vertex position:
        #   - Return vertex position as a namedtuple
        
        for iVert in self._vertLst:
            iVert.scale(s)

    def rotate(self,
               x_deg: int = 0,
               y_deg: int = 0,
               z_deg: int = 0) -> None:
        # Print vertex position:
        #   - Return vertex position as a namedtuple
        
        for iVert in self._vertLst:
            iVert.rotate(x_deg,
                         y_deg,
                         z_deg)

    def rotateAtPoint(self,
                      x_deg: float = 0,
                      y_deg: float = 0,
                      z_deg: float = 0,
                      t = np.array([0,0,0])) -> None:
        
        for iVert in self._vertLst:
            iVert.rotateAtPoint(x_deg,
                                y_deg,
                                z_deg,
                                t)
    
    def nVert(self) -> int:
        return len(self._vertLst)

    @staticmethod
    def link(airfoilA,airfoilB) -> tuple:

        # Ensure airfoils have same size:    
        assert airfoilA.nVert() == airfoilA.nVert()
        nVert = airfoilA.nVert()

        # Pre-allocate list of faces
        faceList: list[Optional[Face]] = [None] * nVert

        for iFace in range(nVert):
            # Create edge from A/B
            index  = np.mod(iFace ,nVert)
            index1 = np.mod(iFace+1,nVert)

            aFace = Face((airfoilA.vert(index),
                          airfoilB.vert(index),
                          airfoilA.vert(index1),
                          airfoilB.vert(index1)))
            faceList[iFace] = aFace

        return faceList

    def disp(self) -> None:
        # Print vertex position:
        #   - Return vertex position as a namedtuple
        
        for iVert in self._vertLst:
            iVert.disp() 
        
        