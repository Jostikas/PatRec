WordCounter Pattern Recognition project
===
### Task:
For a particular keyword, download first 20 English videos shorter than 5 min, find all words and list word frequencies per video.
`filter_words` contains words that are not considered for word frequency
calculation.

### Keywords and playlists:
* Orange - https://www.youtube.com/playlist?list=PLXUEko325Z-D7BjUkNDi5GvOU9dey8Cmb
* Rainbow - https://www.youtube.com/playlist?list=PLXUEko325Z-D7uFK7B4wjDzEN9a3YraF0
* Wolverine - https://www.youtube.com/playlist?list=PLXUEko325Z-BX_lS2HBtszzQ1ZqV2crrm
* Unicorn - https://www.youtube.com/playlist?list=PLIERL4oks-leKg3101ERCEsyE_Rs2FEuP
* Nuclear Reactor - https://www.youtube.com/playlist?list=PLIERL4oks-ldUhDQ0_ZrLGQLOYxu25nKy
* Bon Jovi - https://www.youtube.com/playlist?list=PLIERL4oks-lerKqL_3zQ6Ft154kRkl8zs
* ColdPlay - https://www.youtube.com/playlist?list=PLIERL4oks-lflMeU0TLNhHIuv26BYGhRN
* Donald Trump - https://www.youtube.com/playlist?list=PLIERL4oks-ldSO-E5NwoRmahyLeT8xNrw
* January - https://www.youtube.com/playlist?list=PLIERL4oks-lfB3c3blAE6r3J9JRnKwqoK
* Sushi - https://www.youtube.com/playlist?list=PLIERL4oks-ldvb_2lBcfCKIbjzkGwXhnM

### Implementation
The project uses a makefile for running different tasks of the workflow. Tasks are implemented using python scripts and
existing libraries or APIs.
Three speech recognition solutions are used:
* PocketSphinx
* HavenOnDemand
* IBM Watson Speech Recognition

For evaluation, the usernames and passwords for IBM and Haven have
been hardcoded.

As an evolution, a voice extraction implementation is included in
`extract-center.py`, based on http://www.virtualdub.org/blog/pivot/entry.php?id=102
It is accessible via make as `make center` and accepts the same arguments
as the other tasks. It has not been included in the workflow, as a need
for it only became apparent as we ran the dataset for the poster. As such,
it is tested only on short snippets of sound.

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

### Running
The following commands should form a workflow. All accept optional topic
flags of the form `TOPIC="Wolverine Bon_Jovi"` (note the underscore) and all but downloading
accept input file lists of the form `SRC="Wolverine-2.wav Bon_Jovi-[2-5].wav"`.

* `make download` - Downloads videos
* `make detect` - Runs all three detection algorithms on the files
* `make csv` - Create CSV files with word frequencies.

To hasten processing, it will make sense to pass `-j[num_processes]` to
`make`. However, in such a case it is advisable to perform the processing
separately with `make -j[num_cpu] sphinx`, `make -j8 ibm` and `make -j2 haven`,
as sphinx is CPU-bound and HavenOnDemand heavily throttles request rate,
causing failure.