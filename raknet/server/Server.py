import socket
from threading import Thread
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
            
    def addressToToken(address):
        return str(address.ip) + ":" + str(address.port)
    
    def addConnection(address, mtuSize):
        token = self.addressToToken(address)
        pass # Todo | self.connections[token] = Connection(address, mtuSize)
            
    def setOption(self, name, value):
        GeneralVariables.options[name] = value
        
    def sendPacket(self, packet, ip, port):
        packet.encode()
        print(packet.buffer)
        self.socket.sendto(packet.buffer, (ip, port))
        
    def startServer(self):
        self.start()

    def run(self):
        while True:
            recv = self.socket.recvfrom(65535)
            if recv:
                Handler().handle(recv[0], recv[1])
