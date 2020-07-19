import sys, time, serial, signal
import fcntl
import re
import logging
import argparse

from vallidatePhoneNumber import validateNumber
from parseCallerID import parseCallerID
from announceCall import *



for arg in sys.argv:
    print(arg)

# get/parse arguments
parser = argparse.ArgumentParser(description='caller ID blocker')
parser.add_argument('--port', required=False, default='/dev/ttyU0', help='port')
parser.add_argument('--bus', required=False, default='001', help='modem bus')
parser.add_argument('--device', required=False, default='004', help='modem device')
parser.add_argument('--book', required=False, default='data/listBook.txt', help='addr book')
parser.add_argument('--silent', required=False, default='data/listSilent.txt', help='silent book')
parser.add_argument('--block', required=False, default='data/listBlock.txt', help='block book')
parser.add_argument('--log', required=False, default='logs/callerID.log', help='log file')

args = parser.parse_args()
print(  args.port, '\n', \
        args.bus, '\n', \
        args.device, '\n', \
        args.book, '\n', \
        args.silent, '\n', \
        args.block, '\n', \
        args.log )





modemPort = args.port
modemBus = args.bus
modemDevice = args.device
modemUSBDevice = '/dev/bus/usb/' + modemBus + '/' + modemDevice
# MODEM commands
mInit = 'ATZ'
mTurnOnCallerID = 'AT#CID=1'
mHangUp = 'ATH0'
mAnswerVoice = 'ATA'
mAnswerData = 'ATA'
mAnsewrFax = 'AT+FSCLASS=1'
mBreak = '+++'
mLineTerminator = b'\r\n'



# files
CALLER_ID_LOG = args.log
LIST_BOOK     = args.book
LIST_SILENT   = args.silent
LIST_BLOCK    = args.block


# open log file
logging.basicConfig(filename = CALLER_ID_LOG, format='[%(levelname)s] %(asctime)s **** %(message)s')
log = logging.getLogger()
log.setLevel(logging.DEBUG)

log.critical('test-env: critical')
log.error('test-env: error')
log.warning('test-env: warning')
log.info('test-env: info')
log.debug('test-env: debug')


listSilent = []
listBlock = []
listBook = []



def sig_handler(signum, frame):
    global listSilent, listBlock, listBook
    print('Got Signal: ', signum)
    log.info('Got Signal {}, re-reading phone books'.format(signum))
    
    # read phone book, call silent list, call block list
    listSilent = readSilentList()
    print('silent: ', listSilent)
    log.info('silent: {}'.format(listSilent))

    listBlock = readBlockList()
    print('block: ', listBlock)
    log.info('block: {}'.format(listBlock))

    listBook = readPhoneBook()
    #print('book: ', listBook)
    log.info('book: {}'.format(listBook))



def resetUSB(USBDevice):
    USBDEVFS_RESET= 21780

    print("resetting driver:", USBDevice)
    log.info('resetting driver: {}'.format(USBDevice))

    try:
        f = open(USBDevice, 'w', os.O_WRONLY)
        fcntl.ioctl(f, USBDEVFS_RESET, 0)
    except Exception as msg:
        print("failed to reset device: ", msg)
        log.error('failed to reset device: {}'.format(msg))
    
    print("reset driver")
    log.info('reset driver')

    
    
def putModem(ser, line):
    line = line + '\r\n'
    ser.write(line.encode('ascii'))
    ser.flush()
    log.debug('putModem: {}'.format(line))

    #time.sleep(1)
    # need read loop
    # can you turn on/off read timeout?
    #ser.timeout = 1    
    response = getModem(ser)
    print('Modem Responded: ', response)
    log.debug('Modem Responded: {}'.format(response))



def getModem(ser):
    line = ser.readline().decode('ascii')
    #line = ser.read(size=64).decode('ascii')
    line = line.strip()
    log.debug('getModem: {}'.format(line))
    return(line)



def resetInputBuffer(ser):
    ser.reset_input_buffer()
    print('Modem input buffer reset')
    log.debug('Modem input buffer reset')
    return()



def actionHangUpRelay(modemSer):
    # False sets RTS output high, True low
    print('HU Relay going off hook')
    log.debug('HU Relay going off hook')
    ser = serial.Serial(modemPort, timeout=None)
    ser.setRTS(value=1)
    time.sleep(10)
    ser.setRTS(value=0)
    ser.close()
    print('HU Relay going on hook')
    log.debug('HU Relay going on hook')



def actionHangUp(ser):
    # first answer
    line = mAnswerData + '\r\n'
    ser.write(line.encode('ascii'))
    ser.flush()
    log.debug('hang up: answer call: {}'.format(line))
    print('HU send answer')
    time.sleep(4)
    resetInputBuffer(ser)

    # then hang up by interrupting modem
    line = '\r\n'
    ser.write(line.encode('ascii'))
    ser.flush()
    log.debug('hang up: send crlf')
    print('HU send null string')
    time.sleep(2)
    resetInputBuffer(ser)

    # then hang up by ah0 command
    line = mHangUp + '\r\n'
    ser.write(line.encode('ascii'))
    ser.flush()
    log.debug('hang up: HU cmd: {}'.format(line))
    print('HU send hang up cmd')
    time.sleep(2)
    resetInputBuffer(ser)
    
    

