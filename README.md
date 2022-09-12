# Tracket-Pacer
Y11 Computer Science Project

Network Mapping Tool
## Usage
```
usage: tracketpacer.py [-h] [-n PACKET_NUM] [-t CAPTURE_TIME] [-print] [-mc] [-bc] [-nc] [-i INTERFACE]

Network Mapping and Packet Analysis tool

options:
  -h, --help            show this help message and exit
  -n PACKET_NUM, --packet-num PACKET_NUM
                        The number of packets used to make the network map.
  -t CAPTURE_TIME, --capture-time CAPTURE_TIME
                        The length of time in which to capture packets
  -print, --liveprint   Enables live output of packet information
  -mc, --multicast      Enables multicast packet recording and maping.
  -bc, --broadcast      Enables broadcast packet recording and maping.
  -nc, --non-contributary
                        Enables the display of non-contributary entities on the graph.
  -i INTERFACE, --interface INTERFACE
                        Specifies the network interface to listen on.
```
Example:
```
sudo python tracketpacer.py -i wlan0 --packet-num 10 -mc -bc
```
