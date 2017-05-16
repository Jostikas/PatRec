import numpy as np
import numpy.fft as fft
from scipy.interpolate import interp1d
from scipy.io import wavfile

def apply_transfer(signal, transfer, interpolation='linear'):
    constant = np.linspace(-1, 1, len(transfer))
    interpolator = interp1d(constant, transfer, interpolation)
    return interpolator(signal)


def arctan_compressor(x, factor=2):
    constant = np.linspace(-1, 1, 1000)
    transfer = np.arctan(factor * constant)
    transfer /= np.abs(transfer).max()
    return apply_transfer(x, transfer)


SRC_FILE = "C:/YT/W.wav"

rate, data = wavfile.read(SRC_FILE)

l = data[rate*6:rate*15, 0]
r = data[rate*6:rate*15, 1]

L = fft.rfft(l)
R = fft.rfft(r)

C = L/np.abs(L) + R/np.abs(R)
alpha = np.roots([np.dot(C,C), -np.dot(C, L+R), np.dot(L,R)])[0]
C1 = alpha*C
c = fft.irfft(C1)
c = c / np.max(np.abs(c))
c = arctan_compressor(c, 3)
c_16 = (c*32767).astype(np.int16)

wavfile.write("C:/YT/W1.wav", rate, c_16[:,None])

