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

def choose_date():
    global top # top 변수를 전역변수로 지정
    def set_date():
        selected_date = cal.selection_get()
        entry_date.delete(0, tk.END)
        entry_date.insert(0, selected_date.strftime('%Y-%m-%d'))
        top.destroy()

    def update_calendar():
        nonlocal year, month, days
        year, month = cal.date.year, cal.date.month
        days = cal.monthdayscalendar(year, month)
        year_month_label.config(text='{}년 {}월'.format(year, month))
        for label in top.grid_slaves():
            if int(label.grid_info()["row"]) >= 2 and int(label.grid_info()["column"]) >= 0:
                label.grid_forget()
        for i, week in enumerate(days):
            for j, day in enumerate(week):
                if day == 0:
                    label = tk.Label(top, text=' ', font=('Arial', 12))
                else:
                    label = tk.Label(top, text=str(day), font=('Arial', 12))
                    label.bind('<Button-1>', lambda e, day=day: set_date())
                label.grid(row=i+2, column=j)

    top = tk.Toplevel(root)
    top.geometry('350x350')
    x = (root.winfo_screenwidth() // 2) - (top.winfo_reqwidth() // 2)
    y = (root.winfo_screenheight() // 2) - (top.winfo_reqheight() // 2)
    top.geometry("+{}+{}".format(x, y))
    cal = calendar.Calendar(firstweekday=calendar.SUNDAY)
    try:
        year = int(entry_date.get().split('-')[0])
        month = int(entry_date.get().split('-')[1])
    except ValueError:
        # entry_date.get()의 형식이 YYYY-MM-DD가 아닌 경우 현재 날짜를 기본값으로 사용
        now = datetime.datetime.now()
        year, month = now.year, now.month
    days = cal.monthdayscalendar(year, month)
    day_names = ['일', '월', '화', '수', '목', '금', '토']
    year_month_label = tk.Label(top, font=tkFont.Font(size=16))
    year_month_label.grid(row=0, column=0, columnspan=7, pady=(10, 20))
for i, name in enumerate(day_names):
label = tk.Label(top, text=name, font=tkFont.Font(weight='bold'))
label.grid(row=1, column=i, sticky='nsew')

year_month_label = tk.Label(top, font=tkFont.Font(size=16))
year_month_label.grid(row=0, column=0, columnspan=7, pady=(10, 20))

update_calendar()

prev_month_button = tk.Button(top, text='<', command=cal.prev_month)
prev_month_button.grid(row=0, column=0, padx=10)

next_month_button = tk.Button(top, text='>', command=cal.next_month)
next_month_button.grid(row=0, column=6, padx=10)

top.grab_set()
top.wait_window()


# GUI 창 생성
root = tk.Tk()
root.title('교인 및 헌금 관리 시스템')

# 창 크기 설정
root_width = 400
root_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (root_width // 2)
y = (screen_height // 2) - (root_height // 2)
root.geometry(f'{root_width}x{root_height}+{x}+{y}')

# 레이블
label_name = tk.Label(root, text='이름')
label_name.grid(row=0, column=0)

label_date = tk.Label(root, text='날짜')
label_date.grid(row=1, column=0)

label_donation_type = tk.Label(root, text='헌금 항목')
label_donation_type.grid(row=2, column=0)

label_amount = tk.Label(root, text='금액')
label_amount.grid(row=3, column=0)

# 입력창
entry_name = tk.Entry(root, width=30)
entry_name.grid(row=0, column=1)

entry_date = tk.Entry(root, width=30)
entry_date.grid(row=1, column=1)
entry_date.bind('<Button-1>', lambda e: choose_date())

entry_donation_type = tk.Entry(root, width=30)
entry_donation_type.grid(row=2, column=1)

entry_amount = tk.Entry(root, width=30)
entry_amount.grid(row=3, column=1)

# 버튼
button_insert = tk.Button(root, text='추가', command=insert_data)
button_insert.grid(row=4, column=0, columnspan=2, pady=10)

# 메인 창 숨기기
root.withdraw()

# 로그인 창 생성
login_window = tk.Toplevel()
login_window.title('로그인')
login_window.geometry('500x500')

# 창을 화면 중앙에 위치시키기
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (500 // 2)
y = (screen_height // 2) - (500 // 2)
login_window.geometry(f'+{x}+{y}')

# ID 입력
frame_id = tk.Frame(login_window)
frame_id.pack(pady=20)
label_id = tk.Label(frame_id, text='ID', width=8, font=('Arial', 20))
label_id.pack(side=tk.LEFT)
entry_id = tk.Entry(frame_id, font=('Arial', 20))
entry_id.pack(side=tk.LEFT)

# 비밀번호 입력
frame_pw = tk.Frame(login_window)
frame_pw.pack(pady=20)
label_pw = tk.Label(frame_pw, text='비밀번호', width=8, font=('Arial', 20))
label_pw.pack(side=tk.LEFT)
entry_pw = tk.Entry(frame_pw, show='*', font=('Arial', 20))
entry_pw.pack(side=tk.LEFT)

# 로그인 버튼
button_login = tk.Button(login_window, text='로그인', command=login, font=('Arial', 20))
button_login.pack(pady=20)

# 에러 메시지
label_error = tk.Label(login_window, fg='red', font=('Arial', 20))
label_error.pack()

#창 실행
try:
    while True:
        root.mainloop()
except KeyboardInterrupt:
    pass

# 프로그램 종료
conn.close()

root.destroy()