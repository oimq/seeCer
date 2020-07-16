## seeCer

##### Search the data from HBase

for installing and using, requirements are below : 

* tqdm : https://github.com/tqdm/tqdm

* elasticsearch : https://github.com/elastic/elasticsearch-py

* happybase : https://github.com/python-happybase/happybase

* handEl : https://github.com/oimq/handEl

* hahaHba : https://github.com/oimq/hahaHba

* proCleaner : https://github.com/oimq/proCleaner

* jSona : https://github.com/oimq/jSona

***

### Installation

The pre-install resource is handEl, hahaHba, proCleaner, jSona

```code
pip3 install seeCer-master/
```

***

### Projects

The seeCer is consisted in two parts 

##### seeCer

* essearch : Searching entities from elasticsearch database.

* hbsearch : Searching data from HBase database. the conditions follow the HBase category structure.

* peek : Integrate essearch and hbsearch functions

##### seetools

* for now, only need to define a elasticsearch index prefix.

***

### Examples

* Script
```python3
from seeCer import seeCer
from pprint import pprint as pp

if __name__=="__main__" :
    HAH_PATH = './settings/hbase_meta.json'
    PRO_PATH = './settings/'
    SEE_PATH = './settings/'
    sc = seeCer(HAH_PATH, PRO_PATH, SEE_PATH)
    data = sc.essearch("i want to put some men black tshirt")
    pp(data)
    
    data = sc.decodeDict(sc.hbsearch(data['category'], {
        k:data[k] for k in list(filter(lambda k:k!='category', data.keys()))}))
    pp([data[k] for k in list(data.keys())[:2]])
```
* Outputs
```python
LOAD SUCCESS FROM [ ./settings/hbase_meta.json ]
LOAD SUCCESS FROM [ ./settings/seeConfig.json ]
LOAD SUCCESS FROM [ ./settings/proConfig.json ]
Elasticsearch Connection Success [localhost:8080]
HBase Connection Success [localhost:9090]
Elasticsearch Connection Success [localhost:8080]
{'age': ['adult'],
 'category': ['tshirt'],
 'color': ['black'],
 'gender': ['men']}
[{'a:adult': '1',
  'b:edwin': '1',
  'c:black': '1',
  'f:roundneck': '1',
  'f:vneck': '1',
  'g:men': '1',
  'i:c': 'UHNp5DtSf*hNYpzX^ntV',
  'i:t': 't-shirt print ',
  'i:v': '1',
  'm:zalando': '1',
  't:cotton': '1',
  'u:d': '{"black": '
         '"https://img02.ztat.net/article/ED/32/2O/02/LQ/11/ED322O02L-Q11@6.jpg?imwidth=1800&filter=packshot"}',
  'u:i': 'https://img02.ztat.net/article/ED/32/2O/02/LQ/11/ED322O02L-Q11@6.jpg?imwidth=1800&filter=packshot',
  'u:s': 'https://www.zalando.co.uk//edwin-print-t-shirt-black-ed322o02l-q11.html',
  'v:p': '29.74',
  'v:u': 'euro'},
 {'a:adult': '1',
  'b:adidas': '1',
  'c:black': '1',
  'g:men': '1',
  'i:c': 'UHNpAx4AfADf*ng%.gat',
  'i:t': 'lin tee print tshirt',
  'i:v': '1',
  'm:zalando': '1',
  'u:d': '{"black": '
         '"https://img01.ztat.net/article/AD/54/2D/20/PQ/11/AD542D20P-Q11@4.jpg?imwidth=1800&filter=packshot"}',
  'u:i': 'https://img01.ztat.net/article/AD/54/2D/20/PQ/11/AD542D20P-Q11@4.jpg?imwidth=1800&filter=packshot',
  'u:s': 'https://www.zalando.co.uk/adidas-performance-lin-tee-print-t-shirt-ad542d20p-q11.html',
  'v:p': '16.95',
  'v:u': 'euro'}]
```

***


### Notices

###### Unauthorized distribution and commercial use are strictly prohibited without the permission of the original author and the related module.
