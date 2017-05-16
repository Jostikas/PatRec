from glob import glob
from collections import Counter
import sys

if len(sys.argv) < 2:
    print("Print most common words across some word files, with length > 4."
          "Usage: python get_most.py <FILES>[ <NR>]\n"
          "\t<FILES> - Files to process. Accepts glob patterns."
          "\t<NR> - No. of most frequent items to show.")
    sys.exit(0)

with open('filter_words') as f:
    filter = f.readlines()
print ("Filtered words: ", filter)

all_words = ""

for path in glob(sys.argv[1]):
    with open(path) as f:
        all_words += f.read()

all_words = list(word.lower() for word in all_words.split() if word.lower() not in filter and len(word)>4)

c = Counter(all_words)

if len(sys.argv) > 2:
    print(c.most_common(int(sys.argv[2])))
else:
    print(c.most_common(3))



