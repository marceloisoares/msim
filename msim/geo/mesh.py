# [Description]: 
#   - This module includes the primitives required to generate airfoil shapes

# -------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------
import numpy        as     np
import msim.helpers as mHelp
from collections    import namedtuple

# -------------------------------------------------------------------------
# Basic mesh shapes
# -------------------------------------------------------------------------


class vert():

    def __init__(self,x: float, y: float, z: float) -> None:
        # Description:
        #   - Basic vertex
        # Inputs:
        #   - x,y,z: local vertex position. Objects using this class may use
        #            transformation matrix

        # Basic properties:
        self._x = x
        self._y = y
        self._z = z

    def getPos(self) -> namedtuple:
        # Description:
        #   - Return vertex position as a namedtuple
        
        Vertex = namedtuple('Vert',['x','y','z'])

        return Vertex(self._x,self._y,self._z)

class edge():

    def __init__(self,aVert: vert, bVert: vert) -> None:
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

class face():

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