import socket
from ..GeneralVariables import GeneralVariables

class Server:
    socket = None
    
    def __init__(self, address, interface):
        GeneralVariables.server = self
        self.socket = socket.socket(socket.AF_INET if address.version == 4 else socket.AF_INET6, socket.SOCK_DGRAM socket.IPPROTO_UDP)
        if address.getVersion() == 6:
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
        try:
            self.socket.bind(address.ip, address.port)
        except socket.error as e:
            print(f"Failed to bind to to {str(address.port)}. Is a server already running on this port?")
            print(str(e))
            return
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
    def sendPacket(self, packet, ip, port):
        packet.encode()
        self.socket.sendto(packet.buffer, (ip, port)
