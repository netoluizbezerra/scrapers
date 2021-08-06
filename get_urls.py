from unidecode import unidecode

from wimoveis.get_urls import get_urls_wimoveis
from imovelweb.get_urls import get_urls_imovelweb
from vivareal_.get_urls import get_urls_vivareal
from df_imoveis.get_urls import get_urls_dfimoveis

from wimoveis.extract_features import extract_features_wimoveis
from imovelweb.extract_features import extract_features_imovelweb
from vivareal_.extract_features import extract_features_vivareal
from df_imoveis.extract_features import extract_features_dfimoveis


def _choose(_name, link):
    if _name == 'wimoveis':
        temp = get_urls_wimoveis(link)

    elif _name == 'imovelweb':
        temp =get_urls_imovelweb(link)

    elif _name == 'vivareal':
        temp = get_urls_vivareal(link)

    elif _name == 'dfimoveis':
        temp = get_urls_dfimoveis(link)

    else:
        temp = []
        print('Not yet supported')

    return temp


def _extract_features(_name, links):
    if _name == 'imovelweb':
        temp = extract_features_imovelweb(links)

    elif _name == 'wimoveis':
        temp = extract_features_wimoveis(links)

    elif _name == 'vivareal':
        temp = extract_features_vivareal(links)

    elif _name == 'dfimoveis':
        temp = extract_features_dfimoveis(links)

    else:
        temp = []

    return temp

def _clean_where(_where):
    _where_string = _where.split(',')[0]
    _where_string = _where_string.replace(' ', '_')
    _where_string = unidecode(_where_string).lower()
    return _where_string



