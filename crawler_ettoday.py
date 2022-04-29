import requests
from bs4 import BeautifulSoup  
import re

type_dict={'10':'體育','20':'3c','30':'時尚','24':'遊戲','5':'生活','1':'政治','2':'國際','17':'財經','6':'社會','9':'影劇'}

def writeTotxt(reports, i):
    with open(f'{type_dict[str(i)]}.txt', 'w',encoding='utf-8') as f:
        for report in reports:
          f.write(str(report)+'\n')

def get_content(u):
  article=''
  summa=''
  
  i=1
  try:
    res = requests.get(u)
    soup = BeautifulSoup(res.content, "html.parser")
  except:
    return article, summa
  try:
    soup = soup.find("div", class_="story")
    for j,a in enumerate(soup.find_all("p")):
      if a.text!='':
        if a.text.strip()[-1] not in ['，','。','!','?','？','！','」']:
          continue
        #print(a.text)
        #print(j)
        if re.sub("記者.*報導",'',a.text) == '':
          continue
        if re.sub("政治中心.*報導",'',a.text) == '':
          continue
        if re.sub("新聞節目.*報導",'',a.text) == '':
          continue
        if re.sub(r'▲', '', a.text) != a.text:
          #print('delete')
          continue
        if re.sub(r'▼', '', a.text) != a.text:
          #print('delete')
          continue
        ##到第五個para都還沒找到第一段，就不要此篇了
        if j>8 and i ==1:
          break
        # 如果前三段出現記者、圖或是小於20字就不要爬進去
        ## i 判斷是否還在找summa ，i = 1 找 summa
        if i == 1 and len(a.text) >30:
          summa = a.text
          summa = re.sub(r'\（.*\）','',summa)
          summa = re.sub(r'►', '', summa)
          summa = re.sub(r'▼▼', '', summa)
          summa = re.sub(r'[\r\n\t\xa0\u3000]', '', summa)
          if re.sub(r'【.*新聞】', '',summa) != summa:
            break
          ##不要第一段，就從這裡拔掉就好
          #article += summa
          #print(f'summma,{summa}')
          i = 0
          continue
        if i==0:
          para = a.text
          para = re.sub(r'[\r\n\t\xa0\u3000]', '', para)
          para = re.sub(r'\（.*\）','',para)
          if '►' in para or '▼▼' in para :
            continue 
          ##通常是在文末，更多新聞，所以就直接停止
          if re.sub(r'【.*新聞】', '',para) != para:
            break
          if "★" in para:
            break

          if para!= None:
            article += para
  except:
    pass
  
  return article, summa
for tt in [1, 17, 2, 6, 9, 10, 20, 30, 24, 5]:
    # 月份 n -> 1-12
    outputs=[]
    for n in range(1,13):
      # 日期 n2 -> 4,7,10,13,16,19,21,24
        for n2 in [4,7,10,13,16,19,21,24]:
          # 先建 dict
            
            output=dict()
            output['article'] = ''
            output['summarization'] = ''
            output['title'] = ''
            output['type']=str(type_dict[str(tt)])

            # 建構網址 年分在這裡調
            u = "https://www.ettoday.net/news/news-list-2021-"+str(n)+"-"+str(n2)+"-"+str(tt)+".htm"
            res = requests.get(u)
            soup = BeautifulSoup(res.content, "html.parser")
            soup = soup.find("div", class_="part_list_2")
            domian = "https://www.ettoday.net"
            for a in soup.find_all("h3"):
              tit = a.a.text
              tit = re.sub(r'[\r\n\t\xa0\u3000]', '', tit)
              output['title'] = tit

              
              (output['article'], output['summarization']) = get_content(domian+a.a['href'])
              if output['article']=='' or output['summarization']=='' or output['title']=='':
                continue
              print(domian+a.a['href'])
              print(output)
              outputs.append(str(output))
              
            #print(outputs)
            #print(len(outputs))
            # 依 類別-月份-日期 寫一個txt
    writeTotxt(outputs, tt)
              