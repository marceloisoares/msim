# [Description]: 
#   - This module includes the msim primities (ports, gains, basic blocks)

# -------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------

# Abstract base class
from abc import ABC, abstractmethod

from msim import helpers as mhelp
# -------------------------------------------------------------------------
# Ports
# -------------------------------------------------------------------------

class Port(ABC):

    def __init__(self,aName: str,aType: any, aParent) -> None:
        # Basic properties:
        self._name   = aName
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

    def getName(self):
        return self._name
    
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

    def __init__(self,aName: str,aType: str, aParent) -> None:

        # Use constructor only:
        Port.__init__(self,aName,aType,aParent)

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

    def __init__(self,aName: str,aType: str, aParent) -> None:

        # Use constructor only:
        Port.__init__(self,aName,aType,aParent)

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
        for iPort in self._inports:
            if(iPort.getName() == aName):
                return iPort

    def getInportNames(self):
        blockInports = [iPort.getName() for iPort in self._inports]
        return blockInports

    def getOutport(self, aName):
        for iPort in self._outports:
            if(iPort.getName() == aName):
                return iPort

    def getOutportNames(self):
        blockOutports = [iPort.getName() for iPort in self._outports]
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
        self._inports   = []
        self._outports  = [Outport('y',aType,aParent)]
        self._subBlocks = []

        self._outports[0].setValue(aValue)

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
        self._inports   = [Inport ('u', aType,aParent)]
        self._outports  = [Outport('y',aType,aParent)]
        self._subBlocks = []

    # -----------------
    # Output and update
    # -----------------
    def execute(self):
        # Process inports:
        out = self._inports[0].getValue() * self._gain
        self._outports[0].setValue(out)
        
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
        self._inports   = [Inport ('u', aType,aParent)]
        self._outports  = [Outport('y',aType,aParent)]
        self._subBlocks = []

        self._outports[0].setValue(aInitValue)

    # -----------------
    # Output and update
    # -----------------
    def execute(self):
        # Process inports:
        self._internalValue =self._inports[0].getValue()
        
    def update(self):
        # Do nothing
        self._outports[0].setValue(self._internalValue)
                