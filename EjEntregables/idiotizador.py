# Ejercicio entregable: idiotizador

import numpy as np
import pyaudio, kbhit, time

# variables globales
CHUNK = 1024
CHANNELS = 1
RATE = 44100
lastTime = time.time()
currentTime = time.time()
delay = 1.0
bloque = np.zeros([CHUNK])
frames = np.array([]).astype(np.float32)

# se mira formato de samples
if frames.dtype.name == 'int16': fmt = 2
elif frames.dtype.name == 'int32': fmt = 4
elif frames.dtype.name == 'float32': fmt = 4
elif frames.dtype.name == 'uint8': fmt = 1
else: raise Exception('Not supported')

# inicializacion de pyaudio
p = pyaudio.PyAudio()

""" funcion que sera llamada por el callback del stream de entreda (grabador) 
    guarda en frames el siguiente CHUNK grabado"""
def inputCallback(in_data, frame_count, time_info, status):
    global frames
    frames = np.append(frames, np.frombuffer(in_data))
    print(frames.shape)
    
    return (in_data, pyaudio.paContinue)

""" funcion que sera llamada por el callback del stream de salida (reproductor) 
    lee de frames el siguiente CHUNK grabado, una vez transcurrido el tiempo delay"""
def outputCallback(in_data, frame_count, time_info, status):
    currentTime = time.time()

    if lastTime + delay < currentTime:
        global frames
        global bloque
        bloque = frames[512 : 512 + 512]
        frames = np.delete(frames, np.s_[512 : 512 + 512])

    return (bloque.astype(frames.dtype).tobytes(), pyaudio.paContinue)

# apertura del stream de entrada (grabador) en modo callback (no bloqueante)
inputStream = p.open(format=p.get_format_from_width(fmt), channels=CHANNELS,
rate=RATE, input=True, frames_per_buffer=CHUNK, stream_callback = inputCallback)

# apertura del stream de salida (reproductor) en modo callback (no bloqueante)
outputStream = p.open(format=p.get_format_from_width(fmt), channels=CHANNELS,
rate=RATE, frames_per_buffer=CHUNK, output=True, stream_callback = outputCallback)

# se empiezan a ejecutar ambas hebras (entrada y salida)
inputStream.start_stream()
outputStream.start_stream()

# bucle principal, mientras no se pulse q
kb = kbhit.KBHit()
c = ' '
while c != 'q': 
    if kb.kbhit(): c = kb.getch()
    time.sleep(0.1)

# se paran hebras y se cierran ambos streams y pyaudio
inputStream.stop_stream()
inputStream.close()
outputStream.stop_stream()
outputStream.close()
p.terminate()