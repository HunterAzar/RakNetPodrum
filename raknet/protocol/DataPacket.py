from .EncapsulatedPacket import EncapsulatedPacket
from ..GeneralVariables import GeneralVariables
from .Packet import Packet

class DataPacket(Packet):
    id = GeneralVariables.bitFlags["Valid"] | 0
    sequenceNumber = None
    packets = []
    
    def encodePayload(self):
        self.putLTriad(self.sequenceNumber)
        for packet in self.packets:
            packet.encode()
            self.put(packet.buffer)
        
    def decodePayload(self):
        self.sequenceNumber = self.getLTriad()
        while not self.feof():
            packet = EncapsulatedPacket()
            packet.buffer = self.buffer
            packet.offset = self.offset
            packet.decode()
            self.offset = packet.offset
            self.packets.append(packet)

    def getTotalLength(self):
        length = 4
        for packet in self.packets:
            length += packet.getTotalLength()
        return length
