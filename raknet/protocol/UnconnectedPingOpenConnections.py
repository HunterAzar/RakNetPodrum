from ..GeneralVariables import GeneralVariables
from .UnconnectedPing import UnconnectedPing

class UnconnectedPingOpenConnections(UnconnectedPing):
    id = GeneralVariables.packetIds["UnconnectedPingOpenConnections"]