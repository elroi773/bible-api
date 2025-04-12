from flask import Flask, Response, jsonify, request
import json
import random
import os

app = Flask(__name__)

# 그룹된 말씀 로딩
with open("grouped_verses.json", "r", encoding="utf-8") as f:
    grouped_data = json.load(f)

API_KEYS = ['my-secret-key']

# 전체 verses.json 데이터
@app.route('/api/verses')
def get_verses():
    with open('verses.json', encoding='utf-8') as f:
        data = json.load(f)
    return Response(json.dumps(data, ensure_ascii=False, indent=2), mimetype='application/json')

# 랜덤 말씀
@app.route('/api/random')
def get_random_verse():
    with open('verses.json', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(random.choice(data))

# 그룹된 말씀 전체
@app.route('/api/grouped')
def get_grouped():
    return Response(json.dumps(grouped_data, ensure_ascii=False, indent=2), mimetype='application/json')


# 특정 책만 보여주는 API
@app.route('/api/grouped/<book_name>')
def get_grouped_by_book(book_name):
    book = grouped_data.get(book_name)
    if book:
        return Response(json.dumps(book, ensure_ascii=False, indent=2), mimetype='application/json')
    else:
        return Response(json.dumps({"error": "해당 구절이 없습니다"}, ensure_ascii=False), mimetype='application/json', status=404)

# 홈
@app.route('/')
def home():
    return "홈입니다!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
