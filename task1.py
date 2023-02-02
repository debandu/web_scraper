import requests
from bs4 import BeautifulSoup
import pandas as pd

data=[]

for i in range(1,21):
    url=f"https://www.amazon.in/s?k=bags&page={i}"
    try:
        response=requests.get(url)
        while response.status_code!=200:
            response=requests.get(url)
        
        if response.status_code==200:
            soup=BeautifulSoup(response.text)
            cont=soup.find('span',class_="rush-component s-latency-cf-section")
            articles=cont.find_all('div',class_='a-section a-spacing-small a-spacing-top-small')
            for article in articles:
                row=[]
                a=article.find('a')
                pro_url=a.attrs['href']
                pro_url="https://www.amazon.in"+str(pro_url)
                pro_name=article.find('span').text
                pro_rating=article.find('span',class_='a-icon-alt').text.split()[0]
                pro_review=article.find('span',class_='a-size-base s-underline-text').text[1:-1]
                pro_price=article.find('span',class_='a-offscreen').text[1:]
                row=[pro_name,pro_price,pro_rating,pro_review,pro_url]
                data.append(row)
    except Exception as e:
        print(e)
df=pd.DataFrame(data,columns=['Product Name','Product Price','Product Rating','Product Review','Product URL'])
df.to_csv('data.csv')
