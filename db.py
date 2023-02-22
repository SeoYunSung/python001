import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('diary.db')

# 커서 생성
cur = conn.cursor()

# users 테이블 생성
cur.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )
''')

# 사용자 데이터 추가
cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('seo', '1234'))
cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('user2', 'password2'))
cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('user3', 'password3'))

# 데이터베이스 저장
conn.commit()

# 연결 종료
conn.close()

import sqlite3
from tkinter import *

# 데이터베이스 연결
conn = sqlite3.connect('diary.db')

# 커서 생성
cur = conn.cursor()

# 윈도우 생성
window = Tk()
window.title('diary')
window.geometry('700x800')

# 사용자 이름 입력 레이블과 엔트리
username_label = Label(window, text='Username')
username_label.pack()
username_entry = Entry(window)
username_entry.pack()

# 비밀번호 입력 레이블과 엔트리
password_label = Label(window, text='Password')
password_label.pack()
password_entry = Entry(window, show='*')
password_entry.pack()

# 일기 작성 레이블과 텍스트 박스
diary_label = Label(window, text='Write your diary')
diary_label.pack()
diary_textbox = Text(window)
diary_textbox.pack()

# 일기 작성 버튼
def save_diary():
    username = username_entry.get()
    password = password_entry.get()
    diary = diary_textbox.get('1.0', 'end')
    cur.execute("INSERT INTO diary (username, diary) VALUES (?, ?)", (username, diary))
    conn.commit()
    diary_textbox.delete('1.0', 'end')
    messagebox.showinfo('Success', 'Diary saved successfully')

save_button = Button(window, text='Save', command=save_diary)
save_button.pack()

# 일기 조회 레이블과 텍스트 박스
view_label = Label(window, text='View your diary')
view_label.pack()
view_textbox = Text(window)
view_textbox.pack()

# 일기 조회 버튼
def view_diary():
    username = username_entry.get()
    password = password_entry.get()
    cur.execute("SELECT * FROM diary WHERE username=? AND password=?", (username, password))
    diaries = cur.fetchall()
    view_textbox.delete('1.0', 'end')
    if diaries:
        for diary in diaries:
            view_textbox.insert('end', diary[2] + '\n\n')
    else:
        messagebox.showinfo('No data', 'No diary found')

view_button = Button(window, text='View', command=view_diary)
view_button.pack()

# 윈도우 실행
window.mainloop()

# 연결 종료
conn.close()
