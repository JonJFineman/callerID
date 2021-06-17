set -x

#/usr/bin/mixerctl outputs.master=200,200
/usr/bin/sndioctl output.level=1

cd ~/src/callerID
/bin/mv logs/callerID.log logs/callerID.log.txt
/usr/bin/mail -s "call logs" jjf < logs/callerID.log.txt

/usr/local/bin/python3.8 callBlock.py --email someid@someisp.com &
