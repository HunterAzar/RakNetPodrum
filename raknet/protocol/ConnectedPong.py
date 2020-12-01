from ..GeneralVariables import GeneralVariables
from .Packet import Packet

class ConnectedPong(Packet):
    id = GeneralVariables.packetIds["ConnectedPong"]
    requestTime = None
    replyTime = None

    def encodePayload(self):
        self.putLong(self.requestTime)
        self.putLong(self.replyTime)
        
    def decodePayload(self):
        self.requestTime = self.getLong()
        self.replyTime = self.getLong()
