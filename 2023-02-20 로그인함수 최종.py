import tkinter as tk
import tkinter.messagebox as msgbox
import os

# create main window
root = tk.Tk()
root.title("Login")
root.geometry("700x700+{0}+{1}".format(int(root.winfo_screenwidth()/2 - 350), int(root.winfo_screenheight()/2 - 350)))

# create function to check login
def check_login():
    # check if ID and password match
    if os.path.exists("management.txt"):
        with open("management.txt", "r") as f:
            management_id, management_pw = f.readlines()
            management_id = management_id.strip()
            management_pw = management_pw.strip()
        if entry_id.get() == management_id and entry_pw.get() == management_pw:
            msgbox.showinfo("Login Successful", "Welcome, Administrator!")
            root.destroy()
        else:
            msgbox.showerror("Login Failed", "Please check ID or password and try again.")
            # clear the entry fields
            entry_id.delete(0, tk.END)
            entry_pw.delete(0, tk.END)
    else:
        msgbox.showerror("Login Failed", "No administrator account found.")

# generate management ID and PW at first login
def generate_id_pw():
    # check if management file exists
    if os.path.exists("management.txt"):
        msgbox.showerror("Error", "Administrator account already exists.")
    else:
        # get ID and password
        management_id = entry_id.get()
        management_pw = entry_pw.get()
        # check if ID and password are entered
        if management_id == "" or management_pw == "":
            msgbox.showerror("Error", "Please enter an ID and password.")
        else:
            # store ID and password in a file
            with open("management.txt", "w") as f:
                f.write(f"{management_id}\n{management_pw}")
            msgbox.showinfo("ID and Password Generated", "The management ID and password have been generated.")
            # hide the generate button and show the login button
            create_button.pack_forget()
            label_first_login.pack_forget()
            login_button.configure(command=check_login)
            # set focus on ID field
            entry_id.focus()

# Show login button if admin file exists
if os.path.exists("management.txt"):
    login_button = tk.Button(root, text="Login", font=("TkDefaultFont", 20), command=check_login)
    create_button = None
else:
    login_button = tk.Button(root, text="Login", font=("TkDefaultFont", 20))
    create_button = tk.Button(root, text="Create Admin Account", font=("TkDefaultFont", 20), command=generate_id_pw)

# create label and entry for management ID
label_id = tk.Label(root, text="Management ID:", font=("TkDefaultFont", 20))
label_id.pack()
entry_id = tk.Entry(root, font=("TkDefaultFont", 20))
entry_id.pack()

# create label and entry for management password
label_pw = tk.Label(root, text="Password:", font=("TkDefaultFont", 20))
label_pw.pack()
entry_pw = tk.Entry(root, show="*", font=("TkDefaultFont", 20))
entry_pw.pack()

# create login button
login_button.pack()

if create_button:
    # if the management file does not exist, show a message and
    label_first_login = tk.Label(root, text="This is your first login, please create an ID and PW", font=("TkDefaultFont", 20))
    label_first_login.pack()
    create_button.pack()

root.mainloop()
