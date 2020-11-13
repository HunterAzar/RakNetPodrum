from raknet.server.Server import Server
from raknet.utils.InternetAddress import InternetAddress

address = InternetAddress("0.0.0.0", 19132, 4)

while True:
    command = input()
    if command == "":
        pass
    elif command == "stop":
        exit()
    else:
        print("Invalid Command!")
