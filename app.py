from flask import Flask, jsonify, request
import scrape

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
	result = scrape.ingredients(request.form['url'])
	return jsonify(result)

if __name__ == '__main__':
        app.run()
