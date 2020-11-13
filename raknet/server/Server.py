import socket
from threading import Thread
from ..GeneralVariables import GeneralVariables
from .server.Handler import Handler

class Server(Thread):
    socket = None
    
    def __init__(self, address, interface):
        super().__init__()
        GeneralVariables.server = self
        self.socket = socket.socket(socket.AF_INET if address.version == 4 else socket.AF_INET6, socket.SOCK_DGRAM socket.IPPROTO_UDP)
        if address.version == 6:
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
        try:
            self.socket.bind(address.ip, address.port)
        except socket.error as e:
            print(f"Failed to bind to to {str(address.port)}. Is a server already running on this port?")
            print(str(e))
        else:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.start()
        
    def sendPacket(self, packet, ip, port):
        packet.encode()
        self.socket.sendto(packet.buffer, (ip, port))

    def run(self):
        while True:
            recv = socket.recvfrom(65535)
            if recv:
                Handler.handle(recv[0], recv[1])
