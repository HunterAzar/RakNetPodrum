from .Packet import Packet
from ..GeneralVariables import GeneralVariables

class EncapsulatedPacket(Packet):
    reliability = None
    isFragmented = None
    needAck = None
    length = None
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
        self.isFragmented = (flags & 0x10) > 0
        
    def decodePayload(self):
        pass
    
    @staticmethod
    def isReliable(reliability):
        if reliability == GeneralVariables.reliability["Unreliable"]:
            return True
        elif reliability == GeneralVariables.reliability["ReliableSequenced"]:
            return True
        elif reliability == GeneralVariables.reliability["ReliableOrdered"]:
            return True
        elif reliability == GeneralVariables.reliability["ReliableWithAckReceipt"]:
            return True
        elif reliability == GeneralVariables.reliability["ReliableOrderedWithAckReceipt"]:
            return True
        else:
            return False
            
    @staticmethod
    def isSequenced(reliability):
        if reliability == GeneralVariables.reliability["UnreliableSequenced"]:
            return True
        elif reliability == GeneralVariables.reliability["ReliableSequenced"]:
            return True
        else:
            return False
            
    @staticmethod
    def isOrdered(reliability):
        if reliability == GeneralVariables.reliability["ReliableOrdered"]:
            return True
        elif reliability == GeneralVariables.reliability["ReliableOrderedWithAckReceipt"]:
            return True
        else:
            return False
            
    @staticmethod
    def isSequencedOrOrdered(reliability):
        if reliability == GeneralVariables.reliability["UnreliableSequenced"]:
            return True
        elif reliability == GeneralVariables.reliability["ReliableOrdered"]:
            return True
        elif reliability == GeneralVariables.reliability["ReliableSequenced"]:
            return True
        elif reliability == GeneralVariables.reliability["ReliableOrderedWithAckReceipt"]:
            return True
        else:
            return False
