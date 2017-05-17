"""Centre Channel Extraction based on http://www.virtualdub.org/blog/pivot/entry.php?id=102. Work on this was started to
try and extract speech from song. However, there was no time to get new results based on it before presentation, thus
for now it's a prototype, with hard slicing, no windowing and several indexing bugs It can only work for particular mixing situations."""

import numpy as np
import numpy.fft as fft
from scipy.interpolate import interp1d
from scipy.io import wavfile
import sys
import os
import time

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

def center_extract_section(data, stride = 4096):
    """Extract centre channel. Returns a floating point array between -1 and +1. Stereo audio only."""
    fdata = fft.rfft(data, n=stride, axis=0)

    L = fdata[:,0]
    R = fdata[:,1]

    C = L + R
    alpha = np.roots([np.dot(C,C), -np.dot(C, L+R), np.dot(L,R)])[0]
    C1 = alpha*C
    c = fft.irfft(C1)
    c = c / np.max(np.abs(c))
    return c

def center_extract(data, stride = 4096):
    """Algorithm from https://en.wikipedia.org/wiki/Overlap%E2%80%93add_method. Returns array of double.
    
    There are numpy optimizatons that can be made for this.
    """
    dlen = data.shape[0]
    i = 0
    il = 0
    nextdot = 0
    n_strides = dlen // stride + bool(dlen % stride)
    out = np.empty((n_strides * stride), dtype=np.double)
    print ("in center_extract")
    while i < dlen:
        if i >= nextdot:
            print(".", end="")
            nextdot += dlen // 200
        il = min(i + stride, dlen)
        io = i + stride
        out[i:io] = center_extract_section(data[i:il], stride)
        i += stride
    return out[:il]  # Truncate result back to original length.

if __name__ == "__main__":
    
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Run IBM Watson speech detection on input sound file\n"
              "\tUsage: python ibm.py <infile> [<outfile>]\n"
              "\t<infile> - Input sound file. Accepts some different formats, depending on ffmpeg install.\n"
              "\t<outfile> - Optional. When specified, stores results in this file. Defaults to 'splitext(<infile>)-voice.wav'.")
        sys.exit(0)

    SRC_FILE = sys.argv[1]

    if len(sys.argv) == 3:
        OUT_FILE = sys.argv[2]
    else:
        OUT_FILE = os.path.splitext(SRC_FILE)[0] + "-voice.wav"

    print("Processing {} -> {}".format(SRC_FILE, OUT_FILE))
    s_time = time.time()
    rate, data = wavfile.read(SRC_FILE)

    c = center_extract(data)
    c = arctan_compressor(c, 2)
    c_16 = (c*32767).astype(np.int16)

    wavfile.write(OUT_FILE, rate, c_16[:,None])
    print("Processed {} in {} s.".format(SRC_FILE, time.time()-s_time))

