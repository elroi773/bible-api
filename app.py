from flask import Flask, Response, jsonify, request
import json
import random
import os
import uuid

app = Flask(__name__)

# 그룹된 말씀 로딩
with open("grouped_verses.json", "r", encoding="utf-8") as f:
    grouped_data = json.load(f)

def load_api_keys():
    """users.json에서 모든 API 키를 읽어 set으로 반환."""
    try:
        with open("users.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return {user["api_key"] for user in data.get("users", [])}
    except FileNotFoundError:
        # users.json이 없으면 빈 세트 반환
        return set()

def check_api_key():
    """쿼리스트링 ?key= 에서 키를 읽어 유효성 검사."""
    key = request.args.get("key")
    return key in load_api_keys()

# 전체 verses.json 데이터
@app.route('/api/verses')
def get_verses():
    if not check_api_key():
        return jsonify({"error": "API key가 유효하지 않습니다."}), 403

    with open('verses.json', encoding='utf-8') as f:
        data = json.load(f)
    return Response(
        json.dumps(data, ensure_ascii=False, indent=2),
        mimetype='application/json'
    )

# 랜덤 말씀
@app.route('/api/random')
def get_random_verse():
    if not check_api_key():
        return jsonify({"error": "API key가 유효하지 않습니다."}), 403

    with open('verses.json', encoding='utf-8') as f:
        data = json.load(f)
    verse = random.choice(data)
    return Response(
        json.dumps(verse, ensure_ascii=False, indent=2),
        mimetype='application/json'
    )

# 그룹된 말씀 전체
@app.route('/api/grouped')
def get_grouped():
    if not check_api_key():
        return jsonify({"error": "API key가 유효하지 않습니다."}), 403

    return Response(
        json.dumps(grouped_data, ensure_ascii=False, indent=2),
        mimetype='application/json'
    )

# 특정 책만 보여주는 API
# <book_name> 에 예: 시편, 빌립보서 등
@app.route('/api/grouped/<book_name>')
def get_grouped_by_book(book_name):
    if not check_api_key():
        return jsonify({"error": "API key가 유효하지 않습니다."}), 403

    book = grouped_data.get(book_name)
    if book:
        return Response(
            json.dumps(book, ensure_ascii=False, indent=2),
            mimetype='application/json'
        )
    else:
        return jsonify({"error": "해당 구절이 없습니다"}), 404

# 홈
@app.route('/')
def home():
    return "홈입니다!"

# API 키 발급 엔드포인트
@app.route('/get-key')
def get_api_key():
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "이메일을 입력해주세요"}), 400

    # users.json 로드
    try:
        with open('users.json', 'r', encoding='utf-8') as f:
            users_data = json.load(f)
    except FileNotFoundError:
        users_data = {"users": []}

    # 기존 사용자 확인
    for user in users_data.get('users', []):
        if user.get('email') == email:
            return jsonify({"api_key": user['api_key']})

    # 새 키 생성 및 저장
    new_key = str(uuid.uuid4())
    users_data.setdefault('users', []).append({
        "email": email,
        "api_key": new_key
    })
    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(users_data, f, ensure_ascii=False, indent=2)

    return jsonify({"api_key": new_key})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
