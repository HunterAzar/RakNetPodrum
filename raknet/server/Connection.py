from ..GeneralVariables import GeneralVariables
from time import time

class Connection:
    address = None
    mtuSize = None
    status = None
    channelIndex = None
    isAcive = False
    lastUpdateTime = None
    
    def __init__(self, address, mtuSize):
        self.address = address
        self.mtuSize = mtuSize
        self.status = GeneralVariables.connectionStates["Connecting"]
        self.channelIndex = [0]*32
        self.lastUpdateTime = time()

    def close(self):
        pass # Todo
