import numpy as np
from matplotlib import pyplot as plt

SRATE = 44100

def drawSignal(signal):
    plt.plot(np.arange(signal.shape[0]), signal)
    plt.show()

def generateChunk(frec, chunkSize, yStart):
    start = np.arcsin(yStart)
    xStart = start*SRATE/(2*np.pi*frec)
    ix = np.arange(xStart, chunkSize+xStart)
    signal = np.sin(ix*2*np.pi*frec/SRATE, dtype = "float32")

    return signal

def osc(frec, dur):
    frec = 1/frec
    samples = SRATE*dur
    ix = np.arange(samples)
    signal = np.sin(2*np.pi*ix*(dur/frec)/samples, dtype = "float32")

    return signal

def saw(frec, dur):
    frec = 1/frec
    samples = SRATE*dur
    ix = np.arange(samples)
    signal = np.sin(2*np.pi*ix*(dur/frec)/samples)

    return signal

def square(frec, dur):
    frec = 1/frec
    samples = SRATE*dur
    ix = np.arange(samples)
    signal = np.sin(2*np.pi*ix*(dur/frec)/samples)

    return signal

def triangle(frec, dur):
    frec = 1/frec
    samples = SRATE*dur
    ix = np.arange(samples)
    signal = np.sin(2*np.pi*ix*(dur/frec)/samples)

    return signal

def vol(factor, sample):
    return sample * factor

def fadeOut(sample, t):
    interval = sample.shape[0] - t

    step = 1.0 / interval
    percentage = 1.0

    for i in range(t, sample.shape[0]):
        sample[i] *= percentage
        percentage -= step


    return sample

def fadeIn(sample, t):
    step = 1.0 / t
    percentage = 0.0

    for i in range(0, t):
        sample[i] *= percentage
        percentage += step


    return sample

# def main():   
#     signal = osc(35, 2)
#     signal = fadeIn(signal, 44100)
#     drawSignal(signal)

# main()