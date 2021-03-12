set -x

#/usr/bin/mixerctl outputs.master=200,200
/usr/bin/sndioctl output.level=1

cd ~/src/callerID
/usr/local/bin/python3.8 callBlock.py &
