# [Description]: Helper function to support pysim

import msim.lib as mlib
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
    #   - simData: Data structure used to exercise the inputs
    # [Outputs]:
    #   - simData: Data structure with simulation results

    pass








