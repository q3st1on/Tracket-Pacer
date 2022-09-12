from utils.utils import formatMultiLine, COLOURS, FORMAT, printLines
from typing import TypeGuard
from struct import unpack

def icmpHead(rawData: bytes) -> TypeGuard[tuple]:
    packetType, code, checksum = unpack('! B B H', rawData[:4])
    data = rawData[4:]
    return packetType, code, checksum, data 

def printICMP(icmp: tuple):
    printList = []
    printList.append('{} ICMP Packet:'.format(FORMAT.TAB_2))
    printList.append('{} Type: {}{}{}, Code: {}{}{}, Checksum: {}{}{},'.format(FORMAT.TAB_2, COLOURS.TAN, icmp[0], COLOURS.WHITE, COLOURS.TAN, icmp[1], COLOURS.WHITE, COLOURS.TAN, icmp[2], COLOURS.WHITE))
    printList.append('{} ICMP Data:'.format(FORMAT.TAB_2))
    printList.extend(formatMultiLine(FORMAT.TAB_3, icmp[3]))
    printLines(printList)