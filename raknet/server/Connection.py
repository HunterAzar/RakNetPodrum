from copy import deepcopy
from ..GeneralVariables import GeneralVariables
from ..protocol.Ack import Ack
from ..protocol.DataPacket import DataPacket
from ..protocol.EncapsulatedPacket import EncapsulatedPacket
from ..protocol.Nack import Nack
from ..server.Handler import Handler
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
    handler = None
    
    def __init__(self, address, mtuSize):
        self.address = address
        self.mtuSize = mtuSize
        self.status = GeneralVariables.connectionStates["Connecting"]
        self.channelIndex = [0]*32
        self.lastUpdateTime = time()
        self.sendQueue = DataPacket()
        self.handler = Handler()
        
    def update(self, timestamp):
        if not self.isActive and self.lastUpdate + 10000 < timestamp:
            GeneralVariables.server.removeConnection(self.address)
            return
        self.active = False
        if len(self.ackQueue) > 0:
            packet = Ack()
            packet.sequenceNumbers = self.ackQueue
            GeneralVariables.server.sendPacket(packet, self.address.ip, self.address.port)
            self.ackQueue = []
        if len(self.nackQueue) > 0:
            packet = Nack()
            packet.sequenceNumbers = self.nackQueue
            GeneralVariables.server.sendPacket(packet, self.address.ip, self.address.port)
            self.nackQueue = []
        if len(self.packetToSend) > 0:
            limit = 16
            for key, packet in enumerate(self.packetToSend):
                packet.sendTime = timestamp
                packet.encode()
                self.recoveryQueue[packet.sequenceNumber] = packet
                del self.packetToSend[key]
                self.sendPacket(packet, self.address.ip, self.address.port)
                limit -= 1
                if limit <= 0:
                    break
            if len(self.packetToSend) > 2048:
                self.packetToSend = []
        for sequenceNumber, packet in dict(self.recoveryQueue).items():
            if packet.sendTime < (time() - 8000):
                self.packetToSend.append(packet)
                del self.recoveryQueue[sequenceNumber]
        for sequenceNumber in self.receivedWindow:
            if sequenceNumber < self.windowStart:
                self.receivedWindow.remove(sequenceNumber)
            else:
                break
        self.sendPacketQueue()
        
    def receive(self, data):
        self.isActive = True
        self.lastUpdate = time()
        header = data[0]
        if (header & GeneralVariables.bitFlags["Valid"]) == 0:
            return
        if header & GeneralVariables.bitFlags["Ack"]:
            return self.handler.handleAck(data, self.address)
        if header & GeneralVariables.bitFlags["Nack"]:
            return self.handler.handleNack(data, self.address)
        return self.handler.handleDataPacket(data, self.address)
        
    def receivePacket(self, packet):
        if packet.reliableFrameIndex is None:
            self.handler.handleEncapsulatedPacket(packet, self.address)
        else:
            if packet.reliableFrameIndex < self.reliableWindowStart or packet.reliableFrameIndex > self.reliableWindowEnd:
                return
            if packet.reliableFrameIndex - self.lastReliableIndex == 1:
                self.lastReliableIndex += 1
                self.reliableWindowStart += 1
                self.reliableWindowEnd += 1
                self.handler.handleEncapsulatedPacket(packet, self.address)
                if len(self.reliableWindow) > 0:
                    windows = deepcopy(self.reliableWindow)
                    reliableWindow = {}
                    windows = dict(sorted(windows.items()))
                    for k, v in windows.items():
                        reliableWindow[k] = v
                    self.reliableWindow = reliableWindow
                    for sequenceIndex, packet in self.reliableWindow.items():
                        if (sequenceIndex - self.lastReliableIndex) != 1:
                            break
                        self.lastReliableIndex += 1
                        self.reliableWindowStart += 1
                        self.reliableWindowEnd += 1
                        self.handler.handleEncapsulatedPacket(packet, self.address)
                        del self.reliableWindow[seqIndex]
            else:
                self.reliableWindow[packet.reliableFrameIndex] = packet
                
        
    def addToQueue(self, packet, flags = GeneralVariables.packetPriorities["Normal"]):
        priority = flags & 0b1
        if priority == GeneralVariables.packetPriorities["Immediate"]:
            newPacket = DataPacket()
            newPacket.sequenceNumber = self.sendSequenceNumber
            self.sendSequenceNumber += 1
            newPacket.packets.append(packet)
            GeneralVariables.server.sendPacket(newPacket, self.address.ip, self.address.port)
            newPacket.sendTime = time()
            self.recoveryQueue[newPacket.sequenceNumber] = newPacket
            return
        length = self.sendQueue.getTotalLength()
        if length + packet.getTotalLength() > self.mtuSize:
            self.sendPacketQueue()
        self.sendQueue.packets.append(packet)
        
    def addEncapsulatedToQueue(self, packet, flags = GeneralVariables.packetPriorities["Normal"]):
        if packet.reliability != 5:
            if packet.reliability >= 2 or packet.reliabilit <= 7:
                packet.reliableFrameIndex = self.reliableFrameIndex
                self.reliableFrameIndex += 1
                if packet.reliability == 3:
                    packet.orderedFrameIndex = self.channelIndex[packet.orderedFrameIndex]
                    self.channelIndex[packet.orderedFrameIndex] += 1
        if packet.getTotalLength() + 4 > self.mtuSize:
            buffers = []
            index = 0
            fragmentIndex = 0
            while index < len(packet.buffer):
                buffer = []
                buffer.insert(0, fragmentIndex)
                fragmentIndex += 1
                oldIndex = index
                index += self.mtuSize
                buffer.insert(1, packet.buffer[oldIndex:index - 60])
                buffers.append(buffer)
            self.fragmentId += 1
            fragmentId = self.fragmentId % 65536
            for count, buffer in buffers:
                newPacket = EncapsulatedPacket()
                newPacket.fragmentId = fragmentId
                newPacket.isFragmented = True
                newPacket.fagmentSize = len(buffers)
                newPacket.reliability = packet.reliability
                newPacket.fragmentIndex = count
                newPacket.body = buffer
                if count > 0:
                    newPacket.reliableFrameIndex = self.reliableFrameIndex
                    self.reliableFrameIndex += 1
                else:
                    newPacket.reliableFrameIndex = packet.reliableFrameIndex
                if newPacket.reliability == 3:
                    newPacket.orderedFrameChannel = packet.orderedFrameChannel
                    newPacket.orderedFrameIndex = packet.orderedFrameIndex
                self.addToQueue(newPacket, flags | GeneralVariables.packetPriorities["Immediate"])
        else:
            self.addToQueue(packet, flags)
            
    def sendPacketQueue(self):
        if self.sendQueue.packets.getTotalLength() > 0:
            self.sendQueue.sequenceNumber = self.sendSequenceNumber
            self.sendSequenceNumber += 1
            GeneralVariables.server.sendPacket(self.sendQueue, self.address.ip, self.address.port)
            self.sendQueue.sendTime = time()
            self.recoveryQueue[self.sendQueue.sequenceNumber] = self.sendQueue
            self.sendQueue = DataPacket()

    def close(self):
        packet = EncapsulatedPacket()
        packet.buffer = b'\x00\x00\x08\x15'
        packet.decode()
        self.addEncapsulatedToQueue(packet, GeneralVariables.packetPriorities["Immediate"])
