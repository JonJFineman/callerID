import sys
import argparse

import logging
import re
import vobject



for arg in sys.argv:
    print(arg)

# get/parse arguments
parser = argparse.ArgumentParser(description='caller ID blocker')
parser.add_argument('--vcardIn', required=False, default='data/complete.vcf', help='input vcard file')
parser.add_argument('--vcardOut', required=False, default='data/listBook_new.txt', help='output vcard file')
parser.add_argument('--log', required=False, default='logs/vcard.log', help='log file')

args = parser.parse_args()
print(  args.vcardIn, '\n', \
        args.vcardOut, '\n', \
        args.log )



logFileName = args.log
vcardIn = args.vcardIn
vcardOut = args.vcardOut



# open log file
logging.basicConfig(filename = logFileName, format='[%(levelname)s] %(asctime)s **** %(message)s')
log = logging.getLogger()
log.setLevel(logging.DEBUG)

log.critical('test-env: critical')
log.error('test-env: error')
log.warning('test-env: warning')
log.info('test-env: info')
log.debug('test-env: debug')



fdBook = open(vcardOut, 'w')

with open(vcardIn, 'r') as fd:
    inCard = fd.read()
    vcardlist = vobject.readComponents(inCard)
    for vcard in vcardlist:
        #print(vcard)
        #print(vcard.prettyPrint)
        try:
            vName = vcard.contents['fn']
            vNumber = vcard.contents['tel']
        except Exception as e:
            log.warning('no tel for: {}'.format(vName[0].value))
            continue
        for num in vNumber:
            vNumber = num.value
            vNumber = re.sub(r'\+1', '', vNumber)
            vNumber = re.sub(r'\D', '', vNumber)
            print('NMBR={};NAME={}'.format(vNumber,vName[0].value))
            fdBook.write( 'NMBR={};NAME={}'.format(vNumber,vName[0].value) + '\n' )

fdBook.close()

