from __future__ import print_function
from bs4 import BeautifulSoup
import time
import datetime
import os
import csv
import requests
import re
from collections import defaultdict

## write to csv file
def save_to_csv(data, target='announcement/' + datetime.datetime.now().strftime("%Y%m%d") + '.csv'):
  keys = data[0].keys()
  with open(target, 'wb') as csv_file:
    dict_writer = csv.DictWriter(csv_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(data)


## return asx code only

def get_web_content(json_file='announcement/' + datetime.datetime.now().strftime("%Y%m%d")+".json"):

  data = []
  url = "https://www.asx.com.au/asx/statistics/todayAnns.do"
  pre_fix = "https://www.asx.com.au"
  
  page = requests.get(url)
  contents = page.content

  ## find report table
  
  soup=BeautifulSoup(contents, "lxml")
  table = soup.find("table")
  
  if table:
    
    rows = table.find_all('tr')

    for row in rows:
      link = ''
      priceses = False
      d = defaultdict()
      cols = row.find_all('td')

      ## price sens check
      pricesens = True if row.find_all('td', class_="pricesens") else False
      d['pricesens'] = pricesens
      
      
      for ele in cols:
        ## pdf link
        a_tag = ele.find_all('a', href=True)
        if a_tag:          
          d['link'] = pre_fix + a_tag[0]['href']

        ## price sens
        txt = re.sub(r'[\n\r\t]', r' ', ele.text)
        txt = ' '.join(txt.split())

        ## assign value
        if len(txt)==3:
          d['code']=txt
        elif txt.endswith('M'):
          d['time'] = txt
        else:
          if txt:
            txts = txt.split()
            d['notices'] = ' '.join(txts[:-3])
            d['pages'] = txts[-3]
            d['file_size'] = txts[-1]    
      
      if 'code' in d.keys():
        data.append(d)
  return data

if __name__ == "__main__":

  start_time = time.time()
  data = get_web_content()
  # save to csv file
  save_to_csv(data)
  print("download duration: {:.2f} sec".format(time.time()-start_time))
  
