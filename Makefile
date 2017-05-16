#Set these, likely by passing in from command line
# For processing whole topics, pass in topic names as a list to TOPICS
TOPICS = $(ALL_TOPICS)
# For processing a particular file/s, pass in it's/their name to SRC
SRC := $(wildcard $(TOPICS))

#-------------------------------------------------
# You shouldn't need to change anything under here.
ALL_TOPICS := Orange Rainbow Wolverine January Unicorn Sushi Donald_Trump Coldplay Nuclear_Reactor Bon_Jovi
DATA_DIR := data
DL_NAME = -o $(CURRENT_TOPIC)-%(playlist_index)d.wav
DL_OPTIONS := --extract-audio --audio-format wav --audio-quality 16K
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

SRC_FILES := $(sort $(wildcard $(SRC)))
DST_SPHINX := $(SRC_FILES:.wav=-sphinx.txt)
DST_HAVEN := $(SRC_FILES:.wav=-haven.txt)
DST_IBM := $(SRC_FILES:.wav=-ibm.txt)

.PHONY: all sphinx haven ibm csv clean_sphinx clean_haven clean_ibm clean_all checkdirs download

all: # Do nothing when no arguments given

checkdirs: $(DATA_DIR)

$(DATA_DIR):
	echo $@
	mkdir $@

depends:
	echo "ffmpeg needs to be installed manually, and the binaries should be in PATH. See https://ffmpeg.org/download.html."
	pip install youtube-dl pocketsphinx havenondemand SpeechRecognition

download: checkdirs
	%(foreach CURRENT_TOPIC, $(TOPICS), youtube-dl $(DL_OPTIONS) $(DL_NAME) $($(CURRENT_TOPIC)_PL)

%-sphinx.txt: %.wav
	python sphinx.py $< $@

%-haven.txt: %.wav
	python haven.py $< $@

%-ibm.txt: %.wav
	python ibm.py $< $@
	
sphinx: $(DST_SPHINX)

haven: $(DST_HAVEN)

ibm: $(DST_IBM)

csv: $(DST_HAVEN) $(DST_IBM) $(DST_SPHINX)

clean_sphinx:
	rm -f $(DST_SPHINX)
	
clean_haven:
	rm -f $(DST_HAVEN)
	
clean_ibm:
	rm -f $(DST_IBM)
	
clean_all: clean_sphinx clean_haven clean_ibm

clean_empty:
	python del_empty.py "$(SRC)"