# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 14:25:36 2017

@author: Simran
"""

from urllib.request import Request,urlopen
from bs4 import BeautifulSoup as bs
text_file=open("ScrapedLyrics.txt","w",encoding="utf-8")

def link_to_pages(page):
    u=urlopen(Request(page,headers={"User-Agent":'Mozilla'}))
    soup=bs(u,'lxml')
    href=soup.find('div',{"id":"entry-listing"})
    hrefs=href.find_all('h2',class_='entry-title')
    for x in hrefs:
        link=x.find_all('a')
        for l in link:
            get_text(l.get('href'))
            text_file.write("\n#####################################\n")
            
def get_text(links):
    u2=urlopen(Request(links,headers={"User-Agent":'Mozilla'}))
    soup=bs(u2,'lxml')
    cont=soup.find('div',class_="lyric-content")
    text=cont.find_all('p')
    for y in text:
        text_file.write(y.text)
        text_file.write('\n')


link_to_pages("http://www.lyricsted.com/")
print(1)

for x in range(2,51):
    pg="http://www.lyricsted.com/page/"+str(x)+"/" 
    link_to_pages(pg)
    print('Page ' + x + 'scraped!')

text_file.close()