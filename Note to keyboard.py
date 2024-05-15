import pyaudio
import numpy as np
import pyautogui
import time
import threading

Rate = 48000
Chunk = 2048
Inputformat = pyaudio.paInt16

p = pyaudio.PyAudio()
space = "space"

stream = p.open(format=Inputformat, rate=Rate, channels=1, input=True, frames_per_buffer=Chunk)

def pressKey(key):
    pyautogui.keyDown(key)
    time.sleep(0.6)
    pyautogui.keyUp(key)

def audio():
    while stream.is_active:
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
        roundedfreq = round(thefreq) 

        match roundedfreq:
            case roundedfreq if roundedfreq < 530 and roundedfreq > 490:
                thread_two = threading.Thread(target=pressKey, args="d")
                thread_two.start()
            case roundedfreq if roundedfreq < 560 and roundedfreq > 530:
                thread_two = threading.Thread(target=pressKey, args="s")
                thread_two.start()
            case roundedfreq if roundedfreq < 620 and roundedfreq > 600:
                thread_two = threading.Thread(target=pressKey, args=" ")
                thread_two.start()
            case roundedfreq if roundedfreq < 660 and roundedfreq > 630:
                thread_two = threading.Thread(target=pressKey, args="a")
                thread_two.start()
            case roundedfreq if roundedfreq < 740 and roundedfreq > 710:
                pyautogui.leftClick()

thread_one = threading.Thread(target=audio)

thread_one.start()

audio()