from ..GeneralVariables import GeneralVariables
from ..protocol.Ack import Ack
from ..protocol.ConnectedPing import ConnectedPing
from ..protocol.ConnectedPong import ConnectedPong
from ..protocol.ConnectionClosed import ConnectionClosed
from ..protocol.ConnectionRequest import ConnectionRequest
from ..protocol.ConnectionRequestAccepted import ConnectionRequestAccepted
from ..protocol.DataPacket import DataPacket
from ..protocol.EncapsulatedPacket import EncapsulatedPacket
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
            newPacket.systemAddresses.insert(i, InternetAddress("127.0.0.1", 0))
        newPacket.requestTime = packet.time
        newPacket.replyTime = int(time())
        return newPacket
        
    def handleNewConnection(self, data, address):
        connection = GeneralVariables.server.getConnection(address)
        packet = NewConnection()
        packet.buffer = data
        if address == packet.clientAddress:
            connection.status = GeneralVariables.connectionStates["Connected"]
        
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
                
    def handleDataPacket(self, data, address):
        connection = GeneralVariables.server.getConnection(address)
        packet = DataPacket()
        packet.buffer = data
        packet.decode()
        if packet.sequenceNumber < connection.windowStart:
            return
        if packet.sequenceNumber > connection.windowEnd:
            return
        if packet.sequenceNumber in connection.receivedWindow:
            return
        if packet.sequenceNumber in connection.nackQueue:
            connection.nackQueue.remove(packet.sequenceNumber)
        connection.ackQueue.append(packet.sequenceNumber)
        connection.receivedWindow.append(packet.sequenceNumber)
        diff = packet.sequenceNumber - connection.lastSequenceNumber
        if diff != 1:
            for i in range(connection.lastSequenceNumber + 1, packet.sequenceNumber):
                if i not in connection.receivedWindow:
                    connection.nackQueue.append(i)
        if diff >= 1:
            connection.lastSequenceNumber = packet.sequenceNumber
            connection.windowStart += diff
            connection.windowEnd += diff
        for encapsulatedPacket in packet.packets:
            connection.receivePacket(encapsulatedPacket)
        return
    
    def handleEncapsulatedPacket(self, packet, address):
        connection = GeneralVariables.server.getConnection(address)
        if packet.isFragmented:
            self.handleFragmentedPacket(packet, address)
            return
        packetId = packet.body[0]
        if packetId < 0x80:
            if connection.status == GeneralVariables.connectionStates["Connecting"]:
                if packetId == GeneralVariables.packetIds["ConnectionRequest"]:
                    print("Connecting...")
                    packet = self.handleConnectionRequest(packet.body)
                    packet.encode()
                    sendPacket = EncapsulatedPacket()
                    sendPacket.reliability = 0
                    sendPacket.body = packet.buffer
                    conection.addToQueue(sendPacket, GeneralVariables.packetPriorities["Immediate"])
                elif packetId == GeneralVariables.packetIds["NewConnection"]:
                    self.handleNewConnection(packet.body, address)
            elif packetId == GeneralVariables.packetIds["ConnectionClosed"]:
                GeneralVariables.server.removeConnection(address)
            elif packetId == GeneralVariables.packetIds["ConnectedPing"]:
                packet = self.handleConnectedPing(packet.body)
                packet.encode()
                sendPacket = EncapsulatedPacket()
                sendPacket.reliability = 0
                sendPacket.body = packet.buffer
                conection.addToQueue(sendPacket)
            elif connection.status == GeneralVariables.connectionStates["Connected"]:
                print("Connected!")
                
    def handleFragmentedPacket(self, packet, address):
        connection = GeneralVariables.server.getConnection(address)
        if packet.fragmentId in connection.fragmentedPackets:
            value = connection.fragmentedPackets[packet.fragmentId]
            value[packet.fragmentIndex] = packet
            connection.fragmentedPackets[packet.fragmentId] = value
        else:
            connection.fragmentedPackets[packet.fragmentId] = {packet.fragmentIndex: packet}
        localSplits = connection.fragmentedPackets[packet.fragmentId]
        if len(localSplits) == packet.fragmentSize:
            encapsulatedPacket = EncapsulatedPacket()
            stream = BinaryStream()
            for count, fragmentedPacket in enumerate(localSplits):
                stream.put(fragmentedPacket.body)
            del conection.fragmentedPackets[packet.fragmentId]
            encapsulatedPacket.body = stream.buffer
            conection.receivePacket(encapsulatedPacketpk)
    
    def handle(self, data, address):
        packetId = data[0]
        if GeneralVariables.options["debug"]:
            print(GeneralVariables.packetNames[id])
        connection = GeneralVariables.server.getConnection(InternetAddress(address[0], address[1]))
        if connection:
            connection.receive(data)
        elif packetId == GeneralVariables.packetIds["UnconnectedPing"]:
            newPacket = self.handleUnconnectedPing(data)
            GeneralVariables.server.sendPacket(newPacket, address[0], address[1])
        elif packetId == GeneralVariables.packetIds["UnconnectedPingOpenConnections"]:
            newPacket = self.handleUnconnectedPingOpenConnections(data)
            GeneralVariables.server.sendPacket(newPacket, address[0], address[1])
        elif packetId == GeneralVariables.packetIds["OpenConnectionRequest1"]:
            newPacket = self.handleOpenConnectionRequest1(data)
            GeneralVariables.server.sendPacket(newPacket, address[0], address[1])
        elif packetId == GeneralVariables.packetIds["OpenConnectionRequest2"]:
            newPacket = self.handleOpenConnectionRequest2(data, InternetAddress(address[0], address[1]))
            GeneralVariables.server.sendPacket(newPacket, address[0], address[1])
