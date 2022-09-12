from typing import TypeGuard, Union
from argparse import *
import textwrap
import math

class COLOURVALS:
    def __init__(self):
        self.WHITE = '\033[0m'
        self.RED = '\033[31m'
        self.GREEN = '\033[32m'
        self.ORANGE = '\033[93m'
        self.BLUE = '\033[34m'
        self.PURPLE = '\033[35m'
        self.CYAN = '\033[36m'
        self.GRAY = '\033[37m'
        self.TAN = '\033[93m'

class FORMATVALS:
    def __init__(self):
        self.TAB_1 = '\t'
        self.TAB_2 = '\t\t'
        self.TAB_3 = '\t\t\t'
        self.TAB_4 = '\t\t\t\t'
        self.BRD_STR = 117*'='

class Data:
    def __init__(self):
        self.destNames = []
        self.sourceNames = []
        self.NetworkEntities = {}
        self.packetRecieved = 0
        self.packetRecorded = 0
        self.packetlength = 0
        self.packmon = []

    def protExists(self, protocol: Union[str, int]) -> TypeGuard[list[bool, int]]:
        for x in range(len(self.packmon)):
            if protocol in self.packmon[x]:
                return [True, x]
        return [False, 1]
    
    def genNames(self):
        self.names = self.destNames + self.sourceNames

COLOURS = COLOURVALS()
FORMAT = FORMATVALS()

def getMacAddr(macRaw: bytes) -> TypeGuard[str]:
    byteStr = map('{:02x}'.format, macRaw)
    macAddr = ':'.join(byteStr).upper()
    return macAddr

def formatMultiLine(prefix: str, string: str, size=80) -> TypeGuard[list[str]]:
    size -= len(prefix)
    if isinstance(string, bytes):
        string = ''.join(r'\x{:02x}'.format(byte) for byte in string)
        if size % 2:
            size -= 1
    return [prefix + line for line in textwrap.wrap(string, size)]

def getIp(addr: bytes) -> TypeGuard[str]:
    return '.'.join(map(str, addr))

def addBoolArg(parser: ArgumentParser, short: str, name: str, helpText: str, Destination: str):
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-'+short, '--' + name, dest=Destination, action='store_true', help=helpText)
    parser.set_defaults(**{name:False})

def addArgs(parser: ArgumentParser):
    parser.add_argument('-n', '--packet-num', dest='PACKET_NUM', help="The number of packets used to make the network map.")
    parser.add_argument('-t', '--capture-time', dest='CAPTURE_TIME', help="The length of time in which to capture packets")
    addBoolArg(parser, 'print', 'liveprint', "Enables live output of packet information", Destination='PRINT')
    addBoolArg(parser, 'mc', 'multicast', "Enables multicast packet recording and maping.", Destination='MULTICAST')
    addBoolArg(parser, 'bc', 'broadcast', "Enables broadcast packet recording and maping.", Destination='BROADCAST')
    addBoolArg(parser, 'nc', 'non-contributary', "Enables the display of non-contributary entities on the graph.", Destination='NON_CONTRIB')
    parser.add_argument('-i', '--interface', dest='INTERFACE', help="Specifies the network interface to listen on.")

def asciiArt():
    dollarColour = COLOURS.RED
    bdrStr = 117*'='
    asciiStr = '''


  {a}$$$$$$$${b}\\                           {a}$${b}\\                  {a}$${b}\\     {a}$$$$$$${b}\\
  \\__{a}$${b}  __|                          {a}$${b} |                 {a}$${b} |    {a}$${b}  __{a}$${b}\\
     {a}$${b} | {a}$$$$$${b}\\  {a}$$$$$${b}\\   {a}$$$$$$${b}\\ {a}$${b} |  {a}$${b}\\  {a}$$$$$${b}\\ {a}$$$$$${b}\\   {a}$${b} |  {a}$${b} |{a}$$$$$${b}\\   {a}$$$$$$${b}\\  {a}$$$$$${b}\\   {a}$$$$$${b}\\
     {a}$${b} |{a}$${b}  __{a}$${b}\\ \\____{a}$${b}\\ {a}$${b}  _____|{a}$${b} | {a}$${b}  |{a}$${b}  __{a}$${b}\\\\_{a}$${b}  _|  {a}$$$$$$${b}  |\\____{a}$${b}\\ {a}$${b}  _____|{a}$${b}  __{a}$${b}\\ {a}$${b}  __{a}$${b}\\
     {a}$${b} |{a}$${b} |  \\__|{a}$$$$$$${b} |{a}$${b} /      {a}$$$$$${b}  / {a}$$$$$$$${b} | {a}$${b} |    {a}$${b}  ____/ {a}$$$$$$${b} |{a}$${b} /      {a}$$$$$$$${b} |{a}$${b} |  \\__|
     {a}$${b} |{a}$${b} |     {a}$${b}  __{a}$${b} |{a}$${b} |      {a}$${b}  _{a}$${b}<  {a}$${b}   ____| {a}$${b} |{a}$${b}\\ {a}$${b} |     {a}$${b}  __{a}$${b} |{a}$${b} |      {a}$${b}   ____|{a}$${b} |
     {a}$${b} |{a}$${b} |     \\{a}$$$$$$${b} |\\{a}$$$$$$${b}\\ {a}$${b} | \\{a}$${b}\\ \\{a}$$$$$$${b}\\  \\{a}$$$${b}  |{a}$${b} |     \\{a}$$$$$$${b} |\\{a}$$$$$$${b}\\ \\{a}$$$$$$${b}\\ {a}$${b} |
     \\__|\\__|      \\_______| \\_______|\\__|  \\__| \\_______|  \\____/ \\__|      \\_______| \\_______| \\_______|\\__|
                                                                                                                   
'''.format(a = dollarColour, b = COLOURS.WHITE)
    printLines([('{}\n{}\n{}'.format(bdrStr, asciiStr, bdrStr))])

