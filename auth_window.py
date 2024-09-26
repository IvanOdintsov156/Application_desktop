import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import Database
from datetime import datetime
from application_window import ApplicationWindow
from special_window import SpecialWindow
from registration import RegistrationForm
import customtkinter as ctk

class AuthWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Авторизация")
        self.master.geometry("300x250")  # Set larger window size
        self.master.resizable(False, False)  # Make the window non-resizable

        """ style = ttk.Style()
        style.configure("TLabel", font=("Arial", 16))  # Increase font size for labels
        style.configure("TEntry", font=("Arial", 14))  # Increase font size for entry fields
        style.configure("TButton", font=("Arial", 14))"""
                

        self.db = Database("users.db")

        self.label_username = ctk.CTkLabel(master, text="Имя пользователя") #font=("Arial", 22))
        self.label_username.pack()

        self.entry_username = ctk.CTkEntry(master) # font=("Arial", 12)
        self.entry_username.pack()

        self.label_password = ctk.CTkLabel(master, text="Пароль: ") # font=("Arial", 12)
        self.label_password.pack()

        self.entry_password = ctk.CTkEntry(master, show="*") # font=("Arial", 12)
        self.entry_password.pack()

        self.show_password_var = ctk.BooleanVar()

        self.check_show_password = ctk.CTkCheckBox(master, text="Показать пароль", variable=self.show_password_var, command=self.toggle_password_visibility) # font=("Arial", 10)
        self.check_show_password.pack()

        self.btn_login = ctk.CTkButton(master, text="Войти", command=self.login) #font=("Arial", 12), bg="lightblue"
        self.btn_login.pack(side=tk.TOP)

        self.reg_button = ctk.CTkButton(master, text="Регистрация", command=self.open_registration_form)#font=("Arial", 12), bg="lightblue"
        self.reg_button.pack(side=tk.TOP)
        
        self.label_datetime = ctk.CTkLabel(master, text="") # font=("Arial", 10)
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
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль", parent=self.master)
            self.entry_username.focus_set()  # Set focus back to username entry field

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.entry_password.configure(show="")
        else:
            self.entry_password.configure(show="*")

    def open_application_window(self, username):
        application_window = ctk.CTkToplevel(self.master)
        application_window.title("Главное окно приложения")
        application_window.geometry("600x400")  # Set window size

        # Pass the username to the ApplicationWindow constructor
        ApplicationWindow(application_window, self.db, username, self.master)

    def open_special_window(self, username):
        special_window = ctk.CTkToplevel(self.master)
        special_window.title("Специальное окно для пользователя 2")
        special_window.geometry("600x400")  # Set window size

        # Pass the username to the SpecialWindow constructor
        special_window_instance = SpecialWindow(special_window, self.db, username, self.master)

        tickets = self.db.get_all_tickets()
        special_window_instance._display_tickets(tickets)


    def update_datetime(self):
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.label_datetime.configure(text=current_datetime)
        self.master.after(1000, self.update_datetime)

    def show(self):
        self.master.destroy()
        self.master.deiconify()

    def open_registration_form(self):
        registration_window = ctk.CTkToplevel(self.master)
        registration_window.title("Регистрация")
        registration_window.geometry("300x200")
        registration_window.resizable(False, False)
        registration_form = RegistrationForm(registration_window, self.db)
def main():
    root = ctk.CTk()
    auth_window = AuthWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()

