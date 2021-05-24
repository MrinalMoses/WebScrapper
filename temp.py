import os
import requests
import sys

def scrape_html():
    for year in range(2012,2019):
        for month in range(1,13):
            if(month<10):
                url='https://en.tutiempo.net/climate/0{}-{}/ws-421820.html'.format(month,year)
            else:
                url='https://en.tutiempo.net/climate/{}-{}/ws-421820.html'.format(month,year)
            texts=requests.get(url)
            text_utf=texts.text.encode('utf=8')    
            if not os.path.exists('/Desktop/New folder/data/html/{}'.format(year)):
                os.makedirs("/Desktop/New folder/data/html/{}".format(year))
            with open("/Desktop/New folder/data/html/{}/{}.html".format(year,month),"wb") as output:
                output.write(text_utf)
        sys.stdout.flush()
        
scrape_html()