import cv2
import pyaudio
import numpy as np
import matplotlib.pyplot as plt

RATE=48000
RECORD_SECONDS = 2.5
CHUNKSIZE = 2048

cv2.namedWindow("spect",0)
image_spect = np.zeros((400,CHUNKSIZE//2)).astype("uint8")
try:
    # initialize portaudio
    p = pyaudio.PyAudio()
    n = p.get_device_count()
    for i in range(n):
        d = p.get_device_info_by_index(i)
        print(d["index"],d["name"],d["maxInputChannels"],d["defaultSampleRate"])

    stream = p.open(input_device_index=3,format=pyaudio.paFloat32, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNKSIZE)

    frames = [] # A python-list of chunks(numpy.ndarray)
    while True:
        try:
            data = stream.read(CHUNKSIZE)
        except OSError as e:
            print(e)

        

        sample = np.frombuffer(data, dtype=np.float32)

        sample = sample/sample.max()

        fft = np.abs(np.fft.fft(sample))


        print(fft.max())
        #roll image
        image_spect[:-1,:] = image_spect[1:,:]

        
        #add fft
        image_spect[-1,:] = (fft[:CHUNKSIZE//2]/CHUNKSIZE*4*255).astype("uint8")

        cv2.imshow("spect",image_spect)
        cv2.waitKey(1)

except Exception as e:
    print(e)

finally:
    # close stream
    stream.stop_stream()
    stream.close()
    p.terminate()

