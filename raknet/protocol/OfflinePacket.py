from ..GeneralVariables import GeneralVariables
from .Packet import Packet

class OfflinePacket(Packet):
    magic = None

    def getMagic(self):
        self.magic = self.get(16)

    def putMagic(self):
        self.put(GeneralVariables.magic)
        
    def isValid(self):
        return self.magic == GeneralVariables.magic