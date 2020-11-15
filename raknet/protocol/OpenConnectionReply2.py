from ..GeneralVariables import GeneralVariables
from .OfflinePacket import OfflinePacket

class OpenConnectionReply2(OfflinePacket):
    id = GeneralVariables.packetIds["OpenConnectionReply2"]
    serverGuid = None
    clientAddress = None
    mtuSize = None
    useSecurity = None
    
    def encodePayload(self):
        self.putMagic()
        self.putLong(self.serverGuid)
        self.putAddress(self.clientAddress)
        self.putShort(self.mtuSize)
        self.putByte(self.useSecurity)
        
    def decodePayload(self):
        self.magic = self.getMagic()
        self.serverGuid = self.getLong()
        self.clientAddress = self.getAddress()
        self.mtuSize = self.getShort()
        self.useSecurity = self.getByte()
