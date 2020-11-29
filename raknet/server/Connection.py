from ..GeneralVariables import GeneralVariables

class Connection:
    address = None
    mtuSize = None
    status = None
    channelIndex = None
    
    def __init__(self, address, mtuSize):
        self.address = address
        self.mtuSize = mtuSize
        self.status = GeneralVariables.connectionStates["Connecting"]
        self.channelIndex = [0]*32

    def close(self):
        pass # Todo
