# [Description]: 
#   - This module includes the msim primities (ports, gains, basic blocks)

# -------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------

# Abstract base class
from   abc   import ABC, abstractmethod
import numpy as     np

from msim import helpers as mhelp
# -------------------------------------------------------------------------
# Ports
# -------------------------------------------------------------------------

class Port(ABC):

    def __init__(self,aType: any, aParent) -> None:
        # Basic properties:
        self._parent = aParent

        # Ensure data type is valid:
        assert mhelp.isMsimNumType(aType)
        self._type   = aType

        # Port from where value is extract
        self._sourcePort = None

        # Subscribers listening this port:
        self._subscribers = []

    # -------------
    # Get/set
    # -------------
        
    # Basic methods
    @abstractmethod
    def getValue(self):
        pass
    
    def getType(self):
        return self._type

    def getSource(self):
        return self._sourcePort
    # -------------
    # Connectivity
    # -------------
    def setSource(self,aPort):
        self._sourcePort = aPort

    def connectTo(self,aSource:'Port'):

        # Ensure ports have the same type:
        assert self.getType() is aSource.getType()

        # Transfer all subscribers to new source
        for iSub in self._subscribers:
            # Transfer to the new source
            iSub.setSource(aSource)

            # Let source know the new subscribers:
            aSource.addSubscriber(iSub)
        self._subscribers.clear()

        # Update its own source
        self.setSource(aSource)
        aSource.addSubscriber(self)

    def addSubscriber(self,aPort:'Port'):
        self._subscribers.append(aPort)

class Outport(Port):

    def __init__(self,aType: str, aParent) -> None:

        # Use constructor only:
        Port.__init__(self,aType,aParent)

    def setValue(self,aValue):
        # Ensure the port is not connected
        assert self._sourcePort is None
        self._value = aValue

    def getValue(self):
        # Return local value if not connected:
        if(self._sourcePort is None):
            return self._value
        else:
            return self._sourcePort.getValue()

        # Ensure the port is not connected
        assert self._sourcePort is None
        self._value = aValue

class Inport(Port):

    def __init__(self,aType: str, aParent) -> None:

        # Use constructor only:
        Port.__init__(self,aType,aParent)

    def getValue(self):
        # Return local value if not connected:
        assert self._sourcePort is not None
        return self._sourcePort.getValue()

# -------------------------------------------------------------------------
# Blocks:
# -------------------------------------------------------------------------

class Block(ABC):

    def __init__(self):
        # Basic properties:
        self._name      = None
        self._blockType = None
        self._parent    = None

        # Functional
        self._inports   = []
        self._outports  = []
        self._subBlocks = []

    # -------------
    # Get/set
    # -------------
    def getName(self):
        return self._name

    def getBlockType(self):
        return self._blockType

    def getOutportValue(self, aName):
        iPort = self.getOutport(aName).getValue()

    def getInportValue(self, aName):
        iPort = self.getInport(aName).getValue()            

    def getInport(self, aName):
        return self._inports[aName]

    def getInportNames(self):
        blockInports = list(self._inports.keys())
        return blockInports

    def getOutport(self, aName):
        return self._outports[aName]

    def getOutportNames(self):
        blockOutports = list(self._outports.keys())
        return blockOutports
    
    # -------------------
    # Connectivity:
    #  ------------------- 
    def connectTo(self, inportName: str, aSourcePort: Port):
        self.getInport(inportName).connectTo(aSourcePort)

    # -------------------
    # Helper methods:
    #  ------------------- 
    def dispOutport(self):
        mhelp.dispPortStatus(self._outports)

    def dispInport(self):
        mhelp.dispPortStatus(self._inports)

    # -------------------
    # Simulate:
    #  -------------------
    def sim(self, simIn):
        return mhelp.run(self,simIn)

    @abstractmethod
    def execute(self):
        # Implement by each block
        pass

    @abstractmethod
    def update(self):
        # Implement by each block
        pass
    
class Constant(Block):

    def __init__(self,aName, aType, aValue, aParent):

        # Create empty properties
        Block.__init__(self)

        # Basic properties:
        self._name      = aName
        self._blockType = 'Constant'
        self._parent    = aParent

        # Ensure type is valid:
        assert mhelp.isMsimNumType(aType)
        self._type    = aType

        # Inputs/Outports:
        self._inports   = {}
        self._outports  = {'y':Outport(aType,aParent)}
        self._subBlocks = {}

        self._outports['y'].setValue(aValue)

    # -----------------
    # Output and update
    # -----------------
    def execute(self):
        # Do nothing
        pass
        
    def update(self):
        # Do nothing
        pass

