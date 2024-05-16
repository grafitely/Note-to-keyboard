#import modules
import pyaudio
import numpy as np
import pydirectinput
import time
import threading

#define the pyaudio config
Rate = 48000
Chunk = 2048
Inputformat = pyaudio.paInt16

#initialise pyaudio and open audio stream
p = pyaudio.PyAudio()
stream = p.open(format=Inputformat, rate=Rate, channels=1, input=True, frames_per_buffer=Chunk)


#presses a key with pyautogui
def pressKey(key):
    pydirectinput.keyDown(key)
    time.sleep(0.6)
    pydirectinput.keyUp(key)

#main function
def audio():
    while stream.is_active:
        #grabs data from active audio stream and runs it through a fourier transform
        data = np.frombuffer(stream.read(Chunk), dtype=np.int16)
        fftData=abs(np.fft.rfft(data))**2
        which = fftData[1:].argmax() + 1
        # use quadratic interpolation around the max
        if which != len(fftData)-1:
            y0,y1,y2 = np.log(fftData[which-1:which+2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
            # find the frequency and output it
            thefreq = (which+x1)*Rate/Chunk
            print("The freq is " + str(round(thefreq)) + " Hz.")
        else:
            thefreq = which*Rate/Chunk
            print("The freq is " + str(round(thefreq)) + " Hz.")
        
        #rounds the frequency for use in keyboard output
        roundedfreq = round(thefreq) 

        match roundedfreq:
            case roundedfreq if roundedfreq < 530 and roundedfreq > 490:
                #starts thread to send keyboard output with
                thread_two = threading.Thread(target=pressKey, args="d")
                thread_two.start()
            case roundedfreq if roundedfreq < 560 and roundedfreq > 530:
                thread_two = threading.Thread(target=pressKey, args="s")
                thread_two.start()
            case roundedfreq if roundedfreq < 620 and roundedfreq > 600:
                thread_two = threading.Thread(target=pressKey, args="w")
                thread_two.start()
            case roundedfreq if roundedfreq < 660 and roundedfreq > 630:
                thread_two = threading.Thread(target=pressKey, args="a")
                thread_two.start()
            case roundedfreq if roundedfreq < 740 and roundedfreq > 710:
                thread_two = threading.Thread(target=pressKey, args="v")
                thread_two.start()

#initialise thread for the frequency grabbing
thread_one = threading.Thread(target=audio)
thread_one.start()