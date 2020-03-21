# ejercicio entregable: sampler

import numpy as np # arrays
import pyaudio, kbhit
from scipy.io import wavfile # para manejo de wavs

CHUNK = 1024 # tamanio del buffer

# diccionario de notas con clave = nombre de la nota, valor: distancia en semitonos a DO
notes = {'DO':0, 'DO#':1, 'RE':2, 'RE#':3, 'MI':4, 'FA':5, 'FA#':6, 'SOL':7, 'SOL#':8, 'LA':9, 'LA#':10, 'SI':11, 'DO\'':12}
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
    playPhase = 0     # 0 parado, 1 reproduciendo, -1 parando

    def __init__(self, sample, interval, note):
        self.defaultSample = sample
        self.interval = interval
        self.note = note
        self.frec = SRATE

    """establece la nota que se quiere hacer sonar, modificando el sample original a partir de su nota de referencia"""
    def setNote(self, note):
        semitoneDist = note - self.note           # distancia en semitonos de la nota requerida a la de referencia
        self.frec = SRATE * pow(R, semitoneDist)  # en funcion de esa distancia y con la frecuencia de referncia, se halla la nueva frecuencia

        self.sample = self.__modFrec(self.defaultSample, self.frec/SRATE)    # tomando como referencia el sample original, 
        self.loopInterval = self.sample[self.interval[0]:self.interval[1]] # se modifica para adaptarse a la nueva frecuencia

    """modifica la frecuencia de block, multiplicando la original por un factor"""
    def __modFrec(self, block, factor):
        indices = np.round( np.arange(0, len(block), factor) )
        indices = indices[indices < len(block)].astype(int)
        return block[ indices.astype(int) ]

    """establece todos los parametros de la clase a sus valores por defecto"""
    def __resetParams(self):
        self.ini = 0
        self.fin = 0
        self.loops = 0
        self.attackPhase = True
        self.endPhase = False
        self.sample = np.array([])
        self.loopInterval = np.array([])
    
    """va avanzando el chunk (ventana [ini, fin]) hasta hasta que llega al sustain"""
    def __attack(self):
        self.ini = self.fin
        self.fin = self.fin + CHUNK

        if self.ini > interval[0]:
            self.ini = interval[0]
        if self.fin > interval[0]:
            self.fin = interval[0]

        if self.ini == self.fin:  # ha alcanzado el sustain
            self.attackPhase = False
    
    """va avanzando el chunk (ventana [ini, fin]), haciendo un loop en la zona de sustain"""
    def __loop(self):
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
            self.loopInterval = np.flip(self.loopInterval)

        self.loops += 1

    """va avanzando el chunk (ventana [ini, fin]) hasta la zona de sustain (ataque de la nota). Una vez alli,
    se queda haciendo loop en la zona de sustain"""
    def noteOn(self):
        if self.playPhase == 1:
            if self.attackPhase:
                self.__attack()
                bloque = self.sample[self.ini : self.fin]  # escribimos en el stream el chunk correspondiente
            
            if not self.attackPhase:
                self.__loop()
                bloque = self.loopInterval[self.ini : self.fin]  # escribimos en el stream el chunk correspondiente
            
            stream.write(bloque.astype((self.sample.dtype)).tobytes())

    """va avanzando el chunk (ventana [ini, fin]) hasta el final de la nota"""
    def noteOff(self):
        if self.playPhase == -1:
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
                self.__resetParams()
                self.playPhase = 0    # playPhase = parado
            else:                     # no se ha llegado al final de la nota -> sigue reproduciendo
                bloque = self.sample[self.ini : self.fin]
                stream.write(bloque.astype((self.sample.dtype)).tobytes())
                self.playPhase = -1   # playPhase = parando

    """gestiona el input de usuario. Cada tecla pulsada hara sonar el sampler con una nota, que se
    mantendra hasta que la tecla vuelva a ser pulsada de nuevo"""
    def handleInput(self, c):
        if c == 'z':
            if self.playPhase == 0:
                self.playPhase = 1
                sampler.setNote(notes['DO'])
            elif self.playPhase == 1:
                self.playPhase = -1
        elif c == 's':
            if self.playPhase == 0:
                self.playPhase = 1
                sampler.setNote(notes['DO#'])
            elif self.playPhase == 1:
                self.playPhase = -1
        elif c == 'x':
            if self.playPhase == 0:
                self.playPhase = 1
                sampler.setNote(notes['RE'])
            elif self.playPhase == 1:
                self.playPhase = -1
        elif c == 'd':
            if self.playPhase == 0:
                self.playPhase = 1
                sampler.setNote(notes['RE#'])
            elif self.playPhase == 1:
                self.playPhase = -1
        elif c == 'c':
            if self.playPhase == 0:
                self.playPhase = 1
                sampler.setNote(notes['MI'])
            elif self.playPhase == 1:
                self.playPhase = -1
        elif c == 'v':
            if self.playPhase == 0:
                self.playPhase = 1
                sampler.setNote(notes['FA'])
            elif self.playPhase == 1:
                self.playPhase = -1
        elif c == 'g':
            if self.playPhase == 0:
                self.playPhase = 1
                sampler.setNote(notes['FA#'])
            elif self.playPhase == 1:
                self.playPhase = -1
        elif c == 'b':
            if self.playPhase == 0:
                self.playPhase = 1
                sampler.setNote(notes['SOL'])
            elif self.playPhase == 1:
                self.playPhase = -1
        elif c == 'h':
            if self.playPhase == 0:
                self.playPhase = 1
                sampler.setNote(notes['SOL#'])
            elif self.playPhase == 1:
                self.playPhase = -1
        elif c == 'n':
            if self.playPhase == 0:
                self.playPhase = 1
                sampler.setNote(notes['LA'])
            elif self.playPhase == 1:
                self.playPhase = -1
        elif c == 'j':
            if self.playPhase == 0:
                self.playPhase = 1
                sampler.setNote(notes['LA#'])
            elif self.playPhase == 1:
                self.playPhase = -1
        elif c == 'm':
            if self.playPhase == 0:
                self.playPhase = 1
                sampler.setNote(notes['SI'])
            elif self.playPhase == 1:
                self.playPhase = -1
        elif c == ',':
            if self.playPhase == 0:
                self.playPhase = 1
                sampler.setNote(notes['DO\''])
            elif self.playPhase == 1:
                self.playPhase = -1

#-----------------------------------MAIN-------------------------------------------

SRATE, data = wavfile.read('DOpiano.wav')

# miramos formato de samples
if data.dtype.name == 'int16': fmt = 2
elif data.dtype.name == 'int32': fmt = 4
elif data.dtype.name == 'float32': fmt = 4
elif data.dtype.name == 'uint8': fmt = 1
else: raise Exception('Not supported')

p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(fmt), channels=len(data.shape), 
rate=SRATE, frames_per_buffer=CHUNK, output=True)

interval = np.array([20000, 40000])               # intervalo del sustain
sampler = Sampler(data, interval, notes['DO'])    # nota de referencia del sample (sin modificar, se identifica como esa nota)

kb = kbhit.KBHit()
c= ' '

while c != 'q':
    if kb.kbhit():
        c = kb.getch()
        sampler.handleInput(c)
    
    sampler.noteOn()
    sampler.noteOff()

kb.set_normal_term()
stream.stop_stream()
stream.close()
p.terminate()