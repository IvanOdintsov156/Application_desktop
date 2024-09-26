import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import re
from PIL import Image, ImageTk
import customtkinter as ctk
class RegistrationForm:
    BUTTON_STYLE = {"foreground": "white", "background": "#4CAF50", "font": ("Arial", 12, "bold")}
    LABEL_STYLE = {"background": "#eee", "font": ("Arial", 12)}
    ENTRY_STYLE = {"font": ("Arial", 12)}
    def __init__(self, root, db):
        self.root = root
        self.root.iconbitmap("static/icon.ico")
        self.root.title("Регистрация")
        '''self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton", **RegistrationForm.BUTTON_STYLE)
        self.style.configure("TLabel", **RegistrationForm.LABEL_STYLE)
        self.style.configure("TEntry", **RegistrationForm.ENTRY_STYLE)'''

        self.db = db
        self.photo_path = ctk.StringVar()
        self.create_widgets()
        self.photo_image = None  # Для хранения объекта PhotoImage фотографии

        # Устанавливаем размеры окна
        self.root.minsize(500, 400)
        self.root.maxsize(800, 600)

    def create_widgets(self):
        container_frame = ctk.CTkFrame(self.root)
        container_frame.pack(fill="both", expand=True, padx=10, pady=10)

        for i, frame in enumerate([
            ctk.CTkFrame(container_frame),
            ctk.CTkFrame(container_frame),
            ctk.CTkFrame(container_frame),
            ctk.CTkFrame(container_frame),
            ctk.CTkFrame(container_frame)
        ]):
            frame.grid(row=i, column=0, columnspan=2, sticky='ew')

            if i == 0:
                ctk.CTkLabel(frame, text="Имя:").grid(row=0, column=0, sticky=tk.W)
                self.name_entry = ctk.CTkEntry(frame)
                self.name_entry.grid(row=0, column=1, columnspan=2, sticky='ew', pady=5)
            elif i == 1:
                ctk.CTkLabel(frame, text="Дата рождения (ДД.ММ.ГГГГ):").grid(row=0, column=0, sticky=tk.W, padx=5)
                self.dob_entry = ctk.CTkEntry(frame)
                self.dob_entry.grid(row=0, column=1, columnspan=2, sticky='ew', pady=5, padx=5)
            elif i == 2:
                ctk.CTkLabel(frame, text="Пароль:").grid(row=0, column=0, sticky=tk.W)
                self.password_entry = ctk.CTkEntry(frame, show="*")
                self.password_entry.grid(row=0, column=1, sticky='ew', pady=5)

                self.show_password_var = tk.BooleanVar()
                self.show_password_checkbox = ctk.CTkCheckBox(frame, text="Показать пароль", variable=self.show_password_var, command=self.toggle_password_visibility)
                self.show_password_checkbox.grid(row=0, column=2, sticky='ew', pady=5)
            elif i == 3:
                ctk.CTkLabel(frame, text="Подтвердите пароль:").grid(row=0, column=0, sticky=tk.W)
                self.confirm_password_entry = ctk.CTkEntry(frame, show="*")
                self.confirm_password_entry.grid(row=0, column=1, columnspan=2, sticky='ew', pady=5)
            elif i == 4:
                self.upload_button = ctk.CTkButton(frame, text="Загрузить фото", command=lambda: (self.upload_photo(), self.show_cross_image()))
                self.upload_button.grid(row=1, column=0, sticky='ew', pady=5)

                self.photo_display_label = tk.Label(frame)
                self.photo_display_label.grid(row=1, column=1, sticky='ew', pady=5)

                self.register_button = ctk.CTkButton(container_frame, text="Зарегистрироваться", command=self.complete_registration)
                self.register_button.grid(row=5, column=0, columnspan=2, sticky='ew', pady=5)

                self.exit_button = ctk.CTkButton(container_frame, text="Выход", command=self.root.destroy)
                self.exit_button.grid(row=7, column=0, columnspan=2, sticky='ew', pady=5)

                # Метка для отображения крестика
                self.cross_image = self.load_cross_image()
                self.cross_label = tk.Label(self.root, image=self.cross_image)
                self.cross_label.place(relx=1.0, rely=0.0, anchor='ne', x=-20, y=20)
                self.cross_label.bind('<Button-1>', self.cancel_photo)

        self.upload_button.configure(command=lambda: (self.upload_photo(), self.show_cross_image()))

    def convert_image_to_binary(self):
        with open(self.file_path, 'rb') as file:
            blob_data = file.read()
        return blob_data
    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")
    def load_cross_image(self):
        # Загружаем изображение и изменяем его размер
        image = Image.open("static/cross.png")
        resized_image = image.resize((20, 20), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(resized_image)  # Кнопка исчезает
    file_path = ""
    def upload_photo(self):
    # Функция для загрузки фотографии
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.photo_path = self.file_path
            self.display_photo(self.file_path)
            # Теперь крестик будет отображаться только после загрузки фото
            self.show_cross_image()

    def show_cross_image(self):
        # Отображение крестика для удаления фотографии
        # Координаты x и y устанавливаются так, чтобы крестик был в углу фотографии
        self.cross_label.place(in_=self.photo_display_label, relx=1.25, rely=0.0, anchor='ne')

    
    def display_photo(self, file_path):
        # Отображение фотографии
        with Image.open(file_path) as image:
           
            image = image.resize((100, 100), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.photo_display_label.configure(image=photo)
            self.photo_display_label.image = photo
            # Перемещаем крестик в угол фотографии
            self.cross_label.place(in_=self.photo_display_label, relx=1.0, rely=0.0, anchor='ne')
    
    def cancel_photo(self, event):
        # Функция для удаления фотографии
        self.photo_path = ''  # Очистка пути к фото
        self.photo_display_label.configure(image='')
        self.cross_label.place_forget()
    def complete_registration(self):
        # Проверка данных и сохранение в БД
        name = self.name_entry.get()
        dob = self.dob_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        photo = self.photo_path

        if not self.validate_date(dob):
            messagebox.showerror("Ошибка", "Введите дату в формате ДД.ММ.ГГГГ")
            return
        if not self.validate_password(password):
            messagebox.showerror("Ошибка", "Пароль должен быть не менее 8 символов и содержать цифры и буквы")
            return
        if password != confirm_password:
            messagebox.showerror("Ошибка", "Пароли не совпадают")
            return

        # Предполагаем, что метод insert_user принимает отдельные аргументы
        self.db.insert_user(name, dob, password, self.convert_image_to_binary())
        messagebox.showinfo("Успех", "Регистрация завершена")
        self.root.destroy()
   
    def validate_password(self, password):
        if len(password) < 8 or not re.search(r"\d", password) or not re.search(r"[A-Za-z]", password):
            return False
        return True
    
    def validate_date(self, date_text):
        pattern = r"^\d{2}\.\d{2}\.\d{4}$"
        return re.match(pattern, date_text) is not None