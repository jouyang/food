from flask import Flask, jsonify, request, make_response, abort
from scrape import scraper
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
	s = scraper()
	if not request.json or not 'url' in request.json:
		abort(400)
	try:
		url = request.json['url']
		result = s.getRecipeIngredients(url)
		data = {'ingredients':result}
		s.closeDriver()
		return jsonify(data), 200
	except:
		e = sys.exc_info()
		# abort(400)
		return e

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error':'Not found'}), 404)

if __name__ == '__main__':
	app.debug = True
	app.run()
