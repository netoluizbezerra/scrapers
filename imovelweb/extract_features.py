import time
from scrapy.selector import Selector
import json
import re
import undetected_chromedriver as uc
from io import StringIO
from html.parser import HTMLParser

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



def extract_features_imovelweb(links):
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument()
    driver = uc.Chrome()
    temp = []
    i = -1

    for link in links:
        i += 1
        print('imovel {}'.format(i))
        driver.get('https://www.geoportal.seduh.df.gov.br/mapa/?extent=158185.6432,8233132.1800,242852.4792,8274460.1793&layers=Regi%C3%B5es%20Administrativas')
        time.sleep(2)
        html = driver.page_source
        response_obj = Selector(text=html)

        try:
            try:
                end1 = response_obj.xpath("//h2[@class='title-location']/text()").get()
                end2 = response_obj.xpath("//h2[@class='title-location']/span/text()").get()
                end = '{}{}'.format(end1, end2)
            except:
                end = response_obj.xpath("//h2[@class='title-location']/text()").get()
        except:
            end = 'NULL'

        if end == 'NoneNone':
            end = 'NULL'

        if end == 'None':
            end = 'NULL'

        attr = response_obj.xpath("//li[contains(@class, 'icon-feature')]").getall()
        listToStr = ' '.join([str(elem) for elem in attr])

        area_total_check = 'icon-stotal'
        area_util_check = 'icon-scubierta'
        vagas_check = 'icon-cochera'
        banheiros_check = 'icon-bano'
        quartos_check = 'icon-dormitorio'
        suites_check = 'icon-toilete'
        idade_imovel_check = 'icon-antiguedad'

        if area_total_check in listToStr:
            area_total = int(re.sub("[^0-9]", "", attr[0]))
            del attr[0]
        else:
            area_total = 0

        if area_util_check in listToStr:
            area_util = int(re.sub("[^0-9]", "", attr[0]))
            del attr[0]
        else:
            area_util = 0

        if banheiros_check in listToStr:
            banheiros = int(re.sub("[^0-9]", "", attr[0]))
            del attr[0]
        else:
            banheiros = 0

        if vagas_check in listToStr:
            vagas = int(re.sub("[^0-9]", "", attr[0]))
            del attr[0]
        else:
            vagas = 0

        if quartos_check in listToStr:
            quartos = int(re.sub("[^0-9]", "", attr[0]))
            del attr[0]
        else:
            quartos = 0

        if suites_check in listToStr:
            suites = int(re.sub("[^0-9]", "", attr[0]))
            del attr[0]
        else:
            suites = 0

        if idade_imovel_check in listToStr:
            if 'novo' in attr[0]:
                idade_imovel = 0
            else:
                idade_imovel = re.sub("[^0-9]", "", attr[0])
                del attr[0]
        else:
            idade_imovel = -1

        # URL:
        try:
            url = link['url']
        except:
            url = 'NULL'

        # Título:
        try:
            titulo = response_obj.xpath(
                "//*[@id='article-container']/section[1]/div[1]/h1/text()").get()
        except:
            titulo = 'NULL'

        # Preço:
        try:
            preco = response_obj.xpath(
                "//*[@id='contact-form-sticky']/div[1]/div[1]/div/div[1]/div[2]/span/span/text()").get()
            preco = preco.replace('R$', '').strip()
            preco = int(preco.replace('.', ''))
        except:
            preco = 0

        # IPTU
        try:
            extras = response_obj.xpath(
                "//div[@class='block-expensas block-row']/span/text()").getall()

            extras_str = response_obj.xpath(
                "//div[@class='block-expensas block-row']/text()").getall()

            listToStr_extras = ' '.join([str(elem) for elem in extras_str])

            if "Cond" and "IPTU" in listToStr_extras:
                cond = extras[0]
                cond = cond.replace('R$', '').strip()
                cond = int(cond.replace('.', ''))

                iptu = extras[1]
                iptu = iptu.replace('R$', '').strip()
                iptu = int(iptu.replace('.', ''))

            elif "Cond" in listToStr_extras:
                cond = extras[0]
                cond = cond.replace('R$', '').strip()
                cond = int(cond.replace('.', ''))

                iptu = 0

            elif "IPTU" in listToStr_extras:
                iptu = extras[0]
                iptu = iptu.replace('R$', '').strip()
                iptu = int(iptu.replace('.', ''))
                cond = 0
            else:
                iptu = 0
                cond = 0
        except:
            iptu = 0
            cond = 0

        # Imobiliária:
        try:
            imob = response_obj.xpath(
                "//h5[contains(@class, 'PublisherTitle')]/text()").get()
            imob = imob.replace('\n', ' ').strip()
        except:
            imob = 'NULL'

        # Descricao
        try:
            "//div[@id='longDescription']"
            description = response_obj.xpath("//*[@id='longDescription']/div/text()").getall()
            description_srt = ''
            for desc_line in description:
                description_srt += desc_line
        except:
            description_srt = 'NULL'

        # Coordenadas Geograficas
        try:
            coord_str = response_obj.xpath("//img[contains(@class, 'static-map')]/@src").get()
            coordinates = (coord_str.split("center=")[1]).split("&zoom")[0].split(',')
            latitude = coordinates[0]
            longitude = coordinates[1]

        except:
            latitude = 'NULL'
            longitude = 'NULL'

        # Amenities:
        try:
            amenities_temp = response_obj.xpath(
                "//div[contains(@class, 'AccordionItem-td4pyq')]"
            ).getall()
            amenities = ' '.join(amenities_temp)
            amenities_str = strip_tags(amenities)
        except:
            amenities_str = 'NULL'

        try:
            _type = response_obj.xpath(
                "//div[contains(@class, 'price-operation')]/text()"
            ).getall()
            _type = _type[0]
        except:
            _type = 'NULL'

        temp.append({
            'preco': preco,
            'iptu': iptu,
            'condominio': cond,
            'titulo': titulo,
            'desc': description_srt,
            'amen': amenities_str,
            'end': end,
            'area_tot': area_total,
            'area_util': area_util,
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

    with open('webimoveis.json', 'w') as f:
        json.dump(temp, f)
    return temp







