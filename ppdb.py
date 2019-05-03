import re
import json

ppdb_dict = None

class PPDB(object):

    def __init__(self):
        # each key in self is a token, and each value is a tuple (set, dict).
        super(PPDB, self).__init__()

        self.ppdb_dict = {}

    def load_ppdb(self,path):
        ppdb  = open(path, 'r')
        lines = ppdb.readlines()

        for line in lines:
            # discard lines with unrecoverable encoding errors
            if '\\ x' in line or 'xc3' in line:
                continue
            split = line.split(sep = ' ||| ')
            phrase = split[1]
            self.ppdb_dict[phrase] = {}

            paraphrase = split[2]
            # print(paraphrase)
            self.ppdb_dict[phrase][paraphrase] = {} #associated attributes for paraphrase
            self.ppdb_dict[phrase][paraphrase][0] = split[0] #Part of speech tag
            feat = split[3].split(sep = ' ') #splitting up feature data
            count = 1
            for data in feat: #adding feature data piecewise into paraphrase dict
                self.ppdb_dict[phrase][paraphrase][count] = data
                count += 1
            self.ppdb_dict[phrase][paraphrase][count] = split[4] #alignment
            self.ppdb_dict[phrase][paraphrase][count + 1] = split[5] #entailment
        ppdb.close()


    '''
    Returns a dictionary of paraprases and their simplifications.
    ex: {'most common': 'common', 'excessively specific': 'specific'}
    '''
    def get_simplified(self, filename):
        with open(filename, 'r') as f:
            simps = {}
            lines = f.readlines()
            for line in lines:
                split = line.split(sep = '\t')
                simps[split[3]] = split[4][:-1]
        return simps

    def json_swap(self,filename,d={'most common': 'common'}):
        with open(filename, 'r') as f:
            data = json.load(f)
            questions = data['questions']
            for key in d:
                for question in questions:
                    question['text'] = re.sub(key, d[key], question['text'])
                data['questions'] = questions
        return data
