from ..GeneralVariables import GeneralVariables
from ..protocol.DataPacket import DataPacket
from time import time

class Connection:
    address = None
    mtuSize = None
    status = None
    channelIndex = None
    isAcive = False
    lastUpdateTime = None
    ackQueue = []
    nackQueue = []
    recoveryQueue = {}
    packetToSend = []
    sendQueue = None
    fragmentedPackets = {}
    windowStart = -1
    windowEnd = 2048
    reliableWindowStart = 0
    reliableWindowEnd = 2048
    reliableWindow = {}
    lastReliableIndex = -1
    receivedWindow = []
    lastSequenceNumber = -1
    sendSequenceNumber = 0
    reliableFrameIndex = 0
    fragmentId = 0
    
    def __init__(self, address, mtuSize):
        self.address = address
        self.mtuSize = mtuSize
        self.status = GeneralVariables.connectionStates["Connecting"]
        self.channelIndex = [0]*32
        self.lastUpdateTime = time()
        self.sendQueue = DataPacket()

    def close(self):
        pass # Todo
