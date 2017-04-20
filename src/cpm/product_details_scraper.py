from lxml import html  
import csv,os,json
import requests
import urllib
from exceptions import ValueError
from time import sleep
from urlparse import urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
from pprint import pprint
 
def AmzonParser(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
    page = requests.get(url,headers=headers)
    while True:
        sleep(3)
        try:
            doc = html.fromstring(page.content)

            XPATH_NAME = '//h1[@id="title"]//text()'
            XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
            XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
            XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
            XPATH_AVAILABILITY = '//div[@id="availability"]//text()'
 
            RAW_NAME = doc.xpath(XPATH_NAME)
            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
            RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
            RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
            RAW_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)
            CATEGORY_array=[]
            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
            print 'before category'
            CATEGORY = '>'.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
            print 'after category'
            ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
            AVAILABILITY = ''.join(RAW_AVAILABILITY).strip() if RAW_AVAILABILITY else None
            
            if not ORIGINAL_PRICE:
                ORIGINAL_PRICE = SALE_PRICE
 
            if page.status_code!=200:
                raise ValueError('captha')
            CATEGORY_array = CATEGORY.split(">")
            print CATEGORY
            if len(CATEGORY_array)>=2:
                CATEGORY = CATEGORY_array[0]
                SUBCATEGORY = CATEGORY_array[1]
            else:
                CATEGORY = CATEGORY
                SUBCATEGORY = CATEGORY
            data = {
                    'ITEM':NAME,
                    'SALE_PRICE':SALE_PRICE,
                    'CATEGORY':CATEGORY,
                    'SUBCATEGORY': SUBCATEGORY,
                    'ORIGINAL_PRICE':ORIGINAL_PRICE,
                    'AVAILABILITY':AVAILABILITY,
                    'URL':url,
                    'VENDOR':'Amazon'
                    }
            print 'data obtained'
            return data
        except Exception as e:
            print e
def EbayParser(url):
    print('here in ebay')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
    page = requests.get(url,headers=headers)
    while True:
        sleep(3)
        try:
            doc = html.fromstring(page.content)

            XPATH_NAME = '//title[1]/text()'
            XPATH_SALE_PRICE = '//span[contains(@id,"mm-saleDscPrc") or contains(@id,"saleprice")]/text()'
            XPATH_ORIGINAL_PRICE = '//span[contains(@id,"mm-saleOrgPrc") or contains(text(),"M.R.P") or contains(@id,"prcIsum")]/text()'
            XPATH_CATEGORY = '//span[@itemprop="name"]//text()'
            XPATH_AVAILABILITY = '//span[@id="qtySubTxt"]//text()'
 
            RAW_NAME = doc.xpath(XPATH_NAME)
            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
            RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
            RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
            RAW_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)
            CATEGORY_array=[]
            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
            CATEGORY = '>'.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
            ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
            AVAILABILITY = ''.join(RAW_AVAILABILITY).strip() if RAW_AVAILABILITY else None
            
            if not ORIGINAL_PRICE:
                ORIGINAL_PRICE = SALE_PRICE
 
            if page.status_code!=200:
                raise ValueError('captha')
            CATEGORY_array = CATEGORY.split(">")
            print CATEGORY
            print CATEGORY_array
            if len(CATEGORY_array)>=2:
                CATEGORY = CATEGORY_array[0]
                SUBCATEGORY = CATEGORY_array[1]
            else:
                
                CATEGORY = CATEGORY
                SUBCATEGORY = CATEGORY
            
            data = {
                    'ITEM':NAME,
                    'SALE_PRICE':SALE_PRICE,
                    'CATEGORY':CATEGORY,
                    'SUBCATEGORY': SUBCATEGORY,
                    'ORIGINAL_PRICE':ORIGINAL_PRICE,
                    'AVAILABILITY':AVAILABILITY,
                    'URL':url,
                    'VENDOR':'Ebay'
                    }
 
            return data
        except Exception as e:
            print e 
def MendelParser(url):
    print('here in mendel')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
    page = requests.get(url,headers=headers)
    while True:
        sleep(3)
        try:
            doc = html.fromstring(page.content)

            XPATH_NAME = '//div[@class="product-name"]//text()'
            XPATH_SALE_PRICE = '(//span[contains(@id,"product-price") or contains(@id,"saleprice")])[1]/text()'
            XPATH_ORIGINAL_PRICE = '(//span[contains(@class,"regular-price") or contains(text(),"M.R.P") or contains(@id,"old-price")])[1]/text()'
            XPATH_CATEGORY = '//a[@title=""]//text()'
            XPATH_AVAILABILITY = '//p[@class="availability in-stock"]//text()'
 
            RAW_NAME = doc.xpath(XPATH_NAME)
            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
            RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
            RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
            RAW_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)
            CATEGORY_array=[]
            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
            CATEGORY = '>'.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
            ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
            AVAILABILITY = ''.join(RAW_AVAILABILITY).strip() if RAW_AVAILABILITY else None
            
            if not ORIGINAL_PRICE:
                ORIGINAL_PRICE = SALE_PRICE

            if page.status_code!=200:
                raise ValueError('captha')
            CATEGORY_array = CATEGORY.split(">")
            if len(CATEGORY_array)>=2:
                CATEGORY = CATEGORY_array[0]
                SUBCATEGORY = CATEGORY_array[1]
            else:
                CATEGORY = CATEGORY
                SUBCATEGORY = CATEGORY
            data = {
                    'ITEM':NAME,
                    'SALE_PRICE':SALE_PRICE,
                    'CATEGORY':CATEGORY,
                    'SUBCATEGORY': SUBCATEGORY,
                    'ORIGINAL_PRICE':ORIGINAL_PRICE,
                    'AVAILABILITY':AVAILABILITY,
                    'URL':url,
                    'VENDOR':'Make Mendel',
                    }
 
            return data
        except Exception as e:
            print e 

def ReadAsin(url):
    extracted_data = []
    check_domain = urlparse(url).hostname
    print check_domain
    if 'amazon' in check_domain:
       extracted_data.append(AmzonParser(url))
       #f=open('data.json','w')
       #json.dump(extracted_data,f,indent=4)
    elif 'ebay' in check_domain:
       extracted_data.append(EbayParser(url))
       #f=open('data.json','w')
       #json.dump(extracted_data,f,indent=4)
    elif 'makemendel' in check_domain:
       extracted_data.append(MendelParser(url))
       #f=open('data.json','w')
       #json.dump(extracted_data,f,indent=4)
    return extracted_data
 
 
if __name__ == "__main__":
  ReadAsin('http://www.3dprintronics.com/3d-printer-filaments#!/Red-PLA-1-75-Filament/p/27910566/category=6988017')
  #ReadAsin('https://www.amazon.com/dp/B01L0PS2IA?psc=1&smid=A3JC02LVN0LU5G')