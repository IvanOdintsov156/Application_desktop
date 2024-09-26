import tkinter as tk
from auth_window import AuthWindow
import customtkinter as ctk
def main():
    ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme("themes/sky.json")
    root =ctk.CTk()
    root.iconbitmap("static/icon.ico")
    root.title("Авторизация")
    auth_window = AuthWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()