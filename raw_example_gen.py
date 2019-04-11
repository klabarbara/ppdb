import re
import pandas as pd
import numpy as np

ppdb  = open("tldr_ppdb", 'r')
raw_pp  = open("what_results_tldr_raw", 'w')

lines = ppdb.readlines()

for line in lines:
    split = line.split(sep = ' ||| ')
    if(split[1] == 'what'):
        raw_pp.write(line)