def cleanUpModemResponse(line):
    number = re.sub(r'\D', '', line)
    return(number)
        
        
        
def readPhoneBook():
    fd = open(LIST_BOOK, 'r')
    lines = fd.readlines()
    fd.close()
    
    phoneList = []
    for line in lines:
        line = line.strip()
        if line == '' or '#' in line:
            continue
        entry =  line.split(';')
        number = entry[0].split('=')
        name   = entry[1].split('=')
        newEntry = number[1].lower() + ':' + name[1].lower()
        phoneList.append(newEntry)
        
    return(phoneList)



def readSilentList():
    fd = open(LIST_SILENT, 'r')
    lines = fd.readlines()
    fd.close()
    
    phoneList = []
    for line in lines:
        line = line.strip()
        if line == '' or '#' in line:
            continue
        entry =  line.split(';')
        number = entry[0].split('=')
        name   = entry[1].split('=')
        newEntry = number[1].lower() + ':' + name[1].lower()
        phoneList.append(newEntry)
        
    return(phoneList)



def readBlockList():
    fd = open(LIST_BLOCK, 'r')
    lines = fd.readlines()
    fd.close()
    
    phoneList = []
    for line in lines:
        line = line.strip()
        if line == '' or '#' in line:
            continue
        entry =  line.split(';')
        number = entry[0].split('=')
        name   = entry[1].split('=')
        newEntry = number[1].lower() + ':' + name[1].lower()
        phoneList.append(newEntry)
        
    return(phoneList)



def checkPhoneList(number, name, book):
    for i in book:
        n = i.split(':')
        if number == n[0]:
            log.debug('checkPhoneList for {}, found: {}, {}'.format(number, n[0], n[1]))
            return([True, n[0], n[1]])
        
    # if number not found check name and see if it has * for number
    #for i in book:
    #    n = i.split(':')
    #    if name == n[1] and '*' == n[0]:
    #        return(True)

    log.debug('checkPhoneList no match: {}, {}'.format(number, name))
    return([False,'',''] )



def checkSilentList(number, name, book):
    for i in book:
        n = i.split(':')
        if number == n[0]:
            log.debug('checkSilentList for {}, found: {}, {}'.format(number, n[0], n[1]))
            return([True, n[0], n[1]])
        
    # if number not found check name and see if it has * for number
    #for i in book:
    #    n = i.split(':')
    #    if name == n[1] and '*' == n[0]:
    #        return(True)

    log.debug('checkSilentList no match: {}, {}'.format(number, name))
    return([False,'',''] )



def checkBlockList(number, name, book):
    for i in book:
        n = i.split(':')
        if number == n[0]:
            log.debug('checkBlockList for {}, found: {}, {}'.format(number, n[0], n[1]))
            return([True, n[0], n[1]])
        
    # if number not found check name and see if it has * for number
    for i in book:
        n = i.split(':')
        if name == n[1] and '*' == n[0]:
            log.debug('checkBlockList for {}, found: {}, {}'.format(name, n[0], n[1]))
            return([True, n[0], n[1]])

    log.debug('checkBlockList no match: {}, {}'.format(number, name))
    return([False,'',''] )
        
        

