# ejercicio entregable: delay

import numpy as np # arrays
import pyaudio, kbhit
from scipy.io import wavfile # para manejo de wavs

CHUNK = 1024 # tamanio del buffer
SRATE = 44100

def osc(frec, dur):
    frec = 1/frec
    samples = SRATE*dur
    ix = np.arange(samples)
    signal = np.sin(2*np.pi*ix*(dur/frec)/samples, dtype = "float32")

    return signal

def main():
    srate, data = wavfile.read('tormenta.wav')
    global SRATE
    SRATE = srate

    # miramos formato de samples
    if data.dtype.name == 'int16': fmt = 2
    elif data.dtype.name == 'int32': fmt = 4
    elif data.dtype.name == 'float32': fmt = 4
    elif data.dtype.name == 'uint8': fmt = 1
    else: raise Exception('Not supported')

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(fmt), # formato de los samples
    channels=len(data.shape), # num canales (shape de data)
    rate=SRATE, # frecuencia de muestreo
    frames_per_buffer=CHUNK, # tamanio buffer
    output=True)

    # En data tenemos el wav completo, ahora procesamos por bloques (chunks)
    numBloque = 0
    kb = kbhit.KBHit()
    c= ' '
    alphaLP = 0.0
    alphaHP = 0.0
    freqLP = 1.0
    freqHP = 1.0
    euler = 2.71828
    prev = 0

    while c!= 'q':

        if kb.kbhit():
            c = kb.getch()
            if (c=='d'): freqLP+=500.0
            elif (c=='a'): freqLP-=500.0
            elif (c=='w'): freqHP+=500.0
            elif (c=='s'): freqHP-=500.0

            exp = (-2*np.pi*freqLP)/SRATE
            alphaLP = np.power(euler, exp)
            
            exp = (-2*np.pi*freqHP)/SRATE
            alphaHP = np.power(euler, exp)

            print(alphaLP)

        x = np.array(data[numBloque*CHUNK:(numBloque+1)*CHUNK])
        y1 = np.copy(x)

        y1[0] = prev + alphaLP * (y1[0]-prev)

        #filtro LP
        for i in range(1,CHUNK):
            y1[i] = y1[i-1] + alphaLP * (y1[i]-y1[i-1])

        prev = y1[CHUNK-1]

        y2 = np.copy(y1)

        #filtro HP
        y2[0] = prev + alphaHP * (y2[0]-prev)

        for i in range(1,CHUNK):
            y2[i] = y2[i-1] + alphaHP * (y2[i]-y2[i-1])

        z = y1 - y2

        stream.write(z.astype((data.dtype)).tobytes())

        numBloque+=1

    kb.set_normal_term()
    stream.stop_stream()
    stream.close()
    p.terminate()

main()