import tkinter as tk
from tkinter import ttk
import datetime
from ticket_form import TicketForm
from ticket_edit_form import TicketEditForm
import statistics_window
class ApplicationWindow:
    def __init__(self, master, db, current_user, root):
        self.master = master
        self.root = root
        self.db = db
        self.current_user = current_user
        self.ticket_labels = []
        self.edit_buttons = []
        self.delete_buttons = []


        self.label_current_user = tk.Label(master, text="Добро пожаловать, {}!".format(self.current_user), font=("Arial", 12))
        self.label_current_user.pack()
        self._create_widgets()
        self.update_ticket_info()
        self.update_datetime()

    def _create_widgets(self):
        self.master.title("Управление заявками")
        self.master.geometry("800x600")

        # Стилизация
        style = ttk.Style()
        style.theme_use('clam')  # Выбираем одну из доступных тем
        style.configure("TButton", foreground="white", background="#4CAF50", font=("Arial", 12))
        style.configure("TLabel", background="#eee", font=("Arial", 12))

        style.map("TButton",
          foreground=[('pressed', 'white'), ('active', 'white')],
          background=[('pressed', '#388E3C'), ('active', '#66BB6A')],
          font=[('pressed', ("Arial", 12, 'bold')), ('active', ("Arial", 12, 'bold'))]
         )
        self.top_frame = tk.Frame(self.master, bg="#333")
        self.top_frame.pack(fill=tk.X)

        self.btn_create_ticket = ttk.Button(self.top_frame, text="Создать заявку", command=self.create_ticket)
        self.btn_create_ticket.pack(side=tk.LEFT, padx=10, pady=5)

        self.btn_statistics = ttk.Button(self.top_frame, text="Статистика", command=self.open_statistics_window)
        self.btn_statistics.pack(side=tk.LEFT, padx=10, pady=5)

        self.back_to_main_button = ttk.Button(self.top_frame, text="Назад", command=self.back_to_main)
        self.back_to_main_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.btn_logout = ttk.Button(self.top_frame, text="Выйти", command=self.logout)
        self.btn_logout.pack(side=tk.RIGHT, padx=10, pady=5)

        self.search_frame = tk.Frame(master=self.master, bg="#333")
        self.search_frame.pack(fill=tk.X)

        self.search_label = ttk.Label(self.search_frame, text="Поиск заявок", style="TLabel")
        self.search_label.pack(side=tk.LEFT, padx=10, pady=5)

        self.search_entry = ttk.Entry(self.search_frame, style="TEntry", textvariable="Поиск")
        
        self.search_entry.pack(side=tk.LEFT, padx=(10, 0), pady=5, fill=tk.X, expand=True)


        # Search button
        self.search_button = ttk.Button(self.search_frame, text="Найти", command=self.search_tickets).pack(side=tk.RIGHT, padx=10, pady=5)

        # Виджет для отображения текущей даты и времени
        self.label_datetime = ttk.Label(self.master, text="", style="TLabel")
        self.label_datetime.pack(pady=10)

        # Фрейм для отображения заявок
        self.ticket_frame = tk.Frame(self.master, bg="#eee")
        self.ticket_frame.pack(fill=tk.BOTH, expand=True)

    def create_ticket(self):
        current_datetime = datetime.datetime.now()
        latest_ticket = self.db.get_latest_ticket()
        ticket_window = tk.Toplevel(self.master)
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
        ticket_window = tk.Toplevel(self.master)
        ticket_window.title("Редактирование записи")

        # Анимация затухания
        ticket_window.attributes('-alpha', 0)
        self.fade_in(ticket_window)

        ticket_edit_form = TicketEditForm(ticket_window, self.db, ticket_id, self)

    def delete_ticket(self, ticket_id):
        self.db.delete_ticket(ticket_id)
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
        for ticket in tickets:
            ticket_info = self._get_ticket_info(ticket)
            label = tk.Label(self.ticket_frame, text=ticket_info, bg="#eee", font=("Arial", 12))
            label.pack(fill=tk.X, padx=10, pady=5)
            self.ticket_labels.append(label)
            self._create_edit_button(ticket)
            self._create_delete_button(ticket)

    def _get_ticket_info(self, ticket):
        info = f"Заявка №: {ticket[0]}\nОборудование: {ticket[1]}\nТип неисправности: {ticket[2]}\nОписание проблемы: {ticket[3]}\nКлиент: {ticket[4]}\nСтатус: {ticket[5]}\nДата и время создания: {ticket[6]}"
        if ticket[8]:
            info += f"\nДата и время выполнения: {ticket[8]}"
        return info

    def _create_edit_button(self, ticket):
        button = ttk.Button(self.ticket_frame, text="Редактировать", command=lambda t=ticket[0]: self.edit_ticket(t))
        button.pack(side=tk.LEFT, padx=(10, 5), pady=5)
        self.edit_buttons.append(button)

    def _create_delete_button(self, ticket):
        button = ttk.Button(self.ticket_frame, text="Удалить", command=lambda t=ticket[0]: self.delete_ticket(t))
        button.pack(side=tk.LEFT, padx=(0, 10), pady=5)
        self.delete_buttons.append(button)

    def update_ticket_info(self):
        self.remove_edit_buttons()
        self.remove_delete_buttons()
        self._clear_ticket_labels()
        tickets = self.db.get_all_tickets()
        for ticket in tickets:
            self._display_ticket_info(ticket)

    def _display_ticket_info(self, ticket):
        ticket_info = self._get_ticket_info(ticket)
        label = tk.Label(self.ticket_frame, text=ticket_info, bg="#eee", font=("Arial", 12))
        label.pack(fill=tk.X, padx=10, pady=5)
        self.ticket_labels.append(label)
        self._create_edit_button(ticket)
        self._create_delete_button(ticket)

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
        self.label_datetime.config(text=current_datetime)
        self.master.after(1000, self.update_datetime)

    def logout(self):
        self.master.destroy()
        self.root.destroy()
        
    def back_to_main(self):
        self.master.destroy()
        self.root.deiconify()