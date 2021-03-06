import socket
from threading import Thread
from time import time, sleep
from .Connection import Connection
from ..GeneralVariables import GeneralVariables
from .Handler import Handler

class Server(Thread):
    socket = None
    connections = {}
    
    def __init__(self, address, interface = None):
        super().__init__()
        GeneralVariables.server = self
        self.socket = socket.socket(socket.AF_INET if address.version == 4 else socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        if address.version == 6:
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
        try:
            self.socket.bind((address.ip, address.port))
        except socket.error as e:
            print(f"Failed to bind to to {str(address.port)}. Is a server already running on this port?")
            print(str(e))
        else:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            
    def addressToToken(self, address):
        return str(address.ip) + ":" + str(address.port)
    
    def addConnection(self, address, mtuSize):
        token = self.addressToToken(address)
        self.connections[token] = Connection(address, mtuSize)
    
    def removeConnection(self, address):
        token = self.addressToToken(address)
        if token in self.connections:
            connection = self.connections[token]
            connection.close()
            del connection
            
    def getConnection(self, address):
        token = self.addressToToken(address)
        if token in self.connections:
            return self.connections[token]
        return None
            
    def setOption(self, name, value):
        GeneralVariables.options[name] = value
        
    def sendPacket(self, packet, ip, port):
        packet.encode()
        if GeneralVariables.options["debug"]:
            print("Server to Client: " + hex(packet.buffer[0]))
        self.socket.sendto(packet.buffer, (ip, port))
        
    def tick(self):
        for token, connection in self.connections.items():
            connection.update(time())
        sleep(1 / 100)
        
    def startServer(self):
        self.start()

    def run(self):
        while True:
            recv = self.socket.recvfrom(65535)
            if recv:
                Handler().handle(recv[0], recv[1])
                self.tick()
