# encoding: UTF-8

from bs4 import BeautifulSoup
import requests

url = "http://tieba.baidu.com/f?kw=erlang&ie=utf-8&pn="

beginpage = 0
endpage = 5

class Spider:

	def __init__(self, url):
		self.url = url

	def spider(self, page):
		data = requests.get(self.url+str(page)).content
		soup = BeautifulSoup(data, "html.parser")
		# soup.find('div', attrs = {'class': "threadlist_title pull_left j_th_tit "}).find('a').get_text()
		for li in soup.find_all('div', attrs = {'class': "threadlist_title pull_left j_th_tit "}):
		 	print li.find('a').get_text()

sp = Spider(url)
sp.spider(0)