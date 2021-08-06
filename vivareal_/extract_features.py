import time
from scrapy.selector import Selector
import json
import re
import undetected_chromedriver as uc


def extract_features_vivareal(links):
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
        # endereço:
        try:
            end = response_obj.xpath("//div[contains(@class, 'title__address-wrapper')]/p/text()").get()
        except:
            end = 'NULL'
        # Atributos Principais:
        try:
            area_tot = int(response_obj.xpath(
                "//li[contains(@class, 'features__item features__item--area js-area')]/span/text()").get())
        except:
            area_tot = 0

        try:
            banheiros = int(response_obj.xpath(
                "//li[contains(@class, 'features__item features__item--bathroom js-bathrooms')]/span/text()").get())
        except:
            banheiros = 0

        try:
            vagas = int(response_obj.xpath(
                "//li[contains(@class, 'features__item features__item--parking js-parking')]/span/text()").get())
        except:
            vagas = 0

        try:
            quartos = int(response_obj.xpath(
                "//li[contains(@class, 'features__item features__item--bedroom js-bedrooms')]/span/text()").get())
        except:
            quartos = 0

        try:
            suites = int(response_obj.xpath(
                "//small[contains(@class, 'feature__extra-info')]/text()").get())
        except:
            suites = 0

        # URL:
        try:
            url = response_obj.xpath(
                "//meta[@property='og:url']/@content").get()
        except:
            url = 'NULL'

        # Título:
        try:
            titulo = response_obj.xpath(
                "//h3[contains(@class, 'description__title js-description-title')]/text()").get()
        except:
            titulo = 'NULL'

        # Preço:
        try:
            preco = response_obj.xpath(
                "//h3[contains(@class, 'price__price-info js-price-sale')]/text()").get()
            preco = preco.replace('R$', '').strip()
            preco = int(preco.replace('.', ''))
        except:
            preco = 0


        try:
            _type = response_obj.xpath(
                "//p[contains(@class, 'price__title')]/text()"
            ).get().strip()
            if _type == 'Compra':
                _type = 'Venda'
        except:
            _type = 'NULL'

        # Imobiliária:
        try:
            imob = response_obj.xpath(
                "//a[contains(@class, 'publisher__name')]/text()").get()
            imob = imob.replace('\n', ' ').strip()
        except:
            imob = 'NULL'
        # Código:
        # cod = response_obj.xpath(
        # "//p[contains(@class, 'description__text')]").get()
        try:
            cod = (url.split("center=")[1]).split("&zoom")[0]
        except:
            cod = 'NULL'

        # Descricao
        try:
            description_srt = ''
            description = response_obj.xpath("//p[contains(@class, 'description__text')]")
            for desc_line in description:
                description_srt += desc_line.xpath('./text()').get()
        except:
            description_srt = 'NULL'

        # Coordenadas Geograficas
        try:
            latitude = response_obj.xpath("//meta[contains(@property, 'latitude')]/@content").get()
            longitude = response_obj.xpath("//meta[contains(@property, 'longitude')]/@content").get()
        except:
            latitude = 'NULL'
            longitude = 'NULL'

        if latitude is None:
            latitude = 'NULL'
        if longitude is None:
            longitude = 'NULL'
        # Amenities:
        try:
            amenities_str = ''
            amenities_temp = response_obj.xpath(
                "//ul[contains(@class, 'amenities__list')]/li"
            )
            for amenity in amenities_temp:
                amenities_str += amenity.xpath("./text()").get()
        except:
            amenities_str = 'NULL'

        try:
            condo = response_obj.xpath(
                "//span[contains(@class, 'price__list-value condominium')]/text()"
            ).get()
            condo = condo.replace('R$', '').strip()
            condo = int(condo.replace('.', ''))
        except:
            condo = 0

        try:
            iptu = response_obj.xpath(
                "//span[contains(@class, 'price__list-value iptu')]/text()"
            ).get()
            iptu = iptu.replace('R$', '').strip()
            iptu = int(iptu.replace('.', ''))
        except:
            iptu = 0

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


