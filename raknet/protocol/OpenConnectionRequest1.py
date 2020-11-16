from ..GeneralVariables import GeneralVariables
from .OfflinePacket import OfflinePacket

class OpenConnectionRequest1(OfflinePacket):
    id = GeneralVariables.packetIds["OpenConnectionRequest1"]
    protocolVersion = None
    mtuSize = None
    
    def encodePayload(self):
        self.putMagic()
        self.putByte(self.protocolVersion)
        self.put(bytes(self.mtuSize))
        
    def decodePayload(self):
        self.magic = self.getMagic()
        self.protocolVersion = self.getByte()
        self.mtuSize = len(self.buffer)
