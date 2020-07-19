import sys, time



cidDate = ''
cidTime = ''
cidNMBR = ''



def parseCallerID(line):
    
    if 'OK' in line:
        return([0, 'ok'])

    if 'MESG' in line:
        return([1, 'mesg'])

    if 'RING' in line:
        return([0, 'ring'])

    if 'DATE' in line:
        date = line.split('=')
        cidDate = date[1][0:2] + '/' + date[1][2:4]
        cidDate = cidDate.strip()
        return([0, 'date', cidDate])

    if 'TIME' in line:
        time = line.split('=')
        cidTime = time[1][0:2] + ':' + time[1][2:4]
        cidTime = cidTime.strip()
        return([0, 'time', cidTime])
        
    if 'NAME' in line:
        name = line.split('=')
        cidName = name[1]
        cidName = cidName.strip()
        return([0, 'name', cidName])
        
    if 'NMBR' in line:
        nmbr = line.split('=')
        cidNMBR = nmbr[1]
        cidNMBR = cidNMBR.strip()
        return([0, 'nmbr', cidNMBR])

    return([1, 'no token'])



def main(argv):
    fd = open('data_test/callerIDInputTest.txt', 'r')
    modemReceive = fd.readlines()
    fd.close()

    for lineIn in modemReceive:
        line = lineIn.strip()
        if lineIn == '':
            continue
    
        response = parseCallerID(line)
        if response[1] == 'ring':
            continue
        if response[1] == 'no token':
            continue
        print('validate() resp: ', response)
    
if __name__ == "__main__":
    main(sys.argv)
