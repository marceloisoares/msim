from collections    import namedtuple
import numpy        as np
import msim.lib     as mlib
import msim.helpers as mHelp
# -------------------------------------------------------------------------
# Ports
# -------------------------------------------------------------------------

class Test_Outport:
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
        out1 = mlib.Outport(float,[])

        assert out1.getType() is float

    def test_connect(self):
        # First connection:
        outTier1 = mlib.Outport(float,[])
        outTier2 = mlib.Outport(float,[])
        outTier3 = mlib.Outport(float,[])
        
        outTier3.connectTo(outTier2)
        assert outTier3.getSource() == outTier2

        # Cascaded connections:
        outTier2.connectTo(outTier1)
        assert outTier2.getSource() == outTier1
        assert outTier3.getSource() == outTier1

    def test_dataflow(self):
        # Create and connect sources:
        outTier1 = mlib.Outport(float,[])
        outTier2 = mlib.Outport(float,[])
        outTier3 = mlib.Outport(float,[])

        outTier3.connectTo(outTier2)
        outTier2.connectTo(outTier1)

        # Force value on tier 1:
        outTier1.setValue(2.0)

        assert outTier2.getValue() == 2.0
        assert outTier3.getValue() == 2.0

class Test_Inport:
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
        in1 = mlib.Inport(float,[])

        assert in1.getType() is float

    def test_connect(self):
        # First connection:
        outSource = mlib.Outport(float,[])
        inTier1   = mlib.Inport(float,[])
        inTier2   = mlib.Inport(float,[])
        inTier3   = mlib.Inport(float,[])
        
        inTier3.connectTo(inTier2)
        assert inTier3.getSource() == inTier2

        inTier2.connectTo(inTier1)
        assert inTier2.getSource() == inTier1
        assert inTier3.getSource() == inTier1

        inTier1.connectTo(outSource)
        assert inTier1.getSource() == outSource
        assert inTier2.getSource() == outSource
        assert inTier3.getSource() == outSource

    def test_dataflow(self):
        # Create and connect sources:
        outSource = mlib.Outport(float,[])
        inTier1   = mlib.Inport(float,[])
        inTier2   = mlib.Inport(float,[])
        inTier3   = mlib.Inport(float,[])

        # Make connections:
        inTier3.connectTo(inTier2)
        inTier2.connectTo(inTier1)
        inTier1.connectTo(outSource)
        
        # Force value on tier 1:
        outSource.setValue(2.0)

        assert outSource.getValue() == 2.0
        assert inTier1.getValue()   == 2.0
        assert inTier2.getValue()   == 2.0
        assert inTier3.getValue()   == 2.0
        
# -------------------------------------------------------------------------
# Blocks
# -------------------------------------------------------------------------

class Test_Constant:
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
        const1 = mlib.Constant('const1',float,2.0,None)

        assert const1.getName()         == 'const1'
        assert const1.getBlockType()    == 'Constant'

        assert const1.getInportNames()  == [   ]
        assert const1.getOutportNames() == ['y']
    
    def test_connect(self):
        const1 = mlib.Constant('const1',float,2.0,None)
        
        # First connection:
        outTest   = mlib.Outport(float,None)
        outSource = mlib.Outport(float,None)

        outTest.connectTo(const1.getOutport('y'))

        # Execute model:
        const1.execute()
        const1.update()

        assert outTest.getValue() == 2.0

    def test_run(self):
        const1 = mlib.Constant('const1',# name
                               float,   # type
                               2.0,     # aGain
                               None)    # parent

        simIn = dict()
        simIn['time'] = np.arange(0.0,2.0,0.1,dtype=float)
        simOut        = const1.sim(simIn)

        outExpect     = np.ones_like(simIn['time']) * 2.0

        isEqual, msg = mHelp.verifyEqual(simOut['y'],
                                         outExpect,
                                         0.001) # tol
        assert isEqual, msg

