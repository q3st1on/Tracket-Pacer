from utils.utils import getMacAddr, formatMultiLine, addArgs, COLOURS, FORMAT, printSummary, asciiArt, dataQueryForm, Data
from graph import dataNetwork
from utils.ETHERNET import *
from entity import entity
from struct import unpack
from utils.HTTP import *
from utils.ICMP import *
from utils.IGMP import *
from utils.IPV4 import *
from utils.ARP import *
from utils.TCP import *
from utils.UDP import *
import argparse
import socket
import time
import os

MULTICASTCLEAN = True
BROADCASTCLEAN = True
LIVEPRINT = False
interface = "wlan0"
dataStore = Data()

def ethernetHead(rawData):
    dest, src, prototype = unpack('! 6s 6s H', rawData[:14])
    destMac = getMacAddr(dest)
    srcMac = getMacAddr(src)
    try:
        protoname = ETHERNET['EtherTypes'][prototype]
    except:
        protoname = 'Unnasigned'
    proto = socket.htons(prototype)
    data = rawData[14:]
    return destMac, srcMac, proto, protoname, data 

def main(count, captureTime=0, timeBool=False):
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    try:
        rec = 0
        if timeBool:
            t = int(time.time())
        else:
            t = 0
        
        if not LIVEPRINT:
            print("|"+49*" "+"RECORDING PACKETS"+49*" "+"|")

        while rec < count:
            s.bind((interface, 0))
            rawData, addr = s.recvfrom(65535)
            sourcePort, destPort, destIP, ip = "", "", "", "UNDEFINED"
            dataStore.packetRecieved += 1

            # ETHERNET
            eth = ethernetHead(rawData)
            protocol = "ETHERNET"
            if LIVEPRINT: printETH(eth)

            if eth[2] == 8:
                ipv4 = ipv4Head(eth[4])
                protocol = "IPV4"
                destIP = ipv4[6]
                if LIVEPRINT: printIPV4(ipv4)

                # TCP
                if ipv4[4] == 6:
                    tcp = tcpHead(ipv4[7])
                    ip = ipv4[5]
                    sourcePort = ipv4[0]
                    destPort = ipv4[1]
                    if LIVEPRINT: printTCP(tcp)

                    protocol = "TCP"
                    if len(tcp[10]) > 0:

                        # HTTP
                        if tcp[0] == 80 or tcp[1] == 80:
                            if LIVEPRINT: printHTTP(tcp)
                            protocol = "HTTP"

                        elif LIVEPRINT:
                            printOtherTCP(tcp)
                # ICMP
                elif ipv4[4] == 1:
                    icmp = icmpHead(ipv4[7])
                    protocol = "ICMP"
                    if LIVEPRINT: printICMP(icmp)

                # IGMP
                elif ipv4[4] == 2:
                    igmp = igmpHead(ipv4[7])
                    protocol = "IGMP"
                    if LIVEPRINT: printIGMP(igmp)

                # UDP
                elif ipv4[4] == 17:
                    udp = udpHead(ipv4[7])
                    protocol = "UDP"
                    sourcePort = udp[0]
                    destPort = udp[1]
                    if LIVEPRINT: printUDP(udp)

                # Other IPv4
                elif LIVEPRINT:
                    printOtherIPV4(ipv4)

            # ARP
            elif eth[2] == 1544:
                arp = arpHead(eth[4])
                protocol = "ARP"
                if LIVEPRINT: printARP(arp)

            # Other Ethernet
            elif LIVEPRINT:
                printOtherETH(eth)

            check, x = dataStore.protExists(protocol)
            if check:
                dataStore.packmon[x] = [dataStore.packmon[x][0], dataStore.packmon[x][1]+1]
            else:
                dataStore.packmon.append([protocol, x])


            if eth[0][:8] == "01:00:5E" and MULTICASTCLEAN and sourcePort == 5353:
                if LIVEPRINT: print("MULTICAST CLEAN ON - PACKET DISCARDED") 
            elif BROADCASTCLEAN and eth[0] == "FF:FF:FF:FF:FF:FF":
                if LIVEPRINT: print("BROADCAST CLEAN ON - PACKET DISCARDED")
            else: 
                if eth[0] not in dataStore.destNames:
                    dataStore.destNames.append(eth[0])
                    dataStore.NetworkEntities[eth[0]] = entity(dataStore.destNames.index(eth[0]))
                
                if eth[1] not in dataStore.destNames and eth[1] not in dataStore.sourceNames:
                    dataStore.sourceNames.append(eth[1])
                if not timeBool:
                    rec += 1
                    dataStore.packetRecorded += 1
                    dataStore.packetlength += len(eth[4])
                try:
                    dataStore.NetworkEntities[eth[0]].addPacket(sourcePort, destPort, dataStore.sourceNames.index(eth[1]), destIP, dataStore.protExists(eth[2])[1], eth[4])
                except:
                    dataStore.NetworkEntities[eth[0]].addPacket(sourcePort, destPort, dataStore.destNames.index(eth[1]), destIP, dataStore.protExists(eth[2])[1], eth[4])
            if (time.time())-t >= captureTime and timeBool:
                rec = count+1
                

    except BaseException as e:
        print(f"Capture Fails: {e}")

parser = argparse.ArgumentParser(description="Network Mapping and Packet Analysis tool")
addArgs(parser)
args = parser.parse_args()

if args.PACKET_NUM and args.CAPTURE_TIME:
    parser.error("Cannot specify both a number of packets to capture and a time to capture for.")

if not args.PACKET_NUM and not args.CAPTURE_TIME:
    parser.error("Please specify an packet capture count with the -n or --packet-num option.")

if not args.INTERFACE:
    parser.error("Please specify an interface to sniff with the -i or --interface option.")

if args.CAPTURE_TIME:
    timeBool = True
else:
    timeBool = False

MULTICASTCLEAN = args.MULTICAST
BROADCASTCLEAN = args.BROADCAST
LIVEPRINT = args.PRINT
interface = args.INTERFACE

asciiArt()

if timeBool:
    main(10, int(args.CAPTURE_TIME), timeBool)
else:
    main(int(args.PACKET_NUM), 10, timeBool)

m = dataNetwork(dataStore, 'network.html', args.NON_CONTRIB)

printSummary(dataStore, args.INTERFACE)
dataQueryForm(dataStore)