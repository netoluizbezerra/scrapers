from scrapy.selector import Selector
import time
import json as json
import undetected_chromedriver as uc


def get_urls_imovelweb(link):
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument('--headless')
    driver = uc.Chrome(options=options)
    driver.get(link)
    temp = []
    go = True

    while go == True:
        time.sleep(2)
        html = driver.page_source
        response_obj = Selector(text=html)
        links = response_obj.xpath(
            "//div[contains(@data-qa, 'posting ')]"
        )

        for link in links:
            temp.append({'url': 'https://www.imovelweb.com.br{}'.format(link.xpath("./@data-to-posting").get())})

        try:
            _next = driver.find_element_by_xpath(
                f'//a[contains(@aria-label, "Siguiente")]'
            )
            print('Page Scraped')
            _next.click()
            go = True
        except:
            print('End of Scraping')
            go = False
    return temp

