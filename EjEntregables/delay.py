# ejercicio entregable: delay

import numpy as np # arrays
import pyaudio, kbhit

CHUNK = 1024 # tamanio del buffer
SRATE = 44100

""" funcion que devuelve un chunk a una frecuencia, dado un tamaño y donde tiene que empezar """
def generateChunk(frec, chunkSize, xStart):
    ix = np.arange(xStart, chunkSize+xStart)
    signal = np.sin(ix*2*np.pi*frec/SRATE, dtype = "float32")

    return signal

""" clase que añade un delay a una señal dada, llevando un buffer interno y procesando por chuncks """
class Delay:
    buffer = np.array([])

    def __init__(self, time):
        self.buffer = np.zeros(int(SRATE*time))
        
    def getNextChunk(self, signal):
        self.buffer = np.append(self.buffer, signal)
        chunk = self.buffer[:CHUNK]
        self.buffer = np.delete(self.buffer, np.s_[:CHUNK])
        return chunk

def main():
    
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=SRATE, frames_per_buffer=CHUNK, output=True)

    delay = Delay(3.0)
    kb = kbhit.KBHit()
    c= ' '
    numBloque = 0
    
    while c!= 'q':
        c = ' '
        bloque = delay.getNextChunk(generateChunk(500.0, CHUNK, numBloque*CHUNK))
        print(bloque)

        stream.write(bloque.astype(np.float32).tobytes())

        if kb.kbhit():
            c = kb.getch()
            
        numBloque += 1

    kb.set_normal_term()
    stream.stop_stream()
    stream.close()
    p.terminate()

main()