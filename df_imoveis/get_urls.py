from scrapy.selector import Selector
import time
import undetected_chromedriver as uc

def get_urls_dfimoveis(link):
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
            "//div[contains(@class, 'property js')]"
         )

        print('Page Scraped {}'.format(i))
        for link in links:
            temp.append({'url': 'https://www.dfimoveis.com.br{}'.format(link.xpath("./@data-url").get())})

        time.sleep(2)
        try:
            _next = driver.find_element_by_xpath(
                f"//a[contains(@class, 'pagination__link next')]"
            )
            _next.click()
        except:
            print('end of scraping')
            go = False
    return temp





