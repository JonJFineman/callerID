import sys
import re



def validateNumber(number):
    
    #phEdit = number.replace('-', '')
    phEdit = re.sub(r'\D', '', number)

    numberLen = len(phEdit)
    #print('phEdit len', numberLen)
    if numberLen < 7:
        return([1,'  bad len: {}'.format(numberLen)])

    
    
    npa = '   '
    nxx = '   '
    
    if numberLen == 10:
        npa = phEdit[0:3]
        nxx = phEdit[3:6]
        lin = phEdit[6:10]
        
    if numberLen == 7:
        nxx = phEdit[0:3]
        lin = phEdit[3:7]

    
    
    npa = npa.strip()
#    if len(npa.strip()) > 0 or len(npa.strip()) < 3:
#        #return([0,'  missing npa: {}'.format(npa)])
#        print('  missing npa: {}'.format(npa))
    
#    if len(npa.strip()) < 3 or npa.strip() == '':
#        return([1,'  bad npa: {}'.format(npa)]) 
    
    if len(nxx.strip()) < 3 or nxx.strip() == '':
        return([1,'  bad nxx: {}/{}'.format(npa, phEdit)]) 

    if len(lin.strip()) < 4 or lin.strip() == '':
        return([1,'  bad lin: {}/{}'.format(npa, phEdit)]) 

    
    #    
    #print('raw:    ', number, 'edited: ', phEdit, ', ph :' + str(npa) + ': :' + str(nxx) + ': :' + str(lin))
    
    
    # if npa present
    if numberLen == 10:        
        if (npa[0] >= '2' and npa[0] <= '9') == False:
            return([1,'  bad npa n: {}'.format(npa)])
        
        if (npa[1] >= '0' and npa[1] <= '9') == False:
            return([1,'  bad npa p: {}'.format(npa)])
        
        if (npa[2] >= '0' and npa[2] <= '9') == False:
            return([1,'  bad npa a: {}'.format(npa)])


    #
    if (nxx[0] >= '2' and nxx[0] <= '9') == False:
        return([1,'  bad nxx n: {}'.format(nxx)])
        
    if (nxx[1] >= '0' and nxx[1] <= '9') == False:
        return([1,'  bad nxx x: {}'.format(nxx)])
        
    if (nxx[2] >= '0' and nxx[2] <= '9') == False:
        return([1,'  bad nxx x: {}'.format(nxx)])
        
    if (nxx[1] == '1' and nxx[2] == '1') == True:
        return([1,'  warning nxx x & x =1: {}'.format(nxx)])


    #
    if (lin[0] >= '0' and lin[0] <= '9') == False:
        return([1,'  bad lin x1: {}'.format(lin)])
        
    if (lin[1] >= '0' and lin[1] <= '9') == False:
        return([1,'  bad lin x2: {}'.format(lin)])
        
    if (lin[2] >= '0' and lin[2] <= '9') == False:
        return([1,'  bad lin x3: {}'.format(lin)])

    if (lin[3] >= '0' and lin[3] <= '9') == False:
        return([1,'  bad lin x4: {}'.format(lin)])


    # past
    return([0, phEdit, npa, nxx, lin])




def main(argv):
    fd = open('data_test/testList.txt', 'r')
    phList = fd.readlines()
    fd.close()

    for phRaw in phList:
        phRaw = phRaw.strip()
        if phRaw == '' or '#' in phRaw:
            continue
    
        response = validateNumber(phRaw)
        print('validate() resp: ', phRaw, response)
    
if __name__ == "__main__":
    main(sys.argv)
    
    
