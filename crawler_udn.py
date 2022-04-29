import time
import random
import requests
from bs4 import BeautifulSoup   
from datetime import datetime
import re
import datetime
import time
import calendar

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
}
count=353250
def get_content(href):
    #time.sleep(random.uniform(1, 2))
    global count
    dict={}
    try:
        res=requests.get(href,headers=HEADERS)
        soup=BeautifulSoup(res.text.encode('utf8'),'html.parser')
    except:
        return None
    try:
        dict['title']=soup.select('h1.article-content__title')[0].text.strip()
        dict['time']=soup.select('time.article-content__time')[0].text.strip()
        dict['type']=soup.select('.breadcrumb-items')[1].text.strip()
        content_list=[]
        for i in range(len(soup.select('.article-content__editor p'))):
            input=soup.select('.article-content__editor p')[i].text.strip()
            input=re.sub(r'\\u[0-9]{4}','',input)
            input=re.sub(r'\\x[A-Za-z0-9]{2}','',input)
            ##print(input)
            if input !='':
                if input[-1] not in ['，','。','!','?','？','！','」']:
                    continue
                for i in ["圖/","/圖","影/","/攝影","文/","文/","記者/","/記者"]:
                    if i in input:
                        continue
                if '延伸閱讀' not in input or content_list==[]:
                    content_list.append(input)
        dict['summerization']= content_list[0]
        dict['article']=''
        for num in range(1,len(content_list)):
            dict['article']+= content_list[num]
        if dict['article']=='':
            return None
        print(dict)
        with open(f'udn{int(count/20000)+1}.txt','a',encoding='utf-8') as f:
            f.write(str(dict)+'\n')
        count+=1
        return dict
    except Exception as e:
        print('error\n',e,'\n')
        return None

date=datetime.date(2020,7,1)
start_date=date
while date != datetime.date(2020,6,30):
    flag=1
    if date == start_date:
        page=1
    else:
        page=1
    new_list=[]
    while flag:
        url=f'https://udn.com/api/more?page={page}&date={date.year}{date.month:02d}{date.day:02d}=&type=archive&year={date.year}&month={date.month:02d}&day={date.day:02d}&totalRecNo=10000'
        
        try:
            res= requests.get(url,headers=HEADERS)
            new_data=res.json()
            new_list.extend(new_data['lists'])
        except Exception as e:
            print('error!\n',e,'\n')
            page=0
            break
        for i in new_list:
            url='https://udn.com'
            L=i['titleLink'].split("\\")
            for l in L:
                url+=l
            news=get_content(url)
            print(f'date: {str(date)} page: {page} count:{count}')  
        if len(new_list)<20:
            page=0
            break
        page+=1
        time.sleep(random.uniform(1, 2))
        new_list=[]       
    date=date-datetime.timedelta(days=1)
    
        

