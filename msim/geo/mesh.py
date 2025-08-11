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
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial.transform    import Rotation as mRot


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
    
    def plot(self,aH1) -> None:
        # Print vertex position:
        #   - Return vertex position as a namedtuple
        
        aH1.scatter(self._vert[0], 
                    self._vert[1], 
                    self._vert[2], 
                    color='blue', 
                    s=25)

        
    def disp(self) -> None:
        # Print vertex position:
        #   - Return vertex position as a namedtuple
        
        print( str(round(self._vert[0],2)) + ',' +  
               str(round(self._vert[1],2)) + ',' + 
               str(round(self._vert[2],2)) )


class Edge():

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

    def plot(self,aH) -> None:
        # Description:
        #   - Return vertex position as a namedtuple
        vertA = self._aVert.getPos()
        vertB = self._bVert.getPos()

        # Create a regular list:
        xLine = (vertA.x,vertB.x)
        yLine = (vertA.y,vertB.y)
        zLine = (vertA.z,vertB.z)

        aH.plot(xLine, yLine, zLine, color='blue', linewidth=2)

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
    
    def plot(self,aH) -> None:
        # Description:
        #   - Return vertex position as a namedtuple

        # Create a regular list:
        verts = [ iVert.asVector() for iVert in self._vertLst]
        poly = Poly3DCollection([verts], facecolors='skyblue', edgecolors='black', linewidths=1, alpha=0.5)
        aH.add_collection3d(poly)

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
        
        upperVert = [ Vert(ix,0.0,iy) for ix,iy in zip(xu,yu)]
        lowerVert = [ Vert(ix,0.0,iy) for ix,iy in zip(xl,yl)]

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
    
    def plot(self,aH) -> None:
        # Description:
        #   - Return vertex position as a namedtuple

        nVert = self.nVert()
        for iVert in range(nVert):
            # Create edge from A/B
            index  = np.mod(iVert ,nVert)
            index1 = np.mod(iVert+1,nVert)

            self.vert(index).plot(aH)

            # Edge:
            aEdge = Edge(self.vert(index),
                         self.vert(index1))
            aEdge.plot(aH)
            
    @staticmethod
    def link(airfoilA,airfoilB) -> tuple:

        # Ensure airfoils have same size:    
        assert airfoilA.nVert() == airfoilA.nVert()
        nVert = airfoilA.nVert()

        # Pre-allocate list of faces
        faceList: list[Optional[Face]] = [None] * nVert
        edgeList: list[Optional[Face]] = [None] * nVert

        for iFace in range(nVert):
            # Create edge from A/B
            index  = np.mod(iFace ,nVert)
            index1 = np.mod(iFace+1,nVert)

            # Face
            aFace = Face((airfoilA.vert(index),
                          airfoilB.vert(index),
                          airfoilB.vert(index1),
                          airfoilA.vert(index1)))
            faceList[iFace] = aFace

            # Edge:
            aEdge = Edge(airfoilA.vert(index),airfoilB.vert(index))
            edgeList[iFace] = aEdge

        return (faceList,edgeList)

    def disp(self) -> None:
        # Print vertex position:
        #   - Return vertex position as a namedtuple
        
        for iVert in self._vertLst:
            iVert.disp() 
        
class Cube():

    def __init__(self,
                 size: float,
                 origin = np.array([0,0,0])) -> None:
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
        
        x0 = origin[0]
        y0 = origin[1]
        z0 = origin[2]
        l  = size/2

        mVert0 = Vert(-1.0*l + x0,-1.0*l + y0,-1.0*l + z0)
        mVert1 = Vert(-1.0*l + x0,1.0*l  + y0,-1.0*l + z0)
        mVert2 = Vert(1.0*l  + x0,1.0*l  + y0,-1.0*l + z0)
        mVert3 = Vert(1.0*l  + x0,-1.0*l + y0,-1.0*l + z0)
        mVert4 = Vert(-1.0*l + x0,-1.0*l + y0, 1.0*l + z0)
        mVert5 = Vert(-1.0*l + x0,1.0*l  + y0, 1.0*l + z0)
        mVert6 = Vert(1.0*l  + x0,1.0*l  + y0, 1.0*l + z0)
        mVert7 = Vert(1.0*l  + x0,-1.0*l + y0, 1.0*l + z0)

        self._vertLst = (mVert0,mVert1,mVert2,mVert3,mVert4,mVert5,mVert6,mVert7)

        # mFaces:
        mFace0 = Face((mVert0,mVert1,mVert2,mVert3)) # botton
        mFace1 = Face((mVert4,mVert5,mVert6,mVert7)) # top
        mFace2 = Face((mVert2,mVert3,mVert7,mVert6)) # front
        mFace3 = Face((mVert1,mVert2,mVert6,mVert5)) # Right
        mFace4 = Face((mVert0,mVert1,mVert5,mVert4)) # Back
        mFace5 = Face((mVert0,mVert3,mVert7,mVert4)) # Left
        
        self._faceLst = (mFace0,mFace1,mFace2,mFace3,mFace4,mFace5)

    def getVerts(self) -> Vert:
        # Print vertex position:
        #   - Return vertex position as a namedtuple
        
        return self._vertLst
    
    def getFaces(self) -> Face:
        # Print vertex position:
        #   - Return vertex position as a namedtuple
        
        return self._faceLst
    
