# 1 numPy/playNumPy.py simple reproductor con arrays de numPy
import numpy as np # arrays
import pyaudio, kbhit
import lab2
from scipy.io import wavfile # para manejo de wavs

def main():
    # abrimos wav y recogemos frecMuestreo y array de datos
    CHUNK = 1024 # tamanio del buffer
    data = lab2.osc(1000, 10)

    # miramos formato de samples
    if data.dtype.name == 'int16': fmt = 2
    elif data.dtype.name == 'int32': fmt = 4
    elif data.dtype.name == 'float32': fmt = 4
    elif data.dtype.name == 'uint8': fmt = 1
    else: raise Exception('Not supported')

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, # formato de los samples
    channels=len(data.shape), # num canales (shape de data)
    rate=lab2.SRATE, # frecuencia de muestreo
    frames_per_buffer=CHUNK, # tamanio buffer
    output=True) # stream de salida

    # En data tenemos el wav completo, ahora procesamos por bloques (chunks)
    numBloque = 0
    kb = kbhit.KBHit()
    c= ' '
    vol = 1.0
    volIncr = 0.05
    frec = 500
    maxfrec = 2000
    frecIncr = 5
    bloque = lab2.generateChunk(frec, CHUNK, 0)
    
    while c!= 'q':
        c = ' '
        # nuevo bloque
        #bloque = data[ numBloque*CHUNK : numBloque*CHUNK+CHUNK ]
        bloque = lab2.generateChunk(frec, CHUNK, bloque[-1])
        # modificación del volumen: multiplicacion de todas las muestras * vol
        bloque = bloque*vol
        #pasamos al stream haciendo conversion de tipo
        stream.write(bloque.astype(np.float32).tobytes())

        if kb.kbhit():
            c = kb.getch()
            if (c=='v'): vol= max(0,vol-volIncr)
            elif (c=='V'): vol= min(1,vol+volIncr)
            elif (c=='f'): frec= max(1/maxfrec,frec-frecIncr)
            elif (c=='F'): frec= min(maxfrec,frec+frecIncr)
            print("Vol: ",vol)
            print("Frec: ",frec)
            
        numBloque += 1

    kb.set_normal_term()
    stream.stop_stream()
    stream.close()
    p.terminate()

main()