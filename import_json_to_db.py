import json
import pymysql

# 1. DB 연결 설정
conn = pymysql.connect(
    host='localhost',
    user='your_username',     # 예: 'root'
    password='your_password', # 예: '1234'
    db='bible_app',           # 사용 중인 DB 이름
    charset='utf8mb4'
)
cursor = conn.cursor()

# 2. JSON 파일 열기
with open('structured_verses.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 3. JSON 구조 순회하며 INSERT
for book, chapters in data.items():
    for chapter_entry in chapters:
        chapter = chapter_entry['chapter']
        for verse_entry in chapter_entry['verses']:
            verse = verse_entry['verse']
            text = verse_entry['text']
            try:
                cursor.execute(
                    "INSERT INTO bible_verses (book, chapter, verse, text) VALUES (%s, %s, %s, %s)",
                    (book, chapter, verse, text)
                )
            except pymysql.err.IntegrityError:
                print(f"중복 건너뜀: {book} {chapter} {verse}")
                continue

# 4. DB 반영 후 종료
conn.commit()
cursor.close()
conn.close()

print("데이터 추가 완료")