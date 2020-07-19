set -x

/usr/bin/mixerctl outputs.master=200,200

cd ~/src/callerID
/usr/local/bin/python3 callBlock.py &
