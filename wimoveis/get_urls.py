from scrapy.selector import Selector
import time
import undetected_chromedriver as uc
import re

def get_urls_wimoveis(link):
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument('--headless')
    driver = uc.Chrome(options=options)
    driver.get(link)
    html_temp = driver.page_source
    response_obj_temp = Selector(text=html_temp)

    listing_size = response_obj_temp.xpath(
        "//h1[contains(@class, 'list-result-title')]/text()"
    ).get()
    listing_size = float(re.sub("[^0-9]", "", listing_size))

    i_max = (listing_size/21).__round__()
    i = 0
    temp = []
    go = True

    while i < i_max and go == True:
        print(i)
        i += 1
        time.sleep(6)
        try:
            html = driver.page_source
            response_obj = Selector(text=html)
            links = response_obj.xpath(
                "//div[contains(@data-qa, 'posting ')]"
            )
            print('Page Scraped {}'.format(i))
            for link in links:
                temp.append({'url': 'https://www.wimoveis.com.br{}'.format(link.xpath("./@data-to-posting").get())})
        except:
            pass
        try:
            _next = driver.find_element_by_xpath(
                f'//a[contains(@aria-label, "Siguiente")]'
            )
            _next.click()
            go = True
        except:
            try:
                time.sleep(30)
                print("Try it one more time")
                _next = driver.find_element_by_xpath(
                    f'//a[contains(@aria-label, "Siguiente")]'
                )
                _next.click()
                go = True
            except:
                print('End of Scraping')
                go = False
    return temp


