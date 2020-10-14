import requests
from bs4 import BeautifulSoup
import xlwt
from sqlalchemy import create_engine, Integer, Float, String, Text, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql+pymysql://root:jtwhgx22@127.0.0.1:3306/test?charset=utf8", pool_pre_ping=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Movie(Base):
    __tablename__ = 'douban movie'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=True)
    director = Column(Text, nullable=True)
    actors = Column(Text, nullable=True)
    index = Column(Text, nullable=True)
    score = Column(Float, nullable=True)
    rank = Column(Integer, nullable=True)
    intro = Column(Text, nullable=True)

    def __repr__(self):
        return "<Movie({}|{}'|score:{})>".format(self.name, self.actors, self.score)

def access_page(url):
    r = requests.get(url, headers=headers, verify=False)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    movies = soup.find('ol', class_='grid_view').find_all('li')
    for movie in movies:
        movie_rank = int(movie.find('div', class_='pic').find('em').get_text())
        movie_url = movie.find('div', class_='hd').find('a').get('href')
        try:
            movie_intro = movie.find('span', class_='inq').get_text()
        except:
            movie_intro = '' 
        access_movie(movie_url, movie_rank, movie_intro)

def access_movie(movie_url, movie_rank, movie_intro):
    r = requests.get(movie_url, headers=headers, verify=False)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser') 
    movie_name = soup.find('span', property="v:itemreviewed").get_text()
    movie_drt = soup.find('a', rel="v:directedBy").get_text()
    movie_act = ''
    movie_acts = soup.find_all('a', rel="v:starring")
    act_num = 0
    for act in movie_acts:
        act_num += 1
        if act_num < 4:
            movie_act += (act.get_text() + '/')
        else:
            break
    movie_index= ''
    movie_indexes = soup.find_all('span', property="v:genre")
    for index in movie_indexes:
        movie_index += (index.get_text() + '/')
    movie_score = float(soup.find('strong', class_="ll rating_num").get_text())
    movie_img = soup.find('a', class_='nbgnbg').find('img').get('src')
    print('正在爬取：{}|{}|{}|{}|{}|{}|{}'.format(movie_name, movie_drt, movie_act, movie_index, movie_score, movie_rank, movie_intro))
    '''sheet.write(movie_rank,0,movie_name)
    sheet.write(movie_rank,1,movie_drt)
    sheet.write(movie_rank,2,movie_act)
    sheet.write(movie_rank,3,movie_index)
    sheet.write(movie_rank,4,movie_rank)
    sheet.write(movie_rank,5,movie_score)
    sheet.write(movie_rank,6,movie_intro)'''
    
    #with open('豆瓣电影TOP250.txt', 'a', encoding='utf-8') as f:
    #    f.write('{}|{}|{}|{}|{}|{}|{}\n'.format(movie_name, movie_drt, movie_act, movie_index, movie_score, movie_rank, movie_intro))

    new_movie = Movie(
        name=movie_name,
        director=movie_drt,
        actors=movie_act,
        index=movie_index,
        score=movie_score,
        rank=movie_rank,
        intro=movie_intro
    )
    
    session.add(new_movie)
    session.commit()

if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    Movie.metadata.create_all(engine)
    session = Session()

    for i in range(0, 250, 25):
        url = "http://movie.douban.com/top250?start={}&filter=".format(i)
        access_page(url)

