from ..GeneralVariables import GeneralVariables
from .Packet import Packet

class ConnectionRequest(Packet):
    id = GeneralVariables.ids["ConnectionRequest"]
    clientGuid = None
    time = None
    useSecurity = None

    def encodePayload(self):
        self.putLong(self.clientGuid)
        self.putLong(self.time)
        self.putByte(self.useSecurity)
        
    def decodePayload(self):
        self.clientGuid = self.getLong()
        self.time = self.getLong()
        self.useSecurity = self.getByte()
