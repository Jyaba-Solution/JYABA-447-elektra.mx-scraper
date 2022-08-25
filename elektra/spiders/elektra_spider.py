import scrapy
import datetime
import json
import re

'''
Date == Script run date  (DD/MM/YYYY) 

Canal == “Sanborns” 

Category == category 

Subcategory = Subcategory 

Subcategory2= Subcategory2 

Subcategory3=  BLANK 

Marca == Brand 

Modelo == Model 

SKU ==SKU 

UPC == UPC 

Item == Item 

Item Characteristics == Item Characteristics 

URL SKU == URL 

Image == image 

Price == Price 

Sale Price == Sale Price 

Shipment Cost == BLANK 

Sales Flag == Sales Flag 

Store ID == BLANK 

Store Name = BLANK 

Store Address = BLANK 

Stock == Stock 

UPC WM == UPC[0:-1].zifll(16) 

Final Price == min (price, sale price). 
'''




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
        item['Sale Price'] = json_file.get('offers',{}).get('price')
        item['Price'] = re.findall('"lowPrice":(.*?),',response.text)[0] if re.findall('"lowPrice":(.*?),', response.text) else ''

        item['Shipment Cost'] = ''
        item['Sales Flag'] = ''
        item['Store ID'] = ''
        item['Store Name'] = ''
        item['Store Address'] = ''
        item['Stock'] = json_file.get('offers',{}).get('offers',{})[0].get('availability') if json_file.get('offers',{}).get('offers',{})[0].get('availability') else ''
        item['UPC WM'] = item['UPC'][0:-1].zfill(16)
        item['Final Price'] = ''
        yield item

        
        


        


        