def main(argv):
    global listSilent, listBlock, listBook

    # open unknown number file

    # if lost modem connection retry 10 times

    # initialize modem
    #try:
        #ser = serial.Serial('/dev/ttyACM0', timeout=5)
    ser = serial.Serial(modemPort, timeout=None)
    #ser.reset_input_buffer()
    resetInputBuffer(ser)
    print('Connected to MODEM at: ', ser.name)
    log.info('Connected to MODEM at: {}'.format(ser.name))
    #except Exception as e:
        #print ("Exception: Opening modem: " + str(e))

    #try:
    print('Sending MODEM: ', 'init')
    log.info('Sending MODEM: init')
    putModem(ser, mInit)
    #time.sleep(0.5)
    print('Sending MODEM: ', 'turn on caller id')
    log.info('Sending MODEM: turn on caller id')
    putModem(ser, mTurnOnCallerID)
    #time.sleep(0.5)

    #except Exception as e:
        #print ("Exception: Initializing modem: " + str(e))



    # read phone book, call silent list, call block list
    listSilent = readSilentList()
    print('silent: ', listSilent)
    log.info('silent: {}'.format(listSilent))

    listBlock = readBlockList()
    print('block: ', listBlock)
    log.info('block: {}'.format(listBlock))

    listBook = readPhoneBook()
    #print('book: ', listBook)
    #log.debug('book: {}'.format(listBook))

    # main loop
    intervalTOD = 15
    currentTOD = previousTOD = time.time()
    mName = ''
    mNumber = ''
    bell = False
    nameInBook = False
    gotName = gotNumber = gotRing = False
    firstTime = True
    while True:
        if firstTime:
            firstTime = False
        else:
            pass
        
        # read modem for call status
        mInput = getModem(ser)
        if mInput == '':
            log.debug('modem sent blank line')
            continue
        print('modem sent: ', mInput)
        log.info('modem sent: {}'.format(mInput))

        # parse modem input
        # [0] status code
        # [1] token
        # [3] value
        ret = parseCallerID(mInput)
        if ret[1] == 'ok':
            log.error('not sure why we got ok: {}'.format(mInput))
            continue
        
        if ret[1] == 'mesg':
            log.critical('modem not configured properly: {}'.format(mInput))
            break
        
        if ret[0] != 0:
            log.error('parse token failure: {}'.format(mInput))
            continue
        
        if ret[1] == 'ring':
            gotName = gotNumber = False
            mName = mNumber = ''
            currentTOD = time.time()
            if currentTOD - previousTOD <= intervalTOD:
                if bell == True:
                    log.info('incoming call, ringing bell')
                    # jjf ringBell(nameInBook)
            gotRing = True
            log.info('incoming call')
            continue
        
        if ret[1] == 'date':
            mDate = ret[2]
            log.info('incoming date: {}'.format(mDate))
            continue
        
        if ret[1] == 'time':
            mTime = ret[2]
            log.info('incoming time: {}'.format(mTime))
            continue
        
        if ret[1] == 'name':
            mName = ret[2].lower()
            gotName = True
            log.info('incoming name: {}'.format(mName))
            #continue
        
        if ret[1] == 'nmbr':
            mNumber = ret[2]
            gotNumber = True
            log.info('incoming nmbr: {}'.format(mNumber))
            
        # wait until we have both name and number
        if gotName == True and gotNumber == True:
            gotName = gotNumber = False
            nameInBook = False
            previousTOD = time.time()
            log.debug('got number and name {}, {}'.format(mNumber, mName))
            
            # validate area code and NPA rules
            ret = validateNumber(mNumber)
            if ret[0] != 0:
                print(ret)
                log.info(ret)
                bell = False
                nameInBook = False
                #actionHangUpRelay(ser)
                actionHangUp(ser)
                continue

            # check number
            # if both name and number are null skip announcing
            if mName == '' and mNumber == '':
                log.info('name={}, number={}, skipping'.format(mName, mNumber))
                bell = False
                nameInBook = False
                continue
            
            #
            # check phone book, if found announce
            #
            listName = ''
            log.debug('checking for book number:{}:, name:{}:'.format(mNumber, mName))
            ret = checkPhoneList(mNumber, mName, listBook)
            if ret[0] == True:
                listName = ret[2]
                print('book found: ', mNumber, listName)
                log.info('book found: {} {}'.format(mNumber, listName))
                # call announce routine
                log.info('announcing: {}, {}'.format(mNumber, listName))
                # jjf announceCallerFestival(mNumber, listName)
                # and announce again 
                #announceCallerFestival(mNumber, listName)
                announceCallerESpeak(mNumber, listName)
                # announce second time
                announceCallerESpeak(mNumber, listName)
                bell = True
                nameInBook = True
                continue

            #
            # check block list, if found hang up
            #
            log.debug('checking for block number:{}:, name:{}:'.format(mNumber, mName))
            ret = checkBlockList(mNumber, mName, listBlock)
            if ret[0] == True:
                listName = ret[2]
                print('block found: ', mNumber, listName)
                log.info('block found: {} {}'.format(mNumber, listName))
                #actionHangUpRelay(ser)
                actionHangUp(ser)
                bell = False
                nameInBook = False
                #ser.close()
                #resetUSB(modemUSBDevice)
                #ser.open()
                continue
        
            #
            # check silent list, if found don't announce
            #
            log.debug('checking for silent number:{}:, name:{}:'.format(mNumber, mName))
            ret = checkSilentList(mNumber, mName, listSilent)
            if ret[0] == True:
                listName = ret[2]
                print('silent found: ', mNumber, listName)
                log.info('silent found: {} {}'.format(mNumber, listName))
                bell = False
                nameInBook = False
                continue
        
            #
            # announce once if unsolicited 
            #
            log.info('announcing: {}, {}'.format(mNumber, listName))
            # jjf announceCallerFestival(mNumber, listName)
            announceCallerESpeak(mNumber, mName)
            bell = True
            log.info('incoming call, ringing bell')
            # jjf ringBell(nameInBook)
        
            #
            # prompt to leave a message ???
            #
        
    # bottom of main loop
    
    
    
if __name__ == "__main__":
    
    # define signal
    signal.signal(signal.SIGUSR1, sig_handler)

    main(sys.argv)

