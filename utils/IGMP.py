from utils.utils import getIp, COLOURS, FORMAT, printLines
from typing import TypeGuard
from struct import unpack

IGMP = {
    'Types': {
        11: 'Membership Query',
        12: 'IGMPv1 Membership Report',
        16: 'IGMPv2 Membership Report',
        17: 'Leave Group',
        22: 'IGMPv3 Membership Report'
    }
}

def igmpHead(rawData: bytes) -> TypeGuard[tuple]:
    packetType, respTime, checksum = unpack('! B B H', rawData[:4])
    groupAddr = getIp(rawData[4:])
    try:
        packetType = f"{IGMP['Types'][packetType]} ({packetType})"
    except:
        packetType = f"Unnasigned ({packetType})"
    return packetType, respTime, checksum, groupAddr

def printIGMP(igmp: tuple):
    printList = []
    printList.append('{} -IGMP Packet:'.format(FORMAT.TAB_1))
    printList.append('{} -Type: {}, Max Response Time: {}, Checksum {}'.format(FORMAT.TAB_2, igmp[0], igmp[1], igmp[2]))
    if igmp[0] != "Leave Group (17)":
        printList.append('{} -Group Address: {}'.format(FORMAT.TAB_2, igmp[3]))
    printLines(printList)