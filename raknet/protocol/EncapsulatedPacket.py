from binutilspy.Binary import Binary
from ..GeneralVariables import GeneralVariables

class EncapsulatedPacket:
    def isReliable(reliability):
        if reliability == GeneralVariables.reliability["Unreliable"]:
            return True
        elif reliability == GeneralVariables.reliability["ReliableSequenced"]:
            return True
        elif reliability == GeneralVariables.reliability["ReliableOrdered"]:
            return True
        elif reliability == GeneralVariables.reliability["ReliableWithAckReceipt"]:
            return True
        elif reliability == GeneralVariables.reliability["ReliableOrderedWithAckReceipt"]:
            return True
        else:
            return False
            
    def isSequenced(reliability):
        if reliability == GeneralVariables.reliability["UnreliableSequenced"]:
            return True
        elif reliability == GeneralVariables.reliability["ReliableSequenced"]:
            return True
        else:
            return False
            
    def isOrdered(reliability):
        if reliability == GeneralVariables.reliability["ReliableOrdered"]:
            return True
        elif reliability == GeneralVariables.reliability["ReliableOrderedWithAckReceipt"]:
            return True
        else:
            return False
            
    def isSequencedOrOrdered(reliability):
        if reliability == GeneralVariables.reliability["UnreliableSequenced"]:
            return True
        elif reliability == GeneralVariables.reliability["ReliableOrdered"]:
            return True
        elif reliability == GeneralVariables.reliability["ReliableSequenced"]:
            return True
        elif reliability == GeneralVariables.reliability["ReliableOrderedWithAckReceipt"]:
            return True
        else:
            return False
