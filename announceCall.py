import sys, os, time
#import pyttsx3
import wave
#import pyaudio



#def announceCallerPYTTS(number, name):
    #engine = pyttsx3.init();

    #rate = engine.getProperty('rate')
    #engine.setProperty('rate', rate+50)

    #engine.setProperty('volume', 1.0)

    #voices = engine.getProperty('voices')

    #engine.setProperty('voice', 'english-us')

    #engine.say('Call From')
    #engine.say(name)
    #for n in number:
    #    engine.say(n)
    #print('pyaudio announced: ', number, name)
    #engine.runAndWait() ;
    #return(True)



def announceCallerFestival(number, name):
    text = 'Call From ' + name + ' ' + number
    #os.system(r'echo "(SayText \"' + text + r'\")" | festival')
    os.system(r'echo "' + text + r'" | festival --tts --language english')
    print('festival announced: ', number, name)
    return(True)



def ringBell(inList):
    print('ringing bell: in phone book: ', inList)
    
    if inList == True:
        #os.system(r'aplay --device=default data/vintage2a.wav')
        print('phone book bell')
        #os.system(r'aplay -q data/vintage2a.wav')
        os.system(r'aucat -i data/vintage2a.wav')
    else:
        print('unknown call bell')
        #os.system(r'aplay -q data/euro_ring.wav')
        os.system(r'aucat -i data/euro_ring.wav')
    return()

    

def announceCallerESpeak(number, name):
    # need to figure out how to announce string of numbers
    #text = 'Call From ' + name + ' ' + number
    text = name
    os.system(r'echo "' + text + r'" | espeak')
    print('espeak announced: ', number, name)
    return(True)



def ringBell_py():
    CHUNK = 1024

    limit = 75
    wf = wave.open('data/vintage2a.wav', 'rb')
    p = pyaudio.PyAudio()

    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        print((i, dev['name'], dev['maxInputChannels']))
    
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    output_device_index=0)

    print('ringing bell')
    count = 0
    data = wf.readframes(CHUNK)
    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)
        count += 1
        if count > limit:
            break

    stream.stop_stream()
    stream.close()
    p.terminate()
    return()

    

def main(argv):
    fd = open('data_test/announceInputTest.txt', 'r')
    phList = fd.readlines()
    fd.close()

    for entry in phList:
        entry = entry.strip()
        if entry == '' or '#' in entry:
            continue
    
        line = entry.split(':')
        number = line[0]
        name   = line[1]
        #print('calling announceCallerPYTTS')
        #ret = announceCallerPYTTS(number, name)
        #time.sleep(1)
        
        #print('calling announceCallerFestival')
        #ret = announceCallerFestival(number, name)
        #time.sleep(1)
        
        print('calling announceCallerESpeak')
        ret = announceCallerESpeak(number, name)
        time.sleep(1)
        break

    #print('calling bell true')
    #ringBell(True)
    #time.sleep(1)
    #print('calling bell false')
    #ringBell(False)
    
    #time.sleep(1)
    #print('calling bell_py')
    #ringBell_py()
    
if __name__ == "__main__":
    main(sys.argv)
    
    
