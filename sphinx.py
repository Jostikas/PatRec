#!/usr/bin/env python3

import speech_recognition as sr
from time import time
import sys
import os

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Run PocketSphinx speech detection on input sound file\n"
          "\tUsage: python sphinx.py <infile> [<outfile>]\n"
          "\t<infile> - Input sound file. Accepts some different formats, depending on ffmpeg install.\n"
          "\t<outfile> - Optional. When specified, stores results in this file. Defaults to 'basename(<infile>)-sphinx.txt'.")
    sys.exit(0)

# obtain path to "english.wav" in the same folder as this script
AUDIO_FILE = sys.argv[1]
if len(sys.argv) == 3:
    OUT_FILE = sys.argv[2]
else:
    OUT_FILE = os.path.splitext(AUDIO_FILE)[0] + "-sphinx.txt"

# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file

# recognize speech using Sphinx
try:
    s_time = time()
    print("Processing {} -> {}".format(AUDIO_FILE, OUT_FILE))
    with open(OUT_FILE, 'w') as outfile:
        outfile.write(r.recognize_sphinx(audio, language="en-US"))
    print("{} processed in {}s".format(AUDIO_FILE, time()-s_time))
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))
