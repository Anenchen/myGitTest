# coding:utf-8

import os
import sys
import urllib2
import requests
import re
from lxml import etree


def StringListSave(save_path,filename,slist):
	if not os.path.exists(save_path):
		os.makedirs(save_path)
	path = save_path + "/" + filename + ".txt"
	with open(path,"w+") as fp:
		for s in slist:
			fp.write("%s\t\t%s\n" % (s[0].encode("utf-8"),s[1].encode("utf-8")))

def Page_Info(myPage):
	myPage_Info = re.findall(r'<div class="titleBar" id=".*?"><h2>.*?</h2><div class="more"><a href=".*?>.*?</a></div></div>',myPage,re.S)
	return myPage_Info

def New_Page_Info(new_page):
	dom = etree.HTML(new_page)
	new_items = dom.xpath('//tr/td/a/text()')
	new_urls = dom.xpath('//tr/td/a/text()')
	assert len(new_items) == len(new_urls)
	return zip(new_items,new_urls)
	#new_page_Info = re.findall(r'<td class=".*?">.*?<a href="(.*?)\.html".*?>(.*?)</a></td>',new_page,re.S)
	#results = []
	#for url,item in new_page_Info:
		#results.append((item,url+".html"))
	#return results

def Spider(url):
	i = 0
	print "downloading:" + url
	#myPage = requests.get(url).content.encode('gbk')
	myPage = urllib2.urlopen(url).read()
	myPageResult = Page_Info(myPage)
	save_path = u'网易新闻抓取'
	filename = str(i) + "-" + u"新闻排行榜"
	StringListSave(save_path, filename, myPageResult)
	i +=1
	for item,url in myPageResult:
		print "downloading:" + url
		newpage = requests.get(url).content
		newPageResults = New_Page_Info(new_page)
		filename = str(i) + "_" + item
		StringListSave(save_path, filename, newPageResults)
		i +=1

if __name__ == '__main__':
	print "start"
	start_url = "http://news.163.com/rank/"
	Spider(start_url)
	print "end"