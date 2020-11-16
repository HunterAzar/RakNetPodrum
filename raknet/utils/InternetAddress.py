class InternetAddress:
    ip = None
    port = None
    version = None

    def __init__(self, ip, port = 19132, version = 4):
        self.ip = ip
        self.port = port
        self.version = version

    def getIp(self):
        return self.ip

    def getPort(self):
        return self.port

    def getVersion(self):
        return self.version

    def toString(self):
        return f"{self.ip}:{self.port}"
