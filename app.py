from flask import Flask, Response
import json

app = Flask(__name__)

@app.route('/api/verses')
def get_verses():
    with open('verses.json', encoding='utf-8') as f:
        data = json.load(f)
    return Response(json.dumps(data, ensure_ascii=False, indent=2), mimetype='application/json')


def get_random_verse():
    with open('verses.json', encoding = 'utf-8') as f:
        data = json.load(f)
    import random 
    return jsonify(random.choice(data))

if __name__ == '__main__':
    app.run(debug=True)