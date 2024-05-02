import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import Database
from datetime import datetime
from application_window import ApplicationWindow
from special_window import SpecialWindow

class AuthWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Авторизация")
        self.master.geometry("300x200")  # Set larger window size
        self.master.resizable(False, False)  # Make the window non-resizable

        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 16))  # Increase font size for labels
        style.configure("TEntry", font=("Arial", 14))  # Increase font size for entry fields
        style.configure("TButton", font=("Arial", 14))

        self.db = Database("users.db")

        self.label_username = tk.Label(master, text="Имя пользователя", font=("Arial", 12))
        self.label_username.pack()

        self.entry_username = tk.Entry(master, font=("Arial", 12))
        self.entry_username.pack()

        self.label_password = tk.Label(master, text="Пароль: ", font=("Arial", 12))
        self.label_password.pack()

        self.entry_password = tk.Entry(master, show="*", font=("Arial", 12))
        self.entry_password.pack()

        self.show_password_var = tk.BooleanVar()

        self.check_show_password = tk.Checkbutton(master, text="Показать пароль", variable=self.show_password_var, command=self.toggle_password_visibility, font=("Arial", 10))
        self.check_show_password.pack()

        self.btn_login = tk.Button(master, text="Войти", command=self.login, font=("Arial", 12), bg="lightblue")
        self.btn_login.pack()

        self.label_datetime = tk.Label(master, text="", font=("Arial", 10))
        self.label_datetime.pack()

        self.update_datetime()  # Start updating datetime

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if self.db.check_credentials(username, password):
            self.master.withdraw()
            if username == "2":
                self.open_special_window(username)
            else:
                self.open_application_window(username)
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.entry_password.config(show="")
        else:
            self.entry_password.config(show="*")

    def open_application_window(self, username):
        application_window = tk.Toplevel(self.master)
        application_window.title("Главное окно приложения")
        application_window.geometry("600x400")  # Set window size

        # Pass the username to the ApplicationWindow constructor
        ApplicationWindow(application_window, self.db, username, self.master)

    def open_special_window(self, username):
        special_window = tk.Toplevel(self.master)
        special_window.title("Специальное окно для пользователя 2")
        special_window.geometry("600x400")  # Set window size

        # Pass the username to the SpecialWindow constructor
        special_window_instance = SpecialWindow(special_window, self.db, username, self.master)

        tickets = self.db.get_all_tickets()
        special_window_instance._display_tickets(tickets)


    def update_datetime(self):
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.label_datetime.config(text=current_datetime)
        self.master.after(1000, self.update_datetime)

    def show(self):
        self.master.destroy()
        self.master.deiconify()

def main():
    root = tk.Tk()
    auth_window = AuthWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
