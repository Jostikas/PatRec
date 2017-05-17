"""Centre Channel Extraction based on http://www.virtualdub.org/blog/pivot/entry.php?id=102. Work on this was started to
try and extract speech from song. However, there was no time to get new results based on it before presentation, thus
for now it's a prototype, with no slicing (has only been tested on short snippets thus far)."""

import numpy as np
import numpy.fft as fft
from scipy.interpolate import interp1d
from scipy.io import wavfile
import sys

# Compressor implementation from http://stackoverflow.com/a/34840218/3745323
def apply_transfer(signal, transfer, interpolation='linear'):
    constant = np.linspace(-1, 1, len(transfer))
    interpolator = interp1d(constant, transfer, interpolation)
    return interpolator(signal)

def arctan_compressor(x, factor=2):
    constant = np.linspace(-1, 1, 1000)
    transfer = np.arctan(factor * constant)
    transfer /= np.abs(transfer).max()
    return apply_transfer(x, transfer)

SRC_FILE = sys.argv[1]

rate, data = wavfile.read(SRC_FILE)

l = data[:,0]
r = data[:,1]

L = fft.rfft(l)
R = fft.rfft(r)

C = L/np.abs(L) + R/np.abs(R)
alpha = np.roots([np.dot(C,C), -np.dot(C, L+R), np.dot(L,R)])[0]
C1 = alpha*C
c = fft.irfft(C1)
c = c / np.max(np.abs(c))
c = arctan_compressor(c, 3)
c_16 = (c*32767).astype(np.int16)

wavfile.write(sys.argv[2], rate, c_16[:,None])

