from ..GeneralVariables import GeneralVariables
from .Packet import Packet

class ConnectedPing(Packet):
    id = GeneralVariables.packetIds["ConnectedPing"]
    time = None

    def encodePayload(self):
        self.putLong(self.time)
        
    def decodePayload(self):
        self.time = self.getLong()
