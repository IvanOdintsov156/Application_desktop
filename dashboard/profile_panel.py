import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from .edit_profile import EditProfile
import io
import customtkinter as ctk
class ProfilePanel:
    

    def __init__(self, master, username, database):
        self.master = master
        self.username = username
        self.database = database

        '''style = ttk.Style()
        style.theme_use('clam')  # Выбираем одну из доступных тем

        # Configure style for TButton
        style.configure("TButton", foreground="white", background="#4CAF50", )# font=("Arial", 12))
        style.map("TButton",
          foreground=[('pressed', 'white'), ('active', 'white')],
          background=[('pressed', '#388E3C'), ('active', '#66BB6A')],
          font=[('pressed', ("Arial", 12, 'bold')), ('active', ("Arial", 12, 'bold'))]
         )

        # Configure style for TLabel
        style.configure("TLabel", background="#eee", )# font=("Arial", 12))
'''
        self.user_data = self.database.get_user_by_username(username)
        self.profile_frame = ctk.CTkFrame(master)
        self.profile_frame.pack(fill=tk.BOTH, expand=True)

        self.profile_header = ctk.CTkFrame(self.profile_frame)
        self.profile_header.pack(fill=tk.X, padx=5, pady=5)

        self.welcome_label = ctk.CTkLabel(self.profile_header, text="Добро пожаловать, {}!".format(username), )# font=("Arial", 12))
        self.welcome_label.pack(side=tk.LEFT)
        self.profile_content_frame = None
        self.profile_header_button = ctk.CTkButton(self.profile_header, text="Открыть профиль", command=lambda: self.open_profile_without_editing())
        self.profile_header_button.pack(side=tk.RIGHT)

        self.edit_button_frame = ctk.CTkFrame(self.profile_header )
        self.edit_button_frame.pack(side=tk.RIGHT, padx=5, pady=5)
        self.edit_button = ctk.CTkButton(self.edit_button_frame, text="Изменить данные", command=lambda: self.open_edit_profile(self.user_data))
        self.edit_button.grid(row=0, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))

    def open_profile_without_editing(self):
            if self.profile_content_frame is not None:
                self.profile_content_frame.destroy()
            self.profile_content_frame = ctk.CTkFrame(self.profile_frame)
            self.profile_content_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

            user_data = self.database.get_user_by_username(self.username)

            self.profile_content_frame.grid_rowconfigure(0, weight=1)
            self.profile_content_frame.grid_columnconfigure(0, weight=1)
            self.photo_frame = ctk.CTkFrame(self.profile_content_frame)
            self.photo_frame.grid(row=0, column=0, sticky=(tk.N, tk.E, tk.S, tk.W))

            self.photo_label = tk.Label(self.photo_frame)
            self.photo_label.grid(row=0, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=(10, 10))

            if user_data[4] is not None:
                with Image.open(io.BytesIO(user_data[4])) as image:
                    image_resized = image.resize((300, 300), Image.LANCZOS)
                    
                    # Convert the PIL image to a format suitable for CTkLabel
                    photo = ImageTk.PhotoImage(image_resized)
                    
                    # Configure the label with the CTkImage
                    self.photo_label.configure(image=photo)
                    # Keep a reference to the photo
                    self.photo_label.image = photo
            else:
                self.photo_label.configure(text="Фото отсутствует")

            self.info_frame = ctk.CTkFrame(self.profile_content_frame)
            self.info_frame.grid(row=0, column=1, sticky=(tk.N, tk.E, tk.S, tk.W))

            self.name_label = ctk.CTkLabel(self.info_frame, text="Имя: {}".format(user_data[1]))  # font=("Arial", 12)
            self.name_label.grid(row=0, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=(10, 10))

            self.password_label = ctk.CTkLabel(self.info_frame, text="Пароль: "+"*"*len(user_data[3]), font=("Arial", 12), wraplength=300)
            self.password_label.grid(row=2, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=(10, 10))

            self.show_password_var = ctk.BooleanVar()
            self.show_password_checkbox = ctk.CTkCheckBox(self.info_frame, text="Показать пароль", variable=self.show_password_var, command=lambda: self.toggle_password_visibility(user_data, self.show_password_var, self.password_label))
            self.show_password_checkbox.grid(row=2, column=1, sticky='ew', pady=(10, 10))

            self.birth_date_label = ctk.CTkLabel(self.info_frame, text="Дата рождения: {}".format(user_data[2]))  # font=("Arial", 12)
            self.birth_date_label.grid(row=1, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), pady=(10, 10))

            self.button_frame = ctk.CTkFrame(self.profile_content_frame)
            self.button_frame.grid(row=1, column=1, sticky=(tk.N, tk.E, tk.S, tk.W), pady=(10, 10))

            self.close_button = ctk.CTkButton(self.button_frame, text="Закрыть", command=self.close_profile)
            self.close_button.grid(row=0, column=0, sticky=(tk.N, tk.E, tk.S, tk.W), padx=5)
            self.edit_button = ctk.CTkButton(self.button_frame, text="Изменить данные", command=lambda: self.open_edit_profile(self.user_data))
            self.edit_button.grid(row=0, column=1, sticky=(tk.N, tk.E, tk.S, tk.W), padx=5)

    def toggle_password_visibility(self, user_data, show_password_var, password_label):
        if show_password_var.get():
            password_label.configure(text="Пароль: "+user_data[3])
        else:
            password_label.configure(text="Пароль: "+"*"*len(user_data[3]))

    def close_profile(self):
        """Close profile panel """
        self.profile_content_frame.pack_forget()
        self.close_button.grid_forget()
        self.profile_content_frame.destroy()

    def open_edit_profile(self, user_data):
        """Edit profile data """
        self.edit_profile = ctk.CTkToplevel(self.master)

        EditProfile(self.edit_profile, self.database, user_data)
