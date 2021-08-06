from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from scrapy.selector import Selector
import time


def get_url(_name, _where):
    if _name == 'wimoveis':
        link = 'https://www.wimoveis.com.br/imoveis-distrito-federal-goias.html'

        driver = uc.Chrome()
        driver.get(link)

        search = driver.find_element_by_xpath("(//input[contains(@aria-label, 'Buscar por ciudad o barrio')])[2]")
        time.sleep(5)
        search.send_keys(_where)
        time.sleep(5)

        html_temp = driver.page_source
        response_obj_temp = Selector(text=html_temp)
        items = response_obj_temp.xpath("//li[@aria-label]").extract()
        temp = []
        for item in items:
            temp.append((item.split('aria-label="')[1]).split('" ')[0])
        for i in range(len(temp)):
            print('Selcione {} -> {}'.format(i, temp[i]))

        _option = int(input('Selecione Opção')) + 1
        _item = driver.find_element_by_xpath("(//a[contains(@class, 'dropdown-item')])[{}]".format(_option))
        _item.click()

        time.sleep(5)
        url = driver.current_url

        html = driver.page_source
        response_obj = Selector(text=html)

        print(response_obj.xpath("//h1[contains(@class, 'list-result-title')]/text()").get())
        driver.close()
        return url

    if _name == 'imovelweb':
        link = 'https://www.imovelweb.com.br/imoveis.html'

        driver = uc.Chrome()
        driver.get(link)

        search = driver.find_element_by_xpath("(//input[contains(@aria-label, 'Buscar por ciudad o barrio')])[2]")
        time.sleep(5)
        search.send_keys(_where)
        time.sleep(5)

        html_temp = driver.page_source
        response_obj_temp = Selector(text=html_temp)
        items = response_obj_temp.xpath("//li[@aria-label]").extract()
        temp = []
        for item in items:
            temp.append((item.split('aria-label="')[1]).split('" ')[0])
        for i in range(len(temp)):
            print('Selcione {} -> {}'.format(i, temp[i]))

        _option = int(input('Selecione Opção')) + 1
        _item = driver.find_element_by_xpath("(//a[contains(@class, 'dropdown-item')])[{}]".format(_option))
        _item.click()

        time.sleep(5)
        url = driver.current_url

        html = driver.page_source
        response_obj = Selector(text=html)

        print(response_obj.xpath("//h1[contains(@class, 'list-result-title')]/text()").get())
        driver.close()
        return url

    if _name == 'vivareal':
        _type = int(input('0 -> Aluguel; 1 -> Venda'))
        _type_list = ['aluguel', 'venda']
        link = 'https://www.vivareal.com.br/{}/'.format(_type_list[_type])

        driver = uc.Chrome()
        driver.get(link)

        search = driver.find_element_by_xpath("(//input[contains(@placeholder, 'Digite uma rua')])")
        time.sleep(5)
        search.send_keys(_where)
        time.sleep(5)
        search.send_keys(Keys.RETURN)

        time.sleep(5)
        url = driver.current_url

        html = driver.page_source
        response_obj = Selector(text=html)

        num_of_results = response_obj.xpath("//h1[contains(@class, 'results-summary')]/strong/text()").get().strip()
        print('Número de imóveis encontrados é de {}'.format(num_of_results))
        driver.close()
        return url

    if _name == 'dfimoveis':
        _type = int(input('0 -> Aluguel; 1 -> Venda'))
        _type_list = ['aluguel', 'venda']
        link = 'https://www.dfimoveis.com.br/{}/df/todos/imoveis'.format(_type_list[_type])

        driver = uc.Chrome()
        driver.get(link)

        html_temp = driver.page_source
        response_obj_temp = Selector(text=html_temp)

        items = response_obj_temp.xpath("//select[contains(@class, 'cidades search__select to-upper')]/option/text()").extract()
        temp = []

        for item in items:
            temp.append(item)
        for i in range(len(temp)):
            print('Selcione {} -> {}'.format(i, temp[i]))

        _option = int(input('Selecione Opção')) + 1

        _item = driver.find_element_by_xpath("(//select[contains(@class, 'cidades search__select to-upper')]/option)[{}]".format(_option))
        _item.click()
        time.sleep(3)
        _item = driver.find_element_by_xpath("(//button[contains(@class, 'search__button')])[2]".format(_option))
        _item.click()

        time.sleep(6)
        html_temp = driver.page_source
        response_obj_temp = Selector(text=html_temp)
        url = driver.current_url

        num_of_results = response_obj_temp.xpath("//h1[contains(@itemprop, 'name')]/text()").get()
        print('Número de imóveis encontrados é de {}'.format(num_of_results))
        driver.close()
        return url

    else:
        print('Ainda não temos este portal - EM BREVE!')



