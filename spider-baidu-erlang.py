# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import requests
import os
import codecs

url = "//tieba.baidu.com/f?kw=erlang&ie=utf-8&pn=0"
saveurl = "/baidu-erlang.txt"

class Spider:

	def __init__(self, url):
		self.url = url
		self.saveurl = saveurl
		self.data = []

	def spider(self):
		html = requests.get("http:"+self.url).content
		soup = BeautifulSoup(html, "lxml")
		for li in soup.find_all('div', attrs = {'class': "threadlist_title pull_left j_th_tit "}):
		 	self.data.append(li.find('a').get_text()) 
		nexturl = soup.find('div', attrs = {'class':"pagination-default clearfix"}).find('a', attrs = {'class':"next pagination-item "})
		if nexturl != None:
			self.url = nexturl.get('href')
			self.spider()


	def save(self):
		f = codecs.open(os.getcwd()+saveurl,'w+',"utf-8") 
		f.write("\n".join(self.data))  
		f.close()  


sp = Spider(url)
sp.spider()
sp.save()