def intlen(n: int) -> TypeGuard[int]:
    if n > 0:
        digits = int(math.log10(n))+1
    elif n == 0:
        digits = 1
    else:
        digits = int(math.log10(-n))+2
    return digits

def printLines(n: list[str]):
    for i in n:
        print(i)

def printSummary(dataStore: Data, interface: str):   
    dataStore.genNames()
    collumn1 = [
        '            Packets recieved: {}{}{}'.format(COLOURS.GREEN, dataStore.packetRecieved, COLOURS.WHITE),
        '            Packets recorded: {}{}{}'.format(COLOURS.GREEN, dataStore.packetRecorded, COLOURS.WHITE),
        '           Packets discarded: {}{}{}'.format(COLOURS.GREEN, dataStore.packetRecieved-dataStore.packetRecorded, COLOURS.WHITE),
        ' Unique network destinations: {}{}{}'.format(COLOURS.GREEN, len(dataStore.destNames), COLOURS.WHITE),
        '      Unique network sources: {}{}{}'.format(COLOURS.GREEN, len(set(dataStore.names)), COLOURS.WHITE),
        '     Unique network entities: {}{}{}'.format(COLOURS.GREEN, len(dataStore.NetworkEntities), COLOURS.WHITE) 
    ] 

    for i in range(6):
        diff = 46 - (len(collumn1[i]))
        collumn1[i] = collumn1[i]+(diff*' ')

    collumn2 = [[' No. {} packets'.format(x), ' {}{}{}'.format(COLOURS.GREEN, x, COLOURS.WHITE)] for x in next(zip(*dataStore.packmon))]
    collumn2 = [['Average Data Length',' {}{}{}'.format(COLOURS.GREEN, dataStore.packetlength//dataStore.packetRecorded, COLOURS.WHITE)]] + collumn2
    c2len = len(max(collumn2, key=lambda x: len(x[0]))[0])

    for i in range(6):
        if i < len(collumn2):
            d1 = c2len - len(collumn2[i][0])
            d2 = 45-(c2len+len(collumn2[i][1]))
            collumn2[i] = (d1*' ') + ':'.join(collumn2[i]) + (d2*' ')
        else:
            collumn2.append(37*' ')

    maxName = max(dataStore.destNames, key=lambda x: dataStore.NetworkEntities[x].packetCount)
    maxCount = dataStore.NetworkEntities[maxName].packetCount
    maxpartner = max(dataStore.NetworkEntities[maxName].comms, key=dataStore.NetworkEntities[maxName].comms.get)

    collumn3 = [
        ' Most Active Entity: {}{}{}'.format(COLOURS.GREEN, maxName, COLOURS.WHITE),
        '   Packets Recieved: {}{}{}'.format(COLOURS.GREEN, maxCount, COLOURS.WHITE),
        '   Talked Most With: {}{}{}'.format(COLOURS.GREEN, dataStore.destNames[maxpartner], COLOURS.WHITE)
    ]

    for i in range(6):
        if i < len(collumn3):
            diff = 48-(len(collumn3[i]))
            collumn3[i] = collumn3[i]+diff*' '
        else:
            collumn3.append(39*' ')

    def headPad(d: int, h: str) -> TypeGuard[str]:
        if d %2 == 0:
            h = (d//2)*' '+h+(d//2)*' '
        else:
            h = (d//2)*' '+h+((d//2)+1)*' '
        return h

    intfStr = '|'+headPad(104 - len(interface), "Interface: {}{}{}".format(COLOURS.PURPLE, interface, COLOURS.WHITE))+'|'
    entsStr = '|'+headPad(101, "{}Known Entities{}".format(COLOURS.CYAN, COLOURS.WHITE))+'|'

    c1head = headPad(len(collumn1[0])-26, '{}RECORDING SUMMARY{}'.format(COLOURS.TAN, COLOURS.WHITE))
    c2head = headPad(len(collumn2[0])-23, '{}PACKET SUMMARY{}'.format(COLOURS.TAN, COLOURS.WHITE))
    c3head = headPad(len(collumn3[0])-28, '{}MAIN ENTITY SUMMARY{}'.format(COLOURS.TAN, COLOURS.WHITE))

    collumn1 = [c1head, 37*'-'] + collumn1
    collumn2 = [c2head, 37*'-'] + collumn2
    collumn3 = [c3head, 39*'-'] + collumn3

    collumns = list(map(lambda x, y, z: '|'+x+'|'+y+'|'+z+'|', collumn1, collumn2, collumn3))

    entlist = [i for i in dataStore.NetworkEntities]
    entLen = len(entlist)
    for i in range(entLen):
        var = f" {(intlen(entLen)-intlen(i))*' '+str(i)+': '}{entlist[i]}"
        var = var + (28-len(var))*' '
        entlist[i] = COLOURS.PURPLE+var.split(":")[0]+COLOURS.WHITE+':'+COLOURS.GREEN+':'.join(var.split(":")[1:])+COLOURS.WHITE

    ents = ['|'+entlist[(4*i)]+'|'+entlist[(4*i)+1]+'|'+entlist[(4*i)+2]+'|'+entlist[(4*i)+3]+'|' for i in range(entLen//4)]
    
    if len(ents)*4 < entLen:
        index = (entLen//4)*4
        working = []
        for i in range(4):
            if index+i < entLen:
                working.append(entlist[index+i])
            else:
                working.append(28*' ')
        ents.append('|'+working[0]+'|'+working[1]+'|'+working[2]+'|'+working[3]+'|')
    
    printList = []
    printList.append('{}\n{}\n{}'.format(FORMAT.BRD_STR, intfStr, FORMAT.BRD_STR))
    printList.append('{}\n{}'.format(collumns[0], collumns[1]))
    printList.append('{}\n{}\n{}\n{}\n{}\n{}'.format(collumns[2], collumns[3], collumns[4], collumns[5], collumns[6], collumns[7]))
    printList.append('{}\n{}\n{}'.format(FORMAT.BRD_STR, entsStr, FORMAT.BRD_STR))
    printList.extend(ents)
    printList.append(FORMAT.BRD_STR)
    printLines(printList)

def dataQueryForm(dataStore):
    ents = [i for i in dataStore.NetworkEntities]
    while True:
        try:
            ent = input("{}What entity would you like to see: {}".format(COLOURS.WHITE, COLOURS.GREEN)).upper()
            if ent in ['QUIT', 'QUIT()', 'EXIT', 'EXIT()']:
                break
            try:
                if ent.isnumeric():
                    if int(ent) < len(ents):
                        ent = ents[int(ent)]
                    else:
                        raise Exception("{}{}{} out of range of known entities".format(COLOURS.GREEN, ent, COLOURS.WHITE))
                if ent in dataStore.NetworkEntities:
                    titleStr = '{}{}{} Recieved {}{}{} Packets'.format(COLOURS.GREEN, ent, COLOURS.WHITE, COLOURS.TAN, dataStore.NetworkEntities[ent].packetCount, COLOURS.WHITE)
                    diff = 133-len(titleStr)
                    if diff %2 == 0:
                        titleStr = '|'+(diff//2)*' '+titleStr+(diff//2)*' '+'|'
                    else:
                        titleStr = '|'+(diff//2)*' '+titleStr+((diff//2)+1)*' '+'|'
                    
                    comms = []
                    for i in dataStore.NetworkEntities[ent].comms:
                        var = "{}: {}".format(i, dataStore.NetworkEntities[ent].comms[i])
                        var = " {}{}{}: {}{}{}{}".format(COLOURS.GREEN, ':'.join(var.split(':')[:-1]), COLOURS.WHITE, COLOURS.TAN, var.split(':')[-1], COLOURS.WHITE, (26-len(var))*' ')
                        comms.append(var)

                    commslist = ['|'+comms[(4*i)]+'|'+comms[(4*i)+1]+'|'+comms[(4*i)+2]+'|'+comms[(4*i)+3]+'|' for i in range(len(comms)//4)]
                    
                    if len(commslist)*4 < len(comms):
                        index = ((len(comms)//4)*4)
                        working = []
                        for i in range(4):
                            if index+i < len(comms):
                                working.append(comms[index+i])
                            else:
                                working.append(28*' ')
                        commslist.append('|'+working[0]+'|'+working[1]+'|'+working[2]+'|'+working[3]+'|')

                    printList = []
                    printList.append(COLOURS.WHITE+FORMAT.BRD_STR)
                    printList.append(titleStr)
                    printList.append(FORMAT.BRD_STR)
                    printList.append('|'+50*' '+"{}COMMUNICATIONS{}".format(COLOURS.TAN, COLOURS.WHITE)+51*' '+'|')
                    printList.append('|'+28*'-'+'|'+28*'-'+'|'+28*'-'+'|'+28*'-'+'|')
                    printList.extend(commslist)
                    printList.append(FORMAT.BRD_STR)
                    printLines(printList)
                else:
                    raise Exception("{}{}{} not a known entity.".format(COLOURS.GREEN, ent, COLOURS.WHITE))
            except BaseException as e:
                printLines([e])
        except BaseException as e:
            printLines([f"{COLOURS.WHITE}{e}"])
            break