from handEl     import handEl
from hahaHba    import hahaHba
from jSona      import jSona
from proCleaner import proSweeper

import os
import traceback
import pprint
pp = pprint.pprint

class seeCer :
    def __init__(self, hbase_meta_path, pro_path, see_path, ehost='localhost', eport=8080, hhost='localhost', hport=9090) :
        self.jso    = handEl()
        self.hmeta  = self.jso.loadJson(hbase_meta_path, ex=True)
        self.smeta  = self.jso.loadJson(os.path.join(see_path, "seeConfig.json"), ex=True)
        self.pmeta  = self.jso.loadJson(os.path.join(pro_path, "proConfig.json"), ex=True)
        self.he     = handEl(ehost, eport)
        self.hh     = handEl(hhost, hport)
        self.ps     = proSweeper(ehost, eport, None, pro_path)
        self.tabref = self.hmeta['TABLE']['REF']
        self.fields = [self.hmeta['TABLE']['COLUMN']['FAMILIES'][raw_cf] for raw_cf in self.hmeta['TABLE']['COLUMN']['RAW_FAM']]
        self.hbdict = {self.hmeta['TABLE']['COLUMN']['FAMILIES'][raw_cf]:raw_cf for raw_cf in self.hmeta['TABLE']['COLUMN']['RAW_FAM']}

    def decodeDict(self, d) :
        return {k0.decode():{k1.decode():v1.decode() for k1,v1 in d0.items()} for k0,d0 in d.items()} if type(d)==type({}) else {}

    def peek(self, text) :
        es_results = self.essearch(text)
        table_names = es_results[self.tabref] if self.tabref in es_results else ""
        if self.tabref in es_results : del(es_results[self.tabref])
        return self.decodeDict(self.hbsearch(table_names, es_results))

    def error(self, e, msg="") :
        print("ERROR {} : {}".format(msg, e))
        traceback.print_exc()
        return False

    # search(self, value, index=None, field="alias", fuzziness=0)
    def essearch(self, texts) :
        try :
            if type(texts) == type("") : texts = [texts]
            search_results = dict()
            for text in texts : 
                fuzziness = 0 if all(ord(c) < 128 for c in text) else 0 # if korean, fuzziness 1. 나중에 고치기
                for prop in self.fields+[self.tabref] :
                    result = self.ps.cleaning(prop, {'refers':[prop], 'fulltext':True}, {prop:[text]}, fuzziness=fuzziness)
                    if result : search_results[prop] = result
                for prop in self.pmeta['SWEEPER']['RULES'] : 
                    if prop in search_results : search_results[prop] = self.ps.ruling(prop, search_results[prop])
            return search_results
        except Exception as e:
            return self.error(e, "ESSEARCH"), False

    def hbsearch(self, names, conditions) :
        try :
            if len(names) == 0           : names = self.hmeta['TABLE']['IDS']
            elif type(names) == type("") : names = [names]
            
            # Create the filter query
            filter_queries = list()
            for field, values in conditions.items() :
                filter_values = list()
                for value in values :
                    filter_values.append(
                        "(FamilyFilter(=, 'binaryprefix:{}') AND QualifierFilter(=, 'substring:{}'))".format(self.hbdict[field], value))
                filter_queries.append(" OR ".join(filter_values))
            # print(filter_queries)
            # Get results, #+name
            search_results = dict()
            for name in names :
                seesets = list()
                for filter_query in filter_queries :
                    try :
                        seeset = set(self.hh.scan(self.hmeta['TABLE']['PREFIX']+name, filters=filter_query).keys())
                        if seeset : seesets.append(seeset)
                    except Exception as e :
                        self.error(e, 'FILTERING')
                        continue 
                if seesets :
                    search_results.update(self.hh.rows(self.hmeta['TABLE']['PREFIX']+name, list(set.intersection(*seesets))))
            return search_results

        except Exception as e:
            return self.error(e, "HBSEARCH"), False
