from ..GeneralVariables import GeneralVariables
from .Packet import Packet

class ConnectionClosed(Packet):
    id = GeneralVariables.ids["ConnectionClosed"]
