# coding:utf-8

from bs4 import BeautifulSoup
import requests
import time

def captcha(captcha_data):
	with open ("captcha.jpg","wb") as f:
		f.write(captcha_data)
	text = raw_input("qingshuruyanzhengma:")
	return text

def zhihuLogin():
	#构建一个session对象，用于保存cookie值
	sess = requests.Session()

	headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
	html = sess.get("https://www.zhihu.com/#signin",headers = headers).text

	bs = BeautifulSoup(html,"lxml")

	#_xsrf = bs.find("input",attrs = {"name":"_xsrf"}).get("value")

	captcha_url = "https://www.zhihu.com/captcha.gif?r=%d&type=login" %(time.time()*1000)

	captcha_data = sess.get(captcha_url,headers = headers).content
	text = captcha(captcha_data)

	data = {#"_xsrf" : _xsrf,
	        "email" : "838231072@qq.com",
	        "password" : "1102010123",
	        "captcha" : text
	        }
	response = sess.post("https://www.zhihu.com/login/email",data = data,headers = headers)

	response = sess.get("https://www.zhihu.com/people/maozhaojun/activities", headers = headers)
	with open("my.html","w") as f:
		f.write(response.text.encode("utf-8"))

if __name__ == '__main__':
	zhihuLogin()