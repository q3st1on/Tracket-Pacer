class entity:
    def __init__(self, mac):
        self.mac = mac
        self.packets = []
        self.packetCount = 0
        self.comms = {}


    def addPacket(self, sourcePort, destPort, sourceMac, destIP, protocol, data):
        if not sourceMac in self.comms:
            self.comms[sourceMac] = 1
        else:
            self.comms[sourceMac] = self.comms[sourceMac]+1

        self.packets.append({
            'Source Port': sourcePort,
            'Source MAC': sourceMac,
            'Dest Port': destPort,
            'Dest IP': destIP,
            'Protocol': protocol,
            'Data': data
        })
        self.packetCount += 1
    
    def getPacketInfo(self, packet):
        return({
            'Source Port': self.packets[packet]['Source Port'],
            'Dest Port': self.packets[packet]['Dest Port'],
            'Source MAC': self.packets[packet]['Source MAC'],
            'Dest IP': self.packets[packet]['Dest IP'],
            'Protocol': self.packets[packet]['Protocol']
        })
    
    def getPacketBytes(self, packet):
        return self.packets[packet]['Data']