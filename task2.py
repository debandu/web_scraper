import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

URLS = pd.read_csv('data.csv')
headerAgent = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
data=[]

for url in URLS['Product URL']:
    try:
        row=[]
        response=requests.get(url,headers=headerAgent)
        soup=BeautifulSoup(response.text)
        cont=soup.find('div',class_="a-container")
        name=cont.find('span',class_='a-size-large product-title-word-break').text
        asin=url.split('/')[-1]
        text='Manufacturer'
        try:
            manu=cont.find("table",class_='a-keyvalue prodDetTable')
            Manufacturer = manu.find(lambda tag: tag.name == "tr" and text in tag.text)
            company=Manufacturer.find('td').text.split(',')[0]

        except Exception as e:
            manu=cont.find("ul",class_='a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list')
            Manufacturer = manu.find(lambda tag: tag.name == "li" and text in tag.text)
            company=Manufacturer.find('span',class_='').text.split(',')[0]
        
        pro_desc=cont.find('ul',class_='a-unordered-list a-vertical a-spacing-mini')
        pro_desc=pro_desc.find_all('span',class_='a-list-item')
        product_description=[]
        for pro in pro_desc:
            pro=pro.text
            product_description.append(pro)
        product_description='\n'.join(product_description)
        company=company.replace('\u200e', '')
        company = re.sub(' +', ' ', company)
        row=[name,product_description,asin,company]
        data.append(row)
    except Exception as e:
        print(e)

df=pd.DataFrame(data,columns=['Product Name','Product Description','Product ASIN','Product Manufacturer'])
df.to_csv('product_details.csv')