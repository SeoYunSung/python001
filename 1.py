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

# function to change password
def change_password():
    if os.path.exists("management.txt"):
        with open("management.txt", "r") as f:
            management_id, management_pw = f.readlines()
            management_id = management_id.strip()
            management_pw = management_pw.strip()
        current_password = entry_current_pw.get()
        if current_password == "":
            msgbox.showerror("Error", "Please enter the current password.")
        elif current_password != management_pw:
            msgbox.showerror("Error", "Current password is incorrect.")
            entry_current_pw.delete(0, tk.END)
        else:
            new_password = entry_new_pw.get()
            confirm_new_password = entry_confirm_new_pw.get()
            if new_password == "":
                msgbox.showerror("Error", "Please enter the new password.")
            elif new_password != confirm_new_password:
                msgbox.showerror("Error", "Passwords do not match.")
                entry_new_pw.delete(0, tk.END)
                entry_confirm_new_pw.delete(0, tk.END)
            else:
                with open("management.txt", "w") as f:
                    f.write(f"{management_id}\n{new_password}")
                msgbox.showinfo("Password Changed", "The password has been changed.")
                entry_current_pw.delete(0, tk.END)
                entry_new_pw.delete(0, tk.END)
                entry_confirm_new_pw.delete(0, tk.END)

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

# Show login button if admin file exists
if os.path.exists("management.txt"):
    login_button = tk.Button(root, text="Login", font=("TkDefaultFont", 20), command=check_login)
    create_button = None
else:
    login_button = tk.Button(root, text="Login", font=("TkDefaultFont", 20))
    create_button = tk.Button(root, text="Create Admin Account", font=("TkDefaultFont", 20), command=generate_id_pw)

# create login button
login_button.pack()

if create_button:
    # if the management file does not exist, show a message and
    label_first_login = tk.Label(root, text="This is your first login, please create an ID and PW", font=("TkDefaultFont", 20))
    label_first_login.pack()
    create_button.pack()

# create button and entry for changing password
change_password_button = tk.Button(root, text="Change Password", font=("TkDefaultFont", 20), command=change_password)
change_password_button.pack()
label_current_pw = tk.Label(root, text="Current Password:", font=("TkDefaultFont", 20))
label_current_pw.pack()
entry_current_pw = tk.Entry(root, show="*", font=("TkDefaultFont", 20))
entry_current_pw.pack()
label_new_pw = tk.Label(root, text="New Password:", font=("TkDefaultFont", 20))
label_new_pw.pack()
entry_new_pw = tk.Entry(root, show="*", font=("TkDefaultFont", 20))
entry_new_pw.pack()
label_confirm_new_pw = tk.Label(root, text="Confirm New Password:", font=("TkDefaultFont", 20))
label_confirm_new_pw.pack()
entry_confirm_new_pw = tk.Entry(root, show="*", font=("TkDefaultFont", 20))
entry_confirm_new_pw.pack()

root.mainloop()


