set -x

rm data/vcard_download.txt
cat /home/jjf/vdirsyncer/contacts/jjf/Default/*.vcf >  data/vcard_download.txt
cat /home/jjf/vdirsyncer/contacts/mmf/Default/*.vcf >> data/vcard_download.txt
