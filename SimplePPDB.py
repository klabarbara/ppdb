import nltk
import json
# Dev mode

dev = False

def chomp(x):
    if x.endswith("\r\n"): return x[:-2]
    if x.endswith("\n") or x.endswith("\r"): return x[:-1]
    return x

def filt(x):
        return x.label()=='JP'

class SimplePPDB(object):

    def __init__(self):
        # each key in self is a token, and each value is a tuple (set, dict).
        super(SimplePPDB, self).__init__()

        self.SimplePPDB_dict = {}

    def load(self,path):
        ppdb  = open(path, 'r')
        lines = ppdb.readlines()

        for line in lines:
            # discard lines with unrecoverable encoding errors
            if '\\ x' in line or 'xc3' in line:
                continue
            split = line.split(sep = '\t')
            if split[3] not in self.SimplePPDB_dict:
                self.SimplePPDB_dict[split[3]] = []
            self.SimplePPDB_dict[split[3]].append(split)


        ppdb.close()
    def __getitem__(self, key):
        """
            Return a list of simplifications, if only the key is supplied
            Return shortlisted simplifications, if both key and syntactic category is supplied
                e.g.: Simple
            :param :

        """
        if isinstance(key, str):
            if dev:
                print("Single argument subscripting")
            return self.search(key)
        elif len(key) == 2:
            dict_key, syntax_cat = key
            if isinstance(dict_key, str) and isinstance(syntax_cat, str):
                if dev:
                    print("2 arguments subscripting")
                return self.search(dict_key, syntax_cat=syntax_cat)


        raise KeyError("Invalid subscripting, no appropriate subscription method!")

    def search(self, key, syntax_cat=None):
        key = key.lower()
        if key not in self.SimplePPDB_dict:
            return []
            # raise KeyError("Key not found! str:" + key)
        prelim_search_result = self.SimplePPDB_dict[key]
        search_result = []
        if syntax_cat != None:
            for result in prelim_search_result:
                if (result[2] == syntax_cat or result[2] == "[" + syntax_cat + "]"):
                    search_result.append(result)
        else:
            search_result = prelim_search_result

        return search_result



    def replacement(self, question, replacement=None, pos="JJ", train = True):
        # Tutorial: https://medium.com/greyatom/learning-pos-tagging-chunking-in-nlp-85f7f811a8cb

        """

        Parameter:
        Replacement –– dict


        """

        grammar = ('''
        NP: {<DT>?<JJ>*<NN>}
        JP: {<JJ><JJ>}
        ''')
        token = nltk.word_tokenize(question)
        tagged = nltk.pos_tag(token)
        modified = False

        # chunkParser = nltk.RegexpParser(grammar)
        # tree = chunkParser.parse(tagged)
        sentence = []
        if replacement is None:
            # for subtree in t.subtrees(filter =  filt): # Generate all subtrees


            # JJ_word = []
            # for pos in tagged:
            #     if pos[1] == "JJ":
            #         JJ_word.append(pos[0])
            #     else:
            #         if len(JJ_word) > 0:

            # replaced = []
            for tag in tagged:
                if tag[1] == pos:
                    modified = True
                    word_replacement = self.search(tag[0], pos)
                    if len(word_replacement) > 0:
                        if dev:
                            print(word_replacement[0])

                        word_replacement = chomp(word_replacement[0][4])

                    else:
                        word_replacement = chomp(tag[0])


                    sentence.append(word_replacement)
                else:
                    sentence.append(tag[0])

        else:
            for tag in tagged:
                if tag[1] == pos and tag[0] in replacement:



                    sentence.append(replacement[tag[0]])
                else:
                    sentence.append(tag[0])

        if(modified or not train):
            return " ".join(sentence)
        else:
            return None

    def guesser_swap(self,questions):
        new_qs = []
        for question in questions:
            qdict = question.to_dict()

            #key_locs = [k.start() for k in re.finditer(key, qdict['text'])]
            qdict['text'] = self.replacement(qdict['text'], train = False)
            qdict['first_sentence'] = self.replacement(qdict['first_sentence'], train = False)
            (start,end) = qdict['tokenizations'][0]
            tok_len = end-start
            new_toks = []
            for i in range(start,len(qdict['text']),tok_len+1):
                if i+tok_len+1 > len(qdict['text']):
                    new_toks.append([i,len(qdict['text'])])
                else:
                    new_toks.append([i,i+tok_len])
            qdict['tokenizations'] = new_toks
            new_qs.append(question.from_dict(qdict))
        return new_qs

    def json_appender(self,filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            questions = data['questions']
            for question in questions:
                orig_len = len(question['text'])
                question['text'] = self.replacement(question['text'])
        return data
