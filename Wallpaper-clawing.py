# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 18:23:31 2020

@author: admin
"""

import requests as rq
import filetype as ft
import os
import json
from contextlib import closing

def Down_load(file_url, file_full_name, now_photo_count, all_photo_count):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    with closing(rq.get(file_url,headers = headers, stream = True)) as response:
       chunk_size = 1024
       #stream = True 确保可以获得原始响应
       content_size = int(response.headers['content-length'])
       data_count = 0
       #将文本流保存到文件
       with open(file_full_name,'wb') as file:
           #边下载边存盘，chunk size是一次请求的最大量
           for data in response.iter_content(chunk_size = chunk_size):
              file.write(data)
              done_block = int((data_count / content_size) * 50)
              data_count = data_count + len(data)
              now_jd = (data_count / content_size) * 100
              #进度条
              print("\r %s：[%s%s] %d%% %d/%d" % (file_full_name, done_block * '█', ' ' * (50 - 1 - done_block), now_jd, now_photo_count, all_photo_count), end=" ")
    file_type = ft.guess(file_full_name)
    os.rename(file_full_name, file_full_name + '.' + file_type.extension)

def crawer_photo(type_id,photo_count):
    if(type_id == 1):
        url = 'https://service.paper.meiyuan.in/api/v2/columns/flow/5c68ffb9463b7fbfe72b0db0?page=1&per_page=' + str(photo_count)
    elif(type_id == 2):
        url = 'https://service.paper.meiyuan.in/api/v2/columns/flow/5c69251c9b1c011c41bb97be?page=1&per_page=' + str(photo_count)
    elif(type_id == 3):
        url = 'https://service.paper.meiyuan.in/api/v2/columns/flow/5c81087e6aee28c541eefc26?page=1&per_page=' + str(photo_count)
    elif(type_id == 4):
        url = 'https://service.paper.meiyuan.in/api/v2/columns/flow/5c81f64c96fad8fe211f5367?page=1&per_page=' + str(photo_count)
    
    headers = {"User-Agent":"Mozilla/5.0(Windows NT 6.1; WoW64)AppleWebKit/537.36(KHTML, like Gecko)Chrome/63.0.3239.132 Safari/537.36"}
    #获取网页,params：像URL传递参
    #response.text：获取源码  response.content:二进制响应用于图片
    respond = rq.get(url,headers = headers)
    #将json解码为python
    photo_data = json.loads(respond.content)
    now_photo_count = 1
    all_photo_count = len(photo_data) 
    
    for photo in photo_data:
        #创建存储路径
        if not os.path.exists('./' + str(type_id)):
            os.makedirs('./' + str(type_id))
        file_url = photo['urls']['raw']
        #图片名称
        file_name_only = file_url.split('/')
        file_name_only = file_name_only[len(file_name_only)-1]
        #图片地址
        file_full_name = './' + str(type_id) + '/' + file_name_only
        Down_load(file_url,file_full_name,now_photo_count,all_photo_count)
        now_photo_count = now_photo_count + 1

if __name__ == '__main__':
    print('开始运行')
    crawer_photo(3,10)