class Test_Gain:
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
        gain1 = mlib.Gain('gain1',float,2.0,None)

        assert gain1.getName()         == 'gain1'
        assert gain1.getBlockType()    == 'Gain'

        assert gain1.getInportNames()  == ['u']
        assert gain1.getOutportNames() == ['y']
    
    def test_connect(self):
        gain1 = mlib.Gain('gain1',float,2.0,None)
        
        # First connection:
        outTest   = mlib.Outport(float,None)
        outSource = mlib.Outport(float,None)

        outTest.connectTo(gain1.getOutport('y'))
        gain1.getInport('u').connectTo(outSource)

        # Execute model:
        outSource.setValue(2.0)
        gain1.execute()

        assert outTest.getValue() == 4.0

    def test_run(self):
        gain1 = mlib.Gain('gain1', # name
                          float,   # type
                          2.0,     # aGain
                          None)    # parent

        simIn = dict()
        simIn['time'] = np.arange(0.0,2.0,0.1,dtype=float)
        simIn['u']    = simIn['time'] ** 2
        simOut        = gain1.sim(simIn)

        outExpect     = simIn['u'] * 2.0

        isEqual, msg = mHelp.verifyEqual(simOut['y'],
                                         outExpect,
                                         0.001) # tol
        assert isEqual, msg

class Test_Delay:
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
        delay1 = mlib.Delay('delay1',float,2.0,None)

        assert delay1.getName()         == 'delay1'
        assert delay1.getBlockType()    == 'Delay'

        assert delay1.getInportNames()  == ['u']
        assert delay1.getOutportNames() == ['y']
    
    def test_connect(self):
        delay1 = mlib.Delay('delay1',float,2.0,None)
        
        # First connection:
        # [outSource]--->[Delay]--->[outTest]
        outSource = mlib.Outport(float,None)
        outTest   = mlib.Outport(float,None)
        

        outTest.connectTo(delay1.getOutport('y'))
        delay1.getInport('u').connectTo(outSource)

        # Execute model:
        outSource.setValue(4.0)
        delay1.execute()

        assert outTest.getValue() == 2.0

        # Execute one cycle:
        delay1.update()
        outSource.setValue(8.0)
        delay1.execute()
    
        assert outTest.getValue() == 4.0
        
    def test_run(self):
        delay1 = mlib.Delay('delay1',# name
                            float,   # type
                           2.0,      # aInitValue
                           None)     # parent

        simIn = dict()
        simIn['time'] = np.arange(0.0,2.0,0.1,dtype=float)
        simIn['u']    = np.arange(len(simIn['time']),dtype=float)
        simOut        = delay1.sim(simIn)

        outExpect     = np.roll(simIn['u'],1)
        outExpect[0]  = 2.0

        isEqual, msg = mHelp.verifyEqual(simOut['y'],
                                         outExpect,
                                         0.001) # tol
        assert isEqual, msg

class Test_Switch:
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
        switch1 = mlib.Switch('switch1',float,None)

        assert switch1.getName()         == 'switch1'
        assert switch1.getBlockType()    == 'Switch'

        assert switch1.getInportNames()  == ['on', 'off', 'sw']
        assert switch1.getOutportNames() == ['y']
    
    def test_connect(self):
        switch1 = mlib.Switch('switch1',float,None)
        
        # [onSource]--->
        # [swSource]--->[Switch]--->[outTest]
        # [offSource]-->
        swSource  = mlib.Outport(bool,None)
        onSource  = mlib.Outport(float,None)
        offSource = mlib.Outport(float,None)

        outTest   = mlib.Outport(float,None)

        outTest.connectTo(switch1.getOutport('y'))
        switch1.getInport('on').connectTo(onSource)
        switch1.getInport('off').connectTo(offSource)
        switch1.getInport('sw').connectTo(swSource)

        # Execute model:
        onSource.setValue(2.0)
        offSource.setValue(-2.0)
        swSource.setValue(True)
        switch1.execute()
        
        assert outTest.getValue() == 2.0

        # Execute one cycle:
        switch1.update()
        swSource.setValue(False)
        switch1.execute()
    
        assert outTest.getValue() == -2.0
        
    def test_run(self):
        switch1 = mlib.Switch('Switch1',# name
                              float,   # type
                              None)     # parent

        simIn = dict()
        time = np.arange(0.0,2.0,0.1,dtype=float)
        uOn  = np.arange(len(time),dtype=float)
        uOff = uOn -1
        sw   = np.random.randint(0,2,
                                 size=time.shape,
                                 dtype=bool)
        
        simIn['time'] = time
        simIn['on']   = uOn
        simIn['off']  = uOff
        simIn['sw']   = sw

        simOut        = switch1.sim(simIn)

        outExpect     = uOff
        outExpect[sw] = uOn[sw]

        isEqual, msg = mHelp.verifyEqual(simOut['y'],
                                         outExpect,
                                         0.001) # tol
        assert isEqual, msg        

