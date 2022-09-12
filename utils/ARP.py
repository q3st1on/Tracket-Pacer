from utils.utils import getMacAddr, getIp, COLOURS, FORMAT, printLines
from typing import TypeGuard
from struct import unpack

ARP = {
    'HTYPES': {
        0: 'Reserved',
        1: 'Ethernet',
        2: 'Experimental Ethernet',
        3: 'Amateur Radio AX.25',
        4: 'Proteon ProNET Token Ring',
        5: 'Chaos',
        6: 'IEEE 802 Networks',
        7: 'ARCNET',
        8: 'Hyperchannel',
        9: 'Lanstar',
        10: 'Autonet Short Address',
        11: 'LocalTalk',
        12: 'LocalNet',
        13: 'Ultra link',
        14: 'SMDS',
        15: 'Frame Relay',
        16: 'Asynchronous Transmission Mode',
        17: 'HDLC',
        18: 'Fibre Channel',
        19: 'Asynchronous Transmission Mode',
        20: 'Serial Line',
        21: 'Asynchronous Transmission Mode',
        22: 'MIL-STD-188-220',
        23: 'Metricom',
        24: 'IEEE 1394.1995',
        25: 'MAPOS',
        26: 'Twinaxial',
        27: 'EUI-64',
        28: 'HIPARP',
        29: 'IP and ARP over ISO 7816-3',
        30: 'ARPSec',
        31: 'IPsec tunnel',
        32: 'InfiniBand (TM)',
        33: 'TIA-102 Project 25 Common Air Interface',
        34: 'Wiegand Interface',
        35: 'Pure IP',
        36: 'HW_EXP1',
        37: 'HFI',
        39: 'Unified Bus',
        256: 'HW_EXP2',
        257: 'AEthernet',
        65535: 'Reserved'
    },
    'OPCODES': {
        0: 'Reserved',
        1: 'Request',
        2: 'Reply',
        3: 'Request Reverse',
        4: 'Reply Reverse',
        5: 'DRARP-Request',
        6: 'DRARP-Reply',
        7: 'DRARP-Error',
        8: 'InARP-Request',
        9: 'InARP-Reply',
        10: 'ARP-NAK',
        11: 'MARS-Request',
        12: 'MARS-Multi',
        13: 'MARS-MServ',
        14: 'MARS-Join',
        15: 'MARS-Leave',
        16: 'MARS-NAK',
        17: 'MARS-Unserv',
        18: 'MARS-SJoin',
        19: 'MARS-SLeave',
        20: 'MARS-Grouplist-Request',
        21: 'MARS-Grouplist-Reply',
        22: 'MARS-Redirect-Map',
        23: 'MAPOS-UNARP',
        24: 'OP_EXP1',
        25: 'OP_EXP2',
        65535: 'Reserved'
    },
    'PTYPES': {
        257: 'Experimental',
        512: 'XEROX PUP',
        513: 'PUP Addr Trans',
        1536: 'XEROX NS IDP',
        2048: 'IPV4',
        2054: 'Address Resolution Protocol (ARP)'
    }
}

def arpHead(rawData: bytes) -> TypeGuard[tuple]:
    HTYPE, PTYPE, HLEN, PLEN, OPCODE, SHWA, SPA, THWA, TPA = unpack("! H H B B H 6s 4s 6s 4s", rawData[:28])
    SHWA = getMacAddr(SHWA)
    SPA = getIp(SPA)
    THWA = getMacAddr(THWA)
    TPA = getIp(TPA)
    data = rawData[28:]
    try: 
        HTYPE = f"{ARP['HTYPES'][HTYPE]} {COLOURS.WHITE}({COLOURS.TAN}{HTYPE}{COLOURS.WHITE})"
    except:
        HTYPE = f"Unnasigned {COLOURS.WHITE}({COLOURS.TAN}{HTYPE}{COLOURS.WHITE})"
    try:
        PTYPE = f"{ARP['PTYPES'][PTYPE]} {COLOURS.WHITE}({COLOURS.TAN}{PTYPE}{COLOURS.WHITE})"
    except:
        PTYPE = f"Unnasigned {COLOURS.WHITE}({COLOURS.TAN}{PTYPE}{COLOURS.WHITE})"
    try:
        OPCODE = f"{ARP['OPCODES'][OPCODE]} {COLOURS.WHITE}({COLOURS.TAN}{OPCODE}{COLOURS.WHITE})"
    except:
        OPCODE = f"Unnasigned {COLOURS.WHITE}({COLOURS.TAN}{OPCODE}{COLOURS.WHITE})"
    return HTYPE, PTYPE, HLEN, PLEN, OPCODE, SHWA, SPA, THWA, TPA, data

def printARP(arp: tuple):
    printList = []
    printList.append('{} -ARP Packet:'.format(FORMAT.TAB_1))
    printList.append('{}       Hardware Type: {}{}{}'.format(FORMAT.TAB_2, COLOURS.TAN, arp[0], COLOURS.WHITE))
    printList.append('{}       Protocol Type: {}{}{}'.format(FORMAT.TAB_2, COLOURS.TAN, arp[1], COLOURS.WHITE))
    printList.append('{}       Hardware Size: {}{}{}'.format(FORMAT.TAB_2, COLOURS.TAN, arp[2], COLOURS.WHITE))
    printList.append('{}       Protocol Size: {}{}{}'.format(FORMAT.TAB_2, COLOURS.TAN, arp[3], COLOURS.WHITE))
    printList.append('{}              Opcode: {}{}{}'.format(FORMAT.TAB_2, COLOURS.TAN, arp[4], COLOURS.WHITE))
    printList.append('{}  Sender MAC Address: {}{}{}'.format(FORMAT.TAB_2, COLOURS.GREEN, arp[5], COLOURS.WHITE))
    printList.append('{}   Sender IP Address: {}{}{}'.format(FORMAT.TAB_2, COLOURS.RED, arp[6], COLOURS.WHITE))
    printList.append('{}  Target MAC Address: {}{}{}'.format(FORMAT.TAB_2, COLOURS.GREEN, arp[7], COLOURS.WHITE))
    printList.append('{}   Target IP Address: {}{}{}'.format(FORMAT.TAB_2, COLOURS.BLUE, arp[8], COLOURS.WHITE))
    if len(arp[9]) > 0:
        printList.append('{} -Other ARP Data: {}'.format(FORMAT.TAB_1, arp[9]))
    printLines(printList)