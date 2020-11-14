from ..GeneralVariables import GeneralVariables
from .OfflinePacket import OfflinePacket

class UnconnectedPing(OfflinePacket):
    id = GeneralVariables.packetIds["UnconnectedPing"]
    time = None
    
    def encodePayload(self):
        self.putLong(self.time)
        self.putMagic()
        
    def decodePayload(self):
        self.time = self.getLong()
        self.magic = self.getMagic()
