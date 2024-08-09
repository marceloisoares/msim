import msim.helpers as mHelp
import msim.lib as mlib

class Test_isMsimNumType:
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

    def test_bool(self):
        result = mHelp.isMsimNumType(bool)
        assert result

    def test_int(self):
        result = mHelp.isMsimNumType(int)
        assert result

    def test_float(self):
        result = mHelp.isMsimNumType(float)
        assert result

    def test_str(self):
        result = mHelp.isMsimNumType(str)
        assert not result

class Test_dispPortStatus:
    def setup_class(self):
        # Class setup:
        out1 = mlib.Outport('out1',float,[])
        out2 = mlib.Outport('out2',float,[])
        out3 = mlib.Outport('out3',float,[])
        self._outports = [out1,out2,out3]

        in1 = mlib.Inport('in1',float,[])
        in2 = mlib.Inport('in2',float,[])
        in3 = mlib.Inport('in3',float,[])
        self._inports = [in1,in2,in3]

        # Connect inports to outport:
        in1.connectTo(out1)
        in2.connectTo(out2)
        in3.connectTo(out3)

        # Set sample values:
        out1.setValue(1.0)
        out2.setValue(2.0)
        out3.setValue(3.0)
        
    def teardown_class(self):
        # Class teardown:
        pass

    def setup(self):
        # Method setup:
        pass

    def teardown(self):
        # Method teardown:
        pass

    def test_dispOutports(self):
        result = mHelp.dispPortStatus(self._outports)
        assert True

    def test_dispInports(self):
        result = mHelp.dispPortStatus(self._inports)
        assert True        

class Test_simData:
    def setup_class(self):
        # Class setup:
        data = {'time': [0.0, 0.1, 0.2, 0.3,  0.4,  0.5],
                'a'   : [0.0, 1.0, 2.0, 3.0,  4.0,  5.0],
                'b'   : [6.0, 7.0, 8.0, 9.0, 10.0, 11.0]}


        self.simExample = mHelp.simData(**data)

    def teardown_class(self):
        # Class teardown:
        pass

    def setup(self):
        # Method setup:
        pass

    def teardown(self):
        # Method teardown:
        pass

    def test_SignalNames(self):
        result = self.simExample.getSignalNames()
        assert result == ['time','a','b']

    def test_SignalData(self):

        resultT = self.simExample.getSignalData('time')    
        assert resultT == [0.0, 0.1, 0.2, 0.3,  0.4,  0.5]

        resultA = self.simExample.getSignalData('a')    
        assert resultA == [0.0, 1.0, 2.0, 3.0,  4.0,  5.0]

        resultB = self.simExample.getSignalData('b')    
        assert resultB == [6.0, 7.0, 8.0, 9.0, 10.0, 11.0]

    def test_SignalSample(self):

        resultT0 = self.simExample.getSignalSample('time',0)    
        assert resultT0 == 0.0

        resultT1 = self.simExample.getSignalSample('time',1)    
        assert resultT1 == 0.1

        resultA0 = self.simExample.getSignalSample('a',0)    
        assert resultA0 == 0.0

        resultA = self.simExample.getSignalSample('a',1)    
        assert resultA == 1.0

class Test_assertEqual:
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

    def test_equal(self):
        listA = [0.0, 1.0, 2.0]
        listB = [0.0, 1.0, 2.0]

        isEqual, msg = mHelp.verifyEqual(listA,listB,0.001)
        assert isEqual, msg

    def test_notEqual(self):
        # Ensure error is detected
        listA = [0.0, 1.0, 2.0]
        listB = [0.0, 1.0, 2.01]

        isEqual, msg = mHelp.verifyEqual(listA,listB,0.001)
        assert not isEqual
        assert msg == 'Index [2]: 2.0 is not equal to 2.01'
        