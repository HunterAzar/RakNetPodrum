from ..GeneralVariables import GeneralVariables
from .Packet import Packet

class ConnectionRequestAccepted(Packet):
    id = GeneralVariables.ids["ConnectionRequestAccepted"]
    clientAddress = None
    systemIndex = None
    systemAddresses = []
    requestTime = None
    replyTime = None

    def encodePayload(self):
        self.putAddress(self.clientAddress)
        self.putByte(self.systemIndex)
        for i in range(0, GeneralVariables.options["systemAddressesCount"]):
            self.putAddress(self.systemAddresses[i])
        self.putLong(self.requestTime)
        self.putLong(self.replyTime)
        
    def decodePayload(self):
        self.clientAddress = self.getAddress()
        self.systemIndex = self.getByte()
        for i in range(0, GeneralVariables.options["systemAddressesCount"]):
            self.systemAddresses.insert(i, self.getAddress())
        self.requestTime = self.getLong()
        self.replyTime = self.getLong()
