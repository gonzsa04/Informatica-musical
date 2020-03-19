# ejercicio entregable: sampler

import numpy as np # arrays
import pyaudio, kbhit
from scipy.io import wavfile # para manejo de wavs

CHUNK = 1024 # tamanio del buffer

notes = {'DO':0, 'DO#':1, 'RE':2, 'RE#':3, 'MI':4, 'FA':6, 'FA#':7, 'SOL':8, 'SOL#':9, 'LA':10, 'LA#':11, 'SI':12}
R = 1.059463 # raiz doceava de 2 (http://elclubdelautodidacta.es/wp/2012/08/calculo-de-la-frecuencia-de-nuestras-notas-musicales/)

class Sampler:
    defaultSample = np.array([])
    sample = np.array([])
    interval = np.zeros([2])
    loopInterval = np.array([])
    note = 0
    frec = 0
    ini = 0
    fin = 0
    loops = 0
    attackPhase = True
    endPhase = False

    def __init__(self, sample, interval, note):
        self.defaultSample = sample
        self.interval = interval
        self.note = note
        self.frec = SRATE

    def setNote(self, note):
        semitoneDist = note - self.note
        self.frec = SRATE * pow(R, semitoneDist)
        self.sample = self.modFrec(self.defaultSample, self.frec/SRATE)
        print(self.frec/SRATE)
        self.loopInterval = self.sample[self.interval[0]:self.interval[1]]

    """ Multiplica la 'velocidad' de la muestra por un factor """
    def modFrec(self, block, factor):
        indices = np.round( np.arange(0, len(block), factor) )
        indices = indices[indices < len(block)].astype(int)
        return block[ indices.astype(int) ]
    
    """va avanzando el chunk (ventana [ini, fin]) hasta hasta que llega al sustain"""
    def attack(self):
        self.ini = self.fin
        self.fin = self.fin + CHUNK

        if self.ini > interval[0]:
            self.ini = interval[0]
        if self.fin > interval[0]:
            self.fin = interval[0]

        if self.ini == self.fin:  # ha alcanzado el sustain
            self.attackPhase = False
    
    """va avanzando el chunk (ventana [ini, fin]), haciendo un loop en la zona de sustain"""
    def loop(self):
        self.ini = self.loops*CHUNK
        self.fin = self.loops*CHUNK+CHUNK

        if self.ini >= self.loopInterval.size:
            self.ini = self.loopInterval.size - 1
        if self.fin >= self.loopInterval.size:
            self.fin = self.loopInterval.size - 1

        if self.ini == self.fin: # reinicio de ventana [ini, fin] (vuelta al principio del sustain -> loop)
            self.loops = 0
            self.ini = self.loops*CHUNK
            self.fin = self.loops*CHUNK+CHUNK
            #self.loopInterval = np.flip(self.loopInterval)

        self.loops += 1

    """va avanzando el chunk (ventana [ini, fin]) hasta la zona de sustain (ataque de la nota). Una vez alli,
    se queda haciendo loop en la zona de sustain"""
    def noteOn(self):
        if self.attackPhase:
            self.attack()
            bloque = self.sample[self.ini : self.fin]  # escribimos en el stream el chunk correspondiente
        
        if not self.attackPhase:
            self.loop()
            bloque = self.loopInterval[self.ini : self.fin]  # escribimos en el stream el chunk correspondiente
        
        stream.write(bloque.astype((self.sample.dtype)).tobytes())

    """va avanzando el chunk (ventana [ini, fin]) hasta el final de la nota"""
    def noteOff(self):
        if not self.endPhase:
            self.ini += self.interval[0]
            self.fin += self.interval[0]
            self.endPhase = True

        self.ini = self.fin
        self.fin = self.fin + CHUNK

        if self.ini > self.sample.size:
            self.ini = self.sample.size
        if self.fin > self.sample.size:
            self.fin = self.sample.size

        if self.ini == self.fin:  # se ha llegado al final de la nota -> se reinicia todo
            self.ini = 0
            self.fin = 0
            self.loops = 0
            self.attackPhase = True
            self.endPhase = False
            self.sample = np.array([])
            self.loopInterval = np.array([])
            return 0   # devuelve 0 cuando ya ha parado la nota
        else:
            bloque = self.sample[self.ini : self.fin]
            stream.write(bloque.astype((self.sample.dtype)).tobytes())
            return -1  # devuelve -1 si aun sigue parando la nota

SRATE, data = wavfile.read('piano.wav')

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

interval = np.array([20000, 40000])
sampler = Sampler(data, interval, notes['DO'])

play = 0 # 0 por defecto, 1 reproduciendo, -1 parando
kb = kbhit.KBHit()
c= ' '

while c != 'q':
    if kb.kbhit():
        c = kb.getch()
        if c == 'z':
            if play == 0:
                play = 1
                sampler.setNote(notes['DO'])
            elif play == 1:
                play = -1
        elif c == 's':
            if play == 0:
                play = 1
                sampler.setNote(notes['DO#'])
            elif play == 1:
                play = -1
        elif c == 'x':
            if play == 0:
                play = 1
                sampler.setNote(notes['RE'])
            elif play == 1:
                play = -1
        elif c == 'd':
            if play == 0:
                play = 1
                sampler.setNote(notes['RE#'])
            elif play == 1:
                play = -1
        elif c == 'c':
            if play == 0:
                play = 1
                sampler.setNote(notes['MI'])
            elif play == 1:
                play = -1
        elif c == 'v':
            if play == 0:
                play = 1
                sampler.setNote(notes['FA'])
            elif play == 1:
                play = -1
        elif c == 'g':
            if play == 0:
                play = 1
                sampler.setNote(notes['FA#'])
            elif play == 1:
                play = -1
        elif c == 'b':
            if play == 0:
                play = 1
                sampler.setNote(notes['SOL'])
            elif play == 1:
                play = -1
        elif c == 'h':
            if play == 0:
                play = 1
                sampler.setNote(notes['SOL#'])
            elif play == 1:
                play = -1
        elif c == 'n':
            if play == 0:
                play = 1
                sampler.setNote(notes['LA'])
            elif play == 1:
                play = -1
        elif c == 'j':
            if play == 0:
                play = 1
                sampler.setNote(notes['LA#'])
            elif play == 1:
                play = -1
        elif c == 'm':
            if play == 0:
                play = 1
                sampler.setNote(notes['SI'])
            elif play == 1:
                play = -1
    
    if play == 1:
        sampler.noteOn()
    elif play == -1:
        play = sampler.noteOff()

kb.set_normal_term()
stream.stop_stream()
stream.close()
p.terminate()