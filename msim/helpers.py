# [Description]: Helper function to support pysim

import mypy

# -------------------------------------------------------------------------
# Supporting functions
# -------------------------------------------------------------------------

def isMsimNumType(aType: any) -> bool:
    return aType is bool or \
           aType is int  or \
           aType is float


           
           