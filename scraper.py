# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import FormRequest
from scrapy.selector import Selector
import json

items_per_page = 10
# AJAX data scraper
class AjaxScraper(scrapy.Spider):
    # scraper/spider name
    name = 'ajax'
    
    # base URL
    base_url = 'https://www.gelbeseiten.de/ajaxsuche'
    
    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    # custom settings
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'restaurants.csv'
    }
    
    # form data payload
    params = {
        'umkreis': '-1',
        'WAS': 'restaurants',
        'WO': 'berlin',
        'position': '0',
        'anzahl': str(items_per_page),
        'sortierung': 'relevanz'
    }
    
    # crawler's entry
    def start_requests(self):
        # loop over "page" range
        for page in range(0, 400):
            # calculate next page's starting data index
            self.params['position'] = str(page * items_per_page)
            
            # mimic AJAX call
            yield FormRequest(
                url=self.base_url,
                headers=self.headers,
                formdata=self.params,
                callback=self.parse
            )
    
    # parse response
    def parse(self, response):
        jsonresponse = json.loads(response.text)
        # write HTML response to local file
        with open('res.html', 'w') as f:
            f.write(jsonresponse["html"])
        data = json.loads(response.text)
        selector = scrapy.Selector(text=data['html'], type="html")
        
        '''
        # local HTML content
        content = ''
        
        # load local HTML file to extract data
        with open('res.html', 'r') as f:
            for line in f.read():
                content += line
        
        # init scrapy selector
        response = Selector(text=content)
        '''    
        raw_entry = selector.css('article').xpath('@data-lazyloaddata').getall()
        
        for s in raw_entry:
            j1 = json.loads(s)
            email = ""
            name = j1["name"]
            postalcode = j1["adresseKompakt"]["plzOrt"]
            address = j1["adresseKompakt"]["strasseHausnummer"]
            phone = j1["adresseKompakt"]["telefonnummer"]
            branche = j1["branche"]
            
            for link in j1['trefferButtonListList']['trefferButtonListList'][0]:
                if link["gcLink"]["text"] == 'E-Mail':
                    email = link["gcLink"]["href"].split(":")[1].split("?")[0]
            # s.replace("//", "")
            yield{'Name':name,'Address':address,'PLZ':postalcode,'Tel':phone, 'E-Mail':email, 'Branche': branche }
        
# main driver
if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(AjaxScraper)   
    process.start()
    
    