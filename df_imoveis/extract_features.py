import time
from scrapy.selector import Selector
import json
import re
import undetected_chromedriver as uc
from io import StringIO
from html.parser import HTMLParser
import re


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def extract_features_dfimoveis(links):
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument('--headless')
    driver = uc.Chrome(options=options)
    temp = []
    i = -1

    for link in links:
        i += 1
        print('imovel {}'.format(i))
        driver.get(link['url'])
        time.sleep(4)
        html = driver.page_source
        response_obj = Selector(text=html)

        # Preço:
        try:
            preco = response_obj.xpath("//small[contains(@class, 'display-4 text-warning')]/text()").get()
            preco = preco.replace('R$', '').strip()
            preco = int(preco.replace('.', ''))
        except:
            preco = 0

        # Titulo
        try:
            titulo = response_obj.xpath(
                "//h6[contains(@class, 'mobile-h6 mb-0')]/text()").get()
        except:
            titulo = 'NULL'

        # Endereço
        try:
            try:
                if len(response_obj.xpath(
                        "//h6[contains(@class, 'mb-0 text-normal text-nowrap')]/small/text()").getall()) > 2:
                    cidade = response_obj.xpath(
                        "//h6[contains(@class, 'mb-0 text-normal text-nowrap')]/small/text()").getall()[0]
                    bairro = response_obj.xpath(
                        "//h6[contains(@class, 'mb-0 text-normal text-nowrap')]/small/text()").getall()[1]
                else:
                    cidade = response_obj.xpath(
                        "//h6[contains(@class, 'mb-0 text-normal text-nowrap')]/small/text()").getall()[0]
                    bairro = ''
            except:
                bairro = ''
                cidade = ''
            end = response_obj.xpath("//h1[contains(@class, 'mb-0 font-weight-600 mobile-fs-1-5')]/text()").get()
            end = end + cidade + ' ' + bairro
        except:
            end = 'NULL'

        # Área Útil
        try:
            area_util = response_obj.xpath("//h6[contains(@class, ' text-normal mb-0')]/small/text()").getall()[1]
            area_util = int(area_util.split(",")[0])
        except:
            area_util = 0

        # Área Total
        area_tot = 0

        # Coordenadas Geograficas
        try:
            coord = response_obj.xpath("//script[contains(@type, 'text/javascript')]").getall()
            coord = ''.join(coord)
            latitude = (coord.split("latitude = ")[1]).split(";\n")[0]
            longitude = (coord.split("longitude = ")[1]).split(";\n")[0]
        except:
            latitude = 'NULL'
            longitude = 'NULL'

        if latitude is None:
            latitude = 'NULL'
        if longitude is None:
            longitude = 'NULL'

        try:
            list_all = ' '.join(response_obj.xpath("//h6[contains(@class, 'mb-0 text-normal')]/small").getall())

            if 'quart' in list_all:
                quartos = list_all.split("quart")[0]
                quartos = int(quartos[-3:])
            else:
                quartos = 0

            if 'su' in list_all:
                suites = list_all.split("su")[0]
                suites = int(suites[-3:])
            else:
                suites = 0

            if 'vag' in list_all:
                vagas = list_all.split("vag")[0]
                vagas = int(vagas[-3:])
            else:
                vagas = 0

            if 'banheir' in list_all:
                banheiros = list_all.split("banheir")[0]
                banheiros = int(banheiros[-3:])
            else:
                banheiros = 0
        except:
            quartos = 0
            suites = 0
            vagas = 0
            banheiros = 0

        try:
            condo = int(response_obj.xpath("//h6[contains(@class, 'mb-0 text-normal')]/small/text()").getall()[0])
        except:
            condo = 0

        # Descricao
        try:
            description_srt = response_obj.xpath("//p[contains(@class, 'w-100 pb-3 mb-0 texto-descricao')]/text()").getall()
            description_srt = ''.join(description_srt)
            description_srt = description_srt.replace('\n', '')
        except:
            description_srt = 'NULL'

            # URL:
        try:
            url = response_obj.xpath(
                "//meta[@property='og:url']/@content").get()
        except:
            url = 'NULL'

        # Amenities:
        try:
            amenities_str = response_obj.xpath("//ul[contains(@class, 'checkboxes')]").getall()

            amenities_str = strip_tags(''.join(amenities_str))
            amenities_str = amenities_str.replace('\n', ' ')
            amenities_str = re.sub(' +', ' ', amenities_str)
        except:
            amenities_str = 'NULL'

        try:
            _type = ''.join(response_obj.xpath("//h6[contains(@class, ' text-normal mb-0')]/text()").getall()).lower()
            if 'aluguel' in _type:
                _type = 'Aluguel'
            elif 'venda' in _type:
                _type = 'Venda'
            elif 'lançamento' in _type:
                _type = 'Lançamento'
            else:
                _type = 'NULL'
        except:
            _type = 'NULL'

        # Imobiliária:
        try:
            imob = response_obj.xpath(
                "//h6[contains(@class, 'pb-0 mb-0')]/text()"
            ).get()
        except:
            imob = 'NULL'

        iptu = 0

        print({
            'preco': preco,
            'iptu': iptu,
            'condominio': condo,
            'titulo': titulo,
            'desc': description_srt,
            'amen': amenities_str,
            'end': end,
            'area_tot': area_tot,
            'area_util': 0,
            'banheiros': banheiros,
            'vagas': vagas,
            'quartos': quartos,
            'suites': suites,
            'imob': imob,
            'url': url,
            'latitude': latitude,
            'longitude': longitude,
            'type': _type
        })

        temp.append({
            'preco': preco,
            'iptu': iptu,
            'condominio': condo,
            'titulo': titulo,
            'desc': description_srt,
            'amen': amenities_str,
            'end': end,
            'area_tot': area_tot,
            'area_util': 0,
            'banheiros': banheiros,
            'vagas': vagas,
            'quartos': quartos,
            'suites': suites,
            'imob': imob,
            'url': url,
            'latitude': latitude,
            'longitude': longitude,
            'type': _type
        })

    with open('vivareal.json', 'w') as f:
        json.dump(temp, f)
    return temp


