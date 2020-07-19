# callerID.py

This uses a USRobitics USB [modem][0] to get caller ID from a Plain Old
Telphone Service (POTS) line.

If the caller ID:

* is not a valid phone number[1] it requests the modem to answer the phone and
  then immediatly [hang up][2] on the caller.
* is on the phonebook list it will announce the caller twice.
* is on the block list it requests the modem to answer the phone and then
  immediatly [hang up][2] on the caller.
* is on the silent list it will not announce the call. These are local numbers
  that regulary get spoofed. While we normally don't get any calls from them we
want to be able to pick up just in case.
* is not on any list it will announce one.

[0]Of course I had thrown out all of my modems long ago!

[1]<https://en.wikipedia.org/wiki/North_American_Numbering_Plan>

[2]Interestingly once I added the hang up feature I got much less calls. I
guess they don't like being forced to play for a call completion. Otherwise
they typically hang up before it goes to voice mail.

I am using Python 3.7.7 on OpenBSD 6.7 release

In addition I installed the following packages:

* py3-pip 3.7 19.1.1.1
* socat
* py3-distutils-extra
* espeak
* py3-serial-3.4


## Software Dependencies

* pyserial
* python-distutils-extra
* vobject
* argparse
* logging


## Hardware Dependencies

* U.S. Robotics USR5637 High-performance V.92 modem 56Kbps USB
  <https://www.newegg.com/u-s-robotics-usr5637-dial-up-modem/p/N82E16825104006?Item=N82E16825104006>


## Installation

	cd ~ # or the parrent of whereever you want to install the software
	git clone git@github.com:JonJFineman/callerID.git

I use vdirsyncer[3] to download my phone book. Alternativly you can manually
download it.

set permissions for:

* OpenBSD: /dev/ttyU0
* Raspbian: /dev/ttyACM0


[3]<http://vdirsyncer.pimutils.org/en/stable/>


## Usage

You will need to convert the downloaded VCF file to a flat text file by
running:

	run_convert.sh

Then you will want to add/change any entries in listBlock.txt, listSilent.txt.
I provided a sample for you to follow.


## Operation

Run the below command to run callBlock.py from the command line, which will place it
in the background:

	start_callerid.sh

Or you can run it from cron at boot time by adding the below entry into your
crontab. See crontab.txt.

	@reboot /home/YOUR-PATH/callerID/start_callerid.sh > /tmp/callerid.log 2>&1

