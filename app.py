from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
        return 'Hello world'

@app.route('/data')
def recipes():
        data = {"recipes": ["egg","pork"],
                "ingredients":["soy","butter"]}
        return jsonify(data)

if __name__ == '__main__':
        app.run()
