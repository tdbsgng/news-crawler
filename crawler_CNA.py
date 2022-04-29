  
import requests
from bs4 import BeautifulSoup
import time
import re
import sys
import os

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
url = "https://www.cna.com.tw/news/aipl/"#202107150041.aspx"
batchSize = 500

def dateGenerator(date):#20210715
	day = int(date[6:])+1
	month = int(date[4:6])
	year = int(date[0:4])
	#print(month in [1, 3, 5, 7, 8, 10, 12])
	if (day > 28 and month == 2) or (day > 30 and month in [4, 6, 9, 11]) or (day > 31 and month in [1, 3, 5, 7, 8, 10, 12]) :
		day = 1
		month += 1
		if month == 13:
			month = 1
			year += 1
	
	#print(f'{year:04d}{month:02d}{day:02d}')
	return f'{year:04d}{month:02d}{day:02d}'

#dateGenerator('20210715')


def parmgenerator(parm):#202107150041.aspx
	index = int(parm[8:12])+1
	return f'{parm[0:8]}{index:04d}.aspx'


def crawling(newsUrl):
	try:
		response = requests.request("GET", newsUrl, headers=HEADERS)
		raw_text = response.text.encode('utf8')
		#print(raw_text)

		soup = BeautifulSoup(raw_text, 'html.parser')
		#f = open("test.txt", "w+")
		#f.write(soup.prettify())
		#f.close()

		title = soup.find("h1")
		#print(title.string)
		tag = soup.find("div", class_ = "paragraph")
		type=soup.select('.breadcrumb a')[1].text.strip()

		articles = tag.find_all("p")
		summarization = re.sub(r'\W.+電\W||\W.+導\W','',articles[0].string)
		article = ""
		for i in articles:
			article += re.sub(r'\W.+電\W||\W編.+\d+||\W.+導\W||\W譯.+\d+','',i.string)
		if summarization==article:
			return None
		#print(summarization)
		#print(article)
		#while article[-1] not in ['，','。','!','?','？','！','」']:
			#article=article[:-1]
		dic={"summarization": summarization, "article": article, "title": title.string,"type":type}
		print(dic)
		return str(dic)+'\n'
	except Exception as e:
		#sys.stderr.write(str(e)+"\n")
		return None
date = '20210102'
count=0
while True:
	if count==150000:
		break
	if date=='20210928':
		date='20180731'
	if f'CNA_News_{date}.txt' in os.listdir():
		with open(f'CNA_News_{date}.txt', 'r',encoding='utf-8') as fp:
			if len(fp.readlines())>100:
				date = dateGenerator(date)
				continue
	parm = date+'0001.aspx'
	batchText = ''
	for i in range(batchSize):		
		parm = parmgenerator(parm)
		print(date,'    ',parm[8:12])
		newsUrl = url + parm
		#print(newsUrl)
		text = crawling(newsUrl)
		if text != None:
			batchText += text
			count+=1
	with open(f'CNA_News_{date}.txt', 'a+',encoding='utf-8') as fp:
		fp.write(batchText)
	date = dateGenerator(date)