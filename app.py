from flask import Flask, jsonify, request
from scrape import ingredients
import sys, json

app = Flask(__name__)

@app.route('/')
def index():
        return 'Hello world'

@app.route('/data')
def recipes():
        data = {"recipes": ["egg","pork"],
                "ingredients":["soy","butter"]}
        return jsonify(data)

@app.route('/api/ingredients', methods=['POST'])
def scrape():
	try:
		url = request.form['url']
		result = ingredients(url)
		data = {'ingredients':result}
		return json.dumps(data)
	except:
		e = sys.exc_info()
		return e

if __name__ == '__main__':
	app.debug = True
	app.run()
