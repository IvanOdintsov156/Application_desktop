import tkinter as tk
from tkinter import ttk
import datetime
from ticket_form import TicketForm
from ticket_edit_form import TicketEditForm
import statistics_window
from dashboard.profile_panel import ProfilePanel
import customtkinter as ctk
class ApplicationWindow:
    def __init__(self, master, db, current_user, root):
        self.master = master
        self.root = root
        self.db = db
        self.current_user = current_user
        
        self.ticket_labels = []
        self.edit_buttons = []
        self.delete_buttons = []
        self.ticket_frames = []

        self.master.iconbitmap("static/icon.ico")
        ProfilePanel(self.master, self.current_user, self.db)
        self._create_widgets()
        self.update_ticket_info()
        self.update_datetime()

    def _create_widgets(self):
        self.master.title("Управление заявками")
        self.master.geometry("800x600")

        ''' # Стилизация
        style = ttk.Style()
        style.theme_use('clam')  # Выбираем одну из доступных тем
        style.configure("TButton", foreground="white", background="#4CAF50", )# font=("Arial", 12))
        style.configure("TLabel", background="#eee", )# font=("Arial", 12))

        style.map("TButton",
          foreground=[('pressed', 'white'), ('active', 'white')],
          background=[('pressed', '#388E3C'), ('active', '#66BB6A')],
          font=[('pressed', ("Arial", 12, 'bold')), ('active', ("Arial", 12, 'bold'))]
         )'''
        self.top_frame = ctk.CTkFrame(self.master) # bg="#333")
        self.top_frame.pack(fill=tk.X)

        self.btn_create_ticket = ctk.CTkButton(self.top_frame, text="Создать заявку", command=self.create_ticket)
        self.btn_create_ticket.pack(side=tk.LEFT, padx=10, pady=5)

        self.btn_statistics = ctk.CTkButton(self.top_frame, text="Статистика", command=self.open_statistics_window)
        self.btn_statistics.pack(side=tk.LEFT, padx=10, pady=5)

        self.back_to_main_button = ctk.CTkButton(self.top_frame, text="Назад", command=self.back_to_main)
        self.back_to_main_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.btn_logout = ctk.CTkButton(self.top_frame, text="Выйти", command=self.logout)
        self.btn_logout.pack(side=tk.RIGHT, padx=10, pady=5)

        self.search_frame = ctk.CTkFrame(master=self.master) # bg="#333")
        self.search_frame.pack(fill=tk.X)

        self.search_label = ctk.CTkLabel(self.search_frame, text="Поиск заявок", )
        self.search_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Используем StringVar для связывания с Entry
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(self.search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, padx=(10, 0), pady=5, fill=tk.X, expand=True)

        # Создаем кнопку поиска отдельно
        self.search_button = ctk.CTkButton(self.search_frame, text="Найти", command=self.search_tickets)
        self.search_button.pack(side=tk.RIGHT, padx=10, pady=5)

        # Виджет для отображения текущей даты и времени
        self.label_datetime = ctk.CTkLabel(self.master, text="", )
        self.label_datetime.pack(pady=10)

        self.scrollable_frame = ctk.CTkFrame(self.master)
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True)
    def create_ticket(self):
        current_datetime = datetime.datetime.now()
        latest_ticket = self.db.get_latest_ticket()
        ticket_window = ctk.CTkToplevel(self.master)
        ticket_window.title("Форма заявки")

        # Анимация затухания
        ticket_window.attributes('-alpha', 0)
        self.fade_in(ticket_window)

        ticket_form = TicketForm(ticket_window, self.db, self, creation_time=current_datetime)

    def fade_in(self, window):
        alpha = 0
        while alpha < 1:
            alpha += 0.1
            window.attributes('-alpha', alpha)
            window.update_idletasks()
            window.after(50)

    def open_statistics_window(self):
        statistics_window.create_statistics_window(self.db)

    def edit_ticket(self, ticket_id):
        ticket = self.db.get_ticket_by_id(ticket_id)
        ticket_window = ctk.CTkToplevel(self.master)
        ticket_window.title("Редактирование записи")

        # Анимация затухания
        ticket_window.attributes('-alpha', 0)
        self.fade_in(ticket_window)

        ticket_edit_form = TicketEditForm(ticket_window, self.db, ticket_id, self)

    def delete_ticket(self, ticket_id, frame):
         # Удаление заявки из базы данных
        self.db.delete_ticket(ticket_id)
        
        # Удаление фрейма заявки и всех его дочерних виджетов
        for widget in frame.winfo_children():
            widget.destroy()
        frame.destroy()
        
        # Обновление canvas и его содержимого
        self.canvas.update_idletasks()
        
        # Обновление списка заявок, если это необходимо
        self.update_ticket_info()
    def search_tickets(self):
        search_query = self.search_entry.get()
        if search_query:
            tickets = self.db.search_tickets(search_query)
            self.display_search_results(tickets)

    def display_search_results(self, tickets):
        self.remove_edit_buttons()
        self.remove_delete_buttons()
        self._clear_ticket_labels()
        self._display_tickets(tickets)

    def _get_ticket_info(self, ticket):
        info = f"Заявка №: {ticket[1]}\nОборудование: {ticket[2]}\nТип неисправности: {ticket[3]}\nОписание проблемы: {ticket[4]}\nКлиент: {ticket[5]}\nСтатус: {ticket[6]}\nДата и время создания: {ticket[7]}"
        if ticket[8]:
            info += f"\nДата и время выполнения: {ticket[8]}"
        return info

    def _create_edit_button(self, ticket, frame):
        edit_button = ctk.CTkButton(frame, text="Редактировать", command=lambda: self.edit_ticket(ticket[0]))
        edit_button.pack(side=tk.RIGHT, padx=10, pady=5)
        self.edit_buttons.append(edit_button)

    def _create_delete_button(self, ticket, frame):
        delete_button = ctk.CTkButton(frame, text="Удалить", command=lambda: self.delete_ticket(ticket[0], frame))
        delete_button.pack(side=tk.RIGHT, padx=10, pady=5)
        self.delete_buttons.append(delete_button)

    def update_ticket_info(self):
            # Удаляем старые виджеты заявок
        for frame in self.ticket_frames:
            frame.destroy()
        self.ticket_frames.clear()
        self.edit_buttons.clear()
        self.delete_buttons.clear()

        # Заново создаем виджеты заявок с обновленной информацией
        tickets = self.db.get_all_tickets()  # Предполагается, что здесь происходит запрос к БД
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

            label = ctk.CTkLabel(ticket_frame, text=self._get_ticket_info(ticket))# font=("Arial", 12))
            label.pack(side=tk.LEFT, fill=tk.X, expand=True)

            self._create_edit_button(ticket, ticket_frame)
            self._create_delete_button(ticket, ticket_frame)

        self.tickets_frame.update_idletasks()  # Обновление задач в состоянии ожидания
        self.canvas.config(scrollregion=self.canvas.bbox("all"))  
    def remove_edit_buttons(self):
        for button in self.edit_buttons:
            button.destroy()
        self.edit_buttons = []

    def remove_delete_buttons(self):
        for button in self.delete_buttons:
            button.destroy()
        self.delete_buttons = []

    def _clear_ticket_labels(self):
        for label in self.ticket_labels:
            label.destroy()
        self.ticket_labels = []

    def update_datetime(self):
        current_datetime = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.label_datetime.configure(text=current_datetime)
        self.master.after(1000, self.update_datetime)

    def logout(self):
        self.master.destroy()
        self.root.destroy()

    def back_to_main(self):
        self.master.destroy()
        self.root.deiconify()