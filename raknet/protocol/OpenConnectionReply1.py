from ..GeneralVariables import GeneralVariables
from .OfflinePacket import OfflinePacket

class OpenConnectionReply1(OfflinePacket):
    id = GeneralVariables.packetIds["OpenConnectionReply1"]
    serverGuid = None
    useSecurity = None
    mtuSize = None
    
    def encodePayload(self):
        self.putMagic()
        self.putLong(self.serverGuid)
        self.putByte(self.useSecurity)
        self.putShort(self.mtuSize)
        
    def decodePayload(self):
        self.magic = self.getMagic()
        self.serverGuid = self.getLong()
        self.useSecurity = self.getByte()
        self.mtuSize = self.getShort()
