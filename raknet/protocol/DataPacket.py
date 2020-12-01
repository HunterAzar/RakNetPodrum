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
            data = self.buffer[self.offset:]
            if data == b"":
                break
            packet = EncapsulatedPacket()
            packet.buffer = data
            packet.decode()
            self.packets.append(packet)
            self.offset += packet.getTotalLength()

    def getTotalLength(self):
        length = 4
        for packet in self.packets:
            if isinstance(packet, EncapsulatedPacket):
                length += packet.getTotalLength()
            elif isinstance(packet, bytes):
                length += len(packet)
        return length
