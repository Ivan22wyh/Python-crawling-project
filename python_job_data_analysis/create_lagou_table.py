from sqlalchemy import create_engine, Integer, Float, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column

#创建数据库连接
engine = create_engine("mysql+pymysql://root:jtwhgx22@192.168.1.103:3306/lagou?charset=utf8", pool_pre_ping=True)

#操作数据库
Session = sessionmaker(bind=engine)

#声明一个基类
Base = declarative_base()

class Lagoutables(Base):
	#表名称
	__tablename__ = 'lagou_data_python'

	#id 整数 主键 自增 
	id = Column(Integer, primary_key=True, autoincrement=True)
	#岗位ID 整数 不为空
	positionId = Column(Integer, nullable=True)
	#经度
	longitude = Column(Float, nullable=True)
	#纬度
	latitude = Column(Float, nullable=True)
	#职位名称
	positionName = Column(String(length=50), nullable=True)
	#工作年限
	workYear = Column(String(length=20), nullable=True)
	#学历
	education = Column(String(length=20), nullable=True)
	#岗位性质
	jobNature = Column(String(length=20), nullable=True)
	#公司类型
	financeStage = Column(String(length=30), nullable=True)
	#公司规模
	companySize = Column(String(length=30), nullable=True)
	#业务方向
	industryField = Column(String(length=30), nullable=True)
	#所在城市
	city = Column(String(length=10), nullable=True)
	#岗位标签
	positionAdvantage = Column(String(length=200), nullable=True)
	#公司简称
	companyShortName = Column(String(length=50), nullable=True)
	#公司全称
	companyFullName = Column(String(length=200), nullable=True)
	#公司所在区
	district = Column(String(length=20), nullable=True)
	#公司福利标签
	companyLabelList = Column(String(length=200), nullable=True)
	#工资
	salary = Column(String(length=20), nullable=True)
	#爬取日期
	crawl_date = Column(String(length=20), nullable=True)

if __name__ == '__main__':
	#创建表,必须确保mysql有远程连接的权限
	'''步骤：1.mysql -u root -p密码
	2.use mysql
	3.update user set host = '%'where user = 'root';
	4.FLUSH PRIVILEGES;'''
	Lagoutables.metadata.create_all(engine)





