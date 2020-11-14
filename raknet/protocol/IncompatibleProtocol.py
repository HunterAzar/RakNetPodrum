from ..GeneralVariables import GeneralVariables
from .OfflinePacket import OfflinePacket

class IncompatibleProtocol(OfflinePacket):
    id = GeneralVariables.packetIds["IncompatibleProtocol"]
    protocolVersion = None
    serverGuid = None
    
    def encodePayload(self):
        self.putLong(self.protocolVersion)
        self.putMagic()
        self.putLong(self.serverGuid)
        
    def decodePayload(self):
        self.protocolVersion = self.getLong()
        self.magic = self.getMagic()
        self.serverGuid = self.getLong()
