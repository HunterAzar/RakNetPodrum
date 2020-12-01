import os

class GeneralVariables:
    magic = b"\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78"
    options = {
        "debug": True,
        "name": "",
        "guid": int.from_bytes(os.urandom(8), "little"),
        "systemAddressesCount": 20,
        "acceptedProtocolVersions": [5, 6, 7, 8, 9, 10]
    }
    packetIds = {
        "ConnectedPing": 0x00,
        "UnconnectedPing": 0x01,
        "UnconnectedPong": 0x1c,
        "UnconnectedPingOpenConnections": 0x02,
        "ConnectedPong": 0x03,
        "OpenConnectionRequest1": 0x05,
        "OpenConnectionReply1": 0x06,
        "OpenConnectionRequest2": 0x07,
        "OpenConnectionReply2": 0x08,
        "ConnectionRequest": 0x09,
        "ConnectionRequestAccepted": 0x10,
        "NewConnection": 0x13,
        "ConnectionClosed": 0x15,
        "IncompatibleProtocol": 0x19,
        "Nack": 0xa0,
        "Ack": 0xc0
    }
    packetNames = {
        0x01: "Unconnected Ping",
        0x1c: "Unconnected Pong",
        0x02: "Unconnected Ping Open Connections",
        0x05: "Open Connection Request 1",
        0x06: "Open Connection Reply 1",
        0x07: "Open Connection Request 2",
        0x08: "Open Connection Reply 2",
        0x19: "Incompatible Protocol",
        0xa0: "Nack",
        0xc0: "Ack",
        0x80: "Custom Packet",
        0x81: "Custom Packet",
        0x82: "Custom Packet",
        0x83: "Custom Packet",
        0x84: "Custom Packet",
        0x85: "Custom Packet",
        0x86: "Custom Packet",
        0x87: "Custom Packet",
        0x88: "Custom Packet",
        0x89: "Custom Packet",
        0x8a: "Custom Packet",
        0x8b: "Custom Packet",
        0x8c: "Custom Packet",
        0x8d: "Custom Packet"
    }
    reliability = {
        "Unreliable": 0,
        "UnreliableSequenced": 1,
        "Reliable": 2,
        "ReliableOrdered": 3,
        "ReliableSequenced": 4,
        "UnreliableWithAckReceipt": 5,
        "ReliableWithAckReceipt": 6,
        "ReliableOrderedWithAckReceipt": 7
    }
    bitFlags = {
        "Valid": 0x80,
        "Ack": 0x40,
        "Nack": 0x20,
        "Split": 0x10
    }
    connectionStates = {
        "Connecting": 0,
        "Connected": 1,
        "Disconnecting": 2,
        "Disconnected": 3
    }
    packetPriorities = {
        "Normal": 0,
        "Immediate": 1
    }
    server = None
