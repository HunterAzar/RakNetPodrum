from ..GeneralVariables import GeneralVariables
from ..protocol.UnconnectedPing import UnconnectedPing
from ..protocol.UnconnectedPingOpenConnections import UnconnectedPingOpenConnections
from ..protocol.UnconnectedPong import UnconnectedPong

class Handler:
    def handleUnconnectedPing(self, data):
        packet = UnconnectedPing()
        packet.buffer = data
        packet.decode()
        newPacket = UnconnectedPong()
        newPacket.time = packet.time
        newPacket.serverGuid = GeneralVariables.options["guid"]
        newPacket.serverName = GeneralVariables.options["name"]
        return newPacket
        
    def handleUnconnectedPingOpenConnections(self, data):
        packet = UnconnectedPingOpenConnections()
        packet.buffer = data
        packet.decode()
        newPacket = UnconnectedPong()
        newPacket.time = packet.time
        newPacket.serverGuid = GeneralVariables.options["guid"]
        newPacket.serverName = GeneralVariables.options["name"]
        return newPacket
    
    def handle(self, data, address):
        id = data[0]
        if id == GeneralVariables.ids["UnconnectedPing"]:
            newPacket = handleUnconnectedPing(data)
            GeneralVariables.server.sendPacket(newPacket)
        elif id == GeneralVariables.ids["UnconnectedPingOpenConnections"]:
            newPacket = handleUnconnectedPingOpenConnections(data)
            GeneralVariables.server.sendPacket(newPacket)
