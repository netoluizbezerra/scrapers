from elasticsearch import Elasticsearch
from datetime import datetime
import json

def json_to_elastic(_name, _where, _listings_detail):
    date = datetime.today().strftime('%Y-%m-%d')
    listing = _listings_detail

    _id = list()
    [_id.append('{}_{}_{}_{}'.format(date, _name, _where, i)) for i in range(len(listing))]

    es = Elasticsearch(
        ['https://search-inrealty-vuzxwpm254w4x7tu62c3ypdtoy.us-east-1.es.amazonaws.com'])
    try:
        for i in range(len(listing)):
            es.index(index='{}'.format(_name), id=_id[i], body=listing[i])
            print('{} loop'.format(i))
        print("SUCCESS uploading: {}, captured {} ".format(_name, date))

    except:
        with open('backup_{}_{}_{}.json'.format(date, _name, _where), 'w') as f:
            json.dump(_listings_detail, f)
        print("FAILURE uploading {} ".format(_name, date))

