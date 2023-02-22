import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import calendar
import datetime


# database connection
conn = sqlite3.connect('church.db')

# create cursor
cursor = conn.cursor()

# create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS member (
    id INTEGER PRIMARY KEY,
    name TEXT,
    date TEXT,
    donation_type TEXT,
    amount INTEGER
)
''')

# data insert function
def insert_data():
    # insert data
    name = entry_name.get()
    date = entry_date.get()
    donation_type = entry_donation_type.get()
    amount = entry_amount.get()

    cursor.execute("INSERT INTO member (name, date, donation_type, amount) VALUES (?, ?, ?, ?)", (name, date, donation_type, amount))

    # Print search results
    cursor.execute("SELECT * FROM member WHERE name=?", (name,))
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # commit
    conn.commit()

# login function
def login():
    if entry_id.get() == '123' and entry_pw.get() == 'qwe':
        root.deiconify() # show main window
        login_window.destroy() # Close the login window
    else:
        label_error.config(text='Invalid ID or PW.')


def choose_date():
    def set_date():
        selected_date = cal.selection_get()
        entry_date.delete(0, tk.END)
        entry_date.insert(0, selected_date.strftime('%Y-%m-%d'))
        top.destroy()

    top = tk.Toplevel(root)
    top.title('날짜 선택')
    top.geometry('350x350')

    cal = calendar.Calendar(firstweekday=calendar.SUNDAY)
    try:
        year, month = int(entry_date.get().split('-')[0]), int(entry_date.get().split('-')[1])
    except ValueError:
        now = datetime.datetime.now()
        year, month = now.year, now.month

    def update_calendar():
        nonlocal year, month
        year = int(year_entry.get())
        month = month_combobox.current() + 1
        redraw_calendar()

    def redraw_calendar():
        body = tk.Frame(top)
        body.pack(side="top", fill="both", expand=True)

        day_names = ['일', '월', '화', '수', '목', '금', '토']
        for i, name in enumerate(day_names):
            label = tk.Label(body, text=name, font=tkFont.Font(weight='bold'))
            label.grid(row=0, column=i, sticky='nsw')

        days = cal.monthdayscalendar(year, month)
        button = []
        for week_num, week in enumerate(days):
            row = []
            for day_num, day in enumerate(week):
                if day != 0:
                    b = tk.Button(body, text=day, width=2, height=1,
                                  command=lambda day=day: set_date(day),
                                  font=tkFont.Font(weight='bold'))
                    b.grid(row=week_num+1, column=day_num, sticky="nsew")
                    if day == datetime.datetime.now().day and month == datetime.datetime.now().month:
                        b.configure(bg='light blue')
                    row.append(b)
                else:
                    tk.Label(body, text='', font=tkFont.Font(weight='bold')).grid(row=week_num+1, column=day_num, sticky="nsew")
                    row.append(None)
            button.append(row)

    # Create a calendar for the first time
    redraw_calendar()

    # Year and month selection widget
    year_label = tk.Label(top, text="년도")
    year_label.pack()
    year_entry = tk.Entry(top, width=10)
    year_entry.insert(0, year)
    year_entry.pack()

    month_label = tk.Label(top, text="월")
    month_label.pack()
    month_combobox = ttk.Combobox(top, values=[f"{i}월" for i in range(1, 13)], state="readonly")
    month_combobox.current(month-1)
    month_combobox.pack()

    # "Go" button to update calendar
    go_button = tk.Button(top, text="확인", command=update_calendar)
    go_button.pack()

    top.grab_set()
    top.wait_window()


# Year and month selection widget
year_label = tk.Label(top, text="Year")
year_label.pack()
year_entry = tk.Entry(top, width=10)
year_entry.insert(0, year)
year_entry.pack()

month_label = tk.Label(top, text="Month")
month_label.pack()
month_combobox = ttk.Combobox(top, values=[calendar.month_name[i] for i in range(1, 13)], state="readonly")
month_combobox.current(month-1)
month_combobox.pack()

# "Go" button to update calendar
go_button = tk.Button(top, text="Go", command=update_calendar)
go_button.pack()

top.grab_set()
top.wait_window()

