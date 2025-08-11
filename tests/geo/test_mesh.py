import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy             as np
import pytest
import msim.lib          as mlib
import msim.helpers      as mHelp
import msim.geo.mesh     as mMesh

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

        mVert = mMesh.Vert(-1.1,2.2,0.5)
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

    def test_disp(self):

        mVert = mMesh.Vert(-1.1,2.2,0.5)
        vertPos = mVert.disp()

        assert True

    def test_vector(self):

        mVert = mMesh.Vert(-1.1,2.2,0.5)
        vertPos = mVert.asVector()

        # X
        isequal, msg = mHelp.verifyEqual(vertPos,
                                         np.array([-1.1,2.2,0.5]),
                                         0.0001) # tol
        assert isequal, msg

    def test_translation(self):

        mVert = mMesh.Vert(-1.1,2.2,0.5)
        tVert = np.array([1.0,2.0,3.0])
        mVert.translate(tVert)

        # X
        isequal, msg = mHelp.verifyEqual(mVert.asVector(),
                                         np.array([-1.1,2.2,0.5]) + tVert,
                                         0.0001) # tol
        assert isequal, msg        

    def test_scale(self):

        mVert = mMesh.Vert(1.0,2.0,3.0)
        s     = 2
        mVert.scale(2)

        # X
        isequal, msg = mHelp.verifyEqual(mVert.asVector(),
                                         np.array([1.0,2.0,3.0]) * 2,
                                         0.0001) # tol
        assert isequal, msg        

    def test_rotationX(self):

        # Sample vector:
        mVert = mMesh.Vert(1.0,2.0,3.0)
        mVert.rotate(x_deg = 30)
            
        # Prepare rotation
        x_deg = 30
        x_rad = np.deg2rad(x_deg)

        cx    = np.cos(x_rad)
        sx    = np.sin(x_rad)

        r     = np.array([[ 1.0, 0.0, 0.0],
                          [ 0.0,  cx, -sx],
                          [ 0.0,  sx,  cx]])
        
        expVert = r @ np.array([1.0,2.0,3.0])

        # X
        isequal, msg = mHelp.verifyEqual(mVert.asVector(),
                                         expVert,
                                         0.0001) # tol
        assert isequal, msg

    def test_rotationY(self):

        # Sample vector:
        mVert = mMesh.Vert(1.0,2.0,3.0)
        mVert.rotate(y_deg = 30)
            
        # Prepare rotation
        y_deg = 30
        y_rad = np.deg2rad(y_deg)

        cy    = np.cos(y_rad)
        sy    = np.sin(y_rad)

        r     = np.array([[  cy, 0.0,  sy],
                          [ 0.0, 1.0, 0.0],
                          [ -sy, 0.0,  cy]])
        
        expVert = r @ np.array([1.0,2.0,3.0])

        # Y
        isequal, msg = mHelp.verifyEqual(mVert.asVector(),
                                         expVert,
                                         0.0001) # tol
        assert isequal, msg

    def test_rotationXY(self):

        # Sample vector:
        mVert = mMesh.Vert(1.0,2.0,3.0)
        mVert.rotate(x_deg = 10, y_deg = 20)
            
        # Prepare rotation
        x_deg = 10
        x_rad = np.deg2rad(x_deg)
        y_deg = 20
        y_rad = np.deg2rad(y_deg)

        cx    = np.cos(x_rad)
        sx    = np.sin(x_rad)
        cy    = np.cos(y_rad)
        sy    = np.sin(y_rad)

        rx    = np.array([[ 1.0, 0.0, 0.0],
                          [ 0.0,  cx, -sx],
                          [ 0.0,  sx,  cx]])
        
        ry    = np.array([[  cy, 0.0,  sy],
                          [ 0.0, 1.0, 0.0],
                          [ -sy, 0.0,  cy]])
        
        expVert = ry @ rx @ np.array([1.0,2.0,3.0])

        # XY
        isequal, msg = mHelp.verifyEqual(mVert.asVector(),
                                         expVert,
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
        mVertA = mMesh.Vert(0.0,1.0,0.0)
        mVertB = mMesh.Vert(1.0,0.0,0.0)

        mEdge = mMesh.Edge(mVertA,mVertB)

        # X
        verts = mEdge.getVerts()

        assert verts.a is mVertA
        assert verts.b is mVertB

    def test_plot(self):

        # Create edge from A/B
        mVert0 = mMesh.Vert( 0.5, 0.5, 0.0)
        mVert1 = mMesh.Vert( 0.5,-0.5, 0.0)
        mVert2 = mMesh.Vert(-0.5,-0.5, 0.0)
        mVert3 = mMesh.Vert(-0.5, 0.5, 0.0)

        mEdge1 = mMesh.Edge(mVert0,mVert1)
        mEdge2 = mMesh.Edge(mVert1,mVert2)
        mEdge3 = mMesh.Edge(mVert2,mVert3)
        mEdge4 = mMesh.Edge(mVert3,mVert0)

        # Create 3D plot
        fig = plt.figure()
        aH1 = fig.add_subplot(111, projection='3d')
        
        aH1.axis('equal')
        aH1.set_xlabel('x[m]')
        aH1.set_ylabel('y[m]')

        plt.ion()
        plt.show(block=False)

        mEdge1.plot(aH1)
        mEdge2.plot(aH1)
        mEdge3.plot(aH1)
        mEdge4.plot(aH1)

        plt.draw()
        plt.close(fig)

        assert True

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
        mVertA = mMesh.Vert(0.0,1.0,0.0)
        mVertB = mMesh.Vert(1.0,0.0,0.0)
        mVertC = mMesh.Vert(0.0,0.0,1.0)

        mFace = mMesh.Face((mVertA,mVertB,mVertC))

        # X
        verts = mFace.getVerts()

        assert verts[0] is mVertA
        assert verts[1] is mVertB        
        assert verts[2] is mVertC

    def test_4verts(self):

        # Create edge from A/B
        mVertA = mMesh.Vert(0.0,1.0,0.0)
        mVertB = mMesh.Vert(1.0,0.0,0.0)
        mVertC = mMesh.Vert(0.0,0.0,1.0)
        mVertD = mMesh.Vert(1.0,0.0,1.0)

        mFace = mMesh.Face((mVertA,mVertB,mVertC,mVertD))

        # X
        verts = mFace.getVerts()

        assert verts[0] is mVertA
        assert verts[1] is mVertB        
        assert verts[2] is mVertC        
        assert verts[3] is mVertD        

    def test_2verts(self):

        # Create edge from A/B
        mVertA = mMesh.Vert(0.0,1.0,0.0)
        mVertB = mMesh.Vert(1.0,0.0,0.0)

        with pytest.raises(AssertionError, match="at least 3 verts expected"):
            mFace = mMesh.Face((mVertA,mVertB))

    def test_vertIndex(self):

        # Create edge from A/B
        mVert0 = mMesh.Vert(0.0,1.0,0.0)
        mVert1 = mMesh.Vert(1.0,0.0,0.0)
        mVert2 = mMesh.Vert(0.0,0.0,1.0)
        mVert3 = mMesh.Vert(1.0,0.0,1.0)
        mVert4 = mMesh.Vert(1.0,0.0,1.0)
        mVert5 = mMesh.Vert(1.0,0.0,1.0)
        mVert6 = mMesh.Vert(1.0,0.0,1.0)
        mVert7 = mMesh.Vert(1.0,0.0,1.0)
        mVert8 = mMesh.Vert(1.0,0.0,1.0)
        mVert9 = mMesh.Vert(1.0,0.0,1.0)

        mFace = mMesh.Face((mVert3,mVert6,mVert7,mVert8))
        vertList = (mVert0,mVert1,mVert2,mVert3,mVert4,mVert5,
                    mVert6,mVert7,mVert8,mVert9)
        
        vertIndex = mMesh.Face.getVertIndex(mFace,vertList)

                # XY
        isequal, msg = mHelp.verifyEqual(vertIndex,
                                         (3,6,7,8),
                                         0.0001) # tol
        assert isequal, msg
    def test_plot(self):

        verts = [[0, 0, 0],
                 [1, 0, 0],
                 [1, 1, 0],
                 [0, 1, 0]]
            
        face = [verts]

        # Create edge from A/B
        mVert0 = mMesh.Vert(0.0,0.0,0.0)
        mVert1 = mMesh.Vert(0.0,1.0,0.0)
        mVert2 = mMesh.Vert(1.0,1.0,0.0)
        mVert3 = mMesh.Vert(1.0,0.0,0.0)

        mFace = mMesh.Face((mVert0,mVert1,mVert2,mVert3))

        # Create 3D plot
        fig = plt.figure()
        aH1 = fig.add_subplot(111, projection='3d')

        mFace.plot(aH1)

        # # Add the face to the plot
        # poly = Poly3DCollection(face, facecolors='skyblue', edgecolors='black', linewidths=1, alpha=0.8)
        # aH1.add_collection3d(poly)
        
        aH1.axis('equal')
        aH1.set_xlabel('x[m]')
        aH1.set_ylabel('y[m]')

        plt.ion()
        plt.show(block=False)
        

        plt.draw()
        plt.close(fig)

        assert True
        
class Test_Airfoil:
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
        airfoilA = mMesh.Airfoil(2,4, 5,40)
        airfoilB = mMesh.Airfoil(2,4,12,40)

        plt.style.use('fivethirtyeight')
        fH = plt.figure()
        aH1 = fH.add_subplot(2, 1, 1)
        aH1.axis('equal')
        aH1.set_xlabel('x[m]')
        aH1.set_ylabel('y[m]')

        aH2 = fH.add_subplot(2, 1, 2)
        aH2.axis('equal')
        aH2.set_xlabel('x[m]')
        aH2.set_ylabel('y[m]')

        plt.ion()
        plt.show(block=False)
        
        for iVertA,iVertB in zip(airfoilA.vertList(),airfoilB.vertList()):
            
            aH1.plot(iVertA.asVector()[0],
                     iVertA.asVector()[1],
                     linestyle='-',
                     marker='o',
                     color='b',
                     markerfacecolor='b',
                     markeredgecolor='b')
            
            aH2.plot(iVertB.asVector()[0],
                     iVertB.asVector()[1],
                     linestyle='-',
                     marker='o',
                     color='b',
                     markerfacecolor='b',
                     markeredgecolor='b')            

        plt.draw()
        plt.close(fH)

        assert True
        
    def test_translate(self):

        # Create edge from A/B
        airfoilA = mMesh.Airfoil(2,4,5,40)
        airfoilB = mMesh.Airfoil(2,4,5,40)

        airfoilB.translate(np.array([0.1,0.2,0.0]))

        plt.style.use('fivethirtyeight')
        fH = plt.figure()
        aH1 = fH.add_subplot(1, 1, 1)
        aH1.axis('equal')
        aH1.set_xlabel('x[m]')
        aH1.set_ylabel('y[m]')

        plt.ion()
        plt.show(block=False)
        
        for iVertA,iVertB in zip(airfoilA.vertList(),airfoilB.vertList()):
            aH1.plot(iVertA.asVector()[0],
                     iVertA.asVector()[1],
                     linestyle='-',
                     marker='o',
                     color='b',
                     markerfacecolor='b',
                     markeredgecolor='b')
            
            aH1.plot(iVertB.asVector()[0],
                     iVertB.asVector()[1],
                     linestyle='-',
                     marker='o',
                     color='1',
                     markerfacecolor='r',
                     markeredgecolor='r')

        plt.draw()
        plt.close(fH)

        assert True

    def test_scale(self):

        # Create edge from A/B
        airfoilA = mMesh.Airfoil(2,4,5,40)
        airfoilB = mMesh.Airfoil(2,4,5,40)

        airfoilB.scale(1.5)

        plt.style.use('fivethirtyeight')
        fH = plt.figure()
        aH1 = fH.add_subplot(1, 1, 1)
        aH1.axis('equal')
        aH1.set_xlabel('x[m]')
        aH1.set_ylabel('y[m]')

        plt.ion()
        plt.show(block=False)
        
        for iVertA,iVertB in zip(airfoilA.vertList(),airfoilB.vertList()):
            aH1.plot(iVertA.asVector()[0],
                     iVertA.asVector()[1],
                     linestyle='-',
                     marker='o',
                     color='b',
                     markerfacecolor='b',
                     markeredgecolor='b')
            
            aH1.plot(iVertB.asVector()[0],
                     iVertB.asVector()[1],
                     linestyle='-',
                     marker='o',
                     color='1',
                     markerfacecolor='r',
                     markeredgecolor='r')

        plt.draw()
        plt.close(fH)

        assert True

    def test_rotate(self):

        # Create edge from A/B
        airfoilA = mMesh.Airfoil(2,4,5,40)
        airfoilB = mMesh.Airfoil(2,4,5,40)

        airfoilB.rotate(z_deg = 30)

        plt.style.use('fivethirtyeight')
        fH = plt.figure()
        aH1 = fH.add_subplot(1, 1, 1)
        aH1.axis('equal')
        aH1.set_xlabel('x[m]')
        aH1.set_ylabel('y[m]')

        plt.ion()
        plt.show(block=False)
        
        for iVertA,iVertB in zip(airfoilA.vertList(),airfoilB.vertList()):
            aH1.plot(iVertA.asVector()[0],
                     iVertA.asVector()[1],
                     linestyle='-',
                     marker='o',
                     color='b',
                     markerfacecolor='b',
                     markeredgecolor='b')
            
            aH1.plot(iVertB.asVector()[0],
                     iVertB.asVector()[1],
                     linestyle='-',
                     marker='o',
                     color='1',
                     markerfacecolor='r',
                     markeredgecolor='r')

        plt.draw()
        plt.close(fH)

        assert True

    def test_rotateAtPoint(self):

        # Create edge from A/B
        airfoilA = mMesh.Airfoil(0,0,10,40)
        airfoilB = mMesh.Airfoil(0,0,10,40)

        airfoilB.rotateAtPoint(z_deg = 10,
                               t = np.array([0.25,0,0]))

        plt.style.use('fivethirtyeight')
        fH = plt.figure()
        aH1 = fH.add_subplot(1, 1, 1)
        aH1.axis('equal')
        aH1.set_xlabel('x[m]')
        aH1.set_ylabel('y[m]')

        plt.ion()
        plt.show(block=False)
        
        for iVertA,iVertB in zip(airfoilA.vertList(),airfoilB.vertList()):
            aH1.plot(iVertA.asVector()[0],
                     iVertA.asVector()[1],
                     linestyle='-',
                     marker='o',
                     color='b',
                     markerfacecolor='b',
                     markeredgecolor='b')
            
            aH1.plot(iVertB.asVector()[0],
                     iVertB.asVector()[1],
                     linestyle='-',
                     marker='o',
                     color='1',
                     markerfacecolor='r',
                     markeredgecolor='r')

        plt.draw()
        plt.close(fH)

        assert True

    def test_link(self):

        # Create edge from A/B
        airfoilA = mMesh.Airfoil(0,0,10,40)
        airfoilB = mMesh.Airfoil(0,0,10,40)

        airfoilB.translate(np.array([0.0,0.5,0.0]))

        (faceList,edgeList) = mMesh.Airfoil.link(airfoilA,airfoilB)

        plt.style.use('fivethirtyeight')
        fH = plt.figure()
        aH1 = fH.add_subplot(111, projection='3d')

        aH1.set_xlabel('x[m]')
        aH1.set_ylabel('y[m]')

        plt.ion()
        plt.show(block=False)

        # Plot airfoils
        airfoilA.plot(aH1)
        airfoilB.plot(aH1)

        aH1.set_xlim( 1.1,-0.1)
        aH1.set_ylim( 0.6,-0.6)
        aH1.set_zlim(-0.6, 0.6)
        aH1.view_init(elev=20,
                      azim=-70)
        
        for iFace in faceList:
            iFace.plot(aH1)

        for iEdge in edgeList:
            iEdge.plot(aH1)            

        plt.draw()
        plt.close(fH)

        assert True

    def test_disp(self):

        # Create edge from A/B
        airfoilA = mMesh.Airfoil(2,4,5,10)
        airfoilA.disp()

        assert True

    def test_plot(self):

        # Create edge from A/B
        airfoilA = mMesh.Airfoil(2,4,5,10)

        # Create 3D plot
        fig = plt.figure()
        aH1 = fig.add_subplot(111, projection='3d')
        
        aH1.axis('equal')
        aH1.set_xlabel('x[m]')
        aH1.set_ylabel('y[m]')

        plt.ion()
        plt.show(block=False)

        airfoilA.plot(aH1)

        aH1.set_xlim( 1.1,-0.1)
        aH1.set_ylim( 0.6,-0.6)
        aH1.set_zlim(-0.6, 0.6)
        aH1.view_init(elev=0,
                      azim=-90)
        
        plt.draw()
        plt.close(fig)

        assert True

class Test_Cube:
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

        origin = np.array([1.0,1.0,1.0])
        mCube = mMesh.Cube(size = 1,
                           origin = origin)
        # X
        faces = mCube.getFaces()

        # Create 3D plot
        fH = plt.figure()
        aH1 = fH.add_subplot(111, projection='3d')
        aH1.set_xlabel('x[m]')
        aH1.set_ylabel('y[m]')

        plt.ion()
        plt.show(block=False)

        aH1.scatter(origin[0], origin[1], origin[2], color='blue', s=25)
        for iFace in faces:
            iFace.plot(aH1)

        plt.draw()
        plt.close(fH)

        assert True

class Test_Wing:
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

        # Create simple wing:
        aWing = mMesh.Wing('testWing', # name
                           0.0, # startX_m
                           0.0, # startY_m: float,
                           0.0, # startZ_m: float,
                           1.0, # rootChord_m
                           np.array([2.0,2.0]), # M
                           np.array([4.0,4.0]), # P
                           np.array([12.0,12.0]), # XX
                           np.array([0.0,0.0]), # twist_deg
                           np.array([0.0,0.0]), # dihed_deg
                           np.array([1.0,1.0]), # b_m
                           np.array([1.0,1.0]), # taperRatio
                           np.array([0.0,0.0]), # sweep_deg
                           50) # nPoint

        assert True