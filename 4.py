import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import calendar
import datetime


# 데이터베이스 연결
conn = sqlite3.connect('church.db')

# 커서 생성
cursor = conn.cursor()

# 테이블 생성
cursor.execute('''
CREATE TABLE IF NOT EXISTS member (
    id INTEGER PRIMARY KEY,
    name TEXT,
    date TEXT,
    donation_type TEXT,
    amount INTEGER
)
''')

# 데이터 삽입 함수
def insert_data():
    # 데이터 삽입
    name = entry_name.get()
    date = entry_date.get()
    donation_type = entry_donation_type.get()
    amount = entry_amount.get()

    cursor.execute("INSERT INTO member (name, date, donation_type, amount) VALUES (?, ?, ?, ?)", (name, date, donation_type, amount))

    # 검색 결과 출력
    cursor.execute("SELECT * FROM member WHERE name=?", (name,))
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # 커밋
    conn.commit()

# 로그인 함수
def login():
    if entry_id.get() == '123' and entry_pw.get() == 'qwe':
        root.deiconify()  # 메인 창 보이기
        login_window.destroy()  # 로그인 창 닫기
    else:
        label_error.config(text='ID 또는 PW가 잘못되었습니다.')

# 날짜 선택 함수
def choose_date():
    def set_date(selected_date):
        entry_date.delete(0, tk.END)
        entry_date.insert(0, selected_date.strftime('%Y-%m-%d'))
        top.destroy()

    try:
        year = int(entry_date.get().split('-')[0])
        month = int(entry_date.get().split('-')[1])
    except ValueError:
        # entry_date.get()의 형식이 YYYY-MM-DD가 아닌 경우 현재 날짜를 기본값으로 사용
        year, month = datetime.date.today().year, datetime.date.today().month

    top = tk.Toplevel(root)

    # 년도와 월을 선택하는 콤보박스 추가
    year_month_frame = tk.Frame(top)
    year_month_frame.pack()
    year_scale = ttk.Combobox(year_month_frame, state='readonly', values=[str(y) for y in range(1900, 2101)], width=6)
    year_scale.current(year - 1900)
    year_scale.pack(side=tk.LEFT, padx=5)
    month_scale = ttk.Combobox(year_month_frame, state='readonly', values=[str(m) for m in range(1, 13)], width=4)
    month_scale.current(month - 1)
    month_scale.pack(side=tk.LEFT)
    year_month_frame.pack()

    # 선택한 년도와 월에 해당하는 달력 표시
    def update_calendar():
        year = int(year_scale.get())
        month = int(month_scale.get())
        cal = calendar.monthcalendar(year, month)
        today = datetime.date.today()
        for i, week in enumerate(cal):
            for j, day in enumerate(week):
                if day == 0:
                    day_button_list[i][j].configure(text='', bg='white')
                else:
                    button = day_button_list[i][j]
                    button.configure(text=str(day), bg='white')
                    button.config(relief=tk.RAISED)
