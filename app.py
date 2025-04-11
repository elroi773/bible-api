from flask import Flask, Response, jsonify
import json
import random
import os

app = Flask(__name__)

API_KEYS = ['my-secret-key']

@app.route('/api/verses')
def get_verses():
    with open('verses.json', encoding='utf-8') as f:
        data = json.load(f)
    return Response(json.dumps(data, ensure_ascii=False, indent=2), mimetype='application/json')

@app.route('/api/random')
def get_random_verse():
    with open('verses.json', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(random.choice(data))

@app.route('/')
def home():
    return "홈입니다!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    