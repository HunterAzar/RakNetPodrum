import os

class GeneralVariables:
    magic = b"\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78"
    options = {
        "name": "",
        "guid": int.from_bytes(os.urandom(8), "little"),
        "systemAddressesCount": 20
    }
    packetIds = {
        "ConnectedPing": 0x00,
        "UnconnectedPing": 0x01,
        "UnconnectedPong": 0x1c,
        "UnconnectedPingOpenConnections": 0x02,
        "ConnectedPong": 0x03,
        "OpenConnectionRequest1": 0x05,
        "OpenConnectionResponse1": 0x06,
        "OpenConnectionRequest2": 0x07,
        "OpenConnectionResponse2": 0x08,
        "ConnectionRequest": 0x09,
        "ConnectionResponse": 0x10,
        "NewConnection": 0x13,
        "IncompatibleProtocol": 0x19,
        "nack": 0xa0,
        "ack": 0xc0
    }
    server = None
