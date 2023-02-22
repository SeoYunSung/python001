import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('diary.db')

# 커서 생성
cur = conn.cursor()

# 로그인 기능 구현
username = input('Enter your username: ')
password = input('Enter your password: ')
cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
user = cur.fetchone()
if user:
    print('Login successful')
else:
    print('Login failed')

# 연결 종료
conn.close()
