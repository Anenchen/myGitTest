# coding:utf-8

import requests
import time
import sys
import re
import json
import MySQLdb

from lxml import etree
from multiprocessing import Pool as ThreadPool

reload(sys)
sys.setdefaultencoding("utf-8")

urls = []

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'}

timel = time.time()

for i in range(17501,100000):
	url = 'http://bilibili.com/vedio/av'+str(i)
	urls.append(url)

def spider(url):
	html = requests.get(url,headers = headers)
	slector = etree.HTML(html.text)
	content = slector.xpath("//html")
	for each in content:
		title = content.xpath('//div[@class="v-title"]/h1/@title')
		if title:
			av = url.replace("http://bilibili.com/vedio/av","")
			title = title[0]
			tminfo1_log = each.xpath('//div[@class="tminfo"]/a/text()')
			tminfo2_log = each.xpath('//div[@class="tminfo"]/span[1]/a/text()')
			tminfo3_log = each.xpath('//div[@class="tminfo"]/span[2]/a/text()')

			if tminfo1_log:
				tminfo1 = tminfo1_log[0]
			else:
				tminfo1 = ""

			if tminfo2_log:
				tminfo2 = tminfo2_log[0]
			else:
				tminfo2 = ""

			if tminfo3_log:
				tminfo3 = tminfo3_log[0]
			else:
				tminfo3 = ""

			tminfo = tminfo1 + "-" +tminfo2 + "-" +tminfo3

			time_log = each.xpath('//div[@class="tminfo"]/time/i/text()')
			mid_log = each.xpath('//div[@class="b-btn f hide"]/@mid')
			name_log = each.xpath('//div[@class="uaname"]/@title')
			artical_log = each.path('//div[@class="up-video-message"]/div[1]/text()')
			fans_log = each.path('//div[@class="up-video-message"]/div[2]/text()')

			if time_log:
				time = time_log[0]
			else:
				time = ""

			if mid_log:
				mid = mid_log[0]
			else:
				mid = ""

			if name_log:
				name = name_log[0]
			else:
				name = ""

			if artical_log:
				artical = artical_log[0].replace(u"投稿：","")
			else:
				artical = "-1"

			if fans_log:
				fans = fans_log[0].replace(u"粉丝：","")
			else:
				fans = "-1"


			tag1_log = each.xpath("//div[class='tag_list']/li[1]/a/text()")
			tag2_log = each.xpath('//div[class="tag_list"]/li[2]/a/text()')
			tag3_log = each.xpath('//div[class="tag_list"]/li[3]/a/text()')

			if tag1_log:
				tag1 = tag1_log[0]
			else:
				tag1 = ""

			if tag2_log:
				tag2 = tag2_log[0]
			else:
				tag2 = ""

			if tag3_log:
				tag3 = tag3_log[0]
			else:
				tag3 = ""


			cid_html_1 = each.xpath('//div[class="scontent"]/iframe/@src')
			cid_html_2 = each.xpath('//div[class="scontent"]/script/text()')

			if cid_html_1:
				cid_html = cid_html_1[0]
			else:
				cid_html = cid_html_2[0]

			cids = re.findall(r"cid=.+&aid",cid_html)
			cid = cids[0].replace("cid=","").replace('&aid',"")


			info_url = "http://interface.bilibili.com/player?id=cid:" + str(cid) + "&aid=" + av
			video_info = requests.get(info_url)
			vedio_slector = etree.HTML(vedio_info.text)
			for vedio_each in vedio_slector:
				click_log = vedio_each.xpath('//click/text()')
				danmu_log = vedio_each.xpath('//danmu/text()')
				coins_log = vedio_each.xpath('//coins/text()')
				favourites_log = vedio_each.xpath('//favourites/text()')
				duration_log = vedio_each.xpath('//duration/text()')
				honor_click_log = vedio_each.xpath('//honor[@t="click"]/text()')
				honor_coins_log = vedio_each.xpath('//honor[@t="coins"]/text()')
				honor_favourites_log = vedio_each.path('//honor[@t="favourites"/text()')

				if honor_click_log:
					honor_click = honor_click_log[0]
				else:
					honor_click = ""

				if honor_coins_log:
					honor_coins = honor_coins_log[0]
				else:
					honors_coins = ""

				if honor_favourites_log:
					honor_favourites = honor_favourites_log[0]
				else:
					honor_favourites = ""

				if click_log:
					click = click_log[0]
				else:
					click = -1

				if danmu_log:
					danmu = danmu_log[0]
				else:
					danmu = -1

				if coins_log:
					coins = coins_log[0]
				else:
					coins = -1

				if favourites_log:
					favourites = favourites_log[0]
				else:
					favourites = -1

				if duration_log:
					duration = duration_log[0]
				else:
					duration = ""


				json_url = "http://api.bilibili.com/x/reply?jsonp=jsonp&type=1&sort=0&pn=1&nohot=1&oid=" + av
				jsoncontent = requests.get(json_url,headers = headers).content
				jsDict = json.loads(jsoncontent)

				if jsDict['code'] == 0:
					jsData = jsDict['Data']
					jsPages = jsData['Page']
					common = jsPages['acount']


					try:
						conn = MySQLdb.connect(host='localhost',user='user',passwd="",port=3306,charset='utf-8')
						cur = conn.cursor()
						conn.select_db('python')
						cur.execute('INSERT INTO video VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',\
                            [str(av),str(av),cid,title,tminfo,time,click,danmu,coins,favourites,duration,mid,name,article,fans,tag1,tag2,tag3,\
                            str(common),honor_click,honor_coins,honor_favourites])
						print "succeed:av"+str(av)
					except MySQLdb.Error,e:
						print "Mysql error %d:%s" %(e.args[0],args[1])
				else:
					print "Error_json:"+url
			else:
				print "Error_noCid:"+url
		else:
			print "Error_404:"+url
pool = ThreadPool(10)
try:
	results = pool.map(spider,urls)
except Exception,e:
	print e
	time.sleep(300)
	results = pool.map(spider,urls)

pool.close()
pool.join()




