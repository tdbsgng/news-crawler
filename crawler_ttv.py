import time
import random
import requests
from bs4 import BeautifulSoup   
from datetime import datetime


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
}
count=1
flag=1
while flag:
    f=open(f'ttv{count}.txt','a')
    for page in range((count-1)*100,count*100):
        if page==1065:
            flag=0
            break
        try:
            res = requests.get(f'https://news.ttv.com.tw/realtime/{page+1}')
            soup=BeautifulSoup(res.text,'lxml')
            list=soup.select('article div ul li a')
            for i in list:
                dict={}
                res=requests.get(i['href'])
                soup=BeautifulSoup(res.text,'lxml')
                dict['title']=soup.select('.mb-ht-hf')[0].text.strip()
                dict['time']=soup.select('.date.time')[0].text.strip()
                dict['summerization']=soup.select('#newscontent p')[0].text.strip()
                dict['article']=''
                for num in range(1,len(soup.select('#newscontent p'))):
                    dict['article']+=soup.select('#newscontent p')[num].text.strip()
                
                print(f'{page+1}\n')
                print(dict)
                try:
                    f.write(str(dict)+'\n')
                except Exception as e:
                    print(e,'file writing error')
        except Exception as e:
            print(e,'requests error')
    f.close()
    count+=1
    



