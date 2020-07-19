

#fd = open('data/listBook.txt', 'rb')
fd = open('data/complete.vcf', 'rb')

i = 1
while True:
    c = fd.read(1)
    if not c:
        print('end of file')
        break
    if ord(c) > 128:
        print('bad char: ', i, c)
    i += 1

fd.close()
