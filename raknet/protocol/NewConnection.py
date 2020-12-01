from ..GeneralVariables import GeneralVariables
from .Packet import Packet

class NewConnection(Packet):
    id = GeneralVariables.packetIds["NewConnection"]
    clientAddress = None
    systemAddresses = []
    requestTime = None
    replyTime = None

    def encodePayload(self):
        self.putAddress(self.clientAddress)
        for i in range(0, GeneralVariables.options["systemAddressesCount"]):
            self.putAddress(self.systemAddresses[i])
        self.putLong(self.requestTime)
        self.putLong(self.replyTime)
        
    def decodePayload(self):
        self.clientAddress = self.getAddress()
        for i in range(0, GeneralVariables.options["systemAddressesCount"]):
            self.systemAddresses.insert(i, self.getAddress())
        self.requestTime = self.getLong()
        self.replyTime = self.getLong()
