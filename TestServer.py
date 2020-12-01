from raknet.server.Server import Server
from raknet.utils.InternetAddress import InternetAddress
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]

server = Server(InternetAddress(ip, 19132))

server.setOption("name", "MCPE;Dedicated Server;390;1.14.60;0;10;13253860892328930865;Bedrock level;Survival;1;19132;19133;")
server.startServer()
