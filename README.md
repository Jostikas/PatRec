WordCounter Pattern Recognition project
===
### Task:
For a particular keyword, download first 20 English videos shorter than 5 min, find all words and list word frequencies per video.

### Keywords:
* Orange
* Rainbow
* Wolverine
* Unicorn
* Nuclear Reactor
* Bon Jovi
* ColdPlay
* Donald Trump
* January
* Sushi

### Implementation
The project uses a makefile for running different tasks of the workflow. Tasks are implemented using python scripts and
existing libraries or APIs.
Three speech recognition solutions are used:
* PocketSphinx
* HavenOnDemand
* IBM Watson Speech Recognition

### Requirements:
* GNU Make
* Python 3.5 (3.4 should work, but is untested)
* FFmpeg binaries - https://ffmpeg.org/download.html
* pip
    * youtube-dl
    * pocketsphinx
    * havenondemand
    * SpeechRecognition

All the python packages should be installed by running `make depends`.
If Python is installed systemwide, this needs to be run with
administrative privileges.

HavenOnDemand and IBM Watson require

### Running
The following commands should form a workflow to run