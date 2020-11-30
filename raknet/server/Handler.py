from ..GeneralVariables import GeneralVariables
from ..protocol.Ack import Ack
from ..protocol.ConnectedPing import ConnectedPing
from ..protocol.ConnectedPong import ConnectedPong
from ..protocol.ConnectionClosed import ConnectionClosed
from ..protocol.ConnectionRequest import ConnectionRequest
from ..protocol.ConnectionRequestAccepted import ConnectionRequestAccepted
from ..protocol.Nack import Nack
from ..protocol.NewConnection import NewConnection
from ..protocol.IncompatibleProtocol import IncompatibleProtocol
from ..protocol.OpenConnectionReply1 import OpenConnectionReply1
from ..protocol.OpenConnectionReply2 import OpenConnectionReply2
from ..protocol.OpenConnectionRequest1 import OpenConnectionRequest1
from ..protocol.OpenConnectionRequest2 import OpenConnectionRequest2
from ..protocol.UnconnectedPing import UnconnectedPing
from ..protocol.UnconnectedPingOpenConnections import UnconnectedPingOpenConnections
from ..protocol.UnconnectedPong import UnconnectedPong
from time import time
from ..utils.InternetAddress import InternetAddress

class Handler:
    def handleConnectedPing(self, data):
        packet = ConnectedPing()
        packet.buffer = data
        packet.decode()
        newPacket = ConnectedPong()
        newPacket.requestTime = packet.time
        newPacket.replyTime = int(time())
        return newPacket
    
    def handleConnectionRequest(self, data, address):
        packet = ConnectionRequest()
        packet.buffer = data
        packet.decode()
        newPacket = ConnectionRequestAccepted()
        newPacket.clientAddress = address
        newPacket.systemIndex = 0
        newPacket.systemAddresses = []
        for i in range(0, GeneralVariables.options["systemAddressesCount"]):
            newPacket.systemAddresses.insert(i, InternetAddress("0.0.0.0", 0))
        newPacket.requestTime = packet.time
        newPacket.replyTime = int(time())
        return newPacket
        
    def handleNewConnection(self, data, address):
        packet = NewConnection()
        packet.buffer = data
        if address == packet.clientAddress:
            pass # Todo set connection status to connected
        
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
    
    def handleOpenConnectionRequest1(self, data):
        packet = OpenConnectionRequest1()
        packet.buffer = data
        packet.decode()
        print(f"Your protocol version is {str(packet.protocolVersion)}.")
        if packet.protocolVersion not in GeneralVariables.options["acceptedProtocolVersions"]:
             newPacket = IncompatibleProtocol()
             newPacket.protocolVersion = packet.protocolVersion
             newPacket.serverGuid = GeneralVariables.options["guid"]
             return newPacket
        newPacket = OpenConnectionReply1()
        newPacket.serverGuid = GeneralVariables.options["guid"]
        newPacket.useSecurity = 0
        newPacket.mtuSize = packet.mtuSize
        return newPacket
    
    def handleOpenConnectionRequest2(self, data, address):
        packet = OpenConnectionRequest2()
        packet.buffer = data
        packet.decode()
        newPacket = OpenConnectionReply2()
        newPacket.serverGuid = GeneralVariables.options["guid"]
        newPacket.clientAddress = address
        newPacket.mtuSize = packet.mtuSize
        newPacket.useSecurity = 0
        GeneralVariables.server.addConnection(address, packet.mtuSize)
        return newPacket
    
    def handleAck(self, data, address):
        connection = GeneralVariables.server.getConnection(address)
        packet = Ack()
        packet.buffer = data
        packet.decode()
        for sequenceNumber in packet.sequenceNumbers:
            if sequenceNumber in connection.recoveryQueue:
                del connection.recoveryQueue[sequenceNumber]
                
    def handleNack(self, data, address):
        connection = GeneralVariables.server.getConnection(address)
        packet = Ack()
        packet.buffer = data
        packet.decode()
        for sequenceNumber in packet.sequenceNumbers:
            if sequenceNumber in connection.recoveryQueue:
                newPacket = connection.recoveryQueue[sequenceNumber]
                newPacket.sequenceNumber = connection.sendSequenceNumber
                connection.sendSequenceNumber += 1
                newPacket.sendTime = time()
                newPacket.encode()
                GeneralVariables.server.sendPacket(newPacket, address[0], address[1])
                del connection.recoveryQueue[sequenceNumber]
    
    def handle(self, data, address):
        id = data[0]
        if GeneralVariables.options["debug"]:
            print(GeneralVariables.packetNames[id])
        if GeneralVariables.server.getConnection():
            pass # Todo Custom Packets / Data Packets
        elif id == GeneralVariables.packetIds["UnconnectedPing"]:
            newPacket = self.handleUnconnectedPing(data)
            GeneralVariables.server.sendPacket(newPacket, address[0], address[1])
        elif id == GeneralVariables.packetIds["UnconnectedPingOpenConnections"]:
            newPacket = self.handleUnconnectedPingOpenConnections(data)
            GeneralVariables.server.sendPacket(newPacket, address[0], address[1])
        elif id == GeneralVariables.packetIds["OpenConnectionRequest1"]:
            newPacket = self.handleOpenConnectionRequest1(data)
            GeneralVariables.server.sendPacket(newPacket, address[0], address[1])
        elif id == GeneralVariables.packetIds["OpenConnectionRequest2"]:
            newPacket = self.handleOpenConnectionRequest2(data, InternetAddress(address[0], address[1]))
            GeneralVariables.server.sendPacket(newPacket, address[0], address[1])
