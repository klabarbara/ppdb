import re
import pandas as pd
import numpy as np

target_phrases = ['what']
ppdb_filename = "tldr_ppdb"
pp_dict = {}

def phrase_scrape(target_phrases, ppdb_filename):
    ppdb  = open(ppdb_filename, 'r')
    lines = ppdb.readlines()

    for phrase in target_phrases:
        pp_dict[phrase] = {}
        for line in lines:
            split = line.split(sep = ' ||| ')
            if(split[1] == phrase):
                paraphrase = split[2]
                print(paraphrase)
                pp_dict[phrase][paraphrase] = {} #associated attributes for paraphrase
                pp_dict[phrase][paraphrase][0] = split[0] #Part of speech tag
                feat = split[3].split(sep = ' ') #splitting up feature data
                count = 1
                for data in feat: #adding feature data piecewise into paraphrase dict
                    pp_dict[phrase][paraphrase][count] = data
                    count += 1
                pp_dict[phrase][paraphrase][count] = split[4] #alignment
                pp_dict[phrase][paraphrase][count + 1] = split[5] #entailment
    ppdb.close()

if __name__ == '__main__':
    phrase_scrape(target_phrases, ppdb_filename)
