# [Description]: Helper function to support pysim
from   collections import namedtuple
import numpy       as np
import msim.lib    as     mlib
import mypy

# -------------------------------------------------------------------------
# Supporting functions
# -------------------------------------------------------------------------

def isMsimNumType(aType: any) -> bool:
    return aType is bool or \
           aType is int  or \
           aType is float

# -------------
# Blocks
# -------------

def dispPortStatus(aPortList: list):
    # [Description]: Display the port status of all ports. Typically used for
    #                debugging purposes
    maxChar = 24
    barStr  = '-' * 76

    titleStr = '|' + \
               str.center('Name', maxChar)  + '|' + \
               str.center('Type', maxChar)  + '|' + \
               str.center('Value', maxChar) + '|'
    
    print('')
    print(barStr)
    print(titleStr)
    print(barStr)
    
    # Print status of each port:
    for iPort in aPortList:
        cName  = iPort.getName()
        cType  = str(iPort.getType())
        cValue = str(iPort.getValue())

        listStr = '|' + \
                  str.center(cName,maxChar)  + '|' + \
                  str.center(cType,maxChar)  + '|' + \
                  str.center(cValue,maxChar) + '|' 
        
        print(listStr)

# -------------
# Simulation
# -------------
class simData:
    def __init__(self,**kwargs):
        # [Description]: create a simData object using a 
        #                disctionary as a starting point

        self._dataDict = kwargs
        # Ensure time is included
        assert 'time' in self._dataDict

    def getSignalNames(self):
        return list(self._dataDict.keys())
    
    def getSignalData(self,aName:str)->list:
        return self._dataDict[aName]
    
    def getSignalSample(self,aName:str,aIndex):
        # [Description]: Return signal value at a certain index
        #                designed to support iterations
        return self._dataDict[aName][aIndex]

def run(aBlock, simIn):
    # [Description]: Executes a simulation over a mlib.block
    # [Inputs]:
    #   - aBlock: Block to be simulated
    #   - simIn: Dictionary with input data
    # [Outputs]:
    #   - simOut: Dictionary with input data

    # Ensure block/test have same inputs:
    inportNames  = aBlock.getInportNames()
    inportsNo    = len(inportNames)

    simInports      = simIn.keys()
    simInportsNo    = len(simInports) -1

    assert inportsNo == simInportsNo, '[Error] Number of Inports do not match'
    
    # Create test inports:
    simPorts = dict()
    for portH in aBlock._inports.values():
        aName = portH.getName()
        aType = portH.getType()

        simPorts[aName] = mlib.Outport (aName, # name
                                        aType, # type
                                        None)
        portH.connectTo(simPorts[aName])

    simOut = dict()
    simOut['time'] = simIn['time']
    for portH in aBlock._outports.values():
        aName = portH.getName()
        aType = portH.getType()

        simOut[aName] = np.zeros_like(simIn['time'],dtype=aType)

    # Execute iteration
    for k,iTime in enumerate(simIn['time']):
        for inName in inportNames:
            simPorts[inName].setValue(simIn[inName][k])

        aBlock.execute()

        # Assign outports:
        for outportH in aBlock._outports.values():
            outName = outportH.getName()
            simOut[outName][k] = outportH.getValue()

        aBlock.update()

    return simOut

# -------------
# Testing
# -------------
def verifyEqual(listA: list, listB: list, aTol: float) -> bool:
    # [Description]: Compare two lists against tolerance. 
    #                Returns False if not equal
    # [Output]:
    #   - isEqual: True if lists match
    #   - msg:     Error message

    # Ensure lists have same size:
    aNo = len(listA)
    bNo = len(listB)
    assert aNo == bNo, 'ListA/B do not match size'

    for k,(iA,iB) in enumerate(zip(listA,listB)):
        isEqual = abs(iA - iB) < aTol
        if(not isEqual):
            msg = 'Index [' + str(k) + ']: ' + str(iA) + ' is not equal to ' + str(iB) 
            return isEqual, msg
        
    return isEqual, ''


