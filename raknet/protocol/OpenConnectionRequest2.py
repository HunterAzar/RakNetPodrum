from ..GeneralVariables import GeneralVariables
from .OfflinePacket import OfflinePacket

class OpenConnectionRequest2(OfflinePacket):
    id = GeneralVariables.packetIds["OpenConnectionRequest2"]
    serverAddress = None
    mtuSize = None
    clientGuid = None
    
    def encodePayload(self):
        self.putMagic()
        self.putAddress(self.serverAddress)
        self.putShort(self.mtuSize)
        self.putLong(self.clientGuid)
        
    def decodePayload(self):
        self.magic = self.getMagic()
        self.serverAddress = self.getAddress()
        self.mtuSize = self.getShort()
        self.clientGuid = self.getLong()
