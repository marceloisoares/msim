import msim.lib as mlib

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
        out1 = mlib.Outport('out1',float,[])

        assert out1.getName() == 'out1'
        assert out1.getType() is float

    def test_connect(self):
        # First connection:
        outTier1 = mlib.Outport('outTier1',float,[])
        outTier2 = mlib.Outport('outTier2',float,[])
        outTier3 = mlib.Outport('outTier3',float,[])
        
        outTier3.connectTo(outTier2)
        assert outTier3.getSource() == outTier2

        # Cascaded connections:
        outTier2.connectTo(outTier1)
        assert outTier2.getSource() == outTier1
        assert outTier3.getSource() == outTier1

    def test_dataflow(self):
        # Create and connect sources:
        outTier1 = mlib.Outport('outTier1',float,[])
        outTier2 = mlib.Outport('outTier2',float,[])
        outTier3 = mlib.Outport('outTier3',float,[])

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
        in1 = mlib.Inport('in1',float,[])

        assert in1.getName() == 'in1'
        assert in1.getType() is float

    def test_connect(self):
        # First connection:
        outSource = mlib.Outport('outSource',float,[])
        inTier1   = mlib.Inport('inTier1',float,[])
        inTier2   = mlib.Inport('inTier2',float,[])
        inTier3   = mlib.Inport('inTier3',float,[])
        
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
        outSource = mlib.Outport('outSource',float,[])
        inTier1   = mlib.Inport('inTier1',float,[])
        inTier2   = mlib.Inport('inTier2',float,[])
        inTier3   = mlib.Inport('inTier3',float,[])

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

        assert gain1.getName() == 'gain1'
        assert gain1.getBlockType() == 'Gain'

    def test_connect(self):
        gain1 = mlib.Gain('gain1',float,2.0,None)
        
        # First connection:
        outTest   = mlib.Outport('outTest',float,None)
        outSource = mlib.Outport('outSource',float,None)

        outTest.connectTo(gain1.getOutport('out'))
        gain1.getInport('in').connectTo(outSource)

        # Execute model:
        outSource.setValue(2.0)
        gain1.execute()

        assert outTest.getValue() == 4.0

    def test_dataflow(self):
        # Create and connect sources:
        outTier1 = mlib.Outport('outTier1',float,[])
        outTier2 = mlib.Outport('outTier2',float,[])
        outTier3 = mlib.Outport('outTier3',float,[])

        outTier3.connectTo(outTier2)
        outTier2.connectTo(outTier1)

        # Force value on tier 1:
        outTier1.setValue(2.0)

        assert outTier2.getValue() == 2.0
        assert outTier3.getValue() == 2.0