from utils.utils import formatMultiLine, COLOURS, FORMAT, printLines
from typing import TypeGuard
from struct import unpack

def tcpHead(rawData: bytes) -> TypeGuard[tuple]:
    (srcPort, destPort, sequence, acknowledgment, offsetReservedFlags) = unpack('! H H L L H', rawData[:14])
    offset = (offsetReservedFlags >> 12) * 4
    flagUrg = (offsetReservedFlags & 32) >> 5
    flagAck = (offsetReservedFlags & 16) >> 4
    flagPsh = (offsetReservedFlags & 8) >> 3
    flagRst = (offsetReservedFlags & 4) >> 2
    flagSyn = (offsetReservedFlags & 2) >> 1
    flagFin = offsetReservedFlags & 1
    data = rawData[offset:]
    return srcPort, destPort, sequence, acknowledgment, flagUrg, flagAck, flagPsh, flagRst, flagSyn, flagFin, data

def printTCP(tcp: tuple):
    printList = []
    printList.append('{} -TCP Segment:'.format(FORMAT.TAB_1))
    printList.append('{} -Source Port: {}{}{}, Destination Port: {}{}{}'.format(FORMAT.TAB_2, COLOURS.PURPLE, tcp[0], COLOURS.WHITE, COLOURS.CYAN, tcp[1], COLOURS.WHITE))
    printList.append('{} -Sequence: {}{}{}, Acknowledgment: {}{}{}'.format(FORMAT.TAB_2, COLOURS.TAN, tcp[2], COLOURS.WHITE, COLOURS.TAN, tcp[3], COLOURS.WHITE))
    printList.append('{} -Flags:'.format(FORMAT.TAB_2))
    printList.append('{} -URG: {}{}{}, ACK: {}{}{}, PSH: {}{}{}'.format(FORMAT.TAB_3, COLOURS.TAN, tcp[4], COLOURS.WHITE, COLOURS.TAN, tcp[5], COLOURS.WHITE, COLOURS.TAN, tcp[6], COLOURS.WHITE))
    printList.append('{} -RST: {}{}{}, SYN: {}{}{}, FIN:{}{}{}'.format(FORMAT.TAB_3, COLOURS.TAN, tcp[7], COLOURS.WHITE, COLOURS.TAN, tcp[8], COLOURS.WHITE, COLOURS.TAN, tcp[9], COLOURS.WHITE))
    printLines(printList)

def printOtherTCP(tcp: tuple):
    printList = []
    printList.append('{} -TCP Data:'.format(FORMAT.TAB_3))
    printList.extend(formatMultiLine(FORMAT.TAB_3, tcp[10]))
    printLines(printList)