from raknet.server.Server import Server
from raknet.utils.InternetAddress import InternetAddress

server = Server(InternetAddress("0.0.0.0", 19132))

server.setOption("name", "MCPE;Dedicated Server;390;1.14.60;0;10;13253860892328930865;Bedrock level;Survival;1;19132;19133;")
server.startServer()
