#!/usr/bin/env python3

import speech_recognition as sr
from time import time
import sys
import os

# For monkey-patching
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import json
import base64

URL = "https://stream-fra.watsonplatform.net/speech-to-text/api"
USERNAME = "f0bea13c-1581-450e-b019-4deee5b86e58"
PASSWORD = "Sy2A22q6vOHT"

"""Monkey-patch the Recognizer class, as it's recognize_ibm method doesn't support api url input (has a hardcoded url that
is wrong/only for some countries.
"""
def recognize_ibm(self, audio_data, username, password, language="en-US", show_all=False,
                  url="https://stream.watsonplatform.net/speech-to-text/api"):
    """
    Performs speech recognition on ``audio_data`` (an ``AudioData`` instance), using the IBM Speech to Text API.

    The IBM Speech to Text username and password are specified by ``username`` and ``password``, respectively. Unfortunately, these are not available without `signing up for an account <https://console.ng.bluemix.net/registration/>`__. Once logged into the Bluemix console, follow the instructions for `creating an IBM Watson service instance <https://www.ibm.com/watson/developercloud/doc/getting_started/gs-credentials.shtml>`__, where the Watson service is "Speech To Text". IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX, while passwords are mixed-case alphanumeric strings.

    The recognition language is determined by ``language``, an RFC5646 language tag with a dialect like ``"en-US"`` (US English) or ``"zh-CN"`` (Mandarin Chinese), defaulting to US English. The supported language values are listed under the ``model`` parameter of the `audio recognition API documentation <https://www.ibm.com/watson/developercloud/speech-to-text/api/v1/#sessionless_methods>`__, in the form ``LANGUAGE_BroadbandModel``, where ``LANGUAGE`` is the language value.

    Returns the most likely transcription if ``show_all`` is false (the default). Otherwise, returns the `raw API response <https://www.ibm.com/watson/developercloud/speech-to-text/api/v1/#sessionless_methods>`__ as a JSON dictionary.

    Raises a ``speech_recognition.UnknownValueError`` exception if the speech is unintelligible. Raises a ``speech_recognition.RequestError`` exception if the speech recognition operation failed, if the key isn't valid, or if there is no internet connection.
    """
    assert isinstance(audio_data, sr.AudioData), "Data must be audio data"
    assert isinstance(username, str), "``username`` must be a string"
    assert isinstance(password, str), "``password`` must be a string"

    flac_data = audio_data.get_flac_data(
        convert_rate=None if audio_data.sample_rate >= 16000 else 16000,  # audio samples should be at least 16 kHz
        convert_width=None if audio_data.sample_width >= 2 else 2  # audio samples should be at least 16-bit
    )
    url = "{}/v1/recognize?{}".format(url, urlencode({
        "profanity_filter": "false",
        "continuous": "true",
        "model": "{}_BroadbandModel".format(language),
    }))
    request = Request(url, data=flac_data, headers={
        "Content-Type": "audio/x-flac",
        "X-Watson-Learning-Opt-Out": "true",  # prevent requests from being logged, for improved privacy
    })
    authorization_value = base64.standard_b64encode("{}:{}".format(username, password).encode("utf-8")).decode(
        "utf-8")
    request.add_header("Authorization", "Basic {}".format(authorization_value))
    try:
        response = urlopen(request, timeout=self.operation_timeout)
    except HTTPError as e:
        raise sr.RequestError("recognition request failed: {}".format(e.reason))
    except URLError as e:
        raise sr.RequestError("recognition connection failed: {}".format(e.reason))
    response_text = response.read().decode("utf-8")
    result = json.loads(response_text)

    # return results
    if show_all: return result
    if "results" not in result or len(result["results"]) < 1 or "alternatives" not in result["results"][0]:
        raise sr.UnknownValueError()

    transcription = []
    for utterance in result["results"]:
        if "alternatives" not in utterance: raise sr.UnknownValueError()
        for hypothesis in utterance["alternatives"]:
            if "transcript" in hypothesis:
                transcription.append(hypothesis["transcript"])
    return "\n".join(transcription)

sr.Recognizer.recognize_ibm = recognize_ibm

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Run IBM Watson speech detection on input sound file\n"
              "\tUsage: python ibm.py <infile> [<outfile>]\n"
              "\t<infile> - Input sound file. Accepts some different formats, depending on ffmpeg install.\n"
              "\t<outfile> - Optional. When specified, stores results in this file. Defaults to 'basename(<infile>)-ibm.txt'.")
        sys.exit(0)

    # obtain path to "english.wav" in the same folder as this script
    AUDIO_FILE = sys.argv[1]
    if len(sys.argv) == 3:
        OUT_FILE = sys.argv[2]
    else:
        OUT_FILE = os.path.splitext(AUDIO_FILE)[0] + "-ibm.txt"

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file

    try:
        s_time = time()
        print("Processing {} -> {}".format(AUDIO_FILE, OUT_FILE))
        with open(OUT_FILE, 'w') as outfile:
            outfile.write(r.recognize_ibm(audio,
                                          username=USERNAME,
                                          password=PASSWORD,
                                          language="en-US",
                                          url=URL))
        print("{} processed in {}s".format(AUDIO_FILE, time()-s_time))
        sys.exit(0)
    except sr.UnknownValueError:
        print("Watson could not understand audio")
    except sr.RequestError as e:
        print("Request error; {0}".format(e))

