from ..GeneralVariables import GeneralVariables
from .OfflinePacket import OfflinePacket

class UnconnectedPong(OfflinePacket):
    id = GeneralVariables.packetIds["UnconnectedPong"]
    time = None
    serverGuid = None
    serverName = None
    
    def encodePayload(self):
        self.putLong(self.time)
        self.putLong(self.serverGuid)
        self.putMagic()
        self.putString(self.serverName)
        
    def decodePayload(self):
        self.time = self.getLong()
        self.serverGuid = self.getLong()
        self.magic = self.getMagic()
        self.serverName = self.getString()
