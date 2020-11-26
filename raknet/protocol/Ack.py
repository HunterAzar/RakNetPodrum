from .AcknowledgePacket import AcknowledgePacket
from ..GeneralVariables import GeneralVariables

class Ack(AcknowledgePacket):
    id = GeneralVariables.packetIds["Ack"]
