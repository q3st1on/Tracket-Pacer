from utils.utils import formatMultiLine, COLOURS, FORMAT, printLines

def http(rawData):
    try:
        data = rawData.decode('utf-8')
    except:
        data = rawData
    return data

def printHTTP(tcp):
    printList = []
    printList.append('{} -HTTP Data:'.format(FORMAT.TAB_2))
    try:
        http = http(tcp[10])
        http_info = str(http[10]).split('\n')
        for line in http_info:
            printList.append(FORMAT.TAB_3 + str(line))
    except:
        printList.extend(formatMultiLine(FORMAT.TAB_3, tcp[10]))
    printLines(printList)