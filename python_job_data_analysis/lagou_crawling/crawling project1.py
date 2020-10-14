'''
方法：通过fiddler抓包，了解请求的内容，掌握爬虫模拟请求的信息，运用代理进行模拟请求
目的：对每个城市的每一页进行爬取
步骤：
1.通过访问全部城市的请求获取全部城市列表的html文件，运用bs4进行解析或用正则表达式进行
匹配获取每个城市
2.进入城市界面，查看请求，发现先GET，后携带GET所获取的data，reference和cookies进行POST
3.爬虫GET入网站获取需要的信息，同时用bs4或正则表达式获取每个城市的页数及页数对应的网址，对每页发起POST
'''

import re
import time
import json
import requests
import multiprocessing
from handle_insert_data import HandleLagouData
from bs4 import BeautifulSoup

class HandleLaGou(object):

	def __init__(self):
		#使用session保存coockies信息
		self.session = requests.session()
		self.header = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
		}
		self.city_list = ""

	#获取全国城市
	def handle_city(self):
		all_city_list = []
		city_search = re.compile(r'zhaopin/">(.*?)</a>')
		city_url = "https://www.lagou.com/jobs/allCity.html"
		city_result = self.handle_request(method = 'GET', url = city_url)
		soup = BeautifulSoup(city_result, 'html.parser')
		city_list_firstnumber = soup.find_all('ul', class_ = 'city_list')
		for city_lists in city_list_firstnumber:
			city_list = city_lists.find_all('li')
			for city in city_list:
				city_name = city.get_text()
				city_name = city_name.replace('\n', '', 3)
				all_city_list.append(city_name)
		#self.city_list = re.findall(city_search, city_result)
		#清理coockies，以便后续获取需要的cookies
		self.city_list = all_city_list
		self.session.cookies.clear()
		

	def handle_city_job(self, city):
		
		first_requests_url = 'https://www.lagou.com/jobs/list_python?&px=default&city={}'.format(city)  
		first_response = self.handle_request(method = 'GET', url = first_requests_url)
		total_page_search = re.compile(r'class="span\stotalNum">(\d+)</span>')
		try:
			total_page = total_page_search.search(first_response).group(1)
		except:
			return
		else:
			for i in range(1, int(total_page) + 1):
				page_url = "https://www.lagou.com/jobs/positionAjax.json?px=default&city={}&needAddtionalResult=false".format(city)
				data = {
					"pn":i,
					"kd":"python"
				}
				print(city, i)
				referer_url = "Referer: https://www.lagou.com/jobs/list_python?&px=default&city={}".format(city)
				self.header['Referer'] = referer_url.encode()
				response = self.handle_request(method = 'POST', url = page_url, data = data, info = city)
				lagou_data = json.loads(response)
				job_list = lagou_data['content']['positionResult']['result']
				for job in job_list:
					lagou_mysql.insert_item(job)

	def handle_request(self, method, url, data = None, info = None):
		while True:
			#加入阿布云信息

			requests.packages.urllib3.disable_warnings()

			proxyinfo = "http://{}:{}@{}:{}".format('HH87UY3C38GPV1ID', 'F595952EDA67AA58', 'http-dyn.abuyun.com', '9020')
			proxy = {
				"http":proxyinfo, 
				"https":proxyinfo
			}
			try:
				if method == 'GET':
					#使用session.get可以保留cookie，再次请求时默认使用cookie参数
					response = self.session.get(url = url, headers = self.header, verify = False, proxies = proxy, timeout = 10)
					response.encoding = 'utf-8'
				elif method == 'POST':
					response = self.session.post(url = url, headers = self.header, verify = False, data = data, proxies = proxy, timeout = 10)
					response.encoding = 'utf-8'
			except:
				#代理IP活动性差，需要清理cookies重新使用，清理后记得使用continue再次申请
				first_requests_url = 'https://www.lagou.com/jobs/list_python?&px=default&city={}'.format(info)
				first_response = self.handle_request(method = 'GET', url = first_requests_url, info = info) 
				time.sleep(10)
				continue
			response.encoding = 'utf-8'

			#频繁操作要清理cookies，记得加上continue再次申请
			if '频繁' in response.text:
				print('频繁', response.text)
				self.session.cookies.clear()
				first_requests_url = 'https://www.lagou.com/jobs/list_python?&px=default&city={}'.format(info)
				first_response = self.handle_request(method = 'GET', url = first_requests_url, info = info) 
				time.sleep(10)
				continue
			return response.text

if __name__ == '__main__':
	#禁用https的ssl证书验证
	requests.packages.urllib3.disable_warnings()
	lagou = HandleLaGou()
	lagou.handle_city()
	lagou_mysql = HandleLagouData()
	pool = multiprocessing.Pool(3)
	n = 0
	print(lagou.city_list)
	'''for city in lagou.city_list:
		n += 1
		if (n >= 133) & (n<=133):
			
			lagou.handle_city_job(city)
			'''
			
			#pool.apply_async(lagou.handle_city_job, args = (city,))
	pool.close()
	pool.join()
	
	lagou.handle_city_job('张家界')
	





    


