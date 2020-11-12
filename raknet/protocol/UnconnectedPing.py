from ..GeneralVariables import GeneralVariables
from .OfflinePacket import OfflinePacket

class UnconnectedPing(OfflinePacket):
    id = GeneralVariables.packetIds["UnconnectedPing"]
    time = None
    
    def decodePayload(self):
        self.putLong(self.time)
        self.putMagic()
        
    def encodePayload(self):
        self.time = self.getLong()
        self.magic = self.getMagic()