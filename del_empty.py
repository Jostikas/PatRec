import sys
import os
from glob import glob

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Delete empty files\n"
          "\tUsage: python del_empty.py <infile>\n"
          "\t<infile> - Input files to check. Accepts wildcards\n")
    sys.exit(0)

print("Removing empty files:")
for fname in glob(sys.argv[1]):
    if os.stat(fname).st_size == 0:
        os.remove(fname)
        print(fname)