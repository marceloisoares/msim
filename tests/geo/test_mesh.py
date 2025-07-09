import matplotlib.pylab as plt
import numpy            as np
import pytest
import msim.lib         as mlib
import msim.helpers     as mHelp
import msim.geo.mesh    as mMesh

# -------------------------------------------------------------------------
# Basic mesh shapes
# -------------------------------------------------------------------------

class Test_Vert:
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

    def test_basic(self):

        mVert = mMesh.vert(-1.1,2.2,0.5)
        vertPos = mVert.getPos()

        # X
        isequal, msg = mHelp.verifyEqual(vertPos.x,
                                         -1.1,
                                         0.0001) # tol
        assert isequal, msg

        isequal, msg = mHelp.verifyEqual(vertPos.x,
                                         vertPos[0],
                                         0.0001) # tol
        assert isequal, msg

        isequal, msg = mHelp.verifyEqual(vertPos.y,
                                         2.2,
                                         0.0001) # tol
        assert isequal, msg

        isequal, msg = mHelp.verifyEqual(vertPos.z,
                                         0.5,
                                         0.0001) # tol
        assert isequal, msg


class Test_Edge:
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

    def test_basic(self):

        # Create edge from A/B
        mVertA = mMesh.vert(0.0,1.0,0.0)
        mVertB = mMesh.vert(1.0,0.0,0.0)

        mEdge = mMesh.edge(mVertA,mVertB)

        # X
        verts = mEdge.getVerts()

        assert verts.a is mVertA
        assert verts.b is mVertB


class Test_Face:
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

    def test_3verts(self):

        # Create edge from A/B
        mVertA = mMesh.vert(0.0,1.0,0.0)
        mVertB = mMesh.vert(1.0,0.0,0.0)
        mVertC = mMesh.vert(0.0,0.0,1.0)

        mFace = mMesh.face((mVertA,mVertB,mVertC))

        # X
        verts = mFace.getVerts()

        assert verts[0] is mVertA
        assert verts[1] is mVertB        
        assert verts[2] is mVertC

    def test_4verts(self):

        # Create edge from A/B
        mVertA = mMesh.vert(0.0,1.0,0.0)
        mVertB = mMesh.vert(1.0,0.0,0.0)
        mVertC = mMesh.vert(0.0,0.0,1.0)
        mVertD = mMesh.vert(1.0,0.0,1.0)

        mFace = mMesh.face((mVertA,mVertB,mVertC,mVertD))

        # X
        verts = mFace.getVerts()

        assert verts[0] is mVertA
        assert verts[1] is mVertB        
        assert verts[2] is mVertC        
        assert verts[3] is mVertD        

    def test_2verts(self):

        # Create edge from A/B
        mVertA = mMesh.vert(0.0,1.0,0.0)
        mVertB = mMesh.vert(1.0,0.0,0.0)

        with pytest.raises(AssertionError, match="at least 3 verts expected"):
            mFace = mMesh.face((mVertA,mVertB))
        