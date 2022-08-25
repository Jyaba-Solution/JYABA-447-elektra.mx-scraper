import scrapy
import datetime
import json
import re




class ElektraSpider(scrapy.spiders.SitemapSpider):
    name = "elektra"
    sitemap_urls = ['https://www.elektra.mx/sitemap.xml']
    sitemap_rules = [('/p', 'parse')]


    def parse(self, response):
        ans = response.xpath("//script[@type='application/ld+json']/text()").extract_first()
        try:
            json_file = json.loads(ans)
        except:
            with open("error.txt", "a") as f:
                f.write(response.url + "\n")
            return
        item = dict()
        item['Date'] = datetime.datetime.now().strftime("%d/%m/%Y")
        item['Canal'] = 'Elektra'
        breadcrumb_list = response.xpath('//a[contains(@class,"vtex-breadcrumb")]//text()').extract()
        breadcrumb_json = {x:y for x,y in enumerate(breadcrumb_list)}
        item['Category'] = breadcrumb_json.get(0)
        item['Subcategory'] = breadcrumb_json.get(1)
        item['Subcategory2'] = breadcrumb_json.get(2)
        item['Subcategory3'] = breadcrumb_json.get(3)
        brand_name =  response.xpath("//meta[contains(@property,'brand')]/@content").extract_first()
        item['Marca'] = brand_name if brand_name else ''
        item['Modelo'] = response.xpath("//span[contains(@class,'modelo')]/text()").extract_first()
        item['SKU'] =  response.xpath("//meta[contains(@property,'sku')]/@content").extract_first()
        item['UPC'] = re.findall('"ean":"(.*?)"',response.text)[0] if re.findall('"ean":"(.*?)"',response.text) else ''
        item['Item'] = json_file.get('name')
        item['Item Characteristics'] = json_file.get('description')
        item['URL SKU'] = response.url
        item['Image'] = json_file.get('image')
        prices = re.findall('"lowPrice":(.*?),', response.text)
        if prices:
            all_prices = list(set([float(x) for x in prices]))
            if len(all_prices) == 1:
                price = all_prices[0]
                sale_price = ''
            else:
                sale_price = min(all_prices)
                price = max(all_prices)


        item['Price'] = price
        item['Sales Price'] = sale_price
        item['Shipment Cost'] = ''
        item['Sales Flag'] = response.xpath("//span[contains(@class,'savingsPercentage')]/text()").extract_first()
        item['Store ID'] = ''
        item['Store Name'] = ''
        item['Store Address'] = ''
        item['Stock'] = json_file.get('offers',{}).get('offers',{})[0].get('availability') if json_file.get('offers',{}).get('offers',{})[0].get('availability') else ''
        item['UPC WM'] = item['UPC'][0:-1].zfill(16)
        item['Final Price'] = min(all_prices)
        yield item

        
        


        


        