class Test_Sum:
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
        sum1 = mlib.Sum('sum1',float,'+-+',None)

        assert sum1.getName()         == 'sum1'
        assert sum1.getBlockType()    == 'Sum'

        assert sum1.getInportNames()  == ['u0', 'u1', 'u2']
        assert sum1.getOutportNames() == ['y']
    
    def test_connect(self):
        sum1 = mlib.Sum('sum1',float,'+-+',None)
        
        # [u0Source]--->
        # [u1Source]--->[Sum]--->[outTest]
        # [u2Source]--->
        u0Source = mlib.Outport(float,None)
        u1Source = mlib.Outport(float,None)
        u2Source = mlib.Outport(float,None)

        outTest   = mlib.Outport(float,None)

        outTest.connectTo(sum1.getOutport('y'))
        sum1.getInport('u0').connectTo(u0Source)
        sum1.getInport('u1').connectTo(u1Source)
        sum1.getInport('u2').connectTo(u2Source)

        # Execute model:
        u0Source.setValue(1.0)
        u1Source.setValue(2.0)
        u2Source.setValue(3.0)
        sum1.execute()
        
        assert outTest.getValue() == 2.0

        # Execute one cycle:
        sum1.update()
        u2Source.setValue(4.0)
        sum1.execute()
    
        assert outTest.getValue() == 3.0
    
    def test_run(self):
        sum1 = mlib.Sum('sum1',float,'+-+',None)

        simIn = dict()
        time = np.arange(0.0,2.0,0.1,dtype=float)
        u0  = np.random.randint(-100,100,
                                size=time.shape,
                                dtype=int)
        u1  = np.random.randint(-100,100,
                                size=time.shape,
                                dtype=int)
        u2  = np.random.randint(-100,100,
                                size=time.shape,
                                dtype=int)
        simIn['time'] = time
        simIn['u0']   = u0
        simIn['u1']   = u1
        simIn['u2']   = u2

        simOut        = sum1.sim(simIn)
        #Check results:
        outExpect     = u0 - u1 + u2

        isEqual, msg = mHelp.verifyEqual(simOut['y'],
                                         outExpect,
                                         0.001) # tol
        assert isEqual, msg        

class Test_Logical:
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
        or1 = mlib.Logical('or1','or',None)

        assert or1.getName()         == 'or1'
        assert or1.getBlockType()    == 'Logical'

        assert or1.getInportNames()  == ['u0','u1']
        assert or1.getOutportNames() == ['y']
    
    def test_connect(self):
        or1 = mlib.Logical('or1','or',None)
        
        # [u0Source]--->
        # [u1Source]--->[Logical]--->[outTest]

        # First connection:
        outTest  = mlib.Outport(bool,None)
        u0Source = mlib.Outport(bool,None)
        u1Source = mlib.Outport(bool,None)

        outTest.connectTo(or1.getOutport('y'))
        or1.getInport('u0').connectTo(u0Source)
        or1.getInport('u1').connectTo(u1Source)

        # Execute model:
        u0Source.setValue(True)
        u1Source.setValue(False)
        or1.execute()

        assert outTest.getValue() == True

        # Execute model:
        or1.update()
        u0Source.setValue(False)
        u1Source.setValue(False)
        or1.execute()

        assert outTest.getValue() == False

    def test_run(self):
        and1 = mlib.Logical('and1','and',None)

        time = np.arange(0.0,2.0,0.1,dtype=float)
        u0  = np.random.randint(0,2,
                                 size=time.shape,
                                 dtype=bool)
        u1  = np.random.randint(0,2,
                                 size=time.shape,
                                 dtype=bool)
        simIn = dict()
        simIn['time'] = time
        simIn['u0']   = u0
        simIn['u1']   = u1

        simOut        = and1.sim(simIn)
        outExpect     = np.logical_and(u0,u1)
        
        assert all(simOut['y'] == outExpect)