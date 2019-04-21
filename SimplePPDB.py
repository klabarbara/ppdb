# Dev mode
dev = True
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


        


