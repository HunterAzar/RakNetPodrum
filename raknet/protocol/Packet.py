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
            str((~self.getByte()) & 0xff),
            str((~self.getByte()) & 0xff),
            str((~self.getByte()) & 0xff),
            str((~self.getByte()) & 0xff)
        ])
        port = self.getShort()
        return InternetAddress(ip, port, version)

    def putAddress(self, address):
        self.putByte(address.getVersion())
        parts = address.getIp().split(".")
        for part in parts:
            self.putByte((~(int(part))) & 0xff)
        self.putShort(address.getPort())
