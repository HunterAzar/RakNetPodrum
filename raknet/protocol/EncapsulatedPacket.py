from .Packet import Packet
from ..GeneralVariables import GeneralVariables

class EncapsulatedPacket(Packet):
    reliability = None
    isFragmented = None
    needAck = None
    reliableFrameIndex = None
    sequencedFrameIndex = None
    orderedFrameIndex = None
    orderedFrameChannel = None
    fagmentSize = None
    fragmentId = None
    fragmentIndex = None
    body = None
    
    def encodeHeader(self):
        header = self.reliability << 5
        if self.isFragmented:
            header |= GeneralVariables.bitFlags["Split"]
        self.putByte(header)
        
    def encodePayload(self):
        self.putShort(len(self.body) << 3)
        if self.isReliable(self.reliability):
            self.putLTriad(self.reliableFrameIndex)
        if self.isSequenced(self.reliability):
            self.putLTriad(self.sequencedFrameIndex)
        if self.isSequencedOrOrdered(self.reliability):
            self.putLTriad(self.orderedFrameIndex)
            self.putByte(self.orderedFrameChannel)
        if self.isFragmented:
            self.putInt(self.fagmentSize)
            self.putByte(self.fragmentId)
            self.putInt(self.fragmentIndex)
        self.put(self.body)
    
    def decodeHeader(self):
        flags = self.getByte()
        self.reliability = (flags & 224) >> 5
        self.isFragmented = (flags & GeneralVariables.bitFlags["Split"]) > 0
        
    def decodePayload(self):
        length = self.getShort() >> 3
        if self.isReliable(self.reliability):
            self.reliableFrameIndex = self.getLTriad()
        if self.isSequenced(self.reliability):
            self.sequencedFrameIndex = self.getLTriad()
        if self.isSequencedOrOrdered(self.reliability):
            self.orderedFrameIndex = self.getLTriad()
            self.orderedFrameChannel = self.getByte()
        if self.isFragmented:
            self.fagmentSize = self.getInt()
            self.fragmentId = self.getByte()
            self.fragmentIndex = self.getInt()
        self.body = self.get(length)
        
    def getTotalLength(self):
        value = 3
        value += 3 if self.reliableFrameIndex is not None else 0
        value += 4 if self.orderedFrameIndex is not None else 0
        value += 10 if self.isFragmented else 0
        value += len(self.body)
        return value
    
    @staticmethod
    def isReliable(reliability):
        if reliability == GeneralVariables.reliability["Unreliable"]:
            return True
        if reliability == GeneralVariables.reliability["ReliableSequenced"]:
            return True
        if reliability == GeneralVariables.reliability["ReliableOrdered"]:
            return True
        if reliability == GeneralVariables.reliability["ReliableWithAckReceipt"]:
            return True
        if reliability == GeneralVariables.reliability["ReliableOrderedWithAckReceipt"]:
            return True
        return False
            
    @staticmethod
    def isSequenced(reliability):
        if reliability == GeneralVariables.reliability["UnreliableSequenced"]:
            return True
        if reliability == GeneralVariables.reliability["ReliableSequenced"]:
            return True
        return False
            
    @staticmethod
    def isOrdered(reliability):
        if reliability == GeneralVariables.reliability["ReliableOrdered"]:
            return True
        if reliability == GeneralVariables.reliability["ReliableOrderedWithAckReceipt"]:
            return True
        return False
            
    @staticmethod
    def isSequencedOrOrdered(reliability):
        if reliability == GeneralVariables.reliability["UnreliableSequenced"]:
            return True
        if reliability == GeneralVariables.reliability["ReliableOrdered"]:
            return True
        if reliability == GeneralVariables.reliability["ReliableSequenced"]:
            return True
        if reliability == GeneralVariables.reliability["ReliableOrderedWithAckReceipt"]:
            return True
        return False
