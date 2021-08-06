from link_extractor import get_url
from get_urls import _choose
from get_urls import _extract_features
from get_urls import _clean_where
from db import json_to_postgres
from datetime import datetime
import json
#
 # f = open('backup_wimoveis_Asa Norte_2021-02-18.json', "r")
 # urls = json.load(f)
 # f.close()
 # _name = 'wimoveis'


def scrapy_pipeline():
    _date = datetime.today().strftime('%Y-%m-%d')
    _name = input('Nome do Portal: ')
    _where = str(input('Nome do Bairro, Cidade ou Estado de procura: '))
    link = get_url(_name=_name, _where=_where)
    try:
        urls = _choose(_name=_name, link=link)
        try:
            listings_detail = _extract_features(_name=_name, links=urls)
            _where_cleaned = _clean_where(_where=_where)
#            json_to_postgres(_name=_name, _where=_where, _listings_detail=listings_detail)
            print('Success')
        except:
            with open('backup_{}_{}_{}.json'.format(_name, _where, _date), 'w') as f:
                json.dump(urls, f)
    except:
        print('Failed search for urls')




if __name__ == '__main__':
    scrapy_pipeline()

