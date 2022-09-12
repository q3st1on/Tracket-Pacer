from utils.utils import getIp, formatMultiLine, COLOURS, FORMAT, printLines
from typing import TypeGuard
from struct import unpack

def ipv4Head(rawData: bytes) -> TypeGuard[tuple]:
    versionHeaderLength = rawData[0]
    version = versionHeaderLength >> 4
    headerLength = (versionHeaderLength & 15) * 4
    ttl, proto, src, target = unpack('! 8x B B 2x 4s 4s', rawData[:20])
    src = getIp(src)
    target = getIp(target)
    data = rawData[headerLength:]
    return versionHeaderLength, version, headerLength, ttl, proto, src, target, data

def printIPV4(ipv4: tuple):
    printList = []
    printList.append('{} -IPv4 Packet:'.format(FORMAT.TAB_1))
    printList.append('{} -Version: {}{}{}, Header Length: {}{}{}, TTL: {}{}{},'.format(FORMAT.TAB_2, COLOURS.TAN, ipv4[1], COLOURS.WHITE, COLOURS.TAN, ipv4[2], COLOURS.WHITE, COLOURS.TAN, ipv4[3], COLOURS.WHITE))
    printList.append('{} -Protocol: {}{}{}, Source: {}{}{}, Target: {}{}{}'.format(FORMAT.TAB_2, COLOURS.TAN, ipv4[4], COLOURS.WHITE, COLOURS.RED, ipv4[5], COLOURS.WHITE, COLOURS.BLUE, ipv4[6], COLOURS.WHITE))
    printLines(printList)

def printOtherIPV4(ipv4: tuple):
    printList = []
    printList.append('{} -Other IPv4 Data:'.format(FORMAT.TAB_1))
    printList.extend(formatMultiLine(FORMAT.TAB_2, ipv4[7]))
    printLines(printList)