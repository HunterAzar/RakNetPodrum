from binutilspy.BinaryStream import BinaryStream
from ..utils.InternetAddress import InternetAddress

class Packet(BinaryStream):
    id = -1

    def decodeHeader(self):
        return self.getByte()

    def decodePayload(self):
        pass

    def decode(self):
        self.offset = 0
        self.decodeHeader()
        self.decodePayload()

    def encodeHeader(self):
        self.putByte(self.id)

    def encodePayload(self):
        pass

    def encode(self):
        self.reset()
        self.encodeHeader()
        self.encodePayload()

    def getString(self):
        return self.get(self.getShort()).decode()

    def putString(self, value):
        self.putShort(len(value))
        self.put(value.encode())

    def getAddress(self):
        version = self.getByte()
        ip = ".".join([
            str(-1 * (self.getByte() + 1) + 256),
            str(-1 * (self.getByte() + 1) + 256),
            str(-1 * (self.getByte() + 1) + 256),
            str(-1 * (self.getByte() + 1) + 256)
        ])
        port = self.getShort()
        return InternetAddress(ip, port, version)

    def putAddress(self, address):
        self.putByte(address.getVersion())
        parts = address.getIp().split(".")
        for i in range(0, 4):
            self.putByte(abs(int(parts[i]) -1) - 256)
        self.putShort(address.getPort())