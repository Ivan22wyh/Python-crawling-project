import requests
import re
import os
from bs4 import BeautifulSoup
from progressbar import ProgressBar

class Crawler(object):

    def __init__(self, url, num):
        self.num = num
        self.session = requests.session()
        self.reference_url = url
        self.headers = {
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
        'Referer':url
        }

    def get_soup(self):
        r = self.session.get(self.reference_url, headers=self.headers, verify=False)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    def create_path(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def download(self, url):
        r = self.session.get(url, headers=self.headers, verify=False, stream=True)
        print('正在下载：第{}集'.format(str(self.num + 1)))
        with open(self.name, 'wb') as f:
            for i in r.iter_content(chunk_size=1024):
                f.write(i)

    def get_playdata(self):
        soup = self.get_soup()
        name = soup.find('div', class_='ptitle1').find('h1').find('a').text
        self.path = 'D:/Wenyh database/For fun/TV series & movies/{}'.format(name)
        self.name = self.path +'/{} 第{}集.mp4'.format(name, str(self.num + 1))
        playdata_js = 'http://www.imomoe.in' + soup.find('div', class_='player').find('script', type='text/javascript').get('src')
        playdata_text = self.session.get(playdata_js, headers=self.headers, verify=False).text
        pattern = re.compile(r"https://(.*?)flv")
        self.playdata = re.findall(pattern, playdata_text)[self.num].replace('$','')

    def get_video(self):
        download_url = 'https://' + self.playdata
        create_path(self.path)
        download(download_url)

if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()
    for i in range(24):
        url = "http://www.imomoe.in/player/4213-0-{}.html".format(i)
        crawler = Crawler(url, i)
        crawler.get_playdata()
        crawler.get_video()
        
    
