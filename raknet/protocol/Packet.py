from binutilspy.BinaryStream import BinaryStream
import socket
from ..utils.InternetAddress import InternetAddress

class Packet(BinaryStream):
    id = -1
    sendTime = None

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
        if version == 4:
            ip = ".".join([
                str((~self.getByte()) & 0xff),
                str((~self.getByte()) & 0xff),
                str((~self.getByte()) & 0xff),
                str((~self.getByte()) & 0xff)
            ])
            port = self.getShort()
            return InternetAddress(ip, port, version)
        if version == 6:
            self.getLShort()
            port = self.getShort()
            self.getInt()
            ip = socket.inet_ntop(socket.AF_INET6, self.get(16))
            self.getInt()
            return InternetAddress(ip, port, version)

    def putAddress(self, address):
        version = address.getVersion()
        ip = address.getIp()
        port = address.getPort()
        self.putByte(version)
        if version == 4:
            parts = ip.split(".")
            for part in parts:
                self.putByte((~(int(part))) & 0xff)
            self.putShort(port)
        elif version == 6:
            self.putLShort(socket.AF_INET6)
            self.putShort(port)
            self.putInt(0)
            self.put(socket.inet_pton(socket.AF_INET6, ip))
            self.putInt(0)