class Wing():

    def __init__(self,
                 name: str,
                 startX_m: float,
                 startY_m: float,
                 startZ_m: float,
                 rootChord_m: float,
                 M: np.ndarray, 
                 P: np.ndarray, 
                 XX: np.ndarray, 
                 twist_deg: np.ndarray, 
                 dihed_deg: np.ndarray, 
                 b_m: np.ndarray, 
                 taperRatio: np.ndarray, 
                 sweep_deg: np.ndarray,
                 nPoints) -> None:
        # Description:
        #   - Create a wing with a series of airfoils. Allows user to define wing shape similarly to
        #     Tornado VLM.
        # Inputs:
        #   - startX,Y,Z: Airfoil start position
        #   - rootChord_m: Chord of first airfoil
        #   - M: maximum camber divided by 100 (E.g. M=2, camber is 2% of the chord)
        #   - P: position of the maximum camber divided by 10. (E.g. P=4, maximum camber is at 40% of the chord)
        #   - XX: thickness divided by 100. (E.g. XX=12, thiickness is 12% of the chord.
        #   - twist_deg:
        #   - dihed_deg:
        #   - b_m:
        #   - taperRatio:
        #   - sweep_deg:
        #   - nPoints: Number of points for each airfoil

        # Ensure some number of elements:
        lenM  = len(M)
        lenP  = len(P)
        lenXX = len(XX)
        lenTw = len(twist_deg)
        lenDh = len(dihed_deg)
        lenB  = len(b_m)
        lenT  = len(taperRatio)
        lenS  = len(sweep_deg)

        assert( lenM > 1      and \
                lenM == lenP  and \
                lenM == lenXX and \
                lenM == lenTw and \
                lenM == lenDh and \
                lenM == lenB  and \
                lenM == lenT  and \
                lenM == lenS)
        
        # ------------------------------
        # Define chord for each airfoil:
        # ------------------------------
        nFoil = lenM + 1 
        self._chords = np.zeros(nFoil)
        self._startX = np.zeros(nFoil)
        self._startY = np.zeros(nFoil)
        self._startZ = np.zeros(nFoil)

        self._chords[0] = rootChord_m
        self._startX[0] = startX_m
        self._startY[0] = startY_m
        self._startZ[0] = startZ_m

        for iFoil in range(lenM):
            cTaper     = taperRatio[iFoil]
            cChord_m   = self._chords[iFoil]
            cB_m       = b_m[iFoil]
            cSweep_rad = np.deg2rad(sweep_deg[iFoil])
            cDihed_rad = np.deg2rad(dihed_deg[iFoil])

            self._chords[iFoil+1] = cChord_m * cTaper
            self._startX[iFoil+1] = cChord_m * 0.25 + \
                                    cB_m     * np.tan(cSweep_rad) + \
                                    cChord_m * -0.25 + \
                                    self._startX[iFoil]
            self._startY[iFoil+1] = cB_m     * np.cos(cDihed_rad) + \
                                    self._startY[iFoil]
            self._startZ[iFoil+1] = cB_m     * np.sin(cDihed_rad) + \
                                    self._startZ[iFoil]            

        # Create list of airfoils:
        self._airfoil: list[Optional[Airfoil]] = [None] * nFoil

        for iFoil in range(nFoil):
            # Create edge from A/B
            airfoilA = Airfoil(M[iFoil],
                               P[iFoil], 
                               XX[iFoil],
                               nPoints)
            
            airfoilA.translate(np.array([self._startX[iFoil],
                                         self._startY[iFoil],
                                         self._startZ[iFoil]]))
            
            self._airfoil[iFoil] = airfoilA

