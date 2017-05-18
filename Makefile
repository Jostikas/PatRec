ALL_TOPICS := Orange Rainbow Wolverine January Unicorn Sushi Donald_Trump Coldplay Nuclear_Reactor Bon_Jovi
#Set these, likely by passing in from command line
# For processing whole topics, pass in topic names as a list to TOPICS
TOPICS := $(ALL_TOPICS)
# For processing a particular file/s, pass in it's/their name to SRC
SRC := $(addsuffix -*.wav,$(TOPICS))

#-------------------------------------------------
# You shouldn't need to change anything under here.
DATA_DIR := data
CSV_DIR := csv
Orange_PL := https://www.youtube.com/playlist?list=PLXUEko325Z-D7BjUkNDi5GvOU9dey8Cmb
Rainbow_PL := https://www.youtube.com/playlist?list=PLXUEko325Z-D7uFK7B4wjDzEN9a3YraF0
Wolverine_PL := https://www.youtube.com/playlist?list=PLXUEko325Z-BX_lS2HBtszzQ1ZqV2crrm
January_PL  := https://www.youtube.com/playlist?list=PLIERL4oks-lfB3c3blAE6r3J9JRnKwqoK
Unicorn_PL := https://www.youtube.com/playlist?list=PLIERL4oks-leKg3101ERCEsyE_Rs2FEuP
Sushi_PL := https://www.youtube.com/playlist?list=PLIERL4oks-ldvb_2lBcfCKIbjzkGwXhnM
Donald_Trump_PL := https://www.youtube.com/playlist?list=PLIERL4oks-ldSO-E5NwoRmahyLeT8xNrw
Coldplay_PL := https://www.youtube.com/playlist?list=PLIERL4oks-lflMeU0TLNhHIuv26BYGhRN
Nuclear_Reactor_PL := https://www.youtube.com/playlist?list=PLIERL4oks-ldUhDQ0_ZrLGQLOYxu25nKy
Bon_Jovi_PL := https://www.youtube.com/playlist?list=PLIERL4oks-lerKqL_3zQ6Ft154kRkl8zs

SRC_FILES := $(foreach pattern,$(SRC),$(sort $(wildcard $(DATA_DIR)/$(pattern))))
DST_SPHINX := $(SRC_FILES:.wav=-sphinx.txt)
DST_HAVEN := $(SRC_FILES:.wav=-haven.txt)
DST_IBM := $(SRC_FILES:.wav=-ibm.txt)
DST_CENTER := $(SRC_FILES:.wav=-voice.wav)
DST_SPHINX_CSV := $(foreach pattern,$(SRC:-*.wav=-sphinx.csv),$(DATA_DIR)/$(pattern))
DST_HAVEN_CSV := $(foreach pattern,$(SRC:-*.wav=-haven.csv),$(DATA_DIR)/$(pattern))
DST_IBM_CSV := $(foreach pattern,$(SRC:-*.wav=-ibm.csv),$(DATA_DIR)/$(pattern))

# Create targets for download jobs
DL_JOBS := $(addprefix DL_JOB_,$(TOPICS))

.PHONY: all detect sphinx haven ibm csv clean_sphinx clean_haven clean_ibm clean_audio clean_all download csv DL_JOB_%

all: # Do nothing when no arguments given

# Check and if necessary, create data dir
$(DATA_DIR):
	echo $@
	mkdir $@

# check dependencies
depends:
	echo "ffmpeg needs to be installed manually, and the binaries should be in PATH. See https://ffmpeg.org/download.html."
	pip install youtube-dl pocketsphinx havenondemand SpeechRecognition

# Download videos. Ignore download errors.
DL_OPTIONS := -i --extract-audio --audio-format=wav --audio-quality=16K
DL_NAME = -o $(DATA_DIR)/$*-%(playlist_index)d.%(ext)s
DL_URL = $($*_PL)

DL_JOB_%:
	-youtube-dl $(DL_OPTIONS) $(DL_NAME) $(DL_URL)

download: $(DATA_DIR) $(DL_JOBS)
	echo "Downloaded."

%-sphinx.txt: %.wav
	python sphinx.py $< $@

%-haven.txt: %.wav
	python haven.py $< $@

%-ibm.txt: %.wav
	python ibm.py $< $@

%-voice.wav: %.wav
	python extract_center.py $< $@
	
sphinx: $(DST_SPHINX)

haven: $(DST_HAVEN)

ibm: $(DST_IBM)

detect: sphinx ibm haven

center: $(DST_CENTER)

%-sphinx.csv:
	python make_csv.py $*-*-sphinx.txt $@
	
%-haven.csv:
	python make_csv.py $*-*-haven.txt $@
	
%-ibm.csv:
	python make_csv.py $*-*-ibm.txt $@
	
csv: $(DST_SPHINX_CSV) $(DST_HAVEN_CSV) $(DST_IBM_CSV)
	
clean_sphinx:
	rm -f $(DST_SPHINX)
	
clean_haven:
	rm -f $(DST_HAVEN)
	
clean_ibm:
	rm -f $(DST_IBM)

clean_audio:
	rm -f $(SRC_FILES)
	
clean_all: clean_sphinx clean_haven clean_ibm

clean_empty:
	python del_empty.py "$(SRC)"