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
        
    def addToQueue(self, packet, flags = GeneralVariables.packetPriorities["Normal"]):
        priority = flags & 0b1
        if priority == GeneralVariables.packetPriorities["Immediate"]:
            newPacket = DataPacket()
            packet.sequenceNumber = self.sendSequenceNumber
            self.sendSequenceNumber += 1
            newPacket.packets.append(packet)
            GeneralVariables.server.sendPacket(newPacket, self.address)
            newPacket.sendTime = time()
            self.recoveryQueue[newPacket.sequenceNumber, newPacket]
            return
        length = self.sendQueue.getTotalLength()
        if length + packet.getTotalLength() > self.mtuSize:
            self.sendPacketQueue()
        self.sendQueue.packets.append(packet)
        
    def sendPacketQueue(self):
        if self.sendQueue.packets.getTotalLength() > 0:
            self.sendQueue.sequenceNumber = self.sendSequenceNumber
            self.sendSequenceNumber += 1
            GeneralVariables.server.sendPacket(self.sendQueue, self.address)
            self.sendQueue.sendTime = time()
            self.recoveryQueue[self.sendQueue.sequenceNumber] = self.sendQueue
            self.sendQueue = DataPacket()

    def close(self):
        pass # Todo
