# -*- coding: UTF-8 -*-
import pymongo
import requests
import os
import codecs
import re
from pinyin import PinYin
from bs4 import BeautifulSoup
from pymongo import MongoClient

url = "//so.gushiwen.org/mingju/Default.aspx?p={0}&c=&t="
initials = r'[bpmfdtnlgkhjqxrzcsyw]'

class Spider:

	def __init__(self):
		self.page = 1
		self.data = []
		self.py = PinYin()
		self.py.load_word()
		self.client = MongoClient('mongodb://127.0.0.1:27017/')

	def spider(self):
		html = requests.get("http:"+url.format(self.page)).content
		soup = BeautifulSoup(html, "lxml")
		for li in soup.find('div', attrs = {'class': "main3"}).find('div', attrs = {'class': "left"}).find_all('div', attrs = {'class': "cont"}):
		  	firsta = li.find('a')
		  	content = firsta.get_text()
		  	title = firsta.find_next_sibling('a').get_text()
		  	pinyin = self.py.hanzi2pinyin(string=content[len(content) - 2])[0]
		  	if len(pinyin) > 0 and pinyin[0:2] in ['zh','ch','sh']: 
		  		index = pinyin[2:]
		  		self.data.append({'index':index, 'title':title, 'content':content}) 
		  	elif len(pinyin) > 0:
		  		index = re.sub(initials, '', pinyin[0])+pinyin[1:]
		  		self.data.append({'index':index, 'title':title, 'content':content})
		  	else:
		  		print content[len(content) - 2],'null' 
		oldpage = self.page
		for page in soup.find('div', attrs = {'class': "main3"}).find('div', attrs = {'class': "left"}).find('div', attrs = {'class': "pages"}).find_all('a'):
			if page.get_text().isdigit() and int(page.get_text()) > self.page:
				self.page += 1
				break
		if oldpage != self.page:
		 	self.spider()


	def save(self):
		self.client.gs.gsmj.insert(self.data)
		self.client.gs.gsmj.create_index('index')

sp = Spider()
sp.spider()
sp.save()
print 'success'
