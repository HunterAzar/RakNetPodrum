from binutilspy.BinaryStream import BinaryStream
from ..GeneralVariables import GeneralVariables
from .Packet import Packet

class AcknowledgePacket(Packet):
    sequenceNumbers = []

    def encodePayload(self):
        stream = BinaryStream()
        self.sequenceNumbers.sort()
        recordsCount = 0
        if len(self.sequenceNumbers) > 0:
            startIndex = self.sequenceNumbers[0]
            endIndex = self.sequenceNumbers[0]
            for i in range(1, len(self.sequenceNumbers)):
                index = self.sequenceNumbers[i]
                diff = index - endIndex
                if diff == 1:
                    endIndex = index
                elif diff > 1:
                    if startIndex == endIndex:
                        stream.putByte(1)
                        stream.putLTriad(startIndex)
                        startIndex = endIndex = index
                    else:
                        stream.putByte(0)
                        stream.putLTriad(startIndex)
                        stream.putLTriad(endIndex)
                        startIndex = endIndex = index
                    recordsCount += 1
            if startIndex == endIndex:
                stream.putByte(1)
                stream.putLTriad(startIndex)
            else:
                stream.putByte(0)
                stream.putLTriad(startIndex)
                stream.putLTriad(endIndex)
            recordsCount += 1
        self.putShort(recordsCount)
        self.put(stream.buffer)

    def decodePayload(self):
        self.sequenceNumbers = []
        recordsCount = self.getShort()
        for i in range(0, recordsCount):
            isInRange = self.getByte()
            if isInRange == 0:
                startIndex = self.getLTriad()
                endIndex = self.getLTriad()
                index = startIndex
                while index <= endIndex:
                    self.sequenceNumbers.append(index)
                    if len(self.sequenceNumbers) > 4096:
                        raise Exception("Max sequence number count exceed")
                    index += 1
            else:
                index = self.getLTriad()
                self.sequenceNumbers.append(index)
