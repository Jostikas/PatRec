import sys
import os
from glob import glob
from collections import Counter
from csv import writer
from itertools import chain


if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Collect wordlist into a CSV file with word frequencies."
          "Usage: python get_most.py <FILES>[ <NR>]\n"
          "\t<FILES> - Files to process. Accepts glob patterns."
          "\t<OUTFILE> - Output file")
    sys.exit(0)

with open('filter_words') as f:
    filter = f.readlines()
print ("Filtered words: ", filter)

with open(sys.argv[2], 'w', newline='') as csvfile:
    csvwriter = writer(csvfile)
    for vidpath in sorted(glob(sys.argv[1])):
        with open(vidpath) as f:
            vid_words = f.read()
        vid_words = list(word.lower() for word in vid_words.split() if word.lower() not in filter)
        c = Counter(vid_words)
        row = [os.path.basename(vidpath)]  # Add video name
        row.extend(chain.from_iterable(c.most_common()))   # Add word-count pairs
        print(row[:9],"...")
        csvwriter.writerow(row)


