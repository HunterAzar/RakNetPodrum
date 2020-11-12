import socket

class Server:
    socket = None
    
    def __init__(self, address, interface):
        self.socket = socket.socket(socket.AF_INET if address.getVersion() == 4 else socket.AF_INET6, socket.SOCK_DGRAM)
        
        
    def sendPacket(self, packet, ip, port):
        packet.encode()
        self.socket.sendto(packet.buffer, (ip, port)