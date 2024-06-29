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



