from scrapy.selector import Selector
import time
import json as json
import undetected_chromedriver as uc
import re

def get_urls_vivareal(link):
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument('--headless')
    driver = uc.Chrome(options=options)
    driver.get(link)
    i = 0
    temp = []
    go = True

    while go == True:
        print(i)
        i += 1
        time.sleep(2)
        html = driver.page_source
        response_obj = Selector(text=html)

        links = response_obj.xpath(
            "//div[contains(@data-type,'property')]//a[contains(@class, 'property-card__labels-container js-main')]"
         )
        print('Page Scraped {}'.format(i))
        for link in links:
            temp.append({'url': 'https://www.vivareal.com.br{}'.format(link.xpath("./@href").get())})

        time.sleep(2)
        try:
            _next = driver.find_element_by_xpath(
                f"//a[contains(@title, 'Próxima página')]"
            )
            _next.click()
        except:
            print('end of scraping')
            go = False
    return temp





