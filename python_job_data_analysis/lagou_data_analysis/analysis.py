from flask import Flask
from flask import render_template
from flask import jsonify
import sys
sys.path.append('/data/dqw_cjy/lagou_crawling')
from handle_insert_data import lagou_mysql
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route("/")
def index():
	return 'Hello, world!'

@app.route("/lagou")
def lagou():
	result = lagou_mysql.count_result()
	return render_template('index.html', result=result)

@app.route('/get_echart_data')
def get_echart_data():
	info = {}
	info['echart_1'] = lagou_mysql.query_industryField_result()
	info['echart_2'] = lagou_mysql.query_salary_result()
	info['echart_31'] = lagou_mysql.query_financeStage_result()
	info['echart_32'] = lagou_mysql.query_companySize_result()
	info['echart_33'] = lagou_mysql.query_jobNature_result()
	info['echart_4'] = lagou_mysql.query_positionName_result()
	info['echart_5'] = lagou_mysql.query_workYear_result()
	info['echart_6'] = lagou_mysql.query_education_result()
	info['map'] = lagou_mysql.query_city_result()
	return jsonify(info)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=80)

