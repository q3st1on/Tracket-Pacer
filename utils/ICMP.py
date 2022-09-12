from utils.utils import formatMultiLine, COLOURS, FORMAT, printLines
from struct import unpack

def icmpHead(rawData):
    packetType, code, checksum = unpack('! B B H', rawData[:4])
    data = rawData[4:]
    return packetType, code, checksum, data 

def printICMP(icmp):
    printList = []
    printList.append('{} ICMP Packet:'.format(FORMAT.TAB_2))
    printList.append('{} Type: {}{}{}, Code: {}{}{}, Checksum: {}{}{},'.format(FORMAT.TAB_2, COLOURS.TAN, icmp[0], COLOURS.WHITE, COLOURS.TAN, icmp[1], COLOURS.WHITE, COLOURS.TAN, icmp[2], COLOURS.WHITE))
    printList.append('{} ICMP Data:'.format(FORMAT.TAB_2))
    printList.extend(formatMultiLine(FORMAT.TAB_3, icmp[3]))
    printLines(printList)