class Gain(Block):

    def __init__(self,aName, aType, aGain, aParent):

        # Create empty properties
        Block.__init__(self)

        # Basic properties:
        self._name      = aName
        self._blockType = 'Gain'
        self._parent    = aParent
        self._gain      = aGain

        # Ensure type is valid:
        assert mhelp.isMsimNumType(aType)

        # Inputs/Outports:
        self._inports   = {'u':Inport (aType,aParent)}
        self._outports  = {'y':Outport(aType,aParent)}
        self._subBlocks = {}

    # -----------------
    # Output and update
    # -----------------
    def execute(self):
        # Process inports:
        out = self._inports['u'].getValue() * self._gain
        self._outports['y'].setValue(out)
        
    def update(self):
        # Do nothing
        pass
        
class Delay(Block):

    def __init__(self,aName, aType, aInitValue, aParent):

        # Create empty properties
        Block.__init__(self)

        # Basic properties:
        self._name      = aName
        self._blockType = 'Delay'
        self._parent    = aParent

        # Ensure type is valid:
        assert mhelp.isMsimNumType(aType)

        # Inputs/Outports:
        self._inports   = {'u':Inport (aType,aParent)}
        self._outports  = {'y':Outport(aType,aParent)}
        self._subBlocks = {}

        self._outports['y'].setValue(aInitValue)

    # -----------------
    # Output and update
    # -----------------
    def execute(self):
        # Process inports:
        self._internalValue =self._inports['u'].getValue()
        
    def update(self):
        # Do nothing
        self._outports['y'].setValue(self._internalValue)
                
class Switch(Block):

    def __init__(self,aName, aType, aParent):

        # Create empty properties
        Block.__init__(self)

        # Basic properties:
        self._name      = aName
        self._blockType = 'Switch'
        self._parent    = aParent

        # Ensure type is valid:
        assert mhelp.isMsimNumType(aType)

        # Inputs/Outports:
        uOn  = Inport (aType,aParent)
        uOff = Inport (aType,aParent)
        sw   = Inport (bool,aParent)
        y    = Outport (aType,aParent)

        self._inports   = {'on':uOn, 'off':uOff, 'sw':sw}
        self._outports  = {'y' :y}
        self._subBlocks = {}

    # -----------------
    # Output and update
    # -----------------
    def execute(self):
        # Process inports:
        if(self._inports['sw'].getValue()):
            u = self._inports['on'].getValue()
        else:
            u = self._inports['off'].getValue()
        self._outports['y'].setValue(u)

    def update(self):
        # Do nothing
        pass


class Sum(Block):

    def __init__(self,aName, aType,aOperators,aParent):

        # Create empty properties
        Block.__init__(self)

        # Basic properties:
        self._name      = aName
        self._blockType = 'Sum'
        self._parent    = aParent

        # Ensure type is valid:
        assert mhelp.isMsimNumType(aType)

        # Create inport for each operator:
        self._inports    = dict()
        self._operatorsH = [np.add] * len(aOperators)
        for i,operator in enumerate(aOperators):
            assert operator in ['+','-']
            if(operator == '+'):
                self._operatorsH[i] = np.add
            else:
                self._operatorsH[i] = np.subtract

            inportName = 'u' + str(i)
            inPort = Inport (aType,aParent)
            self._inports.update({inportName:inPort})
            
        y    = Outport (aType,aParent)
        self._outports  = {'y' :y}
        self._subBlocks = {}

    # -----------------
    # Output and update
    # -----------------
    def execute(self):

        # Update output:
        result = 0
        for i,aPort in enumerate(self._inports.values()):
            operator = self._operatorsH[i]
            result = operator(result,aPort.getValue())
        
        self._outports['y'].setValue(result)

    def update(self):
        # Do nothing
        pass

class Logical(Block):

    def __init__(self,aName,aOperator,aParent):

        # Create empty properties
        Block.__init__(self)

        # Basic properties:
        self._name      = aName
        self._blockType = 'Logical'
        self._parent    = aParent

        assert aOperator in ['and','or','xor']
        if(aOperator == 'and'):
            self._operatorH = np.logical_and
        elif(aOperator == 'or'):
            self._operatorH = np.logical_or
        else:
            self._operatorH = np.logical_xor

        # Inputs/Outports:
        u0 = Inport(bool,aParent)
        u1 = Inport(bool,aParent)
        y  = Outport(bool,aParent)

        self._inports   = {'u0':u0, 'u1':u1}
        self._outports  = {'y' :y}
        self._subBlocks = {}

    # -----------------
    # Output and update
    # -----------------
    def execute(self):

        # Update output:
        result = self._operatorH(self._inports['u0'].getValue(),
                                 self._inports['u1'].getValue())
        self._outports['y'].setValue(result)

    def update(self):
        # Do nothing
        pass    