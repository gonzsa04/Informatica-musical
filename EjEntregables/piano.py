# ejercicio entregable: delay

import numpy as np # arrays
import pyaudio, kbhit
from scipy.io import wavfile # para manejo de wavs
import time

CHUNK = 1024 # tamanio del buffer
char = ' '
frec = 1.0
elapsedTime = 0.2
previousTime = 0.0
canPress = True
frequencies = [523.251,554.365,587.33,622.254,659.255,698.456,739.989,783.991,830.609,880,932.328,987.767]

def speedx(sound_array, factor):
    """ Multiplica la 'velocidad' de la muestra por un factor """
    indices = np.round( np.arange(0, len(sound_array), factor) )
    indices = indices[indices < len(sound_array)].astype(int)
    return sound_array[ indices.astype(int) ]

def keyboard_Proc(keychar, block, numBlock, kb):
    """procesa las teclas del teclado que son parte del piano y devuelve el blocke correspondiente"""
    global char
    global frec
    global previousTime
    global canPress

    char = keychar

    if time.time() - previousTime > elapsedTime:
        canPress = True
        previousTime = time.time()

    #quinta octava de 523 a 987, qwe... para las teclas blancas y 123... para las negras
    if char == 'q':
        frec = CHUNK/ frequencies[0]
    elif char == '2':
        frec = CHUNK/ frequencies[1]
    elif char == 'w':
        frec = CHUNK/ frequencies[2]
    elif char == '3':
        frec = CHUNK/ frequencies[3]
    elif char == 'e':
        frec = CHUNK/ frequencies[4]
    elif char == 'r':
        frec = CHUNK/ frequencies[5]
    elif char == '5':
        frec = CHUNK/ frequencies[6]
    elif char == 't':
        frec = CHUNK/ frequencies[7]
    elif char == '6':
        frec = CHUNK/ frequencies[8]
    elif char == 'y':
        frec = CHUNK/ frequencies[9]
    elif char == '7':
        frec = CHUNK/ frequencies[10]
    elif char == 'u':
        frec = CHUNK/ frequencies[11]

    #sexta octava de 1046 a 1975, zxc... para las teclas blancas y asd... para las negras
    elif char == 'z':
        frec = CHUNK/ frequencies[0] / 2.0
    elif char == 's':
        frec = CHUNK/ frequencies[1] / 2.0
    elif char == 'x':
        frec = CHUNK/ frequencies[2] / 2.0
    elif char == 'd':
        frec = CHUNK/ frequencies[3] / 2.0
    elif char == 'c':
        frec = CHUNK/ frequencies[4] / 2.0
    elif char == 'v':
        frec = CHUNK/ frequencies[5] / 2.0
    elif char == 'g':
        frec = CHUNK/ frequencies[6] / 2.0
    elif char == 'b':
        frec = CHUNK/ frequencies[7] / 2.0
    elif char == 'h':
        frec = CHUNK/ frequencies[8] / 2.0
    elif char == 'n':
        frec = CHUNK/ frequencies[9] / 2.0
    elif char == 'j':
        frec = CHUNK/ frequencies[10] / 2.0
    elif char == 'm':
        frec = CHUNK/ frequencies[11] / 2.0

    else: 
        numBlock = 1000000

    block = speedx(block, frec)

    numBlock+=1
    return numBlock, block

def main():
    srate, data = wavfile.read('piano.wav')

    global SRATE
    global canPress
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
    bloque = np.arange(CHUNK,dtype=data.dtype)
    numBloque = data.shape[0]
    kb = kbhit.KBHit()
    c= ' '

    while True:
        # nuevo bloque
        bloque = data[ numBloque*CHUNK : numBloque*CHUNK+CHUNK ]
        # pasamos al stream haciendo conversion de tipo

        if kb.kbhit() & canPress:
            c = kb.getch()
            canPress = False
            numBloque = 0
            
        numBloque, block = keyboard_Proc(c, bloque, numBloque, kb)

        stream.write(block.astype((data.dtype)).tobytes())

        numBloque += 1

    kb.set_normal_term()
    stream.stop_stream()
    stream.close()
    p.terminate()

main()