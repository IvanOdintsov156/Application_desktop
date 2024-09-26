import tkinter as tk
from tkinter import ttk
from datetime import datetime
from ticket_edit_status_form import TicketEditStatusForm
import customtkinter as ctk

from dashboard.profile_panel import ProfilePanel

class SpecialWindow:
    def __init__(self, master, database, current_user, authentication_window):
        self.master = master
        self.current_user = current_user
        self.authentication_window = authentication_window
        self.database = database
        self.master.iconbitmap("static/icon.ico")
        ProfilePanel(self.master, self.current_user, self.database)
        self._create_widgets()
        self.update_datetime()

    def _create_widgets(self):
        self.master.title("Управление заявками")
        self.master.geometry("800x600")
        self.master.resizable(False, False)

        '''# Стилизация
        style = ttk.Style()
        style.theme_use('clam')  # Выбираем одну из доступных тем
        style.configure("TButton", foreground="white", background="#4CAF50", )# font=("Arial", 12))
        style.configure("TLabel", background="#eee", )# font=("Arial", 12))

        style.map("TButton",
          foreground=[('pressed', 'white'), ('active', 'white')],
          background=[('pressed', '#388E3C'), ('active', '#66BB6A')],
          font=[('pressed', ("Arial", 12, 'bold')), ('active', ("Arial", 12, 'bold'))]
         )'''
        
        # Top frame with buttons
        self.top_frame = ctk.CTkFrame(self.master) #) # bg="#333")
        self.top_frame.pack(fill=tk.X)
        
        self.back_to_main_button = ctk.CTkButton(self.top_frame, text="Назад", command=self.back_to_main)
        self.back_to_main_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.logout_button = ctk.CTkButton(self.top_frame, text="Выйти", command=self.logout)
        self.logout_button.pack(side=tk.RIGHT, padx=10, pady=5)

        # Search panel
        self.search_frame = ctk.CTkFrame(master=self.master) # bg="#333")
        self.search_frame.pack(fill=tk.X)

        self.search_label = ctk.CTkLabel(self.search_frame, text="Поиск заявок", )
        self.search_label.pack(side=tk.LEFT, padx=10, pady=5)

        self.search_entry = ctk.CTkEntry(self.search_frame, textvariable=tk.StringVar())
        self.search_entry.pack(side=tk.LEFT, padx=(10, 0), pady=5, fill=tk.X, expand=True)

        # Separate creation and packing of the search_button
        self.search_button = ctk.CTkButton(self.search_frame, text="Найти", command=self.search_tickets)
        self.search_button.pack(side=tk.RIGHT, padx=10, pady=5)

        # Widget to display current date and time
        self.datetime_label = ctk.CTkLabel(self.master, text="", )
        self.datetime_label.pack(pady=10)

        self.scrollable_frame = ctk.CTkFrame(self.master)
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True)

    def _create_label(self, text, style):
        label = ctk.CTkLabel(self.master, text=text, style=style)
        label.pack(padx=5, pady=5, fill=tk.X)
        return label

    def _create_button(self, text, command, style):
        button = ctk.CTkButton(self.master, text=text, command=command, style=style)
        button.pack(padx=5, pady=5)
        return button

    def update_datetime(self):
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.datetime_label.configure(text=current_datetime)
        self.master.after(1000, self.update_datetime)

    def search_tickets(self):
        search_query = self.search_entry.get()
        # Assuming the database.search_tickets method returns a list of tuples as search results.
        tickets = self.database.search_tickets(search_query)
        self._display_tickets(tickets)

    def update_tickets_display(self):
        tickets = self.database.get_all_tickets()
        self._display_tickets(tickets)

    def _display_tickets(self, tickets):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Создание скроллинга для canvas
        self.scrollbar = ctk.CTkScrollbar(self.scrollable_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = ctk.CTkCanvas(self.scrollable_frame, yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar.configure(command=self.canvas.yview)

        # Создание фрейма для заявок внутри canvas
        self.tickets_frame = ctk.CTkFrame(self.canvas)
        self.tickets_frame.pack(fill=tk.BOTH, expand=True)
        self.canvas.create_window((0, 0), window=self.tickets_frame, anchor="nw")

        # Отображение заявок в tickets_frame
        for ticket in tickets:
            ticket_frame = ctk.CTkFrame(self.tickets_frame)
            ticket_frame.pack(fill=tk.X, padx=10, pady=5)

            ticket_info = f"Заявка №: {ticket[1]}\nОборудование: {ticket[2]}\nТип неисправности: {ticket[3]}\nОписание проблемы: {ticket[4]}\nКлиент: {ticket[5]}\nСтатус: {ticket[6]}\nДата и время создания: {ticket[7]}"
            if len(ticket) > 8 and ticket[8]:
                ticket_info += f"\nДата и время выполнения: {ticket[8]}"

            label = ctk.CTkLabel(ticket_frame, text=ticket_info)# font=("Arial", 12))
            label.pack(side=tk.LEFT, fill=tk.X, expand=True)

            edit_button = ctk.CTkButton(ticket_frame, text="Изменить статус", command=lambda ticket_id=ticket[0]: self.edit_ticket_status(ticket_id))
            edit_button.pack(side=tk.RIGHT, padx=10)

        self.tickets_frame.update_idletasks()  # Обновление задач в состоянии ожидания
        self.canvas.config(scrollregion=self.canvas.bbox("all"))  

    def edit_ticket_status(self, ticket_id):
        ticket_edit_status_window = ctk.CTkToplevel(self.master)
        
        ticket_edit_status_window.configure(bg="#f0f0f0")
        ticket_edit_status_window.title("Изменение статуса заявки")
        ticket_edit_status_form = TicketEditStatusForm(ticket_edit_status_window, self.database, 
                                                       ticket_id, self)

    def back_to_main(self):
        self.master.destroy()
        self.authentication_window.deiconify()

    def logout(self):
        self.master.destroy()
        self.authentication_window.destroy()