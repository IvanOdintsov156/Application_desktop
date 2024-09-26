import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter as ctk
class EditProfile:
    def __init__(self, master, db, user):
        self.db = db
        self.user = user
        
        self.window = master
        self.window.iconbitmap("static/icon.ico")
        self.window.title("Редактирование профиля")
        self.label_frame = ctk.CTkFrame(self.window, )
        self.label_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=(5, 10))

        self.create_labels_and_entries()

        self.photo_frame = ctk.CTkFrame(self.window, )
        self.photo_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=(10, 5))

        self.create_photo_frame()

        self.cross_label = tk.Label(self.window, image=self.load_cross_image())
        self.cross_label.grid(row=4, column=2, padx=5, pady=5, sticky=tk.NE)

        self.button_save = ctk.CTkButton(self.window, text="Сохранить", command=self.save)
        self.button_save.grid(row=5, column=0, columnspan=2, padx=5, pady=(10, 10), sticky=tk.EW)

        '''style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0")'''

    def create_labels_and_entries(self):
        """Создаем поля ввода для имени пользователя, старого пароля, нового пароля и даты рождения"""
        label_username = ctk.CTkLabel(self.label_frame, text="Имя пользователя:" )# font=("Arial", 12))
        label_username.grid(row=0, column=0, padx=5, pady=(0, 10), sticky=tk.W)

        self.entry_username = ctk.CTkEntry(self.label_frame, width=30)
        self.entry_username.grid(row=0, column=1, padx=5, pady=(0, 10), sticky=tk.E)
        self.entry_username.insert(0, self.user[1])

        label_old_password = ctk.CTkLabel(self.label_frame, text="Старый пароль:" )# font=("Arial", 12))
        label_old_password.grid(row=1, column=0, padx=5, pady=(0, 10), sticky=tk.W)

        self.entry_old_password = ctk.CTkEntry(self.label_frame, width=30, show=self.user[3])
        self.entry_old_password.grid(row=1, column=1, padx=5, pady=(0, 10), sticky=tk.E)
        self.entry_old_password.insert(0, self.user[3])

        label_new_password = ctk.CTkLabel(self.label_frame, text="Новый пароль:" )# font=("Arial", 12))
        label_new_password.grid(row=2, column=0, padx=5, pady=(0, 10), sticky=tk.W)

        self.entry_password = ctk.CTkEntry(self.label_frame, width=30, show="*")
        self.entry_password.grid(row=2, column=1, padx=5, pady=(0, 10), sticky=tk.E)

        label_date_of_birth = ctk.CTkLabel(self.label_frame, text="Дата рождения:" )# font=("Arial", 12))
        label_date_of_birth.grid(row=3, column=0, padx=5, pady=(0, 10), sticky=tk.W)

        self.entry_date_of_birth = ctk.CTkEntry(self.label_frame, width=30)
        self.entry_date_of_birth.grid(row=3, column=1, padx=5, pady=(0, 10), sticky=tk.E)
        self.entry_date_of_birth.insert(0, self.user[2])

    def convert_image_to_binary(self):
        with open(self.file_path, 'rb') as file:
            blob_data = file.read()
        return blob_data
    file_path = ""
    def create_photo_frame(self):
        """Создаем рамку для фотографии"""
        label_photo = ctk.CTkLabel(self.photo_frame, text="Фотография:")# font=("Arial", 12))
        label_photo.grid(row=0, column=0, padx=5, pady=(0, 10), sticky=tk.W)

        self.photo_display_label = tk.Label(self.photo_frame, width=100)
        self.photo_display_label.grid(row=1, column=0, columnspan=2, padx=5, pady=(0, 10), sticky=tk.EW)

        self.button_photo = ctk.CTkButton(self.photo_frame, text="Выберите файл", command=self.upload_photo)
        self.button_photo.grid(row=2, column=0, columnspan=2, padx=5, pady=(0, 10), sticky=tk.EW)

    def save(self):
        """Сохранение изменений в БД"""
        username = self.entry_username.get()
        date_of_birth = self.entry_date_of_birth.get()
        photo_path = self.photo_path
        password = self.entry_password.get()
        self.user_id = self.user[0]

        if password != "":
            self.db.update_user(self.user_id,username, date_of_birth, password, self.convert_image_to_binary())
        else:
            self.db.update_user(self.user_id,username, date_of_birth, self.user[3], self.convert_image_to_binary())
        self.window.destroy()


    def upload_photo(self):
        """Функция для загрузки фотографии"""
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.photo_path = self.file_path
            self.display_photo(self.file_path)
            # Теперь крестик будет отображаться только после загрузки фото
            self.show_cross_image_after_photo_display()

    def show_cross_image_after_photo_display(self):
        """Отображение крестика для удаления фотографии"""
        # Координаты x и y устанавливаются так, чтобы крестик был в угле фотографии
        self.cross_label.grid(row=2, column=2, sticky=tk.NE, padx=5, pady=5)

    def load_cross_image(self):
        """Загружаем изображение и изменяем его размер"""
        image = Image.open("static/cross.png")
        resized_image = image.resize((20, 20), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(resized_image)


    def display_photo(self, file_path):
        """Отображение фотографии"""
        # Отображение фотографии
        with Image.open(file_path) as image:
            image = image.resize((300, 300), Image.LANCZOS)
                
            # Convert the PIL image to a format suitable for CTkLabel
            photo_image = ImageTk.PhotoImage(image)
            
            
            self.photo_display_label.config(image=photo_image)
                # Keep a reference to the photo
            self.photo_display_label.image = photo_image
            # Перемещаем крестик в угол фотографии
            self.cross_label.place(relx=1.0, rely=0.0, anchor='ne')

    def cancel_photo(self, event):
        """Функция для удаления фотографии"""
        # Очистка пути к фото
        self.photo_path = ''
        # Убире крестик
        self.cross_label.grid_forget()
        # Убире фотографию
        self.photo_display_label.configure(image='')


