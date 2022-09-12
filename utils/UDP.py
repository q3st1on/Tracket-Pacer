from utils.utils import COLOURS, FORMAT, printLines
from struct import unpack

def udpHead(rawData):
    srcPort, destPort, size = unpack('! H H 2x H', rawData[:8])
    data = rawData[8:]
    return srcPort, destPort, size, data

def printUDP(udp):
    printList = []
    printList.append('{} -UDP Segment:'.format(FORMAT.TAB_1))
    printList.append('{} -Source Port: {}{}{}, Destination Port: {}{}{}, Length: {}{}{}'.format(FORMAT.TAB_2, COLOURS.PURPLE, udp[0], COLOURS.WHITE, COLOURS.CYAN, udp[1], COLOURS.WHITE, COLOURS.TAN, udp[2], COLOURS.WHITE))
    printLines(printList)